#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rename the factory shelf from the download query to the provider's real title.

The 88,740 files on the older factory shelf are named after the SEARCH QUERY that fetched
them, which is why `AF-BG-6237__courthouse_steps.mp4` is a university campus and
`AF-TEX-0005__grunge_texture_dark.jpg` is a school chalkboard. That naming is what the
"labels are broken" finding has always been about.

The truth was never lost: factory.jsonl carries the provider's own title for all 88,740
rows. So this is not a guess-and-relabel job, it is copying a value that already exists
into the filename, bringing the shelf into line with CONTRACT 4b:

    <source>__<id>__<real-title-slug>.<ext>

Both halves move together or neither does: the file is renamed and the ledger's file_path
is rewritten in the same pass, then the ledger is written atomically via a temp file. A
crash mid-run leaves renamed files and a stale ledger, so the run records progress to
`factory_rename.progress.jsonl` and can resume.

    python scripts/rename_factory_to_real_titles.py            # dry run
    python scripts/rename_factory_to_real_titles.py --apply
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEDGER_DIR = r"H:\pd-media\assets\archive\_ledger"
FACTORY = os.path.join(LEDGER_DIR, "factory.jsonl")
PROGRESS = os.path.join(LEDGER_DIR, "factory_rename.progress.jsonl")


def slug(text: str, limit: int = 60) -> str:
    """CONTRACT 4b: NFKD -> ASCII, lowercase, non-alphanumerics to single hyphens."""
    t = unicodedata.normalize("NFKD", str(text or ""))
    t = t.encode("ascii", "ignore").decode("ascii").lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:limit].rstrip("-") or "untitled"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="rename (default: dry run)")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    rows = []
    with open(FACTORY, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    print(f"factory.jsonl: {len(rows):,} rows")

    plan = []
    already = missing = notitle = 0
    for r in rows:
        old = r.get("file_path", "") or ""
        if not old:
            missing += 1
            continue
        d, base = os.path.split(old)
        ext = os.path.splitext(base)[1]
        title = str(r.get("title", "") or "").strip()
        if not title:
            notitle += 1
            continue
        src = r.get("source", "factory")
        ident = slug(r.get("id", ""), 60) or slug(os.path.splitext(base)[0], 60)
        new_base = f"{src}__{ident}__{slug(title)}{ext}"
        if new_base == base:
            already += 1
            continue
        if not os.path.exists(old):
            missing += 1
            continue
        plan.append((r, old, os.path.join(d, new_base)))

    print(f"  to rename {len(plan):,}   already conforming {already:,}   "
          f"file missing {missing:,}   no title {notitle:,}\n")
    for r, old, new in plan[:8]:
        print(f"  {os.path.basename(old)[:46]:46}")
        print(f"    -> {os.path.basename(new)[:76]}")

    if not args.apply:
        print("\ndry run — re-run with --apply")
        return 0

    done = 0
    for r, old, new in plan:
        if args.limit and done >= args.limit:
            break
        target = new
        n = 2
        while os.path.exists(target):          # CONTRACT 4b collision rule
            stem, ext = os.path.splitext(new)
            target = f"{stem}-{n}{ext}"
            n += 1
        try:
            os.rename(old, target)
        except OSError as e:
            print(f"  rename failed {old}: {e}")
            continue
        r["file_path"] = target
        r["renamed_from"] = os.path.basename(old)
        done += 1
        if done % 5000 == 0:
            print(f"  ... {done:,} renamed")

    tmp = FACTORY + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, FACTORY)
    print(f"\nrenamed {done:,} files; ledger rewritten with new paths")
    return 0


if __name__ == "__main__":
    sys.exit(main())
