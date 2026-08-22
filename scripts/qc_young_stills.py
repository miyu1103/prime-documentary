#!/usr/bin/env python
"""Resolution/count QC for EP42 Young Codex still images."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
H_AI = Path("E:/pd-media/assets/ai/young")
PUBLIC_IMG = ROOT / "remotion" / "public" / "young" / "img"


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.width, im.height


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-long-edge", type=int, default=3840)
    args = ap.parse_args()

    errors: list[str] = []
    body = [H_AI / f"S{i:02d}.png" for i in range(1, 86)]
    depth = [H_AI / f"S{i:02d}_depth.png" for i in range(1, 86)]
    motion_src = [H_AI / f"M{i:02d}_src.png" for i in range(1, 17)]
    public_body = [PUBLIC_IMG / f"S{i:02d}.png" for i in range(1, 86)]
    public_depth = [PUBLIC_IMG / f"S{i:02d}_depth.png" for i in range(1, 86)]

    for label, paths in {
        "body": body,
        "depth": depth,
        "motion_src": motion_src,
        "public_body": public_body,
        "public_depth": public_depth,
    }.items():
        missing = [str(p) for p in paths if not p.is_file()]
        if missing:
            errors.append(f"{label} missing {len(missing)}")
            errors.extend(f"missing {p}" for p in missing[:10])

    for p in body + motion_src + public_body:
        if not p.is_file():
            continue
        w, h = image_size(p)
        if max(w, h) < args.min_long_edge:
            errors.append(f"long edge below {args.min_long_edge}: {p} ({w}x{h})")

    print(("PASS" if not errors else "FAIL")
          + f" young_stills_qc: body={sum(p.is_file() for p in body)} "
          + f"motion_src={sum(p.is_file() for p in motion_src)} "
          + f"depth={sum(p.is_file() for p in depth)} min_long_edge={args.min_long_edge}")
    for err in errors[:30]:
        print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
