# ADR-0011 — After Effects is part of the picture from EP77 onward

**Status:** Accepted (owner directive, 2026-08-23). Binding on every thread.
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
