#!/usr/bin/env python3
"""Snapshot the live title/description/tags of every public Short BEFORE anything rewrites them.

videos.update replaces the snippet wholesale — a partial write silently drops whatever it omits,
and the previous text is gone from YouTube with no undo. This is the rollback.

Read-only. Costs 1 quota unit per 50 videos.

Usage: py -3.11 scripts/backup_short_metadata.py
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs" / "short_funnel"


def load_env() -> dict:
    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
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


def secs(d: str) -> int:
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    env = load_env()
    st, b = http("POST", "https://oauth2.googleapis.com/token", form={
        "client_id": env["YOUTUBE_CLIENT_ID"], "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    if st != 200:
        sys.exit(f"token failed HTTP {st}")
    auth = {"Authorization": f"Bearer {b['access_token']}"}

    # A backup that silently omits videos is not a backup. The uploads playlist alone omitted nine
    # on 2026-08-03, so enumeration comes from the shared, unioned index.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from yt_channel_index import list_video_ids
    ids = list_video_ids(auth)

    rows = []
    for n in range(0, len(ids), 50):
        chunk = ids[n:n + 50]
        st, vd = http("GET", "https://www.googleapis.com/youtube/v3/videos"
                      "?part=snippet,status,contentDetails,statistics"
                      f"&id={','.join(chunk)}", headers=auth)
        if st != 200:
            sys.exit(f"videos.list HTTP {st}: {vd.get('error', {}).get('message')}")
        for v in vd.get("items", []):
            sn = v["snippet"]
            rows.append({
                "id": v["id"],
                "title": sn.get("title"),
                "description": sn.get("description"),
                "tags": sn.get("tags", []),
                "categoryId": sn.get("categoryId"),
                "defaultLanguage": sn.get("defaultLanguage"),
                "defaultAudioLanguage": sn.get("defaultAudioLanguage"),
                "privacy": v["status"].get("privacyStatus"),
                "publishAt": v["status"].get("publishAt"),
                "duration_sec": secs(v["contentDetails"].get("duration")),
                "views": int(v.get("statistics", {}).get("viewCount") or 0),
            })

    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUT / f"metadata_backup.{stamp}.json"
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    shorts = [r for r in rows if 0 < r["duration_sec"] <= 185]
    longs = [r for r in rows if r["duration_sec"] > 185]
    pub_shorts = [r for r in shorts if r["privacy"] == "public"]
    with_url = [r for r in pub_shorts
                if "youtube.com/watch" in "\n".join((r["description"] or "").splitlines()[:3])]
    print(f"backed up {len(rows)} videos -> {path.relative_to(ROOT)}")
    print(f"  shorts {len(shorts)} ({len(pub_shorts)} public) | long-forms {len(longs)}")
    print(f"  public Shorts whose first 3 description lines already link out: "
          f"{len(with_url)} / {len(pub_shorts)}")
    print(f"  total views sitting on those Shorts: {sum(r['views'] for r in pub_shorts):,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
