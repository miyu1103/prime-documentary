#!/usr/bin/env python3
r"""Parse the FigureSpec union out of FigureBeats.tsx and validate a figure's PROPS, not just its kind.

WHY THIS EXISTS
---------------
2026-08-22, EP72/EP73. `pd_preflight` validated a figure's `kind` string and nothing else. Six new
figure cards were added to two filmconfigs, both films came back READY, and all six carried props
no component reads:

    timeline   declares  events: {year, text}[]     -- the config had items: {date, text}[]
    bar        declares  data | items: {label,value}[]  -- the config had series: [...]
    routemap   declares  pins: {x,y,label}[], label -- the config had from / to / note
    mechanism  declares  mechanism: 'closingdoor'|'gears'|'faultsplit'  -- the config had steps: []

Six blank figures, in a film the gate called ready to render. The kind was spelled correctly every
time, which is exactly why a kind-only check could not see it.

WHY IT PARSES THE .tsx INSTEAD OF LISTING THE PROPS HERE
--------------------------------------------------------
A hand-copied table is a second source of truth and it drifts. That is the same failure the gate's
own `VALID_KINDS` had: 17 kinds listed here against 38 rendered there, which blocked EP71 on
`casetimeline_c` -- a kind that shipped in five finished films. The union in FigureBeats.tsx is the
only thing the renderer actually obeys, so this reads it. A kind added to the component tomorrow is
understood by this checker today, with no edit.

WHAT IT CANNOT SEE
------------------
That a prop is present and well-typed, not that its VALUE is right. `pins: [{x: 9, y: 9}]` is
structurally valid and off-screen. Two frames per figure on the rendered contact sheet is still the
only thing that catches that.

    py -3.11 scripts/figure_spec.py --config episodes/_planning/EP72_lacmegantic_filmconfig.v001.json
    py -3.11 scripts/figure_spec.py --all
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TSX = ROOT / "remotion" / "src" / "components" / "FigureBeats.tsx"

# props every variant carries; the film builder writes them, a filmconfig never does
TIMING = {"start", "end", "kind"}


def _union_body(text: str) -> str:
    """The FigureSpec union, from `export type FigureSpec =` to the terminating `;`."""
    m = re.search(r"export type FigureSpec\s*=(.*?)\n\s*;", text, re.S)
    if not m:
        m = re.search(r"export type FigureSpec\s*=(.*?)\n(?=export |const |function )", text, re.S)
    if not m:
        raise SystemExit(f"[figspec] could not find the FigureSpec union in {TSX}")
    return m.group(1)


def spec() -> dict[str, dict[str, set[str]]]:
    """kind -> {'required': {...}, 'optional': {...}}, read from the component's own type union."""
    body = _union_body(TSX.read_text(encoding="utf-8"))
    # strip // and /* */ comments so a commented-out prop is not read as real
    body = re.sub(r"//[^\n]*", "", body)
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)

    out: dict[str, dict[str, set[str]]] = {}
    # each variant is a {...} block; they are separated by the union bar at brace depth 0
    variants, depth, buf = [], 0, ""
    for ch in body:
        if ch == "{":
            depth += 1
        if depth:
            buf += ch
        if ch == "}":
            depth -= 1
            if depth == 0:
                variants.append(buf)
                buf = ""
    for v in variants:
        km = re.search(r"kind:\s*'([a-z_]+)'", v)
        if not km:
            continue
        kind = km.group(1)
        req, opt = set(), set()
        # a prop is `name: type` or `name?: type`, at the top level of this variant
        inner = v[1:-1]
        depth2 = 0
        field = ""
        fields = []
        for ch in inner:
            if ch in "{[(":
                depth2 += 1
            elif ch in "}])":
                depth2 -= 1
            if ch == ";" and depth2 == 0:
                fields.append(field)
                field = ""
            else:
                field += ch
        fields.append(field)
        for f in fields:
            fm = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)(\??):", f)
            if not fm:
                continue
            name, q = fm.group(1), fm.group(2)
            if name in TIMING:
                continue
            (opt if q else req).add(name)
        out[kind] = {"required": req, "optional": opt}
    return out


def check_figure(fig: dict, table: dict) -> list[str]:
    """Everything wrong with one figure. Empty list means it will render with real content."""
    kind = fig.get("kind")
    if kind not in table:
        return [f"kind {kind!r} is not in the FigureSpec union -- the renderer will draw nothing"]
    want = table[kind]
    # BUILDER KEYS ARE NOT COMPONENT PROPS. `at_seconds`/`hold_seconds` pin a figure to one cut
    # and are consumed by build_case_film_generic before the payload ever reaches FigureBeats --
    # they exist because a bare-ground plate needs text ON IT, not somewhere in the act (EP71 O086,
    # EP76 V010). Underscore keys are notes. Neither reaches the renderer, so neither is a stray.
    BUILDER_KEYS = {"at_seconds", "hold_seconds"}
    have = {k for k in fig if k != "kind" and not k.startswith("_") and k not in BUILDER_KEYS}
    problems = []
    # `bar` is the one variant with a genuine either/or, expressed as two optionals
    missing = want["required"] - have
    if kind == "bar" and not (have & {"data", "items"}):
        problems.append("bar needs data or items: {label, value}[]")
    if missing:
        problems.append(f"missing required {sorted(missing)}")
    # A NUMBER CARD WITH A STRING VALUE RENDERS "NaN" IN 100-PIXEL TYPE. FigureBeats types both
    # `stat` and `numberticker` as `value: number`; "1,102 m" or "11,666" reaches the component as
    # a string and comes out NaN. EP76 morandi shipped five of them past every automated check --
    # black frames, runtime, loudness, animation density all green -- because a machine can see
    # that text is on screen and not that the text is broken. 29 cards across four configs.
    if kind in ("stat", "numberticker") and "value" in fig:
        if not isinstance(fig["value"], (int, float)) or isinstance(fig["value"], bool):
            problems.append(f"value must be a NUMBER, got {fig['value']!r} -- it will render NaN; "
                            f"put the unit in prefix/suffix")
    stray = have - want["required"] - want["optional"]
    if stray:
        problems.append(f"props no component reads {sorted(stray)} "
                        f"(valid here: {sorted(want['required'] | want['optional'])})")
    return problems


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, help="one filmconfig json")
    ap.add_argument("--all", action="store_true", help="every filmconfig in episodes/_planning")
    ap.add_argument("--list-kinds", action="store_true")
    a = ap.parse_args()

    table = spec()
    if a.list_kinds:
        for k in sorted(table):
            r, o = sorted(table[k]["required"]), sorted(table[k]["optional"])
            print(f"{k:16} required={r or '-'}  optional={o or '-'}")
        return 0

    targets: list[Path] = []
    if a.config:
        targets = [a.config]
    elif a.all:
        targets = sorted((ROOT / "episodes" / "_planning").glob("*filmconfig*.json"))
    else:
        print("give --config <file> or --all")
        return 2

    print(f"[figspec] {len(table)} kinds parsed from {TSX.name}")
    bad_files = 0
    for p in targets:
        try:
            cfg = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"  {p.name}: UNREADABLE ({e})")
            bad_files += 1
            continue
        rows = []
        for sec, items in (cfg.get("figures_by_section") or {}).items():
            for i, fig in enumerate(items or []):
                for msg in check_figure(fig, table):
                    rows.append(f"    {sec}[{i}] {fig.get('kind')}: {msg}")
        if rows:
            bad_files += 1
            print(f"  {p.name}: {len(rows)} problem(s)")
            for r in rows:
                print(r)
        else:
            n = sum(len(v or []) for v in (cfg.get("figures_by_section") or {}).values())
            print(f"  {p.name}: OK ({n} figures)")

    print(f"\n{'FAIL' if bad_files else 'PASS'} figure_shapes: "
          f"{bad_files} of {len(targets)} config(s) carry a figure the renderer cannot draw")
    print("  This checks STRUCTURE only. A pin at x=9 is structurally perfect and off-screen; "
          "only the rendered contact sheet catches that.")
    return 1 if bad_files else 0


if __name__ == "__main__":
    raise SystemExit(main())
