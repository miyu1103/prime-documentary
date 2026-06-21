# -*- coding: utf-8 -*-
"""
Asset Factory bulk library builder.
Reuses fetch_stock.py's Pexels/Pixabay helpers (no second implementation) to pull a LARGE,
commercial-OK, rights-clean visual library into H:\\pd-media\\assets\\factory\\<category>\\
and registers every item into assets/asset_manifest.v001.json (AF-<CAT>-NNNN ids).

Idempotent: skips source ids already in the manifest. Safe to re-run / resume.
Only uses Pexels License + Pixabay Content License (both commercial-OK, no attribution required).

Usage:
  python scripts/build_factory_library.py --per-image 30 --per-video 12 --write
  python scripts/build_factory_library.py --only backgrounds,light_assets --per-image 10 --write
  (no --write = dry plan / counts only)
"""
from __future__ import annotations
import sys, os, json, time, argparse, importlib.util, re

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- reuse fetch_stock helpers (no duplication) ---
spec = importlib.util.spec_from_file_location("fetch_stock", os.path.join(REPO, "scripts", "fetch_stock.py"))
fs = importlib.util.module_from_spec(spec); spec.loader.exec_module(fs)

CAT_CODE = {
    "backgrounds": "BG", "light_assets": "LIGHT", "particle_assets": "PART",
    "vfx_overlays": "VFX", "texture_assets": "TEX", "loops": "LOOP",
}

# category -> (asset_kinds, [queries]).  kinds: 'image','video','both'
CATEGORIES: dict[str, tuple[str, list[str]]] = {
    "backgrounds": ("both", [
        "dark cinematic background", "abstract dark background", "moody atmosphere fog",
        "concrete wall texture dark", "blurred city night bokeh", "office interior dark",
        "courtroom interior", "law library books", "government building exterior",
        "american flag waving", "money cash counting", "stock market screen", "server room blue",
        "data center", "technology abstract blue", "circuit board macro", "documents on desk",
        "newspaper macro", "rain on window night", "city skyline dusk", "highway night long exposure",
        "suburban house exterior night", "front door house", "prison corridor", "police car lights night",
        "smartphone in dark", "laboratory glassware", "modern medical lab", "warehouse interior dark",
        "empty stadium seats", "school hallway empty", "bank building columns", "spotlight on dark stage",
        "crowd silhouette", "lone person silhouette walking", "foggy forest", "stormy sky time lapse",
        "ocean horizon moody", "mountain silhouette dusk", "empty road sunset", "old keys on table",
        "handshake business", "courthouse steps", "judge gavel wooden", "surveillance camera city",
        "us constitution document", "supreme court building", "police badge close up", "jail cell bars",
        "evidence bag", "dna laboratory blue", "blood sample vial", "microscope lab", "circuit data flow",
        "city traffic night long exposure", "empty office cubicles", "boardroom table dark",
        "cash stacks money", "bank vault door", "contract paperwork signing", "fingerprint scan blue",
        "mobile phone map location", "cell tower silhouette", "broken house demolition", "moving boxes empty room",
        "rural road america", "small town main street", "storm clouds dramatic", "rain street reflection night",
        "candle in dark", "clock ticking macro", "chess board dramatic", "balance scale brass",
        "old library archive", "stacked legal documents", "newspaper printing press", "vintage typewriter",
        "rain on glass macro", "snowy street night", "candlelit room dark", "fireplace embers close",
        "city rooftop dusk", "subway tunnel empty", "airport terminal empty", "hospital corridor night",
        "operating room", "pills macro", "test tubes rack lab", "binary code screen green",
        "padlock and chain", "shattered mirror", "spotlight smoke stage", "wooden desk lamp night",
        "gold bars stacked", "trading floor screens", "stock chart crashing red", "stock chart rising green",
        "world map dark glowing", "globe spinning dark", "satellite earth at night", "drone city aerial night",
        "forest fog morning", "lighthouse in storm", "lone tree in field", "cemetery fog",
        "church interior light beam", "antique brass scales", "wax seal on document", "quill and ink pot",
        "courtroom empty wide", "jury box empty", "witness stand empty", "police station at night",
        "evidence locker shelves", "crime scene tape night", "magnifying glass on document",
        "long shadow of a person", "silhouette crowd at protest", "empty boardroom at night",
        "vintage radio microphone", "rotary phone close up", "security monitors wall", "fingerprint dust lift",
        "open safe empty", "burning paper documents", "ballot box voting", "capitol dome dusk",
        "abandoned factory interior", "foggy harbor dawn", "train platform night", "empty parking garage",
        "elevator interior steel", "cctv monitor grid wall", "american suburb aerial", "white picket fence",
        "for sale sign yard", "moving truck loading", "law books spines macro", "lady justice statue",
        "white house exterior", "federal building columns night", "prison yard fence", "barbed wire fence sky",
        "police interrogation room empty", "one way mirror room", "case files stack desk", "shredded documents pile",
        "safe deposit boxes vault", "money counting machine", "stock ticker board", "wall street sign",
        "charging bull statue", "atm machine at night", "credit card macro chip", "physical bitcoin coin",
        "fiber optic cables glowing", "hacker hoodie keyboard dark", "smartphone notification glow",
        "cell tower at sunset", "satellite dish array", "city surveillance camera dome", "dna double helix render",
        "laboratory centrifuge", "blood vials in rack", "microscope slide macro", "hospital waiting room empty",
        "ekg heart monitor", "ambulance lights at night", "lone figure with umbrella in rain",
        "person at window silhouette night", "elderly hands close up", "empty playground at dusk",
        "school bus yellow", "graduation cap toss", "protest crowd signs", "voting booth curtain",
        "vintage tv static", "radio tower at night", "stormy ocean waves dark", "desert highway heat haze",
        "mountain road in fog", "snowy forest path", "city bridge night long exposure", "rain on city street neon",
        "courtroom gavel block macro", "stack of hundred dollar bills", "open briefcase of cash",
        "chains and padlock rusty", "broken window glass shards", "single chair empty room",
    ]),
    "light_assets": ("both", [
        "light leak overlay", "lens flare", "bokeh lights", "god rays light", "sun flare warm",
        "light streaks motion", "glowing light particles", "neon glow abstract", "soft golden light",
        "anamorphic lens flare blue", "warm window light rays", "projector beam dust", "neon sign reflection wet",
        "candle flame macro", "sun through trees forest", "caustics water light", "spotlight in darkness",
        "bokeh city lights blur", "blue light leak", "golden hour flare", "flashlight beam fog",
        "stage spotlight beams haze", "police strobe red and blue", "tv screen glow on face", "match strike flame",
        "lantern in fog", "moonlight through clouds", "headlights in rain", "neon underglow city",
    ]),
    "particle_assets": ("both", [
        "dust particles floating", "bokeh particles dark", "embers floating", "snow falling dark",
        "floating dust in light beam", "sparks slow motion", "ash falling", "glitter particles",
        "floating pollen backlit", "confetti slow motion dark", "rain particles backlit", "fireflies at night",
        "embers rising black background", "dust motes sunlight", "bubbles underwater dark", "static noise particles",
        "snow blizzard night", "heavy rain backlit", "leaves blowing in wind", "paper scraps flying",
        "sand blowing desert", "glowing embers fireplace", "plankton bioluminescence", "spark shower welding",
    ]),
    "vfx_overlays": ("both", [
        "smoke on black background", "fog rolling", "ink in water", "smoke wisp dark",
        "dust cloud", "steam rising", "mist atmosphere",
        "fire flames black background", "water splash black background", "ink drop in water slow motion",
        "colored smoke explosion", "dust explosion black", "electric spark", "fog machine stage",
        "cloud time lapse dark", "smoke trail slow", "paper burning edge",
        "explosion fireball black", "lightning strike night", "tear gas smoke cloud", "ink bloom water",
        "shockwave heat distortion", "colored powder burst", "waterfall mist", "frost forming time lapse",
    ]),
    "texture_assets": ("image", [
        "old paper texture", "grunge texture dark", "film grain texture", "scratched film",
        "noise texture", "concrete texture", "parchment texture", "dark marble texture",
        "rusted metal texture", "cracked paint texture", "dark wood texture", "leather texture",
        "fabric weave texture", "watercolor paper texture", "blueprint paper", "vintage map texture",
        "brushed steel texture", "stone wall texture", "canvas texture", "aged document texture",
    ]),
    "loops": ("video", [
        "abstract loop dark", "slow gradient motion", "atmospheric loop", "particle loop dark",
        "looping smoke dark", "looping particles blue", "looping gradient navy", "looping light rays",
        "data stream loop", "abstract network nodes loop", "slow rotation abstract",
    ]),
}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:40]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-image", type=int, default=30)
    ap.add_argument("--per-video", type=int, default=12)
    ap.add_argument("--only", default="")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    env = fs.load_env()
    pk, xk = env.get("PEXELS_API_KEY"), env.get("PIXABAY_API_KEY")
    if not pk and not xk:
        print("NO API KEYS in .env (PEXELS_API_KEY / PIXABAY_API_KEY). Abort."); return 2
    media = fs.media_root() or "H:\\pd-media"
    factory = os.path.join(media, "assets", "factory")

    man_path = os.path.join(REPO, "assets", "asset_manifest.v001.json")
    os.makedirs(os.path.dirname(man_path), exist_ok=True)
    if os.path.exists(man_path):
        man = json.load(open(man_path, encoding="utf-8"))
    else:
        man = {"schema": "asset-manifest/v1", "assets": []}
    seen = {x.get("_srcId") for x in man["assets"]}
    counters = {}
    for x in man["assets"]:
        c = x.get("type")
        counters[c] = max(counters.get(c, 0), int(x["id"].split("-")[-1]))

    only = set(s.strip() for s in a.only.split(",") if s.strip())
    cats = {k: v for k, v in CATEGORIES.items() if (not only or k in only)}

    # ensure all 14 factory folders exist (even ones filled later by MJ/Runway/Lottie)
    for c in ["backgrounds", "parallax_layers", "vfx_overlays", "loops", "transitions",
              "typography_assets", "diagram_assets", "sfx", "ai_video_shots", "lottie_assets",
              "ui_motion_assets", "texture_assets", "light_assets", "particle_assets"]:
        os.makedirs(os.path.join(factory, c), exist_ok=True)

    added = 0; dl_err = 0; planned = 0
    for cat, (kinds, queries) in cats.items():
        code = CAT_CODE[cat]
        outdir = os.path.join(factory, cat)
        for q in queries:
            cands = []
            try:
                if kinds in ("image", "both"):
                    if pk: cands += fs.pexels_image(q, pk, a.per_image)
                    if xk: cands += fs.pixabay_image(q, xk, a.per_image)
                if kinds in ("video", "both"):
                    if pk: cands += fs.pexels_video(q, pk, a.per_video)
                    if xk: cands += fs.pixabay_video(q, xk, a.per_video)
            except Exception as e:
                print(f"  [api err] {cat}/{q}: {e}"); time.sleep(2); continue
            new = [c for c in cands if c["id"] not in seen]
            planned += len(new)
            if not a.write:
                print(f"  (plan) {cat:<16} {q:<32} +{len(new)}"); continue
            for c in new:
                counters[cat] = counters.get(cat, 0) + 1
                aid = f"AF-{code}-{counters[cat]:04d}"
                fname = f"{aid}__{slug(q)}{c['ext']}"
                dest = os.path.join(outdir, fname)
                try:
                    sha, nbytes = fs.download(c["dl"], dest)
                except Exception as e:
                    dl_err += 1; counters[cat] -= 1; print(f"  [dl err] {c['id']}: {e}"); continue
                seen.add(c["id"])
                man["assets"].append({
                    "id": aid, "type": cat, "subtype": slug(q),
                    "path": f"factory/{cat}/{fname}", "previewPath": None,
                    "sourceTool": "stock", "source": c["source"], "_srcId": c["id"],
                    "kind": c["type"], "durationFrames": None, "fps": None,
                    "width": None, "height": None, "hasAlpha": False, "loopable": cat == "loops",
                    "mood": None, "intensity": None,
                    "useCases": [cat], "compatibleSceneTypes": [], "colorTone": None,
                    "tags": [cat, slug(q), c["source"]],
                    "sourcePrompt": q, "negativePrompt": None, "seed": None,
                    "license": c["license"], "sourceUrl": c.get("url", ""),
                    "sha256": sha, "bytes": nbytes, "notes": "stock factory bulk",
                })
                added += 1
                if added % 25 == 0:
                    json.dump(man, open(man_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                    print(f"  ... {added} downloaded (last {cat}/{q})")
            time.sleep(1.0)  # be gentle on APIs
    if a.write:
        json.dump(man, open(man_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nDONE. added={added} dl_err={dl_err} manifest_total={len(man['assets'])} -> {man_path}")
    else:
        print(f"\n(plan) would fetch ~{planned} new candidates. pass --write to download.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
