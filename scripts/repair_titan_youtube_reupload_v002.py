#!/usr/bin/env python3
"""Repair a stuck Titan YouTube processing job by uploading the faststart copy.

This does not delete the old upload. It creates a replacement private upload,
sets thumbnail/captions, schedules it for the approved release time, waits for
YouTube to recognize the duration, then removes publishAt from the stuck upload
to avoid duplicate publication.
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
APR_ID = "APR-0004"
OLD_VIDEO_ID = "BzUUoEtSY-M"
SCHEDULED_AT_LOCAL = "2026-07-01T12:00:00+09:00"
SCHEDULED_AT_UTC = "2026-07-01T03:00:00Z"

EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / f"youtube_meta.{REV}.json"
FINAL_DELIVERY = PKG / f"final_delivery.{REV}.json"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
CAPTIONS = EPDIR / "08_edit" / "captions.v008.srt"
FALLBACK_VIDEO = Path("H:/pd-media/episodes/PD-2026-016-titan/07_edit/v008_youtube_faststart_fallback.mp4")

RESULT = PKG / "youtube_reupload_repair_result.v002.json"
STATUS_VERIFY = PKG / "youtube_reupload_repair_status_verify.v002.json"
OLD_UNSCHEDULE_RESULT = PKG / "youtube_old_stuck_upload_unscheduled.v002.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def sha(path: Path) -> str:
    return "sha256:" + sha256_file(path)


def request_json(req: urllib.request.Request, timeout: int = 60) -> dict:
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body) if body else {}


def get_video_state(token: str, video_id: str) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails,contentDetails,fileDetails&id={video_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return request_json(req)


def status_summary(state: dict) -> dict:
    item = (state.get("items") or [{}])[0]
    status = item.get("status") or {}
    processing = item.get("processingDetails") or {}
    content = item.get("contentDetails") or {}
    file_details = item.get("fileDetails") or {}
    return {
        "video_id": item.get("id"),
        "privacyStatus": status.get("privacyStatus"),
        "publishAt": status.get("publishAt"),
        "uploadStatus": status.get("uploadStatus"),
        "processingStatus": processing.get("processingStatus"),
        "processingFailureReason": processing.get("processingFailureReason"),
        "processingErrors": processing.get("processingErrors"),
        "processingWarnings": processing.get("processingWarnings"),
        "processingProgress": processing.get("processingProgress"),
        "duration": content.get("duration"),
        "definition": content.get("definition"),
        "caption": content.get("caption"),
        "durationMs_fileDetails": file_details.get("durationMs"),
    }


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


def set_thumbnail(token: str, video_id: str, path: Path) -> dict:
    content_type = mimetypes.guess_type(path.name)[0] or "image/png"
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=path.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": content_type},
        method="POST",
    )
    return request_json(req)


def upload_caption(token: str, video_id: str) -> dict:
    boundary = f"titan_repair_caption_{int(time.time())}"
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
    )
    body = (
        f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{metadata}"
        f"\r\n--{boundary}\r\nContent-Type: application/x-subrip\r\n\r\n"
    ).encode("utf-8") + CAPTIONS.read_bytes() + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/related; boundary={boundary}"},
        method="POST",
    )
    return request_json(req)


def update_schedule(token: str, video_id: str, state_before: dict) -> dict:
    existing_status = ((state_before.get("items") or [{}])[0].get("status") or {}).copy()
    status = {
        "privacyStatus": "private",
        "publishAt": SCHEDULED_AT_UTC,
        "selfDeclaredMadeForKids": False,
        "madeForKids": False,
        "license": existing_status.get("license", "youtube"),
        "embeddable": existing_status.get("embeddable", True),
        "publicStatsViewable": existing_status.get("publicStatsViewable", True),
        "containsSyntheticMedia": True,
    }
    body = json.dumps({"id": video_id, "status": status}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"},
        method="PUT",
    )
    return request_json(req)


def unschedule_old(token: str, video_id: str, state_before: dict) -> dict:
    existing_status = ((state_before.get("items") or [{}])[0].get("status") or {}).copy()
    status = {
        "privacyStatus": "private",
        "selfDeclaredMadeForKids": bool(existing_status.get("selfDeclaredMadeForKids", False)),
        "madeForKids": bool(existing_status.get("madeForKids", False)),
        "license": existing_status.get("license", "youtube"),
        "embeddable": existing_status.get("embeddable", True),
        "publicStatsViewable": existing_status.get("publicStatsViewable", True),
        "containsSyntheticMedia": True,
    }
    body = json.dumps({"id": video_id, "status": status}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"},
        method="PUT",
    )
    return request_json(req)


def wait_for_duration(token: str, video_id: str, *, max_wait_seconds: int, interval_seconds: int) -> tuple[dict, list[dict]]:
    observations: list[dict] = []
    deadline = time.time() + max_wait_seconds
    while True:
        state = get_video_state(token, video_id)
        summary = status_summary(state)
        summary["observed_at"] = datetime.now(timezone.utc).isoformat()
        observations.append(summary)
        print("POLL " + json.dumps(summary, ensure_ascii=False))
        failure = summary.get("processingFailureReason") or summary.get("processingErrors")
        if failure:
            raise RuntimeError(f"YouTube processing failed: {failure}")
        duration = summary.get("duration")
        if duration and duration != "P0D":
            return state, observations
        if time.time() >= deadline:
            return state, observations
        time.sleep(interval_seconds)


def update_local_records(new_video_id: str, result: dict, final_state: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    meta = load_json(META)
    meta.update(
        {
            "status": "scheduled",
            "video_id": new_video_id,
            "video_url": f"https://youtu.be/{new_video_id}",
            "studio_url": f"https://studio.youtube.com/video/{new_video_id}/edit",
            "schedule_performed": True,
            "publish_performed": False,
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "publish_at_platform": SCHEDULED_AT_UTC,
            "repair_reupload_result": rel(RESULT),
            "repair_reupload_status_verify": rel(STATUS_VERIFY),
            "superseded_youtube_video_id": OLD_VIDEO_ID,
            "updated_at": now,
        }
    )
    meta["requested_schedule"]["status"] = "scheduled"
    write_json(META, meta)

    delivery = load_json(FINAL_DELIVERY)
    delivery.update(
        {
            "status": "scheduled",
            "video_id": new_video_id,
            "watch": f"https://youtu.be/{new_video_id}",
            "studio": f"https://studio.youtube.com/video/{new_video_id}/edit",
            "schedule_performed": True,
            "publish_performed": False,
            "youtube": {
                **delivery.get("youtube", {}),
                "video_id": new_video_id,
                "watch": f"https://youtu.be/{new_video_id}",
                "studio": f"https://studio.youtube.com/video/{new_video_id}/edit",
                "privacy": "private",
                "scheduled_at_local": SCHEDULED_AT_LOCAL,
                "scheduled_at_utc": SCHEDULED_AT_UTC,
                "schedule_performed": True,
                "public_immediate_publish": False,
                "repair_reupload_result": rel(RESULT),
                "superseded_youtube_video_id": OLD_VIDEO_ID,
            },
            "updated_at": now,
        }
    )
    delivery["requested_schedule"]["status"] = "scheduled"
    write_json(FINAL_DELIVERY, delivery)

    manifest = load_json(MANIFEST)
    manifest["state"] = "scheduled"
    manifest["video_id"] = new_video_id
    manifest["video_url"] = f"https://youtu.be/{new_video_id}"
    manifest["updated_at"] = now
    manifest["active_revisions"].update(
        {
            "youtube_reupload_repair_result": "v002",
            "youtube_reupload_repair_status_verify": "v002",
        }
    )
    manifest["blockers"] = []
    note = (
        f"Titan YouTube upload was repaired by replacing stuck video {OLD_VIDEO_ID} "
        f"with {new_video_id}; replacement scheduled for {SCHEDULED_AT_LOCAL}."
    )
    if note not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(note)
    write_json(MANIFEST, manifest)

    append_event(
        {
            "ts": now,
            "episode_id": EP,
            "stage": "youtube_reupload_repair",
            "event": "youtube_stuck_upload_replaced_and_scheduled",
            "revision": REV,
            "actor": "codex",
            "approval_id": APR_ID,
            "old_video_id": OLD_VIDEO_ID,
            "new_video_id": new_video_id,
            "watch": f"https://youtu.be/{new_video_id}",
            "studio": f"https://studio.youtube.com/video/{new_video_id}/edit",
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "note": "Replacement upload used faststart MP4 after original upload remained processing with duration=P0D. Old upload left private and unscheduled.",
        }
    )


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--wait-seconds", type=int, default=900)
    parser.add_argument("--poll-interval", type=int, default=30)
    args = parser.parse_args(argv)

    for path in (META, FINAL_DELIVERY, MANIFEST, CAPTIONS, FALLBACK_VIDEO):
        if not path.exists():
            raise RuntimeError(f"Missing required file: {path}")
    if RESULT.exists():
        raise RuntimeError(f"Repair result already exists: {rel(RESULT)}")

    meta = load_json(META)
    thumb = (ROOT / meta["thumbnail"]).resolve()
    if not thumb.exists():
        raise RuntimeError(f"Missing thumbnail: {thumb}")

    print(f"OK fallback={FALLBACK_VIDEO}")
    print(f"OK fallback_sha256={sha(FALLBACK_VIDEO)}")
    print(f"OK thumbnail={thumb}")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel allowlisted: {channel_id}")

    old_state_before = get_video_state(token, OLD_VIDEO_ID)
    print("OLD_BEFORE " + json.dumps(status_summary(old_state_before), ensure_ascii=False))

    upload_url = initiate_upload(token, meta, FALLBACK_VIDEO.stat().st_size)
    print(f"OK resumable upload started; uploading {FALLBACK_VIDEO.stat().st_size / 1e6:.0f} MB")
    new_video_id = upload_chunks(upload_url, token, FALLBACK_VIDEO)
    if not new_video_id:
        raise RuntimeError("Upload returned no video_id")
    print(f"OK replacement private upload complete video_id={new_video_id}")

    thumb_status = set_thumbnail(token, new_video_id, thumb)
    print("OK thumbnail set on replacement")
    caption_error = None
    caption_result = None
    try:
        caption_result = upload_caption(token, new_video_id)
        print("OK sidecar captions uploaded on replacement")
    except Exception as exc:
        caption_error = str(exc)
        print(f"WARN sidecar captions failed; burned-in captions remain: {caption_error}")

    replacement_before_schedule = get_video_state(token, new_video_id)
    update_response = update_schedule(token, new_video_id, replacement_before_schedule)
    print("OK replacement scheduled")

    final_state, observations = wait_for_duration(
        token,
        new_video_id,
        max_wait_seconds=args.wait_seconds,
        interval_seconds=args.poll_interval,
    )
    final_summary = status_summary(final_state)
    scheduled_ok = final_summary.get("privacyStatus") == "private" and final_summary.get("publishAt") == SCHEDULED_AT_UTC
    duration_ok = bool(final_summary.get("duration")) and final_summary.get("duration") != "P0D"
    if not scheduled_ok:
        raise RuntimeError(f"Replacement schedule verification failed: {final_summary}")
    if not duration_ok:
        raise RuntimeError(f"Replacement did not expose duration within wait window: {final_summary}")

    old_unschedule_response = unschedule_old(token, OLD_VIDEO_ID, old_state_before)
    old_state_after = get_video_state(token, OLD_VIDEO_ID)
    old_summary_after = status_summary(old_state_after)
    if old_summary_after.get("publishAt"):
        raise RuntimeError(f"Old upload still has publishAt after unschedule: {old_summary_after}")
    print("OK old stuck upload left private and unscheduled")

    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "approval_ref": APR_ID,
        "old_video_id": OLD_VIDEO_ID,
        "new_video_id": new_video_id,
        "watch": f"https://youtu.be/{new_video_id}",
        "studio": f"https://studio.youtube.com/video/{new_video_id}/edit",
        "privacy": "private",
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "publish_at_platform": final_summary.get("publishAt"),
        "fallback_video": rel(FALLBACK_VIDEO),
        "fallback_video_sha256": sha(FALLBACK_VIDEO),
        "thumbnail_file": rel(thumb),
        "thumbnail_sha256": sha(thumb),
        "thumbnail_status": thumb_status,
        "captions_uploaded": caption_result is not None,
        "caption_error": caption_error,
        "caption_result": caption_result,
        "upload_response_video_id": new_video_id,
        "schedule_update_response": update_response,
        "processing_observations": observations,
        "final_summary": final_summary,
        "old_before": status_summary(old_state_before),
        "old_unschedule_response": old_unschedule_response,
        "old_after": old_summary_after,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "public_immediate_publish": False,
    }
    write_json(RESULT, result)
    write_json(STATUS_VERIFY, final_state)
    write_json(OLD_UNSCHEDULE_RESULT, {"old_video_id": OLD_VIDEO_ID, "old_after": old_state_after, "updated_at": datetime.now(timezone.utc).isoformat()})
    update_local_records(new_video_id, result, final_state)
    print(f"REPAIRED new_video_id={new_video_id} scheduled={SCHEDULED_AT_LOCAL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
