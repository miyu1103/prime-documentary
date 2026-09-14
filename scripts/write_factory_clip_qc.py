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
    ap.add_argument("--revision", help="write this revision exactly (default: next free one)")
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
    # The STRONGEST evidence available, when it exists: check_pool_frames' per-clip review, in
    # which every staged clip was sampled across its OWN duration and signed for BY NAME. A sheet
    # tick clears twenty clips at once and a staging receipt clears a clip on its ledger title;
    # this clears exactly the clip a reviewer named. EP65 marmet had 138 such verdicts on disk
    # (121 sheets read as an index, 878 full-resolution frames reopened) and this file could not
    # see them, so visual_asset_qc reported 106 staged clips "NOT reviewed" while the review that
    # HAD looked at all 138 sat unread two directories away.
    pfr = verdicts.get("pool_frame_review") or {}
    pfr_reviewed = set(pfr.get("reviewed_clips") or [])
    pfr_accepted = set(pfr.get("accepted") or [])
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
        # A per-clip pool-frame verdict outranks both: it names THIS clip and it was written
        # after somebody looked at frames from across its own duration.
        in_pfr = p.name in pfr_reviewed
        reviewed = in_pfr or (row is not None) or looked
        why = rejected.get(p.name)
        # Named in the review but absent from its accepted list = looked at and NOT cleared.
        # That is a reject, whatever the staging receipt says its ledger title was.
        if in_pfr and not why and p.name not in pfr_accepted:
            why = "named in the per-clip pool-frame review and not in its accepted list"
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
            "evidence": (
                f"per-clip pool-frame review across the clip's own duration "
                f"({pfr.get('reviewer') or 'unrecorded reviewer'}, "
                f"{pfr.get('reviewed_at') or 'undated'}); receipt "
                f"runs/qc/{a.slug}_pool_frames.v001.json" if in_pfr
                else "archive ledger title match (stage_footage_by_title)" if row
                else "labelled contact sheet review"),
            "source": (row or {}).get("source"),
            "license": (row or {}).get("license"),
        })

    # CLAUDE invariant 6: an existing revision is never overwritten. Until now every run
    # clobbered v001 -- including a v001 that an acceptance receipt had already been written
    # against -- so the manifest could silently change under a receipt that cited it.
    ns = [int(t) for q in (ep / "05_visuals").glob("factory_clip_qc.v*.json")
          if (t := q.name.split(".v")[-1].split(".json")[0]).isdigit()]
    rev = a.revision or ("v%03d" % ((max(ns) + 1) if ns else 1))
    out = ep / "05_visuals" / f"factory_clip_qc.{rev}.json"
    if out.exists() and not a.revision:
        print(f"[clipqc] refusing to overwrite {out.name}")
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "schema_version": f"{a.slug}_factory_qc.v1",
        "episode_id": ep.name,
        "review_method": (
            (f"per-clip pool-frame review: {len(pfr_reviewed)} clip(s) signed for by "
             f"{pfr.get('reviewer') or 'an unrecorded reviewer'} on "
             f"{pfr.get('reviewed_at') or 'an unrecorded date'}, bound to pool_id_sha256="
             f"{str(pfr.get('pool_id_sha256'))[:16]}.. (check_pool_frames); " if pfr_reviewed else "")
            + "ledger-title selection + labelled contact sheets"
            f" ({len(sheets)} sheet(s) on disk)"),
        "pool_frame_review": {k: (len(v) if isinstance(v, list) else v) for k, v in pfr.items()},
        "clips": clips,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[clipqc] {a.slug}: {len(clips)} clip(s) recorded -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
