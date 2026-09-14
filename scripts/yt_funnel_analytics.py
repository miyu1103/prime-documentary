#!/usr/bin/env python3
"""Answer three questions the channel-level report cannot: what feeds the long-form, does the
publish hour matter, and why is PLAYLIST traffic worth 23 minutes a view.

All read-only, and on the Analytics API rather than the Data API, so it costs none of the daily
10,000-unit budget that uploads live on.

  1. FUNNEL. insightTrafficSourceDetail under RELATED_VIDEO returns the referring video id. That
     turns "745 related-video views" into a list of which videos actually send traffic - the only
     way to see whether a Short feeds its own episode or something else does.
  2. PUBLISH HOUR. The Analytics API has no hour dimension, so the hour comes from each video's
     own publishAt and is joined against its lifetime views. That measures the SLOT, not the day.
  3. PLAYLIST. playlistStarts and viewsPerPlaylistStart, per playlist.

Usage: py -3.11 scripts/yt_funnel_analytics.py [START] [END]
"""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env                     # noqa: E402
from pd_factory.providers.youtube import _access_token         # noqa: E402

API = "https://youtubeanalytics.googleapis.com/v2/reports"
JST = timezone(timedelta(hours=9))


def query(tok: str, **params) -> dict:
    params.setdefault("ids", "channel==MINE")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode()[:300], "params": params}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    start = sys.argv[1] if len(sys.argv) > 1 else "2026-05-01"
    end = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()
    tok = _access_token(load_env())
    out: dict = {"window": [start, end]}

    print("=" * 64)
    print("1. WHAT FEEDS THE LONG-FORM  (referring video, RELATED_VIDEO)")
    r = query(tok, startDate=start, endDate=end, metrics="views,estimatedMinutesWatched",
              dimensions="insightTrafficSourceDetail",
              filters="insightTrafficSourceType==RELATED_VIDEO",
              maxResults=25, sort="-views")
    out["related_detail"] = r
    for row in r.get("rows", [])[:25]:
        print(f"   {row[0]:<14} views {row[1]:>5}   watch-min {row[2]:>6}")
    if "error" in r:
        print("   " + r["error"][:200])

    print("\n" + "=" * 64)
    print("2. PUBLISH HOUR vs LIFETIME VIEWS")
    per = query(tok, startDate=start, endDate=end,
                metrics="views,averageViewPercentage,subscribersGained",
                dimensions="video", maxResults=200, sort="-views")
    out["per_video"] = per
    ids = [row[0] for row in per.get("rows", [])]
    meta = {}
    for i in range(0, len(ids), 50):
        u = ("https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id="
             + ",".join(ids[i:i + 50]))
        rq = urllib.request.Request(u, headers={"Authorization": f"Bearer {tok}"})
        for v in json.loads(urllib.request.urlopen(rq, timeout=60).read().decode())["items"]:
            meta[v["id"]] = v
    out["meta_count"] = len(meta)
    buckets: dict[int, list] = {}
    for row in per.get("rows", []):
        v = meta.get(row[0])
        if not v:
            continue
        t = datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00")).astimezone(JST)
        buckets.setdefault(t.hour, []).append(row)
    print(f"   {'hour(JST)':<11}{'videos':>7}{'views':>8}{'median views':>14}{'avg view %':>12}")
    for h in sorted(buckets):
        rows = buckets[h]
        vs = sorted(r[1] for r in rows)
        med = vs[len(vs) // 2]
        avp = sum(r[2] for r in rows) / len(rows)
        print(f"   {h:02d}:00{'':<6}{len(rows):>7}{sum(vs):>8}{med:>14}{avp:>11.1f}%")

    print("\n" + "=" * 64)
    print("3. PLAYLISTS")
    pl = query(tok, startDate=start, endDate=end,
               metrics="views,estimatedMinutesWatched,playlistStarts,viewsPerPlaylistStart",
               dimensions="playlist", maxResults=25, sort="-views")
    out["playlists"] = pl
    for row in pl.get("rows", []):
        print(f"   {row[0]:<36} views {row[1]:>5}  min {row[2]:>6}  "
              f"starts {row[3]:>4}  views/start {row[4]:.1f}")
    if "error" in pl:
        print("   " + pl["error"][:200])

    dst = ROOT / "runs" / "_cache" / "funnel_analytics.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {dst.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
