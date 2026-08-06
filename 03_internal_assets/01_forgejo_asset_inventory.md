# ⚠ RECONCILIATION — two inventory passes, both preserved

**Added by the consolidating author, 2026-08-06.**

This file was written twice. A first agent produced an inventory, then a retry
(after an API failure) **overwrote it**. Both found real things the other
missed. This section preserves the lost findings and reconciles the conflict.

## The estimate conflict

| Pass | Estimate of platform already existing |
|---|---|
| First | **~35–40%** — scoped across aemi-platform, Porterly, OdooIQ, hermes-console, southbrook |
| Retry (body below) | **~55–60%** — deeper on the live aemi repo, lighter on the others |

**Neither is wrong; they measured different things.** The retry inspected the
live `aemi-platform.git` far more thoroughly and found modules the first pass
missed. The first pass covered hermes-console and southbrook governance, which
the retry did not. **Treat the range as 40–60% and re-measure per module before
planning any sprint.**

## Findings the retry lost — RESTORED and VERIFIED

### `avn.capability` — the single most valuable asset (VERIFIED by direct read)

Path: `aemi/aemi_venue/models/avn_capability.py` in `john/aemi-platform.git`.
Self-described as **"the Venue MCP"**. Confirmed contents:

```
SIDE_EFFECTS      = read | advisory | executable
CONNECTOR_TYPES   = mcp | api | portal | web_form | email | human_workflow
CONNECTOR_MATURITY= human_workflow 0 → email 1 → web_form 2 → portal 3 → api 4 → mcp 5
```

Three properties that matter enormously:

1. **`contract()` deliberately excludes `connector_type`.** A venue with a REST
   API and a venue with only a human bridge expose the *identical* contract.
   The caller cannot tell them apart and never branches. `invoke()` dispatches
   to `_connect_<type>` and every strategy returns a **normalised envelope**.
   A venue upgrades `web_form → api → mcp` with **zero change to callers**.
2. **`side_effect` already encodes the advisor/actor boundary** — the exact
   governance line the design spec §6.5 requires (agents propose, humans
   commit) is *already a field on this model*, not something to be added.
3. **Its documented capability examples already include "Loading Dock
   Schedule"** — the precise market gap the competitor research identified as
   unserved by all nine venue platforms.

Sibling models confirmed in the same module: `avn_venue`, `avn_space`,
`avn_capacity`, `avn_service`, `avn_supplier`, `avn_venue_service`,
`avn_portal`, `avn_provenance`, `avn_venue_note`, plus `avn_record_rules.xml`
(record rules present — unlike Porterly).

### Other first-pass findings not in the retry

- **hermes-console** — standalone FastAPI agent control plane implementing
  recommend → human-approve → tenant-push, with an MCP tool server. **LIFT the
  architecture.** Trap: its `auth.py` is effectively a no-op relying on
  Cloudflare Access network topology; safe only behind that.
- **southbrook-v19cr governance** — four-eyes self-review gate and row-locked
  race guard are near-LIFT; as-sold snapshot-at-confirm is GENERALISE.
- **AEMI AI layer previously found dead in production** (no API key wired).
  "Deployed" ≠ working.

## The fork problem — flagged by the retry, and it matters

The retry found that local `~/Downloads/AEMI/aemi_platform/addons/aemi_ai_platform/`
(uncommitted, Odoo 16, 34 tests, **never deployed**) and the live
`john/aemi-platform.git` (34 modules, deployed) are **two independently-evolved
lines with zero model overlap.**

`aemi.service.request` — whose `request_type` selection is *already*
`booth/shipping/rental/power/print/dropoff/av/other`, the exact exhibitor
service-order shape — lives in the **uncommitted, undeployed** line.

**Action independent of this project: commit the local line, then decide
whether the two converge or one is abandoned.** Uncommitted work with 34
passing tests is one disk failure from gone.

---

# Asset Inventory — What We Already Own, Reusable for an Exposition-Services Platform

Research date: 2026-08-06. Read-only inventory; nothing modified.

Access note: the task's suggested `ssh qnap-tunnel "git --git-dir=..."` command does not
work as written — the QNAP host firmware has **no git binary** (confirmed trap,
`qnap_no_git_scp_workaround`). Forgejo runs in a `forgejo` container reachable only via
Container Station's docker, which itself needs `DOCKER_HOST=unix:///var/run/system-docker.sock`
(the container-station docker binary is not on the default socket). Working command used
throughout this research:
```
ssh qnap-tunnel "export DOCKER_HOST=unix:///var/run/system-docker.sock; \
  /share/CACHEDEV3_DATA/.qpkg/container-station/bin/docker exec forgejo \
  git --git-dir=/data/git/repositories/<org>/<repo>.git <cmd>"
```

---

## 1. AEMI — local checkout (`~/Downloads/AEMI/aemi_platform/`)

Odoo 16 CE. `git status` shows `addons/aemi_ai_platform/` as **untracked** — this whole
layer is a local-only Phase-A design exploration, never pushed, never deployed. It is a
different, more recent design line than what's live on QNAP (see §2).

**`aemi_ai_platform` module (built + tested: 3 test files, 34 test methods, views,
security, portal controller — Odoo 16, never deployed):**

| Model | What it is | Verdict |
|---|---|---|
| `aemi.service.request` | Exactly the asset the task predicted. `request_type` selection is **already** `booth / shipping / rental / power / print / dropoff / av / other` — an exhibitor-service-order taxonomy, verbatim. Docstring explicitly cites the Porterly finding of the same shape "re-implemented five times (jobs, shipments, appointments, tickets, documents)." State machine draft→submitted→in_progress→waiting_customer→done/cancelled, each transition emits an observation. | **LIFT** — near-zero rework to repoint at an expo tenant |
| `aemi.agentic.mixin` | 7-method self-description contract (`_ai_semantics/_context/_capabilities/_dependencies/_timeline/_goal/_memory`) + `_ai_describe()` bundle + `_ai_observe()` verb. Framework-only, zero business coupling. | **LIFT** |
| `aemi.portal.mixin` | Ownership-safe portal query primitive. Docstring names the exact Porterly failure modes (§ Traps below) and structurally prevents them: never `sudo()` on read, fail-closed domain (`FALSE_DOMAIN` on falsy partner, never "all"), commercial-hierarchy scoping. `/my/requests` controller built on it as reference implementation (whitelisted sort keys, rate-limited create, forced requester on submit). | **LIFT** — this is the fix for the Porterly IDOR class |
| `aemi.observation` | Append-only fact store: `write()` blocks mutation of frozen fields, `unlink()` blocked for non-admins, confidence∈[0,1] SQL+Python constraint, corrections `supersede_with()` rather than overwrite. | **LIFT** |
| `aemi.attention.item` + `aemi.monitor` | Deterministic rule engine: a monitor scans a target model+domain, emits an observation + a ranked, snoozable/dismissable attention item. No LLM. Cron sweep, dedup against still-current observations. | **LIFT** |
| `aemi.ai.provider` | Model-router config abstraction (provider/workload/model/base_url + key stored only as an `ir.config_parameter` name, never on the record). **No live network calls implemented** — `action_check_config` validates completeness only. | **GENERALISE** (scaffold for the wiring, not a working router yet) |
| `aemi.knowledge.document` (+ `aemi.knowledge.chunk`) | RAG registry: sensitivity-tagged, deterministic paragraph-packing chunker (~1200 chars), `draft→chunked→embedded` state. Embeddings are a stated future increment — keyword search only today. | **GENERALISE / PATTERN ONLY** |
| `aemi.scoped.mixin` (`aemi_core`) | Foundational multi-tenant field (`aemi_client_id`) every record rule filters on. | **LIFT** |

Also present locally: `aemi_ai` (T0/T1/T2/T3 risk-tiered tool dispatcher, append-only
`aemi.tool.call.log`, idempotent `execute_intent` by `intent_id` — the write-governance
layer under all of the above) and `aemi_events` (`aemi.event`/`aemi.event.registration`,
a bare conference-registration model, deliberately not built on native `event.event`) —
**PATTERN ONLY**, thin.

## 2. AEMI — committed/live (`john/aemi-platform.git`)

Confirms the local checkout and the live repo are **two independently-evolved lines that
do not overlap** — none of the local `aemi_ai_platform` model names exist in the live
repo. The live repo (34 modules, actively committed, matches memory's "AEMI live QNAP
:8269") took a different, more mature path:

- **`aemi_venue` — the standout find, not anticipated in the task brief.** `avn.venue`
  (national reference DB, `exhibition_hall` is a first-class category, AI-readiness
  scoring), `avn.space` (parent/child divisible sections — real halls split into lettered
  sub-halls, `exhibit_hall` space type), `avn.capacity` (setup-style capacity matrix,
  `exhibit (booths)` is a literal `SETUP_TYPES` entry), `avn.service` (orderable venue
  service with flat/tiered/weight-banded pricing — parcel handling, rigging, power
  drops), `avn.supplier` (exclusive in-house AV/catering constraint modelling). Built,
  deployed, tenant-nullable-shared-reference-data pattern already solved. **LIFT** — this
  is close to a venue/hall/booth-space/capacity module ready-made.
- `aemi_scheduler` — read-only critical-path/conflict/capacity analysis over an
  `aemi.ops.item`/`aemi.ops.dependency` DAG twin, explicitly forbidden from writing
  planning dates (that stays behind an ownership-gated `recompute_dates(commit=True)`).
  Handles `finish_to_start/start_to_start/finish_to_finish/start_to_finish` edge types
  correctly (a bug fix noted in its own docstring). **GENERALISE** — booth-build-out
  schedule critical path.
- `aemi_attention` v2 (`aemi.ops.item/dependency/readiness/gravity/risk_threshold`) —
  successor to the local `aemi.attention.item`/`aemi.monitor` pair, more evolved.
  **GENERALISE**.
- `aemi_commerce` (`offering/order/invoice/promo/settlement`) — **GENERALISE** for
  exhibitor billing/booth-fee settlement.
- `ai_agent_core/ingest/queue/runtime` — the live agent execution plane (matches memory:
  claim/heartbeat/complete LIVE). **GENERALISE with caution** — memory also records the
  AI layer as functionally dead (no Anthropic key configured) as of the last full review.
- `aemi_onsite` (`aemi.event`/`aemi.event.registration`), `aemi_governance` — thin,
  association-specific. **PATTERN ONLY**.

## 3. Porterly (`aug2026/porterly.git`, `john/porterly_ops.git`) — brief per instructions

`aug2026/porterly.git` is **mostly a vendored third-party/OCA module dump** (24.8k files;
`HR_PAYROLL_16/`, a generic Odoo-store addon shelf under `Porterly_PRODUCTION-master/`) —
not Porterly IP. The genuine custom modules, once filtered out: `Receiving`,
`courier_tracking` (+ `_website`), `metisa_parcel_search`, `porterly_inbound_pwa`
(models `job_request.py` + `parcels_tracking.py` — **direct confirmation** of the
"job/shipment/ticket re-implemented five times" finding cited in `aemi.service.request`'s
own docstring), `pways_adv_parcel_management` (arrival/delivery, packaging, price lists,
type-of-service), `porterly_ai_parcel_extract`, `porterly_documents_finder`,
`stock_quant_package_*` customizations. **Verdict: PATTERN ONLY** — the parcel/job/tracking
*domain shape* maps to exhibitor material handling and a freight/receiving desk, but the
code is Odoo 16 legacy tangled with vendored bulk and carries the known security traps
below; `aemi.service.request` is the already-cleaner reimplementation of the same idea.
`john/porterly_ops.git` is pure iMac deploy plumbing (launchd, conf) — no business
models. **AVOID / not relevant.**

## 4. `qnap/odooiq-factory-intelligence.git` — scheduler architecture

Odoo 16-targeted. Built with tests (78/89 passing per latest commit — not fully green,
not confirmed live). Architecture:

- **Capacity model**: work-center calendars + flow-shop precedence (operations execute in
  routing sequence; no sequence-dependent setup optimization — explicitly out of scope
  v1). A pure EDD-greedy forward-pass solver (`services/scheduler.py`) takes plain
  dataclasses in/out and never touches `self.env` — stated as ERP-portable by design.
- **Read-only against core models**: never writes `date_start`/`date_finished`/
  `date_deadline` on `mrp.production`/`mrp.workorder`. All output lands on its own
  `oiq.schedule.run`/`oiq.schedule.slot` "shadow schedule."
- **Confidence ranges** (`services/delivery_estimator.py`): `oiq.delivery.estimate` is
  *always* a range (`completion_start`→`completion_end`) plus a quality label
  (low/med/high) plus a stated historical-accuracy percentage — never a bare date or
  percentage. Spread comes from the p10/p50/p90 of a historical completion-ratio
  distribution for the cohort, shrinking as sample count grows (`SHRINK_K`) and forced to
  a wide, honestly-labelled default below `MIN_SAMPLE_COUNT=20`. Durations are corrected
  by a calibration engine *before* the solver ever sees them.
- Explicitly self-documents as an EDD *heuristic*, not a provably-optimal schedule —
  same "honest boundaries" doctrine seen elsewhere in this ecosystem.
- **Verdict: GENERALISE** — directly reusable for booth-build-out / general-contractor /
  drayage delivery-confidence estimates; the solver core is engine-agnostic.

## 5. Southbrook governance patterns (`~/southbrook-v19cr`, `southbrook_plm/southbrook_eco.py`)

The reusable shape (no cabinetry detail): an Engineering Change Order moves through a
user-configurable stage pipeline; each target kind (BOM / cut-spec / rule / document) is
handled by its own commit strategy but all share the same skeleton — a **versioned spec
object** that is superseded rather than overwritten (new version created, prior archived,
never edited in place), an **as-sold effectivity pin** so a sold/committed record stays
locked to the spec version it was sold against regardless of later engineering changes
(covered by its own test file), a **four-eyes approval gate** (stage-configurable
`approval_required`, PLM-Approver group membership, and an explicit rule blocking the
ECO's own Responsible from self-approving, with a logged "break-glass" bypass as the only
exception path), and **immutable audit** once applied (`write()` structurally blocks edits
on Applied/Rejected records — terminal states are terminal). **Verdict: PATTERN ONLY** —
port the state-machine shape for expo change control (booth-spec revisions, floor-plan
changes, contract addenda), not the module itself.

## Traps — must not inherit

Prior Porterly reviews (`porterly_portal_security_fixes_deployed`,
`porterly_custom_code_review_2026_07_22`) flagged, not re-verified here:
- **IDOR via empty-domain searches** on `/my/*` portal routes (no ownership filter before
  the fix).
- **`sudo()` on read paths**, voiding record rules and exposing cross-tenant data.
- **`csrf=False`** on form-accepting controllers.

These three are exactly the failure modes `aemi.portal.mixin` (§1) was purpose-built to
structurally prevent — the fix already exists in code, it has just never shipped.

## Reuse manifest

| Asset | Repo | Odoo | Maturity | Verdict |
|---|---|---|---|---|
| `aemi.service.request` | local `aemi_platform` | 16 CE | built, tested, undeployed | **LIFT** |
| `aemi.agentic.mixin` | local `aemi_platform` | 16 CE | built, tested, undeployed | **LIFT** |
| `aemi.portal.mixin` | local `aemi_platform` | 16 CE | built, tested, undeployed | **LIFT** |
| `aemi.observation` | local `aemi_platform` | 16 CE | built, tested, undeployed | **LIFT** |
| `aemi.attention.item` / `aemi.monitor` | local `aemi_platform` | 16 CE | built, tested, undeployed | **LIFT** |
| `aemi.scoped.mixin` | local + live `aemi_core` | 16 CE | deployed | **LIFT** |
| `aemi.ai.provider` | local `aemi_platform` | 16 CE | scaffold (no network calls) | **GENERALISE** |
| `aemi.knowledge.document` | local `aemi_platform` | 16 CE | built, no embeddings | **GENERALISE / PATTERN ONLY** |
| `avn.venue`/`avn.space`/`avn.capacity`/`avn.service`/`avn.supplier` | live `aemi-platform.git` | 16 CE | deployed | **LIFT** |
| `aemi.scheduler` (CPM) | live `aemi-platform.git` | 16 CE | deployed | **GENERALISE** |
| `aemi_attention` v2 (`aemi.ops.item` et al.) | live `aemi-platform.git` | 16 CE | deployed | **GENERALISE** |
| `aemi_commerce` | live `aemi-platform.git` | 16 CE | deployed | **GENERALISE** |
| `ai_agent_core/ingest/queue/runtime` | live `aemi-platform.git` | 16 CE | deployed, AI layer reported dead | **GENERALISE w/ caution** |
| `aemi.event`/`aemi.event.registration` | local + live | 16 CE | thin scaffold | **PATTERN ONLY** |
| Porterly job/parcel/tracking modules | `aug2026/porterly.git` | 16 CE | legacy, vendored bulk + own code mixed | **PATTERN ONLY** |
| OdooIQ shadow scheduler + delivery-confidence engine | `qnap/odooiq-factory-intelligence.git` | 16 CE | built, 78/89 tests, not confirmed live | **GENERALISE** |
| Southbrook ECO governance pattern | `southbrook-v19cr` | 19 CE | deployed (cabinetry) | **PATTERN ONLY** |

## Honest %-exists estimate

Roughly **55-60%** of an exposition-services platform's *data model and core
architecture* already exists in some working form across these repos: venue/hall/booth
space + capacity (~90%, live), exhibitor service ordering incl. the exact booth/shipping/
rental/power/print/dropoff/av taxonomy (~85%, built but undeployed), portal ownership
security (~80%, built but undeployed), attention/exception monitoring (~70%, two
generations), billing/settlement (~60%), change-control governance pattern (~60%, ported
from a different domain), scheduling + delivery-confidence (~50%, built for
manufacturing, needs re-domaining), knowledge/RAG (~50%, no embeddings), agent execution
substrate (~50%, live but AI calls reportedly not wired to a key). Missing entirely:
graphical floor-plan/CAD booth layout, expo-specific sales CRM/prospectus, badge/lead-
retrieval scanning, drayage/GC invoicing integrations, union labor scheduling. The
caveat that matters most: the strongest, most on-point piece (`aemi.service.request` +
its portal/observation/attention scaffold) has **never been deployed or committed** —
it is high quality but has zero production mileage, and it lives in a design line the
live AEMI repo has already diverged from.
