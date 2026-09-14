"""The script-stage retention check must predict what the post-render gate will say.

`retention_cadence` is the most-failed check on the channel (18 of 34 finished episodes) and it
is measured three GPU-hours too late, from `<slug>_film.json captions[]`. Everything it measures
is already fixed by the script, so this predicts it while the script is still text.

The tests below pin the prediction against the films that actually exist. They are the reason to
believe the number, and they caught two things while being written:

  * a parser keyed on `## ACT_*` headings read **0 spoken words** on hyatt, ramirez and
    wronghouse -- EP67 onward carry no headings -- and then reported PASS on all three
  * `03_script/script.en.v001.md` is STALE on EP62-66: greene's says 5 questions where 9 were
    actually recorded. The file's own header says not to edit it and to regenerate it; nobody did
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import check_script_retention_plan as srp  # noqa: E402


def film_truth(slug: str) -> tuple[int, float] | None:
    """What the post-render gate measures: question count and biggest question-free gap (min)."""
    f = REPO / "remotion" / "src" / "data" / f"{slug}_film.json"
    if not f.is_file():
        return None
    caps = json.loads(f.read_text(encoding="utf-8")).get("captions") or []
    if not caps:
        return None
    end = max(c.get("end", 0) for c in caps)
    # Count OCCURRENCES, not captions: a caption can carry two questions, and counting captions
    # instead made this disagree with the script parser by one on ramirez -- two instruments
    # measuring different things and both looking right.
    qs = [c.get("start", 0) for c in caps for _ in range((c.get("text") or "").count("?"))]
    pts = [0.0] + qs + [end]
    gap = max((pts[i + 1] - pts[i] for i in range(len(pts) - 1)), default=0.0)
    return len(qs), gap / 60


# EP67 onward: the format the channel uses now, and the only one this predicts.
CURRENT_FORMAT = ["hyatt", "ramirez", "wronghouse"]


@pytest.mark.parametrize("slug", CURRENT_FORMAT)
def test_prediction_matches_the_finished_film(slug):
    truth = film_truth(slug)
    if truth is None:
        pytest.skip(f"{slug} has no film json")
    n_true, gap_true = truth
    path = srp.find_script(slug)
    assert path, f"no script for {slug}"
    r = srp.analyse(path.read_text(encoding="utf-8", errors="replace"))

    assert r["questions"] == n_true, (
        f"{slug}: script says {r['questions']} questions, the film has {n_true}")
    # The estimate converts words to minutes at an assumed pace, so its error is PROPORTIONAL:
    # a 10% pace difference is 0.5 min on a 5-minute gap and 3 min on a 30-minute one. A fixed
    # 2.5-minute tolerance failed wronghouse (31.0 vs 28.2) for being 10% off on a half-hour gap,
    # which is the estimate working exactly as documented. Judge it in percent.
    tol = max(1.5, gap_true * 0.15)
    assert abs(r["worst_question_gap_min"] - gap_true) <= tol, (
        f"{slug}: predicted gap {r['worst_question_gap_min']} min vs measured {gap_true:.1f} "
        f"(tolerance {tol:.1f})")
    assert r["ok"] is (gap_true * 60 <= srp.MAX_QUESTION_GAP_S)


def test_the_vo_form_is_what_gets_parsed():
    """Nine of fourteen recent episodes have no `## ACT_*` headings at all."""
    text = (REPO / "episodes/PD-2026-069-hyatt/03_script/script.en.v001.md").read_text(
        encoding="utf-8", errors="replace")
    assert srp.vo_lines(text), "the [VO:] parser found nothing in a real script"
    assert srp.analyse(text)["spoken_words"] > 4000, "spoken words read as ~zero again"


def test_a_stale_script_is_reported_not_silently_believed():
    """greene: script 5 questions, narration index 9. Reading it must say so."""
    msg = srp.staleness("greene", 5)
    assert msg and "never regenerated" in msg


def test_a_consistent_script_raises_no_stale_warning():
    assert srp.staleness("hyatt", 0) is None


def test_the_pace_assumption_stays_conservative():
    """PD_CANON §7 25: measured 159.5-169.7 wpm. Assuming the fast end hides real gaps."""
    assert 155.0 <= srp.NARRATION_WPM <= 162.0
