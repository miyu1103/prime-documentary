#!/usr/bin/env python3
"""EP42 young: composite the rendered After-Effects hero cards onto the finished BGM film
as full-frame hero beats at their narration-matched windows.

Each card (beats[].out) is a 1920x1080 opaque render that fully replaces the base during its
window. beats.json start/end are BODY/narration-relative; add film_offset_sec (hook+opening
= 11.5s) to reach FILM time. A beat is SKIPPED if its render is missing or too short. Never
overwrites the input. Modeled on the verified composite_thompson_hero.py.

Usage: python scripts/composite_young_hero.py <bgm_in.mp4> <out_v002_ae.mp4>
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
BEATS = ROOT / "episodes" / "PD-2026-042-young" / "08_edit" / "ae_hero" / "beats.json"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"


def probe(f):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: composite_young_hero.py <bgm_in.mp4> <out_v002_ae.mp4>", file=sys.stderr); return 2
    src = Path(sys.argv[1]); out = Path(sys.argv[2])
    if not src.exists():
        print(f"MISSING input {src}", file=sys.stderr); return 2
    if out.resolve() == src.resolve() or out.exists():
        print("REFUSING to overwrite input/existing output", file=sys.stderr); return 2

    doc = json.loads(BEATS.read_text("utf-8"))
    OFF = float(doc.get("film_offset_sec", 11.5))
    beats = doc["beats"]
    total = probe(src)

    placed = []
    for b in sorted(beats, key=lambda x: x["start"]):
        bid = b["id"]; render = Path(b["out"])
        if not render.is_file():
            print(f"SKIP {bid}: render missing {render}")
            if b.get("required"):
                print(f"  (required card {bid} missing — aborting to avoid a gap)", file=sys.stderr); return 3
            continue
        dur = probe(render)
        s = round(float(b["start"]) + OFF, 3)
        e = round(s + dur, 3)              # gate to the actual render length
        if e > total + 0.5:
            print(f"SKIP {bid}: window {s:.1f}-{e:.1f} past film end {total:.1f}"); continue
        placed.append((bid, str(render), s, e, dur))
    if not placed:
        print("no AE cards placed", file=sys.stderr); return 3

    # overlap guard (film time)
    for (id1, _, s1, e1, _), (id2, _, s2, e2, _) in zip(placed, placed[1:]):
        if s2 < e1:
            print(f"OVERLAP {id1}({s1:.1f}-{e1:.1f}) vs {id2}({s2:.1f}-{e2:.1f})", file=sys.stderr); return 3

    inputs = ["-i", str(src)]
    parts = []
    for i, (bid, render, s, e, dur) in enumerate(placed, start=1):
        inputs += ["-i", render]
        parts.append(f"[{i}:v]setpts=PTS-STARTPTS+{s}/TB,format=yuv420p[c{i}]")
    chain = "[0:v]"
    for i, (bid, render, s, e, dur) in enumerate(placed, start=1):
        lab = f"[v{i}]" if i < len(placed) else "[vout]"
        parts.append(f"{chain}[c{i}]overlay=enable='between(t,{s},{e})':eof_action=pass{lab}")
        chain = lab
    fg = ";".join(parts)

    print(f"[composite] {len(placed)} AE hero cards onto {src.name} ({total:.1f}s), offset {OFF}s")
    for bid, _, s, e, dur in placed:
        print(f"   {bid}: film {s:.1f}-{e:.1f}s ({dur:.1f}s)")
    r = subprocess.run([FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", fg,
                        "-map", "[vout]", "-map", "0:a",
                        "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", str(out)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:], file=sys.stderr); return r.returncode
    print(f"WROTE {out.name} ({probe(out):.1f}s, {len(placed)} AE hero cards composited)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
