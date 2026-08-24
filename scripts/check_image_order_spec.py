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

LIGHT = re.compile(
    r"daylight|sunlight|bright|brillian|dawn|sunrise|sunset|blazing|blown out|blowing out|"
    r"flooding|glare|floodlight|burning|backlit|alight|flare|flaring|glowing|golden hour|"
    r"lamp|light|lit |moonlight|firelight|strobe",
    re.I,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--order", required=True)
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
    rows = ROW.findall(text)
    if not rows:
        print(f"[order-spec] {a.slug}: no plate rows parsed. The table shape is "
              f"| id | beat | prompt | flags | under a '### SECTION' heading")
        return 1

    fails: list[str] = []
    ids = [r[0] for r in rows]
    prefix = ids[0][0]
    want = {f"{prefix}{n:03d}" for n in range(1, len(rows) + 1)}
    if set(ids) != want or len(set(ids)) != len(ids):
        missing = sorted(want - set(ids))
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        fails.append(f"ids not contiguous {prefix}001-{prefix}{len(rows):03d}"
                     + (f"; missing {missing[:8]}" if missing else "")
                     + (f"; duplicated {dupes[:8]}" if dupes else ""))

    n_people = sum(1 for r in rows if r[2] == "P")
    floor = int(spec.get("people_plates_min", 0))
    if n_people < floor:
        fails.append(f"{n_people} P flag(s) against a floor of {floor}")

    hits = [(cid, term) for cid, prompt, _ in rows
            for term in spec.get("forbidden_subjects", []) if term in prompt.lower()]
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

    print(f"[order-spec] {a.slug}: {len(rows)} row(s), {n_people} P flag(s) (floor {floor}), "
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
