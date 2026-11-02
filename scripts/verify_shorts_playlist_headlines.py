#!/usr/bin/env python3
"""Independent re-measurement of the two headline claims driving the Shorts->long-form work.

Claim 1: Shorts are ~7,630 of the channel's 9,675 views (2026-01-01..2026-08-10) and contribute
         0% of every long-form video's traffic mix.
Claim 2: PLAYLIST traffic delivers ~23.1 minutes per view (1,319 minutes from 57 views).

Everything here runs on the Analytics API (youtubeanalytics.googleapis.com), which does NOT draw
on the Data API's 10,000-unit/day allowance, plus at most a handful of 1-unit videos.list calls
for duration/title metadata.

Usage: py -3.11 scripts/verify_shorts_playlist_headlines.py [START] [END]
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
        return {"error": e.read().decode()[:400], "params": params}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    start = sys.argv[1] if len(sys.argv) > 1 else "2026-01-01"
    end = sys.argv[2] if len(sys.argv) > 2 else "2026-08-10"
    auth = authorize(ROOT)
    out: dict = {"window": [start, end]}

    ids = list_video_ids(auth)                       # cached union; 0 units when warm
    meta = fetch_videos(auth, ids)                   # ceil(n/50) units
    dur = {i: iso_seconds(v["contentDetails"]["duration"]) for i, v in meta.items()}
    priv = {i: v["status"]["privacyStatus"] for i, v in meta.items()}
    title = {i: v["snippet"]["title"] for i, v in meta.items()}

    # A Short is <= 180s (YouTube's own cutoff during this window is 3:00).
    shorts = {i for i, s in dur.items() if s <= 180}
    longs = {i for i, s in dur.items() if s > 180}
    out["counts"] = {"videos": len(meta), "shorts": len(shorts), "longs": len(longs),
                     "public_shorts": sum(1 for i in shorts if priv[i] == "public"),
                     "public_longs": sum(1 for i in longs if priv[i] == "public")}
    print(f"videos {len(meta)}  shorts<=180s {len(shorts)} "
          f"(public {out['counts']['public_shorts']})  longs {len(longs)} "
          f"(public {out['counts']['public_longs']})")

    # ---- CLAIM 1a: views split -------------------------------------------------------------
    per = q(auth, startDate=start, endDate=end, metrics="views,estimatedMinutesWatched,"
            "subscribersGained", dimensions="video", maxResults=200, sort="-views")
    rows = per.get("rows", [])
    if not rows:
        print("ANALYTICS ERROR:", per.get("error", "")[:300])
        return 2
    sv = sum(r[1] for r in rows if r[0] in shorts)
    lv = sum(r[1] for r in rows if r[0] in longs)
    uv = sum(r[1] for r in rows if r[0] not in dur)
    sg_s = sum(r[3] for r in rows if r[0] in shorts)
    sg_l = sum(r[3] for r in rows if r[0] in longs)
    total = sv + lv + uv
    out["views"] = {"shorts": sv, "longs": lv, "unknown_id": uv, "total_per_video": total}
    out["subs"] = {"shorts": sg_s, "longs": sg_l}
    print(f"\nCLAIM 1a  views {start}..{end}: shorts {sv} | longs {lv} | unmapped {uv} "
          f"| total {total}   shorts share {sv / total:.1%}")
    print(f"          subs gained: shorts {sg_s} (per 1k views "
          f"{sg_s / max(sv,1) * 1000:.2f}) | longs {sg_l} (per 1k {sg_l / max(lv,1) * 1000:.2f})")

    # channel total for the same window, as a cross-check that per-video sums to the whole
    ch = q(auth, startDate=start, endDate=end, metrics="views,estimatedMinutesWatched,"
           "subscribersGained")
    out["channel_total"] = ch.get("rows", [[None]])[0] if ch.get("rows") else ch
    print(f"          channel-level total row: {out['channel_total']}")

    # ---- CLAIM 1b: do Shorts appear in long-form traffic at all? --------------------------
    # Traffic source mix restricted to the long-form videos only.
    mix = q(auth, startDate=start, endDate=end, metrics="views,estimatedMinutesWatched",
            dimensions="insightTrafficSourceType", sort="-views")
    out["traffic_mix_channel"] = mix.get("rows", [])
    print("\n          channel traffic mix:")
    for r in mix.get("rows", []):
        print(f"            {r[0]:<28} views {r[1]:>6}  min {r[2]:>7}")

    pub_longs = [i for i in longs if priv[i] == "public"]
    grp = ",".join(pub_longs)
    lmix = {}
    if pub_longs:
        # filters allows up to 500 ids joined by comma on `video==`
        lmix = q(auth, startDate=start, endDate=end, metrics="views,estimatedMinutesWatched",
                 dimensions="insightTrafficSourceType", filters="video==" + grp, sort="-views")
    out["traffic_mix_longform_only"] = lmix.get("rows", lmix)
    print("\nCLAIM 1b  traffic mix for PUBLIC LONG-FORMS only:")
    for r in lmix.get("rows", []):
        print(f"            {r[0]:<28} views {r[1]:>6}  min {r[2]:>7}")
    if "error" in lmix:
        print("            error:", lmix["error"][:200])

    # RELATED_VIDEO detail on long-forms: which video ids refer traffic, and are any Shorts?
    rel = {}
    if pub_longs:
        rel = q(auth, startDate=start, endDate=end, metrics="views,estimatedMinutesWatched",
                dimensions="insightTrafficSourceDetail",
                filters="video==" + grp + ";insightTrafficSourceType==RELATED_VIDEO",
                maxResults=50, sort="-views")
    out["related_detail_longform"] = rel.get("rows", rel)
    print("\n          who refers traffic TO the long-forms (RELATED_VIDEO detail):")
    ref_short_views = 0
    for r in rel.get("rows", []):
        kind = "SHORT" if r[0] in shorts else ("long" if r[0] in longs else "off-channel")
        if r[0] in shorts:
            ref_short_views += r[1]
        print(f"            {r[0]:<14} {kind:<12} views {r[1]:>5}  min {r[2]:>6}  "
              f"{title.get(r[0],'')[:44]}")
    print(f"          -> views into long-forms referred by our own Shorts: {ref_short_views}")
    out["longform_views_referred_by_our_shorts"] = ref_short_views

    # ---- CLAIM 2: PLAYLIST traffic ---------------------------------------------------------
    pl = q(auth, startDate=start, endDate=end, metrics="views,estimatedMinutesWatched",
           dimensions="insightTrafficSourceType", filters="insightTrafficSourceType==PLAYLIST")
    out["playlist_traffic"] = pl.get("rows", pl)
    print("\nCLAIM 2  PLAYLIST traffic source:")
    for r in pl.get("rows", []):
        v, m = r[1], r[2]
        print(f"            views {v}  minutes {m}  -> {m / max(v,1):.1f} min/view")

    # playlist engagement metrics, if the channel has any playlists with traffic
    pstart = q(auth, startDate=start, endDate=end,
               metrics="views,estimatedMinutesWatched,playlistStarts,viewsPerPlaylistStart,"
                       "averageTimeInPlaylist", isCurated="1")
    out["playlist_curated"] = pstart.get("rows", pstart)
    print(f"          curated-playlist report rows: {out['playlist_curated']}")

    dest = ROOT / "runs" / "_cache" / "headline_verification.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
