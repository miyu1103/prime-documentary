# -*- coding: utf-8 -*-
"""
Generate brand-styled Asset Factory images LOCALLY via the running SDXL (A1111) API on :7860.
Free (local GPU), authorized (CLAUDE.md sec.3 lists local image generation as automated).
Fills gaps stock can't: brand-consistent cinematic backgrounds + ANONYMOUS people (no real-person
likeness). Saves to H:\\pd-media\\assets\\factory\\<category>\\ and registers in asset_manifest.

Usage:
  python scripts/generate_factory_sdxl.py --limit 1            # smoke test (1 image)
  python scripts/generate_factory_sdxl.py --per 6 --write      # full batch
"""
from __future__ import annotations
import sys, os, json, base64, hashlib, time, argparse, urllib.request, re

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "http://127.0.0.1:7860"
MODEL = "juggernautXL_ragnarokBy"  # main photoreal SDXL per project memory
MAN = os.path.join(REPO, "assets", "asset_manifest.v001.json")

STYLE = (", cinematic documentary still, dramatic chiaroscuro lighting, deep navy and black palette "
         "with electric blue and gold rim light, photorealistic, ultra detailed, volumetric light, "
         "subtle film grain, masterpiece, high resolution, 16:9")
NEG = ("text, letters, words, watermark, logo, signature, caption, identifiable face, recognizable real person, "
       "celebrity likeness, deformed, mutated, extra fingers, extra limbs, bad anatomy, bad hands, "
       "low quality, lowres, blurry, jpeg artifacts, cartoon, anime, illustration, oversaturated, ugly")

CAT_CODE = {"backgrounds": "BG", "light_assets": "LIGHT", "vfx_overlays": "VFX", "parallax_layers": "PLX"}

# (category, subtype) -> list of subjects (brand style + negative appended automatically)
JOBS = {
    ("backgrounds", "brand_cinematic"): [
        "a vast dark courtroom bathed in a single cold shaft of light, empty",
        "an abstract dark data network of glowing electric-blue nodes",
        "a moody empty modern office at night with a single warm gold desk lamp",
        "a dramatic stormy sky over a lone classical government building at dusk",
        "a dark interrogation room with one harsh overhead lamp over a steel table",
        "a cold modern forensic laboratory glowing blue at night, empty",
        "a shadowy archive of endless stacked legal documents fading into darkness",
        "a rain-soaked city street at night with electric-blue and gold neon reflections",
        "a fortress-like suburban home glowing warm under a vast dark sky",
        "a sleek server room with rows of blue glowing racks receding into dark",
        "a single empty witness stand under a dramatic spotlight in a dark court",
        "an abstract glowing brass scale of justice in deep shadow",
        "a wall of cold surveillance monitors glowing in a dark room",
        "a dramatic close-up of a gavel resting on a dark bench, gold rim light",
        "a lone desk with scattered case files under a green banker's lamp at night",
    ],
    ("backgrounds", "anonymous_people"): [
        "an anonymous silhouette of a person at a rain-streaked window at night, no face, backlit",
        "anonymous hands signing a document under a desk lamp, close up, no face",
        "a faceless crowd of silhouettes standing in a dim hall, no faces",
        "a lone hooded figure walking away down a dark corridor, no face, backlit",
        "anonymous business figures in silhouette around a boardroom table at night, no faces",
        "a person's blurred silhouette behind frosted glass, no face",
        "anonymous hands holding a glowing smartphone in the dark, close up",
        "a faceless judge silhouette behind a high bench, backlit, no face",
        "an anonymous police officer silhouette standing at a doorway at night, no face",
        "a small child silhouette at a window looking out, no face, emotional, backlit",
        "anonymous handcuffed wrists in shadow, close up, no face",
        "a faceless scientist silhouette working at a glowing lab bench, no face",
        "anonymous hands offering a small blood vial under clinical light, no face",
        "a lone silhouette of a person on empty stadium bleachers at dusk, no face",
        "anonymous commuters as silhouettes on a train platform at night, no faces",
    ],
    ("light_assets", "brand_light"): [
        "electric-blue volumetric light rays piercing dark fog, pure dark background",
        "a warm gold lens flare and light streaks on a pure black background",
        "soft god rays of cold light through a dark window, dust in the air",
    ],
    ("vfx_overlays", "brand_smoke"): [
        "wisps of electric-blue smoke drifting on a pure black background",
        "fine gold dust particles floating on a pure black background",
        "dark atmospheric fog rolling low on a black background",
    ],
}


def post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:40]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="cap total images (smoke test)")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    media = os.environ.get("PD_MEDIA_ROOT", r"H:\pd-media")
    factory = os.path.join(media, "assets", "factory")
    man = json.load(open(MAN, encoding="utf-8")) if os.path.exists(MAN) else {"schema": "asset-manifest/v1", "assets": []}
    counters = {}
    for x in man["assets"]:
        m = re.match(r"^AF-([A-Z_]+)-(\d+)$", x.get("id", ""))
        if m:
            c = x.get("type"); counters[c] = max(counters.get(c, 0), int(m.group(2)))

    made = 0
    for (cat, subtype), subjects in JOBS.items():
        code = CAT_CODE[cat]; outdir = os.path.join(factory, cat); os.makedirs(outdir, exist_ok=True)
        for subj in subjects:
            for k in range(a.per):
                if a.limit and made >= a.limit:
                    if a.write:
                        json.dump(man, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                    print(f"\nlimit reached ({a.limit}). made={made}"); return 0
                seed = 1000 + made  # deterministic, varies per image
                payload = {
                    "prompt": subj + STYLE, "negative_prompt": NEG,
                    "width": 1344, "height": 768, "steps": 30, "cfg_scale": 5.5,
                    "sampler_name": "DPM++ 2M Karras", "seed": seed, "batch_size": 1,
                    "override_settings": {"sd_model_checkpoint": MODEL},
                }
                try:
                    r = post("/sdapi/v1/txt2img", payload)
                    img_b64 = r["images"][0]
                except Exception as e:
                    print(f"  [gen err] {subtype}/{k}: {e}"); time.sleep(2); continue
                if not a.write:
                    print(f"  (dry) would gen {cat}/{subtype} seed={seed}"); made += 1; continue
                raw = base64.b64decode(img_b64.split(",", 1)[-1])
                counters[cat] = counters.get(cat, 0) + 1
                aid = f"AF-{code}-{counters[cat]:04d}"
                fname = f"{aid}__sdxl_{slug(subj)}.png"
                with open(os.path.join(outdir, fname), "wb") as f:
                    f.write(raw)
                sha = hashlib.sha256(raw).hexdigest()
                man["assets"].append({
                    "id": aid, "type": cat, "subtype": subtype,
                    "path": f"factory/{cat}/{fname}", "previewPath": None,
                    "sourceTool": "sdxl", "source": "sdxl", "kind": "image",
                    "durationFrames": None, "fps": None, "width": 1344, "height": 768,
                    "hasAlpha": False, "loopable": False, "mood": None, "intensity": None,
                    "useCases": [cat], "compatibleSceneTypes": [], "colorTone": "navy_gold",
                    "tags": [cat, subtype, "sdxl", "brand"], "sourcePrompt": subj + STYLE,
                    "negativePrompt": NEG, "seed": seed, "model": MODEL,
                    "license": "generated_owned", "sourceUrl": "", "sha256": sha,
                    "bytes": len(raw), "notes": "local SDXL factory generation",
                })
                made += 1
                if made % 10 == 0:
                    json.dump(man, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                    print(f"  ... {made} generated (last {cat}/{subtype})")
    if a.write:
        json.dump(man, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nDONE. generated={made} manifest_total={len(man['assets'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
