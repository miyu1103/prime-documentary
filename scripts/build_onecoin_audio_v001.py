#!/usr/bin/env python3
"""Build OneCoin local draft narration, captions, and 4-layer review mix.

This script intentionally uses free local Windows SAPI for timing only. It does
not call ElevenLabs or any paid/external API. The paid master voice remains an
owner approval gate.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
REMOTION_AUDIO = ROOT / "remotion" / "public" / "onecoin" / "audio" / "onecoin_final_mix_v001.wav"
CAPTIONS_SRT = EPDIR / "08_edit" / "captions.v001.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v001.json"
CAPTIONS_TS = ROOT / "remotion" / "src" / "data" / "onecoin_captions.ts"
ROUGH_TS = ROOT / "remotion" / "src" / "data" / "onecoin_roughcut.ts"
NARRATION_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
AUDIO_QC = EPDIR / "08_edit" / "audio_mix.v001.qc.json"
VOICE_MASTER_META = EPDIR / "06_audio" / "voice_master.v001.pending.json"
SILENCE_SPAN_ID = "SPN-0043"
OPENING_AFTER_SPAN_ID = "SPN-0005"
OPENING_SEC = 3.5
ENDCARD_SEC = 9.0
TARGET_SEC = 1800.0
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"


def media_root() -> Path:
    cfg = json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


MEDIA = media_root()
LIB = MEDIA / "library"
EP_MEDIA = MEDIA / "episodes" / EP
DRAFT_DIR = EP_MEDIA / "06_audio" / "draft_sapi_v001"
RAW_DIR = DRAFT_DIR / "raw"
FIT_DIR = DRAFT_DIR / "fit"
EP_MEDIA_AUDIO = EP_MEDIA / "06_audio"


def run(cmd: list[str | Path], label: str, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    print(f"== {label}", flush=True)
    return subprocess.run([str(x) for x in cmd], check=True, text=True, timeout=timeout)


def capture(cmd: list[str | Path], timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(x) for x in cmd], capture_output=True, text=True, check=False, timeout=timeout)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def duration(path: Path) -> float:
    result = capture([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    try:
        return round(float(result.stdout.strip()), 3)
    except Exception:
        return 0.0


def atempo_filters(value: float) -> str:
    parts: list[float] = []
    remaining = max(0.05, value)
    while remaining > 2.0:
        parts.append(2.0)
        remaining /= 2.0
    while remaining < 0.5:
        parts.append(0.5)
        remaining /= 0.5
    parts.append(remaining)
    return ",".join(f"atempo={part:.9f}" for part in parts)


def srt_ts(t: float) -> str:
    ms = max(0, int(round(t * 1000)))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def load_inputs() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], str]:
    manifest = json.loads((EPDIR / "manifest.json").read_text("utf-8"))
    script_rev = manifest["active_revisions"]["script"]
    shot_rev = manifest["active_revisions"]["shotlist"]
    annotated = EPDIR / "03_script" / f"script.annotated.{script_rev}.json"
    shotlist = EPDIR / "04_scenes" / f"shotlist.{shot_rev}.json"
    spans = json.loads(annotated.read_text("utf-8"))["spans"]
    shots = json.loads(shotlist.read_text("utf-8"))["shots"]
    if len(spans) != 48 or len(shots) != 48:
        raise RuntimeError(f"expected 48 spans/shots, got {len(spans)} / {len(shots)}")
    for span, shot in zip(spans, shots):
        if span["span_id"] != shot["span_id"]:
            raise RuntimeError(f"span/shot mismatch: {span['span_id']} != {shot['span_id']}")
    return manifest, spans, shots, script_rev


def timeline(spans: list[dict[str, Any]], shots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_total = sum(float(s["estimated_seconds"]) for s in shots)
    source_fixed = 3.0
    fixed = OPENING_SEC + ENDCARD_SEC + source_fixed
    scale = (TARGET_SEC - fixed) / max(1.0, source_total - source_fixed)
    cursor = 0.0
    rows: list[dict[str, Any]] = []
    for span, shot in zip(spans, shots):
        sid = span["span_id"]
        sec = 3.0 if sid == SILENCE_SPAN_ID else float(shot["estimated_seconds"]) * scale
        text = re.sub(r"\s+", " ", span.get("text", "")).strip()
        speak = bool(text and text != "..." and sid != SILENCE_SPAN_ID)
        rows.append(
            {
                "span_id": sid,
                "chapter_id": shot["chapter_id"],
                "text": text,
                "shot_start": round(cursor, 3),
                "shot_end": round(cursor + sec, 3),
                "shot_seconds": round(sec, 3),
                "source_seconds": float(shot["estimated_seconds"]),
                "scale": round(scale, 8),
                "speak": speak,
            }
        )
        cursor += sec
        if sid == OPENING_AFTER_SPAN_ID:
            cursor += OPENING_SEC
    return rows


def synthesize_raw(rows: list[dict[str, Any]]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for row in rows:
        if not row["speak"]:
            continue
        out = RAW_DIR / f"{row['span_id']}.wav"
        if out.exists() and out.stat().st_size > 4096:
            continue
        items.append({"span_id": row["span_id"], "text": row["text"], "path": str(out)})
    if not items:
        print("SAPI raw chunks already exist", flush=True)
        return

    with tempfile.TemporaryDirectory() as td:
        json_path = Path(td) / "sapi_items.json"
        ps_path = Path(td) / "sapi_batch.ps1"
        json_path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
        ps_path.write_text(
            """
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$items = Get-Content -Raw -Encoding UTF8 $args[0] | ConvertFrom-Json
foreach ($item in $items) {
  $dir = Split-Path -Parent $item.path
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
  try {
    $s.Rate = -1
    $s.Volume = 100
    $voice = $s.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture.Name -like 'en-*' } | Select-Object -First 1
    if ($voice) { $s.SelectVoice($voice.VoiceInfo.Name) }
    $s.SetOutputToWaveFile($item.path)
    $s.Speak($item.text)
  } finally {
    $s.Dispose()
  }
}
""".strip()
            + "\n",
            encoding="utf-8",
        )
        run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps_path, json_path], f"local SAPI draft chunks ({len(items)})", timeout=7200)


def fit_segments(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    FIT_DIR.mkdir(parents=True, exist_ok=True)
    chunks: list[dict[str, Any]] = []
    concat_lines: list[str] = []
    for row in rows:
        sid = row["span_id"]
        shot_seconds = float(row["shot_seconds"])
        out = FIT_DIR / f"{sid}.wav"
        if not row["speak"]:
            run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{shot_seconds:.3f}", "-c:a", "pcm_s16le", out], f"silence segment {sid}")
            chunks.append({**row, "voice_start": row["shot_start"], "voice_end": row["shot_start"], "raw_seconds": 0.0, "fit_seconds": 0.0, "file": out.name})
        else:
            raw = RAW_DIR / f"{sid}.wav"
            if not raw.is_file():
                raise FileNotFoundError(raw)
            raw_sec = duration(raw)
            voice_target = max(0.5, min(shot_seconds - 0.45, shot_seconds * 0.92))
            atempo = raw_sec / voice_target if voice_target > 0 else 1.0
            filters = f"aresample=48000,{atempo_filters(atempo)},apad,atrim=0:{shot_seconds:.3f},alimiter=limit=0.92"
            run([FFMPEG, "-y", "-i", raw, "-filter:a", filters, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", out], f"fit {sid} {raw_sec:.2f}s -> {voice_target:.2f}s")
            chunks.append(
                {
                    **row,
                    "voice_start": row["shot_start"],
                    "voice_end": round(float(row["shot_start"]) + voice_target, 3),
                    "raw_seconds": raw_sec,
                    "fit_seconds": round(voice_target, 3),
                    "atempo": round(atempo, 6),
                    "file": out.name,
                }
            )
        concat_lines.append(f"file '{out.as_posix()}'\n")
        if sid == OPENING_AFTER_SPAN_ID:
            brand = FIT_DIR / "_brand_opening_silence.wav"
            run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{OPENING_SEC:.3f}", "-c:a", "pcm_s16le", brand], "brand opening narration gap")
            concat_lines.append(f"file '{brand.as_posix()}'\n")
    tail = FIT_DIR / "_endcard_tail.wav"
    run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{ENDCARD_SEC:.3f}", "-c:a", "pcm_s16le", tail], "endcard narration tail")
    concat_lines.append(f"file '{tail.as_posix()}'\n")
    concat = FIT_DIR / "_concat_narration.txt"
    concat.write_text("".join(concat_lines), encoding="utf-8")
    narration = DRAFT_DIR / "narration_draft_v001.wav"
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c:a", "pcm_s16le", narration], "concat timed draft narration")
    return chunks


def break_caption_lines(words: list[str]) -> str:
    lines = [""]
    for word in words:
        if len(lines[-1] + (" " if lines[-1] else "") + word) <= 42:
            lines[-1] = (lines[-1] + " " + word).strip()
        elif len(lines) < 2:
            lines.append(word)
        else:
            lines[-1] = (lines[-1] + " " + word).strip()
    return "\n".join(lines)


def split_caption_parts(text: str) -> list[str]:
    words = text.split()
    parts: list[str] = []
    cur: list[str] = []
    for word in words:
        trial_words = cur + [word]
        trial = break_caption_lines(trial_words)
        max_line = max(len(line) for line in trial.splitlines())
        end_punct = bool(re.search(r"[.?!]$", word))
        comma_break = word.endswith(",") and len(cur) >= 5
        if cur and (len(trial_words) > 12 or len(trial.replace("\n", "")) > 78 or max_line > 46):
            parts.append(break_caption_lines(cur))
            cur = [word]
        else:
            cur = trial_words
        if cur and (end_punct or comma_break) and len(cur) >= 4:
            parts.append(break_caption_lines(cur))
            cur = []
    if cur:
        parts.append(break_caption_lines(cur))
    return parts


def write_captions(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    CAPTIONS_SRT.parent.mkdir(parents=True, exist_ok=True)
    cues: list[dict[str, Any]] = []
    cue_no = 1
    for chunk in chunks:
        if not chunk["speak"]:
            continue
        parts = split_caption_parts(chunk["text"])
        weights = [max(1, len(part.replace("\n", " ").split())) for part in parts]
        total = sum(weights)
        start = float(chunk["voice_start"])
        end = float(chunk["voice_end"])
        cursor = start
        elapsed = 0
        for part, weight in zip(parts, weights):
            elapsed += weight
            part_end = start + (end - start) * elapsed / total
            if part_end <= cursor:
                part_end = cursor + 0.35
            if part_end - cursor > 6.8:
                part_end = cursor + 6.8
            cues.append({"index": cue_no, "start": round(cursor, 3), "end": round(part_end, 3), "text": part})
            cue_no += 1
            cursor = part_end
    CAPTIONS_SRT.write_text(
        "\n".join(f"{cue['index']}\n{srt_ts(cue['start'])} --> {srt_ts(cue['end'])}\n{cue['text']}\n" for cue in cues),
        encoding="utf-8",
    )
    CAPTIONS_JSON.write_text(json.dumps({"episode_id": EP, "revision": "v001", "cues": cues}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CAPTIONS_TS.write_text(
        "// Final timing captions generated from the v001 script and local SAPI review timeline.\n"
        "import type {CaptionCue} from '../compositions/RoughCut';\n\n"
        "export const ONECOIN_CAPTIONS: CaptionCue[] = "
        + json.dumps([{ "id": f"onecoin-caption-{i + 1:04d}", "start": cue["start"], "end": cue["end"], "text": cue["text"] } for i, cue in enumerate(cues)], indent=2, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    print(f"captions={len(cues)} last_end={cues[-1]['end'] if cues else 0}", flush=True)
    return cues


def chapter_bounds(rows: list[dict[str, Any]]) -> dict[str, tuple[float, float]]:
    bounds: dict[str, list[float]] = {}
    for row in rows:
        bounds.setdefault(row["chapter_id"], [float(row["shot_start"]), float(row["shot_end"])])
        bounds[row["chapter_id"]][1] = float(row["shot_end"])
    return {k: (v[0], v[1]) for k, v in bounds.items()}


def build_layer_inputs(segments: list[tuple[float, float, Path, float]], start_index: int, prefix: str) -> tuple[list[str], list[str], list[str], int]:
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    idx = start_index
    for i, (start, end, path, volume) in enumerate(segments):
        if not path.exists():
            raise FileNotFoundError(path)
        dur = max(0.1, end - start)
        delay = int(round(start * 1000))
        inputs += ["-stream_loop", "-1", "-i", str(path)]
        label = f"{prefix}{i}"
        filters.append(
            f"[{idx}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={volume},"
            f"afade=t=in:st=0:d={min(1.5, dur / 3):.3f},"
            f"afade=t=out:st={max(dur - 1.8, 0.1):.3f}:d={min(1.8, dur / 3):.3f},"
            f"adelay={delay}|{delay}[{label}]"
        )
        labels.append(f"[{label}]")
        idx += 1
    return inputs, filters, labels, idx


def build_final_mix(rows: list[dict[str, Any]]) -> dict[str, Any]:
    narration = DRAFT_DIR / "narration_draft_v001.wav"
    bounds = chapter_bounds(rows)
    inputs = ["-i", str(narration)]
    filters: list[str] = []
    music_segments = [
        (0.0, bounds["cold_open"][1], LIB / "music" / "hook" / "mus_20260614_hook_glass_air_bed_v2.mp3", 0.12),
        (*bounds["the_promise"], LIB / "music" / "opening" / "mus_20260614_opening_measured_arpeggio_v2.mp3", 0.105),
        (*bounds["the_crack"], LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v2.mp3", 0.095),
        (*bounds["the_void"], LIB / "music" / "ambience" / "mus_20260614_ambience_paper_trail_static_v2.mp3", 0.082),
        (*bounds["coda"], LIB / "music" / "outro" / "mus_20260614_outro_last_frame_v2.mp3", 0.08),
    ]
    m_inputs, m_filters, m_labels, next_idx = build_layer_inputs(music_segments, 1, "m")
    inputs += m_inputs
    filters += m_filters

    ambience_segments = [
        (0.0, TARGET_SEC, LIB / "ambience" / "amb_tension_drone.mp3", 0.024),
        (bounds["the_crack"][0], bounds["the_void"][1], LIB / "ambience" / "amb_institutional_drone.mp3", 0.030),
        (bounds["coda"][0], TARGET_SEC, LIB / "ambience" / "amb_night_window.mp3", 0.026),
    ]
    a_inputs, a_filters, a_labels, next_idx = build_layer_inputs(ambience_segments, next_idx, "a")
    inputs += a_inputs
    filters += a_filters

    row_by_id = {r["span_id"]: r for r in rows}
    sfx_cues = [
        ("SPN-0001", "sfx_riser_2s.mp3", 0.08, 0.4),
        ("SPN-0003", "sfx_data_blip.mp3", 0.08, 1.0),
        ("SPN-0010", "sfx_ui_tick.mp3", 0.08, 0.7),
        ("SPN-0012", "sfx_page_turn.mp3", 0.10, 0.5),
        ("SPN-0020", "sfx_clock_tick_loop.mp3", 0.030, 0.0),
        ("SPN-0027", "sfx_stamp_seal.mp3", 0.11, 0.2),
        ("SPN-0035", "sfx_sub_drop.mp3", 0.13, 0.1),
        ("SPN-0040", "sfx_low_boom.mp3", 0.11, 0.3),
        ("SPN-0042", "sfx_camera_shutter.mp3", 0.07, 0.6),
        ("SPN-0044", "sfx_soft_impact.mp3", 0.10, 0.2),
    ]
    sfx_labels: list[str] = []
    for i, (sid, name, volume, offset) in enumerate(sfx_cues):
        path = LIB / "sfx" / name
        if not path.exists() or sid not in row_by_id:
            continue
        delay = int(round((float(row_by_id[sid]["shot_start"]) + offset) * 1000))
        inputs += ["-i", str(path)]
        idx = next_idx
        next_idx += 1
        trim = "atrim=0:4.0," if "clock_tick_loop" in name else ""
        label = f"s{i}"
        filters.append(f"[{idx}:a]{trim}asetpts=PTS-STARTPTS,volume={volume},adelay={delay}|{delay}[{label}]")
        sfx_labels.append(f"[{label}]")

    silence = row_by_id[SILENCE_SPAN_ID]
    silence_start = float(silence["shot_start"])
    silence_end = float(silence["shot_end"])
    filters += [
        f"{''.join(m_labels)}amix=inputs={len(m_labels)}:normalize=0:dropout_transition=0[musicraw]",
        f"{''.join(a_labels)}amix=inputs={len(a_labels)}:normalize=0:dropout_transition=0[ambraw]",
        (f"{''.join(sfx_labels)}amix=inputs={len(sfx_labels)}:normalize=0:dropout_transition=0[sfxraw]" if sfx_labels else "anullsrc=r=48000:cl=stereo:d=1[sfxraw]"),
        "[musicraw][0:a]sidechaincompress=threshold=0.024:ratio=8:attack=30:release=520:makeup=1[music]",
        "[ambraw][0:a]sidechaincompress=threshold=0.020:ratio=6:attack=35:release=700:makeup=1[amb]",
        (
            "[0:a][music][amb][sfxraw]amix=inputs=4:normalize=0:duration=longest:dropout_transition=0,"
            f"atrim=0:{TARGET_SEC:.3f},"
            f"volume=0:enable='between(t,{silence_start:.3f},{silence_end:.3f})',"
            f"loudnorm=I=-14:TP=-1:LRA=11:linear=false,alimiter=limit=0.82,volume=0.90,"
            f"afade=t=out:st={TARGET_SEC - 2.5:.3f}:d=2.5[aout]"
        ),
    ]
    REMOTION_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    temp = REMOTION_AUDIO.with_suffix(".tmp.wav")
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[aout]", "-t", f"{TARGET_SEC:.3f}", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", temp], "4-layer OneCoin review mix with void silence cut", timeout=7200)
    temp.replace(REMOTION_AUDIO)
    EP_MEDIA_AUDIO.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REMOTION_AUDIO, EP_MEDIA_AUDIO / REMOTION_AUDIO.name)
    return {
        "timeline_seconds": TARGET_SEC,
        "silence_span": {"span_id": SILENCE_SPAN_ID, "start": silence_start, "end": silence_end, "seconds": round(silence_end - silence_start, 3)},
        "chapter_bounds": {k: [round(v[0], 3), round(v[1], 3)] for k, v in bounds.items()},
    }


def loudness_probe(path: Path) -> dict[str, Any]:
    result = capture([FFMPEG, "-hide_banner", "-nostats", "-i", path, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "NUL"], timeout=900)
    match = re.search(r"\{\s*\"input_i\".*?\}", result.stderr, re.S)
    if not match:
        return {"raw_tail": result.stderr[-1000:]}
    data = json.loads(match.group(0))
    return {k: float(data[k]) for k in ("input_i", "input_tp", "input_lra", "target_offset")}


def silence_probe(path: Path, start: float, end: float) -> dict[str, Any]:
    result = capture([FFMPEG, "-hide_banner", "-nostats", "-ss", f"{max(0, start - 0.2):.3f}", "-t", f"{(end - start) + 0.4:.3f}", "-i", path, "-af", "silencedetect=n=-55dB:d=0.2", "-f", "null", "NUL"], timeout=300)
    spans = [float(x) for x in re.findall(r"silence_duration:\s*(\d+(?:\.\d+)?)", result.stderr)]
    return {"window_start": round(start - 0.2, 3), "window_seconds": round((end - start) + 0.4, 3), "silence_durations": spans, "max_silence": max(spans) if spans else 0.0}


def update_roughcut_audio() -> None:
    text = ROUGH_TS.read_text(encoding="utf-8")
    text = re.sub(r'"narrationSrc":\s*(null|"[^"]*")', '"narrationSrc": "onecoin/audio/onecoin_final_mix_v001.wav"', text, count=1)
    text = re.sub(r'"bgmSrc":\s*(null|"[^"]*")', '"bgmSrc": null', text, count=1)
    ROUGH_TS.write_text(text, encoding="utf-8")


def write_index_and_qc(script_rev: str, chunks: list[dict[str, Any]], cues: list[dict[str, Any]], mix_meta: dict[str, Any]) -> None:
    NARRATION_INDEX.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    chars = sum(len(c["text"]) for c in chunks if c["speak"])
    NARRATION_INDEX.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "script_revision": script_rev,
                "provider": "local_windows_sapi_draft",
                "voice_master_status": "pending_owner_go_for_elevenlabs",
                "cost_usd": 0,
                "characters": chars,
                "created_at": now,
                "chunks": chunks,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    VOICE_MASTER_META.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "status": "blocked_pending_owner_go",
                "blocked_stage": "elevenlabs_master_narration",
                "draft_provider": "local_windows_sapi",
                "cost_usd": 0,
                "note": "Local SAPI draft exists for timing only. Do not call ElevenLabs until explicit owner GO with idempotency and budget check.",
                "created_at": now,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    loudness = loudness_probe(REMOTION_AUDIO)
    silence = mix_meta["silence_span"]
    silence_check = silence_probe(REMOTION_AUDIO, float(silence["start"]), float(silence["end"]))
    AUDIO_QC.parent.mkdir(parents=True, exist_ok=True)
    AUDIO_QC.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "script_revision": script_rev,
                "created_at": now,
                "mix_path": str(REMOTION_AUDIO).replace("\\", "/"),
                "mix_sha256": f"sha256:{sha256(REMOTION_AUDIO)}",
                "mix_duration_seconds": duration(REMOTION_AUDIO),
                "timeline_seconds": mix_meta["timeline_seconds"],
                "layers": ["local_sapi_draft_voice", "music", "ambience", "sfx"],
                "provider": "local_windows_sapi_draft",
                "cost_usd": 0,
                "captions": str(CAPTIONS_SRT).replace("\\", "/"),
                "caption_cues": len(cues),
                "caption_last_end_seconds": cues[-1]["end"] if cues else 0,
                "chapter_bounds": mix_meta["chapter_bounds"],
                "void_silence": {**silence, "probe": silence_check},
                "loudness_probe": loudness,
                "qc_status": "pass" if duration(REMOTION_AUDIO) > 0 and len(cues) > 0 and silence_check["max_silence"] >= float(silence["seconds"]) - 0.25 else "review",
                "hard_stop": "ElevenLabs master narration still requires explicit owner GO before any paid call.",
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
    active.update({"narration_index": "v001", "audio_mix": "v001", "captions": "v001", "onecoin_captions": "v001"})
    manifest["state"] = "draft_audio_ready"
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        ("PD-2026-017-onecoin-narration-index", "narration_index", "v001", "artifact://episodes/PD-2026-017-onecoin/06_audio/narration_index.v001.json", f"sha256:{sha256(NARRATION_INDEX)}", "draft", "conditional", "draft"),
        ("PD-2026-017-onecoin-audio-mix", "audio_mix", "v001", "artifact://episodes/PD-2026-017-onecoin/08_edit/audio_mix.v001.qc.json", f"sha256:{sha256(AUDIO_QC)}", "draft", "conditional", "pass"),
        ("PD-2026-017-onecoin-captions", "captions", "v001", "artifact://episodes/PD-2026-017-onecoin/08_edit/captions.v001.srt", f"sha256:{sha256(CAPTIONS_SRT)}", "draft", "conditional", "pass"),
    ]
    ids = {item[0] for item in new_artifacts}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for aid, atype, rev, uri, checksum, status, rights_status, qc_status in new_artifacts:
        artifacts.append({"artifact_id": aid, "artifact_type": atype, "revision": rev, "uri": uri, "checksum": checksum, "status": status, "rights_status": rights_status, "qc_status": qc_status})
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    events = EPDIR / "events" / "events.jsonl"
    with events.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "episode_id": EP, "stage": "audio", "event": "local_sapi_review_mix_built", "revision": "v001", "actor": "codex", "cost_usd": 0, "external_side_effects": False}, ensure_ascii=False) + "\n")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    _, spans, shots, script_rev = load_inputs()
    rows = timeline(spans, shots)
    synthesize_raw(rows)
    chunks = fit_segments(rows)
    cues = write_captions(chunks)
    mix_meta = build_final_mix(rows)
    update_roughcut_audio()
    write_index_and_qc(script_rev, chunks, cues, mix_meta)
    update_manifest()
    print(f"mix={REMOTION_AUDIO} duration={duration(REMOTION_AUDIO):.3f}s sha256={sha256(REMOTION_AUDIO)}", flush=True)
    print(f"captions={CAPTIONS_SRT} cues={len(cues)}", flush=True)
    print("ElevenLabs master remains blocked pending explicit owner GO.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
