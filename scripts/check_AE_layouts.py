#!/usr/bin/env python3
"""Preflight gate: AE layout allowlist (phantom-layout crash guard).

EP48/EP49 burned lesson: the AE hero-card JSX ends with `else throw "unsupported
layout"`. If beats.json references a layout that is not implemented (or a Tier-B
layout that has not yet been proven with a `--dryrun --only` single-comp render),
the AfterFX build crashes mid-deck. DATE_STAMP and SEAM_TRANSITION were never
implemented in the cleveland source and are explicitly BANNED.

allowlist = {6 proven layouts}
          UNION {Tier-B layouts that have (a) an `else if (spec.layout === L)`
                 dispatch in the builder source AND (b) at least one dryrun proof
                 mp4 (>100KB) for a beat of that layout}

This gate scans the production beats.json and FAILS if any layout is outside that
allowlist, or if DATE_STAMP / SEAM_TRANSITION appear.

    py -3.11 scripts/check_AE_layouts.py --ep PD-2026-050-centralpark [--json]
Exit 0 = PASS, 1 = FAIL, 2 = missing inputs / schema.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROVEN = {"ACT_TITLE_CARD", "CENTER_STACK", "MONEY_STACK", "QUOTE_CARD",
          "VOTE_SPLIT", "SPLIT_COMPARE"}
TIER_B = {"DNA_LADDER", "STAT_RESOLVE", "CARD_STACK", "REC_LIGHT", "SCALE_TIP",
          "HERO_TIMELINE", "NAME_WALL", "SIGNATURE_ERASE"}
BANNED = {"DATE_STAMP", "SEAM_TRANSITION"}
MIN_PROOF_BYTES = 102400  # >100KB


def evaluate(ep: str) -> dict:
    epdir = ROOT / "episodes" / ep
    beats_path = epdir / "08_edit" / "ae_hero" / "beats.json"
    builder = ROOT / "scripts" / "ae" / "build_centralpark_hero_cards.py"
    proof_dir = epdir / "08_edit" / "_dryrun" / "ae_hero" / "render"

    errors: list[str] = []
    notes: list[str] = []

    if not beats_path.exists():
        return {"ok": False, "schema": False, "errors": [f"missing beats.json: {beats_path}"],
                "allowlist": sorted(PROVEN)}
    if not builder.exists():
        return {"ok": False, "schema": False, "errors": [f"missing builder: {builder}"],
                "allowlist": sorted(PROVEN)}

    doc = json.loads(beats_path.read_text(encoding="utf-8"))
    beats = doc.get("beats") or []
    src = builder.read_text(encoding="utf-8", errors="ignore")

    # group production beat ids by layout
    by_layout: dict[str, list[str]] = {}
    for b in beats:
        by_layout.setdefault(str(b.get("layout")), []).append(str(b.get("id")))

    # build the allowlist grounded in dispatch + dryrun proof mp4s
    allowlist = set(PROVEN)
    proven_tier_b: dict[str, str] = {}
    for layout in TIER_B:
        has_dispatch = bool(re.search(r'spec\.layout\s*===\s*"' + re.escape(layout) + r'"', src))
        proof = None
        for bid in by_layout.get(layout, []):
            mp4 = proof_dir / f"{bid}.mp4"
            if mp4.exists() and mp4.stat().st_size > MIN_PROOF_BYTES:
                proof = f"{mp4.name}({mp4.stat().st_size}B)"
                break
        if has_dispatch and proof:
            allowlist.add(layout)
            proven_tier_b[layout] = proof
        elif layout in by_layout:
            # referenced but not fully proven -> will be flagged below
            if not has_dispatch:
                notes.append(f"{layout}: referenced but no JSX dispatch in builder")
            if not proof:
                notes.append(f"{layout}: referenced but no dryrun proof mp4 (>100KB) in {proof_dir.name}")

    # per-beat verdicts
    seen_layouts = set()
    for b in beats:
        layout = str(b.get("layout"))
        seen_layouts.add(layout)
        if layout in BANNED:
            errors.append(f"{b.get('id')}: BANNED layout {layout} (never implemented -> else-throw crash)")
        elif layout not in allowlist:
            errors.append(f"{b.get('id')}: layout {layout} not in allowlist "
                          f"(not proven / phantom)")

    ae_total = len(beats)
    tier_b_used = sorted(l for l in seen_layouts if l in TIER_B)

    return {
        "ok": not errors,
        "schema": True,
        "ep": ep,
        "beats": ae_total,
        "allowlist": sorted(allowlist),
        "proven_tier_b": proven_tier_b,
        "tier_b_used": tier_b_used,
        "banned_present": sorted(seen_layouts & BANNED),
        "notes": notes,
        "errors": errors,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    r = evaluate(args.ep)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if r["ok"] else "FAIL") + f" check_AE_layouts: {args.ep}")
        print(f"  beats={r.get('beats')} allowlist={r.get('allowlist')}")
        if r.get("proven_tier_b"):
            print(f"  proven Tier-B: {r['proven_tier_b']}")
        for n in r.get("notes", []):
            print(f"  - {n}")
        for e in r.get("errors", [])[:30]:
            print(f"  ! {e}")
    if not r.get("schema", False):
        return 2
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
