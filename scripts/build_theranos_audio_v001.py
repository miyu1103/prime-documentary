#!/usr/bin/env python3
"""Build Theranos final voice timeline, captions, and 4-layer audio mix.

No external paid APIs are called. The final VO is cut from the approved
ElevenLabs master and placed onto the bespoke TheranosPremium timeline.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-015-theranos"
EPDIR = ROOT / "episodes" / EP
SCRIPT = EPDIR / "03_script" / "script.en.v001.md"
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
CAPTIONS = EPDIR / "08_edit" / "captions.v001.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v001.json"
CAPTIONS_TS = ROOT / "remotion" / "src" / "data" / "theranos_captions.ts"
AUDIO_MIX_META = EPDIR / "06_audio" / "audio_mix.v001.json"

MEDIA = Path("H:/pd-media")
LIB = MEDIA / "library"
NARR_MASTER = MEDIA / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
VOICE_TIMELINE = MEDIA / "episodes" / EP / "06_voice" / "master" / "theranos_vo_timeline_v001.wav"
MIX_MASTER = MEDIA / "episodes" / EP / "06_voice" / "master" / "theranos_mix_v001.mp3"
REMOTION_AUDIO = ROOT / "remotion" / "public" / "theranos" / "audio" / "theranos_mix_v001.mp3"

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
FPS = 30
NARRATION_TEMPO = 0.92
HOOK_MONTAGE_SEC = 7.0
BRIDGE_SEC = 1.5
OPENING_SEC = 3.5
CONTENT_START_SEC = HOOK_MONTAGE_SEC + BRIDGE_SEC + OPENING_SEC
ENDCARD_SEC = 9.0


def slow(seconds: float) -> float:
    return seconds / NARRATION_TEMPO


BODY_INPUT = [
    ("SPN-0001", "VC-0001", slow(27.725) + 7.0),
    ("SPN-0002", "VC-0002", slow(36.270) + 10.5),
    ("SPN-0003", "VC-0003", slow(9.381)),
    ("SPN-0004", "VC-0004", slow(25.542)),
    ("SPN-0005", "VC-0005", slow(24.381) + 7.0),
    ("SPN-0023", "VC-0006", slow(19.458)),
    ("SPN-0006", "VC-0007", slow(24.242) + 10.5),
    ("SPN-0007", "VC-0008", slow(9.706)),
    ("SPN-0008", "VC-0009", slow(23.034)),
    ("SPN-0009", "VC-0010", slow(10.449)),
    ("SPN-0010", "VC-0011", slow(24.427) + 6.5),
    ("SPN-0011", "VC-0012", slow(22.756) + 10.5),
    ("SPN-0012", "VC-0013+VC-0014", slow(9.985) + slow(29.582)),
    ("SPN-0024", "VC-0015", slow(26.099)),
    ("SPN-0013", "VC-0016", slow(23.266) + 16.0),
    ("SPN-0014", "VC-0017", slow(16.440)),
    ("SPN-0015", "VC-0018", slow(42.446)),
    ("SPN-0016", "VC-0019", slow(16.300) + 10.5),
    ("SPN-0017", "VC-0020", slow(21.780)),
    ("SPN-0018", "VC-0021", slow(18.437) + 7.0),
    ("SPN-0019", "VC-0022", slow(22.105) + 10.5),
    ("SPN-0020", "VC-0023", slow(33.112) + 6.5),
    ("SPN-0021", "VC-0024", slow(21.037) + 4.5),
    ("SPN-0022", "VC-0025", slow(9.799) + 12.0),
]

BASE_CAPTION_COMMIT = "96e7815"
OLD_BODY_INPUT = [
    ("SPN-0001", "VC-0001", 27.725 + 8.0),
    ("SPN-0002", "VC-0002", 36.270 + 11.5),
    ("SPN-0003", "VC-0003", 9.381),
    ("SPN-0004", "VC-0004", 25.542),
    ("SPN-0005", "VC-0005", 24.381 + 8.0),
    ("SPN-0023", "VC-0006", 19.458),
    ("SPN-0006", "VC-0007", 24.242 + 11.5),
    ("SPN-0007", "VC-0008", 9.706),
    ("SPN-0008", "VC-0009", 23.034),
    ("SPN-0009", "VC-0010", 10.449),
    ("SPN-0010", "VC-0011", 24.427 + 7.0),
    ("SPN-0011", "VC-0012", 22.756 + 11.5),
    ("SPN-0012", "VC-0013+VC-0014", 9.985 + 29.582),
    ("SPN-0024", "VC-0015", 26.099),
    ("SPN-0013", "VC-0016", 23.266 + 20.0),
    ("SPN-0014", "VC-0017", 16.440),
    ("SPN-0015", "VC-0018", 42.446),
    ("SPN-0016", "VC-0019", 16.300 + 11.5),
    ("SPN-0017", "VC-0020", 21.780),
    ("SPN-0018", "VC-0021", 18.437 + 8.0),
    ("SPN-0019", "VC-0022", 22.105 + 11.5),
    ("SPN-0020", "VC-0023", 33.112 + 7.0),
    ("SPN-0021", "VC-0024", 21.037 + 5.0),
    ("SPN-0022", "VC-0025", 9.799 + 16.0),
]


def placement_map(body_input: list[tuple[str, str, float]], *, tempo: float) -> dict[str, dict[str, float]]:
    index = load_index()
    out: dict[str, dict[str, float]] = {}
    cursor = CONTENT_START_SEC
    for span_id, chunk_expr, scene_dur in body_input:
        local = cursor
        for chunk_id in chunk_expr.split("+"):
            seconds = float(index[chunk_id]["seconds"]) / tempo
            out[chunk_id] = {"start": local, "end": local + seconds, "seconds": seconds}
            local += seconds
        cursor += scene_dur
    return out

VOICE_PLACEMENTS: list[dict[str, Any]] = []
cursor = CONTENT_START_SEC
for span_id, chunk_expr, scene_dur in BODY_INPUT:
    local = cursor
    for chunk_id in chunk_expr.split("+"):
        VOICE_PLACEMENTS.append({"span_id": span_id, "chunk_id": chunk_id, "start": round(local, 3)})
        item_seconds = 0.0
        if chunk_id == "VC-0013":
            item_seconds = slow(9.985)
        elif chunk_id == "VC-0014":
            item_seconds = slow(29.582)
        else:
            # Filled from narration_index at runtime.
            item_seconds = -1.0
        local += item_seconds if item_seconds > 0 else 0.0
    cursor += scene_dur

BODY_SEC = sum(item[2] for item in BODY_INPUT)
TOTAL_SEC = CONTENT_START_SEC + BODY_SEC + ENDCARD_SEC


def run(cmd: list[str | Path], label: str) -> None:
    print(f"== {label}", flush=True)
    subprocess.run([str(x) for x in cmd], check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
      for chunk in iter(lambda: f.read(1024 * 1024), b""):
          h.update(chunk)
    return "sha256:" + h.hexdigest()


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


def clean_vo(line: str) -> str:
    text = re.sub(r"\[CLM-[0-9]{4}\]", "", line)
    text = re.sub(r"^\[VO:\]\s*", "", text.strip())
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"\s+([,.;:?!])", r"\1", text)


def script_chunks() -> list[str]:
    chunks = [clean_vo(line) for line in SCRIPT.read_text("utf-8").splitlines() if line.strip().startswith("[VO:]")]
    if len(chunks) != 25:
        raise RuntimeError(f"Expected 25 VO chunks, got {len(chunks)}")
    return chunks


def load_index() -> dict[str, dict[str, Any]]:
    data = json.loads(NARR_INDEX.read_text("utf-8"))
    return {item["chunk_id"]: item for item in data["chunks"]}


def resolved_voice_placements() -> list[dict[str, Any]]:
    index = load_index()
    out: list[dict[str, Any]] = []
    for item in VOICE_PLACEMENTS:
        src = index[item["chunk_id"]]
        out.append(
            {
                **item,
                "source_start": float(src["start"]),
                "source_end": float(src["end"]),
                "seconds": slow(float(src["seconds"])),
                "source_seconds": float(src["seconds"]),
                "tempo": NARRATION_TEMPO,
                "end": round(float(item["start"]) + slow(float(src["seconds"])), 3),
            }
        )
    return out


def ffmpeg_voice_filters(placements: list[dict[str, Any]]) -> tuple[list[str], str]:
    filters: list[str] = []
    labels: list[str] = []
    for i, item in enumerate(placements):
        delay = int(round(float(item["start"]) * 1000))
        filters.append(
            f"[0:a]atrim=start={item['source_start']:.3f}:end={item['source_end']:.3f},"
            f"asetpts=PTS-STARTPTS,atempo={NARRATION_TEMPO:.5f},aresample=48000,adelay={delay}|{delay}[vc{i}]"
        )
        labels.append(f"[vc{i}]")
    filters.append(f"anullsrc=r=48000:cl=stereo:d={TOTAL_SEC:.3f}[narr_silence]")
    filters.append(
        f"[narr_silence]{''.join(labels)}amix=inputs={len(labels) + 1}:normalize=0:duration=first:dropout_transition=0,"
        f"apad=pad_dur={TOTAL_SEC:.3f},atrim=0:{TOTAL_SEC:.3f}[narr_timeline]"
    )
    return filters, "[narr_timeline]"


def build_voice_timeline() -> list[dict[str, Any]]:
    placements = resolved_voice_placements()
    VOICE_TIMELINE.parent.mkdir(parents=True, exist_ok=True)
    filters, voice_label = ffmpeg_voice_filters(placements)
    run(
        [
            FFMPEG,
            "-y",
            "-i",
            NARR_MASTER,
            "-filter_complex",
            ";".join(filters),
            "-map",
            voice_label,
            "-t",
            f"{TOTAL_SEC:.3f}",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            VOICE_TIMELINE,
        ],
        "build master-derived VO timeline with holds",
    )
    return placements


def music_segments() -> list[tuple[float, float, Path, float]]:
    act1 = CONTENT_START_SEC + BODY_INPUT[0][2] + BODY_INPUT[1][2]
    act2 = CONTENT_START_SEC + sum(item[2] for item in BODY_INPUT[:7])
    act3 = CONTENT_START_SEC + sum(item[2] for item in BODY_INPUT[:12])
    verdict = CONTENT_START_SEC + sum(item[2] for item in BODY_INPUT[:14])
    act4 = CONTENT_START_SEC + sum(item[2] for item in BODY_INPUT[:18])
    ending = CONTENT_START_SEC + sum(item[2] for item in BODY_INPUT[:21])
    endcard = CONTENT_START_SEC + BODY_SEC
    return [
        (0.0, 4.0, LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3", 0.20),
        (4.0, HOOK_MONTAGE_SEC + BRIDGE_SEC, LIB / "music" / "hook" / "mus_20260614_hook_glass_air_bed_v1.mp3", 0.20),
        (HOOK_MONTAGE_SEC + BRIDGE_SEC, CONTENT_START_SEC, LIB / "music" / "opening" / "mus_20260614_opening_measured_arpeggio_v1.mp3", 0.16),
        (CONTENT_START_SEC, act1, LIB / "music" / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v1.mp3", 0.12),
        (act1, act2, LIB / "music" / "explainer_bed" / "mus_20260614_explainer_bed_soft_explainer_v1.mp3", 0.11),
        (act2, act3, LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3", 0.12),
        (act3, verdict, LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3", 0.12),
        (verdict, verdict + BODY_INPUT[14][2] + BODY_INPUT[15][2], LIB / "music" / "reveal" / "mus_20260614_reveal_verdict_at_dawn_v1.mp3", 0.14),
        (verdict + BODY_INPUT[14][2] + BODY_INPUT[15][2], act4, LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v1.mp3", 0.105),
        (act4, ending, LIB / "music" / "somber" / "mus_20260614_somber_ledger_of_ash_v1.mp3", 0.105),
        (ending, TOTAL_SEC, LIB / "music" / "outro" / "mus_20260614_outro_last_frame_v1.mp3", 0.14),
    ]


def build_loop_track(
    segments: list[tuple[float, float, Path, float]],
    input_offset: int,
    prefix: str,
) -> tuple[list[str], list[str], str, int]:
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (start, end, path, volume) in enumerate(segments):
        if not path.exists():
            raise FileNotFoundError(path)
        idx = input_offset + i
        dur = end - start
        delay = int(round(start * 1000))
        inputs += ["-stream_loop", "-1", "-i", str(path)]
        filters.append(
            f"[{idx}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={volume},"
            f"afade=t=in:st=0:d={min(1.0, dur / 4):.3f},"
            f"afade=t=out:st={max(dur - 1.2, 0.1):.3f}:d={min(1.2, dur / 4):.3f},"
            f"adelay={delay}|{delay}[{prefix}{i}]"
        )
        labels.append(f"[{prefix}{i}]")
    out_label = f"[{prefix}raw]"
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0{out_label}")
    return inputs, filters, out_label, input_offset + len(segments)


def ambience_segments() -> list[tuple[float, float, Path, float]]:
    return [
        (0.0, 95.5, LIB / "ambience" / "amb_tension_drone.mp3", 0.045),
        (95.5, 218.0, LIB / "ambience" / "amb_office_hum.mp3", 0.035),
        (218.0, 326.9, LIB / "ambience" / "amb_institutional_drone.mp3", 0.037),
        (326.9, 522.5, LIB / "ambience" / "amb_courtroom_room_tone.mp3", 0.035),
        (522.5, 604.4, LIB / "ambience" / "amb_empty_hallway.mp3", 0.037),
        (604.4, TOTAL_SEC, LIB / "ambience" / "amb_night_window.mp3", 0.026),
    ]


def build_sfx(input_offset: int) -> tuple[list[str], list[str], str, int, list[dict[str, Any]]]:
    scene_starts = {}
    c = CONTENT_START_SEC
    for span_id, _, dur in BODY_INPUT:
        scene_starts[span_id] = c
        c += dur
    cues = [
        (0.2, "sfx_riser_2s.mp3", 0.24, "hook riser"),
        (1.8, "sfx_whoosh_short.mp3", 0.18, "hook cut"),
        (3.7, "sfx_whoosh_short.mp3", 0.18, "hook cut"),
        (5.5, "sfx_low_boom.mp3", 0.22, "hook sentence"),
        (scene_starts["SPN-0001"] + 25.0, "sfx_sub_drop.mp3", 0.20, "$9B to $0"),
        (scene_starts["SPN-0005"] + 19.0, "sfx_soft_impact.mp3", 0.16, "$9B rise"),
        (scene_starts["SPN-0010"] + 21.0, "sfx_sub_drop.mp3", 0.18, "SEC collapse"),
        (scene_starts["SPN-0013"] + 3.5, "sfx_gavel_knock.mp3", 0.22, "verdict count 1"),
        (scene_starts["SPN-0013"] + 7.2, "sfx_gavel_knock.mp3", 0.20, "verdict count 2"),
        (scene_starts["SPN-0013"] + 11.0, "sfx_gavel_knock.mp3", 0.20, "verdict count 3"),
        (scene_starts["SPN-0013"] + 15.0, "sfx_gavel_knock.mp3", 0.22, "verdict count 4"),
        (scene_starts["SPN-0013"] + 17.0, "sfx_low_boom.mp3", 0.18, "verdict release"),
        (scene_starts["SPN-0014"] + 3.0, "sfx_ui_tick.mp3", 0.13, "acquitted reveal"),
        (scene_starts["SPN-0014"] + 7.0, "sfx_ui_tick.mp3", 0.13, "no verdict reveal"),
        (scene_starts["SPN-0016"] + 5.0, "sfx_stamp_seal.mp3", 0.18, "sentence seal"),
        (scene_starts["SPN-0018"] + 9.0, "sfx_stamp_seal.mp3", 0.16, "equation seal"),
        (scene_starts["SPN-0022"] + 8.0, "sfx_soft_impact.mp3", 0.17, "subscribe"),
    ]
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    cue_meta: list[dict[str, Any]] = []
    for i, (start, name, volume, note) in enumerate(cues):
        path = LIB / "sfx" / name
        if not path.exists():
            raise FileNotFoundError(path)
        idx = input_offset + i
        delay = int(round(start * 1000))
        inputs += ["-i", str(path)]
        filters.append(f"[{idx}:a]asetpts=PTS-STARTPTS,volume={volume},adelay={delay}|{delay}[sfx{i}]")
        labels.append(f"[sfx{i}]")
        cue_meta.append({"at": round(start, 3), "file": name, "volume": volume, "note": note})
    out_label = "[sfxraw]"
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0{out_label}")
    return inputs, filters, out_label, input_offset + len(cues), cue_meta


def build_final_mix(placements: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    REMOTION_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    MIX_MASTER.parent.mkdir(parents=True, exist_ok=True)
    inputs = ["-i", str(NARR_MASTER)]
    filters, _ = ffmpeg_voice_filters(placements)
    next_input = 1

    music_inputs, music_filters, _, next_input = build_loop_track(music_segments(), next_input, "m")
    inputs += music_inputs
    filters += music_filters

    ambience_inputs, ambience_filters, _, next_input = build_loop_track(ambience_segments(), next_input, "a")
    inputs += ambience_inputs
    filters += ambience_filters

    sfx_inputs, sfx_filters, _, _, sfx_meta = build_sfx(next_input)
    inputs += sfx_inputs
    filters += sfx_filters

    filters += [
        "[narr_timeline]asplit=3[narr_mix][narr_music_sc][narr_amb_sc]",
        "[mraw][narr_music_sc]sidechaincompress=threshold=0.030:ratio=8:attack=18:release=420:makeup=1[mduck]",
        "[araw][narr_amb_sc]sidechaincompress=threshold=0.028:ratio=7:attack=18:release=520:makeup=1[aduck]",
        (
            "[narr_mix][mduck][aduck][sfxraw]amix=inputs=4:normalize=0:duration=longest:dropout_transition=0,"
            f"apad=pad_dur=20,atrim=0:{TOTAL_SEC:.3f},loudnorm=I=-14:TP=-1:LRA=11:linear=false,"
            f"alimiter=limit=0.78,volume=0.84,afade=t=out:st={TOTAL_SEC - 2.0:.3f}:d=2[aout]"
        ),
    ]
    tmp = MIX_MASTER.with_suffix(".tmp.mp3")
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
            tmp,
        ],
        "build VO + BGM + SFX + ambience mix",
    )
    tmp.replace(MIX_MASTER)
    shutil.copy2(MIX_MASTER, REMOTION_AUDIO)
    return loudness_probe(MIX_MASTER), sfx_meta


def loudness_probe(path: Path) -> dict[str, Any]:
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


def norm(word: str) -> str:
    return re.sub(r"[^a-z0-9]", "", word.lower())


def transcribe_words(path: Path) -> list[dict[str, Any]]:
    from faster_whisper import WhisperModel

    print("== forced alignment source: faster-whisper small.en cpu/int8", flush=True)
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(path), word_timestamps=True, vad_filter=False, beam_size=5, language="en")
    words: list[dict[str, Any]] = []
    for seg in segments:
        for word in seg.words or []:
            words.append({"word": word.word.strip(), "norm": norm(word.word), "start": float(word.start), "end": float(word.end)})
    print(f"words={len(words)}", flush=True)
    return words


BAD_BREAK_ENDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "being",
    "but",
    "by",
    "does",
    "every",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "over",
    "that",
    "the",
    "to",
    "was",
    "were",
    "with",
}


def word_cost(script_word: str, heard_word: str) -> float:
    if not script_word or not heard_word:
        return 2.0
    if script_word == heard_word:
        return 0.0
    if script_word in {"nine", "9"} and heard_word in {"9", "nine"}:
        return 0.05
    if script_word in {"dollars", "dollar"} and heard_word in {"billion", "million"}:
        return 0.9
    if min(len(script_word), len(heard_word)) >= 4 and (
        script_word.startswith(heard_word[:4]) or heard_word.startswith(script_word[:4])
    ):
        return 0.2
    ratio = SequenceMatcher(None, script_word, heard_word).ratio()
    if ratio >= 0.72:
        return 1.0 - ratio
    return 1.35


def align_token_times(
    tokens: list[str],
    local_words: list[dict[str, Any]],
    chunk_start: float,
    chunk_end: float,
) -> list[tuple[float, float]]:
    script_norm = [norm(token) for token in tokens]
    heard_norm = [str(word["norm"]) for word in local_words]
    n = len(script_norm)
    m = len(heard_norm)
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    back: list[list[str]] = [[""] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + 0.72
        back[i][0] = "skip_token"
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + 0.58
        back[0][j] = "skip_heard"
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            choices = [
                (dp[i - 1][j - 1] + word_cost(script_norm[i - 1], heard_norm[j - 1]), "match"),
                (dp[i - 1][j] + 0.72, "skip_token"),
                (dp[i][j - 1] + 0.58, "skip_heard"),
            ]
            dp[i][j], back[i][j] = min(choices, key=lambda item: item[0])

    token_times: list[tuple[float, float] | None] = [None] * n
    i, j = n, m
    while i > 0 or j > 0:
        op = back[i][j]
        if op == "match":
            cost = word_cost(script_norm[i - 1], heard_norm[j - 1])
            if cost <= 1.05:
                token_times[i - 1] = (float(local_words[j - 1]["start"]), float(local_words[j - 1]["end"]))
            i -= 1
            j -= 1
        elif op == "skip_token":
            i -= 1
        else:
            j -= 1

    assigned = [idx for idx, value in enumerate(token_times) if value is not None]
    if not assigned:
        span = max(0.1, chunk_end - chunk_start)
        return [
            (chunk_start + span * idx / max(1, n), chunk_start + span * (idx + 1) / max(1, n))
            for idx in range(n)
        ]

    for idx in range(n):
        if token_times[idx] is not None:
            continue
        prev_items = [item for item in assigned if item < idx]
        next_items = [item for item in assigned if item > idx]
        prev_idx = prev_items[-1] if prev_items else None
        next_idx = next_items[0] if next_items else None
        if prev_idx is None and next_idx is None:
            frac = (idx + 0.5) / max(1, n)
            t = chunk_start + frac * (chunk_end - chunk_start)
        elif prev_idx is None:
            next_start = token_times[next_idx][0]  # type: ignore[index]
            t = chunk_start + (next_start - chunk_start) * (idx + 1) / (next_idx + 1)
        elif next_idx is None:
            prev_end = token_times[prev_idx][1]  # type: ignore[index]
            t = prev_end + (chunk_end - prev_end) * (idx - prev_idx) / max(1, n - prev_idx)
        else:
            prev_end = token_times[prev_idx][1]  # type: ignore[index]
            next_start = token_times[next_idx][0]  # type: ignore[index]
            t = prev_end + (next_start - prev_end) * (idx - prev_idx) / (next_idx - prev_idx)
        token_times[idx] = (max(chunk_start, t - 0.08), min(chunk_end, t + 0.22))

    return [(float(item[0]), float(item[1])) for item in token_times if item is not None]


def bad_break(token: str) -> bool:
    return norm(token) in BAD_BREAK_ENDS


def choose_break(tokens: list[str], start: int, end: int) -> int:
    midpoint = (start + end) / 2
    best = start + 1
    best_score = 1_000_000.0
    for idx in range(start + 2, end - 1):
        left = " ".join(tokens[start : idx + 1])
        right = " ".join(tokens[idx + 1 : end + 1])
        score = abs(idx - midpoint) * 4 + abs(len(left) - len(right)) * 0.65
        score += max(0, len(left) - 46) * 8
        score += max(0, len(right) - 46) * 8
        if tokens[idx].endswith(",") or tokens[idx] in {"—", "-", "–"}:
            score -= 28
        if re.search(r"[;:]$", tokens[idx]):
            score -= 18
        if norm(tokens[idx + 1]) in {"and", "but", "because", "while", "when", "where", "so"}:
            score -= 10
        if bad_break(tokens[idx]):
            score += 45
        if score < best_score:
            best = idx
            best_score = score
    return best


def wrap_caption_text(tokens: list[str]) -> str:
    text = " ".join(tokens)
    if len(text) <= 44:
        return text
    split = choose_break(tokens, 0, len(tokens) - 1)
    return " ".join(tokens[: split + 1]) + "\n" + " ".join(tokens[split + 1 :])


def split_caption_groups(tokens: list[str], token_times: list[tuple[float, float]]) -> list[tuple[str, int, int]]:
    sentence_groups: list[tuple[int, int]] = []
    start = 0
    for idx, token in enumerate(tokens):
        if re.search(r"[.?!]$", token) or token.endswith(":"):
            sentence_groups.append((start, idx))
            start = idx + 1
    if start < len(tokens):
        sentence_groups.append((start, len(tokens) - 1))

    groups: list[tuple[int, int]] = []
    pending = sentence_groups[:]
    while pending:
        a, b = pending.pop(0)
        text = " ".join(tokens[a : b + 1])
        dur = token_times[b][1] - token_times[a][0]
        if len(tokens[a : b + 1]) > 16 or len(text) > 90 or dur > 6.2:
            split = choose_break(tokens, a, b)
            pending.insert(0, (split + 1, b))
            pending.insert(0, (a, split))
        else:
            groups.append((a, b))

    out: list[tuple[str, int, int]] = []
    for a, b in groups:
        out.append((wrap_caption_text(tokens[a : b + 1]), a, b))
    return out


def ts_srt(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_caption_files(fixed: list[dict[str, Any]], method: str) -> list[dict[str, Any]]:
    chunks = script_chunks()
    expected = " ".join(chunks).replace("\n", " ")
    actual = " ".join(str(item["text"]).replace("\n", " ") for item in fixed)
    if re.sub(r"\s+", " ", actual).strip() != re.sub(r"\s+", " ", expected).strip():
        raise RuntimeError("Caption text does not exactly match locked script VO text after CLM removal")
    CAPTIONS.parent.mkdir(parents=True, exist_ok=True)
    CAPTIONS.write_text(
        "\n".join(
            f"{i}\n{ts_srt(float(item['start']))} --> {ts_srt(float(item['end']))}\n{item['text']}\n"
            for i, item in enumerate(fixed, start=1)
        ),
        encoding="utf-8",
    )
    CAPTIONS_JSON.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "method": method,
                "timeline_seconds": round(TOTAL_SEC, 3),
                "narration_tempo": NARRATION_TEMPO,
                "cues": fixed,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    cues_for_ts = [{"id": item["id"], "start": item["start"], "end": item["end"], "text": item["text"]} for item in fixed]
    CAPTIONS_TS.write_text(
        "export type TheranosCaption = {id: string; start: number; end: number; text: string};\n"
        f"export const THERANOS_CAPTIONS: TheranosCaption[] = {json.dumps(cues_for_ts, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    print(f"captions={CAPTIONS} cues={len(fixed)}", flush=True)
    return fixed


def load_base_caption_cues() -> list[dict[str, Any]]:
    rel_path = "episodes/PD-2026-015-theranos/08_edit/captions.v001.json"
    result = subprocess.run(
        ["git", "show", f"{BASE_CAPTION_COMMIT}:{rel_path}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode == 0:
        return json.loads(result.stdout)["cues"]
    data = json.loads(CAPTIONS_JSON.read_text(encoding="utf-8"))
    if float(data.get("timeline_seconds", 9999)) > 720:
        raise RuntimeError("Current captions are already slow-timeline captions; cannot use as retiming seed")
    return data["cues"]


def write_stretched_captions() -> list[dict[str, Any]]:
    seed = load_base_caption_cues()
    old_map = placement_map(OLD_BODY_INPUT, tempo=1.0)
    new_map = placement_map(BODY_INPUT, tempo=NARRATION_TEMPO)
    fixed: list[dict[str, Any]] = []
    for i, item in enumerate(seed, start=1):
        chunk_id = item["chunk_id"]
        old = old_map[chunk_id]
        new = new_map[chunk_id]
        start = new["start"] + (float(item["start"]) - old["start"]) / NARRATION_TEMPO
        end = new["start"] + (float(item["end"]) - old["start"]) / NARRATION_TEMPO
        start = max(new["start"], start)
        end = min(new["end"], end)
        if fixed and start < float(fixed[-1]["end"]):
            start = float(fixed[-1]["end"]) + 0.001
        if end <= start:
            end = start + 0.55
        fixed.append({**item, "id": f"CAP-{i:04d}", "start": round(start, 3), "end": round(end, 3)})
    return write_caption_files(
        fixed,
        f"mathematical retime from {BASE_CAPTION_COMMIT} captions; ElevenLabs master stretched with atempo={NARRATION_TEMPO}",
    )


def write_captions(placements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if NARRATION_TEMPO != 1.0:
        return write_stretched_captions()
    chunks = script_chunks()
    words = transcribe_words(VOICE_TIMELINE)
    entries: list[dict[str, Any]] = []
    for idx, (text, placement) in enumerate(zip(chunks, placements), start=1):
        start = float(placement["start"])
        end = float(placement["end"])
        local_words = [w for w in words if start - 0.18 <= (w["start"] + w["end"]) / 2 <= end + 0.18]
        tokens = text.split()
        token_times = align_token_times(tokens, local_words, start, end)
        for line, a, b in split_caption_groups(tokens, token_times):
            s = max(start, token_times[a][0] - 0.04)
            e = min(end, token_times[b][1] + 0.12)
            if e <= s:
                e = min(end, s + 0.65)
            entries.append({"id": f"CAP-{len(entries) + 1:04d}", "start": round(s, 3), "end": round(e, 3), "text": line, "chunk_id": placement["chunk_id"]})
    fixed: list[dict[str, Any]] = []
    for entry in entries:
        if fixed and entry["start"] < fixed[-1]["end"]:
            entry["start"] = round(float(fixed[-1]["end"]) + 0.001, 3)
        if entry["end"] <= entry["start"]:
            entry["end"] = round(float(entry["start"]) + 0.55, 3)
        fixed.append(entry)
    return write_caption_files(fixed, "master-vo-timeline faster-whisper word timestamps aligned to locked script")


def main() -> int:
    if not NARR_MASTER.exists():
        raise FileNotFoundError(NARR_MASTER)
    placements = build_voice_timeline()
    captions = write_captions(placements)
    loudness, sfx = build_final_mix(placements)
    now = datetime.now(timezone.utc).isoformat()
    AUDIO_MIX_META.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "created_at": now,
                "timeline_seconds": round(TOTAL_SEC, 3),
                "voice_source": {
                    "provider": "ElevenLabs",
                    "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
                    "master_sha256": sha256(NARR_MASTER),
                    "method": "ffmpeg atrim from approved master plus timeline holds; no regeneration",
                    "voice_timeline": f"artifact://episodes/{EP}/06_voice/master/{VOICE_TIMELINE.name}",
                    "voice_timeline_sha256": sha256(VOICE_TIMELINE),
                },
                "mix": {
                    "master": f"artifact://episodes/{EP}/06_voice/master/{MIX_MASTER.name}",
                    "master_sha256": sha256(MIX_MASTER),
                    "remotion_static_audio": "theranos/audio/theranos_mix_v001.mp3",
                    "duration_seconds": duration(MIX_MASTER),
                    "loudness_probe": loudness,
                    "layers": ["voice", "bgm", "sfx", "ambience"],
                    "ducking": "FFmpeg sidechaincompress on BGM and ambience keyed by master-derived VO timeline",
                },
                "placements": placements,
                "music_segments": [
                    {"start": round(s, 3), "end": round(e, 3), "file": str(p.relative_to(LIB)).replace("\\", "/"), "volume": v}
                    for s, e, p, v in music_segments()
                ],
                "ambience_segments": [
                    {"start": round(s, 3), "end": round(e, 3), "file": str(p.relative_to(LIB)).replace("\\", "/"), "volume": v}
                    for s, e, p, v in ambience_segments()
                ],
                "sfx_cues": sfx,
                "captions": {
                    "srt": f"artifact://episodes/{EP}/08_edit/captions.v001.srt",
                    "json": f"artifact://episodes/{EP}/08_edit/captions.v001.json",
                    "cue_count": len(captions),
                    "method": "faster-whisper word timestamps on master-derived VO timeline, aligned to locked script text",
                },
                "external_side_effects": {
                    "elevenlabs_generation": False,
                    "paid_api": False,
                    "upload": False,
                    "publish": False,
                },
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"mix={MIX_MASTER} duration={duration(MIX_MASTER):.3f}s loudness={loudness}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
