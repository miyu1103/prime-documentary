#!/usr/bin/env python3
"""Generate PD-2026-042-young narration with the channel voice (ElevenLabs).

Cloned from scripts/gen_narration_thompson.py (EP41, shipped). Paid API. Source of
truth = the LOCKED script `episodes/_planning/EP42_young_script.en.v001.md`. EP42 has
no narration_index yet, so this runner EXTRACTS the spoken narration out of the markdown
and writes:
  - episodes/<EP>/06_audio/voice_plan.v001.json      (schema-identical to thompson)
  - episodes/<EP>/06_audio/narration_index.v001.json (caption/window source, with
    measured start/end/seconds stamped after generation)
Extraction is strictly subtractive -- the narration wording is never rewritten.

WHAT IS DIFFERENT FROM thompson (EP41) and WHY:
  1. Heading convention. EP42 sections are headed `## [HOOK] ...`, `## [OPENING
     NARRATION] ...`, `## ACT 1 ...` ... `## ENDING ...` (square/plain brackets), NOT
     thompson's full-width `## 【HOOK】`. Section detection is by explicit regex per
     heading. `## [BrandOpening]`/`## [BrandEndcard]`/`## 事実対応表`/`## 改稿ログ` and
     the title/frontmatter are NOT narration.
  2. Narration lives INSIDE blockquotes. Every spoken paragraph in EP42 is a `> ...`
     blockquote line (thompson's spoken lines were plain). So `> ` is STRIPPED to reveal
     narration, not dropped. `**[VISUAL: ...]**` and `*(...)*` note lines are dropped.
  3. Scripted silence beats use full-width brackets: `【SILENCE 1.8s】` (HOOK end),
     `【SILENCE 1.5s -- the body camera keeps recording】` (ACT_1), `【SILENCE 0.9s】`
     (ACT_2 end), `【SILENCE 1.0s】` (ENDING). They are NEVER sent to TTS. Each is
     injected into the master as a silence gap at exactly its position, REPLACING the
     mechanical inter-chunk gap there. BrandOpening/BrandEndcard bookends are added later
     at assembly, not here.

Voice is PINNED here (channel voice "Brian", same as EP39/EP40/EP41). Do NOT swap it.

Idempotent: an existing non-empty chunk mp3 is skipped (no double-charge).
--dry-run prints every chunk's spoken_text with NO API call and NO writes.
--remaster rebuilds master+index from existing (already-paid) mp3s at zero cost, and
honours --gap-beat / --gap-section so runtime can be tuned to band WITHOUT re-paying.
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
EP = "PD-2026-051-willingham"
SCRIPT_SRC = ROOT / "episodes" / "_planning" / "EP51_willingham_script.en.v001.md"
SOURCE_SCRIPT_REL = "episodes/_planning/EP51_willingham_script.en.v001.md"
OUT_DIR = ROOT / "episodes" / EP / "06_audio"
VOICE_PLAN = OUT_DIR / "voice_plan.v001.json"
INDEX_PATH = OUT_DIR / "narration_index.v001.json"

MODEL = "eleven_multilingual_v2"
VOICE_ID = "nPczCjzI2devNBz1zQrb"   # PINNED channel voice "Brian" -- same as EP39/40/41
SCRIPT_REVISION = "v001"
TTS = "https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128"
SETTINGS = {
    "calm": {"stability": 0.58, "similarity_boost": 0.80, "style": 0.14, "use_speaker_boost": True},
    "building": {"stability": 0.48, "similarity_boost": 0.82, "style": 0.30, "use_speaker_boost": True},
    "intense": {"stability": 0.38, "similarity_boost": 0.84, "style": 0.44, "use_speaker_boost": True},
}
# canonical section -> delivery arc (SAME presets EP42 used: HOOK intense, ENDING calm,
# everything between building). EP43 BODY is 3 acts (no ACT_4).
# EP50 is the channel's first hour-long film: HOOK + 7 acts (ACT_7 = ENDING). The
# `## [OPENING TITLE — 3.5s]` section is a silent TITLE CARD (only `*THE EXONERATED
# FIVE.*` stage direction, no spoken VO) -> it is deliberately NOT mapped, so it drops.
DELIVERY_BY_SECTION = {
    "HOOK": "intense",    # cold open: the worst concrete moment
    "OP": "building",     # spoken thesis + open loop (after the silent gold BrandOpening card)
    "ACT_1": "building",  # THE MONSTER: a grieving father cast as guilty
    "ACT_2": "building",  # THE TRIAL: arson indicators + the informant
    "ACT_3": "building",  # THE UNRAVELING: Hurst's warning, failed clemency, execution, after
    "ENDING": "calm",     # the honest hedge + the payoff lands last
}
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ENDING"]
# heading text (leading #'s stripped) regex -> canonical section (order matters; first
# match wins). EP51 headings are `## COLD OPEN ...`, `## OPENING ...`, `## ACT I — ...`,
# `## ACT II — ...`, `## ACT III — ...`, `## ENDING ...` (Roman numerals, no brackets).
# Longer Roman numerals FIRST so ACT III/II don't get shadowed by ACT I.
SECTION_HEADINGS = [
    ("HOOK", re.compile(r"^COLD\s+OPEN\b", re.IGNORECASE)),
    ("OP", re.compile(r"^OPENING\b", re.IGNORECASE)),
    ("ACT_3", re.compile(r"^ACT\s+III\b", re.IGNORECASE)),
    ("ACT_2", re.compile(r"^ACT\s+II\b", re.IGNORECASE)),
    ("ACT_1", re.compile(r"^ACT\s+I\b", re.IGNORECASE)),
    ("ENDING", re.compile(r"^ENDING\b", re.IGNORECASE)),
]
# any heading / line that ends the narration body (appendix / non-VO). EP51's post-ENDING
# sections are `## RUNTIME / WORD COUNT` and `## SELF-CHECK — PASS 1/2/3` -> STOP there.
STOP_HEADINGS = [
    re.compile(r"^RUNTIME\b", re.IGNORECASE),
    re.compile(r"^SELF-CHECK\b", re.IGNORECASE),
    re.compile(r"^\*?\[END OF NARRATION", re.IGNORECASE),
    re.compile(r"^事実対応表"),
    re.compile(r"^改稿ログ"),
]

# Default inter-chunk mechanics. UNLIKE thompson (short script, fast voice -> needed BIG
# gaps to reach the 690s floor), EP42's script is LONGER (2,140 words), so speech alone is
# near the 721.3s target and gaps must stay SMALL to avoid blowing past the 750s ceiling.
# These are the FIRST-PASS values; measure speech after generation and --remaster with
# tuned --gap-beat/--gap-section to land the master in the 690-750s band (~720s target).
GAP_BEAT, GAP_SECTION = 0.30, 1.8
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"

CJK = re.compile(r"[　-〿぀-ゟ゠-ヿ㐀-䶿一-鿿＀-￯]")
# EP43 scripted silence: `【DESIGNED SILENCE 1.8s. Hold on ...】` anywhere -> capture seconds
SILENCE_LINE = re.compile(r"DESIGNED SILENCE\s+([0-9]+(?:\.[0-9]+)?)\s*s", re.IGNORECASE)
# EP43 `【beat】` / `【beat. ...】` micro-pause (~0.6s), injected as a small silence gap
BEAT_LINE = re.compile(r"^【\s*beat\b", re.IGNORECASE)
BEAT_SECONDS = 0.6
# inline on-screen-text / direction spans to strip from otherwise-spoken paragraphs
INLINE_MARKER = re.compile(r"【[^】]*】|〔[^〕]*〕|\[[^\]]*\]")
ABBREV = re.compile(
    r"\b(?:[A-Z]|Inc|Ltd|Co|Corp|Mr|Mrs|Ms|Dr|Jr|Sr|St|No|Sen|Gov|Rep|Prof|Sgt|vs|v|al"
    r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\.")
SENT_SPLIT = re.compile(r'(?<=[.!?])["”]?\s+(?=["“—(]?[A-Z0-9])')


# ---------------------------------------------------------------- extraction

def clean_quote(line: str) -> str:
    """Strip a leading blockquote marker, bold/italic/backtick markup, collapse ws."""
    line = re.sub(r"^>\s?", "", line).strip()
    line = re.sub(r"\*\*|\*|`", "", line)
    return " ".join(line.split())


def section_for_heading(head: str) -> tuple[str | None, bool]:
    """Return (canonical_section_or_None, is_stop)."""
    for sec, pat in SECTION_HEADINGS:
        if pat.match(head):
            return sec, False
    for pat in STOP_HEADINGS:
        if pat.match(head):
            return None, True
    return None, False   # a non-narration heading (title / BrandOpening) -> just leaves section


def extract_events(md: str) -> list[tuple]:
    """-> ordered events: ("para", section, text) | ("silence", section, seconds).

    All non-spoken material removed. A silence event marks a scripted 【SILENCE】 gap that
    must follow the most recently emitted paragraph.
    """
    out: list[tuple] = []
    section: str | None = None
    for raw in md.splitlines():
        line = raw.strip()
        hm = re.match(r"^(#{1,6})\s+(.*)$", line)
        if hm:                      # any heading level (EP43 acts are h3)
            sec, is_stop = section_for_heading(hm.group(2).strip())
            if is_stop:
                break
            section = sec           # None for title / `## 3. BODY` (drops until next act)
            continue
        if section is None or not line:
            continue
        sm = SILENCE_LINE.search(line)
        if sm:                      # scripted DESIGNED SILENCE -> injected at concat, never spoken
            out.append(("silence", section, float(sm.group(1))))
            continue
        if BEAT_LINE.match(line):   # 【beat】 micro-pause -> small silence gap, never spoken
            out.append(("silence", section, BEAT_SECONDS))
            continue
        if line == "---":
            continue
        if line.startswith("**[") or line.startswith("*("):   # VISUAL / production note
            continue
        if CJK.search(line):        # Japanese production note (never narration; EP42 is EN)
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


def build_chunks(md: str) -> list[dict]:
    chunks: list[dict] = []
    n = 0
    for ev in extract_events(md):
        if ev[0] == "silence":
            if chunks:              # attach to the preceding chunk; overrides its trailing gap
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
    # EP50: no topic-specific forbidden-phrase guard (the caniglia/4A-home overreach list
    # does not apply to the Exonerated Five story). Structural cleanliness only.
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


PLAN_KEYS = ("chunk_id", "section", "delivery", "spoken_text", "text_sha256", "idempotency_key")


def write_voice_plan(chunks: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plan_chunks = [{k: c[k] for k in PLAN_KEYS} for c in chunks]
    VOICE_PLAN.write_text(json.dumps(
        {"episode_id": EP, "revision": SCRIPT_REVISION, "provider": "ElevenLabs",
         "voice_id": VOICE_ID, "model_id": MODEL, "chunks": plan_chunks},
        indent=2, ensure_ascii=False) + "\n", "utf-8")


def _silence_file(outdir: Path, seconds: float, cache: dict[float, Path]) -> Path:
    key = round(seconds, 3)
    if key in cache:
        return cache[key]
    p = outdir / f"_silence_{key:.3f}.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                    "-t", f"{key}", "-c:a", "libmp3lame", "-b:a", "192k", str(p)], check=True)
    cache[key] = p
    return p


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
    """Concat chunk mp3s + inter-chunk silence into a loudnorm'd master; return
    {chunk_id: {start,end,seconds}} (silence EXCLUDED from each chunk window).

    HOUR-LONG-SAFE assembly: the concat DEMUXER cannot cleanly stitch >1000 VBR-mp3
    segments (it emits "invalid new backstep" / "Invalid data" and truncates/corrupts
    the master -- observed on this 617-chunk / 1233-segment film). So every chunk is
    first decoded to a uniform 44100/mono/s16le WAV, silence is the SAME PCM format,
    and the all-WAV concat (uniform -> zero resync errors) is encoded ONCE to the MP3
    master. Verified: WAV == MP3-ffprobe == MP3-decoded, 0 decode errors.
    """
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


def write_index(chunks: list[dict], offsets: dict[str, dict], master: Path,
                est_cost: float, gap_beat: float, gap_section: float) -> None:
    total = round(dur(master), 3)
    speech = round(sum(o["seconds"] for o in offsets.values()), 3)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    scripted_silence = round(sum(c["silence_after_seconds"] for c in chunks
                                 if c.get("silence_after_seconds") is not None), 3)
    index = {
        "schema_version": "caniglia_narration.v1",
        "episode_id": EP,
        "revision": SCRIPT_REVISION,
        "is_stub": False,
        "provider": "elevenlabs",
        "voice_id": VOICE_ID,
        "model_id": MODEL,
        "source_script": SOURCE_SCRIPT_REL,
        "master": f"artifact://episodes/{EP}/06_voice/master/vc_master_v001.mp3",
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
            "producer": "scripts/gen_narration_caniglia.py",
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
            "note": "start/end are per-chunk master offsets (inter-chunk silence excluded from each "
                    "window). Three scripted DESIGNED SILENCE beats (HOOK 1.8s, ACT_1 1.4s, "
                    "ENDING 2.2s) plus 【beat】 micro-pauses (0.6s) are injected at their positions.",
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
    ap.add_argument("--gap-beat", type=float, default=GAP_BEAT, help="inter-sentence gap seconds")
    ap.add_argument("--gap-section", type=float, default=GAP_SECTION, help="section-boundary gap seconds")
    args = ap.parse_args(argv)

    chunks = build_chunks(SCRIPT_SRC.read_text("utf-8"))
    assert_clean(chunks)
    chars = sum(len(c["spoken_text"]) for c in chunks)
    words = sum(len(c["spoken_text"].split()) for c in chunks)
    est = round(chars / 1000 * 0.30, 2)
    sil = [(c["chunk_id"], c["silence_after_seconds"]) for c in chunks
           if c.get("silence_after_seconds") is not None]
    print(f"episode={EP} chunks={len(chunks)} words={words} chars={chars} est=${est:.2f} model={MODEL}")
    print(f"projected @178wpm = {words / 178.0 * 60:.0f}s speech (EP50 = hour-long film; runtime is MEASURED, no band)")
    print(f"gaps: beat={args.gap_beat}s section={args.gap_section}s  scripted silence beats: {sil}")

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
    offsets = concat_master(chunks, outdir, master, args.gap_beat, args.gap_section)
    write_index(chunks, offsets, master, est, args.gap_beat, args.gap_section)
    import math
    speech = sum(o["seconds"] for o in offsets.values())
    total = dur(master)
    # film durationInFrames @30fps = round(8*30) hook + round(3.5*30) opening
    #   + ceil(narrationSeconds*30) + round(9*30) endcard = 615 + ceil(total*30)
    duration_frames = round(8 * 30) + round(3.5 * 30) + math.ceil(total * 30) + round(9 * 30)
    print(f"made={made} skipped={skipped} failed={failed}")
    print(f"speech total = {speech:.1f}s ({speech / 60:.2f}min)")
    print(f"MASTER measured narrationSeconds = {total:.3f}s ({total / 60:.2f}min)")
    print(f"measured wpm = {words / (speech / 60):.1f}")
    print(f"IMPLIED durationInFrames = 615 + ceil({total:.3f}*30) = {duration_frames} "
          f"(provisional was 108795 @ ~3606s)")
    print(f"master -> {master}")
    print(f"index  -> {INDEX_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
