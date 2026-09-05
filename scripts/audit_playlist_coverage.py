#!/usr/bin/env python3
"""What the channel's playlists actually contain, and which public long-forms are in none of them.

The brief said the playlists were "essentially unbuilt". They are not: four public playlists exist
with 50 slots between them. This measures the real gap rather than rebuilding over the top of it.

For each playlist: id, title, description, item count, ordering, and the first video (the one that
does the recruiting). For the channel: every public long-form that belongs to no playlist, joined
to its measured views / APV / subscribers so the gap can be ranked by what it is worth.

Read-only. Cost: 1 unit per playlist page + ceil(n/50) for videos.list.

Usage: py -3.11 scripts/audit_playlist_coverage.py
"""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yt_channel_index import authorize, fetch_videos, http, iso_seconds, list_video_ids  # noqa
import yt_quota as Q  # noqa: E402

API = "https://www.googleapis.com/youtube/v3"
ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
OUT = ROOT / "runs" / "_cache" / "playlist_coverage.json"


def analytics(auth, **p):
    p.setdefault("ids", "channel==MINE")
    try:
        with urllib.request.urlopen(urllib.request.Request(
                ANALYTICS + "?" + urllib.parse.urlencode(p), headers=auth), timeout=120) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e)[:200]}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    auth = authorize(ROOT)
    ids = list_video_ids(auth, ttl=86400)          # do NOT burn 400 units on a fresh sweep
    V = fetch_videos(auth, ids)
    Q.record("videos.list", (len(ids) + 49) // 50)
    dur = {i: iso_seconds(v["contentDetails"]["duration"]) for i, v in V.items()}
    pub_long = {i for i in V if dur[i] > 180 and V[i]["status"]["privacyStatus"] == "public"}

    per = analytics(auth, startDate="2026-01-01", endDate="2026-08-10",
                    metrics="views,estimatedMinutesWatched,averageViewPercentage,"
                            "subscribersGained", dimensions="video", maxResults=200, sort="-views")
    stats = {r[0]: r[1:] for r in per.get("rows", [])}

    st, pl = http("GET", f"{API}/playlists?part=snippet,contentDetails,status"
                         "&mine=true&maxResults=50", headers=auth)
    Q.record("playlistItems.list")
    if st != 200:
        print("playlists.list failed", st, pl); return 2

    out = {"playlists": [], "uncovered": []}
    covered: set[str] = set()
    for p in pl.get("items", []):
        items, page = [], ""
        while True:
            s2, r2 = http("GET", f"{API}/playlistItems?part=snippet,contentDetails"
                                 f"&playlistId={p['id']}&maxResults=50{page}", headers=auth)
            Q.record("playlistItems.list")
            if s2 != 200:
                break
            items += r2.get("items", [])
            nxt = r2.get("nextPageToken")
            if not nxt:
                break
            page = f"&pageToken={nxt}"
        vids = [i["contentDetails"]["videoId"] for i in items]
        covered |= {v for v in vids if v in pub_long}
        rec = {"id": p["id"], "title": p["snippet"]["title"],
               "description": p["snippet"].get("description", ""),
               "privacy": p["status"]["privacyStatus"],
               "count": len(vids),
               "videos": [{"id": v, "pos": n,
                           "kind": ("long" if dur.get(v, 0) > 180 else
                                    ("short" if v in dur else "off-channel")),
                           "public": V[v]["status"]["privacyStatus"] if v in V else "?",
                           "title": V[v]["snippet"]["title"] if v in V else
                                    items[n]["snippet"]["title"],
                           "views": stats.get(v, [0, 0, 0, 0])[0],
                           "apv": stats.get(v, [0, 0, 0, 0])[2],
                           "subs": stats.get(v, [0, 0, 0, 0])[3]}
                          for n, v in enumerate(vids)]}
        out["playlists"].append(rec)

        print("=" * 92)
        print(f"{rec['id']}  [{rec['privacy']}]  {rec['count']} items   {rec['title']}")
        print(f"  description: {rec['description'][:160] or '(EMPTY)'}")
        for it in rec["videos"]:
            flag = "  <-- FIRST (does the recruiting)" if it["pos"] == 0 else ""
            print(f"   {it['pos']:>2}. {it['id']}  {it['kind']:<11}{it['public']:<8}"
                  f"v{it['views']:>5} apv{it['apv']:>5.1f}% subs{it['subs']:>2}  "
                  f"{it['title'][:44]}{flag}")

    gap = sorted(pub_long - covered, key=lambda v: -stats.get(v, [0])[0])
    print("\n" + "=" * 92)
    print(f"PUBLIC LONG-FORMS {len(pub_long)} | in at least one playlist {len(covered)} "
          f"| in NONE {len(gap)}")
    for v in gap:
        s = stats.get(v, [0, 0, 0, 0])
        out["uncovered"].append({"id": v, "title": V[v]["snippet"]["title"],
                                 "views": s[0], "apv": s[2], "subs": s[3],
                                 "published": V[v]["snippet"]["publishedAt"][:10]})
        print(f"  {v}  v{s[0]:>5} apv{s[2]:>5.1f}% subs{s[3]:>2}  {V[v]['snippet']['publishedAt'][:10]}"
              f"  {V[v]['snippet']['title'][:60]}")

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {OUT}   ledger {Q.spent_today()} spent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
