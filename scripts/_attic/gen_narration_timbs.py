#!/usr/bin/env python3
"""Prepare or generate PD-2026-009 Timbs narration with the channel voice.

Default mode is a no-cost dry run. Use --write-plan to write voice_plan.v001.json
without calling ElevenLabs. Use --generate only after owner approval for the paid
ElevenLabs API call.
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
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-009-timbs"
SCRIPT = ROOT / "episodes" / EP / "03_script" / "script.en.v001.md"
VOICE_PLAN = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
NARR_INDEX = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
EST_USD_PER_1000_CHARS = 0.30
SETTINGS = {
    "calm": {"stability": 0.56, "similarity_boost": 0.80, "style": 0.16, "use_speaker_boost": True},
    "building": {"stability": 0.46, "similarity_boost": 0.82, "style": 0.34, "use_speaker_boost": True},
    "intense": {"stability": 0.36, "similarity_boost": 0.84, "style": 0.48, "use_speaker_boost": True},
}


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    p = ROOT / ".env"
    if p.exists():
        for raw in p.read_text("utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def media_root() -> Path:
    cfg = json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    )
    try:
        return round(float(result.stdout.strip()), 3)
    except Exception:
        return 0.0


def script_hash() -> str:
    return "sha256:" + hashlib.sha256(SCRIPT.read_bytes()).hexdigest()


def clean_spoken_text(text: str) -> str:
    text = re.sub(r"\[CLM-[0-9]{4}\]", "", text)
    text = re.sub(r"^\[VO:\]\s*", "", text)
    return re.sub(r"\s+", " ", text).strip()


def delivery_for(section: str) -> str:
    s = section.lower()
    if "hook" in s or "act iii" in s:
        return "intense"
    if "opening" in s or "act i" in s or "act ii" in s:
        return "building"
    return "calm"


def idempotency_key(text: str, chunk_id: str) -> str:
    material = {
        "episode_id": EP,
        "chunk_id": chunk_id,
        "model": MODEL,
        "voice_id": VOICE_ID,
        "script_revision": "v001",
        "script_sha256": script_hash(),
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
    return "sha256:" + hashlib.sha256(json.dumps(material, sort_keys=True).encode("utf-8")).hexdigest()


def parse_script() -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    current: str | None = None
    chunk_no = 1
    for raw in SCRIPT.read_text("utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            current = re.sub(r"\s+[-—].*$", "", line[3:].strip())
            continue
        if current is None or line.startswith("#"):
            continue
        if "[VO:]" not in line:
            continue
        text = clean_spoken_text(line)
        chunk_id = f"VC-{chunk_no:04d}"
        chunks.append(
            {
                "chunk_id": chunk_id,
                "section": current,
                "delivery": delivery_for(current),
                "spoken_text": text,
                "idempotency_key": idempotency_key(text, chunk_id),
            }
        )
        chunk_no += 1
    if not chunks:
        raise RuntimeError("No [VO:] chunks found")
    return chunks


def write_voice_plan(chunks: list[dict[str, str]]) -> None:
    chars = sum(len(c["spoken_text"]) for c in chunks)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    VOICE_PLAN.parent.mkdir(parents=True, exist_ok=True)
    VOICE_PLAN.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "episode_id": EP,
                "script_revision": "v001",
                "script": "artifact://episodes/PD-2026-009-timbs/03_script/script.en.v001.md",
                "script_sha256": script_hash(),
                "voice_id": VOICE_ID,
                "model_id": MODEL,
                "estimated_characters": chars,
                "estimated_words": words,
                "estimated_cost_usd": round(chars / 1000 * EST_USD_PER_1000_CHARS, 2),
                "chunks": chunks,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        "utf-8",
    )


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
    )
    concat = outdir / "_concat.txt"
    lines: list[str] = []
    index: list[dict[str, str | float]] = []
    cursor = 0.0
    for i, chunk in enumerate(chunks):
        path = outdir / f"{chunk['chunk_id']}.mp3"
        dur = duration(path)
        index.append(
            {
                "chunk_id": chunk["chunk_id"],
                "file": path.name,
                "section": chunk["section"],
                "delivery": chunk["delivery"],
                "idempotency_key": chunk["idempotency_key"],
                "start": round(cursor, 3),
                "end": round(cursor + dur, 3),
                "seconds": dur,
            }
        )
        lines.append(f"file '{path.as_posix()}'\n")
        cursor += dur
        if i != len(chunks) - 1:
            lines.append(f"file '{silence.as_posix()}'\n")
            cursor += 0.35
    concat.write_text("".join(lines), "utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "libmp3lame", "-b:a", "192k", str(master)],
        check=True,
    )
    return index


def generate(chunks: list[dict[str, str]], budget_usd: float) -> int:
    key = load_env().get("ELEVENLABS_API_KEY")
    if not key:
        print("ERROR: ELEVENLABS_API_KEY missing")
        return 1
    chars = sum(len(c["spoken_text"]) for c in chunks)
    est = round(chars / 1000 * EST_USD_PER_1000_CHARS, 2)
    if est > budget_usd:
        print(f"ERROR: estimated cost ${est:.2f} exceeds budget ${budget_usd:.2f}")
        return 1
    outdir = media_root() / "episodes" / EP / "06_voice" / "draft"
    outdir.mkdir(parents=True, exist_ok=True)
    made = skipped = failed = 0
    for chunk in chunks:
        out = outdir / f"{chunk['chunk_id']}.mp3"
        meta = out.with_suffix(".json")
        if out.exists() and out.stat().st_size > 2048:
            skipped += 1
            continue
        body = json.dumps(
            {"text": chunk["spoken_text"], "model_id": MODEL, "voice_settings": SETTINGS[chunk["delivery"]]}
        ).encode("utf-8")
        req = urllib.request.Request(
            TTS.format(vid=VOICE_ID),
            data=body,
            headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                out.write_bytes(resp.read())
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
                        "characters": len(chunk["spoken_text"]),
                        "estimated_cost_usd": round(len(chunk["spoken_text"]) / 1000 * EST_USD_PER_1000_CHARS, 4),
                        "provider": "ElevenLabs",
                        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    },
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                "utf-8",
            )
            made += 1
            print(f"  {chunk['chunk_id']} {chunk['delivery']:8s} {len(chunk['spoken_text']):4d}ch -> {duration(out):.2f}s")
            time.sleep(0.35)
        except urllib.error.HTTPError as exc:
            failed += 1
            print(f"  {chunk['chunk_id']} HTTP {exc.code}: {exc.read().decode(errors='replace')[:240]}")
        except Exception as exc:
            failed += 1
            print(f"  {chunk['chunk_id']} ERR {exc}")
    master = media_root() / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    index = concat_master(chunks, outdir, master)
    NARR_INDEX.parent.mkdir(parents=True, exist_ok=True)
    NARR_INDEX.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "voice_id": VOICE_ID,
                "model_id": MODEL,
                "estimated_cost_usd": est,
                "generated_total_seconds": round(duration(master), 2),
                "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
                "chunks": index,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        "utf-8",
    )
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({duration(master):.1f}s)")
    print(f"index -> {NARR_INDEX.relative_to(ROOT)}")
    return 0 if failed == 0 else 1


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-plan", action="store_true", help="write 06_audio/voice_plan.v001.json without API calls")
    parser.add_argument("--generate", action="store_true", help="make paid ElevenLabs calls; requires owner approval")
    parser.add_argument("--budget-usd", type=float, default=6.0)
    args = parser.parse_args(argv)
    chunks = parse_script()
    chars = sum(len(c["spoken_text"]) for c in chunks)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    est = round(chars / 1000 * EST_USD_PER_1000_CHARS, 2)
    print(f"episode={EP} chunks={len(chunks)} words={words} chars={chars} est=${est:.2f} voice={VOICE_ID} model={MODEL}")
    if args.write_plan:
        write_voice_plan(chunks)
        print(f"voice_plan -> {VOICE_PLAN.relative_to(ROOT)}")
    if not args.generate:
        for chunk in chunks[:5]:
            print(f"  {chunk['chunk_id']} {chunk['delivery']:8s} {len(chunk['spoken_text']):4d}ch {chunk['section']}")
        return 0
    return generate(chunks, args.budget_usd)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
