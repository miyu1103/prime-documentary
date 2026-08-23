"""From EP77 on, the old way of building an episode must not open the gate.

Owner directive 2026-08-23: 「77話以降は今までのやり方で進まないようにしてほしい」. The four
questions this standard asks were red at ship time on 18/34 (retention), 14/34 (structure),
11/34 (footage reuse) and 8/34 (紙芝居) finished episodes -- every one discovered three
GPU-hours too late. These tests prove the road is actually closed: a bad EP77 is refused at
the stage where fixing it costs minutes, an EP76 is untouched, and the wiring sits at the
choke points the queue and the finisher already refuse on.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import check_ep77_standard as e77  # noqa: E402

GOOD_SCRIPT = """# EP77 · PROBE — SCRIPT v001

## HOOK
A man opens his front door on an ordinary Tuesday. Why are there agents on his lawn?

## ACT_1 — WHAT HAPPENED
{body} What did the paperwork actually say?

## ACT_2 — WHY THAT SHOULD BE IMPOSSIBLE
{body} Who signed it?

## ENDING
The rule was never about him. And whose name is on your form?
""".replace("{body}", "word " * 700)

# The first version of this fixture used 300-word acts and expected the questionless variant
# to fail -- but ~600 spoken words is under four minutes, and a four-minute question-free gap
# is LEGAL. The gate was right and the test was wrong. 700-word acts project past the 7-minute
# ceiling, which is what makes the missing questions a real defect.
NO_QUESTIONS = GOOD_SCRIPT.replace("?", ".")
NO_HEADINGS = GOOD_SCRIPT.replace("## ", "-- ")


@pytest.fixture
def road(tmp_path, monkeypatch):
    """A fake repo with one episode. Returns (write_script, set_number)."""
    monkeypatch.setattr(e77, "ROOT", tmp_path)
    state = {"num": 77}

    def build(script: str | None, num: int = 77):
        state["num"] = num
        ep = tmp_path / "episodes" / f"PD-2026-{num:03d}-probe"
        ep.mkdir(parents=True, exist_ok=True)
        if script is not None:
            pl = tmp_path / "episodes" / "_planning"
            pl.mkdir(exist_ok=True)
            (pl / f"EP{num}_probe_script.en.v001.md").write_text(script, encoding="utf-8")
        return ep

    return build


def test_an_episode_before_77_is_untouched(road):
    road(None, num=76)
    rc, msgs = e77.evaluate("probe", "inputs")
    assert rc == 0 and "old route allowed" in msgs[0]


def test_ep77_with_no_script_is_refused_with_the_template_named(road):
    road(None)
    rc, msgs = e77.evaluate("probe", "inputs")
    assert rc == 1
    assert any("_EP_SCRIPT_TEMPLATE" in m for m in msgs)


def test_ep77_without_the_template_headings_is_refused(road):
    road(NO_HEADINGS)
    rc, msgs = e77.evaluate("probe", "inputs")
    assert rc == 1
    assert any("template headings" in m for m in msgs)


def test_ep77_without_spaced_questions_is_refused(road):
    """The owner's top complaint (見ごたえ, red on 18/34) refused while the fix costs a sentence."""
    road(NO_QUESTIONS)
    rc, msgs = e77.evaluate("probe", "inputs")
    assert rc == 1
    assert any("retention" in m for m in msgs)


def test_a_compliant_ep77_script_passes(road):
    road(GOOD_SCRIPT)
    rc, msgs = e77.evaluate("probe", "inputs")
    assert rc == 0, msgs


def test_footage_reused_from_another_episode_is_named(road, tmp_path):
    """arc_nonrepeat (red on 11/34) decided at staging, where the shelf still has 26k clips."""
    road(GOOD_SCRIPT)
    mine = tmp_path / "remotion" / "public" / "probe" / "factory"
    theirs = tmp_path / "remotion" / "public" / "otherep" / "factory"
    mine.mkdir(parents=True)
    theirs.mkdir(parents=True)
    (mine / "a.mp4").write_bytes(b"exactly the same clip bytes")
    (theirs / "b.mp4").write_bytes(b"exactly the same clip bytes")
    (mine / "c.mp4").write_bytes(b"a different clip entirely")
    rc, msgs = e77.evaluate("probe", "inputs")
    assert rc == 1
    joined = " ".join(msgs)
    assert "byte-identical" in joined and "a.mp4" in joined and "c.mp4" not in joined


def test_the_gate_fails_closed_on_an_unknown_stage(road):
    road(GOOD_SCRIPT)
    rc, _ = e77.evaluate("probe", "nonsense")
    assert rc == 2


# --------------------------------------------------------------------------- #
# the wiring IS the directive -- prose cannot close a road, only call sites can
# --------------------------------------------------------------------------- #
def test_the_inputs_stage_is_wired_into_the_choke_point():
    src = (REPO / "scripts" / "check_episode_inputs.py").read_text(encoding="utf-8")
    assert "check_ep77_standard.py" in src
    assert src.index("check_ep77_standard.py") < src.index("READY to build"), \
        "the standard must be consulted before the gate says READY"


def test_the_plan_stage_runs_after_the_film_and_before_the_render():
    src = (REPO / "scripts" / "_finish_episode.sh").read_text(encoding="utf-8")
    assert "check_ep77_standard.py" in src
    i_film = src.index("[4/7] build film.json")
    i_std = src.index("check_ep77_standard.py")
    i_render = src.index("[6/7] guarded render")
    assert i_film < i_std < i_render


def test_still_hold_thresholds_live_in_exactly_one_place():
    """紙芝居 caps belong to check_animation_mix (invariant 14). The standard delegates."""
    src = (REPO / "scripts" / "check_ep77_standard.py").read_text(encoding="utf-8")
    assert "check_animation_mix.py" in src
    body = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith(("#", '"', "'")))
    assert "LONG_HOLD" not in body, "the standard grew its own copy of the still-hold threshold"
