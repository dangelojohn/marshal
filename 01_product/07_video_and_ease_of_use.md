# Live video and ease of use — one requirement, not two

**Source:** John D'Angelo, 2026-08-06 — *"Ease of use and use of live video feed
are both important. The video cameras are Reolink."* `[PRIMARY]`

---

## The reframe: the camera *is* the interface

These arrived as two requirements. They are one.

An ops person at 6am during move-in does not read a Gantt chart. They look at
the door. **Any product that makes them translate between a schedule and reality
has already lost**, because reality is what they're accountable for and the
schedule is a claim about it.

So Marshal's primary surface is not a schedule with a video feature bolted on.

> **It is a wall of dock cameras, each tile overlaid with what is supposed to be
> happening there right now.**

Nothing to learn. The thing you already stare at, annotated with the thing you
currently keep in your head. That is what "easy to use" means here — **not fewer
clicks, no translation step.**

This is also, as far as the research found, unique. No vendor in any of the six
researched categories puts operational video and schedule state on the same
surface.

---

## What we already own — verified by direct read

`~/hermes-console/api/mcp/clients/reolink.py` and `api/mcp/tools/reolink.py`
(both present in `qnap/hermes-console.git`, so pushed and safe — **unlike the
tool-calling path in that same repo**).

**Working today:**

| Capability | Method | Value to Marshal |
|---|---|---|
| Camera auth + command layer | `_login()`, `_cmd()` | **The fiddly part is done** — Reolink's login/token dance is already handled |
| Device info | `get_dev_info()` | Inventory and health |
| **Motion state** | `get_motion_state(channel)` | **The sleeper asset — see below** |
| Snapshot URL | `get_snapshot_url(channel)` | Still image per camera, per channel |
| Multi-camera config from env | `build_cameras_from_env()` | Fleet config already modelled |

**Honest boundary — stated in the source itself (`reolink.py:16`):**

> *"Hermes does NOT stream video. Video access stays in the camera app."*

The client is deliberately **read-only: device info, motion state, snapshot
URL**. Live streaming is **not** built. That would need RTSP or HTTP-FLV pulled
straight from the cameras or an NVR, and it is genuine new work.

**Do not let anyone claim "we already have live video." We have snapshots,
motion state, and — most valuably — a working camera integration.**

---

## Motion state is the sleeper asset

`spec/03` §7 made instrumenting actuals the one decision that couldn't wait, and
flagged the obvious weakness: **humans don't reliably record variance reasons in
the middle of a chaotic move-in.** Ask a dock supervisor to tap "delayed —
reason" at 6am and you'll get nothing, or garbage.

**Motion state removes the ask.**

```
scheduled movement at door 4, 14:20–14:50
   motion at door 4 camera during window     →  it happened, roughly on time
   no motion for 20 min into the window      →  it didn't. Flag it. Ask why ONCE, later
   motion at 13:40, nothing scheduled        →  unplanned activity — safety signal
```

That is **automatic actuals capture from hardware already on the wall.** It
gives Marshal the calibration data for predictive scheduling (`spec/03`) without
asking a single person to type anything — which is the only way that data ever
actually gets collected.

It also feeds the safety framing from D-005: *powered equipment moving in an
aisle with nothing scheduled there* is precisely the exception worth surfacing.

`[ASSUMPTION]` Reolink motion detection is reliable enough at dock distances and
lighting to be a usable signal. **Test this early — cheaply, with one camera —
because a surprising amount rests on it.**

---

## Snapshot refresh probably beats live streaming for the wall board

Counter-intuitive, and worth deciding deliberately rather than defaulting to
video because video sounds better.

| | Live stream | **Snapshot refresh (2–5s)** |
|---|---|---|
| Bandwidth | High × N cameras | Low |
| Player | Needs one, and it breaks | **Just an `<img>`** |
| Tablet/kiosk | Battery and CPU cost | Cheap |
| Works over the tunnel | Painful | Fine |
| Reconnect logic | Real engineering | **Refresh the URL** |
| Enough to see a truck at a door? | Yes | **Yes** |

For a **wall board answering "is door 4 clear?"**, a 2-second-refresh still is
functionally equivalent and dramatically simpler — and it is **what our existing
client already supports.**

Live streaming earns its complexity in exactly two places: **watching a powered
movement in progress** (safety), and **incident review** (evidence). Build those
as a click-through from a tile, not as the default state of twelve tiles.

`[ASSUMPTION]` Snapshot refresh is sufficient for the board. Confirm with the
first venue — an ops person may reasonably insist on true live for safety
supervision, and that is a fair requirement, not a preference.

---

## Video closes two loops that were already open

**1. The defensible record (D-005 §1).** The safety framing's killer feature was
*"prove you controlled the floor"* — being able to answer, after an incident,
*what was supposed to be happening there?* Schedule alone gives intent. Video
alone gives event. **Together they give intent versus event, timestamped**, which
is the artifact a risk manager or insurer actually wants and which nothing on the
market produces.

**2. Billing disputes (D-005 §2).** Metering dock and handling time only turns
into revenue if it survives challenge. *"You billed three hours."* Schedule plus
timestamped stills settles it in seconds instead of becoming a credit note.

Both were already the strongest parts of the case. Video is what makes them
**evidentiary** rather than merely recorded.

---

## What "easy to use" means concretely here

The environment is a loading dock, not an office. These constraints are borrowed
from the shop-floor persona work already proven in the Southbrook stack, and they
transfer almost exactly:

- **Wall-mounted display and tablets**, not laptops. Design for 3 metres away as
  well as arm's length
- **Gloved hands** — touch targets ≥44px, **56px is the established working
  size**; never rely on hover for anything
- **Glare and mixed lighting** — high contrast, no thin light-grey type
- **Every action visibly confirms.** A silent success is a failure — if the
  operator taps "call next truck" and nothing visibly changes, they will tap it
  again
- **Never make them type during a move-in.** Tap, confirm, done. Typing is for
  the office and for afterwards
- **One-tap SMS** from the tile: *call next truck*, *hold*, *re-slot*. The SMS
  requirement from D-005 §4 lands directly on this surface

---

## The surface, concretely

```
┌──────────────┬──────────────┬──────────────┐
│  DOCK 1      │  DOCK 2      │  DOCK 3      │
│  [snapshot]  │  [snapshot]  │  [snapshot]  │
│              │              │              │
│ ● Ryder 4471 │ ○ clear      │ ⚠ NO MOTION  │
│   crate→B412 │   next 14:50 │   due 12 min │
│   on time    │   Kuehne     │   [ CALL ]   │
└──────────────┴──────────────┴──────────────┘
     12 movements queued  ·  2 running late  ·  yard: 7 waiting
```

Three states per tile — **active / clear / exception** — with colour carrying the
same meaning as the words, never colour alone. Exceptions are the only thing that
demands attention; everything else is ambient.

`[ASK]` **Is the dock office the right screen, or does it need to be in the yard
too?** A driver-facing display showing call order would remove a large volume of
radio traffic, and radio traffic is a proxy for how much coordination the system
is failing to do.

---

## What this changes

**Reuse goes up.** The Reolink integration is real, working, and already pushed —
`internal/01`'s reuse estimate didn't account for it because video wasn't a
requirement when that inventory was taken.

**A cheap early test just appeared.** Point the existing client at one camera on
one dock and log motion state against a known schedule for one show. That
validates the sleeper asset for roughly zero cost, needs no product, and answers
whether automatic actuals capture is viable — the assumption the whole predictive
layer sits on.

**New open question — Q-11:** is Reolink motion detection reliable at dock
distance and in dock lighting? Everything above assumes yes.
