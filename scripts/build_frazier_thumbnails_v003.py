#!/usr/bin/env python3
r"""EP39 Frazier CTR thumbnails v003 -- REAL-FOOTAGE background rebuild.

Owner reject on v002: the "subject" was a hand-drawn CG interrogation room (blurry little desk, weak
subject) -> AIスライドショー感, low CTR. This v003 keeps the EXACT winning text layout from v002 (gold
accent sidebar, red kicker tag, XL Arial-Black headline in a 22px black stroke over a bottom-left dark
scrim) but drops the CG subject and paints a REAL photoreal still from the episode's own asset set:
a classic police interrogation room (steel table, two facing chairs, hard overhead light, one-way
mirror on the back wall) -- the exact "police can lie to you" setting.

Backgrounds (episode's own SDXL photoreal stills, H:/pd-media/assets/ai/frazier):
  option 1 (SELECTED) S01 -- interrogation room: steel table, two chairs, hanging light, one-way mirror.
  option 2            S31 -- interrogation room with a desk lamp pool of light on a scarred wood table.
  option 3            S19 -- a stack of signed statement pages with a pen (the false confession), blue.

clamp_highlights caps every pixel at 188 luma so the ONLY >200 cores are the white headline text ->
the 22px black stroke gives the dark outline ring check_thumb_subject_luma needs. The dark scrim sits
on the TEXT side only; the room is lifted so it is not a dark blob (owner: 被写体は明るく残す/暗すぎない).

R2: interrogation room / documents are symbolic, no real faces, no identifiable people.

    py -3.11 scripts/build_frazier_thumbnails_v003.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "PD-2026-039-frazier" / "09_package"
# real photoreal stills live on the media SSD (remotion/public/frazier holds only stub placeholders)
IMG = Path("H:/pd-media/assets/ai/frazier")
W, H = 1280, 720

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"

BLUE = (31, 107, 255)
GOLD = (229, 181, 58)
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
    old_sel = OUT / "thumbnail.selected.v002.png"
    if old_sel.exists():
        shutil.copy2(old_sel, OUT / "thumbnail.selected.v002.prev.png")
    specs = [
        ("S01.png", 1.60, 1.05, "POLICE CAN", "LIE TO YOU", "AND IT'S 100% LEGAL", GOLD, (0.5, 0.34)),
        ("S31.png", 1.55, 1.05, "HE CONFESSED", "TO A LIE", "FALSE CONFESSION · 16 YEARS", GOLD, (0.62, 0.5)),
        ("S19.png", 1.40, 1.06, "IS THIS", "LEGAL?", "DNA LATER PROVED HIM INNOCENT", BLUE, (0.55, 0.4)),
    ]
    paths = []
    for i, (ph, b, c, l1, l2, kick, acc, cen) in enumerate(specs, 1):
        p = OUT / f"thumbnail.v003-{i:02d}.png"
        build(ph, b, c, l1, l2, kick, p, acc, cen)
        paths.append(p)
        print(f"  option {i}: {p.name}  bg={ph}  ({l1} {l2} / {kick})")
    selected = OUT / "thumbnail.selected.v003.png"
    shutil.copy2(paths[0], selected)
    report = {
        "episode_id": "PD-2026-039-frazier",
        "selected": selected.name,
        "selected_bg": specs[0][0],
        "selected_sha256": "sha256:" + sha256(selected),
        "visibility": [score(p) for p in [*paths, selected]],
    }
    (OUT / "thumbnail_visibility.stub.v003.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("selected ->", selected.name)
    print(json.dumps(report["visibility"], ensure_ascii=False))


if __name__ == "__main__":
    main()
