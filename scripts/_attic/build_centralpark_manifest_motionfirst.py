"""EP50 manifest v003. factory=F-loops+stock; motion=i2v (existing + new); stills=S scenes only.

★2026-07-30 (acceptance FAIL fix): the v003 written on 2026-07-26 defined factory as
stock+motion and left the 485 F-loops in remotion/public/centralpark/factory staged but
UNREFERENCED. check_final_acceptance measured it exactly: footage_utilization 17%
(485/485 clips used 0 times) with asset_reuse at 69% because the small pool had to repeat.
The F-loops are this episode's own on-theme material (cold cyan interrogation rooms,
institutional corridors, 1989 NYC night streets, text-free) and the builder's ANTI-KAMISHIBAI
assert was written expecting 485 of them. They go back in the factory pool; both i2v
generations move to motion, so nothing is dropped and nothing repeats.
"""
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
# factory pool = the episode's own F-loops + real stock footage
factory=[]
for pp in pubs("factory",["mp4"])+pubs("stock",["mp4"]):
    factory.append({"asset_id":"CPK-FAC-"+os.path.basename(pp).split('.')[0],"kind":"video","public_path":pp})
# motion pool = both i2v generations (M*_rife + cp_*)
motion=[]
for pp in pubs("motion",["mp4"])+pubs("motion2",["mp4"]):
    motion.append({"asset_id":"CPK-MOT-"+os.path.basename(pp).split('.')[0],"kind":"video","public_path":pp})
# stills = ORIGINAL S body stills only (scenes/objects) — P/V are now motion, not static
stills=[s for s in base.get("stills",[]) if s.get("role")=="body" and os.path.basename(str(s.get("public_path",""))).startswith("S")]
m=dict(base)
m["factory"]=factory; m["motion"]=motion; m["stills"]=stills
m["_note"]="v003 2026-07-30: factory=F-loops+stock (footage_utilization fix), motion=all i2v, stills=S scenes only"
json.dump(m,open(OUT,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(f"factory(F+stock)={len(factory)}  motion(i2v)={len(motion)}  stills(S)={len(stills)}")
print("WROTE",OUT)
