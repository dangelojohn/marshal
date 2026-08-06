# Round 2 — GSCs, organisers, EACs

**Status:** agent output + my flags. **The most strategically important finding
of the session is in here.**

---

# ⭐⭐ The single most important fact

> **GSC blocking power: 7/10 at a convention centre. 2/10 at a hotel.**

At a convention centre the GSC is embedded via multi-year official-contractor
agreements, controls the union labour relationship, and organisers often choose
venues partly on GSC continuity. **A top-3 national threatening non-cooperation
is a credible commercial threat even though the dock is legally the facility's
asset.**

**At a hotel there is usually no GSC at all** — a decorator hired directly by the
meeting planner handles much lighter freight. **The leverage evaporates.**

**This independently confirms hotels-first (Q-6) from a completely different
direction than I'd argued.** I said hotels because the constraints are worse, the
tooling thinner and the relationships already exist. **The real reason is that
the party most able to kill Marshal isn't in the building.**

---

# 🔴 GSCs LOSE — 6/10, and they are the most dangerous stakeholder

Operational gains are real but outweighed by a structural threat they will
eventually name correctly: **Marshal disintermediates a function they already
perform** — the GSC's freight team frequently runs the yard in practice, even
though the facility owns the asset in theory.

**Their gain, quantified (low confidence):** a 10–20 person material-handling
crew idle 1–2 hours at a blended union rate of ~$50–90/hr is **$1,000–3,000 per
incident**, plausibly tens of thousands per large show. Real money to an ops
director; **not enough to change their strategic calculus.**

### 🔴 The real reason they'd fight — the exhibitor budget conflict, not pride

> *"The exhibitor doesn't do resource accounting. They see two bills for one
> truck — a new dock fee from the venue on top of our material handling invoice —
> and they blame us for the total, not you."*

Freight is already the most-resented line in exhibiting. A venue dock fee gets
bucketed into *"what it cost me to get my stuff to the booth"*, regardless of the
correct conceptual distinction between **paying for a time slot** and **paying
for handling labour**.

The chain: exhibitors push back on total freight spend → hand-carry more, ship
less, consolidate → **GSC billable tonnage softens** → organisers use *"exhibitors
are complaining about cost"* as renewal leverage on GSC contracts.

**Why this is dangerous: it's three or four steps removed and nearly impossible
to prove either way.** The anecdote — *"tonnage's been down since that venue put
in the dock fee"* — **will circulate in GSC leadership long before anyone has
rigorous numbers, and the anecdote alone is enough to trigger lobbying.**

> ### ⭐ The counter-move: instrument CWT/tonnage trends at pilot venues from day one
> **Do not let the anecdote get a two-year head start on the evidence.**

### 🔴 Correction to my recommendation: "free read-only forever" is NOT enough

I recommended contractors get a free read-only feed forever. **For the top-3
nationals that is table stakes, not a concession.** It removes the *"why would I
subsidise the tool replacing me"* objection and does nothing about the two that
matter — loss of operational control, and the margin threat above.

**Minimum credible package for the nationals:**
1. **API write-access** — their freight system stays the operational layer rather
   than a bystander
2. **Co-branding on exhibitor-facing scheduling and invoice touchpoints** — so it
   doesn't read as the venue going around them
3. **Modest revenue share or data fee, funded from Marshal's take, never their
   margin.** The amount matters less than the shift from *rival* to *vendor*

**Explicitly NOT a governance seat in product design** — that risks the GSC
re-capturing the exact coordination inefficiency Marshal exists to remove.
Structured input on the API surface is cheap and useful; a veto is not.

*Smaller regional GSCs with no legacy tech investment likely accept free-forever
alone. The nationals will not.*

### GSC-as-customer: a separate SKU, not a pivot
White-label the engine to the GSC as a yard-management tool they pay for and
brand. More aligned with where large shows already sit operationally, and it
sidesteps the turf fight — **but it means building GES Expresso 2.0 and selling
into the incumbent whose sunk investment is the stated threat.** You'd inherit
their procurement cycle and lose the *"neutral venue infrastructure trusted by
everyone including rival GSCs and EACs on the same floor"* positioning.
**Dual-track as a wedge for un-penetrated venues. Not a substitute.**

---

# Show management — WINS 6/10, blocking power 2/10

Wins on the metric that drives their model: exhibitor satisfaction and renewal.
Plus a real-time ground-truth freight feed they've never had — **today they take
the GSC's word for it** — and neutral third-party evidence in the blame-shifting
that follows a bad move-in.

**They don't bill material handling directly** (they typically take a rebate on
GSC service revenue), so the dock fee is a separate ledger on paper. **But it
lands in the same psychological bucket for the exhibitor and the same
cost-of-exhibiting number in the organiser's own sales pitch.**

**Danger is soft but amplifying:** non-endorsement in the exhibitor service kit,
or lending credibility to a GSC-driven junk-fee narrative.

**Fix: hand them the dashboard and the marketing language proactively, before a
GSC or a competing venue frames it for them first.**

---

# EACs — WINS barely, 4/10, and the variance is the story

**Average is the least meaningful number here.** Sophisticated repeat EACs score
7–8; thin one-truck operators score 3–4 — **and there are more of the latter.**

Structurally they win: they are the least-trusted, least-powerful party on the
floor, routinely deprioritised at the dock and blamed by parties with an
incentive to deflect. **A timestamped, camera-verified record is the closest
thing to due process they have ever had at a loading dock.**

**But a rigid slot system also removes the informal safety valve** — today a
friendly dock foreman sometimes squeezes a small operator back into the queue.
Net positive, but a real trade rather than a pure upgrade.

> ### ⚠ The penalty lands hardest on those least able to absorb it
> *"I'm a three-person shop doing five cities this month. I don't have a
> dispatcher watching a scheduling app, and if I'm forty minutes late because the
> last job ran long, I don't want a rebooking fee and a four-hour wait bolted onto
> a booth build I'm already racing to finish overnight."*

**This is both an ethics problem and a political vulnerability** — it's the
segment most likely to trigger the penalty, least able to pay it, and their
anecdotes feed the junk-fee narrative that endangers organiser support.

**Fixes that push them to 8+:** a **30–45 minute grace window** before any
rebooking fee · mobile-only check-in with no back-office requirement · a
**waiver/discount tier for single-truck operators** · **standby-slot access from
cancellations** — turning the system from another paywall into the fairest queue
this segment has ever had.

---

# Kill-risk ranking and what to do about #1

1. **GSCs (top-3 nationals)** — real blocking power at convention centres, a
   direct P&L motive, existing yard control, and the relationships to lobby or
   slow-walk
2. **Organisers** — low direct power, but GSC lobbying plus a junk-fee narrative
   tips them from neutral to quietly discouraging
3. **EACs** — negligible; structurally a winner class with no organising capacity

## The GSC playbook

- **Sequence around the blocking-power split.** Launch in hotels and GSC-thin
  venues. Build reference cases with real numbers — on-time move-in rates,
  damage-dispute resolution speed, idle-cost reduction — **before the fight
  starts.** Never approach a flagship GSC-embedded convention centre first
- **Approach the nationals proactively as partners**, with the
  API/co-brand/revenue-share package in hand, **before they discover Marshal live
  in a venue they operate**
- **Defuse the billing perception explicitly** — unified or co-presented invoice,
  plain-language messaging tested with real exhibitors: *"this reserves your
  truck's arrival time — it is not material handling."* Where true, position the
  dock fee as **reducing** the GSC's own overtime and delay billing, which makes
  it pro-GSC messaging rather than adjacent-fee messaging
- **Lead with liability and insurance, not scheduling efficiency** — the immutable
  record is a provable saver on their own cargo/liability exposure. **It maps to
  their P&L rather than their pride**
- **Instrument tonnage from day one**
