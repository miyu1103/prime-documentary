#!/usr/bin/env python3
r"""Replace the dead H: alias with the drive it actually points at.

WHY. The real H: (a Samsung T7) died. What answers to H: today is `subst H: E:\`, an alias
that lives in the logon session and vanishes on reboot. `H:\pd-media` and `E:\pd-media` are
the same bytes right now, so this rewrite changes nothing today -- and is the difference
between working and not working after the next reboot.

`scripts/ensure_h_drive.ps1` (task PD-EnsureHDrive) recreates the alias at logon. That is the
bandage. This is the cure, and both are wanted: the bandage covers the files this script
deliberately refuses to touch.

WHAT IT REFUSES TO TOUCH, and why each refusal is real:

  * files with uncommitted changes. Two lanes share this repo and one destroyed 117 ledger
    rows on 2026-08-20 by writing where the other was working. Rewriting a file another lane
    is editing hands them a conflict, and committing it commits their unfinished work.
  * shell scripts that are running RIGHT NOW. bash reads a script incrementally, by byte
    offset; editing one mid-run makes it resume at the wrong place in the new text. A python
    file is already parsed and in memory, so it is safe.
  * .json by default. Those 473 files are records of where a file WAS -- manifests, ledgers,
    receipts. Editing a record is not the same act as editing code, and it is not this
    script's call to make. --include-json when that decision has been taken.

VERIFICATION. Every .py file is compiled after the edit and reverted if it stops parsing, and
the replacement is counted: a file that reports zero replacements after being selected is a
bug in this script, not a clean file, and it is reported as such.

    py -3.11 scripts/fix_h_paths.py                 # dry run: what would change
    py -3.11 scripts/fix_h_paths.py --apply
    py -3.11 scripts/fix_h_paths.py --apply --include-json
"""
from __future__ import annotations

import argparse
import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_EXT = {".py", ".sh", ".ps1"}
DATA_EXT = {".json"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "out", "runs"}

# H:\pd-media, H:/pd-media, h:\\pd-media (escaped in a json or a python string literal).
PATTERN = re.compile(r"([Hh]):([\\/]{1,2})(pd-media)")


def replace(text: str) -> tuple[str, int]:
    """H -> E, keeping the separator exactly as written (\\, \\\\ or /)."""
    return PATTERN.subn(lambda m: f"E:{m.group(2)}{m.group(3)}", text)


def dirty_files() -> set[Path]:
    """Paths git reports as modified, staged or untracked."""
    out = subprocess.run(["git", "status", "--porcelain", "-z"], cwd=ROOT,
                         capture_output=True, text=True).stdout
    dirty = set()
    for entry in out.split("\0"):
        if len(entry) > 3:
            dirty.add((ROOT / entry[3:]).resolve())
    return dirty


def running_shell_scripts() -> set[str]:
    """Basenames of .sh/.ps1 files that appear in a running process command line."""
    names: set[str] = set()
    try:
        out = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process | ForEach-Object { $_.CommandLine }"],
            capture_output=True, text=True, timeout=60).stdout
    except Exception:  # noqa: BLE001 - no process list is a reason to be careful, not to stop
        return names
    for m in re.finditer(r"([A-Za-z0-9_.\-]+\.(?:sh|ps1))", out):
        names.add(m.group(1).lower())
    return names


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the changes (default: dry run)")
    ap.add_argument("--include-json", action="store_true",
                    help="also rewrite .json records -- see the module docstring first")
    ap.add_argument("--force-dirty", action="store_true",
                    help="rewrite files with uncommitted changes too")
    a = ap.parse_args()

    exts = CODE_EXT | (DATA_EXT if a.include_json else set())
    dirty = set() if a.force_dirty else dirty_files()
    running = running_shell_scripts()

    hits: list[Path] = []
    for p in ROOT.rglob("*"):
        if p.suffix.lower() not in exts or not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="strict")
        except (UnicodeDecodeError, OSError):
            continue
        if PATTERN.search(text):
            hits.append(p)

    checkdir = Path(tempfile.mkdtemp(prefix="pd_fix_h_"))
    changed = occurrences = 0
    skipped_dirty: list[str] = []
    skipped_running: list[str] = []
    failed: list[str] = []

    for p in sorted(hits):
        rel = p.relative_to(ROOT).as_posix()
        if p.resolve() in dirty:
            skipped_dirty.append(rel)
            continue
        if p.suffix.lower() in {".sh", ".ps1"} and p.name.lower() in running:
            skipped_running.append(rel)
            continue

        # newline="" on BOTH ends. Path.read_text/write_text translate line endings, so on
        # Windows every LF file came back as CRLF: measured 2026-08-22, all 385 rewritten files
        # flipped, and a CRLF .sh makes bash fail on its first line. The rewrite is one
        # character per match; it must not touch anything else in the file.
        with p.open("r", encoding="utf-8", newline="") as fh:
            original = fh.read()
        new, n = replace(original)
        if n == 0:
            failed.append(f"{rel} (selected but replaced 0 -- pattern bug)")
            continue
        occurrences += n
        changed += 1
        if not a.apply:
            continue

        with p.open("w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        if p.suffix.lower() == ".py":
            try:
                # cfile into a directory we own. NamedTemporaryFile keeps the handle OPEN,
                # and on Windows py_compile then cannot write to it: PermissionError, which
                # is not PyCompileError, so it escaped the except and killed the run after
                # one file. Measured 2026-08-22.
                py_compile.compile(str(p), cfile=str(checkdir / "check.pyc"), doraise=True)
            except (py_compile.PyCompileError, OSError) as e:
                with p.open("w", encoding="utf-8", newline="") as fh:
                    fh.write(original)
                changed -= 1
                occurrences -= n
                failed.append(f"{rel} (REVERTED: {e.__class__.__name__})")
                continue
        if PATTERN.search(p.read_text(encoding="utf-8")):
            failed.append(f"{rel} (H: still present after the write)")

    verb = "rewrote" if a.apply else "would rewrite"
    print(f"{verb} {changed} file(s), {occurrences} occurrence(s) of H:\\pd-media -> E:\\pd-media")
    print(f"matched {len(hits)} file(s) before the refusals below")
    if skipped_dirty:
        print(f"\nskipped -- uncommitted changes (another lane may be editing): {len(skipped_dirty)}")
        for r in skipped_dirty[:20]:
            print(f"  {r}")
        if len(skipped_dirty) > 20:
            print(f"  ... and {len(skipped_dirty) - 20} more")
    if skipped_running:
        print(f"\nskipped -- running right now: {len(skipped_running)}")
        for r in skipped_running:
            print(f"  {r}")
    if not a.include_json:
        print("\n.json records not touched (use --include-json once that decision is taken)")
    if failed:
        print(f"\nFAILED: {len(failed)}")
        for r in failed:
            print(f"  {r}")
        return 1
    if not a.apply:
        print("\n(dry run -- nothing written; add --apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
