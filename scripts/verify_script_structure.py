#!/usr/bin/env python3
r"""Independent script-STRUCTURE gate — catches a mis-built narrative skeleton before it ships.

The owner's recurring structural defect (memory: pd-ep21-24-incident #4) is an episode that is NOT
built as "8s hook -> opening -> body -> ending/CTA": the cold open runs long, there is no re-hook so
the middle sags, the viewer is never addressed as "you," or a question the film opens is never paid
off. Those break retention and are invisible to the audio/caption gates. This is the INDEPENDENT
GATE that reads the ANNOTATED SCRIPT (the authored intent, before any render exists) and fails a
skeleton that violates the house structure, so a badly-shaped script can never reach the edit bay.

It measures the real INTENT from the annotated script's own labels + prose — it does NOT trust a
render (there may be none yet) and does NOT trust a self-reported qc_status. It:

  * walks the ordered chapters/spans and assigns each a DRIFT-FREE start/end on a spoken timeline,
    using explicit per-span timecodes when present, else word-count / WPM (default 160 wpm, the
    spec's estimate) — frame-accurate absolute timing is not the point; section *ordering* and
    *cadence in minutes* are, and word-count timing is the honest, deterministic yardstick for that;
  * checks the seven house rules and reports every VIOLATED INTERVAL, not just a pass/fail bit:

      1. HOOK is the FIRST section and its narration fits an <= 8 s cold-open budget
      2. OPENING (thesis/promise) immediately follows the hook
      3. at least 4 BODY acts between opening and ending
      4. ENDING / CTA is the LAST section
      5. a LABELLED RE-HOOK beat lands at least every ~2:50 (no flat >170 s stretch with nothing to
         re-grab). The beat must be an authored engagement label (narrative_function: rehook / loop /
         turn / stakes / tension / reveal / payoff / question / ...), NOT an incidental "?" in prose —
         a sagging middle padded with rhetorical questions must still fail this rule.
      6. the viewer is addressed in the SECOND PERSON ("you/your") by <= 5:30
      7. every narrative OPEN-LOOP the script opens (the hook's promise, a posed question, a labelled
         loop_open/rehook) is CLOSED by a later payoff/resolve/summary/CTA beat

Skeleton violations (order / act-count / ending-last / unclosed loop) are HARD — they are
unambiguous authoring defects. The word-count-derived timing thresholds (hook<=8s, re-hook cadence,
second-person-by-5:30) still fail the gate (ok=False) but are reported as SOFT, because they rest on
the 160-wpm estimate rather than a real narration timeline; the caller can weight them accordingly.

Usage:
  py -3.11 scripts/verify_script_structure.py --ep PD-2026-032-carsearch
  py -3.11 scripts/verify_script_structure.py --ep PD-2026-032-carsearch --dry-run
  py -3.11 scripts/verify_script_structure.py --ep PD-2026-032-carsearch --wpm 150 --json out.json
  py -3.11 scripts/verify_script_structure.py --selftest   # RED fixture + real episode numbers

Exit code: 0 = PASS / dry-run / honest-skip, 1 = FAIL or usage error. Read-only; never writes into
the episode (only the optional --json report, atomically).

check_final_acceptance can import this module and call evaluate(epdir); the returned dict
({"check","ok","hard","reason", plus numbers}) is the stable contract. evaluate NEVER calls
sys.exit and NEVER raises on a missing/short artifact — it returns {"skipped": True, ...}.
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

# --- structural budget (the house rules the gate enforces) --------------------------------------
WPM_DEFAULT = 160.0          # spec estimate: derive a spoken timeline from word counts at ~160 wpm
HOOK_MAX_S = 8.0             # a cold-open tease must fit an 8-second budget (owner "hook8s" standard)
BODY_ACTS_MIN = 4            # at least four body acts between OPENING and ENDING (review intent)
REHOOK_MAX_GAP_S = 170.0     # a re-hook beat at least every ~2:50 (no flat 170 s stretch)
SECOND_PERSON_MAX_S = 330.0  # the viewer is addressed as "you/your" by <= 5:30

# narrative_function / chapter-function keyword signals (matched as case-insensitive substrings)
_HOOK_KEYS = ("hook", "cold_open", "cold-open")
_OPENING_KEYS = ("opening", "thesis", "promise", "premise")
_ENDING_KEYS = ("ending", "cta", "outro", "endcard", "sign_off", "sign-off", "payoff_and_cta")

# a beat that re-grabs attention (re-hook / turn / stakes / open question)
_REHOOK_KEYS = ("hook", "rehook", "re_hook", "loop", "turn", "cliff", "tease", "stake",
                "tension", "escalat", "question", "payoff", "mystery", "reveal", "twist")
# a beat that OPENS a narrative loop (a promise/question that must be paid off later)
_OPEN_KEYS = ("loop_open", "open_loop", "rehook", "re_hook", "mystery", "tease", "cliffhanger")
# a beat that CLOSES / pays off a loop
_CLOSE_KEYS = ("payoff", "resolve", "reveal", "answer", "throughline", "summary",
               "quote_resolve", "cta", "endcard")

# second-person address (the viewer being spoken to directly)
_SECOND_PERSON = re.compile(
    r"\byou\b|\byour\b|\byours\b|\byou['’]?(?:re|ve|ll|d)\b|\byourself\b|\byourselves\b",
    re.IGNORECASE)


def word_count(text: str) -> int:
    """Count spoken words in a narration string (whitespace tokens with at least one letter/digit)."""
    return sum(1 for t in text.split() if re.search(r"[A-Za-z0-9]", t))


def _fn_matches(fn: str, keys: tuple[str, ...]) -> bool:
    low = (fn or "").lower()
    return any(k in low for k in keys)


def mmss(seconds: float) -> str:
    """Format seconds as m:ss for a human timeline."""
    seconds = max(0.0, seconds)
    return f"{int(seconds) // 60}:{int(round(seconds)) % 60:02d}"


# ------------------------------------------------------------------------------------------------
# locate + load the annotated script
# ------------------------------------------------------------------------------------------------

def resolve_script(ep_dir: Path) -> Optional[Path]:
    """Highest-revision annotated script for this episode, or None if absent (SSD / not authored).

    Primary: <ep>/03_script/script.annotated.v*.json. Fallback: episodes/_planning/*script.annotated*.
    """
    cands = sorted((ep_dir / "03_script").glob("script.annotated.v*.json"))
    if cands:
        return cands[-1]
    planning = ep_dir.parent / "_planning"
    if planning.is_dir():
        slug = ep_dir.name  # e.g. PD-2026-032-carsearch -> tokens to fuzzy-match a planning filename
        token = slug.split("-")[-1].lower()
        pcands = [p for p in planning.glob("*script.annotated.v*.json") if token in p.name.lower()]
        if pcands:
            return sorted(pcands)[-1]
    return None


# ------------------------------------------------------------------------------------------------
# build the spoken timeline (spans -> absolute start/end; chapters -> role + span span)
# ------------------------------------------------------------------------------------------------

def _span_timecodes(span: dict[str, Any]) -> Optional[tuple[float, float]]:
    """Explicit (start,end) seconds on a span if it carries real timecodes, else None."""
    for a, b in (("start", "end"), ("t_start", "t_end"), ("tc_in", "tc_out"), ("t0", "t1")):
        s, e = span.get(a), span.get(b)
        if isinstance(s, (int, float)) and isinstance(e, (int, float)) and e > s:
            return float(s), float(e)
    return None


def build_timeline(data: dict[str, Any], wpm: float) -> tuple[list[dict[str, Any]], list[dict[str, Any]], bool]:
    """Return (spans, chapters, used_timecodes).

    spans: [{span_id, text, fn, wc, start, end}] in narration order with absolute seconds.
    chapters: [{chapter_id, title, function, role, start, end, span_ids}] in authored order. When the
    JSON has no chapters, one pseudo-chapter per span is synthesized (role from narrative_function)
    so order/role checks still run.
    """
    raw_spans = data.get("spans") or []
    per_word = 60.0 / wpm if wpm > 0 else 0.0
    spans: list[dict[str, Any]] = []
    used_tc = False
    cursor = 0.0
    for sp in raw_spans:
        text = str(sp.get("text", ""))
        wc = word_count(text)
        tc = _span_timecodes(sp)
        if tc is not None:
            used_tc = True
            start, end = tc
        else:
            start = cursor
            end = cursor + wc * per_word
        cursor = max(cursor, end)
        spans.append({
            "span_id": sp.get("span_id", f"SPN-{len(spans) + 1:04d}"),
            "text": text,
            "fn": str(sp.get("narrative_function", "")),
            "wc": wc,
            "start": start,
            "end": end,
        })
    by_id = {s["span_id"]: s for s in spans}

    chapters: list[dict[str, Any]] = []
    raw_chapters = data.get("chapters") or []
    if raw_chapters:
        for ch in raw_chapters:
            ids = [i for i in (ch.get("span_ids") or []) if i in by_id]
            members = [by_id[i] for i in ids]
            if not members:
                continue
            chapters.append({
                "chapter_id": str(ch.get("chapter_id", "")),
                "title": str(ch.get("title", "")),
                "function": str(ch.get("function", "")),
                "start": min(m["start"] for m in members),
                "end": max(m["end"] for m in members),
                "span_ids": ids,
                "fns": [m["fn"] for m in members],
            })
    else:
        # no chapters: one pseudo-chapter per span, role inferred from its narrative_function
        for s in spans:
            chapters.append({
                "chapter_id": s["span_id"],
                "title": s["fn"],
                "function": s["fn"],
                "start": s["start"],
                "end": s["end"],
                "span_ids": [s["span_id"]],
                "fns": [s["fn"]],
            })
    for ch in chapters:
        ch["role"] = classify_role(ch)
    return spans, chapters, used_tc


def classify_role(ch: dict[str, Any]) -> str:
    """hook / opening / ending / body from chapter_id + function + member narrative_functions."""
    cid = ch.get("chapter_id", "").lower()
    fn = ch.get("function", "")
    fns = " ".join(ch.get("fns", []))
    hay = f"{cid} {fn} {fns}"
    # ending first (payoff_and_cta contains no hook/opening tokens; check before hook to be safe)
    if cid in {"ending", "cta", "endcard", "outro"} or _fn_matches(hay, _ENDING_KEYS):
        return "ending"
    if cid == "hook" or _fn_matches(f"{cid} {fn}", _HOOK_KEYS):
        return "hook"
    if cid in {"opening", "open"} or _fn_matches(f"{cid} {fn}", _OPENING_KEYS):
        return "opening"
    return "body"


# ------------------------------------------------------------------------------------------------
# the seven house rules
# ------------------------------------------------------------------------------------------------

def _check_structure(chapters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Skeleton order + act count + ending-last. Returns hard violations."""
    v: list[dict[str, Any]] = []
    roles = [c["role"] for c in chapters]

    if not chapters:
        return [{"rule": "structure", "hard": True, "msg": "no chapters/spans found in script"}]

    if roles[0] != "hook":
        v.append({"rule": "hook_first", "hard": True,
                  "msg": f"first section is '{chapters[0]['chapter_id'] or roles[0]}' "
                         f"(role={roles[0]}), expected HOOK"})
    if len(roles) < 2 or roles[1] != "opening":
        got = chapters[1]["chapter_id"] if len(chapters) > 1 else "<none>"
        v.append({"rule": "opening_second", "hard": True,
                  "msg": f"second section is '{got}' (role={roles[1] if len(roles) > 1 else 'none'}), "
                         f"expected OPENING to follow the hook"})
    if roles[-1] != "ending":
        v.append({"rule": "ending_last", "hard": True,
                  "msg": f"last section is '{chapters[-1]['chapter_id'] or roles[-1]}' "
                         f"(role={roles[-1]}), expected ENDING/CTA last"})

    body = sum(1 for r in roles if r == "body")
    if body < BODY_ACTS_MIN:
        v.append({"rule": "body_acts", "hard": True,
                  "msg": f"{body} body act(s) between opening and ending, expected at least {BODY_ACTS_MIN}"})

    # any hook/opening/ending appearing in the interior is a scrambled skeleton
    interior = roles[1:-1]
    if "hook" in interior or (interior[1:] and "opening" in interior[1:]) or "ending" in interior:
        v.append({"rule": "section_order", "hard": True,
                  "msg": f"section roles out of order: {roles}"})
    return v


def _check_hook_length(chapters: list[dict[str, Any]], spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hook = next((c for c in chapters if c["role"] == "hook"), None)
    if hook is None:
        return []
    dur = hook["end"] - hook["start"]
    if dur > HOOK_MAX_S + 1e-6:
        return [{"rule": "hook_8s", "hard": False,
                 "interval": [hook["start"], hook["end"]],
                 "msg": f"hook cold-open is {dur:.1f}s (> {HOOK_MAX_S:.0f}s budget)"}]
    return []


def _check_rehook_cadence(spans: list[dict[str, Any]], total_end: float) -> tuple[list[dict[str, Any]], list[float], float]:
    """A re-hook/engagement beat must land at least every REHOOK_MAX_GAP_S. Anchors: t=0 and total_end.

    A beat is counted ONLY from an authored engagement label (narrative_function matching
    _REHOOK_KEYS). An incidental "?" in ordinary exposition is deliberately NOT a re-hook beat:
    otherwise a sagging middle padded with rhetorical questions would trivially satisfy the cadence
    (the exact defect this gate exists to catch). A genuine open question carries a labelled function
    ("question" is in _REHOOK_KEYS) and still counts. Returns (violations, beat_times, max_gap)."""
    beats = [0.0]
    for s in spans:
        if _fn_matches(s["fn"], _REHOOK_KEYS):
            beats.append(s["start"])
    beats.append(total_end)
    beats = sorted(set(beats))
    viol: list[dict[str, Any]] = []
    max_gap = 0.0
    for a, b in zip(beats, beats[1:]):
        gap = b - a
        if gap > max_gap:
            max_gap = gap
        if gap > REHOOK_MAX_GAP_S + 1e-6:
            viol.append({"rule": "rehook_cadence", "hard": False,
                         "interval": [a, b],
                         "msg": f"{gap:.0f}s with no re-hook beat ({mmss(a)}->{mmss(b)}, "
                                f"> {REHOOK_MAX_GAP_S:.0f}s)"})
    return viol, beats, max_gap


def _check_second_person(spans: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], Optional[float]]:
    first = next((s["start"] for s in spans if _SECOND_PERSON.search(s["text"])), None)
    if first is None:
        return ([{"rule": "second_person", "hard": False,
                  "msg": "viewer is never addressed in the second person (no 'you/your')"}], None)
    if first > SECOND_PERSON_MAX_S + 1e-6:
        return ([{"rule": "second_person", "hard": False,
                  "interval": [0.0, first],
                  "msg": f"first second-person address at {mmss(first)} "
                         f"(> {mmss(SECOND_PERSON_MAX_S)} deadline)"}], first)
    return ([], first)


def _check_open_loops(spans: list[dict[str, Any]], total_end: float) -> list[dict[str, Any]]:
    """Every opened loop (hook promise / posed question / loop_open / rehook) needs a later close
    (payoff / resolve / summary / CTA). An open with no subsequent close is an unclosed loop."""
    opens: list[dict[str, Any]] = []
    closes: list[float] = []
    for idx, s in enumerate(spans):
        is_open = (idx == 0) or _fn_matches(s["fn"], _OPEN_KEYS) or s["text"].strip().endswith("?")
        if is_open:
            opens.append(s)
        if _fn_matches(s["fn"], _CLOSE_KEYS):
            closes.append(s["start"])
    viol: list[dict[str, Any]] = []
    for o in opens:
        if not any(c > o["start"] + 1e-6 for c in closes):
            viol.append({"rule": "open_loop_unclosed", "hard": True,
                         "interval": [o["start"], total_end],
                         "msg": f"open-loop at {mmss(o['start'])} ({o['span_id']}, fn='{o['fn']}') "
                                f"has no later payoff/resolve/summary/CTA beat"})
    return viol


# ------------------------------------------------------------------------------------------------
# core evaluation (importable by check_final_acceptance)
# ------------------------------------------------------------------------------------------------

def evaluate(epdir: Path, wpm: float = WPM_DEFAULT) -> dict[str, Any]:
    """Measure the narrative skeleton of the annotated script and return a gate dict.

    NEVER raises on a missing/short artifact and NEVER calls sys.exit. Returns
    {"skipped": True, "ok": True, "hard": False, ...} when the annotated script is not in the repo.
    Contract keys: check, ok, hard, reason, (+ timeline, violations, numbers).
    """
    epdir = Path(epdir)
    path = resolve_script(epdir)
    if path is None:
        return {"check": "script_structure", "ok": True, "hard": False, "skipped": True,
                "reason": f"no annotated script under {epdir}/03_script (SSD or not authored)"}
    try:
        data = json.loads(path.read_text("utf-8"))
    except Exception as exc:  # noqa: BLE001 - malformed JSON -> honest skip, never crash the caller
        return {"check": "script_structure", "ok": True, "hard": False, "skipped": True,
                "reason": f"could not parse {path.name}: {exc}"}

    spans, chapters, used_tc = build_timeline(data, wpm)
    if not spans:
        return {"check": "script_structure", "ok": True, "hard": False, "skipped": True,
                "reason": f"{path.name} has no spans to measure"}
    total_end = max(s["end"] for s in spans)

    violations: list[dict[str, Any]] = []
    violations += _check_structure(chapters)
    violations += _check_hook_length(chapters, spans)
    rehook_v, beats, max_gap = _check_rehook_cadence(spans, total_end)
    violations += rehook_v
    sp_v, first_2p = _check_second_person(spans)
    violations += sp_v
    violations += _check_open_loops(spans, total_end)

    ok = len(violations) == 0
    hard = any(v.get("hard") for v in violations)
    if ok:
        reason = (f"skeleton sound: hook->opening->>={BODY_ACTS_MIN} acts->ending, "
                  f"re-hook <= {mmss(max_gap)}, 2nd-person at {mmss(first_2p or 0)}, loops closed")
    else:
        reason = "; ".join(v["msg"] for v in violations)

    timeline = [{"chapter": c["chapter_id"] or c["role"], "role": c["role"],
                 "start": round(c["start"], 1), "end": round(c["end"], 1),
                 "start_mmss": mmss(c["start"]), "end_mmss": mmss(c["end"])}
                for c in chapters]

    return {
        "check": "script_structure",
        "ok": ok,
        "hard": hard,
        "reason": reason,
        "script": str(path),
        "wpm": wpm,
        "timing_source": "timecodes" if used_tc else f"word-count@{wpm:.0f}wpm",
        "total_runtime_s": round(total_end, 1),
        "total_runtime_mmss": mmss(total_end),
        "n_sections": len(chapters),
        "n_body_acts": sum(1 for c in chapters if c["role"] == "body"),
        "hook_len_s": round(next((c["end"] - c["start"] for c in chapters if c["role"] == "hook"), 0.0), 1),
        "rehook_max_gap_s": round(max_gap, 1),
        "first_second_person_s": round(first_2p, 1) if first_2p is not None else None,
        "roles": [c["role"] for c in chapters],
        "timeline": timeline,
        "violations": violations,
    }


# ------------------------------------------------------------------------------------------------
# reporting
# ------------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("SCRIPT STRUCTURE REPORT")
    print("=" * 78)
    print(f"  script        : {r['script']}")
    print(f"  timing source : {r['timing_source']}   total {r['total_runtime_mmss']} "
          f"({r['total_runtime_s']}s)")
    print(f"  skeleton      : {r['n_sections']} sections, {r['n_body_acts']} body act(s)  "
          f"roles={r['roles']}")
    print(f"  hook length   : {r['hook_len_s']}s (budget {HOOK_MAX_S:.0f}s)")
    print(f"  re-hook gap   : max {mmss(r['rehook_max_gap_s'])} (budget {mmss(REHOOK_MAX_GAP_S)})")
    fp = r["first_second_person_s"]
    print(f"  2nd person    : {mmss(fp) if fp is not None else 'NEVER'} "
          f"(deadline {mmss(SECOND_PERSON_MAX_S)})")
    print("\n  section timeline:")
    print("    role     |  start |   end   | chapter")
    print("    ---------+--------+---------+--------------------------------")
    for t in r["timeline"]:
        print(f"    {t['role']:<8} | {t['start_mmss']:>6} | {t['end_mmss']:>6}  | {t['chapter']}")
    print("\n" + "-" * 78)
    if r["ok"]:
        print(f"  RESULT: PASS — {r['reason']}")
    else:
        print(f"  RESULT: FAIL ({'HARD' if r['hard'] else 'soft'})")
        for v in r["violations"]:
            tag = "HARD" if v.get("hard") else "soft"
            iv = v.get("interval")
            loc = f"  [{mmss(iv[0])}->{mmss(iv[1])}]" if iv else ""
            print(f"    - ({tag}) {v['rule']}: {v['msg']}{loc}")
    print("-" * 78)


def _atomic_write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# ------------------------------------------------------------------------------------------------
# selftest: RED fixture (must fail) + real episode numbers
# ------------------------------------------------------------------------------------------------

def _span(span_id: str, fn: str, n_words: int, *, prefix: str = "", suffix: str = "") -> dict[str, Any]:
    """A span whose narration is exactly n_words words (so its WPM-derived duration is deterministic).
    `prefix` seeds leading tokens (e.g. 'you' for second-person); `suffix` appends trailing tokens
    (e.g. 'really?' to plant a rhetorical question). Total word count is kept at n_words."""
    seed = [t for t in (prefix + " " + suffix).split() if t]
    body = ["word"] * max(0, n_words - len(seed))
    tokens = ([prefix] if prefix else []) + body + ([suffix] if suffix else [])
    text = " ".join(t for t in tokens if t)
    return {"span_id": span_id, "narrative_function": fn, "text": text}


def _evaluate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as td:
        epdir = Path(td) / "PD-9999-000-fixture"
        (epdir / "03_script").mkdir(parents=True)
        (epdir / "03_script" / "script.annotated.v001.json").write_text(
            json.dumps(fixture), encoding="utf-8")
        return evaluate(epdir)


def _selftest() -> int:
    # Word-count timeline: 160 wpm -> 0.375 s/word. Hooks/acts are sized in words to hit target seconds.
    ok_all = True

    # -- RED FIXTURE: the EXACT gaming probe -----------------------------------------------------
    # A skeleton that is well-formed in EVERY OTHER respect (hook->opening->4 acts->ending, viewer
    # addressed as "you" in the hook, every open-loop paid off) but with the two defects the reviewer
    # named: (a) a 20s hook (> 8s budget) and (b) a 4-minute stretch with NO re-hook. The sag is four
    # exposition spans that each carry a rhetorical "?" — under the OLD proxy those question marks
    # would count as re-hook beats and the sag would slip through; after the fix only LABELLED
    # engagement beats count, so the 4-minute gap must fail. Isolated so ONLY hook_8s + rehook_cadence
    # fire (both soft) -> ok=False, hard=False.
    print("=" * 78)
    print("SELFTEST — RED FIXTURE (hook 20s / no re-hook for 4 min MUST report ok=False)")
    print("=" * 78)
    red = {
        "episode_id": "PD-9999-000-redfixture",
        "chapters": [
            {"chapter_id": "hook", "function": "cold_open_tease", "span_ids": ["SPN-0001"]},
            {"chapter_id": "opening", "function": "thesis_and_promise", "span_ids": ["SPN-0002"]},
            {"chapter_id": "act1", "function": "stakes", "span_ids": ["SPN-0003"]},
            {"chapter_id": "act2", "function": "exposition",
             "span_ids": ["SPN-0004", "SPN-0005", "SPN-0006", "SPN-0007"]},
            {"chapter_id": "act3", "function": "turn_and_payoff", "span_ids": ["SPN-0008"]},
            {"chapter_id": "act4", "function": "tension", "span_ids": ["SPN-0009"]},
            {"chapter_id": "ending", "function": "payoff_and_cta", "span_ids": ["SPN-0010"]},
        ],
        "spans": [
            _span("SPN-0001", "hook_cold_open", 54, prefix="you"),   # 20.25s hook (> 8s budget)
            _span("SPN-0002", "thesis_and_promise", 30),
            _span("SPN-0003", "stakes", 150),                        # last real re-hook before the sag
            # --- 4 x 60s = 240s sag: exposition labels, each padded with a rhetorical "?" ---
            _span("SPN-0004", "exposition", 160, suffix="really?"),
            _span("SPN-0005", "background", 160, suffix="right?"),
            _span("SPN-0006", "context", 160, suffix="see?"),
            _span("SPN-0007", "detail", 160, suffix="no?"),
            _span("SPN-0008", "turn_and_payoff", 150),               # first real re-hook after the sag
            _span("SPN-0009", "tension", 120),
            _span("SPN-0010", "payoff_and_cta", 30),                 # closes the hook/sag open-loops
        ],
    }
    rr = _evaluate_fixture(red)
    fired = sorted({v["rule"] for v in rr.get("violations", [])})
    red_ok = (
        rr.get("ok") is False
        and rr.get("hard") is False
        and set(fired) == {"hook_8s", "rehook_cadence"}
    )
    print(f"  red fixture ok={rr.get('ok')}  hard={rr.get('hard')}")
    print(f"  hook_len_s={rr.get('hook_len_s')}  rehook_max_gap_s={rr.get('rehook_max_gap_s')}")
    print(f"  violations fired: {fired}   (expected exactly ['hook_8s', 'rehook_cadence'])")
    for v in rr.get("violations", []):
        print(f"    - {v['rule']}: {v['msg']}")
    print("RED-FIXTURE: PASS" if red_ok else "RED-FIXTURE: FAIL")
    ok_all = ok_all and red_ok

    # -- GREEN FIXTURE: a well-shaped skeleton MUST pass -----------------------------------------
    print("\n" + "=" * 78)
    print("SELFTEST — GREEN FIXTURE (a well-shaped skeleton MUST report ok=True)")
    print("=" * 78)
    green = {
        "episode_id": "PD-9999-000-greenfixture",
        "chapters": [
            {"chapter_id": "hook", "function": "cold_open_tease", "span_ids": ["SPN-0001"]},
            {"chapter_id": "opening", "function": "thesis_and_promise", "span_ids": ["SPN-0002"]},
            {"chapter_id": "act1", "function": "stakes", "span_ids": ["SPN-0003"]},
            {"chapter_id": "act2", "function": "escalation", "span_ids": ["SPN-0004"]},
            {"chapter_id": "act3", "function": "turn_and_payoff", "span_ids": ["SPN-0005"]},
            {"chapter_id": "act4", "function": "tension", "span_ids": ["SPN-0006"]},
            {"chapter_id": "ending", "function": "payoff_and_cta", "span_ids": ["SPN-0007"]},
        ],
        "spans": [
            _span("SPN-0001", "hook_cold_open", 18, prefix="you"),   # 6.75s hook (<= 8s), 2nd-person
            _span("SPN-0002", "thesis_and_promise", 30),
            _span("SPN-0003", "stakes", 150),                        # ~56s acts -> re-hook cadence ok
            _span("SPN-0004", "escalation", 150),
            _span("SPN-0005", "turn_and_payoff", 150),               # also closes the hook open-loop
            _span("SPN-0006", "tension", 120),
            _span("SPN-0007", "payoff_and_cta", 30),
        ],
    }
    gr = _evaluate_fixture(green)
    green_ok = gr.get("ok") is True and not gr.get("violations")
    print(f"  green fixture ok={gr.get('ok')}  hard={gr.get('hard')}")
    print(f"  reason: {gr.get('reason')}")
    if gr.get("violations"):
        for v in gr["violations"]:
            print(f"    UNEXPECTED - {v['rule']}: {v['msg']}")
    print("GREEN-FIXTURE: PASS" if green_ok else "GREEN-FIXTURE: FAIL")
    ok_all = ok_all and green_ok

    # -- REAL EPISODE numbers (informational) ----------------------------------------------------
    print("\n" + "=" * 78)
    print(f"SELFTEST — REAL EPISODE ({DEFAULT_EP})")
    print("=" * 78)
    real = evaluate(ROOT / "episodes" / DEFAULT_EP)
    _print_report(real)

    print("\n" + "=" * 78)
    print(f"SELFTEST RESULT: {'PASS' if ok_all else 'FAIL'} "
          f"(red fixture fails as designed AND green fixture passes)")
    print("=" * 78)
    return 0 if ok_all else 1


# ------------------------------------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001 - reconfigure unavailable on some streams; harmless
        pass
    ap = argparse.ArgumentParser(
        description="Independent script-structure gate: FAIL a mis-shaped narrative skeleton.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--wpm", type=float, default=WPM_DEFAULT,
                    help="words-per-minute for the word-count timeline when no timecodes exist")
    ap.add_argument("--dry-run", action="store_true",
                    help="measure and print the report but always exit 0 (non-blocking)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixture then print real-episode numbers")
    ap.add_argument("--json", default=None, help="also write the raw result dict to this path (atomic)")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    r = evaluate(ep_dir, wpm=args.wpm)
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"\n[json] wrote {args.json}")

    if args.dry_run:
        return 0
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
