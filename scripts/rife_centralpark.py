#!/usr/bin/env python
"""EP50 Central Park interpolation/QC entrypoint.

This is a compatibility wrapper for the CODEX_A material workflow. The current
asset pass uses local FFmpeg loop synthesis and records provider provenance in
the manifest; it does not invoke SDXL, paid APIs, or external services.
"""
from __future__ import annotations

from generate_centralpark_codex_assets import main


if __name__ == "__main__":
    raise SystemExit(main())
