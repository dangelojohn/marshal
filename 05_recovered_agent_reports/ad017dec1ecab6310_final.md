No automated tests in any of these — hardening came from manual review passes, not test coverage. I have enough to report.

## Porterly repo family — findings

**Repo relationship (important):** `aug2026/porterly.git` (= local `~/porterly_dev` checkout) and `john/porterly_erp.git` share the same origin codebase (`custom_addons/Porterly_PRODUCTION-master/...`), but `aug2026/porterly` is a **stale pre-hardening snapshot** (initial commit 2026-07-12) while `john/porterly_erp` HEAD (78e35d57) contains a full security-remediation pass dated 2026-07-22 ("review repairs Q4–Q7"). **`john/porterly_erp` is the only canonical, safe source — do not build from `aug2026/porterly` or `~/porterly_dev`.** `qnap/porterly.git` is just a docker-compose/odoo.conf snapshot (no app code). `john/porterly_ops.git` is iMac deploy scripts only.

**Assets in `john/porterly_erp` (Odoo 16.0, author METISA SOLUTIONS, license mostly proprietary/OPL-1), all owned by John:**
| Module | What it is | Maturity | Verdict |
|---|---|---|---|
| `courier_tracking` + `courier_tracking_website` | parcel model (`parcels.tracking`), portal `/my/parcels`, public tracker | Built, hardened, no tests | **LIFT** (portal patterns) |
| `shipment_request` | public/portal outbound intake — legacy public form **retired in favor of** `porterly_outbound_pwa` | Built, remediated | PATTERN ONLY (see trap) |
| `job_request_custom` | `job.request` model, `/my/jobs` portal, staff assignment | Built, hardened | **LIFT** |
| `event_extend` | booth/exhibitor/group event customization on `event.event`/`calendar.event`, portal templates for exhibitors/groups | Built, deployed, largest surface | **GENERALISE** (real event-services domain logic) |
| `porterly_inbound_pwa` / `porterly_outbound_pwa` | mobile dock-capture + public/portal shipment intake with honeypot, rate-limit, idempotency-by-uuid, staff-gated putaway/ship/deliver actions | Built, deployed, actively hardened | **LIFT** — best-quality asset in the whole review |
| `pways_adv_parcel_management` (3rd-party, Preciseways) | parallel parcel-shipping model + portal, correctly scoped (`user_id` ownership checked before every render/download) | Built | PATTERN ONLY (license risk if 3rd-party) |

**TRAPS (confirmed by reading code, not just grep):**
1. **`aug2026/porterly` / `~/porterly_dev` :: `shipment_request/controller/main.py` `/ship_package_form/submit`** — `auth="public", csrf=False`, directly `create()`s a `parcels.tracking` from raw POST including `'group_id': int(post.get('group_id'))` with zero ownership validation → unauthenticated arbitrary-group billing injection. **Retired** in `porterly_erp` HEAD (route now just redirects to `/outbound`); still live in the stale repo/checkout.
2. **Same stale repo :: `courier_tracking_website/controller/main.py` `/tracking/submit`** — old code used `('tracking_ref','ilike',search)` (substring enumeration) plus a `search_partner` branch doing `('partner_id','ilike', name)` — lets an anonymous visitor list a customer's parcels by typing their name. **Fixed** in `porterly_erp` HEAD to exact-match only, no partner-name branch.
3. Several `csrf=False` routes remain in the *current* codebase (`/tracking/submit`, `/outbound/api/submit` type=json) but are either read-only lookups or `type='json'` (Odoo doesn't CSRF-check JSON-RPC the same way) — **not exploitable**, verified false-positive.
4. No sudo-on-read IDOR found in current `porterly_erp` HEAD controllers — every portal route I read scopes by `commercial_partner_id` or exact `user_id` match before `sudo()` browse/write.

**Non-Odoo asset — `qnap/porterly-future-reference.git`:** a dependency-free Python reference architecture (no Odoo), 4 commits, README describes a 5-reviewer hardened design: event-sourced idempotent ledger (`ledger.py`), guarded FSM (`fsm.py`, blocks e.g. "ship-before-store"), agents-propose/core-decides split (`agents.py` vs `core.py`) with **core re-deriving identity from ground truth rather than trusting agent claims**, policy-as-data pricing enforced server-side, atomic two-event commands, consent-gated billing. 74 invariant tests, `demo.py`, `serve.py`. **PATTERN ONLY** — this is the single most relevant artifact in the whole Porterly family for an agentic-scheduling product: it's literally "how do we let an LLM propose actions without letting it forge state," which is exactly the trust boundary the new exposition-services platform needs. Worth a dedicated read-through by whoever designs the new product's agent/core split.

Full findings above are ready to paste into the coordinator's inventory doc as the Porterly section.