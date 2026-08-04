#!/usr/bin/env python
"""The built film honours the episode's own spec -- checked AFTER the build, BEFORE the render.

check_episode_spec.py proves the contract exists. check_episode_inputs.py proves the raw
inputs exist. Neither of them can see what the builder actually put in the film, and that is
where the expensive failures happened:

  * EP54's fourteen courtroom stills (S211-S224) were generated precisely because the archive
    holds no courtroom footage at all. The builder trimmed a surplus pool from the alphabetical
    tail, the fourteen went with it, and they were then retired as unreferenced. Nobody saw it
    until the finished film had no courtroom in it.
  * EP60 forbids the collapse, the rubble, the rescue and the casualties. The footage queries
    written for it asked for `rubble collapse`, `search and rescue`, `firefighter rescue`,
    `excavator debris` and `ambulance night`; thirty-one clips were staged before a human
    noticed.
  * EP54 shipped 253 footage cuts drawn from 188 distinct assets, so 65 clips ran twice and
    asset_reuse failed -- after a two-hour render.

All three are visible in remotion/src/data/<slug>_film.json in under a second. This reads the
spec and the film and nothing else.

    python scripts/check_spec_satisfied.py --slug flowers

Exit 0 = the film satisfies its spec. Exit 1 = it does not; every failure is printed with its
counts. Read-only, no network.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from check_episode_spec import load_and_validate

ROOT = Path(__file__).resolve().parents[1]
VIDEO_SUFFIXES = (".mp4", ".mov", ".webm", ".m4v")


def _basename(src: str) -> str:
    return str(src or "").replace("\\", "/").rsplit("/", 1)[-1]


def _words(name: str) -> str:
    """Basename reduced to space-separated tokens, so a keyword matches a whole word.

    `rubble_collapse_01.mp4` -> `rubble collapse 01 mp4`. Without this, `bus` matches
    `business_district.mp4` and the check cries wolf until somebody switches it off.
    """
    return re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()


def _hits(keyword: str, haystack: str) -> bool:
    kw = re.sub(r"[^a-z0-9]+", " ", keyword.lower()).strip()
    if not kw:
        return False
    return re.search(rf"(?<![a-z0-9]){re.escape(kw)}(?![a-z0-9])", haystack) is not None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()
    slug = a.slug

    spec, problems, _ = load_and_validate(slug)
    if problems:
        print(f"[satisfied] {slug}: NO SPEC -- {len(problems)} problem(s), "
              f"run scripts/check_episode_spec.py --slug {slug}:")
        for p in problems:
            print(f"  - {p}")
        return 1
    assert spec is not None

    film = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    if not film.is_file():
        print(f"[satisfied] {slug}: NO FILM -- {film.relative_to(ROOT).as_posix()} has not "
              f"been built yet")
        return 1
    try:
        data = json.loads(film.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"[satisfied] {slug}: FAIL -- {film.name} is not valid JSON ({exc})")
        return 1

    cuts = data.get("cuts") or []
    names = [_basename(c.get("src")) for c in cuts]
    present = set(names)
    videos = {n for n in names if n.lower().endswith(VIDEO_SUFFIXES)}

    failures: list[str] = []

    # 1. Every purpose-made still is on screen. This is the EP54 failure, made impossible.
    mandatory = list(spec.get("mandatory_stills") or [])
    # MATCH ON THE STEM, NOT THE EXTENSION.
    # A commissioned still may reach the film as W001.png or, when it has been given motion
    # (i2v, depth parallax), as W001.mp4. It is the same picture carried in a different
    # container, and the rule this check enforces is "the picture the archive could not supply
    # is on screen" -- not "it is on screen as a PNG". Comparing full basenames would fail
    # every motion-converted plate and push the episode back to stills it cannot fit.
    # This does NOT weaken the check: a plate that appears in NO form still fails.
    _stems = {n.rsplit(".", 1)[0].lower() for n in present}
    missing = [s for s in mandatory
               if _basename(s).rsplit(".", 1)[0].lower() not in _stems]
    if missing:
        failures.append(
            f"mandatory_stills: {len(missing)} of {len(mandatory)} declared still(s) are in no "
            f"cut of the film -- {', '.join(sorted(missing))}. These were generated FOR this "
            f"episode to cover a gap the archive cannot fill; a film without them has a hole "
            f"where the coverage was supposed to be.")

    # 2. Nothing the episode forbids is on screen, judged by the source filename.
    forbidden = [k for k in (spec.get("forbidden_subjects") or []) if str(k).strip()]
    if forbidden:
        offenders: dict[str, list[str]] = {}
        for n in sorted(present):
            w = _words(n)
            for kw in forbidden:
                if _hits(kw, w):
                    offenders.setdefault(kw, []).append(n)
        if offenders:
            total = sum(len(v) for v in offenders.values())
            failures.append(
                f"forbidden_subjects: {total} cut source(s) match {len(offenders)} forbidden "
                f"keyword(s) -- " +
                "; ".join(f"{kw} ({len(v)}): {', '.join(v[:4])}"
                          f"{' ...' if len(v) > 4 else ''}"
                          for kw, v in sorted(offenders.items())))

    # 3. Enough distinct video to fill the film without repeating a clip.
    need = int(spec["distinct_video_assets"])
    if len(videos) < need:
        video_cuts = sum(1 for n in names if n.lower().endswith(VIDEO_SUFFIXES))
        failures.append(
            f"distinct_video_assets: {len(videos)} distinct footage+motion source(s) across "
            f"{video_cuts} video cut(s), against a declared {need} -- "
            f"{need - len(videos)} short, so {max(0, video_cuts - len(videos))} cut(s) repeat "
            f"an asset already used")

    print(f"[satisfied] {slug}: cuts={len(cuts)} distinct_video={len(videos)} "
          f"stills_in_film={len(present) - len(videos)} mandatory={len(mandatory)} "
          f"forbidden_keywords={len(forbidden)}")
    if failures:
        print(f"[satisfied] {slug}: FAIL -- {len(failures)} problem(s):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"[satisfied] {slug}: PASS -- the film satisfies its spec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
