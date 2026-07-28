#!/usr/bin/env python
"""Composite EP44 Tekoh AE hero cards over a base render."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EP = "PD-2026-044-tekoh"
EDIT = ROOT / "episodes" / EP / "08_edit"
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
W, H, FPS = 1920, 1080, 30


def probe_dur(path: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def probe_wh(path: Path) -> str:
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)], capture_output=True, text=True)
    return r.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("base", nargs="?", type=Path)
    ap.add_argument("out", nargs="?", type=Path)
    args = ap.parse_args()
    work = EDIT / "ae_hero"
    base = args.base or (EDIT / "tekoh_final_bgm.v002.mp4")
    out = args.out or (EDIT / "tekoh_final_bgm.v003_ae.mp4")
    if base.resolve() == out.resolve():
        print("REFUSE base==out")
        return 2
    if not base.exists():
        print(f"MISSING base {base}")
        return 2
    beats = json.loads((work / "beats.json").read_text(encoding="utf-8")).get("beats", [])
    render = work / "render"
    base_dur = probe_dur(base)
    valid = []
    skipped = []
    for b in beats:
        mp4 = render / f"{b['id']}.mp4"
        if not mp4.exists():
            skipped.append((b["id"], "missing render"))
            continue
        dur = probe_dur(mp4)
        wh = probe_wh(mp4)
        if wh != f"{W}x{H}":
            skipped.append((b["id"], f"wrong size {wh}"))
        elif dur < float(b["dur"]) - 0.3:
            skipped.append((b["id"], f"short {dur:.2f}"))
        elif float(b["end"]) > base_dur:
            skipped.append((b["id"], "window past end"))
        else:
            valid.append({**b, "mp4": mp4})
    for sid, why in skipped:
        print(f"[SKIP] {sid}: {why}")
    if not valid:
        print("no valid beats - nothing to composite")
        return 3
    inputs = ["-i", str(base)]
    parts = []
    prev = "0:v"
    for i, b in enumerate(valid):
        inputs += ["-i", str(b["mp4"])]
        idx = i + 1
        parts.append(f"[{idx}:v]setpts=PTS-STARTPTS+{float(b['start']):.3f}/TB,format=yuv420p[b{i}]")
        lbl = f"v{i}"
        parts.append(f"[{prev}][b{i}]overlay=0:0:eof_action=pass:enable='between(t,{float(b['start']):.3f},{float(b['end']):.3f})'[{lbl}]")
        prev = lbl
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(parts), "-map", f"[{prev}]", "-map", "0:a?", "-r", str(FPS), "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-c:a", "copy", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:])
        return 4
    od = probe_dur(out)
    print(f"wrote {out} dur={od:.2f}s beats={len(valid)}")
    return 0 if abs(od - base_dur) <= 0.5 else 5


if __name__ == "__main__":
    raise SystemExit(main())

