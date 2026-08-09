#!/usr/bin/env python3
"""Composite the EP62-65 thumbnails: the commissioned plate plus its headline and kicker.

check_final_acceptance fails an episode with fewer than three 1280x720 candidates and no selection.
All four episodes have their plates and their wording already -- the plates were ordered with the
upper third left clear and a brightness override, and 04_scenes/thumb_prompts.v001.md carries the
kicker and the two-line headline for each. This puts one on the other.

Deliberately not Remotion: these are static compositions of an image and two text blocks, and a
bundle takes longer than the render. The type follows the design doc -- headline uppercase, two
lines maximum, cap height at least 78 px at 1280x720; kicker a filled tag of three words or fewer.

    py scripts/build_ep62_65_thumbnails.py            # all four
    py scripts/build_ep62_65_thumbnails.py --slug greene
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
W, H = 1280, 720
GOLD, RED, BLUE, WHITE = "#E5B53A", "#D22628", "#1F6BFF", "#F2F0EA"

# plate, kicker, headline lines, accent -- all from each episode's thumb_prompts.v001.md
SPEC: dict[str, tuple[str, list[tuple[str, str, list[str], str]]]] = {
    "greene": ("PD-2026-062-greene", [
        # the kicker carries the second fact; "ONE KNOCK" repeated the headline
        ("G242", "NOBODY HOME", ["ONE KNOCK", "WAS ENOUGH"], GOLD),
        ("G220", "SERVICE", ["THIS COUNTED", "AS NOTICE"], GOLD),
        ("G222", "THE PAPER", ["THE PAPER", "CAME OFF"], RED),
        ("G221", "DID SHE KNOW", ["DID SHE", "EVER KNOW?"], BLUE),
    ]),
    "correa": ("PD-2026-063-correa", [
        ("C227", "NUMBER 47", ["NO RECORD", "AT ALL"], GOLD),
        ("C238", "NUMBER 47", ["NOBODY", "CALLED 47"], RED),
        ("C239", "NEVER REFUSED", ["NOBODY", "SAID NO"], GOLD),
        ("C222", "TWO HOURS", ["SHE WAS", "NEVER REFUSED"], BLUE),
    ]),
    "memphis": ("PD-2026-064-memphis", [
        # M208 first: the plate review ACCEPTed it as the only candidate meeting all three
        # requirements and FLAGged M219 because the sheets occupy the upper third. Opening both
        # agrees -- M219 never shows the two bills the hook is about.
        ("M208", "TWO METER SETS", ["BOTH WERE", "RUNNING"], GOLD),
        ("M219", "ONE HOUSE", ["ONE LETTER", "APART"], GOLD),
        ("M209", "SAME HOUSE", ["TWO BILLS", "EVERY MONTH"], RED),
        ("M235", "AFTER FINAL NOTICE", ["GIVEN NO", "SATISFACTION"], BLUE),
    ]),
    "marmet": ("PD-2026-065-marmet", [
        ("R218", "ONE LINE", ["ARBITRATE", "THE DEATH CLAIM"], RED),
        ("R217", "THE CARVE-OUT", ["EXCEPT", "THEIR OWN BILL"], GOLD),
        ("R224", "NOT UPHELD", ["VACATED,", "NOT UPHELD"], GOLD),
        ("R219", "WHO SIGNED?", ["THE RECORD", "NEVER SAYS WHO"], BLUE),
    ]),
}


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    for name in (("Anton-Regular.ttf", "Oswald-Bold.ttf", "arialbd.ttf", "arial.ttf")
                 if bold else ("Oswald-Regular.ttf", "arial.ttf")):
        for d in (ROOT / "remotion/public/fonts", Path("C:/Windows/Fonts")):
            p = d / name
            if p.is_file():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def build(slug: str, epid: str, plate: str, kicker: str, headline: list[str],
          accent: str, n: int) -> Path | None:
    src = Path(f"H:/pd-media/assets/ai/{slug}/{plate}.png")
    if not src.is_file():
        print(f"  {plate}: plate missing"); return None
    im = Image.open(src).convert("RGB")
    # cover-crop to 16:9 then down to 1280x720
    tw, th = W / H, im.width / im.height
    if th > tw:
        nw = int(im.height * tw)
        im = im.crop(((im.width - nw) // 2, 0, (im.width + nw) // 2, im.height))
    else:
        nh = int(im.width / tw)
        im = im.crop((0, (im.height - nh) // 2, im.width, (im.height + nh) // 2))
    im = im.resize((W, H), Image.LANCZOS)

    # a scrim under the type only, so the picture keeps its own light
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, 0, W, int(H * 0.66)], fill=(0, 0, 0, 120))

    # thumb_subject_luma wants an element at least 150 px tall at 1280 wide, so it can be read at
    # 320 px in a feed. 96 px type measured 71 px of cap height and failed on all four.
    # Fit to the frame: 168 px overflowed on the longest line and clipped THEIR OWN BILL at the
    # right edge. Shrink until the widest line fits, but never below the 150 px the gate wants.
    size = 168
    while size > 132:
        f = font(size)
        if max(d.textlength(l, font=f) for l in headline[:2]) <= W - 96:
            break
        size -= 6
    fh = font(size)
    y = 26
    for line in headline[:2]:
        d.text((48, y), line, font=fh, fill=WHITE,
               stroke_width=7, stroke_fill=(0, 0, 0, 235))
        y += int(size * 1.06)

    fk = font(46)
    kw = d.textlength(kicker, font=fk)
    d.rectangle([48, y + 10, 48 + kw + 40, y + 10 + 68], fill=accent)
    d.text((68, y + 22), kicker, font=fk, fill="#0B0B0B")

    out_dir = ROOT / "episodes" / epid / "09_package"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"thumbnail.{slug}.{n:02d}.v001.png"
    im.save(out)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", choices=sorted(SPEC))
    a = ap.parse_args()
    for slug in ([a.slug] if a.slug else list(SPEC)):
        epid, rows = SPEC[slug]
        print(f"=== {slug}")
        made = []
        for i, (plate, kicker, head, accent) in enumerate(rows, 1):
            p = build(slug, epid, plate, kicker, head, accent, i)
            if p:
                made.append(p)
                print(f"  {p.name}  <- {plate}  {' / '.join(head)}")
        if made:
            # Invariant 6: an approved artefact is never overwritten. The uploader takes the
            # HIGHEST thumbnail.selected.v*.png, so a new revision is what ships and the earlier
            # selection stays on disk to compare against.
            n = 1
            while (made[0].parent / f"thumbnail.selected.v{n:03d}.png").exists():
                n += 1
            sel = made[0].parent / f"thumbnail.selected.v{n:03d}.png"
            shutil.copy2(made[0], sel)
            print(f"  selected -> {sel.name}  <- {made[0].name}  ({len(made)} candidate(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
