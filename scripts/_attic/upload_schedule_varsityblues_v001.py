#!/usr/bin/env python3
"""Upload PD-2026-019 Varsity Blues privately and schedule public release."""
from __future__ import annotations

import argparse
import json
import mimetypes
import subprocess
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

EP = "PD-2026-019-varsityblues"
REV = "v001"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
APPROVALS = EPDIR / "approvals"
META = PKG / "youtube_meta.v001.json"
FINAL_DELIVERY = PKG / "final_delivery.v001.json"
RIGHTS = PKG / "rights_manifest.v001.json"
ACCEPTANCE = PKG / "acceptance_report.v001.json"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
RESULT = PKG / "youtube_schedule_result.v001.json"
IN_PROGRESS = PKG / "youtube_upload_in_progress.v001.json"
STATUS_VERIFY = PKG / "youtube_status_verify.v001.json"
CAPTION_RESULT = PKG / "youtube_captions_result.v001.json"
THUMB_RESULT = PKG / "youtube_thumbnail_result.v001.json"
SCHEDULED_AT_LOCAL = "2026-07-04T12:00:00+09:00"
SCHEDULED_AT_UTC = "2026-07-04T03:00:00Z"
APPROVAL_IDS = ["APR-0001", "APR-0002", "APR-0003", "APR-0004"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def sha(path: Path) -> str:
    return "sha256:" + sha256_file(path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / value


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def require_file(path: Path) -> None:
    if not path.exists():
        raise RuntimeError(f"Missing required artifact: {path}")


def require_hash(path: Path, expected: str, label: str) -> None:
    actual = sha(path)
    if actual != expected:
        raise RuntimeError(f"{label} hash mismatch: expected {expected}, actual {actual}")


def run_final_gate() -> dict:
    cmd = [sys.executable, str(ROOT / "scripts" / "check_final_acceptance.py"), "19", "--json"]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=900)
    if proc.returncode != 0:
        raise RuntimeError(f"final acceptance gate failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return json.loads(proc.stdout)


def verify_approvals(meta: dict, delivery: dict) -> None:
    for apr_id in APPROVAL_IDS:
        path = APPROVALS / f"{apr_id}.json"
        require_file(path)
        data = load_json(path)
        if data.get("decision") != "approved":
            raise RuntimeError(f"{apr_id} is not approved: {data.get('decision')!r}")
        if data.get("target_revision") != REV and apr_id != "APR-0001":
            raise RuntimeError(f"{apr_id} target revision mismatch: {data.get('target_revision')!r}")
        if apr_id != "APR-0001":
            if data.get("video_sha256") != meta.get("video_sha256"):
                raise RuntimeError(f"{apr_id} video hash mismatch")
            if data.get("thumbnail_sha256") != meta.get("thumbnail_sha256"):
                raise RuntimeError(f"{apr_id} thumbnail hash mismatch")
            if data.get("captions_sha256") != meta.get("captions_sha256"):
                raise RuntimeError(f"{apr_id} captions hash mismatch")
            if data.get("youtube_meta_sha256") != sha(META):
                raise RuntimeError(f"{apr_id} youtube_meta hash mismatch")
            if data.get("rights_manifest_sha256") != meta.get("rights_manifest_sha256"):
                raise RuntimeError(f"{apr_id} rights manifest hash mismatch")
            if data.get("final_delivery_sha256") != sha(FINAL_DELIVERY):
                raise RuntimeError(f"{apr_id} final_delivery hash mismatch")
            if data.get("scheduled_at_local") != SCHEDULED_AT_LOCAL or data.get("scheduled_at_utc") != SCHEDULED_AT_UTC:
                raise RuntimeError(f"{apr_id} schedule mismatch")
    apr4 = load_json(APPROVALS / "APR-0004.json")
    if apr4.get("target_type") != "upload_publish_schedule":
        raise RuntimeError("APR-0004 must authorize upload_publish_schedule")
    schedule = delivery.get("requested_schedule") or {}
    if schedule.get("local_time") != SCHEDULED_AT_LOCAL or schedule.get("utc_time") != SCHEDULED_AT_UTC:
        raise RuntimeError("final_delivery schedule target mismatch")


def upload_caption(token: str, video_id: str, captions: Path) -> dict:
    boundary = f"varsityblues_caption_{int(time.time())}"
    metadata = {"snippet": {"videoId": video_id, "language": "en", "name": "English", "isDraft": False}}
    body = b"".join(
        [
            f"--{boundary}\r\n".encode(),
            b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
            json.dumps(metadata, ensure_ascii=False).encode("utf-8"),
            b"\r\n",
            f"--{boundary}\r\n".encode(),
            b"Content-Type: application/x-subrip\r\n\r\n",
            captions.read_bytes(),
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


def verify_preconditions() -> tuple[dict, Path, Path, Path, dict]:
    existing = [p for p in (RESULT, IN_PROGRESS, STATUS_VERIFY) if p.exists()]
    if existing:
        joined = ", ".join(rel(p) for p in existing)
        raise RuntimeError(f"Existing YouTube result/in-progress file found; refusing duplicate upload: {joined}")
    for path in (META, FINAL_DELIVERY, RIGHTS, ACCEPTANCE, MANIFEST):
        require_file(path)
    gate = run_final_gate()
    if gate.get("status") != "PASS":
        raise RuntimeError(f"final acceptance status is not PASS: {gate.get('status')!r}")
    meta = load_json(META)
    delivery = load_json(FINAL_DELIVERY)
    verify_approvals(meta, delivery)
    video = resolve_path(meta["video_actual_path"])
    thumb = resolve_path(meta["thumbnail"])
    captions = resolve_path(meta["captions_sidecar"])
    for path in (video, thumb, captions):
        require_file(path)
    require_hash(video, meta["video_sha256"], "video")
    require_hash(thumb, meta["thumbnail_sha256"], "thumbnail")
    require_hash(captions, meta["captions_sha256"], "captions")
    require_hash(RIGHTS, meta["rights_manifest_sha256"], "rights_manifest")
    if meta.get("status") != "approved_for_private_upload_and_schedule":
        raise RuntimeError(f"youtube_meta is not upload-approved: {meta.get('status')!r}")
    if delivery.get("status") != "approved_for_private_upload_and_schedule":
        raise RuntimeError(f"final_delivery is not upload-approved: {delivery.get('status')!r}")
    if meta.get("intended_schedule_local") != SCHEDULED_AT_LOCAL or meta.get("intended_schedule_utc") != SCHEDULED_AT_UTC:
        raise RuntimeError("youtube_meta schedule target mismatch")
    if meta.get("upload_performed") or meta.get("publish_performed") or meta.get("schedule_performed"):
        raise RuntimeError("youtube_meta already marks upload, publish, or schedule performed")
    return meta, video, thumb, captions, gate


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
            "thumbnail_uploaded": True,
            "captions_uploaded": caption_result is not None,
            "caption_error": caption_error,
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
                "result": rel(RESULT),
            },
            "external_side_effects": {"upload": True, "publish": False, "schedule": True, "paid_api": False},
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
    manifest.setdefault("active_revisions", {}).update({"youtube_meta": REV, "final_delivery": REV, "rights_manifest": REV, "youtube_schedule_result": REV})
    write_json(MANIFEST, manifest)
    append_event(
        {
            "ts": now,
            "episode_id": EP,
            "stage": "youtube_schedule",
            "event": "youtube_upload_scheduled",
            "revision": REV,
            "actor": "codex",
            "approval_ids": APPROVAL_IDS,
            "video_id": video_id,
            "watch": result["watch"],
            "studio": result["studio"],
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "privacy": "private",
            "thumbnail_set": True,
            "captions_uploaded": caption_result is not None,
            "caption_error": caption_error,
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

    meta, video, thumb, captions, gate = verify_preconditions()
    print("OK EP19 approved for exact YouTube schedule package")
    print(f"OK title: {meta['title']}")
    print(f"OK final gate: {gate['status']} duration={gate.get('render_duration_seconds')}s")
    print(f"OK video_sha256={sha(video)}")
    print(f"OK thumbnail_sha256={sha(thumb)}")
    print(f"OK captions_sha256={sha(captions)}")
    print(f"OK schedule local={SCHEDULED_AT_LOCAL} utc={SCHEDULED_AT_UTC}")
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
            "revision": REV,
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
        caption_result = upload_caption(token, video_id, captions)
        write_json(CAPTION_RESULT, caption_result)
        print("OK sidecar captions uploaded")
    except Exception as exc:
        caption_error = str(exc)
        write_json(CAPTION_RESULT, {"episode_id": EP, "video_id": video_id, "uploaded": False, "error": caption_error, "caption_file": rel(captions), "captions_burned_in": True})
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
        "revision": REV,
        "approval_ids": APPROVAL_IDS,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": privacy,
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "publish_at_platform": publish_at,
        "video_file": str(video).replace("\\", "/"),
        "video_sha256": sha(video),
        "thumbnail_file": rel(thumb),
        "thumbnail_sha256": sha(thumb),
        "thumbnail_set": True,
        "caption_file": rel(captions),
        "captions_uploaded": caption_result is not None,
        "caption_error": caption_error,
        "youtube_meta": rel(META),
        "final_delivery": rel(FINAL_DELIVERY),
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_schedule_set": True,
        "public_immediate_publish": False,
        "youtube_state_after": state,
    }
    write_json(RESULT, result)
    update_records(result, caption_result, caption_error, state)
    try:
        IN_PROGRESS.unlink()
    except FileNotFoundError:
        pass
    print(f"RESULT {rel(RESULT)}")
    print(f"WATCH https://youtu.be/{video_id}")
    print(f"STUDIO https://studio.youtube.com/video/{video_id}/edit")
    print(f"SCHEDULED {SCHEDULED_AT_LOCAL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
