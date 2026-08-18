"""Answer one question for every queued episode: will the unattended queue stall on it?

Written 2026-08-11, after the machine sat idle for 545 minutes. The idleness had two causes and
neither was visible from any existing check: a hung `remotion render --help` held the queue's
busy detector at 12, and the queue process itself had died. Both are fixed. This tool is about the
OTHER way the queue stops -- it reaches an episode, finds a prerequisite missing, and moves on.

The dangerous case is not the loud one. `queue_unattended.sh` SKIPS an episode whose film json is
older than its master, reading that as "already rendered against the current plan". EP63 correa
was in exactly that state: its pool had been re-staged after a review rejected 26 clips, the film
json was never rebuilt, and the queue would have marked it done forever. Nothing fails. Nothing
goes red. The work simply never reaches the screen.

So this reports, per episode, every hard prerequisite the finisher needs -- checked cheaply, with
no render, no GPU, and no i2v -- plus the queue's own skip verdict, which is the one no other tool
looks at.

Usage:  py -3.11 scripts/check_queue_will_stall.py
Exit 0 when every episode is either ready or blocked for a reason that is named here.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

# slug, composition id, episode number -- kept in the same order as queue_unattended.sh JOBS
JOBS = [
    ("marmet", "Ep65Marmet", "65"),
    ("greene", "Ep62Greene", "62"),
    ("correa", "Ep63Correa", "63"),
    ("openfields", "Ep66Openfields", "66"),
    ("ramirez", "Ep67Ramirez", "67"),
    ("pinto", "Ep68Pinto", "68"),
    ("hyatt", "Ep69Hyatt", "69"),
]


def ep_dir(num: str, slug: str) -> Path:
    hits = sorted(ROOT.glob(f"episodes/PD-*-0{num}-{slug}"))
    return hits[0] if hits else ROOT / f"episodes/PD-2026-0{num}-{slug}"


def mtime(p: Path) -> float:
    return p.stat().st_mtime if p.is_file() else 0.0


def check(slug: str, comp: str, num: str) -> tuple[str, list[str]]:
    ep = ep_dir(num, slug)
    bad: list[str] = []

    # 1. filmconfig -- the finisher calls die() at step [4/7] without one
    if not sorted(ROOT.glob(f"episodes/_planning/EP*_{slug}_filmconfig.v*.json")):
        bad.append("no filmconfig (finisher dies at [4/7])")

    # 2. the composition must be registered, or the render exits on an unknown id
    root_tsx = (ROOT / "remotion/src/Root.tsx").read_text(encoding="utf-8", errors="replace")
    if f'id="{comp}"' not in root_tsx:
        bad.append(f"{comp} not in Root.tsx (render aborts)")

    # 3. the spec is the only place a number may come from (CLAUDE.md 4.6)
    if not (ep / "episode_spec.v001.json").is_file():
        bad.append("no episode_spec.v001.json (check_episode_spec stops the build)")

    # 4. narration -- the film's whole length is derived from it. NOT a wav: check_episode_inputs
    # reads `06_audio/narration_index.v001.json` and `remotion/public/<slug>/narration.mp3`.
    # My first version globbed for *.wav and reported all seven episodes as having no narration,
    # including marmet, whose own input check prints "narration 364 chunks, 31.4 min" on the line
    # above. A checker that disagrees with a working pipeline is wrong until proven otherwise.
    if not (ep / "06_audio" / "narration_index.v001.json").is_file():
        bad.append("no 06_audio/narration_index.v001.json")
    if not (ROOT / f"remotion/public/{slug}/narration.mp3").is_file():
        bad.append(f"no remotion/public/{slug}/narration.mp3")

    # 5. the scheduler's CONFIG entry. Every gate can go green and the LAST command still fails.
    sched = (ROOT / "scripts/upload_schedule_case_v001.py").read_text(encoding="utf-8", errors="replace")
    if f'"{slug}"' not in sched and f"'{slug}'" not in sched:
        bad.append("no CONFIG entry in upload_schedule_case_v001.py (cannot be scheduled)")

    # 6. THE SILENT ONE. The queue skips this episode entirely and says nothing.
    film = ROOT / f"remotion/src/data/{slug}_film.json"
    master = ep / f"08_edit/{slug}_final_bgm.v001.mp4"
    skipped = film.is_file() and master.is_file() and mtime(film) < mtime(master)
    if skipped:
        bad.append("SILENTLY SKIPPED: film json older than master -- queue thinks it is done")

    # 7. the input gate the queue itself runs before starting anything
    r = subprocess.run(
        ["py", "-3.11", str(ROOT / "scripts/check_episode_inputs.py"), "--slug", slug, "--no-forecast"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT,
    )
    if r.returncode != 0:
        first = next((ln.strip() for ln in (r.stdout + r.stderr).splitlines()
                      if ln.strip() and "READY" not in ln), "check_episode_inputs failed")
        bad.append(f"inputs: {first[:150]}")

    if bad:
        return "STALLS", bad
    return "READY", []


print(f"{'slug':11s} {'verdict':8s} why")
print("-" * 100)
worst = 0
for slug, comp, num in JOBS:
    verdict, why = check(slug, comp, num)
    if verdict != "READY":
        worst = 1
    print(f"{slug:11s} {verdict:8s} {why[0] if why else 'every prerequisite present'}")
    for extra in why[1:]:
        print(f"{'':20s} {extra}")
# ---------------------------------------------------------------- machine-level stalls
# Neither of these belongs to an episode, and neither was caught by any check on 2026-08-11,
# when both were true at once and the machine had been idle for nine hours.

print()
print("MACHINE")

# C: was at 22.1 GB free (99% full) with four renders and three public dirs still to come --
# roughly 29 GB of writes. A render that runs out of disk dies three hours in, having produced
# a truncated mp4 that the freshness gate would then compare against a stale receipt.
free_gb = shutil.disk_usage(str(ROOT)).free / (1024 ** 3)
NEED_GB = 30.0
if free_gb < NEED_GB:
    worst = 1
    print(f"  STALLS   only {free_gb:.1f} GB free on the repo drive; a render writes ~1.8 GB and a")
    print(f"           public dir 2-7 GB, so the remaining queue needs about {NEED_GB:.0f} GB.")
    print( "           Archive old out/*.mp4 to H: -- do not delete them.")
else:
    print(f"  READY    {free_gb:.1f} GB free on the repo drive (need about {NEED_GB:.0f})")

# Two queue instances ran concurrently on 2026-08-11, started 37 minutes apart. Each snapshots
# _finish_episode.sh at startup, so the OLDER one silently carried the pre-4-layer-audio
# finisher: whichever won the race would have decided what the audio of the next film was.
try:
    out = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "@(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*queue_unattended*' "
         "-and $_.CommandLine -notlike '*Win32_Process*' }).Count"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
    ).stdout.strip()
    nq = int(out or 0)
except Exception as exc:                      # a check that cannot measure must say so
    nq, out = -1, f"could not count queue processes: {exc}"
if nq < 0:
    print(f"  UNKNOWN  {out}")
elif nq == 0:
    worst = 1
    print("  STALLS   no queue_unattended.sh is running -- nothing will start the next episode")
else:
    # Process count alone is a weak signal: one queue reads as 1 or 2 depending on whether its
    # child shell is between commands, so a "> 2" threshold can miss two queues reading as 2.
    # Each queue makes its OWN snapshot directory at startup and holds it for its whole life,
    # so the snapshot count is the reliable one -- and it is the snapshots that matter, because
    # on 2026-08-11 the older of two queues was running a pre-4-layer-audio finisher and would
    # have decided the audio of whichever film it started first.
    # NOT Path("/tmp"): Git Bash maps /tmp to %TEMP% (here E:\UserTemp\aab15), while Python
    # reads a literal "/tmp" as C:\tmp and finds nothing. The first version of this line reported
    # "0 snapshot" with a queue plainly running -- a duplicate-queue detector that could never
    # detect a duplicate. tempfile.gettempdir() resolves to the same directory bash uses.
    snaps = sorted(Path(tempfile.gettempdir()).glob("pdq.*"))
    if len(snaps) > 1:
        worst = 1
        print(f"  STALLS   {len(snaps)} queue snapshots exist -- more than one queue has been started")
        print( "           and each runs its own copy of _finish_episode.sh. Kill all, restart one:")
        for s in snaps:
            print(f"             {s}")
    else:
        print(f"  READY    one queue ({nq} process(es), {len(snaps)} snapshot)")

print()
print("READY here means the queue can start it. It does not mean the film is good --")
print("check_spec_satisfied, the plate gate and the pool gate run inside the finisher.")
sys.exit(worst)
