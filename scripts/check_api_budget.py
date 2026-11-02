#!/usr/bin/env python
"""Say how many uploads today's remaining YouTube API quota can actually carry.

On 2026-08-03 the day's 10,000 units went on 42 playlist placements (2,364), chapter and
link edits on the same 42 descriptions (~2,250) and two uploads (3,200). The third upload
died mid-flight on `403 The request cannot be completed because you have exceeded your
quota`, after the gate had passed and the approval was written. Nothing warned first,
because nothing was counting.

The API does not expose a remaining-quota reading, so this MEASURES the floor a different
way: it reads this repo's own record of what it spent today (the receipts and state files
each write-tool leaves behind) and probes whether a 1-unit read still succeeds. A read that
403s means the day is already gone, which is a certainty rather than an estimate.

    python scripts/check_api_budget.py            # report
    python scripts/check_api_budget.py --need 2   # exit 1 unless 2 more uploads fit

Exit 0 = the requested uploads fit. 1 = they do not. Read-only apart from one 1-unit probe.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
DAILY_UNITS = 10_000
COST = {"upload": 1600, "thumbnail": 50, "captions": 400, "update": 50, "playlist_item": 50,
        "playlist": 50, "read": 1}

# The quota day resets at midnight Pacific. In JST that is 16:00 or 17:00 depending on DST.
PACIFIC_OFFSET = timedelta(hours=-7)   # PDT; -8 in winter, and the reset shifts an hour


def quota_day_start_utc(now: datetime) -> datetime:
    local = now + PACIFIC_OFFSET
    midnight = local.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight - PACIFIC_OFFSET


def spent_today(since: datetime) -> tuple[int, list[str]]:
    """Sum what this repo's own receipts say it spent since the quota day began."""
    total, lines = 0, []

    def newer(p: Path) -> bool:
        try:
            return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc) >= since
        except OSError:
            return False

    uploads = [p for p in ROOT.glob("episodes/*/09_package/youtube_schedule_result.v*.json")
               if newer(p)]
    if uploads:
        n = len(uploads)
        cost = n * (COST["upload"] + COST["thumbnail"] + COST["captions"])
        total += cost
        lines.append(f"{n} upload(s) (video + thumbnail + captions)".ljust(46) + f"{cost:>6}")

    applied = ROOT / "episodes/_planning/measurements/DESCRIPTION_APPLY.v001.json"
    if applied.is_file() and newer(applied):
        try:
            n = len(json.loads(applied.read_text(encoding="utf-8")).get("applied", []))
        except Exception:
            n = 0
        if n:
            cost = n * (COST["update"] + 2)
            total += cost
            lines.append(f"{n} description update(s)".ljust(46) + f"{cost:>6}")

    plan = ROOT / "episodes/_planning/measurements/PLAYLIST_EXECUTION.v001.json"
    if plan.is_file() and newer(plan):
        try:
            d = json.loads(plan.read_text(encoding="utf-8"))
            runs = [r for r in d.get("runs", [])
                    if datetime.fromisoformat(r["started_at"]) >= since]
        except Exception:
            runs = []
        if runs:
            cost = d.get("plan_total_quota_units", 2300)
            total += cost
            lines.append("playlist execution".ljust(46) + f"{cost:>6}")

    state = ROOT / "episodes/_planning/measurements/DISTRIBUTION_STATE.v001.json"
    if state.is_file() and newer(state):
        total += 300
        lines.append("channel audit / reads".ljust(46) + f"{300:>6}")
    return total, lines


def reads_still_work() -> bool | None:
    """One unit. True = quota remains, False = the day is spent, None = could not tell."""
    try:
        sys.path.insert(0, str(ROOT / "src"))
        sys.path.insert(0, str(ROOT / "scripts"))
        from pd_factory.providers import load_env
        from pd_factory.providers.youtube import _access_token
        tok = _access_token(load_env())
    except Exception:
        return None
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true",
        headers={"Authorization": f"Bearer {tok}"})
    try:
        urllib.request.urlopen(req, timeout=20)
        return True
    except urllib.error.HTTPError as exc:
        if exc.code == 403 and b"quota" in (exc.read() or b"").lower():
            return False
        return None
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--need", type=int, default=0, help="uploads you are about to make")
    ap.add_argument("--no-probe", action="store_true")
    a = ap.parse_args()

    now = datetime.now(timezone.utc)
    since = quota_day_start_utc(now)
    spent, lines = spent_today(since)
    left = max(0, DAILY_UNITS - spent)
    per_upload = COST["upload"] + COST["thumbnail"] + COST["captions"]
    fits = left // per_upload

    reset_local = (since + timedelta(days=1)).astimezone()
    print(f"[budget] quota day began {since.astimezone():%Y-%m-%d %H:%M} local, "
          f"resets {reset_local:%H:%M}")
    for line in lines:
        print(f"  {line}")
    print("  " + "spent (from this repo's own receipts)".ljust(46) + f"{spent:>6}")
    print(f"  {'remaining'.ljust(46)}{left:>6}")
    print(f"[budget] room for about {fits} more upload(s) at {per_upload} units each")

    if not a.no_probe:
        ok = reads_still_work()
        if ok is False:
            print("[budget] a 1-unit read already returns 403 quotaExceeded -- the day IS spent, "
                  "whatever the arithmetic above says. Wait for the reset.")
            return 1
        if ok is None:
            print("[budget] could not probe the API; the number above is arithmetic only")

    if a.need:
        if a.need > fits:
            print(f"[budget] REFUSING: {a.need} upload(s) need {a.need * per_upload} units and "
                  f"only {left} remain. Upload {fits} now and the rest after the reset, or use "
                  f"the browser, which costs no quota at all.")
            return 1
        print(f"[budget] {a.need} upload(s) fit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
