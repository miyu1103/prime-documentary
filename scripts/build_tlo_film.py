#!/usr/bin/env python
"""Build remotion/src/data/tlo_film.json for EP46 (New Jersey v. T.L.O.) from an asset manifest.

Cloned from scripts/build_cleveland_film.py (EP45). The allocate/tile_window/build_captions/
place_figures LOGIC is unchanged; only the episode constants, the narration/audio paths, and the
figure payloads (the T.L.O. §6 deck) are swapped. Real assets only; footage is mixed in from the
start (factory 92 + motion 32) so the plan is not a 紙芝居.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-046-tlo"
SLUG = "tlo"
FPS = 30
DEFAULT_ASSETS = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
DEFAULT_NARR = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
DEFAULT_OUT = ROOT / "remotion" / "src" / "data" / "tlo_film.json"
PUB_FILM = ROOT / "remotion" / "public" / "tlo" / "film_data.v001.json"
BUILD_MANIFEST = ROOT / "episodes" / EP / "04_scenes" / "tlo_build_manifest.v001.json"
BEATSHEET = ROOT / "episodes" / EP / "04_scenes" / "tlo_beatsheet.v001.json"
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
            cut = {"id": f"cut-{len(cuts):03d}", "start": round(t, 3), "dur": dur, "kind": kind, "src": src, "seed": f"tlo-{len(cuts):03d}", "act": sec}
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
        hook.append({"start": round(t, 3), "dur": d, "kind": "img", "src": src, "seed": f"tlo-hook-{i:02d}"})
        t += d
    return hook


def K(lines, emph=None, style="maskslide"):
    d = {"kind": "kinetic", "lines": lines, "style": style}
    if emph:
        d["emphasisWords"] = emph
    return d


def figure_payloads() -> list[dict]:
    # T.L.O. §6 deck: 36 figures, verified-ledger values only, no dochighlight, White verbatim only.
    # Ordered HOOK(4) / ACT_1(8) / ACT_2(9) / ACT_3(11) / ENDING(4) to match place_figures().
    return [
        # ---- HOOK (4) ----
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction - no real person depicted"},
        K(["THE BAG", "ON THE DESK"], ["BAG"], "emphasis"),
        {"kind": "pindropmap", "pins": [{"x": 0.30, "y": 0.40, "label": "New Jersey"}]},
        {"kind": "mechanism", "mechanism": "closingdoor", "label": "a restroom door swings shut"},
        # ---- ACT_1 (8) ----
        {"kind": "acttitle", "title": "THE SEARCH", "kicker": "ACT ONE", "index": 1},
        {"kind": "timeline", "events": [
            {"year": "restroom", "text": "two students found smoking"},
            {"year": "front office", "text": "sent to the vice principal"},
            {"year": "the purse", "text": "cigarettes, then rolling papers in view"},
            {"year": "juvenile court", "text": "motion to suppress denied; found delinquent"},
            {"year": "appeals", "text": "state high court suppressed; the Supreme Court reversed"},
        ]},
        {"kind": "lowerthird", "primary": "A 14-year-old freshman", "secondary": "known in the record only by her initials, T.L.O."},
        {"kind": "mechanism", "mechanism": "faultsplit", "label": "rolling papers in view - suspicion shifts"},
        {"kind": "routemap", "label": "the search widens, one step at a time", "pins": [
            {"x": 0.16, "y": 0.60, "label": "cigarettes"},
            {"x": 0.40, "y": 0.44, "label": "rolling papers"},
            {"x": 0.64, "y": 0.56, "label": "marijuana"},
            {"x": 0.86, "y": 0.48, "label": "evidence of dealing"},
        ]},
        {"kind": "bar", "items": [
            {"label": "cigarettes", "value": 1},
            {"label": "rolling papers", "value": 1},
            {"label": "pipe, empty bags", "value": 2},
            {"label": "cash, a list, two letters", "value": 2},
        ]},
        {"kind": "numberticker", "value": 14, "label": "a 14-year-old freshman"},
        {"kind": "stat", "value": 2, "label": "two students, one restroom, one broken rule", "topLabel": "WHERE IT BEGAN"},
        # ---- ACT_2 (9) ----
        {"kind": "acttitle", "title": "RIGHTS AT THE SCHOOLHOUSE", "kicker": "ACT TWO", "index": 2},
        {"kind": "lowerthird", "primary": "Does the Fourth Amendment apply inside a public school?", "secondary": "and if it does, by what standard?"},
        {"kind": "compbars", "items": [
            {"label": "ON THE STREET: WARRANT AND PROBABLE CAUSE", "value": 2},
            {"label": "IN SCHOOL: NO WARRANT, BUT THE FOURTH AMENDMENT STILL APPLIES", "value": 1},
        ]},
        K(["THE FOURTH AMENDMENT", "WALKS IN WITH YOU"], ["WITH YOU"], "emphasis"),
        {"kind": "stat", "value": 2, "label": "two easy answers the Court refused", "topLabel": "NOT NO RIGHTS, NOT FULL RIGHTS"},
        {"kind": "mechanism", "mechanism": "gears", "label": "two extremes rejected - a balance"},
        {"kind": "lowerthird", "primary": "The Fourth Amendment applies to public school officials", "secondary": "students do not shed their rights at the schoolhouse door"},
        {"kind": "compbars", "items": [
            {"label": "NOT NO RIGHTS", "value": 1},
            {"label": "NOT FULL RIGHTS", "value": 1},
        ]},
        {"kind": "stat", "value": 1, "label": "a lowered standard, not no standard", "topLabel": "REASONABLE SUSPICION"},
        # ---- ACT_3 (11) ----
        {"kind": "acttitle", "title": "REASONABLENESS", "kicker": "ACT THREE", "index": 3},
        {"kind": "votetally", "majority": 6, "dissent": 3, "label": "the Court reversed and upheld the search"},
        {"kind": "lowerthird", "primary": "New Jersey v. T.L.O.", "secondary": "469 U.S. 325 (1985)"},
        {"kind": "stat", "value": 469, "label": "U.S. Reports, page 325 - decided 1985", "topLabel": "THE CITATION"},
        {"kind": "compbars", "items": [
            {"label": "STREET: PROBABLE CAUSE", "value": 2},
            {"label": "SCHOOL: NO WARRANT, NO PROBABLE CAUSE, REASONABLE SUSPICION - STILL APPLIES", "value": 1},
        ]},
        {"kind": "quote", "quote": "reasonable grounds for suspecting that the search will turn up evidence that the student has violated or is violating either the law or the rules of the school", "attribution": "Justice White, for the Court"},
        {"kind": "quote", "quote": "reasonably related to the objectives of the search and not excessively intrusive in light of the age and sex of the student and the nature of the infraction", "attribution": "Justice White, for the Court"},
        {"kind": "stat", "value": 2, "label": "justified at its inception, reasonable in scope", "topLabel": "A TWO-PART TEST"},
        {"kind": "numberticker", "value": 1985, "label": "decided January 15, 1985"},
        {"kind": "mechanism", "mechanism": "faultsplit", "label": "inception then scope - each step builds on the last"},
        {"kind": "timeline", "events": [
            {"year": "1984", "text": "argued, then reargued"},
            {"year": "Jan 15, 1985", "text": "decided, 6-3"},
            {"year": "reversed", "text": "the state high court's suppression undone"},
        ]},
        # ---- ENDING (4) ----
        K(["NOT NO RIGHTS.", "NOT FULL RIGHTS."], ["RIGHTS"], "emphasis"),
        {"kind": "quote", "quote": "reasonably related in scope to the circumstances which justified the interference in the first place", "attribution": "Justice White, for the Court"},
        {"kind": "lowerthird", "primary": "When police step in, a higher standard can return", "secondary": "footnote 7 - this case is about school officials only"},
        {"kind": "lowerthird", "primary": "AI-assisted visualization", "secondary": "symbolic reconstruction - no real person depicted"},
    ]


def place_figures(windows: dict[str, tuple[float, float]], total: float) -> list[dict]:
    section_counts = [("HOOK", 4), ("ACT_1", 8), ("ACT_2", 9), ("ACT_3", 11), ("ENDING", 4)]
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
        raise SystemExit("EP46 requires a real asset manifest: is_stub must be false")
    # EP45-lesson guard: factory(92) and motion(16) must be populated or the film is a 紙芝居.
    if len(manifest.get("factory") or []) != 92:
        raise SystemExit(f"manifest factory[] must have 92 entries, has {len(manifest.get('factory') or [])}")
    if len(manifest.get("motion") or []) != 16:
        raise SystemExit(f"manifest motion[] must have 16 entries, has {len(manifest.get('motion') or [])}")
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
        "narration": str(narr.get("audio_path") or "tlo/audio/narration_master.v001.mp3"),
        "narrationSeconds": round(total, 3),
        "hookSeconds": 8.0,
        "hookLine": "A teacher searched her purse. Did the Fourth Amendment walk into that school with her?",
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
    BUILD_MANIFEST.write_text(json.dumps({"episode_id": EP, "producer": "scripts/build_tlo_film.py", "inputs": {"assets": str(args.assets), "narr": str(args.narr)}, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    BEATSHEET.write_text(json.dumps({"schema_version": "tlo_beatsheet.v1", "episode_id": EP, "figures": figures, "report": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
