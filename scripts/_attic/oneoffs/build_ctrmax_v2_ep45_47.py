#!/usr/bin/env python3
r"""EP45-47 CTR-MAX v2 consistency pass -- unifies the three already-strong selected thumbnails
(cleveland / tlo / atwater) onto ONE shared high-CTR formula so all EP39-47 long-form thumbs match.

This is a LIGHT-TOUCH recolor, not a rebuild. Each episode keeps its winning hook wording, layout,
and its own strong SDXL background still. The ONLY changes are the shared v2 brand elements:

  SHARED "CTR-MAX v2" SPEC (identical across every episode)
    - KICKER: white ALL-CAPS on a solid RED #D32F2F bar, top of the text block.
    - HEADLINE line 1: bone-white #F5F5F0, heavy Arial-Black ALL-CAPS, 22px black stroke.
    - HEADLINE line 2 (the PUNCH): GOLD #E5B53A + a GOLD underline.
    - Gold vertical accent bar far-left.
    - Brand logo bottom-right on a dark chip.
    - Bright / high-contrast background with a dark gradient scrim over the bottom-left ~40%.
    - Legible at 210px.

  Per-episode delta from v001 (accent -> red/gold):
    EP45 cleveland: crimson lane/punch/underline  -> gold; kicker red stays. bg brighten +.
    EP46 tlo:       green  lane/punch/underline    -> gold; kicker red stays.
    EP47 atwater:   violet lane/punch/underline    -> gold; VIOLET kicker -> RED. bg brighten +.

Backgrounds reuse each episode's own selected still (E:/pd-media/assets/ai/<slug>). No SDXL regen.
Output: episodes/PD-2026-0XX-<slug>/09_package/thumbnail.selected.v002.png (v001 preserved).

    py -3.11 scripts/build_ctrmax_v2_ep45_47.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
W, H = 1280, 720

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"

# --- shared CTR-MAX v2 palette ---
RED = (211, 47, 47)       # #D32F2F  kicker bar
BONE = (245, 245, 240)    # #F5F5F0  headline line 1
GOLD = (229, 181, 58)     # #E5B53A  punch line + underline + left accent bar
CLAMP_LUMA = 188.0


def font(path, size):
    return ImageFont.truetype(path, size)


def photo_bg(path, brightness=1.0, contrast=1.0, centering=(0.5, 0.42)):
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (W, H), method=Image.LANCZOS, centering=centering)
    if brightness != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brightness)
    if contrast != 1.0:
        im = ImageEnhance.Contrast(im).enhance(contrast)
    return im


def clamp_highlights(img):
    px = img.load()
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            L = 0.299 * r + 0.587 * g + 0.114 * b
            if L > CLAMP_LUMA:
                s = CLAMP_LUMA / L
                px[x, y] = (int(r * s), int(g * s), int(b * s))
    return img


def dark_scrim(img, box, dark=(2, 5, 12), strength=205, blur=60):
    s = Image.new("L", (W, H), 0)
    ImageDraw.Draw(s).rectangle(box, fill=strength)
    return Image.composite(Image.new("RGB", (W, H), dark), img, s.filter(ImageFilter.GaussianBlur(blur)))


def headline(img, line1, line2, kicker):
    img = dark_scrim(img, [0, H - 388, int(W * 0.74), H])
    d = ImageDraw.Draw(img)
    MX = 68
    max_w = int(W * 0.66)
    lines = [(line1, BONE)] + ([(line2, GOLD)] if line2 else [])
    kf = font(FONT_BOLD, 34)
    size = 150
    while size > 84:
        f = font(FONT_BLACK, size)
        asc, desc = f.getmetrics()
        adv = int((asc + desc) * 0.80)
        widest = max(d.textlength(t, font=f) for t, _ in lines)
        block_h = 58 + 16 + len(lines) * adv + 26
        if widest <= max_w and block_h <= 372:
            break
        size -= 4
    f = font(FONT_BLACK, size)
    asc, desc = f.getmetrics()
    adv = int((asc + desc) * 0.80)
    block_h = 58 + 16 + len(lines) * adv + 26
    top = H - 30 - block_h
    # far-left GOLD vertical accent bar
    d.rectangle([18, top, 40, min(H - 30, top + block_h)], fill=GOLD)
    # RED kicker bar (shared across all episodes)
    kw = d.textlength(kicker, font=kf)
    d.rectangle([MX, top, MX + kw + 40, top + 58], fill=RED)
    d.text((MX + 20, top + 10), kicker, font=kf, fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
    y = top + 74
    for text, color in lines:
        d.text((MX, y), text, font=f, fill=color, stroke_width=22, stroke_fill=(0, 0, 0))
        y += adv
    # GOLD underline under the punch line
    d.rectangle([MX, y + 4, MX + 360, y + 20], fill=GOLD)
    return img


def build(bg_path, brightness, contrast, line1, line2, kicker, out, centering=(0.5, 0.42)):
    img = photo_bg(bg_path, brightness, contrast, centering)
    img = clamp_highlights(img)
    img = headline(img, line1, line2, kicker)
    logo = ROOT / "remotion" / "public" / "pd_logo.png"
    if logo.exists():
        lg = Image.open(logo).convert("RGBA")
        lw = 118
        lg = lg.resize((lw, int(lg.height * lw / lg.width)))
        lx, ly = W - lw - 38, H - lg.height - 30
        chip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(chip)
        pad = 16
        cd.rounded_rectangle([lx - pad, ly - pad, lx + lw + pad, ly + lg.height + pad],
                             radius=16, fill=(4, 6, 12, 190))
        img = Image.alpha_composite(img.convert("RGBA"), chip).convert("RGB")
        img.paste(lg, (lx, ly), lg)
    img.save(out)
    return out


# (episode dir, media subdir/still, brightness, contrast, line1, line2, kicker, centering)
SPECS = [
    ("PD-2026-045-cleveland", "cleveland/S04.png", 1.42, 1.09,
     "JAILED FOR", "BEING POOR", "DEBTORS' PRISON", (0.50, 0.45)),
    ("PD-2026-046-tlo", "tlo/S08.png", 1.55, 1.12,
     "YOUR LOCKER", "ISN'T SAFE", "NO WARRANT NEEDED", (0.50, 0.46)),
    ("PD-2026-047-atwater", "atwater/S53.png", 1.30, 1.12,
     "JAILED OVER", "A SEATBELT", "ATWATER v. LAGO VISTA", (0.62, 0.50)),
]

IMG_ROOT = Path("E:/pd-media/assets/ai")


def next_selected(pkg: Path) -> Path:
    n = 2
    while (pkg / f"thumbnail.selected.v{n:03d}.png").exists():
        n += 1
    return pkg / f"thumbnail.selected.v{n:03d}.png"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for ep, still, b, c, l1, l2, kick, cen in SPECS:
        pkg = ROOT / "episodes" / ep / "09_package"
        pkg.mkdir(parents=True, exist_ok=True)
        out = next_selected(pkg)
        build(IMG_ROOT / still, b, c, l1, l2, kick, out, cen)
        kb = out.stat().st_size / 1024
        print(f"{ep}: {out.name}  ({kb:.0f} KB)  [{kick} / {l1} {l2}]")


if __name__ == "__main__":
    main()
