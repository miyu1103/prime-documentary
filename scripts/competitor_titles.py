# -*- coding: utf-8 -*-
"""PD has 38 usable rows. The demand probes captured ~900 competitor videos with view counts.
Learn the title model from the big sample, not the small one."""
import json, glob, re, sys, io, statistics, math
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = r"C:\Users\aab15\Documents\prime-documentary\episodes\_planning\measurements"

rows, seen = [], set()
for f in sorted(glob.glob(D + r"\TOPIC_DEMAND_PROBE*.json")):
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    t = d.get("topics") if isinstance(d, dict) else None
    if not isinstance(t, dict): continue
    for q, v in t.items():
        for r in (v.get("rows") or []):
            key = (r.get("t", ""), r.get("views"))
            if key in seen: continue
            seen.add(key)
            r["q"] = q
            rows.append(r)
print(f"competitor videos captured: {len(rows)}")

# only long-form; shorts and news clips are a different market
lf = [r for r in rows if (r.get("sec") or 0) >= 600 and (r.get("views") or 0) > 0]
print(f"of which >=10 minutes: {len(lf)}")
med_all = statistics.median([r["views"] for r in lf])
print(f"median views: {med_all:,.0f}   mean: {statistics.mean([r['views'] for r in lf]):,.0f}")

def norm(t): return re.sub(r"\s+", " ", t or "").strip()

FEATURES = {
    "two_sentences":  lambda t: len([s for s in re.split(r"(?<=[.!?:])\s+", t) if s.strip()]) >= 2,
    "starts_authority": lambda t: bool(re.match(
        r"^(the\s+)?(police|officers?|detectives?|agents?|a\s+(judge|sheriff|deputy|detective|federal)|"
        r"the\s+(state|court|judge|company|government|navy|army|fbi|faa|ntsb|city|county))", t, re.I)),
    "has_number":     lambda t: bool(re.search(r"\d", t)),
    "has_money":      lambda t: "$" in t or bool(re.search(r"\b(million|billion)\b", t, re.I)),
    "has_year":       lambda t: bool(re.search(r"\b(19|20)\d{2}\b", t)),
    "question":       lambda t: t.rstrip().endswith("?"),
    "colon":          lambda t: ":" in t,
    "pipe_brand":     lambda t: "|" in t,
    "the_x_that":     lambda t: bool(re.search(r"\bthat\b", t, re.I)),
    "why_how":        lambda t: bool(re.match(r"^(why|how|what)\b", t, re.I)),
    "disaster_word":  lambda t: bool(re.search(r"\b(disaster|tragedy|horror|deadliest|worst)\b", t, re.I)),
    "died_killed":    lambda t: bool(re.search(r"\b(died|killed|deaths?|dead|fatal)\b", t, re.I)),
    "object_named":   lambda t: bool(re.search(
        r"\b(bridge|ferry|ship|boat|plane|aircraft|train|car|truck|bus|rig|platform|tunnel|dam|"
        r"tower|hotel|nightclub|factory|mine|refinery|pipeline|reactor|submarine|door|window|"
        r"phone|gun|tyre|tire|airbag|valve|pump)\b", t, re.I)),
    "place_named":    lambda t: bool(re.search(
        r"\b(alaska|texas|nevada|ohio|florida|chicago|boston|london|paris|tokyo|india|japan|"
        r"korea|italy|scotland|vegas|maui|hawaii|genoa|bhopal|zeebrugge|piper|valdez)\b", t, re.I)),
    "len_over_60":    lambda t: len(t) > 60,
    "len_over_80":    lambda t: len(t) > 80,
    "all_caps_word":  lambda t: bool(re.search(r"\b[A-Z]{3,}\b", t)),
}

print("\n=== title feature vs median views (competitor long-form, n per row) ===")
print(f"{'feature':18s} {'with n':>7s} {'median':>10s} {'without n':>9s} {'median':>10s} {'lift':>7s}")
res = []
for name, fn in FEATURES.items():
    yes = [r["views"] for r in lf if fn(norm(r.get("t")))]
    no = [r["views"] for r in lf if not fn(norm(r.get("t")))]
    if len(yes) < 15 or len(no) < 15: continue
    my, mn = statistics.median(yes), statistics.median(no)
    res.append((my / mn if mn else 0, name, len(yes), my, len(no), mn))
for lift, name, ny, my, nn, mn in sorted(res, reverse=True):
    print(f"{name:18s} {ny:7d} {my:10,.0f} {nn:9d} {mn:10,.0f} {lift:7.2f}x")

print("\n=== the 25 biggest competitor long-form videos, to read the shape directly ===")
for r in sorted(lf, key=lambda x: -x["views"])[:25]:
    print(f"{r['views']:>10,}  {int(r['sec']/60):3d}m  {r['ch'][:22]:22s}  {norm(r['t'])[:78]}")

print("\n=== and the shape of videos between 100k and 400k (PD's realistic ceiling) ===")
band = [r for r in lf if 100_000 <= r["views"] <= 400_000]
print(f"n={len(band)}")
for r in sorted(band, key=lambda x: -x["views"])[:20]:
    print(f"{r['views']:>10,}  {int(r['sec']/60):3d}m  {r['ch'][:22]:22s}  {norm(r['t'])[:78]}")
