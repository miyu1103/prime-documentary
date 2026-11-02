"""Idempotent: add 2 videos to playlists + upload English captions to 2 videos.

Writes only (no delete, no privacy change, no publish). force-ssl scope.
- Playlist insert skipped if the video is already in the target playlist.
- Caption insert skipped if a non-draft English track already exists.
Secrets never printed.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
EP = ROOT / "episodes"

PLAYLIST_ADDS = [
    # video_id, playlist_id, label
    ("sphERPA4gAc", "PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P", "Madoff -> Fraud, Finance & Power"),
    ("bYcqabvvxak", "PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9", "Terry -> Landmark Rights Cases"),
]
CAPTION_ADDS = [
    ("bYcqabvvxak", EP / "PD-2026-006-terry/08_edit/captions.final.v003.srt", "Terry"),
    ("sphERPA4gAc", EP / "PD-2026-005-madoff/08_edit/captions.review_proxy.v003.srt", "Madoff"),
]


def load_env():
    env = {}
    for l in ENV.read_text(encoding="utf-8").splitlines():
        l = l.strip()
        if l and not l.startswith("#") and "=" in l:
            k, v = l.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def http(m, u, headers=None, data=None):
    req = urllib.request.Request(u, data=data, method=m, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def token(env):
    body = urllib.parse.urlencode({
        "client_id": env["YOUTUBE_CLIENT_ID"], "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    s, b = http("POST", "https://oauth2.googleapis.com/token", data=body)
    if s != 200:
        raise SystemExit(f"token failed {s} {b}")
    return b["access_token"]


def playlist_has_video(auth, playlist_id, video_id):
    page = ""
    while True:
        s, b = http("GET", "https://www.googleapis.com/youtube/v3/playlistItems"
                    f"?part=contentDetails&maxResults=50&playlistId={playlist_id}{page}", headers=auth)
        for it in b.get("items", []):
            if it["contentDetails"]["videoId"] == video_id:
                return True
        tok = b.get("nextPageToken")
        if not tok:
            return False
        page = f"&pageToken={tok}"


def add_to_playlist(auth, playlist_id, video_id):
    payload = json.dumps({"snippet": {"playlistId": playlist_id,
                                      "resourceId": {"kind": "youtube#video", "videoId": video_id}}}).encode()
    return http("POST", "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet",
                headers={**auth, "Content-Type": "application/json"}, data=payload)


def existing_en_caption(auth, video_id):
    s, b = http("GET", f"https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={video_id}", headers=auth)
    for it in b.get("items", []):
        sn = it["snippet"]
        if sn.get("language") == "en" and sn.get("trackKind") != "asr" and not sn.get("isDraft", False):
            return it
    return None


def upload_caption(auth, video_id, srt_path):
    boundary = f"pd_cap_{video_id}"
    meta = {"snippet": {"videoId": video_id, "language": "en", "name": "English", "isDraft": False}}
    body = b"".join([
        f"--{boundary}\r\n".encode(),
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
        json.dumps(meta, ensure_ascii=False).encode("utf-8"), b"\r\n",
        f"--{boundary}\r\n".encode(),
        b"Content-Type: application/octet-stream\r\n\r\n",
        srt_path.read_bytes(), b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ])
    return http("POST",
                "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
                headers={**auth, "Content-Type": f"multipart/related; boundary={boundary}"}, data=body)


def main():
    env = load_env()
    auth = {"Authorization": f"Bearer {token(env)}"}

    print("=== 1) PLAYLIST ADDS ===")
    for vid, pid, label in PLAYLIST_ADDS:
        if playlist_has_video(auth, pid, vid):
            print(f"  SKIP (already in playlist): {label}")
            continue
        s, b = add_to_playlist(auth, pid, vid)
        if s in (200, 201):
            print(f"  ADDED: {label}  itemId={b.get('id')}")
        else:
            print(f"  FAIL {s}: {label}  {b.get('error', {}).get('message', b)}")

    print("\n=== 2) CAPTION UPLOADS ===")
    for vid, srt, label in CAPTION_ADDS:
        if not srt.exists():
            print(f"  FAIL (no SRT): {label}  {srt}")
            continue
        ex = existing_en_caption(auth, vid)
        if ex:
            print(f"  SKIP (en caption exists): {label}  id={ex['id']}")
            continue
        s, b = upload_caption(auth, vid, srt)
        if s in (200, 201):
            print(f"  UPLOADED: {label}  captionId={b.get('id')}  ({srt.name})")
        else:
            print(f"  FAIL {s}: {label}  {b.get('error', {}).get('message', b)}")
        time.sleep(3)

    print("\n=== VERIFY captions now present ===")
    for vid, _, label in CAPTION_ADDS:
        s, b = http("GET", f"https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={vid}", headers=auth)
        langs = [f"{c['snippet'].get('language')}/{c['snippet'].get('trackKind')}" for c in b.get("items", [])]
        print(f"  {label} ({vid}): {langs}")


if __name__ == "__main__":
    main()
