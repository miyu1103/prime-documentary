#!/usr/bin/env python
"""Stage an episode's footage from ITS OWN query set, and drop what does not belong to it.

The unattended queue asked every episode the same generic questions (prison / jail / police /
courtroom / ...), so a British Post Office IT scandal was handed American patrol cars, a neon
HOTEL sign and a rice paddy -- clips that matched the words and not the story. Queries now come
from config/episode_footage_queries.v001.json, one set per episode, and clips whose TITLE is
plainly foreign to that episode are retired first.

    python scripts/stage_episode_footage.py --slug postoffice [--per-query 6] [--dry-run]

Wraps prune_pool_by_blocklist, dedupe_pool_across_episodes and stage_footage_by_title so the
whole "make this pool right" step is one command with one exit code.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUERIES = ROOT / "config" / "episode_footage_queries.v001.json"

# titles that are wrong for EVERY episode in this catalogue, whatever the query matched
UNIVERSAL_JUNK = re.compile(
    r"(hotel|casino|nightclub|neon|rice (paddy|field)|paddy|stadium|football|soccer|"
    r"basketball|beach|resort|tropical|safari|wildlife|zoo|cartoon|3d render|"
    r"abstract art|bokeh|fireworks|wedding|party|dance|yoga|fitness|cooking|recipe|"
    r"makeup|fashion show|drone mountain|ski|surf)", re.I)


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    for line in (r.stdout or "").splitlines():
        if line.startswith(("[prune]", "[dedupe]", "[stage]", "  ")):
            print(line)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--per-query", type=int, default=6)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    spec = json.loads(QUERIES.read_text(encoding="utf-8"))["episodes"].get(a.slug)
    if not spec:
        print(f"[stage] no query set for {a.slug} in {QUERIES.name} -- add one before building",
              file=sys.stderr)
        return 1
    print(f"[stage] {a.slug}: {spec['note']}")

    pool = ROOT / "remotion" / "public" / a.slug / "factory"
    if pool.is_dir():
        junk = [p for p in sorted(pool.glob("*.mp4")) if UNIVERSAL_JUNK.search(p.name)]
        if junk and not a.dry_run:
            dst = pool.parent / "factory_offtopic"
            dst.mkdir(exist_ok=True)
            for p in junk:
                shutil.move(str(p), str(dst / p.name))
        print(f"[stage] {len(junk)} clip(s) retired as foreign to any episode in this catalogue"
              + (f": {', '.join(p.name.split('__')[-1][:28] for p in junk[:6])}" if junk else ""))

    run([sys.executable, str(ROOT / "scripts" / "prune_pool_by_blocklist.py"), "--slug", a.slug]
        + (["--dry-run"] if a.dry_run else []))
    run([sys.executable, str(ROOT / "scripts" / "dedupe_pool_across_episodes.py"), "--slug", a.slug]
        + (["--dry-run"] if a.dry_run else []))

    cmd = [sys.executable, str(ROOT / "scripts" / "stage_footage_by_title.py"),
           "--slug", a.slug, "--per-query", str(a.per_query)]
    for q in spec["queries"]:
        cmd += ["--query", q]
    if a.dry_run:
        cmd.append("--dry-run")
    run(cmd)

    n = len(list(pool.glob("*.mp4"))) if pool.is_dir() else 0
    print(f"[stage] {a.slug}: pool now {n} clip(s) from {len(spec['queries'])} episode-specific queries")
    return 0 if n >= 40 else 1


if __name__ == "__main__":
    raise SystemExit(main())
