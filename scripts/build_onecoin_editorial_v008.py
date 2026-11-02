#!/usr/bin/env python3
"""Build OneCoin v008 editorial timeline, natural-speed audio, and captions.

This is a viewing-quality cut, not a 30-minute contract stretch. It reuses the
approved ElevenLabs contract-voice chunks from voice_master v002 and performs no
external API calls.
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

import build_onecoin_audio_v001 as audio_base


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
REMOTION = ROOT / "remotion"
ROUGH_TS = REMOTION / "src" / "data" / "onecoin_roughcut.ts"
CAPTIONS_TS = REMOTION / "src" / "data" / "onecoin_captions.ts"
REMOTION_AUDIO = REMOTION / "public" / "onecoin" / "audio" / "onecoin_final_mix_v008.wav"
MEDIA = Path("E:/pd-media")
WORK = MEDIA / "episodes" / EP / "06_audio" / "editorial_v008"
FIT_DIR = WORK / "fit_wav"
VOICE_INDEX = EPDIR / "06_audio" / "narration_index.v003.json"
CAPTIONS_SRT = EPDIR / "08_edit" / "captions.v005.editorial_v008.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v005.editorial_v008.json"
AUDIO_QC = EPDIR / "08_edit" / "audio_mix.v005.editorial_v008.qc.json"
PLAN = EPDIR / "08_edit" / "onecoin_editorial_plan.v008.json"
EVENTS = EPDIR / "events" / "events.jsonl"
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

HOOK_SPAN = "SPN-0003"
HOOK_SECONDS = 8.0
ENDCARD_SECONDS = 7.0
SILENCE_SPAN_ID = "SPN-0043"
START_AFTER_HOOK = "SPN-0006"
PROMISE_BRIGHT_POOL = [
    "onecoin/hero/T-IMG-006.png",
    "onecoin/hero/T-IMG-010.png",
    "onecoin/hero/T-IMG-015.png",
    "onecoin/hero/T-IMG-AUX2.png",
    "onecoin/hero/T-IMG-011.png",
    "onecoin/hero/T-IMG-016.png",
    "onecoin/hero/T-IMG-012.png",
    "onecoin/hero/T-IMG-004.png",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def capture(cmd: list[str | Path]) -> str:
    p = subprocess.run([str(x) for x in cmd], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    return p.stdout


def duration(path: Path) -> float:
    return float(capture([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())


def parse_roughcut() -> dict[str, Any]:
    text = ROUGH_TS.read_text(encoding="utf-8")
    match = re.search(r"export const ONECOIN_ROUGHCUT: RoughCutData = (\{.*\});", text, re.S)
    if not match:
        raise RuntimeError("Could not parse onecoin_roughcut.ts")
    return json.loads(match.group(1))


def load_voice_index() -> dict[str, Any]:
    data = json.loads(VOICE_INDEX.read_text(encoding="utf-8"))
    if data.get("voice_id") != "nPczCjzI2devNBz1zQrb":
        raise RuntimeError(f"Unexpected voice id: {data.get('voice_id')}")
    return data


def hero_pool(base: dict[str, Any]) -> list[str]:
    seen: list[str] = []
    for shot in base["shots"]:
        for src in shot.get("images") or []:
            if src and src not in seen:
                seen.append(src)
        if shot.get("src") and shot["src"] not in seen:
            seen.append(shot["src"])
    return seen


def richer_images(pool: list[str], offset: int, seconds: float) -> list[str]:
    if not pool:
        return []
    count = max(5, min(14, int(seconds / 1.55) + 3))
    return [pool[(offset + i) % len(pool)] for i in range(count)]


def pool_for_chapter(chapter_id: str, fallback: list[str]) -> list[str]:
    if chapter_id == "the_promise":
        return [src for src in PROMISE_BRIGHT_POOL if src in fallback] or fallback
    return fallback


def build_rows(base: dict[str, Any], voice: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_span = {shot["spanId"]: shot for shot in base["shots"]}
    chunks = {chunk["span_id"]: chunk for chunk in voice["chunks"]}
    pool = hero_pool(base)
    rows: list[dict[str, Any]] = []
    plan_rows: list[dict[str, Any]] = []

    hook_base = dict(by_span[HOOK_SPAN])
    hook_base["chapterId"] = "cold_open"
    hook_base["seconds"] = HOOK_SECONDS
    hook_base["images"] = richer_images(pool, 2, HOOK_SECONDS)
    rows.append(hook_base)
    plan_rows.append({"span_id": HOOK_SPAN, "role": "trimmed_hook", "raw_start": 0.0, "raw_seconds": HOOK_SECONDS, "shot_seconds": HOOK_SECONDS})

    started = False
    visual_offset = 6
    for shot in base["shots"]:
        sid = shot["spanId"]
        if sid == START_AFTER_HOOK:
            started = True
        if not started:
            continue
        row = dict(shot)
        if sid == SILENCE_SPAN_ID:
            seconds = 3.0
        else:
            raw = float(chunks[sid]["raw_seconds"])
            seconds = max(raw + 0.18, 1.8)
        row["seconds"] = round(seconds, 3)
        if row.get("assetType") == "ai_image":
            chapter_pool = pool_for_chapter(str(row.get("chapterId", "")), pool)
            row["images"] = richer_images(chapter_pool, visual_offset, seconds)
            row["src"] = row["images"][0]
            visual_offset += 3
        rows.append(row)
        plan_rows.append({"span_id": sid, "role": "natural_speed_full", "raw_seconds": float(chunks.get(sid, {}).get("raw_seconds", 0.0)), "shot_seconds": round(seconds, 3)})
    return rows, plan_rows


def run_ffmpeg(cmd: list[str | Path]) -> None:
    subprocess.run([str(x) for x in cmd], check=True)


def build_voice_segments(rows: list[dict[str, Any]], voice: dict[str, Any]) -> tuple[list[dict[str, Any]], float]:
    chunks = {chunk["span_id"]: chunk for chunk in voice["chunks"]}
    FIT_DIR.mkdir(parents=True, exist_ok=True)
    concat_lines: list[str] = []
    timed: list[dict[str, Any]] = []
    cursor = 0.0
    for row in rows:
        sid = row["spanId"]
        seconds = float(row["seconds"])
        out = FIT_DIR / f"{sid}.wav"
        if sid == HOOK_SPAN and cursor == 0:
            raw = Path(chunks[sid]["raw_file"])
            run_ffmpeg([FFMPEG, "-y", "-i", raw, "-filter:a", f"atrim=0:{HOOK_SECONDS:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={HOOK_SECONDS - 0.45:.3f}:d=0.45,aresample=48000,apad,atrim=0:{seconds:.3f}", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", out])
            text = "Here is what you need to know before we start. The coin she is selling does not exist."
            timed.append({**row, "shot_start": cursor, "shot_end": cursor + seconds, "voice_start": cursor, "voice_end": cursor + seconds, "text": text, "speak": True, "raw_seconds": HOOK_SECONDS, "file": out.name})
        elif sid == SILENCE_SPAN_ID:
            run_ffmpeg([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{seconds:.3f}", "-c:a", "pcm_s16le", out])
            timed.append({**row, "shot_start": cursor, "shot_end": cursor + seconds, "voice_start": cursor, "voice_end": cursor, "text": "", "speak": False, "raw_seconds": 0.0, "file": out.name})
        else:
            chunk = chunks[sid]
            raw = Path(chunk["raw_file"])
            raw_sec = float(chunk["raw_seconds"])
            run_ffmpeg([FFMPEG, "-y", "-i", raw, "-filter:a", f"aresample=48000,apad,atrim=0:{seconds:.3f},alimiter=limit=0.92", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", out])
            timed.append({**row, "shot_start": cursor, "shot_end": cursor + seconds, "voice_start": cursor, "voice_end": cursor + raw_sec, "text": chunk["text"], "speak": True, "raw_seconds": raw_sec, "file": out.name})
        concat_lines.append(f"file '{out.as_posix()}'\n")
        cursor += seconds
    tail = FIT_DIR / "_endcard_tail.wav"
    run_ffmpeg([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{ENDCARD_SECONDS:.3f}", "-c:a", "pcm_s16le", tail])
    concat_lines.append(f"file '{tail.as_posix()}'\n")
    total = cursor + ENDCARD_SECONDS
    concat = FIT_DIR / "_concat_editorial.txt"
    concat.write_text("".join(concat_lines), encoding="utf-8")
    narration = WORK / "narration_editorial_v008.wav"
    run_ffmpeg([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c:a", "pcm_s16le", narration])
    return timed, total


def split_caption_parts(text: str) -> list[str]:
    words = text.split()
    parts: list[str] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join(cur + [word])
        if cur and (len(trial) > 40 or len(cur) >= 6 or re.search(r"[.?!]$", cur[-1])):
            parts.append(audio_base.break_caption_lines(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        parts.append(audio_base.break_caption_lines(cur))
    return parts


def write_captions(timed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cues: list[dict[str, Any]] = []
    index = 1
    for row in timed:
        if not row.get("speak"):
            continue
        parts = split_caption_parts(row["text"])
        weights = [max(1, len(part.replace("\n", " ").split())) for part in parts]
        total_weight = sum(weights)
        start = float(row["voice_start"])
        end = float(row["voice_end"])
        cursor = start
        elapsed = 0
        for part, weight in zip(parts, weights):
            elapsed += weight
            part_end = start + (end - start) * elapsed / total_weight
            part_end = min(part_end, cursor + 3.0)
            if part_end <= cursor:
                part_end = cursor + 0.3
            cues.append({"index": index, "start": round(cursor, 3), "end": round(part_end, 3), "text": part})
            index += 1
            cursor = part_end
    CAPTIONS_SRT.write_text("\n".join(f"{cue['index']}\n{audio_base.srt_ts(cue['start'])} --> {audio_base.srt_ts(cue['end'])}\n{cue['text']}\n" for cue in cues), encoding="utf-8")
    CAPTIONS_JSON.write_text(json.dumps({"episode_id": EP, "revision": "v008", "alignment_method": "natural_voice_word_weighted_editorial", "cues": cues}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CAPTIONS_TS.write_text(
        "// Editorial v008 captions from natural-speed ElevenLabs master chunks.\n"
        "import type {CaptionCue} from '../compositions/RoughCut';\n\n"
        "export const ONECOIN_CAPTIONS: CaptionCue[] = "
        + json.dumps([{"id": f"onecoin-caption-v008-{i + 1:04d}", "start": cue["start"], "end": cue["end"], "text": cue["text"]} for i, cue in enumerate(cues)], indent=2, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    return cues


def chapter_bounds(timed: list[dict[str, Any]]) -> dict[str, tuple[float, float]]:
    bounds: dict[str, list[float]] = {}
    for row in timed:
        chap = row["chapterId"]
        bounds.setdefault(chap, [float(row["shot_start"]), float(row["shot_end"])])
        bounds[chap][1] = float(row["shot_end"])
    return {k: (v[0], v[1]) for k, v in bounds.items()}


def build_layer_inputs(segments: list[tuple[float, float, Path, float]], start_index: int, prefix: str) -> tuple[list[str], list[str], list[str], int]:
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    idx = start_index
    for i, (start, end, path, volume) in enumerate(segments):
        dur = max(0.1, end - start)
        delay = int(round(start * 1000))
        inputs += ["-stream_loop", "-1", "-i", str(path)]
        label = f"{prefix}{i}"
        filters.append(
            f"[{idx}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={volume},"
            f"afade=t=in:st=0:d={min(1.2, dur / 3):.3f},"
            f"afade=t=out:st={max(dur - 1.4, 0.1):.3f}:d={min(1.4, dur / 3):.3f},"
            f"adelay={delay}|{delay}[{label}]"
        )
        labels.append(f"[{label}]")
        idx += 1
    return inputs, filters, labels, idx


def build_mix(timed: list[dict[str, Any]], total_sec: float) -> None:
    narration = WORK / "narration_editorial_v008.wav"
    bounds = chapter_bounds(timed)
    lib = audio_base.LIB
    inputs = ["-i", str(narration)]
    filters: list[str] = []
    music_segments = [
        (0.0, bounds["cold_open"][1], lib / "music" / "hook" / "mus_20260614_hook_glass_air_bed_v2.mp3", 0.10),
        (*bounds["the_promise"], lib / "music" / "opening" / "mus_20260614_opening_measured_arpeggio_v2.mp3", 0.085),
        (*bounds["the_crack"], lib / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v2.mp3", 0.08),
        (*bounds["the_void"], lib / "music" / "ambience" / "mus_20260614_ambience_paper_trail_static_v2.mp3", 0.074),
        (*bounds["coda"], lib / "music" / "outro" / "mus_20260614_outro_last_frame_v2.mp3", 0.07),
    ]
    m_inputs, m_filters, m_labels, next_idx = build_layer_inputs(music_segments, 1, "m")
    inputs += m_inputs
    filters += m_filters
    ambience_segments = [
        (0.0, total_sec, lib / "ambience" / "amb_tension_drone.mp3", 0.018),
        (bounds["the_crack"][0], bounds["the_void"][1], lib / "ambience" / "amb_institutional_drone.mp3", 0.023),
        (bounds["coda"][0], total_sec, lib / "ambience" / "amb_night_window.mp3", 0.020),
    ]
    a_inputs, a_filters, a_labels, _ = build_layer_inputs(ambience_segments, next_idx, "a")
    inputs += a_inputs
    filters += a_filters
    silence = next((row for row in timed if row["spanId"] == SILENCE_SPAN_ID), None)
    silence_filter = ""
    if silence:
        silence_filter = f"volume=0:enable='between(t,{float(silence['shot_start']):.3f},{float(silence['shot_end']):.3f})',"
    filters += [
        f"{''.join(m_labels)}amix=inputs={len(m_labels)}:normalize=0:dropout_transition=0[musicraw]",
        f"{''.join(a_labels)}amix=inputs={len(a_labels)}:normalize=0:dropout_transition=0[ambraw]",
        "[musicraw][0:a]sidechaincompress=threshold=0.024:ratio=8:attack=30:release=420:makeup=1[music]",
        "[ambraw][0:a]sidechaincompress=threshold=0.020:ratio=6:attack=35:release=560:makeup=1[amb]",
        (
            "[0:a][music][amb]amix=inputs=3:normalize=0:duration=longest:dropout_transition=0,"
            f"atrim=0:{total_sec:.3f},{silence_filter}"
            f"loudnorm=I=-14:TP=-1:LRA=11:linear=false,alimiter=limit=0.84,volume=0.92,"
            f"afade=t=out:st={max(total_sec - 2.2, 0):.3f}:d=2.2[aout]"
        ),
    ]
    tmp = REMOTION_AUDIO.with_suffix(".tmp.wav")
    run_ffmpeg([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[aout]", "-t", f"{total_sec:.3f}", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", tmp])
    tmp.replace(REMOTION_AUDIO)
    media_audio = MEDIA / "episodes" / EP / "06_audio" / REMOTION_AUDIO.name
    media_audio.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REMOTION_AUDIO, media_audio)


def write_roughcut(base: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    out = {
        "episodeId": EP,
        "title": "Nothing - OneCoin Editorial Cut v008",
        "fps": 30,
        "timelineMode": "editorial",
        "narrationSrc": "onecoin/audio/onecoin_final_mix_v008.wav",
        "bgmSrc": None,
        "shots": rows,
    }
    ROUGH_TS.write_text(
        "// EDITORIAL v008 generated by scripts/build_onecoin_editorial_v008.py.\n"
        "// Natural-speed narration, 8s hook, faster visual turnover, cleaner captions.\n"
        "import type {RoughCutData} from '../compositions/RoughCut';\n\n"
        "export const ONECOIN_ROUGHCUT: RoughCutData = "
        + json.dumps(out, indent=2, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )


def write_qc(timed: list[dict[str, Any]], cues: list[dict[str, Any]], total_sec: float, plan_rows: list[dict[str, Any]]) -> None:
    loudness = audio_base.loudness_probe(REMOTION_AUDIO)
    AUDIO_QC.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v008",
                "audio_revision": "v008",
                "created_at": now(),
                "provider": "elevenlabs_master_reused_contract_voice",
                "voice_id": "nPczCjzI2devNBz1zQrb",
                "external_api_calls": False,
                "mix_path": str(REMOTION_AUDIO).replace("\\", "/"),
                "mix_sha256": sha256(REMOTION_AUDIO),
                "mix_duration_seconds": duration(REMOTION_AUDIO),
                "timeline_seconds": total_sec,
                "caption_cues": len(cues),
                "caption_last_end_seconds": cues[-1]["end"] if cues else 0,
                "loudness_probe": loudness,
                "editorial_changes": [
                    "tightened cold open to an 8.0s hook",
                    "removed global 30-minute time stretch",
                    "used natural-speed ElevenLabs chunks",
                    "increased visual turnover via denser image lists and shorter dwell",
                    "shorter caption chunks and tighter timing windows",
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    PLAN.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v008",
                "created_at": now(),
                "timeline_seconds": total_sec,
                "removed_spans": ["SPN-0001", "SPN-0002", "SPN-0004", "SPN-0005"],
                "hook_source_span": HOOK_SPAN,
                "rows": plan_rows,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def update_manifest() -> None:
    manifest_path = EPDIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    active = manifest.setdefault("active_revisions", {})
    active.update({"roughcut": "v008", "audio_mix": "v005_editorial_v008", "captions": "v005_editorial_v008", "onecoin_captions": "v008"})
    manifest["state"] = "editorial_v008_audio_ready"
    manifest["updated_at"] = now()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"ts": now(), "episode_id": EP, "stage": "edit", "event": "editorial_v008_audio_timeline_built", "actor": "codex", "external_api_calls": False, "note": "8.0s hook, no post-hook brand silence, faster visual turnover, cleaner captions. No upload/publish/schedule."}, ensure_ascii=False) + "\n")


def main() -> int:
    base = parse_roughcut()
    voice = load_voice_index()
    rows, plan_rows = build_rows(base, voice)
    timed, total_sec = build_voice_segments(rows, voice)
    cues = write_captions(timed)
    build_mix(timed, total_sec)
    write_roughcut(base, rows)
    write_qc(timed, cues, total_sec, plan_rows)
    update_manifest()
    print(json.dumps({"timeline_seconds": round(total_sec, 3), "minutes": round(total_sec / 60, 2), "audio": str(REMOTION_AUDIO), "captions": str(CAPTIONS_SRT), "roughcut": str(ROUGH_TS)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
