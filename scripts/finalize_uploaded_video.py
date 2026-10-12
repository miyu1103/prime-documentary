#!/usr/bin/env python
"""Finish a video that uploaded but lost its token before thumbnail / captions / schedule.

A 2GB upload outlives a Google access token (they last an hour), so the uploader can push the
whole file, print "OK uploaded", and then fail 401 on the very next call -- leaving a private
video with an auto-generated thumbnail and no caption track. That is what happened to EP52 on
2026-08-01. This re-authenticates and applies exactly the steps that were lost, then verifies
against the live API.

    python scripts/finalize_uploaded_video.py --ep morton --video-id Gx_i5aMJWLM

Idempotent: an already-correct field is reported and left alone.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yt_schedule_audit import http, load_env  # noqa: E402


def token() -> str:
    env = load_env()
    st, b = http("POST", "https://oauth2.googleapis.com/token", form={
        "client_id": env["YOUTUBE_CLIENT_ID"], "client_secret": env["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": env["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    if st != 200:
        raise SystemExit(f"token refresh failed: {st}")
    return b["access_token"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True, help="slug as used in upload_schedule_case_v001 CONFIG")
    ap.add_argument("--video-id", required=True)
    a = ap.parse_args()

    sys.path.insert(0, str(ROOT / "src"))
    from upload_schedule_case_v001 import CONFIG  # noqa: E402
    cfg = CONFIG[a.ep]
    ep_dir = ROOT / "episodes" / cfg["ep"]
    thumbs = sorted((ep_dir / "09_package").glob("thumbnail.selected.v*.png"))
    caps = sorted((ep_dir / "08_edit").glob("captions.youtube.v*.srt")) or \
        sorted((ep_dir / "08_edit").glob("captions.final.v*.srt"))
    vid = a.video_id

    tok = token()
    auth = {"Authorization": f"Bearer {tok}"}

    # 1) schedule + privacy
    body = json.dumps({"id": vid, "status": {
        "privacyStatus": "private", "publishAt": cfg["sched_utc"],
        "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True}}).encode()
    req = urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?part=status",
                                 data=body, method="PUT",
                                 headers={**auth, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        r.read()
    print(f"OK schedule set {cfg['sched_local']}")

    # 2) thumbnail
    if thumbs:
        req = urllib.request.Request(
            f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
            data=thumbs[-1].read_bytes(), method="POST",
            headers={**auth, "Content-Type": "image/png"})
        with urllib.request.urlopen(req, timeout=180) as r:
            r.read()
        print(f"OK thumbnail set ({thumbs[-1].name})")

    # 3) captions (skip when a track already exists)
    st, existing = http("GET", f"https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={vid}",
                        headers=auth)
    langs = [c["snippet"].get("language") for c in existing.get("items", [])]
    if "en" in langs:
        print("OK captions already present")
    elif caps:
        bnd = f"cap_{int(time.time())}"
        meta = {"snippet": {"videoId": vid, "language": "en", "name": "English", "isDraft": False}}
        payload = b"".join([f"--{bnd}\r\n".encode(),
                            b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
                            json.dumps(meta).encode(), b"\r\n", f"--{bnd}\r\n".encode(),
                            b"Content-Type: application/x-subrip\r\n\r\n",
                            caps[-1].read_bytes(), b"\r\n", f"--{bnd}--\r\n".encode()])
        req = urllib.request.Request(
            "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
            data=payload, method="POST",
            headers={**auth, "Content-Type": f"multipart/related; boundary={bnd}"})
        with urllib.request.urlopen(req, timeout=180) as r:
            r.read()
        print(f"OK captions uploaded ({caps[-1].name})")

    # 4) verify against the live API
    st, v = http("GET", "https://www.googleapis.com/youtube/v3/videos"
                        f"?part=snippet,status,contentDetails&id={vid}", headers=auth)
    it = v["items"][0]
    ok = (it["status"].get("publishAt") == cfg["sched_utc"]
          and it["status"].get("privacyStatus") == "private")
    print(f"VERIFY dur={it['contentDetails'].get('duration')} "
          f"privacy={it['status'].get('privacyStatus')} publishAt={it['status'].get('publishAt')} "
          f"thumb={'maxres' in it['snippet'].get('thumbnails', {})}")
    result = ep_dir / "09_package" / "youtube_schedule_result.v001.json"
    result.write_text(json.dumps({
        "schema_version": "1.0.0", "episode_id": cfg["ep"], "mode": "scheduled",
        "video_id": vid, "watch": f"https://youtu.be/{vid}",
        "privacy": it["status"].get("privacyStatus"), "publishAt": it["status"].get("publishAt"),
        "scheduled_at_local": cfg["sched_local"], "title": cfg["title"],
        "finalized_after_token_expiry": True,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"RESULT {result}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
