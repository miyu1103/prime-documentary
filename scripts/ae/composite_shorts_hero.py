#!/usr/bin/env python
"""Composite VERTICAL AE hero beats onto an existing PD short render.

  base   remotion/out/<short>_yt.mp4            (1080x1920, 30fps, -14 LUFS aac)
  beats  remotion/out/ae_shorts/<short>/render/<id>.mp4  (from build_shorts_hero_cards.py)
  -> remotion/out/<short>_yt_ae.mp4              AE beats overlaid ON TOP (no added dur)
  -> remotion/out/<short>_yt_coverfirst_ae.mp4   + designed cover baked on first 1.5s

The overlay uses enable='between(t,start,end)' so the AE card is a brief
full-frame takeover during its window and the footage plays untouched
otherwise -- runtime is UNCHANGED. Audio is stream-copied (mix intact).
Outputs are NEW files; the scheduled *_coverfirst.mp4 is never touched.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "remotion" / "out"
FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"
W, H, FPS = 1080, 1920, 30


def probe_dur(p: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


def probe_wh(p: Path) -> str:
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x",
                        str(p)], capture_output=True, text=True)
    return r.stdout.strip()


def overlay(short_id: str) -> tuple[int, Path | None]:
    work = OUT / "ae_shorts" / short_id
    doc = json.loads((work / "beats.json").read_text(encoding="utf-8"))
    render = Path(doc["render_dir"])
    base = OUT / f"{short_id}_yt.mp4"
    out = OUT / f"{short_id}_yt_ae.mp4"
    if not base.exists():
        print(f"MISSING base {base}")
        return 2, None
    base_dur = probe_dur(base)

    valid, skipped = [], []
    for b in doc["beats"]:
        mp4 = render / f"{b['id']}.mp4"
        if not mp4.exists():
            skipped.append((b["id"], "missing render")); continue
        wh, dur = probe_wh(mp4), probe_dur(mp4)
        if wh != f"{W}x{H}":
            skipped.append((b["id"], f"wrong size {wh}"))
        elif dur < float(b["dur"]) - 0.3:
            skipped.append((b["id"], f"short {dur:.2f}"))
        elif float(b["end"]) > base_dur + 0.05:
            skipped.append((b["id"], f"window {b['end']} past end {base_dur:.2f}"))
        else:
            valid.append({**b, "mp4": mp4})
    for sid, why in skipped:
        print(f"[SKIP] {sid}: {why}")
    if not valid:
        print("no valid beats"); return 3, None

    inputs = ["-i", str(base)]
    parts, prev = [], "0:v"
    for i, b in enumerate(valid):
        inputs += ["-i", str(b["mp4"])]
        idx = i + 1
        parts.append(f"[{idx}:v]setpts=PTS-STARTPTS+{float(b['start']):.3f}/TB,format=yuv420p[b{i}]")
        lbl = f"v{i}"
        parts.append(f"[{prev}][b{i}]overlay=0:0:eof_action=pass:"
                     f"enable='between(t,{float(b['start']):.3f},{float(b['end']):.3f})'[{lbl}]")
        prev = lbl
    cmd = [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(parts),
           "-map", f"[{prev}]", "-map", "0:a?", "-r", str(FPS),
           "-c:v", "libx264", "-preset", "slow", "-crf", "16",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709",
           "-c:a", "copy", "-movflags", "+faststart", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:]); return 4, None
    od = probe_dur(out)
    print(f"[overlay] wrote {out.name}  dur={od:.3f}s  beats={len(valid)} "
          f"({', '.join(b['id'] for b in valid)})")
    if abs(od - base_dur) > 0.4:
        print(f"[overlay] WARN duration drift {od:.3f} vs base {base_dur:.3f}")
    return 0, out


def coverfirst(short_id: str, src: Path) -> tuple[int, Path | None]:
    thumb = OUT / f"{short_id}_thumb.png"
    dst = OUT / f"{short_id}_yt_coverfirst_ae.mp4"
    if not thumb.exists():
        print(f"MISSING thumb {thumb}"); return 2, None
    cmd = [FFMPEG, "-y", "-hide_banner", "-i", str(src), "-i", str(thumb),
           "-filter_complex",
           "[1:v]scale=1080:1920,setsar=1[cov];"
           "[0:v][cov]overlay=0:0:enable='lte(t,1.5)',format=yuv420p[v]",
           "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "18",
           "-preset", "medium", "-c:a", "copy", "-movflags", "+faststart", str(dst)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:]); return 4, None
    print(f"[cover] wrote {dst.name}  dur={probe_dur(dst):.3f}s")
    return 0, dst


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", required=True, choices=["short50", "short51"])
    args = ap.parse_args()
    rc, ae = overlay(args.short)
    if rc:
        raise SystemExit(rc)
    rc, _ = coverfirst(args.short, ae)
    raise SystemExit(rc)
