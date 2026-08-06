# Headless per-facility infrastructure — the architecture

**Source:** John D'Angelo, 2026-08-06 `[PRIMARY]`

> *"I would not run it. It should be an infrastructure tool per facility that is
> headless and auto-coordinates and has some few humans in the loop and checks
> and balances — such as the condition of equipment and fuel, and if the
> equipment was returned to the right position."*

**This resolves the A/B fork in `PROJECT_PLAN.md`, and the answer is neither.**
Not a SaaS product sold broadly, not a services business we operate. A **third
shape**: infrastructure installed at a facility, running on its own, with humans
appearing only where physical reality has to be confirmed.

---

## Why this is a better answer than either branch

| | A · Product | B · We operate it | **C · Per-facility infrastructure** |
|---|---|---|---|
| Multi-tenancy | Required — expensive | N/A | **Not required. Single tenant per install** |
| Our staffing | Sales + support | **Heavy ops** | **Light** |
| UI surface | Large, polished, self-serve | Internal-grade | **Small — it's headless** |
| Failure mode | Churn | Doesn't scale | **A facility outgrows it** |
| Odoo fit | Awkward | Good | **Excellent** |

Dropping multi-tenancy removes the single largest source of complexity in a
scheduling product — no cross-tenant isolation, no shared-resource contention, no
per-tenant configuration sprawl. **Each install knows about exactly one building**,
which is also the only scope in which the physics makes sense.

---

## What "headless" actually means here

**The scheduler is the product. Every screen is a client of it.**

```
                    ┌───────────────────────────────┐
                    │      MARSHAL CORE (Odoo)      │
                    │                               │
                    │   movements · resources       │
                    │   coordinator loop            │
                    │   checkpoints · ledger        │
                    └───────────────┬───────────────┘
                                    │  REST / GraphQL
        ┌───────────────┬───────────┴────┬──────────────┐
        │               │                │              │
   wall board       SMS gateway      handheld      facility systems
   (cameras +       (drivers,        (checkpoint    (elevator calendar,
    schedule)        vendors)         confirm)       billing, PMS)
```

Consequences that matter:

- **No screen is load-bearing.** Kill the wall board and the facility still runs —
  degraded, not stopped. That is what makes it *infrastructure* rather than an app
- **New surfaces are cheap.** A handheld, a driver display in the yard, a
  read-only view for the show manager — all clients, no core change
- **It integrates by default**, because the API is the primary interface rather
  than an afterthought bolted on later

**We already own the API layer:** `base_rest` + `component` (LGPL-3, OCA) and
`odoo_graphql` (LGPL-3), both found in edata+ (`03_internal_assets/03`). Take
current upstream, not the v15 copies.

---

## Auto-coordination: the loop

Marshal runs continuously rather than waiting to be asked.

```
   observe  →  reconcile  →  plan  →  act  →  verify
      ↑                                          │
      └──────────────────────────────────────────┘
```

| Step | What happens | Human? |
|---|---|---|
| **Observe** | Truck arrivals, motion state (D-006), checkpoint results, SMS replies | No |
| **Reconcile** | Update the model of where everything actually is | No |
| **Plan** | Re-sequence remaining movements under all constraints (`08`) | No |
| **Act** | Assign equipment + operator, SMS the driver, call the next truck | No |
| **Verify** | Checkpoint at the points where reality must be confirmed | **Yes — here only** |

**"Auto-coordinates" means the default path has no human in it.** A person is
interrupted when the physical world needs a witness, or when the plan needs a
judgement the system shouldn't make alone.

---

## Checks and balances: humans as sensors, not operators

This is the sharpest idea in the brief and worth stating plainly.

> **The system's model of the world drifts from the world. Humans are how it
> gets re-anchored.**

A forklift is "at door 4" because Marshal believes it is. In reality it's out of
fuel behind a crate, two aisles over. Every autonomous coordinator has this
problem, and the ones that fail are the ones that assume their model is true.

So checkpoints aren't bureaucracy — **they are the sensor network**, and they map
exactly onto what the brief named:

| Checkpoint | Trigger | Re-anchors | Also gives you |
|---|---|---|---|
| **Equipment condition** | Shift start, after incident | Is this unit usable? | Maintenance trigger, safety record |
| **Fuel / charge level** | Shift start, periodic | How much runtime is left? | **Prevents the hour-8 plan collapse** (`08` §4) |
| **Returned to position** | Movement complete, shift end | **Where is it actually?** | The next plan is built on truth |
| Operator certification | Assignment | Is this person permitted? | Compliance record (D-005) |

**Two sensor classes, and they cover each other:**

- **Automatic** — camera motion state (D-006). Free, continuous, low fidelity
- **Human** — checkpoints. Costly, occasional, high fidelity

Motion tells you *something happened at door 4*. A checkpoint tells you *forklift
3 has 20% charge and is parked in bay B*. Use the cheap sensor constantly and the
expensive one sparingly, at the moments where being wrong is expensive.

**The engine for this already exists and is free:** `quality_control_oca`
(AGPL-3, OCA) — defined tests, defined triggers, pass/fail criteria, recorded
result and inspector. That is the checkpoint pattern, generically. Found in
edata+; take the current upstream version.

---

## Where the humans are — the whole list

Being explicit, because "few humans in the loop" is a design constraint that
silently erodes unless it's written down.

| Role | Touches Marshal | How often |
|---|---|---|
| **Dock coordinator** | Watches the board. Overrides when the system is wrong | Continuous, passive |
| **Equipment operator** | Confirms checkpoints on a handheld | ~4–6 taps per shift |
| **Ops manager** | Approves exceptions; reviews the day | A few times per show |
| **Show manager** | Read-only visibility | Rarely |
| Driver / vendor | **SMS only. Never logs in** | Per arrival |

**Nobody's job is "operate Marshal."** If a role appears whose day is spent
inside the system, the design has failed.

---

## What this does to the plan

`PROJECT_PLAN.md` stands — `Record → Coordinate → Schedule → Meter → Predict` is
unchanged, and **Phase 1 gets easier**:

- **No multi-tenant work.** Ever, possibly
- **API-first from day one**, using `base_rest` rather than hand-rolled controllers
- **Checkpoints ship in Phase 1**, not later — they're how actuals get captured
  when motion detection can't see it, which is also the Q-11 fallback
- **The wall board is one client**, which caps how much UI Phase 1 needs

**Odoo is now clearly right**, resolving Q-3. Single-tenant, per-facility,
record-heavy, with native `maintenance` and `fleet` covering equipment condition
and fuel logs, and `quality_control_oca` covering checkpoints. Very little of the
equipment layer is custom work.

---

## New open questions

| # | Question | Why |
|---|---|---|
| **Q-18** | Where does Marshal run — facility hardware, or our cloud with a local agent? | "Infrastructure per facility" implies on-prem; Law 25 and hotel IT policy may require it |
| **Q-19** | What happens when the network drops mid-move-in? | Infrastructure must degrade gracefully. **A dock cannot stop because a WAN link did** |
| **Q-20** | Handheld: operator's own phone, or facility-provided device? | Decides whether checkpoints are a web app or a native one |
| **Q-21** | Who administers an install — facility IT, or us remotely? | Determines the support model and the update path |
