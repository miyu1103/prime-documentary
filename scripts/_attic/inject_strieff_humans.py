#!/usr/bin/env python3
"""EP49 strieff: inject the 5 anonymized human MOTION clips (G1-G5) at their mapped
narration beats (BODY-relative time), replacing the weakest/most-reused overlapping shot.
Region-rebuild keeps every region contiguous and the global timeline byte-identical in length.
Writes back to remotion/src/data/strieff_film.json. Idempotent-ish: aborts if humans already present.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

FILM = Path(r"C:\Users\aab15\Documents\prime-documentary\remotion\src\data\strieff_film.json")

def footage_cut(cid, start, dur, src, seed, act):
    return {"id": cid, "start": round(start, 3), "dur": round(dur, 3), "kind": "footage",
            "src": src, "seed": seed, "act": act, "treatment": "footage", "startFrom": 0}

def main():
    d = json.loads(FILM.read_text("utf-8"))
    cuts = d["cuts"]
    if any("human/" in c["src"] for c in cuts):
        print("Humans already injected; abort."); return 1
    byid = {c["id"]: i for i, c in enumerate(cuts)}

    # exact clip durations (frames/30)
    G1 = 122/30; G2 = 122/30; G3 = 82/30; G4 = 82/30; G5 = 122/30
    HUM = "strieff/human/"

    # --- G1: fill cut-001 slot (img S01, a reused still) with G1 door footage ---
    i = byid["cut-001"]
    c = cuts[i]
    cuts[i] = footage_cut("cut-001", c["start"], c["dur"], HUM+"G1.mp4", "strieff-h-G1", c["act"])

    # --- G3+G4: arrest window. A pindropmap figure (body 45.37-50.77) is an OPAQUE full-frame
    #     map ("South Salt Lake City, Utah") that hides anything beneath it, so G3 (handcuffs) and
    #     G4 (bag) MUST sit AFTER the map clears (50.773) to be visible. Region [cut-009,010,011]
    #     44.84-59.26 rebuilt: st_drugs_evidence stays under the map; G3+G4 land in the visible
    #     window right after; st_phone_records kept (trimmed); S04 img dropped (also trims its 2x).
    MAP_END = 50.773
    a = byid["cut-009"]; c = byid["cut-011"]
    assert c == a+2, (a, c)
    reg_start = cuts[a]["start"]; reg_end = cuts[c]["start"] + cuts[c]["dur"]
    drugs = cuts[a]; phone = cuts[c]
    new = [
        {**drugs, "start": round(reg_start, 3), "dur": round(MAP_END-reg_start, 3)},
        footage_cut("cut-009b", MAP_END, G3, HUM+"G3.mp4", "strieff-h-G3", cuts[a]["act"]),
        footage_cut("cut-009c", MAP_END+G3, G4, HUM+"G4.mp4", "strieff-h-G4", cuts[a]["act"]),
        {**phone, "start": round(MAP_END+G3+G4, 3), "dur": round(reg_end-(MAP_END+G3+G4), 3)},
    ]
    cuts[a:c+1] = new

    # rebuild index after insertion
    byid = {c["id"]: i for i, c in enumerate(cuts)}

    # --- G5: region [cut-038, cut-039] drop st_feet_walking (reused), keep factory F017 shifted ---
    a = byid["cut-038"]; b = byid["cut-039"]
    assert b == a+1
    reg_start = cuts[a]["start"]; reg_end = cuts[b]["start"] + cuts[b]["dur"]
    f017 = cuts[b]
    new = [
        footage_cut("cut-038", reg_start, G5, HUM+"G5.mp4", "strieff-h-G5", cuts[a]["act"]),
        {**f017, "start": round(reg_start+G5, 3), "dur": round(reg_end-(reg_start+G5), 3)},
    ]
    cuts[a:b+1] = new
    byid = {c["id"]: i for i, c in enumerate(cuts)}

    # --- G2: region [cut-043, cut-044] drop st_police_night, keep factory F019 shifted ---
    a = byid["cut-043"]; b = byid["cut-044"]
    assert b == a+1
    reg_start = cuts[a]["start"]; reg_end = cuts[b]["start"] + cuts[b]["dur"]
    f019 = cuts[b]
    new = [
        footage_cut("cut-043", reg_start, G2, HUM+"G2.mp4", "strieff-h-G2", cuts[a]["act"]),
        {**f019, "start": round(reg_start+G2, 3), "dur": round(reg_end-(reg_start+G2), 3)},
    ]
    cuts[a:b+1] = new

    # ---- VALIDATE contiguity + total length ----
    prev_end = 0.0
    errs = []
    for idx, c in enumerate(cuts):
        if abs(c["start"] - prev_end) > 0.01:
            errs.append(f"gap/overlap at {c['id']} idx{idx}: start {c['start']} vs prev_end {prev_end:.3f}")
        prev_end = c["start"] + c["dur"]
    total = prev_end
    if abs(total - d["narrationSeconds"]) > 0.05:
        errs.append(f"total {total:.3f} != narrationSeconds {d['narrationSeconds']}")
    if errs:
        print("VALIDATION FAILED:"); [print("  ", e) for e in errs]; return 2

    from collections import Counter
    cc = Counter(c["src"] for c in cuts)
    print(f"cuts={len(cuts)} distinct={len(cc)} avg_reuse={len(cuts)/len(cc):.3f} total_end={total:.3f}")
    print("human cuts placed:")
    for c in cuts:
        if "human/" in c["src"]:
            print(f"  {c['id']} {c['start']:.3f}-{c['start']+c['dur']:.3f} {c['src']}")
    FILM.write_text(json.dumps(d, ensure_ascii=False, indent=2), "utf-8")
    print("WROTE", FILM)
    return 0

sys.exit(main())
