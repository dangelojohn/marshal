# Leveraging the Porterly PWA design — what transfers, what's missing

**Source:** two Porterly Inbound PWA mockups supplied by the owner, 2026-08-06
`[PRIMARY]`

**Verdict: yes — and this is a bigger contribution than the code.** These screens
solve several problems `PROJECT_PLAN.md` scoped as new Phase-1 work, and they
solve them in the right environment: a dark, loud, gloved, hurried dock.

> ⚠ **Read as design intent, not proof of implementation.** The asset inventory
> records `porterly_inbound_pwa` as *"built, deployed, actively hardened"*, so
> most of this is real — but **confirm which behaviours are shipped versus
> mocked** before planning against them. Specifically the offline queue and the
> multi-channel notification states.

---

## The screens

**Capture** — live camera with hold-steady guidance, a three-step capture strip
(`LABEL ✓ · PACKAGE (tap) · SHELF`), operator and location in the header
(*Peter Novak · Warehouse 2*), an *Arrived today* list, per-item status badges
(`STORED`, `SHELF PENDING`), and a **`3 queued · syncing`** indicator.

**Detail** — `PR-1041`, evidence photos with thumbnails and **RETAKE**, carrier /
tracking / weight / timestamp, **`Captured by PN · Bay 4 · Rack C2`**, three
notification channels each showing honest state (`Email sent ✓` /
`SMS waiting — retrying in 2 mins` / `Post to master — manual sync required`),
**`TASK: Deliver to booth`**, **`EQUIPMENT: Pump Truck #2`**, a
**chain of custody** rail (`RECEIVED ✓ → RETRIEVED → HANDOVER`), a countdown
timer, and **`FLAG TO MANAGER`**.

---

## ⭐ The observation that matters most

**The three-step capture strip is Marshal's checkpoint pattern, already designed.**

```
   Porterly:   LABEL  ✓   ·   PACKAGE  (tap)   ·   SHELF  (pending)
   Marshal:    CONDITION   ·   FUEL/CHARGE     ·   POSITION
```

Identical interaction: a small fixed set of captures, each with a visible done /
active / pending state, completed in sequence at the point of work, mostly by tap
and camera rather than typing.

D-009 concluded that of the three checkpoints, tagging automates only *position*
— **condition and fuel need a human at the machine.** This strip is exactly how
you ask for that without it feeling like paperwork. It is the single most
reusable idea in the two screens.

---

## What transfers directly

| Element | Serves | Notes |
|---|---|---|
| **Three-step capture strip** | D-008 checkpoints | The interaction pattern, above |
| **Chain of custody rail** | Movement states (`08` §1) | `RECEIVED → RETRIEVED → HANDOVER` becomes `CALLED → ON DOCK → IN TRANSIT → PLACED` |
| **`3 queued · syncing`** | **Q-19 — network drop** | **Offline-first is already designed.** A dock cannot stop because a WAN link did, and this shows the queue honestly instead of hiding it |
| **Three notification channels with honest failure states** | D-005 §4 SMS layer | This is **`avn.capability`'s connector ladder rendered as UI** — and it *shows* degraded state (`retrying`, `manual sync required`) rather than pretending success. Exactly the posture D-009 requires of the LLM layer |
| **Evidence photos + RETAKE** | **D-005 §1 defensible record** | Timestamped photographic evidence at the point of handling. The safety record's raw material, already captured |
| **`Captured by PN · Bay 4 · Rack C2`** | Position (doc `10` §2) | **Zone-level location with no BLE tags** — a human captured it at the moment of handling. Confirms zone granularity is the right target |
| **`EQUIPMENT: Pump Truck #2`** | `08` resource model | Equipment is already recorded against the item |
| **`FLAG TO MANAGER`** | D-008 human-in-loop | The exception escalation path |
| **Dark, high-contrast, large targets** | Shop-floor persona | Glare-legible, gloved-hand sized, no hover dependency. Already correct |
| **`TASK: Deliver to booth`** | — | **Expo vocabulary is native to Porterly, not retrofitted** |

**That is a great deal of Phase 1's fiddly detail already solved** — camera
capture flow, offline queue, evidence handling, custody progression, and honest
channel state are each individually annoying to get right.

---

## What's missing — and it decomposes cleanly

Marshal needs **three surfaces**. Porterly supplies one of them, and it's the one
with the most fiddly detail.

| Surface | Audience | Character | State |
|---|---|---|---|
| **Handheld** | Operator, at the machine | One item, one person, at the point of work | ✅ **Largely exists** — these screens |
| **Wall board** (D-006) | Dock coordinator, 3m away | **Many docks at once, ambient, glanceable** | ❌ New |
| **Headless core** (D-008) | Other systems | API, coordinator loop, checkpoints, ledger | ❌ New |

### Why the wall board can't be built from this design

These screens are **item-centric and interactive** — you hold the device, you
attend to one thing, you tap.

The wall board is **facility-centric and ambient** — mounted, watched at three
metres, answering *"is anything wrong right now?"* without being touched. Camera
tiles overlaid with schedule state, exceptions the only thing demanding
attention. Different information density, different type scale, different
interaction model.

**Same design language — palette, status vocabulary, custody metaphor — applied
to a different job.** Consistency of vocabulary matters more than reuse of layout.

### Gaps in the handheld itself for Marshal

- **No time or sequence dimension.** No *due at*, no *what's next*, no
  planned-versus-actual. The countdown timer hints at an SLA but Marshal needs
  the schedule explicit — that's the whole product
- **Equipment is an attribute, not a resource.** `Pump Truck #2` is recorded
  against the item. In Marshal it is a **scheduled resource with its own state,
  charge level, position and operator** (`08` §2), and it needs its own screen
- **Nothing for the checkpoint-on-equipment flow** — condition and fuel captured
  against a *machine* rather than a *parcel*. Same strip, different subject

---

## Recommendation

1. **Adopt the design language wholesale** — palette, status badges, custody rail,
   capture strip, honest channel states. Don't redesign what already works in
   this environment
2. **Reuse the capture-strip interaction for equipment checkpoints**, changing
   only the subject and the three steps
3. **Confirm what's shipped versus mocked** — specifically the offline queue and
   the notification retry states. If the offline queue is real, **Q-19 is largely
   answered** and that's significant
4. **Build the wall board as a new surface** in the same language. It's the one
   genuinely new UI in Phase 1
5. **Add the time dimension.** Every screen that shows an item should show what's
   supposed to happen to it next, and when

**Plan impact:** Phase 1's UI cost drops materially. Combined with
`03_internal_assets/04` — where the billing spine also turned out to exist —
**Phase 1 is now substantially assembly rather than invention.** The genuinely
new work is the coordinator loop, the resource model, and the wall board.

## New open questions

| # | Question | Why |
|---|---|---|
| **Q-30** | Is the offline queue actually implemented, or mocked? | If real, **Q-19 is largely answered** and it's one of the harder requirements |
| Q-31 | What does the countdown timer represent — an SLA, a hold window, a sync deadline? | May already be a scheduling primitive we can reuse |
| Q-32 | Is the capture strip configurable, or hard-coded to label/package/shelf? | Decides whether equipment checkpoints reuse the component or fork it |
