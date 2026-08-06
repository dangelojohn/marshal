import hashlib
import json
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class MarshalIdempotency(models.Model):
    """Server-side deduplication of client writes.

    Marshal's clients are a watch on a wrist, a phone in a gloved hand, and an
    SMS gateway — all of them on networks that drop. They will retry, and they
    should be able to retry *dumbly*, without tracking whether the first attempt
    landed.

    Without this, a double-tap on a runner's watch creates two movements, and a
    retried SMS books the same truck twice. With it, the second call returns the
    result of the first: same key, same outcome, no duplicate.

    The key is supplied by the CLIENT and must be deterministic for a given
    intent — e.g. sha256(device_id : movement_id : action : timestamp_ms).
    A client that generates a fresh key per retry gets no protection, which is
    why the recipe belongs in the client contract, not here.
    """
    _name = "marshal.idempotency"
    _description = "Marshal Idempotency Key"
    _order = "id desc"
    _rec_name = "key"

    key = fields.Char(required=True, index=True, readonly=True)
    scope = fields.Char(
        required=True, index=True, readonly=True,
        help="What the key is scoped to, usually the model name. Keys are "
             "unique per scope so an unrelated subsystem cannot collide.")
    res_model = fields.Char(readonly=True)
    res_id = fields.Integer(readonly=True)
    payload_digest = fields.Char(
        readonly=True,
        help="Digest of the request body. If the SAME key arrives with a "
             "DIFFERENT payload that is a client bug, not a retry — we log it "
             "loudly rather than silently returning the wrong record.")
    create_date = fields.Datetime(readonly=True)

    _sql_constraints = [
        ("key_scope_uniq", "unique(key, scope)",
         "Idempotency key already used in this scope."),
    ]

    # ------------------------------------------------------------------
    @api.model
    def _digest(self, payload):
        raw = json.dumps(payload, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()

    @api.model
    def replay(self, key, scope, payload=None):
        """Return the record a previous identical call produced, or None.

        None means "not seen — go ahead and do the work".
        """
        if not key:
            return None
        rec = self.search([("key", "=", key), ("scope", "=", scope)], limit=1)
        if not rec:
            return None
        if payload is not None:
            digest = self._digest(payload)
            if rec.payload_digest and rec.payload_digest != digest:
                # Same key, different body. Returning the old record would be
                # wrong; creating a new one would break the guarantee. Surface it.
                _logger.error(
                    "marshal.idempotency: key %s reused in scope %s with a "
                    "DIFFERENT payload — client bug. Returning the original.",
                    key, scope)
        if rec.res_model and rec.res_id:
            target = self.env[rec.res_model].browse(rec.res_id)
            return target if target.exists() else None
        return None

    @api.model
    def remember(self, key, scope, record, payload=None):
        """Record that `key` produced `record`. Safe to call without a key."""
        if not key or not record:
            return False
        self.sudo().create({
            "key": key,
            "scope": scope,
            "res_model": record._name,
            "res_id": record.id,
            "payload_digest": self._digest(payload) if payload is not None else False,
        })
        return True

    @api.model
    def _gc(self, days=2):
        """Keys only need to outlive a client's retry window. Two days is
        generous for a device that reconnects after a shift."""
        cutoff = fields.Datetime.subtract(fields.Datetime.now(), days=days)
        stale = self.search([("create_date", "<", cutoff)])
        n = len(stale)
        stale.unlink()
        if n:
            _logger.info("marshal.idempotency: purged %s expired keys", n)
        return n


class MarshalIdempotentMixin(models.AbstractModel):
    """Mix into any model that accepts writes from an unreliable client."""
    _name = "marshal.idempotent.mixin"
    _description = "Marshal Idempotent Write Mixin"

    @api.model
    def create_idempotent(self, vals, idempotency_key=None):
        """Create once, however many times you are called.

        Returns (record, created) so a caller can tell a fresh action from a
        replayed one — useful for deciding whether to send an SMS again.
        """
        Idem = self.env["marshal.idempotency"]
        existing = Idem.replay(idempotency_key, self._name, vals)
        if existing:
            return existing, False
        record = self.create(vals)
        Idem.remember(idempotency_key, self._name, record, vals)
        return record, True
