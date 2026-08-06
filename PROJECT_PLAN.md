# Marshal — project plan

**Rev 2 · 2026-08-06.** Supersedes rev 1 (same day), which predated the resource
model, the headless decision, the Porterly Design corpus, the scored brainstorm,
the chokepoint design, and the business model.

---

## What Marshal is

> **Per-facility headless infrastructure that schedules and meters the safe
> movement of freight from dock to booth — coordinating carriers by SMS,
> controlling powered equipment in shared space, and producing a defensible
> record of both.**

Odoo 16 CE, single-tenant, one install per facility. Canada first, hotels likely
before convention centres.

## The sequence

> **Record → Coordinate → Schedule → Meter → Predict.** Deliberately not
> schedule-first.

We have no duration data, so an optimiser would be confidently wrong and burn
credibility we get once. The safety record and the metering are the strongest
parts of the case and **neither needs an optimiser**. And every movement recorded
is a calibration sample: Phase 1 is what makes Phase 2 possible.

**Marshal earns trust as a system of record before it becomes a system of
decision.**

---

# 🔴 Phase 0 — three phone calls, before any capital commitment

**The financial model (`01_product/17`) puts breakeven between 4 and 37 venues.**
That 9× spread is driven by two numbers nobody has asked for. **You cannot commit
capital against it, and three calls collapse it.**

| # | Question | Ask | Why it dominates |
|---|---|---|---|
| **Q-58** | **Who absorbs the cost of a truck waiting today?** | A carrier | **Binary.** If detention bills through to the exhibitor, they'll pay to avoid it and the model works. If it's absorbed invisibly, Marshal is a new fee for something previously free and **adoption fails regardless of software quality** |
| **Q-53** | What would an exhibitor pay for a guaranteed dock slot? | An exhibitor / show manager | Dominant revenue lever |
| **Q-55** | How many vehicles book in per show, and what fraction miss their slot? | A venue ops director | Equally dominant; also sizes the enforcement thesis |

**Also in Phase 0, all cheap:**

- **Q-1′ / Q-56** — who holds the handling margin, and does the venue's contract
  with organisers permit third-party exhibitor charges? **This gates whether the
  business model is permitted at all** (D-015 Problem 3)
- **Q-11** — run the Reolink motion harness (`tools/`) on LAN cameras, then one
  real dock. **Already built**
- **Q-22** — do the venue's forklifts have telematics? May answer condition and
  fuel with zero new hardware
- **Q-60** — will an insurer discount a premium against the safety record?
  A broker conversation. **If yes, it's the strongest adoption lever in the product**

**Exit gate:** one named design partner, Q-58 answered, and the breakeven range
narrowed enough to justify what comes next.

---

# Phase 1 — record and coordinate

**One venue, one hall, one real move-in. Marshal records and coordinates; it does
not decide.**

## Wave 0 — enablers, ship first

Adopted from Porterly v2, which sequenced these first for the same reasons
(D-011):

| Item | Source | Why first |
|---|---|---|
| **R25** testing / CI / migration harness | Porterly v2 linchpin | Everything downstream assumes it |
| **R13** fail-closed access + `ir.rule` from module one | Porterly v2 keystone | **Porterly has zero `domain_force` across 289 modules.** Marshal has four parties on different slices — one mis-coded domain is a full leak |
| **Idempotency keys**, server-side dedup | Brainstorm #1, FZ 10 | Foundational plumbing; lets clients be dumb and fire-and-forget |
| **Dead-letter queue** | Brainstorm #4, FZ 9 | No movement ever fails silently. The observability backbone |

## Wave 1 — the spine

- **The movement record** — crate, from dock, to booth, equipment, operator,
  elevator leg. **Planned and actual, plus a coded variance reason**
- **Chokepoint contention** (D-014) — chokepoints, buffers, the blocking rule,
  the seven-test comparator, the immutable contention log. **Build this in
  Phase 1, not Phase 2** — it is what makes the schedule real, and it is also the
  evidence engine for penalty waivers (D-015)
- **R04 tamper-evident custody log** — Porterly v2's **revised** mechanism:
  per-parcel hash chain plus periodic anchor, **not** a global chain
- **Certification-first refuse** (#2, FZ 9) — assignment *refuses*, never warns
- **Checkpoint → `maintenance.request`** (#5, FZ 9) — `quality_control_oca`
  triggers native `maintenance`
- **Breaks as scheduled capacity** (#7, FZ 9) — native `resource.calendar`
- **Activity-based skill decay** (#6, FZ 9)
- **Offline replay with a staleness cutoff** (#8, FZ 8)

## Wave 2 — the surfaces

| Surface | State |
|---|---|
| Receiver — iPhone capture | ✅ **Porterly Inbound PWA, live.** Adopt |
| Exhibitor portal | ✅ **Porterly Outbound PWA, live.** Adopt |
| **Manager — wall board** | ❌ New. Camera tiles + schedule state, snapshot refresh not streaming |
| **Runner — Apple Watch Ultra** | ❌ New. One job, two taps, **physical Action Button** because gloves |
| **Equipment-bay tablet** | ❌ New. Checkpoints are location-bound, not person-bound (Q-42) |
| Driver SMS | ❌ Designed, not built |

**Aisle clearance: propose + human confirm, never auto-release** (#3, FZ 9).

## Explicitly NOT in Phase 1

The optimiser · predictive anything · billing · multi-tenant · the Show Board ·
**unscheduled-motion detection** (killed, D-013) · **battery auto-gating**
(no telemetry exists — blocked on Q-22) · **autonomous offline dispatch**
(killed) · YAML admin (killed).

## Exit gate — three tests, honestly measured

1. Ops ran a real move-in on it and asked to keep it
2. ≥80% of movements carry usable actuals
3. **One incident or dispute where the record answered a question nothing else
   could**

**Test 3 is the real one.** It is binary, and it proves the safety-and-evidence
thesis that both the insurance argument and the penalty-waiver mechanism depend on.

---

# Phase 2 — the scheduler

**Only once Phase 1 has produced real durations.**

Port the OdooIQ solver, re-pointing `(workcenter, day)` at `(resource_unit, day)`
— specific forklifts, elevators, named operators, aisle segments. Then add, in
the order they cost most to omit:

1. Travel / repositioning for mobile resources — omit it and every plan is
   optimistic by a constant
2. Precedence within a movement
3. Capability matching with **directional** substitution
4. Charge windows for electric units
5. Foreign-calendar blackouts (H1, `avn.capability`)

**Evaluate `frepple` (AGPL-3, in edata+) against the OdooIQ solver before
committing** — a real comparison, not a dismissal.

**Agent proposes, human commits.** The solver produces the feasible set; the
agent ranks and explains; a person accepts. **The schedule appears on the tiles,
not in a new screen to learn.**

---

# Phase 3 — meter

Phase 1's actuals become **priced consumption records** in whatever unit Q-8 says
the market already uses.

```
Marshal ──▶ priced consumption records ──▶ QuickBooks · Stripe
(meter)                                    (tax, invoice, collection)
```

**Marshal never pushes an invoice.** A thin connector pulls from the feed and
pushes into QuickBooks Online (one-way, per R11) and Stripe via their own APIs —
correcting the earlier "Stripe pulls" error, without changing the principle.

**The dock fee layer** (D-015) sits here: Stripe Connect with the **venue as the
connected account**, so Marshal never holds funds. **Penalties carry zero
margin**, and the contention log auto-waives when the venue caused the delay.

---

# Phase 4 — predict · Phase 5 — the Show Board

Forecast the **inbound freight arrival curve** — CWT by day, hour, dock. Not head
count, not floor area; demand explodes from **booth mix** via a bill of services.

Then the capacity network, **gated on counsel rather than engineering** (Q-4) —
competing venues seeing each other's availability is antitrust-sensitive.

---

# The commercial model

**5% of the dock fee, processing passed through, venue as merchant.**

| | |
|---|---|
| Exhibitor | Pays the fee. Gets a guaranteed slot instead of a queue |
| **Facility** | One-time **$22K** implementation + hardware at cost+12%. **No subscription.** Keeps the fee revenue |
| Show manager | **Free.** Floor visibility |
| **Service contractor** | **Free forever, read-only feed.** Predictable arrivals, scope-change warning, dispute evidence |

**Qualification rule: a venue must generate ≈$800K+ annual dock-fee volume.**
One line, applied before spending a week on a prospect.

**The line that makes contractor adoption possible:** *Marshal prices dock time.
Contractors price handling. Zero overlap.* Marshal must never price material
handling, drayage, or anything a contractor sells.

Full math: `01_product/17_financial_model.md`.

---

# What we own

| Asset | State | Use |
|---|---|---|
| Porterly Inbound/Outbound PWA | ✅ **Live, v16** | Receiver + exhibitor surfaces |
| `courier_tracking` + `event_extend` | ✅ v16 | Custody, booth/exhibitor structures |
| Porterly v2's 26 scored recommendations | ✅ Feasibility-vetoed on 16 CE | **The backlog** |
| `quality_control_oca` | AGPL-3 | Checkpoint engine. **Odoo 16 CE has no `quality`** — critical path |
| `base_rest` + `component` | LGPL-3 | The headless API |
| Reolink client | ✅ Working, pushed | Motion + snapshots. **No streaming** |
| `avn.capability` | ✅ Verified | Connector ladder; foreign calendars |
| OdooIQ solver | ✅ Verified | Phase 2 base |
| `frepple` | AGPL-3 | Phase 2 alternative to evaluate |
| `porterly-future-reference` | 74 invariant tests | **Read before designing the agent boundary** |
| Native `maintenance` + `fleet` | ✅ In CE | Equipment condition and fuel — near-free |

---

# Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| **Exhibitors won't pay** (Q-58) | **Critical** | **Answer before building payment.** If detention isn't already their cost, the model fails |
| **Venue contract forbids exhibitor charges** (Q-56) | **Critical** | Gates the model. Metering is correct under every outcome — build that |
| Breakeven spans 4–37 venues | **High** | Three phone calls collapse the range |
| Ops won't adopt a new surface mid-show | High | The board *is* the camera wall they already watch. **Never make them type during move-in** |
| Metering unit doesn't match existing billing (Q-8) | High | Blocks Phase 3 |
| Chokepoint buffer capacities guessed (Q-49) | Medium | **The blocking rule is only as good as those numbers.** Measure at the partner |
| Odoo 16 EOL — patches are ours (D-010) | Medium | Budget it. A v19 move later is a project, not an upgrade |
| Scope creep to the full platform | High | `spec/01` is the destination, not the plan. **Phases 1–3 only** |
| Building the optimiser first | High | This document. Record before decide |

---

# Next actions

1. **Make the three Phase-0 calls.** Q-58 first — it's binary and one call
2. **Run the Q-11 motion harness** on LAN cameras, then a real dock. Built, ready
3. **Ask a broker about Q-60** — insurance discount against the safety record
4. **Name a design partner** — likely a Toronto hotel
5. **Then, and only then, Wave 0**

**Nothing is built yet, and that remains correct.** The financial model says the
risk here is commercial, not operational — cost discipline barely moves breakeven
while revenue assumptions move it threefold. **Spend accordingly.**
