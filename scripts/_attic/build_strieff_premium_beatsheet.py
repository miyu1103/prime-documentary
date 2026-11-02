#!/usr/bin/env python
"""Build a CaseFilm-derived premium beatsheet for EP49 animation_mix validation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-049-strieff"
FILM = ROOT / "remotion" / "src" / "data" / "strieff_film.json"
OUT = ROOT / "episodes" / EP / "04_scenes" / "premium_beatsheet.v001.json"


def main() -> int:
    film = json.loads(FILM.read_text(encoding="utf-8"))
    fps = int(film.get("fps") or 30)
    beats = []
    for cut in film.get("cuts") or []:
        start_frame = int(round(float(cut["start"]) * fps))
        dur_frames = max(1, int(round(float(cut["dur"]) * fps)))
        is_still = cut.get("kind") == "img"
        beats.append(
            {
                "id": cut["id"],
                "kind": "hero" if is_still else "factory",
                "component": "WilliamsScene" if is_still else "FactoryClip",
                "start_frame": start_frame,
                "dur_frames": dur_frames,
                "src": cut.get("src"),
            }
        )
    for idx, fig in enumerate(film.get("figures") or [], 1):
        start_frame = int(round(float(fig["start"]) * fps))
        dur_frames = max(1, int(round((float(fig["end"]) - float(fig["start"])) * fps)))
        beats.append(
            {
                "id": f"fig-{idx:03d}",
                "kind": "mg_hero",
                "component": f"FigureBeats:{fig.get('kind', 'unknown')}",
                "start_frame": start_frame,
                "dur_frames": dur_frames,
                "figure_kind": fig.get("kind"),
            }
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {
                "schema_version": "premium_beatsheet.v1",
                "episode_id": EP,
                "meta": {"fps": fps, "source": "remotion/src/data/strieff_film.json"},
                "beats": beats,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT} beats={len(beats)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
