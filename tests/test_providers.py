"""Offline provider-adapter tests: env loading, auth-check parsing, paid gating. No network."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from pd_factory.budget import BudgetLedger, BudgetPolicy
from pd_factory.providers import courtlistener, elevenlabs, runway, youtube
from pd_factory.providers.env import EnvStore
from pd_factory.providers.http import (
    PaidOperationNotConfirmed,
    PreflightError,
    preflight,
    request,
)


def fake(routes):
    """routes: list of (url_substr, status, json_obj). Returns a transport."""
    def transport(method, url, headers, body, timeout):
        for sub, status, obj in routes:
            if sub in url:
                return status, json.dumps(obj).encode(), "application/json"
        return 404, b"{}", "application/json"
    return transport


def env_with(tmp_path: Path, **vals) -> EnvStore:
    (tmp_path / ".env").write_text("\n".join(f"{k}={v}" for k, v in vals.items()), encoding="utf-8")
    return EnvStore(root=tmp_path)


# --- env ---------------------------------------------------------------------
def test_env_get_require_present(tmp_path: Path):
    e = env_with(tmp_path, COURTLISTENER_TOKEN="tok", ELEVENLABS_API_KEY="")
    assert e.get("COURTLISTENER_TOKEN") == "tok"
    assert e.get("ELEVENLABS_API_KEY") is None  # empty counts as missing
    assert e.present("COURTLISTENER_TOKEN") and not e.present("ELEVENLABS_API_KEY")
    with pytest.raises(KeyError):
        e.require("RUNWAY_API_KEY")


# --- preflight ---------------------------------------------------------------
def test_preflight_blocks_unlisted_and_http():
    with pytest.raises(PreflightError):
        preflight("https://evil.example.com/x")
    with pytest.raises(PreflightError):
        preflight("http://api.elevenlabs.io/x")
    assert preflight("https://api.elevenlabs.io/v1/voices") == "api.elevenlabs.io"


# --- auth checks (free) ------------------------------------------------------
def test_courtlistener_auth_check(tmp_path: Path):
    e = env_with(tmp_path, COURTLISTENER_TOKEN="tok")
    t = fake([("courtlistener", 200, {"results": [{"id": 1}]})])
    r = courtlistener.auth_check(e, transport=t)
    assert r["ok"] and r["status"] == 200
    # missing token -> miss, no call
    r2 = courtlistener.auth_check(EnvStore(root=tmp_path / "none"))
    assert not r2["ok"]


def test_elevenlabs_auth_check_counts_voices(tmp_path: Path):
    e = env_with(tmp_path, ELEVENLABS_API_KEY="k")
    t = fake([("elevenlabs.io/v1/voices", 200, {"voices": [{}, {}, {}]})])
    r = elevenlabs.auth_check(e, transport=t)
    assert r["ok"] and "3 voices" in r["detail"]


def test_runway_auth_check_reads_credits(tmp_path: Path):
    e = env_with(tmp_path, RUNWAY_API_KEY="k")
    t = fake([("runwayml.com/v1/organization", 200, {"creditBalance": 1234})])
    r = runway.auth_check(e, transport=t)
    assert r["ok"] and "1234" in r["detail"]


def test_youtube_auth_check_two_step(tmp_path: Path):
    e = env_with(tmp_path, YOUTUBE_CLIENT_ID="i", YOUTUBE_CLIENT_SECRET="s", YOUTUBE_REFRESH_TOKEN="r")
    t = fake([
        ("oauth2.googleapis.com/token", 200, {"access_token": "AT"}),
        ("youtube/v3/channels", 200, {"items": [{"snippet": {"title": "PD Channel"}}]}),
    ])
    r = youtube.auth_check(e, transport=t)
    assert r["ok"] and "PD Channel" in r["detail"]


def test_youtube_auth_check_token_failure(tmp_path: Path):
    e = env_with(tmp_path, YOUTUBE_CLIENT_ID="i", YOUTUBE_CLIENT_SECRET="s", YOUTUBE_REFRESH_TOKEN="bad")
    t = fake([("oauth2.googleapis.com/token", 400, {"error": "invalid_grant"})])
    r = youtube.auth_check(e, transport=t)
    assert not r["ok"]


# --- paid gating -------------------------------------------------------------
def test_paid_ops_refuse_without_confirmation(tmp_path: Path):
    e = env_with(tmp_path, ELEVENLABS_API_KEY="k", ELEVENLABS_VOICE_ID="v", RUNWAY_API_KEY="k")
    b = BudgetLedger(BudgetPolicy(soft_limit=1.0, hard_limit=5.0))
    with pytest.raises(PaidOperationNotConfirmed):
        elevenlabs.generate_speech(e, episode_id="PD-2026-001-miranda", chunk_id="VC-0001", text="hi", confirmed=False, budget=b)
    with pytest.raises(PaidOperationNotConfirmed):
        runway.generate_video(e, episode_id="PD-2026-001-miranda", shot_id="S001", prompt="x", confirmed=False, budget=b)
    with pytest.raises(PaidOperationNotConfirmed):
        youtube.upload_video(e, episode_id="PD-2026-001-miranda", package_revision="v001", confirmed=False, channel_allowlist_id="UCxxxx")


def test_elevenlabs_confirmed_reserves_budget_then_not_implemented(tmp_path: Path):
    e = env_with(tmp_path, ELEVENLABS_API_KEY="k", ELEVENLABS_VOICE_ID="v")
    b = BudgetLedger(BudgetPolicy(soft_limit=1.0, hard_limit=5.0))
    # confirmed but execution intentionally disabled in prep -> NotImplementedError after reserving
    with pytest.raises(NotImplementedError):
        elevenlabs.generate_speech(e, episode_id="PD-2026-001-miranda", chunk_id="VC-0001", text="x" * 1000, confirmed=True, budget=b)
    assert b.reserved > 0  # budget frame engaged
