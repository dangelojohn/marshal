# The resource model — what Marshal actually schedules

**Source:** John D'Angelo, 2026-08-06 `[PRIMARY]`

> *"We also need to schedule lifts and elevators in coordination to arrival time
> and dock schedules, and also equipment such as forklift electric and standard,
> pump trucks and specialized carts."*

This **closes Q-7** (is vertical transport a first-class resource — yes) and
turns D-005's "the constraint is the handling resource and its route" into a
concrete model.

---

## 1. The unit of work is a movement, not a booking

A movement is not an appointment. It is a **chain of resource claims that must
line up in time**, any one of which can break the whole thing:

```
movement:  crate C  ·  dock D → booth B

  arrival     truck at dock D            [dock door + time]
  unload      lift C off the truck       [equipment + certified operator]
  transit-1   dock → elevator lobby      [route + aisle occupancy]
  vertical    floor 1 → floor 3          [elevator: capacity, dimensions, time]
  transit-2   lobby → booth B            [route + aisle occupancy]
  place       set C in position          [equipment + operator]
```

**The elevator has to be free when the crate reaches it.** That is the sentence
that makes this a coordination problem rather than a booking problem — and it is
why every step above has to be planned together, not each in its own calendar.

Book a dock slot without the equipment and you have a truck at a door with
nothing to unload it. Book the equipment without the elevator and you have a
loaded forklift queued at a lobby, blocking the aisle it's standing in.

---

## 2. The resource taxonomy

| Class | Examples | Character | Notes |
|---|---|---|---|
| **Dock position** | Door 1–N, yard bays | Fixed, capacity 1 | The arrival gate, not the bottleneck |
| **Handling equipment** | Electric forklift, standard forklift, pump truck, specialized cart | **Mobile — has a position, must travel to the job** | Not fungible — see §3 |
| **Vertical transport** | Freight elevator, scissor lift, hoist | **Serial, positional, dimension-limited** | Usually the hard constraint |
| **Operator** | Certified forklift operator, general labour | Human, shift-bound, **certification-gated** | Safety and compliance record |
| **Space** | Aisle segment, lobby, booth footprint | **Exclusive occupancy for a window** | What makes plans physically possible |
| **Storage** | Empties/crate storage | Capacity-limited | Gates the move-out sequence |

**Mobile resources are the ones that break naive scheduling.** A forklift is not
"free from 09:00–09:30" — it is *at door 2* and needs four minutes to reach door
7. Ignore that repositioning cost and every plan runs late by exactly the amount
you ignored.

---

## 3. Equipment is not interchangeable

This is the part a generic scheduler gets wrong, and it is a **safety** rule
before it is an efficiency one.

| Equipment | Can do | Cannot do | Hard constraint |
|---|---|---|---|
| **Electric forklift** | Indoor use, finished floors, high lift, heavy | | **Battery — see §4** `[COMMON]` |
| **Standard (LP/diesel) forklift** | Yard, dock apron, heavy, no charge downtime | **Often barred indoors** — exhaust and air quality | Fuel swap; venue rules `[ASSUMPTION]` |
| **Pump truck** (manual/electric) | Palletized goods, flat floors, tight aisles | **No height. Pallets only** | Floor surface — struggles on carpet `[COMMON]` |
| **Specialized cart** | Odd shapes, fragile, glass, art | Not heavy, not high | Often venue-owned, scarce `[ASSUMPTION]` |

**Substitution is directional, not symmetric.** An electric forklift can usually
do a pump truck's job; a pump truck can never do a forklift's. So a movement
declares a **required capability**, and the scheduler picks any unit that
satisfies it — preferring the cheapest and least scarce.

> This is exactly the shape of `avn.capability`, our best-verified internal asset:
> **the caller declares the contract it needs; the system fulfils it with whatever
> satisfies that contract.** The connector ladder becomes an equipment ladder.
> Same pattern, different domain.

`[ASK]` **Which equipment is venue-owned versus contractor-supplied versus
exhibitor-brought?** Ownership determines who schedules it and who bills it —
and that connects straight back to Q-1′.

---

## 4. The constraints that quietly break a plan

These are the ones that make an ops person trust the tool, because they are the
ones they've been burned by.

### Battery charge on electric forklifts `[COMMON]`

A move-in runs 12–16 hours. **Electric forklift batteries do not.** A plan that
doesn't model charge state produces a schedule that dies at hour eight, and the
failure lands mid-move-in when there's no recovery room.

Charging is a **scheduled resource claim**, not downtime to ignore:
- charge duration and opportunity-charge windows
- how many chargers exist — often fewer than trucks
- swap batteries or charge in place
- a truck on charge is unavailable and occupies a charging bay

**If Marshal models nothing else about equipment, it should model this.** It is
concrete, it is currently tracked in nobody's head reliably, and getting it right
is instantly legible to the person who's been stranded by it.

### Elevator dimensions, not just weight `[COMMON]`

A crate can be under the weight limit and still not fit. Door aperture, internal
depth, and diagonal clearance all bind independently. **Weight is the constraint
people model; dimension is the constraint that strands a crate in a lobby.**

### Shared vertical transport in hotels `[ASSUMPTION — hotel-specific, high value]`

In a hotel the freight elevator is **not the event's to command.** It is shared
with housekeeping, F&B, laundry and engineering, and there may be blackout
windows during banquet service or guest peak.

So Marshal must schedule against **a calendar it does not own**, held by hotel
operations — possibly in another system, possibly in someone's head.

This is precisely what `avn.capability`'s connector ladder was built for: the
same contract fulfilled by an API, a portal, an email, or *"phone the loading
dock manager."* **If hotels are the beachhead (Q-6), this is a first-class
requirement, not an edge case.**

### Operator certification `[COMMON]`

Powered equipment requires a certified operator, and in Ontario that's a
regulatory obligation, not a preference. Certification is therefore both a
**scheduling constraint** (the equipment is useless without a qualified body) and
a **compliance record** — which is D-005's defensible-record feature arriving for
free: *who operated what, when, under which certification, on whose authority.*

### Route congestion and aisle exclusion `[ASSUMPTION]`

Two powered units should not work the same aisle segment simultaneously, and a
crew working a booth means no powered traffic past it. **Aisle occupancy is a
schedulable resource** — the spatial-exclusion requirement from `spec/03` §3.2,
now with a concrete owner.

---

## 5. Why this is not appointment booking

Stacking these up, Marshal's core is a **resource-constrained scheduling problem
with mobile resources, precedence, and spatial exclusion** — structurally the
same family as construction sequencing or container-terminal crane scheduling.

| | Appointment booking | **Marshal** |
|---|---|---|
| Resource | Fixed, capacity N | **Mobile, has a position and travel time** |
| Job | One slot | **Chain of claims that must align** |
| Substitution | None | **Directional capability matching** |
| Space | Ignored | **Exclusive occupancy** |
| Availability | Calendar | **Also charge state, certification, foreign calendars** |

**This is why Opendock and the warehouse dock schedulers cannot cross over** —
they solve the first column. It is also why the OdooIQ solver is the right
starting point: it already models capacity as free intervals per resource with
calibrated durations, which is the hard half.

**What has to be added:** mobile-resource repositioning, precedence within a
movement, capability matching, and spatial exclusion. That is real work — and it
is the defensible part, because it is the part nobody has built.

---

## 6. What this means for the solver

Re-point OdooIQ's `(workcenter, day)` free-interval model at
**`(resource_unit, day)`** where a resource unit is a specific forklift, a
specific elevator, a named operator, or an aisle segment.

Then add, in order of how much each one costs to omit:

1. **Travel/repositioning time** between consecutive jobs for mobile resources —
   omit this and every plan is optimistic by a constant
2. **Precedence within a movement** — unload → transit → vertical → transit → place
3. **Capability matching with directional substitution** (§3)
4. **Spatial exclusion** on aisle segments
5. **Charge windows** as first-class claims on electric units (§4)
6. **Foreign-calendar blackouts** for shared vertical transport (§4)

Calibration (`spec/03`) applies per resource class: an electric forklift's
transit time between two points is exactly the kind of duration that should be
learned from actuals rather than guessed — and `get_motion_state` (D-006) can
observe a good deal of it without anyone typing.

---

## 7. Open questions this raises

| # | Question | Why it matters |
|---|---|---|
| **Q-13** | Which equipment is venue-owned vs contractor-supplied vs exhibitor-brought? | Determines who schedules and who bills it — feeds Q-1′ |
| **Q-14** | How many electric units and chargers per venue, and what is the real runtime? | Decides whether charge modelling is critical or merely nice |
| **Q-15** | Who controls the freight elevator calendar in a hotel, and in what system? | If it's a person rather than a system, the connector ladder is load-bearing on day one |
| **Q-16** | Are there venue rules barring LP/diesel units indoors? | A hard safety constraint the scheduler must never violate |
| **Q-17** | Is operator certification tracked today, and where? | Free compliance win if we hold it; a data-entry burden if we must import it |
