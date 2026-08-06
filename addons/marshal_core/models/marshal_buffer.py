from odoo import models, fields, api


class MarshalBuffer(models.Model):
    """A finite holding area BETWEEN chokepoints — a dock apron, an elevator
    lobby, the marshalling yard.

    Buffers are what make partial progress safe. A mover does not wait at the
    dock until the elevator is free; they advance to the lobby and queue. That
    only works if the lobby has room, which is the whole point of modelling
    buffers as first-class objects with a capacity.
    """
    _name = "marshal.buffer"
    _description = "Marshal Buffer"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    capacity = fields.Integer(
        required=True, default=1,
        help="How many movements can wait here. Measure this at the venue — "
             "the blocking rule is only as good as this number.")

    upstream_ids = fields.Many2many(
        "marshal.chokepoint", "marshal_buffer_upstream_rel",
        "buffer_id", "chokepoint_id", string="Fed by",
        help="Chokepoints that discharge INTO this buffer.")
    downstream_ids = fields.Many2many(
        "marshal.chokepoint", "marshal_buffer_downstream_rel",
        "buffer_id", "chokepoint_id", string="Feeds",
        help="Chokepoints this buffer discharges into.")

    occupancy = fields.Integer(compute="_compute_occupancy")
    has_space = fields.Boolean(compute="_compute_occupancy")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("code_uniq", "unique(code)", "Buffer code must be unique."),
        ("capacity_positive", "CHECK(capacity > 0)", "Capacity must be at least 1."),
    ]

    @api.depends("capacity", "upstream_ids")
    def _compute_occupancy(self):
        """A movement counts against this buffer when it has cleared one of the
        upstream chokepoints but not yet entered a downstream one — i.e. it is
        sitting in the holding area.

        Only a movement's LATEST claim is considered. Counting every released
        claim would double-count movements that passed through hops ago and
        have long since left.
        """
        Claim = self.env["marshal.claim"]
        for buf in self:
            n = 0
            if buf.upstream_ids:
                released = Claim.search([
                    ("chokepoint_id", "in", buf.upstream_ids.ids),
                    ("state", "=", "released"),
                    ("movement_id.state", "=", "in_progress"),
                ])
                for claim in released:
                    if claim.movement_id._latest_claim().id == claim.id:
                        n += 1
            buf.occupancy = n
            buf.has_space = n < buf.capacity

    def name_get(self):
        return [(r.id, f"[{r.code}] {r.name} ({r.occupancy}/{r.capacity})") for r in self]
