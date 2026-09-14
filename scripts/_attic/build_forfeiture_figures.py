#!/usr/bin/env python3
r"""§5.6 Figures tier for EP28: turn the data beats into animated figures.

Rewrites remotion/src/data/forfeiture_film.json (+ public copy): the numeric/data beats are
MOVED out of `graphics` (flat kinetic text) into a new `figures` array (StatCounter counts up,
Timeline draws) that CaseFilm renders full-screen via FigureBeats. Idempotent.

    py -3.11 scripts/build_forfeiture_figures.py
"""
from __future__ import annotations
import io, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "remotion" / "src" / "data" / "forfeiture_film.json"
PUB = ROOT / "remotion" / "public" / "forfeiture" / "film_data.v001.json"

# match a beat by a substring in its first line -> the figure spec (timing pulled from the beat)
MAP = {
    "$40": {"kind": "stat", "value": 40, "prefix": "$", "decimals": 0,
            "topLabel": "He sold", "label": 'the entire "crime"'},
    "1,200+ HOMES": {"kind": "stat", "value": 50, "prefix": "$", "suffix": "M+", "decimals": 0,
                     "topLabel": "1,200+ homes · 2002–2018", "label": "seized in cash"},
    "$178": {"kind": "stat", "value": 178, "prefix": "$", "decimals": 0,
             "topLabel": "Philadelphia forfeiture", "label": "median cash seized"},
    "THE MONEY PAID THEIR OWN SALARIES": {"kind": "stat", "value": 6, "prefix": "$", "suffix": "M", "decimals": 0,
                                          "topLabel": "Kept by the D.A. & police", "label": "every single year"},
    "SOUROVELIS v. CITY OF PHILADELPHIA": {"kind": "timeline", "events": [
        {"year": "2014", "text": "$40 arrest · house seized"},
        {"year": "2014", "text": "Institute for Justice sues"},
        {"year": "2018", "text": "Consent decree"}]},
    "THE MACHINE WAS DISMANTLED": {"kind": "stat", "value": 3, "prefix": "$", "suffix": "M", "decimals": 0,
                                   "topLabel": "2018 consent decree", "label": "returned to victims"},
}


def apply(data: dict) -> dict:
    graphics = data.get("graphics", [])
    figures = []
    kept = []
    for b in graphics:
        first = (b.get("lines") or [""])[0]
        spec = next((v for k, v in MAP.items() if k in first), None)
        if spec is not None:
            figures.append({"start": b["start"], "end": b["end"], **spec})
        else:
            kept.append(b)
    data["graphics"] = kept
    data["figures"] = sorted(figures, key=lambda f: f["start"])
    return data


def main():
    for p in (SRC, PUB):
        if not p.exists():
            print(f"skip missing {p}"); continue
        d = json.load(io.open(p, encoding="utf-8"))
        d = apply(d)
        io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2))
        print(f"{p.name}: graphics={len(d['graphics'])} figures={len(d['figures'])}")
    print("figures:", [f"{f['kind']}@{f['start']:.0f}s" for f in json.load(io.open(SRC, encoding='utf-8'))['figures']])


if __name__ == "__main__":
    main()
