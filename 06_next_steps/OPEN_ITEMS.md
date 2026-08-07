# Marshal — open items

Ordered by what unblocks the most. Nothing here needs code.

---

## 1. Two phone calls — the cheapest test in the whole project

**This resolves Q-1, the biggest open question: who do we sell to first.**

**Call a Canadian venue ops director.** Ask: *what does an hour of dock idle cost
you during move-in, and how do you schedule the yard today?* Expect the answer to
be a spreadsheet, a radio, and a person. The cost is already on their books.
**Added 2026-08-07: if it's Toronto, Vancouver, or Calgary, ask specifically
whether they already use Voyage Control (`voyagecontrol.com`) — confirmed live at
MTCC, Vancouver Convention Centre, and BMO Centre Calgary — and if so, what it's
failing to do for them.** See `02_market_research/07_canadian_market.md` §0. Don't
assume greenfield at any of those three venues.

**Call a service contractor.** Ask: *what does it cost you when a show's scope
changes late — and when do you typically find out?* The research's most
counter-intuitive finding is that **the contractor may be the best customer**,
because late notice is a quantified cost they already carry.

Whichever number is bigger and better documented decides whether Phase 1 (venue
dock scheduling) or Phase 4 (contractor early-warning feed) is the first sale.

---

## 2. Register `dock.show`

Verified still available 2026-08-06. Recommended Phase-1 product name
(*Marshal Dock*). A few dollars against a decision you can still walk away from,
and the only asset in this project someone else can take.

---

## 3. ~~Re-run the vendor census with web search enabled~~ DONE 2026-08-07 (Canadian pass)

Re-ran with real WebSearch, scoped to the Canadian market file (`07_canadian_market.md`).
Closed: the 3 venue fetch-failures, market sizing, the national association identity
(it's **CAEM**, not "CEMA"). Found the single most important competitive fact in the
project so far: **Voyage Control already runs dock scheduling at MTCC, Vancouver
Convention Centre, and BMO Centre Calgary** — see §0 of that file and the phone-call
note in item 1 above. Also surfaced two vendors the original pass missed entirely
(Global Convention Services, Encore Canada's cross-provincial AV consolidation).

**Still not re-run**: the other 6 category files (`01`–`06` under `02_market_research/`)
were compiled the same search-unavailable way and carry the same "strong starting
list, not a census" caveat. Re-run those too before any figure reaches an investor
deck. See `04_research_archive/research_method_and_limits.md`.

---

## 4. Get an antitrust opinion before designing the Show Board

Competing venues seeing each other's availability is **information exchange** —
legally sensitive in both Canada and the US regardless of intent.

Likely-necessary constraints, which must be reviewed by counsel rather than
designed by us: availability only with no pricing, no aggregate utilisation
visibility between venues, no historical calendar, anonymised listings until an
enquiry qualifies.

**This shapes the data model**, so the opinion is cheaper now than a redesign
later. Not urgent — the Show Board is Phase 5.

---

## 5. Read `qnap/porterly-future-reference` before designing the agent/core split

Dependency-free Python, **74 invariant tests** — the only tested artifact in the
Porterly family. Event-sourced idempotent ledger, guarded FSM, and an
agents-propose/core-decides split where **core re-derives identity from ground
truth rather than trusting agent claims**.

It is a worked answer to *"how do we let an LLM propose actions without letting
it forge state"* — the exact trust boundary an agentic scheduler needs. The same
insight as Southbrook's `PLM_LIFECYCLE` sentinel, reached independently in a
different codebase.

Details: `03_internal_assets/02_recovered_asset_findings.md` §1.

---

# ⚠ Unrelated to Marshal, but genuinely urgent

Found during this work. **Not Marshal tasks** — recorded here so they aren't lost.

## Two bodies of load-bearing work exist only on this Mac

**`~/Downloads/AEMI/aemi_platform`** — eight uncommitted paths, including
`addons/aemi_ai_platform/` which is entirely **untracked**: 34 passing tests,
`aemi.service.request`, never committed, never pushed, never deployed.

**`~/hermes-console`** — **3 commits ahead of `forgejo/main`** plus 3 dirty
files, carrying Fabio's entire tool-calling path (`api/hermes_agent.py`,
`/api/hermes/ask`). The `github` remote has never been fetched.

Backups exist under `~/Downloads/_backups/`, but a backup is not a remote.

## Live security findings in Porterly

- **CSRF-via-GET**: `event_extend/controller/main.py:682-702` — `/enable/portal`
  and `/disable/portal` perform privileged `sudo()` state changes on bare GET
  routes, sidestepping CSRF regardless of the flag
- **Zero `domain_force`/ir.rule across all 289 modules** — access control is
  100% controller discipline with no ORM backstop
- **`~/porterly_dev` tracks the stale `aug2026/porterly` mirror**, missing the
  Q5/Q7 fixes. Authoritative repo is **`john/porterly_erp`**
