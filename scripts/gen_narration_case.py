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
    "ACT_3": "building", "ACT_4": "building", "ACT_5": "building", "ENDING": "calm",
    # EP60 (surfside) only: THE NIGHT is its own section because it is the only part of
    # that film in a different tense -- 1:22 a.m. itself, not "what had been happening".
    # Read intense, like the cold open, not "building".
    "THE_NIGHT": "intense",
}
# Canon 4-act order (EP52-55). Episodes with a different act count declare their own
# `sections` in the registry below (EP56 is the first 5-act case film).
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ENDING"]
SECTION_ORDER_5ACT = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ACT_5", "ENDING"]
# EP60 (surfside) is the first film with a tense break. Ten script headings --
# COLD OPEN / BRAND STING / OPENING / ACT I..ACT V / THE NIGHT / ENDING -- of which
# BRAND STING is narration-free (as in EP56), so NINE sections carry speech. THE NIGHT
# sits between ACT V and ENDING and is deliberately NOT folded into either: up to ACT V
# the film says what had been happening; THE NIGHT is 1:22 a.m. itself (~2:15).
SECTION_ORDER_5ACT_NIGHT = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ACT_5",
                            "THE_NIGHT", "ENDING"]
# EP52/53/54/55 headings: `## COLD OPEN ...`, `## OPENING ...`, `## ACT I — ...`
# ... `## ACT IV — ...`, `## ENDING ...` (Roman numerals). Longer numerals FIRST.
# EP56 adds `## ACT V — ...` and a narration-free `## BRAND STING ...` card heading
# (the sting is a build element; it carries no spoken line — mapped to None so any
# text that ever lands under it is caught by the section-coverage gate, not silently
# absorbed into the neighbouring act).
SECTION_HEADINGS = [
    ("HOOK", re.compile(r"^COLD\s+OPEN\b", re.IGNORECASE)),
    # EP61 (weimer) heads its cold open `## HOOK` instead of `## COLD OPEN`. Without this
    # pattern the heading maps to no section, and because `started` is still False at that
    # point the orphan guard cannot see the lines either -- the whole cold open would have
    # been dropped in silence. No other registered script has a heading beginning "HOOK",
    # so this anchored pattern cannot change any existing extraction.
    ("HOOK", re.compile(r"^HOOK\b", re.IGNORECASE)),
    # `## OPENING` -> the contract key `OP` (NOT "OPENING"): the figure beats for every
    # episode are keyed to the spec section_vocabulary, so an index emitting "OPENING"
    # would leave those beats attached to nothing.
    ("OP", re.compile(r"^OPENING\b", re.IGNORECASE)),
    ("ACT_4", re.compile(r"^ACT\s+IV\b", re.IGNORECASE)),
    ("ACT_5", re.compile(r"^ACT\s+V\b", re.IGNORECASE)),
    ("ACT_3", re.compile(r"^ACT\s+III\b", re.IGNORECASE)),
    ("ACT_2", re.compile(r"^ACT\s+II\b", re.IGNORECASE)),
    ("ACT_1", re.compile(r"^ACT\s+I\b", re.IGNORECASE)),
    # EP62 (greene) heads its sections with the CONTRACT KEYS themselves -- `## OP`,
    # `## ACT_1` ... `## ACT_5` -- because episode_spec.v001.json tells the writer to
    # spell the headings the way section_vocabulary spells them (EP61 used `## OPENING`
    # where the contract said `OP`, and the mismatch had to be handed on as a warning).
    # None of these can collide with the prose forms above: `^OP\b` cannot match
    # "OPENING" (no word boundary between P and E), and `^ACT_N\b` cannot match
    # "ACT I"/"ACT IV" (underscore is a word character, `\s+` requires whitespace).
    ("OP", re.compile(r"^OP\b", re.IGNORECASE)),
    ("ACT_1", re.compile(r"^ACT_1\b", re.IGNORECASE)),
    ("ACT_2", re.compile(r"^ACT_2\b", re.IGNORECASE)),
    ("ACT_3", re.compile(r"^ACT_3\b", re.IGNORECASE)),
    ("ACT_4", re.compile(r"^ACT_4\b", re.IGNORECASE)),
    ("ACT_5", re.compile(r"^ACT_5\b", re.IGNORECASE)),
    # THE NIGHT (EP60): no other heading in any script begins with "THE", and this
    # pattern is anchored, so it can neither swallow nor be swallowed by the acts above.
    # It stays BELOW the ACT patterns anyway, since this list is matched in order and
    # the ACT entries are deliberately longest-numeral-first (ACT IV before ACT V before
    # ACT III/II/I).
    ("THE_NIGHT", re.compile(r"^THE\s+NIGHT\b", re.IGNORECASE)),
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
    "PD-2026-056-postoffice": {
        "planning": "EP56_postoffice_script.en.v001.md",
        # DESIGN §5: 4,750 w @178.1wpm = 1600.2s provisional; gap budget 181.8s +
        # endcard 9s -> 1791.0s (29:51) provisional inside the 1740-1860 band.
        "design_speech_seconds": 1600.2,
        # FIRST five-act case film (ACT I..ACT V) + a narration-free `## BRAND STING`.
        "sections": SECTION_ORDER_5ACT,
    },
    # EP57-59: same five-act shape as EP56 (COLD OPEN / BRAND STING / OPENING / ACT I..V /
    # ENDING). All three scripts are R3-locked; word counts are the MEASURED ones from each
    # DESIGN §5, not estimates.
    "PD-2026-057-fieldtest": {
        "planning": "EP57_fieldtest_script.en.v001.md",
        # DESIGN §5 (R3 re-locked): 4,673 w modelled at 172.0 wpm -- deliberately NOT 178.1,
        # because EP55 and EP56 both measured ~+71s slower than the channel model.
        "design_speech_seconds": 1630.1,
        "sections": SECTION_ORDER_5ACT,
    },
    "PD-2026-058-lejeune": {
        "planning": "EP58_lejeune_script.en.v001.md",
        # DESIGN §5: 4,738 w @178.1wpm = 1596.1s; total held at 1790.0s via the gap budget.
        "design_speech_seconds": 1596.1,
        "sections": SECTION_ORDER_5ACT,
    },
    "PD-2026-059-robosigning": {
        "planning": "EP59_robosigning_script.en.v001.md",
        # DESIGN §5 (R3 re-derived): 4,670 w @178.1wpm = 1573.3s + gap 200.7 + endcard 9.
        "design_speech_seconds": 1573.3,
        "sections": SECTION_ORDER_5ACT,
    },
    "PD-2026-060-surfside": {
        # LOCKED script is v004 ("v004, もう変えません" -- owner). v003 under
        # episodes/PD-2026-060-surfside/03_script/ is stale and must not be used.
        # v005 supersedes v004: four assertions that nobody had been criminally prosecuted
        # were removed because no source held here supported them, and replaced with what the
        # Miami-Dade State Attorney actually published -- a grand jury convened July 2021 and
        # its December 2021 report, titled "Surfside Condo Collapse: Recommendations to Make
        # Buildings Safer". Absence of reporting is not evidence of absence. Do not use v004.
        "planning": "EP60_surfside_script.en.v005.md",
        # FILM BIBLE v001 (line 3): 40:00 film, narration approximately 36:00, band
        # 6,150-6,350 words at the MEASURED 173 wpm -- deliberately NOT the 178.1 channel
        # model. Extraction of the locked v004 script measures 6,302 narration words, so
        # 6302 / 173 * 60 = 2185.7s (36:26): inside the bible band and on its 36:00 target.
        "design_speech_seconds": 2185.7,
        # Ten script headings; BRAND STING carries no narration (as in EP56), so NINE
        # speech sections, with THE NIGHT standing alone between ACT V and ENDING.
        "sections": SECTION_ORDER_5ACT_NIGHT,
    },
    "PD-2026-061-weimer": {
        # LOCKED script is v003. v001 and v002 are stale and must not be used.
        # v004 supersedes v003: +72 lines of pure insertion, no deletion, 4,408 -> 5,435 words.
        # The design model assumed 173 wpm; this voice measured 194.3 on EP61 and 191.4 on EP60,
        # so a script inside the contract word band still landed 1.7 minutes under its own
        # runtime floor. ACT IV, HOOK and ENDING are byte-identical to v003.
        "planning": "EP61_weimer_script.en.v004.md",
        # ASSEMBLY_HANDOFF v001 step 2: 4,401 narration words / 25.4 min speech.
        "design_speech_seconds": 1524.0,
        # Nine script headings -- HOOK / BRAND STING / OPENING / ACT I..ACT V / ENDING --
        # of which BRAND STING carries no narration (as in EP56/EP60), so EIGHT speech
        # sections, exactly matching episode_spec.v001.json section_vocabulary
        # (HOOK, OP, ACT_1..ACT_5, ENDING) that the 99 figure beats are keyed to.
        "sections": SECTION_ORDER_5ACT,
    },
    "PD-2026-062-greene": {
        # LOCKED script is v003. v001, v002 and v004 are stale and must not be used.
        # v003 is the verified pass: 77 verbatim runs re-checked against 456 U.S. 444 with
        # zero fabrications and zero misattributions, all ten logged defects closed, and the
        # amicus attribution at line 247 corrected to scope "urged the Court to affirm" to
        # the Antioch School of Law alone (what the reporter supports).
        "planning": "EP62_greene_script.en.v003.md",
        # FINISHED-RATE model, not the raw speech rate. EP60 and EP61 measured 178.4 and
        # 178.3 words per finished minute -- that figure already carries the pipeline's own
        # inter-chunk gaps (143 s on EP60, 161 s on EP61). 5,250 narration words / 178.35
        # = 1766 s (29:26), inside the contract band [1620, 1920]. The 191-195 wpm raw
        # speech rate is NOT used here: it charges nothing for the gaps and would report
        # this script as short.
        "design_speech_seconds": 1766.0,
        # Eight headings, spelled as episode_spec.v001.json section_vocabulary spells them:
        # HOOK / OP / ACT_1..ACT_5 / ENDING. Every one carries narration (no BRAND STING).
        "sections": SECTION_ORDER_5ACT,
        # PINNED per-episode voice settings (owner instruction 2026-08-04). EP60 and EP61
        # recorded only voice_id and model_id, so pace parity across episodes is unproven
        # and check_script_length still carries a 237 wpm fast-end risk from two episodes
        # whose settings had drifted. These override the per-delivery presets' stability
        # and similarity_boost for EVERY chunk of this episode and are written into
        # voice_plan.v001.json and the narration index provenance.
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
    "PD-2026-063-correa": {
        # LOCKED script is v002. v001 is stale and must not be used.
        "planning": "EP63_correa_script.en.v002.md",
        # FINISHED-RATE model, as EP62 -- not a raw speech rate. The script derives its own
        # section windows from 176 words per FINISHED minute (script line 9; episode_spec
        # notes 2026-08-04: EP60 191.4 wpm and EP61 194.3 wpm of raw speech become ~176 once
        # gap_beat 0.30s and gap_section 1.80s are charged). 5,278 narration words / 176 wpm
        # = 1799.3s (29:59), inside the contract band [1620, 1920].
        "design_speech_seconds": 1799.3,
        # Eight headings, spelled as episode_spec.v001.json section_vocabulary spells them:
        # HOOK / OP / ACT_1..ACT_5 / ENDING -- each carrying a parenthetical window,
        # e.g. `## ACT_1 (0:27-5:13 - 839 w)`. Every pattern in SECTION_HEADINGS is anchored
        # on the key with a word boundary, so the parenthetical changes nothing. VERIFIED
        # before spending: all eight sections extract non-empty (373 chunks / 5,315 tokens),
        # and the per-section counts reconcile with the script's declared 20/58/839/1,096/
        # 1,110/991/823/341 once the 36 standalone em-dash tokens are discounted.
        "sections": SECTION_ORDER_5ACT,
        # PINNED per-episode voice settings, identical to EP62 so the two ARE comparable.
        # EP62 measured 169.8 words per finished minute at exactly these values. EP60 and
        # EP61 recorded no settings at all, which is why neither can be compared to anything.
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.80},
    },
}

GAP_BEAT, GAP_SECTION = 0.30, 1.8          # EP52-shipped defaults
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"
COST_PER_1K_CHARS_USD = 0.30

CJK = re.compile(r"[　-〿぀-ゟ゠-ヿ㐀-䶿一-鿿＀-￯]")
SILENCE_LINE = re.compile(r"DESIGNED SILENCE\s+([0-9]+(?:\.[0-9]+)?)\s*s", re.IGNORECASE)
# A held beat is a production direction, never narration: `【beat ...】` (EP52 lineage) or
# EP60's `⟨HELD⟩`, which the EP60 film bible defines as the marker for "an isolated slow-read
# line". Both become a BEAT_SECONDS pause after the preceding chunk instead of spoken text.
BEAT_LINE = re.compile(r"^(?:【\s*beat\b|⟨\s*(?:HELD|BEAT)\s*⟩)", re.IGNORECASE)
BEAT_SECONDS = 0.6
# A trailing italic revision footer, e.g. EP61 v003 line 519:
#   *v001 · 2026-08-03 · facts locked to ... · hook to be rewritten last per SPEC v2 row 9.*
# It sits UNDER the ENDING heading with no appendix heading above it, so STOP_HEADINGS cannot
# reach it and it would be read aloud. Anchored on a leading `*vNNN` and a closing `*` so it
# cannot match narration.
REVISION_FOOTER = re.compile(r"^\*v\d{3}\b.*\*$")
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


def extract_events(md: str, orphans: list[str] | None = None) -> list[tuple]:
    """-> ordered events: ("para", section, text) | ("silence", section, seconds).

    `orphans` (optional) collects prose lines that sit under a heading with NO section
    mapping AFTER narration has started (e.g. EP56's `## BRAND STING` card). Such lines
    would otherwise be dropped silently; build_chunks refuses to spend money on them.
    """
    out: list[tuple] = []
    section: str | None = None
    started = False
    for raw in md.splitlines():
        line = raw.strip()
        hm = re.match(r"^(#{1,6})\s+(.*)$", line)
        if hm:
            sec, is_stop = section_for_heading(hm.group(2).strip())
            if is_stop:
                break
            section = sec
            started = started or sec is not None
            continue
        if section is None or not line:
            if (orphans is not None and started and line
                    and not CJK.search(line)
                    and not line.startswith(("|", "#", ">", "- ", "* ", "---", "**["))
                    and len(re.sub(r"[^A-Za-z]", "", line)) >= 20):
                orphans.append(line)
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
        if line.startswith("**[") or line.startswith("*(") or REVISION_FOOTER.match(line):
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
    orphans: list[str] = []
    n = 0
    for ev in extract_events(md, orphans):
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
    if orphans:
        raise SystemExit(
            "REFUSING TO GENERATE -- prose found under an unmapped heading (would be "
            "dropped silently):\n  " + "\n  ".join(o[:120] for o in orphans))
    return chunks


def assert_clean(chunks: list[dict], expected: list[str] | None = None) -> None:
    """Hard gate: refuse to spend money if any production marker leaked into TTS text."""
    bad: list[str] = []
    for c in chunks:
        t = c["spoken_text"]
        if CJK.search(t):
            bad.append(f"{c['chunk_id']}: CJK in spoken_text -> {t[:80]}")
        # ⟨⟩ added 2026-08-03: EP60 v004 marks held beats with ⟨HELD⟩, and this gate did
        # not know that bracket pair, so eight "HELD" chunks would have been read aloud.
        if re.search(r"[\[\]【】〔〕⟨⟩`#*_]", t):
            bad.append(f"{c['chunk_id']}: markup/marker in spoken_text -> {t[:80]}")
        if "OST" in t or "CARD:" in t or "SILENCE" in t or "SOUND:" in t or "VISUAL" in t:
            bad.append(f"{c['chunk_id']}: directive keyword -> {t[:80]}")
        if len(t) < 3:
            bad.append(f"{c['chunk_id']}: too short -> {t!r}")
    if bad:
        raise SystemExit("REFUSING TO GENERATE -- unclean chunks:\n  " + "\n  ".join(bad))
    order = expected or SECTION_ORDER
    got = [s for s in order if any(c["section"] == s for c in chunks)]
    unknown = sorted({c["section"] for c in chunks} - set(order))
    if got != order or unknown:
        raise SystemExit(f"REFUSING TO GENERATE -- section coverage {got}{unknown} != {order}")


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


def resolve_settings(cfg: dict) -> dict[str, dict]:
    """Per-delivery voice settings, with the episode's own pins applied on top.

    An episode may declare `voice_settings` in the registry to pin values across every
    delivery (EP62 pins stability 0.35 / similarity_boost 0.80). Keys the episode does
    not name keep the shipped per-delivery preset. Episodes that declare nothing get
    exactly SETTINGS, unchanged.
    """
    override = cfg.get("voice_settings") or {}
    return {d: {**preset, **override} for d, preset in SETTINGS.items()}


def write_voice_plan(ep: str, chunks: list[dict], out_dir: Path, plan_path: Path,
                     settings_by_delivery: dict[str, dict] | None = None) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    settings_by_delivery = settings_by_delivery or SETTINGS
    plan_chunks = [{k: c[k] for k in PLAN_KEYS} for c in chunks]
    plan_path.write_text(json.dumps(
        {"episode_id": ep, "revision": SCRIPT_REVISION, "provider": "ElevenLabs",
         "voice_id": VOICE_ID, "model_id": MODEL,
         # The exact settings sent to the provider, per delivery. Recorded so that a
         # later episode can prove pace parity instead of assuming it.
         "voice_settings": settings_by_delivery,
         "chunks": plan_chunks},
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
                gap_beat: float, gap_section: float,
                settings_by_delivery: dict[str, dict] | None = None) -> dict:
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
            "voice_settings": settings_by_delivery or SETTINGS,
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
    ap.add_argument("--measure-section", metavar="SECTION",
                    help="generate ONLY this section (e.g. ACT_1), measure it with ffprobe, "
                         "print the words-per-finished-minute it implies, and stop before "
                         "the master and the index. Chunks land in the normal draft dir with "
                         "the normal sha-256 sidecars, so the later full run skips them.")
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
    assert_clean(chunks, cfg.get("sections"))
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

    settings_by_delivery = resolve_settings(cfg)
    write_voice_plan(ep, chunks, out_dir, voice_plan, settings_by_delivery)
    print(f"voice_plan -> {voice_plan.relative_to(ROOT)}")
    if args.plan_only:
        return 0

    # The subset to SPEND on. `chunks` stays whole: assert_clean has already proved the
    # full script's section coverage above, and concat_master/write_index below still see
    # every chunk. Only the generation loop is narrowed.
    gen_chunks = chunks
    if args.measure_section:
        gen_chunks = [c for c in chunks if c["section"] == args.measure_section]
        if not gen_chunks:
            print(f"ERROR: no chunks in section {args.measure_section!r}; "
                  f"sections present = {sorted({c['section'] for c in chunks})}")
            return 1
        sub_chars = sum(len(c["spoken_text"]) for c in gen_chunks)
        print(f"MEASURE MODE: {args.measure_section} only -- {len(gen_chunks)} chunk(s), "
              f"{sum(len(c['spoken_text'].split()) for c in gen_chunks)} words, "
              f"{sub_chars} chars, est ${sub_chars / 1000 * COST_PER_1K_CHARS_USD:.2f}")

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
        for c in gen_chunks:
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
                               "voice_settings": settings_by_delivery[c["delivery"]]}).encode("utf-8")
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

    if args.measure_section:
        secs = [dur(outdir / f"{c['chunk_id']}.mp3") for c in gen_chunks]
        if not all(secs):
            print("ERROR: at least one chunk measured 0.000s -- refusing to report a rate")
            return 1
        speech = round(sum(secs), 3)
        sw = sum(len(c["spoken_text"].split()) for c in gen_chunks)
        n_gaps = len(gen_chunks) - 1
        gaps = args.gap_beat * n_gaps
        finished = speech + gaps
        print(f"MEASURED section={args.measure_section} chunks={len(gen_chunks)} words={sw}")
        print(f"  speech          {speech:.3f}s  ({speech / 60:.2f} min)  "
              f"raw {sw / (speech / 60):.1f} wpm")
        print(f"  + {n_gaps} beat gap(s) @ {args.gap_beat}s = {gaps:.1f}s")
        print(f"  finished        {finished:.3f}s  ({finished / 60:.2f} min)  "
              f"{sw / (finished / 60):.1f} words per finished minute")
        print("no master and no index written: --measure-section stops before both.")
        return 0

    master = media_root() / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3"
    offsets = concat_master(chunks, outdir, master, args.gap_beat, args.gap_section)
    index = write_index(ep, source_script_rel, chunks, offsets, master, index_path,
                        est, args.gap_beat, args.gap_section, settings_by_delivery)
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
