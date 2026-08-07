import logging

from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)


class MarshalRunner(http.Controller):
    """The runner's API — what an Apple Watch Ultra talks to.

    THE DESIGN BUDGET IS TWO TAPS PER MOVEMENT. Everything here exists to keep
    it there: one call to learn the current job, one to say ARRIVED, one to say
    DELIVERED. No lists, no forms, no free text, no photographs — those belong
    on the handheld and the wall board.

    WHY THIS MATTERS MORE THAN IT LOOKS
    A tap at arrived and a tap at delivered give an EXACT start and end for that
    movement, from the person who was there. That is the highest-fidelity
    actuals source in the system — better than camera motion, which can only say
    "something happened near door 4" — and `spec/03` established that without
    actuals the whole predictive layer is dead. It is also cheap enough that it
    might actually get done, which is the part that usually fails.

    EVERY WRITE IS IDEMPOTENT. The client is a watch on a wrist, on a network
    that drops, worn by someone with gloves on. It must be able to retry dumbly
    without tracking whether the first attempt landed. The client supplies a key
    derived from (device, movement, action); the server returns the result of
    the first call for that key.
    """

    # ------------------------------------------------------------------
    def _operator(self):
        """The hr.employee behind the calling user, if any."""
        return request.env["hr.employee"].sudo().search(
            [("user_id", "=", request.env.uid)], limit=1)

    def _job_payload(self, claim):
        """Exactly the four things a wrist can usefully show. Nothing else."""
        if not claim:
            return None
        mv = claim.movement_id
        return {
            "movement": mv.name,
            "movement_id": mv.id,
            "claim_id": claim.id,
            "booth": mv.dest_booth,        # the big text
            "crate": mv.crate_ref,
            "equipment": mv.equipment_id.name or None,
            "chokepoint": claim.chokepoint_id.code,
            "due": claim.expected_end.strftime("%H:%M") if claim.expected_end else None,
            "state": claim.state,
        }

    # ------------------------------------------------------------------
    @http.route("/marshal/runner/next", type="json", auth="user", methods=["POST"])
    def next_job(self, **kw):
        """The ONE job this runner should be doing. Never a list.

        A list would invite scrolling on a 49mm screen with a gloved hand, and
        would put the decision of what to do next back on the person we are
        trying to help.
        """
        emp = self._operator()
        Claim = request.env["marshal.claim"]

        domain_base = [("state", "in", ("held", "occupied"))]
        claim = Claim.search(
            domain_base + [("movement_id.operator_id", "=", emp.id)],
            order="sequence", limit=1) if emp else Claim.browse()
        if not claim:
            # Unassigned work is fair game — a runner who has finished should be
            # able to pick up the next thing without a dispatcher in the loop.
            claim = Claim.search(
                domain_base + [("movement_id.operator_id", "=", False)],
                order="sequence", limit=1)

        nxt = None
        if claim:
            following = Claim.search([
                ("state", "in", ("held", "claimed")),
                ("id", "!=", claim.id),
                "|", ("movement_id.operator_id", "=", emp.id if emp else False),
                     ("movement_id.operator_id", "=", False),
            ], order="sequence", limit=1)
            if following:
                # ONE next-up line so the runner can pre-position. Deliberately
                # not two — that is a list, and a list is a different product.
                nxt = {"booth": following.movement_id.dest_booth,
                       "at": following.start.strftime("%H:%M") if following.start else None}

        return {
            "operator": emp.name if emp else None,
            "job": self._job_payload(claim),
            "next": nxt,
            "server_time": fields.Datetime.now().strftime("%H:%M:%S"),
        }

    # ------------------------------------------------------------------
    def _transition(self, claim_id, action, idempotency_key):
        Claim = request.env["marshal.claim"]
        Idem = request.env["marshal.idempotency"]
        scope = f"marshal.runner.{action}"

        prior = Idem.replay(idempotency_key, scope, {"claim_id": claim_id})
        if prior:
            # A retry, not a second event. Report the ORIGINAL timestamp — the
            # runner must see the time that was actually recorded, not now.
            return {"ok": True, "replayed": True,
                    "recorded_at": prior.recorded_at.strftime("%H:%M:%S")
                    if hasattr(prior, "recorded_at") and prior.recorded_at else None}

        claim = Claim.browse(int(claim_id))
        if not claim.exists():
            return {"ok": False, "error": "unknown_claim"}

        mv = claim.movement_id
        now = fields.Datetime.now()

        if action == "arrived":
            try:
                claim.action_occupy()
            except Exception as exc:  # noqa: BLE001 — the wrist gets a reason, not a traceback
                request.env["marshal.dlq"].raise_entry(
                    mv, "chokepoint_busy", detail=str(exc)[:300],
                    chokepoint=claim.chokepoint_id,
                    suggested="Hold at the buffer until the chokepoint clears.")
                return {"ok": False, "error": "blocked", "detail": str(exc)[:160]}
            if not mv.actual_start:
                mv.actual_start = now
            if mv.state == "planned":
                mv.state = "in_progress"

        elif action == "delivered":
            claim.action_release()
            mv.actual_end = now
            # Last hop of the chain finishes the movement.
            remaining = claim.search_count([
                ("movement_id", "=", mv.id),
                ("state", "in", ("proposed", "claimed", "held", "occupied")),
            ])
            if not remaining:
                mv.state = "done"

        elif action == "blocked":
            request.env["marshal.dlq"].raise_entry(
                mv, "other", detail="Reported blocked by the runner.",
                chokepoint=claim.chokepoint_id,
                suggested="Coordinator to assess: obstruction, equipment fault "
                          "or access refused.")
            mv.variance_reason = "other"

        event = request.env["marshal.event"].record(mv, action if action != "blocked" else "blocked", {
            "chokepoint": claim.chokepoint_id.code,
            "claim_seq": claim.sequence,
            "by": request.env.user.name,
        })
        Idem.remember(idempotency_key, scope, event, {"claim_id": claim_id})

        return {"ok": True, "replayed": False,
                "recorded_at": now.strftime("%H:%M:%S"),
                "movement": mv.name, "state": mv.state}

    @http.route("/marshal/runner/arrived", type="json", auth="user", methods=["POST"])
    def arrived(self, claim_id=None, idempotency_key=None, **kw):
        return self._transition(claim_id, "arrived", idempotency_key)

    @http.route("/marshal/runner/delivered", type="json", auth="user", methods=["POST"])
    def delivered(self, claim_id=None, idempotency_key=None, **kw):
        return self._transition(claim_id, "delivered", idempotency_key)

    @http.route("/marshal/runner/blocked", type="json", auth="user", methods=["POST"])
    def blocked(self, claim_id=None, idempotency_key=None, **kw):
        return self._transition(claim_id, "blocked", idempotency_key)
