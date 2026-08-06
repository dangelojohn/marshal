# edata+ — what's actually on the iMac volume

**Reached 2026-08-06** over SSH to the Porterly iMac (`weld@192.168.68.87`, key
auth — the password wasn't needed and isn't recorded here). Volume mounted at
`/Volumes/iMac`, 572 top-level entries.

**Owner's note:** *"a project called edata+ that I fully own and produced… we
have resources for these types of support for equipment."* `[PRIMARY]`

---

## Where it is

| Path | Size | What |
|---|---|---|
| `/Volumes/iMac/edata-internal-master.zip` | **179 MB** | **The codebase — 52 Odoo 15 modules** |
| `/Volumes/iMac/edata-testing-dev_2023-05-23_15-14-23.zip` | 45 MB | Dev snapshot, May 2023 |
| `/Volumes/iMac/EData+/` | 29 MB | Docs, NDAs, planning material |
| `/Volumes/iMac/edata+ website.zip` | — | Website build |
| `EDATA Needs.pptx`, `EData Nomenclature Cheat Sheet.pdf` | — | Requirements and vocabulary |
| `OneDrive - Essex Weld Solutions/Recordings/` | — | 6+ design-review recordings, 2022–23, incl. *"Edata+ routing through Odoo15"* |

---

## ⚠ Correction: the equipment support isn't the equipment support we need

The recollection is **half right**, and the half that's wrong matters.

**There is no physical-equipment maintenance, condition, or fuel tracking in
edata+.** Searched the whole archive:

- `itm/models/equipment*.py` — **this is IT asset management.** CPU, RAM,
  storage, network, DB engine, IP reservation. Nothing to do with forklifts
- **Odoo's native `maintenance` module is not used anywhere.** The only hit
  across 179 MB is `code_backend_theme/static/src/img/icons/Maintenance.png` —
  an icon
- No fleet, no fuel log, no odometer, no inspection-of-plant records

**But the checkpoint machinery is there, and that's the harder half** — see
`quality_control_oca` below.

**The gap is cheaply filled from core Odoo, not custom work:**

| Need | Native Odoo |
|---|---|
| Equipment register, service history, preventive schedules | **`maintenance`** — `maintenance.equipment`, `maintenance.request` |
| **Fuel logs**, odometer, assignment, cost per unit | **`fleet`** — built for exactly this |
| Condition / return-position checkpoints | **`quality_control_oca`** (below) |

So the answer on equipment support is: **edata+ doesn't have it, and we don't
need it to** — Odoo ships it.

---

## What edata+ genuinely contributes

### ⭐ `quality_control_oca` — AGPL-3, OCA — **the direct hit**

> *"checks and balances… such as the condition of equipment and fuel and if the
> equipment was returned to the right position."* `[PRIMARY]`

That is a **quality-control inspection point**, exactly: a defined test, applied
at a defined trigger, with pass/fail criteria and a recorded result and
inspector. This module is the generic engine for that pattern, **AGPL-3 and
freely reusable**.

This is the single most directly applicable thing in the archive. It is the
mechanism for the human-in-the-loop checkpoints in D-008.

### ⭐ `frepple` — AGPL-3, frePPLe, v15 — **worth evaluating against OdooIQ**

A working integration with **frePPLe**, a mature open-source finite-capacity
production planner. AGPL-3, so freely reusable.

**Do not assume it replaces the OdooIQ solver.** frePPLe models manufacturing —
work orders, routings, work-centre capacity. Marshal's problem is **mobile
resources with position and travel time, precedence within a movement, and
spatial exclusion** (`08` §5), none of which frePPLe models natively.

But it is a real, proven planning engine already wired to Odoo, and a serious
Phase-2 option. `[ASSUMPTION]` OdooIQ remains the better base because it's ours
and already calibrates from actuals — but this deserves a genuine comparison
before Phase 2, not a dismissal.

### ⭐ `base_rest` (LGPL-3, ACSONE/OCA) + `odoo_graphql` (LGPL-3)

**Directly serves the headless requirement (D-008).** `base_rest` is the standard
OCA framework for building REST APIs on Odoo, with the `component` module
alongside it. Both freely licensed. This is how Marshal exposes an API surface
without hand-rolling controllers.

### Useful, owned, but proprietary

| Module | Licence | Note |
|---|---|---|
| `metisa_container_management` | OPL-1, METISA | Container/crate tracking — **John owns METISA**, so a formality |
| `metisa_punch_clock` | OPL-1, METISA | Labour time capture → operator hours |
| `metisa_eng_screen`, `metisa_product_configurator` | OPL-1, METISA | Owned |
| `ews_bryntum_schedular`, `essex_gantt_view_*` | Metisa Solutions | Scheduling UI — **but see Bryntum below** |

### 🚫 Blocked by licence

| Module | Licence | Problem |
|---|---|---|
| **`bryntum_gantt`** | **Bryntum AB — commercial** | The Gantt library is **paid, per-developer**. The `essex_gantt_*` and `ews_bryntum_schedular` wrappers are ours; **the library underneath is not.** Do not build Marshal's UI on it without buying a licence |
| `pways_shift_schedule_management` | OPL-1, Preciseways | Third-party purchased. Shift rostering — useful shape, can't lift the code |
| `bi_all_in_one_project_management_system` | BrowseInfo | Third-party purchased |
| `om_*` (10 modules) | Odoo Mates | Third-party accounting set — irrelevant here anyway |

---

## Provenance flag — not a challenge, just a fact worth knowing

The archive contains **`Appendix A - NDA EData Plus.pdf`** (several copies, one
under `EData+/Essex Weld/`) and a set of `essex_weld_*` modules, and the
recordings live under `OneDrive - Essex Weld Solutions`.

Ownership of edata+ is the owner's to state and is taken as given. But the zip is
**a mixed tree** — owned METISA code, purchased third-party modules, OCA code,
and a commercial Gantt library, alongside material carrying an Essex Weld NDA.

**Practical consequence, same as the Porterly finding:** reuse is a
**per-module** decision, never a wholesale one. The three modules worth taking
(`quality_control_oca`, `frepple`, `base_rest`) are all AGPL-3/LGPL-3 and clean
regardless — which is a convenient outcome.

`[ASK]` Does the Essex Weld NDA constrain reuse of anything in this tree for a
different venture?

---

## Recommended next step

**Extract only the three clean modules** rather than the 179 MB archive:

```
quality_control_oca   AGPL-3   → the checkpoint engine (D-008)
base_rest + component LGPL-3   → the headless API surface
frepple               AGPL-3   → evaluate vs OdooIQ before Phase 2
```

All three are Odoo **15**; Marshal would target 19. `quality_control_oca` and
`base_rest` both have maintained upstream OCA branches — **take the current
upstream version, not the v15 copy in this zip.** The zip's value is telling us
which modules to go and get.
