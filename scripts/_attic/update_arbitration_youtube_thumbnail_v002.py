#!/usr/bin/env python3
"""Replace only the scheduled Arbitration YouTube thumbnail with v002."""
from __future__ import annotations

import argparse
import json
import mimetypes
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


EP = "PD-2026-012-arbitration"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / "youtube_meta.v001.json"
RIGHTS = PKG / "rights_manifest.v001.json"
DELIVERY = PKG / "final_delivery.v001.json"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
THUMB = PKG / "thumbnail.selected.v002.png"
THUMB_META = PKG / "thumbnail_candidates.v002.json"
RESULT = PKG / "youtube_thumbnail_update.v002.json"
VIDEO_ID = "1pox44KsaV8"
EXPECTED_SHA256 = "7d5825ec6606ee1091192d6f7e563497396e727534a56af68e720316f569756c"
SCHEDULED_AT_UTC = "2026-06-27T03:00:00Z"
SCHEDULED_AT_LOCAL = "2026-06-27T12:00:00+09:00"
MAX_THUMBNAIL_BYTES = 2 * 1024 * 1024


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def sha(path: Path) -> str:
    return "sha256:" + sha256_file(path)


def req_json(url: str, token: str, *, method: str = "GET", data: bytes | None = None, content_type: str | None = None) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_video_state(token: str) -> dict:
    return req_json(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={VIDEO_ID}",
        token,
    )


def set_thumbnail(token: str) -> dict:
    content_type = mimetypes.guess_type(THUMB.name)[0] or "image/png"
    return req_json(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={VIDEO_ID}",
        token,
        method="POST",
        data=THUMB.read_bytes(),
        content_type=content_type,
    )


def verify_preconditions() -> dict:
    if RESULT.exists():
        raise RuntimeError(f"Existing update result found; refusing duplicate thumbnail update: {RESULT.relative_to(ROOT)}")
    for path in [META, RIGHTS, DELIVERY, MANIFEST, THUMB, THUMB_META]:
        if not path.exists():
            raise RuntimeError(f"Missing required file: {path}")
    actual = sha256_file(THUMB)
    if actual != EXPECTED_SHA256:
        raise RuntimeError(f"Thumbnail hash mismatch: expected {EXPECTED_SHA256}, actual {actual}")
    if THUMB.stat().st_size > MAX_THUMBNAIL_BYTES:
        raise RuntimeError(f"Thumbnail is too large for YouTube: {THUMB.stat().st_size} bytes")
    meta = load_json(META)
    if meta.get("video_id") != VIDEO_ID or meta.get("status") != "scheduled":
        raise RuntimeError("youtube_meta is not the scheduled Arbitration video")
    if meta.get("publish_performed") is not False or meta.get("schedule_performed") is not True:
        raise RuntimeError("Refusing thumbnail update: publication markers are not in scheduled/private state")
    return meta


def update_local_metadata(result: dict) -> None:
    now = result["updated_at"]
    rel_thumb = str(THUMB.relative_to(ROOT)).replace("\\", "/")
    rel_thumb_meta = str(THUMB_META.relative_to(ROOT)).replace("\\", "/")
    rel_result = str(RESULT.relative_to(ROOT)).replace("\\", "/")

    meta = load_json(META)
    meta["thumbnail_file"] = rel_thumb
    meta["thumbnail_sha256"] = f"sha256:{EXPECTED_SHA256}"
    meta["thumbnail_revision"] = "v002"
    meta["thumbnail_candidates"] = rel_thumb_meta
    meta["thumbnail_update_result"] = rel_result
    meta["thumbnail_updated_at"] = now
    write_json(META, meta)

    rights = load_json(RIGHTS)
    rights["selected_thumbnail"] = rel_thumb
    rights["thumbnail_sha256"] = f"sha256:{EXPECTED_SHA256}"
    rights["thumbnail_revision"] = "v002"
    rights["thumbnail_candidates"] = rel_thumb_meta
    write_json(RIGHTS, rights)

    delivery = load_json(DELIVERY)
    delivery["thumbnail"]["selected_thumbnail"] = rel_thumb
    delivery["thumbnail"]["selected_thumbnail_sha256"] = f"sha256:{EXPECTED_SHA256}"
    delivery["thumbnail"]["revision"] = "v002"
    delivery["thumbnail"]["update_reason"] = "Owner rejected v001 thumbnail; replaced with bolder, higher-CTR v002."
    delivery["youtube"]["thumbnail_update"] = rel_result
    write_json(DELIVERY, delivery)

    manifest = load_json(MANIFEST)
    manifest["updated_at"] = now
    manifest.setdefault("active_revisions", {})["thumbnail"] = "v002"
    manifest.setdefault("active_revisions", {})["thumbnail_candidates"] = "v002"
    manifest.setdefault("active_revisions", {})["youtube_thumbnail_update"] = "v002"
    warning = f"YouTube thumbnail updated to v002 for video_id {VIDEO_ID}; scheduled release remains {SCHEDULED_AT_LOCAL}."
    if warning not in manifest.setdefault("warnings", []):
        manifest["warnings"].append(warning)
    write_json(MANIFEST, manifest)

    append_event(
        {
            "event": "youtube_thumbnail_updated",
            "episode_id": EP,
            "stage": "scheduled",
            "revision": "v002",
            "actor": "codex",
            "detail": warning,
            "video_id": VIDEO_ID,
            "watch": f"https://youtu.be/{VIDEO_ID}",
            "studio": f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
            "thumbnail": rel_thumb,
            "thumbnail_sha256": f"sha256:{EXPECTED_SHA256}",
            "result": rel_result,
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

    meta = verify_preconditions()
    print(f"OK video_id {VIDEO_ID}")
    print(f"OK existing schedule local={meta.get('scheduled_at_local')} utc={meta.get('scheduled_at_utc')}")
    print(f"OK thumbnail {THUMB.relative_to(ROOT)} sha256={EXPECTED_SHA256} size={THUMB.stat().st_size}")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    print(f"OK channel allowlisted: {channel_id}")

    state_before = get_video_state(token)
    status_before = ((state_before.get("items") or [{}])[0].get("status") or {})
    if status_before.get("privacyStatus") != "private" or status_before.get("publishAt") != SCHEDULED_AT_UTC:
        raise RuntimeError(f"Unexpected schedule before thumbnail update: {status_before}")

    thumb_response = set_thumbnail(token)
    state_after = get_video_state(token)
    status_after = ((state_after.get("items") or [{}])[0].get("status") or {})
    if status_after.get("privacyStatus") != "private" or status_after.get("publishAt") != SCHEDULED_AT_UTC:
        raise RuntimeError(f"Unexpected schedule after thumbnail update: {status_after}")

    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "video_id": VIDEO_ID,
        "watch": f"https://youtu.be/{VIDEO_ID}",
        "studio": f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        "channel_id": channel_id,
        "thumbnail": str(THUMB.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": f"sha256:{EXPECTED_SHA256}",
        "thumbnail_size_bytes": THUMB.stat().st_size,
        "thumbnail_candidates": str(THUMB_META.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_response": thumb_response,
        "youtube_state_before": state_before,
        "youtube_state_after": state_after,
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "privacy": status_after.get("privacyStatus"),
        "publish_at_platform": status_after.get("publishAt"),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "external_update": True,
        "thumbnail_only_update": True,
        "schedule_unchanged": True,
        "metadata_unchanged_except_thumbnail": True,
    }
    write_json(RESULT, result)
    update_local_metadata(result)
    print(f"UPDATED_THUMBNAIL_OK result={RESULT.relative_to(ROOT)}")
    print(f"STUDIO https://studio.youtube.com/video/{VIDEO_ID}/edit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
