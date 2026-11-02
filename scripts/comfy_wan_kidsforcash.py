"""
scripts/comfy_wan_kidsforcash.py
Role: Wan 2.2 A14B image-to-video driver for EP38 "Kids for Cash".

One responsibility: turn the episode's locked Codex stills into A14B i2v generation
graphs (one per shot flagged wan==true), and -- only when explicitly told to -- queue
them on a locally running ComfyUI. Default mode writes graph JSON per shot for
inspection and touches NO network and NO GPU.

Node wiring is copied from the proven overnight R&D driver
`C:\\Users\\aab15\\ae-demo\\comfy_wan_a14b.py` (two-expert high/low-noise MoE, split at
50%, WanImageToVideo 3-output latent baking, wan_2.1 VAE). Do not reinvent it.

Settings are the Known-good registry from
`docs/42_AI_MOTION_PIPELINE_HARDENING_AND_GATES.md` sec.5 (shift=5.0, cfg=3.5, steps=40,
expert switch at step 20, 1280x720, 41 frames/cut = 4090 full-load ceiling). Any value
off that registry needs a cited source.

Gates from docs/42 sec.3 are provided as callable functions (dry_validate / G-GEN-2,
assert_loaded_completely / G-CAP-1, assert_frame_math / G-TIME-1). They are wired only
into the --run path and are never executed in --build/--dry-run.

Exit codes: 0 ok, 2 missing/invalid input (e.g. shotlist not present yet).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import uuid
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

# --- fixed locations -------------------------------------------------------
ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
SHOTLIST = ROOT / "episodes" / EP / "04_scenes" / "shotlist.v001.json"
GRAPH_DIR = ROOT / "episodes" / EP / "05_stock" / "wan_graphs"
CONFORM_DIR = ROOT / "episodes" / EP / "05_stock" / "wan_input"
STILL_DIR = Path(r"E:\pd-media\assets\ai\kidsforcash")
VIDEO_OUT_DIR = Path(r"E:\pd-media\assets\ai_video\kidsforcash")

HOST = "http://127.0.0.1:8188"

# --- Known-good registry (docs/42 sec.5) -----------------------------------
# Loaders take bare filenames (resolved by ComfyUI model dirs); absolute registry
# paths kept as reference only.
HIGH = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"   # D:\AI\comfy-models\diffusion_models\
LOW = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"     # D:\AI\comfy-models\diffusion_models\
VAE = "wan_2.1_vae.safetensors"                              # D:\AI\comfy-models\vae\  (2.1, NOT 2.2)
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"             # C:\Users\aab15\ComfyUI\models\text_encoders\

WIDTH = 1280
HEIGHT = 720
FRAMES = 41          # 4090 full-load ceiling @720p (docs/42 G-CAP-1); 81 -> partial load, 3x slower
STEPS = 40
SPLIT = 20           # low-noise expert takes over at 50% of steps
SHIFT = 5.0          # A14B value; 8.0 would be a silent 5B carryover
CFG = 3.5
SAMPLER = "euler"
SCHEDULER = "simple"
FPS = 16             # CreateVideo default; used only for frame-math accounting
SEED_DEFAULT = 12345

NEG_PROMPT = (
    "static, motionless, blurry, low quality, distorted, deformed, extra limbs, "
    "bad anatomy, morphing face, flickering, jitter, warping, text, watermark, "
    "identifiable face, real person likeness"
)
# EP38 stills are anonymized (silhouette / back / hands only, invariant 11); the negative
# prompt reinforces "no identifiable face" so motion does not invent one.

POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = (
    ", slow deliberate camera move, shallow depth of field, film grain, "
    "photoreal, consistent lighting, no sudden changes"
)


# --- data model ------------------------------------------------------------
@dataclass
class Shot:
    shot_id: str                 # normalized "S07"
    wan: bool
    motion_note: str
    duration_s: Optional[float]
    interp: int                  # interpolation factor applied downstream (1 = none)
    seed: int
    still: Path                  # source Codex still
    raw: dict[str, Any]

    @property
    def upload_name(self) -> str:
        return f"kfc_{self.shot_id}_720.png"

    @property
    def conform_path(self) -> Path:
        return CONFORM_DIR / self.upload_name

    @property
    def graph_path(self) -> Path:
        return GRAPH_DIR / f"{self.shot_id}.json"

    @property
    def video_out(self) -> Path:
        return VIDEO_OUT_DIR / f"{self.shot_id}.mp4"


def _log(msg: str) -> None:
    """ASCII-safe stdout line (Windows cp932 kills non-ascii prints)."""
    print("[wan] " + msg, flush=True)


def _norm_shot_id(raw_id: str) -> str:
    """Normalize 's7' / 'S7' / 'S07' / 'S07-SH001' -> 'S07' (two digits)."""
    s = str(raw_id).strip().upper()
    if "-" in s:
        s = s.split("-", 1)[0]
    digits = "".join(ch for ch in s if ch.isdigit())
    if not digits:
        return s
    return "S" + digits.zfill(2)


# --- shotlist --------------------------------------------------------------
def load_shotlist(path: Path) -> list[Shot]:
    """Parse the episode shotlist. Raises FileNotFoundError if absent (handled by caller)."""
    if not path.exists():
        raise FileNotFoundError(str(path))
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("shots") or data.get("entries") or data.get("shotlist")
    if entries is None and isinstance(data, list):
        entries = data
    if not isinstance(entries, list):
        raise ValueError("shotlist has no 'shots'/'entries' list")

    shots: list[Shot] = []
    for e in entries:
        raw_id = e.get("shot_id") or e.get("id") or e.get("scene_id") or e.get("asset_id")
        if raw_id is None:
            continue
        wan = bool(e.get("wan", False))
        note = str(e.get("motion_note") or e.get("motion") or e.get("motion_prompt") or "").strip()
        dur = e.get("duration_s", e.get("duration"))
        duration = float(dur) if isinstance(dur, (int, float)) else None
        interp = int(e.get("interp", e.get("rife", 1)) or 1)
        seed = int(e.get("seed", SEED_DEFAULT))
        still_raw = e.get("still") or e.get("image") or e.get("path")
        # Identity for Wan outputs = the image basename (S07 from S07.png): unique and
        # meaningful. shot_id here is a sequence id (e.g. "SH-03-H3") that collapses to
        # "SH"; only fall back to it when there is no S## image on the shot.
        stem = Path(still_raw).stem.upper() if still_raw else ""
        if stem and stem[0] == "S" and stem[1:].isdigit():
            sid = stem
        else:
            sid = _norm_shot_id(raw_id)
        still = Path(still_raw) if still_raw else (STILL_DIR / f"{sid}.png")
        shots.append(Shot(sid, wan, note, duration, interp, seed, still, e))
    return shots


def select_wan_shots(shots: list[Shot], only: Optional[str] = None) -> list[Shot]:
    """Shots flagged wan==true, optionally filtered to a single --shot id."""
    picked = [s for s in shots if s.wan]
    if only:
        target = _norm_shot_id(only)
        picked = [s for s in picked if s.shot_id == target]
    return picked


def motion_prompt(note: str) -> str:
    """Build the positive prompt from a shot's motion_note."""
    core = note.strip() or "the subject holds still while the frame breathes"
    return POS_PREFIX + core + POS_SUFFIX


# --- graph builder (wiring copied from ae-demo/comfy_wan_a14b.py) -----------
def build_graph(
    image_name: str,
    prompt: str,
    neg: str,
    width: int,
    height: int,
    length: int,
    steps: int,
    split: int,
    seed: int,
    shift: float,
    cfg: float,
    prefix: str,
) -> dict[str, Any]:
    """A14B two-expert i2v graph. WanImageToVideo outputs: 0=positive,1=negative,2=latent."""
    return {
        "10": {"class_type": "UNETLoader", "inputs": {"unet_name": HIGH, "weight_dtype": "default"}},
        "11": {"class_type": "UNETLoader", "inputs": {"unet_name": LOW, "weight_dtype": "default"}},
        "12": {"class_type": "CLIPLoader", "inputs": {"clip_name": CLIP, "type": "wan"}},
        "13": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "14": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["10", 0], "shift": shift}},
        "15": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["11", 0], "shift": shift}},
        "16": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["12", 0], "text": prompt}},
        "17": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["12", 0], "text": neg}},
        "18": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        # WanImageToVideo bakes the start image into the conditioning; samplers MUST consume
        # 19,0 / 19,1 (its pos/neg) and 19,2 (latent), not the raw CLIPTextEncode outputs.
        "19": {"class_type": "WanImageToVideo", "inputs": {
            "positive": ["16", 0], "negative": ["17", 0], "vae": ["13", 0],
            "width": width, "height": height, "length": length, "batch_size": 1,
            "start_image": ["18", 0]}},
        # high-noise expert: early steps, hands leftover noise to low-noise expert
        "20": {"class_type": "KSamplerAdvanced", "inputs": {
            "model": ["14", 0], "add_noise": "enable", "noise_seed": seed,
            "steps": steps, "cfg": cfg, "sampler_name": SAMPLER, "scheduler": SCHEDULER,
            "positive": ["19", 0], "negative": ["19", 1], "latent_image": ["19", 2],
            "start_at_step": 0, "end_at_step": split, "return_with_leftover_noise": "enable"}},
        # low-noise expert: finishes the denoise, no fresh noise
        "21": {"class_type": "KSamplerAdvanced", "inputs": {
            "model": ["15", 0], "add_noise": "disable", "noise_seed": seed,
            "steps": steps, "cfg": cfg, "sampler_name": SAMPLER, "scheduler": SCHEDULER,
            "positive": ["19", 0], "negative": ["19", 1], "latent_image": ["20", 0],
            "start_at_step": split, "end_at_step": 10000, "return_with_leftover_noise": "disable"}},
        "22": {"class_type": "VAEDecode", "inputs": {"samples": ["21", 0], "vae": ["13", 0]}},
        # PNG frame sequence (proven wiring). mp4 muxing (RIFE->AE/Remotion) is downstream.
        "23": {"class_type": "SaveImage", "inputs": {"images": ["22", 0], "filename_prefix": prefix}},
    }


def graph_for(shot: Shot, length: int) -> dict[str, Any]:
    """Assemble the A14B graph for one shot at a given clip length."""
    return build_graph(
        image_name=shot.upload_name,
        prompt=motion_prompt(shot.motion_note),
        neg=NEG_PROMPT,
        width=WIDTH,
        height=HEIGHT,
        length=length,
        steps=STEPS,
        split=SPLIT,
        seed=shot.seed,
        shift=SHIFT,
        cfg=CFG,
        prefix=f"wan_kfc/{shot.shot_id}",
    )


# --- image conform ---------------------------------------------------------
def conform_image(src: Path, dst: Path, width: int = WIDTH, height: int = HEIGHT) -> Path:
    """Cover-fit the still to width x height (center crop) and write to dst. Needs Pillow.
    Local file op only (no network). Called on the --run path."""
    from PIL import Image  # local import: build/dry-run must not require Pillow
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGB")
        sw, sh = im.size
        scale = max(width / sw, height / sh)
        nw, nh = round(sw * scale), round(sh * scale)
        im = im.resize((nw, nh), Image.LANCZOS)
        left = (nw - width) // 2
        top = (nh - height) // 2
        im = im.crop((left, top, left + width, top + height))
        tmp = dst.with_suffix(dst.suffix + ".tmp")
        im.save(tmp, format="PNG")
        os.replace(tmp, dst)
    return dst


# --- ComfyUI transport (only used on --run) --------------------------------
def post_json(path: str, obj: dict[str, Any]) -> dict[str, Any]:
    """POST JSON to ComfyUI. Expands node_errors from the response BODY on HTTPError."""
    data = json.dumps(obj).encode()
    req = urllib.request.Request(HOST + path, data=data,
                                 headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=60).read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        _log("ComfyUI rejected the graph (HTTP %s):" % e.code)
        try:
            d = json.loads(body)
            _log(json.dumps(d.get("error"), ensure_ascii=True))
            for node, err in (d.get("node_errors") or {}).items():
                _log("  node %s (%s):" % (node, err.get("class_type")))
                for x in err.get("errors", []):
                    _log("    - " + str(x.get("details")))
        except Exception:
            _log(body[:2000])
        raise


def upload_image(path: Path) -> str:
    """Multipart-upload an image into ComfyUI's input dir; returns the stored name."""
    boundary = "----wanboundary" + uuid.uuid4().hex
    fname = path.name
    filedata = path.read_bytes()
    body = b""
    body += ("--" + boundary + "\r\n").encode()
    body += ('Content-Disposition: form-data; name="image"; filename="%s"\r\n' % fname).encode()
    body += b"Content-Type: image/png\r\n\r\n"
    body += filedata + b"\r\n"
    body += ("--" + boundary + "\r\n").encode()
    body += b'Content-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n'
    body += ("--" + boundary + "--\r\n").encode()
    req = urllib.request.Request(HOST + "/upload/image", data=body,
                                 headers={"Content-Type": "multipart/form-data; boundary=" + boundary})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())["name"]


# --- GATES (docs/42 sec.3) -- callable; wired only into --run --------------
def dry_validate(graph: dict[str, Any]) -> bool:
    """G-GEN-2: POST the graph with length=5 to catch wiring errors cheaply before spend.
    Expands ComfyUI node_errors. Returns True on 200. Network call (only on --run)."""
    probe = json.loads(json.dumps(graph))  # deep copy
    if "19" in probe and "inputs" in probe["19"]:
        probe["19"]["inputs"]["length"] = 5
    post_json("/prompt", {"prompt": probe, "client_id": uuid.uuid4().hex})
    _log("dry_validate: graph accepted at length=5")
    return True


def assert_loaded_completely(comfy_log: str) -> bool:
    """G-CAP-1: fail if ComfyUI reported a partial model load (weights offloaded to CPU ->
    ~3x slower per docs/42). Pass only when 'loaded completely' is present and no 'partially'."""
    text = comfy_log.lower()
    if "loaded partially" in text or "partially loaded" in text:
        raise RuntimeError("G-CAP-1: model loaded PARTIALLY -> reduce frames or split cut")
    if "loaded completely" not in text:
        raise RuntimeError("G-CAP-1: no 'loaded completely' marker found in ComfyUI log")
    return True


def assert_frame_math(duration_s: float, fps: int, gen_frames: int, interp: int) -> bool:
    """G-TIME-1: supply (gen_frames * interp) must cover need (ceil(duration*fps)) + 3 margin."""
    need = math.ceil(duration_s * fps)
    supply = gen_frames * max(1, interp)
    if supply < need + 3:
        raise RuntimeError(
            "G-TIME-1: frame shortfall -- need %d (+3 margin) but supply %d "
            "(gen=%d x interp=%d)" % (need, supply, gen_frames, interp))
    return True


# --- actions ---------------------------------------------------------------
def _atomic_write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=True, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def build_shot(shot: Shot, dry_run: bool) -> Optional[Path]:
    """Build the full-length graph for one shot and write it for inspection. No network."""
    graph = graph_for(shot, length=FRAMES)
    record = {
        "schema_version": "wan_graph.v1",
        "episode_id": EP,
        "shot_id": shot.shot_id,
        "still_source": str(shot.still),
        "conform_target": str(shot.conform_path),
        "upload_name": shot.upload_name,
        "video_out": str(shot.video_out),
        "settings": {
            "model": "wan2.2_a14b_i2v",
            "high_noise": HIGH, "low_noise": LOW, "vae": VAE, "clip": CLIP,
            "width": WIDTH, "height": HEIGHT, "frames": FRAMES,
            "steps": STEPS, "split": SPLIT, "shift": SHIFT, "cfg": CFG,
            "sampler": SAMPLER, "scheduler": SCHEDULER, "fps": FPS,
            "seed": shot.seed, "interp_downstream": shot.interp,
        },
        "positive_prompt": motion_prompt(shot.motion_note),
        "negative_prompt": NEG_PROMPT,
        "comfy_graph": graph,
    }
    if dry_run:
        _log("DRY-RUN would write graph %s (still=%s)" % (shot.graph_path, shot.still))
        return None
    _atomic_write_json(shot.graph_path, record)
    _log("built %s -> %s" % (shot.shot_id, shot.graph_path))
    return shot.graph_path


def run_shot(shot: Shot, dry_run: bool) -> None:
    """GUARDED: would conform+upload the still, run the gates, and queue generation on
    ComfyUI. Left intact for the main agent; the GPU is busy now, so this is not the
    default path. --dry-run short-circuits before any network/GPU/file side effect."""
    if dry_run:
        _log("DRY-RUN --run requested for %s: no upload, no /prompt, no GPU." % shot.shot_id)
        return
    # --- Everything below is a real side effect. Executed only under real --run. ---
    if not shot.still.exists():
        raise FileNotFoundError("still missing: %s" % shot.still)
    conform_image(shot.still, shot.conform_path)
    # G-CAP-1 note: caller must confirm 'loaded completely' from the ComfyUI log after the
    # first cut (assert_loaded_completely). G-TIME-1: if duration known, verify supply.
    if shot.duration_s is not None:
        assert_frame_math(shot.duration_s, FPS, FRAMES, shot.interp)
    graph = graph_for(shot, length=FRAMES)
    name = upload_image(shot.conform_path)    # upload BEFORE validation so LoadImage resolves
    graph["18"]["inputs"]["image"] = name     # use the exact uploaded name
    dry_validate(graph)                       # G-GEN-2 (length=5); image now exists in ComfyUI
    r = post_json("/prompt", {"prompt": graph, "client_id": uuid.uuid4().hex})
    _log("queued %s prompt_id=%s -> frames for %s" % (shot.shot_id, r.get("prompt_id"), shot.video_out))


# --- cli -------------------------------------------------------------------
def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Wan 2.2 A14B i2v driver for EP38 Kids for Cash.")
    ap.add_argument("--build", action="store_true",
                    help="write graph JSON per wan shot for inspection (default; no network)")
    ap.add_argument("--run", action="store_true",
                    help="GUARDED: conform+upload+validate+queue on ComfyUI (real GPU/network)")
    ap.add_argument("--shot", default=None, help="limit to a single shot id, e.g. S07")
    ap.add_argument("--dry-run", action="store_true",
                    help="describe actions without any network/GPU/file side effect")
    args = ap.parse_args(argv)

    do_run = bool(args.run)
    do_build = bool(args.build) or not do_run  # build is the default when --run is absent

    try:
        shots = load_shotlist(SHOTLIST)
    except FileNotFoundError:
        _log("MISSING shotlist: %s" % SHOTLIST)
        _log("nothing to build yet -- create shotlist.v001.json (shots[] with "
             "shot_id, wan, motion_note[, duration_s, interp, seed, still]).")
        return 2
    except (ValueError, json.JSONDecodeError) as e:
        _log("INVALID shotlist: %s" % e)
        return 2

    picked = select_wan_shots(shots, only=args.shot)
    _log("shotlist=%d shots, wan-selected=%d%s"
         % (len(shots), len(picked), (" (filter %s)" % args.shot) if args.shot else ""))
    if not picked:
        _log("no wan==true shots selected; nothing to do.")
        return 0

    if do_run:
        if args.dry_run:
            _log("--run + --dry-run: simulating, NO network/GPU call.")
        else:
            _log("--run: LIVE mode. Will hit ComfyUI at %s and use the GPU." % HOST)
        for s in picked:
            run_shot(s, dry_run=args.dry_run)
        return 0

    # default: build graphs only, never touches the network
    if do_build:
        for s in picked:
            build_shot(s, dry_run=args.dry_run)
        _log("build complete: %d graph(s) under %s" % (len(picked), GRAPH_DIR))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
