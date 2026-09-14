#!/usr/bin/env python3
"""Launch the minimal one-screen studio UI.

No network, no LLM, no paid calls, no upload. Episodes are written to throwaway
workspaces under runs/ui/ (gitignored). Safe to run repeatedly.

Usage:
    PYTHONPATH=src python scripts/run_ui.py [--host H] [--port N]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pd_factory.web import serve  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(prog="run_ui")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    serve(host=args.host, port=args.port, runs_dir=ROOT / "runs" / "ui")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
