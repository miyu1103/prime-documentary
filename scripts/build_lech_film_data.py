#!/usr/bin/env python
"""Build EP40 Lech CaseFilm data from an asset manifest and slot contract."""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BODY_OFFSET = 11.6

SECTIONS = [
    (11.6, 131.5, 14, 2, 21),
    (131.5, 303.6, 24, 3, 26),
    (303.6, 477.4, 20, 8, 26),
    (477.4, 673.1, 23, 3, 36),
    (673.1, 732.4, 4, 0, 16),
]


def words(text: str) -> list[str]:
    return re.findall(r"[\w'\-]+|[.,?!;:]", text)


def srt_time_to_sec(ts: str) -> float:
    h, m, rest = ts.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_srt(path: Path) -> list[dict]:
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        ts = next((l for l in lines if "-->" in l), None)
        if not ts:
            continue
        start, end = [x.strip() for x in ts.split("-->")]
        text = " ".join(lines[lines.index(ts) + 1:])
        cues.append({"start": srt_time_to_sec(start), "end": srt_time_to_sec(end), "text": text})
    return cues


def fallback_captions(slots: dict) -> list[dict]:
    texts = []
    texts.extend(slots["hook"]["lines"])
    for act in slots["acts"]:
        texts.append(act["narration"])
    ed = slots["ed"]
    texts.extend([ed["payoff_line"], ed["cta_line"], ed["question_line"]])
    all_words = " ".join(texts).split()
    cues = []
    dur = 720.8
    n = max(1, math.ceil(len(all_words) / 7))
    step = dur / n
    for i in range(n):
        chunk = all_words[i * 7:(i + 1) * 7]
        if chunk:
            cues.append({"start": round(i * step, 3), "end": round(min(dur, (i + 1) * step), 3), "text": " ".join(chunk)})
    return cues


def figure_specs(slots: dict) -> list[dict]:
    out = []
    for item in slots.get("figures", []):
        kind = item["kind"]
        base = {
            "start": round(float(item["start"]) - BODY_OFFSET, 3),
            "end": round(float(item["end"]) - BODY_OFFSET, 3),
            "kind": kind,
        }
        if kind == "lowerthird":
            base.update({"primary": item.get("primary") or f"LECH {item['id'].upper()}", "secondary": item.get("secondary") or "POLICE POWER"})
        elif kind == "stat":
            base.update({"value": item.get("value", 3), "label": item.get("label", "PEOPLE"), "topLabel": item.get("topLabel", "")})
        elif kind == "quote":
            base.update({"quote": item.get("quote", "The Tenth Circuit decision stands."), "attribution": item.get("attribution", "case record")})
        elif kind == "kinetic":
            base.update({"lines": item.get("lines", ["WHO PAYS WHEN THE STATE BREAKS IT?"]), "style": item.get("style", "emphasis"), "emphasisWords": item.get("emphasisWords", ["WHO"])})
        elif kind == "compbars":
            base.update({"items": item.get("items", [{"label": "CITY", "value": 1}, {"label": "FAMILY", "value": 3}])})
        elif kind == "mechanism":
            base.update({"mechanism": item.get("mechanism", "faultsplit")})
        elif kind == "routemap":
            base.update({"pins": item.get("pins", [{"x": 0.3, "y": 0.4, "label": "HOUSE"}])})
        out.append(base)
    return out


def pop_many(pool: list[dict], n: int, offset: int = 0) -> list[dict]:
    return [pool[(offset + i) % len(pool)] for i in range(n)]


def build_cuts(assets: dict) -> list[dict]:
    body = sorted([s for s in assets["stills"] if s["role"] == "body"], key=lambda x: (x.get("act", 0), x.get("scene_id", ""), x.get("asset_id", "")))
    factory = list(assets["factory"])
    motion = list(assets["motion"])
    still_seq = body + body[:55]  # 125 cuts from 70 stills: max 2 uses.
    cuts = []
    fi = mi = si = 0
    treatments = ["depth", "scan", "focus"]
    for start_abs, end_abs, nf, nm, ns in SECTIONS:
        start = start_abs - 11.6
        dur = end_abs - start_abs
        items = []
        items += [("factory", factory[fi + i]) for i in range(nf)]
        fi += nf
        items += [("motion", motion[mi + i]) for i in range(nm)]
        mi += nm
        items += [("still", still_seq[si + i]) for i in range(ns)]
        si += ns
        # Deterministic weave: keeps same kinds from clustering while preserving counts.
        ordered = []
        buckets = {k: [x for kk, x in items if kk == k] for k in ("factory", "motion", "still")}
        order = ["factory", "still", "factory", "motion", "still", "factory", "still"]
        while any(buckets.values()):
            progressed = False
            for k in order:
                if buckets[k]:
                    ordered.append((k, buckets[k].pop(0)))
                    progressed = True
            if not progressed:
                break
        weights = {"factory": 4.65, "motion": 3.30, "still": 2.00}
        weight_total = sum(weights[kind] for kind, _ in ordered)
        t = start
        for idx, (kind, item) in enumerate(ordered):
            cdur = dur * weights[kind] / weight_total
            cuts.append({
                "id": f"cut-{len(cuts):03d}",
                "start": round(t, 3),
                "dur": round(cdur, 3),
                "kind": "img" if kind == "still" else "footage",
                "src": item["public_path"],
                "treatment": treatments[len(cuts) % len(treatments)] if kind == "still" else "footage",
                "seed": f"lech-{len(cuts):03d}",
            })
            t += cdur
    assert len(cuts) == 226, len(cuts)
    return cuts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", required=True, type=Path)
    ap.add_argument("--slots", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--captions", type=Path)
    args = ap.parse_args()
    assets = json.loads(args.assets.read_text(encoding="utf-8"))
    slots = json.loads(args.slots.read_text(encoding="utf-8"))
    cuts = build_cuts(assets)
    body_stills = [s for s in assets["stills"] if s["role"] == "body"]
    hook = []
    hook_srcs = [s["public_path"] for s in body_stills[:4]]
    for i, src in enumerate(hook_srcs):
        hook.append({"start": round(i * (8.1 / len(hook_srcs)), 3), "dur": round(8.1 / len(hook_srcs), 3), "kind": "img", "src": src, "seed": f"hook-{i}"})
    captions = parse_srt(args.captions) if args.captions and args.captions.exists() else fallback_captions(slots)
    data = {
        "episode_id": "PD-2026-040-lech",
        "fps": 30,
        "narration": "lech_dryrun/audio/silence.m4a",
        "narrationSeconds": 720.8,
        "hookSeconds": 8.1,
        "hookLine": "Police destroyed a family's house. Then the law asked who pays.",
        "hook": hook,
        "cuts": cuts,
        "captions": captions,
        "graphics": [],
        "figures": figure_specs(slots),
        "externalKineticBeats": [
            {
                "id": beat["id"],
                "start": round(float(beat["start"]) - BODY_OFFSET, 3),
                "end": round(float(beat["end"]) - BODY_OFFSET, 3),
                "kind": f"ae:{beat['layout'].lower()}",
            }
            for beat in slots.get("beats", [])
        ],
        "overlays": assets.get("overlay", []),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {args.out} ({len(cuts)} cuts, {len(data['figures'])} figures, {len(captions)} captions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
