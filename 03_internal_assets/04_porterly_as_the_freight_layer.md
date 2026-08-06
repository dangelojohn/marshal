# Porterly Inbound/Outbound as Marshal's freight and billing layer

**Question (owner, 2026-08-06):** *"What is your recommendation if we use the
newest version of Porterly Inbound and Outbound to track packages and have the
payment? Was that your consideration?"*

**Honest answer: no, it was not — and it should have been.**

The asset inventory (`03_internal_assets/01`) classified the Porterly PWAs as
*"GENERALISE — richest working reference for public→validated-record intake"*
and `courier_tracking` as *"LIFT portal patterns."* **I read them as pattern
sources and missed that the billing spine is real and in production.**

---

## What's actually there — verified by direct read of `john/porterly_erp` HEAD

**Not the stale mirror.** `~/porterly_dev` tracks `aug2026/porterly`, which is
missing the Q5/Q7 security fixes. **Everything below is the authoritative repo.**

### The invoicing pipeline is real

`courier_tracking/models/model.py`:

| Evidence | Line |
|---|---|
| `action_create_invoice()` | :509 |
| `invoice_id = fields.Many2one('account.move')` | :385 |
| `account.move.line` creation | :114, :129 |
| `sale_order._create_invoices()` | :595 |
| `charge_type` Selection — `post_to_master` / `internal` / `credit` | :390 |

`depends`: `sale_management, stock, mail, product, event, account, delivery,
queue_job, sale, l10n_ca, calendar, dms, bi_signature_by_so, contacts`

**`l10n_ca` is already a dependency.** Canadian tax localisation, in production,
on a Canada-first product (D-001). That is not nothing.

### The intake is dock-hardened

`porterly_inbound_pwa` is **literally a mobile dock-capture app**, and
`porterly_outbound_pwa` is public→validated-record intake with **honeypot,
rate-limiting, and idempotency-by-uuid** — the comment at
`outbound/controllers/main.py:67` reads *"a double-tap submit returns the SAME
parcel (no duplicate/charge/email)."*

**Double-tap on a mobile device in a loud, gloved, high-pressure environment is
exactly Marshal's problem**, and it's already solved here in production rather
than in theory.

### Consent-gated charging

The outbound flow tells the customer *"Porterly will confirm the details and any
charges before your packages go out"* (:304). **Charges are classified
automatically and confirmed by a human before they bind.** That is precisely the
posture Marshal needs for metered handling — automatic measurement, human
confirmation, then billing.

---

## The framing that makes this compose

> **Porterly is the noun. Marshal is the verb.**

| | Porterly | Marshal |
|---|---|---|
| Owns | **What the thing is** — identity, ownership, custody state, charge class, invoice | **How it moves** — dock, equipment, operator, elevator, route, timing, safety |
| Answers | *Whose crate is this, where is it, what does it cost, has it been billed* | *How does it get to booth 412, with what, when, safely, verified by whom* |
| Proven | In production | Doesn't exist yet |

They are **not competing models — they're two halves of one system.** A Marshal
`movement` references a tracked thing; Marshal's actuals become billable
consumption feeding the invoice path Porterly already runs.

`event_extend` adds a third piece: booth/exhibitor structures on `event.event`,
which is a starting point for the show model.

**This materially changes the plan.** `PROJECT_PLAN.md` Phase 3 (Metering and
billing) was scoped as new work. **Much of it exists** — including the part
nobody enjoys building, Canadian tax on a real invoice.

---

## ⚠ What comes with it — the debt is real

| Issue | Severity | Detail |
|---|---|---|
| **Odoo 16 → 19 port** | High | Known v19 breakage: `_sql_constraints` gone, `group_ids` rename, `ir.cron` schema, scoped attribute rules. `bi_signature_by_so` (BrowseInfo, purchased) and `dms` need v19 equivalents or removal |
| **Zero `ir.rule` across all 289 modules** | **High** | Access control is **100% controller discipline, no ORM backstop.** Marshal has venue, show manager, exhibitor and carrier each seeing different slices — **one mis-coded domain is a full leak.** Marshal must declare record rules from module one |
| **No tests anywhere** | **High** | 12 modules checked, none. **For infrastructure that emits billing records, that's disqualifying as-is** — anything lifted needs tests written around it |
| **14 dependencies** on `courier_tracking` | Medium | `stock`, `delivery`, `dms`, `bi_signature_by_so`, `event`… taking the module means taking the tail |
| **A parcel is not a crate** | Medium | Porterly models packages a person carries. A 2000lb crate needing a forklift, a route and an elevator is a different physical object. **Identity/custody/billing transfers; handling does not** |
| Licence | Low | METISA/OPL-1 — John owns METISA. `bi_signature_by_so` is purchased third-party |

---

> ## 🔄 REVISED 2026-08-06 — v16 target, QuickBooks for accounting
>
> **Owner decision:** *"Let's not get too involved with tax as we will be using
> Odoo v16 for this development and leverage the QuickBooks application we
> already own."*
>
> **Both halves of my recommendation below were premised on facts that no longer
> hold.** The revision is at the end of this file (§ *Revised recommendation*);
> the original reasoning is kept for the record.
>
> - **v16, not v19 → the port cost disappears.** Porterly *is* v16. The single
>   largest argument for Option B is gone
> - **QuickBooks is the book of record → the tax argument is moot.** `l10n_ca`
>   stops being an asset, and Odoo accounting stops being a destination

## Three options

### A · Run Porterly modules inside Marshal's Odoo

Marshal is single-tenant Odoo per facility (D-008), so this isn't integrating two
systems — it's one install with both module sets.

✅ No integration layer. Invoicing works day one.
❌ Inherits all 14 dependencies, the missing `ir.rule` layer, zero tests, and
parcel semantics — into infrastructure that must be defensible.

### B · Port the spine, rewrite the invoice path natively ⭐ **recommended**

Take the **tracked-thing model, the hardened intake, and the `charge_type`
design**. Let Marshal's metering produce consumption records that feed **Odoo's
native sale→invoice path** — which is what `courier_tracking:595` ultimately does
anyway via `sale_order._create_invoices()`.

✅ Keeps the proven design and the dock-hardened idempotency
✅ **Drops the 14-dependency tail** and the parcel-specific semantics
✅ **Lets us add `ir.rule` and tests from module one** — fixing both structural
weaknesses rather than porting them
✅ Same commercial outcome; `l10n_ca` is core Odoo, not Porterly's

❌ More work than A. **Worth it** — Marshal's entire case is that its records are
defensible, and inheriting a no-tests, no-record-rules billing path contradicts
that on day one.

### C · Treat Porterly as separate and integrate by API

❌ Two systems, two databases, an integration to maintain, and it fights D-008's
single-tenant simplicity. **Only if Porterly stays a live product on v16
independently** — worth asking, but not the default.

---

## Recommendation

**Option B.** Concretely:

1. **Read `courier_tracking:509-624` before designing Marshal's billing.** It is a
   working, Canadian-taxed parcel→invoice path — the design is proven even where
   the code isn't reusable
2. **Lift the idempotency-by-uuid intake pattern verbatim.** Hardened at a real
   dock; don't re-derive it
3. **Lift `charge_type`'s shape** — automatic classification, human confirmation
   before binding. That is exactly right for metered handling (D-005 §2)
4. **Implement invoicing on core Odoo `sale`/`account` + `l10n_ca`**, not by
   porting `courier_tracking`
5. **Declare `ir.rule` record rules from module one.** The single most important
   thing to *not* inherit
6. **Write tests around anything lifted.** Non-negotiable for billing records
7. Use `event_extend` as the reference for booth/exhibitor structures

**Revised plan impact:** Phase 3 gets substantially cheaper and lower-risk,
because the hard commercial questions — what a charge type is, how it reaches an
invoice, how Canadian tax applies — are answered by working code rather than
guessed. **Q-8 (what unit is billed) is still the blocker**, and no amount of
existing code answers it. That remains a phone call.

---

# Revised recommendation — v16 target, billing deferred

**Owner decisions, 2026-08-06:**
> *"We will be using Odoo v16 for this development and leverage the QuickBooks
> application we already own."*
> *"Let Quickbooks and Stripe and the invoice module handle tax later."*

## What this changes

**→ Option A is now the recommendation, not Option B.**

| Was | Now |
|---|---|
| v16→v19 port was the main cost | **No port. Porterly is already v16 — the modules drop straight in** |
| The 14-dependency tail was a risk | Much less so — **those dependencies already work together in production on v16** |
| `l10n_ca` was an asset | **Irrelevant.** Tax isn't Odoo's job |
| `courier_tracking`'s `account.move` path was the prize | **Not the destination.** Billing leaves Odoo |

## The billing boundary — now clean and explicit

> **Marshal produces a defensible, priced consumption record. It does not
> invoice, does not compute tax, and does not take payment.**

```
   Marshal  ──▶  priced consumption records  ──▶  QuickBooks · Stripe · invoice module
   (meter)        what was consumed, by whom,        (tax, invoice, collection)
                  when, evidenced                              [LATER]
```

This is a **better** boundary than the original plan, for three reasons:

1. **It's the honest scope.** Marshal's claim (D-005 §2) was always *"you billed
   40 hours, the floor consumed 62 — here's the record."* That is a **metering**
   claim. Turning it into an invoice was scope we assumed, not scope anyone asked
   for
2. **Tax is genuinely hard and genuinely solved elsewhere.** Deferring it to
   tools already owned removes an entire category of work and risk
3. **It keeps the defensible thing defensible.** The consumption record must be
   exact, evidenced and auditable. An invoice is a downstream artifact — and
   keeping it downstream means a billing dispute is settled by Marshal's evidence
   rather than argued inside Marshal's code

**Architecturally this is a bridge**, and we already own the pattern:
hermes-console's `tenant_bridges/` — one small adapter class per target system.
**QuickBooks becomes a bridge. Stripe becomes a bridge.** Neither is in Phase 1.

## What still stands, unchanged by any of this

The port was never the whole argument. Two items were about **debt, not version**,
and they still apply to anything lifted:

1. **Declare `ir.rule` record rules from module one.** Porterly has **zero
   `domain_force` across all 289 modules** — access control is 100% controller
   discipline with no ORM backstop. Marshal has venue, show manager, exhibitor
   and carrier each seeing different slices. **One mis-coded domain is a full
   leak.** This is the single most important thing not to inherit
2. **Write tests around anything lifted.** No tests exist anywhere in Porterly
   (12 modules checked). For infrastructure emitting consumption records that
   settle money disputes, that is disqualifying as-is

And: **build from `john/porterly_erp`, never from `~/porterly_dev`** — the local
checkout tracks the stale `aug2026/porterly` mirror, which is missing the Q5/Q7
security fixes and still contains the retired public POST hole.

## The v16 trade — stated once, not argued

v16 is outside Odoo's current support window. For **installed per-facility
infrastructure** (D-008) rather than a hosted SaaS, that is a defensible trade,
and it buys alignment with every asset we own — Porterly v16, edata+ v15,
`quality_control_oca` and `base_rest` both having v16 branches.

Worth knowing rather than worth reopening: security patches become our
responsibility, and a v19 move later is a project rather than an upgrade.

## Revised recommendation

1. **Odoo 16, single-tenant per facility.** Porterly module set installed
   alongside Marshal's own modules — one install, no integration layer
2. **Take `courier_tracking` + both PWAs + `event_extend`** for identity, custody,
   dock capture and booth/exhibitor structure
3. **Do not use the `account.move` invoice path.** Marshal writes **consumption
   records**; billing is a later bridge to QuickBooks/Stripe
4. **`charge_type`'s shape still transfers** — automatic classification, human
   confirmation before it binds. That's the right posture for metered handling
5. **`ir.rule` from module one. Tests around everything lifted.** Non-negotiable
6. **Adopt the PWA design language** (see `01_product/12`)

**Plan impact:** Phase 3 shrinks from *"build billing"* to *"produce priced
consumption records"*, with the bridge deferred. Phase 1 becomes substantially
assembly. **Q-8 (what unit is billed) matters more than ever** — it defines the
consumption record's shape, and no existing code answers it. Still a phone call.

## New open questions

| # | Question | Why |
|---|---|---|
| **Q-28** | Does Porterly remain a live product on v16 independently? | If it keeps evolving separately, decide now whether Marshal forks or tracks it |
| **Q-29** | Does `charge_type` map onto handling units (Q-8)? | If handling bills by crate or CWT, it may transfer almost directly |
| **Q-33** | QuickBooks Online or Desktop? | Online has a proper REST API; Desktop needs a connector and changes the bridge entirely |
| Q-34 | Does Stripe collect from exhibitors directly, or is it invoice-follow-up? | Decides whether a payment surface is ever needed in Marshal |
