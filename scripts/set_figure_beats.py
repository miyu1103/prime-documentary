#!/usr/bin/env python3
"""Write a section->figure-beat map into an episode filmconfig, after checking every beat
against the renderer's own TypeScript union.

Why this exists: EP57/58/59 shipped filmconfigs carrying ONE placeholder beat per section
(10, 8 and 8 beats) where EP52-56 carry 78-88. EP57 rendered at 0.37 kinetic beats/min
against a floor of 2.5 and 3.3% animated coverage against 25% -- the gate called it
kamishibai, and it was right. Nothing was wrong with the renderer; the data was empty.

The validation is not a hand-maintained list. It is parsed out of
`remotion/src/components/FigureBeats.tsx`, from the discriminated union that the component
actually switches on, so a beat that names a field the renderer does not read, or omits one
it requires, is rejected here instead of rendering as a blank card two hours later.

    py -3.11 scripts/set_figure_beats.py --config episodes/_planning/EP57_..._filmconfig.v001.json \
                                         --beats path/to/beats.json [--dry-run]

Exit 0 = written (or, with --dry-run, would validate). Exit 1 = at least one bad beat; the
config is not touched.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
TSX = ROOT / "remotion" / "src" / "components" / "FigureBeats.tsx"
BUILDER = ROOT / "scripts" / "build_case_film_generic.py"


def builder_kinds() -> set[str]:
    """Kinds build_case_film_generic.py will actually accept.

    The renderer's union is wider than the builder's VALID_KINDS, and the builder also bans
    some kinds outright. Validating only against the renderer let EP63 and EP65 carry beats
    (brightline, dochighlight) that pass here and then raise SystemExit inside build_figures.
    Parsed from the builder rather than restated, so the two sets cannot drift apart again.
    """
    src = BUILDER.read_text(encoding="utf-8")

    def literals(name: str) -> set[str]:
        m = re.search(name + r"\s*=\s*\{(.*?)\}", src, re.S)
        if not m:
            return set()
        return {a or b for a, b in re.findall(r"\"([a-z_]+)\"|'([a-z_]+)'", m.group(1))}

    valid = literals("VALID_KINDS")
    if not valid:
        return set()          # builder changed shape; fall back to renderer-only checking
    return valid - literals("BANNED_FIGURE_KINDS")

# Fields every beat carries implicitly -- the builder assigns the timing, not the author.
IMPLICIT = {"start", "end"}


def union_schema() -> dict[str, tuple[set[str], set[str]]]:
    """{kind: (required fields, optional fields)} read from the renderer's union.

    Members are written either on one line

        | {start: number; end: number; kind: 'stat'; value: number; label: string}

    or spread over several lines

        | {
            start: number;
            ...
          }

    so the text is flattened before the members are split.
    """
    src = TSX.read_text(encoding="utf-8")
    # keep only the union body: from the first member to the closing of the type alias
    start = src.index("| {")
    body = src[start:]
    body = re.sub(r"//[^\n]*", "", body)              # strip line comments
    flat = re.sub(r"\s+", " ", body)

    # Split into TOP-LEVEL members with a depth counter. A non-greedy {...} regex matches the
    # INNER object of a member like `pins: {x: number; y: number}[]` first, which made every
    # nested field look like a required top-level one (pindropmap "missing required ['y']").
    members: list[str] = []
    depth, buf = 0, []
    for ch in flat:
        if ch == "{":
            depth += 1
            if depth == 1:
                buf = []
                continue
        elif ch == "}":
            depth -= 1
            if depth == 0:
                members.append("".join(buf))
                continue
        if depth >= 1:
            buf.append(ch)

    schema: dict[str, tuple[set[str], set[str]]] = {}
    for member in members:
        # a field whose type is itself an object contributes only its own name
        member = re.sub(r"\{[^{}]*\}", "OBJ", member)
        m = re.search(r"kind:\s*'([a-z0-9_]+)'", member)
        if not m:
            continue
        kind = m.group(1)
        req, opt = set(), set()
        for field in member.split(";"):
            fm = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)(\??):", field)
            if not fm:
                continue
            name, optional = fm.group(1), fm.group(2) == "?"
            if name in IMPLICIT or name == "kind":
                continue
            (opt if optional else req).add(name)
        # a kind can appear once; if the regex catches a nested object first, keep the richer one
        if kind not in schema or len(req | opt) > len(schema[kind][0] | schema[kind][1]):
            schema[kind] = (req, opt)
    return schema


def validate(beats: dict, schema: dict[str, tuple[set[str], set[str]]],
             buildable: set[str] | None = None) -> list[str]:
    problems: list[str] = []
    for section, rows in beats.items():
        if not isinstance(rows, list):
            problems.append(f"{section}: expected a list of beats")
            continue
        for i, beat in enumerate(rows, 1):
            where = f"{section}[{i}]"
            kind = beat.get("kind")
            if kind not in schema:
                problems.append(f"{where}: unknown kind {kind!r} — "
                                f"the renderer has no branch for it")
                continue
            if buildable and kind not in buildable:
                problems.append(f"{where}: kind {kind!r} is in the renderer's union but the "
                                f"builder will not accept it — build_figures raises SystemExit "
                                f"on it. Allowed: {sorted(buildable)}")
                continue
            req, opt = schema[kind]
            given = set(beat) - {"kind"}
            missing = req - given
            unknown = given - req - opt
            if missing:
                problems.append(f"{where} ({kind}): missing required {sorted(missing)}")
            if unknown:
                problems.append(f"{where} ({kind}): field(s) the renderer never reads "
                                f"{sorted(unknown)} — allowed: {sorted(req | opt)}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="episode filmconfig json")
    ap.add_argument("--beats", required=True, help="json: {SECTION: [beat, ...]}")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--min-per-act", type=int, default=10,
                    help="floor for each ACT_* section; EP52-56 run 13-24 per act")
    a = ap.parse_args()

    cfg_path, beats_path = Path(a.config), Path(a.beats)
    beats = json.loads(beats_path.read_text(encoding="utf-8"))
    schema = union_schema()
    buildable = builder_kinds()
    if buildable:
        print(f"[beats] renderer exposes {len(schema)} figure kinds; "
              f"the builder accepts {len(buildable)} of them")
    else:
        print(f"[beats] renderer exposes {len(schema)} figure kinds; "
              f"WARNING: could not read the builder's VALID_KINDS, so builder-legality "
              f"is NOT being checked", file=sys.stderr)

    problems = validate(beats, schema, buildable)
    thin = [s for s, rows in beats.items()
            if s.startswith("ACT_") and len(rows) < a.min_per_act]
    for s in thin:
        problems.append(f"{s}: only {len(beats[s])} beat(s); floor is {a.min_per_act}. "
                        f"A thin act is what produced the kamishibai gate failure on EP57.")

    if problems:
        for p in problems:
            print(f"  REJECT {p}", file=sys.stderr)
        print(f"\n{len(problems)} problem(s); {cfg_path.name} NOT modified", file=sys.stderr)
        return 1

    total = sum(len(v) for v in beats.values())
    print(f"[beats] {total} beat(s) valid: "
          + ", ".join(f"{k}:{len(v)}" for k, v in beats.items()))
    if a.dry_run:
        print("DRY RUN — config not written")
        return 0

    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    before = sum(len(v) for v in cfg.get("figures_by_section", {}).values())
    cfg["figures_by_section"] = beats
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[beats] {cfg_path.name}: {before} -> {total} figure beats")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
