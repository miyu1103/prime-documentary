#!/usr/bin/env python3
"""Mechanical craft gate for a PD narration script. Exit 0 = shippable, 2 = fail.

Owner directive 2026-08-01: the script must be built so it cannot fail, and checked three
times. Two of those three passes are human judgement and cannot be automated. THIS is the
third, and it is the one that catches what a reader's eye slides over — a stock phrase, a
stretch of 90 seconds with nothing concrete in it, a number the facts ledger says we may
not use.

Measured basis (`DEEP_RESEARCH_FINDINGS.v001.md` §4, T4): winner material contains ZERO
emotion commands across ~4 hours; our last two scripts contained 9 and 14. Winners run
5-12 hard specifics per minute; one of ours had a 129-second gap with none. This gate is
those findings turned into arithmetic.

    py -3.11 scripts/check_script_craft.py episodes/_planning/EP60_surfside_script.en.v001.md \
        --ledger episodes/_planning/EP60_surfside_FACTS_LEDGER.v001.md \
        --words 6150 6350 --wpm 173

Narration is every line that is not a heading (#), a quote block (>), a list item (-),
a table row (|), a fence (```), an annotation (【…】) or a stage mark (⟨…⟩). Keep that
convention and the word count is exact.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# --- R-19: emotion commands. Winners: zero in ~4 hours of transcript. -------------
EMOTION_CMD = re.compile(
    r"\b(sit with|think about the|feel the (full )?weight|now sit inside|let that sink|"
    r"aim it at|imagine (for a moment|what)|picture (this|it)|consider for a moment|"
    r"take a moment|ask yourself|remember that feeling)\b", re.I)

# --- Spoken CTA. Measured 2026-08-03: 46 published Shorts read a call to action aloud and
# 45 of them converted zero subscribers. docs/PD_SHORTS_TO_LONGFORM_FUNNEL.v001.md makes the
# rule explicit -- the ask lives in the description, the pinned comment and the end card.
# Long-form inherits it: a narrator who asks for the subscription spends the payoff on the ask.
SPOKEN_CTA = re.compile(
    r"\b(subscribe|hit (the )?(bell|like)|smash (that )?like|like (and|&) subscribe|"
    r"leave a comment|comment below|let me know (what|in the comments)|"
    r"link (is )?in the (description|bio)|check out (the )?(link|description)|"
    r"follow (us|me) (on|for)|ring the bell|turn on notifications|"
    r"if you (enjoyed|liked) (this|the) video|don'?t forget to)\b", re.I)


# --- R-24: AI-smell. Phrases that mark machine prose regardless of topic. ---------
AI_SMELL = [
    "it's important to note", "it is important to note", "it's worth noting",
    "in a world where", "at its core", "the reality is", "little did they know",
    "fast forward", "needless to say", "when all is said and done",
    "serves as a reminder", "stands as a testament", "a testament to",
    "tapestry", "delve into", "delves into", "navigate the complexities",
    "shed light on", "paint a picture", "the perfect storm", "a stark reminder",
    "chilling reminder", "haunting reminder", "begs the question",
    "one thing is certain", "only time will tell", "the bottom line is",
    "not just a", "not merely a", "more than just a",
]

# --- R-24: co-investigator nudges and rhetorical questions ------------------------
SECOND_PERSON = re.compile(r"\b(you|your|yours|you're|you've|you'll)\b", re.I)

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
PROPER = re.compile(r"\b[A-Z][a-z]{2,}\b")
NUMERIC = re.compile(r"\b(\d[\d,\.]*|one|two|three|four|five|six|seven|eight|nine|ten|"
                     r"eleven|twelve|thirteen|twenty|thirty|forty|fifty|sixty|ninety|"
                     r"hundred|thousand|million|billion|january|february|march|april|may|"
                     r"june|july|august|september|october|november|december)\b", re.I)

SKIP_PREFIX = ("#", ">", "-", "|", "```", "*", "【", "⟨", "<!--", "!")


def narration_lines(text: str) -> list[str]:
    out, in_fence = [], False
    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not s or s.startswith(SKIP_PREFIX):
            continue
        out.append(s)
    return out


def words(s: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9'’\-]+", s)


def forbidden_from_ledger(path: Path) -> list[tuple[str, str]]:
    """Every ⛔ row in the ledger becomes a phrase the script may not contain."""
    if not path or not path.exists():
        return []
    out = []
    for line in path.read_text("utf-8").splitlines():
        s = line.strip()
        # ONLY a quarantine row: | ⛔-NN | claim | grade | source |
        if not re.match(r"^\|\s*⛔-\d+\s*\|", s):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        claim = cells[1] if len(cells) > 1 else ""
        for m in re.finditer(r'["“]([^"”]{6,160})["”]', claim):
            out.append((m.group(1).strip(), cells[0]))
        if not re.search(r'["“]', claim):
            plain = re.sub(r"[*`]", "", claim).strip()
            if 6 <= len(plain) <= 160:
                out.append((plain, cells[0]))
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--ledger")
    ap.add_argument("--words", nargs=2, type=int, default=[6150, 6350])
    ap.add_argument("--wpm", type=float, default=173.0)
    ap.add_argument("--gap-seconds", type=float, default=90.0,
                    help="longest stretch allowed with no number, date or proper noun")
    args = ap.parse_args()

    p = Path(args.script)
    text = p.read_text("utf-8")
    lines = narration_lines(text)
    body = " ".join(lines)
    w = words(body)
    n = len(w)
    fails: list[str] = []
    warns: list[str] = []

    print(f"script   : {p.name}")
    print(f"narration: {n} words  ->  {n/args.wpm:5.2f} min at {args.wpm} wpm")

    lo, hi = args.words
    if not (lo <= n <= hi):
        fails.append(f"word count {n} outside band {lo}-{hi}")

    # R-19 emotion commands
    hits = [m.group(0) for m in EMOTION_CMD.finditer(body)]
    print(f"emotion commands      : {len(hits)}  (limit 0)" + (f"  {hits[:4]}" if hits else ""))
    if hits:
        fails.append(f"{len(hits)} emotion command(s): {sorted(set(h.lower() for h in hits))}")

    # R-24 AI smell
    low = body.lower()
    smell = [s for s in AI_SMELL if s in low]
    print(f"AI-smell phrases      : {len(smell)}  (limit 0)" + (f"  {smell}" if smell else ""))
    if smell:
        fails.append(f"AI-smell phrases present: {smell}")

    # Spoken CTA. The ask belongs in the description, the pinned comment and the end card.
    cta = [m.group(0) for m in SPOKEN_CTA.finditer(body)]
    print(f"spoken CTA            : {len(cta)}  (limit 0)" + (f"  {cta[:4]}" if cta else ""))
    if cta:
        fails.append(f"spoken call to action in narration: {cta[:3]} -- 45 of 46 Shorts that "
                     f"read a CTA aloud converted zero subscribers "
                     f"(docs/PD_SHORTS_TO_LONGFORM_FUNNEL.v001.md)")

    # R-24 second person and rhetorical questions
    sp = len(SECOND_PERSON.findall(body))
    sp_rate = sp / max(1, n) * 1000
    print(f"you/your per 1000w    : {sp_rate:5.2f}  (limit 8.0)")
    if sp_rate > 8.0:
        fails.append(f"second person {sp_rate:.2f}/1000w over 8.0")

    sents = [s for s in SENT_SPLIT.split(body) if s.strip()]
    q = sum(1 for s in sents if s.rstrip().endswith("?"))
    q_rate = q / max(1, n) * 1000
    print(f"questions per 1000w   : {q_rate:5.2f}  (limit 2.0)  [{q} total]")
    if q_rate > 2.0:
        fails.append(f"rhetorical questions {q_rate:.2f}/1000w over 2.0")

    # R-24 short-punch share
    short = sum(1 for s in sents if len(words(s)) <= 6)
    share = short / max(1, len(sents)) * 100
    print(f"short sentences (<=6w): {share:5.1f}%  (band 20-35%)  [{short}/{len(sents)}]")
    if not (20.0 <= share <= 35.0):
        (fails if share < 12.0 or share > 45.0 else warns).append(
            f"short-punch share {share:.1f}% outside 20-35%")

    # R-21 specificity: no stretch longer than --gap-seconds without a concrete anchor
    per_word = 60.0 / args.wpm
    worst, worst_at, run, run_start = 0.0, 0, 0, 0
    cursor = 0
    for s in sents:
        sw = len(words(s))
        concrete = NUMERIC.search(s) or PROPER.search(s)
        if concrete:
            run = 0
            run_start = cursor + sw
        else:
            run += sw
            if run * per_word > worst:
                worst, worst_at = run * per_word, run_start
        cursor += sw
    print(f"longest bare stretch  : {worst:5.1f}s  (limit {args.gap_seconds:.0f}s)"
          f"  [~word {worst_at}]")
    if worst > args.gap_seconds:
        fails.append(f"{worst:.0f}s with no number, date or proper noun (word ~{worst_at})")

    specifics = sum(1 for s in sents if NUMERIC.search(s) or PROPER.search(s))
    per_min = specifics / max(0.1, n / args.wpm)
    print(f"specific sentences/min: {per_min:5.2f}  (floor 5.0)")
    if per_min < 5.0:
        fails.append(f"specificity {per_min:.2f}/min under 5.0")

    # facts ledger: quarantined claims must not appear
    forb = forbidden_from_ledger(Path(args.ledger)) if args.ledger else []
    bad = [(ph, why) for ph, why in forb if ph.lower() in low]
    print(f"quarantined claims used: {len(bad)}  (limit 0)")
    for ph, why in bad:
        fails.append(f"uses a QUARANTINED claim: \"{ph}\"  <- {why}")

    print()
    for wmsg in warns:
        print(f"WARN  {wmsg}")
    if fails:
        for f in fails:
            print(f"FAIL  {f}")
        print(f"\n{len(fails)} failure(s). Not shippable.")
        return 2
    print("PASS  every mechanical craft gate is green.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
