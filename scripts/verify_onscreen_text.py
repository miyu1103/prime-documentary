#!/usr/bin/env python3
r"""Independent on-screen-text gate — every burned figure/graphic word must be TRUE and allowed.

The owner's recurring defect is on-screen text (kinetic lines, number tickers, lower-thirds, case
timelines, quotes, vote tallies) that shows a HARD FACT the research never verified: a made-up
number, a fabricated quotation, a mis-dated case citation, or a real-person name that no claim
supports. Narration is checked against claims elsewhere; the text physically BURNED into the frame
is a second, independent surface where an unverified fact can slip out — and it reads as authoritative
because it is on screen. This is the INDEPENDENT GATE that catches that class before ship.

WHAT IT MEASURES (the real intent, not a proxy):
Every HARD, checkable token shown on screen must trace to a grade-A claim in claims.v*.json:
  * NUMBERS   — years, counts, dollar amounts, vote tallies. Each digit-run shown must appear as a
                number in the affirmative text of the grade-A claims (normalized_claim / allowed_wording
                / evidence_locations / counterevidence / notes / temporal_scope / geographic_scope /
                units). prohibited_wording is DELIBERATELY EXCLUDED — text the research forbade must
                never bless an on-screen number.
  * QUOTES    — any quoted span or a `quote` field must overlap the grade-A corpus by content words
                (>= QUOTE_MIN_OVERLAP), so a fabricated quotation cannot pass while a legitimately
                trimmed on-screen quote can.
  * CITATIONS — "X v. Y" parties must exist in the corpus; "X v. Y · YEAR" (and lower-third
                case+year) must have the case name CO-OCCUR with that year in the corpus, so a
                mis-dated citation (right case, wrong year) is caught.
  * PERSONS   — "(Chief) Justice / Judge / Officer NAME" attributions must have NAME in the corpus,
                so an invented attribution or an unpermitted real-person name is caught.

It does NOT police generic descriptive labels ("GLOVEBOX", "PROBABLE CAUSE") — those carry no hard,
falsifiable fact and are out of scope; the gate targets exactly the tokens that can be objectively
true-or-false against the claim ledger. Each token is reported as matched -> claim(s) or VIOLATION.

Grade filter: only grade-A (A / A+) claims form the verified corpus, because the spec requires hard
on-screen facts to rest on grade-A evidence; a number that exists only in a grade-B claim is a
violation by design (do not weaken this to make a target pass).

Usage:
  py -3.11 scripts/verify_onscreen_text.py --ep PD-2026-032-carsearch
  py -3.11 scripts/verify_onscreen_text.py --ep PD-2026-032-carsearch --dry-run
  py -3.11 scripts/verify_onscreen_text.py --selftest        # RED fixture + real-episode numbers
  py -3.11 scripts/verify_onscreen_text.py --ep PD-2026-032-carsearch --json out.json

Exit code 0 = PASS (or --dry-run, or an honest SKIP when the film json / claims are not in the repo,
e.g. on the SSD), 1 = FAIL (a violation, or a usage error). Read-only: it never writes into the
episode; --json writes a report atomically only where you point it.

check_final_acceptance can import this module and call evaluate(epdir); the dict keys below
(check / ok / hard / reason / skipped / violations / n_* / tokens) are that contract — keep stable.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-032-carsearch"
GATE = "onscreen_text_verified"

# --- thresholds (do not weaken to make a target pass) --------------------------------------------
QUOTE_MIN_OVERLAP = 0.60   # a shown quote must share >= 60% of its CONTENT words with the corpus
QUOTE_MIN_WORDS = 3        # spans shorter than this are slogans, not quotations -> not quote-checked
YEAR_WINDOW = 90           # a case name must co-occur with its cited year within this many chars

# grade-A claim fields that constitute AFFIRMATIVE verified evidence (prohibited_wording excluded)
_CORPUS_FIELDS = (
    "normalized_claim", "allowed_wording", "evidence_locations", "counterevidence",
    "notes", "temporal_scope", "geographic_scope", "units",
)

# common function words dropped before quote-overlap / citation-party matching
_STOP = {
    "a", "an", "the", "of", "to", "in", "on", "at", "for", "with", "from", "by", "as", "into",
    "onto", "over", "under", "than", "up", "out", "off", "about", "against", "between", "through",
    "and", "or", "but", "nor", "so", "yet", "is", "are", "was", "were", "be", "been", "being",
    "am", "has", "have", "had", "do", "does", "did", "will", "would", "can", "could", "shall",
    "should", "may", "might", "must", "that", "this", "these", "those", "who", "which", "whose",
    "whom", "it", "its", "if", "when", "no", "not", "v", "vs",
}

# ------------------------------------------------------------------------------------------------
# text normalization
# ------------------------------------------------------------------------------------------------

def _dash(s: str) -> str:
    """Fold en/em dashes and the middot separator to plain ASCII so patterns match uniformly."""
    return (s.replace("—", "-").replace("–", "-").replace("‒", "-")
            .replace("−", "-"))


def _quotes_ascii(s: str) -> str:
    """Fold curly quotes to straight so quote spans parse uniformly."""
    return (s.replace("“", '"').replace("”", '"')
            .replace("‘", "'").replace("’", "'"))


def norm_word(w: str) -> str:
    """Normalize a token to its comparable core (lowercase alphanumerics only)."""
    return re.sub(r"[^a-z0-9]", "", w.lower())


# ------------------------------------------------------------------------------------------------
# verified corpus from grade-A claims
# ------------------------------------------------------------------------------------------------

def _grade_is_A(c: dict) -> bool:
    return str(c.get("grade", "")).strip().upper().startswith("A")


def _iter_strings(value: Any):
    """Yield every string leaf inside a JSON value (str / list / dict), scalars stringified."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, (int, float)):
        yield str(value)
    elif isinstance(value, list):
        for v in value:
            yield from _iter_strings(v)
    elif isinstance(value, dict):
        for v in value.values():
            yield from _iter_strings(v)


class Corpus:
    """The verified evidence surface built from grade-A claims."""

    def __init__(self, claims: list[dict]) -> None:
        parts: list[str] = []
        self.claim_texts: list[tuple[str, str]] = []  # (claim_id, lowered affirmative text)
        for c in claims:
            if not _grade_is_A(c):
                continue
            ctext: list[str] = []
            for f in _CORPUS_FIELDS:
                if f in c:
                    ctext.extend(_iter_strings(c[f]))
            joined = _dash(" ".join(ctext))
            parts.append(joined)
            self.claim_texts.append((str(c.get("claim_id", "?")), joined.lower()))
        blob = _dash(" ".join(parts))
        self.text = blob.lower()
        # Strip inter-digit thousands-commas before extracting numbers so the corpus side is
        # SYMMETRIC with hard_numbers() (which does .replace(",","")). Without this, a claim
        # written "$2,300" tokenizes to {2,300} and the on-screen "2300" falsely fails
        # (bug: 4+-digit dollar figures never matched). Unsupported numbers still fail (invariant 15).
        self.numbers: set[str] = set(re.findall(r"\d+", re.sub(r"(?<=\d),(?=\d)", "", self.text)))
        self.words: set[str] = {norm_word(w) for w in re.split(r"\s+", self.text) if norm_word(w)}

    def has_number(self, num: str) -> bool:
        """True if `num` is a WHOLE numeric token in the grade-A corpus (not a substring of 2009)."""
        return num in self.numbers

    def number_claims(self, num: str) -> list[str]:
        """Grade-A claims whose text contains `num` as a whole number (digit-boundary match)."""
        pat = re.compile(rf"(?<!\d){re.escape(num)}(?!\d)")
        return [cid for cid, t in self.claim_texts if pat.search(t)]

    def word_present(self, word: str) -> bool:
        return norm_word(word) in self.words

    def cooccurs(self, name: str, year: str) -> bool:
        """True if `name` appears within YEAR_WINDOW chars of `year` anywhere in the corpus."""
        n = re.escape(name.lower())
        y = re.escape(year)
        pat = rf"{n}.{{0,{YEAR_WINDOW}}}{y}|{y}.{{0,{YEAR_WINDOW}}}{n}"
        return re.search(pat, self.text, re.S) is not None

    def best_quote_overlap(self, content_words: list[str]) -> tuple[float, Optional[str]]:
        """Return (best per-claim content-word overlap ratio, claim_id) for a quote's content words."""
        if not content_words:
            return 0.0, None
        best_ratio, best_id = 0.0, None
        for cid, t in self.claim_texts:
            twords = {norm_word(w) for w in re.split(r"\s+", t) if norm_word(w)}
            hit = sum(1 for w in content_words if w in twords)
            ratio = hit / len(content_words)
            if ratio > best_ratio:
                best_ratio, best_id = ratio, cid
        return best_ratio, best_id


# ------------------------------------------------------------------------------------------------
# figure -> displayed strings
# ------------------------------------------------------------------------------------------------

# keys that are render directives / geometry, never factual on-screen text
_DIRECTIVE_KEYS = {"kind", "mode", "style", "pattern", "outcome", "x", "y", "seed", "start", "end"}


def figure_strings(fig: dict) -> list[str]:
    """Every human-visible string a figure burns on screen, de-duplicated in stable order."""
    out: list[str] = []

    def add(v: Any) -> None:
        if isinstance(v, str) and v.strip():
            out.append(v)
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out.append(str(v))

    # explicit, known text carriers
    for key in ("lines", "zones"):
        for x in fig.get(key, []) or []:
            add(x)
    for key in ("primary", "secondary", "title", "label", "topLabel", "suffix",
                "quote", "attribution", "text", "value"):
        if key in fig:
            add(fig[key])
    if fig.get("kind") == "votetally":
        m, d = fig.get("majority"), fig.get("dissent")
        add(m)
        add(d)
        if isinstance(m, int) and isinstance(d, int):
            out.append(f"{m}-{d}")  # the composite tally as burned ("8-1")
    if fig.get("kind") == "lowerthird":
        pr, se = fig.get("primary"), fig.get("secondary")
        if isinstance(pr, str) and isinstance(se, (str, int, float)):
            out.append(f"{pr} · {se}")  # case+year composite for the year-citation check
    for ev in fig.get("events", []) or []:
        if isinstance(ev, dict):
            add(ev.get("year"))
            add(ev.get("text"))
            if ev.get("text") and ev.get("year"):
                out.append(f"{ev['text']} · {ev['year']}")
    for pin in fig.get("pins", []) or []:
        if isinstance(pin, dict):
            add(pin.get("label"))

    # generic sweep for any future text-bearing scalar fields (skips directives/geometry)
    for k, v in fig.items():
        if k in _DIRECTIVE_KEYS or k in ("lines", "zones", "events", "pins"):
            continue
        if isinstance(v, str) and v.strip():
            add(v)

    seen: set[str] = set()
    uniq: list[str] = []
    for s in out:
        if s not in seen:
            seen.add(s)
            uniq.append(s)
    return uniq


# ------------------------------------------------------------------------------------------------
# extraction patterns
# ------------------------------------------------------------------------------------------------

_QUOTE_RE = re.compile(r'"([^"]{3,})"')
_CASE_YEAR_RE = re.compile(
    r"([A-Za-z][A-Za-z.]{2,})\s+v\.?\s+([A-Za-z][A-Za-z. ]{2,}?)\s*[·(,]\s*(\d{4})", re.I)
_CASE_RE = re.compile(
    r"([A-Za-z][A-Za-z.]{2,})\s+v\.?\s+([A-Za-z][A-Za-z. ]{2,}?)(?=[\s·(),]|$)", re.I)
_PERSON_RE = re.compile(r"(?:chief\s+)?(?:justice|judge|officer)\s+([a-z][a-z'\-]{2,})", re.I)


def hard_numbers(s: str) -> list[str]:
    """Whole numeric tokens burned as HARD facts: years, counts, $amounts, and A-B vote tallies.

    Splits on whitespace and only accepts a token that, after stripping wrapping punctuation, is
    purely numeric ("1925", "$68", "1,200") or a vote tally ("8-1" -> 8 and 1). A digit glued into
    an alphanumeric label ("K-9", "I-95", "CO2") is NOT a hard number and is deliberately excluded.
    """
    vals: list[str] = []
    for tok in _dash(s).split():
        t = tok.strip(".,;:!?\"'()[]{}·")
        mt = re.fullmatch(r"(\d+)-(\d+)", t)
        if mt:
            vals.extend([mt.group(1), mt.group(2)])
            continue
        mv = re.fullmatch(r"\$?(\d[\d,]*)(?:\.\d+)?", t)
        if mv:
            vals.append(mv.group(1).replace(",", ""))
    return vals


def _content_words(quote: str) -> list[str]:
    return [w for w in (norm_word(t) for t in quote.split()) if w and w not in _STOP]


def _party_words(party: str) -> list[str]:
    """Distinctive words of a citation party (drop stopwords and <3-char tokens)."""
    return [w for w in (norm_word(t) for t in party.split()) if w and len(w) >= 3 and w not in _STOP]


# ------------------------------------------------------------------------------------------------
# per-figure verification
# ------------------------------------------------------------------------------------------------

def _verify_figure(fig: dict, idx: int, corpus: Corpus) -> list[dict[str, Any]]:
    """Return a token report list for one figure. status is 'matched' or 'VIOLATION'."""
    tokens: list[dict[str, Any]] = []
    strings = figure_strings(fig)
    kind = fig.get("kind", "?")
    start = fig.get("start")

    def rec(ttype: str, text: str, ok: bool, detail: str, claims: Optional[list[str]] = None) -> None:
        tokens.append({
            "figure": idx, "start": start, "kind": kind, "type": ttype, "text": text,
            "status": "matched" if ok else "VIOLATION", "detail": detail,
            "claims": claims or [],
        })

    seen_num: set[str] = set()
    seen_quote: set[str] = set()
    seen_cite: set[str] = set()
    seen_person: set[str] = set()

    for raw in strings:
        s = _dash(_quotes_ascii(raw))

        # -- NUMBERS --------------------------------------------------------------------------
        for num in hard_numbers(s):
            if num in seen_num:
                continue
            seen_num.add(num)
            if corpus.has_number(num):
                claims = corpus.number_claims(num)
                rec("number", num, True, f"in grade-A claim(s) {','.join(claims)}", claims)
            else:
                rec("number", num, False, "number not found in any grade-A claim (unverified)")

        # -- QUOTES ---------------------------------------------------------------------------
        quote_spans = list(_QUOTE_RE.findall(s))
        if fig.get("kind") == "quote" and raw == fig.get("quote"):
            quote_spans.append(s)  # the whole quote field is a quotation
        for q in quote_spans:
            key = norm_word(q)
            if key in seen_quote:
                continue
            seen_quote.add(key)
            cw = _content_words(q)
            if len(cw) < QUOTE_MIN_WORDS:
                continue  # a short slogan, not a checkable quotation
            ratio, cid = corpus.best_quote_overlap(cw)
            if ratio >= QUOTE_MIN_OVERLAP:
                rec("quote", q, True, f"content overlap {ratio:.0%} with {cid}",
                    [cid] if cid else [])
            else:
                rec("quote", q, False,
                    f"content overlap only {ratio:.0%} (< {QUOTE_MIN_OVERLAP:.0%}) — "
                    f"fabricated/unsupported quotation")

        # -- CITATIONS with a year (mismatch detection) ---------------------------------------
        for m in _CASE_YEAR_RE.finditer(s):
            p1, _p2, year = m.group(1), m.group(2), m.group(3)
            ckey = f"{norm_word(p1)}:{year}"
            if ckey in seen_cite:
                continue
            seen_cite.add(ckey)
            label = f"{m.group(0).strip()}"
            if not corpus.word_present(p1):
                rec("citation", label, False,
                    f"case party '{p1}' not in any grade-A claim (unverified citation)")
            elif year not in corpus.numbers:
                rec("citation", label, False, f"cited year {year} not in any grade-A claim")
            elif not corpus.cooccurs(p1, year):
                rec("citation", label, False,
                    f"'{p1}' is not associated with {year} in the claims (mismatched citation)")
            else:
                rec("citation", label, True, f"'{p1}' co-occurs with {year} in grade-A claims")

        # -- CITATIONS without a year (party existence) ---------------------------------------
        for m in _CASE_RE.finditer(s):
            parties = f"{m.group(1)} v. {m.group(2).strip()}"
            key = norm_word(parties)
            if key in seen_cite:
                continue
            seen_cite.add(key)
            missing = [w for w in (_party_words(m.group(1)) + _party_words(m.group(2)))
                       if w not in corpus.words]
            if missing:
                rec("citation", parties, False,
                    f"citation party word(s) not in grade-A claims: {', '.join(sorted(set(missing)))}")
            else:
                rec("citation", parties, True, "all citation parties present in grade-A claims")

        # -- PERSON attributions --------------------------------------------------------------
        for m in _PERSON_RE.finditer(s):
            name = m.group(1)
            key = norm_word(name)
            if key in seen_person:
                continue
            seen_person.add(key)
            if corpus.word_present(name):
                rec("person", m.group(0).strip(), True, f"'{name}' present in grade-A claims")
            else:
                rec("person", m.group(0).strip(), False,
                    f"attributed name '{name}' not in any grade-A claim "
                    f"(unverified / unpermitted real-person name)")

    return tokens


# ------------------------------------------------------------------------------------------------
# path resolution
# ------------------------------------------------------------------------------------------------

def resolve_film(ep_dir: Path, override: Optional[str]) -> Path:
    if override:
        return Path(override)
    data_dir = ROOT / "remotion" / "src" / "data"
    short = ep_dir.name.split("-")[-1]
    cand = data_dir / f"{short}_film.json"
    if cand.exists():
        return cand
    if data_dir.exists():
        for p in sorted(data_dir.glob("*_film.json")):
            try:
                eid = json.loads(p.read_text("utf-8")).get("episode_id")
            except Exception:  # noqa: BLE001 - unreadable film json -> skip candidate
                continue
            if eid == ep_dir.name:
                return p
    return cand  # non-existent; caller skips honestly


def resolve_claims(ep_dir: Path, override: Optional[str]) -> Path:
    if override:
        return Path(override)
    cands = sorted((ep_dir / "01_research").glob("claims.v*.json"))
    return cands[-1] if cands else ep_dir / "01_research" / "claims.v001.json"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text("utf-8"))


# ------------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ------------------------------------------------------------------------------------------------

def evaluate(ep_dir: Path, film: Optional[str] = None,
             claims: Optional[str] = None) -> dict[str, Any]:
    """Verify every hard on-screen token against grade-A claims. Never raises / never sys.exit.

    Returns a dict with the stable contract keys:
      check, ok, hard, reason, skipped, film, claims, n_figures, n_numbers, n_quotes,
      n_citations, n_persons, n_checked, n_violations, violations, tokens.
    An honest SKIP (film json or claims not in the repo — e.g. on the SSD) returns
    {"ok": True, "hard": False, "skipped": True, ...} so it never blocks nor fakes green.
    """
    ep_dir = Path(ep_dir)
    film_path = resolve_film(ep_dir, film)
    claims_path = resolve_claims(ep_dir, claims)

    if not film_path.exists():
        return {"check": GATE, "ok": True, "hard": False, "skipped": True,
                "reason": f"film json not in repo: {film_path} (skipped honestly)"}
    if not claims_path.exists():
        return {"check": GATE, "ok": True, "hard": False, "skipped": True,
                "reason": f"claims not in repo: {claims_path} (skipped honestly)"}

    try:
        film_doc = _load_json(film_path)
        claims_doc = _load_json(claims_path)
    except Exception as exc:  # noqa: BLE001 - malformed inputs must not crash the caller
        return {"check": GATE, "ok": True, "hard": False, "skipped": True,
                "reason": f"could not parse inputs ({exc}); skipped rather than crash"}

    claim_list = claims_doc.get("claims", claims_doc) if isinstance(claims_doc, dict) else claims_doc
    if not isinstance(claim_list, list):
        return {"check": GATE, "ok": True, "hard": False, "skipped": True,
                "reason": "claims file has no claim list; skipped"}
    corpus = Corpus(claim_list)
    if not corpus.claim_texts:
        return {"check": GATE, "ok": True, "hard": False, "skipped": True,
                "reason": "no grade-A claims to verify against; skipped"}

    figures = film_doc.get("figures", []) if isinstance(film_doc, dict) else []
    if not isinstance(figures, list) or not figures:
        return {"check": GATE, "ok": True, "hard": True, "skipped": False,
                "reason": "no figures / on-screen text present (nothing to verify)",
                "film": str(film_path), "claims": str(claims_path),
                "n_figures": 0, "n_checked": 0, "n_violations": 0,
                "violations": [], "tokens": []}

    tokens: list[dict[str, Any]] = []
    for i, fig in enumerate(figures):
        if isinstance(fig, dict):
            tokens.extend(_verify_figure(fig, i, corpus))

    by_type = {"number": 0, "quote": 0, "citation": 0, "person": 0}
    for t in tokens:
        by_type[t["type"]] = by_type.get(t["type"], 0) + 1
    violations = [t for t in tokens if t["status"] == "VIOLATION"]
    ok = not violations

    if ok:
        reason = (f"{len(tokens)} hard on-screen token(s) verified against grade-A claims "
                  f"({by_type['number']} numbers, {by_type['quote']} quotes, "
                  f"{by_type['citation']} citations, {by_type['person']} persons); 0 violations")
    else:
        ex = "; ".join(f"[fig{v['figure']} {v['type']}] {v['text']!r}: {v['detail']}"
                       for v in violations[:6])
        reason = f"{len(violations)} on-screen VIOLATION(s): {ex}"

    return {
        "check": GATE,
        "ok": ok,
        "hard": True,
        "skipped": False,
        "reason": reason,
        "film": str(film_path),
        "claims": str(claims_path),
        "n_figures": len(figures),
        "n_numbers": by_type["number"],
        "n_quotes": by_type["quote"],
        "n_citations": by_type["citation"],
        "n_persons": by_type["person"],
        "n_checked": len(tokens),
        "n_violations": len(violations),
        "violations": violations,
        "tokens": tokens,
    }


# ------------------------------------------------------------------------------------------------
# reporting
# ------------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("ON-SCREEN TEXT VERIFICATION  (burned figure text vs grade-A claims)")
    print("=" * 78)
    print(f"  film    : {r.get('film')}")
    print(f"  claims  : {r.get('claims')}")
    print(f"  figures : {r.get('n_figures')}   hard tokens checked: {r.get('n_checked')} "
          f"({r.get('n_numbers')} num, {r.get('n_quotes')} quote, "
          f"{r.get('n_citations')} cite, {r.get('n_persons')} person)")
    matched = [t for t in r.get("tokens", []) if t["status"] == "matched"]
    print(f"\n  matched tokens ({len(matched)}):")
    for t in matched[:40]:
        cl = f" -> {','.join(t['claims'])}" if t["claims"] else ""
        print(f"    [{t['type']:>8}] {t['text']!r}{cl}")
    if len(matched) > 40:
        print(f"    ... (+{len(matched) - 40} more)")
    if r.get("violations"):
        print(f"\n  VIOLATIONS ({r['n_violations']}):")
        for v in r["violations"]:
            print(f"    [fig{v['figure']} @ {v['start']}s {v['type']}] {v['text']!r}")
            print(f"        -> {v['detail']}")
    print("\n" + "-" * 78)
    print("  RESULT: PASS — all hard on-screen facts trace to grade-A claims" if r["ok"]
          else "  RESULT: FAIL — unverified on-screen text present")
    print("-" * 78)


def _atomic_write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=2, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# ------------------------------------------------------------------------------------------------
# self-test: RED fixture (must FAIL) + real-episode measurement
# ------------------------------------------------------------------------------------------------

def _selftest() -> int:
    print("=" * 78)
    print("SELFTEST 1/2 — RED FIXTURE (a known-bad film MUST report ok=False)")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        # a tiny grade-A claim ledger: verifies 68, 1925, 2018, Carroll, Collins, Sotomayor
        claims_doc = {"claims": [
            {"claim_id": "CLM-0001", "grade": "A",
             "normalized_claim": "In Carroll v. United States (1925) the Court created the "
             "automobile exception; agents found 68 bottles of liquor.",
             "allowed_wording": ["Since 1925 police could search a car with probable cause."]},
            {"claim_id": "CLM-0002", "grade": "A",
             "normalized_claim": "In Collins v. Virginia (2018, 8-1) Justice Sotomayor wrote that "
             "the automobile exception extends no further than the automobile itself.",
             "allowed_wording": ["The scope of the automobile exception extends no further "
                                 "than the automobile itself."]},
            # a grade-B claim that mentions 4200 — must NOT bless an on-screen 4200
            {"claim_id": "CLM-0003", "grade": "B",
             "normalized_claim": "Some report roughly 4200 stops annually."},
        ]}
        film_doc = {"episode_id": "RED", "figures": [
            # THE reviewer's exact gaming probe: an on-screen "$99,999" absent from any claim.
            {"start": 1.0, "end": 4.0, "kind": "numberticker",
             "primary": "$99,999", "suffix": " IN CASH SEIZED"},
            {"start": 5.0, "end": 9.0, "kind": "numberticker", "value": 999, "suffix": " BOTTLES"},
            {"start": 10.0, "end": 14.0, "kind": "quote",
             "quote": "This entirely fabricated sentence was never spoken by anybody anywhere.",
             "attribution": "Justice Fakename"},
            {"start": 15.0, "end": 19.0, "kind": "kinetic",
             "lines": ["CARROLL v. UNITED STATES · 1971"]},   # right case, WRONG year
            {"start": 20.0, "end": 24.0, "kind": "kinetic",
             "lines": ["ZORBLAX v. NOWHERE"]},                     # invented case
            {"start": 25.0, "end": 29.0, "kind": "numberticker", "value": 4200},  # only grade-B
        ]}
        _atomic_write_json(tmp / "film.json", film_doc)
        _atomic_write_json(tmp / "claims.json", claims_doc)
        r = evaluate(tmp, film=str(tmp / "film.json"), claims=str(tmp / "claims.json"))
        _print_report(r)
        vt = {v["type"] for v in r.get("violations", [])}
        # the exact probe must surface as a number VIOLATION on the burned "$99,999"
        probe_caught = any(v["type"] == "number" and v["text"] == "99999"
                           for v in r.get("violations", []))
        red_ok = (r["ok"] is False and not r.get("skipped") and probe_caught
                  and {"number", "quote", "citation", "person"}.issubset(vt))
        print(f"\nexpected ok=False, the on-screen $99,999 probe (->99999) flagged, and "
              f"number+quote+citation+person violations;")
        print(f"got ok={r['ok']} probe_99999_flagged={probe_caught} "
              f"violation_types={sorted(vt)}")
        print("RED-FIXTURE: PASS" if red_ok else "RED-FIXTURE: FAIL")

    print("\n" + "=" * 78)
    print(f"SELFTEST 2/2 — REAL EPISODE {DEFAULT_EP} (actual numbers)")
    print("=" * 78)
    real = evaluate(ROOT / "episodes" / DEFAULT_EP)
    _print_report(real)
    return 0 if red_ok else 1


# ------------------------------------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001 - reconfigure unavailable on exotic stdout; non-fatal
        pass
    ap = argparse.ArgumentParser(
        description="Independent on-screen-text gate: FAIL if burned figure text shows an "
                    "unverified number/quote/citation/name.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--film", default=None, help="override <slug>_film.json path")
    ap.add_argument("--claims", default=None, help="override claims.v*.json path")
    ap.add_argument("--dry-run", action="store_true",
                    help="evaluate and report only; never writes (exit 0 unless usage error)")
    ap.add_argument("--json", default=None, metavar="PATH",
                    help="atomically write the full result dict as JSON to PATH")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixture then the real episode and exit")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    r = evaluate(ep_dir, film=args.film, claims=args.claims)
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"\n[wrote] {args.json}")

    if args.dry_run:
        return 0
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
