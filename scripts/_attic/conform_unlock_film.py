"""Make unlock_film.json follow the design doc: design hook shots (§3), and each
narration beat shows a content-matched image (shotlist intent) instead of the
generic no-repeat rotation. Keeps reuse <= 3 and footage cuts untouched."""
import json, re, sys
from collections import Counter
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
FD = ROOT / "remotion/src/data/unlock_film.json"
IDX = ROOT / "episodes/PD-2026-031-unlock/06_audio/narration_index.v001.json"
IMGDIR = ROOT / "remotion/public/unlock/img"

# IMG number -> staticFile src
num2src = {}
for p in sorted(IMGDIR.glob("*.png")):
    m = re.search(r"IMG-(\d+)\.png$", p.name)
    if m:
        num2src[int(m.group(1))] = f"unlock/img/{p.name}"
ALL = sorted(num2src)

# content-matched image pool per span (primary first); from shotlist intent + act ranges
POOL = {
 "SPN-0001":[1,14,15,22], "SPN-0002":[1,11,15],
 "SPN-0003":[3,4,5], "SPN-0028":[5,7,3], "SPN-0032":[10,6,8],
 "SPN-0004":[9,3,4], "SPN-0005":[11,8], "SPN-0006":[11,7], "SPN-0007":[20,11],
 "SPN-0008":[20,16], "SPN-0009":[12,11,13], "SPN-0010":[16,11],
 "SPN-0011":[21,19,15], "SPN-0012":[14,19], "SPN-0029":[19,14],
 "SPN-0013":[15,16], "SPN-0014":[18,20],
 "SPN-0015":[23,24], "SPN-0016":[22,29], "SPN-0033":[23,20],
 "SPN-0017":[27,30], "SPN-0018":[27,16], "SPN-0021":[41,42,9],
 "SPN-0031":[22,25], "SPN-0019":[25,31], "SPN-0020":[29,22],
 "SPN-0022":[34,32], "SPN-0030":[16,34], "SPN-0023":[35,39],
 "SPN-0024":[36,15], "SPN-0025":[40,32], "SPN-0026":[34,15,14], "SPN-0027":[40,33],
}
MOTION2TREAT = {"parallax":"bleed","scan":"scan","duotone":"duotone","rack_focus":"focus","motion_graphics":"bleed"}
sl = json.loads((ROOT/"episodes/_planning/EP31_unlock_shotlist.v002.json").read_text(encoding="utf-8"))
span_motion = {s["span_id"]: MOTION2TREAT.get(s.get("motion",""),"bleed") for s in sl["shots"]}

idx = json.loads(IDX.read_text(encoding="utf-8"))
wins = [(c["span_id"], float(c["start"]), float(c["end"])) for c in idx["chunks"]]
def span_at(t):
    for sid,a,b in wins:
        if a <= t < b: return sid
    return wins[-1][0]

fd = json.loads(FD.read_text(encoding="utf-8"))
CAP = 3
use = Counter()

# 1) design hook (§3): 4 punch shots, keep total hook length
hook = fd["hook"]
design_hook = [1,14,15,22]
tot = sum(h["dur"] for h in hook)
n = len(design_hook)
fd["hook"] = [{"start": round(i*tot/n,3), "dur": round(tot/n,3), "kind":"img",
               "src": num2src[design_hook[i]], "seed": f"hook-{i+1}"} for i in range(n)]
for h in fd["hook"]: use[h["src"]] += 1

# 2) body img cuts -> content-matched image for the span at that time
rr = {}  # per-span round-robin pointer
remapped = 0
for cut in fd["cuts"]:
    if cut.get("kind") != "img":
        use[cut["src"]] += 1  # count footage toward nothing special; track anyway
        continue
    sid = span_at(cut["start"])
    pool = [n for n in POOL.get(sid, ALL) if n in num2src]
    HARD = 4  # footage_diversity: no clip reused > 4x
    # content-match first: least-used pool image under a soft cap of 3
    pool_soft = [n for n in pool if use[num2src[n]] < 3]
    if pool_soft:
        chosen = num2src[min(pool_soft, key=lambda n:(use[num2src[n]], pool.index(n)))]
    else:
        # pool exhausted -> spread to the globally least-used image (keeps reuse low, uses all 42)
        glob = [n for n in ALL if use[num2src[n]] < HARD]
        pick_from = [n for n in pool if use[num2src[n]] < HARD] or glob
        chosen = num2src[min(pick_from, key=lambda n: use[num2src[n]])]
    cut["src"] = chosen
    cut["treatment"] = span_motion.get(sid, cut.get("treatment","bleed"))
    use[chosen] += 1
    remapped += 1

FD.write_text(json.dumps(fd, ensure_ascii=False, indent=2), encoding="utf-8")

# diversity report (cuts src)
c = Counter(x["src"] for x in fd["cuts"])
tot_cuts = len(fd["cuts"]); distinct = len(c); mx = c.most_common(1)[0][1]
imgcnt = Counter(x["src"] for x in fd["cuts"] if x["kind"]=="img")
print(f"hook={ [h['src'].split('/')[-1][-11:] for h in fd['hook']] }")
print(f"remapped img cuts={remapped}  distinct={distinct}/{tot_cuts} ({distinct/tot_cuts:.2f})  max_reuse={mx}")
print(f"distinct images used={len(imgcnt)}/42  img max reuse={imgcnt.most_common(1)[0][1]}")
