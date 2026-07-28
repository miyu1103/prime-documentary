#!/usr/bin/env python
"""Resume EP23 after all hero stills are present.

This does not upload or publish. It refuses to render if the strict sensitive
lock audit fails.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-023-swartz"
EPDIR = ROOT / "episodes" / EP
SELECTED = Path("H:/pd-media/episodes/PD-2026-023-swartz/05_visuals/selected")
FINAL = Path("H:/pd-media/episodes/PD-2026-023-swartz/08_edit/final.mp4")
LOG_DIR = EPDIR / "09_package" / "logs"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(cmd: list[str], label: str) -> dict:
    print(f"== {label}", flush=True)
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return {
        "label": label,
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-8000:],
        "stderr": proc.stderr[-8000:],
    }


def missing_images() -> list[str]:
    return [
        f"EP23-IMG-{i:03d}.png"
        for i in range(1, 55)
        if not (SELECTED / f"EP23-IMG-{i:03d}.png").is_file()
    ]


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log: dict = {"episode_id": EP, "started_at": now(), "steps": []}

    missing = missing_images()
    if missing:
        log["status"] = "BLOCKED_MISSING_IMAGES"
        log["missing_images"] = missing
        out = LOG_DIR / "ep23_resume_after_images.latest.json"
        out.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(log, indent=2, ensure_ascii=False))
        return 1

    commands = [
        ([str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/check_ep23_sensitive_locks.py", "--json"], "strict sensitive lock audit"),
        ([str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/build_ep23_swartz_final.py", "--final"], "build EP23 final"),
        ([str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/check_runtime_band.py", str(FINAL), "--lo", "1620", "--hi", "1980", "--json"], "runtime band 27-33 min"),
        ([str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/check_dynamics.py", str(FINAL), "--json"], "dynamics gate"),
        ([str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/check_final_acceptance.py", "23", "--json"], "final acceptance"),
    ]

    for cmd, label in commands:
        result = run(cmd, label)
        log["steps"].append(result)
        if result["returncode"] != 0:
            log["status"] = "FAIL"
            log["failed_step"] = label
            log["finished_at"] = now()
            out = LOG_DIR / "ep23_resume_after_images.latest.json"
            out.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(json.dumps(log, indent=2, ensure_ascii=False))
            return result["returncode"] or 1

    log["status"] = "PASS"
    log["finished_at"] = now()
    out = LOG_DIR / "ep23_resume_after_images.latest.json"
    out.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(log, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
