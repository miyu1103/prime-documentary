#!/usr/bin/env python
"""The episode's machine contract exists and is complete -- or nothing downstream runs.

On 2026-08-02 the acceptance gate carried this fallback:

    t = manifest.get("target_duration_minutes")
    if not t:
        return RUNTIME_LO, RUNTIME_HI      # silently: 690-750s, an 11.5 minute film

None of EP50-EP59 declared a duration, so every 29-minute episode was measured against a
12-minute band. Six checks failed on eight or nine of nine episodes, a permanently red gate
stopped being read, and three real defects (a rubber-stamp footage QC, a duplicate-upload
guard that never executed, a probe receipt from a different render) sat inside that red for
months.

So the rule this file enforces is the whole point of the layer:

    AN UNDECLARED VALUE IS AN ERROR. NOTHING IS INFERRED.

It validates episodes/PD-*-<slug>/episode_spec.v<NNN>.json against
schemas/episode_spec.v001.json -- the file exists, it parses, every required field is
present, every type and array length is right, and episode_id/slug match the directory the
spec sits in. It reads nothing else and touches the network never.

REVISIONS. The spec is an approved artifact, so it is never edited in place; a correction is
a new immutable revision (CLAUDE.md invariant 6, .claude/rules/12). spec_path() therefore
resolves the HIGHEST episode_spec.vNNN.json present, and main() prints which one it used --
because a correction nobody can see the tool reading is not a correction. Almost every
episode has only v001 and resolves exactly as before.

    python scripts/check_episode_spec.py --slug flowers

Exit 0 = the spec is valid. Exit 1 = it is missing or wrong; every problem is printed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "episode_spec.v001.json"
SPEC_NAME = "episode_spec.v001.json"


SPEC_GLOB = "episode_spec.v[0-9][0-9][0-9].json"


def spec_path(epdir: Path) -> Path:
    """Where this episode's machine contract lives -- the HIGHEST revision present.

    This used to be one hard-coded name with the comment "one name, no revision search", and
    that made the constitution's own revision rule unusable here. Invariant 6 says an approved
    artifact is never overwritten and a correction is a NEW immutable revision; but every tool
    reads the spec through this function, so a correctly-written episode_spec.v002.json was
    invisible to all of them. A correction that no tool reads is worse than no correction: the
    file says one thing, the pre-flight and the post-build gate measure another, and the
    difference is silent. Measured 2026-08-12 while correcting EP66/EP67/EP69
    distinct_video_assets (decisions/0009).

    The glob is deliberately narrow -- `episode_spec.vNNN.json` and nothing else -- so the
    in-place backups that are already sitting in episode directories
    (`episode_spec.v001.json.bak_cutsec`, `.bak_batchB`) can never be picked up as a revision.
    Sorting is on the integer, not the string, so v010 beats v009.

    An episode with only v001 resolves to exactly the file it resolved to before.
    """
    revs = sorted(epdir.glob(SPEC_GLOB),
                  key=lambda p: int(p.name.split(".v")[1].split(".")[0]))
    return revs[-1] if revs else epdir / SPEC_NAME


def find_episode(slug: str) -> tuple[Path | None, list[str]]:
    eps = sorted((ROOT / "episodes").glob(f"PD-*-{slug}"))
    if not eps:
        return None, [f"no episodes/PD-*-{slug} directory"]
    return eps[0], []


def load_and_validate(slug: str) -> tuple[dict | None, list[str], Path | None]:
    """Return (spec, problems, episode_dir). spec is None whenever problems is non-empty.

    Every caller uses this instead of re-reading the file, so there is exactly one place
    that decides whether a spec is usable.
    """
    epdir, problems = find_episode(slug)
    if epdir is None:
        return None, problems, None

    path = spec_path(epdir)
    if not path.is_file():
        return None, [f"no spec: {path.relative_to(ROOT).as_posix()} "
                      f"(an undeclared value is an error -- write the spec, do not build)"], epdir
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return None, [f"spec is not valid JSON ({exc})"], epdir
    if not isinstance(spec, dict):
        return None, [f"spec is a {type(spec).__name__}, expected a JSON object"], epdir

    try:
        import jsonschema
    except ImportError:
        return None, ["jsonschema is not installed in this interpreter, so the spec cannot "
                      "be validated (pip install jsonschema)"], epdir
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return None, [f"schemas/{SCHEMA.name} is unreadable ({exc})"], epdir

    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(spec), key=lambda e: list(e.absolute_path)):
        where = "/".join(str(p) for p in err.absolute_path) or "(root)"
        problems.append(f"{where}: {err.message}")

    # The schema cannot know which directory the file was read from. This is the check that
    # catches a spec copied from a sibling episode and never edited.
    if spec.get("episode_id") != epdir.name:
        problems.append(f"episode_id is {spec.get('episode_id')!r} but the spec sits in "
                        f"episodes/{epdir.name}")
    if spec.get("slug") != slug:
        problems.append(f"slug is {spec.get('slug')!r} but the directory says {slug!r}")

    return (None if problems else spec), problems, epdir


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()
    slug = a.slug

    spec, problems, _ = load_and_validate(slug)
    if problems:
        print(f"[spec] {slug}: INVALID -- {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1

    assert spec is not None
    _epdir, _ = find_episode(slug)
    _rev = spec_path(_epdir).name if _epdir else "?"
    lo, hi = spec["runtime_seconds"]
    wl, wh = spec["script_words"]
    bl, bh = spec["figure_beats_per_act"]
    print(f"[spec] {slug}: valid [{_rev}] -- runtime {lo:.0f}-{hi:.0f}s, script {wl}-{wh} words, "
          f"{len(spec['section_vocabulary'])} sections, beats {bl}-{bh}/act, "
          f"{spec['distinct_video_assets']} distinct video assets, "
          f"{spec['people_plates_min']} people plates, "
          f"{len(spec.get('mandatory_stills') or [])} mandatory still(s), "
          f"{len(spec.get('forbidden_subjects') or [])} forbidden subject(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
