# Audio cue sheet — PD-2026-002-gideon (v001)

Four-layer sound design so the episode is **never silent** (owner note 2026-06-14). Drives the
final Remotion/ffmpeg mix. Unlike EP1, the library now exists, so every cue is **bound to a real
`MUS-*` / `SFX-*` ID** (registries: `library/music_registry.v001.json`,
`library/sfx_registry.v001.json` on the media SSD). Music for the four signature beats uses the
episode's bespoke Suno tracks (`AST-0040…0043`); gaps reuse the shared library (reuse-first).

**Mix targets:** VO (narration master `06_voice/master/vc_master_v001.mp3`) on top and always
intelligible; music bed **−18…−22 LUFS** under VO; ambience near-subliminal (**≈−30 LUFS**, glues
cuts); SFX punctuate transitions/reveals. Master ≈ **−14 LUFS** (YouTube). Music ducks ~3–4 dB
under VO (sidechain). Timing source of truth: `08_edit/timing.v001.json` (atempo 0.84, 0.25s pad).

## Music beds (bound)

| Cue | Track | Scenes | Source |
|---|---|---|---|
| hook | `AST-0040` mus_gideon_hook_pencil (Suno, bespoke) | S001–S002 | episode 07_music |
| opening | `MUS-0003` opening_measured_arpeggio_v1 (library reuse) | S003 | library/music/opening |
| explainer bed | `MUS-0005` explainer_bed_soft_explainer_v1 (loopable, library reuse) | S004, S006, S010, S012, S016–S017 | library/music/explainer_bed |
| wall / tension | `AST-0041` mus_gideon_wall_betts (Suno, bespoke) | S006–S012 (primary under explainer) | episode 07_music |
| reveal | `AST-0042` mus_gideon_reveal_verdict (Suno, bespoke) | S013–S018 | episode 07_music |
| **strain (expansion→reality)** | `MUS-0007` tension_build_courtroom_horizon_v1 (library reuse) | S020, S023–S024 | library/music/tension_build |
| somber | `MUS-0009` somber_ledger_of_ash_v1 (library reuse) | S022 | library/music/somber |
| outro | `AST-0043` mus_gideon_outro (Suno, bespoke) | S025–S028 | episode 07_music |

> Resolves the open owner decision ("expansion→strain bed: reuse library or generate"): **reuse
> library** `MUS-0007` (tension_build) — approved 2026-06-16. No new generation needed.

## Ambience beds (bound — continuous, never silent)

`SFX-0017` courtroom room tone · `SFX-0018` tension drone · `SFX-0019` empty hallway ·
`SFX-0020` office hum · `SFX-0021` night window · `SFX-0022` institutional drone (subliminal glue).
All 22s, loopable, ElevenLabs Creator License.

## Scene-by-scene

| Scene | Emotion | Music | Ambience bed | SFX hits (bound) |
|---|---|---|---|---|
| S001 | hook_tension | hook `AST-0040` | tension drone `SFX-0018` | riser `SFX-0009` → **sub-drop `SFX-0016`** at "9–0"; ui-tick `SFX-0003` on text |
| S002 | curiosity | hook `AST-0040` | night window `SFX-0021` (cell) | soft-impact `SFX-0004` on cell reveal; *cell-door → `SFX-0004` (nearest; see gaps)* |
| S003 | orientation | opening `MUS-0003` | institutional drone `SFX-0022` | ui-tick `SFX-0003` per kinetic line |
| S004 | grounding | explainer `MUS-0005` | courtroom room tone `SFX-0017` | **gavel `SFX-0006`**; camera-shutter `SFX-0007` (still) |
| S005 | injustice | explainer `MUS-0005` (low) | tension drone `SFX-0018` | dust swell `SFX-0015` on the light; low-boom `SFX-0008` |
| S006 | imbalance | wall `AST-0041` + explainer | institutional drone `SFX-0022` | data-blip `SFX-0010` (scales/diagram); ui-tick `SFX-0003` |
| S007 | weight | wall `AST-0041` | courtroom room tone `SFX-0017` | **gavel `SFX-0006`**; stamp `SFX-0013` (GUILTY) |
| S008 | turn | wall `AST-0041` | tension drone `SFX-0018` | *pencil-scratch → `SFX-0005` paper_rustle (nearest)*; ui-tick `SFX-0003` |
| S009 | intimacy | wall `AST-0041` | night window `SFX-0021` (cell) | *pencil-scratch → `SFX-0005`*; paper rustle `SFX-0005` |
| S010 | underdog | explainer `MUS-0005` | institutional drone `SFX-0022` | paper `SFX-0005`; ui-tick `SFX-0003` (in forma pauperis) |
| S011 | obstacle | wall `AST-0041` | institutional drone `SFX-0022` | *stone-thud → low-boom `SFX-0008`*; page-turn `SFX-0011` |
| S012 | stakes | wall `AST-0041` + explainer | empty hallway `SFX-0019` | data-blip `SFX-0010` (funnel); paper `SFX-0005` |
| S013 | reversal | reveal `AST-0042` | courtroom room tone `SFX-0017` | reveal riser `SFX-0009`; stamp `SFX-0013` (name card) |
| S014 | anticipation | reveal `AST-0042` | institutional drone `SFX-0022` | ui-tick `SFX-0003`; riser `SFX-0009` into S015 |
| S015 | payoff | reveal `AST-0042` | courtroom room tone `SFX-0017` | **reveal sting** (music) + soft-impact `SFX-0004` (date card) |
| S016 | clarity | reveal `AST-0042` + explainer | courtroom room tone `SFX-0017` | ui-tick `SFX-0003` (underline); page-turn `SFX-0011` (Constitution) |
| S017 | principle | reveal `AST-0042` + explainer | institutional drone `SFX-0022` | whoosh `SFX-0001` (map sweep); data-blip `SFX-0010` |
| S018 | triumph | reveal `AST-0042` | tension→room `SFX-0018`→`SFX-0017` | *stone-crumble → low-boom `SFX-0008`* + soft-impact `SFX-0004` (OVERRULED) |
| S019 | cliffhanger | — (bed fades; ambience only) | night window `SFX-0021` | *heartbeat → clock-tick `SFX-0012` (subtle, nearest)*; dust `SFX-0015` |
| S020 | suspense | strain `MUS-0007` | courtroom room tone `SFX-0017` | room tone up; soft-impact `SFX-0004` (chair filled) |
| S021 | contrast | strain `MUS-0007` | courtroom room tone `SFX-0017` | **gavel `SFX-0006`**; stamp `SFX-0013` (NOT GUILTY) |
| S022 | revelation | somber `MUS-0009` | institutional drone `SFX-0022` | soft-impact `SFX-0004` (the gap); subtle |
| S023 | expansion | strain `MUS-0007` | office hum `SFX-0020` | whoosh `SFX-0001` (map); ui-tick `SFX-0003` |
| S024 | tension | strain `MUS-0007` | office hum `SFX-0020` | paper pile `SFX-0005`; data-blip `SFX-0010` (caseload) |
| S025 | bridge | outro `AST-0043` | institutional drone `SFX-0022` | ui-tick `SFX-0003`; whoosh `SFX-0001` (arrow to Miranda) |
| S026 | reflection | outro `AST-0043` | night window `SFX-0021` | dust swell `SFX-0015`; soft-swell `SFX-0015` |
| S027 | poignancy | outro `AST-0043` | empty hallway `SFX-0019` | swell `SFX-0015`; soft-impact `SFX-0004` |
| S028 | invitation | outro `AST-0043` | institutional drone `SFX-0022` | ui-tick `SFX-0003`; **end-card low-boom `SFX-0008`** |

## Global

- A continuous **ambience bed** runs under the entire episode (no dead air), swapped per the table
  (room tone in courtroom scenes; tension/institutional drone elsewhere; night window in cell/night).
- Every **wipe/transition** gets a short whoosh (`SFX-0001`/`SFX-0002`); every **on-screen-text
  reveal** a light ui-tick (`SFX-0003`) or soft-impact (`SFX-0004`).
- Reuse-first: all non-bespoke cues are shared library tracks, auto-selectable by family for future
  episodes. Bespoke `AST-0040…0043` are episode-specific (already in `07_music/`).

## Library gaps (honest — nearest substitute used; not blocking)

The library has no exact match for four requested one-shots; the cue sheet uses the documented
nearest substitute so the mix is never blocked. Optional future library additions:

- **pencil-scratch** (S008/S009) → using `SFX-0005` paper_rustle. *Best future add.*
- **cell-door** (S002) → using `SFX-0004` soft_impact.
- **stone thud / crumble** (S011/S018) → using `SFX-0008` low_boom.
- **heartbeat** (S019) → using `SFX-0012` clock_tick_loop (subtle, low).

> These substitutes are acceptable for first cut; QC notes them as S5 (cosmetic). Real `SFX-*`
> additions can be generated later via `scripts/gen_sfx.py` and registered with rights_basis.
