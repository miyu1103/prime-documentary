#!/usr/bin/env python3
"""Build Titan final audio mix and captions from ElevenLabs master chunks.

No external calls. Uses already generated ElevenLabs chunk files, places them
on the approved 107-span visual timeline, keeps SPN-0071 completely silent,
and writes a 4-layer WAV mix for Remotion.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-016-titan"
EPDIR = ROOT / "episodes" / EP
REM_AUDIO = ROOT / "remotion" / "public" / "titan" / "audio" / "titan_final_mix_v001.wav"
REM_CAPTIONS = ROOT / "remotion" / "src" / "data" / "titan_captions.ts"
CAPTIONS_SRT = EPDIR / "08_edit" / "captions.v001.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.v001.json"
QC = EPDIR / "08_edit" / "audio_mix.v001.qc.json"
SILENCE_SPAN_ID = "SPN-0071"
OPENING_AFTER_SPAN_ID = "SPN-0005"
OPENING_SEC = 3.5
ENDCARD_SEC = 9.0
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"


def media_root() -> Path:
    cfg = json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


MEDIA = media_root()
LIB = MEDIA / "library"
EP_MEDIA = MEDIA / "episodes" / EP
DRAFT = EP_MEDIA / "06_voice" / "draft"
WORK = EP_MEDIA / "06_audio" / "final_mix_v001_work"
EP_AUDIO = EP_MEDIA / "06_audio"


def run(cmd: list[str | Path], label: str, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    print(f"== {label}", flush=True)
    return subprocess.run([str(x) for x in cmd], check=True, text=True, timeout=timeout)


def capture(cmd: list[str | Path], timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(x) for x in cmd], capture_output=True, text=True, check=False, timeout=timeout)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
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


def inputs() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = json.loads((EPDIR / "manifest.json").read_text("utf-8"))
    script_rev = manifest["active_revisions"]["script"]
    spans = json.loads((EPDIR / "03_script" / f"script.annotated.{script_rev}.json").read_text("utf-8"))["spans"]
    shots = json.loads((EPDIR / "04_scenes" / "shotlist.v001.json").read_text("utf-8"))["shots"]
    index = json.loads((EPDIR / "06_audio" / "narration_index.v001.json").read_text("utf-8"))["chunks"]
    return manifest, spans, shots, index


def timeline(spans: list[dict[str, Any]], shots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cursor = 0.0
    rows: list[dict[str, Any]] = []
    for span, shot in zip(spans, shots):
        sid = span["span_id"]
        sec = float(shot["estimated_seconds"])
        rows.append(
            {
                "span_id": sid,
                "chapter_id": shot["chapter_id"],
                "text": re.sub(r"\s+", " ", span.get("text", "")).strip(),
                "shot_start": round(cursor, 3),
                "shot_end": round(cursor + sec, 3),
                "shot_seconds": round(sec, 3),
                "speak": bool(span.get("text") and span.get("text") != "..." and sid != SILENCE_SPAN_ID),
            }
        )
        cursor += sec
        if sid == OPENING_AFTER_SPAN_ID:
            cursor += OPENING_SEC
    return rows


def chapter_bounds(rows: list[dict[str, Any]]) -> dict[str, tuple[float, float]]:
    out: dict[str, list[float]] = {}
    for row in rows:
        out.setdefault(row["chapter_id"], [row["shot_start"], row["shot_end"]])
        out[row["chapter_id"]][1] = row["shot_end"]
    return {k: (v[0], v[1]) for k, v in out.items()}


def build_narration(rows: list[dict[str, Any]], index: list[dict[str, Any]], total_sec: float) -> tuple[Path, list[dict[str, Any]]]:
    WORK.mkdir(parents=True, exist_ok=True)
    by_span = {item["span_id"]: item for item in index}
    inputs_args: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    timed: list[dict[str, Any]] = []
    input_idx = 0
    for row in rows:
        if not row["speak"]:
            continue
        item = by_span[row["span_id"]]
        src = DRAFT / item["file"]
        if not src.exists():
            raise FileNotFoundError(src)
        raw_dur = duration(src)
        available = max(0.45, float(row["shot_seconds"]) - 0.32)
        out_dur = min(raw_dur, available)
        filters_for_input = "aresample=48000,asetpts=PTS-STARTPTS"
        if raw_dur > available:
            filters_for_input += f",{atempo_filters(raw_dur / available)}"
        start = float(row["shot_start"])
        delay = int(start * 1000)
        label = f"v{len(labels)}"
        inputs_args += ["-i", str(src)]
        filters.append(
            f"[{input_idx}:a]{filters_for_input},atrim=0:{out_dur:.3f},volume=1.0,adelay={delay}|{delay}[{label}]"
        )
        labels.append(f"[{label}]")
        timed.append({**row, "voice_start": round(start, 3), "voice_end": round(start + out_dur, 3), "voice_seconds": round(out_dur, 3), "raw_voice_seconds": raw_dur, "chunk_id": item["chunk_id"], "file": item["file"]})
        input_idx += 1
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,atrim=0:{total_sec:.3f},alimiter=limit=0.92[vo]")
    out = WORK / "narration_timeline_v001.wav"
    run([FFMPEG, "-y", *inputs_args, "-filter_complex", ";".join(filters), "-map", "[vo]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", out], "place ElevenLabs narration on Titan timeline", timeout=7200)
    return out, timed


def split_caption_parts(text: str) -> list[str]:
    words = text.split()
    parts: list[str] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join(cur + [word])
        flush = cur and (len(cur) >= 6 or len(trial) > 42)
        if flush:
            parts.append(" ".join(cur))
            cur = []
        cur.append(word)
        if re.search(r"[.?!]$", word) or (word.endswith(",") and len(cur) >= 4) or word.endswith(";"):
            parts.append(" ".join(cur))
            cur = []
    if cur:
        parts.append(" ".join(cur))
    return [re.sub(r"\s+", " ", p).strip() for p in parts if p.strip()]


def write_captions(timed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cues: list[dict[str, Any]] = []
    idx = 1
    for item in timed:
        parts = split_caption_parts(item["text"])
        if not parts:
            continue
        weights = [max(1, len(part.split())) for part in parts]
        total = sum(weights)
        start = float(item["voice_start"])
        end = float(item["voice_end"])
        cursor = start
        elapsed = 0
        for part, weight in zip(parts, weights):
            elapsed += weight
            part_end = start + (end - start) * elapsed / total
            if part_end <= cursor + 0.18:
                part_end = min(end, cursor + 0.18)
            if part_end <= cursor:
                continue
            cues.append({"index": idx, "start": round(cursor, 3), "end": round(part_end, 3), "text": part})
            idx += 1
            cursor = part_end
    CAPTIONS_SRT.parent.mkdir(parents=True, exist_ok=True)
    CAPTIONS_SRT.write_text("\n".join(f"{c['index']}\n{srt_ts(c['start'])} --> {srt_ts(c['end'])}\n{c['text']}\n" for c in cues), "utf-8")
    CAPTIONS_JSON.write_text(json.dumps({"episode_id": EP, "revision": "v001", "source": "ElevenLabs timeline chunks", "cues": cues}, indent=2, ensure_ascii=False) + "\n", "utf-8")
    REM_CAPTIONS.write_text(
        "export type TitanCaptionCue = {start: number; end: number; text: string};\n\n"
        "export const TITAN_CAPTIONS: TitanCaptionCue[] = "
        + json.dumps([{k: c[k] for k in ("start", "end", "text")} for c in cues], indent=2, ensure_ascii=False)
        + ";\n",
        "utf-8",
    )
    return cues


def layer_inputs(segments: list[tuple[float, float, Path, float]], start_index: int, prefix: str) -> tuple[list[str], list[str], list[str], int]:
    inputs_args: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    idx = start_index
    for i, (start, end, path, volume) in enumerate(segments):
        if not path.exists():
            raise FileNotFoundError(path)
        dur = max(0.1, end - start)
        delay = int(start * 1000)
        label = f"{prefix}{i}"
        inputs_args += ["-stream_loop", "-1", "-i", str(path)]
        filters.append(
            f"[{idx}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={volume},"
            f"afade=t=in:st=0:d={min(1.8, dur / 3):.3f},"
            f"afade=t=out:st={max(dur - 2.1, 0.1):.3f}:d={min(2.1, dur / 3):.3f},"
            f"adelay={delay}|{delay}[{label}]"
        )
        labels.append(f"[{label}]")
        idx += 1
    return inputs_args, filters, labels, idx


def build_mix(narration: Path, rows: list[dict[str, Any]], total_sec: float) -> None:
    bounds = chapter_bounds(rows)
    inputs_args = ["-i", str(narration)]
    filters: list[str] = []
    music = [
        (0.0, bounds["cold_open"][1], LIB / "music" / "hook" / "mus_20260614_hook_glass_air_bed_v2.mp3", 0.17),
        (*bounds["the_dream"], LIB / "music" / "opening" / "mus_20260614_opening_measured_arpeggio_v2.mp3", 0.15),
        (*bounds["the_warnings"], LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v2.mp3", 0.16),
        (*bounds["the_dive"], LIB / "music" / "somber" / "mus_20260614_somber_ledger_of_ash_v2.mp3", 0.14),
        (*bounds["the_search"], LIB / "music" / "reveal" / "mus_20260614_reveal_hidden_system_clicks_v2.mp3", 0.13),
        (*bounds["the_truth"], LIB / "music" / "ambience" / "mus_20260614_ambience_paper_trail_static_v2.mp3", 0.12),
        (*bounds["coda"], LIB / "music" / "outro" / "mus_20260614_outro_last_frame_v2.mp3", 0.14),
    ]
    mi, mf, ml, next_idx = layer_inputs(music, 1, "m")
    inputs_args += mi
    filters += mf
    ambience = [
        (0.0, total_sec - ENDCARD_SEC, LIB / "ambience" / "amb_tension_drone.mp3", 0.052),
        (bounds["the_warnings"][0], bounds["the_truth"][1], LIB / "ambience" / "amb_institutional_drone.mp3", 0.046),
        (bounds["coda"][0], total_sec, LIB / "ambience" / "amb_night_window.mp3", 0.038),
    ]
    ai, af, al, next_idx = layer_inputs(ambience, next_idx, "a")
    inputs_args += ai
    filters += af
    row_by_id = {row["span_id"]: row for row in rows}
    sfx = [
        ("SPN-0002", "sfx_binder_lock.mp3", 0.38, 0.7, 0.0),
        ("SPN-0005", "sfx_low_boom.mp3", 0.30, 0.1, 0.0),
        ("SPN-0030", "sfx_stamp_seal.mp3", 0.24, 0.2, 0.0),
        ("SPN-0062", "sfx_sub_drop.mp3", 0.28, 0.2, 0.0),
        ("SPN-0066", "sfx_data_blip.mp3", 0.20, 1.0, 0.0),
        ("SPN-0073", "sfx_ui_tick.mp3", 0.18, 0.6, 0.0),
        ("SPN-0075", "sfx_clock_tick_loop.mp3", 0.070, 0.0, 4.0),
        ("SPN-0080", "sfx_clock_tick_loop.mp3", 0.080, 0.0, 4.0),
        ("SPN-0084", "sfx_riser_2s.mp3", 0.20, 0.0, 0.0),
        ("SPN-0090", "sfx_paper_rustle.mp3", 0.20, 0.4, 0.0),
        ("SPN-0106", "sfx_soft_impact.mp3", 0.22, 0.2, 0.0),
    ]
    s_labels: list[str] = []
    for i, (sid, name, volume, offset, trim) in enumerate(sfx):
        path = LIB / "sfx" / name
        if not path.exists():
            raise FileNotFoundError(path)
        delay = int((row_by_id[sid]["shot_start"] + offset) * 1000)
        inputs_args += ["-i", str(path)]
        label = f"s{i}"
        trim_filter = f"atrim=0:{trim:.3f}," if trim else ""
        filters.append(f"[{next_idx}:a]{trim_filter}asetpts=PTS-STARTPTS,volume={volume},adelay={delay}|{delay}[{label}]")
        s_labels.append(f"[{label}]")
        next_idx += 1
    silence = row_by_id[SILENCE_SPAN_ID]
    filters += [
        f"{''.join(ml)}amix=inputs={len(ml)}:normalize=0:dropout_transition=0[musicraw]",
        f"{''.join(al)}amix=inputs={len(al)}:normalize=0:dropout_transition=0[ambraw]",
        f"{''.join(s_labels)}amix=inputs={len(s_labels)}:normalize=0:dropout_transition=0[sfxraw]",
        "[musicraw][0:a]sidechaincompress=threshold=0.020:ratio=9:attack=25:release=600:makeup=1[music]",
        "[ambraw][0:a]sidechaincompress=threshold=0.018:ratio=8:attack=35:release=750:makeup=1[amb]",
        (
            "[0:a][music][amb][sfxraw]amix=inputs=4:normalize=0:duration=longest:dropout_transition=0,"
            f"apad=pad_dur=12,atrim=0:{total_sec:.3f},"
            f"volume=0:enable='between(t,{silence['shot_start']:.3f},{silence['shot_end']:.3f})',"
            f"loudnorm=I=-14:TP=-1:LRA=10:linear=false,alimiter=limit=0.82,volume=0.92,"
            f"afade=t=out:st={total_sec - 2.5:.3f}:d=2.5[aout]"
        ),
    ]
    REM_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    temp = REM_AUDIO.with_suffix(".tmp.wav")
    run([FFMPEG, "-y", *inputs_args, "-filter_complex", ";".join(filters), "-map", "[aout]", "-t", f"{total_sec:.3f}", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", temp], "final Titan 4-layer mix", timeout=7200)
    temp.replace(REM_AUDIO)
    EP_AUDIO.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REM_AUDIO, EP_AUDIO / REM_AUDIO.name)


def loudness_probe(path: Path) -> dict[str, Any]:
    result = capture([FFMPEG, "-hide_banner", "-nostats", "-i", path, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "NUL"], timeout=900)
    match = re.search(r"\{\s*\"input_i\".*?\}", result.stderr, re.S)
    if not match:
        return {"raw_tail": result.stderr[-1000:]}
    data = json.loads(match.group(0))
    return {k: float(data[k]) for k in ("input_i", "input_tp", "input_lra", "target_offset")}


def silence_probe(path: Path, start: float, end: float) -> dict[str, Any]:
    result = capture([FFMPEG, "-hide_banner", "-nostats", "-ss", f"{start - 0.2:.3f}", "-t", f"{end - start + 0.4:.3f}", "-i", path, "-af", "silencedetect=n=-55dB:d=0.2", "-f", "null", "NUL"], timeout=300)
    spans = [float(x) for x in re.findall(r"silence_duration:\s*(\d+(?:\.\d+)?)", result.stderr)]
    return {"silence_durations": spans, "max_silence": max(spans) if spans else 0.0}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    manifest, spans, shots, index = inputs()
    rows = timeline(spans, shots)
    total_sec = sum(row["shot_seconds"] for row in rows) + OPENING_SEC + ENDCARD_SEC
    narration, timed = build_narration(rows, index, total_sec)
    cues = write_captions(timed)
    build_mix(narration, rows, total_sec)
    silence = next(row for row in rows if row["span_id"] == SILENCE_SPAN_ID)
    qc = {
        "episode_id": EP,
        "revision": "v001",
        "script_revision": manifest["active_revisions"]["script"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "provider": "ElevenLabs",
        "voice_id": json.loads((EPDIR / "06_audio" / "narration_index.v001.json").read_text("utf-8"))["voice_id"],
        "mix_path": str(REM_AUDIO).replace("\\", "/"),
        "mix_sha256": "sha256:" + sha256(REM_AUDIO),
        "mix_duration_seconds": duration(REM_AUDIO),
        "timeline_seconds": round(total_sec, 3),
        "layers": ["ElevenLabs narration", "music", "ambience", "sfx"],
        "captions": str(CAPTIONS_SRT).replace("\\", "/"),
        "caption_cues": len(cues),
        "caption_last_end_seconds": cues[-1]["end"] if cues else 0,
        "implosion_silence": {
            "span_id": SILENCE_SPAN_ID,
            "start": silence["shot_start"],
            "end": silence["shot_end"],
            "seconds": round(silence["shot_end"] - silence["shot_start"], 3),
            "probe": silence_probe(REM_AUDIO, silence["shot_start"], silence["shot_end"]),
        },
        "loudness_probe": loudness_probe(REM_AUDIO),
        "cost_usd_estimate": json.loads((EPDIR / "06_audio" / "narration_index.v001.json").read_text("utf-8")).get("estimated_cost_usd"),
    }
    qc["qc_status"] = "pass" if qc["implosion_silence"]["probe"]["max_silence"] >= qc["implosion_silence"]["seconds"] - 0.25 else "review"
    QC.parent.mkdir(parents=True, exist_ok=True)
    QC.write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"mix={REM_AUDIO} duration={qc['mix_duration_seconds']:.3f}s sha256={qc['mix_sha256']}")
    print(f"captions={len(cues)} last_end={qc['caption_last_end_seconds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
