#!/usr/bin/env python3
r"""EP30 cotton — post-render BGM ducking mix + mux (mirrors build_ep29_hinton_final).

The CaseFilm render already carries the ElevenLabs master VO on its audio track. This
takes the pre-built continuous cotton music bed (build_cotton_bgm_bed.py -> hook ->
explainer -> tension -> somber -> reveal -> outro, resolved + faded at the tail),
side-chain ducks it under that VO, mixes, limits, normalizes to -14 LUFS, and muxes it
back onto the video stream (copy). Satisfies bgm_present + bgm_ending + loudness while
leaving the depth-parallax video bytes untouched.

Usage:
  py -3.11 scripts/build_cotton_final.py --video remotion/out/cotton_premium_v002.mp4 \
      --out remotion/out/cotton_final.v002.bgm.mp4
"""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BED = ROOT / "episodes" / "PD-2026-030-cotton" / "06_audio" / "bgm_bed.v001.mp3"
FFMPEG, FFPROBE = "ffmpeg", "ffprobe"


def dur(p: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bed", default=str(BED))
    args = ap.parse_args()
    video, bed = Path(args.video), Path(args.bed)
    for p in (video, bed):
        if not p.exists():
            raise SystemExit(f"missing input: {p}")
    TARGET = dur(video)
    # inputs: 0 = bed (music), 1 = video (video + master VO)
    # Deeper ducking than v003: the owner heard the bed swell over the VO mid-video, so drop
    # the bed baseline ~5dB (volume=0.56) AND duck harder under the VO (lower threshold, higher
    # ratio, faster attack) so narration always sits clearly on top; a light gate floor keeps
    # the music present between phrases.
    fc = (
        # bed trimmed to video length, dropped ~5dB baseline; gentle tail fade already in the bed
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{TARGET:.2f},"
        f"asetpts=N/SR/TB,volume=0.56[bed];"
        # VO from the render, split for playback + sidechain key
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][key];"
        # duck the bed hard under the VO
        "[bed][key]sidechaincompress=threshold=0.025:ratio=14:attack=8:release=320:"
        "makeup=1:level_sc=1[duck];"
        # mix ducked bed + VO, limit, normalize to -14 LUFS
        "[vo][duck]amix=inputs=2:normalize=0:duration=first,"
        "alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11[a]"
    )
    cmd = [FFMPEG, "-y", "-i", str(bed), "-i", str(video), "-filter_complex", fc,
           "-map", "1:v", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
           "-movflags", "+faststart", args.out]
    print("TARGET", round(TARGET, 2), "bed", round(dur(bed), 2))
    if subprocess.run(cmd).returncode != 0:
        raise SystemExit("ffmpeg failed")
    print("WROTE", args.out, round(dur(Path(args.out)), 2), "s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
