"""Generate SDXL coverage stills for PD-2026-004-ftx via local A1111 API.

Local-only: http://127.0.0.1:7860. No upload, no paid API.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import time
import os
from dataclasses import dataclass
from pathlib import Path

import requests

from sdxl_quality_profiles import available_sdxl_profiles, get_sdxl_profile


API = "http://127.0.0.1:7860"
EPISODE_ID = "PD-2026-004-ftx"
OUT_ROOT = Path(r"E:\pd-media\episodes\PD-2026-004-ftx\05_visuals\sdxl_coverage_hq_v001")
MANIFEST = OUT_ROOT / "sdxl_coverage_manifest.v001.json"
BASE_SEED = 40619004

STYLE = (
    "photoreal cinematic documentary still, modern fintech noir, restrained natural colors, "
    "deep charcoal and near-black base, cold teal shadows, sparse acid-green or gold accent, "
    "real camera feel, shallow depth of field, low-key lighting, subtle volumetric haze, "
    "fine 35mm film grain, premium documentary frame, no recognizable real person"
)

NEGATIVE = (
    "cgi, 3d render, illustration, painting, cartoon, anime, oversaturated, hdr, fantasy, "
    "glossy ai art, fake plastic, text, watermark, logo, brand logo, readable letters, "
    "recognizable face, real person likeness, celebrity likeness, deformed face, extra fingers, "
    "bad hands, mutated hands, duplicated people, distorted anatomy, nsfw"
)


@dataclass(frozen=True)
class ShotPrompt:
    shot_id: str
    section: str
    prompt: str


def resolve_profile(profile_name: str) -> dict[str, object]:
    return get_sdxl_profile(profile_name)


PROMPTS: list[ShotPrompt] = [
    ShotPrompt("COV-0001", "00_hook", "silhouette of a person sitting on the edge of a bed at 3am, face hidden in darkness, lit only by a cold phone screen, small bedroom swallowed by black"),
    ShotPrompt("COV-0002", "00_hook", "extreme close-up of a thumb hovering above a glowing withdraw button on a smartphone, tense pause, dark bedroom background, no readable app brand"),
    ShotPrompt("COV-0003", "00_hook", "wide dark bedroom at night with one tiny rectangle of blue phone light, alarm clock shape glowing 3:00 but not readable text, lonely and quiet"),
    ShotPrompt("COV-0004", "00_hook", "macro shot of a phone on wrinkled sheets, frozen loading circle as abstract shape, customer anxiety, no readable brand text"),
    ShotPrompt("COV-0101", "01_cold_open", "a million tiny faceless silhouettes as dots forming a loose map of the United States, each dot faintly lit by phone glow, dark void background"),
    ShotPrompt("COV-0102", "01_cold_open", "anonymous hoodie silhouette at a glowing computer desk, face fully hidden, acid-green monitor light, late-night office, no readable code"),
    ShotPrompt("COV-0103", "01_cold_open", "generic sports arena exterior at night with abstract teal glow and no logos, empty plaza, ominous documentary atmosphere"),
    ShotPrompt("COV-0104", "01_cold_open", "customer deposits represented by small gold coins moving into a locked glass box, then a shadow falling over it, symbolic and restrained"),
    ShotPrompt("COV-0201", "02_opening", "vault interior with neat stacks of gold bars and sealed boxes, cold teal rim light, order before collapse, no text"),
    ShotPrompt("COV-0202", "02_opening", "smartphone on a table showing an abstract safe-balance interface with no readable text, gold reflection on black glass"),
    ShotPrompt("COV-0203", "02_opening", "generic arena exterior glowing at night, crowds as soft silhouettes, no team marks, no logos, money and celebrity spectacle implied"),
    ShotPrompt("COV-0204", "02_opening", "heavy courthouse door seen from a low angle, thin line of cold light underneath, trial ahead, cinematic still"),
    ShotPrompt("COV-1001", "actI_trust", "living room TV casting Super Bowl-like glow onto a couch, anonymous viewers as silhouettes, no logos or readable ad text"),
    ShotPrompt("COV-1002", "actI_trust", "generic stadium concourse with teal brand-like glow but no logos, crowd silhouettes passing under huge blank screens"),
    ShotPrompt("COV-1003", "actI_trust", "athlete-like silhouettes on a dark stage endorsing an unseen product, faces hidden, spotlights, no logos"),
    ShotPrompt("COV-1004", "actI_trust", "large crowd of ordinary customer silhouettes holding phones, tiny gold reflections in screens, trust becoming scale"),
    ShotPrompt("COV-1005", "actI_trust", "trading desk full of glowing monitors at night, no readable charts, frantic reflections, no identifiable faces"),
    ShotPrompt("COV-1006", "actI_trust", "beanbag chair in a glass office after midnight, rumpled hoodie draped over it, executives blurred as silhouettes"),
    ShotPrompt("COV-1007", "actI_trust", "symbolic charity globe on a desk beside stacks of coins, noble promise and hidden risk, dark teal background"),
    ShotPrompt("COV-1008", "actI_trust", "blank magazine cover mockup held in hands, faceless figure silhouette on the cover, fame without identity, no readable text"),
    ShotPrompt("COV-2001", "actII_code", "rows of server racks in a dark data center, one acid-green indicator light blinking in the distance, no readable labels"),
    ShotPrompt("COV-2002", "actII_code", "single server tower behind glass with one glowing green status light, cold controlled composition, hidden switch implied"),
    ShotPrompt("COV-2003", "actII_code", "river of gold coins flowing through a narrow black channel under glass, controlled and secretive, cinematic macro"),
    ShotPrompt("COV-2004", "actII_code", "small house keys on a kitchen table beside a phone and a fading gold reflection, down payment dream, no readable text"),
    ShotPrompt("COV-2005", "actII_code", "open empty wallet under cold phone light, a few coins at the edge, intimate victim-scale detail, no text"),
    ShotPrompt("COV-2006", "actII_code", "ghostly fading account numbers as abstract light bars reflected on a black screen, no readable digits, money vanishing"),
    ShotPrompt("COV-2007", "actII_code", "poker chips arranged like risky bets beside a glowing fintech screen, symbolic gambling with customer money, no logos"),
    ShotPrompt("COV-2008", "actII_code", "dark control room with one empty chair facing many green monitors, power without a visible face, no readable interface"),
    ShotPrompt("COV-3001", "actIII_run", "bankruptcy filing papers on a dark table, official-looking but blank unreadable pages, cold legal atmosphere"),
    ShotPrompt("COV-3002", "actIII_run", "generic news studio monitors showing blurred red alert bars, no readable words, crisis breaking"),
    ShotPrompt("COV-3003", "actIII_run", "empty trading floor after the collapse, chairs pushed back, monitors glowing unattended, desolate"),
    ShotPrompt("COV-3004", "actIII_run", "two abstract exchange-logo shapes turning away from each other, no real logos, support being pulled"),
    ShotPrompt("COV-3005", "actIII_run", "gold chips labeled only by abstract marks tumbling into darkness, billions represented symbolically, no readable numbers"),
    ShotPrompt("COV-3006", "actIII_run", "coins slowly returning along a thin beam of light toward a damaged vault, partial recovery honesty beat, restrained"),
    ShotPrompt("COV-3007", "actIII_run", "arena sign being unbolted at night, blank sign panel, workers as anonymous silhouettes, no real venue name"),
    ShotPrompt("COV-3008", "actIII_run", "black glass office tower with floors going dark one by one, collapse of a financial empire, cinematic wide shot"),
    ShotPrompt("COV-4001", "actIV_verdict", "empty courtroom benches under cold morning light, dust in the air, trial gravity, no people in focus"),
    ShotPrompt("COV-4002", "actIV_verdict", "scales of justice on a dark wooden table, one side lit gold, one side teal, solemn documentary still"),
    ShotPrompt("COV-4003", "actIV_verdict", "two stacks of sentencing chips on a judge's desk, abstract numbers implied but not readable, 115 versus 25 concept"),
    ShotPrompt("COV-4004", "actIV_verdict", "large forfeiture stamp motif on blank legal paper, red ink shape but no readable text, eleven-billion consequence implied"),
    ShotPrompt("COV-4005", "actIV_verdict", "gavel close-up resting on dark wood after impact, jury silhouettes blurred far behind, no faces"),
    ShotPrompt("COV-4006", "actIV_verdict", "empty judge's bench from below, hard overhead light, authority without visible judge, no seal or text"),
    ShotPrompt("COV-5001", "ending", "recap still: secret green-lit door in a concrete wall, vault shadow and gold glint, no text"),
    ShotPrompt("COV-5002", "ending", "recap still: glowing code reflected in a coin, black background, documentary macro, no readable code"),
    ShotPrompt("COV-5003", "ending", "recap still: crater where gold stacks used to be, a courthouse silhouette in the far haze, no text"),
    ShotPrompt("COV-5004", "ending", "recap still: gavel, key, and coin arranged on black velvet, lesson about custody, restrained and cinematic"),
]


def api_get(path: str) -> object:
    response = requests.get(f"{API}{path}", timeout=20)
    response.raise_for_status()
    return response.json()


def api_post(path: str, body: dict, timeout: int = 300) -> object:
    response = requests.post(f"{API}{path}", json=body, timeout=timeout)
    response.raise_for_status()
    return response.json()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def set_model(profile: dict[str, object]) -> None:
    options = api_get("/sdapi/v1/options")
    current = str(options.get("sd_model_checkpoint", ""))
    model = str(profile["model"])
    if model not in current:
        api_post("/sdapi/v1/options", {"sd_model_checkpoint": model}, timeout=120)


def build_request_body(item: ShotPrompt, seed: int, profile: dict[str, object]) -> dict[str, object]:
    prompt = f"{item.prompt}, {STYLE}"
    body: dict[str, object] = {
        "prompt": prompt,
        "negative_prompt": NEGATIVE,
        "steps": int(profile["steps"]),
        "cfg_scale": float(profile["cfg_scale"]),
        "width": int(profile["width"]),
        "height": int(profile["height"]),
        "sampler_name": str(profile["sampler_name"]),
        "scheduler": str(profile["scheduler"]),
        "seed": int(seed),
        "batch_size": 1,
        "n_iter": 1,
        "save_images": False,
        "override_settings": {"sd_model_checkpoint": str(profile["model"])},
    }
    if bool(profile.get("enable_hr", False)):
        body.update(
            {
                "enable_hr": True,
                "denoising_strength": float(profile["denoising_strength"]),
                "hr_scale": float(profile["hr_scale"]),
                "hr_second_pass_steps": int(profile["hr_second_pass_steps"]),
                "hr_upscaler": str(profile["hr_upscaler"]),
            }
        )
    return body


def generate_one(item: ShotPrompt, seed: int, profile: dict[str, object], dry_run: bool) -> dict:
    section_dir = OUT_ROOT / item.section
    section_dir.mkdir(parents=True, exist_ok=True)
    out_path = section_dir / f"{item.shot_id}.png"
    prompt = f"{item.prompt}, {STYLE}"
    record: dict[str, object] = {
        "episode_id": EPISODE_ID,
        "shot_id": item.shot_id,
        "section": item.section,
        "file": str(out_path),
        "prompt": prompt,
        "negative_prompt": NEGATIVE,
        "model": str(profile["model"]),
        "width": int(profile["width"]),
        "height": int(profile["height"]),
        "steps": int(profile["steps"]),
        "cfg_scale": float(profile["cfg_scale"]),
        "sampler_name": str(profile["sampler_name"]),
        "scheduler": str(profile["scheduler"]),
        "seed": seed,
        "quality_profile": str(profile["name"]),
    }
    if dry_run:
        return record
    if out_path.exists():
        record["status"] = "exists"
        record["sha256"] = sha256(out_path)
        return record
    body = build_request_body(item, seed, profile)
    result = api_post("/sdapi/v1/txt2img", body, timeout=360)
    image_bytes = base64.b64decode(result["images"][0])
    out_path.write_bytes(image_bytes)
    record["status"] = "generated"
    record["sha256"] = sha256(out_path)
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Generate only first N prompts.")
    parser.add_argument("--offset", type=int, default=0, help="Skip first N prompts.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--profile",
        default=os.getenv("SDXL_PROFILE", "max"),
        choices=available_sdxl_profiles(),
        help="Quality preset. max=high detail, high quality output.",
    )
    args = parser.parse_args()
    profile = resolve_profile(args.profile)

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    selected = PROMPTS[args.offset :]
    if args.limit:
        selected = selected[: args.limit]

    records: list[dict] = []
    if not args.dry_run:
        api_get("/sdapi/v1/progress")
        set_model(profile)

    started = time.time()
    for idx, item in enumerate(selected, start=args.offset):
        seed = BASE_SEED + idx
        print(f"[{idx + 1}/{len(PROMPTS)}] {item.shot_id} {item.section}", flush=True)
        records.append(generate_one(item, seed, profile, args.dry_run))

    manifest = {
        "episode_id": EPISODE_ID,
        "kind": "sdxl_coverage",
        "count": len(records),
        "total_prompt_count": len(PROMPTS),
        "quality_profile": str(profile["name"]),
        "started_or_updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "duration_sec": round(time.time() - started, 2),
        "local_api": API,
        "external_side_effects": "none",
        "records": records,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(MANIFEST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
