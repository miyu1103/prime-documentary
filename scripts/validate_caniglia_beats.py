#!/usr/bin/env python
"""Validate EP43 AE card beats against Remotion figures."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-043-caniglia"
EPDIR = ROOT / "episodes" / EP
VALID_LAYOUTS = {"DATE_STAMP", "CENTER_STACK", "MONEY_STACK", "SPLIT_COMPARE", "ACT_TITLE_CARD", "QUOTE_CARD", "VOTE_SPLIT", "SEAM_TRANSITION"}
DISCLOSURE = "AI-assisted visualization"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def intervals_overlap(a0: float, a1: float, b0: float, b1: float, pad: float = 0.0) -> bool:
    return max(a0 - pad, b0 - pad) < min(a1 + pad, b1 + pad)


def beat_path(dryrun: bool) -> Path:
    if dryrun:
        return EPDIR / "08_edit" / "_dryrun" / "ae_hero" / "beats.json"
    return EPDIR / "08_edit" / "ae_hero" / "beats.json"


def evaluate(dryrun: bool = False) -> dict:
    errors: list[str] = []
    bp = beat_path(dryrun)
    if not bp.exists():
        return {"ok": False, "errors": [f"missing {bp}"]}
    doc = load(bp)
    beats = doc.get("beats") or []
    last_end = -1.0
    for beat in beats:
        bid = beat.get("id", "?")
        if beat.get("layout") not in VALID_LAYOUTS:
            errors.append(f"{bid}: invalid layout {beat.get('layout')}")
        start = beat.get("start")
        end = beat.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            errors.append(f"{bid}: invalid start/end")
            continue
        if start < last_end:
            errors.append(f"{bid}: overlaps previous beat")
        last_end = float(end)
        if "\n" in str(beat.get("caption", "")):
            errors.append(f"{bid}: caption contains newline")
        still = beat.get("still")
        if still:
            p = Path(still)
            if not p.is_file():
                errors.append(f"{bid}: missing still {still}")
            else:
                try:
                    im = Image.open(p)
                    if max(im.size) < 3840:
                        errors.append(f"{bid}: still long edge below 3840")
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{bid}: cannot read still {exc}")

    film_path = ROOT / "remotion" / "src" / "data" / "caniglia_film.json"
    if film_path.exists():
        figures = load(film_path).get("figures") or []
        for beat in beats:
            for fig in figures:
                if intervals_overlap(float(beat["start"]), float(beat["end"]), float(fig["start"]), float(fig["end"])):
                    errors.append(f"{beat.get('id')}: overlaps figure {fig.get('kind')} {fig.get('start')}-{fig.get('end')}")
                    break

    source = ROOT / "scripts" / "ae" / "build_caniglia_hero_cards.py"
    if source.exists() and DISCLOSURE not in source.read_text(encoding="utf-8", errors="ignore"):
        errors.append("build_caniglia_hero_cards.py lacks AI disclosure layer text")
    return {"ok": not errors, "beats": str(bp), "errors": errors}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dryrun", action="store_true")
    args = ap.parse_args()
    result = evaluate(args.dryrun)
    print(("PASS" if result["ok"] else "FAIL") + f" validate_caniglia_beats: {result['beats']}")
    for err in result["errors"][:30]:
        print(f"  ! {err}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

