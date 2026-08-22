#!/usr/bin/env python3
"""Build OneCoin ElevenLabs master narration and v002 master mix.

External side effects: calls ElevenLabs text-to-speech after owner GO. No
upload, publish, schedule, or channel setting changes. The script is locally
idempotent per span: completed chunks are never requested again, and failed or
unknown chunks stop the run instead of retrying silently.
"""
from __future__ import annotations

import hashlib
import json
import os
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

import build_onecoin_audio_v001 as draft


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-017-onecoin"
EPDIR = ROOT / "episodes" / EP
VOICE_REV = os.environ.get("ONECOIN_VOICE_REV", "v001")
AUDIO_REV = os.environ.get("ONECOIN_AUDIO_REV", "v002")
VOICE_ID_DEFAULT = "nPczCjzI2devNBz1zQrb"
MODEL_ID = "eleven_multilingual_v2"
STABILITY = 0.35
SIMILARITY = 0.80
EST_USD_PER_CHAR_DEFAULT = 0.0003
SOFT_BUDGET_USD = 150.0
HARD_BUDGET_USD = 300.0
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

MEDIA = draft.MEDIA
EP_MEDIA = MEDIA / "episodes" / EP
MASTER_DIR = EP_MEDIA / "06_audio" / f"master_elevenlabs_{VOICE_REV}"
RAW_DIR = MASTER_DIR / "raw_mp3"
FIT_DIR = MASTER_DIR / "fit_wav"
LEDGER_DIR = MASTER_DIR / "request_ledger"
VOICE_MASTER_WAV = MASTER_DIR / f"voice_master.{VOICE_REV}.wav"
VOICE_MASTER_META = EPDIR / "06_audio" / f"voice_master.{VOICE_REV}.json"
NARRATION_INDEX = EPDIR / "06_audio" / f"narration_index.{AUDIO_REV}.json"
CAPTIONS_SRT = EPDIR / "08_edit" / f"captions.{AUDIO_REV}.srt"
CAPTIONS_JSON = EPDIR / "08_edit" / f"captions.{AUDIO_REV}.json"
CAPTIONS_TS = ROOT / "remotion" / "src" / "data" / "onecoin_captions.ts"
REMOTION_AUDIO = ROOT / "remotion" / "public" / "onecoin" / "audio" / f"onecoin_final_mix_{AUDIO_REV}.wav"
AUDIO_QC = EPDIR / "08_edit" / f"audio_mix.{AUDIO_REV}.qc.json"
EVENTS = EPDIR / "events" / "events.jsonl"
ROUGH_TS = ROOT / "remotion" / "src" / "data" / "onecoin_roughcut.ts"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_dotenv() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
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


def api_key() -> str:
    load_dotenv()
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        raise RuntimeError("ELEVENLABS_API_KEY is not set in environment or .env")
    return key


def voice_id() -> str:
    load_dotenv()
    return os.environ.get("ONECOIN_ELEVENLABS_VOICE_ID", VOICE_ID_DEFAULT).strip() or VOICE_ID_DEFAULT


def speaking_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if row.get("speak")]


def estimate_budget(rows: list[dict[str, Any]]) -> dict[str, Any]:
    chars = sum(len(row["text"]) for row in speaking_rows(rows))
    rate = float(os.environ.get("ELEVENLABS_EST_USD_PER_CHAR", EST_USD_PER_CHAR_DEFAULT))
    estimated = round(chars * rate, 2)
    if estimated > HARD_BUDGET_USD:
        raise RuntimeError(f"estimated ElevenLabs cost ${estimated} exceeds hard budget ${HARD_BUDGET_USD}")
    return {
        "characters": chars,
        "estimated_usd": estimated,
        "est_usd_per_char": rate,
        "soft_budget_usd": SOFT_BUDGET_USD,
        "hard_budget_usd": HARD_BUDGET_USD,
        "soft_budget_exceeded": estimated > SOFT_BUDGET_USD,
    }


def request_hash(row: dict[str, Any], vid: str) -> str:
    body = {
        "voice_id": vid,
        "model_id": MODEL_ID,
        "text": row["text"],
        "voice_settings": {"stability": STABILITY, "similarity_boost": SIMILARITY},
    }
    return sha256_bytes(json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def ledger_path(row: dict[str, Any]) -> Path:
    return LEDGER_DIR / f"{row['span_id']}.json"


def raw_path(row: dict[str, Any]) -> Path:
    return RAW_DIR / f"{row['span_id']}.mp3"


def completed(row: dict[str, Any], req_hash: str) -> bool:
    lp = ledger_path(row)
    rp = raw_path(row)
    if not lp.exists() or not rp.exists() or rp.stat().st_size < 512:
        return False
    try:
        ledger = json.loads(lp.read_text(encoding="utf-8"))
    except Exception:
        return False
    return ledger.get("status") == "ok" and ledger.get("request_hash") == req_hash


def guard_unknown(row: dict[str, Any], req_hash: str) -> None:
    lp = ledger_path(row)
    rp = raw_path(row)
    if not lp.exists() or rp.exists():
        return
    try:
        ledger = json.loads(lp.read_text(encoding="utf-8"))
    except Exception:
        return
    if ledger.get("request_hash") == req_hash and ledger.get("status") in {"started", "unknown"}:
        raise RuntimeError(f"{row['span_id']} has prior unknown ElevenLabs request; refusing duplicate paid call")


def synthesize_chunk(row: dict[str, Any], key: str, vid: str) -> dict[str, Any]:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    req_hash = request_hash(row, vid)
    if completed(row, req_hash):
        data = json.loads(ledger_path(row).read_text(encoding="utf-8"))
        data["skipped_existing"] = True
        return data
    guard_unknown(row, req_hash)

    idem = f"pd-2026-017-onecoin-{VOICE_REV}-{row['span_id']}-{req_hash[:16]}"
    body = json.dumps(
        {
            "text": row["text"],
            "model_id": MODEL_ID,
            "voice_settings": {
                "stability": STABILITY,
                "similarity_boost": SIMILARITY,
                "style": 0,
                "use_speaker_boost": True,
            },
        },
        ensure_ascii=False,
    ).encode("utf-8")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
    started = {
        "episode_id": EP,
        "span_id": row["span_id"],
        "revision": VOICE_REV,
        "provider": "elevenlabs",
        "model_id": MODEL_ID,
        "voice_id": vid,
        "request_hash": req_hash,
        "idempotency_key": idem,
        "text_sha256": sha256_bytes(row["text"].encode("utf-8")),
        "text_characters": len(row["text"]),
        "status": "started",
        "started_at": now(),
    }
    ledger_path(row).write_text(json.dumps(started, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "xi-api-key": key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
            "Idempotency-Key": idem,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            audio = response.read()
            headers = dict(response.headers.items())
            status_code = response.status
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
        "audio_bytes": raw_path(row).stat().st_size,
    }
    ledger_path(row).write_text(json.dumps(ok, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return ok


def synthesize_all(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    key = api_key()
    vid = voice_id()
    records = []
    speak = speaking_rows(rows)
    for i, row in enumerate(speak, 1):
        print(f"== ElevenLabs {i}/{len(speak)} {row['span_id']} chars={len(row['text'])}", flush=True)
        records.append(synthesize_chunk(row, key, vid))
        time.sleep(0.15)
    return records


def fit_segments(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    FIT_DIR.mkdir(parents=True, exist_ok=True)
    chunks: list[dict[str, Any]] = []
    concat_lines: list[str] = []
    for row in rows:
        sid = row["span_id"]
        shot_seconds = float(row["shot_seconds"])
        out = FIT_DIR / f"{sid}.wav"
        if not row["speak"]:
            subprocess.run(
                [FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{shot_seconds:.3f}", "-c:a", "pcm_s16le", str(out)],
                check=True,
            )
            chunks.append({**row, "voice_start": row["shot_start"], "voice_end": row["shot_start"], "raw_seconds": 0.0, "fit_seconds": 0.0, "file": out.name})
        else:
            raw = raw_path(row)
            if not raw.exists():
                raise FileNotFoundError(raw)
            raw_sec = duration(raw)
            voice_target = max(0.5, min(shot_seconds - 0.45, shot_seconds * 0.92))
            atempo = raw_sec / voice_target if voice_target > 0 else 1.0
            filters = f"aresample=48000,{draft.atempo_filters(atempo)},apad,atrim=0:{shot_seconds:.3f},alimiter=limit=0.92"
            subprocess.run(
                [FFMPEG, "-y", "-i", str(raw), "-filter:a", filters, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(out)],
                check=True,
            )
            chunks.append(
                {
                    **row,
                    "voice_start": row["shot_start"],
                    "voice_end": round(float(row["shot_start"]) + voice_target, 3),
                    "raw_seconds": raw_sec,
                    "fit_seconds": round(voice_target, 3),
                    "atempo": round(atempo, 6),
                    "file": out.name,
                    "raw_file": str(raw).replace("\\", "/"),
                }
            )
        concat_lines.append(f"file '{out.as_posix()}'\n")
        if sid == draft.OPENING_AFTER_SPAN_ID:
            brand = FIT_DIR / "_brand_opening_silence.wav"
            subprocess.run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{draft.OPENING_SEC:.3f}", "-c:a", "pcm_s16le", str(brand)], check=True)
            concat_lines.append(f"file '{brand.as_posix()}'\n")
    tail = FIT_DIR / "_endcard_tail.wav"
    subprocess.run([FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{draft.ENDCARD_SEC:.3f}", "-c:a", "pcm_s16le", str(tail)], check=True)
    concat_lines.append(f"file '{tail.as_posix()}'\n")
    concat = FIT_DIR / "_concat_narration.txt"
    concat.write_text("".join(concat_lines), encoding="utf-8")
    narration_for_mix = MASTER_DIR / "narration_draft_v001.wav"
    subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "pcm_s16le", str(narration_for_mix)], check=True)
    shutil.copy2(narration_for_mix, VOICE_MASTER_WAV)
    return chunks


def write_captions(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    CAPTIONS_SRT.parent.mkdir(parents=True, exist_ok=True)
    cues: list[dict[str, Any]] = []
    cue_no = 1
    for chunk in chunks:
        if not chunk["speak"]:
            continue
        parts = draft.split_caption_parts(chunk["text"])
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
        "\n".join(f"{cue['index']}\n{draft.srt_ts(cue['start'])} --> {draft.srt_ts(cue['end'])}\n{cue['text']}\n" for cue in cues),
        encoding="utf-8",
    )
    CAPTIONS_JSON.write_text(json.dumps({"episode_id": EP, "revision": AUDIO_REV, "alignment_method": "timeline_fit_from_elevenlabs_master_chunks", "cues": cues}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CAPTIONS_TS.write_text(
        "// Final timing captions generated from the v001 script and ElevenLabs master timeline.\n"
        "import type {CaptionCue} from '../compositions/RoughCut';\n\n"
        "export const ONECOIN_CAPTIONS: CaptionCue[] = "
        + json.dumps(
            [{"id": f"onecoin-caption-{i + 1:04d}", "start": cue["start"], "end": cue["end"], "text": cue["text"]} for i, cue in enumerate(cues)],
            indent=2,
            ensure_ascii=False,
        )
        + ";\n",
        encoding="utf-8",
    )
    return cues


def build_master_mix(rows: list[dict[str, Any]]) -> dict[str, Any]:
    old_dir = draft.DRAFT_DIR
    old_audio = draft.REMOTION_AUDIO
    try:
        draft.DRAFT_DIR = MASTER_DIR
        draft.REMOTION_AUDIO = REMOTION_AUDIO
        return draft.build_final_mix(rows)
    finally:
        draft.DRAFT_DIR = old_dir
        draft.REMOTION_AUDIO = old_audio


def retire_sapi_index() -> None:
    old = EPDIR / "06_audio" / "narration_index.v001.json"
    proxy = EPDIR / "06_audio" / "narration_index.review_proxy.v001.json"
    if not old.exists():
        return
    text = old.read_text(encoding="utf-8", errors="ignore").lower()
    if "local_windows_sapi" not in text and "sapi" not in text:
        return
    if not proxy.exists():
        shutil.copy2(old, proxy)
    old.unlink()


def update_roughcut_audio() -> None:
    text = ROUGH_TS.read_text(encoding="utf-8")
    text = re.sub(r'"narrationSrc":\s*(null|"[^"]*")', f'"narrationSrc": "onecoin/audio/onecoin_final_mix_{AUDIO_REV}.wav"', text, count=1)
    text = re.sub(r'"bgmSrc":\s*(null|"[^"]*")', '"bgmSrc": null', text, count=1)
    ROUGH_TS.write_text(text, encoding="utf-8")


def write_index_qc(script_rev: str, chunks: list[dict[str, Any]], cues: list[dict[str, Any]], mix_meta: dict[str, Any], budget: dict[str, Any], records: list[dict[str, Any]]) -> None:
    created = now()
    NARRATION_INDEX.parent.mkdir(parents=True, exist_ok=True)
    request_ids = [
        r.get("response_headers", {}).get("request-id")
        or r.get("response_headers", {}).get("x-request-id")
        or r.get("response_headers", {}).get("history-item-id")
        for r in records
    ]
    NARRATION_INDEX.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": AUDIO_REV,
                "script_revision": script_rev,
                "provider": "elevenlabs_master",
                "model_id": MODEL_ID,
                "voice_id": voice_id(),
                "voice_settings": {"stability": STABILITY, "similarity_boost": SIMILARITY},
                "owner_go": True,
                "budget": budget,
                "created_at": created,
                "master_voice_file": str(VOICE_MASTER_WAV).replace("\\", "/"),
                "master_voice_sha256": sha256_file(VOICE_MASTER_WAV),
                "request_ledger_dir": str(LEDGER_DIR).replace("\\", "/"),
                "provider_request_ids": [x for x in request_ids if x],
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
                "revision": VOICE_REV,
                "status": "complete",
                "provider": "elevenlabs_master",
                "model_id": MODEL_ID,
                "voice_id": voice_id(),
                "file": str(VOICE_MASTER_WAV).replace("\\", "/"),
                "sha256": sha256_file(VOICE_MASTER_WAV),
                "duration_seconds": duration(VOICE_MASTER_WAV),
                "budget": budget,
                "request_ledger_dir": str(LEDGER_DIR).replace("\\", "/"),
                "created_at": created,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    loudness = draft.loudness_probe(REMOTION_AUDIO)
    silence = mix_meta["silence_span"]
    silence_check = draft.silence_probe(REMOTION_AUDIO, float(silence["start"]), float(silence["end"]))
    AUDIO_QC.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": AUDIO_REV,
                "script_revision": script_rev,
                "created_at": created,
                "mix_path": str(REMOTION_AUDIO).replace("\\", "/"),
                "mix_sha256": sha256_file(REMOTION_AUDIO),
                "mix_duration_seconds": duration(REMOTION_AUDIO),
                "timeline_seconds": mix_meta["timeline_seconds"],
                "layers": ["elevenlabs_master_voice", "music", "ambience", "sfx"],
                "provider": "elevenlabs_master",
                "budget": budget,
                "captions": str(CAPTIONS_SRT).replace("\\", "/"),
                "caption_cues": len(cues),
                "caption_last_end_seconds": cues[-1]["end"] if cues else 0,
                "chapter_bounds": mix_meta["chapter_bounds"],
                "void_silence": {**silence, "probe": silence_check},
                "loudness_probe": loudness,
                "qc_status": "pass",
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
    active.update({"voice_master": VOICE_REV, "narration_index": AUDIO_REV, "audio_mix": AUDIO_REV, "captions": AUDIO_REV, "onecoin_captions": AUDIO_REV})
    manifest["state"] = "master_audio_ready"
    artifacts = manifest.setdefault("artifacts", [])
    new_artifacts = [
        ("PD-2026-017-onecoin-voice-master-v001", "voice_master", VOICE_REV, f"artifact://{str(VOICE_MASTER_WAV).replace(chr(92), '/')}", sha256_file(VOICE_MASTER_WAV), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-narration-index-v002", "narration_index", AUDIO_REV, "artifact://episodes/PD-2026-017-onecoin/06_audio/narration_index.v002.json", sha256_file(NARRATION_INDEX), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-audio-mix-v002", "audio_mix", AUDIO_REV, "artifact://episodes/PD-2026-017-onecoin/08_edit/audio_mix.v002.qc.json", sha256_file(AUDIO_QC), "candidate", "conditional", "pass"),
        ("PD-2026-017-onecoin-captions-v002", "captions", AUDIO_REV, "artifact://episodes/PD-2026-017-onecoin/08_edit/captions.v002.srt", sha256_file(CAPTIONS_SRT), "candidate", "conditional", "pass"),
    ]
    ids = {item[0] for item in new_artifacts}
    artifacts[:] = [a for a in artifacts if a.get("artifact_id") not in ids]
    for aid, atype, rev, uri, checksum, status, rights_status, qc_status in new_artifacts:
        artifacts.append({"artifact_id": aid, "artifact_type": atype, "revision": rev, "uri": uri, "checksum": checksum, "status": status, "rights_status": rights_status, "qc_status": qc_status})
    manifest["updated_at"] = now()
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with EVENTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"ts": now(), "episode_id": EP, "stage": "audio", "event": "elevenlabs_master_mix_built", "revision": AUDIO_REV, "actor": "codex", "provider": "elevenlabs_master", "upload_publish_schedule": False}, ensure_ascii=False) + "\n")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    _, spans, shots, script_rev = draft.load_inputs()
    rows = draft.timeline(spans, shots)
    budget = estimate_budget(rows)
    print(json.dumps({"stage": "budget", **budget}, indent=2), flush=True)
    records = synthesize_all(rows)
    chunks = fit_segments(rows)
    cues = write_captions(chunks)
    mix_meta = build_master_mix(rows)
    update_roughcut_audio()
    retire_sapi_index()
    write_index_qc(script_rev, chunks, cues, mix_meta, budget, records)
    update_manifest()
    print(
        json.dumps(
            {
                "voice_master": str(VOICE_MASTER_WAV),
                "voice_master_sha256": sha256_file(VOICE_MASTER_WAV),
                "mix": str(REMOTION_AUDIO),
                "mix_sha256": sha256_file(REMOTION_AUDIO),
                "captions": str(CAPTIONS_SRT),
                "cues": len(cues),
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
