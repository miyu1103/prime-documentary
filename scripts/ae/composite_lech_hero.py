#!/usr/bin/env python
"""Composite EP40 Lech AE hero beats over the finished CaseFilm."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-040-lech"
EDIT = ROOT / "episodes" / EP / "08_edit"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
W, H, FPS = 1920, 1080, 30


def probe_dur(f: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def probe_wh(f: Path) -> str:
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(f)], capture_output=True, text=True)
    return r.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("base", nargs="?", type=Path)
    ap.add_argument("out", nargs="?", type=Path)
    ap.add_argument("--dryrun", action="store_true")
    args = ap.parse_args()
    work = EDIT / ("_dryrun/ae_hero" if args.dryrun else "ae_hero")
    render = work / "render"
    base = args.base or (EDIT / "_dryrun" / "lech_final_bgm.v002.mp4" if args.dryrun else EDIT / "lech_final_bgm.v002.mp4")
    out = args.out or (EDIT / "_dryrun" / "lech_final_bgm.v003_ae.mp4" if args.dryrun else EDIT / "lech_final_bgm.v003_ae.mp4")
    if not base.exists():
        print(f"MISSING base {base}", file=sys.stderr)
        return 2
    beats = json.loads((work / "beats.json").read_text(encoding="utf-8")).get("beats", [])
    base_dur = probe_dur(base)
    print(f"[base] {base.name} dur={base_dur:.2f}s {probe_wh(base)}")
    valid, skipped = [], []
    for b in beats:
        mp4 = render / f"{b['id']}.mp4"
        if not mp4.exists():
            skipped.append((b["id"], "missing mp4"))
            continue
        d, wh = probe_dur(mp4), probe_wh(mp4)
        if wh != f"{W}x{H}":
            skipped.append((b["id"], f"wrong size {wh}"))
            continue
        if d < b["dur"] - 0.3:
            skipped.append((b["id"], f"short {d:.2f}<{b['dur']:.2f}"))
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
        out_label = f"v{k}"
        blend_mode = b.get("blend_mode", "overlay")
        if blend_mode in {"screen", "multiply"}:
            parts.append(
                f"[{prev}][b{k}]blend=all_mode={blend_mode}:shortest=0:repeatlast=0:"
                f"enable='between(t,{b['start']:.3f},{b['end']:.3f})'[{out_label}]"
            )
        else:
            parts.append(f"[{prev}][b{k}]overlay=0:0:eof_action=pass:enable='between(t,{b['start']:.3f},{b['end']:.3f})'[{out_label}]")
        prev = out_label
    cmd = [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(parts), "-map", f"[{prev}]", "-map", "0:a", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:], file=sys.stderr)
        return 4
    od = probe_dur(out)
    print(f"[done] {out.name} dur={od:.2f}s {probe_wh(out)}")
    if abs(od - base_dur) > 0.5:
        print(f"WARN duration drift {od:.2f} vs {base_dur:.2f}", file=sys.stderr)
        return 5
    if skipped:
        print(f"NOTE: {len(skipped)} beat(s) skipped: " + ", ".join(s for s, _ in skipped), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
