# Round 1 — Efficiency candidates (RAW agent output + my flags)

**Agent:** low-cost generator, focus = efficiency. 14 candidates.
**Status:** RAW. Not yet through the adversarial pass. Do not cite from here.

## ⚠ My flags before scoring — three problems with this set

**1. Every magnitude in it is fabricated.** "30–40% of forklift labor", "200
trips/day", "60% deadheading", "40% of move-in time" — **none of these are
sourced.** No agent in this session has access to a real move-in dataset. Treat
every percentage as a placeholder for a question to ask a venue, never as a
finding. This is the same discipline the market research used and it applies here.

**2. Candidate #1 "Move Staging Tier" is probably wrong and it scored itself
9/10.** It asserts exhibitors "stage their booth frame before freight day (standard
practice)" and that re-handling can therefore be collapsed. That **contradicts the
precedence chain** in `01_product/08_resource_model.md` — rigging → under-floor
utilities → targeted freight → island build → inline build → empties out → aisle
carpet. Freight arrives *before* the booth is built, not after. Marked SUSPECT.

**3. Candidate #14 is a category error.** "Pump-Truck Hydrant Prepositioning —
run hydraulic lines to 3–4 booths simultaneously" confuses a **pallet pump truck**
(a manual hydraulic pallet jack) with a **fire/water pump truck**. There are no
hydraulic lines to run. The agent self-flagged it as failing, but for the wrong
reason. DISCARD.

**4. Candidate #9 "Aisle Segment Locking" is under-scored at 6/10.** The agent
framed it as *efficiency* and concluded contention is "rare". But in
`08_resource_model.md` aisle exclusion is a **safety mechanism first** — two
powered units in one aisle segment, or powered traffic past a working crew, is the
hazard D-005 identified as the core of the product. **Re-score under the safety
lens, not the efficiency lens.**

## Candidates worth carrying into the adversarial pass

| # | Name | Agent value | My read |
|---|---|---|---|
| 3 | **Reverse logistics — empties as a scheduled movement** | 9 | ⭐ Strongest. Matches the research finding that empty-return is the worst queue in the whole lifecycle, and it's almost entirely unscheduled today |
| 2 | **Deadhead detection + move chaining** | 8 | ⭐ Real. Mobile resources have position (`08` §2); chaining is how you exploit that |
| 4 | Dock consolidation window (batch by destination) | 8 | Good, but the offline-hold behaviour is the whole risk |
| 5 | Exhibitor pre-validation by SMS 48h out | 8 | Good — correct use of the LLM edge, and it attacks the "demand arrives late" problem in `spec/03` §3.1 |
| 12 | **Schedule the operator, not the vehicle** | 7 | ⭐ Counter-intuitive and possibly right. Ties directly to the employee-scheduling strand |
| 6 | Battery-aware EV dispatch | 7 | Already required by `08` §4 — this is confirmation, not a new idea |
| 7 | Equipment capability ontology | 7 | Already decided in `08` §3 (directional substitution). Not new |
| 11 | Opportunistic batching at accept-time | 7 | Weaker sibling of #2 |
| 10 | Watch shows next N moves | 6 | ⚠️ Conflicts with `13` §6 — **the watch shows ONE job, never a list.** Needs resolving, not adopting |
| 8 | Elevator slot reservation | 6 | Correctly self-flagged: collapses if the hotel won't cooperate. Q-15 |
| 13 | Elevator congestion pricing | 5 | No enforcement mechanism. Weak |
| 1 | Move staging tier | 9 | **SUSPECT — see flag 2** |
| 14 | Pump-truck prepositioning | 4 | **DISCARD — see flag 3** |

## Genuinely new ideas in this set (not already in our docs)

1. **Empties as first-class scheduled movements, created automatically on inbound
   completion** — turns the worst bottleneck into scheduled work
2. **Move chaining to kill deadheading** — look ahead from a completing movement
   for a near-origin next job
3. **Schedule the operator rather than the vehicle** — assign a certified person,
   let the system pick a compatible unit
4. **Pre-validate the freight manifest by SMS before arrival** — attack demand
   uncertainty upstream instead of absorbing it at the dock
