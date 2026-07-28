#!/usr/bin/env python
"""Read-only EP23 pre-final readiness summary.

Use this while images are still arriving. It reports exactly what remains before
`run_ep23_after_images.py` can attempt a final render.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPDIR = ROOT / "episodes" / "PD-2026-023-swartz"
SELECTED = Path("H:/pd-media/episodes/PD-2026-023-swartz/05_visuals/selected")


def exists(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def run_json(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = {"stdout": proc.stdout, "stderr": proc.stderr}
    data["returncode"] = proc.returncode
    return data


def main() -> int:
    missing = [
        f"EP23-IMG-{i:03d}.png"
        for i in range(1, 55)
        if not exists(SELECTED / f"EP23-IMG-{i:03d}.png")
    ]
    sensitive = run_json([str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/check_ep23_sensitive_locks.py", "--json"])
    acceptance = run_json([str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/check_final_acceptance.py", "23", "--json"])
    checks = {
        "images_complete": not missing,
        "voice_ready": exists(EPDIR / "06_audio" / "narration_index.v001.json"),
        "captions_ready": exists(EPDIR / "08_edit" / "captions.v001.srt"),
        "audio_mix_ready": exists(Path("H:/pd-media/episodes/PD-2026-023-swartz/08_edit/swartz_final_mix.v001.wav")),
        "thumbnails_ready": exists(EPDIR / "09_package" / "thumbnail.selected.v001.png"),
        "factory_ready": (ROOT / "remotion" / "public" / "swartz" / "factory").is_dir(),
        "sensitive_locks_pass": sensitive.get("status") == "PASS",
        "final_acceptance_pass": acceptance.get("status") == "PASS",
    }
    blockers = []
    if missing:
        blockers.append({"type": "missing_images", "count": len(missing), "missing": missing})
    if sensitive.get("status") != "PASS":
        blockers.append({"type": "sensitive_locks", "results": sensitive.get("results", [])})
    if acceptance.get("status") != "PASS":
        blockers.append({"type": "final_acceptance", "results": acceptance.get("results", [])})
    report = {
        "episode_id": "PD-2026-023-swartz",
        "status": "READY_FOR_FINAL_RENDER" if checks["images_complete"] and checks["sensitive_locks_pass"] else "BLOCKED",
        "checks": checks,
        "hero_images_present": 54 - len(missing),
        "hero_images_missing": len(missing),
        "blockers": blockers,
        "resume_command": ".\\.venv\\Scripts\\python.exe scripts\\run_ep23_after_images.py",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "READY_FOR_FINAL_RENDER" else 1


if __name__ == "__main__":
    raise SystemExit(main())
