"""RETENTION-CADENCE gate: the viewer must be re-hooked on a rhythm (SPEC row 16).

WHY THIS GATE EXISTS
--------------------
`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` row 16 ("Watched-to-end + Like rate") is the
ONLY row in the whole contract table with no implemented gate whatsoever -- its Verify
column says "script QC (retention map)" and no such script exists. Row 16 spells out the
requirement numerically: "re-hooks every ~2-3 min (a new question/turn before interest
decays)" and "no dead air, no flat exposition stretch".

It matters more than any other ungated row: `episodes/_planning/STRATEGY_v001.md` makes
retention + CTR the channel's #1 monetization lever, and the retros keep re-deriving the
same floor by hand -- EP33 #54 measured a 6:16 second-person/threat-beat gap against its
own 5:30 floor and failed it; EP35 r2 found the 18:15->ED stretch carried no hook at all.
Both were caught by a human reading a transcript, which is exactly the "don't rely on
memory, make it a gate" META-RULE.

HOW A "RE-HOOK" IS MEASURED (and why there are TWO floors, not one)
------------------------------------------------------------------
Measured from `remotion/src/data/<slug>_film.json` `captions[]` ({start,end,text}) --
the actual spoken line with real timings, not a plan document.

Calibrating this honestly required rejecting two tempting single-metric designs, because
both are false-RED machines (the `caption_integrity` lesson: a gate that fails the entire
back catalogue is a broken gate, not a broken catalogue). Measured 2026-07-19 over all 13
`*_film.json`:

  (a) LITERAL QUESTIONS ONLY, at row 16's "every 3 min": max question-free gap ranges
      180s..787s across the catalogue. The BEST episode in the channel (unlock) sits at
      180.1s. A 180s floor fails 13 of 13 -- including the good ones. Rejected as the
      sole floor.
  (b) BROAD MARKER (question OR 2nd-person "you/your" OR turn word), at 180s: max gap
      ranges 24.7s..139.1s. That passes 13 of 13 -- it catches nothing. Rejected as the
      sole floor.

The truth is in between, so the gate uses BOTH, each at the threshold its own proxy can
honestly support:

  FLOOR 1 -- BROAD re-hook cadence <= REHOOK_GAP_MAX_S (180s).
      This is row 16 encoded literally ("re-hooks every ~2-3 min") over the broad marker
      set. All 13 current films pass (worst: hinders 139.1s). It is a REGRESSION LOCK --
      it holds the line the catalogue already meets so no future episode drifts below it.

  FLOOR 2 -- DIRECT-QUESTION cadence <= QUESTION_GAP_MAX_S (420s).
      A narrower proxy, so a deliberately looser threshold. It catches the real defect
      class the broad marker cannot see: stretches where the narration stops ASKING the
      viewer anything and lapses into pure exposition. Measured max question-free gap:

          unlock       180.1s        rodriguez    192.6s        tyler        212.1s
          carsearch    258.0s        forfeiture   294.6s        katz         301.2s
          kyllo        310.3s        kidsforcash  321.2s        williams     324.6s
          cotton       352.6s        hinders      555.3s  FAIL
          hinton       676.3s  FAIL  (ZERO questions in the entire 11.3-min episode)
          rolin        786.7s  FAIL

      420s sits in the natural gap between the 352.6s cluster and the 555.3s outliers,
      so it separates the catalogue instead of condemning it: 10 pass, 3 fail. hinton
      poses no question to the viewer at any point, which is precisely the flat-exposition
      failure row 16 describes.

NOT gated here (belongs to row 9, and needs semantics not string matching): promise-payoff
-- whether the cold-open question is actually ANSWERED later. Deferred, see
GATE_AUDIT_v001.md.

Read-only. No writes, no network, no paid calls. Exit 0 = PASS, 1 = FAIL.

Usage:
    python scripts/check_retention_cadence.py episodes/PD-2026-038-kidsforcash
    python scripts/check_retention_cadence.py --film remotion/src/data/rolin_film.json --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # cp932 guard (Windows)
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

CHECK_NAME = "retention_cadence"

REHOOK_GAP_MAX_S = 180.0     # spec row 16: re-hooks every ~2-3 min (broad marker)
QUESTION_GAP_MAX_S = 420.0   # direct-question floor (narrow proxy, looser threshold)

RE_QUESTION = re.compile(r"\?")
RE_SECOND_PERSON = re.compile(r"(?i)\b(you|your|yours|you're|you've)\b")
RE_TURN = re.compile(
    r"(?i)\b(but|yet|until|except|instead|however|nobody knew|no one knew|"
    r"what nobody|what no one|never|would not|wasn't|was not|didn't|did not)\b")


def _marks(captions: list, pattern_fns) -> list[float]:
    out = []
    for c in captions:
        text = str(c.get("text") or "")
        if any(fn(text) for fn in pattern_fns):
            out.append(float(c.get("start") or 0.0))
    return sorted(out)


def _max_gap(marks: list[float], total: float) -> tuple[float, float]:
    """Return (largest gap, time the gap starts). Gaps are measured from t=0 to the
    first mark, between marks, and from the last mark to the end -- a hook-free opening
    and a hook-free tail both count (EP35 r2 was a hook-free tail)."""
    pts = [0.0] + marks + [total]
    best, at = 0.0, 0.0
    for a, b in zip(pts, pts[1:]):
        if b - a > best:
            best, at = b - a, a
    return best, at


def evaluate_film(film_path: Path) -> dict:
    data = json.loads(film_path.read_text(encoding="utf-8"))
    caps = data.get("captions") or []
    total = float(data.get("narrationSeconds") or 0.0)

    if not caps or total <= 0:
        return {"check": CHECK_NAME, "ok": True, "skipped": True,
                "reason": f"no captions/narrationSeconds in {film_path.name}"}

    q_marks = _marks(caps, [RE_QUESTION.search])
    broad_marks = _marks(caps, [RE_QUESTION.search, RE_SECOND_PERSON.search, RE_TURN.search])

    broad_gap, broad_at = _max_gap(broad_marks, total)
    q_gap, q_at = _max_gap(q_marks, total)

    problems = []
    if broad_gap > REHOOK_GAP_MAX_S:
        problems.append(
            f"re-hook gap {broad_gap:.0f}s > {REHOOK_GAP_MAX_S:.0f}s "
            f"starting at {broad_at/60:.1f}min")
    if q_gap > QUESTION_GAP_MAX_S:
        problems.append(
            f"no direct question for {q_gap:.0f}s > {QUESTION_GAP_MAX_S:.0f}s "
            f"starting at {q_at/60:.1f}min"
            + (" (episode poses ZERO questions)" if not q_marks else ""))

    return {
        "check": CHECK_NAME,
        "ok": not problems,
        "film": str(film_path),
        "runtime_s": round(total, 1),
        "rehook_marks": len(broad_marks),
        "max_rehook_gap_s": round(broad_gap, 1),
        "max_rehook_gap_at_s": round(broad_at, 1),
        "rehook_gap_max_s": REHOOK_GAP_MAX_S,
        "question_marks": len(q_marks),
        "first_question_s": round(q_marks[0], 1) if q_marks else None,
        "max_question_gap_s": round(q_gap, 1),
        "max_question_gap_at_s": round(q_at, 1),
        "question_gap_max_s": QUESTION_GAP_MAX_S,
        "problems": problems,
    }


def _find_film(epdir: Path) -> Path | None:
    slug = epdir.name.split("-")[-1]
    root = epdir.parent.parent
    cands = list((root / "remotion" / "src" / "data").glob(f"*{slug}*film*.json"))
    cands += list(epdir.glob("04_scenes/*film*.json"))
    return max(cands, key=lambda p: p.stat().st_size) if cands else None


def evaluate(epdir: Path) -> dict:
    """PREFLIGHT adapter for preflight_render_gate._run_ext_gate."""
    epdir = Path(epdir)
    film = _find_film(epdir)
    if film is None:
        return {"ok": True, "hard": True, "skipped": True, "reason": "no film.json yet"}
    try:
        r = evaluate_film(film)
    except (json.JSONDecodeError, OSError) as exc:
        # Fail CLOSED (EP32 B1).
        return {"ok": False, "hard": True, "skipped": False,
                "reason": f"unreadable {film.name}: {exc}"}
    if r.get("skipped"):
        return {"ok": True, "hard": True, "skipped": True, "reason": r.get("reason", "")}

    if r["ok"]:
        reason = (f"re-hook gap {r['max_rehook_gap_s']}s <= {REHOOK_GAP_MAX_S:.0f}s "
                  f"({r['rehook_marks']} marks); question gap {r['max_question_gap_s']}s "
                  f"<= {QUESTION_GAP_MAX_S:.0f}s ({r['question_marks']} questions)")
    else:
        reason = "; ".join(r["problems"])
    return {"ok": r["ok"], "hard": True, "skipped": False, "reason": reason, **r}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("epdir", type=Path, nargs="?", help="episode dir")
    ap.add_argument("--film", type=Path, help="evaluate a specific film.json")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.film:
        if not a.film.is_file():
            print(f"FAIL {CHECK_NAME}: no such film {a.film}")
            return 1
        r = evaluate_film(a.film)
    elif a.epdir:
        if not a.epdir.is_dir():
            print(f"FAIL {CHECK_NAME}: no such episode dir {a.epdir}")
            return 1
        r = evaluate(a.epdir)
    else:
        ap.error("give an episode dir or --film")

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r.get("ok") else 1

    if r.get("skipped"):
        print(f"SKIP {CHECK_NAME}: {r.get('reason','')}")
        return 0
    print(f"{'PASS' if r['ok'] else 'FAIL'} {CHECK_NAME}: {Path(r.get('film','?')).name}")
    print(f"  runtime        : {r.get('runtime_s')}s")
    print(f"  re-hook marks  : {r.get('rehook_marks')}  max gap "
          f"{r.get('max_rehook_gap_s')}s @{(r.get('max_rehook_gap_at_s') or 0)/60:.1f}min "
          f"(max {REHOOK_GAP_MAX_S:.0f}s)")
    fq = r.get("first_question_s")
    print(f"  questions      : {r.get('question_marks')}  first "
          f"{f'{fq}s' if fq is not None else 'never'}  "
          f"max gap {r.get('max_question_gap_s')}s (max {QUESTION_GAP_MAX_S:.0f}s)")
    for p in r.get("problems", []):
        print(f"  ! {p}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
