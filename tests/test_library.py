"""Tests for the reusable music/visual libraries: schema validity + deterministic selection."""
from __future__ import annotations

from pathlib import Path

import pytest

from pd_factory.library import NoCandidateError, select_motif, select_track
from pd_factory.schema_validation import validate_data

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


def track(tid, category, *, mood="neutral", energy=3, reuse=0):
    return {
        "schema_version": "1.0.0",
        "track_id": tid,
        "category": category,
        "title": f"track {tid}",
        "mood": mood,
        "function": category,
        "bpm": 90,
        "energy": energy,
        "duration_sec": 60,
        "loopable": True,
        "source": "suno",
        "suno_origin": True,
        "suno_prompt": "cinematic restrained",
        "asset_uri": None,
        "content_hash": None,
        "rights_basis": "Suno subscription, commercial use per current terms",
        "tags": [category, mood],
        "reuse_count": reuse,
        "last_used_episode": None,
        "verified_at": "2026-06-14",
    }


def motif(mid, name, *, orientation="landscape", mood="neutral", reuse=0):
    return {
        "schema_version": "1.0.0",
        "motif_id": mid,
        "motif": name,
        "mood": mood,
        "orientation": orientation,
        "sref": "1234567890",
        "midjourney_prompt": f"{name}, symbolic --sref 1234567890",
        "source": "midjourney",
        "asset_uri": None,
        "content_hash": None,
        "rights_basis": "Midjourney subscription, commercial per current terms",
        "tags": [name],
        "reuse_count": reuse,
        "last_used_episode": None,
        "verified_at": "2026-06-14",
    }


# --- schema validity ---------------------------------------------------------
def test_track_schema_valid():
    validate_data(track("MUS-0001", "hook"), SCHEMA_DIR / "music-track.schema.json")
    validate_data(track("SFX-0001", "sfx"), SCHEMA_DIR / "music-track.schema.json")


def test_motif_schema_valid():
    validate_data(motif("MOT-0001", "gavel"), SCHEMA_DIR / "visual-motif.schema.json")


# --- music selection ---------------------------------------------------------
def test_select_track_matches_category():
    reg = [track("MUS-0001", "opening"), track("MUS-0002", "tension_build")]
    assert select_track(registry=reg, category="tension_build")["track_id"] == "MUS-0002"


def test_select_track_avoids_recent():
    reg = [track("MUS-0001", "reveal"), track("MUS-0002", "reveal")]
    # MUS-0001 sorts first normally; mark it recent -> MUS-0002 chosen.
    picked = select_track(registry=reg, category="reveal", recent_track_ids={"MUS-0001"})
    assert picked["track_id"] == "MUS-0002"


def test_select_track_relaxes_when_all_recent():
    reg = [track("MUS-0001", "outro", reuse=2), track("MUS-0002", "outro", reuse=0)]
    # both recent -> relax; prefer lower reuse_count -> MUS-0002.
    picked = select_track(
        registry=reg, category="outro", recent_track_ids={"MUS-0001", "MUS-0002"}
    )
    assert picked["track_id"] == "MUS-0002"


def test_select_track_energy_proximity():
    reg = [track("MUS-0001", "explainer_bed", energy=5), track("MUS-0002", "explainer_bed", energy=2)]
    picked = select_track(registry=reg, category="explainer_bed", energy=2)
    assert picked["track_id"] == "MUS-0002"


def test_select_track_deterministic():
    reg = [track("MUS-0002", "hook"), track("MUS-0001", "hook")]
    a = select_track(registry=reg, category="hook")
    b = select_track(registry=reg, category="hook")
    assert a["track_id"] == b["track_id"] == "MUS-0001"  # tie broken by id


def test_select_track_no_candidate_raises():
    with pytest.raises(NoCandidateError):
        select_track(registry=[track("MUS-0001", "hook")], category="somber")


# --- motif selection ---------------------------------------------------------
def test_select_motif_matches_and_avoids_recent():
    reg = [motif("MOT-0001", "gavel"), motif("MOT-0002", "gavel")]
    assert select_motif(registry=reg, motif="gavel", recent_motif_ids={"MOT-0001"})["motif_id"] == "MOT-0002"


def test_select_motif_orientation_preference():
    reg = [motif("MOT-0001", "map", orientation="portrait"), motif("MOT-0002", "map", orientation="landscape")]
    assert select_motif(registry=reg, motif="map", orientation="landscape")["motif_id"] == "MOT-0002"


def test_select_motif_no_candidate_raises():
    with pytest.raises(NoCandidateError):
        select_motif(registry=[motif("MOT-0001", "gavel")], motif="courtroom")
