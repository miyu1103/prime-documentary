#!/usr/bin/env python3
"""Generate narration + the -14 LUFS mix + caption timing for every authored Short.

Runs the existing per-Short tools in order, one Short at a time, and keeps going when one fails
so a single bad episode does not stall the batch (rules/python-adapters: never stop the whole run
on one item). Resumable: a Short whose final mix already exists is skipped, so this can be
re-invoked after an interruption.

Gap is 0.22 s, not the old 0.50 s. Measured 2026-08-02: the inter-line silence was producing a
~10 dB hole every 8-10 seconds on every Short ever shipped, which the owner heard as "the volume
drops for no reason". Shortening the gap and lifting the ducked music floor removed it.

Usage:
  py -3.11 scripts/build_all_short_audio.py --dry-run
  py -3.11 scripts/build_all_short_audio.py [--limit 5] [--only 86,87] [--voice-stage draft]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
GAP = "0.22"


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, ((r.stdout or "") + (r.stderr or ""))[-400:]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="", help="comma-separated short numbers")
    ap.add_argument("--voice-stage", choices=("draft", "master"), default="master")
    args = ap.parse_args()
    only = {x.strip() for x in args.only.split(",") if x.strip()}

    jobs = []
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d["shorts"]:
            if not s.get("angle"):
                continue
            nn = s["short_id"].replace("short", "")
            if only and nn not in only:
                continue
            spec = ROOT / "episodes" / d["episode_id"] / "09_package" / f"short{nn}_lines.v001.json"
            mix = MEDIA / "episodes" / d["episode_id"] / "07_audio" / f"short{nn}_final_mix_v002_en_us.mp3"
            jobs.append({"nn": nn, "ep": d["episode_id"], "spec": spec, "mix": mix,
                         "views": d["destination"]["views"]})
    # highest-value destination first, so an interrupted run has finished the ones that matter
    jobs.sort(key=lambda j: -j["views"])
    # "Already mixed" used to mean "the file exists", which is not the same as "the file matches
    # the script". When the designs went from 5 narration lines to 8, every mix on disk was stale
    # and this reported "14 ok" in zero minutes, leaving 33 s of audio under a 57 s design. It
    # happened twice before anyone measured the mp3. A mix older than its own lines file is stale.
    def stale(j: dict) -> bool:
        if not j["mix"].exists():
            return True
        if not j["spec"].exists():
            return False
        return j["spec"].stat().st_mtime > j["mix"].stat().st_mtime

    todo = [j for j in jobs if stale(j)]
    rebuilt = [j for j in todo if j["mix"].exists()]
    print(f"{len(jobs)} shorts authored | {len(jobs)-len(todo)} already mixed | {len(todo)} to build"
          + (f" ({len(rebuilt)} of them STALE - lines file is newer than the mix)" if rebuilt else ""))
    for j in rebuilt:
        # rename rather than overwrite: an interrupted rebuild must not leave a half-written mix
        # that a later run would treat as current
        bak = j["mix"].with_suffix(j["mix"].suffix + ".stale")
        if bak.exists():
            bak.unlink()
        j["mix"].rename(bak)
        print(f"  short{j['nn']}: stale mix moved aside -> {bak.name}")
    if args.limit:
        todo = todo[:args.limit]
    if args.dry_run:
        for j in todo[:10]:
            print(f"  short{j['nn']:<5} {j['ep']}")
        print(f"  ... {len(todo)} total")
        return 0

    ok = fail = 0
    t0 = time.time()
    for i, j in enumerate(todo, 1):
        if not j["spec"].exists():
            print(f"[{i}/{len(todo)}] short{j['nn']} SKIP - no lines file"); fail += 1; continue
        rc, out = run(["py", "-3.11", "scripts/gen_newshort_narration.py",
                       "--short", j["nn"], "--ep", j["ep"],
                       "--text-json", str(j["spec"]), "--gap", GAP,
                       "--voice-stage", args.voice_stage])
        if rc:
            print(f"[{i}/{len(todo)}] short{j['nn']} NARRATION FAILED: {out[-160:]}"); fail += 1; continue
        rc, out = run(["py", "-3.11", "scripts/build_short_mix.py",
                       "--short", j["nn"], "--ep", j["ep"]])
        if rc:
            print(f"[{i}/{len(todo)}] short{j['nn']} MIX FAILED: {out[-160:]}"); fail += 1; continue
        dur = ""
        for line in out.splitlines():
            if line.startswith("voice_end"):
                dur = line.strip()
        print(f"[{i}/{len(todo)}] short{j['nn']:<5} ok  {dur}")
        ok += 1
    print(f"\nbuilt {ok}, failed {fail}, in {int(time.time()-t0)//60} min")
    return 0 if not fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
