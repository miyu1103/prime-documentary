#!/usr/bin/env python3
"""Build labelled contact sheets of an episode's generated plates, so a person can look at them.

Why this exists: `episode_spec.footage_review_required` is true and every image order in this
repository ends with the same instruction -- build a labelled contact sheet and have a person open
it. Nothing built one. `make_contact_sheets.py` produces one montage per plate, which is a
different thing: 120 files nobody opens. `check_plate_verdicts.py` reads a verdict file it cannot
produce, and its own docstring says it never looks at an image.

The cost of not looking is on the record. EP64 memphis shipped with sixteen REJECTED plates cut
into the film and was pulled hours later. EP66's round pole, tailgate wordmark and fused fingers
all reached a re-order because a per-batch sign-off cleared eight plates at once. The four things
a reviewer is looking for are the four blocking classes, and none of them is detectable by any
tool in this pipeline: a body, a real face, a legible glyph, signage from the wrong country.

    py -3.11 scripts/build_plate_contact_sheet.py --slug itaewon
    py -3.11 scripts/build_plate_contact_sheet.py --slug itaewon --per-sheet 12 --cell 640x360

Writes sheets to runs/qc/plate_sheets/<slug>/ and prints the paths. Nothing else.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BG = (14, 16, 20)
FG = (232, 234, 238)
LABEL_H = 26
PAD = 8


def _font(size: int):
    for name in ("arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:  # noqa: BLE001
            continue
    return ImageFont.load_default()


def build(slug: str, per_sheet: int, cell: tuple[int, int], cols: int,
          src_dir: str | None = None) -> list[Path]:
    # --src lets a batch be reviewed BEFORE it is staged. Added 2026-08-21 for EP76: Codex
    # delivered 115 of 120 plates and deliberately did not stage them, so that a partial set could
    # not be mistaken for render truth. Reviewing only what is already staged would have meant
    # staging first and looking second, which is the wrong order.
    src = Path(src_dir) if src_dir else ROOT / "remotion" / "public" / slug / "img"
    plates = sorted(p for p in src.glob("*.png") if "_depth" not in p.name)
    if not plates:
        print(f"no plates under {src}")
        return []

    out_dir = ROOT / "runs" / "qc" / "plate_sheets" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    cw, ch = cell
    font = _font(17)
    title_font = _font(21)
    written: list[Path] = []

    for start in range(0, len(plates), per_sheet):
        chunk = plates[start:start + per_sheet]
        rows = (len(chunk) + cols - 1) // cols
        W = cols * cw + (cols + 1) * PAD
        H = 44 + rows * (ch + LABEL_H + PAD) + PAD
        sheet = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(sheet)
        n = start // per_sheet + 1
        total = (len(plates) + per_sheet - 1) // per_sheet
        d.text((PAD, 12), f"{slug}  plates {chunk[0].stem}-{chunk[-1].stem}"
                          f"   sheet {n}/{total}   "
                          f"look for: a body / a real face / a legible glyph / wrong-country signage",
               font=title_font, fill=FG)

        for i, p in enumerate(chunk):
            r, c = divmod(i, cols)
            x = PAD + c * (cw + PAD)
            y = 44 + r * (ch + LABEL_H + PAD)
            try:
                im = Image.open(p).convert("RGB")
            except Exception as e:  # noqa: BLE001
                d.text((x, y), f"{p.stem}  UNREADABLE {e}", font=font, fill=(255, 90, 95))
                continue
            im.thumbnail((cw, ch), Image.LANCZOS)
            sheet.paste(im, (x + (cw - im.width) // 2, y + (ch - im.height) // 2))
            d.text((x + 2, y + ch + 4), p.stem, font=font, fill=FG)

        out = out_dir / f"{slug}_plates_{n:02d}.png"
        sheet.save(out)
        written.append(out)
        print(f"[ok] {out}  ({len(chunk)} plates)")

    return written


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--per-sheet", type=int, default=12)
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--cell", default="620x349")
    ap.add_argument("--src", help="review a batch BEFORE it is staged: read plates from this "
                                  "directory instead of remotion/public/<slug>/img")
    a = ap.parse_args()
    w, h = (int(v) for v in a.cell.lower().split("x"))
    sheets = build(a.slug, a.per_sheet, (w, h), a.cols, a.src)
    if not sheets:
        return 1
    print(f"\n{len(sheets)} sheet(s). OPEN THEM. A tool cannot do this part -- "
          f"check_plate_verdicts.py says so in its own docstring.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
