#!/usr/bin/env python3
r"""Independent AI-smell / cadence linter for the narration TEXT — the gate that would catch
the owner's recurring defect #8 ("内容がAI臭い / 一流作家の雰囲気にする").

The other ship gates measure the RENDER (timing, motion, audio). None of them read the WORDS and
ask "does this read like a first-class human documentary, or like templated AI filler?" This gate
does exactly that, on the approved narration (annotated spans, falling back to the `[VO:]` lines of
script.en), and FAILs on three concrete, measurable AI-smell signatures:

  1. BANNED CLICHE  — any of the canned narration crutches ("the answer may surprise you",
     "little did they know", "but here's the thing", "in a world where", ...). This list is
     REUSED from scripts/validate_episode.BANNED (the repo's single source of truth for filler
     phrases) and only EXTENDED with a few more well-known LLM tells — never redefined weaker.

  2. ROBOTIC CADENCE — real prose varies its sentence length hard (a 3-word punch after a 40-word
     build). AI filler drones in a narrow band. We measure the coefficient of variation (CV =
     pstdev/mean) of per-sentence word counts and FAIL when it collapses below a floor.

  3. PROPER-NOUN STUFFING — sentences packed with capitalized names read like a Wikipedia dump,
     not narration. We measure the global proper-noun density (non-sentence-initial capitalized
     tokens) and FAIL when it is unnaturally high, and we surface the worst individual sentences.

Sentence splitting and word tokenizing deliberately mirror scripts/validate_episode.py so this
gate speaks the same numbers as the script-stage QC (no divergent re-definition).

Usage:
  py -3.11 scripts/verify_script_lint.py --ep PD-2026-032-carsearch
  py -3.11 scripts/verify_script_lint.py --ep PD-2026-032-carsearch --dry-run
  py -3.11 scripts/verify_script_lint.py --ep PD-2026-032-carsearch --json out/lint.json
  py -3.11 scripts/verify_script_lint.py --selftest      # RED fixture + real-episode numbers

Exit codes: 0 = PASS (or dry-run, or honest skip when the script text is absent), 1 = FAIL / usage.

check_final_acceptance can `import verify_script_lint; verify_script_lint.evaluate(epdir)`; the
returned dict keys (check / ok / hard / reason / ...numbers) are the stable contract. evaluate()
NEVER calls sys.exit and NEVER raises on missing inputs — it returns a skip dict instead.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-032-carsearch"

# --- FAIL thresholds (module constants; calibrated against the hand-written EP32 script) --------
# EP32 (first-class human prose) measures CV=0.754, proper-noun density=0.031, over 94 sentences —
# both far on the safe side of these floors/ceilings, so the gate keeps real headroom and is not
# tuned to just-pass.
#
# TIGHTENING 2026-07-07 (independent review: the old floors 0.35 / 0.22 only tripped on EGREGIOUS
# scripts; a MODERATELY AI-smelly script sailed through). The reviewer's own scale: robotic cadence
# CV ~0.08, human ~0.75; typical human proper-noun density ~0.03. The old CV floor (0.35) sat far
# below the human band, so a monotone-ish draft at CV~0.40 passed; the old proper-noun ceiling
# (0.22) sat ~7x above typical, so a name-dump at 0.15 passed. Raised the CV floor toward the human
# band and lowered the proper-noun ceiling toward the typical human value so a MODERATE offender now
# FAILS, while the real EP32 prose (0.754 / 0.031) still clears both with wide margin. NOT weakened.
MIN_CADENCE_CV = 0.45          # FAIL if sentence-length CV < this (monotone/robotic; human ~0.75, robotic ~0.08)
MAX_PROPER_NOUN_RATIO = 0.10   # FAIL if global proper-noun density > this (name-dump; typical human ~0.03)
# Cadence sub-check minimum. The OLD value (12) SILENTLY SKIPPED the cadence check for any script
# with < 12 sentences — a gaming hole: an 11-sentence, uniform-length draft dodged the cadence gate
# entirely. Lowered so the check RUNS on short scripts too. It is not zeroed because CV needs a few
# data points to mean anything; 4 sentences is the smallest count at which a collapsed CV is a real
# signal rather than sampling noise. Below 4 the check honestly reports "insufficient sentences".
MIN_SENTENCES_FOR_CADENCE = 4  # run the CV check whenever there are at least this many sentences
STUFFED_SENT_MINLEN = 6        # only sentences at least this long can count as "stuffed"
STUFFED_SENT_FRACTION = 0.60   # a sentence with >= this fraction proper nouns is flagged as stuffed


# ---------------------------------------------------------------------------------------------
# BANNED cliche list — REUSED from scripts/validate_episode.py (single source of truth), then
# EXTENDED (never weakened) with additional well-known LLM/AI-narration tells. If the source
# module cannot be imported, fall back to a copy IDENTICAL to validate_episode.BANNED so the two
# gates can never silently diverge.
# ---------------------------------------------------------------------------------------------

_VALIDATE_EPISODE_BANNED_FALLBACK = [
    "but here's the thing", "what happened next changed everything", "the answer may surprise you",
    "in a world where", "little did they know", "the truth is more complicated",
    "at the end of the day", "needless to say",
]

# Additional canned AI-narration crutches this gate adds on top of the shared list. Kept lowercase
# for case-insensitive substring matching (same style as validate_episode's vo.lower().count()).
_EXTRA_BANNED = [
    "little did he know", "little did she know",
    "you won't believe", "you wouldn't believe",
    "what happened next", "changed everything",
    "one thing is certain", "one thing was certain",
    "only time will tell",
    "buckle up", "let that sink in",
    "when it comes to", "it goes without saying",
    "the rest is history", "stood the test of time",
    "in today's world", "now more than ever",
    "a tale as old as time", "a testament to",
    "leaves us with more questions than answers",
    "the story doesn't end there", "but that's not all",
]


def _load_shared_banned() -> tuple[list[str], str]:
    """Return (banned_list, source_note). Import validate_episode.BANNED as the canonical base and
    extend it; fall back to an identical inline copy if that module cannot be loaded. Never raises."""
    base: list[str]
    source: str
    ve_path = ROOT / "scripts" / "validate_episode.py"
    try:
        spec = importlib.util.spec_from_file_location("pd_validate_episode", ve_path)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # module-level defines only; main() is __main__-guarded
            candidate = getattr(mod, "BANNED", None)
            if isinstance(candidate, (list, tuple)) and candidate:
                base = [str(x).lower() for x in candidate]
                source = "validate_episode.BANNED"
            else:
                base, source = list(_VALIDATE_EPISODE_BANNED_FALLBACK), "fallback(no BANNED attr)"
        else:
            base, source = list(_VALIDATE_EPISODE_BANNED_FALLBACK), "fallback(no spec)"
    except Exception as exc:  # noqa: BLE001 - importing must never break the gate
        base = list(_VALIDATE_EPISODE_BANNED_FALLBACK)
        source = f"fallback({type(exc).__name__})"
    # extend without duplicates, preserving order (base first)
    seen = set(base)
    merged = list(base)
    for phrase in _EXTRA_BANNED:
        p = phrase.lower()
        if p not in seen:
            merged.append(p)
            seen.add(p)
    return merged, source


BANNED, _BANNED_SOURCE = _load_shared_banned()


# ---------------------------------------------------------------------------------------------
# narration text extraction
# ---------------------------------------------------------------------------------------------

def _strip_markers(text: str) -> str:
    """Remove [CLM-####] claim markers and collapse whitespace (spoken words only)."""
    text = re.sub(r"\[CLM-\d{4}\]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _annotated_candidates(ep_dir: Path) -> list[Path]:
    """Annotated script jsons for this episode, newest revision last, incl. the _planning bay."""
    cands = sorted((ep_dir / "03_script").glob("script.annotated.v*.json"))
    if cands:
        return cands
    slug_tail = re.sub(r"^PD-\d{4}-\d{3}-", "", ep_dir.name)
    planning = ep_dir.parent / "_planning"
    if planning.is_dir():
        cands = sorted(planning.glob(f"*{slug_tail}*script.annotated.v*.json"))
    return cands


def _md_candidates(ep_dir: Path) -> list[Path]:
    return sorted((ep_dir / "03_script").glob("script.en.v*.md"))


def extract_narration(ep_dir: Path) -> tuple[str, str]:
    """Return (spoken_text, source_label). Prefers the newest annotated script's span text (clean
    narration, no production notes); falls back to the `[VO:]` lines of the newest script.en.*.md.
    Returns ("", "") when no script text exists in the repo (e.g. artifacts live on the SSD)."""
    for p in reversed(_annotated_candidates(ep_dir)):
        try:
            data = json.loads(p.read_text("utf-8"))
        except Exception:  # noqa: BLE001 - unreadable annotated -> try next / fall through
            continue
        spans = data.get("spans")
        if isinstance(spans, list) and spans:
            text = " ".join(str(sp.get("text", "")) for sp in spans if sp.get("text"))
            text = _strip_markers(text)
            if text:
                return text, f"annotated:{p.name}"
    for p in reversed(_md_candidates(ep_dir)):
        try:
            md = p.read_text("utf-8")
        except Exception:  # noqa: BLE001
            continue
        vo = " ".join(re.findall(r"^\[VO:\]\s*(.+)$", md, flags=re.M))
        vo = _strip_markers(vo)
        if vo:
            return vo, f"script.en:{p.name}"
    return "", ""


# ---------------------------------------------------------------------------------------------
# text metrics (sentence split + tokenizing mirror scripts/validate_episode.py)
# ---------------------------------------------------------------------------------------------

_WORD_RE = re.compile(r"[A-Za-z']+")


def split_sentences(vo: str) -> list[str]:
    """Sentence split identical to validate_episode: break after . ! ? followed by whitespace."""
    return [s for s in re.split(r"(?<=[.!?])\s+", vo) if s.strip()]


def _words(s: str) -> list[str]:
    return _WORD_RE.findall(s)


# Lowercase words that live INSIDE a proper name rather than separating two of them, so that
# "the Circuit Court of Kanawha County" is counted as one court and not as two entities.
_NAME_JOINERS = {"of", "de", "la", "van", "von"}
# Words that open a sentence without naming anyone. Capitalisation here is grammar, not a
# name, and counting them inflated every sentence by one entity.
_SENTENCE_OPENERS = {
    "the", "a", "an", "in", "on", "at", "by", "for", "from", "when", "while", "after",
    "before", "but", "and", "that", "this", "these", "those", "it", "he", "she", "they",
    "there", "then", "no", "none", "both", "each", "every", "if", "as", "so", "yet",
    "her", "his", "their", "its", "what", "which", "who", "nothing", "neither", "not",
}


def _distinct_entities(sentence: str) -> int:
    """How many different named parties this sentence introduces.

    A run of capitalised tokens (optionally bridged by a joiner such as "of") is one entity.
    "Brown sued Marmet Health Care Center." names two: a person and a company. Name-dump prose is
    not defined by how many capitals a sentence contains but by how many DIFFERENT parties it asks
    the listener to hold at once -- a distinction the token ratio alone cannot make, which is why
    it flagged three correctly-terse sentences in EP65.
    """
    ents: list[str] = []
    # Punctuation is what separates one name from the next. Scanning a punctuation-stripped token
    # list merged "Brown, Taylor, Marchio, Marmet and Genesis" into a single run and reported one
    # entity, so the real name dump passed the check.
    for clause in re.split(r"[,;:.()\u2014\u2013]|\band\b|\bor\b", sentence):
        toks = re.findall(r"[A-Za-z][A-Za-z'\-]*", clause)
        cur: list[str] = []
        for i, t in enumerate(toks):
            lead = (i == 0)
            if t[0].isupper() and not (lead and t.lower() in _SENTENCE_OPENERS):
                cur.append(t)
            elif cur and t.lower() in _NAME_JOINERS:
                cur.append(t)          # "Circuit Court of Kanawha County" stays one court
            else:
                if cur:
                    ents.append(" ".join(cur))
                    cur = []
        if cur:
            ents.append(" ".join(cur))
    # "The Supreme Court" and "Supreme Court" are the same body to a listener.
    cleaned = {re.sub(r"^the\s+", "", e.lower()).strip() for e in ents}
    return len({c for c in cleaned if c})


def _proper_noun_tokens(sentence: str) -> tuple[int, int]:
    """(proper_noun_count, total_alpha_tokens) for one sentence. A proper noun is a capitalized
    alphabetic token that is NOT the sentence's first token and is not the pronoun 'I' — a cheap,
    dependency-free heuristic (cv2/scipy/nltk are unavailable in this environment)."""
    toks = re.findall(r"[A-Za-z][A-Za-z'\-]*", sentence)
    pn = 0
    for i, t in enumerate(toks):
        if i > 0 and t[0].isupper() and t != "I":
            pn += 1
    return pn, len(toks)


def find_banned(vo: str) -> list[dict[str, Any]]:
    """Every banned phrase present, with the offending sentence for evidence (case-insensitive)."""
    low = vo.lower()
    sents = split_sentences(vo)
    hits: list[dict[str, Any]] = []
    for phrase in BANNED:
        if phrase in low:
            example = next((s.strip() for s in sents if phrase in s.lower()), "")
            hits.append({"phrase": phrase, "count": low.count(phrase), "example": example[:200]})
    return hits


# ---------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ---------------------------------------------------------------------------------------------

def evaluate(ep_dir: Path) -> dict[str, Any]:
    """Lint the approved narration text for AI-smell (banned cliches), robotic cadence, and
    proper-noun stuffing. Returns a check_final_acceptance-compatible dict; never raises, never
    exits. Skips honestly (ok=True, hard=False, skipped=True) when no script text is in the repo.

    Result keys: check, ok, hard, reason [, skipped], plus numbers: source, n_sentences,
    n_words, cadence_cv, mean_sentence_len, proper_noun_ratio, banned_hits, stuffed_sentences,
    problems.
    """
    ep_dir = Path(ep_dir)
    vo, source = extract_narration(ep_dir)
    if not vo:
        return {"check": "script_lint", "ok": True, "hard": False, "skipped": True,
                "reason": f"no annotated/script.en narration text found under {ep_dir} "
                          f"(script artifact absent — skipped honestly)"}

    sents = split_sentences(vo)
    lens = [len(_words(s)) for s in sents]
    lens = [n for n in lens if n > 0]
    n_words = sum(lens)
    n_sent = len(lens)

    problems: list[str] = []

    # 1. banned cliches (hard AI-smell) --------------------------------------------------------
    banned_hits = find_banned(vo)
    if banned_hits:
        shown = ", ".join(f"{h['phrase']!r}x{h['count']}" for h in banned_hits[:6])
        problems.append(f"{len(banned_hits)} banned cliche(s): {shown}")

    # 2. robotic cadence -----------------------------------------------------------------------
    cadence_cv: Optional[float] = None
    if n_sent >= MIN_SENTENCES_FOR_CADENCE:
        m = mean(lens)
        cadence_cv = (pstdev(lens) / m) if m > 0 else 0.0
        if cadence_cv < MIN_CADENCE_CV:
            problems.append(f"robotic cadence: sentence-length CV {cadence_cv:.3f} "
                            f"< {MIN_CADENCE_CV:.2f} (monotone; vary sentence length)")
    cadence_note = ("insufficient sentences for cadence" if cadence_cv is None else "")

    # 3. proper-noun stuffing ------------------------------------------------------------------
    total_pn = 0
    total_tok = 0
    stuffed: list[dict[str, Any]] = []
    for s in sents:
        pn, tok = _proper_noun_tokens(s)
        total_pn += pn
        total_tok += tok
        # A high ratio alone flags sentences whose names ARE the content: "Brown sued Marmet
        # Health Care Center" cannot be written with fewer proper nouns. Name-dump prose is a
        # sentence that makes the listener hold three or more different parties at once.
        if (tok >= STUFFED_SENT_MINLEN and pn / tok >= STUFFED_SENT_FRACTION
                and _distinct_entities(s) >= 3):
            stuffed.append({"pn": pn, "tok": tok, "ents": _distinct_entities(s),
                            "sentence": s.strip()[:200]})
    proper_noun_ratio = (total_pn / total_tok) if total_tok else 0.0
    if proper_noun_ratio > MAX_PROPER_NOUN_RATIO:
        problems.append(f"proper-noun stuffing: density {proper_noun_ratio:.3f} "
                        f"> {MAX_PROPER_NOUN_RATIO:.2f} ({total_pn}/{total_tok} tokens)")
    elif len(stuffed) >= 3:
        problems.append(f"proper-noun stuffing: {len(stuffed)} sentence(s) are >= "
                        f"{STUFFED_SENT_FRACTION*100:.0f}% proper nouns (name-dump prose)")

    ok = not problems
    return {
        "check": "script_lint",
        "ok": ok,
        "hard": True,
        "reason": ("narration reads clean: no banned cliches, varied cadence, natural noun density"
                   if ok else "; ".join(problems)),
        "source": source,
        "banned_source": _BANNED_SOURCE,
        "n_sentences": n_sent,
        "n_words": n_words,
        "mean_sentence_len": round(mean(lens), 2) if lens else 0.0,
        "cadence_cv": round(cadence_cv, 3) if cadence_cv is not None else None,
        "cadence_note": cadence_note,
        "proper_noun_ratio": round(proper_noun_ratio, 3),
        "banned_hits": banned_hits,
        "stuffed_sentences": stuffed[:5],
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
    print("SCRIPT LINT REPORT  (AI-smell / cadence)")
    print("=" * 78)
    print(f"  source          : {r['source']}")
    print(f"  banned list     : {r['banned_source']} ({len(BANNED)} phrases)")
    print(f"  sentences/words : {r['n_sentences']} sentences, {r['n_words']} words")
    cv = r["cadence_cv"]
    cv_s = f"{cv:.3f}" if cv is not None else f"n/a ({r['cadence_note']})"
    print(f"  cadence CV      : {cv_s}   (floor {MIN_CADENCE_CV:.2f}; higher = more human variety)")
    print(f"  mean sent length: {r['mean_sentence_len']} words")
    print(f"  proper-noun dens: {r['proper_noun_ratio']:.3f}   (ceiling {MAX_PROPER_NOUN_RATIO:.2f})")
    if r["banned_hits"]:
        print("\n  banned cliches found:")
        for h in r["banned_hits"][:10]:
            print(f"    - {h['phrase']!r} x{h['count']}   e.g. {h['example']!r}")
    if r["stuffed_sentences"]:
        print("\n  proper-noun-heavy sentences:")
        for s in r["stuffed_sentences"]:
            print(f"    - {s['pn']}/{s['tok']} proper: {s['sentence']!r}")
    print("\n" + "-" * 78)
    if r["ok"]:
        print("  RESULT: PASS  — no banned cliches, varied cadence, natural noun density")
    else:
        print("  RESULT: FAIL")
        for p in r["problems"]:
            print(f"    - {p}")
    print("-" * 78)


def _atomic_write_json(path: Path, obj: dict[str, Any]) -> None:
    """Atomic JSON write: tmp file in the same dir then os.replace (rule 14)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _evaluate_spans(spans: list[dict[str, Any]]) -> dict[str, Any]:
    """Write the given annotated spans into a throwaway episode dir and evaluate() it."""
    with tempfile.TemporaryDirectory() as td:
        ep = Path(td) / "PD-2026-999-fixture"
        (ep / "03_script").mkdir(parents=True)
        (ep / "03_script" / "script.annotated.v001.json").write_text(
            json.dumps({"spans": spans}), encoding="utf-8")
        return evaluate(ep)


# --- selftest fixtures ---------------------------------------------------------------------------
# GREEN: first-class human prose — hard-varied sentence length, no cliches, near-zero proper nouns.
# Must PASS. This is the "good case that still passes" the fix must not break.
_GREEN_TEXT = (
    "The old car sat there. "
    "Nobody in the small apartment expected it, and for a long moment the whole family simply "
    "stood frozen in the narrow hallway while the officers filled the doorway. "
    "They asked to search the car. "
    "He said no. "
    "What followed would climb, slowly and expensively, through three separate courtrooms over "
    "the better part of a decade before anyone could say who had actually been right. "
    "The question was simple. "
    "Could they open the trunk without a warrant, on the strength of a hunch and a nervous "
    "glance, or did the paper still matter at all? "
    "It mattered. "
    "A judge, reading the old words again, decided that the smell of a thing is not the same as "
    "solid proof of it. "
    "The ruling was quiet. "
    "But it traveled. "
    "Years later, in towns that had never once heard of that first tired defendant, lawyers still "
    "pointed back to the afternoon when one ordinary man simply refused.")

# RED A — BANNED-CLICHE ONLY: the GREEN prose (varied cadence, ~no proper nouns) with ONE canned
# cliche spliced in. Only the banned-cliche detector may fire.
_RED_BANNED_TEXT = _GREEN_TEXT + " The answer may surprise you."

# RED B — CADENCE ONLY: no cliche, ~no proper nouns, but the sentence lengths hug a narrow band so
# the CV collapses into the MODERATE (not egregious) zone — CV ~0.40, which PASSED the old 0.35
# floor and now FAILS the tightened 0.45 floor. Only 8 sentences (< 12) so it ALSO proves the
# cadence check now runs on short scripts instead of silently skipping.
_RED_CADENCE_TEXT = (
    "The old car sat there. "                                                    # 5
    "The officer walked over to the window and asked the driver a simple question. "  # 14
    "The tired driver did not say much. "                                        # 7
    "He looked straight ahead and kept both of his hands on the wheel. "          # 13
    "The night was very cold. "                                                  # 5
    "The officer asked again if he could take a quick look inside the small trunk. "  # 15
    "The driver shook his head once more. "                                      # 7
    "The two of them stood there in the cold for a long silent moment.")          # 14

# RED C — PROPER-NOUN ONLY: hard-varied cadence (so the CV check PASSES), no cliche, but the prose
# is packed with capitalized names at a MODERATE density (~0.13) that PASSED the old 0.22 ceiling
# and now FAILS the tightened 0.10 ceiling. Only the proper-noun detector may fire.
_RED_PROPER_TEXT = (
    "Whitfield knew. "
    "The lawyer for the defense, a careful man named Robert Callahan, spent the entire afternoon "
    "arguing with the junior prosecutor about a single word. "
    "Nobody believed him. "
    "The next morning Callahan drove out to Danville to meet Sheriff Grant. "
    "They talked for hours about the arrest, the traffic stop on Route Nine, and the long quiet "
    "feud between the Harmon family and the whole county. "
    "Grant simply shrugged.")


def _selftest() -> int:
    """RED-FIXTURE probe (the reviewer's gaming probe, made explicit) + real-episode numbers.

    Each AI-smell detector gets its OWN red fixture so a single-detector regression is visible: if
    a future edit accidentally disables (or re-loosens) just the cadence check, RED B alone flips to
    PASS and the selftest fails, pointing straight at the broken detector. A GREEN fixture guards the
    other direction (the tightened thresholds must not false-flag first-class human prose)."""
    print("=" * 78)
    print("SELFTEST 1/2 — GREEN good case (must PASS) + 3 per-detector RED fixtures (each must FAIL)")
    print("=" * 78)

    green = _evaluate_spans([{"span_id": "SPN-0001", "text": _GREEN_TEXT}])
    green_ok = green["ok"] is True
    print(f"  GREEN  ok={green['ok']}  cv={green.get('cadence_cv')}  "
          f"pn={green.get('proper_noun_ratio')}  banned={len(green.get('banned_hits', []))}  "
          f"n_sent={green.get('n_sentences')}  -> {'PASS' if green_ok else 'FAIL'} (want PASS)")

    cases = [
        ("RED A banned-cliche", _RED_BANNED_TEXT, "banned"),
        ("RED B cadence-CV    ", _RED_CADENCE_TEXT, "cadence"),
        ("RED C proper-noun   ", _RED_PROPER_TEXT, "proper"),
    ]
    all_reds_fail = True
    detector_isolated = True
    for label, text, detector in cases:
        r = _evaluate_spans([{"span_id": "SPN-0001", "text": text}])
        failed = r["ok"] is False
        all_reds_fail = all_reds_fail and failed
        probs = r.get("problems", [])
        # isolation: exactly the intended detector should have fired (single-detector visibility)
        fired = {
            "banned": any("banned cliche" in p for p in probs),
            "cadence": any("robotic cadence" in p for p in probs),
            "proper": any("proper-noun" in p for p in probs),
        }
        isolated = fired.get(detector, False) and sum(1 for v in fired.values() if v) == 1
        detector_isolated = detector_isolated and isolated
        print(f"  {label}  ok={r['ok']}  cv={r.get('cadence_cv')}  pn={r.get('proper_noun_ratio')}  "
              f"banned={len(r.get('banned_hits', []))}  n_sent={r.get('n_sentences')}  "
              f"-> {'FAIL(good)' if failed else 'PASS(BAD)'}"
              f"{'' if isolated else '  [WARN: not isolated to one detector]'}")
        for p in probs:
            print(f"        · {p}")

    red_ok = green_ok and all_reds_fail and detector_isolated
    print(f"\nRED-FIXTURE: {'PASS' if red_ok else 'FAIL'}  "
          f"(green passes={green_ok}; all 3 reds fail={all_reds_fail}; "
          f"each isolated to its detector={detector_isolated})")

    print("\n" + "=" * 78)
    print(f"SELFTEST 2/2 — REAL EPISODE {DEFAULT_EP} (actual measured numbers)")
    print("=" * 78)
    real = evaluate(ROOT / "episodes" / DEFAULT_EP)
    _print_report(real)
    return 0 if red_ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(
        description="AI-smell / cadence linter on the narration text: FAIL on banned cliches, "
                    "robotic cadence, or proper-noun stuffing.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--dry-run", action="store_true",
                    help="resolve inputs and print the report, but always exit 0 and write no json")
    ap.add_argument("--json", default=None, help="also write the result dict to this path (atomic)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixture then the real episode and print numbers")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    r = evaluate(ep_dir)
    _print_report(r)

    if args.json and not args.dry_run:
        _atomic_write_json(Path(args.json), r)
        print(f"\nwrote {args.json}")

    if args.dry_run:
        return 0
    if r.get("skipped"):
        return 0  # honest skip is not a failure
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
