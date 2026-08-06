# Financial model — what a CFO would sign

**Purpose:** turn the Dock & Marshalling Fee model (D-015) into unit economics
with a breakeven, a sensitivity range, and a venue qualification threshold.

> ⚠ **Two inputs are unknown and they drive everything: the fee an exhibitor will
> pay (Q-53) and bookings per venue-year (Q-55).** Every figure here is
> parameterised so the model can be re-run the moment those land. **The
> conclusion of this document is that narrowing those two numbers is the highest
> return activity available**, and the math shows why.

---

## 1. The unit — one exhibitor vehicle booking

### Revenue

| Item | Treatment |
|---|---|
| Dock fee `D` | Paid by exhibitor **to the venue** (Stripe Connect, venue is merchant) |
| Marshal take `t` | **22% of `D`** (list) · **18% design-partner rate** |
| Payment processing | **Passed through to the exhibitor**, not absorbed |
| Penalty / rebooking fee | To the venue. **Marshal takes processing cost recovery only — zero margin** |

**The pass-through is the single most important line in this model.**

| | Absorbed | **Passed through** |
|---|---|---|
| Marshal gross (22% of $150) | $33.00 | $33.00 |
| Stripe (2.9% + $0.30) | −$4.65 | $0 |
| **Net** | **$28.35 (18.9%)** | **$33.00 (22.0%)** |

> Absorbing processing costs **3.1 points of take** — at mid-case volume that is
> **$27,900 per venue per year**, or a 15% haircut on contribution. It mattered
> more at 5% (where it halved the business) but it is still free money to pass
> through, and exhibitors already expect it from ticketing.

### Cost

| Item | Per booking |
|---|---|
| SMS — ~8 messages, Canadian rates | **$0.15** |
| Compute / storage marginal | ~$0.00 |
| **Variable cost** | **$0.15** |

### Fixed, per venue per year

| Item | Amount |
|---|---|
| Hosting / infrastructure share | $1,200 |
| Support + account management, ~0.05 FTE at $110K loaded | $5,500 |
| **Facility fixed** | **$6,700** |

### Fixed, company

| Item | Amount |
|---|---|
| Engineering — 2 FTE loaded | $300,000 |
| Ops / support lead — 0.5 FTE | $55,000 |
| Infrastructure baseline, tooling, insurance | $45,000 |
| **Company fixed** | **$400,000** |

---

## 2. Contribution per venue-year

```
Contribution = (bookings × D × t) − (bookings × $0.15) − $6,700
```

| Case | Bookings | Fee `D` | Volume | Marshal @22% | **Contribution** |
|---|---|---|---|---|---|
| **Low** | 3,000 | $120 | $360K | $79,200 | **$71,900** |
| **Mid** | 6,000 | $150 | $900K | $198,000 | **$190,400** |
| **High** | 10,000 | $200 | $2.0M | $440,000 | **$431,800** |

## 3. Take rate — SETTLED at 22% list / 18% design partner

| take | Marshal | facility keeps | contribution | **breakeven** | @10 venues |
|---|---|---|---|---|---|
| 18% (design partner) | $162,000 | $738,000 | $154,400 | **2.6** | $1.14M |
| 20% | $180,000 | $720,000 | $172,400 | 2.3 | $1.32M |
| **22% (list)** | **$198,000** | **$702,000** | **$190,400** | **2.1** | **$1.50M** |
| 25% | $225,000 | $675,000 | $217,400 | 1.8 | $1.77M |

**What 22% actually buys, stated honestly: not de-risking — reinvestment margin.**
Breakeven barely moves (2.6 → 2.1 venues; both are "a handful of design
partners"). **The real gain is $36K/venue-year, or $360K/year at ten venues** —
which is a second engineer, and that compounds.

**Per-booking floor $17.50.** At a $150 fee the rate binds, not the floor — the
floor only engages below a **$79.55** fee. That is exactly its purpose: it
protects the take when a venue discounts off-peak slots to flatten the peak,
which is a thing we actively recommend they do.

**Volume decay to ~18% above $1.5M/yr** at a single venue.

### ⚠ The one cost of 22%: zero headroom

The facility band is **≤20–22% = obvious yes · ~25% = invites a competing bid or
an in-house-build reflex · >30–35% = reads as a landlord on their own asset.**

**22% sits at the top of the safe band.** Two consequences worth accepting
deliberately:

1. **No room to concede.** A venue that pushes back moves you *below* list, so
   the discount needs to be structured in advance rather than improvised
2. **It hands the GSC a number.** D-017 found the nationals are motivated to
   undermine Marshal with the venue — *"that vendor takes 22% of your dock
   revenue"* is an easy sentence to say, and it doesn't need to be fair to work

**The mitigation is the two-tier structure**, not a lower number:

> **22% list. 18% for design partners** — the first venues, who are taking a real
> risk on unproven software. **That is justified rather than conceded**, it
> preserves the anchor, it rewards exactly the venues the hotels-first launch
> depends on, and it means no rate is ever negotiated ad hoc.

**Contractually capped, no unilateral escalation.** A published, consistent rate
is part of infrastructure positioning — a rate that visibly varies by who
negotiated hardest is a vendor's rate, not infrastructure's.

## 4. Breakeven

```
Venues to breakeven = $400,000 company fixed ÷ contribution per venue
```

| Case | Contribution | **Venues to breakeven** |
|---|---|---|
| Low | $71,900 | **5.6** |
| Mid | $190,400 | **2.1** |
| High | $431,800 | **0.9** |

> # 🔴 The finding a CFO cares about
>
> **Raising the take rate did not remove the uncertainty. It moved it into a
> survivable range.**
>
> At 5%, breakeven spanned **4 to 37 venues** — the low case was a different
> company with a different funding requirement, and no rational board commits
> against that. **At 22% it spans roughly 1 to 6.** The spread is still ~6×,
> because it is still driven by two numbers nobody has asked for — but **every
> point in the range is now reachable with a handful of design partners.**
>
> **That robustness is the real argument for 22%, not the extra margin.** We are
> most likely to be wrong about fee and volume; the take rate is the one lever
> that makes being wrong survivable.

**The first dollar still goes to narrowing the range, not to building.** Two
phone calls — *what would you pay for a guaranteed slot* (Q-53) and *how many
vehicles book in per show* (Q-55) — move the decision more than six months of
engineering.

---

## 5. The venue qualification threshold

Solving for a target contribution of **$60,000** per venue-year (enough that
~7 venues clears company fixed with real margin):

```
bookings × D  ≥  ($60,000 + $6,700) ÷ (0.22 − 0.0015/D)   ≈  $305,000
```

> ### The sales qualification rule
> **A venue must generate ≈ $300K+ in annual dock-fee volume to be worth
> serving** — roughly **2,000 bookings/year** at a $150 fee. About 15 shows at
> 135 vehicles, or 30 smaller events at 65.
>
> **At 5% the same test required $800K+.** Raising the rate did not just improve
> unit economics — **it roughly tripled the addressable market**, which matters
> most precisely where the launch strategy points: hotels, where individual
> properties are smaller than convention centres.

**A one-line test a salesperson can apply before spending a week on a venue.**
Below it, the venue consumes support without funding it.

**Multi-property agreements (Q-59) remain the fix for the smallest hotels** — one
implementation across a group's several event properties, sharing facility fixed
cost. Now an optimisation rather than a necessity.

---

## 6. Year-one economics per venue

The implementation fee is what funds the ramp before transaction volume matures.

| Line | Amount | Note |
|---|---|---|
| Implementation fee | **$22,000** | Config, training, workflow design, onboarding |
| Cost to deliver | −$9,100 | ~7 days at $1,300/day loaded |
| **Implementation contribution** | **$12,900** | ≈2.4× cost — profitable, not a loss leader |
| Hardware — cameras, rugged devices, printers, BLE | pass-through | **at cost + 12%** procurement/config margin |
| Transaction contribution, year 1 at 60% adoption | **$114,200** | Mid case, ramping |
| **Year-1 total per venue** | **≈ $127,100** | |
| Year-2+ steady state | **$190,400** | Full adoption |

**Implementation must be priced above cost.** A loss-leader implementation
creates an incentive to under-deliver training, and training is what determines
whether the schedule is actually enforced — which is what determines transaction
volume. **The two are causally linked; price them so they pull the same way.**

---

## 7. Sensitivity — where the model actually breaks

*Ranks computed at the 5% rate; **the ordering is unchanged at 22%**, only the
absolute breakeven numbers shift down.*

| Variable | ±20% swing | Effect on breakeven |
|---|---|---|
| **Fee `D`** | $120 ↔ $180 | **13.7 ↔ 9.1 venues** — *the dominant lever* |
| **Bookings** | 4,800 ↔ 7,200 | **13.9 ↔ 9.0 venues** — *equally dominant* |
| Take rate `t` | 4% ↔ 6% | 14.0 ↔ 8.9 venues |
| Company fixed | $320K ↔ $480K | 8.6 ↔ 12.8 venues |
| Facility fixed | $5,360 ↔ $8,040 | 10.6 ↔ 11.2 venues |
| SMS cost | ±20% | negligible |

**Fee and volume dominate everything else combined.** Cost discipline barely
moves the outcome; **revenue assumptions move it by a factor of three.** That is
an unusual and clarifying result — it says the risk here is commercial, not
operational.

---

## 8. What the exhibitor is actually buying — the model's load-bearing assumption

**They pay something they don't pay today. That only works if it replaces a cost
they already bear.**

| Today, queuing free | With Marshal, $150 slot |
|---|---|
| Driver detention after free time — **$50–100/hr** | Arrive at slot, no wait |
| Miss your target → back of the queue | Slot is held |
| Crew standing idle waiting on freight | Crew called to actual arrival |
| Rescheduling by phone, if at all | Self-serve reschedule |

**A three-hour queue plausibly costs an exhibitor $300+ in detention alone.** At
that level a $150 guaranteed slot is a *saving*, not a new cost — and that is the
only framing under which adoption happens without coercion.

> ### 🔴 Q-58 — the question this model rests on
> **Who currently absorbs the cost of a truck waiting?**
>
> If the **carrier bills detention through to the exhibitor**, the exhibitor
> already bears it and will pay to avoid it. **The model works.**
>
> If it is **absorbed invisibly** — eaten by the carrier, or simply tolerated —
> the exhibitor perceives Marshal as a new fee for something previously free, and
> **adoption fails regardless of how good the software is.**
>
> **This is as important as Q-53 and easier to answer.** One call to a carrier.

---

## 9. Getting the show services companies to adopt

The goal: **GES, Freeman, Shepard and the regional contractors actively want this,
and it costs them nothing.**

### The line that makes it possible

> **Marshal prices dock *time*. Contractors price *handling*. Different
> resources, zero overlap.**

This is why the dock fee is contractually clean where a handling fee would not
be. **The dock is the one resource the venue indisputably owns** — no service
exclusivity covers it (D-002). A facility charging for its own dock does not
compete with a contractor's material-handling billing, and does not cut across
show management's exhibitor relationship.

**Marshal must never price material handling, drayage, or anything a contractor
sells.** That restraint is what makes adoption possible.

### What each party gets, and pays

| Party | Pays | Gets |
|---|---|---|
| **Exhibitor** | The dock fee | A guaranteed slot instead of a queue. **Net saving if detention is real (Q-58)** |
| **Facility** | One-time implementation + hardware | Free platform, higher dock utilisation, more sellable show-days, a safety record, **and the fee revenue** |
| **Show manager** | **Nothing** | Floor visibility, fewer escalations, fewer angry exhibitors |
| **Service contractor** | **Nothing** | Predictable freight arrival, early scope-change warning, **evidence in damage disputes**, reduced crew idle |

### ⭐ The contractor's real incentive is insurance, not efficiency

Efficiency arguments are soft and get discounted. **Insurance is a number on
their P&L.**

A contractor's liability exposure on a show floor is substantial, and their
premium reflects their claims history and their ability to defend a claim.
Marshal produces, as a byproduct of scheduling:

- who moved what, when, **with which certified operator** (D-013 #2)
- which equipment, under what condition checkpoint (D-013 #5)
- an **immutable contention log** showing who held which chokepoint and why (D-014)
- timestamped camera stills at the point of handling

> **After an incident the question is always "what was supposed to be happening
> there?" Nothing on the market can answer it. Marshal answers it by
> construction.**

That is a defensible-claim argument, and a defensible claim is worth real money
to an underwriter. **It is also the same artifact that auto-waives an unfair
penalty (D-015) — one record, three commercial uses.**

→ **Q-60: will an insurer discount a premium against this record?** If yes, it is
the strongest adoption lever in the entire product, and it is a conversation with
a broker rather than an engineering task.

### The adoption sequence

1. **Facility signs** — implementation fee, hardware, keeps the fee revenue
2. **Exhibitors book** because the slot is real and queuing costs them more
3. **Contractors are given a free read-only feed** — arrivals, scope changes,
   the safety record. **No charge, no contract, no lock-in**
4. Contractors begin to *rely* on the feed for crew planning
5. **Contractors start asking other venues for it** — which is the only genuine
   distribution flywheel available in a category the research found has no
   network effects

**Step 3 is deliberately free forever.** The moment Marshal charges a contractor,
it becomes a vendor to be evaluated rather than infrastructure to be assumed.

---

## 10. The CFO recommendation

| # | Decision | Rationale |
|---|---|---|
| **1** | **22% list / 18% design partner, processing passed through** | The facility's alternative is $0, not the fee. **Even the LOW case breaks even at ~6 venues** — robustness, not greed |
| **1b** | **Per-booking floor $17.50; decay to 18% above $1.5M/yr; contractually capped** | The floor protects the take when a venue discounts off-peak, which we actively recommend they do |
| **2** | **Implementation fee $22K, ~2.4× delivery cost** | Funds the ramp; profitable; and it aligns training quality with transaction volume |
| **3** | **Hardware at cost + 12%** | Cover procurement and configuration. **Do not build a hardware business** |
| **4** | **Zero margin on penalties** — processing recovery only | Removes any financial interest in the schedule failing. Governance, not generosity |
| **5** | **Qualify venues at ≥$800K annual fee volume** | One-line sales test. Below it, a venue consumes support without funding it |
| **6** | **Contractors: free, forever, read-only** | It is the distribution mechanism. Charging kills it |
| **7** | **🔴 No capital commitment until Q-53, Q-55 and Q-58 are answered** | Breakeven still spans ~1–6 venues. **That range is the decision, and three phone calls collapse it** |

## Open questions, ranked by financial impact

| # | Question | Impact |
|---|---|---|
| **Q-53** | What will an exhibitor pay for a guaranteed slot? | **Dominant lever** |
| **Q-55** | Bookings per venue-year? | **Equally dominant** |
| **Q-58** | **Who absorbs truck waiting cost today?** | **Binary — the model works or it doesn't** |
| **Q-60** | Will an insurer discount against the safety record? | Strongest adoption lever if yes |
| Q-59 | Can hotel groups be sold as multi-property? | Fixes the small-venue qualification gap |
| Q-56 | Does the venue's organiser contract permit this? | Contractual gate (D-015 Problem 3) |
