"""FREE, PRE-SPEND gate: detect near-duplicate / too-generic image prompts in a
CODEX_A asset file BEFORE any GPU time is spent.

Owner directive 2026-07-26: 「意味のない似たような画像が出るようなら今のうちに修正して」.
The phash gate (CODEX_A QC Q4) catches similar IMAGES after generation — this gate
catches similar PROMPTS before generation, when fixing costs nothing.

Method:
  1. Extract prompt rows (| S### / M## / T## / F## | ... |) from the CODEX_A markdown.
  2. Tokenize each prompt to content words; drop corpus-boilerplate tokens that appear
     in >30% of all prompts (palette/lens/style macros shared by design).
  3. Pairwise Jaccard on the residual tokens. Pairs >= --threshold (default 0.50) FAIL.
  4. Prompts with < --min-tokens residual content words (default 6) are flagged as
     too generic ("meaningless filler" risk) -> WARN (FAIL with --strict).

Usage:
    python scripts/check_prompt_diversity.py episodes/_planning/EP53_norfolk_CODEX_A_ASSETS.v001.md
    python scripts/check_prompt_diversity.py <file> --threshold 0.5 --min-tokens 6 --strict
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STOP = set("""a an the of in on at to for with and or but into over under from by as is are was
were be been being this that these those it its his her their your our one two three four not
no without across against toward through during near behind beside above below out up down
""".split())

# prompt rows live inside code fences as:  - `S001.png`  \n  <prompt text line(s)>
MARK = re.compile(r"^-\s*`?([SMTF]\d{2,3}[A-Za-z0-9]*?)(?:_src|_face)?\.png`?\s*$")
WORD = re.compile(r"[a-z][a-z'-]+")


def extract_prompts(text: str) -> dict[str, str]:
    prompts: dict[str, str] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = MARK.match(lines[i].strip())
        if m:
            sid = m.group(1)
            buf = []
            j = i + 1
            while j < len(lines):
                s = lines[j].strip()
                if MARK.match(s) or s.startswith("```"):
                    break
                if s:
                    buf.append(s)
                j += 1
            prompt = " ".join(buf)
            if len(prompt) >= 40:
                # first occurrence wins (later sections may re-list ids)
                prompts.setdefault(sid, prompt)
            i = j
        else:
            i += 1
    return prompts


def tokens(s: str) -> set[str]:
    return {w for w in WORD.findall(s.lower()) if w not in STOP and len(w) > 2}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--threshold", type=float, default=0.50)
    ap.add_argument("--min-tokens", type=int, default=6)
    ap.add_argument("--boilerplate-df", type=float, default=0.30,
                    help="drop tokens appearing in more than this fraction of prompts")
    ap.add_argument("--strict", action="store_true", help="generic prompts fail, not warn")
    ap.add_argument("--top", type=int, default=15, help="show worst N pairs")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    prompts = extract_prompts(text)
    if len(prompts) < 20:
        print(f"FAIL could not extract a prompt table (found {len(prompts)} rows) — "
              "check the file format or this parser")
        return 1

    tok = {k: tokens(v) for k, v in prompts.items()}
    df = Counter()
    for ts in tok.values():
        df.update(ts)
    n = len(tok)
    boiler = {w for w, c in df.items() if c / n > args.boilerplate_df}
    resid = {k: ts - boiler for k, ts in tok.items()}

    generic = [k for k, ts in resid.items() if len(ts) < args.min_tokens]

    pairs = []       # same-series (S~S, M~M): a viewer sees two near-identical cuts -> FAIL
    cross_pairs = [] # cross-series (S~M etc.): often an intentional still/motion twin -> WARN
    for a, b in combinations(sorted(resid), 2):
        ta, tb = resid[a], resid[b]
        if not ta or not tb:
            continue
        j = len(ta & tb) / len(ta | tb)
        if j >= args.threshold:
            rec = (j, a, b, sorted(ta & tb)[:8])
            (pairs if a[0] == b[0] else cross_pairs).append(rec)
    pairs.sort(reverse=True)
    cross_pairs.sort(reverse=True)

    print(f"info prompts extracted: {n} | boilerplate tokens dropped: {len(boiler)} "
          f"(df>{args.boilerplate_df:.0%})")
    if pairs:
        print(f"\nFAIL {len(pairs)} same-series near-duplicate pair(s) at Jaccard>={args.threshold}:")
        for j, a, b, shared in pairs[:args.top]:
            print(f"  {j:.2f}  {a} ~ {b}   shared: {', '.join(shared)}")
        if len(pairs) > args.top:
            print(f"  ... and {len(pairs) - args.top} more")
    else:
        print(f"ok   no same-series pair reaches Jaccard {args.threshold}")
    if cross_pairs:
        print(f"WARN {len(cross_pairs)} cross-series twin(s) (still/motion pairs are often "
              f"intentional — eyeball them):")
        for j, a, b, shared in cross_pairs[:args.top]:
            print(f"  {j:.2f}  {a} ~ {b}   shared: {', '.join(shared)}")
    if generic:
        tag = "FAIL" if args.strict else "WARN"
        print(f"{tag} {len(generic)} prompt(s) with <{args.min_tokens} distinctive tokens "
              f"(generic-filler risk): {', '.join(generic[:20])}")

    bad = bool(pairs) or (args.strict and bool(generic))
    print(f"\nRESULT: {'FAIL' if bad else 'PASS'} "
          f"({len(pairs)} dup-pairs, {len(generic)} generic)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
