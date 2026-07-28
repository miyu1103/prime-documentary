"""EP50 motion-first manifest v003. factory=stock+existing-i2v; motion=new-i2v; stills=S scenes only."""
import json, glob, os
from pathlib import Path
ROOT=Path(r"C:/Users/aab15/Documents/prime-documentary")
PUB=ROOT/"remotion/public/centralpark"
OUT=ROOT/"episodes/PD-2026-050-centralpark/05_visuals/asset_manifest.v003.json"
base=json.load(open(ROOT/"episodes/PD-2026-050-centralpark/05_visuals/asset_manifest.v001.json",encoding="utf-8"))
def pubs(sub,exts):
    r=[]
    for e in exts:
        for f in sorted(glob.glob(str(PUB/sub/f"*.{e}"))):
            r.append(f"centralpark/{sub}/{os.path.basename(f)}")
    return r
# factory pool = real stock + existing i2v (real motion)
factory=[]
for pp in pubs("stock",["mp4"])+pubs("motion",["mp4"]):
    factory.append({"asset_id":"CPK-FAC-"+os.path.basename(pp).split('.')[0],"kind":"video","public_path":pp})
# motion pool = new i2v (motion2)
motion=[]
for pp in pubs("motion2",["mp4"]):
    motion.append({"asset_id":"CPK-M2-"+os.path.basename(pp).split('.')[0],"kind":"video","public_path":pp})
# stills = ORIGINAL S body stills only (scenes/objects) — P/V are now motion, not static
stills=[s for s in base.get("stills",[]) if s.get("role")=="body" and os.path.basename(str(s.get("public_path",""))).startswith("S")]
m=dict(base)
m["factory"]=factory; m["motion"]=motion; m["stills"]=stills
m["_note"]="v003 MOTION-FIRST: factory=stock+existing-i2v, motion=new-i2v(101), stills=S scenes only"
json.dump(m,open(OUT,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(f"factory(real-motion)={len(factory)}  motion(new-i2v)={len(motion)}  stills(S)={len(stills)}")
print("WROTE",OUT)
