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


# Orders from EP72 onward write the plate list as a markdown table instead of a code fence:
#   | H001 | the beat | the prompt text | flags |
# The fence format above is the EP53-era shape. Measured 2026-08-21: with only the fence parser,
# BOTH EP72 lacmegantic and EP75 lahaina extracted 0 rows and this gate printed the same FAIL for a
# file-format reason rather than a diversity reason -- i.e. it had never once measured a modern
# order. Accept both shapes; the fence wins where a file carries both.
TABLE_ROW = re.compile(
    r"^\|\s*([A-Z]{1,2}\d{2,3}[A-Za-z0-9]*)\s*\|"   # id cell
    r"\s*[^|]*\|"                                   # beat cell (not a prompt)
    r"\s*([^|]+?)\s*\|"                             # prompt cell
)


def extract_table_prompts(text: str) -> dict[str, str]:
    """Plate prompts written as markdown table rows. Same contract as extract_prompts()."""
    out: dict[str, str] = {}
    for line in text.splitlines():
        m = TABLE_ROW.match(line.strip())
        if not m:
            continue
        sid, prompt = m.group(1), m.group(2).strip()
        if len(prompt) >= 40:
            out.setdefault(sid, prompt)
    return out


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
    ap.add_argument("--min-coverage", type=float, default=0.80,
                    help="fail if literal prompts cover less than this fraction of referenced asset ids")
    args = ap.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    prompts = extract_prompts(text) or extract_table_prompts(text)
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

    # --- RAW GATE (added 2026-08-21) ----------------------------------------
    # The boilerplate filter defeats the duplicate detector on exactly the input the
    # detector exists to catch. Demonstrated: an order of 30 IDENTICAL prompts scored
    # 0 dup-pairs and printed RESULT: PASS, because every shared token exceeded the 30%
    # document-frequency threshold and was therefore dropped as "boilerplate" -- leaving
    # nothing to compare. The same file with --boilerplate-df 1.1 returns 435 pairs at
    # Jaccard 1.00, so the detector is sound and the filter was blinding it.
    # So: also compare the UNFILTERED tokens at a deliberately high bar. Real plates that
    # share a style macro sit well under it; wholesale duplication cannot.
    RAW_THRESHOLD = 0.85
    raw_pairs = []
    for a, b in combinations(sorted(tok), 2):
        ta, tb = tok[a], tok[b]
        if not ta or not tb:
            continue
        j = len(ta & tb) / len(ta | tb)
        if j >= RAW_THRESHOLD:
            raw_pairs.append((j, a, b, sorted(ta & tb)[:8]))
    raw_pairs.sort(reverse=True)

    # --- COVERAGE GATE (added 2026-07-28) -----------------------------------
    # A file with only 30 literal prompts out of 261 declared assets used to
    # print "RESULT: PASS" -- a vacuous green, because the tool only ever
    # compared the prompts that EXIST. EP51 (36/180) and EP52 (30/261) both
    # passed that way, meaning Codex would have improvised ~87% of the imagery.
    # Coverage is now measured against every asset id the document references.
    ID_REF = re.compile(r"\b([SMTF])(\d{2,3})\b")
    referenced: dict[str, set[str]] = {}
    for pre, num in ID_REF.findall(text):
        referenced.setdefault(pre, set()).add(num)
    ref_total = sum(len(v) for v in referenced.values())
    coverage = (n / ref_total) if ref_total else 1.0
    if ref_total >= 20 and coverage < args.min_coverage:
        missing = ref_total - n
        print(f"FAIL prompt coverage {coverage:.0%}: {n} literal prompts for "
              f"{ref_total} referenced asset ids ({missing} would be improvised). "
              f"Per-asset literal prompts are mandatory -- a diversity PASS over a "
              f"fraction of the assets is a vacuous green.")
        print(f"\nRESULT: FAIL (coverage {coverage:.0%} < {args.min_coverage:.0%})")
        return 1
    if ref_total:
        print(f"ok   prompt coverage {coverage:.0%} ({n}/{ref_total} referenced asset ids)")

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
    if raw_pairs:
        print(f"\nFAIL {len(raw_pairs)} pair(s) near-identical BEFORE the boilerplate filter "
              f"(raw Jaccard>={RAW_THRESHOLD}) — the filter cannot hide these:")
        for j, a, b, shared in raw_pairs[:args.top]:
            print(f"  {j:.2f}  {a} ~ {b}   shared: {', '.join(shared)}")
        if len(raw_pairs) > args.top:
            print(f"  ... and {len(raw_pairs) - args.top} more")
    else:
        print(f"ok   no pair reaches raw Jaccard {RAW_THRESHOLD} before filtering")
    if generic:
        tag = "FAIL" if args.strict else "WARN"
        print(f"{tag} {len(generic)} prompt(s) with <{args.min_tokens} distinctive tokens "
              f"(generic-filler risk): {', '.join(generic[:20])}")

    bad = bool(pairs) or bool(raw_pairs) or (args.strict and bool(generic))
    print(f"\nRESULT: {'FAIL' if bad else 'PASS'} "
          f"({len(pairs)} dup-pairs, {len(raw_pairs)} raw-dup-pairs, {len(generic)} generic)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
