# -*- coding: utf-8 -*-
"""
Re-fetch archival items that were DESTROYED by an over-strict technical floor.

Recovery tool for the 2026-07-28 regression: `validate_media` implemented the
archival quarantine as a 360-479p BAND, so sub-360p material fell through to the
reject path and was deleted -- including the Nuremberg/Mauthausen reel and the
German doctors' trial (Nuremberg Medical Case). Those items had already PASSED
the relevance gate; only the quality floor removed them.

Reads the reject logs for `tech:video-*` reasons on archival sources, re-fetches
each item through the normal `take()` path (which now quarantines rather than
deletes), and reports what was recovered. Idempotent: items already in a ledger
are skipped, so it is safe to re-run.

Usage:
  python scripts/refetch_archival_rejects.py            # recover everything found
  python scripts/refetch_archival_rejects.py --dry-run
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import ingest_archive_sources as M  # noqa: E402


def queue_from_rejects() -> list[dict]:
    """Unique archival items removed by a technical video floor."""
    out: dict[tuple[str, str], dict] = {}
    for f in glob.glob(os.path.join(M.LEDGER_DIR, "rejects*.jsonl")):
        if "malformed" in f:
            continue
        for line in open(f, encoding="utf-8", errors="replace"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            if (r.get("source") in M.ARCHIVAL_SOURCES
                    and str(r.get("reason", "")).startswith("tech:video-")):
                out.setdefault((r["source"], str(r["id"])), r)
    return list(out.values())


def refetch_ia(ledger: M.Ledger, item: dict, dry_run: bool) -> bool:
    """Re-run one Internet Archive item through the standard take() path."""
    ident = item["id"]
    theme = item["theme"]
    try:
        md = M.NET.get_json(f"https://archive.org/metadata/{ident}")
    except Exception as e:  # noqa: BLE001
        M.log(f"  metadata fail {ident}: {e}")
        return False
    meta = md.get("metadata", {})
    licurl = str(meta.get("licenseurl", "") or "")
    colls = meta.get("collection", [])
    colls = [colls] if isinstance(colls, str) else colls
    if "/zero/" in licurl or "cc0" in licurl.lower():
        decision, raw = "cc0", licurl
    elif "publicdomain" in licurl:
        decision, raw = "pd", licurl
    elif any("prelinger" in c.lower() for c in colls):
        decision, raw = "pd", f"collection:prelinger (public domain); licenseurl={licurl}"
    else:
        decision, raw = "review_required", f"licenseurl={licurl}; collections={colls[:4]}"
    subj = meta.get("subject", [])
    subj = [subj] if isinstance(subj, str) else subj
    desc = f"{meta.get('description', '')} {' '.join(map(str, subj[:20]))}"[:900]
    cands = []
    for f in md.get("files", []):
        name = f.get("name", "")
        if not name.lower().endswith(".mp4"):
            continue
        size = int(f.get("size", 0) or 0)
        fmt = (f.get("format") or "").lower()
        if M.MIN_ITEM_BYTES < size <= M.MAX_ITEM_BYTES:
            cands.append((0 if "h.264" in fmt else 1, size, name))
    if not cands:
        M.log(f"  no usable derivative: {ident}")
        return False
    cands.sort()
    url = f"https://archive.org/download/{ident}/{urllib.parse.quote(cands[0][2])}"
    return M.take(ledger, source="ia", item_id=ident,
                  title=str(meta.get("title", ident)),
                  source_url=f"https://archive.org/details/{ident}", download_url=url,
                  kind="video", theme=theme, license_raw=raw, decision=decision,
                  default_ext="mp4", dry_run=dry_run, desc=desc)


def main() -> int:
    ap = argparse.ArgumentParser(description="Re-fetch floor-destroyed archival items")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    M.load_env()
    ledger = M.Ledger(0)
    ledger.load_existing_index()
    queue = queue_from_rejects()
    M.log(f"recovery queue: {len(queue)} unique archival items removed by technical floors")
    done = skipped = failed = 0
    for item in queue:
        src, ident = item["source"], str(item["id"])
        if ledger.seen(src, ident):
            M.log(f"  already in ledger, skip: {ident[:60]}")
            skipped += 1
            continue
        if src != "ia":
            M.log(f"  not this lane ({src}), left for its owner: {ident[:50]}")
            skipped += 1
            continue
        M.log(f"  refetch [{item['theme']}] {item.get('title') or ident}")
        if refetch_ia(ledger, item, args.dry_run):
            done += 1
        else:
            failed += 1
    M.log("=" * 60)
    M.log(f"RECOVERED: {done}   skipped: {skipped}   failed: {failed}")
    M.log(f"this run: {ledger.run_items} items, {ledger.run_bytes/M.GB:.2f} GB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
