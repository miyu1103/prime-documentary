#!/usr/bin/env python3
"""Downgrade every Internet Archive row whose "free" claim is only the uploader's own field.

WHY THIS EXISTS
---------------
`ingest_archive_sources.py` read the item's `licenseurl` and believed it:

    elif "publicdomain" in licurl:
        decision, raw = "pd", licurl

On Internet Archive that field is typed by whoever uploaded the file. It is a claim, not a
licence. Measured on 2026-08-27, the rows it waved through as usable included a Blu-ray remux
of a 1964 feature, `Killer Klowns From Outer Space 1988 1080p`, `Robocop: The Animated Series`,
a 2017 McDonald's Happy Meal advertisement for The Emoji Movie, and a run of 1996 station
recordings whose whole content is brand advertising. None of those are public domain. The same
mechanism is how Sesame Street reached the shelf in the 2026-08-25 run.

WHAT IS STILL TRUSTED
---------------------
A trusted *collection*, which is curated by the archive rather than asserted by an uploader.
`collection:prelinger` is the only one the ingest currently produces, and rows carrying it are
left alone. Non-IA sources (NASA, government, Coverr, Mixkit) are not touched.

WHAT THIS DOES
--------------
Sets `license_decision` to `review_required` and records what it was, so nothing is lost and the
change is auditable:

    license_decision_previous : "pd" | "cc0"
    reindexed_at              : the run stamp passed in
    reindex_basis             : "uploader_asserted_licenseurl"
    reindex_note              : one sentence saying why

It does NOT move files. Measured on the same day, 20,731 of the 21,375 rows already sitting at
`review_required` live in the normal shelf and only 644 are under `_quarantine`, so the decision
field is the gate the shelf actually uses -- moving 590 files would break that convention, not
follow it.

Ledger files are rewritten atomically (temp then replace) and only when something changed.
Stop the ingest before running this: it appends to the same files.

    py -3.11 scripts/redecide_ia_uploader_licences.py --dry-run
    py -3.11 scripts/redecide_ia_uploader_licences.py --stamp 2026-08-27T10:00:00
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_archive_sources import LEDGER_DIR  # noqa: E402

NOTE = ("license_decision came from the item's own licenseurl field, which on Internet Archive "
        "is set by the uploader and is not evidence of a licence. Held for review.")
BASIS = "uploader_asserted_licenseurl"
TRUSTED_PREFIX = "collection:"


def needs_redecision(row: dict) -> bool:
    if row.get("source") != "ia":
        return False
    if row.get("license_decision") not in ("pd", "cc0", "free_commercial"):
        return False
    raw = str(row.get("license_field_raw") or "")
    return not raw.startswith(TRUSTED_PREFIX)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--stamp", default="", help="value written to reindexed_at")
    args = ap.parse_args()
    if not args.dry_run and not args.stamp:
        sys.exit("--stamp is required for a real run, so the change is dated in the ledger")

    files = sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl")))
    total = changed = 0
    samples: list[str] = []
    for path in files:
        out_lines: list[str] = []
        hit = 0
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                stripped = line.strip()
                if not stripped:
                    out_lines.append(line.rstrip("\n"))
                    continue
                total += 1
                try:
                    row = json.loads(stripped)
                except Exception:
                    out_lines.append(stripped)
                    continue
                if needs_redecision(row):
                    hit += 1
                    if len(samples) < 8:
                        samples.append(f"{row['license_decision']:4s} {str(row.get('title'))[:70]}")
                    row["license_decision_previous"] = row["license_decision"]
                    row["license_decision"] = "review_required"
                    row["reindexed_at"] = args.stamp
                    row["reindex_basis"] = BASIS
                    row["reindex_note"] = NOTE
                    out_lines.append(json.dumps(row, ensure_ascii=False))
                else:
                    out_lines.append(stripped)
        changed += hit
        if hit and not args.dry_run:
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(out_lines) + "\n")
            os.replace(tmp, path)
        if hit:
            print(f"  {os.path.basename(path):40s} {hit:5d} row(s)")

    print(f"\n{changed} of {total} ledger row(s) "
          f"{'would be' if args.dry_run else 'were'} held for review")
    for s in samples:
        print("   ", s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
