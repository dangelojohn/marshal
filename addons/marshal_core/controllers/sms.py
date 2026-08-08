import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class MarshalSms(http.Controller):
    """Twilio's inbound-SMS webhook.

    Public and unauthenticated by necessity — Twilio cannot hold an Odoo
    session — which is exactly why the signature check below is not
    optional. R13 (fail-closed access) applies here as much as it does to
    any ORM record rule: an endpoint that can flip a movement's confirmed
    state must refuse, not guess, when it cannot prove the request is real.
    """

    @http.route("/marshal/sms/inbound", type="http", auth="public",
               methods=["POST"], csrf=False)
    def inbound(self, **post):
        env = request.env  # public user; elevated calls below use .sudo() explicitly
        get_param = env["ir.config_parameter"].sudo().get_param
        auth_token = get_param("marshal.twilio_auth_token")

        if not auth_token:
            # Fail closed: no signing secret configured means this endpoint
            # cannot tell a real Twilio callback from anyone else's POST.
            # Refusing is the honest behaviour — silently trusting it would
            # let anyone confirm or cancel a movement by guessing a phone
            # number.
            _logger.warning("marshal.sms: inbound webhook hit with no "
                            "marshal.twilio_auth_token configured — refusing")
            return request.make_response("", status=403)

        signature = request.httprequest.headers.get("X-Twilio-Signature", "")
        url = request.httprequest.url
        SmsLog = env["marshal.sms.log"].sudo()
        if not SmsLog.verify_twilio_signature(auth_token, url, dict(post), signature):
            _logger.warning("marshal.sms: inbound webhook signature mismatch")
            return request.make_response("", status=403)

        from_number = post.get("From")
        body = post.get("Body", "")
        if not from_number:
            return request.make_response("", status=400)

        Movement = env["marshal.movement"].sudo()
        movement = Movement.search([
            ("driver_phone", "=", from_number),
            ("state", "not in", ("done", "cancelled")),
        ], order="id desc", limit=1)

        empty_twiml = '<?xml version="1.0" encoding="UTF-8"?><Response></Response>'
        if not movement:
            _logger.info("marshal.sms: inbound from unrecognised number %s: %r",
                         from_number, body)
            return request.make_response(
                empty_twiml, [("Content-Type", "text/xml")])

        SmsLog.log_inbound(movement, from_number, body)
        intent = SmsLog.parse_reply(body)

        if intent == "yes":
            when = (movement.planned_start.strftime("%H:%M")
                    if movement.planned_start else "the scheduled time")
            SmsLog.send(movement, "confirmed", time=when)
        elif intent == "no":
            movement.write({"state": "cancelled"})
        else:
            SmsLog.send(movement, "unrecognized")

        return request.make_response(empty_twiml, [("Content-Type", "text/xml")])
