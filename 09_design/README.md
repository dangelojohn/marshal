# Image-generation prompts — Marshal surfaces

For Nano Banana Pro (Google). Paste one prompt per generation. Also copied to
`~/Downloads/` for convenience.

Each carries a long **DO NOT RENDER** list. That section does most of the work:
image models default hard toward consumer-app and marketing aesthetics, and
without explicit exclusions you get rounded cards, gradients, emoji icons and a
smiling model in a clean warehouse — none of which is what either surface is.

## Wall board — `Marshal_Board_Prompt_*`

| # | State | Why it exists |
|---|---|---|
| 1 | **Hero** — 2 exceptions among 6 tiles | The normal working view. Proves exceptions are unmistakable at 3 metres while normal tiles stay ambient |
| 2 | **Calm** — zero exceptions, no red anywhere | **What the board looks like 95% of the time.** Generate this one too: if the calm state doesn't read as genuinely uneventful, the exception state won't land when it matters |
| 3 | **Tablet** — portrait, single column, exception sorted first | The supervisor walking the floor. Shows a 56px `ACKNOWLEDGE` target sized for gloves |

Palette is fixed across all three: background `#0E1116`, header `#161B22`,
accent amber `#E0A458`, exception red-orange `#D7503A`, calm green `#5FB37E`.

**Tile 5 in the hero is deliberately camera-down.** A dead camera must degrade
to a useful tile, never break the board — and the prompt makes the generator
render that case rather than an idealised one.

## Apple Watch Ultra — `Marshal_Watch_Prompt_*`

| # | State | Why it exists |
|---|---|---|
| 1 | **Job screen** — screen only | The primary state. **One job, never a list.** The amber dot beside `ARRIVED` is a visual echo of the physical Action Button |
| 2 | **In context** — gloved thumb on the orange Action Button | **The most important image of the set.** It carries the whole design argument: a capacitive screen does not work through a work glove, so the primary action lives on hardware |
| 3 | **Confirmation** — green check, recorded timestamp, one next-up line | A silent success is a failure — the operator presses again and the movement double-records. Showing the recorded time back is what earns trust |

Prompt 2 is the one to generate first if you only generate one. Everything about
the watch decision is arguable in prose and obvious in that photograph.

## If a generation comes back wrong

The usual failures and their fixes:

- **Looks like a marketing dashboard** → the DO-NOT list was truncated. Paste it whole
- **Rounded cards and gradients** → add "square corners, flat fills, no gradients" to the style paragraph
- **Charts appear** → strengthen the exclusion; models add graphs to anything called a "board"
- **Watch shows activity rings or the default face** → re-state "no watch face, no activity rings" first in the DO-NOT list
- **A finger on the watch glass in prompt 2** → that single detail is the argument; re-state it in the opening line

Related decisions: D-006 (the camera is the interface), D-012 (surface map),
`01_product/13_wearable_operator_surface.md` (why the Action Button decides the
hardware).
