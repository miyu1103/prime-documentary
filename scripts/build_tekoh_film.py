#!/usr/bin/env python
"""Build remotion/src/data/tekoh_film.json for EP44 from an asset manifest."""
from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-044-tekoh"
SLUG = "tekoh"
FPS = 30
DEFAULT_ASSETS = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
DEFAULT_NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
DEFAULT_OUT = ROOT / "remotion" / "src" / "data" / "tekoh_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "tekoh" / "film_data.v001.json"
BUILD_MANIFEST = ROOT / "episodes" / EP / "04_scenes" / "tekoh_build_manifest.v001.json"
BEATSHEET = ROOT / "episodes" / EP / "04_scenes" / "tekoh_beatsheet.v001.json"
DEFAULT_SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"

SECTION_TARGETS = {
    # factory, motion, still. Totals: 93 / 32 / 101 = 226 cuts.
    "HOOK": (6, 2, 4),
    "OP": (3, 0, 7),
    "ACT_1": (12, 3, 12),
    "ACT_2": (16, 3, 16),
    "ACT_3": (44, 16, 41),
    "ENDING": (12, 8, 21),
}
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ENDING"]
VALID_KINDS = {"numberticker", "stat", "votetally", "timeline", "quote", "kinetic", "lowerthird", "acttitle", "compbars", "mechanism", "regionmap", "pindropmap"}


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
            cut = {"id": f"cut-{len(cuts):03d}", "start": round(t, 3), "dur": dur, "kind": kind, "src": src, "seed": f"tekoh-{len(cuts):03d}", "act": sec}
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
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": src, "seed": f"tekoh-hook-{i:02d}"})
        t += d
    return hook


def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def figure_payloads() -> list[dict]:
    return [
        K(["THE WORDS", "THEY NEVER READ YOU"], ["NEVER"], "emphasis"),
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction"},
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "a warning missing from the room"},
        {"kind": "acttitle", "title": "THAT NIGHT", "kicker": "ACT ONE", "index": 1},
        {"kind": "timeline", "events": [{"year": "2014", "text": "medical center, Los Angeles"}]},
        {"kind": "pindropmap", "pins": [{"x": 0.20, "y": 0.58, "label": "Los Angeles"}]},
        K(["NO WARNING", "CAME"], ["WARNING"], "wordpop"),
        {"kind": "lowerthird", "primary": "Deputy Carlos Vega", "secondary": "case participant, symbolic visuals only"},
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "a page between two people"},
        {"kind": "acttitle", "title": "THE TURN", "kicker": "ACT TWO", "index": 2},
        K(["THEY", "ACQUITTED HIM"], ["ACQUITTED"], "emphasis"),
        {"kind": "lowerthird", "primary": "42 U.S.C. section 1983", "secondary": "a civil door to seek accountability"},
        {"kind": "stat", "value": 2, "label": "civil trials - twice for the deputy"},
        {"kind": "timeline", "events": [{"year": "acquitted", "text": "criminal jury did not convict"}, {"year": "appeal", "text": "Ninth Circuit reversed and remanded"}]},
        K(["A CIVIL CLAIM", "FOR MONEY"], ["MONEY"], "emphasis"),
        {"kind": "mechanism", "mechanism": "gears", "label": "rule - broken - remedy"},
        {"kind": "lowerthird", "primary": "a private person, accused and cleared", "secondary": "underlying allegation not shown"},
        {"kind": "acttitle", "title": "THE DOCTRINE", "kicker": "ACT THREE", "index": 3},
        {"kind": "lowerthird", "primary": "Miranda v. Arizona, 384 U.S. 436 (1966)", "secondary": "still good law"},
        {"kind": "lowerthird", "primary": "Dickerson v. United States (2000)", "secondary": "Miranda stands"},
        {"kind": "timeline", "events": [{"year": "1966", "text": "Miranda"}, {"year": "2000", "text": "Dickerson"}, {"year": "2022", "text": "Vega v. Tekoh"}]},
        {"kind": "lowerthird", "primary": "Vega v. Tekoh, 597 U.S. 134 (2022)", "secondary": "No. 21-499"},
        {"kind": "votetally", "majority": 6, "dissent": 3, "label": "one door closed - exclusion stays open"},
        {"kind": "stat", "value": 6, "label": "Alito, for six of nine"},
        {"kind": "mechanism", "mechanism": "faultsplit", "left": "warning as fence", "right": "Fifth Amendment ground"},
        {"kind": "compbars", "items": [{"label": "the warning - a fence", "value": 1}, {"label": "the Fifth Amendment - the ground", "value": 1}]},
        K(["RULE", "BROKEN", "REMEDY"], ["REMEDY"], "wordpop"),
        K(["NOT", "SO SIMPLE"], ["NOT"], "emphasis"),
        {"kind": "lowerthird", "primary": "standing alone", "secondary": "no section 1983 damages for the missed warning"},
        {"kind": "stat", "value": 3, "label": "in dissent - Kagan, Breyer, Sotomayor"},
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "second door closed - exclusion door open"},
        K(["A RIGHT", "AND A REMEDY", "ARE NOT THE SAME"], ["REMEDY"], "emphasis"),
        {"kind": "lowerthird", "primary": "EXCLUSION STAYS OPEN", "secondary": "unwarned words can still be kept out"},
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction"},
        {"kind": "compbars", "items": [{"label": "the shield - still raised", "value": 1}, {"label": "the payment - not there to take", "value": 1}]},
        K(["RIGHT", "REMEDY", "RESULT"], ["REMEDY"], "wordpop"),
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "one narrow door closes"},
    ]


def place_figures(windows: dict[str, tuple[float, float]], total: float) -> list[dict]:
    section_counts = [("HOOK", 3), ("ACT_1", 6), ("ACT_2", 8), ("ACT_3", 15), ("ENDING", 5)]
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
        raise SystemExit("EP44 requires a real asset manifest: is_stub must be false")
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
        "narration": str(narr.get("audio_path") or "tekoh/audio/narration_master.v001.mp3"),
        "narrationSeconds": round(total, 3),
        "hookSeconds": 8.0,
        "hookLine": "If they never read you your rights, can you make them answer?",
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
    BUILD_MANIFEST.write_text(json.dumps({"episode_id": EP, "producer": "scripts/build_tekoh_film.py", "inputs": {"assets": str(args.assets), "narr": str(args.narr)}, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    BEATSHEET.write_text(json.dumps({"schema_version": "tekoh_beatsheet.v1", "episode_id": EP, "figures": figures, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

