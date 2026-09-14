#!/usr/bin/env python3
"""Run EP19 final assembly after hero images are complete.

This is the one-command resume path. It performs no upload/publish. It stops on
image readiness failure, build failure, or independent final acceptance failure.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv" / "Scripts" / "python.exe"
EP = "PD-2026-019-varsityblues"
LOG = ROOT / "episodes" / EP / "09_package" / "final_resume_run.v001.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_step(name: str, args: list[str]) -> dict:
    started = now()
    proc = subprocess.run(
        [str(PY), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return {
        "name": name,
        "args": args,
        "started_at": started,
        "finished_at": now(),
        "exit_code": proc.returncode,
        "stdout_tail": proc.stdout[-5000:],
        "stderr_tail": proc.stderr[-5000:],
    }


def main() -> int:
    steps = []
    for name, args in [
        ("image_readiness", ["scripts/check_ep19_image_readiness.py", "--write-report", "--json"]),
        ("final_build", ["scripts/build_ep19_varsityblues_final.py"]),
        ("final_acceptance", ["scripts/check_final_acceptance.py", "19", "--json"]),
    ]:
        step = run_step(name, args)
        steps.append(step)
        LOG.parent.mkdir(exist_ok=True)
        LOG.write_text(json.dumps({"episode_id": EP, "status": "running", "steps": steps}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if step["exit_code"] != 0:
            LOG.write_text(
                json.dumps({"episode_id": EP, "status": "FAIL", "failed_step": name, "steps": steps, "finished_at": now()}, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"EP19 final resume failed at {name}; see {LOG}")
            return step["exit_code"] or 1
    LOG.write_text(json.dumps({"episode_id": EP, "status": "PASS", "steps": steps, "finished_at": now()}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"EP19 final accepted; see {LOG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
