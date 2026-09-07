#!/usr/bin/env python
"""Build remotion/src/data/strieff_film.json for EP49 from an asset manifest."""
from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-049-strieff"
SLUG = "strieff"
FPS = 30
DEFAULT_ASSETS = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
DEFAULT_NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
DEFAULT_OUT = ROOT / "remotion" / "src" / "data" / "strieff_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "strieff" / "film_data.v001.json"
BUILD_MANIFEST = ROOT / "episodes" / EP / "04_scenes" / "strieff_build_manifest.v001.json"
BEATSHEET = ROOT / "episodes" / EP / "04_scenes" / "strieff_beatsheet.v001.json"
DEFAULT_SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"

SECTION_TARGETS = {
    # factory, motion, still. Totals: 93 / 32 / 101 = 226 cuts.
    "HOOK": (5, 2, 6),
    "OP": (8, 3, 9),
    "ACT_1": (15, 5, 17),
    "ACT_2": (17, 6, 20),
    "ACT_3": (30, 10, 30),
    "ENDING": (18, 6, 19),
}
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ENDING"]
VALID_KINDS = {"numberticker", "stat", "votetally", "timeline", "quote", "kinetic", "lowerthird", "acttitle", "compbars", "bar", "mechanism", "regionmap", "statemap", "brightline", "pindropmap", "routemap"}


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
    for c in narr["chunks"]:
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
    for c in narr["chunks"]:
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
    still_pool = repeated(stills, still_need, 2, "still")
    motion_items = repeated(motion_pool, motion_need, 2, "motion")
    still_q = deque(still_pool)
    motion_q = deque(motion_items)
    cuts = []
    # EP49 warp fix (owner 2026-07-24): the "depth" treatment (CaseFilm DepthStill —
    # Three.js depth-map displacement) MELTED S01's doorway figure into a smeared cone
    # (bad DPT map -> aggressive displacementScale). It is the ONLY warp source in the
    # film (all 16 i2v motion clips + 93 factory plates eyeballed clean). Reliability
    # wins per the owner mandate: drop depth entirely and use divergent-parallax
    # treatments that CANNOT warp (no mesh displacement) while still moving (bleed =
    # bg-blur + sharp-fg opposite drift). Motion density is unchanged (all four are
    # "still" treatments to the kinetic gates).
    treatments = ["bleed", "scan", "duotone", "focus"]
    treat_i = 0
    for sec in SECTION_ORDER:
        if sec not in windows:
            continue
        nf, nm, ns = SECTION_TARGETS[sec]
        if nf + nm + ns == 0:
            continue
        s, e = windows[sec]
        seq = []
        fac = take(factory_q, nf, "factory")
        mot = take(motion_q, nm, "motion")
        sti = take(still_q, ns, "still")
        fi = mi = si = 0
        pattern = ["F", "S", "M", "F", "S", "F"]
        while fi < len(fac) or mi < len(mot) or si < len(sti):
            slot = pattern[(len(seq)) % len(pattern)]
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
        weights = [3.0 if kind == "img" else 3.343 for kind, _ in seq]
        scale = (e - s) / sum(weights)
        t = s
        for kind, src in seq:
            raw = 3.0 if kind == "img" else 3.343
            dur = round(raw * scale, 3)
            cut = {"id": f"cut-{len(cuts):03d}", "start": round(t, 3), "dur": dur, "kind": kind, "src": src, "seed": f"strieff-{len(cuts):03d}", "act": sec}
            if kind == "img":
                cut["treatment"] = treatments[treat_i % len(treatments)]
                treat_i += 1
            else:
                cut["treatment"] = "footage"
            cuts.append(cut)
            t += dur
        if cuts:
            cuts[-1]["dur"] = round(e - cuts[-1]["start"], 3)
    return cuts


def make_hook(manifest: dict) -> list[dict]:
    stills = public_items(manifest, "stills", "body")
    picks = stills[:6]
    dur = round(8.0 / len(picks), 3)
    hook = []
    t = 0.0
    for i, src in enumerate(picks):
        d = round(8.0 - t, 3) if i == len(picks) - 1 else dur
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": src, "seed": f"strieff-hook-{i:02d}"})
        t += d
    return hook


def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def figure_payloads() -> list[dict]:
    # 37 figures, spec floor 31 + 6. Only ledger-verified values are burned; every
    # numeric field is in {0,1,2 (geometry), 3,4,5,8,232,579,2016}. NO dochighlight.
    # Quotes are verbatim dissent excerpts with neutral "dissenting" attribution.
    # Order = HOOK(3), OP(4), ACT_1(8), ACT_2(8), ACT_3(10), ENDING(4).
    return [
        # --- HOOK (3) ---
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction"},
        K(["THE WARRANT", "IN YOUR POCKET"], ["WARRANT"]),
        {"kind": "pindropmap", "pins": [{"x": 0.62, "y": 0.44, "label": "South Salt Lake City, Utah"}]},
        # --- OP (4) ---
        K(["A STOP", "WITH NO REASON"], ["NO REASON"], "emphasis"),
        {"kind": "lowerthird", "primary": "The exclusionary rule", "secondary": "illegal searches are normally thrown out"},
        {"kind": "acttitle", "title": "THE ILLEGAL STOP", "kicker": "UTAH v. STRIEFF"},
        {"kind": "lowerthird", "primary": "Utah v. Strieff, 579 U.S. 232", "secondary": "the U.S. Supreme Court"},
        # --- ACT_1 The stop (8) ---
        {"kind": "acttitle", "title": "THE STOP", "kicker": "ACT ONE", "index": 1},
        {"kind": "routemap", "label": "the chain from an illegal stop to the evidence", "pins": [{"x": 0.12, "y": 0.60, "label": "illegal stop"}, {"x": 0.36, "y": 0.48, "label": "ID check"}, {"x": 0.60, "y": 0.58, "label": "warrant hit"}, {"x": 0.84, "y": 0.48, "label": "arrest and search"}]},
        K(["THE STOP", "WAS ILLEGAL"], ["ILLEGAL"], "emphasis"),
        {"kind": "lowerthird", "primary": "No reasonable suspicion", "secondary": "the State conceded the stop was illegal"},
        {"kind": "mechanism", "mechanism": "faultsplit", "label": "the pre-existing warrant surfaces - the intervening circumstance"},
        {"kind": "stat", "value": 4, "label": "THE FOURTH AMENDMENT - unreasonable searches and seizures"},
        {"kind": "lowerthird", "primary": "Detective Fackrell", "secondary": "South Salt Lake City police"},
        {"kind": "bar", "items": [{"label": "time", "value": 1}, {"label": "warrant", "value": 2}, {"label": "flagrancy", "value": 1}]},
        # --- ACT_2 The exclusionary rule (8) ---
        {"kind": "acttitle", "title": "THE EXCLUSIONARY RULE", "kicker": "ACT TWO", "index": 2},
        {"kind": "brightline", "mode": "draw"},
        {"kind": "lowerthird", "primary": "Fruit of the poisonous tree", "secondary": "the stop poisons what grows from it"},
        K(["ATTENUATION"], None, "maskslide"),
        {"kind": "compbars", "items": [{"label": "minutes - favors suppression", "value": 1}, {"label": "the warrant - favors admission", "value": 2}]},
        {"kind": "stat", "value": 3, "label": "BROWN v. ILLINOIS FACTORS"},
        {"kind": "mechanism", "mechanism": "faultsplit", "label": "did the warrant snap the chain?"},
        K(["DID THE WARRANT", "BREAK THE CHAIN?"], ["WARRANT"]),
        # --- ACT_3 The ruling (10) --- quotes spaced apart (no two adjacent same kind)
        {"kind": "acttitle", "title": "THE RULING", "kicker": "ACT THREE", "index": 3},
        {"kind": "numberticker", "value": 2016, "label": "decided - Supreme Court", "group": False},
        {"kind": "votetally", "majority": 5, "dissent": 3, "label": "an 8-justice court - Scalia's seat empty"},
        {"kind": "stat", "value": 8, "topLabel": "5-3", "label": "JUSTICES SAT - SCALIA'S SEAT WAS EMPTY"},
        {"kind": "quote", "quote": "It implies that you are not a citizen of a democracy but the subject of a carceral state, just waiting to be cataloged.", "attribution": "Justice Sotomayor, dissenting"},
        {"kind": "lowerthird", "primary": "Justice Clarence Thomas", "secondary": "for the majority"},
        {"kind": "quote", "quote": "The officer's incentive to violate the Constitution thus increases.", "attribution": "Justice Kagan, dissenting"},
        {"kind": "compbars", "items": [{"label": "flagrancy - at most negligent", "value": 1}, {"label": "the majority - favors admission", "value": 2}]},
        {"kind": "mechanism", "mechanism": "faultsplit", "label": "the warrant broke the chain - the evidence stayed"},
        {"kind": "quote", "quote": "The white defendant in this case shows that anyone's dignity can be violated in this manner.", "attribution": "Justice Sotomayor, dissenting"},
        # --- ENDING (4) ---
        K(["THE ILLEGAL STOP", "BECOMES ALMOST FREE"], ["FREE"], "emphasis"),
        {"kind": "statemap", "label": "outstanding warrants exist across the country - often for something small"},
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "a door held open - an unlawful stop pays off when a warrant is waiting"},
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction"},
    ]


def place_figures(windows: dict[str, tuple[float, float]], total: float) -> list[dict]:
    section_counts = [("HOOK", 3), ("OP", 4), ("ACT_1", 8), ("ACT_2", 8), ("ACT_3", 10), ("ENDING", 4)]
    payloads = deque(figure_payloads())
    figures = []
    dur = 5.4
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    ap.add_argument("--narr", type=Path, default=DEFAULT_NARR)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--captions", type=Path, default=DEFAULT_SRT)
    args = ap.parse_args()
    manifest = load_json(args.assets)
    if manifest.get("is_stub") is True:
        raise SystemExit("EP49 requires a real asset manifest: is_stub must be false")
    # EP45 empty-array fix: assert factory(93)/motion(16) load non-empty before building.
    # A slideshow (0 footage) is a hard stop -> bounce back to thread A, never green a stub.
    n_factory = len(public_items(manifest, "factory"))
    n_motion = len(public_items(manifest, "motion"))
    if n_factory != 93 or n_motion != 16:
        raise SystemExit(f"factory/motion count mismatch: factory={n_factory} (need 93) motion={n_motion} (need 16)")
    narr = load_json(args.narr)
    captions, total = build_captions(narr)
    windows = section_windows(narr, total)
    cuts = make_cuts(windows, manifest)
    hook = make_hook(manifest)
    figures = place_figures(windows, total)
    total_frames = round(8.0 * FPS) + round(3.5 * FPS) + int(total * FPS + 0.999999) + round(9.0 * FPS)
    if total_frames / FPS > 750.0:
        raise SystemExit(f"duration too long: {total_frames / FPS:.3f}s > 750.0s")
    counts = {
        "factory": sum(1 for c in cuts if "/factory/" in c["src"].replace("\\", "/")),
        "motion": sum(1 for c in cuts if "/motion/" in c["src"].replace("\\", "/")),
        "stills": sum(1 for c in cuts if c["kind"] == "img"),
    }
    expected = {"factory": 93, "motion": 32, "stills": 101}
    if counts != expected or len(cuts) != 226:
        raise SystemExit(f"cut allocation mismatch: cuts={len(cuts)} counts={counts} expected={expected}")
    write_srt(captions, args.captions)
    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": str(narr.get("audio_path") or "strieff/narration.mp3"),
        "narrationSeconds": round(total, 3),
        "hookSeconds": 8.0,
        "hookLine": "A stop with no reason. A warrant. A search the law now lets count.",
        "hook": hook,
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
    still_time = sum(c["dur"] for c in cuts if c["kind"] == "img")
    motion_time = sum(c["dur"] for c in cuts if c["kind"] != "img")
    report = {
        "cuts": len(cuts),
        **counts,
        "distinct_assets": len(uses),
        "first_use_share": round(len(uses) / len(cuts), 4),
        "still_time_share": round(still_time / total, 4),
        "motion_time_share": round(motion_time / total, 4),
        "figures": len(figures),
        "duration_frames": total_frames,
        "duration_sec_with_bookends": round(total_frames / FPS, 3),
    }
    BUILD_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    BUILD_MANIFEST.write_text(json.dumps({"episode_id": EP, "producer": "scripts/build_strieff_film.py", "inputs": {"assets": str(args.assets), "narr": str(args.narr)}, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    BEATSHEET.write_text(json.dumps({"schema_version": "strieff_beatsheet.v1", "episode_id": EP, "figures": figures, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


