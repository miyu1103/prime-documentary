#!/usr/bin/env python
"""Validate a Codex plate order against its episode's own machine contract.

WHY THIS EXISTS. Four episodes running, the same defect reached a finished order
and was caught only because I happened to re-run an ad-hoc snippet:

  EP78  'nobody present'      -> matched forbidden subject 'body'
  EP79  'no wreckage'         -> matched forbidden subject 'wreckage'
  EP81  'plain white bodywork'-> matched forbidden subject 'body'
  EP82  'nobody there'        -> matched forbidden subject 'body', four times

Every one of those is a NEGATION. The prompt says the thing must not appear, and
the substring check that runs after the render cannot tell the difference. A
plate ordered that way either gets refused at check_spec_satisfied time, hours
after the render, or slips through because nobody re-ran the snippet.

check_image_order_neg.py already validates the STYLE/NEG blocks. This validates
the rows against the episode's spec:

  * every id present exactly once, contiguous from 001
  * the P flag count meets episode_spec.people_plates_min
  * no prompt contains any episode_spec.forbidden_subjects term
  * every prompt names a light source -- EP77 lost 16 plates to prompts that
    did not, and the shared STYLE line was not enough

    py -3.11 scripts/check_image_order_spec.py --slug valdez --order <path>

Exit 0 only when all four hold.

2026-08-25: it also reads a THUMBNAIL order. Nothing had ever checked one against
the episode's own contract, and EP85 katrina proves the cost -- its spec forbids
'school bus', 'buses in floodwater' and 'abandoned bus', and candidate T04 was
ordered as "a bus yard of yellow school buses standing up to their windows in dark
floodwater". It was generated, it was reviewed, it was recommended by the previous
lane, and the only thing that caught it was a person reading the spec by hand.
The check on the ORDER would have fired before a single image was made.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]

ROW = re.compile(r"^\|\s*([A-Z]\d{3})\s*\|\s*[A-Z]\d{3}\s*\|\s*(.+?)\s*\|\s*(P?)\s*\|$", re.M)

# The THUMBNAIL order is not a table. It is a block per candidate:
#
#   --- T04 — スクールバスの列
#   <one line: the positive prompt>
#   NEGATIVE: <one line: terms that must NOT appear>
#
# Only the POSITIVE line may be measured against forbidden_subjects. The NEGATIVE
# line lists forbidden terms on purpose, and matching it would fail every order.
THUMB = re.compile(r"^---\s*(T\d{2})\b[^\n]*\n\s*([^\n]+)\n", re.M)

LIGHT = re.compile(
    r"daylight|sunlight|bright|brillian|dawn|sunrise|sunset|blazing|blown out|blowing out|"
    r"flooding|glare|floodlight|burning|backlit|alight|flare|flaring|glowing|golden hour|"
    r"lamp|light|lit |moonlight|firelight|strobe",
    re.I,
)


NEGATION = re.compile(r"(?:^|[^a-z])(?:no|non|un|without)$")


def term_verdict(term: str, prompt_lower: str) -> str:
    """`fail`, `note`, or `` for one forbidden term against one prompt.

    Why this is not a plain `term in prompt`. The specs now carry PLACE terms, because
    a wrong-country pool cost the build thread three re-renders -- and place terms are
    short. `rio` is inside `interior` and `exterior`; `rome` is inside `chrome`; `paris`
    is inside `comparison`. On 2026-08-25 that made all three EP83-85 plate orders red on
    ten hits, none of which was a defect, which is precisely how a gate stops being read.

    What must still fail is the ORIGINAL reason this file exists: a prompt that names the
    forbidden thing in a negation. A diffusion model does not read `nobody present` as an
    absence -- it draws the person. So:

      * whole token, plural tolerated -- `school buses` for `school bus`   -> fail
      * the term starts a word -- `bodywork`                               -> fail
      * the term ends a word preceded by a negation -- `nobody`            -> fail
      * the term buried inside an unrelated word -- `interior`, `chrome`   -> note

    The downstream gate (`check_spec_satisfied._words`) already matches whole words for
    exactly this reason, so this makes the pre-check agree with the gate it forecasts
    rather than being stricter than it.
    """
    verdict = ""
    for m in re.finditer(re.escape(term), prompt_lower):
        s, e = m.span()
        if prompt_lower[e:e + 2] == "es":
            e += 2
        elif prompt_lower[e:e + 1] == "s":
            e += 1
        left = s == 0 or not (prompt_lower[s - 1].isalnum() or prompt_lower[s - 1] == "-")
        right = e == len(prompt_lower) or not (prompt_lower[e].isalnum() or prompt_lower[e] == "-")
        if left and right:
            return "fail"
        if left and not right:
            return "fail"                      # `bodywork` -- the term opens the word
        if right and NEGATION.search(prompt_lower[max(0, s - 8):s]):
            return "fail"                      # `nobody` -- a negation glued to the term
        verdict = "note"
    return verdict


SELFTEST = [
    ("school bus", "a bus yard of yellow school buses standing in dark floodwater", "fail"),
    ("wreckage", "no wreckage, an empty hillside at dawn", "fail"),
    ("body", "nobody present, the rail is empty in bright daylight", "fail"),
    ("body", "plain white bodywork under floodlight", "fail"),
    ("body", "all-white narrow-body airliners lit by dawn", "note"),
    ("rio", "a federal courtroom interior, empty, brilliant daylight", "note"),
    ("rome", "chrome levers in a row, bright overhead light", "note"),
    ("paris", "a much longer one for comparison, bright daylight", "note"),
    ("child", "an empty classroom at dusk, one lamp lit", ""),
]


def selftest() -> int:
    bad = 0
    for term, prompt, want in SELFTEST:
        got = term_verdict(term, prompt)
        ok = got == want
        bad += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'BAD '} '{term}' -> {got or 'clear':4s} (want {want or 'clear'})  {prompt[:52]}")
    print(f"[order-spec] selftest: {len(SELFTEST) - bad}/{len(SELFTEST)} cases correct")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true",
                    help="prove the matcher still fails the cases it exists for, then exit")
    if "--selftest" in sys.argv:
        return selftest()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--order", required=True)
    ap.add_argument("--kind", choices=("auto", "plates", "thumbnails"), default="auto",
                    help="order shape. 'auto' reads the plate table, then the thumbnail blocks")
    a = ap.parse_args()

    sys.path.insert(0, str(ROOT / "scripts"))
    from check_episode_spec import load_and_validate

    spec, problems, _ = load_and_validate(a.slug)
    if not spec:
        print(f"[order-spec] {a.slug}: the contract is not valid, so the order cannot be checked")
        for p in problems:
            print("   -", p)
        return 1

    text = Path(a.order).read_text(encoding="utf-8")
    kind = a.kind
    rows = ROW.findall(text)
    if rows and kind == "thumbnails":
        rows = []
    if not rows and kind in ("auto", "thumbnails"):
        rows = [(tid, prompt, "") for tid, prompt in THUMB.findall(text)]
        if rows:
            kind = "thumbnails"
    if not rows:
        print(f"[order-spec] {a.slug}: no plate rows parsed. The table shape is "
              f"| id | beat | prompt | flags | under a '### SECTION' heading, "
              f"or a thumbnail order's '--- T01 — ...' blocks")
        return 1
    if kind == "auto":
        kind = "plates"

    fails: list[str] = []
    ids = [r[0] for r in rows]
    prefix = ids[0][0]
    width = len(ids[0]) - len(prefix)
    want = {f"{prefix}{n:0{width}d}" for n in range(1, len(rows) + 1)}
    if set(ids) != want or len(set(ids)) != len(ids):
        missing = sorted(want - set(ids))
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        fails.append(f"ids not contiguous {prefix}{1:0{width}d}-{prefix}{len(rows):0{width}d}"
                     + (f"; missing {missing[:8]}" if missing else "")
                     + (f"; duplicated {dupes[:8]}" if dupes else ""))

    n_people = sum(1 for r in rows if r[2] == "P")
    # A thumbnail order is ten candidates, not the film's plate set. The people floor
    # is a property of the FILM and does not apply here; the forbidden-subject and
    # light checks do.
    floor = 0 if kind == "thumbnails" else int(spec.get("people_plates_min", 0))
    if n_people < floor:
        fails.append(f"{n_people} P flag(s) against a floor of {floor}")

    terms = spec.get("forbidden_subjects", [])
    hits: list[tuple[str, str]] = []
    inside: list[tuple[str, str, str]] = []
    for cid, prompt, _ in rows:
        low = prompt.lower()
        for term in terms:
            if term not in low:
                continue
            v = term_verdict(term, low)
            if v == "note":
                where = low.find(term)
                inside.append((cid, term, prompt[max(0, where - 24):where + len(term) + 24]))
            elif v == "fail":
                hits.append((cid, term))
    if inside:
        # Never dropped silently: printed, but not a failure in thumbnails mode.
        print(f"[order-spec] {a.slug}: {len(inside)} substring hit(s) INSIDE another word "
              f"(not a depiction of the forbidden thing):")
        for cid, term, frag in inside[:8]:
            print(f"   note: {cid} '{term}' ...{frag}...")
        if len(inside) > 8:
            print(f"   note: ...and {len(inside) - 8} more")
    if hits:
        for cid, term in hits[:12]:
            prompt = next(p for i, p, _ in rows if i == cid)
            where = prompt.lower().find(term)
            frag = prompt[max(0, where - 24):where + len(term) + 24]
            fails.append(f"{cid} contains forbidden subject '{term}'  ...{frag}...")
        if len(hits) > 12:
            fails.append(f"...and {len(hits) - 12} more forbidden-subject hits")

    dark = [cid for cid, prompt, _ in rows if not LIGHT.search(prompt)]
    if dark:
        fails.append(f"{len(dark)} prompt(s) name no light source: {dark[:10]}")

    print(f"[order-spec] {a.slug}: {kind}, {len(rows)} row(s), {n_people} P flag(s) (floor {floor}), "
          f"{len(spec.get('forbidden_subjects', []))} forbidden subject(s) checked")
    if fails:
        for f in fails:
            print("  FAIL:", f)
        print()
        print("Note on negations: a prompt that says 'nobody there' or 'no wreckage' still")
        print("CONTAINS the forbidden word. The substring check downstream cannot tell the")
        print("difference, so rewrite it positively -- 'the rail is empty', 'an empty quay'.")
        return 1
    print("[order-spec] PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
