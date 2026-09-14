#!/usr/bin/env python
"""Build remotion/src/data/caniglia_film.json for EP43 from an asset manifest."""
from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-043-caniglia"
SLUG = "caniglia"
FPS = 30
DEFAULT_ASSETS = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.stub.v001.json"
DEFAULT_NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.stub.v001.json"
DEFAULT_OUT = ROOT / "remotion" / "src" / "data" / "caniglia_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "caniglia_dryrun" / "film_data.v001.json"
BUILD_MANIFEST = ROOT / "episodes" / EP / "04_scenes" / "caniglia_build_manifest.v001.json"
BEATSHEET = ROOT / "episodes" / EP / "04_scenes" / "caniglia_beatsheet.v001.json"
DEFAULT_SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"

SECTION_TARGETS = {
    # factory, motion, still. Totals: 93 / 32 / 101 = 226 cuts.
    "HOOK": (5, 2, 6),
    "OP": (0, 0, 7),
    "ACT_1": (14, 4, 15),
    "ACT_2": (16, 5, 16),
    "ACT_3": (40, 15, 37),
    "ENDING": (18, 6, 20),
}
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ENDING"]
VALID_KINDS = {"numberticker", "stat", "votetally", "timeline", "quote", "kinetic", "lowerthird", "acttitle", "compbars", "mechanism", "dochighlight", "regionmap", "pindropmap"}


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


def repeated(pool: list[str], n: int, cap: int) -> list[str]:
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
        raise SystemExit(f"unable to allocate {n} assets with cap {cap}")
    return out


def make_cuts(windows: dict[str, tuple[float, float]], manifest: dict) -> list[dict]:
    stills = public_items(manifest, "stills", "body")
    factory_q = deque(public_items(manifest, "factory"))
    motion_pool = public_items(manifest, "motion")
    still_need = sum(ns for nf, nm, ns in SECTION_TARGETS.values())
    motion_need = sum(nm for nf, nm, ns in SECTION_TARGETS.values())
    still_pool = repeated(stills, still_need, 2)
    motion_items = repeated(motion_pool, motion_need, 2)
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
            cut = {"id": f"cut-{len(cuts):03d}", "start": round(t, 3), "dur": dur, "kind": kind, "src": src, "seed": f"caniglia-{len(cuts):03d}", "act": sec}
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
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": src, "seed": f"caniglia-hook-{i:02d}"})
        t += d
    return hook


def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def figure_payloads() -> list[dict]:
    return [
        K(["THE WELFARE CHECK"], ["WELFARE"], "emphasis"),
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction"},
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "threshold"},
        {"kind": "acttitle", "title": "THE NIGHT", "kicker": "ACT ONE", "index": 1},
        {"kind": "timeline", "events": [{"year": "AUGUST 2015", "text": "Cranston, Rhode Island"}]},
        K(["MAKE SURE", "HE IS OK"], ["OK"], "wordpop"),
        {"kind": "lowerthird", "primary": "non-emergency welfare check", "secondary": "symbolic reconstruction"},
        {"kind": "dochighlight", "rects": [{"x": 0.2, "y": 0.35, "w": 0.6, "h": 0.12}], "mode": "redact"},
        {"kind": "mechanism", "mechanism": "faultsplit", "left": "care", "right": "search"},
        {"kind": "acttitle", "title": "THE WELFARE CHECK", "kicker": "ACT TWO", "index": 2},
        {"kind": "stat", "value": 2, "label": "handguns seized - no warrant"},
        K(["NO WARRANT"], ["WARRANT"], "emphasis"),
        {"kind": "pindropmap", "pins": [{"x": 0.42, "y": 0.48, "label": "Cranston, RI"}]},
        {"kind": "dochighlight", "rects": [{"x": 0.18, "y": 0.42, "w": 0.64, "h": 0.1}], "mode": "box"},
        {"kind": "lowerthird", "primary": "First Circuit", "secondary": "953 F.3d 112 (2020)"},
        {"kind": "acttitle", "title": "THE CAR RULE", "kicker": "ACT THREE", "index": 3},
        {"kind": "lowerthird", "primary": "Cady v. Dombrowski", "secondary": "police-custody vehicle"},
        {"kind": "compbars", "items": [{"label": "vehicle", "value": 1}, {"label": "home", "value": 0}]},
        {"kind": "timeline", "events": [{"year": "1973", "text": "Cady - car in custody"}, {"year": "2021", "text": "Caniglia - home"}]},
        {"kind": "regionmap", "label": "lower-court split", "pattern": "varied"},
        {"kind": "acttitle", "title": "THE THRESHOLD", "kicker": "THE COMMAND", "index": 4},
        {"kind": "timeline", "events": [{"year": "MAR 24 2021", "text": "argued"}, {"year": "MAY 17 2021", "text": "decided"}]},
        {"kind": "numberticker", "value": 7, "suffix": " weeks", "label": "argument to decision"},
        {"kind": "lowerthird", "primary": "Caniglia v. Strom", "secondary": "593 U.S. 194 (2021), No. 20-157"},
        {"kind": "quote", "quote": "very core", "attribution": "Florida v. Jardines"},
        {"kind": "votetally", "majority": 9, "dissent": 0, "label": "one excuse closed - vacate and remand"},
        K(["ONE EXCUSE", "CLOSED"], ["EXCUSE"], "emphasis"),
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "community caretaking at home"},
        {"kind": "lowerthird", "primary": "warrant", "secondary": "still open"},
        {"kind": "lowerthird", "primary": "consent", "secondary": "still open"},
        {"kind": "lowerthird", "primary": "emergency aid", "secondary": "still open"},
        {"kind": "dochighlight", "rects": [{"x": 0.24, "y": 0.36, "w": 0.52, "h": 0.14}], "mode": "underline"},
        {"kind": "stat", "value": 3, "label": "separate concurrences"},
        {"kind": "lowerthird", "primary": "sent back down", "secondary": "not final disposition"},
        K(["NOT A WALL", "AROUND YOUR HOME"], ["NOT"], "emphasis"),
        {"kind": "mechanism", "mechanism": "faultsplit", "left": "help", "right": "carry out"},
        K(["WARRANT", "CONSENT", "EMERGENCY"], ["EMERGENCY"], "wordpop"),
        {"kind": "lowerthird", "primary": "what remained open", "secondary": "real emergency aid"},
        {"kind": "timeline", "events": [{"year": "after remand", "text": "hard questions remain"}]},
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "a narrower key"},
        K(["THE DOOR", "IS STILL A DOOR"], ["DOOR"], "emphasis"),
    ]


def place_figures(windows: dict[str, tuple[float, float]], total: float) -> list[dict]:
    section_counts = [("HOOK", 3), ("ACT_1", 8), ("ACT_2", 8), ("ACT_3", 14), ("ENDING", 4)]
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
    narr = load_json(args.narr)
    captions, total = build_captions(narr)
    windows = section_windows(narr, total)
    cuts = make_cuts(windows, manifest)
    hook = make_hook(manifest)
    figures = place_figures(windows, total)
    write_srt(captions, args.captions)
    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": "caniglia_dryrun/audio/silence.m4a",
        "narrationSeconds": round(total, 3),
        "hookSeconds": 0.0,
        "hookLine": "Can the police cross your threshold to help?",
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
        "factory": sum(1 for c in cuts if "/factory/" in c["src"].replace("\\", "/")),
        "motion": sum(1 for c in cuts if "/motion/" in c["src"].replace("\\", "/")),
        "stills": sum(1 for c in cuts if c["kind"] == "img"),
        "distinct_assets": len(uses),
        "first_use_share": round(len(uses) / len(cuts), 4),
        "still_time_share": round(still_time / total, 4),
        "motion_time_share": round(motion_time / total, 4),
        "figures": len(figures),
    }
    BUILD_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    BUILD_MANIFEST.write_text(json.dumps({"episode_id": EP, "producer": "scripts/build_caniglia_film.py", "inputs": {"assets": str(args.assets), "narr": str(args.narr)}, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    BEATSHEET.write_text(json.dumps({"schema_version": "caniglia_beatsheet.v1", "episode_id": EP, "figures": figures, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

