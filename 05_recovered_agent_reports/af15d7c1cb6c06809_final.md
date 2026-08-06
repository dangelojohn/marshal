Report written to `/Users/naadmin/Downloads/Event Renal/internal/01_forgejo_asset_inventory.md`. Summary:

**Asset list with verdicts:**
- **aemi-platform** (Odoo 16, LGPL-3, 36 modules, deployed): `avn.capability` venue-connector abstraction (API-optional: mcp→api→portal→web_form→email→human_workflow, same contract) — **LIFT**. Digital twin, attention engine, KG — **GENERALISE**. Claim/heartbeat/complete agent-runtime API and multi-provider LLM client — **LIFT**. Multi-tenant scoping mixin — **LIFT**.
- **Porterly** (METISA-owned, full rights): `courier_tracking`/`in_shipment`/`shipment_request`/`porterly_inbound_pwa` are real production booth-freight/parcel logistics — **LIFT domain, GENERALISE code**. `event_booth_config` — **GENERALISE**.
- **odooiq-factory-intelligence** (Odoo 19, LGPL-3): **LIFT the architecture** — verified read-only against `mrp.*` (single guarded touchpoint), EDD-greedy solver with pure-Python ERP-portable dataclasses, median/MAD calibration with small-N shrinkage, delivery estimates as honest p10/p50/p90 ranges that widen when data is thin.
- **hermes-console**: standalone FastAPI agent control plane (recommend→human-approve→tenant-push, MCP tool server) — **LIFT architecture**.
- **southbrook-v19cr**: ECO four-eyes self-review gate + row-locked race guard — **near-LIFT**; as-sold snapshot-at-confirm pattern — **GENERALISE**.

**Scheduler architecture (odooiq-factory-intelligence):** capacity modeled as free time-intervals per (workcenter, day) from `resource.calendar`; calibration is a per-scope median/MAD correction multiplier with sample-size-gated trust blending; delivery estimates are always ranges (p10/p50/p90 of historical ratio, shrinking with N, never a point); confirmed read-only — the only `mrp.*` write anywhere in the codebase is a single savepoint-guarded observation-capture hook on `button_finish`.

**Traps:** a real production IDOR in a third-party Porterly module (now patched — read the fix, not the original); hermes-console's `auth.py` is a no-op that relies entirely on Cloudflare Access network topology; AEMI's AI layer was previously found dead in prod (no Anthropic key) — verify before trusting "deployed."

**Estimate: ~35–40%** of the target platform already exists in reusable form — the hard, differentiating pieces (scheduler, capability abstraction, agent runtime contract, orchestration loop) are built; what's missing is domain extraction and integration across four currently-separate repos.