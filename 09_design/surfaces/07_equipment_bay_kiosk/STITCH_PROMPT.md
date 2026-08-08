# Surface 7 — Equipment-Bay Kiosk

**Role:** Any runner, at shift start/end · **Job:** condition, fuel/charge, and position checkpoints for shared equipment (pump trucks, forklifts) · **Status:** new — the "fifth surface" that answers open question Q-42 · **Device:** shared tablet, mounted at the equipment/charging bay, kiosk mode (not a personal device)

**Source docs:** `01_product/14_surface_map.md` §"The gap this exposes," `01_product/12_ui_leverage_from_porterly.md` §"The observation that matters most"

---

## Why this surface looks the way it does — and why it exists at all

D-008 requires three equipment checkpoints — **condition, fuel/charge, returned to position** — and the runner's watch (surface 2) was deliberately ruled out for all three: they need looking at a machine, possibly a photo, and more than two taps. But runners only have watches. So these checkpoints had no home, until this surface.

**The resolution: checkpoints are location-bound, not person-bound.** They happen where the machine is parked, at shift start and shift end, regardless of who's driving that shift. A fixed shared tablet at the charging bay matches the actual workflow, needs no per-person hardware, and keeps the runner's watch to its two-tap budget. This is the recommended answer to Q-42, not yet finalized — the alternative options (runner also carries a phone; the receiver's iPhone doubles as the check device; simplify to fit the watch) were all judged worse for specific reasons documented in the surface map, worth reading before treating this as locked.

**This reuses an interaction pattern that already exists**, deliberately, rather than inventing a new one: the receiver's three-step capture strip (`LABEL · PACKAGE · SHELF`, surface 1) is structurally identical to what this screen needs — a small fixed set of captures, each with a visible done/active/pending state, completed in sequence at the point of work. Only the subject changes:
```
   Receiver (surface 1):  LABEL      ·  PACKAGE     ·  SHELF
   Equipment kiosk:        CONDITION  ·  FUEL/CHARGE  ·  POSITION
```

### Design brief

**Color** — same operational palette as the receiver, runner, and wall board (background `#0E1116`, panel `#161B22`, amber `#E0A458` for active/in-progress, green `#5FB37E` for done, red-orange `#D7503A` reserved for a failed/flagged checkpoint — e.g. reporting damage). This device lives on the same physical dock floor as the wall board and is used by the same people who wear the watch, so the vocabulary must match exactly.

**Type** — same as the receiver's phone (Inter or IBM Plex Sans), but **every element sized up** — this is a tablet mounted at arm's-plus-length, potentially touched with a gloved finger between other tasks, not held close and studied like a phone. Bigger touch targets, bigger text, less density than the phone screen.

**Layout** — one screen, kiosk mode (no navigation chrome, no way to leave the app, no back button to a home screen):
```
┌─────────────────────────────────────┐
│  EQUIPMENT CHECK — Shift Start        │
│  Pump Truck #2                        │
├─────────────────────────────────────┤
│                                        │
│   CONDITION      FUEL/CHARGE   POSITION│
│      ✓               ●            ○   │
│   No damage      [take photo]   pending│
│   reported                            │
│                                        │
├─────────────────────────────────────┤
│  Operator: [ scan badge / tap name ]  │
│  [        SUBMIT CHECK        ]       │
└─────────────────────────────────────┘
```

**Signature element**: **"who's checking in" is a tap or badge-scan, never a typed login** — this is a shared device used by whoever's on shift, so the interaction has to be as fast as picking up the machine itself. No username/password screen anywhere on this surface, ever.

---

## The Stitch prompt

```
Design a kiosk-mode tablet screen (landscape, ~10-13" tablet mounted on a wall
or stand) for equipment checkpoint verification at a shared charging/parking
bay for forklifts and pump trucks at a trade-show loading dock. This is a
SHARED device used by whoever is on shift — not a personal phone — and must
look like a fixed industrial kiosk, not a consumer tablet app. No navigation
bar, no home button, no way to back out to a device home screen — this app
fills the entire screen permanently.

DESIGN SYSTEM: near-black background #0E1116, panel surface #161B22, amber
#E0A458 for the active/in-progress checkpoint step, green #5FB37E for a
completed/passed checkpoint, red-orange #D7503A reserved only for a flagged/
failed checkpoint (e.g. reporting damage). Font: Inter or IBM Plex Sans, sized
notably larger than a phone app throughout — this is read at arm's length on a
wall-mounted tablet, sometimes touched with a gloved finger, not held close.
Minimum touch target size roughly 64px, larger than a typical mobile app.
Flat fills, no gradients, square-ish corners (4-8px radius), thick clear
borders around tappable elements so gloved/quick taps have an obvious target.

DO NOT render: a login screen with username/password fields, a settings menu,
any navigation chrome (tab bar, hamburger menu, back button), or small/dense
text — every element on this screen should read as unmistakably large and
simple, this is not a data-entry-heavy business app.

LAYOUT — a single full-screen kiosk view:
- Header, large and centered or left-aligned: "EQUIPMENT CHECK — Shift Start"
  with the specific machine identified below it in a slightly smaller but
  still prominent line: "Pump Truck #2"
- The main content area: a horizontal three-step capture strip, structurally
  identical to a phone app's step indicator but scaled up significantly for
  tablet/kiosk use — three large tappable segments side by side:
  1. "CONDITION" — shown as DONE: a large green checkmark icon, with a small
     caption beneath reading "No damage reported"
  2. "FUEL/CHARGE" — shown as ACTIVE/current: a large amber filled circle
     icon, with a caption "take photo" and this segment should look
     tappable/glowing-active compared to the other two (via border weight and
     the filled-icon vs outline distinction, not animation)
  3. "POSITION" — shown as PENDING: a large hollow/outline circle icon in
     neutral grey, caption "pending"
  Each of the three segments should be large enough to be its own big tappable
  card, not a small compact progress-bar style indicator — think three big
  buttons in a row, each showing its own state clearly via icon shape (check
  vs filled dot vs hollow ring) as well as color, so status is legible even
  without color.
- Below the three-step strip, an "Operator" row with a large tap target
  labeled "Scan badge or tap your name" — explicitly NOT a text input field or
  password field, this must look like a single-tap or badge-scan action, never
  typing
- At the very bottom, a large full-width primary button in amber/filled:
  "SUBMIT CHECK" — should look substantial and confident, sized like a real
  kiosk confirm button (think airport check-in kiosk scale), not a small web
  form submit button

Generate as a tablet/kiosk mockup, landscape orientation, mounted-device
framing if possible (e.g. shown in a simple wall-mount bezel) to reinforce
that this is fixed hardware, not a handheld device.
```

---

## Notes for whoever adds background material here

- **Confirm this design decision before treating it as final** — the surface map explicitly flags this as a recommendation ("⭐"), not a locked decision, against three other options. If a design partner or operations review picks a different answer to Q-42 (e.g. the receiver's phone doubling as the check device instead), this whole surface may not need to exist as a separate kiosk.
- The "position" checkpoint may be automatable via tagging per D-009 (per the source doc: "of the three checkpoints, tagging automates only *position*") — if that becomes real, the third step of the capture strip might collapse to an automatic confirmation rather than a manual tap, worth flagging as a likely near-term revision to this screen.
- If real charging-bay photos exist (or get taken), they belong in `images/` — the physical mounting context (height, lighting, whether it's genuinely gloved-hand-operable at that specific bay) will sharpen the touch-target sizing far more precisely than this prompt's general "make it big" instruction can.
