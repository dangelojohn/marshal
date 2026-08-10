import logging
import os
import uuid

from odoo import http, fields
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


def _read_static(name):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "static", "src", name)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


class MarshalReceiver(http.Controller):
    """The receiver's capture surface (D-012, surface 1) — the truck has just
    backed up to the dock and someone has to log its arrival.

    In this model that first physical touch IS the movement's first claim:
    acquiring and occupying the intake chokepoint. Everything downstream (the
    runner's watch, the wall board) is a client of the same claim state, so
    the receiver isn't a parallel "arrived" flag bolted on — it's the actual
    first hop of the chain other surfaces already trust.

    `auth="user"`, matching the wall board's reasoning: a shared dock device
    logs in once and stays signed in. Unlike the driver or exhibitor, a
    receiver is staff.
    """

    @http.route("/marshal/receiver/app", type="http", auth="user", website=False)
    def app(self, **kw):
        try:
            html = _read_static("receiver_capture.html")
        except OSError:
            return request.make_response(
                "<h1>Marshal receiver asset missing</h1>", [("Content-Type", "text/html")])
        return request.make_response(html, [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Cache-Control", "no-store"),
        ])

    @http.route("/marshal/receiver/pending", type="json", auth="user", methods=["POST"])
    def pending(self, **kw):
        """Movements planned but with no claim yet — nothing has physically
        started for them. That is exactly the set a receiver can act on."""
        Movement = request.env["marshal.movement"]
        # claim_count is a non-stored compute with no search() defined —
        # Odoo silently drops that domain leaf rather than erroring, so it
        # matched everything regardless of value. claim_ids, the real
        # relational field underneath it, is what's actually searchable.
        movements = Movement.search([
            ("state", "=", "planned"), ("claim_ids", "=", False),
        ], order="planned_start", limit=30)
        return {"movements": [{
            "id": m.id, "name": m.name, "crate_ref": m.crate_ref,
            "booth": m.dest_booth, "carrier": m.carrier,
            "due": m.planned_start.strftime("%H:%M") if m.planned_start else None,
        } for m in movements]}

    @http.route("/marshal/receiver/capture", type="json", auth="user", methods=["POST"])
    def capture(self, movement_id=None, chokepoint_code=None, photo=None,
               idempotency_key=None, **kw):
        Idem = request.env["marshal.idempotency"]
        scope = "marshal.receiver.capture"
        prior = Idem.replay(idempotency_key, scope, {"movement_id": movement_id})
        if prior:
            return {"ok": True, "replayed": True}

        movement = request.env["marshal.movement"].browse(int(movement_id))
        if not movement.exists():
            return {"ok": False, "error": "unknown_movement"}

        Chokepoint = request.env["marshal.chokepoint"]
        if chokepoint_code:
            cp = Chokepoint.search([("code", "=", chokepoint_code)], limit=1)
        else:
            # Default to the lowest-ranked (first) active dock bay — the
            # normal intake point when the capture screen doesn't specify one.
            cp = Chokepoint.search(
                [("chokepoint_type", "=", "dock_bay"), ("active", "=", True)],
                order="rank", limit=1)
        if not cp:
            return {"ok": False, "error": "no_intake_chokepoint"}

        emp = request.env["hr.employee"].sudo().search(
            [("user_id", "=", request.env.uid)], limit=1)
        if emp:
            movement.operator_id = emp.id

        claim = request.env["marshal.claim"].create({
            "movement_id": movement.id, "chokepoint_id": cp.id,
            "start": movement.actual_start or False,
        })
        acquired = claim.action_acquire()
        if not acquired:
            return {"ok": False, "error": "blocked",
                   "detail": "Could not acquire the intake chokepoint — "
                             "check the dead-letter queue for the reason."}

        try:
            claim.action_occupy()
        except UserError as exc:
            # Matches runner.py's "arrived" handling of the identical
            # failure mode. Without this, a claim that WINS action_acquire()
            # but then fails action_occupy() (e.g. capacity filled between
            # the two calls) sits in 'claimed' state with no DLQ entry —
            # invisible to the coordinator queue, and it keeps winning every
            # future contention tie-break by sequence, silently blocking the
            # chokepoint for everyone behind it. An end-to-end pass through
            # the real pipeline is what surfaced this gap.
            request.env["marshal.dlq"].raise_entry(
                movement, "chokepoint_busy", detail=str(exc)[:300],
                chokepoint=cp,
                suggested="This claim already won its contention but could "
                          "not occupy the chokepoint — release it so the "
                          "movement can be re-planned once there is room.")
            return {"ok": False, "error": "blocked", "detail": str(exc)}

        # This is the crate's first physical touch — the same "actuals"
        # runner.py's own "arrived" action records. Without it, a movement
        # whose first claim happens at the receiver (the normal case) would
        # never get an actual_start at all, and spec/03's predictive layer
        # runs on actuals, not plans.
        if not movement.actual_start:
            movement.actual_start = fields.Datetime.now()
        if movement.state == "planned":
            movement.state = "in_progress"

        if photo:
            request.env["ir.attachment"].sudo().create({
                "name": f"{movement.name}-capture-{uuid.uuid4().hex[:8]}.jpg",
                "res_model": "marshal.movement", "res_id": movement.id,
                "type": "binary", "datas": photo,
            })

        # No separate custody event here — claim.action_acquire()/action_occupy()
        # above already logged "claimed" and "occupied" on this movement's
        # chain. A third "received" entry would be a redundant, invented
        # event type duplicating what the claim already recorded truthfully.
        Idem.remember(idempotency_key, scope, claim, {"movement_id": movement_id})

        return {"ok": True, "replayed": False, "chokepoint": cp.code,
               "claim_id": claim.id}
