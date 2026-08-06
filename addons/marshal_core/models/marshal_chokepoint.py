from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MarshalChokepoint(models.Model):
    """An exclusive-occupancy physical resource on the path from dock to booth:
    a dock bay, a freight elevator, an aisle segment, a staging lane.

    Chokepoints are the things that can only hold so much at once, and they are
    what movements contend for. Buffers (marshal.buffer) sit BETWEEN them.
    """
    _name = "marshal.chokepoint"
    _description = "Marshal Chokepoint"
    _order = "rank, id"

    name = fields.Char(required=True)
    code = fields.Char(required=True, help="Short stable identifier, e.g. DOCK4.")
    chokepoint_type = fields.Selection([
        ("dock_bay", "Dock Bay"),
        ("elevator", "Freight Elevator"),
        ("aisle", "Aisle Segment"),
        ("staging", "Staging Lane"),
        ("other", "Other"),
    ], required=True, default="dock_bay")

    capacity = fields.Integer(
        default=1, required=True,
        help="How many movements may occupy this at once. Almost always 1 — "
             "that is what makes it a chokepoint.")

    changeover_minutes = fields.Integer(
        default=0,
        help="Dead time between one movement releasing and the next entering. "
             "A truck must pull out before the next pulls in; ignoring this "
             "makes every plan optimistic by a constant.")

    rank = fields.Integer(
        required=True, default=100, index=True,
        help="DEADLOCK PREVENTION. Chokepoints are always claimed in ascending "
             "rank order, so a cycle (A holds the aisle waiting for the lift "
             "while B holds the lift waiting for the aisle) cannot form. "
             "Order rank along the physical flow: docks low, booths high.")

    is_foreign = fields.Boolean(
        string="Foreign (not ours)",
        help="True for a resource we do not control — a hotel freight elevator "
             "shared with housekeeping. Availability for these is ADVISORY: it "
             "may be occupied on arrival by someone who never told us. Treat "
             "that as a contention event to re-plan, not an error.")

    resource_id = fields.Many2one(
        "resource.resource", string="Calendar Resource", ondelete="set null",
        help="Optional link to a resource.resource so working hours and "
             "blackout windows come from resource.calendar. AVAILABILITY lives "
             "there; CONTENTION within available time lives here.")

    active = fields.Boolean(default=True)
    claim_ids = fields.One2many("marshal.claim", "chokepoint_id")

    _sql_constraints = [
        ("code_uniq", "unique(code)", "Chokepoint code must be unique."),
        ("capacity_positive", "CHECK(capacity > 0)", "Capacity must be at least 1."),
    ]

    @api.constrains("capacity")
    def _check_capacity(self):
        for rec in self:
            if rec.capacity < 1:
                raise ValidationError("Capacity must be at least 1.")

    def name_get(self):
        return [(r.id, f"[{r.code}] {r.name}") for r in self]

    def occupancy(self):
        """How many movements are physically in this chokepoint right now."""
        self.ensure_one()
        return self.env["marshal.claim"].search_count([
            ("chokepoint_id", "=", self.id),
            ("state", "=", "occupied"),
        ])

    def has_room(self):
        self.ensure_one()
        return self.occupancy() < self.capacity
