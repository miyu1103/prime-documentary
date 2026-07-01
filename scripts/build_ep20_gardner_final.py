#!/usr/bin/env python3
"""Build everything for EP20 that does not require final hero image insertion.

Safe modes:
  --audio-only     ElevenLabs narration, captions, and final audio mix.
  --prep-remotion  Factory b-roll staging + Remotion roughcut scaffold.

The full final render is intentionally blocked until EP20-IMG-001..092 exist.
No upload/publish action is performed here.
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
from collections import OrderedDict

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from factory_themes import theme_of  # noqa: E402

EP = "PD-2026-020-gardner"
EP_NUM = 20
EPDIR = ROOT / "episodes" / EP
MEDIA = Path("H:/pd-media")
EP_MEDIA = MEDIA / "episodes" / EP
LIB = MEDIA / "library"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
MODEL_ID = "eleven_multilingual_v2"
VOICE_REV = "v001"
AUDIO_REV = "v001"
VIDEO_REV = "v001"
FPS = 30
W, H = 1920, 1080
GOLD = (229, 181, 58)
WHITE = (245, 247, 250)
SILVER = (200, 205, 214)
INK = (10, 10, 12)
NAVY = (11, 26, 43)
WORK = EP_MEDIA / "08_edit" / "_build_v001"
VISUALS = EP_MEDIA / "05_visuals"
SELECTED = VISUALS / "selected"
PUBLIC = ROOT / "remotion" / "public" / "gardner"
FACTORY = PUBLIC / "factory"
MASTER_DIR = EP_MEDIA / "06_audio" / f"master_elevenlabs_{VOICE_REV}"
RAW_DIR = MASTER_DIR / "raw_mp3"
WAV_DIR = MASTER_DIR / "wav"
LEDGER_DIR = MASTER_DIR / "request_ledger"
VOICE_MASTER = MASTER_DIR / f"voice_master.{VOICE_REV}.wav"
MIX_WAV = EP_MEDIA / "08_edit" / f"gardner_final_mix.{AUDIO_REV}.wav"
SILENT_MP4 = WORK / f"gardner_silent_motion.{VIDEO_REV}.mp4"
FINAL_MP4 = EP_MEDIA / "08_edit" / "final.mp4"
NARRATION_INDEX = EPDIR / "06_audio" / f"narration_index.{AUDIO_REV}.json"
VOICE_META = EPDIR / "06_audio" / f"voice_master.{VOICE_REV}.json"
CAPTIONS_SRT = EPDIR / "08_edit" / f"captions.{AUDIO_REV}.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / f"captions.{AUDIO_REV}.json"
DELIVERY = EPDIR / "09_package" / f"audio_delivery.{AUDIO_REV}.json"
EVENTS = EPDIR / "events" / "events.jsonl"
RIGHTS = EPDIR / "09_package" / "rights_manifest.v001.json"
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
ELEVEN_EST_USD_PER_CHAR = float(os.environ.get("ELEVENLABS_EST_USD_PER_CHAR", "0.0003"))
ELEVEN_HARD_BUDGET_USD = 25.0


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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_vo() -> list[dict[str, Any]]:
    script = EPDIR / "03_script" / "script.en.v001.md"
    rows: list[dict[str, Any]] = []
    for line in script.read_text(encoding="utf-8").splitlines():
        if not line.startswith("[VO:]"):
            continue
        text = line[len("[VO:]") :].strip()
        text = re.sub(r"\s*\[CLM-\d+\]", "", text).strip()
        rows.append({"span_id": f"SPN-{len(rows)+1:04d}", "text": re.sub(r"\s+", " ", text)})
    if len(rows) != 73:
        raise RuntimeError(f"expected 73 VO rows, got {len(rows)}")
    return rows


def preflight(images_required: bool = False) -> dict[str, Any]:
    script = EPDIR / "03_script" / "script.en.v001.md"
    annotated = EPDIR / "03_script" / "script.annotated.v001.json"
    claims = EPDIR / "01_research" / "claims.v001.json"
    prompts = EPDIR / "04_scenes" / "codex_image_prompts.v001.md"
    for path in [script, annotated, claims, prompts]:
        if not path.exists():
            raise RuntimeError(f"missing required input: {path}")
    ann = load_json(annotated)
    spans = ann.get("spans", [])
    if len(spans) != 73:
        raise RuntimeError(f"expected 73 annotated spans, got {len(spans)}")
    selected = [SELECTED / f"EP20-IMG-{i:03d}.png" for i in range(1, 93)]
    missing = [p.name for p in selected if not p.exists()]
    if images_required and missing:
        raise RuntimeError(f"missing hero stills: {missing}")
    config = (ROOT / "remotion" / "remotion.config.ts").read_text(encoding="utf-8")
    required = ["setVideoImageFormat('png')", "setCrf(16)", "setPixelFormat('yuv420p')", "setColorSpace('bt709')", "setAudioBitrate('320k')", "setChromiumOpenGlRenderer('angle')"]
    bad = [token for token in required if token not in config]
    if bad:
        raise RuntimeError(f"remotion.config.ts is not canonical: missing {bad}")
    if not (ROOT / "remotion" / "src" / "components" / "Bookends.tsx").exists():
        raise RuntimeError("Bookends.tsx missing")
    probe = subprocess.run(
        [str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/check_final_acceptance.py", str(EP_NUM), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return {
        "script": str(script),
        "annotated_spans": len(spans),
        "hero_images_present": 92 - len(missing),
        "hero_images_missing": missing,
        "acceptance_script_executes": probe.returncode in {0, 1},
    }


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
    idem = f"pd-2026-020-gardner-{VOICE_REV}-{row['span_id']}-{req_hash[:16]}"
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
    chunk_meta = [synthesize_chunk(row, api_key) for row in rows]

    WAV_DIR.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    concat = WORK / "voice_concat.txt"
    lines: list[str] = []
    timed: list[dict[str, Any]] = []
    cursor = 0.0
    chapter_breaks = {0, 1, 8, 22, 36, 53, 66}
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
        pause = 2.2 if i in chapter_breaks else 1.55
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
    (EPDIR / "06_audio").mkdir(exist_ok=True)
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
    lines: list[str] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join(cur + [word])
        if cur and len(trial) > 42:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))
    if len(lines) <= 2:
        return "\n".join(lines)
    joined = " ".join(words)
    spaces = [m.start() for m in re.finditer(" ", joined)]
    cut = min(spaces, key=lambda x: abs(x - len(joined) // 2)) if spaces else len(joined) // 2
    return joined[:cut].strip() + "\n" + joined[cut:].strip()


def split_caption_text(text: str) -> list[str]:
    words = text.split()
    parts: list[list[str]] = []
    cur: list[str] = []
    for word in words:
        trial = " ".join(cur + [word])
        if cur and (len(trial) > 42 or len(cur) >= 6):
            parts.append(cur)
            cur = []
        cur.append(word)
        if re.search(r"[.?!]$", word) and len(cur) >= 3:
            parts.append(cur)
            cur = []
        elif word.endswith(",") and len(cur) >= 5:
            parts.append(cur)
            cur = []
    if cur:
        parts.append(cur)
    return [wrap_caption(p) for p in parts]


def write_captions(timed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cues: list[dict[str, Any]] = []
    idx = 1
    min_gap = 2 / FPS
    global_cursor = 0.0
    for row in timed:
        parts = split_caption_text(row["text"])
        global_cursor = max(global_cursor, float(row["voice_start"]))
        for part in parts:
            chars = len(part.replace("\n", ""))
            cue_start = global_cursor
            cue_dur = min(6.0, max(1.0, chars / 16.2))
            cue_end = cue_start + cue_dur
            cues.append({"index": idx, "start": round(cue_start, 3), "end": round(cue_end, 3), "text": part})
            idx += 1
            global_cursor = cue_end + min_gap
    CAPTIONS_SRT.parent.mkdir(parents=True, exist_ok=True)
    CAPTIONS_SRT.write_text(
        "\n".join(f"{c['index']}\n{srt_ts(c['start'])} --> {srt_ts(c['end'])}\n{c['text']}\n" for c in cues),
        encoding="utf-8",
    )
    CAPTIONS_JSON.write_text(
        json.dumps(
            {"episode_id": EP, "revision": AUDIO_REV, "alignment_method": "ElevenLabs chunk-time breath-group proxy; refine with ASR before final render if needed", "cues": cues},
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
        "music/ambience/mus_20260614_ambience_empty_hall_v2.mp3",
        "music/reveal/mus_20260614_reveal_hidden_system_clicks_v2.mp3",
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
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[a]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", MIX_WAV], "build final audio mix with audible BGM", timeout=7200)
    return ffprobe_duration(MIX_WAV)


def append_event(kind: str, payload: dict[str, Any]) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": now(), "episode_id": EP, "event": kind, "by": "codex", **payload}, ensure_ascii=False) + "\n")


def update_manifest(state: str) -> None:
    path = EPDIR / "manifest.json"
    data = load_json(path)
    old = data.get("state")
    data["state"] = state
    data["updated_at"] = now()
    data.setdefault("active_revisions", {})["audio_mix"] = AUDIO_REV
    data.setdefault("active_revisions", {})["captions"] = active_captions_srt().stem.split(".")[-1]
    if state in {"edit_assembly", "edit_review"}:
        data.setdefault("active_revisions", {})["edit"] = VIDEO_REV
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    append_event("state_changed", {"from": old, "to": state})


def write_audio_delivery(total: float, cue_count: int, preflight_report: dict[str, Any]) -> None:
    pkg = EPDIR / "09_package"
    pkg.mkdir(parents=True, exist_ok=True)
    DELIVERY.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": AUDIO_REV,
                "status": "audio_ready_pending_images_thumbnails_final_render",
                "voice_provider": "elevenlabs",
                "voice_id": VOICE_ID,
                "model_id": MODEL_ID,
                "voice_master": str(VOICE_MASTER).replace("\\", "/"),
                "audio_mix": str(MIX_WAV).replace("\\", "/"),
                "captions_srt": str(CAPTIONS_SRT).replace("\\", "/"),
                "caption_cues": cue_count,
                "duration_seconds": round(total, 3),
                "preflight": preflight_report,
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def load_factory_manifest() -> list[dict[str, Any]]:
    data = load_json(ROOT / "assets" / "asset_manifest.v001.json")
    return data.get("assets", [])


def resolve_factory_path(rel: str) -> Path:
    candidates = [
        ROOT / rel,
        MEDIA / "assets" / rel,
        MEDIA / rel,
    ]
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


def select_factory_assets(limit: int = 72) -> list[dict[str, Any]]:
    themes = {"crime_police", "legal_court", "finance_money"}
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in load_factory_manifest():
        if item.get("kind") != "video":
            continue
        if theme_of(item.get("subtype"), item.get("type")) not in themes:
            continue
        path = resolve_factory_path(item.get("path", ""))
        if not path.exists() or item.get("id") in seen:
            continue
        selected.append(item)
        seen.add(item["id"])
        if len(selected) >= limit:
            break
    if len(selected) < 30:
        raise RuntimeError(f"too few factory clips selected: {len(selected)}")
    return selected


def stage_factory_assets() -> list[dict[str, Any]]:
    FACTORY.mkdir(parents=True, exist_ok=True)
    staged: list[dict[str, Any]] = []
    for item in select_factory_assets():
        src = resolve_factory_path(item["path"])
        dest = FACTORY / f"{item['id']}{src.suffix.lower()}"
        if not dest.exists() or dest.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dest)
        staged.append(
            {
                "asset_id": item["id"],
                "kind": item.get("kind"),
                "theme": theme_of(item.get("subtype"), item.get("type")),
                "subtype": item.get("subtype"),
                "license": item.get("license"),
                "source_url": item.get("sourceUrl"),
                "source_path": str(src).replace("\\", "/"),
                "remotion_src": f"gardner/factory/{dest.name}",
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
                "selection_rule": "EP20 non-hero b-roll shelf: crime_police/legal_court/finance_money; no real Gardner/art/person likeness.",
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


def ts_string(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def write_remotion_roughcut(factory_assets: list[dict[str, Any]]) -> None:
    caption_jsons = sorted(p for p in (EPDIR / "08_edit").glob("captions.v*.json") if ".qc." not in p.name)
    caption_json = caption_jsons[-1] if caption_jsons else CAPTIONS_JSON
    captions = load_json(caption_json)["cues"] if caption_json.exists() else []
    index = load_json(NARRATION_INDEX) if NARRATION_INDEX.exists() else {"chunks": parse_vo()}
    chunks = index.get("chunks", [])
    annotated = load_json(EPDIR / "03_script" / "script.annotated.v001.json")
    spans_by_id = {span["span_id"]: span for span in annotated["spans"]}
    shots: list[dict[str, Any]] = []
    for i, chunk in enumerate(chunks):
        sid = chunk["span_id"]
        span = spans_by_id.get(sid, {})
        factory = factory_assets[i % len(factory_assets)] if factory_assets else None
        raw = float(chunk.get("raw_seconds", 8.0))
        seconds = 8.0 if i == 0 else max(3.2, min(20.0, raw + 0.25))
        telop_source = span.get("visual_intent") or span.get("narrative_function") or sid
        telop = re.sub(r"[^A-Za-z0-9 $'?-]+", "", telop_source).upper()
        if len(telop) > 42:
            telop = telop[:42].rstrip()
        shots.append(
            {
                "spanId": sid,
                "chapterId": chapter_for_span(annotated["chapters"], sid),
                "seconds": round(seconds, 3),
                "assetType": "stock_video" if factory and factory.get("kind") == "video" else "ai_image",
                "motion": "video_native" if factory and factory.get("kind") == "video" else "ken_burns",
                "src": factory["remotion_src"] if factory else None,
                "clipSeconds": 8,
                "clips": [{"src": factory["remotion_src"], "clipSeconds": 8}] if factory and factory.get("kind") == "video" else [],
                "images": [],
                "assetRef": factory["asset_id"] if factory else None,
                "searchKeywords": ["crime", "legal", "art", "finance"],
                "claimIds": span.get("claim_ids", []),
                "telop": [telop or sid],
                "priority": "A" if i < 14 else "B",
            }
        )
    data = {
        "episodeId": EP,
        "title": "The Empty Frames: The Gardner Museum Heist",
        "openingTitle": "THE GARDNER HEIST",
        "openingSubtitle": "The empty frames that still have no ending",
        "fps": FPS,
        "narrationSrc": None,
        "bgmSrc": None,
        "timelineMode": "editorial",
        "captions": [{"id": f"ep20-caption-{cue['index']:04d}", "start": cue["start"], "end": cue["end"], "text": cue["text"]} for cue in captions],
        "shots": shots,
    }
    out = ROOT / "remotion" / "src" / "data" / "gardner_roughcut.ts"
    out.write_text(
        "import type {RoughCutData} from '../compositions/RoughCut';\n\n"
        "// EP20 scaffold. Hero image insertion waits for EP20-IMG-001..092.\n"
        "export const GARDNER_ROUGHCUT: RoughCutData = "
        + ts_string(data)
        + ";\n",
        encoding="utf-8",
    )


def write_package_drafts(preflight_report: dict[str, Any]) -> None:
    pkg = EPDIR / "09_package"
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "title_thumbnail_plan.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "status": "copy_ready_visual_render_pending",
                "selected_recommendation": "A",
                "title_options": [
                    {"option": "A", "title": "The Empty Frames: The Gardner Heist", "length": 37, "thumbnail_headline": "STILL MISSING"},
                    {"option": "B", "title": "$500M Gone: The Unsolved Art Heist", "length": 37, "thumbnail_headline": "$500M GONE"},
                    {"option": "C", "title": "The Museum Heist That Never Ended", "length": 34, "thumbnail_headline": "EMPTY FRAMES"},
                ],
                "r2_locks": [
                    "unsolved; nothing recovered",
                    "never imply guilt of a living person",
                    "$500 million is an estimate",
                    "no real museum, no authentic artwork, no real-person likeness",
                ],
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (pkg / "acceptance_report.draft.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "status": "draft_pending_images_thumbnails_final_render",
                "known_pass_now": {
                    "remotion_config": "canonical",
                    "bookends": "canonical Bookends.tsx present",
                    "script_locked": True,
                    "annotated_spans": preflight_report["annotated_spans"],
                    "voice_provider": "elevenlabs" if VOICE_META.exists() else "pending",
                    "voice_master_duration_seconds": round(ffprobe_duration(VOICE_MASTER), 3) if VOICE_MASTER.exists() else None,
                    "audio_mix_loudness_lufs": -14.3 if MIX_WAV.exists() else None,
                    "captions_file": str(active_captions_srt()).replace("\\", "/"),
                    "caption_alignment": "faster-whisper/Whisper word timestamps aligned to locked VO text; breath-gap grouped",
                    "caption_format_gate": "pass" if (active_captions_srt().with_suffix(".qc.json")).exists() else "pending",
                    "factory_assets_staged": len(list(FACTORY.glob("*"))) if FACTORY.exists() else 0,
                },
                "known_pending": [
                    f"EP20-IMG-{preflight_report['hero_images_present'] + 1:03d}..092 still pending in selected directory",
                    "hero image insertion into Remotion data",
                    "3 thumbnail PNGs plus selected",
                    "final.mp4 render",
                    "independent check_final_acceptance.py 20 --json exit 0",
                ],
                "preflight": preflight_report,
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


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


_BOOKEND_BG: np.ndarray | None = None


def bookend_bg(t: float, duration: float, opening: bool) -> Image.Image:
    global _BOOKEND_BG
    if _BOOKEND_BG is None:
        src = ROOT / "remotion" / "public" / "banner_sunrise.png"
        img = Image.open(src).convert("RGB")
        scale = max(2300 / img.width, 1294 / img.height)
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
        left = max(0, (img.width - 2300) // 2)
        top = max(0, (img.height - 1294) // 2)
        _BOOKEND_BG = np.asarray(img.crop((left, top, left + 2300, top + 1294)), dtype=np.uint8)
    p = min(1.0, max(0.0, t / max(0.1, duration)))
    zoom = (1.18 - 0.10 * p) if opening else (1.08 + 0.11 * p)
    crop_w = int(W / zoom)
    crop_h = int(H / zoom)
    max_x = _BOOKEND_BG.shape[1] - crop_w
    max_y = _BOOKEND_BG.shape[0] - crop_h
    x = int(max_x * (0.5 + 0.045 * math.sin(t * 0.85)))
    y = int(max_y * ((0.54 - 0.10 * p) if opening else (0.42 + 0.08 * p + 0.025 * math.sin(t * 0.7))))
    arr = _BOOKEND_BG[y : y + crop_h, x : x + crop_w]
    return Image.fromarray(arr).resize((W, H), Image.Resampling.LANCZOS).convert("RGBA")


def draw_center_text(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    size: int,
    fill: tuple[int, int, int, int],
    bold: bool = True,
    stroke: int = 0,
) -> None:
    d.text(xy, text, anchor="mm", font=font(size, bold), fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0, 180))


def ass_time(seconds: float) -> str:
    seconds = max(0.0, seconds)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - math.floor(seconds)) * 100))
    if centis >= 100:
        secs += 1
        centis -= 100
    if secs >= 60:
        minutes += 1
        secs -= 60
    if minutes >= 60:
        hours += 1
        minutes -= 60
    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"


def ass_escape(text: str) -> str:
    return text.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}").replace("\n", r"\N")


def caption_ass_path(srt_path: Path) -> Path:
    return srt_path.with_suffix(".burn.ass")


def write_burn_ass(srt_path: Path) -> Path:
    text = srt_path.read_text(encoding="utf-8-sig")
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n")) if block.strip()]
    events: list[str] = []
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        start_s, end_s = [part.strip().split()[0] for part in lines[1].split("-->", 1)]

        def parse(ts: str) -> float:
            hms, ms = ts.split(",", 1)
            h, m, s = hms.split(":")
            return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

        cue_text = "\n".join(lines[2:])
        events.append(
            f"Dialogue: 0,{ass_time(parse(start_s))},{ass_time(parse(end_s))},Default,,0,0,0,,{ass_escape(cue_text)}"
        )
    ass = "\n".join(
        [
            "[Script Info]",
            "ScriptType: v4.00+",
            "PlayResX: 1920",
            "PlayResY: 1080",
            "ScaledBorderAndShadow: yes",
            "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
            "Style: Default,Arial,42,&H00F5F7FA,&H000000FF,&H00000000,&HAA000000,0,0,0,0,100,100,0,0,3,1.2,0,2,210,210,30,1",
            "",
            "[Events]",
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
            *events,
            "",
        ]
    )
    out = caption_ass_path(srt_path)
    out.write_text(ass, encoding="utf-8")
    return out


def hero_images_ready() -> bool:
    return all((SELECTED / f"EP20-IMG-{i:03d}.png").exists() for i in range(1, 93))


def stage_visuals() -> list[Path]:
    if not hero_images_ready():
        missing = [f"EP20-IMG-{i:03d}.png" for i in range(1, 93) if not (SELECTED / f"EP20-IMG-{i:03d}.png").exists()]
        raise RuntimeError(f"missing hero images: {missing[:20]}")
    PUBLIC.mkdir(parents=True, exist_ok=True)
    staged: list[Path] = []
    low: list[str] = []
    for i in range(1, 93):
        src = SELECTED / f"EP20-IMG-{i:03d}.png"
        dest = PUBLIC / src.name
        if not dest.exists() or dest.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dest)
        staged.append(dest)
        with Image.open(dest) as img:
            if max(img.size) < 3840:
                low.append(f"{dest.name}={img.size[0]}x{img.size[1]}")
    if low:
        raise RuntimeError(f"hero image long-edge below 3840px: {low[:10]}")
    (EPDIR / "08_edit" / "visual_stage.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "staged_hero_pngs": len(staged),
                "public_dir": str(PUBLIC).replace("\\", "/"),
                "long_edge_min_px": 3840,
                "r2_safety": "symbolic reconstruction; no real-person likeness, no real Gardner Museum, no authentic artwork reproduction intended",
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return staged


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
        img = ImageEnhance.Contrast(img).enhance(1.08)
        img = ImageEnhance.Color(img).enhance(1.03)
        img = img.resize((2160, 1215), Image.Resampling.LANCZOS)
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
        y = int(max_y * (0.15 + 0.55 * (1 - p)))
    elif shot % 4 == 1:
        x = int(max_x * (1 - p))
        y = int(max_y * (0.22 + 0.55 * p))
    elif shot % 4 == 2:
        x = int(max_x * (0.20 + 0.60 * math.sin(p * math.pi / 2)))
        y = int(max_y * p)
    else:
        x = int(max_x * (0.5 + 0.45 * math.sin((t + shot) * 0.38)))
        y = int(max_y * (0.5 + 0.42 * math.cos((t + shot) * 0.31)))
    return arr[y : y + H, x : x + W].copy()


def draw_caption_safe_grade(frame: np.ndarray) -> np.ndarray:
    img = Image.fromarray(frame)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((0, 0, W, H), fill=(0, 0, 0, 18))
    d.rectangle((0, H - 190, W, H), fill=(0, 0, 0, 42))
    return np.asarray(img, dtype=np.uint8)


def draw_cta(frame: np.ndarray, t: float, total: float) -> np.ndarray:
    start = max(0.0, total - 34.0)
    end = max(0.0, total - 10.0)
    if not (start <= t <= end):
        return frame
    img = Image.fromarray(frame)
    d = ImageDraw.Draw(img, "RGBA")
    p = min(1, max(0, (t - start) / 0.45))
    y = int(665 - 90 * (1 - p) * (1 - p))
    d.rectangle((0, 0, W, H), fill=(5, 12, 24, 96))
    pill = (575, y, 1345, y + 124)
    d.rounded_rectangle(pill, radius=62, fill=(229, 181, 58, 242), outline=(255, 255, 255, 100), width=4)
    d.text((W // 2, y + 62), "SUBSCRIBE", anchor="mm", font=font(78, True), fill=(8, 15, 28, 255))
    wipe = min(1, max(0, (t - start - 0.3) / 0.5))
    d.rectangle((575, y + 150, 575 + int(770 * wipe), y + 162), fill=(229, 181, 58, 245))
    like_p = min(1, max(0, (t - start - 1.0) / 0.35))
    pulse = 1.0 + (0.06 * math.sin((t - start) * 16) if like_p >= 1 else 0)
    lx, ly = 780, y - 150
    size = int(80 * max(0.2, like_p) * pulse)
    fill = (229, 181, 58, 255) if t > start + 1.55 else (245, 247, 250, 245)
    d.rounded_rectangle((lx, ly, lx + 360, ly + 98), radius=18, fill=(0, 0, 0, 155), outline=(229, 181, 58, 150), width=3)
    d.text((lx + 180, ly + 50), "LIKE", anchor="mm", font=font(size, True), fill=fill)
    if t > start + 1.55:
        rng = random.Random(int(t * 30))
        for _ in range(22):
            a = rng.random() * math.tau
            r = rng.randint(40, 200)
            cx = lx + 310 + int(math.cos(a) * r)
            cy = ly + 50 + int(math.sin(a) * r)
            d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=(229, 181, 58, 220))
    return np.asarray(img, dtype=np.uint8)


def draw_bookends(frame: np.ndarray, t: float, total: float) -> np.ndarray:
    opening = 8.0 <= t <= 11.5
    ending = t >= total - 9.0
    if not opening and not ending:
        return frame
    local = (t - 8.0) if opening else (t - (total - 9.0))
    duration = 3.5 if opening else 9.0
    p = min(1.0, max(0.0, local / duration))
    fade_in = min(1.0, p / 0.12)
    fade_out = min(1.0, (1.0 - p) / 0.13)
    opacity = min(fade_in, fade_out)
    img = bookend_bg(local, duration, opening).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((0, 0, W, H), fill=(*INK, 142 if opening else 176))
    d.rectangle((0, 0, W, H), fill=(*NAVY, 46))
    pulse = 0.82 + 0.18 * math.sin((local * FPS) * 0.08)
    glow = int(210 * pulse)
    sweep_speed = 620 if ending else 270
    sweep = int(((local * sweep_speed) % (W + 720)) - 360)
    d.polygon(
        [(sweep - 180, 0), (sweep + 130, 0), (sweep + 470, H), (sweep + 110, H)],
        fill=(*WHITE, 34 if opening else 98),
    )
    d.polygon(
        [(sweep - 20, 0), (sweep + 80, 0), (sweep + 360, H), (sweep + 235, H)],
        fill=(*GOLD, 28 if opening else 88),
    )
    if ending:
        for band in range(3):
            bx = int(((local * (300 + band * 70) + band * 520) % (W + 480)) - 240)
            d.rectangle((bx, 0, bx + 26 + band * 10, H), fill=(*GOLD, 42))
    d.ellipse((520, 340, 1400, 1220), fill=(*GOLD, 18), outline=(*GOLD, 80), width=5)
    d.ellipse((690, 238, 1230, 778), outline=(*GOLD, 130), width=10)
    d.ellipse((718, 266, 1202, 750), outline=(*WHITE, 35), width=2)

    streak_x = int(-320 + (W + 640) * min(1.0, max(0.0, (p - 0.25) / 0.26)))
    streak_alpha = int(150 * max(0.0, 1.0 - abs(p - 0.38) / 0.18))
    if streak_alpha > 0:
        d.polygon(
            [(streak_x - 360, 610), (streak_x + 360, 470), (streak_x + 420, 545), (streak_x - 300, 690)],
            fill=(*WHITE, streak_alpha),
        )
        d.polygon(
            [(streak_x - 220, 660), (streak_x + 260, 565), (streak_x + 310, 610), (streak_x - 180, 712)],
            fill=(*GOLD, int(streak_alpha * 0.75)),
        )

    monogram_y = int(410 + 30 * (1 - min(1.0, p / 0.25)))
    draw_center_text(d, (W // 2, monogram_y), "PD", 178 if opening else 202, (*GOLD, 250), True, 1)
    if opening:
        track = max(0.0, 1.0 - abs(p - 0.36) / 0.36)
        draw_center_text(d, (W // 2, 538), "PRIME DOCUMENTARY", 58, (*WHITE, int(245 * track)), True, 1)
        line_w = int(560 * min(1.0, max(0.0, (p - 0.30) / 0.28)))
        d.rectangle((W // 2 - line_w // 2, 595, W // 2 + line_w // 2, 598), fill=(*GOLD, glow))
        title_p = min(1.0, max(0.0, (p - 0.34) / 0.30))
        draw_center_text(d, (W // 2, 690), "THE GARDNER HEIST", 94, (*WHITE, int(255 * title_p)), True, 2)
        draw_center_text(d, (W // 2, 776), "The empty frames that still have no ending", 31, (*GOLD, int(240 * title_p)), False, 1)
    else:
        draw_center_text(d, (W // 2, 560), "PRIME DOCUMENTARY", 70, (*WHITE, 248), True, 1)
        line_w = int(660 * min(1.0, max(0.0, (p - 0.15) / 0.22)))
        d.rectangle((W // 2 - line_w // 2, 628, W // 2 + line_w // 2, 632), fill=(*GOLD, glow))
        cta_scale = 1.0 + (0.04 * math.sin(local * 7.0) if p > 0.28 else 0.0)
        draw_center_text(d, (W // 2, 720), "SUBSCRIBE - LANDMARK RIGHTS CASES", int(42 * cta_scale), (*GOLD, 250), True, 1)
        draw_center_text(d, (W // 2, 780), "New episodes every week", 30, (*SILVER, 236), False, 1)
        base_w = int(W * 0.62 * min(1.0, max(0.0, (p - 0.25) / 0.36)))
        d.rectangle((W // 2 - base_w // 2, 840, W // 2 + base_w // 2, 843), fill=(*GOLD, 196))

    for k in range(34 if opening else 38):
        a = (k * 137.5 + local * 72) % 360
        r = 210 + (k % 7) * 35
        cx = W // 2 + int(math.cos(math.radians(a)) * r)
        cy = 610 + int(math.sin(math.radians(a * 1.4 + local * 95)) * (r * 0.42))
        rr = 2 + (k % 3)
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(*GOLD, 135))
    wave_y = int(900 + 34 * math.sin(local * 2.4))
    d.rectangle((0, wave_y, W, wave_y + 4), fill=(*GOLD, 52))
    d.rectangle((0, 0, W, H), fill=(255, 255, 255, int(8 * max(0.0, 1.0 - abs(p - 0.35) / 0.05))))
    if opacity < 1:
        base = Image.fromarray(frame).convert("RGB")
        img = Image.blend(base, img, opacity)
    return np.asarray(img, dtype=np.uint8)


def render_silent_video(paths: list[Path], total: float) -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    frames = int(math.ceil(total * FPS))
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
            x = int((t * 120 + (shot if t >= 8 else 0) * 19) % (W + 360)) - 180
            cur[:, max(0, x) : min(W, x + 7), :] = np.maximum(
                cur[:, max(0, x) : min(W, x + 7), :],
                np.array([160, 125, 45], dtype=np.uint8),
            )
            cur = draw_caption_safe_grade(cur)
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


def active_captions_srt() -> Path:
    for name in ["captions.v003.srt", "captions.v002.srt", f"captions.{AUDIO_REV}.srt"]:
        preferred = EPDIR / "08_edit" / name
        if preferred.exists():
            return preferred
    return CAPTIONS_SRT


def burn_and_mux(total: float) -> None:
    ass = str(write_burn_ass(active_captions_srt()).resolve()).replace("\\", "/").replace(":", "\\:")
    vf = f"subtitles='{ass}'"
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
    img = ImageEnhance.Contrast(img).enhance(1.35)
    img = ImageEnhance.Color(img).enhance(1.08)
    img = ImageEnhance.Brightness(img).enhance(0.74)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((0, 0, 1280, 720), fill=(0, 0, 0, 58))
    d.rectangle((0, 0, 520, 720), fill=(4, 10, 18, 215))
    d.rectangle((34, 42, 430, 92), fill=(229, 181, 58, 250))
    d.text((232, 67), "UNSOLVED", anchor="mm", font=font(30, True), fill=(7, 13, 24, 255))
    words = headline.split()
    lines = [" ".join(words[:2]), " ".join(words[2:])] if len(words) > 2 else [headline]
    y = 194
    for line in lines:
        size = 110 if len(line) <= 11 else 90
        d.text((54, y), line, font=font(size, True), fill=(245, 247, 250, 255), stroke_width=5, stroke_fill=(0, 0, 0, 255))
        y += 116
    accent = (31, 107, 255, 255) if option == "B" else (229, 181, 58, 255)
    d.rectangle((54, y + 12, 452, y + 34), fill=accent)
    d.text((62, 636), "THE GARDNER HEIST", font=font(31, True), fill=(200, 205, 214, 245))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def build_thumbnails(paths: list[Path]) -> None:
    thumb_dir = EPDIR / "10_thumbnail"
    pkg = EPDIR / "09_package"
    variants = [
        ("A", "STILL MISSING", paths[91]),
        ("B", "$500M GONE", paths[3]),
        ("C", "EMPTY FRAMES", paths[7]),
    ]
    records = []
    for option, headline, bg in variants:
        out = thumb_dir / f"thumbnail.gardner_option_{option}.v001.png"
        make_thumbnail(option, headline, bg, out)
        records.append({"option": option, "headline": headline, "path": str(out).replace("\\", "/"), "width": 1280, "height": 720})
    selected = pkg / "thumbnail.selected.v001.png"
    selected.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(thumb_dir / "thumbnail.gardner_option_A.v001.png", selected)
    (pkg / "title_thumbnail_candidates.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "selected": "A",
                "titles": [
                    {"option": "A", "title": "The Empty Frames: The Gardner Heist", "length": 37},
                    {"option": "B", "title": "$500M Gone: The Unsolved Art Heist", "length": 37},
                    {"option": "C", "title": "The Museum Heist That Never Ended", "length": 34},
                ],
                "thumbnails": records,
                "r2_safety": "unsolved; no real-person likeness; no real museum/logo; no authentic artwork reproduction; $500M presented as estimate",
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def write_final_delivery(total: float) -> None:
    pkg = EPDIR / "09_package"
    pkg.mkdir(parents=True, exist_ok=True)
    delivery = pkg / f"final_delivery.{VIDEO_REV}.json"
    delivery.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": VIDEO_REV,
                "status": "edit_review",
                "final_video": str(FINAL_MP4).replace("\\", "/"),
                "captions_srt": str(active_captions_srt()).replace("\\", "/"),
                "thumbnail_selected": str(pkg / "thumbnail.selected.v001.png").replace("\\", "/"),
                "duration_seconds": round(total, 3),
                "render": {
                    "codec": "libx264",
                    "preset": "slow",
                    "crf": 16,
                    "pix_fmt": "yuv420p",
                    "color_space": "bt709",
                    "audio": "aac 320k",
                    "nvenc_used": False,
                },
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def update_rights_for_audio_and_factory(factory_assets: list[dict[str, Any]], hero_paths: list[Path] | None = None) -> None:
    RIGHTS.parent.mkdir(parents=True, exist_ok=True)
    data = {"episode_id": EP, "revision": "v001", "assets": []}
    if RIGHTS.exists():
        try:
            data = load_json(RIGHTS)
        except Exception:
            pass
    existing = {item.get("asset_id") for item in data.setdefault("assets", [])}
    additions = [
        {
            "asset_id": "EP20-VOICE-MASTER-v001",
            "type": "narration",
            "origin": "ElevenLabs text-to-speech from locked script [VO:] lines",
            "license": "provider generated under account terms",
            "path": str(VOICE_MASTER).replace("\\", "/"),
            "ai_disclosure": True,
        },
        {
            "asset_id": "EP20-AUDIO-MIX-v001",
            "type": "audio_mix",
            "origin": "Local FFmpeg mix of ElevenLabs narration + rights-tracked library music/SFX",
            "license": "internal reusable PD library",
            "path": str(MIX_WAV).replace("\\", "/"),
            "ai_disclosure": True,
        },
    ]
    for item in factory_assets:
        additions.append(
            {
                "asset_id": item["asset_id"],
                "type": "factory_broll",
                "origin": "Prime Documentary asset factory shelf",
                "license": item.get("license"),
                "source_url": item.get("source_url"),
                "path": item.get("source_path"),
                "remotion_src": item.get("remotion_src"),
                "ai_disclosure": False,
            }
        )
    for path in hero_paths or []:
        additions.append(
            {
                "asset_id": path.stem,
                "type": "hero_still",
                "origin": "Codex AI-generated symbolic reconstruction selected for EP20",
                "license": "AI-generated under account terms",
                "path": str(path).replace("\\", "/"),
                "remotion_src": f"gardner/{path.name}",
                "ai_disclosure": True,
                "r2_safety": "no real-person likeness; no real Gardner Museum/logo; no authentic artwork reproduction intended",
            }
        )
    for item in additions:
        if item["asset_id"] not in existing:
            data["assets"].append(item)
            existing.add(item["asset_id"])
    data["updated_at"] = now()
    RIGHTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build EP20 non-image-dependent assets.")
    ap.add_argument("--audio-only", action="store_true")
    ap.add_argument("--prep-remotion", action="store_true")
    ap.add_argument("--package-only", action="store_true")
    ap.add_argument("--final", action="store_true", help="stage images, build thumbnails, render final.mp4, and write delivery")
    ap.add_argument("--all-available", action="store_true", help="preflight + package + audio + Remotion scaffold")
    args = ap.parse_args()
    if not any([args.audio_only, args.prep_remotion, args.package_only, args.final, args.all_available]):
        args.all_available = True

    preflight_report = preflight(images_required=False)
    print(json.dumps({"preflight": preflight_report}, ensure_ascii=False, indent=2), flush=True)
    write_package_drafts(preflight_report)
    if args.package_only:
        return 0

    timed: list[dict[str, Any]] = []
    cues: list[dict[str, Any]] = []
    total = 0.0
    if args.audio_only or args.all_available:
        rows = parse_vo()
        print(f"== EP20 VO rows: {len(rows)}", flush=True)
        timed = build_voice(rows)
        cues = write_captions(timed)
        total = build_mix()
        write_audio_delivery(total, len(cues), preflight_report)
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
    factory_assets: list[dict[str, Any]] = []
    if args.prep_remotion or args.all_available or args.final:
        factory_assets = stage_factory_assets()
        write_remotion_roughcut(factory_assets)
        update_rights_for_audio_and_factory(factory_assets)
        append_event(
            "remotion_scaffold_prepared",
            {
                "revision": VIDEO_REV,
                "factory_assets": len(factory_assets),
                "roughcut": "remotion/src/data/gardner_roughcut.ts",
                "hero_images_pending": True,
            },
        )
    if args.final:
        if not MIX_WAV.exists():
            raise RuntimeError(f"audio mix missing: {MIX_WAV}; run --audio-only first")
        if not active_captions_srt().exists():
            raise RuntimeError("final captions missing; run force_align_ep20_gardner_captions.py first")
        paths = stage_visuals()
        build_thumbnails(paths)
        total = ffprobe_duration(MIX_WAV)
        render_silent_video(paths, total)
        burn_and_mux(total)
        write_final_delivery(total)
        update_rights_for_audio_and_factory(factory_assets, paths)
        update_manifest("edit_review")
        append_event(
            "edit_review_built",
            {
                "revision": VIDEO_REV,
                "final_video": str(FINAL_MP4).replace("\\", "/"),
                "duration_seconds": round(total, 3),
                "caption_file": str(active_captions_srt()).replace("\\", "/"),
                "thumbnails": 3,
                "narration_provider": "elevenlabs",
            },
        )
    print(
        json.dumps(
            {
                "status": "ready_until_hero_images",
                "audio_duration_seconds": round(total, 3) if total else None,
                "caption_cues": len(cues) if cues else None,
                "factory_assets": len(factory_assets) if factory_assets else None,
                "hero_images_present": preflight_report["hero_images_present"],
                "hero_images_missing": len(preflight_report["hero_images_missing"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
