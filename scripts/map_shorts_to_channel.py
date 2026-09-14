#!/usr/bin/env python3
"""Work out which locally-rendered Shorts are already on the channel, and which are not.

Why this exists: the answer decides whether a finished Short can still be changed. A Short that is
already uploaded is effectively frozen — re-uploading costs 1600 quota units and mints a new video
id, losing its scheduled slot — while one that has only been rendered can still be improved before
it ships.

Matching is on the DESCRIPTION, not the title. Published titles are rewritten for the packaging
experiment ("Police Can Search Your Car Without a Warrant - But Not the One Spot..."), so they no
longer resemble anything in the design; a title match found 6 of 69. The first line of the
description is the Short's own hook line, verbatim, which is unique per Short.

Enumeration goes through yt_channel_index: the uploads playlist alone omits about nine rotating
videos, and that omission has already caused a two-day schedule gap and a set of missing designs.

Cost: two or three videos.list calls, 1 unit each. Read-only. Writes runs/_cache/shorts_channel_map.json.

Usage: py -3.11 scripts/map_shorts_to_channel.py
"""
from __future__ import annotations

import difflib
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env                      # noqa: E402
from pd_factory.providers.youtube import _access_token          # noqa: E402
import yt_channel_index                                         # noqa: E402
import yt_quota                                                 # noqa: E402

DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
OUT = ROOT / "runs" / "_cache" / "shorts_channel_map.json"
MATCH_FLOOR = 0.72   # on the hook line; a real match scores far above this


def norm(t: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", (t or "").lower()).split())


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    env = load_env()
    token = _access_token(env)
    ids = yt_channel_index.list_video_ids({"Authorization": f"Bearer {token}"})
    print(f"channel has {len(ids)} videos")

    snippets = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        yt_quota.assert_budget(1, what="videos.list page")
        url = ("https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails"
               f"&maxResults=50&id={','.join(chunk)}")
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=120) as r:
            for v in json.loads(r.read().decode("utf-8")).get("items", []):
                snippets[v["id"]] = v
        yt_quota.record("videos.list", 1)
    print(f"fetched {len(snippets)} snippets")

    hooks = {}
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d["shorts"]:
            if s.get("lines"):
                hooks[s["short_id"]] = norm(s["lines"][0].get("text"))

    uploaded, rows = {}, []
    for vid, v in snippets.items():
        desc = norm((v["snippet"].get("description") or "").split("\n")[0])
        if not desc:
            continue
        best_sid, best_r = None, 0.0
        for sid, hook in hooks.items():
            r = difflib.SequenceMatcher(None, desc, hook).ratio()
            if r > best_r:
                best_sid, best_r = sid, r
        if best_r >= MATCH_FLOOR:
            uploaded[best_sid] = {"video_id": vid, "score": round(best_r, 3),
                                  "privacy": v.get("status", {}).get("privacyStatus"),
                                  "publishAt": v.get("status", {}).get("publishAt")}
            rows.append((best_sid, best_r, vid))

    rendered = sorted(int(re.sub(r"\D", "", p.stem.split("_")[0]))
                      for p in (ROOT / "remotion" / "out").glob("short*_yt_coverfirst.mp4"))
    free = [n for n in rendered if f"short{n}" not in uploaded]
    print(f"\nlocally rendered: {len(rendered)}")
    print(f"already on the channel: {len(rendered) - len(free)}  (frozen - re-upload costs 1600 units)")
    print(f"rendered but NOT uploaded: {len(free)}  (still changeable)")
    print("  " + ", ".join(map(str, free)))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"uploaded": uploaded, "rendered": rendered, "changeable": free},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
