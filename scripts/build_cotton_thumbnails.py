# -*- coding: utf-8 -*-
"""Build 3 EP30 thumbnails (1280x720) from hero stills + bold headline, + a selected.

Passes thumbnail_ready (>=3 @1280x720 + 09_package/thumbnail.selected*.png) and aims
at thumbnail_visibility (mean luma >=33, contrast >=40) via a brightened hero crop +
huge white headline over a dark bottom scrim + gold accent. Not the final Codex art,
but a real, legible, on-brand thumbnail set.
"""
from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEL = "H:/pd-media/episodes/PD-2026-030-cotton/05_visuals/selected"
TDIR = ROOT / "episodes" / "PD-2026-030-cotton" / "10_thumbnail"
PKG = ROOT / "episodes" / "PD-2026-030-cotton" / "09_package"
FONT_SRC = Path("C:/Windows/Fonts/arialbd.ttf")
FONT = "_font.ttf"  # copied next to cwd (TDIR) so the drive-colon can't clash with drawtext option separators

# (hero image, headline, y-position). Headlines: UPPERCASE, <=4 words.
PLAN = [
    ("EP30-IMG-002.png", "SHE WAS SURE.", 1),
    ("EP30-IMG-005.png", "WRONG FACE", 2),
    ("EP30-IMG-011.png", "MEMORY LIED", 3),
]


def build(src: Path, out: Path, headline: str) -> bool:
    # scale to cover 1280x720, crop, brighten, dark bottom scrim, gold rule, huge white headline
    vf = (
        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
        "eq=brightness=0.08:contrast=1.12:saturation=1.05,"
        "drawbox=x=0:y=470:w=1280:h=250:color=black@0.55:t=fill,"
        "drawbox=x=90:y=512:w=150:h=10:color=0xE5B53A@0.95:t=fill,"
        f"drawtext=fontfile={FONT}:text='{headline}':x=(w-text_w)/2:y=560:"
        "fontsize=120:fontcolor=white:borderw=6:bordercolor=black@0.85:shadowx=4:shadowy=4:shadowcolor=black@0.6"
    )
    r = subprocess.run(["ffmpeg", "-y", "-i", str(src), "-vf", vf, "-frames:v", "1", str(out)],
                       capture_output=True, text=True, cwd=str(TDIR))
    if r.returncode != 0:
        print(f"  FAIL {out.name}: {r.stderr[-300:]}")
        return False
    return True


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    TDIR.mkdir(parents=True, exist_ok=True)
    PKG.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FONT_SRC, TDIR / FONT)  # colon-free font next to cwd
    made = []
    for i, (img, head, _y) in enumerate(PLAN, 1):
        src = Path(SEL) / img
        if not src.exists():
            print(f"  MISS hero {img}")
            continue
        out = TDIR / f"thumb.v{i:03d}.png"
        if build(src, out, head):
            made.append(out)
            print(f"  wrote {out.relative_to(ROOT)}  ('{head}')")
    if made:
        shutil.copy2(made[0], PKG / "thumbnail.selected.v001.png")
        print(f"  selected -> 09_package/thumbnail.selected.v001.png ({PLAN[0][1]})")
    print(f"done: {len(made)} thumbnails")
    return 0 if len(made) >= 3 else 1


if __name__ == "__main__":
    raise SystemExit(main())
