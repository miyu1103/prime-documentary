#!/usr/bin/env python3
"""One trustworthy list of the channel's videos, shared by every tool that touches YouTube.

Why this module exists, measured 2026-08-03:

    uploads playlist -> 115 ids, 106 unique      <- returns 9 duplicates and OMITS 9 videos
    search forMine   -> 115 unique ids           <- contains all 9 of the missing ones

The uploads playlist is the documented way to enumerate a channel and it is what every script
here used. It silently dropped nine videos, three of them published long-forms (EP34 rolin,
EP35 hinders, EP37 florence). The consequence was not cosmetic: `daily_funnel_sync` concluded
those episodes were "not yet public" and refused to link 15 published Shorts to them, so those
Shorts sat with a dead-end description for days while their destination was live the whole time.

So: never enumerate from one index. Take the union of both, and say so out loud when they differ.

Quota: playlistItems is 1 unit per page, search.list is 100 per page. A full sweep of this
channel is ~3 + ~300 units against a 10,000/day allowance.

Usage:
    from yt_channel_index import authorize, list_video_ids, fetch_videos, iso_seconds
    auth = authorize(ROOT)
    ids = list_video_ids(auth)
    vids = fetch_videos(auth, ids)
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://www.googleapis.com/youtube/v3"


def read_env(root: Path) -> dict[str, str]:
    """Parse .env into a dict. Values are never logged by anything in this module."""
    out: dict[str, str] = {}
    for line in (root / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def http(method: str, url: str, *, headers: dict | None = None,
         form: dict | None = None, body: dict | None = None) -> tuple[int, dict]:
    data = urllib.parse.urlencode(form).encode() if form else (
        json.dumps(body).encode() if body is not None else None)
    h = dict(headers or {})
    if body is not None:
        h["Content-Type"] = "application/json"
    try:
        req = urllib.request.Request(url, data=data, method=method, headers=h)
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode() or "{}")


def authorize(root: Path) -> dict[str, str]:
    """Exchange the stored refresh token for an access token; return an auth header dict."""
    e = read_env(root)
    st, tk = http("POST", "https://oauth2.googleapis.com/token", form={
        "client_id": e["YOUTUBE_CLIENT_ID"], "client_secret": e["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": e["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    if st != 200:
        raise SystemExit(f"YouTube token refresh failed: HTTP {st}")
    return {"Authorization": f"Bearer {tk['access_token']}"}


def _uploads_playlist_ids(auth: dict) -> list[str]:
    st, ch = http("GET", f"{API}/channels?part=contentDetails&mine=true", headers=auth)
    if st != 200 or not ch.get("items"):
        raise SystemExit(f"channels.list failed: HTTP {st}")
    pid = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], ""
    while True:
        st, pl = http("GET", f"{API}/playlistItems?part=contentDetails&maxResults=50"
                             f"&playlistId={pid}{page}", headers=auth)
        if st != 200:
            raise SystemExit(f"playlistItems failed: HTTP {st}")
        ids += [i["contentDetails"]["videoId"] for i in pl.get("items", [])]
        nxt = pl.get("nextPageToken")
        if not nxt:
            return ids
        page = f"&pageToken={nxt}"


def _search_mine_ids(auth: dict) -> list[str]:
    ids, page = [], ""
    while True:
        st, s = http("GET", f"{API}/search?part=id&forMine=true&type=video"
                            f"&maxResults=50{page}", headers=auth)
        if st != 200:
            raise SystemExit(f"search.list failed: HTTP {st}")
        ids += [i["id"]["videoId"] for i in s.get("items", []) if i.get("id", {}).get("videoId")]
        nxt = s.get("nextPageToken")
        if not nxt:
            return ids
        page = f"&pageToken={nxt}"


CACHE = Path(__file__).resolve().parents[1] / "runs" / "_cache" / "yt_channel_index.json"
CACHE_TTL_SEC = 900


def _cache_read(ttl: int) -> list[str] | None:
    try:
        d = json.loads(CACHE.read_text(encoding="utf-8"))
        import time
        if time.time() - d["fetched_at"] <= ttl and d.get("ids"):
            return list(d["ids"])
    except Exception:
        pass
    return None


def _cache_write(ids: list[str]) -> None:
    import time
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE.with_suffix(".tmp")
    tmp.write_text(json.dumps({"fetched_at": time.time(), "ids": ids}), encoding="utf-8")
    tmp.replace(CACHE)


def list_video_ids(auth: dict, *, verbose: bool = True, ttl: int = CACHE_TTL_SEC) -> list[str]:
    """Every video id on the authenticated channel, from BOTH indexes unioned.

    Prints a warning whenever the two indexes disagree, because a silent disagreement is exactly
    what caused fifteen Shorts to keep a dead-end description for days.

    Cached for `ttl` seconds. `search.list` costs 100 quota units per page against a 10,000/day
    allowance — running five tools back to back burned roughly 1,500 units and exhausted the day's
    quota on 2026-08-03. The cache makes a working session cost one sweep instead of one per tool.
    Pass ttl=0 to force a fresh read (do that before anything that must not act on stale state).
    """
    if ttl > 0:
        cached = _cache_read(ttl)
        if cached is not None:
            if verbose:
                print(f"[yt_channel_index] {len(cached)} ids from cache (<{ttl}s old)",
                      file=sys.stderr)
            return cached

    playlist = _uploads_playlist_ids(auth)
    search = _search_mine_ids(auth)
    only_search = sorted(set(search) - set(playlist))
    only_playlist = sorted(set(playlist) - set(search))
    union = sorted(set(playlist) | set(search))
    if verbose and (only_search or only_playlist):
        print(f"[yt_channel_index] indexes disagree: uploads playlist {len(set(playlist))} unique "
              f"({len(playlist)} rows), search {len(set(search))} -> using union of {len(union)}",
              file=sys.stderr)
        if only_search:
            print(f"[yt_channel_index]   missing from uploads playlist: {', '.join(only_search)}",
                  file=sys.stderr)
        if only_playlist:
            print(f"[yt_channel_index]   missing from search: {', '.join(only_playlist)}",
                  file=sys.stderr)
    _cache_write(union)
    return union


def fetch_videos(auth: dict, ids: list[str], *,
                 part: str = "snippet,status,contentDetails") -> dict[str, dict]:
    """videos.list over any number of ids. The API caps `id` at 50, so this chunks and fails loud."""
    out: dict[str, dict] = {}
    uniq = list(dict.fromkeys(ids))
    for n in range(0, len(uniq), 50):
        chunk = uniq[n:n + 50]
        st, r = http("GET", f"{API}/videos?part={part}&id={','.join(chunk)}", headers=auth)
        if st != 200:
            raise SystemExit(f"videos.list failed on chunk {n // 50}: HTTP {st} "
                             f"{r.get('error', {}).get('message', '')[:160]}")
        for v in r.get("items", []):
            out[v["id"]] = v
    return out


def iso_seconds(iso: str) -> int:
    """PT#H#M#S -> seconds. Returns 0 for anything unparseable."""
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    a = authorize(root)
    v = fetch_videos(a, list_video_ids(a))
    longs = [x for x in v.values()
             if iso_seconds(x["contentDetails"]["duration"]) > 185
             and x["status"]["privacyStatus"] == "public"]
    print(f"{len(v)} videos on the channel | {len(longs)} public long-forms")
