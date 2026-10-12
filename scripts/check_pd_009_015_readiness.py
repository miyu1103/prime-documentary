#!/usr/bin/env python3
"""Aggregate readiness check for PD episodes 009-015.

This script is intentionally conservative and mostly read-only. It reruns the
local validators/preflights and writes a current summary under episodes/_planning.
It does not upload, schedule, publish, call paid APIs, or create approvals.
"""
from __future__ import annotations

import json
import re
import hashlib
import struct
import subprocess
import sys
import urllib.parse
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "episodes" / "_planning"
MEDIA = Path("E:/pd-media")
EPISODES = {
    "9": "PD-2026-009-timbs",
    "10": "PD-2026-010-kelo",
    "11": "PD-2026-011-mahanoy",
    "12": "PD-2026-012-arbitration",
    "13": "PD-2026-013-king",
    "14": "PD-2026-014-lange",
    "15": "PD-2026-015-theranos",
}
AI_IMAGE_EPISODES = {
    "PD-2026-014-lange": {
        "slug": "lange",
        "prompt_path": ROOT / "episodes" / "PD-2026-014-lange" / "04_scenes" / "ai_prompts.v001.md",
        "image_dir": MEDIA / "assets" / "ai" / "lange",
    },
    "PD-2026-015-theranos": {
        "slug": "theranos",
        "prompt_path": ROOT / "episodes" / "PD-2026-015-theranos" / "04_scenes" / "ai_prompts.v001.md",
        "image_dir": MEDIA / "assets" / "ai" / "theranos",
    },
}
EXPECTED_MANIFEST_BLOCKER_APPROVALS = {
    "PD-2026-014-lange": ["APR-0002", "APR-0003", "APR-0004", "APR-0005"],
    "PD-2026-015-theranos": ["APR-0002", "APR-0003", "APR-0004", "APR-0005", "APR-0006"],
}
EXPECTED_APPROVAL_DRAFT_GATES = {
    "PD-2026-014-lange": {
        "APR-0002-DRAFT": "first_cut_review",
        "APR-0003-DRAFT": "title_thumbnail",
        "APR-0004-DRAFT": "narration_release",
        "APR-0005-DRAFT": "publish_schedule",
    },
    "PD-2026-015-theranos": {
        "APR-0002-DRAFT": "first_cut_review",
        "APR-0003-DRAFT": "title_thumbnail",
        "APR-0004-DRAFT": "narration_release",
        "APR-0005-DRAFT": "legal_rights",
        "APR-0006-DRAFT": "publish_schedule",
    },
}
EXPECTED_FINAL_DELIVERY_HASHES = {
    "PD-2026-014-lange": {
        "path": "episodes/PD-2026-014-lange/09_package/final_delivery.v001.json",
        "sha256": "sha256:3d38b5b56d9b97df568e5316814acc2526c3bfb9284f55efcf15b9c004eadc61",
    },
    "PD-2026-015-theranos": {
        "path": "episodes/PD-2026-015-theranos/09_package/final_delivery.v001.json",
        "sha256": "sha256:d08b2adc890efcceda39df51c8b06c0d3d130d7132759887d9d8be65a0756e62",
    },
}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        for key in ["href", "src"]:
            value = attr_map.get(key)
            if value:
                self.links.append((tag, key, value))


def run(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    return {
        "args": args,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def artifact_uri_to_path(uri: str) -> Path | None:
    prefix = "artifact://"
    if not uri.startswith(prefix):
        return None
    return ROOT / uri[len(prefix) :]


def parse_validate_result(output: str) -> str:
    for line in reversed(output.splitlines()):
        if line.startswith("RESULT:"):
            return line.replace("RESULT:", "").strip()
    return "UNKNOWN"


def parse_rights_summary(output: str) -> dict[str, int] | None:
    for line in output.splitlines():
        if not line.startswith("summary:"):
            continue
        result: dict[str, int] = {}
        for part in line.replace("summary:", "").split():
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            try:
                result[key.lower().replace("-", "")] = int(value)
            except ValueError:
                pass
        return {
            "ok": result.get("ok", -1),
            "mismatch": result.get("mismatch", -1),
            "missing": result.get("missing", -1),
            "nohash": result.get("nohash", -1),
            "total": result.get("total", -1),
        }
    return None


def check_html_links(path: Path) -> dict[str, Any]:
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    missing: list[dict[str, str]] = []
    ok = 0
    for tag, attr, url in parser.links:
        if url.startswith("http"):
            ok += 1
            continue
        if url.startswith("file:///"):
            target = Path(urllib.parse.unquote(url[8:]))
        else:
            target = (path.parent / url).resolve()
        if target.exists():
            ok += 1
        else:
            missing.append({"tag": tag, "attr": attr, "url": url, "resolved": str(target)})
    return {"path": rel(path), "ok": ok, "missing": missing, "total": len(parser.links)}


def read_png_size(path: Path) -> tuple[int, int] | None:
    try:
        header = path.read_bytes()[:24]
    except OSError:
        return None
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", header[16:24])


def parse_prompt_image_names(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    names: list[str] = []
    for match in re.finditer(r"`([^`]+\.png)`", text):
        name = match.group(1)
        if re.match(r"^[A-Za-z0-9_-]+\.png$", name):
            names.append(name)
    return list(dict.fromkeys(names))


def check_ai_images(episode_id: str, cfg: dict[str, Any]) -> dict[str, Any]:
    expected = parse_prompt_image_names(cfg["prompt_path"])
    present = sorted(path.name for path in cfg["image_dir"].glob("*.png")) if cfg["image_dir"].exists() else []
    expected_set = set(expected)
    present_set = set(present)
    missing = sorted(expected_set - present_set)
    extra = sorted(present_set - expected_set)
    bad_dimensions: list[dict[str, Any]] = []
    invalid_png: list[str] = []

    for name in sorted(expected_set & present_set):
        size = read_png_size(cfg["image_dir"] / name)
        if size is None:
            invalid_png.append(name)
            continue
        width, height = size
        ratio = width / height if height else 0
        if max(width, height) < 2048 or abs(ratio - (16 / 9)) > 0.03:
            bad_dimensions.append({"file": name, "width": width, "height": height})

    return {
        "episode_id": episode_id,
        "slug": cfg["slug"],
        "prompt_path": rel(cfg["prompt_path"]),
        "image_dir": str(cfg["image_dir"]).replace("\\", "/"),
        "required": len(expected),
        "present": len(present),
        "matched": len(expected_set & present_set),
        "missing": missing,
        "extra": extra,
        "invalid_png": invalid_png,
        "bad_dimensions": bad_dimensions,
        "pass": not missing and not invalid_png and not bad_dimensions,
    }


def check_manifest_blockers(episode_id: str, manifest: dict[str, Any]) -> dict[str, Any]:
    blockers = manifest.get("blockers", [])
    blocker_text = "\n".join(str(item) for item in blockers)
    expected = EXPECTED_MANIFEST_BLOCKER_APPROVALS[episode_id]
    missing_approval_refs = [approval_id for approval_id in expected if approval_id not in blocker_text]
    return {
        "episode_id": episode_id,
        "blocker_count": len(blockers),
        "expected_approval_refs": expected,
        "missing_approval_refs": missing_approval_refs,
        "pass": bool(blockers) and not missing_approval_refs,
    }


def check_approval_guides(episode_id: str) -> dict[str, Any]:
    ep_dir = ROOT / "episodes" / episode_id
    drafts_path = ep_dir / "09_package" / "approval_drafts.v001.json"
    template_path = ep_dir / "approvals" / "OWNER_APPROVAL_INPUT.template.v001.txt"
    active_input_path = ep_dir / "approvals" / "OWNER_APPROVAL_INPUT.v001.txt"
    expected = EXPECTED_APPROVAL_DRAFT_GATES[episode_id]
    actual: dict[str, str] = {}
    errors: list[str] = []

    if drafts_path.exists():
        try:
            drafts = load_json(drafts_path).get("drafts", [])
            actual = {str(item.get("draft_id")): str(item.get("gate")) for item in drafts}
            publish_drafts = [item for item in drafts if item.get("gate") == "publish_schedule"]
            expected_delivery = EXPECTED_FINAL_DELIVERY_HASHES[episode_id]
            if len(publish_drafts) != 1:
                errors.append("approval drafts must include exactly one publish_schedule draft")
            else:
                publish_draft = publish_drafts[0]
                if publish_draft.get("final_delivery") != expected_delivery["path"]:
                    errors.append("publish_schedule draft final_delivery mismatch")
                if publish_draft.get("final_delivery_sha256") != expected_delivery["sha256"]:
                    errors.append("publish_schedule draft final_delivery_sha256 mismatch")
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"approval_drafts unreadable: {exc}")
    else:
        errors.append(f"missing approval_drafts: {rel(drafts_path)}")

    if actual != expected:
        errors.append("approval draft gate numbering mismatch")
    if not template_path.exists():
        errors.append(f"missing template: {rel(template_path)}")
    if active_input_path.exists():
        errors.append(f"active owner approval input exists before approval: {rel(active_input_path)}")

    return {
        "episode_id": episode_id,
        "approval_drafts": rel(drafts_path),
        "template": rel(template_path),
        "active_input": rel(active_input_path),
        "expected": expected,
        "actual": actual,
        "errors": errors,
        "pass": not errors,
    }


def check_manifest_artifacts(episode_id: str, manifest: dict[str, Any]) -> dict[str, Any]:
    checked: list[dict[str, Any]] = []
    errors: list[str] = []
    for artifact in manifest.get("artifacts", []):
        artifact_id = str(artifact.get("artifact_id", ""))
        uri = str(artifact.get("uri", ""))
        expected = str(artifact.get("checksum", ""))
        path = artifact_uri_to_path(uri)
        if path is None:
            errors.append(f"{artifact_id}: unsupported uri {uri}")
            checked.append({"artifact_id": artifact_id, "uri": uri, "ok": False, "reason": "unsupported_uri"})
            continue
        if not path.exists():
            errors.append(f"{artifact_id}: missing file {rel(path)}")
            checked.append({"artifact_id": artifact_id, "uri": uri, "ok": False, "reason": "missing_file"})
            continue
        actual = sha256(path)
        ok = actual == expected
        if not ok:
            errors.append(f"{artifact_id}: checksum mismatch")
        checked.append(
            {
                "artifact_id": artifact_id,
                "uri": uri,
                "path": rel(path),
                "expected": expected,
                "actual": actual,
                "ok": ok,
            }
        )

    return {
        "episode_id": episode_id,
        "checked": checked,
        "errors": errors,
        "pass": bool(checked) and not errors,
    }


def main() -> int:
    PLANNING.mkdir(parents=True, exist_ok=True)
    now = datetime.now().astimezone().isoformat(timespec="seconds")

    episodes: list[dict[str, Any]] = []
    for number, episode_id in EPISODES.items():
        ep_dir = ROOT / "episodes" / episode_id
        manifest = load_json(ep_dir / "manifest.json")
        validation = run([sys.executable, "scripts/validate_episode.py", number])
        episodes.append(
            {
                "number": number,
                "episode_id": episode_id,
                "state": manifest.get("state"),
                "approvals": manifest.get("approvals", []),
                "active_revisions": manifest.get("active_revisions", {}),
                "validate_episode": {
                    "returncode": validation["returncode"],
                    "result": parse_validate_result(validation["stdout"] + validation["stderr"]),
                },
            }
        )

    rights_checks = []
    for episode_id, expected_ok in [
        ("PD-2026-014-lange", 173),
        ("PD-2026-015-theranos", 160),
    ]:
        rights_path = ROOT / "episodes" / episode_id / "09_package" / "rights_manifest.v001.json"
        rights = run([sys.executable, "scripts/verify_rights_hashes.py", rel(rights_path)])
        summary = parse_rights_summary(rights["stdout"] + rights["stderr"])
        rights_checks.append(
            {
                "episode_id": episode_id,
                "path": rel(rights_path),
                "returncode": rights["returncode"],
                "summary": summary,
                "expected_ok": expected_ok,
                "pass": bool(
                    rights["returncode"] == 0
                    and summary
                    and summary["ok"] == expected_ok
                    and summary["mismatch"] == 0
                    and summary["missing"] == 0
                    and summary["nohash"] == 0
                ),
            }
        )

    image_checks = [
        check_ai_images(episode_id, cfg) for episode_id, cfg in AI_IMAGE_EPISODES.items()
    ]
    manifest_blocker_checks = [
        check_manifest_blockers(
            episode_id,
            load_json(ROOT / "episodes" / episode_id / "manifest.json"),
        )
        for episode_id in EXPECTED_MANIFEST_BLOCKER_APPROVALS
    ]
    approval_guide_checks = [
        check_approval_guides(episode_id) for episode_id in EXPECTED_APPROVAL_DRAFT_GATES
    ]
    artifact_checks = [
        check_manifest_artifacts(
            episode_id,
            load_json(ROOT / "episodes" / episode_id / "manifest.json"),
        )
        for episode_id in EXPECTED_MANIFEST_BLOCKER_APPROVALS
    ]

    approval_dry = run([sys.executable, "scripts/prepare_lange_theranos_approvals.py", "--json"])
    publish_preflight = run(
        [sys.executable, "scripts/preflight_lange_theranos_publish_readiness.py", "--json"]
    )
    approval_payload = json.loads(approval_dry["stdout"]) if approval_dry["stdout"].strip() else {}
    preflight_payload = (
        json.loads(publish_preflight["stdout"]) if publish_preflight["stdout"].strip() else {}
    )

    html_check = check_html_links(PLANNING / "pd_014_015_owner_review.html")

    payload = {
        "schema_version": "1.0.0",
        "generated_at": now,
        "kind": "pd_009_015_readiness_check",
        "external_side_effects": {
            "paid_api": False,
            "upload": False,
            "publish": False,
            "schedule": False,
            "approval_files_created": False,
        },
        "episodes": episodes,
        "rights_checks": rights_checks,
        "ai_image_checks": image_checks,
        "manifest_blocker_checks": manifest_blocker_checks,
        "approval_guide_checks": approval_guide_checks,
        "artifact_checksum_checks": artifact_checks,
        "owner_review_dashboard_links": html_check,
        "approval_apply_dry_run": {
            "returncode": approval_dry["returncode"],
            "payload": approval_payload,
            "blocked_as_expected": approval_dry["returncode"] == 2,
        },
        "publish_readiness_preflight": {
            "returncode": publish_preflight["returncode"],
            "payload": preflight_payload,
            "blocked_as_expected": publish_preflight["returncode"] == 2
            and preflight_payload.get("public_release_allowed") is False,
        },
    }

    all_validators_pass = all(
        item["validate_episode"]["returncode"] == 0
        and item["validate_episode"]["result"].startswith("PASS")
        for item in episodes
    )
    all_rights_pass = all(item["pass"] for item in rights_checks)
    all_images_pass = all(item["pass"] for item in image_checks)
    all_manifest_blockers_pass = all(item["pass"] for item in manifest_blocker_checks)
    all_approval_guides_pass = all(item["pass"] for item in approval_guide_checks)
    all_artifact_checks_pass = all(item["pass"] for item in artifact_checks)
    links_pass = not html_check["missing"]
    expected_blocks = (
        payload["approval_apply_dry_run"]["blocked_as_expected"]
        and payload["publish_readiness_preflight"]["blocked_as_expected"]
    )
    payload["summary"] = {
        "status": "REVIEW_READY_BLOCKED_BY_APPROVALS"
        if all_validators_pass
        and all_rights_pass
        and all_images_pass
        and all_manifest_blockers_pass
        and all_approval_guides_pass
        and all_artifact_checks_pass
        and links_pass
        and expected_blocks
        else "NEEDS_ATTENTION",
        "validators_pass": all_validators_pass,
        "rights_pass": all_rights_pass,
        "ai_images_pass": all_images_pass,
        "manifest_blockers_pass": all_manifest_blockers_pass,
        "approval_guides_pass": all_approval_guides_pass,
        "artifact_checks_pass": all_artifact_checks_pass,
        "links_pass": links_pass,
        "approval_apply_blocked_as_expected": payload["approval_apply_dry_run"][
            "blocked_as_expected"
        ],
        "publish_blocked_as_expected": payload["publish_readiness_preflight"][
            "blocked_as_expected"
        ],
    }

    out_json = PLANNING / "pd_009_015_readiness_check.latest.json"
    out_md = PLANNING / "pd_009_015_readiness_check.latest.md"
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# PD 009-015 Readiness Check",
        "",
        f"Generated: {now}",
        "",
        f"Status: `{payload['summary']['status']}`",
        "",
        "| Episode | State | Approvals | validate_episode |",
        "|---|---:|---|---|",
    ]
    for item in episodes:
        lines.append(
            f"| {item['episode_id']} | {item['state']} | {', '.join(item['approvals']) or '-'} | {item['validate_episode']['result']} |"
        )
    lines += [
        "",
        "## Rights",
        "",
    ]
    for item in rights_checks:
        summary = item["summary"] or {}
        lines.append(
            f"- {item['episode_id']}: pass={item['pass']} OK={summary.get('ok')} MISMATCH={summary.get('mismatch')} MISSING={summary.get('missing')} NO-HASH={summary.get('nohash')}"
        )
    lines += [
        "",
        "## AI Images",
        "",
    ]
    for item in image_checks:
        lines.append(
            f"- {item['episode_id']}: pass={item['pass']} required={item['required']} present={item['present']} matched={item['matched']} missing={len(item['missing'])} bad_dimensions={len(item['bad_dimensions'])} invalid_png={len(item['invalid_png'])}"
        )
    lines += [
        "",
        "## Manifest Blockers",
        "",
    ]
    for item in manifest_blocker_checks:
        missing = ", ".join(item["missing_approval_refs"]) or "-"
        lines.append(
            f"- {item['episode_id']}: pass={item['pass']} blocker_count={item['blocker_count']} missing_approval_refs={missing}"
        )
    lines += [
        "",
        "## Approval Guides",
        "",
    ]
    for item in approval_guide_checks:
        errors = "; ".join(item["errors"]) or "-"
        lines.append(
            f"- {item['episode_id']}: pass={item['pass']} draft_count={len(item['actual'])} errors={errors}"
        )
    lines += [
        "",
        "## Manifest Artifact Checksums",
        "",
    ]
    for item in artifact_checks:
        errors = "; ".join(item["errors"]) or "-"
        lines.append(
            f"- {item['episode_id']}: pass={item['pass']} checked={len(item['checked'])} errors={errors}"
        )
    lines += [
        "",
        "## Expected Blocks",
        "",
        f"- approval apply dry-run blocked as expected: {payload['approval_apply_dry_run']['blocked_as_expected']}",
        f"- publish readiness blocked as expected: {payload['publish_readiness_preflight']['blocked_as_expected']}",
        f"- owner review dashboard links missing: {len(html_check['missing'])}",
        "",
        "No paid API, upload, schedule, publish, or APR creation was performed.",
    ]
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(rel(out_json))
    print(rel(out_md))
    print(payload["summary"]["status"])
    return 0 if payload["summary"]["status"] == "REVIEW_READY_BLOCKED_BY_APPROVALS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
