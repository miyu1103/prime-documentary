#!/usr/bin/env python3
"""Re-space the Shorts publish schedule to a chosen cadence, without re-uploading anything.

A scheduled Short is a private video with a publishAt. Changing when it goes out is a
videos.update (50 units), not a re-upload (1600) - so the cadence can be changed freely and the
video ids, view history and funnel comments all survive.

Cadence is a real decision, not a detail:
  * uploading is capped at six a day by the API's 10,000-unit budget (videos.insert costs 1600)
  * so publishing six a day leaves ZERO buffer - one missed upload day is a hole in the schedule
  * publishing four a day against six uploaded leaves two a day of slack

Anything already scheduled before --from is left alone; only the tail is re-spaced, in its
existing order, so the running sequence is never shuffled.

Usage:
  py -3.11 scripts/reslot_short_schedule.py --from 2026-08-12 --slots 6,12,18,21 --dry-run
  py -3.11 scripts/reslot_short_schedule.py --from 2026-08-12 --slots 6,12,18,21 --apply
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env                    # noqa: E402
from pd_factory.providers.youtube import _access_token        # noqa: E402
import yt_quota                                               # noqa: E402

JST = dt.timezone(dt.timedelta(hours=9))


def scheduled() -> list[tuple[dt.datetime, int, str, Path]]:
    out = []
    for f in sorted(ROOT.glob("episodes/*/09_package/short*_youtube_schedule_result.*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if not d.get("publishAt") or not d.get("video_id"):
            continue
        n = int(re.sub(r"\D", "", (d.get("short_id") or f.stem.split("_")[0])))
        t = dt.datetime.fromisoformat(d["publishAt"].replace("Z", "+00:00")).astimezone(JST)
        out.append((t, n, d["video_id"], f))
    out.sort()
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", required=True, help="YYYY-MM-DD, JST")
    ap.add_argument("--slots", required=True, help="JST hours per day, e.g. 6,12,18,21")
    ap.add_argument("--avoid-occupied", metavar="JSON",
                    help="channel-truth dump (runs/shorts_thumbs/yt_scheduled.v001.json). Any JST "
                         "hour already taken there by a video this script does not own - a "
                         "long-form episode - is skipped, so a Short never publishes on the same "
                         "minute as an episode.")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")

    start = dt.date.fromisoformat(a.start)
    slots = [int(x) for x in a.slots.split(",") if x.strip()]
    cur = scheduled()
    move = [c for c in cur if c[0].date() >= start]
    keep = len(cur) - len(move)
    print(f"{keep} left untouched before {start}; re-spacing {len(move)} at "
          f"{len(slots)}/day ({a.slots} JST)")

    # Hours already used, per JST day, by videos this script does not own. On 2026-08-09 three
    # long-form episodes sat at 12:00 on days that also carried a Short at 12:00: the episode and
    # the Short went to the feed on the same minute and competed with each other.
    occupied: dict[dt.date, set[int]] = {}
    if a.avoid_occupied:
        mine = {c[2] for c in cur}
        for r in json.loads(Path(a.avoid_occupied).read_text(encoding="utf-8"))["scheduled"]:
            if r["id"] in mine:
                continue
            o = dt.datetime.fromisoformat(r["publishAt"].replace("Z", "+00:00")).astimezone(JST)
            occupied.setdefault(o.date(), set()).add(o.hour)
        if occupied:
            print("occupied by episodes: "
                  + ", ".join(f"{d} {sorted(h)}" for d, h in sorted(occupied.items())))

    # Fallback hours, tried in order, when a requested slot is taken. Kept inside the same waking
    # window so a displaced Short does not land at 03:00.
    ladder = [6, 9, 12, 15, 18, 21]

    plan = []
    i = 0
    for day in range(400):
        d0 = start + dt.timedelta(days=day)
        used = set(occupied.get(d0, set()))
        for h in slots:
            if i >= len(move):
                break
            if h in used:
                alt = next((x for x in ladder if x not in used and x not in slots), None)
                if alt is None:
                    alt = next((x for x in ladder if x not in used), None)
                if alt is None:
                    continue
                h = alt
            used.add(h)
            t, n, vid, f = move[i]
            i += 1
            new = dt.datetime(d0.year, d0.month, d0.day, h, tzinfo=JST)
            plan.append((new, n, vid, f, t))
        if i >= len(move):
            break
    plan.sort(key=lambda p: p[0])

    for new, n, vid, f, old in plan:
        mark = "" if new == old else "  <-"
        print(f"  short{n:<4} {old.strftime('%m-%d %H:%M')} -> {new.strftime('%m-%d %H:%M')} JST{mark}")
    changed = [p for p in plan if p[0] != p[4]]
    print(f"\n{len(changed)} of {len(plan)} actually move" + ("" if a.apply else "   (DRY RUN)"))
    if not a.apply or not changed:
        return 0

    tok = _access_token(load_env())
    for new, n, vid, f, old in changed:
        iso = new.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        yt_quota.assert_budget(50, what=f"videos.update short{n}")
        # read status first: a PUT on part=status replaces the whole object, so anything not sent
        # here would be silently reset
        req = urllib.request.Request(
            f"https://www.googleapis.com/youtube/v3/videos?part=status&id={vid}",
            headers={"Authorization": f"Bearer {tok}"})
        st = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())["items"][0]["status"]
        body = {"id": vid, "status": {
            "privacyStatus": "private", "publishAt": iso,
            "selfDeclaredMadeForKids": st.get("selfDeclaredMadeForKids", False),
            "license": st.get("license", "youtube"),
            "embeddable": st.get("embeddable", True),
            "publicStatsViewable": st.get("publicStatsViewable", True)}}
        req = urllib.request.Request(
            "https://www.googleapis.com/youtube/v3/videos?part=status",
            data=json.dumps(body).encode(), method="PUT",
            headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
        got = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())["status"]
        yt_quota.record("videos.update", 1)
        ok = (got.get("publishAt") or "").startswith(iso[:16])
        print(f"  short{n:<4} -> {got.get('publishAt')}  {'OK' if ok else 'MISMATCH'}")
        d = json.loads(f.read_text(encoding="utf-8"))
        d["publishAt"] = iso
        f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{len(changed)} re-slotted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
