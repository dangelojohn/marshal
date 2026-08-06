# Marshal — project plan

**As of 2026-08-06.** Supersedes the phasing sketched in
`01_product/01_what_we_are_building.md` §4, which was written before the primary
source input (D-005, D-006) and the resource model (`08`).

---

## The shape of the plan, in one line

> **Record → Coordinate → Schedule → Meter → Predict.**
> Deliberately *not* schedule-first.

**Why this order, and why it's the most important decision in the plan.**

The instinct is to build the optimiser first, because it's the clever part and
the differentiator. That would be a mistake here, for three reasons:

1. **We have no duration data.** How long does an electric forklift take from
   door 4 to booth 412 in this hall? Nobody knows. An optimiser built on guessed
   durations produces a confident, wrong schedule — and a schedule nobody trusts
   is worse than the whiteboard it replaced, because it costs credibility you
   only get once.
2. **The recording layer is already worth money.** The safety record (D-005 §1)
   and the metering (D-005 §2) are the two strongest parts of the business case,
   and **neither requires an optimiser.** They only require knowing what
   happened.
3. **Recording generates exactly what the optimiser needs.** Every movement
   logged is a calibration sample. Six months of Phase 1 makes Phase 2 possible;
   no amount of Phase 2 makes Phase 1 unnecessary.

So Marshal earns trust as a **system of record** first, and becomes a system of
*decision* once it has the evidence to justify one.

---

## Phase 0 — Answer the commercial questions · **now, no code**

Everything here is a conversation or a cheap test. **Nothing downstream should
start until these land**, because they change what gets built.

| # | Question | How | Blocks |
|---|---|---|---|
| **Q-1′** | Who captures the handling margin — facility or show manager? | Ask both | Who the customer is |
| **Q-8** | What's billed today, on what unit — dock hour, crate, pallet, weight? | Ask a facility ops director | The whole metering model |
| **Q-11** | Is Reolink motion detection usable at dock distance? | **`tools/` harness is built.** LAN cameras now, real dock later | Automatic actuals — the predictive layer |
| **Q-13** | Equipment: venue-owned, contractor-supplied, or exhibitor-brought? | Ask | Who schedules it, who bills it |
| **Q-15** | Who controls the freight elevator calendar in a hotel, and in what system? | Ask | Whether the connector ladder is day-one critical |
| **Q-6** | Hotels or convention centres first? | Follows from the above | Design partner |

**Exit gate:** one named design partner, and enough of Q-1′/Q-8 answered to know
who receives an invoice and in what unit.

> **Cost: a few phone calls and one camera left running.** This is the highest
> information-per-dollar work in the entire project, and skipping it is how
> people build beautiful software nobody buys.

---

## The fork — and the good news about it

Marshal can be two different businesses. This has to be decided, **but not yet.**

|  | **A · Product** | **B · Operating system for a services business** |
|---|---|---|
| What you sell | Software subscription | **Handling operations**, run on your own spine |
| Revenue | Per venue/hall/month | **The handling margin itself** (Q-1′) |
| Build | Multi-tenant, self-serve, polished | Far less UI, more Odoo, internal-grade |
| Scaling | Sell many, touch few | Fewer sites, deeper, people-heavy |
| Moat | The solver and the network | **Operational competence + the data** |
| Fits | Convention centres | **Hotels, where there's often no GSC at all** |

**Phases 0 and 1 are identical under both branches.** Both need the same movement
record, the same camera board, the same SMS coordination, the same actuals.

**The fork bites at Phase 2–3**, where A needs multi-tenant polish and B needs
depth in one operation. So the decision can be made *with* Phase-1 evidence
rather than ahead of it — which is exactly when it should be made.

`[ASSUMPTION]` B is the more interesting answer if Q-1′ shows the margin sitting
with show management and the facility wants it back. That would make Marshal the
instrument for taking it.

---

## Phase 1 — The board and the movement log · *the first real build*

**Goal:** one venue, one hall, one real move-in — with Marshal recording and
coordinating, not deciding.

**Ships:**

- **The wall board** (D-006) — camera tiles, each overlaid with what's scheduled
  there now. Snapshot refresh, not streaming. Three states: active / clear /
  exception. Shop-floor constraints: 56px targets, glare-legible, no hover, every
  action visibly confirms
- **The movement record** (`08` §1) — crate, from dock, to booth, equipment,
  operator, elevator leg. **Planned and actual, plus a coded variance reason**
- **Two-way SMS** (D-005 §4) — call next truck, hold, re-slot, confirm. Drivers
  are in a truck and will not log in
- **Automatic actuals** from motion state — *if Q-11 passes*. If it doesn't,
  fall back to one-tap confirm on the board
- **Manual sequencing.** A human orders the movements. Marshal records,
  coordinates, and shows the consequences

**Explicitly not in Phase 1:** the optimiser, predictive anything, billing,
multi-tenant, the Show Board.

**Exit gate — all three, honestly measured:**
1. Ops ran a real move-in on it and asked to keep it
2. ≥80% of movements carry usable actuals
3. One incident or dispute where the record answered a question nothing else could

That third gate is the real one. **It is the proof the safety-and-evidence thesis
is true**, and it's binary — either the record settled something or it didn't.

---

## Phase 2 — The scheduler

**Only once Phase 1 has produced real durations.**

Port the OdooIQ solver, re-pointing `(workcenter, day)` at `(resource_unit, day)`
— specific forklifts, specific elevators, named operators, aisle segments. Then
add, in the order they cost most to omit (`08` §6):

1. Travel/repositioning for mobile resources — omit it and every plan is
   optimistic by a constant
2. Precedence within a movement
3. Capability matching with directional substitution
4. Spatial exclusion on aisles
5. Charge windows for electric units
6. Foreign-calendar blackouts for shared vertical transport

**Agent proposes, human commits** (`spec/03` §5). The solver produces the feasible
set; the agent ranks and explains; a person accepts. The board stays the surface —
the schedule appears *on the tiles*, not in a new screen to learn.

**Exit gate:** the proposed sequence is accepted without material edit more often
than not, over a full move-in.

---

## Phase 3 — Metering and billing · *where revenue attaches*

Phase 1's actuals become **billable consumption records**, in whatever unit Q-8
says the market already uses.

The sale: *"you billed 40 hours of handling. The floor consumed 62. Here's the
record, with timestamps and stills."*

**This is the phase that pays for the project**, and it is only credible because
Phase 1 spent months proving the record is trustworthy. Shipped earlier, it would
be an assertion.

Under branch B this isn't a product feature at all — it's the operating margin.

---

## Phase 4 — Predictive

Forecast the **inbound freight arrival curve — CWT by day, hour, dock**
(`spec/03` §4). Not head count. Not floor area. Demand explodes from **booth
mix** via the bill of services (`05` §6).

Needs several shows per venue-hall of history, which Phases 1–3 accumulate. A
venue runs the same halls through the same docks 20–40 times a year — **move-in
is a repeated experiment**, and that's a better learning surface than most
factories get.

---

## Phase 5 — The Show Board

The capacity network (`04_show_board_network.md`). Gap data arrives as a
byproduct of the workflow tool, which dissolves the cold start.

**Gated on counsel, not engineering (Q-4).** Competing venues seeing each other's
availability is antitrust-sensitive in Canada and the US. Get an opinion before
building — the constraint shapes the data model.

---

## What we already own

| Asset | State | Use |
|---|---|---|
| **Reolink client** | ✅ Working, pushed | Motion state + snapshots. **Not streaming** |
| **`avn.capability`** | ✅ Verified by direct read | Connector ladder for SMS/portal/API, and equipment capability matching (`08` §3) |
| **OdooIQ solver** | ✅ Verified read-only | Phase 2 starting point — capacity intervals, median/MAD calibration, p10/p50/p90 |
| **`porterly-future-reference`** | ✅ 74 invariant tests | Agents-propose/core-decides. **Read before designing the agent boundary** |
| **`aemi.service.request`** | ⚠️ Uncommitted, untracked | Best-fit demand model. **Push it** |
| **Porterly portal + PWA patterns** | Licence per module | Public→validated-record intake |

---

## Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| **Q-11 fails — motion unusable** | Medium | Phase 1 falls back to one-tap confirm. Slower actuals, not fatal. **Test costs almost nothing — do it first** |
| Ops won't adopt a new surface mid-show | **High** | The board *is* the camera wall they already watch. Never make them type during move-in |
| Metering unit doesn't match existing billing | **High** | Q-8 blocks Phase 3. Get it before building |
| Spatial/precedence solver is harder than estimated | Medium | Phase 1 ships value without it. Phase 2 can slip without killing the product |
| Hotel elevator calendar is a person, not a system | Medium | `avn.capability`'s human_workflow tier is designed for exactly this |
| Scope creep from the full platform vision | **High** | `spec/01` is the destination, not the plan. **Phases 1–3 only** |
| Building the optimiser first | **High** | This document. Record before decide |

---

## What happens next

1. **Run the Q-11 harness on the LAN test cameras** — validates the tooling
   before it matters. `tools/README.md`
2. **Make the Phase-0 calls.** Q-1′ and Q-8 are the two that gate everything
3. **Name a design partner** — likely a Toronto hotel, from existing relationships
4. Then, and only then, build Phase 1

**Nothing is built yet, and that is correct.** Every hour spent on Phase 0 is
worth a week of Phase 1 rework.
