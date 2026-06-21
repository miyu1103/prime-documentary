#!/usr/bin/env python3
"""Build Timbs first-finish audio mix and caption data.

This is intentionally local and deterministic:
- places the generated ElevenLabs chunks on the 12-minute rough-cut timeline
- builds VO, music, ambience, SFX and a ducked final mix
- writes sentence captions from approved spoken text using chunk timing
- exports Remotion caption data
"""

from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-009-timbs"
FPS = 30
DURATION = 720.0

EP_DIR = ROOT / "episodes" / EP
VOICE_PLAN = EP_DIR / "06_audio" / "voice_plan.v001.json"
VOICE_INDEX = EP_DIR / "06_audio" / "narration_index.v001.json"
EDIT_DIR = EP_DIR / "08_edit"
REMOTION_DATA = ROOT / "remotion" / "src" / "data"
PUBLIC_TIMBS = ROOT / "remotion" / "public" / "timbs"
MEDIA = Path(r"H:\pd-media")
VOICE_DIR = MEDIA / "episodes" / EP / "06_voice" / "draft"
WORK = MEDIA / "episodes" / EP / "08_edit" / "audio_work"
LIB = MEDIA / "library"


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True)


def ffmpeg(*args: str | Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", *map(str, args)])


def load_shots() -> list[dict]:
    text = (ROOT / "remotion" / "src" / "data" / "timbs_roughcut.ts").read_text("utf-8")
    m = re.search(r'"shots":\s*(\[.*\])\s*\n\}', text, re.S)
    if not m:
        raise RuntimeError("Could not parse TIMBS_ROUGHCUT shots")
    return json.loads(m.group(1))


def srt_ts(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - math.floor(t)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def split_caption_lines(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", text)
    lines: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        words = part.split()
        buf: list[str] = []
        for word in words:
            candidate = " ".join([*buf, word])
            if len(candidate) > 74 and buf:
                lines.append(" ".join(buf))
                buf = [word]
            else:
                buf.append(word)
        if buf:
            lines.append(" ".join(buf))
    return lines


def build_timeline() -> tuple[list[dict], list[dict], list[dict]]:
    plan = json.loads(VOICE_PLAN.read_text("utf-8"))
    index = json.loads(VOICE_INDEX.read_text("utf-8"))
    shots = load_shots()
    if len(plan["chunks"]) != len(index["chunks"]) or len(shots) != len(index["chunks"]):
        raise RuntimeError("Chunk/shot count mismatch")

    shot_starts: list[float] = []
    t = 0.0
    for shot in shots:
        shot_starts.append(t)
        t += float(shot["seconds"])

    timeline: list[dict] = []
    cursor = 0.0
    for i, (chunk, timing, shot_start) in enumerate(zip(plan["chunks"], index["chunks"], shot_starts), 1):
        target = max(float(shot_start), cursor + 0.35 if timeline else 0.0)
        dur = float(timing["seconds"])
        item = {
            "chunk_id": chunk["chunk_id"],
            "file": timing["file"],
            "section": chunk["section"],
            "spoken_text": chunk["spoken_text"],
            "start": round(target, 3),
            "end": round(target + dur, 3),
            "seconds": round(dur, 3),
            "shot_span_id": shots[i - 1]["spanId"],
        }
        timeline.append(item)
        cursor = target + dur

    captions: list[dict] = []
    n = 1
    for item in timeline:
        lines = split_caption_lines(item["spoken_text"])
        total_chars = sum(max(1, len(line)) for line in lines) or 1
        span = item["end"] - item["start"]
        pos = item["start"]
        for line in lines:
            dur = max(1.25, span * max(1, len(line)) / total_chars)
            end = min(item["end"], pos + dur)
            captions.append({"id": f"CAP-{n:04d}", "start": round(pos, 3), "end": round(end, 3), "text": line})
            pos = end
            n += 1

    return timeline, captions, shots


def build_vo(timeline: list[dict]) -> Path:
    out = WORK / "timbs_vo_timeline_v001.wav"
    inputs: list[str] = ["-f", "lavfi", "-t", str(DURATION), "-i", "anullsrc=r=48000:cl=stereo"]
    filters: list[str] = []
    mix_inputs = ["[0:a]"]
    for i, item in enumerate(timeline, 1):
        src = VOICE_DIR / item["file"]
        if not src.exists():
            raise FileNotFoundError(src)
        inputs.extend(["-i", str(src)])
        delay = int(round(item["start"] * 1000))
        filters.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={delay}|{delay}[v{i}]")
        mix_inputs.append(f"[v{i}]")
    filters.append("".join(mix_inputs) + f"amix=inputs={len(mix_inputs)}:duration=first:normalize=0,volume=1.25,alimiter=limit=0.95[a]")
    ffmpeg(*inputs, "-filter_complex", ";".join(filters), "-map", "[a]", "-t", str(DURATION), "-ar", "48000", out)
    return out


def loop_segment(src: Path, dur: float, out: Path, volume: float) -> None:
    ffmpeg("-stream_loop", "-1", "-i", src, "-t", f"{dur:.3f}", "-filter:a", f"volume={volume},aresample=48000,aformat=channel_layouts=stereo", out)


def concat_segments(items: list[tuple[float, Path, float]], out: Path, prefix: str) -> None:
    part_paths = []
    for idx, (dur, src, volume) in enumerate(items, 1):
        part = WORK / f"{prefix}_{idx:02}.wav"
        loop_segment(src, dur, part, volume)
        part_paths.append(part)
    concat = WORK / f"{prefix}_concat.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in part_paths), "utf-8")
    ffmpeg("-f", "concat", "-safe", "0", "-i", concat, "-t", str(DURATION), "-c:a", "pcm_s16le", out)


def build_beds() -> tuple[Path, Path, Path]:
    music_out = WORK / "timbs_music_bed_v001.wav"
    ambience_out = WORK / "timbs_ambience_bed_v001.wav"
    sfx_out = WORK / "timbs_sfx_bed_v001.wav"

    music = LIB / "music"
    concat_segments(
        [
            (30.0, music / "hook" / "mus_20260614_hook_glass_air_bed_v2.mp3", 0.35),
            (45.0, music / "opening" / "mus_20260614_opening_measured_arpeggio_v2.mp3", 0.28),
            (150.0, music / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v2.mp3", 0.24),
            (165.0, music / "reveal" / "mus_20260614_reveal_hidden_system_clicks_v2.mp3", 0.24),
            (165.0, music / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v2.mp3", 0.25),
            (90.0, music / "somber" / "mus_20260614_somber_ledger_of_ash_v2.mp3", 0.24),
            (75.0, music / "outro" / "mus_20260614_outro_last_frame_v2.mp3", 0.26),
        ],
        music_out,
        "music",
    )

    amb = LIB / "ambience"
    concat_segments(
        [
            (30.0, amb / "amb_tension_drone.mp3", 0.16),
            (45.0, amb / "amb_empty_hallway.mp3", 0.13),
            (150.0, amb / "amb_night_window.mp3", 0.13),
            (165.0, amb / "amb_office_hum.mp3", 0.12),
            (165.0, amb / "amb_courtroom_room_tone.mp3", 0.13),
            (90.0, amb / "amb_empty_hallway.mp3", 0.12),
            (75.0, amb / "amb_night_window.mp3", 0.12),
        ],
        ambience_out,
        "ambience",
    )

    sfx = LIB / "sfx"
    cues = [
        (0.0, "sfx_sub_drop.mp3", 0.35),
        (0.8, "sfx_riser_2s.mp3", 0.28),
        (4.5, "sfx_whoosh_short.mp3", 0.20),
        (9.0, "sfx_data_blip.mp3", 0.22),
        (15.0, "sfx_low_boom.mp3", 0.24),
        (20.0, "sfx_soft_impact.mp3", 0.26),
        (30.0, "sfx_whoosh_medium.mp3", 0.18),
        (75.0, "sfx_page_turn.mp3", 0.18),
        (130.0, "sfx_data_blip.mp3", 0.20),
        (197.0, "sfx_stamp_seal.mp3", 0.19),
        (225.0, "sfx_binder_lock.mp3", 0.18),
        (295.0, "sfx_paper_rustle.mp3", 0.16),
        (390.0, "sfx_gavel_knock.mp3", 0.20),
        (465.0, "sfx_clock_tick_loop.mp3", 0.09),
        (555.0, "sfx_soft_impact.mp3", 0.20),
        (630.0, "sfx_dust_swell.mp3", 0.18),
        (645.0, "sfx_page_turn.mp3", 0.16),
        (690.0, "sfx_riser_2s.mp3", 0.16),
        (718.0, "sfx_ui_tick.mp3", 0.15),
    ]
    inputs: list[str] = ["-f", "lavfi", "-t", str(DURATION), "-i", "anullsrc=r=48000:cl=stereo"]
    filters: list[str] = []
    mix_inputs = ["[0:a]"]
    for i, (start, name, volume) in enumerate(cues, 1):
        inputs.extend(["-i", str(sfx / name)])
        delay = int(round(start * 1000))
        filters.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={volume},adelay={delay}|{delay}[s{i}]")
        mix_inputs.append(f"[s{i}]")
    filters.append("".join(mix_inputs) + f"amix=inputs={len(mix_inputs)}:duration=first:normalize=0,alimiter=limit=0.8[a]")
    ffmpeg(*inputs, "-filter_complex", ";".join(filters), "-map", "[a]", "-t", str(DURATION), "-ar", "48000", sfx_out)
    return music_out, ambience_out, sfx_out


def build_final_mix(vo: Path, music: Path, ambience: Path, sfx: Path) -> Path:
    out = PUBLIC_TIMBS / "timbs_final_mix_v001.mp3"
    ffmpeg(
        "-i",
        vo,
        "-i",
        music,
        "-i",
        ambience,
        "-i",
        sfx,
        "-filter_complex",
        "[1:a][2:a]amix=inputs=2:duration=first:normalize=0[bedraw];"
        "[bedraw][0:a]sidechaincompress=threshold=0.025:ratio=8:attack=30:release=450:makeup=1[ducked];"
        "[0:a]volume=1.0[vo];[3:a]volume=1.0[sfx];"
        "[vo][ducked][sfx]amix=inputs=3:duration=first:normalize=0,"
        "alimiter=limit=0.95[a]",
        "-map",
        "[a]",
        "-t",
        str(DURATION),
        "-ar",
        "48000",
        "-b:a",
        "192k",
        out,
    )
    shutil.copy2(out, MEDIA / "episodes" / EP / "08_edit" / "timbs_final_mix_v001.mp3")
    return out


def write_captions(timeline: list[dict], captions: list[dict]) -> None:
    EDIT_DIR.mkdir(parents=True, exist_ok=True)
    srt = EDIT_DIR / "captions.v001.srt"
    srt.write_text(
        "\n\n".join(
            f"{i}\n{srt_ts(c['start'])} --> {srt_ts(c['end'])}\n{c['text']}" for i, c in enumerate(captions, 1)
        )
        + "\n",
        "utf-8",
    )
    (EDIT_DIR / "narration_timeline.v001.json").write_text(json.dumps(timeline, indent=2), "utf-8")
    (EDIT_DIR / "captions.v001.json").write_text(json.dumps(captions, indent=2), "utf-8")

    ts = REMOTION_DATA / "timbs_captions.ts"
    ts.write_text(
        "export type TimbsCaptionCue = {id: string; start: number; end: number; text: string};\n\n"
        "export const TIMBS_CAPTIONS: TimbsCaptionCue[] = "
        + json.dumps(captions, indent=2)
        + ";\n",
        "utf-8",
    )


def main() -> None:
    EDIT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_TIMBS.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    timeline, captions, _shots = build_timeline()
    write_captions(timeline, captions)
    vo = build_vo(timeline)
    music, ambience, sfx = build_beds()
    final = build_final_mix(vo, music, ambience, sfx)
    print(f"captions={len(captions)}")
    print(f"final_mix={final}")


if __name__ == "__main__":
    main()
