# EP71 · OROVILLE — FOOTAGE QUERY PLAN v001

**Date 2026-08-20 · slug `oroville` · episode `PD-2026-071-oroville`**
**Contract `episodes/PD-2026-071-oroville/episode_spec.v001.json` — `distinct_video_assets` **260**,
`target_cut_sec` **3.8**, `runtime_seconds` **[1625, 1900]**, `footage_review_required` **true**,
131 `forbidden_subjects`, `era_setting` **Oroville, Butte County, California, USA, 2005–2023**.**

> **Nothing here was staged or copied.** Every number came from
> `stage_footage_by_title.py --emit-candidates`, the same selector `prestage_footage_review.py`
> calls, run against the archive ledger rebuilt from disk that morning.

> **Counts are a lower bound taken at 2026-08-20 04:2x**, with the restock lane still running.
> **Re-measure before staging.**

---

## 0. Result in one block

```
contract distinct_video_assets                             260
video cuts this film has room for (s5)                     427
queries in the final set                                   101
clips the selector would take across 14 registers         3954
registers returning zero                                     0
usable-licence videos in the ledger at measurement       13,345
  of which screened out by this episode's 131 bans        1,536
  searchable after title screens                         11,397
candidates presented for a content verdict                 276  (of 534, 258 dropped mechanically)
labelled contact sheets built                               92
```

**The count is not the problem. The continent is.** 3,954 against 260 required is a factor of
15, and every register answers — but §3 is the part of this document that decides whether this
film can be dressed.

---

## 1. The instrument

Identical to EP70's, and for the same reason: the staging tool's own selection rather than a
second implementation of it (invariant 14). Extension, `OK_LICENSE`, `TITLE_BLOCK`,
`RIP_SIGNATURE`, the 131 `forbidden_subjects`, title-word match, file present and 1–120 MB,
and exclusion of the 10,104 ids other episodes already hold plus 2,135 ids a recorded verdict
rejected.

**The ledger was verified against the files, not against its own row count.**
`check_ledger_integrity.py`: 60,572 rows, 60,572 distinct `file_path`, 0 torn, 0 duplicated,
0 media files without a row.

**The forbidden screen was shown rejecting before it was trusted** — `flooding` and `rescue` are
refused for this episode by name, which is the whole point of it existing here.

---

## 2. The registers, and how many cuts each one owes

| # | register | what it is for in THIS film | cuts | measured |
|---|---|---|---:|---:|
| R1 | river, water, dam, channel | the Feather River and the structure itself | 60 | 774 |
| R2 | valley, farm, orchard, field | the valley floor that was told to leave | 40 | 192 |
| R3 | cattle, livestock, pasture | what the valley floor is used for | 26 | **450** |
| R4 | two-lane road, highway, dusk | the evacuation route, and the drive back | 48 | 805 |
| R5 | small town, main street, shop | Oroville, Marysville, Yuba City, Live Oak | 32 | 197 |
| R6 | leaving — traffic, bags, buses | 188,000 people, in one afternoon | 34 | 186 |
| R7 | foothills, oak, dry grass | low inland foothill, not mountain | 30 | **275** |
| R8 | sky, cloud, rain, fog | February 2017 was a wet winter | 32 | 266 |
| R9 | engineering, construction, crane | the repair, and the inspections before it | 34 | 197 |
| R10 | civic exterior | FERC, the Department of Water Resources, the Third District | 24 | **140** |
| R11 | documents, report, map, plan | the 2005 FERC motion; the 2023 opinion | 32 | 189 |
| R12 | hands, backs, figures | **the people lane** — no identifiable face | 20 | 223 |
| R13 | texture, reflection | connective tissue | 8 | **15** |
| R14 | clock, calendar | 2005 → 2017 → 2023 | 7 | 45 |

---

## 3. What the shelf does NOT hold — read this before trusting §0

**Every register answers, and the big numbers are carried by a word that is not the subject:**

| register | union | carried by | what that word actually returns |
|---|---:|---|---|
| R3 cattle | 450 | `animal` **422** | any animal — wildlife, pets, birds, zoo. `cattle` **0**, `livestock` **1**, `ranch` **2** |
| R7 foothills | 275 | `mountain` **228** | alpine peaks and snow. Butte County is **low inland foothill**. `foothill` **0**, `hill` **14** |
| R10 civic | 140 | `architecture` **135** | world architecture. `government building` **0**, `columns` **0**, `facade` **0** |
| R1 river/water | 774 | `water` **368** | water of every kind. `spillway` **0**, `reservoir` **0**, `riverbank` **4**, `dam` **16** |
| R4 road | 805 | `road` 288 + `sunset` **226** | `sunset` is a mood, not a road. `rural road` **0**, `country road` **5** |
| R13 texture | **15** | `reflection` 15 | the register barely exists after the off-register terms were removed |

**Four subjects this film is about cannot be reached by any query** and must come from
commissioned plates, i2v, or licensed news/agency material:

1. **The spillway itself** — `spillway` 0, `water release` 0, `hydro` 0, `hydroelectric` 0.
   `dam` returns 16, none of them Oroville. This is the film's own object.
2. **Butte County foothill and dry golden grass** — `foothill` 0, `grassland` 0, `dry grass` 0,
   `golden hills` 0, `hillside` 0. Retried as `hills` (394 standalone), which returns green
   European and alpine slopes, not California summer-dry hills.
3. **Cattle on a valley floor** — `cattle` 0. `animal` 422 is not a substitute.
4. **An American civic or agency building exterior** — 0 by every word tried.

**And one whole register is barred by the spec, correctly.** `flooded`, `breach`,
`dam failure`, `collapse`, `rubble`, `rescue`, `wall of water` are all `forbidden_subjects`.
1,536 titles were screened out on those terms. **No query in this set asks for water doing
damage**, and any future addition that does will be refused by `assert_queries_clean` before it
can harvest — which is exactly the machine-readable constraint EP60 did not have when it staged
31 banned clips.

### The contact sheet that was opened

`footage_review_required` is true. On sheet 22 of 92: **Mount Fuji** (wrong continent),
**London tower cranes** labelled "buildings under construction aerial" (wrong continent, and
this is register R9), a poppy on black (off-register), and one genuinely correct item — a grey
overcast cloudscape, which is exactly the February-2017 sky this film needs. **One of four.**

That is consistent with the episode's own precision sample, which judged **35 of 70** register
clips off-register and is quoted in `episode_spec.notes`. Nothing measured tonight improves
that number, and no machine gate measures it. **A person must read the 92 sheets before any
clip enters a cut.**

The mechanical `setting_mismatch` filter is doing real work here — it removed **74 of 534**,
the highest of any episode measured — but Mount Fuji survived it.

---

## 4. The queries, with measured counts

**Counts are marginal within the run order**, not standalone supply: the selector removes a clip
from the pool once an earlier term has taken it (`hills` measured 394 alone and 0 after `hill`,
`grass` and `countryside`). **The register union is the only figure to trust.**

```
R1_river_water    union 774  water 368, river 188, lake 122, waterfall 20, dam 16, canal 16,
                             flowing water 12, stream 9, channel 9, current 8, riverbank 4,
                             rapids 2
R2_valley_farm    union 192  plant 49, field 49, farm 40, agriculture 15, rural 10,
                             farmland 8, valley 6, tractor 4, wheat 3, barn 3, orchard 2,
                             corn 2, harvest 1
R3_cattle         union 450  animal 422, herd 8, sheep 7, horse 7, grazing 3, ranch 2,
                             livestock 1
R4_two_lane_road  union 805  road 288, sunset 226, highway 134, driving 64, dusk 35,
                             asphalt 28, drive 22, country road 5, roadside 2, headlights 1
R5_small_town     union 197  shop 73, city street 63, town 36, downtown 17, parking lot 5,
                             small town 2, gas station 1
R6_leaving        union 186  traffic 96, cars 26, moving 23, people walking 17, bus 16,
                             boxes 7, suitcase 1
R7_foothills      union 275  mountain 228, grass 15, hill 14, meadow 12, countryside 5,
                             slope 1
R8_sky_rain       union 266  cloud 115, sky 88, rain 40, fog 19, mist 2, weather 1,
                             cloudy sky 1
R9_engineering    union 197  construction 99, worker 29, factory 27, machine 18, crane 11,
                             engineering 6, industry 4, excavator 3
R10_civic         union 140  architecture 135, monument 3, office building 2
R11_documents     union 189  book 62, desk 23, note 21, paper 19, map 18, writing 17,
                             chart 12, plan 8, report 5, document 4
R12_people        union 223  hands 99, walk 89, back 12, crowd 9, figure 8, silhouette 5,
                             boots 1
R13_texture       union  15  reflection 15
R14_time          union  45  watch 37, clock 5, waiting 3
```

---

## 5. The cut budget

```
runtime_seconds low                       1625 s
target_cut_sec                             3.8 s
video cuts if every cut were footage       427
distinct_video_assets required             260
clip floor, runtime_lo // 45                 36   -> not binding
```

427 cuts against 260 distinct assets is an average reuse of 1.6, inside `footage_diversity`
(reuse ≤ 4, distinct ≥ 0.40).

---

## 6. What no machine here can decide

- **Continent and climate, not decade.** 2017 is recent, so contemporary stock is
  period-correct. What is wrong is European, Asian, Middle Eastern or Latin American streets
  and signage, EU/UK plates, right-hand drive, megacity skylines, palms, surf, and anything
  reading as the California coast. Butte County is inland agricultural valley and low foothill.
  Mount Fuji and London cranes both reached the sheets.
- **The disaster register is banned, and that is deliberate.** This film is about a decision
  and a warning, not about water destroying things.
- **`sunset` (226 clips in R4).** A mood word doing a road register's work. Every one needs
  eyes on it before it stands in for a Butte County two-lane at dusk.
- **`animal` (422 in R3).** Until a person looks, this register is unproven.

---

## 7. What must happen next, in order

1. **Let the restock finish**, then re-measure. `ingest_modern_web.py` is running with
   `--cap-gb 1172` (cumulative). Its `small_town` vocabulary reaches R4/R5
   (`rural highway driving night`, `gas station at night`, `mailbox rural road`); its
   `landscapes_timelapse` vocabulary is thin (3 video queries) and will **not** fill R7.
   **Do not add `weather_disasters` or `ocean_nature` to this episode's restock** — both
   harvest exactly what `forbidden_subjects` bans.
2. `py -3.11 scripts/prestage_footage_review.py --slug oroville --dry-run`
3. **Read the 92 sheets in `runs/qc/prestage_frames/oroville` and record the rejects**, then
   `--decide rejects.json --stage`.
4. **Commission plates for the four subjects in §3.** The spillway above all: it is the object
   the film is named after and the shelf has none of it.

---

## 8. Post-restock re-measurement (2026-08-20 05:30)

`ingest_modern_web.py` finished: **717 new items, 17.97 GB**. Ledger re-verified: 61,289 rows =
61,289 files on disk, 0 torn, 0 duplicated, 0 missing.

```
usable-licence videos   13,345 -> 13,694
clips for this episode    3,954 ->  4,142
```

Movement was broad and shallow — R1 774→799, R4 805→859, R5 197→218, R8 266→288 — and
**R13 texture stayed at 15**. None of the four subjects in §3 became reachable.

**A theme label is not a subject**, measured: theme `small_town` holds 585 usable videos and
**not one** carries a subject word in its title (samples: mountain forest road, an Italian
village, Los Angeles traffic); `government_buildings` 30 of 1,061; `police_modern` 70 of 818.
`stage_footage_by_title.py` matches the **title only**, so the `theme` field is invisible to
staging in any case.

**The spillway, the dry-grass foothill, the cattle and the agency building still need
commissioned plates.** `landscapes_timelapse` was always going to be thin here — three video
queries — and it was.

---

## 9. CORRECTION (2026-08-20 10:5x) — §3's "needs commissioned plates" was wrong

§3 lists four subjects that "must come from commissioned plates, i2v, or licensed news/agency
material", and §8 repeats it. **That work was already complete before this plan was written.**

`episode_spec.v002.json` declares `mandatory_stills` **O001–O118**;
`episodes/_planning/EP71_oroville_CODEX_BATCH_A.v001.md` specifies each by script anchor and
motif. **All 118 exist at `remotion/public/oroville/img/`, 3840×2160 PNG, 988 MB, no zero-byte
files.**

| §3 said unreachable | actually already a plate |
|---|---|
| **the spillway** | `O029` "a large plain concrete channel carrying water downhill, square on from above, engineering without drama"; `O030` wet weathered concrete with a cold joint; `O031` water leaving a rectangular opening; `O032` a low concrete weir crest with dry ground below it |
| Butte County dry-grass foothill | `O006` "low brown foothills on the far horizon"; `O033` a bare brown hillside with a fresh erosion gully; `O021` valley floor with low foothills far off |
| cattle on a valley floor | `O021` orchard rows, irrigation channel, levee bank, two-lane road |
| an agency building exterior | `O041` the advocate's desk; `O047` a county fairground gate and low painted hall |

**§3 remains true in its narrow sense** — the stock shelf cannot supply these — **but nothing
needs commissioning.** The outstanding work is the human verdict pass on the 92 contact sheets
and the i2v that gives the plates motion.

Note also: this plan was measured against `episode_spec.v001.json`. **`v002` supersedes it**
(2026-08-12) and differs only in the people-plate count, which v002 lowers by one to **19**;
`forbidden_subjects`,
`distinct_video_assets` and `target_cut_sec` are identical, so every count here stands.

---

## 10. The pool that actually exists (2026-08-21) — v002 query set, staged

The v001 set in §4 was read on contact sheets and **failed at 5 %** (`runs/qc/oroville_footage_review.v001.md`).
It was replaced, re-measured, re-sheeted and read again in full. **All 40 sheets were opened.**

```
query terms            101 -> 36
candidates             534 -> 174
dropped mechanically   258 ->  62
presented for verdict  276 -> 112
ACCEPTED                 3 ->  38   (5 % -> 34 %)
staged                            38   pool now 38 clip(s), binding=exact
cross-episode byte duplicates      0   against 10,204 clips in 44 other episodes
```

### The rule that produced the change

**Tight framing travels. A wide shot carries its place with it.**

A water surface, a raindrop on glass, a cloudscape and an anonymous hand are the same object
anywhere on earth. A hillside, a road, a building and an animal are not — and every one of the
v001 registers that failed was asking for one of those from a global stock shelf. `animal` was
never going to return a Butte County cow; it returned a snail, an owl, a labrador and a cartoon
dog. That is not a bad query. It is the wrong thing to ask a shelf for.

### What the 38 are

| register | n | what they are |
|---|---:|---|
| rain on glass / window | 11 | the film's own February. Place-neutral by construction |
| sky, cloud, storm | 8 | storm cloud, rain curtain over a ridge, layered dusk, red cloud bank |
| river, creek, water surface | 9 | water over gravel, wet pebbles, a winter-woods stream, a dry rocky sluice |
| fog | 3 | fog in trees, a misty pond at dawn, a misted field |
| hands, legs | 4 | legs walking on black, a hand writing in a notebook, hands on a phone |
| other | 3 | a night road under one blue lamp, a storm-lit hill, rain falling on grass |

### What this pool is FOR — read this before cutting

**38 clips is not this film's footage. It is its connective tissue.** The contract asks for 260
distinct video assets and the plates supply the film: `O001`–`O118`, all 4K, verdicts accept
118 / reject 0. The spillway is `O029`–`O032`, the foothills `O006`/`O033`, the valley floor
`O021`/`O022`. Those are the film. **These 38 go between them** — a cutaway to rain on glass, a
sky to sit under a date card, a water surface behind a quote.

### Still true, still not fixed

- **No cattle, no foothill, no agency building, no spillway comes from the shelf.** §3 and §9
  stand: they are plates, and they exist.
- The staging receipt records who looked. It does not certify the pool is clean. One reviewer,
  one pass, contact sheets — the full-size frames behind each `look_closer` were not opened.
- `handshake` is a `forbidden_subject` for this episode and a clip titled "shaking hands" walked
  straight through the screen, because the filter matches the word and not the stem. Worth
  fixing before it matters somewhere it does.
