"""The experiment lock and the decision-expiry check must fail on the inputs they exist for.

A check that has never been shown to fail is decoration (docs/HANDOVER.md, permanent rule 5).
These tests are the standing demonstration:

  * a control video of a running experiment cannot be retitled
  * a treated video cannot have its thumbnail changed either
  * an unrelated id passes
  * the lock lifts by itself on the read date -- nobody has to remember to remove it
  * apply_title_batch.py calls the lock BEFORE its first write, not after
  * a decision past its own review date is EXPIRED; one on/after the cutoff with no
    Review by / Revoke if is MISSING; a well-formed one is OK
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_decisions  # noqa: E402
import pd_experiments  # noqa: E402

TITLE_EXPERIMENT = "title-band-2026-08-10"
A_CONTROL = "Enok7A7wGBA"        # named in TITLE_EXPERIMENT_RECEIPT.v001.md section 6
A_TREATED = "marQjsCagh0"        # OceanGate, inside the applied 39
BEFORE_READ = dt.date(2026, 9, 1)
AFTER_READ = dt.date(2026, 9, 8)


def test_register_validates():
    assert pd_experiments.validate() == 0


def test_both_arms_are_locked_before_the_read_date():
    for kind in ("title", "thumbnail"):
        lk = pd_experiments.locks(kind, on=BEFORE_READ)
        assert A_CONTROL in lk, f"{A_CONTROL} must be locked against a {kind} change"
        assert A_TREATED in lk, f"{A_TREATED} must be locked against a {kind} change"
        assert any(TITLE_EXPERIMENT in r for r in lk[A_CONTROL])


def test_assert_unlocked_raises_on_a_control():
    with pytest.raises(SystemExit) as e:
        pd_experiments.assert_unlocked([A_CONTROL], "title")
    assert "REFUSING" in str(e.value) and A_CONTROL in str(e.value)


def test_assert_unlocked_passes_an_unrelated_id():
    pd_experiments.assert_unlocked(["not-a-real-video-id"], "title")


def test_the_lock_lifts_on_the_read_date_without_anyone_removing_it():
    assert A_CONTROL not in pd_experiments.locks("title", on=AFTER_READ)


def test_the_treated_arm_is_derived_from_the_record_the_write_produced():
    """Not copied into the register -- so it cannot drift from what was actually written."""
    exp = next(e for e in pd_experiments.load()["experiments"]
               if e["experiment_id"] == TITLE_EXPERIMENT)
    assert "derived_from" in exp["arms"]["treated"]
    assert len(pd_experiments._arm_ids(exp, "treated")) == 39
    assert len(pd_experiments._arm_ids(exp, "control")) == 13


def test_apply_title_batch_checks_the_lock_before_its_first_write():
    src = (ROOT / "scripts" / "apply_title_batch.py").read_text(encoding="utf-8").splitlines()
    guard = next(i for i, l in enumerate(src) if "pd_experiments.assert_unlocked" in l)
    writes = [i for i, l in enumerate(src) if 'http("PUT"' in l]
    forward = [i for i in writes if i > guard]
    assert forward, "no write found after the guard -- the wiring moved"
    assert guard < min(forward)


def _scan(tmp_path: Path, name: str, body: str) -> dict:
    (tmp_path / name).write_text(body, encoding="utf-8")
    original = check_decisions.DECISIONS
    check_decisions.DECISIONS = tmp_path
    try:
        return {r["path"].name: r["state"] for r in check_decisions.scan()}
    finally:
        check_decisions.DECISIONS = original


def test_decision_past_its_review_date_is_expired(tmp_path):
    body = ("# ADR-0099\n\n**Status:** Accepted (2026-08-01)\n"
            "**Review by:** 2026-08-10\n**Revoke if:** CTR stays under 2.0%\n")
    assert _scan(tmp_path, "0099.md", body)["0099.md"] == "EXPIRED"


def test_new_decision_without_the_two_lines_is_missing(tmp_path):
    after = check_decisions.CUTOFF + dt.timedelta(days=1)
    body = f"# ADR-0100\n\n**Status:** Accepted (owner directive, {after}). Binding.\n"
    assert _scan(tmp_path, "0100.md", body)["0100.md"] == "MISSING"


def test_pre_cutoff_decision_is_legacy_not_a_failure(tmp_path):
    body = "# ADR-0001\n\n**Status:** Accepted (2026-06-01)\n"
    assert _scan(tmp_path, "0001.md", body)["0001.md"] == "LEGACY"


def test_well_formed_decision_is_ok(tmp_path):
    after = check_decisions.CUTOFF + dt.timedelta(days=1)
    body = (f"# ADR-0101\n\n**Status:** Accepted ({after})\n"
            "**Review by:** 2099-01-01\n"
            "**Revoke if:** long-form CTR has not exceeded 2.0% "
            "(scripts/_yt_studio_video_ctr.*.json)\n")
    assert _scan(tmp_path, "0101.md", body)["0101.md"] == "OK"


def test_the_live_register_of_decisions_is_clean():
    """Guards the real decisions/ directory: nothing expired, nothing new left undated."""
    states = [r["state"] for r in check_decisions.scan()]
    assert "EXPIRED" not in states
    assert "MISSING" not in states


def test_adr_0011_carries_a_measurable_revoke_condition():
    text = (ROOT / "decisions" / "0011-AE-FROM-EP77.md").read_text(encoding="utf-8")
    m = check_decisions.RE_REVOKE.search(text)
    assert m and re.search(r"\d", m.group(1)), "a revoke condition must name a number"
