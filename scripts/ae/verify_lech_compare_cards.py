#!/usr/bin/env python
"""Verify the EP40 ACT 4 comparison deck: probe, extract, measure contrast.

Self-reporting is not evidence, so this script only reports what it measured:
  1. ffprobe every ck*.mp4  -> resolution / duration / fps vs the spec
  2. extract the mid-frame  -> PNG on disk, meant to be OPENED and looked at
  3. measure real contrast  -> per text zone, from the actual rendered pixels

Contrast method: inside a named zone rectangle, the darkest pixels are the
field and the brightest are the glyph cores. Antialiased edges sit between the
two and would flatter the number, so the foreground is the 99.0th percentile
luminance and the background the 20.0th percentile. Zones with almost no glyph
coverage are reported as EMPTY rather than given a bogus ratio.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

WORK = Path("H:/pd-media/episodes/PD-2026-040-lech/08_edit/ae_hero")
SHOTS = WORK / "_compare_qc"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

# (name, x0, y0, x1, y1) in 1920x1080 space
ZONES_CASE = [
    ("state", 120, 140, 1000, 245),
    ("case_and_date", 120, 258, 1200, 375),
    ("facts", 200, 415, 1830, 790),
    ("money", 1180, 90, 1800, 340),
    ("who", 120, 840, 1830, 965),
    ("flag", 120, 975, 1830, 1025),
]
ZONES_LEDGER = [
    ("title", 120, 75, 1800, 200),
    ("headers", 120, 240, 1800, 285),
    ("col_state", 120, 310, 460, 860),
    ("col_what", 460, 310, 1400, 860),
    ("col_whopaid", 1420, 300, 1860, 870),
    ("notes", 120, 875, 1800, 1000),
]


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
         "stream=width,height,r_frame_rate,nb_frames", "-show_entries",
         "format=duration", "-of", "json", str(f)],
        capture_output=True, text=True)
    d = json.loads(r.stdout)
    s = d["streams"][0]
    num, den = (int(x) for x in s["r_frame_rate"].split("/"))
    return {"w": s["width"], "h": s["height"], "fps": num / den,
            "frames": int(s.get("nb_frames", 0)),
            "dur": float(d["format"]["duration"])}


def main() -> int:
    SHOTS.mkdir(parents=True, exist_ok=True)
    spec = json.loads((WORK / "compare_beats.json").read_text(encoding="utf-8"))
    ok = True
    rows = []
    for b in spec["beats"]:
        mp4 = WORK / f"{b['id']}.mp4"
        if not mp4.exists():
            print(f"FAIL {b['id']}: no render at {mp4}")
            ok = False
            continue
        p = probe(mp4)
        good = (p["w"] == 1920 and p["h"] == 1080
                and abs(p["fps"] - 30.0) < 0.01
                and abs(p["dur"] - b["dur"]) <= 0.10)
        ok = ok and good
        print(f"[probe] {b['id']}  {p['w']}x{p['h']} {p['fps']:.2f}fps "
              f"{p['dur']:.2f}s (spec {b['dur']:.2f}s) {'OK' if good else 'MISMATCH'}")

        # 0.62 of the runtime landed BEFORE the last footnote reveal on the
        # tally card, so the QC frame was not showing the whole card. 0.80 is
        # past every reveal on every layout and still before the tail dip.
        t = b["dur"] * 0.80
        png = SHOTS / f"{b['id']}_mid.png"
        subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
                        "-frames:v", "1", str(png)], check=True)
        img = np.asarray(Image.open(png).convert("RGB"))
        lum = srgb_lum(img)
        zones = ZONES_LEDGER if b["layout"] == "LEDGER_TABLE" else ZONES_CASE
        for name, x0, y0, x1, y1 in zones:
            patch = lum[y0:y1, x0:x1]
            fg = float(np.percentile(patch, 99.0))
            bg = float(np.percentile(patch, 20.0))
            if fg < 0.02:
                print(f"    {name:<14} EMPTY (no glyph coverage)")
                ok = False
                continue
            cr = ratio(fg, bg)
            flag = "OK " if cr >= 4.5 else "LOW"
            if cr < 4.5:
                ok = False
            print(f"    {name:<14} contrast {cr:6.2f}:1  {flag} "
                  f"(fg L={fg:.4f} bg L={bg:.4f})")
            rows.append((b["id"], name, round(cr, 2)))
        print(f"    frame -> {png}")
    worst = min(rows, key=lambda r: r[2]) if rows else None
    print()
    print(f"[summary] {len(rows)} zones measured; worst {worst}")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
