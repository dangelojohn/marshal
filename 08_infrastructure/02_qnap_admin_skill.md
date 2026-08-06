---
name: qnap-admin
description: Use when administering a QNAP NAS over SSH — running Docker/containers on one, surviving reboots, QTS filesystem and busybox quirks, storage arrays, or the QTS web API. Covers traps that silently waste hours.
---

# QNAP administration

> **Host inventory: `references/hosts.md`** — read it before touching any box.
> The QNAPs here are materially different from each other (one has Container
> Station and needs `system-docker`; the other has no Container Station at all
> and uses hand-installed Docker). Assuming the wrong one wastes time.

QTS is **not a normal Linux distro**. It is busybox on a heavily-customised
kernel, with a root filesystem that is **rebuilt from firmware on every boot**.
Almost every mistake below comes from assuming otherwise.

**Provenance:** the traps below were verified first-hand on a **TS-879 Pro
running QTS 4.3.6** (2026-08-06) while installing Docker and Odoo 16 from
scratch. The Container Station / `system-docker` behaviour is from operational
experience on a second, Celeron-based QNAP — its exact model and firmware are
recorded in `references/hosts.md` only where confirmed. Nothing here is copied
from vendor documentation.

## The filesystem contract — learn this first

| Path | Survives reboot? | Use for |
|---|---|---|
| `/share/CACHEDEV*_DATA/` | ✅ **Yes** | **Everything you install.** Binaries, data, configs, scripts |
| `/mnt/HDA_ROOT/.config/` | ✅ Yes (DOM) | `autorun.sh` only. Small, and it's flash |
| `/etc/config/` | ✅ Yes | `crontab`, QTS config files |
| `/etc`, `/usr`, `/bin`, `/var` | ❌ **NO — reset from firmware** | Nothing. Anything you put here is gone after a reboot |
| `/tmp` | ❌ No, and **tiny** | See the `/tmp` trap below |

> **The rule: if it must survive, it lives on `/share/CACHEDEV*_DATA`.**
> The only exception is the boot hook, which has to be on the DOM.

## Boot persistence

```sh
# /mnt/HDA_ROOT/.config/autorun.sh   — must be chmod +x
setcfg Misc "Run user defined processes during startup" TRUE
getcfg Misc "Run user defined processes during startup"   # verify: TRUE
```

**The flag is separate from the file.** A perfectly good `autorun.sh` silently
never runs if the flag is unset — this is the most common cause of "it worked
until I rebooted".

Always have `autorun.sh` **wait for the data volume** before doing anything; it
runs early and `/share/CACHEDEV2_DATA` may not be mounted yet:

```sh
i=0; while [ ! -d "$BASE" ] && [ $i -lt 60 ]; do sleep 5; i=$((i+1)); done
```

Make it **idempotent** — it should no-op safely if things are already running,
so you can dry-run it without a reboot.

## busybox traps

| Missing / different | Use instead |
|---|---|
| **`nohup`** — does not exist | **`setsid cmd < /dev/null >> log 2>&1 &`** |
| `base64` — often absent | Encode on your workstation and pass the string in |
| `timeout` / `gtimeout` | Not present. Use SSH `ConnectTimeout` and your own loops |
| **`df` wraps long device names onto their own line** | **Index awk from the end**: `$(NF-4)`=Size, `$(NF-3)`=Used, `$(NF-2)`=Avail, `$(NF-1)`=Use%, `$NF`=mount. Positional `$2`/`$3` silently give wrong answers |
| `psql` without `-d` | Defaults to a db named after the user, which usually doesn't exist. Always pass `-d` |

### `/tmp` is a ~64MB tmpfs

Staging a single download there fills it, and a full `/tmp` then breaks **bash
heredocs** with `cannot create temp file for here document` — a baffling error if
you don't know the cause. **Never stage downloads in `/tmp`.** Use the data
volume.

### There is no python3 on QTS

Not a small thing — it breaks any tooling that assumes a scripting language
is present. **Don't install one.** If a container is running, borrow its
interpreter with `docker exec -i <container> python3 - "$ARGS"` and feed the
script on stdin. Remember to translate host paths to the container's
bind-mount points.

### The CA bundle is ancient on older QTS

`curl` to some hosts works; **GitHub fails** with `unable to get local issuer
certificate`. Don't reach for `curl -k`. **Fetch on your workstation and `scp` it
over, then verify the sha256 matches on both ends.**

## Running Docker without Container Station

Container Station is a QPKG and is **not available for every model/firmware** —
on older x86 boxes running QTS 4.3.x it may simply not appear in the App Center.
Installing Docker directly is often better anyway: no QNAP wrapper, upgradeable
independently, fully under your control.

**Check the kernel can actually take it first:**

```sh
uname -r                                    # need 3.10+
ls /sys/fs/cgroup/                          # need memory, cpu, cpuacct, devices…
grep overlay /proc/filesystems              # need overlay
tune2fs -l /dev/mapper/cachedevN | grep -i "filesystem features" | tr ' ' '\n' | grep filetype
                                            # overlay2 needs ext4 d_type
which iptables && iptables -V
```

Then static binaries onto the data volume:

```sh
curl -sSL -o docker.tgz \
  https://download.docker.com/linux/static/stable/x86_64/docker-20.10.24.tgz
```

**Pick a conservative Docker version** for old kernels — 20.10.x is a safe
default on 4.x kernels. Launch with `--data-root` on the data volume:

```sh
setsid dockerd \
  --data-root=/share/CACHEDEV2_DATA/<proj>/docker/data \
  --exec-root=/var/run/<proj>-docker \
  --storage-driver=overlay2 \
  < /dev/null >> logs/dockerd.log 2>&1 &
```

**Put the data-root on a data volume, never the system volume** — images fill
space fast, and a full *system* volume can wedge QTS itself.

## Storage — reading the array

```sh
cat /proc/mdstat
# md2 : active raid1 sdg3[0]  1943559616 blocks super 1.0 [1/1] [U]
#                                                          ^^^^^
```

### `raid1` is a LEVEL, not a headcount

The level says *"mirror whatever members I have."* The **slot count** says how
many members there are. A one-member RAID 1 is a complete, healthy array that
mirrors nothing.

| `mdstat` | mdadm state | What it actually is |
|---|---|---|
| `[1/1] [U]` | `active` | **1 slot, 1 filled. NOT degraded — and NOT redundant.** A mirror with one leg |
| `[2/2] [UU]` | `clean` | A real two-disk mirror |
| `[8/7] [UUUUUU_U]` | `clean, degraded` | 8 slots, 7 filled — **genuinely missing a member** |

**`[1/1]` and `[2/1]` are completely different situations** and both contain a
"1". The first is by design; the second is a mirror that has lost a disk and
needs a rebuild now.

**Why QNAP builds single-disk volumes this way** — it is deliberate and
sensible: because the array already speaks RAID 1, a disk can be added later
with `--grow --raid-devices=2` and the existing data survives. Created as a plain
partition or RAID 0, adding redundancy later would mean destroying and
recreating the volume. **It is a mirror pre-wired for a second disk that was
never fitted.**

**The trap:** `raid1` in `mdstat` reads as "mirrored" to anyone skimming.
**The truth is in `[n/m]`, and `mdadm --detail` states it in words.** Always
check before trusting a volume with a database.

**Expect false-alarm "degraded" on QNAP system arrays.** Boxes with empty bays
show `[8/7]` on the small system mirrors (`md9`, `md13`) that span every bay —
mdadm cannot tell "bay never populated" from "disk died". Check whether the
missing slot corresponds to an empty bay before treating it as a fault.

## The QTS web API

Useful for scripting what the CLI won't do.

```sh
PW64=$(printf '%s' "$PASSWORD" | base64)   # encode OFF the NAS
curl -sk "http://127.0.0.1:8080/cgi-bin/authLogin.cgi?user=admin&pwd=$PW64"
# -> <authSid><![CDATA[xxxxxxxx]]></authSid>, and authPassed=1
```

The login response also reports `modelName`, `platform`, `platform_ex` and
firmware version — the quickest reliable way to identify exactly what you're on.
Pass the sid on every later call as `&sid=<sid>` (GET) or `sid` in the POST body.

**Other endpoints** — reverse-engineered from the maintained `python-qnapstats`
client (what Home Assistant uses). **Unofficial but real and current**; QNAP
publishes no CGI reference.

| Endpoint | Params | Gives you |
|---|---|---|
| `management/manaRequest.cgi` | `subfunc=sysinfo&sysHealth=1` | System health |
| `management/manaRequest.cgi` | `subfunc=sysinfo&hd=no&multicpu=1` | CPU/system info |
| **`disk/qsmart.cgi`** | `func=all_hd_data` | **SMART data for every disk** |
| `management/chartReq.cgi` | `chart_func=disk_usage&disk_select=all&include=all` | Volume usage |
| `sys/sysRequest.cgi` | `subfunc=firm_update` | Firmware update state |
| `devices/devRequest.cgi` (POST) | `func=getExternalDev` | External devices |

**`qsmart.cgi` is the one to remember** — `smartctl` is often absent or silent on
QTS, and this is the reliable way to get drive health.

## QPKG packaging (if you ever need to build one)

Build tooling is **QDK** (`github.com/qnap-dev/QDK`); the real manual is
`docs/QDK-Developer-Guide.md` in that repo, not the README.

- `qbuild --create-env MyQPKG` scaffolds; `qbuild` inside the dir compiles
- **`qpkg.cfg`** — `QPKG_NAME`, `QPKG_VER`, `QPKG_AUTHOR` required; `QPKG_REQUIRE`
  expresses dependencies (e.g. `container-station >= 2.0`)
- **`package_routines`** hooks, in call order: `pkg_init` → `pkg_check_requirement`
  → `pkg_pre_install` → `pkg_install` → `pkg_post_install`; removal is
  `PKG_PRE_REMOVE` → `PKG_MAIN_REMOVE` → `PKG_POST_REMOVE`
- **`SYS_*` at install time** — corroborates the filesystem contract above:
  `SYS_CONFIG_DIR=/etc/config`, `SYS_QPKG_CONFIG_FILE=/etc/config/qpkg.conf`
  ("the system-wide package registry"), `SYS_QPKG_INSTALL_PATH=$SYS_QPKG_BASE/.qpkg`
- **`CMD_*` fixed paths** (don't rely on `$PATH`): `/sbin/getcfg`, `/sbin/setcfg`,
  `/sbin/log_tool`, `/sbin/write_log`, `/usr/local/sbin/qsh`
- Files listed in `QPKG_CONFIG` are MD5-compared on upgrade; **locally modified
  ones are preserved as `.qdksave`**, unmodified ones silently replaced

## Entware — opkg for CLI tooling

An alternative to QPKGs when you just want CLI packages. Installs to **`/opt`**
universally, via a thin QPKG wrapper (App Center → *Install Manually*) that
auto-detects architecture.

- **Remove Optware/Qnapware first — they conflict**
- Non-admin users need `source /opt/etc/profile` to get it on `$PATH`
- `OneCDOnly/sherpa` layers a CLI package manager on top — **self-describes as
  beta, not for production**

## Container Station availability

**Docker requires QTS 4.2.6+** (LXD 4.5.3+, Kata 4.2+ and 64-bit x86 only).

**So the firmware version is rarely the blocker — the *model* is.** A TS-879 Pro
on 4.3.6 clears the version floor comfortably and still has no Container Station
available, because App Center gates per-model on CPU instruction set. **Check the
App Center for the specific model rather than reasoning from the QTS version.**
When it isn't available, install Docker directly (above) — often the better
outcome anyway.

## Odoo on QNAP — three specific traps

1. **Bind-mount UID.** The official `odoo` image runs as **101:101**. Host
   directories owned by `admin` cause
   `PermissionError: '/var/lib/odoo/filestore'` **midway through the base
   install**, not at startup. `chown -R 101:101` the data and addons dirs.
2. **`odoo shell`, `-i` and `-u` all bind port 8069** by default, so they fail
   with `Address already in use` against a running server. **The fix is
   `--no-http`, NOT stopping the service** — verified on a live box: an
   `-i --test-enable --no-http` run against a scratch database coexists happily
   with the running server, so CI needs **zero production downtime**. Add
   `--max-cron-threads=0` so the throwaway run doesn't fire crons.
3. **`ir_module_module does not exist` is a red herring.** It's the shutdown
   handler failing on an already-rolled-back transaction, and it *masks* the real
   error further down the traceback. **Always read the whole log**, never the
   tail.

## Verify from another host

`curl` to `127.0.0.1:<port>` on the NAS can return `000` even when the service is
perfectly healthy — a loopback/curl quirk. **Test published ports from a
different machine** before concluding anything is broken.

## 🔴 Storage — what is NOT known (do not improvise)

**There is no verified procedure here for converting a single-disk QNAP volume to
a real mirror.** A documentation sweep (2026-08-06) found nothing sourceable:
`wiki.qnap.com` is dead, `web.archive.org` is unfetchable, and the community
forum has migrated with no deep technical archive.

> **Do not improvise `mdadm` against a live QNAP volume from memory.** QNAP layers
> its own volume manager over md, and a wrong `--grow`/`--add` on a
> `[1/1]` array is a data-loss event, not a recoverable mistake.
>
> Do it through **Storage & Snapshots in the QTS web UI**, which understands the
> QNAP-specific layering, or confirm the procedure against current vendor
> documentation first. Capture `cat /proc/mdstat` and `mdadm --detail` before
> touching anything.

## Etiquette

- Rapid successive SSH sessions can trigger QTS brute-force protection and you'll
  get `Permission denied` on correct credentials. **Prefer fewer, longer
  sessions**; if you get locked out, wait rather than retry harder.
- QNAP SSH prints post-quantum warnings that pollute output — filter with
  `grep -v -i 'post-quantum\|openssh.com/pq\|store now'`.
