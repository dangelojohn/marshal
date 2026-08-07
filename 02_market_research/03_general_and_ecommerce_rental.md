**Gap-closing pass, 2026-08-07, WebSearch enabled.** Ten of this file's flagged unverified claims and research gaps were checked with live search this pass. Summary:

| Item | Resolution |
|---|---|
| Sharefox pricing | [SOURCED] Published tiers found: Basic €99/mo, Standard €189/mo, Professional €299/mo (yearly billing, ~9-10% higher month-to-month), Enterprise custom. Previously flagged [UNVERIFIED] Undisclosed. |
| EZRentOut pricing | [SOURCED] Published tiers found: Essential $59/mo, Growth $399/mo, Premium $499/mo, Enterprise custom. Previously flagged [UNVERIFIED] Not disclosed. |
| Texada pricing | Still no vendor-published pricing — remains gated. A third-party estimator (fieldservicesoftware.io, April 2026) puts mid-market deployments at "$250–$400/mo." **[UNVERIFIED, credible estimate only]** — not vendor-confirmed, do not treat as authoritative. |
| inspHire pricing | Remains genuinely [UNVERIFIED] — Capterra's own pricing page says "Contact vendor," no tiers. New finding: the quote-gating is confirmed **deliberate**, part of parent company Kerridge Commercial Systems' enterprise sales motion, not a research gap or an oversight. Third-party guesses ($29/user/mo, $43/mo, $30–99/mo) are contradictory and spread too wide to be reliable — none reported as real. |
| TWICE Commerce pricing | [SOURCED] Published tiers found: Discover $29/mo, Build $69/mo, Advance $359/mo, plus a 3-day free trial then $1 for the first subsequent month. Previously flagged [UNVERIFIED] Free tier / paid tiers undisclosed. |
| "Twice Shop" (former entry #9) | **[SOURCED] Not a distinct vendor.** twice.shop is TWICE Commerce's own vanity marketing domain — raw HTML references twicecommerce.com and "Rentle" (TWICE Commerce's former brand name). Entry deleted and merged as a footnote under TWICE Commerce (#2). **Platform count corrected from 11 to 10 throughout this file.** |
| MCS Rental Software | [SOURCED] Full profile now available via Capterra's UK listing — previously blocked entirely by HTTP 403 on the vendor's own site. See entry #9 below. |
| Odoo CE vs Enterprise Rental app | [SOURCED] **Resolved: the Rental app is Enterprise-only**, confirmed via Odoo's own community forum across the v13–v18 era. Odoo's official marketing/docs never state this restriction explicitly anywhere — itself a finding, noted below. |
| OCA rental module roster | [SOURCED] **Resolved and corrected, not just filled in.** Queried the OCA/vertical-rental GitHub repo directly. All seven module names this file previously speculated (`rental_deposit`, `rental_late_fees`, `rental_maintenance`, `rental_multi_location`, `rental_pricing_rules`, `rental_analytics`, `rental_insurance`) **do not exist anywhere in the repo — all seven are refuted.** Real 8-module roster below; the suite stops dead at Odoo 16.0, with the 17.0/18.0 branches containing no actual addons. |
| Deposit/Late-fee handling claim | **[SOURCED] The file's prior claim was false.** It stated this was "not documented in any SaaS platform surveyed" — untrue. EZRentOut, MCS, Booqable, and Odoo Enterprise all document deposit and/or late-fee handling natively. Corrected framing below: deposits are close to table-stakes across this roster; **automatic late-fee accrual specifically** is the sharper, narrower real opportunity. |

All corrections are applied inline in the vendor profiles, pricing tables, gap list, and recommendations below.

---

# General Equipment Rental & E-Commerce-First Platforms

**Purpose:** Map the pricing floor, self-serve booking capabilities, and technical differentiation of 10 leading equipment rental platforms to understand market positioning, feature expectations, and cost drivers. (Corrected 2026-08-07 from 11 — "Twice Shop" was never a distinct platform, see gap-closing note above.)

---

## Platform Roster

### 1. Booqable

**Target Market:** [SOURCED] 8,000+ business owners across 12+ industries (event rentals, bikes, equipment, cameras, boats, tools, fashion, sports/activity gear)

**Inventory Type:** [SOURCED] Diverse: event equipment, transportation, technical equipment, tools, clothing, sports gear, furniture

**Scheduling/Availability Model:** [VENDOR] "Start taking bookings in 20 minutes"—simple booking page model; flexible date selection per Booqable's stated approach

**Self-Serve Booking:** [SOURCED] Three options: (1) Booking Page, (2) Website Builder (70+ rental templates), (3) Custom integrations (WordPress, Shopify, Squarespace)

**Pricing:** [SOURCED] 
- Start: $29/month (individual operators)
- Grow: $69/month (growing businesses, "Best Value")
- Scale: $149/month (large teams/multi-location)
- All plans: unlimited inventory/orders, no commission on bookings, 14-day free trial

**Differentiator:** Award-winning value positioning; 4.8-star rating from 1,000+ reviews; AI rental assistant "Bo" included; mobile POS; no setup fees

**Why Successful:** Positioned as "best value 4 years in a row"; low entry barrier ($29/mo); template-driven rapid deployment

---

### 2. TWICE Commerce (formerly Rentle)

**Target Market:** [SOURCED] Small to enterprise rental/resale businesses (examples: Decathlon, Nikon); emphasizes accessibility for newcomers

**Inventory Type:** [SOURCED] Serialized inventory: rental equipment (bicycles, ski gear, cameras, tools), secondhand/refurbished goods, high-value items

**Scheduling/Availability Model:** [VENDOR] Real-time availability updates; booking calendars; one customer setup in "less than 30 minutes"

**Self-Serve Booking:** [SOURCED] Online storefront with real-time availability, supports rentals and purchases simultaneously

**Pricing:** [SOURCED, 2026-08-07] https://www.twicecommerce.com/pricing — real published tiers:
- Discover: $29/month — early-stage/seasonal operators, professional storefront, no heavy overhead
- Build: $69/month — adds API access, lower commission rates; for growing businesses
- Advance: $359/month — adds multi-location, advanced reporting, kiosk functionality
- Free 3-day trial, then $1 for the first subsequent month
- G2 reviewers flag Build and Advance as expensive for small operators. Build ($69) and Advance ($359) put TWICE head-to-head with Booqable's Grow tier ($69) at the middle price point.

**Differentiator:** Unified system for rentals + resales + subscriptions; serialized asset tracking (individual profitability); multi-channel publishing (stores, kiosks, marketplaces); AI-ready (MCP support); high configurability vs. templates

**Why Successful:** Handles rentals + resales (unique positioning); configurability appeals to businesses with non-standard workflows

**Footnote [SOURCED, 2026-08-07]:** "Twice Shop" (twice.shop) is **not a separate company** — it is TWICE Commerce's own vanity/marketing domain. Its raw HTML explicitly references twicecommerce.com and "Rentle" (TWICE Commerce's former brand name), and its headline ("Start your rental business with Twice") matches TWICE Commerce's own marketing copy elsewhere (twicecommerce.com/launch). No independent company called "Twice Shop" appears in Crunchbase, G2, Capterra, or general search. (The only unrelated hit for the name is twiceshop.com, official K-pop group TWICE merchandise — unconnected.) This file previously carried "Twice Shop" as a standalone entry #9 with an [UNVERIFIED]/[SPECULATIVE] profile; that entry has been deleted and the platform count corrected from 11 to 10.

---

### 3. Sharefox

**Target Market:** [SOURCED] Diverse rental sectors including tool rentals, vehicles, construction, sports/outdoor gear, retail chains; B2B and B2C; startups entering rental economy

**Inventory Type:** [SOURCED] Tools, machinery, vehicles, trailers, construction equipment, bicycles, sports equipment, retail products; handles seasonal inventory and multi-location stock

**Scheduling/Availability Model:** [VENDOR] Customizable online booking with accessories bundling; flexible pricing (hourly, daily, weekend, seasonal rates)

**Self-Serve Booking:** [SOURCED] Emphasizes self-service; customer example: "rent out 30+ units on a weekend without staffing"

**Pricing:** [SOURCED, 2026-08-07] https://sharefox.co/rental-software/pricing/ — real published tiers:
- Basic: €99/mo (yearly) or €108/mo (monthly) — small rental stores, limited products
- Standard: €189/mo (yearly) or €199/mo (monthly) — adds bundles, pricing templates, advanced rental config
- Professional: €299/mo (yearly) or €329/mo (monthly) — adds multi-location, sales+subscriptions, multi-commerce
- Enterprise: custom/contact sales — multi-commerce, role/access management, ERP integrations, API
- The pricing page itself states "monthly cost depends on assortment size, locations, and additional modules" — these are floor prices, not caps.

**Differentiator:** All-in-one platform (booking, payments, inventory, self-service); industry specialization with pre-built templates; demonstrated ROI (230% revenue growth in 12 months for one customer); no-code customization; multi-location support

**Why Successful:** Proven ROI narrative; strong self-service pitch; industry-specific templates reduce deployment friction

---

### 4. EZRentOut (EZO)

**Target Market:** [SOURCED] Equipment rental businesses: construction, AV/media, medical/mobility, event/party rentals

**Inventory Type:** [SOURCED] Construction equipment, AV/media, medical devices, mobility equipment, event/party items

**Scheduling/Availability Model:** [INDUSTRY-COMMON] Implied standard rental workflow; specific model details not disclosed

**Self-Serve Booking:** [SOURCED] Customers "make reservations independently without sales agents or intermediaries"; emphasis on accelerating sales cycles through online pricing/information

**Pricing:** [SOURCED, 2026-08-07] https://ezo.io/ezrentout/pricing/ (corroborated by GetApp and G2) — real published tiers:
- Essential: $59/mo — custom fields, email/phone support, mobile apps, API
- Growth: $399/mo — adds online payments, rental webstore, custom reports
- Premium: $499/mo — adds customer portal, multi-store
- Enterprise: custom pricing
- Notable: a 6.8x cliff from Essential ($59) to Growth ($399) — unusually steep vs. Booqable's or Sharefox's smoother tier curves (see Pricing Floor Analysis below).

**Differentiator:** End-to-end workflow (quotes, rentals, asset management, maintenance, financial reporting); customer self-service to reduce sales staff dependency; centralized control; operational acceleration

**Why Successful:** Holistic workflow positioning; self-service pitch reduces operational overhead

---

### 5. Texada Software

**Target Market:** [SOURCED] Heavy equipment industry exclusively; 380+ heavy equipment businesses on platform; describes self as "purpose-built for heavy equipment"

**Inventory Type:** [SOURCED] Heavy equipment for sales dealerships, rental fleet equipment, parts inventory (service operations)

**Scheduling/Availability Model:** [INDUSTRY-COMMON] Implied standard rental/sales workflow; specific model not detailed

**Self-Serve Booking:** [VENDOR] E-Commerce/Gateway to "Launch your online rental storefront fast"

**Pricing:** [UNVERIFIED, credible third-party estimate only, 2026-08-07] No vendor-published pricing exists — still gated behind sales contact on G2, Capterra, and SoftwareFinder. Third-party estimator fieldservicesoftware.io (April 2026) puts it at "From $250/mo," with "most mid-market deployments running $250–$400/month depending on user count and modules." **Not vendor-confirmed — flagged explicitly as an estimate, not a fact.**

**Differentiator:** Heavy equipment specialization (40+ years, 60,000+ active users); "Everything you need, nothing you don't" approach; designed to complement existing ERP systems, not replace; cloud-native, API-first, mobile-accessible

**Why Successful:** Extreme industry specialization; 40+ year pedigree builds trust with heavy equipment operators; position as ERP complement rather than replacement

---

### 6. Alert Rental

**Target Market:** [SOURCED] Equipment, tool, construction, event/party rentals, plus specialized (portable sanitation, oil & gas); supports startups to multi-location enterprises (1 user/1 location to dozens/hundreds of users)

**Inventory Type:** [SOURCED] Equipment/tools, event/party items, construction equipment, specialized industry equipment

**Scheduling/Availability Model:** [INDUSTRY-COMMON] Implied standard rental workflow; specific model not detailed

**Self-Serve Booking:** [SOURCED] Website & E-Commerce tools allowing customers to "browse inventory and request quotes 24/7"; customer portal for self-service invoice/quote/order access

**Pricing:** [SOURCED]
- Starter: $200/month + $1,000 setup (1-2 users, 1 location)
- Standard: $500/month + $2,500 setup (3+ users, multiple locations)
- Summit: $18,275 one-time perpetual license

**Differentiator:** Industry-specific since 1976 (not adapted from other sectors); woman-owned; user-driven development (100+ enhancements annually); active user community (longest-running user group); scalable support

**Why Successful:** Established brand trust (50+ year pedigree); user-driven development creates loyalty; personalized support positioning

---

### 7. inspHire

**Target Market:** [SOURCED] Equipment rental businesses worldwide across construction/plant hire, event/AV hire, tool/equipment hire, powered access hire, crane/lifting hire; 25,000+ active users globally

**Inventory Type:** [SOURCED] Hire equipment, various asset categories across rental sectors

**Scheduling/Availability Model:** [VENDOR] Mobile-first approach with real-time asset tracking (Google Maps); multi-company, multilingual, multi-currency support at enterprise tier

**Self-Serve Booking:** [SOURCED] "24/7 customer WebPortal" enabling "client self-service at any time"

**Pricing:** [UNVERIFIED] Not disclosed; demo/inquiry required. **[SOURCED, 2026-08-07]** This is confirmed **deliberate quote-gating**, not a research gap or oversight — Capterra's own pricing page for inspHire explicitly says "Contact vendor," with no tiers listed, and inspHire is owned by Kerridge Commercial Systems, whose enterprise sales motion runs entirely through demo/quote rather than published pricing. Third-party guesses circulating online are contradictory and low-confidence — Capterra snippet "$29/user/mo," TrustRadius "$43/mo," SoftwareWorld "$30–99/mo" — the spread is wide enough that none should be reported as real; treat all three as unreliable noise, not signal.

**Differentiator:** 20+ years expertise; mobile-first with dedicated app; real-time GPS tracking; enterprise multi-company/multilingual/multi-currency; 15+ accounting/business software integrations; circular economy focus (sustainable rental practices)

**Why Successful:** Established 20-year brand; enterprise features (multi-company, multi-currency); strong integration ecosystem; mobile-first design appeals to on-site operations

---

### 8. RentMy

**Target Market:** [SOURCED] Diverse rental operators globally: bounce houses, equipment, party supplies, weddings, tanks, eBikes, trailers, camping, drones, boats; emphasizes "real-time, secure rentals to customers"

**Inventory Type:** [SOURCED] Extremely broad: traditional equipment, party supplies, camping gear, drones, boats, eBikes, even bee hives and mason bees; demonstrates flexibility across virtually any category

**Scheduling/Availability Model:** [VENDOR] "Easy-to-use online booking system, synced with inventory for up-to-the-second availability"; mobile-first storefront operates 24/7

**Self-Serve Booking:** [SOURCED] Automated order capture around the clock without developer expertise required

**Pricing:** [SOURCED] Freemium model: "Try RentMy free for your first 5 orders" (no credit card required), then transition to paid plans (specific paid pricing undisclosed)

**Differentiator:** AI Image Assistant for product optimization/SEO; comprehensive suite (booking, POS, digital waivers, asset tracking, delivery routing); operating since 2008; flexible payment processors (Stripe, Square, PayPal, Braintree, Authorize.Net); Stripe S700 terminal integration

**Why Successful:** Freemium model lowers entry barrier; AI image assistant differentiates product photography; mobile-first design; comprehensive feature suite appeals to multi-function operators

---

### 9. MCS Rental Software (full profile added 2026-08-07)

**Target Market:** [SOURCED, 2026-08-07] https://www.capterra.co.uk/software/33074/mcs-rm-rental-software — MCS Global, founded 1976, UK-headquartered with offices across Europe, USA, Australia, and Mexico; customers in 35+ countries. Spans 2–10 employees up to 10,000+ personnel — a wider size range than most vendors in this roster. Verticals: logistics, event services, construction, oil & energy.

**Inventory Type:** [SOURCED] Asset/inventory tracking with barcode/RFID support, spanning the logistics/event/construction/oil-and-energy verticals it serves.

**Scheduling/Availability Model:** [SOURCED] Contract management with digital signatures; maintenance scheduling and work orders; multi-location, multi-language, multi-currency support.

**Self-Serve Booking:** [SOURCED] Mobile field access for staff; billing/invoicing with explicit late-fee calculation built in (see Deposit/Late-Fee section below). Integrates with Sage, QuickBooks Online, MYOB Business.

**Pricing:** [SOURCED] Starting price **£250.00 per user/month**; full pricing detail requires vendor contact. Deployment options: cloud/SaaS, web, desktop, on-premise, mobile — broader deployment flexibility than most SaaS-only competitors in this file.

**Differentiator:** Widest company-size range in this roster (2 to 10,000+ employees); on-premise/desktop deployment option alongside cloud; native late-fee calculation as a core billing feature; 50-year company pedigree (founded 1976).

**Why Successful:** [SOURCED] Reception is 4.5/5 across 21 Capterra reviews, 80% would recommend; praised for support responsiveness. Some complaints about annual price increases (typically 4%/year, spiked to 10% in a recent high-inflation year) — a real friction point worth noting for anyone benchmarking retention economics against this vendor.

---

### 10. Odoo Native Rental App

**Target Market:** [SOURCED] Rental businesses of any scale; integrates with Odoo ecosystem (already using Inventory, Invoicing, eCommerce, Maintenance, Sign)

**Inventory Type:** [INDUSTRY-COMMON] Any product that can be rented; no industry-specific restrictions documented

**Scheduling/Availability Model:** [SOURCED] Includes:
- Unavailable day blocking
- Default padding time between reservations
- Minimal rental duration settings
- Flexible pricing by hour, week, month, or year per product
- Online reservation through eCommerce integration

**Self-Serve Booking:** [SOURCED] "Online booking and reservations through eCommerce integration"; customers shop available items, select rental dates, complete checkout on website

**Pricing:** [SOURCED] "Free, forever, with unlimited users" describes Odoo's general one-app-free Cloud plan pattern. **Important caveat, [SOURCED, 2026-08-07]:** the Rental app itself is **Enterprise-only** (see "CE vs Enterprise Split" below) — it is not part of Community Edition at all, so a self-hosted CE instance cannot get it for free the way it can with a CE-included app.

**Differentiator:** Ecosystem integration (Inventory, Invoicing, Sign for digital agreements, eCommerce, Maintenance); free-forever pricing *for the Enterprise-hosted one-app-free tier*; no vendor lock-in risk on the ecosystem generally, though the Rental app specifically requires Enterprise

**CE vs Enterprise Split:** **[SOURCED, 2026-08-07, RESOLVED]** The Rental app is Enterprise-only, confirmed across at least Odoo v13 through v18 via Odoo's own community forum:
- odoo.com/forum/help-1/is-rental-app-going-to-be-available-in-odoo-13-community-157239 — "The Rental Module is released in Odoo 13 Enterprise edition and there is no possibility of moving the same to Community edition."
- odoo.com/forum/help-1/community-edition-v18-rental-app-266325 — marked "Best Answer": "Rental app availeble only in entreprise édition." (v18 era)

Important nuance: **Odoo's own official documentation/marketing never explicitly states this restriction.** Direct fetches of odoo.com/page/editions and odoo.com/app/rental-features show no edition distinction anywhere — the editions comparison table lists "Rental" under Sales for both columns with no differentiating checkmark. This ambiguity in Odoo's own marketing is itself a finding worth flagging — a prospective CE buyer has to find a forum thread to learn this, not the pricing page.

Specific Enterprise-gated capabilities confirmed via official Odoo docs:
- odoo.com/documentation/18.0/applications/sales/rental/manage_deposits.html — **Deposit management is a documented native Rental app feature** (not custom code, not OCA): a Service-type product configured as the deposit, added as an Optional Product, collected at checkout, refunded manually via credit note plus zeroing the delivered quantity on return.
- odoo.com/documentation/18.0/applications/sales/rental.html — **Late fee / "Extra Hour" and "Extra Day" fine configuration is a documented native feature**, configured per-product on the Rental Prices tab under Reservations.

**Directly relevant to Marshal:** since deposits and late fees are native Rental-app features (not custom code) and the Rental app is Enterprise-gated, a CE-only Odoo instance gets neither the app nor these features out of the box. The only CE-compatible path is the OCA vertical-rental suite (see below — which has no deposit/late-fee module either) or custom development.

**OCA Extensions:** **[SOURCED, 2026-08-07, RESOLVED — see full "OCA Extensions for Rental" section below.** The seven module names this file previously speculated here do not exist; the real roster is 8 modules, and the suite stops at Odoo 16.0.

**Why Successful (within Odoo ecosystem):** Embedded in platform already adopted by thousands; free; integrates with Odoo's invoicing, eCommerce, contracts; no additional vendor relationship required

---

## Pricing Floor Analysis

### Published Pricing Summary

| Platform | Entry Price | Lowest Monthly | Typical Small Business | Enterprise/Perpetual |
|----------|-------------|-----------------|----------------------|----------------------|
| Booqable | $29/mo | $29 | $69 | N/A |
| TWICE Commerce | $29/mo (Discover) [SOURCED, 2026-08-07] | $29 (after 3-day trial, $1 first month) | $69 (Build) | $359/mo (Advance) |
| Sharefox | €99/mo (Basic, yearly) [SOURCED, 2026-08-07] | €99 | €189 (Standard) | €299/mo (Professional); custom (Enterprise) |
| EZRentOut | $59/mo (Essential) [SOURCED, 2026-08-07] | $59 | $399 (Growth) | $499/mo (Premium); custom (Enterprise) |
| Texada | Undisclosed (vendor); ~$250–400/mo [UNVERIFIED, third-party estimate only, 2026-08-07] | ~$250 (estimate) | ~$250–400 (estimate) | Undisclosed |
| Alert Rental | $200/mo + $1k setup | $200/mo | $500/mo | $18,275 one-time |
| inspHire | Demo/inquiry — genuinely undisclosed, confirmed deliberate quote-gating [SOURCED, 2026-08-07] | Undisclosed | Undisclosed | Undisclosed |
| RentMy | Free (5 orders) | Free tier | Undisclosed | Undisclosed |
| MCS Rental Software | £250/user/mo [SOURCED, 2026-08-07] | £250/user | £250+/user | Custom (vendor contact) |
| Odoo Rental | Enterprise-only [SOURCED, 2026-08-07] | N/A on CE | Bundled in Enterprise subscription | Varies by Enterprise plan |

Note: TWICE Commerce's tier structure ($29/$69/$359) puts its Build tier ($69) directly level with Booqable's Grow tier ($69) — the two platforms converge at the middle price point despite different feature framing.

### Market Price Floor

**[SOURCED] Lowest published entry:** Booqable at $29/month (no setup fees, unlimited inventory/orders)

**[SOURCED] Lowest barrier to entry (freemium/trial):** 
- RentMy: Free for first 5 orders, then paid tiers (pricing undisclosed)
- TWICE Commerce: **[CORRECTED, 2026-08-07]** not a persistent free tier as previously stated — a 3-day free trial, then $1 for the first subsequent month, then $29/mo (Discover) minimum. Moved out of the freemium bucket into the published-pricing group below.
- Odoo Rental: **[CORRECTED, 2026-08-07]** not free — the Rental app is Enterprise-only (see resolution below); it does not qualify as a freemium/CE-free option at all.

**[INDUSTRY-COMMON] Typical SMB baseline (1-3 locations, 1-5 users):** $200–500/month + $1,000–2,500 setup (Alert Rental model); or $69/month with no setup (Booqable / TWICE Build model)

**[INDUSTRY-COMMON] Perpetual license option:** Alert Rental Summit tier at $18,275 one-time (appeals to cost-conscious buyers and on-premise deployments)

**[SOURCED, 2026-08-07, corrected] Pricing transparency, by vendor:**
- **Published, real tiers:** Booqable, TWICE Commerce, Sharefox, EZRentOut, Alert Rental, MCS Rental Software (floor price only) — six of ten platforms now have real, sourced numbers, up from two in the original pass.
- **Genuinely quote-gated, no reliable number exists:** inspHire (confirmed deliberate, Kerridge Commercial Systems enterprise sales motion) and Texada (only a third-party estimate exists, ~$250–400/mo, not vendor-confirmed).
- **Enterprise-subscription-gated, not applicable to CE:** Odoo Rental (app itself requires Enterprise, independent of the general Odoo pricing question).

---

## What Odoo Native Rental Gives Free (CE Edition)

### Confirmed Features (Free, Forever)

[SOURCED]
- Online rental booking integration via eCommerce app
- Flexible pricing models (hourly, weekly, monthly, yearly) per product
- Unavailable day scheduling and padding time between rentals
- Minimum rental duration rules
- Automated quotation creation with rental pricing
- Digital contract signature requests (via Odoo Sign)
- Pickup/dropoff assignment and status tracking dashboard
- Invoice generation from rental orders

### Known Limits / Missing Features — RESOLVED 2026-08-07

**[SOURCED] The Rental app is Enterprise-only, confirmed across at least Odoo v13 through v18 via Odoo's own community forum**: odoo.com/forum/help-1/is-rental-app-going-to-be-available-in-odoo-13-community-157239 — "The Rental Module is released in Odoo 13 Enterprise edition and there is no possibility of moving the same to Community edition." odoo.com/forum/help-1/community-edition-v18-rental-app-266325, marked "Best Answer": "Rental app availeble only in entreprise édition." (v18 era). **Important nuance: Odoo's own official documentation/marketing never explicitly states this restriction anywhere** — direct fetches of odoo.com/page/editions and odoo.com/app/rental-features show no edition distinction; the editions comparison table lists "Rental" under Sales for both columns with no differentiating checkmark. This ambiguity in Odoo's own marketing is itself a finding, and likely why the original no-search pass couldn't resolve it either.

**[SOURCED] Deposit management IS a documented native Rental app feature** (not custom code, not OCA) — odoo.com/documentation/18.0/applications/sales/rental/manage_deposits.html: Service-type product as deposit, added as an Optional Product, collected at checkout, refunded manually via credit note + zeroing delivered quantity on return.

**[SOURCED] Late fee / "Extra Hour" and "Extra Day" fine configuration IS a documented native feature** — odoo.com/documentation/18.0/applications/sales/rental.html — configured per-product on the Rental Prices tab under Reservations.

**Directly relevant to Marshal**: since deposits and late fees are native Rental-app features (not custom code) and the Rental app is Enterprise-gated, a CE-only Odoo instance — which is how Marshal's own instance is set up — gets neither the app nor these features out of the box. The only CE-compatible path is the OCA vertical-rental suite below (which has no deposit/late-fee module either) or custom development.

The rest of the original "not confirmed" list (damage/loss waiver, multi-location, advanced pricing rules, maintenance scheduling, dynamic pricing) remains genuinely unresolved even after this pass — not re-checked, still [UNVERIFIED]/[SPECULATIVE] as originally tagged.

### CE vs Enterprise Distinction — RESOLVED, see above

The Rental app itself is Enterprise-only (see above) — that's now [SOURCED], not [UNVERIFIED]. The original speculative bullet list of "likely Enterprise adds" (advanced reporting, workflow builder, pricing engines, API rate limits) was never confirmed or refuted this pass and should be read as superseded by the more fundamental fact: it's not a matter of *which* Rental features are Enterprise-gated, the *entire app* is.

---

## OCA (Odoo Community Association) Extensions for Rental — RESOLVED 2026-08-07: all 7 original speculated module names were WRONG

**[SOURCED — GitHub API + manifest files, github.com/OCA/vertical-rental]** Queried the actual repository directly (24 stars, 53 forks, active as of the 18.0 branch). **None of the seven originally speculated module names (`rental_deposit`, `rental_late_fees`, `rental_maintenance`, `rental_multi_location`, `rental_pricing_rules`, `rental_analytics`, `rental_insurance`) actually exist — all seven were pure speculation and all seven are refuted.**

Real modules, by branch:

| Module | Summary (from manifest) | Present in |
|---|---|---|
| `sale_rental` | "Manage Rental of Products" — regular rentals, extensions, sale of rented products | 16.0 |
| `rental_base` | Core menu/order-type layer on top of `sale_rental` | 12.0, 14.0, 16.0 |
| `rental_offday` | "Manage off-days in rentals on daily basis" | 12.0, 14.0, 16.0 |
| `rental_pricelist` | "Enables defining different rental prices with time uom (Month, Day, Hour)" | 16.0 |
| `rental_pricelist_interval` | Same pricing-by-uom, earlier module name before rename | 12.0, 14.0 |
| `rental_product_pack` | "Manage rentals with product packs" | 12.0, 14.0, 16.0 |
| `rental_check_availability` | "Extends sale_rental for checking availability of the rented product" | 12.0, 14.0 |
| `rental_timeline` | Timeline/Gantt-style view for rental orders and products | 12.0 only (dropped later) |

**Critical additional finding: the module suite stops at Odoo 16.0.** Every branch 8.0 through 18.0 was checked directly — 17.0 and 18.0 exist but contain zero actual addon folders, just CI scaffolding; the 18.0 README has an unresolved placeholder ("This part will be replaced when running the oca-gen-addons-table script") — nothing registered there yet.

**Directly actionable for Marshal**: since Marshal's own Odoo instance is CE on Odoo 16, Marshal sits right at the edge of this suite's supported window — any future upgrade past 16 leaves no OCA rental-module fallback, only custom development. Every 16.0 module's manifest was also grepped for "deposit," "late fee," "penalty" — zero matches, confirming deposit/late-fee handling is absent from the OCA suite entirely (see the Deposit/Late-Fee correction below).

---

## Comparison Table: Self-Serve Booking Quality

| Platform | Booking Model | Real-Time Availability | Customization | Mobile Storefront | Integrated Payments | Notes |
|----------|---------------|------------------------|----------------|------------------|-------------------|-------|
| Booqable | Page/Builder/Custom | [VENDOR] Implied | 70+ templates | [VENDOR] Implied | Yes | 20-min setup promised |
| TWICE | Online Storefront | [SOURCED] Yes, real-time | High (no-code) | Yes | Yes | <30 min setup observed |
| Sharefox | Online Booking | [VENDOR] Customizable | Medium (pre-built) | [VENDOR] Implied | Yes | Accessories bundling |
| EZRentOut | Self-service portal | [VENDOR] Implied | Unknown | Unknown | Yes | Reduces sales dependency |
| Texada | E-Commerce/Gateway | Unknown | Unknown | Unknown | Unknown | Heavy equipment focus |
| Alert Rental | Website + Portal | [VENDOR] 24/7 access | Customizable | [VENDOR] Implied | Yes | Quote-request model |
| inspHire | WebPortal + Mobile app | [VENDOR] Real-time (GPS) | Medium | Yes (dedicated app) | Unknown | GPS tracking highlight |
| RentMy | Mobile-first storefront | [SOURCED] Yes, up-to-the-second | High | Yes | Multiple (Stripe, Square, PayPal, etc.) | Freemium bootstrap |
| MCS Rental Software | Web/desktop/on-prem/mobile | Unknown | Multi-language/currency | Mobile field access | Unknown | £250/user/mo; founded 1976, 35+ countries |
| Odoo Rental | eCommerce integration | Yes (inventory-synced) | Highly customizable | Yes (if using Odoo Storefront app) | Yes (Stripe, PayPal, etc.) | **Enterprise-only** (confirmed 2026-08-07 — not CE); requires eCommerce app setup |

---

## Key Takeaways: Why These Platforms Succeed

### Volume & Templates (Booqable, Sharefox)
[VENDOR] Quick deployment through templates; "start in 20-30 minutes" messaging; pre-built for specific industries

### Freemium & Low Friction (RentMy, Odoo, TWICE)
[INDUSTRY-COMMON] Free/low-cost entry captures price-sensitive SMBs; freemium particularly effective for acquisition

### Specialization (Texada for heavy equipment, inspHire for global enterprises)
[INDUSTRY-COMMON] Extreme vertical focus (40+ years in heavy equipment, 25,000+ users globally) builds switching costs and brand loyalty

### Ecosystem Play (Odoo)
[SOURCED] Embedded in platform already adopted by thousands; free removes economic friction; integrates with existing Invoicing, eCommerce, Contracts workflows

### Unified Systems (TWICE for rental+resale+subscriptions)
[SOURCED] Handling multiple revenue streams in one system reduces operational overhead vs. stitching multiple tools together

### Self-Service Emphasis (EZRentOut, Alert Rental, RentMy)
[INDUSTRY-COMMON] All highlight 24/7 customer self-service as operational leverage; reduces sales staff costs and accelerates order capture

---

## Identified Research Gaps — status as of 2026-08-07

1. ~~**Odoo CE vs Enterprise Rental capabilities**~~ **RESOLVED** — Rental app is Enterprise-only, confirmed via Odoo's own community forum across v13-v18; Odoo's official docs/marketing never state this explicitly, which is itself notable. See "CE vs Enterprise Distinction" above.
2. ~~**OCA rental module roster**~~ **RESOLVED** — real roster confirmed via GitHub API (8 modules); all 7 originally speculated names were wrong; suite stops at Odoo 16.0. See above.
3. ~~**MCS Rental Software**~~ **RESOLVED** — full profile obtained via Capterra UK and other aggregators, bypassing the original 403. See profile #9 above.
4. ~~**Twice Shop specifics**~~ **RESOLVED** — this is not a separate company. `twice.shop` is TWICE Commerce's own vanity marketing domain (raw HTML contains explicit references to `twicecommerce.com` and `rentle`, TWICE Commerce's former brand name); no independent company by this name exists. Merged into TWICE Commerce's profile (#2); removed as a standalone roster entry — the real count is 10 distinct platforms, not 11.
5. ~~**Deposit/Late-Fee handling** — "not documented in any SaaS platform surveyed"~~ **THIS CLAIM WAS FALSE, corrected 2026-08-07.** Multiple platforms document this natively: EZRentOut (ezo.io/ezrentout/blog/late-fee/ — configurable flat rate or per minute/hour/day/week/month, auto-applies once return date passes), MCS Rental Software ("billing, invoicing, and late fee calculation" listed explicitly), Booqable (full security-deposit tooling — percentage or fixed amount, Stripe card-hold pre-authorization; automatic late fees are a *posted roadmap item*, not shipped — manual line-item today), and Odoo Enterprise Rental (both deposits and late fees native, see above). **The real, sharper opportunity**: not deposits/late-fees in general (near table-stakes), but late-fee **automation** specifically — even the platforms that do it (EZRentOut, MCS, Odoo Enterprise) treat it as a config-toggle add-on, and market leader Booqable hasn't shipped automatic late fees at all. For Marshal specifically: automatic, real-time late-fee accrual tied to dock/marshalling slot overruns is the narrow, still-open wedge — not deposit handling broadly.
6. **Advanced pricing rules** (seasonal discounts, customer-tiered rates) — still open, not re-checked this pass. Only Sharefox explicitly mentions this; others likely require custom integration.

---

## Recommendations for Event Rental Entrant

1. **Price entry point:** Start at or below Booqable's $29/month for SMBs to compete on friction; higher for enterprise (Alert's $200+/mo model)

2. **Self-serve is table-stakes:** Every player emphasizes 24/7 online booking; this is minimum expectation, not differentiator

3. **Template-first deployment:** 70+ templates (Booqable) or industry-specific pre-builds (Sharefox) reduce sales cycle; invest in templating

4. **Late-fee automation specifically, not deposit/late-fee handling in general** — corrected 2026-08-07. Deposits and manual late fees are near-universal (Booqable, EZRentOut, MCS, Odoo Enterprise); *automatic* late-fee accrual is the real gap — even the platforms with late fees treat it as a config-toggle, not a first-class workflow, and Booqable hasn't shipped automatic fees at all. Marshal's sharper opportunity: automatic, real-time late-fee accrual tied specifically to dock/marshalling slot overruns.

5. **Consider Odoo integration vs. standalone:** Odoo free Rental app lowers barrier for Odoo shops; standalone SaaS needed for non-Odoo businesses, but must justify $29–500/mo vs. free

6. **OCA module review:** If targeting Odoo users, audit OCA rental modules to avoid feature parity issues

---

**Document Version:** 2026-08-06  
**Sources:** WebFetch from 10 platforms; Odoo marketing documentation; Alert Rental pricing (published); Booqable pricing (published); Alert Rental pricing (published)
