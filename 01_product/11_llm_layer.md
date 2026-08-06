# An LLM in front of Marshal — where it earns its place, and where it must never go

**Question (owner, 2026-08-06):** *"We can also consider placing an LLM model in
front of this system if you believe it would provide the deep support?"*

**Yes — but at the edges, never at the core.** The distinction is not stylistic.
Put it in the wrong place and it destroys the two things the whole business case
rests on: a defensible safety record, and billing anyone will pay.

> **LLM at the edges: language in, language out.
> Deterministic core: decisions, safety, money.**

---

## 1. Where an LLM must never go

Being explicit first, because this list is what makes the rest safe.

| Never | Why |
|---|---|
| **Producing the schedule** | A plan that can't be reproduced can't be defended to a show manager at 6am. *"The model said so"* is not an answer anyone on a floor accepts (`spec/03` §5) |
| **Safety rules** | Certification checks, aisle exclusion, indoor-equipment restrictions. A system that *occasionally* permits an uncertified operator is worse than none |
| **Metering and billing** | Revenue records must be exact and auditable. This is the strongest part of the case (D-005 §2) and it dies the moment a number is generated rather than measured |
| **Anything on a movement's critical path** | Latency and non-determinism at 6am on a dock is a failure mode, not a feature |
| **Writing state directly** | It proposes. The core decides, and **re-derives identity from ground truth rather than trusting the proposal** |

**The never-invocable list is a first-class artifact**, checked in and tested —
not a convention. Southbrook's `PLM_LIFECYCLE` sentinel is the technique:
identity compared with `is`, never a context flag, because **a caller must never
be able to assert its own privilege.**

---

## 2. Where it genuinely earns its place

### ⭐ Making sense of what drivers actually text back — the strongest case

SMS is the vendor surface (D-005 §4). Drivers don't send structured data:

> *"stuck on the 401 maybe 40 min"*
> *"im at the wrong door theres no one here"*
> *"which gate do i use for hall c"*
> *"cant get in, guy says im not on the list"*

Regex is bad at this and always will be. **An LLM turning free text into a
structured intent is exactly the right tool**, and it is naturally bounded:

```
   inbound SMS  →  LLM  →  {intent: DELAY, eta_minutes: 40, confidence: 0.9}
                            │
                            └─→  deterministic core re-slots, or asks a human
```

The LLM never decides anything. It converts language into a proposal; the core
validates and acts. Low confidence, or an intent that would move something
expensive, routes to a person.

### ⭐ Bilingual operation — a compliance burden turned into a feature

Bill 96 makes French availability a legal requirement for Quebec venues (Q-10),
and dock crews frequently aren't first-language English regardless.

**Two-way SMS translation is a strong, concrete, low-risk win** — a driver texts
in French or Punjabi, the coordinator reads English, the reply goes back
translated. This is the single most legible piece of value an LLM adds here, and
it materially widens the addressable market.

### ⭐ Explaining the plan

When the scheduler re-sequences, someone needs to know why:

> *"Dock 4 moved to 15:10 — forklift 3 is on charge until 14:50 and it's the only
> unit rated for that crate."*

The **facts** come from the solver. The LLM only renders them as a sentence.
Read-only, and it directly serves ease of use (D-006) — nobody has to read a
constraint graph.

### ⭐ Asking the system questions

*"Where's the Henderson freight?"* · *"What's running late?"* · *"Why is dock 2
idle?"*

Natural language over current state, read-only. This is what makes a headless
system approachable **without building screens for every question** — which is
precisely the point of headless (D-008).

### Structuring checkpoint free-text

An operator types *"left front tire low, hydraulic weep at the mast."* The LLM
extracts condition flags and drafts a maintenance request; the human confirms.
**Human wrote it, LLM structured it, human confirmed it** — the LLM never
originates a claim about the physical world.

### Incident reconstruction

Assembling movement records, camera stills and checkpoint results into a readable
timeline after an event. Serves D-005's defensible record directly.

**Critical framing: the record is the evidence. The narrative is a convenience.**
Anything that leaves the building must cite the underlying records, and a human
must sign it.

---

## 3. We already own this architecture — three times

This is not a novel pattern for us. It has been arrived at independently in three
of our own codebases, which is about as strong an internal signal as exists:

| Asset | The pattern |
|---|---|
| **`porterly-future-reference`** | Agents propose, **core decides and re-derives identity from ground truth**. 74 invariant tests. **Read this before writing any of it** |
| **Southbrook `PLM_LIFECYCLE`** | Object-identity sentinel — JSON-RPC can forge a context flag but cannot forge Python identity |
| **`hermes-console`** | **Literally this architecture, running today**: agent loops → structured recommendations → local SQLite → `queue → approve → apply` → push through a bridge adapter. Multi-provider LLM client, MCP tool server, approve-gate on every write tool |

**hermes-console is close enough to be the starting point rather than a
reference.** Its `tenant_bridges/` shape — one small adapter per target system —
is exactly right for "watch the floor, raise attention items, draft driver
comms."

---

## 4. The constraint that decides the design: it must be optional at runtime

Marshal is **infrastructure** (D-008), possibly on-premises (Q-18), and **a dock
cannot stop because a WAN link did** (Q-19).

> **If the model is unreachable, the dock keeps running.**

That single rule forces the right architecture:

| Capability | LLM available | LLM unreachable |
|---|---|---|
| Scheduling | unchanged | **unchanged — it never used it** |
| Safety rules | unchanged | **unchanged** |
| Metering | unchanged | **unchanged** |
| SMS intent | parsed richly | **keyword fallback** (`DELAY`, `HERE`, `Y`, `N`) + route to a human |
| Translation | automatic | canned bilingual templates |
| Explanations | prose | the structured facts, unrendered |
| Q&A | natural language | the board still shows everything |

**Every LLM feature degrades to something that still works.** That is what makes
it an enhancement rather than a dependency — and it's why the answer to *"should
we put an LLM in front"* is yes without it becoming a single point of failure.

⚠ **Precedent worth heeding: AEMI's AI layer was found dead in production
because no API key was configured, and nothing noticed.** *"Deployed" is not
"working."* Marshal needs a health check on the model path and a visible
degraded-mode indicator, or it will silently fall back and nobody will know.

---

## 5. Practical shape

- **Provider-agnostic client.** hermes-console already has one (OpenAI-compatible
  + native Anthropic + a harness slot). Never hard-code a vendor
- **A small local model is plausible for SMS intent** — classification into a
  handful of intents plus an ETA is not a frontier task, and running it on
  facility hardware removes the connectivity dependency for the one edge feature
  that's on a live path
- **Frontier model for the low-frequency, high-value work** — incident
  narratives, ops Q&A, exception explanation. Cloud is fine; none of it is on a
  critical path
- **Every LLM call logged with its input, output and confidence.** Same
  discipline as the movement ledger. If it proposed something, that proposal is
  part of the record
- **Confidence thresholds route to humans.** Uncertainty is a routing signal, not
  something to paper over

---

## 6. Verdict

**Yes — as a language layer, not a decision layer.**

It makes a headless system approachable without building a screen for every
question, it turns messy driver texts into structured intent, and it makes
bilingual operation a feature rather than a compliance cost. All of that is real
and worth doing.

**But the moment it schedules, enforces a safety rule, or touches a billing
record, Marshal stops being defensible** — and defensibility is the product.

`[ASSUMPTION]` Phase 1 needs **only** SMS intent parsing and translation.
Explanations and Q&A are Phase 2, once there's a schedule worth explaining.

## New open questions

| # | Question | Why |
|---|---|---|
| **Q-26** | Local model on facility hardware, or cloud with graceful degradation? | Follows Q-18/Q-19. Only genuinely matters for SMS intent, the one edge feature on a live path |
| Q-27 | Does any venue's IT policy prohibit sending operational text to a third-party model? | Hotel and enterprise IT often does. Decides whether local is mandatory rather than preferred |
