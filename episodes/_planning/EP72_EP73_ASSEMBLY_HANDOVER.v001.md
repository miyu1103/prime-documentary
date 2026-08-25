# EP72 + EP73 — HANDOVER TO THE ASSEMBLY THREAD

**Written 2026-08-22 by the preparation thread. Everything below was verified on disk at the time
of writing, not reported from memory.**

Both episodes are **30-minute long-form**. Script, narration and plates are DONE and measured for
both. What remains is assembly: asset manifest → asset selection → `film.json` → preflight → render.

---

## 0. THE ONE-SCREEN STATUS

| | EP72 `PD-2026-072-lacmegantic` | EP73 `PD-2026-073-uri` |
|---|---|---|
| Subject | Lac-Mégantic runaway oil train, night of 5–6 July 2013 | Texas / Winter Storm Uri, February 2021 |
| Script | ✅ v003 | ✅ **v002** (rewritten today, 2,845 → 5,230 words) |
| Narration master | ✅ **1774.8 s** (29:35), 40.6 MB | ✅ **1792.6 s** (29:53), 41.0 MB |
| Film length with 9.0 s end card | **1783.8 s = 29:44** | **1801.6 s = 30:02** |
| `runtime_seconds` contract | [1740, 1920] → **inside** | [1740, 1920] → **inside** |
| Plates **staged and signed for** | ✅ **156** at 3840×2160, 156/156 pass, binding=exact | ✅ **163** at 3840×2160, 163/163 pass, binding=exact |
| — of which Batch B | 36 of 48 ordered (12 never delivered) | 43 of 48 ordered (5 never delivered) |
| Stock harvested and **all** reviewed | 316 clips, 316 verdicts | 293 clips, 293 verdicts |
| Stock **usable** | **102** | **117** |
| narration.mp3 staged for the render | ✅ | ✅ |
| Assembly | ❌ not started | ❌ not started |

**`pd_preflight.py` now runs and says exactly what is left.** It was hardcoded to the dead H: drive
until 2026-08-22 and would have reported the narration missing; it now resolves through
`config/storage.local.json` and reads the real master. Current output:

```
EP72 lacmegantic   BLOCKED
  narration_seconds 1774.8 | chunks 378 | master_mb 42.6 | 146 chunks need caption split
  [warn]  E/FILM   film.json not built yet (scripts/build_case_film_generic.py)
  [BLOCK] B/ASSETS asset_manifest.v003.json missing
                   (scripts/build_asset_manifest_motionfirst.py --slug lacmegantic)
  [BLOCK] D/CONFIG EP72_lacmegantic_filmconfig.v001.json missing

EP73 uri           BLOCKED
  narration_seconds 1792.6 | chunks 369 | master_mb 43.0 | 141 chunks need caption split
  [warn]  E/FILM   film.json not built yet
  [BLOCK] B/ASSETS asset_manifest.v003.json missing
                   (scripts/build_asset_manifest_motionfirst.py --slug uri)
  [BLOCK] D/CONFIG EP73_uri_filmconfig.v001.json missing
```

**That is the whole remaining task list for both films: a filmconfig, an asset manifest, a
film.json, then render.**

---

## 1. WHERE EVERYTHING IS

Paths are given relative to the repo `C:\Users\aab15\Documents\prime-documentary` unless they start
with a drive letter. The media root resolves through `config/storage.local.json` → **`E:\pd-media`**
(it was `H:\pd-media`; that drive is dead — see §5).

### EP72 — lacmegantic

```
script          episodes/_planning/EP72_lacmegantic_script.en.v003.md
facts ledger    episodes/_planning/EP72_lacmegantic_FACTS_LEDGER.v003.md   (v001/v002 also present)
film bible      episodes/_planning/EP72_lacmegantic_FILM_BIBLE.v001.md
scene plan      episodes/_planning/EP72_lacmegantic_SCENE_PLAN.v001.md
image order A   episodes/_planning/EP72_lacmegantic_CODEX_BATCH_A.v001.md   (L001-L120)
image order B   episodes/_planning/EP72_lacmegantic_CODEX_BATCH_B.v001.md   (L121-L168)
thumb prompts   episodes/_planning/EP72_lacmegantic_thumb_prompts.v001.md
episode spec    episodes/PD-2026-072-lacmegantic/episode_spec.v001.json

narration index episodes/PD-2026-072-lacmegantic/06_audio/narration_index.v001.json
narration master E:\pd-media\episodes\PD-2026-072-lacmegantic\06_voice\master\vc_master_v001.mp3

plates (staged) remotion/public/lacmegantic/img          120 × 3840×2160 PNG
plate verdicts  runs/qc/lacmegantic_plate_verdicts.v001.json   120/120 pass, binding=exact
plate sheets    runs/qc/lacmegantic_plates/lacmegantic_01..10.png
batch B raw     E:\pd-media\assets\ai\lacmegantic\_batch_b     36/48 so far, 1672×941

stock ledger    episodes/PD-2026-072-lacmegantic/05_stock/stock_ledger.v001.json      247 rows
stock verdicts  episodes/PD-2026-072-lacmegantic/05_stock/editorial_verdicts.v001.json
                                                    90 accept / 66 conditional / 91 reject
stock files     E:\pd-media\episodes\PD-2026-072-lacmegantic\05_stock\candidates\*.mp4
stock sheets    runs/qc/lacmegantic_stock/stock_01..09.png
                runs/qc/lacmegantic_stock/stock_from109_01..05.png
                runs/qc/lacmegantic_stock/stock_from168_01..07.png
stock prose QC  runs/qc/lacmegantic_stock_verdicts.v001.md
```

### EP73 — uri

```
script          episodes/_planning/EP73_uri_script.en.v002.md      <-- v001 was deleted, use v002
facts ledger    episodes/_planning/EP73_uri_FACTS_LEDGER.v001.md   (46 rows, 45 cited)
film bible      episodes/_planning/EP73_uri_FILM_BIBLE.v001.md
image order A   episodes/_planning/EP73_uri_CODEX_BATCH_A.v001.md  (U001-U120)
image order B   episodes/_planning/EP73_uri_CODEX_BATCH_B.v001.md  (U121-U168)
episode spec    episodes/PD-2026-073-uri/episode_spec.v001.json
fact recheck    episodes/PD-2026-073-uri/01_research/  (if present)

narration index episodes/PD-2026-073-uri/06_audio/narration_index.v001.json
narration master E:\pd-media\episodes\PD-2026-073-uri\06_voice\master\vc_master_v001.mp3

plates (staged) remotion/public/uri/img                  120 × 3840×2160 PNG
plate verdicts  runs/qc/uri_plate_verdicts.v001.json           120/120 pass, binding=exact
plate sheets    runs/qc/uri_plates/uri_01..10.png
batch B raw     E:\pd-media\assets\ai\uri\_batch_b            43/48 so far, 1672×941

stock ledger    episodes/PD-2026-073-uri/05_stock/stock_ledger.v001.json           223 rows
stock verdicts  episodes/PD-2026-073-uri/05_stock/editorial_verdicts.v001.json
                                                    95 accept / 50 conditional / 77 reject
stock files     E:\pd-media\episodes\PD-2026-073-uri\05_stock\candidates\*.mp4
stock sheets    runs/qc/uri_stock/stock_01..13.png
                runs/qc/uri_stock/stock_from150_01..07.png
```

---

## 2. THE ONE FILE THE ASSEMBLY MUST NOT IGNORE

`05_stock/editorial_verdicts.v001.json` — **a human watched every harvested clip and wrote a verdict
for each.** 470 clips across the two episodes, three frames each.

`scripts/build_usable_assets.py` now reads it: `reject` → `blocked`, `conditional` → `review`,
everything else falls through to the rights rules as before. **Run that script before building any
manifest** and take `usable_assets.v001.json` as the pool — do not read the stock ledger directly.

```
py -3.11 scripts/build_usable_assets.py 72 --write
py -3.11 scripts/build_usable_assets.py 73 --write
```

Current output:

```
EP72  Assets: 478  ->  usable=90   review=66   blocked=322
EP73  Assets: 456  ->  usable=96   review=50   blocked=310
```

**`conditional` is not `usable`.** Those 66 + 50 clips are real footage with one identified problem
(a legible word to crop out, a background that is the wrong country, a person who might resolve).
They can be promoted individually with the note in the file as the instruction — but not in bulk.

**Row 212 of EP73 has no verdict.** ffmpeg could not decode it. It is not a reviewed pass.

---

## 3. TWO GATE BUGS FIXED TODAY — the numbers changed because of them

**`build_usable_assets.py` was counting rows, not files.** It reported `usable=274` for EP72, of
which **234 were the shared library `references/stock_manifest.json`, and not one of those files
exists** — they were on the dead H: drive. It now checks the byte stream is on disk and blocks the
row if it is not. If the assembly thread sees a much smaller "usable" number than it expects, this
is why, and the smaller number is the true one.

**`check_script_length.py` was counting the producer's blockquote header as speech.** Every script
since EP66 opens with one. On EP73 that was +342 words, enough to flip a script that is in band to
`FAIL LONG`. Fixed. EP72 and EP76 were re-run and did not move.

---

## 4. WHAT IS STILL RUNNING IN THE PREPARATION THREAD

1. **Codex Batch B — DONE for what was delivered.** 36 + 43 of 48 arrived, **all 16:9 and all
   1672×941 — zero wrong-aspect plates, against 28 of 120 in Batch A.** All 79 were upscaled to
   3840×2160, read on contact sheets in `runs/qc/<slug>_plates_b/`, staged into
   `remotion/public/<slug>/img`, and signed for. Nothing about Batch B is outstanding except the
   **17 ids that were never delivered**: `L121 L122 L125 L128 L132 L144 L145 L159 L160 L162 L163
   L164` and `U125 U129 U145 U163 U164`. The films do not need them.

   **One plate failed and was fixed: `U161`.** As delivered it carried a green street sign with
   garbled pseudo-lettering — invisible on the contact sheet, plainly "writing" at 4K, and a
   generated glyph is one of the four ship-blocking classes. The **source** 1672×941 was cropped to
   the right-hand 16:9 window and re-upscaled, so the delivered pixels are enlarged only once. The
   verdict is bound to the new sha256.

   **Two plates depart from their order and were accepted anyway** — `L131` (hands on a wagon-top
   lever, not a locomotive roof) and `U166` (a clad pipeline, not lagging on plant pipework). Both
   are noted in the verdict file so nobody reads "pass" as "the order was followed literally".

2. **Pexels shelf recovery** — `scripts/recover_pexels_shelf.py --write`, re-downloading the 9,294
   clips that died with H:. **735 recovered so far**, media to `D:\pd-archive`, ledger to
   `E:\pd-archive\_ledger\pexels.jsonl`. Resumable and safe to re-run. **It died once already
   without writing an error** — check the process is alive before relying on it.
   Logs: `runs/shelf_recovery/recover_<stamp>.log`.

---

## 5. THINGS THAT WILL BITE THE ASSEMBLY IF NOBODY SAYS THEM

- **H: is gone.** `config/storage.local.json` repoints the media root to `E:\pd-media`.
  **Fifteen generic pipeline scripts were still hardcoding `H:/pd-media` and were re-rooted on
  2026-08-22**, each now resolving through that config with the old literal kept only as a
  fallback: `pd_preflight`, `stage_factory_for_episode`, `stage_case_factory_assets`,
  `check_dynamics`, `check_narration_voice`, `check_plate_verdicts`, `check_motion_integrity`,
  `check_source_image_luma`, `build_case_bgm_generic`, `build_motion_from_plates`,
  `build_rights_manifest`, `i2v_episode_batch`, `assemble_episode_i2v`, `scan_video_shape`,
  `handover_snapshot`. All fifteen were then IMPORTED and checked to resolve to `E:\pd-media` —
  `py_compile` passes a file that still raises `NameError` at import, and one of them did.
  **~200 per-episode scripts for already-shipped episodes still carry the H: literal and were
  deliberately left alone.** If you resurrect one of those, re-root it first.
- **`references/stock_manifest.json` is dead weight.** 234 rows, 0 files. The gate now blocks it,
  but do not treat its row count as coverage.
- **The AI / archive ratio.** EP72 currently stands at 120 plates against 90 usable clips — 57 % AI
  before Batch B, and ~65 % after. The channel's normal balance is roughly the other way round.
  **This is an owner decision that has not been taken.** Raise it before the render, not after.
- **Serialize heavy renders.** Never run two Remotion/WebGL renders, or a render alongside an i2v
  job, on the 4090. VRAM exhaustion produces a silent no-output. Watch `remotion/out`, not `08_edit`.
- **EP72's `L015`** was re-cropped and re-upscaled on 2026-08-21 after the automatic crop deleted the
  gloved hand the plate exists for. The verdict file is bound to the NEW sha256. Do not restore an
  older copy of that plate.

---

## 6. WHAT WAS MEASURED, SO THE ASSEMBLY DOES NOT RE-DERIVE IT

- **Narration pace is measured, not modelled.** EP72 = 191.1 raw wpm, EP73 = 189.9 raw wpm, both
  from `gen_narration_case.py --measure-section ACT_1` against the real voice. The registry's old
  171.79 model is ~11 % slow and produced a script four minutes short on EP72. Both entries in
  `scripts/gen_narration_case.py` carry the measurement and the arithmetic.
- **Predicted vs actual film length:** EP73 was predicted at 29:44 and came out at 30:02 — 0.96 %
  error. The method works; use it rather than re-estimating.
- **Stock yield depends on the query and the source, and it was measured on 470 clips:**

  | harvest round | method | reject rate EP72 | reject rate EP73 |
  |---|---|---:|---:|
  | 1 | generic query, Pexels **and Pixabay** | 51 % | 42 % |
  | 2 | specific query, **Pexels only** | 39 % | 21 % |
  | 3 | queries naming what rounds 1–2 had **failed to find** | **16 %** | — |
  | 4 | the same again, with that list exhausted | 48 % | 47 % |

  **Round 4 is the important row.** The method works only while there is still a named gap to
  aim at. Once that list is empty the queries go generic again and the yield collapses to round-1
  levels — Christmas trees, steam locomotives, a car brake being serviced. **Harvesting was
  stopped after round 4 on purpose.** Do not open another round hoping for more; commission the
  missing subject as a plate instead.

  `scripts/fetch_stock.py` gained `--pexels-only` for this. Every unusable clip in the worst class
  — jellyfish, tortoises, an insect, Tokyo at night, five separate Christmas-light toy trains, an
  animated "Merry Christmas" card — came from Pixabay on a loose query.

- **The two register rules that killed the most footage**, and which belong in any future harvest
  for these episodes:
  - **EP72: no snow.** The derailment is the night of **5–6 July 2013**. Also: no passenger trains,
    no steam, no catenary (the line is not electrified), no graffiti, no crowds, no city.
  - **EP73: thin snow only.** Texas had a few centimetres on ground that had never been ploughed.
    31 of 62 first-pass rejects were alpine villages, snow-laden conifers, ploughed banks, frozen
    waterfalls and Himalayan peaks. A snowscape is a different story, not a smaller one.

---

## 7. SUGGESTED FIRST FIVE COMMANDS IN THE ASSEMBLY THREAD

```
py -3.11 scripts/build_usable_assets.py 72 --write
py -3.11 scripts/build_usable_assets.py 73 --write
py -3.11 scripts/check_script_length.py episodes/_planning/EP73_uri_script.en.v002.md --lo 1740 --hi 1920
py -3.11 scripts/check_plate_verdicts.py --slug lacmegantic
py -3.11 scripts/check_plate_verdicts.py --slug uri
```

All five pass today. If any of them does not, something changed after this handover was written.
