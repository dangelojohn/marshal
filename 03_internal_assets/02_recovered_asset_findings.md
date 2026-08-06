# Recovered asset findings — reports that never reached the study

**Provenance:** during the 2026-08-06 research run, two coordinator agents died
on `Connection closed mid-response` before writing their reports. They had
already dispatched six sub-agents asynchronously. **Five of those six completed
full reports that were never delivered** — the parents died first.

Recovered 2026-08-06 from the session transcripts and reproduced here. Nothing
below appears in `01_forgejo_asset_inventory.md`; it is additive, not a rewrite.

**Confidence:** these are direct-read findings with file:line evidence, produced
by agents that ran to completion. Treat them as equal in weight to the inventory,
higher where they cite line numbers.

---

## 1. `qnap/porterly-future-reference` — the most relevant artifact found anywhere

**This repo was missed entirely by the surviving inventory pass.** Both recovered
reports flag it, and one calls it *"the single most relevant artifact in the whole
Porterly family for an agentic-scheduling product."*

Not Odoo. A dependency-free Python reference architecture, 4 commits, latest
2026-07-23. Files: `agents.py`, `core.py`, `fsm.py`, `ledger.py`, `policy.py`,
`projections.py`, `validators.py`, `demo.py`, `serve.py`.

Its README describes a five-reviewer hardened design:

| Mechanism | What it does |
|---|---|
| **Event-sourced idempotent ledger** (`ledger.py`) | append-only; replay-safe |
| **Guarded FSM** (`fsm.py`) | blocks illegal transitions, e.g. ship-before-store |
| **Agents-propose / core-decides** (`agents.py` vs `core.py`) | **core re-derives identity from ground truth rather than trusting agent claims** |
| **Policy-as-data pricing** | enforced server-side, not in the agent |
| **Atomic two-event commands** | no partial state |
| **Consent-gated billing** | no charge without recorded consent |
| **74 invariant tests** | the only tested artifact in the entire Porterly family |

**Why it matters here:** it is a worked answer to *"how do we let an LLM propose
actions without letting it forge state"* — precisely the trust boundary an
agentic scheduling product needs. It is the conceptual sibling of Southbrook's
`PLM_LIFECYCLE` identity sentinel, arrived at independently.

**Verdict: PATTERN ONLY** (not Odoo, so nothing lifts directly) — but it deserves
a dedicated read-through by whoever designs the agent/core split. See
`spec/03_predictive_scheduling_analysis.md` §6, which builds on it.

---

## 2. Porterly — evidence-grade security and licence detail

Supersedes the summary treatment in `01`. All against `john/porterly_erp` HEAD
(64 commits, latest 2026-07-25) unless stated.

### Repo relationships — confirmed

| Repo | Commits | Status |
|---|---|---|
| **`john/porterly_erp`** | 64 | **AUTHORITATIVE.** 289 modules; carries the `security(Q7)` / `review repairs (Q5)` remediation campaign |
| `aug2026/porterly` | 3 | **STALE.** Squashed 2026-07-12 snapshot; its only later commit is a licence-text swap, *not* a code sync |
| `~/porterly_dev` (local) | — | tracks the stale mirror. Verified: `grep attachment_guard` → no hit; `in_shipment.py` still pre-fix |
| `john/porterly_ops` | 1 | iMac deploy scripts only |
| `qnap/porterly` | 2 | Decommissioned; `addons/` is literally empty |

### The licence finding — this constrains reuse more than the security issues

**`pways_adv_parcel_management` (AGPL-3) is the only freely-reusable licence
found in the entire Porterly tree.** Everything else is `OPL-1` or
"Other proprietary", authored by METISA SOLUTIONS.

John owns METISA, so this is a *formality* rather than a blocker — but it means
lifting code requires a deliberate relicensing decision per module, not an
assumption. Ironically the one AGPL module is third-party (Preciseways) and
carries the weakest controllers.

### Security — verified with file:line

**CONFIRMED — CSRF-via-GET, live, and missed by the review campaign**
`event_extend/controller/main.py:682-702` — `/enable/portal` and
`/disable/portal` perform privileged `.sudo()` state changes on bare **GET**
routes. This sidesteps CSRF entirely regardless of the `csrf` flag, because
Odoo's CSRF protection covers POST. A link in an email is enough to trigger it.

**CONFIRMED — no ORM backstop anywhere**
`grep -ln domain_force` across all 289 modules returns **zero hits** for
`courier_tracking`, `pways_adv_parcel_management`, `shipment_request`,
`event_extend`, `event_booth_config`, `metisa_event_portal`,
`metisa_parcel_search`, `porterly_inbound_pwa`, `porterly_outbound_pwa`,
`in_shipment`. Access control is 100% controller discipline. One mis-coded
domain is a full data leak with nothing beneath it.

**CONFIRMED — `sudo()` on reads, but with an instructive split**
Reviewed modules now pair `.sudo()` with a hand-built ownership domain and carry
audit comments. Untouched ones don't:
- *Fixed:* `courier_tracking/controller/main.py:74-84` — comment reads
  *"previously counted ALL parcels globally, leaking total volume"*
- *Best pattern in the codebase:* `job_request_custom/controllers/main.py:394` —
  the `/my/jobs` query runs **without** `sudo()`; `.sudo()` is applied at :396
  only to the already-filtered recordset, for rendering
- *Still risky:* `pways_adv_parcel_management/controllers/portal.py:13,23,36,52,68,91,100`
  — every read `.sudo()`, domain inline, no ir.rule

**REFUTED — "empty search domains"** — domains are non-empty everywhere checked.
The real issue is the missing ir.rule layer above, not the domains.

**REFUTED — most `csrf=False`** — `/tracking/submit` is a read-only lookup;
`/outbound/api/submit` is `type='json'`, which Odoo does not CSRF-check the same
way. Rate-limited and honeypotted. Not exploitable. **The GET routes are the real
finding.**

**Historic, now fixed — worth reading the fix, not the original**
- `shipment_request/controller/main.py` `/ship_package_form/submit` was
  `auth="public", csrf=False` creating a `parcels.tracking` from raw POST
  including `'group_id': int(post.get('group_id'))` with no ownership check →
  unauthenticated arbitrary-group billing injection. Now redirects, creates
  nothing. **Still live in the stale mirror and in `~/porterly_dev`.**
- `courier_tracking_website` `/tracking/submit` used
  `('tracking_ref','ilike',search)` plus a `search_partner` branch doing
  `('partner_id','ilike',name)` — anonymous parcel enumeration by customer name.
  Now exact-match only.

### Module verdicts

| Module | Licence | Verdict |
|---|---|---|
| `event_extend` | Other proprietary | **GENERALISE** — real exhibitor/booth domain logic; best portal reference (`_prepare_groups_domain`, `_get_owned_event` IDOR guard) |
| `porterly_outbound_pwa` / `inbound_pwa` | METISA | **GENERALISE** — richest public→validated-record intake: honeypot, rate-limit, idempotency-by-uuid, staff-gated transitions |
| `event_booth_config` | METISA | **LIFT** — self-owned |
| `job_request_custom` | OPL-1 | **PATTERN** — the access-control reference |
| `courier_tracking(+website)` | proprietary | **LIFT** portal patterns / PATTERN for the rest |
| `pways_adv_parcel_management` | **AGPL-3** | **GENERALISE the data model, rewrite the controllers** |

**No tests anywhere.** Twelve modules checked. Maximum maturity in this family is
"built and hardened", never "tested".

---

## 3. `hermes-console` — two memory notes are now wrong

Standalone FastAPI + Vue3 agent control-plane. **Not an Odoo module.** Runs as its
own compose stack (`hermes-api`, `hermes-ui`, optional `hermes-whatsapp`) behind
Caddy/Cloudflare, and treats Odoo as *one of several tenant bridges* it pushes
approved recommendations into (`api/tenant_bridges/southbrook_hermes.py`) — never
the reverse.

Loop: `agent_loops.py` runs scheduled/triggerable loops (`platform_health`,
`daily_digest`, `backup_health`, optional `lead_prospector`) → LLM returns
structured JSON recommendations → persisted to **local SQLite** (survives
Odoo/QNAP restarts) in a `queue → approve/reject → apply` state machine → pushed
through a bridge. Also runs a full **MCP server** (`api/mcp/`) with read tools
(Cloudflare, Home Assistant, Reolink, Phyn) and Phase-2 write tools that respect
the same approve-gate. 30 test files, 48 commits, latest 2026-06-17.

### ⚠ The sub-agent proposed two memory corrections — both were checked, both fail

The recovered report asserted that two existing memory notes were outdated. I
verified each directly against `qnap/hermes-console.git` HEAD (`55d2986`) before
acting. **Neither correction survives, and the check turned up something more
interesting.**

**Claim 1 — "`hermes_console_ask_provider_openai_only` is outdated, a native
Anthropic provider now exists." → HALF TRUE, CONCLUSION WRONG.**

`AnthropicLLMClient` does exist (`api/llm.py:483`) and is registered when
`anthropic_api_key` is set (`:738-743`), alongside the OpenAI-compatible client
and a `GeminiGroundedClient` (`:308`). So the provider exists.

But the memory is not about the provider registry — it is about the
`/api/hermes/ask` route being **pinned** to `openai` because
`AnthropicLLMClient.chat()` doesn't translate Anthropic `tool_use` blocks into
the OpenAI `tool_calls` shape. And:

- there is **no `/api/hermes/ask` route** anywhere in this repo
- there is **no `api/hermes_agent.py`** — `git log --all` on that path is empty,
  so it never existed here
- `api/llm.py` contains **no `tool_use` or `tool_calls` handling at all**
- the memory's cited commit **`c0b5845` is not a valid object** in this repo
  (48 commits, first is `83aa341 feat(hermes): initial standalone agent control plane`)

**The provider existing does not mean the pin was removed — and the code the
memory describes is not in this repository.** Leaving the memory intact.

**Claim 2 — "`hermes_whatsapp_disabled` needs qualifying, the sidecar is built
not vaporware." → MISREADING.** That memory never said the code was unbuilt. It
records that the *deployed container* was stopped on 2026-06-22 because an
unpaired WhatsApp Web + Chrome backend was driving ~2 MB/s sustained block reads
(887 GB over 5 days) against the same disk as `southbrook-postgres`. It already
documents the re-enable recipe as "uncomment + compose up" — i.e. it already says
it is a flip-a-flag feature. No correction needed.

### 🔎 What the check found instead — unpushed local work, not a fork

`api/hermes_agent.py`, the `/api/hermes/ask` route, and commit `c0b5845` are all
real (verified end-to-end 2026-07-01 against the running Southbrook
hermes-console). **None are in `qnap/hermes-console.git`.**

Traced to source: **`~/hermes-console` is 3 commits ahead of `forgejo/main`**,
with 3 further files dirty.

```
a2c41f2  feat(llm) — Anthropic tool_calls translation for run_agent_loop
c0b5845  fix(api) — pin ask endpoint to openai-compat provider (Gemini)
8a26171  feat(api) — POST /api/hermes/ask sidecar route for Southbrook Fabio
 M api/hub_manifest.py   M whatsapp/Dockerfile   M whatsapp/bridge.js
```

The `github` remote has never been fetched — no remote-tracking refs exist — so
`forgejo` is the only real remote, and it is behind.

**Not a fork. Unpushed work.** Which is worse in one respect: a fork has two
copies, this has one. **Fabio's entire tool-calling path exists only on this
Mac** — the same exposure as `aemi_ai_platform`. That makes two bodies of
local-only work found in this review, both load-bearing, neither pushed.

Incidental correction to the correction: `a2c41f2` *does* implement the Anthropic
`tool_calls` translation the memory note listed as a future improvement — but the
pin was never lifted. `provider_name = "openai"` is still hardcoded at
`api/main.py:844`, and the comment above it at :832-836 is now stale. Lifting it
is a one-line change plus a live tool-calling test.

**Method note:** this is exactly the failure mode the study's own README warns
about. The sub-agent read a repo, found a provider class, and generalised to a
claim about a route it never opened. Its structural findings (§1, §2, §4, §5)
cite file:line and hold up; this one didn't and didn't.

**Verdict: LIFT the architecture.** `tenant_bridges/` — one small adapter class
per target system — is the right shape for "watch the scheduling board, raise
attention items, draft exhibitor comms." The local-SQLite-first design decouples
the agent runtime from whatever system of record you build.

**Trap (unchanged):** `auth.py` is a no-op relying entirely on Cloudflare Access
network topology. Fine behind the tunnel, fatal if ever exposed directly.

---

## 4. Negative findings — two repos worth nothing

Recording these so nobody re-investigates.

- **`qnap/odooai`** — a stock Odoo 19 CE demo stack snapshot. docker-compose,
  odoo.conf, empty addons dir. No AI code, no custom modules, nothing
  agent-related despite the name. Single commit 2026-05-26, untouched.
- **`qnap/ops`** — generic QNAP ops snapshot: shared Caddyfile, alfacore compose,
  backup/boot-recovery scripts, autorun hook. Single commit 2026-05-26,
  untouched. Its README "gotchas" table is a decent QNAP deployment reference and
  is the only reason to open it.

---

## 5. Southbrook governance — the depth the inventory summarised

`01` lists these as patterns. The recovered report carries the mechanics, which
is what makes them portable. Reproduced because the detail is the value.

**Versioned specs** — `southbrook.cut.spec`. `version` auto-increments only when
one of 8 named `CONSTANT_FIELDS` actually changes value (per-record comparison in
`write()`, cut_spec.py:163-189) — chatter and name edits don't bump it.
`draft→active→superseded` with a hard single-active invariant
(`_check_single_active`, :284). Point-in-time reconstruction via
`active_from`/`active_to` half-open `[from, to)` plus a doubly-linked
`predecessor_id`/`successor_id` chain, **both stamped from one shared `now`** in
`action_activate()` (:480-514) so windows abut with zero gap or overlap.
`_get_spec_active_at(when)` (:332) answers "what was live on date X".
→ *"Event-package spec v3, active during the Q3 booth-assignment window."*

**As-sold pinning** — `sale.order.line`. Snapshots captured at `action_confirm`
(:113-158), idempotent. A hardening pass closed a real gap: lines added to an
**already-confirmed** order never got stamped because `action_confirm` fires once
— fixed by also capturing in `create()` when `order_id.state in ('sale','done')`
(:211-220). Deliberately **not** captured at draft, because pinning a quotation
is wrong the moment an ECO lands before acceptance.
→ *Package frozen at contract signature, not at quote — including change orders.*

**Four-eyes** — not a role count, an identity comparison:
`is_self_review = self.env.user.id in (eco.user_id.id, eco.create_uid.id)`
blocks approval by the ECO's own Responsible or creator (:1150, :1604). Bypass
requires a mandatory reason, and arming is logged separately from exercising
(:704-722, :946-955). RPC-hardened: setting `emergency_bypass` is blocked in both
`create()` and `write()` unless the caller holds the approver group (:686-698,
:751-763) — closing the hole where the ACL needed for draft authoring would let a
plain user self-arm. Race-safe via `SELECT ... FOR UPDATE` + `invalidate_recordset`
before the decision check (:1131-1137).

**Immutable audit — two mechanisms, deliberately different strength:**
- *Hard:* `southbrook.eco.write()` refuses writes to applied/rejected ECOs outside
  a narrow allowlist, gated by an **object-identity sentinel** —
  `PLM_LIFECYCLE = _PlmLifecycleToken()`, a `__slots__=()` singleton importable
  only in-process, compared with `is`, never `==` or truthiness, because JSON-RPC
  can forge `{"context":{"plm_lifecycle": true}}` but cannot forge Python
  identity. **The most portable single technique in the codebase.**
- *Soft:* `southbrook.qr.scan.log` has no override at all — immutability is pure
  ACL (`perm_write=0, perm_unlink=0`). Fine for a high-volume append log,
  **but any `sudo()` bypasses it.** Don't use this shape where the guarantee matters.

**Typed effectivity** — immediate / scheduled-date (cron auto-applies when due) /
use-up (human-confirmed, never auto-applies). Treats *"is it approved"* and
*"when does it take effect"* as orthogonal (:288-459). Supersession via
`action_create_superseding` (:1383-1498) rather than reopening history, with
explicit stripping of stale description and attachments so a reviewer cannot
rubber-stamp against old evidence. Rejection reason is free text, deliberately
not a coded taxonomy (comment cites Arena/Windchill/CM2 precedent).

Tests: `test_effectivity_pinning.py`, `test_eco_governance.py`,
`test_eco_governance2.py`, `test_eco_workflow.py`, `test_w079_cut_spec_version.py`.
