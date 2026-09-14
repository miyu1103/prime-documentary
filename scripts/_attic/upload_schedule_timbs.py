#!/usr/bin/env python3
"""Upload PD-2026-009 Timbs to YouTube and schedule public release.

Safety behavior:
- refuses duplicate upload if a schedule result already exists
- verifies exact hashes from APR-0002 before any external write
- uploads private first
- sets containsSyntheticMedia=true and selfDeclaredMadeForKids=false
- checks channel allowlist
- sets thumbnail and sidecar captions
- verifies YouTube privacy/publishAt after scheduling
"""
from __future__ import annotations

import argparse
import json
import mimetypes
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


EP = "PD-2026-009-timbs"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / "youtube_meta.v001.json"
RIGHTS = PKG / "rights_manifest.v001.json"
FINAL_QC = EPDIR / "08_edit" / "renders" / "rough.v001.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
APR_ID = "APR-0002"
APR = EPDIR / "approvals" / f"{APR_ID}.json"
VIDEO = ROOT / "remotion" / "out" / "timbs_rough.mp4"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
RESULT = PKG / "youtube_schedule_result.v001.json"
STATUS_VERIFY = PKG / "youtube_status_verify.v001.json"
CAPTION_RESULT = PKG / "youtube_captions_result.v001.json"

SCHEDULED_AT_LOCAL = "2026-06-24T12:00:00+09:00"
SCHEDULED_AT_UTC = "2026-06-24T03:00:00Z"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text("utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", "utf-8")


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def sha(path: Path) -> str:
    return "sha256:" + sha256_file(path)


def resolve_path(value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else ROOT / value


def selected_thumbnail_path(meta: dict) -> Path:
    raw = meta.get("selected_thumbnail") or meta.get("thumbnail")
    if not raw:
        raise RuntimeError("youtube_meta selected thumbnail missing")
    p = resolve_path(raw)
    if not p.exists():
        raise RuntimeError(f"selected thumbnail missing: {p}")
    return p


def verify_preconditions() -> tuple[dict, dict, Path]:
    existing = sorted(PKG.glob("youtube_schedule_result*.json"))
    if existing:
        joined = ", ".join(str(p.relative_to(ROOT)) for p in existing)
        raise RuntimeError(f"Existing schedule result found; refusing duplicate upload: {joined}")
    for path in [APR, META, RIGHTS, FINAL_QC, VIDEO, CAPTIONS]:
        if not path.exists():
            raise RuntimeError(f"Missing required file: {path}")

    apr = load_json(APR)
    meta = load_json(META)
    rights = load_json(RIGHTS)
    qc = load_json(FINAL_QC)
    thumb = selected_thumbnail_path(meta)

    if apr.get("decision") != "approved":
        raise RuntimeError(f"{APR_ID} not approved: {apr.get('decision')!r}")
    if apr.get("scheduled_at_utc") != SCHEDULED_AT_UTC:
        raise RuntimeError("APR schedule does not match target UTC")
    if meta.get("publish_performed") is not False:
        raise RuntimeError("youtube_meta does not explicitly keep publish_performed=false")
    if rights.get("status") not in {"draft_ready_for_review", "ready", "clear"}:
        raise RuntimeError(f"Unexpected rights status: {rights.get('status')!r}")
    if qc.get("status") != "first_cut_ready_for_review":
        raise RuntimeError(f"Unexpected QC status: {qc.get('status')!r}")

    checks = {
        "video_sha256": sha(VIDEO),
        "youtube_meta_sha256": sha(META),
        "thumbnail_sha256": sha(thumb),
        "captions_sha256": sha(CAPTIONS),
    }
    for key, actual in checks.items():
        expected = apr.get(key) or meta.get(key)
        if expected and actual != expected:
            raise RuntimeError(f"{key} mismatch: expected {expected}, actual {actual}")
    if meta.get("video_sha256") != checks["video_sha256"]:
        raise RuntimeError("youtube_meta video hash mismatch")
    if meta.get("selected_thumbnail_sha256") != checks["thumbnail_sha256"]:
        raise RuntimeError("youtube_meta thumbnail hash mismatch")
    return apr, meta, thumb


def initiate_upload(token: str, meta: dict, file_size: int) -> str:
    body = json.dumps(
        {
            "snippet": {
                "title": meta["title"],
                "description": meta["description"],
                "tags": meta.get("tags", []),
                "categoryId": meta.get("categoryId", "27"),
                "defaultLanguage": meta.get("defaultLanguage", "en"),
                "defaultAudioLanguage": meta.get("defaultAudioLanguage", "en"),
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": SCHEDULED_AT_UTC,
                "selfDeclaredMadeForKids": False,
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


def set_thumbnail(token: str, video_id: str, path: Path) -> dict:
    content_type = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=path.read_bytes(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": content_type},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def upload_caption(token: str, video_id: str) -> dict:
    boundary = f"timbs_caption_{int(time.time())}"
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
    caption_bytes = CAPTIONS.read_bytes()
    body = (
        f"--{boundary}\r\n"
        "Content-Type: application/json; charset=UTF-8\r\n\r\n"
    ).encode("utf-8") + metadata + (
        f"\r\n--{boundary}\r\n"
        "Content-Type: application/x-subrip\r\n\r\n"
    ).encode("utf-8") + caption_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
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


def get_video_state(token: str, video_id: str) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def update_local_records(result: dict, caption_result: dict | None) -> None:
    meta = load_json(META)
    meta.update(
        {
            "status": "scheduled",
            "approval_ids": sorted(set(meta.get("approval_ids", []) + [APR_ID])),
            "upload_performed": True,
            "publish_performed": False,
            "video_id": result["video_id"],
            "video_url": result["watch"],
            "studio_url": result["studio"],
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "publish_at_platform": result["publish_at_platform"],
            "schedule_result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
            "processing_status_verified_at": datetime.now(timezone.utc).isoformat(),
            "captions_uploaded": caption_result is not None,
            "captions_result": str(CAPTION_RESULT.relative_to(ROOT)).replace("\\", "/") if caption_result else None,
        }
    )
    write_json(META, meta)

    manifest = load_json(MANIFEST)
    manifest["state"] = "scheduled"
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest["video_id"] = result["video_id"]
    manifest["video_url"] = result["watch"]
    manifest.setdefault("approvals", [])
    for approval in ["APR-0001", APR_ID]:
        if approval not in manifest["approvals"]:
            manifest["approvals"].append(approval)
    manifest.setdefault("active_revisions", {}).update(
        {
            "youtube_meta": "v001",
            "rights_manifest": "v001",
            "youtube_schedule_result": "v001",
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
            "ts": datetime.now(timezone.utc).isoformat(),
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

    _apr, meta, thumb = verify_preconditions()
    print(f"OK {APR_ID} approved")
    print(f"OK target channel must be allowlisted: {sorted(CHANNEL_ALLOWLIST)}")
    print(f"OK title: {meta['title']}")
    print(f"OK video_sha256={sha(VIDEO)}")
    print(f"OK thumbnail_sha256={sha(thumb)}")
    print(f"OK captions_sha256={sha(CAPTIONS)}")
    print(f"OK schedule local={SCHEDULED_AT_LOCAL} utc={SCHEDULED_AT_UTC}")
    print("OK YouTube status will be private, madeForKids=false, containsSyntheticMedia=true")
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
        "video_file": str(VIDEO),
        "video_sha256": sha(VIDEO),
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
    print(f"RESULT {RESULT.relative_to(ROOT)}")
    print(f"WATCH https://youtu.be/{video_id}")
    print(f"STUDIO https://studio.youtube.com/video/{video_id}/edit")
    print(f"SCHEDULED {SCHEDULED_AT_LOCAL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
