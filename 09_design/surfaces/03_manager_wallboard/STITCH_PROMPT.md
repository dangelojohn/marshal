# Surface 3 — Manager Wall Board

**Role:** Manager / dock coordinator · **Job:** see the whole floor, notice exceptions, rarely touch it · **Status:** new (D-006) · **Device:** large-format mounted display, desktop/TV aspect, read from ~3 metres

**Source docs:** `01_product/12_ui_leverage_from_porterly.md`, `08_infrastructure/01_raincloud_odoo_install.md` ("The wall board — live" section, already has a working demo at `/marshal/board`)

This surface already has **Nano Banana Pro image prompts** in `nano_banana_prompts/` (hero state, calm state, tablet variant) — those are illustrative renders for pitching the concept. This Stitch prompt generates the actual **on-screen web UI**, matching the design decisions already locked in and already partially implemented live.

---

## Why this surface looks the way it does

This is **facility-centric and ambient**, the opposite of the receiver's phone (item-centric, interactive, held). It's mounted, watched from three metres, and answers one question — *"is anything wrong right now?"* — without being touched. That single job drives every decision:

- **Tiles never reorder.** Their position mirrors the physical yard the coordinator has memorised. Reflowing the grid would break the mapping between screen and window, which this board must never do.
- **Status is carried by shape as well as colour** (circle / diamond / triangle), so it survives a colour-blind viewer and a sun-washed screen.
- **Exception changes border width, not just colour** — a wider border is visible from further away than a colour shift alone.
- **The clock runs off the device**, never the poll interval, so it stays an honest reference when "updated" looks wrong.
- **No animation anywhere.** A board that moves gets ignored — motion is the one thing reserved for "something needs you," and if everything moves, nothing does.
- **A dead camera degrades to a useful tile, never breaks the board.** Tile 5 in the Nano Banana hero prompt is deliberately camera-down — the design has to survive that gracefully, not treat it as an edge case to hide.
- **Staleness is stated in words**, full-width, when the endpoint is unreachable — a frozen board that still *looks* live is dangerous.

### Design brief

**Color** — the established operational palette, shared with the watch and the coordinator view: background `#0E1116`, header/panel `#161B22`, amber `#E0A458` (waiting/in-progress), exception red-orange `#D7503A`, calm green `#5FB37E`. This is now the fixed vocabulary for every Marshal operator-facing surface — don't introduce a new accent here.

**Type** — a wide, highly legible grotesk built to be read at distance: **Space Grotesk** or **IBM Plex Sans**, bold weight for tile headlines (booth/chokepoint numbers), regular for secondary detail. Numerals should use tabular/monospaced figures so times don't visually jitter tile to tile.

**Layout** — a fixed grid, one tile per chokepoint/dock/booth-zone, never scrolling, never reflowing:
```
┌─────────────────────────────────────────────┐
│  MARSHAL          Thu Aug 7  9:14:22 PM      │  ← device clock, large
├──────────┬──────────┬──────────┬─────────────┤
│ DOCK 1   │ DOCK 2   │ DOCK 3   │ DOCK 4       │
│ [camera] │ [camera] │ [camera] │ [camera:down]│
│ ● calm   │ ▲ EXCEPT │ ● calm   │ ■ no signal  │
│ PR-1041  │ delay:   │ empty    │ tile stays   │
│ due 14:20│ buffer   │          │ useful, shows│
│          │ full     │          │ "camera down"│
├──────────┴──────────┴──────────┴─────────────┤
│ (2 more rows of tiles, fixed positions)       │
└─────────────────────────────────────────────┘
```

**Signature element**: the **shape+colour+border-width triple-encoding of status** — a calm tile is a filled circle, thin border, green; an exception is a triangle, thick border, red-orange, AND (per the "no animation" rule) does NOT pulse or flash — it just sits there, unmistakably different in three independent ways at once, permanently.

---

## The Stitch prompt

```
Design a large-format ambient operations wall board web dashboard for a dock/
marshalling-yard coordinator at an exposition venue, meant to be mounted on a
wall and read from roughly 3 metres away, glanced at rather than interacted
with. This is an industrial monitoring board, explicitly NOT a SaaS analytics
dashboard — no charts, no graphs, no line/bar/pie visualizations anywhere.

DESIGN SYSTEM: near-black background #0E1116, panel/header surface #161B22,
amber #E0A458 for waiting/in-progress status, red-orange #D7503A for exceptions
ONLY, green #5FB37E for calm/normal status ONLY. Font: a wide, highly legible
grotesk such as Space Grotesk or IBM Plex Sans, bold for tile headlines,
tabular/monospaced numerals for all times and countdowns so digits don't shift
width. Flat fills, no gradients, no drop shadows, no glassmorphism. Square
corners, hairline 1px borders between tiles in a subtle grey.

DO NOT render: any chart, graph, KPI sparkline, gradient, rounded pill badges,
emoji icons, stock photography of smiling people, or any generic "business
dashboard" visual language. This must look like an industrial control-room
display, closer to an air-traffic or factory-floor monitor than a marketing
analytics tool.

LAYOUT — a fixed grid of 6-8 tiles (one per loading dock or chokepoint),
arranged 4 columns × 2 rows, NEVER described as reorderable or scrollable —
state explicitly that tile position is permanently fixed per dock:

- Top bar, full width: "MARSHAL" wordmark on the left, a large clock on the
  right showing a specific time (e.g. "9:14:22 PM") in tabular numerals — this
  clock represents the device's own local time, not a "last updated" polling
  timestamp
- Each tile contains: a header row with a dock label ("DOCK 1", "DOCK 2" etc.),
  a camera thumbnail placeholder area (roughly 60% of tile height, dark grey
  rectangle standing in for a live camera feed), and a status footer

STATUS ENCODING — this is the most important instruction in this brief. Status
must be encoded THREE independent ways simultaneously, never by color alone:
1. Shape: a filled circle icon = calm/normal. A filled triangle icon =
   exception. A filled square/diamond icon = camera offline / no signal.
2. Color: green (#5FB37E) for calm, red-orange (#D7503A) for exception, neutral
   grey for camera-offline.
3. Border width: calm tiles have a thin 1px border. Exception tiles have a
   thick 4px border in the exception color, clearly heavier than every other
   tile, visible from across a room.

Generate the board showing a MIX of states across the 6-8 tiles: most tiles
calm (green circle, thin border, showing a crate reference like "PR-1041" and
a due time like "due 14:20"), exactly ONE tile in an exception state (red
triangle, thick red-orange border, text reading "delay: buffer full" or
similar), and exactly ONE tile with its camera offline (grey square icon,
neutral border, text reading "camera down" or "no signal" — this tile must
still show useful information like the dock number and last-known status, it
must NOT look broken or empty, a dead camera should degrade gracefully to a
still-useful tile).

CRITICAL — this board must NOT include: any pulsing, glowing, blinking, or
animated visual treatment on the exception tile (describe the design as static
even though it's the most important tile — the emphasis comes from shape/color/
border-width alone, never motion). No transition effects, no hover states
described (this is a non-interactive display, not a clickable app).

If the layout tool supports a secondary state, also generate a CALM variant of
the same board with zero exception tiles and zero offline tiles — all 6-8 tiles
green, circle icon, thin border — to test that "everything is fine" reads as
genuinely uneventful, not just a duller version of the alert state.

Desktop/TV aspect ratio, landscape, meant for a large mounted display not a
laptop screen.
```

---

## Notes for whoever adds background material here

- **This surface is already partially live** — `08_infrastructure/01_raincloud_odoo_install.md` documents a working demo at `http://192.168.68.89:8069/marshal/board` (add `?demo=1` for hardcoded tiles). **Screenshot the live version and drop it in `images/` before running this prompt** — comparing Stitch's fresh take against what's actually shipped is more useful than designing blind.
- Q-43 (`14_surface_map.md`) is still open: is this the same responsive surface as the coordinator view (surface 4), or a genuinely separate product? Confirm with the design partner before merging their design systems further than "shares the same palette."
- The existing implementation notes ("served as a plain file, not through Odoo's asset pipeline," "snapshots via cache-busted `<img>`, not video") are backend/delivery decisions, not visual ones — they don't need to appear in the Stitch prompt, but are worth remembering when this design gets built for real.
