# -*- coding: utf-8 -*-
"""Retention and subscriber conversion by topic, from the funnel snapshot."""
import json, re, sys, io, statistics
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = Path(r"C:\Users\aab15\Documents\prime-documentary")
d = json.loads((R / "runs/_cache/funnel_analytics.json").read_text(encoding="utf-8"))
T = {t["id"]: t for t in json.loads((R / "runs/_cache/yt_titles.json").read_text(encoding="utf-8"))}
perf = json.loads((R / "runs/_cache/content_genome_perf.v001.json").read_text(encoding="utf-8"))["per_video"]

rows = d["per_video"]["rows"]
print(f"window {d['window']}   videos with data: {len(rows)}")

lf, sh = [], []
for vid, views, avp, subs in rows:
    t = T.get(vid)
    if not t:
        continue
    rec = dict(id=vid, t=t["t"], sec=t["d"], views=views, avp=avp, subs=subs)
    (lf if t["d"] >= 600 else sh).append(rec)
print(f"  long-form {len(lf)}   shorts {len(sh)}\n")

print("A. long-form retention and conversion, by views")
print(f"{'views':>6} {'AVP%':>6} {'subs':>5} {'min':>4}  title")
for r in sorted(lf, key=lambda x: -x["views"]):
    print(f"{r['views']:>6} {r['avp']:>6.1f} {r['subs']:>5} {int(r['sec']/60):>4}  {r['t'][:66]}")

if lf:
    print(f"\n  median AVP {statistics.median([r['avp'] for r in lf]):.1f}%   "
          f"total subs from long-form {sum(r['subs'] for r in lf)}   "
          f"total views {sum(r['views'] for r in lf)}")
    print(f"  subscribers per 1,000 views (long-form): "
          f"{sum(r['subs'] for r in lf)/max(1,sum(r['views'] for r in lf))*1000:.2f}")
if sh:
    print(f"  shorts: median AVP {statistics.median([r['avp'] for r in sh]):.1f}%  "
          f"subs {sum(r['subs'] for r in sh)}  views {sum(r['views'] for r in sh)}  "
          f"per 1,000 = {sum(r['subs'] for r in sh)/max(1,sum(r['views'] for r in sh))*1000:.2f}")

print("\nB. does length hurt retention? (long-form only)")
for lo, hi, lbl in ((600, 900, "10-15 min"), (900, 1500, "15-25 min"), (1500, 2600, "25-43 min")):
    v = [r for r in lf if lo <= r["sec"] < hi]
    if v:
        print(f"   {lbl:10s} n={len(v):2d}  median AVP {statistics.median([x['avp'] for x in v]):5.1f}%  "
              f"median minutes watched {statistics.median([x['avp']*x['sec']/6000 for x in v]):5.1f}")

print("\nC. lifetime view leaders (content_genome, 2026-08-11) with AVP and subs")
rows2 = sorted(perf.values(), key=lambda x: -x["views"])[:15]
for r in rows2:
    t = T.get(r["video"])
    if not t or t["d"] < 600:
        continue
    print(f"   views {r['views']:>4}  AVP {r['averageViewPercentage']:>5.1f}%  "
          f"subs +{r['subscribersGained']}  {int(t['d']/60):>3}m  {t['t'][:58]}")
