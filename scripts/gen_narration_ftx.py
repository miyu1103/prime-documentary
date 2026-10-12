"""Generate PD-2026-004-ftx narration via ElevenLabs TTS.

Paid external call, owner-approved in chat. Idempotent per text hash.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-004-ftx"
ENV = ROOT / ".env"
PLAN = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
DRAFT = Path(r"E:\pd-media\episodes\PD-2026-004-ftx\06_voice\draft")
PROV = DRAFT / "provenance.v001.json"
EVENTS = ROOT / "episodes" / EP / "events" / "events.jsonl"
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.8, "style": 0.12, "use_speaker_boost": True},
    "building": {"stability": 0.46, "similarity_boost": 0.82, "style": 0.32, "use_speaker_boost": True},
    "intense": {"stability": 0.34, "similarity_boost": 0.86, "style": 0.55, "use_speaker_boost": True},
}


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def duration(path: Path) -> float:
    result = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return round(float(result.stdout.strip()), 3)


def normalize(raw: Path, out: Path) -> None:
    tmp = out.with_suffix(".norm.mp3")
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-i",
            str(raw),
            "-af",
            "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-f",
            "mp3",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(tmp),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    tmp.replace(out)


def tts(api_key: str, voice_id: str, model_id: str, text: str, delivery: str) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
    body = json.dumps(
        {
            "text": text,
            "model_id": model_id,
            "voice_settings": SETTINGS.get(delivery, SETTINGS["calm"]),
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        method="POST",
    )
    for attempt in range(1, 6):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            msg = exc.read(400).decode("utf-8", "replace")
            if exc.code == 429 or exc.code >= 500:
                print(f"  retry HTTP {exc.code} attempt={attempt}: {msg[:120]}", flush=True)
                time.sleep(5 * attempt)
                continue
            raise RuntimeError(f"ElevenLabs HTTP {exc.code}: {msg}") from exc
    raise RuntimeError("ElevenLabs TTS failed after retries")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    env = load_env()
    api_key = env.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY missing in .env")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    voice_id = plan.get("voice_id") or env.get("ELEVENLABS_VOICE_ID")
    model_id = plan.get("model_id", "eleven_multilingual_v2")
    chunks = plan["chunks"]
    total_chars = sum(len(c["spoken_text"]) for c in chunks)
    print(f"chunks={len(chunks)} chars={total_chars} est_usd≈{total_chars / 1000 * 0.30:.2f}")

    DRAFT.mkdir(parents=True, exist_ok=True)
    prov = json.loads(PROV.read_text(encoding="utf-8")) if PROV.exists() else {"episode_id": EP, "chunks": {}}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    generated = skipped = 0
    failures: list[str] = []
    for chunk in chunks:
        cid = chunk["chunk_id"]
        text = chunk["spoken_text"]
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        out = DRAFT / f"{cid}.mp3"
        if out.exists() and prov["chunks"].get(cid, {}).get("content_hash") == text_hash:
            skipped += 1
            continue
        try:
            raw = DRAFT / f"{cid}.raw.mp3"
            raw.write_bytes(tts(api_key, voice_id, model_id, text, chunk["delivery"]))
            normalize(raw, out)
            raw.unlink(missing_ok=True)
            d = duration(out)
            prov["chunks"][cid] = {
                "chunk_id": cid,
                "section": chunk["section"],
                "delivery": chunk["delivery"],
                "filename": out.name,
                "duration_sec": d,
                "content_hash": text_hash,
                "file_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                "voice_id": voice_id,
                "model_id": model_id,
                "generated_at": now,
            }
            PROV.write_text(json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
            generated += 1
            print(f"  {cid} {chunk['delivery']:8s} {d:6.2f}s", flush=True)
            time.sleep(0.3)
        except Exception as exc:
            failures.append(cid)
            print(f"  {cid} FAIL {exc}", flush=True)
    total = round(sum(prov["chunks"][c["chunk_id"]]["duration_sec"] for c in chunks if c["chunk_id"] in prov["chunks"]), 2)
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "event": "narration_generated",
                    "episode_id": EP,
                    "stage": "audio_generating",
                    "revision": "v001",
                    "actor": "local-codex",
                    "voice_id": voice_id,
                    "model_id": model_id,
                    "generated": generated,
                    "skipped": skipped,
                    "failed": failures,
                    "total_seconds": total,
                    "estimated_cost_usd": round(total_chars / 1000 * 0.30, 2),
                    "ts": now,
                },
                ensure_ascii=False,
            )
            + "\n"
        )
    print(f"DONE generated={generated} skipped={skipped} failed={len(failures)} total={total}s")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
