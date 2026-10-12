#!/usr/bin/env python3
r"""EP40 Lech CTR thumbnails v002 -- REAL-FOOTAGE background rebuild.

Owner reject on v001: the destroyed house was a flat CG "book-illustration" (AIスライドショー感) and
tanked CTR. This v002 keeps the EXACT winning text layout from v001 (gold accent sidebar, red kicker
tag, XL Arial-Black headline in a 22px black stroke over a bottom-left dark scrim) but drops the whole
CG subject and paints a REAL photoreal still from the finished episode's own asset set as the
background: a destroyed two-story family home from the Lech raid sequence.

Backgrounds (episode's own SDXL photoreal stills, remotion/public/lech/img):
  option 1 (SELECTED) S35_01 -- two-story home with the front wall torn open, a bedroom + bed exposed,
                                 huge rubble pile, bright daylight. The strongest "destroyed house" frame.
  option 2            S36_01 -- full front facade, every window blown out, abandoned/wrecked, daylight.
  option 3            S44_01 -- wide street view of the collapsed house, blue accent.

Pipeline is identical to the proven recipe EXCEPT background = cover-fit photo (optionally lifted a
touch), then clamp_highlights caps every pixel at 188 luma so the ONLY >200 cores are the white
headline text -> the 22px black stroke gives the dark outline ring check_thumb_subject_luma needs. The
dark scrim sits on the TEXT side only; the house stays bright (owner: 被写体は明るく残す).

R2: destroyed house / rubble are symbolic, no real faces, no identifiable people.

    py -3.11 scripts/build_lech_thumbnails_v002.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "PD-2026-040-lech" / "09_package"
IMG = ROOT / "remotion" / "public" / "lech" / "img"
W, H = 1280, 720

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_IMPACT = "C:/Windows/Fonts/impact.ttf"

INK = (6, 9, 15)
BLUE = (31, 107, 255)
GOLD = (229, 181, 58)
WHITE = (247, 249, 252)
RED = (206, 44, 44)
CLAMP_LUMA = 188.0


def font(path, size):
    return ImageFont.truetype(path, size)


def photo_bg(name, brightness=1.0, contrast=1.0, centering=(0.5, 0.42)):
    """Cover-fit a real episode still to WxH, optional midtone lift. Subject stays photographic."""
    im = Image.open(IMG / name).convert("RGB")
    im = ImageOps.fit(im, (W, H), method=Image.LANCZOS, centering=centering)
    if brightness != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brightness)
    if contrast != 1.0:
        im = ImageEnhance.Contrast(im).enhance(contrast)
    return im


def clamp_highlights(img):
    """Cap every pixel at CLAMP_LUMA so the ONLY >200 cores are the headline (drawn AFTER)."""
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


def headline(img, line1, line2, kicker, accent2=GOLD):
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
    d.rectangle([18, top, 40, min(H - 30, top + block_h)], fill=GOLD)
    kw = d.textlength(kicker, font=kf)
    d.rectangle([MX, top, MX + kw + 40, top + 58], fill=RED)
    d.text((MX + 20, top + 10), kicker, font=kf, fill=WHITE)
    y = top + 74
    for text, color in lines:
        d.text((MX, y), text, font=f, fill=color, stroke_width=22, stroke_fill=(0, 0, 0))
        y += adv
    d.rectangle([MX, y + 4, MX + 360, y + 20], fill=GOLD)
    return img


def score(path):
    im = Image.open(path).convert("L")
    st = ImageStat.Stat(im)
    return {"file": path.name, "mean_luma": round(st.mean[0], 2), "contrast_std": round(st.stddev[0], 2)}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(photo, brightness, contrast, line1, line2, kicker, out, accent2=GOLD, centering=(0.5, 0.42)):
    img = photo_bg(photo, brightness, contrast, centering)
    img = clamp_highlights(img)
    img = headline(img, line1, line2, kicker, accent2)
    logo = ROOT / "remotion" / "public" / "pd_logo.png"
    if logo.exists():
        lg = Image.open(logo).convert("RGBA")
        lw = 118
        lg = lg.resize((lw, int(lg.height * lw / lg.width)))
        img.paste(lg, (W - lw - 38, H - lg.height - 30), lg)
    img.save(out)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    # back up the CG v001 selected before we replace it
    old_sel = OUT / "thumbnail.selected.v001.png"
    if old_sel.exists():
        shutil.copy2(old_sel, OUT / "thumbnail.selected.v001.prev.png")
    specs = [
        ("S35_01.png", 1.06, 1.05, "THEY GOT", "$0", "POLICE CHASED A SHOPLIFTER", GOLD, (0.5, 0.40)),
        ("S36_01.png", 1.04, 1.06, "POLICE DESTROYED", "A HOUSE", "TO CATCH A SHOPLIFTER", GOLD, (0.5, 0.46)),
        ("S44_01.png", 1.10, 1.08, "WHO", "PAYS?", "THE CITY PAID NOTHING", BLUE, (0.5, 0.5)),
    ]
    paths = []
    for i, (ph, b, c, l1, l2, kick, acc, cen) in enumerate(specs, 1):
        p = OUT / f"thumbnail.v002-{i:02d}.png"
        build(ph, b, c, l1, l2, kick, p, acc, cen)
        paths.append(p)
        print(f"  option {i}: {p.name}  bg={ph}  ({l1} {l2} / {kick})")
    selected = OUT / "thumbnail.selected.v002.png"
    shutil.copy2(paths[0], selected)
    report = {
        "episode_id": "PD-2026-040-lech",
        "selected": selected.name,
        "selected_bg": specs[0][0],
        "selected_sha256": "sha256:" + sha256(selected),
        "visibility": [score(p) for p in [*paths, selected]],
    }
    (OUT / "thumbnail_visibility.stub.v002.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("selected ->", selected.name)
    print(json.dumps(report["visibility"], ensure_ascii=False))


if __name__ == "__main__":
    main()
