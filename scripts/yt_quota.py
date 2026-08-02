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
}

# Google resets quota at midnight Pacific. PST is UTC-8, PDT is UTC-7; using -8 makes the reset
# look one hour later than it is, which errs toward spending less. That is the safe direction.
PT = timezone(timedelta(hours=-8))


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


def assert_budget(units_needed: int, *, what: str = "this batch") -> None:
    """Refuse to start work that provably cannot finish inside today's allowance.

    Raises QuotaExhausted with the arithmetic spelled out, so the caller can split the batch
    instead of discovering the limit through a 403 in the middle of it.
    """
    left = remaining()
    if units_needed <= left:
        return
    hours = (datetime.now(PT).replace(hour=0, minute=0, second=0) + timedelta(days=1)
             - datetime.now(PT)).total_seconds() / 3600
    raise QuotaExhausted(
        f"{what} needs {units_needed} quota units, {left} left today "
        f"(spent {spent_today()} of {DAILY_LIMIT}). Quota resets in {hours:.1f}h "
        f"(midnight Pacific). Split the batch or wait.")


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
