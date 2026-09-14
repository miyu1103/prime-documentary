#!/usr/bin/env python3
"""Generate PD-2026-034-rolin narration with the channel voice (ElevenLabs).

Paid API. Source of truth = the EXISTING verbatim narration_index.v001.json
(167 spoken chunks, each with `text` + `voice_chunk_id` + `section`). That file
is ALSO the caption source and the caption/coverage window source, so this
runner STAMPS real per-chunk start/end offsets INTO IT IN PLACE (it does NOT
rewrite it with a different schema): `text`, `voice_chunk_id`, `section`,
`span_id`, and `estimated_duration_seconds` are preserved untouched; `start`,
`end`, `seconds` (measured) are added per chunk, plus a top-level `master`
pointer, measured totals, and a `provenance` block.

Idempotent: an existing non-empty chunk mp3 is skipped (no double-charge).
Run --dry-run first to see chars + $ estimate with NO API call and NO writes.
Modeled on scripts/gen_narration_carsearch.py; the chunk source, the section->
delivery map, and the in-place index stamp differ.

Layout (matches gen_captions_forced.resolve_master / verify_caption_sync /
build_case_film_audio, which all glob 06_voice/master/vc_master_v*.mp3 and look
for per-chunk audio under 06_voice/draft):
  - per-chunk mp3  : <media>/episodes/<EP>/06_voice/draft/VC-NNNN.mp3
  - narration master: <media>/episodes/<EP>/06_voice/master/vc_master_v001.mp3
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
EP = "PD-2026-034-rolin"
INDEX_SRC = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
MODEL = "eleven_multilingual_v2"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
# section (narration_index v001 rolin sections) -> delivery arc
DELIVERY_BY_SECTION = {
    "COLD_OPEN_TEASE": "intense",
    "THESIS_AND_PROMISE": "building",
    "COLD_OPEN_STORY": "building",
    "MECHANISM": "building",
    "SCOPE_AND_HUMAN_COST": "building",
    "TURN_AND_PAYOFF": "building",
    "RECKONING_AND_LIMITS": "intense",
    "PAYOFF_AND_CTA": "calm",
}
GAP_BEAT, GAP_SECTION = 0.6, 2.5   # within-section beat gap / section-boundary breath


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


def idempotency_key(text: str, chunk_id: str, voice_id: str) -> str:
    material = json.dumps({"episode_id": EP, "chunk_id": chunk_id, "model": MODEL,
                           "voice_id": voice_id, "text_sha256": sha_text(text),
                           "script_revision": "v001"}, sort_keys=True)
    return "sha256:" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def load_index() -> dict:
    return json.loads(INDEX_SRC.read_text("utf-8"))


def parse_chunks(index: dict, voice_id: str) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    for c in index["chunks"]:
        section = c.get("section", "COLD_OPEN_STORY")
        text = " ".join(str(c["text"]).split()).strip()
        cid = str(c.get("voice_chunk_id") or c.get("chunk_id"))
        chunks.append({
            "chunk_id": cid,
            "section": section,
            "delivery": DELIVERY_BY_SECTION.get(section, "building"),
            "spoken_text": text,
            "text_sha256": sha_text(text),
            "idempotency_key": idempotency_key(text, cid, voice_id),
        })
    return chunks


def concat_master(chunks: list[dict[str, str]], outdir: Path, master: Path) -> dict[str, dict]:
    """Concat all chunk mp3s with inter-chunk silences into the master, and return
    {chunk_id: {"start","end","seconds"}} for the window (silence EXCLUDED from each
    chunk window, matching how captions/coverage/audio read [start,end])."""
    sil_beat = outdir / "_silence_060.mp3"
    sil_sec = outdir / "_silence_250.mp3"
    for _p, _t in ((sil_beat, GAP_BEAT), (sil_sec, GAP_SECTION)):
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                        "-t", f"{_t}", "-c:a", "libmp3lame", "-b:a", "192k", str(_p)], check=True)
    cursor = 0.0
    lines: list[str] = []
    offsets: dict[str, dict] = {}
    for i, c in enumerate(chunks):
        path = outdir / f"{c['chunk_id']}.mp3"
        d = dur(path)
        offsets[c["chunk_id"]] = {"start": round(cursor, 3), "end": round(cursor + d, 3), "seconds": d}
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
    return offsets


def write_voice_plan(chunks: list[dict[str, str]], voice_id: str) -> None:
    p = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"episode_id": EP, "revision": "v001", "provider": "ElevenLabs",
                             "voice_id": voice_id, "model_id": MODEL, "chunks": chunks},
                            indent=2, ensure_ascii=False) + "\n", "utf-8")


def stamp_index(index: dict, offsets: dict[str, dict], master: Path,
                voice_id: str, est_cost: float) -> None:
    """Add measured start/end/seconds to each chunk IN PLACE and update totals +
    provenance, preserving text/voice_chunk_id/section/span_id/estimated_*."""
    total = 0.0
    for c in index["chunks"]:
        cid = str(c.get("voice_chunk_id") or c.get("chunk_id"))
        off = offsets.get(cid)
        if off:
            c["start"] = off["start"]
            c["end"] = off["end"]
            c["seconds"] = off["seconds"]
            total = max(total, off["end"])
    measured_total = round(dur(master), 3)
    index["provider"] = "elevenlabs"
    index["voice_id"] = voice_id
    index["model_id"] = MODEL
    index["master"] = f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3"
    index.setdefault("totals", {})
    index["totals"]["measured_seconds"] = measured_total
    index["totals"]["measured_minutes"] = round(measured_total / 60, 2)
    index["provenance"] = {
        "producer": "scripts/gen_narration_rolin.py",
        "provider": "ElevenLabs",
        "voice_id": voice_id,
        "model_id": MODEL,
        "estimated_cost_usd": est_cost,
        "gap_beat_seconds": GAP_BEAT,
        "gap_section_seconds": GAP_SECTION,
        "master_path_expected": str(master),
        "stamped_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "note": "start/end are per-chunk master offsets (inter-chunk silence excluded from each window).",
    }
    INDEX_SRC.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", "utf-8")


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no API call, no media writes; print cost")
    args = ap.parse_args(argv)

    env = load_env()
    voice_id = env.get("ELEVENLABS_VOICE_ID") or "(unset)"
    index = load_index()
    chunks = parse_chunks(index, voice_id)
    chars = sum(len(c["spoken_text"]) for c in chunks)
    est = round(chars / 1000 * 0.30, 2)
    print(f"episode={EP} chunks={len(chunks)} chars={chars} est=${est:.2f} model={MODEL}")
    if args.dry_run:
        by_delivery: dict[str, int] = {}
        for c in chunks:
            by_delivery[c["delivery"]] = by_delivery.get(c["delivery"], 0) + 1
        for c in chunks[:8]:
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch [{c['section']}]")
        print(f"  ... ({len(chunks)} chunks total)")
        print(f"  delivery mix: {by_delivery}")
        return 0

    key = env.get("ELEVENLABS_API_KEY")
    if not key:
        print("ERROR: ELEVENLABS_API_KEY missing")
        return 1
    if voice_id == "(unset)":
        print("ERROR: ELEVENLABS_VOICE_ID missing")
        return 1
    write_voice_plan(chunks, voice_id)
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
        req = urllib.request.Request(TTS.format(vid=voice_id), data=body,
                                     headers={"xi-api-key": key, "Content-Type": "application/json",
                                              "Accept": "audio/mpeg"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            out.write_bytes(data)
            out.with_suffix(".json").write_text(json.dumps(
                {"episode_id": EP, "chunk_id": c["chunk_id"], "section": c["section"],
                 "delivery": c["delivery"], "idempotency_key": c["idempotency_key"], "model_id": MODEL,
                 "voice_id": voice_id, "characters": len(c["spoken_text"]),
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
    if failed:
        print(f"made={made} skipped={skipped} failed={failed} -> NOT stamping index (fix failures first)")
        return 1
    master = media_root() / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    offsets = concat_master(chunks, outdir, master)
    stamp_index(index, offsets, master, voice_id, est)
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({dur(master):.1f}s)")
    print(f"index  -> {INDEX_SRC.relative_to(ROOT)} (start/end stamped on {len(offsets)} chunks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
