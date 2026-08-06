from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MarshalMovement(models.Model):
    """A single crate's trip from a loading dock to an exhibition booth,
    expressed as an ordered chain of chokepoint claims.
    """
    _name = "marshal.movement"
    _description = "Freight Movement"
    _inherit = ["mail.thread", "mail.activity.mixin", "marshal.idempotent.mixin"]
    _order = "id desc"

    name = fields.Char(default=lambda self: _("New"), copy=False,
                       readonly=True, index=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        ("cancelled", "Cancelled"),
    ], default="draft", required=True, tracking=True)

    crate_ref = fields.Char(string="Crate Reference", tracking=True)
    dest_booth = fields.Char(string="Destination Booth", tracking=True)
    equipment_id = fields.Many2one("maintenance.equipment", string="Equipment")
    operator_id = fields.Many2one("hr.employee", string="Operator")

    planned_start = fields.Datetime()
    planned_end = fields.Datetime(
        help="Comparator rule 5 (earliest due) and the reference for rule 6 "
             "(least slack).")
    actual_start = fields.Datetime()
    actual_end = fields.Datetime()

    variance_reason = fields.Selection([
        ("delay_traffic", "Delay — traffic / congestion"),
        ("delay_equipment", "Delay — equipment fault"),
        ("delay_operator", "Delay — operator unavailable"),
        ("delay_buffer_full", "Delay — downstream buffer full"),
        ("delay_foreign", "Delay — foreign resource occupied"),
        ("reroute", "Rerouted"),
        ("other", "Other"),
    ], string="Variance Reason",
        help="Coded, not free text — this is what makes actuals analysable.")

    hard_deadline = fields.Datetime(
        help="COMPARATOR RULE 1. An external deadline we cannot move, e.g. "
             "hall opens 09:00. A movement with one outranks a movement "
             "without; between two, the earlier wins.")
    priority_class = fields.Selection([
        ("expedite", "Expedite"),
        ("normal", "Normal"),
        ("opportunistic", "Opportunistic"),
    ], default="normal", required=True,
        help="COMPARATOR RULE 4. Set by a human, deliberately — if everyone "
             "can self-declare expedite, this rule is worthless.")

    is_blocking = fields.Boolean(
        string="Blocking / safety",
        help="COMPARATOR RULE 2. True when delaying this movement leaves an "
             "obstruction — a crate in a fire lane, an aisle blocked. "
             "Clearing an obstruction outranks starting new work.")

    claim_ids = fields.One2many("marshal.claim", "movement_id", string="Claims")
    dlq_ids = fields.One2many("marshal.dlq", "movement_id", string="Blockages")
    event_ids = fields.One2many("marshal.event", "movement_id", string="Custody Log")
    chain_ok = fields.Boolean(compute="_compute_chain_ok", string="Chain intact")
    chain_detail = fields.Char(compute="_compute_chain_ok")
    dlq_open_count = fields.Integer(compute="_compute_dlq_open")
    claim_count = fields.Integer(compute="_compute_claim_count")

    @api.depends("claim_ids")
    def _compute_claim_count(self):
        for rec in self:
            rec.claim_count = len(rec.claim_ids)

    @api.depends("dlq_ids.state")
    def _compute_dlq_open(self):
        for rec in self:
            rec.dlq_open_count = len(rec.dlq_ids.filtered(lambda d: d.state == "open"))

    def _compute_chain_ok(self):
        Event = self.env["marshal.event"]
        for rec in self:
            if not rec.id:
                rec.chain_ok, rec.chain_detail = True, "no events"
                continue
            ok, bad, detail = Event.verify_chain(rec)
            rec.chain_ok = ok
            rec.chain_detail = detail if ok else f"BROKEN at seq {bad}: {detail}"

    def action_verify_chain(self):
        """Surfaced as a button — this is what you press in a dispute."""
        self.ensure_one()
        ok, bad, detail = self.env["marshal.event"].verify_chain(self)
        raise UserError(  # deliberately a dialog: the answer must be read
            f"Custody chain for {self.name}: "
            f"{'INTACT' if ok else 'BROKEN'} — {detail}")

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env["ir.sequence"]
        for vals in vals_list:
            if not vals.get("name") or vals["name"] == _("New"):
                vals["name"] = seq.next_by_code("marshal.movement") or _("New")
        records = super().create(vals_list)
        for rec in records:
            self.env["marshal.event"].record(rec, "created", {
                "crate_ref": rec.crate_ref, "dest_booth": rec.dest_booth,
                "priority_class": rec.priority_class,
            })
        return records

    def write(self, vals):
        res = super().write(vals)
        # Only state and variance are worth chaining — chaining every field
        # write would bury the signal in noise.
        if "state" in vals or "variance_reason" in vals:
            for rec in self:
                self.env["marshal.event"].record(rec, "state", {
                    k: vals[k] for k in ("state", "variance_reason") if k in vals
                })
        return res

    def _latest_claim(self):
        """The claim with the highest sequence is this movement's most recent
        state change — and since a crate can only be in one place at a time,
        that is its current physical position. Buffer occupancy depends on this.
        """
        self.ensure_one()
        return self.claim_ids.sorted(lambda c: c.sequence, reverse=True)[:1]

    def precedence_depth(self):
        """COMPARATOR RULE 3 — how many other movements are waiting on this one.

        Approximated by counting movements whose earliest unstarted claim is on
        a chokepoint this movement currently occupies. A movement that is
        holding up three others should win against one holding up none.
        """
        self.ensure_one()
        occupied = self.claim_ids.filtered(lambda c: c.state == "occupied")
        if not occupied:
            return 0
        return self.env["marshal.claim"].search_count([
            ("chokepoint_id", "in", occupied.mapped("chokepoint_id").ids),
            ("state", "in", ("proposed", "claimed", "held")),
            ("movement_id", "!=", self.id),
        ])

    def slack_seconds(self):
        """COMPARATOR RULE 6 — time until due, minus remaining work.

        Returns a large number when unknown so that movements with no stated
        due date never beat ones that have a real deadline.
        """
        self.ensure_one()
        due = self.hard_deadline or self.planned_end
        if not due:
            return float("inf")
        return (due - fields.Datetime.now()).total_seconds()

    def action_plan(self):
        self.write({"state": "planned"})

    def action_start(self):
        self.write({"state": "in_progress", "actual_start": fields.Datetime.now()})

    def action_done(self):
        self.write({"state": "done", "actual_end": fields.Datetime.now()})

    def action_cancel(self):
        self.write({"state": "cancelled"})
