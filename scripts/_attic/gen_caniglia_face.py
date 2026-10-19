#!/usr/bin/env python3
r"""Generate an ILLUSTRATIVE non-real emotive face base for PD-2026-043-caniglia.

Reuses the ep4447 2-stage face recipe (JuggernautXL -> DreamShaperXL img2img d0.55)
so the face reads as a DRAMATIZED NON-REAL character, never a real-person likeness.
Saves the raw (pre-text) to scratch so recompose_faces_v002.py can build v002.

    py -3.11 scripts/gen_caniglia_face.py [--seeds N]
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "scripts" / "build_face_thumbnails_ep4447.py"
_spec = importlib.util.spec_from_file_location("ep4447", SRC)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

SCRATCH = Path(r"C:\Users\aab15\AppData\Local\Temp\claude\C--Users-aab15-OneDrive-Desktop\2fa81074-5db3-40a1-8cda-403c929c15de\scratchpad")

SLUG = "PD-2026-043-caniglia"
SEED_BASE = 43107
SUBJECT = (
    "an ordinary distressed silver-haired man in his 60s standing in the open "
    "doorway of his home at night, a deeply worried and violated expression, "
    "brow furrowed, mouth tight, quiet fear and disbelief, looking off to the "
    "side away from the camera, warm golden rim light tracing his face and "
    "shoulder, cold blue night behind him, plain dark casual jacket, an ordinary "
    "homeowner, head and shoulders large and clearly visible filling the RIGHT "
    "side of the frame, deep dark empty negative space on the LEFT"
)
NEG_EXTRA = (
    "police uniform on the man, badge, epaulettes, duty belt, the man is a police "
    "officer, tiny face, small face, wide shot, full body, gun in frame, weapon, "
    "readable text, two people"
)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    seeds = 2
    if "--seeds" in sys.argv:
        seeds = int(sys.argv[sys.argv.index("--seeds") + 1])
    SCRATCH.mkdir(parents=True, exist_ok=True)
    print(f"=== {SLUG} face gen ({seeds} seeds) ===", flush=True)
    for i in range(seeds):
        sd = SEED_BASE + i * 101
        t0 = time.time()
        face = m.two_stage(SUBJECT, sd, NEG_EXTRA)
        lum = m.subject_luma(face)
        out = SCRATCH / f"{SLUG}_raw_seed{sd}.png"
        face.save(out)
        print(f"  seed {sd}: subject_luma={lum:.1f}  ({time.time()-t0:.0f}s) -> {out.name}",
              flush=True)


if __name__ == "__main__":
    main()
