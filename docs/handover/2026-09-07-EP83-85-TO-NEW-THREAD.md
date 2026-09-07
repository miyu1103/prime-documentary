# HANDOVER — EP83/84/85 to a new thread (2026-09-07 19:10 JST)

You are taking over the **build/publish lane for EP83 max737, EP84 threemile, EP85 katrina**.
Everything except rendering is done. Read the four commands below before believing anything here.

```
py -3.11 scripts/handover_snapshot.py
cat runs/gpu_handoff_83_85.heartbeat          # which episode the chain is on
tail -c 300 out_render_max737.mp4.retry.log | tr '\r' '\n' | grep -oE "(Rendered|Encoded) [0-9]+/[0-9]+" | tail -1
py -3.11 scripts/check_episode_inputs.py --slug <slug>
```

---

## 1. The job in one sentence

Get all three episodes to a **master on disk with a green shipped-frames review**, then stop.
**Do not run `--book`.** The owner asked explicitly for *bookable*, not *booked*, because YouTube
quota (1,650 units per long-form, resets 16:00 JST) is the bottleneck and booking can move to
whichever session has quota.

---

## 2. State at handover, measured 19:08

| | EP83 max737 | EP84 threemile | EP85 katrina |
|---|---|---|---|
| inputs | READY* | READY | READY |
| cards | 73, **0 overlaps** | 69, **0 overlaps** | 74, **0 overlaps** |
| captions | lead 0.0 | lead 0.0 | **lead 0.30** (was failing p90 +0.415s vs +0.35s) |
| packaging | title/thumb/desc present, claims check PASS | same | same |
| stock pool | 42 (11 new aviation) | 71 (15 new nuclear/river) | 80 (18 new levee/flood) |
| master | **rendering now** | queued | queued |

\* max737 reads "NOT READY -- only 8 stills / 25 factory" **and that is normal**. `[5/7]` moves
everything the last film did not cut into `<pool>_unused`; `[0/7]` moves it back. Measured now:
`factory 25 + 17 unused = 42`, `img 8 + 394 unused = 402`. Do not "fix" this.

**EP83 is at 51,364 / 53,455 frames on its second attempt.** The first attempt rendered all
53,455 frames and then FFmpeg died at `Encoded 42764/53455` with exit code `3221225794`
(`STATUS_DLL_INIT_FAILED` — a Windows resource failure, not a content bug). `pd_render_guarded.sh`
retried automatically at `--concurrency=4`, which is the documented mitigation. If it dies the same
way again, that is the thing to investigate, and a reboot is the usual cure — ask the owner first,
another lane is using this machine.

---

## 3. The one thing that will bite you: the GPU

**Another thread's EP86 columbia i2v chain and these renders want the same 4090, and it has
changed hands four times today.** Measured with both running: the render fell from ~350
frames/min to 124, and once to 38. With the card to itself: **751 frames/min**.

- `scripts/_runcopy/hold_gpu_lock.sh` takes the project's own `out_gpu_comfy.lock` so the i2v
  chain declines politely instead of being killed. It was **demonstrated working** — a columbia
  chain launched against it printed `REFUSING: 'longform-renders-EP83-85' is driving ComfyUI`.
- **It did not hold.** As of 19:08 the lock reads `1080773 columbia` while the holder process is
  still alive and visible to `kill -0`, i.e. the other side overwrote it.
- The previous session stopped fighting after the fourth round. **Do not start round five by
  killing their chain** — every kill destroys that chain's in-flight clip, and it comes back.
  Either the owner tells that lane to stand down, or you accept the slower rate.
- Trap worth knowing: writing a **Windows** pid into that lock does nothing. The chain validates
  with `kill -0`, which is an **MSYS** pid, so a Windows pid reads as stale and gets deleted.

---

## 4. What is running right now

```
pid 42692  scripts/_runcopy/gpu_handoff_83_85_r4.sh   the supervisor: max737 -> threemile -> katrina, one at a time
pid 68420  scripts/_runcopy/finish_max737_gpu1.sh     EP83's finisher
pid 60964  scripts/_runcopy/hold_gpu_lock.sh          holds the GPU lock (currently overridden)
```

The supervisor relaunches the columbia i2v chain itself when the last master is built, so that
lane resumes with no action from anyone. It counts finished clips, so nothing it made is lost.

**The supervisor's harness wrapper was killed earlier, so no completion notification arrives from
it.** `scripts/_runcopy/watch_handoff.sh` exists to provide one: it watches the heartbeat for a new
`DONE`/`FAIL` line and exits. Run it in the background, or check the heartbeat yourself.

---

## 5. Per-episode: exactly what to do when a master lands

For each slug as its master appears at `episodes/PD-2026-08N-<slug>/08_edit/<slug>_final_bgm.v001.mp4`:

```
py -3.11 scripts/check_shipped_frames.py --slug <slug> --sheets-only --force
#   -> ~50 contact sheets under runs/qc/<slug>_shipped_frames/
#   READ EVERY SHEET. Then write, by hand:
#   runs/qc/<slug>_shipped_frames_review.v001.json
#     { reviewed_sheets: [FULL PATHS of every sheet], render_sha256: "<sha of the master>",
#       verdict: "PASS", reviewer: "...", reviewed_at: "..." }
bash scripts/ship_episode.sh ship <slug> <NN>
# STOP HERE. No --book.
```

**Read the master twice.** A second pass on an earlier episode found 13 cuts the first missed.

---

## 6. What was fixed today, so you do not re-fix it

1. **Cards drew on top of each other.** `build_figures` staggers, then the AE de-collision pass
   runs afterwards and pushes cards onto their neighbours. EP83 v6 shipped seven pile-ups —
   6.0 s of "THE 737 MAX WAS DESIGNED TO LAND ON LEVEL B" printed through "DECEMBER 2011. A
   CONTRACT WITH THE LAUNCH CUSTOMER." Timing is now settled once, at the end, over the list that
   ships. `scripts/check_card_overlaps.py` proves it at `[4e]`, before any GPU is spent.
   **The AI disclosure is not exempt** — two attempts to pin it both made it less readable.
2. **Stock was placed by cadence, not meaning.** The solver lays cuts on a fixed `F/M/F/M/F/S`
   rhythm and fills each stock slot from a queue in pool order. That is why a coffee-shop laptop
   sat under "Same aeroplane. Same fault. Same wheel." and ducklings under "the company was never
   convicted of lying to the regulator". `scripts/assign_stock_by_meaning.py` now permutes stock
   among the slots it already occupies when a clip's words match the line by **two or more** (at
   threshold 1 it churned). Wired into the finisher.
3. **The pools had no subject footage at all.** EP83's forty stock clips contained **not one
   aircraft**. 97 candidates were fetched from Pexels/Pixabay and **all 97 were opened**; 44 staged,
   53 refused. `scripts/build_candidate_sheets.py` exists so the next fetch is reviewed in the same
   order — candidates first, pool second.
4. **The blocklist prune ran after the restore, too late.** `[0/7]` restores `<pool>_unused`
   wholesale, which is exactly where a newly blocked clip is sitting, and the input pre-flight
   refused on them before `[2b/7]` was reached. Prune now runs right after the restore as well.
5. **`fill_short_schedule.py`** scans forward from today instead of anchoring on the newest
   long-form booking (that anchor left 09-04 and 09-05 with zero shorts).

---

## 7. Traps this session actually hit

- **`pgrep -f` is blind in Git Bash on Windows.** A queue that waited on
  `pgrep -f finish_max737_v7.sh` fired in the same second it started and rendered two episodes in
  parallel. Wait on a **file**, or on `Get-CimInstance Win32_Process`.
- **`pd_render_guarded.sh` retries.** Killing a render's node processes makes it start again a
  minute later. Kill the whole tree (`*Ep84ThreeMile*`, `*public_ep84*`, the bash wrappers) or it
  comes back.
- **Harness background wrappers can be killed while the bash processes survive.** Check with
  `Get-CimInstance Win32_Process` before concluding a job died.
- **Never edit a shell script while bash is executing it** (already canon; still true).
- Real airliner footage almost always carries a livery. That is *why* EP83's pool had no aircraft.
  Expect to refuse roughly half of any aviation fetch.

---

## 8. Shorts (not blocking, but yours now)

- 94/94 funnel-green, **68 in stock**, `short254` booked for 09-08 21:00 JST.
- `fill_short_schedule.py --dry-run` currently refuses with *"channel dump does not know about
  these uploads"* — that is just a stale truth file after my booking. Fix:
  `py -3.11 scripts/yt_full_audit.py && py -3.11 scripts/yt_list_scheduled.py`, then re-run.
- Cap is 4/day at 06:00 / 09:00 / 18:00 / 21:00 JST.

---

## 9. Parked owner decisions (unchanged)

1. Readable third-party brands in two **already published** episodes (norfolk, postoffice).
2. 20 kinetic cards lost across 15 published episodes.
3. EP86-88 slate approval — the previous recommendation was Columbia / El Faro / Purdue, and
   another thread is designing EP86+ now.

---

## 10. Honest limits of what was verified

- The card-overlap, caption-sync, packaging-claims and input checks are **machine-measured** and
  green. Quote them freely.
- The stock selection is **one reviewer's eyes** (mine) on four frames per clip. Nothing here
  proves a clip is clean at every second of its duration — that is what the shipped-frames read
  after the render is for, and it has not happened yet for any of the three.
- **No master from today's fixed build exists yet.** The three `*_final_bgm.v001.mp4` files on
  disk are from 05:41, 07:10 and 12:14 and predate every fix above. Do not ship them.
