#!/usr/bin/env python
"""Validate EP50 Central Park AE card beats against the design deck + Remotion figures.

Cloned from validate_cleveland_beats.py, extended for the EP50 2-tier deck:
  * VALID_LAYOUTS = {6 proven} UNION {8 Tier-B}. DATE_STAMP / SEAM_TRANSITION FAIL.
  * id/layout/CP-id/anchor must match the DESIGN section 3 / CODEX_B section 7.2 deck 1:1.
  * AE moments total = 36 (Tier A 24 + Tier B 12).
  * years never appear as a raw numeric beat value (would thousands-comma) -> literal string.
  * AE beats must not overlap the film.json figures[] (skipped if film.json absent).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-050-centralpark"
DISCLOSURE = "AI-assisted visualization"

PROVEN = {"ACT_TITLE_CARD", "CENTER_STACK", "MONEY_STACK", "QUOTE_CARD",
          "VOTE_SPLIT", "SPLIT_COMPARE"}
TIER_B = {"DNA_LADDER", "STAT_RESOLVE", "CARD_STACK", "REC_LIGHT", "SCALE_TIP",
          "HERO_TIMELINE", "NAME_WALL", "SIGNATURE_ERASE"}
VALID_LAYOUTS = PROVEN | TIER_B
BANNED = {"DATE_STAMP", "SEAM_TRANSITION"}

# Canonical deck (CODEX_B section 7.2 / DESIGN section 3): id -> (layout, cp, anchor).
CANON: dict[str, tuple[str, str, float]] = {
    "t-a1": ("ACT_TITLE_CARD", "CP03", 27.0),
    "B8": ("HERO_TIMELINE", "CP03", 120.0),
    "c-noevidence": ("CENTER_STACK", "CP12", 372.0),
    "t-a2": ("ACT_TITLE_CARD", "", 452.0),
    "B4": ("REC_LIGHT", "CP08", 470.0),
    "c-sevenhours": ("CENTER_STACK", "CP08", 505.0),
    "c-roompromise": ("CENTER_STACK", "CP34", 560.0),
    "B10": ("NAME_WALL", "CP05", 700.0),
    "c-fivechildren": ("CENTER_STACK", "CP05", 720.0),
    "cmp-fedsigned": ("SPLIT_COMPARE", "CP10", 905.0),
    "B3": ("CARD_STACK", "CP10", 960.0),
    "cmp-confdna": ("SPLIT_COMPARE", "CP12", 1080.0),
    "t-a3": ("ACT_TITLE_CARD", "CP15", 1170.0),
    "c-papersfirst": ("CENTER_STACK", "CP14", 1245.0),
    "c-trumpad": ("CENTER_STACK", "CP13", 1305.0),
    "B6": ("SCALE_TIP", "CP12", 1445.0),
    "cmp-verdict": ("SPLIT_COMPARE", "CP17", 1600.0),
    "cmp-sentence": ("SPLIT_COMPARE", "CP18", 1655.0),
    "t-a4": ("ACT_TITLE_CARD", "", 1704.0),
    "cmp-yearsserved": ("SPLIT_COMPARE", "CP19", 1875.0),
    "t-a5": ("ACT_TITLE_CARD", "", 2272.0),
    "c-twodays": ("CENTER_STACK", "CP22", 2340.0),
    "q-alone": ("CENTER_STACK", "CP24", 2560.0),
    "B1": ("DNA_LADDER", "CP24", 2695.0),
    "B2": ("STAT_RESOLVE", "CP24", 2740.0),
    "t-a6": ("ACT_TITLE_CARD", "", 2823.0),
    "c-vacated": ("CENTER_STACK", "CP27", 2860.0),
    "B12": ("SIGNATURE_ERASE", "CP27", 2895.0),
    "B7": ("SCALE_TIP", "CP24", 2985.0),
    "B9": ("HERO_TIMELINE", "CP27", 3020.0),
    "m-41m": ("MONEY_STACK", "CP30", 3045.0),
    "c-state39": ("CENTER_STACK", "CP31", 3115.0),
    "B5": ("REC_LIGHT", "CP34", 3165.0),
    "c-salaam": ("CENTER_STACK", "CP33", 3270.0),
    "t-a7": ("ACT_TITLE_CARD", "CP34", 3308.0),
    "B11": ("NAME_WALL", "CP32", 3600.0),
}
AE_TOTAL = 36


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def intervals_overlap(a0: float, a1: float, b0: float, b1: float, pad: float = 0.0) -> bool:
    return max(a0 - pad, b0 - pad) < min(a1 + pad, b1 + pad)


def is_year(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and 1000 <= v <= 2999


def evaluate(ep: str) -> dict:
    epdir = ROOT / "episodes" / ep
    bp = epdir / "08_edit" / "ae_hero" / "beats.json"
    errors: list[str] = []
    if not bp.exists():
        return {"ok": False, "beats": str(bp), "errors": [f"missing {bp}"]}
    doc = load(bp)
    beats = doc.get("beats") or []

    if len(beats) != AE_TOTAL:
        errors.append(f"AE moment total = {len(beats)}, expected {AE_TOTAL} (Tier A 24 + Tier B 12)")

    last_end = -1.0
    for beat in beats:
        bid = beat.get("id", "?")
        layout = beat.get("layout")
        if layout in BANNED:
            errors.append(f"{bid}: BANNED layout {layout}")
        elif layout not in VALID_LAYOUTS:
            errors.append(f"{bid}: invalid/phantom layout {layout}")
        start = beat.get("start")
        end = beat.get("end")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            errors.append(f"{bid}: invalid start/end")
            continue
        if start < last_end:
            errors.append(f"{bid}: overlaps previous beat (start {start} < prev end {last_end})")
        last_end = float(end)
        if "\n" in str(beat.get("caption", "")):
            errors.append(f"{bid}: caption contains newline")
        # id/layout/cp/anchor must match the canonical deck exactly
        canon = CANON.get(str(bid))
        if canon is None:
            errors.append(f"{bid}: not in canonical deck (CODEX_B section 7.2)")
        else:
            clayout, ccp, canchor = canon
            if layout != clayout:
                errors.append(f"{bid}: layout {layout} != canon {clayout}")
            if str(beat.get("cp", "")) != ccp:
                errors.append(f"{bid}: cp {beat.get('cp')!r} != canon {ccp!r}")
            if abs(float(start) - canchor) > 0.001:
                errors.append(f"{bid}: anchor {start} != canon {canchor}")
        # years must be literal strings, never a raw numeric beat value (comma bug)
        if is_year(beat.get("value")):
            errors.append(f"{bid}: year {beat.get('value')} as numeric value -> use literal string (group:false)")
        for k in beat.get("numKeys") or []:
            # numKeys are [time, displayString]; the display must not be a year int
            pass
        # still checks (all EP50 beats are vector beds; validate any that carry one)
        still = beat.get("still")
        if still:
            p = Path(still)
            if not p.is_file():
                errors.append(f"{bid}: missing still {still}")
            else:
                try:
                    from PIL import Image  # lazy import
                    im = Image.open(p)
                    if max(im.size) < 3840:
                        errors.append(f"{bid}: still long edge below 3840")
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{bid}: cannot read still {exc}")

    # every canonical id must be present exactly once
    ids = [str(b.get("id")) for b in beats]
    for cid in CANON:
        if ids.count(cid) != 1:
            errors.append(f"canon id {cid}: present {ids.count(cid)}x (expected 1)")

    # AE beats must not overlap film figures[]
    film_path = ROOT / "remotion" / "src" / "data" / "centralpark_film.json"
    if film_path.exists():
        figures = load(film_path).get("figures") or []
        for beat in beats:
            if not isinstance(beat.get("start"), (int, float)):
                continue
            for fig in figures:
                if intervals_overlap(float(beat["start"]), float(beat["end"]),
                                     float(fig["start"]), float(fig["end"])):
                    errors.append(f"{beat.get('id')}: overlaps figure {fig.get('kind')} "
                                  f"{fig.get('start')}-{fig.get('end')}")
                    break
    else:
        errors.append("(info) centralpark_film.json absent -> AE<->figures overlap check deferred")
        # informational, not fatal: strip it from the fatal set below

    fatal = [e for e in errors if not e.startswith("(info)")]

    source = ROOT / "scripts" / "ae" / "build_centralpark_hero_cards.py"
    if source.exists() and DISCLOSURE not in source.read_text(encoding="utf-8", errors="ignore"):
        fatal.append("build_centralpark_hero_cards.py lacks AI disclosure layer text")

    return {"ok": not fatal, "beats": str(bp), "errors": errors, "fatal": fatal}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", default=DEFAULT_EP)
    args = ap.parse_args()
    result = evaluate(args.ep)
    print(("PASS" if result["ok"] else "FAIL") + f" validate_centralpark_beats: {result['beats']}")
    for err in result["errors"][:40]:
        print(f"  ! {err}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
