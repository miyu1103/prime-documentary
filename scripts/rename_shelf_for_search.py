#!/usr/bin/env python3
r"""Give shelf files names you can search, using the titles the ledger already holds.

WHY. Staging finds footage by matching the FILENAME -- `stage_footage_by_title.py` reads the
title and nothing else, and the theme field is invisible to it. Measured 2026-08-23: 5,638
files on the shelf are named `pixabay__<id>__id.mp4`. The slug is the literal string "id",
because that is what the Pixabay browse tree carried. Those clips cannot be found by any
search anyone would type, so for practical purposes they are not on the shelf at all.

The titles exist. The ledger row for `pixabay__359377__id.mp4` reads "cave, view, nature,
rocks, geology, moss, cliff, adventure, person, waves". That is the searchable text, sitting
one field away from the name.

WHAT IT REFUSES TO RENAME, and why each refusal is real:

  * anything referenced anywhere in the repo. 281 references live in runs/qc/ staging and
    prestage records; oroville and itaewon both staged clips by name and the long-form lane
    is still building from them. Renaming a staged clip breaks a build in another lane, and
    the record of which clip a human approved stops pointing at anything.
  * anything whose title has fewer than two meaningful words. `freesound__254070__141103-002`
    has a title of "141103 002 mp3"; renaming that produces a different unsearchable name.
  * anything whose new name already exists on disk.

HOW IT STAYS SAFE. The file is renamed first and the ledger row is rewritten only if that
succeeded, so a failure leaves the pair consistent rather than half-applied. The ledger is
rewritten once per source through a temp file and an atomic replace. Run it with the source's
recovery lane STOPPED -- a lane appending during the rewrite would lose the rows it wrote.

    py -3.11 scripts/rename_shelf_for_search.py                 # dry run
    py -3.11 scripts/rename_shelf_for_search.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER_DIR = Path(r"E:\pd-archive\_ledger")
SCAN_EXT = {".json", ".jsonl", ".ts", ".md", ".py", ".txt"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}

STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "at", "for", "with", "from",
    "by", "as", "is", "are", "was", "were", "that", "this", "it", "its", "he", "she",
    "they", "we", "you", "i", "be", "been", "有", "無",
}


def slugify(title: str, limit: int = 60) -> str:
    """Lower-case hyphenated words from the title, stop-words and duplicates dropped.

    Pixabay titles are comma-separated tag lists, so order carries no meaning and the first
    few tags are the subject. Keeping them in order and cutting at a length that leaves the
    whole path inside Windows' 260-character limit.
    """
    words = re.findall(r"[a-z0-9]+", title.lower())
    out: list[str] = []
    seen: set[str] = set()
    for w in words:
        if len(w) < 3 or w in STOP or w in seen:
            continue
        seen.add(w)
        out.append(w)
        if len("-".join(out)) >= limit:
            break
    return "-".join(out)[:limit].strip("-")


def referenced_names() -> set[str]:
    """Every shelf filename mentioned anywhere in the repo."""
    pat = re.compile(r"[A-Za-z0-9_]+__[0-9]+__[A-Za-z0-9_\-]+\.[a-z0-9]{2,4}")
    names: set[str] = set()
    for p in ROOT.rglob("*"):
        if p.suffix.lower() not in SCAN_EXT or not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if "__" not in text:
            continue
        names.update(pat.findall(text))
    return names


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write (default: dry run)")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    print("scanning the repo for filenames that must not move ...", flush=True)
    protected = referenced_names()
    print(f"  {len(protected)} filename(s) referenced somewhere in the repo")

    renamed = skipped_ref = skipped_thin = skipped_missing = skipped_clash = failed = 0
    for ledger in sorted(LEDGER_DIR.glob("*.jsonl")):
        if ledger.name.startswith("rejects"):
            continue
        rows: list[dict] = []
        torn = 0
        for line in ledger.open(encoding="utf-8", errors="replace"):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:  # noqa: BLE001
                torn += 1
        if torn:
            print(f"  {ledger.name}: {torn} torn line(s) -- REFUSING, repair the ledger first")
            return 1

        changed = 0
        for rec in rows:
            fp = rec.get("file_path")
            if not fp:
                continue
            src = Path(fp)
            if not src.stem.endswith("__id"):
                continue
            if src.name in protected:
                skipped_ref += 1
                continue
            slug = slugify(str(rec.get("title", "")))
            if len(slug.split("-")) < 2:
                skipped_thin += 1
                continue
            dst = src.with_name(f"{src.stem[:-4]}__{slug}{src.suffix}")
            if not src.exists():
                skipped_missing += 1
                continue
            if dst.exists():
                skipped_clash += 1
                continue
            if a.apply:
                try:
                    src.rename(dst)
                except OSError as e:
                    print(f"  FAILED {src.name}: {e}")
                    failed += 1
                    continue
                rec["file_path"] = str(dst)
                changed += 1
            renamed += 1
            if a.limit and renamed >= a.limit:
                break

        if a.apply and changed:
            tmp = ledger.with_suffix(".jsonl.rename_tmp")
            with tmp.open("w", encoding="utf-8") as fh:
                for rec in rows:
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            tmp.replace(ledger)
            print(f"  {ledger.name}: {changed} row(s) rewritten")
        if a.limit and renamed >= a.limit:
            break

    verb = "renamed" if a.apply else "would rename"
    print(f"\n{verb} {renamed}")
    print(f"  skipped, referenced in the repo : {skipped_ref}")
    print(f"  skipped, title too thin         : {skipped_thin}")
    print(f"  skipped, file not on disk       : {skipped_missing}")
    print(f"  skipped, target name taken      : {skipped_clash}")
    if failed:
        print(f"  FAILED                          : {failed}")
    if not a.apply:
        print("\n(dry run -- nothing moved; add --apply)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
