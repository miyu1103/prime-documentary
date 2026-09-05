#!/usr/bin/env python3
"""Upload PD-2026-005-madoff final video to YouTube as PRIVATE first.

Guards:
  - APR-0004 approved for exact final hash
  - SHA256 of video and thumbnail match approved values
  - Channel allowlist check
  - privacyStatus forced to private
  - madeForKids false
  - containsSyntheticMedia true
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, sha256_file, upload_chunks

EP = "PD-2026-005-madoff"
EPDIR = ROOT / "episodes" / EP
META = EPDIR / "09_package" / "youtube_meta.final.v009.json"
APR = EPDIR / "approvals" / "APR-0004.json"
VIDEO = EPDIR / "08_edit" / "renders" / "review.final.v009.mp4"
THUMB = EPDIR / "09_package" / "thumbnail" / "thumbnail.final.v006_detail_clean_a.jpg"
EXPECTED_VIDEO = "3b329905352bc4cd43a045bce4fee57443ff807e532b87bfac220f71d121e287"
EXPECTED_THUMB = "83ddba7f4cf896394a3583485f581a7ff6974dc8e18e28a96b64d06ec8a02743"


def initiate_upload_madoff(token: str, meta: dict, file_size: int) -> str:
    snippet = {
        "title": meta["title"],
        "description": meta["description"],
        "tags": meta.get("tags", []),
        "categoryId": meta.get("categoryId", "27"),
        "defaultLanguage": meta.get("defaultLanguage", "en"),
        "defaultAudioLanguage": meta.get("defaultAudioLanguage", "en"),
    }
    status = {
        "privacyStatus": "private",
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": True,
        "license": "youtube",
        "embeddable": True,
        "publicStatsViewable": True,
    }
    body = json.dumps({"snippet": snippet, "status": status}).encode("utf-8")
    url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4",
        "X-Upload-Content-Length": str(file_size),
    }, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        upload_url = resp.headers.get("Location", "")
    if not upload_url.startswith("https://www.googleapis.com/"):
        raise RuntimeError(f"Unexpected upload URL host: {upload_url[:80]}")
    return upload_url


def set_thumbnail(token: str, video_id: str, path: Path) -> dict:
    content_type = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
    req = urllib.request.Request(url, data=path.read_bytes(), headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": content_type,
    }, method="POST")
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_video_status(token: str, video_id: str) -> dict:
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    apr = json.loads(APR.read_text("utf-8"))
    if apr.get("decision") != "approved":
        print(f"BLOCKED: APR-0004 decision={apr.get('decision')!r}")
        return 1
    print("OK APR-0004 approved")

    if not VIDEO.exists():
        print(f"BLOCKED: missing video {VIDEO}")
        return 1
    if not THUMB.exists():
        print(f"BLOCKED: missing thumbnail {THUMB}")
        return 1

    actual_video = sha256_file(VIDEO)
    actual_thumb = sha256_file(THUMB)
    if actual_video != EXPECTED_VIDEO:
        print(f"BLOCKED: video hash mismatch\nexpected {EXPECTED_VIDEO}\nactual   {actual_video}")
        return 1
    if actual_thumb != EXPECTED_THUMB:
        print(f"BLOCKED: thumbnail hash mismatch\nexpected {EXPECTED_THUMB}\nactual   {actual_thumb}")
        return 1
    print("OK exact video/thumbnail hashes verified")

    meta = json.loads(META.read_text("utf-8"))
    print(f"OK title: {meta['title']}")
    print("OK upload status will be PRIVATE, madeForKids=false, containsSyntheticMedia=true")

    if args.dry_run:
        print("DRY_RUN_OK no upload performed")
        return 0

    env = load_env()
    token = _access_token(env)
    print("OK access token obtained")
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        print(f"BLOCKED: channel {channel_id!r} not allowlisted {CHANNEL_ALLOWLIST}")
        return 1
    print(f"OK channel allowlisted: {channel_id}")

    upload_url = initiate_upload_madoff(token, meta, VIDEO.stat().st_size)
    print(f"OK resumable upload session started; uploading {VIDEO.stat().st_size/1e6:.0f} MB PRIVATE")
    video_id = upload_chunks(upload_url, token, VIDEO)
    if not video_id:
        print("FAILED: upload returned no video id")
        return 1
    print(f"OK uploaded private video_id={video_id}")

    thumb_status = None
    thumb_error = None
    try:
        thumb_status = set_thumbnail(token, video_id, THUMB)
        print("OK thumbnail set")
    except Exception as exc:
        thumb_error = str(exc)
        print(f"WARN thumbnail set failed; set manually: {thumb_error}")

    status = get_video_status(token, video_id)
    result = {
        "episode_id": EP,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "privacy": "private",
        "channel_id": channel_id,
        "video_file": str(VIDEO),
        "video_sha256": actual_video,
        "thumbnail_file": str(THUMB),
        "thumbnail_sha256": actual_thumb,
        "thumbnail_set": thumb_status is not None,
        "thumbnail_status": thumb_status,
        "thumbnail_error": thumb_error,
        "youtube_status": status,
        "youtube_meta": str(META),
        "approval_ref": "APR-0004",
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "containsSyntheticMedia": True,
        "madeForKids": False,
    }
    out = EPDIR / "09_package" / "upload_result.final.v009.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"RESULT {out.relative_to(ROOT)}")
    print(f"PRIVATE_URL https://youtu.be/{video_id}")
    print(f"STUDIO_URL https://studio.youtube.com/video/{video_id}/edit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
