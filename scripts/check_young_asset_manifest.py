#!/usr/bin/env python
"""Validate EP42 Young asset manifest from the consumer side."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-042-young"
MIN_COUNTS = {"still_body": 85, "factory": 93, "motion": 16}


def _exists(p: str) -> bool:
    path = Path(p)
    if path.is_file():
        return True
    return (ROOT / "remotion" / "public" / p).is_file()


def evaluate(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("episode_id") != EP:
        errors.append(f"episode_id mismatch: {data.get('episode_id')}")
    counts = data.get("counts") or {}
    for key, floor in MIN_COUNTS.items():
        if int(counts.get(key) or 0) < floor:
            errors.append(f"counts.{key} {counts.get(key)} < {floor}")

    stills = [s for s in data.get("stills") or [] if s.get("role") == "body"]
    factory = data.get("factory") or []
    motion = data.get("motion") or []
    if len(stills) < MIN_COUNTS["still_body"]:
        errors.append(f"body still entries {len(stills)} < 85")
    if len(factory) < MIN_COUNTS["factory"]:
        errors.append(f"factory entries {len(factory)} < 93")
    if len(motion) < MIN_COUNTS["motion"]:
        errors.append(f"motion entries {len(motion)} < 16")

    for group_name, items in [("stills", stills), ("factory", factory), ("motion", motion)]:
        for i, item in enumerate(items):
            public_path = item.get("public_path")
            if not public_path:
                errors.append(f"{group_name}[{i}] missing public_path")
                continue
            if not _exists(public_path):
                errors.append(f"{group_name}[{i}] missing media {public_path}")
            if group_name == "stills":
                if int(item.get("width") or 0) < 3840 and int(item.get("height") or 0) < 3840:
                    errors.append(f"{group_name}[{i}] long edge below 3840")
                depth = item.get("depth_path")
                if depth and not Path(depth).is_file():
                    errors.append(f"{group_name}[{i}] missing depth {depth}")
    return {"ok": not errors, "asset_manifest": str(path), "errors": errors, "counts": counts}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", type=Path, required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.assets.exists():
        print(f"FAIL young_asset_manifest: missing {args.assets}")
        return 1
    result = evaluate(args.assets)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + f" young_asset_manifest: {args.assets}")
        for err in result["errors"][:20]:
            print(f"  ! {err}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
