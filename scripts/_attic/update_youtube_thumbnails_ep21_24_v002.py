#!/usr/bin/env python3
"""Replace YouTube thumbnails for already scheduled EP21-EP24."""
from __future__ import annotations

import hashlib
import json
import mimetypes
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id


REV = "v002"
RESULT_NAME = f"youtube_thumbnail_ctr_update.owner_batch.{REV}.json"

EPISODES = [
    {
        "num": 21,
        "episode_id": "PD-2026-021-dbcooper",
        "video_id": "tt7U1XgjCU4",
        "schedule": "2026-07-06T03:00:00Z",
        "thumbnail": ROOT / "episodes/PD-2026-021-dbcooper/09_package/thumbnail.selected.v002_ctr.png",
        "text": "STILL MISSING / NO TRACE",
        "safety": "Unsolved case only; no suspect named or implied.",
    },
    {
        "num": 22,
        "episode_id": "PD-2026-022-milken",
        "video_id": "mj9qEKPRatE",
        "schedule": "2026-07-07T03:00:00Z",
        "thumbnail": ROOT / "episodes/PD-2026-022-milken/09_package/thumbnail.selected.v002_ctr.png",
        "text": "GENIUS OR GREED? / 6 PLEAS",
        "safety": "Question framing; plea wording avoids conviction-at-trial, insider-trading conviction, RICO, or exoneration claims.",
    },
    {
        "num": 23,
        "episode_id": "PD-2026-023-swartz",
        "video_id": "FTm1icKgycU",
        "schedule": "2026-07-08T03:00:00Z",
        "thumbnail": ROOT / "episodes/PD-2026-023-swartz/09_package/thumbnail.selected.v002_ctr.png",
        "text": "13 FELONIES / OPEN WEB",
        "safety": "No death/self-harm wording, no single-cause claim, no 35-years wording.",
    },
    {
        "num": 24,
        "episode_id": "PD-2026-024-rajaratnam",
        "video_id": "rYV4rxtQCV0",
        "schedule": "2026-07-09T03:00:00Z",
        "thumbnail": ROOT / "episodes/PD-2026-024-rajaratnam/09_package/thumbnail.selected.v002_ctr.png",
        "text": "CAUGHT ON TAPE / WIRETAP",
        "safety": "Record-safe wiretap wording; no profit-size claim or Gupta conflation.",
    },
]

BANNED = {
    21: ["SOLVED", "WAS D.B. COOPER", "WAS DB COOPER"],
    22: ["CONVICTED AT TRIAL", "CONVICTED OF INSIDER", "RICO", "EXONERATED"],
    23: ["SUICIDE", "DEATH", "DIED", "CAUSED", "35 YEARS", "METHOD", "NOTE"],
    24: ["$7B PROFIT", "LONGEST SENTENCE", "GUPTA"],
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def append_event(epdir: Path, data: dict[str, Any]) -> None:
    events = epdir / "events" / "events.jsonl"
    events.parent.mkdir(parents=True, exist_ok=True)
    with events.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def http_json(req: urllib.request.Request, timeout: int = 90) -> dict[str, Any]:
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_video_state(token: str, video_id: str) -> dict[str, Any]:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return http_json(req, timeout=60)


def set_thumbnail(token: str, video_id: str, path: Path) -> dict[str, Any]:
    req = urllib.request.Request(
        f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
        data=path.read_bytes(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": mimetypes.guess_type(path.name)[0] or "image/png",
        },
        method="POST",
    )
    return http_json(req, timeout=180)


def validate_local_thumb(ep: dict[str, Any]) -> None:
    path = ep["thumbnail"]
    if not path.exists():
        raise RuntimeError(f"Missing thumbnail: {path}")
    with Image.open(path) as img:
        if img.size != (1280, 720):
            raise RuntimeError(f"{ep['episode_id']} thumbnail must be 1280x720, got {img.size}")
    upper = ep["text"].upper()
    for fragment in BANNED[ep["num"]]:
        if fragment in upper:
            raise RuntimeError(f"{ep['episode_id']} banned text fragment: {fragment}")


def validate_video_state(ep: dict[str, Any], state: dict[str, Any], channel_id: str) -> dict[str, Any]:
    items = state.get("items") or []
    if len(items) != 1:
        raise RuntimeError(f"{ep['episode_id']} video not found or ambiguous: {ep['video_id']}")
    item = items[0]
    snippet = item.get("snippet", {})
    status = item.get("status", {})
    if snippet.get("channelId") != channel_id:
        raise RuntimeError(f"{ep['episode_id']} channel mismatch")
    if status.get("privacyStatus") != "private":
        raise RuntimeError(f"{ep['episode_id']} is not private")
    if status.get("publishAt") != ep["schedule"]:
        raise RuntimeError(f"{ep['episode_id']} publishAt changed: {status.get('publishAt')}")
    return {
        "video_id": item.get("id"),
        "title": snippet.get("title"),
        "privacyStatus": status.get("privacyStatus"),
        "publishAt": status.get("publishAt"),
        "processingStatus": item.get("processingDetails", {}).get("processingStatus"),
        "thumbnail_keys": sorted((snippet.get("thumbnails") or {}).keys()),
    }


def update_local_records(ep: dict[str, Any], result: dict[str, Any], compact_after: dict[str, Any]) -> None:
    epdir = ROOT / "episodes" / ep["episode_id"]
    pkg = epdir / "09_package"
    thumb_path = ep["thumbnail"]
    thumb_sha = sha256(thumb_path)
    timestamp = now()

    record = {
        "schema_version": "1.0.0",
        "revision": REV,
        "episode_id": ep["episode_id"],
        "video_id": ep["video_id"],
        "watch": f"https://youtu.be/{ep['video_id']}",
        "studio": f"https://studio.youtube.com/video/{ep['video_id']}/edit",
        "thumbnail_file": rel(thumb_path),
        "thumbnail_sha256": thumb_sha,
        "thumbnail_text": ep["text"],
        "safety_note": ep["safety"],
        "updated_at": timestamp,
        "external_upload": True,
        "thumbnail_state": result,
        "youtube_state_after_compact": compact_after,
    }
    write_json(pkg / RESULT_NAME, record)

    final_delivery = pkg / "final_delivery.v001.json"
    if final_delivery.exists():
        data = load_json(final_delivery)
        data["thumbnail_selected"] = str(thumb_path).replace("\\", "/")
        data["thumbnail_selected_sha256"] = thumb_sha
        data["thumbnail_ctr_update"] = {
            "revision": REV,
            "result": rel(pkg / RESULT_NAME),
            "applied_at": timestamp,
            "youtube_video_id": ep["video_id"],
        }
        data["updated_at"] = timestamp
        write_json(final_delivery, data)

    manifest_path = epdir / "manifest.json"
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        manifest.setdefault("active_revisions", {})["thumbnail_selected"] = "v002_ctr"
        manifest.setdefault("active_revisions", {})["youtube_thumbnail_ctr_update"] = REV
        manifest["thumbnail_selected"] = rel(thumb_path)
        manifest["thumbnail_selected_sha256"] = thumb_sha
        manifest["updated_at"] = timestamp
        artifacts = manifest.setdefault("artifacts", [])
        artifact_id = f"{ep['episode_id']}-thumbnail-selected-v002-ctr"
        artifacts[:] = [a for a in artifacts if a.get("artifact_id") != artifact_id]
        artifacts.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": "thumbnail_selected",
                "revision": "v002_ctr",
                "uri": f"artifact://episodes/{ep['episode_id']}/09_package/thumbnail.selected.v002_ctr.png",
                "checksum": thumb_sha,
                "status": "selected",
                "rights_status": "clear",
                "qc_status": "pass",
            }
        )
        write_json(manifest_path, manifest)

    append_event(
        epdir,
        {
            "event": "youtube_thumbnail_replaced_ctr_v002",
            "at": timestamp,
            "episode_id": ep["episode_id"],
            "video_id": ep["video_id"],
            "thumbnail_file": rel(thumb_path),
            "thumbnail_sha256": thumb_sha,
            "safety_note": ep["safety"],
        },
    )


def main() -> None:
    for ep in EPISODES:
        validate_local_thumb(ep)

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Refusing thumbnail update for unexpected channel: {channel_id}")

    summary = []
    for ep in EPISODES:
        before = get_video_state(token, ep["video_id"])
        compact_before = validate_video_state(ep, before, channel_id)
        thumb_state = set_thumbnail(token, ep["video_id"], ep["thumbnail"])
        after = get_video_state(token, ep["video_id"])
        compact_after = validate_video_state(ep, after, channel_id)
        update_local_records(ep, thumb_state, compact_after)
        summary.append(
            {
                "episode": ep["num"],
                "episode_id": ep["episode_id"],
                "video_id": ep["video_id"],
                "watch": f"https://youtu.be/{ep['video_id']}",
                "thumbnail": rel(ep["thumbnail"]),
                "thumbnail_sha256": sha256(ep["thumbnail"]),
                "before": compact_before,
                "after": compact_after,
                "result_file": rel(ROOT / "episodes" / ep["episode_id"] / "09_package" / RESULT_NAME),
            }
        )

    print(json.dumps({"status": "OK", "updated": summary}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
