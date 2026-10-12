#!/usr/bin/env python3
r"""EP35 hinders (IRS structuring / civil forfeiture) FLASHY CTR thumbnails v001.

Adapted from build_forfeiture_thumbnails_v003.py (same civil-forfeiture theme, owner:
"サムネは派手に"). Bright high-contrast hero + RED radial burst behind the headline,
a GIANT glowing gold shock number ($32,820), XL black-stroked headline, solid red
kicker tag, gold underline, PD mark. 3 directions + auto-selected. 1280x720 PNG.

Anonymity (invariant 11): heroes are hands / silhouette / storefront -- no real-person
likeness. Carole Hinders is never named or shown.

    PYTHONUTF8=1 py -3.11 scripts/build_hinders_thumbnails_v001.py

Directions:
  A  empty diner / owner silhouette  ->  "SHE LOST / EVERYTHING"      (human loss)
  B  hands at the register + $32,820 ->  "SEIZED BY / THE IRS"        (the shock number)
  C  hand writing a deposit slip     ->  "NO CRIME. / NO CHARGE."     (the hook line)

Selected = the built option with the highest (mean luma, contrast) that clears the
acceptance visibility floor (mean>=33, std>=40), so thumbnail_visibility passes.
"""
from __future__ import annotations
import shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageStat

ROOT = Path(__file__).resolve().parents[1]
W, H = 1280, 720
# remotion/public/fonts is absent on this node; use the system Arial faces.
BLK = "C:/Windows/Fonts/ariblk.ttf"
BOLD = "C:/Windows/Fonts/arialbd.ttf"
LOGO = ROOT / "remotion" / "public" / "pd_logo.png"
IMG = "remotion/public/hinders/img"
GOLD = (255, 196, 48)
WHITE = (252, 252, 252)
RED = (222, 34, 38)

# visibility floor (mirrors check_final_acceptance THUMB_MIN_MEAN_LUMA / _CONTRAST_STD)
MIN_MEAN, MIN_STD = 33.0, 40.0

# (hero, focus(x,y frac), kicker, line1 white, line2 gold, big_number|None)
OPTIONS = [
    (f"{IMG}/PD-2026-035-S030-IMG-030.png", (0.60, 0.50), "NO CRIME.  NO CHARGE.", "SHE LOST", "EVERYTHING", None),
    (f"{IMG}/PD-2026-035-S007-IMG-007.png", (0.60, 0.48), "SHE BROKE NO LAW", "SEIZED BY", "THE IRS", "$32,820"),
    (f"{IMG}/PD-2026-035-S001-IMG-001.png", (0.58, 0.46), "THEY TOOK $32,820", "NO CRIME.", "NO CHARGE.", None),
]


def fit(d, text, path, target, max_w, floor=54):
    s = target
    while s > floor:
        f = ImageFont.truetype(path, s)
        if d.textlength(text, font=f) <= max_w:
            return f
        s -= 3
    return ImageFont.truetype(path, s)


def build_hero(hero_rel, focus):
    img = Image.new("RGB", (W, H), (8, 12, 22))
    hp = ROOT / hero_rel
    if hp.exists():
        hero = Image.open(hp).convert("RGB")
        sc = max(W / hero.width, H / hero.height) * 1.05
        hero = hero.resize((int(hero.width * sc), int(hero.height * sc)))
        ox, oy = (hero.width - W) // 2, (hero.height - H) // 2
        hero = hero.crop((ox, oy, ox + W, oy + H))
        hero = ImageEnhance.Brightness(hero).enhance(1.42)     # sources are noir-dark => lift hard
        hero = ImageEnhance.Contrast(hero).enhance(1.30)
        hero = ImageEnhance.Color(hero).enhance(1.45)
        img.paste(hero, (0, 0))
        # warm focal glow on the subject
        fx, fy = int(focus[0] * W), int(focus[1] * H)
        glow = Image.new("L", (W, H), 0)
        ImageDraw.Draw(glow).ellipse([fx - 330, fy - 240, fx + 330, fy + 240], fill=130)
        img = Image.composite(Image.new("RGB", (W, H), (255, 240, 205)), img, glow.filter(ImageFilter.GaussianBlur(130)))
    # left scrim
    grad = Image.new("L", (W, 1), 0)
    for x in range(W):
        t = max(0.0, 1.0 - x / (W * 0.64))
        grad.putpixel((x, 0), int(250 * (t ** 1.05)))
    img = Image.composite(Image.new("RGB", (W, H), (2, 5, 14)), img, grad.resize((W, H)))
    # RED radial burst behind the headline (the 派手 pop)
    burst = Image.new("L", (W, H), 0)
    ImageDraw.Draw(burst).ellipse([-220, 150, 760, 700], fill=120)
    img = Image.composite(Image.new("RGB", (W, H), RED), img, burst.filter(ImageFilter.GaussianBlur(160)))
    # bottom scrim
    bs = Image.new("L", (W, H), 0)
    ImageDraw.Draw(bs).rectangle([0, H - 150, W, H], fill=170)
    img = Image.composite(Image.new("RGB", (W, H), (2, 5, 12)), img, bs.filter(ImageFilter.GaussianBlur(55)))
    return img


def render(o, out):
    hero, focus, kicker, l1, l2, num = o
    img = build_hero(hero, focus)
    d = ImageDraw.Draw(img)
    MX = 58
    # giant glowing $number (shock focal) upper-right
    if num:
        nf = ImageFont.truetype(BLK, 190)
        nw = d.textlength(num, font=nf)
        nx, ny = W - nw - 60, 44
        gl = Image.new("L", (W, H), 0)
        ImageDraw.Draw(gl).text((nx, ny), num, font=nf, fill=255)
        img.paste(Image.new("RGB", (W, H), GOLD), (0, 0), gl.filter(ImageFilter.GaussianBlur(26)))
        d = ImageDraw.Draw(img)
        d.text((nx, ny), num, font=nf, fill=GOLD, stroke_width=8, stroke_fill=(0, 0, 0))
    # red kicker tag
    kf = ImageFont.truetype(BLK, 36)
    kw = d.textlength(kicker, font=kf)
    d.rectangle([MX, 60, MX + kw + 40, 128], fill=RED)
    d.text((MX + 20, 71), kicker, font=kf, fill=WHITE)
    # XL headline, thick stroke
    y = 210
    mw = int(W * 0.70)
    for text, color in [(l1, WHITE), (l2, GOLD)]:
        f = fit(d, text, BLK, 168, mw)
        asc, desc = f.getmetrics()
        d.text((MX, y), text, font=f, fill=color, stroke_width=10, stroke_fill=(0, 0, 0))
        y += int((asc + desc) * 0.82)
    d.rectangle([MX, min(y + 8, H - 92), MX + 470, min(y + 18, H - 82)], fill=GOLD)
    if LOGO.exists():
        logo = Image.open(LOGO).convert("RGBA")
        lw = 122
        logo = logo.resize((lw, int(logo.height * lw / logo.width)))
        img.paste(logo, (W - lw - 40, H - logo.height - 34), logo)
    img.save(out)


def measure(p: Path):
    st = ImageStat.Stat(Image.open(p).convert("L"))
    return st.mean[0], st.stddev[0]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    epdir = ROOT / "episodes" / "PD-2026-035-hinders"
    outdir = epdir / "10_thumbnail"
    pkg = epdir / "09_package"
    outdir.mkdir(parents=True, exist_ok=True)
    pkg.mkdir(parents=True, exist_ok=True)
    made = []
    for i, o in enumerate(OPTIONS, 1):
        out = outdir / f"thumbnail_option_{i:02d}.v001.png"
        render(o, out)
        mean, std = measure(out)
        made.append((out, o, mean, std))
        num = f" + {o[5]}" if o[5] else ""
        print(f"  option {i}: {out.name}  [{o[2]} / {o[3]} {o[4]}{num}]  mean={mean:.1f} std={std:.1f}")
    # select brightest option that clears the visibility floor; fall back to highest mean.
    passing = [m for m in made if m[2] >= MIN_MEAN and m[3] >= MIN_STD]
    pick = max(passing or made, key=lambda m: (m[2], m[3]))
    sel_src = pick[0]
    shutil.copy2(sel_src, outdir / "thumbnail_ctr.v001.png")
    shutil.copy2(sel_src, pkg / "thumbnail.selected.v001.png")
    print(f"selected -> {sel_src.name}  (mean={pick[2]:.1f} std={pick[3]:.1f}) "
          f"-> 09_package/thumbnail.selected.v001.png")


if __name__ == "__main__":
    main()
