"""The road's stage list must match the fleet the episode belongs to.

Round 3 of the brushup caught the AE hero stage (ADR-0011, binding EP77+) appearing on
hyatt -- EP69, shipped, scheduled -- and un-DONE-ing it. A seat that misreports a finished
episode as unfinished is the exact instrument-lies failure this whole day was about.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import ep_road  # noqa: E402


def _ctx(num):
    return {"slug": "probe", "num": num, "ep": REPO, "pub": REPO / "nowhere",
            "film": REPO / "nowhere.json"}


def test_the_old_fleet_has_no_ae_stage():
    names = [s.name for s in ep_road.stages(_ctx(69))]
    assert "ae_hero" not in names


def test_ep77_has_the_ae_stage_between_motion_and_film():
    names = [s.name for s in ep_road.stages(_ctx(77))]
    assert "ae_hero" in names
    assert names.index("motion") < names.index("ae_hero") < names.index("film")


def test_every_stage_has_a_next_action_or_a_named_human():
    """A frontier with neither is a dead end -- the road would say NEXT and then nothing."""
    for num in (69, 77):
        for s in ep_road.stages(_ctx(num)):
            assert s.next_cmd or s.human, f"stage {s.name} (EP{num}) is a dead end"
