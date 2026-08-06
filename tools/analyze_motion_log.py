#!/usr/bin/env python3
"""Marshal — motion log analysis.

Turns a ``reolink_motion_probe.py`` JSONL log into the numbers that answer Q-11.

Two phases, because the first needs no schedule and can run the moment you have
a camera pointed at anything:

**Phase A — discrimination (no schedule required)**
    Is the signal capable of telling busy from quiet at all?
    - duty cycle: too high and everything looks busy; too low and it sees nothing
    - event count and duration: twitchy 1-poll blips vs usable sustained runs
    - quiet-hours behaviour: motion at 03:00 is the natural negative control
    - poll reliability: a signal you can't read isn't a signal

**Phase B — accuracy (needs a schedule CSV)**
    Does motion line up with movements that actually happened?
    - detection rate: scheduled movements that produced motion
    - unexplained motion: motion outside every window
    - latency: window start → first motion

Schedule CSV format (header required):
    label,start,end,description
    Dock 4,2026-09-14T08:00:00,2026-09-14T08:30:00,crate to booth 412

``label`` matches the camera ``label`` in cameras.json. Times are ISO 8601;
naive times are treated as UTC.

Standard library only.

Usage
-----
    ./analyze_motion_log.py motion_log/motion-20260914-060000.jsonl
    ./analyze_motion_log.py motion-*.jsonl --schedule schedule.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

QUIET_HOURS = range(1, 5)  # 01:00–04:59 local-ish, used as a negative control


def parse_ts(s: str) -> datetime:
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt


def load(paths: list[Path]) -> dict[tuple[str, int], list[dict]]:
    """Group readings by (label, channel), sorted by time."""
    series: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for p in paths:
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            r["_ts"] = parse_ts(r["ts"])
            series[(r.get("label") or r["camera"], r.get("channel", 0))].append(r)
    for k in series:
        series[k].sort(key=lambda r: r["_ts"])
    return series


def runs(readings: list[dict]) -> list[tuple[datetime, datetime, int]]:
    """Contiguous motion=True stretches → (start, end, poll_count)."""
    out, start, prev, n = [], None, None, 0
    for r in readings:
        if not r.get("ok"):
            continue
        if r.get("motion"):
            if start is None:
                start, n = r["_ts"], 0
            n += 1
            prev = r["_ts"]
        elif start is not None:
            out.append((start, prev, n))
            start = None
    if start is not None:
        out.append((start, prev, n))
    return out


def phase_a(series: dict) -> None:
    print("=" * 72)
    print("PHASE A — can the signal discriminate at all?  (no schedule needed)")
    print("=" * 72)

    for (label, ch), readings in sorted(series.items()):
        ok = [r for r in readings if r.get("ok")]
        errs = len(readings) - len(ok)
        if not ok:
            print(f"\n{label} ch{ch}: no successful readings ({errs} errors)")
            continue

        span_h = (ok[-1]["_ts"] - ok[0]["_ts"]).total_seconds() / 3600
        motion_n = sum(1 for r in ok if r.get("motion"))
        duty = motion_n / len(ok) * 100
        ev = runs(ok)

        print(f"\n{label}  ch{ch}")
        print(f"  window        {ok[0]['_ts']:%Y-%m-%d %H:%M} → "
              f"{ok[-1]['_ts']:%H:%M}  ({span_h:.1f} h)")
        print(f"  polls         {len(ok)} ok, {errs} failed "
              f"({errs / max(1, len(readings)) * 100:.1f}% loss)")
        print(f"  duty cycle    {duty:.1f}%  ({motion_n} of {len(ok)} polls saw motion)")
        print(f"  events        {len(ev)}  ({len(ev) / max(span_h, 0.01):.1f}/hour)")

        if ev:
            durs = [(e - s).total_seconds() for s, e, _ in ev]
            print(f"  event length  median {statistics.median(durs):.0f}s  "
                  f"max {max(durs):.0f}s")
            single = sum(1 for _, _, n in ev if n == 1)
            print(f"  single-poll   {single} of {len(ev)} "
                  f"({single / len(ev) * 100:.0f}%)")

        # Negative control: motion when nothing should be happening.
        quiet = [r for r in ok if r["_ts"].hour in QUIET_HOURS]
        if quiet:
            qduty = sum(1 for r in quiet if r.get("motion")) / len(quiet) * 100
            print(f"  quiet 01–05h  {qduty:.1f}% duty over {len(quiet)} polls")

        # The verdict is the whole point of Phase A.
        print("  → ", end="")
        if errs / max(1, len(readings)) > 0.10:
            print("UNRELIABLE READS — fix connectivity before trusting anything else")
        elif duty > 85:
            print("SATURATED — always-on, cannot distinguish busy from quiet")
        elif duty < 1:
            print("TOO SPARSE — check framing, sensitivity, and that there WAS activity")
        elif ev and statistics.median([(e - s).total_seconds() for s, e, _ in ev]) < 10:
            print("TWITCHY — events too short; needs smoothing before use")
        else:
            print("USABLE — signal discriminates. Proceed to Phase B")


def phase_b(series: dict, sched_path: Path, min_sustain: int) -> None:
    print("\n" + "=" * 72)
    print("PHASE B — does motion match movements that actually happened?")
    print("=" * 72)

    windows = []
    with sched_path.open() as f:
        for row in csv.DictReader(f):
            windows.append({
                "label": row["label"].strip(),
                "start": parse_ts(row["start"].strip()),
                "end": parse_ts(row["end"].strip()),
                "desc": (row.get("description") or "").strip(),
            })
    if not windows:
        print("schedule is empty")
        return

    all_readings = [r for rs in series.values() for r in rs if r.get("ok")]
    detected = 0
    latencies = []

    print(f"  (a window counts as detected only on {min_sustain}+ consecutive "
          f"motion polls — one stray poll is noise, not a movement)\n")

    for w in windows:
        inside = [r for r in all_readings
                  if (r.get("label") or r["camera"]) == w["label"]
                  and w["start"] <= r["_ts"] <= w["end"]]
        # Sustained runs only. A single blip inside a 30-minute window is
        # background noise; without this the detection rate is meaningless.
        sustained = [e for e in runs(inside) if e[2] >= min_sustain]
        if not inside:
            status, extra = "NO DATA", ""
        elif sustained:
            detected += 1
            lat = (sustained[0][0] - w["start"]).total_seconds()
            latencies.append(lat)
            status, extra = "detected", f"  +{lat:.0f}s"
        else:
            blips = sum(1 for r in inside if r.get("motion"))
            status = "MISSED"
            extra = (f"  ({len(inside)} polls, {blips} isolated blip(s))"
                     if blips else f"  ({len(inside)} polls, all quiet)")
        print(f"  {w['label']:<12} {w['start']:%m-%d %H:%M}  {status:<9}{extra}"
              f"   {w['desc'][:36]}")

    covered = [w for w in windows
               if any((r.get("label") or r["camera"]) == w["label"]
                      and w["start"] <= r["_ts"] <= w["end"] for r in all_readings)]
    print(f"\n  detection rate  {detected}/{len(covered)} covered windows"
          f"  ({detected / max(1, len(covered)) * 100:.0f}%)")
    if latencies:
        print(f"  latency         median {statistics.median(latencies):.0f}s  "
              f"max {max(latencies):.0f}s")

    # Unexplained motion — the false-positive proxy.
    for (label, ch), readings in sorted(series.items()):
        ev = [e for e in runs([r for r in readings if r.get("ok")])
              if e[2] >= min_sustain]
        if not ev:
            continue
        lw = [w for w in windows if w["label"] == label]
        outside = [e for e in ev
                   if not any(w["start"] <= e[0] <= w["end"] for w in lw)]
        if ev:
            print(f"  {label} ch{ch}: {len(outside)}/{len(ev)} events outside any "
                  f"scheduled window ({len(outside) / len(ev) * 100:.0f}%)")

    print("\n  Read carefully: unexplained motion is not automatically a false")
    print("  positive. Unscheduled activity on a dock is real — and surfacing it")
    print("  is a safety feature (D-005), not noise. Check the snapshots before")
    print("  concluding the detector is wrong.")


def main() -> int:
    p = argparse.ArgumentParser(description="Analyse a Marshal motion log (Q-11)")
    p.add_argument("logs", nargs="+", type=Path)
    p.add_argument("--schedule", type=Path, default=None,
                   help="CSV of known movements → enables Phase B")
    p.add_argument("--min-sustain", type=int, default=3, metavar="N",
                   help="consecutive motion polls required to count as a real "
                        "movement (default 3 — rejects single-poll noise)")
    args = p.parse_args()

    paths = [q for q in args.logs if q.exists()]
    if not paths:
        sys.exit("no log files found")

    series = load(paths)
    if not series:
        sys.exit("logs contained no readings")

    phase_a(series)
    if args.schedule:
        if not args.schedule.exists():
            sys.exit(f"schedule not found: {args.schedule}")
        phase_b(series, args.schedule, args.min_sustain)
    else:
        print("\n(no --schedule given — Phase B skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
