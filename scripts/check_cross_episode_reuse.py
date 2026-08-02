#!/usr/bin/env python3
r"""Read-only: which archive clips are already burned in a previous episode.

`check_asset_reuse.py` caps reuse INSIDE one film. Nothing checks reuse ACROSS films, and
the owner directive is explicit that both matter: 「素材の被りを避ける(話またぎ/作品内とも)」
— the scales-of-justice clip had been leaned on across several episodes before anyone
counted.

Identity is by CONTENT, not by name. Staged clips are renamed per episode
(`atwater/factory/F001__atwater_safe_broll_S01.mp4`), so the same source appears under a
different filename in every film it is in. The key here is `(bytes, sha1 of the first
256 KB)`, which is fast and collision-free in practice for encoded video.

    py -3.11 scripts/check_cross_episode_reuse.py --build            # index the 5,782 staged clips
    py -3.11 scripts/check_cross_episode_reuse.py --check <path.mp4> [...]
    py -3.11 scripts/check_cross_episode_reuse.py --check-query beach --limit 24
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "remotion" / "public"
INDEX = ROOT / "episodes" / "_planning" / "measurements" / "STAGED_CLIP_INDEX.json"
HEAD_BYTES = 256 * 1024


def key_of(p: Path) -> str | None:
    """(size, sha1 of first 256 KB). Cheap, and stable across renames and hardlinks."""
    try:
        size = p.stat().st_size
        if not size:
            return None
        with p.open("rb") as f:
            head = f.read(HEAD_BYTES)
        return f"{size}:{hashlib.sha1(head).hexdigest()}"
    except OSError:
        return None


def build(workers: int) -> dict:
    clips = [p for p in PUBLIC.glob("*/factory/*") if p.suffix.lower() in {".mp4", ".mov", ".webm"}]
    print(f"indexing {len(clips)} staged clips ...")
    idx: dict[str, list[str]] = {}
    names: dict[str, str] = {}

    def one(p: Path) -> tuple[str | None, str, str]:
        return key_of(p), p.parts[-3], p.name

    n = 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for k, slug, name in ex.map(one, clips):
            n += 1
            if n % 1000 == 0:
                print(f"  {n}/{len(clips)}", flush=True)
            if not k:
                continue
            if slug not in idx.setdefault(k, []):
                idx[k].append(slug)
            names.setdefault(k, name)
    payload = {"schema_version": "staged-clip-index/v001",
               "clips_indexed": len(clips), "distinct": len(idx),
               "index": {k: {"episodes": v, "example_name": names.get(k, "")}
                         for k, v in idx.items()}}
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    tmp = INDEX.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    tmp.replace(INDEX)
    reused = sum(1 for v in idx.values() if len(v) > 1)
    print(f"\n{len(clips)} staged clips -> {len(idx)} distinct sources")
    print(f"already shared by 2+ episodes: {reused}")
    top = sorted(idx.items(), key=lambda kv: -len(kv[1]))[:10]
    for k, eps in top:
        if len(eps) > 1:
            print(f"  {names.get(k,'')[:52]:<54} {len(eps)}話: {', '.join(sorted(eps))}")
    return payload


def load() -> dict:
    if not INDEX.exists():
        raise SystemExit(f"index missing: {INDEX}\nrun with --build first")
    return json.loads(INDEX.read_text(encoding="utf-8"))["index"]


def check(paths: list[str]) -> int:
    idx = load()
    hits = 0
    for s in paths:
        p = Path(s)
        if not p.is_file():
            print(f"  ?  missing file: {s}")
            continue
        k = key_of(p)
        row = idx.get(k or "")
        if row:
            hits += 1
            print(f"  USED  {p.name[:56]}\n        -> {', '.join(sorted(row['episodes']))}"
                  f"  (staged as {row['example_name']})")
        else:
            print(f"  new   {p.name[:56]}")
    print(f"\n{hits}/{len(paths)} already used in a previous episode")
    return 0


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", nargs="*", default=[])
    ap.add_argument("--check-query", help="run search_archive.py and check its results")
    ap.add_argument("--limit", type=int, default=24)
    ap.add_argument("--kind", default="video")
    ap.add_argument("--workers", type=int, default=16)
    a = ap.parse_args(argv)

    if a.build:
        build(a.workers)
        if not (a.check or a.check_query):
            return 0
    if a.check_query:
        r = subprocess.run([sys.executable, str(ROOT / "scripts/search_archive.py"),
                            a.check_query, "--kind", a.kind, "--limit", str(a.limit),
                            "--paths-only"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        paths = [l.strip() for l in (r.stdout or "").splitlines()
                 if l.strip() and Path(l.strip()).suffix.lower() in {".mp4", ".mov", ".webm"}]
        print(f"query '{a.check_query}': {len(paths)} candidates\n")
        return check(paths)
    if a.check:
        return check(a.check)
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
