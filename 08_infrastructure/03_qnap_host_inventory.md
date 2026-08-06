# QNAP host inventory

Load this when working on any of these boxes. **They are materially different
from each other** — the firmware branch decides what's possible, and assuming
the wrong one wastes time.

**Credentials are NOT here.** They live in the memory directory
(`qnap_*` entries). This file is the technical profile.

---

## RainCloud — `192.168.68.89`

| | |
|---|---|
| Model | **TS-879 Pro** (8-bay, 2012) |
| Platform | `TS-NASX86` / `X86_SANDYBRIDGE` |
| Firmware | **QTS 4.3.6** build 20240619 — legacy branch |
| CPU / RAM | Intel i3-2120, 2c/4t @3.3GHz · **15.9 GB** |
| Kernel | 4.2.8 |
| Volumes | CACHEDEV1 (sdf, system) · **CACHEDEV2 (sdg, Marshal)** — both 1.8T |
| SSH user | `admin` |

**Runs:** Odoo 16 CE for **marshal.show** on `:8069`, Postgres 14, under
hand-installed Docker at `/share/CACHEDEV2_DATA/marshal`.

### What's specific to this box

- ❌ **No Container Station** — unavailable for this platform on 4.3.6. Only
  stock QPKGs (netmgr, helpdesk, ResourceMonitor, Qboost, NotificationCenter,
  SSDLaboratory, LicenseCenter, QcloudSSLCertificate, MalwareRemover)
- ✅ **Docker 20.10.24 static binaries** at
  `/share/CACHEDEV2_DATA/marshal/bin/` — plain `docker`, **not** system-docker
- ⚠️ **CA bundle too old for GitHub** — fetch on the workstation, `scp` over,
  verify sha256
- ⚠️ **`/tmp` is 64MB** — never stage downloads there
- 🔴 **No redundancy.** `md1` and `md2` are both `[1/1]` — single disks despite
  showing as raid1. **Five 1.86TB disks (sda–sde) sit idle** and could mirror
  them
- Boot hook: `/mnt/HDA_ROOT/.config/autorun.sh`, flag `Misc / Run user defined
  processes during startup = TRUE`

### Operations

```sh
BASE=/share/CACHEDEV2_DATA/marshal
$BASE/scripts/health.sh                  # status at a glance
$BASE/scripts/backup.sh 14               # db + filestore + config
echo "print(env.user.name)" | $BASE/scripts/odoo-shell.sh
cd $BASE/stack && PATH=$BASE/bin:$PATH docker-compose ps
```
Nightly backup 02:30 via `/etc/config/crontab`.

---

## The Southbrook/Forgejo QNAP — `192.168.68.108`

SSH alias **`qnap-tunnel`** (via cloudflared, `ssh.southbrookcabinetry.space`).

| | |
|---|---|
| CPU | Celeron J1800 — **weak**, and often saturated |
| Container runtime | **Container Station**, and it runs **TWO docker daemons** |

### The critical difference from RainCloud

**Use `system-docker`, not `docker`.** The Container Station default socket does
**not** see the main application stacks:

```sh
SD=/share/CACHEDEV3_DATA/.qpkg/container-station/bin/system-docker
ssh qnap-tunnel "$SD ps"
ssh qnap-tunnel "$SD exec forgejo git --git-dir=/data/git/repositories/<org>/<repo>.git log --oneline -5"
```

**Runs:** Forgejo (git, port 9080/9443 + SSH 2223), Odoo stacks, Caddy,
cloudflared. Storage root is **CACHEDEV3**, not CACHEDEV2.

### Known hazards on this box
Resource saturation · Postgres recovery hazard · Caddyfile bind-mount inode trap ·
cron docker-exec PATH trap · HTTP 413 on large git pushes through Caddy (**push
over SSH `:2223` instead**). See the `qnap_*` memory entries.

---

## Telling them apart quickly

```sh
# identity, platform and firmware in one call
PW64=$(printf '%s' "$PASSWORD" | base64)     # encode OFF the NAS
curl -sk "http://127.0.0.1:8080/cgi-bin/authLogin.cgi?user=admin&pwd=$PW64"
# -> modelName, platform, platform_ex, firmware version, hostname
```

Or simply: `hostname` → `RainCloud` vs the Southbrook box; and
`ls /share/` → CACHEDEV**2** (RainCloud) vs CACHEDEV**3** (Southbrook).
