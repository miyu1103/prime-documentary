#!/usr/bin/env python3
"""Turn a PD markdown script into the `script.annotated.vNNN.json` the pipeline actually asks for.

PD_ONE_PASS_PRODUCTION_SPEC.v3 section 5 item 1 requires `EPnn_FILM_BIBLE.vNNN.md` **plus
`script.annotated.vNNN`**. Every episode since EP66 has produced the first and, in practice, a
markdown script instead of the second -- narration lines each followed by an HTML comment carrying
their ledger row ids. That markdown is readable by people and by check_script_craft, and invisible
to everything that wants spans.

The cost is recorded in the manual itself. `script_structure` has run 0 times and skipped 8 across
32 episodes, and v3 section 2.4 names the reason: it "looks for an annotated script under 03_script,
which does not exist because the script lives on the media root. Never once executed." A check that
has never executed is decoration. `verify_script_lint` degrades the same way: it finds a
`03_script/script.en.v*.md` but extracts only `[VO:]` lines, which PD scripts do not use, so it
reports "script artifact absent -- skipped honestly" on a script that is right there.

This converts one into the other. Narration lines become spans; the HTML comment beneath each line
becomes that span's `claim_ids`; the `## ` headings become `section`; direction blocks, headings,
tables, blockquotes and front matter are dropped, because a span is what is SPOKEN.

    py -3.11 scripts/build_annotated_script.py --script episodes/_planning/EP74_itaewon_script.en.v006.md
    py -3.11 scripts/build_annotated_script.py --script <path> --out <path> --dry-run

Writes nothing without --out or an inferable episode directory, and never overwrites without
--force.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"(?:IT|LM|[A-Z]{2})-\d+[a-z]?|AB-\d+|⛔-\d+")
SKIP_PREFIX = ("#", "|", ">", "---", "<!--", "【", "*", "```", "- ", "1.", "2.", "3.", "4.", "5.")
DIRECTION = re.compile(r"^[A-Z0-9 .,:;/&()\x27-]+$")


def build(md_path: Path) -> dict:
    lines = md_path.read_text(encoding="utf-8").split("\n")
    body = next((i for i, l in enumerate(lines) if l.startswith("## ")), 0)

    spans, section, order = [], None, 0
    for i, line in enumerate(lines):
        if line.startswith("## "):
            section = line[3:].split("—")[0].split("--")[0].strip()
            continue
        s = line.strip()
        if i < body or not s or s.startswith(SKIP_PREFIX) or DIRECTION.match(s):
            continue
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        ids = sorted(set(ID.findall(nxt))) if nxt.startswith("<!--") else []
        order += 1
        spans.append({
            "span_id": f"SPN-{order:04d}",
            "section": section,
            "line": i + 1,
            "text": s,
            "claim_ids": ids,
        })

    return {
        "schema_version": "pd_script_annotated.v1",
        "source": str(md_path.resolve().relative_to(ROOT)).replace("\\", "/"),
        "generated_by": "scripts/build_annotated_script.py",
        "span_count": len(spans),
        "word_count": sum(len(sp["text"].split()) for sp in spans),
        "sections": sorted({sp["section"] for sp in spans if sp["section"]}),
        "spans_without_claim_ids": [sp["span_id"] for sp in spans if not sp["claim_ids"]],
        "spans": spans,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    md = Path(a.script)
    if not md.is_file():
        print(f"no such script: {md}")
        return 1
    data = build(md)

    if a.out:
        out = Path(a.out)
    else:
        m = re.match(r"EP\d+_([a-z0-9]+)_script\.en\.(v\d+)\.md$", md.name)
        if not m:
            print("cannot infer an output path from that filename; pass --out")
            return 1
        slug, rev = m.groups()
        cands = list((ROOT / "episodes").glob(f"PD-*-{slug}"))
        if len(cands) != 1:
            print(f"cannot infer the episode directory for slug {slug!r}; pass --out")
            return 1
        out = cands[0] / "03_script" / f"script.annotated.{rev}.json"

    print(f"{md.name} -> {data['span_count']} spans, {data['word_count']} words, "
          f"sections {data['sections']}")
    if data["spans_without_claim_ids"]:
        print(f"  {len(data['spans_without_claim_ids'])} span(s) carry no claim id: "
              f"{', '.join(data['spans_without_claim_ids'][:8])}")
    else:
        print("  every span carries at least one claim id")

    if a.dry_run:
        print(f"  --dry-run: would write {out}")
        return 0
    if out.exists() and not a.force:
        print(f"  refusing to overwrite {out} without --force")
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(out)
    print(f"  wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
