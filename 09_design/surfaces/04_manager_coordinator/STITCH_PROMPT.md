# Surface 4 — Manager Coordinator View

**Role:** Manager / dock coordinator, at a desk · **Job:** the queue, overrides, approvals (maker-checker), the day's review · **Status:** new, genuinely undesigned anywhere yet · **Device:** desktop web, mouse + keyboard

**Source docs:** `01_product/14_surface_map.md` §"Manager — web"

---

## Why this surface looks the way it does

The wall board (surface 3) answers *"is anything wrong right now?"* for someone standing 3 metres away who isn't touching anything. This is the other half of the same role: **someone sitting at a desk, with a mouse, who needs to act** — approve an exception, override an assignment, review how the day went. Where the wall board is glanceable and static, this is dense and interactive. Where the wall board never demands attention outside an exception, this is a working tool used continuously.

**Open question, not yet resolved (Q-43): is this the same responsive surface as the wall board, or a separate product?** The project's own docs flag this explicitly — "a coordinator standing at a wall board with a mouse is a different person from one sitting at a desk." This prompt treats it as a separate desktop application for now, sharing only the palette and status vocabulary with the wall board, not the layout. Revisit this once real coordinators have been watched using both.

The specific job list this surface has to serve, per the project's own operational model:
- **The queue** — movements waiting on a decision (a chokepoint conflict, an unassigned crate, a blocked runner)
- **Overrides** — manually reassigning a claim, releasing a stuck occupancy, forcing a priority change
- **Approvals (maker-checker, R07)** — a second person confirming a consequential change before it takes effect, not a rubber stamp
- **The day's review** — what happened, what got delayed and why, the dead-letter queue (DLQ) of refused/blocked movements with suggested actions

### Design brief

**Color** — same operational vocabulary as the wall board and watch (background `#0E1116`, panel `#161B22`, amber `#E0A458`, exception red-orange `#D7503A`, calm green `#5FB37E`), because this person moves between the wall board and this screen constantly and the status colors must mean the same thing in both places. **Difference from the wall board**: this surface can use a lighter neutral (`#8B94A3` grey-blue) for secondary/inactive UI chrome — buttons, table headers, filters — since it's an interactive tool, not a pure status display, and needs a wider tonal range to distinguish "data" from "controls."

**Type** — a working desktop-app face, not a distance-legible one: **IBM Plex Sans** or **Inter**, with a monospaced companion (**JetBrains Mono** or **IBM Plex Mono**) for IDs, timestamps, and tabular data — this is a tool for someone reading dense rows all day, tabular alignment matters more than headline drama here.

**Layout** — a three-pane working view, not a single ambient board:
```
┌───────────────────────────────────────────────────┐
│ MARSHAL — Coordinator          [today ▾] [DLQ: 2]  │
├──────────────┬──────────────────────┬──────────────┤
│ QUEUE         │ FLOOR (mini wallboard)│ DETAIL/ACTION │
│──────────────│                      │──────────────│
│ ▲ Dock 3      │  [6-8 small tiles,   │ Movement       │
│  buffer full  │   same status lang   │ PR-1041 → 412  │
│  needs decision│  as surface 3, but  │                │
│──────────────│   smaller/denser]    │ Requested by:  │
│ ● Dock 1      │                      │ runner watch    │
│  on schedule  │                      │                │
│──────────────│                      │ [Approve]      │
│ ● Dock 2      │                      │ [Override →]   │
│  on schedule  │                      │ [Reject]       │
├──────────────┴──────────────────────┴──────────────┤
│ DEAD-LETTER QUEUE — 2 entries, most recent first     │
│ 14:12  Dock 3  chokepoint_busy  "Hold at buffer..."   │
└───────────────────────────────────────────────────┘
```

**Signature element**: the **dead-letter queue rendered as a visible, permanent panel**, not a hidden log — per the project's own operating model, every refusal writes a coded entry with a suggested action, so a blockage is visible and actionable rather than discovered when a truck is already waiting. Most ops tools bury this in a "logs" tab; here it's docked at the bottom of the primary working view, always present.

---

## The Stitch prompt

```
Design a desktop web application for a dock/marshalling-yard coordinator at an
exposition venue — an operations tool used continuously at a desk with a mouse
and keyboard, not an ambient display. This is the "do something about it" tool
that pairs with a separate ambient wall board; treat this brief independently
and don't render camera feeds here (that belongs to the other surface).

DESIGN SYSTEM: near-black background #0E1116, panel surface #161B22, status
colors amber #E0A458 (waiting/in-progress), red-orange #D7503A (exception),
green #5FB37E (calm/normal) — used consistently for status only, never as
decorative color. Secondary neutral grey-blue #8B94A3 for UI chrome (buttons,
table headers, inactive filters, borders). Primary font: Inter or IBM Plex
Sans for labels and body text. Monospaced companion font (JetBrains Mono or
IBM Plex Mono) specifically for IDs, timestamps, and any tabular numeric data
— this distinction matters, don't use the same font for both. Flat fills, no
gradients, no glassmorphism, no rounded pill-shaped buttons — square/slightly
rounded rectangular controls (4-6px radius) that read as a serious operations
tool, not a consumer SaaS product.

DO NOT render: marketing dashboard clichés (donut charts, big vanity-metric
numbers with up/down arrows, gradient stat cards), emoji, illustrations of
people, or a light/white theme — this stays dark to match the coordinator's
other screen (a wall board) and because it's used in low-light dock
environments.

LAYOUT — a three-column desktop working view:

TOP BAR, full width: "MARSHAL — Coordinator" wordmark left, a date selector
and a small red badge reading "DLQ: 2" (dead-letter queue count) on the right
— this badge should look like a real notification count, not decorative.

LEFT COLUMN — "Queue": a vertical list of movements/items needing a decision,
each row showing a status icon (triangle=exception in red-orange, circle=
normal in green — same shape+color language as a companion wall-board
surface), a short location label ("Dock 3"), and a one-line reason
("buffer full — needs decision" for the exception row, "on schedule" for
normal rows). The exception row should be visually first/pinned to the top
regardless of any other sort order, and should be clearly the thing your eye
goes to first.

MIDDLE COLUMN — "Floor": a smaller, denser version of an ambient status-tile
grid (think a compact 6-8 tile mini-map, no camera thumbnails here, just
status icon + dock label + one line of state per tile) — this is a live
overview a coordinator glances at while working the queue, not the primary
focus of this screen.

RIGHT COLUMN — "Detail / Action": shows the currently-selected queue item in
full — a movement reference ("PR-1041 → Booth 412"), who/what requested the
current state ("Requested by: runner watch"), and three clearly distinct
action buttons stacked: "Approve" (filled green), "Override →" (outlined
amber, implying it opens a further choice), "Reject" (outlined red-orange).
These three buttons must look meaningfully different in weight/prominence from
each other — Approve is the common case and should look like the default safe
action; Override is a deliberate escalation; Reject is rare and should require
visible intent, not be a casual click target.

BOTTOM PANEL, full width, docked and always visible (not a hidden tab): "DEAD-
LETTER QUEUE" header, followed by a compact table of 2-3 rows, each showing a
timestamp, a location, a short error-code-style label (e.g. "chokepoint_busy"
in monospace), and a one-line human-readable suggested action in quotes (e.g.
"Hold at the buffer until the chokepoint clears."). This panel should look
like a permanent, always-present part of the interface, not an alert overlay
or a collapsed accordion — the design intent is that blockages are always
visible, never something the coordinator has to go looking for.

Desktop, landscape, browser-window aspect ratio (not mobile).
```

---

## Notes for whoever adds background material here

- This is the least-precedented surface in the whole set — there's no existing mockup or live implementation to reference, unlike surfaces 1, 2, and 3. If you get time with a real dock coordinator (or someone doing an analogous job), **notes from watching them work belong in `background/`** more than anywhere else in this project — this design is currently a synthesis of written requirements, not observed behavior.
- Resolve Q-43 before treating the wall-board/coordinator split as final: are these one responsive surface or two separate products? If "one," this prompt and surface 3's prompt should be merged and re-run together.
- The maker-checker (R07) approval flow implied by "Approve / Override / Reject" is described at the level of "a second person confirms" in the source docs but not specified further — if a fuller maker-checker spec exists elsewhere, it should refine the Detail/Action column here.
