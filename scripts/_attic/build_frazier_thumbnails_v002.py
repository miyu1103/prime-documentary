#!/usr/bin/env python3
r"""EP39 Frazier CTR thumbnails v002 — rebuilt to PASS all thumbnail gates.

The v001 set FAILED check_thumb_subject_luma (outline 0px < 12px: the 7px text stroke and a
brown-blob subject gave no dark rim). This rebuild uses the proven flashy recipe: a dark navy
gradient, a MID-TONE symbolic subject (no real faces; interrogation room / signed confession /
fingerprint card), and an XL Arial-Black headline wrapped in a thick (22px) black stroke over a
dark scrim. Bright cores are clamped to the headline only so the outline ring stays dark.

Facts locked (Frazier v. Cupp, 1969; Barry Laughman): police may legally lie in interrogation;
Laughman gave a false confession and served ~16 years before DNA exonerated him. No exaggeration,
no real likeness (R2). 1280x720, 3 options + selected, writes into 09_package.

    py -3.11 scripts/build_frazier_thumbnails_v002.py
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "PD-2026-039-frazier" / "09_package"
W, H = 1280, 720

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_IMPACT = "C:/Windows/Fonts/impact.ttf"

INK = (6, 9, 15)
NAVY = (13, 28, 46)
NAVY2 = (9, 20, 34)
BLUE = (31, 107, 255)
GOLD = (229, 181, 58)
WHITE = (247, 249, 252)
SILVER = (188, 196, 208)
RED = (206, 44, 44)
CLAMP_LUMA = 188.0  # subject highlights kept below this so only headline text is a >200 core


def luma(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def font(path, size):
    return ImageFont.truetype(path, size)


def background():
    """Dark navy diagonal gradient + soft center glow (mid-tone, never a bright core)."""
    img = Image.new("RGB", (W, H), INK)
    px = img.load()
    for y in range(H):
        fy = y / H
        for x in range(W):
            fx = x / W
            t = (fx * 0.55 + fy * 0.45)
            r = int(NAVY[0] * (1 - t) + INK[0] * t)
            g = int(NAVY[1] * (1 - t) + INK[1] * t)
            b = int(NAVY[2] * (1 - t) + INK[2] * t)
            px[x, y] = (r, g, b)
    # subtle vignette
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-320, -220, W + 320, H + 220], fill=90)
    img = Image.composite(img, Image.new("RGB", (W, H), INK), vig.filter(ImageFilter.GaussianBlur(180)))
    return img


def add_glow(img, cx, cy, rx, ry, color, strength=120, blur=150):
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=strength)
    return Image.composite(Image.new("RGB", (W, H), color), img, g.filter(ImageFilter.GaussianBlur(blur)))


def clamp_highlights(img):
    """Scale down any pixel brighter than CLAMP_LUMA so the ONLY >200 cores are the headline
    (drawn AFTER this). Keeps the outline ring dark -> passes check_thumb_subject_luma."""
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


def fit_font(d, text, path, target, max_w, floor=70):
    s = target
    while s > floor:
        f = font(path, s)
        if d.textlength(text, font=f) <= max_w:
            return f
        s -= 4
    return font(path, floor)


def headline(img, line1, line2, kicker, accent2=GOLD):
    """XL Arial-Black headline over a dark bottom-left scrim, 22px black stroke + soft dark glow.
    The whole kicker+headline block is sized to fit above the bottom margin (no glyph clipping)."""
    img = dark_scrim(img, [0, H - 388, int(W * 0.74), H])
    d = ImageDraw.Draw(img)
    MX = 68
    max_w = int(W * 0.66)
    lines = [(line1, WHITE)] + ([(line2, accent2)] if line2 else [])
    # pick the largest headline size at which the whole block fits vertically & horizontally
    kf = font(FONT_BOLD, 34)
    size = 150
    while size > 84:
        f = font(FONT_BLACK, size)
        asc, desc = f.getmetrics()
        adv = int((asc + desc) * 0.80)
        widest = max(d.textlength(t, font=f) for t, _ in lines)
        block_h = 58 + 16 + len(lines) * adv + 26  # kicker + gap + lines + underline
        if widest <= max_w and block_h <= 372:
            break
        size -= 4
    f = font(FONT_BLACK, size)
    asc, desc = f.getmetrics()
    adv = int((asc + desc) * 0.80)
    block_h = 58 + 16 + len(lines) * adv + 26
    top = H - 30 - block_h
    # tall gold accent sidebar framing the block (also the >=150px accent component the
    # readability gate needs; isolated from the headline stroke so the outline ring stays dark)
    d.rectangle([18, top, 40, min(H - 30, top + block_h)], fill=GOLD)
    # kicker tag (solid red, white text)
    kw = d.textlength(kicker, font=kf)
    d.rectangle([MX, top, MX + kw + 40, top + 58], fill=RED)
    d.text((MX + 20, top + 10), kicker, font=kf, fill=WHITE)
    # headline lines
    y = top + 74
    for text, color in lines:
        d.text((MX, y), text, font=f, fill=color, stroke_width=22, stroke_fill=(0, 0, 0))
        y += adv
    d.rectangle([MX, y + 4, MX + 360, y + 20], fill=GOLD)
    return img


# --------------------------------------------------------------------------- subjects (mid-tone)

def subj_interrogation(img):
    """Empty 1980s interrogation room: back wall, one-way mirror, steel table + lone chair,
    hard overhead light pool. Recognizable silhouette, mid-tone, no people."""
    img = add_glow(img, 700, 330, 430, 340, (150, 156, 176), strength=150, blur=150)
    d = ImageDraw.Draw(img)
    # one-way mirror on back wall
    d.rectangle([560, 120, 980, 360], fill=(40, 56, 78), outline=(96, 122, 158), width=6)
    d.line([600, 150, 700, 330], fill=(84, 108, 142), width=8)
    d.line([660, 150, 760, 330], fill=(66, 90, 122), width=6)
    # hard light pool on the table (warm mid-grey, clamped later)
    pool = Image.new("L", (W, H), 0)
    ImageDraw.Draw(pool).polygon([(690, 150), (860, 150), (1120, 620), (470, 620)], fill=185)
    img = Image.composite(Image.new("RGB", (W, H), (176, 172, 156)), img, pool.filter(ImageFilter.GaussianBlur(60)))
    d = ImageDraw.Draw(img)
    # steel table
    d.polygon([(500, 470), (1090, 470), (1160, 600), (430, 600)], fill=(150, 152, 158))
    d.polygon([(500, 470), (1090, 470), (1090, 486), (500, 486)], fill=(184, 186, 186))
    d.rectangle([540, 600, 570, 700], fill=(92, 96, 104))
    d.rectangle([1010, 600, 1040, 700], fill=(92, 96, 104))
    # lone empty steel chair (foreground silhouette, rim-lit)
    d.rectangle([760, 430, 900, 470], fill=(78, 84, 94))      # seat
    d.rectangle([760, 300, 792, 470], fill=(90, 96, 108))     # back post
    d.rectangle([760, 300, 900, 328], fill=(132, 138, 150))   # backrest top (rim)
    d.line([760, 300, 900, 300], fill=(180, 184, 186), width=6)
    d.rectangle([772, 470, 792, 560], fill=(70, 74, 84))
    d.rectangle([868, 470, 888, 560], fill=(70, 74, 84))
    return img


def subj_confession(img):
    """A signed confession / statement on the table, ruled lines, a scrawled signature, and a
    red 'FALSE' stamp. Paper kept off-white mid-tone (not a bright core)."""
    img = add_glow(img, 720, 300, 380, 300, (110, 116, 132), strength=90, blur=150)
    d = ImageDraw.Draw(img)
    # angled paper
    paper = [(430, 90), (1120, 150), (1050, 560), (360, 470)]
    d.polygon(paper, fill=(176, 172, 160))
    d.line([paper[0], paper[1]], fill=(150, 146, 134), width=4)
    # heading block + ruled lines
    d.rectangle([470, 140, 760, 176], fill=(120, 116, 106))
    for i in range(9):
        y0 = 210 + i * 34
        d.line([(468, y0 + int(i * 3.2)), (1030, y0 + 60 + int(i * 3.2))], fill=(120, 116, 106), width=5)
    # scrawled signature (dark ink)
    sig = [(560, 430), (610, 380), (650, 445), (720, 375), (790, 450), (860, 385), (930, 452)]
    d.line(sig, fill=(24, 26, 34), width=8, joint="curve")
    # red FALSE stamp (rotated, hollow) — accent, not a bright core
    stamp = Image.new("RGBA", (520, 200), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sf = font(FONT_IMPACT, 150)
    sd.rectangle([8, 8, 512, 192], outline=(196, 40, 40, 235), width=12)
    sd.text((30, 18), "FALSE", font=sf, fill=(196, 40, 40, 235))
    stamp = stamp.rotate(-11, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (470, 200), stamp)
    return img


def subj_fingerprint(img):
    """A fingerprint card panel + a large fingerprint whorl in electric blue, and a small
    'no match' bracket. Symbolic of fabricated forensic evidence."""
    img = add_glow(img, 380, 340, 330, 320, (30, 80, 180), strength=110, blur=140)
    d = ImageDraw.Draw(img)
    # fingerprint card on the right
    d.rectangle([820, 110, 1160, 610], fill=(150, 148, 138), outline=(96, 94, 86), width=6)
    d.rectangle([860, 150, 1120, 176], fill=(104, 102, 94))
    for i in range(6):
        d.line([880, 230 + i * 58, 1100, 230 + i * 58], fill=(104, 102, 94), width=5)
    # big fingerprint whorl (blue)
    cx, cy = 380, 350
    for i in range(16):
        rr = 40 + i * 17
        bbox = [cx - rr, cy - int(rr * 1.16), cx + rr, cy + int(rr * 1.16)]
        start = 20 + i * 8
        end = 300 + i * 6
        d.arc(bbox, start, end, fill=(70, 140, 240), width=7)
    d.arc([cx - 20, cy - 24, cx + 20, cy + 24], 0, 360, fill=(120, 180, 255), width=7)
    return img


def score(path):
    im = Image.open(path).convert("L")
    st = ImageStat.Stat(im)
    return {"file": path.name, "mean_luma": round(st.mean[0], 2), "contrast_std": round(st.stddev[0], 2)}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(subject_fn, line1, line2, kicker, out, accent2=GOLD):
    img = background()
    img = subject_fn(img)
    img = clamp_highlights(img)
    img = headline(img, line1, line2, kicker, accent2)
    # PD logo bottom-right
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
    specs = [
        (subj_interrogation, "POLICE CAN", "LIE TO YOU", "AND IT'S 100% LEGAL", GOLD),
        (subj_confession, "HE CONFESSED", "TO A LIE", "FALSE CONFESSION · 16 YEARS", GOLD),
        (subj_fingerprint, "IS THIS", "LEGAL?", "DNA LATER PROVED HIM INNOCENT", BLUE),
    ]
    paths = []
    for i, (fn, l1, l2, kick, acc) in enumerate(specs, 1):
        p = OUT / f"thumbnail.v002-{i:02d}.png"
        build(fn, l1, l2, kick, p, acc)
        paths.append(p)
        print(f"  option {i}: {p.name}  ({l1} {l2} / {kick})")
    selected = OUT / "thumbnail.selected.v002.png"
    shutil.copy2(paths[0], selected)
    # remove failing v001 selected/options so the newest selected is v002
    for old in OUT.glob("thumbnail.v001-*.png"):
        old.unlink()
    old_sel = OUT / "thumbnail.selected.v001.png"
    if old_sel.exists():
        old_sel.unlink()
    report = {
        "episode_id": "PD-2026-039-frazier",
        "selected": selected.name,
        "selected_sha256": "sha256:" + sha256(selected),
        "visibility": [score(p) for p in [*paths, selected]],
    }
    (OUT / "thumbnail_visibility.stub.v002.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("selected ->", selected.name)
    print(json.dumps(report["visibility"], ensure_ascii=False))


if __name__ == "__main__":
    main()
