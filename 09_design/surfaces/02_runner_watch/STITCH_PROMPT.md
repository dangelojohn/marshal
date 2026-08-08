# Surface 2 — Runner Apple Watch

**Role:** Runner (equipment operator — pump truck, forklift) · **Job:** execute one movement: where, what, with what, tap arrived, tap delivered · **Status:** new · **Device:** Apple Watch Ultra, 49mm

**Source docs:** `01_product/13_wearable_operator_surface.md`, `01_product/14_surface_map.md`

This surface already has a set of **Nano Banana Pro image prompts** in `nano_banana_prompts/` — those produce photographic/illustrative renders (a wrist in context, gloved thumb on the Action Button) for pitching the *concept*. This Stitch prompt is different and complementary: it generates the actual **on-screen watchOS UI**, pixel-accurate, for building against.

---

## Why this surface looks the way it does

**The design budget is two taps per movement, and the primary action is a physical button, not the touchscreen.** Capacitive touch doesn't work through a work glove; the Watch Ultra's Action Button does. Everything about this screen follows from that one constraint: **one job, never a list** (a list is the coordinator's problem — the wall board already answers it), nothing that requires typing, nothing safety-critical to *read* (a hazard warning must not depend on a glance at a 45mm screen), and no photos/checkpoints (those live on the handheld or the equipment kiosk).

This is also the highest-fidelity actuals source in the whole system — a tap at ARRIVED and a tap at DELIVERED gives an exact start and end for that movement, better than camera motion detection. The UI's whole job is to make that tap effortless enough that it actually happens, every time, without becoming a chore the operator defeats.

### Design brief

**Color** — reuse the palette already validated for the wall board exactly, since watch and board are two views into the same operational state and should read as one system: background `#0E1116`, header/card `#161B22`, accent amber `#E0A458` (the color of "current, in-progress, waiting on you"), exception red-orange `#D7503A`, calm/confirmed green `#5FB37E`. No blue in this palette — blue is unused across all Marshal operator surfaces to keep the vocabulary small.

**Type** — a rounded, high-legibility face at small watch sizes: **SF Rounded** (or if unavailable to Stitch, the closest equivalent — Manrope or Work Sans, both clean at small sizes). One size does almost all the work: the booth number is the largest thing on the screen, everything else is secondary.

**Layout** — one screen, three states:
```
JOB (default)              CONFIRMATION (after tap)      BLOCKED (escalation)
┌─────────────┐          ┌─────────────┐          ┌─────────────┐
│  BOOTH 412   │          │      ✓       │          │   BLOCKED    │
│  PR-1041     │          │  ARRIVED     │          │  reported to  │
│  Pump Truck#2│          │  14:22        │          │  coordinator  │
│ ──────────── │          │ ──────────── │          │ ──────────── │
│  due 14:20   │          │ next: 411     │          │  [ Action    │
│  ● ARRIVED   │          │  at 14:35     │          │    Button ]  │
└─────────────┘          └─────────────┘          └─────────────┘
   (amber dot echoes         (green check,             (red state,
    the Action Button)      recorded time shown          only reachable
                             back — silence reads         via side button,
                             as failure)                  not primary path)
```

**Signature element**: the amber dot beside the on-screen action label is a **visual echo of the physical Action Button** — it doesn't do anything itself (the screen is never the primary input), it just tells the wearer's eye where the real button's function is mapped right now. This is the one piece of "chrome" the screen is allowed; everything else is data.

---

## The Stitch prompt

```
Design a watchOS app screen for the Apple Watch Ultra (49mm case, rectangular-
ish rounded display, 410×502px approximate render area) for an industrial
equipment operator — a forklift or pump-truck driver moving freight at a
convention centre loading dock. This is NOT a fitness or notification watch
face. It is a single-purpose operational tool.

DESIGN SYSTEM: background near-black #0E1116, card/header surface #161B22,
single accent color amber/gold #E0A458 used for "current/waiting on you"
states, exception color red-orange #D7503A used ONLY for the blocked/escalation
state, confirmation color green #5FB37E used ONLY after a successful tap. No
blue anywhere. Font: SF Rounded or a similarly rounded high-legibility
geometric sans (Manrope as fallback), bold weight for the primary numeral/
label, regular weight for secondary lines. Flat fills only — no gradients, no
glassmorphism/blur effects, no translucent watch-face-style layering. Square-
ish corners on any card elements (8-10px radius) — NOT Apple's typical fully-
rounded watch-app card style, this should feel more like an industrial
instrument panel than a consumer wellness app.

DO NOT render: any watch face, complications, activity rings, heart rate data,
a Digital Crown close-up, or any consumer-fitness visual language at all. This
is a work tool, not a lifestyle device.

Generate THREE screen states:

STATE 1 — JOB (the default/resting screen, shown almost all the time):
- Largest element, top: "BOOTH 412" in large bold white/off-white text — this
  is the single most important piece of information and must dominate the
  screen
- Below it, smaller: "PR-1041" (the crate/movement reference) and
  "Pump Truck #2" (the assigned equipment), both in secondary grey, stacked
- A thin horizontal divider line
- Below the divider: "due 14:20" in amber text
- At the very bottom: a single row reading "ARRIVED" in white, with a small
  filled amber dot to its left — this dot is a deliberate visual echo of the
  physical Action Button on the watch's side, signaling "this is what pressing
  the button does right now," NOT a tappable on-screen button itself (the
  screen must not look like it wants to be tapped — no button chrome, no
  rounded pill background behind the text)
- No list, no scrolling content, no other UI chrome. This screen shows exactly
  one job.

STATE 2 — CONFIRMATION (shown briefly after the Action Button is pressed):
- A green checkmark icon, medium size, centered near the top
- "ARRIVED" in white below it, with the actual recorded time "14:22" beside or
  below in green — showing the recorded timestamp back is deliberate: a
  silent success reads as failure to someone wearing gloves who can't easily
  tell if a press registered, so the confirmation must show real recorded data,
  not just a generic checkmark
- A thin divider
- One quiet "next up" line below the divider: "next: Booth 411 at 14:35" in
  small grey text — exactly one line, never a list of upcoming jobs

STATE 3 — BLOCKED (the escalation state, reached via a secondary control, not
the Action Button):
- Red-orange background tint or accent (not full red screen — a red header bar
  or red icon treatment, keep most of the screen calm near-black)
- "BLOCKED" as the primary label
- "reported to coordinator" as a confirming subtext — the operator needs to
  know this escalation actually went somewhere, not just that they pressed
  something
- A small icon suggesting "waiting for coordinator" (e.g. a clock or radio-wave
  icon, not a spinner)

Render all three as Apple Watch Ultra screen mockups (device frame optional but
if included, show the physical Action Button on the watch's left side in an
orange/amber accent color, consistent with Apple's real Ultra hardware design).
```

---

## Notes for whoever adds background material here

- The **Nano Banana prompts already in `nano_banana_prompts/`** are the "photograph of the concept in use" version (gloved hand on the Action Button, in a warehouse). This Stitch prompt is the "actual pixels on the screen" version. Both are useful, for different audiences — Nano Banana for pitching/explaining the idea, Stitch for building it.
- If you commission real photography or video of an operator's hands in gloves, drop it in `images/` — it'll sharpen state 1's "does this actually work at a glance, gloved, mid-task" test far better than any render can.
- Test claim to validate before treating this as final (per `13_wearable_operator_surface.md` §8): **two taps per movement is an assumption, not a proven number.** Test with one operator for one shift before this ships as final.
