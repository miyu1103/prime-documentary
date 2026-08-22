#!/usr/bin/env python3
"""Upload PD-2026-012 Arbitration to YouTube and schedule public release."""
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


EP = "PD-2026-012-arbitration"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / "youtube_meta.v001.json"
RIGHTS = PKG / "rights_manifest.v001.json"
FINAL_DELIVERY = PKG / "final_delivery.v001.json"
FINAL_QC = EPDIR / "08_edit" / "renders" / "final.v001.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
APR_ID = "APR-0002"
APR = EPDIR / "approvals" / f"{APR_ID}.json"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
RESULT = PKG / "youtube_schedule_result.v001.json"
IN_PROGRESS = PKG / "youtube_upload_in_progress.v001.json"
STATUS_VERIFY = PKG / "youtube_status_verify.v001.json"
CAPTION_RESULT = PKG / "youtube_captions_result.v001.json"

SCHEDULED_AT_LOCAL = "2026-06-27T12:00:00+09:00"
SCHEDULED_AT_UTC = "2026-06-27T03:00:00Z"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def sha(path: Path) -> str:
    return "sha256:" + sha256_file(path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / value


def path_from_meta(meta: dict, key: str) -> Path:
    value = meta.get(key)
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"youtube_meta missing {key}")
    path = resolve_path(value)
    if not path.exists():
        raise RuntimeError(f"Missing {key}: {path}")
    return path


def description_text(meta: dict) -> str:
    path = path_from_meta(meta, "description_file")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise RuntimeError("Description is empty")
    return text


def upload_caption(token: str, video_id: str) -> dict:
    boundary = f"arbitration_caption_{int(time.time())}"
    metadata = json.dumps(
        {
            "snippet": {
                "videoId": video_id,
                "language": "en",
                "name": "Prime Documentary English captions",
                "isDraft": False,
            }
        }
    ).encode("utf-8")
    body = (
        f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n"
    ).encode("utf-8") + metadata + (
        f"\r\n--{boundary}\r\nContent-Type: application/x-subrip\r\n\r\n"
    ).encode("utf-8") + CAPTIONS.read_bytes() + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/related; boundary={boundary}",
        },
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


def initiate_upload(token: str, meta: dict, description: str, file_size: int) -> str:
    body = json.dumps(
        {
            "snippet": {
                "title": meta["title"],
                "description": description,
                "tags": meta.get("tags", []),
                "categoryId": str(meta.get("category_id", "27")),
                "defaultLanguage": meta.get("default_language", "en"),
                "defaultAudioLanguage": meta.get("default_audio_language", "en"),
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": SCHEDULED_AT_UTC,
                "selfDeclaredMadeForKids": bool(meta.get("made_for_kids", False)),
                "containsSyntheticMedia": True,
                "license": "youtube",
                "embeddable": True,
                "publicStatsViewable": True,
            },
        }
    ).encode("utf-8")
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


def verify_preconditions() -> tuple[dict, dict, Path, Path, str]:
    existing = [p for p in [RESULT, IN_PROGRESS, STATUS_VERIFY] if p.exists()]
    if existing:
        joined = ", ".join(str(p.relative_to(ROOT)) for p in existing)
        raise RuntimeError(f"Existing YouTube result/in-progress file found; refusing duplicate upload: {joined}")
    for path in [APR, META, RIGHTS, FINAL_QC, FINAL_DELIVERY, CAPTIONS, MANIFEST]:
        if not path.exists():
            raise RuntimeError(f"Missing required file: {path}")

    apr = load_json(APR)
    meta = load_json(META)
    rights = load_json(RIGHTS)
    qc = load_json(FINAL_QC)
    video = resolve_path(apr["video"])
    thumb = path_from_meta(meta, "thumbnail_file")
    description = description_text(meta)

    if apr.get("decision") != "approved":
        raise RuntimeError(f"{APR_ID} is not approved: {apr.get('decision')!r}")
    if apr.get("scheduled_at_local") != SCHEDULED_AT_LOCAL or apr.get("scheduled_at_utc") != SCHEDULED_AT_UTC:
        raise RuntimeError("APR schedule does not match target schedule")
    if meta.get("intended_schedule_local") != SCHEDULED_AT_LOCAL or meta.get("intended_schedule_utc") != SCHEDULED_AT_UTC:
        raise RuntimeError("youtube_meta intended schedule does not match target")
    if meta.get("upload_performed") is not False or meta.get("publish_performed") is not False or meta.get("schedule_performed") is not False:
        raise RuntimeError("youtube_meta already marks upload, publish, or schedule performed")
    if qc.get("status") != "PASS":
        raise RuntimeError(f"Final QC is not PASS: {qc.get('status')!r}")
    if qc.get("sha256") and meta.get("video_sha256") != "sha256:" + qc["sha256"]:
        raise RuntimeError("Final QC video hash does not match youtube_meta")
    if rights.get("commercial_use") != "allowed":
        raise RuntimeError("Rights manifest does not clear commercial use")

    assertions = rights.get("assertions", {})
    required_true = [
        "script_claims_unchanged",
        "claims_ledger_unchanged",
        "no_real_person_likeness",
        "no_judge_likeness_or_portraits",
        "ai_visuals_symbolic_not_evidence",
        "stock_visuals_symbolic_not_case_footage",
        "critics_forced_arbitration_term_attributed",
        "critics_defenders_balanced",
        "commercial_ok_assets_only",
        "elevenlabs_tts_owner_approved",
        "external_upload_not_performed",
    ]
    missing = [key for key in required_true if assertions.get(key) is not True]
    if missing:
        raise RuntimeError(f"Rights assertions are not clear: {missing}")
    if "critics' concern about what they call forced arbitration" not in description:
        raise RuntimeError("Description does not attribute forced arbitration to critics")

    checks = {
        "video_sha256": sha(video),
        "youtube_meta_sha256": sha(META),
        "thumbnail_sha256": sha(thumb),
        "captions_sha256": sha(CAPTIONS),
    }
    for key, actual in checks.items():
        expected = apr.get(key) or meta.get(key)
        if expected and actual != expected:
            raise RuntimeError(f"{key} mismatch: expected {expected}, actual {actual}")
    if meta.get("video_sha256") != checks["video_sha256"]:
        raise RuntimeError("youtube_meta video_sha256 mismatch")
    if meta.get("thumbnail_sha256") != checks["thumbnail_sha256"]:
        raise RuntimeError("youtube_meta thumbnail_sha256 mismatch")
    return apr, meta, video, thumb, description


def update_local_records(result: dict, caption_result: dict | None) -> None:
    now = datetime.now(timezone.utc).isoformat()
    meta = load_json(META)
    meta.update(
        {
            "status": "scheduled",
            "upload_performed": True,
            "publish_performed": False,
            "schedule_performed": True,
            "publish_gate": "owner_approved_scheduled_publication",
            "video_id": result["video_id"],
            "video_url": result["watch"],
            "studio_url": result["studio"],
            "youtube_channel_id": result["channel_id"],
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "publish_at_platform": result["publish_at_platform"],
            "schedule_result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
            "status_verify": str(STATUS_VERIFY.relative_to(ROOT)).replace("\\", "/"),
            "approval_ids": sorted(set(meta.get("approval_ids", []) + [APR_ID])),
            "captions_uploaded": caption_result is not None,
            "captions_result": str(CAPTION_RESULT.relative_to(ROOT)).replace("\\", "/") if caption_result else None,
            "processing_status_verified_at": now,
        }
    )
    write_json(META, meta)

    rights = load_json(RIGHTS)
    rights["status"] = "cleared_for_scheduled_publication"
    rights["publication_gate"] = "owner_approved_scheduled_publication"
    rights["publication_approval"] = APR_ID
    rights["youtube_video_id"] = result["video_id"]
    rights["scheduled_at_local"] = SCHEDULED_AT_LOCAL
    rights["scheduled_at_utc"] = SCHEDULED_AT_UTC
    rights.setdefault("assertions", {})["external_upload_not_performed"] = False
    rights.setdefault("assertions", {})["youtube_upload_scheduled_by_owner_approval"] = True
    write_json(RIGHTS, rights)

    final_delivery = load_json(FINAL_DELIVERY)
    final_delivery["status"] = "scheduled"
    final_delivery.setdefault("youtube", {}).update(
        {
            "video_id": result["video_id"],
            "watch": result["watch"],
            "studio": result["studio"],
            "privacy": "private",
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "upload_performed": True,
            "schedule_performed": True,
            "public_immediate_publish": False,
            "result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
        }
    )
    write_json(FINAL_DELIVERY, final_delivery)

    manifest = load_json(MANIFEST)
    manifest["state"] = "scheduled"
    manifest["updated_at"] = now
    manifest["video_id"] = result["video_id"]
    manifest["video_url"] = result["watch"]
    approvals = manifest.setdefault("approvals", [])
    for approval in ["APR-0001", APR_ID]:
        if approval not in approvals:
            approvals.append(approval)
    manifest.setdefault("active_revisions", {}).update(
        {
            "youtube_meta": "v001",
            "rights_manifest": "v001",
            "final_delivery": "v001",
            "youtube_schedule_result": "v001",
            "youtube_status_verify": "v001",
            "youtube_captions_result": "v001" if caption_result else None,
        }
    )
    warning = (
        f"YouTube private upload completed and scheduled under {APR_ID}: "
        f"video_id {result['video_id']}, public release {SCHEDULED_AT_LOCAL}. "
        "containsSyntheticMedia=true; immediate public publish not performed."
    )
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    write_json(MANIFEST, manifest)

    append_event(
        {
            "event": "youtube_upload_scheduled",
            "episode_id": EP,
            "stage": "scheduled",
            "revision": "v001",
            "actor": "codex",
            "approval_id": APR_ID,
            "detail": warning,
            "video_id": result["video_id"],
            "watch": result["watch"],
            "studio": result["studio"],
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "thumbnail_set": result["thumbnail_set"],
            "captions_uploaded": caption_result is not None,
            "ts": now,
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

    _apr, meta, video, thumb, description = verify_preconditions()
    print(f"OK {APR_ID} approved")
    print(f"OK title: {meta['title']}")
    print(f"OK video_sha256={sha(video)}")
    print(f"OK thumbnail_sha256={sha(thumb)}")
    print(f"OK captions_sha256={sha(CAPTIONS)}")
    print(f"OK schedule local={SCHEDULED_AT_LOCAL} utc={SCHEDULED_AT_UTC}")
    print(f"OK target channel must be allowlisted: {sorted(CHANNEL_ALLOWLIST)}")
    print("OK upload will be private, madeForKids=false, containsSyntheticMedia=true")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    print("OK access token obtained")
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel allowlisted: {channel_id}")

    upload_url = initiate_upload(token, meta, description, video.stat().st_size)
    print(f"OK resumable upload session started; uploading {video.stat().st_size / 1e6:.0f} MB")
    video_id = upload_chunks(upload_url, token, video)
    if not video_id:
        raise RuntimeError("Upload returned no video_id")
    print(f"OK private upload complete video_id={video_id}")

    write_json(
        IN_PROGRESS,
        {
            "schema_version": "1.0.0",
            "episode_id": EP,
            "approval_ref": APR_ID,
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
    print("OK thumbnail set")

    caption_result = None
    caption_error = None
    try:
        caption_result = upload_caption(token, video_id)
        write_json(CAPTION_RESULT, caption_result)
        print("OK sidecar captions uploaded")
    except Exception as exc:
        caption_error = str(exc)
        print(f"WARN sidecar captions upload failed; burned-in captions remain: {caption_error}")

    state_after = get_video_state(token, video_id)
    write_json(STATUS_VERIFY, state_after)
    items = state_after.get("items") or []
    status = (items[0].get("status") if items else {}) or {}
    privacy = status.get("privacyStatus")
    publish_at = status.get("publishAt")
    if privacy != "private" or publish_at != SCHEDULED_AT_UTC:
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
        "video_file": str(video),
        "video_sha256": sha(video),
        "thumbnail_file": str(thumb),
        "thumbnail_sha256": sha(thumb),
        "thumbnail_set": True,
        "thumbnail_status": thumb_status,
        "caption_file": str(CAPTIONS),
        "captions_uploaded": caption_result is not None,
        "caption_error": caption_error,
        "youtube_meta": str(META),
        "youtube_state_after": state_after,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_schedule_set": True,
        "public_immediate_publish": False,
    }
    write_json(RESULT, result)
    update_local_records(result, caption_result)
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
