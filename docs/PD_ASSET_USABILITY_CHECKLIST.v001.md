# Asset usability checklist v001

Before a clip goes in a film, one command answers what is known about it:

```
py -3.11 scripts/build_asset_usability.py --path <file>
```

It reads `runs/asset_usability.v001.jsonl`, one line per shelf file, built by joining five
sources that never previously met. Rebuild it after any rights or index change:

```
py -3.11 scripts/build_asset_usability.py            # rebuild, ~30 s for 130k assets
py -3.11 scripts/build_asset_usability.py --summary  # counts only
```

**Measured 2026-09-03 across 130,283 assets:**

```
  audio  clear       2000     image  clear      85519     video  clear      31441
  audio  hold        6675     image  hold        2773     video  hold        1345
                             image  blocked         1     video  blocked      526
```

---

## 1. RIGHTS — the only field that can stop a shipment

Three values, and they are not advisory.

| value | meaning | what to do |
|---|---|---|
| `USABLE` | the source itself grants commercial use with no attribution obligation: `pd`, `cc0`, or a blanket stock licence (`free_commercial`) | use it |
| `HOLD` | nobody has established a licence, or the licence needs attribution | **do not use.** Attribution-bearing licences are held on purpose (`ingest_archive_sources.py`: "CC-BY -> quarantine, attribution recorded") because this channel has no attribution surface in-frame |
| `DO NOT USE` | examined and refused: someone else's copyright, or off-brand for the channel | never. The reason is printed under it |

`rights_basis` prints the evidence, not an opinion. Examples actually in the record:

```
nara says: nara use=Unrestricted access=Unrestricted
wikimedia says: CC0 Creative Commons Zero, Public Domain Dedication
archive.org collection 'feature_films' holds other people's copyrighted work; do not restore
uploaded by the rights holder itself ('City of East Grand Forks') ...
```

**A `HOLD` is not a maybe.** 11,320 assets sit there, and most are held because a lookup has not
been run yet, not because anything is wrong with them. `scripts/resolve_item_licences.py` clears
them in batches; Freesound answers 2,000 ids a day and the Library of Congress answers none at
all (every endpoint returns 403, measured 2026-09-03).

## 2. TECHNICAL — what will actually hold up on screen

| field | read it as | floor that matters |
|---|---|---|
| `w x h` | real probed resolution | **below 720p is a defect on a 4K timeline.** 85% of NARA video and 80% of IA video is below 720p |
| `motion` | how much the frame changes | a near-zero value is a still photograph in a video container. The owner rejects those as 紙芝居 |
| `centre_energy` | does the subject survive a 9:16 crop | only 12% of the shelf keeps its subject vertically. Below ~0.25, a Short will crop the subject out |
| `luma_crop` | brightness of the cropped frame | a dark blob reads as a black screen after grading |
| `in semantic search` | is it findable | **`False` means a search will never surface it.** The clip exists but is invisible to the tool that picks clips |

A missing technical field is printed as absent rather than as zero. `resolution unmeasured`
means nobody probed it, not that it is small.

## 2.5 THEME — the least trustworthy field on the shelf

Printed whenever the theme has been scored, with a warning below 50 per cent:

```
  THEME       courtroom_justice  30.3% on-label  <-- THEME IS UNRELIABLE
```

**Measured 2026-09-04 by looking at the pixels.** A 20-tile sheet of `courtroom_justice` held
one courthouse. The other nineteen were a mountain range, a Delhi mosque, a bedroom, a
supermarket drinks aisle, a garden swing, stacking stones, an Italian fruit market and a woman
reading Chomsky on a green screen. `americana_1930s_1970s` was worse: nineteen of twenty tiles
were 16th-18th century European allegorical engravings from the Met.

The queries were never the problem. The ingest asked pixabay for "judge bench gavel" and pixabay
matched it a word at a time, returning "bank wooden bench bench relax to sit sea". It asked the
Met for "america" and got "allegory of america", a 17th century engraving. **Nothing compared the
result to the request**, so 66 per cent of the shelf carries a theme nobody checked.

`check_theme_label_honesty.py` scores each theme: what share of its assets carry a word
distinctive to that theme, after generic scene words (bench, yard, case, cell, room, building)
are removed — those are the exact words that let the wrong assets in. Worst first, measured:

| theme | usable | on-label |
|---|---|---|
| americana_1930s_1970s | 334 | **1.8%** |
| bank_and_branch | 470 | 12.1% |
| world_cities | 1,547 | 12.3% |
| decision_rooms | 209 | 12.4% |
| small_town | 1,451 | 21.0% |
| courtroom_justice | 1,889 | 30.3% |
| police_modern | 1,771 | 33.3% |
| prison_jail | 1,566 | 47.3% |
| money_banking | 2,256 | 47.3% |

Full ranking: `runs/theme_label_honesty.v001.json`. Sheets: `runs/qc/theme_sheets/`.

**A title is not a picture.** This ranks themes for review; it does not condemn an individual
asset. But under 50 per cent, searching by theme is worse than useless — it returns confident
wrong answers. Search semantically (`index_footage_semantic.py --query`) and look at the result.

**Since 2026-09-05 the checklist also prints the EYE VERDICT** — the judgement a person made
after opening that theme's 20-tile sheet (all 68 themes were reviewed; the record is
`docs/shelf/theme_eye_review.v001.json`):

```
  THEME       courtroom_justice  30.3% on-label  |  eye verdict: QUARANTINE
```

The score and the eye disagree in both directions — `police_modern` scored 33% and holds zero
real police; `bank_and_branch` scored 12% and is three-quarters real American banks — so when
they conflict, **the eye verdict wins**. A `QUARANTINE` verdict does not block the asset (the
defect is the label: a mountain filed under `courtroom_justice` is still a fine mountain); it
means the theme name must not be trusted as a description of what the file shows.

## 3. NOT CHECKED — printed on every asset, on purpose

Two lines appear under every single record:

```
- no human has confirmed the content matches the label
- no check for a watermark, a logo or an identifiable real face
```

They are not boilerplate. **Nothing on this shelf has been looked at by a person.** Episode
plates have `runs/qc/<slug>_plate_verdicts.v001.json`; archive clips have no equivalent, and the
two failures that reached shipped work both came through this hole:

* `evidence_bag` returned cartoons — the label was wrong and every gate passed it, because no
  gate reads a pixel.
* A generator watermark reached a plate that a machine had cleared.

So the record refuses to imply otherwise. Before a clip goes in a cut, **open it**. The cheap way
is a labelled contact sheet: `scripts/build_footage_contact_sheet.py`.

## 4. How to use this when choosing clips

1. Search for candidates as usual (`index_footage_semantic.py --query "..."`).
2. Run `--path` on each shortlisted file.
3. Drop anything that is not `USABLE`. A `HOLD` is not a "probably fine".
4. Drop anything below 720p if it will be full-frame, and anything with near-zero `motion`.
5. For a Short, drop anything with low `centre_energy` — the subject will not survive the crop.
6. **Look at what survives**, as a contact sheet, before it is cut in. That step is not optional
   and this file cannot do it for you.

## 5. What this file is not

* It is not a licence. It records what a source said and when, with the text it said it in.
  A record with `rights_basis: "license_decision=free_commercial"` and nothing else is repeating
  an ingest-time assumption, not a verification.
* It is not a quality judgement. `motion=18.5` says the pixels move, not that the shot is good.
* It is not current by itself. Rebuild after any rights pass, or it will describe yesterday's
  shelf with today's confidence.
