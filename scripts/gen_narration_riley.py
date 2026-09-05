#!/usr/bin/env python3
"""Generate PD-2026-007 Riley narration with the channel voice.

Paid ElevenLabs API call. Owner approval is recorded in APR-0002.
This reuses the vetted Terry narration generator with Riley-specific constants.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import gen_narration_terry as base

EP = "PD-2026-007-riley"

base.EP = EP
base.SCRIPT = ROOT / "episodes" / EP / "03_script" / "script.en.v001.md"
base.ANNOTATED = ROOT / "episodes" / EP / "03_script" / "script.annotated.v001.json"
base.APPROVAL_ID = "APR-0002"


if __name__ == "__main__":
    raise SystemExit(base.main(sys.argv[1:]))
