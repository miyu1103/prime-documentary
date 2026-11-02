#!/usr/bin/env python3
r"""Block every archive clip whose own LEDGER TITLE says it is AI-generated.

WHY. EP76's footage review put 101 candidates on contact sheets and two of them were synthetic --
`AR-pixabay_353278` ("ai generated, volcano, eruption, nature, lava") and `AR-v_366249` ("ai
generated, rain, loop, night, cobblestone street"). Both say "ai generated" IN THEIR OWN TITLE and
both still reached a human review sheet, so nothing upstream reads that label. Generated footage
may not be presented as an authentic record (CLAUDE.md invariant 11) and the archive rule bars it,
so the label is not advisory -- it is a hard exclusion that was never wired up.

WHY THE LEDGER AND NOT THE FILENAME. The first version of this script scanned filenames on
D:\pd-archive and found 76 clips -- and MISSED the two that started the whole thing, because they
live on E: and are named `pixabay__357485__id.mp4`. Their filename carries no title at all. The
title exists only in the ledger row, which is the same reason `stage_footage_by_title.py` exists
(`pd-factory-shelf-mislabeled`: the filename label is broken, the human-written title is not).
The blocklist id also comes from the ledger's `id` field, not from the filename, so a filename
scan produced ids the reader would never match. That is why this reads rows through
`stage_footage_by_title.ledger_rows()` rather than re-implementing the walk (invariant 14).

WHY GLOBAL, NOT episodes:["morandi"]. These are archive-wide ids naming one file each, not
per-episode plate numbers like V003, so a global row cannot silently remove a different picture
from a different film -- the hazard `pd_footage_blocklist.py` documents for scoped rows. And the
ban is not episode-specific: no PD episode may cut synthetic footage.

MEASURED BEFORE WRITING (2026-08-22): ZERO AI-labelled clips are cut into any built film in
data/*_film.json, so this row creates no new failure on existing work; it only closes the door.
Several would answer an ordinary documentary query -- `ai-generated-office-clutter-documents-
papers-workspace-chaos` is exactly what a search for office paperwork returns, in a film whose
subject IS paperwork.

The FILTER fix (catching the next one at ingest) is owned by another thread. This is a denylist of
what is on the shelf today, not a rule.

Usage:
    py -3.11 scripts/block_ai_generated_shelf_clips.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import stage_footage_by_title as sfbt  # noqa: E402

BLOCKLIST = ROOT / "config" / "footage_blocklist.v001.json"
LABEL = "ai_generated_synthetic_footage"
AI = re.compile(r"\bai[-_ ]generated\b", re.I)


def ai_ids() -> dict[str, str]:
    """{blocklist id: ledger title} for every row whose title declares itself AI-generated."""
    out: dict[str, str] = {}
    for r in sfbt.ledger_rows():
        title = str(r.get("title") or "")
        if not AI.search(title):
            continue
        src = Path(str(r.get("src") or r.get("path") or ""))
        ident = f"AR-{sfbt.slugify(str(r.get('id', src.stem)), 24)}"
        out[ident] = title[:96]
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    found = ai_ids()
    if not found:
        print("no ledger row declares itself ai-generated -- nothing to do")
        return 1

    # The two that started this must be in the set, or the id derivation is wrong again.
    must = {"AR-pixabay_353278", "AR-v_366249"}
    missing = must - set(found)
    if missing:
        print(f"FAIL: the two clips that reached a review sheet are not in the set: {missing}")
        print("      the id derivation does not match what the pipeline produces; not writing")
        return 1

    doc = json.loads(BLOCKLIST.read_text(encoding="utf-8"))
    before = len(doc["blocked"])
    doc["blocked"] = [r for r in doc["blocked"] if r.get("label") != LABEL]
    replaced = before - len(doc["blocked"])

    doc["blocked"].append({
        "ids": sorted(found),
        "label": LABEL,
        "reason": (
            "The clip's own archive-ledger title says 'ai generated'. Synthetic footage may not be "
            "cut into a PD episode (CLAUDE.md invariant 11: generated visuals are not evidence and "
            "must not be presented as authentic records). GLOBAL, not episode-scoped, because "
            "these are archive-wide file ids and the ban applies to every episode. Found by EP76's "
            "footage review when two of them reached a human contact sheet through the ordinary "
            f"candidate path; measured 2026-08-22 as {len(found)} ledger row(s), ZERO of which are "
            "cut into any built film. Read from the LEDGER, not from filenames: the two that "
            "started this are named `pixabay__357485__id.mp4` and carry no title on disk at all. "
            "This is a denylist of what is on the shelf today, NOT a rule that catches the next "
            "one ingested."),
        "hard_category": "cat4_wrong_subject_reads_as_the_claim",
    })

    print(f"{LABEL}: {len(found)} clip(s) (replaced {replaced} existing row)")
    for k in sorted(found)[:5]:
        print(f"   {k:<22} {found[k][:70]}")
    print(f"   ... and {max(0, len(found) - 5)} more")

    if a.dry_run:
        print("--dry-run: nothing written")
        return 0
    BLOCKLIST.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {BLOCKLIST}")

    import pd_footage_blocklist as fb  # noqa: PLC0415

    glob = fb.load_blocked(None)
    probes = [
        "AR-pixabay_353278__ai_generated_volcano_eruption_nature_lava_tropic.mp4",
        "AR-v_366249__ai_generated_rain_loop_night_cobblestone_street.mp4",
    ]
    ok = True
    print(f"reader: global ids now {len(glob)}")
    for p in probes:
        hit = fb.reason_for(p, glob)
        print(f"reader: {p.split('__')[0]:<22} -> {'BLOCKED' if hit else 'NOT BLOCKED -- BUG'}")
        ok = ok and bool(hit)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
