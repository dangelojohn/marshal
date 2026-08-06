# The wrist surface — where next, what, when, and one tap

**Source:** John D'Angelo, 2026-08-06 `[PRIMARY]`

> *"We might also consider an Apple Watch interface for the employees running the
> pump trucks and forklifts, so they have another tangible surface for where to
> go — what booth, when, with what package — and tap when they have arrived and
> delivered their packages."*

**Yes. And it's worth more than a convenience — it may be the best actuals source
in the whole system.**

---

## 1. Why the wrist is right for this specific person

An equipment operator's hands are **on the controls**. A phone costs them:

> stop → free a hand → find pocket → maybe remove a glove → unlock → find app →
> read → act

That is 15–20 seconds and a break in concentration, **repeated dozens of times a
shift.** It is exactly why operators don't update systems — not unwillingness,
just an interaction budget that doesn't fit the job.

A wrist glance is **one second**, and a haptic tap needs no glance at all.

The information an operator needs is also, conveniently, tiny:

```
   ┌──────────────────┐
   │  BOOTH 412       │
   │  Crate PR-1041   │
   │  Pump Truck #2   │
   │  ──────────────  │
   │  due 14:20       │
   │  [   ARRIVED  ]  │
   └──────────────────┘
```

**One job. Never a list.** A list is the coordinator's problem, not the
operator's — and the wall board (D-006) already answers it.

---

## 2. ⭐ The part that matters most: this is the best actuals source we have

`spec/03` §7 made instrumenting actuals the decision that couldn't wait. Marshal
now has **three** possible sources, and they are not equal:

| Source | Fidelity | Cost to operator | Precision |
|---|---|---|---|
| Camera motion (D-006) | Low — *"something happened at door 4"* | **Zero** | ±poll interval, zone-level |
| Human checkpoint | High | Moderate — a deliberate stop | Point-in-time, occasional |
| **Watch tap** | **High** | **One tap, hands mostly stay put** | **Exact, per movement, both ends** |

**A watch tap at *arrived* and *delivered* gives an exact start and end for that
movement, from the person who was there.**

That is precisely the duration data Phase 2's scheduler needs — better than motion
detection, and cheap enough that it might actually get done. Motion state answers
*did it happen*; the watch answers *how long did it take, door to booth, with that
equipment, in that aisle*.

**It may quietly de-risk Q-11 as well.** If watch taps prove reliable, the
predictive layer no longer depends on motion detection working at dock distance —
motion becomes corroboration rather than the primary signal.

---

## 3. ⚠ Gloves — the constraint that decides the hardware

**The Apple Watch touchscreen does not work with most work gloves.** Capacitive
touch needs skin or conductive fabric. On a dock in winter, in Toronto, that is
not an edge case — it is the normal condition.

**Design the primary action around a physical control, never the screen.**

| Input | Works gloved? | Use for |
|---|---|---|
| **Action Button** (Watch Ultra) | ✅ **Yes — physical** | **`ARRIVED` / `DELIVERED`. The whole product** |
| Digital Crown | ✅ Yes | Scroll, confirm |
| Side button | ✅ Yes | Secondary action |
| Double Tap *(Series 9+)* | ⚠️ Thin gloves only | Convenience, never the only path |
| Touchscreen | ❌ **No** | Never load-bearing |

> **The Apple Watch Ultra's Action Button is the single detail that makes this
> viable.** A programmable physical button, pressable with a work glove, mapped
> to the one action an operator performs all day. Ultra also brings a brighter
> screen for glare and ~36h battery against a 14-hour move-in.

**A standard Apple Watch is a poor fit** — no Action Button, ~18h battery, dimmer
screen.

---

## 4. The honest alternative: industrial wrist wearables

If devices are **facility-provided** (Q-20), a consumer smartwatch is probably the
wrong tool.

| | Apple Watch Ultra | **Industrial wearable** (Zebra WS50 and similar) |
|---|---|---|
| Gloves | Action Button only | ✅ **Designed for gloved use** |
| Ruggedness | Good | ✅ **Drop/dust/water rated for warehouse** |
| Battery | ~36h | ✅ **Hot-swap batteries** |
| Barcode scan | Camera, awkward | ✅ **Built-in scanner** |
| Fleet management | MDM, per-Apple-ID friction | ✅ **Shared-device, shift login** |
| Cost | Higher per unit | Comparable or lower |
| **Shared across shifts** | ⚠️ Awkward — personal device model | ✅ **Built for it** |

**That last row is decisive.** Equipment operators work shifts. An Apple Watch is
architecturally a *personal* device — pairing, Apple ID, wrist detection. A device
handed to whoever is on shift fights that model constantly.

**Recommendation:**
- **Operators using their own devices → Apple Watch Ultra**, Action Button primary
- **Facility-provided, shared across shifts → industrial wrist wearable**
- **Either way, Marshal doesn't care** — see §5

---

## 5. Architecturally this costs almost nothing, and that's the point

D-008 made Marshal headless: **the scheduler is the product, every screen is a
client.** The watch is simply another client.

```
                MARSHAL CORE (headless)
                        │  REST / GraphQL
   ┌────────┬───────────┼───────────┬──────────┐
 wall      handheld    SMS       ⌚ watch    facility
 board      (PWA)    (drivers)  (operators)   systems
```

**No core change. No new concepts.** A movement already has a destination, a
crate, an equipment assignment and a due time — the watch renders four fields of
a record that exists, and writes two timestamps back.

**This is the first real test of whether the headless decision was right, and it
passes cheaply.** If adding a surface required touching the core, D-008 would be
wrong.

---

## 6. What belongs on the wrist — and what must not

**On the wrist:**
- The **current** movement — booth, crate, equipment, due time
- **Haptic** on new assignment. No glance needed
- `ARRIVED` · `DELIVERED` — physical button
- `BLOCKED` — one escalation, routed to the coordinator

**Never on the wrist:**
- Photos or evidence capture → handheld
- Condition/fuel checkpoints → handheld, at the machine
- Lists, schedules, history → wall board
- Anything requiring typing
- **Anything safety-critical to *read*** — a hazard warning must not depend on a
  glance at a 45mm screen

**Two taps per movement is the design budget.** If a third appears, something
belongs on a different surface.

---

## 7. ⚠ This is a wearable on a person — handle it as such

D-009 set the rule: **tag equipment, never people.** A wrist device is worn by a
person, and it will know where they are and how fast they work.

- Marshal should record **the movement**, not the operator's location between
  movements
- No idle tracking, no productivity leaderboards, no dwell-time-by-person
- Ontario's electronic-monitoring disclosure applies; on a unionised floor, so
  does the collective agreement (Q-25)
- **Frame and build it as a tool that saves the operator effort**, because that
  is what it is — the arrival tap replaces a radio call

**Get this wrong and the watches end up in a drawer.** A wearable that feels like
a tracking anklet will be defeated, and it will take the actuals data with it.

---

## 8. Verdict

**Adopt — Phase 1, but after the handheld and the wall board.**

It is the cheapest high-fidelity actuals source available, it fits the operator's
real interaction budget, and it costs the architecture nothing. But it depends on
a scheduler producing assignments worth pushing, so it can't be first.

`[ASSUMPTION]` Two taps per movement is achievable. **Test with one operator for
one shift before buying hardware** — the same shape as Q-11's camera test.

## New open questions

| # | Question | Why |
|---|---|---|
| **Q-38** | Operators' own devices or facility-provided? *(refines Q-20)* | **Decides Apple Watch Ultra vs industrial wearable.** The shared-shift model is the deciding factor |
| Q-39 | Battery over a full 14-hour move-in with frequent haptics? | Ultra ~36h nominal; real duty cycle is unknown. Hot-swap wearables sidestep it |
| Q-40 | Does the watch need to work when the network drops (Q-19)? | If yes it needs a local queue — the same outbox problem as R15 |
| Q-41 | Is there a union position on wearables specifically? | Distinct from equipment monitoring. Ask before buying |
