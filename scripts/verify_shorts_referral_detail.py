#!/usr/bin/env python3
"""Second pass on the two Analytics queries that errored in verify_shorts_playlist_headlines.py.

The first run printed "views into long-forms referred by our own Shorts: 0" from a query that had
actually returned HTTP 500 (FIELD_UNKNOWN_VALUE on max-results). A zero printed from an error is
not a measurement. This re-asks it three independent ways and also pulls per-video analytics that
the playlist design needs.

Usage: py -3.11 scripts/verify_shorts_referral_detail.py [START] [END]
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yt_channel_index import authorize, fetch_videos, iso_seconds, list_video_ids  # noqa: E402

ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"


def q(auth: dict, **params) -> dict:
    params.setdefault("ids", "channel==MINE")
    url = ANALYTICS + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=auth)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode())
            msg = body.get("error", {}).get("message", "")[:200]
        except Exception:
            msg = f"HTTP {e.code}"
        return {"error": msg, "params": params}


def show(label: str, r: dict, decorate=None) -> list:
    print(f"\n--- {label}")
    if "error" in r:
        print("    QUERY FAILED:", r["error"])
        return []
    rows = r.get("rows", [])
    if not rows:
        print("    (no rows returned, query OK)")
    for row in rows:
        extra = decorate(row) if decorate else ""
        print("    " + "  ".join(str(x) for x in row) + "  " + extra)
    return rows


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    start = sys.argv[1] if len(sys.argv) > 1 else "2026-01-01"
    end = sys.argv[2] if len(sys.argv) > 2 else "2026-08-10"
    auth = authorize(ROOT)
    ids = list_video_ids(auth)
    meta = fetch_videos(auth, ids)
    dur = {i: iso_seconds(v["contentDetails"]["duration"]) for i, v in meta.items()}
    priv = {i: v["status"]["privacyStatus"] for i, v in meta.items()}
    title = {i: v["snippet"]["title"] for i, v in meta.items()}
    shorts = {i for i, s in dur.items() if s <= 180}
    longs = {i for i, s in dur.items() if s > 180}
    pub_longs = [i for i in longs if priv[i] == "public"]
    out = {"window": [start, end]}

    def tag(row):
        vid = row[0]
        k = "OUR-SHORT" if vid in shorts else ("our-long" if vid in longs else "off-channel")
        return f"[{k}] {title.get(vid, '')[:50]}"

    # 1. Channel-wide RELATED_VIDEO detail, no maxResults (the param that 500'd).
    r1 = q(auth, startDate=start, endDate=end, metrics="views,estimatedMinutesWatched",
           dimensions="insightTrafficSourceDetail",
           filters="insightTrafficSourceType==RELATED_VIDEO", sort="-views")
    rows1 = show("A. channel-wide RELATED_VIDEO referrers", r1, tag)
    out["related_channelwide"] = rows1

    # 2. Same, restricted to public long-forms as the DESTINATION.
    r2 = q(auth, startDate=start, endDate=end, metrics="views,estimatedMinutesWatched",
           dimensions="insightTrafficSourceDetail",
           filters="video==" + ",".join(pub_longs) + ";insightTrafficSourceType==RELATED_VIDEO",
           sort="-views")
    rows2 = show("B. referrers INTO public long-forms only", r2, tag)
    out["related_into_longforms"] = rows2

    # 3. Does a SHORTS traffic source exist on long-forms at all? Ask each long-form's mix.
    r3 = q(auth, startDate=start, endDate=end, metrics="views",
           dimensions="video,insightTrafficSourceType",
           filters="video==" + ",".join(pub_longs) + ";insightTrafficSourceType==SHORTS")
    rows3 = show("C. SHORTS traffic source landing on any public long-form", r3)
    out["shorts_source_on_longforms"] = rows3

    # 4. Per-video analytics for the playlist design.
    r4 = q(auth, startDate=start, endDate=end,
           metrics="views,estimatedMinutesWatched,averageViewPercentage,subscribersGained",
           dimensions="video", maxResults=200, sort="-views")
    per = {row[0]: row[1:] for row in r4.get("rows", [])} if "error" not in r4 else {}
    out["per_video"] = per
    if "error" in r4:
        print("\n--- D. per-video FAILED:", r4["error"])
    else:
        print(f"\n--- D. per-video rows: {len(per)}  (public long-forms, by views)")
        for vid in sorted(pub_longs, key=lambda v: -per.get(v, [0])[0]):
            v, m, apv, sg = per.get(vid, [0, 0, 0, 0])
            print(f"    {vid}  v{v:>5}  min{m:>6}  apv{apv:>6.1f}%  subs{sg:>3}  "
                  f"{title.get(vid,'')[:60]}")

    out["titles"] = {i: title[i] for i in meta}
    out["dur"] = dur
    out["priv"] = priv
    dest = ROOT / "runs" / "_cache" / "headline_verification_pass2.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
