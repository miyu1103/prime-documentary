#!/usr/bin/env python3
r"""EP29 hinton — post-render BGM ducking mix + mux (bgm_plan.v001).

Builds a continuous, chaptered music bed (hook->opening->explainer->tension->
somber->reveal->outro, crossfaded, + faint glue drone so there is never a >25s gap),
side-chain ducks it under the ElevenLabs VO taken from the rendered mp4, 2-pass-ish
loudnorm to -14 LUFS, and muxes it back onto the video stream (copy).

Satisfies the hard gates bgm_present (continuous bed) + bgm_ending (outro resolves at
the tail with a clean fade) + loudness (-14). Musical feel still needs an ear-check
(bgm_plan step 5) which a machine cannot do.

Usage:
  py -3.11 scripts/build_ep29_hinton_final.py --video remotion/out/hinton_v002_narr.mp4 \
      --out remotion/out/hinton_final.v001.bgm.mp4
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = Path("E:/pd-media/library/music_registry.v001.json")
MEDIA = Path("E:/pd-media")   # path_relative in the registry is media-root-relative
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
XF = 1.2                 # crossfade seconds between chapters
GLUE_VOL = 0.06          # faint continuity drone level
DUCK_FLOOR_DB = -22      # VO-present bed floor target (bgm_plan)


def dur(p: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def resolve() -> dict[str, Path]:
    reg = json.loads(REG.read_text(encoding="utf-8"))
    tracks = reg if isinstance(reg, list) else reg.get("tracks", [])
    by = {t.get("track_id"): t for t in tracks}
    ids = {"hook": "MUS-0002", "opening": "MUS-0003", "explainer": "MUS-0005",
           "tension": "MUS-0007", "somber": "MUS-0009", "reveal": "MUS-0013",
           "outro": "MUS-0016", "glue": "MUS-0018"}
    out: dict[str, Path] = {}
    for role, mid in ids.items():
        p = MEDIA / by[mid]["path_relative"]
        if not p.exists():
            raise SystemExit(f"MISS {role} {mid}: {p}")
        out[role] = p
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    video = Path(args.video)
    if not video.exists():
        raise SystemExit(f"no video: {video}")
    tr = resolve()
    TARGET = dur(video)
    outro_len = dur(tr["outro"])
    body_target = TARGET - outro_len + XF
    order = ["hook", "opening", "explainer", "tension", "somber", "reveal"]

    inputs: list[str] = []
    for role in order:
        inputs += ["-i", str(tr[role])]
    inputs += ["-i", str(tr["outro"]), "-i", str(tr["glue"]), "-i", str(video)]
    G = len(order) + 1  # glue input index
    V = len(order) + 2  # video input index

    # body crossfade chain 0..5 -> trim -> crossfade outro -> ends at TARGET
    fc = f"[0][1]acrossfade=d={XF}:c1=tri:c2=tri[b1];"
    for i in range(2, len(order)):
        fc += f"[b{i-1}][{i}]acrossfade=d={XF}[b{i}];"
    fc += f"[b{len(order)-1}]atrim=0:{body_target:.2f},asetpts=N/SR/TB[body];"
    fc += f"[body][{len(order)}]acrossfade=d={XF}[full0];"
    # glue drone looped to TARGET, faint, mixed under
    fc += f"[{G}]aloop=loop=-1:size=200000000,atrim=0:{TARGET:.2f},asetpts=N/SR/TB,volume={GLUE_VOL}[glue];"
    fc += f"[full0][glue]amix=inputs=2:normalize=0:duration=first[bed0];"
    # bed sits BELOW the VO: drop its base level so even in gaps it never fights the voice
    fc += f"[bed0]afade=t=out:st={TARGET-1.8:.2f}:d=1.8,volume=0.42[bed];"
    # VO from the rendered video, pushed FORWARD (+~5dB) and split for playback + sidechain key
    fc += f"[{V}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.8,asplit=2[vo][key];"
    # duck the bed HARD under the VO (deep floor, fast attack) so narration is always on top
    fc += ("[bed][key]sidechaincompress=threshold=0.02:ratio=16:attack=5:release=260:"
           "makeup=1:level_sc=1.2[duck];")
    # VO first (dominant) + ducked bed, limit, normalize to -14 LUFS
    fc += ("[vo][duck]amix=inputs=2:normalize=0:weights=1.0 0.7:duration=first,"
           "alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11[a]")

    cmd = [FFMPEG, "-y", *inputs, "-filter_complex", fc,
           "-map", f"{V}:v", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
           "-movflags", "+faststart", args.out]
    print("TARGET", round(TARGET, 2), "body_target", round(body_target, 2), "outro", round(outro_len, 2))
    r = subprocess.run(cmd)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg exit {r.returncode}")
    print("WROTE", args.out, round(dur(Path(args.out)), 2), "s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
