import logging
import os
from datetime import timezone

from dateutil import parser as dateutil_parser

from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)


def _read_static(name):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "static", "src", name)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _to_odoo_datetime(value):
    """A browser sends ISO 8601 ('...T...', maybe 'Z', maybe milliseconds);
    Odoo's Datetime fields need '%Y-%m-%d %H:%M:%S'. Parsed with dateutil
    (an Odoo core dependency, not an extra one) rather than a hand-rolled
    format list, since exactly which ISO variant a browser sends varies."""
    if not value:
        return None
    try:
        dt = dateutil_parser.isoparse(value)
    except (ValueError, TypeError):
        return None
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return fields.Datetime.to_string(dt)


class MarshalExhibitor(http.Controller):
    """The exhibitor-facing surface (D-012, surface 5).

    Deliberately `auth="public"`: an exhibitor declaring a shipment has not
    logged into anything and should not have to — the same reasoning D-005
    applies to the driver applies here, one notch less strict. Identity is
    the unguessable `declare_token`, not a session; see marshal.movement's
    own comment on why that has to be a token and not the record ID.
    """

    # ------------------------------------------------------------------
    # declare
    # ------------------------------------------------------------------
    @http.route("/marshal/exhibitor/declare", type="http", auth="public", website=False)
    def declare_page(self, **kw):
        try:
            html = _read_static("exhibitor_declare.html")
        except OSError:
            return request.make_response(
                "<h1>Marshal exhibitor asset missing</h1>", [("Content-Type", "text/html")])
        return request.make_response(html, [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Cache-Control", "no-store"),
        ])

    @http.route("/marshal/exhibitor/declare/submit", type="json", auth="public", methods=["POST"])
    def declare_submit(self, exhibitor_name=None, booth=None, carrier=None,
                       driver_phone=None, window_start=None, window_end=None,
                       idempotency_key=None, **kw):
        if not (exhibitor_name and booth):
            return {"ok": False, "error": "missing_required_field"}

        # A public form is exactly where a double-click or a network retry
        # is likeliest — no session, no client-side disable-on-submit
        # guarantee. Every other write in this system (runner, receiver)
        # already goes through marshal.idempotency; this endpoint originally
        # didn't, and a same-session evaluation pass proved it: two
        # identical submits produced two separate movements.
        Idem = request.env["marshal.idempotency"].sudo()
        prior = Idem.replay(idempotency_key, "marshal.exhibitor.declare", {
            "exhibitor_name": exhibitor_name, "booth": booth,
        })
        if prior:
            return {"ok": True, "replayed": True, "token": prior.declare_token,
                   "track_url": f"/marshal/exhibitor/track/{prior.declare_token}"}

        Movement = request.env["marshal.movement"].sudo()
        partner = request.env["res.partner"].sudo().search(
            [("name", "=", exhibitor_name)], limit=1)
        if not partner:
            partner = request.env["res.partner"].sudo().create({
                "name": exhibitor_name, "company_type": "company"})

        vals = {
            "dest_booth": booth,
            "partner_id": partner.id,
            "carrier": carrier or None,
            "driver_phone": driver_phone or None,
        }
        start = _to_odoo_datetime(window_start)
        end = _to_odoo_datetime(window_end)
        if start:
            vals["planned_start"] = start
        if end:
            vals["planned_end"] = end

        movement = Movement.create(vals)
        movement.action_plan()

        if movement.driver_phone and movement.planned_start:
            request.env["marshal.sms.log"].sudo().send(
                movement, "assignment", dock=movement.dest_booth or "TBD",
                time=movement.planned_start.strftime("%H:%M"),
                crate=movement.name)

        Idem.remember(idempotency_key, "marshal.exhibitor.declare", movement, {
            "exhibitor_name": exhibitor_name, "booth": booth,
        })

        return {"ok": True, "replayed": False, "token": movement.declare_token,
               "track_url": f"/marshal/exhibitor/track/{movement.declare_token}"}

    # ------------------------------------------------------------------
    # track
    # ------------------------------------------------------------------
    @http.route("/marshal/exhibitor/track/<string:token>", type="http", auth="public", website=False)
    def track_page(self, token, **kw):
        try:
            html = _read_static("exhibitor_track.html")
        except OSError:
            return request.make_response(
                "<h1>Marshal exhibitor asset missing</h1>", [("Content-Type", "text/html")])
        return request.make_response(html, [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Cache-Control", "no-store"),
        ])

    @http.route("/marshal/exhibitor/track/state", type="json", auth="public", methods=["POST"])
    def track_state(self, token=None, **kw):
        if not token:
            return {"ok": False, "error": "missing_token"}
        movement = request.env["marshal.movement"].sudo().search(
            [("declare_token", "=", token)], limit=1)
        if not movement:
            return {"ok": False, "error": "not_found"}

        # The customer-facing stepper (D-012): Declared -> In transit ->
        # Arrived -> Placed. Derived from movement/claim state, not a
        # parallel field, so it can never drift from what actually happened.
        latest_claim = movement._latest_claim()
        arrived = bool(movement.actual_start)
        placed = movement.state == "done"
        in_transit = movement.state in ("planned", "in_progress")

        steps = [
            {"key": "declared", "label": "Declared", "done": True,
             "at": self._fmt(movement.create_date)},
            {"key": "in_transit", "label": "In transit",
             "done": in_transit or arrived or placed,
             "at": self._fmt(movement.planned_start) if in_transit else None},
            {"key": "arrived", "label": "Arrived", "done": arrived or placed,
             "at": self._fmt(movement.actual_start)},
            {"key": "placed", "label": "Placed", "done": placed,
             "at": self._fmt(movement.actual_end)},
        ]
        return {
            "ok": True,
            "movement": movement.name,
            "booth": movement.dest_booth,
            "carrier": movement.carrier,
            "state": movement.state,
            "current_location": latest_claim.chokepoint_id.name if latest_claim else None,
            "steps": steps,
        }

    @staticmethod
    def _fmt(dt):
        return dt.strftime("%b %d, %H:%M") if dt else None
