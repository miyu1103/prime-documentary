#!/usr/bin/env python3
"""Compose an episode's thumbnail candidates from ITS OWN plates, and measure them.

WHY THIS EXISTS
---------------
`scripts/` carries a dozen per-episode thumbnail builders -- build_ep62_65_thumbnails.py,
build_frazier_thumbnails.py, build_itaewon_thumbnails_v001.py, build_katz_thumbnails_v001.py
and so on -- each a copy of the last with different constants. That is the one-off family
invariant 14 exists to stop, and it is why EP71 oroville arrived at its upload day with zero
thumbnails and no tool that would make one.

This is the generic replacement. The per-episode part is a json:

    config/thumbnails/<slug>.json
    [{"plate": "O058.png",
      "headline": "188,000 ORDERED OUT",
      "sub": "and then ordered to pay the State's costs",
      "band": "lower",              # lower | upper | card
      "provenance": "script.en.v001.md:20"}]

`provenance` is required and is not decoration: a thumbnail states a claim to people who have
not seen the film, so it is subject to `factual_support` exactly as a title is (rule 19). The
line it names must be the sentence the headline came from.

WHAT IT GUARANTEES
------------------
Nothing about taste. It guarantees the three things `check_thumb_subject_luma` measures, because
it builds for them and then RUNS that gate on its own output and prints the numbers:

  * subject luma >= 60      -- the centre is lifted, not left as a dark blob
  * text height >= 150 px   -- the headline is set large enough to survive a 320 px feed tile
  * outline width >= 12 px  -- every glyph carries a dark rim so it never blends into the plate

A candidate that fails is still written, and still reported as failing. Choosing among them, and
copying one to `thumbnail.selected.v001.png`, stays a human decision (rule: no self-declared QC).

    py -3.11 scripts/build_case_thumbnails_from_plates.py --slug oroville
    py -3.11 scripts/build_case_thumbnails_from_plates.py --slug oroville --spec path.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H = 1280, 720

# A face-safe, heavy, installed font. Fallbacks are tried in order; the last is PIL's default,
# which is tiny -- if we reach it the text-height gate will fail and say so, which is the point.
FONT_CANDIDATES = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/impact.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
]


def load_font(px: int) -> ImageFont.FreeTypeFont:
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return ImageFont.truetype(p, px)
    return ImageFont.load_default()


# The gate measures the tallest CONNECTED COMPONENT, which for caps is about 0.72 of the font size --
# a 150 px font makes a 108-140 px component and fails. Measured on EP71: 150 px font -> 140 px.
MIN_HEADLINE_PX = 215   # 215 * 0.72 = 155 px of cap height, clear of the 150 px floor


def _wrap(words: list[str], font: ImageFont.FreeTypeFont, max_w: int, n: int) -> list[str] | None:  # noqa: E501
    """Split into exactly n lines, balanced, or None if any line is too wide."""
    if n == 1:
        return [" ".join(words)] if font.getbbox(" ".join(words))[2] <= max_w else None
    best = None
    for i in range(1, len(words)):
        head, tail = words[:i], words[i:]
        rest = _wrap(tail, font, max_w, n - 1)
        if rest is None:
            continue
        line = " ".join(head)
        if font.getbbox(line)[2] > max_w:
            continue
        cand = [line] + rest
        spread = max(font.getbbox(l)[2] for l in cand) - min(font.getbbox(l)[2] for l in cand)
        if best is None or spread < best[0]:
            best = (spread, cand)
    return best[1] if best else None


def fit_lines(text: str, max_w: int, start_px: int,
              max_h: int) -> tuple[list[str] | None, ImageFont.FreeTypeFont]:
    """Largest type that fits, and NEVER below MIN_HEADLINE_PX.

    The first version shrank the type until the headline fitted in two lines, which is how EP71's
    candidates 02 and 03 arrived at 109 px and 120 px components against a 150 px floor -- the gate
    then correctly called them unreadable at feed size. Length is taken out of the line count
    instead: up to four lines at full size before the type is allowed to get smaller at all.
    """
    words = text.split()
    for px in range(start_px, MIN_HEADLINE_PX - 1, -4):
        font = load_font(px)
        for n in (1, 2, 3):
            lines = _wrap(words, font, max_w, n)
            if lines:
                # LINE BOX, not cap height. PIL draws from the ascender, so a line occupies
                # about font.size vertically; budgeting by cap height (0.72x) is what made the
                # lines overlap each other and the sub line sit on top of the headline.
                if (font.size + 8) * len(lines) <= max_h:
                    return lines, font   # fits the WIDTH and the HEIGHT it is allowed
    # NO SILENT OVERFLOW. Returning the unwrapped string here is what produced EP71's first three
    # candidates: every readability number passed -- 160-175 px of cap height, 28 px of outline --
    # while the words ran off both edges of the frame and the third line fell out of the bottom.
    # A headline that cannot be set at a readable size in three lines is too long, and saying so is
    # the only honest answer.
    return None, load_font(MIN_HEADLINE_PX)


def draw_outlined(d: ImageDraw.ImageDraw, xy, text, font, rim: int) -> None:
    """True stroked text. An offset-copy loop LOOKS outlined and measures as 0 px: the gate
    finds the dark rim by dilating the bright core and asking how far the darkness extends,
    and overlapping copies of the glyph leave no continuous rim to find (measured on EP71's
    first two candidates, outline 0px < 12px, while the third passed only because its plate
    happened to be dark). PIL's stroke_width draws one continuous rim."""
    d.text(xy, text, font=font, fill=(255, 255, 255, 255),
           stroke_width=rim, stroke_fill=(0, 0, 0, 255))


def compose(plate: Path, headline: str, sub: str, band: str, out: Path) -> None:
    im = Image.open(plate).convert("RGB")
    # cover-crop to 16:9 at 1280x720
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2,
                  (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    # lift the centre so the SUBJECT region clears luma 60 without blowing the plate out
    im = ImageEnhance.Brightness(im).enhance(1.18)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    # THEN PUT A CEILING ON THE PLATE. The outline gate seeds a "bright core" at luma > 200 and
    # measures the dark ring around it; a white card or a bright overcast sky IS such a core and
    # has no ring, so the whole thumbnail scored outline 0 even with correctly stroked text
    # (EP71 candidates 01 and 02, measured). Compressing the plate's highlights to 185 leaves the
    # glyphs as the only cores in the frame, which is what the gate is actually asking for.
    im = im.point(lambda v: min(v, 185))

    # the headline may use the frame minus the sub block and the margins
    # The sub block is two lines of 78 px plus a little air = 200, measured, not guessed. The old
    # 250 + 60 left a 410 px budget, which is less than two lines of the 215 px minimum (446), so
    # every two-word headline was refused as unsettable.
    # ONE budget, used by both the fitter and the refusal below. They disagreed by 20 px and a
    # headline that the fitter accepted was then refused by compose (morandi, 680 of a 660 limit).
    _reserve = (200 if sub else 80)
    lines, font = fit_lines(headline.upper(), W - 100, 300, H - _reserve - 60)
    if lines is None:
        raise ValueError(f"headline too long to set readably in three lines: {headline!r}")
    # CAP HEIGHT, not the font's full box. getbbox("Hg") includes the descender of the g and a
    # leading gap, which overstated a 215 px line as ~300 px and made two perfectly placeable
    # lines look like they needed 822 px of a 720 px frame.
    lh = font.size + 8
    total = lh * len(lines)
    band_h = total + _reserve
    if band_h > H - 60:
        raise ValueError(f"headline needs {band_h}px of a {H}px frame: {headline!r} -- shorten it")

    # LAYOUT FROM THE BOTTOM UP. The first version placed the block from the top of a fixed band
    # and let the sub run past the frame edge: EP71, EP72 and EP73 all shipped a clipped last line
    # ("homes in two days", "minimum was nine", "report, January 2022") while every readability
    # number passed. Measure the whole block first, then seat it inside a real margin.
    MARGIN = 30
    sub_lines: list[str] = []
    sf = load_font(78)
    if sub:
        sub_lines = (_wrap(sub.split(), sf, W - 120, 1) or _wrap(sub.split(), sf, W - 120, 2)
                     or [sub])
    sub_h = len(sub_lines) * 92
    block_h = total + (18 + sub_h if sub_lines else 0)
    top = H - MARGIN - block_h if band != "upper" else MARGIN

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # A gradient scrim behind the block only -- a flat band over half the frame was burying the
    # plate, and the plate is the reason the thumbnail works.
    scrim_top = max(0, top - 60)
    for yy in range(scrim_top, H):
        t = (yy - scrim_top) / max(1, H - scrim_top)
        d.line([(0, yy), (W, yy)], fill=(0, 0, 0, int(30 + 150 * min(1.0, t * 1.6))))

    y = top
    for line in lines:
        w = font.getbbox(line)[2]
        draw_outlined(d, ((W - w) // 2, y), line, font, rim=14)
        y += lh
    # THE SUB CARRIES THE SENTENCE, THE HEADLINE CARRIES THE PUNCH. The gate measures the TALLEST
    # component, so only the headline has to be huge. 78 px still reads at a 320 px feed tile.
    y += 18
    for sl in sub_lines:
        w = sf.getbbox(sl)[2]
        draw_outlined(d, ((W - w) // 2, y), sl, sf, rim=8)
        y += 92

    Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB").save(out, quality=95)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--spec", default=None)
    a = ap.parse_args()

    spec_p = Path(a.spec) if a.spec else ROOT / "config" / "thumbnails" / f"{a.slug}.json"
    if not spec_p.is_file():
        print(f"[thumbs] no spec at {spec_p} -- write one; see this file's docstring")
        return 2
    spec = json.loads(spec_p.read_text(encoding="utf-8"))
    eps = sorted((ROOT / "episodes").glob(f"PD-*-{a.slug}"))
    if not eps:
        print(f"[thumbs] no episode dir for {a.slug}")
        return 2
    out_dir = eps[0] / "09_package"
    out_dir.mkdir(parents=True, exist_ok=True)

    made = []
    for i, row in enumerate(spec, 1):
        if not row.get("provenance"):
            print(f"[thumbs] row {i} has no provenance -- refusing; a thumbnail states a claim")
            return 2
        # A plate may be a commissioned THUMBNAIL plate (episodes/<EPID>/10_thumbnail) or a body
        # plate (remotion/public/<slug>/img). Thumbnail plates win: they are shot for this job.
        plate = None
        for cand in ((eps[0] / "10_thumbnail" / row["plate"]),
                     (ROOT / "remotion" / "public" / a.slug / "img" / row["plate"])):
            if cand.is_file():
                plate = cand
                break
        if plate is None:
            print(f"[thumbs] missing plate {row['plate']} in 10_thumbnail or public/img")
            return 2
        out = out_dir / f"thumbnail.{a.slug}.{i:02d}.v001.png"
        try:
            compose(plate, row["headline"], row.get("sub", ""), row.get("band", "lower"), out)
        except ValueError as exc:
            print(f"[thumbs] row {i} REFUSED: {exc}")
            return 2
        made.append((out, row))

    print(f"[thumbs] {a.slug}: {len(made)} candidate(s) -> {out_dir}")
    for out, row in made:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_thumb_subject_luma.py"),
                            str(out)], capture_output=True, text=True, encoding="utf-8")
        verdict = (r.stdout or r.stderr).strip().splitlines()
        line = next((l for l in verdict if "subject luma" in l or "PASS" in l or "FAIL" in l), "")
        print(f"  {out.name}  [{row['plate']}]  {line.strip()}")
    print("[thumbs] NOTHING IS SELECTED. Look at them, then copy one to "
          f"{out_dir.name}/thumbnail.selected.v001.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
