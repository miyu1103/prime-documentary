# Handover 2026-08-26 — the shorts + assets lane

This session took short310-327 (EP77-82) from "designed" to **18 rendered files**, and found two
defects on the way that reach past this batch. Everything below is measured. Nothing was uploaded.

---

## 1. State at handover

```
short310-327   18 RENDERED. 52.1-57.7 s measured on the coverfirst files, CTA cut present in all
               18, three gates clean. NOT uploaded.
short322-324   RENDERED BUT NOT SHIPPABLE — they carry EP81's thumbnail, which the machine
               rejects against EP81's own ledger (§4). Re-render after the thumbnail is fixed.
short289-309   21 rendered previously. Their CTA cards carry the truncated titles §3 fixed;
               re-assembling them would improve the card, and needs a re-render.
uploads        PAUSED until 2026-12-31. `fill_short_schedule.py --dry-run` still prints it.
```

Re-measure:

```
py -3.11 scripts/check_short_constraints.py episodes/_planning/short_designs/PD-2026-07[789]*.json \
                                            episodes/_planning/short_designs/PD-2026-08[012]*.json
py -3.11 scripts/verify_short_designs.py | grep -E "short3(1[0-9]|2[0-7])"    # 0 lines = clean
py -3.11 scripts/fill_short_schedule.py --dry-run                             # "paused until 2026-12-31"
```

## 2. The order of operations, corrected

The previous handover put the AE step before assembly. That is backwards and cost a pass:
**`assemble_short.py` is what writes `runs/ae_jobs/shortNNN.json`.** The order that works:

1. `emit_short_lines_from_designs.py --only 310-327` — **this step was missing entirely.** Without
   it `build_all_short_audio.py` prints "SKIP - no lines file" for all 18 and exits with
   `built 0, failed 18` in zero minutes, which reads like a broken script rather than a missing input.
2. `build_all_short_audio.py --only ...`
3. `stage_short_reuse_plates.py --short NNN`
4. depth maps, **Python 3.10 interpreter** (unchanged, and still true)
5. `assemble_short.py --short NNN`  ← writes the AE job
6. `bash scripts/ae/render_beats.sh runs/ae_jobs/shortNNN.json`
7. register in `remotion/src/Root.tsx`, `npx tsc --noEmit`
8. `bash scripts/render_shorts.sh N N N` in chunks of three

## 3. Two defects found, one fixed in code

### The CTA card was printing broken titles (FIXED)

`short_title()` trimmed the long-form title to 38 characters on whole-word boundaries. Whole words
are not enough. The shipped cards read:

```
"246 Died in the Texas Freeze. The"          (short289-309, on real published Shorts)
"They Got the Lights Back. They Did Not"     (short310, first pass this session)
```

`scripts/assemble_short.py` now prefers the last sentence boundary inside the cap, and otherwise
drops trailing function words. Same inputs now give `246 Died in the Texas Freeze.` and
`They Got the Lights Back.` The 18 new Shorts were re-assembled and re-rendered against it.

**This reaches the back catalogue**: every Short from 283 up has a CTA card, and the ones built
before today have the truncated form.

### 74 Shorts have no funnel CTA cut at all (MEASURED, NOT FIXED)

The previous handover flagged `isCta: 0` on short280/282. Measured across all numeric data files:

```
74 of the numeric shorts have no `isCta: true` cut.
The highest are 63, 66, 82, and then 271-282 — twelve consecutive.
Everything from 283 up has one.
```

So the gap is a contiguous block ending at 282, not a scatter. short280 and short282 are published;
the rest of 271-282 can be re-assembled and re-rendered without touching YouTube.

## 4. EP81's thumbnail contradicts EP81's own ledger — BLOCKING for short322-324

All three of `episodes/PD-2026-081-station/09_package/thumbnail.station.0*.v001.png`, and the
`thumbnail.selected.v001.png` that points at one of them, carry the words **"100 COUNTS."**
There is no clean alternative on disk. The machine rejects it:

```
py -3.11 scripts/check_packaging_claims.py --slug PD-2026-081-station --thumb-text "100 COUNTS."
  FAIL CONTRADICTED  [thumbnail_text/quantity] '100 COUNTS.'
    EP81_station_FACTS_LEDGER.v001.md:15   > Until it is, no charge, no plea, no sentence and no name may
    EP81_station_FACTS_LEDGER.v001.md:183  > Nothing about charges, pleas...
```

The Shorts' CTA card shows the destination episode's own thumbnail, so short322, short323 and
short324 currently put that claim on screen. They rendered, they are in band, and they must not
ship until the long-form thumbnail is remade. That remake is the packaging lane's job and needs
owner approval; re-rendering the three Shorts afterwards is about fifteen minutes.

The other four are clean by the same check: `90% WORN AWAY`, `STILL ABOARD.`, `ONE TO ONE.`,
`FAILED BEFORE.` — but note that **EP78's "FAILED BEFORE." is exactly what EP78's Shorts were
written to avoid** (the one-in-eight check-ride failure rate is spoken so the captain's record is
not read as the mark of a dangerous man). The machine passes it; a person should look at it.

## 5. Long-form titles for EP78-82 are provisional and need the owner

short313-327 could not be assembled at all: `destination_title()` refuses when the episode has
neither `youtube_meta*.json` nor `_title_draft.v*.json`, and EP78-82 had neither. Written this
session, each claim taken from that episode's own `03_script/script.en.v001.md`, each passing
`check_packaging_claims.py` with rc=0:

| EP | title | on the CTA card |
|---|---|---|
| 078 colgan | The Warning Fired With Wings Level. There Were Eighteen Seconds Before It. | The Warning Fired With Wings Level. |
| 079 alaska261 | It Was Measured Once. There Is No Record of What It Said. | It Was Measured Once. |
| 080 concordia | Sixty-Nine Minutes to Give the Order. Everybody Could Have Got Off. | Sixty-Nine Minutes to Give the Order. |
| 081 station | Two Doors on the Outside. One Door on the Inside. | Two Doors on the Outside. |
| 082 valdez | The Number on the Paper Had Not Moved. The Ship Had Stopped Going to Panama. | The Number on the Paper Had Not Moved. |

They are marked `status: draft_awaiting_owner_approval` in each file. **If the owner picks different
titles, the 15 Shorts have to be re-rendered** — the card burns the text in.

## 6. Other measured facts from this session

* **Seven of the 18 mixes came out over the 57 s gate** (up to 63.9 s) on 180-word designs. The
  words-per-second rate is not constant: short318 runs at **2.75 w/s** because its lines are full of
  spelled-out numbers, against 3.16 for short325. Trim, rebuild, and **measure the mp3** — three
  passes were needed on short318 alone. The word band is still not a length proxy.
* **short312 referenced two rejected plates** (`H086`, `H116`, both sitting in `img/rejected/`), so
  staging failed with `source missing`. Replaced with `H122` (dusk harbour, bridge span behind
  moored vessels) and `H127` (empty lit carriageway across a long bridge at night), and the design's
  `subject` text was rewritten to describe what those plates actually show.
* **`build_plate_contact_sheet.py --src` writes into `runs/qc/plate_sheets/<slug>/` regardless**, so
  reviewing a candidate batch overwrites that slug's real review sheets. keybridge sheets 01-29 were
  regenerated afterwards from the accepted pool; 30-33 are left over from the original 131-plate run
  and no longer line up. The authority is `runs/qc/keybridge_plate_verdicts.v001.json`, not the sheets.
* `--cell` needs `WxH` (`320x180`); a bare number crashes in the argument parser.
* Render: six chunks of three, `failures=0` on every chunk, bundle removed between chunks.

## 7. Costs

ElevenLabs, all at standing approval: $5.37 for the first 18, then $2.04 + $0.86 + $0.30 + $0.28
across four trim passes. **$8.85 total**, of which $3.48 was re-recording lines that were written
too long the first time.
