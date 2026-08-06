# Marshal — open items

Ordered by what unblocks the most. Nothing here needs code.

---

## 1. Two phone calls — the cheapest test in the whole project

**This resolves Q-1, the biggest open question: who do we sell to first.**

**Call a Canadian venue ops director.** Ask: *what does an hour of dock idle cost
you during move-in, and how do you schedule the yard today?* Expect the answer to
be a spreadsheet, a radio, and a person. The cost is already on their books.

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

## 3. Re-run the vendor census with web search enabled

The market research was compiled **without web search** — agents could fetch
known URLs but could not *discover* vendors. Consequences:

- Good coverage of vendors we could name in advance
- **Weak on regional Canadian players and recent entrants** — precisely where a
  competitive study most needs discovery

The structural findings (the seam, the buffer gap, exclusivity, the price floor)
are well evidenced and unlikely to move. **The vendor roster is a strong starting
list, not a census.** Re-run it before any figure reaches an investor deck.

See `04_research_archive/research_method_and_limits.md`.

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
