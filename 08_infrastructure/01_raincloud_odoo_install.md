# RainCloud — Odoo 16 CE install for marshal.show

**Built 2026-08-06.** Host: QNAP **RainCloud**, `192.168.68.89`.
Status: **LIVE and verified.**

---

## Access

| | |
|---|---|
| **Odoo** | **http://192.168.68.89:8069** |
| Login | `admin` / `MountainView1!` |
| Database | `marshal` |
| Master (DB manager) password | `MountainView1!` |
| Postgres | user `odoo` / `MountainView1!` — **not published to the host**, reachable only inside the compose network |
| SSH | `admin` / `Admin!SEG` |
| Longpolling | 8072 |

**Verified working:** `/web/login` returns HTTP 200 from the LAN, and a JSON-RPC
`authenticate` call returns uid 2, "Marshal Administrator", db `marshal`,
server 16.0-20250909, tz America/Toronto.

---

## The disk decision — CACHEDEV2, and why

**The question was disk 1 (system) or disk 2 (free). Answer: disk 2.**

| | CACHEDEV1_DATA | **CACHEDEV2_DATA ✅** |
|---|---|---|
| Device | md1 → sdf | md2 → sdg |
| Size | 1.8T, 16.3G used | 1.8T, **76M used** |
| Role | **QTS system volume** | empty |

**Five reasons, in order of weight:**

1. **Blast radius.** If Postgres or Docker images fill the volume, QTS keeps
   running. A full *system* volume can wedge the NAS itself — recovering a QNAP
   whose system volume is full is materially harder than clearing a data volume.
2. **I/O isolation.** QTS writes logs, thumbnails and index data to CACHEDEV1
   constantly. Postgres `fsync` on the same spindle would contend with it. sdf
   and sdg are **separate physical disks**, so the workloads don't fight.
3. **Backup and snapshot granularity.** A dedicated volume can be snapshotted,
   replicated or restored without touching QTS.
4. **It was empty** — no migration, no risk to existing data.
5. **Clean teardown.** Everything Marshal touches is under one path.

**Everything lives at `/share/CACHEDEV2_DATA/marshal/`.** Nothing was written to
the system volume except the boot hook (which has to live there).

---

## ⚠ Findings you should know about

### 1. Neither volume has redundancy — and five disks are idle

```
md1 : active raid1 sdf3[0]   1943559616 blocks  [1/1] [U]
md2 : active raid1 sdg3[0]   1943559616 blocks  [1/1] [U]
```

`[1/1]` means **one disk each — single points of failure.** They are declared
RAID1 but have no mirror.

Meanwhile **seven 1.86TB disks are physically present** (sda–sdg) and only two
carry data volumes. **Five drives are sitting idle.**

**All seven drives are healthy** — verified via the QTS SMART endpoint
(`disk/qsmart.cgi?func=all_hd_data`), WD Se enterprise units (WD2000F9YZ),
`Health: OK`, 36–38°C. Bay 8 is empty. **So five good drives are idle.**

> **Recommendation: mirror CACHEDEV2 before this instance holds anything you'd
> miss.** Right now a single drive failure loses the whole Odoo instance — and
> the nightly backup currently lives *on the volume it protects*, so it protects
> nothing against that failure.
>
> **⚠ Do it through Storage & Snapshots in the QTS web UI — not `mdadm`.**
> I originally wrote "add a disk to md2", which implies a manual `mdadm --add`.
> That was careless advice. **QNAP layers its own volume manager over md**, and a
> hand-run `--add`/`--grow` against a live `[1/1]` array is a data-loss event
> rather than a recoverable mistake. A documentation sweep found no authoritative
> procedure (QNAP's wiki is dead and archive.org is unreachable), so there is no
> verified CLI recipe to follow — which is exactly why this belongs in the UI
> that understands the layering.
>
> This remains the single most valuable improvement available on this box, and
> the hardware is already installed and healthy.

### 2. QTS 4.3.6 is an end-of-life branch

TS-879 Pro (2012, Sandy Bridge). Firmware builds still appear (this one is dated
2024-06-19) but the 4.3.x branch is legacy. **Container Station is not
installable** — it does not appear in the App Center for `X86_SANDYBRIDGE` on
this firmware, and only stock system QPKGs are present.

**Consequence: Docker was installed directly** (static binaries, 20.10.24) rather
than through QNAP's app framework. This is *better* for our purposes — fully
under our control, no QNAP wrapper to fight, upgradeable independently — but it
means the daemon is ours to maintain and the boot hook is ours to keep working.

### 3. The NAS's CA bundle is too old for modern TLS chains

`curl` to `download.docker.com` works. `curl` to **GitHub fails** with
`SSL certificate problem: unable to get local issuer certificate` — the 2012-era
CA bundle lacks the newer roots.

**Workaround used:** `docker-compose` was fetched on the Mac (where the chain
validates) and copied over, **with the sha256 verified identical on both ends**
(`eca30ae3…`) rather than disabling verification with `curl -k`.

**Anything else fetched from this NAS over HTTPS may hit the same wall.** Fetch
locally and copy, or update the bundle at `/etc/ssl/certs`.

### 4. `/tmp` is a 64MB tmpfs

Small enough that a single 64MB download filled it to 100%, which then broke
`bash` heredocs (`cannot create temp file for here document`). **Never stage
downloads in `/tmp` on this box** — use the data volume. Cleaned up; now at 1%.

---

## What is installed

```
/share/CACHEDEV2_DATA/marshal/
├── bin/            docker 20.10.24 (static), docker-compose v2.24.6
├── stack/          docker-compose.yml, .env (chmod 600)
├── config/         odoo.conf, postgresql.conf.append
├── addons/         custom modules   (owned 101:101)
├── odoo-data/      filestore        (owned 101:101)
├── pgdata/         PostgreSQL 14 data
├── backups/        nightly dumps + filestore + config
├── logs/           dockerd, init, backup, autorun
├── scripts/        dockerd-start · init-db · odoo-shell · backup · health
└── docker/data/    Docker data-root (images, containers, overlay2)
```

| Component | Version | Notes |
|---|---|---|
| Docker | 20.10.24 | Static binaries. Chosen deliberately over a newer release for kernel 4.2.8 compatibility |
| Docker Compose | v2.24.6 | sha256-verified |
| PostgreSQL | 14 | Not published to the host |
| Odoo | 16.0-20250909 | CE, official image |

**Kernel checks that made this viable:** kernel 4.2.8, all required cgroups
present **including `memory`**, `overlay` in `/proc/filesystems`, ext4 with
`filetype` (d_type) enabled for overlay2, `bridge`/`br_netfilter` loaded,
iptables 1.4.21.

---

## Configuration decisions

**Odoo** (`config/odoo.conf`) — deliberately conservative, because this box also
runs QTS and must not be starved:

- `workers = 2`, `max_cron_threads = 1` on 4 threads
- `limit_memory_soft/hard` 640MB/768MB per worker
- `dbfilter = ^marshal.*$` — pins the instance to its own database
- `gevent_port = 8072` (**not** `longpolling_port`, which Odoo 16 deprecates and
  warns about)
- **`list_db = False`** (set 2026-08-06). Verified functionally, not by eye:
  `POST /web/database/list` and RPC `db.list` both return **AccessDenied**, and
  the database name is not rendered in any page. Login unaffected.
  *Note: the login template still ships the database-manager markup inline, so
  grepping the HTML for "create database" gives a false positive — test the
  endpoints, not the page source.*

**PostgreSQL** — tuned for 15.5GB shared with QTS, verified in effect:

| Setting | Value |
|---|---|
| shared_buffers | 1GB |
| effective_cache_size | 4GB |
| work_mem | 32MB |
| maintenance_work_mem | 256MB |
| max_connections | 60 |
| TimeZone | America/Toronto |

**Postgres is not published to the host.** Nothing outside the compose network
needs it, and an exposed 5432 on a NAS is a standing risk. Reach it with
`docker exec marshal-db psql -U odoo -d marshal`.

---

## Operations

```sh
BASE=/share/CACHEDEV2_DATA/marshal

$BASE/scripts/health.sh                 # one-glance status
$BASE/scripts/backup.sh 14              # manual backup, 14-day retention
echo "print(env.user.name)" | $BASE/scripts/odoo-shell.sh
cd $BASE/stack && PATH=$BASE/bin:$PATH docker-compose restart odoo
```

**Nightly backup at 02:30** via `/etc/config/crontab` (persistent), 14-day
retention. First run verified: 1.1M dump + 656K filestore + 3.9K config.

> **An Odoo backup is two things and both are required: the database *and* the
> filestore.** A database restored without its filestore looks fine until
> someone opens a record with an attachment. The script always takes both.

**Boot persistence** — `/mnt/HDA_ROOT/.config/autorun.sh`, with
`Run user defined processes during startup = TRUE`. QTS resets `/etc` and `/var`
on boot, so the hook waits for the data volume, starts dockerd, waits for the
socket, then brings the stack up. **Dry-run tested** — it no-ops safely when
already running.

---

## Gotchas hit during the build — all now handled in scripts

Recorded because each cost real time and will recur.

| Symptom | Actual cause |
|---|---|
| `PermissionError: '/var/lib/odoo/filestore'` — init dies loading `res_lang_data.xml` | **Bind-mount UID mismatch.** The odoo image runs as **101:101**; the host dirs were `admin`. Fixed with `chown -R 101:101 odoo-data addons` |
| `ir_module_module does not exist` | **A red herring.** That's the shutdown handler failing on an already-rolled-back transaction — it *masks* the real error, which is further down the traceback. Always read the whole log |
| `OSError: [Errno 98] Address already in use` on `odoo shell` or a CLI init | Both **try to bind 8069**, which the running server holds. Use `--no-http` for shell; stop the service or use a one-off container for init |
| `nohup: command not found` | QNAP busybox has **no `nohup`**. Use `setsid` |
| `cannot create temp file for here document` | `/tmp` full (see finding 4) |
| Health script printed "1.8T used of 2.7G" | QNAP `df` **wraps long device names onto their own line**, shifting positional awk fields. Index from `NF` instead |
| `curl` to localhost:8069 returns `000` from the NAS | A QNAP loopback/curl quirk. **The service is fine** — verify from another host, which returns 200 |

---

## Recommended next steps

| Priority | Action |
|---|---|
| **1** | **Mirror CACHEDEV2** — add one of the five idle disks to md2. Single points of failure under a database are not acceptable once real work lands |
| ~~2~~ | ~~Set `list_db = False`~~ **DONE.** Still needs a reverse proxy with TLS before any access from outside the LAN |
| **3** | Copy backups **off this box** — a backup on the volume it protects is not a backup |
| 4 | Update `/etc/ssl/certs` so the NAS can fetch from modern HTTPS endpoints |
| 5 | Consider raising `workers` once real load is observed — 2 is deliberately cautious |

---

## `marshal_core` — installed and tested

**Deployed 2026-08-06. State `installed`. All 16 tests pass.**

```
marshal_core: 16 tests  0.37s  512 queries   exit=0, zero failures
```

Implements D-014 (chokepoint contention) on the live instance:

| Model | Purpose |
|---|---|
| `marshal.chokepoint` | Exclusive-occupancy resource — dock bay, elevator, aisle, staging |
| `marshal.buffer` | Finite holding area **between** chokepoints |
| `marshal.movement` | A crate's trip, as a chain of claims |
| `marshal.claim` | One claim on one chokepoint |
| `marshal.contention` | **Immutable** decision log — `write`/`unlink` raise |

**What the tests actually prove**, rather than merely exercise:

- **The blocking rule** — a full downstream buffer refuses entry, and the
  movement is stamped `delay_buffer_full`. A chokepoint with nothing downstream
  never blocks
- **The comparator**, rule by rule — hard deadline (1), blocking/safety (2),
  priority class (4), earliest due (5)
- **Rule 7 determinism** — two claims identical on every other axis still
  produce a decision, and the comparator is **antisymmetric** (`a beats b` ⇔
  `not b beats a`), so a draw is impossible. This is what makes the scheduler
  reproducible
- **Sequences are unique and monotonic** — rule 7 depends on it
- **Contention is logged with the deciding rule**, and the log **rejects writes
  and deletes**
- **Occupancy is never re-acquired** — claims are preemptible, occupancy is not
- **Ranks ascend along the flow** — deadlock-free ordered acquisition

All five models verified reachable over JSON-RPC as `admin`.

**Install/upgrade and test helpers** (both stop the server first, because `-i`,
`-u` and `shell` all bind 8069):

```sh
$BASE/scripts/install-module.sh marshal_core -i     # or -u to upgrade
$BASE/scripts/run-tests.sh marshal_core
```

---

## Seeded topology, and the blocking rule proven on live data

```
[DOCK1..3] ─(APRON cap 2)─ [AISLE-A] ─(LOBBY-L cap 4)─ [LIFT1] ─(LOBBY-U cap 4)─ [AISLE-C]
  rank 10-12                 rank 20                    rank 30                    rank 40
```

Ranks ascend along the flow, which is what makes acquisition deadlock-free.
`LIFT1` is flagged **`is_foreign`** — a hotel freight elevator is shared with
housekeeping and may be occupied on arrival by someone who never told us.

Re-runnable: `cat scripts/seed-venue.py | scripts/odoo-shell.sh`

**The blocking rule, exercised against the real topology** (apron capacity 2):

```
CRATE-1 -> DOCK1  acquire=True   apron=0/2  buffer_ok=True
CRATE-2 -> DOCK2  acquire=True   apron=1/2  buffer_ok=True
CRATE-3 -> DOCK3  acquire=False  apron=2/2  buffer_ok=False  variance=delay_buffer_full
```

Crates 1 and 2 clear the dock into the apron; at capacity the third is refused
and stamped. **Never occupy what you cannot clear.**

---

## Backups are now off-box

The nightly NAS backup wrote to CACHEDEV2 — **the same single-disk,
non-redundant volume it was protecting.** That guards against a bad upgrade or a
dropped database and against **nothing** if sdg dies.

| | |
|---|---|
| Puller | `~/Downloads/_backups/raincloud-offbox/pull-backups.sh` |
| Schedule | **03:15 daily** on the Mac via launchd (`com.marshal.offbox-backup`), 45 min after the NAS backup |
| Holds | backups + `config`, `stack`, `scripts`, `addons` |
| Retention | 30 days off-box, 14 on the NAS |

**Uses tar-over-ssh, not rsync** — the NAS ships busybox rsync, which rejects
GNU rsync's flags.

**Restore is verified, not assumed.** `scripts/verify-restore.sh` restores the
newest dump into a scratch database, checks it, and drops it:

```
restored OK: 222 tables, 30 modules installed, 6 chokepoints
```

A backup you have never restored is a hope, not a backup.

---

## Firmware — no update available, and I would not apply one yet

**Asked: update to the latest QNAP OS. Answer: there isn't one for this model.**

- The NAS's own authenticated update endpoint (`sysRequest.cgi?subfunc=firm_update`)
  returns **empty** version and build fields — QNAP's update service telling this
  device there is nothing newer
- Current build **20240619 (June 2024)** on the 4.3.6 branch, so QNAP was still
  patching this legacy track recently
- TS-879 Pro is a 2012 model; QTS 5.x requires newer hardware

*(`update.qnap.com/SoftwareRelease.xml` turned out to be a **client-application**
feed — Qfile/Qsync, note the `androidSDK`/`iOS` tags — not a firmware-per-model
feed, so its silence on TS-879 is not evidence either way.)*

**Even if an update appeared, the prerequisites were not met until now:**

1. **No redundancy** — both volumes are single-disk. A firmware update that goes
   wrong on a box with no mirror is unrecoverable
2. **No off-box backup** — now fixed, above. This was the real blocker
3. **A live service** with real data
4. **Our Docker install sits outside QNAP's app framework.** Data on CACHEDEV2
   and `autorun.sh` on the DOM both persist — but a firmware update can reset the
   **`Run user defined processes during startup` flag**, which would leave the
   stack down after reboot with no obvious cause

**If an update does appear, the order is:** off-box backup (done) → verify
restore (done) → mirror CACHEDEV2 → snapshot the autorun flag → update →
re-check the flag and `scripts/health.sh`.
