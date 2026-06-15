"""Derive player metadata from repo sources — never hardcode fps/duration (P0 spec §5.3).

fps comes from remotion/src/brand.ts; duration from the sum of scene_plan durations.
The client also reads the actual <video>.duration as the authoritative cross-check.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
BRAND_TS = REPO_ROOT / "remotion" / "src" / "brand.ts"
SCENE_PLAN = REPO_ROOT / "episodes" / "PD-2026-001-miranda" / "04_scenes" / "scene_plan.v001.json"
# Prefer the full-res render; fall back to the half-res preview if that's all that exists.
MEDIA_CANDIDATES = [
    Path(r"H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample\sample_v011.mp4"),
    Path(r"H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample\sample_v010.mp4"),
    REPO_ROOT / "remotion" / "out" / "proof.mp4",
    REPO_ROOT / "remotion" / "out" / "animatic_motion.mp4",
    REPO_ROOT / "remotion" / "out" / "miranda-animatic.mp4",
    REPO_ROOT / "remotion" / "out" / "animatic_miranda.mp4",
]
DEFAULT_FPS = 30


def _fps_from_brand() -> int:
    if BRAND_TS.exists():
        m = re.search(r"fps:\s*(\d+)", BRAND_TS.read_text(encoding="utf-8"))
        if m:
            return int(m.group(1))
    return DEFAULT_FPS  # documented fallback (brand.ts unreadable)


def _duration_seconds_from_scene_plan() -> float | None:
    if not SCENE_PLAN.exists():
        return None
    sp = json.loads(SCENE_PLAN.read_text(encoding="utf-8"))
    return float(sum(s["duration_seconds"] for s in sp["scenes"]))


def media_file() -> Path | None:
    for p in MEDIA_CANDIDATES:
        if p.exists():
            return p
    return None


def build_meta() -> dict[str, Any]:
    fps = _fps_from_brand()
    dur = _duration_seconds_from_scene_plan()
    mp4 = media_file()
    return {
        "composition_id": "Animatic",
        "fps": fps,
        "duration_seconds": dur,
        "duration_frames": int(round(dur * fps)) if dur else None,
        "media_available": mp4 is not None,
        "media_name": mp4.name if mp4 else None,
        "source_revision": {"script": "v001", "scene_plan": "v001", "animatic": "v001"},
    }


if __name__ == "__main__":
    print(json.dumps(build_meta(), ensure_ascii=False, indent=2))
