#!/usr/bin/env python3
"""Upload and schedule as many backlog Shorts as today's quota allows.

92 finished Shorts were rendered, packaged and sitting on disk while the channel published four a
day from a queue that ran out on 2026-08-16. Uploading them one command at a time is the only
reason the backlog exists, so this walks it.

Two rules it will not break:

  * 12:00 JST belongs to the long-form episode. On 2026-08-09 three episodes and three Shorts were
    scheduled on the same minute at 12:00 and competed with each other in the feed. Shorts go at
    6, 9, 18 and 21 JST and never at 12.
  * The episode uploads come first. videos.insert costs 1600 units against a 10,000/day budget, so
    six Shorts empty it; --reserve holds units back for the episode chain that is waiting on the
    same budget.

Free slots are read from the live channel, not from local files: local schedule_result files were
eleven days stale on 2026-08-09 and planning from them double-booked a slot.

Usage:
  py -3.11 scripts/yt_list_scheduled.py                       # refresh channel truth first
  py -3.11 scripts/fill_short_schedule.py --dry-run
  py -3.11 scripts/fill_short_schedule.py --apply --reserve 6300 --max 3
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import yt_quota  # noqa: E402

JST = dt.timezone(dt.timedelta(hours=9))
SHORT_HOURS = (6, 9, 18, 21)          # 12 JST is the episode slot
TRUTH = ROOT / "runs" / "shorts_thumbs" / "yt_scheduled.v001.json"
UPLOAD_UNITS = yt_quota.UNITS.get("videos.insert", 1600)


# Four, not five. Owner's decision 2026-08-24, and the arithmetic that forced it:
#
#   daily allowance                                    10,000
#   one long-form  (videos.insert 1,600 + thumb 50)     1,650
#   four Shorts    (1,600 + 50 each)                    6,600
#   pinned comments, ~6 x 50                              300
#   reads (videos.list, commentThreads.list, audits)      ~150
#   ------------------------------------------------------------
#   total                                               8,700   margin 1,300
#
# Five Shorts makes that 10,350 -- over the allowance before the long-form is attempted. On
# 2026-08-24 that is exactly what happened: measured at 17:45, videos.insert read 5 calls and
# 8,000 units, spent 9,885 of 10,000, 115 left against the 1,650 a long-form needs. EP71
# oroville was finished that morning -- master rendered, 61 shipped-frame sheets read, thumbnail
# picked, packaging at zero unsupported claims, dry run green -- and could not be uploaded. Six
# days of the long-form calendar moved by one day.
#
# The cap lives HERE and not in yt_quota.assert_budget, which is where the other thread
# suggested it. A guard that refuses "the fifth upload of the Pacific day" would refuse the
# LONG-FORM, because four Shorts plus one long-form is five uploads and that is the arrangement
# that fits. What must be capped is Shorts specifically, which only this script counts.
DAILY_SHORTS_CAP = 4
PAUSE_FILE = ROOT / "config" / "shorts_pause.v001.json"


def paused() -> tuple[bool, str]:
    """A dated pause that expires on its own, rather than a disabled task somebody must remember.

    Turning off PD-ShortsPush works and then depends on a human turning it back on. This file
    carries the date it stops applying and the reason it was set, so a run during the pause
    prints WHY it is doing nothing, and the run after it needs no action at all.
    """
    if not PAUSE_FILE.exists():
        return False, ""
    try:
        d = json.loads(PAUSE_FILE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - an unreadable pause file is not a pause
        return False, ""
    until = str(d.get("paused_until", ""))
    if not until:
        return False, ""
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime("%Y-%m-%d")
    if today >= until:
        return False, ""
    return True, f"paused until {until}: {d.get('reason', 'no reason recorded')}"


def uploaded_today() -> int:
    """Shorts this Pacific day, from the quota ledger rather than from this run's memory.

    PD-ShortsPush and PD-ShortsPush-Retry can both run in one day. Counting only what this
    process has done would let the retry add another four on top of the four already sent.
    """
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import yt_quota
        return int(yt_quota.calls_today().get("videos.insert", 0))
    except Exception:  # noqa: BLE001 - no ledger is a reason to be careful, not to stop
        return 0


def backlog() -> list[str]:
    """Shorts that are rendered and packaged but have no video on the channel."""
    src = (ROOT / "scripts" / "schedule_short_youtube.py").read_text(encoding="utf-8")
    cfg = set(re.findall(r'^    "(\d+)":', src, re.M))
    done = set()
    for f in ROOT.glob("episodes/*/09_package/short*_youtube_schedule_result.*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        m = re.match(r"short(\d+)_", f.name)
        if d.get("video_id") and m:
            done.add(m.group(1).zfill(2))
    rendered = {
        re.match(r"short(\d+)_yt_coverfirst", p.stem).group(1).zfill(2)
        for p in (ROOT / "remotion" / "out").glob("short*_yt_coverfirst.mp4")
    }
    return sorted(rendered & cfg - done, key=int)


def free_slots(n: int) -> list[dt.datetime]:
    taken = set()
    for r in json.loads(TRUTH.read_text(encoding="utf-8"))["scheduled"]:
        t = dt.datetime.fromisoformat(r["publishAt"].replace("Z", "+00:00")).astimezone(JST)
        taken.add(t.replace(minute=0, second=0, microsecond=0))
    # Scan forward from today and fill every open Shorts hour, in order -- do not skip ahead
    # to "the day after the last thing on the calendar". A long-form booked far ahead (e.g.
    # valdez at 09-06 12:00) used to become that anchor and the walk started AT 09-06,
    # silently skipping open Shorts days 09-04/09-05 in between. Found 2026-09-04 when those
    # two days ended up with zero Shorts scheduled while a Short two days later got filled.
    out: list[dt.datetime] = []
    day = dt.datetime.now(JST).date()
    while len(out) < n:
        for h in SHORT_HOURS:
            if len(out) >= n:
                break
            slot = dt.datetime(day.year, day.month, day.day, h, tzinfo=JST)
            if slot in taken or slot <= dt.datetime.now(JST):
                continue
            out.append(slot)
        day += dt.timedelta(days=1)
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reserve", type=int, default=0,
                    help="units to leave untouched for the episode upload chain")
    ap.add_argument("--max", type=int, default=DAILY_SHORTS_CAP,
                    help=f"Shorts to upload this run (default {DAILY_SHORTS_CAP}, the daily cap)")
    ap.add_argument("--over-cap", action="store_true",
                    help="exceed the daily Shorts cap; tell the long-form thread FIRST")
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")
    if not TRUTH.exists():
        print(f"missing {TRUTH} - run scripts/yt_list_scheduled.py first")
        return 2
    # The channel dump is built from scripts/_yt_audit.json, and that file lists the ids to ask
    # about. Uploads made after the audit are invisible to it: five Shorts were scheduled and the
    # dump still said 29, so a second run would have planned straight over them.
    #
    # Staleness is decided by content, not by mtime. An mtime test called the dump stale every time
    # the ledger was synced - a write that by definition carries no new upload - and blocked a run
    # that was perfectly safe.
    truth = json.loads(TRUTH.read_text(encoding="utf-8"))
    known = {r["id"] for r in truth["scheduled"]} | {r["id"] for r in truth["unscheduled"]}
    missing = []
    for f in ROOT.glob("episodes/*/09_package/short*_youtube_schedule_result.*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        vid = d.get("video_id")
        when = d.get("publishAt")
        if not vid or not when:
            continue
        # The dump lists private videos only, so anything already published is legitimately absent.
        # Checking those too flagged every Short the channel has ever released.
        if dt.datetime.fromisoformat(when.replace("Z", "+00:00")) <= dt.datetime.now(dt.timezone.utc):
            continue
        if vid not in known:
            missing.append(f"{f.name} ({vid})")
    if missing:
        print("channel dump does not know about these uploads - refresh it first:")
        for m in missing[:6]:
            print(f"  {m}")
        print("  py -3.11 scripts/yt_full_audit.py && py -3.11 scripts/yt_list_scheduled.py")
        return 2

    todo = backlog()
    usable = max(0, yt_quota.remaining() - a.reserve)
    budget_allows = usable // UPLOAD_UNITS
    is_paused, why = paused()
    if is_paused and not a.over_cap:
        print(f"[fill] {why}")
        print("[fill] nothing uploaded. --over-cap overrides, after telling the long-form thread.")
        return 0
    done = uploaded_today()
    room = max(0, DAILY_SHORTS_CAP - done)
    if a.over_cap:
        room = a.max
    n = min(len(todo), budget_allows, a.max, room)
    print(f"backlog={len(todo)}  quota remaining={yt_quota.remaining()} "
          f"(reserve {a.reserve}) -> {budget_allows} uploads  "
          f"cap {DAILY_SHORTS_CAP}/day, {done} already today -> room {room}  doing {n}")
    if not room and not a.over_cap:
        print(f"[fill] the daily cap of {DAILY_SHORTS_CAP} Shorts is already used. The fifth "
              f"Short costs the long-form its upload -- on 2026-08-24 it did. If today really "
              f"needs five, tell the long-form thread first, then pass --over-cap.")
    if not n:
        return 0

    slots = free_slots(n)
    for s, slot in zip(todo[:n], slots):
        iso = slot.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"  short{s} -> {slot.strftime('%m-%d %H:%M')} JST ({iso})")
        if not a.apply:
            continue
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "schedule_short_youtube.py"),
             "--short", s, "--publish-at", iso],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        # On success, echo the child's own last lines. On FAILURE, never echo them: the child
        # prints "OK short<N>: scheduled publish at ..." as a PRE-FLIGHT confirmation, before it
        # touches the API, so a failure that happens later was being logged as
        #     FAILED  OK short151: scheduled publish at 2026-08-24T12:00:00Z
        # which reads as a success and hid the real error for a full day (2026-08-20).
        if r.returncode == 0:
            tail = "\n".join((r.stdout or "").strip().splitlines()[-3:])
            print(f"    OK  {tail}")
        else:
            err = (r.stderr or "").strip() or (r.stdout or "").strip()
            print(f"    FAILED short{s}: exit {r.returncode} -- the lines below are the ERROR, "
                  f"not the child's progress output")
            for line in err.splitlines()[-12:]:
                print(f"      | {line}")
            print("  stopping on first failure - a half-uploaded batch is worse than a short one")
            return 1
    if not a.apply:
        print("\n(DRY RUN)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
