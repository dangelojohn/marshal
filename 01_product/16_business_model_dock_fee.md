# The Dock & Marshalling Fee model — analysis

**Source:** owner proposal, 2026-08-06 `[PRIMARY]`

Exhibitors prepay a Dock & Marshalling Fee based on slot time, vehicle type,
weight and dock resources. Off-slot arrival or no-show without rescheduling
triggers a penalty. Marshal.show retains ~5% to cover SMS, payment processing and
infrastructure. **The venue pays no recurring subscription** — only a one-time
implementation fee plus hardware.

> ⚠ **All figures below are illustrative.** No pricing data was gathered — the
> session's search budget is exhausted, and no venue has been asked yet. The
> *structure* of the analysis holds; **every number is a question to ask, not a
> finding.**

---

## Verdict

**The mechanism is right. The take rate is probably wrong, and one dependency
could make the whole thing impermissible.**

---

## 1. ⭐ The genuinely clever part: the fee IS the scheduling mechanism

This deserves to be understood as a **product** decision, not just a revenue one.

The research established that **target move-in times already exist** — GES and
Freeman assign them by zone. They fail because they're published as a static
document nobody revises, and missing yours just sends you to the back of a queue.
There is no consequence, so the time is a suggestion.

The brainstorm round produced an "elevator congestion pricing" candidate and the
adversarial breaker killed it — **no enforcement mechanism.** Soft cost signals
get ignored and the queue reforms.

> **Prepayment plus a priced consequence is the enforcement that was missing.**
> A slot you paid for and can lose money by missing is a real slot.

That is the difference between Marshal producing a schedule and Marshal producing
a schedule **people follow**. Everything else in the product — the solver, the
chokepoint contention, the wall board — is downstream of whether anyone honours
the plan.

## 2. It puts payment where the payer already expects it

Porterly's own analysis, found in the design corpus (D-011), independently
concluded that **exhibitor/event logistics is the side where the payer expects to
pay** — freight is a known, budgeted show cost, unlike guest mail. Exhibitors
already pay drayage, material handling and electrical. **A dock slot fee is a
recognisable line item, not a new imposition.**

## 3. It removes the hardest sale

D-005 identified the venue as the buyer, but venue software budgets are
discretionary and require annual re-justification. **Removing the recurring line
removes that conversation entirely.** The first meeting stops being *"here's a
cost"* and becomes *"here's a revenue stream and an operational fix."*

---

# ⚠ Problem 1 — the economics don't work at 5% gross

**This is the most important finding in this document.**

### Payment processing eats most of the take

| | |
|---|---|
| Illustrative dock fee | **$150** per vehicle |
| Marshal at 5% gross | **$7.50** |
| **Stripe (≈2.9% + $0.30)** | **−$4.65** |
| SMS, ~6 messages/booking | −$0.08 |
| **Net to Marshal** | **≈ $2.77 — about 1.8% of fee volume** |

> **5% gross is really ~2% net.** Payment processing alone consumes over 60% of
> the take before a single server is paid for.

### At venue scale

30 shows/year × 200 exhibitor vehicles × $150 = **$900K fee volume per venue**.
At 5% that's $45K gross, **~$27K net** — per venue, per year, out of which comes
infrastructure, support, security patching, and all ongoing development.

**One venue does not fund a business.** Ten might fund one person.

### Three ways to fix it, in order of preference

1. **Quote the take net of processing.** Marshal takes 5% **plus pass-through of
   payment costs**, so the exhibitor pays $150 + processing. Standard practice in
   ticketing and marketplaces, and it makes the economics honest instead of
   quietly broken.
2. **Raise the rate to 8–10% gross** — still small against a fee the exhibitor
   already expects to pay, and it survives processing costs.
3. **Keep 5% but add a modest recurring support component.** Less elegant, but
   it's what the ongoing costs actually require. See Problem 5.

**Recommended: option 1.** It preserves the "no recurring cost to the venue"
story exactly, and it's a structure exhibitors already recognise from every event
ticket they've bought.

---

# ⚠ Problem 2 — Marshal must never profit from the schedule failing

The penalty is where the margin *looks* attractive. **Do not take it.**

> **If Marshal earns more when exhibitors miss slots, Marshal has a financial
> interest in a schedule that fails.**

That is a governance defect that would be spotted immediately by any venue
counsel, and it corrodes the product's entire premise — Marshal's claim is that
it makes the floor run better.

**The rule: penalty revenue goes to the party who absorbed the cost** — the
venue, or the contractor who staffed a crew for freight that never arrived.
Marshal takes **the same percentage it takes on everything, or nothing at all.**
Never a higher rate on penalties.

### Adjudication is the hard part, and Marshal is unusually well placed

The common dispute is not *"I forgot"*. It is:

> *"I was late because the truck ahead of me was still in the bay."*

**If Marshal or the venue caused the delay, the exhibitor cannot be charged for
it.** Get this wrong once — a venue's own congestion produces a penalty on an
exhibitor — and you lose the venue.

**But Marshal already holds the evidence to decide it automatically:** the
chokepoint contention log (D-014) records *which claim held the bay and why*,
timestamped, with the deciding rule. Add camera stills and movement records and
you can answer *"was the bay available at their slot?"* deterministically.

> **The defensible-record layer built for safety (D-005) turns out to be the
> dispute-resolution engine.** That is a real convergence, not a coincidence —
> both need the same thing: an incontestable account of what actually happened.

**Design requirement: automatic waiver.** If the contention log shows the bay was
occupied at the exhibitor's slot, the penalty is voided **without the exhibitor
having to argue.** Silent fairness is worth more than a good appeals process.

### Language matters

**Not "ticket". Not "fine".** Those imply punitive authority Marshal doesn't
have and invite a fight. **"Rebooking fee"** and **"missed-slot fee"** describe
the same charge as a commercial term, which is what it is. Must be disclosed and
accepted at booking, and — for Quebec — **available in French (Bill 96)**.

---

# 🔴 Problem 3 — this model may not be permitted, and Q-1′ decides

**The gating dependency, still unanswered.**

D-005 §5 established there are **three** billing parties, not two:

```
Facility PROVIDES handling  →  Show management OFTEN BILLS it  →  Exhibitor PAYS
```

**If show management owns the exhibitor billing relationship, Marshal charging
exhibitors directly cuts across an existing commercial contract** — potentially
breaching the venue's own agreement with the show organiser.

This turns Q-1′ from a go-to-market question into a **viability** question:

| If the margin sits with… | Then the model is… |
|---|---|
| **The facility** | ✅ Works as proposed. The venue is the merchant |
| **Show management** | ⚠️ **Sell to show management instead**, or the venue collects and Marshal is just software |
| Split / varies by show | Marshal must support **both** — the merchant of record becomes configuration, not architecture |

> **Do not build the payment layer until Q-1′ is answered.** Build the metering
> and the consumption record (D-010) — those are correct under every outcome.

---

# ⚠ Problem 4 — price the constraint, not the resentment

The proposal prices on *time required and weight allowed*. **Weight is the wrong
primary axis.**

The research found **drayage — priced by certified weight — is the
most-complained-about line in the entire category.** Fern and GES both sell
products designed to escape their own weight-based pricing. Pricing a dock fee by
weight risks inheriting that resentment on day one, for a service that has
nothing to do with drayage.

**Price what you are actually allocating: the dock slot.**

| Axis | Use it? | Why |
|---|---|---|
| **Slot duration** | ⭐ **Primary** | It *is* the scarce resource being reserved. Obviously fair |
| **Vehicle class** | ⭐ **Primary** | A 53' trailer consumes a bay differently from a cube van |
| **Equipment required** | ✅ Secondary | Forklift vs pump truck vs specialised cart — a real cost difference |
| **Peak vs off-peak** | ✅ Secondary | **Spreads load — the pricing does scheduling work** |
| Weight | ⚠️ Only where it changes handling | Not as a headline rate |

**Off-peak discounting deserves emphasis.** It is the one pricing lever that
directly serves the operational goal: cheaper slots at 05:00 and on the second
move-in day flatten the peak that causes the congestion in the first place.

---

# ⚠ Problem 5 — "free" is not free, in two ways

### Nobody values what they didn't pay for

A venue with no recurring cost has no annual moment of *"is this worth it?"* —
which is good for retention and **bad for engagement**. Venues that pay nothing
may not commit staff to training, may not enforce the schedule, and may let the
deployment decay while still nominally "using" Marshal.

**Mitigation: keep the implementation fee substantial.** It isn't only cost
recovery — **it is the commitment device.** A venue that has written a real cheque
shows up to training.

### The costs don't stop when the implementation does

Ongoing, and funded by a thin transaction margin: support, **security patching
(Odoo 16 is outside its support window — D-010 made those patches ours)**,
hardware replacement, and retraining after staff turnover, which in venue
operations is constant.

**Be honest in the model about year-3 economics.** Many "free platform" businesses
quietly introduce a support tier later, which is a far harder conversation than
pricing it correctly at the start.

---

# ⚠ Problem 6 — never hold the money

If Marshal collects from exhibitors and remits to venues, it starts to look like
a **payment facilitator**, with FINTRAC exposure in Canada and
money-transmitter questions in the US.

**Use Stripe Connect with the venue as the connected account.** The exhibitor
pays *the venue*; Stripe splits Marshal's platform fee automatically. **Marshal
never touches or holds funds.** This is the standard marketplace structure, it
sidesteps the regulatory question entirely, and it makes the venue visibly the
merchant — which also helps with Problem 3.

---

# 🔧 One correction to the hardware list

**AirTags are listed for "optional shipment tracking". They will not work for
this** (D-009):

- **No API.** Location exists only in the Find My app — a data source a human must
  look at in another app is not a data source for a headless system
- **Anti-stalking alerts.** Tagged freight moving among hundreds of exhibitor
  staff triggers *"An AirTag is travelling with you"* on their phones, and any of
  them can make your equipment beep. **Selling these to a facility as tracking
  hardware means selling something that will generate support calls and
  complaints in week one.**

**Sell instead: BLE tags + chokepoint gateways** at docks, elevator lobbies and
charging bays — open protocols, a real API, no stranger alerts. And **ask about
forklift telematics first (Q-22)**; it may answer condition and fuel with no new
hardware at all.

The rest of the hardware list is sound. **Reolink is correct and already
integrated.** Rugged devices, label printers and scanners are all real needs.

---

# What to do

| # | Action | Why |
|---|---|---|
| **1** | **Answer Q-1′ before building any payment code** | It determines whether this model is permitted at all |
| **2** | Restructure the take: **5% + processing pass-through** | Fixes the economics without losing the "no recurring cost" story |
| **3** | **Penalties do not enrich Marshal** — same rate or zero | Removes an incentive to want the schedule to fail |
| **4** | **Automatic waiver from the contention log** | The single most important trust feature in the model |
| **5** | Price on **slot duration + vehicle class**, discount off-peak | Prices the constraint; avoids inheriting drayage resentment |
| **6** | **Stripe Connect, venue as merchant** | Marshal never holds funds |
| **7** | Keep the implementation fee substantial | It is the commitment device, not just cost recovery |
| **8** | **Drop AirTags** from the hardware package | They don't do the job |
| **9** | Rename penalties as **rebooking / missed-slot fees**, bilingual | Enforceable commercial terms, not punitive authority |

## Open questions

| # | Question | Why |
|---|---|---|
| **Q-53** | **What would an exhibitor actually pay for a guaranteed dock slot?** | The whole model's viability. Ask alongside Q-8 |
| **Q-54** | Is a no-show fee enforceable on a card-on-file in Ontario and Quebec? | Determines pre-auth vs post-charge, and the disclosure wording |
| **Q-55** | What fraction of slots are missed today? | Sizes both the problem and the penalty revenue — and if it's tiny, the enforcement thesis weakens |
| **Q-56** | Does the venue's contract with show organisers permit third-party exhibitor charges? | The contractual half of Q-1′ |
| Q-57 | Who owns the exhibitor relationship for support when a charge is disputed? | Marshal, venue or show management — decides the support model |
