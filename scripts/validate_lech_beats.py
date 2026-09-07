#!/usr/bin/env python
"""Validate EP40 Lech AE beat windows against Remotion figure windows."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
EPDIR = ROOT / "episodes" / "PD-2026-040-lech"
PUBLIC = ROOT / "remotion" / "public"
BEATS_DRY = EPDIR / "08_edit" / "_dryrun" / "ae_hero" / "beats.json"
BEATS_PROD = EPDIR / "08_edit" / "ae_hero" / "beats.json"
FILM = ROOT / "remotion" / "src" / "data" / "lech_film.json"
SLOTS = EPDIR / "03_script" / "lech_slots.stub.v001.json"

LAYOUTS = {
    "CENTER_STACK", "SPLIT_COMPARE", "DATE_STAMP", "RATIO_BAR", "ACT_TITLE_CARD",
    "DOCUMENT_CARD", "SIEGE_TIMELINE", "CASE_TIMELINE", "HOUSE_PLAN", "SEAM_TRANSITION",
}
VECTOR_LAYOUTS = {"SIEGE_TIMELINE", "CASE_TIMELINE", "HOUSE_PLAN", "SEAM_TRANSITION"}
BANNED_ZONE = re.compile(r"supreme\s*court|最高裁|SCOTUS", re.IGNORECASE)
ALLOWED_CONTEXT = re.compile(r"declined to hear|denied review|did not take the case|cert(iorari)?\s+(was\s+)?denied|let the ruling stand|never ruled on", re.IGNORECASE)


def intervals_overlap(a_start: float, a_end: float, b_start: float, b_end: float, pad: float = 0.0) -> bool:
    return a_start < b_end + pad and b_start < a_end + pad


def text_ok(value: str) -> bool:
    if not value:
        return True
    if BANNED_ZONE.search(value) and not ALLOWED_CONTEXT.search(value):
        return False
    return True


def load_beats() -> list[dict]:
    path = BEATS_DRY if BEATS_DRY.exists() else BEATS_PROD
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("beats", data if isinstance(data, list) else [])
    if not SLOTS.exists():
        return []
    return json.loads(SLOTS.read_text(encoding="utf-8")).get("beats", [])


def main() -> int:
    violations = []
    beats = load_beats()
    if len(beats) != 23:
        violations.append({"rule": "beats_count", "actual": len(beats), "expected": 23})
    prev_end = None
    for b in beats:
        start, end = float(b["start"]), float(b["end"])
        if prev_end is not None and start < prev_end:
            violations.append({"rule": "ae_overlap", "id": b.get("id")})
        prev_end = end
        if start < 8.1 + 3.5 or end > 732.4:
            violations.append({"rule": "body_window", "id": b.get("id"), "start": start, "end": end})
        layout = b.get("layout")
        if layout not in LAYOUTS:
            violations.append({"rule": "layout", "id": b.get("id"), "layout": layout})
        still = b.get("still")
        if layout in VECTOR_LAYOUTS and still:
            violations.append({"rule": "vector_still_must_be_null", "id": b.get("id")})
        if layout not in VECTOR_LAYOUTS and not still:
            violations.append({"rule": "still_required", "id": b.get("id")})
        if still:
            p = Path(still)
            if not p.is_absolute():
                p = PUBLIC / still
            if not p.exists():
                violations.append({"rule": "still_exists", "id": b.get("id"), "still": str(p)})
            else:
                with Image.open(p) as im:
                    if max(im.size) < 3840:
                        violations.append({"rule": "still_long_edge", "id": b.get("id"), "size": im.size})
        for key in ("top", "bottom", "caption", "footnote", "act_title"):
            if b.get(key) and not text_ok(str(b[key])):
                violations.append({"rule": "accuracy_text", "id": b.get("id"), "field": key})
        for line in b.get("doc_lines") or []:
            if not text_ok(str(line)):
                violations.append({"rule": "accuracy_doc_line", "id": b.get("id")})
        for event in b.get("timeline_events") or []:
            if not text_ok(str(event.get("text") or "")):
                violations.append({"rule": "accuracy_timeline_event", "id": b.get("id")})
        if "\n" in str(b.get("caption") or ""):
            violations.append({"rule": "caption_newline", "id": b.get("id")})
        if layout == "SPLIT_COMPARE":
            if not b.get("label_a") or not b.get("label_b") or not b.get("numKeys_b"):
                violations.append({"rule": "split_compare_payload", "id": b.get("id")})
        if layout == "RATIO_BAR" and b.get("ratio_note") != "CALCULATED FROM THE TWO FIGURES ABOVE":
            violations.append({"rule": "ratio_note", "id": b.get("id")})
        if layout == "ACT_TITLE_CARD" and (not b.get("act_index") or not b.get("act_title")):
            violations.append({"rule": "act_payload", "id": b.get("id")})
        if layout == "DOCUMENT_CARD":
            lines = b.get("doc_lines") or []
            if not 1 <= len(lines) <= 3 or any(not 1 <= len(str(line)) <= 46 or str(line) != str(line).upper() or "\n" in str(line) for line in lines):
                violations.append({"rule": "document_payload", "id": b.get("id")})
        if layout in {"SIEGE_TIMELINE", "CASE_TIMELINE"}:
            events = b.get("timeline_events") or []
            if not 3 <= len(events) <= 6 or any(not e.get("t") or not e.get("text") or len(str(e.get("text"))) > 24 for e in events):
                violations.append({"rule": "timeline_payload", "id": b.get("id")})
        if layout == "HOUSE_PLAN":
            rooms = b.get("plan_rooms") or []
            breaches = b.get("plan_breaches")
            if len(rooms) < 2 or breaches is None or (b.get("id") == "h02" and not breaches):
                violations.append({"rule": "house_plan_payload", "id": b.get("id")})
        if layout == "SEAM_TRANSITION":
            expected = {"s01": "dip", "s02": "wipe", "s03": "wipe", "s04": "grain"}.get(str(b.get("id")))
            if b.get("seam_mode") != expected or b.get("head") != 0.0 or b.get("tail") != 0.0:
                violations.append({"rule": "seam_payload", "id": b.get("id")})
        if b.get("id") == "b08":
            expected = {
                "top": "THE TENTH CIRCUIT",
                "value": 2019,
                "bottom": "NO COMPENSATION OWED",
                "footnote": "THE SUPREME COURT DECLINED TO HEAR IT",
            }
            if any(b.get(k) != v for k, v in expected.items()):
                violations.append({"rule": "b08_accuracy_payload", "id": b.get("id")})
    figures = []
    figures_are_body_relative = False
    if FILM.exists():
        figures = json.loads(FILM.read_text(encoding="utf-8")).get("figures", [])
        figures_are_body_relative = True
    elif SLOTS.exists():
        figures = json.loads(SLOTS.read_text(encoding="utf-8")).get("figures", [])
    if len(figures) != 17:
        violations.append({"rule": "figures_count", "actual": len(figures), "expected": 17})
    for b in beats:
        for f in figures:
            offset = 11.6 if figures_are_body_relative else 0.0
            f_start = float(f["start"]) + offset
            f_end = float(f["end"]) + offset
            if intervals_overlap(float(b["start"]), float(b["end"]), f_start, f_end, pad=1.0):
                violations.append({"rule": "ae_figure_overlap_1s", "beat": b.get("id"), "figure": f.get("id"), "beat_window": [b["start"], b["end"]], "figure_window": [f["start"], f["end"]]})
    if violations:
        print(json.dumps(violations, ensure_ascii=False, indent=2))
        return 1
    print(f"PASS validate_lech_beats: {len(beats)} AE beats, {len(figures)} figures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
