# EP60 · CHAMPLAIN TOWERS SOUTH — FOOTAGE REVIEW v001

**Started 2026-08-02, while EP60 waits on Codex batch D.** This is the eyeball pass that
`ASSET_DESIGN.v002 §2.4 rule 3` requires: *never select a factory clip by filename.* Every
row below was looked at as a rendered frame on a labelled contact sheet, not read off a
path. Sheets live in `runs/qc/shot_<motif>_footage_contact_NN.png`.

Purpose: turn the ~330 archive cuts the film needs from a count into named files.

---

## 0. A tool gap found and closed first

`search_archive.py --sheet` only fired when `--shot` was passed — the **phrase-search** path.
That is the path `ASSET_DESIGN §2` measures as badly undercounting (`--shot "underground
parking garage"` → 3 hits where plain `garage` → 45). So the only selection you could
actually look at was the one the design tells you not to select from, and the keyword path
that carries the real counts had no way to be reviewed at all.

`--sheet` now works on keyword results too. Everything below was produced through it.

---

## 1. MEASURED: how often the filename lies

**Motif `garage`, 24 clips reviewed, 100% of the pool at limit 24.**

Twenty-three of the twenty-four are named `AF-BG-NNNNN__empty_parking_garage.mp4`. That is
the **new** naming convention — the one that looks descriptive. What the frames actually show:

| Verdict | n | What they are |
|---|---|---|
| **Usable for EP60** | **7** | dark or plain concrete decks, columns, no people |
| Wrong tone, right subject | 7 | bright white malls, green/blue floors, commercial signage colour |
| **Has people doing something** | 6 | skateboarders (×3), a man removing a hoodie, a couple at a car door, a go-kart |
| **Not a garage at all** | **4** | municipal trucks in a workshop · an outdoor flea market from above · **icicles** · an autumn street |

**Filename accuracy: 20/24 are a garage of some kind, 7/24 are the garage this film needs.**
Four files named `empty_parking_garage` contain no garage whatsoever, and one of them is a
close-up of icicles.

This is the `pd-factory-shelf-mislabeled` failure, reproduced with numbers on the *new*
intake. `ASSET_DESIGN v002 §2.4` warned that `AF-BG-NNNNN__descriptive_name` is still
query-derived; that warning is now quantified. **Plan the footage layer at roughly a 30%
hit rate**, not at the raw hit counts.

### 1.1 Picks — `garage` (EP60's under-the-pool-deck register)

| # | File | Why |
|---|---|---|
| 1 | `AF-BG-2207__warehouse_interior_dark.mp4` | darkest in the pool; long columned bay receding into black. Reads as *under* something |
| 2 | `AF-BG-21499__empty_parking_garage.mp4` | low deck, dark red columns, wet-looking floor, empty |
| 4 | `AF-BG-21501__empty_parking_garage.mp4` | symmetrical column rows straight down the axis — the punching-shear register |
| 17 | `AF-BG-21514__empty_parking_garage.mp4` | dark, ceiling strip-lights receding, no people. Strongest single clip |
| 19 | `AF-BG-21516__empty_parking_garage.mp4` | plain concrete bay, a few parked cars, neutral grade |
| 20 | `AF-BG-21517__empty_parking_garage.mp4` | warm, grimy, older stock — closest to a 1981 building |
| 7 | `AF-BG-21504__empty_parking_garage.mp4` | reserve. One parked car, arrow on the deck; usable if graded down |

Six firm plus one reserve. The design asks for ~8–10 garage cuts across ACT I and ACT V, so
this motif is **short** and needs a second pass at a higher limit before it is settled.

### 1.2 Rejects — do not stage these

`AF-BG-21500` (white mall) · `AF-BG-21503` (blank wall, out of focus) · `AF-BG-21505` (green
floor) · `AF-BG-21507` (purple light, woman walking) · `AF-BG-21508`, `AF-BG-21509` (blank
walls) · `AF-BG-21510`, `AF-BG-21513`, `AF-BG-21516`… skateboarders · `AF-BG-21511` (car
door, couple) · `AF-BG-21512` (go-kart) · `AF-BG-21515` (blue commercial) · `AF-BG-21518`
(truck workshop) · `AF-BG-21519` (flea market) · `AF-BG-21520` (**icicles**) · `AF-BG-21521`
(autumn street).

---

## 2. REVIEWED — `meeting` (ACT II, the film's only scene)

**24 clips reviewed. This motif does not work, and the reason is not quality.**

ACT II contains the November 2018 board meeting — the one moment in 35 minutes where the film
is in a room with people making a decision. What the shelf holds under `meeting` is glossy
corporate stock: glass boardrooms with skyline views, suits, handshakes, chart presentations.
A condominium association meeting is older people in an ordinary community room.

But the disqualifier is simpler and absolute: **almost every clip puts an identifiable face in
sharp focus, centre frame.** EP60's policy is no identifiable faces. That rules out roughly
19 of 24 on tone-independent grounds.

Usable, and only as texture around the scene rather than as the scene:

| # | File | Use |
|---|---|---|
| 12 | `AF-LIGHT-1470__projector_beam_dust.mp4` | a projector beam in dust, no people. The register of a room where something is being shown |
| 17 | `AF-BG-32679__boardroom_table_dark.mp4` | over-shoulder, hands and paper, heads cut off. Faces unreadable |
| 14 | `AF-BG-29692__office_interior_dark.mp4` | one small figure at a desk in a dark office, back to camera |
| 11 | `AF-BG-15464__empty_boardroom_at_night.mp4` | needs checking in motion — the sampled frame shows a person although the filename says empty |

**Conclusion: the board-meeting scene cannot be carried by archive footage.** It has to be
built. Codex **batch D §4.2 already covers it** (`S127`–`S150`, "第2幕 — 技師の一日、報告書、
そしてあの部屋"), so the design anticipated this correctly and nothing needs redesigning —
but it does mean **batch D is not optional**. Without it there is no scene.

Mislabels seen again: `jury_box_empty.mp4` (×2) shows a conference room, and
`empty_boardroom_at_night.mp4` shows an occupied meeting.

---

## 3. REVIEWED — `coastline` (the ending image)

**24 clips reviewed. ~20% usable — the worst hit rate so far, and the design predicted it.**

`ASSET_DESIGN v002 §2.2` says the 450 coastline clips are "rocky northern / Mediterranean, not
flat sand + turquoise". Confirmed: Portuguese cliffs, Devon cliffs, Japanese headlands, an oil
refinery, factory smokestacks. Surfside is a flat Atlantic barrier island.

| # | File | Why it survives |
|---|---|---|
| 4 | `AF-BG-2669__lone_person_silhouette_walking.mp4` | misty flat beach, one distant silhouette. Flat, muted, no cliff — and the figure is unidentifiable, which the policy needs |
| 12 | `pixabay_extra__v_14297__sand-nature-coast-se.mp4` | aerial straight down on flat sand and the surf line. The closest thing on the shelf to Surfside geography |
| 8 | `AF-PART-5862__sea_foam_spray.mp4` | pale foam close-up. Neutral, grades anywhere |
| 10 | `mixkit__31746__foamy-wav...ing-with-a-coastline.mp4` | warm low sun over open water — a candidate for the final image |

Rejected: everything with a cliff (7 clips), the oil refinery and smokestacks (2), boats,
a purple-graded sky with birds, a crowded resort aerial, and one clip that is **vertical
video letterboxed into 16:9** (`pixabay_extra__v_281640`) — unusable in a 1920×1080 film and
not detectable from its filename.

**`coastline` is the wrong query for this film.** Re-running as `beach` / `sand` / `shoreline`.

---

## 3b. REVIEWED — `beach` (the corrective query, and it works)

**24 clips reviewed. ~50% usable, against `coastline`'s ~20% on the same shelf.**

Same archive, same limit, one different word. `coastline` returns geology — cliffs, headlands,
rock. `beach` returns the thing this film is about: flat wet sand, grey Atlantic weather, one
small figure a long way off. **Use `beach` as the primary query and retire `coastline`.**

| # | File | Use |
|---|---|---|
| 13 | `AF-BG-31282__lone_person_silhouette_walking.mp4` | foggy pebble beach, a pier, one small solitary figure. Muted and mournful without being maudlin. **Best clip found so far in any motif** |
| 3 | `coverr__9808__sunrise-at-the-beach-dock.mp4` | grey-gold sunrise past a pier silhouette. Candidate for the final image |
| 12 | `AF-BG-31276__lone_person_silhouette_walking.mp4` | dark flat beach at dusk, wide, restrained |
| 4 | `AF-BG-2666__lone_person_silhouette_walking.mp4` | flat wet sand mirroring a low sun. Reads Atlantic, not Mediterranean |
| 9 | `AF-BG-27942__stormy_ocean_waves_dark.mp4` | coastal city beach under heavy cloud. Cold, ordinary, unglamorous |
| 8 | `AF-BG-27924__stormy_ocean_waves_dark.mp4` | dark teal water from above. The early-act register |
| 15 | `AF-BG-40767__stormy_ocean_waves_dark.mp4` | grey surf breaking on sand |
| 10 | `AF-LIGHT-2596__soft_golden_light.mp4` | warm backlit surf, shallow. Transition material |
| 17 | `AF-VFX-3767__mist_atmosphere.mp4` | pale mist over water. Transition material |
| 6 | `AF-LIGHT-1952__caustics_water_light.mp4` | sunlight through shallow water. Abstract; pairs with the pool register |

**Held back deliberately:** `AF-BG-46772__empty_chair_in_spotlight_grief.mp4` — a single empty
chair on a beach at sunrise. It is beautiful and it is *too* legible. `footage_diversity` caps
generic symbols at 2 across the film, and an empty chair captioned *grief* spends that budget
on the nose. Keep as a reserve for the ending only if nothing better exists.

Rejected: Portuguese cliffs (2), desert dunes (2), a yellow tour bus at Pattaya, a lighthouse,
a tropical resort aerial, a pink-graded stylised silhouette, and **an hourglass** — the exact
generic-symbol class the diversity gate exists to keep out.

Note: four different clips share the name `lone_person_silhouette_walking.mp4` and they are
genuinely four different beaches. That naming family is unusually reliable.

---

## 3c. REVIEWED — `documents` (ACT II's paper trail) — REJECT THE WHOLE QUERY

**24 clips reviewed. 22 of them are already in a previous episode. Do not use this query.**

Two independent problems, either of which is fatal:

1. **Cross-episode burn: 22/24.** `AF-BG-1276__documents_on_desk.mp4` — the clip this pass
   picked as the best of the sheet before checking — is already in **seven** episodes
   (dbcooper, florence, forfeiture, onecoin, postoffice, thompson, unlock). Choosing it makes
   EP60 the eighth.
2. **Wrong register.** Nine of the 24 are `law_library_books.mp4` — mahogany shelves and
   leather spines. That is the Miranda/Gideon/Mapp look. EP60 has no law library in it. The
   rest is corporate contract-signing with faces in frame, a **divorce** form with readable
   text, pie charts, and an `ON AIR` broadcast studio.

EP60's paper is an engineer's report, an association budget, a warning letter, an envelope in
a tray. **Batch D already covers all four** (`S139`–`S143`, `S150`). The archive contributes
nothing here that is both new and right.

**Replacement queries to try instead of `documents`:** `binder`, `folder`, `envelope`,
`calculator`, `filing cabinet`, `ledger`. Measure the burn rate before eyeballing — it is the
cheaper filter and it killed this motif in one command.

---

## 3d. REVIEWED IN PARALLEL — five agents, ten motifs (2026-08-02)

Contact-sheet review is the slow step and it does not have to be serial. Five agents each
read 2-4 sheets against the same written criteria (no identifiable face, no readable text or
logos, no bright tropical colour, no collapse imagery, no vertical letterboxing, cold
grey-blue register) plus per-motif traps. 96 tiles, about two minutes.

**Anti-fabrication check, run on every returned row.** A previous verification pass on this
project fabricated ten findings with invented URLs, so nothing here is taken on trust: each
reported filename was matched against the live `search_archive.py` pool for that query.
**47 filenames checked, 47 real, 0 invented.**

One false alarm, and it was mine. Five `night street` names came back "not in pool" until I
noticed the sheet had been built with two keywords (`night` `street`) while my check passed
one (`"night street"`). Re-checked correctly: 6/6 real. **The measuring instrument was
wrong, not the agent.**

| Motif | usable | verdict |
|---|---|---|
| `dawn` | **13/24** | **ADOPT.** Foggy harbours, flat pale water, grey-gold bands. The closing register |
| `crane` | 6/24 | ADOPT, overcast silhouettes only. The other 18 are blue-sky commercial stock |
| `archive` | 5/24 | ADOPT with a caveat — all five survivors are the same card-catalogue drawer |
| `night_street` | 4/24 | Sparingly. Two or three 1:22 a.m. beats, no more |
| `balcony` | 2/5 | Too thin to be a register, and the building is the film's subject |
| `laboratory` | **3/24** | **REJECT** |
| `sunrise` | — | **REJECT — strictly worse than `dawn`** |
| `corridor` | 3/24 | **REJECT ENTIRELY** |

### What the parallel pass found that a count never would

**`laboratory` is the wrong word.** Twenty of 24 are school science glassware — coloured
liquids, pipettes, petri dishes, smiling lab models. What ACT V needs is NIST loading
full-scale column replicas until they broke. Retry as `compression press`, `concrete cylinder
test`, `load frame`, `strain gauge`, `specimen under load`.

**`corridor` is a prison.** Nineteen of 24 are `prison_corridor.mp4`. EP60 needs the inside
of somebody's home. Combined with a 19/24 cross-episode burn rate, dropping it costs nothing.

**`archive` correctly refused the law library.** The rejects are tagged `lawlibrary` — the
mahogany-and-leather look that belongs to the Miranda/Gideon episodes. But the five survivors
are one idea filmed five ways, so a second pull is needed (boxes, shelving, a plain room).

**`dawn` beats `sunrise` on the same shelf.** `sunrise` returns golden-hour flares, forests
and timelapse; `dawn` returns overcast flat water. Three clips appear in both pools —
`AF-BG-11098`, `AF-BG-21150`, `AF-BG-21162` — verified independently.

### Adopted so far

`beach` (10) · `dawn` (13) · `garage` (7) · `crane` (6) · `pool` (~5) · `archive` (5) ·
`night_street` (4) · `balcony` (2) = **roughly 52 named clips against a ~330-cut target.**
Still short by a factor of six. The next pulls are the ones the review named: concrete
testing, a residential corridor, a records room, and a second `archive` seam.

---

## 3e. THE DECISIVE PASS — four agents, twelve replacement motifs

Run after §3d named what was missing. 63 filenames returned across the whole parallel
programme, **63 verified real, 0 invented.**

### The finding that decides the asset budget

**`concrete` is not a concrete search.** All 24 hits are one filename family,
`AF-BG-NNNN__concrete_wall_texture_dark.mp4`, and the pixels are a motion-background pack:
herringbone tile, painted plaster, red brick, a hexagon render, neon fluid, a shadow-puppet
rabbit, a scythe gag, an aerial of the Great Wall, a skate floor. **Not one column, soffit,
construction joint, reinforcing bar, rust bleed or spall in the set.**

**`cement` matched on the string.** Eleven hits include a Capcom game trailer, a NASA
ScienceCasts episode titled *Cementing Our Place in Space*, and two cartoon policemen.

**`column` returned architecture, not structure.** 24 of 24 are `bank_building_columns` —
the New York Stock Exchange pediment, cathedral porticos, ancient ruins, falling banknotes.
An architectural column is not a structural column, and the word cannot tell them apart.

> **The punching-shear chain — column head, slab soffit, misplaced bar, chloride rust
> bleeding through, spalled cover — has ZERO archival coverage. Every one of those shots
> must be built.** This is the retroactive justification for the 179 AI stills and the
> reason batch A's 56 concrete images were never optional.

### The other three registers, measured

| Motif | usable | what the pool actually is |
|---|---|---|
| `hallway` | 3/24 | **19/24 are `school_hallway_empty`** — the same failure as `corridor`'s 19 prisons |
| `elevator` | 3/24 | 23/24 one family; mostly subway and airport escalators |
| `lobby` | 0/1 | the entire pool is **one** clip, a hospital waiting room |
| `staircase` | 0/5 | courthouse exteriors and an open-plan office |
| `filing` | 0/2 | two clips. One is **a farrier filing a horse's hoof** |
| `shelf` | 0/20 | 8 law library, 5 retail/domestic. Three files named `evidence_locker_shelves` are **ceramic tiles and dinner plates** |
| `facade` | 1/19 | 8 of 19 are glass towers; one usable balcony stack, and it reads as a 30-storey Asian slab |
| `housing` | 1/3 | pool is three clips |
| `cement` | 0/11 | see above |
| `column` | 0/24 | see above |
| `concrete` | 0/24 | see above |
| `rebar` | 0/1 | one sunny clip of a worker on new reinforcement — construction, not decay |

### Then the queries were wrong, not the shelf

Before sizing a batch E, the agents' proposed replacement terms were counted. The archive is
**not** empty; the words were:

| register | term | video hits |
|---|---|---|
| structure | `bridge` | **215** |
| structure | `abandoned` | **153** |
| structure | `ruin` / `rust` / `demolition` / `underpass` | 53 / 51 / 50 / **49** |
| residential | `door` | **416** |
| residential | `porch` / `entrance` / `stairs` | 31 / 30 / 28 |
| records | `stack` / `desk` / `typewriter` / `boxes` | **308** / 256 / 120 / **111** |
| building | `window` / `rooftop` / `block` | **473** / 89 / 64 |

`underpass` and `bridge` are the lead: a bridge underside is a real reinforced-concrete
soffit with real columns and real water staining, which is exactly what `concrete` failed to
supply. Sheets are building for all twelve.

**Do not size batch E until these are reviewed.** Guessing the number now would repeat the
mistake this whole pass exists to prevent.

---

## 4. WHAT THIS CHANGES ALREADY

1. **Budget the footage layer at a ~30% hit rate.** The film needs ~330 archive cuts, so the
   review pool has to be **roughly 1,000 clips**, not 330. At limit 24 per motif that is far
   too few passes; raise the limit per motif and expect to reject two thirds.
2. **`--limit 24` is a sampling window, not a shortlist.** For `garage` it covered half the
   47-clip pool and yielded six keepers.
3. **No clip enters `asset_manifest` without a row in this file.** That is the mechanism that
   stops the `evidence_bag`-returned-cartoons class of accident reaching a render.
4. **The motif word matters more than the count.** Measured on the same shelf at the same
   limit: `coastline` ~20% usable, `beach` ~50%. One word made the pool two and a half times
   better. Query for the thing, not the category — and **measure the hit rate of a query
   before trusting its count.**
5. **Add a vertical-video check to selection.** One clip in the coastline pool is portrait
   letterboxed into a 16:9 container; nothing in the filename or the ledger says so.
6. **Check the cross-episode burn rate BEFORE the eyeball pass.** `check_cross_episode_reuse.py
   --check-query <q>` costs one command and killed `documents` outright (22/24 burned) after
   the eyeball pass had already picked a clip from it. Measured burn: `documents` 22/24,
   `garage` 6/24, `beach` **3/24**. Cheap filter first, expensive filter second.
7. **Resolution and orientation are a third filter nobody was applying.** 30,113 clips
   scanned: **1,189 are portrait** and **7,048 are below 1920x1080**. Roughly 30% of the
   shelf cannot enter a 16:9 HD film at all, and no filename says so —
   `AF-BG-0074__dark_cinematic_background.mp4` is 720x1280.
8. **Contact-sheet review parallelises; the counting does not.** Five agents cleared ten
   motifs in the time one serial pass clears two. Every returned filename must still be
   matched against the live pool before it is believed.
9. **Verify the verifier.** The one apparent fabrication in this pass was a bug in the
   checking command, not in the agent. Reproduce the exact query form the artefact was
   built with before calling a result false.
10. **A zero result is a statement about the word, not the shelf.** `concrete` 0/24 and
    `filing` 0/2 looked like an empty archive. Re-queried as `bridge`, `underpass`,
    `abandoned`, `boxes`, `stack` the same shelf returns hundreds of rows. Always test a
    second vocabulary before concluding the material does not exist.
11. **One filename family = one search result.** `concrete` -> 24/24 `concrete_wall_texture_dark`,
    `column` -> 24/24 `bank_building_columns`, `elevator` -> 23/24 `elevator_interior_steel`,
    `hallway` -> 19/24 `school_hallway_empty`. When a query resolves to a single ingest
    family, it is retrieving that family's LABEL, not the concept. Check the family spread
    before reviewing the sheet.
12. **Batch D is load-bearing, not additive.** The only scene in the film cannot be shot from
   the archive, and batch D §4.2 is what covers it.
