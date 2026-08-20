#!/usr/bin/env python3
"""Turn an episode's generated stills into i2v motion clips, so the film is not kamishibai.

Why this exists: check_episode_inputs measures distinct video assets, and a still counts for
nothing until it moves. EP63/64/65 have 8, 16 and 11 accepted archive clips against floors near
140. EP62 solved the same problem with 122 clips in remotion/public/greene/motion, but the tool
that made them was never committed, so the next three episodes had no path at all.

The route is the one already proven on this machine and recorded in the project's own notes:
ComfyUI's HTTP API driving Wan 2.2 TI2V-5B image-to-video, with the plate as the start image.
Ken Burns is explicitly NOT this: the owner has rejected zoom-and-pan on a still as kamishibai,
and a probe of greene's clips confirms real subject motion that survives zoom alignment.

MEASURED on an RTX 4090, 2026-08-06:
  1280x704 / 121 frames / 30 steps  -> 306-420 s per STEP. VRAM 23.7 of 24.5 GB: it thrashes.
  832x480  /  49 frames / 20 steps  -> 18.5 s per step, about 6.2 minutes per clip. This fits.
  EP62's 122 clips took about 6.4 minutes each, so this is the same working point.

The motion prompt is derived from the plate's OWN commissioned prompt, so the movement belongs to
the picture instead of being generic drift. Prompts describing paper get paper motion; rooms get
air and light; hands get a shift of grip.

    py scripts/build_motion_from_plates.py --slug correa --limit 130
    py scripts/build_motion_from_plates.py --slug correa --dry-run

Resumable: a plate whose mp4 already exists is skipped, so the run can be stopped and restarted.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import uuid
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
HOST = "http://127.0.0.1:8188"
COMFY_OUT = Path(r"C:\Users\aab15\ComfyUI\output")

BATCH = {
    "greene": ("G", "EP62_greene_CODEX_BATCH_A.v002.md", "PD-2026-062-greene"),
    "correa": ("C", "EP63_correa_CODEX_BATCH_A.v001.md", "PD-2026-063-correa"),
    "memphis": ("M", "EP64_memphis_CODEX_BATCH_A.v001.md", "PD-2026-064-memphis"),
    "marmet": ("R", "EP65_marmet_CODEX_BATCH_A.v001.md", "PD-2026-065-marmet"),
}

W, H, LENGTH, STEPS = 832, 480, 49, 20
# fog, bloom and light leaks are in here because they are what destroyed 33 percent of the first
# strengthened batch: the model renders "light sweeping" and "dust in the beam" as atmosphere,
# and the atmosphere eats the picture by the third second.
NEG = ("static, motionless, still image, frozen, blurry, low quality, distorted, deformed, "
       "extra limbs, bad anatomy, morphing face, face, human face, facial features, text, "
       "lettering, numerals, handwriting, watermark, logo, flickering, jitter, warping, "
       "camera shake, zoom, pan, dolly, crane, whip pan, "
       "fog, haze, mist, smoke, steam, god rays, light shaft, volumetric light, lens flare, "
       "bloom, glow, overexposure, blown highlights, brightening, darkening, light leak, "
       "colour shift, exposure change, fade to white, fade to black, dissolve, "
       "scene change, new objects appearing, objects vanishing")

# What moves, keyed on what the plate's own prompt says is in the picture. First match wins.
# The first pass asked for movement "very slightly" and "almost imperceptibly" and got a third
# of the reference clip's amplitude. The complaint on this channel is always that there is not
# enough animation, so these ask for movement that is unmistakably there while staying physical.
MOTION = [
    (r"\bpaper|sheet|form|notice|bill|flyer|ticket|slip|envelope|document|page\b",
     "the paper lifts and flutters in a draught, its free edge curling up and falling back again "
     "several times, the whole sheet flexing and rippling, dust turning through the shaft of light"),
    (r"\bhand|fingers|thumb|palm|wrist\b",
     "the hand moves, the fingers opening and closing their grip and the wrist turning, the arm "
     "shifting its weight"),
    (r"\bcurtain|window|blind|glass\b",
     "the curtain billows inward on a draught and falls back again, its hem swinging, the blind "
     "cord swaying"),
    (r"\bmeter|dial|telephone|handset|cord|machine|printer\b",
     "the cord swings on its own weight, turning as it slows"),
    (r"\bstreet|road|yard|grass|tree|sky|cloud|field\b",
     "the branches bend and spring back in the wind and the grass moves in waves across the ground"),
    (r"\bwater|puddle|rain|kettle|steam\b",
     "the water surface ripples and settles"),
    (r"\bflame|candle|fire in a grate|smoke from\b",
     "the flame leans and recovers"),
]
# Furniture and architecture used to be in this table -- a chair, a desk, a corridor -- borrowing
# their motion from "loose paper on the surface" and "the door on its hinge". When the plate had no
# paper and no door that could swing, the model supplied one. Those two rules were the catch-all in
# disguise, and between them they matched nearly every interior, which is why removing only the
# DEFAULT left 28 plates out of 198 as stills instead of the majority. They are gone.
# There is no catch-all any more. A plate with nothing movable in it is left as a still: told to
# produce movement in a frame where nothing can move, the model invents, and that is where the man
# walking into the empty corridor came from. Measured: 14 percent of correa's clips survived visual
# QC, against 36 on the two episodes whose plates carry paper, cord, cloth and foliage.
DEFAULT_MOTION = None
COMMON = (", continuous visible movement of the objects themselves throughout the shot, "
          "unhurried and physical, the exposure and the colour holding perfectly steady from the "
          "first frame to the last, the room and its light unchanged, "
          "the camera locked off and completely static on a tripod, "
          "no camera movement of any kind, no zoom, no pan, photoreal, cinematic")


def post_json(path: str, obj: dict) -> dict:
    data = json.dumps(obj).encode()
    req = urllib.request.Request(HOST + path, data=data, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def get_json(path: str) -> dict:
    return json.loads(urllib.request.urlopen(HOST + path, timeout=60).read())


def upload_image(path: Path) -> str:
    boundary = "----pdmotion" + uuid.uuid4().hex
    body = b""
    body += ("--" + boundary + "\r\n").encode()
    body += (f'Content-Disposition: form-data; name="image"; filename="{path.name}"\r\n').encode()
    body += b"Content-Type: image/png\r\n\r\n" + path.read_bytes() + b"\r\n"
    body += ("--" + boundary + "\r\n").encode()
    body += b'Content-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n'
    body += ("--" + boundary + "--\r\n").encode()
    req = urllib.request.Request(HOST + "/upload/image", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())["name"]


def graph(image_name: str, prompt: str, prefix: str, seed: int) -> dict:
    return {
        "10": {"class_type": "UNETLoader",
               "inputs": {"unet_name": "wan2.2_ti2v_5B_fp16.safetensors", "weight_dtype": "default"}},
        "11": {"class_type": "CLIPLoader",
               "inputs": {"clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan"}},
        "12": {"class_type": "VAELoader", "inputs": {"vae_name": "wan2.2_vae.safetensors"}},
        "13": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["10", 0], "shift": 8.0}},
        "14": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["11", 0], "text": prompt}},
        "15": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["11", 0], "text": NEG}},
        "16": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "17": {"class_type": "Wan22ImageToVideoLatent",
               "inputs": {"vae": ["12", 0], "width": W, "height": H, "length": LENGTH,
                          "batch_size": 1, "start_image": ["16", 0]}},
        "18": {"class_type": "KSampler",
               "inputs": {"model": ["13", 0], "positive": ["14", 0], "negative": ["15", 0],
                          "latent_image": ["17", 0], "seed": seed, "steps": STEPS, "cfg": 5.0,
                          "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "19": {"class_type": "VAEDecode", "inputs": {"samples": ["18", 0], "vae": ["12", 0]}},
        "20": {"class_type": "SaveImage", "inputs": {"images": ["19", 0],
                                                     "filename_prefix": f"pdmotion/{prefix}"}},
    }


def plate_prompts(slug: str) -> dict[str, str]:
    pre, batch, _ = BATCH[slug]
    t = (ROOT / "episodes" / "_planning" / batch).read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(rf"^- `({pre}\d{{3}})\.png`\s*\n(.+)$", t, re.M):
        out.setdefault(m.group(1), m.group(2))          # first definition wins
    return out


def motion_for(desc: str) -> str | None:
    """What moves in this plate, or None if nothing in it can."""
    low = desc.lower()
    for pat, mv in MOTION:
        if re.search(pat, low):
            return mv
    return DEFAULT_MOTION


def subject_of(desc: str) -> str:
    """The plate's own opening clause -- what the picture is -- without the style tail."""
    s = desc.split("[STYLE]")[0].split("Avoid:")[0]
    s = re.sub(r"\s+", " ", s).strip(" ,.")
    return s[:320]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, choices=sorted(BATCH))
    ap.add_argument("--limit", type=int, default=130, help="how many clips to make")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    pre, _, epid = BATCH[a.slug]
    src = Path(f"H:/pd-media/assets/ai/{a.slug}")
    outdir = ROOT / "remotion" / "public" / a.slug / "motion"
    outdir.mkdir(parents=True, exist_ok=True)

    # Read the HIGHEST spec revision, not a hard-coded v001. Every other tool that reads
    # `people_plates` goes through check_episode_spec.spec_path(); this one did not, and the
    # consequence is silent rather than loud: a correctly-written episode_spec.v002.json would be
    # ignored here, `people_plates` would come back empty, and every people plate would be animated
    # as if it were an ordinary cut. Found 2026-08-21 on EP75 lahaina, whose people_plates list
    # exists only in v002 because the plate ids did not exist when v001 was written.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from check_episode_spec import spec_path  # noqa: PLC0415 - local import, same dir
    spec = json.loads(spec_path(ROOT / "episodes" / epid).read_text(encoding="utf-8"))
    mandatory = [s[:-4] for s in spec["mandatory_stills"]]
    people = {Path(s).stem for s in spec.get("people_plates", [])}
    prompts = plate_prompts(a.slug)

    # Animate the cuts, not the packaging: mandatory stills, in order, skipping people plates
    # (a person who moves is a person the audience looks at, and these are deliberately faceless).
    todo = [p for p in mandatory
            if p not in people and (src / f"{p}.png").exists() and not (outdir / f"{p}.mp4").exists()]
    skipped_static = [p for p in todo if motion_for(prompts.get(p, "")) is None]
    todo = [p for p in todo if motion_for(prompts.get(p, "")) is not None][:a.limit]
    have = len(list(outdir.glob("*.mp4")))
    print(f"[motion] {a.slug}: {have} clip(s) already built, {len(todo)} to make "
          f"({W}x{H}, {LENGTH} frames, {STEPS} steps, about 1 min each), "
          f"{len(skipped_static)} plate(s) left as stills because nothing in them can move")
    if a.dry_run:
        for p in todo[:8]:
            print(f"   {p}: {motion_for(prompts.get(p, ''))}")
        print(f"   ... {len(todo)} total")
        return 0

    t_start = time.time()
    for n, pid in enumerate(todo, 1):
        png = src / f"{pid}.png"
        desc = prompts.get(pid, "")
        prompt = f"{subject_of(desc)}. {motion_for(desc)}{COMMON}"
        prefix = f"{a.slug}_{pid}"
        for f in COMFY_OUT.glob(f"pdmotion/{prefix}_*.png"):
            f.unlink()
        try:
            name = upload_image(png)
            r = post_json("/prompt", {"prompt": graph(name, prompt, prefix, 1000 + n),
                                      "client_id": uuid.uuid4().hex})
            pid_q = r["prompt_id"]
        except Exception as e:
            print(f"   {pid}: queue failed {e}"); continue

        t0 = time.time()
        while True:
            time.sleep(5)
            try:
                hist = get_json("/history/" + pid_q)
            except Exception:
                continue
            if pid_q in hist and (hist[pid_q].get("outputs") or
                                  hist[pid_q].get("status", {}).get("completed")):
                break
            if hist.get(pid_q, {}).get("status", {}).get("status_str") == "error":
                print(f"   {pid}: comfy error"); break
            if time.time() - t0 > 2400:
                print(f"   {pid}: timeout"); break

        frames = sorted(COMFY_OUT.glob(f"pdmotion/{prefix}_*.png"))
        if len(frames) < LENGTH // 2:
            print(f"   {pid}: only {len(frames)} frames, skipped")
            continue
        stage = COMFY_OUT / "pdmotion" / f"_seq_{prefix}"
        if stage.exists():
            shutil.rmtree(stage)
        stage.mkdir(parents=True)
        for i, f in enumerate(frames):
            shutil.copy(f, stage / f"f{i:04d}.png")
        mp4 = outdir / f"{pid}.mp4"
        # 49 frames at 24 fps is 2.03s; a documentary cut needs about 5. setpts stretches the
        # time base and minterpolate rebuilds the intermediate frames with motion compensation
        # rather than duplicating, so it does not judder. About 36s of CPU, off the GPU.
        cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", "24", "-i", str(stage / "f%04d.png"),
               "-vf", "scale=1920:1080:flags=lanczos,"
                       "setpts=2.45*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1",
               "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(mp4)]
        subprocess.run(cmd, check=True)
        shutil.rmtree(stage, ignore_errors=True)
        for f in frames:
            f.unlink()
        el = time.time() - t_start
        print(f"   [{n}/{len(todo)}] {pid} -> {mp4.name} "
              f"({time.time()-t0:.0f}s, {mp4.stat().st_size//1024} KB, "
              f"eta {(el/n)*(len(todo)-n)/3600:.1f} h)", flush=True)
    print(f"[motion] {a.slug}: {len(list(outdir.glob('*.mp4')))} clip(s) in {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
