# EP69 · THE KANSAS CITY HYATT REGENCY WALKWAYS — FOOTAGE QUERY PLAN v001

**Date 2026-08-11 · slug `hyatt` · episode `PD-2026-069-hyatt`**
**Contract `episodes/PD-2026-069-hyatt/episode_spec.v001.json` — `distinct_video_assets` **236**,
`target_cut_sec` **3.6**, `runtime_seconds` **[1560, 1895]**, `footage_review_required` **true**,
58 `forbidden_subjects`, `era_setting` **Kansas City, Missouri, USA, 1978–1988**.**
**Design `EP69_hyatt_FILM_BIBLE.v001.md` · front `EP69_hyatt_PACKAGING.v001.md` ·
facts `EP69_hyatt_FACTS_LEDGER.v001.md` (§12 fixes what the film shows instead of what it may not).**

> **Nothing here was staged, copied, transcoded or ffprobed.** Every number below was produced by
> reading the rights ledger and the resolution index in two passes, while a long-form render held
> the machine. No clip was moved and no media file was opened.

---

## 0. Result in one block

```
contract distinct_video_assets                           236
clip floor, runtime_lo // 45  (check_final_acceptance)    34     -> not binding
channel target                                            60     -> not binding
video cuts this film has room for (see s5)               320
queries asked, over two rounds                           663
round-1 zeros, every one re-asked in >=3 other words       85
retry queries asked in round 2                           340
sum of the 20 register unions (what the gate counts)  14,747
clip ids already held by some episode's factory*       9,780     <- already subtracted everywhere
```

**The shelf is not the binding constraint on the volume of this episode.** 14,747 screened clips
against 250 required is a factor of 59. The binding constraints are three, and none of them is
volume:

1. **This film happens on a drawing board, on a bench, and inside a room that must never appear.**
   `threaded rod`, `fastener`, `wrench`, `workbench`, `blueprint`, `drafting table`, `ballroom`,
   `atrium`, `lobby`, `courthouse` and `typewriter` all return **0 usable clips** after two rounds
   of retries (§3). Those are precisely this story's objects.
2. **Everything the archive is rich in, this film's `era_setting` rejects.** The steel, welding and
   construction registers on the shelf are dominated by 2015–2024 footage: cordless tools, hi-vis
   PPE, LED site lamps, flat-panel monitors. The episode is **1978–1988**. **No machine gate
   measures a decade** — `check_pool_frames.py` surfaces suspects for human attention and nothing
   more — so period plausibility is the single most likely failure in this pool.
3. **Sixty-eight previous episodes have already eaten the obvious clips.** 9,780 ids are held by
   some episode's `factory*` folder and are excluded from every count here by construction.

---

## 1. The instrument, verified before any zero was trusted

The counts in §4 were produced by **replicating `scripts/stage_footage_by_title.py`'s own
selection** over one pass of the ledger instead of 663 passes. Not a second search implementation:
the measuring script imports that module and uses *its* `ledger_rows()`, *its* `OK_LICENSE`, *its*
`TITLE_BLOCK` and `RIP_SIGNATURE` regexes and *its* `slugify()`, plus
`search_archive.load_video_resolution()`, so every row it counts is a clip the staging tool would
really take. The scripts are `measure_hyatt.py`, `measure_hyatt_r2.py` and `report_hyatt.py` in this
session's scratchpad.

A clip is counted only if **all** of these hold, in this order:

| # | Filter | Where it comes from |
|---|---|---|
| 1 | file extension in `.mp4 .mov .webm .mkv` | `stage_footage_by_title.VIDEO_EXT` |
| 2 | `license_decision` in `free_commercial / pd / cc0` | `OK_LICENSE` |
| 3 | title non-empty and not matching `TITLE_BLOCK` (cartoon, 3d render, christmas, logo, game…) | same module |
| 4 | id + path + title not matching `RIP_SIGNATURE` (y2mate, savefrom, ytdlp…) | same module — a CC0 tag on a ripped upload is the uploader's word, not proof |
| 5 | **every term of the query is a substring of the lowercased TITLE** | the staging tool's match, which is title-only |
| 6 | the file exists on disk and is 1–120 MB | same module |
| 7 | `AR-<slugified id>` is **not** already in any `remotion/public/*/factory*` folder | the cross-episode de-dup, `stage_footage_by_title.py` lines 85–90 |
| 8 | `video_resolution.json` says **w ≥ 1920 and h ≥ 1080** | `search_archive.load_video_resolution` — the ledgers carry no width or height |

**Cross-episode reuse is therefore already subtracted from every number in this document** (owner
complaint 「素材の被り」, gate `footage_diversity`). Nothing here is a clip another episode holds.

**The instrument lied once, on its first run, and the lie was silent.** Every one of the twenty
registers came back **union 0** — 323 queries, not a single hit. That reads as "the shelf has
nothing for this episode", which would have been a false and expensive conclusion. The cause was
filter 8: `load_video_resolution()` is keyed by **`source:id`**, not by file path, and the first
version of the measuring script looked up the path. Fixing the key produced 12,572 in round 1.
**A zero from a new instrument is a fact about the instrument until the instrument has produced a
non-zero.** That is written here because it is the same failure family as `kill -0` and the
self-matching search in `docs/PD_RETRO_20260805_UNPAUSE.v001.md`.

Any single row reproduces with the canonical instrument, whose count is a little **wider**, because
its CLI ANDs against title + id + matched keywords + theme + filename rather than title alone, and
it does not apply the resolution or cross-episode screens:

```bash
py -3.11 scripts/search_archive.py threaded rod --kind video --limit 50
py -3.11 scripts/search_archive.py --shot "threaded steel rod nut washer on a bench" --kind video --limit 25
```

**One honest caveat.** The `9,780 ids already staged` figure is a snapshot: EP67 read 9,068 on
2026-08-11 and this pass reads 9,780, because staging jobs consume ids continuously. The counts
below are a **lower bound taken at 2026-08-11**, and they will only go down. Re-measure before
staging if more than a day passes.

---

## 2. The registers, and how many cuts each one owes

Twenty registers, derived from this film's own sections and from the ledger's §12 list of what real
footage is allowed at all, rather than from a generic list. Cut counts sum to **320**, which is the
video-cut budget computed in §5.

| # | register | what it is for in THIS film | cuts | script beats it serves |
|---|---|---|---:|---|
| R1 | steel fabrication, welding | Havens' shop. The seam that closes the box beam | 22 | ACT_1 the box beam; ACT_2 the fabricator |
| R2 | threaded rod, nut, washer, bench | **the film's own object.** H1 lives here | 26 | HOOK; ACT_1 the connection; ENDING |
| R3 | test frame, gauge, measuring | the NBS test series that pulled the connection apart | 12 | ACT_4 the 18.6 kips |
| R4 | drafting, drawing, pencil | 1978–79. The board where the detail was drawn | 24 | ACT_1 throughout; ACT_2 the shop drawings |
| R5 | blueprint, rolled paper, flat file | drawing S405.1 as an object, never as a readable page | 18 | ACT_2 the review chain; ACT_5 the 442 pages |
| R6 | ballroom, dance floor, band | the tea dance, **empty**, before anybody arrives | 16 | ACT_3 the evening |
| R7 | atrium, hotel interior, walkway | a room of that shape that is **not** the Hyatt | 18 | ACT_1 the atrium; ACT_3 the empty-room sequence |
| R8 | Kansas City, midwest city exterior | the city, 1981, from outside | 16 | ACT_1 opening; ACT_3; ACT_5 the board |
| R9 | steel stock, beam, channel, yard | what a box beam is made of, before it is one | 20 | ACT_1; ACT_2 |
| R10 | construction site, 1979 | fast-track. The building going up around the drawings | 20 | ACT_2 fast-track; ACT_3 the October roof |
| R11 | hands, backs, figures | **the people lane.** Human presence with no identifiable face | 22 | throughout; see §7 |
| R12 | empty room, corridor, doorway | the hearing room, the office, the room after | 18 | ACT_5; ENDING |
| R13 | clock, calendar, time passing | 1979 → 1981 → 1984 → 1986 → 1988 | 10 | act transitions ×5 |
| R14 | civic stone, columns, marble | the Board, the Commission, the Court of Appeals — exteriors only | 16 | ACT_5 |
| R15 | weather, dusk, quiet | the four designed silences | 12 | ACT_3 after the black; ENDING |
| R16 | paper records, typing, files | 442 pages, 180 findings, the report | 14 | ACT_4; ACT_5 |
| R17 | crane, lifting, chain, cable | the heavy crane at 8:30 p.m., **arriving, never working over debris** | 12 | ACT_3 the timeline |
| R18 | light, shadow, dark, macro | the black between beats; the surface of steel | 6 | transitions; H1 backgrounds |
| R19 | vintage film, 1970s–80s texture | period grade reference, used as texture only | 4 | act transitions |
| R20 | engineering office, model, lamp | the firm. Never a named building | 14 | ACT_2; ACT_5 |
|  | **total** |  | **320** | |

**Hard constraint that binds every register.** `check_spec_satisfied.py` matches
`forbidden_subjects` word-wise **against the source filename**, so a clip whose title carries
`collapse`, `rubble`, `debris`, `wreckage`, `rescue`, `ambulance`, `hospital`, `firefighter`,
`victim`, `disaster`, `blood`, `injured`, `police`, `gavel`, `scales`, `hourglass`, `handshake`,
`drone`, `child`, `wedding`, `beach` or **`hyatt`** is an automatic build failure. **That is not a
mistake in the contract — it is the point.** This is a film about 114 people killed by a structural
failure; a stock clip whose own title says `collapse` or `rescue` cut anywhere near this narration
is the exact thing the ledger's §11b forbids, and it is also the thing a tired builder reaches for.
`hyatt` is on the list so that no clip claiming to be the building can enter the pool at all.

---

## 3. The zeros, and the retries that were run before any of them was written down as a gap

**Round 1 asked 323 queries and produced 85 zeros. Round 2 re-asked every zero-producing term in
different words — 340 further queries, at least three per zero — before a single gap was recorded.**
A zero is a fact about the words until it has been asked at least three other ways. The measured
wins:

| director's phrasing | usable | supplier phrasing that worked | usable |
|---|---:|---|---:|
| `steel factory` · `steel mill` · `cutting steel` · `steel worker` | **0** | `plant` **89** · `factory` **60** · `mill` **24** · `manufacturing` **21** | 226 round-2 union |
| `threaded rod` · `fastener` · `wrench` · `spanner` · `workbench` · `tool bench` · `machine part` · `gear metal` · `rusty bolt` · `iron rod` · `steel rod` · `nut bolt` | **0** | `machine` **66** · `rod` **54** · `iron` **33** · `nut` **27** · `spiral` **26** · `craft` **25** · `repair` **20** · `nail` **18** | 354 round-2 union |
| `dial` · `micrometer` · `caliper` · `scientific` · `engineering test` | **0** | `science` **125** · `lab` **39** · `breaking` **14** · `precision` **5** | 193 round-2 union |
| `draft` · `blueprint` · `technical drawing` · `compass drawing` · `paper pencil` | **0** | `architect` **424** · `pen` **177** · `geometry` **13** · `architectural` **8** · `graph paper` **7** | 86 round-2 union |
| `documents` · `folder` | **0** | `paper` **433** · `plan` **189** · `map` **71** · `document` **8** | 28 round-2 union |
| `ballroom` · `ball room` · `banquet` · `orchestra` · `saxophone` · `chairs row` · `empty hall` | **0** | `empty` **92** · `dancing` **54** · `band` **54** · `horn` **29** · `musician` **6** | 157 round-2 union |
| `lobby` · `atrium` · `reception` · `skylight` · `balcony` · `mezzanine` · `elevator` · `foyer` · `entrance hall` · `courtyard` · `gallery` | **0** | `corridor` **34** · `check in` **24** · `escalator` **23** · `hotel` **13** · `hall` **13** · `lift` **12** · `terrace` **9** | 55 round-2 union |
| `courthouse` · `columns` · `stone building` · `classical building` · `pillar` | **0** | `architecture` **408** · `temple` **130** · `stone` **82** · `dome` **26** · `court` **14** | 215 round-2 union |
| `typewriter` · `old typwriter` · `type writer` · `stack paper` · `paper stack` · `archive` · `shelves` | **0** | `sign` **270** · `office` **141** · `typing` **46** · `records` **2** | 16 round-2 union |
| `8mm` · `super 8` · `film grain` · `film reel` · `celluloid` · `archival` · `1980s` · `80s` · `1970s` | **0** | `cine` **62** · `vintage` **44** · `black and white` **37** · `retro` **34** · `past` **31** · `old footage` **16** | 149 round-2 union |
| `drafting table` · `scale model` · `blueprint desk` · `desk lamp` | **0** | `model` **44** · `study` **34** · `office desk` **25** · `miniature` **5** · `drawing table` **2** | 69 round-2 union |
| `grey sky` | **0** | `cloudy` **53** · `overcast` **2** | 2 round-2 union |
| `hoist` · `pulley` · `winch` · `rigging` · `crane hook` · `excavator arm` · `digger` | **0** | `rope` **133** · `truck` **68** · `rig` **60** · `crane` **52** · `wire` **47** · `chain` **40** | 253 round-2 union |
| `hard hat` · `scaffold` · `scaffolding` · `renovation` | **0** | `construction` **145** · `works` **75** · `temporary structure` **49** · `repair building` **14** | 158 round-2 union |

Six of those rows are worth reading twice, because **a hit count is not a supply count** and five of
these numbers are lies about what is in the frame:

- **`plant` 89, in a steel register, is mostly botany.** The top real titles behind it are
  *indoor plants at the office* and *close up view of green plants against rays of sunlight*.
  Substring matching does not know the difference between a plant and a plant.
- **`rig` 60, in a crane register, is almost entirely the word "bright".** *bright lens flare in
  dark abstract background*, *the brightness of the sun in the sky*. Not one of the top three is
  rigging.
- **`nut` 27 is doughnuts, almonds and "one minute".** *police officers eating doughnuts in car*
  is the top hit, and `police` is a `forbidden_subject`, so it is blocked anyway.
- **`cine` 62 is "medicine" and "cinematic".** *lab laboratory medical medicine* scores here.
- **`architect` 424 is "architecture"**, and the architecture on this shelf is European civic and
  religious — the same pool that gives `temple` 130. It is not a drawing board.
- **`empty` 92, in the ballroom register, is offices and jails**: *an empty office*, *empty jail*.
  `jail` is a `forbidden_subject`.

**That is why the screened figure and the union figure are different things, and why
`footage_review_required` is true.** The union is the number of clips a person has to look at. It is
not the number that will survive looking.

### The six real gaps, and what fills them

| gap | measured | filled by |
|---|---|---|
| **a 1¼-inch threaded rod, a nut and a washer on a bench** | `threaded rod`, `fastener`, `wrench`, `workbench`, `tool bench` all 0 usable | **generated plates + 3D.** This is hero object **H1** and it is the first and last shot of the film. It cannot be approximated by a clip of a machine part |
| **a drawing board with a pencil, 1978** | `draft`, `blueprint`, `technical drawing`, `drafting table`, `blueprint desk` all 0 usable; `architect` 424 is European architecture | **generated plates.** Thumbnail variant 3 and the whole ACT_1 register |
| **a ballroom or dance floor with nobody in it** | `ballroom`, `ball room`, `banquet`, `empty hall` all 0 usable; `empty` 92 is offices | **generated plates.** The ledger's §12 substitution for the tea dance depends entirely on this shot existing |
| **an atrium of that shape that is not the Hyatt** | `atrium`, `lobby`, `foyer`, `mezzanine`, `skylight` all 0 usable | **generated plates**, used three times as the same plate at 3:00, 4:30 and 7:00. Archive `escalator` / `corridor` / `check in` supply approach and scale only |
| **an American courthouse or hearing room, exterior** | `courthouse`, `columns`, `stone building` all 0 usable; `architecture` 408 and `temple` 130 are the wrong continent and the wrong function | **generated plates** for ACT_5, plus archive `stone` / `dome` for texture. **No courtroom interior at all** (§6) |
| **1970s–80s period texture** | `8mm`, `super 8`, `film grain`, `1980s`, `1970s`, `archival` all 0 usable | **grade, not footage.** R19 owes only 4 cuts and they are texture overlays; the period is carried by the generated plates' art direction, not by found film |

---

## 4. The queries, verbatim, with measured hit counts

663 queries over 20 registers, both rounds merged. `title-AND` = ledger rows whose title contains
every term. `usable` = of those, the rows that survive **all eight** filters in s1 — licence,
title-block, rip-signature, on-disk, 1-120 MB, not already staged by another episode, and
>= 1920x1080. `union` on each heading is the count of **distinct** clip ids in the usable column
across that register's queries, both rounds; it is not the column sum, because one clip answers
several queries. Only the ten highest-yield queries per register are tabulated; the full 663 are in
`measure_hyatt.py` and `measure_hyatt_r2.py`.

**A hit count is not a supply count.** Read the three real titles under each heading before
believing the number above it. s3 lists the five registers where the number is actively misleading.

### R1_steel_fabrication_welding   union 257
32 queries over two rounds (16 round 1, 16 retries), 4 round-1 zeros, 9 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *sparks from burning flame* / *man cutting metal with angle grinder* / *women working at weaving factory*

| query | title-AND | usable |
|---|---:|---:|
| `plant` | 256 | **89** |
| `factory` | 153 | **60** |
| `mill` | 69 | **24** |
| `sparks` | 44 | **23** |
| `manufacturing` | 52 | **21** |
| `industry` | 112 | **16** |
| `saw` | 29 | **11** |
| `metal work` | 32 | **7** |
| `weld` | 36 | **6** |
| `cutting` | 29 | **6** |

### R2_threaded_rod_nut_washer   union 371
67 queries over two rounds (19 round 1, 48 retries), 12 round-1 zeros, 22 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *unrecognizable people riding on skateboards* / *technician looking at tool box* / *fire engine at winter night*

| query | title-AND | usable |
|---|---:|---:|
| `machine` | 280 | **66** |
| `rod` | 167 | **54** |
| `iron` | 129 | **33** |
| `nut` | 133 | **27** |
| `spiral` | 48 | **26** |
| `craft` | 119 | **25** |
| `repair` | 45 | **20** |
| `engine` | 79 | **19** |
| `nail` | 33 | **18** |
| `mechanic` | 44 | **13** |

### R3_test_frame_gauge_measure   union 286
36 queries over two rounds (16 round 1, 20 retries), 5 round-1 zeros, 15 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *a woman working with modern science technology* / *protesters on the street* / *breaking waves on a sandy beach under a stormy sky*

| query | title-AND | usable |
|---|---:|---:|
| `science` | 279 | **125** |
| `test` | 167 | **67** |
| `lab` | 268 | **39** |
| `meter` | 69 | **15** |
| `laboratory` | 113 | **14** |
| `breaking` | 33 | **14** |
| `research` | 47 | **11** |
| `experiment` | 32 | **8** |
| `pressure` | 9 | **5** |
| `precision` | 6 | **5** |

### R4_drafting_drawing_pencil   union 682
36 queries over two rounds (16 round 1, 20 retries), 5 round-1 zeros, 15 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *girl looking through window blowing on it and drawing* / *close up on hands opening wallet and showing cards* / *close up on pencils on tax sheet*

| query | title-AND | usable |
|---|---:|---:|
| `architect` | 658 | **424** |
| `pen` | 577 | **177** |
| `artist` | 40 | **21** |
| `draw` | 110 | **15** |
| `drawing` | 88 | **14** |
| `geometry` | 23 | **13** |
| `notebook` | 66 | **11** |
| `illustration` | 17 | **10** |
| `architectural` | 13 | **8** |
| `graph paper` | 38 | **7** |

### R5_blueprint_rolls_flat_file   union 788
28 queries over two rounds (16 round 1, 12 retries), 3 round-1 zeros, 7 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *cropland* / *woman scrolling social media* / *airplanes on airport runway at night*

| query | title-AND | usable |
|---|---:|---:|
| `paper` | 1013 | **433** |
| `plan` | 515 | **189** |
| `map` | 103 | **71** |
| `print` | 113 | **38** |
| `chart` | 94 | **27** |
| `scroll` | 40 | **13** |
| `document` | 111 | **8** |
| `file` | 28 | **8** |
| `architectural` | 13 | **8** |
| `old paper` | 33 | **5** |

### R6_ballroom_dance_band   union 346
36 queries over two rounds (16 round 1, 20 retries), 5 round-1 zeros, 15 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *man singing at concert* / *drunken man dancing in red light* / *people dancing in illuminated room*

| query | title-AND | usable |
|---|---:|---:|
| `empty` | 288 | **92** |
| `dancing` | 106 | **54** |
| `band` | 275 | **54** |
| `dance` | 105 | **35** |
| `music` | 177 | **32** |
| `horn` | 46 | **29** |
| `party` | 91 | **27** |
| `stage` | 81 | **26** |
| `guitar` | 37 | **22** |
| `concert` | 48 | **16** |

### R7_atrium_hotel_lobby   union 150
44 queries over two rounds (16 round 1, 28 retries), 7 round-1 zeros, 24 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *time lapse of people on escalators* / *escalator on railway station* / *a walkway with graffiti on it and a fence*

| query | title-AND | usable |
|---|---:|---:|
| `corridor` | 86 | **34** |
| `check in` | 49 | **24** |
| `escalator` | 43 | **23** |
| `hotel` | 33 | **13** |
| `hall` | 118 | **13** |
| `lift` | 61 | **12** |
| `terrace` | 15 | **9** |
| `stairs` | 45 | **7** |
| `walkway` | 14 | **7** |
| `glass wall` | 11 | **3** |

### R8_kansas_city_midwest_exterior   union 1034
24 queries over two rounds (16 round 1, 8 retries), 2 round-1 zeros, 5 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *bus driving in city at night* / *bird s eye view of a road in a town* / *aerial shot of city in winter*

| query | title-AND | usable |
|---|---:|---:|
| `street` | 730 | **350** |
| `highway` | 354 | **184** |
| `city street` | 305 | **170** |
| `cityscape` | 213 | **129** |
| `skyline` | 185 | **126** |
| `town` | 276 | **125** |
| `aerial city` | 200 | **107** |
| `us city` | 249 | **105** |
| `city skyline` | 116 | **82** |
| `america` | 169 | **77** |

### R9_steel_stock_yard_beam   union 463
36 queries over two rounds (16 round 1, 20 retries), 5 round-1 zeros, 14 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *pipette with red substance* / *man cutting metal with angle grinder* / *subscribe animation on newsaper scrapes*

| query | title-AND | usable |
|---|---:|---:|
| `yard` | 194 | **126** |
| `scrap` | 158 | **91** |
| `metal` | 277 | **48** |
| `tube` | 175 | **48** |
| `industrial` | 157 | **36** |
| `iron` | 129 | **33** |
| `beam` | 55 | **26** |
| `i beam` | 54 | **25** |
| `duct` | 99 | **19** |
| `platform` | 27 | **12** |

### R10_construction_site_1979   union 315
28 queries over two rounds (16 round 1, 12 retries), 3 round-1 zeros, 6 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *fireworks exploding in sky at night* / *fireworks on sky at night* / *clouds over harbor cranes*

| query | title-AND | usable |
|---|---:|---:|
| `construction` | 262 | **145** |
| `works` | 158 | **75** |
| `crane` | 81 | **52** |
| `temporary structure` | 49 | **49** |
| `excavator` | 76 | **36** |
| `site` | 80 | **21** |
| `repair building` | 18 | **14** |
| `platform` | 27 | **12** |
| `concrete` | 40 | **10** |
| `builder` | 18 | **7** |

### R11_hands_backs_people   union 873
16 queries over two rounds (16 round 1, 0 retries), 0 round-1 zeros, 0 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *a man walking on the road* / *man filming a woman while walking* / *a man walking while filming a woman*

| query | title-AND | usable |
|---|---:|---:|
| `people` | 881 | **410** |
| `hand` | 824 | **237** |
| `hands` | 377 | **149** |
| `man walking` | 250 | **97** |
| `worker` | 240 | **89** |
| `people walking` | 118 | **57** |
| `man hand` | 177 | **51** |
| `man working` | 74 | **32** |
| `woman walking` | 66 | **30** |
| `crowd` | 126 | **29** |

### R12_empty_room_corridor   union 1061
28 queries over two rounds (16 round 1, 12 retries), 3 round-1 zeros, 9 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *a paramedic closing the back door of an ambulance vehicle* / *a person holding a developing tank in a darkroom* / *a person developing film in a darkroom*

| query | title-AND | usable |
|---|---:|---:|
| `wall` | 872 | **449** |
| `door` | 481 | **171** |
| `table` | 514 | **130** |
| `room` | 451 | **105** |
| `tunnel` | 150 | **91** |
| `floor` | 116 | **58** |
| `abandoned` | 241 | **43** |
| `desk` | 197 | **39** |
| `corridor` | 86 | **34** |
| `window room` | 83 | **10** |

### R13_clock_calendar_time   union 1631
28 queries over two rounds (16 round 1, 12 retries), 3 round-1 zeros, 8 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *time lapse of clouds in grayscale* / *sky at sunset and night* / *time lapse of blue sky and clouds*

| query | title-AND | usable |
|---|---:|---:|
| `sunset` | 976 | **553** |
| `time` | 924 | **395** |
| `sunrise` | 449 | **162** |
| `summer` | 385 | **156** |
| `winter` | 501 | **144** |
| `night city` | 321 | **131** |
| `timelapse` | 186 | **116** |
| `watch` | 185 | **87** |
| `autumn` | 290 | **83** |
| `spring` | 198 | **75** |

### R14_civic_stone_hearing_room   union 652
32 queries over two rounds (16 round 1, 16 retries), 4 round-1 zeros, 15 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *aerial shot of church with domes* / *stones on sea bottom* / *church dome in city*

| query | title-AND | usable |
|---|---:|---:|
| `architecture` | 625 | **408** |
| `temple` | 202 | **130** |
| `stone` | 168 | **82** |
| `dome` | 45 | **26** |
| `court` | 57 | **14** |
| `monument` | 29 | **13** |
| `historic building` | 30 | **7** |
| `public building` | 8 | **7** |
| `government building` | 19 | **5** |
| `palace` | 14 | **5** |

### R15_weather_dusk_silence   union 1775
20 queries over two rounds (16 round 1, 4 retries), 1 round-1 zeros, 4 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *time lapse of clouds in grayscale* / *sky at sunset and night* / *time lapse of blue sky and clouds*

| query | title-AND | usable |
|---|---:|---:|
| `sky` | 1429 | **855** |
| `clouds` | 861 | **500** |
| `rain` | 1081 | **312** |
| `wind` | 906 | **186** |
| `fog` | 516 | **121** |
| `evening` | 165 | **96** |
| `dusk` | 137 | **69** |
| `cloudy` | 99 | **53** |
| `storm` | 191 | **45** |
| `mist` | 252 | **36** |

### R16_paper_records_typing   union 778
28 queries over two rounds (16 round 1, 12 retries), 3 round-1 zeros, 12 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *globe of death performance in circus* / *a person filming a female model with a medium format camera* / *old books and burning candle*

| query | title-AND | usable |
|---|---:|---:|
| `sign` | 957 | **270** |
| `office` | 416 | **141** |
| `form` | 280 | **131** |
| `book` | 419 | **121** |
| `library` | 146 | **65** |
| `office work` | 149 | **57** |
| `typing` | 140 | **46** |
| `books` | 122 | **44** |
| `notes` | 86 | **40** |
| `writing` | 158 | **31** |

### R17_crane_lift_heavy   union 413
40 queries over two rounds (16 round 1, 24 retries), 6 round-1 zeros, 19 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *propeller plane landing* / *a fire truck parked near a stop sign* / *clouds over harbor cranes*

| query | title-AND | usable |
|---|---:|---:|
| `rope` | 209 | **133** |
| `truck` | 174 | **68** |
| `rig` | 149 | **60** |
| `crane` | 81 | **52** |
| `wire` | 83 | **47** |
| `chain` | 77 | **40** |
| `cable` | 31 | **5** |
| `forklift` | 12 | **5** |
| `loader` | 14 | **5** |
| `tower crane` | 8 | **5** |

### R18_light_shadow_dark_abstract   union 2431
24 queries over two rounds (16 round 1, 8 retries), 2 round-1 zeros, 8 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *woman against braille lights* / *close up of flying insects* / *match lighting up chemical*

| query | title-AND | usable |
|---|---:|---:|
| `light` | 2080 | **907** |
| `abstract` | 979 | **571** |
| `close up` | 1060 | **419** |
| `smoke` | 395 | **216** |
| `bokeh` | 259 | **184** |
| `dark` | 430 | **181** |
| `particles` | 180 | **112** |
| `glass` | 399 | **107** |
| `texture` | 276 | **100** |
| `black background` | 177 | **94** |

### R19_vintage_film_1980s   union 275
48 queries over two rounds (16 round 1, 32 retries), 8 round-1 zeros, 28 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *flat lay footage of pastries and breads on a surface* / *a man filming using an analog camera* / *a person filming a female model with a medium format camera*

| query | title-AND | usable |
|---|---:|---:|
| `cine` | 147 | **62** |
| `vintage` | 196 | **44** |
| `black and white` | 155 | **37** |
| `retro` | 104 | **34** |
| `historic` | 111 | **31** |
| `past` | 92 | **31** |
| `old footage` | 24 | **16** |
| `historical` | 41 | **14** |
| `vintage car` | 26 | **12** |
| `museum` | 17 | **10** |

### R20_engineering_office_model   union 166
32 queries over two rounds (16 round 1, 16 retries), 4 round-1 zeros, 11 still zero after retrying. Real titles from the survivors, so the number can be judged rather than believed: *a person filming a female model with a medium format camera* / *close up of a person painting a corsair pilot miniature* / *a 3d model of a bunch of colorful blocks*

| query | title-AND | usable |
|---|---:|---:|
| `model` | 205 | **44** |
| `study` | 78 | **34** |
| `3d model` | 39 | **25** |
| `office desk` | 101 | **25** |
| `engineer` | 54 | **13** |
| `lamp` | 64 | **13** |
| `meeting` | 350 | **11** |
| `engineering` | 28 | **9** |
| `planning` | 18 | **8** |
| `workspace` | 10 | **5** |

---

## 5. The cut budget, checked so the contract is satisfiable

EP66 declared a contract its own cut budget could not satisfy — 350 distinct video assets against a
video-cut ceiling of 311 — and that arithmetic was only found after the plan was written. It is done
first here.

```
runtime band (episode_spec)                        1560 .. 1895 s     (design point 1798.5 s)
target_cut_sec (episode_spec)                              3.6 s
total cuts                    1560/3.6 = 433      1798/3.6 = 499      1895/3.6 = 526
stills may occupy at most 32% of cuts                      138                 159         168
video cuts available          433-138 = 295       499-159 = 340       526-168 = 358
mandatory_stills declared                                  113        -> fits at every edge
distinct_video_assets declared                             250        -> fits at every edge
video cuts this plan allocates (s2)                        320        -> the design-point figure
```

**250 distinct sources over 320 video cuts** gives a distinct fraction of **0.781** against the
`footage_diversity` floor of **0.40**, and leaves 70 second uses to spread — inside the `reuse ≤ 4`
cap and the `generic symbols ≤ 2` cap. `footage_utilization` wants **≥ 80%** of staged clips
actually used; staging **290–320** against 250 required keeps that reachable, and staging 1,000
would not. **Do not stage the whole 14,747.**

`animation_density` (near-still ≤ 10% of runtime, single hold ≤ 3.0 s) and `motion_density`
(≥ 2.5 kinetic beats/min, coverage ≥ 0.25, variety ≥ 3) are met by the motion budget in film bible
§10 and §12.5, not by this document. What this document owes them is **enough distinct moving
footage that no cut has to be a held still**, and 320 video cuts at 3.6 s is that.

---

## 6. Screening rules a machine cannot apply, and who applies them

`footage_review_required` is **true** in the contract. These are the judgements a person makes over
a labelled contact sheet before any clip enters a cut. The factory shelf's filename labels measure
**~40–50% wrong**, and 683 of 1,094 clips across five earlier episodes were wrong for their story
when somebody finally looked.

1. **Period first, every clip, before anything else.** `era_setting` is **1978–1988**. A cordless
   drill, a hi-vis vest, an LED work lamp, a flat-panel monitor, a mobile phone, a laptop, a CAD
   screen or a post-1990 car makes a clip unusable however good it is. **This register is where the
   shelf is newest**, and no gate measures it. EP62 shipped a 2011 Range Rover on an EU plate past
   five green gates for exactly this reason.
2. **No collapse, no rubble, no rescue, no casualty, in any clip, at any point.** The contract
   blocks them by title word; a human blocks them by looking. A demolition clip, a
   disaster-response clip or an excavator moving broken concrete is the single most defamatory cut
   this film could make, and every one of them survives the title screen.
3. **Nothing that reads as the Hyatt Regency.** No hotel with that atrium geometry, no signage, no
   brand mark, no Kansas City hotel exterior that a local would recognise. The building is real and
   currently trading. `hyatt` is a `forbidden_subject` so no title can carry it; a picture can.
4. **No courtroom interior, re-enacted or stock.** Everything the Board, the Commission and the
   Court of Appeals did in this story is text — findings, a statute, a footnote. Stock "courtroom"
   footage is a television set. The tribunals are exteriors, stone, doors and typography.
5. **No readable drawing, no readable page, no seal.** Any drawing, plan or document in any cut
   must be out of focus, edge-on, or blank. A legible technical drawing next to this narration
   reads as *drawing S405.1*, which is barred outright (⛔-14, invariant 11).
6. **People: required, and faces are allowed** — see §7. What is barred is a *real, identifiable
   individual's likeness*, and above all anything a viewer could take for Daniel Duncan, Jack
   Gillum, a named victim, or anyone who was in that room.
7. **Register check, per clip:** is this the United States, and is it the Midwest? A Bangkok street,
   a European plaza and a Middle Eastern skyline all survive every machine gate and all of them are
   wrong here. `temple` 130 and `architecture` 408 are the two registers where this will bite.
8. **No-repeat, across the film and across the channel.** Within the film, a clip is used at most
   twice unless the repetition is an argument the bible names (the empty atrium at three, at half
   past four and at seven is the one deliberate motif return, and it is the SAME plate three times
   on purpose). Across the channel, §1 filter 7 has already excluded every id another episode holds;
   before staging, re-run `py -3.11 scripts/check_cross_episode_reuse.py --build` so
   `STAGED_CLIP_INDEX.json` is current — the count moved by 712 ids between EP67's measurement and
   this one.

### The staging command

```bash
# dry run first, always
py -3.11 scripts/stage_footage_by_title.py --slug hyatt --per-query 3 --dry-run \
  --query "plant" --query "factory" --query "rod" --query "machine" --query "architect" ...

# then the contact sheet, then a person looks at it, then the pool is trimmed
py -3.11 scripts/search_archive.py --shot "threaded steel rod nut washer bench" --kind video --sheet --limit 24
```

---

## 7. The people lane — required, not tolerated

**Owner decision 2026-07-04: depicted people are REQUIRED and welcome. The only thing barred is the
likeness of a real, identifiable individual** (CLAUDE invariant 11). EP60 shipped a film with nobody
in it and that was wrong.

**This film's people are unusually constrained, and the constraint is the ledger's, not a
preference.** ⛔-11 bars any body, injured person, rescue or casualty. ⛔-12 bars any depiction of
the crowded lobby at or near the moment of collapse, from any angle. ⛔-13 bars naming or depicting
any victim, survivor, rescuer, witness, board member or engineer. So the film cannot use people the
way a disaster film uses people. **It uses them the way a workshop uses them.**

- `episode_spec.people_plates_min` = **22**, and `episode_spec.people_plates` names all twenty-two
  ids explicitly, because `check_episode_inputs` once reported 0 of 10 on forty plates that existed
  and were correct.
- **How the people requirement is met without breaching the depiction rules.** Hands and bodies at
  work, in rooms nobody died in: a hand rolling a drawing flat; a hand setting a plain seal onto
  paper; a draughtsman's stool, occupied, seen from behind; three stamps landing on a drawing edge
  for the contractor, the structural engineer and the architect; a fabricator's gloved hands on a
  channel section; a man in his fifties at a drawing board, three-quarter, **face resolvable**,
  who is nobody in this record; a technician holding a print up to a window; two people talking in
  a doorway in a plain office; a woman at a filing cabinet; a clerk carrying a stack of paper down
  a corridor; a caretaker crossing an empty ballroom floor at midday.
- **Nine of the twenty-two plates carry a resolvable face — eight full, one in profile only — and that is deliberate.** None of them
  is presented, captioned, cut or narrated as anyone in this record. They are engineers,
  draughtsmen, clerks and fabricators in the abstract — the ordinary people whose ordinary conduct
  the Commission found had combined into something lethal, which is the film's thesis. A film that
  hides every face while arguing that a system of ordinary people killed 114 of them has argued
  against itself.
- **Register R11 owes 22 of the 320 video cuts**, and it is the only register whose clips are all
  review-required by default: a title that names a human is a candidate, never supply. `people` 410
  and `hand` 237 are the two largest usable counts in the whole plan and also the two most likely
  to be modern.

---

## 8. What must happen next, in order

1. Re-run `scripts/check_cross_episode_reuse.py --build`; the staged-id count is moving (9,068 →
   9,780 since EP67).
2. Stage 290–320 clips with `--dry-run` first, from the §4 queries with the highest usable counts in
   each register, **not** from the highest title-AND counts.
3. Build labelled contact sheets and **have a person look at them**, period screen first. Record a
   verdict per clip; `footage_review_required` is true and a stamped-without-looking QC is the
   failure this contract exists to stop.
4. Commission the generated plates (H001–H113, `EP69_hyatt_CODEX_BATCH_A.v001.md`), which cover all
   six gaps in §3 that the archive cannot supply.
5. Only then build `hyatt_film.json`, and run `check_spec_satisfied.py` before the render.

*Measured 2026-08-11 in two ledger passes. 663 queries, 85 round-1 zeros re-asked in 340 other words
before any of them was recorded as a gap. The instrument was caught lying once, on its first run,
and the fix is recorded in §1. Nothing was staged and nothing was moved.*

---

> **Correction, 2026-08-12.** `distinct_video_assets` was corrected in `episode_spec.v002.json` because the original figure was never derived from the allocator. Superseded numbers may remain in the body above for provenance; the spec is authoritative. See `decisions/0009-DISTINCT-VIDEO-ASSETS-CORRECTION.md`.
