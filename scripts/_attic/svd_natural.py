"""
Natural / 'real footage' look (anti-AI):
- realistic still (rain on window + bokeh) -> SVD subtle motion (rain, light flicker)
- handheld micro-movement (no dramatic zoom)
- restrained grade (slight desaturate) + real film-grain texture (grain-sized, temporal)
- motion-compensated smoothing -> looks like a clip shot on a camera
Local / free (RTX 4090).
"""
import os, math, subprocess
import numpy as np
import cv2
import torch
from PIL import Image
from diffusers import StableVideoDiffusionPipeline

SRC   = r"C:\Users\aab15\Documents\prime-documentary\_sdxl_test\natural.png"
OUT   = r"C:\Users\aab15\Documents\prime-documentary\_demo"
FR    = os.path.join(OUT, "nat_frames")
AUDIO = os.path.join(OUT, "rain_audio.wav")
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR):
    os.remove(os.path.join(FR, f))

print("[1/5] load image", flush=True)
img = Image.open(SRC).convert("RGB").resize((1024, 576), Image.LANCZOS)

print("[2/5] SVD subtle natural motion (bucket=110)", flush=True)
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16, variant="fp16")
pipe.enable_model_cpu_offload()
gen = torch.manual_seed(3)
frames = pipe(img, decode_chunk_size=8, motion_bucket_id=110,
              noise_aug_strength=0.02, num_frames=25, generator=gen).frames[0]

print("[3/5] handheld micro-move + restrained grade + film grain", flush=True)
W, H = 1920, 1080
N = len(frames)
rng = np.random.default_rng(5)
def grade(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] *= 0.90                                  # gentle desaturation
    f = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)
    f = f.astype(np.float32)
    f = (f - 128) * 0.96 + 128 + 2                        # soft contrast, tiny lift
    return np.clip(f, 0, 255).astype(np.uint8)
for i, fr in enumerate(frames):
    bgr = cv2.cvtColor(np.array(fr), cv2.COLOR_RGB2BGR)
    up = cv2.resize(bgr, (W, H), interpolation=cv2.INTER_LANCZOS4)
    # subtle handheld: small drift/shake + tiny slow zoom (no dramatic move)
    e = i / (N - 1)
    dx = 4 * math.sin(i * 0.7 + 1) + 2.5 * math.sin(i * 0.31)
    dy = 3.5 * math.sin(i * 0.5 + 2) + 2 * math.cos(i * 0.23)
    rot = 0.18 * math.sin(i * 0.4)
    zoom = 1.0 + 0.03 * e
    M = cv2.getRotationMatrix2D((W / 2, H / 2), rot, zoom)
    M[0, 2] += dx; M[1, 2] += dy
    f = cv2.warpAffine(up, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    f = grade(f)
    # real film grain: grain-sized (half-res noise upscaled), low amplitude, temporal
    g = rng.standard_normal((H // 2, W // 2, 1)).astype(np.float32)
    g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    f = np.clip(f.astype(np.float32) + g * 3.5, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(FR, f"s{i:03d}.png"), f)

print("[4/5] synthesize natural rain/room ambience", flush=True)
from scipy.signal import butter, lfilter
SR = 44100; DUR = 6.0; n = int(SR * DUR); tt = np.linspace(0, DUR, n)
def bf(x, cut, bt):
    b, a = butter(2, np.atleast_1d(cut) / (SR / 2), btype=bt); return lfilter(b, a, x)
white = rng.standard_normal(n)
rain = bf(white, [600, 9000], "band") * 0.25            # hiss of rain
patter = bf(rng.standard_normal(n), 2500, "low") * (0.5 + 0.5 * rng.standard_normal(n).clip(-1,1)) * 0.0
low = bf(np.cumsum(rng.standard_normal(n)), 150, "low"); low /= (np.max(np.abs(low))+1e-9); low *= 0.18
amb = rain + low
fade = np.ones(n); fl = int(SR * 0.8)
fade[:fl] = np.linspace(0, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
amb *= fade; amb = amb / (np.max(np.abs(amb)) + 1e-9) * 0.5
import wave
pcm = (np.stack([amb, amb], 1) * 32767).astype(np.int16)
with wave.open(AUDIO, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

print("[5/5] interpolate -> 30fps -> encode CRF15", flush=True)
mp4 = os.path.join(OUT, "natural_rain.mp4")
vf = "[0:v]minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1:scd=none[v]"
cmd = ["ffmpeg", "-y", "-framerate", "4.2", "-i", os.path.join(FR, "s%03d.png"),
       "-i", AUDIO, "-filter_complex", vf, "-map", "[v]", "-map", "1:a",
       "-c:v", "libx264", "-preset", "veryslow", "-crf", "15",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-shortest", mp4]
subprocess.run(cmd, check=True)
print("DONE ->", mp4, flush=True)
