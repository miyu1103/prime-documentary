#!/usr/bin/env python3
"""Build OneCoin v009 editorial timeline, natural-speed audio, and captions.

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
REMOTION_AUDIO = REMOTION / "public" / "onecoin" / "audio" / "onecoin_final_mix_v009.wav"
MEDIA = Path("H:/pd-media")
WORK = MEDIA / "episodes" / EP / "06_audio" / "editorial_v009"
FIT_DIR = WORK / "fit_wav"
VOICE_INDEX = EPDIR / "06_audio" / "narration_index.v003.json"
CAPTIONS_SRT = EPDIR / "08_edit" / "captions.v006.editorial_v009.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v006.editorial_v009.json"
AUDIO_QC = EPDIR / "08_edit" / "audio_mix.v006.editorial_v009.qc.json"
PLAN = EPDIR / "08_edit" / "onecoin_editorial_plan.v009.json"
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
    narration = WORK / "narration_editorial_v009.wav"
    run_ffmpeg([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c:a", "pcm_s16le", narration])
    return timed, total


def wrap_caption_chunks(text: str) -> list[str]:
    words = text.replace("\n", " ").split()
    chunks: list[str] = []
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if len(trial) <= 42:
            current = trial
            continue
        if len(lines) < 1:
            if current:
                lines.append(current)
            current = word
            continue
        if current:
            lines.append(current)
        chunks.append("\n".join(lines))
        lines = []
        current = word
    if current:
        lines.append(current)
    if lines:
        chunks.append("\n".join(lines[:2]))
    return chunks


def split_caption_parts(text: str) -> list[str]:
    tokens = re.findall(r"\S+", text)
    parts: list[str] = []
    cur: list[str] = []
    for token in tokens:
        trial = " ".join(cur + [token])
        hard_pause = bool(cur and re.search(r"[.?!]$", cur[-1]))
        soft_pause = bool(cur and re.search(r"[,;:]$", cur[-1]) and len(cur) >= 4)
        length_pause = bool(cur and (len(trial) > 74 or len(cur) >= 12))
        if hard_pause or soft_pause or length_pause:
            parts.extend(wrap_caption_chunks(" ".join(cur)))
            cur = [token]
        else:
            cur.append(token)
    if cur:
        parts.extend(wrap_caption_chunks(" ".join(cur)))
    return parts


def silence_windows(path: Path, raw_seconds: float) -> list[tuple[float, float]]:
    proc = subprocess.run(
        [
            FFMPEG,
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-af",
            "silencedetect=noise=-38dB:d=0.16",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    text = (proc.stderr or "") + "\n" + (proc.stdout or "")
    starts = [float(x) for x in re.findall(r"silence_start:\s*([0-9.]+)", text)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", text)]
    silences: list[tuple[float, float]] = []
    for i, start in enumerate(starts):
        end = ends[i] if i < len(ends) else raw_seconds
        if end > start:
            silences.append((max(0.0, start), min(raw_seconds, end)))
    windows: list[tuple[float, float]] = []
    cursor = 0.0
    for start, end in silences:
        if start - cursor >= 0.22:
            windows.append((cursor, start))
        cursor = max(cursor, end)
    if raw_seconds - cursor >= 0.22:
        windows.append((cursor, raw_seconds))
    return windows


def assign_parts_to_windows(parts: list[str], windows: list[tuple[float, float]], row_start: float, row_end: float) -> list[tuple[float, float, str]]:
    if not parts:
        return []
    if len(windows) < 2:
        weights = [max(1, len(part.replace("\n", " ").split())) for part in parts]
        total = sum(weights)
        cursor = row_start
        elapsed = 0
        cues: list[tuple[float, float, str]] = []
        for part, weight in zip(parts, weights):
            elapsed += weight
            end = row_start + (row_end - row_start) * elapsed / total
            cues.append((cursor, end, part))
            cursor = end
        return cues

    if len(parts) > len(windows):
        cues: list[tuple[float, float, str]] = []
        n_parts = len(parts)
        n_windows = len(windows)
        for i in range(n_windows):
            first = round(i * n_parts / n_windows)
            last = max(first + 1, round((i + 1) * n_parts / n_windows))
            chunks = wrap_caption_chunks(" ".join(part.replace("\n", " ") for part in parts[first:last]))
            start = row_start + windows[i][0]
            end = row_start + windows[i][1]
            weights = [max(1, len(chunk.replace("\n", " ").split())) for chunk in chunks]
            total = sum(weights)
            cursor = start
            elapsed = 0
            for chunk, weight in zip(chunks, weights):
                elapsed += weight
                chunk_end = start + (end - start) * elapsed / total
                cues.append((cursor, chunk_end, chunk))
                cursor = chunk_end
        return cues

    cues = []
    n = len(parts)
    w = len(windows)
    for i, part in enumerate(parts):
        first = round(i * w / n)
        last = max(first, round((i + 1) * w / n) - 1)
        first = min(first, w - 1)
        last = min(last, w - 1)
        start = row_start + windows[first][0]
        end = row_start + windows[last][1]
        cues.append((start, end, part))
    return cues


def write_captions(timed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cues: list[dict[str, Any]] = []
    index = 1
    for row in timed:
        if not row.get("speak"):
            continue
        parts = split_caption_parts(row["text"])
        start = float(row["voice_start"])
        end = float(row["voice_end"])
        raw_seconds = max(0.2, float(row.get("raw_seconds", end - start)))
        windows = silence_windows(FIT_DIR / row["file"], raw_seconds)
        assigned = assign_parts_to_windows(parts, windows, start, end)
        for cue_start, cue_end, part in assigned:
            cue_start = max(start, min(cue_start, end - 0.18))
            cue_end = min(end, max(cue_end, cue_start + 0.35))
            cues.append({"index": index, "start": round(cue_start, 3), "end": round(cue_end, 3), "text": part})
            index += 1
    CAPTIONS_SRT.write_text("\n".join(f"{cue['index']}\n{audio_base.srt_ts(cue['start'])} --> {audio_base.srt_ts(cue['end'])}\n{cue['text']}\n" for cue in cues), encoding="utf-8")
    CAPTIONS_JSON.write_text(json.dumps({"episode_id": EP, "revision": "v009", "alignment_method": "breath_pause_silencedetect_sentence_weighted", "cues": cues}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CAPTIONS_TS.write_text(
        "// Editorial v009 captions from natural-speed ElevenLabs master chunks, cut by breath pauses.\n"
        "import type {CaptionCue} from '../compositions/RoughCut';\n\n"
        "export const ONECOIN_CAPTIONS: CaptionCue[] = "
        + json.dumps([{"id": f"onecoin-caption-v009-{i + 1:04d}", "start": cue["start"], "end": cue["end"], "text": cue["text"]} for i, cue in enumerate(cues)], indent=2, ensure_ascii=False)
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
    narration = WORK / "narration_editorial_v009.wav"
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
        "title": "Nothing - OneCoin Editorial Cut v009",
        "fps": 30,
        "timelineMode": "editorial",
        "narrationSrc": "onecoin/audio/onecoin_final_mix_v009.wav",
        "bgmSrc": None,
        "shots": rows,
    }
    ROUGH_TS.write_text(
        "// EDITORIAL v009 generated by scripts/build_onecoin_editorial_v009.py.\n"
        "// Natural-speed narration, 8s hook, faster visual turnover, breath-pause captions.\n"
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
                "revision": "v009",
                "audio_revision": "v009",
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
                    "caption cues rebuilt from sentence clauses and detected breath pauses",
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
                "revision": "v009",
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
    active.update({"roughcut": "v009", "onecoin_roughcut": "v009", "audio_mix": "v006_editorial_v009", "captions": "v006_editorial_v009", "onecoin_captions": "v009"})
    manifest["state"] = "editorial_v009_audio_ready"
    manifest["updated_at"] = now()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"ts": now(), "episode_id": EP, "stage": "edit", "event": "editorial_v009_audio_timeline_built", "actor": "codex", "external_api_calls": False, "note": "v009 rebuilds captions by breath pauses and improves subtitle readability. No upload/publish/schedule."}, ensure_ascii=False) + "\n")


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
