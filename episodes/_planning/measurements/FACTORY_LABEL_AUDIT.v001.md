# FACTORY SHELF LABEL AUDIT v001 — how wrong are the theme folders?

Date: 2026-07-28
Scope: `H:\pd-media\assets\factory\` — 88,740 files, 221 GB, the whole b-roll shelf.
Tool: `scripts/audit_factory_labels.py` (measure / report / sheet / link / selftest)
Artifacts: `H:\pd-media\assets\archive\_qc\factory_label_audit\`
Ledger: `H:\pd-media\assets\archive\_ledger\factory.jsonl` (backup:
`factory.jsonl.pre_label_audit.bak`)

**Headline: 40.0% of the shelf's theme labels are contradicted by the recovered
source metadata. 17.5% are confidently mislabeled and have been re-homed. Eyeball
verification on 40 items: the raw shelf label is visually correct 52.5% of the
time; the corrected browse view is correct 70%. Builders must stop selecting from
the raw shelf folders / `select_factory_assets.py --theme`.**

---

## 1. Why this was unmeasurable until now

The shelf was built by running ~300 curated queries against Pexels/Pixabay and
naming every downloaded file **after the query**, not after what came back:

    H:\pd-media\assets\factory\backgrounds\AF-BG-40537__voting_booth_curtain.jpg

`voting_booth_curtain` is the *search string*. The theme a builder reads off that
name (`factory_themes.theme_of(subtype)` → `civic_voting`) is therefore a claim
about the query, not about the pixels. The known casualty was a theme folder
`evidence_bag` full of cartoons; there was no way to tell how widespread that was.

The 2026-07-27 retrofit recovered the **real provider title** (Pexels/Pixabay
canonical URL slug) for all 88,740 files into `factory.jsonl`. AF-BG-40537's real
title is **"christmas market nuremberg"** — which contradicts both the filename and
the theme. That field makes the whole shelf auditable for the first time.

## 2. Method

For every ledger row, the recovered title is scored against **every** theme in the
factory taxonomy and compared with the local filename slug.

- **Relevance engine is imported, not reimplemented.** `audit_factory_labels.py`
  imports `relevance` / `term_hits` / `sense_ok` / `WEAK_TERMS` / `GLOBAL_NEG` /
  `SENSE_GUARDS` / `STOPWORDS` from `scripts/ingest_archive_sources.py` and merely
  *registers* the factory taxonomy into that engine (term cache + `STRONG_EXTRA`),
  so the factory shelf and the archive shelf are judged by one vocabulary, one set
  of sense guards, one weak-term cap and one negative list.
- Per-theme vocabulary = curated single-word domain terms + curated phrases +
  `factory_themes.RULES` keywords (weight 30) + the mapped ingest theme's query
  vocabulary inherited at **weak** weight 15. (Inheriting at full weight was a bug
  found in development: "floor" from money_banking's *"stock exchange trading
  floor"* was single-handedly making *"brown wooden armchair on brown wooden
  floor"* a finance photo.)
- `term_hits` is swapped for a memoized identical-pattern version; `selftest`
  asserts equivalence over 1,150 terms × 1,500 real titles = **0 mismatches**.

### Verdicts

| verdict | rule |
|---|---|
| `match` | local theme's vocabulary is supported by the recovered title (score ≥ 30) |
| `contradiction:cross_theme` | local theme unsupported (< 30) **and** another theme scores ≥ 30 with a ≥ 25 margin → **re-homed to that theme** |
| `contradiction:off_label` | local theme scores **zero** and the title shares no subject-bearing word with the filename slug. No rival theme fits either, so the item **stays in place** and is only flagged |
| `weak` | title neither supports nor refutes (generic slug), or the label is `misc_background`, which claims nothing |
| `no_metadata` | no recovered title — **0 rows** (all 88,740 have one) |

A label is only *contradicted* when the title fails to support it **and** clearly
supports something else. An item whose title supports both (e.g. *"colorful
abstract light streaks explosion"* in the `light` bucket) is `match:dual_subject`,
not a mislabel. This audit accuses the shelf, so it is deliberately conservative.

## 3. Results — overall

| verdict | files | share of 88,740 |
|---|---:|---:|
| match (incl. 1,344 dual-subject) | 34,655 | 39.1% |
| **contradiction — cross_theme (re-homed)** | **13,558** | **15.3%** |
| **contradiction — off_label (flagged in place)** | **17,393** | **19.6%** |
| weak — generic title | 7,975 | 9.0% |
| weak — filename-corroborated only | 3,709 | 4.2% |
| weak — `misc_background` (label claims nothing) | 11,450 | 12.9% |
| no_metadata | 0 | 0.0% |

Excluding `misc_background` (which makes no claim), the population whose label
asserts a subject is **77,290 files**:

- **contradiction rate 40.0%** (30,951)
- **confident mislabel rate 17.5%** (13,558 cross_theme)

## 4. Results — per theme (which folders are poisoned)

Sorted by confident-mislabel (`cross`) rate. `off` = flagged-unsupported.

| local theme | files | match | cross | off | weak | cross % | cross+off % |
|---|---:|---:|---:|---:|---:|---:|---:|
| property_home | 3,674 | 980 | 1,246 | 779 | 669 | **33.9%** | 55.1% |
| forensics_dna | 1,337 | 282 | 413 | 471 | 171 | **30.9%** | **66.1%** |
| legal_court | 4,303 | 763 | 1,325 | 1,036 | 1,179 | **30.8%** | 54.9% |
| particle | 6,564 | 2,108 | 1,550 | 1,984 | 922 | **23.6%** | 53.8% |
| finance_money | 4,888 | 2,071 | 1,142 | 938 | 737 | **23.4%** | 42.6% |
| crime_police | 3,388 | 1,147 | 755 | 769 | 717 | 22.3% | 45.0% |
| school_youth | 1,131 | 503 | 250 | 254 | 124 | 22.1% | 44.6% |
| atmosphere_symbolic | 8,487 | 3,643 | 1,576 | 2,070 | 1,198 | 18.6% | 43.0% |
| abstract | 522 | 158 | 96 | 140 | 128 | 18.4% | 45.2% |
| vfx | 6,229 | 2,410 | 1,116 | 2,057 | 646 | 17.9% | 50.9% |
| civic_voting | 1,204 | 627 | 205 | 263 | 109 | 17.0% | 38.9% |
| surveillance_tech | 6,625 | 2,880 | 1,002 | 1,442 | 1,301 | 15.1% | 36.9% |
| documents_paper | 2,995 | 1,471 | 418 | 657 | 449 | 14.0% | 35.9% |
| medical_lab | 2,358 | 1,351 | 319 | 425 | 263 | 13.5% | 31.6% |
| abstract_loop | 454 | 170 | 56 | 14 | 214 | 12.3% | 15.4% |
| light | 7,428 | 3,261 | 881 | 2,145 | 1,141 | 11.9% | 40.7% |
| urban_night | 5,968 | 3,599 | 702 | 782 | 885 | 11.8% | 24.9% |
| nature_landscape | 5,824 | 4,389 | 365 | 454 | 616 | 6.3% | 14.1% |
| texture | 3,911 | 2,842 | 141 | 713 | 215 | 3.6% | 21.8% |
| misc_background | 11,450 | — | — | — | 11,450 | n/a | n/a |

**Worst offenders (do not select from these unfiltered):** `forensics_dna` (66%
of the folder is contradicted or unsupported), `property_home` (55%),
`legal_court` (55%), `particle` (54%), `vfx` (51%).

**Most trustworthy:** `nature_landscape` (14% contradicted), `abstract_loop` (15%),
`texture` (22%), `urban_night` (25%). These are themes whose vocabulary is dense in
ordinary stock titles, so the provider mostly returned what was asked for.

Top correction flows (cross_theme only):

    particle            -> light               677     legal_court     -> documents_paper 458
    property_home       -> nature_landscape    648     property_home   -> urban_night     458
    atmosphere_symbolic -> nature_landscape    623     finance_money   -> nature_landscape 403
    particle            -> texture             510     vfx             -> texture         390
    surveillance_tech   -> nature_landscape    479     vfx             -> light           389

## 5. Second defect found: the taxonomy itself misfiles by substring

`factory_themes.theme_of()` matches its rule keywords as **bare substrings** with no
word boundary, so a keyword hidden inside a longer word wins. This misfiles files
*before* any provider ever returns anything — it is independent of, and additive
to, the mislabel rate above:

| hidden keyword | subtype | files | filed as | should be |
|---|---|---:|---|---|
| `tree` inside s-**tree**-t | `snowy_street_night`, `rain_street_reflection_night`, `homeless_person_on_street_night` | 682 | nature_landscape | urban_night / atmosphere_symbolic |
| `house` inside light**house** / ware**house** | `lighthouse_in_storm`, `warehouse_interior_dark`, `warehouse_loading_dock` | 740 | property_home | nature_landscape / urban_night |
| `phone` inside micro**phone** | `vintage_radio_microphone` | 310 | surveillance_tech | documents_paper |
| `atm` inside **atm**osphere | `moody_atmosphere_fog` | 236 | finance_money | atmosphere_symbolic |

**1,968 files** are misfiled purely by this bug. The audit repairs most of them
from the title (e.g. 251 of 288 `lighthouse_in_storm` recovered to
`nature_landscape`), but the bug will keep misfiling anything new. Fixing it
requires anchoring the rules at `_` boundaries in `scripts/factory_themes.py` —
**not done here** (it changes `select_factory_assets.py --theme` results for every
episode and needs its own regression pass).

## 6. Eyeball verification — do the pixels agree?

Channel rule: eyeball, don't trust filenames or metadata. 40 items were sampled
(seed 23, images only) **after** the classifier was frozen — a separate seed-7
sample had been used to find and fix classifier defects, and none of those 40 items
appear here. Contact sheets: `contact_sheet_p01..p05.jpg`, index:
`eyeball_sample.json`. All 40 were viewed at 480×270 with their local theme,
recovered theme, filename slug and recovered title burned in.

| bucket | n | verdict |
|---|---:|---|
| `contradiction:cross_theme` | 13 | local label visually valid in **2**; flag justified in **11 (85%)**; recovered theme visually valid in **9 (69%)** |
| `contradiction:off_label` | 12 | flag justified in **6 (50%)**; the other 6 were actually fine locally — but these items are **not moved**, so a false flag costs review noise only |
| `match` | 7 | correct in **6 (86%)**; 1 miss |
| `weak` | 8 | no clearly-mislabeled item was missed |

**The number that matters:**

| | visually correct |
|---|---:|
| raw shelf label (`theme_local`, what a builder reads off the filename) | **21/40 = 52.5%** |
| corrected browse view (`theme_recovered`) | **28/40 = 70.0%** |

Of the 13 items the audit moved, the move **improved 8, worsened 2, was neutral on
3**. The two regressions were both plausible-either-way images
(`water_splash_black_background` moved from `vfx` to `texture` because the title
said "acrylic paint"; a silhouette-at-window moved to `surveillance_tech` because
the title mentioned a smartphone).

Representative confirmed mislabels seen with my own eyes:

- `legal_court/courtroom_interior` → a man riding a **bus in Vietnam**
- `legal_court/courtroom_empty_wide` → a **lake and mountain** landscape; another → **airplane seats**
- `crime_police/evidence_bag` → a **brown leather wallet** (the original incident, confirmed)
- `crime_police/prison_corridor` → the **Hamburg Elbe road tunnel**
- `surveillance_tech/server_room_red_alert` → a **cat on a fence**
- `forensics_dna/fingerprint_scan_blue` → a **Heineken bottle**
- `forensics_dna/blood_sample_vial` → a **Moderna COVID vaccine vial**
- `civic_voting/ballot_box_voting` → a **US roadside mailbox**
- `legal_court/judge_gavel_wooden` → a **puppy behind a fence**
- `vfx/smoke_trail_slow` → a **forest path**, and separately a **mountain range**

Known limits of the measurement:

1. Titles are provider URL slugs, i.e. SEO text ("summer vibes", "dream fantasy
   ghost halloween dark"). They describe the image loosely. No `tags` are present
   on any row, so the audit is title-only.
2. `off_label` is a low-precision flag (~50% by eyeball) — it means *"nothing in
   this title supports the label"*, which is often true of a vague title on a
   correct image. It is deliberately non-destructive.
3. `match` is not proof: 1 in 7 sampled matches was wrong (a **rodeo bull** kept in
   `finance_money` because "bull" is a finance rule keyword).
4. Format buckets (`light`/`vfx`/`particle`/`texture`/`abstract*`) are only ever
   re-homed *within* the format buckets, so a nature photo sitting in `vfx` can be
   flagged but not sent to `nature_landscape`.

## 7. What changed

**Nothing under `H:\pd-media\assets\factory\` was moved, renamed or deleted.**
Episode builds reference those paths and they are untouched — verified after the
rebuild: 88,740 files still present (backgrounds 64,154 · light_assets 7,428 ·
particle_assets 6,564 · vfx_overlays 6,229 · texture_assets 3,911 · loops 454).

1. `factory.jsonl` — every row gained `theme_local` (the pre-audit label, also still
   in `original_dir_theme`), `theme_recovered`, `label_verdict`,
   `label_verdict_kind`, `label_scores`. The canonical `theme` field was set to
   `theme_recovered` (with `theme_source: "label_audit_v001"`) so
   `search_archive.py --theme` and both link tools agree on one tree. Backup at
   `factory.jsonl.pre_label_audit.bak`.
2. `D:\pd-media-browse\factory_browse\<theme_recovered>\` — rebuilt as NTFS symlinks
   on the corrected themes. (H: is exFAT; no links possible there. See
   `H:\pd-media\assets\FACTORY_BROWSE_LOCATION.txt`.) Result:
   `created=16,376 kept=72,364 re-linked=16,376 missing=0 errors=0`, 88,740 links
   across 20 theme folders — the folder counts sum to exactly 88,740. `misc_background`
   shrank 11,450 → 5,437 (6,013 unclaimed files recovered into a real theme);
   `nature_landscape` grew 5,824 → 11,659.
3. `D:\pd-media-browse\factory_browse\_mislabeled\` — 190 groups holding **30,951**
   symlinks (= exactly the contradiction count), grouped `<local>__to__<recovered>`
   for the re-homed ones and `<local>__unsupported` for the flagged-in-place ones,
   so they can be eyeballed as a group. Largest groups:
   `light__unsupported` 2,145 · `atmosphere_symbolic__unsupported` 2,070 ·
   `vfx__unsupported` 2,057 · `particle__to__light` 677 ·
   `property_home__to__nature_landscape` 648.
4. QC artifacts in `H:\pd-media\assets\archive\_qc\factory_label_audit\`:
   `audit_summary.json`, `contradictions.csv` (all 30,951 rows),
   `eyeball_sample.json`, `contact_sheet_p01..05.jpg`, `link_rebuild.log`.

Reproduce:

    python scripts/audit_factory_labels.py selftest   # matcher equivalence
    python scripts/audit_factory_labels.py measure    # ~70 s over 88,740 rows
    python scripts/audit_factory_labels.py report
    python scripts/audit_factory_labels.py sheet --sample 40 --contra 25 --seed 23
    python scripts/audit_factory_labels.py link

## 8. Recommendation for builders

**The raw shelf theme folders are not safe to select from.** Two out of five
labelled files are contradicted by their own source metadata, and eyeballing says a
builder picking blind off the filename gets the wrong subject about **half** the
time. That is exactly the failure mode behind "the footage doesn't match the
narration" and "why is there a Christmas market in the surveillance episode".

Binding guidance until the shelf is re-derived:

1. **Do not use `select_factory_assets.py --theme <t>`** as a selection source for a
   shipped episode. It derives the theme from the filename via
   `factory_themes.theme_of()` — the exact label this audit measured at 40% wrong,
   and it additionally carries the substring bug in §5.
2. **Use `search_archive.py`**, which matches the *recovered title*, and/or browse
   `D:\pd-media-browse\factory_browse\<theme>\` whose filenames are now
   `<source>__<id>__<real-title>` on the corrected theme.
3. **Eyeball before shipping, always.** The corrected view is 70% right, not 100%.
   Generate a labelled contact sheet of the shortlist and look at it. This audit
   exists because metadata lied; the corrected metadata still lies 30% of the time.
4. Treat `forensics_dna`, `property_home`, `legal_court`, `particle` and `vfx` as
   **manual-review-only** folders.
5. Prefer `nature_landscape`, `texture`, `abstract_loop`, `urban_night` when a
   generic bed is needed — they are the folders that survived the audit.

Follow-ups worth doing (not done here):

- Fix the `factory_themes.RULES` substring matching (§5) with `_`-anchored rules and
  re-run this audit; ~1,968 files are misfiled for that reason alone.
- Re-point `select_factory_assets.py --theme` at the ledger's `theme` field instead
  of `theme_of(subtype)`, so one corrected taxonomy serves every consumer.
- `retrofit_factory_ledger.py link` now produces the same tree as this tool (both
  read `theme`), so nightly resume will not undo the correction — verify after the
  next nightly run.
