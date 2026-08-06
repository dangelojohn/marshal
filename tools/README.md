# Reolink motion test — Q-11

**Question:** is Reolink motion detection reliable enough at dock distance and in
dock lighting to serve as **automatic actuals capture**?

**Why it matters more than it looks.** `spec/03` established that Marshal must
record planned-vs-actual on every movement from day one, and flagged the obvious
problem: nobody taps *"delayed — reason"* at 6am during a move-in. If
`get_motion_state` can tell busy from quiet, the actuals collect themselves from
hardware already on the wall — and the entire predictive layer becomes viable.
If it can't, someone has to type, and experience says they won't.

**Cost to answer: one camera, one dock, one show.** No product required.

---

## Setup

```bash
cd tools
cp cameras.example.json cameras.json      # gitignored — it holds passwords
$EDITOR cameras.json
./reolink_motion_probe.py --check         # connectivity + device info
```

`--check` prints model, firmware and a live motion reading per channel. If that
works, everything else will.

## Run

```bash
# LAN test cameras — validate the harness before it matters
./reolink_motion_probe.py --hours 2

# Real dock, full move-in day, with periodic stills for ground truth
./reolink_motion_probe.py --hours 14 --snapshot-every 300
```

Writes `motion_log/motion-<stamp>.jsonl`, one JSON object per camera per channel
per poll. Default interval 5s. Ctrl-C stops cleanly. A camera that fails is
logged as `ok: false` and the run continues — **one dead camera never kills the
test.**

## Analyse

```bash
./analyze_motion_log.py motion_log/motion-*.jsonl
./analyze_motion_log.py motion_log/motion-*.jsonl --schedule schedule.csv
```

### Phase A — discrimination (no schedule needed)

Runnable the moment a camera points at anything. Answers *can this signal tell
busy from quiet at all?*

| Metric | What it tells you |
|---|---|
| **Duty cycle** | >85% saturated (everything looks busy); <1% blind |
| **Event count and length** | 1-poll blips mean twitchy; hours-long runs mean saturated |
| **Quiet hours 01–05** | The natural negative control — motion at 3am with nobody there is a false positive |
| **Poll loss** | A signal you can't read reliably isn't a signal |

Ends with a verdict: `USABLE`, `SATURATED`, `TOO SPARSE`, `TWITCHY`, or
`UNRELIABLE READS`.

### Phase B — accuracy (needs a schedule)

`schedule.csv`, one row per movement you know actually happened:

```csv
label,start,end,description
Dock 4,2026-09-14T08:00:00,2026-09-14T08:30:00,crate to booth 412
```

`label` matches the camera label in `cameras.json`. Reports detection rate,
latency from window start to first motion, and motion outside every window.

**A window counts as detected only on `--min-sustain` consecutive motion polls
(default 3).** This matters: a synthetic test with 2% background noise scored a
false detection on a deliberately-empty control window from a single stray poll.
One blip in a 30-minute window is noise, not a movement — without the sustain
requirement the detection rate is meaningless.

---

## Reading the result honestly

**Unexplained motion is not automatically a false positive.** Unscheduled
activity on a dock is real, and surfacing it is a *safety feature* (D-005), not
noise. Check the snapshots before concluding the detector is wrong — that's what
`--snapshot-every` is for.

**A `TWITCHY` verdict is not a failure either.** It means the raw signal needs
smoothing (require N consecutive polls, or debounce), not that the approach is
dead. Only `SATURATED` at a busy dock is genuinely fatal — a detector that is
always on carries no information.

**Poll interval is a real variable.** 5s is the default; if events are being
missed, try 2s before concluding the camera can't see them.

---

## Implementation notes

Standard library only — no pip, no virtualenv. Copy to any machine with Python
3.8+.

Protocol replicated from the verified working client at
`~/hermes-console/api/mcp/clients/reolink.py`: `POST /cgi-bin/api.cgi`, login
returns a token carried as `?token=`, re-login on *"please login first"*,
`GetMdState` for motion, `Snap` for stills. Self-signed certs on `:443` are
accepted, matching that client's `verify=False` — these are LAN devices.

**`cameras.json` and `motion_log/` are gitignored.** Passwords never enter the
repo.
