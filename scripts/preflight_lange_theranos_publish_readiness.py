#!/usr/bin/env python3
"""Read-only publish-readiness preflight for PD-2026-014/015.

This script does not upload, schedule, publish, generate paid narration, or mutate
episode state. It verifies exact local package evidence and reports which approval
gates still block public release.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

EPISODES = {
    "14": {
        "episode_id": "PD-2026-014-lange",
        "slug": "lange",
        "required_real_approvals": {
            "first_cut": "APR-0002",
            "title_thumbnail": "APR-0003",
            "narration_release": "APR-0004",
            "publish_schedule": "APR-0005",
        },
        "required_packet": "prepublish_review_packet.v001.json",
        "rights_expected": {"ok": 173, "mismatch": 0, "missing": 0, "nohash": 0},
        "legal_review_required": False,
    },
    "15": {
        "episode_id": "PD-2026-015-theranos",
        "slug": "theranos",
        "required_real_approvals": {
            "first_cut": "APR-0002",
            "title_thumbnail": "APR-0003",
            "narration_release": "APR-0004",
            "legal_rights": "APR-0005",
            "publish_schedule": "APR-0006",
        },
        "required_packet": "legal_rights_review_packet.v001.json",
        "rights_expected": {"ok": 160, "mismatch": 0, "missing": 0, "nohash": 0},
        "legal_review_required": True,
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def run_text(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def parse_rights_summary(output: str) -> dict[str, int] | None:
    for line in output.splitlines():
        if line.startswith("summary:"):
            values: dict[str, int] = {}
            for part in line.replace("summary:", "").split():
                if "=" not in part:
                    continue
                key, raw = part.split("=", 1)
                try:
                    values[key.lower().replace("-", "")] = int(raw)
                except ValueError:
                    pass
            return {
                "ok": values.get("ok", -1),
                "mismatch": values.get("mismatch", -1),
                "missing": values.get("missing", -1),
                "nohash": values.get("nohash", -1),
                "total": values.get("total", -1),
            }
    return None


def check_episode(number: str) -> dict[str, Any]:
    cfg = EPISODES[number]
    ep = cfg["episode_id"]
    ep_dir = ROOT / "episodes" / ep
    pkg = ep_dir / "09_package"
    approvals_dir = ep_dir / "approvals"
    result: dict[str, Any] = {
        "episode_id": ep,
        "status": "UNKNOWN",
        "public_release_allowed": False,
        "checks": [],
        "blockers": [],
        "warnings": [],
    }

    def add_check(name: str, ok: bool, detail: str) -> None:
        result["checks"].append({"name": name, "ok": ok, "detail": detail})
        if not ok:
            result["blockers"].append(f"{name}: {detail}")

    manifest_path = ep_dir / "manifest.json"
    final_path = pkg / "final_delivery.v001.json"
    meta_path = pkg / "youtube_meta.v001.json"
    rights_path = pkg / "rights_manifest.v001.json"
    owner_request_path = pkg / "OWNER_REVIEW_REQUEST.v001.json"
    approval_drafts_path = pkg / "approval_drafts.v001.json"
    review_packet_path = pkg / cfg["required_packet"]

    required_files = [
        manifest_path,
        final_path,
        meta_path,
        rights_path,
        owner_request_path,
        approval_drafts_path,
        review_packet_path,
    ]
    for path in required_files:
        add_check(f"file_exists:{rel(path)}", path.exists(), rel(path))

    if result["blockers"]:
        result["status"] = "BLOCKED"
        return result

    manifest = load_json(manifest_path)
    final = load_json(final_path)
    meta = load_json(meta_path)
    rights = load_json(rights_path)
    owner_request = load_json(owner_request_path)

    add_check("state_is_edit_review_or_later", manifest.get("state") in {"edit_review", "finalizing", "package_ready", "publish_approved", "scheduled", "published"}, str(manifest.get("state")))
    add_check("package_marks_no_public_release", owner_request.get("public_release_allowed") is False, "owner review request must not authorize release")
    add_check("no_logo_or_likeness_declared", rights.get("contains_real_person_likeness") is False and rights.get("contains_logo_or_brand_mark") is False, "rights manifest likeness/logo flags")
    add_check("synthetic_disclosure_required", rights.get("synthetic_content_disclosure_required") is True, "synthetic disclosure flag")

    video_path = Path(final["review_video"])
    add_check("video_exists", video_path.exists(), str(video_path))
    if video_path.exists():
        actual_video_sha = sha256(video_path)
        add_check("video_sha_matches_final_delivery", actual_video_sha == final.get("review_video_sha256"), actual_video_sha)
        add_check("video_sha_matches_youtube_meta", actual_video_sha == meta.get("video_sha256"), actual_video_sha)
        add_check("video_sha_matches_owner_request", actual_video_sha == owner_request.get("review_video", {}).get("sha256"), actual_video_sha)

    thumb_path = ROOT / meta["thumbnail"]
    add_check("thumbnail_exists", thumb_path.exists(), rel(thumb_path))
    if thumb_path.exists():
        thumb_sha = sha256(thumb_path)
        declared_thumb_sha = meta.get("selected_thumbnail_sha256")
        add_check("thumbnail_sha_matches_youtube_meta", thumb_sha == declared_thumb_sha, thumb_sha)
        add_check("thumbnail_sha_matches_owner_request", thumb_sha == owner_request.get("thumbnail", {}).get("sha256"), thumb_sha)

    code, validation_output = run_text([sys.executable, "scripts/validate_episode.py", number])
    add_check("validate_episode_pass", code == 0 and "RESULT: PASS" in validation_output, validation_output.strip().splitlines()[-1] if validation_output.strip() else "")

    code, rights_output = run_text([sys.executable, "scripts/verify_rights_hashes.py", rel(rights_path)])
    summary = parse_rights_summary(rights_output)
    expected = cfg["rights_expected"]
    rights_ok = (
        code == 0
        and summary is not None
        and summary["ok"] == expected["ok"]
        and summary["mismatch"] == expected["mismatch"]
        and summary["missing"] == expected["missing"]
        and summary["nohash"] == expected["nohash"]
    )
    add_check("rights_hashes_match_expected", rights_ok, json.dumps(summary, sort_keys=True) if summary else "missing summary")

    real_approvals = set(manifest.get("approvals", []))
    for gate, approval_id in cfg["required_real_approvals"].items():
        approval_path = approvals_dir / f"{approval_id}.json"
        ok = approval_id in real_approvals and approval_path.exists()
        add_check(f"approval_present:{gate}:{approval_id}", ok, rel(approval_path))

    if cfg["legal_review_required"]:
        packet = load_json(review_packet_path)
        recommendation = packet.get("public_release_recommendation", "")
        add_check(
            "theranos_legal_packet_blocks_until_review",
            "do_not_publish" in recommendation,
            recommendation or "missing recommendation",
        )

    if any(not item["ok"] for item in result["checks"]):
        result["status"] = "BLOCKED"
        result["public_release_allowed"] = False
    else:
        result["status"] = "PASS"
        result["public_release_allowed"] = True
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", choices=["14", "15"], action="append", help="episode number to check; default: both")
    parser.add_argument("--json", action="store_true", help="emit JSON only")
    args = parser.parse_args()

    numbers = args.episode or ["14", "15"]
    results = [check_episode(number) for number in numbers]
    payload = {
        "schema_version": "1.0.0",
        "kind": "pd_014_015_publish_readiness_preflight",
        "public_release_allowed": all(item["public_release_allowed"] for item in results),
        "episodes": results,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"{item['episode_id']}: {item['status']}")
            for blocker in item["blockers"]:
                print(f"  BLOCKED: {blocker}")
            if not item["blockers"]:
                print("  PASS: public release gates are satisfied")
        print(f"\npublic_release_allowed={payload['public_release_allowed']}")
    return 0 if payload["public_release_allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
