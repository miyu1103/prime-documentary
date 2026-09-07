#!/usr/bin/env python
"""Technical QC for EP54 Flowers still assets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
QC = ROOT / "episodes" / "PD-2026-054-flowers" / "05_visuals" / "still_qc.v001.json"
MEDIA = Path("E:/pd-media/assets/ai/flowers")


def expected_ids() -> list[str]:
    return [f"S{i:03d}" for i in range(1, 211)] + [f"M{i:02d}_src" for i in range(1, 45)] + [f"T{i:02d}_face" for i in range(1, 4)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-resolution", action="store_true")
    args = ap.parse_args()
    errors: list[str] = []
    data = json.loads(QC.read_text(encoding="utf-8")) if QC.is_file() else {}
    rows = {x.get("asset_id"): x for x in data.get("assets", [])}
    for aid in expected_ids():
        p = MEDIA / f"{aid}.png"
        if not p.is_file():
            errors.append(f"missing {aid}")
            continue
        if aid not in rows:
            errors.append(f"{aid} missing from still_qc")
        if args.check_resolution:
            with Image.open(p) as im:
                if max(im.size) < 3840:
                    errors.append(f"{aid} long edge below 3840 {im.size}")
    counts = data.get("counts", {})
    if counts.get("body") != 210 or counts.get("i2v_source") != 44 or counts.get("thumb_face") != 3:
        errors.append(f"bad still_qc counts {counts}")
    if counts.get("technical_errors") != 0:
        errors.append(f"technical_errors {counts.get('technical_errors')}")
    if counts.get("phash_pairs_ge_0_90") != 0:
        errors.append(f"phash_pairs_ge_0_90 {counts.get('phash_pairs_ge_0_90')}")
    if counts.get("visual_reviewed") != 257:
        errors.append(f"visual_reviewed {counts.get('visual_reviewed')}")
    print(f"{'PASS' if not errors else 'FAIL'} flowers_stills_qc checked=257 errors={len(errors)}")
    for err in errors[:80]:
        print("  !", err)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
