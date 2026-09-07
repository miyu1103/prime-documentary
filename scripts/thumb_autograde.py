#!/usr/bin/env python
"""Deterministic colour grade that moves a near-miss thumbnail plate into the punch bands.

WHY THIS EXISTS. On 2026-08-24 the EP77-82 thumbnail order stopped at its first gate:
six Codex attempts at keybridge THUMB-01 all failed check_thumb_punch.py, and the receipt
(EP77-82_THUMB_CODEX.v003.blocked_receipt.json) offered "deterministic local color grading
of gate02" as one of three ways forward. gate02 missed on exactly one band (contrast 57.6
against a floor of 60.0) and passed the other four. Regenerating a whole image to fix a
2.4-point contrast deficit is waste; a reproducible curve is not.

The grade is a grid search over PIL contrast/brightness factors (both bounded, both
recorded). The output is written ONLY if every band in check_thumb_punch.BANDS passes,
and the receipt line printed at the end carries the factors and the measured metrics so
the operation can be re-run bit-for-bit.

    py -3.11 scripts/thumb_autograde.py <input.png> --output <graded.png>
    py -3.11 scripts/thumb_autograde.py <input.png> --output <graded.png> --dry-run

WHAT IT CANNOT DO. It measures light, not meaning (same limit as check_thumb_punch.py).
It also cannot rescue a plate that is far outside the bands: the factor grid is
deliberately narrow (0.85-1.30) so it can only finish a near-miss, never invent punch
that the generation does not have. A plate needing more than that goes back to Codex.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_thumb_punch import BANDS, measure, verdict  # noqa: E402

CONTRAST_GRID = [round(0.85 + 0.025 * i, 3) for i in range(19)]  # 0.85 .. 1.30
BRIGHTNESS_GRID = [round(0.90 + 0.025 * i, 3) for i in range(13)]  # 0.90 .. 1.20


def band_distance(m: dict) -> float:
    """Sum of normalised distances outside each band. 0.0 means all bands pass."""
    d = 0.0
    for k, (lo, hi) in BANDS.items():
        v = m[k]
        if v < lo:
            d += (lo - v) / (hi - lo)
        elif v > hi:
            d += (v - hi) / (hi - lo)
    return d


def grade(src: Path, out: Path, dry_run: bool, force: bool) -> int:
    from PIL import Image, ImageEnhance

    if out.exists() and not force and not dry_run:
        print(f"REFUSE: {out} exists (use --force)")
        return 2

    im = Image.open(src).convert("RGB")
    best: tuple[float, float, float, dict] | None = None
    for cf, bf in itertools.product(CONTRAST_GRID, BRIGHTNESS_GRID):
        candidate = ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(cf)).enhance(bf)
        tmp = out.with_suffix(".tmp_measure.png")
        candidate.save(tmp)
        m = measure(tmp)
        tmp.unlink()
        d = band_distance(m)
        # Prefer a pass; among passes prefer the smallest departure from the original.
        departure = abs(cf - 1.0) + abs(bf - 1.0)
        key = (0.0 if d == 0.0 else 1.0, d, departure)
        if best is None or key < (0.0 if best[3]["_dist"] == 0.0 else 1.0, best[3]["_dist"], abs(best[0] - 1.0) + abs(best[1] - 1.0)):
            m["_dist"] = d
            best = (cf, bf, departure, m)
            if d == 0.0 and departure <= 0.15:
                break

    assert best is not None
    cf, bf, _, m = best
    passed = m["_dist"] == 0.0
    metrics = {k: round(v, 2) for k, v in m.items() if not k.startswith("_")}
    receipt = {
        "input": str(src),
        "output": str(out),
        "contrast_factor": cf,
        "brightness_factor": bf,
        "metrics": metrics,
        "verdict": "pass" if passed else "fail",
        "residual": verdict({k: v for k, v in m.items() if not k.startswith("_")}),
    }
    print(json.dumps(receipt, indent=2))
    if not passed:
        print("FAIL: no factor pair in the bounded grid passes all bands. Back to generation.")
        return 1
    if dry_run:
        print("DRY-RUN: not written.")
        return 0
    final = ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(cf)).enhance(bf)
    tmp_out = out.with_suffix(".tmp_write.png")
    final.save(tmp_out)
    tmp_out.replace(out)
    print(f"WROTE {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if not a.input.exists():
        print(f"missing input: {a.input}")
        return 2
    return grade(a.input, a.output, a.dry_run, a.force)


if __name__ == "__main__":
    raise SystemExit(main())
