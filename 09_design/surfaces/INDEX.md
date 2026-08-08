# Marshal surfaces — UX/UI design index

Seven interfaces, one per role in `01_product/14_surface_map.md`. Each has its
own folder with an in-depth Stitch prompt, plus empty `images/` and
`background/` folders for you to add reference material, screenshots, and
notes as the design develops.

| # | Folder | Surface | Device | Status | Shares palette with |
|---|---|---|---|---|---|
| 1 | `01_receiver_iphone/` | Receiver | iPhone PWA | Base app live (Porterly Inbound), Marshal adds the movement/handoff layer | Own dark industrial palette (needs correcting against real Porterly screenshots) |
| 2 | `02_runner_watch/` | Runner | Apple Watch Ultra | New — also has Nano Banana photographic-concept prompts alongside the Stitch UI prompt | Wall board, coordinator (`#0E1116`/`#161B22`/`#E0A458`/`#D7503A`/`#5FB37E`) |
| 3 | `03_manager_wallboard/` | Manager (ambient) | Mounted display | New — partially live already at `/marshal/board`; also has Nano Banana prompts | Watch, coordinator |
| 4 | `04_manager_coordinator/` | Manager (desk) | Desktop web | New, genuinely undesigned anywhere yet — least-precedented surface in the set | Watch, wall board |
| 5 | `05_exhibitor_portal/` | Exhibitor + show manager | Responsive web | Base app live (Porterly Outbound), Marshal's schedule data is the new addition | Own — deliberately different, calmer, customer-facing palette |
| 6 | `06_driver_sms/` | Driver/carrier | Plain SMS | Designed, not built — a copy-design exercise, not really a "screen" | None — stock Messages app UI, no branding |
| 7 | `07_equipment_bay_kiosk/` | Any runner, shared device | Wall-mounted tablet | New — resolves open question Q-42, not yet locked | Receiver, watch, wall board |

## The two design languages in this set

**Operator-facing** (receiver, runner, wall board, coordinator, equipment
kiosk) — dark, industrial, high-contrast, built to be read fast under bad
light with cold or gloved hands. One shared status vocabulary: amber
`#E0A458` = waiting/in-progress, red-orange `#D7503A` = exception, green
`#5FB37E` = calm/done. No blue in this family.

**Customer-facing** (exhibitor portal) — warm, calm, professional B2B tool,
deliberately NOT dark or industrial, because the audience is a business
person planning ahead, not someone on a dock floor under pressure. Driver SMS
(surface 6) sits outside both languages entirely — it's stock Messages app UI
with no Marshal branding, by design.

## What's already built vs genuinely new

```
✅ LIVE (base app exists)   Receiver iPhone      Porterly Inbound PWA
✅ LIVE (base app exists)   Exhibitor portal      Porterly Outbound PWA
✅ PARTIALLY LIVE            Manager wall board    /marshal/board (demo mode)
⚠  DESIGNED, NOT BUILT       Driver SMS            D-005 §4
❌ NEW                       Runner watch          13_wearable_operator_surface.md
❌ NEW                       Manager coordinator    Q-43 open — may merge with wall board
❌ NEW                       Equipment-bay kiosk    Q-42 open — the recommended answer, not locked
```

## Live Stitch generation status (as of 2026-08-07)

All 7 Stitch prompts below were fed live into Google Stitch to generate actual
screens, not just written as documents. Result: **4 of 7 surfaces have a
generated screen; 3 timed out on every attempt** (server-side timeouts in the
Stitch tool itself, not a prompt-content problem — the same prompt style
worked for the other 4).

| Surface | Stitch project | Screens generated | Attempts |
|---|---|---|---|
| Runner watch | `11083755986653929486` | ✅ 3/3 (Job, Confirmation, Blocked) | 3 |
| Manager wall board | `16058307761228463082` | ✅ 1/1 (8-tile board) | 3 |
| Driver SMS | `12344250436276857594` | ✅ 1/1 (SMS thread) | 2 |
| Equipment-bay kiosk | `6709148109466083048` | ✅ 1/1 | 1 |
| Receiver iPhone | `11715200098096487538` | ❌ 0/2 planned | 6, all timed out |
| Manager coordinator | `911681423700399441` | ❌ 0/1 planned | 6, all timed out |
| Exhibitor portal | `18077315178070195948` | ❌ 0/2 planned | 6, all timed out |

Each of the 3 failing projects and its tailored design system asset already
exist in Stitch and are ready to receive a screen — the `STITCH_PROMPT.md` in
each folder has the exact prompt text used. Re-running
`generate_screen_from_text` against the existing project/design-system IDs
above (no new setup needed) is the fastest path to finishing these three;
worth trying again on a future session, or generating directly in the Stitch
web UI by pasting the prompt from `STITCH_PROMPT.md` if the MCP tool keeps
timing out.

**Retried 2026-08-08: same 3 failed a 7th time, still 0 screens, still
confirmed empty via `list_screens` on every attempt.** This is a stable,
reproducible failure specific to these 3 Stitch projects (not a transient
blip) — not worth further blind retries. Generating directly in the Stitch
web UI, pasting the prompt from each folder's `STITCH_PROMPT.md`, is the
most likely way to actually close these out.

## Background material — screenshot attempt blocked (2026-08-08)

Tried to populate `background/`/`images/` with real screenshots of the two
live precedents this project explicitly calls for — the wall board
(`192.168.68.89:8069/marshal/board`) and the live Porterly Inbound/Outbound
PWAs (`192.168.68.87:8069`, or `porterly.space`) — via browser automation.

**Blocked:** the Chrome extension's automation returns "Permission denied
for this action on this domain" for both `192.168.68.89` and `192.168.68.87`
— this reads as a blanket policy on private-network (`192.168.x.x`) IPs, the
same wall hit earlier trying to reach RainCloud's QTS admin UI at
`:8080`. `porterly.space` itself didn't resolve/connect from this network
path either. **Only the account owner can grant the extension permission
for these hosts** (or take the screenshots manually and drop them in) — this
isn't something retrying fixes.

**What's confirmed working instead (curl, not a browser, so no permission
wall applies):** the wall board is fully live and correct when authenticated
— `/marshal/board` and `?demo=1` both return HTTP 200, `/marshal/board/state`
returns real tile data (4 tiles, all clear, 0 open DLQ entries, 0 broken
custody chains). It redirects unauthenticated requests to `/web/login`,
which is **by design** (`board.py`'s own comment: "the board hangs on a wall
and logs in once"), not a bug — worth knowing so a future session doesn't
mistake that redirect for a regression the way a first pass at this did today.

## Open questions that affect these designs

Carried over from `01_product/14_surface_map.md` — worth resolving before
treating any of these as final:

- **Q-42** — Is the equipment-bay kiosk (surface 7) really the right answer, or should checkpoints live somewhere else?
- **Q-43** — Are the wall board (surface 3) and coordinator view (surface 4) one responsive surface or two separate products?
- **Q-44** — Do receivers and runners overlap in practice, or are they distinct people? (Affects whether surfaces 1 and 2 are ever used by the same person in one shift.)

## How to use each folder

1. Read `STITCH_PROMPT.md` — it has the full design brief (color/type/layout
   rationale) and the literal prompt text to feed Stitch.
2. Drop reference screenshots (especially of the two already-live Porterly
   apps) into `images/`.
3. Drop any notes from watching real operators, coordinators, or exhibitors
   use the current (pre-Marshal) process into `background/` — this project
   has more written requirements than observed behavior right now, and that
   gap matters most for surfaces 4 and 7, which have no live precedent at all.
