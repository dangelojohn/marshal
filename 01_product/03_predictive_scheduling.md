# Agentic predictive scheduling — does the manufacturing analogy hold?

**Question (owner, 2026-08-06):** *"Should we consider agentic predictive
schedulers in this project, as they have in manufacturing, where we consider show
head count or rented floor space the 'Demand'?"*

**Short answer: yes — the analogy is real and it is the strongest technical idea
in this project. But the demand unit in the question is wrong, and getting it
wrong would build the model against the weakest signal available.**

---

## 1. The correction first: head count is nearly irrelevant, and sq ft is incomplete

The instinct to find a demand primitive is exactly right. The candidates rank
very differently once you follow what each one actually drives.

| Candidate demand unit | Drives | Cost weight | Constrains move-in? |
|---|---|---|---|
| **Attendee head count** | cleaning, security, HVAC, registration, shuttle, concessions | Low, roughly linear | **No** |
| **Rented floor space (sq ft)** | a rough proxy for everything | Medium | Partially |
| **Booth mix** (count × type × size) | electrical, rigging, furniture, labour hours | **High** | **Yes** |
| **Inbound freight weight (CWT) and its arrival curve** | dock doors, forklifts, crews, marshalling yard | **Highest** | **Yes — it *is* the bottleneck** |

Two things fall out of this.

**Head count drives show-hours services, not move-in.** The capacity crunch in
exposition services is move-in and move-out, not show days. Head count barely
touches that window. It is a real demand signal for a small, linear, low-margin
slice — worth modelling eventually, worth nothing as the primary driver.

**Sq ft hides the variable that matters.** A 20×20 island and four 10×10 inlines
are both 400 sq ft. The island needs a hanging sign (rigging — the highest-margin,
most-constrained service), typically more power, often a multi-level structure,
and its own dedicated setup crew. The four inlines need almost none of that.
**Sq ft with no booth-type breakdown makes those identical to the model.** They
are not remotely identical to the floor.

So: **booth mix is the demand primitive, and freight weight is what it explodes
into.** Head count is a secondary, separately-modelled driver for show-hours
services.

---

## 2. Where the manufacturing analogy genuinely holds

Stronger than it first appears. This *is* MRP:

- **Independent demand → dependent demand.** Space sold is the independent
  demand. Electrical drops, rigging points, drayage weight, labour hours and
  dock slots are dependent demand, derived through what is functionally a **bill
  of services per booth type**. That is a BOM explosion in everything but name.
- **Finite, time-phased capacity.** Dock doors, forklifts, freight elevators,
  crews and aisle access are workcenters with calendars. Finite-capacity
  scheduling is the correct frame.
- **Duration calibration from history.** Manufacturing learns cycle times from
  actuals. So can this.
- **We already own the engine.** `qnap/odooiq-factory-intelligence` models
  capacity as free time-intervals per `(workcenter, day)` derived from
  `resource.calendar`, solves EDD-greedy over pure-Python ERP-portable
  dataclasses, and calibrates with per-scope median/MAD and small-N shrinkage.
  Re-point `(workcenter, day)` at `(dock door, day)`, `(crew, shift)`,
  `(forklift, day)` and the architecture transfers directly.

**The single best argument for predictive here is one manufacturing rarely gets:
repetition.** A venue runs the same halls through the same docks for 20–40 shows
a year. Move-in for Hall C is a *repeated experiment* with a stable physical
configuration. A single-plant manufacturer usually has fewer distinct products
than a venue has shows. **The learning surface is unusually good.**

---

## 3. Where it breaks — and these are not small

### 3.1 The demand signal arrives backwards

In manufacturing you have an order book with lead time: demand is known before
capacity is needed. In exposition services, exhibitor service orders arrive as a
**spike at the advance-order deadline and keep changing straight through
move-in**, with a meaningful share landing at floor rates after the plan is set.

Consequence: **a scheduler that waits for firm demand is useless.** It must
forecast demand, not merely schedule it. This is the strongest argument *for*
the predictive layer rather than against it — but it means the forecast is
load-bearing, not a nice-to-have dashboard.

### 3.2 The real constraint is space and sequence, not machines

Manufacturing capacity is largely parallel and independent — two workcenters
rarely block each other physically. Move-in is not like that:

- carpet cannot go down an aisle that still holds crates
- rigging must precede booth build in the same footprint
- the last truck in is the first truck out
- two crews cannot occupy the same aisle

This is **construction scheduling** — cumulative resources plus *spatial
exclusion* plus precedence — not job-shop scheduling. EDD-greedy alone is
insufficient. The solver needs precedence constraints and a space-occupancy
resource, or it will produce plans that are arithmetically feasible and
physically impossible.

**This is the main engineering risk in lifting the OdooIQ solver.** The capacity
model and calibration port cleanly; the sequencing logic needs genuine new work.

### 3.3 Variance is far higher than manufacturing

A CNC cycle repeats to the second. Setting an island booth depends on whether the
exhibitor's own crew turned up, whether their freight cleared, and whether the
aisle was clear. Point estimates would be dishonest.

This makes OdooIQ's **p10/p50/p90 ranges that widen when data is thin** *more*
appropriate here than in the factory it was built for, not less.

---

## 4. What the first predictive model should actually forecast

Not head count. Not revenue.

> **The inbound freight arrival curve: CWT by day and hour, per dock.**

Reasons it wins:

1. **It is the true bottleneck.** Dock doors and forklift-hours gate everything
   downstream. Everything else has slack; this does not.
2. **It is forecastable from data you will hold** — booth mix plus per-exhibitor
   history plus the advance/floor deadline structure.
3. **It has an immediate, unambiguous operational use** — marshalling-yard
   sequencing and crew call times. The output is an action, not a number on a
   dashboard.
4. **It is measurable the same day.** Feedback arrives in hours, so the model
   calibrates fast — unlike a forecast whose error you learn about next year.
5. **Drayage is already the most-complained-about line in the category**
   (`competitors/04`). Predicting it well is a wedge into the thing customers
   already hate.

Secondary targets, in order: labour-hours by service type; setup duration per
booth type; and only then show-hours services from head count.

---

## 5. What "agentic" should mean — and what it must not

The competitor research (`competitors/02`, `08`) found five things **every**
vendor leaves entirely to humans:

1. ranking shortage resolutions
2. whole-roster crew assignment
3. learning durations from history
4. **cross-job portfolio trade-offs — invisible in every tool examined**
5. supplier selection

Those five are the agentic surface. Note what they have in common: each is a
*judgement over a feasible set*, not a computation. The deterministic solver
produces the feasible set; the agent ranks, explains and negotiates the
exceptions.

**The division of labour that holds:**

| Layer | Owns | Character |
|---|---|---|
| Forecast | demand curve with honest uncertainty | statistical, calibrated, testable |
| Solver | feasible plans under capacity + precedence + space | **deterministic and reproducible** |
| Agent | ranking, explanation, trade-off proposal, exception handling | LLM, proposes only |
| Human | commits | always |

Keep the solver deterministic. A plan that cannot be reproduced cannot be
defended to a show manager at 6am when the schedule slips — and "the model said
so" is not an answer anyone on a show floor accepts.

This is the same conclusion `spec/01` reached independently: **agent proposes,
human commits**, with a never-invocable list.

---

## 6. The trust boundary — and we already own a worked answer

A predictive scheduler is exactly where agentic systems go wrong: the agent
proposes a plan, the plan mutates state, and nobody can reconstruct why.

**`qnap/porterly-future-reference`** (recovered 2026-08-06 — see
`internal/02_recovered_asset_findings.md` §1) is a dependency-free Python
reference architecture that solves precisely this, with **74 invariant tests**:

- **event-sourced idempotent ledger** — every state change replayable
- **guarded FSM** — illegal transitions blocked structurally
- **agents-propose / core-decides**, where **core re-derives identity from ground
  truth rather than trusting agent claims**
- **policy-as-data**, enforced server-side rather than inside the agent

That last point is the load-bearing one. It is the same insight as Southbrook's
`PLM_LIFECYCLE` identity sentinel — *never let the caller assert its own
privilege* — arrived at independently in a different codebase. Two of our own
systems converged on it, which is about as strong a signal as internal evidence
gets.

**Read this repo before designing the agent/core split.** It is the single most
directly applicable artifact found in the entire asset review.

---

## 7. Sequencing — and the one decision that must be made now

Prediction needs history. On day one there is none. The honest order:

| Phase | What ships | Why here |
|---|---|---|
| **1** | Deterministic finite-capacity scheduling with precedence + space exclusion | Stands alone; useful with zero history |
| **1 (silent)** | **Actuals capture on every window** | Costs almost nothing now, impossible to backfill later |
| **2** | Calibration — median/MAD per scope, small-N shrinkage, p10/p50/p90 | Switch on per scope as N crosses threshold |
| **3** | Demand forecast — freight arrival curve | Needs several shows per venue-hall |
| **4** | Agentic exception handling and portfolio trade-offs | Needs 1–3 to be trusted first |
| **5** | Cross-venue learning → feeds the Show Board (`spec/02`) | The compounding asset |

> **The decision that cannot wait: instrument for actuals in version one.**

Every `floor.window` must record planned *and* actual start/end, and the reason
for variance, from the first release — even while nothing consumes it. Skip this
and Phase 2 is dead until a year after you remember to add it. It is nearly free
now and unrecoverable later. This is the same "near-free now, expensive retrofit
later" argument `spec/02` §9 makes about gap-listing fields, and it applies with
more force here because the missing asset is *time*, not schema.

---

## 8. Concrete additions to the data model

Beyond what `spec/01` already specifies:

**`floor.demand.driver`** — per show, per hall: booth count by type and size,
total sq ft, expected inbound CWT, and — separately, flagged as low-weight —
expected attendance. Versioned, because it changes continuously up to move-in;
the *history of how it changed* is itself a predictive feature.

**`floor.service.bom`** — bill of services per booth type. `20x20 island →
{rigging: 1 point, power: 20A × 2, labour: 6h, freight: ~800 CWT}`. Data, not
code — the same "configuration as data" discipline used elsewhere in the stack.
This is the explosion table that makes booth mix a real demand primitive.

**`floor.window` gains** `planned_start/end`, `actual_start/end`,
`variance_reason` (coded), and `predicted_p10/p50/p90`. Storing the prediction
*alongside* the actual is what makes the model auditable — you can always ask
"what did we think, and were we right", which is the only defensible basis for
ever letting the forecast drive a decision.

**`floor.space.occupancy`** — the spatial-exclusion resource. Aisle and footprint
as schedulable capacity, without which the solver produces impossible plans
(§3.2).

---

## 9. Verdict

**Adopt the framing, correct the demand unit, phase the intelligence.**

- ✅ **Yes** to finite-capacity scheduling with a manufacturing lineage — we own
  the engine and it is the differentiator in a category where
  `competitors/06` found setup/teardown buffers essentially unautomated and dock
  scheduling a confirmed category-wide gap
- ✅ **Yes** to predictive, forecasting **freight arrival**, not head count
- ✅ **Yes** to agentic — over the feasible set, proposing only, never committing
- ⚠️ **Correct the demand unit** to booth mix; treat head count as a minor
  secondary driver
- ⚠️ **Budget real work for precedence and spatial exclusion** — this is
  construction scheduling, not job-shop, and the lifted solver does not cover it
- 🔒 **Instrument actuals in v1** regardless of when the prediction ships

The honest summary: the manufacturing analogy is sound enough to build on, and
the category is unusually under-served here. It fails in exactly one place —
space and sequence — and that failure is the part worth building ourselves,
because it is also the part nobody else has built.
