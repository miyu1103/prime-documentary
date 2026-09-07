#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Delete shelf material the owner judged unusable, and leave a tombstone for every file.

Separate from quarantine_ban_risk.py on purpose. That tool takes ban-risk material OFF
the shelf and keeps it, because a wrong call there is a lost asset and a right call is a
safety decision. This is the opposite job: the owner has looked at contact sheets, ruled
a theme/source combination unusable, and wants the disk back. It deletes, so it is built
to be slower and louder — dry run by default, an explicit target list it will not exceed,
and a tombstone row for every removed file so the ledger can still be reconciled.

Scope is exactly the rows whose (theme, source) pair carries verdict "unusable" in
`_qc\\archive_verdicts.jsonl`. Nothing else is eligible, ever.

    python scripts/purge_unusable.py                       # dry run
    python scripts/purge_unusable.py --apply
    python scripts/purge_unusable.py --theme americana_1930s_1970s --apply
"""
from __future__ import annotations

import argparse
import collections
import datetime
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEDGER_DIR = r"E:\pd-media\assets\archive\_ledger"
VERDICTS = r"E:\pd-media\assets\archive\_qc\archive_verdicts.jsonl"
TOMBSTONE = os.path.join(LEDGER_DIR, "purged.jsonl")


def unusable_pairs() -> dict:
    pairs = {}
    with open(VERDICTS, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if (r.get("verdict") or "").lower() == "unusable":
                pairs[(r.get("theme"), r.get("source"))] = r.get("note", "")
    return pairs


def already_purged() -> set:
    done = set()
    if os.path.exists(TOMBSTONE):
        with open(TOMBSTONE, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                done.add(f"{r.get('source')}:{r.get('id')}")
    return done


def append_tombstones(rows: list) -> None:
    """One atomic write per line; the ingest lanes are appending to this directory."""
    for r in rows:
        line = (json.dumps(r, ensure_ascii=False) + "\n").encode("utf-8")
        fd = os.open(TOMBSTONE, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
        try:
            os.write(fd, line)
        finally:
            os.close(fd)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="actually delete (default: dry run)")
    ap.add_argument("--theme", help="restrict to one theme")
    ap.add_argument("--limit", type=int, default=0, help="stop after N deletions (0 = no limit)")
    args = ap.parse_args()

    pairs = unusable_pairs()
    if args.theme:
        pairs = {k: v for k, v in pairs.items() if k[0] == args.theme}
    if not pairs:
        print("no unusable (theme, source) pairs match")
        return 2
    done = already_purged()

    targets = []
    per = collections.Counter()
    per_b = collections.Counter()
    missing = 0
    for path in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        base = os.path.basename(path)
        if base.startswith("rejects") or base.endswith(
                ("_dedup_removed.jsonl", "_removed.jsonl", "_candidates.jsonl")) \
                or base in ("purged.jsonl", "ban_risk_quarantine.jsonl", "title_df.json"):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                key = (rec.get("theme"), rec.get("source"))
                if key not in pairs:
                    continue
                if f"{rec.get('source')}:{rec.get('id')}" in done:
                    continue
                fp = rec.get("file_path", "") or ""
                # Never touch quarantine: those are already off the shelf and under review.
                if "_quarantine" in fp.lower():
                    continue
                if not os.path.exists(fp):
                    missing += 1
                    continue
                targets.append((rec, fp))
                per[f"{key[0]} / {key[1]}"] += 1
                per_b[f"{key[0]} / {key[1]}"] += rec.get("bytes", 0) or 0

    total_b = sum(per_b.values())
    print(f"{'' if args.apply else 'DRY RUN — '}{len(targets):,} files, "
          f"{total_b/1e9:.1f} GB on disk")
    print(f"  ({missing:,} ledger rows already had no file; {len(done):,} purged previously)\n")
    print(f"{'theme / source':40} {'files':>8} {'GB':>8}")
    for k in sorted(per, key=lambda x: -per_b[x]):
        print(f"{k:40} {per[k]:8,} {per_b[k]/1e9:8.1f}")

    if not args.apply:
        print("\ndry run only — re-run with --apply to delete")
        return 0

    deleted = freed = 0
    batch = []
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for rec, fp in targets:
        if args.limit and deleted >= args.limit:
            break
        try:
            size = os.path.getsize(fp)
            os.remove(fp)
        except OSError as e:
            print(f"  could not delete {fp}: {e}")
            continue
        deleted += 1
        freed += size
        batch.append({"source": rec.get("source"), "id": rec.get("id"),
                      "theme": rec.get("theme"), "title": rec.get("title"),
                      "path": fp, "bytes": size, "sha256": rec.get("sha256"),
                      "source_url": rec.get("source_url"),
                      "reason": "owner verdict: unusable", "purged_at": now})
        if len(batch) >= 500:
            append_tombstones(batch)
            batch = []
            print(f"  ... {deleted:,} deleted, {freed/1e9:.1f} GB freed")
    if batch:
        append_tombstones(batch)
    print(f"\ndeleted {deleted:,} files, freed {freed/1e9:.1f} GB")
    print(f"tombstones -> {TOMBSTONE} (source_url kept, so any item can be re-fetched)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
