# Main thread → Shorts lane, 2026-08-24 (second note)

**Four Shorts a day, not five. Owner's decision, taken today.** The fifth Short costs the
long-form its upload, and today it did.

---

## What happened, measured

```
py -3.11 scripts/yt_quota.py --status      # 2026-08-24 17:45 JST
```

```
Pacific date 2026-08-24 | spent 9,885 of 10,000 | remaining 115

  videos.insert          5 calls   8,000 units     <- five Shorts
  commentThreads.insert 31 calls   1,550 units     <- pinned comments
  thumbnails.set         5 calls     250 units
  commentThreads.list   80 calls      80 units
  videos.list            5 calls       5 units
```

**115 units left. A long-form upload needs 1,650.** EP71 oroville has been finished and waiting
since this morning — master rendered, 61 shipped-frame sheets read tile by tile, thumbnail
selected, packaging measured at zero unsupported claims, scheduler entry written, dry run green —
and it could not be uploaded. Its slot moves from 8/25 to 8/26, and every episode behind it moves
with it: EP74, EP75, EP76, EP72, EP73, six days of the calendar, all one day later.

## The arithmetic that has to hold

| | units |
|---|---|
| daily allowance | 10,000 |
| one long-form (`videos.insert` 1,600 + `thumbnails.set` 50) | **1,650** |
| four Shorts (1,600 + 50 each) | **6,600** |
| pinned comments, ~6 × 50 | 300 |
| reads (`videos.list`, `commentThreads.list`, audits) | ~150 |
| **total** | **8,700** |
| **margin** | **1,300** |

Five Shorts makes that 10,350 — over the allowance before the long-form is even attempted, which
is why today's `videos.insert` count reads 5 and not 6.

## What this asks of you

1. **Cap the daily push at four Shorts.** 06:00 / 09:00 / 18:00 / 21:00 JST, as before.
2. **If a day genuinely needs five, say so here first** and this thread will move its long-form off
   that day deliberately, rather than discovering it at 17:45.
3. **Nothing else changes.** The 16:20 automation stays yours; the 12:00 long-form slot stays with
   this thread. The boundary is the slot time, not the tool.

A guard is worth adding on your side: refuse the fifth upload of a Pacific day unless an override
is passed. `scripts/yt_quota.py` already records every call, so the count is one read away —
`assert_budget()` in that file is the place, and it already raises before spending anything.

## Still true from this morning's brief

`docs/handover/MAIN_TO_SHORTS_2026-08-24.md` — the Shorts calendar runs dry at **2026-08-29
21:00**, and EP70 through EP76 have zero Shorts between them. Next free number is **289**;
three per episode is 21 Shorts, which buys the runway back with a day to spare. EP70 wronghouse
went **public today at 12:00 JST** (`1nxecNneBVk`), so its Shorts have the most to gain from being
made first.
