# Round 1 — Employee scheduling candidates (RAW + my flags)

**Agent:** low-cost generator, focus = scheduling company employees. 14 candidates.
**Status:** RAW, pre-adversarial. Materially stronger set than the efficiency one.

## ⭐ The synthesis insight the agent missed

It marked five candidates as "FAILS REVIEW" on union/privacy grounds. **Look at
what actually fails in each:**

| Candidate | The good mechanism | The part that kills it |
|---|---|---|
| SHCC — custody chain | **Dual attestation on handover** | GPS logging + "blockchain-lite" + framing operators as suspected thieves |
| WSIGD — offline watch shift | **Offline cache so work continues** | Geofencing |
| FWDL — fair distribution | **Balancing hours across the crew** | Weighting by "unpopular job type" — correlates with protected classes |
| SDCR — skill decay | **Activity-based competency expiry** | Labelling a person "rusty" |

> **In every case the mechanism is sound and a surveillance layer was bolted on
> top of it. Strip the surveillance and most of these survive.**

A handover receipt signed by two people is **not** surveillance — it is how every
warehouse in the world has worked for a century. GPS on the person is. **That
distinction is the whole game**, and it is exactly D-009's rule: *record the
movement, never the operator's location between movements.*

## ⭐ SHP and SHCC are the same idea at two surveillance intensities

Candidate 2 (Shift Handover Protocol) passed at risk 6. Candidate 12 (Custody
Chain) failed at risk 9. **They are the same mechanism.** The difference is GPS
and framing.

**Resolution:** take SHP's workflow, give it the immutability we already have
from **R04's per-parcel hash chain** (D-011) — which is per-artifact, not
per-person — and drop GPS entirely. Full auditability, zero surveillance of
people.

## 🚩 Two independent agents proposed watch look-ahead — my doc says no

`01_product/13` §6 states **one job, never a list.** Both the efficiency agent
(#10) and this one (WSIGD) independently proposed showing the next N movements,
with the same reasoning: knowing what's next lets a runner pre-position and
prepare equipment, saving the hand-off gap.

**That's a real argument and two independent hits is a signal, not noise.**
Likely resolution: **one job, plus a single glanceable next-up line** —
*"next: booth 118 · 14:50"*. Not a list, not blind. **Needs deciding, not
dismissing.** → Q-45.

## Carried into the adversarial pass

| Cand | Name | Value | Risk | My read |
|---|---|---|---|---|
| 1 | **Certification-first roster** | 9 | 5 | ⭐ Non-negotiable. A hard constraint, not a preference — you cannot roster someone onto equipment they aren't certified for |
| 2 | **Shift handover protocol** | 9 | 6 | ⭐ **The most important idea in this set.** A shift ends with a crate in the elevator and nobody owns it. This is a *custody* problem wearing a scheduling costume |
| 3 | **Fatigue / safety-hours limits** | 8 | 3 | ⭐ Best value-to-risk ratio here. Legal, safety, and unions *expect* it |
| 11 | **Activity-based skill decay** | 6 | 6 | ⭐ Genuinely clever — a pump-truck operator who hasn't touched one in 9 months is dangerous, and date-based expiry misses it entirely. **Salvage by flagging the certification, never the person** |
| 4 | Absence backfill by skill match | 7 | 4 | Good — surge resilience |
| 14 | Offline roster cache | 7 | 3 | Required by Q-19 regardless |
| 5 | Breaks + overtime as scheduled state | 7 | 4 | A break is *capacity off the board*, which the planner must know |
| 7 | Certification expiry workflow | 6 | 2 | Cheap, low risk, proactive |
| 8 | Cross-training / mentorship hours | 7 | 5 | Strategic bench depth. Later |
| 9 | Call-in surge pool with pay tiers | 7 | **8** | Necessary for a 1–3 day surge, but auto-escalating pay tiers by SMS reads badly. **Needs human approval per tier** |
| 6 | Fair distribution lottery | 6 | 7 | **Salvage the hours-balancing, discard the job-desirability weighting** |
| 12 | Custody chain + GPS + hash | 8 | 9 | **Merge into #2, drop GPS** |
| 10 | Watch offline + geofencing | 7 | 8 | **Salvage offline, drop geofencing** |
| 13 | Predictive individual absence | 5 | 9 | ❌ **NEVER.** Modelling which individual will call in sick is invasive, probably discriminatory, and worth little. Put it on the never-build list |

## Genuinely new (not already in our docs)

1. **Shift handover as a custody transfer** — the single best idea from this round
2. **Certification as a hard scheduling constraint with expiry** — and the roster
   refuses, rather than warns
3. **Activity-based skill decay** — competency rots from disuse, not just from time
4. **A break is scheduled capacity-off-the-board**, not an absence of data
5. **Fatigue limits as a planner constraint**, enforced at assignment time rather
   than audited afterwards
