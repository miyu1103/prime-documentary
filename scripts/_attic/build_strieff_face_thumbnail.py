#!/usr/bin/env python3
r"""EP49 Strieff EMOTIVE FACE thumbnail -- CTR_PLAYBOOK.v001 sec 4A, 2-stage face recipe.

Reuses the audited EP44-48 face builder (build_face_thumbnails_ep4447.py): stage-1
JuggernautXL photoreal portrait -> stage-2 DreamShaperXL img2img d0.55 illustrative
(non-real face, R2 likeness firewall).

strieff = a wronged, ordinary man stopped on the street for NO reason and searched;
the evidence still counted. Cold procedural dread. Hook <=3 words: STOPPED FOR NOTHING.

    py scripts/build_strieff_face_thumbnail.py [--seeds N]
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

STRIEFF = dict(
    seed=49207,
    subject=(
        "a tight cinematic close-up head-and-shoulders portrait of an ordinary "
        "working-class man in his late 30s stopped by police on a dark residential "
        "sidewalk at night, his face large and clearly visible filling the right side "
        "of the frame, a resigned wronged disbelieving expression, tired wary eyes, "
        "tense jaw, hands raised slightly in a resigned gesture, cold blue and red "
        "patrol light washing across his face, a warm rim light tracing one cheek and "
        "shoulder, glancing warily off to the side away from the camera toward the "
        "police lights, plain casual jacket over a plain shirt, an ordinary civilian, "
        "no uniform, a dark heavily-blurred night street and a chain-link fence behind "
        "him, deep dark negative space on the LEFT"
    ),
    neg_extra=(
        "police uniform on the man, badge on the man, the man is a police officer, "
        "duty belt, handcuffs, readable text, readable signs, numbers on screen, "
        "tiny face, small face, wide shot, two heads, extra person, hat, cap"
    ),
    zoom=1.14, cx=0.66, cy=0.40,
    kicker="AN ILLEGAL STOP",
    lines=[("STOPPED FOR", WHITE), ("NOTHING", YELLOW)],
    redbar=False, accent=YELLOW,
)


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    seeds = 3
    if "--seeds" in sys.argv:
        seeds = int(sys.argv[sys.argv.index("--seeds") + 1])
    slug = "PD-2026-049-strieff"
    scratch = Path(r"C:\Users\aab15\AppData\Local\Temp\claude\C--Users-aab15-OneDrive-Desktop\2fa81074-5db3-40a1-8cda-403c929c15de\scratchpad")
    scratch.mkdir(parents=True, exist_ok=True)
    best, best_luma = None, -1.0
    for i in range(seeds):
        sd = STRIEFF["seed"] + i * 101
        t0 = time.time()
        face = m.two_stage(STRIEFF["subject"], sd, STRIEFF.get("neg_extra", ""))
        lum = m.subject_luma(face)
        print(f"  seed {sd}: subject_luma={lum:.1f}  ({time.time()-t0:.0f}s)", flush=True)
        face.save(scratch / f"strieff_raw_seed{sd}.png")
        if lum > best_luma:
            best, best_luma = face, lum
    comp = m.compose(best, STRIEFF)
    pkg = ROOT / "episodes" / slug / "09_package"
    pkg.mkdir(parents=True, exist_ok=True)
    out = pkg / "thumbnail.face.v001.png"
    edge, nbytes = m.save_under_cap(comp, out)
    comp.save(scratch / "strieff_face_composite.png")
    print(f"  -> {out}  ({edge}px, {nbytes/1024:.0f} KB, subject_luma={best_luma:.1f})", flush=True)


if __name__ == "__main__":
    main()
