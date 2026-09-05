#!/usr/bin/env python
r"""EP40 Lech - composite the FIXED AE hero/compare cards onto lech_final_bgm.v003.mp4.

Why this exists instead of running scripts/ae/composite_lech_hero.py directly
----------------------------------------------------------------------------
composite_lech_hero.py reads per-card placement (start/end/blend_mode) from
ae_hero/beats.json.  The measurement-based "fixed" rebuild (build_lech_hero_cards.py,
2026-07-20 17:51) overwrote beats.json with a CARD-DEFINITION-ONLY schema that no
longer carries start/end, and it also renders to ae_hero/fixed/ rather than
ae_hero/render/.  The original placement used for the owner-approved
lech_final_bgm.v002_ae.mp4 was therefore lost.

Recovery: the approved v002_ae == the clean base (lech_final_bgm.v001.mp4) with the
AE cards overlaid.  A full 5 fps frame-difference scan of v002_ae vs v001 recovered
the exact 12 overlay windows (13 cards; ck5+ck6 share one merged window, split by a
10 fps rescan).  Card identity is fixed by chronological order + duration match.
v002_ae used only 13 of the 20 built cards; the 4 act-titles, 1 schematic and 2 seams
were skipped by the approved composite, so they are skipped here too.

This script overlays the corresponding ae_hero/fixed/<id>.mp4 (measurement-fixed text)
at the recovered windows.  Filter logic mirrors composite_lech_hero.py exactly
(setpts offset + overlay enable='between'), audio copied from the base.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
FIXED = Path("E:/pd-media/episodes/PD-2026-040-lech/08_edit/ae_hero/fixed")
BASE = Path("E:/pd-media/episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v003.mp4")
OUT = Path("E:/pd-media/episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v003_ae.mp4")
W, H, FPS = 1920, 1080, 30

# id -> (enable_start, enable_end).  Windows recovered from v002_ae vs v001 diff scan,
# padded to restore sub-threshold fade frames and capped to card duration / neighbour.
PLACEMENTS = [
    ("c01", 11.30, 15.30),
    ("c02", 29.70, 33.20),
    ("c03", 184.30, 190.80),
    ("b04", 240.70, 247.70),   # INTENTIONAL ACTS ... EXCLUDED  (owner-flagged clip)
    ("c04", 277.70, 284.70),
    ("b07", 383.90, 390.90),
    ("ck1", 458.70, 465.70),   # ACT4 state comparison (owner-flagged)
    ("ck2", 490.10, 497.10),
    ("ck3", 538.50, 545.50),
    ("ck4", 559.70, 566.70),
    ("ck5", 578.40, 584.10),
    ("ck6", 584.30, 592.60),
    ("c05", 629.10, 634.10),
]


def probe_dur(f: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(f)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def probe_wh(f: Path) -> str:
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height",
                        "-of", "default=nw=1:nk=1", str(f)], capture_output=True, text=True)
    vals = r.stdout.split()
    return "x".join(vals[:2]) if len(vals) >= 2 else r.stdout.strip()


def main() -> int:
    if not BASE.exists():
        print(f"MISSING base {BASE}", file=sys.stderr)
        return 2
    base_dur = probe_dur(BASE)
    print(f"[base] {BASE.name} dur={base_dur:.2f}s {probe_wh(BASE)}")

    valid, skipped = [], []
    for cid, start, end in PLACEMENTS:
        mp4 = FIXED / f"{cid}.mp4"
        if not mp4.exists():
            skipped.append((cid, "missing mp4")); continue
        wh = probe_wh(mp4)
        if wh != f"{W}x{H}":
            skipped.append((cid, f"wrong size {wh}")); continue
        d = probe_dur(mp4)
        window = end - start
        if d < window - 0.05:
            skipped.append((cid, f"card {d:.2f}s shorter than window {window:.2f}s")); continue
        if end > base_dur:
            skipped.append((cid, "window past end")); continue
        valid.append((cid, start, end, str(mp4), d))
        print(f"  [ok] {cid}  {start:7.2f}-{end:7.2f}  win={window:.2f}s card={d:.2f}s")

    for sid, why in skipped:
        print(f"  [SKIP] {sid}: {why}", file=sys.stderr)
    if not valid:
        print("no valid cards - nothing to composite", file=sys.stderr)
        return 3

    # overlap guard
    for (a, s0, e0, *_), (b, s1, e1, *_) in zip(valid, valid[1:]):
        if s1 < e0 - 1e-6:
            print(f"OVERLAP {a}({s0:.2f}-{e0:.2f}) vs {b}({s1:.2f}-{e1:.2f})", file=sys.stderr)
            return 6

    inputs = ["-i", str(BASE)]
    parts, prev = [], "0:v"
    for k, (cid, start, end, mp4, _d) in enumerate(valid):
        inputs += ["-i", mp4]
        idx = k + 1
        parts.append(f"[{idx}:v]setpts=PTS-STARTPTS+{start:.3f}/TB,format=yuv420p[c{k}]")
        out_label = f"v{k}"
        parts.append(
            f"[{prev}][c{k}]overlay=0:0:eof_action=pass:"
            f"enable='between(t,{start:.3f},{end:.3f})'[{out_label}]"
        )
        prev = out_label

    cmd = [FFMPEG, "-y", "-hide_banner", *inputs,
           "-filter_complex", ";".join(parts),
           "-map", f"[{prev}]", "-map", "0:a",
           "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "16",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
           "-color_trc", "bt709", "-c:a", "copy", str(OUT)]
    print(f"[composite] {len(valid)} cards -> {OUT.name}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:], file=sys.stderr)
        return 4
    od = probe_dur(OUT)
    print(f"[done] {OUT.name} dur={od:.2f}s {probe_wh(OUT)}")
    if abs(od - base_dur) > 0.5:
        print(f"WARN duration drift {od:.2f} vs {base_dur:.2f}", file=sys.stderr)
        return 5
    if skipped:
        print(f"NOTE: {len(skipped)} skipped: " + ", ".join(s for s, _ in skipped), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
