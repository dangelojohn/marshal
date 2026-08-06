# Operating model v2 — corrected by primary source

**Source:** John D'Angelo, 2026-08-06. Direct operating knowledge from building
ERPs for a number of top Toronto hotels with event/banquet operations.

This supersedes the guesswork in `05_movein_operating_model.md` where the two
conflict. Claims here are `[PRIMARY]` — first-hand practitioner knowledge, the
strongest evidence in this project so far. `05` remains as the record of what we
assumed before asking.

---

## What was confirmed

> **"The venue does feel the pain. Move-in and move-out days are crazy and need
> scheduling."** `[PRIMARY]`

This closes the riskiest open assumption in the entire thesis. `05` §8 said not
to build until this was answered. **It is answered.**

Also confirmed: the dock and the material movement into booths are the real
constraint, and move-out is as bad as move-in.

---

## What changed — five reframes, in order of how much they move the product

### 1. It is a SAFETY problem first, efficiency second

> **"It is primarily a safety issue, and a resource issue — forklifts and pump
> trucks, tight spaces."** `[PRIMARY]`

We modelled this as a throughput problem. It is a **controlled-movement problem
that happens to have throughput consequences.** Powered equipment manoeuvring
heavy crates through congested aisles with people working in them is the hazard,
and scheduling is the control that manages it.

**This changes the product, the buyer and the pitch:**

| | Efficiency framing (wrong) | Safety framing (right) |
|---|---|---|
| Buyer | Ops manager, wants faster | Ops **and risk/GM**, must demonstrate control |
| Budget | Discretionary, competes with everything | Far less discretionary |
| Pitch | "Save an hour of dock idle" | **"Prove you controlled the floor"** |
| Killer feature | Optimised sequence | **Defensible record of who moved what, where, when, with which equipment, under whose supervision** |

**Features this pulls forward that weren't in scope at all:** equipment and
certified-operator assignment, aisle exclusion windows (no powered equipment
while a crew works that aisle), incident and near-miss capture against the
schedule, and an after-the-fact reconstruction of any movement.

That last one is the sleeper. **After an incident, the question is always "what
was supposed to be happening there?"** Nothing on the market can answer it,
because the plan lives in a spreadsheet that was overwritten.

### 2. This is REVENUE, not cost avoidance

> **"There are charges at some facilities for docks and when materials
> arrive."** `[PRIMARY]`

We priced Marshal as cost avoidance — soft ROI, hard sale. Wrong. **Dock time and
material handling are already billable services.** If it is billed, it is
metered, and it is metered on paper.

**Paper metering leaks.** The floor consumes more handling than anyone captures,
and nobody can reconstruct it well enough to argue. A system that schedules the
movement *also* meters it, and metering attaches Marshal to a revenue line
instead of a cost line.

> The sale becomes: **"you billed 40 hours of handling last show. The floor
> consumed 62. Here's the record."**

That is a categorically easier conversation than "we'll save you time," it pays
for itself out of recovered revenue, and it makes the product very hard to remove
once it is the billing system of record.

### 3. Hotels may be the better beachhead than convention centres

The primary source is **hotels**, not convention centres. That is worth taking
seriously as a market signal rather than an accident of who we know.

| | Convention centres | **Hotels with event space** |
|---|---|---|
| Count | Few per country | **Many — every major hotel** |
| Dock | Purpose-built, many doors | **Shared with F&B, laundry, guest ops — brutally contended** |
| Vertical | Mostly flat floors | **Freight elevators, tight back-of-house** |
| Incumbent | GES/Freeman embedded | **Usually none** |
| Ops team | Exhibition specialists | **Hotel staff, no exhibition tooling** |
| Our access | Cold | **Existing relationships + ERP credibility** `[PRIMARY]` |

Hotels have **worse** physical constraints, **less** specialist tooling, and
**no embedded incumbent to dislodge.** They are also numerous enough to be a
repeatable sale rather than a series of bespoke enterprise deals.

`[ASSUMPTION]` Convention centres remain the larger per-site contract and the
better logo — but they are the second market, not the first.

**This does not weaken the exclusivity argument from D-002; it strengthens it.**
The dock was the one place no exclusivity contract reached. In a hotel there is
often no general service contractor at all, so the whole floor is reachable.

### 4. SMS is the vendor surface — not a portal

> **"They need communication with vendors via SMS."** `[PRIMARY]`

Carriers, drivers and exhibitor-appointed contractors **will not log into a
portal.** They are in a truck. Any design that assumes a login has already failed
for the population that most needs to be coordinated.

**Two-way SMS is the primary channel**, not a notification add-on:

- *"Dock 4 at 14:20. Reply Y to confirm, D to declare a delay."*
- *"You're next — pull to door 7 now."*
- *"Running late? Reply with an ETA and we'll re-slot you."*

This is a direct vindication of `avn.capability`'s connector-maturity ladder
(`mcp → api → portal → web_form → email → human_workflow`), our best-verified
internal asset: **the same contract is fulfilled at whatever integration maturity
the counterparty actually has.** A driver with a phone and a national carrier with
an API present the identical contract to the scheduler.

`[ASK]` Does French-language SMS matter for Quebec under Bill 96? Almost
certainly yes for Montreal venues, and it is cheap to design in now.

### 5. There are THREE billing parties, not two

> **"Many times it is the SHOW MANAGEMENT companies, not the facilities, that
> charge for this service."** `[PRIMARY]`

We modelled venue and contractor. There is a third, and it holds the margin:

```
Facility PROVIDES the handling  →  Show management BILLS it  →  Exhibitor PAYS
```

The facility supplies equipment and operators; the show manager marks it up and
invoices the exhibitor. **Whoever holds that margin has the strongest reason to
meter it accurately — and whoever is losing it has the strongest reason to
start.**

This reopens Q-1 in a more useful form. It is no longer "venue or contractor" but
**"who currently captures the handling margin, and who wants it back?"**

---

## What this does to the constraint model

`05` §2 guessed the binding constraint was the marshalling yard or dock doors.
**Primary source says otherwise:** the constraint is the **specialised handling
resource and its route** — forklift or pump truck, a competent operator, and a
physically tight path from dock to a specific booth.

**Doors are not the bottleneck. Getting the crate from the door to booth 412
is.** A truck at a dock with nothing to move it inward is not progress.

That makes the schedulable unit **a movement, not a slot**:

```
movement := crate/pallet → from dock D → to booth B
            requires: equipment E + certified operator O
            traverses: route R (aisles, corners, elevator)
            duration:  f(distance, congestion, crate size, elevator)
            excludes:  other powered equipment in the same aisle window
```

This is closer to **warehouse task interleaving with a safety envelope** than to
appointment booking — and it is a much better fit for the OdooIQ solver's
`(resource, day)` free-interval model than dock doors ever were. Re-point
`workcenter` at *equipment + operator pairs* rather than doors.

`[ASSUMPTION]` The freight elevator is the hard serial constraint in hotels,
in the way the dock door was assumed to be in convention centres.

---

## Revised view of what Marshal is

> **Marshal schedules and meters the safe movement of freight from dock to booth
> and back — coordinating carriers by SMS, controlling powered equipment in
> shared space, and producing a defensible record of both.**

Three jobs, one dataset:

1. **Schedule** the movements under equipment, operator, route and safety limits
2. **Coordinate** the outside world over SMS, because that's where it lives
3. **Meter** what was actually consumed, because it is billable and currently leaks

---

## Open questions after this update

| # | Question | Why it matters now |
|---|---|---|
| **Q-1′** | **Who currently captures the handling margin — the facility or the show manager — and who wants it back?** | Replaces the old venue-vs-contractor question. Determines the buyer |
| Q-6 | Do hotels or convention centres go first? | Leaning hotels: worse constraints, no incumbent, existing relationships |
| Q-7 | Is the freight elevator the true serial constraint in hotels? | Decides whether the solver models vertical transport as a first-class resource |
| Q-8 | What is already charged, and on what unit — dock hour, crate, pallet, weight? | The metering model must match the existing billing unit or it won't be adopted |
| Q-9 | Who carries liability for a floor incident — facility or show manager? | Safety framing only sells to whoever holds the risk |
| Q-10 | Is French-language SMS required for Quebec? | Cheap now, expensive to retrofit |

---

## What is now safe to build

`05` §8 said don't build until the pain was confirmed and the constraint
identified. **Both are now answered**, so the following are no longer speculative:

- the **movement** primitive (not "dock slot")
- **equipment + operator** as the scheduled resource
- **two-way SMS** as the primary external channel
- **actuals capture** on every movement — planned vs actual, plus variance reason
- **billable-consumption metering** derived from those actuals

**Still blocked on Q-1′ and Q-8:** anything that decides *who the invoice is
addressed to*, and *what unit it is denominated in*. Get those wrong and the
metering — the strongest part of the business case — doesn't match anyone's
existing billing.
