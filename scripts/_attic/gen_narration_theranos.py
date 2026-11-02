#!/usr/bin/env python3
"""Generate PD-2026-015 Theranos narration with the channel voice.

Paid ElevenLabs API call. Authorized by edit_design.v002 (ElevenLabs narration
OK without charge-approval-wait) + explicit owner instruction to finish EP15.
Same channel voice as every other episode (nPczCjzI2devNBz1zQrb) = "the usual voice".
Idempotent: existing non-empty chunks are skipped.
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
EP = "PD-2026-015-theranos"
SCRIPT = ROOT / "episodes" / EP / "03_script" / "script.en.v001.md"
MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.56, "similarity_boost": 0.80, "style": 0.16, "use_speaker_boost": True},
    "building": {"stability": 0.46, "similarity_boost": 0.82, "style": 0.34, "use_speaker_boost": True},
    "intense": {"stability": 0.36, "similarity_boost": 0.84, "style": 0.48, "use_speaker_boost": True},
}


def load_env() -> dict[str, str]:
    env = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text("utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def media_root() -> Path:
    cfg = json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def dur(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    )
    try:
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return 0.0


def idempotency_key(text: str, chunk_id: str) -> str:
    material = json.dumps({
        "episode_id": EP,
        "chunk_id": chunk_id,
        "model": MODEL,
        "voice_id": VOICE_ID,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "script_revision": "v001",
    }, sort_keys=True)
    return "sha256:" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def parse_script() -> list[dict[str, str]]:
    body = SCRIPT.read_text("utf-8")
    chunks = []
    current = "unknown"
    started = False
    buf: list[str] = []
    chunk_no = 1

    def flush() -> None:
        nonlocal chunk_no, buf
        text = " ".join(x.strip() for x in buf if x.strip()).strip()
        buf = []
        if not text:
            return
        text = re.sub(r"\[CLM-[0-9]{4}\]", "", text)
        text = re.sub(r"^\[VO:\]\s*", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        delivery = "calm"
        sec = current.lower()
        if "hook" in sec or "act iii" in sec:
            delivery = "intense"
        elif "act i" in sec or "act ii" in sec or "opening" in sec:
            delivery = "building"
        if "ending" in sec or "act iv" in sec:
            delivery = "calm"
        chunks.append({
            "chunk_id": f"VC-{chunk_no:04d}",
            "section": current,
            "delivery": delivery,
            "spoken_text": text,
            "idempotency_key": idempotency_key(text, f"VC-{chunk_no:04d}"),
        })
        chunk_no += 1

    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            flush()
            started = True
            current = re.sub(r"\s+[-—].*$", "", line[3:].strip())
            continue
        if not started:
            continue
        if not line:
            flush()
            continue
        if line.startswith("#") or line.startswith("- ") or line == "---":
            continue
        if "[VO:]" in line:
            buf.append(line)
    flush()
    return chunks


def concat_master(chunks: list[dict[str, str]], outdir: Path, master: Path) -> list[dict[str, str | float]]:
    index = []
    silence = outdir / "_silence_035.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.35", "-c:a", "libmp3lame", "-b:a", "192k", str(silence)], check=True)
    cursor = 0.0
    concat = outdir / "_concat.txt"
    lines = []
    for i, c in enumerate(chunks):
        path = outdir / f"{c['chunk_id']}.mp3"
        d = dur(path)
        index.append({
            "chunk_id": c["chunk_id"],
            "file": path.name,
            "section": c["section"],
            "delivery": c["delivery"],
            "idempotency_key": c["idempotency_key"],
            "start": round(cursor, 3),
            "end": round(cursor + d, 3),
            "seconds": d,
        })
        lines.append(f"file '{path.as_posix()}'\n")
        cursor += d
        if i != len(chunks) - 1:
            lines.append(f"file '{silence.as_posix()}'\n")
            cursor += 0.35
    concat.write_text("".join(lines), "utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True)
    return index


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    env = load_env()
    key = env.get("ELEVENLABS_API_KEY")
    chunks = parse_script()
    chars = sum(len(c["spoken_text"]) for c in chunks)
    est = round(chars / 1000 * 0.30, 2)
    print(f"episode={EP} chunks={len(chunks)} chars={chars} est=${est:.2f} voice={VOICE_ID} model={MODEL}")
    if args.dry_run:
        for c in chunks[:3]:
            print(f"  {c['chunk_id']} {c['delivery']} {len(c['spoken_text'])}ch {c['idempotency_key'][:22]}...")
        return 0
    if not key:
        print("ERROR: ELEVENLABS_API_KEY missing")
        return 1
    outdir = media_root() / "episodes" / EP / "06_voice" / "draft"
    outdir.mkdir(parents=True, exist_ok=True)
    made = skipped = failed = 0
    for c in chunks:
        out = outdir / f"{c['chunk_id']}.mp3"
        meta = out.with_suffix(".json")
        if out.exists() and out.stat().st_size > 2048:
            skipped += 1
            continue
        settings = SETTINGS[c["delivery"]]
        body = json.dumps({"text": c["spoken_text"], "model_id": MODEL, "voice_settings": settings}).encode("utf-8")
        req = urllib.request.Request(
            TTS.format(vid=VOICE_ID),
            data=body,
            headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            out.write_bytes(data)
            meta.write_text(json.dumps({
                "episode_id": EP,
                "chunk_id": c["chunk_id"],
                "section": c["section"],
                "delivery": c["delivery"],
                "idempotency_key": c["idempotency_key"],
                "model_id": MODEL,
                "voice_id": VOICE_ID,
                "characters": len(c["spoken_text"]),
                "estimated_cost_usd": round(len(c["spoken_text"]) / 1000 * 0.30, 4),
                "provider": "ElevenLabs",
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            }, indent=2, ensure_ascii=False) + "\n", "utf-8")
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch -> {out.stat().st_size//1024}KB {dur(out):.2f}s")
            made += 1
            time.sleep(0.35)
        except urllib.error.HTTPError as e:
            failed += 1
            print(f"  {c['chunk_id']} HTTP {e.code}: {e.read().decode(errors='replace')[:240]}")
        except Exception as e:
            failed += 1
            print(f"  {c['chunk_id']} ERR {e}")
    master = media_root() / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    index = concat_master(chunks, outdir, master)
    idx = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
    idx.parent.mkdir(parents=True, exist_ok=True)
    idx.write_text(json.dumps({
        "episode_id": EP,
        "provider": "ElevenLabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL,
        "estimated_cost_usd": est,
        "generated_total_seconds": round(dur(master), 2),
        "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
        "chunks": index,
    }, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({dur(master):.1f}s)")
    print(f"index -> {idx.relative_to(ROOT)}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
