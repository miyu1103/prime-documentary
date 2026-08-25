#!/usr/bin/env python3
r"""Bring every shelf index back in step with the shelf, in one command.

WHY THIS IS ONE COMMAND. On 2026-08-25 the three ways of finding footage had drifted apart and
each failure was silent:

  * the semantic index held 31,480 rows of which **18,084 pointed at files that no longer
    exist** -- 15,955 of them on H:, the drive that died in August. Half of "search by what is
    on screen" returned ghosts, and nothing said so.
  * the vertical (9:16) index read `E:\pd-media\assets\archive\_ledger`, a path that moved when
    the shelf did. It scanned zero rows and wrote no file: "no clips" is not an error.
  * neither index knew about the 388 clips ingested that day.

Ingest adds rows to the ledger; nothing downstream notices. So this runs after ingest, or on a
schedule, and does the three steps in the order that keeps them consistent:

  1. prune dead rows from the semantic index (paths.json + embeddings.npy stay row-aligned)
  2. embed whatever is on the shelf and not yet in the index
  3. score whatever is on the shelf and not yet in the vertical index

Every step is resumable and skips completed work, so re-running costs only the new clips.
Steps 2 and 3 need torch/transformers, which live in the Python 3.10 interpreter on this
machine, not in 3.11 -- pass --python if that changes.

    py -3.11 scripts/refresh_shelf_indexes.py --dry-run
    py -3.11 scripts/refresh_shelf_indexes.py
    py -3.11 scripts/refresh_shelf_indexes.py --skip-vertical
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TORCH_PY = r"C:\Users\aab15\AppData\Local\Programs\Python\Python310\python.exe"


def run(label: str, cmd: list[str], dry: bool) -> int:
    print(f"\n=== {label} ===")
    print("  " + " ".join(cmd))
    if dry:
        return 0
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print(f"  {label}: exit {r.returncode}")
    return r.returncode


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--python", default=TORCH_PY,
                    help="interpreter that has torch + transformers (default: the 3.10 install)")
    ap.add_argument("--skip-vertical", action="store_true")
    ap.add_argument("--skip-semantic", action="store_true")
    a = ap.parse_args()

    if not Path(a.python).is_file():
        sys.exit(f"no interpreter at {a.python} -- pass --python <path to one with torch>")

    failures = 0
    failures += run("prune dead rows from the semantic index",
                    [a.python, "scripts/prune_semantic_index.py", "--apply"], a.dry_run) != 0
    if not a.skip_semantic:
        failures += run("embed clips missing from the semantic index",
                        [a.python, "scripts/index_footage_semantic.py", "--build"], a.dry_run) != 0
    if not a.skip_vertical:
        failures += run("score clips missing from the vertical index",
                        ["py", "-3.11", "scripts/index_archive_vertical.py"], a.dry_run) != 0

    print(f"\nrefresh finished; {failures} step(s) reported a failure")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
