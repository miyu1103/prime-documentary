#!/usr/bin/env python
"""Validate EP49 Strieff asset manifest from the consumer side."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-049-strieff"
EXPECTED = {"still_body": 85, "still_i2v_source": 16, "factory": 93, "motion": 16, "overlay": 12}
VALID_STILL_ROLES = {"body", "i2v_source", "reject"}
THUMB_IDS = {"S01", "S05", "S15", "S30", "S37", "S47"}


def _exists(p: str) -> bool:
    path = Path(p)
    if path.is_file():
        return True
    return (ROOT / "remotion" / "public" / p).is_file()


def evaluate(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("schema_version") != "strieff_assets.v1":
        errors.append(f"schema_version mismatch: {data.get('schema_version')}")
    if data.get("episode_id") != EP:
        errors.append(f"episode_id mismatch: {data.get('episode_id')}")
    if data.get("is_stub") is True:
        errors.append("is_stub must be false for EP49")
    if data.get("sdxl_used") is not False:
        errors.append("sdxl_used must be false")

    counts = data.get("counts") or {}
    for key, expected in EXPECTED.items():
        if int(counts.get(key) or 0) != expected:
            errors.append(f"counts.{key} {counts.get(key)} != {expected}")

    all_stills = data.get("stills") or []
    bad_roles = sorted({str(s.get("role")) for s in all_stills if s.get("role") not in VALID_STILL_ROLES})
    if bad_roles:
        errors.append(f"invalid still roles: {bad_roles}")
    body = [s for s in all_stills if s.get("role") == "body"]
    i2v = [s for s in all_stills if s.get("role") == "i2v_source"]
    groups = {
        "still_body": body,
        "still_i2v_source": i2v,
        "factory": data.get("factory") or [],
        "motion": data.get("motion") or [],
        "overlay": data.get("overlay") or [],
    }
    for key, rows in groups.items():
        if len(rows) != EXPECTED[key]:
            errors.append(f"{key} entries {len(rows)} != {EXPECTED[key]}")
    thumbs = {str(s.get("scene_id")) for s in body if s.get("also_thumb") is True}
    if thumbs != THUMB_IDS:
        errors.append(f"also_thumb set {sorted(thumbs)} != {sorted(THUMB_IDS)}")

    seen_public: set[str] = set()
    seen_sha: set[str] = set()
    for group_name, items in [("stills", all_stills), ("factory", groups["factory"]), ("motion", groups["motion"]), ("overlay", groups["overlay"])]:
        for i, item in enumerate(items):
            public_path = item.get("public_path")
            if not public_path:
                errors.append(f"{group_name}[{i}] missing public_path")
                continue
            if public_path in seen_public:
                errors.append(f"{group_name}[{i}] duplicate public_path {public_path}")
            seen_public.add(str(public_path))
            if not _exists(str(public_path)):
                errors.append(f"{group_name}[{i}] missing public media {public_path}")
            sha = item.get("sha256")
            if sha:
                if sha in seen_sha:
                    errors.append(f"{group_name}[{i}] duplicate sha256 {sha}")
                seen_sha.add(str(sha))
            if group_name == "stills":
                if int(item.get("width") or 0) != 3840 or int(item.get("height") or 0) != 2160:
                    errors.append(f"{group_name}[{i}] wrong size {item.get('width')}x{item.get('height')}")
                if item.get("role") in {"thumb", "still_thumb"}:
                    errors.append(f"{group_name}[{i}] forbidden still role {item.get('role')}")
                depth = item.get("depth_path")
                if item.get("role") == "body" and (not depth or not Path(str(depth)).is_file()):
                    errors.append(f"{group_name}[{i}] missing depth {depth}")
                qc = item.get("qc") or {}
                if item.get("role") != "reject" and any(qc.get(k) is True for k in ("has_readable_text", "has_identifiable_face", "has_human_body")):
                    errors.append(f"{group_name}[{i}] non-reject has unsafe visual qc flag")
            if group_name == "motion":
                if not str(public_path).endswith("_rife.mp4"):
                    errors.append(f"{group_name}[{i}] motion public_path must be *_rife.mp4")
            if group_name == "factory":
                if "/factory/" not in str(public_path).replace("\\", "/"):
                    errors.append(f"{group_name}[{i}] public_path must include /factory/")
                qc = item.get("qc") or {}
                if not item.get("eyeballed_content"):
                    errors.append(f"{group_name}[{i}] missing eyeballed_content")
                if qc.get("label_matches_content") is not True:
                    errors.append(f"{group_name}[{i}] qc.label_matches_content must be true")
            if group_name == "overlay" and "/overlay/" not in str(public_path).replace("\\", "/"):
                errors.append(f"{group_name}[{i}] overlay public_path must include /overlay/")
    return {"ok": not errors, "asset_manifest": str(path), "counts": counts, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.assets.exists():
        print(f"FAIL strieff_asset_manifest: missing {args.assets}")
        return 1
    result = evaluate(args.assets)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + f" strieff_asset_manifest: {args.assets}")
        for err in result["errors"][:40]:
            print(f"  ! {err}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
