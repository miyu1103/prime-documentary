#!/usr/bin/env python3
"""Generate and register 180 premium Riley v004 visual plates.

Local A1111 SDXL only. No upload, no paid API, no script/claims edits.
The generated plates are copied into remotion/public so RileyPremium can use
all 180 as timed background plates with motion/crossfades.
"""
from __future__ import annotations

import base64
import hashlib
import json
import shutil
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-007-riley"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
OUT = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_hq_v004_180"
PUBLIC_ROOT = ROOT / "remotion" / "public" / "riley" / "v004_180"
REPO_MANIFEST = EPDIR / "05_visuals" / "riley_hq_180_v004_manifest.json"
TS_OUT = ROOT / "remotion" / "src" / "data" / "riley_v004_plates.ts"
API = "http://127.0.0.1:7860/sdapi/v1/txt2img"

STYLE = (
    "museum-quality premium documentary key art, cinematic legal-tech privacy thriller, "
    "physically plausible editorial photography, deep black and navy palette, electric-blue practical data light, "
    "restrained gold legal accent, glossy glass, wet stone, fine fabric texture, dust motes, volumetric haze, "
    "rich atmospheric depth, elegant negative space, strong subject hierarchy, expensive poster finish, "
    "mature serious tone, symbolic reconstruction, no authentic footage, no readable text"
)

NEG = (
    "readable text, letters, numbers, captions, UI text, app icons, logos, watermark, signature, official court seal, "
    "license plate, address, real person, identifiable face, portrait, David Riley likeness, Brima Wurie likeness, "
    "judge portrait, police badge text, gun pointed at viewer, blood, gore, sensational crime scene, gang imagery, "
    "cheap cyberpunk, neon overload, cluttered interface, cartoon, anime, flat vector, plastic CGI, low detail, blurry, "
    "pixelated, jpeg artifacts, warped phone, melted phone, duplicate phone, broken perspective, bad hands, extra fingers, "
    "oversaturated, muddy shadows"
)

VARIANTS = [
    "wide establishing frame, strong foreground and deep background, clean title-safe negative space",
    "macro detail plate, glass reflection, shallow depth of field, tactile surface texture",
    "low-angle cinematic composition, blue practical light cutting through darkness",
    "overhead editorial still life, crisp geometry, legal evidence table feeling",
    "side-lit noir tableau, foreground obstruction for parallax, restrained gold edge light",
    "minimal black-space composition, one precise legal/privacy symbol, elegant contrast",
    "rainy reflective surface, wet pavement or polished black stone, subtle bokeh",
    "architectural depth frame, corridor or columns receding into darkness, no people",
    "compressed telephoto look, luminous data shapes layered behind a real object",
    "hero frame, balanced poster composition, premium YouTube documentary finish",
]


@dataclass(frozen=True)
class ScenePrompt:
    scene_id: str
    start: float
    duration: float
    kind: str
    core: str


SCENES = [
    ScenePrompt("S001", 0, 28, "hook", "modern unbranded black smartphone half pulled from a dark coat pocket on wet roadside fabric, blue police-light reflection across black glass, no face, no badge"),
    ScenePrompt("S002", 28, 44, "opening", "single smartphone upright on black glass opening into translucent private-life layers: blurred photo cards without faces, unreadable messages, map dots, cloud panes"),
    ScenePrompt("S003", 72, 22, "roadside", "anonymous Southern California roadside stop at night, cropped car door, rain-slick asphalt, blue light bokeh, generic phone and keys on hood edge"),
    ScenePrompt("S004", 94, 22, "pocket", "phone removed from pocket as symbolic evidence, cropped anonymous hands only, dark car interior reflections, no face, no logo, no readable UI"),
    ScenePrompt("S005", 116, 32, "warrant", "locked smartphone on dark evidence table, blank warrant-like paper shape as gold light, courthouse columns blurred in background, no official seal"),
    ScenePrompt("S006", 148, 18, "case_bridge", "traffic-stop evidence bridge, abstract car silhouette, phone, keys, and case-file forms on black stone, restrained blue and gold light"),
    ScenePrompt("S007", 166, 28, "two_cases", "two generic phones side by side, one smartphone and one older flip-phone-like object, dark court table, linked by blue evidence line"),
    ScenePrompt("S008", 194, 12, "old_rule", "old search-incident-to-arrest doctrine visualized as worn blank legal paper forms beside a modern black phone, no readable marks"),
    ScenePrompt("S009", 206, 32, "rationales", "officer-safety and evidence-preservation rationales as two abstract legal objects facing a sealed smartphone, precise blue and gold split lighting"),
    ScenePrompt("S010", 238, 23, "wallet_phone", "wallet-like leather object and smartphone on dark table, contrast between small physical item and deep glowing data volume, no card data"),
    ScenePrompt("S011", 261, 30, "smartphone_depth", "modern smartphone as deep archive, glass layers of private data receding into darkness, unreadable blocks and abstract thumbnails only"),
    ScenePrompt("S012", 291, 24, "cloud", "phone in pocket-like darkness connected to a distant cloud-shaped glass volume, blue dots and clean light strands only, completely blank black phone screens, no panels, no cards, no documents, no app icons, no real UI, no text-like marks"),
    ScenePrompt("S013", 315, 26, "secure_device", "secured smartphone in dark evidence locker, lock glow on screen, legal restraint mood, no text, no human figure"),
    ScenePrompt("S014", 341, 26, "court_result", "abstract Supreme Court-like chamber with columns, no justices, no portraits, phone and gold legal light in foreground"),
    ScenePrompt("S015", 367, 25, "privacies_life", "anonymous life mosaic emerging from a locked phone: calendar blocks, blurred photos without faces, health bars, map dots, intimate and beautiful"),
    ScenePrompt("S016", 392, 24, "house_phone", "empty abstract house outline and smartphone as two privacy containers, phone revealing deeper luminous rooms, no human silhouettes, no figures, no faces, dark editorial composition"),
    ScenePrompt("S017", 416, 20, "get_warrant", "locked phone under narrow gold warrant beam on courthouse stone, authoritative minimalist frame, no readable document"),
    ScenePrompt("S018", 436, 27, "katz", "1960s-style glass phone booth as anonymous privacy metaphor, silhouetted empty interior, no person, blue and gold legal light"),
    ScenePrompt("S019", 463, 18, "category_rule", "entire phone category represented by many generic device silhouettes behind one locked foreground phone, clean legal taxonomy image"),
    ScenePrompt("S020", 481, 10, "emergency", "true emergency exception as urgent blue light outside a sealed phone boundary, abstract siren glow and locked phone with an entirely blank black screen, no signs, no readable labels, no UI, no text-like marks"),
    ScenePrompt("S021", 491, 26, "contents_protected", "phone contents protected by luminous lock and layered private archive behind glass, warrant consent emergency as abstract three gates"),
    ScenePrompt("S022", 517, 28, "life_archive", "single locked smartphone on dark polished glass, abstract blue and gold light particles suggesting private life data, soft blurred color fields only, no cards, no panels, no documents, no charts, no UI, no text-like marks"),
    ScenePrompt("S023", 545, 24, "automatic_records", "automatic records forming behind a phone without user touch, blue data trail leaving black glass, ominous but elegant"),
    ScenePrompt("S024", 569, 12, "inside_vs_trail", "split symbolic composition: glowing phone contents on one side, external location trail on the other, black boundary between"),
    ScenePrompt("S025", 581, 22, "warrant_needed", "private phone and gold warrant barrier, legal line stopping data extraction, premium dark documentary image"),
    ScenePrompt("S026", 603, 18, "chosen_automatic", "chosen contents versus automatic records as two glass chambers, one locked, one trailing blue dots into darkness"),
    ScenePrompt("S027", 621, 16, "carpenter_tease", "smartphone on dark map surface, blue location points arcing toward anonymous cell towers, quiet cliffhanger, no place names"),
    ScenePrompt("S028", 637, 9, "endcard", "final viewer device in darkness reflecting blue city points and one gold location path, elegant closing background, no text"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return "sha256:" + h.hexdigest()


def post(payload: dict) -> dict:
    req = urllib.request.Request(API, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))


def save_image(b64: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(b64))


def allocations() -> dict[str, int]:
    target = 180
    raw = [(s.scene_id, max(2, s.duration / 646.0 * target)) for s in SCENES]
    base = {sid: int(value) for sid, value in raw}
    while sum(base.values()) < target:
        sid = max(raw, key=lambda x: (x[1] - base[x[0]], x[1]))[0]
        base[sid] += 1
    while sum(base.values()) > target:
        sid = max((s.scene_id for s in SCENES if base[s.scene_id] > 2), key=lambda x: base[x])
        base[sid] -= 1
    return base


def prompt_for(scene: ScenePrompt, index: int) -> str:
    variant = VARIANTS[(index - 1) % len(VARIANTS)]
    cycle = (index - 1) // len(VARIANTS)
    extra = [
        "slightly wider lens, more negative space",
        "closer subject emphasis, richer shadow detail",
        "more atmospheric depth, subtler gold accent",
        "cleaner geometry, stronger editorial hierarchy",
    ][cycle % 4]
    return f"{scene.core}, {variant}, {extra}, {STYLE}"


def copy_public(src: Path, scene_id: str, name: str) -> Path:
    dst = PUBLIC_ROOT / scene_id / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or sha256(dst) != sha256(src):
        shutil.copy2(src, dst)
    return dst


def write_ts(scene_to_public: dict[str, list[str]]) -> None:
    TS_OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "export const rileyV004Plates: Record<string, string[]> = {",
    ]
    for scene in SCENES:
        paths = scene_to_public.get(scene.scene_id, [])
        quoted = ", ".join(f"'{p}'" for p in paths)
        lines.append(f"  {scene.scene_id}: [{quoted}],")
    lines.append("};")
    lines.append("")
    lines.append("export const rileyV004PlateCount = Object.values(rileyV004Plates).reduce((sum, items) => sum + items.length, 0);")
    lines.append("")
    TS_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    alloc = allocations()
    manifest = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v004",
        "set": "sdxl_hq_v004_180",
        "target_count": 180,
        "generator": "codex-controlled-local-a1111-sdxl",
        "api": API,
        "model_checkpoint": "juggernautXL_ragnarokBy.safetensors [dd08fa32f9]",
        "ai_disclosure_required": True,
        "symbolic_reconstruction": True,
        "rights_status": "generated_symbolic_reconstruction_requires_qc_before_publish",
        "output_dir": str(OUT),
        "public_dir": str(PUBLIC_ROOT),
        "allocation": alloc,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "items": [],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    PUBLIC_ROOT.mkdir(parents=True, exist_ok=True)

    scene_to_public: dict[str, list[str]] = {s.scene_id: [] for s in SCENES}
    total = sum(alloc.values())
    n = 0
    failures = 0
    for scene_no, scene in enumerate(SCENES, start=1):
        for idx in range(1, alloc[scene.scene_id] + 1):
            n += 1
            seed = 940000 + scene_no * 1000 + idx * 43
            name = f"{scene.scene_id}_{idx:03d}.png"
            out = OUT / scene.scene_id / name
            prompt = prompt_for(scene, idx)
            meta = {
                "asset_id": f"{EP}-V004-{scene.scene_id}-{idx:03d}",
                "scene_id": scene.scene_id,
                "kind": scene.kind,
                "candidate": idx,
                "seed": seed,
                "file": str(out),
                "public": f"riley/v004_180/{scene.scene_id}/{name}",
                "prompt": prompt,
                "negative_prompt": NEG,
                "status": "candidate",
                "ai_disclosure_required": True,
                "symbolic_reconstruction": True,
                "no_real_person_likeness_intended": True,
            }
            if out.exists() and out.stat().st_size > 1024:
                print(f"[{n:03d}/{total}] skip {scene.scene_id} {name}", flush=True)
            else:
                payload = {
                    "prompt": prompt,
                    "negative_prompt": NEG,
                    "seed": seed,
                    "subseed": seed + 1009,
                    "subseed_strength": 0.10,
                    "sampler_name": "DPM++ 2M Karras",
                    "scheduler": "Karras",
                    "steps": 34,
                    "cfg_scale": 4.6,
                    "width": 1280,
                    "height": 720,
                    "batch_size": 1,
                    "n_iter": 1,
                    "enable_hr": True,
                    "hr_resize_x": 1920,
                    "hr_resize_y": 1080,
                    "hr_second_pass_steps": 12,
                    "denoising_strength": 0.20,
                    "hr_upscaler": "Latent",
                    "restore_faces": False,
                    "tiling": False,
                    "do_not_save_samples": True,
                    "do_not_save_grid": True,
                }
                try:
                    result = post(payload)
                    save_image(result["images"][0], out)
                    print(f"[{n:03d}/{total}] {scene.scene_id} -> {name}", flush=True)
                except Exception as exc:
                    failures += 1
                    meta["status"] = "failed"
                    meta["error"] = repr(exc)
                    print(f"[{n:03d}/{total}] ERROR {scene.scene_id} {name}: {exc}", flush=True)
            if out.exists() and out.stat().st_size > 1024:
                public_path = copy_public(out, scene.scene_id, name)
                meta["sha256"] = sha256(out)
                meta["public_sha256"] = sha256(public_path)
                scene_to_public[scene.scene_id].append(meta["public"])
            out.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            manifest["items"].append(meta)
            if n % 10 == 0:
                manifest["generated_count"] = len([x for x in manifest["items"] if x.get("status") != "failed"])
                (OUT / "asset_manifest.v004.partial.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                REPO_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                write_ts(scene_to_public)

    manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    manifest["generated_count"] = len([x for x in manifest["items"] if x.get("status") != "failed"])
    manifest["failures"] = failures
    manifest["public_plate_count"] = sum(len(v) for v in scene_to_public.values())
    (OUT / "asset_manifest.v004.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPO_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_ts(scene_to_public)
    print(f"generated={manifest['generated_count']} public={manifest['public_plate_count']} failures={failures} out={OUT}", flush=True)
    return 0 if failures == 0 and manifest["public_plate_count"] >= 180 else 1


if __name__ == "__main__":
    raise SystemExit(main())
