# The move-in operating model — a strawman to be corrected

**Purpose:** this is not a specification. It is **a deliberately specific,
probably-wrong model of how a move-in actually runs**, built to be put in front
of a venue ops director and a service contractor so they correct it.

The corrections are the product spec. A blank page gets you polite generalities;
a wrong diagram gets you *"no — that's not how the empties work"*, and that
sentence is worth more than a week of desk research.

> ## ⚠ Confidence — read this before quoting anything here
>
> The market research behind Marshal was compiled **without web search
> available**. This document is worse than that: it is largely **industry-common
> knowledge recalled, not sourced**. Every number is a placeholder.
>
> - `[COMMON]` — established industry practice, not individually sourced here
> - `[ASSUMPTION]` — our inference, explicitly untested
> - `[ASK]` — a question to put to a human, where our guess is weakest
>
> **Nothing in this file should reach a customer deck or an investor until a
> practitioner has marked it up.** Its whole job is to be marked up.

---

## 1. The sequence we think we're scheduling

Move-in is not a set of parallel tasks. It is a **precedence chain with spatial
exclusion** — most steps physically block the next until they clear the floor.

| # | Step | Why it blocks what follows | Confidence |
|---|---|---|---|
| 1 | **Floor marking** — booth positions chalked/taped from the floor plan | Nothing can be placed until positions exist | `[COMMON]` |
| 2 | **Rigging** — hanging signs, truss, lighting | Needs clear floor for lifts/cranes. **Must precede booth build in the same footprint** | `[COMMON]` |
| 3 | **Under-floor utilities** — electrical drops, plumbing, data | Must be placed before anything covers the floor | `[COMMON]` |
| 4 | **Targeted freight** — trucks called in waves by zone | Freight lands where booths will be built | `[COMMON]` |
| 5 | **Island / large booth build** — EAC crews | Longest builds, need lift access, start first | `[COMMON]` |
| 6 | **Inline booth build** | Faster, fits around the islands | `[COMMON]` |
| 7 | **Empties out** — crates labelled and hauled to storage | **Aisles cannot clear until crates are gone** | `[COMMON]` |
| 8 | **Aisle carpet** | Goes down last, on a clear floor | `[COMMON]` |
| 9 | **Final clean** | | `[COMMON]` |

**The load-bearing claim:** steps 2→3→4 and 7→8 are hard precedence, and the
whole chain is competing for the same aisles. That is why a general-purpose
scheduler produces plans that are arithmetically valid and physically
impossible — and it is the part of the solver we would have to build ourselves.

`[ASK]` **Is this order right, and what breaks it?** Which steps actually run
concurrently that we've drawn as sequential?

---

## 2. Where the queue forms — the five constraints

Marshal's whole thesis is that the bottleneck is physical and upstream of
everything else.

| Constraint | What it is | Our guess | Confidence |
|---|---|---|---|
| **Marshalling yard** | Trucks waiting to be called to a door | **This is where the hours go** | `[ASSUMPTION]` |
| **Dock doors** | Finite per hall | 10–40 for a large hall | `[ASSUMPTION]` |
| **Forklift + crew** | Unload capacity per door | The real throughput limit, not the door count | `[ASSUMPTION]` |
| **Freight elevators** | Multi-level venues only | Severe where present | `[COMMON]` |
| **Empties storage** | Where crates live during the show | Capacity-constrained; gates step 7→8 | `[COMMON]` |

`[ASK]` **Which of these actually binds first?** Our bet is the yard, but if the
true constraint is crew rather than doors, the product is a labour-planning tool
wearing a dock-scheduling costume — **and that changes what we build.**

---

## 3. The target-time system — the incumbent mechanism we'd be improving

Exhibitors are assigned **target move-in times** by zone, so freight arrives in
waves rather than all at once. `[COMMON]`

**What we believe goes wrong, and why it's a software problem:**

- Targets are set **before** the real freight picture exists — booth mix and
  actual weights firm up late `[ASSUMPTION]`
- A missed target sends you to the back of the queue, so **the cost of lateness
  is non-linear** `[ASSUMPTION]`
- Targets are published as a static document, not a live schedule, so nobody
  re-plans when reality drifts `[ASSUMPTION]`
- The yard has no queue visibility — a driver knows they're waiting, not for how
  long `[ASSUMPTION]`

**If all four are true, Marshal is a re-planner, not a scheduler.** The value
isn't the initial plan — it's continuously repairing it as trucks arrive early,
late, or not at all. That is a meaningfully different product, and it is also
much harder for an incumbent to bolt on.

`[ASK]` **Who sets targets today, in what tool, and how often do they change
after publication?**

---

## 4. What it costs when it slips

The pitch depends entirely on these numbers, and **we do not have them.**

| Cost | Who eats it | Our guess | Confidence |
|---|---|---|---|
| **Truck detention** | Carrier bills the exhibitor/contractor | Hourly, after a free window | `[COMMON]` |
| **Overtime labour** | Show/exhibitor | Union rates step up after hours and at weekends — often the single biggest swing | `[COMMON]` |
| **Crew idle** | Contractor | Crew booked, freight not there | `[ASSUMPTION]` |
| **Compressed schedule** | Venue | Longer turnaround = fewer show-days sold per year | `[ASSUMPTION]` |
| **Show-open risk** | Everyone | The unpriced catastrophe | `[COMMON]` |

`[ASK]` **the two numbers the whole business case rests on:**
1. *(venue)* What does an hour of dock idle cost during move-in — and what would
   one extra sellable show-day per year be worth?
2. *(contractor)* What does late scope-change notice cost you, and when do you
   typically find out?

**Whichever is bigger and better documented decides whether we sell to the venue
or the contractor first.** That is open question Q-1, and it is answered by two
phone calls rather than any amount of building.

---

## 5. Move-out is probably the worse problem

Move-in is staged over days. **Move-out is a stampede** — everyone leaves at
once, and the sequence inverts: empties must come *back* to every booth before
anything can be packed. `[COMMON]`

`[ASSUMPTION]` The empty-return is the single worst queue in the entire show
lifecycle, and it is almost entirely unscheduled.

`[ASK]` **Is move-out the more painful sale?** If so it may be the better wedge —
same data model, more acute pain, and nobody is even pretending to solve it.

---

## 6. First-cut bill of services — the demand explosion

`spec/03` established that **booth mix is the demand primitive**, not floor area
or head count. This is the table that makes booth mix computable. **Every figure
is a placeholder to be corrected.**

| Booth type | Typical size | Rigging | Power | Labour (build) | Freight | Confidence |
|---|---|---|---|---|---|---|
| Inline | 10×10 | rare | 1× 20A | ~2 h | light | `[ASSUMPTION]` |
| Inline (large) | 10×20 | rare | 1–2× 20A | ~3 h | light | `[ASSUMPTION]` |
| Peninsula | 20×20 | sometimes | 2× 20A | ~5 h | medium | `[ASSUMPTION]` |
| **Island** | 20×20+ | **usually — hanging sign** | 2–4× 20A + 208V | **~6–10 h, lift needed** | **heavy** | `[ASSUMPTION]` |
| Multi-level | 20×20+ | yes | high | very high, permit/engineering | very heavy | `[COMMON]` |

**Why this table is the crux:** a 20×20 island and four 10×10 inlines are both
400 sq ft, and to a floor-area model they are identical. They are not remotely
identical to the floor — the island needs rigging (before everything), a lift
(competing for aisle space), and several times the crew hours.

`[ASK]` **What are the real multipliers?** Is an island genuinely ~3× an inline
on labour, or is that badly wrong?

---

## 7. What we'd instrument on day one

Independent of which way Q-1 resolves, the same facts need capturing — and
`spec/03` §7 makes the case that this cannot be backfilled later:

- truck **arrival** at the yard, **call** to a door, **on-dock**, **released**
- crew **planned vs actual** start and end, per booth
- **variance reason**, coded, every time
- empties **out** and **returned**

**Four timestamps and a reason code.** That is the entire dataset that makes
prediction possible, and none of it exists in a spreadsheet today.

---

## 8. How to use this document

1. Print it. Take it to one venue ops director and one service contractor.
2. Ask them to **cross things out**. Resistance is the signal — the parts they
   argue with hardest are the parts we've modelled wrongest.
3. Get the two numbers in §4.
4. Bring the marked-up copy back and it becomes `06_*_operating_model_v2.md`,
   with `[ASK]` replaced by sourced answers.

**Do not build until §2 and §4 are answered.** Everything else in this project is
reversible; building the wrong solver is the one mistake that costs months.
