"""The AE design gate must REFUSE a bad design, not just accept a good one.

decisions/0011 put After Effects into the film from EP77; the owner's clarification the same
day (2026-08-23) is that AE is used heavily and that the DESIGN STAGE is what has to work
first. `ae_problems()` in scripts/check_episode_spec.py is that design stage.

A gate that has never been shown to fail is decoration (docs/HANDOVER.md, permanent rule 5),
so every floor below is exercised with an input that must break it. If someone loosens a
floor to make an episode pass, one of these fails.

    py -3.11 -m pytest tests/test_ae_beats_design_gate.py -q
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_episode_spec import ae_problems  # noqa: E402

ACTS = ["HOOK", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ACT_5", "ACT_6", "ENDING"]


def beat(i: int, act: str, kind: str = "hero_number", sec: float = 8.0) -> dict:
    return {"id": f"AE{i:03d}", "act": act, "kind": kind,
            "headline": f"HEADLINE {i}", "source": f"FACTS_LEDGER row LH-{i:03d}",
            "duration_sec": sec}


def spec_with(beats: list[dict], slug: str = "aetest", **over) -> dict:
    ae = {"min_count": 12, "per_act_min": 1, "screen_seconds_min": 90.0,
          "jobs_file": f"scripts/ae/jobs_{slug}.json", "beats": beats}
    ae.update(over)
    return {"slug": slug, "section_vocabulary": list(ACTS), "ae_beats": ae}


def good_beats() -> list[dict]:
    # 16 beats: two in every one of the eight acts, 8s each = 128s on screen.
    return [beat(i + 1, ACTS[i % 8]) for i in range(16)]


def ep(n: int) -> Path:
    return Path(f"PD-2026-{n:03d}-aetest")


# --- the design that should pass -------------------------------------------------------

def test_a_complete_design_passes():
    assert ae_problems(spec_with(good_beats()), ep(77)) == []


def test_the_good_design_also_validates_against_the_schema():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((ROOT / "schemas" / "episode_spec.v001.json").read_text(encoding="utf-8"))
    sub = schema["properties"]["ae_beats"]
    jsonschema.Draft202012Validator(sub).validate(spec_with(good_beats())["ae_beats"])


# --- every floor, broken on purpose ----------------------------------------------------

def test_ep77_without_ae_beats_is_refused():
    problems = ae_problems({"slug": "aetest", "section_vocabulary": ACTS}, ep(77))
    assert problems and "ae_beats is missing" in problems[0]


def test_ep76_without_ae_beats_is_left_alone():
    # EP70-76 finish on the Remotion-only path (decisions/0011). The gate must not touch them.
    assert ae_problems({"slug": "aetest", "section_vocabulary": ACTS}, ep(76)) == []


def test_too_few_beats_is_refused():
    problems = ae_problems(spec_with(good_beats()[:11]), ep(77))
    assert any("min_count says 12" in p for p in problems)


def test_all_the_beats_in_one_act_is_refused():
    # 16 beats, 128 seconds, every count floor met -- and it is still not the film the
    # directive asked for, because seven acts have no AE in them at all.
    piled = [beat(i + 1, "ACT_2") for i in range(16)]
    problems = ae_problems(spec_with(piled), ep(77))
    assert any("per_act_min" in p for p in problems)


def test_an_act_outside_the_section_vocabulary_is_refused():
    beats = good_beats()
    beats[3]["act"] = "ACT_9"
    problems = ae_problems(spec_with(beats), ep(77))
    assert any("not in section_vocabulary" in p for p in problems)


def test_duplicate_beat_ids_are_refused():
    beats = good_beats()
    beats[5]["id"] = beats[0]["id"]
    problems = ae_problems(spec_with(beats), ep(77))
    assert any("duplicate beat id" in p for p in problems)


def test_twelve_flashes_that_nobody_can_read_are_refused():
    # 12 beats at 2s each is 24 seconds. It clears min_count and per_act_min is irrelevant
    # here; screen_seconds_min is the floor that says a hero card has to be readable.
    quick = [beat(i + 1, ACTS[i % 8], sec=2.0) for i in range(12)]
    problems = ae_problems(spec_with(quick), ep(77))
    assert any("screen_seconds_min" in p for p in problems)


def test_a_jobs_file_belonging_to_another_episode_is_refused():
    problems = ae_problems(
        spec_with(good_beats(), jobs_file="scripts/ae/jobs_lahaina.json"), ep(77))
    assert any("jobs_file" in p for p in problems)


def test_every_beat_must_name_where_its_headline_comes_from():
    # `source` is required by the schema, not by ae_problems -- an AE card states a fact on
    # screen and is subject to factual_support like a title (rule 19). This proves the schema
    # is the thing enforcing it, so nobody moves the requirement into prose.
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((ROOT / "schemas" / "episode_spec.v001.json").read_text(encoding="utf-8"))
    sub = schema["properties"]["ae_beats"]
    beats = good_beats()
    del beats[0]["source"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(sub).validate(spec_with(beats)["ae_beats"])
