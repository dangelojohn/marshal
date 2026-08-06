import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class MarshalDlq(models.Model):
    """Dead-letter queue — the "no silent failures" backbone.

    When a movement cannot be scheduled, the temptation is to raise, log, or
    quietly leave it in `draft`. All three are wrong on a dock: the coordinator
    finds out when a truck is already waiting.

    Instead every unschedulable movement lands here with a CODED reason and a
    concrete set of next actions. A blocked movement is then visible and
    actionable rather than hidden — which is the difference between a system
    that degrades and one that silently stops.

    This is also the landing zone for foreign-resource collisions (a hotel
    elevator occupied by housekeeping who never told us). Those are contention
    events to re-plan, not errors — and the accumulating record of them is the
    evidence for asking the venue for a reserved window.
    """
    _name = "marshal.dlq"
    _description = "Marshal Dead-Letter Queue"
    _inherit = ["mail.thread"]
    _order = "id desc"

    name = fields.Char(compute="_compute_name", store=True)
    movement_id = fields.Many2one(
        "marshal.movement", required=True, ondelete="cascade", index=True)
    chokepoint_id = fields.Many2one("marshal.chokepoint", ondelete="set null")

    reason_code = fields.Selection([
        ("buffer_full", "Downstream buffer full"),
        ("chokepoint_busy", "Chokepoint at capacity"),
        ("foreign_occupied", "Foreign resource occupied"),
        ("no_equipment", "No compatible equipment available"),
        ("no_operator", "No certified operator available"),
        ("cert_expired", "Operator certification expired"),
        ("lost_contention", "Lost contention to a higher-priority movement"),
        ("no_slot", "No feasible slot before the deadline"),
        ("other", "Other"),
    ], required=True, index=True,
        help="Coded, never free text. A queue you cannot group by is a inbox, "
             "not a queue.")

    detail = fields.Text(help="What actually happened, for a human.")
    suggested_actions = fields.Text(
        help="What the coordinator could do about it. Populated by the caller "
             "because only the caller knows the alternatives it considered.")

    state = fields.Selection([
        ("open", "Open"),
        ("resolved", "Resolved"),
        ("dismissed", "Dismissed"),
    ], default="open", required=True, index=True, tracking=True)

    resolved_by = fields.Many2one("res.users", readonly=True)
    resolved_on = fields.Datetime(readonly=True)
    resolution_note = fields.Text()

    @api.depends("movement_id", "reason_code")
    def _compute_name(self):
        for rec in self:
            mv = rec.movement_id.name or "?"
            rec.name = f"{mv} — {dict(self._fields['reason_code'].selection).get(rec.reason_code, '?')}"

    # ------------------------------------------------------------------
    @api.model
    def raise_entry(self, movement, reason_code, detail=None,
                    chokepoint=None, suggested=None):
        """Record a blocked movement. Never raises — the whole point is that a
        blockage becomes data rather than an exception that unwinds a job.

        Deduplicates on (movement, reason, chokepoint) while still open, so a
        retry loop cannot flood the queue with the same problem.
        """
        existing = self.search([
            ("movement_id", "=", movement.id),
            ("reason_code", "=", reason_code),
            ("chokepoint_id", "=", chokepoint.id if chokepoint else False),
            ("state", "=", "open"),
        ], limit=1)
        if existing:
            return existing

        entry = self.create({
            "movement_id": movement.id,
            "chokepoint_id": chokepoint.id if chokepoint else False,
            "reason_code": reason_code,
            "detail": detail,
            "suggested_actions": suggested,
        })
        _logger.info("marshal.dlq: %s blocked — %s%s",
                     movement.name, reason_code,
                     f" at {chokepoint.code}" if chokepoint else "")
        return entry

    def action_resolve(self, note=None):
        self.write({
            "state": "resolved",
            "resolved_by": self.env.uid,
            "resolved_on": fields.Datetime.now(),
            "resolution_note": note or self.resolution_note,
        })

    def action_dismiss(self):
        self.write({
            "state": "dismissed",
            "resolved_by": self.env.uid,
            "resolved_on": fields.Datetime.now(),
        })

    @api.model
    def open_count(self):
        """For the wall board — one number the coordinator can watch."""
        return self.search_count([("state", "=", "open")])
