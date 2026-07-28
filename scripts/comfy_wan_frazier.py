#!/usr/bin/env python3
"""Wan 2.2 A14B i2v driver for EP39 Frazier.

Unlike the EP38 driver, this deliberately does not read a script-dependent
shotlist.  The 22 approved stills and motion notes come from the EP39 asset
handoff.  Default/--build writes reviewable graph JSON only; --run is the sole
path that contacts the already-running local ComfyUI instance.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comfy_wan_kidsforcash as wan  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-039-frazier"
STILL_DIR = ROOT / "remotion/public/frazier/img/selected"
GRAPH_DIR = ROOT / "episodes" / EP / "05_visuals/wan_graphs"
CONFORM_DIR = ROOT / "episodes" / EP / "05_visuals/wan_input"
VIDEO_OUT_DIR = Path("H:/pd-media/assets/ai_video/frazier")

SHOTS = [
    ("S02", "the heavy steel door slowly swings closed, the blade of corridor light narrowing across the floor"),
    ("S15", "the door swings shut from the outside, the lit gap collapsing to a thin line"),
    ("S17", "a hand slides the stack of papers slowly across the steel table toward camera"),
    ("S20", "the clock hands sweep forward, light shifting across the wall as hours pass"),
    ("S21", "the fluorescent tube stutters and flickers, glare pulsing into the lens"),
    ("S23", "the tape reels turn steadily, the red record light pulsing in the dark"),
    ("S01", "slow lateral dolly across the empty interrogation room, light shifting on the table"),
    ("S03", "reflections drift across the one-way mirror as the lit room beyond stays still"),
    ("S09", "streetlights slide past the cruiser window, the cage bars steady in the foreground"),
    ("S14", "the seated figure shifts almost imperceptibly, shoulders sinking lower, camera creeps closer"),
    ("S19", "pages riffle and settle, the pen rocking slightly on the top sheet"),
    ("S27", "the ceiling light glare pulses and the walls breathe inward, disorienting drift"),
    ("S30", "the file is carried down the corridor, light and shadow sliding across the manila cover"),
    ("S38", "points of golden light fall onto the black water, ripples spreading and overlapping"),
    ("S44", "the recording camera LED blinks, flat LED light humming, faint air movement in the empty room"),
    ("S45", "the barred window light bar crawls slowly across the cell floor"),
    ("S49", "the line of golden light brightens and widens slowly across the marble floor"),
    ("S08", "the silhouettes behind the frosted glass shift and one raises a hand to knock"),
    ("S25", "the monitor glow flickers in the dark observation room, faint reflections on the glass"),
    ("S26", "the caged bulb sways almost imperceptibly, its shadow crawling across the cinderblock"),
    ("S13", "slow push in on the empty chair, the hard shadow lengthening across the floor"),
    ("S28", "the pen lowers toward the page, the hand trembling, lamp light wavering"),
]


def still_for(scene: str) -> Path:
    hits = sorted(STILL_DIR.glob(f"FRZC_{scene}_V*.png"))
    hits = [p for p in hits if not p.name.endswith("_depth.png")]
    if not hits:
        raise FileNotFoundError(f"no corrected still for {scene} under {STILL_DIR}")
    return hits[0]


def graph_for(scene: str, note: str, upload_name: str) -> dict:
    return wan.build_graph(
        image_name=upload_name,
        prompt=wan.motion_prompt(note),
        neg=wan.NEG_PROMPT,
        width=wan.WIDTH,
        height=wan.HEIGHT,
        length=wan.FRAMES,
        steps=wan.STEPS,
        split=wan.SPLIT,
        seed=wan.SEED_DEFAULT + int(scene[1:]),
        shift=wan.SHIFT,
        cfg=wan.CFG,
        prefix=f"wan_frazier/{scene}",
    )


def record_for(scene: str, note: str) -> dict:
    still = still_for(scene)
    upload_name = f"frazier_{scene}_720.png"
    graph = graph_for(scene, note, upload_name)
    return {
        "schema_version": "wan_graph.v1",
        "episode_id": EP,
        "shot_id": scene,
        "still_source": str(still),
        "conform_target": str(CONFORM_DIR / upload_name),
        "upload_name": upload_name,
        "video_out": str(VIDEO_OUT_DIR / f"{scene}.mp4"),
        "settings": {
            "model": "wan2.2_a14b_i2v",
            "high_noise": wan.HIGH,
            "low_noise": wan.LOW,
            "vae": wan.VAE,
            "clip": wan.CLIP,
            "width": wan.WIDTH,
            "height": wan.HEIGHT,
            "frames": wan.FRAMES,
            "steps": wan.STEPS,
            "split": wan.SPLIT,
            "shift": wan.SHIFT,
            "cfg": wan.CFG,
            "sampler": wan.SAMPLER,
            "scheduler": wan.SCHEDULER,
            "fps": wan.FPS,
            "seed": wan.SEED_DEFAULT + int(scene[1:]),
        },
        "positive_prompt": wan.motion_prompt(note),
        "negative_prompt": wan.NEG_PROMPT,
        "comfy_graph": graph,
    }


def build(scene_filter: str | None, dry_run: bool) -> int:
    picked = [(s, n) for s, n in SHOTS if not scene_filter or s == scene_filter.upper()]
    for scene, note in picked:
        out = GRAPH_DIR / f"{scene}.json"
        if dry_run:
            print(f"[wan-frazier] DRY-RUN would write {out}")
        else:
            wan._atomic_write_json(out, record_for(scene, note))
            print(f"[wan-frazier] built {out}")
    print(f"[wan-frazier] build complete: {len(picked)} graph(s)")
    return 0


def run(scene_filter: str | None, dry_run: bool) -> int:
    picked = [(s, n) for s, n in SHOTS if not scene_filter or s == scene_filter.upper()]
    for scene, note in picked:
        if dry_run:
            print(f"[wan-frazier] DRY-RUN would queue {scene}; no network/GPU call")
            continue
        rec = record_for(scene, note)
        still = Path(rec["still_source"])
        conformed = Path(rec["conform_target"])
        wan.conform_image(still, conformed)
        upload_name = wan.upload_image(conformed)
        graph = rec["comfy_graph"]
        graph["18"]["inputs"]["image"] = upload_name
        wan.dry_validate(graph)
        response = wan.post_json("/prompt", {"prompt": graph, "client_id": uuid.uuid4().hex})
        print(f"[wan-frazier] queued {scene} prompt_id={response.get('prompt_id')}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Wan 2.2 A14B i2v driver for EP39 Frazier")
    ap.add_argument("--build", action="store_true", help="write graph JSON only (default)")
    ap.add_argument("--run", action="store_true", help="queue on an already-running local ComfyUI")
    ap.add_argument("--shot", help="limit to one scene, for example S02")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if len(SHOTS) != 22 or len({s for s, _ in SHOTS}) != 22:
        raise AssertionError("EP39 Wan list must contain 22 unique scene codes")
    return run(args.shot, args.dry_run) if args.run else build(args.shot, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
