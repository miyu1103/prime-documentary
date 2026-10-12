"""Mix PD-2026-004-ftx narration + existing music + ambience + SFX."""

from __future__ import annotations

import subprocess
from pathlib import Path


EP = "PD-2026-004-ftx"
MEDIA = Path(r"E:\pd-media")
LIB = MEDIA / "library"
NARR = MEDIA / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
OUT_DIR = MEDIA / "episodes" / EP / "06_audio"
TMP = MEDIA / "episodes" / EP / "tmp" / "audio_mix"
FFMPEG = "ffmpeg"

TOTAL = 720.0

MUSIC = [
    (LIB / "music/hook/mus_20260614_hook_glass_air_bed_v2.mp3", 0.0, 56.9, 0.12),
    (LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v1.mp3", 56.9, 106.2, 0.12),
    (LIB / "music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v1.mp3", 106.2, 234.0, 0.105),
    (LIB / "music/reveal/mus_20260614_reveal_hidden_system_clicks_v2.mp3", 234.0, 402.0, 0.12),
    (LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3", 402.0, 535.0, 0.14),
    (LIB / "music/reveal/mus_20260614_reveal_verdict_at_dawn_v2.mp3", 535.0, 657.0, 0.13),
    (LIB / "music/outro/mus_20260614_outro_last_frame_v2.mp3", 657.0, 720.0, 0.13),
]

AMBIENCE = [
    (LIB / "ambience/amb_night_window.mp3", 0.0, 56.9, 0.06),
    (LIB / "ambience/amb_office_hum.mp3", 106.2, 234.0, 0.055),
    (LIB / "ambience/amb_tension_drone.mp3", 234.0, 535.0, 0.05),
    (LIB / "ambience/amb_courtroom_room_tone.mp3", 535.0, 657.0, 0.055),
    (LIB / "ambience/amb_empty_hallway.mp3", 657.0, 720.0, 0.05),
]

SFX = [
    (LIB / "sfx/sfx_ui_tick.mp3", 8.0, 0.45),
    (LIB / "sfx/sfx_sub_drop.mp3", 20.8, 0.45),
    (LIB / "sfx/sfx_low_boom.mp3", 37.6, 0.42),
    (LIB / "sfx/sfx_whoosh_medium.mp3", 106.2, 0.28),
    (LIB / "sfx/sfx_camera_shutter.mp3", 146.0, 0.22),
    (LIB / "sfx/sfx_low_boom.mp3", 214.0, 0.35),
    (LIB / "sfx/sfx_data_blip.mp3", 255.0, 0.45),
    (LIB / "sfx/sfx_soft_impact.mp3", 341.0, 0.48),
    (LIB / "sfx/sfx_riser_2s.mp3", 398.0, 0.25),
    (LIB / "sfx/sfx_sub_drop.mp3", 470.0, 0.42),
    (LIB / "sfx/sfx_gavel_knock.mp3", 565.0, 0.72),
    (LIB / "sfx/sfx_stamp_seal.mp3", 584.0, 0.45),
    (LIB / "sfx/sfx_stamp_seal.mp3", 585.0, 0.43),
    (LIB / "sfx/sfx_stamp_seal.mp3", 586.0, 0.41),
    (LIB / "sfx/sfx_stamp_seal.mp3", 587.0, 0.39),
    (LIB / "sfx/sfx_stamp_seal.mp3", 588.0, 0.37),
    (LIB / "sfx/sfx_stamp_seal.mp3", 589.0, 0.35),
    (LIB / "sfx/sfx_stamp_seal.mp3", 590.0, 0.33),
    (LIB / "sfx/sfx_low_boom.mp3", 620.0, 0.36),
    (LIB / "sfx/sfx_ui_tick.mp3", 686.0, 0.3),
    (LIB / "sfx/sfx_page_turn.mp3", 704.0, 0.28),
]


def check_files(paths: list[Path]) -> None:
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        raise FileNotFoundError("\n".join(missing))


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    final = OUT_DIR / "final_mix_v001.m4a"
    all_inputs: list[tuple[Path, bool]] = [(NARR, False)]
    all_inputs += [(p, True) for p, _, _, _ in MUSIC]
    all_inputs += [(p, True) for p, _, _, _ in AMBIENCE]
    all_inputs += [(p, False) for p, _, _ in SFX]
    check_files([p for p, _ in all_inputs])

    args = [FFMPEG, "-y"]
    for p, loop in all_inputs:
        if loop:
            args += ["-stream_loop", "-1"]
        args += ["-i", str(p)]

    filters = []
    labels = []
    filters.append(f"[0:a]aformat=channel_layouts=stereo,volume=1.0,apad,atrim=0:{TOTAL:.3f},asetpts=PTS-STARTPTS[narr]")
    labels.append("[narr]")
    idx = 1
    for mi, (_p, start, end, vol) in enumerate(MUSIC, start=1):
        dur = end - start
        delay = int(start * 1000)
        fade = min(2.5, dur / 4)
        label = f"mus{mi}"
        filters.append(
            f"[{idx}:a]aformat=channel_layouts=stereo,atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d={fade:.3f},afade=t=out:st={max(0, dur - fade):.3f}:d={fade:.3f},"
            f"volume={vol},adelay={delay}|{delay}[{label}]"
        )
        labels.append(f"[{label}]")
        idx += 1
    for ai, (_p, start, end, vol) in enumerate(AMBIENCE, start=1):
        dur = end - start
        delay = int(start * 1000)
        label = f"amb{ai}"
        filters.append(
            f"[{idx}:a]aformat=channel_layouts=stereo,atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={vol},adelay={delay}|{delay}[{label}]"
        )
        labels.append(f"[{label}]")
        idx += 1
    for si, (_p, start, vol) in enumerate(SFX, start=1):
        delay = int(start * 1000)
        label = f"sfx{si}"
        filters.append(f"[{idx}:a]aformat=channel_layouts=stereo,volume={vol},adelay={delay}|{delay}[{label}]")
        labels.append(f"[{label}]")
        idx += 1
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[mix]")
    args += ["-filter_complex", ";".join(filters), "-map", "[mix]", "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL:.3f}", str(final)]
    subprocess.run(args, check=True)
    print(final)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
