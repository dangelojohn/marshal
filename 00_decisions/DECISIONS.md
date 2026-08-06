# Marshal — decision log

Durable record of what has been decided, by whom, and on what evidence.
Newest first. **A decision here is settled** — reopen it deliberately, not by
drift.

---

## D-005 · Venue pain CONFIRMED · it's a safety and revenue product
**2026-08-06 · John, primary source · SETTLED**

From direct experience building ERPs for top Toronto hotels with event
operations. **This closes the riskiest assumption in the project** — that a
software gap might not be a felt pain. It is felt: move-in and move-out days are
"crazy" and need scheduling.

Five things changed as a result. Full detail in
`01_product/06_operating_model_v2_sourced.md`.

1. **Safety first, efficiency second.** Forklifts and pump trucks in tight
   spaces is the hazard; scheduling is the control. Changes the buyer (risk, not
   just ops), the budget (less discretionary), and the killer feature — a
   **defensible record of who moved what, where, when, with which equipment**.
   Nothing on the market can answer "what was supposed to be happening there?"
   after an incident.
2. **Revenue, not cost avoidance.** Docks and material handling are *already
   billable*, and metered on paper — so they leak. Marshal meters what it
   schedules. *"You billed 40 hours. The floor consumed 62."*
3. **The constraint is not the dock door.** It is the **specialised handling
   resource and its route** — equipment + certified operator + a tight path to a
   specific booth. **The schedulable unit is a movement, not a slot.**
4. **SMS is the vendor surface**, not a portal. Drivers are in a truck and will
   not log in. Vindicates `avn.capability`'s connector-maturity ladder.
5. **Three billing parties, not two.** Facility *provides* handling; **show
   management often bills it**; exhibitor pays. Whoever holds that margin has the
   reason to meter it.

**Also:** hotels may be the better beachhead than convention centres — worse
constraints, no embedded GES/Freeman, far more of them, and existing
relationships. Does not weaken D-002; strengthens it.

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

**Q-1 is superseded by Q-1′.** D-005 confirmed the pain, so the question is no
longer *whether* the venue hurts but *who holds the money*.

| # | Question | How to resolve it |
|---|---|---|
| **Q-1′** | **Who captures the material-handling margin today — the facility or the show manager — and who wants it back?** | Determines who the invoice is addressed to, and therefore the buyer. Ask a facility ops director and a show manager the same question |
| **Q-8** | **What is charged today, and on what unit** — dock hour, crate, pallet, weight? | **The metering model must match the existing billing unit or it won't be adopted.** Blocks the strongest part of the business case |
| Q-6 | Hotels or convention centres first? | Leaning **hotels** — worse constraints, no embedded incumbent, more of them, existing relationships |
| Q-7 | Is the freight elevator the true serial constraint in hotels? | Decides whether vertical transport is a first-class resource in the solver |
| Q-9 | Who carries liability for a floor incident — facility or show manager? | The safety framing only sells to whoever holds the risk |
| Q-10 | Is French-language SMS required for Quebec (Bill 96)? | Cheap to design in now, expensive to retrofit |
| Q-2 | Register `dock.show`? | Still available. Cheap. Decide before someone else does |
| Q-3 | Odoo-based or standalone? | Depends on Q-1′. Metering + billing argues strongly for Odoo, where we own the most |
| Q-4 | Is the Show Board's information-exchange model defensible? | **Needs counsel, not engineering.** Antitrust-sensitive in both Canada and the US. The constraint shapes the data model |
| Q-5 | Which venue is the design partner? | Now likely a Toronto hotel, from existing relationships |
