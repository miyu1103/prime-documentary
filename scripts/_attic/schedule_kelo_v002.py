#!/usr/bin/env python3
"""Schedule the already-uploaded Kelo v002 YouTube video.

This script does not upload a new file and does not perform an immediate public
publish. It sets publishAt on the existing private video after owner approval.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, sha256_file


EP = "PD-2026-010-kelo"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / "youtube_meta.v002.json"
RIGHTS = PKG / "rights_manifest.v002.json"
PREFLIGHT = PKG / "publish_preflight.v002.json"
FINAL_DELIVERY = PKG / "final_delivery.v002.json"
FINAL_QC = EPDIR / "08_edit" / "renders" / "final.v002.qc.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v002.srt"
APR = EPDIR / "approvals" / "APR-0002.json"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
UPLOAD_RESULT = PKG / "youtube_private_upload_result.v002.json"
RESULT = PKG / "youtube_schedule_result.v002.json"
STATUS_VERIFY = PKG / "youtube_status_verify.scheduled.v002.json"

SCHEDULED_AT_LOCAL = "2026-06-25T12:00:00+09:00"
SCHEDULED_AT_UTC = "2026-06-25T03:00:00Z"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text("utf-8"))


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


def request_json(url: str, token: str, data: bytes | None = None, headers: dict[str, str] | None = None, method: str | None = None, timeout: int = 120) -> dict:
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {token}", **(headers or {})}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_video_state(token: str, video_id: str) -> dict:
    return request_json(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        token,
        timeout=60,
    )


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
    return request_json(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        token,
        data=json.dumps({"id": video_id, "status": status}).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=UTF-8"},
        method="PUT",
        timeout=60,
    )


def update_snippet(token: str, video_id: str, existing_state: dict, meta: dict) -> dict:
    items = existing_state.get("items") or []
    existing_snippet = (items[0].get("snippet") if items else {}) or {}
    snippet = {
        "title": meta["title"],
        "description": meta["description"].rstrip(),
        "tags": meta.get("tags", []),
        "categoryId": str(meta.get("categoryId") or existing_snippet.get("categoryId") or "27"),
        "defaultLanguage": meta.get("defaultLanguage", existing_snippet.get("defaultLanguage", "en")),
        "defaultAudioLanguage": meta.get("defaultAudioLanguage", existing_snippet.get("defaultAudioLanguage", "en")),
    }
    return request_json(
        "https://www.googleapis.com/youtube/v3/videos?part=snippet",
        token,
        data=json.dumps({"id": video_id, "snippet": snippet}).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=UTF-8"},
        method="PUT",
        timeout=60,
    )


def set_thumbnail(token: str, video_id: str, path: Path) -> dict:
    return request_json(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        token,
        data=path.read_bytes(),
        headers={"Content-Type": "image/png"},
        method="POST",
        timeout=180,
    )


def verify_preconditions(allow_existing_result: bool = False) -> tuple[dict, dict, dict, Path, Path]:
    if RESULT.exists() and not allow_existing_result:
        raise RuntimeError(f"Existing schedule result found; refusing duplicate schedule: {RESULT.relative_to(ROOT)}")
    for path in [APR, META, RIGHTS, PREFLIGHT, FINAL_DELIVERY, FINAL_QC, CAPTIONS, UPLOAD_RESULT]:
        if not path.exists():
            raise RuntimeError(f"Missing required artifact: {path}")
    apr = load_json(APR)
    meta = load_json(META)
    rights = load_json(RIGHTS)
    preflight = load_json(PREFLIGHT)
    qc = load_json(FINAL_QC)
    upload = load_json(UPLOAD_RESULT)
    video = video_path(meta)
    thumb = selected_thumbnail_path(meta)
    if apr.get("decision") != "approved":
        raise RuntimeError(f"APR-0002 not approved: {apr.get('decision')!r}")
    if apr.get("scheduled_at_local") != SCHEDULED_AT_LOCAL or apr.get("scheduled_at_utc") != SCHEDULED_AT_UTC:
        raise RuntimeError("APR schedule does not match requested schedule")
    if rights.get("status") != "clear":
        raise RuntimeError(f"rights status is not clear: {rights.get('status')!r}")
    if preflight.get("status") != "PASS":
        raise RuntimeError("preflight is not PASS")
    if qc.get("status") != "PASS":
        raise RuntimeError("final QC is not PASS")
    if meta.get("publish_performed") is not False:
        raise RuntimeError("youtube_meta already marks public publish performed")
    if meta.get("video_id") != upload.get("video_id") or meta.get("video_id") != apr.get("youtube_video_id"):
        raise RuntimeError("video_id mismatch between APR, meta, and upload result")
    if meta.get("video_sha256") != sha(video):
        raise RuntimeError(f"video hash mismatch: meta={meta.get('video_sha256')} actual={sha(video)}")
    if meta.get("selected_thumbnail_sha256") != sha(thumb):
        raise RuntimeError("thumbnail hash mismatch")
    if apr.get("exact_video_sha256") != sha(video) or apr.get("selected_thumbnail_sha256") != sha(thumb):
        raise RuntimeError("approval exact hashes do not match current artifacts")
    return apr, meta, upload, video, thumb


def update_records(result: dict, state_after: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    meta = load_json(META)
    meta.update(
        {
            "status": "scheduled",
            "publish_performed": False,
            "schedule_performed": True,
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "publish_at_platform": result["publish_at_platform"],
            "schedule_result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
            "status_verify_scheduled_result": str(STATUS_VERIFY.relative_to(ROOT)).replace("\\", "/"),
            "public_schedule_active": True,
            "publish_gate": "owner_approved_scheduled",
            "approval_ids": sorted(set(meta.get("approval_ids", []) + ["APR-0002"])),
            "updated_at": now,
        }
    )
    meta.setdefault("pre_publish_checks", {}).update(
        {
            "owner_schedule_approval": str(APR.relative_to(ROOT)).replace("\\", "/"),
            "schedule_result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
        }
    )
    write_json(META, meta)

    preflight = load_json(PREFLIGHT)
    preflight["generated_at"] = now
    preflight["status"] = "PASS"
    preflight["checks"]["publish_or_schedule_requested"] = True
    preflight["checks"]["public_release_gate_closed"] = False
    preflight["checks"]["owner_schedule_approval_present"] = True
    preflight["checks"]["youtube_schedule_verified"] = True
    preflight["scheduled_at_local"] = SCHEDULED_AT_LOCAL
    preflight["scheduled_at_utc"] = SCHEDULED_AT_UTC
    preflight["schedule_result"] = str(RESULT.relative_to(ROOT)).replace("\\", "/")
    write_json(PREFLIGHT, preflight)

    final_delivery = load_json(FINAL_DELIVERY)
    final_delivery["status"] = "scheduled"
    final_delivery["generated_at"] = now
    final_delivery["youtube"].update(
        {
            "publish_gate": "owner_approved_scheduled",
            "public_schedule_active": True,
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "schedule_result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
        }
    )
    write_json(FINAL_DELIVERY, final_delivery)

    manifest = load_json(MANIFEST)
    manifest["state"] = "scheduled"
    manifest["video_id"] = result["video_id"]
    manifest["video_url"] = result["watch"]
    manifest["updated_at"] = now
    if "APR-0002" not in manifest.setdefault("approvals", []):
        manifest["approvals"].append("APR-0002")
    manifest.setdefault("active_revisions", {}).update(
        {
            "youtube_meta": "v002",
            "youtube_schedule_result": "v002",
            "youtube_status_verify_scheduled": "v002",
            "final_delivery": "v002",
            "final_qc": "v002",
            "rights_manifest": "v002",
            "captions_final": "v002",
            "thumbnail_candidates": "v002",
            "approval_publish_schedule": "v002",
        }
    )
    warning = f"Kelo v002 scheduled on YouTube: video_id {result['video_id']} for {SCHEDULED_AT_LOCAL}. Immediate public publish not performed."
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    write_json(MANIFEST, manifest)

    append_event(
        {
            "event": "youtube_schedule_set",
            "episode_id": EP,
            "stage": "scheduled",
            "revision": "v002",
            "actor": "codex",
            "approval_id": "APR-0002",
            "detail": warning,
            "video_id": result["video_id"],
            "watch": result["watch"],
            "studio": result["studio"],
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "publish_at_platform": result["publish_at_platform"],
            "thumbnail_set": result["thumbnail_set"],
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
    parser.add_argument("--allow-existing-result", action="store_true")
    args = parser.parse_args(argv)

    apr, meta, upload, video, thumb = verify_preconditions(allow_existing_result=args.allow_existing_result)
    video_id = meta["video_id"]
    print(f"OK APR-0002 approved for {SCHEDULED_AT_LOCAL}")
    print(f"OK target video_id={video_id}")
    print(f"OK video {video.stat().st_size / 1e6:.0f} MB {sha(video)}")
    print(f"OK thumbnail {sha(thumb)}")
    if args.dry_run:
        print("DRY_RUN_OK no external writes")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    state_before = get_video_state(token, video_id)
    if not state_before.get("items"):
        raise RuntimeError(f"YouTube video not found: {video_id}")
    snippet_update = update_snippet(token, video_id, state_before, meta)
    schedule_update = update_schedule(token, video_id, state_before)
    thumb_status = set_thumbnail(token, video_id, thumb)
    state_after = get_video_state(token, video_id)
    write_json(STATUS_VERIFY, state_after)
    item = (state_after.get("items") or [{}])[0]
    status = item.get("status", {})
    publish_at = status.get("publishAt")
    privacy = status.get("privacyStatus")
    if privacy != "private" or publish_at != SCHEDULED_AT_UTC:
        raise RuntimeError(f"Schedule verification failed: privacy={privacy!r}, publishAt={publish_at!r}")
    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "approval_ref": "APR-0002",
        "revision": "v002",
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
        "thumbnail_file": str(thumb.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": sha(thumb),
        "thumbnail_status": thumb_status,
        "youtube_meta": str(META.relative_to(ROOT)).replace("\\", "/"),
        "youtube_private_upload_result": str(UPLOAD_RESULT.relative_to(ROOT)).replace("\\", "/"),
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
        "immediate_public_publish": False,
    }
    write_json(RESULT, result)
    update_records(result, state_after)
    print(f"SCHEDULED_OK video_id={video_id}")
    print(f"SCHEDULED_LOCAL {SCHEDULED_AT_LOCAL}")
    print(f"SCHEDULED_UTC {SCHEDULED_AT_UTC}")
    print(f"STUDIO {result['studio']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
