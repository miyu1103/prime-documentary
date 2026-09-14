# EP68 · THE FORD PINTO / *GRIMSHAW v. FORD* — FOOTAGE QUERY PLAN v001

**Date 2026-08-11 · slug `pinto` · episode `PD-2026-068-pinto`**
**Contract `episodes/PD-2026-068-pinto/episode_spec.v001.json` — `distinct_video_assets` **265**,
`target_cut_sec` **3.7**, `runtime_seconds` **[1560, 1895]**, `footage_review_required` **true**,
**124** `forbidden_subjects`, `era_setting` **USA 1968–1981**.**
**Design `EP68_pinto_FILM_BIBLE.v001.md` · front `EP68_pinto_PACKAGING.v001.md` ·
facts `EP68_pinto_FACTS_LEDGER.v001.md`.**

> **Nothing here was staged, copied, transcoded or ffprobed.** Every number below was produced by
> reading the rights ledger and the resolution index in a single pass, while another episode's
> render held the disks. No clip was moved.

---

## 0. Result in one block

```
contract distinct_video_assets                            265
clip floor, runtime_lo // 45  (check_final_acceptance)     34     -> not binding
channel target                                             60     -> not binding
video cuts this film has room for (see s5)                324
queries asked, over two rounds                            623
counted register unions (19 registers)                 14,314
of those, surviving the off-register + forbidden screen 11,089
a 20th register measured and then REFUSED (fire)        1,021     <- excluded from both totals
ledger videos with a usable licence and a clean title  37,922
clip ids already held by some episode's factory*        9,780     <- already subtracted everywhere
queries still returning 0 after BOTH rounds               153
```

**The shelf is not the binding constraint on volume, and is very nearly the binding constraint on
period.** 11,089 screened clips against 265 required is a factor of 41. But this is a film set
between **1968 and 1981**, and the factory shelf is a contemporary stock library. The three real
constraints are:

1. **Era.** `vintage tv`, `crt`, `film reel`, `old film`, `8mm film`, `super 8`, `archival`,
   `archive footage`, `historic footage`, `1970s`, `nostalgia` and `home movie` **all return 0
   usable clips after two rounds** (§4, R19). The whole period register screens to **119 clips**,
   the thinnest in the plan. Nothing in this film may show an LED headlight, a flat-screen monitor,
   a mobile phone, a modern motorway gantry or a euro number plate, and **every one of those
   survives every machine gate**. `era_setting` exists in the contract for exactly this, and it is
   a human's job (§6 rule 6).
2. **The four things the film is actually about are the four things the shelf does not have** —
   typed paper, the underside of a car, an American courthouse, and the 1970s (§3).
3. **This film shows no crash and no fire, at all, ever.** That is not squeamishness; it is
   ⛔-08/⛔-09 in the facts ledger and §3.5 of the film bible. It costs a whole register (§1.5).

---

## 1. The instrument, verified before any zero was trusted

The counts in §4 were produced by **replicating `scripts/stage_footage_by_title.py`'s own
selection** over one pass of the ledger instead of 623 passes. Not a second search implementation:
the measuring script imports that module and uses *its* `ledger_rows()`, *its* `OK_LICENSE`, *its*
`TITLE_BLOCK` and `RIP_SIGNATURE` regexes and *its* `slugify()`, so every row it counts is a clip
the staging tool would really take. The scripts are
`…/scratchpad/measure_pinto.py` (round 1), `measure_pinto2.py` (round 2, merged) and
`rescreen_pinto.py` (the final screen against the contract as declared).

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
| 8 | `_ledger/video_resolution.json` says **w ≥ 1920 and h ≥ 1080** | `search_archive.load_video_resolution` — the ledgers carry no width or height, and most archival video on the shelf is below 720p |

**Cross-episode reuse is therefore already subtracted from every number in this document** (owner
complaint 「素材の被り」, gate `footage_diversity`). **9,780 ids** are held by some episode's
`factory*` folder and none of them is counted here. That figure was **8,997** when EP67 measured it
overnight and **9,068** by the end of that pass; it is a moving number and it only ever goes up.
**Re-measure before staging if more than a day passes.**

Any single row reproduces with the canonical instrument, whose count is a little **wider** because
its CLI ANDs against title + id + matched keywords + theme + filename rather than title alone, and
which prints its total as `-- N hits total` on the last line:

```bash
py -3.11 scripts/search_archive.py vintage car --kind video --limit 50
py -3.11 scripts/search_archive.py --shot "empty three lane highway from above" --kind video --limit 25
```

### 1.5 The register this episode measured and then refused

**`R7 heat / flame / ember` was asked, in 20 words over two rounds, and returned a union of 1,021
clips and 390 that survive the off-register screen. Not one of them will be staged.**

The film shows no fire. The contract enforces it: `fire`, `fires`, `flame`, `flames`, `burning`,
`burn`, `burns`, `burned`, `burnt`, `blaze`, `blazing`, `bonfire`, `campfire`, `wildfire`, `smoke`,
`smoking`, `ember`, `embers`, `ash`, `ashes`, `soot`, `charred` and `inferno` are all in
`forbidden_subjects`, so `check_spec_satisfied.py` fails the build on any clip whose source filename
carries one. **The register is printed in §4 under a `####` heading rather than a `###` one, so the
design gate does not count it as supply.** It is printed at all because a register that was refused
on purpose is worth more in the record than one nobody thought to ask about — and because the next
person to build a fire-adjacent episode will want the 1,021.

The same decision removes crash imagery: `crash`, `crashing`, `crashes`, `collision`, `accident`,
`wreck`, `wrecked` and `wreckage` are forbidden too. **R6 is therefore not a crash register.** It
survives as a *laboratory and instrument* register — test rigs, high-speed camera, glass, slow
motion, measurement — and 184 of its union titles are removed by that screen. Read §4 R6 with that
in mind: its remaining 865 is dominated by `hit` (641 clips, most of them nothing to do with a
vehicle) and by waves crashing on rocks. **The usable core of that register is perhaps thirty
clips**, and finding them is a person's job.

---

## 2. The registers, and how many cuts each one owes

Nineteen counted registers, derived from this film's own sections rather than from a generic list.
Cut counts sum to **324**, which is the video-cut budget computed in §5.

| # | register | what it is for in THIS film | cuts | script beats it serves |
|---|---|---|---:|---|
| R1 | the car, unbadged, 1970s | the object of the whole story. **Never a badge, never a plate, never a real Pinto** | 26 | A1-01…A1-06; A2-01; ENDING |
| R2 | freeway, road, the middle lane | Interstate 15, and the empty lane the film returns to instead of the crash | 24 | HOOK none; A2-01…A2-05; A5-01; ENDING |
| R3 | fuel, pump, liquid, container | gasoline as a substance, never as a fire | 10 | A1-03; A1-07; A2-02 |
| R4 | factory, assembly, machinery | a rush project going into production in 1970 | 24 | A1-01; A1-02; A1-09; A1-16 |
| R5 | drafting, measuring, tools | styling preceded engineering. Boards, rules, hands, dividers | 20 | A1-02; A1-04; A1-08; A1-10 |
| R6 | laboratory, instrument, test | crash **testing**, represented by instruments and never by a collision (§1.5) | 12 | A1-07; A1-08; A1-09; A5-11 |
| R8 | corporate office, meeting, tower | the April 1971 product review, and the company seen from outside | 20 | A1-13…A1-16; A4-02 |
| R9 | paper, files, typing, mail | the eight pages, exhibit 125, the recall letters, the record | 26 | HOOK all; A4-01…A4-10; A3-14 |
| R10 | press, printing, newsprint, broadcast | September 1977, and what a magazine could still do in 1977 | 20 | HOOK cut 4; A3-01…A3-06 |
| R11 | government, capitol, flag, federal | NHTSA. The regulator is a real instrument of the United States | 12 | A1-16; A1-17; A3-07…A3-13 |
| R12 | stone, columns, civic exterior | two courts. **Never a re-enacted courtroom** (§6) | 18 | A2-08…A2-15; A5-02…A5-10 |
| R13 | Indiana farmland, small town | Elkhart County in August, and Winamac | 18 | A5-01; A5-05; A5-09 |
| R14 | money, counting, arithmetic | five pairs of numbers that must stay apart | 12 | A1-11; A2-10…A2-13; A4-07…A4-09 |
| R15 | crowd, public, anonymous | the buyers of 2.2 million cars, and the people who read the article | 14 | A3-04; A3-08; A3-15 |
| R16 | hands, backs, figures | **the people lane.** Human presence with no identifiable face | 20 | throughout; see §7 |
| R17 | clock, calendar, seasons | 1968 → 1971 → 1972 → 1977 → 1978 → 1980 → 1981 | 10 | act transitions ×6 |
| R18 | salvage, rust, disused metal | the end of a car's life, with no collision in it | 10 | A5-11; ENDING |
| R19 | period media, film grain, television | 1977–78, when this became a television story. **The thinnest register in the plan** | 10 | A3-06; A3-14 |
| R20 | dusk, weather, quiet street | the five designed silences | 18 | A2-05; A2-06; A4-01; A5-14; ENDING |
|  | **total** |  | **324** | |

**Hard constraint that binds every register.** `check_spec_satisfied.py` matches
`forbidden_subjects` word-wise **against the source filename**, so a clip whose title carries
`fire`, `flame`, `smoke`, `crash`, `collision`, `accident`, `wreck`, `victim`, `injury`, `hospital`,
`ambulance`, `child`, `teenager`, `girl`, `boy`, `police`, `prison`, `gavel`, `scales`, `hourglass`,
`handshake`, `drone`, `racing` or `wedding` is an automatic build failure. **That is not a mistake
in the contract — it is the point.** This is an episode about a woman who died of burns and a
13-year-old who survived them; a stock clip whose own title says `fire` placed anywhere in this
film is the single most damaging thing it could do.

---

## 3. The zeros, and the retries that were run before any of them was written down as a gap

**Round 1 asked 429 queries and produced 84 zeros. Round 2 re-asked every zero-producing register in
different words — 194 further queries — before a single gap was recorded.** A zero is a fact about
the words until it has been asked at least three other ways. The measured wins:

| director's phrasing | usable | supplier phrasing that worked | usable |
|---|---:|---|---:|
| `sedan` · `hatchback` · `compact car` · `bumper` · `tyre` | **0** | `car road` **242** · `city car` **131** · `car street` **98** · `wheel` **21** · `car vintage` **12** · `antique car` **5** | 896 union |
| `road marking` | **0** | `street road` **107** · `asphalt road` **24** · `road line` **8** | 977 union |
| `fuel pump` · `gas pump` · `fuel tank` · `refuel` · `canister` | **0** | `container` **50** · `gas` **28** · `tank water` **9** · `water pour` **4** | 150 union |
| `blueprint` · `drafting` · `technical drawing` · `caliper` · `grid paper` · `prototype` · `workbench` | **0** | `craft` **25** · `cad` **21** · `draw` **15** · `making` **14** · `notebook` **11** · `tool` **9** | 903 union |
| `crash test` · `collision` · `dummy` · `safety test` · `glass break` | **0** | `hit` **641** · `slow motion` **115** · `glass` **107** · `safety` **8** · `old cars` **6** | 1,104 union |
| `boardroom` · `elevator` · `empty office` · `meeting room` · `cubicle` | **0** | `board` **145** | 531 union |
| `documents` · `typewriter` · `old typwriter` · `files` · `folder` · `archive` · `signature` · `envelope` | **0** | `library` **65** · `post` **13** · `storage` **9** · `old machine` **5** | 1,332 union |
| `newspaper` · `printing press` · `print press` · `headline` · `camera crew` · `turning pages` | **0** | `camera` **109** · `print` **38** · `reading book` **37** · `video camera` **15** | 643 union |
| `senate` · `lectern` · `microphone stand` | **0** | `capital` **33** · `speech` **14** · `government building` **5** | 549 union |
| `courthouse` · `courtroom` · `columns` · `stone columns` · `classical building` · `pillar` · `civic building` · `town hall` | **0** | `arch` **468** · `temple` **130** · `stone` **82** · `stairs` **7** · `city hall` **4** | 774 union |
| `corn field` · `small town` · `main street` · `farmhouse` · `front porch` | **0** | `street` **350** · `town` **125** · `downtown` **41** · `porch` **4** | 772 union |
| `abacus` · `adding machine` · `ledger` · `cash register` | **0** | `numbers` **22** · `payment` **9** · `math` **8** | 717 union |
| `queue` · `audience` | **0** | `line` **374** · `row people` **18** · `seats` **10** | 855 union |
| `wall clock` · `calendar` · `clock face` · `old clock` · `month` | **0** | `date` **11** · `days` **8** | 1,417 union |
| `scrap metal` · `derelict` · `landfill` · `corroded` · `rusted` | **0** | `ruins` **31** · `waste` **7** · `trash` **5** | 211 union |
| `vintage tv` · `crt` · `film reel` · `old film` · `8mm film` · `super 8` · `archival` · `1970s` | **0** | `film` **33** · `cinema` **28** · `studio` **23** · `glitch` **18** · `old footage` **16** · `tv screen` **15** · `old video` **12** · `grain` **7** | 167 union |
| `grey sky` · `gray sky` · `drizzle` · `quiet street` · `street lamp` | **0** | `clouds` **500** · `raining` **37** · `alley` **25** · `lantern` **23** · `street light` **20** | 1,278 union |

Four of those rows are worth reading twice:

- **`grey sky` 0 → `gray sky` 0 → `cloudy sky` 26 → `clouds` 500.** Both spellings returned nothing
  and the register was still there, five hundred clips deep, behind a shorter word. A zero is never
  recorded until it has been re-asked, and this row is why.
- **`crash test` 0, `collision` 0, `dummy` 0 — and `hit` 641.** The 641 is not a win. Most of it is
  waves hitting rocks and balls hitting bats, and the film cannot use a vehicle collision anyway
  (§1.5). **This is the clearest case in the plan of a hit count that is not a supply count.**
- **`courthouse` 0, `courtroom` 0, `columns` 0 — and `arch` 468.** The 468 is European cathedrals,
  Roman ruins and Asian temples. It is not an American courthouse and it will not become one by
  being counted. The two courts in this film are **generated plates** (§3, gap c).
- **The whole of R19.** Eight period queries returned zero and the register screens to 119 clips
  total. **The archive has essentially no 1968–1981 material for this story.**

### The four real gaps, and what fills them

| gap | measured | filled by |
|---|---|---|
| **typed paper — the eight pages, exhibit 125, the record** | `documents`, `typewriter`, `old typwriter`, `files`, `folder`, `archive`, `signature`, `envelope`, `binder`, `folders` all **0 usable** | **generated plates.** R001–R022 in the image order. This is the hook, the TURN and thumbnail variant 1, so it cannot be approximated |
| **the underside of a car — the gap between axle and tank** | `fuel tank`, `fuel pump`, `gas pump`, `refuel` all 0; `blueprint` and `technical drawing` 0; nothing in the shelf shows a vehicle on a lift | **generated plates.** R023–R040. This is **H1**, the film's central visual argument, returned six times, and thumbnail variant 2 |
| **an American courthouse, exterior and interior corridor** | `courthouse`, `supreme court`, `court building`, `courtroom`, `civic building`, `town hall` all 0; `arch` 468 is European and religious | **generated plates** R041–R056 for the two courts, plus archive `stone`, `stairs` and `old building` for approach and scale only. **No re-enacted courtroom interior at all** (§6) |
| **1968–1981 itself** | every period query 0; R19 screens to 119 | **generated plates** R057–R080 carry the period interiors, the product-review room, the press and the domestic 1970s. The archive supplies **timeless** material only — road, weather, stone, hands, crowds, machinery — and every clip is checked against `era_setting` by a person (§6 rule 6) |

---

## 4. The queries, verbatim, with measured hit counts

623 queries over 20 registers, both rounds merged. `title-AND` = ledger rows whose title contains
every term. `on disk` = of those, the file exists and is 1–120 MB. `unused` = of those, the id is in
no episode's `factory*` folder. `>=1920x1080 & unused` = the operative supply figure, joined against
`_ledger/video_resolution.json`. `union` on each heading is the count of **distinct** clip ids in
that last column across the register's queries — it is not the column sum, because one clip answers
several queries. `round` is which pass asked it.

**A hit count is not a supply count.** Each register heading also carries the count that survives
the off-register title screen (crypto, beach, food, sport, wedding, medical, space, racing, 3d…)
**and this episode's own 124 `forbidden_subjects`**, plus three real titles from the survivors so
the number can be judged rather than believed. Read them: `crash` is full of waves, `court` is full
of a wren's courtship dance, and `arch` is full of architecture. **The screened figure is the number
of clips a person has to look at — not the number that will survive looking.**

### R1_the_car_1970s_traffic   union 896
screened supply **715** after removing 66 off-register and 115 `forbidden_subjects` titles; this register owes **26** of the 324 video cuts. Examples of what the union is made of: *car, street, night, city, moon, buildings, road, lights, vintage, urban, traff* / *automobile, black, antique car, vehicle, luxury, car, dare, vintage, dynamics,* / *automobile, black, antique car, vehicle, luxury, car, dare, vintage, dynamics,*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `car` | 1 | 1555 | 1110 | 897 | **751** |
| `car road` | 2 | 422 | 347 | 304 | **242** |
| `vehicle` | 1 | 342 | 252 | 226 | **212** |
| `city car` | 2 | 186 | 163 | 141 | **131** |
| `auto` | 1 | 202 | 138 | 130 | **118** |
| `car street` | 2 | 150 | 138 | 102 | **98** |
| `car driving` | 1 | 150 | 124 | 104 | **82** |
| `automobile` | 1 | 86 | 57 | 55 | **51** |
| `old car` | 1 | 57 | 50 | 40 | **35** |
| `wheel` | 2 | 161 | 46 | 23 | **21** |
| `car park` | 1 | 62 | 36 | 22 | **19** |
| `vintage car` | 1 | 26 | 24 | 14 | **12** |
| `parking lot` | 1 | 40 | 28 | 17 | **12** |
| `car vintage` | 2 | 26 | 24 | 14 | **12** |
| `car close` | 2 | 33 | 25 | 14 | **12** |
| `old vehicle` | 2 | 9 | 9 | 9 | **9** |
| `dashboard` | 1 | 17 | 16 | 14 | **8** |
| `car wheel` | 1 | 33 | 9 | 9 | **8** |
| `tire` | 1 | 36 | 23 | 21 | **8** |
| `car moving` | 2 | 17 | 15 | 8 | **8** |
| `classic car` | 1 | 12 | 11 | 7 | **7** |
| `retro car` | 1 | 14 | 10 | 9 | **7** |
| `car lot` | 1 | 27 | 15 | 13 | **7** |
| `car show` | 1 | 6 | 6 | 6 | **5** |
| `antique car` | 2 | 5 | 5 | 5 | **5** |
| `car front` | 2 | 7 | 7 | 5 | **5** |
| `car engine` | 1 | 7 | 4 | 4 | **4** |
| `car key` | 1 | 16 | 7 | 7 | **4** |
| `car interior` | 1 | 7 | 5 | 3 | **3** |
| `car door` | 1 | 8 | 8 | 5 | **3** |
| `car window` | 1 | 25 | 10 | 4 | **3** |
| `car rear` | 1 | 6 | 5 | 3 | **3** |
| `car mirror` | 1 | 4 | 4 | 4 | **3** |
| `small car` | 1 | 8 | 4 | 2 | **2** |
| `car seat` | 1 | 3 | 2 | 2 | **2** |
| `wheels` | 2 | 20 | 3 | 3 | **2** |
| `car small` | 2 | 8 | 4 | 2 | **2** |
| `steering wheel` | 1 | 10 | 1 | 1 | **1** |
| `rear view` | 1 | 5 | 4 | 2 | **1** |

Still 0 usable after both rounds: `sedan` - `tyre` - `hatchback` - `compact car` - `bumper` - `small vehicle` - `car detail`

### R2_freeway_road_traffic   union 977
screened supply **750** after removing 94 off-register and 133 `forbidden_subjects` titles; this register owes **24** of the 324 video cuts. Examples of what the union is made of: *Driving down a highway in a big city* / *Cars traveling at high speed on a highway at night* / *highway, car, traffic, street, city, vehicle, transportation, transfer, work, *

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `road` | 1 | 1219 | 960 | 726 | **609** |
| `traffic` | 1 | 682 | 574 | 483 | **415** |
| `highway` | 1 | 354 | 286 | 213 | **184** |
| `street road` | 2 | 180 | 147 | 113 | **107** |
| `driving` | 1 | 201 | 168 | 138 | **104** |
| `lane` | 1 | 214 | 115 | 106 | **88** |
| `car light` | 1 | 104 | 83 | 65 | **50** |
| `night traffic` | 1 | 95 | 91 | 44 | **39** |
| `asphalt` | 1 | 67 | 46 | 41 | **32** |
| `highway aerial` | 1 | 43 | 40 | 30 | **28** |
| `road night` | 1 | 78 | 65 | 37 | **27** |
| `freeway` | 1 | 41 | 32 | 26 | **26** |
| `truck road` | 1 | 63 | 30 | 26 | **25** |
| `asphalt road` | 2 | 56 | 38 | 33 | **24** |
| `desert road` | 1 | 29 | 24 | 20 | **18** |
| `road trip` | 1 | 26 | 20 | 15 | **13** |
| `traffic jam` | 1 | 18 | 13 | 13 | **12** |
| `motorway` | 1 | 9 | 8 | 8 | **8** |
| `road line` | 2 | 14 | 9 | 8 | **8** |
| `road sign` | 1 | 17 | 11 | 6 | **5** |
| `roadside` | 1 | 10 | 5 | 5 | **5** |
| `overpass` | 1 | 5 | 5 | 4 | **4** |
| `tail light` | 1 | 4 | 4 | 4 | **4** |
| `interstate` | 1 | 2 | 2 | 2 | **2** |
| `empty road` | 1 | 24 | 21 | 1 | **1** |
| `long road` | 1 | 10 | 5 | 3 | **1** |
| `headlight` | 1 | 4 | 3 | 1 | **1** |

Still 0 usable after both rounds: `road marking`

### R3_fuel_petrol_tank   union 150
screened supply **101** after removing 40 off-register and 9 `forbidden_subjects` titles; this register owes **10** of the 324 video cuts. Examples of what the union is made of: *tome lapse footage of vehicles filling at a gas station* / *people standing on gas station* / *vibrant nighttime gas station with neon lights*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `container` | 2 | 76 | 62 | 57 | **50** |
| `gas` | 2 | 99 | 58 | 32 | **28** |
| `oil` | 1 | 77 | 46 | 32 | **27** |
| `tank` | 1 | 43 | 23 | 20 | **17** |
| `drum` | 1 | 17 | 11 | 10 | **10** |
| `tank water` | 2 | 13 | 11 | 10 | **9** |
| `gas station` | 1 | 22 | 21 | 9 | **6** |
| `pump` | 1 | 21 | 9 | 5 | **5** |
| `water pour` | 2 | 14 | 9 | 4 | **4** |
| `petrol` | 1 | 7 | 3 | 3 | **3** |
| `petrol station` | 1 | 4 | 2 | 2 | **2** |
| `liquid pour` | 1 | 9 | 5 | 4 | **2** |
| `pouring liquid` | 1 | 8 | 4 | 3 | **2** |
| `spill` | 1 | 7 | 5 | 4 | **2** |
| `fuel` | 1 | 23 | 7 | 4 | **1** |
| `gasoline` | 1 | 1 | 1 | 1 | **1** |
| `filling station` | 1 | 1 | 1 | 1 | **1** |
| `nozzle` | 1 | 4 | 2 | 2 | **1** |
| `barrel` | 1 | 5 | 2 | 1 | **1** |
| `diesel` | 2 | 5 | 1 | 1 | **1** |
| `bottle pour` | 2 | 7 | 2 | 2 | **1** |

Still 0 usable after both rounds: `fuel pump` - `gas pump` - `fuel tank` - `refuel` - `canister` - `petrol pump` - `fuel station` - `jerry can` - `hose`

### R4_factory_assembly_manufacturing   union 372
screened supply **307** after removing 42 off-register and 23 `forbidden_subjects` titles; this register owes **24** of the 324 video cuts. Examples of what the union is made of: *a woman in an abandon factory* / *indian textile workers in a factory setting* / *factory workers*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `plant` | 1 | 256 | 133 | 97 | **89** |
| `machine` | 1 | 280 | 140 | 89 | **66** |
| `factory` | 1 | 153 | 92 | 71 | **60** |
| `crane` | 1 | 81 | 65 | 58 | **52** |
| `workers` | 1 | 118 | 78 | 59 | **48** |
| `industrial` | 1 | 157 | 110 | 44 | **36** |
| `worker factory` | 1 | 41 | 37 | 31 | **29** |
| `manufacturing` | 1 | 52 | 30 | 24 | **21** |
| `industry` | 1 | 112 | 24 | 17 | **16** |
| `warehouse` | 1 | 53 | 44 | 15 | **10** |
| `conveyor` | 1 | 22 | 17 | 8 | **8** |
| `robot arm` | 1 | 10 | 10 | 9 | **7** |
| `workshop` | 1 | 44 | 15 | 10 | **7** |
| `metal work` | 1 | 32 | 16 | 12 | **7** |
| `machinery` | 1 | 38 | 25 | 9 | **6** |
| `steel` | 1 | 85 | 16 | 7 | **5** |
| `forklift` | 1 | 12 | 12 | 7 | **5** |
| `welding` | 1 | 32 | 16 | 9 | **4** |
| `production line` | 1 | 9 | 8 | 7 | **3** |
| `press machine` | 1 | 13 | 5 | 3 | **3** |
| `assembly` | 1 | 18 | 2 | 2 | **1** |
| `assembly line` | 1 | 2 | 2 | 2 | **1** |


### R5_engineering_drafting_design   union 903
screened supply **693** after removing 121 off-register and 89 `forbidden_subjects` titles; this register owes **20** of the 324 video cuts. Examples of what the union is made of: *person drawing a world map* / *man drawing on a map using a pencil and a ruler* / *The hand of a person drawing*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `architect` | 1 | 658 | 557 | 439 | **424** |
| `design` | 1 | 587 | 243 | 225 | **205** |
| `plan` | 1 | 515 | 273 | 223 | **189** |
| `model` | 1 | 205 | 56 | 53 | **44** |
| `craft` | 2 | 119 | 42 | 36 | **25** |
| `cad` | 2 | 64 | 44 | 24 | **21** |
| `draw` | 2 | 110 | 28 | 17 | **15** |
| `drawing` | 1 | 88 | 22 | 15 | **14** |
| `making` | 2 | 40 | 28 | 21 | **14** |
| `engineer` | 1 | 54 | 28 | 26 | **13** |
| `notebook` | 2 | 66 | 50 | 12 | **11** |
| `engineering` | 1 | 28 | 11 | 11 | **9** |
| `tool` | 2 | 65 | 15 | 11 | **9** |
| `compass` | 1 | 9 | 8 | 8 | **8** |
| `graph paper` | 1 | 38 | 12 | 7 | **7** |
| `diagram` | 1 | 28 | 8 | 8 | **6** |
| `tools` | 2 | 38 | 9 | 5 | **5** |
| `measuring` | 1 | 6 | 4 | 4 | **4** |
| `sketch` | 1 | 14 | 6 | 5 | **3** |
| `drawing hand` | 2 | 17 | 4 | 3 | **3** |
| `plan paper` | 2 | 7 | 5 | 4 | **2** |
| `measure` | 2 | 16 | 3 | 3 | **2** |
| `measurement` | 2 | 15 | 3 | 3 | **2** |
| `bench` | 2 | 33 | 22 | 2 | **2** |
| `ruler` | 1 | 1 | 1 | 1 | **1** |
| `pencil drawing` | 1 | 8 | 2 | 1 | **1** |
| `drawing paper` | 2 | 8 | 3 | 1 | **1** |
| `sketching` | 2 | 2 | 1 | 1 | **1** |

Still 0 usable after both rounds: `blueprint` - `drafting` - `technical drawing` - `caliper` - `grid paper` - `prototype` - `workbench` - `draft` - `engineering drawing` - `design drawing` - `tape measure` - `squared paper` - `model making`

### R6_crash_test_impact   union 1104
screened supply **865** after removing 55 off-register and 184 `forbidden_subjects` titles; this register owes **12** of the 324 video cuts. Examples of what the union is made of: *high speed shattering glass jar impact* / *close up of a test tube rotator* / *a pouring liquid in the test tubes*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `hit` | 2 | 1381 | 902 | 688 | **641** |
| `slow motion` | 2 | 177 | 154 | 133 | **115** |
| `glass` | 2 | 399 | 230 | 140 | **107** |
| `dent` | 1 | 193 | 134 | 111 | **91** |
| `test` | 1 | 167 | 120 | 76 | **67** |
| `crash` | 1 | 63 | 48 | 41 | **35** |
| `laboratory` | 1 | 113 | 103 | 21 | **14** |
| `breaking` | 1 | 33 | 20 | 14 | **14** |
| `experiment` | 1 | 32 | 21 | 12 | **8** |
| `wreck` | 1 | 28 | 15 | 14 | **8** |
| `safety` | 2 | 23 | 12 | 8 | **8** |
| `old cars` | 2 | 7 | 7 | 6 | **6** |
| `helmet` | 2 | 29 | 7 | 6 | **5** |
| `cracked` | 2 | 7 | 6 | 5 | **5** |
| `junkyard` | 1 | 4 | 4 | 4 | **4** |
| `scrap car` | 1 | 5 | 4 | 3 | **3** |
| `accident` | 2 | 5 | 3 | 3 | **3** |
| `damage` | 1 | 31 | 12 | 10 | **2** |
| `car crash` | 2 | 2 | 2 | 2 | **2** |
| `broken glass` | 2 | 3 | 3 | 2 | **2** |
| `demolition` | 2 | 15 | 8 | 2 | **2** |
| `impact` | 1 | 5 | 1 | 1 | **1** |
| `lab test` | 1 | 5 | 5 | 3 | **1** |
| `shatter` | 1 | 2 | 2 | 2 | **1** |
| `wrecked car` | 1 | 1 | 1 | 1 | **1** |
| `scrapyard` | 1 | 1 | 1 | 1 | **1** |
| `smash` | 2 | 5 | 2 | 2 | **1** |
| `protective` | 2 | 4 | 1 | 1 | **1** |

Still 0 usable after both rounds: `crash test` - `collision` - `dummy` - `safety test` - `slow motion impact` - `glass break` - `salvage` - `car accident` - `bump` - `mannequin` - `wrecking`

#### R7_heat_flame_ember   union 1021
**MEASURED AND THEN REJECTED BY THE CONTRACT.** Deliberately written with `####` so the design gate does not count it as supply: this episode's `forbidden_subjects` bans `fire`, `flame`, `smoke`, `ember`, `ash` and `soot` outright, so none of these clips can enter a cut. The register was measured anyway, and the number is printed, because a register that is refused on purpose is worth more in the record than one that was never asked about. **0 of these 1,021 clips are staged.**
screened supply **390** after removing 69 off-register and 562 `forbidden_subjects` titles. Examples of what the union is made of: *a hanging firecrackers on a bamboo* / *lighted firecrackers exploding while hanging on tree branch* / *A woman in a pink suit points a firearm to the camera*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `ash` | 1 | 701 | 472 | 377 | **324** |
| `fire` | 1 | 630 | 370 | 285 | **246** |
| `smoke` | 1 | 395 | 316 | 243 | **216** |
| `glowing` | 1 | 153 | 126 | 113 | **112** |
| `burn` | 1 | 248 | 181 | 125 | **107** |
| `burning` | 1 | 189 | 151 | 103 | **87** |
| `spark` | 1 | 100 | 68 | 56 | **50** |
| `flame` | 1 | 132 | 77 | 52 | **46** |
| `heat` | 1 | 141 | 84 | 52 | **45** |
| `sparks` | 1 | 44 | 35 | 27 | **23** |
| `bonfire` | 1 | 39 | 31 | 24 | **22** |
| `steam` | 2 | 73 | 37 | 23 | **19** |
| `black smoke` | 2 | 51 | 35 | 18 | **17** |
| `flare` | 1 | 28 | 19 | 14 | **13** |
| `campfire` | 1 | 26 | 18 | 14 | **12** |
| `candle flame` | 1 | 31 | 13 | 8 | **6** |
| `soot` | 2 | 39 | 11 | 6 | **6** |
| `smoke rising` | 1 | 7 | 6 | 5 | **5** |
| `ember` | 1 | 109 | 16 | 10 | **4** |
| `furnace` | 1 | 9 | 7 | 6 | **4** |
| `smoky` | 2 | 8 | 6 | 4 | **4** |
| `torch` | 1 | 8 | 5 | 3 | **3** |
| `smoke slow` | 2 | 1 | 1 | 1 | **1** |

Still 0 usable after both rounds: `charred` - `smoulder` - `burnt wood`

### R8_corporate_office_meeting   union 531
screened supply **447** after removing 47 off-register and 37 `forbidden_subjects` titles; this register owes **20** of the 324 video cuts. Examples of what the union is made of: *office supplies painted in green* / *four men working in an office* / *a woman working in an office*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `board` | 2 | 415 | 261 | 184 | **145** |
| `office` | 1 | 416 | 326 | 155 | **141** |
| `skyscraper` | 1 | 151 | 108 | 100 | **88** |
| `tower` | 1 | 143 | 119 | 75 | **72** |
| `office work` | 1 | 149 | 118 | 63 | **57** |
| `desk` | 1 | 197 | 142 | 55 | **39** |
| `presentation` | 1 | 116 | 38 | 37 | **31** |
| `work desk` | 1 | 101 | 78 | 34 | **26** |
| `office desk` | 1 | 101 | 71 | 27 | **25** |
| `escalator` | 1 | 43 | 40 | 31 | **23** |
| `office people` | 1 | 35 | 30 | 22 | **21** |
| `corporate` | 1 | 76 | 23 | 22 | **20** |
| `businessman` | 1 | 42 | 28 | 21 | **14** |
| `lift` | 1 | 61 | 32 | 18 | **12** |
| `meeting` | 1 | 350 | 56 | 27 | **11** |
| `office building` | 1 | 19 | 14 | 11 | **10** |
| `suit` | 1 | 40 | 25 | 21 | **10** |
| `glass building` | 1 | 17 | 14 | 8 | **8** |
| `conference` | 1 | 47 | 27 | 9 | **7** |
| `office room` | 1 | 25 | 17 | 6 | **6** |
| `business meeting` | 1 | 24 | 12 | 5 | **4** |

Still 0 usable after both rounds: `boardroom` - `elevator` - `empty office` - `meeting room` - `conference room` - `stairs office` - `lobby` - `office empty` - `empty room` - `cubicle`

### R9_paper_memo_typewriter   union 1332
screened supply **1130** after removing 81 off-register and 121 `forbidden_subjects` titles; this register owes **26** of the 324 video cuts. Examples of what the union is made of: *people handing out papers for voting* / *a man flying a paper airplane* / *a person throwing paper into the trash bin*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `paper` | 1 | 1013 | 660 | 464 | **433** |
| `sign` | 1 | 957 | 413 | 302 | **270** |
| `pen` | 1 | 577 | 378 | 246 | **177** |
| `form` | 1 | 280 | 177 | 147 | **131** |
| `book` | 1 | 419 | 293 | 135 | **121** |
| `box` | 1 | 183 | 136 | 95 | **79** |
| `library` | 2 | 146 | 134 | 84 | **65** |
| `typing` | 1 | 140 | 134 | 62 | **46** |
| `notes` | 1 | 86 | 70 | 46 | **40** |
| `writing` | 1 | 158 | 130 | 43 | **31** |
| `boxes` | 1 | 52 | 50 | 26 | **24** |
| `post` | 2 | 39 | 26 | 15 | **13** |
| `storage` | 2 | 21 | 20 | 9 | **9** |
| `document` | 1 | 111 | 105 | 8 | **8** |
| `file` | 1 | 28 | 22 | 13 | **8** |
| `shelf` | 1 | 21 | 20 | 9 | **8** |
| `page` | 1 | 60 | 30 | 8 | **7** |
| `stamp` | 1 | 15 | 12 | 7 | **6** |
| `old paper` | 1 | 33 | 21 | 6 | **5** |
| `old machine` | 2 | 8 | 6 | 5 | **5** |
| `records` | 1 | 5 | 3 | 2 | **2** |
| `papers` | 1 | 36 | 34 | 1 | **1** |
| `letter` | 1 | 138 | 54 | 1 | **1** |
| `vintage paper` | 1 | 4 | 3 | 1 | **1** |
| `vintage machine` | 2 | 2 | 2 | 1 | **1** |
| `signing` | 2 | 40 | 39 | 4 | **1** |
| `mail` | 2 | 15 | 10 | 1 | **1** |

Still 0 usable after both rounds: `documents` - `typewriter` - `old typwriter` - `files` - `folder` - `archive` - `signature` - `envelope` - `keys typing` - `binder` - `folders` - `portfolio` - `shelves` - `writing hand` - `pen paper`

### R10_press_magazine_newsprint   union 643
screened supply **444** after removing 78 off-register and 121 `forbidden_subjects` titles; this register owes **20** of the 324 video cuts. Examples of what the union is made of: *stand, news paper, road, street, news* / *stand, news paper, road, street, city* / *close up of a person pressing on a keypad*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `ink` | 1 | 766 | 449 | 396 | **322** |
| `camera` | 2 | 252 | 159 | 142 | **109** |
| `press` | 1 | 155 | 74 | 54 | **48** |
| `print` | 2 | 113 | 92 | 56 | **38** |
| `reading book` | 2 | 81 | 63 | 41 | **37** |
| `tv` | 1 | 63 | 35 | 29 | **27** |
| `printing` | 1 | 50 | 50 | 30 | **22** |
| `radio` | 1 | 57 | 32 | 20 | **18** |
| `microphone` | 1 | 26 | 17 | 15 | **15** |
| `screen tv` | 1 | 29 | 15 | 15 | **15** |
| `video camera` | 2 | 33 | 18 | 18 | **15** |
| `television` | 1 | 97 | 34 | 17 | **13** |
| `news` | 1 | 98 | 53 | 19 | **10** |
| `filming` | 2 | 9 | 9 | 8 | **7** |
| `reporter` | 1 | 10 | 8 | 7 | **6** |
| `journalist` | 1 | 6 | 5 | 5 | **5** |
| `journal` | 2 | 16 | 9 | 5 | **5** |
| `news paper` | 1 | 38 | 37 | 4 | **3** |
| `flipping` | 1 | 18 | 15 | 5 | **3** |
| `paper news` | 2 | 38 | 37 | 4 | **3** |
| `magazine` | 1 | 4 | 3 | 2 | **2** |
| `broadcast` | 1 | 9 | 2 | 1 | **1** |
| `printer` | 2 | 19 | 8 | 2 | **1** |
| `print machine` | 2 | 9 | 8 | 1 | **1** |

Still 0 usable after both rounds: `newspaper` - `print press` - `printing press` - `headline` - `camera crew` - `turning pages` - `typography` - `page turn`

### R11_government_regulator_capitol   union 549
screened supply **479** after removing 60 off-register and 10 `forbidden_subjects` titles; this register owes **12** of the 324 video cuts. Examples of what the union is made of: *majestic government building in baku azerbaijan* / *government building in baku azerbaijan* / *grand government building in baku azerbaijan*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `flag` | 1 | 593 | 530 | 484 | **453** |
| `flag wind` | 1 | 82 | 56 | 50 | **43** |
| `government` | 1 | 60 | 57 | 41 | **38** |
| `capital` | 2 | 46 | 42 | 34 | **33** |
| `flag pole` | 1 | 23 | 23 | 14 | **14** |
| `speech` | 2 | 20 | 15 | 14 | **14** |
| `usa flag` | 1 | 21 | 21 | 17 | **12** |
| `chamber` | 1 | 16 | 13 | 10 | **10** |
| `voting` | 1 | 10 | 9 | 9 | **9** |
| `parliament` | 1 | 11 | 10 | 8 | **8** |
| `washington` | 1 | 29 | 26 | 11 | **7** |
| `seal` | 1 | 19 | 13 | 8 | **6** |
| `government building` | 2 | 19 | 18 | 5 | **5** |
| `capitol` | 1 | 37 | 35 | 3 | **1** |
| `congress` | 1 | 2 | 2 | 1 | **1** |
| `official` | 1 | 4 | 1 | 1 | **1** |
| `state building` | 1 | 17 | 17 | 2 | **1** |
| `federal` | 1 | 12 | 6 | 1 | **1** |
| `assembly` | 1 | 18 | 2 | 2 | **1** |
| `hearing` | 1 | 7 | 1 | 1 | **1** |
| `podium` | 1 | 6 | 3 | 1 | **1** |

Still 0 usable after both rounds: `senate` - `lectern` - `microphone stand`

### R12_courthouse_stone_columns   union 774
screened supply **610** after removing 55 off-register and 109 `forbidden_subjects` titles; this register owes **18** of the 324 video cuts. Examples of what the union is made of: *an abandoned fenced court* / *wild bird, wren, natural, male, courtship dance, whisper, japan* / *spider, web, nature, arachnid, scary, hairy, animals, at the court of, inverte*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `arch` | 2 | 838 | 651 | 510 | **468** |
| `architecture` | 1 | 625 | 532 | 420 | **408** |
| `temple` | 2 | 202 | 174 | 157 | **130** |
| `stone` | 2 | 168 | 119 | 86 | **82** |
| `trial` | 1 | 178 | 117 | 50 | **38** |
| `dome` | 1 | 45 | 29 | 27 | **26** |
| `statue` | 1 | 57 | 48 | 28 | **25** |
| `law` | 1 | 229 | 69 | 22 | **21** |
| `court` | 1 | 57 | 39 | 22 | **14** |
| `monument` | 1 | 29 | 21 | 14 | **13** |
| `historic building` | 1 | 30 | 21 | 9 | **7** |
| `stairs` | 2 | 45 | 31 | 7 | **7** |
| `stone wall` | 2 | 16 | 12 | 6 | **6** |
| `city hall` | 2 | 18 | 13 | 4 | **4** |
| `marble` | 1 | 11 | 9 | 4 | **3** |
| `old building` | 1 | 77 | 61 | 3 | **3** |
| `facade` | 1 | 23 | 19 | 3 | **3** |
| `justice` | 1 | 29 | 23 | 2 | **2** |
| `staircase` | 1 | 7 | 7 | 1 | **1** |
| `column` | 2 | 9 | 8 | 1 | **1** |
| `steps` | 2 | 11 | 8 | 1 | **1** |
| `staircase` | 2 | 7 | 7 | 1 | **1** |

Still 0 usable after both rounds: `courthouse` - `courtroom` - `columns` - `stone columns` - `classical building` - `stone stairs` - `pillar` - `civic building` - `old courthouse` - `law court` - `colonnade` - `stone building` - `neoclassical` - `pillars` - `town hall` - `municipal`

### R13_indiana_farmland_smalltown   union 772
screened supply **599** after removing 77 off-register and 96 `forbidden_subjects` titles; this register owes **18** of the 324 video cuts. Examples of what the union is made of: *farmer harvesting in lush green field* / *farmer* / *farmers preparing land on a tractor in pakistan*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `street` | 2 | 730 | 615 | 374 | **350** |
| `town` | 2 | 276 | 218 | 143 | **125** |
| `field` | 1 | 349 | 247 | 126 | **107** |
| `farm` | 1 | 203 | 142 | 104 | **94** |
| `downtown` | 2 | 77 | 59 | 42 | **41** |
| `meadow` | 1 | 103 | 57 | 42 | **37** |
| `rural` | 1 | 146 | 104 | 32 | **28** |
| `village` | 1 | 81 | 47 | 34 | **25** |
| `countryside` | 1 | 104 | 73 | 29 | **24** |
| `houses` | 1 | 94 | 52 | 27 | **17** |
| `road town` | 2 | 28 | 22 | 20 | **17** |
| `town street` | 1 | 44 | 36 | 18 | **16** |
| `street town` | 2 | 44 | 36 | 18 | **16** |
| `farmland` | 1 | 30 | 18 | 14 | **14** |
| `country road` | 1 | 60 | 47 | 17 | **14** |
| `corn` | 1 | 38 | 23 | 13 | **13** |
| `suburb` | 1 | 50 | 47 | 11 | **8** |
| `tractor` | 1 | 28 | 14 | 11 | **7** |
| `grain` | 1 | 38 | 20 | 14 | **7** |
| `wheat` | 1 | 40 | 25 | 8 | **5** |
| `porch` | 2 | 30 | 17 | 4 | **4** |
| `barn` | 1 | 10 | 4 | 4 | **3** |
| `harvest` | 1 | 27 | 14 | 6 | **3** |
| `midwest` | 1 | 4 | 2 | 2 | **2** |
| `wooden house` | 2 | 17 | 6 | 2 | **2** |
| `house front` | 2 | 8 | 8 | 2 | **2** |
| `silo` | 1 | 2 | 2 | 1 | **1** |
| `prairie` | 1 | 3 | 1 | 1 | **1** |

Still 0 usable after both rounds: `corn field` - `small town` - `main street` - `farmhouse` - `front porch` - `maize` - `crop field` - `farm house` - `old house` - `veranda`

### R14_money_cost_arithmetic   union 717
screened supply **544** after removing 66 off-register and 107 `forbidden_subjects` titles; this register owes **12** of the 324 video cuts. Examples of what the union is made of: *close up of barista taking money from a customer* / *a woman putting money on the briefcase* / *australian money*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `money` | 1 | 464 | 412 | 340 | **306** |
| `graph` | 1 | 468 | 263 | 240 | **204** |
| `bank` | 1 | 239 | 205 | 177 | **147** |
| `cash` | 1 | 191 | 176 | 157 | **133** |
| `coin` | 1 | 282 | 222 | 194 | **127** |
| `dollar` | 1 | 189 | 171 | 154 | **115** |
| `coins` | 1 | 168 | 140 | 118 | **60** |
| `counting` | 1 | 120 | 92 | 42 | **33** |
| `chart` | 1 | 94 | 41 | 35 | **27** |
| `banknote` | 1 | 41 | 39 | 31 | **25** |
| `numbers` | 2 | 114 | 28 | 25 | **22** |
| `payment` | 2 | 20 | 16 | 12 | **9** |
| `statistics` | 1 | 25 | 8 | 8 | **8** |
| `math` | 2 | 41 | 11 | 8 | **8** |
| `book page` | 2 | 49 | 23 | 5 | **5** |
| `invoice` | 1 | 4 | 4 | 4 | **4** |
| `calculator` | 1 | 45 | 29 | 7 | **2** |
| `accounting` | 1 | 4 | 2 | 2 | **2** |
| `till` | 1 | 16 | 4 | 4 | **2** |
| `price` | 1 | 25 | 8 | 8 | **2** |
| `accounts` | 2 | 2 | 2 | 2 | **2** |
| `receipt` | 1 | 4 | 4 | 3 | **1** |
| `shop counter` | 2 | 2 | 2 | 2 | **1** |

Still 0 usable after both rounds: `abacus` - `adding machine` - `ledger` - `cash register` - `typing numbers` - `office machine`

### R15_crowd_public_anonymous   union 855
screened supply **641** after removing 65 off-register and 149 `forbidden_subjects` titles; this register owes **14** of the 324 video cuts. Examples of what the union is made of: *crowd gathering at indoor music concert venue* / *a crowd of commuters walking in a tunnel* / *vibrant city scene with crowded urban streets*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `people` | 1 | 881 | 592 | 450 | **410** |
| `line` | 2 | 666 | 472 | 411 | **374** |
| `street people` | 1 | 114 | 95 | 60 | **57** |
| `walking people` | 1 | 118 | 112 | 66 | **57** |
| `people walking` | 1 | 118 | 112 | 66 | **57** |
| `pedestrian` | 1 | 52 | 48 | 37 | **36** |
| `crowd` | 1 | 126 | 47 | 31 | **29** |
| `busy street` | 1 | 37 | 35 | 27 | **25** |
| `office people` | 1 | 35 | 30 | 22 | **21** |
| `row people` | 2 | 67 | 24 | 19 | **18** |
| `crossing` | 1 | 43 | 33 | 23 | **15** |
| `line people` | 1 | 19 | 14 | 12 | **12** |
| `group people` | 1 | 28 | 17 | 11 | **10** |
| `seats` | 2 | 22 | 16 | 11 | **10** |
| `sidewalk` | 1 | 29 | 27 | 10 | **9** |
| `waiting` | 1 | 49 | 33 | 14 | **6** |
| `commuters` | 1 | 5 | 5 | 2 | **2** |
| `gathering` | 1 | 2 | 2 | 1 | **1** |
| `hall people` | 2 | 1 | 1 | 1 | **1** |

Still 0 usable after both rounds: `queue` - `audience`

### R16_hands_backs_figures   union 666
screened supply **524** after removing 61 off-register and 81 `forbidden_subjects` titles; this register owes **20** of the 324 video cuts. Examples of what the union is made of: *counting currency notes in hand close up* / *handheld shot of spotlights* / *group of people shaking hands*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `hand` | 1 | 824 | 498 | 329 | **237** |
| `arm` | 1 | 501 | 294 | 218 | **188** |
| `hands` | 1 | 377 | 291 | 201 | **149** |
| `holding` | 1 | 266 | 253 | 140 | **110** |
| `man walking` | 1 | 250 | 233 | 118 | **97** |
| `man hand` | 1 | 177 | 108 | 77 | **51** |
| `woman walking` | 1 | 66 | 60 | 33 | **30** |
| `silhouette` | 1 | 154 | 86 | 33 | **29** |
| `hand close` | 1 | 75 | 65 | 30 | **24** |
| `person walking` | 1 | 57 | 54 | 24 | **22** |
| `gloves` | 1 | 29 | 29 | 25 | **18** |
| `hands close` | 1 | 40 | 36 | 17 | **16** |
| `fingers` | 1 | 40 | 22 | 19 | **9** |
| `hands person` | 1 | 18 | 16 | 9 | **7** |
| `back person` | 1 | 7 | 5 | 4 | **3** |
| `shoulder` | 1 | 1 | 1 | 1 | **1** |
| `worker hands` | 1 | 3 | 3 | 1 | **1** |


### R17_clock_calendar_time   union 1417
screened supply **989** after removing 96 off-register and 332 `forbidden_subjects` titles; this register owes **10** of the 324 video cuts. Examples of what the union is made of: *a person turning off the alarm clock in the smartphone* / *Big Ben clock time lapse* / *Woman turning off her alarm clock in the morning*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `sunset` | 1 | 976 | 746 | 632 | **553** |
| `time` | 1 | 924 | 635 | 475 | **395** |
| `time lapse` | 1 | 473 | 444 | 334 | **266** |
| `sunrise` | 1 | 449 | 243 | 189 | **162** |
| `winter` | 1 | 501 | 254 | 163 | **144** |
| `timelapse` | 1 | 186 | 177 | 131 | **116** |
| `night sky` | 1 | 152 | 121 | 97 | **91** |
| `watch` | 1 | 185 | 115 | 94 | **87** |
| `autumn` | 1 | 290 | 173 | 110 | **83** |
| `dawn` | 1 | 97 | 65 | 52 | **50** |
| `season` | 1 | 77 | 20 | 18 | **18** |
| `clock` | 1 | 231 | 69 | 18 | **17** |
| `timer` | 1 | 121 | 20 | 19 | **17** |
| `hourglass` | 1 | 20 | 16 | 14 | **13** |
| `date` | 2 | 38 | 19 | 12 | **11** |
| `days` | 2 | 14 | 9 | 8 | **8** |
| `second hand` | 1 | 6 | 5 | 4 | **4** |
| `stars time` | 1 | 6 | 6 | 4 | **4** |

Still 0 usable after both rounds: `wall clock` - `calendar` - `clock face` - `old clock` - `month`

### R18_wreck_salvage_aftermath   union 211
screened supply **171** after removing 17 off-register and 23 `forbidden_subjects` titles; this register owes **10** of the 324 video cuts. Examples of what the union is made of: *person walking on a junkyard* / *a white car on a junkyard* / *elevated cars on a junkyard at night*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `scrap` | 1 | 158 | 112 | 104 | **91** |
| `abandoned` | 1 | 241 | 151 | 48 | **43** |
| `ruin` | 1 | 78 | 51 | 35 | **33** |
| `ruins` | 2 | 62 | 40 | 32 | **31** |
| `broken` | 1 | 56 | 47 | 23 | **20** |
| `rust` | 1 | 75 | 37 | 14 | **12** |
| `pile` | 1 | 27 | 25 | 14 | **10** |
| `debris` | 1 | 19 | 17 | 9 | **8** |
| `decay` | 1 | 37 | 28 | 9 | **8** |
| `waste` | 2 | 15 | 9 | 7 | **7** |
| `old metal` | 1 | 29 | 11 | 5 | **5** |
| `trash` | 2 | 12 | 9 | 5 | **5** |
| `junk` | 1 | 6 | 5 | 4 | **4** |
| `junkyard` | 1 | 4 | 4 | 4 | **4** |
| `garbage` | 2 | 14 | 4 | 4 | **3** |
| `rusty` | 1 | 14 | 13 | 2 | **2** |
| `abandoned car` | 1 | 9 | 5 | 3 | **2** |
| `dump` | 1 | 11 | 6 | 4 | **2** |
| `empty building` | 2 | 36 | 35 | 2 | **2** |
| `wasteland` | 1 | 1 | 1 | 1 | **1** |

Still 0 usable after both rounds: `scrap metal` - `derelict` - `landfill` - `corroded` - `metal scrap` - `steel scrap` - `rusted` - `oxidized`

### R19_television_1970s_media   union 167
screened supply **119** after removing 15 off-register and 33 `forbidden_subjects` titles; this register owes **10** of the 324 video cuts. Examples of what the union is made of: *A thug in a pink suit kicks and hits an old TV with a bat* / *purple static background with wavy patterns* / *static screen*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `film` | 2 | 230 | 80 | 59 | **33** |
| `cinema` | 2 | 82 | 40 | 32 | **28** |
| `studio` | 2 | 58 | 34 | 26 | **23** |
| `glitch` | 2 | 38 | 21 | 18 | **18** |
| `old footage` | 2 | 24 | 23 | 18 | **16** |
| `tv screen` | 2 | 29 | 15 | 15 | **15** |
| `old video` | 2 | 19 | 18 | 14 | **12** |
| `retro tv` | 1 | 16 | 11 | 10 | **10** |
| `analog` | 1 | 37 | 18 | 9 | **8** |
| `grain` | 2 | 38 | 20 | 14 | **7** |
| `noise screen` | 1 | 22 | 12 | 5 | **5** |
| `antenna` | 1 | 11 | 7 | 6 | **5** |
| `screen noise` | 2 | 22 | 12 | 5 | **5** |
| `static` | 1 | 18 | 12 | 6 | **4** |
| `projector` | 1 | 18 | 5 | 4 | **4** |
| `reel` | 2 | 51 | 15 | 11 | **4** |
| `vintage film` | 1 | 17 | 14 | 4 | **3** |
| `vhs` | 1 | 21 | 4 | 3 | **2** |
| `old tv` | 1 | 6 | 2 | 1 | **1** |

Still 0 usable after both rounds: `vintage tv` - `crt` - `broadcast studio` - `film reel` - `old film` - `8mm film` - `super 8` - `archival` - `grain film` - `old television` - `news studio` - `film grain` - `retro film` - `8mm` - `vintage footage` - `home movie` - `nostalgia` - `1970s` - `archive footage` - `historic footage` - `scratched film`

### R20_dusk_weather_quiet   union 1278
screened supply **961** after removing 73 off-register and 244 `forbidden_subjects` titles; this register owes **18** of the 324 video cuts. Examples of what the union is made of: *a house is seen at dusk by the water* / *calm ocean waves at dusk serene sea footage* / *silhouetted figures on abandoned structure at dusk*

| query | round | title-AND | on disk | unused | >=1920x1080 & unused |
|---|:--:|---:|---:|---:|---:|
| `clouds` | 2 | 861 | 642 | 522 | **500** |
| `rain` | 1 | 1081 | 649 | 363 | **312** |
| `wind` | 1 | 906 | 463 | 207 | **186** |
| `fog` | 1 | 516 | 262 | 131 | **121** |
| `dusk` | 1 | 137 | 101 | 73 | **69** |
| `cloudy` | 1 | 99 | 79 | 58 | **53** |
| `twilight` | 1 | 70 | 50 | 40 | **39** |
| `raining` | 2 | 119 | 61 | 47 | **37** |
| `mist` | 1 | 252 | 134 | 43 | **36** |
| `cloudy sky` | 1 | 46 | 42 | 31 | **26** |
| `alley` | 2 | 75 | 60 | 27 | **25** |
| `lantern` | 2 | 42 | 35 | 27 | **23** |
| `street night` | 1 | 135 | 123 | 20 | **20** |
| `street light` | 2 | 68 | 59 | 23 | **20** |
| `lamp` | 2 | 64 | 39 | 15 | **13** |
| `dark clouds` | 1 | 21 | 17 | 10 | **10** |
| `wet` | 2 | 93 | 36 | 11 | **9** |
| `haze` | 1 | 38 | 9 | 6 | **6** |
| `overcast` | 1 | 24 | 21 | 2 | **2** |
| `rain window` | 1 | 132 | 44 | 3 | **2** |
| `empty street` | 1 | 27 | 23 | 2 | **2** |
| `street empty` | 2 | 27 | 23 | 2 | **2** |
| `gray sky` | 1 | 2 | 2 | 1 | **1** |

Still 0 usable after both rounds: `grey sky` - `drizzle` - `quiet street` - `street lamp` - `sky grey`

---

## 5. The cut budget, checked so the contract is satisfiable

EP66 declared a contract its own cut budget could not satisfy — 350 distinct video assets against a
video-cut ceiling of 311 — and that arithmetic was only found after the plan was written. It is done
first here.

```
runtime band (episode_spec)                        1560 .. 1895 s      (design centre 1762.5 s)
target_cut_sec (episode_spec)                              3.7 s
total cuts                    1560/3.7 = 421     1762.5/3.7 = 476      1895/3.7 = 512
stills may occupy at most 32% of cuts                      134                  152         163
video cuts available          421-134 = 287      476-152 = 324         512-163 = 349
mandatory_stills declared                                  104         -> fits at every edge
distinct_video_assets declared                             265         -> fits at every edge
video cuts this plan allocates (s2)                        324         -> the design-centre figure
```

**265 distinct sources over 324 video cuts** gives a distinct fraction of **0.818** against the
`footage_diversity` floor of **0.40**, and leaves 59 second uses to spread — comfortably inside the
`reuse <= 4` cap and the `generic symbols <= 2` cap. `footage_utilization` wants **>= 80%** of staged
clips actually used; **staging 300–330 against 265 required keeps that reachable, and staging 11,089
would not. Do not stage the screened pool.**

`animation_density` (near-still <= 10% of runtime, single hold <= 3.0 s) and `motion_density`
(>= 2.5 kinetic beats/min, coverage >= 0.25, variety >= 3) are met by the motion budget in the film
bible §6, §10 and §12.5, not by this document. What this document owes them is **enough distinct
moving footage that no cut has to be a held still**, and 324 video cuts at 3.7 s is that.

**One deliberate exception, declared here so nobody treats it as a defect.** Film bible §3.5 puts
**fifteen seconds with no picture at all** at A2-05 — black, sound cut, one line of the opinion set
as type. That is the moment of the collision, which this film refuses to show. It is black, not a
held still, so `animation_density` does not see a near-still span; but a reviewer who does not know
it is deliberate will report it as a fault. **It is in the design, it is in this plan, and it is the
strongest fifteen seconds available.**

---

## 6. Screening rules a machine cannot apply, and who applies them

`footage_review_required` is **true** in the contract. These are the judgements a person makes over
a labelled contact sheet before any clip enters a cut. The factory shelf's filename labels have
measured **~40–50% wrong**, and 683 of 1,094 clips across five earlier episodes were wrong for their
story when somebody finally looked.

1. **Look at R6 and R12 first.** They are the two registers whose numbers most overstate their
   supply. R6's 865 is mostly `hit` (641) and waves crashing on rocks; R12's 610 is mostly `arch`
   (468), which is European and religious architecture. **Both will look healthy to every machine
   gate and neither is what the script asked for.**
2. **Period, every clip, no exceptions.** `era_setting` is **1968–1981**. Reject on sight: LED
   headlights and daytime running lights, flat-screen monitors, mobile phones, modern motorway
   gantries and signage, euro number plates, contemporary clothing, bicycle lanes, solar panels,
   modern office glass. **This is the failure mode most likely to reach a finished cut**, because
   nothing machine-readable can see it and the shelf is overwhelmingly contemporary.
3. **No crash, no fire, no smoke, no injury, no hospital, in any clip, at any point.** The contract
   blocks them by title; a human blocks them by looking. A film about a woman who died of burns and
   a 13-year-old who survived them cannot cut to stock fire footage, and the same rule applies to a
   staged crash test.
4. **No vehicle identity.** No badge, no oval, no nameplate, no model script, no grille emblem, no
   licence plate, no dealership signage. If a clip shows a car, the car must be unidentifiable as a
   make — and it must never be, or resemble, a Pinto presented as the Pinto.
5. **No courtroom interior, re-enacted or stock.** Everything the two courts did in this story is
   text — an opinion, a footnote, a verdict. Stock "courtroom" footage is a television set and it
   would be the one place this film pretends. The courts are exteriors, stone, doors and typography.
6. **No screen that can be read**, no legible document, no legible newspaper front page. A legible
   page next to this narration reads as *the actual memo*, which is barred outright (⛔-15,
   invariant 11).
7. **People: required, and faces are allowed** — see §7. What is barred is a *real, identifiable
   individual's likeness*, and above all anything a viewer could take for Richard Grimshaw, Lilly
   Gray, the Ulrich sisters and their cousin, the van driver, or any named Ford employee, judge or
   lawyer.
8. **No-repeat, across the film and across the channel.** Within the film, a clip is used at most
   twice unless the repetition is an argument the bible names — the five hero objects in §3 are the
   only deliberate motif returns. Across the channel, §1 filter 7 has already excluded every id
   another episode holds; before staging, re-run
   `py -3.11 scripts/check_cross_episode_reuse.py --build` so `STAGED_CLIP_INDEX.json` is current,
   because the count moved by 71 ids during EP67's measurement alone and stands at 9,780 today.

### The staging command

```bash
# dry run first, always
py -3.11 scripts/stage_footage_by_title.py --slug pinto --per-query 3 --dry-run \
  --query "car road" --query "vintage car" --query "highway" --query "factory" ...

# then the contact sheet, then a person looks at it, then the pool is trimmed
py -3.11 scripts/search_archive.py --shot "empty three lane highway middle lane" \
  --kind video --sheet --limit 24
```

---

## 7. The people lane — required, not tolerated

**Owner decision 2026-07-04: depicted people are REQUIRED and welcome. The only thing barred is the
likeness of a real, identifiable individual** (CLAUDE invariant 11). This is a film about engineers
at drawing boards, a committee in a meeting room, a jury that sat for six months and a country that
read a magazine; a version of it with nobody in it would be absurd, and EP60 shipped exactly that
and was wrong.

- `episode_spec.people_plates_min` = **24**, and `episode_spec.people_plates` names them:
  **R081–R104**. That is a declared list, not a filename convention, because
  `check_episode_inputs` once reported 0 of 10 on forty plates that existed and were correct.
- **Register R16 (hands, backs, figures) owes 20 of the 324 video cuts**, and it is the only
  register whose clips are all review-required by default: a title that names a human is a
  candidate, never supply.
- **Faces are allowed in generated plates.** What is not allowed is a face presented as a specific
  real person in this record. The image order's rule is: a face may appear when it belongs to
  nobody in the story — a passer-by, a crowd, a worker at a different bench — and must not appear in
  any plate captioned or cut as Grimshaw, Lilly Gray, the Ulrich family, the van driver, a Ford
  employee, a judge or a lawyer.

---

## 8. What must happen next, in order

1. Re-run `scripts/check_cross_episode_reuse.py --build`; the staged-id count is moving and stands
   at 9,780.
2. Stage 300–330 clips with `--dry-run` first, from the §4 queries with the highest **screened**
   counts in each register, **not** from the highest raw counts.
3. Build labelled contact sheets and **have a person look at them, starting with R6, R12 and R19.**
   Record a verdict per clip; `footage_review_required` is true and a stamped-without-looking QC is
   the failure this contract exists to stop.
4. Commission the four generated-plate groups in §3 (R001–R080), which the archive cannot supply,
   plus the people lane R081–R104. That is the whole of `mandatory_stills`.
5. Only then build `pinto_film.json`, and run `check_spec_satisfied.py` before the render.

*Measured 2026-08-11 in one ledger pass. 623 queries, two rounds, 84 zeros re-asked in other words
before any of them was recorded as a gap, and 153 still zero at the end. One register measured and
refused. Nothing was staged and nothing was moved.*
