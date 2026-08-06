import hashlib
import json
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MarshalEvent(models.Model):
    """Tamper-evident, append-only event log — one hash chain PER MOVEMENT.

    WHY PER-MOVEMENT AND NOT ONE GLOBAL CHAIN
    -----------------------------------------
    A single global chain is the obvious design and the wrong one here. It
    serialises every write in the system behind one tail pointer — on a dock
    where three runners tap at once, that is a contention bottleneck — and
    verifying one crate's history means walking every event ever recorded.

    Per-movement chains are independent, short, and verifiable in isolation:
    "prove this crate's history" touches only that crate. Cross-chain integrity
    comes from periodic ANCHORS (marshal.anchor) instead.

    This is Porterly v2's R04 as revised by its own feasibility review, which
    scored the global-chain version down for exactly these reasons.

    WHAT IT IS AND IS NOT
    ---------------------
    This detects TAMPERING — silent edits to history. It is not a blockchain and
    it does not stop a determined admin with database access from rewriting a
    chain wholesale; the anchor is what makes that expensive, because an anchor
    published before the rewrite will not match after it.
    """
    _name = "marshal.event"
    _description = "Marshal Custody Event"
    _order = "movement_id, seq"

    movement_id = fields.Many2one(
        "marshal.movement", required=True, ondelete="restrict", index=True,
        help="ondelete=restrict deliberately: evidence must not vanish when "
             "someone tidies up a movement.")
    seq = fields.Integer(required=True, index=True,
                         help="Position in THIS movement's chain, from 1.")

    event_type = fields.Selection([
        ("created", "Movement created"),
        ("claimed", "Chokepoint claimed"),
        ("occupied", "Entered chokepoint"),
        ("released", "Left chokepoint"),
        ("yielded", "Yielded to another movement"),
        ("blocked", "Blocked"),
        ("checkpoint", "Checkpoint recorded"),
        ("variance", "Variance recorded"),
        ("state", "State changed"),
    ], required=True, index=True)

    payload = fields.Text(help="JSON, canonicalised before hashing.")
    payload_digest = fields.Char(required=True, readonly=True)
    prev_hash = fields.Char(required=True, readonly=True)
    hash = fields.Char(required=True, readonly=True, index=True)

    user_id = fields.Many2one("res.users", required=True, readonly=True,
                              default=lambda s: s.env.user)
    recorded_at = fields.Datetime(required=True, readonly=True,
                                  default=fields.Datetime.now)

    _sql_constraints = [
        ("movement_seq_uniq", "unique(movement_id, seq)",
         "An event sequence must be unique within a movement's chain."),
    ]

    # ------------------------------------------------------------------
    # immutability
    # ------------------------------------------------------------------
    def write(self, vals):
        raise UserError(
            "Custody events are append-only. Rewriting history is precisely "
            "what this log exists to detect.")

    def unlink(self):
        raise UserError("Custody events cannot be deleted.")

    # ------------------------------------------------------------------
    # chaining
    # ------------------------------------------------------------------
    @api.model
    def _canonical(self, payload):
        """Stable JSON so the same facts always hash identically — key order
        must not change the digest."""
        return json.dumps(payload or {}, sort_keys=True, separators=(",", ":"),
                          default=str)

    @api.model
    def _compute_hash(self, prev_hash, digest, seq, recorded_at):
        material = f"{prev_hash}|{digest}|{seq}|{recorded_at}"
        return hashlib.sha256(material.encode()).hexdigest()

    @api.model
    def _genesis_hash(self, movement):
        """Each chain starts from something derived from the movement itself,
        so two movements can never share a prefix."""
        return hashlib.sha256(
            f"marshal.movement:{movement.id}:{movement.name}".encode()).hexdigest()

    @api.model
    def record(self, movement, event_type, payload=None):
        """Append one event. The only supported way to write to the log."""
        movement.ensure_one()
        last = self.search([("movement_id", "=", movement.id)],
                           order="seq desc", limit=1)
        seq = (last.seq + 1) if last else 1
        prev = last.hash if last else self._genesis_hash(movement)

        canonical = self._canonical(payload)
        digest = hashlib.sha256(canonical.encode()).hexdigest()
        now = fields.Datetime.now()
        h = self._compute_hash(prev, digest, seq, now)

        return self.sudo().create({
            "movement_id": movement.id,
            "seq": seq,
            "event_type": event_type,
            "payload": canonical,
            "payload_digest": digest,
            "prev_hash": prev,
            "hash": h,
            "recorded_at": now,
            "user_id": self.env.uid,
        })

    # ------------------------------------------------------------------
    # verification
    # ------------------------------------------------------------------
    @api.model
    def verify_chain(self, movement):
        """Recompute the chain. Returns (ok, first_bad_seq, detail).

        This is the method that gets pointed at in a dispute, so it reports
        WHERE the chain broke rather than just failing.
        """
        movement.ensure_one()
        events = self.search([("movement_id", "=", movement.id)], order="seq")
        expected_prev = self._genesis_hash(movement)
        for i, ev in enumerate(events, start=1):
            if ev.seq != i:
                return False, ev.seq, f"sequence gap: expected {i}, found {ev.seq}"
            if ev.prev_hash != expected_prev:
                return False, ev.seq, "prev_hash does not match the previous event"
            digest = hashlib.sha256((ev.payload or "").encode()).hexdigest()
            if digest != ev.payload_digest:
                return False, ev.seq, "payload was altered after recording"
            recomputed = self._compute_hash(
                ev.prev_hash, ev.payload_digest, ev.seq, ev.recorded_at)
            if recomputed != ev.hash:
                return False, ev.seq, "hash does not match its own contents"
            expected_prev = ev.hash
        return True, None, f"{len(events)} events verified"


class MarshalAnchor(models.Model):
    """Periodic cross-chain anchor.

    A per-movement chain proves nobody edited one event in the middle. It does
    NOT stop someone rebuilding an entire chain from scratch with plausible
    hashes. The anchor is what makes that expensive: it records a digest over
    every chain head at a point in time, so a chain rewritten afterwards will
    not reproduce an anchor taken before.

    Its value grows with where it is published. Kept only in this database it
    is weak evidence; copied off-box with the nightly backup — which is what
    happens now — it is considerably stronger.
    """
    _name = "marshal.anchor"
    _description = "Marshal Chain Anchor"
    _order = "id desc"

    taken_at = fields.Datetime(required=True, readonly=True,
                               default=fields.Datetime.now)
    chain_count = fields.Integer(readonly=True)
    event_count = fields.Integer(readonly=True)
    digest = fields.Char(required=True, readonly=True, index=True)
    detail = fields.Text(readonly=True)

    def write(self, vals):
        raise UserError("Anchors are immutable.")

    def unlink(self):
        raise UserError("Anchors are immutable.")

    @api.model
    def take(self):
        """Snapshot every chain head. Cheap enough to run hourly."""
        self.env.cr.execute("""
            SELECT movement_id, MAX(seq) FROM marshal_event GROUP BY movement_id
            ORDER BY movement_id
        """)
        heads = self.env.cr.fetchall()
        if not heads:
            return self.browse()

        Event = self.env["marshal.event"]
        parts, total = [], 0
        for movement_id, max_seq in heads:
            ev = Event.search([("movement_id", "=", movement_id),
                               ("seq", "=", max_seq)], limit=1)
            if ev:
                parts.append(f"{movement_id}:{ev.seq}:{ev.hash}")
                total += max_seq

        blob = "|".join(parts)
        digest = hashlib.sha256(blob.encode()).hexdigest()
        anchor = self.sudo().create({
            "chain_count": len(parts),
            "event_count": total,
            "digest": digest,
            "detail": blob if len(blob) < 60000 else blob[:60000] + "…(truncated)",
        })
        _logger.info("marshal.anchor: anchored %s chains / %s events -> %s",
                     len(parts), total, digest[:12])
        return anchor
