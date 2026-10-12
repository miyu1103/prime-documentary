#!/usr/bin/env python3
"""Publish SHORT #6 (Terry v. Ohio) to YouTube Shorts (US English).

Modeled on upload_short07_youtube_public.py. Uploads the cover-first render (flashy thumbnail baked
into a 0.7s front frame, since Shorts does not reliably surface an API thumbnail), also sets the
custom thumbnail via API, declares synthetic media, and only targets the allowlisted channel.
Idempotent guard: refuses if a publish result already exists. Records actual SHA-256 of the artifacts.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
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

EP = "PD-2026-006-terry"
SHORT_ID = "short06"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
VIDEO = ROOT / "remotion" / "out" / "short06_yt_coverfirst.mp4"
THUMB = ROOT / "remotion" / "out" / "short06_thumb.png"
PUBLISH_MD = EPDIR / "short06_publish.md"
RESULT = PKG / "short06_youtube_publish_result.v001.json"
STATUS_VERIFY = PKG / "short06_youtube_status_verify.v001.json"
EVENTS = EPDIR / "events" / "events.jsonl"

TITLE = "Police Can Stop & Frisk You Without an Arrest #Shorts"
DESCRIPTION = """Police can stop you and pat you down — even without arresting you.
No warrant. No proof of a crime. All they need is "reasonable suspicion."
In 1968, the Supreme Court allowed it 8-1, and "stop and frisk" was born (Terry v. Ohio).

Watch the full story on the channel.

#Shorts #SupremeCourt #Law #StopAndFrisk #FourthAmendment #Police #Rights #Documentary
"""
TAGS = [
    "Shorts",
    "Supreme Court",
    "Law",
    "Stop and Frisk",
    "Fourth Amendment",
    "Police",
    "Rights",
    "Documentary",
]


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def request_json(url: str, token: str, *, timeout: int = 180) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def initiate_upload(token: str, file_size: int) -> str:
    snippet = {
        "title": TITLE,
        "description": DESCRIPTION.rstrip(),
        "tags": TAGS,
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
    }
    status = {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": True,
        "license": "youtube",
        "embeddable": True,
        "publicStatsViewable": True,
    }
    body = json.dumps({"snippet": snippet, "status": status}).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(file_size),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        upload_url = resp.headers.get("Location", "")
    if not upload_url.startswith("https://www.googleapis.com/"):
        raise RuntimeError(f"Unexpected upload URL host: {upload_url[:80]}")
    return upload_url


def set_thumbnail(token: str, video_id: str) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=THUMB.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_video_state(token: str, video_id: str) -> dict:
    return request_json(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        token,
        timeout=60,
    )


def compact_video_state(state: dict) -> dict:
    items = state.get("items") or []
    item = items[0] if items else {}
    status = item.get("status", {})
    processing = item.get("processingDetails", {})
    snippet = item.get("snippet", {})
    return {
        "id": item.get("id"),
        "title": snippet.get("title"),
        "privacyStatus": status.get("privacyStatus"),
        "uploadStatus": status.get("uploadStatus"),
        "processingStatus": processing.get("processingStatus"),
        "containsSyntheticMedia": status.get("containsSyntheticMedia"),
        "madeForKids": status.get("madeForKids"),
        "selfDeclaredMadeForKids": status.get("selfDeclaredMadeForKids"),
    }


def wait_for_processing(token: str, video_id: str) -> tuple[dict, str]:
    state: dict = {}
    processing_status = "unknown"
    for _ in range(16):
        state = get_video_state(token, video_id)
        processing_status = compact_video_state(state).get("processingStatus") or "unknown"
        if processing_status in {"succeeded", "failed", "terminated"}:
            break
        time.sleep(10)
    return state, processing_status


def verify_preconditions() -> None:
    if RESULT.exists():
        raise RuntimeError(f"Existing short06 YouTube publish result found; refusing duplicate upload: {RESULT.relative_to(ROOT)}")
    for path in (VIDEO, THUMB, PUBLISH_MD):
        if not path.exists():
            raise RuntimeError(f"Missing required artifact: {path}")


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    verify_preconditions()
    video_sha = sha256_file(VIDEO)
    thumb_sha = sha256_file(THUMB)
    print(f"OK short artifact: {VIDEO.relative_to(ROOT)} ({VIDEO.stat().st_size/1e6:.1f} MB) sha={video_sha[:12]}")
    print(f"OK thumbnail: {THUMB.relative_to(ROOT)} sha={thumb_sha[:12]}")
    print(f"OK title: {TITLE}")
    print("OK upload target: public YouTube Shorts, madeForKids=false, containsSyntheticMedia=true")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel allowlisted: {channel_id}")

    upload_url = initiate_upload(token, VIDEO.stat().st_size)
    print(f"OK resumable upload started; uploading {VIDEO.stat().st_size / 1e6:.1f} MB")
    video_id = upload_chunks(upload_url, token, VIDEO)
    if not video_id:
        raise RuntimeError("Upload returned no video_id")
    print(f"OK public upload complete video_id={video_id}")

    thumb_status: dict | None = None
    thumb_error: dict | None = None
    try:
        thumb_status = set_thumbnail(token, video_id)
        print("OK thumbnail set")
    except urllib.error.HTTPError as exc:
        thumb_error = {"code": exc.code, "reason": exc.reason, "body": exc.read().decode("utf-8", errors="replace")}
        print(f"WARN thumbnail set failed HTTP {exc.code}; cover frame still shows the thumbnail")

    state, processing_status = wait_for_processing(token, video_id)
    compact = compact_video_state(state)
    privacy = compact.get("privacyStatus")
    if privacy != "public":
        raise RuntimeError(f"Upload completed but privacy is not public: {privacy!r}")

    now = datetime.now(timezone.utc).isoformat()
    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "short_id": SHORT_ID,
        "platform": "youtube",
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": privacy,
        "title": TITLE,
        "description": DESCRIPTION.rstrip(),
        "tags": TAGS,
        "video_file": str(VIDEO.relative_to(ROOT)).replace("\\", "/"),
        "video_sha256": "sha256:" + video_sha,
        "thumbnail_file": str(THUMB.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": "sha256:" + thumb_sha,
        "thumbnail_set": thumb_status is not None,
        "thumbnail_status": thumb_status,
        "thumbnail_error": thumb_error,
        "cover_frame_baked_in": True,
        "cover_frame_duration_sec": 0.7,
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_publish": True,
        "owner_instruction": "投稿して。サムネイルは派手に。",
        "published_at": now,
        "youtube_state_compact": compact,
        "youtube_state": state,
    }
    write_json(RESULT, result)
    write_json(
        STATUS_VERIFY,
        {
            "schema_version": "1.0.0",
            "episode_id": EP,
            "short_id": SHORT_ID,
            "platform": "youtube",
            "video_id": video_id,
            "watch": f"https://youtu.be/{video_id}",
            "processing_status": processing_status,
            "youtube_state_compact": compact,
            "verified_public": privacy == "public",
            "checked_at": now,
        },
    )
    append_event(
        {
            "event": "short06_youtube_published",
            "episode_id": EP,
            "short_id": SHORT_ID,
            "stage": "published",
            "actor": "claude",
            "video_id": video_id,
            "watch": f"https://youtu.be/{video_id}",
            "studio": f"https://studio.youtube.com/video/{video_id}/edit",
            "privacy": privacy,
            "thumbnail_set": thumb_status is not None,
            "result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
            "ts": now,
        }
    )
    print(json.dumps(
        {
            "video_id": video_id,
            "watch": f"https://youtu.be/{video_id}",
            "studio": f"https://studio.youtube.com/video/{video_id}/edit",
            "privacy": privacy,
            "processing_status": processing_status,
            "thumbnail_set": thumb_status is not None,
            "result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
        },
        indent=2, ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
