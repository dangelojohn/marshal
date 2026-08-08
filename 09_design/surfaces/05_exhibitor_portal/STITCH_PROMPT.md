# Surface 5 — Exhibitor Portal

**Role:** Exhibitor (primary) + Show manager (read-only view of the same portal) · **Job:** exhibitor declares what's coming and tracks status; show manager gets floor-wide visibility without operating anything · **Status:** the base app (Porterly Outbound PWA) is live; Marshal's movement/schedule data is the new addition · **Device:** responsive web, desktop-first (booked from an office) but must hold up on mobile

**Source docs:** `01_product/14_surface_map.md` §"Customer — SMS + portal"

---

## Why this surface looks the way it does

This is the one surface in the whole system that is **not** operator-facing, and it should look like it. Every other Marshal surface (receiver, runner, wall board, coordinator, equipment kiosk) is used by someone on a loud, dark dock floor, in gloves, under time pressure — dark, high-contrast, industrial. **The exhibitor is a business person in an office, planning a shipment days or weeks ahead**, and the show manager is checking status from a laptop, not a dock. This surface can and should look like a calm, professional B2B logistics tool — closer to a shipping/freight-tracking product than a warehouse console.

Two genuinely different jobs live in one portal:
- **Exhibitor**: declares what's coming (carrier, contents, expected arrival window), and tracks it once it's moving — this is the primary, write-capable view.
- **Show manager**: wants floor-wide visibility across every exhibitor's shipments, read-only — they're not moving anything, just watching the whole show's logistics converge.

Both views share the same visual language; the show-manager view is the exhibitor's single-shipment tracker generalized to a filterable table of everyone's shipments.

### Design brief

**Color** — a deliberately different palette from every operator-facing surface, since this genuinely is a different subject for a different audience: warm off-white background `#FAF8F4` (not stark white — this is a professional tool, not a form), deep ink `#1C1F26` for primary text, a confident mid-blue `#2A5FA3` as the single brand/action accent (buttons, links, active states), amber `#C98A2C` for in-transit/pending (a warmer, less saturated cousin of the operator-surface amber, keeping the family resemblance without being identical), and a muted forest green `#3E7A5C` for delivered/complete. Status colors intentionally desaturated compared to the operator surfaces — this audience reads calmly, not at a glance from three metres under stress.

**Type** — a text-forward serif/sans pairing that reads as considered rather than templated: **Newsreader** (serif) for the shipment headline/tracking number display, **Public Sans** or **Work Sans** for body/UI text and data tables. This is the one Marshal surface with room for a display face — use it once, on the tracking number itself, not throughout.

**Layout** — two views:
```
EXHIBITOR: "My Shipment"                SHOW MANAGER: "Floor Overview"
┌────────────────────────┐          ┌────────────────────────┐
│  PR-1041                 │          │ Floor Overview  [filter▾]│
│  Newsreader, large        │          ├────────────────────────┤
├────────────────────────┤          │ Exhibitor │ Status │ ETA  │
│ ● Declared → ● In transit│          │ Acme Co.  │●transit│14:20│
│   → ○ Arrived → ○ Placed │          │ Beta Inc. │○arrived│  —  │
├────────────────────────┤          │ Cee Corp. │●declared│15:00│
│ Carrier: RainFreight      │          │ ...        │        │      │
│ Expected: Today, 14:00-16:00│         └────────────────────────┘
├────────────────────────┤
│ SMS alerts: ON  [toggle]  │
│ [Declare a shipment +]    │
└────────────────────────┘
```

**Signature element**: the **shipment status stepper rendered as a horizontal timeline with real dates/times attached to completed steps, not just labels** — Declared → In transit → Arrived → Placed, each completed step showing exactly when it happened. This is the customer-facing version of the same custody-chain idea that runs through every other Marshal surface, translated into a register a non-operator reads comfortably.

---

## The Stitch prompt

```
Design a responsive web portal for exhibitors at a trade show to declare and
track incoming freight shipments to their booth, plus a read-only "floor
overview" variant of the same portal for a show manager watching all
exhibitors at once. This is a calm, professional B2B logistics/shipping tool
— think a courier tracking page crossed with a freight-booking form — NOT an
industrial dock-floor console (that's a different, separate surface in this
project; don't reuse dark/high-contrast operator styling here).

DESIGN SYSTEM: warm off-white background #FAF8F4 (not pure white), deep ink
#1C1F26 for primary text, confident mid-blue #2A5FA3 as the single accent
color for buttons/links/active elements, warm amber #C98A2C for in-transit/
pending status only, muted forest green #3E7A5C for delivered/complete status
only. Typography: Newsreader (a serif) used ONCE, for the large shipment
tracking-number headline only — everywhere else use Public Sans or Work Sans
for a clean, legible sans body/UI face. Generous whitespace, soft 8-12px
corner radius on cards (a deliberately softer, warmer geometry than a strict
industrial tool would use), subtle 1px borders in light warm grey, no heavy
shadows.

DO NOT render: dark backgrounds, neon/saturated status colors, industrial
iconography (no forklift/warehouse imagery), or generic stock-photo hero
banners. Keep this text-and-data forward, like a real freight-tracking
product, not a marketing landing page.

SCREEN 1 — EXHIBITOR VIEW ("My Shipment"):
- Header: the tracking code "PR-1041" set large in the serif display face,
  with a smaller company/booth line beneath it ("Acme Co. · Booth 412")
- A horizontal status stepper with four stages connected by a line: "Declared"
  (filled blue circle, done), "In transit" (filled amber circle, current),
  "Arrived" (hollow circle, pending), "Placed" (hollow circle, pending) — each
  COMPLETED stage shows a small timestamp beneath its label (e.g. "Declared —
  Aug 5, 9:14 AM"), pending stages show no timestamp yet
- Below the stepper, a compact detail card: "Carrier: RainFreight Logistics",
  "Expected arrival: Today, 2:00 PM – 4:00 PM", shown as clean label/value
  pairs, generous line spacing
- An "SMS alerts" toggle switch, clearly in the ON position, with a one-line
  caption "Get a text when your shipment is 30 minutes out"
- A prominent primary button, filled blue, rounded corners: "Declare a new
  shipment +"
- Below the fold, a simple list of past/other shipments for the same
  exhibitor, each row showing tracking code, a small status pill, and date

SCREEN 2 — SHOW MANAGER VIEW ("Floor Overview") — a structurally different
screen, not just the same page with more rows:
- Header: "Floor Overview" with a filter/dropdown control (e.g. "All
  exhibitors ▾") and a search field
- A clean data table, NOT cards: columns for Exhibitor name, Booth number,
  Status (small colored pill matching the same status vocabulary — blue/amber/
  green), and ETA or arrival time. Roughly 6-8 visible rows, alternating
  subtle row shading for scanability
- No action buttons anywhere on this screen except perhaps a row-level "View
  detail" link — this view is explicitly read-only, the show manager can look
  but not touch, so the design should NOT include any primary/filled action
  buttons the way the exhibitor screen does — only quiet outlined or text
  links

Generate as a responsive web layout, desktop-first (a wide browser window),
but describe it as needing to degrade gracefully to a single-column mobile
layout for the exhibitor view specifically (the show-manager table view can
remain desktop-oriented).
```

---

## Notes for whoever adds background material here

- **This is the second surface (after the receiver) built on an existing Porterly base — the Porterly Outbound PWA is already live.** Screenshot the real thing and put it in `images/` before treating this prompt's layout as final; the design brief above is a reasonable B2B-logistics direction but hasn't been checked against what already exists and works.
- The driver is explicitly **not** part of this portal (surface 6, SMS-only, "will never log in") — don't let a future revision try to add a driver login here, that was a deliberate exclusion in the source doc, not an oversight.
- If a design partner reviews the "different visual identity from the operator surfaces" choice and prefers one unified Marshal look across every surface instead, that's a real, legitimate alternative — flag it as a decision to make explicitly rather than silently drifting one way or the other across surfaces.
