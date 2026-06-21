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
    uploads = item["contentDetails"]["relatedPlaylists"]["uploads"]

    print("=== CHANNEL ===")
    print(f"title        : {sn.get('title')}")
    print(f"channelId    : {item.get('id')}")
    print(f"published    : {sn.get('publishedAt')}")
    print(f"subscribers  : {st.get('subscriberCount')} (hidden={st.get('hiddenSubscriberCount')})")
    print(f"total views  : {st.get('viewCount')}")
    print(f"video count  : {st.get('videoCount')}")

    status, pl = http(
        "GET",
        "https://www.googleapis.com/youtube/v3/playlistItems"
        f"?part=snippet,contentDetails&maxResults=15&playlistId={uploads}",
        headers=auth,
    )
    if status != 200:
        print(f"PLAYLIST FAILED: HTTP {status} {pl}")
        return 0
    vids = pl.get("items", [])
    ids = [v["contentDetails"]["videoId"] for v in vids]
    stats_by_id: dict[str, dict] = {}
    if ids:
        status, vd = http(
            "GET",
            "https://www.googleapis.com/youtube/v3/videos"
            f"?part=status,statistics&id={','.join(ids)}",
            headers=auth,
        )
        if status == 200:
            for v in vd.get("items", []):
                stats_by_id[v["id"]] = v

    print(f"\n=== RECENT UPLOADS ({len(vids)}) ===")
    for v in vids:
        vid = v["contentDetails"]["videoId"]
        title = v["snippet"]["title"]
        pub = v["contentDetails"].get("videoPublishedAt", "-")
        meta = stats_by_id.get(vid, {})
        priv = meta.get("status", {}).get("privacyStatus", "?")
        views = meta.get("statistics", {}).get("viewCount", "?")
        print(f"[{priv:7}] {pub[:10]}  views={views:>6}  {title[:60]}  ({vid})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
