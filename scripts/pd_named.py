# -*- coding: utf-8 -*-
"""Does a searchable proper name in PD's own title earn impressions?
Impressions, not CTR, is the binding constraint: median 23.7 per video per day."""
import json, re, sys, io, statistics
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = Path(r"C:\Users\aab15\Documents\prime-documentary")
rows = json.loads((R / "scripts/_yt_studio_video_ctr.20260819.json").read_text(encoding="utf-8"))["rows"]
lf = [r for r in rows if (r.get("length_seconds") or 0) >= 600]

NAMED = re.compile(
    r"\b(OceanGate|Madoff|Alabama|Texas|Boston|FTX|IRS|SEC|FBI|Supreme Court|"
    r"Central Park|Hyatt|Ford|Pinto|Post Office|Theranos|D\.?B\.? Cooper|Surfside|"
    r"Lac[- ]M[ée]gantic|Itaewon|Lahaina|Morandi|Oroville|Uri|Titan|Wells Fargo)\b", re.I)
DEATH = re.compile(r"\b(died|killed|deaths?|dead|execute[d]?|murder)\b", re.I)

def block(name, sel):
    v = [r for r in lf if sel(r.get("title", ""))]
    if not v: print(f"  {name}: none"); return
    imp = [r.get("VIDEO_THUMBNAIL_IMPRESSIONS") or 0 for r in v]
    ctr = [r.get("VIDEO_THUMBNAIL_IMPRESSIONS_VTR") or 0.0 for r in v]
    ti = sum(imp)
    w = sum(i*c for i, c in zip(imp, ctr))/ti if ti else 0
    print(f"  {name:34s} n={len(v):3d}  median impressions {statistics.median(imp):7,.0f}  "
          f"weighted CTR {w:5.2f}%  clicks {sum(i*c/100 for i, c in zip(imp, ctr)):6.0f}")

print(f"long-form n={len(lf)}\n")
print("A. a searchable proper name in the title")
block("HAS a searchable name", lambda t: bool(NAMED.search(t)))
block("has NO searchable name", lambda t: not NAMED.search(t))

print("\nB. death language in the title")
block("HAS death language", lambda t: bool(DEATH.search(t)))
block("has NO death language", lambda t: not DEATH.search(t))

print("\nC. title length")
block("<= 60 characters", lambda t: len(t) <= 60)
block("61-80 characters", lambda t: 61 <= len(t) <= 80)
block("81+ characters", lambda t: len(t) > 80)

print("\nD. digits")
block("HAS a digit", lambda t: bool(re.search(r"\d", t)))
block("has NO digit", lambda t: not re.search(r"\d", t))
