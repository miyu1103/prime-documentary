#!/usr/bin/env python
"""Composite EP41 Thompson AE hero beats over the finished CaseFilm.

BASE = thompson_final_bgm.v001.mp4  ->  OUT = thompson_final_bgm.v002_ae.mp4
The shipped v001 is NEVER overwritten (DESIGN v001 section 6.7).

SKIP conditions (all four preserved verbatim from the design):
  1. render/<id>.mp4 missing            -> SKIP
  2. resolution != 1920x1080            -> SKIP
  3. measured dur < beat.dur - 0.3      -> SKIP
  4. beat.end > base_dur (or start/end  -> SKIP  (start/end are null until the
     unset)                                       film timeline is locked)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-041-thompson"
EDIT = Path("E:/pd-media/episodes") / EP / "08_edit"
WORK = EDIT / "ae_hero"
RENDER = WORK / "render"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
W, H, FPS = 1920, 1080, 30


def probe_dur(f: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def probe_wh(f: Path) -> str:
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of",
                        "csv=p=0:s=x", str(f)], capture_output=True, text=True)
    return r.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("base", nargs="?", type=Path,
                    default=EDIT / "thompson_final_bgm.v001.mp4")
    ap.add_argument("out", nargs="?", type=Path,
                    default=EDIT / "thompson_final_bgm.v002_ae.mp4")
    args = ap.parse_args()
    base, out = args.base, args.out
    if base.resolve() == out.resolve():
        print("REFUSE base==out (never overwrite shipped v001)", file=sys.stderr)
        return 2
    if not base.exists():
        print(f"MISSING base {base} -- render the film first, then composite",
              file=sys.stderr)
        return 2
    beats = json.loads((WORK / "beats.json").read_text(encoding="utf-8")).get("beats", [])
    base_dur = probe_dur(base)
    print(f"[base] {base.name} dur={base_dur:.2f}s {probe_wh(base)}")

    valid, skipped = [], []
    for b in beats:
        mp4 = RENDER / f"{b['id']}.mp4"
        if not mp4.exists():
            skipped.append((b["id"], "missing render"))
            continue
        d, wh = probe_dur(mp4), probe_wh(mp4)
        if wh != f"{W}x{H}":
            skipped.append((b["id"], f"wrong size {wh}"))
            continue
        if d < b["dur"] - 0.3:
            skipped.append((b["id"], f"short {d:.2f}<{b['dur']:.2f}"))
            continue
        if b.get("start") is None or b.get("end") is None:
            skipped.append((b["id"], "start/end unset (timeline not locked)"))
            continue
        if b["end"] > base_dur:
            skipped.append((b["id"], "window past end"))
            continue
        valid.append({**b, "mp4": str(mp4)})

    for sid, why in skipped:
        print(f"  [SKIP] {sid}: {why}", file=sys.stderr)
    if not valid:
        print("no valid beats - nothing to composite", file=sys.stderr)
        return 3

    inputs = ["-i", str(base)]
    parts, prev = [], "0:v"
    for k, b in enumerate(valid):
        inputs += ["-i", b["mp4"]]
        idx = k + 1
        parts.append(f"[{idx}:v]setpts=PTS-STARTPTS+{b['start']:.3f}/TB,format=yuv420p[b{k}]")
        lbl = f"v{k}"
        parts.append(f"[{prev}][b{k}]overlay=0:0:eof_action=pass:"
                     f"enable='between(t,{b['start']:.3f},{b['end']:.3f})'[{lbl}]")
        prev = lbl
    cmd = [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(parts),
           "-map", f"[{prev}]", "-map", "0:a", "-r", str(FPS), "-c:v", "libx264",
           "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-c:a", "copy", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:], file=sys.stderr)
        return 4
    od = probe_dur(out)
    print(f"[done] {out.name} dur={od:.2f}s {probe_wh(out)} beats={len(valid)}")
    if abs(od - base_dur) > 0.5:
        print(f"WARN duration drift {od:.2f} vs {base_dur:.2f}", file=sys.stderr)
        return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
