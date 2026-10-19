#!/usr/bin/env python
"""Verify LONG-FORM AE cards by reading their pixels. Self-reporting is not evidence.

ADR-0011 requires this step before a film json is built: "An AE card that rendered blank must
fail before the film json is built." `verify_lech_compare_cards.py` is the model and is left
alone -- it verifies one episode's bespoke compare deck in `E:/pd-media`. This one verifies the
generic `kinetic_card.jsx` output for ANY episode, keyed by the card KIND, so there is one
verifier rather than one per episode (invariant 14).

For each card in a jobs file:
  1. ffprobe the installed webm      -> 1920x1080 / 30 fps / duration vs `seconds`
  2. extract the frame at 0.80*dur   -> PNG on disk, meant to be OPENED and looked at
  3. measure contrast per text zone  -> from the rendered pixels, per the card's own layout

Contrast method (same as the lech verifier): inside a zone rectangle the darkest pixels are the
field and the brightest are the glyph cores; antialiased edges sit between and would flatter the
number, so foreground is the 99.0th percentile luminance and background the 20.0th. A zone with
almost no bright coverage is reported EMPTY rather than given a bogus ratio.

WHY THE FRAME IS MEASURED OVER BLACK. The webm is VP9 with a real alpha plane (render_cards.sh
proves `alpha_mode=1` before installing). ffmpeg's own decoder ignores that tag, so the frame
extracted here is the colour plane alone -- white type on the black field AE composited it
against. That is the correct thing to measure: it is the card's own ink, with nothing borrowed
from a background. It is NOT what the viewer sees; use --over to also write a version composited
on mid-grey if you want to judge legibility over picture.

Usage:
  py -3.11 scripts/ae/verify_cards.py --jobs scripts/ae/jobs_keybridge.json
  py -3.11 scripts/ae/verify_cards.py --jobs scripts/ae/jobs_keybridge.json --only keybridge_ae006
Exit 0 only when every card probed clean and every zone measured >= 4.5:1.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

W, H = 1920, 1080
MIN_CONTRAST = 4.5
SAMPLE_AT = 0.80  # past every reveal on every layout, before the 0.34 s exit

# Zones mirror kinetic_card.jsx's layout constants. When a layout constant moves there, it moves
# here -- a verifier measuring the wrong rectangle reports EMPTY on a good card and, worse, OK on
# a blank one. Each entry: (name, x0, y0, x1, y1) in 1920x1080 space.
ZONES: dict[str, list[tuple[str, int, int, int, int]]] = {
    "hero_number": [
        ("big", 200, 300, 1720, 570),
        ("label", 200, 590, 1720, 720),
    ],
    "title_card": [
        ("big", 200, 380, 1720, 660),
    ],
    "quote_card": [
        ("quote", 140, 300, 1780, 650),
        ("attribution", 400, 650, 1520, 780),
    ],
    "list_build": [
        ("headline", 300, 200, 1620, 300),
        ("items", 200, 380, 1720, 780),
    ],
    "comparison": [
        ("label_a", 110, 210, 880, 292),
        ("label_b", 1040, 210, 1810, 292),
        ("value_a", 110, 355, 880, 495),
        ("value_b", 1040, 355, 1810, 495),
        ("rows_a", 110, 545, 880, 720),
        ("rows_b", 1040, 545, 1810, 720),
        ("divider", 944, 200, 976, 700),
    ],
    "timeline": [
        ("headline", 380, 158, 1540, 272),
        ("value", 480, 315, 1440, 475),
        ("spine", 200, 574, 1720, 604),
        ("node_first", 240, 622, 940, 770),
        ("node_last", 980, 622, 1680, 770),
    ],
    "system_map": [
        ("headline", 380, 160, 1540, 246),
        ("node_first", 140, 350, 630, 612),
        ("node_last", 1290, 350, 1780, 612),
        # the connectors sit at boxY, between the panels. Measured against the 3-node geometry
        # (gutter 72): 634..706 and 1211..1283. A zone at the old y=560 reported EMPTY on a card
        # whose connectors were drawn correctly at y=480 -- the verifier was wrong, not the card.
        ("connectors", 620, 462, 1300, 500),
    ],
    "map_move": [
        ("headline", 380, 158, 1540, 252),
        ("value", 500, 268, 1420, 412),
        ("track", 160, 546, 1780, 578),
        ("target", 1440, 450, 1700, 580),
        ("mover", 1090, 530, 1290, 594),
        ("gap_bracket", 1240, 626, 1640, 672),
        ("caption", 260, 686, 1660, 768),
    ],
    "document_blowup": [
        ("headline", 380, 164, 1540, 256),
        ("frame_edge", 470, 262, 1450, 296),
        ("detail_bars", 530, 330, 1430, 530),
        ("focus", 850, 396, 1130, 444),
        ("caption", 240, 606, 1680, 800),
    ],
}


def srgb_lum(arr: np.ndarray) -> np.ndarray:
    c = arr.astype(np.float64) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]


def ratio(fg: float, bg: float) -> float:
    hi, lo = max(fg, bg), min(fg, bg)
    return (hi + 0.05) / (lo + 0.05)


def probe(f: Path) -> dict:
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,r_frame_rate", "-show_entries", "stream_tags=alpha_mode",
         "-show_entries", "format=duration", "-of", "json", str(f)],
        capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    s = d["streams"][0]
    num, den = (int(x) for x in s["r_frame_rate"].split("/"))
    return {"w": s["width"], "h": s["height"], "fps": num / den,
            "alpha": (s.get("tags") or {}).get("alpha_mode"),
            "dur": float(d["format"]["duration"])}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", required=True, help="scripts/ae/jobs_<slug>.json")
    ap.add_argument("--only", nargs="*", default=[], help="verify only these ids")
    ap.add_argument("--shots", default=None, help="where the QC frames go")
    ap.add_argument("--over", action="store_true",
                    help="also write the frame composited on mid-grey, as a viewer would see it")
    a = ap.parse_args()

    jobs = json.loads(Path(a.jobs).read_text(encoding="utf-8"))
    if a.only:
        jobs = [j for j in jobs if j["id"] in a.only]
        missing = set(a.only) - {j["id"] for j in jobs}
        if missing:
            sys.exit("no such job id: " + ", ".join(sorted(missing)))
    if not jobs:
        sys.exit("nothing to verify")

    shots = Path(a.shots) if a.shots else ROOT / "runs" / "ae_qc"
    shots.mkdir(parents=True, exist_ok=True)

    ok = True
    rows: list[tuple[str, str, float]] = []
    for j in jobs:
        jid, kind = j["id"], j.get("kind", "hero_number")
        slug = jid.split("_", 1)[0]
        webm = ROOT / "remotion" / "public" / slug / "ae" / f"{jid}.webm"
        if not webm.exists():
            print(f"FAIL {jid}: not installed at {webm}")
            ok = False
            continue
        p = probe(webm)
        want = float(j.get("seconds", 6.0))
        good = (p["w"] == W and p["h"] == H and abs(p["fps"] - 30.0) < 0.01
                and abs(p["dur"] - want) <= 0.10 and p["alpha"] == "1")
        ok = ok and good
        print(f"[probe] {jid:<18} {kind:<16} {p['w']}x{p['h']} {p['fps']:.2f}fps "
              f"{p['dur']:.2f}s (spec {want:.2f}s) alpha_mode={p['alpha']} "
              f"{'OK' if good else 'MISMATCH'}")

        t = p["dur"] * SAMPLE_AT
        png = shots / f"{jid}_mid.png"
        subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(webm),
                        "-frames:v", "1", str(png)], check=True)
        if a.over:
            grey = shots / f"{jid}_mid_on_grey.png"
            subprocess.run(
                [FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=0x6b6b6b:s={W}x{H}",
                 "-ss", f"{t:.3f}", "-c:v", "libvpx-vp9", "-i", str(webm),
                 "-filter_complex", "[0:v][1:v]overlay=shortest=1",
                 "-frames:v", "1", str(grey)], check=True)

        img = np.asarray(Image.open(png).convert("RGB"))
        lum = srgb_lum(img)
        ink = float((lum > 0.25).mean())
        if ink < 0.002:
            print(f"    !! WHOLE FRAME NEARLY BLANK: ink coverage {ink*100:.3f}%")
            ok = False
        else:
            print(f"    ink coverage {ink*100:.2f}% of frame")

        for name, x0, y0, x1, y1 in ZONES.get(kind, []):
            patch = lum[y0:y1, x0:x1]
            fg = float(np.percentile(patch, 99.0))
            bg = float(np.percentile(patch, 20.0))
            if fg < 0.02:
                print(f"    {name:<14} EMPTY (no bright coverage)")
                ok = False
                continue
            cr = ratio(fg, bg)
            if cr < MIN_CONTRAST:
                ok = False
            print(f"    {name:<14} contrast {cr:6.2f}:1  {'OK ' if cr >= MIN_CONTRAST else 'LOW'} "
                  f"(fg L={fg:.4f} bg L={bg:.4f})")
            rows.append((jid, name, round(cr, 2)))
        print(f"    frame -> {png}")

    print()
    if rows:
        worst = min(rows, key=lambda r: r[2])
        print(f"[summary] {len(rows)} zones measured across {len(jobs)} card(s); worst {worst}")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
