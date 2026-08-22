"""Generate additional high-quality SDXL stills for PD-2026-004-ftx.

These are meant to replace repeated/looping SVD motion with stable, cinematic
still frames that can be animated safely in Remotion.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

import requests

from sdxl_quality_profiles import available_sdxl_profiles, get_sdxl_profile


API = "http://127.0.0.1:7860"
EPISODE_ID = "PD-2026-004-ftx"
OUT_ROOT = Path(r"E:\pd-media\episodes\PD-2026-004-ftx\05_visuals\sdxl_expansion_v001")
MANIFEST = OUT_ROOT / "sdxl_expansion_manifest.v001.json"
BASE_SEED = 40619700

STYLE = (
    "photoreal cinematic documentary still, premium investigative documentary frame, "
    "modern financial crime noir, realistic camera optics, sharp subject, controlled depth of field, "
    "low-key lighting, soft volumetric haze, realistic texture, restrained color grade, "
    "deep charcoal blacks, cold teal shadows, tiny warm gold highlights, 35mm documentary realism, "
    "no recognizable real person"
)

NEGATIVE = (
    "cgi, 3d render, illustration, painting, cartoon, anime, fantasy, surreal, plastic skin, "
    "oversaturated, excessive bloom, hdr, glitch, distorted screen text, readable text, readable letters, "
    "numbers, watermark, logo, brand logo, real company logo, celebrity likeness, recognizable face, "
    "deformed face, bad anatomy, bad hands, extra fingers, duplicated body, crowd faces in focus, nsfw"
)


@dataclass(frozen=True)
class PromptSpec:
    shot_id: str
    section: str
    prompt: str


def specs() -> list[PromptSpec]:
    raw: dict[str, list[str]] = {
        "00_hook": [
            "anonymous customer reflected in a dark phone screen at 3am, only hands and silhouette visible, tense bedroom darkness",
            "smartphone on a kitchen counter in the middle of the night, withdrawal spinner as abstract circle, no readable interface",
            "cold blue phone glow lighting a worried silhouette from behind, face hidden, apartment swallowed by shadow",
            "close-up of a bank card beside a silent phone on black fabric, tiny green status light, quiet panic",
            "empty hallway outside an apartment at night, one door cracked with phone light spilling out, cinematic suspense",
            "macro detail of a finger frozen above a generic withdraw button shape, no readable text, shallow focus",
        ],
        "01_cold_open": [
            "thousands of small phone screens glowing across a dark map-like table, anonymous customer scale, no readable marks",
            "black glass office tower after midnight, a few floors glowing green, financial system secrecy",
            "faceless coder silhouette at a desk with abstract green terminal light, no readable code, controlled menace",
            "gold coins under glass with a dark hand-shaped shadow crossing over them, symbolic custody risk",
            "long corridor of locked deposit boxes, one box slightly ajar with teal light inside",
            "empty fintech lobby at night, glossy floor reflections, blank reception wall, no logo",
            "wide shot of an anonymous customer support floor after hours, chairs empty, monitors dim",
            "abstract money trail represented by gold reflections disappearing into a black server room",
        ],
        "02_opening": [
            "clean vault shelves before a collapse, sealed boxes and gold reflections, cold order and trust",
            "generic balance app interface represented by abstract green and gold bars on a phone, no readable text",
            "huge blank billboard above a night city street, fame and finance implied, no letters or logo",
            "dark studio spotlight on an empty chair, public image without the person, documentary interview mood",
            "hands holding a blank magazine-like cover with faceless silhouette, fame implied, no readable title",
            "low angle courthouse doors at dawn, thin warm light at the threshold, coming accountability",
            "financial district skyline in rain, windows like ledgers, restrained teal-gold palette",
            "single safe deposit key on black velvet beside a phone, promise of custody and risk",
        ],
        "actI_trust": [
            "glass conference room after midnight with beanbag chair and monitors, no people in focus",
            "Super Bowl-like living room glow on a couch, anonymous viewers in silhouette, no logos",
            "blank arena screens above crowd silhouettes, marketing spectacle without readable branding",
            "charity globe on a desk beside stacked coins and a dark laptop, noble promise under suspicion",
            "two office towers connected by a narrow bridge of light, symbolic exchange and hedge fund",
            "messy executive desk with sticky notes blurred beyond readability, phone, glasses, and cold coffee",
            "rows of customer phones on a dark table, each screen a tiny green glow, collective trust",
            "faceless figure in hoodie walking past a glass boardroom, reflection broken by vertical blinds",
            "empty trading office with sleep bag under a desk, exhaustion and power implied",
            "gold coins moving through transparent tubes between two dark buildings, no labels",
            "close-up of an unsigned pledge document beside a pen and coin, all text out of focus",
            "luxury event stage with blank back wall and spotlights, faceless silhouettes, no logos",
            "quiet boardroom table with two nameplates turned away, teal reflections, no readable names",
            "stack of customer account cards as abstract blank rectangles, sorted neatly then shadowed",
        ],
        "actII_code": [
            "data center aisle with one green-lit cabinet slightly open, hidden exception implied, no labels",
            "macro shot of a server status light reflected in a coin, technical loophole mood",
            "abstract black control panel with one green switch glowing, no readable labels",
            "glass wall between gold coins and a dark server room, secret path implied",
            "open empty wallet beside a phone on a kitchen table, personal loss without text",
            "dark monitor showing only blurred green bars and shapes, no readable code or digits",
            "narrow channel of gold reflections flowing under a locked grate, siphon symbolism",
            "faceless engineer chair in front of many dim screens, no readable interface",
            "close-up of a keycard on black desk next to a coin and green light strip",
            "abstract ledger pages as blank pale sheets under teal light, no readable lines",
            "vault door edge with thin green light leaking from a hidden side entrance",
            "black server rack corridor bending around a corner, secret route, documentary realism",
            "customer savings represented by a small stack of coins on a family table, phone glow nearby",
            "high angle of two separated cash trays connected by a thin illuminated line",
            "blank compliance checklist on clipboard, boxes visible but no words, ominous office light",
            "coin balanced on a red glass barrier, risk threshold, no text",
            "dark room with reflected graph shapes on glass, no readable numbers, money uncertainty",
            "single drawer half-open with blank financial papers and a cold green glow",
        ],
        "actIII_run": [
            "large crowd silhouettes outside a glass financial office in rain, panic without faces",
            "empty trading floor with monitors abandoned, chairs pushed back, collapse aftermath",
            "phone screens lined up on a table all showing abstract red warning blocks, no readable words",
            "gold chips sliding toward darkness on black glass, billions vanishing symbolically",
            "black office tower with floors going dark one by one, financial empire collapse",
            "blank news studio wall with red light reflections, crisis broadcast implied, no text",
            "damaged vault interior with empty shelves and dust in the air, no people",
            "papers scattered across a conference table, bankruptcy atmosphere, all text unreadable",
            "night exterior of a generic arena with blank sign panel being removed, no name or logo",
            "thin beam of light crossing a field of scattered coins, partial recovery uncertainty",
            "empty customer service desk with ringing phone implied by light, no screen text",
            "close-up of unplugged server cable beside gold coin, sudden stop, teal shadows",
            "dark city street reflected in a puddle with falling gold flecks, collapse mood",
            "anonymous hands holding a phone over a sink, screen abstract red shape, no text",
            "warehouse-like office with boxed documents and blank labels, post-collapse evidence",
            "glass doors of a closed office with paper notices blurred beyond reading",
            "wide night shot of people as silhouettes under umbrellas outside a tower, no faces",
            "empty desk with two phones face down and a stack of blank legal papers",
        ],
        "actIV_trial": [
            "empty courtroom from the witness stand perspective, solemn light, no judge or jurors visible",
            "witness chair under a hard overhead light, dark courtroom background, no people",
            "jury box as blurred empty wooden seats, cold morning light, no faces",
            "close-up of a microphone at a courtroom desk, polished wood, dust in light",
            "scales of justice on dark table, teal and gold split lighting, no text",
            "blank evidence folders stacked neatly on a courtroom table, no readable labels",
            "courthouse hallway at dawn with long shadows, faceless silhouettes far away",
            "wooden bench and gavel in foreground, courtroom depth behind, no seal or text",
            "legal pad with blank pages and pen beside a glass of water, trial tension",
            "empty prosecution table and defense table facing each other, low cinematic angle",
        ],
        "actV_verdict": [
            "gavel just after impact on dark wood, jury silhouettes blurred far behind, no faces",
            "prison corridor door with narrow vertical light, no visible person, solemn",
            "blank sentencing papers under red-edged shadow, no readable text or numbers",
            "forfeiture represented by gold coins sealed inside a clear evidence box, no labels",
            "courtroom clock silhouette out of focus above empty benches, verdict time implied",
            "heavy steel door closing with warm light disappearing, no person visible",
            "single chair under courtroom spotlight, aftermath and accountability, no text",
            "dark wooden table with gavel, key, and coin arranged apart, judgement and custody",
            "courthouse steps at night after rain, no crowds, reflections and silence",
            "abstract prison bars shadow falling across blank legal paper, no readable marks",
        ],
        "ending": [
            "safe deposit key and coin on black velvet, final lesson about custody, no text",
            "secret green-lit door in concrete wall, vault shadow behind, no readable signs",
            "old ledger book with blank pages beside a coin and candle, history repeating",
            "dark ocean-like surface with scattered gold reflections fading into distance",
            "empty desk after an investigation, lamp pool of light, blank notes and coin",
            "gavel, phone, and key arranged in a triangle on dark wood, restrained final image",
            "faceless silhouette leaving a dark office corridor, tiny green exit light",
            "macro coin edge lit like a horizon, abstract finance lesson, no text",
            "closed vault door from inside a dark room, final lockup mood",
            "blank documentary end tableau: key, paper, phone, and coin under soft overhead light",
            "small stack of coins protected under a glass dome, custody and caution, no words",
            "wide black room with one open door spilling teal light, final unresolved question",
        ],
    }
    out: list[PromptSpec] = []
    prefixes = {
        "00_hook": "X-HOOK",
        "01_cold_open": "X-COLD",
        "02_opening": "X-OPEN",
        "actI_trust": "X-TRUST",
        "actII_code": "X-CODE",
        "actIII_run": "X-RUN",
        "actIV_trial": "X-TRIAL",
        "actV_verdict": "X-VERDICT",
        "ending": "X-END",
    }
    for section, prompts in raw.items():
        prefix = prefixes[section]
        for index, prompt in enumerate(prompts, start=1):
            out.append(PromptSpec(f"{prefix}-{index:03d}", section, prompt))
    return out


SPECS = specs()


def resolve_profile(profile_name: str) -> dict[str, object]:
    return get_sdxl_profile(profile_name)


def api_get(path: str) -> object:
    response = requests.get(f"{API}{path}", timeout=20)
    response.raise_for_status()
    return response.json()


def api_post(path: str, body: dict, timeout: int = 420) -> object:
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
        api_post("/sdapi/v1/options", {"sd_model_checkpoint": model}, timeout=180)


def build_request_body(item: PromptSpec, seed: int, profile: dict[str, object]) -> dict[str, object]:
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


def generate_one(item: PromptSpec, seed: int, profile: dict[str, object], dry_run: bool, force: bool) -> dict:
    section_dir = OUT_ROOT / item.section
    section_dir.mkdir(parents=True, exist_ok=True)
    out_path = section_dir / f"{item.shot_id}.png"
    record = {
        "episode_id": EPISODE_ID,
        "shot_id": item.shot_id,
        "section": item.section,
        "file": str(out_path),
        "prompt": f"{item.prompt}, {STYLE}",
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
        record["status"] = "dry_run"
        return record
    if out_path.exists() and not force:
        record["status"] = "exists"
        record["sha256"] = sha256(out_path)
        return record
    body = build_request_body(item, seed, profile)
    result = api_post("/sdapi/v1/txt2img", body, timeout=480)
    out_path.write_bytes(base64.b64decode(result["images"][0]))
    record["status"] = "generated"
    record["sha256"] = sha256(out_path)
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--profile",
        default=os.getenv("SDXL_PROFILE", "max"),
        choices=available_sdxl_profiles(),
        help="Quality preset. max=highest quality output.",
    )
    args = parser.parse_args()
    profile = resolve_profile(args.profile)

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    selected = SPECS[args.offset :]
    if args.limit:
        selected = selected[: args.limit]

    if not args.dry_run:
        api_get("/sdapi/v1/progress")
        set_model(profile)

    started = time.time()
    records: list[dict] = []
    for absolute_index, item in enumerate(selected, start=args.offset):
        seed = BASE_SEED + absolute_index
        print(f"[{absolute_index + 1}/{len(SPECS)}] {item.shot_id} {item.section}", flush=True)
        records.append(generate_one(item, seed, profile, args.dry_run, args.force))

    manifest = {
        "episode_id": EPISODE_ID,
        "kind": "sdxl_expansion",
        "quality": str(profile["name"]),
        "quality_profile": str(profile["name"]),
        "count": len(records),
        "total_prompt_count": len(SPECS),
        "started_or_updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "duration_sec": round(time.time() - started, 2),
        "local_api": API,
        "external_side_effects": "none",
        "records": records,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(MANIFEST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
