#!/usr/bin/env python3
"""Update the scheduled Mahanoy YouTube thumbnail to v002."""
from __future__ import annotations

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


EP = "PD-2026-011-mahanoy"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / "youtube_meta.v001.json"
RIGHTS = PKG / "rights_manifest.v001.json"
DELIVERY = PKG / "final_delivery.v002.json"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
THUMB = PKG / "thumbnail.selected.v002.png"
RESULT = PKG / "youtube_thumbnail_update.v002.json"
VIDEO_ID = "cSfe3iGnBBM"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(data: dict) -> None:
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def sha(path: Path) -> str:
    return "sha256:" + sha256_file(path)


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


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if RESULT.exists():
        raise RuntimeError(f"Existing update result found; refusing duplicate thumbnail update: {RESULT}")
    for path in [META, RIGHTS, DELIVERY, MANIFEST, THUMB]:
        if not path.exists():
            raise RuntimeError(f"Missing required file: {path}")

    meta = load_json(META)
    if meta.get("video_id") != VIDEO_ID or meta.get("status") != "scheduled":
        raise RuntimeError("youtube_meta is not the scheduled Mahanoy video")
    if meta.get("publish_performed") is not False:
        raise RuntimeError("Refusing thumbnail update after public publish marker")

    thumb_sha = sha(THUMB)
    env = load_env()
    token = _access_token(env)
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")

    response = set_thumbnail(token, VIDEO_ID, THUMB)
    state = get_video_state(token, VIDEO_ID)
    status = ((state.get("items") or [{}])[0].get("status") or {})
    if status.get("privacyStatus") != "private" or status.get("publishAt") != "2026-06-26T03:00:00Z":
        raise RuntimeError(f"Unexpected schedule after thumbnail update: {status}")

    now = datetime.now(timezone.utc).isoformat()
    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "video_id": VIDEO_ID,
        "watch": f"https://youtu.be/{VIDEO_ID}",
        "studio": f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        "thumbnail_file": str(THUMB.relative_to(ROOT)).replace("\\", "/"),
        "thumbnail_sha256": thumb_sha,
        "thumbnail_status": response,
        "youtube_state_after": state,
        "scheduled_at_local": "2026-06-26T12:00:00+09:00",
        "scheduled_at_utc": "2026-06-26T03:00:00Z",
        "privacy": status.get("privacyStatus"),
        "publish_at_platform": status.get("publishAt"),
        "updated_at": now,
        "external_update": True,
        "public_immediate_publish": False,
    }
    write_json(RESULT, result)

    meta["thumbnail_file"] = str(THUMB.relative_to(ROOT)).replace("\\", "/")
    meta["thumbnail_sha256"] = thumb_sha
    meta["thumbnail_revision"] = "v002"
    meta["thumbnail_update_result"] = str(RESULT.relative_to(ROOT)).replace("\\", "/")
    meta["thumbnail_updated_at"] = now
    meta["title_thumbnail_candidates"] = str((PKG / "thumbnail_candidates.v002.json").relative_to(ROOT)).replace("\\", "/")
    write_json(META, meta)

    rights = load_json(RIGHTS)
    rights["selected_thumbnail"] = str(THUMB.relative_to(ROOT)).replace("\\", "/")
    rights["thumbnail_sha256"] = thumb_sha
    rights["thumbnail_revision"] = "v002"
    write_json(RIGHTS, rights)

    delivery = load_json(DELIVERY)
    delivery["thumbnail"] = str(THUMB.relative_to(ROOT)).replace("\\", "/")
    delivery["thumbnail_sha256"] = thumb_sha
    delivery["thumbnail_revision"] = "v002"
    delivery["youtube_thumbnail_update"] = str(RESULT.relative_to(ROOT)).replace("\\", "/")
    write_json(DELIVERY, delivery)

    manifest = load_json(MANIFEST)
    manifest["updated_at"] = now
    manifest.setdefault("active_revisions", {})["thumbnail"] = "v002"
    manifest.setdefault("active_revisions", {})["youtube_thumbnail_update"] = "v002"
    warning = f"YouTube thumbnail updated to v002 for video_id {VIDEO_ID}; scheduled release remains 2026-06-26T12:00:00+09:00."
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
            "thumbnail": str(THUMB.relative_to(ROOT)).replace("\\", "/"),
            "thumbnail_sha256": thumb_sha,
            "ts": now,
        }
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
