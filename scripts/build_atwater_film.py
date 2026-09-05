#!/usr/bin/env python
"""Build remotion/src/data/atwater_film.json for EP47 from an asset manifest.

Cloned from build_cleveland_film.py (EP45). Only constants + SECTION_TARGETS +
figure payloads are swapped for Atwater; the allocation logic
(public_items/repeated/take/make_cuts/place_figures) is unchanged.

EP47 requires REAL footage. The manifest MUST carry factory[] (92) and
motion[] (16). If those arrays are absent/empty (EP45 paper-slideshow failure),
this exits 1 and refers the build back upstream instead of going green on stills.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-047-atwater"
SLUG = "atwater"
FPS = 30
DEFAULT_ASSETS = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
DEFAULT_NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
DEFAULT_OUT = ROOT / "remotion" / "src" / "data" / "atwater_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "atwater" / "film_data.v001.json"
BUILD_MANIFEST = ROOT / "episodes" / EP / "04_scenes" / "atwater_build_manifest.v001.json"
BEATSHEET = ROOT / "episodes" / EP / "04_scenes" / "atwater_beatsheet.v001.json"
DEFAULT_SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"

SECTION_TARGETS = {
    # factory, motion, still. Totals: 92 / 32 / 101 = 225 cuts.
    "HOOK": (6, 2, 5),
    "OP": (6, 3, 10),
    "ACT_1": (14, 5, 17),
    "ACT_2": (18, 6, 20),
    "ACT_3": (30, 10, 30),
    "ENDING": (18, 6, 19),
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
    treatments = ["depth", "scan", "duotone", "focus"]
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
            cut = {"id": f"cut-{len(cuts):03d}", "start": round(t, 3), "dur": dur, "kind": kind, "src": src, "seed": f"atwater-{len(cuts):03d}", "act": sec}
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
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": src, "seed": f"atwater-hook-{i:02d}"})
        t += d
    return hook


def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def figure_payloads() -> list[dict]:
    # 36 figures. Ledger-backed values only ($50/2001/5-4/532/§1983 etc).
    # No dochighlight. No 1997, no child ages (A18/A19 medium -> never burned).
    # votetally uses majority/dissent per the real FigureBeats union.
    return [
        # -- HOOK (3) --
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction, no likeness"},
        K(["THE FIFTY DOLLAR", "ARREST"], ["FIFTY"], "emphasis"),
        {"kind": "pindropmap", "pins": [{"x": 0.55, "y": 0.62, "label": "Lago Vista, Texas"}]},
        # -- OP (3) --
        {"kind": "stat", "value": 50, "prefix": "$", "label": "MAXIMUM FINE - NO JAIL", "topLabel": "THE ENTIRE PENALTY"},
        K(["HANDCUFFS FOR", "FIFTY DOLLARS?"], ["FIFTY"], "emphasis"),
        {"kind": "lowerthird", "primary": "Atwater v. City of Lago Vista", "secondary": "532 U.S. 318, decided 2001"},
        # -- ACT_1 (7) --
        {"kind": "acttitle", "title": "THE STOP", "kicker": "ACT ONE", "index": 1},
        {"kind": "routemap", "label": "stop - handcuffs - squad car - station - holding cell - magistrate"},
        {"kind": "lowerthird", "primary": "Officer Bart Turek", "secondary": "Lago Vista Police Department"},
        {"kind": "stat", "value": 0, "suffix": " DAYS OF JAIL", "label": "the entire penalty is a fine", "topLabel": "FINE-ONLY OFFENSE"},
        {"kind": "numberticker", "value": 50, "prefix": "$", "label": "no contest - the fine paid"},
        {"kind": "compbars", "items": [{"label": "the sentence: a $50 fine", "value": 1}, {"label": "before any verdict: handcuffs, a cell, a booking photo", "value": 1}]},
        {"kind": "stat", "value": 1, "label": "booking: shoes, possessions, about an hour in a cell", "topLabel": "HELD, THEN RELEASED ON BOND"},
        # -- ACT_2 (8) --
        {"kind": "acttitle", "title": "THE QUESTION", "kicker": "ACT TWO", "index": 2},
        {"kind": "lowerthird", "primary": "The Fourth Amendment", "secondary": "protection against unreasonable searches and seizures"},
        {"kind": "lowerthird", "primary": "42 U.S.C. Section 1983", "secondary": "sue an official for a constitutional violation"},
        {"kind": "probablecause", "outcome": "stall"},
        {"kind": "compbars", "items": [{"label": "Atwater: fine-only, so write a citation", "value": 1}, {"label": "City: probable cause, so a full arrest is allowed", "value": 1}]},
        {"kind": "brightline", "mode": "draw"},
        K(["IS PROBABLE CAUSE", "ENOUGH?"], ["ENOUGH?"], "emphasis"),
        {"kind": "stat", "value": 0, "suffix": " JAIL TIME", "label": "no jail exists for this offense", "topLabel": "FINE-ONLY"},
        # -- ACT_3 (10) --
        {"kind": "acttitle", "title": "THE RULING", "kicker": "ACT THREE", "index": 3},
        {"kind": "timeline", "events": [{"year": "the stop", "text": "a fine-only seatbelt offense"}, {"year": "Section 1983", "text": "the suit reaches federal court"}, {"year": "2001", "text": "the Supreme Court affirms"}]},
        {"kind": "votetally", "majority": 5, "dissent": 4, "label": "Souter majority - O'Connor dissent"},
        {"kind": "stat", "value": 5, "suffix": " / 4", "label": "THE ARREST STANDS - constitutional (5-4)", "topLabel": "UPHELD"},
        {"kind": "quote", "quote": "Atwater's claim to live free of pointless indignity and confinement clearly outweighs anything the City can raise against it specific to her case.", "attribution": "Justice Souter, for the Court - yet permitted"},
        {"kind": "mechanism", "mechanism": "faultsplit"},
        {"kind": "compbars", "items": [{"label": "majority: probable cause is enough", "value": 1}, {"label": "dissent: reasonableness must balance", "value": 1}]},
        {"kind": "quote", "quote": "The Court neglects the Fourth Amendment's express command in the name of administrative ease. In so doing, it cloaks the pointless indignity that Gail Atwater suffered with the mantle of reasonableness.", "attribution": "Justice O'Connor, dissenting"},
        {"kind": "numberticker", "value": 2001, "label": "decided - the Supreme Court"},
        {"kind": "mechanism", "mechanism": "closingdoor"},
        # -- ENDING (5) --
        K(["ALLOWED,", "NOT ILLEGAL"], ["ALLOWED"], "emphasis"),
        {"kind": "stat", "value": 50, "prefix": "$", "label": "the whole penalty, yet the arrest was allowed", "topLabel": "ALLOWED, NOT REQUIRED"},
        {"kind": "statemap", "label": "some states legislate limits - the Constitution does not"},
        {"kind": "bar", "items": [{"label": "covered by your state's statute", "value": 1}, {"label": "not by the Fourth Amendment", "value": 1}]},
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction, no likeness"},
    ]


def place_figures(windows: dict[str, tuple[float, float]], total: float) -> list[dict]:
    section_counts = [("HOOK", 3), ("OP", 3), ("ACT_1", 7), ("ACT_2", 8), ("ACT_3", 10), ("ENDING", 5)]
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", type=Path, default=DEFAULT_ASSETS)
    ap.add_argument("--narr", type=Path, default=DEFAULT_NARR)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--captions", type=Path, default=DEFAULT_SRT)
    args = ap.parse_args()
    manifest = load_json(args.assets)
    if manifest.get("is_stub") is True:
        raise SystemExit("EP47 requires a real asset manifest: is_stub must be false")
    # EP45 paper-slideshow guard: factory[]/motion[] must be populated with real footage.
    n_factory = len(public_items(manifest, "factory"))
    n_motion = len(public_items(manifest, "motion"))
    if n_factory != 92:
        raise SystemExit(f"manifest factory[] has {n_factory} items, need 92 real clips - footage missing, refer upstream (do not go green on stills)")
    if n_motion != 16:
        raise SystemExit(f"manifest motion[] has {n_motion} items, need 16 real i2v clips - i2v missing, refer upstream")
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
    expected = {"factory": 92, "motion": 32, "stills": 101}
    if counts != expected or len(cuts) != 225:
        raise SystemExit(f"cut allocation mismatch: cuts={len(cuts)} counts={counts} expected={expected}")
    write_srt(captions, args.captions)
    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": str(narr.get("audio_path") or "atwater/audio/narration_master.v001.mp3"),
        "narrationSeconds": round(total, 3),
        "hookSeconds": 8.0,
        "hookLine": "For something worth nothing but a fifty dollar fine, can the police handcuff you and take you to jail?",
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
    BUILD_MANIFEST.write_text(json.dumps({"episode_id": EP, "producer": "scripts/build_atwater_film.py", "inputs": {"assets": str(args.assets), "narr": str(args.narr)}, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    BEATSHEET.write_text(json.dumps({"schema_version": "atwater_beatsheet.v1", "episode_id": EP, "figures": figures, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
