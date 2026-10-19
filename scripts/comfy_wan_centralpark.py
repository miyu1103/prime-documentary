#!/usr/bin/env python
"""EP50 Central Park motion-asset entrypoint.

The CODEX_A contract named this as the Wan/Comfy motion pass, but this project
run is explicitly locked to no SDXL and no paid/external generation. It delegates
to the deterministic local renderer, which creates the required i2v source
stills, motion loops, factory loops, overlays, and manifest entries.
"""
from __future__ import annotations

from generate_centralpark_codex_assets import main


if __name__ == "__main__":
    raise SystemExit(main())
