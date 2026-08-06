# What to build, what to call it, and whether the name is available

**Question (owner, 2026-08-06):** *"What Exposition App should we build for the
EXPO market that will succeed, fill a deep need, be widely adopted and
profitable? What should we call it, and what URL is available?"*

This is the go-to-market answer that `spec/01` deliberately didn't give.
`spec/01` describes the *destination*. This describes the *wedge*.

---

> ## ✅ DECIDED — `marshal.show` registered by the owner, 2026-08-06
>
> The name is settled. Everything below is the reasoning that led there, kept
> for the record. **Marshal** is the product name; `marshal.show` is the domain.
>
> Still open and still available as of the check below: **`dock.show`** — the
> recommended Phase-1 product name (*Marshal Dock*).

## 1. The answer in one line

> **Build dock and marshalling-yard scheduling for exposition venues.
> Call it Marshal. `marshal.show` is available.**

Not the full services platform. Not show management. Not rental. One narrow,
physical, undeniable bottleneck — then expand along the data it generates.

---

## 2. Why this wedge and not the platform

`spec/01` specifies the right destination and the wrong v1. A full
exposition-services platform needs venues, exhibitors *and* contractors to adopt
together. That is three cold starts stacked, and the research found the category
has **no network effects to help you** (`competitors/08`).

The dock has eight properties nothing else in this market has at once.

**1 — It is a confirmed category-wide gap.** Across all six researched
categories, **loading-dock scheduling does not exist as a product**. The nearest
thing found anywhere was Skedda — a general-purpose room-booking tool — which is
the only vendor that even documents a named setup/teardown buffer mechanic
(`competitors/06`).

**2 — The category is proven, just not here.** Dock scheduling is a real, funded,
consolidating software category in warehousing and distribution: Opendock, C3
Solutions, Transporeon. Buyers there already pay for it. **It has simply never
been built for exhibition halls.** That is the arbitrage — a validated category
absent from an adjacent vertical.

**3 — The adjacent incumbents structurally cannot cross over.** Warehouse dock
scheduling assumes steady state: repeat carriers, standing appointments, a
predictable daily rhythm. Exposition move-in is the opposite — a 36–72 hour
surge, mostly one-time carriers, hard precedence constraints, and spatial
exclusion (`spec/03` §3.2). Pointing Opendock at a convention centre produces
plans that are arithmetically valid and physically impossible. **They would have
to rebuild the solver, and their existing customers would not pay for it.**

**4 — One buyer, with budget, whose P&L actually moves.** The venue. Dark time
between shows is revenue that never comes back, and turnaround density is the
metric their GM is measured on. `competitors/08` already established the venue as
the only party whose economics improve from better scheduling.

**5 — No cold start.** A single venue can deploy it alone and get value in its
first show. It does not need exhibitors, contractors, or other venues to
participate. Every other idea in this study needs at least two sides.

**6 — It is neutral territory. This is the decisive go-to-market unlock.**

Service exclusivity is **venue-granted, per service** — electrical to one firm,
rigging to another, one contractor exclusive across 50+ venues
(`competitors/04`). Those exclusives are exactly what kill new entrants: sell
exhibitor electrical ordering and you are in a fight with an incumbent holding a
signed contract.

**But dock and yard access is always the venue's own.** It is the one piece of
the floor no service contractor holds exclusivity over, because it is the
building itself. **Marshal can be sold into a venue without touching a single
exclusive contract, and without asking GES or Freeman for anything.**

That single fact is why this wedge is enterable and the obvious ones are not.

**7 — It manufactures the data everything else needs.** Actual truck arrival
times, dock dwell, crew durations and variance reasons are precisely the
calibration inputs `spec/03` requires for predictive scheduling — and the gap
data `spec/02` needs for the Show Board. **Phase 1 is also the instrumentation
for Phases 3–5.**

**8 — ROI is provable in one show cycle.** Marshalling-yard wait time, dock
idle, and overtime are all measurable within 72 hours of go-live. That is what
converts a pilot into a renewal, and it is the difference between *widely
adopted* and *widely admired*.

---

## 3. What we are explicitly not building first

| Option | Why not now |
|---|---|
| Full exposition-services platform | Right destination, three simultaneous cold starts. This is Phase 3+ |
| Show-management platform | Momentus already rolled the category up (`competitors/06`) — fighting a roll-up |
| Party/event rental software | $29/mo price floor, Odoo ships Rental free. No business (`competitors/01`, `03`) |
| Exhibitor service ordering | This *is* the proven seam (`competitors/05`) — but it collides head-on with GES Expresso and needs exclusivity navigation. Enter it from inside the venue, not from outside |

---

## 4. The expansion path — each phase paid for by the last

| Phase | Product | Buyer | Unlocked by |
|---|---|---|---|
| **1** | Dock + marshalling-yard scheduling | Venue ops | — |
| **2** | Full move-in/move-out plan: crews, equipment, spatial sequencing | Venue (expansion) | Phase-1 actuals |
| **3** | Exhibitor order page | Venue sells it in | **We now hold the truth about when freight lands — the seam closes as a side effect** |
| **4** | Contractor early-warning feed on scope change | **Service contractor** | Phases 1–3 data |
| **5** | Show Board capacity network (`spec/02`) | Show managers + venues | Gap data accrued as byproduct |

Phase 4 is the research's most counter-intuitive finding and worth restating:
**the contractor is the best customer for change notice**, because late notice is
already a quantified cost on their books (`spec/02` §6). They are allies here,
not competitors — consistent with routing around their moat rather than at it.

---

## 5. Why it is profitable

- **Venue subscription** priced by hall and dock count — a mid-size convention
  centre is a four-to-low-five-figure monthly line, and it replaces a
  spreadsheet plus a person on a radio, not a competing product
- **Expansion is structural**, not upsell pressure: Phase 2 sells itself once
  Phase-1 actuals show where the plan broke
- **Contractor feed is a second revenue line against a different budget** with
  quantifiable cost avoided
- **Low delivery cost** — we already own the scheduling engine, the capability
  abstraction, the agent runtime and the portal patterns
  (`internal/01`, `internal/02`)

---

## 6. Canada first is a moat, not a compromise

Bill 96's French-availability deadline has passed, and Law 25 requires a privacy
impact assessment before personal data leaves Quebec (`competitors/07`).
**Canadian hosting plus genuine bilingual UI is a structural barrier to US
entrants** who treat Canada as an afterthought — and we are already built to
satisfy it. The fragmentation the research found (Ottawa splitting two
contractors across two venues) is *helpful* for a venue-side product: no single
incumbent to dislodge.

---

## 7. The name

**Marshal.**

- **It is the exact industry term.** A *marshalling yard* is where trucks stage
  before they are called to a dock. Every ops person in this market uses the
  word daily — the product is named after the job it does
- **The verb is the product.** To marshal is to bring into order. That holds as
  the product grows from trucks to crews to freight to whole shows — where
  "Dock" or "Bay" would box it in at Phase 1
- **It sounds like an authority, not a SaaS tool.** It carries the register of
  the floor, which matters to the buyer

**Collision check:** Marshall Amplification (double-l, musical instruments) and
the law-enforcement sense. Neither competes for attention in a convention-centre
ops context, and the single-l spelling separates from the amp brand. Acceptable.

### The domain — verified 2026-08-06 via RDAP

| Domain | Status |
|---|---|
| **`marshal.show`** | 🟢 **REGISTERED 2026-08-06 — this is the name** |
| `dock.show` | ✅ AVAILABLE — a genuinely premium single-word domain |
| `movein.show` | ✅ AVAILABLE — the literal industry term |
| `marshall.show` | ✅ AVAILABLE (double-l defensive) |
| `marshaldock.com` / `marshalfloor.com` | ✅ AVAILABLE (.com fallbacks) |
| `marshal.com`, `marshal.ca`, `yardline.com`, `apron.com`, `dockline.com`, `loadin.com`, `trymarshal.com`, `usemarshal.com`, `marshalyard.com` | ❌ taken |

**`marshal.show` reads as "marshal the show."** The TLD is doing semantic work
rather than apologising for a missing `.com` — in this one industry, `.show` is
more credible than `.com`, not less.

**Registration status:**
1. ~~`marshal.show` — the brand~~ ✅ **DONE 2026-08-06**
2. `dock.show` — the Phase-1 product name (*Marshal Dock*) and a strong redirect;
   **still open, too good to leave for someone else**
3. `marshall.show` + `marshaldock.com` — cheap defensive holds, optional

*Method: RDAP (`rdap.org`), where 404 = unregistered. Controls confirmed —
`google.com` and `floorplan.show` both returned registered. Note that macOS
`whois` cannot resolve `.show` (it falls back to IANA and reports the TLD
record), so any whois-based check of these names is unreliable. **Availability
moves; re-verify at the registrar before committing to the brand.***

---

## 8. Verdict

**Marshal — dock and marshalling-yard scheduling for exposition venues, Canada
first, at `marshal.show`.**

It wins because it is the only entry point in this market that is simultaneously
a real unmet need, a proven software category, physically impossible for the
adjacent incumbents to serve, sellable to one buyer with a moving P&L, free of
the exclusivity contracts that block every other door, and — the part that
compounds — the instrument that generates the data for everything else in this
study.

**Immediate next step, and it is cheap:** phone one Canadian venue ops director
and one service contractor. Ask the venue what an hour of dock idle costs during
move-in, and ask the contractor what late scope-change notice costs them. Both
answers are already on someone's books. Neither requires a line of code.
