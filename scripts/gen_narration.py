"""
scripts/gen_narration.py
Role: audio-director
Generate master narration for PD-2026-001-miranda from voice_plan.v001.json.

Voice: Brian (nPczCjzI2devNBz1zQrb), eleven_multilingual_v2
QC: loudnorm -16 LUFS / -1.5 TP / LRA 11
Idempotency: SHA-256 of spoken_text → skip if file + hash match registry
Output: H:\pd-media\episodes\PD-2026-001-miranda\06_voice\draft\VC-NNNN.mp3
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── Config ──────────────────────────────────────────────────────────────────
ENV_PATH      = pathlib.Path(r"C:\Users\aab15\Documents\prime-documentary\.env")
VOICE_PLAN    = pathlib.Path(
    r"C:\Users\aab15\Documents\prime-documentary\episodes"
    r"\PD-2026-001-miranda\06_audio\voice_plan.v001.json"
)
DRAFT_DIR     = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_voice\draft")
PROV_PATH     = DRAFT_DIR / "provenance.v001.json"
EVENTS_JSONL  = pathlib.Path(
    r"C:\Users\aab15\Documents\prime-documentary\episodes"
    r"\PD-2026-001-miranda\events.jsonl"
)
FFMPEG        = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE       = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

VOICE_ID      = "nPczCjzI2devNBz1zQrb"   # Brian
MODEL_ID      = "eleven_multilingual_v2"
EL_TTS_URL    = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

VOICE_SETTINGS = {
    "stability": 0.60,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": True,
}

# ── Helpers ─────────────────────────────────────────────────────────────────

def _load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _probe_duration(path: pathlib.Path) -> float:
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return round(float(r.stdout.strip()), 3)


def _loudnorm(raw: pathlib.Path, out: pathlib.Path) -> None:
    """Single-pass loudnorm to -16 LUFS / -1.5 TP / LRA 11."""
    tmp = out.parent / (out.stem + ".norm_tmp.mp3")  # explicit .mp3 so ffmpeg picks format
    r = subprocess.run([
        FFMPEG, "-y", "-i", str(raw),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-f", "mp3", "-c:a", "libmp3lame", "-b:a", "192k",
        str(tmp),
    ], capture_output=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"loudnorm failed: {r.stderr[-500:]}")
    tmp.replace(out)


def _generate_tts(api_key: str, text: str, retries: int = 3) -> bytes:
    payload = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
    }).encode("utf-8")
    req = urllib.request.Request(
        EL_TTS_URL,
        data=payload,
        method="POST",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
    )
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            body = e.read(300).decode("utf-8", errors="replace")
            if e.code == 429 or e.code >= 500:
                wait = 6 * attempt
                print(f"    HTTP {e.code} attempt {attempt}/{retries}, retry {wait}s: {body[:100]}")
                time.sleep(wait)
                continue
            raise RuntimeError(f"ElevenLabs HTTP {e.code}: {body}") from e
    raise RuntimeError(f"All {retries} TTS attempts failed")


def _load_provenance() -> dict:
    if PROV_PATH.exists():
        return json.loads(PROV_PATH.read_text(encoding="utf-8"))
    return {"voice_plan_id": "VP-PD-2026-001-miranda", "chunks": {}}


def _save_provenance(prov: dict) -> None:
    tmp = PROV_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(PROV_PATH)


def _append_event(event: dict) -> None:
    with EVENTS_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


# ── Main ────────────────────────────────────────────────────────────────────

def main(dry_run: bool = False) -> None:
    env = _load_env()
    api_key = env.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set in .env")

    plan = json.loads(VOICE_PLAN.read_text(encoding="utf-8"))
    chunks = plan["chunks"]
    DRAFT_DIR.mkdir(parents=True, exist_ok=True)

    prov = _load_provenance()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    generated: list[str] = []
    skipped:   list[str] = []
    failed:    list[str] = []

    for chunk in chunks:
        cid   = chunk["chunk_id"]
        text  = chunk["spoken_text"]
        h     = _content_hash(text)
        out   = DRAFT_DIR / f"{cid}.mp3"

        existing = prov["chunks"].get(cid, {})
        if existing.get("content_hash") == h and out.exists():
            print(f"  SKIP {cid} (content unchanged)")
            skipped.append(cid)
            continue

        chars = len(text)
        print(f"  GEN  {cid}  {chars} chars  {'[DRY]' if dry_run else ''}")
        if dry_run:
            continue

        try:
            raw_tmp = DRAFT_DIR / f"{cid}.raw.partial"

            # ① TTS → raw bytes (skip if cached from a previous failed run)
            if raw_tmp.exists():
                print(f"    reuse cached raw ({raw_tmp.stat().st_size // 1024} KB)")
                raw_bytes = raw_tmp.read_bytes()
            else:
                raw_bytes = _generate_tts(api_key, text)
                raw_tmp.write_bytes(raw_bytes)

            # ② loudnorm → normalized MP3
            _loudnorm(raw_tmp, out)
            raw_tmp.unlink(missing_ok=True)

            # ③ Measure
            dur      = _probe_duration(out)
            fhash    = hashlib.sha256(out.read_bytes()).hexdigest()

            # ④ Provenance
            prov["chunks"][cid] = {
                "chunk_id":     cid,
                "content_hash": h,
                "file_sha256":  fhash,
                "duration_sec": dur,
                "voice_id":     VOICE_ID,
                "model_id":     MODEL_ID,
                "lufs_target":  -16,
                "generated_at": now,
                "filename":     out.name,
            }
            _save_provenance(prov)
            generated.append(cid)
            print(f"    ✓ {out.name}  {dur:.1f}s  {len(raw_bytes)/1024:.0f} KB raw")
            time.sleep(0.3)

        except Exception as e:
            print(f"    ✗ {cid} FAILED: {e}")
            failed.append(cid)

    if not dry_run and generated:
        _append_event({
            "event":      "narration_generated",
            "episode_id": "PD-2026-001-miranda",
            "stage":      "audio_generating",
            "revision":   "v001",
            "voice_id":   VOICE_ID,
            "model_id":   MODEL_ID,
            "generated":  generated,
            "skipped":    skipped,
            "failed":     failed,
            "output_dir": str(DRAFT_DIR),
            "timestamp":  now,
        })

    print(f"\n{'='*54}")
    print(f"Generated : {len(generated)}")
    print(f"Skipped   : {len(skipped)}")
    print(f"Failed    : {len(failed)}")
    if failed:
        print(f"Failed IDs: {failed}")
    print(f"Output    : {DRAFT_DIR}")
    print(f"Provenance: {PROV_PATH}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    main(dry_run=args.dry_run)
