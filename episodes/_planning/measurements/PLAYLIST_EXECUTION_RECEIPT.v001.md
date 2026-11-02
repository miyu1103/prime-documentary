# PLAYLIST EXECUTION RECEIPT v001

Execution of `episodes/_planning/measurements/PLAYLIST_PLAN.v001.json` against the live
channel under approval **APR-0006** (owner, 2026-07-28, 「①→実行して」).

| | |
|---|---|
| channel | `UCuQPtAz1rca9eJ4xhvX0yKA` (allowlist-checked before the first write) |
| design revision | `v001` / `config/distribution/series_clusters.v001.json` (status `approved`) |
| approval record | `APR-0006` |
| executor | `scripts/yt_playlist_executor.py`, invoked only through the guard chain in `scripts/plan_series_playlists.py` |
| run 1 | 2026-07-28T01:12:38.123587+00:00 |
| completed | 2026-07-28T01:17:09.711298+00:00 |
| status | **completed** |
| write calls | **45** (approved maximum 46) |
| write quota | **2250 units** (approved 2300) |
| read calls | 93 (93 units - verification reads, not in the plan's estimate) |
| total quota | **2343 units** of the 10,000/day allowance |
| failed calls | 0 |
| retries | 0 |
| endpoints touched | playlistItems, playlists - nothing else |

Guards all held: `--execute` + `--owner-approval APR-0006` + exact `--confirm` phrase +
`config.status == approved` + zero validation errors. Each was re-tested as refusing before
the run (wrong phrase, missing phrase, unknown approval id, missing approval id all exit 4).

## 1. Final verified state (read back from the API after execution)

| playlist id | title | items | position 0 (entry point) | privacy |
|---|---|---|---|---|
| `PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9` | Police Power: What They Can Actually Do to You | 18 | `tpAKfHKuwqY` | public |
| `PLd04glUie5rg` | The Forfeiture Files: When the Government Takes What's Yours | 7 | `Xc_PxdC_75c` | public |
| `PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P` | Fraud, Finance & Power | 9 | `sphERPA4gAc` | public |
| `PLfPI0t-nSRxw` | The System Got It Wrong | 8 | `marQjsCagh0` | public |

- <https://www.youtube.com/playlist?list=PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9>
- <https://www.youtube.com/playlist?list=PLd04glUie5rg>
- <https://www.youtube.com/playlist?list=PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P>
- <https://www.youtube.com/playlist?list=PLfPI0t-nSRxw>

Independent verification (a separate reader, not the executor's own code) re-read the
channel and passed **51/51** checks:

- exactly 4 playlists exist on the channel; each title, description and privacy matches the approved design
- each playlist's full order equals the approved order exactly (18 / 7 / 9 / 8 items)
- `contentDetails.itemCount` from the API agrees with the counted items in all 4
- position 0 of each playlist is the approved entry-point video
- positions are contiguous 0..n-1; no duplicate video inside any playlist
- 42 memberships, 42 distinct videos, no video in two playlists
- the covered set equals the 42 public long-forms exactly (0 missing, 0 extra)
- no deleted/private placeholder item remains in any playlist
- all 42 playlisted videos resolve as live and public

Re-running the executor after completion performed **0 writes** (idempotency proven on the
live channel, not only in simulation).

## 2. Every call, in execution order

`playlistItems.insert`/`update` rows are the item-level steps; each was followed by a
`playlistItems.list` read-back that confirmed the intended video occupies the intended index
before the next call was issued. A mismatch would have aborted the run.

| # | playlist | operation | target | index | result | returned id |
|---|---|---|---|---|---|---|
| 1 | police_power | `playlists.update` | title/description | - | was 'Landmark Rights Cases', read back OK | `PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9` |
| 2 | police_power | `playlistItems.delete` | `PjGEqW6F9WM` (Deleted video) | was 0 | deleted, verified gone | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 3 | police_power | `playlistItems.insert` | `tpAKfHKuwqY` | 0 | inserted at 0, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 4 | police_power | `playlistItems.insert` | `bXATF9ZnKLE` | 1 | inserted at 1, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 5 | police_power | `playlistItems.insert` | `Sz8zPUoBANM` | 2 | inserted at 2, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 6 | police_power | `playlistItems.update` | `bYcqabvvxak` | 3 | moved from 5, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 7 | police_power | `playlistItems.insert` | `XWYWAgkExH4` | 4 | inserted at 4, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 8 | police_power | `playlistItems.insert` | `YQIhk2dKZHU` | 5 | inserted at 5, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 9 | police_power | `playlistItems.insert` | `zE3nCUlUmLY` | 6 | inserted at 6, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 10 | police_power | `playlistItems.insert` | `rrftLmSVivk` | 7 | inserted at 7, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 11 | police_power | `playlistItems.insert` | `68oWZRiOnB8` | 8 | inserted at 8, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 12 | police_power | `playlistItems.update` | `An0to4U0hJQ` | 9 | moved from 10, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 13 | police_power | `playlistItems.insert` | `Enok7A7wGBA` | 10 | inserted at 10, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 14 | police_power | `playlistItems.insert` | `g5yFmDt48oU` | 11 | inserted at 11, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 15 | police_power | `playlistItems.insert` | `gR_nzXIyIlk` | 12 | inserted at 12, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 16 | police_power | `playlistItems.insert` | `SOu4Y1NkGGY` | 13 | inserted at 13, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 17 | police_power | `playlistItems.insert` | `X40EbUw5kzQ` | 14 | inserted at 14, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 18 | police_power | `playlistItems.update` | `cQFql7tT1fE` | 15 | moved from 16, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 19 | police_power | `playlistItems.insert` | `cSfe3iGnBBM` | 17 | inserted at 17, verified | `UExLY3JNM3g0ZzFoOXVCNF9QREpR...` |
| 20 | forfeiture_files | `playlists.insert` | The Forfeiture Files: When the Government Takes What's Yours | - | created, read back OK | `PLd04glUie5rg` |
| - | forfeiture_files | `playlists.update` | - | - | skipped (already matching) | - |
| 21 | forfeiture_files | `playlistItems.insert` | `Xc_PxdC_75c` | 0 | inserted at 0, verified | `UExkMDRnbFVpZTVyZy41NkI0NEY2...` |
| 22 | forfeiture_files | `playlistItems.insert` | `6ozsIfwqrP0` | 1 | inserted at 1, verified | `UExkMDRnbFVpZTVyZy4yODlGNEE0...` |
| 23 | forfeiture_files | `playlistItems.insert` | `rU2vk9XL4vY` | 2 | inserted at 2, verified | `UExkMDRnbFVpZTVyZy4wMTcyMDhG...` |
| 24 | forfeiture_files | `playlistItems.insert` | `YhEJHK279f8` | 3 | inserted at 3, verified | `UExkMDRnbFVpZTVyZy41MjE1MkI0...` |
| 25 | forfeiture_files | `playlistItems.insert` | `m-uWzgWHGPg` | 4 | inserted at 4, verified | `UExkMDRnbFVpZTVyZy4wOTA3OTZB...` |
| 26 | forfeiture_files | `playlistItems.insert` | `4uuY6G0LmHo` | 5 | inserted at 5, verified | `UExkMDRnbFVpZTVyZy4xMkVGQjNC...` |
| 27 | forfeiture_files | `playlistItems.insert` | `89SQoRgAD7U` | 6 | inserted at 6, verified | `UExkMDRnbFVpZTVyZy41MzJCQjBC...` |
| 28 | fraud_finance_power | `playlists.update` | title/description | - | was 'Fraud, Finance & Power', read back OK | `PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P` |
| 29 | fraud_finance_power | `playlistItems.update` | `sphERPA4gAc` | 0 | moved from 1, verified | `UExLY3JNM3g0ZzFoOGY0QTRQTkpM...` |
| 30 | fraud_finance_power | `playlistItems.insert` | `vikfOBHullI` | 1 | inserted at 1, verified | `UExLY3JNM3g0ZzFoOGY0QTRQTkpM...` |
| 31 | fraud_finance_power | `playlistItems.insert` | `LXFjJqE6vKU` | 2 | inserted at 2, verified | `UExLY3JNM3g0ZzFoOGY0QTRQTkpM...` |
| 32 | fraud_finance_power | `playlistItems.insert` | `mj9qEKPRatE` | 3 | inserted at 3, verified | `UExLY3JNM3g0ZzFoOGY0QTRQTkpM...` |
| 33 | fraud_finance_power | `playlistItems.insert` | `j8U8c4BB_GQ` | 4 | inserted at 4, verified | `UExLY3JNM3g0ZzFoOGY0QTRQTkpM...` |
| 34 | fraud_finance_power | `playlistItems.insert` | `5Jap-0h43A4` | 5 | inserted at 5, verified | `UExLY3JNM3g0ZzFoOGY0QTRQTkpM...` |
| 35 | fraud_finance_power | `playlistItems.insert` | `1pox44KsaV8` | 6 | inserted at 6, verified | `UExLY3JNM3g0ZzFoOGY0QTRQTkpM...` |
| 36 | fraud_finance_power | `playlistItems.insert` | `rYV4rxtQCV0` | 8 | inserted at 8, verified | `UExLY3JNM3g0ZzFoOGY0QTRQTkpM...` |
| 37 | system_got_it_wrong | `playlists.insert` | The System Got It Wrong | - | created, read back OK | `PLfPI0t-nSRxw` |
| - | system_got_it_wrong | `playlists.update` | - | - | skipped (already matching) | - |
| 38 | system_got_it_wrong | `playlistItems.insert` | `marQjsCagh0` | 0 | inserted at 0, verified | `UExmUEkwdC1uU1J4dy41NkI0NEY2...` |
| 39 | system_got_it_wrong | `playlistItems.insert` | `Qyad4FejCIc` | 1 | inserted at 1, verified | `UExmUEkwdC1uU1J4dy4yODlGNEE0...` |
| 40 | system_got_it_wrong | `playlistItems.insert` | `5L_HCGJxX_U` | 2 | inserted at 2, verified | `UExmUEkwdC1uU1J4dy4wMTcyMDhG...` |
| 41 | system_got_it_wrong | `playlistItems.insert` | `tYZuE76Hwdc` | 3 | inserted at 3, verified | `UExmUEkwdC1uU1J4dy41MjE1MkI0...` |
| 42 | system_got_it_wrong | `playlistItems.insert` | `Pmh6h5SfWw4` | 4 | inserted at 4, verified | `UExmUEkwdC1uU1J4dy4wOTA3OTZB...` |
| 43 | system_got_it_wrong | `playlistItems.insert` | `tt7U1XgjCU4` | 5 | inserted at 5, verified | `UExmUEkwdC1uU1J4dy4xMkVGQjNC...` |
| 44 | system_got_it_wrong | `playlistItems.insert` | `1h267U6PY0I` | 6 | inserted at 6, verified | `UExmUEkwdC1uU1J4dy41MzJCQjBC...` |
| 45 | system_got_it_wrong | `playlistItems.insert` | `FTm1icKgycU` | 7 | inserted at 7, verified | `UExmUEkwdC1uU1J4dy5DQUNERDQ2...` |

Write totals by operation: `playlistItems.delete` x1, `playlistItems.insert` x36, `playlistItems.update` x4, `playlists.insert` x2, `playlists.update` x2.
All 45 returned HTTP 200/204 on the first attempt (0 retries, 0 failures).
The full request/response log with per-call ids and timestamps is in
`episodes/_planning/measurements/PLAYLIST_EXECUTION.v001.json` (`call_log`).

## 3. The DELETE

- **outcome: executed, exactly one, as approved.**
- playlist: `PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9` (the reused "Landmark Rights Cases" playlist)
- playlist item id: `UExLY3JNM3g0ZzFoOXVCNF9QREpRTlVFWDJvTlVtQVpaOS41NkI0NEY2RDEwNTU3Q0M2` - resolved live; the plan's url was the placeholder `<playlistItemId for PjGEqW6F9WM - re-read at execution time>`
- video id: `PjGEqW6F9WM`, item title `Deleted video`, position `0`

Three independent proofs were required before the DELETE was sent, all of which passed:

1. the item sat at **position 0** (the slot every playlist link lands on) - any other position aborts;
2. `videos.list?id=PjGEqW6F9WM` returned **zero items**, i.e. the video really is deleted - if the video had existed, the run would have aborted without deleting;
3. the item title was the placeholder string `Deleted video`.

After the DELETE, a re-read confirmed both the item id and the video id are absent from the
playlist. Post-run verification re-confirmed `PjGEqW6F9WM` is still a deleted video, i.e.
nothing live was removed. Both abort paths were exercised against a simulated API before the
live run (a live video behind the placeholder, and a placeholder at a non-zero position);
both aborted with **zero** DELETE calls sent.

## 4. Deviations from the plan

### 4.1 The plan's literal call order would not have produced the approved order (corrected)

**This is the material finding.** `PLAYLIST_PLAN.v001.json` computed every `position`
argument against the pre-write state, then listed all inserts before all reorders. A
`playlistItems.insert` at position N shifts every later item down by one, so the plan's
positions do not survive its own inserts. Replaying the 46 calls literally (simulated
offline, no writes) leaves `police_power` wrong from index 3 onward:

```
idx  3  got XWYWAgkExH4  want bYcqabvvxak
idx  4  got YQIhk2dKZHU  want XWYWAgkExH4      ... 13 items shifted ...
idx 15  got bYcqabvvxak  want cQFql7tT1fE
```

`bYcqabvvxak` (Terry) would have stranded at index 15 instead of 3. `fraud_finance_power`
happened to survive; `police_power` did not.

The plan anticipates this in its own text - it annotates item ids and the delete url as
"re-read at execution time" - so the executor resolves positions live: it walks each
playlist's approved order index by index, re-reading the live item list before every
decision, and inserts or moves whichever video belongs at the cursor. Indices below the
cursor are already final, so each write is the only one that can put the right video in
place, and the read-back proves it did. The end state is exactly the approved design in
`series_clusters.v001.json`, which is what the owner approved; only the arithmetic used to
reach it was recomputed. Op types, target playlists and target videos are unchanged, and
the run stayed inside the approved envelope.

### 4.2 45 writes instead of 46 (one fewer than approved)

| operation | planned | executed |
|---|---|---|
| `playlists.insert` | 2 | 2 |
| `playlists.update` | 2 | 2 |
| `playlistItems.insert` | 36 | 36 |
| `playlistItems.update` | 5 | 4 |
| `playlistItems.delete` | 1 | 1 |
| **total** | **46** | **45** |

The plan's 5th reorder moved `waA4XJ9bYcE` (FTX) from position 0 to 7 in
`fraud_finance_power`. Inserting the seven videos ahead of it carried it to index 7 on its
own, so the explicit move was unnecessary and was not sent. Write quota consumed is
**2250 units against the approved 2300**; the run is under budget, never over. The
executor also enforces the approved count as a hard cap and aborts rather than exceed it.

### 4.3 Verification reads are additional quota (expected, not in the plan's number)

The plan's 2,300 units counted writes only. Verify-then-proceed adds 93 read units
(1 unit each), for **2343 units total** across both runs - 23% of one day's 10,000-unit
allowance. Cheap insurance: it is what proved every write landed.

### 4.4 The two new playlist ids were NOT written back into the approved config

The plan notes that a created playlist's id must reach
`config/distribution/series_clusters.v001.json` before the description batch runs, or the
WATCH NEXT links 404. That config is an owner-approved artifact and CLAUDE.md invariant 6
forbids overwriting one in place, so the executor did not edit it. The ids are recorded in
`PLAYLIST_EXECUTION.v001.json` (`playlist_ids`) and here:

- `forfeiture_files` -> **`PLd04glUie5rg`** (The Forfeiture Files: When the Government Takes What's Yours)
- `system_got_it_wrong` -> **`PLfPI0t-nSRxw`** (The System Got It Wrong)

**Follow-up required before the description batch:** create a `v002` revision of the config
carrying these two ids. That batch is a `videos.update` workload and is explicitly *not*
approved by APR-0006.

### 4.5 No other deviation

No call touched a video title, description, thumbnail, visibility, schedule, chapter,
comment or end screen. The scope fence rejected every endpoint except `playlists` and
`playlistItems`, was applied to the whole plan before the first write and re-applied to each
outgoing request, and the recorded log confirms only those two endpoints were contacted.

## 5. Rollback

- The two created playlists: `playlists.delete` on `PLd04glUie5rg` and `PLfPI0t-nSRxw`. No live description links them yet, so nothing is stranded.
- The two reused playlists' metadata: re-PUT the `was_title` / `was_description` captured per step in `PLAYLIST_EXECUTION.v001.json`.
  - `police_power` was titled `Landmark Rights Cases`
  - `fraud_finance_power` was titled `Fraud, Finance & Power`
- Inserted items: `playlistItems.delete` on the `playlist_item_id` recorded for each insert step.
- Reordered items: re-PUT the `was_position` recorded for each update step.
- The deleted placeholder is not restorable, and needs no restoring: it pointed at a video that no longer exists.

## 6. Files

| file | role |
|---|---|
| `scripts/yt_playlist_executor.py` | new - the executor (scope fence, verify-then-proceed, resume, retry, budget cap) |
| `scripts/plan_series_playlists.py` | the `--execute` path now calls the executor past the unchanged guard chain |
| `episodes/_planning/measurements/PLAYLIST_EXECUTION.v001.json` | machine state: every completed step, returned ids, full call log |
| `episodes/_planning/measurements/PLAYLIST_PLAN.v001.json` | marked `executed: true` with timestamp and approval id |
| `episodes/_planning/measurements/PLAYLIST_EXECUTION_RECEIPT.v001.md` | this receipt |

_Generated from `PLAYLIST_EXECUTION.v001.json`; every figure above is read from the recorded run, not transcribed._
