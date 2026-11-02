#!/usr/bin/env python
"""Open up under-exposed episode stills in place, measured per image.

`visual_asset_qc` and `image_cut_luma` both measure the SOURCE stills, and EP51 arrived with
93.4% of 182 stills below the readable floor (median luma < 45) -- the recurring 「画像が暗くて
見えにくい」. A render-time lift fixes what the viewer sees but not what the gates measure, and
leaves the next build guessing, so the correction belongs on the file: each still is measured,
and only the dark ones are lifted, with the original kept beside it.

    python scripts/brighten_dark_stills.py --slug willingham [--target 82] [--dry-run]

Originals are copied to img_original/ before the first write, so this is reversible and never
compounds across runs (an already-processed image measures bright and is skipped).
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFile

# one EP51 still is truncated on disk; a half-read PNG must not stop the whole pass
ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = Path(__file__).resolve().parents[1]


def mean_luma(im: Image.Image) -> float:
    g = im.convert("L").resize((64, 36))
    px = list(g.getdata())
    return sum(px) / len(px)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--target", type=float, default=82.0, help="target mean luma for dark stills")
    ap.add_argument("--floor", type=float, default=62.0, help="only images below this are touched")
    ap.add_argument("--max-gain", type=float, default=2.1)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    img_dir = ROOT / "remotion" / "public" / a.slug / "img"
    if not img_dir.is_dir():
        print(f"[bright] no img dir for {a.slug}")
        return 0
    backup = img_dir.parent / "img_original"
    backup.mkdir(parents=True, exist_ok=True)

    touched, before, after = 0, [], []
    skipped = 0
    for p in sorted(img_dir.glob("*.png")):
        try:
            im = Image.open(p).convert("RGB")
            m = mean_luma(im)
        except Exception as exc:  # noqa: BLE001
            print(f"[bright]   SKIP {p.name} ({exc})")
            skipped += 1
            continue
        before.append(m)
        if m >= a.floor or m <= 1.0:
            after.append(m)
            continue
        gain = min(a.max_gain, a.target / m)
        out = ImageEnhance.Brightness(im).enhance(gain)
        # a pure gain flattens the image, so put a little contrast back
        out = ImageEnhance.Contrast(out).enhance(1.0 + (gain - 1.0) * 0.22)
        after.append(mean_luma(out))
        touched += 1
        if not a.dry_run:
            if not (backup / p.name).exists():
                shutil.copy2(p, backup / p.name)
            out.save(p)

    def med(v):
        v = sorted(v)
        return round(v[len(v) // 2], 1) if v else 0.0

    print(f"[bright] {a.slug}: {touched}/{len(before)} still(s) lifted "
          f"{'(dry run) ' if a.dry_run else ''}| median luma {med(before)} -> {med(after)} "
          f"| below 45: {sum(1 for x in before if x < 45)} -> {sum(1 for x in after if x < 45)}"
          f"{f' | {skipped} unreadable' if skipped else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
