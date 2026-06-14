"""Tests for the download watcher's pure logic (classification + non-colliding naming)."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import download_watcher as dw  # noqa: E402


def test_classify_by_extension():
    assert dw.classify("artwork.PNG") == "image"
    assert dw.classify("scene.jpeg") == "image"
    assert dw.classify("track.mp3") == "music"
    assert dw.classify("clip.MP4") == "video"
    assert dw.classify("notes.txt") is None  # unknown -> not moved


def test_is_temp_download():
    assert dw.is_temp(Path("a.png.crdownload"))
    assert dw.is_temp(Path("b.mp4.part"))
    assert not dw.is_temp(Path("c.png"))


def test_next_name_increments(tmp_path: Path):
    n1 = dw.next_name(tmp_path, "image", ".png", today="20260614")
    assert n1 == "img_20260614_001.png"
    (tmp_path / n1).write_bytes(b"x")
    n2 = dw.next_name(tmp_path, "image", ".png", today="20260614")
    assert n2 == "img_20260614_002.png"


def test_next_name_per_type_and_ext(tmp_path: Path):
    assert dw.next_name(tmp_path, "music", ".mp3", today="20260614") == "mus_20260614_001.mp3"
    assert dw.next_name(tmp_path, "video", ".MOV", today="20260614") == "vid_20260614_001.mov"
