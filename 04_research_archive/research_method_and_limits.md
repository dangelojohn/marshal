# Event / Exposition Services Platform — competitive research & design

**Folder note:** created at the path given (`Event Renal`). Likely intended
"Event Rental" — rename freely, nothing here depends on the folder name.

**Scope:** research the competitive landscape around Goodshuffle Pro and its
adjacent categories, then specify a new entrant built on our existing Odoo
assets as an **agentic, minimal-surface** product — **show-manager centric and
facilities centric**, Canada first, US-capable.

---

## The reframe that shapes everything here

The brief names Goodshuffle Pro as the anchor, but the two stated centres of
gravity — **show manager** and **facilities** — sit outside party rental.

Party-rental software sells *inventory availability* to the company that owns
the chairs. A show manager and a facility care about something else: an event
floor where **many exhibitors order many services from many suppliers against
one venue's constraints and one show's timeline.**

That is the **exposition services** category — booth, electrical, rigging,
material handling/drayage, AV, furniture, internet, labour, cleaning — plus
**venue/facility booking** underneath it.

**This is why our own assets fit.** AEMI's `aemi.service.request` already
carries the polymorphic type list `booth / shipping / rental / power / print /
dropoff / av / other`. That *is* an exhibitor service order. The demand-side
model already exists.

So the landscape is researched across **six categories**, not one.

---

## Categories researched

| # | Category | Why it's in scope |
|---|---|---|
| 1 | Event & party rental software | The named anchor (Goodshuffle and direct peers) |
| 2 | AV / production / staging rental | Closest on scheduling sophistication — gear *and* crew |
| 3 | General & e-commerce rental platforms | Where the low-cost/self-serve pressure comes from |
| 4 | **Exposition services contractors** | Freeman, GES, Shepard — the real incumbents for show services |
| 5 | **Show management platforms** | Floor plans, exhibitor management, the show manager's daily tool |
| 6 | **Venue / facility booking** | The facilities half of the brief |
| 7 | **Canada specifics** | Market structure, venues, labour rules, bilingual obligations |

---

## Method and honest limits

Research ran as parallel low-cost agents, one per category, each writing to
`competitors/`.

### ⚠ The constraint that matters

**This session's WebSearch budget was exhausted before the work began.**
Agents retained `WebFetch` — they can retrieve **known URLs** directly — but
could not *discover* vendors by searching.

Practical consequence for a competitive sweep:

- Coverage is good for vendors we could name in advance and whose sites
  respond to automated fetch.
- Coverage is weak for **regional Canadian players, recent entrants, and
  anyone we didn't already know to look for** — precisely where a competitive
  study most needs discovery.
- Pricing is frequently quote-gated in this category regardless of search.

**Every claim is tagged:**

- `[SOURCED]` — retrieved from a cited URL this session
- `[VENDOR]` — from the vendor's own published material
- `[INDUSTRY-COMMON]` — established knowledge, not individually sourced here
- `[UNVERIFIED]` — recall that must be checked before use
- `[SPECULATIVE]` — inference, explicitly not a finding

**Treat the vendor roster as a strong starting list, not a complete census.**
Re-run the discovery pass with search enabled before any competitive claim
goes into a business plan or investor material.

---

## Internal asset review

`internal/` holds the review of what we already own and can reuse. Forgejo
repositories inspected:

- **`john/aemi-platform`** — the AI-OS layer: agentic mixin, portal ownership
  mixin, append-only observations, attention engine, service request model
- **`aug2026/porterly`**, **`john/porterly_erp`**, **`john/porterly_ops`**,
  `qnap/porterly*` — event logistics: parcels, courier, jobs, tickets,
  shipment requests, the planner-built event stack
- **`qnap/odooiq-factory-intelligence`** — deterministic calibrated scheduler
  with confidence ranges (directly relevant to agentic scheduling)
- **`qnap/hermes-console`**, **`qnap/odooai`**, **`qnap/ops`** — agent/console
  and operations layers
- **`qnap/southbrook-v19cr`** — governance patterns worth stealing: versioned
  specs, as-sold pinning, four-eyes approval, immutable audit

---

## Deliverables

| Path | Contents |
|---|---|
| `competitors/` | One file per category, plus a cross-category synthesis |
| `internal/` | What we own, what's reusable, what's a trap |
| `spec/` | The design specification for the new entrant |
| `00_README_and_method.md` | This file |
