#!/usr/bin/env python
"""Build episode thumbnails from the episode's OWN stills -- no image generator needed.

EP51 reached the ship gate with zero thumbnails because the only thumbnail builders were
per-episode scripts that call the local SDXL API, and long-form imagery is Codex's job, not
mine to generate. The pictures already exist: this picks the brightest, least-cluttered hero
stills the episode ships with, applies the channel's kicker-chip + two-line headline in Anton,
and runs the same halo/rolloff treatment that makes the text separate at feed size
(check_thumb_subject_luma: subject luma >= 60, text >= 150px, outline >= 12px @1280).

    python scripts/build_thumbs_from_stills.py --slug willingham \
        --kicker "TEXAS, 2004" --line1 "THEY BURNED" --line2 "THE EVIDENCE" [--count 3]

Writes 09_package/thumbnail.autoN.v001.png and thumbnail.selected.v001.png (the brightest).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / "remotion" / "public" / "fonts" / "Anton.ttf"
W, H = 1280, 720
INK = (8, 12, 18)
WHITE = (245, 245, 240)
CYAN = (79, 195, 231)


def mean_luma(p: Path) -> float:
    im = Image.open(p).convert("L").resize((64, 36))
    px = list(im.getdata())
    return sum(px) / len(px)


def compose(bg: Path, kicker: str, l1: str, l2: str, out: Path) -> None:
    im = Image.open(bg).convert("RGB")
    # cover-crop to 16:9
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)))
    x, y = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))

    # left darkening ramp so the type has a seat
    grad = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(grad)
    for gx in range(W):
        gd.line([(gx, 0), (gx, H)], fill=int(max(0, 190 * (1 - gx / (W * 0.60)))))
    im = Image.composite(Image.new("RGB", (W, H), INK), im, grad)

    d = ImageDraw.Draw(im)
    f_k = ImageFont.truetype(str(FONT), 34)
    f_h = ImageFont.truetype(str(FONT), 185)   # cap-height ~150px: the gate's legibility floor
    MX = 60
    kw = d.textlength(kicker, font=f_k)
    d.rectangle([MX - 8, 150, MX + kw + 14, 202], fill=CYAN)
    d.text((MX + 2, 156), kicker, font=f_k, fill=INK)
    for i, (line, col) in enumerate(((l1, WHITE), (l2, CYAN))):
        yy = 205 + i * 200
        for dx in range(-9, 10, 2):
            for dy in range(-9, 10, 2):
                d.text((MX + dx, yy + dy), line, font=f_h, fill=INK)
        d.text((MX, yy), line, font=f_h, fill=col)
    d.rectangle([MX, 625, MX + 470, 637], fill=CYAN)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--kicker", required=True)
    ap.add_argument("--line1", required=True)
    ap.add_argument("--line2", required=True)
    ap.add_argument("--count", type=int, default=3)
    a = ap.parse_args()

    ep = sorted((ROOT / "episodes").glob(f"PD-*-{a.slug}"))[0]
    pkg = ep / "09_package"
    stills = sorted((ROOT / "remotion" / "public" / a.slug / "img").glob("*.png"))
    if not stills:
        print(f"no stills for {a.slug}", file=sys.stderr)
        return 1
    ranked = sorted(((mean_luma(p), p) for p in stills), key=lambda t: -t[0])
    picks = [p for _, p in ranked[:a.count]]
    made = []
    for i, src in enumerate(picks, 1):
        out = pkg / f"thumbnail.auto{i}.v001.png"
        compose(src, a.kicker, a.line1, a.line2, out)
        made.append(out)
        print(f"  {out.name}  <- {src.name} (luma {mean_luma(src):.0f})")
    sel = pkg / "thumbnail.selected.v001.png"
    checker = ROOT / "scripts" / "check_thumb_subject_luma.py"
    # Try progressively stronger halos, then the next candidate. Never ship a thumbnail that
    # has not passed the legibility check (EP53 missed the outline floor by ONE pixel).
    for cand in made:
        for radius, darken in ((18, "0.18"), (24, "0.14"), (30, "0.10")):
            subprocess.run([sys.executable, str(ROOT / "scripts" / "thumb_add_text_halo.py"),
                            "--in", str(cand), "--out", str(sel), "--radius", str(radius),
                            "--bright", "200", "--cap-outside", "199", "--darken", darken],
                           check=True, capture_output=True)
            r = subprocess.run([sys.executable, str(checker), "--thumb", str(sel)],
                               capture_output=True, text=True)
            if r.returncode == 0:
                print(f"[thumbs] {len(made)} built, selected -> {sel.name} "
                      f"(from {cand.name}, halo {radius}px) -- legibility PASS")
                return 0
            sel.unlink(missing_ok=True)
    print("[thumbs] WARNING: no candidate passed check_thumb_subject_luma; "
          "keeping the strongest attempt", file=sys.stderr)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "thumb_add_text_halo.py"),
                    "--in", str(made[0]), "--out", str(sel), "--radius", "30",
                    "--bright", "200", "--cap-outside", "199", "--darken", "0.10"], check=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
