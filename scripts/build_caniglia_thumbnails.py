#!/usr/bin/env python3
r"""EP43 Caniglia CTR thumbnails v001 -- clones the winning Frazier v003 text treatment.

Caniglia v. Strom (2021), a UNANIMOUS 9-0 Supreme Court decision: police did a "welfare check" on a
man's home and, with no warrant, entered and seized two handguns under the "community caretaking"
doctrine. The Court held that the community-caretaking exception -- born in the vehicle context -- does
NOT extend a standalone license to enter the HOME without a warrant. It did NOT abolish warrantless
entry (warrant / consent / exigent-emergency still apply); it narrowed caretaking as to the home.

This reuses the EXACT winning layout from build_frazier_thumbnails_v003.py:
  - XL Arial-Black headline (auto-fit) in a 22px black stroke, over a bottom-left dark scrim on the
    TEXT SIDE ONLY (subject side stays bright -> owner rule 被写体を暗くしすぎない).
  - a small RED kicker tag, an ACCENT sidebar + underline.
  - clamp_highlights() caps every background pixel at 188 luma so the ONLY >200 cores are the white
    headline glyphs -> the 22px black stroke gives the dark outline ring check_thumb_subject_luma wants.
The ONE brand change: Frazier's GOLD accent -> Caniglia's lane color AMBER #E0913C (no gold/blue, which
belong to other episodes' lanes). The kicker tag stays RED.

Backgrounds (episode's own SDXL 4K photoreal stills, H:/pd-media/assets/ai/caniglia):
  option 1  S05 -- a residential FRONT DOOR at dusk under a lit porch lantern (warrantless home entry).
  option 2  S06 -- the U.S. Supreme Court building at night, marble columns lit (the 9-0 ruling).
  option 3  S01 -- a HANDGUN resting on a dining table beside a warm lamp (the two seized handguns).

R2: doors / a building / an object on a table -- no faces, no identifiable people. Neutral welfare-check
/ warrantless-home-entry framing only; no distress or self-harm imagery.

    py -3.11 scripts/build_caniglia_thumbnails.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "PD-2026-043-caniglia" / "09_package"
# real photoreal stills live on the media SSD
IMG = Path("H:/pd-media/assets/ai/caniglia")
W, H = 1280, 720

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"

AMBER = (224, 145, 60)   # #E0913C -- EP43 lane color (replaces Frazier's GOLD)
WHITE = (247, 249, 252)
RED = (206, 44, 44)
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


def headline(img, line1, line2, kicker, accent2=AMBER):
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
    d.rectangle([18, top, 40, min(H - 30, top + block_h)], fill=AMBER)
    kw = d.textlength(kicker, font=kf)
    d.rectangle([MX, top, MX + kw + 40, top + 58], fill=RED)
    # thin black stroke on the white kicker text so its bright cores are wrapped by a DARK ring (the red
    # tag, luma ~92, is too close to the outline gate's 95 floor once anti-aliased -> would zero the
    # outline metric when the headline itself is short, e.g. "NO")
    d.text((MX + 20, top + 10), kicker, font=kf, fill=WHITE, stroke_width=4, stroke_fill=(0, 0, 0))
    y = top + 74
    for text, color in lines:
        d.text((MX, y), text, font=f, fill=color, stroke_width=22, stroke_fill=(0, 0, 0))
        y += adv
    d.rectangle([MX, y + 4, MX + 360, y + 20], fill=AMBER)
    return img


def build(photo, brightness, contrast, line1, line2, kicker, out, accent2=AMBER, centering=(0.5, 0.42)):
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
        # background (e.g. the lit SCOTUS marble) -> keeps check_thumb_subject_luma's outline metric valid
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
        ("S05.png", 2.10, 1.06, "INTO YOUR", "HOME", "WARRANTLESS ENTRY", AMBER, (0.52, 0.42)),
        ("S06.png", 1.34, 1.06, "NO", "WARRANT", "SUPREME COURT · 9-0", AMBER, (0.50, 0.46)),
        ("S01.png", 2.30, 1.06, "THEY TOOK", "HIS GUNS", "A WELFARE CHECK", AMBER, (0.50, 0.46)),
    ]
    paths = []
    for i, (ph, b, c, l1, l2, kick, acc, cen) in enumerate(specs, 1):
        p = OUT / f"thumbnail.v001-{i:02d}.png"
        build(ph, b, c, l1, l2, kick, p, acc, cen)
        paths.append((p, f"{i:02d}  {ph}  {kick} / {l1} {l2}"))
        print(f"  option {i}: {p.name}  bg={ph}  ({kick} / {l1} {l2})")
    sheet = contact_sheet(paths, OUT / "thumbnail_options_contact.png")
    print("contact ->", sheet.name)
    # NOTE: intentionally NOT writing thumbnail.selected.v001.png -- selection left to the owner.


if __name__ == "__main__":
    main()
