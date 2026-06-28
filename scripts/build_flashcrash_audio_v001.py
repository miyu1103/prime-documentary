#!/usr/bin/env python3
"""Build Flash Crash final 4-layer audio mix and retimed captions.

No paid/provider calls. The script reuses the already generated ElevenLabs
chunk files, spaces them across the 28-minute edit, then layers library BGM,
ambience, and SFX with VO ducking.
"""
from __future__ import annotations

import json
import hashlib
import math
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-018-flashcrash"
EPDIR = ROOT / "episodes" / EP
SCRIPT = EPDIR / "03_script" / "script.en.v001.md"
NARRATION_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
CAPTIONS_SRT = EPDIR / "08_edit" / "captions.v001.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v001.json"
CAPTIONS_TS = ROOT / "remotion" / "src" / "data" / "flashcrash_captions.ts"
ALIGNMENT_META = EPDIR / "06_audio" / "caption_alignment.v001.json"
AUDIO_MIX_META = EPDIR / "06_audio" / "audio_mix.v001.json"
REMOTION_AUDIO = ROOT / "remotion" / "public" / "flashcrash" / "audio" / "flashcrash_mix_v001.wav"
TOTAL_SEC = 28 * 60.0
ENDCARD_SEC = 9.0
VOICE_END_TARGET = TOTAL_SEC - ENDCARD_SEC - 4.0
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"


def media_root() -> Path:
    cfg = json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


MEDIA = media_root()
LIB = MEDIA / "library"
VOICE_DRAFT = MEDIA / "episodes" / EP / "06_voice" / "draft"
VOICE_MASTER = MEDIA / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
EP_AUDIO = MEDIA / "episodes" / EP / "06_audio" / "mix"
EP_RENDER_AUDIO = MEDIA / "episodes" / EP / "08_edit" / "audio"


def run(cmd: list[str | Path], label: str) -> subprocess.CompletedProcess[str]:
    print(f"== {label}", flush=True)
    return subprocess.run([str(x) for x in cmd], text=True, check=True)


def capture(cmd: list[str | Path]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(x) for x in cmd], capture_output=True, text=True, check=False)


def duration(path: Path) -> float:
    result = capture([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    try:
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_index() -> dict[str, Any]:
    data = json.loads(NARRATION_INDEX.read_text("utf-8"))
    if "eleven" not in str(data.get("provider", "")).lower():
        raise RuntimeError(f"narration provider is not ElevenLabs: {data.get('provider')}")
    return data


def build_voice_schedule(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    total_voice = sum(float(c["seconds"]) for c in chunks)
    needed_gap = VOICE_END_TARGET - total_voice
    if needed_gap <= 0:
        raise RuntimeError(f"voice target too short: target={VOICE_END_TARGET} voice={total_voice}")
    weights: list[float] = []
    for i, chunk in enumerate(chunks[:-1]):
        w = 1.0
        if i == 0:
            w += 1.4
        if chunk.get("section") != chunks[i + 1].get("section"):
            w += 1.7
        if chunk["chunk_id"] in {"VC-0005", "VC-0013", "VC-0021", "VC-0030", "VC-0038", "VC-0047"}:
            w += 0.9
        if chunk["chunk_id"] in {"VC-0036", "VC-0037", "VC-0038"}:
            w += 1.2
        weights.append(w)
    gap_unit = needed_gap / sum(weights)
    cursor = 0.0
    rows: list[dict[str, Any]] = []
    for i, chunk in enumerate(chunks):
        seconds = float(chunk["seconds"])
        rows.append(
            {
                **chunk,
                "source_start": float(chunk["start"]),
                "source_end": float(chunk["end"]),
                "timeline_start": round(cursor, 3),
                "timeline_end": round(cursor + seconds, 3),
                "timeline_seconds": round(seconds, 3),
            }
        )
        cursor += seconds
        if i < len(weights):
            cursor += weights[i] * gap_unit
    drift = VOICE_END_TARGET - cursor
    if abs(drift) > 0.050:
        rows[-1]["timeline_end"] = round(float(rows[-1]["timeline_end"]) + drift, 3)
    return rows


def input_count(args: list[str]) -> int:
    return sum(1 for item in args if item == "-i")


def build_voice_layer(schedule: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, row in enumerate(schedule):
        path = VOICE_DRAFT / str(row["file"])
        if not path.exists():
            raise FileNotFoundError(path)
        start_ms = int(round(float(row["timeline_start"]) * 1000))
        inputs += ["-i", str(path)]
        filters.append(f"[{i}:a]aresample=48000,volume=1.0,adelay={start_ms}|{start_ms}[v{i}]")
        labels.append(f"[v{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,apad,atrim=0:{TOTAL_SEC:.3f}[vo]")
    return inputs, filters


def music_segments() -> list[tuple[float, float, Path, float]]:
    music = LIB / "music"
    return [
        (0.0, 38.0, music / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v2.mp3", 0.22),
        (38.0, 330.0, music / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v2.mp3", 0.115),
        (330.0, 850.0, music / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3", 0.135),
        (850.0, 1110.0, music / "reveal" / "mus_20260614_reveal_hidden_system_clicks_v2.mp3", 0.13),
        (1110.0, 1245.0, music / "ambience" / "mus_20260614_ambience_paper_trail_static_v2.mp3", 0.09),
        (1245.0, 1515.0, music / "somber" / "mus_20260614_somber_ledger_of_ash_v2.mp3", 0.12),
        (1515.0, TOTAL_SEC, music / "outro" / "mus_20260614_outro_last_frame_v2.mp3", 0.16),
    ]


def ambience_segments() -> list[tuple[float, float, Path, float]]:
    amb = LIB / "ambience"
    return [
        (0.0, 360.0, amb / "amb_tension_drone.mp3", 0.038),
        (360.0, 720.0, amb / "amb_office_hum.mp3", 0.034),
        (720.0, 1085.0, amb / "amb_institutional_drone.mp3", 0.037),
        (1085.0, 1238.0, amb / "amb_tension_drone.mp3", 0.045),
        (1238.0, 1515.0, amb / "amb_empty_hallway.mp3", 0.034),
        (1515.0, TOTAL_SEC, amb / "amb_night_window.mp3", 0.030),
    ]


def build_loop_layer(segments: list[tuple[float, float, Path, float]], first_input: int, prefix: str, duck_label: str) -> tuple[list[str], list[str]]:
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (start, end, path, volume) in enumerate(segments):
        if not path.exists():
            raise FileNotFoundError(path)
        idx = first_input + i
        dur = end - start
        delay = int(round(start * 1000))
        inputs += ["-stream_loop", "-1", "-i", str(path)]
        filters.append(
            f"[{idx}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={volume},"
            f"afade=t=in:st=0:d={min(1.8, dur / 4):.3f},"
            f"afade=t=out:st={max(0.1, dur - 2.0):.3f}:d={min(2.0, dur / 4):.3f},"
            f"adelay={delay}|{delay}[{prefix}{i}]"
        )
        labels.append(f"[{prefix}{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0[{duck_label}]")
    return inputs, filters


def sfx_cues(schedule: list[dict[str, Any]]) -> list[tuple[float, str, float, float]]:
    cues: list[tuple[float, str, float, float]] = [
        (0.4, "sfx_riser_2s.mp3", 0.23, 2.0),
        (4.2, "sfx_sub_drop.mp3", 0.22, 1.4),
        (12.0, "sfx_whoosh_short.mp3", 0.18, 0.9),
        (22.4, "sfx_low_boom.mp3", 0.24, 1.6),
        (29.0, "sfx_whoosh_medium.mp3", 0.18, 1.2),
    ]
    for row in schedule:
        start = float(row["timeline_start"])
        cid = row["chunk_id"]
        if cid in {"VC-0005", "VC-0010", "VC-0016", "VC-0023", "VC-0030", "VC-0036", "VC-0042", "VC-0048"}:
            cues.append((max(0.0, start - 0.2), "sfx_whoosh_short.mp3", 0.14, 0.8))
        if cid in {"VC-0036", "VC-0037", "VC-0038"}:
            cues.append((start + 1.0, "sfx_sub_drop.mp3", 0.21, 1.4))
            cues.append((start + 4.0, "sfx_low_boom.mp3", 0.22, 1.6))
        if cid in {"VC-0018", "VC-0027", "VC-0044"}:
            cues.append((start + 0.8, "sfx_data_blip.mp3", 0.12, 0.8))
        if row.get("section") == "ENDING" and cid == "VC-0048":
            cues.append((start + 3.0, "sfx_soft_impact.mp3", 0.16, 1.0))
    return sorted(cues, key=lambda item: item[0])


def build_sfx_layer(schedule: list[dict[str, Any]], first_input: int) -> tuple[list[str], list[str]]:
    cues = sfx_cues(schedule)
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (start, name, volume, trim) in enumerate(cues):
        path = LIB / "sfx" / name
        if not path.exists():
            raise FileNotFoundError(path)
        idx = first_input + i
        delay = int(round(start * 1000))
        inputs += ["-i", str(path)]
        filters.append(f"[{idx}:a]atrim=0:{trim:.3f},asetpts=PTS-STARTPTS,volume={volume},adelay={delay}|{delay}[s{i}]")
        labels.append(f"[s{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0[sfxraw]")
    return inputs, filters


def clean_vo(line: str) -> str:
    text = re.sub(r"^\[VO:\]\s*", "", line.strip())
    text = re.sub(r"\s*(?:\[CLM-[0-9]{4}\]\s*)+", ". ", text)
    text = re.sub(r"\.{2,}", ".", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_vo_texts() -> list[str]:
    texts = [clean_vo(line) for line in SCRIPT.read_text("utf-8").splitlines() if line.strip().startswith("[VO:]")]
    if len(texts) != 51:
        raise RuntimeError(f"expected 51 [VO:] chunks, got {len(texts)}")
    return texts


def wrap_two_lines(words: list[str]) -> str:
    text = " ".join(words)
    if len(text) <= 42:
        return text
    best = None
    for i in range(1, len(words)):
        left = " ".join(words[:i])
        right = " ".join(words[i:])
        if len(left) > 42 or len(right) > 42:
            continue
        score = abs(len(left) - len(right))
        if best is None or score < best[0]:
            best = (score, i)
    if best is None:
        return text
    return " ".join(words[: best[1]]) + "\n" + " ".join(words[best[1] :])


def split_caption_parts(text: str) -> list[str]:
    words = text.split()
    parts: list[list[str]] = []
    cur: list[str] = []
    weak = {"and", "or", "of", "the", "a", "an", "to", "in", "with", "for", "as", "that"}
    for word in words:
        trial = cur + [word]
        trial_text = " ".join(trial)
        boundary = bool(re.search(r"[.?!]$", word)) or (bool(re.search(r"[,;:]$", word)) and len(trial) >= 5)
        if cur and (len(trial) > 9 or len(trial_text) > 76):
            if cur[-1].lower().strip(".,;:?!") in weak and len(cur) > 1:
                carry = cur.pop()
                parts.append(cur)
                cur = [carry]
            else:
                parts.append(cur)
                cur = []
        cur.append(word)
        if boundary and len(cur) >= 3:
            parts.append(cur)
            cur = []
    if cur:
        parts.append(cur)
    flat: list[str] = []
    for part in parts:
        if len(" ".join(part)) <= 84:
            flat.append(wrap_two_lines(part))
            continue
        for i in range(0, len(part), 6):
            flat.append(wrap_two_lines(part[i : i + 6]))
    return flat


def srt_ts(t: float) -> str:
    ms = max(0, int(round(t * 1000)))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_retimed_captions(schedule: list[dict[str, Any]]) -> list[dict[str, Any]]:
    texts = load_vo_texts()
    if len(texts) != len(schedule):
        raise RuntimeError(f"VO/script mismatch: {len(texts)} text chunks / {len(schedule)} audio chunks")
    cues: list[dict[str, Any]] = []
    for text, row in zip(texts, schedule):
        parts = split_caption_parts(text)
        if not parts:
            continue
        start = float(row["timeline_start"])
        end = float(row["timeline_end"])
        dur = end - start
        weights = [max(1, len(part.replace("\n", " ").split())) for part in parts]
        total_weight = sum(weights)
        cursor = start
        acc = 0
        for i, (part, weight) in enumerate(zip(parts, weights)):
            acc += weight
            part_end = end if i == len(parts) - 1 else start + dur * acc / total_weight
            if part_end - cursor > 6.6 and len(part.replace("\n", " ").split()) > 6:
                words = part.replace("\n", " ").split()
                mid = max(3, min(len(words) - 3, len(words) // 2))
                split_at = start + dur * (acc - weight / 2) / total_weight
                cues.append({"start": round(cursor, 3), "end": round(split_at, 3), "text": wrap_two_lines(words[:mid])})
                cues.append({"start": round(split_at + 0.035, 3), "end": round(part_end, 3), "text": wrap_two_lines(words[mid:])})
            else:
                cues.append({"start": round(cursor, 3), "end": round(part_end, 3), "text": part})
            cursor = part_end + 0.035
    for i, cue in enumerate(cues):
        cue["text"] = re.sub(r"\.{2,}", ".", str(cue["text"]))
        start = float(cue["start"])
        end = float(cue["end"])
        if end - start >= 0.72:
            continue
        next_start = float(cues[i + 1]["start"]) if i + 1 < len(cues) else TOTAL_SEC
        cue["end"] = round(min(start + 0.72, max(start + 0.72, next_start - 0.035)), 3)
    blocks = []
    for i, cue in enumerate(cues, start=1):
        blocks.append(f"{i}\n{srt_ts(float(cue['start']))} --> {srt_ts(float(cue['end']))}\n{cue['text']}\n")
    CAPTIONS_SRT.write_text("\n".join(blocks), encoding="utf-8")
    CAPTIONS_JSON.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "method": "retimed_existing_final_captions_to_flashcrash_chunk_schedule",
                "cues": cues,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    CAPTIONS_TS.write_text(
        "export type FlashCrashCaptionCue = {\n"
        "  start: number;\n"
        "  end: number;\n"
        "  text: string;\n"
        "};\n\n"
        f"export const FLASHCRASH_CAPTIONS: FlashCrashCaptionCue[] = {json.dumps(cues, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    return cues


def build_final_mix(schedule: list[dict[str, Any]]) -> None:
    REMOTION_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    voice_inputs, filters = build_voice_layer(schedule)
    inputs = voice_inputs

    music_inputs, music_filters = build_loop_layer(music_segments(), input_count(inputs), "m", "musicraw")
    inputs += music_inputs
    filters += music_filters

    ambience_inputs, ambience_filters = build_loop_layer(ambience_segments(), input_count(inputs), "a", "ambraw")
    inputs += ambience_inputs
    filters += ambience_filters

    sfx_inputs, sfx_filters = build_sfx_layer(schedule, input_count(inputs))
    inputs += sfx_inputs
    filters += sfx_filters

    filters += [
        "[musicraw][vo]sidechaincompress=threshold=0.028:ratio=8:attack=18:release=420:makeup=1[mduck]",
        "[ambraw][vo]sidechaincompress=threshold=0.026:ratio=6:attack=22:release=520:makeup=1[aduck]",
        (
            "[vo][mduck][aduck][sfxraw]amix=inputs=4:normalize=0:duration=longest:dropout_transition=0,"
            f"atrim=0:{TOTAL_SEC:.3f},loudnorm=I=-14:TP=-1:LRA=11:linear=false,"
            f"alimiter=limit=0.88,afade=t=out:st={TOTAL_SEC - 2.2:.3f}:d=2.2[aout]"
        ),
    ]
    temp = REMOTION_AUDIO.with_suffix(".tmp.wav")
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
            "pcm_s16le",
            temp,
        ],
        "FlashCrash VO + BGM + SFX + ambience mix",
    )
    temp.replace(REMOTION_AUDIO)
    EP_AUDIO.mkdir(parents=True, exist_ok=True)
    EP_RENDER_AUDIO.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REMOTION_AUDIO, EP_AUDIO / REMOTION_AUDIO.name)
    shutil.copy2(REMOTION_AUDIO, EP_RENDER_AUDIO / REMOTION_AUDIO.name)


def loudness_probe(path: Path) -> dict[str, float | str]:
    result = capture(
        [
            FFMPEG,
            "-hide_banner",
            "-nostats",
            "-i",
            path,
            "-af",
            "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
            "-f",
            "null",
            "NUL",
        ]
    )
    match = re.search(r"\{\s*\"input_i\".*?\}", result.stderr, re.S)
    if not match:
        return {"raw_tail": result.stderr[-1200:]}
    data = json.loads(match.group(0))
    return {
        "input_i": float(data["input_i"]),
        "input_tp": float(data["input_tp"]),
        "input_lra": float(data["input_lra"]),
        "target_offset": float(data["target_offset"]),
    }


def write_metadata(index: dict[str, Any], schedule: list[dict[str, Any]], cues: list[dict[str, Any]]) -> None:
    mix_sha = sha256_file(REMOTION_AUDIO)
    ALIGNMENT_META.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "method": "existing final captions retimed to final 28-minute VO chunk schedule",
                "script_locked": True,
                "voice_retained": True,
                "caption_cues": len(cues),
                "last_caption_end": cues[-1]["end"],
                "schedule": [
                    {
                        "chunk_id": row["chunk_id"],
                        "source_start": row["source_start"],
                        "source_end": row["source_end"],
                        "timeline_start": row["timeline_start"],
                        "timeline_end": row["timeline_end"],
                    }
                    for row in schedule
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    AUDIO_MIX_META.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "provider": index.get("provider"),
                "voice_id": index.get("voice_id"),
                "narration_master": index.get("master"),
                "narration_reuse_note": "Reused already-generated ElevenLabs chunks; no provider/API call was made.",
                "timeline_seconds": TOTAL_SEC,
                "voice_end_target": VOICE_END_TARGET,
                "voice_last_chunk_end": schedule[-1]["timeline_end"],
                "layers": ["voice", "bgm", "sfx", "ambience"],
                "ducking": "FFmpeg sidechaincompress on music and ambience keyed by VO",
                "remotion_static_audio": "flashcrash/audio/flashcrash_mix_v001.wav",
                "media_mix": f"artifact://episodes/{EP}/06_audio/mix/{REMOTION_AUDIO.name}",
                "render_audio_copy": f"artifact://episodes/{EP}/08_edit/audio/{REMOTION_AUDIO.name}",
                "sha256": mix_sha,
                "loudness_probe": loudness_probe(REMOTION_AUDIO),
                "music_segments": [str(row[2].relative_to(LIB)).replace("\\", "/") for row in music_segments()],
                "ambience_segments": [str(row[2].relative_to(LIB)).replace("\\", "/") for row in ambience_segments()],
                "sfx_cues": len(sfx_cues(schedule)),
                "caption_cues": len(cues),
                "caption_last_end": cues[-1]["end"],
                "external_cost_usd": 0,
                "external_calls": [],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    index = load_index()
    if not VOICE_MASTER.exists():
        raise FileNotFoundError(VOICE_MASTER)
    schedule = build_voice_schedule(index["chunks"])
    cues = write_retimed_captions(schedule)
    build_final_mix(schedule)
    write_metadata(index, schedule, cues)
    print(
        json.dumps(
            {
                "mix": str(REMOTION_AUDIO),
                "duration": round(duration(REMOTION_AUDIO), 3),
                "last_caption_end": cues[-1]["end"],
                "voice_last_chunk_end": schedule[-1]["timeline_end"],
                "loudness": loudness_probe(REMOTION_AUDIO),
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
