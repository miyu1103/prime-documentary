#!/usr/bin/env python3
"""Track YouTube API quota spend so a batch cannot die halfway through.

Measured 2026-08-03: the day's 10,000-unit allowance was exhausted by *read* traffic. Five audit
tools were run back to back, each doing a full channel sweep, and each sweep called `search.list`
three times at 100 units apiece. Nothing warned; the next call simply returned HTTP 403
quotaExceeded, which surfaced as "CHANNELS FAILED" and looked like a code bug for several minutes.

The costs that matter here (units per call, from the published quota table):
    videos.insert      1600      <- an upload. Six per day and the allowance is gone.
    videos.update        50
    search.list         100      <- per page
    videos.list           1      <- per call, up to 50 ids
    playlistItems.list    1

So a 14-Short batch needs 22,400 units: it cannot complete in one day no matter what. Knowing that
before starting is the difference between "scheduled 6, resuming tomorrow" and "scheduled 6, then
eight cryptic 403s and a half-written state".

The ledger is an estimate, not an oracle: it counts what our own tools report. It is keyed by
Pacific date because that is when Google resets the allowance.

Usage:
  from yt_quota import record, spent_today, remaining, assert_budget, UNITS
  assert_budget(UNITS["videos.insert"] * len(batch))   # raises before spending anything
  record("videos.insert")

  py -3.11 scripts/yt_quota.py            # show today's spend
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "runs" / "_cache" / "yt_quota.json"
DAILY_LIMIT = 10_000

UNITS = {
    "videos.insert": 1600,
    "videos.update": 50,
    "thumbnails.set": 50,
    "search.list": 100,
    "videos.list": 1,
    "playlistItems.list": 1,
    "channels.list": 1,
    "playlistItems.insert": 50,
    "commentThreads.insert": 50,
    "commentThreads.list": 1,
}

# Google resets quota at midnight Pacific, which means the date must follow US daylight saving.
# A fixed -8 was tried first as "the safe direction": it is not. In August, Pacific is -7, so a
# fixed -8 kept the ledger on the PREVIOUS day for an hour after the real reset — long enough for
# assert_budget to refuse uploads against a quota that had already refilled. Use the real zone.
try:
    from zoneinfo import ZoneInfo
    PT = ZoneInfo("America/Los_Angeles")
except Exception:                       # no tzdata: fall back, and say so rather than be silently wrong
    PT = timezone(timedelta(hours=-7))
    print("[yt_quota] zoneinfo unavailable; assuming Pacific is UTC-7 (correct Mar-Nov only)",
          file=sys.stderr)


def _today() -> str:
    return datetime.now(PT).strftime("%Y-%m-%d")


def _load() -> dict:
    try:
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    except Exception:
        return {}


def record(op: str, n: int = 1, *, units: int | None = None) -> int:
    """Add `n` calls of `op` to today's ledger and return the new total. Unknown ops cost 1."""
    cost = (units if units is not None else UNITS.get(op, 1)) * n
    d = _load()
    day = d.setdefault(_today(), {"total": 0, "ops": {}})
    day["ops"][op] = day["ops"].get(op, 0) + n
    day["total"] += cost
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    tmp = LEDGER.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, indent=2), encoding="utf-8")
    tmp.replace(LEDGER)
    return day["total"]


def spent_today() -> int:
    return _load().get(_today(), {}).get("total", 0)


def remaining() -> int:
    return max(0, DAILY_LIMIT - spent_today())


class QuotaExhausted(RuntimeError):
    pass


def exhausted_observed_today() -> bool:
    """True only if a real quotaExceeded 403 was recorded today. This is evidence, not estimate."""
    return _load().get(_today(), {}).get("ops", {}).get("exhausted_observed_403", 0) > 0


def assert_budget(units_needed: int, *, what: str = "this batch", hard: bool = False) -> None:
    """Warn when the ESTIMATE says a batch will not fit; refuse only on OBSERVED exhaustion.

    The ledger multiplies recorded calls by Google's published unit table, and it drifts high:
    `record()` is called around requests rather than only after successful ones, so retries and
    failures add units Google never charged. Measured on 2026-08-10 the ledger read 10,734 of
    10,000 and every subsequent write returned 200; on 2026-08-08 and 08-09 it sat near the cap
    with nothing amiss. Only 2026-08-02 carries an actual `exhausted_observed_403`.

    A guard that refuses on the estimate therefore blocks work the API would have accepted, and
    because it refuses before trying, the estimate is never corrected. So:

      * quotaExceeded 403 seen today  -> QuotaExhausted (ground truth)
      * estimate exceeded only        -> loud warning on stderr, and proceed
      * hard=True                     -> the old behaviour, for callers that must not overrun

    Record the 403 when one is actually seen, with `record("exhausted_observed_403")`; that is what
    turns this guard back into a hard stop for the rest of the day.
    """
    left = remaining()
    if units_needed <= left:
        return
    hours = (datetime.now(PT).replace(hour=0, minute=0, second=0) + timedelta(days=1)
             - datetime.now(PT)).total_seconds() / 3600
    arithmetic = (f"{what} needs {units_needed} quota units, {left} left today "
                  f"(spent {spent_today()} of {DAILY_LIMIT}). Quota resets in {hours:.1f}h "
                  f"(midnight Pacific).")
    if hard or exhausted_observed_today():
        raise QuotaExhausted(arithmetic + " A quotaExceeded 403 was already observed today."
                             if exhausted_observed_today() else arithmetic + " Split the batch or wait.")
    print(f"[quota] WARNING: {arithmetic} No quotaExceeded 403 has been seen today, and the "
          f"ledger is an estimate that drifts high -- proceeding. Stop if a 403 appears.",
          file=sys.stderr)


def max_uploads_now() -> int:
    return remaining() // UNITS["videos.insert"]


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    d = _load()
    day = d.get(_today(), {"total": 0, "ops": {}})
    print(f"Pacific date {_today()} | spent {day['total']} of {DAILY_LIMIT} "
          f"| remaining {remaining()}")
    for op, n in sorted(day.get("ops", {}).items(), key=lambda kv: -UNITS.get(kv[0], 1) * kv[1]):
        print(f"  {op:<22}{n:>5} calls  {UNITS.get(op, 1) * n:>6} units")
    print(f"\nuploads still possible today: {max_uploads_now()} "
          f"(videos.insert costs {UNITS['videos.insert']} each)")
