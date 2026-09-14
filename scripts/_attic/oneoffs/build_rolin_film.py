#!/usr/bin/env python3
r"""Reusable assembly builder for Prime Documentary EP34 "rolin" (PD-2026-034-rolin,
airport civil forfeiture) — the CaseFilm data-driven cut list / figure beats.

Modeled CLOSELY on scripts/build_case_film_assets.py (carsearch): same CLI shape
(--ep/--hookline), the same FilmData output keys (fps/narration/narrationSeconds/
hookSeconds/hookLine/hook/cuts/captions/graphics/figures), the same cut-time-grid +
treatment-assignment + depth-map gate + SRT caption parsing patterns. It writes:

    remotion/public/rolin/film_data.v001.json
    remotion/src/data/rolin_film.json

which the `CaseFilm` composition renders. Differences from carsearch (all justified by
the EP34 design bible + animation-assets manifest):

  * TIMING: read narration_index.v00N.json IF present (167 chunks, 8 sections). If it is
    ABSENT (produced by another team, may be missing), fall back to the DESIGN §6 per-act
    second budget (HOOK 8 / OP 17 / 幕1 244 / 幕2 221 / 幕3 223 / 幕4 242 / 幕5 213 / ED 36
    ≈ 1204s) and emit a design-timed PREVIEW film_data. The source is printed clearly.
  * CUT GRID: built per-act from the design §6 cut allocation (160 image cuts + 188 footage
    cuts) so the per-act image/footage split matches the bible. Cuts fill each act window
    CONTINUOUSLY (carsearch pattern) and figures OVERLAY on top (so the moving cut sits
    behind every FigureBeats.SceneBed, exactly like carsearch).
  * FOOTAGE: no-reuse (each factory clip cut at most once). If NO factory clips are staged
    (the current EP34 state), footage slots degrade to image cuts and a WARN is printed —
    it never crashes.
  * FIGURES: the 44 figure beats are placed from the §1 figure table by ACT (OP/幕1..幕5/ED),
    each with its correct FigureBeats `kind` (the 7 aircash kinds cashstack/burdenflip/
    signswap/xrayscan/convergemap/thresholdmeter/returnledger + reused kinds numberticker/
    pindropmap/casetimeline_c/kinetic/lowerthird/acttitle/mechanism). Only design-confirmed
    numbers are burned in (numberticker $209M/$3.2B/$68.8B/$22M vs 57/$800K/~$82,000); every
    other figure passes minimal props and relies on the component self-defaults (no
    fabricated facts — CLAUDE invariant 1).
  * HERO Blender mp4s: 5 exist (checkpointconverge / signswap / usforfeiture_209m/32b/688b).
    CaseFilm has NO clean hero-video cut mechanism (its only OffthreadVideo path is a
    `footage` cut which forces a startFrom offset + Ken-Burns + navy tint — unsuitable for a
    pre-composed hero). So per design, each hero figure is emitted with its normal FigureBeats
    `kind` AND the hero mapping is recorded in an informational `heroVideos` block + printed,
    proposing the minimal integration (add a `footage` cut of src `rolin/hero_<name>.mp4`, or
    a tiny hero-cut type). CaseFilm is NOT modified.

    py scripts/build_rolin_film.py --ep PD-2026-034-rolin --hookline "You broke no law. By the gate, your cash was gone."
"""
from __future__ import annotations
import argparse, json, math, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# EP34 is a 60fps super-heavy composition (ANIMATION_ASSETS §0: 合成fps 60 / durationInFrames 72000).
# CaseFilm reads useVideoConfig().fps for all frame math (data.fps is informational), so this value
# documents the design's canonical fps; register CaseFilm-rolin at 60fps to honor it.
FPS = 60
MIN_GAP = 22                     # min cuts between reuse of the same still (carsearch parity)
# Varied cut cadence (NOT a metronome) — quick bursts mixed with long held frames. Used as RATIOS
# within each act window so the underlying photo/footage bed alternates fast montage with calm holds.
DUR_CYCLE = [1.7, 2.1, 5.6, 1.8, 3.0, 6.5, 2.0, 1.6, 4.2, 2.4, 5.2, 1.9]
GENERIC_PAT = r"scales|lady_justice|justice_statue|gavel|hourglass|balance|scales_of_justice"
# real DPT `depth` parallax must cover >= this share of IMAGE cuts (EP34 §2: >=42% of image-cut
# seconds; enforced by count here, which tracks seconds since durations are comparable).
DEPTH_FLOOR = 0.42
DEPTH_MAX_RATIO = 0.85
IMG_TREAT = ["depth", "scan", "depth", "duotone", "depth", "focus", "depth", "bleed"]
FLAT_TREATS = []
for _t in IMG_TREAT:
    if _t != "depth" and _t not in FLAT_TREATS:
        FLAT_TREATS.append(_t)
if not FLAT_TREATS:
    FLAT_TREATS = ["scan", "duotone", "focus", "bleed"]

# --- DESIGN §6 per-act allocation (name, narration section key, budget seconds, n_img, n_foot,
#     n_fig). Section keys map the design acts (HOOK/OP/幕1..幕5/ED) to the narration_index sections
#     (COLD_OPEN_TEASE / THESIS_AND_PROMISE / COLD_OPEN_STORY / MECHANISM / SCOPE_AND_HUMAN_COST /
#     TURN_AND_PAYOFF / RECKONING_AND_LIMITS / PAYOFF_AND_CTA). The order matches their time order.
ACT_PLAN = [
    ("HOOK", "COLD_OPEN_TEASE",       8,   2,  1, 0),
    ("OP",   "THESIS_AND_PROMISE",   17,   2,  2, 1),
    ("ACT1", "COLD_OPEN_STORY",      244,  42, 43, 8),
    ("ACT2", "MECHANISM",            221,  30, 34, 8),
    ("ACT3", "SCOPE_AND_HUMAN_COST", 223,  30, 33, 9),
    ("ACT4", "TURN_AND_PAYOFF",      242,  30, 38, 9),
    ("ACT5", "RECKONING_AND_LIMITS", 213,  20, 36, 8),
    ("ED",   "PAYOFF_AND_CTA",        36,   4,  1, 1),
]

# --- FIGURE TABLE (§1 figure table -> FigureBeats kinds), grouped by act. Each entry:
#     (kind, dur_seconds, props_dict, hero_mp4_basename_or_None). hero basename (without .mp4)
#     references remotion/public/rolin/hero_<name>.mp4 when the Blender render exists. Reuse/spare
#     instances (design §6: 27 unique + 17 reuse = 44) are appended deterministically below to hit
#     each act's n_fig. Only design-confirmed numbers are burned in.
FIG_TABLE = {
    "OP": [
        ("cashstack", 12, {"caption": "~$82,000"}, "cashstack"),                              # #1 (hero pending)
    ],
    "ACT1": [
        ("convergemap", 12, {}, "checkpointconverge"),                                          # #4 (hero EXISTS)
        ("xrayscan", 10, {"caption": "CARRY-ON X-RAY"}, None),                                   # #3
        ("thresholdmeter", 9, {}, None),                                                        # #5
        ("kinetic", 4, {"lines": ["NO DRUGS", "NO ARREST", "NO CHARGE"], "style": "emphasis"}, None),  # #6 NoChargeStamp
    ],
    "ACT2": [
        ("acttitle", 6, {"title": "THE MACHINE", "index": 1}, None),                            # #24 幕2頭
        ("kinetic", 8, {"lines": ["UNITED STATES", "v.", "THE CASH"], "style": "maskslide"}, None),  # #7 InRem (illustrative)
        ("burdenflip", 12, {}, "burdenflipscale"),                                              # #8 (hero pending)
        ("mechanism", 7, {"mechanism": "gears"}, None),                                         # #9 ProfitIncentiveFlow
        ("kinetic", 6, {"lines": ["FORFEITURE REVENUE", "KEPT BY THE AGENCY"], "style": "emphasis"}, None),  # #10 ForfeitureRevenueBar
    ],
    "ACT3": [
        ("acttitle", 6, {"title": "THE SCALE", "index": 2}, None),                              # #25 幕3頭
        ("pindropmap", 8, {"pins": [
            {"x": 0.30, "y": 0.40, "label": "PITTSBURGH"}, {"x": 0.22, "y": 0.34},
            {"x": 0.44, "y": 0.28}, {"x": 0.58, "y": 0.40}, {"x": 0.72, "y": 0.30},
            {"x": 0.34, "y": 0.60}, {"x": 0.66, "y": 0.62}, {"x": 0.50, "y": 0.50},
        ]}, None),                                                                              # #11 15 airports
        ("numberticker", 12, {"value": 209, "prefix": "$", "suffix": "M",
                              "label": "15 AIRPORTS - 2006-2015"}, "usforfeiture_209m"),        # #12 (hero EXISTS)
        # #13/#14: the $3.2B/~65,000 and $68.8B aggregates are grade-B estimates (IJ/DOJ-OIG,
        # flagged for verbatim recheck), so they must NOT be burned as authoritative on-screen
        # numbers (onscreen_text_verified allows only grade-A digits). Show the scale
        # QUALITATIVELY instead — no digits, still true under the grade-B sources — and drop the
        # usforfeiture_32b / usforfeiture_688b number heroes (they render the grade-B figures in 3D).
        ("kinetic", 12, {"lines": ["TENS OF THOUSANDS", "OF CASH SEIZURES", "NO CHARGES FILED"],
                        "style": "emphasis"}, None),                                            # #13 (was $3.2B/65k)
        ("kinetic", 12, {"lines": ["BILLIONS SEIZED", "OFTEN WITHOUT", "A SINGLE CHARGE"],
                        "style": "emphasis"}, None),                                            # #14 (was $68.8B)
        ("kinetic", 14, {"lines": ["THE COST OF WAITING", "DELAYED CARE", "REPAIRS UNDONE"],
                        "style": "emphasis"}, None),                                            # #15 HardshipStill (no fabricated quote)
    ],
    "ACT4": [
        ("acttitle", 6, {"title": "THE RETURN", "index": 3}, None),                             # #26 幕4頭
        ("lowerthird", 5, {"primary": "Brown v. TSA", "secondary": "W.D. Pa. - 2020"}, None),   # #16 CaseHeader
        ("kinetic", 12, {"lines": ["EXCEEDED AUTHORITY", "NO REASONABLE SUSPICION",
                                   "SEIZED WITHOUT CAUSE"], "style": "maskslide"}, None),        # #17 ThreeClaims
        ("casetimeline_c", 10, {"events": [
            {"year": "2020", "text": "Complaint filed"},
            {"year": "2020", "text": "Cash returned"}]}, None),                                 # #18 ReturnTimeline
        ("returnledger", 14, {"caption": "RETURNED IN FULL"}, "returnhands"),                   # #19 ReturnHands (hero pending)
        ("returnledger", 10, {}, None),                                                         # #27 ReturnLedgerMotion
    ],
    "ACT5": [
        ("acttitle", 6, {"title": "UNRESOLVED", "index": 4}, None),                             # 幕5頭
        # #20: the "$22M / 57 arrests" scorecard is grade-B (source/comparison unconfirmed) -> no
        # on-screen digits; keep the beat qualitatively (millions seized, almost no one charged).
        ("kinetic", 10, {"lines": ["MILLIONS SEIZED", "ALMOST NO ONE", "EVER CHARGED"], "style": "emphasis"}, None),  # #20 Program Scorecard
        ("signswap", 12, {"fromLabel": "AIRPORT CASH PROGRAM", "toLabel": "DHS - HSI - CBP"}, "signswap"),  # #21 (hero EXISTS)
        ("kinetic", 6, {"lines": ["CONSTITUTIONALITY", "UNRESOLVED"], "style": "emphasis"}, None),  # #22 SplitBar
        # #23: the ~$800K Texas seizure is grade-B (late-2025 reporting, unconfirmed) -> show the
        # recurrence beat without the digit; the point is "it keeps happening, no charge".
        ("kinetic", 10, {"lines": ["ANOTHER AIRPORT", "ANOTHER TRAVELER", "NO CHARGE"], "style": "emphasis"}, None),  # #23 DHSAirportRecur
    ],
    "ED": [
        ("kinetic", 6, {"lines": ["THEY BROKE NO LAW", "IT WAS GONE"], "style": "emphasis"}, None),  # payoff
    ],
}


# --------------------------------------------------------------------------- helpers
def _even_positions(m: int, k: int):
    """k evenly-spaced, distinct, increasing indices in range(m) (requires 0 <= k <= m)."""
    if k <= 0 or m <= 0:
        return []
    return [(x * m) // k for x in range(k)]


def parse_srt(path: Path):
    """Parse an SRT into [{start,end,text}] (carsearch parity)."""
    cues = []
    for b in re.split(r"\n\s*\n", path.read_text("utf-8").strip()):
        L = [x for x in b.splitlines() if x.strip()]
        if len(L) < 2:
            continue
        m = re.search(r"(\d\d):(\d\d):(\d\d),(\d\d\d)\s*-->\s*(\d\d):(\d\d):(\d\d),(\d\d\d)", L[1])
        if not m:
            continue
        g = list(map(int, m.groups()))
        s = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        e = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        txt = " ".join(L[2:]).strip()
        if txt:
            cues.append({"start": round(s, 3), "end": round(e, 3), "text": txt})
    return cues


def depth_map_path(pub: Path, src: str) -> Path:
    """DPT depth map path for a staged still, matching CaseFilm.tsx depthSrcOf
    (`<name>.<ext>` -> `<name>_depth.png`). `src` is the uri `<slug>/img/<name>.<ext>`."""
    p = pub.parent / src
    return p.with_name(re.sub(r"\.[^.]+$", "_depth.png", p.name))


def assign_image_treatments(img_cuts, target_ratio):
    """Deterministically assign a treatment per image cut so real DPT `depth` covers >= target_ratio
    of image cuts (>= DEPTH_FLOOR); the rest rotate through the flat looks. Pure function."""
    n = len(img_cuts)
    if n == 0:
        return []
    want = min(max(0, math.ceil(min(max(target_ratio, DEPTH_FLOOR), DEPTH_MAX_RATIO) * n)), n)
    is_depth = [False] * n
    for j in _even_positions(n, want):
        is_depth[j] = True
    treats, fi = [], 0
    for i in range(n):
        if is_depth[i]:
            treats.append("depth")
        else:
            treats.append(FLAT_TREATS[fi % len(FLAT_TREATS)])
            fi += 1
    return treats


def section_windows(chunks: list) -> dict:
    """{section_key -> (min_start, max_end)} from the narration chunks."""
    r: dict = {}
    for c in chunks:
        k = c.get("section", "")
        s = float(c["start"]); e = float(c["end"])
        if k in r:
            lo, hi = r[k]; r[k] = (min(lo, s), max(hi, e))
        else:
            r[k] = (s, e)
    return r


def resolve_act_windows(sec_win: dict | None):
    """Return [(name, a0, a1, n_img, n_foot, n_fig), ...] contiguous over [0, T].

    narration mode (sec_win given): a1 = the act's section max_end (a0 = previous a1) so the grid is
    seamless and every figure lands inside its own narration section. design mode (sec_win None):
    a1 = cumulative §6 budget."""
    acts = []
    a0 = 0.0
    for name, seckey, budget, n_img, n_foot, n_fig in ACT_PLAN:
        if sec_win is not None and seckey in sec_win:
            a1 = float(sec_win[seckey][1])
        else:
            a1 = a0 + float(budget)
        if a1 <= a0:                       # degenerate section — nudge forward by the budget
            a1 = a0 + float(budget)
        acts.append((name, round(a0, 3), round(a1, 3), n_img, n_foot, n_fig))
        a0 = a1
    return acts


def build_act_grid(a0, a1, n_img, n_foot, foot_seq, foot_ptr, pick_img, seed_base, idx0):
    """Fill [a0, a1] with (n_img + n_foot) continuous cuts (varied cadence). Footage at evenly-spaced
    slots, no-reuse from foot_seq; when the pool is exhausted the slot becomes an image cut. Returns
    (cuts, new_foot_ptr, next_idx)."""
    n = n_img + n_foot
    if n <= 0 or a1 <= a0:
        return [], foot_ptr, idx0
    ratios = [DUR_CYCLE[(idx0 + i) % len(DUR_CYCLE)] for i in range(n)]
    tot = sum(ratios); span = a1 - a0
    durs = [span * r / tot for r in ratios]
    avail = max(0, len(foot_seq) - foot_ptr)
    n_foot_eff = min(n_foot, avail)
    foot_pos = set(_even_positions(n, n_foot_eff))
    cuts = []; t = a0
    for k in range(n):
        gi = idx0 + k
        dur = round(a1 - t, 3) if k == n - 1 else round(durs[k], 3)
        if k in foot_pos and foot_ptr < len(foot_seq):
            src = foot_seq[foot_ptr]; foot_ptr += 1
            cuts.append({"start": round(t, 3), "dur": dur, "kind": "footage",
                         "src": src, "seed": f"{seed_base}-{gi}", "treatment": "footage"})
        else:
            src = pick_img(gi)
            cuts.append({"start": round(t, 3), "dur": dur, "kind": "img",
                         "src": src, "seed": f"{seed_base}-{gi}", "treatment": None})
        t += dur
    return cuts, foot_ptr, idx0 + n


def act_figures(act_name: str, n_fig: int):
    """The act's figure entries padded (deterministic cycle of its own uniques) to length n_fig."""
    base = FIG_TABLE.get(act_name, [])
    if not base or n_fig <= 0:
        return []
    out = list(base[:n_fig])
    i = 0
    while len(out) < n_fig:
        out.append(base[i % len(base)])
        i += 1
    return out


def place_figures(a0, a1, entries, pub: Path):
    """Place an act's figure entries evenly across [a0, a1] (no overlap), each with its designed
    duration. Returns (figures, hero_videos) where hero_videos records existing hero_<name>.mp4."""
    figures, heroes = [], []
    n = len(entries)
    if n == 0:
        return figures, heroes
    slot = (a1 - a0) / n
    for i, (kind, dur, props, hero) in enumerate(entries):
        s = a0 + i * slot + min(0.3, slot * 0.1)
        d = min(float(dur), max(0.5, slot - 0.5))
        e = min(s + d, a1)
        fig = {"start": round(s, 3), "end": round(e, 3), "kind": kind}
        fig.update(props)
        figures.append(fig)
        if hero:
            src = f"{pub.name}/hero_{hero}.mp4"
            heroes.append({"hero": hero, "src": src, "kind": kind,
                           "start": fig["start"], "end": fig["end"],
                           "exists": (pub / f"hero_{hero}.mp4").exists()})
    return figures, heroes


# --------------------------------------------------------------------------- main
def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Build EP34 rolin CaseFilm film_data (carsearch-shaped).")
    ap.add_argument("--ep", required=True)
    ap.add_argument("--hookline", required=True)
    ap.add_argument("--allow-missing-depth-maps", action="store_true",
                    help="downgrade the missing-depth-map hard error to a warning (staging phase).")
    args = ap.parse_args()
    ep = args.ep
    slug = re.sub(r"^PD-\d{4}-\d{3}-", "", ep)
    EPDIR = ROOT / "episodes" / ep
    IMG_SRC = EPDIR / "04_scenes" / "generated_images"
    SRT = EPDIR / "08_edit" / "captions.final.v001.srt"
    PUB = ROOT / "remotion" / "public" / slug
    FACT = PUB / "factory"
    (PUB / "img").mkdir(parents=True, exist_ok=True)
    FACT.mkdir(parents=True, exist_ok=True)

    print(f"[{ep}] building CaseFilm film_data (slug={slug}, fps={FPS})")

    # --- stage stills (flatten) from source if present, then enumerate the staged pool -----------
    if IMG_SRC.exists():
        for p in sorted(IMG_SRC.rglob("*.png")):
            if p.stat().st_size < 20000 or p.stem.endswith("_depth"):
                continue
            dst = PUB / "img" / p.name
            if not dst.exists() or dst.stat().st_mtime < p.stat().st_mtime:
                shutil.copy2(p, dst)
    imgs = [f"{slug}/img/{p.name}" for p in sorted((PUB / "img").glob("*.png"))
            if not p.stem.endswith("_depth") and p.stat().st_size >= 20000]
    if not imgs:
        print(f"[{ep}] ABORT: no staged stills in {PUB/'img'}", file=sys.stderr)
        return 2
    print(f"[{ep}] stills: {len(imgs)} staged")

    # --- narration.mp3: prefer the SSD master, else keep an already-staged copy ------------------
    narration_uri = f"{slug}/narration.mp3"
    try:
        media = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))
                     ["roots"]["media"]["path"])
        master = media / "episodes" / ep / "06_voice" / "master" / "vc_master_v001.mp3"
    except (OSError, ValueError, KeyError):
        master = None
    if master and master.exists():
        shutil.copy2(master, PUB / "narration.mp3")
        print(f"[{ep}] narration.mp3 <- master {master}")
    elif (PUB / "narration.mp3").exists():
        print(f"[{ep}] narration.mp3 = already-staged copy (master not found)")
    else:
        print(f"[{ep}] WARN no narration.mp3 (no master, none staged); the Body audio will be silent.")

    # --- TIMING SOURCE: narration_index.v00N if present, else DESIGN §6 budget (preview) ---------
    idx_path = None
    for rev in ("v002", "v001"):
        cand = EPDIR / "06_audio" / f"narration_index.{rev}.json"
        if cand.exists():
            idx_path = cand
            break
    sec_win = None
    timing_source = None
    if idx_path is not None:
        idx = json.loads(idx_path.read_text("utf-8"))
        chunks = idx.get("chunks") or []
        if chunks:
            sec_win = section_windows(chunks)
            T = max(float(c["end"]) for c in chunks)
            timing_source = f"NARRATION ({idx_path.name}, {len(chunks)} chunks, {len(sec_win)} sections)"
    if sec_win is None:
        T = float(sum(a[2] for a in ACT_PLAN))                    # §6 budget total (~1204s)
        timing_source = "DESIGN §6 per-act budget (PREVIEW — narration_index absent)"
        print(f"[{ep}] WARN narration_index.v00N.json not found — using design-timed PREVIEW budget.")
    print(f"[{ep}] TIMING SOURCE = {timing_source}; body T = {T:.3f}s")

    # --- captions -------------------------------------------------------------------------------
    if SRT.exists():
        cues = parse_srt(SRT)
        print(f"[{ep}] captions: {len(cues)} cues <- {SRT.name}")
    else:
        cues = []
        print(f"[{ep}] WARN no captions ({SRT.name} absent) — emitting empty captions (preview).")

    # --- footage pool: drop generics, no-reuse (empty in current EP34 state -> WARN) -------------
    foot_all = [f"{slug}/factory/{p.name}" for p in sorted(FACT.glob("*.mp4"))]
    foot_generic = [s for s in foot_all if re.search(GENERIC_PAT, s, re.I)]
    foot_pool = [s for s in foot_all if not re.search(GENERIC_PAT, s, re.I)]
    if not foot_pool:
        print(f"[{ep}] WARN no factory clips staged in {FACT} — footage slots will degrade to image "
              f"cuts. Stage FRESH-ONLY themed clips (avoids the arc_nonrepeat cross-episode reuse "
              f"gate) e.g.:  python scripts/select_factory_assets.py --theme <finance_money|"
              f"legal_court|crime_police|urban_night> --kind video --exclude-used --ep {ep}  then "
              f"copy the chosen AF-* files into remotion/public/{slug}/factory and re-run.")

    # --- resolve act windows, then build cut grid + figures per act -----------------------------
    acts = resolve_act_windows(sec_win)
    img_used, img_last = {}, {}

    def pick_img(i):
        elig = [s for s in imgs if i - img_last.get(s, -999) > MIN_GAP] or imgs
        s = sorted(elig, key=lambda s: (img_used.get(s, 0), img_last.get(s, -999)))[0]
        img_used[s] = img_used.get(s, 0) + 1
        img_last[s] = i
        return s

    cuts, figures, hero_videos = [], [], []
    foot_ptr, idx = 0, 0
    for name, a0, a1, n_img, n_foot, n_fig in acts:
        ac, foot_ptr, idx = build_act_grid(a0, a1, n_img, n_foot, foot_pool, foot_ptr,
                                           pick_img, slug, idx)
        cuts.extend(ac)
        figs, heroes = place_figures(a0, a1, act_figures(name, n_fig), PUB)
        figures.extend(figs)
        hero_videos.extend(heroes)
    cuts.sort(key=lambda c: c["start"])
    figures.sort(key=lambda f: f["start"])

    # --- image treatment assignment (>= DEPTH_FLOOR real depth) ----------------------------------
    img_cuts = [c for c in cuts if c["kind"] == "img"]
    for c, tr in zip(img_cuts, assign_image_treatments(img_cuts, DEPTH_FLOOR)):
        c["treatment"] = tr
    n_img = len(img_cuts)
    n_depth = sum(1 for c in img_cuts if c["treatment"] == "depth")
    depth_share = (n_depth / n_img) if n_img else 0.0
    print(f"[{ep}] image treatments: depth={n_depth}/{n_img} ({depth_share*100:.1f}%) "
          f"floor={DEPTH_FLOOR*100:.0f}% flats={FLAT_TREATS}")
    if n_img and depth_share < DEPTH_FLOOR - 1e-9:
        raise SystemExit(f"[{ep}] ABORT: depth share {depth_share*100:.1f}% < floor {DEPTH_FLOOR*100:.0f}%")

    # --- depth-map existence gate (never silently downgrade a depth cut to a flat look) ----------
    missing = [(c["src"], depth_map_path(PUB, c["src"])) for c in img_cuts
               if c["treatment"] == "depth" and not depth_map_path(PUB, c["src"]).exists()]
    if missing:
        print(f"[{ep}] !! DEPTH MAP MISSING for {len(missing)} of {n_depth} depth cut(s):", file=sys.stderr)
        for s, dm in missing[:12]:
            print(f"    {s} -> expected {dm}", file=sys.stderr)
        if not args.allow_missing_depth_maps:
            raise SystemExit(f"[{ep}] ABORT: {len(missing)} depth cut(s) lack <name>_depth.png. Run "
                             f"tools/depth/gen_depth.py remotion/public/{slug} then re-run, or pass "
                             f"--allow-missing-depth-maps.")
        print(f"[{ep}] WARN proceeding with --allow-missing-depth-maps (depth cuts render flat).",
              file=sys.stderr)

    # --- hook montage (first 6 stills, 1.34s each = 8.04s, design HOOK 8s) -----------------------
    hook, ht = [], 0.0
    for s in imgs[:6]:
        hook.append({"start": round(ht, 3), "dur": 1.34, "kind": "img", "src": s, "seed": f"hook-{ht}"})
        ht += 1.34

    data = {
        "episode_id": ep, "fps": FPS, "narration": narration_uri, "narrationSeconds": round(T, 3),
        "hookSeconds": round(ht, 3), "hookLine": args.hookline, "hook": hook, "cuts": cuts,
        "captions": cues, "graphics": [], "figures": figures,
        # informational (ignored by CaseFilm): existing Blender hero renders + the proposed minimal
        # integration. See report — CaseFilm has no clean hero-video cut mechanism, so these are NOT
        # rendered yet; a `footage` cut of `src` (or a tiny hero-cut type) would composite them.
        "heroVideos": hero_videos,
    }
    (PUB / "film_data.v001.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    (ROOT / "remotion" / "src" / "data" / f"{slug}_film.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), "utf-8")

    # --- summary --------------------------------------------------------------------------------
    import collections
    ni = sum(1 for c in cuts if c["kind"] == "img")
    nf = sum(1 for c in cuts if c["kind"] == "footage")
    fig_secs = sum(f["end"] - f["start"] for f in figures)
    fig_pct = fig_secs / T * 100 if T else 0.0
    fcnt = collections.Counter(c["src"] for c in cuts if c["kind"] == "footage")
    foot_max_reuse = max(fcnt.values()) if fcnt else 0
    kinds = collections.Counter(f["kind"] for f in figures)
    heroes_exist = sum(1 for h in hero_videos if h["exists"])
    print(f"[{ep}] cuts={len(cuts)} (img {ni} / footage {nf})  figures={len(figures)}  "
          f"stills={len(imgs)}  factory_pool={len(foot_pool)}(+{len(foot_generic)} generic dropped)")
    print(f"[{ep}] DEPTH: {n_depth}/{n_img} img cuts = {depth_share*100:.1f}% (floor {DEPTH_FLOOR*100:.0f}%)")
    print(f"[{ep}] FIGURES: {len(figures)} beats, {fig_secs:.0f}s = {fig_pct:.1f}% of body; kinds="
          + " ".join(f"{k}:{v}" for k, v in sorted(kinds.items())))
    print(f"[{ep}] FOOTAGE no-reuse: {nf} cuts, {len(fcnt)} distinct, max_reuse={foot_max_reuse}"
          + ("" if nf else " (pool empty -> all image cuts)"))
    print(f"[{ep}] HERO videos: {len(hero_videos)} figure(s) map to hero_*.mp4 "
          f"({heroes_exist} present, {len(hero_videos)-heroes_exist} pending):")
    for h in hero_videos:
        print(f"    {'OK ' if h['exists'] else 'PEND'} {h['src']}  <- {h['kind']} @ {h['start']:.0f}-{h['end']:.0f}s")
    print(f"wrote remotion/public/{slug}/film_data.v001.json + remotion/src/data/{slug}_film.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
