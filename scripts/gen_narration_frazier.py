#!/usr/bin/env python3
"""Generate PD-2026-039-frazier narration with the channel voice (ElevenLabs).

Paid API. Source of truth = the FINAL script markdown
`episodes/_planning/EP39_frazier_script.en.v001.md`. Unlike the rolin/hinders/
williams runners (which read an existing narration_index), EP39 has no
narration_index yet, so this runner EXTRACTS the spoken narration out of the
markdown and writes both:
  - episodes/<EP>/06_audio/voice_plan.v001.json     (same schema as rolin)
  - episodes/<EP>/06_audio/narration_index.v001.json (caption/window source,
    with measured start/end/seconds stamped after generation)

Extraction is strictly subtractive -- the narration wording is never rewritten.
Everything below is DROPPED and never sent to TTS:
  - 【OST: ...】 on-screen text lines
  - 〔CARD: ...〕 lines
  - [ ... ] stage directions ([SILENCE 2.5秒。...], [FLASH-FORWARD ...],
    [`BrandEndcard` 9秒] ...)
  - markdown headings (## HOOK, ## 事実対応表, ...), the frontmatter block,
    horizontal rules, and every Japanese production note
  - the whole tail from `## 事実対応表` onward
A hard guard (assert_clean) re-scans every spoken_text for CJK characters and
for bracket markers and REFUSES to spend money if any survive.

Voice is PINNED here (channel voice "Brian", measured 176.0 wpm median across 20
shipped episodes -> 2,127 script words ~= 725s, inside the 690-750s band). Do not
swap it; the runtime length gate is calibrated on this voice.

Idempotent: an existing non-empty chunk mp3 is skipped (no double-charge).
Run --dry-run first: prints every chunk's spoken_text with NO API call and NO
writes, so the text can be eyeballed before spending.

Layout (matches gen_captions_forced / verify_caption_sync / build_case_film_audio):
  - per-chunk mp3   : <media>/episodes/<EP>/06_voice/draft/VC-NNNN.mp3
  - narration master: <media>/episodes/<EP>/06_voice/master/vc_master_v001.mp3
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-039-frazier"
SCRIPT_SRC = ROOT / "episodes" / "_planning" / "EP39_frazier_script.en.v001.md"
OUT_DIR = ROOT / "episodes" / EP / "06_audio"
VOICE_PLAN = OUT_DIR / "voice_plan.v001.json"
INDEX_PATH = OUT_DIR / "narration_index.v001.json"

MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"   # PINNED channel voice "Brian" -- do not change
SCRIPT_REVISION = "v001"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
# script act (## heading) -> canonical section name -> delivery arc
DELIVERY_BY_SECTION = {
    "HOOK": "intense",       # flash-forward cold open
    "OPENING": "building",   # thesis
    "ACT_I": "building",     # 1987, the interrogation
    "ACT_II": "building",    # the confession that does not fit
    "ACT_III": "intense",    # Frazier v. Cupp -- the rule
    "ACT_IV": "building",    # sixteen years / scope / reform
    "ENDING": "calm",        # emotional payoff + earned CTA
}
SECTION_ORDER = ["HOOK", "OPENING", "ACT_I", "ACT_II", "ACT_III", "ACT_IV", "ENDING"]
HEADING_TO_SECTION = {
    "HOOK": "HOOK", "OPENING": "OPENING",
    "ACT I": "ACT_I", "ACT II": "ACT_II", "ACT III": "ACT_III", "ACT IV": "ACT_IV",
    "ENDING": "ENDING",
}
# beat 0.6 -> 0.30 (2026-07-20). Measured: 126 beat gaps + 6 section breaths put the
# master at 754.1s, which finishes at ~766s against a 690-750s band. The 6 section
# breaths sit on act boundaries and are scripted craft, so they stay at 2.5s; only the
# mechanical inter-chunk gap is tightened. 0.30 lands the master at ~716s, leaving room
# for the script's [SILENCE] beats to be added at assembly without breaching the ceiling.
GAP_BEAT, GAP_SECTION = 0.30, 2.5
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"

CJK = re.compile(r"[　-〿぀-ゟ゠-ヿ㐀-䶿一-鿿＀-￯]")
ABBREV = re.compile(
    r"\b(?:[A-Z]|Inc|Ltd|Co|Corp|Mr|Mrs|Ms|Dr|Jr|Sr|St|No|Sen|Gov|Rep|Prof|vs|v|al"
    r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\."
)
SENT_SPLIT = re.compile(r'(?<=[.!?])["”]?\s+(?=["“—(]?[A-Z0-9])')


# ---------------------------------------------------------------- extraction

def extract_lines(md: str) -> list[tuple[str, str]]:
    """-> [(section, paragraph_text)] with all non-spoken material removed."""
    out: list[tuple[str, str]] = []
    section: str | None = None
    seen_rule = False
    for raw in md.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            head = line[3:].strip()
            # stop at the production appendix (fact table / revision log)
            if CJK.search(head.split("(")[0].split("—")[0][:6]):
                break
            key = re.split(r"\s+[—(]", head)[0].strip().rstrip("`")
            section = HEADING_TO_SECTION.get(key)
            if section is None:
                break   # unknown heading = not a narration act; stop
            continue
        if line == "---":
            seen_rule = True
            continue
        if not seen_rule or section is None or not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("【") or line.startswith("〔"):   # 【OST】 / 〔CARD〕
            continue
        if line.startswith("[") or line.startswith("**") or line.startswith(">"):
            continue
        if line.startswith("- ") or line.startswith("* "):
            continue
        out.append((section, line))
    return out


def split_sentences(text: str) -> list[str]:
    guarded = ABBREV.sub(lambda m: m.group(0).replace(".", "\x00"), text)
    parts = [p.replace("\x00", ".").strip() for p in SENT_SPLIT.split(guarded)]
    return [" ".join(p.split()) for p in parts if p.strip()]


def build_chunks(md: str) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    n = 0
    for section, para in extract_lines(md):
        for sent in split_sentences(para):
            n += 1
            cid = f"VC-{n:04d}"
            chunks.append({
                "chunk_id": cid,
                "section": section,
                "delivery": DELIVERY_BY_SECTION[section],
                "spoken_text": sent,
                "text_sha256": sha_text(sent),
                "idempotency_key": idempotency_key(sent, cid),
            })
    return chunks


def assert_clean(chunks: list[dict[str, str]]) -> None:
    """Hard gate: refuse to spend money if any production marker leaked into TTS text."""
    bad: list[str] = []
    for c in chunks:
        t = c["spoken_text"]
        if CJK.search(t):
            bad.append(f"{c['chunk_id']}: CJK in spoken_text -> {t[:80]}")
        if re.search(r"[\[\]【】〔〕`#*_]", t):
            bad.append(f"{c['chunk_id']}: markup/marker in spoken_text -> {t[:80]}")
        if "OST" in t or "CARD:" in t or "SILENCE" in t:
            bad.append(f"{c['chunk_id']}: directive keyword -> {t[:80]}")
        if len(t) < 3:
            bad.append(f"{c['chunk_id']}: too short -> {t!r}")
    if bad:
        raise SystemExit("REFUSING TO GENERATE -- unclean chunks:\n  " + "\n  ".join(bad))
    got = [s for s in SECTION_ORDER if any(c["section"] == s for c in chunks)]
    if got != SECTION_ORDER:
        raise SystemExit(f"REFUSING TO GENERATE -- section coverage {got} != {SECTION_ORDER}")


# ---------------------------------------------------------------- helpers

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


def write_voice_plan(chunks: list[dict[str, str]]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    VOICE_PLAN.write_text(json.dumps(
        {"episode_id": EP, "revision": SCRIPT_REVISION, "provider": "ElevenLabs",
         "voice_id": VOICE_ID, "model_id": MODEL, "chunks": chunks},
        indent=2, ensure_ascii=False) + "\n", "utf-8")


def concat_master(chunks: list[dict[str, str]], outdir: Path, master: Path) -> dict[str, dict]:
    """Concat chunk mp3s with inter-chunk silence into a loudnorm'd master; return
    {chunk_id: {start,end,seconds}} (silence EXCLUDED from each chunk window)."""
    sil_beat = outdir / "_silence_060.mp3"
    sil_sec = outdir / "_silence_250.mp3"
    for _p, _t in ((sil_beat, GAP_BEAT), (sil_sec, GAP_SECTION)):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
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
            lines.append(f"file '{(sil_sec if boundary else sil_beat).as_posix()}'\n")
            cursor += GAP_SECTION if boundary else GAP_BEAT
    concat = outdir / "_concat.txt"
    concat.write_text("".join(lines), "utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-af", LOUDNORM, "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True)
    return offsets


def write_index(chunks: list[dict[str, str]], offsets: dict[str, dict],
                master: Path, est_cost: float) -> None:
    total = round(dur(master), 3)
    speech = round(sum(o["seconds"] for o in offsets.values()), 3)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    index = {
        "episode_id": EP,
        "revision": SCRIPT_REVISION,
        "provider": "elevenlabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL,
        "source_script": "episodes/_planning/EP39_frazier_script.en.v001.md",
        "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
        "totals": {
            "chunks": len(chunks),
            "words": words,
            "speech_seconds": speech,
            "measured_seconds": total,
            "measured_minutes": round(total / 60, 2),
            "measured_wpm": round(words / (speech / 60), 1) if speech else 0.0,
        },
        "chunks": [{
            "voice_chunk_id": c["chunk_id"],
            "section": c["section"],
            "text": c["spoken_text"],
            "word_count": len(c["spoken_text"].split()),
            "start": offsets[c["chunk_id"]]["start"],
            "end": offsets[c["chunk_id"]]["end"],
            "seconds": offsets[c["chunk_id"]]["seconds"],
        } for c in chunks],
        "provenance": {
            "producer": "scripts/gen_narration_frazier.py",
            "provider": "ElevenLabs",
            "voice_id": VOICE_ID,
            "model_id": MODEL,
            "estimated_cost_usd": est_cost,
            "gap_beat_seconds": GAP_BEAT,
            "gap_section_seconds": GAP_SECTION,
            "loudnorm": LOUDNORM,
            "master_path_expected": str(master),
            "stamped_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "note": "start/end are per-chunk master offsets (inter-chunk silence excluded from each window).",
        },
    }
    INDEX_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", "utf-8")


# ---------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no API call, no writes; print every chunk")
    ap.add_argument("--plan-only", action="store_true", help="write voice_plan only, no API call")
    ap.add_argument("--remaster", action="store_true", help="skip TTS; rebuild master + index from existing mp3s")
    args = ap.parse_args(argv)

    chunks = build_chunks(SCRIPT_SRC.read_text("utf-8"))
    assert_clean(chunks)
    chars = sum(len(c["spoken_text"]) for c in chunks)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    est = round(chars / 1000 * 0.30, 2)
    print(f"episode={EP} chunks={len(chunks)} words={words} chars={chars} est=${est:.2f} model={MODEL}")
    print(f"projected @176.0wpm = {words / 176.0 * 60:.0f}s (band 690-750s)")

    if args.dry_run:
        for c in chunks:
            print(f"  {c['chunk_id']} {c['section']:8s} {c['delivery']:8s} | {c['spoken_text']}")
        by: dict[str, int] = {}
        for c in chunks:
            by[c["section"]] = by.get(c["section"], 0) + 1
        print(f"  section mix: {by}")
        return 0

    write_voice_plan(chunks)
    print(f"voice_plan -> {VOICE_PLAN.relative_to(ROOT)}")
    if args.plan_only:
        return 0

    outdir = media_root() / "episodes" / EP / "06_voice" / "draft"
    outdir.mkdir(parents=True, exist_ok=True)
    made = skipped = failed = 0

    if not args.remaster:
        env = load_env()
        key = env.get("ELEVENLABS_API_KEY")
        if not key:
            print("ERROR: ELEVENLABS_API_KEY missing")
            return 1
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
            ok = False
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(req, timeout=180) as r:
                        data = r.read()
                    out.write_bytes(data)
                    ok = True
                    break
                except urllib.error.HTTPError as e:
                    msg = e.read().decode(errors="replace")[:200]
                    print(f"  {c['chunk_id']} HTTP {e.code} (try {attempt + 1}): {msg}")
                    if e.code < 500 and e.code != 429:
                        break
                    time.sleep(3 * (attempt + 1))
                except Exception as e:  # noqa: BLE001
                    print(f"  {c['chunk_id']} ERR (try {attempt + 1}) {e}")
                    time.sleep(3 * (attempt + 1))
            if not ok:
                failed += 1
                continue
            d = dur(out)
            out.with_suffix(".json").write_text(json.dumps(
                {"episode_id": EP, "chunk_id": c["chunk_id"], "section": c["section"],
                 "delivery": c["delivery"], "idempotency_key": c["idempotency_key"], "model_id": MODEL,
                 "voice_id": VOICE_ID, "characters": len(c["spoken_text"]), "seconds": d,
                 "estimated_cost_usd": round(len(c["spoken_text"]) / 1000 * 0.30, 4),
                 "provider": "ElevenLabs", "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")},
                indent=2, ensure_ascii=False) + "\n", "utf-8")
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch -> {out.stat().st_size // 1024}KB {d:.2f}s", flush=True)
            made += 1
            time.sleep(0.35)

    if failed:
        print(f"made={made} skipped={skipped} failed={failed} -> NOT building master (fix failures first)")
        return 1

    master = media_root() / "episodes" / EP / "06_voice" / "master" / "vc_master_v001.mp3"
    offsets = concat_master(chunks, outdir, master)
    write_index(chunks, offsets, master, est)
    speech = sum(o["seconds"] for o in offsets.values())
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"speech total = {speech:.1f}s ({speech / 60:.2f}min)  band 690-750s -> "
          f"{'PASS' if 690 <= speech <= 750 else 'FAIL'}")
    print(f"measured wpm = {words / (speech / 60):.1f} (expected ~176.0)")
    print(f"master -> {master} ({dur(master):.1f}s incl. gaps)")
    print(f"index  -> {INDEX_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
