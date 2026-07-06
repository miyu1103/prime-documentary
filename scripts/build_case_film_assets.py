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
# CUT CADENCE (owner 2026-07-06 "毎回同じペースで画面が切替わるのは見ていて疲れる"): NOT a uniform
# ~3s metronome. This cycle deliberately mixes QUICK bursts (~1.6-2.4s) with LONG holds (~4.2-6.5s)
# so the underlying photo/footage bed alternates fast montage with calm held frames — the held
# frames are where a figure/kinetic-text animation carries the scene over a steady background
# (owner: "背景は同じで文字や図解のアニメーションでしばらく表現する瞬間があってもいい").
DUR_CYCLE = [1.7, 2.1, 5.6, 1.8, 3.0, 6.5, 2.0, 1.6, 4.2, 2.4, 5.2, 1.9]
# FOOTAGE NO-REUSE (owner 2026-07-06 "また天秤の動画素材" / "同じ素材が繰り返し使われる"): every
# factory clip is cut AT MOST ONCE in the whole film (reuse <= 1). If the distinct pool is smaller
# than the natural footage-cut count we emit FEWER footage cuts (filling with images) rather than
# repeat, and warn how many more distinct clips are needed. FOOT_SHARE_DESIRED is the footage
# fraction the old 3-of-5 cadence wanted; it only drives that shortfall warning now.
FOOT_SHARE_DESIRED = 0.60
# GENERIC SYMBOLS to DROP from the footage pool entirely (owner: over-familiar "天秤/木槌" stock).
GENERIC_PAT = r"scales|lady_justice|justice_statue|gavel|hourglass|balance|scales_of_justice"
# Overall (image-inclusive) diversity floor for the acceptance gate's footage_diversity; images
# necessarily repeat (small still pool) so this is measured over ALL cuts, footage is reuse<=1.
DIVERSITY_TARGET = 0.40
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


def _map_pins(mode: str):
    """Default stylized-map pins (0..1 coords) for a PinDropMap/RouteMap whose plan props carry
    only a `mode`, not explicit pin coordinates. FigureBeats' PinDropMap/RouteMap require pins."""
    m = (mode or "").strip().lower()
    if "resid" in m:                       # residential — a tight neighborhood cluster
        return [{"x": 0.46, "y": 0.5, "label": "HOME"},
                {"x": 0.52, "y": 0.56}, {"x": 0.49, "y": 0.45}]
    if "route" in m or "path" in m:        # a route line across the plane
        return [{"x": 0.22, "y": 0.62, "label": "STOP"}, {"x": 0.44, "y": 0.5},
                {"x": 0.66, "y": 0.44}, {"x": 0.82, "y": 0.34, "label": "HOME"}]
    # grid-multiply / nationwide default — spread across the map plane
    return [{"x": 0.22, "y": 0.34}, {"x": 0.4, "y": 0.28}, {"x": 0.58, "y": 0.4},
            {"x": 0.72, "y": 0.3}, {"x": 0.34, "y": 0.6}, {"x": 0.66, "y": 0.62},
            {"x": 0.5, "y": 0.5}]


def key_graphic_to_figure(component: str, props: dict):
    """Map one plan key_graphic (component name + props) to (kind, fields) for a
    FigureSpec, or None to skip. Only the BrandOpening/BrandEndcard bookends are dropped;
    every content graphic is wired (ActTitle->acttitle, CitationLowerThird->lowerthird,
    PinDropMap->pindropmap, RouteMap->routemap, RegionHighlightMap->regionmap)."""
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
    if c == "StateMap":
        f = {}
        if props.get("label"):
            f["label"] = str(props["label"])
        return ("statemap", f)
    if c == "RegionHighlightMap":
        f = {}
        if props.get("label"):
            f["label"] = str(props["label"])
        pat = str(props.get("pattern", "")).strip().lower()
        if pat in ("uniform", "varied"):
            f["pattern"] = pat
        return ("regionmap", f)
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
    if c == "CitationLowerThird":
        primary = str(props.get("case") or props.get("primary") or props.get("citation") or "")
        secondary = props.get("year") or props.get("secondary") or props.get("court")
        f = {"primary": primary}
        if secondary:
            f["secondary"] = str(secondary)
        return ("lowerthird", f)
    if c == "ActTitle":
        f = {"title": str(props.get("title") or props.get("label") or "")}
        if props.get("kicker"):
            f["kicker"] = str(props["kicker"])
        if props.get("index") is not None:
            f["index"] = props["index"]
        return ("acttitle", f)
    if c == "PinDropMap":
        pins = props.get("pins") or _map_pins(str(props.get("mode", "")))
        return ("pindropmap", {"pins": pins})
    if c == "RouteMap":
        pins = props.get("pins") or props.get("stops") or _map_pins("route")
        return ("routemap", {"pins": pins})
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


# --- figure / kinetic-text durations (owner 2026-07-06) --------------------------------------
# Moving diagrams are NO LONGER capped at a punchy 2.9s. FigureBeats' FigureScene applies a
# MONOTONIC Ken-Burns + raking light sweeps + perpetual Drift, so a long hold NEVER reads as a
# freeze — length is therefore safe, and the owner explicitly WANTS extended held moments where
# "背景は同じで文字や図解のアニメーションでしばらく表現する". HERO diagrams (the slam, the key/lock,
# the curtilage payoff, the Sotomayor quote, the car cutaway) run 7-10s where the animation is
# the whole point; supporting graphics run ~5.5-7.5s. This is the primary lever that raises
# moving-diagram coverage well past the old 8.6%.
FIG_DUR = {
    "brightline": 6.5,      # 'slam' promoted to a 9.0s hero hold below
    "carcutaway": 8.0,      # hero — the glovebox/trunk cutaway carries the scene
    "probablecause": 6.0,
    "curtilage": 8.5,       # hero — the curtilage payoff
    "statemap": 6.5,
    "regionmap": 6.5,
    "casetimeline_c": 7.5,
    "carkeylock": 9.0,      # hero — key/lock mechanism
    "numberticker": 6.5,
    "votetally": 7.5,
    "quote": 9.0,           # hero — the Sotomayor quote reads slowly
    "lowerthird": 5.5,
    "acttitle": 6.0,
    "pindropmap": 7.5,
    "routemap": 7.5,
}
FIG_DUR_DEFAULT = 6.0
KIN_STYLES = ["maskslide", "wordpop", "emphasis"]   # rotate for variety across spans


def _figure_dur(kind: str, fields: dict) -> float:
    """Target on-screen seconds for a diagram figure (hero kinds run long)."""
    if kind == "brightline" and str(fields.get("mode", "")).lower() == "slam":
        return 9.0
    return FIG_DUR.get(kind, FIG_DUR_DEFAULT)


def _kinetic_dur(lines: list) -> float:
    """Target on-screen seconds for a kinetic-caption block — scales with how much text there is
    so 3-line cards get a longer, readable hold (owner wants text to carry the scene for a while)."""
    n = len([l for l in lines if str(l).strip()])
    return {0: 0.0, 1: 6.0, 2: 7.5}.get(n, 9.0)


def _figure_groups(plan_path: Path, windows: dict) -> dict:
    """{span_id -> [(kind, fields), ...]} for every plan key_graphic that maps to a FigureSpec and
    anchors to a section-aligned window. Preserves plan order within each span."""
    groups: "dict[str, list]" = {}
    try:
        plan = json.loads(plan_path.read_text("utf-8")) if plan_path.exists() else {}
    except (OSError, ValueError) as e:
        print(f"WARN could not read plan {plan_path} for figures: {e}")
        return groups
    for kg in plan.get("key_graphics") or []:
        mapped = key_graphic_to_figure(kg.get("component", ""), kg.get("props") or {})
        if mapped is None:                        # BrandOpening/BrandEndcard only
            continue
        sid = _scene_id_to_span_id(kg.get("scene_id", ""))
        if sid is None or sid not in windows:     # no section-aligned window to anchor to -> skip
            continue
        groups.setdefault(sid, []).append(mapped)
    return groups


def build_animated(plan_path: Path, windows: dict, spans: list) -> list:
    """Emit film_data.figures: the moving-diagram tier (plan key_graphics) AND a 'kinetic'
    KineticCaptions block for EVERY span's on_screen_text, so animated diagrams + kinetic text
    punctuate the WHOLE body instead of clustering.

    Per span, the diagram figures then the span's kinetic-text block are laid out SEQUENTIALLY
    inside that span's section-aligned window (a small footage breath between them), so no two
    animated blocks overlap in time and each gets a real, readable hold. When the blocks would
    overrun the window they are scaled down proportionally to fit. Returns FigureSpec dicts sorted
    by start; kinetic blocks carry kind='kinetic' so callers can split diagram vs text coverage."""
    groups = _figure_groups(plan_path, windows)
    ost_by_span: dict = {}
    for sp in spans:
        sid = str(sp.get("span_id", ""))
        lines = [str(s) for s in (sp.get("on_screen_text") or []) if str(s).strip()]
        if lines:
            ost_by_span[sid] = lines
    figures: list = []
    GAP = 0.3   # footage breath between two animated blocks in one window
    ki = 0
    for sid in sorted(windows.keys(), key=lambda s: windows[s][0]):
        ws, we = windows[sid]
        blocks: list = []   # (dur, kind, fields)
        for kind, fields in groups.get(sid, []):
            blocks.append((_figure_dur(kind, fields), kind, fields))
        if sid in ost_by_span:
            blocks.append((_kinetic_dur(ost_by_span[sid]), "kinetic",
                           {"lines": ost_by_span[sid], "style": KIN_STYLES[ki % len(KIN_STYLES)]}))
            ki += 1
        if not blocks:
            continue
        avail = we - ws
        total = sum(d for d, _, _ in blocks) + GAP * (len(blocks) - 1)
        scale = (avail / total) if (total > avail and total > 0) else 1.0
        cur = ws
        for d, kind, fields in blocks:
            s = cur
            e = min(cur + d * scale, we)
            if e - s < 0.4:                       # never emit a sub-frame-flash block
                e = min(cur + 0.4, we)
            figures.append({"start": round(s, 3), "end": round(e, 3), "kind": kind, **fields})
            cur = e + GAP * scale
    figures.sort(key=lambda f: f["start"])
    return figures


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

    # --- footage pool: DROP generic symbols entirely (owner "また天秤の動画素材"), then NO-REUSE ---
    foot_generic=[s for s in foot if re.search(GENERIC_PAT, s, re.I)]
    foot_pool=[s for s in foot if not re.search(GENERIC_PAT, s, re.I)]
    n_generic_removed=len(foot_generic)

    # --- CUT TIME GRID first (varied cadence), THEN assign kinds so footage spreads evenly ---
    grid=[]; t=0.0; di=0
    while t < T-0.4:
        dur=DUR_CYCLE[di%len(DUR_CYCLE)]; di+=1
        if t+dur>T: dur=round(T-t,3)
        grid.append((round(t,3),round(dur,3))); t+=dur
    n=len(grid)
    # how many footage cuts the old 3-of-5 cadence WANTED, vs how many distinct clips we actually
    # have. NO-REUSE: cap footage cuts at the distinct pool size and spread them evenly; the rest
    # become image cuts (images may repeat — small still pool — but footage never does).
    natural_foot=round(FOOT_SHARE_DESIRED*n)
    n_foot=min(len(foot_pool), natural_foot) if imgs else min(len(foot_pool), n)
    foot_short=max(0, natural_foot-len(foot_pool))
    foot_positions=set(_even_positions(n, n_foot))       # evenly spaced footage indices
    foot_seq=list(foot_pool[:n_foot])                    # each distinct clip used exactly once
    # image round-robin: least-used first, honoring the min-gap when possible (reuse allowed)
    img_used={}; img_last={}
    def pick_img(i):
        elig=[s for s in imgs if i-img_last.get(s,-999)>MIN_GAP] or imgs
        s=sorted(elig,key=lambda s:(img_used.get(s,0), img_last.get(s,-999)))[0]
        img_used[s]=img_used.get(s,0)+1; img_last[s]=i
        return s
    # FOOTAGE only on SHORT slots. A nearly-static footage clip (e.g. a locked-off library shot)
    # held on a long slot reads as near-still to the freeze gate even with the drift overlay (which
    # is weaker on bright footage). Long holds are reserved for IMAGE cuts (Ken-Burns depth parallax)
    # and figure/kinetic-text moments (their own strong motion) — matching the owner's intent that
    # the LONG held moments are where an animation carries the scene, not static footage.
    FOOT_MAX_DUR = 3.0
    cuts=[]; fp=0
    for i,(st,dur) in enumerate(grid):
        if i in foot_positions and fp<len(foot_seq) and dur<=FOOT_MAX_DUR:
            src=foot_seq[fp]; fp+=1; is_foot=True
        elif imgs:
            src=pick_img(i); is_foot=False
        elif foot_pool:                                  # degenerate: no stills -> must reuse footage
            src=foot_pool[i%len(foot_pool)]; is_foot=True
        else:
            continue
        # image treatments are assigned in a second pass (below) so the depth share can be
        # guaranteed against the plan target / DEPTH_FLOOR; footage keeps the fixed "footage" look.
        cuts.append({"start":st,"dur":dur,"kind":"footage" if is_foot else "img",
                     "src":src,"seed":f"{slug}-{i}","treatment":"footage" if is_foot else None})

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
    # ANIMATED tier: moving diagrams (remotion_plan.key_graphics) + a 'kinetic' KineticCaptions
    # block for EVERY span's on_screen_text, laid out sequentially inside each span window so
    # animated diagrams + kinetic text punctuate the WHOLE body (not just 6 spans). The kinetic
    # blocks live in film_data.figures (kind='kinetic') and render via FigureBeats -> KineticCaptions
    # in the upper band, so `graphics` (the old GraphicsBeats path) is now empty (no double text).
    figures=build_animated(EPDIR/"04_scenes"/"remotion_plan.v001.json", windows, spans)
    beats=[]   # kinetic text now lives in figures[]; keep the graphics channel empty to avoid double-drawing

    hero=imgs[:6]
    hook=[]; ht=0.0
    for s in hero:
        hook.append({"start":round(ht,3),"dur":1.34,"kind":"img","src":s,"seed":f"hook-{ht}"}); ht+=1.34

    data={"episode_id":ep,"fps":FPS,"narration":f"{slug}/narration.mp3","narrationSeconds":round(T,3),
          "hookSeconds":round(ht,3),"hookLine":args.hookline,"hook":hook,"cuts":cuts,"captions":cues,
          "graphics":beats,"figures":figures}
    (PUB/"film_data.v001.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),"utf-8")
    (ROOT/"remotion"/"src"/"data"/f"{slug}_film.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),"utf-8")

    # ---------- coverage + pacing + footage-diversity report ----------
    import collections
    ni=sum(1 for c in cuts if c["kind"]=="img"); nf=sum(1 for c in cuts if c["kind"]=="footage")
    total=len(cuts)
    # animated coverage (moving diagrams + kinetic text) as a share of the body T
    diag=[f for f in figures if f["kind"]!="kinetic"]; kin=[f for f in figures if f["kind"]=="kinetic"]
    fig_secs=sum(f["end"]-f["start"] for f in diag); kin_secs=sum(f["end"]-f["start"] for f in kin)
    fig_pct=fig_secs/T*100 if T else 0.0; kin_pct=kin_secs/T*100 if T else 0.0
    comb_pct=(fig_secs+kin_secs)/T*100 if T else 0.0
    # cut-duration distribution (prove the cadence is VARIED, not metronomic)
    durs=[c["dur"] for c in cuts]
    buckets=collections.OrderedDict([("<2s",0),("2-3s",0),("3-4s",0),("4-5s",0),("5-7s",0),(">=7s",0)])
    for d in durs:
        if d<2: buckets["<2s"]+=1
        elif d<3: buckets["2-3s"]+=1
        elif d<4: buckets["3-4s"]+=1
        elif d<5: buckets["4-5s"]+=1
        elif d<7: buckets["5-7s"]+=1
        else: buckets[">=7s"]+=1
    dmin=min(durs) if durs else 0; dmax=max(durs) if durs else 0
    dmean=sum(durs)/len(durs) if durs else 0
    # footage no-reuse verification (measured over FOOTAGE cuts only)
    foot_cuts=[c for c in cuts if c["kind"]=="footage"]
    fcnt=collections.Counter(c["src"] for c in foot_cuts)
    foot_max_reuse=max(fcnt.values()) if fcnt else 0
    foot_distinct=len(fcnt)
    foot_generic_in_cuts=sum(1 for c in foot_cuts if re.search(GENERIC_PAT, c["src"], re.I))
    # overall (image-inclusive) diversity for the acceptance gate
    allcnt=collections.Counter(c["src"] for c in cuts); all_distinct=len(allcnt)
    all_frac=all_distinct/total if total else 0.0; all_max=allcnt.most_common(1)[0][1] if allcnt else 0
    # longest animated moments
    longest=sorted(figures, key=lambda f:f["end"]-f["start"], reverse=True)[:6]

    print(f"[{ep}] cuts={total}(img{ni}/foot{nf}) imgs={len(imgs)} factory_pool={len(foot)}->"
          f"{len(foot_pool)}(after -{n_generic_removed} generic)")
    print(f"[{ep}] ANIMATED COVERAGE: diagrams {len(diag)}fig {fig_secs:.0f}s ({fig_pct:.1f}%) + "
          f"kinetic-text {len(kin)} {kin_secs:.0f}s ({kin_pct:.1f}%) = COMBINED {comb_pct:.1f}% of body "
          f"(target >=40%)  [{'PASS' if comb_pct>=40 else 'UNDER'}]")
    print(f"[{ep}] CUT CADENCE: min={dmin:.1f}s max={dmax:.1f}s mean={dmean:.1f}s dist=" +
          " ".join(f"{k}:{v}" for k,v in buckets.items()))
    print(f"[{ep}] FOOTAGE: {nf} cuts, {foot_distinct} distinct, MAX REUSE={foot_max_reuse} "
          f"(no-reuse={'OK' if foot_max_reuse<=1 else 'FAIL'}), generics_in_cuts={foot_generic_in_cuts} "
          f"(removed {n_generic_removed} from pool)")
    print(f"[{ep}] OVERALL diversity (img-inclusive, for acceptance gate): distinct_frac={all_frac:.2f} "
          f"max_reuse={all_max} (gate needs distinct>=0.40 reuse<=4)")
    print(f"[{ep}] longest animated moments: " +
          " | ".join(f"{f['kind']}@{f['start']:.0f}s {f['end']-f['start']:.1f}s" for f in longest))
    if foot_short>0:
        print(f"  !! FOOTAGE POOL TOO SMALL for no-reuse: the cadence wanted ~{natural_foot} footage "
              f"cuts but only {len(foot_pool)} distinct clips remain after dropping generics. Used "
              f"{n_foot} footage cuts + more image cuts instead (no clip repeated). Stage >= {foot_short} "
              f"MORE distinct clips (e.g. scripts/select_factory_assets.py --theme <legal|crime|police|"
              f"finance>) into remotion/public/{slug}/factory and re-run to raise footage variety.")
    if all_frac < DIVERSITY_TARGET:
        need=int(-(-total*DIVERSITY_TARGET//1)) - all_distinct
        print(f"  !! OVERALL DIVERSITY LOW: distinct_frac {all_frac:.2f} < {DIVERSITY_TARGET:.2f}; "
              f"stage >= {need} more distinct clips or the acceptance gate footage_diversity may fail.")
    print(f"wrote remotion/public/{slug}/film_data.v001.json + src/data/{slug}_film.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
