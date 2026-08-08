import base64
import hashlib
import hmac
import logging

import requests

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

# D-005 §4 — every outbound message stays under one SMS segment (~160 chars),
# always ends with an explicit single-word reply instruction when a reply is
# expected, and every reply gets an explicit confirmation. The copy lives
# here, not scattered across callers, so the templates stay auditable in one
# place the way the driver-SMS design doc always intended.
TEMPLATES = {
    "assignment": "Marshal: Dock {dock} at {time} for {crate}. Reply Y to confirm.",
    "confirmed": "Confirmed. See you at {time}.",
    "reminder_change": "Dock {dock} now {time} (was {old_time}). Reply Y to confirm.",
    "unrecognized": "Sorry, I didn't catch that. Reply Y to confirm your slot, "
                     "or call the dock office.",
}

YES_WORDS = {"y", "yes", "yeah", "yep", "ok", "okay", "confirm", "confirmed"}


class MarshalSmsLog(models.Model):
    """Every SMS in or out, and every one is confirmed in the log the same way
    it must be confirmed to the driver — D-005: silence after a reply is the
    "did it register?" failure this whole surface exists to avoid, so a
    message with no matching confirmation is a visible gap here too, not a
    silent one.

    Deliberately a real model, not a text log file: an insurer or a driver's
    dispute needs "what did we actually send, and when," and that has to
    survive the same way custody events do.
    """
    _name = "marshal.sms.log"
    _description = "Marshal SMS Log"
    _order = "id desc"

    movement_id = fields.Many2one("marshal.movement", required=True,
                                  ondelete="cascade", index=True)
    direction = fields.Selection([
        ("out", "Outbound"), ("in", "Inbound"),
    ], required=True, index=True)
    phone = fields.Char(required=True)
    body = fields.Char(required=True)
    template_key = fields.Char(
        help="Which message this was, e.g. 'assignment', 'confirmation', "
             "'reminder_change' — lets the pattern in D-005 be audited later "
             "even though the body text itself may vary run to run.")
    state = fields.Selection([
        ("queued", "Queued"),
        ("sent", "Sent"),
        ("delivered", "Delivered"),
        ("failed", "Failed"),
        ("simulated", "Simulated — no provider configured"),
    ], default="queued", required=True, index=True)
    provider_sid = fields.Char(string="Twilio SID")
    error = fields.Char()

    @api.model
    def log_inbound(self, movement, phone, body):
        return self.sudo().create({
            "movement_id": movement.id, "direction": "in", "phone": phone,
            "body": body, "state": "delivered",
        })

    # ------------------------------------------------------------------
    # sending
    # ------------------------------------------------------------------
    @api.model
    def send(self, movement, template_key, **ctx):
        """Compose and send (or simulate) a message to movement.driver_phone.

        HONEST BOUNDARY: without a configured Twilio account this NEVER
        pretends to send. It writes state='simulated' and logs at INFO what
        would have gone out — visible and testable, not a silent no-op that
        looks identical to success. Matches this project's own discipline
        (D-006's correction on motion-state honesty) rather than inventing a
        new standard for this one surface.
        """
        if not movement.driver_phone or not movement.sms_opt_in:
            return None

        body = TEMPLATES.get(template_key, TEMPLATES["unrecognized"]).format(**ctx)
        if len(body) > 160:
            _logger.warning("marshal.sms: %s template exceeds one SMS segment "
                             "(%d chars) for %s", template_key, len(body), movement.name)

        get_param = self.env["ir.config_parameter"].sudo().get_param
        enabled = get_param("marshal.sms_enabled") == "True"
        sid = get_param("marshal.twilio_account_sid")
        token = get_param("marshal.twilio_auth_token")
        from_number = get_param("marshal.twilio_from_number")

        if not (enabled and sid and token and from_number):
            _logger.info("marshal.sms [SIMULATED, no provider configured] "
                         "-> %s: %s", movement.driver_phone, body)
            return self.log_outbound(movement, movement.driver_phone, body,
                                     template_key, "simulated")

        try:
            resp = requests.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
                auth=(sid, token),
                data={"To": movement.driver_phone, "From": from_number, "Body": body},
                timeout=10,
            )
            resp.raise_for_status()
            provider_sid = resp.json().get("sid")
            return self.log_outbound(movement, movement.driver_phone, body,
                                     template_key, "sent", provider_sid=provider_sid)
        except requests.RequestException as exc:
            _logger.error("marshal.sms: Twilio send failed for %s: %s",
                          movement.name, exc)
            return self.log_outbound(movement, movement.driver_phone, body,
                                     template_key, "failed", error=str(exc)[:300])

    def log_outbound(self, movement, phone, body, template_key, state, provider_sid=None, error=None):
        return self.sudo().create({
            "movement_id": movement.id, "direction": "out", "phone": phone,
            "body": body, "template_key": template_key, "state": state,
            "provider_sid": provider_sid, "error": error,
        })

    # ------------------------------------------------------------------
    # receiving — D-009: keyword fallback when the LLM-parsing layer isn't
    # configured. NOTE: this ships keyword-only. Free-text LLM intent parsing
    # (the primary path in D-009) needs a model API key that isn't configured
    # on this box — an honest gap, not a silent one; unrecognized replies get
    # a clarifying text back rather than being misread as a no.
    # ------------------------------------------------------------------
    @api.model
    def parse_reply(self, body):
        """Return 'yes', 'no', or 'unrecognized'.

        Deliberately requires the WHOLE reply to be a single keyword, not
        just its first word — "yeah be there in 10" must not read as a bare
        yes. That specific phrase is the design doc's own worked example of
        the harder case only the (unbuilt) LLM path can safely resolve;
        matching on the first word alone would silently misparse it as a
        clean confirm instead of surfacing it as unrecognized.
        """
        token = (body or "").strip().lower().strip(".!?,")
        if token in YES_WORDS:
            return "yes"
        if token in {"n", "no", "cancel"}:
            return "no"
        return "unrecognized"

    @staticmethod
    def verify_twilio_signature(auth_token, url, post_params, signature):
        """Twilio's own HMAC-SHA1 scheme (documented, not Twilio-SDK-specific):
        sort POST params by key, concatenate key+value onto the full URL,
        HMAC-SHA1 with the auth token, base64-encode, compare to the header.

        Implemented directly rather than depending on the `twilio` pip
        package, which may not be installed in this container.
        """
        s = url
        for key in sorted(post_params.keys()):
            s += key + post_params[key]
        computed = base64.b64encode(
            hmac.new(auth_token.encode("utf-8"), s.encode("utf-8"),
                     hashlib.sha1).digest()
        ).decode("utf-8")
        return hmac.compare_digest(computed, signature or "")
