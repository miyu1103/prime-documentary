# -*- coding: utf-8 -*-
"""Build a continuous ~710s BGM bed for EP30 cotton, ending on a RESOLVED outro.

Order matches the arc: hook -> explainer -> tension -> somber(11yrs) -> reveal(DNA)
-> outro(hopeful_resolved, its natural end lands at the video end + clean fade).
Crossfaded so there's no gap (bgm_present) and the outro resolves at the tail
(bgm_ending). Output is music-only; the post-render step ducks it under the VO.

Usage: python scripts/build_cotton_bgm_bed.py   -> H:/.../PD-2026-030-cotton/06_audio/bgm_bed.v001.mp3
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUS = Path("H:/pd-media/library/music")
OUT = ROOT / "episodes" / "PD-2026-030-cotton" / "06_audio" / "bgm_bed.v001.mp3"
TARGET = 710.0           # ~ video length
OUTRO_LEN = 159.68
XF = 3.0                 # crossfade seconds

TRACKS = {
    "hook": MUS / "hook" / "mus_20260614_hook_glass_air_bed_v1.mp3",
    "explainer": MUS / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v1.mp3",
    "tension": MUS / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3",
    "somber": MUS / "somber" / "mus_20260614_somber_ledger_of_ash_v1.mp3",
    "reveal": MUS / "reveal" / "mus_20260614_reveal_hidden_system_clicks_v1.mp3",
    "outro": MUS / "outro" / "mus_20260614_outro_last_frame_v1.mp3",
}


def dur(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    for k, p in TRACKS.items():
        if not p.exists():
            print(f"MISS {k}: {p}")
            return 2
    body_target = TARGET - OUTRO_LEN + XF   # body then crossfades into full outro ending at TARGET
    order = ["hook", "explainer", "tension", "somber", "reveal"]
    inputs = []
    for k in order:
        inputs += ["-i", str(TRACKS[k])]
    inputs += ["-i", str(TRACKS["outro"])]
    # body = acrossfade chain of the 5, then atrim to body_target; then crossfade outro; then fade out.
    fc = (
        f"[0][1]acrossfade=d={XF}:c1=tri:c2=tri[b1];"
        f"[b1][2]acrossfade=d={XF}[b2];"
        f"[b2][3]acrossfade=d={XF}[b3];"
        f"[b3][4]acrossfade=d={XF}[b4];"
        f"[b4]atrim=0:{body_target:.2f},asetpts=PTS-STARTPTS[body];"
        f"[body][5]acrossfade=d={XF}[full];"
        f"[full]afade=t=out:st={TARGET-2.0:.2f}:d=2.0,loudnorm=I=-20:TP=-1.5[out]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-map", "[out]",
           "-c:a", "libmp3lame", "-b:a", "256k", str(OUT)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG FAILED:\n", r.stderr[-1200:])
        return 1
    d = dur(OUT)
    print(f"wrote {OUT.name}  {d:.1f}s (target {TARGET}) — order: {'->'.join(order)}->outro(resolved+fade)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
