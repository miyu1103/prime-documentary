#!/usr/bin/env python3
"""EP41 thompson: composite the 8 rendered After-Effects hero cards (b01-b08) onto the
finished BGM film as full-frame hero beats at their narration-matched windows.

Each card is a 1920x1080 opaque render; it fully replaces the base during its window
(enable=between). Windows are BODY-relative narration timings + OFF (hook+opening=11.5s)
to reach FILM time. A beat is SKIPPED if its render is missing. Never overwrites input.

Card content -> narration anchor (body seconds):
  b01 NEW ORLEANS 1984-1985      -> 74.0   (New Orleans, 1984)
  b03 BLOOD TYPE B / THOMPSON O  -> 144.4  (crime lab typed it: type B / type O)
  b02 ON DEATH ROW / 14 YEARS    -> 176.5  (fourteen years on death row)
  b05 EXECUTION SET MAY 20       -> 265.6  (Louisiana sets the date)
  b04 WHAT THE STATE TOOK / 18Y  -> 339.5  (eighteen years, gone)
  b06 JURY AWARDED $14,000,000   -> 352.7  (fourteen million dollars)
  b07 SUPREME COURT 5 - 4        -> 380.0  (five to four, reversed)
  b08 4 PROSECUTORS KNEW         -> 471.8  (four prosecutors knew)

Usage: python scripts/composite_thompson_hero.py <bgm_in.mp4> <out_v002_ae.mp4>
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
BEATS = ROOT / "episodes" / "PD-2026-041-thompson" / "08_edit" / "ae_hero" / "beats.json"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
OFF = 8.0 + 3.5   # hookSeconds + OPENING_SEC -> body time to film time

PLACEMENTS = {  # body-relative start (seconds)
    "b01": 74.0, "b03": 144.4, "b02": 176.5, "b05": 265.6,
    "b04": 339.5, "b06": 352.7, "b07": 380.0, "b08": 471.8,
}


def probe(f):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    src = Path(sys.argv[1]); out = Path(sys.argv[2])
    if not src.exists():
        print(f"MISSING input {src}", file=sys.stderr); return 2
    if out.resolve() == src.resolve() or out.exists():
        print("REFUSING to overwrite input/existing output", file=sys.stderr); return 2
    beats = {b["id"]: b for b in json.loads(BEATS.read_text("utf-8"))["beats"]}
    total = probe(src)

    placed = []
    for bid, body_start in sorted(PLACEMENTS.items(), key=lambda kv: kv[1]):
        b = beats.get(bid)
        if not b:
            print(f"SKIP {bid}: not in beats.json"); continue
        render = Path(b["out"])
        if not render.is_file():
            print(f"SKIP {bid}: render missing {render}"); continue
        dur = probe(render)
        s = round(body_start + OFF, 3)
        e = round(s + dur, 3)
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
        # shift the card so its frame 0 lands at film time s, then gate visibility to [s,e)
        parts.append(f"[{i}:v]setpts=PTS-STARTPTS+{s}/TB,format=yuv420p[c{i}]")
    chain = "[0:v]"
    for i, (bid, render, s, e, dur) in enumerate(placed, start=1):
        lab = f"[v{i}]" if i < len(placed) else "[vout]"
        parts.append(f"{chain}[c{i}]overlay=enable='between(t,{s},{e})':eof_action=pass{lab}")
        chain = lab
    fg = ";".join(parts)

    print(f"[composite] {len(placed)} AE hero cards onto {src.name} ({total:.1f}s)")
    for bid, _, s, e, dur in placed:
        print(f"   {bid}: film {s:.1f}-{e:.1f}s ({dur:.1f}s)")
    r = subprocess.run([FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", fg,
                        "-map", "[vout]", "-map", "0:a",
                        "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                        "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-c:a", "copy", "-movflags", "+faststart", str(out)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3500:], file=sys.stderr); return 4
    print(f"WROTE {out}  ({probe(out):.1f}s, {len(placed)} AE hero cards composited)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
