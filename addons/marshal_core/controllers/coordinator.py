import logging
import os

from odoo import http, fields
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


def _read_static(name):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "static", "src", name)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _require_manager():
    """R13 fail-closed: resolving a DLQ entry or overriding an assignment is
    a manager-level action (14_surface_map.md: "Manager / dock coordinator"),
    not something any operator should be able to do from the queue view.
    Every mutating route below checks this before touching anything."""
    if not request.env.user.has_group("marshal_core.group_marshal_manager"):
        return False
    return True


class MarshalCoordinator(http.Controller):
    """The coordinator's desk tool (D-012 surface 4) — the queue, overrides,
    and the DLQ, always visible per this project's own signature element
    (14_surface_map.md / 04_manager_coordinator/STITCH_PROMPT.md): a
    blockage is something to act on, not something buried in a logs tab.

    NOTE ON SCOPE: this ships single-person resolution/override, logged with
    who and when. The design brief's "maker-checker (R07)" — a SECOND person
    confirming before a consequential change takes effect — is not built;
    that needs a real two-person workflow (propose, then a DIFFERENT user
    approves) this pass didn't have a second role to build against. Treat
    action_resolve/action_dismiss/override here as the single-approver
    version, not the full R07 spec.
    """

    @http.route("/marshal/coordinator/app", type="http", auth="user", website=False)
    def app(self, **kw):
        try:
            html = _read_static("coordinator_app.html")
        except OSError:
            return request.make_response(
                "<h1>Marshal coordinator asset missing</h1>", [("Content-Type", "text/html")])
        return request.make_response(html, [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Cache-Control", "no-store"),
        ])

    @http.route("/marshal/coordinator/queue", type="json", auth="user", methods=["POST"])
    def queue(self, **kw):
        Dlq = request.env["marshal.dlq"]
        Claim = request.env["marshal.claim"]

        dlq_entries = Dlq.search([("state", "=", "open")], order="id desc", limit=50)
        # A claim a human needs to look at: lost a contention (yielded) or
        # could not enter (proposed, having already failed acquire once —
        # a fresh proposed claim that simply hasn't been tried yet is normal,
        # so this only flags ones on a movement the DLQ has ALSO flagged).
        stuck_movement_ids = dlq_entries.mapped("movement_id").ids
        stuck_claims = Claim.search([
            ("movement_id", "in", stuck_movement_ids),
            ("state", "in", ("proposed", "yielded")),
        ]) if stuck_movement_ids else Claim.browse()

        return {
            "is_manager": _require_manager(),
            "dlq": [{
                "id": d.id, "movement": d.movement_id.name,
                "movement_id": d.movement_id.id,
                "reason": d.reason_code, "detail": d.detail,
                "suggested": d.suggested_actions,
                "chokepoint": d.chokepoint_id.code if d.chokepoint_id else None,
            } for d in dlq_entries],
            "stuck_claims": [{
                "id": c.id, "movement": c.movement_id.name,
                "chokepoint": c.chokepoint_id.code, "state": c.state,
                "operator": c.movement_id.operator_id.name or None,
            } for c in stuck_claims],
        }

    @http.route("/marshal/coordinator/dlq/resolve", type="json", auth="user", methods=["POST"])
    def resolve(self, dlq_id=None, note=None, **kw):
        if not _require_manager():
            return {"ok": False, "error": "not_authorized"}
        entry = request.env["marshal.dlq"].browse(int(dlq_id))
        if not entry.exists():
            return {"ok": False, "error": "unknown_entry"}
        entry.action_resolve(note=note)
        return {"ok": True}

    @http.route("/marshal/coordinator/dlq/dismiss", type="json", auth="user", methods=["POST"])
    def dismiss(self, dlq_id=None, **kw):
        if not _require_manager():
            return {"ok": False, "error": "not_authorized"}
        entry = request.env["marshal.dlq"].browse(int(dlq_id))
        if not entry.exists():
            return {"ok": False, "error": "unknown_entry"}
        entry.action_dismiss()
        return {"ok": True}

    @http.route("/marshal/coordinator/override/release_claim", type="json", auth="user", methods=["POST"])
    def release_claim(self, claim_id=None, **kw):
        """Force-release a stuck claim so the movement can be re-planned.
        Deliberately NOT force-occupy or force-acquire — this only ever
        gives up a hold, never grants one, so it cannot be used to jump a
        queue, only to unstick one."""
        if not _require_manager():
            return {"ok": False, "error": "not_authorized"}
        claim = request.env["marshal.claim"].browse(int(claim_id))
        if not claim.exists():
            return {"ok": False, "error": "unknown_claim"}
        if claim.state not in ("proposed", "claimed", "held", "yielded"):
            return {"ok": False, "error": "cannot_release",
                   "detail": f"Claim is {claim.state} — only a not-yet-occupied "
                             "claim can be released this way."}
        claim.write({"state": "released"})
        return {"ok": True}

    @http.route("/marshal/coordinator/override/reassign", type="json", auth="user", methods=["POST"])
    def reassign(self, movement_id=None, operator_id=None, **kw):
        if not _require_manager():
            return {"ok": False, "error": "not_authorized"}
        movement = request.env["marshal.movement"].browse(int(movement_id))
        if not movement.exists():
            return {"ok": False, "error": "unknown_movement"}
        movement.operator_id = int(operator_id) if operator_id else False
        return {"ok": True}
