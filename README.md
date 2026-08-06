# Marshal — `marshal.show`

**Dock and marshalling-yard scheduling for exposition venues. Canada first.**

Domain registered 2026-08-06. This folder is the project home.

---

## What Marshal is

A *marshalling yard* is where trucks stage before they are called to a dock.
Marshal schedules that — the trucks, the docks, the yard, and eventually the
whole move-in.

It exists because of one finding: **the loading dock is the only part of an
exhibition floor that no service-exclusivity contract covers.** Electrical,
rigging, drayage and AV are all locked to venue-appointed contractors. The dock
belongs to the building. That is the one door left open, and it happens to sit
on the physical bottleneck everything else queues behind.

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
| 5 | `02_market_research/` | The competitive evidence behind all of it |

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

**Nothing is built.** This is research and a product decision. No code has been
written for Marshal, and no code in any existing repo has been modified.

The sourcing limit that applies to the market research is real and documented in
`04_research_archive/research_method_and_limits.md` — **the vendor census was
compiled without web search available**, so it is a strong starting list rather
than a complete one. The structural findings (the seam, the buffer gap,
exclusivity, the price floor) are well evidenced. **Re-run vendor discovery with
search enabled before any figure goes in front of an investor.**
