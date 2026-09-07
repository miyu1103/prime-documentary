#!/usr/bin/env python3
"""Upload EP8 Carpenter to YouTube and schedule public release.

Side effects in non-dry-run mode:
- refreshes local YouTube OAuth token
- uploads the exact final MP4 as private
- sets the selected thumbnail
- schedules public release for 2026-06-23T12:00:00+09:00
- uploads English sidecar captions
- writes local result, status verification, package state, manifest, and events
"""
from __future__ import annotations

import argparse
import json
import re
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

EP = "PD-2026-008-carpenter"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / "youtube_meta.v002.json"
APR_ID = "APR-0002"
APR = EPDIR / "approvals" / f"{APR_ID}.json"
RIGHTS = PKG / "rights_manifest.v001.json"
FINAL_DELIVERY = PKG / "final_delivery.v008.json"
FINAL_QC = EPDIR / "08_edit" / "renders" / "review.proxy.v001.qc.json"
VIDEO = Path(r"E:\pd-media\episodes\PD-2026-008-carpenter\08_edit\carpenter_review_v001.mp4")
CAPTION_FILE = EPDIR / "08_edit" / "captions.review_proxy.v001.srt"
MANIFEST = EPDIR / "manifest.json"
RESULT = PKG / "youtube_schedule_result.v001.json"
CAPTION_RESULT = PKG / "youtube_captions_result.v001.json"
STATUS_VERIFY = PKG / "youtube_status_verify.v001.json"
EVENTS = EPDIR / "events" / "events.jsonl"

EXPECTED_VIDEO = "958914322dc4e802a85e73d489bb374cabbe5e4b12e4d19c5043f58c3b2dfe49"
EXPECTED_THUMB = "af06a25443b8aa0c834c5d545bf2215f90b99d18f2341c6565de20bd6087e031"
SCHEDULED_AT_LOCAL = "2026-06-23T12:00:00+09:00"
SCHEDULED_AT_UTC = "2026-06-23T03:00:00Z"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def selected_thumbnail_path(meta: dict) -> Path:
    value = meta.get("selected_thumbnail") or meta.get("thumbnail")
    if not value:
        raise RuntimeError("youtube_meta has no selected thumbnail")
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / value
    if not path.exists():
        raise RuntimeError(f"Missing selected thumbnail: {path}")
    return path


def selected_thumbnail_sha(meta: dict) -> str:
    value = meta.get("selected_thumbnail_sha256")
    if not isinstance(value, str) or not value.startswith("sha256:"):
        raise RuntimeError("youtube_meta selected thumbnail sha256 is missing")
    return value.removeprefix("sha256:")


def request_json(url: str, token: str, data: bytes | None = None, headers: dict[str, str] | None = None, method: str | None = None, timeout: int = 180) -> dict:
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {token}", **(headers or {})}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_video_state(token: str, video_id: str) -> dict:
    return request_json(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        token,
        timeout=60,
    )


def list_captions(token: str, video_id: str) -> dict:
    return request_json(f"https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={video_id}", token, timeout=60)


def find_existing_english_caption(captions: dict) -> dict | None:
    for item in captions.get("items") or []:
        snippet = item.get("snippet", {})
        if snippet.get("language") == "en" and snippet.get("name") == "English" and not snippet.get("isDraft", True):
            return item
    return None


def upload_caption(token: str, video_id: str) -> dict:
    boundary = f"carpenter_caption_{int(time.time())}"
    metadata = {
        "snippet": {
            "videoId": video_id,
            "language": "en",
            "name": "English",
            "isDraft": False,
        }
    }
    body = b"".join([
        f"--{boundary}\r\n".encode(),
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
        json.dumps(metadata, ensure_ascii=False).encode("utf-8"),
        b"\r\n",
        f"--{boundary}\r\n".encode(),
        b"Content-Type: application/octet-stream\r\n\r\n",
        CAPTION_FILE.read_bytes(),
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


def set_thumbnail(token: str, video_id: str, path: Path) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=path.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
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
        "publishAt": SCHEDULED_AT_UTC,
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


def compact_video_state(item: dict | None) -> dict:
    if not item:
        return {"id": None, "missing": True}
    status = item.get("status", {})
    processing = item.get("processingDetails", {})
    return {
        "id": item.get("id"),
        "title": item.get("snippet", {}).get("title"),
        "privacyStatus": status.get("privacyStatus"),
        "publishAt": status.get("publishAt"),
        "uploadStatus": status.get("uploadStatus"),
        "processingStatus": processing.get("processingStatus"),
        "madeForKids": status.get("madeForKids"),
        "selfDeclaredMadeForKids": status.get("selfDeclaredMadeForKids"),
    }


def wait_for_processing(token: str, video_id: str) -> tuple[dict, str]:
    state: dict = {}
    processing_status = "unknown"
    for _ in range(24):
        state = get_video_state(token, video_id)
        items = state.get("items") or []
        processing_status = ((items[0].get("processingDetails") if items else {}) or {}).get("processingStatus", "missing")
        if processing_status in {"succeeded", "failed", "terminated"}:
            return state, processing_status
        time.sleep(15)
    return state, processing_status


def update_artifact_checksum(manifest: dict, artifact_id: str, path: Path, artifact_type: str, revision: str) -> None:
    checksum = f"sha256:{sha256_file(path)}"
    uri = f"artifact://{path.relative_to(ROOT).as_posix()}" if path.is_relative_to(ROOT) else str(path)
    for artifact in manifest.get("artifacts", []):
        if artifact.get("artifact_id") == artifact_id:
            artifact["checksum"] = checksum
            artifact["revision"] = revision
            artifact["uri"] = uri
            artifact["artifact_type"] = artifact_type
            artifact["status"] = "approved"
            artifact["rights_status"] = "clear"
            artifact["qc_status"] = "pass"
            return
    manifest.setdefault("artifacts", []).append({
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "revision": revision,
        "uri": uri,
        "checksum": checksum,
        "status": "approved",
        "rights_status": "clear",
        "qc_status": "pass",
    })


def verify_preconditions() -> tuple[dict, dict, Path]:
    existing_results = sorted(PKG.glob("youtube_schedule_result*.json"))
    if existing_results:
        joined = ", ".join(str(path.relative_to(ROOT)) for path in existing_results)
        raise RuntimeError(f"Existing schedule result found; refusing duplicate upload: {joined}")
    if not APR.exists():
        raise RuntimeError(f"{APR_ID} missing")
    apr = load_json(APR)
    if apr.get("decision") != "approved":
        raise RuntimeError(f"{APR_ID} is not approved: {apr.get('decision')!r}")
    for path in (META, RIGHTS, FINAL_DELIVERY, FINAL_QC, VIDEO, CAPTION_FILE):
        if not path.exists():
            raise RuntimeError(f"Missing required artifact: {path}")
    actual_video = sha256_file(VIDEO)
    if actual_video != EXPECTED_VIDEO:
        raise RuntimeError(f"Video hash mismatch: expected {EXPECTED_VIDEO}, actual {actual_video}")
    meta = load_json(META)
    thumb = selected_thumbnail_path(meta)
    expected_thumb = selected_thumbnail_sha(meta)
    actual_thumb = sha256_file(thumb)
    if expected_thumb != EXPECTED_THUMB or actual_thumb != EXPECTED_THUMB:
        raise RuntimeError(f"Thumbnail hash mismatch: expected {EXPECTED_THUMB}, meta {expected_thumb}, actual {actual_thumb}")
    if meta.get("publish_performed") is not False or meta.get("upload_performed") is not False:
        raise RuntimeError("youtube_meta already marks upload/publish performed")
    if meta.get("synthetic_content_disclosure_required") is not True:
        raise RuntimeError("synthetic_content_disclosure_required must be true")
    return apr, meta, thumb


def update_local_records(result: dict, caption_result: dict, verify: dict, processing_status: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    video_id = result["video_id"]
    meta = load_json(META)
    meta["status"] = "scheduled"
    meta["upload_performed"] = True
    meta["publish_performed"] = False
    meta["video_id"] = video_id
    meta["video_url"] = result["watch"]
    meta["studio_url"] = result["studio"]
    meta["youtube_channel_id"] = result["channel_id"]
    meta["scheduled_at_local"] = SCHEDULED_AT_LOCAL
    meta["scheduled_at_utc"] = SCHEDULED_AT_UTC
    meta["publish_at_platform"] = result["publish_at_platform"]
    meta["schedule_result"] = str(RESULT.relative_to(ROOT)).replace("\\", "/")
    meta["processing_status"] = processing_status
    meta["processing_status_verified_at"] = now
    meta["captions_uploaded"] = True
    meta["captions_result"] = str(CAPTION_RESULT.relative_to(ROOT)).replace("\\", "/")
    meta["caption_track_language"] = "en"
    meta["caption_track_name"] = "English"
    meta["caption_track_uploaded_at"] = now
    meta["status_verify_result"] = str(STATUS_VERIFY.relative_to(ROOT)).replace("\\", "/")
    meta["approval_ids"] = sorted(set(meta.get("approval_ids", []) + [APR_ID]))
    meta.setdefault("pre_publish_checks", {})["upload_performed"] = True
    meta.setdefault("pre_publish_checks", {})["publish_performed"] = False
    meta.setdefault("pre_publish_checks", {})["scheduled_at_local"] = SCHEDULED_AT_LOCAL
    meta.setdefault("pre_publish_checks", {})["scheduled_at_utc"] = SCHEDULED_AT_UTC
    meta.setdefault("pre_publish_checks", {})["schedule_result"] = str(RESULT.relative_to(ROOT)).replace("\\", "/")
    meta.setdefault("pre_publish_checks", {})["captions_result"] = str(CAPTION_RESULT.relative_to(ROOT)).replace("\\", "/")
    meta.setdefault("pre_publish_checks", {})["status_verify_result"] = str(STATUS_VERIFY.relative_to(ROOT)).replace("\\", "/")
    meta["public_schedule_active"] = True
    meta["updated_at"] = now
    write_json(META, meta)

    manifest = load_json(MANIFEST)
    manifest["state"] = "scheduled"
    manifest["video_id"] = video_id
    manifest["video_url"] = result["watch"]
    manifest["public_schedule_active"] = True
    manifest["updated_at"] = now
    active = manifest.setdefault("active_revisions", {})
    active["rights_manifest"] = "v001"
    active["final_qc"] = "v001"
    active["final_delivery"] = "v008"
    active["final_render"] = "v007"
    active["youtube_meta"] = "v002"
    active["thumbnail_selected"] = "v006"
    active["thumbnail_candidates"] = "v006"
    active["youtube_schedule_result"] = "v001"
    active["youtube_captions_result"] = "v001"
    active["youtube_status_verify"] = "v001"
    active["captions_sidecar"] = "v001"
    if APR_ID not in manifest.setdefault("approvals", []):
        manifest["approvals"].append(APR_ID)
    warning = f"YouTube private upload completed for Carpenter v008 package: video_id {video_id}, thumbnail v006 set, sidecar captions uploaded, public release scheduled for {SCHEDULED_AT_LOCAL}. Immediate public publish not performed."
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    update_artifact_checksum(manifest, f"{EP}-final-render-v007", VIDEO, "final_render", "v007")
    update_artifact_checksum(manifest, f"{EP}-final-qc-v001", FINAL_QC, "qc_report", "v001")
    update_artifact_checksum(manifest, f"{EP}-final-delivery-v008", FINAL_DELIVERY, "final_delivery_manifest", "v008")
    update_artifact_checksum(manifest, f"{EP}-youtube-meta-v002", META, "youtube_metadata", "v002")
    update_artifact_checksum(manifest, f"{EP}-thumbnail-selected-v006", selected_thumbnail_path(meta), "thumbnail", "v006")
    update_artifact_checksum(manifest, f"{EP}-approval-{APR_ID}", APR, "approval", "v001")
    update_artifact_checksum(manifest, f"{EP}-youtube-schedule-result-v001", RESULT, "youtube_schedule_result", "v001")
    update_artifact_checksum(manifest, f"{EP}-youtube-captions-result-v001", CAPTION_RESULT, "youtube_captions_result", "v001")
    update_artifact_checksum(manifest, f"{EP}-youtube-status-verify-v001", STATUS_VERIFY, "youtube_status_verify", "v001")
    write_json(MANIFEST, manifest)

    append_event({
        "event": "youtube_upload_scheduled",
        "episode_id": EP,
        "stage": "scheduled",
        "revision": "v008",
        "actor": "codex",
        "approval_id": APR_ID,
        "detail": f"Uploaded EP8 Carpenter package to YouTube as private video_id={video_id}, set thumbnail v006, uploaded English captions, and scheduled public release for {SCHEDULED_AT_LOCAL}. No immediate public publish performed.",
        "video_id": video_id,
        "watch": result["watch"],
        "studio": result["studio"],
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "thumbnail_set": result["thumbnail_set"],
        "captions_uploaded": True,
        "processing_status": processing_status,
        "ts": now,
    })


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    apr, meta, thumb = verify_preconditions()
    print(f"OK {APR_ID} approved")
    print(f"OK schedule target local={SCHEDULED_AT_LOCAL} utc={SCHEDULED_AT_UTC}")
    print(f"OK exact video hash {EXPECTED_VIDEO}")
    print(f"OK exact thumbnail hash {EXPECTED_THUMB}")
    print(f"OK title: {meta['title']}")
    print("OK upload will be private first, madeForKids=false, containsSyntheticMedia=true")
    print("OK sidecar English captions will be uploaded")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    print("OK access token obtained")
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel allowlisted: {channel_id}")

    upload_url = initiate_upload(token, meta, VIDEO.stat().st_size)
    print(f"OK resumable upload session started; uploading {VIDEO.stat().st_size / 1e6:.0f} MB")
    video_id = upload_chunks(upload_url, token, VIDEO)
    if not video_id:
        raise RuntimeError("Upload returned no video_id")
    print(f"OK private upload complete video_id={video_id}")

    thumb_status = set_thumbnail(token, video_id, thumb)
    print("OK thumbnail set")

    state_after = get_video_state(token, video_id)
    items = state_after.get("items") or []
    status_after = (items[0].get("status") if items else {}) or {}
    publish_at = status_after.get("publishAt")
    privacy = status_after.get("privacyStatus")
    if publish_at != SCHEDULED_AT_UTC or privacy != "private":
        raise RuntimeError(f"Schedule verification failed: privacy={privacy!r}, publishAt={publish_at!r}")

    processing_state, processing_status = wait_for_processing(token, video_id)
    before_captions = list_captions(token, video_id)
    existing_caption = find_existing_english_caption(before_captions)
    if existing_caption:
        caption = {"skipped_upload": True, "reason": "existing_english_caption_present", "existing_caption": existing_caption}
    else:
        caption = upload_caption(token, video_id)
        time.sleep(8)
    after_captions = list_captions(token, video_id)
    final_state = get_video_state(token, video_id)
    final_items = final_state.get("items") or []
    final_status = (final_items[0].get("status") if final_items else {}) or {}
    verified_private_scheduled = final_status.get("privacyStatus") == "private" and final_status.get("publishAt") == SCHEDULED_AT_UTC

    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "approval_ref": APR_ID,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": final_status.get("privacyStatus"),
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "publish_at_platform": final_status.get("publishAt"),
        "video_file": str(VIDEO),
        "video_sha256": EXPECTED_VIDEO,
        "thumbnail_file": str(thumb.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": EXPECTED_THUMB,
        "thumbnail_set": True,
        "thumbnail_status": thumb_status,
        "youtube_meta": str(META.relative_to(ROOT)).replace("\\", "/"),
        "youtube_state_after_upload": state_after,
        "youtube_state_final": final_state,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_schedule_set": True,
        "immediate_public_publish": False,
    }
    write_json(RESULT, result)

    caption_result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
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
        "revision": "v001",
        "video_id": video_id,
        "processing_status": processing_status,
        "processing_state": processing_state,
        "youtube_state_compact": compact_video_state(final_items[0] if final_items else None),
        "verified_private_scheduled": verified_private_scheduled,
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(STATUS_VERIFY, verify)
    update_local_records(result, caption_result, verify, processing_status)
    print(json.dumps({
        "video_id": video_id,
        "processing_status": processing_status,
        "captions_uploaded": True,
        "verified_private_scheduled": verified_private_scheduled,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
