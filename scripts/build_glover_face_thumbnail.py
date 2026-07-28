#!/usr/bin/env python3
r"""EP48 Glover EMOTIVE FACE thumbnail -- CTR_PLAYBOOK.v001 sec 4A, 2-stage face recipe.

Reuses the audited EP44-47 face builder (build_face_thumbnails_ep4447.py): stage-1
JuggernautXL photoreal portrait -> stage-2 DreamShaperXL img2img d0.55 illustrative
(non-real face, R2 likeness firewall). glover = a wronged driver pulled over at night
because an officer ran his plate (a name), not his driving. Hook <=4 words.

    py scripts/build_glover_face_thumbnail.py [--seeds N]
"""
from __future__ import annotations

import importlib.util
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "scripts" / "build_face_thumbnails_ep4447.py"
spec = importlib.util.spec_from_file_location("ep4447", SRC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

WHITE, YELLOW = m.WHITE, m.YELLOW

GLOVER = dict(
    seed=48311,
    subject=(
        "a close cinematic head-and-shoulders portrait of an ordinary working-class man "
        "in his late 30s with short hair and light stubble, a tense worried disbelieving "
        "expression, jaw tight, brow furrowed, glancing warily to the side away from the "
        "camera, his face lit by cold blue and red police patrol lights at night from "
        "behind, dark heavily-blurred night highway and pine trees in the background, a "
        "warm rim light tracing one cheek and shoulder, plain flannel shirt collar, no "
        "hat, a civilian in plain clothes"
    ),
    neg_extra=("police uniform on the man, badge on the man, the man is a police officer, "
               "steering wheel, hands covering the face, two heads, extra person, hat, cap"),
    zoom=1.15, cx=0.66, cy=0.40,
    kicker="THEY RAN YOUR PLATE",
    lines=[("STOPPED FOR", WHITE), ("A NAME", YELLOW)],
    redbar=False, accent=YELLOW,
)


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    seeds = 3
    if "--seeds" in sys.argv:
        seeds = int(sys.argv[sys.argv.index("--seeds") + 1])
    slug = "PD-2026-048-glover"
    scratch = Path(r"C:\Users\aab15\AppData\Local\Temp\claude\C--Users-aab15-OneDrive-Desktop\2fa81074-5db3-40a1-8cda-403c929c15de\scratchpad")
    scratch.mkdir(parents=True, exist_ok=True)
    best, best_luma = None, -1.0
    for i in range(seeds):
        sd = GLOVER["seed"] + i * 101
        t0 = time.time()
        face = m.two_stage(GLOVER["subject"], sd, GLOVER.get("neg_extra", ""))
        lum = m.subject_luma(face)
        print(f"  seed {sd}: subject_luma={lum:.1f}  ({time.time()-t0:.0f}s)", flush=True)
        face.save(scratch / f"glover_raw_seed{sd}.png")
        if lum > best_luma:
            best, best_luma = face, lum
    comp = m.compose(best, GLOVER)
    pkg = ROOT / "episodes" / slug / "09_package"
    pkg.mkdir(parents=True, exist_ok=True)
    out = pkg / "thumbnail.face.v001.png"
    edge, nbytes = m.save_under_cap(comp, out)
    comp.save(scratch / "glover_face_composite.png")
    print(f"  -> {out}  ({edge}px, {nbytes/1024:.0f} KB, subject_luma={best_luma:.1f})", flush=True)


if __name__ == "__main__":
    main()
