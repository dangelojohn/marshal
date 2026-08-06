# Round 1 — Automation + Headless candidates (RAW + my flags)

**Status:** RAW, pre-adversarial.

---

# AUTOMATION set

## ⚠ Flags

**1. Several candidates smuggle in worker geofencing.** Candidates 2, 12 and 13
validate a runner's tap or photo against **the runner's GPS location**. That
violates D-009's rule — *tag equipment, never people.* The author didn't notice
because it reads as a data-quality measure rather than surveillance.

There is also a practical problem: GPS inside a hotel basement or a steel-framed
exhibition hall is unreliable to ±30m, which the agent itself flagged for
candidate 13. **So it's both against the rules and doesn't work.** Validate
against the *movement* (was the crate placed?) not the *person's coordinates*.

**2. The "spoofing" framing in candidate 12 is the wrong instinct.** It worries a
runner might tap ARRIVED, get coffee, then tap DELIVERED. True — but the fix
proposed is more surveillance. **The better answer: those timestamps exist to
calibrate the schedule, not to police people.** If someone games them, the
schedule degrades and shows up as variance. You do not need to watch a person to
notice their durations are wrong.

**3. Candidate 5 (aisle clearance) is correctly identified as a safety
boundary** — but the agent's own warning is the important part and should be
carried forward verbatim: *if the camera has a systematic blind spot, humans
will rubber-stamp the release every time and stop checking carefully.* **A
confirm-button that is always pressed is worse than no automation**, because it
manufactures a false audit trail. Either fix the camera coverage or don't
automate the release.

## ⭐ The strongest thing in this set

**The NEVER-AUTOMATE list.** Eight items, each with a reason. The best of them:

- **Plans are social contracts.** Automatic rescheduling breeds *"why did the
  schedule change? The system did it."* Humans must own the plan and be able to
  explain changes
- *"The system said it was OK"* is not acceptable insurance language
- Automation is an optimisation layer on deterministic observation + human
  verification. **It saves seconds, not minutes.** If it breaks, the facility
  falls back to manual — and that must be survivable

That last line is the correct posture for the whole product and should go in the
plan.

## Carried forward
A1 checkpoint failure → auto `maintenance.request` (fully-auto after a human
confirms the failure — no value in a second approval) · A2 unscheduled motion →
safety exception · A3 aisle release **propose-only** · A4 schedule drift alert ·
A5 battery gating (telematics-dependent) · A6 offline replay with a staleness
limit.

---

# HEADLESS set — the strongest round

This agent did the thing the others didn't: **it answered the hard question
honestly instead of routing around it.**

> *"The dock cannot keep running with zero Odoo uptime. The best you can achieve
> is an edge ledger that dispatches work queued before Odoo went down. New work
> cannot be added. Don't claim zero downtime; claim cached dispatch + degraded
> SLA."*

That is the correct answer to Q-19 and it corrects an overclaim in D-008, which
said *"kill the wall board and the facility still runs."* True for screens.
**Not true for Odoo itself** — and the distinction matters.

Two more honest calls worth keeping:
- **"Offline write conflicts resolve via business rules, not automation.
  Automatic resolution is a trap."** Conflicts go to a dead-letter queue and a
  human decides. Visible and intentional beats silent and arbitrary
- **"A foreign calendar is never imported. It's a capability you query on
  interval."** You cannot own a system you don't control

## ❌ One factual error to correct before it spreads

The agent claims **"Apple Watch Ultra has no built-in GPS, it requires iPhone
proximity."** **That is wrong** — the Ultra has built-in dual-frequency (L1+L5)
GPS and its own cellular radio; precision GPS is one of its headline features.

**But the candidate it blocks (H10, geo-distributed assignment) fails anyway** —
on D-009 grounds, because it tracks where *runners* are. **Right verdict, wrong
reason.** Worth recording because a wrong hardware fact will otherwise be reused
to justify a future decision.

## Carried forward
H1 foreign calendar as capability · **H2 edge ledger** · H3 idempotency keys ·
H4 consumption records as a PULL feed · H5 dead-letter queue · H6 capability
maturity ladder with runtime step-down · H7 facility admin by YAML, no admin UI.

## ⭐ H4 deserves special note

**Consumption records as an immutable feed that QuickBooks and Stripe PULL from,
rather than something Marshal pushes.** This is D-010's billing boundary,
independently arrived at and made concrete — and pull decouples Marshal from
every billing system's availability. If Stripe is down, records simply queue.
