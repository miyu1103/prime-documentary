#!/usr/bin/env python
"""EP23 strict sensitive-topic lock audit.

Read-only. This is intentionally stricter than check_final_acceptance.py because
EP23 is R3 + suicide-sensitive. Exit 0 only when the shippable surfaces satisfy
the current safe-handling contract.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-023-swartz"
EPDIR = ROOT / "episodes" / EP

BANNED = [
    "committed suicide",
    "killed himself",
    "took his own life",
    "suicide method",
    "method of suicide",
    "suicide note",
    "death scene",
    "reenactment",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def strip_srt_timing(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.strip().isdigit() or "-->" in line:
            continue
        lines.append(line)
    return "\n".join(lines)


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def has_unqualified_35_years(text: str) -> bool:
    plain = compact(text)
    explainer_match = re.search(
        r"this is the moment in the story where you have very likely heard one particular number attached\."
        r".{0,1800}?theoretical legal ceiling"
        r".{0,1800}?six months"
        r".{0,1800}?orin kerr"
        r".{0,900}?wildly overstated",
        plain,
        flags=re.IGNORECASE,
    )
    # The strict on-screen rule rejects a standalone "Thirty-five years." cue or
    # any plain "35 years" headline unless the same explanatory passage clearly
    # frames it as a theoretical maximum, not the expected sentence.
    if re.search(r"\b(?:thirty-five|35)\s+years[.!?]?(?:\s|$)", plain, flags=re.IGNORECASE):
        for m in re.finditer(r"\b(?:thirty-five|35)\s+years\b", plain, flags=re.IGNORECASE):
            window = plain[max(0, m.start() - 220): m.end() + 260].lower()
            broader = plain[max(0, m.start() - 900): m.end() + 1100].lower()
            locally_qualified = "theoretical" in broader and ("six months" in broader or "orin kerr" in broader)
            if not (locally_qualified or explainer_match):
                return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit EP23 sensitive-topic locks.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    narration_index = EPDIR / "06_audio" / "narration_index.v001.json"
    narration_text = ""
    if narration_index.exists():
        data = json.loads(read(narration_index))
        narration_text = " ".join(chunk.get("text", "") for chunk in data.get("chunks", []))

    captions = strip_srt_timing(read(EPDIR / "08_edit" / "captions.v001.srt"))
    description = read(EPDIR / "09_package" / "description.v001.md")
    thumb_public_parts: list[str] = []
    for path in [
        EPDIR / "09_package" / "title_thumbnail_candidates.v001.json",
        EPDIR / "09_package" / "title_thumbnail_plan.v001.json",
    ]:
        if not path.exists():
            continue
        try:
            data = json.loads(read(path))
        except json.JSONDecodeError:
            continue
        for title in data.get("titles", []) + data.get("title_options", []):
            thumb_public_parts.append(str(title.get("title", "")))
            thumb_public_parts.append(str(title.get("thumbnail_headline", "")))
        for thumb in data.get("thumbnails", []):
            thumb_public_parts.append(str(thumb.get("headline", "")))
    thumb_public_text = "\n".join(thumb_public_parts)

    shippable_text = "\n".join([captions, description, thumb_public_text])
    narration_suicide_count = count(r"\bsuicide\b", narration_text)
    caption_suicide_count = count(r"\bsuicide\b", captions)
    banned_hits = {term: count(re.escape(term), shippable_text) for term in BANNED}
    banned_hits = {k: v for k, v in banned_hits.items() if v}

    results = [
        {
            "check": "narration_suicide_once",
            "ok": narration_suicide_count == 1,
            "value": narration_suicide_count,
            "expected": 1,
        },
        {
            "check": "caption_suicide_once",
            "ok": caption_suicide_count == 1,
            "value": caption_suicide_count,
            "expected": 1,
        },
        {
            "check": "no_banned_suicide_wording_on_shippable_surfaces",
            "ok": not banned_hits,
            "value": banned_hits,
        },
        {
            "check": "no_unqualified_35_years_in_captions",
            "ok": not has_unqualified_35_years(captions),
        },
        {
            "check": "988_in_description",
            "ok": "988 Suicide & Crisis Lifeline -- call or text 988" in description,
        },
        {
            "check": "no_death_suicide_thumbnail_metadata",
            "ok": not re.search(r"\b(suicide|death|dead|died|killed)\b", thumb_public_text, flags=re.IGNORECASE),
        },
        {
            "check": "no_single_cause_thumbnail_metadata",
            "ok": not re.search(r"\b(caused his death|caused the death|drove him)\b", thumb_public_text, flags=re.IGNORECASE),
        },
    ]

    ok = all(item["ok"] for item in results)
    report = {"check": "ep23_sensitive_locks", "episode": EP, "status": "PASS" if ok else "FAIL", "results": results}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"{'PASS' if item['ok'] else 'FAIL'} {item['check']}: {item.get('value', '')}")
        print("RESULT:", report["status"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
