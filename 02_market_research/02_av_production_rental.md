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

**Gap-closing pass, 2026-08-07, WebSearch enabled.** Closed, substantially: HireHop and RTPro —
both totally blocked in the original no-search pass (403s, empty JS-shell page bodies, blocked
Wayback Machine) — are now fully substantiated vendor profiles with company-registry data,
published pricing, and concrete feature detail. The **easyJOB section in the original pass
profiled the wrong company** — a genuine name collision: it described Because Software AG, a
German agency-project-management ERP vendor with zero AV/event/rental content, because
`easyjob.de` redirects to `because-software.com`. The actual AV-industry easyjob is made by a
different company entirely, **Protonic Software GmbH** (Hanau, Germany), and is now profiled
correctly below, with the Because Software mixup retained and clearly flagged as a resolved false
lead so it isn't repeated. **RentalWorks** — flagged as identity-ambiguous in the original pass —
turned out to be **three separate entities wearing similar names**: the real, independent
AV/broadcast RentalWorks (Database Works, Inc. — unrelated to United Rentals despite the
`unitedrentals.com/rental-works` redirect), a same-named but unrelated industrial tool-crib
product inside United Rentals' own Specialty Solutions division, and a probable mis-attribution to
a distinct vehicle-rental product, RentWorks (no "al"), by BARS/Bluebird. **Lasso** — present only
in the comparison table and the patterns/gaps sections in the original pass, never with its own
vendor writeup — now has a full 9-point profile matching Rentman/Current RMS/Flex. A discovery
pass beyond the original candidate list surfaced six additional vendors, most notably **Stagera** —
a brand-new, purpose-built, explicitly AI-native competitor to Rentman/Current RMS/Flex/Point of
Rental whose positioning is close to what Marshal itself is trying to be; see the new
"Discovery pass" section below. Not everything closed: RTPro's pricing remains genuinely
quote-gated everywhere searched (confirmed as vendor policy, not a research miss), and the
RentalWorks/RentWorks Capterra-listing mismatch could not be resolved with full certainty. New
findings are tagged **[SOURCED, 2026-08-07]** inline below.

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

## 4. Lasso

**Site:** lasso.io. Positions itself as "the operating system event companies run on," not
rental-only software.

1. **Scheduling engine** — [SOURCED] Event-centric, not order-centric: "built around the event —
   gear, crew, travel, and billing on one timeline." Crew "scheduled across multiple shows and
   multiple venues at once." "No line-count lag" even with "unlimited line items per gear order."
   [SOURCED] Real-time availability with "Scanning Mode/Manual Prep Mode" for serialized cases; an
   AI agent called "Lassie."
2. **Crew/labour** — [SOURCED] Full crew stack: Scheduling, e-Signature, Time Tracking, Travel,
   Payroll, plus LASSO's own Crew Marketplace ("500,000+ Crew on our App"). Crew database tracks
   position/role history. "Deep scheduling with OT by state, certifications, and compliance built
   in" — a stronger compliance/labor-law claim than Rentman/Current RMS/Flex show. Travel booking
   claims "15% average savings on crew travel."
3. **Multi-warehouse/multi-location** — [SOURCED] Transfer orders between warehouses; real-time
   stock levels/locations/movements. Warehouse Operations is a line item inside the Inventory
   Management bundle. Less granular than Current RMS's container model or Flex's per-location
   pricing — bundled into the platform, not priced separately.
4. **Job/project structure** — [SOURCED] Event-centric: "Rather than order-based tools, LASSO is
   built around the event." Run-of-show and centralized event info live inside a "Project
   Management" module.
5. **Customer-facing surface** — [SOURCED] Client-facing invoicing/payment collection exists but no
   dedicated self-service client booking portal was found — closer to Flex's model than to
   Rentman/Current RMS's account area.
6. **Integrations & extensibility** — [SOURCED] QuickBooks (via Zapier and a third-party connector
   "Commercium"), Zapier generally, and an "extensive API." Narrower publicly-documented
   integration list than Current RMS or Rentman.
7. **Pricing model** — Quote-gated on lasso.io. [UNVERIFIED, third-party estimator only]
   ITQlick/Vendr show $3–5/user/month for narrow add-ons scaling to $50/mo at 1 user up to
   $35,000/mo at 1,000 users for fuller bundles; implementation estimates $5,000 (small) to
   $200,000+ (enterprise). Flagged clearly as third-party estimates, not vendor-published figures.
8. **What it does differently** — [VENDOR/SOURCED] Explicit positioning against rental-only tools:
   "If you also schedule crew, track hours across venues, and run payroll and compliance, you've
   outgrown rental-only software." Combines rental/inventory + full HR/payroll/compliance + crew
   marketplace — materially broader scope than Rentman/Current RMS/Flex.
9. **Why customers choose it / leave it** — [SOURCED, Capterra] Choose: "Great 5/5 across the
   board," "scheduling is easy," "comparable price wise to the alternatives, while also offering
   more on a base level." Leave: one reviewer flagged "a lot of training required to get going"
   (offset by strong support per their own account). [SPECULATIVE] the payroll/compliance breadth
   could be excess complexity for a small AV shop wanting only equipment scheduling — no direct
   churn evidence, inference only.

---

## 5. HireHop

**Site:** hirehop.com / hirehop.biz. **[SOURCED, 2026-08-07]** Resolved via WebSearch this pass —
the original no-search attempt hit HTTP 403 on every direct fetch path (consistent with active
bot-blocking) and could not retrieve any first- or third-party content; search retrieval got past
that block.

- **[SOURCED — company registry]** UK company, HireHop Software Limited, registered no. 11241806,
  based in Potters Bar, UK. Founded **2011 by Justin Levene**.
- **[SOURCED]** Scheduling: visual calendar for crew assignment and cost allocation; "warehouse
  schedule filters" and a recently-added "Availability Grid." No explicit Gantt-chart language
  found. [SOURCED] Kit/package: "pre-preps" let the warehouse pre-allocate assets into boxes;
  users can import a spreadsheet to match items by name/part number/bulk barcode into a kit list.
  [SOURCED] Serialized tracking: tracks assets via barcode, QR, RFID, NFC, or serial number; a
  "tracked products" type stores serial numbers/barcodes per individual asset; a dedicated
  "second barcode" field exists specifically for non-programmable RFID tags.
- **[SOURCED]** Crew: native calendar-based crew assignment inside HireHop itself, plus a distinct
  third-party integration with **CrewBrain** — "information for projects and jobs automatically
  sent from HireHop so crew scheduling can be directly managed from within CrewBrain," which adds
  time recording, leave management, application forms, and risk assessments.
- **[SOURCED]** Multi-warehouse/depot: unlimited depots, including "depots inside other depots"
  (e.g., two companies trading from one address); users can be assigned to a specific depot;
  barcode numbering customizable per depot. Multi-depot gated to Professional/Enterprise tiers.
- **[SOURCED]** Pricing, published: Free/Starter tier (1 user, limited) → Professional at
  £46/month primary user + £23/month per additional user → Enterprise (quote-gated: multi-depot,
  advanced permissions, custom integrations). Licensing is concurrent-user, not named-seat —
  "you only pay for the number of administrative team members logging in and processing actions
  simultaneously"; read-only warehouse staff are free.
- **[SOURCED]** Integrations: Xero, QuickBooks, Sage Business Cloud, Sage 50 Cloud, Zapier, and a
  newer Microsoft Business Central integration. [VENDOR claim] "the only rental software that
  allows different depots to sync with different accounting software."
- **[SOURCED]** Reviews: 4.9/5 on Capterra (75 reviews); G2 users describe it as "inexpensive and
  easy to use." Aggregator summary cites 97% satisfaction across 90 reviews on 3 sites.
- **What it does differently** — concurrent-user pricing, a deep barcode/RFID/serial-tracking
  layer, and reviewer sentiment repeatedly framing it as cheaper than Current RMS for comparable
  feature depth.
- **Job/project structure and customer-facing surface** — [UNVERIFIED] not covered in the sources
  retrieved this pass; flagged as a residual gap rather than filled with recalled detail.

---

## 6. RTPro (Rental Tracker Pro)

**Site:** rentaltracker.com. **[SOURCED, 2026-08-07]** Resolved via WebSearch this pass — the
original no-search attempt got empty JS-shell page bodies and 404s on every direct path.

- **[SOURCED]** Company: Rental Tracker Inc. RTPro is pitched as "the leading Inventory and
  Warehouse Management Software for the Film/Entertainment Rental Industry," used from
  1,000-asset shops up to 500,000+ asset studios, "for over 20 years." Sold in industry-specific
  editions: "RTPro Set Lighting Audio Video Camera Touring Edition" and "RTPro Costume Property
  Drapery Edition."
- **[SOURCED]** Scheduling engine: a Space Scheduling module — "Schedule and book any type of
  space, such as Stages, Office, and Parking spots," hourly/daily/weekly/monthly booking, calendar
  and Gantt-chart views, conflict handling. [SOURCED] Kit/package + serialized+bulk explicitly
  confirmed — "handle high-value serialized assets, bulk items, and supplies, kits, labor,
  delivery and pick-up charges, outside processing, sub-rentals, and re-rents… inventory can be
  grouped to form Kits or Packages, with pricing assigned to these bundles."
- **[SOURCED]** Crew/labour: a Crew Scheduling product plus a separate Labor/Space Schedule add-on
  module that feeds invoicing (Labor billed alongside Rentals, Sub-rentals, Sales, Restocking,
  Cleaning, Loss, Damages, Space).
- **[SOURCED]** Multi-location: real-time inventory visibility across all locations,
  multi-currency, multi-language, centralized order management with staging/checkout/transfer/
  return workflows, physical inventory cycle counts across locations. Handles "Parent companies,
  Production companies, and Contact persons" as an org hierarchy.
- **[SOURCED]** Customer-facing surface: customers can review terms, e-sign documents, accept
  agreements online via a Customer Portal.
- **[SOURCED]** RFID: "Mobile RFID Solution," marketed as [VENDOR claim] "the only proven mobile
  RFID solution worldwide in the entertainment industry."
- **[SOURCED]** Deployment flexibility: on-premise, cloud/SaaS, or hybrid — distinctive versus
  every other vendor in this file (all cloud-only).
- **Pricing** — still **[FETCH-FAILED, persists after search]**/quote-gated: no published pricing
  found anywhere this pass either. Confirmed quote-gated, not a research miss.
- **What it does differently** — the strongest confirmed differentiator is the on-prem/cloud/
  hybrid deployment choice plus industry-specific editions — no other vendor in this file offers
  anything but cloud-only.
- **Why customers choose/leave** — [UNVERIFIED] no review or complaint data was surfaced this
  pass.

---

## 7. easyjob (Protonic Software) — corrects the original "easyJOB" wrong-company profile

**Resolved false lead, [SOURCED, 2026-08-07]: the original pass profiled the wrong company.**
easyjob.de redirects to `because-software.com`, and the original research took that redirect at
face value. **Because Software AG** (Germering/Munich + Vienna, founded 1988, ~25 employees,
850+ installations, "35 years in the market") makes project-management/ERP software for
**advertising and marketing agencies** — modules: job/project management, controlling, time
tracking, CRM/groupware, HR, document management, resource planning; integrations Jira, awork,
Personio. There is no AV/event/rental/broadcast content anywhere on its site. A Capterra listing
under the `easyjob` slug corroborates: agency-ERP tool, 1.0/5 from its single reviewer, zero
crew/kit/AV language, €39/month flat. **This is a genuine name collision** — "job" means "client
project" in agency parlance, unrelated to AV production "job" — and it should not be repeated as
the AV-industry easyJOB in future passes.

**The actual AV/production/event-rental easyjob is made by Protonic Software GmbH**, Hanau,
Germany — "developing professional solutions for the global event industry for more than 20
years," "trusted by more than 2,000 companies worldwide," at protonic-software.com. Targeted at
"rental, production and event logistics companies" working in "audio, video, trade shows, events,
conferences, stages, touring, and tents."

1. **Scheduling engine** — [SOURCED] A dedicated "Scheduling Board" and documented
   "Dispositions-Terminologie"; "get availabilities, build schedules… plan more efficiently by
   creating packages and anticipating shortages"; items are reschedulable directly in the Bill of
   Items.
2. **Crew/labour** — [SOURCED] A Crew Scheduling function to "manage and schedule employees, get
   availabilities, build schedules and easily communicate with crew."
3. **Multi-warehouse/multi-location** — [SOURCED] "Works across all sites and stock locations,
   also in different countries and with different currencies."
4. **Job/project structure** — [SOURCED] Editions scale by company size: easyjob S (one-man-shows),
   M (~5 employees), L (~2 sites/~15 employees), XL (large, multi-site). Kit/package: "creating
   packages and anticipating shortages" is explicit; a "Freelancer Communication Pack" module also
   exists.
5. **Customer-facing surface** — [UNVERIFIED] not found in the sources retrieved this pass.
6. **Integrations & extensibility** — [SOURCED] Microsoft Teams (presence status, per-project
   channels), DATEV export (German accounting standard) — narrower/more German-market-specific
   than Rentman/Current RMS/Flex.
7. **Pricing model** — Quote-gated (OMR review aggregator, 3.5/5 single review).
8. **What it does differently** — sells adjacent products easytools (consumables) and rm.biz — a
   small product family alongside the core easyjob line.
9. **Why customers choose/leave** — [UNVERIFIED/thin evidence] only a single OMR review (3.5/5)
   surfaced this pass — not enough to characterize sentiment reliably.

---

## 8. RentalWorks — three separate entities, not one ambiguous one

**Resolved, [SOURCED, 2026-08-07]:** the original pass flagged this as identity-ambiguous after
`rentalworks.com` 301-redirected to `unitedrentals.com/rental-works` (which itself 403'd) and a
Capterra listing described a "car rental" RentalWorks. WebSearch untangled it into three distinct
entities:

1. **The AV/broadcast/entertainment RentalWorks is real, independent, and still actively sold.**
   Made by Database Works, Inc., Brea, California — parent company founded 1983 by Terry Young.
   Live at dbworks.com/products/rentalworks/ and rentalworkscloud.com. Named customer: 4Wall
   Entertainment. Product suite: RentalWorks (core) + Storefront (customer-facing) + Customer
   Portal (payments/account). [SOURCED] Features: multi-office/multi-warehouse, RFID/barcode
   tracking via a QuikScan mobile app (iOS/Android), extensive third-party API, multi-currency,
   customizable forms/reports/dashboards. This is **not** United Rentals and has not been absorbed
   by anyone. [UNVERIFIED] scheduling-engine mechanics, crew module, job/project structure, and
   pricing were not itemized in the sources retrieved this pass — flagged as residual gaps rather
   than filled with recalled detail.
2. **Separately, "Rental Works" acquired by United Rentals is a different company entirely** — it
   sits under United Rentals' Specialty Solutions → Tool Solutions vertical (tool cribs, mobile
   tool rooms "ProBox," construction/industrial tool-tracking via IoT/Bluetooth tags). A
   construction/industrial tool-rental management company, unrelated to AV/entertainment.
   Pre-acquisition history/original name remains [UNVERIFIED].
3. **The Capterra "4.5/5, 124 reviews, car rental" listing the original pass cited does NOT match
   Database Works' current Capterra listing (5.0/5, 1 review).** [SPECULATIVE, moderate
   confidence] Most likely a mis-attribution/conflation with "RentWorks" (no "al") — a real,
   distinct vehicle-rental product by BARS/Bluebird (barsnet.com/products/rentworks/). Could not
   be fully confirmed with 100% certainty.

---

## 9. Navigator Business Solutions — likely not a category vendor

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

## 10. Discovery pass, 2026-08-07: vendors found beyond the original candidate list

WebSearch this pass surfaced six vendors not in the original candidate list. One of them —
Stagera — is the most strategically relevant finding in this entire file.

**Stagera (stagera.ai) — a direct, AI-native competitor to what Marshal itself is trying to be.**
[SOURCED] A brand-new, purpose-built AV/production rental platform positioning itself as the
modern/AI-native alternative to Rentman, Current RMS, Flex, and Point of Rental (dedicated
`/vs-rentman`, `/compare/flex/`, `/compare/current-rms/`, `/compare/point-of-rental/` pages).
Features: multi-warehouse inventory with barcode scanning and automated inter-location transfers;
crew scheduling with certification tracking ("no more group texts or phone calls to fill a show");
catalog/reservations/maintenance/automated pick lists; QuickBooks sync. Pricing: **flat
$80/seat/month, all-inclusive, no feature gates, 14-day free trial, no card required** — the
cleanest flat-rate pricing story in the category, and the only vendor in this file (besides Flex's
unlimited-users model) not gating features by tier. AI angle: an "AI Features" nav link exists but
wasn't detailed on pages fetched — [VENDOR claim, feature depth unconfirmed]. Company background:
founded by "Cruz," described as "a technical founder and Oregon State University student who grew
up around live event production" — reads as early-stage/possibly solo-founder/student-led, no
funding/team size/founding date disclosed. **Treat as a nascent, unproven, very-early-stage direct
competitor to what Marshal itself is trying to be** — near-identical "AI-native, purpose-built, not
adapted from party-rental-tools" pitch, worth watching closely, not yet market-validated.

**IntelliEvent Lightning** (intellieventlightning.com) — [SOURCED] Established 1998, "almost
1,500 customers across 5 countries" — mature, not a newcomer. Real-time inventory across multiple
business units/warehouses (audio, video, camera, lighting, rigging, staging); sub-rentals and PO
creation; labor/crew scheduling for technicians/drivers/internal/freelance; serialized/
non-serialized inventory; package management; RFID/barcode; QuickBooks. Close peer to RTPro — a
direct third-party comparison exists (Slashdot: "IntelliEvent Lightning vs. Rental Track Pro"),
confirming they compete head-to-head.

**InTempo Software** (intemposoftware.com) — [SOURCED] Dedicated AV/camera/lighting/film-video
vertical pages. Cycle counts, reorder-point management, rate/pricing control, quote/reservation/
contract creation with cloning, automated maintenance alerts, utilization tracking, branch-to-
branch transfer, mobile app. Self-positioned "for local and regional businesses" — a smaller/
mid-market player.

**Picker** — [UNVERIFIED/LOW CONFIDENCE] Appears in SEO-listicle aggregator content with plausible
claims (mobile barcode scanning, online storefront, $129/$229/mo pricing) but no independent
vendor website or company name could be located. **Recommend NOT including as a confirmed
vendor** — flagged as possibly unreliable/fabricated listicle content, not added to the comparison
table below.

**EZRentOut** (ezo.io/ezrentout) — [SOURCED] Real, broader-scope (construction, heavy equipment,
oil & gas, medical, event rental, AV/media) — a horizontal asset-tracking tool with AV as one of
several verticals, not AV-native. 4.6/5 on G2 (211 reviews), starts $89/month. Worth a one-line
"adjacent, not AV-native" mention, not a full profile.

**Reservety** (reservety.com) — [SOURCED] Has an AV/production landing page but is fundamentally a
small/midsize storefront rental-booking tool, closer to the party/event-rental category than
AV-production scheduling depth. Lower priority.

**Cheqroom** — appeared only in a secondary aggregator list alongside Rentman/Booqable/Point of
Rental, no AV-specific detail. [UNVERIFIED] whether it has real AV-production depth vs. being a
general asset-tracking tool (known market position: broader equipment/asset management for
universities/corporate AV departments). Not verified this session beyond the passing mention.

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

None of the vendors with confirmed detail in this file (Rentman, Current RMS, Flex, Lasso,
HireHop, RTPro, easyjob/Protonic, RentalWorks/Database Works) showed evidence of anything beyond
**filter-and-manually-assign** logic — every "smart" claim found was UI convenience (drag-and-drop,
color coding, real-time sync), not decision-making. [SOURCED, 2026-08-07] Stagera (see the
Discovery pass section above) is the one vendor in the category that markets an "AI Features" nav
link, but its actual decision-making depth was not detailed on the pages fetched — worth
re-checking once Stagera publishes more than a nav link.

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
| **Lasso** | Event-centric timeline (gear+crew+travel+billing on one view); unlimited line items, no line-count lag; Scanning/Manual Prep Mode for serialized cases; AI agent "Lassie" | Full stack: Scheduling, e-Signature, Time Tracking, Travel, Payroll + Crew Marketplace (500,000+ crew); OT by state, certifications, compliance built in | Transfer orders between warehouses; bundled into Inventory Management, not priced separately | Serialized case tracking confirmed; kit depth not detailed | Quote-gated; [UNVERIFIED, 3rd-party estimate] ~$50–$35,000/mo depending on scale | [SOURCED, 2026-08-07] Full 9-point profile added |
| **HireHop** | Visual calendar; warehouse schedule filters; Availability Grid; no explicit Gantt language | Native calendar-based crew assignment + CrewBrain integration (time/leave/applications/risk) | Unlimited depots incl. depots-inside-depots; per-depot barcode numbering; gated to Professional/Enterprise | Serialized (barcode/QR/RFID/NFC/serial#) + kit "pre-preps" with spreadsheet import | **Published**: Free/Starter → Professional £46 + £23/user/mo → Enterprise quote-gated; concurrent-user licensing | [SOURCED, 2026-08-07] Resolved via search — was [FETCH-FAILED] |
| **RTPro** | Space Scheduling module: calendar + Gantt views, hourly–monthly booking, conflict handling | Crew Scheduling product + Labor/Space Schedule add-on feeding invoicing | Real-time multi-location, multi-currency/language, cycle counts across locations, parent/production-company hierarchy | Explicit serialized + bulk + kits/packages with bundle pricing | Quote-gated — confirmed unpublished after search too, not a research miss | [SOURCED, 2026-08-07] Resolved via search — was [FETCH-FAILED]; pricing still gated |
| **easyjob (Protonic Software)** | Dedicated Scheduling Board; "creating packages and anticipating shortages"; items reschedulable in Bill of Items | Crew Scheduling function (availabilities, schedules, crew communication) | Works across all sites/stock locations, multi-country/currency | Package creation explicit; editions S/M/L/XL scale by company size | Quote-gated | [SOURCED, 2026-08-07] Original profile was the WRONG company (Because Software, agency ERP) — corrected, real vendor now profiled |
| **RentalWorks (Database Works)** | Not itemized in sources retrieved this pass [UNVERIFIED] | Not found [UNVERIFIED] | Multi-office/multi-warehouse confirmed | Not itemized [UNVERIFIED] | Not found — presumed quote-gated [UNVERIFIED] | [SOURCED, 2026-08-07] Identity resolved into 3 distinct entities — was [FETCH-FAILED/AMBIGUOUS]; feature depth still partial |
| **Navigator Business Solutions** | N/A | N/A | N/A | N/A | N/A | **[SOURCED]** Not an AV-rental vendor — likely wrong category match |
| **Stagera** (new, 2026-08-07) | Multi-warehouse inventory w/ barcode scanning + automated inter-location transfers | Crew scheduling with certification tracking | Multi-warehouse confirmed | Catalog/reservations/maintenance/automated pick lists | **Published, flat**: $80/seat/mo all-inclusive, no feature gates, 14-day free trial, no card required | [SOURCED, 2026-08-07] New entrant — nascent, unproven, direct AI-native competitor to Marshal's own positioning |

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

**2026-08-07, WebSearch enabled — resolved all of the above except RTPro's pricing:** HireHop, RTPro, and RentalWorks all substantiated via search (see sections 5, 6, 8). `easyjob.de`'s redirect to Because Software turned out to be a name collision, not the real rebrand — the actual AV-industry easyjob is Protonic Software GmbH, unrelated to the domain chased in the original pass (§7). Still genuinely unresolved even with search: RTPro's pricing (confirmed quote-gated, not a research gap), and G2/TrustRadius/Capterra review depth for HireHop/RTPro/RentalWorks (all still 403 or no-listing).
