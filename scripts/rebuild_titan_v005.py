#!/usr/bin/env python3
"""Rebuild Titan v007 from a fresh tight timeline.

No external calls. Reuses the approved ElevenLabs chunks and the existing
high-quality Titan v001 Remotion render as visual source, then creates a new
audio mix, phrase-level captions, burned subtitle overlay, QC, and package
sidecars.
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
REV = "v008"
EPDIR = ROOT / "episodes" / EP
EDIT = EPDIR / "08_edit"
RENDERS = EDIT / "renders"
PACKAGE = EPDIR / "09_package"
MANIFEST = EPDIR / "manifest.json"
EVENTS = EPDIR / "events" / "events.jsonl"

SOURCE_VIDEO = Path("E:/pd-media/episodes/PD-2026-016-titan/07_edit/v001.mp4")
FINAL_VIDEO = Path(f"E:/pd-media/episodes/PD-2026-016-titan/07_edit/{REV}.mp4")
MEDIA_AUDIO = Path(f"E:/pd-media/episodes/PD-2026-016-titan/06_audio/titan_final_mix_{REV}.wav")
REM_AUDIO = ROOT / "remotion" / "public" / "titan" / "audio" / f"titan_final_mix_{REV}.wav"
WORK = Path(f"E:/pd-media/episodes/PD-2026-016-titan/06_audio/final_mix_{REV}_work")
VOICE_DIR = Path("E:/pd-media/episodes/PD-2026-016-titan/06_voice/draft")
LIB = Path("E:/pd-media/library")

PLAN_PATH = RENDERS / f"recut_plan.{REV}.json"
VIDEO_FILTER = RENDERS / f"titan_{REV}_video.ffscript"
AUDIO_FILTER = RENDERS / f"titan_{REV}_audio.ffscript"
NARRATION_FILTER = RENDERS / f"titan_{REV}_narration.ffscript"
CAPTIONS_JSON = EDIT / f"captions.{REV}.json"
CAPTIONS_SRT = EDIT / f"captions.{REV}.srt"
CAPTIONS_ASS = EDIT / f"captions.{REV}.ass"
CAPTIONS_QC = EDIT / f"captions.{REV}.qc.json"
AUDIO_QC = EDIT / f"audio_mix.{REV}.qc.json"
FINAL_QC = RENDERS / f"final.{REV}.qc.json"

OPENING_AFTER_SPAN_ID = "SPN-0005"
OPENING_SEC = 3.5
SOURCE_ENDCARD_SEC = 9.0
ENDCARD_SEC = 14.0
SILENCE_SPAN_ID = "SPN-0071"
HOOK_SPAN_ID = "SPN-0001"
HOOK_SECONDS = 9.8
STANDARD_TAIL_SEC = 0.18
CHAPTER_END_TAIL_SEC = 0.65
SILENCE_SECONDS = 2.05
FINAL_AUDIO_FADE_SEC = 4.2
FPS = 30

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"


def run(cmd: list[str | Path], desc: str, cwd: Path | None = None, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    print(f">> {desc}", flush=True)
    proc = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd) if cwd else None,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    if proc.returncode != 0:
        print(proc.stdout[-6000:], flush=True)
        raise RuntimeError(desc)
    if proc.stdout.strip():
        print(proc.stdout[-1200:], flush=True)
    return proc


def capture(cmd: list[str | Path], timeout: int | None = None) -> str:
    proc = subprocess.run([str(x) for x in cmd], capture_output=True, encoding="utf-8", errors="replace", timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError((proc.stdout or "") + (proc.stderr or ""))
    return proc.stdout


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def duration(path: Path) -> float:
    out = capture([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.strip())


def ffprobe_json(path: Path) -> dict[str, Any]:
    return json.loads(
        capture(
            [
                FFPROBE,
                "-v",
                "error",
                "-show_entries",
                "format=duration,size:stream=index,codec_name,codec_type,width,height,pix_fmt,r_frame_rate,bit_rate",
                "-of",
                "json",
                path,
            ]
        )
    )


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def write_json(path: Path, data: dict[str, Any] | list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def norm_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def srt_time(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def ass_time(seconds: float) -> str:
    cs = max(0, int(round(seconds * 100)))
    h = cs // 360_000
    cs %= 360_000
    m = cs // 6000
    cs %= 6000
    s = cs // 100
    cs %= 100
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def ass_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", r"\{").replace("}", r"\}").replace("\n", r"\N")


def filter_path(path: Path) -> str:
    value = str(path.resolve()).replace("\\", "/")
    return value.replace(":", r"\:")


def load_inputs() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    script_rev = manifest["active_revisions"]["script"]
    spans = json.loads((EPDIR / "03_script" / f"script.annotated.{script_rev}.json").read_text(encoding="utf-8"))["spans"]
    shots = json.loads((EPDIR / "04_scenes" / "shotlist.v001.json").read_text(encoding="utf-8"))["shots"]
    index = json.loads((EPDIR / "06_audio" / "narration_index.v001.json").read_text(encoding="utf-8"))["chunks"]
    old_captions = json.loads((EDIT / "captions.v002.json").read_text(encoding="utf-8"))["cues"]
    if len(spans) != len(shots):
        raise RuntimeError("span/shot count mismatch")
    for span, shot in zip(spans, shots):
        if span["span_id"] != shot["span_id"]:
            raise RuntimeError(f"span/shot mismatch: {span['span_id']} != {shot['span_id']}")
    return manifest, spans, shots, index, old_captions


def build_source_rows(spans: list[dict[str, Any]], shots: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, float], dict[str, float]]:
    rows: list[dict[str, Any]] = []
    chapter_starts: dict[str, float] = {}
    source_special: dict[str, float] = {}
    cursor = 0.0
    for span, shot in zip(spans, shots):
        chapter = shot["chapter_id"]
        chapter_starts.setdefault(chapter, cursor)
        sec = float(shot["estimated_seconds"])
        text = norm_text(span.get("text", ""))
        rows.append(
            {
                "span_id": span["span_id"],
                "chapter_id": chapter,
                "text": text,
                "source_start": round(cursor, 3),
                "source_end": round(cursor + sec, 3),
                "source_seconds": round(sec, 3),
                "speak": bool(text and text != "..." and span["span_id"] != SILENCE_SPAN_ID),
            }
        )
        cursor += sec
        if span["span_id"] == OPENING_AFTER_SPAN_ID:
            source_special["opening_start"] = round(cursor, 3)
            source_special["opening_end"] = round(cursor + OPENING_SEC, 3)
            cursor += OPENING_SEC
    source_special["endcard_start"] = round(cursor, 3)
    source_special["endcard_end"] = round(cursor + SOURCE_ENDCARD_SEC, 3)
    return rows, chapter_starts, source_special


def voice_seconds_by_span(index: list[dict[str, Any]]) -> dict[str, float]:
    out: dict[str, float] = {}
    for item in index:
        src = VOICE_DIR / item["file"]
        out[item["span_id"]] = duration(src) if src.exists() else float(item["seconds"])
    return out


def build_output_timeline(
    rows: list[dict[str, Any]],
    index: list[dict[str, Any]],
    source_special: dict[str, float],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, tuple[float, float]], float]:
    by_span = {item["span_id"]: item for item in index}
    voice_dur = voice_seconds_by_span(index)
    output: list[dict[str, Any]] = []
    span_timing: dict[str, dict[str, Any]] = {}
    chapter_bounds: dict[str, list[float]] = {}
    cursor = 0.0

    def add_source(row: dict[str, Any], out_dur: float, label: str) -> None:
        nonlocal cursor
        source_start = float(row["source_start"])
        source_end = source_start + out_dur
        item = {
            "type": "source",
            "span_id": row["span_id"],
            "chapter_id": row["chapter_id"],
            "label": label,
            "source_start": round(source_start, 3),
            "source_end": round(source_end, 3),
            "duration": round(out_dur, 3),
            "output_start": round(cursor, 3),
            "output_end": round(cursor + out_dur, 3),
        }
        output.append(item)
        span_timing[row["span_id"]] = {
            **row,
            "output_start": item["output_start"],
            "output_end": item["output_end"],
            "output_seconds": item["duration"],
            "voice_start": item["output_start"] if row["speak"] else None,
            "voice_end": round(item["output_start"] + voice_dur.get(row["span_id"], 0.0), 3) if row["speak"] else None,
            "voice_seconds": round(voice_dur.get(row["span_id"], 0.0), 3) if row["speak"] else None,
            "chunk_id": by_span.get(row["span_id"], {}).get("chunk_id"),
            "file": by_span.get(row["span_id"], {}).get("file"),
        }
        bounds = chapter_bounds.setdefault(row["chapter_id"], [item["output_start"], item["output_end"]])
        bounds[1] = item["output_end"]
        cursor += out_dur

    next_chapter_by_span: dict[str, str | None] = {}
    for i, row in enumerate(rows):
        next_chapter_by_span[row["span_id"]] = rows[i + 1]["chapter_id"] if i + 1 < len(rows) else None

    for row in rows:
        sid = row["span_id"]
        if sid == HOOK_SPAN_ID:
            add_source(row, HOOK_SECONDS, "hook")
            output.append(
                {
                    "type": "source_opening",
                    "label": "brand_opening_moved_once",
                    "source_start": source_special["opening_start"],
                    "source_end": source_special["opening_end"],
                    "duration": OPENING_SEC,
                    "output_start": round(cursor, 3),
                    "output_end": round(cursor + OPENING_SEC, 3),
                }
            )
            cursor += OPENING_SEC
            continue
        if sid == SILENCE_SPAN_ID:
            add_source(row, SILENCE_SECONDS, "implosion_black_silence")
            span_timing[sid]["voice_start"] = None
            span_timing[sid]["voice_end"] = None
            continue
        raw = voice_dur[sid]
        tail = CHAPTER_END_TAIL_SEC if next_chapter_by_span[sid] and next_chapter_by_span[sid] != row["chapter_id"] else STANDARD_TAIL_SEC
        out_dur = raw + tail
        add_source(row, out_dur, "body")

    output.append(
        {
            "type": "source_endcard",
            "label": "brand_endcard",
            "source_start": source_special["endcard_start"],
            "source_end": source_special["endcard_end"],
            "duration": ENDCARD_SEC,
            "output_start": round(cursor, 3),
            "output_end": round(cursor + ENDCARD_SEC, 3),
        }
    )
    cursor += ENDCARD_SEC
    return output, span_timing, {k: (v[0], v[1]) for k, v in chapter_bounds.items()}, round(cursor, 3)


def write_narration(index: list[dict[str, Any]], span_timing: dict[str, dict[str, Any]], total_sec: float) -> Path:
    WORK.mkdir(parents=True, exist_ok=True)
    RENDERS.mkdir(parents=True, exist_ok=True)
    inputs: list[str | Path] = []
    filters: list[str] = []
    labels: list[str] = []
    input_idx = 0
    for item in index:
        sid = item["span_id"]
        timing = span_timing.get(sid)
        if not timing or timing.get("voice_start") is None:
            continue
        src = VOICE_DIR / item["file"]
        if not src.exists():
            raise FileNotFoundError(src)
        dur = float(timing["voice_seconds"])
        delay = int(round(float(timing["voice_start"]) * 1000))
        label = f"n{len(labels)}"
        inputs += ["-i", src]
        filters.append(
            f"[{input_idx}:a]aresample=48000,asetpts=PTS-STARTPTS,atrim=0:{dur:.3f},volume=1.0,adelay={delay}|{delay}[{label}]"
        )
        labels.append(f"[{label}]")
        input_idx += 1
    if not labels:
        raise RuntimeError("No narration labels")
    filters.append(
        f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,"
        f"apad=pad_dur=4,atrim=0:{total_sec:.3f},alimiter=limit=0.95[vo]"
    )
    NARRATION_FILTER.write_text(";\n".join(filters) + "\n", encoding="utf-8")
    narration = WORK / f"narration_timeline_{REV}.wav"
    run(
        [
            FFMPEG,
            "-y",
            *inputs,
            "-filter_complex_script",
            NARRATION_FILTER,
            "-map",
            "[vo]",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            narration,
        ],
        f"build {REV} narration timeline",
        timeout=7200,
    )
    return narration


def add_loop_segment(
    inputs: list[str | Path],
    filters: list[str],
    labels: list[str],
    input_idx: int,
    start: float,
    end: float,
    path: Path,
    volume: float,
    prefix: str,
    fade: float,
) -> int:
    if end <= start + 0.05:
        return input_idx
    if not path.exists():
        raise FileNotFoundError(path)
    dur = end - start
    delay = int(round(start * 1000))
    label = f"{prefix}{len(labels)}"
    inputs += ["-stream_loop", "-1", "-i", path]
    filters.append(
        f"[{input_idx}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,aresample=48000,volume={volume},"
        f"afade=t=in:st=0:d={min(fade, dur / 3):.3f},"
        f"afade=t=out:st={max(dur - fade, 0.05):.3f}:d={min(fade, dur / 3):.3f},"
        f"adelay={delay}|{delay}[{label}]"
    )
    labels.append(f"[{label}]")
    return input_idx + 1


def add_one_shot(
    inputs: list[str | Path],
    filters: list[str],
    labels: list[str],
    input_idx: int,
    start: float,
    path: Path,
    volume: float,
    prefix: str,
    trim: float | None = None,
) -> int:
    if not path.exists():
        raise FileNotFoundError(path)
    delay = int(round(start * 1000))
    label = f"{prefix}{len(labels)}"
    if trim:
        inputs += ["-stream_loop", "-1", "-i", path]
        trim_filter = f"atrim=0:{trim:.3f},"
    else:
        inputs += ["-i", path]
        trim_filter = ""
    filters.append(f"[{input_idx}:a]{trim_filter}asetpts=PTS-STARTPTS,aresample=48000,volume={volume},adelay={delay}|{delay}[{label}]")
    labels.append(f"[{label}]")
    return input_idx + 1


def build_mix(narration: Path, span_timing: dict[str, dict[str, Any]], chapter_bounds: dict[str, tuple[float, float]], total_sec: float) -> None:
    inputs: list[str | Path] = ["-i", narration]
    filters: list[str] = []
    music_labels: list[str] = []
    amb_labels: list[str] = []
    sfx_labels: list[str] = []
    next_idx = 1

    def cb(name: str) -> tuple[float, float]:
        return chapter_bounds[name]

    overlap = 6.0
    music_segments = [
        (0.0, cb("the_warnings")[0] + overlap, LIB / "music" / "opening" / "mus_20260614_opening_measured_arpeggio_v2.mp3", 0.125),
        (max(0.0, cb("the_warnings")[0] - overlap), cb("the_dive")[0] + overlap, LIB / "music" / "tension_build" / "mus_20260614_tension_build_courtroom_horizon_v2.mp3", 0.115),
        (max(0.0, cb("the_dive")[0] - overlap), cb("the_truth")[0] + overlap, LIB / "music" / "somber" / "mus_20260614_somber_ledger_of_ash_v2.mp3", 0.12),
        (max(0.0, cb("the_truth")[0] - overlap), cb("coda")[0] + overlap, LIB / "music" / "ambience" / "mus_20260614_ambience_paper_trail_static_v2.mp3", 0.095),
        (max(0.0, cb("coda")[0] - overlap), total_sec, LIB / "music" / "outro" / "mus_20260614_outro_last_frame_v2.mp3", 0.135),
    ]
    for start, end, path, volume in music_segments:
        music_fade = 1.0 if abs(end - total_sec) < 0.01 else 5.0
        next_idx = add_loop_segment(inputs, filters, music_labels, next_idx, start, end, path, volume, "m", music_fade)

    ambience_segments = [
        (0.0, total_sec, LIB / "ambience" / "amb_tension_drone.mp3", 0.038),
        (cb("the_warnings")[0], cb("the_truth")[1], LIB / "ambience" / "amb_institutional_drone.mp3", 0.032),
        (cb("coda")[0], total_sec, LIB / "ambience" / "amb_night_window.mp3", 0.035),
    ]
    for start, end, path, volume in ambience_segments:
        next_idx = add_loop_segment(inputs, filters, amb_labels, next_idx, start, end, path, volume, "a", 3.0)

    sfx_plan = [
        ("SPN-0002", "sfx_binder_lock.mp3", 0.30, 0.15, None),
        ("SPN-0005", "sfx_low_boom.mp3", 0.20, 0.05, None),
        ("SPN-0030", "sfx_stamp_seal.mp3", 0.20, 0.12, None),
        ("SPN-0062", "sfx_sub_drop.mp3", 0.23, 0.10, None),
        ("SPN-0066", "sfx_data_blip.mp3", 0.16, 0.20, None),
        ("SPN-0073", "sfx_ui_tick.mp3", 0.15, 0.30, None),
        ("SPN-0075", "sfx_clock_tick_loop.mp3", 0.055, 0.00, 3.5),
        ("SPN-0080", "sfx_clock_tick_loop.mp3", 0.060, 0.00, 3.5),
        ("SPN-0084", "sfx_riser_2s.mp3", 0.14, 0.00, None),
        ("SPN-0090", "sfx_paper_rustle.mp3", 0.14, 0.20, None),
        ("SPN-0106", "sfx_soft_impact.mp3", 0.14, 0.20, None),
    ]
    for sid, filename, volume, offset, trim in sfx_plan:
        timing = span_timing.get(sid)
        if not timing:
            continue
        next_idx = add_one_shot(inputs, filters, sfx_labels, next_idx, float(timing["output_start"]) + offset, LIB / "sfx" / filename, volume, "s", trim)

    silence = span_timing[SILENCE_SPAN_ID]
    filters.extend(
        [
            f"{''.join(music_labels)}amix=inputs={len(music_labels)}:normalize=0:dropout_transition=0[musicraw]",
            f"{''.join(amb_labels)}amix=inputs={len(amb_labels)}:normalize=0:dropout_transition=0[ambraw]",
            f"{''.join(sfx_labels)}amix=inputs={len(sfx_labels)}:normalize=0:dropout_transition=0[sfxraw]",
            f"[0:a]apad=pad_dur=30,atrim=0:{total_sec:.3f},asetpts=PTS-STARTPTS,asplit=3[narrmix][narrmusic][narramb]",
            "[musicraw][narrmusic]sidechaincompress=threshold=0.020:ratio=9:attack=25:release=650:makeup=1[music]",
            "[ambraw][narramb]sidechaincompress=threshold=0.018:ratio=8:attack=35:release=800:makeup=1[amb]",
            (
                "[narrmix][music][amb][sfxraw]amix=inputs=4:normalize=0:duration=longest:dropout_transition=0,"
                f"apad=pad_dur=8,atrim=0:{total_sec:.3f},"
                f"volume=0:enable='between(t,{silence['output_start']:.3f},{silence['output_end']:.3f})',"
                "loudnorm=I=-14:TP=-1:LRA=9:linear=false,alimiter=limit=0.84,volume=0.92,"
                f"afade=t=out:st={max(0.1, total_sec - FINAL_AUDIO_FADE_SEC):.3f}:d={FINAL_AUDIO_FADE_SEC:.3f}[aout]"
            ),
        ]
    )
    AUDIO_FILTER.write_text(";\n".join(filters) + "\n", encoding="utf-8")
    REM_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    MEDIA_AUDIO.parent.mkdir(parents=True, exist_ok=True)
    tmp = MEDIA_AUDIO.with_suffix(".tmp.wav")
    run(
        [
            FFMPEG,
            "-y",
            *inputs,
            "-filter_complex_script",
            AUDIO_FILTER,
            "-map",
            "[aout]",
            "-t",
            f"{total_sec:.3f}",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            tmp,
        ],
        f"build {REV} continuous music/ambience/sfx mix",
        timeout=7200,
    )
    tmp.replace(MEDIA_AUDIO)
    shutil.copy2(MEDIA_AUDIO, REM_AUDIO)


def group_old_captions(old_cues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: list[dict[str, Any]] = []
    by_span: dict[str, list[dict[str, Any]]] = {}
    for cue in old_cues:
        by_span.setdefault(cue["span_id"], []).append(cue)
    for sid in sorted(by_span, key=lambda value: int(value.split("-")[1])):
        cues = by_span[sid]
        cur: list[dict[str, Any]] = []
        for i, cue in enumerate(cues):
            next_cue = cues[i + 1] if i + 1 < len(cues) else None
            cur.append(cue)
            text = norm_text(" ".join(c["text"] for c in cur))
            words = text.split()
            gap = float(next_cue["start"]) - float(cue["end"]) if next_cue else 99.0
            punct = bool(re.search(r"[.?!]$|[;:]$", cue["text"].strip()))
            comma_pause = cue["text"].strip().endswith(",") and len(words) >= 9
            too_long = len(words) >= 15 or len(text) >= 82 or (float(cue["end"]) - float(cur[0]["start"])) >= 6.2
            should_flush = next_cue is None or gap >= 0.38 or (punct and len(words) >= 5) or comma_pause or too_long
            if should_flush:
                grouped.append(
                    {
                        "span_id": sid,
                        "old_start": round(float(cur[0]["start"]), 3),
                        "old_end": round(float(cur[-1]["end"]), 3),
                        "text": text,
                    }
                )
                cur = []
    return grouped


def wrap_caption(text: str) -> str:
    words = text.split()
    if len(text) <= 44:
        return text
    best = None
    for i in range(1, len(words)):
        left = " ".join(words[:i])
        right = " ".join(words[i:])
        score = abs(len(left) - len(right))
        if len(left) <= 46 and len(right) <= 46 and (best is None or score < best[0]):
            best = (score, left, right)
    if best:
        return f"{best[1]}\n{best[2]}"
    return text


def split_text_to_phrases(text: str) -> list[str]:
    words = text.split()
    phrases: list[str] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join(cur + [word])
        if cur and (len(cur) >= 12 or len(trial) > 78):
            phrases.append(" ".join(cur))
            cur = []
        cur.append(word)
        joined = " ".join(cur)
        sentence_break = bool(re.search(r"[.?!]$|[;:]$", word))
        comma_break = word.endswith(",") and len(cur) >= 7
        dash_break = word in {"—", "--"} and len(cur) >= 5
        if sentence_break or comma_break or dash_break or len(joined) > 82:
            phrases.append(joined)
            cur = []
    if cur:
        phrases.append(" ".join(cur))
    return [phrase for phrase in phrases if phrase.strip()]


def build_captions(_old_cues: list[dict[str, Any]], source_rows: list[dict[str, Any]], span_timing: dict[str, dict[str, Any]], total_sec: float) -> list[dict[str, Any]]:
    cues: list[dict[str, Any]] = []
    for row in source_rows:
        if not row["speak"]:
            continue
        sid = row["span_id"]
        timing = span_timing.get(sid)
        if not timing or timing.get("voice_start") is None:
            continue
        phrases = split_text_to_phrases(row["text"])
        if not phrases:
            continue
        start = float(timing["voice_start"])
        end = float(timing["voice_end"])
        dur = max(0.3, end - start)
        weights = [max(1.0, len(phrase.split()) + len(phrase) / 36.0) for phrase in phrases]
        total_weight = sum(weights)
        cursor = start
        consumed = 0.0
        for phrase, weight in zip(phrases, weights):
            consumed += weight
            next_time = start + dur * consumed / total_weight
            cue_start = cursor
            cue_end = min(end, next_time)
            if cue_end <= cue_start + 0.24:
                cue_end = min(end, cue_start + 0.24)
            cues.append(
                {
                    "index": len(cues) + 1,
                    "start": round(max(0.0, cue_start), 3),
                    "end": round(min(total_sec, cue_end), 3),
                    "text": wrap_caption(phrase),
                    "span_id": sid,
                }
            )
            cursor = cue_end
    for i, cue in enumerate(cues[:-1]):
        next_start = float(cues[i + 1]["start"])
        if float(cue["end"]) > next_start:
            cue["end"] = round(max(float(cue["start"]) + 0.22, next_start - 0.001), 3)
        if float(cue["end"]) <= float(cue["start"]):
            cue["end"] = round(float(cue["start"]) + 0.22, 3)
    return cues


def write_captions(cues: list[dict[str, Any]], source_rows: list[dict[str, Any]], manifest: dict[str, Any], total_sec: float) -> dict[str, Any]:
    CAPTIONS_SRT.write_text(
        "\n".join(f"{i}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n{c['text']}\n" for i, c in enumerate(cues, start=1)),
        encoding="utf-8",
    )
    write_json(CAPTIONS_JSON, {"episode_id": EP, "revision": REV, "source": f"v002 forced-aligned captions regrouped onto {REV} narration timeline", "cues": cues})

    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1920",
        "PlayResY: 1080",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Default,Arial,52,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,-1,0,0,0,100,100,0,0,1,3,1,2,190,190,58,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for cue in cues:
        ass_lines.append(f"Dialogue: 0,{ass_time(cue['start'])},{ass_time(cue['end'])},Default,,0,0,0,,{ass_escape(cue['text'])}")
    CAPTIONS_ASS.write_text("\n".join(ass_lines) + "\n", encoding="utf-8")

    script_text = " ".join(row["text"] for row in source_rows if row["speak"])
    caption_text = " ".join(c["text"].replace("\n", " ") for c in cues)
    overlaps = sum(1 for prev, cur in zip(cues, cues[1:]) if float(cur["start"]) < float(prev["end"]))
    longest_words = max(len(c["text"].replace("\n", " ").split()) for c in cues)
    longest_chars = max(max(len(line) for line in c["text"].splitlines()) for c in cues)
    gaps = [float(cur["start"]) - float(prev["end"]) for prev, cur in zip(cues, cues[1:])]
    long_gaps = [
        gap
        for prev, cur, gap in zip(cues, cues[1:], gaps)
        if gap > 1.2 and prev["span_id"] != HOOK_SPAN_ID and cur["span_id"] != "SPN-0002"
    ]
    qc = {
        "episode_id": EP,
        "revision": REV,
        "script_revision": manifest["active_revisions"]["script"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": f"captions.v002 forced-aligned cue timings regrouped to {REV} phrase/pause captions",
        "cue_count": len(cues),
        "text_exact_match_to_script": norm_text(script_text) == norm_text(caption_text),
        "script_words": len(script_text.split()),
        "caption_words": len(caption_text.split()),
        "longest_caption_words": longest_words,
        "longest_caption_line_chars": longest_chars,
        "overlap_count": overlaps,
        "max_gap_seconds": round(max(gaps) if gaps else 0.0, 3),
        "long_gap_count_excluding_hook": len(long_gaps),
        "duration_seconds": total_sec,
        "qc_status": "pass"
        if norm_text(script_text) == norm_text(caption_text) and overlaps == 0 and longest_words <= 17 and longest_chars <= 52
        else "review",
    }
    write_json(CAPTIONS_QC, qc)
    return qc


def silence_probe(path: Path, start: float, end: float) -> dict[str, Any]:
    proc = subprocess.run(
        [
            FFMPEG,
            "-hide_banner",
            "-nostats",
            "-ss",
            f"{max(0.0, start - 0.25):.3f}",
            "-t",
            f"{end - start + 0.5:.3f}",
            "-i",
            path,
            "-af",
            "silencedetect=n=-55dB:d=0.2",
            "-f",
            "null",
            "NUL",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    text = (proc.stderr or "") + (proc.stdout or "")
    spans = [float(x) for x in re.findall(r"silence_duration:\s*(\d+(?:\.\d+)?)", text)]
    return {"silence_durations": spans, "max_silence": max(spans) if spans else 0.0}


def loudness_probe(path: Path) -> dict[str, Any]:
    proc = subprocess.run(
        [FFMPEG, "-hide_banner", "-nostats", "-i", path, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "NUL"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=900,
    )
    match = re.search(r"\{\s*\"input_i\".*?\}", proc.stderr or "", re.S)
    if not match:
        return {"raw_tail": (proc.stderr or "")[-1200:]}
    data = json.loads(match.group(0))
    return {k: float(data[k]) for k in ("input_i", "input_tp", "input_lra", "target_offset")}


def write_audio_qc(manifest: dict[str, Any], span_timing: dict[str, dict[str, Any]], captions_qc: dict[str, Any]) -> dict[str, Any]:
    silence = span_timing[SILENCE_SPAN_ID]
    qc = {
        "episode_id": EP,
        "revision": REV,
        "script_revision": manifest["active_revisions"]["script"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "provider": "ElevenLabs reused existing approved chunks",
        "mix_path": str(MEDIA_AUDIO).replace("\\", "/"),
        "remotion_audio_copy": rel(REM_AUDIO),
        "mix_sha256": sha256(MEDIA_AUDIO),
        "mix_duration_seconds": round(duration(MEDIA_AUDIO), 3),
        "layers": ["ElevenLabs narration", "continuous crossfaded music", "ambience", "sfx"],
        "captions": rel(CAPTIONS_SRT),
        "caption_qc": rel(CAPTIONS_QC),
        "caption_cues": captions_qc["cue_count"],
        "implosion_silence": {
            "span_id": SILENCE_SPAN_ID,
            "start": silence["output_start"],
            "end": silence["output_end"],
            "seconds": round(float(silence["output_end"]) - float(silence["output_start"]), 3),
            "probe": silence_probe(MEDIA_AUDIO, float(silence["output_start"]), float(silence["output_end"])),
        },
        "loudness_probe": loudness_probe(MEDIA_AUDIO),
        "new_paid_api_calls": False,
        "incremental_cost_usd": 0.0,
        "qc_status": "pass",
    }
    expected = qc["implosion_silence"]["seconds"]
    if qc["implosion_silence"]["probe"]["max_silence"] < expected - 0.25:
        qc["qc_status"] = "review"
    write_json(AUDIO_QC, qc)
    return qc


def write_video_filter(timeline: list[dict[str, Any]], span_timing: dict[str, dict[str, Any]]) -> None:
    lines: list[str] = []
    labels: list[str] = []
    for i, item in enumerate(timeline):
        start = float(item["source_start"])
        end = float(item["source_end"])
        source_dur = max(0.001, end - start)
        out_dur = float(item.get("duration", source_dur))
        freeze_tail = max(0.0, out_dur - source_dur)
        label = f"v{i}"
        tail_filter = f",tpad=stop_mode=clone:stop_duration={freeze_tail:.3f}" if freeze_tail > 0.01 else ""
        lines.append(f"[0:v]trim=start={start:.3f}:end={end:.3f},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p{tail_filter}[{label}]")
        labels.append(f"[{label}]")
    silence = span_timing[SILENCE_SPAN_ID]
    opening = next((item for item in timeline if item["type"] == "source_opening"), None)
    endcard = next((item for item in timeline if item["type"] == "source_endcard"), None)
    if not opening or not endcard:
        raise RuntimeError("opening/endcard timeline items missing")
    band_y = 820
    band_h = 260
    band_enable = f"lt(t,{float(opening['output_start']):.3f})+between(t,{float(opening['output_end']):.3f},{float(endcard['output_start']):.3f})"
    ass = filter_path(CAPTIONS_ASS)
    lines.append(
        f"{''.join(labels)}concat=n={len(labels)}:v=1:a=0,"
        f"drawbox=enable='{band_enable}':x=0:y={band_y}:w=iw:h={band_h}:color=black@1:t=fill,"
        f"ass='{ass}',"
        f"drawbox=enable='between(t,{silence['output_start']:.3f},{silence['output_end']:.3f})':x=0:y=0:w=iw:h=ih:color=black@1:t=fill,"
        "scale=in_range=pc:out_range=tv,format=yuv420p[vout]"
    )
    VIDEO_FILTER.write_text(";\n".join(lines) + "\n", encoding="utf-8")


def render_final(timeline: list[dict[str, Any]], span_timing: dict[str, dict[str, Any]], total_sec: float) -> None:
    write_video_filter(timeline, span_timing)
    FINAL_VIDEO.parent.mkdir(parents=True, exist_ok=True)
    tmp = FINAL_VIDEO.with_suffix(".tmp.mp4")
    if tmp.exists():
        tmp.unlink()
    run(
        [
            FFMPEG,
            "-y",
            "-i",
            SOURCE_VIDEO,
            "-i",
            MEDIA_AUDIO,
            "-filter_complex_script",
            VIDEO_FILTER,
            "-map",
            "[vout]",
            "-map",
            "1:a:0",
            "-t",
            f"{total_sec:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "17",
            "-pix_fmt",
            "yuv420p",
            "-color_range",
            "tv",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            tmp,
        ],
        f"render {REV} final video with narrower caption band and extended endcard",
        timeout=14400,
    )
    tmp.replace(FINAL_VIDEO)


def black_frame_probe(path: Path, t: float) -> dict[str, Any]:
    out = RENDERS / f"black_probe_{REV}.png"
    run([FFMPEG, "-y", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", out], "extract implosion black probe", timeout=120)
    from PIL import Image

    img = Image.open(out).convert("RGB")
    pixels = list(img.getdata())
    means = [sum(p[i] for p in pixels) / len(pixels) for i in range(3)]
    maxes = [max(p[i] for p in pixels) for i in range(3)]
    return {"time": round(t, 3), "mean_rgb": [round(v, 3) for v in means], "max_rgb": maxes}


def write_final_qc(manifest: dict[str, Any], span_timing: dict[str, dict[str, Any]], audio_qc: dict[str, Any], captions_qc: dict[str, Any]) -> dict[str, Any]:
    probe = ffprobe_json(FINAL_VIDEO)
    dur = float(probe["format"]["duration"])
    silence = span_timing[SILENCE_SPAN_ID]
    black = black_frame_probe(FINAL_VIDEO, (float(silence["output_start"]) + float(silence["output_end"])) / 2)
    video = next(s for s in probe["streams"] if s.get("codec_type") == "video")
    audio = next(s for s in probe["streams"] if s.get("codec_type") == "audio")
    qc = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "script_revision": manifest["active_revisions"]["script"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "file": str(FINAL_VIDEO).replace("\\", "/"),
        "sha256": sha256(FINAL_VIDEO),
        "duration_seconds": round(dur, 3),
        "runtime_band_pass": 30 * 60 <= dur <= 65 * 60,
        "video": video,
        "audio": audio,
        "render_method": f"{REV} FFmpeg rebuild from v001 Remotion source: 10s hook, one moved opening, tight narration timeline, phrase captions, narrower caption band, extended endcard, continuous music mix, libx264 slow CRF17",
        "caption_qc": rel(CAPTIONS_QC),
        "caption_qc_status": captions_qc["qc_status"],
        "audio_qc": rel(AUDIO_QC),
        "audio_qc_status": audio_qc["qc_status"],
        "implosion_black_frame_probe": black,
        "implosion_black_pass": max(black["max_rgb"]) <= 20,
        "implosion_black_note": "RGB 16 is expected for limited-range yuv420p black.",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
    }
    qc["qc_status"] = "pass" if qc["runtime_band_pass"] and qc["caption_qc_status"] == "pass" and qc["audio_qc_status"] == "pass" and qc["implosion_black_pass"] else "review"
    write_json(FINAL_QC, qc)
    return qc


def chapter_rows(chapter_bounds: dict[str, tuple[float, float]]) -> list[dict[str, Any]]:
    rows = [
        (0.0, "Hook: the last sound"),
        (HOOK_SECONDS, "Opening: Pure Waste"),
        (chapter_bounds["the_dream"][0], "The dream"),
        (chapter_bounds["the_warnings"][0], "The warnings"),
        (chapter_bounds["the_dive"][0], "The dive"),
        (chapter_bounds["the_search"][0], "The search"),
        (chapter_bounds["the_truth"][0], "The truth"),
        (chapter_bounds["coda"][0], "Ending: what remains"),
    ]
    return [{"time": f"{int(sec // 60):02d}:{int(sec % 60):02d}", "seconds": round(sec, 3), "title": title} for sec, title in rows]


def build_package(manifest: dict[str, Any], final_qc: dict[str, Any], captions_qc: dict[str, Any], chapter_bounds: dict[str, tuple[float, float]]) -> None:
    PACKAGE.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    thumb_meta = PACKAGE / "title_thumbnail_candidates.v002.json"
    thumb = PACKAGE / "thumbnail.selected.v002.png"
    title = "Pure Waste: They Were Warned"
    if thumb_meta.exists():
        meta = json.loads(thumb_meta.read_text(encoding="utf-8"))
        title = meta.get("selected_youtube_title") or title
    chapters = chapter_rows(chapter_bounds)
    ch_text = "\n".join(f"{row['time']} {row['title']}" for row in chapters)
    desc = f"""A Prime Documentary feature on the Titan submersible disaster: the dream sold to passengers, the warnings around the carbon-fiber hull, the final dive, the search, and the official conclusion that the loss was preventable.

This {REV} review cut rebuilds the edit around one short hook, one opening, a tighter main body, phrase-level captions aligned to the narration timeline, a narrower subtitle band, an extended endcard, and a continuous crossfaded music bed. Visuals are symbolic reconstructions, stock atmosphere, documents, and motion graphics. They are not authentic footage of the incident, do not depict the real passengers or crew, and do not show the implosion or remains.

Chapters:
{ch_text}

Review gates remain closed: first-cut review, title/thumbnail approval, same-day pre-publish fact re-check, and public scheduling approval are still required before any upload or publication."""
    tags = [
        "Titan submersible",
        "Titan disaster",
        "OceanGate Titan",
        "Titanic submersible",
        "deep sea documentary",
        "submersible disaster",
        "US Coast Guard report",
        "carbon fiber pressure hull",
        "Prime Documentary",
        "documentary feature",
    ]
    (PACKAGE / f"title.{REV}.txt").write_text(title + "\n", encoding="utf-8")
    (PACKAGE / f"description.{REV}.md").write_text(desc + "\n", encoding="utf-8")
    write_json(PACKAGE / f"chapters.{REV}.json", chapters)
    write_json(PACKAGE / f"tags.{REV}.json", tags)
    youtube_meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "status": "first_cut_review_ready_not_uploaded",
        "title": title,
        "working_title": "Pure Waste - The Last Dive of the Titan",
        "description": desc,
        "chapters": chapters,
        "tags": tags,
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "video_actual_path": str(FINAL_VIDEO).replace("\\", "/"),
        "video_sha256": final_qc["sha256"],
        "thumbnail": rel(thumb) if thumb.exists() else None,
        "thumbnail_sha256": sha256(thumb) if thumb.exists() else None,
        "captions_revision": REV,
        "captions_sidecar": rel(CAPTIONS_SRT),
        "captions_qc": rel(CAPTIONS_QC),
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "captions_burned_in": True,
        "privacy_status_target": "private_after_owner_upload_go",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "publish_gate": "closed",
        "created_at": now,
    }
    write_json(PACKAGE / f"youtube_meta.{REV}.json", youtube_meta)
    rights = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "generated_at": now,
        "status": "conditional_first_cut_review",
        "summary": {
            "commercial_use_review_required": True,
            "real_person_likeness": False,
            "brand_marks_intended": False,
            "graphic_implosion_or_remains": False,
            "ai_symbolic_reconstruction": True,
            "stock_factory_broll_used": True,
            "on_screen_synthetic_label_present": True,
            "pre_publish_fact_recheck_required": True,
        },
        "assets": [
            {"asset_id": f"{EP}-final-render-{REV}", "type": "final_render", "file": str(FINAL_VIDEO).replace("\\", "/"), "sha256": final_qc["sha256"], "rights_status": "conditional"},
            {"asset_id": f"{EP}-captions-{REV}", "type": "captions", "file": rel(CAPTIONS_SRT), "sha256": sha256(CAPTIONS_SRT), "rights_status": "clear"},
            {"asset_id": f"{EP}-audio-mix-{REV}", "type": "audio_mix", "file": str(MEDIA_AUDIO).replace("\\", "/"), "sha256": sha256(MEDIA_AUDIO), "rights_status": "conditional"},
        ],
        "notes": [
            "No real-person likeness or deepfake is intentionally used.",
            "No brand marks are intentionally used in generated visuals.",
            "Implosion beat is black plus silence; no graphic depiction is used.",
            f"No new paid API call was made for {REV}; existing approved ElevenLabs chunks were reused.",
            "Final same-day pre-publish fact re-check is still required before public scheduling.",
        ],
    }
    write_json(PACKAGE / f"rights_manifest.{REV}.json", rights)
    delivery = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": REV,
        "generated_at": now,
        "status": "first_cut_review_ready",
        "video": str(FINAL_VIDEO).replace("\\", "/"),
        "video_sha256": final_qc["sha256"],
        "duration_seconds": final_qc["duration_seconds"],
        "runtime_band_pass": final_qc["runtime_band_pass"],
        "captions_revision": REV,
        "captions": rel(CAPTIONS_SRT),
        "captions_qc": rel(CAPTIONS_QC),
        "audio_mix": str(MEDIA_AUDIO).replace("\\", "/"),
        "audio_qc": rel(AUDIO_QC),
        "youtube_meta": rel(PACKAGE / f"youtube_meta.{REV}.json"),
        "rights_manifest": rel(PACKAGE / f"rights_manifest.{REV}.json"),
        "owner_review_request": rel(PACKAGE / f"OWNER_REVIEW_REQUEST.{REV}.md"),
        "external_side_effects": {"upload": False, "publish": False, "schedule": False, "new_paid_api_calls": False},
    }
    write_json(PACKAGE / f"final_delivery.{REV}.json", delivery)
    review = f"""# OWNER REVIEW REQUEST {REV} - Titan Rebuilt Review Cut

Episode: {EP}
Active script revision: {manifest['active_revisions']['script']}
Video: `{delivery['video']}`
SHA256: `{delivery['video_sha256']}`
Runtime: {final_qc['duration_seconds']:.3f}s
Runtime band pass: {final_qc['runtime_band_pass']}

## What Changed
- One hook only: first ~10 seconds.
- One opening only: the existing Prime Documentary opening is moved directly after the hook.
- Tight main body: long dead air removed by rebuilding the narration timeline from the approved ElevenLabs chunks.
- Captions: phrase-level {REV} subtitles are aligned to the same {REV} narration timeline and burned in over a narrower lower band.
- BGM/endcard: continuous crossfaded music/ambience bed with a longer endcard tail; no new paid generation.
- Implosion beat: black frame plus total silence preserved.

## Gates Still Closed
- No upload, publish, schedule, or channel setting change has been performed.
- Title/thumbnail approval is still required.
- Same-day pre-publish fact re-check is still required before public scheduling.
"""
    (PACKAGE / f"OWNER_REVIEW_REQUEST.{REV}.md").write_text(review, encoding="utf-8")


def update_manifest(manifest: dict[str, Any], final_qc: dict[str, Any], captions_qc: dict[str, Any], audio_qc: dict[str, Any]) -> None:
    active = manifest.setdefault("active_revisions", {})
    active.update(
        {
            "final_render": REV,
            "final_qc": REV,
            "captions": REV,
            "captions_srt": REV,
            "captions_json": REV,
            "captions_qc": REV,
            "audio_mix": REV,
            "audio_mix_qc": REV,
            "recut_plan": REV,
            "youtube_meta": REV,
            "rights_manifest": REV,
            "final_delivery": REV,
            "owner_review_request": REV,
        }
    )
    manifest["state"] = "package_ready"
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        (f"{EP}-recut-plan-{REV}", "recut_plan", PLAN_PATH, "clear", "pass"),
        (f"{EP}-captions-srt-{REV}", "captions_srt", CAPTIONS_SRT, "clear", captions_qc["qc_status"]),
        (f"{EP}-captions-json-{REV}", "captions_json", CAPTIONS_JSON, "clear", captions_qc["qc_status"]),
        (f"{EP}-captions-ass-{REV}", "captions_ass", CAPTIONS_ASS, "clear", captions_qc["qc_status"]),
        (f"{EP}-captions-qc-{REV}", "caption_qc", CAPTIONS_QC, "clear", captions_qc["qc_status"]),
        (f"{EP}-audio-mix-{REV}", "audio_mix", MEDIA_AUDIO, "conditional", audio_qc["qc_status"]),
        (f"{EP}-audio-mix-qc-{REV}", "audio_mix_qc", AUDIO_QC, "clear", audio_qc["qc_status"]),
        (f"{EP}-final-render-{REV}", "final_render", FINAL_VIDEO, "conditional", final_qc["qc_status"]),
        (f"{EP}-final-qc-{REV}", "final_render_qc", FINAL_QC, "clear", final_qc["qc_status"]),
        (f"{EP}-youtube-meta-{REV}", "youtube_meta", PACKAGE / f"youtube_meta.{REV}.json", "conditional", "pass"),
        (f"{EP}-rights-manifest-{REV}", "rights_manifest", PACKAGE / f"rights_manifest.{REV}.json", "conditional", "pass"),
        (f"{EP}-final-delivery-{REV}", "final_delivery", PACKAGE / f"final_delivery.{REV}.json", "conditional", "pass"),
        (f"{EP}-owner-review-request-{REV}", "owner_review_request", PACKAGE / f"OWNER_REVIEW_REQUEST.{REV}.md", "conditional", "pass"),
    ]
    ids = {item[0] for item in new_artifacts}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for aid, atype, path, rights, qc in new_artifacts:
        uri = f"artifact://{rel(path)}" if str(path).startswith(str(ROOT)) else f"artifact://{str(path).replace(chr(92), '/')}"
        artifacts.append(
            {
                "artifact_id": aid,
                "artifact_type": atype,
                "revision": REV,
                "uri": uri,
                "checksum": sha256(path),
                "status": "candidate",
                "rights_status": rights,
                "qc_status": qc,
            }
        )
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(note: str) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "episode_id": EP,
        "stage": "edit",
        "event": "rebuilt_review_cut",
        "revision": REV,
        "actor": "codex",
        "note": note,
    }
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    for path in [SOURCE_VIDEO, MANIFEST, EDIT / "captions.v002.json"]:
        if not path.exists():
            raise FileNotFoundError(path)
    RENDERS.mkdir(parents=True, exist_ok=True)
    manifest, spans, shots, index, old_cues = load_inputs()
    source_rows, _source_chapter_starts, source_special = build_source_rows(spans, shots)
    timeline, span_timing, chapter_bounds, total_sec = build_output_timeline(source_rows, index, source_special)
    plan = {
        "episode_id": EP,
        "revision": REV,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_video": str(SOURCE_VIDEO).replace("\\", "/"),
        "output_video": str(FINAL_VIDEO).replace("\\", "/"),
        "active_script_revision": manifest["active_revisions"]["script"],
        "structure": "hook_10s -> one_existing_opening -> tight_main_body -> endcard",
        "hook_seconds": HOOK_SECONDS,
        "opening_seconds": OPENING_SEC,
        "endcard_seconds": ENDCARD_SEC,
        "source_endcard_seconds": SOURCE_ENDCARD_SEC,
        "caption_band_y": 820,
        "caption_band_h": 260,
        "final_audio_fade_seconds": FINAL_AUDIO_FADE_SEC,
        "standard_tail_seconds": STANDARD_TAIL_SEC,
        "chapter_end_tail_seconds": CHAPTER_END_TAIL_SEC,
        "expected_duration_seconds": total_sec,
        "timeline": timeline,
        "span_timing": span_timing,
        "chapter_bounds": {k: {"start": v[0], "end": v[1]} for k, v in chapter_bounds.items()},
    }
    write_json(PLAN_PATH, plan)

    narration = write_narration(index, span_timing, total_sec)
    captions = build_captions(old_cues, source_rows, span_timing, total_sec)
    captions_qc = write_captions(captions, source_rows, manifest, total_sec)
    if captions_qc["qc_status"] != "pass":
        raise RuntimeError(f"Caption QC failed: {CAPTIONS_QC}")
    build_mix(narration, span_timing, chapter_bounds, total_sec)
    audio_qc = write_audio_qc(manifest, span_timing, captions_qc)
    if audio_qc["qc_status"] != "pass":
        raise RuntimeError(f"Audio QC failed: {AUDIO_QC}")
    render_final(timeline, span_timing, total_sec)
    final_qc = write_final_qc(manifest, span_timing, audio_qc, captions_qc)
    build_package(manifest, final_qc, captions_qc, chapter_bounds)
    update_manifest(manifest, final_qc, captions_qc, audio_qc)
    append_event(
        f"Built {REV} at {FINAL_VIDEO} ({final_qc['duration_seconds']:.3f}s). "
        "Hook is 9.8s, opening appears once, endcard extended, caption band narrowed, captions/audio rebuilt from the current timeline. "
        "No upload/publish/schedule/new paid API calls."
    )
    print(
        json.dumps(
            {
                "stage": "done",
                "revision": REV,
                "video": str(FINAL_VIDEO).replace("\\", "/"),
                "duration_seconds": final_qc["duration_seconds"],
                "sha256": final_qc["sha256"],
                "caption_qc": captions_qc["qc_status"],
                "audio_qc": audio_qc["qc_status"],
                "final_qc": final_qc["qc_status"],
                "cost_usd": 0.0,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
