#!/usr/bin/env python3
"""EP48 Glover: mux local review VO with a ducked music and ambience bed.

Input render has the review narration baked by Remotion. This replaces the audio
with the measured local review VO plus rights-cleared library music/ambience,
then loudness-normalizes to -14 LUFS. No external API calls.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-048-glover"
IDX = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
VO = Path("H:/pd-media/episodes/PD-2026-048-glover/06_voice/master/vc_master_v001.mp3")  # REAL ElevenLabs "Brian" master (was SAPI local_review)
EDIT = ROOT / "episodes" / EP / "08_edit"
LIB = Path("H:/pd-media/library")
MUS = LIB / "music"
AMB = LIB / "ambience"
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
OFF = 8.0 + 3.5


def probe(path: Path) -> float:
    r = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(r.stdout.strip())


def section_bounds() -> dict[str, tuple[float, float]]:
    data = json.loads(IDX.read_text(encoding="utf-8"))
    bounds: dict[str, list[float]] = {}
    for chunk in data["chunks"]:
        sec = str(chunk["section"])
        bounds.setdefault(sec, [10**9, -10**9])
        bounds[sec][0] = min(bounds[sec][0], float(chunk["start"]))
        bounds[sec][1] = max(bounds[sec][1], float(chunk["end"]))
    return {key: (value[0], value[1]) for key, value in bounds.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", type=Path, default=ROOT / "remotion" / "out" / "glover.mp4")
    ap.add_argument("--out", type=Path, default=EDIT / "glover_final_bgm.v002.mp4")
    args = ap.parse_args()
    if not args.render.is_file():
        print(f"MISSING render {args.render}")
        return 2
    if not VO.is_file():
        print(f"MISSING narration {VO}")
        return 2
    if args.render.resolve() == args.out.resolve():
        print("REFUSE render==out")
        return 2

    total = probe(args.render)
    bounds = section_bounds()

    def start(sec: str) -> float:
        return bounds[sec][0] + OFF

    a1, a2, a3 = start("ACT_1"), start("ACT_2"), start("ACT_3")
    ending = start("ENDING")
    vo_end = max(end for _, end in bounds.values()) + OFF
    act3_mid = (a3 + ending) / 2

    bgm = [
        (MUS / "hook/mus_20260614_hook_glass_air_bed_v1.mp3", 0.0, OFF, 0.28),
        (MUS / "opening/mus_20260614_opening_measured_arpeggio_v1.mp3", OFF, a1, 0.22),
        (MUS / "tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3", a1, a2, 0.20),
        (MUS / "somber/mus_20260614_somber_ledger_of_ash_v1.mp3", a2, a3, 0.18),
        (MUS / "reveal/mus_20260614_reveal_verdict_at_dawn_v1.mp3", a3, act3_mid, 0.21),
        (MUS / "tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3", act3_mid, ending, 0.20),
        (MUS / "reveal/mus_20260614_reveal_verdict_at_dawn_v2.mp3", ending, vo_end, 0.22),
        (MUS / "outro/mus_20260614_outro_last_frame_v1.mp3", vo_end, total, 0.24),
    ]
    amb = [
        (AMB / "amb_highway_traffic.mp3", 0.0, a1),
        (AMB / "amb_engine_idle.mp3", a1, a2),
        (AMB / "amb_courtroom_room_tone.mp3", a2, a3),
        (AMB / "amb_institutional_drone.mp3", a3, ending),
        (AMB / "amb_night_window.mp3", ending, vo_end),
        (AMB / "amb_light_wind.mp3", vo_end, total),
    ]
    for row in [*bgm, *amb]:
        if not row[0].is_file():
            print(f"MISSING bed {row[0]}")
            return 2

    inputs = ["-i", str(VO)]
    parts = [
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(OFF * 1000)}|{int(OFF * 1000)},apad,atrim=0:{total:.3f},asplit=2[vo][vokey]"
    ]
    labels = []
    idx = 1
    for i, (path, begin, end, volume) in enumerate(bgm):
        dur = max(0.1, end - begin)
        label = f"m{i}"
        inputs += ["-i", str(path)]
        parts.append(
            f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,aloop=loop=-1:size=2000000000,atrim=0:{dur:.3f},"
            f"afade=t=in:st=0:d=1.2,afade=t=out:st={max(0, dur - 1.8):.3f}:d=1.8,volume={volume:.3f},"
            f"adelay={int(begin * 1000)}|{int(begin * 1000)}[{label}]"
        )
        labels.append(f"[{label}]")
        idx += 1
    parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0[music_raw]")
    parts.append("[music_raw][vokey]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=320:makeup=1[music]")

    labels = []
    for i, (path, begin, end) in enumerate(amb):
        dur = max(0.1, end - begin)
        label = f"a{i}"
        inputs += ["-i", str(path)]
        parts.append(
            f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,aloop=loop=-1:size=2000000000,atrim=0:{dur:.3f},"
            f"afade=t=in:st=0:d=1.0,afade=t=out:st={max(0, dur - 1.3):.3f}:d=1.3,volume=0.12,"
            f"adelay={int(begin * 1000)}|{int(begin * 1000)}[{label}]"
        )
        labels.append(f"[{label}]")
        idx += 1
    parts.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0[amb]")
    parts.append(f"[vo][music][amb]amix=inputs=3:normalize=0:weights=1.0 0.9 0.8:dropout_transition=0,atrim=0:{total:.3f}[pre]")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    work = args.out.with_name("_glover_bgm_pre.wav")
    mix = subprocess.run(
        [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", ";".join(parts), "-map", "[pre]", "-ar", "48000", "-ac", "2", str(work)],
        capture_output=True,
        text=True,
    )
    if mix.returncode:
        print(mix.stderr[-3000:])
        return 3

    ln1 = subprocess.run(
        [FFMPEG, "-hide_banner", "-i", str(work), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    stats = json.loads(ln1[ln1.rfind("{"): ln1.rfind("}") + 1])
    loudnorm = (
        f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:linear=true"
    )
    mux = subprocess.run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-i",
            str(args.render),
            "-i",
            str(work),
            "-af",
            loudnorm,
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "320k",
            "-ar",
            "48000",
            "-shortest",
            str(args.out),
        ],
        capture_output=True,
        text=True,
    )
    work.unlink(missing_ok=True)
    if mux.returncode:
        print(mux.stderr[-3000:])
        return 4
    print(f"PASS build_glover_bgm_real {args.out} dur={probe(args.out):.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
