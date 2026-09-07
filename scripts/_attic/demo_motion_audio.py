"""
Demo: still image -> depth-based 2.5D parallax motion -> + procedural ambience/SFX -> mp4
All local (RTX 4090), no paid services, no external assets (audio synthesized = rights-clean).
"""
import os, math, wave, subprocess, sys
import numpy as np
import cv2
import torch
from PIL import Image
from scipy.signal import butter, lfilter

IMG = r"C:\Users\aab15\Documents\prime-documentary\_sdxl_test\wonder.png"
OUT = r"C:\Users\aab15\Documents\prime-documentary\_demo"
os.makedirs(OUT, exist_ok=True)
FRAMES = os.path.join(OUT, "frames")
os.makedirs(FRAMES, exist_ok=True)

TW, TH = 1920, 1080
FPS, DUR = 30, 6.0
N = int(FPS * DUR)

print("[1/4] load + upscale image", flush=True)
bgr = cv2.imread(IMG)
bgr = cv2.resize(bgr, (TW, TH), interpolation=cv2.INTER_CUBIC)

print("[2/4] depth estimation (DPT, GPU)", flush=True)
from transformers import DPTImageProcessor, DPTForDepthEstimation
dev = "cuda" if torch.cuda.is_available() else "cpu"
proc = DPTImageProcessor.from_pretrained("Intel/dpt-hybrid-midas")
model = DPTForDepthEstimation.from_pretrained("Intel/dpt-hybrid-midas").to(dev).eval()
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
inp = proc(images=Image.fromarray(rgb), return_tensors="pt").to(dev)
with torch.no_grad():
    pred = model(**inp).predicted_depth
depth = torch.nn.functional.interpolate(pred.unsqueeze(1), size=(TH, TW),
        mode="bicubic", align_corners=False).squeeze().cpu().numpy()
d = (depth - depth.min()) / (depth.max() - depth.min() + 1e-8)  # 1 = near
cv2.imwrite(os.path.join(OUT, "depth_preview.png"), (d * 255).astype(np.uint8))

print("[3/4] render 2.5D parallax frames", flush=True)
xs, ys = np.meshgrid(np.arange(TW), np.arange(TH))
xs = xs.astype(np.float32); ys = ys.astype(np.float32)
cx, cy = TW / 2.0, TH / 2.0
MAXSHIFT, MAXZOOM = 30.0, 0.12
for i in range(N):
    t = i / (N - 1)
    s = 0.5 - 0.5 * math.cos(math.pi * t)           # ease in/out 0..1
    zoom = 1.0 + MAXZOOM * s
    shift = MAXSHIFT * s
    dispx = (d - 0.55) * shift                       # near pixels shift more
    mapx = (cx + (xs - cx) / zoom - dispx).astype(np.float32)
    mapy = (cy + (ys - cy) / zoom).astype(np.float32)
    frame = cv2.remap(bgr, mapx, mapy, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    cv2.imwrite(os.path.join(FRAMES, f"f{i:04d}.png"), frame)

print("[3.5] synthesize 'wonder' soundscape (wind + rising awe swell + air)", flush=True)
SR = 44100
n = int(SR * DUR)
tt = np.linspace(0, DUR, n)
rng = np.random.default_rng(7)
white = rng.standard_normal(n)
def butter_f(x, cut, btype):
    b, a = butter(2, np.atleast_1d(cut) / (SR / 2), btype=btype); return lfilter(b, a, x)

# cold mountain wind: band-limited noise with slow breathing tremolo
wind = butter_f(white, [180, 1600], "band")
tremolo = 0.6 + 0.4 * np.sin(2 * math.pi * 0.15 * tt)
wind = wind * tremolo * 0.22

# faint high air / starlight shimmer
air = butter_f(rng.standard_normal(n), 6000, "high") * 0.02

# rising "awe" pad: open A-minor-ish chord swelling up then settling (sense of wonder)
chord = [110.0, 164.81, 220.0, 329.63]
pad = sum(np.sin(2 * math.pi * f * tt + p) for f, p in zip(chord, [0, 1.1, 2.3, 0.7]))
pad /= len(chord)
swell = np.clip((1 - np.cos(math.pi * np.minimum(tt / (DUR * 0.7), 1.0))) / 2, 0, 1)  # rise to 70%
pad = pad * swell * 0.30

amb = wind + air + pad
fade = np.ones(n); fl = int(SR * 1.2)
fade[:fl] = np.linspace(0, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
amb = amb * fade
amb = amb / (np.max(np.abs(amb)) + 1e-9) * 0.7
stereo = np.stack([amb, amb], axis=1)
pcm = (stereo * 32767).astype(np.int16)
wavp = os.path.join(OUT, "ambience.wav")
with wave.open(wavp, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

print("[4/4] mux video + audio (libx264, quality-first)", flush=True)
mp4 = os.path.join(OUT, "demo_wonder.mp4")
cmd = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", os.path.join(FRAMES, "f%04d.png"),
       "-i", wavp, "-c:v", "libx264", "-preset", "slow", "-crf", "17",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", mp4]
subprocess.run(cmd, check=True)
print("DONE ->", mp4, flush=True)
