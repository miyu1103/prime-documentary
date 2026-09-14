#!/usr/bin/env python3
"""Read-only: list the channel's uploads and classify Shorts. Writes JSON to stdout target path."""
from __future__ import annotations
import json, sys, urllib.request, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

CHANNEL_ID = "UCuQPtAz1rca9eJ4xhvX0yKA"
UPLOADS = "UU" + CHANNEL_ID[2:]  # uploads playlist id


def get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def iso8601_to_sec(dur: str) -> int:
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", dur or "")
    if not m:
        return 0
    h, mm, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mm * 60 + s


def main():
    env = load_env()
    token = _access_token(env)
    # 1) page through uploads playlist -> video ids
    items = []
    page = ""
    while True:
        url = ("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails"
               f"&maxResults=50&playlistId={UPLOADS}")
        if page:
            url += f"&pageToken={page}"
        data = get(url, token)
        items.extend(data.get("items", []))
        page = data.get("nextPageToken", "")
        if not page:
            break
    vids = [it["contentDetails"]["videoId"] for it in items]
    # 2) fetch details in batches of 50
    out = []
    for i in range(0, len(vids), 50):
        batch = vids[i:i + 50]
        url = ("https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,status"
               f"&id={','.join(batch)}&maxResults=50")
        data = get(url, token)
        for v in data.get("items", []):
            sn = v.get("snippet", {})
            secs = iso8601_to_sec(v.get("contentDetails", {}).get("duration", ""))
            title = sn.get("title", "")
            is_short = secs <= 75 or "#short" in title.lower()
            out.append({
                "video_id": v["id"],
                "title": title,
                "seconds": secs,
                "publishedAt": sn.get("publishedAt"),
                "privacy": v.get("status", {}).get("privacyStatus"),
                "is_short": is_short,
            })
    out.sort(key=lambda x: x.get("publishedAt") or "")
    dest = ROOT / "runs" / "shorts_thumbs" / "channel_uploads.v001.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    shorts = [o for o in out if o["is_short"]]
    print(f"total uploads: {len(out)}  shorts: {len(shorts)}")
    print(f"written: {dest}")
    for s in shorts:
        print(f"  {s['video_id']}  {s['seconds']:>3}s  {s['privacy']:<8} {s['title'][:70]}")


if __name__ == "__main__":
    main()
