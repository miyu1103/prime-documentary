#!/usr/bin/env python3
"""Generic case-episode narration runner (ElevenLabs) — `--ep <EPID>`.

Invariant 14: this GENERALIZES the proven per-episode lineage (scripts/
gen_narration_morton.py, EP52, shipped) instead of adding a 21st per-episode
copy. All canon settings are preserved from that lineage + scripts/
gen_narration.py (miranda):
  - voice PINNED: Brian nPczCjzI2devNBz1zQrb / eleven_multilingual_v2
  - per-delivery voice settings (calm/building/intense) — the EP52-shipped
    presets that the voice_plan `delivery` vocabulary drives. (gen_narration.py
    EP1 used a single flat setting; EP39+ canon is per-delivery. Recorded as a
    deliberate canon choice: voice must match the last ~15 shipped episodes.)
  - loudnorm QC -16 LUFS / -1.5 TP / LRA 11 (applied once on the master;
    narration_index offsets are measured from the exact concatenated WAVs)
  - retry w/ backoff on 429/5xx, 3 attempts
  - sha-256 idempotency: a chunk is re-generated ONLY if its mp3 is missing/
    truncated or its sidecar text_sha256 no longer matches the script text.
    Re-runs never double-spend.
  - per-chunk provenance sidecar VC-NNNN.json + events.jsonl append
    (gen_narration.py pattern) with characters + estimated cost.

Paid API. Source of truth = the LOCKED _planning script (verbatim; extraction
is strictly subtractive — narration wording is never rewritten).

Outputs (mirrors PD-2026-052-morton exactly):
  episodes/<EPID>/06_audio/voice_plan.v001.json
  episodes/<EPID>/06_audio/narration_index.v001.json  (measured, ffprobe)
  <media>/episodes/<EPID>/06_voice/draft/VC-NNNN.mp3 (+ .json provenance)
  <media>/episodes/<EPID>/06_voice/master/vc_master_v001.mp3
  episodes/<EPID>/events.jsonl (narration_generated / narration_mastered)

--dry-run   prints every chunk, NO API call, NO writes.
--plan-only writes voice_plan only, no API call.
--remaster  skips TTS; rebuilds master + index from existing (already-paid)
            mp3s at zero cost; honours --gap-beat / --gap-section.
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
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"   # PINNED channel voice "Brian"
SCRIPT_REVISION = "v001"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
DELIVERY_BY_SECTION = {
    "HOOK": "intense", "OP": "building", "ACT_1": "building", "ACT_2": "building",
    "ACT_3": "building", "ACT_4": "building", "ENDING": "calm",
}
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ENDING"]
# EP52/53/54/55 headings: `## COLD OPEN ...`, `## OPENING ...`, `## ACT I — ...`
# ... `## ACT IV — ...`, `## ENDING ...` (Roman numerals). Longer numerals FIRST.
SECTION_HEADINGS = [
    ("HOOK", re.compile(r"^COLD\s+OPEN\b", re.IGNORECASE)),
    ("OP", re.compile(r"^OPENING\b", re.IGNORECASE)),
    ("ACT_4", re.compile(r"^ACT\s+IV\b", re.IGNORECASE)),
    ("ACT_3", re.compile(r"^ACT\s+III\b", re.IGNORECASE)),
    ("ACT_2", re.compile(r"^ACT\s+II\b", re.IGNORECASE)),
    ("ACT_1", re.compile(r"^ACT\s+I\b", re.IGNORECASE)),
    ("ENDING", re.compile(r"^ENDING\b", re.IGNORECASE)),
]
# post-ENDING appendix headings (EP53 `Fact Correspondence & Self-Checks`,
# EP54 `Fact Correspondence & Revision Log`, EP55 `Fact Correspondence / ...`,
# plus the EP52 RUNTIME/SELF-CHECK forms).
STOP_HEADINGS = [
    re.compile(r"^Fact\s+Correspondence", re.IGNORECASE),
    re.compile(r"^RUNTIME\b", re.IGNORECASE),
    re.compile(r"^SELF-CHECK\b", re.IGNORECASE),
    re.compile(r"^\*?\[END OF NARRATION", re.IGNORECASE),
    re.compile(r"^事実対応表"),
    re.compile(r"^改稿ログ"),
]

# Episode registry. design_speech_seconds = DESIGN §5 narration model (@178.1
# wpm, speech only, gaps excluded); band = the finished-film 29:00-31:00 model.
EPISODES = {
    "PD-2026-053-norfolk": {
        "planning": "EP53_norfolk_script.en.v001.md",
        "design_speech_seconds": 1564.9,   # DESIGN §5: 1564.9 × 1.150 ≈ 1799.6s film
    },
    "PD-2026-054-flowers": {
        "planning": "EP54_flowers_script.en.v001.md",
        "design_speech_seconds": 1579.3,   # DESIGN §5: 4,688 w @178.1wpm
    },
    "PD-2026-055-burge": {
        "planning": "EP55_burge_script.en.v001.md",
        "design_speech_seconds": 1582.1,   # DESIGN §5: 4,696 w @178.1wpm
    },
}

GAP_BEAT, GAP_SECTION = 0.30, 1.8          # EP52-shipped defaults
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"
COST_PER_1K_CHARS_USD = 0.30

CJK = re.compile(r"[　-〿぀-ゟ゠-ヿ㐀-䶿一-鿿＀-￯]")
SILENCE_LINE = re.compile(r"DESIGNED SILENCE\s+([0-9]+(?:\.[0-9]+)?)\s*s", re.IGNORECASE)
BEAT_LINE = re.compile(r"^【\s*beat\b", re.IGNORECASE)
BEAT_SECONDS = 0.6
INLINE_MARKER = re.compile(r"【[^】]*】|〔[^〕]*〕|\[[^\]]*\]")
ABBREV = re.compile(
    r"\b(?:[A-Z]|Inc|Ltd|Co|Corp|Mr|Mrs|Ms|Dr|Jr|Sr|St|No|Sen|Gov|Rep|Prof|Sgt|vs|v|al"
    r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\.")
SENT_SPLIT = re.compile(r'(?<=[.!?])["”]?\s+(?=["“—(]?[A-Z0-9])')


# ---------------------------------------------------------------- extraction

def clean_quote(line: str) -> str:
    line = re.sub(r"^>\s?", "", line).strip()
    line = re.sub(r"\*\*|\*|`", "", line)
    return " ".join(line.split())


def section_for_heading(head: str) -> tuple[str | None, bool]:
    for sec, pat in SECTION_HEADINGS:
        if pat.match(head):
            return sec, False
    for pat in STOP_HEADINGS:
        if pat.match(head):
            return None, True
    return None, False


def extract_events(md: str) -> list[tuple]:
    """-> ordered events: ("para", section, text) | ("silence", section, seconds)."""
    out: list[tuple] = []
    section: str | None = None
    for raw in md.splitlines():
        line = raw.strip()
        hm = re.match(r"^(#{1,6})\s+(.*)$", line)
        if hm:
            sec, is_stop = section_for_heading(hm.group(2).strip())
            if is_stop:
                break
            section = sec
            continue
        if section is None or not line:
            continue
        sm = SILENCE_LINE.search(line)
        if sm:
            out.append(("silence", section, float(sm.group(1))))
            continue
        if BEAT_LINE.match(line):
            out.append(("silence", section, BEAT_SECONDS))
            continue
        if line == "---":
            continue
        if line.startswith("**[") or line.startswith("*("):
            continue
        if CJK.search(line):        # 【OST: ...】 cards / JP production notes — never narration
            continue
        if line.startswith("|") or line.startswith("#"):
            continue
        if line.startswith(">"):
            text = clean_quote(line)
        elif line.startswith(("- ", "* ")):
            continue
        else:
            text = " ".join(re.sub(r"\*\*|\*|`", "", line).split())
        text = " ".join(INLINE_MARKER.sub(" ", text).split())
        if not text:
            continue
        out.append(("para", section, text))
    return out


def split_sentences(text: str) -> list[str]:
    guarded = ABBREV.sub(lambda m: m.group(0).replace(".", "\x00"), text)
    parts = [p.replace("\x00", ".").strip() for p in SENT_SPLIT.split(guarded)]
    return [" ".join(p.split()) for p in parts if p.strip()]


def sha_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def idempotency_key(ep: str, text: str, chunk_id: str) -> str:
    material = json.dumps({"episode_id": ep, "chunk_id": chunk_id, "model": MODEL,
                           "voice_id": VOICE_ID, "text_sha256": sha_text(text),
                           "script_revision": SCRIPT_REVISION}, sort_keys=True)
    return "sha256:" + hashlib.sha256(material.encode("utf-8")).hexdigest()


def build_chunks(ep: str, md: str) -> list[dict]:
    chunks: list[dict] = []
    n = 0
    for ev in extract_events(md):
        if ev[0] == "silence":
            if chunks:
                chunks[-1]["silence_after_seconds"] = ev[2]
            continue
        _, section, para = ev
        for sent in split_sentences(para):
            n += 1
            cid = f"VC-{n:04d}"
            chunks.append({
                "chunk_id": cid,
                "section": section,
                "delivery": DELIVERY_BY_SECTION[section],
                "spoken_text": sent,
                "text_sha256": sha_text(sent),
                "idempotency_key": idempotency_key(ep, sent, cid),
                "silence_after_seconds": None,
            })
    return chunks


def assert_clean(chunks: list[dict]) -> None:
    """Hard gate: refuse to spend money if any production marker leaked into TTS text."""
    bad: list[str] = []
    for c in chunks:
        t = c["spoken_text"]
        if CJK.search(t):
            bad.append(f"{c['chunk_id']}: CJK in spoken_text -> {t[:80]}")
        if re.search(r"[\[\]【】〔〕`#*_]", t):
            bad.append(f"{c['chunk_id']}: markup/marker in spoken_text -> {t[:80]}")
        if "OST" in t or "CARD:" in t or "SILENCE" in t or "SOUND:" in t or "VISUAL" in t:
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


def append_event(ep: str, event: dict) -> None:
    """gen_narration.py events.jsonl pattern (episodes/<EPID>/events.jsonl)."""
    p = ROOT / "episodes" / ep / "events.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


PLAN_KEYS = ("chunk_id", "section", "delivery", "spoken_text", "text_sha256", "idempotency_key")


def write_voice_plan(ep: str, chunks: list[dict], out_dir: Path, plan_path: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    plan_chunks = [{k: c[k] for k in PLAN_KEYS} for c in chunks]
    plan_path.write_text(json.dumps(
        {"episode_id": ep, "revision": SCRIPT_REVISION, "provider": "ElevenLabs",
         "voice_id": VOICE_ID, "model_id": MODEL, "chunks": plan_chunks},
        indent=2, ensure_ascii=False) + "\n", "utf-8")


def _silence_wav(outdir: Path, seconds: float, cache: dict[float, Path]) -> Path:
    key = round(seconds, 3)
    if key in cache:
        return cache[key]
    p = outdir / f"_silw_{key:.3f}.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                    "-t", f"{key}", "-c:a", "pcm_s16le", str(p)], check=True)
    cache[key] = p
    return p


def concat_master(chunks: list[dict], outdir: Path, master: Path,
                  gap_beat: float, gap_section: float) -> dict[str, dict]:
    """Concat chunk mp3s + inter-chunk silence into a loudnorm'd master.

    HOUR-LONG-SAFE (EP50 lesson): decode every chunk to uniform 44100/mono/s16le
    WAV first; all-WAV concat -> encode ONCE to the MP3 master."""
    wavdir = outdir / "_wav"
    wavdir.mkdir(parents=True, exist_ok=True)
    sil_cache: dict[float, Path] = {}
    cursor = 0.0
    lines: list[str] = []
    offsets: dict[str, dict] = {}
    for i, c in enumerate(chunks):
        src = outdir / f"{c['chunk_id']}.mp3"
        wav = wavdir / f"{c['chunk_id']}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-ar", "44100",
                        "-ac", "1", "-c:a", "pcm_s16le", str(wav)], check=True)
        d = dur(wav)
        offsets[c["chunk_id"]] = {"start": round(cursor, 3), "end": round(cursor + d, 3), "seconds": d}
        lines.append(f"file '{wav.as_posix()}'\n")
        cursor += d
        if i != len(chunks) - 1:
            override = c.get("silence_after_seconds")
            if override is not None:
                gap = float(override)
            else:
                boundary = c["section"] != chunks[i + 1]["section"]
                gap = gap_section if boundary else gap_beat
            lines.append(f"file '{_silence_wav(wavdir, gap, sil_cache).as_posix()}'\n")
            cursor += gap
    concat = outdir / "_concat.txt"
    concat.write_text("".join(lines), "utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    raw = wavdir / "_master_raw.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-c:a", "pcm_s16le", str(raw)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw),
                    "-af", LOUDNORM, "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True)
    return offsets


def write_index(ep: str, source_script_rel: str, chunks: list[dict], offsets: dict[str, dict],
                master: Path, index_path: Path, est_cost: float,
                gap_beat: float, gap_section: float) -> dict:
    total = round(dur(master), 3)
    speech = round(sum(o["seconds"] for o in offsets.values()), 3)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    scripted_silence = round(sum(c["silence_after_seconds"] for c in chunks
                                 if c.get("silence_after_seconds") is not None), 3)
    index = {
        "schema_version": "caniglia_narration.v1",
        "episode_id": ep,
        "revision": SCRIPT_REVISION,
        "is_stub": False,
        "provider": "elevenlabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL,
        "source_script": source_script_rel,
        "master": f"artifact://episodes/{ep}/06_voice/master/vc_master_v001.mp3",
        "total_seconds": total,
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
            "id": c["chunk_id"],
            "section": c["section"],
            "text": c["spoken_text"],
            "spoken_text": c["spoken_text"],
            "word_count": len(c["spoken_text"].split()),
            "start": offsets[c["chunk_id"]]["start"],
            "end": offsets[c["chunk_id"]]["end"],
            "seconds": offsets[c["chunk_id"]]["seconds"],
            "duration": offsets[c["chunk_id"]]["seconds"],
        } for c in chunks],
        "provenance": {
            "producer": "scripts/gen_narration_case.py",
            "provider": "ElevenLabs",
            "voice_id": VOICE_ID,
            "model_id": MODEL,
            "estimated_cost_usd": est_cost,
            "gap_beat_seconds": gap_beat,
            "gap_section_seconds": gap_section,
            "scripted_silence_seconds": scripted_silence,
            "loudnorm": LOUDNORM,
            "master_path_expected": str(master),
            "stamped_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "note": "start/end are per-chunk master offsets (inter-chunk silence excluded "
                    "from each window). Durations MEASURED with ffprobe from generated files.",
        },
    }
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", "utf-8")
    return index


# ---------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ep", required=True, choices=sorted(EPISODES),
                    help="episode id (registry-gated: paid API)")
    ap.add_argument("--dry-run", action="store_true", help="no API call, no writes; print every chunk")
    ap.add_argument("--plan-only", action="store_true", help="write voice_plan only, no API call")
    ap.add_argument("--remaster", action="store_true", help="skip TTS; rebuild master + index from existing mp3s")
    ap.add_argument("--gap-beat", type=float, default=GAP_BEAT, help="inter-sentence gap seconds")
    ap.add_argument("--gap-section", type=float, default=GAP_SECTION, help="section-boundary gap seconds")
    args = ap.parse_args(argv)

    ep = args.ep
    cfg = EPISODES[ep]
    script_src = ROOT / "episodes" / "_planning" / cfg["planning"]
    source_script_rel = f"episodes/_planning/{cfg['planning']}"
    out_dir = ROOT / "episodes" / ep / "06_audio"
    voice_plan = out_dir / "voice_plan.v001.json"
    index_path = out_dir / "narration_index.v001.json"

    chunks = build_chunks(ep, script_src.read_text("utf-8"))
    assert_clean(chunks)
    chars = sum(len(c["spoken_text"]) for c in chunks)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    est = round(chars / 1000 * COST_PER_1K_CHARS_USD, 2)
    design = cfg["design_speech_seconds"]
    print(f"episode={ep} chunks={len(chunks)} words={words} chars={chars} est=${est:.2f} model={MODEL}")
    print(f"projected @178.1wpm = {words / 178.1 * 60:.0f}s speech  (DESIGN §5 model = {design}s)")
    print(f"gaps: beat={args.gap_beat}s section={args.gap_section}s")

    if args.dry_run:
        for c in chunks:
            tail = f"  <SILENCE {c['silence_after_seconds']}s>" if c.get("silence_after_seconds") else ""
            print(f"  {c['chunk_id']} {c['section']:6s} {c['delivery']:8s} | {c['spoken_text']}{tail}")
        by: dict[str, int] = {}
        for c in chunks:
            by[c["section"]] = by.get(c["section"], 0) + 1
        print(f"  section mix: {by}")
        return 0

    write_voice_plan(ep, chunks, out_dir, voice_plan)
    print(f"voice_plan -> {voice_plan.relative_to(ROOT)}")
    if args.plan_only:
        return 0

    outdir = media_root() / "episodes" / ep / "06_voice" / "draft"
    outdir.mkdir(parents=True, exist_ok=True)
    made = skipped = failed = 0
    made_ids: list[str] = []
    skipped_ids: list[str] = []
    failed_ids: list[str] = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if not args.remaster:
        env = load_env()
        key = env.get("ELEVENLABS_API_KEY")
        if not key:
            print("ERROR: ELEVENLABS_API_KEY missing")
            return 1
        for c in chunks:
            out = outdir / f"{c['chunk_id']}.mp3"
            side = out.with_suffix(".json")
            # sha-256 idempotency: existing file + matching text hash -> never re-spend.
            if out.exists() and out.stat().st_size > 2048:
                prev_sha = None
                if side.exists():
                    try:
                        prev_sha = json.loads(side.read_text("utf-8")).get("text_sha256")
                    except Exception:
                        prev_sha = None
                if prev_sha in (None, c["text_sha256"]):
                    skipped += 1
                    skipped_ids.append(c["chunk_id"])
                    continue
                print(f"  {c['chunk_id']} text changed (sha mismatch) -> regenerating")
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
                failed_ids.append(c["chunk_id"])
                continue
            d = dur(out)
            side.write_text(json.dumps(
                {"episode_id": ep, "chunk_id": c["chunk_id"], "section": c["section"],
                 "delivery": c["delivery"], "text_sha256": c["text_sha256"],
                 "idempotency_key": c["idempotency_key"], "model_id": MODEL,
                 "voice_id": VOICE_ID, "characters": len(c["spoken_text"]), "seconds": d,
                 "estimated_cost_usd": round(len(c["spoken_text"]) / 1000 * COST_PER_1K_CHARS_USD, 4),
                 "provider": "ElevenLabs", "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")},
                indent=2, ensure_ascii=False) + "\n", "utf-8")
            print(f"  {c['chunk_id']} {c['delivery']:8s} {len(c['spoken_text']):4d}ch -> "
                  f"{out.stat().st_size // 1024}KB {d:.2f}s", flush=True)
            made += 1
            made_ids.append(c["chunk_id"])
            time.sleep(0.35)

        gen_chars = sum(len(c["spoken_text"]) for c in chunks if c["chunk_id"] in set(made_ids))
        append_event(ep, {
            "event": "narration_generated",
            "episode_id": ep,
            "stage": "audio_generating",
            "revision": SCRIPT_REVISION,
            "provider": "ElevenLabs",
            "voice_id": VOICE_ID,
            "model_id": MODEL,
            "generated": len(made_ids),
            "skipped": len(skipped_ids),
            "failed": failed_ids,
            "characters_sent_this_run": gen_chars,
            "characters_total_plan": chars,
            "estimated_cost_usd_this_run": round(gen_chars / 1000 * COST_PER_1K_CHARS_USD, 2),
            "estimated_cost_usd_total_plan": est,
            "output_dir": str(outdir),
            "timestamp": now,
        })

    if failed:
        print(f"made={made} skipped={skipped} failed={failed} -> NOT building master (fix failures first)")
        return 1

    master = media_root() / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3"
    offsets = concat_master(chunks, outdir, master, args.gap_beat, args.gap_section)
    index = write_index(ep, source_script_rel, chunks, offsets, master, index_path,
                        est, args.gap_beat, args.gap_section)
    speech = index["totals"]["speech_seconds"]
    total = index["total_seconds"]
    append_event(ep, {
        "event": "narration_mastered",
        "episode_id": ep,
        "stage": "audio_generating",
        "revision": SCRIPT_REVISION,
        "provider": "ElevenLabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL,
        "chunks": len(chunks),
        "characters_total_plan": chars,
        "estimated_cost_usd_total_plan": est,
        "speech_seconds": speech,
        "master_seconds": total,
        "audio_minutes": round(total / 60, 2),
        "design_speech_seconds": design,
        "speech_vs_design_delta_s": round(speech - design, 1),
        "gap_beat": args.gap_beat,
        "gap_section": args.gap_section,
        "master": str(master),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"speech total = {speech:.1f}s ({speech / 60:.2f}min)  DESIGN model {design}s  "
          f"delta {speech - design:+.1f}s")
    print(f"MASTER measured narrationSeconds = {total:.3f}s ({total / 60:.2f}min)")
    print(f"measured wpm = {index['totals']['measured_wpm']}")
    print(f"master -> {master}")
    print(f"index  -> {index_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
