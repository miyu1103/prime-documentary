# Handover 2026-08-22 — the shorts + assets lane

This lane is **asset gathering (the archive shelf, its ledger, footage) and Shorts (upload,
scheduling, calendar)**. It does **not** touch long-form production, i2v, renders or the
long-form calendar — a separate thread owns those, and on 2026-08-20 the two lanes writing one
file destroyed 117 files' ledger rows. **Run one lane at a time.**

Everything below is measured, not remembered. Commands to re-measure are inline.

---

## 1. State at handover (2026-08-22 15:49)

```
shelf ledger      63,629 rows = 63,629 files on disk, 0 torn, 0 duplicated, 0 missing   PASS
usable video      15,815 clips with a commercial licence
Shorts scheduled  21, from 2026-08-22 18:00 JST through 2026-08-27 09:00 JST
Shorts backlog    47 finished Shorts on disk, not yet uploaded
stuck videos      0
quota today       81 units left (an upload costs 1,600) -- spent; resets 16:00 JST
network           1 live default route (Wi-Fi off) -- this is the safe state
running now       nothing
```

Re-measure all of it:

```
py -3.11 scripts/check_ledger_integrity.py          # ledger vs the actual files
py -3.11 scripts/yt_list_scheduled.py               # the live calendar, not a local file
py -3.11 scripts/fill_short_schedule.py --dry-run   # backlog + quota + which slots are next
pwsh -NoProfile -c "(Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Where-Object { (Get-NetAdapter -InterfaceIndex $_.ifIndex).Status -eq 'Up' } | Measure-Object).Count"
```

---

## 2. Shorts run themselves. Do not do this by hand.

`PD-ShortsPush` (Windows Task Scheduler) runs **daily at 16:20 JST**, twenty minutes after the
YouTube quota resets. Last run 2026-08-21 16:20, result 0. It uploads what the quota allows onto
free **6 / 9 / 18 / 21 JST** slots and reserves 1,650 units for the long-form chain.

**12:00 JST is the long-form slot and Shorts never go there.**

**A guard was added 2026-08-22: the task refuses to upload while two default routes are live**,
and exits 1 so a skipped day is visible in `LastTaskResult`. Reason in §4.

So the normal state of this lane is: **nothing to do.** Check the numbers, confirm the guard did
not refuse, go away.

---

## 3. The rule that decides whether shelf footage is usable

**Tight framing travels. A wide shot carries its place with it.**

A water surface, a raindrop on glass, a cloudscape and an anonymous hand are the same object
anywhere on earth. A hillside, a road, a building and an animal are not.

Measured on EP71 oroville, which is the proof and the worked example:

| | query set v001 | v002 (place-neutral) |
|---|---|---|
| terms | 101 | 56 |
| judged on contact sheets | 56 | 112 + 138 |
| **usable** | **3 (5 %)** | **48 (34 %)** |

v001 asked a global stock shelf for *places*. `animal` (422 hits, standing in for "cattle")
returned a snail, an owl, a labrador and a cartoon dog; `mountain` (228, standing in for
"low foothill") returned the Alps; `architecture` (135, standing in for "civic building")
returned a university library. **`cattle` itself measured 0.** The sheets showed Times Square,
Mount Fuji, a Croatian tractor field, green-screen money rain and sci-fi tunnel CGI.

**A hit count is not a supply count, and a supply count is not suitability.** Both episodes
declare `footage_review_required: true`; a person opens the contact sheets. The staging receipt
records *who looked* — it does not certify the pool is clean, and it says so in its own text.

Full record: `episodes/_planning/EP71_oroville_FOOTAGE_PLAN.v001.md` §10 and
`runs/qc/oroville_footage_review.v001.md` (which states plainly that 56 of 276 were judged, not
all of them).

**Corollary, measured and expensive:** a *theme* label is not a subject. Theme
`government_buildings` holds 1,061 usable videos and **30** carry a subject word in the title —
the rest are a German cathedral, an Israeli flag, Brexit news. Theme `small_town`: **0 of 585**.
And `stage_footage_by_title.py` matches the **title only**, so the theme field is invisible to
staging even when it is right. **Do not spend a night of bandwidth on `--theme
government_buildings` expecting a federal courthouse.** Subjects that need a place come from
plates, which is what the plate contracts exist for.

---

## 4. Four instruments that lied, and what each now does instead

Every one of these read as success. That is the pattern to expect.

| what lied | how it looked | fixed by |
|---|---|---|
| **two reindexers on one ledger** | 66,324 rows for 60,572 files — *fuller* than the shelf, `shelf_rows()` cheerfully non-zero, while 586 lines were torn and **117 files lost their row entirely** | `atomic_append` (the ingest lane's own helper) + `single_instance()` lock in `reindex_archive_shelf.py`. Shown refusing a second copy before being relied on |
| **a row count as an integrity check** | the number went up, so it looked healthy | `scripts/check_ledger_integrity.py` (new) compares the ledger to the FILES: torn / duplicate / missing. Shown FAILING on the damaged ledger first |
| **the manifest as proof of possession** | the restock would have downloaded nothing and printed `+0` | `build_factory_library.py` and `ingest_modern_web.py` now require the file to exist on disk. Measured: `88850 of 88850 manifest entries have NO FILE on disk` |
| **`publishAt` empty = stuck** | 2 live Shorts reported as UNSCHEDULED; acting on it would have re-scheduled published videos | `yt_list_scheduled.py` now reads the `privacyStatus` the API already returned. Output separates `already-published` from `private-with-no-date` |

And one that was not an instrument but a network:

**Two live default routes kill an upload mid-transfer, and YouTube accepts the metadata first.**
`qKzMltLYAjg` sat in Studio looking scheduled for 08-24 21:00 with nothing behind it and would
have published empty. EP69 hyatt aborted the same way at 1,334 MB of 1,645 MB. With one route,
five Shorts went through with zero drops, all five `processed/succeeded`.

**`fileDetails.fileSize` is the size the client DECLARED, not the bytes received.** It matched a
master to the byte on a transfer that had failed. Size agreement is not evidence.

---

## 5. Working rules this lane earned the hard way

1. **Ask the live API, then speak.** Channel state comes from `yt_video_status.py` /
   `yt_list_scheduled.py`, never from a local manifest or a cached audit. A cached
   `_yt_audit.json` was 8 hours stale and produced two wrong reports in one night.
2. **Never `tail` a list you are about to draw a conclusion from.** Reporting "the schedule runs
   dry on 08-24 18:00" was wrong because the last line was cut off; it ran to 21:00.
3. **A check that has never been shown to fail is decoration.** Every guard added here was
   demonstrated rejecting a deliberately bad input first.
4. **Count live adapters, not route-table rows.** A disconnected Wi-Fi leaves its row behind, and
   counting rows already produced a false refusal that stopped a healthy run.
5. **Never `git add -A`.** Two lanes share this repo; name the files.
6. **Uploads and deletions need the owner.** Reads do not.

---

## 6. Open items for the next thread

**Now**
- Nothing. The 16:20 task covers today. Confirm `LastTaskResult` is 0 tomorrow; if it is 1, read
  `runs/shorts_thumbs/daily_push.log` — most likely Wi-Fi came back and the guard refused.
- **Keep Wi-Fi off.** If it returns, the daily push stops (safely) and that day's 4 Shorts do not go out.

**Soon**
- Backlog is 47 Shorts, draining ~5/day: about **nine days of runway**. Nothing to do until it
  gets short, then more Shorts must be produced.

**Load-bearing and not yet fixed**
- **`H:` is `subst H: E:\`, not the recovered drive.** `subst` does not survive a reboot, and
  **339 scripts still hard-code `H:\pd-media`**. A reboot breaks all of them at once, with no
  obvious cause. Either make the subst persistent at logon or fix the paths.
- Five episodes owe an archive copy of their i2v masters
  (`runs/qc/*_i2v_archive_copy_pending.v001.txt` — hyatt, openfields, pinto, ramirez, wronghouse).
  They were written into the repo because the archive drive was absent.
- `forbidden_subjects` matches whole words, not stems: a clip titled **"shaking hands" walked
  past a `handshake` ban**. Harmless this time.

**Not this lane** — EP70 wronghouse rendered and FAILED acceptance with 13 hard failures
(39:59 against a 40:45 floor, plus motion density). EP71 oroville is `READY to build` with 118
plates and 48 staged clips and needs i2v. Both belong to the long-form thread.

---

## 7. Second session, 2026-08-22 16:00–18:00

### The line above that said "running now: nothing" was wrong

Three jobs in this lane were running when it was written: two copies of
`recover_pexels_shelf.py` (09:55 `--want-ep76`, 11:29 plain) and `ingest_modern_web.py`. The
ledger was being written at 16:11:32, during the integrity check that reported PASS.

**Two writers, and this script was the one that never got a lock.** The 2026-08-20 fix landed in
`reindex_archive_shelf.py`, `ingest_modern_web.py`, `ingest_archive_sources.py` and
`ingest_science_museum.py`. This one was missed. Nothing was torn — every row is written and
flushed one short line at a time — but `already_have()` is read once at start, so the two todo
lists overlapped and the same id could be written twice. And it bought nothing: Pexels allows
200 requests/hour, so two copies at 200/hour each hit 429 and back off. Measured throughput with
both running was 44–155 rows/hour: **the throughput of one copy for twice the monthly budget.**

### What changed

| | |
|---|---|
| `recover_pexels_shelf.py` → **`recover_stock_shelf.py`** | one script, `--source pexels\|pixabay`. A sibling would have copied the browse scan, theme map, tier placement, ledger row and lock |
| `single_instance()`, per source | shown refusing a locked ledger (exit 1) and releasing on a clean run |
| destination | was hard-coded `D:\pd-archive`; now `TIERS`, so it lands on E: (1,490 GB free vs D:'s 530) |
| `already_have()` | read ONE root and ONE filename prefix. Reported 1,399 pexels clips held when the ledger knew 1,434, and **0** pixabay clips when 668 were there under `pixabay_extra__v_<id>__` naming. Now reads every tier and the ledger, `.mp4` rows only |
| `pick_file()` | capped `width<=1920 AND height<=1080`, which **no portrait clip can satisfy**, then fell back to the LARGEST. Live proof: pixabay 359377 came down 2160x3840, 197.8 MB. Now caps long/short edge and falls back to the smallest — retested live at 1920x1080, 15.6 MB |
| `ensure_h_drive.ps1` + task **PD-EnsureHDrive** | recreates the H: alias at logon. Refuses if `E:\pd-archive` is absent: a wrong H: is worse than no H: |
| `fix_h_paths.py` | **247 tracked scripts rewritten** `H:\pd-media` → `E:\pd-media` |
| `.claude/pd-safety-policy.json` | `protected_paths` named `H:/pd-media/assets` only. The moment the code said E:, the guard stopped covering what it exists to cover. Both spellings listed now |

### Running now (really)

Both detached via `scripts/run_stock_recovery.ps1`, logs in `runs/recover_<source>.log`:

```
pexels   7,924 to fetch, ~40 h at the provider's 200/hour (EP76's 596 first, then the rest)
pixabay  5,663 to fetch, ~2 h at 50/min
```

Measured 30 minutes in: pexels +75, pixabay +87, all onto E:. Ledger still PASS at 63,985 files,
0 torn / 0 duplicate / 0 missing. Videos only — the owner chose that on 2026-08-22; **100,460
images are still missing and out of scope.**

### Three mistakes worth not repeating

1. **A process search matched its own PowerShell.** `Where CommandLine -match 'recover_stock_shelf'`
   matched the shell running that very query, and `Stop-Process` killed it mid-script — so the
   locks were never cleaned and the relaunch never happened. Exclude `$PID`.
2. **`Path.write_text` translated line endings.** All 385 rewritten files flipped LF → CRLF, and
   six were `.sh`, where CRLF makes bash fail on the first line. Repaired and re-checked with
   `bash -n`. The tool now uses `newline=""` on both ends.
3. **The rewrite hit prose.** Two docstrings ended up reading "E:\pd-media … H: is dead". Restored.

### Still open

- **473 `.json` files still say `H:`.** They are records of where a file *was* — manifests,
  ledgers, receipts. `fix_h_paths.py --include-json` when that decision is taken. Until then
  PD-EnsureHDrive is what keeps them resolvable.
- Untracked scripts were skipped (another lane owns them) and still say `H:`.
- `scripts/gen_short25_images.py` does not compile at HEAD either — `SyntaxError`, unclosed `[`
  at `SHOTS`. Pre-existing, unrelated, still broken.
- Disk: cleared 27.3 GB of temp and caches from C: (297.3 → 324.6 GB free). **Not touched, needs
  a decision:** `.git` 163 GB, `hiberfil.sys` 51 GB, Codex sessions 54 GB, Codex images 23 GB,
  Ollama 24 GB.
- Today's `PD-ShortsPush` ran at 16:20, result 0, five Shorts scheduled, no collisions. Backlog
  47 → 42.
