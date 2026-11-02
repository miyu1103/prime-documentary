# -*- coding: utf-8 -*-
"""Does a famous subject earn PD impressions, or does the incumbent film eat them?

PD_CANON's topic rule says reject a subject with a definitive film at 3M+.
`pd-feeder-rail` says the only measured growth mechanism is being linked by external videos
after publication. Those point opposite ways. This decides it on PD's own catalogue.
"""
import json, re, sys, io, statistics
from datetime import datetime, timezone
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = Path(r"C:\Users\aab15\Documents\prime-documentary")

rows = json.loads((R / "scripts/_yt_studio_video_ctr.20260819.json").read_text(encoding="utf-8"))["rows"]
titles = json.loads((R / "runs/_cache/yt_titles.json").read_text(encoding="utf-8"))
pub = {t["id"]: t["at"] for t in titles}
NOW = datetime(2026, 8, 19, tzinfo=timezone.utc)

# A subject an ordinary American could name before the video existed.
FAMOUS = re.compile(
    r"OceanGate|Fifty Years On the FBI|Madoff|\$8 Billion Had Already Left|"
    r"\$4 Billion for a Cryptocurrency|The Machine Never Worked|Boston Museum|"
    r"Side Door Into America|One Banker Was Paid|Billionaire Heard His Own Voice|"
    r"\$1 Trillion Vanished|Five Children Confessed|A Computer Invents a .2,000 Debt|"
    r"Texas Executed Him|13 Felonies", re.I)

lf = []
for r in rows:
    if (r.get("length_seconds") or 0) < 600:
        continue
    v = r["video_id"]; at = pub.get(v)
    age = None
    if at:
        try: age = (NOW - datetime.fromisoformat(at.replace("Z", "+00:00"))).days
        except Exception: pass
    lf.append(dict(t=r.get("title", ""), imp=r.get("VIDEO_THUMBNAIL_IMPRESSIONS") or 0,
                   ctr=r.get("VIDEO_THUMBNAIL_IMPRESSIONS_VTR") or 0.0, age=age,
                   sec=r.get("length_seconds") or 0))

def show(label, sel, pool):
    v = [r for r in pool if sel(r)]
    if not v: print(f"  {label:34s} none"); return
    imp = [r["imp"] for r in v]; ti = sum(imp)
    w = sum(r["imp"]*r["ctr"] for r in v)/ti if ti else 0
    clicks = sum(r["imp"]*r["ctr"]/100 for r in v)
    print(f"  {label:34s} n={len(v):3d}  median imp {statistics.median(imp):7,.0f}  "
          f"mean imp {statistics.mean(imp):8,.0f}  wCTR {w:5.2f}%  clicks {clicks:6.0f}")

print(f"long-form n={len(lf)}\n")
print("A. famous subject vs unknown case  (ALL long-form)")
show("FAMOUS subject", lambda r: FAMOUS.search(r["t"]), lf)
show("unknown case", lambda r: not FAMOUS.search(r["t"]), lf)

aged = [r for r in lf if r["age"] and 20 <= r["age"] <= 70]
print(f"\nB. same, restricted to 20-70 days old (removes the age artifact), n={len(aged)}")
show("FAMOUS subject", lambda r: FAMOUS.search(r["t"]), aged)
show("unknown case", lambda r: not FAMOUS.search(r["t"]), aged)

print("\nC. every famous-subject episode, so the claim can be checked by eye")
for r in sorted([r for r in lf if FAMOUS.search(r["t"])], key=lambda x: -x["imp"]):
    print(f"   imp {r['imp']:6,d}  ctr {r['ctr']:5.2f}%  clicks {r['imp']*r['ctr']/100:5.0f}  "
          f"age {r['age'] if r['age'] else '?':>3}d  {r['t'][:62]}")

print("\nD. the ten biggest by impressions, whatever they are")
for r in sorted(lf, key=lambda x: -x["imp"])[:10]:
    fam = "FAMOUS" if FAMOUS.search(r["t"]) else "      "
    print(f"   {fam}  imp {r['imp']:6,d}  ctr {r['ctr']:5.2f}%  age {r['age'] if r['age'] else '?':>3}d  {r['t'][:58]}")
