#!/usr/bin/env python3
r"""Is the reserved HEADLINE BAND of a thumbnail plate actually empty?

Why this exists
---------------
`check_thumb_subject_luma.py` measures a FINISHED thumbnail: it wants a tall bright
connected component (the headline) wrapped in a dark outline. Run on a BARE plate --
one commissioned so a headline can be burned in later -- it reports `outline 0px` and
`text height` measured off open sky, because there is no headline yet. Those numbers
are meaningless before compositing and must not be read as a plate defect.

What a bare plate has to prove is the opposite thing: that the band where the headline
will go is EMPTY. This gate measures that, and only that.

What it measures
----------------
The image is reduced to 1280x720 (Lanczos, luma = ITU-R 601 grey) so the numbers do not
depend on the plate's native size, then, inside the band (default: the upper 40% of the
frame = rows 0..287):

  sky_ref        the 90th percentile luma of the band. On an overcast plate this is the
                 sky itself; using a percentile rather than the max ignores specular
                 speckle.
  non_sky_pct    percent of band pixels darker than `sky_ref - 45`. 45 levels is the
                 separation between overcast sky and a bare winter branch against it;
                 it is the same rule the EP66 v001 verdicts published, so the numbers
                 here are directly comparable with that table.
  first_row      the topmost band row in which more than 0.8% of the row's pixels are
                 non-sky, i.e. where an object first cuts into the band. `-` means no
                 row in the band does.
  clear_rows     height in px of the unbroken run of clear rows measured DOWN FROM THE
                 TOP of the frame. This is the usable headline height: the spec wants a
                 150px headline plus a 12px outline, so anything under 174 cannot hold
                 the designed headline no matter where it is placed.
  edge_pct       percent of band pixels whose Sobel-free gradient magnitude
                 (|dx|+|dy|, the same `detail()` energy `qc_delivered_plates.py` uses to
                 keep the telop and caption bands quiet) exceeds 8. Catches soft
                 structure -- a hazy ridge, a colour ramp -- that the 45-level darkness
                 test steps over.
  band_mean/sd   mean and standard deviation of band luma. An unbroken overcast band is
                 bright and flat; sd is the honest version of "is anything in there".

The band is measured with a horizontal SAFE-AREA INSET (default 3% of width off each
side) because these plates carry a lens vignette. Measured without it, L256 reports 203
broken rows starting at row 0 and reads as catastrophically blocked; the pixels
responsible are columns 0 and 1279 at luma 175-206 against a 242 centre, i.e. the corner
falloff, and the band is in fact unbroken sky. A headline is never set into the outer 3%
of a thumbnail, so measuring there only manufactures failures. Set --inset-pct 0 to see
the raw figure.

Thresholds
----------
  non_sky_pct <= 1.00      clear_rows >= 174      edge_pct <= 1.00

Calibration note, and the reason `first_row` is REPORTED but is not a floor: the natural
reading of the order ("nothing whatever entering the upper 40%") would make `first_row is
None` the rule, but L258 -- the one EP66 thumbnail plate that passed human QC on this
exact question -- breaks at row 274 of 288. The v001 verdicts called it a clean PASS
because they measured the upper THIRD (240 rows) and the intrusion sits below that. A
floor stricter than the accepted reference plate would be an invented standard, so the
operative question is the one the band exists to answer: is there an unbroken run of
clear rows down from the top tall enough to burn the designed headline into. That is
`clear_rows >= 174`, and `non_sky_pct` / `edge_pct` confirm that run is genuinely flat
rather than merely un-dark.

This gate is deterministic, reads only numpy + PIL, and writes nothing.

Usage:
  py -3.11 scripts/check_thumb_headline_band.py IMG [IMG ...] [--band-pct 40] [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

REF_W, REF_H = 1280, 720
DARK_DELTA = 45.0          # levels below sky_ref that counts as "not sky"
ROW_HIT_PCT = 0.8          # % of a row's pixels that must be non-sky to call the row broken
EDGE_MAG = 8.0             # |dx|+|dy| above this counts as an edge pixel

MAX_NON_SKY_PCT = 1.00
MAX_EDGE_PCT = 1.00
MIN_CLEAR_ROWS = 174       # 150px headline + 12px outline top and bottom


def measure(path: Path, band_pct: float = 40.0, inset_pct: float = 3.0) -> dict:
    im = Image.open(path).convert("RGB").resize((REF_W, REF_H), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float64)
    g = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

    band_h = int(round(REF_H * band_pct / 100.0))
    inset = int(round(REF_W * inset_pct / 100.0))
    band = g[:band_h, inset:REF_W - inset] if inset else g[:band_h]

    sky_ref = float(np.percentile(band, 90))
    non_sky = band < (sky_ref - DARK_DELTA)
    non_sky_pct = float(non_sky.mean() * 100.0)

    row_pct = non_sky.mean(axis=1) * 100.0
    broken = np.nonzero(row_pct > ROW_HIT_PCT)[0]
    first_row = int(broken[0]) if broken.size else None
    clear_rows = int(broken[0]) if broken.size else band_h

    dy = np.abs(np.diff(band, axis=0))
    dx = np.abs(np.diff(band, axis=1))
    d = np.zeros_like(band)
    d[: dy.shape[0], :] += dy
    d[:, : dx.shape[1]] += dx
    edge_pct = float((d > EDGE_MAG).mean() * 100.0)

    ok = (
        non_sky_pct <= MAX_NON_SKY_PCT
        and clear_rows >= MIN_CLEAR_ROWS
        and edge_pct <= MAX_EDGE_PCT
    )
    return {
        "id": path.stem,
        "band_px": band_h,
        "sky_ref": round(sky_ref, 1),
        "non_sky_pct": round(non_sky_pct, 2),
        "first_row": first_row,
        "clear_rows": clear_rows,
        "edge_pct": round(edge_pct, 2),
        "band_mean": round(float(band.mean()), 1),
        "band_sd": round(float(band.std()), 1),
        "ok": bool(ok),
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+")
    ap.add_argument("--band-pct", type=float, default=40.0)
    ap.add_argument("--inset-pct", type=float, default=3.0,
                    help="safe-area inset off each side, %% of width (0 = raw)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = [measure(Path(p), args.band_pct, args.inset_pct) for p in args.images]
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print(f"band = upper {args.band_pct:g}% of a 1280x720 reduction "
              f"({rows[0]['band_px']}px), {args.inset_pct:g}% safe-area inset each side\n"
              f"floors: non_sky<={MAX_NON_SKY_PCT} clear_rows>={MIN_CLEAR_ROWS} "
              f"edge<={MAX_EDGE_PCT}   (first_row: reported, not a floor)")
        print(f"{'id':<8}{'skyref':>7}{'nonsky%':>9}{'1st row':>9}{'clear':>7}"
              f"{'edge%':>8}{'mean':>7}{'sd':>7}  verdict")
        for r in rows:
            fr = "-" if r["first_row"] is None else str(r["first_row"])
            print(f"{r['id']:<8}{r['sky_ref']:>7.1f}{r['non_sky_pct']:>9.2f}{fr:>9}"
                  f"{r['clear_rows']:>7}{r['edge_pct']:>8.2f}{r['band_mean']:>7.1f}"
                  f"{r['band_sd']:>7.1f}  {'PASS' if r['ok'] else 'FAIL'}")
    return 0 if all(r["ok"] for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
