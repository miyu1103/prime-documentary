"""
MAX-QUALITY demo: 4K master -> DPT-Large depth -> 2.5D parallax rendered at 4K
(supersampled) -> downscale 1080p -> cinematic grade + vignette + film grain ->
libx264 veryslow CRF15 + loudness-normalized 'wonder' soundscape.
Fully local (RTX 4090). No paid services. Audio synthesized (rights-clean).
"""
import os, math, wave, subprocess
import numpy as np
import cv2
import torch
from PIL import Image
from scipy.signal import butter, lfilter, fftconvolve

MASTER = r"C:\Users\aab15\Documents\prime-documentary\_sdxl_test\wonder_4k.png"
OUT    = r"C:\Users\aab15\Documents\prime-documentary\_demo"
FRAMES = os.path.join(OUT, "frames_hq")
os.makedirs(FRAMES, exist_ok=True)
for f in os.listdir(FRAMES):
    os.remove(os.path.join(FRAMES, f))

RW, RH = 3840, 2160          # render (supersample) resolution
OW, OH = 1920, 1080          # output resolution
FPS, DUR = 60, 8.0
N = int(FPS * DUR)

print("[1/5] load 4K master", flush=True)
master = cv2.imread(MASTER)
master = cv2.resize(master, (RW, RH), interpolation=cv2.INTER_AREA)

print("[2/5] depth estimation (DPT-Large, GPU)", flush=True)
from transformers import DPTImageProcessor, DPTForDepthEstimation
dev = "cuda" if torch.cuda.is_available() else "cpu"
proc = DPTImageProcessor.from_pretrained("Intel/dpt-large")
model = DPTForDepthEstimation.from_pretrained("Intel/dpt-large").to(dev).eval()
rgb = cv2.cvtColor(cv2.resize(master, (1024, 576)), cv2.COLOR_BGR2RGB)
inp = proc(images=Image.fromarray(rgb), return_tensors="pt").to(dev)
with torch.no_grad():
    pred = model(**inp).predicted_depth
depth = torch.nn.functional.interpolate(pred.unsqueeze(1), size=(RH, RW),
        mode="bicubic", align_corners=False).squeeze().cpu().numpy()
d = (depth - depth.min()) / (depth.max() - depth.min() + 1e-8)   # 1 = near
d = cv2.bilateralFilter(d.astype(np.float32), 9, 0.1, 9)          # edge-aware smooth
cv2.imwrite(os.path.join(OUT, "depth_hq.png"), (d * 255).astype(np.uint8))

print("[3/5] precompute grade LUT / vignette / grids", flush=True)
# cinematic S-curve contrast + lifted cool shadows + warm highlights
x = np.linspace(0, 1, 256)
scurve = np.clip(x + 0.18 * np.sin(2 * math.pi * (x - 0.0)) * (x * (1 - x)) * 4, 0, 1)
def chan_lut(gamma, lift, gain):
    v = np.clip((scurve ** gamma) * gain + lift, 0, 1)
    return (v * 255).astype(np.uint8)
lut_b = chan_lut(0.96, 0.012, 1.02)   # slight cool lift in shadows (blue)
lut_g = chan_lut(1.00, 0.004, 1.00)
lut_r = chan_lut(1.03, 0.000, 1.02)   # warm highlights
# vignette (output res)
yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32)
cx, cy = OW / 2, OH / 2
r = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)
vig = np.clip(1.0 - 0.28 * np.clip(r - 0.5, 0, 1) ** 2, 0, 1)[..., None]
# render grids
gx, gy = np.meshgrid(np.arange(RW), np.arange(RH))
gx = gx.astype(np.float32); gy = gy.astype(np.float32)
RCX, RCY = RW / 2.0, RH / 2.0
MAXSHIFT, MAXPAN, MAXZOOM = 60.0, 45.0, 0.12
rng = np.random.default_rng(11)

print(f"[4/5] render {N} frames (4K -> 1080p, grade+grain)", flush=True)
for i in range(N):
    t = i / (N - 1)
    s = 0.5 - 0.5 * math.cos(math.pi * t)                 # ease in/out
    zoom = 1.0 + MAXZOOM * s
    shift = MAXSHIFT * s
    pan = MAXPAN * s
    dispx = (d - 0.5) * shift                             # parallax: near moves more
    mapx = (RCX + (gx - RCX) / zoom - dispx).astype(np.float32)
    mapy = (RCY + (gy - RCY) / zoom + pan).astype(np.float32)   # slow upward reveal
    big = cv2.remap(master, mapx, mapy, interpolation=cv2.INTER_CUBIC,
                    borderMode=cv2.BORDER_REFLECT)
    f = cv2.resize(big, (OW, OH), interpolation=cv2.INTER_AREA)  # supersample down
    # grade
    f = cv2.merge([cv2.LUT(f[:, :, 0], lut_b),
                   cv2.LUT(f[:, :, 1], lut_g),
                   cv2.LUT(f[:, :, 2], lut_r)])
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.12, 0, 255)   # saturation
    f = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    # vignette
    f = (f.astype(np.float32) * vig).astype(np.uint8)
    # subtle film grain (luminance)
    grain = rng.standard_normal((OH, OW, 1)).astype(np.float32) * 3.2
    f = np.clip(f.astype(np.float32) + grain, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(FRAMES, f"f{i:05d}.png"), f)

print("[4.5] synthesize + master 'wonder' soundscape", flush=True)
SR = 44100
n = int(SR * DUR)
tt = np.linspace(0, DUR, n)
def butter_f(x, cut, btype):
    b, a = butter(2, np.atleast_1d(cut) / (SR / 2), btype=btype); return lfilter(b, a, x)
white = rng.standard_normal(n)
wind = butter_f(white, [180, 1600], "band") * (0.6 + 0.4 * np.sin(2 * math.pi * 0.13 * tt)) * 0.22
air  = butter_f(rng.standard_normal(n), 6000, "high") * 0.02
chord = [110.0, 164.81, 220.0, 329.63]
pad = sum(np.sin(2 * math.pi * fhz * tt + p) for fhz, p in zip(chord, [0, 1.1, 2.3, 0.7])) / len(chord)
swell = np.clip((1 - np.cos(math.pi * np.minimum(tt / (DUR * 0.7), 1.0))) / 2, 0, 1)
pad = pad * swell * 0.30
amb = wind + air + pad
# simple reverb (exp-decay noise impulse), wet/dry
ir = (rng.standard_normal(int(SR * 0.5)) * np.exp(-np.linspace(0, 6, int(SR * 0.5)))).astype(np.float32)
wet = fftconvolve(amb, ir)[:n]
amb = 0.75 * amb + 0.25 * (wet / (np.max(np.abs(wet)) + 1e-9))
# fades
fade = np.ones(n); fl = int(SR * 1.2)
fade[:fl] = np.linspace(0, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
amb *= fade
# loudness: ~ -16 dBFS RMS (≈ -14 LUFS-ish for this bed) + peak guard at -1 dBFS
rms = np.sqrt(np.mean(amb ** 2)) + 1e-9
amb *= (10 ** (-16 / 20)) / rms
peak = np.max(np.abs(amb)) + 1e-9
amb *= min(1.0, (10 ** (-1 / 20)) / peak)
pcm = (np.stack([amb, amb], axis=1) * 32767).astype(np.int16)
wavp = os.path.join(OUT, "wonder_audio.wav")
with wave.open(wavp, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

print("[5/5] encode (libx264 veryslow CRF15, tune film)", flush=True)
mp4 = os.path.join(OUT, "demo_wonder_HQ.mp4")
cmd = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", os.path.join(FRAMES, "f%05d.png"),
       "-i", wavp, "-c:v", "libx264", "-preset", "veryslow", "-crf", "15",
       "-tune", "film", "-pix_fmt", "yuv420p", "-x264-params", "ref=6:bframes=8",
       "-c:a", "aac", "-b:a", "320k", "-shortest", mp4]
subprocess.run(cmd, check=True)
print("DONE ->", mp4, flush=True)
