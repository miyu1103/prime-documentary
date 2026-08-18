# Build the distinct-playable-video pool exactly as EP68_pinto_register_inventory did.
import json,os,sys,glob
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
L=r"H:\pd-media\assets\archive\_ledger"
NOT={"purged.jsonl","ban_risk_quarantine.jsonl","shot_feedback.jsonl","factory_rename.progress.jsonl"}
SUF=("_removed.jsonl","_candidates.jsonl"); PRE=("rejects",)
def stock(b):
    if not b.endswith(".jsonl"): return False
    if b in NOT or b.startswith(PRE): return False
    return not b.endswith(SUF)
VIDEO={".mp4",".mov",".webm",".mkv",".avi",".mpeg",".mpg"}
# withheld sets
ban=set()
p=os.path.join(L,"ban_risk_quarantine.jsonl")
if os.path.exists(p):
    for l in open(p,encoding="utf-8",errors="replace"):
        try:r=json.loads(l);ban.add(f"{r.get('source')}:{r.get('id')}")
        except:pass
unus=set()
qv=r"H:\pd-media\assets\archive\_qc\archive_verdicts.jsonl"
if os.path.exists(qv):
    for l in open(qv,encoding="utf-8",errors="replace"):
        try:
            r=json.loads(l)
            if str(r.get("verdict","")).lower()=="unusable": unus.add((r.get("theme"),r.get("source")))
        except:pass
absent=set()
ap=os.path.join(L,"absent_index.json")
if os.path.exists(ap):
    absent=set(json.load(open(ap,encoding="utf-8")).get("absent",{}))
rows={}; nban=nq=nun=nabs=nmiss=0
for f in sorted(os.listdir(L)):
    if not stock(f): continue
    for l in open(os.path.join(L,f),encoding="utf-8",errors="replace"):
        try: r=json.loads(l)
        except: continue
        if (r.get("kind") or "")!="video":
            fp=r.get("file_path") or ""
            if os.path.splitext(fp)[1].lower() not in VIDEO: continue
        fp=r.get("file_path") or ""
        if not fp: continue
        key=f"{r.get('source')}:{r.get('id')}"
        if key in ban: nban+=1; continue
        if "_quarantine" in fp.replace("/","\\"): nq+=1; continue
        if (r.get("theme"),r.get("source")) in unus: nun+=1; continue
        if key in absent: nabs+=1; continue
        h=r.get("sha256") or fp
        if h in rows: continue
        rows[h]={"t":(r.get("title") or os.path.basename(fp)),"src":r.get("source"),"theme":r.get("theme"),"fp":fp}
print("distinct video rows (pre disk-check)",len(rows),"| withheld ban",nban,"quar",nq,"unusable",nun,"absent",nabs)
json.dump(rows,open("pool.json","w",encoding="utf-8"),ensure_ascii=False)
