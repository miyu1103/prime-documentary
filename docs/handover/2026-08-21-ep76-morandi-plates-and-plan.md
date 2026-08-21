# 2026-08-21 — EP76 morandi: the plates came back, and the report did not match the disk

**Continues `2026-08-21-ep76-morandi-design.md`.** That session took EP76 to a measured script. This
one took delivery of 120 Codex plates, read them, and built the four left-process artefacts that were
still missing.

> **Another session was working EP74 in this repo at the same time** and pushed several commits
> (`27449f94`…`45811ed6`). Nothing collided — it even finished the `--src` option on
> `build_plate_contact_sheet.py` that this session had started, and it carried this session's
> `episode_footage_queries` morandi entry in with its own commit. Worth knowing that the branch moves
> under you.

---

## 1. The delivery, and the two places it disagreed with the disk

The report said: 120 generated, 115 passing QC and upscaled, five withheld, **nothing staged** so a
partial set could not become render truth. That last part is exactly the right instinct.

**Measured before acting on any of it:**

| claim | disk |
|---|---|
| 120 generated, all upscaled | **true** — 120 PNGs, **every one exactly 3840×2160**, ids matching the order, none extra |
| five withheld and not staged | **false** — all 120 were in `remotion/public/morandi/img`, the five included. A render started then would have cut them in |
| five failed QC | **one of five holds** |

**Four of the five rejections did not survive a look at the file:**

- `V070` "a landscape instead of an inspection form" → a blank ruled sheet on a desk, which is what
  V070 asks for.
- `V073` "a landscape instead of graph paper" → blank graph paper with two ruled axes.
- `V086` "a landscape instead of a printed form" → a blank ruled form with a paperclip.
- `V085` "readable digits and lettering on the fax machine" → two full-resolution crops of the body
  and the output tray show blank moulded plastic and blank thermal paper. No keypad, no display, no
  glyph in frame.
- `V024` "bridge type and period wrong" → **correct**. It is a white steel truss where a concrete
  cable-stayed viaduct was ordered.

**And one rejection of mine did not survive either, which is the lesson worth keeping.** I rejected
`V106` — the severed deck, the last image of ACT_4 — off a 400 px contact-sheet tile as "an intact
viaduct". At full resolution the deck is plainly cut: a span ends in mid-air, a wide gap of grey sky,
the span resumes, the valley and the port far below, no debris and no vehicle. **A thumbnail is not
evidence.** This time it cost one crop; the same mistake on a delivery day costs a regeneration
round.

## 2. What was actually wrong

**Three plates, quarantined to `remotion/public/morandi/_rejected_v001/` — retired, never deleted:**

| id | why |
|---|---|
| V008 | concrete with exposed aggregate where the stay's steel cables should be. It is the OP's hero object and the film's central idea |
| V020 | mid-1960s construction with both workmen in modern orange hi-vis and hard hats |
| V024 | a white steel truss where a concrete cable-stayed viaduct was ordered |

**Four plates where the ORDER was wrong, not the generation.** `V078 V104 V112 V114` carry the `P`
people flag on prompts that ask for no person — two of them say *empty* outright. The generator was
right. **This mattered: it put the real people count at 20 against a declared `people_plates_min` of
24.** v002 reorders them with a figure.

**Regeneration batch is seven**, in `episodes/_planning/EP76_morandi_CODEX_REDO_ALL.txt`.

**Three off-brief plates ship as they are**, recorded so their absence is not read as an oversight:
V025 (no traffic in a "period traffic" plate), V051 (three towers, one scaffolded, does not read),
V063 (no step in the dropped slab). All texture, none carrying a beat.

`check_plate_verdicts.py --slug morandi` → **PASS**, 117 accept / 3 reject, every verdict sha-bound
to the bytes. The verdict file is under `runs/`, which this repo does not track.

## 3. The four artefacts that were missing

| artefact | what it says |
|---|---|
| **FOOTAGE_PLAN v001** + `episode_footage_queries.morandi` | **The headline is positive, which is the opposite of EP75.** This shelf carries the film's road, port and paperwork registers: 3,067 rows over 34 measured terms against a utilisation floor of 40 and a distinct-asset target of 265. What it cannot carry is the film's own texture — `corrosion` 1, `rebar` 1, `viaduct` 1, `scaffolding` 1 — which is what the 120 plates are for |
| **SCENE_PLAN v001** | PROJECTED, and says so. 468 cuts at a 3.75 s mean, 119 plate cuts under a 150 ceiling, 349 video-and-motion cuts over a 318 floor |
| **thumb_prompts v001** | Three titles, all through `check_packaging_claims` with zero unsupported claims; six concepts; NEG carrying all five families |
| **fact_recheck v001** | Four items before the render, six for publish day, and **one with a date on it** — §5 below |

## 4. Every obvious search term for this episode is a trap

Measured by reading what came back, not by trusting a count:

| term | rows | what it actually returns |
|---|---|---|
| `port` | 554 | trans**port**ation, **Port**ugal, **port**al, s**port**s |
| `rain` | 491 | t**rain**ing, railway — and **"money raining"**, itself a forbidden subject |
| `paper` | 914 | news**paper**, and "beautiful wall**paper**" flags and landscapes |
| `hand` / `hands` | 807 / 723 | people eating pizza and dancing. Not a paperwork register |
| `beam` | 30 | balance beams and sunbeams. **Zero structural beams** |
| `toll` | 6 | entirely a**toll** |
| **`italy`** | **84** | **Venice gondolas, Tuscan cypress avenues, the Dolomites** — the exact register `forbidden_subjects` bars |

The replacements were measured too, and that is the half that matters: `dock` 46, `cargo ship` 33,
`documents` 12, `office desk` 78, `hands writing` 37 — all clean.

## 5. The item with a date on it

**The court gave itself ninety days from 16 July 2026 to file its reasons — on or about
14 October 2026.** The script's ENDING says *"we will not know it for weeks"*. **If this film
publishes after that, the sentence is false**, and an appeal may by then have been formally lodged
rather than merely announced.

On the day a publish date is set: re-check whether the *motivazioni* are deposited and whether an
appeal is lodged. If either, **ACT_5's last three lines and the description are rewritten before
scheduling. It is a splice, not a re-render.**

## 6. State now

| | |
|---|---|
| spec / ledger / bible / script | done, and `check_script_standard --slug morandi --wpm 184.0` = **12/12** |
| scene plan / footage plan / thumbs / fact_recheck / manifest | done |
| plates | **117 of 120 staged and verdict-bound; 7 outstanding** (3 rejects + 4 reorders) |
| narration master | **generating as this note was written** (~$8.86). Log: `out_ep76_narration.log` |
| footage | **0 staged.** `check_cross_episode_reuse.py` first, then a labelled contact sheet |
| render | not started, and `preflight_render_gate.py` must be green first |

## 7. Next, in order

1. Paste `EP76_morandi_CODEX_REDO_ALL.txt` to Codex — seven plates. Upscale to exactly 3840×2160,
   then stage all 120 at once and **read the seven at full resolution, not on a tile**.
2. When the narration master lands, write **SCENE_PLAN v002 from `06_audio/narration_index.v001.json`**
   — every timestamp in v001 moves.
3. Then `episode_spec.mandatory_stills` gets all 120 basenames, because EP54's fourteen purpose-made
   stills were silently dropped by a surplus-trimming rule and retired as unreferenced.
4. Footage staging, cross-episode reuse check, contact sheet.
5. Preflight green, then render.
