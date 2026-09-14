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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shelf import shelf_rows  # noqa: E402  the one definition of "on the shelf"

LEDGER_DIR = r"E:\pd-media\assets\archive\_ledger"
QUARANTINE = r"E:\pd-media\assets\archive\_quarantine"
RECORD = os.path.join(LEDGER_DIR, "ban_risk_quarantine.jsonl")

# Each pattern is a channel-safety judgement, not a relevance one. Keep them narrow and
# name the reason: a broad pattern would sweep up the legitimate archival record
# ("TRIAL OF NAZI SPIES", "WAR CRIMES TRIALS, TOKYO") which is exactly the material the
# channel is built on.
RULES = {
    "ban-risk": [
        ("advocacy_extremist",
         # "ns " with no trailing boundary matched "NS Pearl Harbor" (Naval Station)
         # and quarantined two US Navy photographs. It has to be the movement's own name.
         r"\bns revolutionary\b|\bnational socialist\b|\bneo-?nazi\b"
         r"|\bwhite power\b|\baryan nation\b"
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
        # Found by eye 2026-08-09 on the `foreclosure sign house` sheet: seven press photos
        # of a named sitting politician sat in `household_loss`, scoring as generic b-roll.
        # A serving officeholder in a documentary about foreclosure reads as a claim about
        # that person, which is exactly what invariant 11 forbids — and the shot spec that
        # cited it would never say so. The list is of OFFICE-HOLDER names and the phrases
        # that mark a press-availability photo, not of "person" or "man": ordinary
        # unidentifiable people are the b-roll this shelf exists to supply.
        ("serving_officeholder",
         r"\b(kamala harris|barack obama|president obama|joe biden|president biden"
         r"|donald trump|hillary clinton|ag kamala)\b"
         r"|\b(meets with|delivers remarks|greets)\b.{0,40}\b(union|victims|leaders)\b",
         "press photograph of a named serving officeholder — invariant 11 likeness"),
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
         # A bare \bdisney\b matched a night photograph of Disneyland -- a place, not a
         # character mislabelled pd -- and "taxi driver" matched a real taxi driver reading
         # a newspaper. Both now need the studio or the film to be named.
         r"walt disney|disney/|disney's|disney channel|superman|mr\.? bean|baby huey|"
         r"oswald the lucky|what a cartoon|chester cheetah|keebler|star wars|"
         r"taxi driver \(19|fireball xl5|cartoon craze|max fleischer|"
         # Found 2026-08-09: music_performance_pd_era/ia is eight items and six are these
         # -- Wiggles TV episodes, three ABC For Kids concerts and a Nintendo compilation,
         # every one tagged pd or cc0 in the ledger, every one actively owned.
         r"the wiggles|abc for kids|\bnintendo\b",
         "actively owned studio character or feature mislabelled pd/cc0 — Content ID risk"),
        ("off_air_recording",
         # \b on media smart: it is a prefix of "media smartphone".
         r"wgn cable|\bkvbc\b|wall street warriors|\bmedia smart\b",
         "off-air broadcast capture, often with a burned-in station logo"),
        ("fringe_channel_upload",
         r"citizen media news|citizen journalist|peter navarro|bank of ireland bail|"
         r"justice at all costs|court to court|prison radicalization|portland protest",
         "partisan or self-published channel upload — rights-dirty and reputationally risky"),
        ("disclaimed_ownership",
         r"not made by me",
         "the uploader's own title disclaims authorship — no rights chain at all"),
        ("conspiracy_pseudoscience",
         r"moon landing hoax|landing was faked|flat earth|chemtrail|9/?11 truth|"
         r"crisis actor|false flag|new world order|deep state exposed|"
         # \b on illuminati: without it, it is a prefix of "illuminations", and 24
         # photographs of street and holiday lights matched.
         r"vaccine (hoax|truth)|great reset agenda|\billuminati\b|reptilian",
         "conspiracy content - a monetised channel about money and law cannot carry it"),
        ("named_litigant",
         r"brian david hill",
         "proceeding tied to a named private litigant"),
        # Found by eye 2026-08-09 on the laboratory_forensics sheet. Two of that pair's
        # seven items are COVID conspiracy broadcasts sitting beside a USAF sonic boom
        # test and a 1945 Navy film; the older conspiracy pattern looks for "vaccine hoax"
        # and neither title says it. Named broadcasters and claim shapes instead.
        # "depopulation" is deliberately absent: it matched four Pixabay photographs of an
        # empty swing tagged for RURAL depopulation, which is ordinary small-town imagery.
        ("medical_misinformation",
         r"stew peters|carrie madej|plandemic|scamdemic|graphene oxide"
         r"|died suddenly|vaccine shedding|spike protein shed"
         r"|\bco ?v ?[- ]?19\b[^|]{0,40}\bmicroscope\b"
         r"|\bcovid\b[^|]{0,40}\bmicroscope\b"
         r"|\bagenda 2[01]3?0?\b|adrenochrome|\bq ?anon\b|great awakening",
         "medical or governance misinformation — a monetised channel cannot carry it"),
    ],
    # A documentary shelf cannot hold synthetic pictures of the world it is documenting.
    # These 464 items announce themselves in their own titles -- Pixabay contributors tag
    # "ai generated" -- so they are the findable part of the problem, not all of it. One
    # surfaced on the prison_jail sheet as a plausible lamplit window and another on the
    # newspapers sheet as an anime illustration; neither is evidence of anything, and
    # invariant 11 forbids presenting generated visuals as an authentic record.
    "ai-generated": [
        ("declared_synthetic",
         r"\bai[- ]generated\b|\bgenerative ai\b|\bai art\b|\baiart\b"
         r"|\bmidjourney\b|\bstable diffusion\b|\bdall[- ]?e\b",
         "the contributor's own tags declare it synthetic — invariant 11"),
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
    # The factory shelf used to be excluded here, and it is 88,963 of the items
    # search_archive offers -- the biggest single block a shot spec draws from. A rule
    # that only guards the archive half leaves the other half unguarded: the first dry
    # run over it found 73 declared-synthetic images and six Star Wars stills.
    return list(shelf_rows(include_factory=True))


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
