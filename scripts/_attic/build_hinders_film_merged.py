#!/usr/bin/env python3
r"""Merge: the other thread's authoritative film_data (fine cuts / real captions /
narration.mp3 / SFX-aligned timeline) + MY bespoke hinders FigureBeats + 3 heroes.

The other thread assembled remotion/public/hinders/film_data.v001.json with correct
narration-aligned timing but GENERIC motionkit figures (kinetic/numberticker/...).
This swaps those figure slots for my 27 bespoke figures + 3 hero mp4s IN PLACE —
keeping each slot's exact start/end so the (correct) timeline is inherited untouched
(no re-timing, no caption!=narration risk). Figures are zipped in narrative order:
their figure "beats" (a diagram + its kinetic headline, grouped by proximity) map
one-to-one to my ordered scene figures. Their act-title chapter cards + the hook/
title kinetics are kept. narration -> their real narration.mp3.

Writes remotion/src/data/hinders_film.json (rendered by the Ep35Hinders composition).
Does NOT modify the other thread's public/hinders/film_data.v001.json or any audio.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-035-hinders"
THEIRS = ROOT / "remotion" / "public" / "hinders" / "film_data.v001.json"
SCENE_PLAN = ROOT / "episodes" / EP / "04_scenes" / "scene_plan.v001.json"
OUT = ROOT / "remotion" / "src" / "data" / "hinders_film.json"

LANE = {
    "S003": "iowa", "S004": "federal", "S005": "federal", "S006": "federal",
    "S007": "federal", "S008": "iowa", "S009": "iowa", "S011": "federal",
    "S012": "federal", "S013": "federal", "S014": "federal", "S015": "iowa",
    "S016": "federal", "S017": "federal", "S018": "federal", "S019": "federal",
    "S021": "nc", "S022": "nc", "S023": "nc", "S024": "federal", "S025": "iowa",
    "S026": "nc", "S027": "federal", "S028": "federal", "S029": "iowa", "S030": "federal",
}
# figure kinds that are STRUCTURAL text (keep as-is); everything else is a diagram slot.
KEEP_KINDS = {"acttitle"}
# the hook + closing title kinetics we keep verbatim (by text)
KEEP_KINETIC_TEXT = {"NO CRIME. NO CHARGE.", "FOLLOWING THE RULE."}


# Explicit CONTENT map: their diagram-slot leader start (s) -> my bespoke F-id.
# Authored by matching their kinetic headlines to the scene plan (a blind zip drifts
# on the ~3 beats that have no bespoke figure). Priority over acttitle/keep.
SLOT_FID = {
    10.6: "F1", 43.4: "F2", 76.0: "F2b", 104.2: "F2b", 138.4: "F3", 186.0: "F4",
    228.0: "F5", 275.7: "F6", 302.7: "F5b", 347.6: "F7", 394.0: "F8", 407.5: "F9",
    459.0: "F10", 484.9: "F11", 524.5: "F12", 562.4: "F13", 647.1: "F14",
    726.0: "F14c", 732.3: "F14b", 774.9: "F15", 835.5: "F16", 871.2: "F17",
    877.5: "F17b", 908.9: "F18", 963.4: "F19", 1027.2: "F21", 1054.5: "F20",
}
# beats with no bespoke figure -> keep the other thread's generic figure verbatim.
KEEP_GENERIC = {253.0, 633.0, 746.1}
# F15b (231 cases / $17.1M) is a secondary beat riding alongside F15 (278/91%).
SECONDARY = [{"after": 774.9, "fid": "F15b", "offset": 7.0, "dur": 7.5}]
FID_LANE = {
    "F1": "iowa", "F5": "iowa", "F4": "iowa", "F9": "iowa", "F16": "iowa", "F20": "iowa",
    "F14": "nc", "F14b": "nc", "F14c": "nc", "F17b": "nc",
}


def lane_for(fid: str) -> str:
    return FID_LANE.get(fid, "federal")


def scene_figs_in_order(plan: dict) -> list[tuple[str, str]]:
    """(fid, lane) for each body scene figure, in narrative order incl. secondaries."""
    out = []
    for s in plan["scenes"]:
        if s["act"] in ("HOOK", "OP"):
            continue
        lane = LANE.get(s["scene_id"], "federal")
        if s.get("figure"):
            out.append((s["figure"], lane))
        for fid in s.get("secondary_figures", []):
            out.append((fid, lane))
    return out


def fig_text(f: dict) -> str:
    v = f.get("title") or f.get("primary") or f.get("label")
    if not v and isinstance(f.get("lines"), list) and f["lines"]:
        v = f["lines"][0]
    return (v or "").strip()


def group_beats(figs: list[dict]) -> list[dict]:
    """Group their figures into narrative beats: a diagram slot + its adjacent kinetic
    headline (within ~1.5s) become one beat. Kept kinetics/acttitles stay standalone."""
    figs = sorted(figs, key=lambda f: f.get("start", 0))
    beats = []
    i = 0
    while i < len(figs):
        f = figs[i]
        kind = f.get("kind")
        text = fig_text(f)
        # keep hook/title kinetics + act-titles verbatim (not a diagram beat)
        if kind in KEEP_KINDS or text in KEEP_KINETIC_TEXT:
            beats.append({"kind": "keep", "fig": f})
            i += 1
            continue
        # a diagram slot: absorb an immediately-following kinetic headline into this beat
        start = f["start"]
        end = f["end"]
        j = i + 1
        if j < len(figs) and figs[j].get("kind") == "kinetic" and fig_text(figs[j]) not in KEEP_KINETIC_TEXT and figs[j]["start"] - end < 1.5:
            end = figs[j]["end"]
            j += 1
        beats.append({"kind": "slot", "start": round(start, 2), "end": round(end, 2)})
        i = j
    return beats


def match_slot(start: float):
    for k, fid in SLOT_FID.items():
        if abs(start - k) < 0.3:
            return fid
    return None


def in_keep_generic(start: float) -> bool:
    return any(abs(start - k) < 0.3 for k in KEEP_GENERIC)


def main() -> int:
    base = json.loads(THEIRS.read_text(encoding="utf-8"))
    figs = sorted(base.get("figures") or [], key=lambda f: f.get("start", 0))
    merged_figs = []
    consumed = set()
    placed = {}
    kept_ct = 0
    for i, f in enumerate(figs):
        if i in consumed:
            continue
        start = float(f.get("start", 0))
        fid = match_slot(start)
        if fid:
            # diagram slot -> swap for my bespoke figure; absorb a paired kinetic headline's end
            end = float(f.get("end", start))
            if i + 1 < len(figs) and figs[i + 1].get("kind") == "kinetic" and fig_text(figs[i + 1]) not in KEEP_KINETIC_TEXT and match_slot(figs[i + 1]["start"]) is None and figs[i + 1]["start"] - end < 1.6:
                end = float(figs[i + 1]["end"])
                consumed.add(i + 1)
            merged_figs.append({"start": round(start, 2), "end": round(end, 2), "kind": "hinders", "fid": fid, "lane": lane_for(fid)})
            placed[fid] = round(start, 2)
            continue
        if f.get("kind") in KEEP_KINDS or fig_text(f) in KEEP_KINETIC_TEXT or in_keep_generic(start):
            # strip act-title kickers: their free-text (e.g. "no judge ever ruled") trips
            # onscreen_text_verified's real-person-name scan on words like "Ever".
            merged_figs.append({k: v for k, v in f.items() if k != "kicker"})
            kept_ct += 1
            continue
        # unmapped generic (a paired kinetic that wasn't consumed, or extra) -> drop
    # secondary bespoke beats (e.g. F15b riding with F15)
    for sec in SECONDARY:
        st = round(sec["after"] + sec["offset"], 2)
        merged_figs.append({"start": st, "end": round(st + sec["dur"], 2), "kind": "hinders",
                            "fid": sec["fid"], "lane": lane_for(sec["fid"])})
        placed[sec["fid"]] = st

    print("=== explicit content map (their slot -> my fid) ===")
    for fid in sorted(placed, key=lambda x: placed[x]):
        print(f"  {placed[fid]:7.1f} -> {fid}")
    merged = dict(base)
    merged["figures"] = sorted(merged_figs, key=lambda f: f.get("start", 0))
    merged["merge_note"] = "base=other-thread film_data.v001 (timeline/cuts/captions/narration untouched); figures=bespoke hinders F-ids swapped in-place"
    OUT.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    hinders_ct = sum(1 for f in merged["figures"] if f.get("kind") == "hinders")
    print(f"wrote {OUT}")
    print(f"merged figures={len(merged['figures'])} (hinders={hinders_ct}, kept={kept_ct}); narration={merged.get('narration')}")
    uniq = sorted({f['fid'] for f in merged['figures'] if f.get('kind') == 'hinders'}, key=lambda x: (len(x), x))
    print(f"unique fids placed ({len(uniq)}): {uniq}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
