"""Inject a rich, VARIED set of animated figures into EP38 film_data (owner: 'アニメがない';
gate motion_density FAIL: 12 kinetic-only figures). Replaces the figures[] with ~24 beats
across 7 distinct FigureBeats kinds (acttitle / lowerthird / numberticker / cashstack /
mechanism / thresholdmeter / returnledger) at CaseFilm-timeline seconds (narration + hook/OP
offset). Writes both public/kidsforcash/film_data.v001.json and src/data/kidsforcash_film.json."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
PUB = ROOT / "remotion" / "public" / "kidsforcash" / "film_data.v001.json"
SRC = ROOT / "remotion" / "src" / "data" / "kidsforcash_film.json"
OFF = 11.533  # film time = narration time + hook(8.033) + OPENING_SEC(3.5)


def N(narr: float) -> float:
    return round(narr + OFF, 3)


def fig(kind, narr, dur, **kw):
    return {"start": N(narr), "end": round(N(narr) + dur, 3), "kind": kind, **kw}


# narration-time anchors (seconds) drawn from the card/section beats
FIGURES = [
    # act titles (4)
    fig("acttitle", 28.5, 5.5, title="ORDINARY CHILDREN"),
    fig("acttitle", 138.0, 5.5, title="FOLLOW THE MONEY"),
    fig("acttitle", 258.5, 5.5, title="ONE FAMILY"),
    fig("acttitle", 336.5, 5.5, title="THE RECKONING"),
    # lower thirds — names (6)
    fig("lowerthird", 46.0, 5.0, primary="MARK CIAVARELLA", secondary="Juvenile Court Judge"),
    fig("lowerthird", 146.0, 5.0, primary="MICHAEL CONAHAN", secondary="President Judge"),
    fig("lowerthird", 182.0, 5.0, primary="ROBERT POWELL", secondary="Owner, PA Child Care"),
    fig("lowerthird", 263.0, 5.0, primary="EDWARD KENZAKOSKI", secondary="Seventeen years old"),
    fig("lowerthird", 292.0, 5.0, primary="SANDY FONZO", secondary="His mother"),
    fig("lowerthird", 398.0, 5.0, primary="JUVENILE LAW CENTER", secondary="Philadelphia"),
    # number tickers (5)
    fig("numberticker", 11.7, 6.0, value=90, suffix=" SEC", topLabel="THE HEARING", label="NO LAWYER"),
    fig("numberticker", 51.0, 6.0, value=3, suffix=" MONTHS", topLabel="FOR A PRANK"),
    fig("numberticker", 224.0, 6.0, value=11, prefix="7–", suffix="×", topLabel="NO-LAWYER RATE"),
    fig("numberticker", 442.0, 6.0, value=17.5, decimals=1, suffix=" YRS", topLabel="CONAHAN"),
    fig("numberticker", 457.0, 6.0, value=28, suffix=" YEARS", topLabel="CIAVARELLA"),
    # cash stacks (2)
    fig("cashstack", 196.5, 6.5, amount=2800000, caption="$2.8M IN KICKBACKS"),
    fig("cashstack", 461.5, 6.5, amount=200000000, caption="$200M TO THE FAMILIES"),
    # comparison meter (1) — 8.4% statewide vs ~50% in his court
    fig("thresholdmeter", 82.5, 8.0),
    # mechanisms (3)
    fig("mechanism", 104.0, 6.5, mechanism="closingdoor"),   # the side door / county center shut
    fig("mechanism", 168.0, 6.5, mechanism="gears"),          # the machine / inventory
    fig("mechanism", 235.5, 6.5, mechanism="faultsplit"),     # inventory / system split
    # records vacated (1)
    fig("returnledger", 409.0, 6.5, caption="THOUSANDS OF CONVICTIONS VACATED"),
    # extra beats to clear the density/coverage floors (>=2.5/min, >=25%)
    fig("lowerthird", 4.5, 5.0, primary="LUZERNE COUNTY", secondary="Pennsylvania"),
    fig("numberticker", 358.0, 5.5, value=2251, topLabel="CONVICTIONS", label="VACATED"),
    fig("mechanism", 300.0, 6.0, mechanism="gears"),
    fig("acttitle", 478.5, 5.0, title="WHAT IT COSTS"),
    fig("numberticker", 62.0, 5.5, value=50, suffix="%", topLabel="IN HIS COURT", label="SENT AWAY"),
]


def main() -> int:
    d = json.loads(PUB.read_text(encoding="utf-8"))
    old = len(d.get("figures", []))
    figs = sorted(FIGURES, key=lambda f: f["start"])
    kinds = sorted({f["kind"] for f in figs})
    total_cov = sum(f["end"] - f["start"] for f in figs)
    d["figures"] = figs
    for p in (PUB, SRC):
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(p)
    print(f"figures: {old} -> {len(figs)}  kinds={kinds} ({len(kinds)} distinct)")
    print(f"animated coverage ~{total_cov:.0f}s over 552s body ({100*total_cov/540:.0f}% of body)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
