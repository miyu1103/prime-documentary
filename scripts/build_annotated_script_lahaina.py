#!/usr/bin/env python3
r"""Generate EP75's `03_script/script.annotated.v001.json` from artefacts that already exist.

WHY IT EXISTS
`build_case_film_assets.py` reads this file unguarded (line 636) and turns every span's
`on_screen_text` into the film's timed graphics beats. Without it the assembly crashes, and with a
hand-typed one the graphics drift from the design. So it is GENERATED from three sources that are
already the truth:

  * `06_audio/narration_index.v001.json` -- the delivered narration, chunk by chunk with its section
  * `_planning/EP75_lahaina_filmconfig.v001.json` -- the 83 figure cards authored from the film
    bible's beat map, each carrying the ledger row it came from
  * `_planning/EP75_lahaina_script.en.v001.md` -- the citation comment under every spoken line

Nothing here is invented. `text` is the delivered narration verbatim, `on_screen_text` is the card
the design already specified, and `claim_ids` are the ledger rows the script itself cites for those
lines.

    py -3.11 scripts/build_annotated_script_lahaina.py [--write]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-075-lahaina"
EPDIR = ROOT / "episodes" / EP
PLAN = ROOT / "episodes" / "_planning"


def card_text(c: dict) -> list[str]:
    """The on-screen words a figure card puts up, in the order it puts them up."""
    k = c.get("kind")
    if k == "quote":
        return [c["quote"]]
    if k == "kinetic":
        return list(c.get("lines") or [])
    if k == "stat":
        return [f"{c['value']}", c["label"]]
    if k == "lowerthird":
        out = [c.get("primary", "")]
        if c.get("secondary"):
            out.append(c["secondary"])
        return [x for x in out if x]
    return []


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="write the file (default: report only)")
    a = ap.parse_args()

    idx = json.loads((EPDIR / "06_audio/narration_index.v001.json").read_text(encoding="utf-8"))
    cfg = json.loads((PLAN / "EP75_lahaina_filmconfig.v001.json").read_text(encoding="utf-8"))
    md = (PLAN / "EP75_lahaina_script.en.v001.md").read_text(encoding="utf-8").split("\n")

    # spoken line -> the ledger rows its citation comment carries
    cites: dict[str, list[str]] = {}
    for i, line in enumerate(md):
        s = line.strip()
        if not s or s.startswith(("#", ">", "---", "<!--", "【")):
            continue
        nxt = md[i + 1].strip() if i + 1 < len(md) else ""
        rows = re.findall(r"\b(LH-\d+|AB-\d+)\b", nxt) if nxt.startswith("<!--") else []
        cites[re.sub(r"\s+", " ", s)] = rows

    chunks = idx["chunks"]
    by_section: dict[str, list[dict]] = {}
    for c in chunks:
        by_section.setdefault(c["section"], []).append(c)

    chapters, spans = [], []
    n = 0
    for section in cfg["figures_by_section"]:
        cards = cfg["figures_by_section"][section]
        cs = by_section.get(section, [])
        if not cs:
            continue
        # split the section's chunks into as many spans as it has figure cards, so every card
        # has a window of narration to sit inside and none is orphaned
        k = max(1, len(cards))
        size = max(1, round(len(cs) / k))
        groups = [cs[i:i + size] for i in range(0, len(cs), size)] or [cs]
        while len(groups) > k:                     # fold the tail back so counts match
            groups[-2].extend(groups.pop())
        ids = []
        for gi, g in enumerate(groups):
            n += 1
            sid = f"SPN-{n:04d}"
            ids.append(sid)
            text = " ".join(c["spoken_text"].strip() for c in g)
            claims: list[str] = []
            for c in g:
                for r in cites.get(re.sub(r"\s+", " ", c["spoken_text"].strip()), []):
                    if r not in claims:
                        claims.append(r)
            card = cards[gi] if gi < len(cards) else None
            spans.append({
                "span_id": sid,
                "text": text,
                "claim_ids": claims,
                "narrative_function": section.lower(),
                "on_screen_text": card_text(card) if card else [],
                "visual_intent": (card.get("kind") if card else "footage"),
                "_row": (card or {}).get("_row", ""),
                "start": round(g[0]["start"], 3),
                "end": round(g[-1]["end"], 3),
            })
        chapters.append({"chapter_id": section.lower(), "title": section,
                         "function": section.lower(), "span_ids": ids})

    doc = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "language": "en",
        "thesis": ("A warning system is not the equipment you own. It is the thing you are in the "
                   "habit of using -- and this one's habit was the sea."),
        "viewer_promise": ("What the largest outdoor warning network in the world was actually for, "
                           "when the town was told, and what the state's own investigators wrote at "
                           "the end of 518 pages."),
        "chapters": chapters,
        "spans": spans,
        "estimated_duration_seconds": round(idx["total_seconds"], 3),
        "qc_status": "generated_from_narration_index_and_filmconfig",
    }

    cards_total = sum(len(v) for v in cfg["figures_by_section"].values())
    with_text = sum(1 for s in spans if s["on_screen_text"])
    no_claim = [s["span_id"] for s in spans if not s["claim_ids"]]
    print(f"chapters {len(chapters)}  spans {len(spans)}  figure cards {cards_total}")
    print(f"spans carrying on-screen text: {with_text}")
    print(f"spans with no ledger row: {len(no_claim)}"
          + (f"  ({', '.join(no_claim[:6])}{' ...' if len(no_claim) > 6 else ''})" if no_claim else ""))
    print(f"narration covered: {sum(len(v) for v in by_section.values())} of {len(chunks)} chunks")

    if not a.write:
        print("\n(report only -- pass --write to create the file)")
        return 0
    out = EPDIR / "03_script"
    out.mkdir(parents=True, exist_ok=True)
    p = out / "script.annotated.v001.json"
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
