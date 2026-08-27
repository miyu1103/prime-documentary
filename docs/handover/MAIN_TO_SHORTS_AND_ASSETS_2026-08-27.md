# → shorts + assets lane, 2026-08-27 — the ingest no longer dies with your session

Your 2026-08-26 handover, §9, ends with this warning:

> **It will die with this session too** — check it is alive before assuming the shelf grew.

That is fixed. The ingest is a Windows scheduled task now, it survives closing the chat and it
survives a reboot. Everything below was measured tonight with the command printed beside it.

---

## 1. Why it kept dying, and the second reason nobody had measured

Two separate failures were stacked on top of each other.

**The one you found:** a foreground `py -3.11 scripts/ingest_archive_sources.py ...` is a child of
the session and dies with it. Today alone, three runs died mid-theme:

```
runs/ingest_video_deep_20260827.log    last line 18:59:58   theme=itaewon_korea_night
runs/ingest_video_deep_20260827b.log   last line 20:35:19   theme=bench_to_line
runs/ingest_video_deep_20260827c.log   last line 21:42:18   theme=chicago_city
```

No traceback in any of them. They stop mid-theme, which is what a killed process looks like.

**The one nobody had measured:** there *was* a scheduled task, `PD-Ingest-IA`, and it had been
failing every single time it fired. Its registered action was:

```
cmd /c cd /d C:\Users\aab15\Documents\prime-documentary && python -u scripts\ingest_archive_sources.py
    --source ia --tiers H,D >> H:\pd-media\assets\archive\_ledger\ingest_run1.log 2>&1
```

`H:` is a `subst` alias for `E:` and **it does not exist after a reboot**, so the redirect target
was unwritable and `cmd` exited before Python ever started. Measured:

```
Get-ScheduledTask -TaskName 'PD-Ingest-IA' | Get-ScheduledTaskInfo
  LastRunTime    : 2026/08/27 19:06:49
  LastTaskResult : 1
```

So the safety net was there the whole time, reporting `result=1`, and the lane was compensating by
hand-launching foreground copies that died. That is also why `--tiers H,D` was in it — a tier flag
naming a drive that evaporates.

## 2. What is registered now

`scripts/install_ingest_task_admin.ps1` re-registered the same task name (replaced, not added — a
second task is how you get two writers). Verified action:

```
cmd /c cd /d "C:\Users\aab15\Documents\prime-documentary" && py -3.11 -u scripts\ingest_archive_sources.py
    --source ia,nasa,coverr,mixkit --theme all --limit 200 --passes 20
    >> runs\ingest_scheduled.log 2>&1
```

| | |
|---|---|
| triggers | **AtStartup** (so a reboot restarts it) + **daily 03:07** as a safety net |
| multiple instances | `IgnoreNew` — a second fire while one is running is dropped, not queued |
| execution time limit | none (`TimeSpan::Zero`) — it will not be killed at 72 hours |
| log | `runs\ingest_scheduled.log`, repo-relative, **on C:, not on the subst alias** |
| working dir | the repo, so no tier flag and no absolute media path in the command |
| run level | `Limited`, `S4U` — runs without you being logged in, no stored password |

Same args your §9 recipe used, so this is your run, made durable — not a different run.

## 3. The handoff was done tonight, and it is live

There was still a foreground copy alive (**PID 43412**, started 20:36, identical args). Two writers
on one ledger is what corrupted it before, so it was stopped before the task was started. Safe to
kill: the ledger append is a single atomic write and `(source,id)` pairs already recorded are
skipped on resume, so a kill costs listing calls, not downloads.

```
[08-27 22:01:21] run start: sources=['ia','nasa','coverr','mixkit'] themes=46 limit=200 passes<=20
[08-27 22:01:21] resume state: 128008 items in ledgers, 1791.3GB total (E:669.8 D:706.0 F:415.5)
[08-27 22:01:21]   tier E: free 564GB / floor 250GB     D: 377/250     F: 511/50
[08-27 22:32:48] [p1:ia] theme=prison_jail
```

One process, **PID 5136**, owned by the task. `LastTaskResult 267009` = still running.

Ledger integrity, run separately after the handoff:

```
py -3.11 scripts/check_ledger_integrity.py
  rows parsed 129,735 | distinct file_path 129,735 | torn lines 0 | duplicated files 0
  media files on disk 129,735 | files with NO row 0
  PASS -- the ledger describes the shelf exactly once
```

Note these are **two different counters** and should not be added together or compared: `128,008`
is the ingest run's own resume state across its per-source jsonl ledgers, `129,735` is the shelf
ledger at `E:\pd-archive\_ledger` checked against files on disk. Both are healthy; they measure
different things.

## 4. The one rule this changes for your lane

**Do not launch `ingest_archive_sources.py` from a chat session again.** The script has no lock of
its own. A hand-launched copy running alongside the task is a second writer, and the task's
`IgnoreNew` cannot see it — that guard only applies to task instances.

Replace the §9 recipe with these three:

```powershell
Get-ScheduledTask -TaskName 'PD-Ingest-IA' | Get-ScheduledTaskInfo   # 267009 = running
Get-Content 'C:\Users\aab15\Documents\prime-documentary\runs\ingest_scheduled.log' -Tail 5
Start-ScheduledTask -TaskName 'PD-Ingest-IA'                          # only if not running
```

If you genuinely need a one-off run with different flags, stop the task first
(`Stop-ScheduledTask -TaskName 'PD-Ingest-IA'`) and start it again when you are done.

## 5. Two things this does NOT do, said plainly

* **It does not make the shelf good, only bigger.** `check_ledger_integrity` proves every file has
  exactly one row. It reads no pixels. The mislabelled-shelf problem is untouched — `evidence_bag`
  returning cartoons is not something a row count can see, and the ingest's own contact sheets are
  the only thing between it and another batch of wrong material. Keep looking at them.
* **It does not settle whether the IA lane should be on at all.** On 2026-08-10 four ingest tasks
  were disabled on the finding that the shelf was already large enough. Right now `PD-Ingest-IA` is
  the only one back on; `PD-Ingest-Gov`, `PD-Ingest-Science`, `PD-Ingest-Web` and `PD-TikTokPush`
  are still `Disabled`. Tonight's work made the running lane durable; it did not re-open that
  decision. If the answer is that collecting is finished, the whole change is one line:

  ```powershell
  Disable-ScheduledTask -TaskName 'PD-Ingest-IA'
  ```

  and the ledger keeps its resume state, so it costs nothing to turn back on later.
