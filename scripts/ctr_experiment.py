# -*- coding: utf-8 -*-
"""The 2026-08-10 title rewrite is a controlled experiment. Read it."""
import json, sys, io, statistics, re
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = Path(r"C:\Users\aab15\Documents\prime-documentary")

def load(name):
    p = R / "scripts" / name
    if not p.exists(): return None
    d = json.loads(p.read_text(encoding="utf-8"))
    rows = d["rows"] if isinstance(d, dict) and "rows" in d else d
    out = {}
    for r in rows:
        out[r["video_id"]] = {
            "t": r.get("title", ""),
            "imp": r.get("VIDEO_THUMBNAIL_IMPRESSIONS") or 0,
            "ctr": r.get("VIDEO_THUMBNAIL_IMPRESSIONS_VTR") or 0.0,
            "sec": r.get("length_seconds") or 0,
        }
    return out

snaps = {}
for n in ("_yt_studio_video_ctr.20260810.json", "_yt_studio_video_ctr.20260811.json",
          "_yt_studio_video_ctr.20260819.json", "_yt_studio_video_ctr.json"):
    s = load(n)
    if s: snaps[n] = s
    print(f"{n:42s} {'-' if not s else str(len(s))+' rows'}")

a = snaps.get("_yt_studio_video_ctr.20260810.json")
c = snaps.get("_yt_studio_video_ctr.20260819.json")
if not (a and c):
    print("cannot compare"); raise SystemExit

# which videos were retitled?
applied = R / "episodes/_planning/measurements/TITLE_APPLY_39.applied.v001.json"
treated = set()
if applied.exists():
    j = json.loads(applied.read_text(encoding="utf-8"))
    items = j if isinstance(j, list) else (j.get("items") or j.get("rows") or [])
    for it in items:
        if isinstance(it, dict):
            vid = it.get("video_id") or it.get("id")
            if vid: treated.add(vid)
print(f"\nretitled (from the applied record): {len(treated)}")

# fall back: detect by title change between the two snapshots
changed = {v for v in a if v in c and a[v]["t"].strip() != c[v]["t"].strip()}
print(f"titles that differ between 08-10 and 08-19 snapshots: {len(changed)}")
if not treated:
    treated = changed

both = [v for v in a if v in c and a[v]["sec"] >= 600]
tr = [v for v in both if v in treated]
ct = [v for v in both if v not in treated]
print(f"\nlong-form present in both snapshots: {len(both)}   treated {len(tr)}   control {len(ct)}")

def wctr(vs, snap):
    i = sum(snap[v]["imp"] for v in vs)
    return sum(snap[v]["imp"] * snap[v]["ctr"] for v in vs) / i / 1 if i else 0

def block(name, vs):
    if not vs: print(f"  {name}: none"); return
    b = wctr(vs, a); e = wctr(vs, c)
    mb = statistics.median([a[v]["ctr"] for v in vs]); me = statistics.median([c[v]["ctr"] for v in vs])
    ib = sum(a[v]["imp"] for v in vs); ie = sum(c[v]["imp"] for v in vs)
    print(f"  {name:9s} n={len(vs):3d}  weighted CTR {b:5.2f}% -> {e:5.2f}%  ({e-b:+.2f})   "
          f"median {mb:5.2f}% -> {me:5.2f}%  ({me-mb:+.2f})   impressions {ib:,} -> {ie:,}")

print("\n=== the experiment ===")
block("TREATED", tr)
block("CONTROL", ct)

print("\n=== per-video, treated, sorted by CTR change ===")
rows = []
for v in tr:
    rows.append((c[v]["ctr"] - a[v]["ctr"], a[v]["ctr"], c[v]["ctr"], a[v]["imp"], c[v]["imp"],
                 a[v]["t"], c[v]["t"]))
for d, b, e, ib, ie, ot, nt in sorted(rows, key=lambda x: -x[0]):
    print(f"{d:+6.2f}  {b:5.2f} -> {e:5.2f}   imp {ib:>6,} -> {ie:>6,}")
    print(f"        OLD  {ot[:96]}")
    print(f"        NEW  {nt[:96]}")
