#!/usr/bin/env python3
r"""Prove a claim ledger is TRACED, not COPIED — every grade-A claim quotes a real primary source.

WHY THIS EXISTS
---------------
`verify_onscreen_text.py` checks burned on-screen text against the grade-A claims in
`01_research/claims.v*.json`. That gate is only worth anything if the ledger itself was built by
tracing each claim to a primary source. A ledger back-filled from the episode's own script would
make the gate circular: the script would be checked against a restatement of the script, every
token would "match", and the receipt would print a green that measured nothing.

This script closes that hole mechanically. For every grade-A claim it requires at least one
`evidence_locations` entry containing a QUOTED span (in "..." or '...') that occurs VERBATIM,
after normalization, in a primary-source capture file supplied on the command line. A quote that
is not in the source cannot be waved through: the claim is reported and the run exits non-zero.

WHAT IT DOES NOT PROVE
----------------------
That the capture file is genuinely a primary source, that the quote means what the claim says it
means, or that a grade-B/C/D/E claim is true. It proves exactly one thing: the words the ledger
attributes to the source are in the source. Everything else stays a human judgement.

Normalization (must match how research captures are read, and is deliberately forgiving of OCR
whitespace, page markers and curly punctuation, and nothing else):
  curly quotes -> straight; en/em/figure dash and minus -> "-"; NBSP -> space; "&amp;" -> "&";
  reporter page markers of the `*447` family removed (including ones glued to a word or splitting
  a word across a page break); bare footnote markers of the `[8]` family removed (digits ONLY --
  a bracketed WORD is a reporter insertion such as "[t]hat" or "[the writs]" and is kept, so a
  ledger cannot delete words from a quotation by bracketing them); "§" -> "section"; everything
  that is not a letter, digit, period or space dropped; case folded; whitespace collapsed.

Usage:
  py -3.11 scripts/verify_claim_evidence.py --ep PD-2026-062-greene \
      --source episodes/_planning/measurements/EP62_greene_RAW.md
  py -3.11 scripts/verify_claim_evidence.py --ep PD-2026-062-greene --source <f> --json out.json
  py -3.11 scripts/verify_claim_evidence.py --selftest

Exit 0 = every grade-A claim traces to a supplied source. Exit 1 = at least one does not, or a
usage error. Read-only; --json writes a report only where you point it.
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
GATE = "claim_evidence_traced"

# a quoted span must carry at least this many words to count as a traceable quotation
MIN_QUOTE_WORDS = 5

# A single-quoted span must be delimited by NON-word characters. Without the lookaround, the
# apostrophe in a locator such as "O'Connor, J., dissenting" opens a bogus span that swallows the
# real double-quoted evidence and makes a perfectly traceable claim report NOT_IN_SOURCE.
_QUOTED = re.compile(r'"([^"]{12,})"' + r"|(?<![A-Za-z0-9])'([^']{12,})'(?![A-Za-z0-9])")
_PAGE_MARK = re.compile(r"\*\d{2,4}\s*")
_FOOTNOTE_MARK = re.compile(r"\[\s*\d{1,3}\s*\]")


def normalize(s: str) -> str:
    """Fold a capture or a quote to the comparable form described in the module docstring."""
    s = (s.replace("“", '"').replace("”", '"')
         .replace("‘", "'").replace("’", "'")
         .replace("—", "-").replace("–", "-").replace("‒", "-")
         .replace("−", "-").replace(" ", " ").replace("`", "'"))
    s = s.replace("&amp;", "&")
    s = s.replace("§", " section ")
    s = _PAGE_MARK.sub(" ", s)
    s = _FOOTNOTE_MARK.sub(" ", s)
    s = re.sub(r"[^A-Za-z0-9. ]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def quoted_spans(text: str) -> list[str]:
    """Every quoted span in an evidence_locations entry, in order."""
    out: list[str] = []
    for m in _QUOTED.finditer(text):
        out.append(m.group(1) if m.group(1) is not None else m.group(2))
    return out


def _grade_is_A(c: dict) -> bool:
    return str(c.get("grade", "")).strip().upper().startswith("A")


def evaluate(claims_path: Path, source_paths: list[Path]) -> dict[str, Any]:
    """Verify every grade-A claim quotes at least one supplied source. Never raises."""
    if not claims_path.exists():
        return {"check": GATE, "ok": False, "reason": f"claims file not found: {claims_path}"}
    missing_src = [str(p) for p in source_paths if not p.exists()]
    if missing_src:
        return {"check": GATE, "ok": False,
                "reason": f"source capture(s) not found: {', '.join(missing_src)}"}
    if not source_paths:
        return {"check": GATE, "ok": False, "reason": "no --source given; nothing to trace against"}

    try:
        doc = json.loads(claims_path.read_text("utf-8"))
    except Exception as exc:  # noqa: BLE001 - a malformed ledger is a failure, not a crash
        return {"check": GATE, "ok": False, "reason": f"could not parse claims ({exc})"}

    claims = doc.get("claims", doc) if isinstance(doc, dict) else doc
    if not isinstance(claims, list):
        return {"check": GATE, "ok": False, "reason": "claims file has no claim list"}

    corpora = {str(p): normalize(p.read_text("utf-8", errors="replace")) for p in source_paths}

    rows: list[dict[str, Any]] = []
    for c in claims:
        if not isinstance(c, dict) or not _grade_is_A(c):
            continue
        cid = str(c.get("claim_id", "?"))
        spans: list[str] = []
        for loc in c.get("evidence_locations", []) or []:
            if isinstance(loc, str):
                spans.extend(quoted_spans(loc))
        checked = [s for s in spans if len(s.split()) >= MIN_QUOTE_WORDS]
        if not checked:
            rows.append({"claim_id": cid, "status": "NO_QUOTE", "n_spans": len(spans),
                         "detail": f"grade-A claim has no quoted span of >= {MIN_QUOTE_WORDS} "
                                   f"words in evidence_locations (cannot be traced)"})
            continue
        hit_src, hit_span = None, None
        for span in checked:
            n = normalize(span)
            for name, blob in corpora.items():
                if n and n in blob:
                    hit_src, hit_span = name, span
                    break
            if hit_src:
                break
        if hit_src:
            rows.append({"claim_id": cid, "status": "traced", "source": hit_src,
                         "span_words": len(hit_span.split()),
                         "detail": f"quoted span verbatim in {Path(hit_src).name}"})
        else:
            rows.append({"claim_id": cid, "status": "NOT_IN_SOURCE",
                         "n_spans": len(checked),
                         "detail": "no quoted span occurs verbatim in any supplied source "
                                   "(claim is asserted, not traced)"})

    bad = [r for r in rows if r["status"] != "traced"]
    ok = not bad and bool(rows)
    if not rows:
        reason = "no grade-A claims in the ledger (nothing to trace)"
    elif ok:
        reason = f"{len(rows)} grade-A claim(s) each quote a supplied primary source verbatim"
    else:
        ex = "; ".join(f"{r['claim_id']}: {r['status']}" for r in bad[:8])
        reason = f"{len(bad)} of {len(rows)} grade-A claim(s) not traced: {ex}"

    return {"check": GATE, "ok": ok, "reason": reason, "claims": str(claims_path),
            "sources": [str(p) for p in source_paths], "n_grade_a": len(rows),
            "n_traced": len(rows) - len(bad), "n_untraced": len(bad), "rows": rows}


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


def _print_report(r: dict[str, Any]) -> None:
    print("\n" + "=" * 78)
    print("CLAIM EVIDENCE TRACING  (grade-A claims vs primary-source captures)")
    print("=" * 78)
    print(f"  claims : {r.get('claims')}")
    for s in r.get("sources", []):
        print(f"  source : {s}")
    print(f"  grade-A: {r.get('n_grade_a')}   traced: {r.get('n_traced')}   "
          f"untraced: {r.get('n_untraced')}")
    for row in r.get("rows", []):
        if row["status"] != "traced":
            print(f"    [{row['claim_id']}] {row['status']} -> {row['detail']}")
    print("-" * 78)
    print("  RESULT: PASS — " + str(r.get("reason")) if r.get("ok")
          else "  RESULT: FAIL — " + str(r.get("reason")))
    print("-" * 78)


def _selftest() -> int:
    """A ledger whose quote is NOT in the source must FAIL; the same ledger fixed must PASS."""
    print("=" * 78)
    print("SELFTEST — an untraceable grade-A claim MUST fail")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        (tmp / "src.md").write_text(
            "The fundamental requisite of due process of law is the opportunity to be heard. "
            "In a “good percentage” of cases, [8] posting follows forthwith. "
            "The tenant’s door was the last resort in every one of these three cases.",
            encoding="utf-8")
        bad = {"claims": [
            {"claim_id": "CLM-0001", "grade": "A", "normalized_claim": "traceable",
             "evidence_locations": ['opinion II-A | "requisite of due process of law is the '
                                    'opportunity to be heard"']},
            {"claim_id": "CLM-0002", "grade": "A", "normalized_claim": "invented",
             "evidence_locations": ['opinion II-A | "this sentence was never in any opinion '
                                    'anywhere at all"']},
            {"claim_id": "CLM-0003", "grade": "A", "normalized_claim": "no quote at all",
             "evidence_locations": ["opinion, Part I"]},
            # a locator with an intra-word apostrophe must not swallow the real evidence
            {"claim_id": "CLM-0004", "grade": "A", "normalized_claim": "apostrophe in locator",
             "evidence_locations": ['O’Connor, J., dissenting | "the tenant’s door was '
                                    'the last resort in every one of these three cases"']},
            # a bare footnote marker in the capture must not break a genuine quotation
            {"claim_id": "CLM-0005", "grade": "A", "normalized_claim": "footnote marker inside",
             "evidence_locations": ['opinion II-B | "In a good percentage of cases, posting '
                                    'follows forthwith"']},
            # ... but a bracketed WORD is a real edit and must still fail
            {"claim_id": "CLM-0006", "grade": "A", "normalized_claim": "words deleted by bracket",
             "evidence_locations": ['opinion II-B | "In a good percentage of cases, [posting '
                                    'follows] forthwith and the sheriff drove away"']},
        ]}
        _atomic_write_json(tmp / "claims.json", bad)
        r = evaluate(tmp / "claims.json", [tmp / "src.md"])
        _print_report(r)
        st = {row["claim_id"]: row["status"] for row in r["rows"]}
        red_ok = (r["ok"] is False and st.get("CLM-0001") == "traced"
                  and st.get("CLM-0002") == "NOT_IN_SOURCE" and st.get("CLM-0003") == "NO_QUOTE"
                  and st.get("CLM-0004") == "traced" and st.get("CLM-0005") == "traced"
                  and st.get("CLM-0006") == "NOT_IN_SOURCE")
        print(f"\nexpected ok=False, CLM-0002/0006 NOT_IN_SOURCE, CLM-0003 NO_QUOTE, "
              f"CLM-0001/0004/0005 traced; got ok={r['ok']} {st}")
        print("SELFTEST: PASS" if red_ok else "SELFTEST: FAIL")
    return 0 if red_ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001 - exotic stdout; non-fatal
        pass
    ap = argparse.ArgumentParser(
        description="FAIL if a grade-A claim does not quote a supplied primary-source capture.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=None, help="episode slug (resolves claims.v*.json)")
    ap.add_argument("--claims", default=None, help="explicit claims.v*.json path")
    ap.add_argument("--source", action="append", default=[],
                    help="primary-source capture file (repeatable)")
    ap.add_argument("--json", default=None, metavar="PATH", help="write the report dict to PATH")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    if args.claims:
        claims_path = Path(args.claims)
    elif args.ep:
        cands = sorted((ROOT / "episodes" / args.ep / "01_research").glob("claims.v*.json"))
        if not cands:
            print(f"[ERROR] no claims.v*.json under episodes/{args.ep}/01_research")
            return 1
        claims_path = cands[-1]
    else:
        print("[ERROR] give --ep or --claims")
        return 1

    r = evaluate(claims_path, [Path(s) for s in args.source])
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"\n[wrote] {args.json}")
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
