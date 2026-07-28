#!/usr/bin/env python3
r"""EP46 T.L.O. CTR thumbnails v001 -- clones the winning Tekoh/Cleveland v001 text treatment.

New Jersey v. T.L.O., 469 U.S. 325 (1985), a 6-3 Supreme Court decision: a high-school student's
purse was searched by an assistant vice principal after she was accused of smoking in a restroom.
The Court held the Fourth Amendment DOES apply to searches by public-school officials -- but at
school those officials need only "reasonable suspicion," NOT a warrant and NOT probable cause, to
search a student's belongings. The packaging frames the holding as a curiosity gap ("can they
really search you at school without a warrant?"), never as legal advice, and never shows a face,
a minor, or the underlying suspected offense (R2).

This reuses the EXACT winning layout from build_tekoh_thumbnails.py:
  - XL Arial-Black headline (auto-fit) in a 22px black stroke, over a bottom-left dark scrim on the
    TEXT SIDE ONLY (subject side stays bright -> owner rule 被写体を暗くしすぎない).
  - a small RED kicker tag, an ACCENT sidebar + underline.
  - clamp_highlights() caps every background pixel at 188 luma so the ONLY >200 cores are the white
    headline glyphs -> the 22px black stroke gives the dark outline ring check_thumb_subject_luma wants.
The ONE brand change: the lane accent is EP46's SCHOOLHOUSE GREEN #3F8F5F (replaces Tekoh's teal).
Kicker stays RED.

CTR-max headlines (<=3-4 huge words, second-person / curiosity-gap hook, mobile-legible):
  option 1  "SEARCHED AT SCHOOL"     -- symbolic school-hallway lockers (the schoolhouse).
  option 2  "THEY SEARCHED HER BAG"  -- an open purse on the administrator's desk (the search).
  option 3  "YOUR LOCKER ISN'T SAFE" -- a single closed locker (second-person threat / relatability).

Backgrounds (episode's own SDXL 4K photoreal stills, H:/pd-media/assets/ai/tlo):
  S06 -- a high-school hallway lined with grey metal lockers receding into low institutional light.
  S15 -- a canvas purse tipped open on a vice principal's wooden desk under warm lamplight.
  S08 -- a single closed school locker with its combination dial in cool institutional light.
R2: a hallway / a bag / a locker -- no faces, no people, no minors, no offense imagery.

SELECTION: option 3 "YOUR LOCKER ISN'T SAFE" (S08) is copied to thumbnail.selected.v001.png --
the strongest CTR hook (second-person + personal threat, single high-contrast subject that reads at
~210px mobile width).

    py -3.11 scripts/build_tlo_thumbnails.py
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "PD-2026-046-tlo" / "09_package"
# real photoreal stills live on the media SSD
IMG = Path("H:/pd-media/assets/ai/tlo")
W, H = 1280, 720

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"

LANE = (63, 143, 95)     # #3F8F5F -- EP46 tlo lane color (schoolhouse green)
WHITE = (247, 249, 252)
RED = (206, 44, 44)
CLAMP_LUMA = 188.0

# 1-based index of the option copied to thumbnail.selected.v001.png
SELECTED = 3


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
    d.rectangle([MX, top, MX + kw + 40, top + 58], fill=RED)
    # thin black stroke on the white kicker text so its bright cores are wrapped by a DARK ring (the red
    # tag, luma ~92, is too close to the outline gate's 95 floor once anti-aliased -> would zero the
    # outline metric when the headline itself is short)
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
        # background -> keeps check_thumb_subject_luma's outline metric valid
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
        ("S06.png", 1.62, 1.10, "SEARCHED", "AT SCHOOL", "NO WARRANT NEEDED", LANE, (0.50, 0.45)),
        ("S15.png", 1.30, 1.12, "THEY SEARCHED", "HER BAG", "SUPREME COURT · 6-3", LANE, (0.50, 0.52)),
        ("S08.png", 1.55, 1.12, "YOUR LOCKER", "ISN'T SAFE", "NO WARRANT NEEDED", LANE, (0.50, 0.46)),
    ]
    paths = []
    for i, (ph, b, c, l1, l2, kick, acc, cen) in enumerate(specs, 1):
        p = OUT / f"thumbnail.v001-{i:02d}.png"
        build(ph, b, c, l1, l2, kick, p, acc, cen)
        paths.append((p, f"{i:02d}  {ph}  {kick} / {l1} {l2}"))
        print(f"  option {i}: {p.name}  bg={ph}  ({kick} / {l1} {l2})")
    sheet = contact_sheet(paths, OUT / "thumbnail_options_contact.png")
    print("contact ->", sheet.name)
    sel_src = OUT / f"thumbnail.v001-{SELECTED:02d}.png"
    sel_dst = OUT / "thumbnail.selected.v001.png"
    shutil.copyfile(sel_src, sel_dst)
    print(f"selected -> {sel_dst.name}  (option {SELECTED}: {sel_src.name})")


if __name__ == "__main__":
    main()
