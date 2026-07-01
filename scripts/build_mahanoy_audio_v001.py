#!/usr/bin/env python3
"""Build Mahanoy final audio mix and captions for MahanoyPremium.

Creates:
- H:/pd-media/.../06_voice/master/vc_master_v001_fit_711s.wav
- episodes/.../08_edit/captions.v001.srt and captions.v001.json
- remotion/src/data/mahanoy_captions.ts
- remotion/public/mahanoy/audio/mahanoy_final_mix_v001.mp3
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-011-mahanoy"
TOTAL_SEC = 720.0
VOICE_TARGET_SEC = 711.0
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EPM = MEDIA / "episodes" / EP
LIB = MEDIA / "library"
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
NARR_MASTER = EPM / "06_voice" / "master" / "vc_master_v001.mp3"
NARR_FIT = EPM / "06_voice" / "master" / "vc_master_v001_fit_711s.wav"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v001.json"
CAPTIONS_TS = ROOT / "remotion" / "src" / "data" / "mahanoy_captions.ts"
PUBLIC_AUDIO = ROOT / "remotion" / "public" / "mahanoy" / "audio" / "mahanoy_final_mix_v001.mp3"
AUDIO_QC = EPDIR / "08_edit" / "audio_mix.v001.qc.json"

MUSIC = [
    (0.0, 31.5, LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3", 0.18),
    (31.5, 115.0, LIB / "music" / "opening" / "mus_20260614_opening_measured_arpeggio_v1.mp3", 0.12),
    (115.0, 275.0, LIB / "music" / "somber" / "mus_20260614_somber_ledger_of_ash_v1.mp3", 0.13),
    (275.0, 455.0, LIB / "music" / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v1.mp3", 0.12),
    (455.0, 575.0, LIB / "music" / "reveal" / "mus_20260614_reveal_verdict_at_dawn_v1.mp3", 0.15),
    (575.0, 711.0, LIB / "music" / "somber" / "mus_20260614_somber_ledger_of_ash_v2.mp3", 0.12),
    (711.0, 720.0, LIB / "music" / "outro" / "mus_20260614_outro_last_frame_v1.mp3", 0.18),
]

AMBIENCE = [
    (0.0, 150.0, LIB / "ambience" / "amb_night_window.mp3", 0.035),
    (150.0, 455.0, LIB / "ambience" / "amb_institutional_drone.mp3", 0.028),
    (455.0, 590.0, LIB / "ambience" / "amb_courtroom_room_tone.mp3", 0.03),
    (590.0, 711.0, LIB / "ambience" / "amb_empty_hallway.mp3", 0.028),
]

SFX = [
    (5.4, LIB / "sfx" / "sfx_whoosh_short.mp3", 0.35),
    (8.3, LIB / "sfx" / "sfx_low_boom.mp3", 0.32),
    (136.0, LIB / "sfx" / "sfx_camera_shutter.mp3", 0.45),
    (328.0, LIB / "sfx" / "sfx_whoosh_short.mp3", 0.34),
    (458.0, LIB / "sfx" / "sfx_gavel_knock.mp3", 0.34),
    (461.0, LIB / "sfx" / "sfx_low_boom.mp3", 0.28),
    (464.0, LIB / "sfx" / "sfx_stamp_seal.mp3", 0.34),
    (548.0, LIB / "sfx" / "sfx_data_blip.mp3", 0.34),
    (591.0, LIB / "sfx" / "sfx_low_boom.mp3", 0.24),
    (691.0, LIB / "sfx" / "sfx_riser_2s.mp3", 0.20),
    (710.5, LIB / "sfx" / "sfx_soft_impact.mp3", 0.28),
]


def run(cmd: list[str], label: str) -> None:
    print(label)
    subprocess.run(cmd, check=True)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def duration(path: Path) -> float:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(result.stdout.strip() or 0)


def fit_voice() -> None:
    src = duration(NARR_MASTER)
    atempo = src / VOICE_TARGET_SEC
    if not 0.5 <= atempo <= 2.0:
        raise RuntimeError(f"atempo out of range: {atempo}")
    NARR_FIT.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(NARR_MASTER),
            "-filter:a",
            f"atempo={atempo:.8f},aresample=48000",
            "-c:a",
            "pcm_s16le",
            str(NARR_FIT),
        ],
        f"fit narration {src:.1f}s -> {VOICE_TARGET_SEC:.1f}s",
    )


def split_caption_text(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if len(trial) > 56 and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    chunks: list[str] = []
    for i in range(0, len(lines), 2):
        chunks.append("\n".join(lines[i : i + 2]))
    return chunks


def fmt_srt(t: float) -> str:
    ms = int(round(t * 1000))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_captions() -> list[dict[str, float | str]]:
    index = json.loads(NARR_INDEX.read_text("utf-8"))
    src_total = float(index["generated_total_seconds"])
    scale = VOICE_TARGET_SEC / src_total
    cues: list[dict[str, float | str]] = []
    for chunk in index["chunks"]:
        text = str(chunk["spoken_text"])
        parts = split_caption_text(text)
        start = float(chunk["start"]) * scale
        end = float(chunk["end"]) * scale
        span = max(1.0, end - start)
        weights = [max(1, len(re.sub(r"\s+", " ", part).split())) for part in parts]
        total_weight = sum(weights)
        cursor = start
        for part, weight in zip(parts, weights):
            dur = span * weight / total_weight
            cue_end = min(end, cursor + dur)
            cues.append({"start": round(cursor, 3), "end": round(cue_end, 3), "text": part})
            cursor = cue_end
    CAPTIONS.parent.mkdir(parents=True, exist_ok=True)
    blocks = []
    for i, cue in enumerate(cues, 1):
        blocks.append(f"{i}\n{fmt_srt(float(cue['start']))} --> {fmt_srt(float(cue['end']))}\n{cue['text']}\n")
    CAPTIONS.write_text("\n".join(blocks), encoding="utf-8")
    CAPTIONS_JSON.write_text(json.dumps({"episode_id": EP, "revision": "v001", "voice": str(NARR_FIT), "cues": cues}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CAPTIONS_TS.write_text(
        "export type MahanoyCaptionCue = {\n  start: number;\n  end: number;\n  text: string;\n};\n\nexport const MAHANOY_CAPTIONS: MahanoyCaptionCue[] = "
        + json.dumps(cues, indent=2, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    print(f"captions={CAPTIONS} cues={len(cues)}")
    return cues


def filter_inputs() -> tuple[list[str], str]:
    inputs = ["-i", str(NARR_FIT)]
    filters: list[str] = [f"[0:a]atrim=0:{TOTAL_SEC:.3f},asetpts=PTS-STARTPTS,volume=1.0[v0]"]
    labels = ["[v0]"]
    input_index = 1
    for start, end, path, vol in MUSIC:
        inputs += ["-stream_loop", "-1", "-i", str(path)]
        dur = end - start
        delay = int(start * 1000)
        filters.append(f"[{input_index}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={vol},adelay={delay}:all=1[m{input_index}]")
        labels.append(f"[m{input_index}]")
        input_index += 1
    for start, end, path, vol in AMBIENCE:
        inputs += ["-stream_loop", "-1", "-i", str(path)]
        dur = end - start
        delay = int(start * 1000)
        filters.append(f"[{input_index}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={vol},adelay={delay}:all=1[a{input_index}]")
        labels.append(f"[a{input_index}]")
        input_index += 1
    for start, path, vol in SFX:
        inputs += ["-i", str(path)]
        delay = int(start * 1000)
        filters.append(f"[{input_index}:a]volume={vol},adelay={delay}:all=1[s{input_index}]")
        labels.append(f"[s{input_index}]")
        input_index += 1
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=longest:normalize=0,atrim=0:{TOTAL_SEC:.3f},loudnorm=I=-14:TP=-1:LRA=11:linear=false[mix]")
    return inputs, ";".join(filters)


def build_mix() -> None:
    PUBLIC_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    inputs, graph = filter_inputs()
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", graph, "-map", "[mix]", "-c:a", "libmp3lame", "-b:a", "192k", str(PUBLIC_AUDIO)]
    run(cmd, "build final audio mix")


def loudnorm_qc() -> dict[str, object]:
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(PUBLIC_AUDIO), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    match = re.search(r"\{[\s\S]*\}", result.stderr)
    loud = json.loads(match.group(0)) if match else {}
    qc = {
        "episode_id": EP,
        "audio_mix": str(PUBLIC_AUDIO),
        "audio_mix_sha256": "sha256:" + sha(PUBLIC_AUDIO),
        "duration_seconds": round(duration(PUBLIC_AUDIO), 3),
        "target_duration_seconds": TOTAL_SEC,
        "target_lufs": -14,
        "target_true_peak_max_db": -1,
        "loudnorm": loud,
        "layers": ["voice", "bgm", "sfx", "ambience"],
        "ducking_note": "Music and ambience are held low under VO; final loudnorm targets -14 LUFS / TP <= -1.",
    }
    AUDIO_QC.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return qc


def main() -> int:
    fit_voice()
    cues = write_captions()
    build_mix()
    qc = loudnorm_qc()
    print(f"mix={PUBLIC_AUDIO} duration={qc['duration_seconds']} cues={len(cues)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
