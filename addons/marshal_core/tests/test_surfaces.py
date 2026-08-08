from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install", "marshal")
class TestExhibitorAndSms(TransactionCase):
    """Wave 3 — the customer-facing declare/track flow and the driver SMS
    layer. Controllers themselves are verified over real HTTP (matching how
    the runner API was verified — curl against a live instance, not a Python
    HTTP test harness); these tests cover the model-level logic underneath."""

    def _movement(self, **kw):
        vals = {"crate_ref": "C1", "dest_booth": "412"}
        vals.update(kw)
        return self.env["marshal.movement"].create(vals)

    # ---------------- declare token ----------------

    def test_declare_token_generated_on_create(self):
        m = self._movement()
        self.assertTrue(m.declare_token, "every movement needs a public "
                        "tracking token, not just ones from the portal")

    def test_declare_token_is_unique(self):
        a, b = self._movement(), self._movement()
        self.assertNotEqual(a.declare_token, b.declare_token)

    def test_unclaimed_planned_movements_are_searchable_by_claim_ids(self):
        """Regression: claim_count is a non-stored compute with no search()
        defined, so a domain leaf on it is silently DROPPED by Odoo rather
        than raising — a filter meant to exclude claimed movements would
        match everything. claim_ids, the real relation underneath it, is the
        field the receiver's pending-list controller must filter on."""
        m = self._movement(state="planned")
        found = self.env["marshal.movement"].search([
            ("state", "=", "planned"), ("claim_ids", "=", False), ("id", "=", m.id),
        ])
        self.assertIn(m, found, "unclaimed planned movement should be found")

        self.env["marshal.claim"].create({
            "movement_id": m.id,
            "chokepoint_id": self.env["marshal.chokepoint"].search([], limit=1).id,
        })
        found_after = self.env["marshal.movement"].search([
            ("state", "=", "planned"), ("claim_ids", "=", False), ("id", "=", m.id),
        ])
        self.assertNotIn(m, found_after, "once claimed it must drop out of the unclaimed set")

    def test_declare_token_survives_explicit_blank(self):
        """A caller that doesn't set declare_token still gets one — the
        create() override must not be skippable by omission."""
        m = self.env["marshal.movement"].create({"crate_ref": "C2"})
        self.assertTrue(m.declare_token)

    # ---------------- SMS: keyword parser (D-009 fallback) ----------------

    def test_parse_reply_yes_variants(self):
        Sms = self.env["marshal.sms.log"]
        for word in ("Y", "y", "yes", "Yes!", "YEP", "ok", "confirmed"):
            self.assertEqual(Sms.parse_reply(word), "yes", f"{word!r} should parse as yes")

    def test_parse_reply_no_variants(self):
        Sms = self.env["marshal.sms.log"]
        for word in ("N", "no", "cancel"):
            self.assertEqual(Sms.parse_reply(word), "no")

    def test_parse_reply_unrecognized(self):
        Sms = self.env["marshal.sms.log"]
        self.assertEqual(Sms.parse_reply("yeah be there in 10"), "unrecognized")
        self.assertEqual(Sms.parse_reply(""), "unrecognized")
        self.assertEqual(Sms.parse_reply(None), "unrecognized")

    # ---------------- SMS: sending, gated ----------------

    def test_send_without_provider_configured_is_simulated_not_silent(self):
        """HONEST BOUNDARY: no Twilio configured must never look identical to
        a successful send — it must be visibly logged as simulated."""
        m = self._movement(driver_phone="+14165550123")
        log = self.env["marshal.sms.log"].send(
            m, "assignment", dock="4", time="14:20", crate=m.name)
        self.assertTrue(log)
        self.assertEqual(log.state, "simulated")
        self.assertIn("Reply Y to confirm", log.body)

    def test_send_without_phone_is_a_noop(self):
        m = self._movement()  # no driver_phone
        log = self.env["marshal.sms.log"].send(m, "assignment", dock="4",
                                               time="14:20", crate=m.name)
        self.assertFalse(log)

    def test_send_respects_opt_out(self):
        m = self._movement(driver_phone="+14165550123", sms_opt_in=False)
        log = self.env["marshal.sms.log"].send(m, "assignment", dock="4",
                                               time="14:20", crate=m.name)
        self.assertFalse(log)

    def test_confirmed_template_under_one_segment(self):
        m = self._movement(driver_phone="+14165550123")
        log = self.env["marshal.sms.log"].send(m, "confirmed", time="14:20")
        self.assertLessEqual(len(log.body), 160)

    # ---------------- SMS: inbound webhook signature ----------------

    def test_twilio_signature_round_trips(self):
        Sms = self.env["marshal.sms.log"]
        token = "test-auth-token"
        url = "https://marshal.show/marshal/sms/inbound"
        params = {"From": "+14165550123", "Body": "Y", "To": "+14165551234"}

        # Compute what a genuine Twilio request would send, the same way the
        # verifier does, so this test proves round-trip correctness rather
        # than just re-asserting the implementation against itself blind.
        import base64, hashlib, hmac
        s = url
        for key in sorted(params.keys()):
            s += key + params[key]
        good_sig = base64.b64encode(
            hmac.new(token.encode(), s.encode(), hashlib.sha1).digest()
        ).decode()

        self.assertTrue(Sms.verify_twilio_signature(token, url, params, good_sig))
        self.assertFalse(Sms.verify_twilio_signature(token, url, params, "tampered"))
        self.assertFalse(Sms.verify_twilio_signature(token, url, params, ""))

    def test_twilio_signature_rejects_tampered_params(self):
        """If a param is altered after signing, the signature must no longer
        validate — otherwise the check is theatre."""
        Sms = self.env["marshal.sms.log"]
        token = "test-auth-token"
        url = "https://marshal.show/marshal/sms/inbound"
        original = {"From": "+14165550123", "Body": "Y"}

        import base64, hashlib, hmac
        s = url
        for key in sorted(original.keys()):
            s += key + original[key]
        sig = base64.b64encode(
            hmac.new(token.encode(), s.encode(), hashlib.sha1).digest()
        ).decode()

        tampered = {"From": "+14165550123", "Body": "N"}  # attacker flips Y to N
        self.assertFalse(Sms.verify_twilio_signature(token, url, tampered, sig))
