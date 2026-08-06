# Marshal — decision log

Durable record of what has been decided, by whom, and on what evidence.
Newest first. **A decision here is settled** — reopen it deliberately, not by
drift.

---

## D-012 · Surface map — one per role
**2026-08-06 · John · SETTLED**

> *"Receivers get iPhone, runners get Apple Watch, managers get web interface,
> customers get SMS and a web portal."*

| Role | Surface | State |
|---|---|---|
| **Receiver** | **iPhone** — capture, evidence, custody | ✅ **LIVE** (Porterly Inbound PWA) |
| **Runner** | **Apple Watch** — one movement, two taps | ❌ New |
| **Manager** | **Web** — wall board + coordinator | ❌ New |
| **Customer** | **SMS + portal** | Portal ✅ **LIVE** (Outbound PWA) · SMS designed only |

**🔑 Five surfaces is FEWER, not more.** The original brief asked for *"as few
surfaces as possible"* and `spec/01` proposed three — but the metric was wrong.
**What matters is how many surfaces any ONE PERSON must learn. Here it is one.**
`spec/01`'s three were *role-spanning* (a shared console for venue ops AND show
managers), so both had to navigate past the other's concerns. Role-scoped
surfaces where nobody sees another role's screen are simpler for every
individual. **This only works because of D-008 — one headless core, N
renderings. Adding a surface costs a client, not a system.**

**"Customer" is three parties with diverging needs:** driver/carrier = **SMS
only** (in a truck, will never log in) · exhibitor = portal + SMS · show manager
= portal, read-only.

**⚠ Gap this exposes (Q-42): equipment checkpoints have no home.** Runners only
carry watches, but condition/fuel/position need eyes, probably a photo, and more
than two taps. **Recommendation: a shared tablet at the equipment/charging bay** —
checkpoints are *location-bound*, not person-bound; they happen where the machine
is parked, at shift start and end. Keeps the watch to two taps, needs no
per-person hardware.

**Q-38 RESOLVED** — facility-provided, Apple ecosystem. So Watch **Ultra** for
the Action Button (gloves), not a standard Watch.

**Half the surface area is already in production.** New work concentrates exactly
where Marshal is differentiated: the runner's watch, the manager's board, and the
coordinator loop underneath.

Full detail: `01_product/14_surface_map.md`.

---

## D-011 · Porterly Design corpus is the backlog · wrist surface adopted
**2026-08-06 · SETTLED**

**`~/Downloads/Porterly Design`** — 461 files, 344 markdown, July–Aug 2026.
**Porterly v2's 26 hardened recommendations are substantially Marshal's Phase 1–3
backlog**, already scored by a 4-reviewer panel with a hard feasibility veto, on
**Odoo 16 CE** — exactly Marshal's target since D-010. Only 2 of 28 candidates
cleared first pass; the survivors were re-scoped to what this team can run.

**Directly adopted:** R25 testing/CI + migration harness (**linchpin, ship
first**) · R13 fail-closed access + tenant isolation (keystone) · **R04
tamper-evident custody log — use the REVISED mechanism: per-parcel hash chain +
periodic anchor, NOT a global chain** (FZ 6 was the CE feasibility reality) ·
R07 maker-checker billing (highest-scored, *no silent charge ever*) · R02
point-in-time custody snapshots · R03 effective-dated pricing · R16 task→billing.
**Wave 0 = R25 + R13 + `porterly_core` kernel, and that's right for Marshal too.**

**⭐ Validates the thesis from a different direction.** Porterly's own analysis:
at label capture the system already knows it holds one of **two different
products** — guest incidental mail (*expects NOT to pay*, hotel relationship at
risk, should be a free amenity) versus **exhibitor/event logistics (expects to
pay — freight is a known show cost, priced by weight/dims/storage/accessorials)**.
**Marshal is the second column.** D-005 §2 reached independently, months earlier.

**⭐ Fourth independent convergence on the LLM boundary:** *"perception is
probabilistic, actuation is deterministic — an LLM may read and propose, only a
typed idempotent core may act."* With `PLM_LIFECYCLE`, porterly-future-reference
and hermes-console, that's four. **Treat it as settled doctrine, not a choice.**
Also: a big-bang rewrite **scored ~45%** and lost to strangler-fig + shadow mode
+ kill-switch.

**Q-30 ANSWERED, precisely:** 3-shot capture, `PR###` sequence, **idempotency via
`capture_uuid`**, geo, captured-by, 90s auto-logout are **SHIPPED AND LIVE
(2026-07-21)**. The **offline outbox is R15 — designed, revised for "phase +
device limits", NOT built.** So `3 queued · syncing` in the mockup is intent, not
behaviour. **Q-19 is still real work.**
**Q-33 ANSWERED:** QuickBooks **Online**, R11 async reconciled, **one-way** —
matching D-010's boundary exactly.

**⚠ CORRECTION I owe:** I called *"zero `domain_force` across 289 modules"* a live
risk. Accurate but framed too harshly — an **Access-Control Baseline campaign was
run and completed**, and the **2026-07-24 live-`main` audit verifies every IDOR,
unauth-sudo and enumeration oracle is fixed.** The vulnerabilities were remediated
at the controller layer and independently audited. What's missing is the *ORM
backstop* — that's R13, designed and unbuilt. Guidance unchanged; the
characterisation was unfair to work that was done.

**Marshal = Porterly v2's exhibitor half + the resource layer Porterly never had.**
New work is: resource scheduling, the coordinator loop, the wall board, and
motion/tap actuals.

### ⌚ Wrist surface — ADOPTED
> *"An Apple Watch interface for the employees running the pump trucks and
> forklifts — where to go, what booth, when, with what package — and tap when
> they have arrived and delivered."*

**It's the best actuals source in the system**, not just a convenience. A tap at
*arrived* and *delivered* gives an **exact start and end per movement from the
person who was there** — better than camera motion, and cheap enough to actually
happen. **May de-risk Q-11**: motion becomes corroboration rather than primary.

- **🔑 GLOVES decide the hardware.** Apple Watch touchscreen fails with work
  gloves. **Design the primary action around the Watch Ultra's physical Action
  Button** — that single detail makes it viable. Ultra also gives ~36h battery
  and a brighter screen. **A standard Apple Watch is a poor fit**
- **If devices are facility-provided and shared across shifts, an industrial
  wrist wearable (Zebra WS50 class) beats it** — glove-designed, hot-swap
  battery, built-in scanner, shared-device login. Apple Watch is architecturally
  a *personal* device. **Q-38 decides this**
- **Costs the architecture nothing** — it's another client of the headless core.
  **First real test of D-008, and it passes**
- **Two taps per movement is the design budget.** Never photos, checkpoints,
  lists or typing — those belong on the handheld and the wall board
- ⚠ **A wearable is on a *person*.** Record the movement, never the operator's
  location between movements. No idle tracking, no leaderboards. **Get this wrong
  and the watches end up in a drawer, taking the actuals with them**

Full detail: `03_internal_assets/05_porterly_design_corpus.md`,
`01_product/13_wearable_operator_surface.md`.

---

## D-010 · Odoo 16 · Porterly is the freight layer · billing leaves Odoo
**2026-08-06 · John · SETTLED**

> *"We will be using Odoo v16 for this development and leverage the QuickBooks
> application we already own."* · *"Let Quickbooks and Stripe and the invoice
> module handle tax later."*

**Target is Odoo 16, not 19.** Porterly *is* v16, edata+ is v15 — the port cost
that dominated the earlier recommendation disappears. Trade stated once: v16 is
outside Odoo's support window, so patches become ours and a v19 move later is a
project not an upgrade. Defensible for **installed per-facility infrastructure**
(D-008); not reopened.

**Porterly Inbound/Outbound + `courier_tracking` + `event_extend` become
Marshal's freight layer** — installed in the same single-tenant Odoo, no
integration layer. **I had wrongly scoped this as new work**: `courier_tracking`
has a working invoice pipeline (`action_create_invoice` :509, `account.move.line`
:114/:129, `sale_order._create_invoices()` :595, `charge_type` :390), the inbound
PWA is a real mobile dock-capture app, and the outbound PWA has **honeypot,
rate-limit and idempotency-by-uuid** — *"a double-tap submit returns the SAME
parcel"*, which is exactly the gloved-hands dock problem.

**🔑 The billing boundary — Marshal meters, it does not bill.**
```
Marshal ──▶ priced consumption records ──▶ QuickBooks · Stripe · invoice module
(meter)      what/who/when, evidenced        (tax, invoice, collection) [LATER]
```
Better than the original plan: it's the honest scope (D-005 §2 was always a
*metering* claim), tax is solved elsewhere by tools already owned, and it keeps
the defensible thing defensible — a dispute is settled by Marshal's evidence
rather than argued inside Marshal's code. **QuickBooks and Stripe are
`tenant_bridges`** (hermes-console's pattern). Neither is Phase 1.
**Do NOT use `courier_tracking`'s `account.move` path.**

**⚠ Two debts do NOT go away with the port cost — they were never about version:**
1. **`ir.rule` from module one.** Porterly has **zero `domain_force` across 289
   modules** — 100% controller discipline, no ORM backstop. Marshal has venue,
   show manager, exhibitor and carrier on different slices; one mis-coded domain
   is a full leak. **The single most important thing not to inherit**
2. **Tests around anything lifted.** None exist anywhere in Porterly. For
   infrastructure emitting records that settle money disputes, disqualifying as-is

**Build from `john/porterly_erp`, never `~/porterly_dev`** (stale mirror, missing
Q5/Q7 fixes, still contains the retired public POST hole).

**PWA design language adopted** — the three-step capture strip
(`LABEL·PACKAGE·SHELF`) is structurally identical to Marshal's three checkpoints
(`CONDITION·FUEL·POSITION`). Offline `queued · syncing`, evidence photos +
retake, custody rail, and honest per-channel failure states all transfer. See
`01_product/12_ui_leverage_from_porterly.md`.

Full detail: `03_internal_assets/04_porterly_as_the_freight_layer.md`.

---

## D-009 · Tracking + LLM · both at the edges, never the core
**2026-08-06 · SETTLED**

**AirTags: NO as a system input.** Two fatal blockers, both deliberate design
choices by Apple and Google, neither configurable: (1) **no API** — location
lives in the Find My app only, and a data source a human must look at in another
app is not a data source for a headless system; (2) **anti-stalking alerts** —
tagged equipment moving among hundreds of exhibitor staff triggers *"an AirTag is
travelling with you"* on their phones, and any of them can make it beep. Same for
Android. *Legitimate minor use:* a human find-aid for genuinely lost carts.

**What works instead:** **BLE tags + chokepoint gateways** at docks, elevator
lobbies, charging bays and the yard gate — the same points Marshal already models
as constrained resources. Open protocols, MQTT/HTTP, no anti-stalking issue.
Marshal needs **zone-level** location (*Bay B*, *Level 3*), never coordinates,
which is why this is cheap. **Check forklift telematics FIRST (Q-22)** — Toyota,
Crown, Hyster and others already report hours, charge/fuel, impact detection and
operator ID, which answers condition and fuel better than any tag.

**Tagging automates exactly ONE of the three named checkpoints:** position ✅,
fuel ❌ (telematics or a gauge), condition ❌ (**human eyes, nothing replaces
this**). That split strengthens D-008 rather than weakening it.

⚠ **Tag equipment, never people.** Operator-ID telematics crosses into employee
monitoring — Ontario electronic-monitoring disclosure, provincial privacy law,
and collective agreements on a unionised floor. A safety product that feels like
surveillance gets sabotaged by the people it depends on.

**LLM: YES at the edges, NEVER at the core.**
- **Never:** producing the schedule, safety rules, metering/billing, anything on
  a movement's critical path, or writing state directly. The **never-invocable
  list is a checked-in, tested artifact**, enforced with a `PLM_LIFECYCLE`-style
  identity sentinel
- **Yes:** parsing what drivers actually text (*"stuck on the 401 maybe 40 min"*)
  into structured intent; **bilingual SMS — turning the Bill 96 burden into a
  feature**; explaining why the plan changed; natural-language Q&A over state;
  structuring checkpoint free-text; incident narratives (**the record is the
  evidence, the narrative is a convenience**)
- **🔑 The rule that decides the design: if the model is unreachable, the dock
  keeps running.** Every LLM feature degrades to something that still works —
  keyword SMS fallback, canned bilingual templates, unrendered facts. An
  enhancement, never a dependency
- ⚠ **AEMI's AI layer was dead in prod because no key was configured and nothing
  noticed.** Marshal needs a health check on the model path and a visible
  degraded-mode indicator
- **We own this architecture three times over:** `porterly-future-reference`
  (agents propose / core re-derives from ground truth, 74 invariant tests),
  `PLM_LIFECYCLE`, and **hermes-console — which is literally this, running
  today.** Close enough to be the starting point, not just a reference

Full detail: `01_product/10_equipment_tracking_options.md`, `11_llm_layer.md`.

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
| **Q-22** | **Do the venue's forklifts have telematics, and can we get the data?** | May answer fuel + condition + utilisation with zero new hardware. **Add to the Phase-0 calls** |
| **Q-33** | **QuickBooks Online or Desktop?** | Online has a REST API; Desktop needs a connector and changes the bridge entirely |
| **Q-30** | **Is the PWA offline queue implemented or mocked?** | If real, **Q-19 is largely answered** — one of the harder requirements |
| Q-34 | Does Stripe collect from exhibitors directly, or is it invoice follow-up? | Decides whether a payment surface is ever needed in Marshal |
| Q-28 | Does Porterly stay a live v16 product independently? | Decide now whether Marshal forks or tracks it |
| Q-23 | Which zones actually need distinguishing? | Gateway count and placement — **answer from Phase-1 data, not guesswork** |
| Q-25 | Union / works-council position on equipment monitoring? | Cheaper to know before install than after |
| Q-26 | Local model on facility hardware, or cloud with graceful degradation? | Follows Q-18/Q-19; only matters for SMS intent, the one edge feature on a live path |
| Q-27 | Does venue IT policy prohibit sending operational text to a third-party model? | Hotel/enterprise IT often does — decides whether local is mandatory |
| Q-20 | Handheld: operator's own phone or facility-provided device? | Decides whether checkpoints are web or native |
| Q-21 | Who administers an install — facility IT or us remotely? | Support model and update path |
| ~~Q-3~~ | ~~Odoo or standalone?~~ | **RESOLVED by D-008 — Odoo.** Single-tenant, record-heavy, native maintenance+fleet |
| Q-4 | Is the Show Board's information-exchange model defensible? | **Needs counsel, not engineering.** Antitrust-sensitive in both Canada and the US. The constraint shapes the data model |
| Q-5 | Which venue is the design partner? | Now likely a Toronto hotel, from existing relationships |
