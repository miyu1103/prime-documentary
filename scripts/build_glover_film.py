#!/usr/bin/env python
"""Build remotion/src/data/glover_film.json for EP48 from real manifest assets."""
from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-048-glover"
SLUG = "glover"
FPS = 30
DEFAULT_ASSETS = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
DEFAULT_NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
DEFAULT_OUT = ROOT / "remotion" / "src" / "data" / "glover_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "glover" / "film_data.v001.json"
BUILD_MANIFEST = ROOT / "episodes" / EP / "04_scenes" / "glover_build_manifest.v001.json"
BEATSHEET = ROOT / "episodes" / EP / "04_scenes" / "glover_beatsheet.v001.json"
PREMIUM_BEATSHEET = ROOT / "episodes" / EP / "04_scenes" / "premium_beatsheet.v001.json"
DEFAULT_SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"
SECTION_TARGETS = {
    "HOOK": (6, 2, 5),
    "OP": (3, 3, 10),
    "ACT_1": (12, 8, 16),
    "ACT_2": (23, 6, 18),
    "ACT_3": (36, 8, 28),
    "ENDING": (12, 5, 24),
}
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ENDING"]
VALID_KINDS = {
    "numberticker", "stat", "votetally", "timeline", "quote", "kinetic", "lowerthird",
    "acttitle", "compbars", "bar", "mechanism", "regionmap", "pindropmap", "routemap",
    "statemap", "brightline", "probablecause",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def srt_ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_captions(narr: dict) -> tuple[list[dict], float]:
    cues = []
    chunks = narr.get("chunks") or narr.get("lines") or []
    for c in chunks:
        text = str(c.get("text") or c.get("spoken_text") or "").strip()
        if text:
            cues.append({"start": round(float(c["start"]), 3), "end": round(float(c["end"]), 3), "text": text})
    return cues, max(c["end"] for c in cues)


def write_srt(cues: list[dict], out: Path) -> None:
    lines = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{srt_ts(c['start'])} --> {srt_ts(c['end'])}", c["text"], ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def section_windows(narr: dict, total: float) -> dict[str, tuple[float, float]]:
    starts = {}
    ends = {}
    chunks = narr.get("chunks") or narr.get("lines") or []
    for c in chunks:
        sec = c["section"]
        starts.setdefault(sec, float(c["start"]))
        ends[sec] = max(float(c["end"]), ends.get(sec, 0.0))
    windows = {}
    for i, sec in enumerate(SECTION_ORDER):
        if sec not in starts:
            continue
        nxt = next((s for s in SECTION_ORDER[i + 1:] if s in starts), None)
        windows[sec] = (starts[sec], starts[nxt] if nxt else total)
    return windows


def public_items(manifest: dict, key: str, role: str | None = None) -> list[str]:
    items = manifest.get(key) or []
    if role:
        items = [x for x in items if x.get("role") == role]
    out = [str(x["public_path"]) for x in items if x.get("public_path")]
    if len(out) != len(set(out)):
        raise SystemExit(f"duplicate public_path in {key}")
    return out


def take(q: deque[str], n: int, label: str) -> list[str]:
    if len(q) < n:
        raise SystemExit(f"not enough {label}: need {n}, have {len(q)}")
    return [q.popleft() for _ in range(n)]


def repeated(pool: list[str], n: int, cap: int, label: str) -> list[str]:
    if not pool:
        raise SystemExit(f"not enough {label}: need {n}, have 0")
    out = []
    uses: Counter[str] = Counter()
    i = 0
    guard = 0
    while len(out) < n and guard < n * 10 + 100:
        item = pool[i % len(pool)]
        if uses[item] < cap:
            uses[item] += 1
            out.append(item)
        i += 1
        guard += 1
    if len(out) < n:
        raise SystemExit(f"unable to allocate {n} {label} assets with cap {cap}")
    return out


def make_cuts(windows: dict[str, tuple[float, float]], manifest: dict) -> list[dict]:
    stills = public_items(manifest, "stills", "body")
    factory_q = deque(public_items(manifest, "factory"))
    motion_pool = public_items(manifest, "motion")
    still_need = sum(ns for nf, nm, ns in SECTION_TARGETS.values())
    motion_need = sum(nm for nf, nm, ns in SECTION_TARGETS.values())
    still_q = deque(repeated(stills, still_need, 2, "still"))
    motion_q = deque(repeated(motion_pool, motion_need, 2, "motion"))
    cuts = []
    # EP48 warp/matte-seam fix (owner 2026-07-24): the "depth" treatment is a real 3D depth-map
    # displacement (DepthStill / <name>_depth.png on a subdivided plane). On night shots with a
    # strong foreground subject at a hard depth discontinuity (the patrol car in S01/S37) the plane
    # STRETCHES across the depth cliff and TEARS into a hard-edged polygonal patch + streaks — this
    # is exactly the "warp / broken composite seam" the owner flagged at 0:18 and 4:39. Drop depth
    # for glover and cycle only the NON-tearing 2.5D parallax treatments (blurred bg layer + sharp fg
    # drifting opposite — genuine depth MOTION, no displacement map, cannot tear). Keeps premium
    # motion (no 紙芝居) while removing every matte-seam.
    treatments = ["bleed", "scan", "duotone", "focus"]
    treat_i = 0
    for sec in SECTION_ORDER:
        nf, nm, ns = SECTION_TARGETS[sec]
        s, e = windows[sec]
        fac = take(factory_q, nf, "factory")
        mot = take(motion_q, nm, "motion")
        sti = take(still_q, ns, "still")
        seq = []
        fi = mi = si = 0
        pattern = ["F", "S", "M", "F", "S", "F"]
        while fi < len(fac) or mi < len(mot) or si < len(sti):
            slot = pattern[len(seq) % len(pattern)]
            if slot == "F" and fi < len(fac):
                seq.append(("footage", fac[fi])); fi += 1
            elif slot == "M" and mi < len(mot):
                seq.append(("footage", mot[mi])); mi += 1
            elif slot == "S" and si < len(sti):
                seq.append(("img", sti[si])); si += 1
            elif fi < len(fac):
                seq.append(("footage", fac[fi])); fi += 1
            elif mi < len(mot):
                seq.append(("footage", mot[mi])); mi += 1
            elif si < len(sti):
                seq.append(("img", sti[si])); si += 1
        weights = [3.0 if kind == "img" else 3.34 for kind, _ in seq]
        scale = (e - s) / sum(weights)
        t = s
        for kind, src in seq:
            raw = 3.0 if kind == "img" else 3.34
            dur = round(raw * scale, 3)
            cut = {"id": f"cut-{len(cuts):03d}", "start": round(t, 3), "dur": dur, "kind": kind, "src": src, "seed": f"glover-{len(cuts):03d}", "act": sec}
            cut["treatment"] = treatments[treat_i % len(treatments)] if kind == "img" else "footage"
            if kind == "img":
                treat_i += 1
            cuts.append(cut)
            t += dur
        cuts[-1]["dur"] = round(e - cuts[-1]["start"], 3)
    return cuts


def make_hook(manifest: dict) -> list[dict]:
    stills = [x for x in manifest.get("stills", []) if x.get("role") == "body" and x.get("also_thumb")]
    picks = [str(x["public_path"]) for x in stills[:6]]
    dur = round(8.0 / len(picks), 3)
    hook = []
    t = 0.0
    for i, src in enumerate(picks):
        d = round(8.0 - t, 3) if i == len(picks) - 1 else dur
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": src, "seed": f"glover-hook-{i:02d}"})
        t += d
    return hook


def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def figure_payloads() -> list[dict]:
    return [
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction, no likeness"},
        K(["A PLATE", "A HIT", "A STOP"], ["STOP"], "emphasis"),
        {
            "kind": "routemap",
            "label": "plate run - owner status - brief stop - Court review",
            "pins": [
                {"x": 0.24, "y": 0.62, "label": "LICENSE REVOKED"},
                {"x": 0.48, "y": 0.46, "label": "owner status known"},
                {"x": 0.72, "y": 0.58, "label": "brief stop"},
            ],
        },
        {"kind": "acttitle", "title": "THE STOP", "kicker": "ACT ONE", "index": 1},
        {"kind": "lowerthird", "primary": "Charles Glover Jr.", "secondary": "symbolic objects only"},
        {"kind": "compbars", "items": [{"label": "driver not yet identified", "value": 1}, {"label": "owner status known", "value": 1}]},
        {"kind": "probablecause", "outcome": "stall"},
        K(["NOT PROOF", "REASONABLE SUSPICION"], ["REASONABLE"], "emphasis"),
        {"kind": "acttitle", "title": "THE INFERENCE", "kicker": "ACT TWO", "index": 2},
        {"kind": "brightline", "mode": "draw"},
        {"kind": "lowerthird", "primary": "reasonable suspicion", "secondary": "less than probable cause"},
        {"kind": "mechanism", "mechanism": "faultsplit"},
        {"kind": "compbars", "items": [{"label": "common sense inference", "value": 1}, {"label": "contrary information dissolves it", "value": 1}]},
        {"kind": "statemap", "label": "a narrow rule, not a blank check"},
        {"kind": "acttitle", "title": "THE LIMIT", "kicker": "ACT THREE", "index": 3},
        {"kind": "votetally", "majority": 8, "dissent": 1, "label": "the stop stands under a narrow rule"},
        {"kind": "stat", "value": 8, "suffix": " / 1", "label": "UPHELD, with limits", "topLabel": "KANSAS v. GLOVER"},
        {"kind": "numberticker", "value": 2020, "label": "decided April 6", "group": False},
        {"kind": "quote", "quote": "When the officer lacks information negating an inference that the owner is driving the vehicle, the stop is reasonable.", "attribution": "Justice Thomas, for the Court"},
        {"kind": "quote", "quote": "We emphasize the narrow scope of our holding.", "attribution": "Justice Thomas, for the Court"},
        {"kind": "lowerthird", "primary": "Justice Kagan, concurring", "secondary": "joined by Justice Ginsburg"},
        {"kind": "mechanism", "mechanism": "closingdoor"},
        {"kind": "quote", "quote": "Consider, for example, if Kansas had suspended rather than revoked Glover's license.", "attribution": "Justice Kagan, concurring"},
        {"kind": "lowerthird", "primary": "Justice Sotomayor, dissenting", "secondary": "the lone dissent"},
        {"kind": "quote", "quote": "The majority today has paved the road to finding reasonable suspicion based on nothing more than a demographic profile.", "attribution": "Justice Sotomayor, dissenting"},
        K(["A NARROW RULE", "NOT ANY CAR"], ["NARROW"], "emphasis"),
        {"kind": "timeline", "events": [{"year": "plate", "text": "owner status"}, {"year": "stop", "text": "brief investigation"}, {"year": "2020", "text": "upheld with limits"}]},
        {"kind": "compbars", "items": [{"label": "owner may be driving", "value": 1}, {"label": "plainly different driver", "value": 0}]},
        {"kind": "acttitle", "title": "YOUR CAR", "kicker": "ENDING", "index": 4},
        {"kind": "bar", "items": [{"label": "reasonable", "value": 1}, {"label": "certainty", "value": 0}]},
        {"kind": "numberticker", "value": 589, "suffix": " U.S.", "label": "Kansas v. Glover"},
        {"kind": "numberticker", "value": 556, "prefix": "No. 18-", "label": "case docket"},
        {"kind": "stat", "value": 4, "label": "Fourth Amendment question", "topLabel": "YOUR CAR"},
        K(["THE REASON", "CAN DISAPPEAR"], ["DISAPPEAR"], "emphasis"),
        {"kind": "lowerthird", "primary": "The stop stood", "secondary": "the inference remains limited"},
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction, no likeness"},
    ]


def place_figures(windows: dict[str, tuple[float, float]], total: float) -> list[dict]:
    section_counts = [("HOOK", 3), ("ACT_1", 5), ("ACT_2", 6), ("ACT_3", 14), ("ENDING", 8)]
    payloads = deque(figure_payloads())
    figures = []
    dur = 5.8
    for sec, count in section_counts:
        s, e = windows[sec]
        lo = s + (4.0 if sec == "HOOK" else 3.0)
        hi = e - 7.0
        if sec == "ENDING":
            hi = min(hi, total - 12.5)
        span = max(dur + 0.5, hi - lo)
        for i in range(count):
            start = lo + (span * (i + 0.5) / count) - dur / 2
            payload = payloads.popleft()
            if payload["kind"] not in VALID_KINDS:
                raise SystemExit(f"invalid figure kind {payload['kind']}")
            figures.append({"start": round(start, 3), "end": round(start + dur, 3), **payload})
    figures.sort(key=lambda x: x["start"])
    return figures


def write_premium_beats(cuts: list[dict], figures: list[dict], total: float) -> None:
    beats = []
    fps = FPS
    for c in cuts:
        kind = "factory" if c["kind"] == "footage" else "hero"
        component = "FactoryClip" if c["kind"] == "footage" else "WilliamsScene"
        beats.append({"kind": kind, "component": component, "start_frame": int(round(c["start"] * fps)), "dur_frames": max(1, int(round(c["dur"] * fps)))})
    for f in figures:
        beats.append({"kind": "mg_hero", "component": f"FigureBeats:{f.get('kind')}", "start_frame": int(round(f["start"] * fps)), "dur_frames": max(1, int(round((f["end"] - f["start"]) * fps)))})
    PREMIUM_BEATSHEET.write_text(json.dumps({"meta": {"fps": fps, "projected_runtime_seconds": total}, "beats": beats}, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    ap.add_argument("--narr", type=Path, default=DEFAULT_NARR)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--captions", type=Path, default=DEFAULT_SRT)
    args = ap.parse_args()
    manifest = load_json(args.assets)
    n_factory = len(public_items(manifest, "factory"))
    n_motion = len(public_items(manifest, "motion"))
    if n_factory != 92 or n_motion != 16:
        raise SystemExit(f"manifest footage counts invalid: factory={n_factory} motion={n_motion}")
    narr = load_json(args.narr)
    captions, total = build_captions(narr)
    windows = section_windows(narr, total)
    cuts = make_cuts(windows, manifest)
    figures = place_figures(windows, total)
    write_srt(captions, args.captions)
    counts = {
        "factory": sum(1 for c in cuts if "/factory/" in c["src"].replace("\\", "/")),
        "motion": sum(1 for c in cuts if "/motion/" in c["src"].replace("\\", "/")),
        "stills": sum(1 for c in cuts if c["kind"] == "img"),
    }
    expected = {"factory": 92, "motion": 32, "stills": 101}
    if counts != expected or len(cuts) != 225:
        raise SystemExit(f"cut allocation mismatch: cuts={len(cuts)} counts={counts} expected={expected}")
    total_frames = round(8.0 * FPS) + round(3.5 * FPS) + int(total * FPS + 0.999999) + round(9.0 * FPS)
    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": str(narr.get("audio_path") or "glover/audio/vc_master_v001.mp3"),
        "narrationSeconds": round(total, 3),
        "hookSeconds": 8.0,
        "hookLine": "A plate. A hit. A stop you never saw coming.",
        "hook": make_hook(manifest),
        "cuts": cuts,
        "captions": captions,
        "graphics": [],
        "figures": figures,
        "overlays": [x["public_path"] for x in manifest.get("overlay", []) if x.get("public_path")],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")
    PUB_FILM.parent.mkdir(parents=True, exist_ok=True)
    PUB_FILM.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")
    uses = Counter(c["src"] for c in cuts)
    report = {
        "cuts": len(cuts),
        **counts,
        "distinct_assets": len(uses),
        "first_use_share": round(len(uses) / len(cuts), 4),
        "figures": len(figures),
        "duration_frames": total_frames,
        "duration_sec_with_bookends": round(total_frames / FPS, 3),
    }
    BUILD_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    BUILD_MANIFEST.write_text(json.dumps({"episode_id": EP, "producer": "scripts/build_glover_film.py", "inputs": {"assets": str(args.assets), "narr": str(args.narr)}, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    BEATSHEET.write_text(json.dumps({"schema_version": "glover_beatsheet.v1", "episode_id": EP, "figures": figures, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    write_premium_beats(cuts, figures, total)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
