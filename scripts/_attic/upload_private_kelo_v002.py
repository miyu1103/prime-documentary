#!/usr/bin/env python3
"""Upload Kelo v002 to YouTube as private only.

No public publish and no publishAt scheduling are performed by this script.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import upload_private_kelo_v001 as base
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, upload_chunks


EP = "PD-2026-010-kelo"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / "youtube_meta.v002.json"
RIGHTS = PKG / "rights_manifest.v002.json"
PREFLIGHT = PKG / "publish_preflight.v002.json"
FINAL_DELIVERY = PKG / "final_delivery.v002.json"
FINAL_QC = EPDIR / "08_edit" / "renders" / "final.v002.qc.json"
CAPTION_FILE = EPDIR / "08_edit" / "captions.v002.srt"
MANIFEST = EPDIR / "manifest.json"
RESULT = PKG / "youtube_private_upload_result.v002.json"
CAPTION_RESULT = PKG / "youtube_captions_result.v002.json"
STATUS_VERIFY = PKG / "youtube_status_verify.v002.json"

base.META = META
base.RIGHTS = RIGHTS
base.PREFLIGHT = PREFLIGHT
base.FINAL_DELIVERY = FINAL_DELIVERY
base.FINAL_QC = FINAL_QC
base.CAPTION_FILE = CAPTION_FILE
base.RESULT = RESULT
base.CAPTION_RESULT = CAPTION_RESULT
base.STATUS_VERIFY = STATUS_VERIFY


def verify_preconditions() -> tuple[dict, Path, Path]:
    existing = sorted(PKG.glob("youtube_private_upload_result.v002.json")) + sorted(PKG.glob("youtube_schedule_result.v002.json"))
    if existing:
        raise RuntimeError("Existing v002 YouTube result found; refusing duplicate upload: " + ", ".join(str(p.relative_to(ROOT)) for p in existing))
    for path in [META, RIGHTS, PREFLIGHT, FINAL_DELIVERY, FINAL_QC, CAPTION_FILE]:
        if not path.exists():
            raise RuntimeError(f"Missing required artifact: {path}")
    meta = base.load_json(META)
    rights = base.load_json(RIGHTS)
    preflight = base.load_json(PREFLIGHT)
    qc = base.load_json(FINAL_QC)
    video = base.video_path(meta)
    thumb = base.selected_thumbnail_path(meta)
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
    if rights.get("status") != "clear":
        raise RuntimeError(f"rights status is not clear: {rights.get('status')!r}")
    if preflight.get("status") != "PASS" or any(checks.get(k) is not True for k in required_true) or any(checks.get(k) is not False for k in required_false):
        raise RuntimeError(f"preflight failed: {preflight}")
    if qc.get("status") != "PASS":
        raise RuntimeError("final QC is not PASS")
    if meta.get("privacy_status_target") != "private":
        raise RuntimeError("youtube_meta target is not private")
    if meta.get("publish_performed") is not False or meta.get("schedule_performed") is not False:
        raise RuntimeError("youtube_meta must keep publish/schedule false")
    if meta.get("video_sha256") != base.sha(video):
        raise RuntimeError(f"video hash mismatch: meta={meta.get('video_sha256')} actual={base.sha(video)}")
    if meta.get("selected_thumbnail_sha256") != base.sha(thumb):
        raise RuntimeError("thumbnail hash mismatch")
    return meta, video, thumb


def update_records(meta: dict, result: dict, caption: dict | None, state: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    compact = base.compact_state(state)
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
            "processing_status": compact.get("processingStatus"),
            "processing_status_verified_at": now,
            "public_schedule_active": False,
            "publish_gate": "closed",
            "updated_at": now,
        }
    )
    base.write_json(META, meta)

    manifest = base.load_json(MANIFEST)
    manifest["state"] = "package_ready"
    manifest["video_id"] = result["video_id"]
    manifest["video_url"] = result["watch"]
    manifest["updated_at"] = now
    manifest.setdefault("active_revisions", {}).update(
        {
            "youtube_meta": "v002",
            "youtube_private_upload_result": "v002",
            "youtube_captions_result": "v002" if caption else None,
            "youtube_status_verify": "v002",
            "final_delivery": "v002",
            "final_qc": "v002",
            "rights_manifest": "v002",
            "captions_final": "v002",
            "thumbnail_candidates": "v002",
        }
    )
    warning = f"YouTube private upload completed for Kelo v002: video_id {result['video_id']}. Public publish/schedule not performed; owner approval still required for 2026-06-25T12:00:00+09:00."
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    base.write_json(MANIFEST, manifest)
    base.append_event(
        {
            "event": "youtube_private_upload_completed",
            "episode_id": EP,
            "stage": "private_uploaded",
            "revision": "v002",
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
    parser.add_argument("--video-id", default=None)
    args = parser.parse_args(argv)
    meta, video, thumb = verify_preconditions()
    print(f"OK private preflight v002: {meta['title']}")
    print(f"OK video {video.stat().st_size / 1e6:.0f} MB {base.sha(video)}")
    print(f"OK thumbnail {base.sha(thumb)}")
    if args.dry_run:
        print("DRY_RUN_OK no external writes")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted")
    video_id = args.video_id or upload_chunks(base.initiate_upload(token, meta, video), token, video)
    if not video_id:
        raise RuntimeError("Upload returned no video_id")
    thumb_status = base.set_thumbnail(token, video_id, thumb)
    caption = None
    caption_error = None
    try:
        caption = base.upload_caption(token, video_id)
        base.write_json(CAPTION_RESULT, caption)
    except Exception as exc:
        caption_error = str(exc)
    state = base.get_video_state(token, video_id)
    base.write_json(STATUS_VERIFY, state)
    compact = base.compact_state(state)
    if compact.get("privacyStatus") != "private" or compact.get("publishAt"):
        raise RuntimeError(f"privacy verification failed: {compact}")
    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v002",
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": compact.get("privacyStatus"),
        "publishAt": compact.get("publishAt"),
        "video_file": str(video),
        "video_sha256": base.sha(video),
        "thumbnail_file": str(thumb.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": base.sha(thumb),
        "thumbnail_set": True,
        "thumbnail_status": thumb_status,
        "captions_uploaded": caption is not None,
        "caption_error": caption_error,
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "publish_performed": False,
        "schedule_performed": False,
        "planned_public_release_at_jst": "2026-06-25T12:00:00+09:00",
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "youtube_state_compact": compact,
    }
    base.write_json(RESULT, result)
    update_records(meta, result, caption, state)
    print(f"PRIVATE_UPLOAD_OK video_id={video_id}")
    print(f"STUDIO {result['studio']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
