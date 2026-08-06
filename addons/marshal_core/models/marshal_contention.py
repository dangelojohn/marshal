from odoo import models, fields, api
from odoo.exceptions import UserError


class MarshalContention(models.Model):
    """An immutable record of one contention decision.

    Every comparison writes one of these. It is what makes the scheduler
    explainable rather than oracular — you can always answer "why did 517 get
    the elevator instead of 482?" with the rule number and a sentence.

    It is also, unexpectedly, the commercial artifact: the same log that
    defends a safety decision is what auto-waives a late-arrival fee when the
    venue's own congestion caused the delay.
    """
    _name = "marshal.contention"
    _description = "Marshal Contention Log"
    _order = "id desc"

    claim_a_id = fields.Many2one("marshal.claim", required=True, ondelete="cascade")
    claim_b_id = fields.Many2one("marshal.claim", required=True, ondelete="cascade")
    winning_claim_id = fields.Many2one("marshal.claim", required=True, ondelete="cascade")
    chokepoint_id = fields.Many2one(related="claim_a_id.chokepoint_id", store=True)
    deciding_rule = fields.Integer(
        required=True,
        help="Which comparator test (1-7) actually discriminated.")
    reason = fields.Text(required=True, help="Human-readable, for the coordinator.")

    _sql_constraints = [
        ("rule_range", "CHECK(deciding_rule BETWEEN 1 AND 7)",
         "Deciding rule must be one of the seven comparator tests."),
    ]

    def write(self, vals):
        raise UserError("The contention log is immutable — it is evidence.")

    def unlink(self):
        raise UserError("The contention log is immutable — it is evidence.")
