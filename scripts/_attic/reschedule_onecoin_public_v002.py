#!/usr/bin/env python3
"""Reschedule the already-uploaded OneCoin video to 2026-07-03 12:00 JST."""
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


EP = "PD-2026-017-onecoin"
PREV_REV = "v012"
REV = "v013"
APR_ID = "APR-0005"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
APPROVALS = EPDIR / "approvals"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"

PREV_META = PKG / f"youtube_meta.{PREV_REV}.json"
PREV_DELIVERY = PKG / f"final_delivery.{PREV_REV}.json"
META = PKG / f"youtube_meta.{REV}.json"
DELIVERY = PKG / f"final_delivery.{REV}.json"
PREV_RESULT = PKG / "youtube_schedule_result.v001.json"
RESULT = PKG / "youtube_schedule_update.v002.json"
STATUS_VERIFY = PKG / "youtube_status_verify.v003.json"
APR = APPROVALS / f"{APR_ID}.json"

SCHEDULED_AT_LOCAL = "2026-07-03T12:00:00+09:00"
SCHEDULED_AT_UTC = "2026-07-03T03:00:00Z"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path).replace("\\", "/")


def sha(path: Path) -> str:
    return "sha256:" + sha256_file(path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / value


def append_event(data: dict) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def get_video_state(token: str, video_id: str) -> dict:
    req = urllib.request.Request(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails&id={video_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def update_schedule(token: str, video_id: str, status_before: dict) -> dict:
    existing_status = ((status_before.get("items") or [{}])[0].get("status") or {}).copy()
    status = {
        "privacyStatus": "private",
        "publishAt": SCHEDULED_AT_UTC,
        "selfDeclaredMadeForKids": False,
        "madeForKids": False,
        "license": existing_status.get("license", "youtube"),
        "embeddable": existing_status.get("embeddable", True),
        "publicStatsViewable": existing_status.get("publicStatsViewable", True),
        "containsSyntheticMedia": True,
    }
    body = json.dumps({"id": video_id, "status": status}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"},
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def prepare_revision(video_id: str) -> tuple[dict, dict]:
    created = now()
    meta = load_json(PREV_META)
    delivery = load_json(PREV_DELIVERY)
    video = resolve_path(meta["video_actual_path"])
    thumb = resolve_path(meta["thumbnail"])
    captions = resolve_path(meta["captions_sidecar"])
    for path in (video, thumb, captions):
        if not path.exists():
            raise RuntimeError(f"Missing artifact: {path}")
    if sha(video) != meta["video_sha256"]:
        raise RuntimeError("video hash mismatch")
    if sha(thumb) != meta["thumbnail_sha256"]:
        raise RuntimeError("thumbnail hash mismatch")
    if RESULT.exists():
        raise RuntimeError(f"Schedule update result already exists: {rel(RESULT)}")

    meta.update(
        {
            "revision": REV,
            "status": "approved_for_reschedule",
            "publish_schedule_target_jst": SCHEDULED_AT_LOCAL,
            "publish_schedule_target_utc": SCHEDULED_AT_UTC,
            "intended_schedule_local": SCHEDULED_AT_LOCAL,
            "intended_schedule_utc": SCHEDULED_AT_UTC,
            "requested_schedule": {
                "local_time": SCHEDULED_AT_LOCAL,
                "utc_time": SCHEDULED_AT_UTC,
                "status": "approved_pending_reschedule",
                "reason": "owner_approved_reschedule_to_2026-07-03_1200_jst",
            },
            "rescheduled_from": {
                "revision": PREV_REV,
                "local_time": "2026-07-02T12:00:00+09:00",
                "utc_time": "2026-07-02T03:00:00Z",
            },
            "video_id": video_id,
            "video_url": f"https://youtu.be/{video_id}",
            "studio_url": f"https://studio.youtube.com/video/{video_id}/edit",
            "schedule_performed": False,
            "publish_performed": False,
            "updated_at": created,
        }
    )
    write_json(META, meta)

    delivery.update(
        {
            "revision": REV,
            "status": "approved_for_reschedule",
            "requested_schedule": {"local_time": SCHEDULED_AT_LOCAL, "utc_time": SCHEDULED_AT_UTC, "status": "approved_pending_reschedule"},
            "video_id": video_id,
            "watch": f"https://youtu.be/{video_id}",
            "studio": f"https://studio.youtube.com/video/{video_id}/edit",
            "youtube_meta": rel(META),
            "youtube_meta_sha256": sha(META),
            "rescheduled_from": {"revision": PREV_REV, "local_time": "2026-07-02T12:00:00+09:00", "utc_time": "2026-07-02T03:00:00Z"},
            "external_side_effects": {"upload": False, "publish": False, "schedule_update": False, "paid_api": False},
            "updated_at": created,
        }
    )
    write_json(DELIVERY, delivery)

    approval = {
        "schema_version": "1.0.0",
        "approval_id": APR_ID,
        "episode_id": EP,
        "target_type": "reschedule_public_release",
        "target_revision": REV,
        "decision": "approved",
        "requested_by": "owner",
        "approved_by": "owner",
        "actor": "codex",
        "decision_source": "Owner message on 2026-06-30 JST: 7/3.12:00で予約投稿して。サムネイルは派手に。全て承認する。",
        "decided_at": "2026-06-30T00:00:00+09:00",
        "video_id": video_id,
        "video": meta["video_actual_path"],
        "video_sha256": meta["video_sha256"],
        "thumbnail": meta["thumbnail"],
        "thumbnail_sha256": meta["thumbnail_sha256"],
        "youtube_meta": rel(META),
        "youtube_meta_sha256": sha(META),
        "final_delivery": rel(DELIVERY),
        "final_delivery_sha256": sha(DELIVERY),
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "scope": [
            "Reschedule existing private YouTube upload to 2026-07-03T12:00:00+09:00.",
            "Keep the already-set flashy thumbnail.",
            "Do not re-upload the video.",
            "Do not immediate-public publish.",
        ],
    }
    write_json(APR, approval)
    return meta, delivery


def update_records(video_id: str, state_after: dict, update_response: dict) -> None:
    updated = now()
    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "approval_id": APR_ID,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "privacy": "private",
        "rescheduled_from_local": "2026-07-02T12:00:00+09:00",
        "rescheduled_from_utc": "2026-07-02T03:00:00Z",
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "publish_at_platform": ((state_after.get("items") or [{}])[0].get("status") or {}).get("publishAt"),
        "thumbnail_kept": True,
        "public_schedule_set": True,
        "public_immediate_publish": False,
        "external_upload": False,
        "update_response": update_response,
        "youtube_state_after": state_after,
        "updated_at": updated,
    }
    write_json(RESULT, result)
    write_json(STATUS_VERIFY, state_after)

    meta = load_json(META)
    meta.update(
        {
            "status": "scheduled",
            "schedule_performed": True,
            "publish_performed": False,
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "publish_at_platform": result["publish_at_platform"],
            "schedule_update_result": rel(RESULT),
            "status_verify": rel(STATUS_VERIFY),
            "updated_at": updated,
        }
    )
    meta["requested_schedule"]["status"] = "scheduled"
    write_json(META, meta)

    delivery = load_json(DELIVERY)
    delivery.update(
        {
            "status": "scheduled",
            "schedule_performed": True,
            "publish_performed": False,
            "youtube": {
                "video_id": video_id,
                "watch": result["watch"],
                "studio": result["studio"],
                "privacy": "private",
                "scheduled_at_local": SCHEDULED_AT_LOCAL,
                "scheduled_at_utc": SCHEDULED_AT_UTC,
                "schedule_update_result": rel(RESULT),
                "public_immediate_publish": False,
            },
            "external_side_effects": {"upload": False, "publish": False, "schedule_update": True, "paid_api": False},
            "updated_at": updated,
        }
    )
    delivery["requested_schedule"]["status"] = "scheduled"
    write_json(DELIVERY, delivery)

    manifest = load_json(MANIFEST)
    manifest["state"] = "scheduled"
    manifest["video_id"] = video_id
    manifest["video_url"] = result["watch"]
    manifest["public_schedule_active"] = True
    manifest["updated_at"] = updated
    manifest.setdefault("active_revisions", {}).update(
        {
            "youtube_meta": REV,
            "final_delivery": REV,
            "owner_approval": APR_ID,
            "youtube_schedule_update": "v002",
            "youtube_status_verify": "v003",
        }
    )
    approvals = manifest.setdefault("approvals", [])
    if APR_ID not in approvals:
        approvals.append(APR_ID)
    write_json(MANIFEST, manifest)

    append_event(
        {
            "ts": updated,
            "episode_id": EP,
            "stage": "youtube_schedule",
            "event": "youtube_public_schedule_updated",
            "revision": REV,
            "actor": "codex",
            "approval_id": APR_ID,
            "video_id": video_id,
            "watch": result["watch"],
            "studio": result["studio"],
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "thumbnail_kept": True,
            "public_immediate_publish": False,
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

    if not PREV_RESULT.exists():
        raise RuntimeError(f"Missing previous schedule result: {rel(PREV_RESULT)}")
    prev = load_json(PREV_RESULT)
    video_id = prev.get("video_id")
    if not video_id:
        raise RuntimeError("Previous schedule result has no video_id")
    prepare_revision(video_id)
    print(f"OK approval {APR_ID} prepared for {video_id}")
    print(f"OK target schedule local={SCHEDULED_AT_LOCAL} utc={SCHEDULED_AT_UTC}")
    print("OK same flashy thumbnail retained")
    if args.dry_run:
        print("DRY_RUN_OK no external writes performed")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    state_before = get_video_state(token, video_id)
    before_status = ((state_before.get("items") or [{}])[0].get("status") or {})
    if before_status.get("privacyStatus") != "private":
        raise RuntimeError(f"Refusing to reschedule non-private video: {before_status}")
    update_response = update_schedule(token, video_id, state_before)
    state_after = get_video_state(token, video_id)
    status = ((state_after.get("items") or [{}])[0].get("status") or {})
    if status.get("privacyStatus") != "private" or status.get("publishAt") != SCHEDULED_AT_UTC:
        raise RuntimeError(f"Schedule verification failed: {status}")
    update_records(video_id, state_after, update_response)
    print(f"RESCHEDULED {video_id} {SCHEDULED_AT_LOCAL}")
    print(f"WATCH https://youtu.be/{video_id}")
    print(f"STUDIO https://studio.youtube.com/video/{video_id}/edit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
