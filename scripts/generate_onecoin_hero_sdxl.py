#!/usr/bin/env python
"""Generate EP17 (PD-2026-017-onecoin) SDXL hero stills via local A1111 (:7860).

MAX-quality: juggernautXL, 40 steps, Hires.fix R-ESRGAN 4x+ (2x -> 2688x1536).
Keepers are later upscaled to >=3840 long edge (PD_ONE_PASS_PRODUCTION_SPEC row 5).
Scoped to EP17 only. No paid API, no upload, no publish. Idempotent: skips files
that already exist. Read-only against the A1111 server; writes PNGs to H: only.
"""
from __future__ import annotations
import urllib.request, json, base64, time, os, sys

BASE = "http://127.0.0.1:7860"
OUT = r"H:\pd-media\episodes\PD-2026-017-onecoin\05_stock\hero"
N_VAR = int(sys.argv[1]) if len(sys.argv) > 1 else 4

SUFFIX = (", cinematic documentary still, dramatic chiaroscuro lighting, photorealistic, "
          "ultra detailed, volumetric light, atmospheric haze, subtle film grain, shallow "
          "depth of field, anamorphic, masterpiece, ultra high resolution, 16:9")
COLOR = {
    "gold": ", deep black background with warm gold and amber rim light, opulent, seductive",
    "white": ", cold fluorescent white and pale blue light, clinical, sterile, uneasy",
    "black": ", near-black palette, a single cold light source, void, emptiness",
}
NEG = ("text, letters, words, watermark, logo, signature, caption, brand markings, "
       "identifiable face, recognizable real person, celebrity likeness, portrait of a specific "
       "person, deformed, mutated, extra fingers, extra limbs, bad anatomy, bad hands, low quality, "
       "lowres, blurry, jpeg artifacts, cartoon, anime, illustration, 3d render look, oversaturated, "
       "cluttered, ugly")

PROMPTS = [
 ("T-IMG-001", "gold", "a vast concert arena from above, bathed in warm golden light, thousands of out-of-focus people standing and cheering toward a distant bright stage, haze, lens flare"),
 ("T-IMG-003", "gold", "a single ornate gold coin with a perfectly round hole bored through its center, suspended in black, one shaft of light passing through the empty hole, macro, reflective"),
 ("T-IMG-004", "gold", "a cascade of crisp hundred-dollar bills falling in slow motion into an open briefcase, warm seductive golden light, wealth, abundance"),
 ("T-IMG-005", "gold", "the backlit silhouette of a woman in a long gown standing alone at a podium on a huge stage, gold rim light, face unreadable in shadow, commanding, no visible features"),
 ("T-IMG-006", "gold", "close on official-looking documents and a magnifying glass on a dark desk, a fountain pen signing a contract, warm light cooling at the edges, shallow focus"),
 ("T-IMG-007", "gold", "a crowd of ordinary people lit by warm gold light, faces lifted and hopeful, phones raised filming a bright unseen stage, reverent"),
 ("T-IMG-AUX1", "gold", "a row of sealed premium boxes of increasing size on a dark shelf, gold foil edges, like luxury product tiers, one spotlit, aspirational"),
 ("T-IMG-008", "white", "a lone analyst seen from behind, lit only by a cold computer monitor in a dark room, rain streaking a window, tense, isolated, no visible face"),
 ("T-IMG-009", "white", "a close-up of hands typing numbers into a glowing spreadsheet in a dark room, the figures invented not calculated, cold blue screen light on the keys"),
 ("T-IMG-010", "white", "an official government warning letter with an embossed seal and letterhead on a desk, a rubber stamp coming down, cold authoritative light, bureaucratic"),
 ("T-IMG-011", "white", "a single empty wooden chair in a bare cold room, one shaft of pale window light, absence, isolation, melancholic"),
 ("T-IMG-016", "white", "the lone silhouette of a figure at a podium under a single light, while around it stacks of unopened warning letters pile up unread in the cold dark, oblivious"),
 ("T-IMG-015", "white", "a long empty airport corridor flooded with cold white light, polished floor, no people, vanishing-point perspective, lonely, antiseptic"),
 ("T-IMG-002", "black", "a vast concert arena now dark and abandoned, every seat empty, one cold spotlight on a bare stage where someone once stood, dust in the beam, silence"),
 ("T-IMG-012", "black", "an empty private-jet airstair under a single cold white airport light at night, no figure, no luggage, the stair leading up into darkness, desolate"),
 ("T-IMG-013", "black", "a single FBI-style wanted poster pinned in darkness under one harsh light, the photograph area left as a featureless dark silhouette with no face, official, cold"),
 ("T-IMG-014", "black", "black ink slowly unfurling and dispersing into deep black water, a faint blue glow swallowed, then stillness, abstract, void"),
 ("T-IMG-AUX2", "black", "an open ledger book of blank faintly glowing pages on black, a hand turning a page to reveal another blank page, nothing written anywhere, cold light"),
]


def gen(prompt: str) -> bytes:
    payload = {"prompt": prompt, "negative_prompt": NEG, "steps": 40, "cfg_scale": 5.5,
               "sampler_name": "DPM++ 2M", "scheduler": "Karras", "width": 1344, "height": 768,
               "enable_hr": True, "hr_upscaler": "R-ESRGAN 4x+", "hr_scale": 2.0,
               "hr_second_pass_steps": 15, "denoising_strength": 0.35,
               "n_iter": 1, "batch_size": 1, "seed": -1, "save_images": False}
    req = urllib.request.Request(BASE + "/sdapi/v1/txt2img", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    return base64.b64decode(json.loads(urllib.request.urlopen(req, timeout=900).read())["images"][0])


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time(); made = 0; skipped = 0; failed = 0
    total = len(PROMPTS) * N_VAR
    print(f"[start] {len(PROMPTS)} prompts x {N_VAR} = {total} images -> {OUT}", flush=True)
    for tid, color, core in PROMPTS:
        prompt = core + SUFFIX + COLOR[color]
        for v in range(1, N_VAR + 1):
            out = os.path.join(OUT, f"{tid}_v{v}.png")
            if os.path.exists(out):
                skipped += 1; continue
            try:
                t = time.time()
                data = gen(prompt)
                open(out, "wb").write(data)
                h = data[:24]; w_, ht_ = int.from_bytes(h[16:20], "big"), int.from_bytes(h[20:24], "big")
                made += 1
                print(f"[{made+skipped+failed}/{total}] {tid}_v{v} {w_}x{ht_} {len(data)//1024}KB {time.time()-t:.0f}s", flush=True)
            except Exception as exc:  # noqa: BLE001
                failed += 1
                print(f"[FAIL] {tid}_v{v}: {exc}", flush=True)
    print(f"[done] made={made} skipped={skipped} failed={failed} in {(time.time()-t0)/60:.1f}min", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
