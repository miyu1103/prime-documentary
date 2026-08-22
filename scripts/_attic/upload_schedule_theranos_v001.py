#!/usr/bin/env python3
"""Upload PD-2026-015 Theranos to YouTube and schedule public release."""
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

EP = "PD-2026-015-theranos"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
APPROVALS = EPDIR / "approvals"
META = PKG / "youtube_meta.v009.json"
FINAL_DELIVERY = PKG / "final_delivery.v009.json"
ACCEPTANCE = EPDIR / "08_edit" / "renders" / "final.v006.acceptance.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"

RESULT = PKG / "youtube_schedule_result.v001.json"
IN_PROGRESS = PKG / "youtube_upload_in_progress.v001.json"
STATUS_VERIFY = PKG / "youtube_status_verify.v001.json"
CAPTION_RESULT = PKG / "youtube_captions_result.v001.json"
THUMB_RESULT = PKG / "youtube_thumbnail_result.v001.json"

SCHEDULED_AT_LOCAL = "2026-06-30T12:00:00+09:00"
SCHEDULED_AT_UTC = "2026-06-30T03:00:00Z"

EXPECTED = {
    "video": "sha256:3c769f26b3a63b4c665b8b2fb4c68492be2e3e2c965f075cb474c3695063a4ec",
    "thumbnail": "sha256:17f4e97f0b34ce1697cf7ac089201b213df9184ae744a2cbc4c0b67d72aa2f3a",
    "captions": "sha256:fb8e241e4c54df7dea2c94a66b874e7d4836f9be0807446e0b7a225591ff03e6",
    "acceptance": "sha256:9fd0129980216de24a68855829c0bd460440a34e3e27ba9013a3d22d01adea26",
    "youtube_meta": "sha256:9f06451604144a2a054beec98fc7815ef64fa830ee8fb8b828216fc7aa07cfe2",
    "final_delivery": "sha256:994910f65df49e6629f561b2532ce68df91c96cc43ed898835c67da0f3428ad6",
    "rights_manifest": "sha256:25b7b2837bf9dfd7466620386e86ee1d23718de0d5b8aab3ecf8d1a5d218b865",
    "legal_packet": "sha256:0ad72c5ce2f84ee2c01eb8c84f4540cc1da1cdb084fa5255ec06cb204a243d56",
}


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


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def require_file(path: Path) -> None:
    if not path.exists():
        raise RuntimeError(f"Missing required artifact: {path}")


def require_hash(path: Path, expected: str, label: str) -> None:
    actual = sha(path)
    if actual != expected:
        raise RuntimeError(f"{label} hash mismatch: expected {expected}, actual {actual}")


def verify_approvals() -> None:
    required = {
        "APR-0002": ("video_sha256", EXPECTED["video"]),
        "APR-0003": ("youtube_meta_sha256", EXPECTED["youtube_meta"]),
        "APR-0004": ("final_audio_mix_sha256", "sha256:083b1500352a3eab4945428e0f6b96ab0a7b57f5a60a6c8cf1aa439b6b492be5"),
        "APR-0005": ("rights_manifest_sha256", EXPECTED["rights_manifest"]),
        "APR-0006": ("final_delivery_sha256", EXPECTED["final_delivery"]),
    }
    for apr_id, (field, expected) in required.items():
        path = APPROVALS / f"{apr_id}.json"
        require_file(path)
        data = load_json(path)
        if data.get("decision") != "approved":
            raise RuntimeError(f"{apr_id} is not approved: {data.get('decision')!r}")
        if data.get(field) != expected:
            raise RuntimeError(f"{apr_id} {field} mismatch: expected {expected}, got {data.get(field)!r}")


def upload_caption(token: str, video_id: str) -> dict:
    boundary = f"theranos_caption_{int(time.time())}"
    metadata = {
        "snippet": {
            "videoId": video_id,
            "language": "en",
            "name": "English",
            "isDraft": False,
        }
    }
    body = b"".join(
        [
            f"--{boundary}\r\n".encode(),
            b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
            json.dumps(metadata, ensure_ascii=False).encode("utf-8"),
            b"\r\n",
            f"--{boundary}\r\n".encode(),
            b"Content-Type: application/x-subrip\r\n\r\n",
            CAPTIONS.read_bytes(),
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
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
        "publishAt": SCHEDULED_AT_UTC,
        "selfDeclaredMadeForKids": False,
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
    existing = [p for p in (RESULT, IN_PROGRESS, STATUS_VERIFY) if p.exists()]
    if existing:
        joined = ", ".join(str(p.relative_to(ROOT)) for p in existing)
        raise RuntimeError(f"Existing YouTube result/in-progress file found; refusing duplicate upload: {joined}")

    for path in (META, FINAL_DELIVERY, ACCEPTANCE, CAPTIONS, MANIFEST):
        require_file(path)
    verify_approvals()

    meta = load_json(META)
    delivery = load_json(FINAL_DELIVERY)
    acceptance = load_json(ACCEPTANCE)
    video = resolve_path(meta["video_actual_path"])
    thumb = resolve_path(meta["thumbnail"])

    for path in (video, thumb):
        require_file(path)
    require_hash(video, EXPECTED["video"], "video")
    require_hash(thumb, EXPECTED["thumbnail"], "thumbnail")
    require_hash(CAPTIONS, EXPECTED["captions"], "captions")
    require_hash(ACCEPTANCE, EXPECTED["acceptance"], "acceptance")
    require_hash(META, EXPECTED["youtube_meta"], "youtube_meta")
    require_hash(FINAL_DELIVERY, EXPECTED["final_delivery"], "final_delivery")

    if acceptance.get("status") != "PASS":
        raise RuntimeError(f"Acceptance is not PASS: {acceptance.get('status')!r}")
    if delivery.get("status") != "approved_for_private_upload_and_schedule":
        raise RuntimeError(f"final_delivery status is not upload-approved: {delivery.get('status')!r}")
    if meta.get("upload_performed") is not False or meta.get("publish_performed") is not False or meta.get("schedule_performed") is not False:
        raise RuntimeError("youtube_meta already marks upload, publish, or schedule performed")
    schedule = meta.get("requested_schedule") or {}
    if schedule.get("local_time") != SCHEDULED_AT_LOCAL or schedule.get("utc_time") != SCHEDULED_AT_UTC:
        raise RuntimeError("youtube_meta schedule target does not match script target")
    if "Public upload remains blocked" in meta.get("description", ""):
        raise RuntimeError("youtube_meta description still contains internal blocked-release text")
    return meta, video, thumb


def update_artifact(manifest: dict, artifact_id: str, path: Path, artifact_type: str, revision: str, status: str = "approved") -> None:
    checksum = sha(path)
    uri = f"artifact://{path.relative_to(ROOT).as_posix()}" if path.is_relative_to(ROOT) else str(path)
    for artifact in manifest.get("artifacts", []):
        if artifact.get("artifact_id") == artifact_id:
            artifact.update({"artifact_type": artifact_type, "revision": revision, "uri": uri, "checksum": checksum, "status": status, "rights_status": "clear", "qc_status": "pass"})
            return
    manifest.setdefault("artifacts", []).append({"artifact_id": artifact_id, "artifact_type": artifact_type, "revision": revision, "uri": uri, "checksum": checksum, "status": status, "rights_status": "clear", "qc_status": "pass"})


def update_records(result: dict, caption_result: dict | None, caption_error: str | None, state: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    video_id = result["video_id"]
    meta = load_json(META)
    meta.update(
        {
            "status": "scheduled",
            "upload_performed": True,
            "publish_performed": False,
            "schedule_performed": True,
            "video_id": video_id,
            "video_url": result["watch"],
            "studio_url": result["studio"],
            "youtube_channel_id": result["channel_id"],
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "publish_at_platform": result["publish_at_platform"],
            "schedule_result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
            "status_verify": str(STATUS_VERIFY.relative_to(ROOT)).replace("\\", "/"),
            "thumbnail_uploaded": True,
            "thumbnail_result": str(THUMB_RESULT.relative_to(ROOT)).replace("\\", "/"),
            "captions_uploaded": caption_result is not None,
            "captions_result": str(CAPTION_RESULT.relative_to(ROOT)).replace("\\", "/"),
            "caption_error": caption_error,
            "processing_status_verified_at": now,
            "updated_at": now,
        }
    )
    meta["requested_schedule"]["status"] = "scheduled"
    write_json(META, meta)

    delivery = load_json(FINAL_DELIVERY)
    delivery.update(
        {
            "status": "scheduled",
            "upload_performed": True,
            "schedule_performed": True,
            "publish_performed": False,
            "public_immediate_publish": False,
            "video_id": video_id,
            "watch": result["watch"],
            "studio": result["studio"],
            "youtube": {
                "video_id": video_id,
                "watch": result["watch"],
                "studio": result["studio"],
                "privacy": "private",
                "scheduled_at_local": SCHEDULED_AT_LOCAL,
                "scheduled_at_utc": SCHEDULED_AT_UTC,
                "upload_performed": True,
                "schedule_performed": True,
                "public_immediate_publish": False,
                "result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
            },
            "updated_at": now,
        }
    )
    delivery["requested_schedule"]["status"] = "scheduled"
    write_json(FINAL_DELIVERY, delivery)

    manifest = load_json(MANIFEST)
    manifest["state"] = "scheduled"
    manifest["video_id"] = video_id
    manifest["video_url"] = result["watch"]
    manifest["public_schedule_active"] = True
    manifest["updated_at"] = now
    manifest["blockers"] = []
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "youtube_meta": "v009",
            "final_delivery": "v009",
            "youtube_schedule_result": "v001",
            "youtube_status_verify": "v001",
            "youtube_captions_result": "v001",
            "youtube_thumbnail_result": "v001",
        }
    )
    approvals = manifest.setdefault("approvals", [])
    for apr_id in ("APR-0002", "APR-0003", "APR-0004", "APR-0005", "APR-0006"):
        if apr_id not in approvals:
            approvals.append(apr_id)
    update_artifact(manifest, f"{EP}-youtube_metadata-v009", META, "youtube_metadata", "v009", status="scheduled")
    update_artifact(manifest, f"{EP}-final_delivery-v009", FINAL_DELIVERY, "final_delivery", "v009", status="scheduled")
    update_artifact(manifest, f"{EP}-youtube_schedule_result-v001", RESULT, "youtube_schedule_result", "v001", status="scheduled")
    update_artifact(manifest, f"{EP}-youtube_status_verify-v001", STATUS_VERIFY, "youtube_status_verify", "v001", status="scheduled")
    if caption_result is not None or caption_error is not None:
        update_artifact(manifest, f"{EP}-youtube_captions_result-v001", CAPTION_RESULT, "youtube_captions_result", "v001", status="scheduled")
    update_artifact(manifest, f"{EP}-youtube_thumbnail_result-v001", THUMB_RESULT, "youtube_thumbnail_result", "v001", status="scheduled")
    warning = f"YouTube private upload completed for Theranos v009 package: video_id {video_id}, thumbnail set, public release scheduled for {SCHEDULED_AT_LOCAL}. Immediate public publish not performed."
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    write_json(MANIFEST, manifest)

    append_event(
        {
            "ts": now,
            "episode_id": EP,
            "stage": "youtube_schedule",
            "event": "youtube_upload_scheduled",
            "revision": "v009",
            "actor": "codex",
            "approval_ids": ["APR-0002", "APR-0003", "APR-0004", "APR-0005", "APR-0006"],
            "video_id": video_id,
            "watch": result["watch"],
            "studio": result["studio"],
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "privacy": "private",
            "thumbnail_set": True,
            "captions_uploaded": caption_result is not None,
            "caption_error": caption_error,
            "youtube_state": state,
            "note": "Private upload, thumbnail, sidecar caption attempt, and scheduled public release completed. No immediate public publish performed.",
        }
    )


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    meta, video, thumb = verify_preconditions()
    print("OK APR-0002..APR-0006 approved for exact hashes")
    print(f"OK title: {meta['title']}")
    print(f"OK video_sha256={sha(video)}")
    print(f"OK thumbnail_sha256={sha(thumb)}")
    print(f"OK captions_sha256={sha(CAPTIONS)}")
    print(f"OK schedule local={SCHEDULED_AT_LOCAL} utc={SCHEDULED_AT_UTC}")
    print("OK upload will be private, madeForKids=false, containsSyntheticMedia=true")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel allowlisted: {channel_id}")

    upload_url = initiate_upload(token, meta, video.stat().st_size)
    print(f"OK resumable upload session started; uploading {video.stat().st_size / 1e6:.0f} MB")
    video_id = upload_chunks(upload_url, token, video)
    if not video_id:
        raise RuntimeError("Upload returned no video_id")
    print(f"OK private upload complete video_id={video_id}")
    write_json(
        IN_PROGRESS,
        {
            "episode_id": EP,
            "video_id": video_id,
            "watch": f"https://youtu.be/{video_id}",
            "studio": f"https://studio.youtube.com/video/{video_id}/edit",
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "status": "uploaded_before_thumbnail_caption_verify",
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "external_upload": True,
        },
    )

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
        write_json(CAPTION_RESULT, {"episode_id": EP, "video_id": video_id, "uploaded": False, "error": caption_error, "caption_file": str(CAPTIONS), "captions_burned_in": True})
        print(f"WARN sidecar captions upload failed; burned-in captions remain: {caption_error}")

    state = get_video_state(token, video_id)
    write_json(STATUS_VERIFY, state)
    items = state.get("items") or []
    status = (items[0].get("status") if items else {}) or {}
    privacy = status.get("privacyStatus")
    publish_at = status.get("publishAt")
    if privacy != "private" or publish_at != SCHEDULED_AT_UTC:
        raise RuntimeError(f"Schedule verification failed: privacy={privacy!r}, publishAt={publish_at!r}")

    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "approval_ids": ["APR-0002", "APR-0003", "APR-0004", "APR-0005", "APR-0006"],
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": privacy,
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "publish_at_platform": publish_at,
        "video_file": str(video),
        "video_sha256": sha(video),
        "thumbnail_file": str(thumb.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": sha(thumb),
        "thumbnail_set": True,
        "thumbnail_result": str(THUMB_RESULT.relative_to(ROOT)).replace("\\", "/"),
        "caption_file": str(CAPTIONS.relative_to(ROOT)).replace("\\", "/"),
        "captions_uploaded": caption_result is not None,
        "caption_error": caption_error,
        "youtube_meta": str(META.relative_to(ROOT)).replace("\\", "/"),
        "final_delivery": str(FINAL_DELIVERY.relative_to(ROOT)).replace("\\", "/"),
        "youtube_state_after": state,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_schedule_set": True,
        "public_immediate_publish": False,
    }
    write_json(RESULT, result)
    update_records(result, caption_result, caption_error, state)
    try:
        IN_PROGRESS.unlink()
    except FileNotFoundError:
        pass

    print(f"RESULT {RESULT.relative_to(ROOT)}")
    print(f"WATCH https://youtu.be/{video_id}")
    print(f"STUDIO https://studio.youtube.com/video/{video_id}/edit")
    print(f"SCHEDULED {SCHEDULED_AT_LOCAL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
