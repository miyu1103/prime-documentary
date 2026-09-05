#!/usr/bin/env python3
"""Demo: run the vertical-slice pipeline on a throwaway episode under runs/.

No network, no LLM, no paid calls, no upload. Safe to run repeatedly.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pd_factory.pipeline import init_episode_from_topic, run_pipeline  # noqa: E402


def main() -> int:
    target = ROOT / "runs" / "demo-episode"
    if target.exists():
        shutil.rmtree(target)
    repo = init_episode_from_topic(target, ROOT / "examples" / "episode")

    print("== first run ==")
    first = run_pipeline(repo)
    for r in first.results:
        print(f"  {r.action:8} {r.name:14} {r.revision}")
    print(f"  final_state: {first.final_state}")

    print("== second run (idempotent resume) ==")
    second = run_pipeline(repo)
    print(f"  produced={len(second.by_action('produced'))} skipped={len(second.by_action('skipped'))}")

    print("== partial rerun from claims (downstream invalidation) ==")
    third = run_pipeline(repo, from_stage="claims")
    print(f"  produced={third.by_action('produced')}")

    qc = repo.read_artifact("08_qc", "qc_report", repo.read_manifest()["active_revisions"]["qc_report"])
    print(f"== QC gate: {qc['result']} ({len(qc['findings'])} findings) ==")
    print(json.dumps([f["code"] for f in qc["findings"]], indent=2))
    print(f"\nArtifacts written under: {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
