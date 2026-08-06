# Marshal — decision log

Durable record of what has been decided, by whom, and on what evidence.
Newest first. **A decision here is settled** — reopen it deliberately, not by
drift.

---

## D-004 · Domain registered — `marshal.show`
**2026-08-06 · John · SETTLED**

`marshal.show` purchased. The name is no longer a proposal.

Checked and still open at time of writing: **`dock.show`** — recommended as the
Phase-1 product name (*Marshal Dock*). Re-verify before assuming.
Also open: `movein.show`, `marshall.show`, `marshaldock.com`, `marshalfloor.com`.

*Method note: macOS `whois` cannot resolve `.show` — it silently falls back to
IANA and reports the TLD record, so whois checks of these names return
nonsense. Use RDAP (`https://rdap.org/domain/<name>`, 404 = available).*

---

## D-003 · The name is Marshal
**2026-08-06 · SETTLED**

A *marshalling yard* is the exact industry term for where trucks stage before a
dock. The product is named after the job it does, and the verb travels as the
product grows from trucks to crews to whole shows — where "Dock" or "Bay" would
box it in at Phase 1.

`marshal.show` reads as *"marshal the show."* In this industry the TLD does
semantic work rather than apologising for a missing `.com`.

Collision considered and accepted: Marshall Amplification (double-l, different
category) and the law-enforcement sense. Neither competes for attention in a
convention-centre ops context.

**Rejected:** Dock (boxes in at Phase 1), Bayline, Yardline, Apron, Tarmac,
Load-In. Single-word `.com` for all of these is taken.

---

## D-002 · Enter at the dock, not the platform
**2026-08-06 · SETTLED**

Build dock and marshalling-yard scheduling first. **Not** the full
exposition-services platform, which needs venues, exhibitors and contractors to
adopt simultaneously — three stacked cold starts in a category with no network
effects.

**The decisive reason:** service exclusivity is venue-granted per service and
blocks every other entry point. **Dock and yard access is always the venue's
own**, so Marshal sells into a venue without touching an exclusive contract or
asking GES or Freeman for anything.

Supporting: the category is proven next door (Opendock, C3, Transporeon in
warehousing) but structurally un-crossable — warehouse dock scheduling assumes
steady state and repeat carriers; expo move-in is a surge with precedence and
spatial exclusion.

Full reasoning: `01_product/01_what_we_are_building.md`.

---

## D-001 · Sell the venue, don't fight the contractors
**2026-08-06 · SETTLED — from the market research**

Four findings that constrain everything downstream:

1. **Don't build rental software** — $29/mo price floor (Booqable), Odoo ships
   Rental free with buffers built in. No defensible business.
2. **Don't fight GES/Freeman** — their moat is labour and trucks. Software is a
   cost centre they refresh on roughly a decade cadence. Code can't beat it, and
   they won't out-build us either.
3. **Sell the venue** — the only party whose P&L moves on better scheduling.
4. **The seam is proven, not theorised** — GES's live Expresso portal makes
   exhibitors search for their own booth with an **"I Don't Know"** option and a
   "Create One Here" fallback. Booth data demonstrably does not flow from
   show-management platforms into service ordering.

Evidence: `02_market_research/`.

---

# Open questions — not yet decided

| # | Question | How to resolve it |
|---|---|---|
| Q-1 | Is Phase 1 (venue) or Phase 4 (contractor early-warning) the better first sale? | **Two phone calls.** Ask a venue ops director the cost of an hour of dock idle during move-in; ask a contractor the cost of late scope-change notice. Both numbers are already on someone's books |
| Q-2 | Register `dock.show`? | Still available. Cheap. Decide before someone else does |
| Q-3 | Odoo-based or standalone? | Depends on Q-1 — a contractor-first product argues for standalone; venue-first argues for Odoo, where we own more |
| Q-4 | Is the Show Board's information-exchange model defensible? | **Needs counsel, not engineering.** Competing venues seeing each other's availability is antitrust-sensitive in both Canada and the US. Get an opinion before building it — the constraint shapes the data model |
| Q-5 | Which Canadian venue is the design partner? | Market is fragmented (Ottawa splits two contractors across two venues) — that helps a venue-side product. No incumbent to dislodge |
