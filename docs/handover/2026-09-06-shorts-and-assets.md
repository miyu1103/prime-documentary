# Handover 2026-09-06 — the assets lane

Continues [2026-09-05](2026-09-05-shorts-and-assets.md). Nothing was scheduled for this session —
the Freesound tail waits for its 24-hour window (~13:00 today). A routine liveness check turned
into two findings, one of them my own mistake.

---

## 1. The ingest is alive and producing almost nothing

Measured from the ledger (`fetched_at`, assets actually taken, rejects excluded):

```
2026-08-31  ia 13   nasa 7
2026-09-01  ia 1
2026-09-02  ia 1    nasa 1
2026-09-03  nasa 1
2026-09-04  (none)
2026-09-05  ia 1
2026-09-06  (none)
```

**Four assets in the last four days**, against a shelf of 130,285. The only ledger file written
since 09-05 10:51 is `rejects_ia.jsonl` (81 MB). Every source ledger except that one is hours or
days stale: `nasa.jsonl` last grew 09-04 05:31.

This is the evidence the owner's open question needed ("IA収集そのものを続けるか"). The shelf is
full; the machine is now buying rejects.

## 2. The oversized-download defect (fixed, `194ba2f1`)

`runs/ingest_scheduled.log` for the three hours before the check held nothing but this:

```
[09-05 22:55:12]   dl-fail: file exceeds MAX_ITEM_BYTES: .../SpaceX_Crew_9_Live_Launch_Coverage...
[09-05 23:11:30]   dl-fail: file exceeds MAX_ITEM_BYTES: ...
[09-06 00:26:03]   dl-fail: file exceeds MAX_ITEM_BYTES: ...
```

15-19 minutes apart, because **the size guard fired after the bytes had already been pulled**.
`Net.download` counts as it streams and raises once the counter passes `MAX_ITEM_BYTES` (2 GB) —
so each rejection cost up to 2 GB of bandwidth and a quarter-hour of the run. The IA path never
does this: it pre-filters on the size in the item metadata (line ~1620). The NASA path has no
size to filter on — `images-api.nasa.gov/asset/<id>` returns hrefs only — so it always paid full
price. **239 oversized rejections all time, every one of them NASA.**

Fix: read `Content-Length` off the streaming response before touching the body. Three lines, and
it covers every source rather than the NASA path alone.

Demonstrated both directions against live URLs:

```
oversized (4K Crew-9 coverage)  REJECTED in 2.6s, 0 bytes written to disk
normal (Apollo AS11-40-5874)    ACCEPTED, 74,132 bytes, sha 984655f1b493
```

## 3. The trap I walked into: `Stop-ScheduledTask` does not kill the child

**This is now the state of the machine and it needs one elevated command to clear.**

To make the fix take effect I stopped and restarted `PD-Ingest-IA`. The restart failed instantly,
`LastTaskResult = 1`, and **nothing at all was appended to the log** — which reads exactly like the
old vanishing-`H:` failure from 08-27 and is not that.

What actually happened:

* `Stop-ScheduledTask` killed the `cmd.exe` wrapper (PID 60696, now gone) and left its child
  **`py -3.11` PID 20496 → `python3.11` PID 53416 alive**, started 09-05 13:42:59.
* That orphan still holds `runs\ingest_scheduled.log` open. The task's action is
  `cmd /c ... >> runs\ingest_scheduled.log`, so every new instance dies before Python starts:
  `The process cannot access the file because it is being used by another process`.
* The orphan cannot be killed from a normal session. `taskkill /F /T`, `Stop-Process` (sandbox
  off) and `schtasks /end` all return access denied or report success without killing it — the
  process lives in the task's **S4U logon session**. Registering a temporary task with an S4U
  principal to kill it from inside that session is itself refused without admin.

**Silver lining, and the reason nothing is at risk:** the file lock is why no second writer could
start. The ledger still passes — `check_ledger_integrity.py`: 130,285 rows, torn 0, duplicated 0,
files with no row 0. There is exactly one writer, as there should be.

**To clear it, in an elevated PowerShell:**

```
taskkill /F /T /PID 20496          # or: Get-Process py,python3.11 | Stop-Process -Force
Start-ScheduledTask -TaskName 'PD-Ingest-IA'
```

Do NOT start the task while 20496 lives — the lock is currently the only thing preventing two
writers on one ledger. If the owner decides to stop collecting instead, killing the orphan IS the
stop, and the restart line is simply not run (`Disable-ScheduledTask -TaskName 'PD-Ingest-IA'`
keeps it off; resume state survives).

## 4. The stills had no way in, and now they do

The one open item in this lane that was not blocked was the owner's quarantine decision on the
eleven rotten themes. Preparing it produced the number that decides it:

```
                     video   reachable by meaning   image   reachable by meaning
the 11 themes         5,891   5,887 (99.9%)        13,073   0
```

`index_footage_semantic.py` globbed `*.mp4` and `*.mov`, so every one of its 30,470 entries was a
clip. **For a still, the rotten theme label was the only way in** — and those are the labels the
eye review found describing something other than their contents. That is why theme names keep
getting used despite the canon saying not to: for images there was no alternative.

`--images` (commit `64e219ad`) extends the same indexer — same CLIP model, same vector space, a
separate index so the clip index is never disturbed — over **87,558 shelf stills**. Started 10:17
on the GPU. `--sheet` (commit `5c45a8ab`) tiles any query's hits through the existing contact-sheet
builder, because a retrieval score is not evidence that the picture is right.

Two things found on the way:

* **The `ai_video` exclusion never existed in code.** The file header has said since August that
  generated material is "deliberately left out"; nothing implemented it. It happened to be true —
  0 of the 30,470 indexed paths — and would have stopped being true on the next rebuild. Now
  enforced in `_excluded()` for `ai_video`/`ai_image`/`ai_gen`/`synthetic`.
* **My own count was wrong and the correction matters.** The first pass said 19,378 assets and
  95.6% video reachability. It counted 414 rows whose files already sit in
  `E:\pd-archive\_quarantine` from an earlier `quarantine_theme.py` run; the indexer excludes
  `_quarantine` by design, so they read as an indexing hole when they were the opposite. Corrected
  in `docs/shelf/QUARANTINE_DECISION.v001.md` (`f16c535e`). `anonymous_crowd` exposed it: 291 of
  its 302 assets were quarantined months ago.

**It finished the same morning.** 87,542 stills embedded; 16 skipped as unreadable — exactly the
16 truncated JPEGs yesterday's integrity sweep already knew about, two instruments agreeing
without being told to. The clip index was caught up in the same pass (989 videos the shelf had
gained since 08-25; now 31,455 of 31,459). Semantic side index: **30,470 → 118,997**.
`build_asset_usability.py` reads both, so `in semantic search` is now true for stills, and the
whole record was rebuilt (130,285 assets).

Re-measured: **images went 0 → 13,073 of 13,073 reachable by meaning.** The quarantine decision's
one real cost is now zero.

Then it was tested by looking, not by scoring:

* **"a uniformed police officer"** returned real officers, where `police_modern` held **zero** in
  its 20 sampled tiles. But the readable ones are Japanese, British, Chinese and European, plus a
  carnival costume — **the shelf's real police are mostly not American**, and a query that does
  not say so will not say so. Same defect that put Shenzhen and a Chinatown market into EP74.
* **"an American courthouse exterior with columns"** returned **12 of 12 genuine American
  courthouses** — Texarkana, Belzoni, Sioux City, Milwaukee County, Louisville, Jackson TN, several
  with the flag in frame. `courtroom_justice` had one courthouse in twenty; the shelf had these all
  along, under labels nobody would search. **7 of the 12 are `loc__` and every LOC row is RIGHTS
  HOLD** — the item API was re-tested today and still answers 403. The best pictures this shelf has
  of the channel's own subject are the ones it may not use.

The decision packet is `docs/shelf/QUARANTINE_DECISION.v001.md`. With C done, it recommends
guarding theme-name selection — at `factory_ledger_themes.select()`/`tier_of()`, not on the
`--theme` flag, and demonstrated biting before it is relied on. Do not delete:
`atmosphere_symbolic` is 40% on-label, the material is real and the label is what failed. The
packet also maps every entry point a guard needs, including that **there are two shelves with two
ledgers and `quarantine_theme.py` cannot reach the factory one**, which is the shelf that actually
serves episodes.

## 5. A trap that returns success with no output

`subprocess.run(capture_output=True, text=True)` decodes the child with the **locale** codec —
cp932 on this machine. A child that prints Japanese raises `UnicodeDecodeError` **inside
subprocess's reader thread**, where `run()` never sees it. The call returns **returncode 0 with
`stdout=None`**. Exit zero, output gone, nothing raised.

Found because `--sheet` crashed on `r.stdout.strip()`. Fixed there with
`encoding="utf-8", errors="replace"`.

Measured repo-wide: **116 of 1,112 scripts print non-ASCII, and 33 of them are invoked from a
caller that uses `capture_output` with `text=True`** — including the ship path
(`pd_ship_policy.py`, `check_final_acceptance.py`, `upload_schedule_case_v001.py`). One was
checked by hand: `pd_ship_policy.py:381` reads `check_spec_satisfied.py` this way and **fails
closed** on an unreadable answer, so it would over-block rather than under-block. **The other 32
are measured, not verified** — this is the build/ship lane's to judge, not this one's, and it is
recorded here rather than fixed across 269 files by a lane that does not own them.

## 6. Unchanged

* **Freesound tail**: 2,637 rows, waiting on the window (~13:00 09-06). Procedure unchanged and
  unrun. `docs/shelf/rights_progress.v001.json` is still current (derived from the ledger).
* LOC 2,724 and IA 649 stay held. No machine path exists; that is the final state.
* The quarantine decision on 11 themes (~19k assets) is still the owner's.
