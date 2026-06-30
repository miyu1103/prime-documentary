#!/usr/bin/env python3
"""Wait for EP22 Codex hero images, then build final video and run acceptance.

This script performs no image generation and no upload/publish action. It only
waits for EP22-IMG-001..074 under H:/pd-media, runs the local build, and records
the independent acceptance output.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-022-milken"
EPDIR = ROOT / "episodes" / EP
SELECTED = Path("H:/pd-media/episodes/PD-2026-022-milken/05_visuals/selected")
EXPECTED = 74
PY = ROOT / ".venv" / "Scripts" / "python.exe"
EVIDENCE = EPDIR / "09_package" / "EVIDENCE"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def count_images() -> tuple[int, list[str]]:
    present: list[str] = []
    if SELECTED.exists():
        for i in range(1, EXPECTED + 1):
            p = SELECTED / f"EP22-IMG-{i:03d}.png"
            if p.exists():
                present.append(p.name)
    return len(present), present


def run(cmd: list[str], timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout)


def append_event(event: str, payload: dict) -> None:
    path = EPDIR / "events" / "events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": now(), "event": event, "payload": payload}, ensure_ascii=False) + "\n")


def update_manifest_blocker(count: int) -> None:
    path = EPDIR / "manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    blocker = (
        f"Final render is blocked because hero images are incomplete: found {count}/{EXPECTED} under "
        "H:/pd-media/episodes/PD-2026-022-milken/05_visuals/selected. "
        "No local image generation was performed for missing hero stills."
    )
    if count >= EXPECTED:
        data["blockers"] = [b for b in data.get("blockers", []) if "hero images are incomplete" not in b]
    else:
        others = [b for b in data.get("blockers", []) if "hero images are incomplete" not in b]
        data["blockers"] = others + [blocker]
    data["updated_at"] = now()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Wait for EP22 hero images, then final-build and accept.")
    ap.add_argument("--interval-seconds", type=int, default=60)
    ap.add_argument("--max-wait-minutes", type=int, default=240)
    ap.add_argument("--no-wait", action="store_true", help="fail immediately if images are incomplete")
    args = ap.parse_args()

    deadline = time.time() + max(0, args.max_wait_minutes) * 60
    while True:
        count, _ = count_images()
        print(f"{now()} EP22 hero images: {count}/{EXPECTED}", flush=True)
        update_manifest_blocker(count)
        if count >= EXPECTED:
            break
        if args.no_wait or time.time() >= deadline:
            append_event("final_wait_blocked", {"hero_images": count, "expected": EXPECTED})
            return 2
        time.sleep(max(5, args.interval_seconds))

    append_event("final_wait_ready", {"hero_images": EXPECTED})
    build = run([str(PY), "scripts/build_ep22_milken_final.py"], timeout=24 * 60 * 60)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "final_build.v001.stdout.txt").write_text(build.stdout, encoding="utf-8")
    (EVIDENCE / "final_build.v001.stderr.txt").write_text(build.stderr, encoding="utf-8")
    if build.returncode != 0:
        append_event("final_build_failed", {"returncode": build.returncode})
        print(build.stdout)
        print(build.stderr, file=sys.stderr)
        return build.returncode

    acceptance = run([str(PY), "scripts/check_final_acceptance.py", "22", "--json"], timeout=2 * 60 * 60)
    (EVIDENCE / "final_acceptance.v001.json").write_text(acceptance.stdout, encoding="utf-8")
    (EVIDENCE / "final_acceptance.v001.stderr.txt").write_text(acceptance.stderr, encoding="utf-8")
    append_event("final_acceptance_measured", {"returncode": acceptance.returncode})
    print(acceptance.stdout)
    return acceptance.returncode


if __name__ == "__main__":
    raise SystemExit(main())
