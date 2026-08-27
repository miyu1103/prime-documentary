#!/usr/bin/env python3
"""Write the collection audit's verdicts back into the ledger.

`audit_ia_collections.py` produces `runs/ia_collection_verdicts.v001.json` from archive.org's
own collection membership -- the one rights signal on that site an uploader cannot set. This
applies it:

  free           -> pd              a collection the archive curates as public domain
  public_access  -> pd              the CREATOR is the rights holder and declared it public
                                    domain: 174 of these are "City of East Grand Forks"
                                    uploading its own council recordings, plus City of Albany,
                                    Belmont Public Library and Beech Street Center
  paywalled      -> stays held      a collection of other people's copyrighted work
  unsafe         -> stays held      archive.org's own `deemphasize` flag, or conspiracy and
                                    insurrection footage: a channel risk, not a rights one
  eyes           -> untouched       116 of 129 are `opensource_movies`, which is the generic
                                    anyone-can-upload bucket carrying no evidence whatsoever

`paywalled` and `unsafe` rows are not merely left alone: `rights_verdict` is set to `reject` so
a later restore pass can see they were examined and refused, rather than never looked at.

STOP THE INGEST FIRST. It appends to these same files and has no lock of its own; two writers
is how the ledger was corrupted before.

    py -3.11 scripts/apply_ia_collection_verdicts.py --dry-run
    py -3.11 scripts/apply_ia_collection_verdicts.py --stamp 2026-08-27T20:00:00
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

ROOT = Path(__file__).resolve().parents[1]
VERDICTS = ROOT / "runs" / "ia_collection_verdicts.v001.json"
CACHE = ROOT / "runs" / "_cache" / "ia_collections.json"

RESTORE = {"free", "public_access"}
REFUSE = {"paywalled", "unsafe"}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--stamp", default="")
    args = ap.parse_args()
    if not args.dry_run and not args.stamp:
        sys.exit("--stamp is required for a real run, so the change is dated in the ledger")

    verdicts = json.loads(VERDICTS.read_text("utf-8"))
    cache = json.loads(CACHE.read_text("utf-8")) if CACHE.exists() else {}
    plan: dict[str, tuple[str, str]] = {}
    for bucket, items in verdicts.items():
        if bucket not in RESTORE and bucket not in REFUSE:
            continue
        for it in items:
            plan[it["id"]] = (bucket, it.get("why", ""))
    print(f"{len(plan)} row(s) in the plan "
          f"({sum(len(verdicts.get(b, [])) for b in RESTORE)} restore, "
          f"{sum(len(verdicts.get(b, [])) for b in REFUSE)} refuse)")

    counts = {"restored": 0, "refused": 0}
    for path in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        out: list[str] = []
        hit = 0
        for line in open(path, encoding="utf-8"):
            stripped = line.strip()
            if not stripped:
                out.append(stripped)
                continue
            try:
                row = json.loads(stripped)
            except Exception:
                out.append(stripped)
                continue
            ident = row.get("id")
            if row.get("reindex_basis") != "uploader_asserted_licenseurl" or ident not in plan:
                out.append(stripped)
                continue
            bucket, why = plan[ident]
            creator = (cache.get(ident) or {}).get("creator", "")
            hit += 1
            if bucket in RESTORE:
                row["license_decision"] = row.get("license_decision_previous") or "pd"
                row["rights_verdict"] = "accept"
                row["reindex_basis"] = ("curated_collection" if bucket == "free"
                                        else "rights_holder_upload")
                row["reindex_note"] = (
                    f"archive.org collection '{why}' is curated by the archive, not by the "
                    f"uploader" if bucket == "free" else
                    f"uploaded by the rights holder itself ('{creator}') in collection '{why}', "
                    f"which declared it public domain")
                counts["restored"] += 1
            else:
                row["license_decision"] = "review_required"
                row["rights_verdict"] = "reject"
                row["reindex_basis"] = ("rights_holder_collection" if bucket == "paywalled"
                                        else "channel_unsafe")
                row["reindex_note"] = (
                    f"archive.org collection '{why}' holds other people's copyrighted work; "
                    f"do not restore" if bucket == "paywalled" else
                    f"archive.org collection '{why}'; off-brand for the channel, do not restore")
                counts["refused"] += 1
            row["reindexed_at"] = args.stamp
            out.append(json.dumps(row, ensure_ascii=False))
        if hit and not args.dry_run:
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(out) + "\n")
            os.replace(tmp, path)
        if hit:
            print(f"  {os.path.basename(path):30s} {hit:5d} row(s)")

    print(f"\n{'would restore' if args.dry_run else 'restored'}: {counts['restored']}   "
          f"{'would refuse' if args.dry_run else 'refused'}: {counts['refused']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
