#!/usr/bin/env python
"""EP52 Morton motion-asset entrypoint.

This delegates to the local deterministic renderer for this A-side pass. It
creates real MP4 motion assets and records them in the manifest.
"""
from __future__ import annotations

from generate_morton_codex_assets import main


if __name__ == "__main__":
    raise SystemExit(main())
