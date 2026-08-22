#!/usr/bin/env python3
"""Generate PD-2026-031-unlock narration with the channel ElevenLabs voice.

Paid ElevenLabs API call (within Pro plan quota). Idempotent: a chunk whose
mp3 exists (>2KB) with a matching idempotency key is skipped, so re-runs cost
nothing. No upload, no publish. Reads the design-stage annotated script in
episodes/_planning/ (this episode's working folder is not bootstrapped yet).

Output (all under a gitignored raw dir; heavy audio never committed):
  episodes/PD-2026-031-unlock/06_audio/narration/raw/VC-####.mp3 (+ .json meta)
  episodes/PD-2026-031-unlock/06_audio/narration/raw/narration_master.v001.mp3
  episodes/PD-2026-031-unlock/06_audio/narration_index.v001.json  (text, committable)
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-031-unlock"
REV = sys.argv[1] if len(sys.argv) > 1 else "v001"
ANNOTATED = ROOT / "episodes" / "_planning" / f"EP31_unlock_script.annotated.{REV}.json"
OUTDIR = ROOT / "episodes" / EP / "06_audio" / "narration" / "raw"
INDEX = ROOT / "episodes" / EP / "06_audio" / f"narration_index.{REV}.json"
MASTER_NAME = f"narration_master.{REV}.mp3"
MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
EST_USD_PER_1000 = 0.30
GAP_SEC = 0.28  # inter-span breath in the master

# Per-chapter delivery (channel voice; v2 baseline stability~0.35/sim~0.80, varied by act)
SETTINGS = {
    "hook":    {"stability": 0.40, "similarity_boost": 0.82, "style": 0.34, "use_speaker_boost": True},
    "opening": {"stability": 0.42, "similarity_boost": 0.82, "style": 0.28, "use_speaker_boost": True},
    "act1":    {"stability": 0.45, "similarity_boost": 0.83, "style": 0.22, "use_speaker_boost": True},
    "act2":    {"stability": 0.46, "similarity_boost": 0.83, "style": 0.22, "use_speaker_boost": True},
    "act3":    {"stability": 0.48, "similarity_boost": 0.83, "style": 0.20, "use_speaker_boost": True},
    "act4":    {"stability": 0.54, "similarity_boost": 0.84, "style": 0.15, "use_speaker_boost": True},
    "ending":  {"stability": 0.60, "similarity_boost": 0.84, "style": 0.10, "use_speaker_boost": True},
}


def load_env() -> dict:
    env = {}
    for line in (ROOT / ".env").read_text("utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def sha256_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return 0.0


def idem_key(text: str, sid: str) -> str:
    mat = json.dumps({"ep": EP, "sid": sid, "model": MODEL, "voice": VOICE_ID,
                      "text_sha256": sha256_text(text)}, sort_keys=True)
    return "sha256:" + sha256_text(mat)


def build_chunks() -> list[dict]:
    doc = json.loads(ANNOTATED.read_text("utf-8"))
    span_chapter = {}
    for ch in doc["chapters"]:
        for sid in ch["span_ids"]:
            span_chapter[sid] = ch["chapter_id"]
    out = []
    for span in doc["spans"]:
        sid = span["span_id"]
        text = re.sub(r"\s+", " ", span.get("text", "")).strip()
        if not text:
            continue
        out.append({
            "chunk_id": sid.replace("SPN", "VC"),
            "span_id": sid,
            "chapter_id": span_chapter.get(sid, "act1"),
            "spoken_text": text,
            "idempotency_key": idem_key(text, sid),
        })
    return out


def is_current(mp3: Path, meta: Path, key: str) -> bool:
    if not mp3.exists() or mp3.stat().st_size <= 2048 or not meta.exists():
        return False
    try:
        return json.loads(meta.read_text("utf-8")).get("idempotency_key") == key
    except Exception:
        return False


def request_tts(api_key: str, chunk: dict) -> tuple[bytes, dict]:
    body = json.dumps({"text": chunk["spoken_text"], "model_id": MODEL,
                       "voice_settings": SETTINGS.get(chunk["chapter_id"], SETTINGS["act1"])}).encode("utf-8")
    req = urllib.request.Request(TTS.format(vid=VOICE_ID), data=body,
                                 headers={"xi-api-key": api_key, "Content-Type": "application/json",
                                          "Accept": "audio/mpeg"}, method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        audio = r.read()
        ev = {k.lower(): v for k, v in r.headers.items()
              if k.lower() in {"request-id", "x-request-id", "history-item-id"}}
    return audio, ev


def concat_master(plan: list[dict], master: Path):
    silence = OUTDIR / "_gap.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                    "-t", str(GAP_SEC), "-c:a", "libmp3lame", "-b:a", "128k", str(silence)],
                   check=True, capture_output=True)
    listfile = OUTDIR / "_concat.txt"
    lines = []
    for i, p in enumerate(plan):
        lines.append(f"file '{(OUTDIR / (p['chunk_id'] + '.mp3')).as_posix()}'")
        if i != len(plan) - 1:
            lines.append(f"file '{silence.as_posix()}'")
    listfile.write_text("\n".join(lines), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True, capture_output=True)


def main():
    env = load_env()
    api_key = env.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        sys.exit("ELEVENLABS_API_KEY missing in .env")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    plan = build_chunks()
    total_chars = sum(len(c["spoken_text"]) for c in plan)
    print(f"spans={len(plan)}  chars={total_chars}  est_cost=${total_chars/1000*EST_USD_PER_1000:.2f}")

    generated = skipped = 0
    index_rows = []
    for c in plan:
        mp3 = OUTDIR / f"{c['chunk_id']}.mp3"
        meta = OUTDIR / f"{c['chunk_id']}.json"
        if is_current(mp3, meta, c["idempotency_key"]):
            skipped += 1
        else:
            audio, ev = request_tts(api_key, c)
            mp3.write_bytes(audio)
            meta.write_text(json.dumps({**{k: c[k] for k in ("chunk_id", "span_id", "chapter_id",
                            "idempotency_key")}, "bytes": len(audio), "evidence": ev},
                            ensure_ascii=False, indent=2), encoding="utf-8")
            generated += 1
            print(f"  gen {c['chunk_id']} [{c['chapter_id']}] {len(audio)}B")
        index_rows.append({"chunk_id": c["chunk_id"], "span_id": c["span_id"],
                           "chapter_id": c["chapter_id"], "file": f"narration/raw/{c['chunk_id']}.mp3",
                           "chars": len(c["spoken_text"]), "duration_sec": duration(mp3)})

    master = OUTDIR / MASTER_NAME
    concat_master(plan, master)
    master_dur = duration(master)

    INDEX.write_text(json.dumps({
        "schema_version": "1.0.0", "episode_id": EP, "revision": REV,
        "provider": "ElevenLabs", "voice_id": VOICE_ID, "model_id": MODEL,
        "source_annotated": "episodes/_planning/EP31_unlock_script.annotated.v001.json",
        "gap_sec": GAP_SEC, "total_chars": total_chars,
        "master": f"narration/raw/{MASTER_NAME}",
        "master_duration_sec": master_dur, "chunks": index_rows,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"generated={generated} skipped={skipped}")
    print(f"MASTER: {master}  ({master_dur:.1f}s = {master_dur/60:.2f}min)")
    print(f"index: {INDEX}")


if __name__ == "__main__":
    main()
