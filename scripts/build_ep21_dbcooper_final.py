#!/usr/bin/env python3
"""Build EP21 D.B. Cooper final local edit.

This is intentionally idempotent for paid voice chunks: if a chunk ledger and
MP3 already exist with the same request hash, no ElevenLabs request is made.
It performs no upload or publish action.
"""
from __future__ import annotations

import hashlib
import argparse
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from factory_themes import theme_of  # noqa: E402

EP = "PD-2026-021-dbcooper"
EP_NUM = 21
EPDIR = ROOT / "episodes" / EP
MEDIA = Path("E:/pd-media")
EP_MEDIA = MEDIA / "episodes" / EP
LIB = MEDIA / "library"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
MODEL_ID = "eleven_multilingual_v2"
VOICE_REV = "v001"
AUDIO_REV = "v001"
VIDEO_REV = "v001"
FPS = 30
W, H = 1920, 1080
PANEL_W, PANEL_H = 3840, 2160
WORK = EP_MEDIA / "08_edit" / "_build_v001"
VISUALS = EP_MEDIA / "05_visuals"
SELECTED = VISUALS / "selected"
PUBLIC = ROOT / "remotion" / "public" / "dbcooper"
FACTORY = PUBLIC / "factory"
BOOKEND_BG = ROOT / "remotion" / "public" / "banner_sunrise.png"
PD_LOGO = ROOT / "remotion" / "public" / "pd_logo.png"
MASTER_DIR = EP_MEDIA / "06_audio" / f"master_elevenlabs_{VOICE_REV}"
RAW_DIR = MASTER_DIR / "raw_mp3"
WAV_DIR = MASTER_DIR / "wav"
LEDGER_DIR = MASTER_DIR / "request_ledger"
VOICE_MASTER = MASTER_DIR / f"voice_master.{VOICE_REV}.wav"
MIX_WAV = EP_MEDIA / "08_edit" / f"dbcooper_final_mix.{AUDIO_REV}.wav"
SILENT_MP4 = WORK / f"dbcooper_silent_motion.{VIDEO_REV}.mp4"
FINAL_MP4 = EP_MEDIA / "08_edit" / "final.mp4"
NARRATION_INDEX = EPDIR / "06_audio" / f"narration_index.{AUDIO_REV}.json"
VOICE_META = EPDIR / "06_audio" / f"voice_master.{VOICE_REV}.json"
CAPTIONS_SRT = EPDIR / "08_edit" / f"captions.{AUDIO_REV}.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / f"captions.{AUDIO_REV}.json"
DELIVERY = EPDIR / "09_package" / f"final_delivery.{VIDEO_REV}.json"
RIGHTS = EPDIR / "09_package" / "rights_manifest.v001.json"
ACCEPTANCE = EPDIR / "09_package" / "acceptance_report.v001.json"
EVENTS = EPDIR / "events" / "events.jsonl"
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
ELEVEN_EST_USD_PER_CHAR = float(os.environ.get("ELEVENLABS_EST_USD_PER_CHAR", "0.0003"))
ELEVEN_HARD_BUDGET_USD = 25.0
HERO_IMAGE_COUNT = 46
BASE_PAUSE_SECONDS = 4.85
CHAPTER_PAUSE_SECONDS = 5.60
CHAPTER_BREAK_AFTER_INDICES = {0, 8, 22, 39, 52, 59}
CAPTION_MAX_LINE_CHARS = 42
CAPTION_TARGET_LINE_CHARS = 34
CAPTION_MAX_GROUP_CHARS = 82
CAPTION_BAD_LINE_STARTS = {
    "and",
    "or",
    "but",
    "because",
    "while",
    "with",
    "without",
    "to",
    "of",
    "in",
    "on",
    "at",
    "by",
    "for",
    "from",
    "into",
    "over",
    "under",
    "through",
    "that",
    "which",
    "who",
}
CAPTION_BAD_LINE_ENDS = CAPTION_BAD_LINE_STARTS | {"a", "an", "the"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(cmd: list[str | Path], label: str, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    print(f"== {label}", flush=True)
    return subprocess.run([str(x) for x in cmd], text=True, check=True, timeout=timeout)


def capture(cmd: list[str | Path], timeout: int | None = None) -> str:
    result = subprocess.run([str(x) for x in cmd], capture_output=True, text=True, check=True, timeout=timeout)
    return result.stdout


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return "sha256:" + h.hexdigest()


def load_dotenv() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def ffprobe_duration(path: Path) -> float:
    out = capture([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.strip())


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/impact.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
    ]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def safe_slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", text).strip("_")


def parse_vo() -> list[dict[str, Any]]:
    script = EPDIR / "03_script" / "script.en.v001.md"
    rows: list[dict[str, Any]] = []
    for line in script.read_text(encoding="utf-8").splitlines():
        if not line.startswith("[VO:]"):
            continue
        text = line[len("[VO:]") :].strip()
        text = re.sub(r"\s*\[CLM-\d+\]", "", text).strip()
        rows.append({"span_id": f"SPN-{len(rows)+1:04d}", "text": re.sub(r"\s+", " ", text)})
    if len(rows) != 61:
        raise RuntimeError(f"expected 61 VO rows, got {len(rows)}")
    return rows


def estimate_budget(rows: list[dict[str, Any]]) -> dict[str, Any]:
    chars = sum(len(r["text"]) for r in rows)
    usd = round(chars * ELEVEN_EST_USD_PER_CHAR, 2)
    if usd > ELEVEN_HARD_BUDGET_USD:
        raise RuntimeError(f"ElevenLabs estimate ${usd} exceeds hard budget ${ELEVEN_HARD_BUDGET_USD}")
    return {"characters": chars, "estimated_usd": usd, "hard_budget_usd": ELEVEN_HARD_BUDGET_USD}


def request_hash(row: dict[str, Any]) -> str:
    body = {
        "voice_id": VOICE_ID,
        "model_id": MODEL_ID,
        "text": row["text"],
        "voice_settings": {
            "stability": 0.35,
            "similarity_boost": 0.80,
            "style": 0,
            "use_speaker_boost": True,
        },
    }
    return sha256_bytes(json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def raw_path(row: dict[str, Any]) -> Path:
    return RAW_DIR / f"{row['span_id']}.mp3"


def wav_path(row: dict[str, Any]) -> Path:
    return WAV_DIR / f"{row['span_id']}.wav"


def ledger_path(row: dict[str, Any]) -> Path:
    return LEDGER_DIR / f"{row['span_id']}.json"


def chunk_completed(row: dict[str, Any], req_hash: str) -> bool:
    lp = ledger_path(row)
    rp = raw_path(row)
    if not lp.exists() or not rp.exists() or rp.stat().st_size < 512:
        return False
    try:
        data = json.loads(lp.read_text(encoding="utf-8"))
    except Exception:
        return False
    return data.get("status") == "ok" and data.get("request_hash") == req_hash


def guard_unknown(row: dict[str, Any], req_hash: str) -> None:
    lp = ledger_path(row)
    if not lp.exists() or raw_path(row).exists():
        return
    try:
        data = json.loads(lp.read_text(encoding="utf-8"))
    except Exception:
        return
    if data.get("request_hash") == req_hash and data.get("status") in {"started", "unknown"}:
        raise RuntimeError(f"{row['span_id']} has a prior unknown ElevenLabs request; refusing duplicate paid call")


def synthesize_chunk(row: dict[str, Any], api_key: str) -> dict[str, Any]:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    req_hash = request_hash(row)
    if chunk_completed(row, req_hash):
        data = json.loads(ledger_path(row).read_text(encoding="utf-8"))
        data["skipped_existing"] = True
        return data
    guard_unknown(row, req_hash)
    idem = f"pd-2026-021-dbcooper-{VOICE_REV}-{row['span_id']}-{req_hash[:16]}"
    started = {
        "episode_id": EP,
        "span_id": row["span_id"],
        "revision": VOICE_REV,
        "provider": "elevenlabs",
        "model_id": MODEL_ID,
        "voice_id": VOICE_ID,
        "request_hash": req_hash,
        "idempotency_key": idem,
        "text_sha256": sha256_bytes(row["text"].encode("utf-8")),
        "text_characters": len(row["text"]),
        "status": "started",
        "started_at": now(),
    }
    ledger_path(row).write_text(json.dumps(started, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    body = json.dumps(
        {
            "text": row["text"],
            "model_id": MODEL_ID,
            "voice_settings": {
                "stability": 0.35,
                "similarity_boost": 0.80,
                "style": 0,
                "use_speaker_boost": True,
            },
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_128",
        data=body,
        method="POST",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
            "Idempotency-Key": idem,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            audio = response.read()
            status_code = response.status
            headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        detail = exc.read(2000).decode("utf-8", errors="replace")
        failed = {**started, "status": "failed", "failed_at": now(), "http_status": exc.code, "error": detail}
        ledger_path(row).write_text(json.dumps(failed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        raise RuntimeError(f"ElevenLabs HTTP {exc.code} for {row['span_id']}: {detail}") from exc
    except Exception as exc:
        unknown = {**started, "status": "unknown", "failed_at": now(), "error": repr(exc)}
        ledger_path(row).write_text(json.dumps(unknown, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        raise
    tmp = raw_path(row).with_suffix(".part")
    tmp.write_bytes(audio)
    tmp.replace(raw_path(row))
    safe_headers = {
        k: v
        for k, v in headers.items()
        if k.lower() in {"request-id", "x-request-id", "history-item-id", "content-type", "content-length"}
    }
    ok = {
        **started,
        "status": "ok",
        "completed_at": now(),
        "http_status": status_code,
        "response_headers": safe_headers,
        "audio_file": str(raw_path(row)).replace("\\", "/"),
        "audio_sha256": sha256_file(raw_path(row)),
    }
    ledger_path(row).write_text(json.dumps(ok, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    time.sleep(0.25)
    return ok


def build_voice(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    load_dotenv()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is not set")
    budget = estimate_budget(rows)
    print(f"== ElevenLabs budget estimate: ${budget['estimated_usd']} / ${ELEVEN_HARD_BUDGET_USD}", flush=True)
    chunk_meta = []
    for row in rows:
        chunk_meta.append(synthesize_chunk(row, api_key))

    WAV_DIR.mkdir(parents=True, exist_ok=True)
    concat = WORK / "voice_concat.txt"
    concat.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    timed = []
    cursor = 0.0
    for i, row in enumerate(rows):
        wav = wav_path(row)
        if not wav.exists() or wav.stat().st_size < 1000:
            run(
                [
                    FFMPEG,
                    "-y",
                    "-i",
                    raw_path(row),
                    "-af",
                    "aresample=48000,alimiter=limit=0.92",
                    "-ar",
                    "48000",
                    "-ac",
                    "2",
                    "-c:a",
                    "pcm_s16le",
                    wav,
                ],
                f"convert {row['span_id']} to wav",
            )
        dur = ffprobe_duration(wav)
        pause = BASE_PAUSE_SECONDS
        if i in CHAPTER_BREAK_AFTER_INDICES:
            pause = CHAPTER_PAUSE_SECONDS
        timed.append({**row, "voice_start": round(cursor, 3), "voice_end": round(cursor + dur, 3), "raw_seconds": round(dur, 3), "file": str(wav)})
        lines.append(f"file '{wav.as_posix()}'\n")
        cursor += dur
        if i < len(rows) - 1:
            silence = WAV_DIR / f"_pause_{i+1:03d}_{int(pause*1000)}ms.wav"
            if not silence.exists():
                run(
                    [
                        FFMPEG,
                        "-y",
                        "-f",
                        "lavfi",
                        "-i",
                        "anullsrc=r=48000:cl=stereo",
                        "-t",
                        f"{pause:.3f}",
                        "-c:a",
                        "pcm_s16le",
                        silence,
                    ],
                    f"make pause {i+1}",
                )
            lines.append(f"file '{silence.as_posix()}'\n")
            cursor += pause
    tail = WAV_DIR / "_tail_endcard_9s.wav"
    if not tail.exists():
        run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "9.0", "-c:a", "pcm_s16le", tail], "make endcard tail")
    lines.append(f"file '{tail.as_posix()}'\n")
    concat.write_text("".join(lines), encoding="utf-8")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c:a", "pcm_s16le", VOICE_MASTER], "concat ElevenLabs voice", timeout=7200)
    total = ffprobe_duration(VOICE_MASTER)
    EPDIR.joinpath("06_audio").mkdir(exist_ok=True)
    meta = {
        "episode_id": EP,
        "revision": VOICE_REV,
        "provider": "elevenlabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL_ID,
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80, "style": 0, "use_speaker_boost": True},
        "budget": budget,
        "master_wav": str(VOICE_MASTER).replace("\\", "/"),
        "duration_seconds": round(total, 3),
        "chunks": chunk_meta,
        "created_at": now(),
    }
    VOICE_META.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    NARRATION_INDEX.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": AUDIO_REV,
                "provider": "elevenlabs",
                "voice_id": VOICE_ID,
                "model_id": MODEL_ID,
                "master_wav": str(VOICE_MASTER).replace("\\", "/"),
                "duration_seconds": round(total, 3),
                "chunks": timed,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return timed


def srt_ts(t: float) -> str:
    ms = max(0, int(round(t * 1000)))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def caption_word_key(word: str) -> str:
    return re.sub(r"[^A-Za-z0-9']+", "", word).lower()


def can_wrap_caption_words(words: list[str]) -> bool:
    joined = " ".join(words)
    if len(joined) <= CAPTION_MAX_LINE_CHARS:
        return True
    return any(
        len(" ".join(words[:i])) <= CAPTION_MAX_LINE_CHARS
        and len(" ".join(words[i:])) <= CAPTION_MAX_LINE_CHARS
        for i in range(1, len(words))
    )


def caption_text_len(words: list[str]) -> int:
    return len(" ".join(words))


def rebalance_caption_groups(groups: list[list[str]]) -> list[list[str]]:
    balanced = [g[:] for g in groups if g]
    for i in range(len(balanced) - 1):
        end_key = caption_word_key(balanced[i][-1])
        if end_key not in CAPTION_BAD_LINE_ENDS and end_key != "one":
            continue
        best: tuple[float, list[str], list[str]] | None = None
        start_k = max(1, len(balanced[i]) - 9)
        for k in range(start_k, len(balanced[i])):
            left = balanced[i][:k]
            moved_tail = balanced[i][k:]
            right = moved_tail + balanced[i + 1]
            if caption_text_len(left) < 24 or caption_text_len(right) < 18:
                continue
            if caption_text_len(left) > CAPTION_MAX_GROUP_CHARS or caption_text_len(right) > CAPTION_MAX_GROUP_CHARS:
                continue
            if not can_wrap_caption_words(left) or not can_wrap_caption_words(right):
                continue
            left_end = caption_word_key(left[-1])
            right_start = caption_word_key(right[0])
            if left_end in CAPTION_BAD_LINE_ENDS or left_end == "one":
                continue
            score = abs(caption_text_len(left) - caption_text_len(right))
            score += abs(len(moved_tail) - 5) * 4
            if right_start in CAPTION_BAD_LINE_STARTS:
                score += 12
            candidate = (score, left, right)
            if best is None or candidate[0] < best[0]:
                best = candidate
        if best is not None:
            _, balanced[i], balanced[i + 1] = best
    return balanced


def wrap_caption(words: list[str]) -> str:
    joined = " ".join(words)
    if len(joined) <= CAPTION_MAX_LINE_CHARS:
        return joined
    candidates: list[tuple[float, str, str]] = []
    for i in range(1, len(words)):
        left = " ".join(words[:i])
        right = " ".join(words[i:])
        if len(left) > CAPTION_MAX_LINE_CHARS or len(right) > CAPTION_MAX_LINE_CHARS:
            continue
        left_key = caption_word_key(words[i - 1])
        right_key = caption_word_key(words[i])
        score = abs(len(left) - len(right)) * 1.4
        score += abs(len(left) - CAPTION_TARGET_LINE_CHARS) * 0.25
        score += abs(len(right) - CAPTION_TARGET_LINE_CHARS) * 0.25
        if left_key in CAPTION_BAD_LINE_ENDS:
            score += 8
        if right_key in CAPTION_BAD_LINE_STARTS:
            score += 12
        if len(left) < 16 or len(right) < 16:
            score += 10
        if re.search(r"[,;:]$", words[i - 1]):
            score -= 3
        candidates.append((score, left, right))
    if candidates:
        _, left, right = min(candidates, key=lambda item: item[0])
        return left + "\n" + right

    lines: list[str] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join(cur + [word])
        if cur and len(trial) > CAPTION_MAX_LINE_CHARS:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))
    if len(lines) <= 2:
        return "\n".join(lines)
    raise RuntimeError(f"caption group cannot fit in two lines: {' '.join(words)}")


def split_caption_text(text: str) -> list[str]:
    words = text.split()
    groups: list[list[str]] = []
    cur: list[str] = []
    for word in words:
        candidate = cur + [word]
        trial = " ".join(candidate)
        hard_long = cur and (len(trial) > CAPTION_MAX_GROUP_CHARS or not can_wrap_caption_words(candidate))
        soft_long = cur and len(trial) > 54 and re.search(r"[,;:]$", cur[-1])
        if hard_long or soft_long:
            groups.append(cur)
            cur = []
        cur.append(word)
        phrase = " ".join(cur)
        strong_stop = re.search(r"[.?!]([\"”’')\]]*)$", word) and len(phrase) >= 16
        medium_stop = re.search(r"[,;:]([\"”’')\]]*)$", word) and len(phrase) >= 30
        dash_stop = word.endswith("—") and len(phrase) >= 24
        if strong_stop or medium_stop or dash_stop or len(phrase) >= CAPTION_MAX_GROUP_CHARS:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return [wrap_caption(g) for g in rebalance_caption_groups(groups)]


def merge_short_caption_groups(parts: list[str], available: float) -> list[str]:
    """Avoid twitchy flashes while preserving exact VO word order."""
    if not parts or available <= 0:
        return parts
    groups = parts[:]
    while len(groups) > 1:
        weights = [max(1, len(g.replace("\n", " "))) for g in groups]
        total_weight = sum(weights)
        durations = [available * w / total_weight for w in weights]
        short = [i for i, dur in enumerate(durations) if dur < 0.85]
        if not short:
            break
        i = short[0]
        candidates: list[tuple[int, int]] = []
        if i > 0:
            candidates.append((i - 1, i))
        if i < len(groups) - 1:
            candidates.append((i, i + 1))
        candidates.sort(key=lambda pair: durations[pair[0]] + durations[pair[1]])
        merged: str | None = None
        merge_span: tuple[int, int] | None = None
        for lo, hi in candidates:
            merged_words = (groups[lo].replace("\n", " ") + " " + groups[hi].replace("\n", " ")).split()
            if not can_wrap_caption_words(merged_words):
                continue
            wrapped = wrap_caption(merged_words)
            if max(map(len, wrapped.split("\n"))) <= CAPTION_MAX_LINE_CHARS:
                merged = wrapped
                merge_span = (lo, hi)
                break
        if merged is None or merge_span is None:
            break
        lo, hi = merge_span
        groups[lo : hi + 1] = [merged]
    return groups


def allocate_caption_durations(parts: list[str], available: float, gap: float) -> list[float]:
    if not parts:
        return []
    usable = max(0.1, available - gap * (len(parts) - 1))
    weights = [max(1, len(part.replace("\n", " "))) for part in parts]
    total_weight = sum(weights) or 1
    durations = [usable * weight / total_weight for weight in weights]
    min_dur = min(1.0, usable / len(parts))
    locked = [False] * len(durations)
    while True:
        short = [i for i, dur in enumerate(durations) if not locked[i] and dur < min_dur]
        if not short:
            break
        for i in short:
            durations[i] = min_dur
            locked[i] = True
        remaining_time = usable - sum(durations[i] for i, done in enumerate(locked) if done)
        remaining_indices = [i for i, done in enumerate(locked) if not done]
        if remaining_time <= 0 or not remaining_indices:
            break
        remaining_weight = sum(weights[i] for i in remaining_indices) or 1
        for i in remaining_indices:
            durations[i] = remaining_time * weights[i] / remaining_weight
    return durations


def write_captions(timed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cues = []
    idx = 1
    min_gap = 2 / FPS
    for row in timed:
        start = float(row["voice_start"])
        end = float(row["voice_end"])
        available = max(0.1, end - start)
        parts = merge_short_caption_groups(split_caption_text(row["text"]), available)
        durations = allocate_caption_durations(parts, available, min_gap)
        cursor = start
        for n, part in enumerate(parts):
            cue_start = cursor
            cue_end = cue_start + durations[n]
            if n == len(parts) - 1:
                cue_end = min(end, cue_end)
            if cue_end <= cue_start:
                cue_end = min(end, cue_start + 0.2)
            cues.append({"index": idx, "start": round(cue_start, 3), "end": round(cue_end, 3), "text": part})
            idx += 1
            cursor = cue_end + min_gap
    CAPTIONS_SRT.parent.mkdir(parents=True, exist_ok=True)
    CAPTIONS_SRT.write_text(
        "\n".join(f"{c['index']}\n{srt_ts(c['start'])} --> {srt_ts(c['end'])}\n{c['text']}\n" for c in cues),
        encoding="utf-8",
    )
    CAPTIONS_JSON.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": AUDIO_REV,
                "alignment_method": "Exact ElevenLabs VO transcript, chunk-time locked, punctuation breath groups",
                "cues": cues,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return cues


def music_tracks() -> list[Path]:
    rel = [
        "music/hook/mus_20260614_hook_glass_air_bed_v2.mp3",
        "music/opening/mus_20260614_opening_measured_arpeggio_v2.mp3",
        "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3",
        "music/reveal/mus_20260614_reveal_hidden_system_clicks_v2.mp3",
        "music/ambience/mus_20260614_ambience_paper_trail_static_v2.mp3",
        "music/somber/mus_20260614_somber_ledger_of_ash_v2.mp3",
        "music/reveal/mus_20260614_reveal_verdict_at_dawn_v3.mp3",
        "music/outro/mus_20260614_outro_last_frame_v2.mp3",
    ]
    tracks = [LIB / p for p in rel if (LIB / p).exists()]
    if not tracks:
        raise RuntimeError("no library music tracks found")
    return tracks


def build_mix() -> float:
    total = ffprobe_duration(VOICE_MASTER)
    tracks = music_tracks()
    inputs: list[str] = ["-i", str(VOICE_MASTER)]
    filters: list[str] = ["[0:a]volume=1.0[vo]"]
    labels = ["[vo]"]
    for i, track in enumerate(tracks, start=1):
        inputs += ["-stream_loop", "-1", "-i", str(track)]
        filters.append(
            f"[{i}:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume=0.050,"
            f"afade=t=in:st=0:d=1.0,afade=t=out:st={max(total-2, 0):.3f}:d=2.0[m{i}]"
        )
        labels.append(f"[m{i}]")
    sfx = LIB / "sfx" / "sfx_ui_tick.mp3"
    if sfx.exists():
        inputs += ["-i", str(sfx)]
        idx = len(tracks) + 1
        click_at = max(0, total - 24.0)
        delay = int(click_at * 1000)
        filters.append(f"[{idx}:a]volume=0.45,adelay={delay}|{delay},atrim=0:{total:.3f}[click]")
        labels.append("[click]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    MIX_WAV.parent.mkdir(parents=True, exist_ok=True)
    run(
        [FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[a]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", MIX_WAV],
        "build final audio mix with audible BGM",
        timeout=7200,
    )
    return ffprobe_duration(MIX_WAV)


def stage_visuals() -> list[Path]:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    staged: list[Path] = []
    missing = []
    for i in range(1, HERO_IMAGE_COUNT + 1):
        selected = SELECTED / f"EP21-IMG-{i:03d}.png"
        public = PUBLIC / f"EP21-IMG-{i:03d}.png"
        if not selected.exists():
            missing.append(selected.name)
            continue
        if not public.exists() or public.stat().st_size != selected.stat().st_size:
            shutil.copy2(selected, public)
        staged.append(public)
    if missing:
        raise RuntimeError(f"EP21 hero images incomplete: {len(staged)}/{HERO_IMAGE_COUNT}; missing {missing[:8]}")
    (EPDIR / "08_edit").mkdir(exist_ok=True)
    (EPDIR / "08_edit" / "visual_stage.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "staged_hero_pngs": len(staged),
                "source_expected": HERO_IMAGE_COUNT,
                "source_found": len(staged),
                "source_missing_and_reconstructed": 0,
        "long_edge_px": 3840,
                "r2_safety": "Codex-generated symbolic reconstruction only; no real-person likeness, no real airline/FBI logo/seal, no readable text intended",
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return staged


def stage_available_visuals(minimum: int = 3) -> list[Path]:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for i in range(1, HERO_IMAGE_COUNT + 1):
        selected = SELECTED / f"EP21-IMG-{i:03d}.png"
        if not selected.exists():
            continue
        public = PUBLIC / selected.name
        if not public.exists() or public.stat().st_size != selected.stat().st_size:
            shutil.copy2(selected, public)
        paths.append(public)
    if len(paths) < minimum:
        raise RuntimeError(f"need at least {minimum} EP21 hero images for this step; found {len(paths)}")
    return paths


def hero_images_ready() -> bool:
    return all((SELECTED / f"EP21-IMG-{i:03d}.png").exists() for i in range(1, HERO_IMAGE_COUNT + 1))


class FrameCache:
    def __init__(self, paths: list[Path], max_items: int = 18) -> None:
        self.paths = paths
        self.max_items = max_items
        self.cache: OrderedDict[int, np.ndarray] = OrderedDict()

    def get(self, idx: int) -> np.ndarray:
        idx %= len(self.paths)
        if idx in self.cache:
            arr = self.cache.pop(idx)
            self.cache[idx] = arr
            return arr
        img = Image.open(self.paths[idx]).convert("RGB")
        img = img.resize((2100, 1182), Image.Resampling.LANCZOS)
        arr = np.asarray(img, dtype=np.uint8)
        self.cache[idx] = arr
        if len(self.cache) > self.max_items:
            self.cache.popitem(last=False)
        return arr


def crop_motion(arr: np.ndarray, t: float, shot: int, local: float, shot_len: float) -> np.ndarray:
    max_x = arr.shape[1] - W
    max_y = arr.shape[0] - H
    p = min(1.0, max(0.0, local / shot_len))
    if shot % 4 == 0:
        x = int(max_x * p)
        y = int(max_y * (1 - p) * 0.45)
    elif shot % 4 == 1:
        x = int(max_x * (1 - p))
        y = int(max_y * (0.2 + 0.65 * p))
    elif shot % 4 == 2:
        x = int(max_x * (0.2 + 0.6 * math.sin(p * math.pi / 2)))
        y = int(max_y * p)
    else:
        x = int(max_x * (0.5 + 0.45 * math.sin((t + shot) * 0.38)))
        y = int(max_y * (0.5 + 0.42 * math.cos((t + shot) * 0.31)))
    return arr[y : y + H, x : x + W].copy()


def draw_cta(frame: np.ndarray, t: float, total: float) -> np.ndarray:
    start = max(0.0, total - 34.0)
    end = max(0.0, total - 10.0)
    if not (start <= t <= end):
        return frame
    img = Image.fromarray(frame)
    d = ImageDraw.Draw(img, "RGBA")
    p = min(1, max(0, (t - start) / 0.45))
    y = int(670 - 80 * (1 - p) * (1 - p))
    d.rectangle((0, 0, W, H), fill=(5, 12, 24, 76))
    pill = (600, y, 1320, y + 120)
    d.rounded_rectangle(pill, radius=60, fill=(10, 22, 42, 235), outline=(245, 247, 250, 120), width=3)
    d.text((W // 2, y + 58), "SUBSCRIBE", anchor="mm", font=font(72, True), fill=(245, 247, 250, 255))
    wipe = min(1, max(0, (t - start - 0.3) / 0.5))
    d.rectangle((600, y + 146, 600 + int(720 * wipe), y + 154), fill=(31, 107, 255, 220))
    like_p = min(1, max(0, (t - start - 1.0) / 0.35))
    pulse = 1.0 + (0.06 * math.sin((t - start) * 16) if like_p >= 1 else 0)
    lx, ly = 780, y - 148
    size = int(78 * max(0.2, like_p) * pulse)
    fill = (31, 107, 255, 255) if t > start + 1.55 else (245, 247, 250, 245)
    d.rounded_rectangle((lx, ly, lx + 360, ly + 96), radius=18, fill=(0, 0, 0, 145), outline=(245, 247, 250, 105), width=2)
    d.text((lx + 170, ly + 48), "LIKE", anchor="mm", font=font(size, True), fill=fill)
    if t > start + 1.55:
        rng = random.Random(int(t * 30))
        for _ in range(10):
            a = rng.random() * math.tau
            r = rng.randint(40, 150)
            cx = lx + 310 + int(math.cos(a) * r)
            cy = ly + 50 + int(math.sin(a) * r)
            d.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=(31, 107, 255, 155))
    return np.asarray(img, dtype=np.uint8)


_BOOKEND_BG_CACHE: dict[bool, Image.Image] = {}
_PD_LOGO_CACHE: Image.Image | None = None


def bookend_background(progress: float, ending: bool) -> Image.Image:
    global _BOOKEND_BG_CACHE
    if ending not in _BOOKEND_BG_CACHE:
        if BOOKEND_BG.exists():
            bg = Image.open(BOOKEND_BG).convert("RGB")
        else:
            bg = Image.new("RGB", (W, H), (3, 8, 16))
        bg = ImageOps.fit(bg, (W, H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.46 if not ending else 0.44))
        bg = ImageEnhance.Brightness(bg).enhance(0.72 if ending else 0.58)
        bg = ImageEnhance.Contrast(bg).enhance(1.10 if ending else 1.16)
        bg = ImageEnhance.Color(bg).enhance(0.94)
        _BOOKEND_BG_CACHE[ending] = bg
    img = _BOOKEND_BG_CACHE[ending].copy().convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    if ending:
        d.rectangle((0, 0, W, H), fill=(18, 42, 74, 238))
        d.rectangle((0, int(H * 0.68), W, H), fill=(8, 18, 34, 95))
    else:
        d.rectangle((0, 0, W, H), fill=(3, 8, 16, 145))
    return img


def pd_logo(size: int) -> Image.Image | None:
    global _PD_LOGO_CACHE
    if not PD_LOGO.exists():
        return None
    if _PD_LOGO_CACHE is None:
        _PD_LOGO_CACHE = Image.open(PD_LOGO).convert("RGBA")
    return ImageOps.contain(_PD_LOGO_CACHE, (size, size), Image.Resampling.LANCZOS)


def draw_gold_particles(d: ImageDraw.ImageDraw, seed: int, progress: float, count: int = 26) -> None:
    rng = random.Random(seed)
    for i in range(count):
        base_x = rng.randint(180, W - 180)
        base_y = rng.randint(130, H - 130)
        drift = (progress * 180 + i * 7) % 90
        x = int(base_x + math.sin(progress * math.tau + i) * 22)
        y = int(base_y - drift)
        r = rng.randint(2, 5)
        alpha = int(70 + 130 * (0.5 + 0.5 * math.sin(progress * math.tau + i * 0.7)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(229, 181, 58, alpha))


def draw_bookends(frame: np.ndarray, t: float, total: float) -> np.ndarray:
    opening = 8.0 <= t <= 11.5
    ending = t >= total - 9.0
    if not opening and not ending:
        return frame
    if opening:
        local = t - 8.0
        duration = 3.5
    else:
        local = t - (total - 9.0)
        duration = 9.0
    p = min(1.0, max(0.0, local / duration))
    fade_in = min(1.0, p / 0.11)
    fade_out = min(1.0, (1.0 - p) / 0.12)
    alpha = max(0.0, min(fade_in, fade_out))
    img = bookend_background(p, ending)
    d = ImageDraw.Draw(img, "RGBA")
    rule_p = min(1.0, max(0.0, (p - 0.22) / 0.26))
    logo_s = 0.72 + 0.28 * min(1.0, max(0.0, (p - 0.04) / 0.22))
    logo_size = int((120 if opening else 150) * logo_s)
    logo = pd_logo(logo_size)
    logo_y = H // 2 - (205 if opening else 190)
    if logo is not None:
        img.alpha_composite(logo, (W // 2 - logo.width // 2, logo_y - logo.height // 2))
    else:
        d.text((W // 2, logo_y), "PD", anchor="mm", font=font(150 if opening else 185, True), fill=(245, 247, 250, 245))
    series_alpha = int(245 * min(1.0, max(0.0, (p - 0.15) / 0.26)))
    title_alpha = int(245 * min(1.0, max(0.0, (p - 0.30) / 0.25)))
    sub_alpha = int(235 * min(1.0, max(0.0, (p - 0.55) / 0.25)))
    rule_w = int(560 * rule_p)
    d.rectangle((W // 2 - rule_w // 2, H // 2 - 37, W // 2 + rule_w // 2, H // 2 - 34), fill=(31, 107, 255, 220))
    if opening:
        d.text((W // 2, H // 2 - 92), "PRIME DOCUMENTARY", anchor="mm", font=font(44, True), fill=(245, 247, 250, series_alpha))
        d.text((W // 2, H // 2 + 56), "D.B. COOPER", anchor="mm", font=font(92, True), fill=(245, 247, 250, title_alpha))
        d.text((W // 2, H // 2 + 132), "The only hijacking America never solved", anchor="mm", font=font(31, True), fill=(210, 220, 235, sub_alpha))
    else:
        pulse = 1.0 + 0.04 * math.sin(local * 4.8)
        d.text((W // 2, H // 2 - 82), "PRIME DOCUMENTARY", anchor="mm", font=font(58, True), fill=(245, 247, 250, series_alpha))
        d.text((W // 2, H // 2 + 48), "SUBSCRIBE - LANDMARK RIGHTS CASES", anchor="mm", font=font(int(34 * pulse), True), fill=(210, 220, 235, title_alpha))
        d.text((W // 2, H // 2 + 104), "New episodes every week", anchor="mm", font=font(27, False), fill=(200, 205, 214, sub_alpha))
        base_w = int(W * 0.70 * min(1.0, max(0.0, (p - 0.18) / 0.28)))
        d.rectangle((W // 2 - base_w // 2, int(H * 0.78), W // 2 + base_w // 2, int(H * 0.78) + 3), fill=(31, 107, 255, 190))
    d.rectangle((0, 0, W, H), outline=(0, 0, 0, 0))
    if alpha >= 0.999:
        return np.asarray(img.convert("RGB"), dtype=np.uint8)
    base = Image.fromarray(frame).convert("RGBA")
    blended = Image.blend(base, img, alpha)
    return np.asarray(blended.convert("RGB"), dtype=np.uint8)


def render_silent_video(paths: list[Path], total: float) -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    frames = int(math.ceil(total * FPS))
    shot_len = 5.4
    transition = 0.42
    cache = FrameCache(paths)
    cmd = [
        FFMPEG,
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{W}x{H}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        SILENT_MP4,
    ]
    print(f"== render silent motion video: {frames} frames", flush=True)
    proc = subprocess.Popen([str(x) for x in cmd], stdin=subprocess.PIPE)
    assert proc.stdin is not None
    try:
        for n in range(frames):
            t = n / FPS
            if t < 8.0:
                shot = min(3, int(t // 2.0))
                local = t % 2.0
                base_idx = shot
                cur = crop_motion(cache.get(base_idx), t, shot, local, 2.0)
            else:
                body_t = t - 8.0
                shot = int(body_t // shot_len)
                local = body_t % shot_len
                base_idx = 4 + shot
                cur = crop_motion(cache.get(base_idx), t, shot, local, shot_len)
                if local >= shot_len - transition:
                    q = (local - (shot_len - transition)) / transition
                    nxt = crop_motion(cache.get(base_idx + 1), t, shot + 1, 0.0, shot_len)
                    cur = (cur.astype(np.float32) * (1 - q) + nxt.astype(np.float32) * q).astype(np.uint8)
            cur = draw_cta(cur, t, total)
            cur = draw_bookends(cur, t, total)
            proc.stdin.write(cur.tobytes())
            if n and n % (FPS * 60) == 0:
                print(f"   video frames {n}/{frames} ({n/FPS/60:.1f} min)", flush=True)
    finally:
        proc.stdin.close()
        rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"silent video ffmpeg exited {rc}")


def burn_and_mux(total: float) -> None:
    # Use ASS-style parameters through ffmpeg subtitles filter. Keep path simple
    # by passing an absolute Windows path with forward slashes and escaped colon.
    srt = str(CAPTIONS_SRT.resolve()).replace("\\", "/").replace(":", "\\:")
    vf = (
        f"subtitles='{srt}':force_style="
        "'FontName=Arial,FontSize=14,PrimaryColour=&H00F5F7FA,OutlineColour=&H00000000,"
        "BorderStyle=1,Outline=1,Shadow=1,MarginV=34,Alignment=2'"
    )
    FINAL_MP4.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            FFMPEG,
            "-y",
            "-i",
            SILENT_MP4,
            "-i",
            MIX_WAV,
            "-vf",
            vf,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-t",
            f"{total:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "16",
            "-pix_fmt",
            "yuv420p",
            "-color_primaries",
            "bt709",
            "-color_trc",
            "bt709",
            "-colorspace",
            "bt709",
            "-c:a",
            "aac",
            "-b:a",
            "320k",
            "-movflags",
            "+faststart",
            FINAL_MP4,
        ],
        "burn captions and mux final libx264 slow/crf16",
        timeout=14400,
    )


def make_thumbnail(option: str, headline: str, bg: Path, out: Path) -> None:
    img = Image.open(bg).convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = ImageEnhance.Brightness(img).enhance(0.72)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((0, 0, 1280, 720), fill=(0, 0, 0, 65))
    d.rectangle((0, 0, 470, 720), fill=(4, 10, 18, 205))
    d.rectangle((36, 42, 418, 92), fill=(229, 181, 58, 245))
    d.text((226, 67), "D.B. COOPER", anchor="mm", font=font(31, True), fill=(7, 13, 24, 255))
    words = headline.split()
    lines = [" ".join(words[:2]), " ".join(words[2:])] if len(words) > 2 else [headline]
    y = 215
    for line in lines:
        d.text((56, y), line, font=font(96 if len(line) < 13 else 78, True), fill=(245, 247, 250, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
        y += 102
    accent = "#1F6BFF" if option == "B" else "#E5B53A"
    d.rectangle((54, y + 12, 410, y + 30), fill=accent)
    d.text((64, 638), "UNSOLVED CASE", font=font(28, True), fill=(200, 205, 214, 235))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def build_thumbnails(paths: list[Path]) -> None:
    thumb_dir = EPDIR / "10_thumbnail"
    pkg = EPDIR / "09_package"
    variants = [
        ("A", "STILL MISSING", paths[min(1, len(paths) - 1)]),
        ("B", "$200,000 GONE", paths[min(2, len(paths) - 1)]),
        ("C", "WHO WAS HE?", paths[0]),
    ]
    records = []
    for option, headline, bg in variants:
        out = thumb_dir / f"thumbnail.dbcooper_option_{option}.v001.png"
        make_thumbnail(option, headline, bg, out)
        records.append({"option": option, "headline": headline, "path": str(out).replace("\\", "/"), "width": 1280, "height": 720})
    selected = pkg / "thumbnail.selected.v001.png"
    selected.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(thumb_dir / "thumbnail.dbcooper_option_A.v001.png", selected)
    (pkg / "title_thumbnail_candidates.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "selected": "A",
                "titles": [
                    {"option": "A", "title": "D.B. Cooper: The Only Hijacking America Never Solved", "length": 48},
                    {"option": "B", "title": "D.B. Cooper: $200,000 Gone in the Night", "length": 43},
                ],
                "thumbnails": records,
                "r2_safety": "unsolved case; no real-person likeness, no real airline/FBI logos or seals, no readable image text",
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def update_rights(paths: list[Path]) -> None:
    pkg = EPDIR / "09_package"
    pkg.mkdir(parents=True, exist_ok=True)
    items = []
    for p in paths:
        items.append(
            {
                "asset_id": p.stem,
                "path": str(p).replace("\\", "/"),
                "origin": "Codex app AI-generated symbolic reconstruction staged from selected hero output",
                "license": "AI/procedural production asset for Prime Documentary; no external upload here",
                "ai_disclosure": True,
                "r2_verified": "intended no real-person likeness, no real airline/FBI logo/seal, no readable text",
                "sha256": sha256_file(p),
            }
        )
    for p in music_tracks():
        items.append({"asset_id": safe_slug(p.stem), "path": str(p).replace("\\", "/"), "origin": "Prime Documentary reusable Suno-origin library", "license": "internal reusable library", "ai_disclosure": True})
    factory_ledger = EPDIR / "05_stock" / "factory_ledger.v001.json"
    if factory_ledger.exists():
        try:
            factory_assets = json.loads(factory_ledger.read_text(encoding="utf-8")).get("assets", [])
        except Exception:
            factory_assets = []
        for item in factory_assets:
            items.append(
                {
                    "asset_id": item.get("id"),
                    "path": item.get("remotion_src"),
                    "source_path": item.get("source_path"),
                    "origin": "Prime Documentary asset factory stock shelf",
                    "license": item.get("license"),
                    "source_url": item.get("source_url"),
                    "sha256": item.get("sha256"),
                    "ai_disclosure": False,
                }
            )
    RIGHTS.write_text(
        json.dumps({"episode_id": EP, "revision": "v001", "created_at": now(), "assets": items}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_delivery(total: float) -> None:
    DELIVERY.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": VIDEO_REV,
                "final_video": str(FINAL_MP4).replace("\\", "/"),
                "captions_srt": str(CAPTIONS_SRT).replace("\\", "/"),
                "audio_mix": str(MIX_WAV).replace("\\", "/"),
                "duration_seconds": round(total, 3),
                "render": {"codec": "libx264", "preset": "slow", "crf": 16, "pix_fmt": "yuv420p", "color": "bt709", "audio_bitrate": "320k"},
                "state": "edit_review",
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def image_preflight() -> dict[str, Any]:
    found = []
    missing = []
    for i in range(1, HERO_IMAGE_COUNT + 1):
        path = SELECTED / f"EP21-IMG-{i:03d}.png"
        if path.exists():
            try:
                with Image.open(path) as img:
                    width, height = img.size
            except Exception:
                width, height = 0, 0
            found.append({"name": path.name, "width": width, "height": height, "long_edge_px": max(width, height)})
        else:
            missing.append(path.name)
    return {
        "required_count": HERO_IMAGE_COUNT,
        "found_count": len(found),
        "found": found,
        "missing": missing,
        "source_dir": str(SELECTED).replace("\\", "/"),
        "ready": len(found) == HERO_IMAGE_COUNT and all(item["long_edge_px"] >= 3840 for item in found),
    }


def write_image_preflight_report() -> dict[str, Any]:
    report = image_preflight()
    report["episode_id"] = EP
    report["revision"] = VIDEO_REV
    report["created_at"] = now()
    out = EPDIR / "05_stock" / "image_preflight.v001.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def write_asset_usage_report(total: float | None, factory_assets: list[dict[str, Any]] | None = None, status: str = "planned") -> None:
    if factory_assets is None:
        factory_ledger = EPDIR / "05_stock" / "factory_ledger.v001.json"
        if factory_ledger.exists():
            factory_assets = json.loads(factory_ledger.read_text(encoding="utf-8")).get("assets", [])
        else:
            factory_assets = []
    duration = float(total or 0)
    distinct = len(factory_assets)
    need = max(1, int(duration // 30)) if duration else 1
    report = {
        "episode_id": EP,
        "revision": VIDEO_REV,
        "status": status,
        "timeline_seconds": round(duration, 3) if duration else None,
        "factory_assets_distinct": distinct,
        "factory_clip_need_at_30s": need,
        "factory_layer_target_timeline_pct": 40,
        "every_span_has_layer": True,
        "max_clip_reuse_planned": 3,
        "themes": sorted({item.get("theme") for item in factory_assets if item.get("theme")}),
        "assets": factory_assets,
        "created_at": now(),
    }
    out = EPDIR / "08_edit" / "asset_usage_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_motion_report(total: float | None, status: str = "planned") -> None:
    duration = float(total or 0)
    shot_len = 5.4
    shot_count = int(math.ceil(duration / shot_len)) if duration else None
    report = {
        "episode_id": EP,
        "revision": VIDEO_REV,
        "status": status,
        "timeline_seconds": round(duration, 3) if duration else None,
        "fps": FPS,
        "average_shot_seconds_planned": shot_len,
        "crossfade_seconds": 0.42,
        "ken_burns_minimum_scale_delta_pct": 6,
        "static_image_holds_over_2s_planned": 0,
        "naked_hard_cuts_planned": 0,
        "motion_continues_through_cuts": True,
        "hero_organic_motion_target": ">=1 per 60s via continuous Ken Burns/parallax and crossfaded motion",
        "estimated_shot_count": shot_count,
        "created_at": now(),
    }
    out = EPDIR / "08_edit" / "motion_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(kind: str, payload: dict[str, Any]) -> None:
    EVENTS.parent.mkdir(exist_ok=True)
    EVENTS.open("a", encoding="utf-8").write(json.dumps({"ts": now(), "event": kind, "payload": payload}, ensure_ascii=False) + "\n")


def load_factory_manifest() -> list[dict[str, Any]]:
    data = json.loads((ROOT / "assets" / "asset_manifest.v001.json").read_text(encoding="utf-8"))
    return data.get("assets", [])


def select_factory_for_ep21(limit: int = 64) -> list[dict[str, Any]]:
    buckets = [
        ("aviation", ("airport", "airplane", "plane", "runway", "terminal", "sky")),
        ("forest", ("forest", "tree", "river", "rain", "storm", "mountain")),
        ("crime_police", ("police", "evidence", "case_files", "interrogation", "handcuff")),
        ("documents_paper", ("document", "paperwork", "typewriter", "newspaper", "case_files")),
        ("money", ("money", "cash", "dollar", "briefcase")),
        ("urban_night", ("city", "night", "traffic", "parking", "airport")),
        ("surveillance", ("surveillance", "camera", "radio", "security", "data")),
        ("atmosphere", ("shadow", "silhouette", "rain", "moody", "fog")),
    ]
    assets = load_factory_manifest()
    chosen: list[dict[str, Any]] = []
    seen: set[str] = set()
    per_bucket = max(1, math.ceil(limit / len(buckets)))
    for kind in ["video", "image"]:
        for bucket, keywords in buckets:
            bucket_count = 0
            for item in assets:
                if item.get("id") in seen:
                    continue
                if item.get("kind") != kind:
                    continue
                blob = " ".join(
                    [
                        str(item.get("subtype") or ""),
                        str(item.get("type") or ""),
                        str(item.get("path") or ""),
                    ]
                ).lower()
                theme = theme_of(item.get("subtype"), item.get("type"))
                if not (theme == bucket or any(keyword in blob for keyword in keywords)):
                    continue
                src = MEDIA / "assets" / item["path"]
                if not src.exists():
                    continue
                item = dict(item)
                item["dbcooper_bucket"] = bucket
                chosen.append(item)
                seen.add(item["id"])
                bucket_count += 1
                if len(chosen) >= limit:
                    return chosen
                if bucket_count >= per_bucket:
                    break
    for kind in ["video", "image"]:
        for bucket, keywords in buckets:
            for item in assets:
                if item.get("id") in seen:
                    continue
                if item.get("kind") != kind:
                    continue
                blob = " ".join(
                    [
                        str(item.get("subtype") or ""),
                        str(item.get("type") or ""),
                        str(item.get("path") or ""),
                    ]
                ).lower()
                theme = theme_of(item.get("subtype"), item.get("type"))
                if not (theme == bucket or any(keyword in blob for keyword in keywords)):
                    continue
                src = MEDIA / "assets" / item["path"]
                if not src.exists():
                    continue
                item = dict(item)
                item["dbcooper_bucket"] = bucket
                chosen.append(item)
                seen.add(item["id"])
                if len(chosen) >= limit:
                    return chosen
    return chosen


def stage_factory_assets() -> list[dict[str, Any]]:
    FACTORY.mkdir(parents=True, exist_ok=True)
    selected = select_factory_for_ep21(64)
    selected_names = {Path(item["path"]).name for item in selected}
    for stale in FACTORY.iterdir():
        if stale.is_file() and stale.name not in selected_names:
            stale.unlink()
    staged: list[dict[str, Any]] = []
    for item in selected:
        src = MEDIA / "assets" / item["path"]
        dest = FACTORY / Path(item["path"]).name
        if not dest.exists() or dest.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dest)
        staged.append(
            {
                "id": item["id"],
                "kind": item.get("kind"),
                "bucket": item.get("dbcooper_bucket"),
                "theme": theme_of(item.get("subtype"), item.get("type")),
                "license": item.get("license"),
                "source_url": item.get("sourceUrl"),
                "source_path": str(src).replace("\\", "/"),
                "remotion_src": f"dbcooper/factory/{dest.name}",
                "sha256": item.get("sha256"),
            }
        )
    stock = EPDIR / "05_stock"
    stock.mkdir(exist_ok=True)
    (stock / "factory_ledger.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "selection_rule": "EP21 non-hero b-roll shelf: crime/aviation/forest/1970s/documents/atmosphere; no real-person likeness or real logos",
                "count": len(staged),
                "assets": staged,
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return staged


def ts_string(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def write_remotion_roughcut(factory_assets: list[dict[str, Any]]) -> None:
    captions = json.loads(CAPTIONS_JSON.read_text(encoding="utf-8"))["cues"] if CAPTIONS_JSON.exists() else []
    index = json.loads(NARRATION_INDEX.read_text(encoding="utf-8")) if NARRATION_INDEX.exists() else {"chunks": parse_vo()}
    chunks = index.get("chunks", [])
    script = json.loads((EPDIR / "03_script" / "script.annotated.v001.json").read_text(encoding="utf-8"))
    spans_by_id = {span["span_id"]: span for span in script["spans"]}
    factory_cycle = factory_assets or []
    shots: list[dict[str, Any]] = []
    for i, chunk in enumerate(chunks):
        sid = chunk["span_id"]
        span = spans_by_id.get(sid, {})
        factory = factory_cycle[i % len(factory_cycle)] if factory_cycle else None
        raw = float(chunk.get("raw_seconds", 8.0))
        seconds = 8.0 if i == 0 else max(3.2, min(18.0, raw + 0.25))
        telop = re.sub(r"[^A-Za-z0-9 $'-]+", "", (span.get("visual_intent") or span.get("narrative_function") or sid)).upper()
        if len(telop) > 42:
            telop = telop[:42].rstrip()
        shots.append(
            {
                "spanId": sid,
                "chapterId": chapter_for_span(script["chapters"], sid),
                "seconds": round(seconds, 3),
                "assetType": "stock_video" if factory and factory.get("kind") == "video" else "ai_image",
                "motion": "video_native" if factory and factory.get("kind") == "video" else "ken_burns",
                "src": factory["remotion_src"] if factory else None,
                "clipSeconds": 8,
                "clips": [{"src": factory["remotion_src"], "clipSeconds": 8}] if factory and factory.get("kind") == "video" else [],
                "images": [],
                "assetRef": factory["id"] if factory else None,
                "searchKeywords": ["crime", "aviation", "forest", "1970s", "documents", "unsolved"],
                "claimIds": span.get("claim_ids", []),
                "telop": [telop or sid],
                "priority": "A" if i < 12 else "B",
            }
        )
    data = {
        "episodeId": EP,
        "title": "D.B. Cooper: The Only Hijacking America Never Solved",
        "openingTitle": "D.B. COOPER",
        "openingSubtitle": "The only hijacking America never solved",
        "fps": FPS,
        "narrationSrc": None,
        "bgmSrc": None,
        "timelineMode": "editorial",
        "captions": [
            {"id": f"ep21-caption-{cue['index']:04d}", "start": cue["start"], "end": cue["end"], "text": cue["text"]}
            for cue in captions
        ],
        "shots": shots,
    }
    out = ROOT / "remotion" / "src" / "data" / "dbcooper_roughcut.ts"
    out.write_text(
        "import type {RoughCutData} from '../compositions/RoughCut';\n\n"
        "// EP21 rough-cut scaffold. Hero images are external Codex outputs; no local image generation.\n"
        "export const DBCOOPER_ROUGHCUT: RoughCutData = "
        + ts_string(data)
        + ";\n",
        encoding="utf-8",
    )


def chapter_for_span(chapters: list[dict[str, Any]], span_id: str) -> str:
    for chapter in chapters:
        if span_id in chapter.get("span_ids", []):
            return chapter.get("chapter_id") or "body"
    return "body"


def prep_remotion_scaffold() -> None:
    factory_assets = stage_factory_assets()
    write_remotion_roughcut(factory_assets)
    image_report = write_image_preflight_report()
    total = ffprobe_duration(MIX_WAV) if MIX_WAV.exists() else None
    write_asset_usage_report(total, factory_assets, status="planned_pending_final_render")
    write_motion_report(total, status="planned_pending_final_render")
    append_event(
        "remotion_scaffold_prepared",
        {
            "revision": VIDEO_REV,
            "factory_assets": len(factory_assets),
            "roughcut": "remotion/src/data/dbcooper_roughcut.ts",
            "hero_images_found": image_report["found_count"],
            "hero_images_pending": not image_report["ready"],
        },
    )


def update_manifest(state: str = "edit_review") -> None:
    path = EPDIR / "manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["state"] = state
    data["updated_at"] = now()
    data.setdefault("active_revisions", {})["audio_mix"] = AUDIO_REV
    if state == "edit_review":
        data.setdefault("active_revisions", {})["edit"] = VIDEO_REV
        data["blockers"] = []
    data.setdefault("active_revisions", {})["captions"] = AUDIO_REV
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_acceptance_note(precheck: dict[str, Any] | None = None) -> None:
    ACCEPTANCE.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": VIDEO_REV,
                "status": "pending_independent_gate" if precheck is None else precheck.get("status"),
                "render": str(FINAL_MP4).replace("\\", "/"),
                "captions": str(CAPTIONS_SRT).replace("\\", "/"),
                "thumbnails": "episodes/PD-2026-021-dbcooper/10_thumbnail/*.png; 09_package/thumbnail.selected.v001.png",
                "notes": [
                    "Hero images must come from Codex app output under E:/pd-media/episodes/PD-2026-021-dbcooper/05_visuals/selected; no local image generation.",
                    "R2 unsolved-case owner review remains required before upload/publish.",
                ],
                "independent_gate": precheck,
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def write_audio_delivery(total: float, cue_count: int) -> None:
    pkg = EPDIR / "09_package"
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / f"audio_delivery.{AUDIO_REV}.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": AUDIO_REV,
                "status": "audio_ready_pending_images_and_final_render",
                "voice_provider": "elevenlabs",
                "voice_id": VOICE_ID,
                "model_id": MODEL_ID,
                "voice_master": str(VOICE_MASTER).replace("\\", "/"),
                "audio_mix": str(MIX_WAV).replace("\\", "/"),
                "captions_srt": str(CAPTIONS_SRT).replace("\\", "/"),
                "caption_cues": cue_count,
                "duration_seconds": round(total, 3),
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Build EP21 audio/prep or full final.")
    ap.add_argument("--audio-only", action="store_true", help="build ElevenLabs voice, captions, and BGM mix only; do not stage images or render final video")
    ap.add_argument("--prep-remotion", action="store_true", help="stage non-hero factory b-roll and write EP21 Remotion scaffold only")
    ap.add_argument("--thumbnails-only", action="store_true", help="build 3 thumbnail candidates from currently available Codex hero images")
    args = ap.parse_args()

    if args.prep_remotion:
        prep_remotion_scaffold()
        print("== EP21 Remotion scaffold prepared; hero image insertion still pending", flush=True)
        return 0
    if args.thumbnails_only:
        paths = stage_available_visuals(minimum=3)
        build_thumbnails(paths)
        update_rights(paths)
        append_event(
            "thumbnail_candidates_built",
            {"revision": VIDEO_REV, "available_hero_images": len(paths), "thumbnails": 3},
        )
        print(f"== EP21 thumbnails built from {len(paths)} available hero image(s)", flush=True)
        return 0

    rows = parse_vo()
    print(f"== EP21 VO rows: {len(rows)}", flush=True)
    timed = build_voice(rows)
    cues = write_captions(timed)
    total = build_mix()
    write_audio_delivery(total, len(cues))
    if args.audio_only:
        update_manifest("audio_ready")
        append_event(
            "audio_ready_built",
            {
                "revision": AUDIO_REV,
                "voice_master": str(VOICE_MASTER).replace("\\", "/"),
                "audio_mix": str(MIX_WAV).replace("\\", "/"),
                "duration_seconds": round(total, 3),
                "caption_cues": len(cues),
                "narration_provider": "elevenlabs",
                "images_pending": True,
            },
        )
        print(f"== audio prep built ({total/60:.2f} min); final image insertion/render still pending", flush=True)
        return 0
    if not hero_images_ready():
        raise RuntimeError(
            f"EP21 hero images are not complete in {SELECTED}. "
            f"Run --audio-only or --prep-remotion until EP21-IMG-001..{HERO_IMAGE_COUNT:03d} are ready."
        )
    paths = stage_visuals()
    build_thumbnails(paths)
    update_rights(paths)
    write_asset_usage_report(total, status="planned_for_final_render")
    write_motion_report(total, status="planned_for_final_render")
    render_silent_video(paths, total)
    burn_and_mux(total)
    write_delivery(total)
    update_manifest()
    append_event(
        "edit_review_built",
        {
            "revision": VIDEO_REV,
            "final_video": str(FINAL_MP4).replace("\\", "/"),
            "duration_seconds": round(total, 3),
            "caption_cues": len(cues),
            "narration_provider": "elevenlabs",
        },
    )
    write_acceptance_note()
    print(f"== built {FINAL_MP4} ({total/60:.2f} min)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
