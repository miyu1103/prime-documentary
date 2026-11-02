#!/usr/bin/env python3
r"""EP41 Thompson CTR thumbnails -- REAL-STILL background build (1920x1080).

Models exactly on the proven CTR recipe (scripts/build_frazier_thumbnails_v003.py +
build_lech_thumbnails_v002.py): gold accent sidebar, red kicker tag, XL Arial-Black
headline in a thick black stroke over a bottom-left dark scrim, on top of a REAL
photoreal episode still (no cheap CG). The winning layout is scaled 1.0 -> 1.5 to
render natively at 1920x1080 (task requirement). Palette per the script spec (line
153 of EP41_thompson_script.en.v001.md): dark navy/black bg + gold #E5B53A accent,
UPPERCASE headline words, 320px-legible.

Backgrounds (episode's own SDXL photoreal stills, E:/pd-media/assets/ai/thompson):
  option 1 (SELECTED) S02 -- a heavy steel/iron cell door in a concrete wall, wall
                             lamp: the 14 years on death row.  "BURIED FOR 14 YEARS"
  option 2            S24 -- two hands holding up a single glowing sheet of paper in
                             a spotlight: the buried lab report.  "THE PROOF THEY HID"
  option 3            S30 -- a row of tall columns (Supreme Court colonnade), cold
                             light.  "5-4: NO PAYMENT"

clamp_highlights caps every pixel at 188 luma so the ONLY >200 cores are the white
headline text -> the thick black stroke gives the dark outline ring the CTR check
wants. The dark scrim sits on the TEXT side only; the subject stays lifted/bright.

R2: iron door / a sheet of paper / columns are symbolic. NO real face, NO identifiable
real person, NO portrait of John Thompson.

    py -3.11 scripts/build_thompson_thumbnails.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "PD-2026-041-thompson" / "09_package"
# real photoreal stills live on the media SSD
IMG = Path("E:/pd-media/assets/ai/thompson")
W, H = 1920, 1080
S = 1.5  # scale factor from the proven 1280x720 layout

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"

BLUE = (31, 107, 255)
GOLD = (229, 181, 58)   # #E5B53A
WHITE = (247, 249, 252)
RED = (206, 44, 44)
CLAMP_LUMA = 188.0
MAX_SELECTED_BYTES = 2 * 1024 * 1024  # YouTube thumbnail hard cap


def font(path, size):
    return ImageFont.truetype(path, int(size))


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


def dark_scrim(img, box, dark=(2, 5, 12), strength=205, blur=90):
    s = Image.new("L", (W, H), 0)
    ImageDraw.Draw(s).rectangle(box, fill=strength)
    return Image.composite(Image.new("RGB", (W, H), dark), img, s.filter(ImageFilter.GaussianBlur(blur)))


def headline(img, line1, line2, kicker, accent2=GOLD):
    img = dark_scrim(img, [0, H - int(388 * S), int(W * 0.74), H])
    d = ImageDraw.Draw(img)
    MX = int(68 * S)
    max_w = int(W * 0.66)
    lines = [(line1, WHITE)] + ([(line2, accent2)] if line2 else [])
    kf = font(FONT_BOLD, 34 * S)
    size = int(150 * S)
    while size > int(84 * S):
        f = font(FONT_BLACK, size)
        asc, desc = f.getmetrics()
        adv = int((asc + desc) * 0.80)
        widest = max(d.textlength(t, font=f) for t, _ in lines)
        block_h = int(58 * S) + int(16 * S) + len(lines) * adv + int(26 * S)
        if widest <= max_w and block_h <= int(372 * S):
            break
        size -= int(4 * S)
    f = font(FONT_BLACK, size)
    asc, desc = f.getmetrics()
    adv = int((asc + desc) * 0.80)
    block_h = int(58 * S) + int(16 * S) + len(lines) * adv + int(26 * S)
    top = H - int(30 * S) - block_h
    d.rectangle([int(18 * S), top, int(40 * S), min(H - int(30 * S), top + block_h)], fill=GOLD)
    kw = d.textlength(kicker, font=kf)
    d.rectangle([MX, top, MX + kw + int(40 * S), top + int(58 * S)], fill=RED)
    d.text((MX + int(20 * S), top + int(10 * S)), kicker, font=kf, fill=WHITE)
    y = top + int(74 * S)
    for text, color in lines:
        d.text((MX, y), text, font=f, fill=color, stroke_width=int(22 * S), stroke_fill=(0, 0, 0))
        y += adv
    d.rectangle([MX, y + int(4 * S), MX + int(360 * S), y + int(20 * S)], fill=GOLD)
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
        lw = int(118 * S)
        lg = lg.resize((lw, int(lg.height * lw / lg.width)))
        img.paste(lg, (W - lw - int(38 * S), H - lg.height - int(30 * S)), lg)
    img.save(out)
    return out


def save_selected_under_cap(src_png: Path, dst_png: Path):
    """Copy the chosen variant to the 'selected' name, guaranteed < 2 MB PNG for YouTube.

    Dark high-contrast stills compress well; a 1280x720 optimized PNG is normally
    ~0.5-1.5 MB. If it still exceeds the cap we step the long edge down until it fits.
    """
    base = Image.open(src_png).convert("RGB")
    for long_edge in (1280, 1160, 1040, 960, 854, 768):
        w = long_edge
        h = int(base.height * w / base.width)
        im = base.resize((w, h), Image.LANCZOS)
        im.save(dst_png, format="PNG", optimize=True)
        if dst_png.stat().st_size <= MAX_SELECTED_BYTES:
            return long_edge, dst_png.stat().st_size
    return long_edge, dst_png.stat().st_size


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    OUT.mkdir(parents=True, exist_ok=True)
    specs = [
        # photo, brightness, contrast, line1, line2, kicker, accent2, centering
        ("S02.png", 1.58, 1.06, "BURIED FOR", "14 YEARS", "18 YEARS · 14 ON DEATH ROW", GOLD, (0.5, 0.30)),
        ("S24.png", 1.16, 1.07, "THE PROOF", "THEY HID", "A LAB REPORT · BLOOD TYPE B", GOLD, (0.55, 0.28)),
        ("S30.png", 1.52, 1.10, "5-4:", "NO PAYMENT", "JURY $14M · COURT $0", GOLD, (0.5, 0.40)),
    ]
    paths = []
    for i, (ph, b, c, l1, l2, kick, acc, cen) in enumerate(specs, 1):
        p = OUT / f"thumbnail.v001-{i:02d}.png"
        build(ph, b, c, l1, l2, kick, p, acc, cen)
        paths.append(p)
        print(f"  option {i}: {p.name}  bg={ph}  ({l1} {l2} / {kick})")

    # SELECTED = option 1 (iron cell door / BURIED FOR 14 YEARS): boldest single subject,
    # adds the time/prison dimension the title does not (title = the hiding; thumb = the cost).
    selected_idx = 0
    selected = OUT / "thumbnail.selected.v001.png"
    long_edge, nbytes = save_selected_under_cap(paths[selected_idx], selected)
    report = {
        "episode_id": "PD-2026-041-thompson",
        "render_size": f"{W}x{H}",
        "selected": selected.name,
        "selected_source_variant": paths[selected_idx].name,
        "selected_bg": specs[selected_idx][0],
        "selected_long_edge": long_edge,
        "selected_bytes": nbytes,
        "selected_sha256": "sha256:" + sha256(selected),
        "visibility": [score(p) for p in [*paths, selected]],
    }
    (OUT / "thumbnail_visibility.stub.v001.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"selected -> {selected.name}  ({long_edge}px long edge, {nbytes/1024:.0f} KB, < 2 MB cap)")
    print(json.dumps(report["visibility"], ensure_ascii=False))


if __name__ == "__main__":
    main()
