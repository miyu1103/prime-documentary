#!/usr/bin/env python
"""Validate EP49 Strieff AE card beats against Remotion figures."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-049-strieff"
EPDIR = ROOT / "episodes" / EP
VALID_LAYOUTS = {"DATE_STAMP", "CENTER_STACK", "MONEY_STACK", "SPLIT_COMPARE", "ACT_TITLE_CARD", "QUOTE_CARD", "VOTE_SPLIT", "SEAM_TRANSITION"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def overlap(a0: float, a1: float, b0: float, b1: float, pad: float = 1.0) -> bool:
    return max(a0 - pad, b0 - pad) < min(a1 + pad, b1 + pad)


def main() -> int:
    argparse.ArgumentParser().parse_args()
    errors: list[str] = []
    beats_path = EPDIR / "08_edit" / "ae_hero" / "beats.json"
    film_path = ROOT / "remotion" / "src" / "data" / "strieff_film.json"
    if not beats_path.is_file():
        errors.append(f"missing {beats_path}")
        beats = []
    else:
        beats = load(beats_path).get("beats") or []
    last = -1.0
    for beat in beats:
        bid = beat.get("id", "?")
        if beat.get("layout") not in VALID_LAYOUTS:
            errors.append(f"{bid}: invalid layout {beat.get('layout')}")
        start = beat.get("start")
        end = beat.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            errors.append(f"{bid}: invalid start/end")
            continue
        if float(start) < last:
            errors.append(f"{bid}: overlaps previous beat")
        last = float(end)
        if "dochighlight" in json.dumps(beat, ensure_ascii=False).lower():
            errors.append(f"{bid}: dochighlight forbidden")
    if film_path.is_file():
        figures = load(film_path).get("figures") or []
        for beat in beats:
            if "start" not in beat or "end" not in beat:
                continue
            for fig in figures:
                if overlap(float(beat["start"]), float(beat["end"]), float(fig["start"]), float(fig["end"])):
                    errors.append(f"{beat.get('id')}: overlaps figure {fig.get('kind')} {fig.get('start')}-{fig.get('end')}")
                    break
    print(("PASS" if not errors else "FAIL") + f" validate_strieff_beats: {beats_path}")
    for err in errors[:40]:
        print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
