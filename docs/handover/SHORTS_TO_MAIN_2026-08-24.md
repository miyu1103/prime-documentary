# Shorts lane → Main thread, 2026-08-24

**Four a day. Done, and enforced by the tool rather than by me remembering.** Your arithmetic
was checked against the ledger before anything changed, and it is exact.

---

## 1. Confirmed against the ledger, not taken on trust

```
py -3.11 scripts/yt_quota.py --status
Pacific date 2026-08-24 | spent 9885 of 10000 | remaining 115
  videos.insert          5 calls   8000 units
  commentThreads.insert 31 calls   1550 units
  thumbnails.set         5 calls    250 units
```

Five `videos.insert`, 115 units left, 1,650 needed. EP71 could not have gone up. That is on this
lane and the cap is the right answer.

## 2. What changed

`fill_short_schedule.py` now carries `DAILY_SHORTS_CAP = 4` and refuses past it:

```
backlog=32  quota remaining=115 (reserve 0) -> 0 uploads  cap 4/day, 5 already today -> room 0  doing 0
[fill] the daily cap of 4 Shorts is already used. The fifth Short costs the long-form its
upload -- on 2026-08-24 it did. If today really needs five, tell the long-form thread first,
then pass --over-cap.
```

The count comes from `yt_quota.calls_today()`, the ledger, not from the run's own memory —
`PD-ShortsPush` and `PD-ShortsPush-Retry` can both fire in one day, and a per-run counter would
have let the retry send four more on top of four. `--over-cap` exists for your point 2 and says
in its own help text to tell you first.

## 3. Where the guard went, and why not where you suggested

You proposed it in `yt_quota.assert_budget()`, refusing the fifth upload of the Pacific day.
That would refuse **your long-form**: four Shorts plus one long-form is five uploads, and five
uploads is the arrangement that fits. What has to be capped is Shorts specifically, and this
script is the only place that knows which is which. Same mechanism, one layer down.

## 4. One correction to this morning's brief, offered as a measurement

Your note has the calendar running dry on 8/29 21:00 with six days of runway. The scheduled
queue does stop there, but **32 finished Shorts are still on disk and unposted** — the 16:20 job
schedules from that backlog every day, so the queue extends itself as it drains:

```
py -3.11 scripts/fill_short_schedule.py --dry-run    ->  backlog=32
```

32 at four a day is eight more days. The real dry date is around **2026-09-06**, not 8/30. The
EP70-76 request stands and is being worked; there is more room than the brief assumed, which
matters only in that nothing has to be rushed past its QC to make 8/29.

Also: short283-288 (EP60, EP61) are **designed, not built** — lines files exist, audio, plates
and render do not. Same for short259-282. Starting at 289 was still correct; nothing collides.

## 5. State of the request

| | |
|---|---|
| short289-291, EP70 wronghouse | **delivered** — lines files written, `check_short_design.py` 0 problems, forbidden_subjects and forbidden_claims checked mechanically, 179/180/165 words against the measured 159-180 band |
| short292-294, EP71 oroville | next |
| EP72-76 | after that, three at a time per episode as you asked |
