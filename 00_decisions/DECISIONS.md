# Marshal — decision log

Durable record of what has been decided, by whom, and on what evidence.
Newest first. **A decision here is settled** — reopen it deliberately, not by
drift.

---

## D-008 · Per-facility headless infrastructure · the fork is resolved
**2026-08-06 · John, primary source · SETTLED**

> *"I would not run it. It should be an infrastructure tool per facility that is
> headless and auto-coordinates and has some few humans in the loop and checks
> and balances — such as the condition of equipment and fuel, and if the
> equipment was returned to the right position."*

**Neither branch A nor B. A third shape** — infrastructure installed at a
facility, single-tenant, running on its own, humans only where physical reality
must be confirmed.

- **Drops multi-tenancy entirely** — the largest source of complexity in a
  scheduling product, gone. Each install knows one building, which is the only
  scope where the physics makes sense
- **Headless: the scheduler is the product, every screen is a client.** Kill the
  wall board and the facility still runs, degraded not stopped. That is what
  makes it infrastructure rather than an app
- **Auto-coordination loop:** observe → reconcile → plan → act → **verify**.
  Humans appear at *verify* only
- **🔑 Humans are sensors, not operators.** The system's model drifts from the
  world; checkpoints re-anchor it. Cheap sensor (camera motion, D-006) runs
  constantly; expensive sensor (human checkpoint) runs where being wrong is
  costly. **Nobody's job is "operate Marshal"** — if such a role appears, the
  design has failed
- **Q-3 RESOLVED: Odoo.** Single-tenant, record-heavy, and native `maintenance` +
  `fleet` cover equipment condition and fuel logs

**edata+ reviewed on the Porterly iMac** (`/Volumes/iMac`, 179 MB, 52 Odoo-15
modules). **Correction to the recollection: it has NO physical-equipment
maintenance, condition or fuel tracking** — `itm`'s "equipment" is IT assets
(CPU/RAM/IP), and native `maintenance` is unused across the whole archive except
one icon file. What it *does* contribute, all cleanly licensed:
`quality_control_oca` (AGPL-3) is the checkpoint engine and a direct hit;
`base_rest`+`component` (LGPL-3) is the headless API layer; `frepple` (AGPL-3)
is a real finite-capacity planner worth comparing to OdooIQ before Phase 2.
**Bryntum Gantt is commercially licensed — do not build the UI on it.**

Full detail: `01_product/09_headless_architecture.md`,
`03_internal_assets/03_edata_plus_inventory.md`.

---

## D-007 · Record before decide · plan sequenced, fork deferred
**2026-08-06 · SETTLED**

**`Record → Coordinate → Schedule → Meter → Predict`.** Deliberately not
schedule-first. Three reasons: we have no duration data, so an optimiser would
be confidently wrong and burn credibility we get once; the safety record and the
metering are the strongest parts of the case and **neither needs an optimiser**;
and recording generates exactly the calibration data the optimiser later needs.

Marshal earns trust as a **system of record** before it becomes a system of
decision.

**Q-7 CLOSED** by primary source — lifts and elevators are first-class scheduled
resources, coordinated with arrival and dock times, along with equipment
(electric/standard forklift, pump truck, specialized cart). See
`01_product/08_resource_model.md`. **Equipment is not fungible**; substitution is
directional; the model is `avn.capability`'s contract pattern in a new domain.

**The A/B fork — product vs operating system for a services business — is
deliberately deferred.** Phases 0 and 1 are identical under both, so the decision
can be made *with* Phase-1 evidence instead of ahead of it. It bites at Phase 2–3.

Full plan: `PROJECT_PLAN.md`.

---

## D-006 · The camera is the interface · Reolink confirmed on site
**2026-08-06 · John, primary source · SETTLED**

> *"Ease of use and use of live video feed are both important. The video cameras
> are Reolink."* — and confirmed we already have the integration.

**These are one requirement, not two.** An ops person at 6am looks at the door,
not at a Gantt chart. Any product that makes them translate between schedule and
reality has lost. So the primary surface is **a wall of dock camera tiles, each
overlaid with what is scheduled there right now** — not a schedule with video
bolted on. No vendor in any researched category does this.

**Verified by direct read** of `~/hermes-console/api/mcp/clients/reolink.py`
(present in `qnap/hermes-console.git` — pushed and safe):

- ✅ Working: camera auth/command layer, `get_dev_info`, **`get_motion_state`**,
  `get_snapshot_url`, multi-camera config from env
- ❌ **NOT built: live streaming.** The client says so itself at line 16 —
  *"Hermes does NOT stream video."* RTSP/FLV is new work. **Never claim we have
  live video; we have snapshots, motion state, and a working integration**

**Motion state is the sleeper asset.** `spec/03` said instrument actuals in v1
but couldn't solve the obvious weakness — nobody types a variance reason at 6am.
Motion state removes the ask: motion during a scheduled window means it happened;
silence means it didn't; **motion with nothing scheduled is a safety exception.**
That is automatic actuals capture from hardware already on the wall, and it is
what the entire predictive layer rests on.

**Snapshot refresh (2–5s) probably beats live streaming for the wall board** —
an `<img>` rather than a player, low bandwidth, trivial reconnect, and enough to
answer "is door 4 clear?". Reserve true streaming for supervising a live movement
and for incident review, as a click-through from a tile.

Full reasoning: `01_product/07_video_and_ease_of_use.md`.

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
| **Q-11** | **Is Reolink motion detection reliable at dock distance and in dock lighting?** | **The cheapest de-risking test in the project.** Point the existing client at one camera on one dock, log motion state against a known schedule for one show. No product needed. Validates automatic actuals capture — which the whole predictive layer rests on |
| **Q-13** | **Equipment: venue-owned, contractor-supplied, or exhibitor-brought?** | Determines who schedules and who bills it — feeds Q-1′ |
| **Q-15** | **Who controls the freight elevator calendar in a hotel, and in what system?** | If it's a person not a system, `avn.capability`'s human_workflow tier is day-one critical |
| Q-14 | How many electric units and chargers per venue, and real runtime? | Decides whether battery-charge modelling is critical |
| Q-16 | Venue rules barring LP/diesel units indoors? | A hard safety constraint the scheduler must never violate |
| Q-17 | Is operator certification tracked today, and where? | Free compliance win if we hold it |
| Q-6 | Hotels or convention centres first? | Leaning **hotels** — worse constraints, no embedded incumbent, more of them, existing relationships |
| Q-12 | Wall board in the dock office only, or a driver-facing display in the yard too? | Radio traffic is a proxy for coordination the system is failing to do |
| Q-7 | Is the freight elevator the true serial constraint in hotels? | Decides whether vertical transport is a first-class resource in the solver |
| Q-9 | Who carries liability for a floor incident — facility or show manager? | The safety framing only sells to whoever holds the risk |
| Q-10 | Is French-language SMS required for Quebec (Bill 96)? | Cheap to design in now, expensive to retrofit |
| Q-2 | Register `dock.show`? | Still available. Cheap. Decide before someone else does |
| **Q-18** | **Where does Marshal run — facility hardware or our cloud with a local agent?** | "Infrastructure per facility" implies on-prem; Law 25 and hotel IT policy may require it |
| **Q-19** | **What happens when the network drops mid-move-in?** | Infrastructure must degrade gracefully. A dock cannot stop because a WAN link did |
| Q-20 | Handheld: operator's own phone or facility-provided device? | Decides whether checkpoints are web or native |
| Q-21 | Who administers an install — facility IT or us remotely? | Support model and update path |
| ~~Q-3~~ | ~~Odoo or standalone?~~ | **RESOLVED by D-008 — Odoo.** Single-tenant, record-heavy, native maintenance+fleet |
| Q-4 | Is the Show Board's information-exchange model defensible? | **Needs counsel, not engineering.** Antitrust-sensitive in both Canada and the US. The constraint shapes the data model |
| Q-5 | Which venue is the design partner? | Now likely a Toronto hotel, from existing relationships |
