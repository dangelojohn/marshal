#!/usr/bin/env python3
"""Marshal — Reolink motion probe.

Answers Q-11: *is Reolink motion detection reliable enough at dock distance and
in dock lighting to be used as automatic actuals capture?*

Polls ``GetMdState`` on one or more Reolink cameras and appends every reading to
a JSONL log. Optionally saves periodic snapshots so the lighting and framing can
be judged after the fact.

**Standard library only.** No pip install, no virtualenv — copy this file to any
machine with Python 3.8+ and run it.

Protocol replicated from the verified working client at
``~/hermes-console/api/mcp/clients/reolink.py``:

    POST {scheme}://{ip}:{port}/cgi-bin/api.cgi
    Login  -> [{"cmd":"Login","action":0,"param":{"User":{...}}}]
              token at data[0].value.Token.name
    Cmd    -> same URL + "?token=<tok>", body [{"cmd":C,"action":0,"param":P}]
              error when data[0].code != 0; re-login on "please login first"
    Motion -> GetMdState {"channel": N}  -> value.state is truthy
    Snap   -> ?cmd=Snap&channel=N&rs=marshal&token=<tok>

Usage
-----
    ./reolink_motion_probe.py --check              # connectivity + device info
    ./reolink_motion_probe.py                      # poll until Ctrl-C
    ./reolink_motion_probe.py --hours 24 --snapshot-every 300

Config: ``cameras.json`` next to this script (see cameras.example.json).
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG = HERE / "cameras.json"
DEFAULT_OUT = HERE / "motion_log"

# Cameras serve self-signed certs on :443 — the working client sets verify=False
# for exactly this reason. These are LAN devices on a trusted network.
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

_running = True


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _stop(signum, frame):  # noqa: ARG001
    global _running
    _running = False
    print("\n· stopping after the current poll…", file=sys.stderr)


class ReolinkError(RuntimeError):
    pass


class Camera:
    """One camera. Holds the auth token and re-logins when it expires."""

    def __init__(self, cfg: dict) -> None:
        self.name = cfg["name"]
        self.ip = cfg["ip"]
        self.user = cfg["user"]
        self.password = cfg["password"]
        self.port = int(cfg.get("port", 80))
        self.scheme = cfg.get("scheme", "http")
        self.channels = cfg.get("channels", [0])
        self.label = cfg.get("label", self.name)  # e.g. "Dock 4"
        self._token = None

    @property
    def _base(self) -> str:
        return f"{self.scheme}://{self.ip}:{self.port}/cgi-bin/api.cgi"

    def _post(self, url: str, body: list, timeout: float = 8.0):
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as r:
                if r.status != 200:
                    raise ReolinkError(f"{self.name}: http {r.status}")
                return json.loads(r.read().decode())
        except urllib.error.URLError as exc:
            raise ReolinkError(f"{self.name}: transport ({exc.__class__.__name__})") from exc
        except ValueError as exc:
            raise ReolinkError(f"{self.name}: non-json response") from exc

    def _login(self) -> None:
        body = [{
            "cmd": "Login", "action": 0,
            "param": {"User": {
                "userName": self.user,
                "password": self.password,
                "Version": "0",
            }},
        }]
        data = self._post(self._base, body)
        if not isinstance(data, list) or not data:
            raise ReolinkError(f"{self.name}: login unexpected shape")
        first = data[0]
        if first.get("code") != 0:
            raise ReolinkError(f"{self.name}: login code={first.get('code')}")
        token = ((first.get("value") or {}).get("Token") or {}).get("name")
        if not token:
            raise ReolinkError(f"{self.name}: login returned no token")
        self._token = token

    def cmd(self, cmd: str, param: dict | None = None, _retry: bool = True):
        if self._token is None:
            self._login()
        body = [{"cmd": cmd, "action": 0, "param": param or {}}]
        data = self._post(f"{self._base}?token={self._token}", body)
        if not isinstance(data, list) or not data:
            raise ReolinkError(f"{self.name}: {cmd} unexpected shape")
        first = data[0]
        if first.get("code") != 0:
            detail = str((first.get("error") or {}).get("detail", "")).lower()
            if _retry and "login first" in detail:
                self._token = None
                return self.cmd(cmd, param, _retry=False)
            raise ReolinkError(f"{self.name}: {cmd} code={first.get('code')}")
        return first.get("value")

    def dev_info(self) -> dict:
        d = (self.cmd("GetDevInfo") or {}).get("DevInfo", {})
        return {
            "model": d.get("model"),
            "firmware": d.get("firmVer"),
            "channels": d.get("channelNum"),
            "name": d.get("name"),
        }

    def motion(self, channel: int = 0) -> bool:
        return bool((self.cmd("GetMdState", {"channel": channel}) or {}).get("state"))

    def snapshot(self, channel: int, dest: Path) -> None:
        if self._token is None:
            self._login()
        url = (f"{self.scheme}://{self.ip}:{self.port}/cgi-bin/api.cgi"
               f"?cmd=Snap&channel={channel}&rs=marshal&token={self._token}")
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15, context=_SSL_CTX) as r:
            dest.write_bytes(r.read())


def load_cameras(path: Path) -> list[Camera]:
    if not path.exists():
        sys.exit(
            f"No config at {path}\n"
            f"Copy cameras.example.json to cameras.json and fill it in.\n"
            f"(cameras.json is gitignored — it holds passwords.)"
        )
    cfg = json.loads(path.read_text())
    cams = [Camera(c) for c in cfg["cameras"]]
    if not cams:
        sys.exit("Config contains no cameras.")
    return cams


def check(cams: list[Camera]) -> int:
    """Connectivity test. Prints device info and one motion reading each."""
    bad = 0
    for c in cams:
        try:
            info = c.dev_info()
            states = {ch: c.motion(ch) for ch in c.channels}
            print(f"✅ {c.label:<16} {c.ip:<15} {info.get('model')} "
                  f"fw={info.get('firmware')} channels={info.get('channels')}")
            print(f"   motion now: {states}")
        except ReolinkError as exc:
            bad += 1
            print(f"❌ {c.label:<16} {c.ip:<15} {exc}")
    return 1 if bad else 0


def run(cams: list[Camera], out_dir: Path, interval: float,
        hours: float | None, snapshot_every: int | None) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = out_dir / f"motion-{stamp}.jsonl"
    snap_dir = out_dir / f"snapshots-{stamp}"
    if snapshot_every:
        snap_dir.mkdir(exist_ok=True)

    deadline = time.time() + hours * 3600 if hours else None
    print(f"logging → {log_path}")
    if snapshot_every:
        print(f"snapshots → {snap_dir} (every {snapshot_every}s)")
    print(f"interval {interval}s · {len(cams)} camera(s) · Ctrl-C to stop\n")

    polls = 0
    last_snap = 0.0
    with log_path.open("a") as log:
        while _running and (deadline is None or time.time() < deadline):
            cycle_start = time.time()
            for cam in cams:
                for ch in cam.channels:
                    rec = {"ts": _now(), "camera": cam.name,
                           "label": cam.label, "channel": ch}
                    try:
                        rec["motion"] = cam.motion(ch)
                        rec["ok"] = True
                    except ReolinkError as exc:
                        rec["ok"] = False
                        rec["error"] = str(exc)
                    log.write(json.dumps(rec) + "\n")
            log.flush()
            polls += 1

            if snapshot_every and cycle_start - last_snap >= snapshot_every:
                last_snap = cycle_start
                ts = datetime.now().strftime("%H%M%S")
                for cam in cams:
                    for ch in cam.channels:
                        try:
                            cam.snapshot(ch, snap_dir / f"{cam.name}-ch{ch}-{ts}.jpg")
                        except Exception as exc:  # noqa: BLE001 — never kill the run
                            print(f"  snapshot failed {cam.label}: {exc}", file=sys.stderr)

            if polls % 20 == 0:
                print(f"  {_now()}  {polls} polls")

            elapsed = time.time() - cycle_start
            time.sleep(max(0.0, interval - elapsed))

    print(f"\ndone — {polls} polls → {log_path}")
    print(f"analyse with:  ./analyze_motion_log.py {log_path}")


def main() -> int:
    p = argparse.ArgumentParser(description="Marshal Reolink motion probe (Q-11)")
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--interval", type=float, default=5.0,
                   help="seconds between polls (default 5)")
    p.add_argument("--hours", type=float, default=None,
                   help="stop after N hours (default: run until Ctrl-C)")
    p.add_argument("--snapshot-every", type=int, default=None, metavar="SEC",
                   help="also save a snapshot every SEC seconds")
    p.add_argument("--check", action="store_true",
                   help="connectivity test only, then exit")
    args = p.parse_args()

    cams = load_cameras(args.config)
    if args.check:
        return check(cams)

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)
    run(cams, args.out, args.interval, args.hours, args.snapshot_every)
    return 0


if __name__ == "__main__":
    sys.exit(main())
