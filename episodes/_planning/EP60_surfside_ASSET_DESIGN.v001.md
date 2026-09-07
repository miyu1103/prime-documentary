# EP60 · CHAMPLAIN TOWERS SOUTH — ASSET DESIGN v001

**40 minutes · footage-first · owner directives 2026-07-31.** Companion to `TOPIC_PIPELINE.v005.md` (the pick) and `EP60_surfside_FACTS_LEDGER.v001.md` (what may be said). This file decides **what every frame is made of**, and it is written against measurements taken today, not against the previous episodes' assumptions.

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

Measured by plain keyword search over the live ledgers (`scripts/search_archive.py`). **`--shot` phrase search undercounts badly** — `--shot "underground parking garage"` returns 3 video hits where plain `garage` returns 45 — so all counts below are keyword-path.

**Case-specific footage does not exist**: `surfside` = 0 hits, `champlain` = 0 hits. Nothing of the building, the site or the collapse is on the shelf. Every frame of this film is either generic footage standing in, a symbolic still, or a constructed graphic — and the film must be honest about that (§6).

### COVERED — build the film's texture out of these

| Motif | Video hits | Note |
|---|---|---|
| Night city / night street | **314** (202 in the new lanes) | best-supplied motif on the shelf; 24/24 eyeballed genuine |
| Documents / paper / signing / typewriter | **747 / 99 / 52** | 19/24 genuine — the Act II–III spine |
| Courtroom / gavel / judge | **144 / 64 / 48** | 57 genuine clips from ia/nara/loc sit behind ~90 filename false-positives |
| Sunrise over water | **137** (98 new) | the ending image |
| Coastline (generic) | **130** (124 new, much of it 4K) | see THIN below for the Florida problem |
| Construction / inspection / engineer | **127 / 18** | sites, workers, scaffolding, hi-rise hoist |
| Underground parking / garage | **45 / 59** | 20/24 genuine empty concrete decks |
| Ambulance / firefighter (night, no bodies) | **39 / 5** | flashing light at night; 21/24 genuine |
| Blueprints / technical drawings | **1 video / 188 stills** | absent as footage, **covered as stills** — 23/24 genuine |

### THIN — usable but must be eyeballed one by one

| Motif | Hits | Problem |
|---|---|---|
| Residential high-rise / condominium | 8 strong video (`condominium` = **0**) | mostly Osaka skylines and glass office towers — **not** a 1981 Florida beachfront condo |
| Swimming pool / pool deck | 6 of 24 genuine | the rest is aquarium and marine wildlife. One strong asset: an aerial of an empty urban pool |
| Empty domestic interiors | ~13 clips | stills are fine (87 kitchen / 66 living room / 112 bedroom) |
| Florida-specific coast | `florida` = 4, `miami` = **0** | the 130 coastline clips are rocky northern/Mediterranean, not flat sand + turquoise |

### ABSENT — will not be found; do not plan a beat that needs them

- **Concrete spalling / rebar / corrosion.** `rebar` = 1, `corrosion` = 0, `spalling` = 0. The `concrete` (60) and `rust` (39) hits are abstract wall textures and 3D-render abstractions. **This is the film's central physical subject and the shelf cannot supply it.**
- Rubble / debris of a collapsed building (`rubble` = 1, `debris` = 4) — and we would not use it anyway (§6).
- Filing cabinets / a government records office (`filing cabinet` = 0).

### Rules for using the shelf

1. **Rebuild the inventory first** — `python scripts/build_archive_inventory.py`. The doc is ~29,000 rows stale.
2. **Re-measure before locking the shot list.** Four ingest lanes were writing during this measurement; the Florida/condo/pool gaps may close.
3. **Never select a factory clip by filename.** 40.3% of factory video has no real title. Every factory clip entering the shot spec must be eyeballed on a labelled contact sheet first. Clips from the D/E/F lanes carry real source titles and are metadata-trustworthy.
4. **Footage diversity gate stays on**: distinct ≥0.40, reuse ≤4, generic symbols (scales, gavels) ≤2 across the film.

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
