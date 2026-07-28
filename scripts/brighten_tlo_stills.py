#!/usr/bin/env python
"""Raise EP46 TLO still median luma enough to pass the visual QC floor."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
AI_DIR = Path("H:/pd-media/assets/ai/tlo")
PUBLIC_IMG = ROOT / "remotion" / "public" / "tlo" / "img"
FLOOR = 45.0
TARGET = 58.0


def median_luma(path: Path) -> float:
    with Image.open(path) as im:
        arr = np.asarray(im.convert("L").resize((64, 64)), dtype=np.float64)
    return float(np.median(arr))


def paired_paths() -> list[tuple[Path, Path]]:
    names = [f"S{i:02d}.png" for i in range(1, 85)] + [f"M{i:02d}_src.png" for i in range(1, 17)]
    pairs: list[tuple[Path, Path]] = []
    for name in names:
        src = AI_DIR / name
        pub = PUBLIC_IMG / name
        if not src.is_file() or not pub.is_file():
            raise FileNotFoundError(f"missing still pair: {src} / {pub}")
        pairs.append((src, pub))
    return pairs


def backup_once(path: Path, backup_root: Path) -> None:
    rel = path.name
    dst = backup_root / rel
    if not dst.exists():
        shutil.copy2(path, dst)


def brighten(path: Path, factor: float) -> None:
    with Image.open(path) as im:
        out = ImageEnhance.Brightness(im.convert("RGB")).enhance(factor)
    out.save(path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()

    rows = []
    pairs = paired_paths()
    for src, pub in pairs:
        before = median_luma(pub)
        if before < FLOOR:
            factor = min(2.4, max(1.05, TARGET / max(before, 1.0)))
            rows.append((src, pub, before, factor))

    if not args.run:
        print(json.dumps({"dark_count": len(rows), "planned": [{"name": p.name, "luma": round(l, 1), "factor": round(f, 3)} for _, p, l, f in rows]}, ensure_ascii=False, indent=2))
        return 0

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_ai = AI_DIR / f"_pre_luma_fix_{stamp}"
    backup_public = PUBLIC_IMG / f"_pre_luma_fix_{stamp}"
    backup_ai.mkdir(parents=True, exist_ok=False)
    backup_public.mkdir(parents=True, exist_ok=False)

    changed = []
    for src, pub, before, factor in rows:
        backup_once(src, backup_ai)
        backup_once(pub, backup_public)
        brighten(src, factor)
        brighten(pub, factor)
        after = median_luma(pub)
        changed.append({"name": pub.name, "before": round(before, 1), "after": round(after, 1), "factor": round(factor, 3)})

    print(json.dumps({
        "changed": len(changed),
        "backup_ai": str(backup_ai),
        "backup_public": str(backup_public),
        "items": changed,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
