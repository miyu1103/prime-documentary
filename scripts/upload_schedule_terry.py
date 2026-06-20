#!/usr/bin/env python3
"""Upload EP6 Terry to YouTube and schedule public release.

Side effects in non-dry-run mode:
- refreshes the local YouTube OAuth token
- uploads the exact final MP4 as a private video
- sets the selected thumbnail
- schedules public release for 2026-06-22T12:00:00+09:00
- writes local result, package state, manifest, and event files

Idempotency strategy:
- blocks if any schedule result already exists before any external write
- update-existing mode updates the recorded YouTube video instead of uploading a duplicate
- records video_id, URL, hashes, schedule time and platform state immediately
- if a timeout happens after upload but before result write, manually inspect
  YouTube Studio before retrying to avoid duplicate uploads
"""
from __future__ import annotations

import argparse
import json
import re
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

EP = "PD-2026-006-terry"
EPDIR = ROOT / "episodes" / EP
META = EPDIR / "09_package" / "youtube_meta.v001.json"
APR_ID = "APR-0005"
APR = EPDIR / "approvals" / f"{APR_ID}.json"
RIGHTS = EPDIR / "09_package" / "rights_manifest.v001.json"
FINAL_QC = EPDIR / "08_edit" / "renders" / "final.v001.qc.json"
VIDEO = Path(r"H:\pd-media\episodes\PD-2026-006-terry\08_edit\terry_final_v001.mp4")
THUMB = EPDIR / "10_thumbnail" / "thumbnail_option_08.v001.png"
MANIFEST = EPDIR / "manifest.json"
RESULT = EPDIR / "09_package" / "youtube_schedule_result.v002.json"
UPDATE_RESULT = EPDIR / "09_package" / "youtube_schedule_update.v002.json"
EVENTS = EPDIR / "events" / "events.jsonl"

EXPECTED_VIDEO = "938897c59113adb46d501b81c379ab692dc918fd8c931a9f4743cb9a8d30343e"
EXPECTED_THUMB = "2410160486162ad7e2b0f25c8e6f92dbcba19177a1618622e9fb28f366a4acc0"
SCHEDULED_AT_LOCAL = "2026-06-22T12:00:00+09:00"
SCHEDULED_AT_UTC = "2026-06-22T03:00:00Z"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def update_artifact_checksum(manifest: dict, artifact_id: str, path: Path, artifact_type: str | None = None) -> None:
    checksum = f"sha256:{sha256_file(path)}"
    revision_match = re.search(r"\.v([0-9]{3})\.", path.name)
    revision = f"v{revision_match.group(1)}" if revision_match else "v001"
    uri = f"artifact://{path.relative_to(ROOT).as_posix()}"
    for artifact in manifest.get("artifacts", []):
        if artifact.get("artifact_id") == artifact_id:
            artifact["checksum"] = checksum
            artifact["revision"] = revision
            artifact["uri"] = uri
            if artifact_type:
                artifact["artifact_type"] = artifact_type
            return
    manifest.setdefault("artifacts", []).append({
        "artifact_id": artifact_id,
        "artifact_type": artifact_type or "artifact",
        "revision": revision,
        "uri": uri,
        "checksum": checksum,
        "status": "approved",
        "rights_status": "clear",
        "qc_status": "pass",
    })


def update_local_package_state(result: dict, result_path: Path = RESULT) -> None:
    meta = load_json(META)
    meta["status"] = "scheduled"
    meta["upload_performed"] = True
    meta["publish_performed"] = False
    meta["video_id"] = result["video_id"]
    meta["video_url"] = result["watch"]
    meta["studio_url"] = result["studio"]
    meta["scheduled_at_local"] = SCHEDULED_AT_LOCAL
    meta["scheduled_at_utc"] = SCHEDULED_AT_UTC
    meta["schedule_result"] = str(result_path.relative_to(ROOT)).replace("\\", "/")
    meta["approval_ids"] = sorted(set(meta.get("approval_ids", []) + [APR_ID]))
    meta.setdefault("pre_publish_checks", {})["upload_performed"] = True
    meta.setdefault("pre_publish_checks", {})["publish_performed"] = False
    meta.setdefault("pre_publish_checks", {})["scheduled_at_local"] = SCHEDULED_AT_LOCAL
    meta.setdefault("pre_publish_checks", {})["schedule_result"] = str(result_path.relative_to(ROOT)).replace("\\", "/")
    write_json(META, meta)

    manifest = load_json(MANIFEST)
    manifest["state"] = "scheduled"
    manifest["video_id"] = result["video_id"]
    manifest["video_url"] = result["watch"]
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    approvals = manifest.setdefault("approvals", [])
    if APR_ID not in approvals:
        approvals.append(APR_ID)
    warning = f"YouTube upload completed as private and scheduled for {SCHEDULED_AT_LOCAL}; public immediate publish not performed."
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    update_artifact_checksum(manifest, f"{EP}-youtube-meta", META, "youtube_metadata")
    update_artifact_checksum(manifest, f"{EP}-approval-{APR_ID}", APR, "approval")
    update_artifact_checksum(manifest, f"{EP}-youtube-schedule-result", result_path, "youtube_schedule_result")
    write_json(MANIFEST, manifest)


def description_with_chapters(meta: dict) -> str:
    desc = meta["description"].rstrip()
    chapters = meta.get("chapters") or []
    if not chapters:
        return desc
    lines = ["", "", "Chapters:"]
    for chapter in chapters:
        lines.append(f"{chapter['time']} {chapter['title']}")
    return desc + "\n".join(lines)


def initiate_upload(token: str, meta: dict, file_size: int) -> str:
    snippet = {
        "title": meta["title"],
        "description": description_with_chapters(meta),
        "tags": meta.get("tags", []),
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
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


def set_thumbnail(token: str, video_id: str, path: Path) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=path.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"},
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


def update_schedule(token: str, video_id: str, existing_state: dict) -> dict:
    items = existing_state.get("items") or []
    existing_status = (items[0].get("status") if items else {}) or {}
    status = {
        "privacyStatus": "private",
        "publishAt": SCHEDULED_AT_UTC,
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": True,
        "license": existing_status.get("license", "youtube"),
        "embeddable": existing_status.get("embeddable", True),
        "publicStatsViewable": existing_status.get("publicStatsViewable", True),
    }
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        data=json.dumps({"id": video_id, "status": status}).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"},
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def update_snippet(token: str, video_id: str, existing_state: dict, meta: dict) -> dict:
    items = existing_state.get("items") or []
    existing_snippet = (items[0].get("snippet") if items else {}) or {}
    snippet = {
        "title": meta["title"],
        "description": description_with_chapters(meta),
        "tags": meta.get("tags", []),
        "categoryId": existing_snippet.get("categoryId", "27"),
        "defaultLanguage": existing_snippet.get("defaultLanguage", "en"),
        "defaultAudioLanguage": existing_snippet.get("defaultAudioLanguage", "en"),
    }
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=snippet",
        data=json.dumps({"id": video_id, "snippet": snippet}).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"},
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def verify_preconditions(allow_existing_result: bool = False) -> tuple[dict, dict]:
    existing_results = sorted((EPDIR / "09_package").glob("youtube_schedule_result*.json"))
    if existing_results and not allow_existing_result:
        joined = ", ".join(str(path.relative_to(ROOT)) for path in existing_results)
        raise RuntimeError(f"Existing schedule result found; refusing duplicate upload: {joined}")
    if not APR.exists():
        raise RuntimeError(f"{APR_ID} missing")
    apr = load_json(APR)
    if apr.get("decision") != "approved":
        raise RuntimeError(f"{APR_ID} is not approved: {apr.get('decision')!r}")
    if not META.exists() or not RIGHTS.exists() or not FINAL_QC.exists():
        raise RuntimeError("Missing metadata, rights manifest, or final QC")
    if not VIDEO.exists():
        raise RuntimeError(f"Missing final video: {VIDEO}")
    if not THUMB.exists():
        raise RuntimeError(f"Missing selected thumbnail: {THUMB}")
    actual_video = sha256_file(VIDEO)
    actual_thumb = sha256_file(THUMB)
    if actual_video != EXPECTED_VIDEO:
        raise RuntimeError(f"Video hash mismatch: expected {EXPECTED_VIDEO}, actual {actual_video}")
    if actual_thumb != EXPECTED_THUMB:
        raise RuntimeError(f"Thumbnail hash mismatch: expected {EXPECTED_THUMB}, actual {actual_thumb}")
    meta = load_json(META)
    if meta.get("selected_thumbnail_sha256") != f"sha256:{EXPECTED_THUMB}":
        raise RuntimeError("youtube_meta selected thumbnail hash does not match option 08")
    if not allow_existing_result and (meta.get("publish_performed") is not False or meta.get("upload_performed") is not False):
        raise RuntimeError("youtube_meta already marks upload/publish performed")
    if allow_existing_result and meta.get("publish_performed") is not False:
        raise RuntimeError("youtube_meta already marks public publish performed")
    return apr, meta


def load_existing_video_id() -> str:
    existing_results = sorted((EPDIR / "09_package").glob("youtube_schedule_result*.json"))
    if not existing_results:
        raise RuntimeError("No existing schedule result found for update-existing mode")
    result = load_json(existing_results[-1])
    video_id = result.get("video_id")
    if not video_id:
        raise RuntimeError(f"Existing result has no video_id: {existing_results[-1]}")
    return video_id


def run_update_existing(meta: dict, dry_run: bool) -> int:
    video_id = load_existing_video_id()
    print(f"OK existing YouTube video found: {video_id}")
    print(f"OK update target local={SCHEDULED_AT_LOCAL} utc={SCHEDULED_AT_UTC}")
    print(f"OK updated title: {meta['title']}")
    print("OK update will keep privacy private, madeForKids=false, containsSyntheticMedia=true")
    if dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    env = load_env()
    token = _access_token(env)
    print("OK access token obtained")
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel allowlisted: {channel_id}")

    state_before = get_video_state(token, video_id)
    snippet_update = update_snippet(token, video_id, state_before, meta)
    print("OK snippet updated")
    schedule_update = update_schedule(token, video_id, state_before)
    print("OK schedule updated")
    thumb_status = set_thumbnail(token, video_id, THUMB)
    print("OK thumbnail re-set")
    state_after = get_video_state(token, video_id)
    items = state_after.get("items") or []
    status_after = (items[0].get("status") if items else {}) or {}
    publish_at = status_after.get("publishAt")
    privacy = status_after.get("privacyStatus")
    if publish_at != SCHEDULED_AT_UTC or privacy != "private":
        raise RuntimeError(f"Schedule verification failed: privacy={privacy!r}, publishAt={publish_at!r}")

    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "approval_ref": APR_ID,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": privacy,
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "publish_at_platform": publish_at,
        "metadata_updated": True,
        "thumbnail_set": True,
        "thumbnail_status": thumb_status,
        "youtube_meta": str(META),
        "youtube_state_before": state_before,
        "youtube_state_after": state_after,
        "snippet_update_response": snippet_update,
        "schedule_update_response": schedule_update,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": False,
        "external_update": True,
        "public_schedule_set": True,
    }
    write_json(UPDATE_RESULT, result)
    update_local_package_state(result, UPDATE_RESULT)
    append_event({
        "event": "youtube_schedule_updated",
        "episode_id": EP,
        "stage": "scheduled",
        "revision": "v001",
        "actor": "codex",
        "approval_id": APR_ID,
        "detail": f"Updated existing EP6 Terry YouTube video_id={video_id}: metadata refreshed and public release rescheduled for {SCHEDULED_AT_LOCAL}. No duplicate upload performed.",
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "thumbnail_set": True,
        "ts": datetime.now(timezone.utc).isoformat(),
    })
    print(f"RESULT {UPDATE_RESULT.relative_to(ROOT)}")
    print(f"WATCH https://youtu.be/{video_id}")
    print(f"STUDIO https://studio.youtube.com/video/{video_id}/edit")
    print(f"SCHEDULED {SCHEDULED_AT_LOCAL}")
    return 0


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--update-existing", action="store_true", help="Update the existing recorded YouTube video instead of uploading a duplicate.")
    args = parser.parse_args(argv)

    apr, meta = verify_preconditions(allow_existing_result=args.update_existing)
    print(f"OK {APR_ID} approved")
    print(f"OK schedule target local={SCHEDULED_AT_LOCAL} utc={SCHEDULED_AT_UTC}")
    print(f"OK exact video hash {EXPECTED_VIDEO}")
    print(f"OK exact thumbnail hash {EXPECTED_THUMB}")
    print(f"OK title: {meta['title']}")
    print("OK upload will be private first, madeForKids=false, containsSyntheticMedia=true")

    if args.update_existing:
        return run_update_existing(meta, args.dry_run)

    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    env = load_env()
    token = _access_token(env)
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

    thumb_status = None
    thumb_error = None
    try:
        thumb_status = set_thumbnail(token, video_id, THUMB)
        print("OK thumbnail set")
    except Exception as exc:
        thumb_error = str(exc)
        print(f"WARN thumbnail set failed; set manually in Studio: {thumb_error}")

    state_before = get_video_state(token, video_id)
    schedule_update = update_schedule(token, video_id, state_before)
    state_after = get_video_state(token, video_id)
    items = state_after.get("items") or []
    status_after = (items[0].get("status") if items else {}) or {}
    publish_at = status_after.get("publishAt")
    privacy = status_after.get("privacyStatus")
    if publish_at != SCHEDULED_AT_UTC or privacy != "private":
        raise RuntimeError(f"Schedule verification failed: privacy={privacy!r}, publishAt={publish_at!r}")

    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "approval_ref": APR_ID,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": privacy,
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "publish_at_platform": publish_at,
        "video_file": str(VIDEO),
        "video_sha256": EXPECTED_VIDEO,
        "thumbnail_file": str(THUMB),
        "thumbnail_sha256": EXPECTED_THUMB,
        "thumbnail_set": thumb_status is not None,
        "thumbnail_status": thumb_status,
        "thumbnail_error": thumb_error,
        "youtube_meta": str(META),
        "youtube_state_after": state_after,
        "schedule_update_response": schedule_update,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_schedule_set": True,
    }
    write_json(RESULT, result)
    update_local_package_state(result)
    append_event({
        "event": "youtube_upload_scheduled",
        "episode_id": EP,
        "stage": "scheduled",
        "revision": "v001",
        "actor": "codex",
        "approval_id": APR_ID,
        "detail": f"Uploaded EP6 Terry to YouTube as private video_id={video_id} and scheduled public release for {SCHEDULED_AT_LOCAL}. Thumbnail option 08 selected. No public immediate publish performed.",
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "thumbnail_set": thumb_status is not None,
        "ts": datetime.now(timezone.utc).isoformat(),
    })
    print(f"RESULT {RESULT.relative_to(ROOT)}")
    print(f"WATCH https://youtu.be/{video_id}")
    print(f"STUDIO https://studio.youtube.com/video/{video_id}/edit")
    print(f"SCHEDULED {SCHEDULED_AT_LOCAL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
