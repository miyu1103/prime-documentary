#!/usr/bin/env python3
r"""Register EP76 morandi's rejected i2v clips in config/footage_blocklist.v001.json.

WHY A SCRIPT AND NOT A HAND EDIT. The main assembly thread was reverted twice for moving files
out of `remotion/public/morandi/motion` by hand: step [1/7] of the chain rebuilds a clip from its
frame sequence and step [2/7] re-copies from the archive, so a deleted file comes back. The
blocklist is the only durable place a rejection survives a rebuild, and `pd_footage_blocklist.py`
is the only reader (`blocked` binds, `quality_deferred` does not).

WHAT WAS MEASURED. `qc_motion_clips.py --slug morandi --samples 6 --per-sheet 6` wrote 20 contact
sheets to runs/qc/motion_frames/morandi. All 20 were read. 52 of 120 clips grow people, hands or
objects that are NOT in their plate. Two ambiguous clips (V098, V120) were re-checked at full
resolution rather than judged from a 400px tile -- V098 came back clean (its four seated figures
are in frame 1), V120 came back rejected (a car drives onto the severed carriageway by frame 80).

WHY THESE ARE HARD FOR THIS EPISODE AND NOT A TASTE CALL. EP76's binding constraint is that the
film may never assert the collapse was foreseen (⛔-02; `episode_spec.forbidden_claims`). A person
who appears from nowhere to touch corroded steel, shine a light into a box girder or fill in an
inspection form is a visual assertion that someone was looking at it -- a claim the record does
not support. That is `factual_support` under config/ship_policy.v001.json, one of the four classes
that may still close the door. Hence `cat4_wrong_subject_reads_as_the_claim`.

EVERY ROW IS EPISODE-SCOPED. The ids are V001-style plate numbers, which name a completely
different picture in every other episode. A global row here would silently delete unrelated
images from unrelated films -- the exact hazard `pd_footage_blocklist.py` documents.

Usage:
    py -3.11 scripts/block_morandi_motion_rejects.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKLIST = ROOT / "config" / "footage_blocklist.v001.json"

# --- the four rows, each with the per-clip finding that produced it ------------------------

# A person, a hand or an arm that is not in the plate arrives and handles the structure or the
# paperwork. Reads as "somebody was inspecting this", which is the claim EP76 must never make.
INSPECTION: dict[str, str] = {
    "V003": "a woman reaches toward the exposed rusted rebar",
    "V004": "a hand, then a whole person, enters at the broken high-tensile wires",
    "V007": "a figure walks along the deck under the four ties",
    "V008": "hands reach into the sectioned stay",
    "V012": "a person in a red top works at the 1962 drawing board",
    "V018": "an arm, then a young woman's face, enters at the bearing",
    "V023": "a head and torso appear beneath the pier crossbeam",
    "V027": "a figure climbs the pylon",
    "V031": "a bare arm reaches in and grasps the new strand",
    "V032": "two hands come in and touch the corroded strand",
    "V033": "a hand reaches down and picks at the spalled deck edge",
    "V034": "a man with a backpack walks in and looks into the box-girder cell",
    "V035": "a person reaches for the folder on the 1960s desk",
    "V036": "a figure stands beneath the deck access hatch",
    "V038": "legs, then a torso holding a tool, appear at the drainage pipe",
    "V041": "a person in a blue shirt walks in and stands over the concrete cores",
    "V043": "a bare hand reaches into the exposed strands",
    "V044": "a hand reaches repeatedly into the broken concrete",
    "V047": "a bare arm reaches into the bearing detail",
    "V055": "an orange-sleeved hand reaches into the open ring binder",
    "V057": "a hand holding a pen writes on the form",
    "V058": "a woman appears holding the clipboard at the parapet -- the literal inspection image",
    "V069": "a man with a backpack walks through the base of the pier",
    "V070": "a hand turns the blank page AND glyph-like marks resolve on the turned face",
    "V072": "a dark hand holding a tool appears at the duct",
    "V073": "a hand with red nail polish appears on the blank graph paper",
    "V075": "a hand enters at the open ledger",
    "V081": "a person in beige reaches into the filing drawer",
    "V082": "a hand appears at the file tabs",
    "V083": "a woman with dark hair pulls a box off the archive shelf",
    "V084": "a hand wearing a watch appears at the desk paper",
    "V085": "an arm and hand reach into the fax machine",
    "V086": "a hand appears on the ruled form",
    "V087": "a person in white walks past the rolled drawings",
    "V088": "a hand, then a torso, appears at the drawing table",
    "V089": "a large arm and hand press down on the ledger",
    "V090": "a hand enters at the ring binder",
    "V091": "hands in white sleeves arrive at the stack of paper",
    "V092": "a person in a white shirt resolves out of a blur in the drawing office",
    "V093": "a hand appears at the right edge of the blank page",
    "V097": "people arrive one by one in what the plate holds as an empty hearing room",
    "V101": "a hand and arm reach for the rubber stamp",
    "V102": "a leg, then a hand, appears at the document tray",
    "V110": "arms and hands arrive at the two bound volumes",
    "V114": "a standing woman walks into the hall of chairs",
    "V115": "a man's head and shoulders appear at the noticeboard",
    "V116": "a hand, then a seated person reading, appears at the open binder",
}

# A face that is not in the plate resolves to photoreal detail. Nothing binds this face to a real
# person, and nothing rules it out either; ship_policy calls this class real_person_likeness and
# it is one of the four that close the door.
LIKENESS: dict[str, str] = {
    "V010": "a lit female face resolves out of what the plate holds as an empty black ground",
    "V064": "a man appears at the steelwork and looks into the lens",
}

# Not a rights or safety finding: the clip is simply broken and cannot be cut.
BROKEN: dict[str, str] = {
    "V026": "frame 1 is white and every later frame is black",
    "V056": "the ruled form fades to near-black by frame 3 and never returns",
}

# ⛔ bars depicting the fall, the vehicles and the dead. This one puts a car on the broken road.
FORBIDDEN: dict[str, str] = {
    "V120": "a car drives onto the severed carriageway by frame 80; confirmed at full resolution",
}

SHEET_NOTE = ("read on runs/qc/motion_frames/morandi/morandi_motion_01..20.png, "
              "6 frames per clip; V098 and V120 re-checked at full resolution")


def row(ids: dict[str, str], label: str, headline: str, cat: str) -> dict:
    findings = "; ".join(f"{k} {v}" for k, v in sorted(ids.items()))
    return {
        "ids": sorted(ids),
        "label": label,
        "reason": f"{headline} Per-clip findings ({SHEET_NOTE}): {findings}.",
        "hard_category": cat,
        "episodes": ["morandi"],
    }


ROWS = [
    row(INSPECTION, "wan_hallucinated_inspector",
        "Wan drew a person, a hand or an arm that is not in the plate, handling the structure or "
        "the paperwork. EP76 may never assert the collapse was foreseen (⛔-02, "
        "episode_spec.forbidden_claims); a figure who arrives to touch corroded steel or fill in "
        "a form asserts that somebody was looking at it.",
        "cat4_wrong_subject_reads_as_the_claim"),
    row(LIKENESS, "wan_hallucinated_face",
        "A face that is not in the plate resolves to photoreal detail.",
        "cat2_real_person_likeness"),
    row(BROKEN, "i2v_clip_broken",
        "The clip is unusable on its own terms -- it goes black. No rights or safety finding.",
        "none_kept_for_a_mechanical_reason"),
    row(FORBIDDEN, "forbidden_subject_vehicle_on_severed_road",
        "EP76 forbids depicting the fall, the vehicles and the dead.",
        "cat4_wrong_subject_reads_as_the_claim"),
]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    doc = json.loads(BLOCKLIST.read_text(encoding="utf-8"))
    before = len(doc["blocked"])
    labels = {r["label"] for r in ROWS}
    # Re-runnable: replace this script's own rows rather than appending a second copy.
    doc["blocked"] = [r for r in doc["blocked"]
                      if not (r.get("label") in labels and r.get("episodes") == ["morandi"])]
    removed = before - len(doc["blocked"])
    doc["blocked"].extend(ROWS)

    total = sum(len(r["ids"]) for r in ROWS)
    for r in ROWS:
        print(f"{r['label']:<44} {len(r['ids']):>3} clips  [{r['hard_category']}]")
    print(f"total {total} of 120 clips blocked for morandi "
          f"({100*total/120:.0f}%); replaced {removed} existing row(s)")

    if a.dry_run:
        print("--dry-run: nothing written")
        return 0
    BLOCKLIST.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {BLOCKLIST}")

    # Prove it through the real reader, not through the file we just wrote.
    sys.path.insert(0, str(ROOT / "scripts"))
    import pd_footage_blocklist as fb  # noqa: PLC0415

    mine = fb.load_blocked("morandi")
    other = fb.load_blocked("oroville")
    glob = fb.load_blocked(None)
    seen = fb.reason_for("V003.mp4", mine)
    print(f"reader: morandi sees {len(mine)} ids, oroville {len(other)}, global {len(glob)}")
    print(f"reader: V003.mp4 -> {seen[:90] if seen else 'NOT BLOCKED -- BUG'}")
    leaked = [i for i in INSPECTION if i in other]
    print(f"reader: morandi ids leaking into another episode: {leaked or 'none'}")
    return 0 if seen and not leaked else 1


if __name__ == "__main__":
    raise SystemExit(main())
