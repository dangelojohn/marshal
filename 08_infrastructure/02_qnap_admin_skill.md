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

## Storage

```sh
cat /proc/mdstat
# md2 : active raid1 sdg3[0]  1943559616 blocks super 1.0 [1/1] [U]
#                                                          ^^^^^
```

**`[1/1]` means ONE disk.** QNAP presents single-disk volumes as `raid1` with no
mirror — they look redundant in `mdstat` and are not. **Always check the
`[n/m]` count before trusting a volume with a database.** Compare
`ls /dev/sd?` against the arrays: idle disks are common.

## The QTS web API

Useful for scripting what the CLI won't do:

```sh
PW64=$(printf '%s' "$PASSWORD" | base64)   # encode OFF the NAS
curl -sk "http://127.0.0.1:8080/cgi-bin/authLogin.cgi?user=admin&pwd=$PW64"
# -> <authSid><![CDATA[xxxxxxxx]]></authSid>, and authPassed=1
```

The login response also reports `modelName`, `platform`, `platform_ex` and
firmware version — the quickest reliable way to identify exactly what you're on.

## Odoo on QNAP — three specific traps

1. **Bind-mount UID.** The official `odoo` image runs as **101:101**. Host
   directories owned by `admin` cause
   `PermissionError: '/var/lib/odoo/filestore'` **midway through the base
   install**, not at startup. `chown -R 101:101` the data and addons dirs.
2. **`odoo shell` and CLI `-i` both bind port 8069**, so they fail with
   `Address already in use` against a running server. Use `--no-http` for shell;
   stop the service or use a one-off container for installs.
3. **`ir_module_module does not exist` is a red herring.** It's the shutdown
   handler failing on an already-rolled-back transaction, and it *masks* the real
   error further down the traceback. **Always read the whole log**, never the
   tail.

## Verify from another host

`curl` to `127.0.0.1:<port>` on the NAS can return `000` even when the service is
perfectly healthy — a loopback/curl quirk. **Test published ports from a
different machine** before concluding anything is broken.

## Etiquette

- Rapid successive SSH sessions can trigger QTS brute-force protection and you'll
  get `Permission denied` on correct credentials. **Prefer fewer, longer
  sessions**; if you get locked out, wait rather than retry harder.
- QNAP SSH prints post-quantum warnings that pollute output — filter with
  `grep -v -i 'post-quantum\|openssh.com/pq\|store now'`.
