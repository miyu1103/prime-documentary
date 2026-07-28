"""Generate real image-to-video motion clips for PD-2026-004-ftx using local SVD.

This is intentionally separate from the Remotion render. It turns selected
high-value stills into short MP4 clips with actual generative motion, then
Remotion can use those clips instead of static images.
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from diffusers import StableVideoDiffusionPipeline


try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-004-ftx"
MEDIA = Path(r"H:\pd-media")
VIS = MEDIA / "episodes" / EP / "05_visuals" / "upscaled_4x_v001"
OUT_DIR = MEDIA / "episodes" / EP / "05_visuals" / "svd_motion_v001"
WORK = OUT_DIR / "_work"
MANIFEST = OUT_DIR / "svd_motion_manifest.v001.json"

CLIPS: list[dict] = [
    {"id": "SVD-0001", "asset": "COV-0004", "seed": 101, "motion": 135, "noise": 0.025, "dur": 4.7},
    {"id": "SVD-0002", "asset": "THUMB-A-dissolving-vault", "seed": 102, "motion": 170, "noise": 0.035, "dur": 4.7},
    {"id": "SVD-0003", "asset": "H03-code-vault-coins", "seed": 103, "motion": 150, "noise": 0.03, "dur": 4.7},
    {"id": "SVD-0004", "asset": "H10-secret-door-green-light", "seed": 104, "motion": 160, "noise": 0.03, "dur": 4.7},
    {"id": "SVD-0005", "asset": "H14-secret-siphon", "seed": 105, "motion": 175, "noise": 0.035, "dur": 4.7},
    {"id": "SVD-0006", "asset": "H17-bank-run-crowd", "seed": 106, "motion": 180, "noise": 0.035, "dur": 4.7},
    {"id": "SVD-0007", "asset": "H20-crater-missing-gold", "seed": 107, "motion": 150, "noise": 0.025, "dur": 4.7},
    {"id": "SVD-0008", "asset": "H23-gavel-verdict", "seed": 108, "motion": 135, "noise": 0.02, "dur": 4.7},
    {"id": "SVD-0009", "asset": "H25-prison-door-fall", "seed": 109, "motion": 145, "noise": 0.025, "dur": 4.7},
    {"id": "SVD-0010", "asset": "H28-ledger-old-fraud", "seed": 110, "motion": 125, "noise": 0.02, "dur": 4.7},
    {"id": "SVD-0011", "asset": "COV-2007", "seed": 111, "motion": 165, "noise": 0.03, "dur": 4.7},
    {"id": "SVD-0012", "asset": "COV-3003", "seed": 112, "motion": 175, "noise": 0.035, "dur": 4.7},
    {"id": "SVD-0013", "asset": "H08-money-to-skyscraper", "seed": 213, "motion": 175, "noise": 0.035, "dur": 4.7},
    {"id": "SVD-0014", "asset": "COV-4001", "seed": 214, "motion": 135, "noise": 0.022, "dur": 4.7},
    {"id": "SVD-0015", "asset": "COV-2006", "seed": 215, "motion": 160, "noise": 0.03, "dur": 4.7},
    {"id": "SVD-0016", "asset": "COV-3007", "seed": 216, "motion": 185, "noise": 0.038, "dur": 4.7},
    {"id": "SVD-0017", "asset": "COV-3008", "seed": 217, "motion": 185, "noise": 0.038, "dur": 4.7},
    {"id": "SVD-0018", "asset": "COV-2005", "seed": 218, "motion": 165, "noise": 0.032, "dur": 4.7},
    {"id": "SVD-0019", "asset": "H21-courthouse-dawn", "seed": 219, "motion": 120, "noise": 0.02, "dur": 4.7},
    {"id": "SVD-0020", "asset": "H22-empty-witness-stand", "seed": 220, "motion": 135, "noise": 0.024, "dur": 4.7},
    {"id": "SVD-0021", "asset": "COV-4005", "seed": 221, "motion": 130, "noise": 0.022, "dur": 4.7},
    {"id": "SVD-0022", "asset": "COV-5003", "seed": 222, "motion": 150, "noise": 0.028, "dur": 4.7},
    {"id": "SVD-0023", "asset": "H26-key-coin-custody", "seed": 223, "motion": 145, "noise": 0.026, "dur": 4.7},
    {"id": "SVD-0024", "asset": "COV-5001", "seed": 224, "motion": 150, "noise": 0.028, "dur": 4.7},
    {"id": "SVD-0025", "asset": "COV-5004", "seed": 225, "motion": 155, "noise": 0.03, "dur": 4.7},
    {"id": "SVD-0026", "asset": "THUMB-B-hooded-code", "seed": 226, "motion": 165, "noise": 0.032, "dur": 4.7},
    {"id": "SVD-0027", "asset": "H12-red-barrier-coin", "seed": 227, "motion": 170, "noise": 0.034, "dur": 4.7},
    {"id": "SVD-0028", "asset": "H15-scrubs-phone-savings", "seed": 228, "motion": 155, "noise": 0.03, "dur": 4.7},
    {"id": "SVD-0029", "asset": "COV-0202", "seed": 229, "motion": 140, "noise": 0.026, "dur": 4.7},
    {"id": "SVD-0030", "asset": "COV-0101", "seed": 230, "motion": 145, "noise": 0.028, "dur": 4.7},
    {"id": "SVD-0031", "asset": "COV-1001", "seed": 231, "motion": 140, "noise": 0.026, "dur": 4.7},
    {"id": "SVD-0032", "asset": "COV-3001", "seed": 232, "motion": 175, "noise": 0.035, "dur": 4.7},
]


def find_asset(asset: str) -> Path:
    matches = sorted(VIS.rglob(f"*{asset}*.png"))
    if not matches:
        raise FileNotFoundError(asset)
    return matches[0]


def cover_image(path: Path, width: int = 1024, height: int = 576) -> Image.Image:
    with Image.open(path) as im:
        im = im.convert("RGB")
    scale = max(width / im.width, height / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.Resampling.LANCZOS)
    x = (im.width - width) // 2
    y = (im.height - height) // 2
    return im.crop((x, y, x + width, y + height))


def grade_and_camera(frame: Image.Image, i: int, n: int) -> np.ndarray:
    w, h = 1920, 1080
    bgr = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    up = cv2.resize(bgr, (w, h), interpolation=cv2.INTER_LANCZOS4)
    e = 0.5 - 0.5 * math.cos(math.pi * (i / max(1, n - 1)))
    zoom = 1.02 + 0.06 * e
    rot = 0.12 * math.sin(i * 0.31)
    dx = 14 * math.sin(i * 0.21) - 12 * e
    dy = 8 * math.cos(i * 0.17) - 6 * e
    mat = cv2.getRotationMatrix2D((w / 2, h / 2), rot, zoom)
    mat[0, 2] += dx
    mat[1, 2] += dy
    out = cv2.warpAffine(up, mat, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] *= 0.92
    out = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)
    out = np.clip((out.astype(np.float32) - 128) * 1.03 + 126, 0, 255).astype(np.uint8)
    return out


def encode_frames(frames_dir: Path, output: Path, duration: float, native_count: int) -> None:
    input_fps = native_count / duration
    vf = "[0:v]minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1:scd=none[v]"
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        f"{input_fps:.5f}",
        "-i",
        str(frames_dir / "s%03d.png"),
        "-filter_complex",
        vf,
        "-map",
        "[v]",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "15",
        "-pix_fmt",
        "yuv420p",
        "-t",
        f"{duration:.3f}",
        str(output),
    ]
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--only", nargs="*", default=None)
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    jobs = CLIPS
    if args.only:
        wanted = set(args.only)
        jobs = [clip for clip in jobs if clip["id"] in wanted or clip["asset"] in wanted]
    if args.limit:
        jobs = jobs[: args.limit]

    print("loading SVD-XT", flush=True)
    pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid-xt",
        torch_dtype=torch.float16,
        variant="fp16",
    )
    pipe.enable_model_cpu_offload()

    records: list[dict] = []
    for index, clip in enumerate(jobs, start=1):
        out = OUT_DIR / f"{clip['id']}_{clip['asset']}.mp4"
        if out.exists():
            print(f"[{index}/{len(jobs)}] skip {out.name}", flush=True)
            records.append({**clip, "file": str(out), "skipped": True})
            continue
        frames_dir = WORK / clip["id"]
        if frames_dir.exists():
            shutil.rmtree(frames_dir)
        frames_dir.mkdir(parents=True)
        src = find_asset(clip["asset"])
        print(f"[{index}/{len(jobs)}] {clip['id']} <- {src.name}", flush=True)
        image = cover_image(src)
        frames = pipe(
            image,
            decode_chunk_size=8,
            motion_bucket_id=int(clip["motion"]),
            noise_aug_strength=float(clip["noise"]),
            num_frames=25,
            generator=torch.manual_seed(int(clip["seed"])),
        ).frames[0]
        for i, frame in enumerate(frames):
            out_bgr = grade_and_camera(frame, i, len(frames))
            cv2.imwrite(str(frames_dir / f"s{i:03d}.png"), out_bgr)
        encode_frames(frames_dir, out, float(clip["dur"]), len(frames))
        records.append({**clip, "source": str(src), "file": str(out), "skipped": False})
        print(f"  wrote {out}", flush=True)

    MANIFEST.write_text(
        json.dumps({"episode_id": EP, "revision": "v001", "clips": records}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"manifest {MANIFEST}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
