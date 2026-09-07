#!/usr/bin/env python3
"""Centre-crop approved long-form plates for a Short REUSE design.

REUSE is a derived asset, not a second image generation: the source plate stays untouched and a
1080x1920 centre crop is written into the Short's public folder. The design records source_plate,
so provenance remains inspectable. Existing outputs are never overwritten unless --force is used.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
PUBLIC = ROOT / "remotion" / "public"


def find_short(sid: str) -> tuple[dict, dict]:
    for path in sorted(DESIGNS.glob("*.json")):
        design = json.loads(path.read_text(encoding="utf-8"))
        for short in design.get("shorts", []):
            if short.get("short_id") == sid:
                return design, short
    raise SystemExit(f"no design for {sid}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--short", required=True, help="number or shortNNN")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    sid = args.short if args.short.startswith("short") else f"short{args.short}"
    design, short = find_short(sid)
    slug = design["slug"]
    out_dir = PUBLIC / "shorts" / sid
    out_dir.mkdir(parents=True, exist_ok=True)

    staged = kept = 0
    for plate in short.get("plates", []):
        if plate.get("source") != "REUSE":
            continue
        source_plate = plate.get("source_plate")
        if not source_plate:
            raise SystemExit(f"{sid} plate {plate.get('n')}: missing source_plate")
        candidates = [
            PUBLIC / slug / "img" / f"{source_plate}.png",
            PUBLIC / slug / "img_unused" / f"{source_plate}.png",
            PUBLIC / slug / "img_deprecated" / f"{source_plate}.png",
        ]
        src = next((path for path in candidates if path.is_file()), candidates[0])
        dst = out_dir / f"{sid}_{plate['n']:02d}.png"
        if not src.is_file():
            raise SystemExit(f"{sid} plate {plate['n']}: source missing: {src}")
        if dst.exists() and not args.force:
            kept += 1
            continue
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-i", str(src),
            "-vf", "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920:flags=lanczos",
            "-frames:v", "1", str(dst),
        ], check=True)
        staged += 1

    print(f"{sid}: staged {staged}, kept {kept} -> {out_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
