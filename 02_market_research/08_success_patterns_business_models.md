# Business Models, Go-to-Market, and the Entry Verdict

**Synthesis pass, 2026-08-06.** No new research performed — this file reasons across files 01, 03, 04, 05, 06, 07 already on disk. Tags: **[SOURCED-FROM-CORPUS]** = drawn from a specific finding in those six files. **[INDUSTRY-COMMON]** = general trade knowledge, not independently sourced in this session. **[SPECULATIVE]** = my own inference/synthesis, flagged as such, not a claim any source made.

---

## 1. Business models observed

The category splits into distinct pricing architectures that map almost exactly to who the buyer is and how sticky the relationship already is.

**Per-seat / tiered SaaS (rental companies, SMB venues).** Booqable: $29 / $69 / $149 per month, unlimited inventory, no booking commission. Alert Rental: $200/mo + $1,000 setup (starter) up to $500/mo + $2,500 setup (standard), or an $18,275 one-time perpetual license (Summit tier). Planning Pod: $199–$319/month, priced by concurrent event volume rather than seats. [SOURCED-FROM-CORPUS — files 03, 06]

**Quote-gated enterprise sales (show management, venue, most rental enterprise tiers).** Every vendor in file 05 (Map Your Show, a2z, ExpoCad, Cvent, Swapcard, Expo Logic, Momentus) and most of file 06 (Momentus, EventPro, Artifax, Tripleseat, Event Temple, Skedda) publish zero pricing. Point of Rental, RentalResult, TapGoods, Goodshuffle, ERS, Party Track, Rentopian, and InflatableOffice in file 01 are all quote-gated too — meaning quote-gating is the *default* posture even in the "commodity" rental-software tier, not just the enterprise one. [SOURCED-FROM-CORPUS — files 01, 05, 06]

**Freemium / near-zero floor.** Odoo Rental: free forever (CE), no seat cap. RentMy: free for the first 5 orders. TWICE: an undisclosed but real free tier. [SOURCED-FROM-CORPUS — file 03]

**Perpetual license.** Alert Rental's $18,275 one-time Summit tier is the one confirmed non-subscription option in the whole corpus. [SOURCED-FROM-CORPUS — file 03]

**Payment processing.** Multiple vendors integrate several processors (Stripe, Square, PayJunction, Authorize.net, Braintree) but none in the corpus is shown taking a transaction-level rake beyond normal processor fees — Booqable explicitly advertises "no commission on bookings," which only makes sense as a differentiator if commission-based rev-share is a live alternative model somewhere in the category. [SOURCED-FROM-CORPUS — file 03; commission-model existence is INDUSTRY-COMMON, not directly evidenced]

**Services-attached (the outlier that matters most).** Exposition GSCs — Freeman, GES, Fern, Stronco, Levy — do not sell software at all. Their ordering portals (Expresso, FernOneView, ExpoPortal, and CyberServices before it) are free-to-exhibitor front ends for a business whose actual revenue is drayage billed by certified weight (CWT), labor billed at a union-wage markup, and booth/furniture/carpet rental. [SOURCED-FROM-CORPUS — file 04]

### The price floor, and what it means

File 03 establishes the floor precisely: **Booqable at $29/month, Odoo Rental at $0.** Both offer unlimited inventory and orders. Between them they show that horizontal "manage my rental inventory" SaaS is already priced to the bottom by two credible, well-integrated incumbents — one free-forever and open-source, one venture-backed and cheap. A new entrant competing purely on generic rental-management features has no room to price above the floor and no room to differentiate on feature set either: file 01's comparison table shows near-total feature parity across eight vendors (real-time availability, e-sign contracts, route optimization, QuickBooks integration are table stakes everywhere). **This closes the door on "build another rental-inventory SaaS."** [SOURCED-FROM-CORPUS — file 03]

### The asymmetry that matters most: software as a defended cost center, not a product

This is the single most important business-model fact in the whole study, and it only shows up if you compare files 04 and 06 directly.

For a **GSC**, software is *decoupled* from profit. Expresso, FernOneView, and CyberServices exist to take orders and calculate a surcharge stack — they are not how Freeman or GES make money. The evidence for this is the refresh cadence itself: "innovative" portal relaunches happened in 2009 (Freeman), 2011 (GES), 2018 (Javits), and 2025 (The Expo Group's ExpoPortal, replacing a system that had run over 20 years). [SOURCED-FROM-CORPUS — file 04] A company that actually depended on its software for revenue does not let it run unmodernized for two decades. GES and Fern are now selling *predictability itself* as a paid add-on (Transportation+, 1RATE) rather than fixing the base pricing model — that is a company optimizing around its cost center, not investing in it. [SOURCED-FROM-CORPUS — file 04] The real moat is union labor relationships, warehouses, trucks, and venue-exclusivity contracts (Edlen at 50+ venues, Smart City at 40+) — none of which a software company can code its way into. [SOURCED-FROM-CORPUS — file 04]

For a **venue**, software sits one layer closer to the money. File 06 shows a venue's real optimization targets are space-utilization/gap-filling, exclusive-service revenue capture (F&B, AV, rigging), and turnaround-driven event density — and the booking/scheduling system is the *instrument* that directly enables or leaks that revenue (a hall sitting empty between a Tuesday load-out and Thursday load-in is lost rent that better turnaround modeling recovers). Momentus's own headline framing — "identify schedule gaps, optimize event spaces, fill unused bookings" — confirms the vendor itself sells on this logic. [SOURCED-FROM-CORPUS — file 06] So venue software is a cost center with a *visible, arguable ROI line*, unlike GSC software.

For a **rental company**, software effectively *is* the product — it's the storefront, the availability engine, the contract, the payment rail. That is exactly why this tier is the one that's been commoditized to a $29/free floor: when the software is the whole value proposition, competition drives its price toward zero the fastest.

**[SPECULATIVE synthesis]** This gives three tiers of "how much a category's economics reward better software," from least to most: GSC (software irrelevant to profit, near-zero incentive to invest) → rental company (software is the entire product, therefore commoditized and price-floored) → venue/show-manager (software is instrumentally tied to a real revenue line — utilization, renewal, exclusive-service capture — and therefore the one place a genuinely better product can still move a customer's own P&L, which is also the one place buyers behave like enterprise buyers: quote-gated, demo-led, multi-year).

---

## 2. Who lands first

**Rental company — weakest entry.** Commoditized to the price floor, near-total feature parity, SMB sales cycle with low margin per account. Building here means competing against free (Odoo) and $29/mo (Booqable) with no room to charge more without a real workflow differentiator, and file 01's "what this category is bad at" list (multi-supplier orchestration, venue constraints, labor-rule enforcement) is exactly the kind of complexity a rental-company-first entrant would have to solve alone, for a customer segment that can't pay enough to fund solving it.

**Exhibitor — weakest entry, for a different reason.** Exhibitors have no budget authority (they don't choose the show-management platform or the GSC — the organizer and venue do), no persistent platform relationship (see §3), and are, per file 04's own framing, "the one party forced to touch all of the above" — pure demand-side friction, not a buyer.

**Show manager — strongest transactional entry.** Organizers have real budget authority, an already-normalized quote-gated/demo-led sales motion (file 05 shows zero published pricing across all seven vendors, meaning the category expects and tolerates this motion), and a documented, currently-unsolved integration gap: booth assignment does not travel from the show-management platform to the GSC's ordering portal. GES's Expresso literally has an "I Don't Know" field next to booth number — the exhibitor has to re-supply data the organizer already collected. Even ExpoCad, the one vendor selling into both sides of that seam, doesn't publicly confirm the two products share a live database rather than a common file format. [SOURCED-FROM-CORPUS — file 05] This is a real, bounded, unsolved problem with a clear buyer.

**Venue — best *strategic* entry, especially Canada-first.** Four reasons converge:
1. **Small number of high-leverage relationships.** File 07 lists roughly a dozen major Canadian venues total, several of which couldn't even be reached this research pass (BMO Centre Calgary, RBC Winnipeg, Quebec City, Shaw/Rogers Centre Ottawa domain issues) — meaning direct enterprise relationships with the entire addressable venue set are within reach of a small team, unlike the US market where hundreds of venues exist.
2. **Directly P&L-tied ROI story.** Unlike a GSC pitch (which has no revenue line to point to), a venue pitch has one: gap-filling and turnaround compression are literally "sell more hall-hours," and file 06 identifies a specific, evidenced white space — no enterprise venue platform (Momentus, EventPro, Artifax, Tripleseat, Event Temple, Planning Pod) publicly documents an automated buffer/turnaround primitive; only Skedda has one, and Skedda isn't built for convention-hall complexity. Loading dock scheduling is even more open — none of the nine venue-platform vendors researched name it as a feature at all, and the one point-solution that does (Mobiledock) could not even be reliably fetched, suggesting minimal market presence. [SOURCED-FROM-CORPUS — file 06]
3. **Canada specifically is not locked up.** File 07's market-structure verdict is explicit: fragmented, not consolidated. Ottawa alone runs two flagship venues on two different exclusive GSCs (Stronco at Cohere Centre, GES at Rogers Centre). Vancouver's exclusive-supplier roster (Proshow, Riggit, Promosa, Loungeworks) skips the big national GSC names entirely. No player holds a Canada-wide lock the way Freeman/GES do in large swaths of the US. [SOURCED-FROM-CORPUS — file 07]
4. **A real, dated compliance moat.** Bill 96's software-French deadline already passed (June 2025); Law 25's mandatory privacy-impact-assessment for any cross-border data transfer is a live, current cost for a US-hosted competitor selling into Quebec venues (Palais des congrès de Montréal explicitly gates English content by law). A bilingual, Canadian-hosted platform removes friction competitors are carrying *today*, not friction that might matter eventually — and this argument lands hardest with institutional buyers (venues, organizers), not individual exhibitors or SMB rental shops. [SOURCED-FROM-CORPUS — file 07]

**Recommendation:** enter through the venue, in Canada, on the turnaround/buffer and dock-scheduling gap, then use the venue relationship as a distribution channel into the show managers and GSCs who already have to operate on that venue's floor — closing the seam identified in file 05 as a second wave of the same underlying product, not a separate business. Rental-company and exhibitor entry points are ruled out for the reasons above.

---

## 3. Network effects — real vs imagined

Skepticism is warranted; the corpus does not support most of the network-effect stories this category likes to tell about itself.

**Does an exhibitor carry the platform between shows? No evidence of it, and direct evidence against it.** GES's Expresso portal requires the exhibitor to search for their own booth by company name/booth number every single show, with a "Create One Here" fallback and an "I Don't Know" option next to the booth field. [SOURCED-FROM-CORPUS — file 05] There is no persistent, cross-show exhibitor identity documented anywhere in files 04 or 05. Exhibitor loyalty runs to *the show*, not to whichever GSC or organizer-tech-stack happens to be running it that year. This is the network effect pitch decks assume and the evidence directly contradicts.

**Does a venue pull its contractors? Partially, but it's contract exclusivity, not a network effect.** Edlen (electrical, 50+ venues), Smart City (internet, 40+ venues), Sodexo Live (catering, exclusive at OCCC), and Vancouver's named roster (Proshow/Riggit/Promosa/Loungeworks) are all real, legally-granted exclusivity arrangements. [SOURCED-FROM-CORPUS — file 04, 06] That *is* a genuine lever a venue could pull for a booking platform (mandate its exclusive contractors use the venue's system) — but it's forced adoption by contract, not value compounding with the number of participants, which is what "network effect" actually means. Worth being precise about the distinction: exclusivity ≠ network effect.

**Is there a real two-sided effect anywhere?** The closest candidate is narrow and scoped to a single event, not the platform as a whole: if a platform became the shared system of record that the venue, the organizer, and the GSC all read/write against for one show's booth data, each additional participant genuinely would increase the value of that specific event's data graph (that's what closing the "seam" in §2 would produce). But this is a workflow-level effect bounded to one event, not a platform-wide effect that compounds as unrelated customers join — it does not resemble a marketplace network effect and shouldn't be modeled or pitched as one. [SPECULATIVE, built from file 05's seam analysis]

**Multi-year organizer retention (a2z's "Global HQ," MYS's renewal tooling) is switching-cost-driven, not network-effect-driven** — see §4. It's stored proprietary data (floor plans, renewal priority points) compounding in value *for that one organizer*, not value increasing because other organizers are also on the platform.

---

## 4. Switching costs — what actually locks customers in

The deepest lock-in in this entire corpus is **contractual/relational, not data-driven.**

- **Venue exclusivity contracts** (Edlen, Smart City, Sodexo Live, Vancouver's supplier roster) are the hardest lock in the whole study — they're granted by the venue via multi-year (often public-authority RFP) agreements, and a competitor cannot contract its way past them. [SOURCED-FROM-CORPUS — file 04, 06]
- **GSC appointment by the organizer** is a similar relational lock — CyberServices ran 20+ years not because it was technically sticky but because there was no competitive pressure to displace the business relationship underneath it. [SOURCED-FROM-CORPUS — file 04]
- **Show-management platforms carry real data lock-in**: floor plans reused year over year, renewal/priority-points logic encoded in the sales engine, multi-year portfolio dashboards (a2z's "Global HQ"). This is high-consequence lock-in — ripping it out mid-relationship with major recurring exhibitors risks damaging six- or seven-figure customer relationships — which explains why this tier sells demo-led and quote-gated rather than self-serve. [SOURCED-FROM-CORPUS — file 05]
- **Venue booking software** shows the single strongest tenure claim in the corpus: Momentus's own marketing leans on customers having "kept the system for nearly 30 years." [SOURCED-FROM-CORPUS — file 06] Once a scheduling system is the calendar of record across sales, ops, and finance for an institution, replacing it threatens the institution's operations, not just a software contract.
- **Rental-company SaaS lock-in is the weakest tier** — moderate at most. Several vendors (Planning Pod explicitly) market "dedicated migration specialists" as a sales point, which only makes sense in a category where switching is common enough to need de-risking. [SOURCED-FROM-CORPUS — file 06]

**[SPECULATIVE]** Net: the switching costs that actually protect incumbents in this category are legal/relational (venue exclusivity, GSC appointment), not software-data lock-in — which means a new entrant's realistic path to defensibility is *becoming* one of those relational locks (an exclusive/preferred position with a venue or organizer), not out-featuring an incumbent's data model.

---

## 5. Consolidation signal

Momentus (formerly Ungerboeck) has absorbed VenueOps, Priava, EventBooking, ShoWorks, and RiskSense/WeTrack into one brand — `venueops.com` and `priava.com` now simply redirect into Momentus login pages. [SOURCED-FROM-CORPUS — file 06] Momentive Software now owns both a2z (floor plan/booth sales) and Expo Logic (registration/badging) under one roof. [SOURCED-FROM-CORPUS — file 05]

**What it says about where value accrues:** Momentus's own stated differentiator is explicitly "sheer market consolidation" — breadth across convention centers, arenas, performing arts, and universities — rather than a differentiated product mechanic. [SOURCED-FROM-CORPUS — file 06] Value in this category is accruing to whoever owns the *logo count and account inertia* at the system-of-record layer, not to whoever has the best individual feature. This tracks with the switching-cost finding in §4: once you're the 30-year incumbent, breadth and inertia are the product.

**Does it open or close the window?** Both, cleanly split by segment:
- **Closes** the "build a better VenueOps/Priava clone and get bought" lane. That lane now has one dominant, deeply entrenched player with 30-year retention claims and 85%+ of the largest convention centers as customers [VENDOR claim per file 06]. Going head-on against Momentus for an entrenched large-venue relationship is not a fight a new entrant wins on product alone.
- **Opens** two things. First, the *un-integrated seams inside the roll-up itself*: file 05 explicitly notes there's "no evidence yet" that a2z and Expo Logic — same parent, since 2025 — are actually wired together. Consolidators buy logos faster than they integrate workflows; that lag is real market opening even within their own customer base. Second, the *segments and geographies the roll-up hasn't reached*: the GSC–organizer seam (§2), loading-dock scheduling, and — per file 07 — the Canadian market specifically, which remains structurally fragmented with no Freeman/GES/Momentus-style lock.

---

## 6. Seasonality

Events cluster hard by season — trade-show calendars concentrate spring/fall, wedding/event-rental demand peaks summer, and Canada's outdoor season is further compressed by climate relative to warmer US markets. [INDUSTRY-COMMON]

**Effect on rental-company SaaS pricing:** flat monthly subscriptions (Booqable $29–149/mo) bill a seasonal business at a non-seasonal cadence — a real cash-flow mismatch for the customer. This is almost certainly why Alert Rental structures around setup fees + lower recurring cost, and why a perpetual-license option ($18,275 one-time, Alert's Summit tier) persists at all: some buyers would rather take one capex hit than carry fixed opex through an off-season. [SOURCED-FROM-CORPUS — file 03]

**Effect on show-management/venue pricing:** smoother, because the *buyer* is an aggregator. A single organizer or venue runs many events across a full calendar — which is exactly why a2z markets a "Global HQ" multi-show portfolio dashboard: cross-show, cross-season visibility is a genuine buyer need, not a nice-to-have. [SOURCED-FROM-CORPUS — file 05] Selling to the aggregator (venue, multi-show organizer) rather than the single event or single rental company is structurally the better seasonality hedge for a vendor's own revenue too.

**[SPECULATIVE] Implication for a new entrant:** avoid pure per-event or per-transaction pricing unless explicitly serving an aggregator; prefer a hybrid (small recurring platform fee + event-linked usage) so the vendor's own revenue isn't as seasonal as any one customer's cash flow; anchor contracts to the customer's own event calendar rather than the calendar year. On the cost side, GSCs manage seasonality with variable union labor pools rather than fixed headcount — the same lesson applies to any entrant considering a services-attached model: keep labor variable, not fixed.

---

## 7. The "one throat to choke" dynamic

This is a real, structural preference, not a soft cultural quirk, and it explains a lot of category behavior that would otherwise look irrational. GSCs bundle eight-plus service lines — booth, furniture, carpet, signage, drayage, electrical/rigging where not venue-exclusive, labor, AV — under a single appointment even though the margins across those lines surely vary widely. [SOURCED-FROM-CORPUS — file 04] The bundling isn't primarily an upsell tactic; it's what the organizer is actually buying: one accountable party when something breaks at show time.

**Implication for a minimal-surface product:** this cuts hard against a fragmented point-solution strategy. File 05 already shows exhibitors juggling 3+ logins per event (show-management portal, GSC ordering portal, sometimes a separate venue-exclusive utilities portal) — that fragmentation is a documented pain point, not a template to imitate. A minimal-surface entrant has two viable postures, and only two:

1. **Be invisible infrastructure the incumbent licenses or white-labels** — the organizer still has exactly one throat to choke (the GSC or the venue), and never has to manage the new vendor directly.
2. **Go deep on one clearly-bounded, currently-unowned seam** (booth-assignment handoff, dock scheduling, turnaround/buffer) that *removes* a manual step from an existing relationship rather than *adding* a new vendor relationship to manage.

A minimal-surface product that shows up as "one more login" in an already-fragmented stack will hit exactly the resistance this dynamic predicts.

---

## 8. What kills entrants here

- **Operational complexity, unbounded.** Ten distinct service types (file 04's list — booth, furniture, carpet, signage, drayage, electrical, rigging, internet, labor, freight), each with jurisdiction-specific labor rules, weight-based surcharge stacks, and advance/floor deadline structures. Trying to model all of it before shipping is a boil-the-ocean trap.
- **Long sales cycles misjudged.** Quote-gated pricing across nearly every vendor in files 01, 05, and 06 signals enterprise, multi-stakeholder, often RFP-driven procurement — several Canadian venues in file 07 weren't even reachable by a simple web fetch, which is itself a signal of how procurement-gated this buyer class is. A team sized for SMB SaaS sales cycles will misjudge burn if it assumes the same motion works on venues or show managers.
- **Incumbents own the labor and the trucks.** The GSC segment's real moat is union labor relationships, warehouses, and trucking — assets no amount of good software replicates. This is why "disrupt drayage with software" specifically is implausible (§1).
- **Customisation drowning.** EventPro's "assemble what you need" modularity, RentalResult's ERP integrations (CMiC, SAP, Oracle, JD Edwards), Artifax's finance/ticketing integration depth — once you sell mid-market-and-up, bespoke integration work multiplies per customer. Without a strong platform/API architecture, a thin team gets pulled into professional-services work that quietly destroys SaaS unit economics.
- **Exclusivity as a hard structural wall, not just competitive pressure.** A new entrant cannot contract its way into a venue's exclusive electrical/internet/catering slot — that's granted by the venue, often through a years-long public-authority RFP cycle, not a sales call.
- **Buyer numbness to bad software.** CyberServices ran 20+ years; Ungerboeck/Momentus markets 30-year retention as a *selling point*. This category's buyers tolerate mediocre tools far longer than typical SaaS churn models assume — "our UX is better" is a much weaker wedge here than in most verticals, because urgency to switch is chronically low.

---

## 8 patterns to copy

1. **Segment the pricing model to the buyer's switching cost, don't pick one motion category-wide.** Quote-gated/demo-led for high-switching-cost enterprise buyers (show mgmt, venue); transparent self-serve floor pricing for low-switching-cost SMB (rental). The corpus shows every successful vendor already does this — mixing the two motions on the wrong segment is the mistake, not the pattern.
2. **Bundle to be the one throat to choke**, not a point tool — GSCs bundling 8+ service lines under a single appointment is the direct evidence (§7).
3. **Monetize predictability as a paid add-on**, not just capacity — Fern's 1RATE and GES's Transportation+ both sell certainty against the base pricing model's own complexity; any entrant with a complex pricing surface (dock scheduling, turnaround) can copy this directly.
4. **Build the portfolio/multi-event aggregation view early** — a2z's "Global HQ" simultaneously drives retention (§4) and hedges seasonality (§6) for the same reason: it's the single feature that serves a repeat professional buyer's actual unit of work (their whole calendar, not one event).
5. **Use a generous free/low floor as a funnel, not the business.** Odoo's free-forever tier and RentMy's first-5-orders-free both function as acquisition, with real revenue expected higher up-market — copy the funnel shape, not the price point.
6. **Name the mechanic.** Skedda's "buffer time" turns a vague operational concept ("setup/teardown") into a discrete, demoable, sellable feature — even though Skedda isn't built for full convention-hall complexity, the naming pattern itself is what makes a pain point marketable.
7. **De-risk switching-in explicitly**, not just lock-in after the fact — Planning Pod's "dedicated migration specialists" is a direct wedge against entrenched incumbents' switching-cost advantage (§4).
8. **Earn trust by narrowing, then position as a complement, not a replacement.** Texada explicitly frames itself as designed to "complement existing ERP systems, not replace" them; Artifax (40 years, arts/culture only), Alert Rental (50 years, event/party since 1976) show the same logic — extreme vertical narrowness plus a non-threatening posture toward the incumbent stack is what builds buyer trust in this category, not horizontal breadth.

## 5 traps that kill entrants

1. **Boiling the ocean** on service-type and jurisdiction modeling (10 service types × union/right-to-work variation × CWT pricing × advance/floor deadlines) before shipping anything.
2. **Applying SMB sales-cycle economics to enterprise buyers** — venues and show managers are RFP-driven, multi-year, multi-stakeholder; running a $29/mo self-serve funnel playbook against them burns runway for nothing.
3. **Competing with exclusivity instead of routing around it** — no software product out-bids a 50-venue electrical exclusivity contract or a legally-granted GSC appointment.
4. **Becoming one more login** in an already 3-login-per-exhibitor stack — adding vendor-relationship overhead in a category that structurally wants fewer throats to choke, not more (§7).
5. **Sliding into bespoke professional services per deal** until the company is functionally a systems integrator carrying SaaS-company cost structure without SaaS-company margins.

---

## Entry verdict

**The case that software alone loses:** GSC economics prove software is a defended cost center, not a product — the incumbents' real moat is union labor, warehouses, and trucks, none of which code replicates. Venue exclusivity (Edlen, Smart City, Sodexo Live) is a legal wall a software company cannot out-compete. Consolidation (Momentus absorbing five brands, Momentive pairing a2z with Expo Logic) shows scale and account inertia beating product depth. And buyers in this category tolerate genuinely bad software for 20-30 years — CyberServices, Ungerboeck/Momentus's own retention pitch — so "we built something better" does not, by itself, create switching urgency. A pure-software entrant that plans to out-compete Freeman, GES, or Momentus on their own ground loses.

**The case that a layer/infrastructure play wins:** the "seam" between show-management platforms and GSC ordering portals is real, unsolved, and doesn't require owning labor or trucks — it requires being the data layer both sides already have to touch, and even the one vendor positioned on both sides (ExpoCad) doesn't confirm it's actually solved. Loading dock scheduling is a genuine, evidenced, currently near-abandoned gap (served, if at all, by a niche vendor that couldn't even be reliably fetched). Canada specifically is fragmented rather than locked, has a dated regulatory moat (Bill 96/Law 25) that favors a bilingual Canadian-hosted platform, and has a small enough venue set (~a dozen) for direct relationships to be realistic. And the consolidators are proven integration-lazy — a2z and Expo Logic sharing a parent since 2025 with no evidence of actual product integration is the clearest tell that roll-ups buy logos faster than they close seams, which is exactly the opening a smaller player can exploit.

**Verdict:** Do not build a rental-company SaaS — that lane is commoditized to $0–$29/mo by Odoo and Booqable with no differentiation runway. Do not attempt to become or displace a GSC — that requires owning labor and trucks, which is not a software company's game. Enter as a **layer**: build the connective tissue nobody in this corpus has built — booth/venue-assignment data continuity, turnaround/buffer modeling, and dock scheduling — sell it first to Canadian venues (small reachable set, direct P&L-tied ROI, real compliance moat, no incumbent lock), and let the venue relationship pull in the show managers and GSCs who already have to operate on that floor. Win by being the thing incumbents are relieved to integrate with — reinforcing the "one throat to choke" dynamic instead of fighting it — not by trying to out-truck or out-labor companies that have been doing this for 50-70 years.
