"""Score an episode premise against the owner's rubric and return a build verdict.

The rubric, the gate, the bonuses and the series registry live in `config/pd_planning_os.*.json`;
this file contains no thresholds of its own, so raising or lowering the bar is a data change and
shows up in a diff.

Two rubric generations exist and both are supported, because v001 records a real decision and the
episodes scored under it must stay reproducible:

  v001 (2026-08-11 morning)  8 axes, raw total 100, gate GO/IMPROVE/NO-GO at 85/75.
  v002 (2026-08-11 evening)  11 axes summing 120 raw, normalised to 100, plus four +5 bonuses,
                             graded REJECT / RESERVE / PRODUCTION / PRIORITY / FLAGSHIP.

**v002 is the DEFAULT and therefore the binding gate**, switched by the owner on 2026-08-12. They
also settled the open arithmetic: the eleven axis weights sum to 120 while the directive calls the
total 100, and the owner chose the 100-point reading -- so the raw sum is normalised (raw x 100/120)
and the four +5 bonuses apply afterwards, giving the 120 ceiling the directive states.

`--os v001` still scores against the old 8-axis, 85-point rubric, because EP60-EP69 were judged by it
and those judgements must stay reproducible.

Why this exists as code rather than prose. A requirement written only in a document is a requirement
that does not run: the `[4a]` spec gate could never fire because of a grep that dropped its own
failure lines, and five of eight episodes were about to burn captions at the wrong offset because a
sidecar was trusted instead of measured. A premise rubric in a markdown file would go the same way.
So the gate is a command, and it comes BEFORE research -- a weak premise should cost an hour, not a
week.

The scores themselves are judgement, and this tool does not pretend otherwise: it takes them as
input, checks them for internal consistency, applies the gate, and writes an auditable record. What
it mechanises is the DECISION and the paper trail, not the taste.

Usage
  py -3.11 scripts/score_premise.py --show                        # print the rubric and the gate
  py -3.11 scripts/score_premise.py --score premise.json          # score one premise
  py -3.11 scripts/score_premise.py --score premise.json --emit   # ...and write the record
  py -3.11 scripts/score_premise.py --score premise.json --os v001

A premise file is:
  {
    "slug": "oroville",
    "working_title": "...",
    "one_line": "...",
    "contradiction": "no criminal charge, and the money is gone",
    "series_id": "S01",
    "title_archetype": "T2",
    "scores": {"personal_relevance": 12, "wtf_factor": 15, ...},
    "bonuses": ["specific_money_amount"],
    "justification": {"personal_relevance": "why 12 and not 15", ...}
  }
Every axis must be present, every score must carry a justification, and no score may exceed its
maximum. A missing justification is an error, not a default -- an unexplained 15 is how a rubric
becomes a rubber stamp. Under v002 the premise must also state its contradiction in one sentence,
because contradiction is the rubric's primary feature and a premise that cannot name one is weak
whatever the other axes say.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DEFAULT_OS = "v002"  # binding gate, switched by the owner on 2026-08-12 on the 100-point reading


def os_path(version: str) -> Path:
    return CONFIG_DIR / f"pd_planning_os.{version}.json"


def load_os(version: str) -> dict:
    p = os_path(version)
    if not p.is_file():
        available = ", ".join(sorted(f.stem.split(".")[-1] for f in CONFIG_DIR.glob("pd_planning_os.v*.json")))
        raise SystemExit(f"missing {p} -- the rubric lives there, not in this script. available: {available}")
    cfg = json.loads(p.read_text(encoding="utf-8"))
    cfg["_source"] = f"config/{p.name}"
    return cfg


def is_v2(cfg: dict) -> bool:
    """v002 introduced normalisation and graded tiers; v001 has a flat build/improve/discard gate."""
    return "flagship" in cfg["premise_score"]["gate"]


def normalise(cfg: dict, raw: float) -> int:
    ps = cfg["premise_score"]
    target = ps.get("normalise_to")
    raw_max = ps.get("raw_max") or sum(a["max"] for a in ps["axes"])
    if not target or raw_max == target:
        return int(round(raw))
    return int(round(raw * target / raw_max))


def verdict_for(cfg: dict, total: int) -> str:
    g = cfg["premise_score"]["gate"]
    if is_v2(cfg):
        for tier in ("flagship", "priority", "production", "reserve"):
            if total >= g[tier]:
                return tier.upper()
        return "REJECT"
    return "GO" if total >= g["build"] else ("IMPROVE" if total >= g["improve"] else "NO-GO")


def is_build(cfg: dict, verdict: str) -> bool:
    return verdict in ({"PRODUCTION", "PRIORITY", "FLAGSHIP"} if is_v2(cfg) else {"GO"})


def show(cfg: dict) -> None:
    ps = cfg["premise_score"]
    g = ps["gate"]
    b = cfg["brand"]
    print(f"RUBRIC {cfg['_source']}")
    print(f"BRAND  {b['one_line']}")
    if b.get("tagline"):
        print(f"       tagline: {b['tagline']}")
    print(f"       centre : {b['centre']}")
    print(f"       test   : {b['test']}\n")
    print(f"{'axis':22s} {'max':>4s}  question")
    print("-" * 104)
    for a in ps["axes"]:
        star = " *" if a["key"] == ps.get("primary_feature") else "  "
        print(f"{a['key']:22s} {a['max']:4d}{star} {a['question']}")
    print("-" * 104)
    raw_max = sum(a["max"] for a in ps["axes"])
    if is_v2(cfg):
        print(f"{'RAW TOTAL':22s} {raw_max:4d}   normalised to {ps['normalise_to']}")
        print("\nBONUSES -- added after normalisation")
        for x in ps["bonuses"]:
            print(f"  +{x['points']}  {x['key']:26s} {x['question']}")
        print(f"\nGATE   >= {g['flagship']:3d}  FLAGSHIP    {ps['gate_meaning']['flagship']}")
        print(f"       >= {g['priority']:3d}  PRIORITY    {ps['gate_meaning']['priority']}")
        print(f"       >= {g['production']:3d}  PRODUCTION  {ps['gate_meaning']['production']}")
        print(f"       >= {g['reserve']:3d}  RESERVE     {ps['gate_meaning']['reserve']}")
        print(f"       <= {g['reject']:3d}  REJECT      {ps['gate_meaning']['reject']}")
        print(f"\n  primary feature: {ps['primary_feature']} -- {ps['primary_feature_note']}")
    else:
        print(f"{'TOTAL':22s} {raw_max:4d}\n")
        print(f"GATE   >= {g['build']}  build")
        print(f"       {g['improve']}-{g['build'] - 1}  improve and re-score")
        print(f"       <= {g['discard']}  discard")
    print(f"\n  {ps['hard_rule']}\n")

    print("SERIES")
    for s in cfg["series"]:
        tags = []
        if s.get("flagship"):
            tags.append("flagship")
        if s.get("tier"):
            tags.append(s["tier"])
        tag = f"  [{', '.join(tags)}]" if tags else ""
        print(f"  {s['id']}  {s['name']:38s}{tag}")
        print(f"       {s['thesis']}")

    if cfg.get("title_archetypes"):
        print("\nTITLE ARCHETYPES -- twenty candidates come from these and no others")
        for t in cfg["title_archetypes"]:
            print(f"  {t['id']}  {t['name']:28s} {t['shape']}")
    elif cfg.get("title"):
        t = cfg["title"]
        print(f"\nTITLE  shape: {t['shape']}   candidates per episode: {t['candidates_per_episode']}")
        print(f"       verbs: {', '.join(t['verbs'])}")
        print(f"       avoid: {', '.join(t['avoid'])}")
        print(f"       pair : write both, ship {t['pair_rule']['default']}")

    if cfg.get("producibility_gate"):
        pg = cfg["producibility_gate"]
        th = pg["thresholds"]
        print(f"\nPRODUCIBILITY GATE -- runs after the score, before greenlight")
        print(f"  utilisation = clips_needed / clips_available in the topic's visual register")
        print(f"  green <= {th['green']:.2f}   amber <= {th['amber']:.2f}   red > {th['amber']:.2f}")

    if cfg.get("production_order"):
        print("\nPRODUCTION ORDER")
        for step in cfg["production_order"]:
            print(f"  {step}")
        print(f"\n  {cfg['order_note']}")


def score(cfg: dict, premise: dict) -> tuple[int, int, list[str], str, list[str]]:
    """Return (raw, total_after_bonuses, bonuses_awarded, verdict, problems)."""
    ps = cfg["premise_score"]
    axes = {a["key"]: a["max"] for a in ps["axes"]}
    given = premise.get("scores") or {}
    just = premise.get("justification") or {}
    problems: list[str] = []

    missing = [k for k in axes if k not in given]
    if missing:
        problems.append(f"no score given for: {', '.join(missing)}")
    for k, v in given.items():
        if k not in axes:
            problems.append(f"'{k}' is not an axis in this rubric ({cfg['_source']})")
            continue
        if not isinstance(v, (int, float)) or v < 0 or v > axes[k]:
            problems.append(f"{k}={v} is outside 0..{axes[k]}")
        if not str(just.get(k, "")).strip():
            problems.append(f"{k} scores {v} with no justification -- an unexplained score is a rubber stamp")

    sid = premise.get("series_id")
    if sid and sid not in {s["id"] for s in cfg["series"]}:
        problems.append(f"series_id '{sid}' is not in the registry of {cfg['_source']}")
    tid = premise.get("title_archetype")
    archetypes = {t["id"] for t in cfg.get("title_archetypes", [])}
    if tid and archetypes and tid not in archetypes:
        problems.append(f"title_archetype '{tid}' is not in the registry")

    # Only in-range values are summed. An out-of-range score is a rubric problem, not a large score:
    # counting it would let `contradiction: 99` carry a garbage premise to PRIORITY on the printout,
    # which is exactly the kind of green a reader remembers and an exit code does not fix.
    raw = sum(v for k, v in given.items()
              if k in axes and isinstance(v, (int, float)) and 0 <= v <= axes[k])
    total = normalise(cfg, raw)

    awarded: list[str] = []
    if is_v2(cfg):
        if not str(premise.get("contradiction", "")).strip():
            problems.append("no `contradiction` stated -- it is the rubric's primary feature and must be "
                            "one sentence, e.g. 'never charged with a crime, and the money is gone'")
        allowed = {x["key"]: x["points"] for x in ps["bonuses"]}
        for key in premise.get("bonuses") or []:
            if key not in allowed:
                problems.append(f"bonus '{key}' is not one of: {', '.join(allowed)}")
                continue
            awarded.append(key)
            total += allowed[key]

    # A score with rubric problems has no verdict. Reporting one invites it to be quoted.
    verdict = "INVALID" if problems else verdict_for(cfg, total)
    return int(raw), int(total), awarded, verdict, problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--show", action="store_true", help="print the rubric, gate, series and archetypes")
    ap.add_argument("--score", metavar="PREMISE_JSON", help="score a premise file")
    ap.add_argument("--emit", action="store_true", help="write the scored record beside the premise file")
    ap.add_argument("--os", default=DEFAULT_OS, metavar="VERSION",
                    help=f"planning-OS revision to score against (default {DEFAULT_OS})")
    args = ap.parse_args()

    cfg = load_os(args.os)
    if args.show or not args.score:
        show(cfg)
        return 0

    p = Path(args.score)
    premise = json.loads(p.read_text(encoding="utf-8"))
    raw, total, awarded, verdict, problems = score(cfg, premise)
    ps = cfg["premise_score"]
    g = ps["gate"]

    print(f"{premise.get('working_title') or premise.get('slug','(unnamed)')}")
    print(f"rubric {cfg['_source']}")
    if premise.get("contradiction"):
        print(f"contradiction: {premise['contradiction']}")
    print()
    print(f"{'axis':22s} {'score':>7s} {'max':>5s}  justification")
    print("-" * 112)
    for a in ps["axes"]:
        k = a["key"]
        v = (premise.get("scores") or {}).get(k, "-")
        j = str((premise.get("justification") or {}).get(k, ""))[:64]
        cell = f"{v:7d}" if isinstance(v, (int, float)) else f"{str(v):>7s}"
        print(f"{k:22s} {cell} {a['max']:5d}  {j}")
    print("-" * 112)
    raw_max = sum(a["max"] for a in ps["axes"])
    print(f"{'RAW':22s} {raw:7d} {raw_max:5d}")
    if is_v2(cfg):
        print(f"{'NORMALISED':22s} {normalise(cfg, raw):7d} {ps['normalise_to']:5d}")
        for key in awarded:
            pts = next(x["points"] for x in ps["bonuses"] if x["key"] == key)
            print(f"{'  bonus ' + key:22s} {'+' + str(pts):>7s}")
        print(f"{'TOTAL':22s} {total:7d}")
        print(f"\nVERDICT  {verdict}   (flagship>={g['flagship']} | priority>={g['priority']} | "
              f"production>={g['production']} | reserve>={g['reserve']} | reject<={g['reject']})")
        next_up = g["production"]
    else:
        print(f"\nVERDICT  {verdict}   (build >= {g['build']} | improve {g['improve']}-{g['build']-1} | "
              f"discard <= {g['discard']})")
        next_up = g["build"]

    if verdict != "INVALID" and not is_build(cfg, verdict):
        weak = sorted(((a["max"] - (premise.get("scores") or {}).get(a["key"], 0)), a["key"]) for a in ps["axes"])
        gap = next_up - total
        print(f"         {gap} point(s) below the build line. Largest gaps: " +
              ", ".join(f"{k} (-{d})" for d, k in weak[-3:][::-1] if d > 0))

    if problems:
        print("\nRUBRIC PROBLEMS -- these invalidate the score, fix them before trusting it:")
        for x in problems:
            print(f"  - {x}")

    if cfg.get("producibility_gate") and is_build(cfg, verdict):
        print("\nNEXT GATE  producibility -- measure the shelf's inventory for this topic's visual "
              "register\n           before greenlight. A build verdict is not a greenlight.")

    if args.emit:
        out = p.with_name(p.stem + ".scored.json")
        rec = dict(premise)
        rec["scored"] = {
            "raw": raw, "total": total, "bonuses_awarded": awarded,
            "verdict": verdict, "problems": problems,
            "rubric": cfg["_source"], "gate": g,
            "at": datetime.now(timezone.utc).isoformat(),
        }
        out.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nwrote {out}")

    # exit 0 only for a clean build verdict -- so this can sit in front of the design-doc gate
    return 0 if (is_build(cfg, verdict) and not problems) else 1


if __name__ == "__main__":
    raise SystemExit(main())
