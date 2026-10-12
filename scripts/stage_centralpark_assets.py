#!/usr/bin/env python
"""Stage and verify EP50 Central Park public assets.

Delegates to the deterministic local asset pipeline so the manifest and
`remotion/public/centralpark/**` stay in sync.
"""
from __future__ import annotations

from generate_centralpark_codex_assets import main


if __name__ == "__main__":
    raise SystemExit(main())
