# Surface 1 — Receiver iPhone

**Role:** Receiver · **Job:** take custody of arriving freight — capture, evidence, identity, then hand it to a runner · **Status:** the base app (Porterly Inbound PWA) is built and live; Marshal adds the movement/handoff layer on top · **Device:** iPhone, portrait, PWA

**Source docs:** `01_product/14_surface_map.md`, `01_product/12_ui_leverage_from_porterly.md`

---

## Why this surface looks the way it does

The receiver's hands are free at the moment of capture and the job needs a camera, evidence review, and retake — that's why this is a phone and not a watch. It's used on a loud, dark, gloved, hurried dock, so the existing Porterly design language (dark, high-contrast, large targets, glare-legible, no hover dependency) is correct and should be **adopted wholesale, not redesigned** — the two mockups already supplied by the project owner solved camera capture flow, offline queue, evidence handling, custody progression, and honest channel state, which are each individually annoying to get right.

**What Marshal adds that Porterly doesn't have**: a time dimension. Porterly's screens show *what happened* (received, retrieved, handover) but not *what's supposed to happen next, and when*. Marshal's whole product is the schedule, so the detail screen needs a due time and a destination, not just a status.

**Put your own Porterly mockup screenshots in `images/` before running this** — the palette and type below are a reasonable reconstruction from the written description in `12_ui_leverage_from_porterly.md`, not measured from the real screens. Correct the hex values once you have the originals; everything else (the interaction pattern, the information architecture) should carry over exactly regardless of the exact palette.

### Design brief

**Color** (proposed, correct against real screenshots): `#12151A` app background (near-black, not pure black — reads better under dock lighting than #000), `#1B2028` card/surface fill, `#F4F6F8` primary text, `#8B94A3` secondary text, `#4FA8E0` in-progress/active blue (the "tap to capture" state), `#4CAF6D` done/confirmed green, `#E0A458` pending/waiting amber (shared with the wall board and watch — pending is pending everywhere in Marshal), `#E0524A` flagged/exception red.

**Type**: a body-forward grotesk built for small-screen legibility at arm's length in bad light — **Inter** or **IBM Plex Sans**, not a display face; this screen has no room for personality, only clarity. One weight jump (600 for labels/status, 400 for values) is enough — don't add a third weight.

**Layout**: two screens, matching the two mockups already supplied.
```
CAPTURE                          DETAIL
┌────────────────────┐          ┌────────────────────┐
│ Peter Novak         │          │ ← PR-1041           │
│ Warehouse 2          │          │ [photo][photo][RETAKE]
├────────────────────┤          │ Carrier · Tracking   │
│                      │          │ Weight · Timestamp   │
│   [ live camera ]    │          │──────────────────────│
│                      │          │ Captured by PN        │
├────────────────────┤          │ Bay 4 · Rack C2       │
│ LABEL✓ PACKAGE● SHELF○         │──────────────────────│
├────────────────────┤          │ TASK: Deliver→Booth 412│
│ 3 queued · syncing   │          │ due 14:20 ⏱ 22 min    │
├────────────────────┤          │ EQUIPMENT: Pump Truck#2│
│ Arrived today         │          │──────────────────────│
│ PR-1040  STORED       │          │ RECEIVED✓→RETRIEVED→HANDOVER
│ PR-1039  SHELF PENDING│          │──────────────────────│
└────────────────────┘          │ ✓Email  ⟳SMS  ⚠Manual │
                                  │ [FLAG TO MANAGER]     │
                                  └────────────────────┘
```

**Signature element**: the three-step capture strip (`LABEL ✓ · PACKAGE (tap) · SHELF (pending)`) — done/active/pending rendered as three fixed, named steps rather than a generic progress bar. This exact interaction pattern gets reused on the equipment-bay kiosk (surface 7) with different labels, so get its visual grammar right here first.

---

## The Stitch prompt

```
Design a two-screen iPhone PWA for a warehouse/exposition-dock freight receiver,
used one-handed in a dim, loud, industrial environment — think night dock at a
convention centre, not a consumer shopping app.

DESIGN SYSTEM: near-black background #12151A, card surface #1B2028, primary
text #F4F6F8 off-white, secondary text #8B94A3 grey. Status colors used
consistently: #4FA8E0 blue = active/in-progress, #4CAF6D green = done/confirmed,
#E0A458 amber = pending/waiting, #E0524A red = flagged/exception. Body font: a
clean grotesk (Inter or IBM Plex Sans), only two weights (600 semibold for
labels, 400 regular for values). Flat fills, no gradients, no drop shadows
heavier than a 1px hairline border in a slightly lighter grey than the
background. Square-ish corners (4-8px radius), never fully rounded pill shapes
— this is an industrial tool, not a social app. Large tap targets (min 44px)
sized for gloved or cold hands.

SCREEN 1 — CAPTURE (the default/home screen):
- Header: operator name "Peter Novak" and location "Warehouse 2", small and
  quiet, top-left
- Full-width live camera viewfinder taking up roughly 40% of the screen height,
  with a thin corner-bracket frame overlay (not a full rectangle border) and a
  one-line hold-steady instruction beneath it
- Below the camera: a three-step horizontal capture strip with three segments —
  "LABEL" (checkmark icon, green, done), "PACKAGE" (filled blue dot, active,
  labelled "tap to capture"), "SHELF" (hollow outline, grey, pending) — each
  segment is tappable and shows its own done/active/pending state distinctly,
  not just via color but via icon shape too (check vs filled dot vs hollow
  ring), so it still reads correctly if colorblind
- A thin status bar: "3 queued · syncing" with a small sync icon — must look
  calm/informational, not alarming, since this is a normal offline-first state
  not an error
- Below that, a scrollable list "Arrived today" — each row shows a tracking
  code (e.g. "PR-1040"), a status pill ("STORED" in green, "SHELF PENDING" in
  amber), and a timestamp, right-aligned

SCREEN 2 — DETAIL (tapping a list row opens this):
- Back arrow + tracking code as the header ("PR-1041")
- A horizontal row of 2-3 evidence photo thumbnails with a "RETAKE" text
  button beside them
- A compact metadata block: Carrier, Tracking number, Weight, Timestamp — label
  above value, small caps labels in secondary grey, values in primary white
- "Captured by PN · Bay 4 · Rack C2" as a single quiet line — this is the
  zone-level location captured by a human, not a GPS pin, don't render a map
- A NEW block Marshal adds (not in the original Porterly design) —
  "TASK: Deliver to Booth 412" as a prominent line, with "due 14:20" and a live
  countdown "22 min" beside it in amber if under 30 minutes remaining, red if
  overdue. Below it "EQUIPMENT: Pump Truck #2"
- A horizontal custody rail with four stages connected by a line:
  "RECEIVED" (green, checked) → "RETRIEVED" (grey, next) → "HANDOVER" (grey) —
  render as connected nodes on a horizontal timeline, the current stage
  highlighted, future stages dimmed but visible (never hidden)
- Three notification-channel rows, each showing HONEST state, not just a
  generic "sent" checkmark: "Email  ✓ sent", "SMS  ⟳ retrying in 2 min",
  "Master system  ⚠ manual sync required" — three different states rendered
  distinctly (checkmark/spinner/warning triangle), because pretending
  everything succeeded when it didn't is the one thing this screen must never
  do
- A full-width secondary (not primary-colored, outlined) button at the very
  bottom: "FLAG TO MANAGER" in red outline — this is an escalation path, it
  should look available but not attention-grabbing until pressed

Generate both screens as a connected flow (tapping a capture-strip photo leads
toward the detail view's evidence section; tapping a list row on screen 1 opens
screen 2). Mobile, portrait, iPhone frame, PWA aesthetic not native-iOS chrome.
```

---

## Notes for whoever adds background material here

- Drop the **real Porterly Inbound PWA screenshots** in `images/` — this prompt was written from the written description in `12_ui_leverage_from_porterly.md`, not from pixels. Once real screenshots are here, re-run with "match the attached reference exactly, only add the TASK/EQUIPMENT/countdown block" instead of describing the whole screen from scratch.
- Confirm before treating as final: **is the offline queue real or mocked** (Q-30 in `12_ui_leverage_from_porterly.md`)? If real, design the "3 queued" state to look genuinely reliable, not tentative — it's a solved problem, not a caveat.
- The capture strip's exact three labels (LABEL/PACKAGE/SHELF) are Porterly's, for parcels. Don't let Stitch invent new ones — they're deliberate and get reused verbatim on the equipment kiosk (surface 7) with different subjects.
