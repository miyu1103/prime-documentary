#!/usr/bin/env python3
"""Upload Kelo to YouTube as private only.

No public publish and no publishAt scheduling are performed by this script.
"""
from __future__ import annotations

import argparse
import json
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


EP = "PD-2026-010-kelo"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / "youtube_meta.v001.json"
RIGHTS = PKG / "rights_manifest.v001.json"
PREFLIGHT = PKG / "publish_preflight.v001.json"
FINAL_DELIVERY = PKG / "final_delivery.v001.json"
FINAL_QC = EPDIR / "08_edit" / "renders" / "final.v001.qc.json"
CAPTION_FILE = EPDIR / "08_edit" / "captions.v001.srt"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
RESULT = PKG / "youtube_private_upload_result.v001.json"
CAPTION_RESULT = PKG / "youtube_captions_result.v001.json"
STATUS_VERIFY = PKG / "youtube_status_verify.v001.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def resolve_path(value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else ROOT / value


def selected_thumbnail_path(meta: dict) -> Path:
    value = meta.get("selected_thumbnail") or meta.get("thumbnail")
    if not value:
        raise RuntimeError("youtube_meta has no selected thumbnail")
    path = resolve_path(value)
    if not path.exists():
        raise RuntimeError(f"Missing selected thumbnail: {path}")
    return path


def video_path(meta: dict) -> Path:
    path = resolve_path(meta["video_actual_path"])
    if not path.exists():
        raise RuntimeError(f"Missing video: {path}")
    return path


def sha(path: Path) -> str:
    return "sha256:" + sha256_file(path)


def request_json(url: str, token: str, data: bytes | None = None, headers: dict[str, str] | None = None, method: str | None = None, timeout: int = 180) -> dict:
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {token}", **(headers or {})}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def initiate_upload(token: str, meta: dict, video: Path) -> str:
    body = json.dumps(
        {
            "snippet": {
                "title": meta["title"],
                "description": meta["description"].rstrip(),
                "tags": meta.get("tags", []),
                "categoryId": str(meta.get("categoryId", "27")),
                "defaultLanguage": meta.get("defaultLanguage", "en"),
                "defaultAudioLanguage": meta.get("defaultAudioLanguage", "en"),
            },
            "status": {
                "privacyStatus": "private",
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
            "X-Upload-Content-Length": str(video.stat().st_size),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        upload_url = resp.headers.get("Location", "")
    if not upload_url.startswith("https://www.googleapis.com/"):
        raise RuntimeError(f"Unexpected upload URL host: {upload_url[:80]}")
    return upload_url


def set_thumbnail(token: str, video_id: str, path: Path) -> dict:
    return request_json(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        token,
        data=path.read_bytes(),
        headers={"Content-Type": "image/png"},
        method="POST",
        timeout=180,
    )


def upload_caption(token: str, video_id: str) -> dict:
    boundary = f"kelo_caption_{int(time.time())}"
    metadata = {"snippet": {"videoId": video_id, "language": "en", "name": "English", "isDraft": False}}
    body = b"".join(
        [
            f"--{boundary}\r\n".encode(),
            b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
            json.dumps(metadata, ensure_ascii=False).encode("utf-8"),
            b"\r\n",
            f"--{boundary}\r\n".encode(),
            b"Content-Type: application/octet-stream\r\n\r\n",
            CAPTION_FILE.read_bytes(),
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        ]
    )
    return request_json(
        "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
        token,
        data=body,
        headers={"Content-Type": f"multipart/related; boundary={boundary}"},
        method="POST",
        timeout=180,
    )


def get_video_state(token: str, video_id: str) -> dict:
    return request_json(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        token,
        timeout=60,
    )


def compact_state(state: dict) -> dict:
    item = (state.get("items") or [{}])[0]
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


def verify_preconditions() -> tuple[dict, Path, Path]:
    existing = sorted(PKG.glob("youtube_private_upload_result*.json")) + sorted(PKG.glob("youtube_schedule_result*.json"))
    if existing:
        raise RuntimeError("Existing YouTube result found; refusing duplicate upload: " + ", ".join(str(p.relative_to(ROOT)) for p in existing))
    for path in [META, RIGHTS, PREFLIGHT, FINAL_DELIVERY, FINAL_QC, CAPTION_FILE]:
        if not path.exists():
            raise RuntimeError(f"Missing required artifact: {path}")
    meta = load_json(META)
    rights = load_json(RIGHTS)
    preflight = load_json(PREFLIGHT)
    qc = load_json(FINAL_QC)
    video = video_path(meta)
    thumb = selected_thumbnail_path(meta)
    if rights.get("status") != "clear":
        raise RuntimeError(f"rights status is not clear: {rights.get('status')!r}")
    checks = preflight.get("checks", {})
    required_true = [
        "final_qc_pass",
        "video_hash_matches_youtube_meta",
        "thumbnail_hash_matches_youtube_meta",
        "rights_clear",
        "privacy_target_private",
        "public_release_gate_closed",
        "script_claims_locked",
    ]
    required_false = ["publish_or_schedule_requested", "real_person_likeness_risk"]
    if preflight.get("status") != "PASS":
        raise RuntimeError("preflight is not PASS")
    if any(checks.get(key) is not True for key in required_true):
        raise RuntimeError(f"preflight required true checks failed: {checks}")
    if any(checks.get(key) is not False for key in required_false):
        raise RuntimeError(f"preflight required false checks failed: {checks}")
    if qc.get("status") != "PASS":
        raise RuntimeError("final QC is not PASS")
    if meta.get("privacy_status_target") != "private":
        raise RuntimeError("youtube_meta target is not private")
    if meta.get("publish_performed") is not False or meta.get("schedule_performed") is not False:
        raise RuntimeError("youtube_meta must keep publish/schedule false")
    if meta.get("video_sha256") != sha(video):
        raise RuntimeError(f"video hash mismatch: meta={meta.get('video_sha256')} actual={sha(video)}")
    if meta.get("selected_thumbnail_sha256") != sha(thumb):
        raise RuntimeError("thumbnail hash mismatch")
    return meta, video, thumb


def update_records(meta: dict, result: dict, caption: dict | None, state: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    meta.update(
        {
            "status": "private_uploaded_public_gate_closed",
            "upload_performed": True,
            "publish_performed": False,
            "schedule_performed": False,
            "video_id": result["video_id"],
            "video_url": result["watch"],
            "studio_url": result["studio"],
            "youtube_channel_id": result["channel_id"],
            "private_upload_result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
            "captions_uploaded": caption is not None,
            "captions_result": str(CAPTION_RESULT.relative_to(ROOT)).replace("\\", "/") if caption else None,
            "status_verify_result": str(STATUS_VERIFY.relative_to(ROOT)).replace("\\", "/"),
            "processing_status": compact_state(state).get("processingStatus"),
            "processing_status_verified_at": now,
            "public_schedule_active": False,
            "publish_gate": "closed",
            "updated_at": now,
        }
    )
    write_json(META, meta)

    manifest = load_json(MANIFEST)
    manifest["state"] = "private_uploaded"
    manifest["video_id"] = result["video_id"]
    manifest["video_url"] = result["watch"]
    manifest["public_schedule_active"] = False
    manifest["updated_at"] = now
    manifest.setdefault("active_revisions", {}).update(
        {
            "youtube_meta": "v001",
            "youtube_private_upload_result": "v001",
            "youtube_captions_result": "v001" if caption else None,
            "youtube_status_verify": "v001",
            "final_delivery": "v001",
            "final_qc": "v001",
            "rights_manifest": "v001",
        }
    )
    warning = f"YouTube private upload completed for Kelo: video_id {result['video_id']}. Public publish/schedule not performed; owner approval still required."
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    write_json(MANIFEST, manifest)
    append_event(
        {
            "event": "youtube_private_upload_completed",
            "episode_id": EP,
            "stage": "private_uploaded",
            "revision": "v001",
            "actor": "codex",
            "detail": warning,
            "video_id": result["video_id"],
            "watch": result["watch"],
            "studio": result["studio"],
            "thumbnail_set": result["thumbnail_set"],
            "captions_uploaded": caption is not None,
            "publish_performed": False,
            "schedule_performed": False,
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
    parser.add_argument("--video-id", default=None, help="Recover/finalize an already uploaded private video ID.")
    args = parser.parse_args(argv)
    meta, video, thumb = verify_preconditions()
    print(f"OK private preflight: {meta['title']}")
    print(f"OK video {video.stat().st_size / 1e6:.0f} MB {sha(video)}")
    print(f"OK thumbnail {sha(thumb)}")
    if args.dry_run:
        print("DRY_RUN_OK no external writes")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted")
    if args.video_id:
        video_id = args.video_id
    else:
        upload_url = initiate_upload(token, meta, video)
        video_id = upload_chunks(upload_url, token, video)
        if not video_id:
            raise RuntimeError("Upload returned no video_id")
    thumb_status = set_thumbnail(token, video_id, thumb)
    caption = None
    caption_error = None
    try:
        caption = upload_caption(token, video_id)
        write_json(CAPTION_RESULT, caption)
    except Exception as exc:
        caption_error = str(exc)
    state = get_video_state(token, video_id)
    write_json(STATUS_VERIFY, state)
    compact = compact_state(state)
    if compact.get("privacyStatus") != "private" or compact.get("publishAt"):
        raise RuntimeError(f"privacy verification failed: {compact}")
    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": compact.get("privacyStatus"),
        "publishAt": compact.get("publishAt"),
        "video_file": str(video),
        "video_sha256": sha(video),
        "thumbnail_file": str(thumb.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": sha(thumb),
        "thumbnail_set": True,
        "thumbnail_status": thumb_status,
        "captions_uploaded": caption is not None,
        "caption_error": caption_error,
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "publish_performed": False,
        "schedule_performed": False,
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "youtube_state_compact": compact,
    }
    write_json(RESULT, result)
    update_records(meta, result, caption, state)
    print(f"PRIVATE_UPLOAD_OK video_id={video_id}")
    print(f"STUDIO {result['studio']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
