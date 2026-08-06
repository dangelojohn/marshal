# Design Specification — an agentic show-floor operations platform

**Working name:** FLOOR
**Positioning:** infrastructure between the venue, the show manager, the service suppliers and the exhibitor.
**Built on:** Odoo (our existing AEMI / Porterly / OdooIQ assets)
**Market:** Canada first, US-capable
**Status:** design specification. Nothing built. No code written to produce this.

Evidence base: `../competitors/01`–`08`, `../internal/01`. Read
`../00_README_and_method.md` for the sourcing constraint before quoting figures.

---

## 1. The thesis

Nine research tracks converged on one position:

> **Do not build rental software. Do not try to displace the general service
> contractors. Build the coordination layer that neither the show-management
> platforms nor the contractors have built — and sell it to the venue.**

Three findings force this:

**Rental scheduling is commoditised.** Published floor is $29/month; Odoo ships
it free. There is no defensible business in availability calendars.

**The contractors' moat is labour and trucks, not software.** Their ordering
portals refresh on a decade cadence because revenue comes from drayage weight
and labour markup, not the interface. Code cannot beat that moat — but it also
means they will not out-build us on software, because software isn't where they
compete.

**The venue is the one party whose P&L moves on better software.** Facilities
optimise utilisation, turnaround density and exclusive-service capture.
Turnaround is a scheduling problem. Nobody has automated it.

### The proven gap

An exhibitor ordering booth services today re-keys their identity across three
or more logins. A major contractor's live ordering portal asks the exhibitor to
**search for their own booth by company name, with an "I Don't Know" option and
a "Create One Here" fallback** — proof in production that booth data does not
flow from the show-management system into service ordering. The only bridging
artifact found anywhere in the research is a one-way DXF/PDF export.

**That seam is the product.**

---

## 2. What we are explicitly NOT building

Discipline here is the specification's most load-bearing section.

| Not building | Why |
|---|---|
| A rental availability/booking system | Commoditised. Odoo gives it free |
| A general service contractor | Their moat is labour, trucks and union relationships |
| A show-management platform | Map Your Show and a2z own floor plans and booth sales; integrate, don't replace |
| An attendee/registration product | Different buyer, different sale, no adjacency |
| A CRM | Odoo has one |
| Customs/carnet tooling | Already absorbed as a broker service — not a software gap |
| Anything that becomes "one more login" | The category's defining failure |

---

## 3. The wedge

**Sell to Canadian venues first.** Reachable set (roughly a dozen major
facilities), P&L-tied ROI, no national contractor lock — Ottawa alone splits
between two different contractors across its two venues — and a **dated
regulatory moat**: Bill 96's French-availability deadline passed in June 2025
and Law 25 requires a privacy impact assessment before personal data leaves
Quebec. A bilingual, Canadian-hosted platform clears both by construction.
American incumbents mostly do not.

Show managers are the second wedge, entered *through* the venue relationship.
Exhibitors and rental companies are weak entry points — no budget authority and
a commoditised product respectively.

**Land on turnaround and dock scheduling. Expand into the ordering seam.**

---

## 4. Surfaces — the budget

The brief demands as few interfaces as possible. **Three surfaces, and one of
them is not a screen.**

### Surface 1 — The Console *(Odoo backend, role-scoped)*
One console. Venue operations and show management see the same records through
different role scopes rather than different applications. Their data is the
same floor, the same dates, the same services — splitting it into two products
would be the fragmentation we exist to remove.

### Surface 2 — The Order Page *(portal; mobile-first, bilingual)*
One page per exhibitor per show. Their booth, their services, their deadlines,
their money. No dashboard, no navigation tree, no second login.

### Surface 3 — The Capability Adapter *(not a UI)*
Suppliers and venues integrate at whatever maturity they actually have. Lifted
directly from AEMI's `avn.capability` — **verified by direct source read**, not
inferred:

```
CONNECTOR_TYPES    mcp | api | portal | web_form | email | human_workflow
CONNECTOR_MATURITY human_workflow 0 → email 1 → web_form 2 → portal 3 → api 4 → mcp 5
SIDE_EFFECTS       read | advisory | executable
```

The load-bearing detail: **`contract()` deliberately excludes
`connector_type`.** A venue with a REST API and a venue with only a human
bridge expose the *identical* contract — the caller cannot tell them apart and
never branches. `invoke()` dispatches internally and every strategy returns a
normalised envelope, so a venue upgrades `web_form → api → mcp` with **zero
change to calling code**.

Two further facts that shorten the build materially:

- **`side_effect` already encodes the advisor/actor boundary** required by
  §6.5. The governance line is an existing field, not new work.
- Its own documented capability examples **already include "Loading Dock
  Schedule"** — the exact gap the research found unserved across all nine
  venue platforms.

**This is the highest-leverage asset we own.** One venue has an API. The next
has a web form. The third has a person who reads email. All three onboard
behind one interface, and any of them can be upgraded later without changing a
single caller. Competitors assuming API-first cannot onboard the third venue at
all.

### The surface we deliberately do not build

**No dashboards.** Every dashboard is a surface, and a dashboard is what you
build when the software cannot decide anything. Instead: **one Decision Inbox**
— a single prioritised queue of things needing a human, generalised from AEMI's
attention engine. A scheduling conflict, a shortage, a dock clash and a deadline
breach all arrive in the same queue with a recommended action attached.

> **N dashboards collapse into 1 inbox. That is how the surface count stays low
> while capability grows.**

---

## 5. Domain model

Core entities, kept deliberately small.

| Entity | Notes |
|---|---|
| `floor.venue` | Facility, halls, capacities, **exclusivity rules per service type** |
| `floor.show` | An event at a venue: move-in, show days, move-out |
| `floor.space` | Hall/room/booth — bookable, with buffer semantics |
| `floor.exhibitor` | Per show; the identity that must stop being re-keyed |
| `floor.service.catalog` | What can be ordered at this venue for this show |
| `floor.order` | An exhibitor's service order (generalised from `aemi.service.request`) |
| `floor.supplier` | With a **capability profile** (§4, Surface 3) |
| `floor.window` | **The scheduling primitive — see §6** |
| `floor.dock` | Loading dock slots. A confirmed market gap |
| `floor.decision` | An item in the Decision Inbox |

**Exclusivity is a first-class constraint, not configuration.** Venues grant
exclusive rights per service — electrical, rigging, internet, catering — often
to *different* suppliers, and one electrical firm holds exclusivity at 50+
venues independent of the contractor. A platform that treats this as a
preference will produce illegal orders.

---

## 6. Agentic scheduling — the core

### 6.1 The primitive: the window, not the booking

Stolen from the best idea found in AV rental software: schedule at **line-item
sub-window** granularity — `Prep · Travel · Setup · In-Use · Strike · Return` —
rather than booking a single opaque block.

This is what makes turnaround computable. A hall is not "busy 9–5"; it is
unavailable from the first delivery through the last strike, and *those windows
are derivable from the services ordered.* No venue platform researched does
this — only a general-purpose room-booking tool documents even a simple buffer
mechanic.

**The agent's first job: populate these windows automatically from the order,
instead of a human typing them.**

### 6.2 Estimates are ranges, and they widen honestly

Lifted wholesale from OdooIQ factory intelligence, which is already built and
verified read-only:

- capacity as free time-intervals per resource per day
- per-scope **median/MAD** correction with sample-size-gated trust blending
- **p10/p50/p90 outputs that widen when data is thin** — never a false point
  estimate

> **Never collapse a range and its basis into a bare time.** The honesty *is*
> the product. A confidently wrong move-in time is worse than an honest window.

### 6.3 Shortage is a warning, never a block

Confirmed in two independent AV products: shortages surface as badges and
dashboard tiles with an **inline resolution action**, never a refusal. In
events the answer to "you are short three lifts" is never "you may not
proceed."

The agent's contribution is **ranking the resolutions** — which supplier, which
substitute, which reschedule — which is exactly the judgement every researched
tool leaves entirely to a human.

### 6.4 Where the agent genuinely adds value

Five gaps, all confirmed unserved across every vendor researched:

1. **Ranking shortage resolutions** — supplier, substitute, or move it
2. **Whole-roster labour assignment** — every tool filters, then makes a human assign
3. **Learning durations from history** — prep, travel and setup times, instead of manual entry
4. **Cross-show portfolio trade-offs** — every tool shows shortages *per job only*; the venue's real problem is across concurrent shows
5. **Dock sequencing** — a confirmed category-wide gap

### 6.5 The governance line — non-negotiable

Carried directly from the PLM programme, where it was researched against
aviation advisory systems, clinical decision support and pre-trade financial
controls:

> **The agent proposes. A human commits.**
>
> An LLM supplies neither thing an audit trail requires: no accountable *who*,
> and no reproducibility across silent model updates.

**Never agent-invocable:** confirming an order that costs money · dispatching
labour · overriding a venue exclusivity rule · changing a price · releasing a
dock slot that displaces a booked one · anything with a safety consequence.

**Agent-invocable freely:** proposing windows, ranking options, drafting
messages, flagging conflicts, predicting durations, filling the Decision Inbox.

Scheduling *placement* stays deterministic — earliest-due-date greedy with
calibration, as already built. The LLM operates in the explanation, ranking and
negotiation layer *around* the solver, never inside it. It cannot reliably
respect hard constraints, and it cannot produce the same schedule twice.

---

## 7. Canada requirements — build in, don't retrofit

| Requirement | Implication |
|---|---|
| **Bill 96** | French availability. Deadline passed June 2025. Every customer-facing string, document and email, bilingual from commit one |
| **Law 25** | Privacy impact assessment before personal data leaves Quebec → **Canadian hosting is a design constraint, not a deployment choice** |
| **Tax** | Five regimes: GST-only, GST+PST, HST, GST+QST. Place-of-supply rules on event services |
| **AODA** | WCAG 2.0 AA on the exhibitor page |
| **Currency** | CAD/USD; US exhibitors at Canadian shows are normal |

Retrofitting bilingual is far more expensive than starting bilingual. The
regulatory moat only works if we actually clear it.

---

## 8. Architecture

```
        ┌──────────────────────────────────────────────┐
        │  CONSOLE (Odoo backend, role-scoped)         │  Surface 1
        │  venue ops  ·  show manager                  │
        │  ── Decision Inbox (replaces all dashboards) │
        └───────────────────┬──────────────────────────┘
                            │
        ┌───────────────────▼──────────────────────────┐
        │  CORE (Odoo modules)                         │
        │  venue · show · space · exhibitor · order    │
        │  window · dock · supplier · decision         │
        │  ── exclusivity + deadline rules (data)      │
        └───────┬───────────────────────┬──────────────┘
                │                       │
    ┌───────────▼──────────┐  ┌─────────▼─────────────┐
    │ SCHEDULER            │  │ AGENT LAYER           │
    │ deterministic        │  │ advisory only         │
    │ EDD-greedy + median/ │  │ ranks · drafts ·      │
    │ MAD calibration      │  │ explains · predicts   │
    │ p10/p50/p90 ranges   │  │ fills Decision Inbox  │
    │ (LIFT from OdooIQ)   │  │ (LIFT hermes pattern) │
    └──────────────────────┘  └───────────────────────┘
                │                       │
        ┌───────▼───────────────────────▼──────────────┐
        │  CAPABILITY ADAPTER  (LIFT avn.capability)   │  Surface 3
        │  mcp → api → portal → web_form → email →     │
        │  human_workflow — one contract, any maturity │
        └───────┬──────────────────────────────────────┘
                │
     venues · exclusive suppliers · GSCs · carriers

        ┌──────────────────────────────────────────────┐
        │  ORDER PAGE (portal, mobile, EN/FR)          │  Surface 2
        │  one page · one booth · one show             │
        └──────────────────────────────────────────────┘
```

---

## 9. Reuse manifest

**40–60% exists already — and it is the hard part.** Two independent inventory
passes produced 35–40% and 55–60% respectively; they measured different scopes
(see `../internal/01` §Reconciliation). Re-measure per module before planning a
sprint. What's missing is domain extraction and integration across repos, not
the difficult architecture.

> ⚠ **Fork warning.** `aemi.service.request` — the single best-fit asset, whose
> type list is *already* `booth/shipping/rental/power/print/dropoff/av/other` —
> lives in an **uncommitted, never-deployed** line that has **zero model
> overlap** with the live deployed repo. Commit it before building on it.

| Asset | From | Verdict |
|---|---|---|
| `avn.capability` connector abstraction | aemi-platform | **LIFT** — the single most valuable asset |
| Scheduler: EDD-greedy, median/MAD calibration, p10/p50/p90 | odooiq-factory-intelligence | **LIFT the architecture** (pure-Python, portable) |
| `aemi.service.request` (booth/power/AV/shipping types) | aemi-platform | **GENERALISE** → `floor.order` |
| Attention engine (monitor + attention item) | aemi-platform | **GENERALISE** → Decision Inbox |
| Portal ownership mixin (IDOR-safe, zero sudo) | aemi-platform | **LIFT** |
| Agent runtime: claim/heartbeat/complete | aemi-platform | **LIFT** |
| Recommend → human-approve → push loop | hermes-console | **LIFT the pattern** |
| Booth freight / parcel logistics | Porterly (METISA-owned) | **LIFT domain, rewrite controllers** |
| Four-eyes gate, row-lock race guard, as-sold pinning | southbrook-v19cr | **GENERALISE** |

### Traps — must not inherit

- **Zero `ir.rule` backstop across 289 Porterly modules.** Access control is
  100% controller discipline. **The new build declares record rules from
  module one.**
- **A live CSRF-via-GET hole** — privileged `sudo()` state changes on bare GET
  routes. Do not copy that controller shape.
- **AEMI's AI layer was found dead in production** (missing API key).
  "Deployed" ≠ working; verify before depending on it.
- **Hermes auth is a no-op** relying on network topology. Fine behind
  Cloudflare Access, unsafe standalone.
- **No tests anywhere in Porterly.** Anything lifted arrives untested.
- **The local `porterly_dev` checkout tracks a stale mirror** missing security
  fixes. Work from `john/porterly_erp`.

---

## 10. Phasing

**Phase 0 — Prove the window.** Model one Canadian venue: halls, exclusivity
rules, one real show's move-in/move-out. Generate windows from a service order.
Show a venue manager their own turnaround, computed. *Exit: they recognise it
as correct.*

**Phase 1 — Decision Inbox + deterministic scheduler.** Lift the OdooIQ
scheduler. Conflicts, shortages and dock clashes arrive in one queue with
ranked options. No agent yet. *Exit: a scheduler uses it for a real show.*

**Phase 2 — The Order Page.** Bilingual, mobile, one page per exhibitor.
Booth identity flows from the show record — the exhibitor never types their
booth number. *Exit: an exhibitor completes an order without a second login.*

**Phase 3 — Capability adapters.** Onboard three suppliers at three different
maturities — API, web form, email. *Exit: all three work through one contract.*

**Phase 4 — Agents.** Advisory only, into the existing inbox: rank
resolutions, predict durations, draft supplier messages. *Exit: recommendations
accepted at a measured rate, with attribution recorded.*

**Phase 5 — Cross-show portfolio.** The capability nobody has.

---

## 11. Risks

| Risk | Mitigation |
|---|---|
| Becoming "one more login" — the category's defining failure | Three surfaces, hard-capped. Exhibitor identity flows from the show record |
| Boiling the ocean on service/jurisdiction modelling | One venue, one show, real data, Phase 0 |
| Enterprise RFP sales cycles vs SMB assumptions | Venues are procurement-driven. Budget 9–18 months |
| Bespoke work per deal collapsing margin | Capability adapters absorb variance instead of forks |
| Exclusivity contracts block us | Route around, never compete. We coordinate suppliers, we don't replace them |
| Seasonality wrecks SaaS cash flow | Price per show or per square foot, not per seat |
| Agent erodes into decision-maker | The never-invocable list (§6.5) is architectural, not policy |

---

## 12. Open questions for the owner

1. **Do we have a venue relationship to start from?** Phase 0 needs one real
   facility's cooperation. Without it this is speculative.
2. **Is this a product or a services business?** The research is clear that
   incumbents monetise services and treat software as a cost centre. Are we
   selling software, or using software to sell coordination services?
3. **AEMI overlap** — AEMI is an association *and events* management company
   with the service-request model already built. Is FLOOR a product AEMI uses,
   a product AEMI sells, or a separate venture?
4. **Which Canadian venue is reachable first?** Determines everything about
   Phase 0.
5. **Do we accept the ~9–18 month enterprise sales cycle**, or does this need
   to pay sooner?

---

## 13. Evidence caveat

The session that produced the supporting research had **no web-search
capability** — agents could fetch known URLs but not discover vendors. Coverage
is therefore weak on regional Canadian players and recent entrants, and no
Canadian market-size figure could be sourced at all (it appears genuinely
untracked). Several vendor sites blocked automated access; those failures are
logged in each file.

**Re-run the discovery pass with search enabled before any of this informs an
investment decision.** The structural findings — the seam, the buffer gap, the
exclusivity model, the price floor — are well evidenced and unlikely to move.
The vendor census is not complete.
