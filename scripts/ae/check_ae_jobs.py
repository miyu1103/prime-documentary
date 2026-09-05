#!/usr/bin/env python3
"""Validate scripts/ae/jobs_<slug>.json against the episode's own ae_beats contract.

Format: scripts/ae/JOBS_FORMAT.v001.md. The contract is episode_spec.v001.json `ae_beats`
(ADR-0011): the jobs file may add render detail but may not drop, retime, retype or invent a
beat. The typing rule exists because EP76 morandi shipped "NaN" in 100-pixel type five times --
a numeric card whose value arrived as a string (docs/handover/2026-08-24.md).

    py -3.11 scripts/ae/check_ae_jobs.py --slug keybridge
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STYLES_RENDERABLE = {"number", "punch"}          # what kinetic_beat.jsx draws today
NUM = (int, float)


def fail_list(slug: str, jobs_path: Path) -> list[str]:
    out: list[str] = []
    specs = glob.glob(str(ROOT / "episodes" / f"PD-*-{slug}" / "episode_spec.v001.json"))
    if len(specs) != 1:
        return [f"expected exactly one spec for slug {slug!r}, found {len(specs)}"]
    spec = json.loads(Path(specs[0]).read_text(encoding="utf-8"))
    ab = spec.get("ae_beats")
    if not ab:
        return [f"{Path(specs[0]).name} declares no ae_beats"]

    try:
        jobs = json.loads(jobs_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"{jobs_path} missing"]
    except json.JSONDecodeError as e:
        return [f"{jobs_path.name}: not valid JSON ({e})"]
    if not isinstance(jobs, list):
        return [f"{jobs_path.name}: must be a flat array (render_beats.sh reads it directly)"]

    beats = {b["id"]: b for b in ab["beats"]}
    seen: dict[str, int] = {}
    ids: set[str] = set()

    for i, j in enumerate(jobs):
        tag = j.get("id", f"[index {i}]")
        b_id = j.get("beat")
        if b_id not in beats:
            out.append(f"{tag}: beat {b_id!r} is not declared in the spec")
            continue
        seen[b_id] = seen.get(b_id, 0) + 1
        b = beats[b_id]
        want_id = f"{slug}_{b_id.lower()}"
        if j.get("id") != want_id:
            out.append(f"{tag}: id must be {want_id!r} (shared AE out dir needs global uniqueness)")
        if j.get("id") in ids:
            out.append(f"{tag}: duplicate id")
        ids.add(j.get("id", ""))
        for field in ("act", "kind"):
            if j.get(field) != b[field]:
                out.append(f"{tag}: {field}={j.get(field)!r} but spec declares {b[field]!r}")
        if not isinstance(j.get("seconds"), NUM) or isinstance(j.get("seconds"), bool):
            out.append(f"{tag}: seconds must be a JSON number, got {type(j.get('seconds')).__name__}")
        elif abs(j["seconds"] - b["duration_sec"]) > 1e-9:
            out.append(f"{tag}: seconds={j['seconds']} but spec declares duration_sec={b['duration_sec']}")
        if j.get("headline") != b["headline"]:
            out.append(f"{tag}: headline differs from the spec's")
        for vf in ("value", "value_a", "value_b"):
            if vf in j and (not isinstance(j[vf], NUM) or isinstance(j[vf], bool)):
                out.append(f"{tag}: {vf} must be a JSON number, got {j[vf]!r} "
                           f"({type(j[vf]).__name__}) -- a string renders as NaN")
        st = j.get("style")
        if st is not None and st not in STYLES_RENDERABLE:
            out.append(f"{tag}: style {st!r} is not one kinetic_beat.jsx draws "
                       f"({sorted(STYLES_RENDERABLE)}); omit style until the generic builder exists")
        if st == "number" and not j.get("big"):
            out.append(f"{tag}: style=number needs 'big'")
        if st == "punch" and not j.get("words"):
            out.append(f"{tag}: style=punch needs 'words'")
        if j["kind"] == "quote_card" and not (j.get("quote") and j.get("attribution")):
            out.append(f"{tag}: quote_card needs verbatim 'quote' and 'attribution'")
        if j["kind"] in ("list_build", "system_map", "timeline", "comparison") and not j.get("lines"):
            out.append(f"{tag}: kind={j['kind']} needs 'lines' body copy")
        for ln in j.get("lines", []):
            if not isinstance(ln, dict) or not ln.get("t") or not ln.get("cite"):
                out.append(f"{tag}: every line needs 't' and a ledger 'cite', got {ln!r}")

    missing = [b for b in beats if b not in seen]
    if missing:
        out.append(f"spec beats missing from jobs file: {missing}")
    dupes = [b for b, n in seen.items() if n > 1]
    if dupes:
        out.append(f"spec beats appearing more than once: {dupes}")

    n, tot = len(jobs), sum(j.get("seconds", 0) for j in jobs
                            if isinstance(j.get("seconds"), NUM))
    if n < ab["min_count"]:
        out.append(f"{n} jobs < declared min_count {ab['min_count']}")
    if tot < ab["screen_seconds_min"]:
        out.append(f"{tot}s on screen < declared floor {ab['screen_seconds_min']}s")

    others = [p for p in glob.glob(str(ROOT / "scripts" / "ae" / "jobs_*.json"))
              if Path(p).name != jobs_path.name]
    for p in others:
        try:
            for j in json.loads(Path(p).read_text(encoding="utf-8")):
                if isinstance(j, dict) and j.get("id") in ids:
                    out.append(f"id {j['id']!r} collides with {Path(p).name} (shared out dir)")
        except Exception:
            continue
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--file", help="override jobs file path (for self-test)")
    a = ap.parse_args()
    jobs_path = Path(a.file) if a.file else ROOT / "scripts" / "ae" / f"jobs_{a.slug}.json"
    problems = fail_list(a.slug, jobs_path)
    if problems:
        for p in problems:
            print(f"FAIL  {p}")
        print(f"[ae-jobs] {a.slug}: {len(problems)} problem(s)")
        return 1
    jobs = json.loads(jobs_path.read_text(encoding="utf-8"))
    tot = sum(j["seconds"] for j in jobs)
    styled = sum(1 for j in jobs if j.get("style"))
    print(f"[ae-jobs] {a.slug}: PASS -- {len(jobs)} beats, {tot}s on screen, "
          f"{styled} renderable today, {len(jobs) - styled} awaiting the generic builder")
    return 0


if __name__ == "__main__":
    sys.exit(main())
