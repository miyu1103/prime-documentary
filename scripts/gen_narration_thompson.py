#!/usr/bin/env python3
"""Generate PD-2026-041-thompson narration with the channel voice (ElevenLabs).

Cloned from scripts/gen_narration_lech.py (EP40, shipped -- latest form). Paid API.
Source of truth = the FINAL script markdown
`episodes/_planning/EP41_thompson_script.en.v001.md`. Like EP39/EP40, EP41 has no
narration_index yet, so this runner EXTRACTS the spoken narration out of the markdown
and writes both:
  - episodes/<EP>/06_audio/voice_plan.v001.json     (same schema as lech/frazier)
  - episodes/<EP>/06_audio/narration_index.v001.json (caption/window source, with
    measured start/end/seconds stamped after generation)

Extraction is strictly subtractive -- the narration wording is never rewritten.

WHAT IS DIFFERENT FROM lech (EP40) and WHY:
  1. Heading convention. EP41 acts are headed `## 【HOOK】...`, `## 【OP】...`,
     `## 【BODY 第1幕】...` ... `## 【ENDING】...` (full-width brackets around the
     tag), NOT lech's `## HOOK — ...`. The lech parser fed the heading's first 6
     chars to a CJK guard to detect the appendix; on 【HOOK】 that guard matches 【
     (U+3010, a CJK-punctuation codepoint) and aborts immediately. So heading parsing
     is rewritten: pull the tag out of 【...】 and map it; any `## ` heading WITHOUT
     a 【 (タイトル / 事実対応表 / 改稿ログ) ends the narration body.
  2. Japanese production notes inside acts. Each EP41 act opens with `役割: ...` and
     `画: ...` note lines (Japanese) before the English narration. These do not start
     with a drop-prefix, so they must be dropped by a CJK-line filter (EP41 narration
     is English-only; any line containing CJK is a production note, never narration).
  3. Scripted silence beats. EP41 has NO 〔CARD〕/【OST〕. Its only audio-direction
     markers are two `〔SILENCE ...〕` lines (HOOK 1.8s after "said: no."; 第2幕 2.2s
     after "No motion filed."). They are NEVER sent to TTS. Instead each is injected
     into the master as a silence gap at exactly that position, REPLACING the
     mechanical inter-chunk gap there (the scripted value is the design intent for
     that boundary). BrandOpening/BrandEndcard bookends are added later at assembly,
     not here.

Everything DROPPED and never sent to TTS:
  - `## 【...】` act headings and every non-narration `## ...` appendix heading
  - the frontmatter (中心の問い / 答え / 主役 / 尺, the `> ビジュアル拘束` blockquote)
  - `役割: ...` / `画: ...` and any other Japanese production note line (CJK-bearing)
  - `〔SILENCE ...〕` audio-direction lines (injected as silence, see above)
  - `*[gold BrandOpening ...]*` assembly notes, bullet lists, horizontal rules
  - the whole tail from `## タイトル / サムネ候補` onward (title/thumb, 事実対応表, 改稿ログ)
A hard guard (assert_clean) re-scans every spoken_text for CJK and bracket/markup
markers and REFUSES to spend money if any survive.

Voice is PINNED here (channel voice, measured ~176-178 wpm). Same voice + model as
EP39/EP40 -- do NOT swap it; the runtime length gate is calibrated on this voice.

Idempotent: an existing non-empty chunk mp3 is skipped (no double-charge).
Run --dry-run first: prints every chunk's spoken_text with NO API call and NO writes.

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
EP = "PD-2026-041-thompson"
SCRIPT_SRC = ROOT / "episodes" / "_planning" / "EP41_thompson_script.en.v001.md"
SOURCE_SCRIPT_REL = "episodes/_planning/EP41_thompson_script.en.v001.md"
OUT_DIR = ROOT / "episodes" / EP / "06_audio"
VOICE_PLAN = OUT_DIR / "voice_plan.v001.json"
INDEX_PATH = OUT_DIR / "narration_index.v001.json"

MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"   # PINNED channel voice -- same as EP39/EP40, do not change
SCRIPT_REVISION = "v001"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
# canonical section -> delivery arc
DELIVERY_BY_SECTION = {
    "HOOK": "intense",   # flash-forward: hidden page, blood, the Court says no
    "OP": "building",    # thesis: can you make the prosecutor answer for it
    "ACT_1": "building", # the choice: arrest, robbery-first, buried blood report
    "ACT_2": "building", # the wait: 14 years on death row, Deegan's deathbed confession
    "ACT_3": "intense",  # the verdict: not guilty, $14M, 5-4 reversal
    "ACT_4": "building", # the reach: Brady, this is your story
    "ENDING": "calm",    # emotional payoff + earned CTA + sign-off
}
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ENDING"]
# full-width-bracket tag inside a `## 【...】` heading -> canonical section
HEADING_TAG_TO_SECTION = {
    "HOOK": "HOOK",
    "OP": "OP",
    "BODY 第1幕": "ACT_1",
    "BODY 第2幕": "ACT_2",
    "BODY 第3幕": "ACT_3",
    "BODY 第4幕": "ACT_4",
    "ENDING": "ENDING",
}
# Started at EP40's tuned values (0.16 / 2.5). MEASURED 2026-07-20: at 0.16 the EP41
# voice ran FAST this session -- 191.1 wpm (vs the 176-178 EP39/EP40 cluster; within the
# channel's observed spread, cf. williams 237 / florence 228 / 202-211). That put speech
# at only 618.5s and the master at 660.2s (11.0 min), UNDER the 690s (11.5 min) band floor
# even after the +12.5s BrandOpening/BrandEndcard bookends added at assembly. The script
# itself PASSES the pre-spend length gate (1,954-2,026 words, in band), so this is pace
# drift, not a short script -- the gap budget is the correct lever (that is exactly what
# check_script_length's RATIO_MIN..MAX 1.04-1.30 documents). Raised to 0.34 / 3.0 and
# --remaster'd from the existing (already-paid) mp3s at zero additional cost: 157 beat
# gaps x0.34 + 5 section breaths x3.0 + the two scripted SILENCE beats -> master 690.9s
# (clears 11.5 min on its own), assembled film ~703s (mid-band 690-750). 0.34s inter-
# sentence beats and 3.0s act breaths read as gravitas on a death-row subject, not dead
# air. The two scripted 〔SILENCE〕 beats (1.8s HOOK, 2.2s 第2幕) are absolute values and
# are injected on top of these mechanics at their exact positions (see SILENCE handling).
GAP_BEAT, GAP_SECTION = 0.34, 3.0
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"

CJK = re.compile(r"[　-〿぀-ゟ゠-ヿ㐀-䶿一-鿿＀-￯]")
# whole-line prefixes that are never narration
DROP_PREFIX = ("【", "〔", "[", "*", ">", "#")
# inline on-screen-text / direction spans to strip from otherwise-spoken paragraphs
INLINE_MARKER = re.compile(r"【[^】]*】|〔[^〕]*〕|\[[^\]]*\]")
# `## 【HOOK】...` -> capture "HOOK" ; `## 【BODY 第1幕】...` -> capture "BODY 第1幕"
HEADING_TAG = re.compile(r"^【([^】]+)】")
# `〔SILENCE 1.8s, ...〕` -> capture 1.8
SILENCE_LINE = re.compile(r"^〔\s*SILENCE\s+([0-9]+(?:\.[0-9]+)?)\s*s", re.IGNORECASE)
ABBREV = re.compile(
    r"\b(?:[A-Z]|Inc|Ltd|Co|Corp|Mr|Mrs|Ms|Dr|Jr|Sr|St|No|Sen|Gov|Rep|Prof|vs|v|al"
    r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\."
)
SENT_SPLIT = re.compile(r'(?<=[.!?])["”]?\s+(?=["“—(]?[A-Z0-9])')


# ---------------------------------------------------------------- extraction

def clean_inline(line: str) -> str:
    """Strip inline OST/CARD/direction spans and collapse whitespace."""
    return " ".join(INLINE_MARKER.sub(" ", line).split())


def extract_events(md: str) -> list[tuple]:
    """-> ordered events: ("para", section, text) | ("silence", section, seconds).

    All non-spoken material removed. Silence events mark a scripted 〔SILENCE〕 gap that
    must follow the most recently emitted paragraph.
    """
    out: list[tuple] = []
    section: str | None = None
    seen_rule = False
    for raw in md.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            head = line[3:].strip()
            m = HEADING_TAG.match(head)
            if not m:
                break   # non-bracket heading (タイトル / 事実対応表 / 改稿ログ) = appendix
            tag = m.group(1).strip()
            section = HEADING_TAG_TO_SECTION.get(tag)
            if section is None:
                break   # unknown 【tag】 = not a narration act; stop
            continue
        if line == "---":
            seen_rule = True
            continue
        if not seen_rule or section is None or not line:
            continue
        sm = SILENCE_LINE.match(line)
        if sm:   # scripted silence beat -> injected at concat, never spoken
            out.append(("silence", section, float(sm.group(1))))
            continue
        if line.startswith("#"):
            continue
        if line.startswith(DROP_PREFIX):   # 〔..〕 / [..] / *[..]* / > / #
            continue
        if line.startswith("- ") or line.startswith("* "):
            continue
        if CJK.search(line):               # Japanese production note (役割:/画:/メモ)
            continue
        line = clean_inline(line)          # remove any mid-paragraph 〔..〕/[..] span
        if not line:
            continue
        out.append(("para", section, line))
    return out


def split_sentences(text: str) -> list[str]:
    guarded = ABBREV.sub(lambda m: m.group(0).replace(".", "\x00"), text)
    parts = [p.replace("\x00", ".").strip() for p in SENT_SPLIT.split(guarded)]
    return [" ".join(p.split()) for p in parts if p.strip()]


def build_chunks(md: str) -> list[dict]:
    chunks: list[dict] = []
    n = 0
    for ev in extract_events(md):
        if ev[0] == "silence":
            if chunks:   # attach to the preceding chunk; override its trailing gap
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
                "idempotency_key": idempotency_key(sent, cid),
                "silence_after_seconds": None,   # internal only; not written to voice_plan
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
        if "OST" in t or "CARD:" in t or "SILENCE" in t or "SOUND:" in t or "Bookends" in t:
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


# canonical voice_plan chunk keys (schema-identical to lech/frazier; silence_after is internal)
PLAN_KEYS = ("chunk_id", "section", "delivery", "spoken_text", "text_sha256", "idempotency_key")


def write_voice_plan(chunks: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plan_chunks = [{k: c[k] for k in PLAN_KEYS} for c in chunks]
    VOICE_PLAN.write_text(json.dumps(
        {"episode_id": EP, "revision": SCRIPT_REVISION, "provider": "ElevenLabs",
         "voice_id": VOICE_ID, "model_id": MODEL, "chunks": plan_chunks},
        indent=2, ensure_ascii=False) + "\n", "utf-8")


def _silence_file(outdir: Path, seconds: float, cache: dict[float, Path]) -> Path:
    """Get (creating once) a mono mp3 of exactly `seconds` of silence."""
    key = round(seconds, 3)
    if key in cache:
        return cache[key]
    p = outdir / f"_silence_{key:.3f}.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                    "-t", f"{key}", "-c:a", "libmp3lame", "-b:a", "192k", str(p)], check=True)
    cache[key] = p
    return p


def concat_master(chunks: list[dict], outdir: Path, master: Path) -> dict[str, dict]:
    """Concat chunk mp3s with inter-chunk silence into a loudnorm'd master; return
    {chunk_id: {start,end,seconds}} (silence EXCLUDED from each chunk window).

    Gap after chunk i: the scripted 〔SILENCE〕 value if one was attached there,
    else GAP_SECTION at a section boundary, else GAP_BEAT.
    """
    sil_cache: dict[float, Path] = {}
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
            override = c.get("silence_after_seconds")
            if override is not None:
                gap = float(override)
            else:
                boundary = c["section"] != chunks[i + 1]["section"]
                gap = GAP_SECTION if boundary else GAP_BEAT
            lines.append(f"file '{_silence_file(outdir, gap, sil_cache).as_posix()}'\n")
            cursor += gap
    concat = outdir / "_concat.txt"
    concat.write_text("".join(lines), "utf-8")
    master.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-af", LOUDNORM, "-c:a", "libmp3lame", "-b:a", "192k", str(master)], check=True)
    return offsets


def write_index(chunks: list[dict], offsets: dict[str, dict],
                master: Path, est_cost: float) -> None:
    total = round(dur(master), 3)
    speech = round(sum(o["seconds"] for o in offsets.values()), 3)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    scripted_silence = round(sum(c["silence_after_seconds"] for c in chunks
                                 if c.get("silence_after_seconds") is not None), 3)
    index = {
        "episode_id": EP,
        "revision": SCRIPT_REVISION,
        "provider": "elevenlabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL,
        "source_script": SOURCE_SCRIPT_REL,
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
            "producer": "scripts/gen_narration_thompson.py",
            "provider": "ElevenLabs",
            "voice_id": VOICE_ID,
            "model_id": MODEL,
            "estimated_cost_usd": est_cost,
            "gap_beat_seconds": GAP_BEAT,
            "gap_section_seconds": GAP_SECTION,
            "scripted_silence_seconds": scripted_silence,
            "loudnorm": LOUDNORM,
            "master_path_expected": str(master),
            "stamped_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "note": "start/end are per-chunk master offsets (inter-chunk silence excluded from each window). "
                    "Two scripted SILENCE beats (HOOK 1.8s, ACT_2 2.2s) are injected at their positions.",
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
    sil = [(c["chunk_id"], c["silence_after_seconds"]) for c in chunks
           if c.get("silence_after_seconds") is not None]
    print(f"episode={EP} chunks={len(chunks)} words={words} chars={chars} est=${est:.2f} model={MODEL}")
    print(f"projected @176.0wpm = {words / 176.0 * 60:.0f}s (band 690-750s)")
    print(f"scripted silence beats: {sil}")

    if args.dry_run:
        for c in chunks:
            tail = f"  <SILENCE {c['silence_after_seconds']}s>" if c.get("silence_after_seconds") else ""
            print(f"  {c['chunk_id']} {c['section']:6s} {c['delivery']:8s} | {c['spoken_text']}{tail}")
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
          f"{'PASS' if 690 <= speech <= 750 else 'CHECK'}")
    projto = speech * 1.04
    projhi = speech * 1.13
    print(f"finished projection = {projto:.0f}-{projhi:.0f}s (speech x1.04-1.13)  "
          f"target 690-750s -> {'PASS' if projto <= 750 and projhi >= 690 else 'CHECK'}")
    print(f"measured wpm = {words / (speech / 60):.1f} (expected ~176-178)")
    print(f"master -> {master} ({dur(master):.1f}s incl. gaps)")
    print(f"index  -> {INDEX_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
