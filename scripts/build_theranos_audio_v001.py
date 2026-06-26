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
HOOK_MONTAGE_SEC = 7.0
BRIDGE_SEC = 1.5
OPENING_SEC = 3.5
CONTENT_START_SEC = HOOK_MONTAGE_SEC + BRIDGE_SEC + OPENING_SEC
ENDCARD_SEC = 9.0

BODY_INPUT = [
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

VOICE_PLACEMENTS: list[dict[str, Any]] = []
cursor = CONTENT_START_SEC
for span_id, chunk_expr, scene_dur in BODY_INPUT:
    local = cursor
    for chunk_id in chunk_expr.split("+"):
        VOICE_PLACEMENTS.append({"span_id": span_id, "chunk_id": chunk_id, "start": round(local, 3)})
        item_seconds = 0.0
        if chunk_id == "VC-0013":
            item_seconds = 9.985
        elif chunk_id == "VC-0014":
            item_seconds = 29.582
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
                "seconds": float(src["seconds"]),
                "end": round(float(item["start"]) + float(src["seconds"]), 3),
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
            f"asetpts=PTS-STARTPTS,aresample=48000,adelay={delay}|{delay}[vc{i}]"
        )
        labels.append(f"[vc{i}]")
    filters.append(
        f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest:dropout_transition=0,"
        f"apad=pad_dur={TOTAL_SEC:.3f},atrim=0:{TOTAL_SEC:.3f}[vo]"
    )
    return filters, "[vo]"


def build_voice_timeline() -> list[dict[str, Any]]:
    placements = resolved_voice_placements()
    VOICE_TIMELINE.parent.mkdir(parents=True, exist_ok=True)
    filters, _ = ffmpeg_voice_filters(placements)
    run(
        [
            FFMPEG,
            "-y",
            "-i",
            NARR_MASTER,
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[vo]",
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
        "[mraw][vo]sidechaincompress=threshold=0.030:ratio=8:attack=18:release=420:makeup=1[mduck]",
        "[araw][vo]sidechaincompress=threshold=0.028:ratio=7:attack=18:release=520:makeup=1[aduck]",
        (
            "[vo][mduck][aduck][sfxraw]amix=inputs=4:normalize=0:duration=longest:dropout_transition=0,"
            f"atrim=0:{TOTAL_SEC:.3f},loudnorm=I=-14:TP=-1:LRA=11:linear=false,"
            f"alimiter=limit=0.78,afade=t=out:st={TOTAL_SEC - 2.0:.3f}:d=2[aout]"
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


def split_caption_lines(tokens: list[str]) -> list[tuple[str, int, int]]:
    lines: list[tuple[str, int, int]] = []
    cur: list[tuple[str, int]] = []
    for i, token in enumerate(tokens):
        trial = " ".join([x for x, _ in cur] + [token]) if cur else token
        if cur and (len(cur) >= 8 or len(trial) > 50):
            lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
            cur = []
        cur.append((token, i))
        if re.search(r"[.?!]$", token) or token.endswith(":") or (token.endswith(",") and len(cur) >= 5):
            lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
            cur = []
    if cur:
        lines.append((" ".join(x for x, _ in cur), cur[0][1], cur[-1][1]))
    return lines


def ts_srt(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_captions(placements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chunks = script_chunks()
    words = transcribe_words(VOICE_TIMELINE)
    entries: list[dict[str, Any]] = []
    for idx, (text, placement) in enumerate(zip(chunks, placements), start=1):
        start = float(placement["start"])
        end = float(placement["end"])
        local_words = [w for w in words if start - 0.18 <= (w["start"] + w["end"]) / 2 <= end + 0.18]
        tokens = text.split()
        token_times: list[tuple[float, float] | None] = [None] * len(tokens)
        j = 0
        for ti, token in enumerate(tokens):
            tn = norm(token)
            if not tn:
                continue
            found = None
            for k in range(j, min(j + 5, len(local_words))):
                wn = str(local_words[k]["norm"])
                if wn == tn or (len(tn) >= 4 and wn.startswith(tn[:4])):
                    found = k
                    break
            if found is None and j < len(local_words):
                found = j
            if found is not None:
                token_times[ti] = (float(local_words[found]["start"]), float(local_words[found]["end"]))
                j = found + 1
        for ti, current in enumerate(token_times):
            if current is None:
                frac = (ti + 0.5) / max(1, len(tokens))
                t = start + frac * (end - start)
                token_times[ti] = (t, min(end, t + 0.35))
        for line, a, b in split_caption_lines(tokens):
            s = token_times[a][0]  # type: ignore[index]
            e = token_times[b][1]  # type: ignore[index]
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
                "method": "master-vo-timeline faster-whisper word timestamps aligned to locked script",
                "timeline_seconds": round(TOTAL_SEC, 3),
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
