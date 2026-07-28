"""EP50 rebuild Stage 1a: inject the 36 people (P) + 48 diverse scenes (V) into the manifest
stills pool, INTERLEAVED with existing S stills so faces + variety appear throughout. Writes
asset_manifest.v002.json. (Stock + i2v are a later stage.)"""
import json, glob
from pathlib import Path
ROOT=Path(r"C:/Users/aab15/Documents/prime-documentary")
MAN=ROOT/"episodes/PD-2026-050-centralpark/05_visuals/asset_manifest.v001.json"
OUT=ROOT/"episodes/PD-2026-050-centralpark/05_visuals/asset_manifest.v002.json"
AI=Path("H:/pd-media/assets/ai/centralpark")
m=json.load(open(MAN,encoding="utf-8"))
existing=m.get("stills",[])
# new P + V as body stills
new=[]
for pre,rng in [("P",range(1,37)),("V",range(1,49))]:
    for i in rng:
        vid=f"{pre}{i:02d}"
        p=AI/f"{vid}.png"
        if not p.exists(): continue
        new.append({"asset_id":f"CPK-{vid}","scene_id":vid,"role":"body","also_thumb":False,
                    "act":0,"path":str(p).replace("\\","/"),
                    "public_path":f"centralpark/img/{vid}.png"})
print(f"existing body stills={sum(1 for s in existing if s.get('role')=='body')}  new P/V={len(new)}")
# interleave: insert the new faces/scenes evenly through the existing body-stills list
body=[s for s in existing if s.get("role")=="body"]
other=[s for s in existing if s.get("role")!="body"]
if new:
    step=max(1,len(body)//len(new))
    merged=[]; ni=0
    for i,s in enumerate(body):
        merged.append(s)
        if ni<len(new) and (i+1)%step==0:
            merged.append(new[ni]); ni+=1
    merged.extend(new[ni:])  # any remainder
else:
    merged=body
m["stills"]=other+merged
# dedupe public_path guard
seen=set(); dups=[x["public_path"] for x in m["stills"] if x.get("public_path") and (x["public_path"] in seen or seen.add(x["public_path"]))]
print(f"total stills now={len(m['stills'])}  dup public_path={len(dups)}")
m["_rebuild_note"]="v002: injected 36 people(P)+48 scenes(V) interleaved into body stills (2026-07-26)"
json.dump(m,open(OUT,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("WROTE",OUT)
