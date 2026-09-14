#!/usr/bin/env python3
r"""Independent PADDING gate — the direct anti-"水増しで20分" detector.

The owner's recurring complaint about a long cut is that it was STRETCHED to hit a
runtime instead of earning it: dead air inserted around the lines, and the same point
restated in slightly different words ("synonym filler"). A 20-minute video that is
really 14 minutes of content plus 6 minutes of silence and repetition is padding.

This gate measures that INTENT on the narration itself — the spoken text and, when
present, the per-chunk [start,end] timings in narration_index — NOT on a proxy that a
stretched cut could satisfy. It fires on real padding signatures:

  1. DEAD AIR — silence used to eat clock. Measured in FOUR places, not just between
     consecutive lines:
       a. INTER-CHUNK gaps between consecutive lines. It does NOT punish the deliberate
          section beat (a pause at a HOOK->OPENING->ACT boundary is good pacing): a gap at
          a *section change* is allowed up to BEAT_MAX; a gap *inside* one section over
          MID_GAP_MAX, or ANY gap over HARD_GAP_MAX, is padding.
       b. LEADING silence before the first spoken line (start >> 0).
       c. TRAILING silent outro: the render/audio was declared to run to
          `generated_total_seconds` (or `totals.estimated_seconds`) but narration stops
          well before the end — a silent tail used to pad runtime.
       d. WITHIN-CHUNK dead air: a single chunk whose clock duration far exceeds the time
          it could possibly take to speak its words (words / MIN_SPEECH_WPS) is hiding a
          long pause inside the line.
     It also fails if total dead air exceeds DEAD_AIR_FRAC_MAX of the runtime (pervasive slack).

  2. RESTATED SENTENCES (near-verbatim) — near-duplicate sentences (SequenceMatcher ratio
     >= DUP_RATIO) that say the same thing twice with the same word order.

  3. PARAPHRASED SENTENCES (semantic) — non-adjacent sentences that share most of their
     CONTENT words (bag-of-content-words Jaccard >= JACCARD_DUP) even after the word order
     and function words are changed. This is synonym/paraphrase padding that (2) misses:
     reordering and light rewording drop the SequenceMatcher ratio below DUP_RATIO, but the
     set of meaning-bearing words barely changes, so the Jaccard stays high.

  4. REPEATED LONG PHRASES — the same >= NGRAM_N-word phrase recurring across the script.
     A stitched-from-boilerplate pad reuses whole clauses; genuine narration rarely repeats
     a 7-word run more than once (a thematic refrain is tolerated up to a small floor).

Every finding is reported as a concrete padded SPAN (timestamp for dead air, the offending
sentence pair / phrase for repetition) so a human can see exactly where the water is.

Design notes:
  * Read-only. Never writes into the episode. Never raises on missing inputs — returns a
    skip dict so it can never crash check_final_acceptance.
  * Deterministic: no clock, no randomness. Same input -> same verdict.
  * Thresholds were calibrated with headroom against a clean real episode
    (PD-2026-032-carsearch: 6.2% dead air, 0s leading, ~0s trailing, worst within-chunk
    slack 2.8s, 0 near-dup and 0 paraphrase pairs, <=1 repeated 6-gram) so a well-made cut
    passes and a padded one fails.

check_final_acceptance can import this module and call evaluate(epdir); the returned dict
follows the gate contract {"check","ok","hard","reason", ...numbers...}. Keep those keys stable.

Usage:
  py -3.11 scripts/check_padding.py --ep PD-2026-032-carsearch
  py -3.11 scripts/check_padding.py --ep PD-2026-032-carsearch --dry-run
  py -3.11 scripts/check_padding.py --ep PD-2026-032-carsearch --json out.json
  py -3.11 scripts/check_padding.py --selftest        # RED fixtures + real episode numbers

Exit code: 0 = PASS (or --dry-run / skip), 1 = FAIL or usage error.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-032-carsearch"
CHECK_NAME = "padding"

# --- dead-air thresholds (seconds) -------------------------------------------------------------
# A pause at a SECTION CHANGE is deliberate pacing (good). A pause INSIDE a section, or any
# absurdly long pause, is dead air used to stretch runtime.
MID_GAP_MAX = 1.5        # same-section gap over this = padded dead air
BEAT_MAX = 3.0           # a section-boundary beat is allowed up to this (calibrated: real = 2.5s)
HARD_GAP_MAX = 4.0       # ANY gap over this is padding, boundary or not
DEAD_AIR_FRAC_MAX = 0.18 # total silence / runtime over this = pervasive slack (real = 0.062)

# --- edge / within-chunk silence thresholds (seconds) ------------------------------------------
LEAD_SILENCE_MAX = 2.0   # dead air before the first spoken line (real = 0.0)
TRAIL_SILENCE_MAX = 3.0  # silent outro: declared render end minus last spoken line (real ~ 0.0)
WITHIN_CHUNK_GAP_MAX = 8.0  # (chunk clock duration) - (words / MIN_SPEECH_WPS) over this = inner pause
MIN_SPEECH_WPS = 3.0     # fastest floor speaking rate; real episode averages ~3.0 wps (worst slack 2.8s)

# --- text-repetition thresholds ----------------------------------------------------------------
MIN_SENT_WORDS = 4       # ignore fragments shorter than this when comparing sentences
DUP_RATIO = 0.80         # SequenceMatcher ratio at/above which two sentences are "the same"
DUP_PAIRS_MAX = 2        # tolerate up to this many near-dup sentence pairs (real = 0); over = FAIL
JACCARD_DUP = 0.60       # content-word Jaccard at/above which two sentences are paraphrases
JACCARD_MIN_CONTENT = 4  # need at least this many content words before a Jaccard match counts
PARAPHRASE_PAIRS_MAX = 2 # tolerate up to this many paraphrase pairs (real = 0); over = FAIL
NGRAM_N = 7              # length of the "long phrase" whose recurrence signals boilerplate padding
REPEAT_NGRAM_MAX = 4     # tolerate this many distinct repeated 7-grams (real = 0); over = FAIL
NGRAM_HARD_COUNT = 3     # a single 7-gram repeated this many+ times = padding on its own

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[a-z0-9']+")

# Function words carry structure, not meaning; paraphrase padding reshuffles these while
# keeping the meaning-bearing content words. Excluding them makes the Jaccard measure the
# actual overlap of ideas rather than of grammar.
_STOPWORDS = frozenset("""
a an the this that these those there here it its it's they them their theirs he she his her
him you your yours we us our ours i me my mine who whom whose which what when where why how
and or but nor so yet for as if than then because while although though whether
of to in on at by from with without within into onto over under above below between among
about against during before after around through across near off out up down
is are was were be been being am do does did done have has had having will would shall should
can could may might must not no yes only just also too very more most much many few less least
such same other another each every any all both either neither some none one two three
""".split())


def _norm(text: str) -> str:
    """Lowercase, strip to alphanumerics + single spaces (comparable core of a phrase)."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", text.lower())).strip()


def _content_tokens(norm_sentence: str) -> frozenset[str]:
    """Bag of meaning-bearing words: normalized tokens with stopwords and 1-2 char tokens dropped."""
    return frozenset(w for w in norm_sentence.split()
                     if w not in _STOPWORDS and len(w) > 2)


# ---------------------------------------------------------------------------------------------
# input resolution
# ---------------------------------------------------------------------------------------------

def resolve_narration_index(ep_dir: Path) -> Optional[Path]:
    """Pick the narration_index.v*.json (excluding the vertical 'short' index) whose chunks
    carry the most usable timed+spoken data. Returns None if none exists."""
    cands = [p for p in (ep_dir / "06_audio").glob("narration_index.v*.json")
             if "short" not in p.name.lower()]
    if not cands:
        return None

    def _score(p: Path) -> tuple[int, str]:
        try:
            chunks = (json.loads(p.read_text("utf-8")) or {}).get("chunks", [])
        except Exception:  # noqa: BLE001 - malformed file scores 0, never crashes resolution
            return (0, p.name)
        n = sum(1 for c in chunks
                if isinstance(c, dict)
                and str(c.get("spoken_text", c.get("text", ""))).strip()
                and c.get("start") is not None and c.get("end") is not None)
        return (n, p.name)

    return max(cands, key=_score)


def _declared_end(data: dict[str, Any]) -> Optional[float]:
    """The runtime the render/audio was DECLARED to fill, from index-level totals. Used to
    detect a silent outro (declared end well past the last spoken line). None if not stated."""
    for key in ("generated_total_seconds", "render_seconds", "duration_seconds", "film_seconds"):
        v = data.get(key)
        if isinstance(v, (int, float)) and v > 0:
            return float(v)
    tot = data.get("totals")
    if isinstance(tot, dict):
        # Prefer the ACTUAL generated length over the pre-TTS word-count estimate: once narration
        # is voiced, `generated_seconds` is the real audio end. Using `estimated_seconds` (a guess
        # made before generation) as the declared end fabricates a trailing-silence span equal to
        # (estimate - actual), which is not real dead air. `estimated_seconds` stays only as a
        # last-resort fallback when no generated/render length was recorded.
        for key in ("generated_seconds", "render_seconds", "seconds", "estimated_seconds"):
            v = tot.get(key)
            if isinstance(v, (int, float)) and v > 0:
                return float(v)
    return None


def load_chunks(ep_dir: Path) -> tuple[list[dict[str, Any]], Optional[Path], Optional[float]]:
    """Return (chunks, source_path, declared_end). Each chunk keeps text/section and, when
    numeric, start/end. Returns ([], None, None) when no narration index is present."""
    src = resolve_narration_index(ep_dir)
    if src is None:
        return [], None, None
    try:
        data = json.loads(src.read_text("utf-8")) or {}
    except Exception:  # noqa: BLE001
        return [], src, None
    chunks = data.get("chunks", [])
    out: list[dict[str, Any]] = []
    for c in chunks:
        if not isinstance(c, dict):
            continue
        txt = str(c.get("spoken_text", c.get("text", ""))).strip()
        if not txt:
            continue
        s, e = c.get("start"), c.get("end")
        out.append({
            "text": txt,
            "section": str(c.get("section", "")).strip(),
            "start": float(s) if isinstance(s, (int, float)) else None,
            "end": float(e) if isinstance(e, (int, float)) else None,
        })
    return out, src, _declared_end(data)


# ---------------------------------------------------------------------------------------------
# padding detectors
# ---------------------------------------------------------------------------------------------

def _fmt_ts(sec: float) -> str:
    m, s = divmod(max(0.0, sec), 60)
    return f"{int(m):d}:{s:05.2f}"


def find_dead_air(chunks: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], float, float, bool]:
    """Scan inter-chunk gaps. Returns (padded_gaps, total_dead_air, span_seconds, has_timing).

    A gap is padded when it is a same-section pause over MID_GAP_MAX, or ANY pause over
    HARD_GAP_MAX. A section-boundary beat up to BEAT_MAX is allowed (deliberate pacing)."""
    timed = [c for c in chunks if c["start"] is not None and c["end"] is not None]
    if len(timed) < 2:
        return [], 0.0, 0.0, False
    padded: list[dict[str, Any]] = []
    total_dead = 0.0
    prev = timed[0]
    for cur in timed[1:]:
        gap = cur["start"] - prev["end"]
        if gap > 0:
            total_dead += gap
        boundary = cur["section"] != prev["section"]
        limit = BEAT_MAX if boundary else MID_GAP_MAX
        if gap > limit or gap > HARD_GAP_MAX:
            padded.append({
                "at": prev["end"],
                "gap": round(gap, 3),
                "boundary": boundary,
                "section": cur["section"],
                "kind": ("over-long boundary beat" if boundary else "mid-section dead air")
                        if gap <= HARD_GAP_MAX else "extreme dead air",
            })
        prev = cur
    span = timed[-1]["end"] - timed[0]["start"]
    return padded, round(total_dead, 3), round(span, 3), True


def find_edge_silence(chunks: list[dict[str, Any]], declared_end: Optional[float]
                      ) -> tuple[list[dict[str, Any]], float, float, float]:
    """Silence that inter-chunk scanning misses: LEADING (before line 1), TRAILING (silent
    outro up to the declared render end), and WITHIN-CHUNK (one line far longer than the
    time its words could take). Returns (padded_spans, leading_s, trailing_s, within_dead_s)."""
    timed = [c for c in chunks if c["start"] is not None and c["end"] is not None]
    spans: list[dict[str, Any]] = []
    if not timed:
        return [], 0.0, 0.0, 0.0

    leading = max(0.0, timed[0]["start"])
    if leading > LEAD_SILENCE_MAX:
        spans.append({"at": 0.0, "gap": round(leading, 3), "section": timed[0]["section"],
                      "kind": "leading silence"})

    trailing = 0.0
    if declared_end is not None:
        trailing = max(0.0, declared_end - timed[-1]["end"])
        if trailing > TRAIL_SILENCE_MAX:
            spans.append({"at": timed[-1]["end"], "gap": round(trailing, 3),
                          "section": timed[-1]["section"], "kind": "trailing silent outro"})

    within_dead = 0.0
    for c in timed:
        words = len(_WORD.findall(c["text"].lower()))
        if words <= 0:
            continue
        dur = c["end"] - c["start"]
        slack = dur - words / MIN_SPEECH_WPS   # clock time beyond the fastest possible delivery
        if slack > WITHIN_CHUNK_GAP_MAX:
            within_dead += slack
            spans.append({"at": c["start"], "gap": round(slack, 3), "section": c["section"],
                          "kind": "within-chunk dead air"})
    return spans, round(leading, 3), round(trailing, 3), round(within_dead, 3)


def _sentences(chunks: list[dict[str, Any]]) -> list[str]:
    """Normalized sentences (>= MIN_SENT_WORDS words) across the whole narration, in order."""
    full = " ".join(c["text"] for c in chunks)
    out: list[str] = []
    for raw in _SENT_SPLIT.split(full):
        n = _norm(raw)
        if len(n.split()) >= MIN_SENT_WORDS:
            out.append(n)
    return out


def find_restated_sentences(sents: list[str]) -> list[dict[str, Any]]:
    """Near-VERBATIM duplicate sentence pairs (SequenceMatcher ratio >= DUP_RATIO). Each idea
    is only reported once (a sentence already matched to an earlier one is not re-paired)."""
    pairs: list[dict[str, Any]] = []
    claimed: set[int] = set()
    for i in range(len(sents)):
        if i in claimed:
            continue
        for j in range(i + 1, len(sents)):
            if j in claimed:
                continue
            ratio = difflib.SequenceMatcher(None, sents[i], sents[j]).ratio()
            if ratio >= DUP_RATIO:
                claimed.add(j)
                pairs.append({"ratio": round(ratio, 3), "a": sents[i], "b": sents[j]})
    return pairs


def find_paraphrased_sentences(sents: list[str]) -> list[dict[str, Any]]:
    """Semantic (paraphrase) duplicates the verbatim detector misses: NON-ADJACENT sentences
    whose CONTENT-word sets overlap by Jaccard >= JACCARD_DUP. Reordering / synonym-light
    rewording keeps the content-word set but drops the SequenceMatcher ratio, so this is the
    detector that catches "say it again in different words" filler.

    Only pairs with SequenceMatcher ratio < DUP_RATIO are reported here, so a pair is counted
    by exactly one of the two repetition detectors (verbatim vs paraphrase)."""
    toks = [_content_tokens(s) for s in sents]
    pairs: list[dict[str, Any]] = []
    claimed: set[int] = set()
    for i in range(len(sents)):
        if i in claimed or len(toks[i]) < JACCARD_MIN_CONTENT:
            continue
        for j in range(i + 2, len(sents)):   # non-adjacent only: skip immediate neighbour
            if j in claimed or len(toks[j]) < JACCARD_MIN_CONTENT:
                continue
            union = len(toks[i] | toks[j])
            if union == 0:
                continue
            jac = len(toks[i] & toks[j]) / union
            if jac >= JACCARD_DUP and (
                    difflib.SequenceMatcher(None, sents[i], sents[j]).ratio() < DUP_RATIO):
                claimed.add(j)
                pairs.append({"jaccard": round(jac, 3), "a": sents[i], "b": sents[j]})
    return pairs


def find_repeated_phrases(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Distinct NGRAM_N-word phrases that recur across the narration, most-repeated first."""
    words = _norm(" ".join(c["text"] for c in chunks)).split()
    counts: dict[tuple[str, ...], int] = {}
    for i in range(len(words) - NGRAM_N + 1):
        g = tuple(words[i:i + NGRAM_N])
        counts[g] = counts.get(g, 0) + 1
    reps = [{"phrase": " ".join(g), "count": c} for g, c in counts.items() if c >= 2]
    reps.sort(key=lambda r: (-r["count"], r["phrase"]))
    return reps


# ---------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ---------------------------------------------------------------------------------------------

def evaluate(epdir: Path) -> dict[str, Any]:
    """Measure narration padding and return a gate dict. NEVER calls sys.exit; never raises on
    missing inputs (returns a skip dict). Keys: check, ok, hard, reason, skipped?, plus numbers:
    dead_air_gaps, dead_air_seconds, dead_air_frac, edge_gaps, leading_silence_s,
    trailing_silence_s, within_chunk_dead_s, restated_pairs, paraphrase_pairs,
    repeated_phrases, problems."""
    epdir = Path(epdir)
    chunks, src, declared_end = load_chunks(epdir)
    if not chunks:
        return {"check": CHECK_NAME, "ok": True, "hard": False, "skipped": True,
                "reason": f"no narration index with spoken text under {epdir / '06_audio'} "
                          "(likely on SSD) - padding not measurable"}

    dead_gaps, dead_secs, span, has_timing = find_dead_air(chunks)
    edge_gaps, leading_s, trailing_s, within_dead_s = find_edge_silence(chunks, declared_end)
    total_dead = round(dead_secs + within_dead_s + trailing_s + leading_s, 3)
    dead_frac = round(total_dead / span, 4) if span > 0 else 0.0

    sents = _sentences(chunks)
    restated = find_restated_sentences(sents)
    paraphrased = find_paraphrased_sentences(sents)
    repeated = find_repeated_phrases(chunks)
    hard_repeats = [r for r in repeated if r["count"] >= NGRAM_HARD_COUNT]

    problems: list[str] = []
    if has_timing:
        if dead_gaps:
            worst = max(dead_gaps, key=lambda g: g["gap"])
            problems.append(
                f"{len(dead_gaps)} padded dead-air gap(s); worst {worst['gap']:.2f}s at "
                f"{_fmt_ts(worst['at'])} ({worst['kind']})")
        if leading_s > LEAD_SILENCE_MAX:
            problems.append(f"leading silence {leading_s:.2f}s before first line > "
                            f"{LEAD_SILENCE_MAX:.0f}s")
        if trailing_s > TRAIL_SILENCE_MAX:
            problems.append(
                f"trailing silent outro {trailing_s:.2f}s after last line at "
                f"{_fmt_ts(chunks[-1]['end'] if chunks[-1]['end'] else 0.0)} > "
                f"{TRAIL_SILENCE_MAX:.0f}s")
        within = [g for g in edge_gaps if g["kind"] == "within-chunk dead air"]
        if within:
            w = max(within, key=lambda g: g["gap"])
            problems.append(f"{len(within)} within-chunk dead-air span(s); worst {w['gap']:.2f}s "
                            f"at {_fmt_ts(w['at'])}")
        if dead_frac > DEAD_AIR_FRAC_MAX:
            problems.append(
                f"total dead air {dead_frac*100:.1f}% of runtime > {DEAD_AIR_FRAC_MAX*100:.0f}%")
    if len(restated) > DUP_PAIRS_MAX:
        ex = "; ".join(f"[{p['ratio']:.2f}] {p['a'][:40]!r}~{p['b'][:40]!r}" for p in restated[:3])
        problems.append(f"{len(restated)} restated near-duplicate sentence(s) > {DUP_PAIRS_MAX}: {ex}")
    if len(paraphrased) > PARAPHRASE_PAIRS_MAX:
        ex = "; ".join(f"[J{p['jaccard']:.2f}] {p['a'][:36]!r}~{p['b'][:36]!r}"
                       for p in paraphrased[:3])
        problems.append(
            f"{len(paraphrased)} paraphrased (same-idea) sentence(s) > {PARAPHRASE_PAIRS_MAX}: {ex}")
    if len(repeated) > REPEAT_NGRAM_MAX:
        problems.append(
            f"{len(repeated)} distinct {NGRAM_N}-word phrase(s) repeat > {REPEAT_NGRAM_MAX}")
    if hard_repeats:
        w = hard_repeats[0]
        problems.append(
            f"phrase repeated x{w['count']} (>= {NGRAM_HARD_COUNT}): {w['phrase'][:60]!r}")

    ok = not problems
    return {
        "check": CHECK_NAME,
        "ok": ok,
        "hard": True,
        "reason": ("no padding: pacing beats deliberate, no silent tail, no restated/"
                   "paraphrased/boilerplate lines" if ok else "; ".join(problems)),
        "source": str(src) if src else None,
        "chunks": len(chunks),
        "has_timing": has_timing,
        "declared_end_s": declared_end,
        "runtime_span_s": span,
        "dead_air_seconds": total_dead,
        "inter_chunk_dead_seconds": dead_secs,
        "dead_air_frac": dead_frac,
        "dead_air_gaps": dead_gaps,
        "edge_gaps": edge_gaps,
        "leading_silence_s": leading_s,
        "trailing_silence_s": trailing_s,
        "within_chunk_dead_s": within_dead_s,
        "restated_pairs": restated,
        "paraphrase_pairs": paraphrased,
        "repeated_phrases": repeated[:10],
        "repeated_phrase_count": len(repeated),
        "problems": problems,
    }


# ---------------------------------------------------------------------------------------------
# reporting / CLI
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("PADDING REPORT  (anti-'水増しで20分' — dead air + restated/paraphrased/boilerplate)")
    print("=" * 78)
    print(f"  source        : {r['source']}")
    print(f"  narration     : {r['chunks']} chunks, span {r['runtime_span_s']:.1f}s, "
          f"declared_end={r['declared_end_s']}, timing={'yes' if r['has_timing'] else 'NO'}")
    print(f"  dead air      : {r['dead_air_seconds']:.1f}s total "
          f"({r['dead_air_frac']*100:.1f}% of runtime; cap {DEAD_AIR_FRAC_MAX*100:.0f}%)")
    print(f"                  inter-chunk {r['inter_chunk_dead_seconds']:.1f}s | "
          f"leading {r['leading_silence_s']:.1f}s (cap {LEAD_SILENCE_MAX:.0f}) | "
          f"trailing {r['trailing_silence_s']:.1f}s (cap {TRAIL_SILENCE_MAX:.0f}) | "
          f"within-chunk {r['within_chunk_dead_s']:.1f}s")
    print(f"  padded gaps   : {len(r['dead_air_gaps'])} inter-chunk + {len(r['edge_gaps'])} edge/inner "
          f"(same-section > {MID_GAP_MAX}s, boundary > {BEAT_MAX}s, any > {HARD_GAP_MAX}s)")
    for g in (r["dead_air_gaps"] + r["edge_gaps"])[:10]:
        print(f"      {g['gap']:+.2f}s at {_fmt_ts(g['at'])}  {g['kind']} -> {g['section']!r}")
    print(f"  restated lines: {len(r['restated_pairs'])}  (near-verbatim, cap {DUP_PAIRS_MAX})")
    for p in r["restated_pairs"][:6]:
        print(f"      [{p['ratio']:.2f}] {p['a'][:52]!r}")
        print(f"             ~ {p['b'][:52]!r}")
    print(f"  paraphrased   : {len(r['paraphrase_pairs'])}  (content-word Jaccard >= "
          f"{JACCARD_DUP}, cap {PARAPHRASE_PAIRS_MAX})")
    for p in r["paraphrase_pairs"][:6]:
        print(f"      [J{p['jaccard']:.2f}] {p['a'][:52]!r}")
        print(f"              ~ {p['b'][:52]!r}")
    print(f"  repeated {NGRAM_N}-grams: {r['repeated_phrase_count']}  (cap {REPEAT_NGRAM_MAX}; "
          f"any x{NGRAM_HARD_COUNT}+ fails)")
    for rp in r["repeated_phrases"][:6]:
        print(f"      x{rp['count']}: {rp['phrase'][:56]!r}")
    print("\n" + "-" * 78)
    if r["ok"]:
        print("  RESULT: PASS  — runtime is earned, not padded with silence or repetition")
    else:
        print("  RESULT: FAIL")
        for p in r["problems"]:
            print(f"    - {p}")
    print("-" * 78)


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    """Write JSON atomically (temp file in the same dir, then os.replace)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# ---------------------------------------------------------------------------------------------
# selftest: RED fixtures (known-bad) must FAIL, then real episode numbers
# ---------------------------------------------------------------------------------------------

def _selftest() -> int:
    print("=" * 78)
    print("SELFTEST 1/4 — RED FIXTURE A: DEAD AIR (6s mid-section silence must report ok=False)")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td)
        (ep / "06_audio").mkdir(parents=True)
        chunks = [
            {"chunk_id": "VC-0001", "section": "ACT I", "start": 0.0, "end": 6.0,
             "spoken_text": "The officer walked up to the driver's window and asked for a license."},
            # 6.0 -> 12.0 = a 6.0s same-section gap = extreme dead air used to eat clock
            {"chunk_id": "VC-0002", "section": "ACT I", "start": 12.0, "end": 18.0,
             "spoken_text": "The driver handed it over without saying a single word to him."},
            {"chunk_id": "VC-0003", "section": "ACT I", "start": 18.6, "end": 24.0,
             "spoken_text": "This is a totally different sentence about the highway stop later."},
        ]
        _atomic_write_json(ep / "06_audio" / "narration_index.v001.json",
                           {"generated_total_seconds": 24.0, "chunks": chunks})
        ra = evaluate(ep)
    a_fail = (ra.get("ok") is False and len(ra.get("dead_air_gaps", [])) >= 1)
    print(f"  verdict ok={ra.get('ok')}  dead_air_gaps={len(ra.get('dead_air_gaps', []))}")
    print(f"  reason: {ra.get('reason')}")
    print("  DEAD-AIR PRONG: PASS" if a_fail else "  DEAD-AIR PRONG: FAIL")

    print("\n" + "=" * 78)
    print("SELFTEST 2/4 — RED FIXTURE B: NEAR-VERBATIM REPETITION (restated lines -> ok=False)")
    print("=" * 78)
    base = "the police can search your car without a warrant if there is probable cause here"
    variants = [
        base,
        base.replace(" if ", " when "),
        base.replace(" your car ", " your vehicle "),
        base.replace(" here", " today"),
    ]
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td)
        (ep / "06_audio").mkdir(parents=True)
        chunks = []
        t = 0.0
        for i, v in enumerate(variants, 1):
            chunks.append({"chunk_id": f"VC-{i:04d}", "section": "ACT I",
                           "start": round(t, 3), "end": round(t + 5.0, 3),
                           "spoken_text": v.capitalize() + "."})
            t += 5.6  # 0.6s clean beat, never dead air
        _atomic_write_json(ep / "06_audio" / "narration_index.v001.json",
                           {"generated_total_seconds": round(t - 0.6, 3), "chunks": chunks})
        rb = evaluate(ep)
    b_fail = (rb.get("ok") is False and len(rb.get("dead_air_gaps", [])) == 0
              and (len(rb.get("restated_pairs", [])) > DUP_PAIRS_MAX
                   or rb.get("repeated_phrase_count", 0) > REPEAT_NGRAM_MAX))
    print(f"  verdict ok={rb.get('ok')}  dead_air_gaps={len(rb.get('dead_air_gaps', []))}  "
          f"restated_pairs={len(rb.get('restated_pairs', []))}  "
          f"repeated_7grams={rb.get('repeated_phrase_count')}")
    print(f"  reason: {rb.get('reason')}")
    print("  VERBATIM PRONG: PASS" if b_fail else "  VERBATIM PRONG: FAIL")

    print("\n" + "=" * 78)
    print("SELFTEST 3/4 — RED FIXTURE C: THE REVIEWER'S GAMING PROBE")
    print("  (a PARAPHRASED duplicate paragraph + a 30s TRAILING silence; the old gate passed")
    print("   this because no gap is near-verbatim and no gap sits BETWEEN two lines)")
    print("=" * 78)
    # A 3-sentence paragraph, then unrelated filler, then the SAME paragraph reworded: word order
    # shuffled and function words swapped so SequenceMatcher ratio < 0.80 (verbatim detector
    # misses it) while the content-word sets barely change so Jaccard >= 0.60 (paraphrase catches).
    para_a = ("The Supreme Court ruled that a warrantless vehicle search violates the Fourth "
              "Amendment. Officers must show probable cause before they open a locked trunk. "
              "A driver can refuse consent and the stop cannot be extended without cause.")
    filler = ("Rain fell steadily on the empty parking lot outside the county courthouse. "
              "A single lamp buzzed above the clerk's window down the quiet hall.")
    para_b = ("A warrantless vehicle search violates the Fourth Amendment, according to how the "
              "Supreme Court ruled. Before they open a locked trunk, officers must show probable "
              "cause. Without cause the stop cannot be extended, and a driver can refuse consent.")
    texts = [para_a, filler, para_b]
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td)
        (ep / "06_audio").mkdir(parents=True)
        chunks = []
        t = 0.0
        for i, tx in enumerate(texts, 1):
            words = len(_WORD.findall(tx.lower()))
            dur = round(words / 3.0, 3)          # natural speaking rate, no within-chunk pause
            chunks.append({"chunk_id": f"VC-{i:04d}", "section": "ACT I",
                           "start": round(t, 3), "end": round(t + dur, 3), "spoken_text": tx})
            t += dur + 0.5                        # 0.5s clean beat, never a padded gap
        last_end = chunks[-1]["end"]
        # 30s silent outro: render/audio declared to run 30s past the final spoken word.
        _atomic_write_json(ep / "06_audio" / "narration_index.v001.json",
                           {"generated_total_seconds": round(last_end + 30.0, 3), "chunks": chunks})
        rc = evaluate(ep)
    # Prove BOTH previously-missed holes fire and that the OLD detectors do NOT (so this is
    # genuinely the new code failing the probe, not the old code).
    no_old_signal = (len(rc.get("dead_air_gaps", [])) == 0
                     and len(rc.get("restated_pairs", [])) <= DUP_PAIRS_MAX)
    paraphrase_fires = len(rc.get("paraphrase_pairs", [])) > PARAPHRASE_PAIRS_MAX
    trailing_fires = rc.get("trailing_silence_s", 0.0) > TRAIL_SILENCE_MAX
    c_fail = (rc.get("ok") is False and no_old_signal and paraphrase_fires and trailing_fires)
    print(f"  verdict ok={rc.get('ok')}")
    print(f"  OLD detectors quiet: inter_chunk_gaps={len(rc.get('dead_air_gaps', []))}  "
          f"restated_pairs={len(rc.get('restated_pairs', []))}  (both within tolerance)")
    print(f"  NEW detectors fire : paraphrase_pairs={len(rc.get('paraphrase_pairs', []))} "
          f"(cap {PARAPHRASE_PAIRS_MAX})  trailing_silence={rc.get('trailing_silence_s')}s "
          f"(cap {TRAIL_SILENCE_MAX})")
    print(f"  reason: {rc.get('reason')}")
    print("  PROBE PRONG: PASS" if c_fail else "  PROBE PRONG: FAIL")

    red_ok = a_fail and b_fail and c_fail
    print("\n" + ("RED-FIXTURE: PASS" if red_ok else "RED-FIXTURE: FAIL")
          + "  (all padding prongs proven to fail on known-bad input)")

    print("\n" + "=" * 78)
    print(f"SELFTEST 4/4 — REAL EPISODE {DEFAULT_EP} (actual measured numbers; must PASS)")
    print("=" * 78)
    r2 = evaluate(ROOT / "episodes" / DEFAULT_EP)
    _print_report(r2)
    green_ok = bool(r2.get("skipped")) or bool(r2.get("ok"))
    print("\n" + ("GREEN-CASE: PASS" if green_ok else "GREEN-CASE: FAIL")
          + "  (a well-made real cut is not falsely flagged)")
    return 0 if (red_ok and green_ok) else 1


def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # em-dashes / Japanese in narration text
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="Independent padding gate: FAIL on dead-air / restated / paraphrased / boilerplate.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--dry-run", action="store_true",
                    help="evaluate and print, but always exit 0 (never blocks)")
    ap.add_argument("--json", nargs="?", const="-", default=None,
                    help="also emit the raw result dict as JSON (path, or '-' for stdout)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixtures (must fail) then print real-episode numbers")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    r = evaluate(ep_dir)
    _print_report(r)
    if args.json:
        if args.json == "-":
            print(json.dumps(r, indent=2, ensure_ascii=False, default=str))
        else:
            _atomic_write_json(Path(args.json), r)
            print(f"\n[wrote] {args.json}")

    if args.dry_run or r.get("skipped"):
        return 0
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
