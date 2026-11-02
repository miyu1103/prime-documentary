#!/usr/bin/env python3
"""Prepare APR files for PD-2026-014/015 only from explicit owner approval text.

Default mode is dry-run and read-only. To create APR files, pass --apply and put
the owner approval text into:

  episodes/PD-2026-014-lange/approvals/OWNER_APPROVAL_INPUT.v001.txt
  episodes/PD-2026-015-theranos/approvals/OWNER_APPROVAL_INPUT.v001.txt

The text must contain one of the exact approval blocks from
episodes/_planning/pd_014_015_owner_approval_packet.v001.md, including hashes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

EPISODES = {
    "14": {
        "episode_id": "PD-2026-014-lange",
        "title": "Can a Cop Follow You Into Your Own Home?",
        "video": "E:/pd-media/episodes/PD-2026-014-lange/08_edit/renders/lange_premium_review_proxy_v001.mp4",
        "video_sha": "sha256:0698e4294d536506c7eac40b693e911d548d23e24706d607f12f91c38d49022b",
        "thumbnail": "episodes/PD-2026-014-lange/09_package/thumbnail.selected.v001.png",
        "thumbnail_sha": "sha256:dae3f3a81eeb0253b077bbab5f581fc56e95d7eae9174fb8e84b18f73c6c6e97",
        "audio": "E:/pd-media/episodes/PD-2026-014-lange/07_audio/review_proxy_mix_v001.mp3",
        "final_delivery": "episodes/PD-2026-014-lange/09_package/final_delivery.v001.json",
        "final_delivery_sha": "sha256:3d38b5b56d9b97df568e5316814acc2526c3bfb9284f55efcf15b9c004eadc61",
        "publish_schedule_local": "2026-06-29T12:00:00+09:00",
        "publish_schedule_utc": "2026-06-29T03:00:00Z",
        "gates": {
            "first_cut": "APR-0002",
            "title_thumbnail": "APR-0003",
            "narration_release": "APR-0004",
            "publish_schedule": "APR-0005",
        },
    },
    "15": {
        "episode_id": "PD-2026-015-theranos",
        "title": "When Does a Bold Promise Become a Crime?",
        "video": "E:/pd-media/episodes/PD-2026-015-theranos/08_edit/renders/theranos_premium_review_proxy_v003.mp4",
        "video_sha": "sha256:fa119c6af8c3f37c55f23f2885d34250f65c0b0ee2f87f73ca1cccb2ce873df9",
        "thumbnail": "episodes/PD-2026-015-theranos/09_package/thumbnail.selected.v001.png",
        "thumbnail_sha": "sha256:f0d14264ffaf47aaa601ce7ad7eff5106dc828e30a3da8da17c31c3eca603963",
        "audio": "E:/pd-media/episodes/PD-2026-015-theranos/07_audio/review_proxy_mix_v001.mp3",
        "final_delivery": "episodes/PD-2026-015-theranos/09_package/final_delivery.v001.json",
        "final_delivery_sha": "sha256:d08b2adc890efcceda39df51c8b06c0d3d130d7132759887d9d8be65a0756e62",
        "publish_schedule_local": "2026-06-30T12:00:00+09:00",
        "publish_schedule_utc": "2026-06-30T03:00:00Z",
        "gates": {
            "first_cut": "APR-0002",
            "title_thumbnail": "APR-0003",
            "narration_release": "APR-0004",
            "legal_rights": "APR-0005",
            "publish_schedule": "APR-0006",
        },
    },
}

GATE_PATTERNS = {
    "first_cut": [
        r"APPROVED:\s*{episode_id}\s+first-cut review v001",
        r"Video SHA-256:\s*{video_sha}",
    ],
    "title_thumbnail": [
        r"APPROVED:\s*{episode_id}\s+title/thumbnail v001",
        r"Title:\s*{title}",
        r"Thumbnail SHA-256:\s*{thumbnail_sha}",
    ],
    "narration_release": [
        r"APPROVED:\s*{episode_id}\s+may use the local review-proxy narration for release",
        r"Audio:\s*{audio}",
    ],
    "legal_rights": [
        r"APPROVED:\s*{episode_id}\s+legal/rights review v001",
        r"legal_rights_review_packet\.v001\.md",
    ],
    "publish_schedule": [
        r"APPROVED:\s*{episode_id}\s+publish/schedule",
        r"Final delivery:\s*{final_delivery}",
        r"Final delivery SHA-256:\s*{final_delivery_sha}",
        r"Public schedule target:\s*{publish_schedule_local}\s*/\s*{publish_schedule_utc}",
    ],
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def resolve_path(value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else ROOT / value


def format_pattern(pattern: str, cfg: dict[str, Any]) -> str:
    out = pattern
    for key, value in cfg.items():
        if isinstance(value, str):
            out = out.replace("{" + key + "}", re.escape(value))
    return out


def approved_gate(text: str, gate: str, cfg: dict[str, Any]) -> bool:
    patterns = GATE_PATTERNS[gate]
    return all(re.search(format_pattern(pattern, cfg), text, flags=re.I) for pattern in patterns)


def approval_doc(cfg: dict[str, Any], gate: str, approval_id: str, input_path: Path) -> dict[str, Any]:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    episode_id = cfg["episode_id"]
    if gate == "first_cut":
        target_type = "edit"
        target_id = "review_proxy_video"
        notes = f"Owner approved first-cut review for exact video hash {cfg['video_sha']}."
        conditions = [
            "Approval covers first-cut review only.",
            "No upload, schedule, public release, or paid narration is authorized by this approval.",
        ]
        evidence = "artifact://episodes/" + episode_id + "/09_package/OWNER_REVIEW_REQUEST.v001.json"
    elif gate == "title_thumbnail":
        target_type = "package"
        target_id = "title_thumbnail"
        notes = f"Owner approved title '{cfg['title']}' and thumbnail hash {cfg['thumbnail_sha']}."
        conditions = [
            "Approval covers title/thumbnail only.",
            "No upload, schedule, public release, or paid narration is authorized by this approval.",
        ]
        evidence = "artifact://episodes/" + episode_id + "/09_package/youtube_meta.v001.json"
    elif gate == "narration_release":
        target_type = "package"
        target_id = "review_proxy_narration_release"
        notes = "Owner approved use of local review-proxy narration for release if all other gates pass."
        conditions = [
            "Approval covers narration decision only.",
            "No upload, schedule, or public release is authorized by this approval alone.",
        ]
        evidence = "artifact://episodes/" + episode_id + "/09_package/rights_manifest.v001.json"
    elif gate == "legal_rights":
        target_type = "package"
        target_id = "legal_rights_review"
        notes = "Owner approved legal/rights review packet for exact package hashes."
        conditions = [
            "Approval covers public-release risk gate only.",
            "No upload or schedule is authorized by this approval alone.",
            "Keep living-person framing record-based and neutral; no Holmes/Balwani likeness; no Theranos logo/brand mark.",
        ]
        evidence = "artifact://episodes/" + episode_id + "/09_package/legal_rights_review_packet.v001.json"
    elif gate == "publish_schedule":
        target_type = "publish"
        target_id = "youtube_schedule"
        notes = (
            "Owner approved future private upload and public schedule target "
            f"{cfg['publish_schedule_local']} / {cfg['publish_schedule_utc']}. "
            f"Approval is bound to final delivery hash {cfg['final_delivery_sha']}. "
            "This approval must be rechecked against final package hashes immediately before upload/schedule."
        )
        conditions = [
            "Initial upload must be private.",
            "Synthetic media disclosure must be set where supported.",
            f"Final delivery artifact must still hash to {cfg['final_delivery_sha']} before publish/schedule.",
        ]
        evidence = "artifact://episodes/" + episode_id + "/09_package/final_delivery.v001.json"
    else:
        raise ValueError(gate)
    return {
        "schema_version": "1.0.0",
        "approval_id": approval_id,
        "episode_id": episode_id,
        "target_type": target_type,
        "target_id": target_id,
        "target_revision": "v001",
        "decision": "approved",
        "requested_at": now,
        "requested_by": "codex",
        "decided_at": now,
        "decided_by": "owner",
        "notes": notes + f" Source input: {rel(input_path)}.",
        "conditions": conditions,
        "expires_at": None,
        "evidence_snapshot_ref": evidence,
    }


def append_event(ep_dir: Path, data: dict[str, Any]) -> None:
    events = ep_dir / "events" / "events.jsonl"
    with events.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(data, ensure_ascii=False) + "\n")


def update_manifest(ep_dir: Path, created: list[str]) -> None:
    manifest_path = ep_dir / "manifest.json"
    manifest = load_json(manifest_path)
    approvals = manifest.setdefault("approvals", [])
    for approval_id in created:
        if approval_id not in approvals:
            approvals.append(approval_id)
    manifest.setdefault("active_revisions", {})["approval_application"] = "v001"
    manifest["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    write_json(manifest_path, manifest)


def process_episode(number: str, apply: bool) -> dict[str, Any]:
    cfg = EPISODES[number]
    ep_dir = ROOT / "episodes" / cfg["episode_id"]
    approvals_dir = ep_dir / "approvals"
    input_path = approvals_dir / "OWNER_APPROVAL_INPUT.v001.txt"
    result: dict[str, Any] = {
        "episode_id": cfg["episode_id"],
        "input": rel(input_path),
        "apply": apply,
        "created": [],
        "would_create": [],
        "blocked": [],
    }
    if not input_path.exists():
        result["blocked"].append("missing owner approval input file")
        return result
    text = input_path.read_text(encoding="utf-8")

    # Guard current artifacts before trusting text.
    video_path = resolve_path(cfg["video"])
    thumb_path = resolve_path(cfg["thumbnail"])
    final_delivery_path = resolve_path(cfg["final_delivery"])
    if not video_path.exists() or sha256(video_path) != cfg["video_sha"]:
        result["blocked"].append("video missing or hash mismatch")
    if not thumb_path.exists() or sha256(thumb_path) != cfg["thumbnail_sha"]:
        result["blocked"].append("thumbnail missing or hash mismatch")
    if not final_delivery_path.exists() or sha256(final_delivery_path) != cfg["final_delivery_sha"]:
        result["blocked"].append("final delivery missing or hash mismatch")
    if result["blocked"]:
        return result

    for gate, approval_id in cfg["gates"].items():
        if not approved_gate(text, gate, cfg):
            result["blocked"].append(f"missing exact approval text for {gate}:{approval_id}")
            continue
        out_path = approvals_dir / f"{approval_id}.json"
        if out_path.exists():
            result["blocked"].append(f"approval already exists: {rel(out_path)}")
            continue
        doc = approval_doc(cfg, gate, approval_id, input_path)
        if apply:
            write_json(out_path, doc)
            result["created"].append(rel(out_path))
        else:
            result["would_create"].append(rel(out_path))

    if apply and result["created"]:
        update_manifest(ep_dir, [Path(p).stem for p in result["created"]])
        append_event(
            ep_dir,
            {
                "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
                "episode_id": cfg["episode_id"],
                "stage": "edit_review",
                "event": "owner_approvals_applied",
                "revision": "v001",
                "actor": "codex",
                "note": "Applied owner approval input into APR files for exact approved gates. Upload/schedule/publish not performed.",
                "created": result["created"],
            },
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", choices=["14", "15"], action="append", help="episode to process; default both")
    parser.add_argument("--apply", action="store_true", help="create APR files from owner approval input")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    numbers = args.episode or ["14", "15"]
    results = [process_episode(number, args.apply) for number in numbers]
    payload = {
        "schema_version": "1.0.0",
        "kind": "pd_014_015_prepare_owner_approvals",
        "apply": args.apply,
        "results": results,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"{result['episode_id']}:")
            for item in result["would_create"]:
                print(f"  WOULD_CREATE: {item}")
            for item in result["created"]:
                print(f"  CREATED: {item}")
            for item in result["blocked"]:
                print(f"  BLOCKED: {item}")
    return 0 if all(not r["blocked"] for r in results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
