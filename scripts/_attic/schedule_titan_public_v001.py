#!/usr/bin/env python3
"""Schedule the already-private Titan upload for public release.

This is intentionally a separate final-gate script. It refuses to schedule
unless the 2026-07-01 same-day fact re-check artifact exists and explicitly
passes, including a decision on the Rush quote-order deviation.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id


EP = "PD-2026-016-titan"
REV = "v009"
APR_ID = "APR-0004"
EPDIR = ROOT / "episodes" / EP
PKG = EPDIR / "09_package"
META = PKG / f"youtube_meta.{REV}.json"
FINAL_DELIVERY = PKG / f"final_delivery.{REV}.json"
APR = EPDIR / "approvals" / f"{APR_ID}.json"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"
FACT_RECHECK_FINAL = EPDIR / "01_research" / "fact_recheck.v003.md"
RESULT = PKG / "youtube_schedule_result.v001.json"
STATUS_VERIFY = PKG / "youtube_schedule_status_verify.v001.json"

SCHEDULED_AT_LOCAL = "2026-07-01T12:00:00+09:00"
SCHEDULED_AT_UTC = "2026-07-01T03:00:00Z"
REQUIRED_LOCAL_DATE = "2026-07-01"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


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


def final_fact_gate() -> tuple[bool, str]:
    today = datetime.now(timezone(timedelta(hours=9))).date().isoformat()
    if today != REQUIRED_LOCAL_DATE:
        return False, f"today is {today} JST, required same-day date is {REQUIRED_LOCAL_DATE}"
    if not FACT_RECHECK_FINAL.exists():
        return False, f"missing final fact re-check: {rel(FACT_RECHECK_FINAL)}"
    text = FACT_RECHECK_FINAL.read_text(encoding="utf-8")
    required = [
        "Re-check date: 2026-07-01 JST",
        "Status: PASS",
    ]
    if not all(item in text for item in required):
        return False, "final fact re-check must contain 'Re-check date: 2026-07-01 JST' and 'Status: PASS'"
    if "Rush quote deviation: accepted" not in text and "Rush quote deviation: corrected" not in text:
        return False, "final fact re-check must explicitly mark Rush quote deviation accepted or corrected"
    return True, "final same-day fact re-check gate passed"


def verify_preconditions(*, dry_run: bool, owner_override_final_fact_gate: bool) -> tuple[dict, str, str | None]:
    for path in (META, FINAL_DELIVERY, APR, MANIFEST):
        if not path.exists():
            raise RuntimeError(f"Missing required file: {path}")
    if RESULT.exists():
        raise RuntimeError(f"Schedule result already exists; refusing duplicate schedule: {rel(RESULT)}")
    apr = load_json(APR)
    if apr.get("decision") != "approved" or apr.get("target_type") != "publish" or apr.get("target_revision") != REV:
        raise RuntimeError(f"{APR_ID} does not approve publish package {REV}")
    meta = load_json(META)
    video_id = meta.get("video_id")
    if not video_id:
        raise RuntimeError("youtube_meta has no private-upload video_id")
    if meta.get("upload_performed") is not True:
        raise RuntimeError("private upload has not been recorded")
    if meta.get("schedule_performed") is not False:
        raise RuntimeError("youtube_meta already marks schedule_performed")
    if meta.get("intended_schedule_local") != SCHEDULED_AT_LOCAL or meta.get("intended_schedule_utc") != SCHEDULED_AT_UTC:
        raise RuntimeError("youtube_meta schedule target mismatch")
    ok, reason = final_fact_gate()
    if not ok and not dry_run and not owner_override_final_fact_gate:
        raise RuntimeError(f"FINAL FACT GATE BLOCKED: {reason}")
    return meta, video_id, None if ok or owner_override_final_fact_gate else reason


def update_records(video_id: str, state_after: dict, update_response: dict, *, owner_override_final_fact_gate: bool) -> None:
    now = datetime.now(timezone.utc).isoformat()
    result = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "approval_ref": APR_ID,
        "video_id": video_id,
        "watch": f"https://youtu.be/{video_id}",
        "studio": f"https://studio.youtube.com/video/{video_id}/edit",
        "privacy": "private",
        "scheduled_at_local": SCHEDULED_AT_LOCAL,
        "scheduled_at_utc": SCHEDULED_AT_UTC,
        "publish_at_platform": ((state_after.get("items") or [{}])[0].get("status") or {}).get("publishAt"),
        "update_response": update_response,
        "youtube_state_after": state_after,
        "scheduled_at": now,
        "public_schedule_set": True,
        "public_immediate_publish": False,
        "owner_override_final_fact_gate": owner_override_final_fact_gate,
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
            "schedule_result": rel(RESULT),
            "schedule_status_verify": rel(STATUS_VERIFY),
            "owner_override_final_fact_gate": owner_override_final_fact_gate,
            "updated_at": now,
        }
    )
    meta["requested_schedule"]["status"] = "scheduled"
    write_json(META, meta)

    delivery = load_json(FINAL_DELIVERY)
    delivery.update(
        {
            "status": "scheduled",
            "schedule_performed": True,
            "publish_performed": False,
            "youtube": {
                **delivery.get("youtube", {}),
                "video_id": video_id,
                "watch": result["watch"],
                "studio": result["studio"],
                "privacy": "private",
                "scheduled_at_local": SCHEDULED_AT_LOCAL,
                "scheduled_at_utc": SCHEDULED_AT_UTC,
                "schedule_performed": True,
                "public_immediate_publish": False,
                "schedule_result": rel(RESULT),
                "owner_override_final_fact_gate": owner_override_final_fact_gate,
            },
            "updated_at": now,
        }
    )
    delivery["requested_schedule"]["status"] = "scheduled"
    write_json(FINAL_DELIVERY, delivery)

    manifest = load_json(MANIFEST)
    manifest["state"] = "scheduled"
    manifest["video_id"] = video_id
    manifest["video_url"] = result["watch"]
    manifest["updated_at"] = now
    manifest.setdefault("active_revisions", {}).update({"youtube_schedule_result": "v001", "youtube_schedule_status_verify": "v001"})
    manifest["blockers"] = []
    approvals = manifest.setdefault("approvals", [])
    if APR_ID not in approvals:
        approvals.append(APR_ID)
    write_json(MANIFEST, manifest)

    append_event(
        {
            "ts": now,
            "episode_id": EP,
            "stage": "youtube_schedule",
            "event": "youtube_public_schedule_set",
            "revision": REV,
            "actor": "codex",
            "approval_id": APR_ID,
            "video_id": video_id,
            "watch": result["watch"],
            "studio": result["studio"],
            "scheduled_at_local": SCHEDULED_AT_LOCAL,
            "scheduled_at_utc": SCHEDULED_AT_UTC,
            "owner_override_final_fact_gate": owner_override_final_fact_gate,
            "note": "Existing private upload scheduled for public release. No immediate public publish performed. Owner explicitly overrode same-day final fact gate before scheduling." if owner_override_final_fact_gate else "Existing private upload scheduled for public release. No immediate public publish performed.",
        }
    )


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--owner-override-final-fact-gate", action="store_true")
    args = parser.parse_args(argv)

    meta, video_id, blocked_reason = verify_preconditions(dry_run=args.dry_run, owner_override_final_fact_gate=args.owner_override_final_fact_gate)
    print(f"OK {APR_ID} publish approval found")
    print(f"OK video_id={video_id}")
    print(f"OK intended schedule local={SCHEDULED_AT_LOCAL} utc={SCHEDULED_AT_UTC}")
    if blocked_reason:
        print(f"DRY_RUN_BLOCKED final fact gate: {blocked_reason}")
        return 0
    if args.dry_run:
        print("DRY_RUN_OK final gate would allow scheduling; no external writes performed")
        return 0

    token = _access_token(load_env())
    channel_id = get_channel_id(token)
    if channel_id not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"Channel {channel_id!r} not allowlisted: {CHANNEL_ALLOWLIST}")
    state_before = get_video_state(token, video_id)
    update_response = update_schedule(token, video_id, state_before)
    state_after = get_video_state(token, video_id)
    status = ((state_after.get("items") or [{}])[0].get("status") or {})
    if status.get("privacyStatus") != "private" or status.get("publishAt") != SCHEDULED_AT_UTC:
        raise RuntimeError(f"Schedule verification failed: {status}")
    update_records(video_id, state_after, update_response, owner_override_final_fact_gate=args.owner_override_final_fact_gate)
    print(f"SCHEDULED {video_id} {SCHEDULED_AT_LOCAL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
