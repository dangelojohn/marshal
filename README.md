# Marshal — `marshal.show`

**Dock and marshalling-yard scheduling for exposition venues. Canada first.**

Domain registered 2026-08-06. This folder is the project home.

---

## What Marshal is

A *marshalling yard* is where trucks stage before they are called to a dock.
Marshal schedules that — the trucks, the docks, the yard, and eventually the
whole move-in.

It exists because of one finding, **refined 2026-08-07 after a pass built
specifically to test it, not confirm it** (`02_market_research/12_exhibitor_facility_interaction_map.md`):
electrical, rigging, drayage and AV are locked to venue-appointed contractors —
but the dock isn't the *only* exhibitor-facility touchpoint that escapes those
contracts (fire-marshal inspection and venue-exclusive utility installers are
direct touchpoints too). **It's the only one of those touchpoints that is also
a recurring scarce-resource scheduling problem** — many trucks, few doors, a
hard time window, real cost to idling — rather than a one-time compliance gate
or a discrete labor task. That's the physical bottleneck everything else queues
behind, and it's why a real, funded, live competitor (Voyage Control, already
running Toronto/Vancouver/Calgary's flagship venues) exists specifically for
the dock and nowhere else on this list.

## Why it should work

| | |
|---|---|
| **Real gap** | Dock scheduling does not exist as a product anywhere in this market |
| **Proven category** | Opendock, C3, Transporeon sell exactly this — to warehouses |
| **They can't cross over** | Warehouse docks are steady-state; expo move-in is a 36–72h surge with precedence and spatial exclusion. Their solver produces impossible plans here |
| **One buyer** | The venue — dark time is unrecoverable, turnaround density is the GM's metric |
| **No cold start** | One venue alone gets value in its first show |
| **It compounds** | Dock actuals are the calibration data for prediction and the gap data for the network |
| **Fast proof** | ROI measurable inside one show cycle |

## Where to start reading

| Order | File | Why |
|---|---|---|
| 1 | `01_product/01_what_we_are_building.md` | **The thesis, the wedge, the name.** Start here |
| 2 | `00_decisions/DECISIONS.md` | What's settled and what's still open |
| 3 | `01_product/03_predictive_scheduling.md` | The scheduling engine and the demand model |
| 4 | `03_internal_assets/` | What we already own and can reuse |
| 5 | `02_market_research/INDEX.md` | **Live status of the competitive evidence** — which files are gap-closing-pass complete |

## Folder map

```
00_decisions/            decision log — the durable record of what was chosen
01_product/              what we're building (thesis → full spec → engine → network)
02_market_research/      8 competitor/category studies
03_internal_assets/      reusable code we already own, plus traps
04_research_archive/     method, sourcing limits, original study index
05_recovered_agent_reports/  raw reports recovered from agents that died mid-run
06_next_steps/           the open list
```

## Saving

This folder is a **git repository**, pushed to Forgejo on the QNAP.

```bash
./save.sh "what changed"      # commit, mirror, and push
git log --oneline             # see every save
```

| | |
|---|---|
| **Repo** | `john/marshal` |
| **Web** | https://southbrookcabinetry.space/git/john/marshal |
| **Clone** | `https://southbrookcabinetry.space/git/john/marshal.git` |
| **SSH** | `ssh://git@192.168.68.108:2223/john/marshal.git` |
| **Visibility** | **Public** — anonymous clone and read, no credentials needed |
| **Local mirror** | `~/Downloads/_backups/marshal-show-latest` |

Deliberately public so it's easy to reach on the internal network. Anonymous
**read** needs nothing; **push** still needs your Forgejo credential, which is
what keeps the history intact.

## Honest status

**Infrastructure is live.** Odoo 16 CE running on RainCloud (QNAP), `marshal_core`
module installed with 30 passing tests, implementing the chokepoint/buffer
contention model (D-014), an idempotency/dead-letter/custody-chain spine (Wave
0+1), and a live wall board. Full detail: `08_infrastructure/01_raincloud_odoo_install.md`.
**The product/market thesis is still gated by two phone calls** — see
`06_next_steps/OPEN_ITEMS.md`.

The sourcing limit that applied to the market research is documented in
`04_research_archive/research_method_and_limits.md` — the original vendor census
was compiled **without web search available**. **Re-run complete, 2026-08-07**:
all of `02_market_research/01`–`08` were gap-closed with real web search, plus
four new files (`09`–`12`) applying Jobs-To-Be-Done research to the GSC, the
venue, the exhibitor, and the direct exhibitor-facility interface — sourced
from job postings, union agreements, and exhibitor complaints rather than
vendor marketing. See `02_market_research/INDEX.md` for the full status and
headline findings per file. The single most consequential result: **Voyage
Control already runs dock scheduling at Toronto/Vancouver/Calgary's flagship
venues** — not greenfield — which is why this file's own thesis above is
stated more narrowly than the original version was.
