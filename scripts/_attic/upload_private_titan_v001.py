#!/usr/bin/env python3
"""Upload PD-2026-016 Titan to YouTube as private only.

Side effects in non-dry-run mode:
- refreshes YouTube OAuth token
- verifies the authenticated channel is allowlisted
- creates a private YouTube upload, with containsSyntheticMedia=true
- sets the selected thumbnail
- attempts sidecar caption upload
- writes local result/status JSON and updates v009 package records

This does not set publishAt and does not make the video public.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, sha256_file, upload_chunks


EP = "PD-2026-016-titan"
REV = "v009"
CUT_REV = "v008"
APR_ID = "APR-0002"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
APPROVALS = EPDIR / "approvals"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"

META = PKG / f"youtube_meta.{REV}.json"
FINAL_DELIVERY = PKG / f"final_delivery.{REV}.json"
RIGHTS = PKG / f"rights_manifest.{REV}.json"
FINAL_QC = EPDIR / "08_edit" / "renders" / "final.v008.qc.json"
CAPTION_QC = EPDIR / "08_edit" / "captions.v008.qc.json"
AUDIO_QC = EPDIR / "08_edit" / "audio_mix.v008.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v008.srt"
APR = APPROVALS / f"{APR_ID}.json"

RESULT = PKG / "youtube_private_upload_result.v001.json"
IN_PROGRESS = PKG / "youtube_upload_in_progress.v001.json"
STATUS_VERIFY = PKG / "youtube_status_verify.v001.json"
CAPTION_RESULT = PKG / "youtube_captions_result.v001.json"
THUMB_RESULT = PKG / "youtube_thumbnail_result.v001.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return "sha256:" + sha256_file(path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / value


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def upload_caption(token: str, video_id: str) -> dict:
    boundary = f"titan_caption_{int(time.time())}"
    metadata = json.dumps(
        {
            "snippet": {
                "videoId": video_id,
                "language": "en",
                "name": "Prime Documentary English captions",
                "isDraft": False,
            }
        },
        ensure_ascii=False,
    ).encode("utf-8")
    body = (
        f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n"
    ).encode("utf-8") + metadata + (
        f"\r\n--{boundary}\r\nContent-Type: application/x-subrip\r\n\r\n"
    ).encode("utf-8") + CAPTIONS.read_bytes() + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/related; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def set_thumbnail(token: str, video_id: str, path: Path) -> dict:
    content_type = mimetypes.guess_type(path.name)[0] or "image/png"
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=path.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": content_type},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_video_state(token: str, video_id: str) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def initiate_upload(token: str, meta: dict, file_size: int) -> str:
    snippet = {
        "title": meta["title"],
        "description": meta["description"].rstrip(),
        "tags": meta.get("tags", []),
        "categoryId": str(meta.get("categoryId", "27")),
        "defaultLanguage": meta.get("defaultLanguage", "en"),
        "defaultAudioLanguage": meta.get("defaultAudioLanguage", "en"),
    }
    status = {
        "privacyStatus": "private",
        "selfDeclaredMadeForKids": bool(meta.get("made_for_kids", False)),
        "containsSyntheticMedia": True,
        "license": "youtube",
        "embeddable": True,
        "publicStatsViewable": True,
    }
    body = json.dumps({"snippet": snippet, "status": status}, ensure_ascii=False).encode("utf-8")
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
        raise RuntimeError(f"Unexpected upload URL: {upload_url[:80]}")
    return upload_url


def verify_preconditions() -> tuple[dict, Path, Path]:
    existing = [p for p in (RESULT, IN_PROGRESS) if p.exists()]
    if existing:
        joined = ", ".join(rel(p) for p in existing)
        raise RuntimeError(f"Existing YouTube upload result/in-progress file found; refusing duplicate upload: {joined}")
    for path in (META, FINAL_DELIVERY, RIGHTS, FINAL_QC, CAPTION_QC, AUDIO_QC, CAPTIONS, APR, MANIFEST):
        if not path.exists():
            raise RuntimeError(f"Missing required file: {path}")
    apr = load_json(APR)
    if apr.get("decision") != "approved" or apr.get("target_type") != "package" or apr.get("target_revision") != REV:
        raise RuntimeError(f"{APR_ID} does not approve package {REV}")
    meta = load_json(META)
    video = resolve_path(meta["video_actual_path"])
    thumb = resolve_path(meta["thumbnail"])
    if not video.exists():
        raise RuntimeError(f"Missing video: {video}")
    if not thumb.exists():
        raise RuntimeError(f"Missing thumbnail: {thumb}")
    if meta.get("upload_performed") is not False or meta.get("publish_performed") is not False or meta.get("schedule_performed") is not False:
        raise RuntimeError("youtube_meta already marks upload, publish, or schedule performed")
    if meta.get("video_sha256") != sha(video):
        raise RuntimeError("youtube_meta video hash mismatch")
    if meta.get("thumbnail_sha256") != sha(thumb):
        raise RuntimeError("youtube_meta thumbnail hash mismatch")
    if meta.get("captions_sha256") != sha(CAPTIONS):
        raise RuntimeError("youtube_meta caption hash mismatch")
    for label, path in (("final", FINAL_QC), ("caption", CAPTION_QC), ("audio", AUDIO_QC)):
        qc = load_json(path)
        if qc.get("qc_status") != "pass":
            raise RuntimeError(f"{label} QC is not pass: {path}")
    return meta, video, thumb


def update_records(result: dict, thumb_status: dict, caption_result: dict | None, caption_error: str | None, state: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    video_id = result["video_id"]
    meta = load_json(META)
    meta.update(
        {
            "status": "private_uploaded_public_schedule_blocked_pending_2026_07_01_fact_recheck",
            "upload_performed": True,
            "publish_performed": False,
            "schedule_performed": False,
            "video_id": video_id,
            "video_url": result["watch"],
            "studio_url": result["studio"],
            "youtube_channel_id": result["channel_id"],
            "thumbnail_set": True,
            "thumbnail_result": rel(THUMB_RESULT),
            "captions_uploaded": caption_result is not None,
            "captions_result": rel(CAPTION_RESULT) if caption_result else None,
            "caption_error": caption_error,
            "private_upload_result": rel(RESULT),
            "status_verify": rel(STATUS_VERIFY),
            "processing_status_verified_at": now,
            "updated_at": now,
        }
    )
    write_json(META, meta)

    delivery = load_json(FINAL_DELIVERY)
    delivery.update(
        {
            "status": "private_uploaded_public_schedule_blocked_pending_2026_07_01_fact_recheck",
            "upload_performed": True,
            "publish_performed": False,
            "schedule_performed": False,
            "video_id": video_id,
            "watch": result["watch"],
            "studio": result["studio"],
            "youtube": {
                "video_id": video_id,
                "watch": result["watch"],
                "studio": result["studio"],
                "privacy": "private",
                "upload_performed": True,
                "schedule_performed": False,
                "public_immediate_publish": False,
                "result": rel(RESULT),
            },
            "updated_at": now,
        }
    )
    write_json(FINAL_DELIVERY, delivery)

    manifest = load_json(MANIFEST)
    manifest["state"] = "publish_approved"
    manifest["video_id"] = video_id
    manifest["video_url"] = result["watch"]
    manifest["updated_at"] = now
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "youtube_private_upload_result": "v001",
            "youtube_status_verify": "v001",
            "youtube_thumbnail_result": "v001",
            "youtube_captions_result": "v001" if caption_result else "v001",
        }
    )
    warning = f"Titan {CUT_REV} was uploaded privately to YouTube as {video_id}; public scheduling remains blocked until 2026-07-01 same-day fact re-check."
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    approvals = manifest.setdefault("approvals", [])
    if APR_ID not in approvals:
        approvals.append(APR_ID)
    write_json(MANIFEST, manifest)

    append_event(
        {
            "ts": now,
            "episode_id": EP,
            "stage": "youtube_private_upload",
            "event": "youtube_private_upload_completed",
            "revision": REV,
            "actor": "codex",
            "approval_id": APR_ID,
            "video_id": video_id,
            "watch": result["watch"],
            "studio": result["studio"],
            "privacy": "private",
            "thumbnail_set": True,
            "captions_uploaded": caption_result is not None,
            "caption_error": caption_error,
            "youtube_state": state,
            "note": "Private upload, thumbnail, and sidecar caption attempt completed. No public schedule or publish performed.",
        }
    )


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--adopt-video-id", help="Adopt an already-created private upload and continue thumbnail/caption/local records without re-uploading.")
    args = parser.parse_args(argv)

    meta, video, thumb = verify_preconditions()
    print(f"OK {APR_ID} approved for private upload package {REV}")
    print(f"OK title: {meta['title']}")
    print(f"OK video_sha256={sha(video)}")
    print(f"OK thumbnail_sha256={sha(thumb)}")
    print(f"OK captions_sha256={sha(CAPTIONS)}")
    print("OK upload will be private; containsSyntheticMedia=true; no publishAt will be set")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    print("OK access token obtained")
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel allowlisted: {channel_id}")

    if args.adopt_video_id:
        video_id = args.adopt_video_id.strip()
        state_before = get_video_state(token, video_id)
        items = state_before.get("items") or []
        if not items:
            raise RuntimeError(f"adopted video id not found: {video_id}")
        snippet = items[0].get("snippet", {})
        status = items[0].get("status", {})
        if snippet.get("title") != meta["title"]:
            raise RuntimeError(f"adopted video title mismatch: {snippet.get('title')!r}")
        if status.get("privacyStatus") != "private" or status.get("publishAt"):
            raise RuntimeError(f"adopted video is not unscheduled private: {status}")
        print(f"OK adopted existing private upload video_id={video_id}")
    else:
        upload_url = initiate_upload(token, meta, video.stat().st_size)
        print(f"OK resumable upload session started; uploading {video.stat().st_size / 1e6:.0f} MB")
        video_id = upload_chunks(upload_url, token, video)
        if not video_id:
            raise RuntimeError("Upload returned no video_id")
        print(f"OK private upload complete video_id={video_id}")

    progress = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "approval_ref": APR_ID,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "status": "uploaded_before_thumbnail_caption_verify",
        "privacy": "private",
        "external_upload": True,
        "public_schedule_set": False,
        "public_immediate_publish": False,
    }
    write_json(IN_PROGRESS, progress)

    thumb_status = set_thumbnail(token, video_id, thumb)
    write_json(THUMB_RESULT, thumb_status)
    print("OK thumbnail set")

    caption_result = None
    caption_error = None
    try:
        caption_result = upload_caption(token, video_id)
        write_json(CAPTION_RESULT, caption_result)
        print("OK sidecar captions uploaded")
    except Exception as exc:
        caption_error = str(exc)
        write_json(CAPTION_RESULT, {"error": caption_error, "burned_in_captions": True, "created_at": datetime.now(timezone.utc).isoformat()})
        print(f"WARN sidecar captions upload failed; burned-in captions remain: {caption_error}")

    state = get_video_state(token, video_id)
    write_json(STATUS_VERIFY, state)
    items = state.get("items") or []
    status = (items[0].get("status") if items else {}) or {}
    privacy = status.get("privacyStatus")
    publish_at = status.get("publishAt")
    if privacy != "private" or publish_at:
        raise RuntimeError(f"Private upload verification failed: privacy={privacy!r}, publishAt={publish_at!r}")

    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "approval_ref": APR_ID,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": "private",
        "publish_at_platform": publish_at,
        "video_file": str(video).replace("\\", "/"),
        "video_sha256": sha(video),
        "thumbnail_file": rel(thumb),
        "thumbnail_sha256": sha(thumb),
        "thumbnail_set": True,
        "thumbnail_status": thumb_status,
        "caption_file": rel(CAPTIONS),
        "captions_uploaded": caption_result is not None,
        "caption_error": caption_error,
        "youtube_state_after": state,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_schedule_set": False,
        "public_immediate_publish": False,
    }
    write_json(RESULT, result)
    update_records(result, thumb_status, caption_result, caption_error, state)
    try:
        IN_PROGRESS.unlink()
    except FileNotFoundError:
        pass

    print(f"RESULT {rel(RESULT)}")
    print(f"WATCH https://youtu.be/{video_id}")
    print(f"STUDIO https://studio.youtube.com/video/{video_id}/edit")
    print("PUBLIC_SCHEDULE_SET false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
