# Shelf coverage — what the archive can dress, and what it cannot (2026-08-06)

Measured, not estimated. Each channel was given a realistic 20-shot list for a typical
episode and every shot was run through `search_archive.py --shot`. A shot counts as
**serviceable** when the ranked search returns three or more candidates that exist on disk.

| Channel | Serviceable | Thin (1-2) | None | Verdict |
|---|---:|---:|---:|---|
| **Prime Business** | 18/20 | 2 | 0 | **90% — ready to produce** |
| **Prime Documentary** | 17/20 | 1 | 2 | **85% — ready to produce** |
| **Prime Finance** | 10/20 | 3 | 7 | **50% — seven shots have no source** |

Shelf at time of measurement: 236,069 items / 2.56 TB. Finance-specific 10,351,
Business-specific 19,704.

---

## The number that mattered was never the item count

The original target was 30,000 items per channel. That figure was proposed, not measured,
and it was wrong in both directions: Business reached 90% coverage at 19,704 items and
needs nothing more, while Finance would not reach 100% at any item count because the
missing shots are not on any free source.

Counting items measures the shelf. Running a shot list measures whether an episode can be
cut. Only the second one is a production answer.

---

## Prime Finance — the seven shots with no source

Every one of these returned zero after Commons categories were exhausted (`Bank runs`,
`Ticker tape`, `Stock tickers`, `Foreclosure`, `Boarded doors` all walked to completion,
yielding one new file), all 147 stock queries reported `sources exhausted`, and Openverse
returned HTTP 500 on three separate verification attempts.

| Shot | Why free sources fail | Cheapest fix |
|---|---|---|
| stacks of banknotes counted | stock sites have static cash, not the counting action | **generate** — no real person or event depicted |
| savings passbook close up | obsolete object, not photographed by stock contributors | **prop** — print and shoot, or generate |
| ticker tape machine | 1920s-30s hardware; Commons holds 14 files, all already taken | **paid archive** (Getty/AP) |
| falling chart on screen | direction words return animals and sunsets on tag-based sites | **generate** — a screen graphic is synthetic anyway |
| eviction notice on door | legal document photographed in situ is rare and often identifying | **prop** — write and shoot |
| foreclosure sign house | US-specific signage, thin outside paid libraries | **generate** or paid |
| run on the bank crowd | historical event; Commons `Bank runs` holds 6 files | **paid archive** |

**Two of the seven need a paid archive** (ticker tape machine, bank run crowd) because they
are historical events that were filmed by commercial newsreels, not by federal agencies.
The rest are props or graphics, where generation is both cheaper and rights-clean — none
depicts a real person or a real event, so invariant 11 is not engaged.

## Prime Documentary — two shots with no source

`fingerprint card` and `police interview room`. Both are modern procedural interiors that
stock libraries do not carry and that federal archives do not photograph. Prop or generate.

## Prime Business — no gaps

`workers leaving factory gate` and `forklift moving pallets` return two candidates each.
Usable, but a second option should be sourced before either is cut twice in one episode.

---

## How to use the shelf

```
py -3.11 scripts\search_archive.py --shot "<shot description>" --kind video --md --sheet
py -3.11 scripts\search_archive.py --pick 1,3 --reject 2,4
```

`--sheet` renders the candidates as a labelled contact sheet. Look at it. Filenames lie —
`AF-BG-6237__courthouse_steps.mp4` is a university campus, and a clip titled
"2019 AUG 11 U.S. FBI Eyes Epstein's Death" turned out to carry a Fox News chyron that no
title pattern could have caught.

Excluded automatically and not offered: 115,305 rows under owner `unusable` verdicts,
234 ban-risk rows, and anything sitting in `_quarantine`.

---

## Known open issue

`nypl` has climbed back to 64,370 rows. 46,707 New York City directory page scans were
deleted on 2026-08-02 as unusable; a lane running `--source all` has been re-fetching the
same collection since. The ledger rows keep them out of search results, so production is
unaffected, but the disk cost is real and it will keep growing until that lane is given a
`--theme` restriction or the ingest is taught to read the verdict file.
