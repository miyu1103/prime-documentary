"""The mux-order signal must run on every master version, and must never skip in silence.

WHAT WAS WRONG (measured 2026-08-23)
------------------------------------
`check_freshness` carries a third signal, added after a real near-miss: correa finished its
render, then `_finish_episode.sh` died before step 7, so the 08_edit master was a build from
three days earlier. Every other freshness signal passes on a stale master -- it has its own sha
and its own mtime. Only "is the master newer than the render it should contain" exposes it.

That signal was gated on the literal filename `<slug>_final_bgm.v001.mp4`. Seven shipped
episodes were graded on **v002** (marmet, greene, memphis, openfields, ramirez, pinto, hyatt).
On every one of them the signal did not run, did not fail, and did not warn. `render_freshness`
went green without it.

These tests hold the fix: the name is matched by SHAPE, and a name with no recognisable shape
produces a note rather than silence.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import check_final_acceptance as cfa  # noqa: E402


@pytest.fixture
def bench(tmp_path, monkeypatch):
    """A render and its raw source, with the mtimes under our control."""
    monkeypatch.setattr(cfa, "ROOT", tmp_path)
    (tmp_path / "out").mkdir()
    epdir = tmp_path / "episodes" / "PD-2026-099-demo"
    (epdir / "09_package").mkdir(parents=True)
    (epdir / "08_edit").mkdir(parents=True)

    def make(master_name: str, master_time: int, raw_time: int | None = 1_000_000):
        master = epdir / "08_edit" / master_name
        master.write_bytes(b"master")
        import os
        os.utime(master, (master_time, master_time))
        if raw_time is not None:
            raw = tmp_path / "out" / "demo.mp4"
            raw.write_bytes(b"raw")
            os.utime(raw, (raw_time, raw_time))
        return cfa.check_freshness(epdir, master, "a" * 64, None)

    return make


def _text(result) -> str:
    return str(result.get("reason", ""))


@pytest.mark.parametrize("name", [
    "demo_final_bgm.v001.mp4",
    "demo_final_bgm.v002.mp4",     # the version that silently skipped the signal
    "demo_final_bgm.v009.mp4",
    "demo_final_bgm.v003_ae.mp4",  # the After Effects variant
])
def test_a_master_older_than_its_render_fails_on_every_version(bench, name):
    r = bench(name, master_time=900_000, raw_time=1_000_000)
    assert r["ok"] is False
    assert "OLDER than the render" in _text(r), _text(r)


@pytest.mark.parametrize("name", ["demo_final_bgm.v001.mp4", "demo_final_bgm.v002.mp4"])
def test_a_master_newer_than_its_render_passes_and_says_so(bench, name):
    r = bench(name, master_time=1_000_060, raw_time=1_000_000)
    assert r["ok"] is True
    assert "muxed 60s after its render" in _text(r), _text(r)


def test_a_missing_raw_render_is_recorded_not_skipped_silently(bench):
    r = bench("demo_final_bgm.v002.mp4", master_time=1_000_060, raw_time=None)
    assert "mux-order signal not run" in _text(r), _text(r)


def test_an_unrecognisable_name_is_recorded_not_skipped_silently(bench):
    r = bench("demo_something_else.mp4", master_time=1_000_060, raw_time=1_000_000)
    assert "mux-order signal not run" in _text(r), _text(r)


def test_the_literal_v001_gate_is_gone():
    """The exact shape of the bug. If this literal comes back, the signal stops running again."""
    src = (REPO / "scripts" / "check_final_acceptance.py").read_text(encoding="utf-8")
    body = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("#"))
    assert 'suffix = "_final_bgm.v001.mp4"' not in body
    assert 'endswith(suffix)' not in body
