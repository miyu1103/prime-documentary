# The 11 quarantined themes — what the decision actually costs

Owner decision, prepared 2026-09-06 by the assets lane. Nothing here has been applied. Every
number below was measured today from the ledger, the eye review and the semantic index; the
commands are named so any of it can be re-run.

---

## 1. The question

`docs/shelf/theme_eye_review.v001.json` marks 11 of 68 themes QUARANTINE — their labels do not
describe their contents. **Nothing in the pipeline acts on that verdict.** The per-asset checklist
prints it, and that is all: a grep for `theme_eye_review` across `scripts/` returns exactly one
file, `build_asset_usability.py`, which reports and never removes. So
`select_factory_assets --theme courtroom_justice` still serves mountains and allegorical engravings
today, exactly as it did before anyone looked.

The question is not "are these themes bad" — that was settled by opening every sheet. It is
**what should happen when a tool asks for one by name.**

## 2. What is behind the label

19,378 usable assets. The `eye` column is what 20 sampled tiles actually showed.

| theme | assets | eye | what is really in it |
|---|---:|---:|---|
| `atmosphere_symbolic` | 6,091 | 40% | **a Mickey Mouse figurine** (Disney IP), 2 corrupted images, a JOHN BROADWOOD nameplate |
| `misc_background` | 4,025 | — | **a LEGO minifigure**, **a Bee Gees record with a legible label**, a branded heater; mostly wedding rings |
| `legal_court` | 2,292 | 10% | 1 Lady Justice in 20. Gym equipment, a Hindu temple, London buses, Mars, a Swiss farm ("court farm yard") |
| `courtroom_justice` | 1,889 | 5% | 1 courthouse in 20. A mountain, a Delhi mosque, a bedroom, a Coca-Cola shelf, Chomsky on green screen |
| `police_modern` | 1,771 | **0%** | **zero real police.** Two cartoon police figurines, a steampunk CG hover-car, BMW/Morgan/IKEA branding |
| `small_town` | 1,451 | 8% | the 3D cartoon cowboy, a THYSSEN sign, a Hungarian railway, a rice paddy, fantasy CG |
| `economy_crisis` | 922 | 25% | **Chinese schoolchildren in uniform** (matched "queue") — children, and foreign |
| `americana_1930s_1970s` | 334 | 5% | 19 of 20 are 16th–18th c. European allegorical engravings ("allegory of america") |
| `anonymous_crowd` | 302 | 20% | "feet" matched a plate of pork feet. A swan, a bear, a carousel, a fashion model |
| `household_loss` | 289 | 30% | **a "FREE PALESTINE / END THE OCCUPATION" door sign** — channel risk |
| `laboratory_forensics` | 12 | 8% | nothing forensic. NOAA's undersea AQUARIUS and Mars Science Laboratory |

Four of these carry things that stop a ship under the existing four classes (IP, identifiable
children, a political sign), not merely things that waste an editor's afternoon.

## 3. The cost of quarantining, measured

The canon already says the right way to search is by meaning, then look at the picture. If that
were true for everything, closing theme-name access would cost nothing. It is true for video and
**false for images**:

```
                     usable   video   image   in semantic index
TOTAL                 19,378   6,157  13,221               5,887
```

**95.6% of the video (5,887 of 6,157) is reachable by meaning without its theme name.**
**0% of the 13,221 images is** — `index_footage_semantic.py` globs `*.mp4` and `*.mov` only, so
all 30,470 index entries are clips. For an image, the rotten theme label is the *only* way in.

That is the whole trade-off. Quarantine by theme name and video loses almost nothing, while
13,221 images become unfindable — including the genuinely good ones, which in
`atmosphere_symbolic` alone is on the order of 2,000 pictures.

(`anonymous_crowd` is the one anomaly: 175 videos but 11 indexed. Not investigated.)

## 4. Where a guard would have to go

Surveyed today; **read this as a map to verify, not as verified code** — no guard has been written
or demonstrated. Two facts in it are load-bearing and were checked by hand: only
`build_asset_usability.py` reads the eye review, and the semantic indexer is video-only.

* **There are two shelves with two ledgers.** `quarantine_theme.py` moves files under
  `E:\pd-archive`; the factory shelf lives under `E:\pd-media\assets\archive` with its own ledger.
  **`quarantine_theme.py --theme courtroom_justice` cannot hide anything from
  `select_factory_assets.py`**, which is the tool that actually serves episodes.
* The cheapest chokepoint is `factory_ledger_themes.select()` / `tier_of()` — every factory pick
  funnels through it. Guarding the `--theme` *flag* is not enough: `--subtype`, `--query`,
  `--category` and `--scene-type` reach the same assets without naming a theme, and `--no-ledger`
  drops to filename-derived themes where a ledger-reading guard vanishes.
* `search_archive.py` already has a per-theme unusable map (`_qc/archive_verdicts.jsonl`), keyed by
  `(theme, source)` — the 11 could be written into it, with `--include-unusable` as the escape.
* Two routes are theme-blind and a theme guard will not touch them:
  `bind_short_footage_semantic.py` (picture similarity) and `stage_footage_by_title.py`.
* **The quarantine would erode.** `recover_stock_shelf.py` re-links assets and re-derives the theme
  with no quarantine check, and the scheduled ingest runs `--theme all`, so the same labels refill.

## 5. The three options

**A. Leave it. Warn only.** Today's state. The checklist prints QUARANTINE when someone asks about
one asset, and nothing stops a bulk theme pick. Costs nothing, changes nothing, and the next
episode that asks for `courtroom_justice` gets mountains — which has already happened.

**B. Guard theme-name selection for these 11.** Refuse them at
`factory_ledger_themes.select()` and in `search_archive.py` unless an explicit override is passed.
Nothing is deleted or moved. Video is essentially unaffected (95.6% still reachable by meaning);
**13,221 images become unreachable** until an image index exists. Erosion has to be handled
separately.

**C. Build an image semantic index first, then guard.** Extend the CLIP indexer to still images
(85,423 usable images shelf-wide, not just these 19k). That removes the dependency on rotten labels
for the whole shelf, not only the 11 themes, and makes B free of its one real cost. The GPU is idle
right now (2.1 of 24.5 GB, 4%), but this lane does not own the GPU — a render or i2v job in another
lane would contend, so the timing is the owner's call.

**Recommendation: C, then B.** B alone trades a known problem for a quieter one — the images do not
become safe, they become invisible, and invisible material is what produced these labels in the
first place. C is the only option that makes "search by meaning, then look" true for images, which
is what the canon has been telling everyone to do since the labels were found rotten.

Not recommended: deleting anything. `atmosphere_symbolic` is 40% on-label — the material is real,
the label is what failed.
