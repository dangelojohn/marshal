# The Porterly Design corpus — Marshal's backlog already exists

**Source:** `/Users/naadmin/Downloads/Porterly Design` — 461 files, 344 markdown,
7.4 MB, July–August 2026. Indexed at `00_INDEX_and_What_We_Were_Building.md`.

**This is the most valuable thing found for Marshal so far**, and it is not the
code. It is a scored, feasibility-vetoed build backlog for **Odoo 16 CE** —
which, since D-010, is exactly Marshal's target.

---

## The headline

> **Porterly v2's 26 hardened recommendations are substantially Marshal's
> Phase 1–3 backlog, already scored for feasibility by a four-reviewer panel with
> a hard veto — on the exact stack Marshal will use.**

28 candidates → a 7-lens stakeholder panel → an adversarial Odoo-16-CE
feasibility breaker → 26 survivors, re-scored with an 8/10 PASS/FAIL and a
**feasibility veto**. Only 2 of 28 cleared on first pass. That is real work,
already done, by people who knew the constraints.

---

## ⭐ The business insight that validates Marshal's entire thesis

From `Porterly Future/` — owner-supplied, and it survived the adversarial loop:

> At label capture the system already knows which of **two completely different
> products** it holds.

| | Guest incidental mail | **Exhibitor / event logistics** |
|---|---|---|
| Expects to pay? | **No** — *"it's my mail"* | **Yes — freight is a known show cost** |
| Relationship at risk | The hotel's guest relationship | A B2B logistics relationship |
| Right model | Free / flat-trivial, disclosed — an amenity | **Priced by weight, dims, storage, accessorials** |

Treating both as *"a parcel, charge by weight"* is the single conflation that
produces both guest resentment and the monthly reconciliation meeting.

**Marshal is the second column.** This is Porterly's own analysis concluding —
independently, months earlier — that **the exhibitor/event side is where money
legitimately lives, because it is the side where the payer expects to pay.**

That is D-005 §2 arrived at from a completely different direction. **Marshal is
the monetizable half of Porterly, extracted and deepened with the resource layer
Porterly never had.**

---

## ⭐ The architecture line, reached independently

From `Porterly Future/` — the thesis in one line:

> **"Perception is probabilistic, actuation is deterministic — an LLM may read
> and propose, only a typed idempotent core may act."**

That is **exactly** D-009's conclusion, written weeks earlier. Reached with an
adversarial agent loop, a five-reviewer code review, and a runnable
`reference-build/` (pure-stdlib Python: invariant tests, 10 end-to-end scenarios,
an HTTP surface).

This is the fourth independent convergence on the same principle across our
codebases — `PLM_LIFECYCLE`, `porterly-future-reference`, hermes-console, and
now this. **Stop treating it as a design choice and treat it as settled doctrine.**

Also worth heeding: a big-bang rewrite **scored ~45%** and was rejected in favour
of strangler-fig with shadow mode and a hard kill-switch.

---

## The recommendations that are Marshal's backlog

Scored `BF / FO / TA / FZ`, where **FZ is the feasibility veto**.

| R | What | Score | Marshal relevance |
|---|---|---|---|
| **R04** | **Tamper-evident custody log** | 9/9/10/**6** → REVISED | **D-005's defensible record.** Mechanism re-scoped by the loop to a **per-parcel hash chain + periodic anchor, NOT a global chain** — that FZ 6 is the feasibility reality of global chaining on CE. **Use the revised mechanism** |
| **R25** | Testing/CI + migration harness | 9/7/8/8 | **KEEP — the linchpin, ship first.** Directly answers the "no tests" debt I called non-negotiable |
| **R13** | Fail-closed access + tenant isolation | 8/6/9/8 | **KEEP — keystone.** Answers the `ir.rule` gap |
| **R07** | Gated folio-aware billing, maker-checker | **10**/7/9/8 | **KEEP — keystone, highest-scored.** *No silent charge, ever.* Four-eyes applied to money — the right posture for metered handling |
| **R02** | Point-in-time custody snapshots | 9/6/9/9 | As-sold pinning for custody. Same pattern as Southbrook's spec pinning |
| **R03** | Deterministic effective-dated pricing | 9/7/8/8 | **Rates as data with effective dates** — how a consumption record gets priced |
| **R05** | Single evidence pipeline | 8/8/8/8 | Photo/evidence handling, unified. Feeds the safety record |
| **R06** | Signature-gated release + override | 8/8/8/8 | Custody handover — the `HANDOVER` step in the rail |
| **R08** | Orphan / exception queue | 9/8/8/8 | Where D-008's exceptions land |
| **R15** | **Mobile capture + offline outbox** | 8/**9**/8/7 → REVISED | **Q-30 answered — see below** |
| **R16** | Task orchestration → billing (CE views) | 8/8/8/8 | **Movement → consumption record.** Marshal's core loop |
| **R11** | **Async reconciled QBO** | 9/6/8/**6** → REVISED | **Q-33 answered — QuickBooks Online, one-way for now** |
| **R22** | Liability cap + claims workflow | 9/6/8/8 | GATED on R04. Matters for damaged-crate disputes |
| **R24** | Retention / legal-hold / disposal | 8/6/9/7 | PIPEDA. Policy now, purge gated |
| R23 | PMS / reservation connector | 8/6/7/**5** | **DEFERRED — needs a design partner.** Relevant to Q-15 (hotel elevator calendar) |

**Build order (Porterly v2's, and it transfers):**
Wave 0 enablers (**R25, R13**, `porterly_core` kernel) → Wave 1 custody & access
spine → Wave 2 billing integrity → Wave 3 identity/mobile/visibility → Wave 4
customer & liability.

**That Wave 0 is exactly right for Marshal too** — CI and fail-closed access
before anything else.

---

## Open questions this closes

### Q-30 — is the offline queue real? **Partly. Be precise.**

- ✅ **Shipped and live (2026-07-21):** 3-shot capture (Label · Package · Shelf),
  DRAFT `parcels.tracking` with real `PR###` sequence, **idempotency via
  `capture_uuid`**, geo, captured-by, 90s idle auto-logout, native-camera
  fallback on LAN http
- ⚠️ **A designed v2 recommendation, not built:** R15's **offline outbox**,
  revised for *"phase + device limits"*

**So the `3 queued · syncing` in the mockup is design intent, not shipped
behaviour.** Idempotency is real; the outbox is not. **Q-19 is not answered** —
it remains real work, but with a scored design in hand.

### Q-33 — QuickBooks Online or Desktop? **Online, one-way.**

R11 *"Async reconciled QBO"*, revised to **one-way for now**. Feasibility 6 —
the loop pushed back on bidirectional sync. That matches D-010's boundary
exactly: **Marshal pushes priced consumption out; it does not read books back.**

### A correction I owe on the security finding

I stated *"zero `domain_force`/ir.rule across all 289 modules"* as a live risk.
**Accurate, but I framed it too harshly.** The corpus shows an
**Access-Control Baseline** campaign was run and completed, and the
**2026-07-24 live-`main` audit verifies every IDOR, unauth-sudo and enumeration
oracle is fixed.**

Precisely: **the vulnerabilities were found and remediated at the controller
layer and independently audited.** What still doesn't exist is the **ORM-level
backstop** — that is R13, a designed-but-unbuilt recommendation.

The guidance is unchanged (**declare record rules from module one**), but the
characterisation was unfair to work that was actually done.

### The two "debts" I called non-negotiable were already identified

R25 (testing/CI) and R13 (fail-closed access) are **the linchpin and a keystone**
of Porterly v2 — identified, scored and sequenced first. I flagged them as things
Marshal must not inherit. **They're already the top of someone's backlog.**

---

## What Marshal actually adds

Porterly v2 covers custody, evidence, access, billing integrity, identity and
mobile. **It has no resource layer at all.**

| Layer | Porterly v2 | Marshal |
|---|---|---|
| Thing custody, evidence, pricing, billing | ✅ designed & scored | inherit |
| Access, CI, tenant isolation | ✅ designed & scored | inherit |
| Mobile capture | ✅ **built and live** | inherit |
| **Dock / equipment / elevator scheduling** | ❌ | **build** |
| **Coordinator loop (observe→reconcile→plan→act→verify)** | ❌ | **build** |
| **Wall board** (D-006) | ❌ | **build** |
| **Motion-based automatic actuals** | ❌ | **build** |
| **Safety envelope** — certification, aisle exclusion | ❌ | **build** |

> **Marshal = Porterly v2's exhibitor half + the resource scheduling layer.**

---

## Revised plan impact

`PROJECT_PLAN.md` Phase 1 was *"build the movement record, board, SMS,
actuals."* It becomes:

1. **Adopt Porterly v2 Wave 0** — R25 (CI/migration harness) and R13 (fail-closed
   access) **first**, exactly as sequenced there
2. **Adopt Wave 1** — custody spine with **R04's revised per-parcel hash chain**
3. **Build the resource layer** — the genuinely new work (`08`)
4. **Build the wall board** — the genuinely new surface (D-006)
5. **Defer billing** — R16 produces consumption records; R11's one-way QBO bridge
   is later, per D-010

**The invention is narrower than it looked yesterday.** Most of Phase 1 is
adopting decisions already made and scored by people who knew the constraints.

## New open questions

| # | Question | Why |
|---|---|---|
| **Q-35** | Does Marshal *become* Porterly v2's Wave 0–1, or fork from it? | Two products sharing a kernel vs one diverging. **The most consequential remaining structural question** |
| **Q-36** | Is the `porterly_core` kernel written, or still a design? | It's the Wave-0 foundation both would sit on |
| Q-37 | Does R04's per-parcel hash chain extend to *movements*, not just parcels? | Marshal's defensible record is about movements and equipment, not only custody |
