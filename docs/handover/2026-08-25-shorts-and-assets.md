# Handover 2026-08-25 — the shorts + assets lane

This lane is **asset gathering and Shorts**. Owner's direction, restated 2026-08-25 in-session:
this thread does footage DL and Shorts creation, **and Shorts are stopped for a while** — so the
Shorts deliverable was frozen at the design stage (deliberately complete, ready to thaw) and the
thread's active work is the shelf. Long-form belongs to the main thread, as before.

Everything below is measured. Commands are inline.

---

## 1. State at handover

```
Shorts designs        short289-309 ALL 21 designed -- the 15 remaining (295-309) were
                      authored this session, 5 design files, 0 problems on both gates
Shorts audio/build    NOT STARTED, on purpose (owner: shorts stopped for a while)
Shorts scheduled      26 uploaded with publishAt, publishing through 2026-08-30; push
                      itself PAUSED until 2026-08-29 (config/shorts_pause.v001.json)
shelf                 128,160 files, ledger PASS, 0 torn / 0 dup / 0 missing (measured
                      at session start; ingest has added since)
ingest                place-neutral 4 themes (night_road_lamp, window_interior_light,
                      clock_and_waiting, corridor_and_stairs) x pixabay+mixkit+coverr,
                      50-pass run live in background, log runs/ingest_placeneutral_20260824c.log
anonymous_crowd       deny round 3 applied (india/ukraine/baby-stroller class), smoke-
                      verified; REAL batch + contact sheet still owed (see §4)
```

Re-measure:

```
py -3.11 scripts/check_ledger_integrity.py
py -3.11 scripts/check_short_design.py --all          # 99 problems, ALL in short86-269 (old designs); short295-309 = 0
py -3.11 scripts/check_short_constraints.py episodes/_planning/short_designs/PD-2026-07*.design.v001.json
tail -5 runs/ingest_placeneutral_20260824c.log
```

## 2. The 15 Shorts, and what "designed" means here

Five design files, `episodes/_planning/short_designs/`:

| file | shorts | words (measured) |
|---|---|---|
| PD-2026-074-itaewon.design.v001.json | short295-297 | 178 / 175 / 174 |
| PD-2026-075-lahaina.design.v001.json | short298-300 | 172 / 175 / 161 |
| PD-2026-076-morandi.design.v001.json | short301-303 | 171 / 173 / 178 |
| PD-2026-072-lacmegantic.design.v001.json | short304-306 | 173 / 176 / 178 |
| PD-2026-073-uri.design.v001.json | short307-309 | 168 / 178 / 164 |

Every line traces verbatim to the episode's own `03_script/script.en.v001.md` (the gate proves
it), every plate was verified present on disk before being named, specs were read at their
HIGHEST revision (lahaina = v003), and the prose `forbidden_claims` — 12 for itaewon, 10 for
lahaina, 10 for morandi, 8 each for lacmegantic and uri — were read by hand against every Short.
The deliberate design choices worth knowing before touching them:

* **No Short names a person.** itaewon's ward chief appears only by office with the first-instance
  acquittal in the same breath; morandi's convictions are not mentioned at all; lacmegantic's
  acquitted three are absent entirely. This is what keeps the four ship-blocking classes clean.
* **Counterfactuals are refused in the text itself** — lahaina's siren Short CLOSES on "not one
  of them says that sounding the siren would have changed the outcome"; uri never says the grid
  collapsed; lacmegantic gives the seven hand brakes against BOTH the railway's nine and the
  investigation's 17-26, per spec.
* Lines files for the narration generator are already emitted:
  `episodes/<EPID>/09_package/short295..309_lines.v001.json` (via emit_short_lines_from_designs.py,
  ElevenLabs estimate ~$0.90/episode).

**To thaw the lane**: `build_all_short_audio.py --only 289-309` (resumable, skips existing) →
`assemble_short.py` / `build_short_mix.py` / `verify_short_designs.py` / `verify_short_plates.py`
→ the 16:20 push from 8/29, four a day at 06/09/18/21. Nothing before the owner un-stops Shorts.

## 3. Plate-on-disk is not plate-reviewed: three episodes have holes

The constraint gate checks the plate EXISTS; existence turned out to be the scarce thing:

* lahaina: 14 of the reviewed plates are NOT on disk as PNGs (H010, H013, H016, H022, H025,
  H049, H053, H061, H076, H084, H089, H108, H111, H132) — consumed by i2v/motion. Designs
  were re-pointed at on-disk alternates and re-verified.
* morandi: only 60 of ~120 reviewed plates survive as PNGs. itaewon: I001/I063/I092/I120 absent.
* If anyone regenerates or restores plates, the designs name their exact plate ids — re-run
  `check_short_constraints.py` and it will tell you if a named plate vanished.

## 4. The shelf work (the thread's active lane)

* The 4 tuned place-neutral themes are being walked to exhaustion across pixabay/mixkit/coverr
  in a 50-pass background run. **Trap measured this session**: `--cap-gb` is a CUMULATIVE cap
  against the whole archive total (1,417 GB), not a per-run download cap — any value below the
  archive total stops the run at pass 1 with "ARCHIVE CAP reached, 0 items". Run with no cap;
  the tier free-space floors still guard the disks.
* `anonymous_crowd` deny round 3 is IN the code (ingest_archive_sources.py CO_OCCUR, applied via
  pd_edit with a smoke import): dry-run titles showed place-specific (india/shiva, ukraine/pokrov)
  and child-adjacent (baby stroller) passing. Still owed: a REAL batch of ~12, then
  `py -3.11 scripts/qc_archive_contact_sheets.py --theme anonymous_crowd --refresh` and a human
  read of the sheet. The bar from 8/24: trust the theme only after a sheet reads ≥~55% usable.
* **Do not run two ingest processes at once** — the ledger has been corrupted by concurrent
  appends before (this lane's own memory). One at a time, always.
* 135 quarantined clips still pass the tuned gate and could be restored without downloading —
  but ~45% are still wrong; restore only after a sheet. (Unchanged from 8/24.)

## 5. Old-design debt, measured and left

`check_short_design.py --all`: 99 problems across short86-269 — scripts those old designs point
at have moved/renamed. Zero of them touch short289-309. Not this session's scope; recorded so
the number doesn't surprise anyone.

## 6. Token audit (rule 20)

`token_audit.py --live` at handover: average context 189,419 / peak 342,182 / amplification
263x / billed 37.2M. Design work (5 scripts read whole + 5 designs authored) is the honest cost
of doing provenance by hand; the next session should start clean at the audio 工程 if Shorts thaw.
