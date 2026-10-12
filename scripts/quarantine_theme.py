#!/usr/bin/env python3
r"""Move a theme's downloads off the searchable shelf without deleting them.

WHY. 2026-08-23/24 the five place-neutral themes pulled 1,481 clips and a contact sheet said
almost none of them were the thing asked for. `night_road_lamp` returned Brooklyn Bridge, a
rice-terrace night view and five abstract CGI loops -- 0 of 12 usable. `anonymous_crowd`
returned a leopard, an egret, a bumblebee and a gull -- 1 of 12. The queries were written
tightly; the acceptance gate matches single words, so "light" admits a firework render.

Leaving them costs more than the disk. A shelf you cannot trust is searched anyway, and the
next person stages a leopard under "crowd". Deleting them costs the record of what was tried.
So: quarantine, the convention this shelf already has --
`E:\pd-archive\_quarantine\<theme>\`, which `search_archive.py` skips unless asked for it
explicitly (`--include-quarantined`).

The ledger row moves with the file rather than being dropped, so provenance and the
re-download guard both survive: the id stays known, and nothing fetches it again.

    py -3.11 scripts/quarantine_theme.py --theme night_road_lamp,anonymous_crowd
    py -3.11 scripts/quarantine_theme.py --theme ... --apply
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

LEDGER_DIR = Path(r"E:\pd-archive\_ledger")
QUARANTINE = Path(r"E:\pd-archive\_quarantine")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", default="", help="comma-separated theme names")
    ap.add_argument("--title-regex", default="",
                    help="quarantine rows whose TITLE matches this instead of/as well as a theme")
    ap.add_argument("--not-theme", default="",
                    help="never touch these themes (for graphic themes where generated IS the subject)")
    ap.add_argument("--reason", default="contact-sheet review: the query returned the word, not "
                                        "the subject")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    themes = {t.strip() for t in a.theme.split(",") if t.strip()}
    skip = {t.strip() for t in a.not_theme.split(",") if t.strip()}
    rx = re.compile(a.title_regex, re.I) if a.title_regex else None
    if not themes and not rx:
        ap.error("give --theme or --title-regex")

    def wanted(rec: dict) -> bool:
        """Which rows this run takes off the shelf.

        --title-regex exists for a criterion no theme expresses: measured 2026-08-24, 259 clips
        on the searchable shelf carry an AI-generated marker in their own title, and 179 of them
        sit under themes a documentary draws from -- courtroom_justice, police_modern,
        government_buildings, forensics_dna, and 47 under itaewon_korea_night while EP74 is in
        production. A generated image cut as a record of a real place is invariant 11. The
        remaining 73 are under abstract, vfx, particle and light, where a generated graphic IS
        the subject, and --not-theme leaves those alone.
        """
        if str(rec.get("theme", "")) in skip:
            return False
        if themes and str(rec.get("theme", "")) in themes:
            return True
        if rx and rx.search(str(rec.get("title", ""))):
            return True
        return False

    moved = missing = failed = 0
    for ledger in sorted(LEDGER_DIR.glob("*.jsonl")):
        if ledger.name.startswith("rejects") or ledger.name.startswith("ban_risk"):
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
        if not any(wanted(r) for r in rows):
            continue

        changed = 0
        for rec in rows:
            if not wanted(rec):
                continue
            src = Path(str(rec.get("file_path", "")))
            if QUARANTINE.as_posix().lower() in src.as_posix().lower():
                continue                      # already quarantined
            dst = QUARANTINE / str(rec["theme"]) / src.name
            if not src.exists():
                missing += 1
                continue
            moved += 1
            if not a.apply:
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(src), str(dst))
            except OSError as e:
                print(f"  FAILED {src.name}: {e}")
                failed += 1
                continue
            rec["file_path"] = str(dst)
            rec["quarantined_at"] = datetime.now(timezone.utc).isoformat()
            rec["quarantine_reason"] = a.reason
            changed += 1

        if a.apply and changed:
            tmp = ledger.with_suffix(".jsonl.quarantine_tmp")
            with tmp.open("w", encoding="utf-8") as fh:
                for rec in rows:
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            tmp.replace(ledger)
            print(f"  {ledger.name}: {changed} row(s) rewritten")

    verb = "moved" if a.apply else "would move"
    print(f"\n{verb} {moved} file(s) to {QUARANTINE}")
    if missing:
        print(f"  {missing} row(s) had no file on disk")
    if failed:
        print(f"  FAILED {failed}")
        return 1
    if not a.apply:
        print("\n(dry run -- nothing moved; add --apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
