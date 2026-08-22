#!/usr/bin/env python3
"""Mix a ducked BGM bed under EP31's rendered narration track (post-render step).

CaseFilm renders narration only (BGM is mixed in post, per docs/07). This adds a
continuous tension bed (looped) sidechain-ducked under the voice, crossfading to a
somber resolve for the ending, with a clean fade to silence at the tail, then a
final loudnorm to ~-14 LUFS. Video stream is stream-copied (no re-encode).

Satisfies acceptance: bgm_present (continuous energy, no >25s silence, audible under
VO) + bgm_ending (resolving fade, not a full-volume chop) + loudness -16..-12.

Usage:
  ./.venv/Scripts/python.exe scripts/mix_bgm_unlock.py \
      --render episodes/PD-2026-031-unlock/08_edit/renders/unlock_casefilm.v001.mp4 \
      --out    episodes/PD-2026-031-unlock/08_edit/renders/unlock_final.v001.mp4
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUSIC = Path(r"E:\pd-media\library\music")
TENSION = MUSIC / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3"
SOMBER = MUSIC / "somber" / "mus_20260614_somber_ledger_of_ash_v1.mp3"

TAIL = 46.0        # seconds of somber resolve at the end
FADE = 2.5         # final fade-to-silence
XFADE = 4.0        # tension -> somber crossfade
BED_DB = "-15dB"   # base bed level before ducking (loudnorm re-normalizes the mix)


def dur(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    render = Path(args.render)
    out = Path(args.out)
    if not render.exists():
        sys.exit(f"render not found: {render}")
    out.parent.mkdir(parents=True, exist_ok=True)

    D = dur(render)
    body = max(1.0, D - TAIL)
    # tension bed covers [0 .. body+XFADE]; somber covers the tail; acrossfade joins them.
    fg = (
        f"[1:a]aloop=loop=-1:size=2147483647,atrim=duration={body + XFADE:.3f},"
        f"asetpts=N/SR/TB,volume={BED_DB}[bt];"
        f"[2:a]aloop=loop=-1:size=2147483647,atrim=duration={TAIL:.3f},"
        f"asetpts=N/SR/TB,volume={BED_DB}[bs];"
        f"[bt][bs]acrossfade=d={XFADE:.3f}:c1=tri:c2=tri[bed];"
        # sidechain-duck the bed against the narration (key = narration)
        f"[0:a]asplit=2[narr][key];"
        f"[bed][key]sidechaincompress=threshold=0.03:ratio=9:attack=8:release=320:makeup=1[bedduck];"
        f"[narr][bedduck]amix=inputs=2:duration=first:dropout_transition=0:weights=1.0 0.85,"
        f"afade=t=out:st={D - FADE:.3f}:d={FADE:.3f},"
        f"loudnorm=I=-14:TP=-1.5:LRA=11[outa]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", str(render),
        "-i", str(TENSION),
        "-i", str(SOMBER),
        "-filter_complex", fg,
        "-map", "0:v", "-map", "[outa]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
        "-movflags", "+faststart",
        str(out),
    ]
    print("video:", f"{D:.1f}s  body(tension)={body:.1f}s  tail(somber)={TAIL}s")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-1500:])
        return r.returncode
    print("wrote", out, f"({out.stat().st_size/1e6:.1f}MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
