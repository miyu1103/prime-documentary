#!/usr/bin/env python
"""Stage EP45 Cleveland generated media into remotion/public without overwriting."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AI = Path("H:/pd-media/assets/ai/cleveland")
MOTION = Path("H:/pd-media/assets/ai_video/cleveland")
PUBLIC = ROOT / "remotion" / "public" / "cleveland"


def copy_missing(src: Path, dst: Path) -> bool:
    if not src.is_file() or dst.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def main() -> int:
    made = 0
    for i in range(1, 85):
        stem = f"S{i:02d}"
        made += int(copy_missing(AI / f"{stem}.png", PUBLIC / "img" / f"{stem}.png"))
        made += int(copy_missing(AI / f"{stem}_depth.png", PUBLIC / "img" / f"{stem}_depth.png"))
    for i in range(1, 17):
        made += int(copy_missing(MOTION / f"M{i:02d}_rife.mp4", PUBLIC / "motion" / f"M{i:02d}_rife.mp4"))
    print(f"staged_missing={made} public={PUBLIC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

