# Handover 2026-08-24 — the shorts + assets lane

This lane is **asset gathering (the archive shelf, its ledger, footage) and Shorts (design,
upload, scheduling)**. It does not touch long-form production, i2v, renders or the 12:00
long-form slot — a separate thread owns those, and the two threads talk through
`docs/handover/MAIN_TO_SHORTS_*` and `SHORTS_TO_MAIN_*`.

Everything below is measured. Commands are inline.

---

## 1. State at handover

```
recovery, video      pexels 9,373 and pixabay 6,331 unique ids -- COMPLETE, both kinds
recovery, images     STOPPED by owner decision (see §3)
shelf                121,902+ files, ledger PASS, 0 torn / 0 duplicate / 0 missing
Shorts scheduled     26, publishing through 2026-08-31
Shorts backlog       32 built and unposted
Shorts push          PAUSED until 2026-08-29 (config/shorts_pause.v001.json, self-expiring)
Shorts delivered     short289-294 (EP70 wronghouse, EP71 oroville) -- 6 of the 21 asked for
quarantine           1,481 place-neutral downloads + 239 AI-generated clips
```

Re-measure:

```
py -3.11 scripts/check_ledger_integrity.py
py -3.11 scripts/recover_stock_shelf.py --source pexels --kind video --plan
py -3.11 scripts/fill_short_schedule.py --dry-run
py -3.11 scripts/yt_list_scheduled.py
```

## 2. The thing that made the day long: five one-way ratchets

Every stall today had the same shape — a controller that could go one direction and not back.
They are worth knowing as a family, because a sixth will look new and will not be.

| what ratcheted | how it showed | fixed by |
|---|---|---|
| the adaptive pace | 4 workers each reported ONE refusal, halving the pace four times: 1200 to 75 in a breath | one incident per 30 s |
| the recovery of that pace | doubling walked straight back into the ceiling, 150→300→600→1200→refused→75 | +10 % at a time |
| `known_bad_gap` | every refusal remembered a pace as permanently unsafe; a transient at 150/hour lowered the ceiling to 130, the next to 65 | forgotten after 20 clean minutes |
| a dead connection pool | 58 RemoteDisconnected in 60 lines while a fresh client got 10/10; the pacer only speeds up after a SUCCESS, so all-failures had no way back | drop the Session, retry the WHOLE item |
| my first fix for that | re-ran the metadata call, printed "recovered", then failed the clip without downloading it | attempt the item twice, not the call |

Net effect, measured from the ledger: **12:00–17:00 produced zero items** and nobody noticed
until the owner asked. `PD-WatchStockRecovery` (every 15 min) now restarts a lane whose ledger
has not moved for 25 minutes; shown detecting and restarting before being registered.

## 3. Images are out of scope, and the measurement that decided it

Across the 52 finished films:

```
stock VIDEO    6,781 cuts   43.6 %   <- the spine of every film
plates         5,620 cuts   36.1 %
i2v            2,794 cuts   18.0 %
stock IMAGES       0 cuts    0.0 %
```

Zero. Shorts use plate-derived PNGs; thumbnails likewise; the only references to a stock image
filename anywhere in the repo are five lines of prose in `docs/` and `decisions/`. The owner's
call: *"画像は最悪作れるからそんなになくてもいい"*. The 23,700 remaining Pexels images are not
being fetched. **The half that gets used is complete.**

## 4. The gate, and why "more footage" is not the same as more footage

Volume was never the problem. On 2026-08-23 five place-neutral themes pulled 1,481 clips
overnight, and a contact sheet said `night_road_lamp` had returned Brooklyn Bridge, a
rice-terrace night view and five CGI loops — 0 of 12 usable. All 1,481 are quarantined.

Three rounds of tuning, each read off a sheet rather than guessed:

```
word matching only           ~8 % usable
full phrase required          0 % admitted   <- Pixabay titles are comma-separated tags
tag co-occurrence            ~32 %
co-occurrence + deny lists   ~55 %
```

The phrase rule failed for the same reason the Pexels rate probe failed earlier: **it was
validated against titles I wrote, not titles the sources return.** A test that does not
reproduce the real input measures the test.

`CO_OCCUR` in `ingest_archive_sources.py` holds the rules; the deny lists are written from what
sheets actually returned. Still open: `anonymous_crowd` reads 2/5 and needs another round.

## 5. AI-generated footage was reachable in search

Found by reading one clip's own title: `ai generated, figure, hallway`. Measured across 31,186
shelf videos, **259 carry an AI marker in their own metadata, and 179 sat under themes a
documentary draws from** — courtroom_justice, police_modern, government_buildings, legal_court,
forensics_dna — including **47 under itaewon_korea_night while EP74 was in production**.
Staging one is invariant 11.

239 quarantined (`quarantine_theme.py --title-regex`). The 73 under abstract, vfx, particle and
light are left: a generated graphic IS the subject there. **0 remain reachable under a
real-subject theme.**

## 6. Names, so staging can find things

`stage_footage_by_title.py` matches the FILENAME and nothing else. 5,638 files were named
`pixabay__<id>__id.mp4` — the slug was the literal string "id" — while their titles sat one
field away in the ledger. Renamed 5,521 (117 skipped: referenced by name in `runs/qc/` staging
records that another lane is still building from).

```
water / river   2,436 -> 3,203      sky / cloud   2,221 -> 3,082
forest / tree   2,147 -> 2,707      night / lamp  1,241 -> 1,580
```

`recover_stock_shelf.py` now names from the API title when the browse slug carries no words, so
no future batch needs this.

## 7. Shorts

`short289-291` (EP70 wronghouse) and `short292-294` (EP71 oroville) are delivered — lines files
written, `check_short_design.py` 0 problems, 165-180 words against the measured 159-180 band.

`check_short_constraints.py` is new and reads the episode's **highest** spec revision via
`check_episode_spec.spec_path`. That mattered immediately: EP70 has only v001, but **EP71 is
v002 and EP75 is v003**, and the ad-hoc check that preceded it named v001. It also prints the
prose `forbidden_claims` it cannot match and refuses to imply it did — EP70 has 23, EP71 has 27,
and both sets were read by hand against the Shorts.

Remaining: **EP72-76, 12 Shorts, short295-309.**

## 8. Open

- `anonymous_crowd` still returns a bus and a dog at 2/5. One more deny round before trusting it.
- 135 quarantined clips now pass the tuned gate and could be restored without downloading
  anything — but ~45 % of them are still wrong, so restore only after a sheet.
- `.git` is 168 GB, 158 of it loose objects. `PD-GitGC` runs 03:30 and skips while anything
  heavy is running; it has not had an idle night yet.
- `gen_short25_images.py` does not compile at HEAD either. Pre-existing.
- 473 `.json` files still say `H:\pd-media`. They are records of where a file was;
  `fix_h_paths.py --include-json` when that decision is taken. `PD-EnsureHDrive` covers them.
