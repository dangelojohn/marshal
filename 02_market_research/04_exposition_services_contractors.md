# Exposition Services Contractors — The Real Incumbents

**Research date:** 2026-08-06
**Method:** Live WebFetch against vendor sites, venue sites, and trade press. WebSearch was unavailable/exhausted for this session — every fact below came from direct URL fetches. Failures are logged honestly at the end so gaps aren't mistaken for "nothing there."

**Tagging key:** [SOURCED] = confirmed via a live fetch of a primary/vendor/venue/press page today. [VENDOR] = from a company's own marketing copy (self-interested framing, treat claims about "solving" pain points skeptically). [INDUSTRY-COMMON] = widely known/standard industry practice, but not independently re-verified today (search tool unavailable, direct sourcing attempts failed). [UNVERIFIED] = plausible but I could not confirm it in this session. [SPECULATIVE] = my inference/analysis, not a claim of fact.

---

## 1. What a general service contractor (GSC) actually does

A GSC is the prime contractor for a trade show's physical build-out. Confirmed service lines, pulled directly from GSC sites today:

- **Exhibit rental / custom exhibits** — Freeman "Exhibit Rentals," GES "Custom & Turnkey Exhibit Rentals," GES's Spiro subsidiary for custom builds [SOURCED — freeman.com, ges.com]
- **Graphics/signage production** — banners, hanging signs, directional graphics (Freeman) [SOURCED]
- **Furniture** [SOURCED — freeman.com]
- **AV/production** — LED, lighting, digital displays, sound (Freeman "Exhibit AV"); Encore operates as a standalone AV-and-more full-service contractor, now folded together with exhibit builder Hargrove ("Hargrove from Encore") [SOURCED — freeman.com, encoreglobal.com]
- **Material handling / drayage** — GES bundles it into exhibit rental packages and also sells it standalone via "GES Transportation+"; Fern has a branded flat-rate product, "1RATE" [SOURCED — ges.com, fernexpo.com]
- **Shipping & freight / logistics** — Freeman Transportation®, GES Shipping & Logistics (round-trip, inbound-only, outbound-only, domestic/international) [SOURCED]
- **Labor (I&D — installation & dismantle)** — GES bundles "Professional Labor" with rentals; Fern has a dedicated "Labor Management" service line [SOURCED — ges.com, fernexpo.com]
- **Electrical, plumbing, rigging, internet/telecom, cleaning** — [INDUSTRY-COMMON] standard GSC/venue catalogue items; GSC marketing pages I could reach (Freeman's exhibitor-services page) notably did **not** list these explicitly — they were absent from the page content, which itself is a finding (see §7). Confirmed as real line items indirectly via venue-side sourcing: McCormick Place's official service contractors employ union "carpenters, electricians, plumbers, riggers, decorators, projectionists, stagehands, teamsters" [SOURCED — mccormickplace.com]
- **Lead retrieval** — [INDUSTRY-COMMON] standard catalogue item across the industry; not found explicitly on any page fetched today — likely sold via a separate registration/tech vendor bundled into the show, not always a core GSC line.

**Structural note:** the "GSC" and "exhibit builder" categories are not the same, and vendors are blurring them. Czarnowski (now "Czarnowski Collective," czarco.com) explicitly positions itself as an exhibit/experiential design-and-build agency, *not* a GSC — no material handling, electrical, or ordering-portal function on its site [SOURCED]. Nth Degree is a labor/project-management holding company whose portfolio includes Fern Expo (a true GSC) and INVNT (event production) — i.e., what looks like "one company" in the market is often a holding-company roll-up of formerly independent, differently-scoped businesses [SOURCED — nthdegree.com].

---

## 2. The exhibitor ordering experience

This is the core UX of the category, and it is materially the same shape across every vendor:

1. **Log in to a proprietary portal**, tied to a specific show. GES's portal is **Expresso** (ordering.ges.com): exhibitors authenticate as an "Authorized User," verify email (MFA optional), then search for their booth by **Company Name, Booth Number, or Customer Number**. If the booth isn't listed, the exhibitor manually creates it (name, booth number, width/depth). Billing is either "Exhibitor Billing" (invoice to the exhibiting company) or "Third Party Billing" (invoice to a hired vendor) [SOURCED — ordering.ges.com].
2. **Freeman's equivalent is "Find Show & Order"** at freemanco.com/store — functionally the same pattern (find your show → order products/services online), though I could not get past a 503/cert error to see the live UI today [SOURCED nav existence; UNVERIFIED live UI].
3. **Fern's is FernOneView** (fernoneview.com) — returned 403 today so I couldn't inspect it directly [UNVERIFIED beyond name/URL — fernexpo.com nav].
4. **Orange County Convention Center runs its own venue-level ordering portal for utilities and aerial rigging on Ungerboeck** (`occc.ungerboeck.net/prod/app85.cshtml?AppCode=COE...`) — i.e., some venue-exclusive services are ordered on a *different* system than the GSC's own portal, so a single exhibitor may need two or three separate logins for one booth [SOURCED — occc.net]. This directly evidences the fragmentation problem described in §7.
5. **The Expo Group just replaced a 20+-year-old system called "CyberServices"** with a new unified portal, **ExpoPortal**, in 2025 — merging "ecommerce and traditional exhibitor service manual information into a cohesive experience with one simple exhibitor login," adding persona-based onboarding (first-time vs. repeat exhibitor), a task-progress bar, a "dimensional, interactive booth configurator," and a dashboard of ordered items [SOURCED — exhibitcitynews.com, theexpogroup.com]. The fact that a 20+-year-old system was still in production until 2025 is itself the strongest direct evidence found this session of how old the category's software actually is.
6. **Advance vs. floor (show-site) pricing**: I could not pull an exact rate card today (vendor marketing pages don't publish them; a live show's exhibitor kit PDF would be needed and none were reachable without search). But the mechanism is confirmed structurally: GES's "Transportation+" product is explicitly framed around avoiding penalty costs — "avoid costly after-hour or carrier wait time charges," "10% off material handling, free weight certificate, no carrier wait time fees" for shipments ≤5,000 lbs [SOURCED — ges.com]. This confirms the underlying pricing architecture (base rate + a stack of surcharges for missing deadlines/off-hours/uncertified weight) exists and that vendors are now selling *insurance products against their own surcharge structure* — a strong signal of how punitive the default pricing is perceived to be. The advance-rate/floor-rate deadline split itself is [INDUSTRY-COMMON] — universal in every published exhibitor service manual — but I could not source a specific dollar figure or specific deadline window live today.

---

## 3. The show manager's side

Direct sourcing here was thin — GSC marketing sites gate this content behind sales contact forms rather than publishing it. What I could confirm:

- GES has a distinct organizer-facing product line separate from its exhibitor line: "Show Planning," "Operational Excellence," "Sponsorship Consulting," "Exhibitor Success," "Experiential Strategy," listed as top-level nav categories under "Organizers" [SOURCED — ges.com].
- The exhibitor service manual (ESM) — the document/portal that encodes what's included, deadlines, and floor-plan rules — is confirmed to exist as a named artifact (The Expo Group explicitly describes merging "ecommerce and traditional exhibitor service manual information") [SOURCED].
- Floor plan approval, reporting dashboards for show management, and deadline-setting mechanics specifically from the *organizer's* console were not reachable today — no organizer-side login/demo content was surfaced by any vendor site. [UNVERIFIED / gap]

---

## 4. The facility's side — exclusivity is the single biggest structural fact in this category

Confirmed directly from two convention centers today:

**Orange County Convention Center (OCCC)** publishes named exclusive "Planner Service Partners":
- Catering → **Sodexo Live** (exclusive)
- Audio/Visual → **LMG** (exclusive)
- Internet/Telecom/Wi-Fi → **Smart City** (exclusive)
- Shipping & Print/Business Center → **FedEx Office** (exclusive)
- Utilities and aerial rigging ordered through a separate venue-run Ungerboeck portal
[SOURCED — occc.net]

**McCormick Place** runs internet/telecom **in-house** via its own "Technology Services Department" and "Communication Service Technicians" — not even outsourced to a specialty vendor, fully venue-owned — while electrical, plumbing, rigging, carpentry, projection, staging, teamster, and cleaning labor all run through union "Event Service Contractors" [SOURCED — mccormickplace.com].

**Smart City Networks** (the OCCC internet exclusive) operates in 40+ convention/meeting facilities nationally and frames itself as running "partnership agreements" rather than "exclusive monopoly contracts" — but functionally, at any single venue, an exhibitor cannot bring an alternate internet provider [SOURCED/VENDOR — smartcitynetworks.com self-description softens the word "exclusive" even while the practical effect is exclusivity].

**Edlen Electrical** self-describes as "the nation's leading temporary utility contractor to the trade show, convention, and special event industry," serving 5,000+ events/year across 50+ venues (Mandalay Bay, MGM Grand, LA, Miami, Chicago, San Diego, SF, Denver, Atlanta, etc.) — a *separate* exclusive electrical provider that operates independently of (not owned by) the GSC running the floor [SOURCED — edlen.com]. Their site does not itself use the word "exclusive" to describe venue arrangements, so the exclusivity mechanism specifically (single-source contract vs. preferred-vendor) is [INDUSTRY-COMMON] knowledge, not confirmed in Edlen's own language today.

**Why this matters structurally:** a single trade show floor routinely has 3-5 *different, non-substitutable* vendors for different service categories — the GSC (booth/furniture/carpet/material handling/labor), the venue-exclusive electrical (e.g., Edlen at many venues), the venue-exclusive internet/telecom (e.g., Smart City), the venue-exclusive or venue-in-house rigging, and a venue-exclusive caterer (e.g., Sodexo Live at OCCC) — each with **its own ordering flow, deadline schedule, and invoice**. An exhibitor ordering "everything" for one 10x10 booth may need 3+ separate logins/portals and 3+ separate bills. No new entrant can contract this away; exclusivity is granted by the venue (often a public authority) via long-term contract, not by the GSC.

---

## 5. Material handling / drayage — the most complained-about, most profitable line

**Pricing basis:** billed by weight, per hundredweight (CWT), on the *certified* weight of the shipment **including crates, pallets, and packing materials** — not just the goods [SOURCED — fernexpo.com]. This is why "shipping a box of 300 buttons directly to the venue" can cost dramatically more than the same box shipped to an office — the CWT minimum and packaging weight dominate small/light shipments [SOURCED — Exhibit City News, "Shop to Showfloor: Alleviating the Nightmare of Drayage Charges," Jan 14 2020].

**Traditional cost structure** stacks a base per-CWT rate with variable add-ons: overtime, warehouse handling, "special handling" (loose/uncrated freight, multiple-piece shipments), and marshalling fees — which is exactly what exhibitors object to. Direct quote from Fern's own page describing the *problem* it says it solves: "exhibitors struggled to make sense out of the unpredictability of the cost of material handling" [SOURCED/VENDOR — fernexpo.com].

**Two vendor responses confirmed today, both telling:**
- **Fern's "1RATE"** — a single flat per-pound rate with no minimums and explicitly "no overtime, warehouse, special handling, or marshalling fees" [SOURCED/VENDOR — fernexpo.com]
- **GES "Transportation+"** — 10% off material handling, free weight certificate, no carrier wait-time fees, for round-trip domestic shipments ≤5,000 lbs [SOURCED/VENDOR — ges.com]

Both are essentially "buy your way out of our own surcharge structure" products — strong evidence that the underlying default pricing is opaque and punitive enough that vendors now monetize *predictability itself* as an add-on rather than fixing the base product.

**Advance warehouse vs. direct-to-show**: advance shipments go to a warehouse pre-event for smoother, better-timed delivery; direct-to-show arrives during a scheduled move-in window requiring tight carrier coordination — missing that window is a common source of extra fees [SOURCED — fernexpo.com].

**Exhibit City News documents a sustained, multi-year pattern of exhibitor complaints**, not a one-off gripe:
- "Demystifying Exorbitant Material Handling Rates and The Truth Behind It" (Sept 5 2017) — "moving your company's booth properties several hundred feet cost more than shipping it from overseas"
- "Traditional Material Handling Rates Out of Control?" (Aug 22 2018) — material handling called "the most misunderstood line item on their trade show invoice"
- "Shop to Showfloor: Alleviating the Nightmare of Drayage Charges" (Jan 14 2020)
- "The Price of Presence" (Feb 4 2026) — booth program costs "roughly doubled post-pandemic," "every part of the tradeshow budget, from drayage to rigging, feels heavier"
[SOURCED — exhibitcitynews.com search results]

**Why exhibitors hate it, synthesized:** it's charged on a unit (weight incl. packaging) the exhibitor doesn't fully control, priced with minimums that punish small shipments, layered with situational surcharges (overtime/special handling/marshalling) that are hard to predict in advance, and — because it's usually GSC- or venue-exclusive — there's no competitive alternative to shop against. [SPECULATIVE synthesis of the above sourced facts, not itself a quoted claim.]

**Business-model implication** — drayage/material handling is widely described in the industry as the GSC's highest-margin line [INDUSTRY-COMMON / could not independently verify a specific margin percentage today — no source with actual P&L data was reachable]. The fact that two major GSCs are now marketing flat-rate/discount alternatives specifically for material handling (and not, say, for furniture or carpet) is circumstantial support that it's the line under the most competitive/reputational pressure. [SPECULATIVE]

---

## 6. Labour rules — union jurisdiction, what exhibitors can/can't do, right-to-work variation

**McCormick Place gives the clearest concrete rule set found this session** [SOURCED — mccormickplace.com]:

*Exhibitors MAY do themselves:*
- Hand-carry small packages and pop-up booths
- Hang signs without tools or ladders, if it takes under 30 minutes
- Skirt tables with custom-fit skirts (no staples, snaps, or Velcro)
- Hand-carry computers and small appliances

*Requires union/official labor:*
- Any electrical work drawing from building systems
- Plumbing installation
- Machinery handling/positioning
- Equipment projection/staging
- Drape, fabric, or Velcro sign installation that requires tools
- Crate removal involving power equipment or restraint tools

This is a real, cited jurisdictional rule set from one major venue — and it's a good proxy for the shape of rules everywhere, but the specific thresholds (e.g., "30 minutes," "no tools") are McCormick-Place-specific, not universal. [SOURCED for McCormick Place specifically; INDUSTRY-COMMON that every major venue has an equivalent but differently-worded list.]

**Fern's own labor-management page confirms the general pattern without giving specifics:** "What exhibitors may do themselves depends on local labor rules," varying "by city, venue, and jurisdiction"; union/official labor is required for certain tasks "to comply with local labor agreements, maintain safety standards, protect exhibitors and organizers from risk" [SOURCED/VENDOR — fernexpo.com]. Fern explicitly claims it "clearly communicates" the do/don't list per show but the page itself gives no task breakdown — meaning even a GSC's own marketing treats this as too complex/variable to state generically. [SOURCED that the vagueness exists; SPECULATIVE on why.]

**Right-to-work variation**: this is a well-known industry reality (right-to-work states like Texas, Nevada, Florida, Georgia generally impose fewer union-labor mandates and allow more self-install by exhibitors and non-union I&D houses, versus heavily unionized markets like Chicago/McCormick Place, New York/Javits, and parts of California) — but **I could not independently verify this with a live source today**; direct attempts (Javits Center site 403, ESCA glossary unreadable, targeted press searches on Exhibit City News returned no matching articles) all failed. **Flag this explicitly as [INDUSTRY-COMMON / UNVERIFIED THIS SESSION]** — it's near-universally cited in the industry but I do not have a fresh citation for it.

---

## 7. Technology posture — service companies with a portal bolted on, not tech companies

This is the best-evidenced section of the research, because the *dates* of "launch" announcements tell the story on their own:

- **Freeman** announced "enhanced online ordering," calling it "the industry's first truly integrated platform" — in **2009** [SOURCED — Exhibit City News search result].
- **GES** "launches self-service web platform" — in **2011** [SOURCED — Exhibit City News search result].
- **Javits Center** launched its online ordering system, branded "Jake" — in **2018** [SOURCED — Exhibit City News search result].
- **The Expo Group** ran on a system called **CyberServices for over 20 years**, only replacing it with ExpoPortal in **2025** [SOURCED — Exhibit City News, theexpogroup.com].
- The back-end venue/show-management software underlying much of the industry is **Ungerboeck**, which rebranded to **Momentus Technologies** (gomomentus.com). Momentus's own marketing says clients have "kept" the system for "nearly 30 years" — i.e., the vendor's own pitch leans on multi-decade customer retention of what is, by any definition, a legacy enterprise platform now wrapped in an "AI-powered" and "cloud" marketing layer [SOURCED — gomomentus.com self-description]. Momentus claims 85%+ of the largest global convention centers as clients [SOURCED/VENDOR claim, unverified against an independent count].
- **GES's exhibitor ordering portal (Expresso)** requires per-show login, manual booth lookup/creation, and separate exhibitor vs. third-party billing flows — a transactional order-form UX, not a modern self-service commerce experience [SOURCED — ordering.ges.com].
- **OCCC runs venue-exclusive utility/rigging orders on a raw Ungerboeck app URL** (`occc.ungerboeck.net/prod/app85.cshtml?AppCode=COE...`) — a URL structure that is itself evidence of an old, unmodernized enterprise app, separate from whatever portal the GSC on that floor is running [SOURCED — occc.net].

**Conclusion, directly supported by the above:** these are service/logistics companies that have periodically bolted e-commerce ordering onto decades-old back-end systems, roughly once a decade (2009 → 2011 → 2018 → 2025 relaunch cycles). None of the major players (Freeman, GES, Fern) publishes a modern developer-facing API, real-time floor-status dashboard, or mobile-native ordering flow anywhere discoverable from their public marketing sites today — and where I could reach an actual portal (GES Expresso), the interaction model is 2010s-era enterprise web-forms, not modern consumer-grade commerce. [SOURCED facts above; the synthesis/conclusion sentence is SPECULATIVE but directly built from those facts.] I was blocked from directly testing Freeman's live store (503/cert errors) and Fern's live portal (403) today, so I cannot personally confirm their current UI quality — this is a gap, not a claim they're fine. [UNVERIFIED / explicit gap.]

---

## 8. Business model & margins

- Base contract: the GSC is typically appointed by show management as the official/exclusive contractor for a given event, giving it first claim on furniture/carpet/signage/booth-rental spend across the whole floor. [INDUSTRY-COMMON]
- Material handling/drayage is widely regarded as the highest-margin, most profit-critical line (see §5) — [INDUSTRY-COMMON, could not independently verify a specific margin figure this session].
- Labor is a pass-through-plus-markup model: the GSC bills union labor hours at a marked-up rate versus what it pays the union hall. [INDUSTRY-COMMON, not independently sourced today.]
- Exclusivity elsewhere on the floor (venue-exclusive electrical/internet/rigging/catering, §4) means those revenue pools largely bypass the GSC entirely and go to Edlen, Smart City, Sodexo Live, etc. — so "the GSC's margin" is only part of the total exhibitor spend on a show floor; the rest is captured by venue-contracted specialists under completely separate economics. [SPECULATIVE synthesis from §4 facts.]
- Roll-up/consolidation is visible in the vendor landscape itself: Nth Degree owns Fern Expo + INVNT; Encore and Hargrove have merged branding ("Hargrove from Encore"); Brede Exposition Services shut down permanently in August 2020 (a COVID casualty) [SOURCED — brede.com closure notice]; Czarnowski rebranded as "Czarnowski Collective." This is a consolidating, thinning field, not a stable set of independent competitors. [SOURCED facts; consolidation-trend framing is SPECULATIVE interpretation.]

---

## Where the incumbents are weak

1. **Fragmented multi-portal ordering** — a single booth can require separate logins across the GSC's own portal, a venue-exclusive utilities/rigging portal (e.g., OCCC's raw Ungerboeck app), a venue-exclusive internet/telecom vendor, and a venue-exclusive caterer — each with its own account, deadlines, and invoice. [SOURCED — occc.net structure]
2. **Decade-scale technology refresh cycles** — major "innovative" portal relaunches happened in 2009, 2011, 2018, and 2025; The Expo Group ran a 20+-year-old system (CyberServices) until 2025. This is not a fast-iterating software category. [SOURCED — Exhibit City News dates]
3. **Legacy back-end dependency** — much of the venue/show-management layer runs on Ungerboeck/Momentus, a platform whose own vendor markets nearly-30-year customer tenure as a selling point. [SOURCED — gomomentus.com]
4. **Opaque, punitive drayage pricing** — CWT-based billing on certified weight including packaging, stacked with overtime/special-handling/marshalling surcharges, has generated a *sustained, multi-year* stream of trade-press complaint articles (2017, 2018, 2020, 2026) — this is not a one-time PR problem, it's chronic. [SOURCED — Exhibit City News]
5. **Vendors are monetizing predictability as an add-on rather than fixing the base product** — Fern's 1RATE and GES's Transportation+ both exist specifically to let exhibitors pay extra to avoid the base pricing model's own surcharges. That's a tell that the default product is broken by design, not by accident. [SPECULATIVE interpretation of SOURCED facts]
6. **Deadline-driven advance/floor pricing** creates a structural incentive to rush-order early rather than plan accurately — confirmed as the underlying mechanism via the Transportation+/1RATE "avoid surcharges" framing, though I could not source an exact current rate table today. [SOURCED mechanism; UNVERIFIED specific numbers]
7. **Marketing sites actively withhold operational detail** — pricing, deadlines, and even basic service lists (electrical, plumbing, rigging were absent from Freeman's own exhibitor-services page) are gated behind a sales-contact flow rather than published. This is a service-company posture (relationship/sales-led), not a tech-company posture (self-serve/transparent). [SOURCED — freeman.com page content gaps, observed directly]
8. **No evidence of real-time floor visibility or mobile-native tooling** was found anywhere in vendor marketing today — not necessarily proof it doesn't exist, but proof it isn't being marketed as a differentiator, which is itself telling for a category this mature. [UNVERIFIED / absence-of-evidence, flagged as a gap not a confirmed weakness]

---

## The 10 service types a new platform MUST model

1. Booth/exhibit rental (structures, walls, custom builds)
2. Furniture rental
3. Carpet/flooring
4. Signage & graphics production
5. Material handling / drayage (CWT-based, advance-warehouse vs. direct-to-show)
6. Electrical & power distribution (often venue-exclusive, separate vendor)
7. Rigging (often venue-exclusive/union)
8. Internet/telecom/Wi-Fi (often venue-exclusive)
9. Labor (I&D — installation & dismantle, union-jurisdiction-aware)
10. Shipping & freight/logistics (inbound/outbound, domestic/international, advance vs. direct)

(Plumbing, cleaning, AV, and lead retrieval are real and common but were less consistently surfaced as standalone platform-level service objects in today's research — treat as a secondary tier, not because they're unimportant, but because they were either bundled into the above [AV inside "exhibit rental" packages] or venue/vendor-specific enough [catering, cleaning] to need per-venue modeling anyway.)

## The 5 structural facts any entrant must respect or fail

1. **Exclusivity is granted by the venue, not the GSC, and it's real** — electrical (e.g., Edlen at 50+ venues), internet/telecom (e.g., Smart City at 40+ venues, or venue-in-house as at McCormick Place), rigging, and catering (e.g., Sodexo Live at OCCC) are routinely single-source per venue. A platform cannot "disrupt" this by offering a competing vendor inside that venue — it has to integrate with/route to the incumbent exclusive provider. [SOURCED — occc.net, mccormickplace.com, edlen.com, smartcitynetworks.com]
2. **Drayage is priced by certified weight (CWT) including packaging, not by the goods alone**, and carries deadline- and condition-dependent surcharges (overtime, special handling, marshalling). Any platform must model weight certification, advance-warehouse vs. direct-to-show routing, and a surcharge stack — not a flat rental-style price. [SOURCED — fernexpo.com, ges.com]
3. **Labor is jurisdiction-specific and union-governed at most major venues**, with explicit, narrow carve-outs for what an exhibitor may do by hand (McCormick Place: hand-carry, sub-30-minute tool-free sign hanging, custom table skirts) versus what requires paid union labor (anything touching building electrical/plumbing, machinery, tools). This varies by city/venue and reportedly by right-to-work status of the state [INDUSTRY-COMMON/UNVERIFIED THIS SESSION on the right-to-work point specifically]. A platform must be venue-aware on labor rules, not apply one national policy.
4. **Advance-rate vs. floor-rate deadline pricing is the pricing spine of the entire category** — ordering ahead of a published cutoff is cheaper than ordering at show-site, across material handling, labor, and most services. A platform must have first-class deadline/cutoff modeling, not just a price list. [SOURCED mechanism via GES Transportation+/Fern 1RATE framing; specific numbers UNVERIFIED today]
5. **The buying unit is the show, not the booth or the vendor** — exhibitors order against a specific event's exhibitor service manual/portal, tied to booth number and show dates, often needing 2-3 separate logins (GSC + venue-exclusive utility + venue-exclusive internet). A platform that assumes a single continuous vendor relationship (like generic party rental) will not match how this category actually transacts. [SOURCED — ordering.ges.com booth-lookup flow, occc.net multi-portal structure]

---

## Sources fetched today (successes)

freeman.com (homepage, /how-we-help/, /event-services/exhibitor-services/) · ges.com (homepage, /exhibitor/, /exhibitor/shipping-logistics/) · ordering.ges.com (Expresso portal) · shepardes.com (homepage) · fernexpo.com (homepage, /services/material-handling/, /services/labor-management/) · encoreglobal.com · czarco.com (Czarnowski redirect) · nthdegree.com · mccormickplace.com · occc.net · edlen.com · smartcitynetworks.com · gomomentus.com (Ungerboeck rebrand) · esca.org · exhibitcitynews.com (search results ×3) · theexpogroup.com · brede.com (closure notice)

## Sources attempted and failed (honest log)

- freeman.com/how-we-help/exhibitors/, /how-we-help/facility-partners/material-handling/, /how-we-help/exhibitor-services/, /store/ → 404 / 503 / cert mismatch (freemanco.com cert doesn't cover bare domain)
- ges.com/exhibitors → 404 (correct path was /exhibitor/, singular)
- shepardes.com/exhibitors/ → 404
- fernoneview.com (Fern's ordering portal) → 403 Forbidden
- hargrove-inc.com, viadexperience.com → DNS resolution failure (domains likely wrong/defunct — Hargrove is now folded under encoreglobal.com)
- brede.com deeper service pages → company confirmed permanently closed Aug 14, 2020; only closure notice retrievable
- oceccenter.com → DNS failure (correct domain is occc.net, not oceccenter.com)
- exhibitoronline.com → 403 Forbidden
- lvcva.com/facilities/las-vegas-convention-center/exhibitor-services/ → 404
- javitscenter.com → 403 Forbidden
- iaee.com glossary → returned unreadable binary/PNG content, not text
- tsnn.com → reachable but no relevant articles surfaced on homepage; would need working search
- g2.com GES Expresso reviews → 403 Forbidden

These gaps mean: I do not have independently confirmed current pricing/rate-card figures, no direct read on Freeman's or Fern's live ordering-portal UI quality, no organizer/show-manager-side console walkthrough, and no fresh (this-session) citation for the right-to-work labor variation claim despite it being standard industry knowledge.
