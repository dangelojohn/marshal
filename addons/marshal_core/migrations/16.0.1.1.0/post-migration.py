"""Remove the permissive record rule left over from 16.0.1.0.0.

WHY THIS EXISTS
---------------
1.0.0 shipped `rule_movement_company` with domain [(1,'=',1)] and
perm_write/perm_create granted to Marshal Operators — a placeholder that was
never a real control.

1.1.0 replaces it with a scoped pair (read-all / write-own-or-unassigned).
But Odoo ORs rules within a group, so leaving the old one active means the
scoped rule grants nothing: any operator can still write any movement.

And because the rule was declared under `noupdate="1"` and the new rules use
NEW xml ids, an upgrade neither updates nor removes it. It survives silently —
which is the worst kind of security regression, because the new rules LOOK
correct in the data file and in the UI.

Removing it here rather than deactivating it, so it cannot be re-enabled by
someone tidying up "inactive" records later.
"""
import logging

_logger = logging.getLogger(__name__)

STALE = [
    ("marshal_core", "rule_movement_company"),
]


def migrate(cr, version):
    if not version:
        return
    for module, name in STALE:
        cr.execute(
            "SELECT res_id FROM ir_model_data WHERE module=%s AND name=%s AND model='ir.rule'",
            (module, name),
        )
        row = cr.fetchone()
        if not row:
            _logger.info("marshal_core: stale rule %s.%s already absent", module, name)
            continue
        rule_id = row[0]
        cr.execute("DELETE FROM rule_group_rel WHERE rule_group_id=%s", (rule_id,))
        cr.execute("DELETE FROM ir_rule WHERE id=%s", (rule_id,))
        cr.execute(
            "DELETE FROM ir_model_data WHERE module=%s AND name=%s AND model='ir.rule'",
            (module, name),
        )
        _logger.warning(
            "marshal_core: REMOVED permissive rule %s.%s (id %s) — it would have "
            "OR'd with the new scoped rules and granted operators write on every "
            "movement.", module, name, rule_id)
