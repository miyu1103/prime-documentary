#!/usr/bin/env python3
"""Build Kelo final audio mix and captions.

Outputs:
- H:/pd-media/.../06_voice/master/vc_master_v001_fit_631s.wav
- H:/pd-media/.../08_edit/captions.v001.srt
- episodes/.../08_edit/captions.v001.srt
- remotion/src/data/kelo_captions.ts
- remotion/public/kelo/audio/kelo_final_mix_v001.mp3
- episodes/.../06_audio/audio_mix.v001.json
"""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-010-kelo"
EPDIR = ROOT / "episodes" / EP
SCRIPT = EPDIR / "03_script" / "script.en.v001.md"
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v001.json"
CAPTIONS_TS = ROOT / "remotion" / "src" / "data" / "kelo_captions.ts"
REMOTION_AUDIO = ROOT / "remotion" / "public" / "kelo" / "audio" / "kelo_final_mix_v001.mp3"
AUDIO_MIX_META = EPDIR / "06_audio" / "audio_mix.v001.json"
VOICE_TARGET_SEC = 631.0
TOTAL_SEC = 640.5


def media_root() -> Path:
    cfg = json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


MEDIA = media_root()
LIB = MEDIA / "library"
NARR_MASTER = MEDIA / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
NARR_FIT = MEDIA / "episodes" / EP / "06_voice" / "master" / "vc_master_v001_fit_631s.wav"
EP_MEDIA_AUDIO = MEDIA / "episodes" / EP / "07_audio"
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"


def run(cmd: list[str | Path], label: str) -> None:
    print(f"== {label}", flush=True)
    subprocess.run([str(x) for x in cmd], check=True)


def duration(path: Path) -> float:
    result = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        return round(float(result.stdout.strip()), 3)
    except Exception:
        return 0.0


def atempo_filters(value: float) -> str:
    parts: list[float] = []
    remaining = value
    while remaining > 2.0:
        parts.append(2.0)
        remaining /= 2.0
    while remaining < 0.5:
        parts.append(0.5)
        remaining /= 0.5
    parts.append(remaining)
    return ",".join(f"atempo={part:.9f}" for part in parts)


def clean_vo(line: str) -> str:
    text = re.sub(r"\[CLM-[0-9]{4}\]", "", line)
    text = re.sub(r"^\[VO:\]\s*", "", text.strip())
    return re.sub(r"\s+", " ", text).strip()


def parse_vo_chunks() -> list[str]:
    chunks = [clean_vo(line) for line in SCRIPT.read_text("utf-8").splitlines() if line.strip().startswith("[VO:]")]
    if not chunks:
        raise RuntimeError("No [VO:] chunks found")
    return chunks


def ts_srt(t: float) -> str:
    ms = max(0, int(round(t * 1000)))
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_caption_parts(text: str) -> list[str]:
    words = text.split()
    parts: list[str] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join(cur + [word])
        if cur and (len(cur) >= 8 or len(trial) > 48):
            parts.append(" ".join(cur))
            cur = []
        cur.append(word)
        if re.search(r"[.?!]$", word) or (word.endswith(",") and len(cur) >= 5):
            parts.append(" ".join(cur))
            cur = []
    if cur:
        parts.append(" ".join(cur))
    return parts


def fit_narration() -> float:
    src_dur = duration(NARR_MASTER)
    atempo = src_dur / VOICE_TARGET_SEC
    NARR_FIT.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            FFMPEG,
            "-y",
            "-i",
            NARR_MASTER,
            "-filter:a",
            f"aresample=48000,asetpts=PTS-STARTPTS,{atempo_filters(atempo)},alimiter=limit=0.92",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            NARR_FIT,
        ],
        f"fit ElevenLabs narration {src_dur:.1f}s -> {VOICE_TARGET_SEC:.1f}s",
    )
    return duration(NARR_FIT)


def write_captions() -> list[dict[str, float | str]]:
    chunks = parse_vo_chunks()
    index = json.loads(NARR_INDEX.read_text("utf-8"))["chunks"]
    scale = VOICE_TARGET_SEC / float(index[-1]["end"])
    CAPTIONS.parent.mkdir(parents=True, exist_ok=True)
    cues: list[str] = []
    cue_json: list[dict[str, float | str]] = []
    cue_no = 1
    for text, item in zip(chunks, index):
        start = float(item["start"]) * scale
        end = float(item["end"]) * scale
        parts = split_caption_parts(text)
        weights = [max(1, len(part.split())) for part in parts]
        total = sum(weights)
        cursor = start
        for part, weight in zip(parts, weights):
            dur = max(1.05, (end - start) * weight / total)
            part_end = min(end, cursor + dur)
            if part_end <= cursor:
                part_end = min(end, cursor + 0.8)
            cues.append(f"{cue_no}\n{ts_srt(cursor)} --> {ts_srt(part_end)}\n{part}\n")
            cue_json.append({"start": round(cursor, 3), "end": round(part_end, 3), "text": part})
            cue_no += 1
            cursor = part_end
    CAPTIONS.write_text("\n".join(cues), encoding="utf-8")
    CAPTIONS_JSON.write_text(json.dumps({"episode_id": EP, "target_seconds": VOICE_TARGET_SEC, "cues": cue_json}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CAPTIONS_TS.write_text(
        "export type KeloCaptionCue = {\n"
        "  start: number;\n"
        "  end: number;\n"
        "  text: string;\n"
        "};\n\n"
        f"export const KELO_CAPTIONS: KeloCaptionCue[] = {json.dumps(cue_json, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    print(f"captions={CAPTIONS} cues={len(cue_json)}", flush=True)
    return cue_json


def build_music() -> tuple[list[str], list[str], list[str]]:
    segments = [
        (0.0, 24.5, LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v2.mp3", 0.20),
        (24.5, 31.5, LIB / "music" / "opening" / "mus_20260614_opening_measured_arpeggio_v2.mp3", 0.14),
        (31.5, 191.5, LIB / "music" / "somber" / "mus_20260614_somber_ledger_of_ash_v2.mp3", 0.10),
        (191.5, 297.1, LIB / "music" / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v2.mp3", 0.10),
        (297.1, 417.9, LIB / "music" / "reveal" / "mus_20260614_reveal_verdict_at_dawn_v2.mp3", 0.12),
        (417.9, 559.5, LIB / "music" / "somber" / "mus_20260614_somber_ledger_of_ash_v1.mp3", 0.095),
        (559.5, TOTAL_SEC, LIB / "music" / "outro" / "mus_20260614_outro_last_frame_v2.mp3", 0.13),
    ]
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (start, end, path, volume) in enumerate(segments):
        if not path.exists():
            raise FileNotFoundError(path)
        dur = end - start
        delay = int(start * 1000)
        inputs += ["-stream_loop", "-1", "-i", str(path)]
        filters.append(
            f"[{i + 1}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={volume},"
            f"afade=t=in:st=0:d={min(1.2, dur / 3):.3f},"
            f"afade=t=out:st={max(dur - 1.4, 0.1):.3f}:d={min(1.4, dur / 3):.3f},"
            f"adelay={delay}|{delay}[m{i}]"
        )
        labels.append(f"[m{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0[musicraw]")
    return inputs, filters, labels


def build_ambience(input_offset: int) -> tuple[list[str], list[str], list[str]]:
    segments = [
        (0.0, 24.5, LIB / "ambience" / "amb_tension_drone.mp3", 0.045),
        (72.3, 191.5, LIB / "ambience" / "amb_night_window.mp3", 0.038),
        (191.5, 297.1, LIB / "ambience" / "amb_institutional_drone.mp3", 0.036),
        (297.1, 417.9, LIB / "ambience" / "amb_courtroom_room_tone.mp3", 0.034),
        (417.9, 559.5, LIB / "ambience" / "amb_empty_hallway.mp3", 0.037),
        (559.5, 631.5, LIB / "ambience" / "amb_night_window.mp3", 0.026),
    ]
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (start, end, path, volume) in enumerate(segments):
        if not path.exists():
            raise FileNotFoundError(path)
        idx = input_offset + i
        dur = end - start
        delay = int(start * 1000)
        inputs += ["-stream_loop", "-1", "-i", str(path)]
        filters.append(
            f"[{idx}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={volume},"
            f"afade=t=in:st=0:d={min(1.0, dur / 3):.3f},"
            f"afade=t=out:st={max(dur - 1.2, 0.1):.3f}:d={min(1.2, dur / 3):.3f},"
            f"adelay={delay}|{delay}[a{i}]"
        )
        labels.append(f"[a{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0[ambraw]")
    return inputs, filters, labels


def build_sfx(input_offset: int) -> tuple[list[str], list[str], list[str]]:
    cues = [
        (0.3, "sfx_riser_2s.mp3", 0.22),
        (4.8, "sfx_low_boom.mp3", 0.24),
        (7.4, "sfx_whoosh_short.mp3", 0.20),
        (12.5, "sfx_sub_drop.mp3", 0.18),
        (24.5, "sfx_whoosh_medium.mp3", 0.20),
        (72.3, "sfx_page_turn.mp3", 0.16),
        (105.5, "sfx_ui_tick.mp3", 0.14),
        (170.7, "sfx_low_boom.mp3", 0.18),
        (191.5, "sfx_data_blip.mp3", 0.15),
        (240.7, "sfx_ui_tick.mp3", 0.14),
        (297.1, "sfx_gavel_knock.mp3", 0.22),
        (303.4, "sfx_low_boom.mp3", 0.20),
        (309.0, "sfx_stamp_seal.mp3", 0.20),
        (359.1, "sfx_whoosh_short.mp3", 0.18),
        (436.3, "sfx_ui_tick.mp3", 0.15),
        (485.1, "sfx_clock_tick_loop.mp3", 0.05),
        (629.9, "sfx_soft_impact.mp3", 0.18),
    ]
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (start, name, volume) in enumerate(cues):
        path = LIB / "sfx" / name
        if not path.exists():
            raise FileNotFoundError(path)
        idx = input_offset + i
        delay = int(start * 1000)
        inputs += ["-i", str(path)]
        trim = "atrim=0:1.6," if "clock_tick_loop" in name else ""
        filters.append(f"[{idx}:a]{trim}asetpts=PTS-STARTPTS,volume={volume},adelay={delay}|{delay}[s{i}]")
        labels.append(f"[s{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0[sfxraw]")
    return inputs, filters, labels


def build_final_mix() -> None:
    REMOTION_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    EP_MEDIA_AUDIO.mkdir(parents=True, exist_ok=True)
    inputs = ["-i", str(NARR_FIT)]
    filters: list[str] = []

    music_inputs, music_filters, _ = build_music()
    inputs += music_inputs
    filters += music_filters
    next_input = 1 + sum(1 for item in music_inputs if item == "-i")

    ambience_inputs, ambience_filters, _ = build_ambience(next_input)
    inputs += ambience_inputs
    filters += ambience_filters
    next_input += sum(1 for item in ambience_inputs if item == "-i")

    sfx_inputs, sfx_filters, _ = build_sfx(next_input)
    inputs += sfx_inputs
    filters += sfx_filters

    filters += [
        f"[0:a]volume=1.0,apad=pad_dur=12,atrim=0:{TOTAL_SEC:.3f}[vo]",
        "[musicraw][vo]sidechaincompress=threshold=0.030:ratio=8:attack=20:release=420:makeup=1[mduck]",
        "[ambraw][vo]sidechaincompress=threshold=0.028:ratio=6:attack=20:release=520:makeup=1[aduck]",
        (
            "[vo][mduck][aduck][sfxraw]amix=inputs=4:normalize=0:duration=longest:dropout_transition=0,"
            f"atrim=0:{TOTAL_SEC:.3f},loudnorm=I=-14:TP=-1:LRA=11:linear=false,"
            f"alimiter=limit=0.78,volume=0.85,afade=t=out:st={TOTAL_SEC - 2:.3f}:d=2[aout]"
        ),
    ]
    temp = REMOTION_AUDIO.with_suffix(".tmp.mp3")
    run(
        [
            FFMPEG,
            "-y",
            *inputs,
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[aout]",
            "-t",
            f"{TOTAL_SEC:.3f}",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            temp,
        ],
        "VO + BGM + SFX + ambience ducked mix",
    )
    temp.replace(REMOTION_AUDIO)
    shutil.copy2(REMOTION_AUDIO, EP_MEDIA_AUDIO / REMOTION_AUDIO.name)


def loudness_probe(path: Path) -> dict[str, float | str | None]:
    result = subprocess.run(
        [
            FFMPEG,
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-af",
            "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
            "-f",
            "null",
            "NUL",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    text = result.stderr
    match = re.search(r"\{\s*\"input_i\".*?\}", text, re.S)
    if not match:
        return {"raw_tail": text[-1200:]}
    data = json.loads(match.group(0))
    return {
        "input_i": float(data["input_i"]),
        "input_tp": float(data["input_tp"]),
        "input_lra": float(data["input_lra"]),
        "target_offset": float(data["target_offset"]),
    }


def main() -> int:
    fit_seconds = fit_narration()
    cues = write_captions()
    build_final_mix()
    probe = loudness_probe(REMOTION_AUDIO)
    AUDIO_MIX_META.parent.mkdir(parents=True, exist_ok=True)
    AUDIO_MIX_META.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "narration_master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
                "narration_fit": f"artifact://episodes/{EP}/06_voice/master/{NARR_FIT.name}",
                "narration_fit_seconds": fit_seconds,
                "target_voice_seconds": VOICE_TARGET_SEC,
                "timeline_seconds": TOTAL_SEC,
                "mix": f"artifact://episodes/{EP}/07_audio/{REMOTION_AUDIO.name}",
                "remotion_static_audio": "kelo/audio/kelo_final_mix_v001.mp3",
                "layers": ["voice", "bgm", "sfx", "ambience"],
                "ducking": "FFmpeg sidechaincompress on music and ambience keyed by voice",
                "loudness_probe": probe,
                "captions": f"artifact://episodes/{EP}/08_edit/captions.v001.srt",
                "caption_cues": len(cues),
                "caption_timing_note": "Timed from measured ElevenLabs chunk durations and uniformly scaled to the final voice-fit timeline.",
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"mix={REMOTION_AUDIO} duration={duration(REMOTION_AUDIO):.3f}s loudness={probe}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
