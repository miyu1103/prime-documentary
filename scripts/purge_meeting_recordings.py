#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Delete gavel-to-gavel meeting recordings: council sessions, hearings, sermons.

Found 2026-08-09 with a lane stalled halfway through a 1.4 GB download of "Enumclaw City
Council - Regular Meeting". 646 of the 704 items filed under `government_buildings` were
municipal council sessions, 375 GB - 55% of the entire Internet Archive shelf by size.

They pass every gate the ingest has. The relevance scorer sees "city council chambers" and
scores it high; the technical floor sees 1080p H.264 and passes it; the licence is clearly
public. Nothing measures that the shot is a fixed camera pointed at a dais for two hours,
which is unusable as documentary b-roll at any length.

So the rule is about FORM, not subject: a recording of a proceeding, published as one long
take. Kept: archival films that merely mention the same institutions ("Dawn Strikes The
Capitol Dome Circa 1936", "Washington in War Time", home movies).

The same title rule now runs at ingest inside base.take(), so this is a one-off cleanup of
what the shelf already holds, not a recurring sweep.

    python scripts/purge_meeting_recordings.py             # dry run, prints both sides
    python scripts/purge_meeting_recordings.py --apply
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEDGER_DIR = r"H:\pd-media\assets\archive\_ledger"
ABSENT = os.path.join(LEDGER_DIR, "absent_index.json")
TOMBSTONES = os.path.join(LEDGER_DIR, "purged.jsonl")

# Proceedings recorded end to end. Deliberately narrow: each term names the EVENT, not a
# place or topic, so "Supreme Court building" and "courtroom sketch" are untouched.
MEETING_TERMS = (
    "city council", "town council", "county council", "village council",
    "council meeting", "council - regular", "council regular", "council work session",
    "city commission", "county commission", "planning commission", "planning board",
    "board of supervisors", "board of education", "board of trustees",
    "town hall meeting", "committee meeting", "budget hearing",
    "oversight hearing", "subcommittee on", "senate hearing", "house hearing",
    "public hearing", "confirmation hearing", "markup of", "legislative session",
    "public access television", "sermon", "church service", "worship service",
)
# Dropped after the first dry run: "podcast", "webinar", "zoning", bare "school board",
# "lecture series", "commencement address". On Pixabay and Pexels the title is a tag dump,
# so those words land on microphone close-ups, a chalkboard and a dark abstract - 40 usable
# stills were queued for deletion by them. "school board meeting" survives in STRONG.

# A recording of a sitting is long. Nothing this small is one, whatever the title says.
MIN_BYTES = 50 * 1024 * 1024
# A title that says outright it is a full recording of a sitting.
STRONG = ("regular meeting", "special meeting", "work session", "council meeting",
          "board meeting", "school board meeting", "full hearing", "gavel to gavel")


def is_meeting(title: str, size: int = MIN_BYTES) -> bool:
    """True for a gavel-to-gavel recording. `size` is the item's bytes; the floor is what
    keeps tag-dump titles on small stills from matching."""
    if size < MIN_BYTES:
        return False
    t = " " + " ".join((title or "").lower().split()) + " "
    return any(k in t for k in MEETING_TERMS) or any(k in t for k in STRONG)


def ledger_paths():
    for p in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        b = os.path.basename(p)
        if b.startswith("rejects") or b in ("purged.jsonl", "ban_risk_quarantine.jsonl",
                                            "shot_feedback.jsonl") \
                or b.endswith(("_removed.jsonl", "_candidates.jsonl")):
            continue
        yield p


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="delete (default: dry run)")
    args = ap.parse_args()

    absent = set()
    if os.path.exists(ABSENT):
        with open(ABSENT, encoding="utf-8", errors="replace") as fh:
            absent = set(json.load(fh).get("absent", {}))

    hits, kept_sample = [], []
    for path in ledger_paths():
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if f"{r.get('source')}:{r.get('id')}" in absent:
                    continue
                title = r.get("title") or ""
                if is_meeting(title, r.get("bytes", 0)):
                    hits.append(r)
                elif r.get("theme") == "government_buildings" and len(kept_sample) < 14:
                    kept_sample.append(r)

    gb = sum(r.get("bytes", 0) for r in hits) / 1e9
    print(f"{'DRY RUN' if not args.apply else 'DELETING'} — "
          f"{len(hits):,} recordings of proceedings, {gb:.0f} GB\n")

    by = {}
    for r in hits:
        k = (r.get("theme"), r.get("source"))
        b = by.setdefault(k, [0, 0])
        b[0] += 1
        b[1] += r.get("bytes", 0)
    print(f"{'theme / source':44} {'files':>7} {'GB':>8}")
    for (t, s), (n, b) in sorted(by.items(), key=lambda kv: -kv[1][1]):
        print(f"{str(t) + ' / ' + str(s):44} {n:7,} {b/1e9:8.1f}")

    print("\n削除される側 (大きい順):")
    for r in sorted(hits, key=lambda x: -x.get("bytes", 0))[:8]:
        print(f"  {r.get('bytes',0)/1e6:7.0f} MB  {(r.get('title') or '')[:66]}")
    print("\n残る側 (同テーマ・誤爆確認用):")
    for r in kept_sample:
        print(f"  {r.get('bytes',0)/1e6:7.0f} MB  {(r.get('title') or '')[:66]}")

    if not args.apply:
        print("\ndry run only — re-run with --apply to delete")
        return 0

    now = datetime.now(timezone.utc).isoformat()
    deleted = freed = failed = 0
    with open(TOMBSTONES, "a", encoding="utf-8") as tomb:
        for r in hits:
            fp = r.get("file_path") or ""
            size = r.get("bytes", 0)
            try:
                if fp and os.path.exists(fp):
                    size = os.path.getsize(fp)
                    os.remove(fp)
                    deleted += 1
                    freed += size
            except OSError as e:
                failed += 1
                print(f"  delete failed {fp}: {e}")
                continue
            tomb.write(json.dumps({
                "source": r.get("source"), "id": r.get("id"), "theme": r.get("theme"),
                "title": r.get("title"), "source_url": r.get("source_url"),
                "bytes": size, "reason": "meeting-recording", "purged_at": now,
            }, ensure_ascii=False) + "\n")

    print(f"\ndeleted {deleted:,} files, freed {freed/1e9:.1f} GB"
          + (f" ({failed} failed)" if failed else ""))
    print(f"tombstones -> {TOMBSTONES} (source_url kept)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
