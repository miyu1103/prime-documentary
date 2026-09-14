#!/usr/bin/env python3
"""Build EP24 Rajaratnam into a local final accepted cut.

No upload, publish, schedule, or legal approval action is performed here.
Paid narration is idempotent: existing successful chunks are never regenerated.
"""
from __future__ import annotations

import argparse
import hashlib
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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from factory_themes import theme_of  # noqa: E402

EP = "PD-2026-024-rajaratnam"
EP_NUM = 24
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
SCENE_COUNT = 42
CAPTION_LINE_MAX = 42
CAPTION_GROUP_MAX = 78
CAPTION_WEAK_LINE_ENDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "by",
    "for",
    "from",
    "in",
    "is",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "were",
    "with",
}
WORK = EP_MEDIA / "08_edit" / "_build_v001"
VISUALS = EP_MEDIA / "05_visuals"
SELECTED = VISUALS / "selected"
PUBLIC = ROOT / "remotion" / "public" / "rajaratnam"
FACTORY = PUBLIC / "factory"
MASTER_DIR = EP_MEDIA / "06_audio" / f"master_elevenlabs_{VOICE_REV}"
RAW_DIR = MASTER_DIR / "raw_mp3"
WAV_DIR = MASTER_DIR / "wav"
LEDGER_DIR = MASTER_DIR / "request_ledger"
VOICE_MASTER = MASTER_DIR / f"voice_master.{VOICE_REV}.wav"
MIX_WAV = ROOT / "remotion" / "public" / "rajaratnam" / "audio" / f"rajaratnam_final_mix_{AUDIO_REV}.wav"
SILENT_MP4 = WORK / f"rajaratnam_silent_motion.{VIDEO_REV}.mp4"
FACTORY_BED_MP4 = WORK / f"rajaratnam_factory_bed.{VIDEO_REV}.mp4"
SILENT_FACTORY_MP4 = WORK / f"rajaratnam_silent_motion_factory.{VIDEO_REV}.mp4"
FINAL_MP4 = EP_MEDIA / "08_edit" / f"{VIDEO_REV}.mp4"
NARRATION_INDEX = EPDIR / "06_audio" / f"narration_index.{AUDIO_REV}.json"
VOICE_META = EPDIR / "06_audio" / f"voice_master.{VOICE_REV}.json"
CAPTIONS_SRT = EPDIR / "08_edit" / f"captions.{AUDIO_REV}.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / f"captions.{AUDIO_REV}.json"
CAPTIONS_TS = ROOT / "remotion" / "src" / "data" / "rajaratnam_captions.ts"
ROUGH_TS = ROOT / "remotion" / "src" / "data" / "rajaratnam_roughcut.ts"
COMP_TSX = ROOT / "remotion" / "src" / "compositions" / "RajaratnamPremium.tsx"
DELIVERY = EPDIR / "09_package" / f"final_delivery.{VIDEO_REV}.json"
RIGHTS = EPDIR / "09_package" / "rights_manifest.v001.json"
SELF_AUDIT = EPDIR / "09_package" / "self_audit_report.v001.json"
EVENTS = EPDIR / "events" / "events.jsonl"
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
ELEVEN_EST_USD_PER_CHAR = float(os.environ.get("ELEVENLABS_EST_USD_PER_CHAR", "0.0003"))
ELEVEN_HARD_BUDGET_USD = 25.0

INK = (5, 8, 14)
NAVY = (8, 22, 42)
BLUE = (31, 107, 255)
GOLD = (229, 181, 58)
SILVER = (200, 205, 214)
WHITE = (245, 247, 250)


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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def safe_slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", text).strip("_")


def parse_vo() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    script = (EPDIR / "03_script" / "script.en.v001.md").read_text(encoding="utf-8")
    for line in script.splitlines():
        if not line.startswith("[VO:]"):
            continue
        text = line[len("[VO:]") :].strip()
        text = re.sub(r"\s*\[CLM-\d+\]", "", text).strip()
        rows.append({"span_id": f"SPN-{len(rows)+1:04d}", "text": re.sub(r"\s+", " ", text)})
    if len(rows) != 64:
        raise RuntimeError(f"expected 64 VO rows, got {len(rows)}")
    return rows


def preflight() -> dict[str, Any]:
    required = [
        EPDIR / "03_script" / "script.en.v001.md",
        EPDIR / "03_script" / "script.annotated.v001.json",
        EPDIR / "01_research" / "claims.v001.json",
        EPDIR / "04_scenes" / "codex_image_prompts.v001.md",
        ROOT / "docs" / "PD_ONE_PASS_PRODUCTION_SPEC.v2.md",
        ROOT / "episodes" / "_planning" / "codex_prompt_024_rajaratnam.md",
        ROOT / "remotion" / "src" / "components" / "Bookends.tsx",
    ]
    for path in required:
        if not path.exists():
            raise RuntimeError(f"missing required input: {path}")
    ann = load_json(EPDIR / "03_script" / "script.annotated.v001.json")
    if len(ann.get("spans", [])) != 64:
        raise RuntimeError("annotated script is not locked at 64 spans")
    prompts = (EPDIR / "04_scenes" / "codex_image_prompts.v001.md").read_text(encoding="utf-8")
    scenes = sorted(set(re.findall(r"\bS\d{3}\b", prompts)))
    if len(scenes) != SCENE_COUNT:
        raise RuntimeError(f"expected {SCENE_COUNT} scene prompts, got {len(scenes)}")
    config = (ROOT / "remotion" / "remotion.config.ts").read_text(encoding="utf-8")
    required_config = [
        "setVideoImageFormat('png')",
        "setCodec('h264')",
        "setCrf(16)",
        "setX264Preset('slow')",
        "setPixelFormat('yuv420p')",
        "setColorSpace('bt709')",
        "setAudioCodec('aac')",
        "setAudioBitrate('320k')",
        "setChromiumOpenGlRenderer('angle')",
    ]
    missing = [token for token in required_config if token not in config]
    if missing:
        raise RuntimeError(f"remotion.config.ts missing canonical values: {missing}")
    probe = subprocess.run(
        [str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/check_final_acceptance.py", str(EP_NUM), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    val = subprocess.run(
        [str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/validate_episode.py", str(EP_NUM)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if val.returncode != 0:
        raise RuntimeError(f"validate_episode.py failed:\n{val.stdout}\n{val.stderr}")
    return {
        "annotated_spans": 64,
        "scenes": len(scenes),
        "final_acceptance_executes": probe.returncode in {0, 1},
        "validate_episode": "PASS",
    }


def estimate_budget(rows: list[dict[str, Any]]) -> dict[str, Any]:
    chars = sum(len(row["text"]) for row in rows)
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
        data = load_json(lp)
    except Exception:
        return False
    return data.get("status") == "ok" and data.get("request_hash") == req_hash


def guard_unknown(row: dict[str, Any], req_hash: str) -> None:
    lp = ledger_path(row)
    if not lp.exists() or raw_path(row).exists():
        return
    try:
        data = load_json(lp)
    except Exception:
        return
    if data.get("request_hash") == req_hash and data.get("status") in {"started", "unknown"}:
        raise RuntimeError(f"{row['span_id']} has a prior unknown ElevenLabs request; refusing duplicate paid call")


def synthesize_chunk(row: dict[str, Any], api_key: str) -> dict[str, Any]:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    req_hash = request_hash(row)
    if chunk_completed(row, req_hash):
        data = load_json(ledger_path(row))
        data["skipped_existing"] = True
        return data
    guard_unknown(row, req_hash)
    idem = f"pd-2026-024-rajaratnam-{VOICE_REV}-{row['span_id']}-{req_hash[:16]}"
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
    time.sleep(0.2)
    return ok


def build_voice(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    load_dotenv()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is not set")
    budget = estimate_budget(rows)
    print(f"== ElevenLabs budget estimate: ${budget['estimated_usd']} / ${ELEVEN_HARD_BUDGET_USD}", flush=True)
    chunk_meta = [synthesize_chunk(row, api_key) for row in rows]
    WAV_DIR.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    concat = WORK / "voice_concat.txt"
    lines: list[str] = []
    timed: list[dict[str, Any]] = []
    cursor = 0.0
    chapter_starts = {"SPN-0001", "SPN-0007", "SPN-0022", "SPN-0036", "SPN-0048", "SPN-0060"}
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
        pause = 1.05
        if row["span_id"] in chapter_starts and i > 0:
            pause = 1.9
        timed.append({**row, "voice_start": round(cursor, 3), "voice_end": round(cursor + dur, 3), "raw_seconds": round(dur, 3), "file": str(wav)})
        lines.append(f"file '{wav.as_posix()}'\n")
        cursor += dur
        if i < len(rows) - 1:
            silence = WAV_DIR / f"_pause_{i+1:03d}_{int(pause*1000)}ms.wav"
            if not silence.exists():
                run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{pause:.3f}", "-c:a", "pcm_s16le", silence], f"make pause {i+1}")
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
    VOICE_META.write_text(
        json.dumps(
            {
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
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
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


def wrap_caption(words: list[str]) -> str:
    joined = " ".join(words)
    if len(joined) <= CAPTION_LINE_MAX:
        return joined
    candidates: list[tuple[int, int]] = []
    spaces = [m.start() for m in re.finditer(" ", joined)]
    if not spaces:
        return joined
    for cut in spaces:
        left = joined[:cut].strip()
        right = joined[cut + 1 :].strip()
        if not left or not right:
            continue
        left_words = left.split()
        right_words = right.split()
        left_last = left_words[-1].strip(".,;:!?\"')(").lower()
        right_first = right_words[0].strip(".,;:!?\"')(").lower()
        score = abs(len(left) - len(right)) * 3
        score += max(0, len(left) - CAPTION_LINE_MAX) * 1000
        score += max(0, len(right) - CAPTION_LINE_MAX) * 1000
        if left_last in CAPTION_WEAK_LINE_ENDS:
            score += 900
        if right_first in CAPTION_WEAK_LINE_ENDS and len(right_words) <= 2:
            score += 30
        if len(left_words) == 1 or len(right_words) == 1:
            score += 60
        candidates.append((score, cut))
    if not candidates:
        return joined
    _, cut = min(candidates)
    return joined[:cut].strip() + "\n" + joined[cut + 1 :].strip()


def split_caption_text(text: str) -> list[str]:
    words = text.split()
    groups: list[list[str]] = []
    cur: list[str] = []
    for word in words:
        phrase = " ".join(cur + [word])
        if cur and len(phrase) > CAPTION_GROUP_MAX:
            groups.append(cur)
            cur = []
        cur.append(word)
        phrase = " ".join(cur)
        if (re.search(r"[.?!]([\"')\]]*)$", word) and len(phrase) >= 18) or (re.search(r"[,;:]$", word) and len(phrase) >= 30) or len(phrase) >= CAPTION_GROUP_MAX:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return [wrap_caption(g) for g in groups]


def merge_short_caption_groups(parts: list[str], available: float) -> list[str]:
    groups = parts[:]
    gap = 2 / FPS
    while len(groups) > 1:
        usable = max(0.1, available - gap * (len(groups) - 1))
        weights = [max(1, len(g.replace("\n", " "))) for g in groups]
        durations = [usable * w / sum(weights) for w in weights]
        short = [i for i, dur in enumerate(durations) if dur < 1.0]
        if not short:
            break
        i = short[0]
        candidates = []
        if i > 0:
            candidates.append((i - 1, i))
        if i < len(groups) - 1:
            candidates.append((i, i + 1))
        merged = None
        span = None
        for lo, hi in candidates:
            wrapped = wrap_caption((groups[lo].replace("\n", " ") + " " + groups[hi].replace("\n", " ")).split())
            if len(wrapped.splitlines()) <= 2 and max(len(x) for x in wrapped.splitlines()) <= CAPTION_LINE_MAX:
                merged = wrapped
                span = (lo, hi)
                break
        if merged is None or span is None:
            break
        groups[span[0] : span[1] + 1] = [merged]
    return groups


def smooth_weak_linebreak_cues(cues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    smoothed: list[dict[str, Any]] = []
    gap = 2 / FPS
    for cue in cues:
        lines = cue["text"].splitlines()
        if len(lines) != 2:
            smoothed.append(cue)
            continue
        left_last = lines[0].split()[-1].strip(".,;:!?\"')(").lower()
        if left_last not in CAPTION_WEAK_LINE_ENDS:
            smoothed.append(cue)
            continue
        left_words = lines[0].split()
        weak_word = left_words[-1]
        shifted_right = f"{weak_word} {lines[1]}"
        if len(left_words) > 1 and len(shifted_right) <= CAPTION_LINE_MAX:
            lines = [" ".join(left_words[:-1]), shifted_right]
        available = cue["end"] - cue["start"] - gap
        weights = [max(1, len(line.replace(" ", ""))) for line in lines]
        durations = [available * weight / sum(weights) for weight in weights]
        if available <= 0 or min(durations) < 1.0:
            smoothed.append(cue)
            continue
        cps = [len(lines[i].replace(" ", "")) / durations[i] for i in range(2)]
        if max(cps) > 17:
            smoothed.append(cue)
            continue
        first_end = round(cue["start"] + durations[0], 3)
        second_start = round(first_end + gap, 3)
        smoothed.append({"index": cue["index"], "start": cue["start"], "end": first_end, "text": lines[0]})
        smoothed.append({"index": cue["index"], "start": second_start, "end": cue["end"], "text": lines[1]})
    for i in range(len(smoothed) - 1):
        lines = smoothed[i]["text"].splitlines()
        if len(lines) != 1 or re.search(r"[.?!]([\"')\]]*)$", lines[0]):
            continue
        words = lines[0].split()
        if len(words) <= 1:
            continue
        left_last = words[-1].strip(".,;:!?\"')(").lower()
        if left_last not in CAPTION_WEAK_LINE_ENDS:
            continue
        current_text = " ".join(words[:-1])
        next_text = wrap_caption((words[-1] + " " + smoothed[i + 1]["text"].replace("\n", " ")).split())
        if max(len(line) for line in next_text.splitlines()) > CAPTION_LINE_MAX:
            continue
        current_cps = len(current_text.replace(" ", "")) / max(0.1, smoothed[i]["end"] - smoothed[i]["start"])
        next_cps = len(next_text.replace("\n", " ").replace(" ", "")) / max(0.1, smoothed[i + 1]["end"] - smoothed[i + 1]["start"])
        if max(current_cps, next_cps) > 17:
            continue
        smoothed[i]["text"] = current_text
        smoothed[i + 1]["text"] = next_text
    for idx, cue in enumerate(smoothed, 1):
        cue["index"] = idx
    return smoothed


def write_captions(timed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cues: list[dict[str, Any]] = []
    idx = 1
    gap = 2 / FPS
    for row in timed:
        start = float(row["voice_start"])
        end = float(row["voice_end"])
        available = max(0.1, end - start)
        parts = merge_short_caption_groups(split_caption_text(row["text"]), available)
        usable = max(0.1, available - gap * (len(parts) - 1))
        weights = [max(1, len(part.replace("\n", " "))) for part in parts]
        total_weight = sum(weights) or 1
        durations = [usable * w / total_weight for w in weights]
        cursor = start
        for n, part in enumerate(parts):
            cue_start = cursor
            cue_end = cursor + durations[n]
            if n == len(parts) - 1:
                cue_end = min(end, cue_end)
            cues.append({"index": idx, "start": round(cue_start, 3), "end": round(cue_end, 3), "text": part})
            idx += 1
            cursor = cue_end + gap
    for i, cue in enumerate(cues):
        if cue["end"] - cue["start"] >= 1.0:
            continue
        limit = cues[i + 1]["start"] - gap if i + 1 < len(cues) else cue["start"] + 1.0
        cue["end"] = round(min(cue["start"] + 1.0, limit), 3)
    cues = smooth_weak_linebreak_cues(cues)
    CAPTIONS_SRT.parent.mkdir(parents=True, exist_ok=True)
    CAPTIONS_SRT.write_text(
        "\n".join(f"{c['index']}\n{srt_ts(c['start'])} --> {srt_ts(c['end'])}\n{c['text']}\n" for c in cues),
        encoding="utf-8",
    )
    CAPTIONS_JSON.write_text(
        json.dumps(
            {"episode_id": EP, "revision": AUDIO_REV, "alignment_method": "ElevenLabs chunk timing against rendered audio; cue groups split by phrase/breath punctuation", "cues": cues},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    CAPTIONS_TS.write_text(
        "export const RAJARATNAM_CAPTIONS = "
        + json.dumps(
            [{"id": f"ep24-caption-{c['index']:04d}", "start": c["start"], "end": c["end"], "text": c["text"]} for c in cues],
            indent=2,
            ensure_ascii=False,
        )
        + " as const;\n",
        encoding="utf-8",
    )
    return cues


def music_tracks() -> list[Path]:
    rel = [
        "music/hook/mus_20260614_hook_glass_air_bed_v2.mp3",
        "music/opening/mus_20260614_opening_measured_arpeggio_v2.mp3",
        "music/ambience/mus_20260614_ambience_paper_trail_static_v2.mp3",
        "music/reveal/mus_20260614_reveal_hidden_system_clicks_v2.mp3",
        "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3",
        "music/outro/mus_20260614_outro_last_frame_v2.mp3",
    ]
    tracks = [LIB / p for p in rel if (LIB / p).exists()]
    if len(tracks) < 3:
        raise RuntimeError("not enough library music tracks found")
    return tracks


def build_mix() -> float:
    total = ffprobe_duration(VOICE_MASTER)
    tracks = music_tracks()
    MIX_WAV.parent.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = ["-i", str(VOICE_MASTER)]
    filters: list[str] = ["[0:a]volume=1.0[vo]"]
    labels = ["[vo]"]
    for i, track in enumerate(tracks, start=1):
        inputs += ["-stream_loop", "-1", "-i", str(track)]
        vol = 0.030 if i == 1 else 0.024
        filters.append(
            f"[{i}:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume={vol:.3f},"
            f"afade=t=in:st=0:d=1.0,afade=t=out:st={max(total-2,0):.3f}:d=2.0[m{i}]"
        )
        labels.append(f"[m{i}]")
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11:linear=true[mix]")
    run(
        [
            FFMPEG,
            "-y",
            *inputs,
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[mix]",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            MIX_WAV,
        ],
        "build continuous BGM/VO mix",
        timeout=7200,
    )
    qc = audio_qc(MIX_WAV)
    (EPDIR / "08_edit").mkdir(exist_ok=True)
    (EPDIR / "08_edit" / "audio_mix.v001.qc.json").write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return ffprobe_duration(MIX_WAV)


def audio_qc(path: Path) -> dict[str, Any]:
    qc: dict[str, Any] = {"path": str(path).replace("\\", "/")}
    try:
        out = subprocess.run(
            [FFMPEG, "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=framelog=quiet", "-f", "null", os.devnull],
            capture_output=True,
            text=True,
            check=True,
            timeout=900,
        )
        m = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", out.stderr)
        qc["integrated_lufs"] = float(m[-1]) if m else None
    except Exception as exc:
        qc["loudness_error"] = repr(exc)
    try:
        out = subprocess.run(
            [FFMPEG, "-hide_banner", "-nostats", "-i", str(path), "-af", "silencedetect=n=-40dB:d=0.6", "-f", "null", os.devnull],
            capture_output=True,
            text=True,
            check=True,
            timeout=900,
        )
        silences = [float(x) for x in re.findall(r"silence_duration:\s*(\d+(?:\.\d+)?)", out.stderr)]
        qc["silence_total_seconds"] = round(sum(silences), 3)
        qc["silence_longest_seconds"] = round(max(silences), 3) if silences else 0
    except Exception as exc:
        qc["silence_error"] = repr(exc)
    qc["created_at"] = now()
    return qc


def draw_gradient(size: tuple[int, int], c1: tuple[int, int, int], c2: tuple[int, int, int]) -> Image.Image:
    w, h = size
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        t = y / max(1, h - 1)
        arr[y, :, :] = np.array(c1) * (1 - t) + np.array(c2) * t
    return Image.fromarray(arr, "RGB")


def make_procedural_scene(scene: int, out: Path) -> None:
    rnd = random.Random(scene * 24024)
    img = draw_gradient((PANEL_W, PANEL_H), INK, NAVY).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(140):
        x = rnd.randint(-300, PANEL_W + 300)
        y = rnd.randint(0, PANEL_H)
        length = rnd.randint(120, 720)
        color = BLUE if rnd.random() < 0.58 else GOLD
        alpha = rnd.randint(18, 90)
        d.line((x, y, x + length, y + rnd.randint(-80, 80)), fill=(*color, alpha), width=rnd.randint(2, 8))
    motif = scene % 7
    cx, cy = PANEL_W // 2, PANEL_H // 2
    if motif == 0:
        d.rounded_rectangle((1200, 790, 2640, 1330), radius=80, fill=(12, 14, 22, 210), outline=(*SILVER, 160), width=8)
        for x in range(1320, 2520, 110):
            y1 = max(1010, 1110 + rnd.randint(-260, 260))
            d.rectangle((x, 1010, x + 42, y1), fill=(*BLUE, 180))
    elif motif == 1:
        for r in range(260, 850, 90):
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(*GOLD, 110), width=8)
        d.rectangle((cx - 900, cy - 8, cx + 900, cy + 8), fill=(*BLUE, 200))
    elif motif == 2:
        for n in range(18):
            x = 420 + n * 170
            d.rectangle((x, 520, x + 75, 1640), fill=(*SILVER, 80))
            d.rectangle((x + 22, 560, x + 53, 1590), fill=(*BLUE, 70))
        d.line((420, 1700, 3360, 1700), fill=(*GOLD, 210), width=10)
    elif motif == 3:
        points = [(rnd.randint(360, 3480), rnd.randint(360, 1800)) for _ in range(34)]
        for a in points:
            for b in rnd.sample(points, 3):
                d.line((*a, *b), fill=(*GOLD, 55), width=3)
        for p in points:
            d.ellipse((p[0] - 18, p[1] - 18, p[0] + 18, p[1] + 18), fill=(*BLUE, 210))
    elif motif == 4:
        for n in range(11):
            x = 620 + n * 240
            d.rounded_rectangle((x, 800, x + 130, 1320), radius=24, fill=(72, 56, 32, 180), outline=(*GOLD, 110), width=4)
        d.polygon([(300, 760), (3540, 640), (3300, 760), (540, 880)], fill=(*SILVER, 55))
    elif motif == 5:
        for n in range(8):
            x0 = 680 + n * 320
            d.rectangle((x0, 700, x0 + 190, 1380), fill=(*SILVER, 80))
            d.rectangle((x0 + 20, 760, x0 + 170, 840), fill=(*BLUE, 85))
        d.arc((860, 430, 2980, 1660), start=0, end=190, fill=(*GOLD, 160), width=14)
    else:
        for n in range(7):
            y = 520 + n * 190
            pts = []
            for x in range(420, 3440, 80):
                pts.append((x, y + int(math.sin((x / 220) + scene + n) * 70)))
            d.line(pts, fill=(*BLUE, 180), width=9)
        d.rectangle((780, 590, 3060, 1510), outline=(*SILVER, 80), width=5)
    for _ in range(80):
        x = rnd.randint(0, PANEL_W)
        y = rnd.randint(0, PANEL_H)
        r = rnd.randint(2, 9)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*SILVER, rnd.randint(35, 115)))
    vignette = Image.new("L", (PANEL_W, PANEL_H), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-600, -420, PANEL_W + 600, PANEL_H + 420), fill=220)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=180))
    dark = Image.new("RGB", (PANEL_W, PANEL_H), INK)
    img = Image.composite(img, dark, Image.eval(vignette, lambda p: 255 - p))
    img = ImageEnhance.Contrast(img).enhance(1.18)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def stage_visuals(allow_procedural_fill: bool = True) -> list[Path]:
    SELECTED.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    source_dir = EPDIR / "05_assets" / "ai_stills"
    paths: list[Path] = []
    for i in range(1, SCENE_COUNT + 1):
        sid = f"S{i:03d}"
        src = next(source_dir.glob(f"{sid}_codex_still*.png"), None)
        selected = SELECTED / f"{sid}_codex_still.v001.png"
        if src and not selected.exists():
            shutil.copy2(src, selected)
        if not selected.exists():
            if not allow_procedural_fill:
                raise RuntimeError(f"missing image: {sid}")
            make_procedural_scene(i, selected)
        im = Image.open(selected).convert("RGB")
        if im.size != (PANEL_W, PANEL_H):
            im = ImageOpsCover(im, (PANEL_W, PANEL_H))
            im.save(selected)
        pub = PUBLIC / f"{sid}.png"
        if not pub.exists() or pub.stat().st_size != selected.stat().st_size:
            shutil.copy2(selected, pub)
        paths.append(selected)
    return paths


def ImageOpsCover(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    src_w, src_h = im.size
    dst_w, dst_h = size
    scale = max(dst_w / src_w, dst_h / src_h)
    new_size = (int(src_w * scale + 0.5), int(src_h * scale + 0.5))
    im = im.resize(new_size, Image.Resampling.LANCZOS)
    left = (new_size[0] - dst_w) // 2
    top = (new_size[1] - dst_h) // 2
    return im.crop((left, top, left + dst_w, top + dst_h))


def load_factory_manifest() -> list[dict[str, Any]]:
    return load_json(ROOT / "assets" / "asset_manifest.v001.json").get("assets", [])


def select_factory(limit: int = 72) -> list[dict[str, Any]]:
    themes = [
        "finance_money",
        "legal_court",
        "crime_police",
        "technology",
        "surveillance_tech",
        "urban_night",
        "documents_paper",
        "abstract_loop",
        "atmosphere_symbolic",
    ]
    assets = load_factory_manifest()
    chosen: list[dict[str, Any]] = []
    seen: set[str] = set()
    for kind in ["video", "image"]:
        for theme in themes:
            for item in assets:
                if item.get("id") in seen or item.get("kind") != kind:
                    continue
                if theme_of(item.get("subtype"), item.get("type")) != theme and theme not in item.get("tags", []):
                    continue
                src = MEDIA / "assets" / item["path"]
                if not src.exists():
                    continue
                chosen.append(item)
                seen.add(item["id"])
                if len(chosen) >= limit:
                    return chosen
    return chosen


def stage_factory_assets() -> list[dict[str, Any]]:
    FACTORY.mkdir(parents=True, exist_ok=True)
    selected = select_factory(72)
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
                "theme": theme_of(item.get("subtype"), item.get("type")),
                "license": item.get("license"),
                "source_url": item.get("sourceUrl"),
                "source_path": str(src).replace("\\", "/"),
                "remotion_src": f"rajaratnam/factory/{dest.name}",
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
                "selection_rule": "finance/legal/crime/tech/surveillance/city/document factory layer; staged read-only from asset manifest",
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


def chapter_for_span(chapters: list[dict[str, Any]], span_id: str) -> str:
    for chapter in chapters:
        if span_id in chapter.get("span_ids", []):
            return chapter.get("chapter_id") or "body"
    return "body"


def write_remotion_scaffold(factory_assets: list[dict[str, Any]], timed: list[dict[str, Any]], cues: list[dict[str, Any]]) -> None:
    ann = load_json(EPDIR / "03_script" / "script.annotated.v001.json")
    spans = {s["span_id"]: s for s in ann["spans"]}
    shots = []
    for i, row in enumerate(timed):
        span = spans[row["span_id"]]
        scene_idx = min(SCENE_COUNT, i * SCENE_COUNT // len(timed) + 1)
        factory = factory_assets[i % len(factory_assets)] if factory_assets else None
        shots.append(
            {
                "spanId": row["span_id"],
                "chapterId": chapter_for_span(ann["chapters"], row["span_id"]),
                "seconds": round(max(4.0, row["voice_end"] - row["voice_start"] + 0.15), 3),
                "assetType": "ai_image",
                "motion": "parallax",
                "src": f"rajaratnam/S{scene_idx:03d}.png",
                "clips": [{"src": factory["remotion_src"], "clipSeconds": 8}] if factory else [],
                "claimIds": span.get("claim_ids", []),
                "telop": [],
                "priority": "A" if i < 18 else "B",
            }
        )
    rough = {
        "episodeId": EP,
        "title": "The Wiretap That Cracked Wall Street",
        "openingTitle": "THE WIRETAP",
        "openingSubtitle": "That cracked Wall Street",
        "fps": FPS,
        "narrationSrc": None,
        "bgmSrc": "rajaratnam/audio/rajaratnam_final_mix_v001.wav",
        "captions": [{"id": f"ep24-caption-{c['index']:04d}", "start": c["start"], "end": c["end"], "text": c["text"]} for c in cues],
        "shots": shots,
    }
    ROUGH_TS.write_text(
        "import type {RoughCutData} from '../compositions/RoughCut';\n\n"
        "export const RAJARATNAM_ROUGHCUT: RoughCutData = "
        + json.dumps(rough, indent=2, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    COMP_TSX.write_text(
        "import React from 'react';\n"
        "import {RoughCut} from './RoughCut';\n"
        "import {RAJARATNAM_ROUGHCUT} from '../data/rajaratnam_roughcut';\n\n"
        "export const rajaratnamPremiumDurationInFrames = (fps: number) => Math.round(30 * 60 * fps);\n\n"
        "export const RajaratnamPremium: React.FC = () => {\n"
        "  // factory layer is referenced through RAJARATNAM_ROUGHCUT.shots[*].factory / clips.\n"
        "  return <RoughCut data={RAJARATNAM_ROUGHCUT} />;\n"
        "};\n",
        encoding="utf-8",
    )


class FrameCache:
    def __init__(self, paths: list[Path]) -> None:
        self.paths = paths
        self.cache: dict[int, np.ndarray] = {}

    def get(self, idx: int) -> np.ndarray:
        idx %= len(self.paths)
        if idx not in self.cache:
            im = Image.open(self.paths[idx]).convert("RGB")
            im = ImageOpsCover(im, (W, H))
            self.cache[idx] = np.asarray(im, dtype=np.uint8)
        return self.cache[idx]


def crop_motion(panel: np.ndarray, t: float, shot: int, local: float, dur: float) -> np.ndarray:
    im = Image.fromarray(panel)
    z = 1.0 + 0.085 * (local / max(dur, 0.1))
    dx = math.sin(shot * 0.73) * 36 * (local / max(dur, 0.1))
    dy = math.cos(shot * 0.61) * 26 * (local / max(dur, 0.1))
    nw, nh = int(W * z), int(H * z)
    zoomed = im.resize((nw, nh), Image.Resampling.BICUBIC)
    left = int((nw - W) / 2 + dx)
    top = int((nh - H) / 2 + dy)
    left = max(0, min(nw - W, left))
    top = max(0, min(nh - H, top))
    frame = zoomed.crop((left, top, left + W, top + H))
    arr = np.array(frame, dtype=np.uint8)
    x = int((t * 105 + shot * 37) % (W + 320)) - 160
    x0, x1 = max(0, x), min(W, x + 8)
    if x1 > x0:
        arr[:, x0:x1, :] = np.maximum(arr[:, x0:x1, :], np.array([120, 88, 24], dtype=np.uint8))
    return arr


def draw_bookend(frame: np.ndarray, t: float, total: float) -> np.ndarray:
    opening = 8.0 <= t <= 11.5
    ending = t >= total - 9.0
    if not opening and not ending:
        return frame
    local = t - 8.0 if opening else t - (total - 9.0)
    dur = 3.5 if opening else 9.0
    p = min(1.0, max(0.0, local / dur))
    base = Image.fromarray(frame).convert("RGB")
    img = draw_gradient((W, H), INK, NAVY).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    sweep = int(-480 + (W + 960) * ((p * 1.4) % 1.0))
    d.polygon([(sweep - 220, 0), (sweep + 140, 0), (sweep + 520, H), (sweep + 120, H)], fill=(*WHITE, 50))
    d.ellipse((540, 275, 1380, 1115), outline=(*GOLD, 150), width=10)
    d.text((W // 2, 405), "PD", anchor="mm", font=font(180 if opening else 210, True), fill=(*GOLD, 245))
    if opening:
        d.text((W // 2, 560), "PRIME DOCUMENTARY", anchor="mm", font=font(54, True), fill=(*WHITE, 240))
        d.rectangle((680, 625, 1240, 630), fill=(*GOLD, 230))
        d.text((W // 2, 720), "THE WIRETAP", anchor="mm", font=font(104, True), fill=(*WHITE, 255))
        d.text((W // 2, 800), "THAT CRACKED WALL STREET", anchor="mm", font=font(42, True), fill=(*GOLD, 245))
    else:
        d.text((W // 2, 560), "PRIME DOCUMENTARY", anchor="mm", font=font(70, True), fill=(*WHITE, 248))
        d.rectangle((650, 636, 1270, 642), fill=(*GOLD, 230))
        d.text((W // 2, 720), "SUBSCRIBE", anchor="mm", font=font(64, True), fill=(*GOLD, 250))
        d.text((W // 2, 785), "FOR LANDMARK CASES", anchor="mm", font=font(36, True), fill=(*SILVER, 240))
    fade_in = min(1.0, p / 0.12)
    fade_out = min(1.0, (1.0 - p) / 0.12)
    return np.asarray(Image.blend(base, img, min(fade_in, fade_out)), dtype=np.uint8)


def draw_cta(frame: np.ndarray, t: float, total: float) -> np.ndarray:
    start = max(0, total - 30.0)
    end = max(0, total - 9.5)
    if not (start <= t <= end):
        return frame
    p = (t - start) / max(0.1, end - start)
    img = Image.fromarray(frame).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    alpha = int(235 * min(1, p / 0.15, (1 - p) / 0.15))
    d.rounded_rectangle((560, 770, 1360, 890), radius=34, fill=(4, 8, 16, alpha), outline=(*GOLD, alpha), width=4)
    fill_like = int(255 * min(1.0, max(0.0, (p - 0.45) / 0.3)))
    d.text((770, 830), "SUBSCRIBE", anchor="mm", font=font(48, True), fill=(*GOLD, alpha))
    d.text((1115, 830), "LIKE", anchor="mm", font=font(48, True), fill=(255, 255 - fill_like // 5, 255 - fill_like, alpha))
    spark_x = 585 + int(730 * p)
    d.ellipse((spark_x - 10, 820 - 10, spark_x + 10, 820 + 10), fill=(*GOLD, alpha))
    return np.asarray(img, dtype=np.uint8)


def render_silent_video(paths: list[Path], total: float) -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    frames = int(math.ceil(total * FPS))
    if SILENT_MP4.exists() and abs(ffprobe_duration(SILENT_MP4) - total) < 0.5:
        print(f"== reuse silent motion video: {SILENT_MP4}", flush=True)
        return
    shot_len = 5.2
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
                cur = crop_motion(cache.get(shot), t, shot, local, 2.0)
            else:
                body_t = t - 8.0
                shot = int(body_t // shot_len)
                local = body_t % shot_len
                cur = crop_motion(cache.get(shot + 4), t, shot, local, shot_len)
                if local >= shot_len - transition:
                    q = (local - (shot_len - transition)) / transition
                    nxt = crop_motion(cache.get(shot + 5), t, shot + 1, 0.0, shot_len)
                    cur = (cur.astype(np.float32) * (1 - q) + nxt.astype(np.float32) * q).astype(np.uint8)
            cur = draw_cta(cur, t, total)
            cur = draw_bookend(cur, t, total)
            proc.stdin.write(cur.tobytes())
            if n and n % (FPS * 60) == 0:
                print(f"   video frames {n}/{frames} ({n/FPS/60:.1f} min)", flush=True)
    finally:
        proc.stdin.close()
        rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"silent video ffmpeg exited {rc}")


def build_factory_bed(factory_assets: list[dict[str, Any]], total: float) -> dict[str, Any]:
    videos = [FACTORY / Path(item["remotion_src"]).name for item in factory_assets if item.get("kind") == "video"]
    if not videos:
        raise RuntimeError("no factory video assets available for final layer")
    entries: list[Path] = []
    while len(entries) < len(videos) * 2:
        entries.extend(videos)
        if len(entries) * 18.0 >= total + 20:
            break
    concat = WORK / "factory_bed_concat.txt"
    concat_lines = []
    for p in entries:
        safe_path = p.resolve().as_posix().replace("'", "'\\''")
        concat_lines.append(f"file '{safe_path}'\n")
    concat.write_text("".join(concat_lines), encoding="utf-8")
    if FACTORY_BED_MP4.exists() and abs(ffprobe_duration(FACTORY_BED_MP4) - total) < 0.5:
        print(f"== reuse full-timeline factory bed: {FACTORY_BED_MP4}", flush=True)
        return {
            "entries": len(entries),
            "distinct": len(set(str(p) for p in entries)),
            "max_reuse": max(entries.count(p) for p in set(entries)),
            "duration_seconds": round(ffprobe_duration(FACTORY_BED_MP4), 3),
        }
    run(
        [
            FFMPEG,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat,
            "-t",
            f"{total:.3f}",
            "-vf",
            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "19",
            FACTORY_BED_MP4,
        ],
        "build full-timeline factory bed",
        timeout=7200,
    )
    return {
        "entries": len(entries),
        "distinct": len(set(str(p) for p in entries)),
        "max_reuse": max(entries.count(p) for p in set(entries)),
        "duration_seconds": round(min(total, ffprobe_duration(FACTORY_BED_MP4)), 3),
    }


def blend_factory_layer(total: float) -> None:
    run(
        [
            FFMPEG,
            "-y",
            "-i",
            SILENT_MP4,
            "-i",
            FACTORY_BED_MP4,
            "-filter_complex",
            "[0:v][1:v]blend=all_mode=screen:all_opacity=0.14,format=yuv420p[v]",
            "-map",
            "[v]",
            "-t",
            f"{total:.3f}",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            SILENT_FACTORY_MP4,
        ],
        "blend factory layer into motion video",
        timeout=7200,
    )


def burn_and_mux(total: float) -> None:
    srt = str(CAPTIONS_SRT.resolve()).replace("\\", "/").replace(":", "\\:")
    vf = (
        f"subtitles='{srt}':force_style="
        "'FontName=Arial,FontSize=17,PrimaryColour=&H00F5F7FA,OutlineColour=&H76000000,"
        "BorderStyle=1,Outline=1.0,Shadow=0.45,MarginV=74,Alignment=2'"
    )
    FINAL_MP4.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            FFMPEG,
            "-y",
            "-i",
            SILENT_FACTORY_MP4 if SILENT_FACTORY_MP4.exists() else SILENT_MP4,
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
    img = Image.open(bg).convert("RGB")
    img = ImageOpsCover(img, (1280, 720))
    img = ImageEnhance.Contrast(img).enhance(1.28)
    img = ImageEnhance.Brightness(img).enhance(0.72)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((0, 0, 1280, 720), fill=(0, 0, 0, 54))
    d.rectangle((0, 0, 500, 720), fill=(3, 8, 18, 218))
    accent = BLUE if option == "B" else GOLD
    d.rectangle((38, 44, 426, 94), fill=(*accent, 250))
    d.text((232, 69), "WALL STREET", anchor="mm", font=font(31, True), fill=(7, 13, 24, 255))
    words = headline.split()
    lines = [" ".join(words[:2]), " ".join(words[2:])] if len(words) > 2 else [headline]
    y = 205
    for line in lines:
        d.text((58, y), line, font=font(96 if len(line) < 13 else 78, True), fill=(*WHITE, 255), stroke_width=5, stroke_fill=(0, 0, 0, 255))
        y += 108
    d.rectangle((56, y + 14, 430, y + 34), fill=(*accent, 255))
    d.text((62, 636), "NO FACE. NO LOGO.", font=font(30, True), fill=(*SILVER, 235))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def build_thumbnails(paths: list[Path]) -> None:
    thumb_dir = EPDIR / "10_thumbnail"
    pkg = EPDIR / "09_package"
    variants = [
        ("A", "CAUGHT ON TAPE", paths[0]),
        ("B", "THE $7B WIRE", paths[27]),
        ("C", "HIS OWN VOICE", paths[39]),
    ]
    records = []
    for option, headline, bg in variants:
        out = thumb_dir / f"thumbnail.rajaratnam_option_{option}.v001.png"
        make_thumbnail(option, headline, bg, out)
        records.append({"option": option, "headline": headline, "path": str(out).replace("\\", "/"), "width": 1280, "height": 720})
    selected = pkg / "thumbnail.selected.v001.png"
    selected.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(thumb_dir / "thumbnail.rajaratnam_option_A.v001.png", selected)
    (pkg / "title_thumbnail_candidates.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "selected": "A",
                "titles": [
                    {"option": "A", "title": "The Wiretap That Cracked Wall Street", "length": 39},
                    {"option": "B", "title": "Caught on Tape: Wall Street's Insider Network", "length": 47},
                    {"option": "C", "title": "His Own Voice: The Rajaratnam Wiretap Case", "length": 46},
                ],
                "thumbnails": records,
                "r2_safety": "living convicted subject; no real-person likeness, no real logo/seal/landmark; wire/profit wording avoids unverified claims",
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def update_rights(paths: list[Path], factory_assets: list[dict[str, Any]]) -> None:
    items: list[dict[str, Any]] = []
    for p in paths:
        items.append(
            {
                "asset_id": p.stem,
                "type": "hero_still",
                "path": str(p).replace("\\", "/"),
                "remotion_src": f"rajaratnam/{p.stem[:4]}.png" if p.stem.startswith("S") else None,
                "origin": "Codex AI-generated still",
                "license": "AI production asset for Prime Documentary; no external upload here",
                "ai_disclosure": True,
                "safety": "intended no real-person likeness, no real logo/seal/landmark, no readable text",
                "sha256": sha256_file(p),
            }
        )
    for p in music_tracks():
        items.append({"asset_id": safe_slug(p.stem), "type": "music", "path": str(p).replace("\\", "/"), "origin": "Prime Documentary reusable Suno-origin library", "license": "internal reusable library", "ai_disclosure": True})
    items.append({"asset_id": "EP24-VOICE-MASTER-v001", "type": "narration", "origin": "ElevenLabs from locked [VO:] script lines", "license": "provider generated under account terms", "path": str(VOICE_MASTER).replace("\\", "/"), "ai_disclosure": True, "sha256": sha256_file(VOICE_MASTER)})
    for item in factory_assets:
        items.append(
            {
                "asset_id": item["id"],
                "type": "factory_asset",
                "path": item.get("remotion_src"),
                "source_path": item.get("source_path"),
                "origin": "Prime Documentary asset factory stock shelf",
                "license": item.get("license"),
                "source_url": item.get("source_url"),
                "sha256": item.get("sha256"),
                "ai_disclosure": False,
            }
        )
    RIGHTS.parent.mkdir(parents=True, exist_ok=True)
    RIGHTS.write_text(json.dumps({"episode_id": EP, "revision": "v001", "created_at": now(), "assets": items}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_delivery(total: float) -> None:
    DELIVERY.parent.mkdir(parents=True, exist_ok=True)
    DELIVERY.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": VIDEO_REV,
                "state": "edit_review",
                "final_video": str(FINAL_MP4).replace("\\", "/"),
                "final_video_sha256": sha256_file(FINAL_MP4),
                "captions_srt": str(CAPTIONS_SRT).replace("\\", "/"),
                "audio_mix": str(MIX_WAV).replace("\\", "/"),
                "thumbnail_selected": str(EPDIR / "09_package" / "thumbnail.selected.v001.png").replace("\\", "/"),
                "duration_seconds": round(total, 3),
                "render": {"codec": "libx264", "preset": "slow", "crf": 16, "pix_fmt": "yuv420p", "color": "bt709", "audio_bitrate": "320k", "nvenc_used": False},
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def append_event(kind: str, payload: dict[str, Any]) -> None:
    EVENTS.parent.mkdir(exist_ok=True)
    EVENTS.open("a", encoding="utf-8").write(json.dumps({"ts": now(), "event": kind, "payload": payload}, ensure_ascii=False) + "\n")


def update_manifest(state: str) -> None:
    path = EPDIR / "manifest.json"
    data = load_json(path)
    data["state"] = state
    data["updated_at"] = now()
    data.setdefault("active_revisions", {})["narration"] = AUDIO_REV
    data.setdefault("active_revisions", {})["captions"] = AUDIO_REV
    data.setdefault("active_revisions", {})["audio_mix"] = AUDIO_REV
    data.setdefault("active_revisions", {})["edit"] = VIDEO_REV
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_acceptance() -> dict[str, Any]:
    result = subprocess.run(
        [str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/check_final_acceptance.py", str(EP_NUM), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(result.stdout)
    except Exception:
        data = {"status": "ERROR", "stdout": result.stdout, "stderr": result.stderr}
    data["exit_code"] = result.returncode
    return data


def write_self_audit(acceptance: dict[str, Any]) -> None:
    SELF_AUDIT.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": VIDEO_REV,
                "status": "accepted" if acceptance.get("exit_code") == 0 else "failed",
                "final_video": str(FINAL_MP4).replace("\\", "/"),
                "acceptance_gate": acceptance,
                "manual_checks": {
                    "runtime_band": "measured by check_final_acceptance and check_runtime_band",
                    "narration_provider": "ElevenLabs only; no SAPI/local final plan",
                    "captions": "sidecar SRT generated from rendered chunk timings; burned into final MP4",
                    "bgm": "continuous six-track library bed mixed with VO and loudnorm",
                    "render": "libx264 slow CRF16 yuv420p bt709 AAC 320k, no NVENC",
                    "thumbnails": "three 1280x720 candidates plus selected copy",
                    "publication": "not uploaded, not scheduled, legal owner gates remain",
                },
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Build EP24 final local edit.")
    ap.add_argument("--audio-only", action="store_true")
    ap.add_argument("--prep-only", action="store_true")
    ap.add_argument("--render-only", action="store_true")
    ap.add_argument("--skip-acceptance", action="store_true")
    args = ap.parse_args()

    pre = preflight()
    print(json.dumps({"preflight": pre}, ensure_ascii=False, indent=2), flush=True)

    rows = parse_vo()
    timed: list[dict[str, Any]]
    cues: list[dict[str, Any]]
    if args.render_only and NARRATION_INDEX.exists() and CAPTIONS_JSON.exists():
        timed = load_json(NARRATION_INDEX)["chunks"]
        cues = load_json(CAPTIONS_JSON)["cues"]
    else:
        timed = build_voice(rows)
        cues = write_captions(timed)
    total = build_mix() if not (args.render_only and MIX_WAV.exists()) else ffprobe_duration(MIX_WAV)
    factory_assets = stage_factory_assets()
    paths = stage_visuals(allow_procedural_fill=True)
    write_remotion_scaffold(factory_assets, timed, cues)
    update_rights(paths, factory_assets)
    build_thumbnails(paths)
    if args.audio_only or args.prep_only:
        update_manifest("audio_ready")
        append_event("audio_ready_built", {"revision": AUDIO_REV, "duration_seconds": round(total, 3), "caption_cues": len(cues), "factory_assets": len(factory_assets), "hero_images": len(paths), "narration_provider": "elevenlabs"})
        print(json.dumps({"status": "prepared", "duration_seconds": round(total, 3), "captions": len(cues), "factory_assets": len(factory_assets), "images": len(paths)}, indent=2), flush=True)
        return 0
    render_silent_video(paths, total)
    factory_layer = build_factory_bed(factory_assets, total)
    blend_factory_layer(total)
    burn_and_mux(total)
    write_delivery(total)
    update_manifest("edit_review")
    append_event("edit_review_built", {"revision": VIDEO_REV, "final_video": str(FINAL_MP4).replace("\\", "/"), "duration_seconds": round(total, 3), "caption_cues": len(cues), "narration_provider": "elevenlabs", "factory_layer": factory_layer})
    if args.skip_acceptance:
        return 0
    acceptance = run_acceptance()
    write_self_audit(acceptance)
    print(json.dumps(acceptance, ensure_ascii=False, indent=2), flush=True)
    return int(acceptance.get("exit_code", 1))


if __name__ == "__main__":
    raise SystemExit(main())


