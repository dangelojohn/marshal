import logging
from datetime import datetime

from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)


class MarshalBoard(http.Controller):
    """The wall board's data endpoint.

    D-008 makes the scheduler the product and every screen a client of it. This
    controller is the seam: it composes chokepoint state, the movement in
    progress, buffer pressure and a camera snapshot URL into one JSON document
    the board can render without knowing anything about Odoo.

    Because it IS the seam, it is also the natural place for a second surface
    later — a driver display in the yard, a phone view for a supervisor — with
    no core change. That is the headless claim being cashed rather than asserted.
    """

    # `auth="user"` deliberately: the board hangs on a wall and logs in once.
    # Public access would expose the floor plan, crate references and operator
    # names to anyone on the venue's guest wifi.
    @http.route("/marshal/board", type="http", auth="user", website=False)
    def board(self, **kw):
        """Serve the board as a single self-contained document.

        Deliberately NOT through Odoo's asset pipeline: the board is a client
        of /marshal/board/state and nothing more, so it must be servable from
        anywhere — a kiosk, a spare tablet, a different host entirely. Coupling
        it to Odoo's bundler would quietly make that untrue.
        """
        import os
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "static", "src", "board.html")
        try:
            with open(path, "r", encoding="utf-8") as fh:
                html = fh.read()
        except OSError:
            return request.make_response(
                "<h1>Marshal board asset missing</h1>", [("Content-Type", "text/html")])
        return request.make_response(html, [
            ("Content-Type", "text/html; charset=utf-8"),
            # A wall board must never serve a stale cached copy after a deploy.
            ("Cache-Control", "no-store"),
        ])

    @http.route("/marshal/board/state", type="json", auth="user", methods=["POST"])
    def board_state(self, **kw):
        env = request.env
        Chokepoint = env["marshal.chokepoint"]
        Claim = env["marshal.claim"]
        Buffer = env["marshal.buffer"]

        # Only the chokepoints worth watching on a wall. Aisle segments are
        # real resources but there are too many to tile usefully.
        watchable = Chokepoint.search([
            ("active", "=", True),
            ("chokepoint_type", "in", ("dock_bay", "elevator", "staging")),
        ], order="rank")

        tiles = []
        for cp in watchable:
            occupied = Claim.search([
                ("chokepoint_id", "=", cp.id),
                ("state", "=", "occupied"),
            ], limit=1)
            nxt = Claim.search([
                ("chokepoint_id", "=", cp.id),
                ("state", "in", ("held", "claimed")),
            ], order="sequence", limit=1)

            downstream = Buffer.search([("upstream_ids", "in", cp.id)], limit=1)
            buf = None
            if downstream:
                buf = {
                    "code": downstream.code,
                    "occupancy": downstream.occupancy,
                    "capacity": downstream.capacity,
                    "has_space": downstream.has_space,
                }

            movement = None
            late = 0
            if occupied:
                mv = occupied.movement_id
                if occupied.expected_end:
                    late = max(0, int((fields.Datetime.now() - occupied.expected_end)
                                      .total_seconds() // 60))
                movement = {
                    "name": mv.name,
                    "crate_ref": mv.crate_ref,
                    "dest_booth": mv.dest_booth,
                    "operator": mv.operator_id.name or None,
                    "equipment": mv.equipment_id.name or None,
                    "due": occupied.expected_end.strftime("%H:%M") if occupied.expected_end else None,
                    "late_minutes": late,
                }

            camera = env["marshal.camera"].search(
                [("chokepoint_id", "=", cp.id), ("active", "=", True)], limit=1)
            snapshot = camera.snapshot_url() if camera else False

            # Exception is deliberately narrow. If everything is an exception,
            # nothing is — and the board gets ignored within a week.
            status = "clear"
            if occupied:
                status = "active"
            if late > 0 or (buf and not buf["has_space"]) or (camera and not snapshot):
                status = "exception"

            tiles.append({
                "code": cp.code,
                "name": cp.name,
                "type": cp.chokepoint_type,
                "status": status,
                "snapshot_url": snapshot or None,
                "movement": movement,
                "next": ({"name": nxt.movement_id.name,
                          "eta": nxt.start.strftime("%H:%M") if nxt.start else None}
                         if nxt else None),
                "buffer": buf,
            })

        broken = 0
        Event = env["marshal.event"]
        for mv in env["marshal.movement"].search([("state", "=", "in_progress")], limit=50):
            if not Event.verify_chain(mv)[0]:
                broken += 1

        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "alerts": {
                "dlq_open": env["marshal.dlq"].open_count(),
                "chains_broken": broken,
            },
            "tiles": tiles,
        }
