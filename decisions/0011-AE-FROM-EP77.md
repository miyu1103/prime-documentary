# ADR-0011 — After Effects is part of the picture from EP77 onward

**Status:** Accepted (owner directive, 2026-08-23). Binding on every thread.
**Review by:** 2026-10-05
**Revoke if:** the thumbnail experiment `thumbnail-2026-09-07` returns WIN on 2026-10-05
(`py -3.11 scripts/pd_experiments.py`), i.e. the measured constraint is packaging rather than
the picture — in which case AE work is deferred, not cancelled, and the 51 scripts stay on disk.
Also revoke if adding AE raises per-episode production time by more than 25% without the
median watch percentage of AE episodes exceeding 30% (`scripts/_yt_studio_video_ctr.*.json`).
The review date and the condition are the assistant's reading, added 2026-08-23 under
`scripts/check_decisions.py`; the owner may replace either at any time.
**Scope:** episodes **PD-2026-077-\*** and later. EP70–EP76 are unaffected and finish on the
current Remotion-only path.
**Supersedes:** nothing. **Superseded by:** nothing.

---

## The decision

**From EP77, After Effects is used in the film.** It is no longer a retired tool kept alive by
old scripts; it is part of how an episode is made.

The owner's instruction was one line and it is not conditional. What follows is the reading of
it that this repository will act on until told otherwise, written down so that no thread has to
guess.

## What was measured before writing this (2026-08-23)

| what | measurement |
|---|---|
| AE automation in the repo | `scripts/ae/` — **51 scripts**, driving `AfterFX -r` to build and `aerender` to write |
| what it has produced | hero cards for atwater, centralpark, cleveland, frazier, glover, kidsforcash, lech, strieff, tekoh, thompson, tlo, young — and Shorts |
| last AE job on disk | `runs/ae_jobs/short273,276,282.json`, **2026-08-12** |
| AE assets referenced by EP70–76 film json | **0** |
| AE mentioned in EP70–76 filmconfigs | **0** |

So the capability is built and proven, and the current long-form line simply stopped calling it.
Restarting is a wiring job, not a build.

## How it is used (default reading, adjustable by the owner)

1. **Hero cards are AE's job.** The single-image beats that carry a number, a comparison or a
   document blow-up — the places where the film stops and shows one thing large. This is where
   AE measurably beats `FigureBeats`, and it is what the 51 existing scripts already do.
2. **Everything else stays in Remotion.** Cuts, captions, bookends, motion blur, the 38 figure
   kinds. There is no second implementation of anything Remotion already draws (invariant 14),
   and `scripts/figure_spec.py` now type-checks those figures against `FigureBeats.tsx`, which
   the AE path has no equivalent of.
3. **AE output is a plate, not a live layer.** AE writes an mp4 or a PNG sequence into the
   episode's own asset directory, it is registered like any other asset (provenance, sha256,
   licence), and Remotion cuts it. The film json never depends on AE being installed.

## What must exist before EP77's first AE beat

None of this is optional and none of it is done yet:

- **A generic builder.** `scripts/ae/build_<slug>_hero_cards.py` × 12 is the invariant-14 smell
  the sound-plan one-offs were. EP77 gets `scripts/ae/build_hero_cards.py --slug <slug>` reading
  a per-episode json, in the shape of `write_sound_plan.py`.
- **A verify step that reads pixels.** `scripts/ae/verify_lech_compare_cards.py` is the model:
  probe every output, extract the mid-frame to disk, measure real contrast per text zone. An AE
  card that rendered blank must fail before the film json is built — the EP76 `split` lesson,
  where eight figures would have drawn white and only a type check caught them.
- **The crash trap, handled.** A force-killed AE leaves `PriorSafeMode.txt` and the crash-recovery
  dialog then blocks **every** later launch, including headless ones. The builder deletes that
  file before starting and quits AE through `app.quit()`, never by taskkill.
- **Serialisation with the GPU.** i2v, a Remotion render and AE all want the machine. AE goes
  through `scripts/pd_run.sh` with its own lock class, like everything else.
- **`gpuAccelType = SOFTWARE`** unless a measurement says otherwise; GPU acceleration in AE has
  been unstable on this node.

## What this does not change

- The ship gate, the four blocking classes, and the requirement that a human read the shipped
  frames of the real render.
- The rule that generated imagery is never presented as an authentic record. An AE hero card is
  a designed graphic; if it renders a document, the same `fabricated_record` rules apply.
- EP70–EP76. They ship as they are.

---

## 2026-08-23 — owner clarification, and the design stage built against it

The owner restated the directive the same day, in one line: **from EP77, After Effects is used
heavily, and it is the DESIGN STAGE that has to work now.** That widens §"How it is used" item 1.
Written down rather than reconciled silently, because a reader six weeks from now will otherwise
find two readings of one directive:

| | as first written above | as clarified 2026-08-23 |
|---|---|---|
| AE's role | hero cards only | nine declared kinds: `hero_number`, `document_blowup`, `comparison`, `timeline`, `system_map`, `quote_card`, `map_move`, `list_build`, `title_card` |
| how much | not stated | **≥12 beats, ≥1 per act, ≥90s on screen** — floors, not targets |
| what is built first | the generic builder and the pixel verify | **the design contract**, so an episode cannot be designed without AE in it |

Item 2 is unchanged and still governs: cuts, captions, bookends, motion blur and the 38 figure
kinds stay in Remotion, and nothing here is a second implementation of them (invariant 14).

**Where the floors come from.** Measured 2026-08-23 across the 26 episodes carrying an
`episode_spec`: the median declares 8 acts at 13–17 figure beats each — 104–136 declared
motion-graphic beats — and built film json carries 16–99 actual figures. Twelve AE beats is
about a tenth of the declared beats and **6–12× the previous standard**, which was PD_CANON §6's
"one or two kinetic beats mid-film" (1–2%). 90 seconds is 12 × the 7.5 s a hero card needs to be
readable. If a later measurement moves these, move them here and in the schema together.

**What now exists (design stage only, as instructed).**

| what | where | proof |
|---|---|---|
| the declaration | `ae_beats` in `schemas/episode_spec.v001.json` — optional field, so every EP001–076 spec still validates unchanged | 26 specs re-validated; the only two failures (`lacmegantic`, `uri`) are a pre-existing `_people_plates_note` extra property and predate this change |
| the gate | `ae_problems()` in `scripts/check_episode_spec.py`, called from `load_and_validate()` — so it runs wherever the spec is already checked, with **no new tool to forget** (invariant 14) | reads the spec only: no AE, no GPU, no network |
| required from EP77 | `AE_FROM_EPISODE = 77`; a missing `ae_beats` on EP077+ is an error, and on EP076 and earlier is silence | `test_ep77_without_ae_beats_is_refused`, `test_ep76_without_ae_beats_is_left_alone` |
| shown to fail | `tests/test_ae_beats_design_gate.py`, 11 cases, all green 2026-08-23 | every floor is broken on purpose: 11 beats, 16 beats piled into one act, an act outside the vocabulary, duplicate ids, 12 two-second flashes, another episode's jobs file, a headline with no `source` |

**`source` is required on every beat.** An AE card states a fact on screen, so it is subject to
`factual_support` exactly as a title is (rule 19). The schema refuses a beat without the ledger
row or script line its headline came from.

**What this still does not do, stated plainly.** It cannot see whether an AE card rendered. The
pixel-reading verify in "What must exist before EP77's first AE beat" above is untouched and
still required before a film json is built — eight EP76 figures would have drawn white and only
a type check caught them. A green design is not a rendered beat.
