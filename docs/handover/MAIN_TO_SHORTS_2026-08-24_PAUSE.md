# Main thread → Shorts lane, 2026-08-24 (third note)

**Pause the Shorts push for four days — 25, 26, 27 and 28 August. Owner's decision.**
Nothing published disappears. Spend those four days building the EP70–76 Shorts instead.

---

## 1. Why this costs nothing, measured

Twenty-seven Shorts are **already uploaded and already carry a `publishAt`**. They publish on
their own; no further quota, no further push, no human.

```
py -3.11 scripts/yt_schedule_audit.py
```

| date | Shorts already booked |
|---|---|
| 2026-08-24 | 3 |
| 2026-08-25 | 4 |
| 2026-08-26 | 4 |
| 2026-08-27 | 4 |
| 2026-08-28 | 4 |
| 2026-08-29 | 4 |
| 2026-08-30 | 4 |

**Pausing the push stops UPLOADS, not PUBLICATIONS.** Every one of those 27 goes out as booked.
The first day a pause could actually cost a slot is **8/31** — and 8/31 is already empty whether we
pause or not, because the booked run ends on 8/30. Nothing is lost by stopping; the cliff is in the
same place either way.

## 2. What the freed quota buys

6,600 units a day × 4 days = **26,400 units** returned to the pool.

A long-form upload is 1,650, and `publishAt` can name any future date, so uploading early is not
publishing early — it is **banking the slot**:

```
8/25 16:05   EP71, EP74, EP75, EP76   4 x 1,650 = 6,600   -> booked for 8/26, 8/27, 8/28, 8/29
8/26 16:05   EP72, EP73               2 x 1,650 = 3,300   -> booked for 8/30, 8/31
```

**Two days, six episodes, the long-form calendar filled through 31 August.** After that the films
publish themselves and nobody has to be at a keyboard at 16:00.

This matters because of what happened today. EP71 oroville was finished at 05:00 — master rendered,
61 shipped-frame sheets read tile by tile, thumbnail selected, packaging at zero unsupported claims,
dry run green — and it did not go out, because the day's allowance was gone by 16:20 and the reset
comes at 16:00, after the 12:00 slot it was meant to fill. **8/25 12:00 is empty and cannot be
filled.** Banking the slots is how that stops being possible.

## 3. What to do with the four days

**Build the EP70–76 Shorts.** From this morning's brief
(`docs/handover/MAIN_TO_SHORTS_2026-08-24.md`), unchanged and now urgent:

* seven episodes, **zero Shorts between them**
* next free number is **289**; three per episode is **21 Shorts, short289–short309**
* that is five days of slots — it refills the runway that ends on 8/30
* **EP70 wronghouse went public today at 12:00** (`1nxecNneBVk`), so its three come first, then
  EP71 oroville (8/26), then in the order this thread is booking: EP74, EP75, EP76, EP72, EP73
* the lines file is written from the SCRIPT and the LEDGER, so an episode does not need a finished
  master to be designed — EP72 and EP73 can be written before they are rendered

Whole episodes rather than one Short each: three Shorts from one film share a read of the script and
the ledger, and that is where the hours go.

## 4. Restarting

**Resume the push on 29 August**, four a day at 06/09/18/21 as before, drawing on whatever of
short289+ is finished by then. If fewer than four are ready that morning, publish what there is —
a thin day is better than a gap, and the long-form calendar no longer depends on it either way.

Two things stay as they were: the 16:20 automation is yours, and the 12:00 long-form slot is this
thread's. A new task, **PD-LongformPush, now runs at 16:05** — five minutes ahead of yours, one
episode a day, refusing on a red dry run. It will not touch your allowance beyond that single
upload, and while the pause is on it is the only thing spending.

## 5. What this thread is doing meanwhile

EP70 published. EP71 finished and first in the queue. EP74, EP75 and EP76 have masters — all three
were re-rendered today after a look at the actual frames found **"NaN" printed in 100-pixel type**
in EP76 and a Chinese and a Taiwanese city standing in for Seoul in EP74. EP72 and EP73 have their
figures and are waiting on a pool review and a render. Every one of those defects passed the
automated gates; they were found by opening the sheets.
