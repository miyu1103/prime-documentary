#!/usr/bin/env python3
"""Upload EP6 Terry v003 to YouTube and publish it publicly now.

Side effects in non-dry-run mode:
- refreshes the local YouTube OAuth token
- uploads the exact v003 MP4 as private first
- sets the selected thumbnail
- switches the uploaded video to public
- writes local result, package state, manifest, and event files
"""
from __future__ import annotations

import argparse
import json
import re
import sys
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
META = EPDIR / "09_package" / "youtube_meta.v003.json"
APR_ID = "APR-0008"
APR = EPDIR / "approvals" / f"{APR_ID}.json"
RIGHTS = EPDIR / "09_package" / "rights_manifest.v003.json"
FINAL_QC = EPDIR / "08_edit" / "renders" / "final.v003.qc.json"
FINAL_DELIVERY = EPDIR / "09_package" / "final_delivery.v003.json"
VIDEO = Path(r"H:\pd-media\episodes\PD-2026-006-terry\08_edit\terry_final_v003.mp4")
MANIFEST = EPDIR / "manifest.json"
RESULT = EPDIR / "09_package" / "youtube_publish_result.v003.json"
EVENTS = EPDIR / "events" / "events.jsonl"

PREVIOUS_VIDEO_ID = "dcqWIPXun7c"
EXPECTED_VIDEO = "b28f14502d8a0937e5b5b2eaaff7245cdda6ad04ef99149f8780166cfb75ca26"
EXPECTED_THUMB = "5f364026fc46758441c9673e47cdd93f96ceec265810d2267643d0d4695c45bf"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
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


def description_with_chapters(meta: dict) -> str:
    desc = meta["description"].rstrip()
    chapters = meta.get("chapters") or []
    if not chapters:
        return desc
    lines = ["", "", "Chapters:"]
    for chapter in chapters:
        lines.append(f"{chapter['time']} {chapter['title']}")
    return desc + "\n".join(lines)


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
        "description": description_with_chapters(meta),
        "tags": meta.get("tags", []),
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
    }
    status = {
        "privacyStatus": "private",
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


def set_public(token: str, video_id: str, existing_state: dict) -> dict:
    items = existing_state.get("items") or []
    existing_status = (items[0].get("status") if items else {}) or {}
    status = {
        "privacyStatus": "public",
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


def set_private(token: str, video_id: str, existing_state: dict) -> dict:
    items = existing_state.get("items") or []
    existing_status = (items[0].get("status") if items else {}) or {}
    status = {
        "privacyStatus": "private",
        "selfDeclaredMadeForKids": existing_status.get("selfDeclaredMadeForKids", False),
        "containsSyntheticMedia": existing_status.get("containsSyntheticMedia", True),
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


def update_artifact_checksum(manifest: dict, artifact_id: str, path: Path, artifact_type: str | None = None, revision: str | None = None) -> None:
    checksum = f"sha256:{sha256_file(path)}"
    if revision is None:
        revision_match = re.search(r"\.v([0-9]{3})\.", path.name)
        revision = f"v{revision_match.group(1)}" if revision_match else "v001"
    uri = f"artifact://{path.relative_to(ROOT).as_posix()}" if path.is_relative_to(ROOT) else str(path)
    for artifact in manifest.get("artifacts", []):
        if artifact.get("artifact_id") == artifact_id:
            artifact["checksum"] = checksum
            artifact["revision"] = revision
            artifact["uri"] = uri
            if artifact_type:
                artifact["artifact_type"] = artifact_type
            artifact["status"] = "approved"
            artifact["rights_status"] = "clear"
            artifact["qc_status"] = "pass"
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


def update_local_package_state(result: dict) -> None:
    meta = load_json(META)
    meta["status"] = "published"
    meta["upload_performed"] = True
    meta["publish_performed"] = True
    meta["video_id"] = result["video_id"]
    meta["video_url"] = result["watch"]
    meta["studio_url"] = result["studio"]
    meta["youtube_channel_id"] = result["channel_id"]
    meta["privacy_status"] = "public"
    meta["published_at_utc"] = result["published_at_utc"]
    meta["publish_result"] = str(RESULT.relative_to(ROOT)).replace("\\", "/")
    meta["previous_video_id_checked"] = PREVIOUS_VIDEO_ID
    meta["previous_video_action"] = result.get("previous_video_action")
    meta["approval_ids"] = sorted(set(meta.get("approval_ids", []) + [APR_ID]))
    meta.setdefault("pre_publish_checks", {})["upload_performed"] = True
    meta.setdefault("pre_publish_checks", {})["publish_performed"] = True
    meta.setdefault("pre_publish_checks", {})["publish_result"] = str(RESULT.relative_to(ROOT)).replace("\\", "/")
    write_json(META, meta)

    manifest = load_json(MANIFEST)
    manifest["state"] = "published"
    manifest["video_id"] = result["video_id"]
    manifest["video_url"] = result["watch"]
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest.setdefault("active_revisions", {})["final_build_script"] = "v003"
    manifest.setdefault("active_revisions", {})["captions_final"] = "v003"
    manifest.setdefault("active_revisions", {})["final_qc"] = "v003"
    manifest.setdefault("active_revisions", {})["final_delivery"] = "v003"
    manifest.setdefault("active_revisions", {})["rights_manifest"] = "v003"
    manifest.setdefault("active_revisions", {})["youtube_meta"] = "v003"
    manifest.setdefault("active_revisions", {})["youtube_publish_result"] = "v003"
    approvals = manifest.setdefault("approvals", [])
    if APR_ID not in approvals:
        approvals.append(APR_ID)
    warning = f"YouTube public upload completed for Terry v003 under {APR_ID}: video_id {result['video_id']}. Synthetic-content disclosure set; previous video check/action: {result.get('previous_video_action')}."
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    update_artifact_checksum(manifest, f"{EP}-approval-{APR_ID}", APR, "approval")
    update_artifact_checksum(manifest, f"{EP}-final-qc-v003", FINAL_QC, "qc_report")
    update_artifact_checksum(manifest, f"{EP}-final-delivery-v003", FINAL_DELIVERY, "final_delivery_manifest")
    update_artifact_checksum(manifest, f"{EP}-rights-manifest-v003", RIGHTS, "rights_manifest")
    update_artifact_checksum(manifest, f"{EP}-final-render-v003", VIDEO, "final_render", "v003")
    update_artifact_checksum(manifest, f"{EP}-youtube-meta-v003", META, "youtube_metadata")
    update_artifact_checksum(manifest, f"{EP}-youtube-publish-result-v003", RESULT, "youtube_publish_result")
    write_json(MANIFEST, manifest)


def verify_preconditions() -> tuple[dict, dict, Path]:
    if RESULT.exists():
        raise RuntimeError(f"Existing v003 publish result found; refusing duplicate upload: {RESULT.relative_to(ROOT)}")
    for path in [APR, META, RIGHTS, FINAL_QC, FINAL_DELIVERY]:
        if not path.exists():
            raise RuntimeError(f"Missing required file: {path}")
    apr = load_json(APR)
    if apr.get("decision") != "approved":
        raise RuntimeError(f"{APR_ID} is not approved: {apr.get('decision')!r}")
    if not VIDEO.exists():
        raise RuntimeError(f"Missing final video: {VIDEO}")
    actual_video = sha256_file(VIDEO)
    if actual_video != EXPECTED_VIDEO:
        raise RuntimeError(f"Video hash mismatch: expected {EXPECTED_VIDEO}, actual {actual_video}")
    meta = load_json(META)
    thumb = selected_thumbnail_path(meta)
    actual_thumb = sha256_file(thumb)
    if actual_thumb != EXPECTED_THUMB:
        raise RuntimeError(f"Thumbnail hash mismatch: expected {EXPECTED_THUMB}, actual {actual_thumb}")
    if meta.get("upload_performed") is not False or meta.get("publish_performed") is not False:
        raise RuntimeError("youtube_meta already marks upload/publish performed")
    qc = load_json(FINAL_QC)
    if not qc.get("synthetic_content_disclosure_required"):
        raise RuntimeError("QC does not require synthetic disclosure; expected true for symbolic AI visuals")
    return apr, meta, thumb


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
    print(f"OK exact video hash {EXPECTED_VIDEO}")
    print(f"OK exact thumbnail hash {EXPECTED_THUMB}")
    print(f"OK title: {meta['title']}")
    print("OK upload will be private first, then public; madeForKids=false; containsSyntheticMedia=true")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    print("OK access token obtained")
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel allowlisted: {channel_id}")

    previous_before = get_video_state(token, PREVIOUS_VIDEO_ID)
    previous_items = previous_before.get("items") or []
    print(f"OK previous video lookup {PREVIOUS_VIDEO_ID}: {'found' if previous_items else 'not found'}")

    upload_url = initiate_upload(token, meta, VIDEO.stat().st_size)
    print(f"OK resumable upload session started; uploading {VIDEO.stat().st_size / 1e6:.0f} MB")
    video_id = upload_chunks(upload_url, token, VIDEO)
    if not video_id:
        raise RuntimeError("Upload returned no video_id")
    print(f"OK private upload complete video_id={video_id}")

    thumbnail_status = set_thumbnail(token, video_id, thumb)
    print("OK thumbnail set")

    private_state = get_video_state(token, video_id)
    private_items = private_state.get("items") or []
    private_status = (private_items[0].get("status") if private_items else {}) or {}
    if private_status.get("privacyStatus") != "private":
        raise RuntimeError(f"Private-first verification failed: {private_status}")

    public_status = set_public(token, video_id, private_state)
    print("OK video set public")
    public_state = get_video_state(token, video_id)
    public_items = public_state.get("items") or []
    status_after = (public_items[0].get("status") if public_items else {}) or {}
    if status_after.get("privacyStatus") != "public":
        raise RuntimeError(f"Public verification failed: {status_after}")

    previous_action = "not_found_no_action"
    previous_after = None
    if previous_items and PREVIOUS_VIDEO_ID != video_id:
        prev_status = (previous_items[0].get("status") if previous_items else {}) or {}
        prev_privacy = prev_status.get("privacyStatus")
        if prev_privacy != "private":
            previous_private_status = set_private(token, PREVIOUS_VIDEO_ID, previous_before)
            previous_after = get_video_state(token, PREVIOUS_VIDEO_ID)
            previous_action = f"set_private_from_{prev_privacy}"
        else:
            previous_private_status = None
            previous_after = previous_before
            previous_action = "already_private_no_action"
    else:
        previous_private_status = None

    now = datetime.now(timezone.utc).isoformat()
    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "approval_ref": APR_ID,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "channel_id": channel_id,
        "privacy": "public",
        "published_at_utc": now,
        "video_file": str(VIDEO),
        "video_sha256": EXPECTED_VIDEO,
        "thumbnail_file": str(thumb),
        "thumbnail_sha256": EXPECTED_THUMB,
        "thumbnail_set": True,
        "thumbnail_status": thumbnail_status,
        "private_state_before_public": private_state,
        "public_status_update": public_status,
        "youtube_state_after": public_state,
        "youtube_meta": str(META),
        "madeForKids": False,
        "containsSyntheticMedia": True,
        "external_upload": True,
        "public_publish_performed": True,
        "previous_video_id_checked": PREVIOUS_VIDEO_ID,
        "previous_video_state_before": previous_before,
        "previous_video_private_status": previous_private_status,
        "previous_video_state_after": previous_after,
        "previous_video_action": previous_action
    }
    write_json(RESULT, result)
    update_local_package_state(result)
    append_event({
        "event": "youtube_public_published",
        "episode_id": EP,
        "stage": "published",
        "revision": "v003",
        "actor": "codex",
        "approval_id": APR_ID,
        "detail": f"Uploaded Terry v003 to YouTube private-first, set selected thumbnail, then published public. Previous video action: {previous_action}.",
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "previous_video_id_checked": PREVIOUS_VIDEO_ID,
        "previous_video_action": previous_action,
        "ts": now
    })
    print(f"RESULT {RESULT.relative_to(ROOT)}")
    print(f"WATCH https://youtu.be/{video_id}")
    print(f"STUDIO https://studio.youtube.com/video/{video_id}/edit")
    print("PUBLISHED public")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
