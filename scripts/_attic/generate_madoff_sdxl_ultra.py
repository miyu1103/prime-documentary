#!/usr/bin/env python3
"""Generate higher-detail SDXL replacement stills for Madoff.

Focus: fewer, denser, more cinematic images for core scenes.
Local A1111 only.
"""
from __future__ import annotations

import base64
import json
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-005-madoff"
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_ultra_v002"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "premium cinematic documentary key art, extremely detailed symbolic noir, expensive editorial still, "
    "dark graphite black and warm gold palette, precise realistic materials, polished brass, textured paper, "
    "volumetric light, controlled haze, shallow depth of field, subtle film grain, high micro-contrast, "
    "faceless anonymous silhouettes only, no recognizable person, no portrait likeness, no readable text, no logos"
)
NEG = (
    "pink, magenta, neon, candy colors, readable words, fake letters, watermark, signature, logo, "
    "face, facial features, celebrity, Bernie Madoff likeness, portrait, bad anatomy, deformed hands, "
    "extra fingers, blurry, low detail, cheap render, cartoon, anime, plastic, oversaturated, noisy, jpeg artifacts"
)

PROMPTS = [
    ("U01_perfect_line_statement", "hook", "a pristine cream-colored financial statement on a black marble desk, a single smooth gold return curve printed as a chart, brass desk lamp reflection, no readable text, macro paper texture"),
    ("U02_line_in_dark_room", "hook", "a vast black room with only a floating smooth golden return curve illuminating dust in the air, one tiny faceless silhouette observing it from below"),
    ("U03_trusted_wall_street_name", "opening", "a monumental polished brass nameplate without readable letters, mounted on black stone, warm gold rim light, prestige and menace, no text"),
    ("U04_private_club_door", "actI", "exclusive dark wood investment office door half-open, velvet rope, warm golden light spilling out, no signage, no readable letters"),
    ("U05_elite_investor_table", "actI", "faceless wealthy investors around a long mahogany table, all focused on a glowing gold chart, cinematic overhead composition"),
    ("U06_empty_trading_desk", "actII", "empty trading desk at night, monitors off, dusty keyboard, bank ledger drawer open with cash inside, amber spotlight"),
    ("U07_bank_account_vault_drawer", "actII", "cash disappearing into a plain bank account drawer rather than a trading floor, precise metal drawer details, symbolic no-real-trades image"),
    ("U08_ponzi_coin_loop", "actII", "faceless gloved hands passing gold coins in a circular loop, elegant but ominous, sharp focus on coins, background fades to black"),
    ("U09_fake_statement_storm", "actII", "hundreds of cream account statements swirling in a dark hall like paper snow, gold edges catching light, no readable words"),
    ("U10_empty_vault", "actII", "huge bank vault door open to complete darkness, one last gold coin on the floor, cinematic wide shot"),
    ("U11_analyst_midnight", "actIII", "lone faceless analyst at midnight with calculator, coffee, annotated chart shapes, brass lamp, dense paper texture, no readable text"),
    ("U12_red_flags_chart", "actIII", "close macro shot of a printed chart with red circles and pencil marks, smooth gold line, no readable text, investigative mood"),
    ("U13_unopened_warnings", "actIII", "stack of sealed warning envelopes outside a cold institutional stone door, dramatic corridor perspective, no text"),
    ("U14_sleeping_watchtower", "actIII", "dark regulatory watchtower with the searchlight off, gold fog and distant city lights, symbolic institutional failure"),
    ("U15_2008_withdrawal_panic", "actIV", "faceless crowd rushing through a marble financial lobby toward a single teller window, panic, motion blur, gold-black palette"),
    ("U16_drained_vault_floor", "actIV", "drained vault interior with scattered receipts and one rolling coin, deep shadows, high detail"),
    ("U17_federal_court_steps", "actIV", "federal courthouse steps at dusk, anonymous silhouette ascending, columns, gold sunset edge light, no signage"),
    ("U18_prison_corridor", "actIV", "prison corridor with a steel door closing, thin gold light narrowing, cinematic depth"),
    ("U19_recovery_coins_return", "actIV", "gold coins flowing back from darkness into open anonymous hands, bittersweet restitution, high detail"),
    ("U20_smooth_vs_real", "ending", "two abstract investment paths in a dark void, one smooth gold and one jagged silver, elegant symbolic contrast, no text"),
    ("U21_final_doubt", "ending", "single faceless investor silhouette pausing before a perfect glowing gold line, choosing doubt, atmospheric wide shot"),
    ("U22_thumbnail_bright", "thumbnail", "bright premium YouTube documentary thumbnail background, cream financial statement and gold chart, black and gold contrast, no text, clean negative space"),
    ("U23_thumbnail_vault", "thumbnail", "bright gold-lit empty vault with a smooth chart reflection on the floor, high contrast, no text, cinematic thumbnail background"),
    ("U24_thumbnail_statement_macro", "thumbnail", "macro luxury financial statement with gold rising line, bright cream and black contrast, no text, crisp paper fibers"),
]


def post(payload: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=360) as r:
        return json.loads(r.read().decode("utf-8"))


def save(b64: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {"episode_id": EP, "set": "sdxl_ultra_v002", "items": [], "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    base_seed = 620000
    total = len(PROMPTS) * 3
    n = 0
    for item_id, section, core in PROMPTS:
        for c in range(3):
            n += 1
            seed = base_seed + n * 101
            prompt = f"{core}, {STYLE}"
            payload = {
                "prompt": prompt,
                "negative_prompt": NEG,
                "seed": seed,
                "subseed": seed + 999,
                "subseed_strength": 0.12,
                "sampler_name": "DPM++ 2M Karras",
                "scheduler": "Karras",
                "steps": 52,
                "cfg_scale": 5.0,
                "width": 1536,
                "height": 864,
                "batch_size": 1,
                "n_iter": 1,
                "enable_hr": True,
                "hr_resize_x": 2304,
                "hr_resize_y": 1296,
                "hr_second_pass_steps": 24,
                "denoising_strength": 0.22,
                "hr_upscaler": "Latent",
                "restore_faces": False,
                "do_not_save_samples": True,
                "do_not_save_grid": True,
            }
            result = post(payload)
            out = OUT / section / f"{item_id}_c{c+1:02d}_seed{seed}.png"
            save(result["images"][0], out)
            meta = {"id": item_id, "section": section, "candidate": c + 1, "seed": seed, "path": str(out), "prompt": prompt}
            out.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", "utf-8")
            manifest["items"].append(meta)
            print(f"[{n:02d}/{total}] {out}")
            if n % 6 == 0:
                (OUT / "asset_manifest.v002.partial.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    manifest["count"] = len(manifest["items"])
    (OUT / "asset_manifest.v002.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"done count={len(manifest['items'])} out={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
