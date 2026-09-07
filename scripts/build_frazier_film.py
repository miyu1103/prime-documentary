#!/usr/bin/env python3
"""Build remotion/src/data/frazier_film.json from an EP39 asset manifest.

The same code path consumes both the stub manifest and the final asset manifest.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-039-frazier"
SLUG = "frazier"
FPS = 30
DUR_CYCLE = [1.7, 2.1, 5.6, 1.8, 3.0, 6.5, 2.0, 1.6, 4.2, 2.4, 5.2, 1.9]
FIGURE_KINDS = [
    "numberticker",
    "timeline",
    "bar",
    "kinetic",
    "acttitle",
    "lowerthird",
    "dochighlight",
    "routemap",
    "pindropmap",
    "regionmap",
    "compbars",
    "mechanism",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def body_seconds(annotated: dict, captions: dict) -> float:
    cues = captions.get("cues") or captions.get("captions") or []
    if isinstance(cues, list) and cues:
        return float(max(c.get("end", 0) for c in cues))
    spans = annotated.get("spans") or []
    if spans:
        return float(max(s.get("end", 0) for s in spans))
    return 705.0


def normalize_captions(captions: dict) -> list[dict]:
    cues = captions.get("cues") or captions.get("captions") or []
    out = []
    for c in cues:
        text = str(c.get("text") or "").strip()
        if not text:
            continue
        out.append({"start": round(float(c["start"]), 3), "end": round(float(c["end"]), 3), "text": text})
    return out


def qc_assets(manifest: dict) -> dict[str, list[dict]]:
    groups = {"still": [], "factory": [], "motion": []}
    for a in manifest.get("assets") or []:
        if not (a.get("qc") or {}).get("pass", False):
            continue
        kind = a.get("kind")
        if kind in groups and a.get("public_path"):
            groups[kind].append(a)
    for kind in groups:
        groups[kind].sort(key=lambda x: x["asset_id"])
    return groups


def cut_grid(total: float) -> list[tuple[float, float]]:
    grid = []
    t = 0.0
    i = 0
    while t < total - 0.25:
        dur = DUR_CYCLE[i % len(DUR_CYCLE)]
        if t + dur > total:
            dur = total - t
        grid.append((round(t, 3), round(dur, 3)))
        t += dur
        i += 1
    return grid


def positions(n: int, k: int, offset: int = 0) -> set[int]:
    if k <= 0:
        return set()
    return {min(n - 1, (i * n) // k + offset) for i in range(k)}


def assign_assets(groups: dict[str, list[dict]], total: float, overlays: list[dict]) -> list[dict]:
    grid = cut_grid(total)
    n = len(grid)
    factory = deque(groups["factory"])
    motion = deque(groups["motion"] * 2)
    still = deque(groups["still"] * 2)
    long_slots = sorted(range(n), key=lambda idx: grid[idx][1], reverse=True)
    video_by_pos: dict[int, dict] = {}
    for pos in long_slots:
        if factory:
            picked = factory.popleft()
        elif motion:
            picked = motion.popleft()
        else:
            break
        video_by_pos[pos] = picked
    overlay_pool = [o for o in overlays if o.get("public_path")]
    cuts = []
    for i, (start, dur) in enumerate(grid):
        picked = None
        if i in video_by_pos:
            picked = video_by_pos[i]
            kind = "footage"
            treatment = "footage" if picked["kind"] == "factory" else "motion"
        elif still:
            picked = still.popleft()
            kind = "img"
            treatment = ["depth", "scan", "duotone", "focus"][(i // 2) % 4]
        elif factory:
            picked = factory.popleft()
            kind = "footage"
            treatment = "footage"
        elif motion:
            picked = motion.popleft()
            kind = "footage"
            treatment = "motion"
        else:
            break
        cut = {
            "start": start,
            "dur": dur,
            "kind": kind,
            "src": picked["public_path"],
            "seed": f"frazier-{i}",
            "treatment": treatment,
            "scene_code": picked.get("scene_code"),
            "asset_id": picked.get("asset_id"),
        }
        if kind == "img" and picked.get("depth_map"):
            cut["depth"] = picked["depth_map"]
        if kind == "img" and overlay_pool:
            overlay = overlay_pool[i % len(overlay_pool)]
            previous = cuts[-1].get("overlay") if cuts else None
            if overlay["public_path"] == previous:
                overlay = overlay_pool[(i + 1) % len(overlay_pool)]
            cut["overlay"] = overlay["public_path"]
            cut["blendHint"] = overlay.get("blend_hint") or "add"
            cut["overlayDuration"] = float(overlay.get("duration_sec") or dur)
        cuts.append(cut)
    return cuts


def figure_payload(kind: str, start: float, end: float, idx: int) -> dict:
    base = {"start": round(start, 3), "end": round(end, 3), "kind": kind}
    if kind == "numberticker":
        return {**base, "value": 16, "suffix": " YEARS", "label": "TIME LOST"}
    if kind == "timeline":
        return {**base, "events": [{"year": "1969", "text": "RULE"}, {"year": "2003", "text": "DNA"}, {"year": "2021", "text": "MATCH"}]}
    if kind == "bar":
        # ledger-only values (C-19 OST): 29% false confession / 62% mistaken eyewitness ID.
        return {**base, "data": [{"label": "FALSE CONFESSION", "value": 29}, {"label": "EYEWITNESS ID", "value": 62}]}
    if kind == "kinetic":
        return {**base, "lines": ["THE ROOM", "CHANGES THE STORY"], "style": "maskslide", "emphasisWords": ["ROOM"]}
    if kind == "acttitle":
        # acttitle beats fall every 12th figure (idx 5,17,29,41); advance the act each time
        # so the four cards read ACT 1..4 instead of all "ACT 1".
        act_no = ((idx - 1) // 12) % 4 + 1
        return {**base, "title": f"ACT {act_no}", "kicker": "FRAZIER", "index": act_no}
    if kind == "lowerthird":
        return {**base, "primary": "ILLUSTRATIVE REENACTMENT", "secondary": "AI-assisted visualization"}
    if kind == "dochighlight":
        return {**base, "rects": [{"x": 0.18, "y": 0.36, "w": 0.64, "h": 0.08}], "mode": "redact"}
    if kind == "routemap":
        return {**base, "pins": [{"x": 0.25, "y": 0.58, "label": "HOME"}, {"x": 0.66, "y": 0.42, "label": "ROOM"}]}
    if kind == "pindropmap":
        return {**base, "pins": [{"x": 0.35, "y": 0.5, "label": "1987"}, {"x": 0.62, "y": 0.45, "label": "2003"}]}
    if kind == "regionmap":
        return {**base, "label": "STATE RULES", "pattern": "varied"}
    if kind == "compbars":
        return {**base, "items": [{"label": "ADULTS", "value": 10}, {"label": "YOUTH", "value": 34}]}
    if kind == "mechanism":
        return {**base, "mechanism": ["closingdoor", "gears", "faultsplit"][idx % 3]}
    return base


def build_figures(total: float) -> list[dict]:
    figures = []
    # 42 beats, 5.4s each, spread across the body. Coverage target is 226s+.
    step = max(12.0, (total - 12.0) / 42)
    for i in range(42):
        start = 6.0 + i * step
        end = min(total - 1.0, start + 5.4)
        kind = FIGURE_KINDS[i % len(FIGURE_KINDS)]
        figures.append(figure_payload(kind, start, end, i + 1))
    return figures


def build_hook(groups: dict[str, list[dict]]) -> list[dict]:
    hero = [a["public_path"] for a in groups["still"][:6]]
    hook = []
    t = 0.0
    for i, src in enumerate(hero):
        hook.append({"start": round(t, 3), "dur": 1.34, "kind": "img", "src": src, "seed": f"hook-{i}"})
        t += 1.34
    return hook


def write_premium_beatsheet(out: Path, film: dict) -> None:
    epdir = ROOT / "episodes" / EP
    bs_path = epdir / "04_scenes" / "premium_beatsheet.v001.json"
    stub_bs_path = epdir / "04_scenes" / "premium_beatsheet.v001.stub.json"
    bs_path.parent.mkdir(parents=True, exist_ok=True)
    beats = []
    for i, c in enumerate(film["cuts"]):
        if c["kind"] == "img":
            kind = "hero"
            comp = "WilliamsScene"
        else:
            kind = "factory"
            comp = "FactoryClip"
        beats.append(
            {
                "id": f"cut-{i:03d}",
                "kind": kind,
                "component": comp,
                "start_frame": int(round(c["start"] * FPS)),
                "dur_frames": int(round(c["dur"] * FPS)),
                "src": c["src"],
            }
        )
    for i, f in enumerate(film["figures"]):
        beats.append(
            {
                "id": f"fig-{i:03d}",
                "kind": "mg_hero" if f["kind"] != "acttitle" else "act_title",
                "component": f"FigureBeats:{f['kind']}",
                "start_frame": int(round(f["start"] * FPS)),
                "dur_frames": int(round((f["end"] - f["start"]) * FPS)),
            }
        )
    payload = {"episode_id": EP, "meta": {"fps": FPS}, "beats": beats}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    bs_path.write_text(text, encoding="utf-8")
    stub_bs_path.write_text(text, encoding="utf-8")


def validate_caps(cuts: list[dict]) -> None:
    uses = Counter(c["src"] for c in cuts)
    for src, n in uses.items():
        low = src.lower()
        cap = 1 if "/factory/" in low else 2
        if n > cap:
            raise SystemExit(f"asset reuse cap exceeded: {src} {n}>{cap}")
    first_share = len(uses) / len(cuts)
    if first_share < 0.70:
        raise SystemExit(f"first-use share {first_share:.3f}<0.70")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--annotated", type=Path, required=True)
    ap.add_argument("--captions", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    manifest = load_json(args.manifest)
    annotated = load_json(args.annotated)
    captions = load_json(args.captions)
    groups = qc_assets(manifest)
    missing = [k for k, v in groups.items() if not v]
    if missing:
        raise SystemExit(f"manifest lacks qc-passing assets for: {', '.join(missing)}")
    total = body_seconds(annotated, captions)
    cuts = assign_assets(groups, total, manifest.get("overlays") or [])
    validate_caps(cuts)
    hook = build_hook(groups)
    figures = build_figures(total)
    film = {
        "episode_id": EP,
        "fps": FPS,
        "narration": f"{SLUG}/narration.mp3",
        "narrationSeconds": round(total, 3),
        "hookSeconds": round(sum(h["dur"] for h in hook), 3),
        "hookLine": "Police can lie in the interrogation room.",
        "hook": hook,
        "cuts": cuts,
        "captions": normalize_captions(captions),
        "graphics": [],
        "figures": figures,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "remotion" / "public" / SLUG / "film_data.v001.json").write_text(
        json.dumps(film, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_premium_beatsheet(args.out, film)
    print(
        json.dumps(
            {
                "ok": True,
                "out": str(args.out),
                "cuts": len(cuts),
                "distinct_assets": len(set(c["src"] for c in cuts)),
                "figures": len(figures),
                "narrationSeconds": film["narrationSeconds"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
