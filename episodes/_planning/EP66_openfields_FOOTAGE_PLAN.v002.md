# EP66 · THE OPEN-FIELDS DOCTRINE — FOOTAGE QUERY PLAN v002

**Date 2026-08-10 · slug `openfields` · episode `PD-2026-066-openfields`**
**Contract `episodes/PD-2026-066-openfields/episode_spec.v001.json` (as corrected 2026-08-10:
`mandatory_stills` L070–L254 = 185 ids, `people_plates` L235–L254 = 20 ids, `face` / `portrait` /
`headshot` no longer in `forbidden_subjects`)**
**Script `episodes/_planning/EP66_openfields_script.en.v003.md` · bible
`EP66_openfields_FILM_BIBLE.v001.md` · narration master measured at 1598.038 s**

> **Why v002 and not v001.** `EP66_openfields_FOOTAGE_PLAN.v001.md` already exists and is the
> written record of a completed staging round — 338 clips staged, 203 accepted, 135 rejected each
> with a reason, 17 pool sheets, 5 face-check sheets, a pixabay blind probe. Overwriting it would
> destroy measured evidence (CLAUDE invariant 6, rule 05). v001 stands. This file is the query plan
> for the **corrected** contract, which v001 predates: v001 was written against a target of 60
> accepted clips, and the contract now asks for 350 distinct video sources.
>
> **Nothing here was staged, copied, transcoded or ffprobed.** Every number was produced by reading
> the ledgers and the resolution index. Three long-form renders were running.

---

## 0. Result in one block

```
contract distinct_video_assets                      308
distinct video sources in hand today                203   (accepted archive) + 0 (motion) = 203
hard pre-flight floor  350 // 2                     175   -> ALREADY MET (203 >= 175)
new unused >=1920x1080 clips this plan reaches      760   (313 queries, --per-query 4)
i2v motion plates the arithmetic actually forces     21   (see the finding in section 5)
```

**The binding constraint is not the shelf.** It is the builder's cut budget, and it makes the
contract as written unsatisfiable at the pre-revision `target_cut_sec` of 3.5. Path A was taken on 2026-08-11 and the spec now declares 3.1; the arithmetic below is kept as the record of that decision. Section 5 shows the arithmetic and the
two legal fixes. Read that before staging anything.

---

## 1. The instrument, verified before any zero was trusted

`scripts/search_archive.py` does **not** call `shelf_rows()`. It walks `H:\pd-media\assets\archive\_ledger`
itself (`main()` L413-416), skipping only `rejects*`, `*_dedup_removed.jsonl` and `*_candidates.jsonl`.
It has no `include_factory` switch and **does not exclude `factory.jsonl`** — so it takes the
`include_factory=True` path by construction. The 58%-blind failure of `build_archive_inventory.py`
/ `qc_archive_contact_sheets.py` / `qc_audio_stats.py` does not apply to it, and none of the zeros
below is a factory-blindness artifact.

Measured, video rows visible to that enumeration:

```bash
py -3.11 -c "import json,os,collections;D=r'H:\pd-media\assets\archive\_ledger';VID={'.mp4','.mov','.webm','.mkv','.avi','.mpeg','.mpg'};per=collections.Counter();tot=0
for fn in sorted(os.listdir(D)):
    if not fn.endswith('.jsonl') or fn.startswith('rejects') or fn.endswith(('_dedup_removed.jsonl','_candidates.jsonl')): continue
    n=0
    for line in open(os.path.join(D,fn),encoding='utf-8',errors='replace'):
        try: r=json.loads(line)
        except Exception: continue
        if os.path.splitext(str(r.get('file_path','')))[1].lower() in VID: n+=1
    if n: per[fn]=n; tot+=n
print(tot); [print(f'  {k:24}{v:7,}  {100*v/tot:5.1f}%') for k,v in per.most_common()]"
```

```
40,480 video rows visible to search_archive.py
  pixabay_extra.jsonl    18,275   45.1%
  factory.jsonl          15,683   38.7%     <- the lane the three broken counters hide
  mixkit.jsonl            2,588    6.4%
  ia.jsonl                2,211    5.5%
  nara.jsonl                837    2.1%
  nasa.jsonl                630    1.6%
  noaa.jsonl                114    0.3%
  stock.jsonl                74    0.2%
  coverr.jsonl               68    0.2%
```

### 1.1 What the counts in section 4 actually are

`search_archive.py --shot` is a *ranked* path with its own score floor. The tool that actually puts
clips in the pool is `scripts/stage_footage_by_title.py`, and it selects differently: every query
term must be a **substring of the lowercase title**, the licence must be in
`{free_commercial, pd, cc0}`, `TITLE_BLOCK` and `RIP_SIGNATURE` must not match, size must be
1–120 MB, the file must exist, and the clip id must not already sit in **any** episode's
`factory*` folder.

So the counts in section 4 were produced by replicating that selection exactly, over one pass of
the ledger instead of 313 passes. Script:
`E:\UserTemp\aab15\claude\C--Users-aab15\d654d1fe-e458-4466-83a4-f13b171f9f50\scratchpad\measure_openfields.py`.
Every row it reports is a clip staging would really take.

Cross-episode reuse (owner complaint 4, `footage_diversity`) is therefore **already subtracted**:
**8,521 clip ids are held by some episode's `factory*` folder** (338 of them by openfields itself),
and not one of them is counted as supply anywhere below.

```
candidate rows after the static filters      34,395
ids already consumed by some episode          8,521
hard-blocklist ids excluded                      41   (config/footage_blocklist.v001.json "blocked",
                                                       incl. AR-10159563)
```

### 1.2 Duration is deferred

No ledger row carries a duration and `_ledger/video_resolution.json` holds `{w,h}` only. Getting
duration means ffprobing thousands of files on H: while three renders are running. **Deferred, not
estimated.** Resolution *is* reported: every count marked `>=1920x1080` was filtered against that
index, which covers 31,107 videos.

---

## 2. The registers, derived from this script's own sections

Measured per-section speech seconds from `06_audio/narration_index.v001.json` (275 chunks,
1,488.5 s of speech inside a 1,598.038 s master):

| section | speech s | share | video cuts @351 |
|---|---:|---:|---:|
| HOOK | 11.8 | 0.8% | 3 |
| OP | 1.3 | 0.1% | 1 |
| ACT_1 | 304.9 | 20.5% | 72 |
| ACT_2 | 227.0 | 15.2% | 53 |
| ACT_3 | 289.4 | 19.4% | 68 |
| ACT_4 | 343.0 | 23.0% | 81 |
| ACT_5 | 244.5 | 16.4% | 58 |
| ENDING | 66.6 | 4.5% | 15 |

Nineteen registers. This is not the generic list: R14–R19 do not exist in v001's plan, and R17
(wildlife) was actively suppressed there, which was wrong — `PA-35`, `PA-05` and the ENDING's
*"Wildlife is what both of these records are filed under"* make it a register the film argues from.

| # | register | what it is for | cuts | script beats it serves |
|---|---|---|---:|---|
| R1 | gate, chain, padlock | the motif. States 1–7. The object the whole film points at | 19 | HOOK img 2; ACT_1 *"a chained gate of his own"*, motif 1 & 2; ACT_4 *"installed locked gates at all public entrances"*, motif 4 & 5; ENDING motif 7 |
| R2 | fence line, wire, posts | what the law now measures: steps taken to exclude | 23 | ACT_1 *"sixty-nine acres on Liberty Road, fenced all the way around"*; ACT_4 PA-07 *"fenced … with waist-high, metal wire"*; ACT_5 PA-28 |
| R3 | posted boundary, placard, purple paint | the sign the statute names *in order to disregard it* | 14 | ACT_1 *"with a No Trespassing sign on it"*; ACT_4 PA-07, PA-10 purple paint; ACT_4 *"named in order to be disregarded"* |
| R4 | open field, pasture, crops, grass | the ninety-three acres; *wild or waste lands*; *rural, undeveloped land* | 49 | ACT_1 arithmetic on 93 acres; ACT_3 TN-32; ACT_5 ND-02 |
| R5 | woodland, trunk, bark, canopy | the tree the camera went on; the Pennsylvania hard cut | 51 | HOOK *"single trunk in mid-ground woodland"*; ACT_1 TN-16 cut branch; ACT_4 Appalachian hardwood, 4,400 + 1,100 acres |
| R6 | tracks, lanes, gravel drive | access, and the visits he stopped making | 26 | ACT_1 *"his neighbour's private gravel drive"*, *"reduced his visits"*; ACT_3 ⟨HELD⟩ *"the empty track, still"* |
| R7 | rain, wet ground, mud, prints | motif state 3 and the 5-second silence; the boot prints beyond the lock | 14 | ACT_3 motif 3 *"the padlock wet, the chain wet, the track empty"*; ACT_1 motif 2 |
| R8 | sky, fog, overcast, low light | the four silences; *a different light* across the turn | 33 | ACT_3/4/5 ⟨HELD⟩ ×4; ACT_4 the hard cut |
| R9 | figures on the land, no face | use and occupation by a person, **review-required** | 12 | HOOK *"boots passing behind, no face"*; ACT_1 *"go to their own ground less than they used to"* |
| R10 | farm work, tractor, hay, barn, livestock | *"farmed in a regular and conspicuous manner"* — the fact that decided the case | 18 | ACT_2 TN-09; ACT_3 TN-30/TN-31 *"constitute actual use of the property"* |
| R11 | creek, stream, pond, fishing | one of the four uses the appellate judges counted | 14 | ACT_1 *"fishing, farming, camping and hunting"*; ACT_3 TN-30 |
| R12 | camping, fire, cabin, lantern | *a private place — a sanctuary*; camping as occupation | 10 | ACT_4 PA-04; ACT_1 *"previously more regularly camped"* |
| R13 | a building seen from far off | the curtilage — *"a narrow ring around a house"*; the two homes; the nine-acre tract with a pool | 12 | ACT_1 curtilage; ACT_2 TN-09 *"two homes on it"*; ACT_5 ND-02 |
| R14 | trail camera, lens, cut branch | the film's title image and its 78-day payoff | 9 | HOOK *"the three branch/camera plates"*; ACT_1 TN-16; ACT_4 PA-13 |
| R15 | old paper, quill, brick, historic town | *"customs officials more than two centuries ago in colonial Boston"*; the general-warrants clause | 10 | ACT_3 TN-37, TN-23 read whole |
| R16 | timelapse, seasons, shadows | *seventy-eight days*, *twenty-three months*, *since 2013* | 9 | ACT_4 PA-13, PA-12; ACT_2 the two dates |
| R17 | deer, elk, birds — living wildlife | what both statutes are filed under; *spook nearby wildlife* | 9 | ACT_4 PA-05, illegal elk feeding; ACT_5 PA-35; ENDING TN-01 |
| R18 | books, code, files, library | *"The statute is still in the Tennessee code"*; the two provisions struck | 7 | ACT_3, ACT_5, ENDING |
| R19 | ridge, valley, county, state line | *"Each ruling stops at its own state line"*; the two geographies | 12 | ACT_4 Clearfield County; ACT_5; ENDING |
|  | **total** |  | **351** | |

**Hard constraints that bind every register.** `forbidden_subjects` is matched by
`check_spec_satisfied.py` against the **source filename**, word-wise. So a clip whose title carries
`drone`, `police`, `gun`, `rifle`, `gavel`, `courtroom`, `prison`, `handcuffs`, `hourglass`,
`handshake`, `child`, `children`, `baby` is an automatic build failure — and 64 of the 760 union
clips carry `aerial|drone|flyover|top view`. An aerial whose title does *not* contain `drone`
passes the machine gate; that is a judgement, not a licence. The HOOK is written on an
*"archive aerial farmland at low sun"*, so this needs an owner line, not a silent pick.

---

## 3. The zeros, and the retries that were run before any of them was recorded as a gap

**149 phrasings returned 0** across two rounds — 44 in round 1, 105 in the retry round. Every
register that produced a zero was re-asked in at least three differently-worded ways before
anything was called a gap. The retries are the reason this plan is not v001's plan.

The measured wins:

| director's phrasing | hits | supplier phrasing that worked | hits (≥1080p, unused) |
|---|---:|---|---:|
| `farm gate` · `gate road` · `latch` · `bolt rusty` · `hinge` · `hinges` · `door latch` · `cattle gate` · `livestock gate` · `gate wooden old` · `gate rural` | **0** | `lock chain` | **31** |
| " | | `gate` | **25** |
| " | | `chain fence` | **8** |
| " | | `old lock` · `iron chain` | **7** · **6** |
| `fence post` · `post fence` · `wooden posts` · `pole wooden` · `split rail` · `barbwire` · `chicken wire` · `palisade` | **0** | `fence` | **67** |
| " | | `wire` | **50** |
| " | | `barb wire` · `fencing` | **2** · **2** |
| `boundary` · `private property` · `sign rusty` · `notice board` · `marker post` · `signpost` · `sign nailed` · `prohibited sign` · `restricted` | **0** | `old sign` · `sign tree` | **13** · **12** |
| " | | `signage` · `warning` · `sign board` | **7** · **6** · **6** |
| `blaze tree` · `spray paint tree` · `marking tree` · `paint on wood` · `violet paint` | **0** | `purple paint` | **4** (all paint splashes — see G2) |
| `hay field` · `stubble` · `seed heads` · `ploughed field` · `plough` · `tilled` · `furrow` · `bare soil` · `mown` · `grass heads` · `overgrown` | **0** | `oats` | **47** |
| " | | `wild grass` | **27** |
| " | | `straw` · `hay` · `haystack` | **5** · **4** · **1** |
| `leaf litter` · `birch` · `birch trees` · `hardwood` · `hardwood forest` · `deciduous` · `broadleaf` · `bare forest` · `leafless` · `bare branches` · `oak forest` · `aspen` | **0** | `winter forest` | **40** |
| " | | `maple` · `forest ground` | **6** · **5** |
| " | | `leaves forest floor` · `brown leaves` · `beech forest` | **3** · **2** · **2** |
| `narrow road` · `road narrow` · `single track road` · `unpaved` · `unpaved road` · `wheel ruts` · `ruts` · `tracks dirt` · `tracks mud` · `tyre` · `tire track` · `tire tracks` · `wheel tracks` | **0** | `old road` | **21** |
| " | | `back road` · `farm road` | **8** · **8** |
| " | | `rural road` · `vehicle tracks` | **2** · **1** |
| `farm buildings` · `farmyard` · `barns` · `old barn` · `wooden barn` · `wooden shed` · `granary` · `outbuilding` · `homestead` | **0** | `shed` · `farm yard` | **16** · **17** |
| " | | `stable` · `ranch house` · `farm building` | **3** · **1** · **1** |
| `sowing` · `mowing` · `plowing` · `harvester` · `combine` · `irrigation` | **0** | `farm` | **108** |
| " | | `agriculture` · `farming` · `farmer` | **19** · **15** · **13** |
| `wax seal` · `sealing wax` · `stamp wax` · `yellowed paper` · `ledger book` · `colonial house` · `brick wall old` | **0** | `old paper` · `old book` | **9** · **9** |
| " | | `brick wall` · `stone building old` · `manuscript` · `quill` | **2** · **2** · **1** · **1** |
| `changing seasons` · `season change` · `four seasons` · `frost grass` · `frozen grass` · `shadows moving` | **0** | `frost` · `shadows` | **8** · **5** |
| `animal tracks` · `track animal` · `paw prints` · `hoof prints` · `footprints snow` · `prints mud` · `insects grass` · `bugs grass` · `bees meadow` | **0** | `hoof` · `footprints` · `grasshopper` | **2** · **2** · **3** |
| `archive boxes` · `file cabinet` · `storage boxes` · `shelf files` · `drawers` · `office cabinet` · `records room` · `stacks paper` | **0** | `library books` · `boxes` | **36** · **24** |
| `landscape wide` · `wide landscape` | **0** | `scenic landscape` · `panorama landscape` | **28** · **9** |
| `trail camera` · `camera pole` · `camera mounted` · `hidden camera` · `wildlife camera` · `camera box` · `observation camera` · `camera strap` · `device tree` · `recording device` | **0** | *nothing.* See G3 — this is a real gap |
| `cutting branch` · `pruning` · `saw branch` · `knife wood` · `strap tree` · `hatchet` · `trimming tree` · `tree cutting` · `cutting wood` | **0** | *nothing on register.* See G4 |

Reproduce any single row:

```bash
py -3.11 scripts/search_archive.py --shot "wind in bare branches" --kind video
py -3.11 scripts/search_archive.py --shot "tree branches swaying in the wind" --kind video
py -3.11 scripts/search_archive.py --shot "closed farm gate chain padlock" --kind video --weak-ok --limit 25
```

### 3.1 A hit count is not a supply count. Measured.

The single biggest honest finding in this plan. Take the counts above at face value and you will
stage rubbish:

| query | ≥1080p unused | its top three titles |
|---|---:|---|
| `lock chain` | **31** | *digital blue blockchain* · *money, crypto, cryptocurrency, bitcoin, ethereum, blockchain* · *bitcoin, cryptocurrency, blockchain, digital currency* |
| `man walking` | **130** | *young people walking to manifest equality concept* · *man walking in the dark* · *a woman walking in front of the building* |
| `old sign` | **13** | *a woman holding a signage* · *a **sold** signboard and a person holding keys* · *a woman holding a sold sign* |
| `roof` | **35** | *dramatic sunset over cityscape rooftops* · *an eco friendly building with transparent triangular roofing* |
| `gate` | **25** | *a beautiful flower bouquet at the gate* · *love locks on **golden gate bridge*** · *golden gate bridge through barbed wire* |
| `purple paint` | **4** | *purple and yellow paint* · *purple liquid paint* |

So the 760-clip union was screened at title level. Measured:

```
union of new, unused, on-disk, >=1920x1080 clips (313 queries, --per-query 4)   760
  minus off-register by title (city/crypto/office/3d/beach/food/sport/...)     -179
  = survives the off-register screen                                            581
      of which the title names a human (review-required, NOT supply)             82
      of which the title says snow / winter / ice (wrong season)                  43
      of which the title says aerial / drone / flyover (forbidden_subjects)       64
  = CORE screened supply                                                        395
```

**And 395 is still not a usable count.** Sampling the core list: *"golden gate bridge fireworks
exposition"*, *"a close up video of cable wires connected on a motherboard"*, *"watchtower, prison,
barbedwire, war, ww2"*. A filename is not evidence of content — PD_CANON 20c, and AR-10159563
which passed a filename check, a pool QC and every machine gate and still shipped a real
identifiable woman. **395 is the number of clips a human has to look at, not the number that will
survive.**

---

## 4. The queries, verbatim, with measured hit counts

313 queries, 18 registers. `title-AND` = rows whose title contains every term. `on disk` = of
those, the file exists. `unused` = of those, the id is in no episode's `factory*` folder.
`>=1920x1080 & unused` = the operative supply figure, joined against
`_ledger/video_resolution.json`. Produced in one ledger pass by the replication script named in §1.1;
any single row reproduces with:

```bash
py -3.11 scripts/search_archive.py <the query words> --kind video --limit 50
```

(that CLI ANDs against title + id + matched_keywords + theme + filename, so its count is a little
**wider** than the staging tool's title-only match; the tables below are the staging tool's.)

### R1_gate_chain_padlock   union 35
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `lock chain` | 43 | 35 | 31 | **31** |
| `gate` | 68 | 51 | 26 | **25** |
| `chain fence` | 13 | 13 | 9 | **8** |
| `old lock` | 22 | 10 | 7 | **7** |
| `iron chain` | 9 | 7 | 6 | **6** |
| `chain metal` | 11 | 7 | 6 | **5** |
| `old gate` | 10 | 8 | 3 | **3** |
| `gate green` | 4 | 4 | 3 | **3** |
| `chain link` | 6 | 6 | 2 | **2** |
| `gate open` | 6 | 5 | 2 | **2** |
| `gate fence` | 6 | 6 | 2 | **2** |
| `chained` | 2 | 2 | 2 | **2** |
| `lock gate` | 8 | 7 | 2 | **2** |
| `fencing` | 3 | 3 | 2 | **2** |
| `gate field` | 1 | 1 | 1 | **1** |
| `entrance gate` | 8 | 4 | 1 | **1** |
| `chain rusty` | 3 | 3 | 1 | **1** |
| `metal barrier` | 3 | 3 | 1 | **1** |
| `corral` | 2 | 1 | 1 | **1** |
| `rail fence` | 1 | 1 | 1 | **1** |
| `fenced` | 1 | 1 | 1 | **1** |

### R2_fence_wire_post   union 33
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `fence` | 119 | 114 | 76 | **67** |
| `wire` | 83 | 79 | 54 | **50** |
| `fence snow` | 10 | 10 | 10 | **10** |
| `old fence` | 9 | 9 | 8 | **8** |
| `stone wall` | 15 | 12 | 8 | **8** |
| `garden fence` | 10 | 10 | 8 | **8** |
| `fence wood` | 7 | 7 | 5 | **5** |
| `fence grass` | 5 | 5 | 4 | **4** |
| `fence pasture` | 5 | 5 | 4 | **4** |
| `fence field` | 6 | 6 | 3 | **3** |
| `fence countryside` | 3 | 3 | 3 | **3** |
| `barbed wire` | 15 | 15 | 3 | **2** |
| `wooden fence` | 3 | 3 | 2 | **2** |
| `fence sky` | 3 | 3 | 2 | **2** |
| `barb wire` | 15 | 15 | 3 | **2** |
| `wire fence` | 13 | 13 | 4 | **1** |
| `fence line` | 1 | 1 | 1 | **1** |
| `wire post` | 3 | 3 | 1 | **1** |
| `wire mesh` | 2 | 2 | 1 | **1** |
| `enclosure` | 2 | 2 | 1 | **1** |

### R3_posted_sign_boundary   union 35
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `old sign` | 32 | 18 | 13 | **13** |
| `sign tree` | 22 | 14 | 12 | **12** |
| `signage` | 17 | 17 | 9 | **7** |
| `sign board` | 26 | 13 | 10 | **6** |
| `warning` | 23 | 7 | 6 | **6** |
| `purple paint` | 4 | 4 | 4 | **4** |
| `notice` | 12 | 5 | 4 | **4** |
| `board wooden` | 5 | 3 | 3 | **3** |
| `warning sign` | 9 | 3 | 2 | **2** |
| `sign post` | 3 | 2 | 2 | **2** |
| `sign metal` | 12 | 3 | 2 | **2** |
| `danger sign` | 4 | 2 | 2 | **2** |
| `sign fence` | 3 | 3 | 1 | **1** |
| `keep out` | 6 | 2 | 2 | **1** |
| `paint mark` | 1 | 1 | 1 | **1** |

### R4_open_field_pasture_crops   union 85
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `field` | 330 | 247 | 133 | **114** |
| `oats` | 104 | 57 | 53 | **47** |
| `meadow` | 96 | 57 | 44 | **39** |
| `countryside` | 93 | 73 | 38 | **33** |
| `wild grass` | 37 | 29 | 28 | **27** |
| `pasture` | 35 | 25 | 21 | **20** |
| `farmland` | 29 | 18 | 15 | **15** |
| `field wind` | 24 | 22 | 14 | **14** |
| `field sunset` | 34 | 27 | 13 | **10** |
| `green field` | 34 | 24 | 11 | **10** |
| `rural landscape` | 60 | 58 | 12 | **9** |
| `field clouds` | 14 | 11 | 8 | **8** |
| `tree field` | 42 | 23 | 10 | **8** |
| `grass field` | 37 | 21 | 8 | **7** |
| `open field` | 12 | 11 | 6 | **6** |
| `grass wind` | 20 | 15 | 5 | **5** |
| `straw` | 16 | 8 | 7 | **5** |
| `wheat` | 40 | 25 | 8 | **5** |
| `wheat field` | 20 | 19 | 5 | **4** |
| `lone tree` | 28 | 26 | 5 | **4** |
| `hay` | 7 | 6 | 5 | **4** |
| `harvest field` | 13 | 8 | 3 | **3** |
| `rolling hills` | 6 | 6 | 3 | **3** |
| `grassland` | 7 | 6 | 2 | **2** |
| `field sunrise` | 16 | 3 | 1 | **1** |
| `field fog` | 19 | 3 | 1 | **1** |
| `dry grass` | 3 | 3 | 1 | **1** |
| `field horizon` | 1 | 1 | 1 | **1** |
| `reeds` | 2 | 2 | 2 | **1** |
| `haystack` | 1 | 1 | 1 | **1** |
| `rye` | 7 | 3 | 2 | **1** |
| `weeds` | 7 | 4 | 1 | **1** |
| `barley` | 7 | 3 | 1 | **1** |

### R5_woodland_trunk_bark   union 96
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `forest` | 968 | 703 | 539 | **478** |
| `trees forest` | 276 | 192 | 139 | **124** |
| `woods` | 89 | 78 | 52 | **44** |
| `winter forest` | 100 | 56 | 41 | **40** |
| `autumn forest` | 96 | 57 | 46 | **38** |
| `forest light` | 86 | 61 | 40 | **31** |
| `leaves tree` | 94 | 48 | 28 | **27** |
| `forest fog` | 104 | 46 | 23 | **20** |
| `trunk` | 23 | 20 | 15 | **15** |
| `forest morning` | 109 | 29 | 18 | **14** |
| `branches` | 33 | 22 | 15 | **13** |
| `forest mist` | 73 | 40 | 13 | **13** |
| `forest floor` | 19 | 18 | 12 | **12** |
| `moss` | 33 | 19 | 14 | **10** |
| `tree wind` | 48 | 25 | 10 | **10** |
| `tree branches` | 20 | 14 | 9 | **7** |
| `pine forest` | 15 | 11 | 8 | **6** |
| `maple` | 8 | 7 | 6 | **6** |
| `tree trunk` | 11 | 9 | 5 | **5** |
| `bark` | 13 | 9 | 7 | **5** |
| `forest ground` | 12 | 8 | 5 | **5** |
| `woodland` | 11 | 8 | 7 | **4** |
| `tree bark` | 8 | 6 | 4 | **4** |
| `roots` | 6 | 6 | 4 | **4** |
| `tree top` | 9 | 7 | 4 | **4** |
| `canopy` | 9 | 7 | 3 | **3** |
| `sunlight forest` | 26 | 19 | 6 | **3** |
| `beech` | 4 | 3 | 3 | **3** |
| `leaves forest floor` | 5 | 5 | 3 | **3** |
| `tree stump` | 4 | 3 | 2 | **2** |
| `misty forest` | 27 | 26 | 2 | **2** |
| `brown leaves` | 3 | 2 | 2 | **2** |
| `beech forest` | 2 | 2 | 2 | **2** |
| `bare trees` | 2 | 2 | 1 | **1** |
| `branches wind` | 2 | 1 | 1 | **1** |
| `sun through trees` | 14 | 14 | 1 | **1** |
| `oak` | 4 | 3 | 1 | **1** |
| `foggy forest` | 8 | 7 | 1 | **1** |

### R6_track_lane_path   union 63
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `lane` | 208 | 115 | 110 | **92** |
| `path` | 152 | 114 | 75 | **71** |
| `forest road` | 119 | 102 | 85 | **69** |
| `road trees` | 89 | 82 | 71 | **62** |
| `trail` | 84 | 68 | 54 | **47** |
| `forest path` | 61 | 52 | 35 | **34** |
| `road autumn` | 43 | 42 | 34 | **22** |
| `old road` | 37 | 25 | 21 | **21** |
| `walking path` | 27 | 26 | 16 | **16** |
| `country road` | 52 | 47 | 18 | **15** |
| `empty road` | 24 | 21 | 16 | **15** |
| `dirt road` | 21 | 19 | 8 | **8** |
| `road fog` | 31 | 18 | 9 | **8** |
| `road morning` | 25 | 11 | 10 | **8** |
| `road countryside` | 33 | 31 | 11 | **8** |
| `back road` | 14 | 9 | 8 | **8** |
| `farm road` | 17 | 15 | 8 | **8** |
| `path woods` | 11 | 10 | 6 | **6** |
| `road field` | 25 | 22 | 6 | **4** |
| `footpath` | 8 | 7 | 4 | **3** |
| `gravel` | 7 | 3 | 2 | **2** |
| `rural road` | 22 | 21 | 2 | **2** |
| `track field` | 1 | 1 | 1 | **1** |
| `vehicle tracks` | 1 | 1 | 1 | **1** |

### R7_rain_wet_ground   union 46
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `rain` | 1022 | 649 | 417 | **358** |
| `raining` | 103 | 61 | 50 | **40** |
| `rain forest` | 47 | 25 | 17 | **15** |
| `water drops` | 51 | 29 | 14 | **14** |
| `rain ground` | 37 | 25 | 13 | **11** |
| `storm rain` | 42 | 16 | 10 | **7** |
| `rain trees` | 30 | 12 | 6 | **6** |
| `droplets` | 45 | 25 | 9 | **6** |
| `puddle` | 15 | 14 | 4 | **4** |
| `mud` | 7 | 6 | 3 | **3** |
| `heavy rain` | 20 | 15 | 6 | **2** |
| `rain leaves` | 10 | 5 | 2 | **2** |
| `muddy` | 3 | 3 | 2 | **2** |
| `footprints` | 2 | 2 | 2 | **2** |
| `wet road` | 4 | 3 | 2 | **1** |
| `prints sand` | 1 | 1 | 1 | **1** |

### R8_sky_fog_cloud_light   union 74
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `clouds` | 835 | 642 | 566 | **542** |
| `sunrise` | 423 | 243 | 212 | **182** |
| `fog` | 486 | 262 | 163 | **149** |
| `dusk` | 123 | 101 | 84 | **79** |
| `mist` | 247 | 134 | 71 | **60** |
| `dawn` | 93 | 65 | 57 | **55** |
| `cloud timelapse` | 61 | 61 | 49 | **46** |
| `sky timelapse` | 48 | 48 | 43 | **40** |
| `low cloud` | 44 | 37 | 35 | **32** |
| `cloudy sky` | 43 | 42 | 32 | **27** |
| `misty` | 84 | 64 | 28 | **24** |
| `morning fog` | 200 | 40 | 25 | **20** |
| `moving clouds` | 42 | 33 | 18 | **17** |
| `wind clouds` | 57 | 20 | 17 | **16** |
| `dark clouds` | 20 | 17 | 11 | **11** |
| `overcast` | 24 | 21 | 10 | **9** |
| `golden hour` | 24 | 11 | 8 | **8** |
| `frost` | 49 | 16 | 9 | **8** |
| `haze` | 38 | 9 | 7 | **6** |
| `storm clouds` | 32 | 22 | 5 | **5** |
| `shadows` | 13 | 8 | 5 | **5** |
| `sun shadow` | 8 | 2 | 2 | **2** |
| `fog field` | 19 | 3 | 1 | **1** |
| `fog hills` | 12 | 5 | 1 | **1** |
| `shadow trees` | 3 | 1 | 1 | **1** |

### R9_figure_on_land_review   union 40
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `man walking` | 244 | 233 | 161 | **130** |
| `walking forest` | 60 | 58 | 47 | **42** |
| `person walking` | 57 | 54 | 35 | **33** |
| `walking road` | 36 | 33 | 23 | **18** |
| `legs walking` | 10 | 10 | 10 | **10** |
| `back of a man` | 15 | 15 | 7 | **6** |
| `walking away` | 6 | 6 | 6 | **6** |
| `walking field` | 20 | 19 | 8 | **5** |
| `person standing` | 8 | 8 | 4 | **4** |
| `boots` | 10 | 4 | 3 | **3** |
| `walking grass` | 5 | 5 | 2 | **2** |
| `shadow person` | 6 | 6 | 2 | **2** |

### R10_farm_work_occupation   union 36
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `farm` | 192 | 142 | 119 | **108** |
| `ranch` | 114 | 76 | 65 | **57** |
| `agriculture` | 59 | 36 | 21 | **19** |
| `farm yard` | 17 | 17 | 17 | **17** |
| `shed` | 30 | 23 | 16 | **16** |
| `farming` | 20 | 18 | 16 | **15** |
| `farmer` | 25 | 21 | 14 | **13** |
| `grain` | 37 | 20 | 16 | **9** |
| `tractor` | 28 | 14 | 11 | **7** |
| `livestock` | 49 | 32 | 32 | **6** |
| `cattle` | 6 | 6 | 6 | **5** |
| `barn` | 10 | 4 | 4 | **3** |
| `sheep field` | 3 | 3 | 3 | **3** |
| `stable` | 4 | 3 | 3 | **3** |
| `horse field` | 6 | 3 | 2 | **2** |
| `hay bale` | 3 | 2 | 1 | **1** |
| `bales` | 3 | 2 | 1 | **1** |
| `silo` | 2 | 2 | 1 | **1** |
| `cows field` | 1 | 1 | 1 | **1** |
| `farm building` | 1 | 1 | 1 | **1** |

### R11_water_creek_pond   union 43
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `stream` | 97 | 71 | 65 | **61** |
| `pond` | 86 | 64 | 55 | **50** |
| `water forest` | 89 | 59 | 52 | **47** |
| `river forest` | 62 | 50 | 39 | **37** |
| `reflection water` | 56 | 42 | 33 | **29** |
| `river bank` | 32 | 28 | 26 | **26** |
| `creek` | 46 | 30 | 27 | **25** |
| `stream rocks` | 15 | 13 | 13 | **13** |
| `fishing` | 34 | 17 | 17 | **13** |
| `water grass` | 24 | 14 | 12 | **12** |
| `lake morning` | 51 | 12 | 12 | **12** |
| `marsh` | 13 | 7 | 7 | **4** |
| `small river` | 8 | 2 | 2 | **1** |
| `still water` | 1 | 1 | 1 | **1** |
| `fishing rod` | 1 | 1 | 1 | **1** |

### R12_camping_sanctuary   union 27
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `smoke fire` | 61 | 50 | 47 | **43** |
| `fire wood` | 75 | 46 | 38 | **36** |
| `cabin` | 61 | 31 | 30 | **29** |
| `lantern` | 40 | 35 | 31 | **27** |
| `camp fire` | 36 | 22 | 18 | **15** |
| `tent` | 28 | 19 | 15 | **13** |
| `campfire` | 26 | 18 | 14 | **12** |
| `camping` | 13 | 7 | 7 | **7** |
| `cabin woods` | 2 | 2 | 1 | **1** |
| `log cabin` | 2 | 1 | 1 | **1** |

### R13_building_far_off_curtilage   union 35
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `roof` | 61 | 50 | 38 | **35** |
| `abandoned house` | 68 | 62 | 32 | **25** |
| `porch` | 30 | 17 | 13 | **13** |
| `chimney` | 27 | 17 | 11 | **11** |
| `old house` | 61 | 32 | 6 | **6** |
| `cottage` | 15 | 6 | 5 | **5** |
| `house trees` | 33 | 16 | 8 | **4** |
| `lit window` | 8 | 6 | 4 | **4** |
| `stone building old` | 4 | 3 | 2 | **2** |
| `house woods` | 4 | 4 | 1 | **1** |
| `rural house` | 11 | 4 | 1 | **1** |
| `driveway` | 2 | 2 | 1 | **1** |
| `swimming pool` | 9 | 8 | 1 | **1** |
| `ranch house` | 2 | 2 | 2 | **1** |
| `farmhouse` | 1 | 1 | 1 | **0** |
| `farm house` | 2 | 1 | 1 | **0** |

### R15_colonial_general_warrants   union 27
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `historic building` | 26 | 21 | 15 | **13** |
| `old town` | 23 | 16 | 11 | **11** |
| `old paper` | 32 | 21 | 10 | **9** |
| `old book` | 18 | 17 | 10 | **9** |
| `book pages` | 23 | 9 | 2 | **2** |
| `old map` | 3 | 3 | 2 | **2** |
| `brick wall` | 6 | 4 | 2 | **2** |
| `candlelight` | 7 | 3 | 2 | **2** |
| `quill` | 2 | 1 | 1 | **1** |
| `old letter` | 8 | 5 | 1 | **1** |
| `manuscript` | 1 | 1 | 1 | **1** |
| `vintage paper` | 4 | 3 | 1 | **1** |
| `old document` | 10 | 10 | 1 | **0** |

### R16_time_seasons   union 19
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `time lapse` | 465 | 444 | 358 | **286** |
| `timelapse` | 181 | 177 | 138 | **122** |
| `autumn leaves` | 98 | 45 | 31 | **28** |
| `snow field` | 7 | 7 | 7 | **7** |
| `sun moving` | 7 | 6 | 6 | **6** |
| `leaves falling` | 37 | 9 | 4 | **3** |
| `spring field` | 8 | 2 | 2 | **2** |
| `ice grass` | 1 | 1 | 1 | **1** |

### R17_wildlife_conservation   union 21
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `deer` | 162 | 154 | 148 | **127** |
| `animal forest` | 129 | 115 | 113 | **103** |
| `deer forest` | 84 | 78 | 72 | **65** |
| `bird tree` | 50 | 30 | 28 | **26** |
| `birds flying` | 17 | 15 | 14 | **13** |
| `elk` | 6 | 5 | 5 | **5** |
| `grasshopper` | 8 | 3 | 3 | **3** |
| `hoof` | 4 | 2 | 2 | **2** |
| `deer field` | 1 | 1 | 1 | **1** |

### R18_statute_code_law   union 13
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `library books` | 53 | 50 | 37 | **36** |
| `document` | 108 | 105 | 15 | **10** |
| `books shelf` | 8 | 7 | 5 | **4** |
| `filing` | 4 | 4 | 4 | **3** |
| `old library` | 3 | 3 | 3 | **2** |

### R19_state_line_geography   union 32
| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `scenic landscape` | 45 | 32 | 28 | **28** |
| `valley` | 39 | 36 | 27 | **21** |
| `aerial field` | 31 | 30 | 21 | **17** |
| `hills` | 46 | 31 | 19 | **16** |
| `aerial farmland` | 11 | 10 | 9 | **9** |
| `panorama landscape` | 12 | 10 | 10 | **9** |
| `road sign` | 17 | 11 | 7 | **6** |
| `border` | 24 | 9 | 5 | **5** |
| `state line` | 3 | 3 | 3 | **3** |
| `county` | 7 | 6 | 5 | **3** |
| `vast landscape` | 2 | 2 | 2 | **2** |
| `hillside` | 3 | 2 | 1 | **1** |
| `tennessee` | 5 | 3 | 1 | **1** |


---

## 5. The arithmetic — and the finding that has to be resolved before staging

### 5.1 Where the film stands today, measured

```bash
py -3.11 -c "import json;d=json.load(open('episodes/PD-2026-066-openfields/05_visuals/factory_clip_qc.v001.json',encoding='utf-8'));import collections;print(collections.Counter(x['verdict'] for x in d['clips']))"
ls remotion/public/openfields/motion | wc -l        # 0  (directory does not exist)
ls remotion/public/openfields/img    | wc -l        # 0
ls episodes/PD-2026-066-openfields/04_scenes/generated_images | wc -l   # 0
```

```
staged clips              338
accepted (verdict accept) 203
rejected                  135
motion (i2v) clips          0
generated stills            0     <- the 185 mandatory plates L070-L254 do not exist yet
distinct video sources    203 = 203 accepted + 0 motion
```

**The hard pre-flight floor is already met.** `check_episode_inputs.py` L279-283:
`no_reuse = max(declared, int(secs/4.5*0.65))` = `max(350, int(1598.038/4.5*0.65))` = `max(350,230)` = **350**;
`need = max(40, 350 // 2)` = **175**. 203 ≥ 175, so the pre-flight does not block. What blocks is
`check_spec_satisfied.py` L131-138, which needs **350 distinct footage+motion sources in the film**.

### 5.2 The finding: 350 is unreachable at the pre-revision `target_cut_sec` of 3.5 (RESOLVED -- Path A taken, spec now 3.1)

`build_case_film_generic.solve_totals` (L186-205), with `MIN_VIDEO_SHARE = 0.68`,
`MAX_VIDEO_REUSE = 2`, `MAX_STILL_REUSE = 1`, and `total_sec` = the end of the last narration
window = **1598.038 s**:

```
want        = round(1598.038 / 3.5)            = 457 cuts
video_want  = ceil(457 * 0.68)                 = 311 video cuts
still_max   = floor(311 * 0.32 / 0.68)         = 146 still cuts
```

A film with 311 video cuts can carry **at most 311 distinct video sources**. The contract asks for
350. `check_spec_satisfied` fails **no matter how large the pool is**. This is not a shelf problem
and no amount of staging fixes it.

The cause is in the spec's own derivation: it computed 350 from a **1800 s design target**
(`1800/3.5 = 514 cuts; ceil(514 × 0.68) = 350`). The delivered narration master is **1598.038 s**,
not 1800 — 26:38, not 30:00. The 350 was derived from a film that was never made.

The same mismatch bites the stills. `mandatory_stills` is now **185 ids** (L070–L254) and
`MAX_STILL_REUSE = 1`, so 185 plates need 185 still cuts; only 146 exist. `check_spec_satisfied`
matches on the **stem**, so a plate delivered as `L241.mp4` after i2v satisfies `L241.png` *and*
counts as a distinct video source. That is the release valve — and it is what sets the plate count.

### 5.3 The two legal resolutions. Both are owner decisions, per the spec's own rule.

The spec says raising `target_cut_sec` is an owner decision and never a silent edit. Lowering it is
the same kind of decision.

**Path A — keep `distinct_video_assets: 308`, lower `target_cut_sec` to 3.1.**

```
want       = round(1598.038 / 3.1)      = 515 cuts
video cuts = ceil(515 * 0.68)           = 351      >= 350   PASS
still cuts = min(pool, 515-351, 165)    = 164
slot length at the builder's minimum video share = 3.1 * 1.0340 = 3.21 s
```

3.21 s is **further** below the 4.80 s i2v clip length than 3.5's 3.62 s, so this is strictly safer
against the EP65 marmet looping failure the spec's `target_cut_sec` section exists to prevent, not
riskier. It also reproduces exactly the 514/350/164 structure the spec designed.

Plate pigeonhole: `185 mandatory stills − 164 still cuts` = **21 plates must reach the film as
motion**, not as stills.

```
i2v motion plates required   = 21          (the pigeonhole minimum)
accepted archive required    = 351 - 21    = 330      if plates are minimised
                             = 351 - 148   = 203      if archive is left where it is
                                             ^ i.e. 148 i2v plates, the other end of the line
```

**Path B (NOT TAKEN) — keep `target_cut_sec` at 3.5, re-derive `distinct_video_assets` from the measured master.**

```
distinct_video_assets = ceil(round(1598.038/3.5) * 0.68) = 311
pre-flight floor      = 311 // 2                          = 155
still cuts            = 146  ->  185 - 146 = 39 plates must be motion
accepted archive required = 311 - 39 = 272   (plates minimised)
                          = 311 - 108 = 203  (archive left where it is)
```

The spec's own TODO 7 says to re-derive the band from the measured master once the VO exists. The
VO exists. Path B is the more honest one; Path A is the one that keeps the declared number.

### 5.4 The subtraction, against measured supply

Take Path A (351 sources). The shelf has to close `351 − 203 = 148`, minus whatever the 21
mandatory motion plates contribute.

```
new clips this plan reaches (unused, on disk, licence-clean, >=1920x1080, --per-query 4)   760
  measured acceptance of the previous openfields visual-QC pass, same shelf, same tool
      203 accept / 338 staged                                                            60.1 %
      excluding its 49 resolution rejections (this batch is pre-filtered to >=1920x1080)
      203 accept / 289                                                                   70.2 %

  760 x 0.601 = 457 new accepted   ->  203 + 457 = 660 sources   i2v needed = 21 (pigeonhole only)
  760 x 0.400 = 304 new accepted   ->  203 + 304 = 507 sources   i2v needed = 21
  760 x 0.250 = 190 new accepted   ->  203 + 190 = 393 sources   i2v needed = 21
  760 x 0.195 = 148 new accepted   ->  203 + 148 = 351 sources   i2v needed = 21   <- break-even
```

**Break-even is a 19.5% visual-QC acceptance rate on the new batch.** The measured rate for this
episode, on this shelf, with this tool, was 60.1% — and that pass had no resolution pre-filter,
which was its single largest rejection reason. The new batch is broader and noisier than v001's
hand-curated 275 (§3.1), so it will accept lower than 60.1%; it would have to accept **three times
worse** to miss.

```
================  THE SUBTRACTION  ================
Path A     351 distinct video sources required
         - 203 accepted archive clips in hand
         = 148 to find
         - 148 expected from staging 760 new clips at any acceptance rate >= 19.5%
         =   0 shortfall from the shelf

i2v motion plates to generate = 21   (forced by 185 mandatory stills vs 164 still cuts,
                                      NOT by any shelf shortage)
still plates to generate      = 164  (185 - 21)
total plates in Batch B/C     = 185  (L070-L254; none exist yet)
===================================================

Path B     311 required - 203 in hand = 108 to find; break-even acceptance 14.2%
           i2v motion plates = 39; still plates = 146
```

**Recommendation: stage at `--per-query 4` (760 clips), not 3 (609) and not 6 (984).** 6 buys depth
inside queries that are already noise-dominated; 4 buys breadth across registers and keeps the
visual-QC read to a size a human will actually finish. Even at a 25% acceptance rate, 4 clears the
target with 42 sources of margin.

### 5.5 Which 21 plates get i2v'd

Not an arbitrary 21. They are the registers the shelf cannot serve at all — G1 through G6 in §6 —
and the film's own held beats, where a motionless plate would read as the freeze that
`check_motion_clip_stillness.py` exists to catch:

- the padlock motif states 1, 2, 3, 4, 5, 7 (six plates — the closed chain, the boot prints beyond
  it, the wet chain in rain, the second Pennsylvania padlock, the exhibit-flat frontal, the final
  morning chain)
- the blank weathered placard and the purple paint blaze (two)
- the trail camera: the cut branch, the housing on the trunk, the lens (three — the film's title
  image, seen at 0:15 and again in ACT_5)
- the empty gate post with a loop of wire, ACT_5 recognition and HOOK last image (one, used twice
  as the identical framing)
- the remaining nine from the people plates L235–L254, which are the ones most likely to carry
  motion (a figure crossing a field, a hand on a wire) and where archive is review-required anyway

Run `py -3.11 scripts/check_motion_clip_stillness.py --slug openfields` over the motion pool before
the build and quarantine anything whose longest still stretch exceeds 3.0 s. The spec is explicit
that `target_cut_sec` alone did not save marmet.

---

## 6. The gaps — after honest retries

Seven. Each was asked in at least three phrasings; the phrasings are in §3.

| id | register | measured | the answer |
|---|---|---|---|
| **G1** | closed farm gate with a chain and padlock | 21 phrasings round 1, 30 in retry. Best real hits: `gate` 25 (Golden Gate Bridge, flower bouquet), `lock chain` 31 (blockchain), `chain fence` 8. On-register: roughly 6 items, unchanged from v001's eyeballed finding | **i2v plate.** Motif states 1–7 are already ordered as plates. Archive carries the fence either side (R2, 33 clips). **Plus an owner call**: v001 §5.1 found the three best padlock clips on the whole shelf locked to `robosigning` (`pexels 3999371` / `3999356` / `4976926`), two of them in `factory_rejected` — rejected *for a mortgage-fraud film*, where a rusty farm gate is obviously wrong. Releasing those three roughly doubles this film's weakest register. Still an owner decision, still not taken. |
| **G2** | posted boundary placard, purple paint blaze | `purple paint` 4 — all paint splashes. `blaze tree`, `spray paint tree`, `marking tree`, `paint on wood`, `violet paint` all 0. `no trespassing` 1, `private property` 0 | **i2v plate.** And the spec's PROSE RULE forbids lettering on a generated plate, so it is ordered as a weathered blank placard, a colour, a shape, and a purple blaze — never as the words. |
| **G3** | a trail camera strapped to a trunk | 25 phrasings across two rounds. `trail camera` 0, `wildlife camera` 0, `camera mounted` 0, `hidden camera` 0, `camera strap` 0, `device tree` 0. What exists: `cctv` 1, `camera outdoor` 4, `webcam` 2, `sensor` 3 — and every one of those is the surveillance-thriller styling the spec forbids by name | **i2v plate.** Three of them: the branch, the housing, the lens. The spec is right that this is the film's title image and it has to be made. |
| **G4** | the cut branch | `cutting branch` 0, `pruning` 0, `saw branch` 0, `trimming tree` 0, `tree cutting` 0, `cutting wood` 0, `knife wood` 0, `hatchet` 0. `chainsaw` 2 and `wood chopping` 3 exist and read as forestry labour, not a warden removing one branch | **i2v plate**, or **drop the cut** — the beat survives on the tree alone (`tree trunk` 5, `trunk` 15, `tree bark` 4) with TN-16 carried by the narration. Do not use the chainsaw clips; they change what the sentence says. |
| **G5** | boot prints in mud beyond a closed gate (motif state 2) | `boot prints in mud` 0 (v001), `footprints` 2, `prints mud` 0, `paw prints` 0, `footprints snow` 0, `muddy` 2, `mud` 3 | **i2v plate.** The beat is a two-object composition (closed lock in front, prints behind) that stock does not shoot. |
| **G6** | a farmhouse seen from far off — the curtilage | `farmhouse` 1 and it is sub-HD; `farm house` 1 sub-HD; `rural house` 1 (Indonesia); `house field` 0; `abandoned house` 25 but they are Madeira and horror-set | **Different framing.** Use `lit window` (4) and `porch` (13) at distance for *"a narrow ring around a house"*, and let R13's 12 cuts come from those plus one plate. A plate is cheaper than a wrong farmhouse. |
| **G7** | Appalachian / Middle Tennessee specificity | `appalachian` 2 rows, 0 unused; `tennessee` 1; `pennsylvania` 0 at ≥1080p; `middle tennessee farmland` 0 (v001) | **Different framing, and deliberately so.** The spec's PROSE RULE bars identifiable real property anyway. The register is hardwood ridge, fog and elevation, which is abundant (R5 51 cuts, R19 12). No plate. **No clip may carry a legible place name.** |

### 6.1 People — supply, or review-required?

`face` / `portrait` / `headshot` are no longer forbidden subjects, so a generated face is fine and
the 20 PEOPLE plates L235–L254 are face-forward by design. **Archive is a different question.**
82 of the 760 union clips name a human in the title; after the off-register screen, R9's core is
**6 clips** — legs, back-of-camera, a figure at distance. Everything else in R9 is urban
(`man walking` → *young people walking to manifest equality*, *a woman walking in front of the
building*).

R9's 12 cuts are therefore marked **review-required, not counted as supply**, and every one of them
must be frame-sampled at 10/35/60/88% and read on a labelled sheet before it enters a cut. That is
what v001 did for 23 clips and 92 frames, and it is the only procedure that has ever caught this:
AR-10159563 passed a filename check, a pool QC and every machine gate and shipped a real
identifiable woman whose age could not be settled from the footage. It is now the only
`cat2_real_identifiable_minor` row in `config/footage_blocklist.v001.json`.

`footage_review_required: true` is declared in the contract. It is not satisfied by a stamp.

### 6.2 What might be hiding in the unreachable lane — stated, not counted

```bash
py -3.11 -c "import json,os,collections;c=collections.Counter();n=0
for line in open(r'H:\pd-media\assets\archive\_ledger\factory.jsonl',encoding='utf-8',errors='replace'):
    r=json.loads(line)
    if r.get('source')=='pixabay' and os.path.splitext(str(r.get('file_path','')))[1].lower() in ('.mp4','.mov','.webm','.mkv'):
        n+=1; c[str(r.get('title'))]+=1
print(n, c.most_common(3))"
```

```
6,322 pixabay video rows in factory.jsonl, and the most common title is ('id', 6322)
      -- i.e. ALL of them. 6,357 pixabay video rows shelf-wide (35 sit in other ledgers).
```

Pixabay's URL for an untitled video is `/videos/id-28860/`, so the slug-derived title is the
literal string `"id"` for every one. **Zero of my 760 union clips come from that lane**, and none
can: `stage_footage_by_title` matches on title, `stage_footage_from_allowlist`'s `AF-` regex no
longer matches the renamed factory filenames, and `search_archive --shot` has nothing to rank
(title `id`, `matched_keywords` empty, theme `subtype_unverified`).

**Which of my gaps could be in there: G1 (gate/padlock), G5 (boot prints), G6 (farmhouse at
distance).** All three are ordinary outdoor rural stock, which is exactly what an untitled Pixabay
clip usually is. v001 §7 sheeted 60 of the 703 quality-passing rows under the three land themes and
read all three sheets: 12/60 usable, projecting **~140 usable clips**. I did not re-run that probe —
it needs contact sheets, which is disk work, and three renders are running. **That ~140 is v001's
measurement, not mine, and it is not counted as supply anywhere in §5.** It is a reserve behind a
tooling gap. The fix is an `--id` flag on `stage_footage_by_title` or restoring `AF-` ids to the
allowlist matcher; both are owner-gated tool changes.

---

## 7. Staging command block — run unmodified once the machine is idle

**Preconditions.** No render running (`Get-Process | Where-Object {$_.Name -like '*chrome*'}` empty,
CPU idle). `git pull` first.

```bash
cd /c/Users/aab15/Documents/prime-documentary

# ---- 0. the machine must actually be idle; staging copies ~760 files off H:
py -3.11 scripts/check_episode_inputs.py --slug openfields || true

# ---- 1. write round 3's queries and merge them into the canonical config (idempotent)
cat > config/episode_footage_queries.openfields_round3.v001.json <<'JSON'
{
 "R1_gate_chain_padlock": [
  "gate",
  "old gate",
  "chain link",
  "gate open",
  "gate fence",
  "gate field",
  "entrance gate",
  "chained",
  "gate green",
  "chain rusty",
  "chain metal",
  "lock gate",
  "lock chain",
  "old lock",
  "iron chain",
  "chain fence",
  "metal barrier",
  "corral",
  "rail fence",
  "fencing",
  "fenced"
 ],
 "R2_fence_wire_post": [
  "fence",
  "wire fence",
  "barbed wire",
  "wooden fence",
  "fence field",
  "fence line",
  "wire",
  "old fence",
  "fence wood",
  "fence grass",
  "fence snow",
  "wire post",
  "fence countryside",
  "stone wall",
  "fence pasture",
  "fence sky",
  "barb wire",
  "wire mesh",
  "garden fence",
  "enclosure"
 ],
 "R3_posted_sign_boundary": [
  "warning sign",
  "sign post",
  "sign tree",
  "sign fence",
  "old sign",
  "keep out",
  "signage",
  "paint mark",
  "purple paint",
  "sign board",
  "sign metal",
  "danger sign",
  "warning",
  "notice",
  "board wooden"
 ],
 "R4_open_field_pasture_crops": [
  "open field",
  "field",
  "meadow",
  "pasture",
  "grass field",
  "wheat field",
  "harvest field",
  "field wind",
  "grass wind",
  "grassland",
  "field sunset",
  "field sunrise",
  "field fog",
  "green field",
  "dry grass",
  "field clouds",
  "lone tree",
  "tree field",
  "farmland",
  "countryside",
  "rural landscape",
  "field horizon",
  "reeds",
  "hay",
  "haystack",
  "straw",
  "wheat",
  "oats",
  "rye",
  "wild grass",
  "weeds",
  "barley",
  "rolling hills"
 ],
 "R5_woodland_trunk_bark": [
  "forest",
  "woodland",
  "woods",
  "tree trunk",
  "trunk",
  "bark",
  "tree bark",
  "trees forest",
  "forest floor",
  "autumn forest",
  "bare trees",
  "tree stump",
  "branches",
  "tree branches",
  "branches wind",
  "canopy",
  "sunlight forest",
  "sun through trees",
  "forest light",
  "pine forest",
  "oak",
  "beech",
  "forest morning",
  "forest mist",
  "misty forest",
  "foggy forest",
  "forest fog",
  "moss",
  "roots",
  "tree top",
  "leaves tree",
  "tree wind",
  "winter forest",
  "leaves forest floor",
  "forest ground",
  "brown leaves",
  "beech forest",
  "maple"
 ],
 "R6_track_lane_path": [
  "dirt road",
  "gravel",
  "country road",
  "road trees",
  "forest road",
  "forest path",
  "path",
  "trail",
  "footpath",
  "track field",
  "road field",
  "road fog",
  "empty road",
  "road morning",
  "road countryside",
  "lane",
  "path woods",
  "walking path",
  "road autumn",
  "rural road",
  "back road",
  "old road",
  "farm road",
  "vehicle tracks"
 ],
 "R7_rain_wet_ground": [
  "rain",
  "heavy rain",
  "rain trees",
  "rain forest",
  "raining",
  "rain leaves",
  "rain ground",
  "puddle",
  "water drops",
  "droplets",
  "storm rain",
  "mud",
  "muddy",
  "wet road",
  "footprints",
  "prints sand"
 ],
 "R8_sky_fog_cloud_light": [
  "clouds",
  "overcast",
  "cloudy sky",
  "storm clouds",
  "dark clouds",
  "fog",
  "mist",
  "misty",
  "morning fog",
  "fog field",
  "fog hills",
  "low cloud",
  "dawn",
  "dusk",
  "golden hour",
  "moving clouds",
  "cloud timelapse",
  "sky timelapse",
  "haze",
  "wind clouds",
  "sunrise",
  "frost",
  "shadows",
  "shadow trees",
  "sun shadow"
 ],
 "R9_figure_on_land_review": [
  "person walking",
  "man walking",
  "walking forest",
  "walking field",
  "walking grass",
  "boots",
  "legs walking",
  "back of a man",
  "person standing",
  "walking away",
  "walking road",
  "shadow person"
 ],
 "R10_farm_work_occupation": [
  "farmer",
  "tractor",
  "farming",
  "farm",
  "agriculture",
  "hay bale",
  "bales",
  "barn",
  "silo",
  "cattle",
  "cows field",
  "sheep field",
  "horse field",
  "grain",
  "livestock",
  "ranch",
  "shed",
  "stable",
  "farm yard",
  "farm building"
 ],
 "R11_water_creek_pond": [
  "creek",
  "stream",
  "small river",
  "river forest",
  "pond",
  "water grass",
  "stream rocks",
  "river bank",
  "water forest",
  "marsh",
  "reflection water",
  "still water",
  "fishing",
  "fishing rod",
  "lake morning"
 ],
 "R12_camping_sanctuary": [
  "campfire",
  "camp fire",
  "tent",
  "camping",
  "cabin",
  "cabin woods",
  "log cabin",
  "fire wood",
  "smoke fire",
  "lantern"
 ],
 "R13_building_far_off_curtilage": [
  "farmhouse",
  "farm house",
  "old house",
  "house trees",
  "abandoned house",
  "house woods",
  "rural house",
  "lit window",
  "porch",
  "roof",
  "chimney",
  "driveway",
  "swimming pool",
  "cottage",
  "ranch house",
  "stone building old"
 ],
 "R15_colonial_general_warrants": [
  "old paper",
  "old document",
  "quill",
  "old book",
  "book pages",
  "old letter",
  "manuscript",
  "vintage paper",
  "old town",
  "historic building",
  "old map",
  "brick wall",
  "candlelight"
 ],
 "R16_time_seasons": [
  "timelapse",
  "time lapse",
  "autumn leaves",
  "leaves falling",
  "snow field",
  "spring field",
  "sun moving",
  "ice grass"
 ],
 "R17_wildlife_conservation": [
  "deer",
  "deer forest",
  "deer field",
  "elk",
  "birds flying",
  "bird tree",
  "animal forest",
  "hoof",
  "grasshopper"
 ],
 "R18_statute_code_law": [
  "books shelf",
  "library books",
  "old library",
  "document",
  "filing"
 ],
 "R19_state_line_geography": [
  "state line",
  "border",
  "road sign",
  "county",
  "hills",
  "hillside",
  "valley",
  "tennessee",
  "aerial farmland",
  "aerial field",
  "panorama landscape",
  "scenic landscape",
  "vast landscape"
 ]
}
JSON

py -3.11 - <<'PY'
import json, pathlib
cfg = pathlib.Path("config/episode_footage_queries.v001.json")
d = json.loads(cfg.read_text(encoding="utf-8"))
new = json.loads(pathlib.Path(
    "config/episode_footage_queries.openfields_round3.v001.json").read_text(encoding="utf-8"))
flat = [q for v in new.values() for q in v]
ep = d["episodes"]["openfields"]
have = set(ep["queries"])
added = [q for q in flat if q not in have]
ep["queries"] = ep["queries"] + added
ep["note"] = ep["note"] + (
    " Round 3 (2026-08-10, FOOTAGE_PLAN.v002): 313 register-tagged queries measured against a "
    "replication of stage_footage_by_title's own selection; 760 distinct unused >=1920x1080 clips "
    "reachable at --per-query 4. 149 phrasings measured 0 and were each retried >=3 ways before "
    "being recorded as a gap.")
cfg.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"merged {len(added)} new queries; openfields now has {len(ep['queries'])}")
PY

# ---- 2. stage.  --per-query 4 is the measured choice (760 clips; 3 -> 609, 6 -> 984)
#      dry-run first and read the per-query counts before the copy
py -3.11 scripts/stage_episode_footage.py --slug openfields --per-query 4 --dry-run
py -3.11 scripts/stage_episode_footage.py --slug openfields --per-query 4

# ---- 3. look at every new tile.  THIS IS NOT OPTIONAL (footage_review_required: true)
py -3.11 scripts/build_footage_contact_sheet.py \
    --dir remotion/public/openfields/factory --media video \
    --out-dir runs/qc/openfields_factory_r3

# ---- 4. frame-sample every clip whose title names a human, at 10/35/60/88%,
#         and read the sheets.  AR-10159563 is why.
#         (record accept/reject in runs/qc/openfields_clip_verdicts.v001.json)

# ---- 5. re-stamp the QC manifest and re-check the floor
py -3.11 scripts/write_factory_clip_qc.py --slug openfields
py -3.11 scripts/check_episode_inputs.py --slug openfields
```

### 7.1 Two traps in that block, both measured

1. **`stage_episode_footage.py` retires clips by filename before it stages.** Its `UNIVERSAL_JUNK`
   regex is unanchored and matches `wildlife`, `safari`, `zoo`, `beach`, `party`, `dance`, `surf`
   as substrings. **57 of the 760 would be caught** — including
   *"deer, safari, natural, animal, wildlife, zoo, landscape, field"* and
   *"sedge warbler, bird, wildlife, reeds, nature"*, which are R17, a register this film argues
   from. They survive **this** run (the sweep runs over the pool *before* staging) and are retired
   on the **next** invocation, into `factory_offtopic` — which kills them for every episode
   forever. If R17 matters, either run `scripts/stage_footage_by_title.py --slug openfields
   --query ... --per-query 4` directly (same selection, no junk sweep) and then
   `prune_pool_by_blocklist.py` / `dedupe_pool_across_episodes.py` by hand, or move the wanted ids
   back out of `factory_offtopic` in the same session.

2. **`forbidden_subjects` is matched on the filename by `check_spec_satisfied.py`.** The staged name
   is `AR-<id>__<title-slug>.mp4`, so a supplier title containing `drone`, `police`, `gun`,
   `rifle`, `handcuffs`, `gavel`, `courtroom`, `prison`, `child` fails the build after the render.
   64 of the 760 carry `aerial|drone|flyover|top view`; at least one R2 hit is
   *"watchtower, prison, barbedwire, war, ww2"*. Reject these at contact-sheet QC, not at the gate.

### 7.2 Before anything is staged — the owner decisions

1. **§5.2/§5.3: the pre-revision `target_cut_sec` of 3.5 + `distinct_video_assets 308` cannot both stand.** RESOLVED 2026-08-11: Path A taken, `target_cut_sec` is 3.1 in the spec. Path A
   (drop to 3.1) or Path B (re-derive to 311). Not a silent edit.
2. **§6 G1: release `pexels 3999371`, `3999356`, `4976926` from `robosigning`'s `factory_rejected`?**
   Two were rejected for a mortgage-fraud film. They are the three best on-subject images on the
   shelf for this one.
3. **The HOOK is written on an aerial** (`PACKAGING §3`, *"Archive aerial farmland at low sun"*) and
   `drone` is a forbidden subject. An aerial whose title omits the word passes the machine gate.
   Owner line, not a silent pick.
4. **§6.2: the pixabay lane.** ~140 usable clips (v001's measurement) unreachable by any tool.
   Tool fix is owner-gated.

---

## 8. What is deferred, and why

- **Clip durations.** No ledger field; ffprobe over thousands of files on H: while three renders
  run. Deferred.
- **Re-running the pixabay blind probe.** Needs contact sheets. v001's 12/60 stands; not re-measured
  and not counted as supply.
- **Per-clip visual verdicts on the 760.** That is the staging step, not this plan. This plan's job
  was to make it mechanical.
- **The 185 plates L070–L254.** None exist. Codex Batch B/C. Not this plan's scope, but §5.5 fixes
  which 21 of them must be i2v'd, and nothing downstream can be built until they are ordered.

---

> **Correction, 2026-08-12.** `distinct_video_assets` was corrected in `episode_spec.v002.json` because the original figure was never derived from the allocator. Superseded numbers may remain in the body above for provenance; the spec is authoritative. See `decisions/0009-DISTINCT-VIDEO-ASSETS-CORRECTION.md`.
