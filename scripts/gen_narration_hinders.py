#!/usr/bin/env python3
"""Generate PD-2026-035-hinders narration with the channel voice (ElevenLabs).

Paid API. Source of truth = the VERBATIM 06_audio/narration_index.v001.json chunks
(`voice_chunk_id` + `text`), which are ALSO the caption source (字幕=ナレ一致). This
episode has a single narration_index.v001.json that already carries the verbatim
`text`, so we STAMP the real per-chunk start/end offsets back IN PLACE (preserving
`text`, `voice_chunk_id`, `section`, `span_id`, `word_count`) instead of rewriting
the schema. That keeps captions (resolve_text_source reads `text` from v001) and the
sync/coverage windows (load_windows reads start/end from v001) consistent from one
file.

Idempotent: existing non-empty chunk mp3s are skipped (no double-charge). Run
--dry-run first to see chars + $ estimate with NO API call and NO media writes.
Modeled on scripts/gen_narration_carsearch.py; differences: (1) chunk source is the
in-place v001 `text`/`voice_chunk_id`; (2) delivery arc keyed on this episode's
section names; (3) offsets are stamped in place (v001 verbatim `text` preserved).
Voice id is read from .env ELEVENLABS_VOICE_ID at generation time.
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
EP = "PD-2026-035-hinders"
INDEX_PATH = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
MODEL = "eleven_multilingual_v2"
SCRIPT_REVISION = "v001"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
# section (this episode's narration_index) -> delivery arc
DELIVERY_BY_SECTION = {
    "COLD_OPEN_THREAT": "intense",
    "SETUP_AND_MECHANISM": "building",
    "SEIZURE_AND_INVERSION": "building",
    "TURN_AND_PARTIAL_WIN": "building",
    "FAKE_ENDING_AND_SCALE": "intense",
    "PAYOFF_REFORM_AND_NEXT_LOOP": "building",
    "EARNED_CTA_AND_NEXT_ARC": "calm",
}
GAP_BEAT, GAP_SECTION = 0.6, 2.5   # breathing: within-section beat gap / section-boundary breath


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


def load_index() -> dict:
    return json.loads(INDEX_PATH.read_text("utf-8"))


def parse_chunks(index: dict) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    for c in index["chunks"]:
        section = c.get("section", "SETUP_AND_MECHANISM")
        text = " ".join(c["text"].split()).strip()
        cid = c["voice_chunk_id"]
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
    """Concat the per-chunk mp3s with breathing silences into one master and return the per-chunk
    [start,end,seconds] windows (SPEECH windows only; silences advance the cursor but are excluded
    from each window, exactly what the sync/coverage gates expect)."""
    windows: list[dict] = []
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
        windows.append({"chunk_id": c["chunk_id"], "start": round(cursor, 3),
                        "end": round(cursor + d, 3), "seconds": d})
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
    return windows


def write_voice_plan(chunks: list[dict[str, str]]) -> None:
    p = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"episode_id": EP, "revision": "v001", "provider": "ElevenLabs",
                             "voice_id": VOICE_ID, "model_id": MODEL, "chunks": chunks},
                            indent=2, ensure_ascii=False) + "\n", "utf-8")


def stamp_index(index: dict, windows: list[dict], chunks: list[dict[str, str]],
                master: Path, est: float) -> None:
    """Stamp real per-chunk start/end/seconds IN PLACE, preserving text/voice_chunk_id/section."""
    win_by_id = {w["chunk_id"]: w for w in windows}
    deliv_by_id = {c["chunk_id"]: c["delivery"] for c in chunks}
    total = 0.0
    for c in index["chunks"]:
        w = win_by_id.get(c["voice_chunk_id"])
        if not w:
            continue
        c["start"] = w["start"]
        c["end"] = w["end"]
        c["seconds"] = w["seconds"]
        c["delivery"] = deliv_by_id.get(c["voice_chunk_id"], "building")
        total = max(total, w["end"])
    real_total = round(dur(master), 3)
    index["provider"] = "elevenlabs"
    index["voice_id"] = VOICE_ID
    index["model_id"] = MODEL
    index.setdefault("totals", {})
    index["totals"]["generated_seconds"] = real_total
    index["totals"]["generated_minutes"] = round(real_total / 60.0, 2)
    index["generation"] = {
        "provider": "ElevenLabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL,
        "master": f"artifact://episodes/{EP}/06_voice/master/{master.name}",
        "estimated_cost_usd": est,
        "generated_total_seconds": real_total,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "gap_beat_seconds": GAP_BEAT,
        "gap_section_seconds": GAP_SECTION,
    }
    INDEX_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", "utf-8")


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
    VOICE_ID = env.get("ELEVENLABS_VOICE_ID", "")

    index = load_index()
    chunks = parse_chunks(index)
    chars = sum(len(c["spoken_text"]) for c in chunks)
    est = round(chars / 1000 * 0.30, 2)
    print(f"episode={EP} chunks={len(chunks)} chars={chars} est=${est:.2f} "
          f"voice={VOICE_ID or '(ELEVENLABS_VOICE_ID missing)'} model={MODEL}")
    if args.dry_run:
        from collections import Counter
        by_sec = Counter(c["section"] for c in chunks)
        for sec, n in by_sec.items():
            print(f"  section {sec:32s} {n:3d} chunks -> {DELIVERY_BY_SECTION.get(sec,'building')}")
        for c in chunks[:5] + chunks[-3:]:
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch [{c['section']}]")
        return 0

    if not VOICE_ID:
        print("ERROR: ELEVENLABS_VOICE_ID missing from .env")
        return 1
    key = env.get("ELEVENLABS_API_KEY")
    if not key:
        print("ERROR: ELEVENLABS_API_KEY missing")
        return 1

    write_voice_plan(chunks)
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
        print(f"made={made} skipped={skipped} failed={failed} -> NOT stamping index (fix failures first)")
        return 1
    master = media_root() / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    windows = concat_master(chunks, outdir, master)
    stamp_index(index, windows, chunks, master, est)
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"master -> {master} ({dur(master):.1f}s)")
    print(f"index  -> {INDEX_PATH.relative_to(ROOT)} (start/end stamped in place, {len(windows)} chunks)")
    return 0


if __name__ == "__main__":
    VOICE_ID = ""  # set in main() from .env
    raise SystemExit(main(sys.argv[1:]))
