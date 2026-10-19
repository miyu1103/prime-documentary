"""
SVD v2 — stronger, 'proper' motion + clean cinematic camera move.
- SVD generative content motion (aurora/atmosphere) at higher strength
- uniform camera push-in + slight drift (no parallax -> no warping)
- motion-compensated interpolation to smooth 30fps ~6s
- clean 1080p, libx264 CRF15, no grain
Local / free (RTX 4090).
"""
import os, math, subprocess
import numpy as np
import cv2
import torch
from PIL import Image
from diffusers import StableVideoDiffusionPipeline

SRC   = r"C:\Users\aab15\Documents\prime-documentary\_sdxl_test\wonder.png"
OUT   = r"C:\Users\aab15\Documents\prime-documentary\_demo"
FR    = os.path.join(OUT, "svd2_frames")
AUDIO = os.path.join(OUT, "wonder_audio.wav")
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR):
    os.remove(os.path.join(FR, f))

print("[1/4] load image", flush=True)
img = Image.open(SRC).convert("RGB").resize((1024, 576), Image.LANCZOS)

print("[2/4] SVD generate (motion_bucket_id=190)", flush=True)
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16, variant="fp16")
pipe.enable_model_cpu_offload()
gen = torch.manual_seed(12)
frames = pipe(img, decode_chunk_size=8, motion_bucket_id=190,
              noise_aug_strength=0.03, num_frames=25, generator=gen).frames[0]

print("[3/4] add clean camera move (uniform zoom + drift) @1080p", flush=True)
W, H = 1920, 1080
N = len(frames)
for i, fr in enumerate(frames):
    bgr = cv2.cvtColor(np.array(fr), cv2.COLOR_RGB2BGR)
    up = cv2.resize(bgr, (W, H), interpolation=cv2.INTER_LANCZOS4)
    e = 0.5 - 0.5 * math.cos(math.pi * (i / (N - 1)))      # ease 0..1
    zoom = 1.0 + 0.12 * e                                   # push in 12%
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, zoom)
    M[0, 2] += -22 * e                                      # slow drift left
    M[1, 2] += -10 * e                                      # slight rise
    out = cv2.warpAffine(up, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    cv2.imwrite(os.path.join(FR, f"s{i:03d}.png"), out)

print("[4/4] interpolate -> smooth 30fps ~6s -> encode CRF15", flush=True)
mp4 = os.path.join(OUT, "svd_wonder_v2.mp4")
# input 4.2 fps (25 frames ~6s) then motion-compensated interpolation to 30 fps
vf = "[0:v]minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1:scd=none[v]"
cmd = ["ffmpeg", "-y", "-framerate", "4.2", "-i", os.path.join(FR, "s%03d.png"),
       "-i", AUDIO, "-filter_complex", vf, "-map", "[v]", "-map", "1:a",
       "-c:v", "libx264", "-preset", "veryslow", "-crf", "15",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k", "-shortest", mp4]
subprocess.run(cmd, check=True)
print("DONE ->", mp4, flush=True)
