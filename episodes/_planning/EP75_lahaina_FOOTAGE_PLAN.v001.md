# EP75 · LAHAINA — FOOTAGE PLAN v001

**Every number in this document was measured against the archive on 2026-08-21 before the query set
was written.** That is what `config/episode_footage_queries.v001.json` demands of itself, and the
reason it demands it is on the record: a previous episode wrote 38 descriptive-phrase queries and
**37 of them returned zero rows.**

Counts are `py -3.11 scripts/search_archive.py "<term>" --kind video --limit 5000 --paths-only | wc -l`
against `D:\pd-archive` (14,663 video items indexed).

---

## 1. THE HEADLINE FINDING IS NEGATIVE, AND IT IS THE POINT

**This shelf cannot carry a single one of this film's subject registers.** Measured, not assumed:

| probe | rows | what came back |
|---|---|---|
| `power line` | 0 | nothing |
| `utility pole` | 0 | nothing |
| `electric pole` | 1 | one pixabay landscape |
| `dry grass` | 1 | and it is a **sunset**, which ⛔-12 bars |
| `corrugated` | 1 | — |
| `charred` | 1 | — |
| `overcast` | 5 | — |
| `siren` | 5 | **all police and ambulance sirens**, and one is labelled *ai generated* |
| `smoke` | 215 | factory stacks, welding sparks, studio smoke on black. **No wildfire smoke** |
| `fence` | 83 | **prison footage with prisoners in it** — "angry prisoner behind a wire fence" |
| `chain` | 45 | mostly **blockchain**, and the rest is the same prison yard |
| `theme:weather_disasters` | **14** | the entire library's holding for this subject |

**So the subject registers are removed from the shelf and dressed by plates `H001`–`H132`**, which is
what the image order was written for. This is the same conclusion EP71 reached and for the same
reason: the registers where **place matters** cannot come from a shelf filmed somewhere else.

## 2. ZERO-HIT QUERIES, AND WHAT THEY WERE RETRIED WITH

A zero is a fact about the words, not about the shelf, so **every zero was re-run with different
vocabulary before it was written down as a gap**:

| first attempt | rows | retried as | rows | verdict |
|---|---|---|---|---|
| `power line` | 0 | `electric pole` | 1 | still a gap → plates |
| `utility pole` | 0 | `pole` (bare) | — | rejected: bare `pole` matches *polent*, *Napoleon*, *police* |
| `dry grass` | 1 | `grass field` | 4 | the retry returned rice paddy and mountain highland → plates |
| `corrugated` | 1 | `metal` | 39 | too generic to be a register → plates |
| `charred` | 1 | `burned` | 9 | nine rows, none of them a burned structure → plates |
| `overcast` | 5 | `cloudy` / `cloudscape` | 33 / 79 | **the retry worked** — these are in the kept set |

**The retry that worked is the one that matters**: `overcast` at 5 rows would have been written off as
a gap, and the same register under `cloudy` and `cloudscape` holds 112.

## 3. THE KEPT QUERY SET — 18 terms, measured

These are the registers where **place does not matter**. A cloud filmed anywhere is a cloud over
Maui; a street filmed anywhere is not a Lahaina street.

| query | rows |
|---|---|
| paper | 914 |
| timelapse | 906 |
| hand | 807 |
| hands | 723 |
| screen | 304 |
| office | 256 |
| desk | 128 |
| particle | 98 |
| cloudscape | 79 |
| corridor | 55 |
| dust | 52 |
| asphalt road | 47 |
| document | 33 |
| cloudy | 33 |
| monitor | 21 |
| hallway | 16 |
| grain | 15 |
| console | 4 |

**Supply measured: 4,491 rows across 18 queries** (with overlap between them).

- Clip floor for this runtime: `1857.4 s / 45 s` = **42 distinct clips**. Target is **60**.
- `episode_spec.distinct_video_assets` = **265**.
- **4,491 ≥ 265 ≥ 60 ≥ 42.** The supply clears every floor with a wide margin.

**A hit count is not a supply count and this document says so plainly.** These 4,491 rows are search
matches on human-written titles. What survives filtering, the forbidden-subject sweep and a human
looking at a contact sheet will be a fraction of it. The number above proves the shelf is not empty
for these registers; it proves nothing about any individual clip.

## 4. SUBSTRING TRAPS — measured, and barred by name

The config's own `_why` warns that terms are ANDed substring matches. Confirmed here by reading what
came back:

| term | rows | why it is barred |
|---|---|---|
| `ash` | 365 | matches **wash**ington, sp**lash**, cr**ash**ing, **Ash**ley. Almost no ash |
| `wind` | 339 | mostly **wind**ow; the rest is flags waving |
| `chain` | 45 | mostly block**chain** |
| `paper` | 914 | mostly news**paper** — and a legible newspaper is a `fabricated_record` |
| `texture` | 644 | christmas lights, hookah lights, orange fabric |

`paper` is **kept** but only for the register "hands and paper on a desk", never for a newspaper, and
the forbidden-subject sweep plus the contact sheet are what enforce that.

## 5. WHOLE THEMES EXCLUDED, BY SUBJECT

| theme | items | why |
|---|---|---|
| `prison_jail` | 434 | this is where the shelf's chain-link lives, and every frame of it has a prisoner in it. The gate sequence needs the opposite |
| `small_town` | 617 | every street in it is mainland US, which `era_setting` names as the single most likely wrong clip for this episode |
| `ocean_nature` | 1,060 | **conditionally** — the ocean appears in this film only as a direction, flat and grey. Anything that reads as beauty is barred by ⛔-12 |

## 5.4 CORRECTION, 2026-08-21 — §5.5 BELOW COUNTED AN INDEX, NOT FILES

**Read this before §5.5. The counts in it are from an index whose files are not on disk.**

`select_factory_assets.py` reports "88,850 in shelf" and answers every query from that index. The
media it points at is **`H:\pd-media\assets\factory`**, and it is gone. Measured after mapping
`H:` back to the real media root with `subst H: E:\`:

```
find H:/pd-media/assets/factory -type f   ->   0 files
E:\pd-media total                          ->   13 GB, 6,766 files   (plates and voice masters)
```

The directory tree survives — `backgrounds`, `particle_assets`, `light_assets`, `vfx_overlays` —
and **every one of them is empty**. The contact-sheet tool proved it before the arithmetic did:
`8/8 tiles could not be decoded`, every failure an ffmpeg `CalledProcessError` on a path under
`H:\pd-media\as…`. **A sheet reviewed with those tiles is a sheet reviewed blind**, which is the
tool's own phrasing.

### What IS reachable, measured on disk

The clips survive as **per-episode copies** under `D:\pd-public\<slug>\factory\`, left behind by the
59 episodes that have already staged from the shelf:

| | measured |
|---|---|
| episodes with a staged factory directory | **59** |
| **distinct factory files actually on disk** | **5,806** |
| of those, in this film's usable registers | **2,019** |
| this film needs | **265 distinct** |

**2,019 against 265 is 7.6× the requirement. The downloaded footage is there and this film can be
built with it** — but not through `select_factory_assets.py`, which will keep answering from the
dead index until either the shelf is restored or the tool is pointed at `D:\pd-public`.

### The real counts, from filenames on disk

| register | files | | register | files |
|---|---|---|---|---|
| night | 482 | | office | 108 |
| light | 276 | | road | 92 |
| water | 192 | | desk | 88 |
| wind | 165 | | corridor | 81 |
| sky | 145 | | hand | 75 |
| cloud | 140 | | dust | 68 |
| window | 123 | | **fence** | **64** |
| paper | 116 | | silhouette | 61 |
| ash | 105 | | traffic | 47 |
| smoke | 36 | | screen | 38 |
| **grass** | **35** | | **ember** | **14** |

**Two of §5.5's "zero" findings are wrong on disk.** `grass` returns 0 from the index and **35 real
files** exist; `fence` and `pole` likewise. The index and the disk are different populations, and
**the disk is the one that renders.**

### The cost, stated plainly

**Every one of those 5,806 files has already been used in another episode.** `check_cross_episode_reuse`
identifies by content, so staging from `D:\pd-public` is knowingly re-using footage that has appeared
in up to 59 earlier films. That collides directly with `footage_diversity` and with the standing
instruction to avoid repeated material across episodes.

**The decision this forces, and it is the owner's:**

1. **Restore the factory shelf from backup** — `E:\ValueBackups` is 12.6 GB and `E:\backups` exists;
   neither was checked for a factory archive. This is the only route that gives EP75 unused footage.
2. **Stage from `D:\pd-public` and accept the reuse**, recording it as a release deviation.
3. **Raise the i2v share** so more of the 330 video cuts come from this episode's own 132 plates and
   fewer from any shelf. Costs GPU time, not diversity.

**Nothing should be staged until that is decided.** §5.5 below is left unedited as the record of what
the index claimed, so the difference between the index and the disk stays visible.

## 5.5 THE FACTORY SHELF — as the INDEX reports it (superseded by §5.4)

**There are two shelves and §1–§5 above measured only one of them.** That is a real error in the
first draft of this document and it is corrected here rather than quietly patched:

| shelf | items | searched with | what it is |
|---|---|---|---|
| `D:\pd-archive` | 14,663 video | `search_archive.py` | public-domain and CC archive footage, human-written titles |
| `E:\pd-media\assets\factory` | **88,850** | `select_factory_assets.py` | the production shelf — particles, light, backgrounds, VFX overlays |

The register names in `SCENE_PLAN` §3 are **factory** filenames, not archive titles, so they had to
be measured against the factory shelf. Measured 2026-08-21:

| query | rows | verdict |
|---|---|---|
| `light` | 1,913 | **use** |
| `night` | 1,417 | **use** |
| `particle` | 1,340 | **use** — grounds and overlays |
| `silhouette` | 582 | **use** — the people lane at distance |
| `water` | 529 | **use** — ACT_4 |
| `wind` | 498 | **use** — the film's whole first act |
| `sky` | 437 | **use** |
| `smoke` | 324 | **use, after eyeballing** |
| `window` | 303 | **use** |
| `paper` | 287 | **use** — ACT_5 |
| `cloud` | 244 | **use** |
| `dust` | 210 | **use** |
| `desk` | 177 | **use** — ACT_5 |
| `monitor` | 165 | **use** |
| `road` | 158 | **use** |
| `ocean` | 153 | **conditional** — flat and grey only, never as beauty (⛔-12) |
| `hand` | 149 | **use** — the people lane |
| `ember` | **149** | **use** — verified real: `embers_floating`, `embers_rising_black_background` |
| `screen` | 139 | **use** |
| `corridor` | 112 | **use** — ACT_5 |
| `chair` | 87 | **use** |
| `shadow` | 81 | **use** |
| `metal` | 53 | **use** |
| `concrete` | 53 | **use** |
| `traffic` | 33 | **use** — ACT_3 and ACT_4 |

**Barred after reading what came back, not after assuming:**

| query | rows | why barred |
|---|---|---|
| `fire` | 380 | `campfire_glow_night`, `explosion_fireball_black`, `fire_flames_black_background`, `fireflies_at_night`. **`movie explosion` and `fireball vfx` are in `forbidden_subjects`**, and none of it is a wildfire |
| `fence` | 128 | `prison_yard_fence`, `barbed_wire_fence_sky` (category `crime_police`), `white_picket_fence`. **No usable chain-link.** The gate register stays commissioned |
| `ash` | 348 | the same substring trap as the archive: `cash_stacks_money`, `flashlight_beam_fog`. Only `ash_falling` is real ash |
| `rain` | 459 | wrong weather for a leeward slope in a drought. Not a register in this film |
| `grass` | **0** | nothing. The film's primary fuel does not exist on this shelf |
| `pole` | **0** | nothing |
| `hydrant` | **0** | nothing |
| `folder` | **0** | nothing |

**`grass` 0, `pole` 0, `hydrant` 0 on a shelf of 88,850 items** is the same conclusion §1 reached
about the archive, reached independently on the other shelf. Those registers are plates.

## 5.6 THE DL BUDGET — how many downloaded clips actually reach the cut

**This is the number this document exists to state, because "the downloaded footage never gets used"
is a failure this channel has had before.**

Against the measured master (486 cuts at a 3.8 s mean):

| | cuts | where from |
|---|---|---|
| stills ceiling, 32 % | **156** | the 132 commissioned plates, held with Ken-Burns motion |
| video cuts, 68 % | **330** | of which: |
| — i2v derived from plates | ~**124** | motion generated from `H001`–`H088`, for the registers no shelf holds |
| — **downloaded clips** | **~206** | **the factory shelf, and this is the floor the build must hit** |

**~206 of 486 cuts, or about 42 % of the film, is downloaded footage.** In distinct terms that is
about **165 distinct clips** at the planned 1.25× reuse — **four times** the utilisation floor of 42.

**If the assembled `film.json` contains fewer than 42 distinct factory clips, the build is wrong and
must not be rendered**, whatever else is green. `check_footage_utilization.py` measures it and
`footage_utilization` is the receipt line to read.

## 6. DIVERSITY AND UTILISATION FLOORS — declared

Measured against the delivered master (1,857.4 s) and `episode_spec`:

| floor | value | where it comes from |
|---|---|---|
| **footage diversity**, distinct share | **≥ 0.40** | `check_final_acceptance.footage_diversity` |
| **max reuse of any one clip** | **≤ 4×** | same |
| generic-symbol clips (scales, gavels, clocks) | **≤ 2** | same |
| **footage utilisation** | **≥ 1 distinct factory clip per 45 s** = **42 minimum** | `FACTORY_SECONDS_PER_CLIP` |
| distinct video assets | **265** | `episode_spec.distinct_video_assets` |
| planned mean reuse | **1.25×** against 330 video cuts | scene plan §2.0 |
| cross-episode | `check_cross_episode_reuse.py` **before** staging, not after | identity is by content, not filename |

**EP68 pinto and EP69 hyatt have already spent this shelf's industrial, engineering and
emergency-light registers.** Run the cross-episode check first.

## 7. WHAT MUST HAPPEN BEFORE A CLIP ENTERS A CUT

1. **The factory ledger is missing.** `select_factory_assets.py` warns that with no ledger it falls
   back to filename parsing, which `FACTORY_LABEL_AUDIT.v001` measured at **40 % wrong**. The media
   root moved from `H:` to `E:` and the ledger is not at either path. **Until it is restored, every
   staged clip is UNVERIFIED and the contact sheet is the only check that exists.**
2. **A person opens a labelled contact sheet** of the sky, texture, hands, corridor and road-surface
   registers. `footage_review_required` is `true` in the spec and **no gate in this pipeline ever
   looks at an image**.
3. Nothing from `prison_jail` or `small_town`, and nothing that reads as holiday footage — the spec
   carries 65 `forbidden_subjects`, 25 of them in the holiday family.
