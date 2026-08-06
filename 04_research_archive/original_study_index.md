# Event / Exposition Services Platform — research & design library

Compiled 2026-08-06. **Research and design only — no code was written or modified.**
Read `00_README_and_method.md` for the sourcing constraint before quoting any figure.

## 🚩 Start here

| Order | File | Why |
|---|---|---|
| 1 | **`spec/01_design_specification.md`** | The deliverable — what to build, what not to build, and why |
| 2 | `competitors/08_success_patterns_business_models.md` | The entry verdict and business-model asymmetry |
| 3 | `competitors/04_exposition_services_contractors.md` | The real incumbents and the structural facts |
| 4 | `internal/01_forgejo_asset_inventory.md` | What we already own (~35–40%) and the traps |

## The thesis in five lines

1. **Don't build rental software** — floor is $29/mo, Odoo gives it free.
2. **Don't fight the contractors** — their moat is labour and trucks, not code.
3. **Sell the venue** — the one party whose P&L moves on better scheduling.
4. **The seam is proven** — booth data demonstrably doesn't reach service ordering.
5. **Enter at the dock** — the one part of the floor no exclusivity contract covers.

**→ Build `Marshal`: dock and marshalling-yard scheduling for exposition venues.
Canada first. `marshal.show` registered 2026-08-06.** See `spec/04`.

## Competitor research

| File | Category | Headline |
|---|---|---|
| `01_event_party_rental_software.md` | Party/event rental | Category fails at multi-supplier, venue constraints, exhibitor scale ⚠ *carries a correction on unverified ownership claims* |
| `02_av_production_rental.md` | AV/production | Best scheduling ideas: shortage-as-warning; Prep/Travel/Setup/In-Use sub-windows |
| `03_general_and_ecommerce_rental.md` | General/e-commerce | The price floor. Odoo native Rental is free and capable |
| `04_exposition_services_contractors.md` | **The incumbents** | Exclusivity is venue-granted; drayage by CWT; decade-scale tech refresh |
| `05_show_management_platforms.md` | Show management | **THE SEAM** — "I Don't Know" booth field proves data doesn't flow |
| `06_venue_facility_platforms.md` | Venue/facility | Momentus rolled up the category; buffers unautomated; dock scheduling a gap |
| `07_canadian_market.md` | **Canada** | Bill 96 + Law 25 = real moat; market fragmented; size untracked |
| `08_success_patterns_business_models.md` | Business models | Enter as infrastructure, venue-first |

## Design analyses

| File | Question answered |
|---|---|
| `spec/01_design_specification.md` | What to build — FLOOR, three surfaces, one of them not a screen |
| `spec/02_show_board_network_concept.md` | The Phase-5 network payoff — publish gaps, don't sync calendars |
| `spec/03_predictive_scheduling_analysis.md` | **Do manufacturing-style predictive schedulers apply?** Yes — but demand is *booth mix*, not head count |
| **`spec/04_product_recommendation_and_name.md`** | **What to build first and what to call it** — **Marshal**, dock scheduling. 🟢 `marshal.show` registered 2026-08-06; `dock.show` still open |

## Internal assets

| File | Contents |
|---|---|
| `internal/01_forgejo_asset_inventory.md` | Reuse manifest, scheduler architecture, security traps |
| `internal/02_recovered_asset_findings.md` | **Reports recovered from agents that died before delivering** — all additive |

**Top asset:** `avn.capability` — one contract fulfilled by mcp/api/portal/web_form/email/human.
Onboards venues at any integration maturity. Competitors assuming API-first cannot.

**Runner-up, found late:** `qnap/porterly-future-reference` — a dependency-free
reference architecture for agents-propose/core-decides with **74 invariant tests**.
The worked answer to "how do we let an LLM propose without letting it forge state."

## ⚠ Operational findings needing attention regardless of this project

- **`porterly_dev` local checkout tracks a stale mirror** missing security fixes — use `john/porterly_erp`
- **Live CSRF-via-GET**: `event_extend/controller/main.py:682-702` — privileged `sudo()` state changes on bare GET routes
- **Zero `domain_force`/ir.rule across all 289 Porterly modules** — access control is controller discipline only
- **AEMI's AI layer was found dead in production** (missing API key)
- **Only one Porterly module carries a freely-reusable licence** (`pways_adv_parcel_management`, AGPL-3); everything else is OPL-1 or proprietary, so reuse needs a deliberate relicensing decision per module
- **🔴 Two bodies of load-bearing work exist only on this Mac, unpushed** — `addons/aemi_ai_platform/` (untracked, 34 passing tests) and `~/hermes-console` (3 commits ahead of `forgejo/main`, carrying Fabio's entire tool-calling path). See `internal/02` §3
