# Tracking the equipment — can we just use AirTags?

**Question (owner, 2026-08-06):** *"Can we consider AirTags, either Apple or
Android versions, to place on these expensive pieces of equipment? Could items be
tracked that way?"*

**Short answer: no — not AirTags, and not the Android equivalents.** Not because
of range, battery or cost, but because of two design decisions Apple and Google
made deliberately, both of which are fatal here.

**There is a better answer, and part of it may already be on your forklifts.**

> ⚠ **Verify before purchasing.** The session's web-search budget is exhausted
> (`06_next_steps` item 3), so the vendor and protocol claims below are from
> established knowledge, not sourced this session. The two structural blockers in
> §1 are well established and unlikely to have changed; **specific products and
> prices must be re-checked.**

---

## 1. Why consumer trackers can't do this

### Blocker 1 — there is no API. `[COMMON]`

Apple has never exposed AirTag locations programmatically. Location lives in the
**Find My app** and nowhere else. The MFi "Find My network accessory" programme
lets third-party hardware join the network, but those devices also surface only
in Find My — **there is no developer API to read an item's position.**

Google's Find My Device network is the same: no public API for tag location.

**Marshal is headless (D-008). A data source a human has to look at in a
different app is not a data source** — it's a phone call with extra steps.

### Blocker 2 — anti-stalking protection is hostile to this use case. `[COMMON]`

Apple and Google jointly built unwanted-tracker detection *into both platforms*.
A tag separated from its owner, travelling near someone else's phone, triggers an
alert on that phone and can be made to beep.

Now picture a convention floor: hundreds of exhibitor staff, contractors and
drivers, each with a phone, moving alongside tagged forklifts for days.

- Dozens of people get *"An AirTag is travelling with you"* alerts
- Any of them can make your equipment beep
- Some will report it as a stalking device

**The feature that makes AirTags safe for consumers makes them unusable for
tracking shared equipment in a crowded public space.** This is not a
configuration problem — it cannot be turned off, by design.

### The lesser problems

- **Update cadence is opportunistic** — position refreshes when an iPhone happens
  to pass. Not real-time, and useless when a hall is empty at 04:00
- **Accuracy is proximity, not position.** Sub-metre precision requires a human
  holding an iPhone in Precision Finding mode
- **Ownership is a personal Apple ID.** Equipment tags tied to a staff member's
  account walk out the door when they do

### The one legitimate use

**As a human find-aid for genuinely lost items.** A specialized cart that
vanished — someone opens Find My and walks it down. That is a real use and costs
almost nothing.

**Just never as a system input.** Marshal must not depend on it.

---

## 2. What Marshal actually needs — a smaller requirement than it sounds

From D-008, the position question is: **"was the equipment returned to the right
position?"** and **"where is forklift 3 now?"**

That is **zone-level location**, not coordinates. Marshal never needs (x,y). It
needs *Bay B*, *Level 3*, *charging bay 2*, *still in aisle 400*.

**That distinction removes most of the cost**, because zone-level tracking is
solved with cheap hardware at a handful of places — not blanket coverage.

---

## 3. The options that do work

### ⭐ BLE tags + chokepoint gateways — the right primary answer

Small BLE beacons on each unit; fixed gateways at the places equipment *must*
pass. Gateway sees tag → Marshal knows the zone.

**The key insight: you do not need continuous coverage.** Reading at the
transitions tells you nearly everything:

```
   dock doors  ·  elevator lobbies  ·  charging bays  ·  aisle heads  ·  yard gate
```

Those are exactly the points Marshal already models as constrained resources
(`08` §2). **The tracking infrastructure and the scheduling model want gateways
in the same places.**

| | |
|---|---|
| Tags | Roughly $10–30 each, multi-year battery `[ASSUMPTION — verify]` |
| Gateways | Roughly $50–200 each, need power and network `[ASSUMPTION — verify]` |
| Output | **MQTT/HTTP — a real API.** Fits headless exactly |
| Fit | ⭐⭐⭐⭐⭐ — open protocols, no vendor lock, no anti-stalking issue |

Anonymous BLE beacons on company assets raise none of the consumer-tracker
problems: no crowd-sourced network, no stranger alerts, no personal Apple ID.

### ⭐ Forklift telematics — check this before buying anything

**Modern forklifts frequently already report.** Toyota, Crown, Hyster-Yale, Linde
and others ship fleet-management telematics that typically cover:

- **hours and utilisation**
- **battery charge / fuel level** ← D-008 checkpoint, automatically
- **impact detection** ← *directly serves the safety framing in D-005*
- **operator ID** via key card or PIN ← but see §5
- pre-shift checklist enforcement on some systems

> **If the venue's forklifts have telematics, that is a better data source than
> any tag** — richer, already installed, and it answers the condition and fuel
> checkpoints that a location tag never could.

**Q-22 belongs in the Phase-0 calls:** *do your forklifts have telematics, and can
we get at the data?*

### UWB tags + anchors

Sub-30cm, real-time. Genuinely excellent, and genuinely more expensive — anchor
infrastructure throughout the space. **Overkill for zone tracking.** Revisit only
if "which booth is it at" turns out to matter more than "which zone."

### Passive UHF RFID

Very cheap tags, but needs read portals and is orientation- and
metal-sensitive. **Better suited to crates and pallets than to vehicles** — worth
keeping in mind for the empties problem, which is its own bottleneck (`06` §5).

### The cameras you already have

Reolink is installed and integrated (D-006). Object detection could identify
equipment at known points — no new hardware, but real ML work and a much less
reliable signal than a beacon. **Not a Phase-1 answer.**

---

## 4. What tagging actually buys — be precise about this

Of the three checkpoints the owner named, **tagging automates exactly one.**

| Checkpoint | Tag solves it? | What actually answers it |
|---|---|---|
| **Returned to right position** | ✅ **Yes** | BLE gateway at the bay |
| **Fuel / charge level** | ❌ No | Telematics, or a human reading a gauge |
| **Condition** | ❌ No | **Human eyes. Nothing replaces this** |

So tags remove the most tedious checkpoint — the one people skip, and the one
whose absence quietly corrupts the next plan — while the human sensors stay for
the two that need judgement.

**That is the right split**, and it strengthens rather than weakens D-008:
automate the sensor that's cheap to automate, keep humans for the ones that
require eyes.

---

## 5. ⚠ Operator tracking is a different question — handle it deliberately

Telematics operator-ID and any tag that ends up attached to a *person* rather
than a machine crosses from asset tracking into **employee monitoring**.

In Canada that engages provincial privacy law, Ontario's electronic-monitoring
disclosure requirement, and — on a unionised show floor — collective agreements.
`[COMMON, but confirm with counsel]`

**Design rule for Marshal: tag the equipment, never the person.** Where operator
identity is genuinely needed for the safety record (D-005), it should come from
an explicit action — signing on to a unit — rather than passive location.

A safety product that feels like surveillance will be rejected by the people
whose cooperation it depends on. **The distinction is not legal caution; it is
the difference between adoption and sabotage.**

---

## 6. Recommendation

1. **Don't use AirTags as a system input.** No API, and anti-stalking alerts make
   them actively disruptive in a crowded hall. Keep a couple as a human find-aid
   for lost carts — that's genuinely useful and nearly free
2. **Ask about forklift telematics before buying any hardware** (Q-22). It may
   already answer fuel, condition and utilisation better than tags ever would
3. **Plan for BLE tags + chokepoint gateways** at docks, elevator lobbies,
   charging bays and the yard gate — the same points Marshal already models as
   constrained resources
4. **Not Phase 1.** Phase 1 uses human checkpoints and camera motion. Add tags
   in Phase 2 once the zones that matter are known **from real data** rather than
   guessed — installing gateways in the wrong places is expensive and annoying to
   undo
5. **Tag equipment, never people** (§5)

---

## New open questions

| # | Question | Why |
|---|---|---|
| **Q-22** | **Do the venue's forklifts have telematics, and can we get the data?** | Might answer fuel + condition + utilisation with zero new hardware. **Add to the Phase-0 calls** |
| Q-23 | Which zones actually need to be distinguished? | Determines gateway count and placement. **Answer from Phase-1 data, not guesswork** |
| Q-24 | Who owns the equipment — venue, contractor or exhibitor (Q-13)? | You cannot tag equipment you don't own |
| Q-25 | Is there a works council or union position on equipment monitoring? | Cheaper to know before install than after |
