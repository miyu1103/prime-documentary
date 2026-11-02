# EP62-EP69 scheduling plan (v001)

Measured 2026-08-12 00:10-00:40 JST. **Read-only run: nothing was uploaded, no `publishAt` was
created or changed, no scheduled video was touched.** Every number below is followed by the command
that produced it. Where something could not be measured it says so instead of estimating.

Clock at time of measurement (`py -3.11 -c "... datetime.now ..."`):

```
UTC  2026-08-11T15:09:44+00:00
JST  2026-08-12T00:09:44+09:00
PT   2026-08-11T08:09:44-07:00
```

---

## 1. CHANNEL TRUTH

`scripts/yt_channel_index.py` is the union enumerator (uploads playlist ∪ `search.list?forMine`);
`scripts/yt_full_audit.py` calls it and dumps per-video status; `scripts/yt_list_scheduled.py` is
the only one of the three that reads `status.publishAt` (the full audit does **not** record it).

```
py -3.11 scripts/yt_full_audit.py
```

```
[yt_channel_index] indexes disagree: uploads playlist 141 unique (156 rows), search 156 -> using union of 156
[yt_channel_index]   missing from uploads playlist: 4iAGWU96CY4, ACS2lVlX_mQ, EOJ0UZpez2c, I2KsZdt94SI,
  J97Rh1qOTPA, Qyad4FejCIc, SC6_ClfusJ4, SpXTxT6nd24, WeWkj8ns_LI, YQIhk2dKZHU, _8DaMu8_yFw,
  bXATF9ZnKLE, bYcqabvvxak, ssvpqiFPM7k, tkWdCHhgrUI
=== CHANNEL ===
title       : Prime Documentary
subs        : 21
views       : 10789
videoCount  : 120
=== VIDEOS (156) ===
```

The uploads playlist still lies: **15 videos** are absent from it, including four of the five
long-forms already booked for this week. `videoCount: 120` from `channels.list` is the public count
only — it is not the total.

Counts (`py -3.11` over `scripts/_yt_audit.json`, written by the audit above):

| metric | value |
|---|---|
| total videos (union index) | **156** |
| public | **120** |
| private (all of them carry a future `publishAt`) | **36** |
| long-form (>185 s) total / public | 62 / 57 |

Every future `publishAt` (`py -3.11 scripts/yt_list_scheduled.py`, joined with the audit dump for
duration; `scheduled=36  private-with-no-date=0`):

| publishAt (JST) | kind | dur | video id | title |
|---|---|---|---|---|
| 2026-08-12 06:00 | short | 37s | ACS2lVlX_mQ | Police Broke In With a Warrant That Didn't Exist — Then Wh… |
| 2026-08-12 09:00 | short | 56s | SC6_ClfusJ4 | He was not even driving. He was the passenger #Shorts |
| **2026-08-12 12:00** | **LONG** | 29m38s | **J97Rh1qOTPA** | He Buried His Daughter at Nine. 408,000 Have Filed… (EP58 lejeune) |
| 2026-08-12 18:00 | short | 53s | ssvpqiFPM7k | His own words for it: scared, petrified, humiliated #Shorts |
| 2026-08-12 21:00 | short | 52s | EOJ0UZpez2c | The name the world knows him by was never even his #Shorts |
| 2026-08-13 06:00 | short | 54s | tkWdCHhgrUI | He did not pick that plane by accident… |
| 2026-08-13 09:00 | short | 58s | I2KsZdt94SI | One man handed regulators the arithmetic… |
| **2026-08-13 12:00** | **LONG** | 20m30s | **l7-oHSNEIjc** | Texas Executed Him for an Arson… (EP51 willingham) |
| 2026-08-13 18:00 | short | 57s | 4iAGWU96CY4 | In December 2008 he told his own sons… |
| 2026-08-13 21:00 | short | 56s | WeWkj8ns_LI | In 2002 someone finally did the one thing… |
| 2026-08-14 06:00 | short | 52s | WqUIxrBvKpM | He walked out in 2015… |
| 2026-08-14 09:00 | short | 55s | Fo1gLlPifPw | The Court did not say police can never follow you in… |
| **2026-08-14 12:00** | **LONG** | 30m07s | **67gynOvKf1M** | A 3-Year-Old Said His Father Wasn't Home… (EP52 morton) |
| 2026-08-14 18:00 | short | 54s | 2zg0ZjUD5JE | The baseline nobody states out loud… |
| 2026-08-14 21:00 | short | 56s | mbnLAkEGJbA | He won his freedom, then the Supreme Court took the money… |
| 2026-08-15 06:00 | short | 51s | 6BdWgVzEqjw | Louisiana set his execution date… |
| 2026-08-15 09:00 | short | 57s | ZOHr_I5mFso | The excuse came from a 1973 case about a car… |
| **2026-08-15 12:00** | **LONG** | 30m24s | **SpXTxT6nd24** | The Lab Cleared Her in Weeks. She Served Eleven Years. (EP61 weimer) |
| 2026-08-15 18:00 | short | 58s | WmlASZrzuPI | The Court did not say police can never come in… |
| 2026-08-15 21:00 | short | 54s | k0lOXQAcxaM | Regulators warned. Germany ordered it stopped… |
| 2026-08-16 06:00 | short | 47s | rh5kP-sLqtg | From the inside it could not be seen… |
| 2026-08-16 09:00 | short | 56s | XVIKwOTDLVc | In 1997 she sat down across from the man… |
| 2026-08-16 18:00 | short | 54s | Z7hoCi11NHg | The problem was never that she was not certain enough #Shorts |
| 2026-08-16 21:00 | short | 54s | eN5btn2-e6s | On 18 January 2012 the internet went dark… |
| 2026-08-17 06:00 | short | 57s | SSWm1bcb_A8 | Nobody ever proved what he meant to do… |
| 2026-08-17 09:00 | short | 59s | VfZpo-RqvtQ | Miranda was never one man's case… |
| 2026-08-17 18:00 | short | 1m00s | nclLM0R9gL0 | The most famous objection to the Mapp rule… |
| 2026-08-17 21:00 | short | 57s | XyvWOmjy0e4 | Get a warrant came with an off switch… |
| 2026-08-18 06:00 | short | 1m01s | OU0-K_JgDIE | The reason nobody needed a warrant… |
| 2026-08-18 09:00 | short | 1m00s | G0W4-iE756k | Carpenter was five to four… |
| **2026-08-18 12:00** | **LONG** | 32m11s | **oaFNcW0iDig** | One Wrong Initial Split Their House Into Two Accounts… (**EP64 memphis**) |
| 2026-08-18 18:00 | short | 58s | 9trRPk57RYo | Forfeiture works by filing the case against your property… |
| 2026-08-18 21:00 | short | 1m02s | M0nfXriWMJU | The unanimous win did not abolish forfeiture… |
| 2026-08-19 06:00 | short | 1m01s | cdt4nzt2XA0 | Justice O'Connor's dissent… |
| 2026-08-19 09:00 | short | 1m07s | Im1XjAwwqTw | Roughly forty states rewrote their eminent domain laws… |
| 2026-08-19 18:00 | short | 1m05s | s9yTEiQwiNo | The school's entire case rested on disruption… |

Episode identity of the five booked long-forms was resolved by matching the video ids against
`episodes/*/09_package/youtube_schedule_result*.json`.

**EP64 memphis is already uploaded and scheduled** (`oaFNcW0iDig`, 2026-08-18 12:00 JST,
private + publishAt, thumbnail set, captions uploaded, receipt written 2026-08-11T10:00:54Z).
It must not be uploaded again — see §4.

---

## 2. FREE 12:00 JST SLOTS — next 14 days from 2026-08-12

Derived from the same measured `publishAt` set. Shorts (06/09/18/21 JST) never touch 12:00, so no
short collides with a long-form on any day below.

| date | 12:00 JST slot | who takes it |
|---|---|---|
| 2026-08-12 (Wed) | TAKEN | J97Rh1qOTPA — EP58 lejeune (29m38s) |
| 2026-08-13 (Thu) | TAKEN | l7-oHSNEIjc — EP51 willingham (20m30s) |
| 2026-08-14 (Fri) | TAKEN | 67gynOvKf1M — EP52 morton (30m07s) |
| 2026-08-15 (Sat) | TAKEN | SpXTxT6nd24 — EP61 weimer (30m24s) |
| 2026-08-16 (Sun) | **FREE** | — |
| 2026-08-17 (Mon) | **FREE** | — |
| 2026-08-18 (Tue) | TAKEN | oaFNcW0iDig — **EP64 memphis** (32m11s) |
| 2026-08-19 (Wed) | **FREE** | — |
| 2026-08-20 (Thu) | **FREE** | — |
| 2026-08-21 (Fri) | **FREE** | — |
| 2026-08-22 (Sat) | **FREE** | — |
| 2026-08-23 (Sun) | **FREE** | — |
| 2026-08-24 (Mon) | **FREE** | — |
| 2026-08-25 (Tue) | **FREE** | — |

Shorts coverage measured per day (collision check): 08-12…08-15 and 08-18 each have 06/09/18/21;
08-16, 08-17 and 08-19 have 06/09/18/21 or fewer, none at 12:00. **No shorts collision exists.**

---

## 3. QUOTA

There are **two** quota ledgers in this repo and they disagree. The one the uploader actually gates
on is `check_api_budget.py`.

**(a) `scripts/yt_quota.py` — the call-counting ledger (`runs/_cache/yt_quota.json`)**

```
py -3.11 scripts/yt_quota.py
```

```
Pacific date 2026-08-11 | spent 5188 of 10000 | remaining 4812
  search.list              35 calls    3500 units
  commentThreads.insert    33 calls    1650 units
  commentThreads.list      34 calls      34 units
  videos.list               4 calls       4 units

uploads still possible today: 3 (videos.insert costs 1600 each)
```

Today's Pacific date **as the API sees it: 2026-08-11**. Reset is midnight Pacific = **16:00 JST**
(confirmed independently below). The 3,500 `search.list` units are the hand-recorded entry noted on
2026-08-11; nothing else self-records — `topic_demand_probe.py` does not, and
`upload_schedule_case_v001.py` contains **no** call to `yt_quota.record` (`grep -n
"yt_quota\|record(\|assert_budget" scripts/upload_schedule_case_v001.py` returns nothing). This
ledger therefore **misses the EP64 memphis upload made at 19:00 JST 08-11**.

**(b) `scripts/check_api_budget.py` — the receipt-mtime ledger, and the actual gate**

```
py -3.11 scripts/check_api_budget.py
```

```
[budget] quota day began 2026-08-11 16:00 local, resets 16:00
  1 upload(s) (video + thumbnail + captions)      2050
  spent (from this repo's own receipts)           2050
  remaining                                       7950
[budget] room for about 3 more upload(s) at 2050 units each
```

Reset time in JST: **16:00 JST** (both tools agree; `check_api_budget` prints it from the real
Pacific midnight, `yt_quota` uses `zoneinfo America/Los_Angeles`).

**Measured cost of one upload**, read off the code path in `upload_schedule_case_v001.py` (published
unit table applied to the calls the script actually makes):

| call | where | units |
|---|---|---|
| `search.list` (duplicate pre-check, `forMine`, 1 page) | `_search_mine` before anything else | 100 |
| `channels.list` (budget probe) | `check_api_budget.reads_still_work` | 1 |
| `channels.list` (`get_channel_id`, allowlist) | after dry-run gate | 1 |
| `videos.insert` (resumable, `part=snippet,status`, publishAt in body) | `initiate_upload` | 1600 |
| `thumbnails.set` | `set_thumbnail` | 50 |
| `captions.insert` | `upload_caption` | 400 |
| `videos.list` verify × 1–3 | `get_state` retry loop | 1–3 |
| `videos.update` status change | **not used** — publishAt is set in the insert body | 0 |
| **total** | | **2,152 – 2,154** |

`check_api_budget` models this as 2,050 (it omits the 100-unit duplicate search and the reads), so
its "3 fit" is one upload optimistic.

**How many uploads fit:**

* **Today (quota day 2026-08-11 PT, ends 16:00 JST 2026-08-12):** the gate will pass up to
  **3**. Honest arithmetic says fewer: 5,188 recorded reads + 2,050 memphis upload + ~411 units this
  read-only audit spent (4 `search.list` pages = 400, 4+1 `videos.list` chunks, 2 `channels.list`)
  ≈ **7,649 spent, ~2,351 left → 1 upload**. It does not matter today: **nothing is upload-ready**
  (§5), so no upload should be attempted before the 16:00 JST reset.
* **Each subsequent day, ceiling:** 10,000 ÷ 2,152 = **4 uploads/day** if nothing else touches the
  API.
* **Each subsequent day, realistic:** measured non-upload traffic on the current quota day is
  5,188 units (shorts comments + audits), leaving 4,812 → **2 uploads/day**. Plan on 2.
* The ledger drifts high by its own docstring; only an observed `quotaExceeded` 403 is ground truth.

---

## 4. THE EXACT COMMAND

`.claude/rules/19-ship-gate.md` (verbatim, binding): a long-form is never scheduled until an
independent gate measures the real render's bytes and emits a green receipt; scheduling happens
**only** through `upload_schedule_case_v001.py --ep <slug>`; and it only goes out when the receipt's
`video_sha256` matches the file and the tolerated hard failure is `runtime_band` alone (the single
owner-approved channel-wide deviation).

**Invocation (one episode):**

```
py -3.11 scripts/upload_schedule_case_v001.py --ep greene --dry-run   # verify first, no external writes
py -3.11 scripts/upload_schedule_case_v001.py --ep greene             # the real booking
```

`--ep` is `choices=sorted(CONFIG)`. All eight slugs already exist in CONFIG with dates:

```python
"greene":     PD-2026-062-greene     2026-08-16T12:00:00+09:00 / 2026-08-16T03:00:00Z
"correa":     PD-2026-063-correa     2026-08-17T12:00:00+09:00 / 2026-08-17T03:00:00Z
"memphis":    PD-2026-064-memphis    2026-08-18T12:00:00+09:00 / 2026-08-18T03:00:00Z   # ALREADY DONE
"marmet":     PD-2026-065-marmet     2026-08-19T12:00:00+09:00 / 2026-08-19T03:00:00Z
"openfields": PD-2026-066-openfields 2026-08-20T12:00:00+09:00 / 2026-08-20T03:00:00Z
"ramirez":    PD-2026-067-ramirez    2026-08-21T12:00:00+09:00 / 2026-08-21T03:00:00Z
"pinto":      PD-2026-068-pinto      2026-08-22T12:00:00+09:00 / 2026-08-22T03:00:00Z
"hyatt":      PD-2026-069-hyatt      2026-08-23T12:00:00+09:00 / 2026-08-23T03:00:00Z
```

These dates land exactly on the free 12:00 JST slots from §2. **No CONFIG date needs editing.**

**Preconditions it enforces, in execution order:**

1. CONFIG entry is built from `09_package/youtube_meta.v001.json`; missing `title`/`description`/
   `tags` → `SystemExit`. (Title/description/tags are never duplicated in the script.)
2. **Duplicate pre-check** — `search.list?forMine&order=date&maxResults=50`; if any video carries
   the byte-identical title it refuses and tells you to use `finalize_uploaded_video.py` or
   `--replaces <id>`. Three attempts; if the check *cannot run*, it refuses rather than proceeding
   ("not knowing whether a duplicate exists is not the same as knowing there is none").
3. `09_package/youtube_schedule_result.v001.json` must not exist → `Refusing duplicate`.
   With `--replaces VIDEO_ID` the receipt is written to the next free `v00N` instead, and the
   superseded video must already be `private` with **no** `publishAt` or it refuses.
4. All four files must exist: `08_edit/<slug>_final_bgm.v001.mp4`, newest
   `09_package/thumbnail.selected.v*.png`, captions (newest `08_edit/captions.youtube.v*.srt`,
   else `captions.final.v001.srt`), newest `09_package/final_delivery.v*.json`.
5. `sha256(video)` must equal `final_delivery.canonical_final.video_sha256`.
6. Thumbnail < 2 MB.
7. `check_api_budget.py --need 1` must exit 0.
8. `check_shipped_frames.py --slug <slug> --render <mp4>` must exit 0 — a human/vision verdict of
   PASS recorded in `runs/qc/<slug>_shipped_frames.v001.json` **and bound to these exact bytes**.
9. **Acceptance hard lock:** newest `09_package/acceptance_receipt.v*.json` must exist, its
   `video_sha256` must equal the sha of this file, and every entry in `hard_failures` must be inside
   `ALLOWED_DEVIATIONS`.
   `ALLOWED_DEVIATIONS = {"runtime_band"} ∪ accepted_deviations` from that episode's
   `approvals/*.json` where `target_type == "edit"` and `decision` starts with `approved`.
10. `sched_utc` must be in the future — checked twice (once before the dry-run return, once inside
    `initiate_upload`). A past `publishAt` publishes immediately and publicly; this is why even a
    dry-run fails on a stale date.
11. Channel id must be in `CHANNEL_ALLOWLIST`.

**`--dry-run`: yes.** It runs steps 1–11 and prints `DRY_RUN_OK no external writes`. It is **not
free**: the duplicate `search.list` (100) and the budget probe (1) fire before the dry-run return,
so a dry-run costs ≈101 quota units.

**On success** it uploads private with `publishAt` in the insert body, sets the thumbnail, uploads
captions (a caption failure is a warning only), re-reads status up to 3× with 10 s gaps to defeat
read-after-write lag, and only then writes `youtube_schedule_result.v001.json`.

---

## 5. THE BOOKING PLAN

Readiness measured per episode (files on disk, receipts, approvals, QC verdicts). Render+gate wall
time measured from `out_finish_ep62_65.log`: greene 1h43m, correa 2h23m, memphis 2h25m,
marmet 2h09m — **~2h10m per episode**, one at a time (the GPU takes one job).

Queue order in `scripts/queue_unattended.sh` (read-only inspection, not modified):
`marmet, greene, correa, openfields, ramirez, pinto, hyatt` — memphis is deliberately absent.
`film.json` is newer than the mp4 for all seven, so the queue will render every one of them
(measured mtimes).

| # | episode | proposed publishAt (JST) | upload must happen | what still blocks it |
|---|---|---|---|---|
| 0 | **EP64 memphis** | **2026-08-18 12:00 — ALREADY BOOKED** (`oaFNcW0iDig`) | done 2026-08-11 19:00 JST | **Nothing. Do not run `--ep memphis` again** — `youtube_schedule_result.v001.json` exists and the title is live, so the script refuses twice over. |
| 1 | EP62 greene | 2026-08-16 12:00 (CONFIG, slot free) | by 2026-08-15 | Re-render pending in queue (film.json 08-11 01:46 > mp4 08-10 17:15). Then: **`final_delivery.v*.json` does not exist** (`write_final_delivery.py --slug greene`); new acceptance receipt bound to the new bytes; **shipped-frames verdict is FAIL** — rejection at 10:35, `AR-8847832 person_holding_papers` = a modern US election ballot. That asset id no longer appears in the current `greene_film.json` (grep = 0), so the re-render should clear it, but a fresh review of the new bytes is still required. Receipt hard failures (`animation_density, sound_layers, padding, asset_reuse, preflight_receipt`) are **all covered** by APR-0002 + APR-0003. |
| 2 | EP63 correa | 2026-08-17 12:00 (CONFIG, slot free) | by 2026-08-16 | Same shape. Re-render pending (film.json 08-11 20:57 > mp4 08-10 22:17). **`final_delivery` missing**; new receipt; **shipped-frames FAIL** — 15:10-15:14 `AR-v_120266` is present-day Seoul (Lotte World Tower, Hangul signage). Grep = 0 in the current film.json. Hard failures (`animation_density, sound_layers, asset_reuse, preflight_receipt`) all covered by APR-0002 + APR-0003. |
| 3 | EP65 marmet | 2026-08-19 12:00 (CONFIG, slot free) | by 2026-08-18 | **Render is running right now** (`out_finish_marmet.log` at stage `[3/4] RENDER Ep65Marmet`). After it: new `final_delivery` (current one names sha `c4e967…` while the newest receipt names `8aeed8…` — they already disagree), new receipt, new shipped-frames review (current verdict FAIL: cut-0006 at 0:47-0:51 shows an **identifiable real minor**, `AR-10159563`; grep = 0 in the current film.json). **Extra blocker unique to marmet:** its approvals carry only APR-0001/APR-0002, which do **not** include `animation_density` — greene/correa/memphis have APR-0003 for that and marmet does not. If the new receipt still lists `animation_density`, the ship gate hard-fails and an owner approval is required. |
| 4 | EP66 openfields | 2026-08-20 12:00 (CONFIG, slot free) | by 2026-08-19 | Never rendered — no `*_final_bgm.v001.mp4`, no receipt, no delivery. `check_episode_inputs.py --slug openfields` = **READY to build** (191 stills, 191 factory clips, 26.7 min narration; warns `asset_reuse will FAIL`, which is a covered deviation on 62-64 but has **no approval on file for 66-69**). Then the full chain: render → receipt → `write_final_delivery` → shipped-frames review. |
| 5 | EP67 ramirez | 2026-08-21 12:00 (CONFIG, slot free) | by 2026-08-20 | Same. `READY to build` (146 stills, 107 clips, 26.7 min). No approvals directory at all, so `ALLOWED_DEVIATIONS` is `{runtime_band}` only — any other hard failure blocks. |
| 6 | EP68 pinto | 2026-08-22 12:00 (CONFIG, slot free) | by 2026-08-21 | Same. `READY to build` (123 stills, **only 42 distinct clips** vs ~265 footage cuts — the worst reuse of the eight). No approvals directory. |
| 7 | EP69 hyatt | 2026-08-23 12:00 (CONFIG, slot free) | by 2026-08-22 | Same. `READY to build` (127 stills, 146 clips, 28.3 min). No approvals directory. |

**Collisions:** none. The only already-scheduled date inside this run is **2026-08-18**, taken by
EP64 memphis itself — which is correct, not a conflict. Every other CONFIG date (08-16, 08-17,
08-19 … 08-23) is a measured-free 12:00 JST slot.

**Pacing against quota:** 7 uploads remain, spread over 8 calendar days, at ≤1 upload/day. The
realistic ceiling is 2 uploads/day (§3), so **quota is not the binding constraint — the gates and
the single-GPU render queue are.**

**Critical-path arithmetic (measured, not estimated):** 7 renders × ~2h10m ≈ **15.2 GPU-hours**
before the last episode even has bytes to gate, and each one then needs a human/vision shipped-frames
review that cannot be automated away. The first deadline (greene, upload by 08-15) has ~4 days of
slack. The last (hyatt, upload by 08-22) has ~10 days. Both fit — provided the queue is left alone
and the shipped-frames reviews keep pace with the renders.

**Two things that will silently bite if not handled:**

1. `write_final_delivery.py` is **not** part of `_finish_episode.sh` — greene and correa both have a
   finished master and no delivery record, which is exactly the "first scheduling attempt died on
   `missing final_delivery`" failure its own docstring describes. It must be run per episode after
   every re-render.
2. EP65-EP69 lack an `animation_density` / `asset_reuse` approval that EP62-64 have. The gate will
   hard-fail on deviations the earlier episodes were allowed, and no amount of re-rendering changes
   that — it needs an owner approval record, or the deviation genuinely fixed.
