# EP60 · CHAMPLAIN TOWERS SOUTH — ASSET DESIGN v002

**40 minutes · footage-first · owner directives 2026-07-31.** **v002 (2026-08-02): §2 re-measured against the grown ledger.** v001's supply table was taken while four ingest lanes were still writing; the owner has since downloaded more and asked whether any of it serves EP60. It was re-measured today and §2 below is the current truth. v001 stays readable as the record of what was believed on 2026-07-31. **Nothing outside §0 and §2 changed** — the layer split, the still count and the AE/Blender plan all survive the re-measure, and §2.0 says why. Companion to `TOPIC_PIPELINE.v005.md` (the pick) and `EP60_surfside_FACTS_LEDGER.v001.md` (what may be said). This file decides **what every frame is made of**, and it is written against measurements taken today, not against the previous episodes' assumptions.

**The three owner directives this file implements**
1. Build the film out of the **real footage now being downloaded**, not out of AI stills.
2. Use **After Effects abundantly**.
3. **One prompt = one image.** No variant pools, no "generate several and pick".

---

## 0. WHAT THE MEASUREMENTS CHANGED

Three parallel measurement passes ran before any of this was designed. Each one overturned something.

| Measured | Finding | Consequence for EP60 |
|---|---|---|
| **AE capability** | The AE hero-card pipeline works mechanically (EP50 rendered 36/36 cards and composited them twice, cleanly). **It was then deliberately dropped**: the composited cut measured **6.0s of pure black at 132.5s** and **132.9s of frozen frames** across 36 full-frame 5–7s title cards, which trips `images_present` (blackdetect) and `animation_density` (freezedetect). **No episode since EP50 has used AE at all**, and the AE builder/compositor scripts named in the EP51–59 planning docs **do not exist on disk**. | AE is used, but **never as a full-frame card composited on top**. See §4. |
| **Image pipeline** | Every planning doc says "1シーン1枚・バリエーション0". `generate_sdxl_4k.py` defaulted to **3 variants for every episode except EP56**. Disk agrees with the code: flowers wrote **628 images against a 257-image spec**, 355 into eight `rejected/` batches. Worse: **stills `S101`–`S210` appear in ZERO cuts in every built film** — about half the body-still budget is generated and never placed. Delivered films are **~370 cuts, not the specified 563**. | Generator fixed (default 1, >1 refused). Spec is now **cut-count-driven**: we specify only images that will be placed. See §3. |
| **Archive supply** | The new ingest is **not** where it was assumed. `H:\pd-media\assets\archive` holds 1,368 rows; the bulk is on **D:, E: and F: under `<drive>:\pd-archive\`** — live ledger total **171,597 rows**. **Four ingest lanes are still writing.** `ARCHIVE_SHELF_INVENTORY.v001.md` is stale by ~29,000 rows. **40.3% of factory video (6,322 rows) has no real title** — `"title": "id"` — so its only descriptor is the download-query filename, the known ~50%-wrong label. | Footage-first is viable for atmosphere and **not** for this story's specific objects. See §2. |
| **Archive supply, re-measured 2026-08-02** | Ledger grew **171,597 → 188,268 rows**. Every atmosphere motif got materially deeper (courtroom 144→**871**, coastline 130→**450**, tower/skyscraper 8→**176**, construction 127→**219**, domestic interiors 13→**37**, plus a **638**-clip laboratory shelf that had never been measured). **Every case-specific term is still at or near zero**: `rebar` 1, `corrosion` 0, `spalling` 0, `reinforced concrete` 0, `pool deck` 0, `condominium` 1, `surfside` 0, `champlain` 0. | The footage layer is now comfortably supplied — §1's 63% archive share is safe and no longer tight. **The AI-still allocation is unchanged**: the 56 Batch-A images exist precisely because the shelf cannot supply this film's physical subject, and after 16,671 more rows it still cannot. |

---

## 1. TARGET SHAPE

Measured cut density of the built 30-minute films: norfolk 364 cuts / 27.9 min, burge 380 / 29.2, postoffice 384 / 29.4 = **13.0 cuts per minute**. Holding that density:

| | value |
|---|---|
| Runtime | **40:00** |
| Narration | ~36:00 · **6,150–6,350 words** at the measured ~173 wpm |
| Total cuts | **~520** |
| Figure beats (Remotion motionkit) | **110–130** (EP50 shipped 165 over 61 min) |

### Layer split — and why it differs from EP53–59

| Layer | EP53–56 as built | **EP60 target** | cuts |
|---|---|---|---|
| Archive / real footage | 48–68% | **63%** | ~330 |
| AI stills (Codex/SDXL) | 32% (locked, every episode) | **21%** | ~110 |
| i2v motion | 0–20% | **8%** | ~42 (from 14 seeds) |
| Hero windows (Blender + AE, full-frame) | 0% | **7%** | ~36 |

**burge and postoffice shipped at 68.2% archive with zero i2v.** So 63% is not ambitious; it is below what this channel has already delivered twice. The change that matters is not the archive share — it is **what the AI stills are spent on** (§3).

---

## 2. FOOTAGE PLAN — measured supply, motif by motif

**Re-measured 2026-08-02** against the live ledgers (`scripts/search_archive.py`, plain keyword path). Raw
numbers: `episodes/_planning/measurements/EP60_MOTIF_REMEASURE.json`. **`--shot` phrase search undercounts
badly** — it returns 3 video hits for `underground parking garage` where plain `garage` returns 45 — so
every count here is keyword-path, and a zero from a phrase query (`meeting room`, `filing cabinet`) is not
evidence of absence.

### 2.0 The one finding that decides the budget

The shelf grew by 16,671 rows, and **none of the growth touches this story**.

| Case-specific term | video | image |
|---|---|---|
| `surfside` / `champlain` | 0 / 0 | 0 / 0 |
| `spalling` | **0** | **0** |
| `reinforced concrete` | **0** | **0** |
| `corrosion` | **0** | 24 |
| `rebar` | 1 | 1 |
| `pool deck` | **0** | **0** |
| `condominium` | 1 | 3 |
| `search and rescue` | **0** | **0** |
| `inspection` | 2 | 9 |

Deteriorating reinforced concrete is the physical subject of this film, and across 188,268 catalogued assets
the shelf holds **one** clip that names rebar and **zero** that name spalling. The `concrete` (67 video / 690
image) and `rust` (46 / 839) hits are abstract wall textures and 3D-render surfaces — they can carry a mood,
they cannot carry a diagnosis. **This is the standing justification for Batch A's 56 AI stills**, and the
re-measure confirms it rather than weakening it.

### 2.1 COVERED — build the film's texture out of these

2026-08-02 counts, video / image. The arrow is the change from the 2026-07-31 baseline where one was taken.

| Motif | Video | Image | Note |
|---|---|---|---|
| Courtroom / gavel / judge | **871** ↑144 | 2,052 | biggest gain on the shelf; the Act III–IV spine. ~90 filename false-positives remain — eyeball first |
| Documents / paper / typewriter | **752** | **3,374** | already deep, unchanged. The Act II paper trail |
| Laboratory / lab | **638** | 2,800 | newly measured. Carries the materials-testing register without faking a specific test |
| Coastline / coast | **450** ↑130 | 823 | ×3.5; much of the new intake is 4K |
| Sunrise / dawn | **242** ↑137 | 664 | the ending image. Now deep enough that the last shot need not be reused earlier |
| Construction / engineer / scaffold | **219** ↑127 | 779 | sites, hoists, workers |
| Tower / skyscraper / high-rise | **176 / 123 / 7** ↑8 | 1,229 / 505 | read the caveat in §2.2 before using any of these |
| Crane | **99** | 679 | newly measured; the site-work register |
| Night city / night street | 66 | 139 | v001 printed 314 from a single-word `night` query. On the two-word motif it is 66 — **a method correction, not a loss**; the ledger only grows. Still sufficient |
| Meeting room / conference / town hall | **66** | 298 | the board-meeting register, previously unmeasured |
| Garage / parking | **61** ↑45 | 289 | empty concrete decks |
| Concrete (texture) | 67 | 690 | mood only — §2.0 |
| Rust (texture) | 46 | 839 | mood only — §2.0 |
| Ambulance / firefighter | 40 | 173 | night flashers, no bodies |
| Archive / filing / records | **40** | **624** | previously unmeasured |
| Domestic interiors | **37** ↑13 | 173 | ×2.8 — enough to stop leaning on stills for the home register |
| Debris | 16 | 59 | up from 4, but §6 forbids collapse debris regardless |
| Collapse | 12 | 7 | generic/abstract only |

Theme shelves backing these (`FACTORY_INVENTORY`): property_home 2,982 · urban_night 8,281 ·
documents_paper 3,933 · government_buildings 2,342 · legal_court 3,104 · courtroom_justice 2,451 ·
medical_lab 2,456 · science_tech 3,215 · ocean_nature 2,536 · small_town 1,618. **The theme labels are
known to be broken** (`evidence_bag` returned cartoons), so these are a starting pool to eyeball, never a
selection.

### 2.2 THIN — usable but must be eyeballed one by one

| Motif | Hits | Problem |
|---|---|---|
| **Residential** high-rise | `tower` 176, `skyscraper` 123, `apartment` 10, `high-rise` 7, `condominium` **1** | the 176/123 are **glass commercial towers and city skylines**. A 1981 twelve-storey beachfront condominium is still not on the shelf. Skyline register only — never as "the building" |
| Balcony | 5 / 40 | thin as footage; stills carry it |
| Swimming pool | 8 / 23 | `pool deck` = 0. One strong asset: an aerial of an empty urban pool |
| Florida-specific coast | `florida` 6, `miami` 6 | the 450 coastline clips are rocky northern / Mediterranean, not flat sand and turquoise. Grade warm and flat, or keep the horizon tight |
| Blueprints / technical drawing | 2 / 189 | absent as footage, **covered as stills** |
| Excavator | 8 / 94 | generic site machinery |

### 2.3 ABSENT — do not plan a beat that needs them

- **Spalling, reinforced concrete, rebar, corrosion in place, pool deck, search-and-rescue.** All 0–1. §2.0.
- **The building itself**, at any date, in any condition.
- Rubble of a collapsed residential building — and §6 forbids it regardless.

### 2.4 Rules for using the shelf

1. **Rebuild the inventory before locking the shot list** — `python scripts/build_archive_inventory.py`. The
   ingest lanes are still running, so `ARCHIVE_SHELF_INVENTORY.v001.md` lags the ledger.
2. **Re-measure once more at shot-lock.** This is the second re-measure; each moved the atmosphere numbers and
   moved none of the case-specific ones. If that pattern holds a third time, stop re-measuring and build.
3. **Never select a factory clip by filename.** 40.3% of factory video has no real title (`"title": "id"`).
   Every factory clip entering the shot spec is eyeballed on a labelled contact sheet first. D/E/F lane clips
   carry real source titles; the new intake uses `AF-BG-NNNNN__descriptive_name.mp4`, which is descriptive but
   still query-derived — eyeball it too.
4. **Footage diversity gate stays on**: distinct ≥ 0.40, reuse ≤ 4, generic symbols (scales, gavels) ≤ 2
   across the film. With courtroom at 871 there is no longer any excuse for a repeated gavel.

---

## 3. AI STILLS — 126 images, one prompt each, all of them placed

### 3.1 The count

| Role | Count | Used |
|---|---|---|
| Body stills `S001`–`S110` | **110** | one cut each |
| i2v seed stills `M01`–`M14` | **14** | 42 motion cuts |
| Thumbnail plates `T01`–`T02` | **2** | title A/B test only |
| **Total generated** | **126** | **126** |

Comparison, measured:

| | EP53–56 (30 min) | **EP60 (40 min)** |
|---|---|---|
| Specified | 267 | **126** |
| Actually generated | 267 – 628 | **126** |
| Actually placed in the film | ~120 | **126** |
| Generated and never used | ~150–500 | **0** |

The runtime goes up by a third and the image count halves, because the specification is now **derived from the cut list** instead of from a 210-line motif library that the edit then drew ~100 items from.

### 3.2 What the stills are allowed to be

AI stills are spent **only on what cannot be filmed and cannot be found**. In practice that is three groups:

- **The physical subject the shelf lacks (§2 ABSENT):** corroded reinforcement in concrete, spalling, a slab soffit, water standing on a deck, a planter's weight on a slab, a column head. ~45 stills. This is the film's core imagery and it is exactly what the archive cannot supply.
- **The specific building, handled honestly:** a 1981 Florida beachfront condominium as a *type*, never as a portrait of Champlain Towers South. No attempt at likeness of the real building, and no depiction of the collapse. ~25 stills.
- **Symbolic document beats:** a report crossing a desk, an envelope in a tray, a drawer, an unread page under a lamp — the Act II–III grammar this channel already does well. ~40 stills.

### 3.3 Generation rules (owner directive 3, now enforced in code)

1. **One prompt = one image.** `scripts/generate_sdxl_4k.py` now defaults to `--variants 1` and **refuses** anything higher without `--allow-variants` plus a written reason. Verified: `--variants 3` exits with a refusal.
2. **No candidate pools, no "pick the best", no `_02`/`_03`.**
3. **The only legal re-run is a fixed prompt.** If a plate violates the spec (readable text, a real-person likeness, wrong motif), **edit the prompt and generate that one shot once**. Re-rolling the same prompt on a new seed is banned — that is variant-picking with extra steps.
4. **The "generate until the gate passes" loops are removed.** EP58's `accepted >= 210 になるまで繰り返す` and EP59's "3回失敗したら…再度1枚" must not be copied into EP60's CODEX_A doc. A plate that fails QC three times is a **design** problem: change the beat, or move it to footage or to a graphic.
5. **Hard bans, unchanged:** no readable text or letterforms, no official-looking seals, no likeness of any real person, no fabricated record. Add for this film: **no depiction of the collapse itself and no image that could be mistaken for a photograph of the real building.**

---

## 4. AFTER EFFECTS AND MOTION GRAPHICS — abundant, but not as overlay cards

The owner asked for abundant AE. The measurement says the *quantity* is safe and the *form* is not: EP50's 36 full-frame 5–7s cards produced 6.0s of black and 132.9s of frozen frames and were dropped from the final. So EP60 gets more motion graphics than any previous episode, delivered three ways, none of which is "opaque card pasted over the film".

### 4.1 Remotion `figures[]` — the bulk. 110–130 beats.

Already proven at 165 beats on EP50, in-render, graded and captioned with everything else. 40 components are on the shelf with a passing render smoke test. The ones this story wants:

| Need | Component |
|---|---|
| 98 · 40 years · $9.1M · $15M · $1.02bn | `NumberTicker` |
| the three weeks | `CountdownClock` |
| 1981 → 2018 → 2021 | `YearSweep`, `timeline`, `casetimeline_c` |
| load moving off a failed connection | `ProcessSteps`, `DiagramFlow`, `mechanism: 'gears'` |
| $9.1M vs $15M vs $1.02bn | `ComparisonBars`, `StackedProportion` |
| **pointing at a detail in real footage** | `HighlightRing`, `AnnotationArrow`, `Spotlight` |
| the failure itself | `MechanismReveal kind='faultsplit'` |
| the two verbatim NIST quotes | `QuoteCard` |

`HighlightRing` / `AnnotationArrow` / `Spotlight` are the footage-first workhorses: they let a generic archive clip carry a specific meaning without faking anything. **Banned:** `dochighlight` (builder-level ban, reads as a rendering bug).

### 4.2 AE cards — via `heroCuts`, not via post-render composite

`CaseFilm`'s `FilmData` already types **`heroCuts?: {start, dur, src}[]`** — a full-frame pre-rendered video window, inside the render, below the captions. **It is typed, implemented and used by zero episodes.** Putting AE output there instead of ffmpeg-compositing it over the finished mp4 removes the EP50 failure mode structurally: the card is graded and gated like every other frame.

Rules for EP60's cards:
- **≤3.0 seconds each.** EP50's 5–7s holds are what froze.
- **Never a full-frame black title card.** Type over a live plate, or type that enters and exits within the beat.
- Build with a clone of `build_centralpark_hero_cards.py` (the only Tier-B-capable builder; `HERO_TIMELINE`, `SCALE_TIP`, `STAT_RESOLVE` are proven-rendered).
- **Point `scripts/check_AE_layouts.py:41` at the EP60 builder** or the layout gate silently reports "missing builder".
- If a card must be composited after render instead, use **`composite_hero_scrimkey.py`** or `composite_hero_generic.py --max-card-sec 3.0` (which measures its own output and deletes it if it added black or frozen time). **Never clone a `composite_<slug>_hero.py`** — that generation is what failed.
- Target **12–16 cards**, act titles included.

### 4.3 Blender hero shots — the one thing that must be built new

**Nothing in Remotion, AE or Blender renders a building cross-section, a slab, a column or a load path.** This film needs one. The Blender pipeline is real and affordable: 15 scene scripts exist, EEVEE renders ~1.8 s/frame, so a 6-second 30fps shot is ~5 minutes.

Build **`remotion/src/blender/surfside_section.py`**, cloned from `tyler_govtargument_fracture.py`, rendering **4–6 hero shots**:

1. The building in section — twelve floors, the deck, the garage below.
2. A slab-column connection, clean.
3. The same connection punching through — the mechanism, abstract and unlabelled.
4. Load re-routing to neighbouring columns after the first two fail.
5. The three-week walk across the deck, as a time-compressed abstraction.
6. Optional: the 1981 margin, shown as a bar that was always short.

**These are diagrams, not reconstructions.** They must read as explanatory geometry — no photoreal building, no debris, no bodies, no collapse cinematography (§6).

---

## 5. THE SHOT SPEC IS BUILT FROM THE CUT LIST, NOT THE OTHER WAY ROUND

The failure this replaces: a 210-line motif library was written, 267 images were generated (or up to 628), the edit then placed ~120 of them, and `S101`–`S210` were never seen by anyone.

The EP60 order of work:

1. `EP60_surfside_FILM_BIBLE.v001` → the beat map with per-beat seconds.
2. **Cut list first** — ~520 cuts, each assigned a layer (`footage` / `still` / `motion` / `hero`) before a single prompt is written.
3. Footage cuts → `search_archive.py` queries + **labelled contact sheet + eyeball**, then file paths into the spec.
4. Still cuts → exactly one prompt each, numbered `S001`–`S110`.
5. `M01`–`M14` seeds and `T01`–`T02` thumbs.
6. `EP60_surfside_filmconfig.v001.json` → `scripts/build_case_film_generic.py`.
7. `build_ep60_asset_manifest.py --verify` with `EXPECTED` = the §3.1 counts. **The manifest count and the cut-list count must be equal** — that equality is the gate that makes over-generation impossible.

---

## 6. HONESTY AND DIGNITY (binds every layer)

- **No footage of the collapse, the rubble, the search, or the victims.** None is on the shelf and none will be sought.
- **No reconstruction of the building's fall.** The Blender shots are labelled explanatory geometry.
- **No AI image that could be mistaken for a photograph of Champlain Towers South**, and no likeness of any real person (invariant 11).
- Generic archive footage is used as **texture**, never captioned or implied to be of this case. Where a clip could be mistaken for the real site, it does not go in.
- The 98 are not named (`FACTS_LEDGER` §6, pending owner ruling). The named people are the ones who wrote things down.
- AI disclosure per channel standard; `containsSyntheticMedia` set at upload.

---

## 7. OPEN ITEMS

| # | Item | Blocks |
|---|---|---|
| 1 | Rebuild `ARCHIVE_SHELF_INVENTORY` and re-measure the four THIN/ABSENT motifs once the ingest lanes finish. | Footage plan |
| 2 | Owner ruling: is `heroCuts` acceptable as the AE delivery path (in-render) rather than post-render composite? | §4.2 |
| 3 | Build and smoke-render `surfside_section.py` before the cut list is locked — if the section shots do not work, ~35 cuts move back to stills. | §4.3 |
| 4 | Decide whether i2v runs at all. burge and postoffice shipped **zero** i2v cuts and still reached 68% archive. If the shelf's motion supply is enough, the 14 seeds and 42 motion cuts become archive cuts and the image count drops to **112**. | §3.1 |
| 5 | `check_AE_layouts.py` must be pointed at the EP60 builder. | §4.2 |

---

*Built 2026-07-31 from three measurement passes run in parallel: an AE/motion capability inventory of the repo, an audit of the image specification-vs-generation-vs-placement chain across seven built episodes, and a live probe of the archive shelf (171,597 ledger rows across four drives, 13 motifs, 37 labelled contact sheets eyeballed). Every count in §1–§4 is measured, not estimated. No media was moved and no build file was touched.*
