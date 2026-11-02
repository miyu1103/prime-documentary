#!/usr/bin/env python3
"""Keep every Short pointed at its long-form, every day, without anyone remembering to.

The gap this closes, measured 2026-08-02/03:
  * 37 of 46 PUBLISHED Shorts were backfilled with a first-line link by hand.
  * 0 of 18 SCHEDULED Shorts have one, and they cannot get one yet: their destinations (EP50-59)
    are not published. A link to a private video is worse than no link.
  * Long-forms now publish one a day, so a different Short becomes linkable every single day.

Doing that by hand means remembering, daily, forever. This does it: run it once a day and it
links whatever became linkable since the last run, and leaves everything else alone.

Idempotent and safe to run repeatedly:
  * a Short that already links out is skipped
  * a Short whose destination is not yet public is skipped, silently, to be retried tomorrow
  * `status` is never sent, so publishAt cannot be disturbed
  * title, tags and categoryId are read back and re-sent unchanged

Quota: ~1 unit to list, 50 per video updated. A normal day updates one or two.

Usage:
  py -3.11 scripts/daily_funnel_sync.py            # dry run
  py -3.11 scripts/daily_funnel_sync.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "remotion" / "src" / "data"
RUNS = ROOT / "runs" / "short_funnel"
CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}

sys.path.insert(0, str(Path(__file__).resolve().parent))
# Enumeration lives in one place because this script's whole job depends on knowing which
# long-forms are public. Reading the uploads playlist alone hid three published episodes on
# 2026-08-03 and this script therefore refused to link fifteen Shorts to live destinations.
from yt_channel_index import (  # noqa: E402
    authorize, fetch_videos, http, iso_seconds as secs, list_video_ids)


def short_to_episode() -> dict[str, str]:
    out = {}
    for f in sorted(DATA.glob("short*.ts")):
        if f.name.endswith("_timing.ts"):
            continue
        m = re.search(r"episodeId:\s*'([^']+)'", f.read_text("utf-8", errors="replace"))
        if m:
            out[f.stem] = m.group(1)
    return out


def video_id_of_short() -> dict[str, str]:
    out = {}
    for p in list((ROOT / "runs" / "new_shorts" / "schedule").glob("short*.result.json")) + \
             list((ROOT / "episodes").rglob("short*_youtube_schedule_result.v001.json")):
        m = re.match(r"(short\d+[a-z]?)", p.name)
        if not m:
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        v = d.get("video_id") or d.get("videoId") or (d.get("response") or {}).get("id")
        if isinstance(v, str) and len(v) == 11:
            out.setdefault(m.group(1), v)
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    auth = authorize(ROOT)
    V = fetch_videos(auth, list_video_ids(auth))

    longs = {i: v for i, v in V.items()
             if secs(v["contentDetails"]["duration"]) > 185 and v["status"]["privacyStatus"] == "public"}

    ep_of_short, vid_of_short = short_to_episode(), video_id_of_short()
    ep_long = {}
    for ep_dir in sorted((ROOT / "episodes").glob("PD-2026-*")):
        for j in ep_dir.rglob("*.json"):
            if "short" in j.name.lower():
                continue
            try:
                txt = j.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for lid in longs:
                if lid in txt:
                    ep_long.setdefault(ep_dir.name, lid)

    todo, waiting, done = [], [], 0
    for sid, vid in sorted(vid_of_short.items()):
        v = V.get(vid)
        if not v or secs(v["contentDetails"]["duration"]) > 185:
            continue
        ep = ep_of_short.get(sid)
        lid = ep_long.get(ep) if ep else None
        head = "\n".join(v["snippet"].get("description", "").splitlines()[:3])
        if lid and lid in head:
            done += 1
            continue
        if not lid:
            waiting.append((sid, ep or "?"))
            continue
        todo.append({"short": sid, "video": vid, "longform": lid,
                     "title": v["snippet"]["title"][:44],
                     "state": v["status"]["privacyStatus"]})

    print(f"{done} Shorts already link out | {len(todo)} became linkable | "
          f"{len(waiting)} still waiting for their long-form to publish")
    for t in todo:
        print(f"  {t['short']:<9} [{t['state']:<9}] {t['title']}  ->  {t['longform']}")
    if waiting[:8]:
        print("  waiting:", ", ".join(f"{s}({e.split('-',3)[-1]})" for s, e in waiting[:8]),
              f"... +{max(0, len(waiting)-8)}" if len(waiting) > 8 else "")

    if not args.apply or not todo:
        if not args.apply:
            print("\nDRY RUN — nothing written.")
        return 0

    ok = fail = 0
    for t in todo:
        v = V[t["video"]]
        if v["snippet"].get("channelId") not in CHANNEL_ALLOWLIST:
            print(f"  {t['short']} NOT ON ALLOWLISTED CHANNEL — skipped"); fail += 1; continue
        lv = longs[t["longform"]]
        url = f"https://www.youtube.com/watch?v={t['longform']}"
        sn = v["snippet"]
        desc = f"▶ FULL CASE: {lv['snippet']['title']}\n{url}\n\n{sn.get('description','')}"
        payload = {"id": t["video"], "snippet": {
            "title": sn["title"], "description": desc,
            "categoryId": sn.get("categoryId", "27"), "tags": sn.get("tags", []),
            **({"defaultLanguage": sn["defaultLanguage"]} if sn.get("defaultLanguage") else {}),
        }}
        st, res = http("PUT", "https://www.googleapis.com/youtube/v3/videos?part=snippet",
                       headers=auth, body=payload)
        if st == 200:
            ok += 1
            print(f"  linked {t['short']} -> {t['longform']}")
        else:
            fail += 1
            print(f"  FAILED {t['short']} {st}: {res.get('error', {}).get('message','')[:100]}")

    RUNS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (RUNS / f"daily_sync.{stamp}.json").write_text(
        json.dumps({"linked": ok, "failed": fail, "waiting": len(waiting),
                    "already": done, "items": todo}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nlinked {ok}, failed {fail}")
    return 0 if not fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
