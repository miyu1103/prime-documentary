#!/usr/bin/env python3
"""Generate Gideon (EP2) narration from voice_plan.v001.json via ElevenLabs TTS.

PAID but in-plan. Idempotent: skips a chunk whose mp3 already exists (non-empty).
Delivery markers (calm/building/intense) map to voice_settings for dynamic delivery.
Output: <media>/episodes/PD-2026-002-gideon/06_voice/draft/<chunk_id>.mp3
Also writes 06_audio/narration_index.v001.json (durations) for caption sync + assembly.

Usage: py -3.11 scripts/gen_narration_gideon.py [--dry-run]
"""
from __future__ import annotations
import argparse, json, subprocess, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-002-gideon"
VOICE_PLAN = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
MODEL = "eleven_multilingual_v2"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm":     {"stability": 0.55, "similarity_boost": 0.80, "style": 0.15, "use_speaker_boost": True},
    "building": {"stability": 0.45, "similarity_boost": 0.80, "style": 0.35, "use_speaker_boost": True},
    "intense":  {"stability": 0.32, "similarity_boost": 0.85, "style": 0.55, "use_speaker_boost": True},
}

def load_env() -> dict:
    env = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("="); env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def media_root() -> Path:
    cfg = json.loads((ROOT / "config/storage.local.json").read_text(encoding="utf-8"))
    return Path(cfg["roots"]["media"]["path"])

def dur(p: Path) -> float:
    try:
        r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],
                           capture_output=True, text=True)
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return 0.0

def main(argv) -> int:
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    vp = json.loads(VOICE_PLAN.read_text(encoding="utf-8"))
    env = load_env()
    key = env.get("ELEVENLABS_API_KEY")
    vid = vp.get("voice_id") or env.get("ELEVENLABS_VOICE_ID")
    chunks = vp["chunks"]
    total_chars = sum(len(c["spoken_text"]) for c in chunks)
    print(f"chunks={len(chunks)} chars={total_chars} est=${total_chars/1000*0.30:.2f} voice={vid} model={MODEL}")
    if args.dry_run:
        print("[dry-run] no API calls."); return 0
    if not key:
        print("ERROR: ELEVENLABS_API_KEY missing"); return 1

    outdir = media_root() / "episodes" / EP / "06_voice" / "draft"
    outdir.mkdir(parents=True, exist_ok=True)
    index = []
    made = skipped = failed = 0
    for c in chunks:
        cid = c["chunk_id"]; text = c["spoken_text"]; delivery = c.get("delivery","calm")
        out = outdir / f"{cid}.mp3"
        if out.exists() and out.stat().st_size > 1024:
            skipped += 1; index.append({"chunk_id": cid, "file": out.name, "delivery": delivery, "seconds": dur(out)}); continue
        body = json.dumps({"text": text, "model_id": MODEL, "voice_settings": SETTINGS.get(delivery, SETTINGS["calm"])}).encode()
        req = urllib.request.Request(TTS.format(vid=vid), data=body,
            headers={"xi-api-key": key, "Content-Type":"application/json", "Accept":"audio/mpeg"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            out.write_bytes(data)
            d = dur(out)
            index.append({"chunk_id": cid, "file": out.name, "delivery": delivery, "seconds": d})
            made += 1; print(f"  [{cid}] {delivery:8s} {len(text):4d}ch -> {len(data)//1024}KB {d}s")
            time.sleep(0.4)
        except urllib.error.HTTPError as e:
            failed += 1; print(f"  [{cid}] HTTP {e.code}: {e.read().decode(errors='replace')[:160]}")
        except Exception as e:
            failed += 1; print(f"  [{cid}] ERR {e}")

    idx = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
    idx.write_text(json.dumps({"episode_id": EP, "voice_id": vid, "model_id": MODEL,
        "generated_total_seconds": round(sum(i["seconds"] for i in index),2), "chunks": index}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"\nmade={made} skipped={skipped} failed={failed}  total={sum(i['seconds'] for i in index):.1f}s")
    print(f"index -> {idx.relative_to(ROOT)}")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
