#!/usr/bin/env python3
"""Set Miranda premium replacement thumbnail to the Codex-generated flashy v005 image."""
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

EP = "PD-2026-001-miranda"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events.jsonl"
META = PKG / "youtube_meta.v004.json"
THUMB = PKG / "thumbnail.selected.v005.jpg"
SOURCE_THUMB = EPDIR / "10_thumbnail" / "thumbnail_miranda_codex_flashy.v005.source.png"
RESULT = PKG / "youtube_thumbnail_update.v005.json"

VIDEO_ID = "cQFql7tT1fE"
EXPECTED_THUMB_SHA = "e76d753f56c049a92c0ebf2b2384dd6d31d9babcad0ca6f0d517bc37b52da5d1"
EXPECTED_SOURCE_SHA = "78298d73dbdd0185cef33ae72ada3b3156c81c921603df418d2b3ea5f53ec460"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def request_json(method: str, url: str, token: str, data: bytes | None = None, headers: dict[str, str] | None = None) -> dict:
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {token}", **(headers or {})},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8") or "{}")


def get_video(token: str) -> dict:
    return request_json(
        "GET",
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={VIDEO_ID}",
        token,
    )


def set_thumbnail(token: str) -> dict:
    return request_json(
        "POST",
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={VIDEO_ID}",
        token,
        data=THUMB.read_bytes(),
        headers={"Content-Type": "image/jpeg"},
    )


def verify_local() -> tuple[str, str]:
    if not THUMB.exists():
        raise FileNotFoundError(THUMB)
    if not SOURCE_THUMB.exists():
        raise FileNotFoundError(SOURCE_THUMB)
    thumb_sha = sha256_file(THUMB)
    source_sha = sha256_file(SOURCE_THUMB)
    if thumb_sha != EXPECTED_THUMB_SHA:
        raise RuntimeError(f"Thumbnail SHA mismatch expected={EXPECTED_THUMB_SHA} actual={thumb_sha}")
    if source_sha != EXPECTED_SOURCE_SHA:
        raise RuntimeError(f"Source thumbnail SHA mismatch expected={EXPECTED_SOURCE_SHA} actual={source_sha}")
    if THUMB.stat().st_size >= 2_000_000:
        raise RuntimeError(f"Thumbnail is too large for safe YouTube upload: {THUMB.stat().st_size}")
    return thumb_sha, source_sha


def update_local_records(result: dict) -> None:
    now = datetime.now(timezone.utc).isoformat()
    meta = load_json(META)
    meta["thumbnail"] = str(THUMB)
    meta["thumbnail_source"] = str(SOURCE_THUMB)
    meta["thumbnail_revision"] = "v005"
    meta["thumbnail_sha256"] = result["thumbnail_sha256"]
    meta["thumbnail_update_result"] = str(RESULT.relative_to(ROOT)).replace("\\", "/")
    meta["updated_at"] = now
    write_json(META, meta)

    manifest = load_json(MANIFEST)
    manifest.setdefault("active_revisions", {})["thumbnail"] = "v005"
    manifest.setdefault("active_revisions", {})["youtube_thumbnail_update"] = "v005"
    manifest["updated_at"] = now
    manifest.setdefault("warnings", []).append(
        f"Miranda public upload {VIDEO_ID} thumbnail updated to Codex flashy v005 image; title text is baked into the thumbnail."
    )
    write_json(MANIFEST, manifest)

    append_event(
        {
            "event": "youtube_thumbnail_updated",
            "episode_id": EP,
            "revision": "thumbnail_v005",
            "actor": "codex",
            "video_id": VIDEO_ID,
            "thumbnail": str(THUMB),
            "thumbnail_sha256": result["thumbnail_sha256"],
            "source_thumbnail": str(SOURCE_THUMB),
            "source_thumbnail_sha256": result["source_thumbnail_sha256"],
            "youtube_result": str(RESULT.relative_to(ROOT)).replace("\\", "/"),
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

    thumb_sha, source_sha = verify_local()
    print(f"OK thumbnail sha {thumb_sha}")
    print(f"OK source sha {source_sha}")
    print(f"OK thumbnail bytes {THUMB.stat().st_size}")
    if args.dry_run:
        print("DRY_RUN_OK no external writes")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    before = get_video(token)
    items = before.get("items") or []
    if not items:
        raise RuntimeError(f"Video not found: {VIDEO_ID}")
    if items[0].get("status", {}).get("privacyStatus") != "public":
        raise RuntimeError(f"Video is not public: {items[0].get('status')}")
    youtube_result = set_thumbnail(token)
    after = get_video(token)
    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "video_id": VIDEO_ID,
        "watch_url": f"https://youtu.be/{VIDEO_ID}",
        "thumbnail": str(THUMB),
        "thumbnail_sha256": thumb_sha,
        "thumbnail_size_bytes": THUMB.stat().st_size,
        "source_thumbnail": str(SOURCE_THUMB),
        "source_thumbnail_sha256": source_sha,
        "channel_id": channel_id,
        "youtube_before": before,
        "youtube_thumbnail_result": youtube_result,
        "youtube_after": after,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "external_public_write": True,
    }
    write_json(RESULT, result)
    update_local_records(result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
