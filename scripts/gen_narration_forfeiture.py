#!/usr/bin/env python3
"""Generate PD-2026-028 forfeiture narration with the channel voice (ElevenLabs).

Paid API. Source of truth = the planning annotated JSON (spans are the chunks).
Idempotent: existing non-empty chunk mp3s are skipped (no double-charge). Run
--dry-run first to see chars + $ estimate with NO API call and NO writes to media.
Modeled on scripts/gen_narration_kyllo.py; only the chunk source differs (annotated
JSON spans instead of [VO:] markers).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-028-forfeiture"
ANNOT = ROOT / "episodes" / "_planning" / "EP28_forfeiture_script.annotated.v001.json"
MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
DELIVERY_BY_CHAPTER = {
    "hook": "intense", "opening": "building",
    "act1": "building", "act2": "building", "act3": "intense", "act4": "building",
    "ending": "calm",
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
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return 0.0


def sha_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def idempotency_key(text: str, chunk_id: str) -> str:
    material = json.dumps({"episode_id": EP, "chunk_id": chunk_id, "model": MODEL,
                           "voice_id": VOICE_ID, "text_sha256": sha_text(text),
                           "script_revision": "v001"}, sort_keys=True)
    return "sha256:" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def parse_chunks() -> list[dict[str, str]]:
    ann = json.loads(ANNOT.read_text("utf-8"))
    span_chapter = {sid: c["chapter_id"] for c in ann["chapters"] for sid in c["span_ids"]}
    chunk_title = {c["chapter_id"]: c["title"] for c in ann["chapters"]}
    chunks = []
    for i, s in enumerate(ann["spans"], start=1):
        ch = span_chapter.get(s["span_id"], "act1")
        text = " ".join(s["text"].split()).strip()
        cid = f"VC-{i:04d}"
        chunks.append({
            "chunk_id": cid,
            "span_id": s["span_id"],
            "section": chunk_title.get(ch, ch),
            "delivery": DELIVERY_BY_CHAPTER.get(ch, "building"),
            "spoken_text": text,
            "text_sha256": sha_text(text),
            "idempotency_key": idempotency_key(text, cid),
        })
    return chunks


def concat_master(chunks, outdir: Path, master: Path):
    index = []
    silence = outdir / "_silence_035.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                    "-t", "0.35", "-c:a", "libmp3lame", "-b:a", "192k", str(silence)], check=True)
    cursor = 0.0
    lines = []
    for i, c in enumerate(chunks):
        path = outdir / f"{c['chunk_id']}.mp3"
        d = dur(path)
        index.append({"chunk_id": c["chunk_id"], "span_id": c["span_id"], "file": path.name,
                      "section": c["section"], "delivery": c["delivery"], "spoken_text": c["spoken_text"],
                      "text_sha256": c["text_sha256"], "idempotency_key": c["idempotency_key"],
                      "start": round(cursor, 3), "end": round(cursor + d, 3), "seconds": d})
        lines.append(f"file '{path.as_posix()}'\n")
        cursor += d
        if i != len(chunks) - 1:
            lines.append(f"file '{silence.as_posix()}'\n")
            cursor += 0.35
    concat = outdir / "_concat.txt"
    concat.write_text("".join(lines), "utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True)
    return index


def write_voice_plan(chunks):
    p = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"episode_id": EP, "revision": "v001", "provider": "ElevenLabs",
                             "voice_id": VOICE_ID, "model_id": MODEL, "chunks": chunks},
                            indent=2, ensure_ascii=False) + "\n", "utf-8")


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no API call, no media writes; print cost")
    args = ap.parse_args(argv)
    chunks = parse_chunks()
    chars = sum(len(c["spoken_text"]) for c in chunks)
    est = round(chars / 1000 * 0.30, 2)
    print(f"episode={EP} chunks={len(chunks)} chars={chars} est=${est:.2f} voice={VOICE_ID} model={MODEL}")
    if args.dry_run:
        for c in chunks:
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch [{c['section']}]")
        return 0
    write_voice_plan(chunks)
    env = load_env()
    key = env.get("ELEVENLABS_API_KEY")
    if not key:
        print("ERROR: ELEVENLABS_API_KEY missing")
        return 1
    outdir = media_root() / "episodes" / EP / "06_voice" / "draft"
    outdir.mkdir(parents=True, exist_ok=True)
    made = skipped = failed = 0
    for c in chunks:
        out = outdir / f"{c['chunk_id']}.mp3"
        if out.exists() and out.stat().st_size > 2048:
            skipped += 1
            continue
        body = json.dumps({"text": c["spoken_text"], "model_id": MODEL,
                           "voice_settings": SETTINGS[c["delivery"]]}).encode("utf-8")
        req = urllib.request.Request(TTS.format(vid=VOICE_ID), data=body,
                                     headers={"xi-api-key": key, "Content-Type": "application/json",
                                              "Accept": "audio/mpeg"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            out.write_bytes(data)
            out.with_suffix(".json").write_text(json.dumps(
                {"episode_id": EP, "chunk_id": c["chunk_id"], "section": c["section"],
                 "delivery": c["delivery"], "idempotency_key": c["idempotency_key"], "model_id": MODEL,
                 "voice_id": VOICE_ID, "characters": len(c["spoken_text"]),
                 "estimated_cost_usd": round(len(c["spoken_text"]) / 1000 * 0.30, 4),
                 "provider": "ElevenLabs", "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")},
                indent=2, ensure_ascii=False) + "\n", "utf-8")
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch -> {out.stat().st_size//1024}KB {dur(out):.2f}s")
            made += 1
            time.sleep(0.35)
        except urllib.error.HTTPError as e:
            failed += 1
            print(f"  {c['chunk_id']} HTTP {e.code}: {e.read().decode(errors='replace')[:240]}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  {c['chunk_id']} ERR {e}")
    master = media_root() / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    index = concat_master(chunks, outdir, master)
    idx = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
    idx.parent.mkdir(parents=True, exist_ok=True)
    idx.write_text(json.dumps({"episode_id": EP, "voice_id": VOICE_ID, "model_id": MODEL,
                               "estimated_cost_usd": est, "generated_total_seconds": round(dur(master), 2),
                               "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
                               "chunks": index}, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({dur(master):.1f}s)")
    print(f"index -> {idx.relative_to(ROOT)}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
