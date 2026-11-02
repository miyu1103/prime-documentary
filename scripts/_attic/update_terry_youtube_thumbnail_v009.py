#!/usr/bin/env python3
"""Replace only the EP6 Terry YouTube thumbnail with option 09.

Side effects in non-dry-run mode:
- refreshes local YouTube OAuth token
- verifies the authenticated channel is allowlisted
- sends the selected thumbnail to the existing YouTube video
- writes local result JSON and updates local metadata references
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id

EP = "PD-2026-006-terry"
EPDIR = ROOT / "episodes" / EP
META = EPDIR / "09_package" / "youtube_meta.v001.json"
RESULT = EPDIR / "09_package" / "youtube_thumbnail_update.v003.json"
THUMB = EPDIR / "10_thumbnail" / "thumbnail_option_09_codex_beauty.v001.png"
THUMB_REPORT = EPDIR / "10_thumbnail" / "thumbnail_option_09_codex_beauty.v001.json"
OPTIONS = EPDIR / "10_thumbnail" / "thumbnail_options.v001.json"
APR_ID = "APR-0006"
APR = EPDIR / "approvals" / f"{APR_ID}.json"
EVENTS = EPDIR / "events" / "events.jsonl"

VIDEO_ID = "dcqWIPXun7c"
EXPECTED_SHA256 = "5f364026fc46758441c9673e47cdd93f96ceec265810d2267643d0d4695c45bf"
MAX_THUMBNAIL_BYTES = 2 * 1024 * 1024


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise RuntimeError(f"Thumbnail is not a valid PNG: {path}")
    return struct.unpack(">II", header[16:24])


def append_event(data: dict) -> None:
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


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
    return req_json(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={VIDEO_ID}",
        token,
        method="POST",
        data=THUMB.read_bytes(),
        content_type="image/png",
    )


def verify_preconditions() -> dict:
    if not APR.exists():
        raise RuntimeError(f"Missing approval: {APR}")
    apr = load_json(APR)
    if apr.get("decision") != "approved":
        raise RuntimeError(f"{APR_ID} is not approved: {apr.get('decision')!r}")
    if not META.exists():
        raise RuntimeError(f"Missing YouTube metadata: {META}")
    meta = load_json(META)
    video_id = meta.get("video_id") or meta.get("youtube_video_id")
    if video_id != VIDEO_ID:
        raise RuntimeError(f"Unexpected video id in meta: {video_id!r}")
    if not THUMB.exists():
        raise RuntimeError(f"Missing thumbnail: {THUMB}")
    actual_sha = sha256_file(THUMB)
    if actual_sha != EXPECTED_SHA256:
        raise RuntimeError(f"Thumbnail hash mismatch: expected {EXPECTED_SHA256}, actual {actual_sha}")
    size = THUMB.stat().st_size
    if size > MAX_THUMBNAIL_BYTES:
        raise RuntimeError(f"Thumbnail is too large for YouTube: {size} bytes")
    dimensions = png_size(THUMB)
    if dimensions != (1280, 720):
        raise RuntimeError(f"Thumbnail dimensions must be 1280x720, got {dimensions}")
    return meta


def update_local_metadata(result: dict) -> None:
    rel_thumb = str(THUMB.relative_to(ROOT)).replace("\\", "/")
    rel_result = str(RESULT.relative_to(ROOT)).replace("\\", "/")

    meta = load_json(META)
    meta["thumbnail"] = rel_thumb
    meta["selected_thumbnail"] = rel_thumb
    meta["selected_thumbnail_sha256"] = f"sha256:{EXPECTED_SHA256}"
    meta["thumbnail_set"] = True
    meta["thumbnail_update_result"] = rel_result
    meta["approval_ids"] = sorted(set(meta.get("approval_ids", []) + [APR_ID]))
    meta.setdefault("pre_publish_checks", {})["selected_thumbnail"] = rel_thumb
    meta.setdefault("pre_publish_checks", {})["selected_thumbnail_sha256"] = f"sha256:{EXPECTED_SHA256}"
    meta.setdefault("pre_publish_checks", {})["thumbnail_update_result"] = rel_result
    write_json(META, meta)

    if OPTIONS.exists():
        options = load_json(OPTIONS)
        options["status"] = "thumbnail_selected_and_youtube_updated"
        options["selected"] = THUMB.name
        options["selection_reason"] = "Owner requested a more beautiful Codex-made thumbnail. Option 09 keeps the cinematic Codex key-art background but improves mobile readability with a cleaner STOPPED? / NO WARRANT hierarchy."
        existing = {item.get("file"): item for item in options.get("options", [])}
        rel_file = rel_thumb
        existing[rel_file] = {
            "id": "thumb09",
            "file": rel_file,
            "headline": "STOPPED?",
            "kicker": "NO WARRANT",
            "sha256": EXPECTED_SHA256,
            "assessment": "Selected replacement. Cleaner, more premium, and more readable at mobile size than option 08 while preserving the Terry-specific legal tension.",
            "dimensions": "1280x720",
        }
        ordered = [item for item in options.get("options", []) if item.get("file") != rel_file]
        ordered.append(existing[rel_file])
        options["options"] = ordered
        options["recommended_shortlist"] = [THUMB.name, "thumbnail_option_08.v001.png", "thumbnail_option_07.v001.png"]
        options["youtube_thumbnail_update"] = rel_result
        write_json(OPTIONS, options)

    append_event({
        "event": "youtube_thumbnail_updated",
        "episode_id": EP,
        "stage": "scheduled",
        "revision": "v001",
        "actor": "codex",
        "approval_id": APR_ID,
        "detail": "Replaced the existing scheduled YouTube video's thumbnail with Codex-composed option 09. Video file, metadata, privacy, and schedule were not changed.",
        "video_id": VIDEO_ID,
        "watch": f"https://youtu.be/{VIDEO_ID}",
        "studio": f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        "thumbnail": rel_thumb,
        "thumbnail_sha256": EXPECTED_SHA256,
        "result": rel_result,
        "ts": datetime.now(timezone.utc).isoformat(),
    })


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    meta = verify_preconditions()
    print(f"OK {APR_ID} approved")
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
    thumb_response = set_thumbnail(token)
    state_after = get_video_state(token)
    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "approval_ref": APR_ID,
        "video_id": VIDEO_ID,
        "watch": f"https://youtu.be/{VIDEO_ID}",
        "studio": f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        "channel_id": channel_id,
        "thumbnail": str(THUMB.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": EXPECTED_SHA256,
        "thumbnail_size_bytes": THUMB.stat().st_size,
        "thumbnail_report": str(THUMB_REPORT.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_response": thumb_response,
        "youtube_state_before": state_before,
        "youtube_state_after": state_after,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "external_upload": False,
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
