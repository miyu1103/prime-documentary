#!/usr/bin/env python3
"""Composite validated EP39 AE cards over a finished base render."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDIT = ROOT / "episodes" / "PD-2026-039-frazier" / "08_edit"
WORK = EDIT / "ae_hero"
RENDER = WORK / "render"
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
W, H, FPS = 1920, 1080, 30


def probe_duration(path: Path) -> float:
    result = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except ValueError:
        return -1.0


def probe_dimensions(path: Path) -> str:
    result = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)], capture_output=True, text=True)
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    if not args.base.exists():
        print(f"MISSING base {args.base}", file=sys.stderr)
        return 2
    cards_file = WORK / "cards.json"
    if not cards_file.exists():
        print(f"MISSING cards {cards_file}", file=sys.stderr)
        return 2
    cards = json.loads(cards_file.read_text(encoding="utf-8"))["cards"]
    base_duration = probe_duration(args.base)
    valid, skipped = [], []
    for card in cards:
        mp4 = RENDER / f"{card['id']}.mp4"
        duration = probe_duration(mp4) if mp4.exists() else -1
        dimensions = probe_dimensions(mp4) if mp4.exists() else ""
        if not mp4.exists():
            skipped.append((card["id"], "missing mp4"))
        elif dimensions != f"{W}x{H}":
            skipped.append((card["id"], f"wrong size {dimensions}"))
        elif duration < float(card["dur"]) - 0.3:
            skipped.append((card["id"], f"short {duration:.2f}<{float(card['dur']):.2f}"))
        elif float(card["end"]) > base_duration:
            skipped.append((card["id"], "window past end"))
        else:
            valid.append({**card, "mp4": mp4})
    for card_id, reason in skipped:
        print(f"[SKIP] {card_id}: {reason}", file=sys.stderr)
    if not valid:
        print("no valid cards - nothing to composite", file=sys.stderr)
        return 3

    inputs = ["-i", str(args.base)]
    filters, previous = [], "0:v"
    for index, card in enumerate(valid):
        inputs.extend(["-i", str(card["mp4"])])
        input_index = index + 1
        filters.append(f"[{input_index}:v]setpts=PTS-STARTPTS+{float(card['start']):.3f}/TB,format=yuv420p[b{index}]")
        output = f"v{index}"
        filters.append(f"[{previous}][b{index}]overlay=0:0:eof_action=pass:enable='between(t,{float(card['start']):.3f},{float(card['end']):.3f})'[{output}]")
        previous = output
    args.out.parent.mkdir(parents=True, exist_ok=True)
    command = [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(filters), "-map", f"[{previous}]", "-map", "0:a", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy", str(args.out)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        print(result.stderr[-3000:], file=sys.stderr)
        return 4
    output_duration = probe_duration(args.out)
    print(f"[done] {args.out.name} dur={output_duration:.2f}s {probe_dimensions(args.out)} cards={len(valid)} skipped={len(skipped)}")
    if abs(output_duration - base_duration) > 0.5:
        print(f"WARN duration drift {output_duration:.2f} vs {base_duration:.2f}", file=sys.stderr)
    return 0 if not skipped else 5


if __name__ == "__main__":
    raise SystemExit(main())
