#!/usr/bin/env python3
"""Generate PD-2026-006 Terry narration with the channel voice.

Paid ElevenLabs API call. Owner approval is recorded in APR-0002.
Idempotent: existing non-empty chunks with matching idempotency keys are skipped.
No upload and no publish.
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


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-006-terry"
SCRIPT = ROOT / "episodes" / EP / "03_script" / "script.en.v001.md"
ANNOTATED = ROOT / "episodes" / EP / "03_script" / "script.annotated.v001.json"
MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
APPROVAL_ID = "APR-0002"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.56, "similarity_boost": 0.80, "style": 0.16, "use_speaker_boost": True},
    "building": {"stability": 0.46, "similarity_boost": 0.82, "style": 0.34, "use_speaker_boost": True},
    "intense": {"stability": 0.36, "similarity_boost": 0.84, "style": 0.48, "use_speaker_boost": True},
}
EST_USD_PER_1000_CHARS = 0.30


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
    cfg = json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def dur(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    )
    try:
        return round(float(result.stdout.strip()), 3)
    except Exception:
        return 0.0


def idempotency_key(text: str, chunk_id: str) -> str:
    material = json.dumps(
        {
            "episode_id": EP,
            "chunk_id": chunk_id,
            "model": MODEL,
            "voice_id": VOICE_ID,
            "text_sha256": sha256_text(text),
            "script_revision": "v001",
            "approval_id": APPROVAL_ID,
        },
        sort_keys=True,
    )
    return "sha256:" + sha256_text(material)


def script_hashes() -> dict[str, str]:
    return {
        "script": "sha256:" + sha256_file(SCRIPT),
        "annotated_script": "sha256:" + sha256_file(ANNOTATED),
    }


def parse_script() -> list[dict[str, str]]:
    body = SCRIPT.read_text("utf-8")
    chunks: list[dict[str, str]] = []
    current = "unknown"
    chunk_no = 1

    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            current = re.sub(r"\s+[-—].*$", "", line[3:].strip())
            continue
        if not line.startswith("[VO:]"):
            continue
        text = re.sub(r"\[CLM-[0-9]{4}\]", "", line)
        text = re.sub(r"^\[VO:\]\s*", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        delivery = "calm"
        section = current.lower()
        if "hook" in section or "act iii" in section:
            delivery = "intense"
        elif "opening" in section or "act i" in section or "act ii" in section:
            delivery = "building"
        if "act iv" in section or "ending" in section:
            delivery = "calm"
        chunk_id = f"VC-{chunk_no:04d}"
        chunks.append(
            {
                "chunk_id": chunk_id,
                "section": current,
                "delivery": delivery,
                "spoken_text": text,
                "idempotency_key": idempotency_key(text, chunk_id),
            }
        )
        chunk_no += 1
    if not chunks:
        raise RuntimeError("No [VO:] chunks found")
    return chunks


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


def concat_master(chunks: list[dict[str, str]], outdir: Path, master: Path) -> list[dict[str, str | float]]:
    silence = outdir / "_silence_035.mp3"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=44100:cl=mono",
            "-t",
            "0.35",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(silence),
        ],
        check=True,
        capture_output=True,
    )
    concat = outdir / "_concat.txt"
    lines: list[str] = []
    index: list[dict[str, str | float]] = []
    cursor = 0.0
    for i, chunk in enumerate(chunks):
        path = outdir / f"{chunk['chunk_id']}.mp3"
        seconds = dur(path)
        index.append(
            {
                "chunk_id": chunk["chunk_id"],
                "file": path.name,
                "section": chunk["section"],
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
        if i != len(chunks) - 1:
            lines.append(f"file '{silence.as_posix()}'\n")
            cursor += 0.35
    concat.write_text("".join(lines), encoding="utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "libmp3lame", "-b:a", "192k", str(master)],
        check=True,
    )
    return index


def request_tts(api_key: str, chunk: dict[str, str]) -> tuple[bytes, dict[str, str]]:
    body = json.dumps(
        {
            "text": chunk["spoken_text"],
            "model_id": MODEL,
            "voice_settings": SETTINGS[chunk["delivery"]],
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


def write_index(chunks: list[dict[str, str]], index: list[dict[str, str | float]], master: Path, est: float, chars: int) -> Path:
    idx = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
    idx.parent.mkdir(parents=True, exist_ok=True)
    idx.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "provider": "ElevenLabs",
                "voice_id": VOICE_ID,
                "model_id": MODEL,
                "approval_id": APPROVAL_ID,
                "script_hashes": script_hashes(),
                "characters": chars,
                "estimated_cost_usd": est,
                "generated_total_seconds": round(dur(master), 3),
                "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
                "master_sha256": "sha256:" + sha256_file(master),
                "chunks": index,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return idx


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--budget-usd", type=float, default=100.0)
    args = parser.parse_args(argv)

    chunks = parse_script()
    chars = sum(len(chunk["spoken_text"]) for chunk in chunks)
    est = round(chars / 1000 * EST_USD_PER_1000_CHARS, 2)
    print(f"episode={EP} chunks={len(chunks)} chars={chars} est=${est:.2f} budget=${args.budget_usd:.2f} voice={VOICE_ID} model={MODEL}")
    if est > args.budget_usd:
        print("ERROR: estimated cost exceeds budget")
        return 2
    if args.dry_run:
        for chunk in chunks:
            print(f"  {chunk['chunk_id']} {chunk['delivery']:8s} {len(chunk['spoken_text']):4d}ch {chunk['idempotency_key'][:26]}...")
        return 0

    env = load_env()
    api_key = env.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY missing")
        return 1

    outdir = media_root() / "episodes" / EP / "06_voice" / "draft"
    outdir.mkdir(parents=True, exist_ok=True)
    made = skipped = failed = 0
    for chunk in chunks:
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
                        "section": chunk["section"],
                        "delivery": chunk["delivery"],
                        "idempotency_key": chunk["idempotency_key"],
                        "model_id": MODEL,
                        "voice_id": VOICE_ID,
                        "approval_id": APPROVAL_ID,
                        "characters": len(chunk["spoken_text"]),
                        "estimated_cost_usd": round(len(chunk["spoken_text"]) / 1000 * EST_USD_PER_1000_CHARS, 4),
                        "provider": "ElevenLabs",
                        "provider_evidence": evidence,
                        "audio_sha256": "sha256:" + sha256_file(out),
                        "seconds": dur(out),
                        "generated_at": datetime.now(timezone.utc).isoformat(),
                    },
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            print(f"  {chunk['chunk_id']} {chunk['delivery']:8s} {len(chunk['spoken_text']):4d}ch -> {out.stat().st_size//1024}KB {dur(out):.2f}s")
            made += 1
            time.sleep(0.35)
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
    index = concat_master(chunks, outdir, master)
    idx = write_index(chunks, index, master, est, chars)
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({dur(master):.1f}s)")
    print(f"index -> {idx.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
