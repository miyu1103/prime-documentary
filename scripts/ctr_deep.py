# -*- coding: utf-8 -*-
"""Is PD's problem CTR, or is it that nobody is being shown anything?"""
import json, sys, io, statistics, math
from datetime import datetime, timezone
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = Path(r"C:\Users\aab15\Documents\prime-documentary")

cur = json.loads((R / "scripts/_yt_studio_video_ctr.20260819.json").read_text(encoding="utf-8"))["rows"]
old = json.loads((R / "scripts/_yt_studio_video_ctr.20260810.json").read_text(encoding="utf-8"))["rows"]
titles = json.loads((R / "runs/_cache/yt_titles.json").read_text(encoding="utf-8"))
pub = {t["id"]: t["at"] for t in titles}

O = {r["video_id"]: r for r in old}
NOW = datetime(2026, 8, 19, tzinfo=timezone.utc)

rows = []
for r in cur:
    v = r["video_id"]
    imp = r.get("VIDEO_THUMBNAIL_IMPRESSIONS") or 0
    ctr = r.get("VIDEO_THUMBNAIL_IMPRESSIONS_VTR") or 0.0
    sec = r.get("length_seconds") or 0
    if sec < 600:
        continue
    at = pub.get(v)
    age = None
    if at:
        try:
            age = (NOW - datetime.fromisoformat(at.replace("Z", "+00:00"))).days
        except Exception:
            pass
    d_imp = imp - (O[v].get("VIDEO_THUMBNAIL_IMPRESSIONS") or 0) if v in O else None
    rows.append(dict(v=v, t=r.get("title", ""), imp=imp, ctr=ctr, sec=sec, age=age, d_imp=d_imp))

print(f"long-form rows: {len(rows)}")

# --- 1. how many impressions does a video actually receive per day? ---
withage = [r for r in rows if r["age"] and r["age"] > 0]
per_day = sorted(r["imp"] / min(r["age"], 28) for r in withage)
print(f"\n1. impressions per video per day (28d window, n={len(withage)})")
print(f"   median {statistics.median(per_day):.1f}   mean {statistics.mean(per_day):.1f}   "
      f"max {max(per_day):.1f}   min {min(per_day):.1f}")
print(f"   videos under 20/day: {sum(1 for x in per_day if x < 20)} of {len(per_day)}")

# --- 2. is CTR higher or lower when impressions are higher? ---
def pearson(xs, ys):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x-mx)**2 for x in xs)); dy = math.sqrt(sum((y-my)**2 for y in ys))
    return num/(dx*dy) if dx and dy else 0

big = [r for r in rows if r["imp"] >= 300]
xs = [math.log10(r["imp"]) for r in big]; ys = [r["ctr"] for r in big]
print(f"\n2. correlation between log(impressions) and CTR, n={len(big)}: r = {pearson(xs, ys):+.2f}")
buckets = {"300-800": [], "800-2000": [], "2000+": []}
for r in big:
    k = "300-800" if r["imp"] < 800 else ("800-2000" if r["imp"] < 2000 else "2000+")
    buckets[k].append(r["ctr"])
for k, vs in buckets.items():
    print(f"   {k:9s} n={len(vs):2d}  median CTR {statistics.median(vs):.2f}%  mean {statistics.mean(vs):.2f}%")

# --- 3. does age explain CTR? ---
wa = [r for r in big if r["age"]]
print(f"\n3. correlation between age(days) and CTR, n={len(wa)}: "
      f"r = {pearson([r['age'] for r in wa], [r['ctr'] for r in wa]):+.2f}")
for lo, hi in ((0, 20), (20, 40), (40, 70)):
    vs = [r["ctr"] for r in wa if lo <= r["age"] < hi]
    if vs:
        print(f"   published {lo:2d}-{hi:2d} days ago  n={len(vs):2d}  median CTR {statistics.median(vs):.2f}%")

# --- 4. duration vs CTR ---
print("\n4. duration vs CTR (>=300 impressions)")
for lo, hi, lbl in ((600, 900, "10-15 min"), (900, 1500, "15-25 min"),
                    (1500, 2200, "25-36 min"), (2200, 9999, "36 min+")):
    vs = [r["ctr"] for r in big if lo <= r["sec"] < hi]
    ims = [r["imp"] for r in big if lo <= r["sec"] < hi]
    if vs:
        print(f"   {lbl:10s} n={len(vs):2d}  median CTR {statistics.median(vs):.2f}%  "
              f"median impressions {statistics.median(ims):,.0f}")

# --- 5. where the clicks actually are ---
print("\n5. clicks, not CTR (impressions x CTR)")
for r in sorted(rows, key=lambda x: -(x["imp"]*x["ctr"]))[:12]:
    print(f"   {r['imp']*r['ctr']/100:6.0f} clicks   ctr {r['ctr']:5.2f}%  imp {r['imp']:6,d}  "
          f"{int(r['sec']/60):3d}m  {r['t'][:56]}")
tot_clicks = sum(r["imp"]*r["ctr"]/100 for r in rows)
print(f"   long-form total clicks in 28 days: {tot_clicks:,.0f}")
