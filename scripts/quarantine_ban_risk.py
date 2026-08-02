#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Move ban-risk material off the archive shelf into quarantine, repeatably.

Found by eyeballing the labeled contact sheets (2026-07-30): a neo-Nazi prison speech
in `prison_jail` and a Holocaust-denial trial video in `courtroom_justice` had passed
every automated gate — they are on-topic by keyword, correctly licensed as PD, and
technically clean. Nothing in the ingest pipeline is looking for content that would end
the channel (growth-and-safety north star: grow, but never get banned).

The harm is not that the files exist; it is that a builder can stage them into a cut
without anyone naming them. So they leave the shelf.

Repeatable on purpose: the ingest lanes keep running for days, so new matches keep
arriving. Re-run after every ingest wave.

What it does NOT do: delete. Files move to `_quarantine\\<theme>\\` (CONTRACT.md 1),
and every move is recorded so it can be undone. The source ledgers are NOT rewritten —
five lanes are appending to them concurrently and a rewrite would race (the film.json
write-collision lesson). `search_archive.py` reads the quarantine record instead.

Usage:
    python scripts/quarantine_ban_risk.py                      # dry-run (default)
    python scripts/quarantine_ban_risk.py --apply
    python scripts/quarantine_ban_risk.py --set ban-risk,likeness --apply
    python scripts/quarantine_ban_risk.py --undo <path-in-quarantine> --apply
"""
from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEDGER_DIR = r"H:\pd-media\assets\archive\_ledger"
QUARANTINE = r"H:\pd-media\assets\archive\_quarantine"
RECORD = os.path.join(LEDGER_DIR, "ban_risk_quarantine.jsonl")

# Each pattern is a channel-safety judgement, not a relevance one. Keep them narrow and
# name the reason: a broad pattern would sweep up the legitimate archival record
# ("TRIAL OF NAZI SPIES", "WAR CRIMES TRIALS, TOKYO") which is exactly the material the
# channel is built on.
RULES = {
    "ban-risk": [
        ("advocacy_extremist",
         r"\b(ns |national socialist|neo-?nazi|white power|aryan nation)\b"
         r"|revolutionary[^|]{0,20}(speech|address)",
         "extremist advocacy — a policy strike ends the channel"),
        ("denial_revisionist",
         r"great holocaust trial|holocaust (hoax|denial|myth)|revisionis|zundel|zündel",
         "historical denial content — policy strike risk"),
        ("third_party_broadcast",
         r"\b(cnn|fox news|msnbc|bbc news|abc news|nbc news|cbs news|sky news"
         r"|60 minutes|dateline nbc)\b",
         "third-party news broadcast — copyright strike risk"),
    ],
    "likeness": [
        ("named_individual_record",
         r"\b(inmate file of|mugshot|booking photo of|prisoner record of|arrest record of)\b",
         "record of a named real person incl. mugshots — CLAUDE invariant 11"),
    ],
    # Found by EYES, not by pattern (2026-07-31 parallel contact-sheet review). None of
    # these carry a word the earlier keyword sweep looked for — the Censored Eleven short
    # is titled "Hittin' The Trail To Hallelujah Land" and the DVD rip announces itself
    # only in a burned-in warning card visible in the frame. Every one of them is tagged
    # `pd` or `cc0` in the ledger, which is simply wrong. Patterns stay narrow on purpose:
    # the genuine archival record this channel is built on ("TRIAL OF NAZI SPIES",
    # "WAR CRIMES TRIALS, TOKYO") must never be swept up with them.
    "qc-flagged": [
        ("racist_caricature",
         r"hallelujah land|jungle drums|\bbosko\b|hugh harman",
         "blackface-lineage / Censored Eleven animation — unusable regardless of PD status"),
        ("third_party_character",
         r"walt disney|\bdisney\b|superman|mr\.? bean|baby huey|oswald the lucky|"
         r"what a cartoon|chester cheetah|keebler|star wars|taxi driver|fireball xl5|"
         r"cartoon craze|max fleischer",
         "actively owned studio character or feature mislabelled pd/cc0 — Content ID risk"),
        ("off_air_recording",
         r"wgn cable|\bkvbc\b|wall street warriors|media smart",
         "off-air broadcast capture, often with a burned-in station logo"),
        ("fringe_channel_upload",
         r"citizen media news|citizen journalist|peter navarro|bank of ireland bail|"
         r"justice at all costs|court to court|prison radicalization|portland protest",
         "partisan or self-published channel upload — rights-dirty and reputationally risky"),
        ("disclaimed_ownership",
         r"not made by me",
         "the uploader's own title disclaims authorship — no rights chain at all"),
        ("named_litigant",
         r"brian david hill",
         "proceeding tied to a named private litigant"),
    ],
    # Documented, NOT swept: studio features whose PD status the reviewers doubted. These
    # need a title-by-title copyright-renewal check, not a blanket quarantine — run this
    # set only after that check says they are in fact encumbered.
    "rights-doubt": [
        ("unverified_pd_feature",
         r"naked kiss|kiss me deadly|pickup on south street|killers from space",
         "studio feature marked review_required; PD status doubtful, verify renewal"),
    ],
}


def load_shelf() -> list[dict]:
    recs = []
    for path in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        base = os.path.basename(path)
        if base.startswith("rejects") or base.endswith(
                ("_dedup_removed.jsonl", "_removed.jsonl", "_candidates.jsonl")) \
                or base in ("factory.jsonl", "ban_risk_quarantine.jsonl"):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    recs.append(json.loads(line))
                except Exception:
                    continue
    return recs


def already_done() -> set[str]:
    done = set()
    if os.path.exists(RECORD):
        with open(RECORD, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("action") == "quarantine":
                    done.add(f"{r.get('source')}:{r.get('id')}")
                elif r.get("action") == "undo":
                    done.discard(f"{r.get('source')}:{r.get('id')}")
    return done


def append_record(row: dict) -> None:
    """Single atomic write per line — four lanes tearing a shared log is a solved
    problem here (CONTRACT.md 5); do not hold a buffered handle open."""
    line = (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8")
    fd = os.open(RECORD, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
    try:
        os.write(fd, line)
    finally:
        os.close(fd)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--set", default="ban-risk",
                    help="comma list of rule sets: " + ",".join(RULES) + " (default ban-risk)")
    ap.add_argument("--apply", action="store_true",
                    help="actually move files (default is a dry run)")
    ap.add_argument("--undo", help="path of a quarantined file to restore")
    ap.add_argument("--id", action="append", default=[], metavar="SOURCE:ID",
                    help="quarantine one specific item a human identified by looking at "
                         "it. Some risks are invisible to any title pattern: a Fox News "
                         "chyron burned into the frame of an item titled '2019 AUG 11 "
                         "U.S. FBI Eyes Epstein's Death' is only findable by eye. "
                         "Repeatable.")
    args = ap.parse_args()

    sets = [s.strip() for s in args.set.split(",") if s.strip()]
    unknown = [s for s in sets if s not in RULES]
    if unknown:
        print(f"unknown rule set(s): {unknown}; available: {list(RULES)}")
        return 2
    rules = [r for s in sets for r in RULES[s]]

    if args.undo:
        if not os.path.exists(args.undo):
            print(f"not found: {args.undo}")
            return 2
        with open(RECORD, encoding="utf-8", errors="replace") as fh:
            match = [json.loads(l) for l in fh if l.strip()
                     and json.loads(l).get("new_path") == args.undo]
        if not match:
            print(f"no quarantine record for {args.undo}")
            return 2
        r = match[-1]
        if not args.apply:
            print(f"DRY RUN would restore -> {r['old_path']}")
            return 0
        os.makedirs(os.path.dirname(r["old_path"]), exist_ok=True)
        shutil.move(args.undo, r["old_path"])
        append_record({**r, "action": "undo",
                       "at": datetime.datetime.now(datetime.timezone.utc).isoformat()})
        print(f"restored -> {r['old_path']}")
        return 0

    done = already_done()
    wanted = set(args.id or [])
    hits, missing, skipped = [], 0, 0
    for rec in load_shelf():
        title = str(rec.get("title", ""))
        key = f"{rec.get('source')}:{rec.get('id')}"
        if key in done:
            skipped += 1
            continue
        if key in wanted:
            hits.append((rec, "eyeballed", "flagged by a human looking at the frame"))
            continue
        if args.id:
            continue          # --id is an explicit list, not a filter on top of the rules
        for name, pat, why in rules:
            if re.search(pat, title.lower()):
                hits.append((rec, name, why))
                break

    if not hits:
        print(f"no matches ({skipped} already quarantined)")
        return 0

    moved = 0
    total_mb = 0.0
    print(f"{'' if args.apply else 'DRY RUN — '}{len(hits)} match(es), "
          f"{skipped} already quarantined\n")
    for rec, name, why in hits:
        old = rec.get("file_path", "")
        theme = rec.get("theme") or "_unthemed"
        dest_dir = os.path.join(QUARANTINE, theme)
        new = os.path.join(dest_dir, os.path.basename(old))
        mb = (rec.get("bytes", 0) or 0) / 1e6
        total_mb += mb
        print(f"  [{name}] {rec.get('source')}/{theme} {mb:7.1f}MB  {str(rec.get('title',''))[:66]}")
        # An item the ingest lane already quarantined (for resolution, license, ...) is
        # physically in place but was never flagged as a CONTENT risk, so it still needs
        # the record — the record is what keeps search from offering it.
        in_quarantine = QUARANTINE.lower() in old.lower()
        if in_quarantine:
            print("      (already in _quarantine for another reason — recording as ban-risk)")
            new = old
        elif not os.path.exists(old):
            print("      (file already gone from the shelf — recording only)")
            missing += 1
        if not args.apply:
            continue
        if not in_quarantine and os.path.exists(old):
            os.makedirs(dest_dir, exist_ok=True)
            if os.path.exists(new):
                stem, ext = os.path.splitext(new)
                n = 2
                while os.path.exists(f"{stem}-{n}{ext}"):
                    n += 1
                new = f"{stem}-{n}{ext}"
            shutil.move(old, new)
            moved += 1
        append_record({
            "action": "quarantine", "rule": name, "reason": why,
            "source": rec.get("source"), "id": rec.get("id"), "theme": theme,
            "title": rec.get("title"), "bytes": rec.get("bytes"),
            "old_path": old, "new_path": new,
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        })

    print(f"\n{len(hits)} matched, {total_mb/1000:.2f} GB")
    if args.apply:
        print(f"moved {moved} file(s) to {QUARANTINE}\\<theme>\\ "
              f"({missing} had no file on disk)")
        print(f"recorded in {RECORD} — restore any item with --undo <new_path> --apply")
    else:
        print("dry run only — re-run with --apply to move them")
    return 0


if __name__ == "__main__":
    sys.exit(main())
