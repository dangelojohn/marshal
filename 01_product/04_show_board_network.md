# The Show Board — a shared capacity network

**Origin:** owner insight, 2026-08-06. Captured as a design concept, not a
decision.

> "One major difficulty show managers have is finding a centralised and
> synchronised venue list of shows across venues… if the auto show at MTCC
> changes size, capacity could open up for other automotive-motivated show
> managers. It's more efficient for show managers and venues, and then GES /
> Freeman in the middle aren't left struggling to adapt."

---

## 1. What this actually is

**Venue space-time is perishable inventory with no channel layer.**

An empty hall-day is revenue that can never be recovered — structurally
identical to an unsold airline seat or hotel room night. Both of those
industries built distribution layers decades ago: global distribution systems
for airlines, channel managers for hotels.

**Exhibition space has no equivalent.** Booking happens through relationships,
phone calls and long-cycle contracts. When a show contracts, the freed space is
known to three parties — the organiser, the venue, and eventually the service
contractor — and reaches nobody else in time to be useful.

This is a genuine structural gap, not a feature request.

## 2. Why the adjacency example matters

The auto-show example contains the real product. It isn't "list all venues" —
it's **match freed capacity to demand that fits it**.

An automotive show shrinking by 30,000 sq ft in February is interesting to a
show with an automotive-adjacent audience, similar exhibitor base, and a
compatible date window. It is worthless to a medical device conference.

So the core capability is **matching and notification**, not a directory:

- semantic adjacency between show profiles (audience, exhibitor overlap, sector)
- date-window compatibility, including move-in/move-out feasibility
- physical fit — hall size, ceiling height, floor loading, dock access
- and the honest constraint nobody models: **can the freed slot actually be
  serviced?** Freed space with no available labour or dock capacity is not a
  real opportunity

That is genuinely agentic work — ranking and notifying under uncertainty — as
distinct from the deterministic scheduling in the main specification.

## 3. Why it doesn't already exist

Worth being unsentimental about this. The idea is not novel; the obstacles are
what stopped it.

| Obstacle | Severity |
|---|---|
| **Venues treat their booking calendar as commercially sensitive** — publishing it reveals utilisation weakness to competing venues | High |
| **Show dates are strategic** — a competitor could counter-programme | High |
| **A shrinking show is bad news** the organiser doesn't want broadcast | High |
| **Cold start** — no value until many venues participate | High |
| **Asymmetric willingness to pay** — venues won't pay to advertise their gaps; show managers would pay but have thinner budgets | High |
| **Slow signal** — shows book two to five years out, so churn is infrequent | Medium |

**Any version that asks venues to publish their calendar will fail.** That is
the design constraint, and it kills the naive version of this idea.

## 4. The reframe that makes it buildable

> **Don't sync calendars. Publish gaps.**

A venue posting *"Hall C, 40,000 sq ft, 3–9 March 2027, available"* reveals
almost nothing strategic — it is an offer, not a disclosure. It's a **load
board**, not a shared calendar.

Freight solved exactly this problem the same way. Carriers and shippers are
fiercely private about capacity and rates, yet load boards work — because
participants reveal **asymmetrically and late**: you post the lane when you want
it filled, not your whole operation.

Everything follows from that inversion:

- Venues opt in **per gap**, not per calendar
- A gap can be **anonymised** until a qualified enquiry arrives ("a downtown
  Toronto facility, 40k sq ft, early March")
- No obligation, no exclusivity, no exposure of what *didn't* get posted
- Withdrawal is free

## 5. The sequencing insight — this is the important part

A cold-start marketplace is a hard business. But **the workflow product in the
main specification generates this data as a byproduct.**

If we are already running turnaround and dock scheduling for a venue, we
**know their gaps without asking them to publish anything.** The venue doesn't
supply a feed; the feed is a derivative of work they were already doing in the
tool.

> **Come for the turnaround scheduling. Stay for the network.**

That resolves the cold-start problem, and it means the network is defensible in
a way the workflow tool alone is not — the workflow tool can be copied; the
accumulated gap history and adjacency graph cannot.

It also matters because the competitor research concluded network effects in
this category are **largely absent** — exhibitors don't carry platforms between
shows, and venue "pull" on contractors is contract exclusivity rather than a
compounding effect. **This would be the only genuine network effect in the
market.**

## 6. Who actually pays — probably not who you'd guess

The owner's framing contains the answer: *"GES / Freeman in the middle aren't
left struggling to adapt."*

**The service contractor is the party most damaged by late notice.** They staff
crews, book trucks, and stage material against a floor plan. A show contracting
20% two months out is directly expensive to them — and they typically learn late
because the information reaches them last.

That suggests three revenue lines with different characteristics:

| Payer | Product | Willingness |
|---|---|---|
| **Service contractor** | Early-warning feed on scope change at shows they service | **Highest** — quantifiable cost avoided |
| Show manager | Matched opportunity alerts for adjacent freed capacity | Medium — real value, thinner budget |
| Venue | Gap fill / reduced dark days | Medium — high value but resistant to paying to advertise weakness |

**The counter-intuitive conclusion: the contractor may be the best customer for
the network, while the venue is the best customer for the workflow tool.** They
are different sales, and the contractor sale is *easier* because the cost of
late notice is already on their books.

Notably this also makes the contractors **allies rather than competitors** —
consistent with the main specification's position that we route around their
moat rather than attack it.

## 7. The risk that needs real advice, not engineering

**Competitor information exchange is an antitrust-sensitive activity.**

A platform where competing venues see each other's availability, pricing
signals, or utilisation could be characterised as facilitating coordination —
regardless of intent. This is a genuine legal question in both Canada and the
US, not a theoretical one.

Mitigations that are likely necessary, and must be reviewed by counsel rather
than designed by us:

- **No pricing data on the network.** Availability only. Rates negotiate offline
- **No aggregate utilisation visibility** between venues
- **No historical calendar** — only currently-offered gaps
- Anonymised listings until an enquiry qualifies
- Possibly: only *show managers* see gaps; venues never see other venues

**Get an opinion before building this.** It is cheaper than redesigning it
later, and the constraint shapes the data model.

## 8. What would have to be true

1. **Enough venues in the workflow tool** to make derived gaps meaningful — this
   is why sequencing after the main specification matters
2. **Gap posting is genuinely low-risk** for a venue, or they will not do it
3. **Adjacency matching is good enough to be useful** — a feed of irrelevant
   opportunities is worse than none
4. **Counsel confirms** the information-exchange model is defensible
5. **A contractor will pay for early warning** — the cheapest hypothesis to test,
   and testable with a phone call rather than a build

## 9. Where this sits relative to the main spec

**Not Phase 0. Probably not Phase 1.**

It is the **Phase 5+ payoff** that makes the earlier phases strategically
valuable rather than merely useful. Build the workflow tool because it stands
alone; design the data model so the network becomes possible without a
migration.

Concretely, that means the main specification's `floor.window`, `floor.space`
and `floor.show` records should carry the fields a gap listing would need — hall
dimensions, dock access, serviceability, and a show-profile descriptor for
adjacency — **from the first version**, even though nothing consumes them yet.

That is a near-free decision now and an expensive retrofit later.
