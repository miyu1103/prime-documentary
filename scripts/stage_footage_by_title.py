#!/usr/bin/env python
"""Stage episode footage by the archive ledger's TITLE, not by the filename's subtype label.

WHY THIS EXISTS (2026-07-30, EP51 visual QC): the factory shelf's filename labels are
pervasively wrong -- `AF-BG-23326__barbed_wire_fence_sky.mp4` is really "majestic texas
longhorns in rural pasture", `AF-BG-18181__evidence_bag.mp4` is a close-up of a child's face.
Every selector we had picked by that label, which is why serious documentaries kept getting
cartoon gravestones and pastel office desks (pd-factory-shelf-mislabeled). The ledger row,
however, carries the REAL human-written title. Selecting on the title -- and re-naming the
staged copy after it -- makes the mislabelling structurally unable to reach a film, and makes
the contact sheet readable, because the caption under each tile is now the truth.

    python scripts/stage_footage_by_title.py --slug willingham \
        --query "house fire" --query "prison cell" --per-query 4 [--dry-run]

Writes remotion/public/<slug>/factory/AR-<id>__<title-slug>.mp4 plus a staging receipt.
Read-only against the shelf: files are COPIED, never moved or edited.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER_DIR = Path(r"H:\pd-media\assets\archive\_ledger")
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}
OK_LICENSE = {"free_commercial", "pd", "cc0"}
# titles that read as stock-cheap or plainly wrong for a documentary, whatever they matched
TITLE_BLOCK = re.compile(
    r"\b(cartoon|3d render|3d animation|animated character|christmas|halloween|santa|"
    r"emoji|meme|logo|template|mockup|game|anime|toy car|funny)\b", re.I)
# Names left behind by YouTube-ripping sites. Hyphen, underscore and space all appear, because
# the identifier is slugified at different points by different tools.
RIP_SIGNATURE = re.compile(
    r"y[-_ ]?2mate|ytmp3|savefrom|ss[-_ ]?youtube|9convert|yt1s|snaptube|x2mate|"
    r"onlinevideoconverter|tubemate|4k[-_ ]?download|ytdlp|youtube[-_ ]?dl", re.I)


def slugify(text: str, limit: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return (s[:limit].rstrip("_")) or "untitled"


def ledger_rows():
    for fn in sorted(os.listdir(LEDGER_DIR)):
        if not fn.endswith(".jsonl") or fn.startswith("rejects") or fn.endswith(
                ("_dedup_removed.jsonl", "_candidates.jsonl")):
            continue
        with open(LEDGER_DIR / fn, encoding="utf-8") as f:
            for line in f:
                try:
                    yield json.loads(line)
                except Exception:
                    continue


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--query", action="append", required=True,
                    help="title terms, ANDed; repeat the flag for more queries")
    ap.add_argument("--per-query", type=int, default=4)
    ap.add_argument("--min-mb", type=float, default=1.0)
    ap.add_argument("--max-mb", type=float, default=120.0)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    dest = ROOT / "remotion" / "public" / a.slug / "factory"
    dest.mkdir(parents=True, exist_ok=True)
    have = {p.name for p in dest.glob("*.mp4")}
    have_ids = {n.split("__")[0] for n in have}

    # CROSS-EPISODE DE-DUP (EP51 acceptance, 2026-07-30: 143 of 263 cuts were clips this
    # episode shared with morton/flowers, i.e. the owner's 「素材の被り」 measured). The same
    # top-N title match was handed to every episode because staging looked only at ITS OWN
    # folder. Anything already staged for another episode is off the table here.
    # `factory*` on purpose: factory_rejected / factory_pruned_offtopic / factory_offtopic hold
    # clips a human already looked at and threw out. Globbing only `factory` re-staged them the
    # moment a pool was topped up (EP57 fieldtest, 2026-08-02) -- a rejected clip must stay dead
    # for every episode, not come back through the next query.
    for other in sorted((ROOT / "remotion" / "public").glob("*/factory*")):
        if other.parent.name == a.slug and other.name == "factory":
            continue
        for q in other.glob("*.mp4"):
            have_ids.add(q.name.split("__")[0])
    print(f"[stage] {len(have_ids)} clip id(s) already used by this or another episode -- excluded")

    rows = [r for r in ledger_rows()
            if Path(str(r.get("file_path", ""))).suffix.lower() in VIDEO_EXT
            and r.get("license_decision") in OK_LICENSE]
    print(f"[stage] ledger videos with a usable licence: {len(rows)}")

    staged, receipt = 0, []
    for q in a.query:
        terms = [t.lower() for t in q.split()]
        picked = 0
        for r in rows:
            if picked >= a.per_query:
                break
            title = str(r.get("title", "")).strip()
            if not title or TITLE_BLOCK.search(title):
                continue
            # A RIPPED UPLOAD ANNOUNCES ITSELF IN ITS OWN NAME. The signature lives in the
            # archive.org identifier, not the title, so TITLE_BLOCK never sees it -- and the
            # licence filter cannot help, because the tag is whatever the uploader typed.
            if RIP_SIGNATURE.search(f"{r.get('id', '')} {r.get('file_path', '')} {title}"):
                print(f"  RIGHTS: refusing {title[:60]!r} -- its name says it was ripped from "
                      f"YouTube; a CC0 tag on archive.org is the uploader's word, not proof")
                continue
            if not all(t in title.lower() for t in terms):
                continue
            src = Path(str(r.get("file_path", "")))
            mb = float(r.get("bytes", 0)) / 1e6
            if not src.exists() or not (a.min_mb <= mb <= a.max_mb):
                continue
            ident = f"AR-{slugify(str(r.get('id', src.stem)), 24)}"
            if ident in have_ids:
                continue
            name = f"{ident}__{slugify(title)}{src.suffix.lower()}"
            if name in have:
                continue
            receipt.append({"query": q, "id": ident, "title": title, "source": r.get("source"),
                            "license": r.get("license_decision"), "src": str(src), "staged_as": name})
            have.add(name); have_ids.add(ident); picked += 1; staged += 1
            if not a.dry_run:
                shutil.copy2(src, dest / name)
        print(f"  {q!r:38} -> {picked} clip(s)")

    print(f"[stage] {staged} clip(s) {'would be ' if a.dry_run else ''}staged into {dest}")
    if not a.dry_run and receipt:
        out = ROOT / "runs" / "qc" / f"{a.slug}_title_staging.v001.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"slug": a.slug, "staged": receipt}, ensure_ascii=False, indent=1),
                       encoding="utf-8")
        print(f"[stage] receipt {out}")
    print("[stage] NEXT: build a labelled contact sheet and look at every tile before rendering.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
