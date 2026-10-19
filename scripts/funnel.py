# -*- coding: utf-8 -*-
"""Which topics actually receive suggested traffic, and from what?"""
import json, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = Path(r"C:\Users\aab15\Documents\prime-documentary")
d = json.loads((R / "runs/_cache/funnel_analytics.json").read_text(encoding="utf-8"))
titles = {t["id"]: t for t in json.loads((R / "runs/_cache/yt_titles.json").read_text(encoding="utf-8"))}
print("window:", d.get("window"))

rd = d.get("related_detail", {})
rows = rd.get("rows", [])
print(f"\nA. traffic-source detail rows (the videos that suggested PD): {len(rows)}")
tot = sum(r[1] for r in rows)
print(f"   total views arriving this way: {tot}")
own = [r for r in rows if r[0] in titles]
ext = [r for r in rows if r[0] not in titles]
print(f"   from PD's OWN videos: {len(own)} sources, {sum(r[1] for r in own)} views")
print(f"   from OTHER channels : {len(ext)} sources, {sum(r[1] for r in ext)} views")
print("\n   top sources:")
for vid, v, m in sorted(rows, key=lambda r: -r[1])[:15]:
    who = "PD: " + titles[vid]["t"][:56] if vid in titles else "EXTERNAL " + vid
    print(f"     {v:5d} views  {m:6d} min   {who}")

pv = d.get("per_video")
print(f"\nB. per_video keys: {type(pv)}")
if isinstance(pv, dict):
    ks = list(pv)[:3]
    print("   sample:", json.dumps({k: pv[k] for k in ks}, ensure_ascii=False)[:900])
elif isinstance(pv, list):
    print("   n =", len(pv), json.dumps(pv[:2], ensure_ascii=False)[:900])

pl = d.get("playlists")
print(f"\nC. playlists: {json.dumps(pl, ensure_ascii=False)[:400] if pl else 'none'}")
