#!/usr/bin/env python
"""Composite AE hero cards over a finished PD film using SCRIM + LUMAKEY (not opaque overlay).

WHY THIS EXISTS (measured on EP50, 2026-07-29 -- see PD_FAILURE_REGISTRY.v001.md F-12):
the previous method (`composite_<slug>_hero.py`) overlaid each AE card OPAQUE and full-frame.
Measuring all 36 EP50 cards showed the deck is structurally unfit for that:

  * 21/36 cards have mean luma < 20 and >=98% of pixels below luma 25.5
    -> `blackdetect=d=1.2:pic_th=0.98` correctly reports them as BLACK.
  * 18/36 cards are FROZEN from ~50% of their duration onward (the AE animation
    finishes in ~2-3s, then holds a dead still for the remaining 3-5s)
    -> `freezedetect=n=-60dB:d=4.0` correctly reports FREEZE.

Opaque compositing therefore replaces ~3.6 minutes of a 61-minute film with dark static
cards, which is exactly the kamishibai failure the house style bans.

THE FIX (validated on a 14s prototype before any full-length spend):
  1. Dim the BASE film inside every card window (`lutyuv y=val*SCRIM`) instead of hiding it.
  2. Knock the card's near-black background out with `lumakey`, keeping text/rules/glyphs
     at full alpha, and overlay that.
Result: the film keeps MOVING under the graphics (no freeze), the frame is never >=98%
black (no black stretch), and the card's typography stays fully opaque and legible.

Measured on the EP50 B8 window (base luma 168.7 = the brightest card window of the 36):
  opaque:      luma 13.7, frozen 4.0s of 7.0s, blackdetect FAIL, freezedetect FAIL
  scrim+key:   luma 21-34, no frozen pair, blackdetect clean, freezedetect clean

Base brightness under EP50's 36 windows ranges 30.9-168.7, so a fixed scrim is safe:
card typography is composited OPAQUE (lumakey only removes the dark background), so
legibility does not depend on how bright the base happens to be.

Usage:
  py -3.11 scripts/ae/composite_hero_scrimkey.py --beats <beats.json> --base <in.mp4> --out <out.mp4>
      [--scrim 0.30] [--key-threshold 0.12] [--key-tolerance 0.10] [--key-softness 0.15]
      [--preset medium] [--crf 16] [--dry-run]

Exit codes: 0 ok / 2 bad args or missing input / 3 no valid beats / 4 ffmpeg failed
            / 5 output duration drifted from the base by > 0.5s.

ALWAYS run scripts/pd_postrender_gate.py on the output afterwards -- compositing is exactly
the step that historically introduced black/freeze (PD_IRONCLAD_GATES.v001.md).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
W, H, FPS = 1920, 1080, 30


def probe_dur(path: Path) -> float:
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def probe_wh(path: Path) -> str:
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
         "-of", "csv=p=0:s=x", str(path)], capture_output=True, text=True)
    return r.stdout.strip()


def select_beats(beats: list[dict], render: Path, offset: float, base_dur: float) -> tuple[list[dict], list[tuple[str, str]]]:
    """Same SKIP contract as the original compositor: missing / wrong-size / short / past-end."""
    valid: list[dict] = []
    skipped: list[tuple[str, str]] = []
    for b in beats:
        mp4 = render / f"{b['id']}.mp4"
        abs_start = float(b["start"]) + offset
        abs_end = float(b["end"]) + offset
        if not mp4.exists():
            skipped.append((b["id"], "missing render"))
            continue
        dur = probe_dur(mp4)
        wh = probe_wh(mp4)
        if wh != f"{W}x{H}":
            skipped.append((b["id"], f"wrong size {wh}"))
        elif dur < float(b["dur"]) - 0.3:
            skipped.append((b["id"], f"short {dur:.2f}"))
        elif abs_end > base_dur:
            skipped.append((b["id"], "window past end"))
        else:
            valid.append({**b, "mp4": mp4, "abs_start": abs_start, "abs_end": abs_end})
    return valid, skipped


def build_filtergraph(valid: list[dict], scrim: float, thr: float, tol: float, soft: float) -> tuple[list[str], str]:
    """One shared scrim pass (OR of every card window) then one keyed overlay per card."""
    parts: list[str] = []
    # `enable` takes a numeric expression: summing between() gives a non-zero (true) value
    # inside ANY card window, so a single dim+overlay pass covers all of them.
    windows = "+".join(f"between(t,{b['abs_start']:.3f},{b['abs_end']:.3f})" for b in valid)
    parts.append("[0:v]split=2[b0][b1]")
    parts.append(f"[b1]lutyuv=y='val*{scrim:.3f}'[dim]")
    parts.append(f"[b0][dim]overlay=0:0:enable='{windows}'[scr]")
    prev = "scr"
    for i, b in enumerate(valid):
        # setpts shifts the card onto absolute film time; lumakey turns its near-black
        # background transparent while leaving typography fully opaque.
        parts.append(
            f"[{i + 1}:v]setpts=PTS-STARTPTS+{b['abs_start']:.3f}/TB,format=yuva420p,"
            f"lumakey=threshold={thr}:tolerance={tol}:softness={soft}[k{i}]")
        lbl = f"v{i}"
        parts.append(
            f"[{prev}][k{i}]overlay=0:0:eof_action=pass:"
            f"enable='between(t,{b['abs_start']:.3f},{b['abs_end']:.3f})'[{lbl}]")
        prev = lbl
    return parts, prev


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--beats", type=Path, required=True, help="08_edit/ae_hero/beats.json")
    ap.add_argument("--base", type=Path, required=True, help="finished film to composite onto")
    ap.add_argument("--out", type=Path, required=True, help="output mp4 (never the base)")
    ap.add_argument("--render", type=Path, default=None, help="dir of <beat id>.mp4 (default: beats.json's sibling render/)")
    ap.add_argument("--scrim", type=float, default=0.30, help="base luma multiplier inside card windows")
    ap.add_argument("--key-threshold", type=float, default=0.12)
    ap.add_argument("--key-tolerance", type=float, default=0.10)
    ap.add_argument("--key-softness", type=float, default=0.15)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--dry-run", action="store_true", help="print the ffmpeg command, write nothing")
    a = ap.parse_args()

    if not a.base.exists():
        print(f"MISSING base {a.base}")
        return 2
    if not a.beats.exists():
        print(f"MISSING beats {a.beats}")
        return 2
    if a.base.resolve() == a.out.resolve():
        print("REFUSE base==out")
        return 2
    if a.out.exists() and not a.dry_run:
        print(f"REFUSE overwrite existing {a.out} (immutable revisions: pick a new version)")
        return 2

    doc = json.loads(a.beats.read_text(encoding="utf-8"))
    beats = doc.get("beats", [])
    offset = float(doc.get("film_offset_sec", 11.5))
    render = a.render or (a.beats.parent / "render")
    base_dur = probe_dur(a.base)

    valid, skipped = select_beats(beats, render, offset, base_dur)
    for sid, why in skipped:
        print(f"[SKIP] {sid}: {why}", file=sys.stderr)
    print(f"[composite] valid={len(valid)} skipped={len(skipped)} offset={offset} "
          f"scrim={a.scrim} base_dur={base_dur:.1f}s", file=sys.stderr)
    if not valid:
        print("no valid beats - nothing to composite")
        return 3

    inputs = ["-i", str(a.base)]
    for b in valid:
        inputs += ["-i", str(b["mp4"])]
    parts, last = build_filtergraph(valid, a.scrim, a.key_threshold, a.key_tolerance, a.key_softness)
    cmd = [FFMPEG, "-y", "-hide_banner", *inputs,
           "-filter_complex", ";".join(parts),
           "-map", f"[{last}]", "-map", "0:a?",
           "-r", str(FPS), "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-c:a", "copy", str(a.out)]
    if a.dry_run:
        print(" ".join(cmd))
        return 0

    a.out.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:])
        return 4
    od = probe_dur(a.out)
    print(f"wrote {a.out} dur={od:.2f}s cards={len(valid)} scrim={a.scrim}")
    if abs(od - base_dur) > 0.5:
        print(f"DURATION DRIFT: out {od:.2f}s vs base {base_dur:.2f}s")
        return 5
    print("NEXT: py -3.11 scripts/pd_postrender_gate.py "
          f"{a.out} --expect-sec {base_dur:.1f} --frames 30 --out qc_frames_<name>")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
