# EP66 · THE OPEN-FIELDS DOCTRINE — ARCHIVE FOOTAGE PLAN v001

**Date 2026-08-10 · slug `openfields` · episode `PD-2026-066-openfields`**
**Script `EP66_openfields_script.en.v003.md` · contract `episodes/PD-2026-066-openfields/episode_spec.v001.json`**
**Queries live in `config/episode_footage_queries.v001.json` → `episodes.openfields` (275 of them, verbatim).**
**Verdicts in `runs/qc/openfields_clip_verdicts.v001.json` · sheets in `runs/qc/openfields_factory/` (17) and `runs/qc/openfields_facecheck/` (5).**

---

## 0. Result

```
staged      338 clips     remotion/public/openfields/factory/
accepted    203 clips     every one looked at on a labelled sheet
rejected    135 clips     each with its own written reason
floor        35 clips     one per 45 s of a ~26 min film (factory_used)
target       60 clips
```

**203 against a floor of 35 and a target of 60.** EP65 shipped seven and took an owner-approved
deviation on `factory_used` because "the shelf is thin". The shelf is not thin. EP65's queries were.

---

## 1. Which lanes were searched

`shelf_rows()` (`scripts/shelf.py`) — never a private glob — puts **151,869 items on the shelf, of
which 31,150 are video.** Every lane that holds video was searched:

| lane | video on shelf | rural-vocabulary title matches | staged | accepted |
|---|---:|---:|---:|---:|
| pexels | 9,398 | 1,545 | 193 | 135 |
| pixabay_extra | 10,262 | 4,035 | 102 | 57 |
| mixkit | 2,158 | 314 | 39 | 10 |
| ia | 1,422 | 18 | 2 | 1 |
| coverr | 68 | 7 | 1 | 0 |
| nara | 814 | 1 | 0 | 0 |
| nasa | 630 | 3 | 0 | 0 |
| noaa | 41 | 0 | 0 | 0 |
| **pixabay** | **6,357** | **0 — see §7** | **1** | **0** |
| freesound / wikimedia / loc / unsplash / smithsonian / met / oyez / courtlistener / sdxl | 0 video | — | — | — |
| **total** | **31,150** | **5,923** | **338** | **203** |

mixkit's low acceptance is almost entirely resolution: most of its library is 1280×720 (§6.1).

Reproduce the lane counts:

```bash
py -3.11 scripts/shelf.py
```

**Only one lane was not mined, and not because it was missed: `pixabay` cannot be queried at all.
See §7 — that is a tooling finding, with a measured cost.**

---

## 2. The queries that failed, and what fixed them

The rule from the 2026-08-09/10 shelf audit: *a query returning 0 is a fact about your wording,
not about the shelf.* It held again here. Every "0 hits" line below was rewritten in the vocabulary
suppliers actually use, and the rewrite is on the line under it.

| director's language | hits | supplier vocabulary | hits |
|---|---:|---|---:|
| `posted no trespassing sign boundary` | **0** | `fence with a sign` | 8 |
| `boundary sign posted on tree` | **0** | `no trespassing sign` | 1 |
| `flat overcast woodland light` | **0** | `forest in fog` | 16 |
| `wind in bare branches` | **0** | `tree branches swaying in the wind` | **71** |
| `old farmhouse in field` | **0** | `farmhouse seen from far off` | 17 |
| `rural pennsylvania hardwood ridge` | **0** | `autumn forest hillside` | 5 |
| `appalachian mountains forest` | **0** | `road through the woods` | 53 |
| `middle tennessee farmland` | **0** | `country road with trees` | 21 |
| `farmland at low sun` | **0** | `sunset over farmland` | 18 |
| `boots walking on mud` | **0** | `walking through tall grass` | 25 |
| `boot prints in mud` | **0** | `footprints in the mud` | 1 |
| `wooden fence post in field` | **0** | `barbed wire on wooden post` | 12 |
| `country lane trees` | **0** | `country road with trees` | 21 |
| `cornfield rows` / `corn field wind` | **0** | `grass moving in the wind` | **86** |
| `overgrown grass` | **0** | `tall grass field wind` | 21 |
| `gravel road` (title-AND) | **0** | `dirt road` | 19 |
| `muddy ground footprints` | **0** | `puddle in dirt road` | 16 |
| `fence post` (title-AND) | **0** | `barbed wire` | 15 |
| `picket fence` | **0** | `wire fence` | 13 |
| `farm gate` | **0** | `gate` | 51 |
| `wet grass` | **0** | `grass swaying in the wind` | 86 |
| `hay field` / `farmland field` (title-AND) | **0** | `wheat field` | 19 |
| `storm clouds field` (title-AND) | **0** | `overcast sky` | 21 |

Reproduce any row:

```bash
py -3.11 scripts/search_archive.py --shot "wind in bare branches" --kind video
py -3.11 scripts/search_archive.py --shot "tree branches swaying in the wind" --kind video
```

**The single biggest lever was dropping the adjectives.** "flat overcast woodland light" is how a
director talks. A supplier writes "eerie forest in dense fog mysterious atmosphere" and "misty
forest with tall trees in foggy atmosphere". Both are in the accepted list.

---

## 3. The staging query set

275 title-AND queries, written pass 1 (153) and pass 2 (122), all in
`config/episode_footage_queries.v001.json`. Staged with the project's own tool, twice:

```bash
py -3.11 scripts/stage_episode_footage.py --slug openfields --per-query 4    # pass 1 → 186
py -3.11 scripts/stage_episode_footage.py --slug openfields --per-query 3    # pass 2 → +152
```

Counts by register, measured by matching register words against the query strings and against the
suppliers' own titles. **A clip serves more than one register, so the columns sum past 275 and 338 —
these are coverage figures, not a partition.**

| register | queries | staged | accepted |
|---|---:|---:|---:|
| woodland, trunks, bark, canopy, sun through trees | 127 | 167 | 97 |
| fields, pasture, crops, grass, stubble | 76 | 98 | 60 |
| fog, mist, overcast, cloud, sky, storm | 63 | 79 | 49 |
| autumn and fallen leaves, forest floor | 47 | 56 | 36 |
| tracks, paths, lanes, walking figures | 45 | 61 | 25 |
| gates, fences, wire, boundary signage | 23 | 24 | **19** |
| rain on land, wet leaves, puddles | 22 | 26 | 13 |
| creeks, streams, ponds, rivers | 18 | 29 | 13 |
| buildings seen from far off | 6 | 7 | 3 |
| trail camera, cut branch, lens on a trunk | **0** | **0** | **0** |

The last row is zero queries because every phrasing I tried returned nothing usable — §5.2. The
gate row survives at 19 only because "fence" and "wire" carry it; gates and padlocks alone are four
clips, and that is §5.1.

---

## 4. What each register carries in the film

The film is 26 minutes of two men's land. The archive is not illustration here; it is the subject.
Register → the script line it serves → the clips.

### 4.1 The chained gate — ACT_1 motif states 1, 2, 4, 5, 7
> *"It is landlocked. He reaches it through his neighbour's private gravel drive and gate, then
> through a chained gate of his own, with a No Trespassing sign on it."*
> *"That gate is not the line."*

`AR-27732553` a rusty iron gate with a chain and lock · `AR-4169282` a rusty old steel gate ·
`AR-v_59670` gate, fence, enclosure, sky, clouds, outdoors (a wooden farm gate on a wire fence —
the best gate in the pool) · `AR-7029595` a creepy trail in gated property (a closed gate in fog).

### 4.2 The fence line and the posted boundary — ACT_1, ACT_4
> *"He has sixty-nine acres on Liberty Road, fenced all the way around, and accessible through a
> chained gate with No Trespassing signs."*
> *"They have posted their properties' boundary lines with clearly visible no trespassing signs and
> purple paint."*

`AR-27568805` a fence with a sign that says no trespassing · `AR-34967664` close up of rustic barbed
wire on wooden post · `AR-7895635` close up video of a barbed wire · `AR-6581406` close up shot of
barbed fence · `AR-11490316` close up view of barbed wire · `AR-3151466` a cut tree trunk used as
post for spiked wires fencing · `AR-35029175` close up of ants on rusty wire in nature ·
`AR-v_29637` barbed wire security metal barrier · `AR-v_135011` fence protection metal tip nature
country · `AR-v_101975` fence wood border cinematic limit · `AR-v_288440` fence field meadow wild
grass · `AR-v_62389` mountains trees field fence · `AR-v_18085` plastic fence pasture (torn sheeting
caught on a wire fence — the most eloquent boundary shot in the pool) · `AR-34783021` serene
countryside leaves in sunlight (fence rail, field beyond) · `AR-35551357` scenic sandy pathway
(post-and-rail alongside a track) · `AR-v_66433` mountain river creek fence barrier.

### 4.3 Ninety-three acres of open field — ACT_1 arithmetic, ACT_3 "wild or waste lands"
> *"On ninety-three acres, almost all of the ninety-three is outside the ring."*
> *"These were not wild or waste lands outside the shield of Article I, Section 7."*

`AR-14284224` clouds over single tree on grassland · `AR-33773292` / `AR-33019536` / `AR-34933189` /
`AR-29497669` / `AR-28799699` lone tree in field · `AR-34585026` / `AR-34870770` lone pine on
grassland · `AR-21577` large open field · `AR-6577022` a day in an open field · `AR-29990270`
dramatic cloud timelapse over open field · `AR-4070` green meadow · `AR-6487245` mist meadow ·
`AR-timelapseofpastureatsuns` pasture at sunset (4096×2304, Internet Archive) · `AR-v_93320` /
`AR-v_93323` ploughed and harvested, empty · `AR-v_91992` spikes field rural · `AR-v_152291` /
`AR-v_89549` field at last light · `AR-v_100257` mown strips and a silo — the mown-track register ·
`AR-11355346` / `AR-12914929` crops waving · `AR-30408296` barley · `AR-35199731` / `AR-37709831` /
`AR-6680114` wheat · `AR-11320908` / `AR-5786949` / `AR-35644197` / `AR-4073698` / `AR-4911544` /
`AR-6033454` / `AR-35796014` / `AR-8526726` grass and seedheads in wind · `AR-5866166` fallen leaves
on grass · `AR-v_42029` / `AR-v_77300` / `AR-v_135665` / `AR-v_136482` / `AR-v_136483` / `AR-v_94106`
reeds and flower meadow in wind.

### 4.4 The tree the camera went on — HOOK, ACT_1, ACT_4
> *"He walks out to a tree. He cuts a branch off it, and installs a camera on it."*
> *"Warden Gritzer even placed a trail camera on Punxsutawney's property."*

There is no trail-camera footage on this shelf (§5). What the archive carries is the tree:
`AR-4248046` close up of a tree trunk · `AR-6056823` close up of tree trunks · `AR-5292464` tree
bark · `AR-v_26691` deadwood · `AR-v_27113` dead tree stump, weathered · `AR-v_175912` tree roots ·
`AR-v_108140` a bare dead tree against a grim moving sky.

### 4.5 Woodland in flat overcast light — ACT_4 Clearfield County, the hard cut
> *"Appalachian hardwood, elevation, a different light, a different gate."*
> *"four thousand four hundred acres and eleven hundred acres of woodland"*

`AR-15086879` tall trees in the forest (bare, foggy, brown floor — the exact register) ·
`AR-37244865` misty landscape with fog and bare trees · `AR-32675101` misty forest with tall trees ·
`AR-34061737` eerie forest in dense fog · `AR-31808079` misty sunrise in a tranquil forest ·
`AR-35821946` sunlight filtering through misty forest trees · `AR-3615892` fog over the woods ·
`AR-13340258` fog over trees · `AR-28339` forest covered by mist · `AR-28335` sunrise from a large
forest on a cloudy day · `AR-v_253435` misty beech woodland · `AR-v_231773` sunlit beech woodland ·
`AR-v_82216` / `AR-v_3574` / `AR-v_120641` woodland · `AR-11265968` / `AR-14057076` / `AR-19975560` /
`AR-27065367` / `AR-31807993` / `AR-5624206` / `AR-856325` / `AR-857042` / `AR-6677775` sun through
trees · `AR-7645660` / `AR-v_29713` / `AR-v_29715` forest floor, moss, leaf litter · `AR-50544`
fallen trees in a pond.

### 4.6 The tracks he stopped walking — ACT_1
> *"he has reduced his visits to his land, where he previously more regularly camped and fished."*
> *"Two men who go to their own ground less than they used to."*

`AR-v_141149` a gravel twin-track farm lane through woodland · `AR-31808103` misty forest pathway ·
`AR-35830059` a track vanishing into fog across a field · `AR-7029584` a tree-lined avenue in fog ·
`AR-v_62385` a sandy path through misty pine woodland · `AR-v_19731` / `AR-v_49063` / `AR-v_98661` /
`AR-v_98083` paths and boardwalks · `AR-26081666` a road in the middle of a forest · `AR-18761163` a
foggy road in the woods · `AR-v_189967` leaves on a windy track.

Figures on the land, all back-to-camera or below the head — §6.3:
`AR-18089238` a person walking down a dirt road at sunrise · `AR-31638607` solitary walk through a
forest path · `AR-32622` legs and boots on a woodland path · `AR-13853773` a man in a black coat in
mist · `AR-38146211` a solitary figure under a tree · `AR-v_212474` / `AR-v_212476` / `AR-v_220348`
a man walking away through woodland · `AR-v_43637` a rubber boot in a puddle.

Working the land, no faces: `AR-10041357` farmer walking over field · `AR-10041394` farmer in hat
pulling weeds · `AR-16585594` cutting grass · `AR-34841996` farmer at work · `AR-4683883` hands and
a sickle in crop · `AR-v_45657` hands holding grain.

### 4.7 Rain on land — ACT_2 motif state 3, the 5-second held silence
> *"motif state 3: rain. The padlock wet, the chain wet, the track empty."*

`AR-14213653` / `AR-14213657` heavy rain on green trees · `AR-4828773` heavy downpour ·
`AR-27219313` raining · `AR-33791047` leaves in rainfall · `AR-28036566` colorful leaves with rain ·
`AR-34568951` sunlit leaves in a rainy forest · `AR-18311` a leaf wet from the rain · `AR-4405573`
rain clouds over the forest · `AR-v_152801` rain on the ground · `AR-1254570` a tree in wind and
rain.

### 4.8 Weather over the land — the four silences, the reset beats
`AR-12373316` / `AR-6350030` / `AR-33739938` overcast · `AR-4312865` / `AR-4317605` / `AR-4377446` /
`AR-5761035` moving cloud · `AR-4557248` grayscale landscape under cloudy sky · `AR-18499673`
sunrays through cloud · `AR-51108` cloud over tree branches, low view · `AR-v_291622` thunderclouds ·
`AR-v_224739` cloud fields over a hill · `AR-v_16135` stormy spring landscape · `AR-30449776` moody
foggy hillside at dusk · `AR-10632772` fog over a barren hill · `AR-17868275` sunrise over a valley
with fog · `AR-29419147` / `AR-38214440` / `AR-v_52161` / `AR-v_30032` / `AR-v_20406` / `AR-44648` /
`AR-4804583` / `AR-v_203920` mist on hills and meadow · `AR-50936` a slow white mist ·
`AR-33535611` mist over heath at sunrise.

### 4.9 A farmhouse seen from far off — HOOK, ACT_4
`AR-1996373` a house in the middle of the woods (a lit window through trees, distance held).
This register is thin: one clip. See §5.

---

## 5. Where the shelf really is thin — with the evidence

Two registers, and I only say so after writing them in supplier vocabulary and looking at a
`--weak-ok --sheet` result with my eyes.

### 5.1 The chained gate and padlock — 4 accepted clips

The film's central object. Twenty supplier-vocabulary phrasings:

```
farm entrance gate          1     cattle grid                 0     paddock                 0
corral fence                0     ranch gate                  0     wooden barrier across   0
chain across road           0     locked padlock chain        3     metal latch             0
gate hinge                  0     livestock enclosure fence   0     boundary marker post    0
property line fence         0     private property sign       0     keep out sign           1
posted sign on post         1     gate fence enclosure        0     iron gate security      4
fence barrier metal country 0     old stone wall field       11
```

Then the check the canon demands before recording an absence:

```bash
py -3.11 scripts/search_archive.py --shot "closed farm gate chain padlock" \
    --kind video --weak-ok --limit 25 --sheet
```

I read both sheets (`runs/qc/shot_closed_farm_gate_chain_padlock_footage_contact_0{1,2}.png`).
Twenty-five candidates: two correct farm gates, three rusty gate close-ups, and then love-locks on
the Golden Gate Bridge, padlocks on a tourist railing, a locker, a ship's chain, a prison door, a
construction sign, and a cop unlocking a cell. **The register is genuinely about six items deep.**

And it is worse than six, because of cross-episode dedup. The two best clips on the whole shelf for
this film —

```
pexels 3999371  "a closed gate with a chain and a padlock"  -> robosigning/factory
pexels 3999356  "a closed rusty gate with padlock"          -> robosigning/factory_rejected
pexels 4976926  "a padlock in a wire fence"                 -> robosigning/factory_rejected
```

— are locked away. `stage_footage_by_title` excludes every id already in any `factory*` folder, and
that deliberately includes `factory_rejected`, so a clip one episode threw out stays dead for all of
them. Two of these three were rejected *for robosigning*, a mortgage-fraud film, where a rusty farm
gate is obviously wrong. For EP66 they are the single most on-subject images in the archive.
**This is an owner call, not mine.** If the rule is relaxed for these three ids, EP66's weakest
register roughly doubles.

Mitigation as staged: the gate motif in the script (states 1–7) is a **generated** plate series
(`L001`–`L065`), not archive. The archive carries the fence line either side of it, which is 16
accepted clips, and that is healthy.

### 5.2 The trail camera on a trunk — 0 clips

```
trail camera on a tree              0     camera strapped to a trunk    0
cutting a branch with a knife       0     pruning a branch              0     axe cutting wood  0
security camera on a pole outdoors  6     surveillance camera outdoor   4
```

The six and the four are not usable: "police officer monitoring security camera" (forbidden
subject: police), "woman covering a security camera" (a face), "close up of security camera and
smoke" (exactly the surveillance-thriller styling `episode_spec` forbids), and four photographers
holding cameras. **The trail camera has to be generated**, which is what the script already assumes
— the film's title image is the cut branch, the housing and the lens, and those are `L`-plates.

---

## 6. What was rejected, and why

135 clips, each with its own line in `runs/qc/openfields_clip_verdicts.v001.json`.

| reason | n |
|---|---:|
| resolution — below 1920 wide, or vertical | 49 |
| wrong register — town, car, paved highway, tropical, identifiably foreign, unreadable frame | 47 |
| aerial / drone — a `forbidden_subjects` entry | 18 |
| wrong season — snow, frost, ice | 9 |
| a second take of a clip already accepted | 6 |
| AI-looking illustration or composited, not photography | 4 |
| a recognisable face, or identity that could not be cleared | 2 |

### 6.1 Resolution — the check no staging tool performs

`stage_footage_by_title` has no resolution filter, and `check_final_acceptance` measures only the
**finished** file at ≥1920×1080 (PD_CANON §10: *"a film that stretches 640×480 across a 1080p
timeline passes the gate"*). So resolution was measured here, per clip, against
`_ledger/video_resolution.json`, and 49 clips were rejected on it — one 854×480 (an Internet Archive
home movie), 38 at 1280×720 or 1366×720, nine vertical 1080×1920, one with no entry at all.

Several were painful: `AR-23342` (a group of boots on a dirt road, no faces — the exact HOOK image)
and `AR-17791081` (a frosty misty meadow) are both 1280×720. They are correct pictures at the wrong
resolution and the film is better without them than with a soft insert.

### 6.2 Aerial

`drone` is in `episode_spec.v001.json` `forbidden_subjects`, so 18 clips went, including some good
land: vineyard rows from above, motorway interchanges over Drenthe farmland, a hairpin mountain
road, a top-down field edge. Several announce it in the supplier's own tag list
(`road, path, trees, forest, aerial, flying, nature, drone`); the rest were caught by eye.

### 6.3 Faces — the EP65 failure mode, checked properly

Two clips rejected outright: `AR-14620` (a person walking toward camera with the face resolvable)
and `AR-000419_202005` (a 1960s Prelinger family home movie — faces throughout, plus a burned-in
archive title card).

Then, because **one frame at t=1s is what let EP65 through**, every accepted clip whose supplier
title names a human was sampled at 10 / 35 / 60 / 88 % of its duration and the 92 frames were tiled
and read: `runs/qc/openfields_facecheck/openfields_face_check_footage_contact_0{1..5}.png`.
**23 clips, 92 frames, no recognisable face at any sample point** — every figure is back-to-camera,
below the head, at distance, or in silhouette.

The same treatment went to the four accepted clips whose `pixabay_extra` tag list names an animal
(`v_130880` deer, `v_231773` deer, `v_253435` bird, `AR-5900287` bird): five frames each,
`runs/qc/openfields_wildlife/`. No animal is visible in the three woodland clips; `AR-5900287` is a
bird in silhouette on a branch. `episode_spec` forbids hunting-kill imagery and none of these carry
it — this is a property-rights film, and a hunting club is the plaintiff, so the register has to
stay on gates, tracks, cameras and boundaries.

### 6.6 Licences on the accepted 203

`free_commercial` 202, `cc0` 1. No `review_required` row reached the pool: `stage_footage_by_title`
admits only `{free_commercial, pd, cc0}`, and its YouTube-rip signature check refused several
archive.org uploads during staging on the grounds that a CC0 tag there is the uploader's word.

### 6.4 AI-generated material

Four clips are illustration, not photography: two painted "rain creek forest" plates and two
Christmas-cottage renders, all from `pixabay_extra`, none self-declared as AI. The shelf's
ban-risk quarantine catches only self-declared AI (`PD_ARCHIVE_SHELF_WORKLOG` §12), so these were
caught by eye. Two more turned up in the pixabay blind probe (§7). **They are still on the shelf and
still discoverable by other episodes.**

### 6.5 The `unusable` verdicts — read, and deliberately not applied as a per-clip rule

104 of the 338 sit on a `(theme, source)` pair `archive_verdicts.jsonl` marks `unusable`. Their own
notes say what that verdict means:

```
courtroom_justice/mixkit    "walking and library dominate: 9 tiles of people walking ... 8 of
                             general (not law) libraries"
prison_jail/pixabay_extra   "a laid dinner table, a neon heart, a mussel dish ... roughly 6 of 24
                             usable"
courtroom_justice/pixabay_extra  "bench collides with PARK BENCH - 11 of 24 tiles are park benches"
nature_landscape/pexels     "one item, and it is people rallying in the street - filed under nature"
```

These say the **bucket is a bad place to shop for that theme**. They are not per-clip quality
judgements — and the clips misfiled into `prison_jail` and `courtroom_justice` (fences, pasture,
boots in a puddle, ploughed fields) are precisely what this episode needs. The last row is also
demonstrably a one-tile sample: `nature_landscape/pexels` holds hundreds of rows, not one.

PD_CANON §10's warning — *don't select from an unusable theme×source* — protects blind, theme-based
selection. Nothing here was theme-selected: every clip was chosen on the supplier's own written
title and then looked at, frame by frame, on a labelled sheet, and 23 of them frame-sampled again
for faces. Recorded in the verdicts file so the next reader sees the reasoning rather than a silent
override.

---

## 7. The pixabay lane cannot be queried — 6,357 videos, ~20 % of shelf video

Every row in the `pixabay` lane has:

```json
{"title": "id", "matched_keywords": [], "title_provenance": "source_url_slug",
 "file_path": "H:\\pd-media\\assets\\factory\\backgrounds\\pixabay__28860__id.mp4"}
```

Pixabay's URL for an untitled video is `/videos/id-28860/`, so the slug-derived title is the literal
string `"id"` — for all 6,357. Consequences, both verified:

* `stage_footage_by_title` matches on title only. `"id"` matches nothing meaningful, and as a query
  term it is a substring of `bridge`, `midday`, `wide`… so it cannot be used.
* `stage_footage_from_allowlist` resolves clips by filename against
  `^(AF-[A-Z]+-\d+)__(.+)\.(mp4|mov|webm|mkv)$`. The 2026-08-10 factory rename replaced
  `AF-BG-0070__dark_cinematic_background.mp4` with `pixabay__28860__id.mp4`, so that regex no longer
  matches **any renamed factory clip**. Neither staging tool can reach this lane.
* `search_archive --shot` cannot rank it either: title, id and filename are all `"id"`, and
  `matched_keywords` is empty. Only the folder-derived `theme` remains, and
  `theme_source: subtype_unverified` says that theme is a guess.

**So I measured what is being lost.** 703 pixabay videos pass the quality filters (≥1900 wide,
landscape, on disk) under the three themes that could plausibly hold land. I sheeted the first 60
blind and read all three sheets (`runs/qc/openfields_pixabay_probe/`):

```
sheet 1   6 / 20 usable   misty conifer woodland, fog over a bare ridge, sun through woodland,
                          autumn woodland floor, cloud over land
sheet 2   5 / 20 usable   mist over a pond in pine woodland, fog over a meadow, fallen leaves on a
                          trunk, bare trees and fog at dawn, mist over a fence line
sheet 3   1 / 20 usable   (flower macros on studio backgrounds, ocean, tropical, and two obvious
                          AI-generated illustrations)
------------------------------------------------------------------
         12 / 60 = 20 %   → roughly 140 usable clips in the 703, unreachable by any tool
```

Two of the three sheets contain material better than several clips I accepted. **This is a real
reserve and a real tooling gap, and it is not mine to fix behind the owner's back** — the fix is
either an `--id` flag on `stage_footage_by_title` or restoring `AF-` ids to the allowlist matcher.
Raised here rather than worked around.

---

## 8. Reproduce

```bash
py -3.11 scripts/shelf.py                                              # lane counts
py -3.11 scripts/search_archive.py --shot "<shot>" --kind video --weak-ok --sheet
py -3.11 scripts/stage_episode_footage.py --slug openfields --per-query 4
py -3.11 scripts/build_footage_contact_sheet.py \
    --dir remotion/public/openfields/factory --media video \
    --out-dir runs/qc/openfields_factory                               # 17 sheets
py -3.11 scripts/write_factory_clip_qc.py --slug openfields            # 338 recorded
```

Outputs:

```
remotion/public/openfields/factory/                    338 clips
runs/qc/openfields_clip_verdicts.v001.json             135 rejections, each with a reason
runs/qc/openfields_title_staging.v001.json             338 receipt rows (title, source, licence)
runs/qc/openfields_factory/*.png                       17 pool sheets, all read
runs/qc/openfields_facecheck/*.png                     5 face-check sheets, 92 frames, all read
runs/qc/openfields_wildlife/*.png                      1 animal-check sheet, 20 frames, read
runs/qc/openfields_pixabay_probe/*.png                 3 blind-probe sheets of the unqueryable lane
runs/qc/shot_closed_farm_gate_chain_padlock_*.png      2 weak-ok sheets behind the §5.1 shortage
episodes/PD-2026-066-openfields/05_visuals/factory_clip_qc.v001.json
                                                       338 clips, 203 accept / 135 reject
```

## 9. Open items for the owner

1. **Three padlock clips locked to `robosigning`** (two of them in its `factory_rejected`). §5.1.
   Releasing them for EP66 would roughly double this film's weakest register.
2. **The pixabay lane is unreachable by both staging tools.** §7. ~140 usable clips measured.
3. **Four AI-generated clips found by eye in `pixabay_extra`**, none self-declared, still live on
   the shelf for other episodes: `v_162017`, `v_167689`, `v_245390`, `v_245391`, plus `pixabay`
   `270445` and `267661` from the blind probe.
