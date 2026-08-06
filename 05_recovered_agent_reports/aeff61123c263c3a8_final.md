## Repo relationship (authoritative source identified)

| Repo | Commits | Latest | What it is |
|---|---|---|---|
| **john/porterly_erp** | 64 | 2026-07-25 00:00 | **AUTHORITATIVE.** Full Odoo 16 addons tree (289 modules under `Porterly_PRODUCTION-master/`), including an in-progress, explicitly-tagged security remediation campaign (commit messages `security(Q7)`, `review repairs (Q5)`, co-authored by Claude Opus 4.8). |
| aug2026/porterly | 3 | 2026-07-25 19:32 | **STALE mirror**, squashed from a 2026-07-12 snapshot. Its only later commit is a license-text swap, not a code sync — it lacks the `porterly_attachment_guard` module and the Q5/Q7 fixes that exist in `porterly_erp` (verified: `grep attachment_guard` → no hit; `in_shipment.py` content identical to the pre-fix state). |
| **/Users/naadmin/porterly_dev (local)** | — | tracks aug2026/porterly | `git remote -v` → `ssh://git@192.168.68.108:2223/Aug2026/porterly.git`, clean, up to date with that stale mirror. **The local checkout is behind the real security fixes** — do not treat it as current. |
| john/porterly_ops | 1 | 2026-07-11 | Ops/deploy scripts only (iMac box config), no addon code. |
| qnap/porterly-future-reference | 4 | 2026-07-23 | Not Odoo — a from-scratch conceptual prototype (`agents.py`, `fsm.py`, `ledger.py`, `policy.py`, `projections.py`, `validators.py`) exploring an "AI-native architecture." Idea fodder only. |
| qnap/porterly | 2 | 2026-05-26 | Decommissioned QNAP snapshot; `addons/` is literally empty (`.gitkeep`). Dead. |

**All analysis below is against `john/porterly_erp`, the current code.**

## Security claims — verified with current file:line evidence

**"sudo() on reads that should be user-scoped"** — CONFIRMED as a pervasive pattern, but with a real split: modules touched by the Jul 22-25 review now pair `.sudo()` with a hand-built ownership domain and carry audit comments; untouched modules don't.
- Fixed pattern: `courier_tracking/controller/main.py:74-84` — comment: *"previously counted ALL parcels globally, leaking total volume"*, now `domain = [('tracking_ref','!=',False),'|',('partner_id','child_of',[commercial.id]),('event_group_id','in',my_group_ids)]` before `.sudo().search_count()`.
- Best pattern in the codebase: `job_request_custom/controllers/main.py:394` — primary `/my/jobs` list uses plain `request.env["job.request"].search(domain,...)`, **no sudo()** on the query itself; `.sudo()` only applied at line 396 to the already-filtered recordset for template rendering.
- Untouched/still risky: `pways_adv_parcel_management/controllers/portal.py:13,23,36,52,68,91,100` — every read is `.sudo()` with domain built inline, **no `ir.rule domain_force` anywhere in the module** (only `ir.model.access.csv` + a groups XML) — zero ORM-level backstop if a domain is ever coded wrong.

**"empty search domains without ir.rule"** — REFUTED literally (domains are non-empty everywhere checked) but UPDATED: `grep -ln domain_force` across the whole 289-module tree returns zero hits for `courier_tracking`, `pways_adv_parcel_management`, `shipment_request`, `event_extend`, `event_booth_config`, `metisa_event_portal`, `metisa_parcel_search`, `porterly_inbound_pwa`, `porterly_outbound_pwa`, `in_shipment`. Access control is 100% controller-code discipline, not defense-in-depth via ir.rule.

**"csrf=False on routes that should be protected"** — CONFIRMED, current, with one instructive fixed case:
- Live and unreviewed: `pways_adv_parcel_management/controllers/portal.py:17,34,50,66,95` (5 routes, `auth="user"`) and `courier_tracking_website/controller/main.py:39,59`.
- Fixed-in-place: `shipment_request/controller/main.py:6-25` — docstring documents this exact route (`/ship_package_form/submit`) was *"unvalidated public POST (arbitrary FK/group injection, CSRF disabled)"*; now redirects to `/outbound`, creates nothing.
- Intentional/low-severity: `porterly_outbound_pwa/controllers/main.py:327,334` — anonymous, rate-limited (`_rate_ok`) public intake form; `type='json'` routes are CSRF-exempt by Odoo design.
- New residual risk found (not in old memory): `event_extend/controller/main.py:682-702` — `/enable/portal`, `/disable/portal` trigger privileged `.sudo()` state changes via bare **GET** routes, sidestepping CSRF entirely regardless of the flag — a CSRF-via-GET gap the review missed.

## Capability inventory (verdicts)

All modules: Odoo **16.x**, no `tests/` directory anywhere (checked 12 modules) — max maturity is "built + hardened," never "tested."

- **event_extend** (`event.booth`/`calendar.event` portal, "Other proprietary") — GENERALISE. Best exhibitor/meeting portal reference (`_prepare_groups_domain`, `_get_owned_event` IDOR guard).
- **event_booth_config** (booth fields, header `Copyright METISA SOLUTIONS`) — LIFT candidate; self-owned IP.
- **job_request_custom** (on-site jobs/tickets, OPL-1) — PATTERN; correct-access-control reference, don't copy verbatim (licensed).
- **porterly_outbound_pwa/inbound_pwa** (warehouse intake PWA, has `migrations/`) — GENERALISE; richest working reference for public→validated-record intake, verify ownership before lifting.
- **pways_adv_parcel_management** (AGPL-3, only freely-reusable license found) — GENERALISE data model, rewrite controllers (csrf, ir.rule).
- **courier_tracking(+website)**, **shipment_request**, **in_shipment**, **metisa_event_portal/parcel_search** — "Other proprietary"/OPL-1 — PATTERN ONLY, license blocks lifting code.
- **qnap/porterly-future-reference** — PATTERN ONLY, architecture ideas, not Odoo.