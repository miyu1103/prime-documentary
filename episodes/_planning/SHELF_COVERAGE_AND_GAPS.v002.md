# Shelf coverage — what the archive can dress (2026-08-09)

Supersedes `SHELF_COVERAGE_AND_GAPS.v001.md`, which was measured by hand on 2026-08-06.
This one comes from `scripts/check_shot_coverage.py`, so it can be re-run after any purge:

```
python scripts/check_shot_coverage.py            # all three channels
python scripts/check_shot_coverage.py --md       # the table below
```

| Channel | Serviceable | Thin (1-2) | None | Coverage |
|---|---:|---:|---:|---:|
| **Prime Documentary** | 20/20 | 0 | 0 | **100%** |
| **Prime Finance** | 18/20 | 0 | 2 | **90%** |
| **Prime Business** | 20/20 | 0 | 0 | **100%** |

Shelf at time of measurement: 63,601 items after 498 GB was deleted the same day.

---

## The shelf was never the problem. The wording was.

v001 reported 85 / 50 / 90 percent and named thirteen shots with no source. Twelve of
those thirteen had material sitting behind them the whole time:

| v001 shot | hits | rewritten as | hits |
|---|---:|---|---:|
| handcuffs on wrists | 0 | `person in handcuffs` | 16 |
| fingerprint card | 0 | `fingerprints on paper document` | 23 |
| police interview room | 0 | `interrogation room detective` | 12 |
| foreclosure sign house | 0 | `for sale sign house` | 109 |
| falling chart on screen | 0 | `stock chart screen` | 47 |
| checkout till transaction | 0 | `cash register shop` | 75 |
| courthouse exterior wide | 2 | `courthouse building exterior` | 399 |

The scoring floor was not lowered to get there. The relevance rule caps a match that
reaches only one of a shot's rare words — precision over recall, CONTRACT 4 — and that
rule is why "county courthouse exterior" stopped returning suburban houses. What changed
is that the shot list is now written in the words a stock title actually uses.

**A zero means "ask differently" far more often than it means "buy it".** Twelve of
thirteen, on this shelf.

---

## Prime Finance — the two that are real

Both were confirmed by looking, not by counting.

| Shot | What is actually there | Fix |
|---|---|---|
| `savings passbook close up` | Two scans of a British Post Office Savings Bank deposit book. `savings account book` returns 16 — 14 are banknote stills carrying the tag. | **prop or generate** |
| `eviction notice on door` | Nothing. All 20 weak hits are road signs, chalkboards and OPEN signs. | **prop** — write the notice and shoot it |

v001 listed seven Finance gaps and recommended a **paid archive** for `ticker tape
machine` and `run on the bank crowd`. Both are now on the shelf and neither costs
anything: `stock ticker board` returns the Western Union and Edison ticker machines plus
period photographs of the NYSE board room, and `foreclosure sale crowd` returns the NARA
farm-foreclosure-sale plates — a crowd at a distressed sale, which is the shot.

---

## Why those NARA plates were invisible until today

`build_footage_contact_sheet.py` did not list `.tif` as an image extension, so a TIF fell
through to the ffmpeg branch, ffmpeg failed to seek one second into a still, and the tile
was drawn as a red UNREADABLE box. 2,953 items on the shelf are TIF — 1,447 from the
Library of Congress, 1,404 from Wikimedia.

Every contact sheet reviewed before 2026-08-09 showed the archival half of those sources
as blank red, and verdicts were recorded from those sheets. Four "Farm foreclosure sale -
NARA" plates sat behind red boxes on the foreclosure sheet — exactly what this channel was
recorded as lacking.

The two `unusable` verdicts most exposed to this were re-checked after the fix and **both
stand**: `prison_jail / loc` is 10 printed pages in 12 (letters, committee reports, labour
tables), and `weather_disasters / noaa` is satellite compositing with CIRA branding and
state boundaries burned in. The sheet builder now also prints how many tiles it could not
decode, so a silent decoder failure cannot be mistaken for bad files again.

---

## How to use the shelf

```
python scripts/search_archive.py --shot "<shot>" --kind video --md --sheet
python scripts/search_archive.py --pick 1,3 --reject 2,4
```

Write the shot the way a contributor would title it. `interrogation room detective`, not
`police interview room`. If a shot returns nothing, run it again with `--weak-ok --sheet`
and look before concluding anything — the weak pool is mostly word collisions ("branch"
returns trees, "card" returns circuit boards), but the real thing is often in there.

Excluded automatically: rows under an owner `unusable` verdict, 492 ban-risk rows, and
anything in `_quarantine`. That now includes 32 press photographs of named serving
officeholders, which had been sitting in `household_loss` scoring as ordinary b-roll.

---

## Not resolved

- **The ingest lanes are exhausted.** gov, sci, web_video and web_audio all ended their
  last run with 0 new items; only `ia` is still moving, slowly. More volume needs new
  queries or new sources, not more time.
- **`savings passbook` and `eviction notice` need props.** Neither depicts a real person
  or event, so generation is rights-clean under invariant 11.
- **~135 theme × source pairs still have no verdict.** They are offered by search today
  on machine score alone.
