# EP65 · MARMET — ARCHIVE FOOTAGE PLAN v001

**Written 2026-08-10.** Episode `PD-2026-065-marmet`.
Script read: `EP65_marmet_script.en.v002.md` (highest revision).
Contract read: `episodes/PD-2026-065-marmet/episode_spec.v001.json` (`forbidden_subjects`,
`forbidden_claims`, `approved_deviations: ["factory_used"]`).
Shelf doctrine read: `docs/PD_ARCHIVE_SHELF_WORKLOG.v001.md`, `docs/PD_CANON.md` §10.

| | |
|---|---|
| Pool before | **7** clips |
| Floor (`factory_used`, ~1 per 45 s over a 29:23 film) | **~35** |
| Staged this session | **121** clips across **99** title queries |
| **Accepted after visual QC** | **57** |
| Margin over floor | **+22 (+63 %)** |
| Rejected this session (appended to the verdicts file) | **67** |
| Rejected entries in the verdicts file, total | **48 previous + 67 new = 115** |

`remotion/public/marmet/factory/` holds the 57. Every rejected clip is parked in
`remotion/public/marmet/factory_offtheme/` (113 files) so that
`stage_footage_by_title.py`, which excludes every id already sitting under
`remotion/public/*/factory*`, can never re-stage one. Nothing was deleted.

---

## 1. The premise EP65 shipped on was wrong

EP65 took an owner-approved deviation on `factory_used` on the ground that the shelf is thin.
Measured today with `scripts/shelf.py` (the single definition of the shelf — no `glob("*.jsonl")`
anywhere in this work):

```
shelf 151,869 items · 31,150 video
  pixabay        53,760   video  6,357
  pexels         34,905   video  9,398
  pixabay_extra  24,364   video 10,262
  nasa           11,409   video    630
  freesound       8,635   video      0
  wikimedia       5,569   video      0
  nara            3,600   video    814
  loc             3,092   video      0
  mixkit          2,158   video  2,158
  ia              1,422   video  1,422
  unsplash        1,027   video      0
  smithsonian       751   video      0
  noaa              530   video     41
  met               328   video      0
  sdxl              216   video      0
  coverr             68   video     68
  oyez               26   video      0
  courtlistener       9   video      0
```

Of those, **26,886 video rows are actually stageable** — usable licence, file present on disk,
1–120 MB, past the title blocklist. **8,373 clip ids were already consumed by other episodes**
when this session started (8,506 by the end; the EP62/63/64 threads are staging concurrently),
which is the real constraint on this pool, not shelf size.

**Lanes searched.** Every lane that holds video: `pexels`, `pixabay`, `pixabay_extra`, `mixkit`,
`ia`, `nara`, `nasa`, `coverr`, `noaa`. Searches ran over the whole shelf rather than per lane,
so all nine were queried by every one of the 99 queries. Two lanes named in the brief,
**`wikimedia` (5,569) and `loc` (3,092), contain zero video rows** — measured, not assumed; they
are stills and cannot contribute to a `factory_used` count. `nara` holds 814 video but 89 % of it
is below 720p, and none of it survived the 1920×1080 floor for this pool.

Where the 57 came from: **pexels 34 · pixabay_extra 18 · mixkit 5**. Licence on all 57 rows:
`free_commercial`.

---

## 2. Registers derived from the script

Read off `EP65_marmet_script.en.v002.md` rather than the brief, then matched to supplier
vocabulary.

| # | Register | Script line it serves |
|---|---|---|
| R1 | pen, ink, a hand writing on a ruled page | HOOK R001; ACT_1 motif states 2–4 (L44, L70, L86) |
| R2 | paper being handled across a table | ACT_1 L76 "What the record does describe closely is the paper"; L86 |
| R3 | files, binders, a drawer of tabs | ACT_1 L62 (ring binder, nothing filed behind the tab); ACT_2 L102 (the drawer closes on it) |
| R4 | shelved volumes, the record, a hand searching it | ACT_2 L104–L110; ACT_5 L321–L323 "greatly at sea without a chart or compass" |
| R5 | corridor, passage, threshold | the institution the paper was signed inside; ACT_4 L264 "the file went back to Charleston" |
| R6 | an empty chair; a wheelchair with nobody's face | ACT_1 L36 the second-chair plant; ENDING L373 |
| R7 | a window, rain on glass, flat late light | ACT_1 L60 "Now the part where the record stops"; ENDING L373 |
| R8 | institutional architecture, Washington | OP L26; ACT_3 L184–L216; ENDING L353 "an Act of Congress passed in 1925" |
| R9 | weather and season | 2009-08-25 → 2012-06-13. Five orders across three winters |
| R10 | roads through hills | ACT_1 L58 "all travelling to the state's highest court" |

Distribution of the 57 accepted clips: **R9 weather/season 17 · R8 architecture 8 · R10 roads 5 ·
R4 record/shelves 6 · R1 pen and writing 5 · R7 window/light 3 · R5 corridor/passage 4 ·
R2 paper handled 2 · R3 files 1 · R6 chair/wheelchair 2 · fog and water 4**.

---

## 3. Queries — including the ones that returned nothing, and what fixed them

The rule from the worklog holds: **a zero is a fact about the wording, not about the shelf.**
Counts are hits with a usable licence, present on disk, at ≥1920×1080, not already used by
another episode.

### 3.1 Zeroes that were a wording problem

| Query written as a director would | hits | Rewritten in supplier vocabulary | hits |
|---|---:|---|---:|
| `filing cabinet` | **0** | `binder office work paperwork` | 1 |
| `clipboard` | **0** | `a person pointing on a document` | 1 (rejected: legible policy heading) |
| `row of chairs` / `chairs in a row` | **0** | `historic amphitheatre with ornate ceiling` | 1 |
| `venetian` / `shutter` / `window frame` | **0** | `rain on window dark weather` | 1 |
| `archive room` | **0** | `alley shelves books library` | 1 |
| `handrail` | **0** | `modern urban underpass with curved railings` | 1 |
| `empty hallway`, `walking hallway`, `hallway` | 0 unused | `alley shelves books library`, `underpass`, `hallway alley building basement` | 3 |
| `wall clock`, `desk lamp`, `mailbox`, `signature paper`, `atrium`, `foyer`, `colonnade`, `tiled floor`, `auditorium`, `seating` | **0** | not needed once R4/R5/R7 were filled | — |

### 3.2 Zeroes that are real, and were confirmed as real

The film's central image is an admission counter. **It is not on this shelf**, and that is a
measured conclusion, not a first impression. Eighteen phrasings were tried:

```
reception desk 0 · front desk 0 · receptionist 0 · admission 0 · concierge 0 · service desk 0
help desk 0 · cashier 0 (3 hits, all sub-HD) · teller 0 (fortune tellers) · clerk 2 (parcel couriers)
check in 24 (medical check-ups and an airport) · checkout 1 (retail scanner) · queue 0
counter 16 (a coffee-shop counter, a juice stand, and twelve digital countdown timers)
lobby 0 unused · hotel lobby 0 · handing 2 (books, ballot papers) · bank interior 0
```

`counter` is the instructive one: 26 title hits, 16 of them HD and unused, and **twelve are
countdown-timer motion graphics** — the word means something else to this shelf. There is no
admission desk, no reception counter and no hand offering a pen across one.

**This does not need archive.** The design already commissions the counter as plates R225 and
R226 (`EP65_marmet_CODEX_BATCH_A.v001.md` §7), and the hand at the desk as R152 / R066 / R035 /
R038 / R064. The archive's job in this film is everything around that: the record, the corridor,
the weather, the institution. **No further searching is warranted for R-desk.**

### 3.3 Substring matching is a trap in this tool

`stage_footage_by_title.py` ANDs raw substrings against the title. Measured false-positive
counts:

```
form  → 177 hits, mostly "performing" and "platform"
ink   → 449 hits, mostly "thinking", "drinking", "sinking", "link"
lock  → 252 hits, mostly "clock", "blocks", "lockdown"
```

Single common words are unusable as queries here. Every one of the 99 queries that produced an
accepted clip was either a two-to-four-word phrase or a rare token.

### 3.4 How the queries were built

For each candidate clip identified by reading titles, the **shortest ANDed term set that selects
that one clip and nothing else** among the unused pool was solved for, then run with
`--per-query 1`. 80 of 104 first-round targets resolved to a unique query; the 24 that did not
are duplicate-title families (six identically-titled "living room, furniture, windows" clips,
three "ceiling lights inside a church", two "snow falling") and were taken with a group query at
`--per-query N`. **Every one of the four living-room clips turned out to be an architectural
render** — the tag-list title carried no warning, which is exactly why a group query has to be
looked at, tile by tile, before it is trusted.

---

## 4. What each accepted clip is for

`AR-` ids as staged in `remotion/public/marmet/factory/`.

### R1 — pen, ink, a hand on a ruled page (HOOK; ACT_1 L44 / L70 / L86)
| id | what it is |
|---|---|
| `AR-v_131992` | a ballpoint lying on a white sheet; a hand comes in and lifts it. The closest archive analogue of R001 and of motif state 2 (L44, the pen offered across the counter) |
| `AR-v_155023` | a hand writing in a spiral notebook, close, no face, the writing illegible — motif state 3, "It is not the shape of a name" (L70) |
| `AR-v_141435` | a man writing on a clipboard shot from directly above and behind; no face in any frame |
| `AR-v_10824` | a hand drawing on a blank ruled page — the bare line at the head of ACT_1 (L36) |
| `AR-v_100584` | a low-light still life: paper, a pen, an inkwell. "The ink dry" (L102) |

### R2 — paper handled across a table (ACT_1 L76, L86)
| id | what it is |
|---|---|
| `AR-7821854` | several hands over printed forms at a table, no faces, no legible heading — "a hand flattens each sheet against the table" (L86) |
| `AR-v_141280` | an open notebook and a pen on a table with nobody there — "From here to the end of the film the desk works with nobody at it" (L102) |

### R3 — files and the drawer (ACT_1 L62; ACT_2 L102)
| id | what it is |
|---|---|
| `AR-v_221506` | lever-arch files on a shelf, a hand pulling one out — the drawer of tabs closing on the form |

### R4 — the record (ACT_2 L104–L110; ACT_5 L321–L323)
| id | what it is |
|---|---|
| `AR-7841673` | a hand pulling a bound volume from a run of lettered spines. The closest thing on the shelf to a law report — ACT_2 "an extensive opinion with three holdings" |
| `AR-50726` | a hand running along book spines — "greatly at sea without a chart or compass" (L323) |
| `AR-4723` | hands turning pages, looking for one — ACT_4 "the state court had not addressed the question" (L232) |
| `AR-v_16359` | a hand on printed pages, warm light — the five pages read closely (OP L28–L30) |
| `AR-21593` | thick old stacked books in close detail — "the file" |
| `AR-21597` | a stack of books on a reading-room table, nobody there — "Both sides were now arguing about an empty file" (L270) |

### R5 — corridor, passage, threshold (the institution; ACT_4 L264)
| id | what it is |
|---|---|
| `AR-v_190162` | a long dark corridor with strip lights and a lit doorway at the end |
| `AR-5971048` | a bright multi-storey atrium, one distant unidentifiable figure |
| `AR-v_126966` | a library aisle receding past windows — corridor and record in one image |
| `AR-37798364` | a concrete ramp curving down out of frame — the passage between courts |
| `AR-v_123572` | a stone archway with the gate standing open, light on the path beyond — "the file went back to Charleston with a mandate in it" (L264) |

### R6 — the chair, the wheelchair (ACT_1 L36; ENDING L373)
| id | what it is |
|---|---|
| `AR-6343713` | an empty armchair with a cushion beside a bright window. Held; the second-chair plant |
| `AR-8400706` | an empty wheelchair pushed by a coat and two hands, no face — the register the spec measured at 43 clips and the batch deliberately left to archive |

### R7 — window, rain on glass, flat light (ACT_1 L60; ENDING L373)
| id | what it is |
|---|---|
| `AR-v_262125` | rain running down a large window from inside a dim room. The strongest single image in the pool for "Now the part where the record stops" |
| `AR-7292647` | a dark facade at night with two lit windows. "Almost everything a person would want to know is not in them" (OP L30) |
| `AR-36199319` | a glazed oval dome over an empty tiered hall — institutional ceiling, no people |

### R8 — institutional architecture, Washington (OP L26; ACT_3 L184–L216; ENDING L353)
| id | what it is |
|---|---|
| `AR-29188235` | the US Capitol from the lawn, bare trees — the Act of Congress of 1925 (L353) |
| `AR-29188252` | the Capitol from a street crossing, traffic — "The Supreme Court granted certiorari" (L184) |
| `AR-29188251` | the Library of Congress — the record in Washington |
| `AR-2872689` | a colonnaded marble hall, empty — the institution with nobody in it |
| `AR-8639227` | an ornate municipal facade from a low angle — the circuit court |
| `AR-2958504` | a street beside a government building with a flag on a pole |
| `AR-2017` | a heavy stone building on a city corner at night — Charleston after hours |
| `AR-v_35688` | a town in a valley under fog at dawn |

### R9 — weather and season, 2009 → 2012 (five orders, three winters)
`AR-6527135` snow at a streetlamp · `AR-10716927` snow on a forest path · `AR-35968579` a fenced
walkway under snow · `AR-31807897` frost on branches at sunrise · `AR-v_108697` bare trees against
a winter sky · `AR-4031697` rain on dark pavement · `AR-6470927` rain in a night road ·
`AR-16834480` a wet street reflecting a building · `AR-34322674` cloud forming over an overcast
sky · `AR-34539583` an overcast sky with birds · `AR-3786014` a dark cloudy sky in timelapse ·
`AR-4352239` cloud moving in timelapse · `AR-6508285` cloud in timelapse, cold cast ·
`AR-6546062` sunrise through cloud over bare trees · `AR-v_210983` cloud over hills at dusk ·
`AR-v_217623` storm cloud with rain falling over a valley · `AR-v_224934` cloud over a city at
last light · `AR-v_134510` sun passing behind cumulus.

Placed on the dated beats: 2009-08-25 (L46), 2009-09-29 (L52), 2010-06-02 (L56), 2011-06-29
(L104), 2012-02-21 (L184), 2012-04-03 (L266), 2012-06-06 and 2012-06-13 (L272, L278).

### R10 — roads through hills (ACT_1 L58; ACT_4 L264)
`AR-28201392` cloud rolling across a mountain highway · `AR-26081682` a road through a frosted
landscape · `AR-26081787` a road running through a farmed valley · `AR-33428342` a wet mountain
road under low cloud · `AR-10863232` a flat road under heavy cloud.

### Fog and water — the record that is not there
`AR-12388130` a foggy morning on flat water · `AR-5541847` a fogged river.
For L66 "That is the whole account", and L68 "No ages. No conditions."

---

## 5. Visual QC — what was actually looked at

Two passes. **Both were read tile by tile; neither was sampled.**

1. **Subject pass, 6 sheets, 105 tiles**, one frame per clip —
   `runs/qc/marmet_factory_v002/factory_footage_contact_01..06.png`
2. **Face and content pass, 16 sheets, 300 tiles**, 3–4 frames per clip spread across each clip's
   duration — `runs/qc/marmet_factory_v002_multiframe/frames_footage_contact_01..13.png` and
   `runs/qc/marmet_factory_v002_multiframe_b/frames2_footage_contact_01..03.png`

**The second pass is not optional, and this pool proves it.** `AR-8297995`
("woman looking at papers") passed the subject sheet cleanly: its first second is a hand and a
folder with no person in shot. At 38 %, 64 % and 88 % of the clip a woman is at the desk with her
face sharp and identifiable. A one-frame sheet accepts it. That is the same shape of failure as
`AR-10159563`, the clip that reached the scheduling command inside a finished render.

`scripts/check_pool_faces.py` was run over the whole pool
(`runs/qc/marmet_pool_faces.v002.json`, 105 clips × 8 frames × 4 cascades). **It is recorded as a
pointer, never as a filter.** Its top scores include a cloud timelapse at 24.9 % "face" and a
snow-covered footpath at 36.5 %; Haar cascades fire on foliage and cloud texture. Its own
docstring says a detection is not a verdict, and this run is the evidence for that. It was used
to decide where to look, and the eye decided.

**Resolution was measured on the staged files, not read out of the index.** `ffprobe` on all 106
found exactly one sub-1920×1080 clip (`AR-8523701`, 1280×720). The index
`_ledger/video_resolution.json` is keyed `source:id` and **ledger ids collide across sources** —
it reported mixkit's `AR-4723` as 1280×720 because pixabay also has an item `4723`. The same
collision put a wrong title into the staging receipt; both are corrected, and the receipt now
matches rows on the id **and** the title slug baked into the staged filename.

---

## 6. Rejections — 67 this session, by cause

Every one is written into `runs/qc/marmet_clip_verdicts.v001.json` with its own reason. **The 48
verdicts already in that file were not touched and none of those clips was re-staged** — the
append refuses to overwrite an existing key.

| cause | n | notes |
|---:|---:|---|
| CG, archviz render, green screen, motion graphic | 20 | almost all `pixabay_extra`, whose tag-list titles never say "render". All four "living room, furniture, windows" clips; the "stamp ink wood handle" that is a 3D object on black; "frame blank empty paper notebook" that is a CG shelving unit with no paper in it |
| wrong subject or wrong institution | 14 | a cathedral; two church interiors; a conference room set with EU and Norwegian flags; an embassy facade; a graffitied underpass; a Christmas-decorated bistro; an airport travelator carrying advertising screens; a wildfire plume; a warehouse of shrink-wrapped pallets |
| **real identifiable person** | 13 | including `AR-8297995` (found only on the multi-frame pass) and `AR-4747`, a 26.2 %-of-frame face that was **inside the shipped seven-clip pool** and had never been re-judged |
| readable text on a document, or third-party branding | 8 | HOME INSURANCE POLICY; CONTRACT; LEASE AGREEMENT; scrabble tiles spelling CONTRACT; AMERICA ONLINE on a CRT; a green-screen stamp reading SOLD; Spanish and Cyrillic book titles filling frame |
| duplicate shoot or register saturation | 10 | two further angles on the same Paris hall; a second night-streetlamp snow clip; a second still life from the same set-up; a third mountain valley; three more walls of colourful paperbacks on top of the seven book clips already kept |
| near-black plate | 1 | snow specks on black; as a cut it reads as a dead frame |
| below 1920×1080 | 1 | `AR-8523701`, measured by ffprobe |

### Two judgement calls worth flagging to the owner

- **`AR-v_131012` (elevator interior) was withdrawn from the shipped pool.** The picture is fine
  and it served a register the spec measured. But its shelf row was **purged on 2026-08-08 with
  reason `owner verdict: unusable`** (theme `decision_rooms` × source `pixabay_extra`), confirmed
  in `_ledger/absent_index.json`. An owner unusable verdict outranks every machine signal
  (`PD_CANON` §10), and the staged copy is the only reason this clip survived the purge at all.
- **Identifiable named buildings were kept where the script names the institution and refused
  where it does not.** The US Capitol and the Library of Congress are kept: the script's own words
  are "an Act of Congress passed in 1925" and "the Supreme Court of the United States", so the
  picture means what the sentence means. The Texas state capitol was refused — standing in for
  West Virginia's highest court it is a meaning mismatch — and the "capitol" clip dominated by a
  statue of an identifiable real man was refused under invariant 11. `forbidden_subjects` bars
  "any real building … identifiable by signage or architecture"; read absolutely it would also bar
  the courthouse exterior the brief asks for, so it is read as barring buildings that would be
  taken for *the* institution in this case. **Flagging the reading rather than deciding it
  silently.**

---

## 7. Mechanism added

`AR-10159563` — the real person, age indeterminate, that reached the scheduling command — **was
not in `config/footage_blocklist.v001.json`.** It had been "handled" by deleting the staged copy
from marmet, which protects marmet and nothing else: the shelf row is live and any other
episode's query can stage it again tomorrow. It is now entry 22 in that file under
`cat2_real_identifiable_minor`, and the guard was demonstrated firing:

```
pd_footage_blocklist.reason_for("…/AR-10159563__woman_sitting_on_a_chair…mp4")
  -> real_person_age_indeterminate_marmet (global): …
pd_footage_blocklist.reason_for("…/AR-v_155023__to_write_hand_ballpoint…mp4")
  -> None
```

`build_case_film_generic.py` refuses to emit a film naming a blocked clip, so this now holds for
every episode, not just this one. The gym-chairs clip `AR-5712753` is deliberately **not** added:
the existing verdict records it as "not a safety issue", and this file is hard findings only.

---

## 8. Artefacts

| path | what |
|---|---|
| `remotion/public/marmet/factory/` | **57 accepted clips** |
| `remotion/public/marmet/factory_offtheme/` | 113 rejected clips, parked so no query can re-stage them |
| `runs/qc/marmet_title_staging.v001.json` | consolidated staging receipt, all 57, with source, licence, source_url and sha256 |
| `runs/qc/marmet_title_staging.v001.json.bak_pre_restage_20260810` | the previous per-run receipt |
| `runs/qc/marmet_clip_verdicts.v001.json` | 115 rejections (48 previous + 67 new), 22 sheets listed under `reviewed_sheets` |
| `runs/qc/marmet_clip_verdicts.v001.json.bak_pre_append_20260810` | pre-append backup |
| `runs/qc/marmet_pool_faces.v002.json` | machine face sweep, pointer only |
| `runs/qc/marmet_factory_v002/` | 6 subject sheets |
| `runs/qc/marmet_factory_v002_multiframe/` | 13 multi-frame sheets |
| `runs/qc/marmet_factory_v002_multiframe_b/` | 3 multi-frame sheets, top-up batch |
| `episodes/PD-2026-065-marmet/05_visuals/factory_clip_qc.v001.json` | 57 clips, written by `write_factory_clip_qc.py --slug marmet` |
| `config/footage_blocklist.v001.json` | +1 entry (§7); backup `.bak_20260810_marmet` |

Not touched, by instruction: `manifest.json`, `film.json`, and no render was started.

## 9. For whoever assembles this

- The pool is **57**, over the ~35 floor. `approved_deviations: ["factory_used"]` in
  `episode_spec.v001.json` is now **unnecessary** and should be removed when the spec is next
  revised, so the gate measures this episode honestly.
- `footage_diversity` wants distinct ≥ 0.40 and reuse ≤ 4 per clip. At 57 clips over a 29:23 film
  at `target_cut_sec` 3.7 the film needs roughly 480 cuts, so archive can carry about 230 of them
  at ≤ 4 uses each. Weather and architecture are the deep registers (17 and 8); R2 paper and
  R3 files are the shallow ones (2 and 1) and must not be leaned on.
- **The admission counter, the ruled line and the hand at the desk are commissioned plates, not
  archive** — R225, R226, R152, R066, R035, R038, R064. §3.2 shows the archive has no counter
  under any of eighteen phrasings, so do not send anyone back to look for one.
- Four clips are deliberately dark (`AR-7292647`, `AR-v_190162`, `AR-4031697`, `AR-6470927`).
  They carry visible content, but if `pd_postrender_gate` reports black frames, look at these
  first before assuming a render fault.
