#!/usr/bin/env python3
"""Re-voice PD-2026-035-hinders with the channel voice and rebuild a TIME-FIT master.

Why this exists (CLAUDE invariant 14 — extend, don't fork):
    ``scripts/gen_narration_hinders.py`` generates per-chunk TTS AND stamps NEW
    start/end offsets into ``narration_index.v001.json`` from the fresh chunk
    durations. EP35 was generated with the WRONG voice (n8kTUi6dVrplENT9Un56).
    The owner approved re-generating with the channel voice
    (nPczCjzI2devNBz1zQrb). But the video (burned captions / figures / cuts) is
    already rendering against the FIXED narration_index [start,end] timeline, so
    those offsets MUST NOT change. This script therefore:

      1. Generates the 170 chunks with the CHANNEL voice into a NEW dir
         (06_voice/draft_nPcz) — old wrong-voice draft/ is left untouched.
      2. TIME-FITS each new chunk to its EXISTING narration_index slot
         (end-start) via ffmpeg ``atempo`` (natural stretch, NEVER truncation),
         then reassembles a master (06_voice/master/vc_master_v002.mp3) with the
         SAME inter-chunk silences, so every spoken chunk lands at its index
         start/end and the total equals the index total. narration_index
         start/end/seconds are NOT rewritten.
      3. Updates voice_plan.v001.json + narration_index voice METADATA only.

Idempotent: a chunk mp3 is reused when its sidecar records the same voice_id +
text sha256 (no double-charge on rerun). ``--dry-run`` prints the plan + $ with
NO API call and NO writes. Paid API (ElevenLabs) only without --dry-run.
Modeled on gen_narration_hinders.py (same SETTINGS / delivery arc / model).
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
VOICE_PLAN_PATH = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
MODEL = "eleven_multilingual_v2"
SCRIPT_REVISION = "v001"
EXPECTED_VOICE_PREFIX = "nPczCjzI"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SR = 44100
MASTER_NAME = "vc_master_v002.mp3"

# identical to gen_narration_hinders.py
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
DELIVERY_BY_SECTION = {
    "COLD_OPEN_THREAT": "intense",
    "SETUP_AND_MECHANISM": "building",
    "SEIZURE_AND_INVERSION": "building",
    "TURN_AND_PARTIAL_WIN": "building",
    "FAKE_ENDING_AND_SCALE": "intense",
    "PAYOFF_REFORM_AND_NEXT_LOOP": "building",
    "EARNED_CTA_AND_NEXT_ARC": "calm",
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


def idempotency_key(text: str, chunk_id: str, voice_id: str) -> str:
    material = json.dumps({"episode_id": EP, "chunk_id": chunk_id, "model": MODEL,
                           "voice_id": voice_id, "text_sha256": sha_text(text),
                           "script_revision": SCRIPT_REVISION}, sort_keys=True)
    return "sha256:" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def parse_chunks(index: dict, voice_id: str) -> list[dict]:
    out: list[dict] = []
    for c in index["chunks"]:
        section = str(c.get("section", "SETUP_AND_MECHANISM"))
        text = " ".join(str(c["text"]).split()).strip()
        cid = c["voice_chunk_id"]
        out.append({
            "chunk_id": cid,
            "span_id": c.get("span_id", cid),
            "section": section,
            "delivery": DELIVERY_BY_SECTION.get(section, "building"),
            "spoken_text": text,
            "text_sha256": sha_text(text),
            "idempotency_key": idempotency_key(text, cid, voice_id),
            "start": float(c["start"]),
            "end": float(c["end"]),
        })
    return out


def atempo_chain(factor: float) -> str:
    """ffmpeg atempo supports 0.5..2.0 per stage; chain for anything outside."""
    if abs(factor - 1.0) < 1e-4:
        return "atempo=1.0"
    stages: list[float] = []
    f = factor
    while f > 2.0:
        stages.append(2.0)
        f /= 2.0
    while f < 0.5:
        stages.append(0.5)
        f /= 0.5
    stages.append(f)
    return ",".join(f"atempo={s:.6f}" for s in stages)


def generate(chunks: list[dict], voice_id: str, key: str, outdir: Path) -> tuple[int, int, int]:
    outdir.mkdir(parents=True, exist_ok=True)
    made = skipped = failed = 0
    for c in chunks:
        out = outdir / f"{c['chunk_id']}.mp3"
        side = out.with_suffix(".json")
        if out.exists() and out.stat().st_size > 2048 and side.exists():
            try:
                meta = json.loads(side.read_text("utf-8"))
                if meta.get("voice_id") == voice_id and meta.get("text_sha256") == c["text_sha256"]:
                    skipped += 1
                    continue
            except Exception:
                pass
        body = json.dumps({"text": c["spoken_text"], "model_id": MODEL,
                           "voice_settings": SETTINGS[c["delivery"]]}).encode("utf-8")
        req = urllib.request.Request(TTS.format(vid=voice_id), data=body,
                                     headers={"xi-api-key": key, "Content-Type": "application/json",
                                              "Accept": "audio/mpeg"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            out.write_bytes(data)
            side.write_text(json.dumps(
                {"episode_id": EP, "chunk_id": c["chunk_id"], "section": c["section"],
                 "delivery": c["delivery"], "idempotency_key": c["idempotency_key"], "model_id": MODEL,
                 "voice_id": voice_id, "text_sha256": c["text_sha256"],
                 "characters": len(c["spoken_text"]),
                 "estimated_cost_usd": round(len(c["spoken_text"]) / 1000 * 0.30, 4),
                 "provider": "ElevenLabs", "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")},
                indent=2, ensure_ascii=False) + "\n", "utf-8")
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch -> "
                  f"{out.stat().st_size // 1024}KB {dur(out):.2f}s")
            made += 1
            time.sleep(0.35)
        except urllib.error.HTTPError as e:
            failed += 1
            print(f"  {c['chunk_id']} HTTP {e.code}: {e.read().decode(errors='replace')[:240]}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  {c['chunk_id']} ERR {e}")
    return made, skipped, failed


def build_master(chunks: list[dict], srcdir: Path, workdir: Path, master: Path) -> dict:
    """Time-fit each chunk to its narration_index slot and reassemble a master whose
    spoken windows == the index [start,end] (silences fill the gaps). Returns stats."""
    workdir.mkdir(parents=True, exist_ok=True)
    fit_parts: list[Path] = []
    concat_lines: list[str] = []
    max_factor = 1.0
    warnings: list[str] = []
    n = len(chunks)
    for i, c in enumerate(chunks):
        src = srcdir / f"{c['chunk_id']}.mp3"
        raw = dur(src)
        slot = round(c["end"] - c["start"], 3)
        if slot <= 0:
            raise RuntimeError(f"{c['chunk_id']} non-positive slot {slot}")
        factor = raw / slot  # >1 => new voice longer than slot => speed up to fit
        max_factor = max(max_factor, factor, 1.0 / factor)
        if not (0.90 <= factor <= 1.10):
            warnings.append(f"{c['chunk_id']} atempo={factor:.3f} (raw={raw:.2f}s slot={slot:.2f}s)")
        fit = workdir / f"{c['chunk_id']}.fit.wav"
        af = f"{atempo_chain(factor)},aresample={SR},apad,atrim=end={slot:.6f},asetpts=PTS-STARTPTS"
        subprocess.run(["ffmpeg", "-y", "-i", str(src), "-af", af,
                        "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(fit)],
                       check=True, capture_output=True)
        fit_parts.append(fit)
        concat_lines.append(f"file '{fit.as_posix()}'\n")
        # inter-chunk gap = next.start - this.end (silence). Last chunk: no trailing pad.
        if i != n - 1:
            gap = round(chunks[i + 1]["start"] - c["end"], 3)
            if gap > 0.0005:
                sil = workdir / f"gap_{i:03d}.wav"
                subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                                f"anullsrc=r={SR}:cl=mono", "-t", f"{gap:.6f}",
                                "-c:a", "pcm_s16le", str(sil)], check=True, capture_output=True)
                concat_lines.append(f"file '{sil.as_posix()}'\n")
    concat = workdir / "_concat.txt"
    concat.write_text("".join(concat_lines), "utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(master)],
                   check=True, capture_output=True)
    return {"master_seconds": dur(master), "max_atempo_factor": round(max_factor, 4),
            "warnings": warnings}


def write_voice_plan(chunks: list[dict], voice_id: str) -> None:
    plan = {"episode_id": EP, "revision": "v001", "provider": "ElevenLabs",
            "voice_id": voice_id, "model_id": MODEL,
            "chunks": [{"chunk_id": c["chunk_id"], "span_id": c["span_id"],
                        "section": c["section"], "delivery": c["delivery"],
                        "spoken_text": c["spoken_text"], "text_sha256": c["text_sha256"],
                        "idempotency_key": c["idempotency_key"]} for c in chunks]}
    VOICE_PLAN_PATH.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", "utf-8")


def update_index_metadata(voice_id: str, master_seconds: float) -> tuple[bool, str]:
    """Update ONLY voice metadata in narration_index; assert start/end/seconds unchanged."""
    before = json.loads(INDEX_PATH.read_text("utf-8"))
    before_slots = [(c["voice_chunk_id"], c["start"], c["end"], c["seconds"]) for c in before["chunks"]]
    idx = json.loads(INDEX_PATH.read_text("utf-8"))
    idx["voice_id"] = voice_id
    gen = idx.setdefault("generation", {})
    gen["voice_id"] = voice_id
    gen["master"] = f"artifact://episodes/{EP}/06_voice/master/{MASTER_NAME}"
    gen["revoiced_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    gen["revoice_note"] = ("re-voiced to channel voice nPczCjzI2devNBz1zQrb; per-chunk "
                           "time-fit (atempo) into the fixed narration_index slots so "
                           "start/end/seconds are unchanged (timeline contract preserved)")
    gen["revoiced_master_seconds"] = master_seconds
    INDEX_PATH.write_text(json.dumps(idx, indent=2, ensure_ascii=False) + "\n", "utf-8")
    after = json.loads(INDEX_PATH.read_text("utf-8"))
    after_slots = [(c["voice_chunk_id"], c["start"], c["end"], c["seconds"]) for c in after["chunks"]]
    ok = before_slots == after_slots
    return ok, ("start/end/seconds IDENTICAL before/after" if ok
                else "TIMELINE CHANGED — start/end differ (BUG)")


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no API, no writes; print plan + cost")
    ap.add_argument("--assemble-only", action="store_true",
                    help="skip TTS; only time-fit existing draft_nPcz chunks + rebuild master + metadata")
    args = ap.parse_args(argv)

    env = load_env()
    voice_id = env.get("ELEVENLABS_VOICE_ID", "")
    if not voice_id.startswith(EXPECTED_VOICE_PREFIX):
        print(f"ERROR: .env ELEVENLABS_VOICE_ID={voice_id!r} is not the channel voice "
              f"({EXPECTED_VOICE_PREFIX}...). Refusing.", file=sys.stderr)
        return 2

    index = json.loads(INDEX_PATH.read_text("utf-8"))
    chunks = parse_chunks(index, voice_id)
    chars = sum(len(c["spoken_text"]) for c in chunks)
    est = round(chars / 1000 * 0.30, 2)
    media = media_root()
    draftdir = media / "episodes" / EP / "06_voice" / "draft_nPcz"
    workdir = media / "episodes" / EP / "06_voice" / "_timefit_nPcz"
    master = media / "episodes" / EP / "06_voice" / "master" / MASTER_NAME
    index_total = index["chunks"][-1]["end"]
    print(f"episode={EP} chunks={len(chunks)} chars={chars} est=${est:.2f} "
          f"voice={voice_id} model={MODEL}")
    print(f"index_total={index_total:.3f}s draft={draftdir} master={master.name}")
    if args.dry_run:
        from collections import Counter
        by = Counter(c["delivery"] for c in chunks)
        print("deliveries:", dict(by))
        return 0

    if not args.assemble_only:
        key = env.get("ELEVENLABS_API_KEY")
        if not key:
            print("ERROR: ELEVENLABS_API_KEY missing", file=sys.stderr)
            return 2
        made, skipped, failed = generate(chunks, voice_id, key, draftdir)
        print(f"TTS: made={made} skipped={skipped} failed={failed}")
        if failed:
            print("Some chunks failed -> NOT building master (fix + rerun; idempotent).")
            return 1

    # every chunk file present?
    missing = [c["chunk_id"] for c in chunks if not (draftdir / f"{c['chunk_id']}.mp3").exists()]
    if missing:
        print(f"ERROR: {len(missing)} chunk mp3 missing (e.g. {missing[0]})", file=sys.stderr)
        return 2

    stats = build_master(chunks, draftdir, workdir, master)
    write_voice_plan(chunks, voice_id)
    ok, msg = update_index_metadata(voice_id, stats["master_seconds"])

    print(f"master -> {master} ({stats['master_seconds']:.3f}s; index_total={index_total:.3f}s; "
          f"delta={stats['master_seconds'] - index_total:+.3f}s)")
    print(f"max atempo factor = {stats['max_atempo_factor']} "
          f"({len(stats['warnings'])} chunks beyond +/-10%)")
    for w in stats["warnings"][:12]:
        print("   warn", w)
    print(f"voice_plan -> {VOICE_PLAN_PATH.relative_to(ROOT)} (voice_id={voice_id})")
    print(f"index metadata -> {msg}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
