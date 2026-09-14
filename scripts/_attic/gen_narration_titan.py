#!/usr/bin/env python3
"""Generate PD-2026-016 Titan narration with the channel voice.

Paid ElevenLabs API call. Idempotent: existing non-empty chunks with matching
idempotency keys are skipped. No upload, no publish.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-016-titan"
EPDIR = ROOT / "episodes" / EP
MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
APPROVAL_ID = "CHAT-2026-06-27-COMPLETE-TITAN"
SILENCE_SPAN_ID = "SPN-0071"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
EST_USD_PER_1000_CHARS = 0.30
SETTINGS = {
    "cold_open": {"stability": 0.40, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
    "the_dream": {"stability": 0.52, "similarity_boost": 0.82, "style": 0.25, "use_speaker_boost": True},
    "the_warnings": {"stability": 0.47, "similarity_boost": 0.84, "style": 0.34, "use_speaker_boost": True},
    "the_dive": {"stability": 0.56, "similarity_boost": 0.84, "style": 0.20, "use_speaker_boost": True},
    "the_search": {"stability": 0.54, "similarity_boost": 0.84, "style": 0.24, "use_speaker_boost": True},
    "the_truth": {"stability": 0.58, "similarity_boost": 0.84, "style": 0.18, "use_speaker_boost": True},
    "coda": {"stability": 0.64, "similarity_boost": 0.84, "style": 0.10, "use_speaker_boost": True},
}


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text("utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def media_root() -> Path:
    cfg = json.loads((ROOT / "config" / "storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        return round(float(result.stdout.strip()), 3)
    except Exception:
        return 0.0


def active_script_rev() -> str:
    manifest = json.loads((EPDIR / "manifest.json").read_text("utf-8"))
    return manifest["active_revisions"]["script"]


def idempotency_key(text: str, span_id: str, script_rev: str) -> str:
    material = json.dumps(
        {
            "episode_id": EP,
            "span_id": span_id,
            "model": MODEL,
            "voice_id": VOICE_ID,
            "text_sha256": sha256_text(text),
            "script_revision": script_rev,
            "approval_id": APPROVAL_ID,
        },
        sort_keys=True,
    )
    return "sha256:" + sha256_text(material)


def chunks() -> tuple[str, list[dict[str, Any]]]:
    script_rev = active_script_rev()
    annotated = EPDIR / "03_script" / f"script.annotated.{script_rev}.json"
    shotlist = EPDIR / "04_scenes" / "shotlist.v001.json"
    spans = json.loads(annotated.read_text("utf-8"))["spans"]
    shots = json.loads(shotlist.read_text("utf-8"))["shots"]
    shot_by_id = {shot["span_id"]: shot for shot in shots}
    out: list[dict[str, Any]] = []
    for span in spans:
        sid = span["span_id"]
        text = re.sub(r"\s+", " ", span.get("text", "")).strip()
        if not text or text == "..." or sid == SILENCE_SPAN_ID:
            continue
        chapter = shot_by_id.get(sid, {}).get("chapter_id") or "the_dream"
        out.append(
            {
                "chunk_id": sid.replace("SPN", "VC"),
                "span_id": sid,
                "chapter_id": chapter,
                "delivery": chapter,
                "spoken_text": text,
                "idempotency_key": idempotency_key(text, sid, script_rev),
            }
        )
    if len(out) != 106:
        raise RuntimeError(f"expected 106 spoken chunks, got {len(out)}")
    return script_rev, out


def chunk_is_current(out: Path, meta: Path, expected_key: str) -> bool:
    if not out.exists() or out.stat().st_size <= 2048:
        return False
    if not meta.exists():
        return False
    try:
        data = json.loads(meta.read_text("utf-8"))
    except Exception:
        return False
    return data.get("idempotency_key") == expected_key


def request_tts(api_key: str, chunk: dict[str, Any]) -> tuple[bytes, dict[str, str]]:
    body = json.dumps(
        {
            "text": chunk["spoken_text"],
            "model_id": MODEL,
            "voice_settings": SETTINGS.get(chunk["chapter_id"], SETTINGS["the_dream"]),
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        TTS.format(vid=VOICE_ID),
        data=body,
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as response:
        audio = response.read()
        evidence = {
            key.lower(): value
            for key, value in response.headers.items()
            if key.lower() in {"request-id", "x-request-id", "history-item-id", "x-elevenlabs-history-item-id"}
        }
    return audio, evidence


def write_voice_plan(script_rev: str, plan: list[dict[str, Any]], est: float, chars: int) -> Path:
    path = EPDIR / "06_audio" / "voice_plan.v001.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    annotated = EPDIR / "03_script" / f"script.annotated.{script_rev}.json"
    script = EPDIR / "03_script" / f"script.en.{script_rev}.md"
    path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "episode_id": EP,
                "script_revision": script_rev,
                "provider": "ElevenLabs",
                "voice_id": VOICE_ID,
                "model_id": MODEL,
                "approval_id": APPROVAL_ID,
                "script_hashes": {
                    "script": "sha256:" + sha256_file(script),
                    "annotated_script": "sha256:" + sha256_file(annotated),
                },
                "estimated_characters": chars,
                "estimated_cost_usd": est,
                "chunks": plan,
                "silence_span_omitted": SILENCE_SPAN_ID,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def concat_master(plan: list[dict[str, Any]], outdir: Path, master: Path) -> list[dict[str, Any]]:
    silence = outdir / "_silence_018.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.18", "-c:a", "libmp3lame", "-b:a", "192k", str(silence)],
        check=True,
        capture_output=True,
    )
    lines: list[str] = []
    index: list[dict[str, Any]] = []
    cursor = 0.0
    for i, chunk in enumerate(plan):
        path = outdir / f"{chunk['chunk_id']}.mp3"
        seconds = duration(path)
        index.append(
            {
                "chunk_id": chunk["chunk_id"],
                "span_id": chunk["span_id"],
                "file": path.name,
                "chapter_id": chunk["chapter_id"],
                "delivery": chunk["delivery"],
                "idempotency_key": chunk["idempotency_key"],
                "start": round(cursor, 3),
                "end": round(cursor + seconds, 3),
                "seconds": seconds,
                "characters": len(chunk["spoken_text"]),
            }
        )
        lines.append(f"file '{path.as_posix()}'\n")
        cursor += seconds
        if i != len(plan) - 1:
            lines.append(f"file '{silence.as_posix()}'\n")
            cursor += 0.18
    concat = outdir / "_concat_master.txt"
    concat.write_text("".join(lines), encoding="utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True)
    return index


def write_index(script_rev: str, plan: list[dict[str, Any]], index: list[dict[str, Any]], master: Path, est: float, chars: int) -> Path:
    path = EPDIR / "06_audio" / "narration_index.v001.json"
    annotated = EPDIR / "03_script" / f"script.annotated.{script_rev}.json"
    script = EPDIR / "03_script" / f"script.en.{script_rev}.md"
    path.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "provider": "ElevenLabs",
                "voice_id": VOICE_ID,
                "model_id": MODEL,
                "approval_id": APPROVAL_ID,
                "script_revision": script_rev,
                "script_hashes": {
                    "script": "sha256:" + sha256_file(script),
                    "annotated_script": "sha256:" + sha256_file(annotated),
                },
                "characters": chars,
                "estimated_cost_usd": est,
                "actual_cost_usd_estimate": est,
                "generated_total_seconds": round(duration(master), 3),
                "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
                "master_sha256": "sha256:" + sha256_file(master),
                "chunks": index,
                "silence_span_omitted": SILENCE_SPAN_ID,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--budget-usd", type=float, default=150.0)
    args = parser.parse_args(argv)

    script_rev, plan = chunks()
    chars = sum(len(chunk["spoken_text"]) for chunk in plan)
    est = round(chars / 1000 * EST_USD_PER_1000_CHARS, 2)
    print(f"episode={EP} script={script_rev} chunks={len(plan)} chars={chars} est=${est:.2f} budget=${args.budget_usd:.2f} voice={VOICE_ID} model={MODEL}")
    write_voice_plan(script_rev, plan, est, chars)
    if est > args.budget_usd:
        print("ERROR: estimated cost exceeds budget")
        return 2
    if args.dry_run:
        for chunk in plan[:8]:
            print(f"  {chunk['chunk_id']} {chunk['chapter_id']:13s} {len(chunk['spoken_text']):4d}ch {chunk['idempotency_key'][:26]}...")
        print(f"  ... {len(plan)} chunks total")
        return 0

    api_key = load_env().get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY missing")
        return 1

    outdir = media_root() / "episodes" / EP / "06_voice" / "draft"
    outdir.mkdir(parents=True, exist_ok=True)
    made = skipped = failed = 0
    for chunk in plan:
        out = outdir / f"{chunk['chunk_id']}.mp3"
        meta = out.with_suffix(".json")
        if chunk_is_current(out, meta, chunk["idempotency_key"]):
            skipped += 1
            print(f"  {chunk['chunk_id']} skip current")
            continue
        try:
            audio, evidence = request_tts(api_key, chunk)
            if len(audio) <= 2048:
                raise RuntimeError("provider returned too little audio data")
            out.write_bytes(audio)
            meta.write_text(
                json.dumps(
                    {
                        "episode_id": EP,
                        "chunk_id": chunk["chunk_id"],
                        "span_id": chunk["span_id"],
                        "chapter_id": chunk["chapter_id"],
                        "idempotency_key": chunk["idempotency_key"],
                        "model_id": MODEL,
                        "voice_id": VOICE_ID,
                        "approval_id": APPROVAL_ID,
                        "characters": len(chunk["spoken_text"]),
                        "estimated_cost_usd": round(len(chunk["spoken_text"]) / 1000 * EST_USD_PER_1000_CHARS, 4),
                        "provider": "ElevenLabs",
                        "provider_evidence": evidence,
                        "audio_sha256": "sha256:" + sha256_file(out),
                        "seconds": duration(out),
                        "generated_at": datetime.now(timezone.utc).isoformat(),
                    },
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            print(f"  {chunk['chunk_id']} {chunk['chapter_id']:13s} {len(chunk['spoken_text']):4d}ch -> {out.stat().st_size//1024}KB {duration(out):.2f}s")
            made += 1
            time.sleep(0.25)
        except urllib.error.HTTPError as exc:
            failed += 1
            print(f"  {chunk['chunk_id']} HTTP {exc.code}: {exc.read().decode(errors='replace')[:240]}")
        except Exception as exc:
            failed += 1
            print(f"  {chunk['chunk_id']} ERR {exc}")
    if failed:
        print(f"made={made} skipped={skipped} failed={failed}")
        return 1

    master = media_root() / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    index = concat_master(plan, outdir, master)
    idx = write_index(script_rev, plan, index, master, est, chars)
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({duration(master):.1f}s)")
    print(f"index -> {idx.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
