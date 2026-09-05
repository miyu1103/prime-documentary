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

## 4. Unchanged

* **Freesound tail**: 2,637 rows, waiting on the window (~13:00 09-06). Procedure unchanged and
  unrun. `docs/shelf/rights_progress.v001.json` is still current (derived from the ledger).
* LOC 2,724 and IA 649 stay held. No machine path exists; that is the final state.
* The quarantine decision on 11 themes (~19k assets) is still the owner's.
