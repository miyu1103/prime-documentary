#!/usr/bin/env python
"""Move the repository's loose working files out of the way. Nothing is ever deleted.

WHY THIS EXISTS. On 2026-08-23 the repository root held 455 loose files -- 400 of them logs
from finished jobs -- plus 32 duplicate `qc_frames_*` directories, and `scripts/` held 1,046
files of which 217 were called from nowhere. None of that is wrong on its own; together it is
the reason a new session cannot tell what is live from what is finished.

WHY IT IS NOT A ONE-LINE `mv`. Three exclusions were measured before this was written, and
each one would have caused real damage:

1. SEVEN FILES THAT LOOK LIKE LOGS ARE NOT LOGS. `out_finish_<slug>.log.satisfied` is the
   marker that says an episode's finisher completed. `handover_snapshot.py` and
   `_finish_episode.sh` both read it. Moving those seven would have told the machine that
   seven finished episodes were unfinished, and a finisher run is about three hours.
   `out_prepare_done.txt` is the same shape for `prepare_for_scheduling.sh`.
2. SIX "UNUSED" SCRIPTS ARE IMPORTED BY MODULE NAME. The unused list was built by searching
   for the filename WITH its extension, and Python imports without one, so
   `import sdxl_quality_profiles` was invisible to it.
3. A LOCK IS NOT A LOG. `out_pdrun_*.lock` is how `pd_run.sh` stops two heavy jobs running at
   once. Five scripts depend on it.

The instrument that found (1) also reported 36 hits of which 34 were false -- it was matching
a variable called `out_path`. So the exclusions below are written out as literal names, read
once and checked by hand, rather than recomputed by a pattern at run time.

    py -3.11 scripts/tidy_repo_root.py              # dry run: prints, moves nothing
    py -3.11 scripts/tidy_repo_root.py --apply      # moves, and writes the undo script

Undo is one command: the script prints its path and every move is recorded there.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = "20260823"
FRESH_HOURS = 48

# --- exclusions, measured 2026-08-23, listed literally on purpose -----------------------

# Files at the root whose name begins like a log but which are STATE. Read by
# handover_snapshot.py, _finish_episode.sh and prepare_for_scheduling.sh.
STATE_MARKERS = {
    "out_finish_correa.log.satisfied",
    "out_finish_greene.log.satisfied",
    "out_finish_hyatt.log.satisfied",
    "out_finish_marmet.log.satisfied",
    "out_finish_openfields.log.satisfied",
    "out_finish_pinto.log.satisfied",
    "out_finish_ramirez.log.satisfied",
    "out_finish_wronghouse.log.satisfied",
    "out_prepare_done.txt",
    "cuts_tmp.json",
    "freeze.txt",
    "scratch_accept.json",
    "scratch_accept2.json",
    "scratch_accept3.json",
    "scratch_accept_final.json",
    "scratch_arc.json",
    "scratch_narration_index.v001.bak.json",
    "scratch_rolin_spans.json",
    "scratch_spans.txt",
    "tmp_black_memphis_new.txt",
    "tmp_black_memphis_new2.txt",
}

# Scripts on the "called from nowhere" list that are in fact imported by module name.
IMPORTED_BY_NAME = {
    "gen_narration_terry.py",
    "sdxl_quality_profiles.py",
    "upload_private_kelo_v001.py",
    "upload_short07_youtube_public.py",
    "assemble_gideon.py",
    "upload_madoff.py",
}

MOVABLE_PREFIXES = ("out_", "scratch", "tmp_", "run_")


def running_command_lines() -> str:
    """Everything the machine is executing right now, as one blob to test names against."""
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process | ForEach-Object { $_.CommandLine }"],
            capture_output=True, text=True, errors="ignore", timeout=120).stdout or ""
    except Exception:
        out = ""
    try:
        sched = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-ScheduledTask | Where-Object {$_.TaskName -match 'PD-'} | "
             "ForEach-Object { $_.Actions | ForEach-Object { \"$($_.Execute) $($_.Arguments)\" } }"],
            capture_output=True, text=True, errors="ignore", timeout=120).stdout or ""
    except Exception:
        sched = ""
    return out + "\n" + sched


def destination(name: str) -> Path:
    if name.startswith("out_"):
        return ROOT / "runs" / "logs" / f"attic_{STAMP}"
    if name.startswith("run_"):
        return ROOT / "scripts" / "_attic" / "root"
    return ROOT / "runs" / "_attic" / STAMP


def plan_root_files(live: str) -> tuple[list[tuple[Path, Path]], list[tuple[str, str]]]:
    cut = datetime.now() - timedelta(hours=FRESH_HOURS)
    moves, skipped = [], []
    for f in sorted(ROOT.iterdir()):
        if not f.is_file() or not f.name.startswith(MOVABLE_PREFIXES):
            continue
        n = f.name
        if n.endswith(".lock"):
            skipped.append((n, "lock -- pd_run.sh serialises heavy jobs with it")); continue
        if n in STATE_MARKERS:
            skipped.append((n, "STATE MARKER -- a finished-step flag, not a log")); continue
        if datetime.fromtimestamp(f.stat().st_mtime) > cut:
            skipped.append((n, f"touched inside {FRESH_HOURS}h")); continue
        if n in live:
            skipped.append((n, "named by a running or scheduled command")); continue
        moves.append((f, destination(n) / n))
    return moves, skipped


def plan_qc_dirs() -> list[tuple[Path, Path]]:
    dest = ROOT / "out_qc" / f"_root_attic_{STAMP}"
    return [(d, dest / d.name) for d in sorted(ROOT.glob("qc_frames*")) if d.is_dir()]


def plan_scripts(attic_list: list[str], live: str) -> tuple[list[tuple[Path, Path]], list[tuple[str, str]]]:
    dest = ROOT / "scripts" / "_attic"
    cut = datetime.now() - timedelta(days=21)
    moves, skipped = [], []
    for name in sorted(attic_list):
        f = ROOT / "scripts" / name
        if not f.is_file():
            skipped.append((name, "already gone")); continue
        if name in IMPORTED_BY_NAME:
            skipped.append((name, "imported by module name")); continue
        if name in live:
            skipped.append((name, "named by a running or scheduled command")); continue
        if datetime.fromtimestamp(f.stat().st_mtime) > cut:
            skipped.append((name, "touched inside 21 days")); continue
        moves.append((f, dest / name))
    return moves, skipped


def do_moves(moves: list[tuple[Path, Path]], apply: bool, done: list[dict]) -> int:
    n = 0
    for src, dst in moves:
        if not apply:
            n += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            dst = dst.with_name(f"{dst.name}.dup{int(time.time())}")
        try:
            shutil.move(str(src), str(dst))
        except OSError as exc:
            # Windows refuses to move a file another process holds open. That is the
            # behaviour we want: it fails loudly instead of corrupting a live job.
            print(f"  !! IN USE, left in place: {src.name} ({exc.__class__.__name__})")
            continue
        done.append({"from": str(src), "to": str(dst)})
        n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually move (default: dry run)")
    ap.add_argument("--undo-from", default="", metavar="JSON",
                    help="put every move in this record back where it came from")
    ap.add_argument("--attic-list", default="", help="json file with attic_scripts[]")
    a = ap.parse_args()

    if a.undo_from:
        # The apply run prints this command, so it has to exist. A tool that advertises an
        # undo it does not have is worse than one with no undo: it buys confidence it cannot
        # honour. Caught 2026-08-23, immediately after the first real run.
        rec = json.loads(Path(a.undo_from).read_text(encoding="utf-8"))
        back = ok = 0
        for row in reversed(rec):
            src, dst = Path(row["to"]), Path(row["from"])
            if not src.exists():
                print(f"  !! not where the record says: {src}")
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(src), str(dst))
                ok += 1
            except OSError as exc:
                print(f"  !! could not move back: {src.name} ({exc.__class__.__name__})")
            back += 1
        print(f"undo: {ok} of {len(rec)} move(s) reversed ({back} attempted)")
        return 0 if ok == len(rec) else 1

    live = running_command_lines()
    attic_list: list[str] = []
    if a.attic_list:
        attic_list = json.loads(Path(a.attic_list).read_text(encoding="utf-8"))["attic_scripts"]

    root_moves, root_skipped = plan_root_files(live)
    qc_moves = plan_qc_dirs()
    script_moves, script_skipped = plan_scripts(attic_list, live)

    mode = "APPLY" if a.apply else "DRY RUN -- nothing is moved"
    print(f"=== tidy_repo_root [{mode}] ===\n")
    print(f"root files   : move {len(root_moves):4d}   keep {len(root_skipped):3d}")
    for n, why in root_skipped:
        print(f"    keep  {n:44s} {why}")
    print(f"qc_frames dirs: move {len(qc_moves):4d}")
    print(f"scripts       : move {len(script_moves):4d}   keep {len(script_skipped):3d}")
    for n, why in script_skipped[:20]:
        print(f"    keep  {n:44s} {why}")

    done: list[dict] = []
    moved = do_moves(root_moves, a.apply, done)
    moved += do_moves(qc_moves, a.apply, done)
    moved += do_moves(script_moves, a.apply, done)

    print(f"\n{'moved' if a.apply else 'would move'}: {moved}")

    if a.apply and done:
        undo = ROOT / "runs" / "_attic" / f"UNDO_tidy_{STAMP}.json"
        undo.parent.mkdir(parents=True, exist_ok=True)
        undo.write_text(json.dumps(done, indent=1), encoding="utf-8")
        print(f"undo record: {undo.relative_to(ROOT).as_posix()}  ({len(done)} move(s))")
        print(f"undo with:   py -3.11 scripts/tidy_repo_root.py --undo-from "
              f"{undo.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
