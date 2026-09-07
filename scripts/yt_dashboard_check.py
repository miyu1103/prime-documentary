"""Read-only YouTube dashboard check. No cost, no writes, no publish.

Refreshes an access token from the stored refresh token, then reads:
- channel snippet + statistics (subs / views / video count)
- the channel's uploads playlist -> most recent uploads with per-video stats

Secrets are never printed.
"""
from __future__ import annotations

import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import urllib.parse
import urllib.request
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def http(method: str, url: str, *, headers=None, form=None):
    data = urllib.parse.urlencode(form).encode() if form else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def main() -> int:
    env = load_env()
    for k in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"):
        if not env.get(k):
            print(f"MISSING {k}")
            return 2

    status, body = http(
        "POST",
        "https://oauth2.googleapis.com/token",
        form={
            "client_id": env["YOUTUBE_CLIENT_ID"],
            "client_secret": env["YOUTUBE_CLIENT_SECRET"],
            "refresh_token": env["YOUTUBE_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
    )
    if status != 200 or "access_token" not in body:
        print(f"TOKEN REFRESH FAILED: HTTP {status} {body.get('error')}")
        return 3
    token = body["access_token"]
    auth = {"Authorization": f"Bearer {token}"}

    status, ch = http(
        "GET",
        "https://www.googleapis.com/youtube/v3/channels"
        "?part=snippet,statistics,contentDetails&mine=true",
        headers=auth,
    )
    if status != 200 or not ch.get("items"):
        print(f"CHANNELS FAILED: HTTP {status} {ch}")
        return 4
    item = ch["items"][0]
    sn = item["snippet"]
    st = item["statistics"]

    print("=== CHANNEL ===")
    print(f"title        : {sn.get('title')}")
    print(f"channelId    : {item.get('id')}")
    print(f"published    : {sn.get('publishedAt')}")
    print(f"subscribers  : {st.get('subscriberCount')} (hidden={st.get('hiddenSubscriberCount')})")
    print(f"total views  : {st.get('viewCount')}")
    print(f"video count  : {st.get('videoCount')}")

    # "Recent" used to mean "first 15 rows of the uploads playlist". That playlist is not a
    # complete census — it omitted nine videos on 2026-08-03 — so a dashboard reading it could
    # leave the newest upload off the screen entirely. Take the union and sort by publish time.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from yt_channel_index import fetch_videos, list_video_ids
    all_videos = fetch_videos(auth, list_video_ids(auth), part="snippet,status,statistics")
    recent = sorted(all_videos.values(),
                    key=lambda v: v["snippet"].get("publishedAt", ""), reverse=True)[:15]
    vids = recent
    stats_by_id = {v["id"]: v for v in recent}

    print(f"\n=== RECENT UPLOADS ({len(vids)} of {len(all_videos)}) ===")
    for v in vids:
        vid = v["id"]
        title = v["snippet"]["title"]
        pub = v["snippet"].get("publishedAt", "-")
        meta = stats_by_id.get(vid, {})
        priv = meta.get("status", {}).get("privacyStatus", "?")
        views = meta.get("statistics", {}).get("viewCount", "?")
        print(f"[{priv:7}] {pub[:10]}  views={views:>6}  {title[:60]}  ({vid})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
