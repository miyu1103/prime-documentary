# -*- coding: utf-8 -*-
"""Measure the shipped thumbnails against CTR. Eyeballing two images is not evidence."""
import json, re, sys, io, glob, statistics, math
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = Path(r"C:\Users\aab15\Documents\prime-documentary")
try:
    from PIL import Image, ImageStat, ImageFilter
except ImportError:
    print("Pillow not installed in this interpreter"); raise SystemExit(1)

ctr_rows = json.loads((R / "scripts/_yt_studio_video_ctr.20260819.json").read_text(encoding="utf-8"))["rows"]
BYID = {r["video_id"]: r for r in ctr_rows}

# episode -> video id, from whatever receipt carries it
def video_id_for(epdir: Path):
    for pat in ("09_package/youtube_schedule_result*.json", "09_package/final_delivery*.json",
                "09_package/youtube_upload*.json", "manifest.json"):
        for f in epdir.glob(pat):
            try: t = f.read_text(encoding="utf-8", errors="ignore")
            except Exception: continue
            for m in re.finditer(r'"(?:video_id|videoId|id)"\s*:\s*"([A-Za-z0-9_-]{11})"', t):
                if m.group(1) in BYID:
                    return m.group(1)
    return None

def shipped_thumb(epdir: Path):
    cands = sorted(epdir.glob("09_package/thumbnail.selected.v*.png")) + \
            sorted(epdir.glob("09_package/thumbnail.selected.v*.jpg"))
    if cands:
        return cands[-1]
    other = sorted(epdir.glob("09_package/thumbnail*.png"))
    return other[-1] if other else None

rows = []
for epdir in sorted((R / "episodes").glob("PD-2026-*")):
    vid = video_id_for(epdir)
    if not vid: continue
    r = BYID[vid]
    if (r.get("length_seconds") or 0) < 600: continue
    th = shipped_thumb(epdir)
    if not th: continue
    try:
        im = Image.open(th).convert("RGB").resize((320, 180))
    except Exception:
        continue
    g = im.convert("L")
    st = ImageStat.Stat(g)
    edges = ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES))
    # how much of the frame is very bright (big white/gold type) and very dark
    px = list(g.getdata())
    bright = sum(1 for p in px if p > 200) / len(px)
    dark = sum(1 for p in px if p < 40) / len(px)
    # colour: is it gold/amber dominated?
    rgb = ImageStat.Stat(im).mean
    warm = (rgb[0] + rgb[1]) / 2 - rgb[2]
    rows.append(dict(ep=epdir.name, ctr=r.get("VIDEO_THUMBNAIL_IMPRESSIONS_VTR") or 0.0,
                     imp=r.get("VIDEO_THUMBNAIL_IMPRESSIONS") or 0,
                     mean=st.mean[0], sd=st.stddev[0], bright=bright, dark=dark,
                     edge=edges.mean[0], warm=warm, file=th.name))

print(f"episodes matched to a video id, a CTR and a thumbnail: {len(rows)}")
big = [r for r in rows if r["imp"] >= 300]
print(f"of which >=300 impressions: {len(big)}\n")
if len(big) < 8:
    print("too few to correlate; printing what there is")
    big = rows

def pearson(xs, ys):
    n = len(xs)
    if n < 3: return 0
    mx, my = sum(xs)/n, sum(ys)/n
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x-mx)**2 for x in xs)); dy = math.sqrt(sum((y-my)**2 for y in ys))
    return num/(dx*dy) if dx and dy else 0

ys = [r["ctr"] for r in big]
for k, lbl in (("mean", "mean brightness"), ("sd", "contrast (sd)"),
               ("bright", "fraction very bright (>200)"), ("dark", "fraction very dark (<40)"),
               ("edge", "edge energy"), ("warm", "warmth (gold vs blue)")):
    print(f"  r(CTR, {lbl:28s}) = {pearson([r[k] for r in big], ys):+.2f}")

print("\n  by CTR, high to low:")
print(f"{'CTR':>6} {'imp':>6} {'mean':>6} {'sd':>6} {'bright%':>8} {'dark%':>7} {'warm':>6}  episode")
for r in sorted(big, key=lambda x: -x["ctr"]):
    print(f"{r['ctr']:6.2f} {r['imp']:6d} {r['mean']:6.1f} {r['sd']:6.1f} "
          f"{r['bright']*100:8.1f} {r['dark']*100:7.1f} {r['warm']:+6.1f}  {r['ep'][8:]}")
