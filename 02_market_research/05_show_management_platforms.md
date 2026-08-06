# Show Management Platforms — the show manager's daily tool

Research method: WebFetch against vendor-owned URLs only (WebSearch unavailable this session). Every vendor site is quote-gated with no public pricing page found anywhere in this category — that absence, repeated across all seven vendors, is itself tagged as a finding below. Failed fetches are reported honestly rather than papered over.

Tags: [SOURCED] = pulled from a live vendor page this session. [VENDOR] = vendor marketing claim, unverified by a third party. [INDUSTRY-COMMON] = general trade-show-industry knowledge not confirmed by a fetch this session. [UNVERIFIED] = plausible but could not confirm. [SPECULATIVE] = my inference/synthesis, not a claim any source made.

---

## 1. Map Your Show (MYS)

Owned independently (not part of the Personify/Momentive rollup). Serves major organizers directly — CES, WEFTEC, InfoComm cited as customers [SOURCED, mapyourshow.com homepage]. Claims "trusted by over 1.7 Million Trade Show Exhibitors" [VENDOR].

- **Floor plan (Floor Builder)** [SOURCED, mapyourshow.com/trade-show-exposition-floor-builder]: drag-and-drop, "no CAD software required." Multiple team members can edit concurrently. Booths can be locked "to prevent accidental changes, or reserve spaces for key exhibitors." Booths are color-coded by status/type. Includes an audit tool that flags "sizing or placement errors." Critically: **"Export functionality to DXF or PDF formats for general service contractors"** — i.e., the floor plan leaves the platform as a file, not a live feed.
- **Booth sales (MYS Sales Pro)** [SOURCED, mapyourshow.com/trade-show-booth-sales]: exhibitors "compare pricing of available spaces and self select their booth based on the available budget" — self-service, price/size-driven selection. Sponsorship inventory shown "in real time" alongside booths, single checkout. 15+ payment processors integrated. Customizable reporting dashboard for real-time booth-sales/sponsorship tracking. Explicitly supports on-site renewal: "leverage Booth Sales on-site to secure commitments from exhibitors for the following year."
- **Exhibitor management (Exhibitor Resource Center)** [SOURCED]: profile management, balance/invoice viewing, lead access, a deadline checklist with a "vendor connections" line item — this is a link out to the GSC's own portal, not a data integration (see Seam section).
- **Registration coupling**: registration listed as an integration category, not a native module — implies MYS partners with separate registration systems rather than owning that layer outright [SOURCED, inferred from integrations page language: "Registration system connectivity for seamless registration experience"].
- **Attendee/engagement layer (MYS Connected)** [SOURCED]: AI concierge ("Ask Lina"), matchmaking, wayfinding — a bolt-on product, separate from Floor Builder/Sales Pro.
- **Integrations confirmed**: CRM software, payment processors, AMS, registration [SOURCED]. **No GSC (Freeman/GES/Shepard) integration named anywhere across the homepage, Floor Builder page, Sales Pro page, or MYS Connected page** — four separate fetches, zero mentions.
- **Pricing**: not published; demo-gated [SOURCED, absence].
- **Differentiator**: purpose-built, organizer-only focus (not a general event platform with trade shows bolted on); Floor Builder is treated as the plan-of-record artifact the rest of the product hangs off.

## 2. a2z Events (Personify → now Momentive Software)

`personifycorp.com/products/a2z-events` 301-redirects to `mya2zevents.com` [SOURCED]. a2z is now bundled under Momentive Software alongside WildApricot, MemberClicks, ThreeSixty, and — notably — **Expo Logic** (see below): the same parent now owns both a show-management platform and a former standalone registration/badging company [SOURCED, footer links on mya2zevents.com].

- **Floor plan management** [SOURCED, mya2zevents.com/solutions/floorplan-management/]: drag-and-drop builder, real-time visual updates, color-coded statuses (available/reserved/occupied) with live sync across users. Organizers can "move, merge, upgrade, downgrade, or cancel booth assignments" from one interface. Booth-change reports track "assignments, moves, and cancellations over time." Past floor plans can be reused across shows. Multi-show management from a "Global HQ" dashboard [SOURCED, homepage].
- **Exhibitor management** [SOURCED, mya2zevents.com/solutions/exhibitor-management-software/]: "Event Portal" hub for profiles, staff registration, content; online contracting with e-signature; exhibitor directory with attendee-facing recommendations; lead tracking/reporting.
- **Booth sales (Event Sales Engine)** [SOURCED, mya2zevents.com/solutions/event-sales-engine/]: exhibitors can "select their own booths, submit applications for tiered priority, or offer a guided, consultative experience" — **"tiered priority" is a2z's language for the renewal/priority-points mechanic** the brief asked about. Booths, sponsorships, and add-ons purchase in a single cart. Branded, downloadable invoices.
- **Registration coupling**: registration is a listed solution alongside floor plan/exhibitor mgmt, not visibly separate infrastructure — badge printing/check-in bundled in the same product family [SOURCED, nav].
- **GSC integration**: checked exhibitor-management page and floor-plan page directly — **no mention of Freeman/GES/Shepard integration on either** [SOURCED, absence].
- **Pricing**: not published; demo-gated.
- **Differentiator**: multi-year, multi-event portfolio architecture aimed at large associations/trade shows running many events off one back office; AI-driven attendee matchmaking layered on top.

## 3. ExpoCad

- **Floor plan** [SOURCED, new.expocad.com]: real-time design/edit/share across monitor/tablet/mobile, automated CAD generation, 3D visualization, electrical-layout automation.
- **Exhibitor management (Exhibitor Resource Center)** [SOURCED]: online contracting/e-sign, integrated booth+sponsorship sales, invoicing/payment, multi-event management, AI-assisted directory setup.
- **Integration with service ordering — the one structural exception in this category**: ExpoCad is explicitly sold to **three separate buyers**: organizers (core ExpoCad), **general service contractors via "EXPOCAD Contractor™"** [SOURCED], and venues (CAD-based hall planning). This is the only vendor researched that has a *product line* on both sides of the organizer/GSC seam. However, the page's language on how the two products actually connect is thin — "seamless integrations" with registration/CRM/marketing tools is claimed but **no specifics on whether EXPOCAD Contractor pulls booth assignments live from the organizer's ExpoCad file, or whether it's the same file format re-imported** [VENDOR claim, unverified — could not find a page describing the data flow between the two products].
- **Pricing**: not published.
- **Differentiator**: the CAD/electrical-plan depth (used historically by GSCs for engineering-grade floor plans) and the fact that it straddles organizer + GSC + venue, which none of the other pure-play organizer tools do.

## 4. Cvent (exhibition/trade-show slice of a much larger platform)

- Cvent's trade-show story is **assembled from acquisitions bolted onto its core registration/event-marketing platform**, not a purpose-built floor-plan-first product like MYS/a2z [SPECULATIVE, based on product catalog structure below].
- **Exhibitor Management** [SOURCED, cvent.com/en/event-marketing-management/exhibitor-management]: booth information tracking, "real-time booth associations," self-service exhibitor portal, task management, appointment scheduling, lead capture, automated comms. No contracting, GSC-integration, pricing, or floor-plan-inventory detail on this page.
- **iCapture** — trade show lead retrieval [SOURCED, product catalog]. **JiffleNow** — trade-show appointment scheduling [SOURCED]. Both are separate acquired products under the Cvent umbrella, not native modules.
- **Cvent Event Diagramming**: this is a room-layout/seating-chart tool for banquets and meeting rooms, **not** a trade-show booth-inventory/floor-plan-sales tool [SOURCED, cvent.com/en/products — description: "Create event diagrams and manage seating"]. This is an important distinction: Cvent has no page discovered that maps to what Floor Builder or a2z's Floor Plan Management do (booth inventory + sales status + holds).
- **Eventscloud** (formerly etouches, historically Cvent-adjacent) has been **divested and rebranded to Stova**, now a separate company [SOURCED, eventscloud.com redirects/is-now a Stova login portal, support@stova.io]. Confirms Cvent does not currently own this brand.
- **Pricing**: not published; Cvent is well known industry-wide as an enterprise, sales-led, quote-only platform [INDUSTRY-COMMON].
- **Differentiator / why successful**: dominant on the registration/attendee-management side of large corporate and association events; trade-show/exhibitor tooling reads as a secondary product line relative to MYS/a2z, which appear more purpose-built for the show manager's floor-plan-centric workflow.

## 5. Swapcard

- **Not a floor-plan/booth-sales platform.** Explicitly an attendee-engagement, registration, and exhibitor-ROI layer [SOURCED, swapcard.com]: ticketing, badge printing/QR check-in, AMS/CRM validation, exhibitor self-service portal for booth staff roles, lead capture with badge scanning, "Exhibitor Marketplace" for self-serve add-on purchases, AI matchmaking ("Sherlock AI"), CRM sync to Salesforce/HubSpot.
- **No floor plan or booth-inventory/sales tooling found anywhere on the site** [SOURCED, absence — explicitly flagged in the fetch].
- Claims integration with "30+ external systems" [VENDOR] — reads as a plug-in layer that expects a floor-plan/booth-inventory system of record to already exist elsewhere (i.e., a de facto admission that Swapcard is not that system).
- **Pricing**: not published.
- **Differentiator**: mobile app adoption claim (70-80% vs. "30-40% industry average") [VENDOR, unverified] and AI matchmaking depth; positions itself as revenue-add on the attendee side, not as the show manager's operational core.

## 6. Expo Logic

- As of "Summer 2025," Expo Logic has been folded into **Momentive Event Management Software** [SOURCED, momentivesoftware.com/expologic/ — page is now a migration/rebrand notice, not a product page]. Same parent (Momentive Software) as a2z Events — the two acquisitions sit under one roof now.
- Confirmed remaining feature list from the migration notice: registration (attendee/sponsor/exhibitor), check-in/badging ("branded, on-demand badge printing"), lead retrieval, attendee tracking, event apps [SOURCED].
- **No floor-plan or booth-sales detail available** — the original product page no longer exists in a form that describes it [SOURCED, absence — explicitly a "migration notice," not a spec].
- **Read on the roll-up**: Momentive Software now owns both a2z (floor plan + booth sales) and Expo Logic (registration/badging) — a horizontal consolidation move that, if the two are ever wired together, would close part of the seam described below for their shared customers. No evidence yet that this integration exists.

## 7. Momentus Technologies (formerly Ungerboeck)

`ungerboeck.com` 301-redirects to `gomomentus.com` [SOURCED] — Ungerboeck has been fully rebranded. (`momentustech.com` is expired/parked on GoDaddy — not the live domain [SOURCED, redirect to forsale.godaddy.com].)

- **Structurally different from every other vendor in this category**: Momentus is a **venue/facility management system that also serves exhibition organizers**, rather than an organizer tool that assumes an independent venue. Product lines: **Momentus Enterprise** (convention centers, corporate campuses, universities) and **Momentus Elite** (stadiums, arenas, performing arts centers) [SOURCED, gomomentus.com].
- **Exhibition organizer capability** [SOURCED]: "streamline booth sales, exhibitor services, floor plans, and trade show operations." Customers named: **Jaarbeurs, MCH Group, Messe München** [SOURCED] — all three are venue-operator-as-organizer businesses (they own the halls AND run the shows), which is exactly the case Momentus is built for.
- Also offers **Momentus WeTrack** (incident management), an AI sales assistant, and white-label ticketing [SOURCED/VENDOR].
- One reviewer quote surfaced: "our venue and catering teams easily share client details, contracts, and event timelines" [VENDOR/testimonial] — suggests internal cross-department data sharing (venue ops + catering + sales), but this is about internal Momentus modules talking to each other, not about a third-party GSC.
- **Pricing**: not published.
- **Differentiator / why successful**: for the subset of the market where the venue and the organizer are the same legal entity (major European trade-fair operators like Messe München, Jaarbeurs), Momentus collapses the organizer/venue seam that every other vendor in this category leaves open. It does not solve the organizer/GSC seam.

---

## The seam

Four parties, mapped by what system each one lives in day-to-day:

**(a) Show management platform** (MYS / a2z / ExpoCad / Cvent Exhibitor Management) — system of record for: booth inventory, booth-to-exhibitor assignment, exhibitor company/contact info, contract status, payment status, floor plan geometry.

**(b) General service contractor (GSC) ordering system** (GES's **Expresso**, Shepard's **ExhibitorPro**, Freeman's ordering portal — subdomain `fol.freemanco.com` confirmed to exist via the TLS certificate's alternate names returned when `freemanco.com` failed to load [SOURCED — this came from a certificate-mismatch error, not a marketing claim, so it's a harder data point than most in this document]) — system of record for: what services (carpet, electrical, furniture, labor, rigging, material handling) each exhibitor has ordered and owes for.

**(c) Venue/facility system** — building-level scheduling, dock/loading schedules, union labor jurisdiction, fire-marshal approval of the floor plan. Sometimes this is Momentus/Ungerboeck if the venue runs it; often it's a proprietary or paper-based process.

**(d) The exhibitor** — the one party forced to touch all of the above.

**Where the fragmentation is worst, with direct evidence:**

1. **Booth number does not travel from (a) to (b).** Fetching GES's live ordering portal (`ordering.ges.com`, product name **Expresso**) showed the exhibitor must search for their own booth by "Company Name, Booth Number, or Customer Number," with an explicit **"I Don't Know"** option next to the booth-number field, and a "Create One Here" fallback if the show/booth isn't already listed [SOURCED — this is the single strongest piece of direct evidence gathered this session]. That UI only makes sense if Expresso is **not** reading booth assignments live from whatever show-management platform the organizer used. The exhibitor — who already told the organizer their booth number when they signed the contract in MYS/a2z — has to re-supply it to the GSC from scratch, sometimes not even knowing it.

2. **The show-management platforms treat the GSC as a link, not an integration.** Map Your Show's own Exhibitor Resource Center checklist includes a "vendor connections" line item [SOURCED] — read in context, this is a pointer out to the GSC's separate portal, not a data feed. Across MYS's homepage, Floor Builder page, Sales Pro page, and the dedicated integrations page, **zero mentions of Freeman/GES/Shepard as an integration partner** were found. Same result for a2z's exhibitor-management and floor-plan pages. The only artifact that explicitly bridges organizer and GSC on any vendor page is Floor Builder's **"export to DXF or PDF for general service contractors"** [SOURCED] — a one-way, point-in-time file drop, not a live sync. Booth moves made in the floor plan after that export require a fresh export and manual re-communication.

3. **ExpoCad is the closest thing to a fix, and even it doesn't confirm the fix.** It's the only vendor selling into both the organizer side (ExpoCad) and the GSC side (EXPOCAD Contractor™) [SOURCED]. But its own marketing copy only claims generic "seamless integrations" without describing whether the two products share a live booth database or just a common file format [VENDOR, unverified]. If even the vendor best positioned to have solved this doesn't say so plainly, it's reasonable to conclude it isn't solved cleanly.

4. **The venue is a third silo.** Floor plans get exported as DXF/PDF for "general service contractors" [SOURCED] — the same export path is, by strong industry convention, also how fire-marshal/venue approval typically happens [INDUSTRY-COMMON, not directly confirmed by a fetch]. Momentus/Ungerboeck only closes this gap for the minority of shows where the venue operator is also the organizer (Messe München, Jaarbeurs, MCH Group) [SOURCED]. For the majority case — independent organizer, independent venue, independent GSC — there is no vendor in this research that claims to connect all three.

5. **The exhibitor logs into 3+ systems for one event, each asking for data the others already have:** the show-management exhibitor portal (MYS Exhibitor Resource Center / a2z Event Portal / Cvent Exhibitor Management) for profile, staff badges, directory listing, leads; the GSC ordering portal (Expresso / ExhibitorPro / Freeman Online) for booth services, re-entering company name, booth number, and billing info; and — separately again, per Swapcard's and Grip's product framing (both explicitly position themselves as a plug-in layer, not a system of record) — often a third engagement/matchmaking layer if the organizer licenses one on top of whichever floor-plan platform they use. A fourth system (hotel/housing) is common industry practice for larger shows [INDUSTRY-COMMON, not fetched this session].

**This is the strategic opening.** No vendor researched — including the one (ExpoCad) with products on both sides of the seam — publicly demonstrates a live, bidirectional data path from "booth assigned in the floor plan" to "GSC ordering portal already knows the booth number, dimensions, and exhibitor contact." A minimal-surface product that owned that single handoff (push booth assignment + exhibitor identity from the show-management system into GES/Freeman/Shepard's ordering systems, and pull order status back) would remove the one step every exhibitor and every show manager currently does by hand or not at all.

---

## What a show manager does in a week, and which tool serves it today

This is a composite built from the feature sets found above, not a sourced "week in the life" document — tag: **[SPECULATIVE synthesis]**, individual tool-to-task mappings are [SOURCED] to the feature claims above.

| Day | Task | Tool used today | Seam friction |
|---|---|---|---|
| Mon | Review overnight booth sales — new contracts, payments, expiring holds | MYS Sales Pro / a2z Event Sales Engine dashboard | none — native |
| Tue | Update floor plan — move/merge/split booths per sales requests, lock VIP renewal spaces, clear placement-conflict flags | Floor Builder / a2z drag-and-drop editor | must manually notify GSC of any change post-export |
| Wed | Exhibitor services — chase overdue contracts/COIs, answer portal questions, coordinate booth-assignment changes with the GSC | Exhibitor Resource Center / a2z Event Portal, plus **separate email/phone to GES/Freeman/Shepard** since no live sync exists | GSC has to be told out-of-band; no shared record |
| Thu | Report to leadership — space sold, revenue, exhibitor mix, YoY comparison | MYS Insights / a2z reporting dashboards | reconciled by hand against GSC/venue billing, which live outside the platform |
| Fri | Registration/attendee coordination, prep next renewal push | Registration module (native or partner) + MYS Connected / Swapcard / Grip if a separate engagement layer is licensed | a third login/system for the engagement layer |
| Ongoing | Venue coordination — hall dates, dock schedules, fire-marshal floor-plan approval | Email/phone with venue, or Momentus if the venue runs it; DXF/PDF export from Floor Builder | fully manual for the majority of shows (independent venue) |
| Ongoing | Exhibitor escalations about booth services (carpet, electrical, furniture) not showing correct booth number | Exhibitor is redirected to GES Expresso / Freeman Online / Shepard ExhibitorPro, where they may have to search or **manually recreate their own booth record** | the sharpest edge of the seam — confirmed directly via Expresso's "I Don't Know" booth-number field |

---

## Fetch failures (reported honestly)

- **Boomset**: home page returned only blog/content-hub navigation, no product description. Could not confirm feature set from a live fetch this session; general market knowledge that it's a check-in/badging/lead-retrieval company is [INDUSTRY-COMMON], not sourced here.
- **Freeman**: `freeman.com/store` redirected to `freemanco.com/store`, which failed TLS hostname validation; `www.freemanco.com/store/` returned HTTP 503. Product name and portal subdomain (`fol.freemanco.com`) were confirmed only indirectly via the certificate's SAN list in the error message, not via a rendered page.
- **Cvent** homepage-level URLs guessed (`/en/event-management-software/exhibition-tradeshow-management`, `/en/exhibition-management-software`, `/en/venue-sourcing-software`) all 404'd; had to reconstruct the real product URLs via `/en/products`.
- **MYS integrations page**: URL without the `?hsLang=en` query parameter 404'd; original URL worked. Not re-fetched with corrected parameter after first success — integration-partner names beyond category labels (CRM/registration/payment/AMS) were not obtained.
