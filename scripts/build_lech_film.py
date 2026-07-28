#!/usr/bin/env python3
r"""Build remotion/src/data/lech_film.json (EP40 PD-2026-040-lech) from the re-mapped
asset ledger + the measured narration index.

Adapted from scripts/build_frazier_film.py (do NOT touch frazier). Differences for lech:

  * The lech asset set is SDXL stills only (no factory / motion). Each scene has 3
    near-identical variants; we PICK BEST = one per scene (min variant / gap-fill base)
    so check_asset_reuse is not defeated by 3 look-alikes.
  * cuts[] are laid out in act order and tiled across the measured act windows, with a
    global per-asset cap of 2 uses and a >=0.70 first-use share (still cap).
  * figures[] (the premium MG beats) are DESIGNED from the script's on-screen CARDs and
    the act structure — only ledger numbers/verified facts, only FigureBeats.tsx kinds,
    never attributing a merits ruling to the Supreme Court.
  * captions[] are the measured narration chunks verbatim (real audio timing, real text)
    — no mechanical 7-word grid (that was the old-SRT defect).

Inputs are read directly; the intermediate manifest is also emitted for provenance.
No paid calls. Does NOT render. Copies the selected stills H: -> remotion/public/lech/img.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-040-lech"
SLUG = "lech"
FPS = 30

ASSET_MAP = ROOT / "episodes" / "_planning" / "EP40_lech_asset_map.v001.json"
NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
H_SRC = Path("H:/pd-media/assets/ai/lech")
PUB_DIR = ROOT / "remotion" / "public" / "lech" / "img"
OUT_FILM = ROOT / "remotion" / "src" / "data" / "lech_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "lech" / "film_data.v001.json"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"

# FigureBeats.tsx kinds actually implemented (generic tier only — no case-specific bespoke).
VALID_FIGURE_KINDS = {
    "stat", "timeline", "bar", "numberticker", "quote", "kinetic", "acttitle",
    "lowerthird", "highlightring", "spotlight", "dochighlight", "routemap",
    "pindropmap", "regionmap", "compbars", "mechanism",
}
TREATMENTS = ["scan", "duotone", "focus", "bleed"]


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------------------
# 1. best-pick per scene from the asset ledger
# ------------------------------------------------------------------------------------------------

def parse_scene(fname: str):
    m = re.match(r"(S\d+)(?:_(\d+))?\.png$", fname)
    if not m:
        return None, None
    return m.group(1), (int(m.group(2)) if m.group(2) else 1)


def best_picks(asset_map: dict) -> dict[str, dict]:
    """scene_code -> chosen entry (min variant; gap-fill base counts as variant 1)."""
    by_scene: dict[str, list[dict]] = {}
    for e in asset_map.get("usable", []):
        scene, var = parse_scene(e["file"])
        if scene is None:
            continue
        rec = dict(e, _scene=scene, _var=var)
        by_scene.setdefault(scene, []).append(rec)
    picks = {}
    for scene, entries in by_scene.items():
        picks[scene] = sorted(entries, key=lambda r: r["_var"])[0]
    return picks


def scene_num(scene: str) -> int:
    return int(scene[1:])


# ------------------------------------------------------------------------------------------------
# 2. copy selected stills to public + build manifest
# ------------------------------------------------------------------------------------------------

def public_path_for(fname: str) -> str:
    return f"lech/img/{fname}"


def copy_and_manifest(picks: dict[str, dict]) -> tuple[dict[str, str], list[dict]]:
    PUB_DIR.mkdir(parents=True, exist_ok=True)
    src_by_scene: dict[str, str] = {}
    manifest_assets = []
    for i, scene in enumerate(sorted(picks, key=scene_num), start=1):
        e = picks[scene]
        fname = e["file"]
        src = H_SRC / fname
        if not src.is_file():
            raise SystemExit(f"MISSING source still on H: {src}")
        dst = PUB_DIR / fname
        if (not dst.is_file()) or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
        pub = public_path_for(fname)
        src_by_scene[scene] = pub
        manifest_assets.append({
            "asset_id": f"ST-040-{i:03d}",
            "kind": "still",
            "scene_code": scene,
            "assign": e.get("assign"),
            "variant_picked": e["_var"],
            "public_path": pub,
            "abs_path": str(dst).replace("\\", "/"),
            "source_path": str(src).replace("\\", "/"),
            "qc": {"pass": True, "notes": "SDXL still; best-of-3 pick; visually verified in asset_map"},
        })
    return src_by_scene, manifest_assets


# ------------------------------------------------------------------------------------------------
# 3. captions from measured narration chunks (verbatim, real timing)
# ------------------------------------------------------------------------------------------------

def build_captions(narr: dict) -> tuple[list[dict], float]:
    cues = []
    for c in narr["chunks"]:
        text = str(c.get("text", "")).strip()
        if not text:
            continue
        cues.append({"start": round(float(c["start"]), 3),
                     "end": round(float(c["end"]), 3),
                     "text": text})
    total = max(c["end"] for c in cues)
    return cues, float(total)


def section_windows(narr: dict) -> dict[str, tuple[float, float]]:
    """First-chunk-start of each script section, used to bound the act windows."""
    starts: dict[str, float] = {}
    for c in narr["chunks"]:
        sec = c["section"]
        if sec not in starts:
            starts[sec] = float(c["start"])
    return starts


def srt_ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(cues: list[dict]) -> None:
    lines = []
    for i, c in enumerate(cues, start=1):
        lines.append(str(i))
        lines.append(f"{srt_ts(c['start'])} --> {srt_ts(c['end'])}")
        lines.append(c["text"])
        lines.append("")
    SRT.parent.mkdir(parents=True, exist_ok=True)
    SRT.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------------------------------------------
# 4. cuts[] — tile the act windows with the still pool (cap 2, first-use >= 0.70)
# ------------------------------------------------------------------------------------------------

# Ordered scene pools per act. Every scene appears once as a FIRST use somewhere here.
INTRO_SCENES = ["S72", "S05", "S09", "S02", "S23", "S01"]
ACT1_SCENES = ["S15", "S71", "S03", "S04", "S06", "S07", "S08", "S11", "S12", "S13",
               "S28", "S25", "S26", "S24", "S29", "S33", "S32", "S30", "S31", "S21",
               "S35", "S37", "S38", "S43"]
ACT2_SCENES = ["S36", "S39", "S40", "S41", "S42", "S44", "S45", "S46", "S47", "S49",
               "S50", "S51", "S52", "S56", "S57", "S61"]
ACT3_DED = ["S55", "S62", "S70"]
ENDING_DED = ["S48", "S63", "S64"]

# thematically-appropriate reuse pools for the still-starved legal acts (second uses only).
# These must NOT drain the capacity a later act needs for its own FIRST uses:
#  - ACT3 reuse stops at 5 picks (S70/S55/S62/S56/S57) and never touches S63/S64/S48 (ENDING).
#  - ACT4 reuse draws only from ACT1/ACT2 aftermath/assault stills (each has 1 free slot),
#    excluding anything already at cap after ACT3 and excluding ENDING's dedicated stills.
#  - ENDING reuse leads with its own now-once-used S63/S64 (1 free slot) before the capped rest.
ACT3_REUSE = ["S70", "S55", "S62", "S56", "S57", "S49", "S44", "S43", "S39", "S61"]
ACT4_REUSE = ["S44", "S43", "S39", "S40", "S41", "S46", "S45", "S51", "S49", "S50",
              "S52", "S47", "S38", "S28", "S61", "S30", "S31", "S21", "S42", "S35"]
ENDING_REUSE = ["S63", "S64", "S44", "S39", "S43", "S62"]

DUR_PATTERN = [1.0, 1.18, 0.9, 1.06, 0.92, 1.12, 0.86, 1.1]


def allocate(dedicated, reuse, n, use_count, cap=2):
    """Pick n scene codes: dedicated first (first uses), then reuse pool (<= cap total)."""
    picks = []
    ded_i = 0
    reuse_i = 0
    for _ in range(n):
        chosen = None
        while ded_i < len(dedicated):
            a = dedicated[ded_i]; ded_i += 1
            if use_count.get(a, 0) < cap:
                chosen = a; break
        if chosen is None:
            for _try in range(len(reuse) * 3 + 1):
                a = reuse[reuse_i % len(reuse)]; reuse_i += 1
                if use_count.get(a, 0) < cap:
                    chosen = a; break
        if chosen is None:
            raise SystemExit("allocate: ran out of reuse capacity")
        use_count[chosen] = use_count.get(chosen, 0) + 1
        picks.append(chosen)
    return picks


def tile_window(scenes, start, end, first_idx, treat_i0):
    """Distribute scenes across [start,end) with varied durations that sum exactly."""
    n = len(scenes)
    weights = [DUR_PATTERN[i % len(DUR_PATTERN)] for i in range(n)]
    total_w = sum(weights)
    span = end - start
    cuts = []
    t = start
    for i, (scene, w) in enumerate(zip(scenes, weights)):
        dur = span * w / total_w
        if i == n - 1:
            dur = end - t  # absorb rounding into the last cut
        cuts.append({"scene": scene, "start": round(t, 3), "dur": round(dur, 3),
                     "treat": TREATMENTS[(treat_i0 + i) % len(TREATMENTS)]})
        t += dur
    return cuts


def build_cuts(src_by_scene, windows, total):
    use_count: dict[str, int] = {}
    plan = [
        ("INTRO", INTRO_SCENES, [], 6, 0.0, windows["ACT_1"]),
        ("ACT1", ACT1_SCENES, ACT1_SCENES, 24, windows["ACT_1"], windows["ACT_2"]),
        ("ACT2", ACT2_SCENES, ACT2_SCENES, 17, windows["ACT_2"], windows["ACT_3"]),
        ("ACT3", ACT3_DED, ACT3_REUSE, 8, windows["ACT_3"], windows["ACT_4"]),
        ("ACT4", [], ACT4_REUSE, 11, windows["ACT_4"], windows["ENDING"]),
        ("ENDING", ENDING_DED, ENDING_REUSE, 5, windows["ENDING"], total),
    ]
    cuts = []
    treat_i = 0
    for name, ded, reuse, n, wstart, wend in plan:
        picks = allocate(ded, reuse, n, use_count)
        tiled = tile_window(picks, wstart, wend, len(cuts), treat_i)
        treat_i += n
        for c in tiled:
            idx = len(cuts)
            cuts.append({
                "id": f"cut-{idx:03d}",
                "start": c["start"],
                "dur": c["dur"],
                "kind": "img",
                "src": src_by_scene[c["scene"]],
                "treatment": c["treat"],
                "seed": f"lech-{idx:03d}",
                "scene_code": c["scene"],
                "act": name,
            })
    return cuts, use_count


# ------------------------------------------------------------------------------------------------
# 5. hook[]
# ------------------------------------------------------------------------------------------------

def build_hook(src_by_scene):
    seq = ["S72", "S05", "S09", "S02"]
    hook = []
    t = 0.0
    d = 2.0
    for i, s in enumerate(seq):
        hook.append({"start": round(t, 3), "dur": d, "kind": "img",
                     "src": src_by_scene[s], "seed": f"hook-{i}"})
        t += d
    return hook


# ------------------------------------------------------------------------------------------------
# 6. figures[] — designed premium MG beats (ledger-only, valid kinds, no SCOTUS merits)
# ------------------------------------------------------------------------------------------------

def K(lines, style="maskslide", emph=None):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def NUM(value, label, suffix=None, prefix=None):
    d = {"kind": "numberticker", "value": value, "label": label}
    if suffix:
        d["suffix"] = suffix
    if prefix:
        d["prefix"] = prefix
    return d


# (anchor_start_seconds, payload).  DUR is applied then clamped so none overlap.
FIGURE_ANCHORS = [
    # INTRO / OPENING
    (11.9, NUM(19, "THE HOUSE HELD", suffix=" HOURS")),
    (18.6, K(["ELEVEN YEARS", "LATER"], "emphasis", ["ELEVEN"])),
    (28.6, {"kind": "mechanism", "mechanism": "closingdoor"}),
    (33.7, K(["TWO DOORS", "ONE PAYS  ·  ONE DOESN'T"], "maskslide", ["DOORS"])),
    # ACT 1
    (41.2, {"kind": "acttitle", "title": "4219 SOUTH ALTON STREET", "kicker": "ACT ONE", "index": 1}),
    (61.3, {"kind": "lowerthird", "primary": "ILLUSTRATIVE RECONSTRUCTION",
            "secondary": "AI-assisted visualization — not actual footage"}),
    (96.1, K(["HIGH-RISK", "BARRICADE"], "emphasis", ["BARRICADE"])),
    (101.3, NUM(5, "NEGOTIATION", suffix=" HOURS")),
    (115.3, K(["THE RECORD", "RUNS A FEW SENTENCES"], "maskslide")),
    (124.1, {"kind": "mechanism", "mechanism": "gears"}),
    (143.2, NUM(19, "SIEGE ENDS", suffix=" HOURS")),
    (156.7, K(["NOBODY DID", "THE WRONG THING"], "emphasis", ["NOBODY"])),
    (167.3, K(["WHO PAYS?"], "wordpop", ["PAYS"])),
    # ACT 2
    (173.2, {"kind": "acttitle", "title": "WHAT IT COSTS TO BE THE ADDRESS", "kicker": "ACT TWO", "index": 2}),
    (178.4, NUM(5000, "OFFERED — TEMPORARY LIVING", prefix="$")),
    (199.6, {"kind": "dochighlight", "rects": [{"x": 0.16, "y": 0.40, "w": 0.68, "h": 0.10}], "mode": "redact"}),
    (223.1, K(["INTENTIONAL ACTS BY", "GOVERNMENT OFFICIALS", "EXCLUDED"], "emphasis", ["EXCLUDED"])),
    (242.0, K(["ASBESTOS"], "wordpop", ["ASBESTOS"])),
    (263.4, NUM(250000, "BORROWED TO REBUILD", prefix="$")),
    (268.7, NUM(5, "RETIREMENT DELAYED", suffix=" YEARS")),
    (294.4, K(["THE CONSTITUTION HAS", "A SENTENCE FOR THIS"], "maskslide")),
    (300.9, {"kind": "quote",
             "quote": "…nor shall private property be taken for public use, without just compensation.",
             "attribution": "Fifth Amendment"}),
    (306.0, NUM(14, "FIFTH AMENDMENT", suffix=" WORDS")),
    # ACT 3
    (313.4, {"kind": "acttitle", "title": "POLICE POWER", "kicker": "ACT THREE", "index": 3}),
    (321.1, {"kind": "mechanism", "mechanism": "faultsplit"}),
    (333.4, K(["POLICE POWER", "NOT EMINENT DOMAIN"], "emphasis", ["POLICE", "EMINENT"])),
    (356.4, K(["THE SAME HOUSE", "THE SAME RUBBLE"], "maskslide")),
    (364.3, {"kind": "timeline", "events": [
        {"year": "2015", "text": "SIEGE"}, {"year": "2018", "text": "DISTRICT COURT"},
        {"year": "2019", "text": "TENTH CIRCUIT"}, {"year": "2020", "text": "CERT DENIED"}]}),
    (374.9, {"kind": "dochighlight", "rects": [{"x": 0.18, "y": 0.30, "w": 0.64, "h": 0.08}], "mode": "box"}),
    (380.6, K(["NOT BINDING", "PRECEDENT"], "emphasis", ["NOT"])),
    (393.7, {"kind": "quote",
             "quote": "As unfair as it may seem, the Takings Clause does not entitle all aggrieved owners to recompense.",
             "attribution": "Tenth Circuit, 2019"}),
    (404.9, K(["CONSIDERABLE", "APPEAL"], "emphasis", ["CONSIDERABLE"])),
    (413.3, {"kind": "quote",
             "quote": "The innocence of the property owner does not factor into the determination.",
             "attribution": "Tenth Circuit, 2019"}),
    (435.4, K(["CERT DENIED", "JUNE 29, 2020"], "maskslide", ["DENIED"])),
    # ACT 4
    (444.2, {"kind": "acttitle", "title": "THE ADDRESS IS THE ONLY QUALIFICATION", "kicker": "ACT FOUR", "index": 4}),
    (450.3, {"kind": "pindropmap", "pins": [
        {"x": 0.34, "y": 0.45, "label": "CO 2015"}, {"x": 0.62, "y": 0.40, "label": "IN 2022"},
        {"x": 0.50, "y": 0.68, "label": "TX 2020"}, {"x": 0.66, "y": 0.52, "label": "TN 2022"},
        {"x": 0.12, "y": 0.52, "label": "CA 2022"}, {"x": 0.20, "y": 0.46, "label": "NV 2025"}]}),
    (463.7, NUM(30, "TEAR GAS — INDIANA", suffix=" CANISTERS")),
    (469.8, NUM(16000, "HADLEY — INDIANA", prefix="$")),
    (499.2, NUM(60000, "BAKER — TEXAS (JURY)", prefix="$")),
    (528.9, NUM(35, "SLAYBAUGH — TENNESSEE", suffix=" CANISTERS")),
    (535.9, NUM(70000, "TENNESSEE DAMAGE", prefix="$")),
    (548.6, K(["CARLOS PENA", "GETS NOTHING"], "emphasis", ["NOTHING"])),
    (575.9, NUM(30000, "LAS VEGAS — NEVADA", prefix="$")),
    (584.2, K(["SAME EMERGENCY", "DIFFERENT ANSWER"], "maskslide", ["DIFFERENT"])),
    (597.4, K(["NOT THE CONSTITUTION —", "WHICH CITY YOU LIVE IN"], "emphasis", ["CITY"])),
    (634.1, K(["A SPLIT AMONG", "THE CIRCUITS"], "maskslide", ["SPLIT"])),
    (649.4, K(["FURTHER", "PERCOLATION"], "emphasis", ["PERCOLATION"])),
    # ENDING
    (662.4, K(["MAY 2026"], "wordpop")),
    (675.4, {"kind": "timeline", "events": [
        {"year": "APR 6", "text": "FILED 2026"}, {"year": "SEP 28", "text": "CONFERENCE"}]}),
    (708.2, K(["SOME PEOPLE", "ALONE"], "emphasis", ["ALONE"])),
    (715.5, {"kind": "quote",
             "quote": "…forcing some people alone to bear public burdens which, in all fairness and justice, should be borne by the public as a whole.",
             "attribution": "Armstrong v. United States, 1960"}),
    (726.9, K(["THE ANSWER", "IS THE ADDRESS"], "emphasis", ["ADDRESS"])),
]

FIG_DUR = 4.9
FIG_MIN_DUR = 3.0
FIG_GAP = 0.4


def build_figures(total):
    anchors = sorted(FIGURE_ANCHORS, key=lambda x: x[0])
    figs = []
    for i, (start, payload) in enumerate(anchors):
        end = start + FIG_DUR
        if i + 1 < len(anchors):
            end = min(end, anchors[i + 1][0] - FIG_GAP)
        end = min(end, total - 0.5)
        if end - start < FIG_MIN_DUR:
            raise SystemExit(f"figure at {start} clamped below min dur ({end-start:.2f}s) — respace anchors")
        kind = payload["kind"]
        if kind not in VALID_FIGURE_KINDS:
            raise SystemExit(f"invalid figure kind '{kind}' not in FigureBeats.tsx")
        figs.append({"start": round(start, 3), "end": round(end, 3), **payload})
    # overlap assertion
    for a, b in zip(figs, figs[1:]):
        if b["start"] < a["end"] - 1e-6:
            raise SystemExit(f"figure overlap: {a['end']} > {b['start']}")
    return figs


# ------------------------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------------------------

def union_seconds(intervals):
    ivs = sorted(intervals)
    tot = 0.0
    cs = ce = None
    for a, b in ivs:
        if cs is None:
            cs, ce = a, b
        elif a <= ce:
            ce = max(ce, b)
        else:
            tot += ce - cs
            cs, ce = a, b
    if cs is not None:
        tot += ce - cs
    return tot


def main() -> int:
    asset_map = load_json(ASSET_MAP)
    narr = load_json(NARR)

    picks = best_picks(asset_map)
    src_by_scene, manifest_assets = copy_and_manifest(picks)

    captions, total = build_captions(narr)
    windows = section_windows(narr)
    write_srt(captions)

    cuts, use_count = build_cuts(src_by_scene, windows, total)
    hook = build_hook(src_by_scene)
    figures = build_figures(total)

    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": f"{SLUG}/narration.mp3",
        "narrationSeconds": round(total, 3),
        "hookSeconds": round(sum(h["dur"] for h in hook), 3),
        "hookLine": "The nine-year-old walked out of the house first.",
        "hook": hook,
        "cuts": cuts,
        "captions": captions,
        "graphics": [],
        "figures": figures,
    }

    OUT_FILM.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILM.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")
    PUB_FILM.parent.mkdir(parents=True, exist_ok=True)
    PUB_FILM.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")

    manifest = {
        "episode_id": EP,
        "manifest_version": "v001",
        "producer": "scripts/build_lech_film.py",
        "source_asset_map": "episodes/_planning/EP40_lech_asset_map.v001.json",
        "kind_policy": "SDXL stills only; best-of-3 pick per scene",
        "counts": {"still": len(manifest_assets), "distinct_scenes": len(manifest_assets)},
        "caps": {"still": 2, "factory": 1, "motion": 2},
        "assets": manifest_assets,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- report ----
    from collections import Counter
    srcs = [c["src"] for c in cuts]
    uses = Counter(srcs)
    distinct = len(uses)
    first_share = distinct / len(srcs)
    body_min = total / 60.0
    density = len(figures) / body_min
    cover = union_seconds([(f["start"], f["end"]) for f in figures]) / total
    variety_forms = set()
    for f in figures:
        variety_forms.add("fig:" + f["kind"])
    over_cap = {s: n for s, n in uses.items() if n > 2}

    report = {
        "narrationSeconds": round(total, 3),
        "cuts": len(cuts),
        "distinct_cut_assets": distinct,
        "first_use_share": round(first_share, 4),
        "over_cap_assets": over_cap,
        "captions": len(captions),
        "figures": len(figures),
        "figure_density_per_min": round(density, 2),
        "figure_coverage": round(cover, 3),
        "figure_variety": len(variety_forms),
        "figure_kinds": sorted({f["kind"] for f in figures}),
        "manifest_assets": len(manifest_assets),
        "public_stills_exist": all((ROOT / "remotion" / "public" / c["src"]).is_file() for c in cuts),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
