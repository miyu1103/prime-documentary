#!/usr/bin/env python
"""Validate EP45 Cleveland asset manifest from the consumer side."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-045-cleveland"
MIN_COUNTS = {"still_body": 84, "still_i2v_source": 16, "factory": 92, "motion": 16, "overlay": 12}
VALID_STILL_ROLES = {"body", "i2v_source", "reject"}
THUMB_IDS = {"S01", "S03", "S18", "S46", "S68", "S84"}


def _exists(p: str) -> bool:
    path = Path(p)
    if path.is_file():
        return True
    return (ROOT / "remotion" / "public" / p).is_file()


def evaluate(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("schema_version") != "cleveland_assets.v1":
        errors.append(f"schema_version mismatch: {data.get('schema_version')}")
    if data.get("episode_id") != EP:
        errors.append(f"episode_id mismatch: {data.get('episode_id')}")
    if data.get("is_stub") is True:
        errors.append("is_stub must be false for EP45")
    counts = data.get("counts") or {}
    for key, floor in MIN_COUNTS.items():
        if int(counts.get(key) or 0) < floor:
            errors.append(f"counts.{key} {counts.get(key)} < {floor}")

    all_stills = data.get("stills") or []
    bad_roles = sorted({str(s.get("role")) for s in all_stills if s.get("role") not in VALID_STILL_ROLES})
    if bad_roles:
        errors.append(f"invalid still roles: {bad_roles}")
    stills = [s for s in all_stills if s.get("role") == "body"]
    i2v_sources = [s for s in all_stills if s.get("role") == "i2v_source"]
    factory = data.get("factory") or []
    motion = data.get("motion") or []
    overlay = data.get("overlay") or []
    if len(stills) < MIN_COUNTS["still_body"]:
            errors.append(f"body still entries {len(stills)} < {MIN_COUNTS['still_body']}")
    if len(i2v_sources) < MIN_COUNTS["still_i2v_source"]:
        errors.append(f"i2v source entries {len(i2v_sources)} < 16")
    if len(factory) < MIN_COUNTS["factory"]:
            errors.append(f"factory entries {len(factory)} < {MIN_COUNTS['factory']}")
    if len(motion) < MIN_COUNTS["motion"]:
        errors.append(f"motion entries {len(motion)} < 16")
    if len(overlay) != MIN_COUNTS["overlay"]:
        errors.append(f"overlay entries {len(overlay)} != 12")
    also_thumb = {str(s.get("scene_id")) for s in stills if s.get("also_thumb") is True}
    if also_thumb != THUMB_IDS:
        errors.append(f"also_thumb set {sorted(also_thumb)} != {sorted(THUMB_IDS)}")

    for group_name, items in [("stills", all_stills), ("factory", factory), ("motion", motion), ("overlay", overlay)]:
        for i, item in enumerate(items):
            public_path = item.get("public_path")
            if group_name == "stills" and item.get("role") == "i2v_source":
                public_path = None
            elif not public_path:
                errors.append(f"{group_name}[{i}] missing public_path")
                continue
            if public_path and not _exists(public_path):
                errors.append(f"{group_name}[{i}] missing media {public_path}")
            if group_name == "stills":
                if int(item.get("width") or 0) < 3840 and int(item.get("height") or 0) < 3840:
                    errors.append(f"{group_name}[{i}] long edge below 3840")
                if item.get("role") in {"thumb", "still_thumb"}:
                    errors.append(f"{group_name}[{i}] forbidden still role {item.get('role')}")
                depth = item.get("depth_path")
                if item.get("role") == "body" and (not depth or not Path(depth).is_file()):
                    errors.append(f"{group_name}[{i}] missing depth {depth}")
                qc = item.get("qc") or {}
                if item.get("role") != "reject" and any(qc.get(k) is True for k in ("has_readable_text", "has_identifiable_face", "has_human_body")):
                    errors.append(f"{group_name}[{i}] non-reject has unsafe visual qc flag")
            if group_name == "motion" and (not str(public_path).endswith(".mp4") or "_rife" not in str(public_path)):
                errors.append(f"{group_name}[{i}] motion public_path must be *_rife.mp4")
            if group_name == "factory":
                if "/factory/" not in str(public_path).replace("\\", "/"):
                    errors.append(f"{group_name}[{i}] public_path must include /factory/")
                qc = item.get("qc") or {}
                if not item.get("eyeballed_content"):
                    errors.append(f"{group_name}[{i}] missing eyeballed_content")
                if qc.get("label_matches_content") is not True:
                    errors.append(f"{group_name}[{i}] qc.label_matches_content must be true")
            if group_name == "overlay":
                norm = str(public_path).replace("\\", "/")
                if "/overlay/" not in norm or "/factory/" in norm:
                    errors.append(f"{group_name}[{i}] overlay public_path must be under /overlay/ only")
    return {"ok": not errors, "asset_manifest": str(path), "errors": errors, "counts": counts}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", type=Path, required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.assets.exists():
        print(f"FAIL cleveland_asset_manifest: missing {args.assets}")
        return 1
    result = evaluate(args.assets)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + f" cleveland_asset_manifest: {args.assets}")
        for err in result["errors"][:20]:
            print(f"  ! {err}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


