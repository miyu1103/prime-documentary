"""
15s, MAX-QUALITY, natural 'real footage' look.
- realistic still (rain on window + bokeh)
- SVD CHAINED across chunks (last frame -> next init) => ~15s of continuous motion
- per-frame R-ESRGAN upscale (real detail) -> supersample to clean 1080p
- subtle handheld micro-move, restrained grade, real film grain
- motion-compensated smoothing -> 30fps, libx264 veryslow CRF14
Local / free (RTX 4090).
"""
import os, math, base64, subprocess, io
import numpy as np
import cv2
import torch
import requests
from PIL import Image
from diffusers import StableVideoDiffusionPipeline
from scipy.signal import butter, lfilter
import wave

SRC   = r"C:\Users\aab15\Documents\prime-documentary\_sdxl_test\natural.png"
OUT   = r"C:\Users\aab15\Documents\prime-documentary\_demo"
FR    = os.path.join(OUT, "nathq_frames")
AUDIO = os.path.join(OUT, "rain_audio15.wav")
API   = "http://127.0.0.1:7860/sdapi/v1/extra-single-image"
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR):
    os.remove(os.path.join(FR, f))

CHUNKS = 5            # 25 + 24*4 = 121 native frames
MB, NA = 110, 0.02   # subtle, natural motion

print("[1/6] load image", flush=True)
img = Image.open(SRC).convert("RGB").resize((1024, 576), Image.LANCZOS)

print(f"[2/6] SVD chained generation ({CHUNKS} chunks)", flush=True)
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16, variant="fp16")
pipe.enable_model_cpu_offload()
native = []
cur = img
for c in range(CHUNKS):
    out = pipe(cur, decode_chunk_size=8, motion_bucket_id=MB,
               noise_aug_strength=NA, num_frames=25,
               generator=torch.manual_seed(3 + c)).frames[0]
    native += out if c == 0 else out[1:]      # drop duplicated seam frame
    cur = out[-1]
    print(f"   chunk {c+1}/{CHUNKS} -> total {len(native)} frames", flush=True)
del pipe
torch.cuda.empty_cache()

print("[3/6] per-frame R-ESRGAN upscale -> supersample 1080p", flush=True)
def resrgan(bgr):
    ok, buf = cv2.imencode(".png", bgr)
    b64 = base64.b64encode(buf).decode()
    r = requests.post(API, json={"image": b64, "upscaling_resize": 2,
                                 "upscaler_1": "R-ESRGAN 4x+", "upscaler_2": "None"}, timeout=180)
    arr = cv2.imdecode(np.frombuffer(base64.b64decode(r.json()["image"]), np.uint8), cv2.IMREAD_COLOR)
    return arr

W, H = 1920, 1080
N = len(native)
rng = np.random.default_rng(5)
def grade(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] *= 0.90
    f = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    f = (f - 128) * 0.96 + 128 + 2
    return np.clip(f, 0, 255).astype(np.uint8)

for i, fr in enumerate(native):
    bgr = cv2.cvtColor(np.array(fr), cv2.COLOR_RGB2BGR)
    try:
        big = resrgan(bgr)                                   # ~2048x1152
    except Exception as e:
        big = cv2.resize(bgr, (W * 2, H * 2), interpolation=cv2.INTER_LANCZOS4)
    up = cv2.resize(big, (W, H), interpolation=cv2.INTER_AREA)   # supersample down
    # subtle handheld (continuous over all frames) + tiny slow zoom
    e = i / (N - 1)
    dx = 4 * math.sin(i * 0.23 + 1) + 2.5 * math.sin(i * 0.11)
    dy = 3.5 * math.sin(i * 0.17 + 2) + 2 * math.cos(i * 0.08)
    rot = 0.15 * math.sin(i * 0.13)
    zoom = 1.0 + 0.05 * e
    M = cv2.getRotationMatrix2D((W / 2, H / 2), rot, zoom)
    M[0, 2] += dx; M[1, 2] += dy
    f = cv2.warpAffine(up, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    f = grade(f)
    g = rng.standard_normal((H // 2, W // 2, 1)).astype(np.float32)
    g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    f = np.clip(f.astype(np.float32) + g * 3.2, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(FR, f"s{i:04d}.png"), f)
    if i % 20 == 0:
        print(f"   frame {i}/{N}", flush=True)

print("[4/6] synthesize 15s rain ambience", flush=True)
SR = 44100; DUR = 15.0; n = int(SR * DUR)
def bf(x, cut, bt):
    b, a = butter(2, np.atleast_1d(cut) / (SR / 2), btype=bt); return lfilter(b, a, x)
rain = bf(rng.standard_normal(n), [600, 9000], "band") * 0.25
low = bf(np.cumsum(rng.standard_normal(n)), 150, "low"); low /= (np.max(np.abs(low)) + 1e-9); low *= 0.18
amb = rain + low
fade = np.ones(n); fl = int(SR * 1.0)
fade[:fl] = np.linspace(0, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
amb *= fade; amb = amb / (np.max(np.abs(amb)) + 1e-9) * 0.5
pcm = (np.stack([amb, amb], 1) * 32767).astype(np.int16)
with wave.open(AUDIO, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

print("[5/6] encode 15s @30fps, libx264 veryslow CRF14", flush=True)
in_fps = N / DUR
mp4 = os.path.join(OUT, "natural_rain_HQ_15s.mp4")
vf = "[0:v]minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1:scd=none[v]"
cmd = ["ffmpeg", "-y", "-framerate", f"{in_fps:.4f}", "-i", os.path.join(FR, "s%04d.png"),
       "-i", AUDIO, "-filter_complex", vf, "-map", "[v]", "-map", "1:a",
       "-c:v", "libx264", "-preset", "veryslow", "-crf", "14",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-shortest", mp4]
subprocess.run(cmd, check=True)
print("[6/6] DONE ->", mp4, flush=True)
