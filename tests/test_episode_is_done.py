"""`done` must be answered from bytes. These are the four ways the old mtime check was wrong.

Each test is a failure that actually happened, or that the old check would have produced:

  * the master ships as v002 -- the old check looked only at v001 and said "not done"
  * the receipt stores `sha256:<hex>`; comparing that to a bare digest reports NO MATCH for
    every episode on the channel. It fooled the author of this module first.
  * a master exists but is not the film that was accepted -- that is NOT done, however new it is
  * no receipt at all -- nothing has been accepted, so build it
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import episode_is_done as eid  # noqa: E402


@pytest.fixture
def fake(tmp_path, monkeypatch):
    """A minimal episode tree. Returns a builder: (master_versions, receipt_sha) -> slug."""
    monkeypatch.setattr(eid, "ROOT", tmp_path)

    def build(masters: dict[str, bytes], receipt_sha: str | None, slug: str = "demo") -> str:
        ep = tmp_path / "episodes" / f"PD-2026-099-{slug}"
        (ep / "08_edit").mkdir(parents=True)
        (ep / "09_package").mkdir(parents=True)
        for name, blob in masters.items():
            (ep / "08_edit" / name).write_bytes(blob)
        if receipt_sha is not None:
            (ep / "09_package" / "acceptance_receipt.v001.json").write_text(
                json.dumps({"video_sha256": receipt_sha}), encoding="utf-8")
        return slug

    return build


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def test_a_v002_master_counts_as_done(fake):
    """The old check hard-coded v001. Six of seven live episodes ship v002."""
    blob = b"the film that was accepted"
    slug = fake({"demo_final_bgm.v001.mp4": b"an older cut",
                 "demo_final_bgm.v002.mp4": blob}, sha(blob))
    rc, why = eid.verdict(slug)
    assert rc == eid.DONE and "v002" in why


def test_the_sha256_prefix_in_the_receipt_is_stripped(fake):
    """`sha256:2d368d...` vs a bare digest reported NO MATCH for the whole channel."""
    blob = b"the film that was accepted"
    slug = fake({"demo_final_bgm.v001.mp4": blob}, f"sha256:{sha(blob)}")
    assert eid.verdict(slug)[0] == eid.DONE


def test_uppercase_and_whitespace_in_the_receipt_still_match(fake):
    blob = b"the film that was accepted"
    slug = fake({"demo_final_bgm.v001.mp4": blob}, f"  SHA256:{sha(blob).upper()}  ")
    assert eid.verdict(slug)[0] == eid.DONE


def test_a_newer_master_that_is_not_the_accepted_film_is_not_done(fake):
    """mtime would call this done. It is a different film."""
    slug = fake({"demo_final_bgm.v001.mp4": b"something else entirely"},
                sha(b"the film that was accepted"))
    rc, why = eid.verdict(slug)
    assert rc == eid.NOT_DONE and "not here" in why


def test_no_receipt_means_build_it(fake):
    slug = fake({"demo_final_bgm.v001.mp4": b"an unaccepted render"}, None)
    rc, why = eid.verdict(slug)
    assert rc == eid.NOT_DONE and "no acceptance receipt" in why


def test_receipt_without_a_usable_hash_is_unusable_not_done(fake):
    """Never answer 'done' from a receipt that cannot be read. Unusable builds; it does not skip."""
    slug = fake({"demo_final_bgm.v001.mp4": b"x"}, "not-a-hash")
    assert eid.verdict(slug)[0] == eid.UNUSABLE


def test_unknown_slug_is_unusable(fake):
    fake({}, None)
    assert eid.verdict("nosuchslug")[0] == eid.UNUSABLE


def test_the_seven_live_episodes_are_all_built():
    """The finding that motivated this: check_queue_will_stall called five of them lost."""
    for slug in ("marmet", "greene", "correa", "openfields", "ramirez", "pinto", "hyatt"):
        rc, why = eid.verdict(slug)
        assert rc == eid.DONE, f"{slug}: {why}"


def test_the_queue_no_longer_decides_from_mtime():
    src = (REPO / "scripts" / "queue_unattended.sh").read_text(encoding="utf-8")
    body = src[src.index("already_done()"):]
    body = body[:body.index("\n}")]
    assert "episode_is_done.py" in body
    assert "-ot " not in body, "already_done is comparing mtimes again"
    assert "v001.mp4" not in body, "already_done is hard-coding a master version again"
