from odoo import models, fields, api
from odoo.exceptions import UserError


class MarshalClaim(models.Model):
    """A movement's claim on ONE chokepoint.

    Lifecycle:  proposed -> claimed -> held -> occupied -> released
                                  \\-> yielded  (lost a contention)

    THE RULE THAT MATTERS MOST: claims are preemptible, occupancy is NOT.
    A movement scheduled for the elevator can lose the slot to something more
    urgent. A forklift physically IN the elevator cannot — that would be absurd
    and dangerous.
    """
    _name = "marshal.claim"
    _description = "Marshal Chokepoint Claim"
    _order = "sequence, id"

    movement_id = fields.Many2one("marshal.movement", required=True,
                                  ondelete="cascade", index=True)
    chokepoint_id = fields.Many2one("marshal.chokepoint", required=True,
                                    ondelete="restrict", index=True)

    sequence = fields.Integer(
        required=True, index=True, copy=False,
        help="COMPARATOR RULE 7 — the guaranteed final discriminator. "
             "Monotonic and unique. Without a tie-break that can never draw, "
             "two runs on identical data could pick different winners and the "
             "scheduler would not be reproducible. That is not a nicety: a "
             "plan you cannot reproduce cannot be defended at 6am.")

    start = fields.Datetime()
    expected_end = fields.Datetime(
        help="Use a p90 duration, not a median. Optimistic estimates on a "
             "chokepoint propagate delay to everything queued behind it.")

    state = fields.Selection([
        ("proposed", "Proposed"),
        ("claimed", "Claimed"),
        ("held", "Held"),
        ("occupied", "Occupied"),
        ("released", "Released"),
        ("yielded", "Yielded"),
    ], default="proposed", required=True, index=True, tracking=False)

    # Denormalised from the movement so the comparator can sort without
    # touching related records for every comparison.
    priority_class = fields.Selection(
        related="movement_id.priority_class", store=True, readonly=True)
    hard_deadline = fields.Datetime(
        related="movement_id.hard_deadline", store=True, readonly=True)

    buffer_ok = fields.Boolean(
        compute="_compute_buffer_ok",
        help="THE BLOCKING RULE. False when the downstream buffer is full, "
             "which means this claim must not be allowed to enter.")

    _sql_constraints = [
        ("sequence_uniq", "unique(sequence)",
         "Claim sequence must be globally unique — it is the final tie-break."),
    ]

    # ------------------------------------------------------------------
    # sequence allocation
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env["ir.sequence"]
        for vals in vals_list:
            if not vals.get("sequence"):
                vals["sequence"] = int(seq.next_by_code("marshal.claim.seq") or 1)
        return super().create(vals_list)

    # ------------------------------------------------------------------
    # THE BLOCKING RULE
    # ------------------------------------------------------------------
    @api.depends("chokepoint_id", "state")
    def _compute_buffer_ok(self):
        for claim in self:
            claim.buffer_ok = claim._downstream_has_space()

    def _downstream_has_space(self):
        """A movement may enter a chokepoint only if the DOWNSTREAM buffer has
        room for it.

        Never occupy what you cannot clear. A forklift that enters the elevator
        and finds the upper lobby full blocks the elevator for EVERYONE — and
        unlike a software transaction, you cannot roll back a crate. The lobby
        is now the problem of every movement behind it.

        No downstream buffer defined => nothing to block on (e.g. the final hop
        into the booth itself).
        """
        self.ensure_one()
        buffers = self.env["marshal.buffer"].search([
            ("upstream_ids", "in", self.chokepoint_id.id)
        ])
        if not buffers:
            return True
        return any(b.has_space for b in buffers)

    # ------------------------------------------------------------------
    # THE COMPARATOR
    # ------------------------------------------------------------------
    def _beats(self, other):
        """Return (wins, rule_number, reason).

        Seven tests, evaluated IN ORDER until one discriminates. Rule 7 can
        never draw, so this always returns a decision — that is what makes the
        scheduler reproducible.
        """
        self.ensure_one()
        other.ensure_one()
        a, b = self.movement_id, other.movement_id

        # 1. hard external deadline
        if bool(a.hard_deadline) != bool(b.hard_deadline):
            wins = bool(a.hard_deadline)
            who = a if wins else b
            return wins, 1, (
                f"{who.name} has a hard external deadline "
                f"({who.hard_deadline}) and the other does not")
        if a.hard_deadline and b.hard_deadline and a.hard_deadline != b.hard_deadline:
            wins = a.hard_deadline < b.hard_deadline
            who = a if wins else b
            return wins, 1, (
                f"{who.name} has the earlier hard deadline ({who.hard_deadline})")

        # 2. blocking / safety — clearing an obstruction outranks new work
        if a.is_blocking != b.is_blocking:
            wins = a.is_blocking
            who = a if wins else b
            return wins, 2, (
                f"{who.name} is blocking — delaying it leaves an obstruction")

        # 3. precedence depth
        da, db = a.precedence_depth(), b.precedence_depth()
        if da != db:
            wins = da > db
            return wins, 3, (
                f"{(a if wins else b).name} is holding up "
                f"{max(da, db)} other movement(s) vs {min(da, db)}")

        # 4. priority class
        order = {"expedite": 0, "normal": 1, "opportunistic": 2}
        pa, pb = order.get(a.priority_class, 1), order.get(b.priority_class, 1)
        if pa != pb:
            wins = pa < pb
            who = a if wins else b
            return wins, 4, f"{who.name} is priority '{who.priority_class}'"

        # 5. earliest due
        ea = a.planned_end or a.hard_deadline
        eb = b.planned_end or b.hard_deadline
        if ea and eb and ea != eb:
            wins = ea < eb
            who = a if wins else b
            return wins, 5, f"{who.name} is due earlier ({ea if wins else eb})"
        if bool(ea) != bool(eb):
            wins = bool(ea)
            return wins, 5, f"{(a if wins else b).name} has a stated due time"

        # 6. least slack
        sa, sb = a.slack_seconds(), b.slack_seconds()
        if sa != sb:
            wins = sa < sb
            return wins, 6, (
                f"{(a if wins else b).name} has less slack "
                f"({int(min(sa, sb))}s vs {int(max(sa, sb))}s)")

        # 7. claim sequence — CANNOT draw, sequence is unique
        wins = self.sequence < other.sequence
        who = self if wins else other
        return wins, 7, (
            f"{who.movement_id.name} claimed first "
            f"(sequence {who.sequence}) — all other tests tied")

    # ------------------------------------------------------------------
    # acquisition
    # ------------------------------------------------------------------
    def action_acquire(self):
        """Try to take the chokepoint. Resolves contention SYNCHRONOUSLY —
        a movement must know immediately whether it holds the elevator, so this
        is never deferred to a queue.
        """
        self.ensure_one()

        if self.state in ("occupied", "released"):
            raise UserError("Occupancy is never preempted or re-acquired.")

        # Serialise against other claims on the same chokepoint. This exact
        # pattern (row lock -> invalidate -> re-read) closed a real
        # double-approval race in a sibling codebase; without it two claims can
        # both read "free" and both proceed.
        self.env.cr.execute(
            "SELECT id FROM marshal_claim WHERE chokepoint_id = %s FOR UPDATE",
            (self.chokepoint_id.id,),
        )
        self.env.invalidate_all()

        if not self._downstream_has_space():
            self.write({"state": "proposed"})
            self.movement_id.variance_reason = "delay_buffer_full"
            self.env["marshal.dlq"].raise_entry(
                self.movement_id, "buffer_full",
                detail=(f"Downstream buffer of {self.chokepoint_id.code} is at "
                        f"capacity; entering would block it for everyone behind."),
                chokepoint=self.chokepoint_id,
                suggested="Wait for the buffer to drain, or re-route via "
                          "another chokepoint of the same type.")
            return False

        rivals = self.search([
            ("chokepoint_id", "=", self.chokepoint_id.id),
            ("state", "in", ("claimed", "held")),
            ("id", "!=", self.id),
        ])

        for rival in rivals:
            wins, rule, reason = self._beats(rival)
            self.env["marshal.contention"].create({
                "claim_a_id": self.id,
                "claim_b_id": rival.id,
                "winning_claim_id": self.id if wins else rival.id,
                "deciding_rule": rule,
                "reason": reason,
            })
            if not wins:
                self.write({"state": "yielded"})
                self.env["marshal.dlq"].raise_entry(
                    self.movement_id, "lost_contention",
                    detail=f"Yielded {self.chokepoint_id.code}: {reason}",
                    chokepoint=self.chokepoint_id,
                    suggested="Re-plan after the winning movement releases, or "
                              "escalate priority if this is genuinely urgent.")
                return False
            rival.write({"state": "yielded"})

        self.write({"state": "held" if self.chokepoint_id.has_room() else "claimed"})
        self._log("claimed")
        return True

    def _log(self, event_type, **extra):
        payload = {"chokepoint": self.chokepoint_id.code, "claim_seq": self.sequence}
        payload.update(extra)
        self.env["marshal.event"].record(self.movement_id, event_type, payload)

    def action_occupy(self):
        """Physically enter. Re-checks the blocking rule: the world may have
        changed since the claim was granted."""
        self.ensure_one()
        if not self._downstream_has_space():
            raise UserError(
                "Downstream buffer is full — entering would block this "
                "chokepoint for everyone behind you.")
        if not self.chokepoint_id.has_room():
            raise UserError("Chokepoint is at capacity.")
        self.write({"state": "occupied"})
        self._log("occupied")

    def action_release(self):
        """Occupancy ends ONLY here or by human action — never by a timer.
        A timer that frees a physical chokepoint while something is still in it
        causes a collision."""
        self.ensure_one()
        self.write({"state": "released"})
        self._log("released")
