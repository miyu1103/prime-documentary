#!/usr/bin/env python3
r"""EP47 Atwater CTR thumbnails v001 -- clones the EP45 Cleveland text treatment (which itself clones
the winning Caniglia/Frazier v003 layout).

Atwater v. Lago Vista, 532 U.S. 318 (2001): Gail Atwater was handcuffed, arrested, and jailed over a
seatbelt violation carrying only a $50 fine. The Supreme Court, 5-4, held that the Fourth Amendment
does NOT forbid a warrantless custodial arrest for a minor, fine-only offense. CTR-max packaging:
HUGE <=4-word hooks readable at ~210px (mobile = 68.7% of views), a violet KEYWORD pop, dark
cinematic base, bone-white headline with a heavy black stroke. R2: symbolic stills only -- a seatbelt
buckle, isolated handcuffs, marble/dome -- no faces, no people, no legible text.

Reuses the EXACT winning layout:
  - XL Arial-Black headline (auto-fit) in a 22px black stroke, over a bottom-left dark scrim on the
    TEXT SIDE ONLY (subject side stays bright -> owner rule 被写体を暗くしすぎない).
  - a small violet kicker tag, a violet sidebar + underline.
  - clamp_highlights() caps every background pixel at 188 luma so the ONLY >200 cores are the white
    headline glyphs -> the 22px black stroke gives the dark outline ring check_thumb_subject_luma wants.
The ONE brand change vs Cleveland: the lane accent is EP47's VIOLET #7A5CD0 (replaces the crimson).
The violet keyword (SEATBELT / $50 / IT'S LEGAL) is the POP element -- used sparingly, once per option.

Backgrounds (episode's own SDXL 4K photoreal stills, H:/pd-media/assets/ai/atwater):
  option 1  S53 -- a car seatbelt buckle lit by violet electric arcs on a dark cracked surface
                   (the $50 seatbelt that put her in cuffs -- already carries the lane's violet).
  option 2  S54 -- a single pair of steel handcuffs, spotlit and isolated on cold dark stone
                   (handcuffed for a fine you could pay with a couple of twenties).
  option 3  S57 -- a domed courthouse under a violet dusk sky (the Court that said it was legal, 5-4).

R2: a seatbelt / handcuffs / a building -- no faces, no people, no distress imagery.

    py -3.11 scripts/build_atwater_thumbnails.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "PD-2026-047-atwater" / "09_package"
# real photoreal stills live on the media SSD
IMG = Path("H:/pd-media/assets/ai/atwater")
W, H = 1280, 720

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"

LANE = (122, 92, 208)    # #7A5CD0 -- EP47 atwater lane color (violet)
WHITE = (247, 249, 252)
KICK = (122, 92, 208)    # violet kicker tag (single-accent branding)
CLAMP_LUMA = 188.0


def font(path, size):
    return ImageFont.truetype(path, size)


def photo_bg(name, brightness=1.0, contrast=1.0, centering=(0.5, 0.42)):
    im = Image.open(IMG / name).convert("RGB")
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


def headline(img, line1, line2, kicker, accent2=LANE):
    img = dark_scrim(img, [0, H - 388, int(W * 0.74), H])
    d = ImageDraw.Draw(img)
    MX = 68
    max_w = int(W * 0.66)
    lines = [(line1, WHITE)] + ([(line2, accent2)] if line2 else [])
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
    d.rectangle([18, top, 40, min(H - 30, top + block_h)], fill=LANE)
    kw = d.textlength(kicker, font=kf)
    d.rectangle([MX, top, MX + kw + 40, top + 58], fill=KICK)
    # thin black stroke on the white kicker text so its bright cores are wrapped by a DARK ring (the
    # violet tag, luma ~114, is close enough to the outline gate's floor once anti-aliased that a
    # short headline could zero the outline metric -> the stroke keeps it valid).
    d.text((MX + 20, top + 10), kicker, font=kf, fill=WHITE, stroke_width=4, stroke_fill=(0, 0, 0))
    y = top + 74
    for text, color in lines:
        d.text((MX, y), text, font=f, fill=color, stroke_width=22, stroke_fill=(0, 0, 0))
        y += adv
    d.rectangle([MX, y + 4, MX + 360, y + 20], fill=LANE)
    return img


def build(photo, brightness, contrast, line1, line2, kicker, out, accent2=LANE, centering=(0.5, 0.42)):
    img = photo_bg(photo, brightness, contrast, centering)
    img = clamp_highlights(img)
    img = headline(img, line1, line2, kicker, accent2)
    logo = ROOT / "remotion" / "public" / "pd_logo.png"
    if logo.exists():
        lg = Image.open(logo).convert("RGBA")
        lw = 118
        lg = lg.resize((lw, int(lg.height * lw / lg.width)))
        lx, ly = W - lw - 38, H - lg.height - 30
        # dark chip behind the logo so its bright pixels are wrapped by a dark ring even over a bright
        # background (e.g. a lit dome) -> keeps check_thumb_subject_luma's outline metric valid.
        chip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(chip)
        pad = 16
        cd.rounded_rectangle([lx - pad, ly - pad, lx + lw + pad, ly + lg.height + pad],
                             radius=16, fill=(4, 6, 12, 190))
        img = Image.alpha_composite(img.convert("RGBA"), chip).convert("RGB")
        img.paste(lg, (lx, ly), lg)
    img.save(out)
    return out


def contact_sheet(paths, out, cols=3, panel_w=600, gap=18, pad=18, label_h=34):
    panel_h = int(panel_w * H / W)
    rows = (len(paths) + cols - 1) // cols
    sheet_w = pad * 2 + cols * panel_w + (cols - 1) * gap
    sheet_h = pad * 2 + rows * (panel_h + label_h) + (rows - 1) * gap
    sheet = Image.new("RGB", (sheet_w, sheet_h), (16, 17, 21))
    d = ImageDraw.Draw(sheet)
    lf = font(FONT_BOLD, 22)
    for i, (p, label) in enumerate(paths):
        r, c = divmod(i, cols)
        x = pad + c * (panel_w + gap)
        y = pad + r * (panel_h + label_h + gap)
        thumb = Image.open(p).convert("RGB").resize((panel_w, panel_h), Image.LANCZOS)
        sheet.paste(thumb, (x, y))
        d.text((x + 4, y + panel_h + 6), label, font=lf, fill=WHITE)
    sheet.save(out)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    # (photo, brightness, contrast, line1, line2, kicker, accent2, centering)
    specs = [
        ("S53.png", 1.16, 1.10, "JAILED OVER", "A SEATBELT", "ATWATER v. LAGO VISTA", LANE, (0.62, 0.50)),
        ("S54.png", 1.22, 1.12, "HANDCUFFED", "FOR $50", "A FINE-ONLY OFFENSE", LANE, (0.58, 0.46)),
        ("S57.png", 1.05, 1.08, "THE COURT SAID", "IT'S LEGAL", "SUPREME COURT · 5-4 · 2001", LANE, (0.56, 0.42)),
    ]
    paths = []
    for i, (ph, b, c, l1, l2, kick, acc, cen) in enumerate(specs, 1):
        p = OUT / f"thumbnail.v001-{i:02d}.png"
        build(ph, b, c, l1, l2, kick, p, acc, cen)
        paths.append((p, f"{i:02d}  {ph}  {kick} / {l1} {l2}"))
        print(f"  option {i}: {p.name}  bg={ph}  ({kick} / {l1} {l2})")
    sheet = contact_sheet(paths, OUT / "thumbnail_options_contact.png")
    print("contact ->", sheet.name)
    # selection is applied separately (copied to thumbnail.selected.v001.png) after eyeballing.


if __name__ == "__main__":
    main()
