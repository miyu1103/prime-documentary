#!/usr/bin/env python3
"""One record per shelf file answering "can I put this in a film, and what do I owe for it?"

WHY THIS EXISTS
---------------
The answer was spread across five files that never met: the ledger knew the licence, the
resolution index knew 4K from 320x240, the vertical index knew whether the subject survives a
9:16 crop, the semantic index knew whether the clip is findable at all, and nobody recorded
whether a human had ever looked at the pixels. An editor picking a clip had to open none of them,
so in practice they opened none of them -- which is how `evidence_bag` returned cartoons and how
a Blu-ray remux of a 1964 feature sat in the shelf marked usable.

This joins them and writes ONE line per file. `--path` prints that line as a checklist.

WHAT EACH FIELD MEANS -- and what it does NOT mean -- is in
`docs/PD_ASSET_USABILITY_CHECKLIST.v001.md`. Read it once before trusting a green field.

    py -3.11 scripts/build_asset_usability.py                       # rebuild the whole record
    py -3.11 scripts/build_asset_usability.py --path <file>         # checklist for one asset
    py -3.11 scripts/build_asset_usability.py --summary             # counts only, no rebuild
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_archive_sources import LEDGER_DIR  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs" / "asset_usability.v001.jsonl"
RES_INDEX = Path(LEDGER_DIR) / "video_resolution.json"
VERT_INDEX = Path(r"E:\pd-media\assets\archive\_qc\vertical_index.jsonl")
SEM_PATHS = ROOT / "runs" / "footage_semantic" / "paths.json"

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}
AUDIO_EXT = {".mp3", ".wav", ".flac", ".m4a", ".ogg", ".aac"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}

# A licence that permits commercial use with no attribution obligation.
CLEAR_DECISIONS = {"pd", "cc0", "free_commercial"}


def kind_of(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    if ext in IMAGE_EXT:
        return "image"
    return "other"


def load_side_indexes() -> tuple[dict, dict, set]:
    res = json.loads(RES_INDEX.read_text("utf-8")) if RES_INDEX.exists() else {}
    vert: dict[str, dict] = {}
    if VERT_INDEX.exists():
        for line in VERT_INDEX.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("file_path"):
                vert[r["file_path"]] = r
    sem = set(json.loads(SEM_PATHS.read_text("utf-8"))) if SEM_PATHS.exists() else set()
    return res, vert, sem


def ledger_rows():
    for f in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("file_path"):
                yield r


def classify(row: dict, res: dict, vert: dict, sem: set) -> dict:
    path = row["file_path"]
    kind = kind_of(path)
    decision = row.get("license_decision")
    verdict = row.get("rights_verdict")

    # --- rights -------------------------------------------------------------------------
    if verdict == "reject":
        rights, why = "blocked", row.get("reindex_note") or "examined and refused"
    elif decision in CLEAR_DECISIONS:
        rights, why = "clear", row.get("reindex_note") or f"license_decision={decision}"
    else:
        rights, why = "hold", (row.get("reindex_basis")
                               or "never examined -- no licence recorded")

    # --- technical ----------------------------------------------------------------------
    tech: dict = {}
    rk = f"{row.get('source')}:{row.get('id')}"
    wh = res.get(rk)
    if wh:
        tech["w"], tech["h"] = wh.get("w"), wh.get("h")
        tech["hd"] = bool(wh.get("h") and wh["h"] >= 720)
    v = vert.get(path)
    if v:
        tech["centre_energy"] = v.get("centre_energy")
        tech["motion"] = v.get("motion")
        tech["luma_crop"] = v.get("luma_crop")
    tech["mb"] = round((row.get("bytes") or 0) / 1e6, 1)
    tech["searchable"] = path in sem

    # --- what nobody has checked --------------------------------------------------------
    # There is no shelf-wide record of a human having looked at an archive clip. Episode
    # plates have `runs/qc/<slug>_plate_verdicts.v001.json`; the shelf has nothing. Saying
    # so in every row is the point: a false green here is worse than an admitted blank.
    gaps = []
    if kind == "video" and "w" not in tech:
        gaps.append("resolution unmeasured")
    if kind == "video" and not v:
        gaps.append("framing/motion unmeasured")
    if kind == "video" and not tech["searchable"]:
        gaps.append("not in the semantic index -- a search will never surface it")
    gaps.append("no human has confirmed the content matches the label")
    gaps.append("no check for a watermark, a logo or an identifiable real face")

    return {"path": path, "kind": kind, "source": row.get("source"), "id": row.get("id"),
            "title": row.get("title"), "theme": row.get("theme"),
            "rights": rights, "rights_basis": str(why)[:200],
            "license_decision": decision, "rights_verdict": verdict,
            "tech": tech, "unchecked": gaps}


def print_checklist(rec: dict) -> None:
    mark = {"clear": "USABLE", "hold": "HOLD", "blocked": "DO NOT USE"}[rec["rights"]]
    print(f"\n{rec['path']}")
    print(f"  {rec['title']}")
    print(f"\n  RIGHTS      {mark}")
    print(f"              {rec['rights_basis']}")
    print(f"              source={rec['source']} decision={rec['license_decision']}"
          f" verdict={rec['rights_verdict']}")
    t = rec["tech"]
    print(f"\n  TECHNICAL   kind={rec['kind']}  {t.get('mb')} MB")
    if "w" in t:
        print(f"              {t['w']}x{t['h']}  {'HD or better' if t.get('hd') else 'BELOW 720p'}")
    if "motion" in t:
        print(f"              motion={t['motion']}  centre_energy={t['centre_energy']}"
              f"  luma_crop={t['luma_crop']}")
    print(f"              in semantic search: {t.get('searchable')}")
    print("\n  NOT CHECKED (a person must):")
    for g in rec["unchecked"]:
        print(f"              - {g}")
    print()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", help="print the checklist for one asset (reads the built record)")
    ap.add_argument("--summary", action="store_true", help="counts from the built record")
    args = ap.parse_args()

    if args.path or args.summary:
        if not OUT.exists():
            sys.exit(f"{OUT.relative_to(ROOT)} does not exist yet -- run without --path first")
        if args.path:
            want = os.path.normcase(os.path.abspath(args.path))
            for line in OUT.open(encoding="utf-8"):
                rec = json.loads(line)
                if os.path.normcase(rec["path"]) == want or args.path in rec["path"]:
                    print_checklist(rec)
                    return 0
            sys.exit("no record for that path")
        tally = collections.Counter()
        for line in OUT.open(encoding="utf-8"):
            rec = json.loads(line)
            tally[(rec["kind"], rec["rights"])] += 1
        for (kind, rights), n in sorted(tally.items()):
            print(f"  {kind:6s} {rights:8s} {n:7d}")
        return 0

    res, vert, sem = load_side_indexes()
    print(f"side indexes: resolution={len(res)} vertical={len(vert)} semantic={len(sem)}")
    tally: collections.Counter = collections.Counter()
    tmp = str(OUT) + ".tmp"
    n = 0
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        for row in ledger_rows():
            rec = classify(row, res, vert, sem)
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            tally[(rec["kind"], rec["rights"])] += 1
            n += 1
    os.replace(tmp, OUT)
    print(f"wrote {OUT.relative_to(ROOT)}  ({n} assets)\n")
    for (kind, rights), c in sorted(tally.items()):
        print(f"  {kind:6s} {rights:8s} {c:7d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
