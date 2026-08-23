#!/usr/bin/env python3
"""The EP77 road: from EP77 on, an episode cannot be built the old way.

WHY THIS EXISTS (owner directive, 2026-08-23)
---------------------------------------------
「77話以降は今までのやり方で進まないようにしてほしい」— and the numbers behind it. Of 34
finished episodes, the checks the owner's complaints map onto were red at ship time on:

    retention_cadence (見ごたえ)  18/34      structure_4part (構成)   14/34
    arc_nonrepeat    (素材被り)   11/34      animation_mix   (紙芝居)  8/34

Every one was detected AFTER the three-hour render, when the only options were ship-red or
burn another three hours. Every episode shipped red. This gate asks the same questions at the
stage where the fix costs minutes: the script is a text file, the pool is a folder of clips,
the film json is a plan no GPU has touched.

THIS IS NOT A NEW BRAKE. It is the same four questions, moved to where stopping is free.
The old route is closed by wiring: `check_episode_inputs.py` (step [0/7], which the queue and
the finisher both refuse on) calls `--stage inputs` for episode 077+, and `_finish_episode.sh`
calls `--stage plan` right after the film json is built, before the render.

Episodes below 077 are untouched: this returns PASS instantly for them, by number, so nothing
about EP70-76 changes while they finish.

STAGES
------
  --stage inputs   (script + pool; before anything expensive)
    1. the planning script exists and follows the template: HOOK / ACT_1..N / ENDING headings
    2. retention plan: a literal question at least every ~7 projected minutes
       (check_script_retention_plan; ramirez asked 10 questions and still failed on spacing)
    3. no staged factory clip is byte-identical to a clip used by another episode
       (the shelf holds 26,422 videos, measured 2026-08-23; reuse is a lookup failure, not
       scarcity)
  --stage plan     (film json built, render not started)
    4. animation mix: still-holds within the caps check_animation_mix already defines
       (紙芝居 -- delegated to that tool so there is exactly one implementation)

Usage:
    py -3.11 scripts/check_ep77_standard.py --slug <slug> --stage inputs
    py -3.11 scripts/check_ep77_standard.py --slug <slug> --stage plan

Exit codes: 0 pass (or episode < 077), 1 the standard is not met, 2 cannot evaluate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

FIRST_EPISODE = 77
REQUIRED_HEADINGS = ("HOOK", "ACT_1", "ENDING")     # the template's minimum skeleton
RE_HEADING = re.compile(r"^##\s+([A-Z_0-9]+)", re.M)


def episode_number(slug: str) -> tuple[int | None, Path | None]:
    hits = sorted(ROOT.glob(f"episodes/PD-2026-*-{slug}"))
    if not hits:
        return None, None
    m = re.match(r"PD-2026-(\d+)-", hits[-1].name)
    return (int(m.group(1)) if m else None), hits[-1]


def planning_script(slug: str, num: int) -> Path | None:
    hits = sorted(ROOT.glob(f"episodes/_planning/EP{num}_{slug}_script.en.v*.md"))
    return hits[-1] if hits else None


# --------------------------------------------------------------------------- #
# inputs stage
# --------------------------------------------------------------------------- #
def check_template(text: str) -> list[str]:
    heads = set(RE_HEADING.findall(text))
    missing = [h for h in REQUIRED_HEADINGS if h not in heads]
    return ([f"script is missing the template headings: {missing}. Start from "
             f"episodes/_planning/_EP_SCRIPT_TEMPLATE.v001.md"] if missing else [])


def check_retention(script: Path) -> list[str]:
    import check_script_retention_plan as srp
    r = srp.analyse(script.read_text(encoding="utf-8", errors="replace"))
    if r["ok"]:
        return []
    return [f"retention: {r['questions']} question(s), biggest question-free gap "
            f"{r['worst_question_gap_min']} min (ceiling {r['gap_ceiling_min']:.0f}). "
            f"Not more questions -- better spaced ones: one per act."]


def _digest(p: Path) -> str:
    """Size + first/last 64KiB. Full sha over every pool on the channel is minutes; this is
    seconds, and a partial-hash collision still forces a full compare before we accuse."""
    st = p.stat()
    h = hashlib.sha256()
    h.update(str(st.st_size).encode())
    with p.open("rb") as f:
        h.update(f.read(65536))
        if st.st_size > 131072:
            f.seek(-65536, 2)
            h.update(f.read(65536))
    return h.hexdigest()


def _full_sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def check_pool_reuse(slug: str) -> list[str]:
    """No staged clip may be byte-identical to a clip in another episode's pool.

    This is arc_nonrepeat (11/34 red at ship time) decided at staging, where the remedy is
    'pick a different clip from the 26,422 on the shelf' instead of 'reopen a finished film'.
    """
    mine = sorted((ROOT / "remotion" / "public" / slug / "factory").glob("*.mp4"))
    if not mine:
        return []                                   # nothing staged yet -> nothing to collide
    theirs: dict[str, Path] = {}
    for d in (ROOT / "remotion" / "public").iterdir():
        if not d.is_dir() or d.name == slug:
            continue
        for p in (d / "factory").glob("*.mp4"):
            theirs.setdefault(_digest(p), p)
    hits = []
    for p in mine:
        other = theirs.get(_digest(p))
        if other is not None and _full_sha(p) == _full_sha(other):
            hits.append(f"{p.name} == {other.parent.parent.name}/{other.name}")
    if not hits:
        return []
    return [f"{len(hits)} staged clip(s) are byte-identical to another episode's footage; "
            f"swap them (shelf holds 26,422 videos): " + "; ".join(hits[:5])
            + (" ..." if len(hits) > 5 else "")]


# --------------------------------------------------------------------------- #
# plan stage
# --------------------------------------------------------------------------- #
def check_stills(epid: str) -> list[str]:
    """紙芝居 (8/34 red at ship) -- delegated to check_animation_mix so the thresholds live in
    exactly one place (invariant 14). It reads the film json; no pixels, no GPU."""
    r = subprocess.run(["py", "-3.11", str(ROOT / "scripts/check_animation_mix.py"),
                        "--ep", epid],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=ROOT)
    if r.returncode == 0:
        return []
    tail = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    return ["animation mix (紙芝居): " + (tail[-1][:160] if tail else f"exit {r.returncode}")]


# --------------------------------------------------------------------------- #
def evaluate(slug: str, stage: str) -> tuple[int, list[str]]:
    num, epdir = episode_number(slug)
    if num is None or epdir is None:
        return 2, [f"no episode directory for slug {slug!r}"]
    if num < FIRST_EPISODE:
        return 0, [f"EP{num} predates the EP77 standard -- old route allowed, nothing checked"]

    problems: list[str] = []
    if stage == "inputs":
        script = planning_script(slug, num)
        if script is None:
            problems.append(f"no planning script episodes/_planning/EP{num}_{slug}_script.en.v*.md "
                            f"-- start from _EP_SCRIPT_TEMPLATE.v001.md")
        else:
            text = script.read_text(encoding="utf-8", errors="replace")
            problems += check_template(text)
            problems += check_retention(script)
        problems += check_pool_reuse(slug)
    elif stage == "plan":
        problems += check_stills(epdir.name)
    else:
        return 2, [f"unknown stage {stage!r}"]
    return (1 if problems else 0), problems


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--stage", choices=("inputs", "plan"), required=True)
    a = ap.parse_args()
    rc, problems = evaluate(a.slug, a.stage)
    tag = {0: "PASS", 1: "FAIL", 2: "ERROR"}[rc]
    print(f"[ep77-standard] {a.slug} stage={a.stage}: {tag}")
    for p in problems:
        print(f"  - {p}")
    if rc == 1:
        print("  The fix at this stage costs minutes. After the render it costs three hours. "
              "That is the whole point of this gate.")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
