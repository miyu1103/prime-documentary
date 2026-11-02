"""Every gate must still reject the input it exists to reject, on every test run.

`scripts/check_gates_still_bite.py` is wired into the render queue so three GPU-hours are never
spent on a film that will be judged by a check which cannot fail. This file runs the same
probes in the ordinary suite, so the failure surfaces at commit time rather than at 3am.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import check_gates_still_bite as gb  # noqa: E402


@pytest.mark.parametrize("probe", gb.PROBES, ids=lambda p: p.name)
def test_gate_still_bites(probe):
    r = probe.run()
    assert r.bit, (f"{probe.name} accepted an input it must reject. "
                   f"It now lets through: {probe.guards}. Gate said: {r.detail}")


def test_the_probes_are_wired_into_the_render_queue():
    """A self-test nobody runs is the same decoration it was written to replace."""
    src = (REPO / "scripts" / "queue_unattended.sh").read_text(encoding="utf-8")
    assert "check_gates_still_bite.py" in src
    body = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("#"))
    assert body.index("check_gates_still_bite.py") < body.index('JOBS="'), \
        "the self-test must run BEFORE the job list, not after"


def test_every_probe_names_the_real_failure_it_guards():
    """`guards` is printed when a gate goes blunt. A vague one wastes the alarm."""
    for p in gb.PROBES:
        assert len(p.guards) > 20, f"{p.name}: say what actually gets through"
