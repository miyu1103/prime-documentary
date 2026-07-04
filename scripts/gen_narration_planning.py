#!/usr/bin/env python3
r"""Generate EP28-30 narration (ElevenLabs) from the _planning annotated JSON.

Parametric version of gen_narration_forfeiture.py: chunks = annotated spans, delivery
by act, canonical channel voice, idempotent (skips existing chunks -> no double
charge). Run --dry-run first for chars + $ with NO API call / NO media writes.

    py -3.11 scripts/gen_narration_planning.py --slug hinton --dry-run
    py -3.11 scripts/gen_narration_planning.py --slug hinton
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
SLUGS = {
    "forfeiture": ("PD-2026-028-forfeiture", "EP28_forfeiture"),
    "hinton": ("PD-2026-029-hinton", "EP29_hinton"),
    "cotton": ("PD-2026-030-cotton", "EP30_cotton"),
}
MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
DELIVERY_BY_CHAPTER = {"hook": "intense", "opening": "building", "act1": "building",
                       "act2": "building", "act3": "intense", "act4": "building", "ending": "calm"}


def load_env():
    env = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text("utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def media_root():
    return Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])


def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 3)
    except Exception:
        return 0.0


def sha_text(t):
    return "sha256:" + hashlib.sha256(t.encode("utf-8")).hexdigest()


def parse_chunks(ep, annot):
    ann = json.loads(annot.read_text("utf-8"))
    span_chapter = {sid: c["chapter_id"] for c in ann["chapters"] for sid in c["span_ids"]}
    title = {c["chapter_id"]: c["title"] for c in ann["chapters"]}
    chunks = []
    for i, s in enumerate(ann["spans"], 1):
        ch = span_chapter.get(s["span_id"], "act1")
        text = " ".join(s["text"].split()).strip()
        cid = f"VC-{i:04d}"
        mat = json.dumps({"episode_id": ep, "chunk_id": cid, "model": MODEL, "voice_id": VOICE_ID,
                          "text_sha256": sha_text(text), "script_revision": "v001"}, sort_keys=True)
        chunks.append({"chunk_id": cid, "span_id": s["span_id"], "section": title.get(ch, ch),
                       "delivery": DELIVERY_BY_CHAPTER.get(ch, "building"), "spoken_text": text,
                       "text_sha256": sha_text(text),
                       "idempotency_key": "sha256:" + hashlib.sha256(mat.encode()).hexdigest()})
    return chunks


def concat_master(chunks, outdir, master):
    index = []
    silence = outdir / "_silence_035.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.35",
                    "-c:a", "libmp3lame", "-b:a", "192k", str(silence)], check=True)
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
    (outdir / "_concat.txt").write_text("".join(lines), "utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(outdir / "_concat.txt"),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True)
    return index


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, choices=list(SLUGS))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    ep, planbase = SLUGS[args.slug]
    annot = ROOT / "episodes" / "_planning" / f"{planbase}_script.annotated.v001.json"
    chunks = parse_chunks(ep, annot)
    chars = sum(len(c["spoken_text"]) for c in chunks)
    est = round(chars / 1000 * 0.30, 2)
    print(f"episode={ep} chunks={len(chunks)} chars={chars} est=${est:.2f}")
    if args.dry_run:
        return 0
    # voice_plan (git-tracked)
    vp = ROOT / "episodes" / ep / "06_audio" / "voice_plan.v001.json"
    vp.parent.mkdir(parents=True, exist_ok=True)
    vp.write_text(json.dumps({"episode_id": ep, "revision": "v001", "provider": "ElevenLabs",
                              "voice_id": VOICE_ID, "model_id": MODEL, "chunks": chunks},
                             indent=2, ensure_ascii=False) + "\n", "utf-8")
    key = load_env().get("ELEVENLABS_API_KEY")
    if not key:
        print("ERROR: ELEVENLABS_API_KEY missing")
        return 1
    outdir = media_root() / "episodes" / ep / "06_voice" / "draft"
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
                out.write_bytes(r.read())
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch -> {out.stat().st_size//1024}KB {dur(out):.2f}s")
            made += 1
            time.sleep(0.35)
        except urllib.error.HTTPError as e:
            failed += 1
            print(f"  {c['chunk_id']} HTTP {e.code}: {e.read().decode(errors='replace')[:200]}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  {c['chunk_id']} ERR {e}")
    master = media_root() / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3"
    index = concat_master(chunks, outdir, master)
    idx = ROOT / "episodes" / ep / "06_audio" / "narration_index.v001.json"
    idx.parent.mkdir(parents=True, exist_ok=True)
    idx.write_text(json.dumps({"episode_id": ep, "voice_id": VOICE_ID, "model_id": MODEL,
                               "estimated_cost_usd": est, "generated_total_seconds": round(dur(master), 2),
                               "master": f"artifact://episodes/{ep}/06_voice/master/vc_master_v001.mp3",
                               "chunks": index}, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"made={made} skipped={skipped} failed={failed} master={dur(master):.1f}s")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
