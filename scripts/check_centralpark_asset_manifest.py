#!/usr/bin/env python
"""Validate EP50 Central Park asset manifest from the consumer side."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-050-centralpark"
DEFAULT_ASSETS = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
EXPECTED_COUNTS = {
    "still_body": 430,
    "still_i2v_source": 85,
    "depth_maps": 515,
    "motion": 85,
    "factory": 485,
    "overlay": 60,
}
VALID_STILL_ROLES = {"body", "i2v_source", "reject"}
THUMB_IDS = {"S001", "S018", "S095", "S210", "S268", "S331", "S372", "S408"}


def _exists(path_value: str | None) -> bool:
    if not path_value:
        return False
    path = Path(path_value)
    if path.is_file():
        return True
    return (ROOT / "remotion" / "public" / path_value).is_file()


def evaluate(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("schema_version") != "centralpark_assets.v1":
        errors.append(f"schema_version mismatch: {data.get('schema_version')}")
    if data.get("episode_id") != EP:
        errors.append(f"episode_id mismatch: {data.get('episode_id')}")
    if data.get("slug") != "centralpark":
        errors.append(f"slug mismatch: {data.get('slug')}")
    if data.get("is_stub") is True:
        errors.append("is_stub must be false for EP50")
    if data.get("sdxl_used") is not False:
        errors.append("sdxl_used must be false")

    counts = data.get("counts") or {}
    for key, expected in EXPECTED_COUNTS.items():
        if int(counts.get(key) or 0) != expected:
            errors.append(f"counts.{key} {counts.get(key)} != {expected}")

    all_stills = data.get("stills") or []
    body = [s for s in all_stills if s.get("role") == "body"]
    i2v_sources = [s for s in all_stills if s.get("role") == "i2v_source"]
    factory = data.get("factory") or []
    motion = data.get("motion") or []
    overlay = data.get("overlay") or []

    lengths = {
        "still_body": len(body),
        "still_i2v_source": len(i2v_sources),
        "depth_maps": sum(1 for s in all_stills if s.get("depth_path")),
        "motion": len(motion),
        "factory": len(factory),
        "overlay": len(overlay),
    }
    for key, expected in EXPECTED_COUNTS.items():
        if lengths[key] != expected:
            errors.append(f"{key} entries {lengths[key]} != {expected}")

    bad_roles = sorted({str(s.get("role")) for s in all_stills if s.get("role") not in VALID_STILL_ROLES})
    if bad_roles:
        errors.append(f"invalid still roles: {bad_roles}")
    if any(s.get("role") in {"thumb", "still_thumb"} for s in all_stills):
        errors.append("forbidden thumb/still_thumb still role present")
    also_thumb = {str(s.get("scene_id")) for s in body if s.get("also_thumb") is True}
    if also_thumb != THUMB_IDS:
        errors.append(f"also_thumb set {sorted(also_thumb)} != {sorted(THUMB_IDS)}")

    seen_sha: set[str] = set()
    for group_name, items in [("stills", all_stills), ("factory", factory), ("motion", motion), ("overlay", overlay)]:
        for i, item in enumerate(items):
            public_path = item.get("public_path")
            if group_name == "stills" and item.get("role") == "i2v_source":
                public_path = None
            elif not public_path:
                errors.append(f"{group_name}[{i}] missing public_path")
            if public_path and not _exists(public_path):
                errors.append(f"{group_name}[{i}] missing public media {public_path}")
            path_value = item.get("path")
            if path_value and not _exists(path_value):
                errors.append(f"{group_name}[{i}] missing source media {path_value}")
            sha = str(item.get("sha256") or "")
            if sha:
                if sha in seen_sha:
                    errors.append(f"{group_name}[{i}] duplicate sha256 {sha}")
                seen_sha.add(sha)

            qc = item.get("qc") or {}
            if group_name == "stills":
                if int(item.get("width") or 0) < 3840 and int(item.get("height") or 0) < 3840:
                    errors.append(f"{group_name}[{i}] long edge below 3840")
                depth = item.get("depth_path")
                if item.get("role") == "body" and not _exists(depth):
                    errors.append(f"{group_name}[{i}] missing depth {depth}")
                # Reconciled EP50 spec: anonymized-by-composition human bodies are ALLOWED
                # (qc.has_human_body may be True). We still hard-reject as-real-person likeness,
                # readable text, and any victim/assault depiction.
                unsafe_keys = (
                    "has_readable_text",
                    "has_identifiable_face",
                    "has_identifiable_real_person",
                    "depicts_victim",
                    "depicts_assault",
                )
                if item.get("role") != "reject" and any(qc.get(k) is True for k in unsafe_keys):
                    errors.append(f"{group_name}[{i}] unsafe visual qc flag")
            if group_name == "motion" and (not str(public_path).endswith(".mp4") or "_rife" not in str(public_path)):
                errors.append(f"{group_name}[{i}] motion public_path must be *_rife.mp4")
            if group_name == "factory":
                if "/factory/" not in str(public_path).replace("\\", "/"):
                    errors.append(f"{group_name}[{i}] public_path must include /factory/")
                if not item.get("eyeballed_content"):
                    errors.append(f"{group_name}[{i}] missing eyeballed_content")
                if qc.get("label_matches_content") is not True:
                    errors.append(f"{group_name}[{i}] qc.label_matches_content must be true")
            if group_name == "overlay":
                norm = str(public_path).replace("\\", "/")
                if "/overlay/" not in norm or "/factory/" in norm:
                    errors.append(f"{group_name}[{i}] overlay public_path must be under /overlay/ only")
                if qc.get("label_matches_content") is not True:
                    errors.append(f"{group_name}[{i}] qc.label_matches_content must be true")
    return {"ok": not errors, "asset_manifest": str(path), "errors": errors, "counts": counts}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.assets.exists():
        print(f"FAIL centralpark_asset_manifest: missing {args.assets}")
        return 1
    result = evaluate(args.assets)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + f" centralpark_asset_manifest: {args.assets}")
        for err in result["errors"][:30]:
            print(f"  ! {err}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
