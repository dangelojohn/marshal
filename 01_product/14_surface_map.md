# The surface map — one per role

**Source:** John D'Angelo, 2026-08-06 `[PRIMARY]`

> *"Receivers get iPhone, runners get Apple Watch, managers get web interface,
> customers get SMS and a web portal."*

---

## The map

| Role | Surface | Job | State |
|---|---|---|---|
| **Receiver** | **iPhone** | Take custody of arriving freight — capture, evidence, identity | ✅ **BUILT AND LIVE** — Porterly Inbound PWA |
| **Runner** | **Apple Watch** | Execute one movement: where, what, with what — tap arrived, tap delivered | ❌ New |
| **Manager** | **Web** | See the whole floor, resolve exceptions, approve | ❌ New — the wall board (D-006) |
| **Customer** | **SMS + web portal** | Tell us what's coming, find out where it is | ⚠️ Portal ✅ **LIVE** (Outbound PWA) · SMS designed, not built |

**Two of four already exist and are in production.**

---

## Why five surfaces is *fewer*, not more

The original brief asked for **"as few surfaces as possible."** `spec/01` proposed
three. This is more — and it is the better answer, because the metric was wrong.

> **What matters is not how many surfaces exist. It is how many any one person has
> to learn.**
>
> **Here, that number is one.**

`spec/01`'s three surfaces were **role-spanning** — a shared console for venue ops
*and* show managers, meaning both had to navigate past the other's concerns to
reach their own. Four role-scoped surfaces where nobody ever sees another role's
screen is **simpler for every individual**, even though the system has more of
them.

This only works because of D-008. **One headless core, four renderings.** They are
not four apps with four data models — they are four views of one set of records.
Adding a surface costs a client, not a system.

---

## Surface by surface

### 📱 Receiver — iPhone · *already built*

Porterly Inbound PWA, live since 2026-07-21. Three-shot capture
(`LABEL · PACKAGE · SHELF`), draft `parcels.tracking` with real `PR###`
sequence, **idempotency via `capture_uuid`**, geo, captured-by, 90s idle
auto-logout, native-camera fallback.

**Marshal adds:** the movement that follows — *this crate is going to booth 412,
by pump truck, at 14:20.* Custody hands off to a runner.

**Why a phone and not a watch:** the receiver's hands are free at the moment of
capture, and the job needs a camera, evidence review and retake. A watch cannot
do this and shouldn't try.

### ⌚ Runner — Apple Watch · *new*

One movement at a time. Never a list.

```
   BOOTH 412  ·  PR-1041  ·  Pump Truck #2  ·  due 14:20
                    [ Action Button → ARRIVED ]
```

**Design budget: two taps per movement.** Gloves mean the **Watch Ultra's
physical Action Button carries the primary action** — never the touchscreen
(`13` §3).

**This is also the best actuals source in the system** — an exact start and end
per movement, from the person who was there.

### 🖥 Manager — web · *new*

Two jobs that may want two layouts:

- **The wall board** (D-006) — mounted, ambient, read at three metres. Camera
  tiles overlaid with schedule state. **Exceptions are the only thing that
  demands attention.** Rarely touched
- **The coordinator view** — interactive, at a desk. The queue, overrides,
  approvals (R07's maker-checker), the day's review

`[ASSUMPTION]` These are one responsive surface, not two products. **Confirm with
the design partner** — a coordinator standing at a wall board with a mouse is a
different person from one sitting at a desk.

### 💬 Customer — SMS + portal

**"Customer" is three different parties.** Worth separating, because their needs
diverge sharply:

| Party | Surface | Why |
|---|---|---|
| **Driver / carrier** | **SMS only** | **In a truck. Will never log in.** *"Dock 4 at 14:20. Reply Y."* |
| **Exhibitor** | Portal + SMS | Declares what's coming (Outbound PWA ✅ live), tracks status. SMS for time-critical alerts |
| **Show manager** | Portal, read-only | Wants floor-wide visibility, not to operate anything |

Free-text SMS replies are parsed by the LLM into structured intent, with a
keyword fallback when the model is unreachable (D-009).

---

## ⚠ The gap this exposes: where do equipment checkpoints happen?

D-008 requires three checkpoints — **condition, fuel/charge, returned to
position.** `13` §6 ruled these off the watch: they need looking at a machine,
possibly a photo, and more than two taps.

**But runners only have watches.** So the checkpoints currently have no home.

Four options:

| Option | Trade |
|---|---|
| Runner also carries an iPhone | Realistic, but erodes the reason for the watch |
| **Shared tablet at the equipment/charging bay** | ⭐ **Checkpoints happen where the equipment is.** One device per bay, not per person |
| Receiver's iPhone doubles as the shift-start check device | Cheap, but couples two roles awkwardly |
| Simplify enough to fit the watch | *Position* could be a short pick-list. **Condition and fuel cannot** — they need eyes and probably a photo |

**Recommendation: a shared tablet at the equipment bay.** Checkpoints are
*location-bound* rather than person-bound — they happen where the machine is
parked, at shift start and shift end. A fixed device at the charging bay matches
the actual workflow, needs no per-person hardware, and keeps the runner's watch
to two taps.

**That is a fifth surface** — and it still costs one screen for one job, seen by a
person who already sees a watch. **Q-42.**

---

## What's built vs what's new

```
  ✅ LIVE      Receiver iPhone      Porterly Inbound PWA
  ✅ LIVE      Exhibitor portal     Porterly Outbound PWA
  ⚠  DESIGNED  Driver SMS           D-005 §4 — not built
  ❌ NEW       Runner watch         13
  ❌ NEW       Manager web          D-006 wall board
  ❌ NEW       Equipment-bay kiosk  Q-42
```

**Half the surface area is already in production.** The new work concentrates
where Marshal is actually differentiated: **the runner's watch, the manager's
board, and the coordinator loop underneath them.**

## New open questions

| # | Question | Why |
|---|---|---|
| **Q-42** | **Where do equipment checkpoints happen?** | Runners have watches; checkpoints need more. **Leaning: a shared tablet at the equipment bay** |
| Q-43 | Is the manager's wall board and coordinator view one responsive surface or two? | Standing-at-a-wall differs from sitting-at-a-desk |
| Q-44 | Do receivers and runners overlap in practice, or are they distinct people? | If one person does both, the device split needs rethinking |
| ~~Q-38~~ | ~~Own devices or facility-provided?~~ | **RESOLVED — facility-provided, Apple ecosystem** |
