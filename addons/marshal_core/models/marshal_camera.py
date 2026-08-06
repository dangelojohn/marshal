import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class MarshalCamera(models.Model):
    """A camera watching a chokepoint.

    D-006: the camera IS the interface. An ops person at 6am looks at the door,
    not at a Gantt chart — so the board is a wall of camera tiles annotated with
    what is scheduled there, rather than a schedule with video bolted on.

    SNAPSHOTS, NOT STREAMING — deliberately. A 2-5s refreshing still is an
    `<img>` tag: no player to break, trivial reconnect, low bandwidth across N
    tiles, and entirely sufficient to answer "is door 4 clear?". Live streaming
    earns its complexity only for supervising a movement in progress and for
    incident review, and should be a click-through from a tile rather than the
    default state of twelve of them.

    Reolink specifics (verified against a working client): the camera exposes
    `POST /cgi-bin/api.cgi`; Login returns a token carried as `?token=`, and
    `cmd=Snap&channel=N&rs=<nonce>&token=<tok>` returns a JPEG. Tokens last
    about an hour, so the URL must be refreshed rather than cached forever.
    """
    _name = "marshal.camera"
    _description = "Marshal Camera"
    _order = "chokepoint_id, name"

    name = fields.Char(required=True)
    chokepoint_id = fields.Many2one(
        "marshal.chokepoint", required=True, ondelete="cascade", index=True,
        help="What this camera watches. The board groups tiles by chokepoint.")

    host = fields.Char(required=True, help="LAN IP or hostname.")
    port = fields.Integer(default=80)
    scheme = fields.Selection([("http", "http"), ("https", "https")],
                              default="http", required=True)
    username = fields.Char(default="admin")
    password = fields.Char(
        help="Stored in the clear because the camera API needs it verbatim. "
             "These are LAN devices on a trusted segment; do not reuse a "
             "password that protects anything else.")
    channel = fields.Integer(default=0)

    vendor = fields.Selection([
        ("reolink", "Reolink"),
        ("generic", "Generic snapshot URL"),
    ], default="reolink", required=True)
    snapshot_url_override = fields.Char(
        help="For generic cameras, or to bypass token handling entirely. If "
             "set, the board uses this verbatim.")

    active = fields.Boolean(default=True)
    last_seen = fields.Datetime(readonly=True)
    last_error = fields.Char(readonly=True)

    _sql_constraints = [
        ("host_channel_uniq", "unique(host, channel)",
         "That camera and channel is already registered."),
    ]

    def snapshot_url(self):
        """Best-effort snapshot URL for the board.

        Returns False rather than raising: a dead camera must degrade to a tile
        with no image, never take the board down. The board is what the
        coordinator watches — it failing is worse than a blank tile.
        """
        self.ensure_one()
        if self.snapshot_url_override:
            return self.snapshot_url_override
        if self.vendor != "reolink":
            return False
        # Deliberately not fetching a token here: doing a login round-trip per
        # tile per refresh would hammer the cameras. The board asks for tokens
        # through `refresh_tokens()` on a slower cadence instead.
        tok = self.env["ir.config_parameter"].sudo().get_param(
            f"marshal.camera.token.{self.id}")
        if not tok:
            return False
        return (f"{self.scheme}://{self.host}:{self.port}/cgi-bin/api.cgi"
                f"?cmd=Snap&channel={self.channel}&rs=marshal&token={tok}")

    @api.model
    def refresh_tokens(self):
        """Log in to each camera and cache its token. Cron this ~every 30 min;
        Reolink tokens last about an hour."""
        import json as _json
        import urllib.request
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        ok = 0
        for cam in self.search([("vendor", "=", "reolink"), ("active", "=", True)]):
            url = f"{cam.scheme}://{cam.host}:{cam.port}/cgi-bin/api.cgi"
            body = _json.dumps([{
                "cmd": "Login", "action": 0,
                "param": {"User": {"userName": cam.username,
                                   "password": cam.password or "",
                                   "Version": "0"}},
            }]).encode()
            try:
                req = urllib.request.Request(
                    url, data=body,
                    headers={"Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req, timeout=8, context=ctx) as r:
                    data = _json.loads(r.read().decode())
                tok = (((data[0].get("value") or {}).get("Token") or {}).get("name"))
                if not tok:
                    raise ValueError("login returned no token")
                self.env["ir.config_parameter"].sudo().set_param(
                    f"marshal.camera.token.{cam.id}", tok)
                cam.sudo().write({"last_seen": fields.Datetime.now(),
                                  "last_error": False})
                ok += 1
            except Exception as exc:  # noqa: BLE001 — one bad camera must not stop the rest
                cam.sudo().write({"last_error": f"{type(exc).__name__}: {exc}"[:200]})
                _logger.warning("marshal.camera: %s login failed: %s", cam.name, exc)
        _logger.info("marshal.camera: refreshed %s/%s tokens",
                     ok, self.search_count([("active", "=", True)]))
        return ok
