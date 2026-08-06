# AV / Production / Staging Rental Software

## Why this category matters more than the others

Party/event rental software (see `01_event_party_rental_software.md`) treats scheduling as an
inventory-availability problem: is the item free on that date? AV/production rental cannot get
away with that. A single touring show or broadcast job requires equipment *and* crew *and*
transport to all be free in the same window, with prep and strike time bracketing the show date,
sub-rentals filling gaps, and hundreds of serialized/bulk items exploding out of "package"
templates. This is the closest existing category to what an agentic scheduler for events needs to
out-plan. Tag legend: **[SOURCED]** = confirmed this session from the vendor's own site.
**[VENDOR]** = vendor's own marketing claim, stated as a claim not a verified fact.
**[INDUSTRY-COMMON]** = widely repeated in the category, not confirmed from a primary source this
session. **[UNVERIFIED]** = could not confirm; included because it's a commonly-asked question.
**[SPECULATIVE]** = my inference, flagged as such. **[FETCH-FAILED]** = the vendor's own site (and
fallbacks) refused or returned nothing this session; noted rather than invented.

---

## 1. Rentman

**Site:** rentman.io — homepage, pricing, and 8 sub-pages fetched successfully via its sitemap.

1. **Scheduling engine** — [SOURCED] Built around a central equipment-availability view: "See all
   available and rented equipment," "Get real-time equipment availabilities," "Allocate gear
   across jobs." Explicit conflict language: "Prevent double bookings and shortages" with
   "warning signals when there are shortages." [SOURCED] Sub-rental is a first-class shortage
   resolution path: "Solve equipment shortages with alternatives and subrentals," and multi-
   warehouse shortages can be solved by "subrent[ing] equipment from your other stock locations."
   [VENDOR] No dedicated Gantt-chart terminology was found in the fetched marketing copy (the
   product is known industry-wide to use a timeline/planning-board view, but I could not confirm
   the exact UI paradigm from vendor text this session — [UNVERIFIED]). No explicit prep/transit-
   buffer time modeling or kit/package "explosion" language was found in the pages fetched
   [UNVERIFIED — may exist in-product but isn't in the marketing copy].
2. **Crew/labour** — [SOURCED] Crew profiles store "work history, reputation, rates,
   qualifications, and certified skills," and planners can "filter crew based on the needed
   skills or expertise, and assign suitable crew members to job functions." Crew can self-serve:
   "Schedule crew members, or let them sign up for jobs." [SOURCED] Conflict detection is named
   directly: "Spot shortages & double bookings."
3. **Multi-warehouse / multi-location** — [SOURCED] Dedicated feature: "Manage equipment stored
   in multiple warehouses or storage locations," with per-location filtering and cross-location
   scheduling ("Schedule equipment from multiple locations to events in a few clicks"). Priced as
   an add-on: €5/warehouse/month.
4. **Job/project structure** — [VENDOR] Marketing language centers on "jobs" and "events" as the
   scheduling unit; no explicit quote → job → sub-job/phase hierarchy was described in the pages
   fetched [UNVERIFIED].
5. **Customer-facing surface** — [UNVERIFIED] Not found in the pages fetched this session.
6. **Integrations & extensibility** — [SOURCED] Zapier, QuickBooks, Xero, a "Routetitan"
   integration for delivery route optimization, and a documented custom API. No API docs URL was
   found in the sitemap [UNVERIFIED on API depth/quality].
7. **Pricing model** — [SOURCED] **Published**, modular: €39/month platform fee + per-power-user
   module pricing (Inventory €14–19, Crew €14–24, Enterprise Crew quote-gated), add-ons
   (Quoting & Invoicing €9, History Logs €12, Equipment Tracking €9, extra warehouse €5), all
   per power-user/month; "basic" execution-only users are free. Capterra lists a $39/mo flat-rate
   starting price and a 4.6/5 rating across 243 reviews [SOURCED via Capterra category page].
8. **What it does differently** — [VENDOR] Positions itself as "built by people with decades of
   experience in the AV & event industry" with human-staffed global support rather than
   ticket-bot support, and a granular à-la-carte pricing model rare in this category (competitors
   mostly quote-gate everything).
9. **Why customers choose it / leave it** — [SPECULATIVE] Choose: transparent/modular pricing,
   strong inventory+crew combo, active European base. Leave: [UNVERIFIED] — no churn/complaint
   data was surfaced in the pages fetched.

---

## 2. Current RMS

**Site:** current-rms.com — homepage, pricing, warehouse-management, crewing-module blog post,
shortage-alerts feature page, and extended-scheduler feature page fetched successfully.

1. **Scheduling engine** — [SOURCED] The core view is an "Interactive Resource Planner" — a
   drag-and-drop board with **color-coded status tiles: blue = unallocated, green = confirmed,
   red = booked out**. This is a real three-state planning ladder (open → assigned → confirmed),
   not just a binary booked/free flag. [SOURCED] **Shortage detection is a soft-warning system,
   not a hard block**: shortages surface as an exclamation-mark badge on the Opportunities list,
   red line items in the order detail view, and a dashboard tile ("Upcoming orders with
   shortages") — the system lets you keep booking into a shortage and flags it rather than
   stopping you. [SOURCED] A genuinely notable feature: the **"Extended Service Item Schedule"**
   lets a single service line item be broken into **named sub-phases with their own date/time
   windows — Prep, Travel, Setup, In Use** — i.e. explicit prep/transit/buffer modeling attached
   to the booking itself, toggled on in Opportunity Settings.
2. **Crew/labour** — [SOURCED] Crew is one resource type inside a general "Services Module"
   covering "crew, transport, venues or rooms" uniformly — the same Resource Planner used for
   equipment is reused for people/vehicles/rooms. Users can "specify periods of unavailability"
   and get an iCal feed per resource. [UNVERIFIED] No skills-matching, certification, or
   union/overtime language was found in the pages fetched — crew allocation appears to be
   availability-only, not competency-matched.
3. **Multi-warehouse / multi-location** — [SOURCED] Warehouse workflow: prep → check-out →
   check-in with barcode/QR scanning, temporary containers (flight cases) vs permanent containers
   (fixed assets that travel together), and a "Global Check-in" that reconciles assets across
   multiple jobs in one pass. [SOURCED] Kit/package explosion exists: "Build kits and packages of
   your gear ensuring certain products go out together, such as wireless mic packs, tent
   packages, or camera kits." [SOURCED] Sub-rental is explicit: "Mark products as sub-rented if
   it's a product you don't own, or if you have a shortage."
4. **Job/project structure** — [SOURCED] The unit is an "Opportunity" (quote → order →
   invoice lifecycle), with templates ("Opportunity Templates") and cloning ("Clone/copy-paste
   opportunity groups") for repeatable job structures.
5. **Customer-facing surface** — [UNVERIFIED] Document-approval workflow for project documents
   was referenced in the feature list, implying some client-facing approval step, but no
   dedicated "portal" product was confirmed in the pages fetched.
6. **Integrations & extensibility** — [SOURCED] Open/documented API ("current-rms-open-api"),
   Xero, QuickBooks, Sage, HubSpot data sync, WooCommerce, PatGuard Cloud (PAT testing), Adobe
   Sign, MailChimp — one of the broader confirmed integration lists in this category.
7. **Pricing model** — [SOURCED] **Published, per-user, currency-localized**: first user
   $79/£59/€69 per month, additional users $49/£39/€49 per month, unlimited features on every
   tier (no feature-gating by plan), 30-day free trial, no card required.
8. **What it does differently** — [VENDOR/SOURCED] Genuinely distinctive: (a) shortages as a
   **visible warning, never a hard stop**, and (b) sub-phase time-blocking (Prep/Travel/Setup/In
   Use) on individual line items rather than only at the job level. Flat, all-features-included
   pricing is also atypical for the category (most competitors reserve advanced modules for
   higher tiers).
9. **Why customers choose it / leave it** — [SPECULATIVE] Choose: UK/EU mid-market fit,
   transparent pricing, unified resource model (equipment+crew+transport+rooms in one planner).
   Leave: [UNVERIFIED] — no confirmed complaint data this session; the "all resources on one
   generic planner" design is a plausible source of friction for crews wanting skills/cert
   matching that the fetched pages don't show as present.

---

## 3. Flex Rental Solutions

**Site:** flexrentalsolutions.com — homepage, inventory-management, StaffingPlus, and
plan-pricing pages fetched successfully via its sitemap.

1. **Scheduling engine** — [SOURCED] "A unified view of inventory across all active jobs and
   warehouses," showing committed / available / in-transit states simultaneously. [SOURCED]
   **Explicit dual-mode serialized+bulk tracking**: "Flex tracks both [serialized and bulk] in
   the same kits and pull sheets" — this is the clearest, most direct vendor confirmation of
   serialized-vs-bulk handling found across all vendors researched. [SOURCED] Kit/package
   explosion is confirmed: "Build reusable kits, pack containers, and link accessories
   automatically" so "every job leaves the warehouse complete." [SOURCED] Conflict detection is
   named directly: "Live availability and conflict detection… prevent double-booking & missed
   items." [SOURCED] Execution layer: auto-generated pull sheets and batch scanning at
   load-out. [UNVERIFIED] No explicit prep/transit/buffer time *configuration* language was found
   (as distinct from Current RMS's explicit sub-phase scheduler) — Flex's time modeling appears
   to live at the job level, not the line-item level, based on what was fetched.
2. **Crew/labour** — [SOURCED] Separate paid module, **Flex StaffingPlus**: skills-based
   availability inquiries sent to multiple freelancers at once, one-click job offers on
   confirmation, per-freelancer call/end times feeding auto-generated daily call sheets, real-time
   response notifications, and a **Gantt view for staffing** ("Load any job into Flex
   StaffingPlus that requires staffing resources with Gantt view"). [UNVERIFIED] No
   certification-tracking, overtime-calculation, or union-rule language found.
3. **Multi-warehouse / multi-location** — [SOURCED] Explicitly priced and supported: additional
   locations are $150/mo (2nd), $100/mo each (3rd–5th), $75/mo each (6th+) — a rare case of a
   vendor pricing multi-location depth in public tiers rather than quote-gating it.
4. **Job/project structure** — [UNVERIFIED] Not detailed in pages fetched beyond "jobs" as the
   scheduling unit; Flex Asset Solutions / Flex GTS appear to be separate verticalized products
   (K-12, medical, church, local-business asset management) built on the same platform, suggesting
   a multi-tenant/vertical product strategy rather than sub-job phases within one job.
5. **Customer-facing surface** — [SOURCED] E-signature (DocuSign) and Flex Payments for
   client-facing quote approval/payment; no dedicated self-service portal product was confirmed.
6. **Integrations & extensibility** — [SOURCED] QuickBooks (paid add-on, $50/mo), DocuSign, Flex
   Payments, and "API for custom needs" — API depth/docs not confirmed publicly.
7. **Pricing model** — [SOURCED] **Published**: base plan from $510/month with **unlimited
   users included** (a genuine differentiator vs. per-seat competitors), 30-day trial, itemized
   add-on pricing (RFID $100/mo, StaffingPlus $100/mo, custom reports $240/hr, training
   $165/hr).
8. **What it does differently** — [VENDOR/SOURCED] Positions itself explicitly against
   "simplified" competitors: "industrial-strength capabilities" for touring/broadcast-scale
   operations rather than a general SMB tool, 15+ years on "high-stakes productions," and
   unlimited users baked into the base price rather than sold per seat.
9. **Why customers choose it / leave it** — [SPECULATIVE] Choose: proven at large-scale touring
   /broadcast/award-show scale [VENDOR claim], unlimited users economics for large crews. Leave:
   [SPECULATIVE] $510/mo floor plus per-location/per-module add-ons likely prices out small
   shops — this is a top-of-market product, not an entry-level one.

---

## 4. HireHop

**Site:** hirehop.com — **[FETCH-FAILED]**. Every attempt this session (root domain, `www` and
bare, `/index.php`, `/features.php`, `/tour.php`) returned **HTTP 403**, consistent with active
bot-blocking (likely Cloudflare) rather than the pages not existing. `docs.hirehop.com` had no DNS
record. Wayback Machine (`web.archive.org`) is blocked entirely in this environment. G2, TrustRadius,
and two Capterra product-slug guesses for HireHop all returned 403/404. A DuckDuckGo HTML search
hit a CAPTCHA wall; a Bing HTML search returned unrelated cached content (not usable). I could not
retrieve a single first- or third-party page with real HireHop content this session.
**Everything below is [UNVERIFIED]** — reported, not invented, per instructions:
- [UNVERIFIED] Widely known in the category as a UK-founded, relatively low-cost/high-feature
  competitor with a generous free tier for very small operators, a diary/calendar scheduling view,
  and its own CRM/accounting layer (Xero/QuickBooks/Sage integrations commonly cited).
- [UNVERIFIED] Frequently cited in industry discussion as one of the more aggressively-priced
  full-feature options, which is the closest thing to a "differentiator" I can report without a
  primary source. **This claim should be independently verified before use** — it could not be
  confirmed this session.

---

## 5. RTPro (Rental Tracker Pro)

**Site:** rentaltrackerpro.com — **[FETCH-FAILED]**. The root domain and `/index.html` returned
empty page bodies twice (the fetch tool explicitly reported no text content, not a network error —
consistent with a JavaScript-only shell that this tool can't render), `/features` and
`/product-features` returned 404. Capterra, G2, and Software Advice profile-URL guesses all 403'd
or 404'd. DuckDuckGo/Bing searches returned irrelevant results (not usable). **No vendor content
was retrieved this session.** I have deliberately not filled this section with recalled/assumed
detail, per instructions not to invent — RTPro is long-established in broadcast/production camera
and grip-rental circles but I cannot substantiate specific scheduling-engine claims from this
session's fetches. Treat as a research gap, not an absence of capability.

---

## 6. easyJOB (now under "Because Software")

**Sites tried:** easyjobsoftware.com (DNS failure — domain no longer resolves), easyjob.net (500
error), easyjob.de (redirected to `because-software.com`, then to `en.because-software.com`,
which loaded). The rebrand itself is a finding: **[SOURCED]** the German/Austrian company behind
easyJOB now trades as **Because Software**, positioning as "The ERP platform for agencies &
project-driven businesses" — general project-agency ERP language, not AV/production-specific
marketing, on the page fetched. [SOURCED] Claims "850+ installations and 35 years" in market.
[SOURCED] Core modules mentioned: project management, accounting, controlling, time tracking.
[SOURCED] Integrations: awork, Jira, Personio (none of these are AV/rental-industry tools —
they're general project/HR tools, reinforcing that the fetched page is the generic-ERP framing of
the product, not its rental-specific configuration). [SOURCED] Pricing is quote-gated (free-trial
CTA only, no published tiers). **[UNVERIFIED]** — no equipment-availability, Gantt, crew-scheduling,
kit-bundling, or serialized-stock language was present on the page fetched; this may simply mean
the AV-specific product page lives at a different URL than the ones I found this session — treat
the absence as a gap in what was retrieved, not as evidence the features don't exist. easyJOB has
a long-standing **[INDUSTRY-COMMON]** reputation in German-speaking broadcast/event-technology
markets specifically, which the "35 years" claim is consistent with, but I could not pull the
AV-specific feature page to confirm scheduling-engine mechanics.

---

## 7. RentalWorks — identity could not be confirmed

**[FETCH-FAILED / AMBIGUOUS]**. rentalworks.com 301-redirects to `unitedrentals.com/rental-works`,
which itself returned 403 on fetch. The Capterra category listing separately surfaced a product
called **"RentalWorks"** described as **"a powerful windows-based car rental software package for
the global vehicle rental industry"** (4.5/5, 124 reviews) — i.e. **vehicle/car rental**, not
AV/production. It is not clear from what I could fetch this session whether this is the same
RentalWorks historically associated with entertainment/broadcast asset rental, a same-named
different product, or whether United Rentals absorbed/repurposed the brand for its own internal
tool-rental software. **I am flagging this explicitly rather than guessing**: treat "RentalWorks"
as unconfirmed for this category until someone can browse `unitedrentals.com/rental-works`
directly (it 403'd every automated fetch attempt) or find the vendor's independent site if one
still exists.

---

## 8. Navigator Business Solutions — likely not a category vendor

**[SOURCED — negative result]**. navigatorbusinesssolutions.com (the domain named in the task
brief) 301-redirects to an individual's personal LinkedIn profile — the domain has been
repurposed/parked. A search-engine snippet surfaced `nbs-us.com` as "Navigator Business
Solutions," which **is a real, live company** — but its fetched homepage shows it as an **SAP**
implementation partner (SAP Cloud ERP / Business One / Business ByDesign) serving Consumer
Products, Retail, Industrial Products, Life Sciences, Manufacturing, Wholesale & Distribution, and
Professional Services. **No AV, production, staging, or event-rental vertical was found on its
site.** My working conclusion: **this vendor does not belong in an AV/production rental
competitive set** — it appears to have been included in the task's candidate list on a name
collision, not a real product match. Recommend dropping it from this category's tracking list
unless someone can point to a specific AV-vertical offering under this name that I failed to find.

---

## Scheduling patterns worth stealing

Concrete, technical, and grounded in what was actually confirmed above (each tagged back to its
source vendor):

1. **Three-state (or more) planning ladder with color as the primary signal, not just a
   checkbox.** [SOURCED — Current RMS] blue/unallocated → green/confirmed → red/booked-out on
   every resource tile. This is the single most copy-worthy UX pattern in the category: it
   answers "is this real yet?" at a glance across hundreds of line items, which a plain
   available/unavailable boolean cannot.
2. **Shortages as a surfaced warning, never a silent hard block.** [SOURCED — Current RMS,
   Rentman] Both vendors let you keep booking into a shortage and instead badge it (exclamation
   icon, red text, dashboard tile of "orders with shortages"; Rentman's "warning signals").
   Hard-blocking availability is the wrong default for a business where sub-rentals, swaps, and
   last-minute adds are routine — the software's job is to make the shortage impossible to miss,
   not to prevent the booking.
3. **Line-item-level sub-phase time blocking (Prep / Travel / Setup / In Use), not just a single
   job-level date range.** [SOURCED — Current RMS "Extended Service Item Schedule"] Each service
   or equipment line can carry its own internal timeline. This is exactly the prep/transit/buffer
   modeling a naive scheduler skips — and it's applied per line item, so a truck's travel window
   and a rigger's setup window can be tracked independently within the same job.
4. **Kit/package explosion with mixed serialized+bulk tracking in the same object.** [SOURCED —
   Flex explicitly; Current RMS's "wireless mic packs, tent packages, camera kits"] A "camera
   package" reserves its named serialized bodies/lenses *and* its bulk consumables (cables,
   batteries) as one atomic reservation, and pull sheets/kit contents auto-generate from it —
   this is the pattern that prevents "job left the warehouse missing an adapter."
5. **Sub-rental as a first-class shortage-resolution action inside the scheduler, not a separate
   purchasing workflow.** [SOURCED — Rentman "solve equipment shortages with alternatives and
   subrentals," Current RMS "mark products as sub-rented"] When the system detects a shortage, the
   fix (borrow from another warehouse, sub-rent from a vendor, or substitute an alternative SKU)
   is offered right there, in the same screen that raised the alert — not a context-switch to a
   different module.
6. **Crew treated as a resource type inside the same planner as equipment/vehicles/rooms,** with
   skills/qualification tags as filter criteria for assignment. [SOURCED — Rentman: "filter crew
   based on the needed skills… assign suitable crew members to job functions"; Current RMS unifies
   crew/transport/venues/rooms in one Resource Planner]. Worth stealing the *unification*, but
   worth improving on the *matching* — none of the vendors researched showed evidence of
   constraint-solving (e.g., auto-suggest the best-fit available crew member), only
   filter-then-manually-assign.
7. **Per-seat-free "execution" tier alongside paid "planning" seats.** [SOURCED — Rentman: "Basic
   users are always free" for execution-only staff] Recognizes that a scheduler's real cost driver
   is the number of people who *plan*, not the number who *execute* — a pricing pattern worth
   mirroring architecturally even independent of pricing strategy (i.e., design the permission
   model around planner vs. executor roles from day one).

---

## Where human judgment still dominates (the opening for agentic scheduling)

None of the four vendors with confirmed detail (Rentman, Current RMS, Flex, Lasso) showed evidence
of anything beyond **filter-and-manually-assign** logic — every "smart" claim found was UI
convenience (drag-and-drop, color coding, real-time sync), not decision-making:

- **Shortage *resolution* is entirely manual.** Every vendor surfaces the shortage; none showed
  evidence of *ranking* the resolution options (which sub-rental vendor is cheapest/fastest right
  now, which alternate SKU is close enough spec-wise, which other job could donate its allocation
  without itself going short). This is squarely an optimization problem a solver or agent could
  own — the category currently stops at "here's a red badge, go figure it out."
- **Crew-to-job matching is filter-then-pick, not constraint-solved.** [SOURCED — Rentman, Flex
  StaffingPlus] Both let you filter by skill and blast an availability inquiry to everyone who
  matches; neither shows evidence of optimizing *across* the whole roster and the whole week
  (who should go on which job to minimize overtime, travel, or idle time company-wide). That's a
  genuinely hard scheduling problem (a variant of vehicle-routing/assignment) that human
  schedulers currently solve by feel and phone calls.
- **Prep/transit/buffer time is configured per line item by a human, not derived.** [SOURCED —
  Current RMS's Extended Service Item Schedule] The *capability* to model Prep/Travel/Setup/In-Use
  exists, but nothing found suggests the system *predicts* these durations (e.g., from distance
  between warehouse and venue, or from historical strike times for a given rig). An agent that
  learns "this crew takes 3 hours to strike this size of PA system" and pre-fills the buffer would
  be doing something none of these tools do today.
- **Cross-job trade-offs are invisible.** Nothing in the fetched material shows a system-level view
  that says "committing this item to Job B will endanger Job A's margin/timeline" — shortages are
  shown per-job, not as a portfolio-level trade-off. This is exactly the kind of multi-job
  reasoning an LLM-based planner is well suited to narrate ("I can fill Job B's gap by pulling
  from Job A's spare capacity, but that leaves Job A with zero buffer if their load-in slips") in
  a way a Gantt chart cannot.
- **Sub-rental vendor selection and price negotiation remain 100% outside these tools.** [SOURCED
  — the feature is "mark as sub-rented"/"solve with subrentals," i.e. a status flag, not a
  vendor-selection workflow]. Deciding *which* sub-rental house to call, at what rate, with what
  reliability history, is entirely human institutional knowledge today — a natural place for an
  agent with access to a vendor-performance history to add real value rather than just replicate a
  calendar.

---

## Comparison table

| Vendor | Scheduling engine (confirmed) | Crew module | Multi-location | Kit/serialized+bulk | Pricing | Status this session |
|---|---|---|---|---|---|---|
| **Rentman** | Real-time availability + shortage warnings; sub-rental as shortage fix | Skills/qualifications tagged, self-serve sign-up | Dedicated feature, €5/warehouse add-on | Not confirmed in fetched copy | **Published**, modular à la carte (€39 base + modules) | [SOURCED] Strong |
| **Current RMS** | Color-coded 3-state Resource Planner; soft shortage warnings; per-line-item Prep/Travel/Setup/In-Use scheduler | Unified into general Resource Planner (no skills-match confirmed) | Container-based warehouse flow, Global Check-in | Kits confirmed; serialized/bulk split not explicit | **Published**, flat per-user, all features included | [SOURCED] Strong |
| **Flex Rental Solutions** | Unified committed/available/in-transit view; live conflict detection | Separate paid module (StaffingPlus) with Gantt view, skills-based blast-inquiry | Explicitly priced per additional location | **Explicit** dual serialized+bulk tracking confirmed | **Published**, $510/mo base, unlimited users | [SOURCED] Strong |
| **Lasso** | Real-time availability; "Scanning Mode/Manual Prep Mode" for serialized cases | Bulk scheduling + skills-matching claimed; AI agent "Lassie" | Warehouse ops referenced, not detailed | Serialized road-case tracking confirmed; kit depth not detailed | Quote-gated | [SOURCED] Partial |
| **HireHop** | Unknown this session | Unknown this session | Unknown this session | Unknown this session | Unknown this session | **[FETCH-FAILED]** — 403 on every path |
| **RTPro** | Unknown this session | Unknown this session | Unknown this session | Unknown this session | Unknown this session | **[FETCH-FAILED]** — empty/404 |
| **easyJOB (Because Software)** | Not shown on fetched (generic-ERP) page | Not shown | Not shown | Not shown | Quote-gated | [SOURCED] Rebrand confirmed; product detail not found |
| **RentalWorks** | Unknown — identity ambiguous (car rental vs. AV rental) | Unknown | Unknown | Unknown | Unknown | **[FETCH-FAILED/AMBIGUOUS]** |
| **Navigator Business Solutions** | N/A | N/A | N/A | N/A | N/A | **[SOURCED]** Not an AV-rental vendor — likely wrong category match |

---

## Ranked: 5 best scheduling ideas to steal

1. **Shortage-as-warning, never hard-block, with the resolution action inline** (Current RMS +
   Rentman combined pattern). Highest-leverage single UX decision in the category — it's the
   difference between a tool schedulers fight and one they trust with edge cases.
2. **The blue/green/red (or richer) planning-state ladder applied uniformly across equipment,
   crew, and transport** (Current RMS). Cheap to build, immediately legible, and it's the visual
   vocabulary an agentic layer should *narrate in*, not replace — "I moved this from green to red
   because…" is a sentence a user will trust precisely because they already know what red means.
3. **Line-item-level Prep/Travel/Setup/In-Use sub-scheduling** (Current RMS) as the data model an
   agent should populate *automatically* from historical job data instead of requiring a human to
   hand-enter it — this is where "steal the pattern, beat the execution" applies most directly.
4. **Kit/package objects that mix serialized and bulk items and auto-generate pull sheets**
   (Flex, Current RMS). Non-negotiable table-stakes for any AV/production entrant — get this
   wrong and ops staff won't trust the system with load-out.
5. **Free/unlimited execution-tier seats vs. paid planning seats** (Rentman) and **unlimited users
   at a flat base price** (Flex) — two different pricing philosophies converging on the same
   insight: charge for planning intelligence, not for headcount using the app. Directly relevant
   to how a new agentic-scheduling entrant should price itself — the agent *is* the planning
   intelligence, so per-planner (or per-agent-decision) pricing likely beats per-seat pricing.

---

## Fetch-failure log (for reproducibility)

- `web.archive.org` — blocked entirely by this environment's WebFetch tool ("unable to fetch").
- `hirehop.com` (root, `/index.php`, `/features.php`, `/tour.php`, both `www` and bare) — HTTP 403
  every time.
- `docs.hirehop.com` — DNS does not resolve.
- `rentaltrackerpro.com` (root, `/index.html`) — empty page body returned (no error, no content);
  `/features`, `/product-features` — HTTP 404.
- `easyjobsoftware.com` — DNS does not resolve. `easyjob.net` — HTTP 500 (root and `/en/`).
  `42he.com` — wrong company (a Cologne CRM vendor, unrelated). `easyjob.de` → redirected twice to
  `because-software.com` → `en.because-software.com`, which loaded.
- `navigatorbusinesssolutions.com` — 301 redirect to an unrelated LinkedIn personal profile
  (domain repurposed/parked).
- `rentalworks.com` — 301 redirect to `unitedrentals.com/rental-works`, which then 403'd.
- G2 (`g2.com/products/{hirehop,rtpro,rentalworks,current-rms}/reviews`) — HTTP 403 on all four.
- TrustRadius (HireHop) — HTTP 403. Capterra direct product-slug guesses for HireHop and RTPro —
  HTTP 404 (wrong slug or delisted); the general Capterra rental-software category page did load
  and yielded real data for Rentman and a same-named-but-likely-different "RentalWorks" (car
  rental).
- DuckDuckGo HTML search — returned a CAPTCHA challenge page, no results extractable.
- Bing HTML search — returned unrelated/cached content not matching the query, not usable.
