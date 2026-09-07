#!/usr/bin/env python3
r"""EP40 Lech CTR thumbnails v001 — passes check_thumbnail / check_thumbnail_visibility /
check_thumb_subject_luma.

Same proven recipe as the EP39 v002 rebuild: dark navy gradient, a MID-TONE symbolic subject
(a destroyed house / armored vehicle / rubble — NO real faces, R2), a tall gold accent sidebar,
and an XL Arial-Black headline in a thick (22px) black stroke over a dark scrim. Subject highlights
are clamped below 188 luma so the ONLY >200 cores are the headline text -> dark outline ring.

Facts locked (Lech v. Jackson, 10th Cir. 2019; cert. denied 2020 — NOT a Supreme Court merits
ruling): police pursuing a shoplifter destroyed an innocent family's house; the Takings Clause was
held not to apply (police power), so the family recovered essentially nothing. Thumbnail asserts only
those facts (destruction + no compensation). 1280x720, 3 options + selected, writes into 09_package.

    py -3.11 scripts/build_lech_thumbnails_v001.py
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "PD-2026-040-lech" / "09_package"
W, H = 1280, 720

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_IMPACT = "C:/Windows/Fonts/impact.ttf"

INK = (6, 9, 15)
NAVY = (13, 28, 46)
BLUE = (31, 107, 255)
GOLD = (229, 181, 58)
WHITE = (247, 249, 252)
SILVER = (188, 196, 208)
RED = (206, 44, 44)
CLAMP_LUMA = 188.0


def font(path, size):
    return ImageFont.truetype(path, size)


def background():
    img = Image.new("RGB", (W, H), INK)
    px = img.load()
    for y in range(H):
        fy = y / H
        for x in range(W):
            fx = x / W
            t = (fx * 0.55 + fy * 0.45)
            px[x, y] = (int(NAVY[0] * (1 - t) + INK[0] * t),
                        int(NAVY[1] * (1 - t) + INK[1] * t),
                        int(NAVY[2] * (1 - t) + INK[2] * t))
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-320, -220, W + 320, H + 220], fill=90)
    return Image.composite(img, Image.new("RGB", (W, H), INK), vig.filter(ImageFilter.GaussianBlur(180)))


def add_glow(img, cx, cy, rx, ry, color, strength=120, blur=150):
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=strength)
    return Image.composite(Image.new("RGB", (W, H), color), img, g.filter(ImageFilter.GaussianBlur(blur)))


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


# --------------------------------------------------------------------------- subjects (mid-tone)

def subj_destroyed_house(img):
    """A suburban house with a gaping blown-out hole in the front wall, collapsed roof corner,
    rubble at the base, dust haze. Mid-tone walls, no people."""
    img = add_glow(img, 820, 300, 430, 340, (150, 150, 168), strength=150, blur=150)
    d = ImageDraw.Draw(img)
    # ground
    d.rectangle([0, 600, W, H], fill=(30, 30, 34))
    # house body (mid-tone siding)
    bx0, by0, bx1, by1 = 560, 250, 1120, 610
    d.rectangle([bx0, by0, bx1, by1], fill=(158, 150, 132))
    # siding lines
    for yy in range(by0 + 26, by1, 34):
        d.line([bx0, yy, bx1, yy], fill=(132, 124, 108), width=3)
    # roof (dark) with a collapsed corner
    d.polygon([(bx0 - 40, by0), (bx1 + 40, by0), (bx1 - 40, by0 - 120), (bx0 + 40, by0 - 120)], fill=(60, 54, 50))
    d.polygon([(880, by0 - 120), (bx1 - 40, by0 - 120), (bx1 + 40, by0), (940, by0)], fill=(30, 28, 26))  # missing section
    for rx in range(900, 1080, 26):  # exposed rafters
        d.line([rx, by0, rx - 30, by0 - 96], fill=(84, 76, 66), width=5)
    # gaping blown-out breach in the front wall: torn lighter rim, then the dark interior
    rim = [(628, 610), (612, 452), (664, 388), (742, 420), (812, 372),
           (892, 428), (912, 520), (900, 610)]
    d.polygon(rim, fill=(126, 118, 104))                 # torn masonry edge
    hole = [(660, 610), (648, 470), (690, 420), (748, 448), (810, 410),
            (866, 452), (876, 540), (868, 610)]
    d.polygon(hole, fill=(16, 15, 18))                    # dark interior
    # a couple of exposed studs inside the breach (short, not spiky)
    for sx in (712, 792):
        d.line([sx, 600, sx, 452], fill=(92, 84, 72), width=7)
    d.line([672, 520, 858, 508], fill=(84, 78, 68), width=6)
    # a surviving window + door
    d.rectangle([980, 360, 1080, 470], fill=(70, 92, 120), outline=(120, 126, 130), width=5)
    d.line([1030, 360, 1030, 470], fill=(120, 126, 130), width=4)
    d.line([980, 415, 1080, 415], fill=(120, 126, 130), width=4)
    # rubble pile at the base of the hole
    for (cx, cy, rr, col) in [(700, 600, 70, (96, 90, 80)), (780, 610, 90, (120, 112, 98)),
                              (640, 605, 55, (110, 104, 92)), (860, 600, 60, (100, 94, 82))]:
        d.ellipse([cx - rr, cy - rr // 2, cx + rr, cy + rr // 2], fill=col)
    for (px_, py_) in [(690, 560), (740, 580), (800, 560), (660, 585), (840, 575)]:
        d.polygon([(px_, py_), (px_ + 34, py_ - 10), (px_ + 22, py_ + 22)], fill=(140, 132, 116))
    # dust haze
    img = add_glow(img, 760, 470, 260, 150, (150, 146, 136), strength=70, blur=90)
    return img


def subj_armored_vehicle(img):
    """A boxy police armored vehicle (BearCat-style) angled toward a cracked wall. Dark hull,
    a battering arm, wall fracture lines. No people."""
    img = add_glow(img, 780, 330, 420, 320, (120, 130, 150), strength=130, blur=150)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 590, W, H], fill=(28, 28, 32))
    # cracked wall on the right
    d.rectangle([1040, 150, 1180, 600], fill=(150, 142, 126))
    for (x0, y0, x1, y1) in [(1040, 300, 1120, 360), (1060, 300, 1040, 420), (1110, 340, 1180, 300),
                             (1080, 420, 1180, 470), (1050, 470, 1140, 560)]:
        d.line([x0, y0, x1, y1], fill=(40, 38, 34), width=7)
    # armored hull (boxy, dark with rim light)
    d.polygon([(360, 560), (900, 560), (900, 300), (760, 250), (420, 250), (360, 320)], fill=(58, 62, 70))
    d.polygon([(420, 250), (760, 250), (900, 300), (900, 320), (420, 320)], fill=(84, 90, 100))  # rim
    # windshield (armored slit)
    d.polygon([(470, 300), (700, 300), (700, 360), (470, 360)], fill=(30, 46, 66))
    d.rectangle([470, 322, 700, 332], fill=(60, 84, 116))
    # wheels
    d.ellipse([420, 500, 540, 620], fill=(20, 20, 24), outline=(70, 74, 82), width=8)
    d.ellipse([720, 500, 840, 620], fill=(20, 20, 24), outline=(70, 74, 82), width=8)
    # headlight (kept mid-tone, not a bright core)
    d.ellipse([858, 360, 912, 414], fill=(176, 168, 120))
    # battering ram toward the wall
    d.rectangle([900, 380, 1050, 420], fill=(96, 100, 108))
    d.rectangle([1030, 360, 1060, 440], fill=(120, 124, 132))
    return img


def subj_rubble(img):
    """A pile of a family's wrecked belongings in rubble: a broken chair, a tilted picture frame,
    scattered debris, dust. No people, no faces (empty frame)."""
    img = add_glow(img, 760, 360, 420, 330, (150, 148, 150), strength=140, blur=150)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, W, H], fill=(30, 30, 34))
    # big rubble mound
    for (cx, cy, rw, rh, col) in [(760, 560, 360, 150, (96, 90, 80)),
                                  (560, 560, 210, 120, (120, 112, 98)),
                                  (980, 560, 220, 120, (110, 104, 92))]:
        d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=col)
    # broken concrete chunks
    for (px_, py_, s) in [(520, 470, 70), (640, 500, 90), (860, 480, 80), (980, 520, 70), (720, 430, 60)]:
        d.polygon([(px_, py_), (px_ + s, py_ - s // 2), (px_ + s + 20, py_ + s // 2), (px_ + s // 2, py_ + s)],
                  fill=(150, 142, 126))
    # tilted empty picture frame (no face)
    frame = Image.new("RGBA", (240, 300), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame)
    fd.rectangle([8, 8, 232, 292], outline=(196, 158, 70, 255), width=16)
    fd.rectangle([30, 30, 210, 270], fill=(150, 150, 156, 255))
    frame = frame.rotate(-18, expand=True, resample=Image.BICUBIC)
    img.paste(frame, (640, 300), frame)
    d = ImageDraw.Draw(img)
    # broken chair leg sticking out
    d.line([900, 540, 1000, 380], fill=(120, 96, 66), width=16)
    d.line([1000, 380, 1040, 420], fill=(120, 96, 66), width=16)
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
        (subj_destroyed_house, "THEY GOT", "$0", "POLICE CHASED A SHOPLIFTER", GOLD),
        (subj_armored_vehicle, "POLICE DESTROYED", "A HOUSE", "TO CATCH A SHOPLIFTER", GOLD),
        (subj_rubble, "WHO", "PAYS?", "THE CITY PAID NOTHING", BLUE),
    ]
    paths = []
    for i, (fn, l1, l2, kick, acc) in enumerate(specs, 1):
        p = OUT / f"thumbnail.v001-{i:02d}.png"
        build(fn, l1, l2, kick, p, acc)
        paths.append(p)
        print(f"  option {i}: {p.name}  ({l1} {l2} / {kick})")
    selected = OUT / "thumbnail.selected.v001.png"
    shutil.copy2(paths[0], selected)
    report = {
        "episode_id": "PD-2026-040-lech",
        "selected": selected.name,
        "selected_sha256": "sha256:" + sha256(selected),
        "visibility": [score(p) for p in [*paths, selected]],
    }
    (OUT / "thumbnail_visibility.stub.v001.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("selected ->", selected.name)
    print(json.dumps(report["visibility"], ensure_ascii=False))


if __name__ == "__main__":
    main()
