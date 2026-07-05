#!/usr/bin/env python3
r"""Stage assets + build the data-driven cut list / graphics beats for ANY PD case episode.

Generic version of build_kyllo_film_assets.py (--ep, --hookline). Uses ALL generated hero
stills + ALL factory clips (staged under remotion/public/<slug>/factory) in a no-repeat
rotation, builds the DESIGNED on_screen_text (script.annotated) into timed graphics beats,
and an 8s cold-open hook. Output -> remotion/public/<slug>/film_data.v001.json + src/data.

    py -3.11 scripts/build_case_film_assets.py --ep PD-2026-026-katz --hookline "The FBI recorded his calls—and never touched the booth."
"""
from __future__ import annotations
import argparse, json, math, re, shutil, sys
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
# `depth` = real DPT depth-map 3D parallax (CaseFilm DepthStill); the only treatment that is
# genuine spatial parallax. `scan`/`duotone`/`focus` are FLAT CSS color/filter looks (variety only,
# NOT parallax). Design + scene_plan require depth on >= DEPTH_FLOOR of image cuts; the old table
# (depth 3/12 = 25%) silently undershot the 40% floor (defect M2, EP32_DESIGN_REMEDIATION.v001).
#
# IMG_TREAT is the single source of truth for the fallback treatment mix: `depth` now dominates at
# 6/12 = 50% (clears the 40% floor with margin), alternating with the flat looks so no two adjacent
# cuts share a treatment. The flat rotation and the fallback depth ratio are DERIVED from it below,
# so rebalancing this list rebalances the whole builder. Requires <name>_depth.png beside each
# staged image (tools/depth/gen_depth.py); a missing map hard-fails rather than silently downgrading.
IMG_TREAT = ["depth","scan","depth","duotone","depth","focus","depth","scan","depth","duotone","depth","focus"]
# flat (non-parallax) looks, de-duplicated in IMG_TREAT order; used to fill non-depth image cuts.
FLAT_TREATS = []
for _t in IMG_TREAT:
    if _t != "depth" and _t not in FLAT_TREATS:
        FLAT_TREATS.append(_t)
if not FLAT_TREATS:
    FLAT_TREATS = ["scan", "duotone", "focus"]
DEPTH_FLOOR = 0.40                                               # hard floor: >=40% of image cuts must be real depth
DEPTH_FALLBACK_RATIO = IMG_TREAT.count("depth") / len(IMG_TREAT)  # = 0.50 when no plan target is available
DEPTH_MAX_RATIO = 0.85                                            # cap so some flat variety always survives


def load_plan_depth_target(plan_path: Path):
    """Read the episode Remotion plan (if present) and return
    (explicit_depth_still_basenames, target_depth_ratio_for_image_cuts).

    Reconciles the builder with the plan (defect M2: the builder previously ignored the plan).
    - Explicit per-still depth marks are honored when the plan provides them via an optional
      `depth_stills` / `cut_treatments` field (either a list of basenames, or a list of
      {src|still|image, treatment|depth} objects).
      NOTE: remotion_plan.v001 encodes depth only as aggregate scene counts + a target percent,
      NOT as per-still ids, so this set is normally EMPTY and the even-distribution fallback fills
      in to hit the plan's target share.
      TODO(schema): have the scene planner emit per-still depth ids (matching the staged still
      basenames) so exact cuts can be pinned to depth instead of relying on the round-robin share.
    - target_depth_ratio: taken from motion_budget.depth.depth_cut_percent (or cut_plan_totals),
      floored at the plan's floor_percent and the hard DEPTH_FLOOR (0.40) and capped at
      DEPTH_MAX_RATIO. Falls back to DEPTH_FALLBACK_RATIO (0.50) when no plan is present.
    """
    depth_srcs: set = set()
    ratio = DEPTH_FALLBACK_RATIO
    try:
        plan = json.loads(plan_path.read_text("utf-8")) if plan_path.exists() else {}
    except (OSError, ValueError) as e:
        print(f"WARN could not read plan {plan_path}: {e}; using fallback depth ratio {ratio:.2f}")
        return depth_srcs, ratio
    if not plan:
        return depth_srcs, ratio
    # explicit per-still depth marks (optional; absent in v001 schema -> stays empty)
    for key in ("depth_stills", "cut_treatments"):
        for item in plan.get(key, []) or []:
            if isinstance(item, str):
                depth_srcs.add(Path(item).name)
            elif isinstance(item, dict):
                treat = str(item.get("treatment", "")).lower()
                s = item.get("src") or item.get("still") or item.get("image")
                if s and (treat == "depth" or item.get("depth") is True):
                    depth_srcs.add(Path(str(s)).name)
    # target depth share
    d = (plan.get("motion_budget") or {}).get("depth") or {}
    pct = d.get("depth_cut_percent")
    if pct is None:
        pct = (plan.get("cut_plan_totals") or {}).get("depth_cut_percent")
    floor_pct = d.get("floor_percent", 40) or 0
    cands = [DEPTH_FLOOR, floor_pct / 100.0]
    if pct is not None:
        cands.append(pct / 100.0)
    ratio = min(max(cands), DEPTH_MAX_RATIO)
    return depth_srcs, ratio


def _even_positions(m: int, k: int):
    """k evenly-spaced, distinct, increasing indices in range(m) (requires 0 <= k <= m)."""
    if k <= 0 or m <= 0:
        return []
    return [(x * m) // k for x in range(k)]


def assign_image_treatments(img_cuts, plan_depth_srcs, target_ratio):
    """Deterministically assign a treatment to each image cut so real DPT `depth` parallax covers
    >= target_ratio of image cuts (>= DEPTH_FLOOR). Plan-marked stills are pinned to depth first;
    the remaining depth budget is spread evenly across the rest; everything else rotates through
    the flat looks (FLAT_TREATS) for variety. Pure function (no I/O) so it is unit-testable."""
    n = len(img_cuts)
    if n == 0:
        return []
    is_depth = [Path(c["src"]).name in plan_depth_srcs for c in img_cuts]
    have = sum(is_depth)
    want = min(max(have, math.ceil(target_ratio * n)), n)
    free = [i for i, d in enumerate(is_depth) if not d]
    add = max(0, want - have)
    for j in _even_positions(len(free), add):
        is_depth[free[j]] = True
    treats = []
    fi = 0
    for i in range(n):
        if is_depth[i]:
            treats.append("depth")
        else:
            treats.append(FLAT_TREATS[fi % len(FLAT_TREATS)])
            fi += 1
    return treats


def depth_map_path(pub: Path, src: str) -> Path:
    """Filesystem path of the DPT depth map for a staged still, matching CaseFilm.tsx depthSrcOf
    (`<name>.<ext>` -> `<name>_depth.png`). `src` is the logical uri `<slug>/img/<name>.<ext>`."""
    p = pub.parent / src            # remotion/public / "<slug>/img/<name>.<ext>"
    return p.with_name(re.sub(r"\.[^.]+$", "_depth.png", p.name))


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


# ---------------------------------------------------------------------------
# figures tier: map the episode Remotion plan's key_graphics (carsearch/motionkit
# "moving diagram" components) into film_data.figures = FigureSpec[] so CaseFilm's
# <FigureBeats> actually renders them. Generic: any episode with a remotion_plan
# key_graphics list gets figures; without one it stays []. Pure mapping (no I/O)
# so it is unit-testable. See remotion/src/components/FigureBeats.tsx FigureSpec.
# ---------------------------------------------------------------------------

def _brightline_mode(props: dict) -> str:
    """BrightLine enum is 'draw'|'hold'|'slam'. The plan sometimes writes a
    transition like 'draw->slam'; collapse it to the closest single valid enum
    (the impact end-state), defaulting to 'draw'."""
    m = str(props.get("mode", "draw")).strip().lower()
    if m in ("draw", "hold", "slam"):
        return m
    if "slam" in m:
        return "slam"
    if "hold" in m:
        return "hold"
    return "draw"


def key_graphic_to_figure(component: str, props: dict):
    """Map one plan key_graphic (component name + props) to (kind, fields) for a
    FigureSpec, or None to skip (BrandOpening/BrandEndcard bookends and any
    component not wired into FigureBeats, e.g. PinDropMap/CitationLowerThird/ActTitle)."""
    props = props or {}
    c = (component or "").strip()
    if c == "BrightLine":
        return ("brightline", {"mode": _brightline_mode(props)})
    if c == "CarCutaway":
        f: dict = {"mode": str(props.get("mode", "all")).strip().lower()}
        if props.get("zones"):
            f["zones"] = [str(z) for z in props["zones"]]
        return ("carcutaway", f)
    if c == "ProbableCauseMeter":
        return ("probablecause", {"outcome": str(props.get("outcome", "cross")).strip().lower()})
    if c == "CurtilageShield":
        return ("curtilage", {})
    if c in ("StateMap", "RegionHighlightMap"):
        f = {}
        if props.get("label"):
            f["label"] = str(props["label"])
        return ("statemap", f)
    if c == "CaseTimeline":
        events = [
            {"year": str(e.get("year", "")), "text": str(e.get("text", ""))}
            for e in (props.get("events") or [])
            if isinstance(e, dict)
        ]
        return ("casetimeline_c", {"events": events})
    if c == "CarKeyLock":
        return ("carkeylock", {})
    if c == "NumberTicker":
        f = {"value": props.get("value", 0)}
        for k in ("prefix", "suffix", "decimals", "label", "topLabel"):
            if props.get(k) is not None:
                f[k] = props[k]
        return ("numberticker", f)
    if c == "VoteTally":
        f = {"majority": props.get("majority", 0), "dissent": props.get("dissent", 0)}
        if props.get("label"):
            f["label"] = str(props["label"])
        return ("votetally", f)
    if c == "QuoteCard":
        return ("quote", {"quote": str(props.get("quote", "")),
                          "attribution": str(props.get("attribution", ""))})
    return None


# ---------------------------------------------------------------------------
# SECTION-ALIGNED span -> narration TIME WINDOW (narration-timing fix).
# The annotated script has 22 spans (SPN-00NN, one per scene S0NN); the narration
# has 52 spoken chunks. The old builder mapped scene/span S0NN -> chunk index N (1:1),
# but 22 != 52, so every figure/text beat landed ~30s off its content (e.g. the
# NumberTicker(68) sat at chunk 4 = 38.3s, while "sixty-eight bottles" is actually
# spoken at 74.2-89.8s). Fix: align by SECTION. Group the chunks into their sections
# (HOOK/OPENING/ACT I..IV/ENDING) to get each section's contiguous time range, then
# place a span at the equal sub-slice of its section's range corresponding to its
# ordinal position among the spans of that section's chapter. This lands every figure
# and kinetic-text beat inside the CORRECT section at roughly the right position.
# ---------------------------------------------------------------------------

_ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7}


def _norm_section(s: str) -> str:
    """Canonicalize a chapter_id/title OR a narration `section` string to one comparable
    key so 'act1', 'Act I', 'ACT I' all collapse to 'ACT1' (and hook/opening/ending pass
    through). Robust to case, spaces, punctuation and roman-vs-arabic act numbering."""
    t = re.sub(r"[^a-z0-9]", "", (s or "").lower())   # 'act i' -> 'acti'; 'act1' -> 'act1'
    if t.startswith("hook"):
        return "HOOK"
    if t.startswith("opening"):
        return "OPENING"
    if t.startswith("ending"):
        return "ENDING"
    m = re.match(r"act([ivx]+|\d+)$", t)
    if m:
        g = m.group(1)
        n = int(g) if g.isdigit() else _ROMAN.get(g.upper(), 0)
        return f"ACT{n}"
    return t.upper()


def build_span_time_windows(chunks: list, chapters: list) -> dict:
    """Map every span_id -> (start, end) narration time window via SECTION alignment.

    1. Group the narration chunks by their normalized `section` -> each section gets a
       contiguous time range [min chunk start, max chunk end].
    2. For each chapter, normalize chapter_id/title to a section key and take its ordered
       span_ids. A span at ordinal p of P spans in section X gets the p-th equal sub-slice
       of section X's time range: start = sec_start + (p/P)*range, end = start + (1/P)*range.

    Pure function (no I/O) so it is unit-testable. Returns {} span_ids with no matching
    section are simply omitted (callers skip them)."""
    windows: dict = {}
    # section time ranges (preserve nothing but min/max; sections are contiguous in the index)
    sec_range: dict = {}
    for ch in chunks:
        key = _norm_section(ch.get("section", ""))
        s = float(ch["start"]); e = float(ch["end"])
        if key in sec_range:
            lo, hi = sec_range[key]
            sec_range[key] = (min(lo, s), max(hi, e))
        else:
            sec_range[key] = (s, e)
    for chap in chapters or []:
        key = _norm_section(chap.get("chapter_id") or chap.get("title") or "")
        span_ids = chap.get("span_ids") or []
        if key not in sec_range or not span_ids:
            continue
        s0, e0 = sec_range[key]
        rng = e0 - s0
        P = len(span_ids)
        for p, sid in enumerate(span_ids):
            ws = s0 + (p / P) * rng
            we = ws + (1.0 / P) * rng
            windows[str(sid)] = (ws, we)
    return windows


def _scene_id_to_span_id(scene_id: str) -> str | None:
    """Scene 'S0NN' -> span id 'SPN-00NN' (both key the same ordinal in this pipeline)."""
    m = re.match(r"S0*(\d+)", str(scene_id or ""))
    return f"SPN-{int(m.group(1)):04d}" if m else None


def build_figures(plan_path: Path, windows: dict) -> tuple:
    """Read <ep>/04_scenes/remotion_plan.v001.json key_graphics and emit FigureSpec[].
    scene 'S0NN' -> span 'SPN-00NN' -> its SECTION-ALIGNED narration window (see
    build_span_time_windows); when several key_graphics share a scene, that span window
    is split into equal sequential sub-slots so the full-screen figures never stack
    destructively. Returns (figures, fig_span_ids) — fig_span_ids drives the text-beat
    declutter (one clear graphic per moment)."""
    figures: list = []
    fig_span_ids: set = set()
    try:
        plan = json.loads(plan_path.read_text("utf-8")) if plan_path.exists() else {}
    except (OSError, ValueError) as e:
        print(f"WARN could not read plan {plan_path} for figures: {e}")
        return figures, fig_span_ids
    kgs = plan.get("key_graphics") or []
    if not kgs:
        return figures, fig_span_ids
    # group mapped key_graphics by span id, preserving plan order
    groups: "dict[str, list]" = {}
    order: list = []
    for kg in kgs:
        mapped = key_graphic_to_figure(kg.get("component", ""), kg.get("props") or {})
        if mapped is None:
            continue
        sid = _scene_id_to_span_id(kg.get("scene_id", ""))
        if sid is None or sid not in windows:   # no section-aligned window to anchor to -> skip
            continue
        if sid not in groups:
            groups[sid] = []
            order.append(sid)
        groups[sid].append(mapped)
    # Keep each moving diagram a PUNCHY beat (~7s), not the whole section window.
    # A figure's full-screen scene hides the photo/footage cuts underneath, so an
    # un-capped figure (a 30s section slot) would sit on one static graphic and bury
    # all the story images. Cap the duration and let the cuts show for the rest.
    FIGURE_MAX_DUR = 7.0
    for sid in order:
        items = groups[sid]
        ws, we = windows[sid]
        k = len(items)
        slot = (we - ws) / k if k else 0.0
        for j, (kind, fields) in enumerate(items):
            s = ws + slot * j
            e = min(ws + slot * (j + 1), s + FIGURE_MAX_DUR)
            figures.append({"start": round(s, 3), "end": round(e, 3), "kind": kind, **fields})
        fig_span_ids.add(sid)
    figures.sort(key=lambda f: f["start"])
    return figures, fig_span_ids


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap=argparse.ArgumentParser(); ap.add_argument("--ep", required=True); ap.add_argument("--hookline", required=True)
    ap.add_argument("--allow-missing-depth-maps", action="store_true",
                    help="downgrade the missing-depth-map hard error to a warning for the staging phase "
                         "(run before tools/depth/gen_depth.py has produced the maps, then re-run strict).")
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
        if p.stem.endswith("_depth"): continue   # depth maps are not stills (gen_depth.py output); never cut them
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
    cuts=[]; t=0.0; di=0
    while t < T-0.4:
        i=len(cuts); want=KIND[i%len(KIND)]
        kind,src = pick(ALL_IMG,i) if (want=="img" or not ALL_FOOT) else pick(ALL_FOOT,i)
        dur=DUR_CYCLE[di%len(DUR_CYCLE)]; di+=1
        if t+dur>T: dur=round(T-t,3)
        is_foot = (kind=="foot")
        # image treatments are assigned in a second pass (below) so the depth share can be
        # guaranteed against the plan target / DEPTH_FLOOR; footage keeps the fixed "footage" look.
        cuts.append({"start":round(t,3),"dur":round(dur,3),"kind":"footage" if is_foot else "img",
                     "src":src,"seed":f"{slug}-{i}","treatment":"footage" if is_foot else None})
        used[src]=used.get(src,0)+1; last[src]=i; t+=dur

    # --- image treatment assignment (defect M2: real depth >= 40% + read the plan) ---
    img_cuts=[c for c in cuts if c["kind"]=="img"]
    plan_depth_srcs, target_ratio = load_plan_depth_target(EPDIR/"04_scenes"/"remotion_plan.v001.json")
    for c, tr in zip(img_cuts, assign_image_treatments(img_cuts, plan_depth_srcs, target_ratio)):
        c["treatment"]=tr
    n_img=len(img_cuts); n_depth=sum(1 for c in img_cuts if c["treatment"]=="depth")
    depth_share=(n_depth/n_img) if n_img else 0.0
    print(f"[{ep}] image treatments: depth={n_depth}/{n_img} ({depth_share*100:.1f}%) "
          f"target={target_ratio*100:.1f}% floor={DEPTH_FLOOR*100:.0f}% plan_pins={len(plan_depth_srcs)} "
          f"flats={FLAT_TREATS}")
    if n_img and depth_share < DEPTH_FLOOR:   # defensive: should never trip given assign_image_treatments
        raise SystemExit(f"[{ep}] ABORT: depth share {depth_share*100:.1f}% < floor {DEPTH_FLOOR*100:.0f}% "
                         f"after assignment — refusing to write an under-parallaxed cut list.")

    # --- depth-map existence gate (defect M2: never silently downgrade a depth cut to a flat look) ---
    # CaseFilm.tsx quietly falls back to a flat/bleed look when <name>_depth.png is missing; that is
    # exactly how the designed depth share silently eroded. Fail here so the operator generates the
    # maps (tools/depth/gen_depth.py) before the real render, instead of shipping fake depth.
    missing=[(c["src"], depth_map_path(PUB, c["src"])) for c in img_cuts
             if c["treatment"]=="depth" and not depth_map_path(PUB, c["src"]).exists()]
    if missing:
        print(f"[{ep}] !! DEPTH MAP MISSING for {len(missing)} of {n_depth} depth cut(s):", file=sys.stderr)
        for s, dm in missing[:20]:
            print(f"    {s} -> expected {dm}", file=sys.stderr)
        if len(missing) > 20:
            print(f"    ... and {len(missing)-20} more", file=sys.stderr)
        print(f"    Generate them first (ComfyUI venv):\n"
              f"      C:\\Users\\aab15\\ComfyUI\\venv\\Scripts\\python.exe tools/depth/gen_depth.py "
              f"remotion/public/{slug}", file=sys.stderr)
        if not args.allow_missing_depth_maps:
            raise SystemExit(
                f"[{ep}] ABORT: {len(missing)} depth-treated cut(s) lack <name>_depth.png. Refusing to write "
                f"film_data whose depth cuts would silently fall back to a flat treatment at render "
                f"(this is how depth quietly dropped to 25%). Run gen_depth.py then re-run, or pass "
                f"--allow-missing-depth-maps to stage first.")
        print(f"[{ep}] WARN proceeding with --allow-missing-depth-maps; you MUST run gen_depth.py and re-run "
              f"before the real render, or these depth cuts will render as flat.", file=sys.stderr)

    ann=json.loads(ANN.read_text("utf-8")); spans=ann.get("spans",[]); chapters=ann.get("chapters",[])
    # SECTION-ALIGNED span -> narration time windows (narration-timing fix): every span
    # (SPN-00NN <-> scene S0NN) lands inside its own section (HOOK/OPENING/ACT I..IV/ENDING)
    # at the right ordinal position, instead of the old broken span N -> chunk N (22 vs 52).
    windows=build_span_time_windows(chunks, chapters)
    # figures first (carsearch/motionkit moving diagrams from remotion_plan.key_graphics)
    # so the overlapping kinetic-text beat on the same span can be suppressed ->
    # ONE clear graphic per moment (the figure IS the graphic; no text/figure collision).
    figures, fig_span_ids=build_figures(EPDIR/"04_scenes"/"remotion_plan.v001.json", windows)
    # graphics text beats from annotated on_screen_text, placed at each span's
    # section-aligned window, skipped on any span a figure already occupies (declutter).
    beats=[]
    for sp in spans:
        sid=str(sp.get("span_id",""))
        if sid not in windows: continue
        if sid in fig_span_ids: continue
        ost=sp.get("on_screen_text") or []
        if not ost: continue
        ws,we=windows[sid]
        bs=ws; be=min(we-0.3, bs+5.6)
        if be-bs<1.4: be=min(we-0.1, bs+1.4)
        beats.append({"start":round(bs,3),"end":round(be,3),"lines":[s for s in ost if s.strip()]})

    hero=imgs[:6]
    hook=[]; ht=0.0
    for s in hero:
        hook.append({"start":round(ht,3),"dur":1.34,"kind":"img","src":s,"seed":f"hook-{ht}"}); ht+=1.34

    data={"episode_id":ep,"fps":FPS,"narration":f"{slug}/narration.mp3","narrationSeconds":round(T,3),
          "hookSeconds":round(ht,3),"hookLine":args.hookline,"hook":hook,"cuts":cuts,"captions":cues,
          "graphics":beats,"figures":figures}
    (PUB/"film_data.v001.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),"utf-8")
    (ROOT/"remotion"/"src"/"data"/f"{slug}_film.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),"utf-8")
    ni=sum(1 for c in cuts if c["kind"]=="img"); nf=sum(1 for c in cuts if c["kind"]=="footage")
    import collections
    cnt=collections.Counter(c["src"] for c in cuts); distinct=len(cnt); total=len(cuts)
    frac=distinct/total if total else 0.0; worst=cnt.most_common(1)[0]
    print(f"[{ep}] imgs={len(imgs)} factory={len(foot)} cuts={total}(img{ni}/foot{nf}) "
          f"distinct={distinct} distinct_frac={frac:.2f} max_reuse={worst[1]} beats={len(beats)} "
          f"figures={len(figures)} hook={len(hook)} narr={T:.0f}s")
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
