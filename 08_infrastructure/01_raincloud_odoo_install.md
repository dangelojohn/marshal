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

**RESOLVED, unprompted — checked 2026-08-06 evening.** QNAP's own
`QcloudSSLCertificate` QPKG (stock-installed, see host inventory) evidently
refreshed `/etc/ssl/certs` on its own schedule (file dates Jul 30 / Aug 4).
`curl -v https://github.com` now returns `SSL certificate verify ok`, issuer
Sectigo, exit 0. No action needed — leave this QPKG alone, it's doing its job.

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
| **1** | **Mirror CACHEDEV2** — add one of the five idle disks to md2. Single points of failure under a database are not acceptable once real work lands. **Must be done by the owner in the QTS web UI** (Storage & Snapshots) — not something to script blind |
| ~~2~~ | ~~Set `list_db = False`~~ **DONE.** Offsite/external access still needs a plan (reverse proxy+TLS, or a VPN overlay) — **network-layer decision, owner's call**, see below |
| ~~3~~ | ~~Copy backups off this box~~ **DONE**, see below |
| ~~4~~ | ~~Update `/etc/ssl/certs`~~ **Turned out already fine** — QcloudSSLCertificate keeps it current on its own, checked 2026-08-06 |
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

---

## Wave 0 + Wave 1 — what is now running

**`marshal_core` 16.0.1.2.0 · 30 tests passing · CI gate green · zero downtime.**

### Wave 0
| Piece | Why |
|---|---|
| **Idempotency keys** | Clients are a watch, a gloved phone and an SMS gateway on networks that drop. They must be able to retry *dumbly*. Client-supplied key, server-side dedup, and a loud log if the same key returns with a different payload — that is a client bug, not a retry |
| **Dead-letter queue** | Every refusal writes a coded entry with suggested actions. A blockage is visible and actionable rather than discovered when a truck is already waiting |
| **Fail-closed access** | Operators read all movements, **write only their own or unassigned**, never unlink |
| **CI gate** | `scripts/ci.sh` — static checks, then a real install+test against a scratch database |

### Wave 1 — the custody spine (R04)
Per-movement hash chain, **not one global chain**. A global chain serialises
every write behind one tail pointer and makes verifying one crate mean walking
every event ever recorded. Per-movement chains are independent and short:
*"prove this crate's history"* touches only that crate. Cross-chain integrity
comes from periodic **anchors** instead.

Verified on live data: `CHAIN INTACT | events=3` and an anchor over the chain
heads. Tests prove it **detects** tampering rather than merely storing history —
each bypasses the ORM guard with raw SQL, the way someone with database access
would: an edited payload is caught, a deleted middle event is caught, and
tampering with one movement's chain leaves another's intact.

> **What it is not:** this is not a blockchain and it will not stop an admin
> rewriting a chain wholesale. The anchor is what makes that expensive — and it
> is worth far more now that anchors leave the box with the nightly off-box
> backup.

### Two corrections found along the way

**`--no-http` means zero downtime.** I had been stopping production for every
install and test, and had written that into the skill as fact. Tested and
disproved: `-i --test-enable --no-http` against a scratch database coexists with
the live server. Both helper scripts corrected.

**QTS has no python3 at all**, so `lint.sh` borrows the odoo container's
interpreter over stdin rather than installing anything.

### The CI gate earned itself immediately

Its first real run caught a bug before it reached the live database: a
string-replace put the *Verify Custody Chain* button on `marshal.dlq` instead of
`marshal.movement`, which Odoo rejects at view-validation time. Static checks
alone would have passed it — it took the real install to catch.

---

## The wall board — live

**http://192.168.68.89:8069/marshal/board** (add `?demo=1` for hardcoded tiles,
no backend needed). `marshal_core 16.0.1.3.0`.

Verified from the LAN: board page **200**, demo mode **200**, state endpoint
returning 4 tiles with buffer occupancy, backend **200**.

**Served as a plain file, not through Odoo's asset pipeline.** The board is a
client of `POST /marshal/board/state` and nothing more, so it must stay servable
from a kiosk, a spare tablet, or another host entirely — bundling it would
quietly make the headless claim untrue.

### Design decisions worth keeping

- **Tiles never reorder.** Their position mirrors the physical yard the
  coordinator has memorised. Reflowing the grid every 3 seconds would break the
  mapping between screen and window, which is the one thing this board must
  never do. Exceptions are made loud *in place* instead
- **Status is carried by shape as well as colour** — circle / diamond /
  triangle — so it survives a colour-blind viewer and a sun-washed screen
- **Exception changes border width, not just colour**
- **The clock runs off the device**, never the poll, so it stays an honest
  reference when "updated" looks wrong
- **Snapshots via cache-busted `<img>`, not video.** No player to break, trivial
  reconnect, and enough to answer *"is door 4 clear?"*. A failed image falls back
  to a "no camera" tile that still shows schedule state
- **Staleness is stated in words** across the full width when the endpoint is
  unreachable. A frozen board that still looks live is dangerous
- **No animation anywhere.** A board that moves gets ignored

### ⚠ Correction: "zero downtime" applies to tests and data, not new Python

`--no-http` lets tests and `-u` run against a live server with no downtime, and
that still holds. **But a new controller or model needs a container restart** —
the running process holds the old Python in memory and `-u` never re-imports it.
The board returned 404 until `docker-compose restart odoo`, and the fix is not
obvious from the upgrade log, which exits 0.

**Deploy rule: data and view changes are hot; new Python is not.**

---

## Wave 2 — the runner API, live and verified (2026-08-08)

**`marshal_core` 16.0.1.4.0.** `controllers/runner.py` — the Apple-Watch-facing
REST surface — was committed to git 2026-08-06 (`89ddc37`) but never actually
deployed; the live instance was still running 16.0.1.3.0 with no `runner.py`
on the NAS at all. Deployed 2026-08-08: copied the controller + manifest +
`controllers/__init__.py`, `chown 101:101`, `-u` upgrade, container restart
(new Python needs one, per the deploy rule above), 30/30 tests still pass.

**End-to-end verified over real HTTP, not just "the upgrade log said 0":**
authenticated as admin against `/web/session/authenticate`, then called
`/marshal/runner/next` (returned well-formed JSON, `job: null` because no
claim is currently `held`/`occupied` in the seed data — a legitimate empty
state) and `/marshal/runner/arrived` with a bogus `claim_id` (clean
`{"ok": false, "error": "unknown_claim"}`, no 500, no idempotency record
written for a claim that never existed).

**Found and fixed a real bug while verifying:** `scripts/run-tests.sh`'s own
comment claimed `--no-http avoids the 8069 bind, so the live server stays
up` — but the actual `docker exec` command was missing the `--no-http` flag
entirely (unlike `install-module.sh`, which has it correctly). Running tests
crashed with `OSError: [Errno 98] Address already in use` because the test
run tried to bind 8069 against the already-running production container.
**The comment and the code had drifted apart** — exactly the kind of
NAS-local script that isn't in git and has no CI catching it. Fixed on the
box (`--no-http --max-cron-threads=0` added, matching `install-module.sh`'s
pattern); re-ran clean, 30 tests, 0.61s, exit=0. **This script lives only on
the NAS** (`scripts/` isn't tracked in the `john/marshal` git repo — it's
covered by the off-box backup puller instead), so this fix has no git commit
of its own; recorded here so it isn't silently lost or re-broken.

---

## Wave 3 — the customer-facing surfaces, live and proven end-to-end (2026-08-08)

**`marshal_core` 16.0.1.5.0.** Built the three pieces that turn the Wave 0-2
backend into something a real exhibitor, receiver, and runner can actually
use, not just an API a Python test calls:

| Surface | Route | What it does |
|---|---|---|
| Exhibitor declare | `GET /marshal/exhibitor/declare` | Public form — name, booth, carrier, driver phone, expected window |
| Exhibitor track | `GET /marshal/exhibitor/track/<token>` | Public status stepper (Declared → In transit → Arrived → Placed), no login — identity is an unguessable token, not a session |
| Receiver capture | `GET /marshal/receiver/app` (staff login) | Lists unclaimed planned movements, captures arrival = acquire + occupy the intake dock, optional photo |
| Runner app | `GET /marshal/runner/app` (staff login) | Mobile-web front end for the Wave 2 REST API — the two-tap contract as an actual page, not just a tested endpoint |
| Driver SMS | `marshal.sms.log` model + `POST /marshal/sms/inbound` | D-005 templates, keyword-only reply parsing (Y/N), Twilio webhook with signature verification |

**Proven end-to-end over real HTTP, twice, with a fresh movement the second
time** (`MV00382`): declare → receiver capture → runner deliver → exhibitor
tracker shows all four steps done with real timestamps, custody chain
intact. Not a demo script — the actual controllers, hit with curl the way a
browser would hit them.

### Honest boundaries — what this is not

- **No native watchOS app.** `runner_app.html` is the same two-tap contract
  served as a page any phone or watch browser can open — building and
  shipping an actual watchOS binary needs Xcode, an Apple Developer account,
  and provisioning this environment doesn't have. If a real watch app is
  wanted later, the REST API underneath (`/marshal/runner/*`) is already
  built and tested; only the native shell would be new work.
- **SMS ships safely OFF by default.** No Twilio account is configured on
  this box. Without one, `marshal.sms.log.send()` never pretends to send —
  it writes a `state='simulated'` log entry and logs at INFO what *would*
  have gone out, so the flow is fully testable without a real account and
  never silently no-ops. **To go live**, set three `ir.config_parameter`
  values (Settings → Technical → Parameters → System Parameters, or via
  shell): `marshal.sms_enabled` = `True`, `marshal.twilio_account_sid`,
  `marshal.twilio_auth_token`, `marshal.twilio_from_number` — then point the
  Twilio number's inbound webhook at
  `https://<public-host>/marshal/sms/inbound`. **The inbound webhook
  fails closed (403) with no auth token configured** — it will not accept
  or act on any inbound message until a real Twilio auth token is set,
  since without one there's no way to tell a genuine Twilio callback from
  anyone else's POST to a public URL.
- **No billing.** Stripe Connect and the 22%/18% dock-fee model (D-016) have
  zero code — a real payment processor account is needed before that's
  buildable, and none is configured.
- **Still runs against the fictional seed venue** (`DOCK1-3`, `AISLE-A`,
  `LIFT1`) — nothing here required or assumed a real venue's topology, but
  nothing here provides one either. Swapping in a real venue is a data
  change (`marshal.chokepoint`/`marshal.buffer` records), not a code change.

### Three real bugs the end-to-end proving pass caught (not just written, verified)

1. **`declare_submit` crashed on ISO 8601 datetimes** — the browser's
   `datetime-local` input sends `2026-08-08T14:00:00.000Z`; Odoo's Datetime
   fields need `%Y-%m-%d %H:%M:%S`. Fixed by parsing with `dateutil`
   (already an Odoo core dependency) and normalizing to UTC server-side, so
   the controller is robust to whatever ISO variant a client sends.
2. **`runner._transition` tried to log invalid event types.** `'arrived'`
   and `'delivered'` were never valid `marshal.event.event_type` values —
   this is a **Wave 2 bug**, not a Wave 3 one, and it survived the previous
   session's "verification" because that pass only exercised the
   unknown-claim error path, never a real successful transition. This
   session's first real end-to-end delivery caught it immediately.
   `action_occupy()`/`action_release()` already log valid `occupied`/
   `released` events and the movement's own `write()` override logs a
   `state` event — the trailing call was redundant as well as broken.
3. **Receiver's pending-list filter silently matched everything.**
   `claim_count` is a non-stored computed field with no `search()` defined;
   Odoo drops that domain leaf rather than erroring, so
   `[("claim_count", "=", 0)]` filtered nothing. Fixed to filter on the real
   relational field, `[("claim_ids", "=", False)]`. Caught by comparing the
   controller's actual output against what it should have returned, not by
   trusting that "no exception" meant "correct" — a search returning 200
   with the wrong rows is exactly the "something failing while reporting
   success" pattern worth staying suspicious of.

**45/45 tests pass** (`test_contention.py` + new `test_surfaces.py` — 12 new
tests: token generation/uniqueness, the SMS keyword parser including the
"yeah be there in 10" case the design doc itself flags as the hard one,
send-when-unconfigured is simulated not silent, Twilio signature
round-trips and rejects tampering, the `claim_ids` regression above).
