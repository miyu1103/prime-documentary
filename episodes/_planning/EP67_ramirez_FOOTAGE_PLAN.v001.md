# EP67 · TRANSUNION v. RAMIREZ — FOOTAGE QUERY PLAN v001

**Date 2026-08-11 · slug `ramirez` · episode `PD-2026-067-ramirez`**
**Contract `episodes/PD-2026-067-ramirez/episode_spec.v001.json` — `distinct_video_assets` **222**,
`target_cut_sec` **3.8**, `runtime_seconds` **[1560, 1895]**, `footage_review_required` **true**,
47 `forbidden_subjects`.**
**Design `EP67_ramirez_FILM_BIBLE.v001.md` · front `EP67_ramirez_PACKAGING.v001.md` ·
facts `EP67_ramirez_FACTS_LEDGER.v001.md`.**

> **Nothing here was staged, copied, transcoded or ffprobed.** Every number below was produced by
> reading the rights ledger and the resolution index in a single pass, while other jobs held the
> disks. No clip was moved.

---

## 0. Result in one block

```
contract distinct_video_assets                          222
clip floor, runtime_lo // 45  (check_final_acceptance)   34     -> not binding
channel target                                           60     -> not binding
video cuts this film has room for (see s5)              323
queries asked, over two rounds                          586
sum of the 20 register unions (what the gate counts)  11,682
distinct clips behind those unions                     7,820
after an off-register and forbidden_subjects screen    5,537
clip ids already held by some episode's factory*       9,068     <- already subtracted everywhere
```

**The shelf is not the binding constraint on this episode.** 5,537 screened clips against 260
required is a factor of 21. The binding constraints are two, and both are about *register*, not
volume:

1. **This film happens indoors, at a counter, on a screen and in the mail.** Those are the four
   registers the shelf is thinnest in — `envelope`, `mailbox`, `file cabinet`, `desk drawer`,
   `courthouse` and `courtroom` all return **0 usable clips** after two rounds of retries (§3).
2. **Sixty-six previous episodes have already eaten the obvious clips.** 9,068 ids are held by some
   episode's `factory*` folder and are excluded from every count here by construction, which is why
   `documents` (54 title matches, 53 on disk) yields **0** and `envelope` (19 / 17) yields **0**.

---

## 1. The instrument, verified before any zero was trusted

The counts in §4 were produced by **replicating `scripts/stage_footage_by_title.py`'s own
selection** over one pass of the ledger instead of 586 passes. Not a second search implementation:
the measuring script imports that module and uses *its* `ledger_rows()`, *its* `OK_LICENSE`,
*its* `TITLE_BLOCK` and `RIP_SIGNATURE` regexes and *its* `slugify()`, so every row it counts is a
clip the staging tool would really take. The script is
`E:\UserTemp\aab15\claude\C--Users-aab15\d654d1fe-e458-4466-83a4-f13b171f9f50\scratchpad\final_ramirez.py`.

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
| 8 | `_ledger/video_resolution.json` says **w ≥ 1920 and h ≥ 1080** | `search_archive.load_video_resolution` — the ledgers carry no width or height, and 1,770 of the 2,280 archival videos are below 720p |

**Cross-episode reuse is therefore already subtracted from every number in this document** (owner
complaint 「素材の被り」, gate `footage_diversity`). Nothing here is a clip another episode is holding.

Any single row reproduces with the canonical instrument, whose count is a little **wider** because
its CLI ANDs against title + id + matched keywords + theme + filename rather than title alone:

```bash
py -3.11 scripts/search_archive.py car showroom --kind video --limit 50
py -3.11 scripts/search_archive.py --shot "hand on a keyboard, monitor light" --kind video --limit 25
```

**One honest caveat about the instrument.** The `9,068 ids already staged` figure moved during this
measurement: the first pass at 01:0x read **8,997** and the final pass read **9,068**, because a
footage-staging job was running on another thread and consuming ids. The counts below are therefore
a **lower bound taken at 2026-08-11**, and they will only go down. Re-measure before staging if more
than a day passes.

---

## 2. The registers, and how many cuts each one owes

Twenty registers, derived from this film's own sections rather than from a generic list. Cut counts
sum to **323**, which is the video-cut budget computed in §5.

| # | register | what it is for in THIS film | cuts | script beats it serves |
|---|---|---|---:|---|
| R1 | dealership, showroom, cars | the counter where it happens. The hook and A1 live here | 26 | HOOK all six lines; A1-01…A1-04 |
| R2 | counter, paperwork, signing | the credit application, the desk, the hand that stops | 22 | HOOK cut 4; A1-02; A2-11 (the identifiers OFAC publishes) |
| R3 | screen, data, matching | the machine. The two-word comparison, Accuity, the name-only search | 28 | A2-04…A2-09; the `two_words` AE beat |
| R4 | mail, letter, envelope | the two mailings of 28 Feb and 1 March, and the letter that does not say how to dispute | 14 | A1-06…A1-10; ENDING |
| R5 | drawer, file, cabinet | **the majority's own image** — the defamatory letter stored in a desk drawer | 12 | A4-08 (HD-08); A4-11; ENDING |
| R6 | courthouse, columns, marble | the two courts. Never a re-enacted courtroom (see §6) | 24 | A3-10…A3-14; A4-01…A4-04; A5-01 |
| R7 | crowd, anonymous people | 8,185 of them. The class as a quantity of human beings | 22 | A3-05…A3-08; A4-12 (the 6,332) |
| R8 | money, damages | three figures that must stay apart | 16 | A3-12; A3-14; the `jury_award` AE beat |
| R9 | travel, the cancelled trip | he consulted a lawyer and cancelled a planned trip | 10 | A1-12; A1-13 |
| R10 | home, street, ordinary life | where 6,332 files sat while nothing happened to anyone | 16 | A4-13; A5-06; ENDING |
| R11 | government, flag, Treasury | OFAC. The list is a real instrument of the United States | 14 | A2-01…A2-03 |
| R12 | paper, print, records | credit files as objects; the FCRA of 1970 | 18 | A2-10; A3-01; A3-02 |
| R13 | corporate office, tower | the company, seen from outside. **Never a named building** | 20 | A2-12; A3-03; A5-04 |
| R14 | clock, time, seasons | 2010 → 2011 → 2016 → 2020 → 2021 | 12 | act transitions ×5; A3-09 |
| R15 | phone, calling, waiting | consulting a lawyer; the dispute that had no instructions | 8 | A1-11; A1-13 |
| R16 | lock, blocked, held | blocked assets, prohibited transactions — what the list actually does | 10 | A2-02; A2-03 |
| R17 | road, driving, leaving | the car he did not drive home; the drive away | 12 | A1-05; ENDING |
| R18 | hands, backs, figures | **the people lane.** Human presence with no identifiable face | 20 | throughout; see §6 |
| R19 | weather, dusk, quiet | the four designed silences | 14 | A3-15; A4-14; A5-12; ENDING |
| R20 | law, statute, voting | Congress passed it, Nixon signed it | 7 | A3-01; A5-08 |
|  | **total** |  | **323** | |

**Hard constraint that binds every register.** `check_spec_satisfied.py` matches
`forbidden_subjects` word-wise **against the source filename**, so a clip whose title carries
`terrorist`, `police`, `gun`, `prison`, `gavel`, `scales`, `hourglass`, `handshake`, `drone`,
`child`, `crypto`, `bitcoin`, `wedding` or `beach` is an automatic build failure. **That is not a
mistake in the contract — it is the point.** This is an episode about a man wrongly labelled a
terrorist; a stock clip whose own title says "terrorist" placed anywhere near his story is the
single most defamatory thing this film could do. 1,965 of the 7,820 union clips are removed by that
screen and by the off-register screen, and none of them is a loss.

---

## 3. The zeros, and the retries that were run before any of them was written down as a gap

**Round 1 asked 335 queries and produced 87 zeros. Round 2 re-asked every zero-producing register in
different words — 252 further queries — before a single gap was recorded.** A zero is a fact about
the words until it has been asked at least three other ways. The measured wins:

| director's phrasing | usable | supplier phrasing that worked | usable |
|---|---:|---|---:|
| `car keys` · `buying car` · `car dealer` · `car dealership` | **0** | `auto` **119** · `customer` **24** · `purchase` **11** · `key hand` **10** · `car show` **5** · `car key` **4** | 173 union |
| `paperwork` · `document signing` · `hand writing` · `pen paper` · `application form` · `clipboard` · `form filling` · `writing document` | **0** | `sign` **275** · `pen` **191** · `form` **135** · `office work` **57** · `notes` **40** · `desk` **39** | 742 union |
| `server room` · `cursor` · `database` · `search bar` · `spreadsheet` | **0** | `graph` **206** · `chart` **29** · `mouse` **7** · `data analysis` **5** · `searching` **4** | 250 union |
| `envelope` · `envelopes` · `mailbox` · `post box` · `postal` · `postman` · `post office` · `paper letter` · `writing letter` | **0** | `shipping` **33** · `post` **16** · `package` **11** · `parcel` **5** · `courier` **4** · `delivery man` **4** | 65 union |
| `files` · `folder` · `documents` · `drawer` · `desk drawer` · `file cabinet` · `office files` · `paper files` · `paper stack` · `shelf files` · `storage boxes` · `archive` | **0** | `box` **81** · `pile` **11** · `file` **9** · `shelf` **8** · `chest` **3** · `cardboard box` **2** | 115 union |
| `supreme court` · `courthouse` · `court building` · `courtroom` · `federal building` · `columns` · `stone columns` · `classical building` · `staircase stone` · `steps building` | **0** | `architecture` **433** · `trial` **49** · `old building` **28** · `dome` **26** · `court` **14** · `historic building` **10** | 562 union |
| `queue` · `waiting people` | **0** | `office people` **21** · `line people` **12** · `group people` **11** · `waiting` **6** | 54 union |
| `suitcase` · `plane window` | **0** | `holiday` **47** · `vacation` **46** · `sky plane` **9** · `trolley` **5** · `backpack` **3** | 107 union |
| `front door` · `garage` · `neighborhood` · `residential` · `suburban` | **0** | `door` **180** · `village` **25** · `town street` **21** · `houses` **17** · `entrance` **17** · `suburb` **8** | 259 union |
| `capitol building` · `official building` · `bureaucracy` | **0** | `flag wind` **45** · `flag pole` **14** · `usa flag` **12** · `parliament building` **6** | 78 union |
| `typewriter` · `old typwriter` · `handwriting` · `newspaper` · `print press` · `turning pages` | **0** | `press` **52** · `news` **10** · `calligraphy` **8** · `flipping` **4** · `news paper` **3** | 78 union |
| `elevator` · `lobby` · `meeting room` · `empty office` | **0** | `escalator` **23** · `lift` **14** · `meeting` **11** · `conference` **8** · `office room` **6** | 62 union |
| `calendar` · `clock ticking` · `wall clock` · `seasons` | **0** | `winter` **161** · `autumn` **95** · `season` **18** · `hourglass` **13** *(forbidden)* · `second hand` **4** | 287 union |
| `dial` | **0** | `phone hand` **13** | 13 union |
| `padlock` · `keyhole` · `locked` | **0** | `chain` **46** · `lock chain` **31** · `bolt` **5** · `locking` **2** · `old key` **1** | 54 union |
| `hands working` | **0** | `man hand` **57** · `hand close` **28** · `hands close` **20** · `hands person` **9** | 98 union |
| `grey sky` | **0** | `gray sky` **1** · `cloudy sky` **26** · `cloudy` **54** · `dark clouds` **10** · `haze` **6** | 70 union |
| `constitution` · `statute` · `legal` · `law book` · `legislation` · `official document` · `senate` · `archive documents` · `document old` | **0** | `chamber` **10** · `old paper` **5** · `certificate` **2** · `law office` **2** · `assembly` **1** | 26 union |

Three of those rows are worth reading twice:

- **`grey sky` 0 → `gray sky` 1 → `cloudy sky` 26.** The zero was a spelling. This is the exact
  failure mode the standing note names (`typewriter`→0 but `old typwriter`→1), and it is why a zero
  is never recorded until it has been re-asked.
- **`old typwriter` was 1 the last time the channel measured it and is 0 today.** Not because the
  shelf changed — because that one clip is now held by another episode's `factory*` folder. A
  measured supply figure has a shelf life.
- **`documents` 54 title matches, 53 on disk, 0 unused. `envelope` 19 / 17 / 0. `courthouse`
  11 / 7 / 0.** These are not gaps in the shelf. They are gaps left by sixty-six previous episodes.

### The four real gaps, and what fills them

| gap | measured | filled by |
|---|---|---|
| **a sealed letter / envelope on a table** | `envelope`, `mailbox`, `post box`, `paper letter` all 0 usable | **generated plates.** R018–R031 in the image order. This is the second thumbnail plate and the ENDING image, so it cannot be approximated |
| **a desk drawer, opening and closing** | `drawer`, `desk drawer`, `office drawer`, `opening drawer` all 0 usable | **generated plates.** R032–R041. It is the majority's own metaphor (HD-08) and the film argues with it for four minutes |
| **an American courthouse, exterior** | `courthouse`, `supreme court`, `court building` all 0 usable; `architecture` 433 is European and civic, not judicial | **generated plates** R042–R053 for the two courts, plus archive `dome` / `old building` / `historic building` for approach and scale only. **No re-enacted courtroom interior at all** (§6) |
| **a car-dealership sales desk** | `car showroom` 1, `showroom` 1, `car dealership` 0 | **generated plates** R001–R017. The archive supplies the forecourt, the parked rows and the car exterior; everything at the desk is generated |

---

## 4. The queries, verbatim, with measured hit counts

586 queries over 20 registers, both rounds merged. `title-AND` = ledger rows whose title contains
every term. `on disk` = of those, the file exists and is 1–120 MB. `unused` = of those, the id is in
no episode's `factory*` folder. `>=1920x1080 & unused` = the operative supply figure, joined against
`_ledger/video_resolution.json`. `union` on each heading is the count of **distinct** clip ids in
that last column across the register's queries — it is not the column sum, because one clip answers
several queries.

**A hit count is not a supply count.** Each register heading also carries the count that survives an
off-register title screen (crypto, city, beach, food, sport, wedding, medical, space, war, racing,
3d…) and the `forbidden_subjects` screen, plus three real titles from the survivors so the number
can be judged rather than believed. Read them: `lock chain` is full of blockchain, `customer` is
full of baristas, and `field`-class words are full of holiday footage. **The screened figure is the
number of clips a person has to look at — not the number that will survive looking.**

### R1_dealership_showroom_car   union 384
screened supply **304** after removing 73 off-register and 21 `forbidden_subjects` titles. Examples of what the union is made of: *light streaks of vehicles travelling at night in timelapse mode* / *super fast footage of vehicle traveling at night* / *an automated analyser in a lab*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `vehicle` | 342 | 252 | 227 | **213** |
| `auto` | 202 | 138 | 132 | **119** |
| `automobile` | 86 | 57 | 55 | **51** |
| `customer` | 51 | 39 | 30 | **24** |
| `car park` | 62 | 36 | 23 | **20** |
| `parking lot` | 40 | 28 | 17 | **12** |
| `purchase` | 14 | 11 | 11 | **11** |
| `key hand` | 35 | 26 | 15 | **10** |
| `new car` | 13 | 12 | 11 | **10** |
| `car lot` | 27 | 15 | 13 | **7** |
| `car show` | 6 | 6 | 6 | **5** |
| `car key` | 16 | 7 | 7 | **4** |
| `car door` | 8 | 8 | 6 | **4** |
| `car window` | 25 | 10 | 6 | **4** |
| `sports car` | 12 | 4 | 4 | **3** |
| `car interior` | 7 | 5 | 3 | **3** |
| `car parked` | 12 | 11 | 3 | **3** |
| `cars parking` | 4 | 3 | 3 | **3** |
| `keys` | 48 | 21 | 10 | **2** |
| `auto shop` | 3 | 2 | 2 | **1** |
| `car sale` | 21 | 2 | 1 | **1** |
| `car showroom` | 1 | 1 | 1 | **1** |
| `showroom` | 1 | 1 | 1 | **1** |
| `steering wheel` | 10 | 1 | 1 | **1** |

Still 0 usable after both rounds: `car keys` - `car buy` - `buying car` - `car dealer` - `car dealership` - `car sales` - `car service` - `dealership` - `garage car` - `salesman`

### R2_counter_paperwork_signing   union 773
screened supply **593** after removing 168 off-register and 13 `forbidden_subjects` titles. Examples of what the union is made of: *counting currency notes in hand close up* / *dynamic digital waveform in futuristic setting* / *blue light tunnel with a spiral design*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `sign` | 957 | 413 | 309 | **275** |
| `pen` | 577 | 378 | 269 | **191** |
| `form` | 280 | 177 | 151 | **135** |
| `office work` | 149 | 118 | 64 | **57** |
| `notes` | 86 | 70 | 46 | **40** |
| `desk` | 197 | 142 | 61 | **39** |
| `writing` | 158 | 130 | 51 | **35** |
| `work desk` | 101 | 78 | 37 | **26** |
| `desk office` | 101 | 71 | 28 | **25** |
| `office desk` | 101 | 71 | 28 | **25** |
| `counter` | 95 | 26 | 22 | **16** |
| `write` | 141 | 119 | 20 | **16** |
| `agreement` | 10 | 9 | 7 | **7** |
| `pencil` | 21 | 8 | 6 | **5** |
| `business meeting` | 24 | 12 | 5 | **4** |
| `invoice` | 4 | 4 | 4 | **4** |
| `filling` | 13 | 9 | 4 | **2** |
| `handing` | 5 | 4 | 4 | **2** |
| `customer service` | 10 | 6 | 3 | **2** |
| `signing` | 40 | 39 | 5 | **1** |
| `contract` | 28 | 24 | 4 | **1** |
| `receipt` | 4 | 4 | 3 | **1** |
| `papers` | 36 | 34 | 1 | **1** |

Still 0 usable after both rounds: `signing contract` - `notepad` - `paperwork` - `document signing` - `pen paper` - `application form` - `checklist` - `clipboard` - `form filling` - `hand writing` - `hands writing` - `signature` - `signing paper` - `table papers` - `writing document`

### R3_screen_database_matching   union 688
screened supply **453** after removing 234 off-register and 2 `forbidden_subjects` titles. Examples of what the union is made of: *modern data center in urban business district* / *a motion graphic illustration* / *man analyzing graphs*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `computer` | 526 | 380 | 256 | **238** |
| `graph` | 468 | 263 | 242 | **206** |
| `network` | 230 | 156 | 154 | **141** |
| `computer work` | 177 | 145 | 98 | **92** |
| `laptop` | 186 | 151 | 110 | **89** |
| `data` | 222 | 86 | 76 | **57** |
| `typing` | 140 | 134 | 63 | **46** |
| `chart` | 94 | 41 | 37 | **29** |
| `digital data` | 98 | 33 | 32 | **29** |
| `keyboard` | 121 | 78 | 30 | **25** |
| `computer screen` | 61 | 37 | 23 | **21** |
| `binary` | 31 | 14 | 13 | **13** |
| `programming` | 30 | 17 | 14 | **10** |
| `monitor screen` | 22 | 15 | 8 | **8** |
| `mouse` | 15 | 8 | 7 | **7** |
| `software` | 15 | 8 | 7 | **7** |
| `data analysis` | 15 | 5 | 5 | **5** |
| `searching` | 9 | 9 | 7 | **4** |
| `computer mouse` | 7 | 5 | 4 | **4** |
| `algorithm` | 3 | 3 | 3 | **3** |
| `server` | 21 | 16 | 14 | **2** |
| `computer server` | 7 | 3 | 3 | **2** |
| `clicking` | 3 | 2 | 2 | **2** |
| `data screen` | 5 | 3 | 2 | **2** |
| `data center` | 12 | 11 | 8 | **1** |
| `browser` | 1 | 1 | 1 | **1** |
| `code screen` | 7 | 5 | 1 | **1** |
| `screen code` | 7 | 5 | 1 | **1** |
| `screen text` | 17 | 3 | 1 | **1** |
| `web search` | 2 | 1 | 1 | **1** |

Still 0 usable after both rounds: `server room` - `datacenter` - `servers` - `big data` - `cursor` - `database` - `excel` - `search bar` - `search engine` - `spreadsheet` - `table data`

### R4_mail_letter_envelope   union 81
screened supply **58** after removing 23 off-register and 0 `forbidden_subjects` titles. Examples of what the union is made of: *a person using magnifying glass on stamps* / *a man holding a charity yard sale poster* / *poster and coins*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `shipping` | 53 | 35 | 35 | **33** |
| `delivery` | 43 | 35 | 22 | **17** |
| `post` | 39 | 26 | 18 | **16** |
| `package` | 22 | 21 | 15 | **11** |
| `stamp` | 15 | 12 | 7 | **6** |
| `parcel` | 10 | 9 | 6 | **5** |
| `delivery man` | 12 | 12 | 7 | **4** |
| `courier` | 7 | 7 | 5 | **4** |
| `letter` | 138 | 54 | 1 | **1** |
| `mail` | 15 | 10 | 1 | **1** |
| `postcard` | 1 | 1 | 1 | **1** |

Still 0 usable after both rounds: `correspondence` - `envelop` - `envelope` - `envelopes` - `letter paper` - `letterbox` - `letters` - `mail box` - `mailbox` - `old letter` - `old letters` - `opening letter` - `paper letter` - `paper mail` - `post box` - `post office` - `postal` - `postman` - `write letter` - `writing letter`

### R5_drawer_file_cabinet   union 119
screened supply **106** after removing 12 off-register and 1 `forbidden_subjects` titles. Examples of what the union is made of: *technician looking at tool box* / *a man laying on the floor with boxes on top of him* / *a man laying on the floor with boxes*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `box` | 183 | 136 | 98 | **81** |
| `boxes` | 52 | 50 | 26 | **24** |
| `pile` | 27 | 25 | 15 | **11** |
| `file` | 28 | 22 | 15 | **9** |
| `shelf` | 21 | 20 | 11 | **8** |
| `filing` | 4 | 4 | 4 | **3** |
| `cabinet` | 4 | 3 | 3 | **3** |
| `chest` | 6 | 3 | 3 | **3** |
| `cardboard box` | 14 | 13 | 5 | **2** |
| `records` | 5 | 3 | 2 | **2** |
| `shelves` | 15 | 14 | 2 | **1** |

Still 0 usable after both rounds: `files` - `archive` - `folder` - `binder` - `bookshelf` - `boxes storage` - `cabinet office` - `desk drawer` - `documents` - `drawer` - `file cabinet` - `folders` - `metal cabinet` - `office drawer` - `office files` - `old records` - `opening drawer` - `paper files` - `paper stack` - `papers desk` - `pile paper` - `shelf files` - `stack paper` - `storage boxes` - `wooden desk`

### R6_courthouse_marble_columns   union 613
screened supply **479** after removing 128 off-register and 60 `forbidden_subjects` titles. Examples of what the union is made of: *a large building with a large statue on the front* / *a person holding a statue* / *footage of robert a long high school facade*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `architecture` | 625 | 532 | 446 | **433** |
| `trial` | 178 | 117 | 64 | **49** |
| `statue` | 57 | 48 | 34 | **31** |
| `old building` | 77 | 61 | 28 | **28** |
| `dome` | 45 | 29 | 27 | **26** |
| `monument` | 29 | 21 | 19 | **17** |
| `court` | 57 | 39 | 22 | **14** |
| `historic building` | 30 | 21 | 12 | **10** |
| `washington` | 29 | 26 | 14 | **9** |
| `stairs` | 45 | 31 | 9 | **9** |
| `facade` | 23 | 19 | 8 | **8** |
| `city hall` | 18 | 13 | 6 | **6** |
| `government building` | 19 | 18 | 6 | **6** |
| `steps` | 11 | 8 | 6 | **5** |
| `pillar` | 21 | 14 | 4 | **4** |
| `marble` | 11 | 9 | 4 | **3** |
| `town hall` | 11 | 7 | 3 | **3** |
| `arches` | 3 | 3 | 3 | **2** |
| `justice` | 29 | 23 | 2 | **2** |
| `capitol` | 37 | 35 | 3 | **1** |
| `column` | 9 | 8 | 1 | **1** |
| `pillars` | 8 | 6 | 1 | **1** |
| `staircase` | 7 | 7 | 1 | **1** |

Still 0 usable after both rounds: `government office` - `judge` - `state capitol` - `supreme court` - `classical building` - `colonnade` - `columns` - `court building` - `court room` - `courthouse` - `courtroom` - `federal building` - `marble floor` - `staircase stone` - `steps building` - `stone columns`

### R7_crowd_anonymous_people   union 297
screened supply **248** after removing 48 off-register and 6 `forbidden_subjects` titles. Examples of what the union is made of: *group of people shaking hands* / *urban evening traffic with busy pedestrians* / *a man walking crossing the street*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `people city` | 135 | 108 | 99 | **97** |
| `street people` | 114 | 95 | 79 | **76** |
| `people walking` | 118 | 112 | 82 | **72** |
| `crowd` | 126 | 47 | 38 | **36** |
| `walking street` | 48 | 45 | 31 | **29** |
| `busy street` | 37 | 35 | 27 | **25** |
| `pedestrians` | 30 | 29 | 25 | **24** |
| `office people` | 35 | 30 | 22 | **21** |
| `city crowd` | 25 | 12 | 12 | **12** |
| `line people` | 19 | 14 | 12 | **12** |
| `group people` | 28 | 17 | 12 | **11** |
| `crowd street` | 30 | 10 | 10 | **10** |
| `waiting` | 49 | 33 | 14 | **6** |
| `crowd walking` | 10 | 8 | 6 | **6** |
| `station people` | 14 | 9 | 6 | **5** |
| `people crossing` | 5 | 5 | 5 | **5** |
| `people standing` | 6 | 5 | 5 | **5** |
| `commuters` | 5 | 5 | 2 | **2** |
| `silhouettes people` | 3 | 3 | 2 | **2** |
| `subway people` | 3 | 3 | 2 | **1** |
| `many people` | 2 | 1 | 1 | **1** |

Still 0 usable after both rounds: `queue` - `sitting waiting` - `waiting people` - `waiting room` - `waiting line`

### R8_money_damages   union 603
screened supply **407** after removing 195 off-register and 66 `forbidden_subjects` titles. Examples of what the union is made of: *finance nyse wall street new york city* / *dynamic financial charts in a low light workspace* / *close up footage of financial reports on a surface*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `money` | 464 | 412 | 341 | **307** |
| `finance` | 310 | 235 | 225 | **203** |
| `bank` | 239 | 205 | 178 | **148** |
| `cash` | 191 | 176 | 157 | **133** |
| `atm` | 175 | 133 | 121 | **118** |
| `dollar` | 189 | 171 | 154 | **115** |
| `coins` | 168 | 140 | 118 | **60** |
| `financial` | 93 | 66 | 61 | **57** |
| `dollars` | 75 | 70 | 63 | **51** |
| `banknotes` | 34 | 32 | 24 | **21** |
| `savings` | 29 | 20 | 20 | **16** |
| `credit card` | 24 | 22 | 20 | **12** |
| `payment` | 20 | 16 | 12 | **9** |
| `budget` | 18 | 8 | 8 | **5** |
| `wallet` | 7 | 6 | 6 | **5** |
| `counting money` | 34 | 33 | 3 | **3** |
| `calculator` | 45 | 29 | 8 | **2** |
| `accounting` | 4 | 2 | 2 | **2** |

### R9_travel_cancelled_trip   union 514
screened supply **347** after removing 165 off-register and 43 `forbidden_subjects` titles. Examples of what the union is made of: *light streaks of vehicles travelling at night in timelapse mode* / *super fast footage of vehicle traveling at night* / *blood collection tubes being checked*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `travel` | 493 | 330 | 303 | **275** |
| `flight` | 122 | 65 | 61 | **58** |
| `airport` | 75 | 64 | 57 | **47** |
| `holiday` | 181 | 55 | 52 | **47** |
| `vacation` | 108 | 54 | 49 | **46** |
| `airplane` | 44 | 35 | 34 | **31** |
| `check in` | 49 | 43 | 33 | **24** |
| `terminal` | 32 | 25 | 21 | **16** |
| `sky plane` | 25 | 12 | 10 | **9** |
| `airport terminal` | 9 | 9 | 8 | **8** |
| `border` | 26 | 9 | 5 | **5** |
| `trolley` | 7 | 7 | 5 | **5** |
| `boarding` | 12 | 9 | 7 | **4** |
| `packing` | 8 | 6 | 5 | **4** |
| `airplane sky` | 7 | 4 | 4 | **4** |
| `luggage` | 9 | 6 | 4 | **4** |
| `backpack` | 7 | 5 | 5 | **3** |
| `departure` | 12 | 3 | 3 | **3** |
| `passport` | 8 | 6 | 6 | **2** |
| `empty airport` | 3 | 3 | 2 | **2** |
| `bag travel` | 1 | 1 | 1 | **1** |
| `traveler` | 3 | 1 | 1 | **1** |

Still 0 usable after both rounds: `suit case` - `suitcase` - `airplane window` - `luggage bag` - `packing bag` - `plane window` - `window seat`

### R10_home_family_suburb   union 461
screened supply **340** after removing 117 off-register and 19 `forbidden_subjects` titles. Examples of what the union is made of: *a coastline village* / *the entrance to the building has a large sign that says the sun shines for us * / *a couple dancing at home*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `door` | 481 | 329 | 195 | **180** |
| `house` | 579 | 374 | 173 | **141** |
| `home` | 286 | 172 | 111 | **87** |
| `village` | 81 | 47 | 34 | **25** |
| `town street` | 44 | 36 | 23 | **21** |
| `houses` | 94 | 52 | 27 | **17** |
| `entrance` | 53 | 33 | 21 | **17** |
| `family` | 54 | 24 | 21 | **14** |
| `porch` | 30 | 17 | 10 | **10** |
| `suburb` | 50 | 47 | 11 | **8** |
| `living room` | 114 | 23 | 8 | **6** |
| `window home` | 39 | 20 | 6 | **6** |
| `home interior` | 28 | 18 | 4 | **4** |
| `housing` | 9 | 6 | 4 | **4** |
| `table home` | 14 | 10 | 4 | **4** |
| `houses street` | 8 | 5 | 2 | **2** |
| `street houses` | 8 | 5 | 2 | **2** |
| `kitchen` | 79 | 22 | 4 | **1** |
| `apartment` | 23 | 13 | 1 | **1** |
| `doorway` | 6 | 1 | 1 | **1** |
| `driveway` | 2 | 2 | 1 | **1** |
| `driveway car` | 2 | 2 | 1 | **1** |

Still 0 usable after both rounds: `front door` - `garage` - `small town` - `apartment building` - `car garage` - `family home` - `home family` - `neighborhood` - `residential` - `residential area` - `suburban`

### R11_government_treasury_flag   union 506
screened supply **416** after removing 88 off-register and 4 `forbidden_subjects` titles. Examples of what the union is made of: *flags on a skyscraper* / *a large building with a flag on top of it* / *flag swaying in the pole*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `flag` | 593 | 530 | 487 | **456** |
| `national flag` | 85 | 79 | 75 | **71** |
| `flag wind` | 82 | 56 | 52 | **45** |
| `government` | 60 | 57 | 42 | **39** |
| `eagle` | 36 | 27 | 27 | **19** |
| `flag pole` | 23 | 23 | 14 | **14** |
| `usa flag` | 21 | 21 | 17 | **12** |
| `seal` | 19 | 13 | 9 | **6** |
| `parliament building` | 7 | 7 | 6 | **6** |
| `american flag` | 32 | 32 | 4 | **4** |
| `washington dc` | 10 | 10 | 3 | **3** |
| `politics` | 5 | 3 | 3 | **2** |
| `federal` | 12 | 6 | 2 | **2** |
| `white house` | 4 | 4 | 2 | **2** |
| `capitol` | 37 | 35 | 3 | **1** |
| `state building` | 17 | 17 | 2 | **1** |
| `dome building` | 1 | 1 | 1 | **1** |
| `official` | 4 | 1 | 1 | **1** |

Still 0 usable after both rounds: `bureaucracy` - `office government` - `administration` - `capitol building` - `institution` - `ministry` - `official building`

### R12_paper_records_print   union 1002
screened supply **710** after removing 286 off-register and 13 `forbidden_subjects` titles. Examples of what the union is made of: *pink sunset timelapse* / *close up of books collection* / *a man choosing a book*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `paper` | 1013 | 660 | 478 | **442** |
| `ink` | 766 | 449 | 404 | **328** |
| `book` | 419 | 293 | 176 | **155** |
| `library` | 146 | 134 | 92 | **71** |
| `reading` | 157 | 135 | 70 | **60** |
| `press` | 155 | 74 | 58 | **52** |
| `library books` | 54 | 50 | 34 | **33** |
| `printing` | 50 | 50 | 30 | **22** |
| `notebook` | 66 | 50 | 13 | **12** |
| `news` | 98 | 53 | 19 | **10** |
| `calligraphy` | 16 | 9 | 8 | **8** |
| `old book` | 18 | 17 | 6 | **6** |
| `old paper` | 33 | 21 | 6 | **5** |
| `flipping` | 18 | 15 | 7 | **4** |
| `news paper` | 38 | 37 | 4 | **3** |
| `magazine` | 4 | 3 | 2 | **2** |
| `pages` | 28 | 12 | 2 | **2** |
| `press paper` | 12 | 4 | 2 | **1** |
| `printer` | 19 | 8 | 2 | **1** |
| `document paper` | 8 | 4 | 1 | **1** |
| `printing machine` | 7 | 7 | 1 | **1** |
| `typing machine` | 1 | 1 | 1 | **1** |

Still 0 usable after both rounds: `hand write` - `type writer` - `typewriter` - `print press` - `book pages` - `handwriting` - `newspaper` - `old typwriter` - `pages book` - `printing press` - `turning pages` - `writing machine`

### R13_corporate_office_tower   union 663
screened supply **486** after removing 171 off-register and 43 `forbidden_subjects` titles. Examples of what the union is made of: *flags on a skyscraper* / *a glass building in lisbon* / *a glass building on lisbon street*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `business` | 648 | 405 | 326 | **274** |
| `city buildings` | 253 | 216 | 191 | **182** |
| `office` | 416 | 326 | 160 | **142** |
| `skyscraper` | 151 | 108 | 102 | **90** |
| `downtown` | 77 | 59 | 48 | **45** |
| `escalator` | 43 | 40 | 31 | **23** |
| `corporate` | 76 | 23 | 22 | **20** |
| `lift` | 61 | 32 | 20 | **14** |
| `meeting` | 350 | 56 | 27 | **11** |
| `office building` | 19 | 14 | 11 | **10** |
| `glass building` | 17 | 14 | 9 | **9** |
| `conference` | 47 | 27 | 10 | **8** |
| `office room` | 25 | 17 | 6 | **6** |
| `business district` | 5 | 4 | 4 | **3** |
| `hall building` | 9 | 5 | 3 | **3** |
| `modern office` | 13 | 13 | 3 | **3** |
| `office window` | 10 | 4 | 2 | **2** |
| `workplace` | 8 | 4 | 1 | **1** |

Still 0 usable after both rounds: `boardroom` - `reception` - `abandoned office` - `cubicle` - `elevator` - `empty office` - `entrance hall` - `lobby` - `meeting room` - `office chair` - `office empty`

### R14_clock_time_years   union 1405
screened supply **850** after removing 536 off-register and 126 `forbidden_subjects` titles. Examples of what the union is made of: *pink sunset timelapse* / *timelapse of a sunset* / *timelapse of manhattan at sunset*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `sunset` | 976 | 746 | 654 | **575** |
| `time` | 924 | 635 | 488 | **407** |
| `sunrise` | 449 | 243 | 203 | **173** |
| `winter` | 501 | 254 | 181 | **161** |
| `timelapse` | 186 | 177 | 136 | **120** |
| `watch` | 185 | 115 | 108 | **99** |
| `autumn` | 290 | 173 | 124 | **95** |
| `clock` | 231 | 69 | 28 | **24** |
| `season` | 77 | 20 | 18 | **18** |
| `hourglass` | 20 | 16 | 14 | **13** |
| `night day` | 11 | 9 | 8 | **6** |
| `second hand` | 6 | 5 | 4 | **4** |
| `old clock` | 15 | 5 | 3 | **3** |
| `hands clock` | 6 | 4 | 2 | **2** |
| `shadows` | 14 | 8 | 2 | **2** |
| `vintage clock` | 12 | 4 | 2 | **1** |
| `dates` | 2 | 1 | 1 | **1** |

Still 0 usable after both rounds: `analog clock` - `calendar` - `clock face` - `clock ticking` - `clock wall` - `day month` - `month` - `seasons` - `ticking` - `wall clock`

### R15_phone_call_waiting   union 151
screened supply **143** after removing 7 off-register and 1 `forbidden_subjects` titles. Examples of what the union is made of: *a woman using her smartphone* / *young man focusing on smartphone at night* / *a person holding a smartphone*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `phone` | 388 | 253 | 184 | **147** |
| `smartphone` | 110 | 67 | 58 | **51** |
| `mobile phone` | 55 | 22 | 21 | **16** |
| `cell phone` | 46 | 32 | 18 | **16** |
| `phone hand` | 35 | 22 | 17 | **13** |
| `hold phone` | 21 | 18 | 14 | **10** |
| `phone screen` | 37 | 16 | 12 | **8** |
| `phone call` | 30 | 21 | 13 | **6** |
| `telephone` | 46 | 33 | 10 | **6** |
| `answering` | 8 | 8 | 5 | **3** |
| `calling` | 6 | 6 | 4 | **3** |
| `old telephone` | 3 | 2 | 1 | **1** |

Still 0 usable after both rounds: `dial` - `dialing` - `button phone` - `landline` - `receiver` - `rotary`

### R16_lock_list_security   union 372
screened supply **262** after removing 94 off-register and 23 `forbidden_subjects` titles. Examples of what the union is made of: *close up of a person pressing on a keypad* / *flock of birds flying at sunset* / *a person putting a smartphone in a locker*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `lock` | 447 | 252 | 181 | **139** |
| `key` | 445 | 199 | 129 | **99** |
| `fence` | 126 | 114 | 70 | **62** |
| `chain` | 77 | 59 | 47 | **46** |
| `chain lock` | 44 | 35 | 31 | **31** |
| `lock chain` | 44 | 35 | 31 | **31** |
| `security` | 72 | 40 | 33 | **28** |
| `safe` | 47 | 27 | 24 | **22** |
| `alarm` | 43 | 22 | 12 | **8** |
| `vault` | 27 | 9 | 9 | **7** |
| `bolt` | 14 | 7 | 7 | **5** |
| `barrier` | 13 | 10 | 5 | **5** |
| `surveillance` | 6 | 3 | 3 | **3** |
| `locking` | 7 | 7 | 2 | **2** |
| `old key` | 21 | 11 | 6 | **1** |
| `cctv` | 3 | 2 | 2 | **1** |
| `security camera` | 5 | 3 | 2 | **1** |
| `door lock` | 12 | 10 | 1 | **1** |

Still 0 usable after both rounds: `closed door` - `iron lock` - `key hole` - `keyhole` - `keys door` - `lock key` - `locked` - `pad lock` - `padlock`

### R17_road_driving_leaving   union 919
screened supply **686** after removing 226 off-register and 112 `forbidden_subjects` titles. Examples of what the union is made of: *pedestrian traffic light* / *midwest traffic* / *traffic light timer*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `road` | 1219 | 960 | 758 | **640** |
| `traffic` | 682 | 574 | 498 | **427** |
| `highway` | 354 | 286 | 218 | **189** |
| `driving` | 201 | 168 | 138 | **104** |
| `car driving` | 150 | 124 | 104 | **82** |
| `street night` | 135 | 123 | 33 | **30** |
| `intersection` | 32 | 30 | 24 | **24** |
| `country road` | 60 | 47 | 18 | **15** |
| `road trip` | 26 | 20 | 16 | **14** |
| `empty road` | 24 | 21 | 12 | **12** |
| `road sign` | 17 | 11 | 7 | **6** |
| `driving night` | 14 | 13 | 6 | **4** |
| `rear view` | 5 | 4 | 2 | **1** |
| `windshield` | 9 | 7 | 1 | **1** |

### R18_hands_person_close   union 581
screened supply **513** after removing 61 off-register and 11 `forbidden_subjects` titles. Examples of what the union is made of: *counting currency notes in hand close up* / *a person holding a smartphone* / *a person holding a flask*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `hand` | 824 | 498 | 368 | **265** |
| `hands` | 377 | 291 | 224 | **167** |
| `holding` | 266 | 253 | 170 | **138** |
| `man walking` | 250 | 233 | 150 | **121** |
| `man hand` | 177 | 108 | 86 | **57** |
| `silhouette` | 154 | 86 | 58 | **53** |
| `man hands` | 94 | 68 | 56 | **41** |
| `woman walking` | 66 | 60 | 42 | **36** |
| `hand holding` | 59 | 53 | 43 | **34** |
| `woman hands` | 62 | 47 | 42 | **32** |
| `man sitting` | 75 | 70 | 37 | **32** |
| `hand close` | 75 | 65 | 35 | **28** |
| `hands close` | 40 | 36 | 22 | **20** |
| `fingers` | 40 | 22 | 19 | **9** |
| `hands person` | 18 | 16 | 11 | **9** |
| `hands work` | 13 | 13 | 10 | **7** |
| `person sitting` | 10 | 9 | 4 | **4** |
| `portrait` | 5 | 5 | 4 | **4** |
| `back person` | 7 | 5 | 4 | **3** |
| `hands together` | 3 | 3 | 2 | **1** |
| `craft hands` | 1 | 1 | 1 | **1** |
| `hands table` | 3 | 2 | 1 | **1** |

Still 0 usable after both rounds: `hands working` - `working hands`

### R19_weather_mood_silence   union 1488
screened supply **1001** after removing 481 off-register and 180 `forbidden_subjects` titles. Examples of what the union is made of: *time lapse video of dark and cloudy sky* / *clouds in the sky* / *dramatic cloudscape over mountain range at sunset*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `clouds` | 861 | 642 | 544 | **521** |
| `rain` | 1081 | 649 | 391 | **336** |
| `wind` | 906 | 463 | 251 | **225** |
| `night city` | 321 | 285 | 167 | **151** |
| `fog` | 516 | 262 | 154 | **142** |
| `dusk` | 137 | 101 | 79 | **74** |
| `cloudy` | 99 | 79 | 59 | **54** |
| `mist` | 252 | 134 | 60 | **50** |
| `storm` | 191 | 100 | 57 | **48** |
| `cloudy sky` | 46 | 42 | 31 | **26** |
| `rain street` | 55 | 42 | 20 | **18** |
| `dark room` | 33 | 33 | 16 | **14** |
| `empty street` | 27 | 23 | 14 | **14** |
| `dark clouds` | 21 | 17 | 10 | **10** |
| `overcast` | 24 | 21 | 7 | **6** |
| `haze` | 38 | 9 | 6 | **6** |
| `rain window` | 132 | 44 | 3 | **2** |
| `window rain` | 132 | 44 | 3 | **2** |
| `gray sky` | 2 | 2 | 1 | **1** |
| `puddle` | 17 | 14 | 1 | **1** |

Still 0 usable after both rounds: `drizzle` - `grey sky` - `sky grey`

### R20_law_statute_congress   union 62
screened supply **53** after removing 6 off-register and 3 `forbidden_subjects` titles. Examples of what the union is made of: *video of a man voting* / *people handing out papers for voting* / *a person voting*

| query | title-AND | on disk | unused | >=1920x1080 & unused |
|---|---:|---:|---:|---:|
| `law` | 229 | 69 | 22 | **21** |
| `chamber` | 16 | 13 | 10 | **10** |
| `voting` | 10 | 9 | 9 | **9** |
| `parliament` | 11 | 10 | 8 | **8** |
| `old paper` | 33 | 21 | 6 | **5** |
| `certificate` | 3 | 3 | 2 | **2** |
| `justice` | 29 | 23 | 2 | **2** |
| `law office` | 8 | 8 | 2 | **2** |
| `assembly` | 18 | 2 | 2 | **1** |
| `attorney` | 5 | 5 | 1 | **1** |
| `code book` | 1 | 1 | 1 | **1** |
| `congress` | 2 | 2 | 1 | **1** |
| `declaration` | 2 | 1 | 1 | **1** |
| `hearing` | 7 | 1 | 1 | **1** |
| `regulation` | 1 | 1 | 1 | **1** |
| `vintage paper` | 4 | 3 | 1 | **1** |

Still 0 usable after both rounds: `constitution` - `document old` - `government meeting` - `old document` - `parchment` - `thick book` - `archive documents` - `archives` - `books law` - `congress hall` - `documents archive` - `historic document` - `law book` - `lawyer` - `legal` - `legal book` - `legislation` - `official document` - `parliament hall` - `rule book` - `seal document` - `senate` - `stamp document` - `statute`

---

## 5. The cut budget, checked so the contract is satisfiable

EP66 declared a contract its own cut budget could not satisfy — 350 distinct video assets against a
video-cut ceiling of 311 — and that arithmetic was only found after the plan was written. It is done
first here.

```
runtime band (episode_spec)                        1560 .. 1895 s      (design centre 1720 s)
target_cut_sec (episode_spec)                              3.8 s
total cuts                    1560/3.8 = 411       1720/3.8 = 453      1895/3.8 = 499
stills may occupy at most 32% of cuts                      131                  145         160
video cuts available          411-131 = 280        453-145 = 308       499-160 = 339
mandatory_stills declared                                   96         -> fits at every edge
distinct_video_assets declared                             260         -> fits at every edge
video cuts this plan allocates (s2)                        323         -> the design-centre figure
```

**260 distinct sources over 323 video cuts** gives a distinct fraction of **0.805** against the
`footage_diversity` floor of **0.40**, and leaves 63 second uses to spread — comfortably inside the
`reuse ≤ 4` cap and the `generic symbols ≤ 2` cap. `footage_utilization` wants **≥ 80%** of staged
clips actually used; staging 300–320 against 260 required keeps that reachable, and staging 600
would not. **Do not stage the whole 5,537.**

`animation_density` (near-still ≤ 10% of runtime, single hold ≤ 3.0 s) and `motion_density`
(≥ 2.5 kinetic beats/min, coverage ≥ 0.25, variety ≥ 3) are met by the motion budget in the film
bible §6 and §12.5, not by this document. What this document owes them is **enough distinct moving
footage that no cut has to be a held still**, and 323 video cuts at 3.8 s is that.

---

## 6. Screening rules a machine cannot apply, and who applies them

`footage_review_required` is **true** in the contract. These are the judgements a person makes over
a labelled contact sheet before any clip enters a cut. The factory shelf's filename labels have
measured **~40–50% wrong**, and 683 of 1,094 clips across five earlier episodes were wrong for their
story when somebody finally looked.

1. **No courtroom interior, re-enacted or stock.** Everything the two courts did in this story is
   text — an opinion, a dissent, a jury form. Stock "courtroom" footage is a television set and it
   would be the one place this film pretends. The courts are exteriors, stone, doors and typography.
2. **No screen that can be read.** Any monitor, phone or laptop in any cut must be out of focus,
   turned away, or blown out. A legible screen next to this narration reads as *the actual credit
   report*, which is barred outright (⛔-13, invariant 11).
3. **No brand marks, no licence plates, no dealership signage, no bank logos.** The corporation in
   this film is real, living and named in the narration. It is never shown.
4. **People: required, and faces are allowed** — see §7. What is barred is a *real, identifiable
   individual's likeness*, and above all anything a viewer could take for Sergio Ramirez, his wife,
   his father-in-law, the salesman, or the two people on the sanctions list whose names the record
   does not print.
5. **No war, no weapons, no extremism, no narcotics, no arrest, in any clip, at any point.** The
   contract blocks them by title; a human blocks them by looking. A film about a man wrongly called
   a terrorist that cuts to stock terror footage has made the mistake it is describing.
6. **Register check, per clip:** is this the United States, and is it 2011 or timeless? A Bangkok
   street, a European plaza and a 1970s newsreel are all off-register here and all of them survive
   every machine gate.
7. **No-repeat, across the film and across the channel.** Within the film, a clip is used at most
   twice unless the repetition is an argument the bible names (the drawer, the envelope and the
   forecourt are the three deliberate motif returns). Across the channel, §1 filter 7 has already
   excluded every id another episode holds; before staging, re-run
   `py -3.11 scripts/check_cross_episode_reuse.py --build` so `STAGED_CLIP_INDEX.json` is current,
   because the count moved by 71 ids during this measurement alone.

### The staging command

```bash
# dry run first, always
py -3.11 scripts/stage_footage_by_title.py --slug ramirez --per-query 3 --dry-run \
  --query "auto" --query "customer" --query "purchase" --query "key hand" ...

# then the contact sheet, then a person looks at it, then the pool is trimmed
py -3.11 scripts/search_archive.py --shot "car showroom sales desk" --kind video --sheet --limit 24
```

---

## 7. The people lane — required, not tolerated

**Owner decision 2026-07-04: depicted people are REQUIRED and welcome. The only thing barred is the
likeness of a real, identifiable individual** (CLAUDE invariant 11). This is a film about a man
standing at a counter with his wife and his father-in-law; a version of it with nobody in it would
be absurd, and EP60 shipped exactly that and was wrong.

- `episode_spec.people_plates_min` = **24**, and `episode_spec.people_plates` names them:
  **R073–R096**. That is a declared list, not a filename convention, because
  `check_episode_inputs` once reported 0 of 10 on forty plates that existed and were correct.
- **Register R18 (hands, backs, figures) owes 20 of the 323 video cuts**, and it is the only
  register whose clips are all review-required by default: 82 of the union's titles name a human,
  and a title that names a human is a candidate, never supply.
- **Faces are allowed in generated plates.** What is not allowed is a face presented as a specific
  real person in this record. The image order's rule is: a face may appear when it belongs to nobody
  in the story — a passer-by, a crowd, a clerk at a different counter — and must not appear in any
  plate captioned or cut as Ramirez, his family, the salesman, or a named justice.

---

## 8. What must happen next, in order

1. Re-run `scripts/check_cross_episode_reuse.py --build`; the staged-id count is moving.
2. Stage 300–320 clips with `--dry-run` first, from the §4 queries with the highest screened counts
   in each register, **not** from the highest raw counts.
3. Build labelled contact sheets and **have a person look at them.** Record a verdict per clip;
   `footage_review_required` is true and a stamped-without-looking QC is the failure this contract
   exists to stop.
4. Commission the four generated-plate groups in §3 (R001–R053), which the archive cannot supply.
5. Only then build `ramirez_film.json`, and run `check_spec_satisfied.py` before the render.

*Measured 2026-08-11 in one ledger pass. 586 queries, two rounds, 87 zeros re-asked in other words
before any of them was recorded as a gap. Nothing was staged and nothing was moved.*

---

> **Correction, 2026-08-12.** *(corrected 2026-08-12: the declaration was lowered to **222** in `episode_spec.v002.json` — 260 was never derived from the allocator; see `decisions/0009-DISTINCT-VIDEO-ASSETS-CORRECTION.md`. The figure below is the retired one, kept for provenance.)*
