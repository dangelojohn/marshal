# Brainstorm synthesis — 2026-08-06

**Method:** four low-cost generators (efficiency · employee scheduling ·
automation · headless) produced **52 candidates**. I filtered to a 24-candidate
shortlist, correcting several errors on the way. One adversarial breaker then
attacked all 24 with a **hard FZ<7 auto-kill** on Odoo 16 CE feasibility, plus
kill authority for violating any decided rule.

**Result: 8 clean survivors, 6 more that clear the bar below them, 4 dead.**

---

# 🔴 The breaker killed two mechanisms I had already decided. Both kills are right.

## D-006 was wrong about motion detection

I wrote: *"motion with nothing scheduled is a safety exception."* That was in the
decision log as a feature.

**It doesn't work.** A working convention dock has constant incidental motion —
staff walking through, non-Marshal equipment, doors, HVAC-driven curtains. The
exception queue fires continuously and the coordinator stops reading it inside a
week. **Narrowing the scope doesn't save it**: even a single chokepoint door has
legitimate foot traffic in an active venue.

Separating safety-relevant motion from ordinary workplace motion requires
classifying **what** moved — object detection the Reolink client explicitly does
not provide.

> ### The asymmetry I missed
> **Motion state is useful as *corroboration*, not as *detection*.**
>
> *"Did the movement we scheduled for 14:20 at dock 4 actually happen?"* — a good
> question for a boolean motion signal, because it's checked inside a known
> window.
>
> *"Is something happening that shouldn't be?"* — a bad question, because the
> null hypothesis on a live dock is *there is always motion*.

**Everything D-006 claims about motion as automatic actuals capture still
stands.** Only the unscheduled-activity detector dies. Q-11's test is unchanged.

## D-008 overclaimed on network failure

I wrote: *"kill the wall board and the facility still runs, degraded not
stopped."* True for **screens**. **Not true for Odoo**, and I let the phrasing
blur the two.

The proposed fix — an edge ledger doing autonomous dispatch for 1–2 hours — is
**dead**, for three reasons that don't have small-team answers:

1. **Cross-box double-booking.** SQLite is dock-local. During an outage, two edge
   boxes cannot negotiate ownership of a shared forklift or operator. That's not
   a tuning problem, it's **the absence of a distributed lock** — exactly the
   deep-pit distributed-systems work a small team must not sign up for.
2. **Stale safety gates.** A decertification issued at minute 5, or a fatigue
   threshold crossed at minute 40, never reaches the edge. It keeps dispatching
   against data it can no longer trust — **the safety story silently becomes
   non-deterministic exactly when it matters most.**
3. **Reconciliation has no good answer.** *"Coordinator cancelled movement #482 at
   14:02; the offline edge marked it complete at 14:05 on stale state."* Whoever
   writes that auto-merge rule is **quietly authoring a second, hidden scheduler**
   that nobody budgeted for and that can't be tested with the rigour the primary
   one gets.

### The honest claim, which is the one to make

> **When the network drops: already-assigned work continues and is recorded. No
> new assignments are made. Everything recorded offline is reviewed on
> reconnect.**

That is defensible, buildable, and answers **Q-19** properly. It's also just
candidate A6 running on local hardware — see the heuristic below.

---

# ⭐ The gap all 52 candidates missed

> **Nothing addresses two of Marshal's *own* movements needing the same physical
> chokepoint at overlapping times.**

E3 handles voluntary batching. H1 handles one *foreign* calendar (the hotel's
elevator). **But the ordinary case — two scheduled movements both needing dock
bay 3, or the freight elevator, or a staging lane — has no mechanism at all.**

In a convention centre the dock bay and the freight elevator are **at least as
often the bottleneck as the vehicle or the operator.** And a "deterministic,
reproducible scheduler" is meaningless without an explicit booking and locking
rule for the chokepoints themselves.

**This is the most important thing to come out of the exercise**, and it came
from the adversary rather than from any of the four generators. It is arguably
*the* core scheduling primitive, and 52 candidates walked past it.

→ **Q-46: chokepoint contention. Design it before anything else in Phase 2.**

*(Runner-up gap the breaker named — "nothing describes what the coordinator at
6am actually looks at" — is a false positive. That's the wall board, D-006. It
wasn't in the agents' briefing, so they couldn't see it. My prompt's fault, not a
real hole.)*

---

# 🔑 A review heuristic worth keeping

**Twice in one round, two candidates turned out to be the same mechanism at
different intensities — one safe, one not.**

| Safe | Dangerous | The difference |
|---|---|---|
| **P2** shift handover — attest, accept custody | **SHCC** handover + GPS + hash chain | GPS on the person, and framing operators as suspected thieves |
| **A6** offline replay of known facts | **H2** edge ledger that keeps *dispatching* | Making **new decisions** while cut off from safety-gate data |

> **The fix in both cases was "stop being the dangerous version of the safe one."**

That generalises: when a candidate feels valuable but uncomfortable, look for the
weaker sibling that keeps the value and drops the exposure. **It usually exists,
and it's usually already in the same list.**

---

# The shortlist — FZ ≥ 8, no rule violations, ship as specified

| # | Mechanism | FZ | Why it's here |
|---|---|---|---|
| **1** | **Idempotency keys, server-side dedup** | **10** | Foundational plumbing every other mechanism leans on. Clients can be dumb and fire-and-forget |
| **2** | **Certification-first refuse** — assignment *refuses*, never warns | **9** | Highest safety value per line of code in the entire set |
| **3** | **Aisle clearance: propose + human confirm, never auto-release** | **9** | Best-designed automation in the set. Human gate baked in; uses exactly the boolean motion we have; a camera blind spot is mitigated rather than fatal |
| **4** | **Dead-letter queue** — no unschedulable movement fails silently | **9** | The observability backbone everything else needs. A blocked movement is visible and actionable, never hidden |
| **5** | **Failed checkpoint → `maintenance.request` + out-of-service** | **9** | Clean `quality_control_oca` → `maintenance` trigger. Both modules confirmed present |
| **6** | **Activity-based skill decay** | **9** | A pump-truck operator who hasn't touched one in 9 months is dangerous, and date-based expiry misses it entirely |
| **7** | **Breaks as scheduled capacity-off-the-board** | **9** | Nearly free — correct use of native `resource.calendar.attendance` |
| **8** | **Offline replay with a staleness cutoff** | **8** | **Ship this instead of the edge ledger.** Bounded to replaying known facts; anything stale routes to a human |

## Clears the bar, ranked below

**E5** operator-first assignment (8) · **P2** shift handover custody (8) ·
**P5** absence backfill with first-accept-wins locking (8) · **E3** dock
consolidation window (7, needs a "do not batch" flag for anything with a hard
external deadline) · **H1** foreign calendar with manual fallback (7 — *the value
is the structured fallback, not the polling; most hotel elevator "calendars" are
a sign-up sheet*) · **P3** fatigue limits (7 — **flagged: legal exposure means a
bug here is a compliance incident, not a UX bug. Budget disproportionate test
effort**)

## Dead

| Killed | FZ | Why |
|---|---|---|
| **A2** unscheduled-motion safety exception | 5 | Alert fatigue. Needs object classification we don't have |
| **A5** battery auto-gating | 4 | **No telemetry source exists in the verified stack.** Blocked on Q-22 |
| **H2** edge ledger with autonomous dispatch | 5 | Distributed lock + stale safety gates + unsolvable reconciliation |
| **H7** YAML admin, no Odoo admin UI | 4 | Contradicts the premise — everything else treats Odoo as the single system of record. A second config surface drifts and loses `ir.rule` and audit for free |

**The pattern across all four kills:** each reaches for a capability, sensor or
surface **that was never verified to exist.** Object classification, equipment
telemetry, safe distributed offline authority, a reason to bypass Odoo's admin.

---

# Two hidden rule violations the breaker caught

**A4 schedule drift — the sharpest catch in the review.** As worded it never says
*how* "actual" timing is captured. The only compliant source is the two watch
taps. **If anyone implements it via continuous location polling to infer arrival,
it silently becomes per-operator tracking dressed up as an equipment metric** —
and the framing ("schedule drift") sounds like it's about freight, not people,
which is exactly why it would pass review.

→ **Hard-code into the spec: `actual = tap timestamp, never a GPS breadcrumb`.**

**P3 fatigue limits — safe now, highest future temptation.** Built on
`hr_attendance` clock events, it's disclosed consented timeclock data. But
someone will eventually propose improving accuracy with *"is the operator
actually present at the dock right now"* via continuous presence detection.
**Flag it now so that arrives as a policy violation rather than a feature idea.**

**Compliance footnote:** the dock cameras record a workspace people move through.
Even reporting only zone-level boolean motion with no identification, **Ontario's
electronic-monitoring disclosure obligation likely still attaches.** Not a
rule-1 violation — a disclosure requirement. → Q-47.

---

# One technical correction

**"Stripe PULL" is not a real Stripe pattern.** Stripe has no mechanism to poll a
third-party feed for invoice lines; you push to Stripe, or Stripe webhooks push
to you. QuickBooks is more pull-friendly but still typically needs a connector.

**Fix without changing the principle:** a thin external connector — plausibly a
thirty-line cron job — pulls from Marshal's consumption feed and pushes into
Stripe/QBO via their own APIs. **Marshal itself still never pushes an invoice**,
which is all D-010 ever required.

---

# What this changes in the plan

`PROJECT_PLAN.md` Phase 1 was *"movement record, board, SMS, actuals."* The
shortlist sharpens it:

**Wave 0 (with R25 + R13 from Porterly v2):** idempotency keys (#1), dead-letter
queue (#4). Both are plumbing everything else assumes.

**Wave 1:** certification-first refuse (#2), checkpoint → maintenance (#5),
breaks as capacity (#7), offline replay (#8).

**Before Phase 2 starts:** design **chokepoint contention** (Q-46). It's the core
scheduling primitive and it currently doesn't exist.

**Explicitly not building:** unscheduled-motion detection, battery gating (until
Q-22 answers whether telematics exist), autonomous offline dispatch, YAML admin.

## New open questions

| # | Question | Why |
|---|---|---|
| **Q-46** | **How do two of our own movements contend for the same dock bay / elevator / staging lane?** | **The missing core primitive.** Design before Phase 2 |
| **Q-47** | Does Ontario's electronic-monitoring disclosure apply to zone-level dock cameras? | Likely yes. Cheap to disclose, expensive to retrofit |
| Q-48 | Should `web_form` stay in the capability maturity ladder? | Browser scrapers against bespoke venue portals are a real ongoing burden. **Ship the 2-rung `api → human queue` version by default** |
