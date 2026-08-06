# Odoo 16 CE — what we actually have

**Verified 2026-08-06** against the live install at
`weld@192.168.68.87:/Users/weld/odoo-dev/v16/odoo/addons` — **not** from
documentation or recollection. This is the real constraint surface for every
design decision from D-010 onward.

## Available in CE

| Module | Marshal use |
|---|---|
| **`resource`** | `resource.calendar` / `resource.resource` — **the capacity primitive.** Working hours, leaves, intervals. What the OdooIQ solver already builds on |
| **`hr`** | Employees, jobs, departments — the roster |
| **`hr_contract`** | Contract terms, working schedule per employee |
| **`hr_attendance`** | Check in/out — actual worked time |
| **`maintenance`** | `maintenance.equipment`, `maintenance.request` — **equipment register, service history, preventive schedules.** Confirms D-008 |
| **`fleet`** | Vehicles, **fuel logs**, odometer, assignment, cost. Confirms D-008 |
| **`project`** | Tasks, stages — a fallback orchestration primitive |
| **`mrp`** | Work orders, workcenters, routings — where `frepple` plugs in |

## ❌ NOT available — Enterprise only

| Module | Consequence |
|---|---|
| **`planning`** | **There is no shift-planning app.** Employee rostering (D-013 candidates) must be built on `hr` + `resource.calendar`. This is the single biggest constraint on the employee-scheduling workstream |
| **`quality`** | **No quality-control app.** This is *why* `quality_control_oca` (AGPL-3) matters — it isn't a convenience, it's the only route to the checkpoint engine (D-008). The edata+ find is load-bearing |
| `sign` | No e-signature. Custody handover signatures (R06) need another mechanism |
| `appraisal`, `helpdesk`, `field_service` | Not available |

## What this settles

1. **Employee scheduling is a build, not a config.** No `planning` module. The
   primitives are there (`resource.calendar` for availability, `hr_contract` for
   working schedule, `hr_attendance` for actuals) but the rostering layer on top
   is ours to write. **Budget for it properly.**
2. **`quality_control_oca` is on the critical path**, not a nice-to-have. Without
   it there is no checkpoint engine, and checkpoints are how humans re-anchor the
   model (D-008).
3. **Equipment condition and fuel are genuinely near-free** — `maintenance` and
   `fleet` are both present and are the right models. D-008's claim holds up.
4. **`resource.calendar` is the shared primitive** across equipment availability,
   operator shifts and elevator blackout windows. One concept, three uses — worth
   designing around deliberately rather than discovering later.

## Method note

This took one SSH command. **Do this before asserting any Odoo capability** —
the CE/Enterprise split is the most common source of confidently wrong
architecture in this stack, and it is trivially checkable against a real install.
