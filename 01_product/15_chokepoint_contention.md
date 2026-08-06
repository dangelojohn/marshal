# Chokepoint contention — the core scheduling primitive

**Answers Q-46**, the gap all 52 brainstorm candidates walked past: *what happens
when two of Marshal's own movements need the same physical chokepoint at
overlapping times?*

**Why it's the core primitive:** Rule 4 requires a **deterministic, reproducible**
scheduler — *"the model said so"* is not an answer a dock coordinator accepts at
6am. That requirement is meaningless without an explicit, inspectable rule for
who gets the dock bay.

---

## 1. What makes this different from calendar booking

Every off-the-shelf booking system models a resource as *free or busy over an
interval*. That model breaks here in six ways:

| Reality | Why booking software fails |
|---|---|
| **Durations are uncertain** | You don't know how long an unload takes until it's done |
| **Changeover is non-zero** | A truck must pull out before the next pulls in |
| **You can't roll back a crate** | A half-executed movement leaves a physical object in the way. There is no undo |
| **Some claims aren't ours** | Hotel housekeeping takes the elevator without telling us |
| **Exclusion is a safety rule** | Two powered units in one aisle isn't inefficiency, it's a hazard |
| **Chokepoints chain** | dock → aisle → elevator → aisle → booth, and the claims must align |

That third row is the one that drives the whole design.

> **In software, a failed transaction rolls back. In a hall, a stranded crate
> makes everything worse for everyone, for hours.**

---

## 2. The model — chokepoints and buffers

The single most important structural decision: **chokepoints are separated by
buffers**, and buffers have finite capacity.

```
 [DOCK BAY 3]──(apron)──[AISLE A2]──(elev. lobby)──[ELEVATOR]──(upper lobby)──[AISLE C4]──▶ booth
   exclusive    cap 2     exclusive     cap 4        exclusive     cap 4        exclusive
```

**Chokepoint** — exclusive occupancy, capacity 1 (occasionally N). Dock bay,
freight elevator, aisle segment, staging lane.

**Buffer** — a finite holding area between chokepoints. The elevator lobby, the
dock apron, the marshalling yard. **The yard is just the buffer upstream of the
dock bays**, which is why it behaves like a queue.

### ⭐ The blocking rule — the heart of the design

> **A movement may enter a chokepoint only if the *downstream* buffer has space
> for it.**

Never occupy a chokepoint you cannot clear. A forklift that enters the elevator
and then finds the upper lobby full **blocks the elevator for everyone** — and
unlike a software deadlock, you cannot roll it back. You now have a loaded
machine in a shared vertical shaft and a growing queue below.

This is the classic fix for blocking in flow shops, and it is exactly right here.
It also makes the yard behave correctly for free: trucks wait in the yard
*because the apron is full*, not because a timer said so.

---

## 3. Claims and their lifecycle

A movement acquires a `marshal.claim` per chokepoint in its chain.

```
 PROPOSED ──▶ CLAIMED ──▶ HELD ──▶ OCCUPIED ──▶ RELEASED
     │            │          │          │
     │            │          │          └─▶ physically in it. NOT preemptible
     │            │          └─▶ next in line, downstream buffer confirmed
     │            └─▶ scheduled. Preemptible
     └─▶ candidate. Freely reordered
                  │
                  └──▶ YIELDED ──▶ back to PROPOSED, or to the dead-letter queue
```

### The preemption rule

> **Claims are preemptible. Occupancy never is.**

A movement that is *scheduled* for the elevator at 14:20 can lose that slot to
something more urgent. A forklift that is *in* the elevator cannot — that would
be physically absurd and dangerous.

Clean, defensible, and it maps to a line a person can see.

---

## 4. The comparator — how contention is resolved

Deterministic and explainable, evaluated **in order until one discriminates**.
Configuration as data, not code branches.

| # | Test | Rationale |
|---|---|---|
| **1** | **Hard external deadline** | A slot on a calendar we don't own (H1), or show-open. Miss it and it's gone |
| **2** | **Blocking / safety** | A movement whose delay leaves a crate in a fire lane or an aisle blocked. **Clearing an obstruction outranks starting new work** |
| **3** | **Precedence depth** | How many other movements are waiting on this one — the critical path |
| **4** | **Priority class** | expedite · normal · opportunistic. Set by a human, per movement type |
| **5** | **Earliest due** | Classic EDD, matching the OdooIQ solver |
| **6** | **Least slack** | Time to due, minus remaining work |
| **7** | **Claim sequence number** | **The final total-order tie-break** |

**Row 7 is not optional.** Without a guaranteed final discriminator the scheduler
is not reproducible — two runs on identical data could differ, and rule 4 is
broken. A monotonic claim sequence guarantees a total order in every case.

**Every comparison records which rule decided it.** That's what makes the answer
explainable rather than oracular:

> *"Movement 482 yielded the elevator to 517 — rule 1, hard external deadline
> (hall opens 09:00)."*

The LLM may render that sentence more warmly (D-009). **It never computes it.**

---

## 5. Overrun — a chokepoint is never released by a timer

A claim carries `[start, expected_end]`, where `expected_end` uses a **p90**
duration from calibration (`spec/03`), not a median. Optimistic estimates on a
chokepoint propagate delay to everything behind them.

**When actual runs past expected:**

- The resource is **NOT** auto-released
- The next claim in line is notified — *"elevator running long, +6 min"*
- The overrun surfaces as schedule drift (shortlist A4)
- Occupancy ends **only** by explicit release or human decision

> **This is the same lesson as the aisle-clearance candidate (shortlist #3):
> propose, never auto-release.** A timer that frees a physical chokepoint while
> something is still in it causes a collision. The system's model of the world is
> not the world (D-008) — and a chokepoint is exactly where that gap hurts.

---

## 6. Foreign claims — the elevator we don't own

The hotel freight elevator is shared with housekeeping, F&B and engineering
(Q-15). Marshal polls its availability through an `avn.capability` (H1) and
caches it.

**A claim on a foreign chokepoint is advisory, not authoritative.**

- Marshal may *believe* the elevator is free at 14:20
- On arrival it may be occupied by someone who never told us
- That is a **contention event**, not an error: it lands in the dead-letter queue
  (shortlist #4) with reason `foreign_occupancy`, and the movement is re-planned

**Do not build retry logic that hammers a foreign resource.** Record the
collision, re-plan, and let the accumulating record of `foreign_occupancy` events
become the evidence for a conversation with the hotel about a reserved window.
**The data is the argument.**

---

## 7. Deadlock

Movement A holds aisle A2 waiting for the elevator; movement B holds the elevator
waiting for A2. Classic, and physically nasty.

**Prevented by two rules together, not one:**

1. **Ordered acquisition** — chokepoints carry a global integer rank and are
   always claimed in ascending order. A cycle cannot form.
2. **The blocking rule (§2)** — you cannot enter without downstream space, so a
   movement can always drain forward.

**Deliberately rejected: whole-chain atomic acquisition.** Requiring every
chokepoint in the chain to be free before starting sounds safer and is worse in
practice — on a long chain nothing ever starts, and it contradicts how a floor
really runs. A mover *does* leave the dock before the elevator is free; they
queue in the lobby. **The lobby buffer is the mechanism that makes partial
progress safe**, which is why buffers are first-class rather than incidental.

---

## 8. Odoo 16 CE implementation

Everything below uses modules verified present (`03_internal_assets/06`).

| Model | Purpose |
|---|---|
| `marshal.chokepoint` | `resource_id` → `resource.resource`, `capacity`, `changeover_minutes`, `rank` (deadlock ordering), `is_foreign`, `capability_id` |
| `marshal.buffer` | `capacity`, `upstream_ids`, `downstream_ids`, computed `occupancy` |
| `marshal.claim` | `movement_id`, `chokepoint_id`, `start`, `expected_end`, `state`, `priority_class`, `sequence` (monotonic) |
| `marshal.contention` | Immutable log: the two claims, **the deciding rule number**, the rendered reason |

**Concurrency is the part to get right.** Two claims racing for one chokepoint
must serialise. Use the pattern already proven in Southbrook's ECO approval:

```
SELECT ... FOR UPDATE   →   invalidate_recordset()   →   re-read   →   decide
```

That closed a real double-approval race there. **The same shape closes
double-claim here** — and it is a known-good pattern in this stack rather than
something invented for this design.

`resource.calendar` supplies *availability* (when a dock is staffed, when the
elevator is blacked out). **The claim layer sits above it** and handles
contention *within* available time. Two different questions, deliberately kept in
two different places.

**Contention resolution runs synchronously** in the claim transaction — never in
`queue_job`. A movement must know immediately whether it holds the elevator. Only
notification and re-planning are async.

---

## 9. What this deliberately does not do

- **No optimisation.** It resolves *contention*, it does not minimise makespan.
  Sequencing optimisation is Phase 2 and sits above this
- **No prediction.** p90 durations come from calibration; this layer consumes them
- **No automatic foreign booking.** Marshal never writes to a calendar it doesn't
  own
- **No preemption of occupancy.** Ever
- **No timer-based release.** Ever

---

## 10. Why this is buildable now

It needs no telemetry, no ML, no object detection, and no distributed lock — the
four things that killed candidates in D-013. It is a state machine, an ordered
comparator, and a row lock, over models that already exist.

**It also makes three shortlist survivors materially more useful:** the
dead-letter queue gets its most important producer, idempotency keys protect
claim creation from double-submit, and offline replay has a clear rule — *a
claim made offline is `PROPOSED`, never `HELD`.*

## Open questions

| # | Question | Why |
|---|---|---|
| **Q-49** | What are the real buffer capacities — apron, elevator lobby, yard? | **The blocking rule is only as good as these numbers.** Measure at the design partner; do not guess |
| **Q-50** | Is `changeover_minutes` per chokepoint enough, or is it pair-dependent? | Truck-to-truck at a bay may differ from forklift-to-forklift in an aisle |
| Q-51 | Who sets `priority_class`, and can a show manager escalate their own freight? | If everyone can self-declare expedite, rule 4 of the comparator is worthless |
| Q-52 | Do aisle segments need directionality (one-way during move-in)? | Common on a real floor, and it changes the topology from a graph to a digraph |
