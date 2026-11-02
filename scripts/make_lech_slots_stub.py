#!/usr/bin/env python
"""Create EP40 Lech episode scaffolding and slot-contract stub."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EP = "PD-2026-040-lech"
EPDIR = ROOT / "episodes" / EP
SLOTS = EPDIR / "03_script" / "lech_slots.stub.v001.json"

ACTS = [
    (1, "An Ordinary House", 11.6, 350),
    (2, "The Siege Moves In", 131.5, 505),
    (3, "The House Comes Apart", 303.6, 510),
    (4, "Nobody Pays", 477.4, 575),
]

AE_BEATS = [
    ("t01", "ACT_TITLE_CARD", None, True, 11.600, 15.100, None),
    ("h01", "HOUSE_PLAN", None, True, 118.000, 124.000, None),
    ("s01", "SEAM_TRANSITION", None, True, 129.400, 131.400, None),
    ("t02", "ACT_TITLE_CARD", None, True, 131.500, 135.000, None),
    ("b01", "DATE_STAMP", "F07", True, 136.000, 141.000, "CT_DATE"),
    ("d01", "DOCUMENT_CARD", None, True, 200.000, 206.000, None),
    ("b02", "CENTER_STACK", "F01", True, 252.000, 258.000, "CT_NUMBER"),
    ("g01", "SIEGE_TIMELINE", "F01", True, 280.000, 288.000, None),
    ("s02", "SEAM_TRANSITION", None, True, 301.500, 303.500, None),
    ("t03", "ACT_TITLE_CARD", None, True, 303.600, 307.100, None),
    ("b03", "SPLIT_COMPARE", "F02", True, 312.000, 319.000, "CT_MONEY"),
    ("b04", "CENTER_STACK", "F06", False, 412.000, 417.500, "CT_NUMBER"),
    ("h02", "HOUSE_PLAN", None, True, 440.000, 447.000, None),
    ("s03", "SEAM_TRANSITION", None, True, 475.300, 477.300, None),
    ("t04", "ACT_TITLE_CARD", None, True, 477.400, 480.900, None),
    ("b05", "CENTER_STACK", "F03", True, 492.000, 498.000, "CT_MONEY"),
    ("d02", "DOCUMENT_CARD", None, True, 520.000, 526.500, None),
    ("d03", "DOCUMENT_CARD", "F03", False, 560.000, 566.000, None),
    ("b06", "CENTER_STACK", "F04", True, 605.000, 611.500, "CT_MONEY"),
    ("b07", "RATIO_BAR", "F05", False, 620.000, 626.000, "CT_PERCENT"),
    ("g02", "CASE_TIMELINE", "F09", True, 630.000, 638.000, None),
    ("b08", "DATE_STAMP", "F09", True, 655.000, 661.000, "CT_DATE"),
    ("s04", "SEAM_TRANSITION", None, True, 671.000, 673.000, None),
]

FIGURES = [
    ("f01", 20.0, 25.0, "lowerthird"),
    ("f02", 55.0, 60.0, "stat"),
    ("f03", 92.0, 97.0, "lowerthird"),
    ("f04", 150.0, 157.0, "routemap"),
    ("f05", 175.0, 180.0, "lowerthird"),
    ("f06", 215.0, 221.0, "quote"),
    ("f07", 265.0, 270.0, "stat"),
    ("f08", 330.0, 336.0, "kinetic"),
    ("f09", 360.0, 366.0, "compbars"),
    ("f10", 385.0, 390.0, "stat"),
    ("f11", 455.0, 461.0, "quote"),
    ("f12", 500.0, 507.0, "mechanism"),
    ("f13", 535.0, 541.0, "quote"),
    ("f14", 575.0, 582.0, "mechanism"),
    ("f15", 590.0, 596.0, "compbars"),
    ("f16", 645.0, 652.0, "mechanism"),
    ("f17", 700.0, 705.0, "lowerthird"),
]


def marker(path: str) -> str:
    return f"[[SLOT:{path}]]"


def words(n: int, label: str) -> str:
    base = [f"{label.lower()}word{i:03d}" for i in range(1, n + 1)]
    return " ".join(base) + "."


def ensure_dirs() -> None:
    for rel in [
        "00_topic", "01_research", "03_script", "04_scenes", "06_audio",
        "08_edit/ae_hero", "08_edit/_dryrun/ae_hero", "09_package",
        "approvals", "events",
    ]:
        (EPDIR / rel).mkdir(parents=True, exist_ok=True)


def build_slots() -> dict:
    hook_lines = [
        "A stranger ran into a family's quiet house.",
        "Police destroyed it to force him back out.",
        "Then the law said the loss was theirs.",
    ]
    beats = []
    for bid, layout, fact_id, required, start, end, count_type in AE_BEATS:
        beats.append({
            "id": bid,
            "layout": layout,
            "count_type": count_type or "CT_NONE",
            "fact_id": fact_id,
            "required": required,
            "start": start,
            "end": end,
            "top": marker(f"beats.{bid}.top"),
            "bottom": marker(f"beats.{bid}.bottom"),
            "caption": marker(f"beats.{bid}.caption"),
            "footnote": "THE SUPREME COURT DECLINED TO HEAR IT" if bid == "b08" else None,
        })
    figures = []
    for fid, start, end, kind in FIGURES:
        item = {"id": fid, "start": start, "end": end, "kind": kind}
        if kind == "stat":
            item.update({"value": 3, "label": marker(f"figures.{fid}.label"), "topLabel": marker(f"figures.{fid}.topLabel")})
        elif kind == "quote":
            item.update({"quote": marker(f"figures.{fid}.quote"), "attribution": marker(f"figures.{fid}.attribution")})
        elif kind == "kinetic":
            item.update({"lines": [marker(f"figures.{fid}.lines.0")], "style": "emphasis", "emphasisWords": ["WHO"]})
        elif kind == "compbars":
            item.update({"items": [{"label": marker(f"figures.{fid}.items.0.label"), "value": 1}]})
        elif kind == "mechanism":
            mech = {"f12": "faultsplit", "f14": "closingdoor", "f16": "gears"}[fid]
            item.update({"mechanism": mech})
        elif kind == "routemap":
            item.update({"pins": [{"x": 0.32, "y": 0.44, "label": marker(f"figures.{fid}.pins.0.label")}]})
        else:
            item.update({"primary": marker(f"figures.{fid}.primary"), "secondary": marker(f"figures.{fid}.secondary")})
        figures.append(item)
    facts = {
        f"F{i:02d}": {"value": None, "unit": "", "verified": False, "source_url": "", "quote": ""}
        for i in range(1, 10)
    }
    facts["F01"]["unit"] = "hours"
    facts["F02"]["unit"] = "usd"
    facts["F03"]["unit"] = "usd"
    facts["F04"]["unit"] = "usd"
    facts["F05"]["unit"] = "percent"
    facts["F06"]["unit"] = "count"
    facts["F07"]["unit"] = "date"
    facts["F08"]["unit"] = "people"
    facts["F09"]["unit"] = "year"
    return {
        "schema_version": "lech_slots.v1",
        "episode_id": EP,
        "slug": "lech",
        "accuracy_lock": {
            "court": "United States Court of Appeals for the Tenth Circuit",
            "court_short": "Tenth Circuit",
            "decision_year": 2019,
            "citation": "Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019)",
            "cert_denied_year": 2020,
            "is_supreme_court_decision": False,
        },
        "title_candidates": [
            {"text": "Police Destroyed Their House. Nobody Paid For It.", "variant": "A"},
            {"text": "Can Police Destroy Your Home And Pay You Nothing?", "variant": "B"},
        ],
        "thumb_headlines": [
            {"concept_id": "T1", "text": "YOUR HOUSE. THEIR CALL."},
            {"concept_id": "T2", "text": "STOLEN DESTROYED"},
            {"concept_id": "T3", "text": "THEY PAID NOTHING"},
        ],
        "hook": {"seconds": 8.1, "lines": hook_lines, "source_cut_ids": ["cut-000", "cut-001", "cut-002"]},
        "acts": [
            {
                "act": act,
                "title_ja": marker(f"acts.{act}.title_ja"),
                "title_card": title.upper(),
                "start_sec": start,
                "narration": words(target, f"act{act}"),
                "rehook_sec": [0.0],
                "open_loop_close": [f"L{act}"],
            }
            for act, title, start, target in ACTS
        ],
        "narration_total_words": 2140,
        "wpm_assumed": 178.1,
        "act_word_targets": [350, 505, 510, 575],
        "ed_word_target": 176,
        "beats": beats,
        "figures": figures,
        "ed": {
            "payoff_line": words(90, "edpayoff"),
            "cta_line": words(72, "edcta"),
            "question_line": "If it were your house, should the city pay or should you instead pay?",
            "next_hook": marker("ed.next_hook"),
        },
        "facts": facts,
    }


def main() -> int:
    ensure_dirs()
    data = build_slots()
    SLOTS.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {
        "episode_id": EP,
        "slug": "lech",
        "state": "asset_plan_ready",
        "title": "They Destroyed Their House",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "notes": "EP40 implementation stub scaffold generated by scripts/make_lech_slots_stub.py",
    }
    manifest_path = EPDIR / "manifest.json"
    if not manifest_path.exists():
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    pinned = EPDIR / "09_package" / "pinned_comment.v001.txt"
    if not pinned.exists():
        pinned.write_text(
            "Two things this case turns on, and neither is obvious:\n"
            "(1) The Tenth Circuit held this was an exercise of police power, not a taking -\n"
            "    so the Takings Clause never kicks in.\n"
            "(2) The Supreme Court declined to hear the appeal in 2020.\n"
            "    That is not agreement; it just means the ruling stands.\n\n"
            "If it were your house - should the city pay, or should you?\n",
            encoding="utf-8",
        )
    print(f"wrote {SLOTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
