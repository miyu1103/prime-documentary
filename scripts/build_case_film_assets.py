#!/usr/bin/env python3
r"""Stage assets + build the data-driven cut list / graphics beats for ANY PD case episode.

Generic version of build_kyllo_film_assets.py (--ep, --hookline). Uses ALL generated hero
stills + ALL factory clips (staged under remotion/public/<slug>/factory) in a no-repeat
rotation, builds the DESIGNED on_screen_text (script.annotated) into timed graphics beats,
and an 8s cold-open hook. Output -> remotion/public/<slug>/film_data.v001.json + src/data.

    py -3.11 scripts/build_case_film_assets.py --ep PD-2026-026-katz --hookline "The FBI recorded his calls—and never touched the booth."
"""
from __future__ import annotations
import argparse, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FPS = 30
MIN_GAP = 22
DUR_CYCLE = [3.0, 3.6, 3.2, 4.0, 3.4, 2.8]
KIND = ["img", "foot", "img", "foot", "foot"]
# footage diversity (owner 2026-07-04 "毎作品同じ素材 ... 天秤の動画は何度も見てきた").
# Cap reuse at build time so the acceptance gate's footage_diversity passes: aim stricter
# than the gate (gate = max 4 / distinct 0.40 / generic 2).
MAX_USES = 3                       # a clip may be cut at most this many times per film
GENERIC_PAT = r"scale|gavel|hourglass|clock|stopwatch|balance"  # over-familiar symbols
GENERIC_MAX = 1                    # a generic symbol may appear at most once
DIVERSITY_TARGET = 0.55            # warn (loudly) if distinct/total falls below this
# `depth` = real DPT depth-map 3D parallax (CaseFilm DepthStill); replaces the fake `bleed`
# pseudo-2.5D as the anti-紙芝居 default, rotated ~1/4 with the CSS treatments for variety and
# render feasibility. Requires <name>_depth.png beside each staged image (tools/depth/gen_depth.py).
IMG_TREAT = ["depth","scan","duotone","focus","depth","duotone","card","scan","focus","depth","duotone","scan"]


def parse_srt(path):
    cues=[]
    for b in re.split(r"\n\s*\n", path.read_text("utf-8").strip()):
        L=[x for x in b.splitlines() if x.strip()]
        if len(L)<2: continue
        m=re.search(r"(\d\d):(\d\d):(\d\d),(\d\d\d)\s*-->\s*(\d\d):(\d\d):(\d\d),(\d\d\d)", L[1])
        if not m: continue
        g=list(map(int,m.groups())); s=g[0]*3600+g[1]*60+g[2]+g[3]/1000; e=g[4]*3600+g[5]*60+g[6]+g[7]/1000
        txt=" ".join(L[2:]).strip()
        if txt: cues.append({"start":round(s,3),"end":round(e,3),"text":txt})
    return cues


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap=argparse.ArgumentParser(); ap.add_argument("--ep", required=True); ap.add_argument("--hookline", required=True)
    args=ap.parse_args(); ep=args.ep
    slug=re.sub(r"^PD-\d{4}-\d{3}-", "", ep)
    EPDIR=ROOT/"episodes"/ep
    IMG_SRC=EPDIR/"04_scenes"/"generated_images"
    INDEX=EPDIR/"06_audio"/"narration_index.v001.json"
    SRT=EPDIR/"08_edit"/"captions.final.v001.srt"
    ANN=EPDIR/"03_script"/"script.annotated.v001.json"
    media=Path(json.loads((ROOT/"config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
    MASTER=media/"episodes"/ep/"06_voice"/"master"/"vc_master_v001.mp3"
    PUB=ROOT/"remotion"/"public"/slug
    FACT=PUB/"factory"
    (PUB/"img").mkdir(parents=True, exist_ok=True); FACT.mkdir(parents=True, exist_ok=True)

    # stage stills (flatten) and narration
    imgs=[]
    for p in sorted(IMG_SRC.rglob("*.png")):
        if p.stat().st_size < 20000: continue
        shutil.copy2(p, PUB/"img"/p.name); imgs.append(f"{slug}/img/{p.name}")
    shutil.copy2(MASTER, PUB/"narration.mp3")
    foot=[f"{slug}/factory/{p.name}" for p in sorted(FACT.glob('*.mp4'))]
    if not foot:
        print(f"WARN no factory clips staged in {FACT} — stage themed clips first")

    idx=json.loads(INDEX.read_text("utf-8")); chunks=idx["chunks"]; T=max(c["end"] for c in chunks)
    cues=parse_srt(SRT)

    ALL_IMG=[("img",s) for s in imgs]; ALL_FOOT=[("foot",s) for s in foot]
    used={}; last={}
    def cap_for(src): return GENERIC_MAX if re.search(GENERIC_PAT, src, re.I) else MAX_USES
    def pick(pool,i):
        # prefer clips still under their reuse cap AND past the min-gap; fall back only if the
        # whole pool is exhausted (small staged pool -> the diversity warning fires below).
        under=[a for a in pool if used.get(a[1],0) < cap_for(a[1])]
        base=under or pool
        elig=[a for a in base if i-last.get(a[1],-999)>MIN_GAP]
        return sorted(elig or base, key=lambda a:(used.get(a[1],0), last.get(a[1],-999)))[0]
    cuts=[]; t=0.0; di=0; ict=0; lt=None
    while t < T-0.4:
        i=len(cuts); want=KIND[i%len(KIND)]
        kind,src = pick(ALL_IMG,i) if (want=="img" or not ALL_FOOT) else pick(ALL_FOOT,i)
        dur=DUR_CYCLE[di%len(DUR_CYCLE)]; di+=1
        if t+dur>T: dur=round(T-t,3)
        if kind=="foot": treat="footage"
        else:
            treat=IMG_TREAT[ict%len(IMG_TREAT)]; ict+=1
            if treat==lt: treat=IMG_TREAT[ict%len(IMG_TREAT)]; ict+=1
            lt=treat
        cuts.append({"start":round(t,3),"dur":round(dur,3),"kind":"footage" if kind=="foot" else "img","src":src,"seed":f"{slug}-{i}","treatment":treat})
        used[src]=used.get(src,0)+1; last[src]=i; t+=dur

    # graphics beats from annotated on_screen_text (span N <-> chunk N)
    ann=json.loads(ANN.read_text("utf-8")); spans=ann.get("spans",[])
    beats=[]
    for i,ch in enumerate(chunks):
        if i>=len(spans): break
        ost=spans[i].get("on_screen_text") or []
        if not ost: continue
        bs=ch["start"]; be=min(ch["end"]-0.3, bs+5.6)
        if be-bs<1.4: be=min(ch["end"]-0.1, bs+1.4)
        beats.append({"start":round(bs,3),"end":round(be,3),"lines":[s for s in ost if s.strip()]})

    hero=imgs[:6]
    hook=[]; ht=0.0
    for s in hero:
        hook.append({"start":round(ht,3),"dur":1.34,"kind":"img","src":s,"seed":f"hook-{ht}"}); ht+=1.34

    data={"episode_id":ep,"fps":FPS,"narration":f"{slug}/narration.mp3","narrationSeconds":round(T,3),
          "hookSeconds":round(ht,3),"hookLine":args.hookline,"hook":hook,"cuts":cuts,"captions":cues,"graphics":beats}
    (PUB/"film_data.v001.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),"utf-8")
    (ROOT/"remotion"/"src"/"data"/f"{slug}_film.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),"utf-8")
    ni=sum(1 for c in cuts if c["kind"]=="img"); nf=sum(1 for c in cuts if c["kind"]=="footage")
    import collections
    cnt=collections.Counter(c["src"] for c in cuts); distinct=len(cnt); total=len(cuts)
    frac=distinct/total if total else 0.0; worst=cnt.most_common(1)[0]
    print(f"[{ep}] imgs={len(imgs)} factory={len(foot)} cuts={total}(img{ni}/foot{nf}) "
          f"distinct={distinct} distinct_frac={frac:.2f} max_reuse={worst[1]} beats={len(beats)} hook={len(hook)} narr={T:.0f}s")
    if frac < DIVERSITY_TARGET:
        need=int(-(-total*DIVERSITY_TARGET//1)) - distinct  # ceil(total*target) - distinct
        print(f"  !! FOOTAGE DIVERSITY LOW: distinct_frac {frac:.2f} < {DIVERSITY_TARGET:.2f} "
              f"(pool only {distinct} distinct for {total} cuts). Stage >= {need} MORE distinct clips "
              f"(e.g. scripts/select_factory_assets.py --theme <legal|crime|police|finance>) into "
              f"remotion/public/{slug}/factory and re-run, OR the acceptance gate footage_diversity WILL fail.")
    print(f"wrote remotion/public/{slug}/film_data.v001.json + src/data/{slug}_film.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
