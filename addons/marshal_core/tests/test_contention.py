from odoo.tests.common import TransactionCase, tagged
from odoo import fields
from datetime import timedelta


@tagged("post_install", "-at_install", "marshal")
class TestContention(TransactionCase):
    """Tests for the two mechanics that must be exactly right: the blocking
    rule, and the comparator (including its guarantee of determinism)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        CP = cls.env["marshal.chokepoint"]
        # Codes are namespaced `ZZT-*` deliberately. `code` is UNIQUE, and these
        # tests run against a database that already holds a seeded venue
        # topology — an earlier version used "APRON" and passed on an empty DB,
        # then failed the moment real data existed. Fixtures must never assume
        # they are alone in the database.
        cls.dock = CP.create({"name": "T Dock", "code": "ZZT-DOCK",
                              "chokepoint_type": "dock_bay", "rank": 9010})
        cls.aisle = CP.create({"name": "T Aisle", "code": "ZZT-AISLE",
                               "chokepoint_type": "aisle", "rank": 9020})
        cls.lift = CP.create({"name": "T Lift", "code": "ZZT-LIFT",
                              "chokepoint_type": "elevator", "rank": 9030})
        # capacity 1 so the blocking rule trips on the second movement
        cls.apron = cls.env["marshal.buffer"].create({
            "name": "T Apron", "code": "ZZT-APRON", "capacity": 1,
            "upstream_ids": [(6, 0, [cls.dock.id])],
            "downstream_ids": [(6, 0, [cls.aisle.id])],
        })

    def _movement(self, **kw):
        vals = {"crate_ref": "C1", "dest_booth": "412", "state": "in_progress"}
        vals.update(kw)
        return self.env["marshal.movement"].create(vals)

    def _claim(self, movement, chokepoint, **kw):
        vals = {"movement_id": movement.id, "chokepoint_id": chokepoint.id}
        vals.update(kw)
        return self.env["marshal.claim"].create(vals)

    # ---------------- the blocking rule ----------------

    def test_blocking_rule_allows_when_buffer_has_space(self):
        c = self._claim(self._movement(), self.dock)
        self.assertTrue(c._downstream_has_space(),
                        "empty apron should admit a movement")

    def test_blocking_rule_refuses_when_buffer_full(self):
        """Never occupy what you cannot clear."""
        # fill the apron: one movement has cleared the dock and is waiting
        m1 = self._movement()
        self._claim(m1, self.dock, state="released")
        self.assertEqual(self.apron.occupancy, 1)
        self.assertFalse(self.apron.has_space)

        m2 = self._movement()
        c2 = self._claim(m2, self.dock)
        self.assertFalse(c2._downstream_has_space(),
                         "full apron must block entry to the dock")
        self.assertFalse(c2.action_acquire(), "acquire must fail when blocked")
        self.assertEqual(m2.variance_reason, "delay_buffer_full")

    def test_no_downstream_buffer_never_blocks(self):
        """The last hop into the booth has nothing downstream to fill."""
        c = self._claim(self._movement(), self.lift)
        self.assertTrue(c._downstream_has_space())

    # ---------------- the comparator, rule by rule ----------------

    def test_rule1_hard_deadline_beats_none(self):
        soon = fields.Datetime.now() + timedelta(hours=1)
        a = self._claim(self._movement(hard_deadline=soon), self.lift)
        b = self._claim(self._movement(), self.lift)
        wins, rule, _ = a._beats(b)
        self.assertTrue(wins)
        self.assertEqual(rule, 1)

    def test_rule2_blocking_beats_normal(self):
        a = self._claim(self._movement(is_blocking=True), self.lift)
        b = self._claim(self._movement(), self.lift)
        wins, rule, _ = a._beats(b)
        self.assertTrue(wins)
        self.assertEqual(rule, 2)

    def test_rule4_expedite_beats_normal(self):
        a = self._claim(self._movement(priority_class="expedite"), self.lift)
        b = self._claim(self._movement(priority_class="normal"), self.lift)
        wins, rule, _ = a._beats(b)
        self.assertTrue(wins)
        self.assertEqual(rule, 4)

    def test_rule5_earliest_due(self):
        now = fields.Datetime.now()
        a = self._claim(self._movement(planned_end=now + timedelta(hours=1)), self.lift)
        b = self._claim(self._movement(planned_end=now + timedelta(hours=5)), self.lift)
        wins, rule, _ = a._beats(b)
        self.assertTrue(wins)
        self.assertEqual(rule, 5)

    # ---------------- rule 7: the determinism guarantee ----------------

    def test_rule7_breaks_otherwise_identical_claims(self):
        """Two claims identical on every other axis must still produce a
        decision — otherwise the scheduler is not reproducible."""
        a = self._claim(self._movement(), self.lift)
        b = self._claim(self._movement(), self.lift)
        wins, rule, reason = a._beats(b)
        self.assertEqual(rule, 7, "must fall through to the sequence tie-break")
        self.assertTrue(wins, "the earlier sequence should win")
        self.assertIn("claimed first", reason)

    def test_rule7_is_antisymmetric_and_total(self):
        """a beats b  <=>  not (b beats a). No draw is possible."""
        a = self._claim(self._movement(), self.lift)
        b = self._claim(self._movement(), self.lift)
        self.assertNotEqual(a._beats(b)[0], b._beats(a)[0])

    def test_sequence_is_unique_and_monotonic(self):
        seqs = [self._claim(self._movement(), self.lift).sequence for _ in range(5)]
        self.assertEqual(len(set(seqs)), 5, "sequences must be unique")
        self.assertEqual(seqs, sorted(seqs), "sequences must be monotonic")

    # ---------------- contention is logged ----------------

    def test_contention_is_recorded_with_the_deciding_rule(self):
        a = self._claim(self._movement(priority_class="expedite"), self.lift)
        b = self._claim(self._movement(priority_class="normal"), self.lift,
                        state="claimed")
        a.action_acquire()
        log = self.env["marshal.contention"].search([("claim_a_id", "=", a.id)])
        self.assertTrue(log, "every comparison must be logged")
        self.assertEqual(log[0].deciding_rule, 4)
        self.assertEqual(log[0].winning_claim_id, a)
        self.assertEqual(b.state, "yielded")

    def test_contention_log_is_immutable(self):
        a = self._claim(self._movement(priority_class="expedite"), self.lift)
        b = self._claim(self._movement(), self.lift, state="claimed")
        a.action_acquire()
        log = self.env["marshal.contention"].search([("claim_a_id", "=", a.id)])[0]
        with self.assertRaises(Exception):
            log.write({"reason": "tampered"})
        with self.assertRaises(Exception):
            log.unlink()

    # ---------------- occupancy is never preempted ----------------

    def test_occupied_claim_cannot_be_reacquired(self):
        c = self._claim(self._movement(), self.lift, state="occupied")
        with self.assertRaises(Exception):
            c.action_acquire()

    # ---------------- deadlock-free ordering ----------------

    def test_chokepoint_ranks_are_ascending_along_the_flow(self):
        """Claims are acquired in ascending rank so no cycle can form."""
        self.assertLess(self.dock.rank, self.aisle.rank)
        self.assertLess(self.aisle.rank, self.lift.rank)
        # scope to our fixtures: the database also holds the seeded venue
        ordered = self.env["marshal.chokepoint"].search(
            [("code", "like", "ZZT-%")]).sorted("rank")
        self.assertEqual(ordered[0], self.dock)


@tagged("post_install", "-at_install", "marshal")
class TestAccessRules(TransactionCase):
    """R13 — the record rules must actually constrain.

    Porterly has zero `domain_force` across 289 modules; access there is pure
    controller discipline. Marshal declares rules from module one, and these
    tests exist because a rule that reads [(1,'=',1)] with write granted is
    indistinguishable from no rule at all — and Odoo ORs rules within a group,
    so ONE permissive leftover silently nullifies every scoped rule beside it.
    """

    def _rules(self, model, perm):
        return self.env["ir.rule"].search([
            ("model_id.model", "=", model),
            (perm, "=", True),
            ("active", "=", True),
        ])

    def test_no_permissive_write_rule_for_operators(self):
        op = self.env.ref("marshal_core.group_marshal_user")
        for rule in self._rules("marshal.movement", "perm_write"):
            if op in rule.groups:
                self.assertNotIn(
                    rule.domain_force.replace(" ", ""), ("[(1,'=',1)]", '[(1,"=",1)]'),
                    f"Rule '{rule.name}' grants operators unrestricted WRITE — "
                    "it will OR with the scoped rule and nullify it.")

    def test_operator_write_rule_is_scoped_to_assignment(self):
        op = self.env.ref("marshal_core.group_marshal_user")
        scoped = [r for r in self._rules("marshal.movement", "perm_write")
                  if op in r.groups and "operator_id" in (r.domain_force or "")]
        self.assertTrue(scoped, "operators must have a rule scoped by operator_id")

    def test_operators_cannot_unlink_movements(self):
        op = self.env.ref("marshal_core.group_marshal_user")
        for rule in self._rules("marshal.movement", "perm_unlink"):
            self.assertNotIn(op, rule.groups,
                             "operators must never be granted unlink on movements")
