#!/usr/bin/env python
"""Record the per-clip QC evidence visual_asset_qc asks for.

The check refuses a pool whose clips were never reviewed, because the shelf's filenames lie.
Clips staged by stage_footage_by_title are different: they are selected on the archive ledger's
human-written TITLE and renamed after it, and the staging receipt keeps the title, source and
licence for each one. This writes that evidence into the manifest the check reads, and marks
shelf clips (AF-BG-*) as reviewed only when a contact sheet for the episode exists on disk.

    python scripts/write_factory_clip_qc.py --slug norfolk
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()

    pool = ROOT / "remotion" / "public" / a.slug / "factory"
    if not pool.is_dir():
        print(f"[clipqc] no pool for {a.slug}")
        return 0
    ep_dirs = sorted((ROOT / "episodes").glob(f"PD-*-{a.slug}"))
    if not ep_dirs:
        print(f"[clipqc] no episode dir for {a.slug}")
        return 0
    ep = ep_dirs[0]

    titles: dict[str, dict] = {}
    receipt = ROOT / "runs" / "qc" / f"{a.slug}_title_staging.v001.json"
    if receipt.is_file():
        for row in json.loads(receipt.read_text(encoding="utf-8")).get("staged", []):
            titles[row["staged_as"]] = row

    sheets = sorted((ROOT / "runs" / "qc").glob(f"*{a.slug}*/*.png"))
    sheets += sorted((ROOT / "runs" / "qc").glob(f"*{a.slug}*.png"))
    # A per-clip verdict file, written by whoever actually LOOKED at the sheets:
    #   {"rejected": {"AF-BG-26319__ambulance_lights_at_night.mp4": "why", ...},
    #    "reviewed_sheets": ["runs/qc/flowers_factory/factory_footage_contact_01.png", ...]}
    # Without it, shelf clips are recorded as NOT reviewed. Before 2026-08-02 this script
    # stamped every clip reviewed/on_theme/accept unconditionally -- `sheets` was computed and
    # then used only to print a count -- so visual_asset_qc passed on evidence that did not
    # exist. EP54s pool was 76 broken-label shelf clips deep in modern ambulances, a Japanese
    # house and a corporate finance office, in a 1996 Mississippi story, and the gate was green.
    verdicts_path = ROOT / "runs" / "qc" / f"{a.slug}_clip_verdicts.v001.json"
    verdicts = json.loads(verdicts_path.read_text(encoding="utf-8")) if verdicts_path.is_file() else {}
    rejected = verdicts.get("rejected", {})
    reviewed_sheets = verdicts.get("reviewed_sheets", [])
    TILES_PER_SHEET = 20   # build_footage_contact_sheet.py tiles 5 x 4
    clips = []
    for idx, p in enumerate(sorted(pool.glob("*.mp4"))):
        row = titles.get(p.name)
        shelf = p.name.startswith("AF-")
        # A ledger-title clip carries its own evidence: it was selected on a human-written
        # title and the staging receipt kept that title, source and licence. A shelf clip
        # carries a filename that may be a lie, so it counts as reviewed ONLY if someone
        # recorded a verdict for this pool.
        # Which contact sheet is this clip on? build_footage_contact_sheet tiles the pool in
        # sorted order, 20 per sheet, so sheet number is derived, not declared. A clip counts as
        # looked at only if ITS sheet is in reviewed_sheets -- listing all 11 sheets while having
        # opened four of them is the same false green this file was just fixed for.
        sheet_no = idx // TILES_PER_SHEET + 1
        looked = any(f"_{sheet_no:02d}.png" in s for s in reviewed_sheets)
        # Evidence is evidence regardless of prefix. An AR-* clip staged WITHOUT a receipt row
        # has exactly as much backing as a shelf clip: none. The first version of this rule let
        # those through on the filename alone, which is the same mistake in a different coat --
        # EP57s gate had already named 44 unreviewed AR-* clips (a futuristic lab, a Shenzhen
        # highway, a robot arm) in a roadside-drug-test film.
        reviewed = (row is not None) or looked
        why = rejected.get(p.name)
        clips.append({
            "filename": p.name,
            "asset_id": p.name.split("__")[0],
            "public_path": f"{a.slug}/factory/{p.name}",
            "reviewed": reviewed,
            "on_theme": reviewed and not why,
            "verdict": "reject" if why else ("accept" if reviewed else "unreviewed"),
            "reject_reason": why,
            "observed_content": (row or {}).get("title")
            or p.stem.split("__", 1)[-1].replace("_", " "),
            "evidence": ("archive ledger title match (stage_footage_by_title)" if row
                         else "labelled contact sheet review"),
            "source": (row or {}).get("source"),
            "license": (row or {}).get("license"),
        })

    out = ep / "05_visuals" / f"factory_clip_qc.v001.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "schema_version": f"{a.slug}_factory_qc.v1",
        "episode_id": ep.name,
        "review_method": ("ledger-title selection + labelled contact sheets"
                          f" ({len(sheets)} sheet(s) on disk)"),
        "clips": clips,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[clipqc] {a.slug}: {len(clips)} clip(s) recorded -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
