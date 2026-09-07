#!/usr/bin/env python
"""Build remotion/src/data/cleveland_film.json for EP45 from an asset manifest."""
from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-045-cleveland"
SLUG = "cleveland"
FPS = 30
DEFAULT_ASSETS = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
DEFAULT_NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
DEFAULT_OUT = ROOT / "remotion" / "src" / "data" / "cleveland_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "cleveland" / "film_data.v001.json"
BUILD_MANIFEST = ROOT / "episodes" / EP / "04_scenes" / "cleveland_build_manifest.v001.json"
BEATSHEET = ROOT / "episodes" / EP / "04_scenes" / "cleveland_beatsheet.v001.json"
DEFAULT_SRT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"

SECTION_TARGETS = {
    # factory, motion, still. Totals: 92 / 32 / 100 = 224 cuts.
    "HOOK": (6, 2, 5),
    "OP": (3, 2, 10),
    "ACT_1": (12, 6, 14),
    "ACT_2": (19, 8, 22),
    "ACT_3": (33, 8, 30),
    "ENDING": (19, 6, 19),
}
SECTION_ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ENDING"]
VALID_KINDS = {"numberticker", "stat", "votetally", "timeline", "quote", "kinetic", "lowerthird", "acttitle", "compbars", "bar", "mechanism", "regionmap", "pindropmap", "routemap"}


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
            cut = {"id": f"cut-{len(cuts):03d}", "start": round(t, 3), "dur": dur, "kind": kind, "src": src, "seed": f"cleveland-{len(cuts):03d}", "act": sec}
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
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": src, "seed": f"cleveland-hook-{i:02d}"})
        t += d
    return hook


def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def figure_payloads() -> list[dict]:
    return [
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction"},
        K(["THE PRICE", "OF BEING POOR"], ["POOR"], "emphasis"),
        {"kind": "pindropmap", "pins": [{"x": 0.55, "y": 0.56, "label": "Montgomery, Alabama"}]},
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "an intake door closes"},
        {"kind": "acttitle", "title": "THE ROAD THAT ENDS AT A CELL", "kicker": "ACT ONE", "index": 1},
        {"kind": "routemap", "label": "license suspended - driving continues - more tickets - order - intake"},
        {"kind": "stat", "value": 1554, "prefix": "$", "label": "or 31 days - per Fines & Fees Justice Center"},
        {"kind": "numberticker", "value": 31, "suffix": " days", "label": "before release"},
        {"kind": "stat", "value": 1, "label": "no ability-to-pay hearing before jail"},
        {"kind": "compbars", "items": [{"label": "debt sits", "value": 1}, {"label": "fees grow", "value": 2}]},
        {"kind": "timeline", "events": [{"year": "ticket", "text": "unpaid fines"}, {"year": "license", "text": "suspended"}, {"year": "$1,554", "text": "or 31 days, FFJC"}]},
        {"kind": "bar", "items": [{"label": "license", "value": 1}, {"label": "work", "value": 0}, {"label": "debt", "value": 2}]},
        {"kind": "acttitle", "title": "THE MACHINE", "kicker": "ACT TWO", "index": 2},
        {"kind": "lowerthird", "primary": "Judicial Correction Services", "secondary": "offender-funded probation, founded 2001 in Georgia"},
        {"kind": "compbars", "items": [{"label": "$200 per month", "value": 200}, {"label": "$40 to the company - FFJC", "value": 40}]},
        {"kind": "bar", "items": [{"label": "$40 monthly company fee", "value": 40}, {"label": "fine balance", "value": 200}]},
        {"kind": "mechanism", "mechanism": "gears", "label": "court - company - monthly fee"},
        {"kind": "mechanism", "mechanism": "gears", "label": "ability-to-pay judgment outsourced to the fee collector"},
        {"kind": "stat", "value": 38000, "prefix": "~", "label": "people across four states by 2013"},
        {"kind": "regionmap", "label": "four states, not every state", "regions": ["AL", "GA", "MS", "FL"]},
        {"kind": "stat", "value": 100, "suffix": "+", "label": "Alabama courts by 2013"},
        {"kind": "quote", "quote": "a judicially sanctioned extortion racket", "attribution": "Judge Hub Harrington"},
        {"kind": "acttitle", "title": "BEARDEN", "kicker": "ACT THREE", "index": 3},
        {"kind": "timeline", "events": [{"year": "1970", "text": "Williams"}, {"year": "1971", "text": "Tate"}, {"year": "1983", "text": "Bearden ability-to-pay rule; enforcement failed"}]},
        {"kind": "lowerthird", "primary": "Bearden v. Georgia, 461 U.S. 660 (1983)", "secondary": "ability-to-pay rule; the rule held, enforcement failed"},
        {"kind": "lowerthird", "primary": "Williams v. Illinois, 399 U.S. 235 (1970)", "secondary": "Tate v. Short, 401 U.S. 395 (1971)"},
        {"kind": "quote", "quote": "it is fundamentally unfair to revoke his probation automatically, without even considering whether an adequate alternative to prison exists", "attribution": "Justice O'Connor, for the Court"},
        {"kind": "compbars", "items": [{"label": "closed: jail for inability with no hearing", "value": 1}, {"label": "still allowed: fines, fees, restitution", "value": 1}]},
        {"kind": "lowerthird", "primary": "Fourteenth Amendment", "secondary": "due process and equal protection converge"},
        {"kind": "compbars", "items": [{"label": "$500 fine", "value": 500}, {"label": "$250 restitution", "value": 250}]},
        {"kind": "mechanism", "mechanism": "faultsplit", "left": "empty counsel chair", "right": "could she pay?"},
        K(["UNCONSTITUTIONAL SINCE 1983", "YET IT CONTINUED"], ["CONTINUED"], "emphasis"),
        {"kind": "stat", "value": 2014, "label": "settled in a lower court, not the Supreme Court"},
        {"kind": "timeline", "events": [{"year": "2014", "text": "lower court settlement, not the Supreme Court"}, {"year": "2015", "text": "SPLC RICO suit"}, {"year": "2015", "text": "JCS Alabama operations closed"}]},
        {"kind": "numberticker", "value": 2014, "label": "settled - lower court, not the Supreme Court"},
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction"},
    ]


def place_figures(windows: dict[str, tuple[float, float]], total: float) -> list[dict]:
    section_counts = [("HOOK", 4), ("ACT_1", 8), ("ACT_2", 10), ("ACT_3", 9), ("ENDING", 5)]
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
        raise SystemExit("EP45 requires a real asset manifest: is_stub must be false")
    narr = load_json(args.narr)
    captions, total = build_captions(narr)
    windows = section_windows(narr, total)
    cuts = make_cuts(windows, manifest)
    hook = make_hook(manifest)
    figures = place_figures(windows, total)
    total_frames = round(0.0 * FPS) + round(3.5 * FPS) + int(total * FPS + 0.999999) + round(9.0 * FPS)
    if total_frames / FPS > 750.0:
        raise SystemExit(f"duration too long: {total_frames / FPS:.3f}s > 750.0s")
    counts = {
        "factory": sum(1 for c in cuts if "/factory/" in c["src"].replace("\\", "/")),
        "motion": sum(1 for c in cuts if "/motion/" in c["src"].replace("\\", "/")),
        "stills": sum(1 for c in cuts if c["kind"] == "img"),
    }
    expected = {"factory": 92, "motion": 32, "stills": 100}
    if counts != expected or len(cuts) != 224:
        raise SystemExit(f"cut allocation mismatch: cuts={len(cuts)} counts={counts} expected={expected}")
    write_srt(captions, args.captions)
    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": str(narr.get("audio_path") or "cleveland/audio/narration_master.v001.mp3"),
        "narrationSeconds": round(total, 3),
        "hookSeconds": 8.0,
        "hookLine": "Can a court jail you for money you do not have?",
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
    BUILD_MANIFEST.write_text(json.dumps({"episode_id": EP, "producer": "scripts/build_cleveland_film.py", "inputs": {"assets": str(args.assets), "narr": str(args.narr)}, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    BEATSHEET.write_text(json.dumps({"schema_version": "cleveland_beatsheet.v1", "episode_id": EP, "figures": figures, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


