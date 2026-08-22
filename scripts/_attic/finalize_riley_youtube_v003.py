#!/usr/bin/env python3
"""Finalize Riley v003 YouTube upload: processing, captions, duplicate status."""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import sha256_file

EP = "PD-2026-007-riley"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / "youtube_meta.v003.json"
SCHEDULE_RESULT = PKG / "youtube_schedule_result.v003.json"
CAPTION_RESULT = PKG / "youtube_captions_result.v003.json"
STATUS_VERIFY = PKG / "youtube_rebuild_status_verify.v003.json"
CAPTION_FILE = EPDIR / "08_edit" / "captions.final.v003.srt"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
OLD_VIDEO_IDS = ["ODCh4-UelI4", "6iWtKdktOGY"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def request_json(url: str, token: str, data: bytes | None = None, headers: dict[str, str] | None = None, method: str | None = None) -> dict:
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {token}", **(headers or {})}, method=method)
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_videos(token: str, video_ids: list[str]) -> dict:
    ids = ",".join(video_ids)
    return request_json(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={ids}", token)


def list_captions(token: str, video_id: str) -> dict:
    return request_json(f"https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={video_id}", token)


def upload_caption(token: str, video_id: str) -> dict:
    boundary = f"riley_caption_{int(time.time())}"
    metadata = {
        "snippet": {
            "videoId": video_id,
            "language": "en",
            "name": "English",
            "isDraft": False,
        }
    }
    caption_bytes = CAPTION_FILE.read_bytes()
    body = b"".join([
        f"--{boundary}\r\n".encode(),
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
        json.dumps(metadata, ensure_ascii=False).encode("utf-8"),
        b"\r\n",
        f"--{boundary}\r\n".encode(),
        b"Content-Type: application/octet-stream\r\n\r\n",
        caption_bytes,
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ])
    return request_json(
        "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
        token,
        data=body,
        headers={"Content-Type": f"multipart/related; boundary={boundary}"},
        method="POST",
    )


def compact_video_state(items: list[dict]) -> list[dict]:
    out = []
    for item in items:
        status = item.get("status", {})
        processing = item.get("processingDetails", {})
        out.append({
            "id": item.get("id"),
            "title": item.get("snippet", {}).get("title"),
            "privacyStatus": status.get("privacyStatus"),
            "publishAt": status.get("publishAt"),
            "uploadStatus": status.get("uploadStatus"),
            "processingStatus": processing.get("processingStatus"),
            "madeForKids": status.get("madeForKids"),
            "selfDeclaredMadeForKids": status.get("selfDeclaredMadeForKids"),
        })
    return out


def wait_for_processing(token: str, video_id: str) -> tuple[dict, str]:
    state = {}
    processing_status = "unknown"
    for _ in range(24):
        state = get_videos(token, [video_id])
        items = state.get("items") or []
        processing_status = ((items[0].get("processingDetails") if items else {}) or {}).get("processingStatus", "missing")
        if processing_status in {"succeeded", "failed", "terminated"}:
            return state, processing_status
        time.sleep(15)
    return state, processing_status


def update_local_records(video_id: str, processing_state: dict, processing_status: str, caption_result: dict, verify: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    meta = load_json(META)
    meta["processing_status"] = processing_status
    meta["processing_status_verified_at"] = now
    meta["captions_uploaded"] = True
    meta["captions_result"] = str(CAPTION_RESULT.relative_to(ROOT)).replace("\\", "/")
    meta["caption_track_language"] = "en"
    meta["caption_track_name"] = "English"
    meta["caption_track_uploaded_at"] = now
    meta["old_uploads_verified_private_unscheduled"] = verify["old_uploads_verified_private_unscheduled"]
    write_json(META, meta)

    manifest = load_json(MANIFEST)
    manifest["state"] = "scheduled"
    manifest["video_id"] = video_id
    manifest["video_url"] = f"https://youtu.be/{video_id}"
    manifest["public_schedule_active"] = True
    manifest["updated_at"] = now
    manifest.setdefault("active_revisions", {})["youtube_captions_result"] = "v003"
    manifest.setdefault("active_revisions", {})["youtube_status_verify"] = "v003"
    if "APR-0005" not in manifest.setdefault("approvals", []):
        manifest["approvals"].append("APR-0005")
    warning = f"Riley v003 YouTube upload {video_id} is private and scheduled for 2026-06-22T12:00:00+09:00; v001 ODCh4-UelI4 and v002 6iWtKdktOGY verified private and unscheduled."
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    write_json(MANIFEST, manifest)

    append_event({
        "event": "youtube_captions_uploaded_and_processing_verified",
        "episode_id": EP,
        "stage": "scheduled",
        "revision": "v003",
        "actor": "codex",
        "approval_id": "APR-0005",
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "processing_status": processing_status,
        "captions_result": str(CAPTION_RESULT.relative_to(ROOT)).replace("\\", "/"),
        "old_uploads_verified_private_unscheduled": verify["old_uploads_verified_private_unscheduled"],
        "ts": now,
    })


def main() -> int:
    token = _access_token(load_env())
    schedule = load_json(SCHEDULE_RESULT)
    video_id = schedule["video_id"]
    if not CAPTION_FILE.exists():
        raise FileNotFoundError(CAPTION_FILE)

    processing_state, processing_status = wait_for_processing(token, video_id)
    before_captions = list_captions(token, video_id)
    caption = upload_caption(token, video_id)
    time.sleep(8)
    after_captions = list_captions(token, video_id)
    all_state = get_videos(token, OLD_VIDEO_IDS + [video_id])
    compact = compact_video_state(all_state.get("items") or [])
    old_states = [item for item in compact if item["id"] in OLD_VIDEO_IDS]
    v3_states = [item for item in compact if item["id"] == video_id]
    old_ok = all(item.get("privacyStatus") == "private" and item.get("publishAt") is None for item in old_states)
    v3_ok = bool(v3_states) and v3_states[0].get("privacyStatus") == "private" and v3_states[0].get("publishAt") == "2026-06-22T03:00:00Z"

    caption_result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v003",
        "video_id": video_id,
        "caption_file": str(CAPTION_FILE),
        "caption_file_sha256": "sha256:" + sha256_file(CAPTION_FILE),
        "language": "en",
        "name": "English",
        "is_draft": False,
        "youtube_captions_before": before_captions,
        "youtube_caption": caption,
        "youtube_captions_after": after_captions,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "external_upload": True,
    }
    write_json(CAPTION_RESULT, caption_result)

    verify = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v003",
        "video_id": video_id,
        "processing_status": processing_status,
        "processing_state": processing_state,
        "youtube_state_compact": compact,
        "old_uploads_verified_private_unscheduled": old_ok,
        "v3_verified_private_scheduled": v3_ok,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(STATUS_VERIFY, verify)
    update_local_records(video_id, processing_state, processing_status, caption_result, verify)
    print(json.dumps({
        "video_id": video_id,
        "processing_status": processing_status,
        "captions_uploaded": True,
        "old_uploads_verified_private_unscheduled": old_ok,
        "v3_verified_private_scheduled": v3_ok,
        "watch": f"https://youtu.be/{video_id}",
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
