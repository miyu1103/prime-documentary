"""A decision the pipeline makes must have exactly one implementation.

WHY THIS FILE EXISTS
--------------------
2026-08-23. One question -- "is this episode already built?" -- was implemented in FOUR places,
each by comparing an mtime against a hard-coded `_final_bgm.v001.mp4`:

    scripts/queue_unattended.sh       already_done()
    scripts/check_queue_will_stall.py the "SILENTLY SKIPPED" branch
    scripts/handover_snapshot.py      the "QUEUE SKIPS THIS" column
    scripts/check_final_acceptance.py the mux-order signal

The first was fixed. An hour later the second was found still wrong, then the third, then the
fourth. That is not carelessness -- it is arithmetic. A defect in a decision copied N times has
to be found N times, and the person fixing it has no way to know what N is.

Measured the same day: 813 scripts, 198 of them named after a single episode; 41 files decide
something from `final_bgm.v...`; 26 build a film json; 9 start a render. The repository does not
have a bug problem so much as a duplication problem, and every duplicate is a place a future
fix will miss.

These tests do not forbid duplication in general -- that would be unenforceable noise. They pin
the specific decisions that have already cost real time, so the next copy is caught at commit
rather than in production.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"

# The one module allowed to answer "is this episode already built?"
DONE_OWNER = "episode_is_done.py"

# Retired one-offs and their attic. Nothing here is on the live path; they are kept as a record.
IGNORED_DIRS = {"_attic", "__pycache__", "ae", "pd-visual-system", "studio", "tiktok"}


def live_scripts() -> list[Path]:
    out = []
    for p in list(SCRIPTS.glob("*.py")) + list(SCRIPTS.glob("*.sh")):
        if any(part in IGNORED_DIRS for part in p.parts):
            continue
        out.append(p)
    return out


def strip_comments(text: str, suffix: str) -> str:
    """Comments and docstrings explain the bug; they must not be mistaken FOR the bug.

    Stripping only `#` lines was not enough: check_gates_still_bite.py describes this very
    defect in its module docstring and was reported as an offender on the first run. A test
    that flags the file explaining the bug is a test nobody keeps.
    """
    if suffix == ".py":
        text = re.sub(r'"""(?:.|\n)*?"""', "", text)
        text = re.sub(r"'''(?:.|\n)*?'''", "", text)
    return "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))


MTIME_DONE = re.compile(
    r"final_bgm[^\n]{0,80}(st_mtime|getmtime|\s-ot\s|\s-nt\s)"
    r"|(st_mtime|getmtime|\s-ot\s|\s-nt\s)[^\n]{0,80}final_bgm")


def test_only_one_module_decides_done_and_it_does_not_use_mtime():
    offenders = []
    for p in live_scripts():
        if p.name == DONE_OWNER:
            continue
        body = strip_comments(p.read_text(encoding="utf-8", errors="replace"), p.suffix)
        if MTIME_DONE.search(body):
            offenders.append(p.name)
    assert not offenders, (
        "these decide 'is the film built?' from a file timestamp instead of asking "
        f"{DONE_OWNER}: {offenders}. That question was implemented four times in four places "
        "and was wrong in all four. Call the one implementation.")


HARD_CODED_MASTER = re.compile(r"_final_bgm\.v001\b")

# Scripts that legitimately WRITE or NAME a v001 master rather than deciding from it.
# `_finish_episode.sh:166` really does write v001; a v002 exists only where an episode was
# re-muxed afterwards, which is why six of the seven live episodes are v002 while the builder
# still names v001. That asymmetry is the soil the whole defect grew in.
WRITERS_ALLOWED = {
    "build_case_bgm_generic.py",     # names the file it is creating
    "build_case_film_mux.py",        # ditto
    "pd_splice_cuts.py",             # operates on a named master given to it
    # Re-derives which builder muxes by reading _finish_episode.sh, and returns "unknown"
    # rather than an answer when the name changes. Degrading to unknown is correct; this is
    # not a gate that silently stops applying.
    "predict_acceptance.py",
    # Retired one-offs for EP62-65, all four shipped. Nothing calls them; PD_CANON quotes
    # queue_finish_62_65.v002.sh as the worked example of the snapshot-the-script technique,
    # so they stay on disk as the record rather than being deleted.
    "queue_finish_62_65.sh",
    "queue_finish_62_65.v002.sh",
}


def test_no_gate_hard_codes_the_first_master_version():
    """Six of seven live episodes ship as v002. A gate keyed to v001 silently stops applying."""
    offenders = []
    for p in live_scripts():
        if p.name in WRITERS_ALLOWED or p.name == DONE_OWNER:
            continue
        if not p.name.startswith(("check_", "handover_", "queue_", "predict_")):
            continue
        body = strip_comments(p.read_text(encoding="utf-8", errors="replace"), p.suffix)
        if HARD_CODED_MASTER.search(body):
            offenders.append(p.name)
    assert not offenders, (
        f"these gates are keyed to the v001 master: {offenders}. On a v002 episode the check "
        "does not fail -- it does not run at all, and nothing says so.")


@pytest.mark.parametrize("panel", ["check_queue_will_stall.py", "handover_snapshot.py"])
def test_both_status_panels_ask_the_same_module(panel):
    src = (SCRIPTS / panel).read_text(encoding="utf-8", errors="replace")
    assert DONE_OWNER in src, f"{panel} answers 'built?' on its own again"
