#!/usr/bin/env python3
"""Generate PD-2026-033-tyler narration with the channel voice (ElevenLabs).

Paid API. Source of truth = the VERBATIM narration_index.v001.json (167 spoken chunks — the caption
source). Idempotent: existing non-empty chunk mp3s are skipped (no double-charge). Run --dry-run
first to see chars + $ estimate with NO API call and NO media writes.

Modeled on scripts/gen_narration_carsearch.py. Differences for this episode:
  * INDEX_SRC = narration_index.v001.json (this episode ships a single rich v001 index).
  * VOICE_ID is read from .env (ELEVENLABS_VOICE_ID, fallback VOICE_ID), not hard-coded.
  * DELIVERY_BY_SECTION maps THIS episode's section names.
  * The index is stamped IN PLACE: the runner adds each chunk's real start/end/seconds (measured by
    ffprobe on the concatenated master, including inter-chunk silence) WITHOUT discarding the index's
    existing schema/metadata. Chunk order and count are preserved 1:1 so the per-chunk caption
    windows (align_windowed) stay paired to the verbatim text.

Downstream contract (do not change layout — these consumers depend on it):
  * master  -> H:\\pd-media\\episodes\\<EP>\\06_voice\\master\\vc_master_v001.mp3
              (gen_captions_forced.resolve_master / verify_caption_sync.resolve_master glob
               vc_master_v*.mp3 here).
  * windows -> 06_audio/narration_index.v001.json chunks[].start/end (align_windowed + both gates).
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
EP = "PD-2026-033-tyler"
INDEX_SRC = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
SCRIPT_REVISION = "v001"
MODEL = "eleven_multilingual_v2"
VOICE_ID = ""  # resolved from .env in main() before any chunk work
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
# section (narration_index v001) -> delivery arc
DELIVERY_BY_SECTION = {
    "COLD_OPEN_PARADOX": "intense",
    "THESIS_AND_PROMISE": "building",
    "SETUP_CHARACTER_AND_DEBT": "building",
    "SEIZURE_AND_SURPLUS": "building",
    "PARALLEL_CASE_AND_SCALE": "building",
    "HISTORY_AND_ARGUMENT": "building",
    "RULING_AND_PAYOFF": "intense",
    "CODA_AND_CTA": "calm",
}


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
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
                           "script_revision": SCRIPT_REVISION}, sort_keys=True)
    return "sha256:" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def parse_chunks() -> list[dict[str, str]]:
    idx = json.loads(INDEX_SRC.read_text("utf-8"))
    chunks: list[dict[str, str]] = []
    for i, c in enumerate(idx["chunks"], start=1):
        section = c.get("section", "SETUP_CHARACTER_AND_DEBT")
        text = " ".join(c["text"].split()).strip()
        cid = c.get("voice_chunk_id") or f"VC-{i:04d}"
        chunks.append({
            "chunk_id": cid,
            "span_id": c.get("span_id", cid),
            "section": section,
            "delivery": DELIVERY_BY_SECTION.get(section, "building"),
            "spoken_text": text,
            "text_sha256": sha_text(text),
            "idempotency_key": idempotency_key(text, cid),
        })
    return chunks


def concat_master(chunks: list[dict[str, str]], outdir: Path, master: Path) -> list[dict]:
    """Concatenate every chunk mp3 (with breathing silence) into the master and return per-chunk
    start/end/seconds measured on the assembled timeline (cursor accumulates real durations + gaps).
    """
    index: list[dict] = []
    GAP_BEAT, GAP_SECTION = 0.6, 2.5   # within-section beat gap / section-boundary breath
    sil_beat = outdir / "_silence_060.mp3"
    sil_sec = outdir / "_silence_250.mp3"
    for _p, _t in ((sil_beat, GAP_BEAT), (sil_sec, GAP_SECTION)):
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                        "-t", f"{_t}", "-c:a", "libmp3lame", "-b:a", "192k", str(_p)], check=True)
    cursor = 0.0
    lines: list[str] = []
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
            boundary = c["section"] != chunks[i + 1]["section"]
            gap = GAP_SECTION if boundary else GAP_BEAT
            lines.append(f"file '{(sil_sec if boundary else sil_beat).as_posix()}'\n")
            cursor += gap
    concat = outdir / "_concat.txt"
    concat.write_text("".join(lines), "utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True)
    return index


def write_voice_plan(chunks: list[dict[str, str]]) -> None:
    p = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"episode_id": EP, "revision": "v001", "provider": "ElevenLabs",
                             "voice_id": VOICE_ID, "model_id": MODEL, "chunks": chunks},
                            indent=2, ensure_ascii=False) + "\n", "utf-8")


def stamp_index(index: list[dict], master: Path, est: float) -> None:
    """Stamp real per-chunk start/end/seconds into narration_index.v001.json IN PLACE, preserving
    the existing schema/metadata. Chunk order/count are unchanged (matched 1:1 by voice_chunk_id)."""
    data = json.loads(INDEX_SRC.read_text("utf-8"))
    by_id = {e["chunk_id"]: e for e in index}
    total = round(dur(master), 3)
    for c in data.get("chunks", []):
        cid = c.get("voice_chunk_id")
        e = by_id.get(cid)
        if not e:
            continue
        c["start"] = e["start"]
        c["end"] = e["end"]
        c["seconds"] = e["seconds"]
    gen = data.setdefault("generation", {})
    gen.update({
        "provider": "elevenlabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL,
        "script_revision": SCRIPT_REVISION,
        "estimated_cost_usd": est,
        "generated_total_seconds": total,
        "generated_total_minutes": round(total / 60.0, 2),
        "master": f"artifact://episodes/{EP}/06_voice/master/{master.name}",
        "offsets_include_silence": True,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    })
    tmp = INDEX_SRC.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", "utf-8")
    tmp.replace(INDEX_SRC)


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no API call, no media writes; print cost")
    args = ap.parse_args(argv)

    global VOICE_ID
    env = load_env()
    VOICE_ID = env.get("ELEVENLABS_VOICE_ID") or env.get("VOICE_ID") or ""

    chunks = parse_chunks()
    chars = sum(len(c["spoken_text"]) for c in chunks)
    est = round(chars / 1000 * 0.30, 2)
    print(f"episode={EP} chunks={len(chunks)} chars={chars} est=${est:.2f} "
          f"voice={VOICE_ID or '(unset)'} model={MODEL}")
    if args.dry_run:
        for c in chunks:
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch [{c['section']}]")
        return 0

    write_voice_plan(chunks)
    key = env.get("ELEVENLABS_API_KEY")
    if not key:
        print("ERROR: ELEVENLABS_API_KEY missing")
        return 1
    if not VOICE_ID:
        print("ERROR: ELEVENLABS_VOICE_ID / VOICE_ID missing in .env")
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
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch -> "
                  f"{out.stat().st_size//1024}KB {dur(out):.2f}s")
            made += 1
            time.sleep(0.35)
        except urllib.error.HTTPError as e:
            failed += 1
            print(f"  {c['chunk_id']} HTTP {e.code}: {e.read().decode(errors='replace')[:240]}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  {c['chunk_id']} ERR {e}")
    if failed:
        print(f"made={made} skipped={skipped} failed={failed}  (aborting master/stamp until all "
              f"chunks exist so offsets stay correct)")
        return 1
    master = media_root() / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    index = concat_master(chunks, outdir, master)
    stamp_index(index, master, est)
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({dur(master):.1f}s)")
    print(f"index  -> {INDEX_SRC.relative_to(ROOT)} (stamped start/end for {len(index)} chunks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
