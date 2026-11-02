"""
30s meaningful cat story (6 shots, edited).
Per shot: SVD motion (chained, per-shot strength) -> R-ESRGAN upscale -> 1080p
supersample -> handheld + warmth-ramp grade + film grain -> 5s shot.
Concatenated to 30s with an emotional synth pad + rain ambience.
Local / free (RTX 4090). MAX quality (CRF13).
"""
import os, math, base64, subprocess, wave
import numpy as np, cv2, torch, requests
from PIL import Image
from diffusers import StableVideoDiffusionPipeline
from scipy.signal import butter, lfilter

SDIR = r"C:\Users\aab15\Documents\prime-documentary\_sdxl_test\cat_story"
OUT  = r"C:\Users\aab15\Documents\prime-documentary\_demo"
WORK = os.path.join(OUT, "cat_work")
API  = "http://127.0.0.1:7860/sdapi/v1/extra-single-image"
os.makedirs(WORK, exist_ok=True)
W, H, SHOT_SEC, FPS = 1920, 1080, 5.0, 30
# (motion_bucket, chunks) per shot — LOW motion on cats to stop morphing ("guny")
CFG = [(30, 1), (30, 1), (16, 1), (95, 2), (32, 1), (26, 1)]
# clean directional camera drift per shot (px over the shot) to add life without warping
PAN = [(10, 0), (0, -8), (-6, 0), (8, 0), (0, -10), (-8, 0)]
rng = np.random.default_rng(7)

# ---------- phase 1: SVD generation ----------
print("[1] SVD generate all shots", flush=True)
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16, variant="fp16")
pipe.enable_model_cpu_offload()
raw_counts = []
for s, (mb, nch) in enumerate(CFG):
    img = Image.open(os.path.join(SDIR, f"shot{s}.png")).convert("RGB").resize((1024, 576), Image.LANCZOS)
    frames, cur = [], img
    for c in range(nch):
        out = pipe(cur, decode_chunk_size=8, motion_bucket_id=mb,
                   noise_aug_strength=0.02, num_frames=25,
                   generator=torch.manual_seed(10 + s * 7 + c)).frames[0]
        frames += out if c == 0 else out[1:]
        cur = out[-1]
    rd = os.path.join(WORK, f"raw{s}"); os.makedirs(rd, exist_ok=True)
    for j in [int(x) for x in os.listdir(rd)] if False else []:
        pass
    for f in os.listdir(rd):
        os.remove(os.path.join(rd, f))
    for j, fr in enumerate(frames):
        fr.save(os.path.join(rd, f"r{j:04d}.png"))
    raw_counts.append(len(frames))
    print(f"   shot{s}: {len(frames)} frames", flush=True)
del pipe; torch.cuda.empty_cache()

# ---------- phase 2: upscale + grade + grain ----------
print("[2] R-ESRGAN upscale + grade + grain", flush=True)
def resrgan(bgr):
    ok, buf = cv2.imencode(".png", bgr)
    r = requests.post(API, json={"image": base64.b64encode(buf).decode(),
        "upscaling_resize": 2, "upscaler_1": "R-ESRGAN 4x+", "upscaler_2": "None"}, timeout=180)
    return cv2.imdecode(np.frombuffer(base64.b64decode(r.json()["image"]), np.uint8), cv2.IMREAD_COLOR)

def grade(f, warm):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] *= 0.92
    f = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    f = (f - 128) * 0.97 + 128
    f[:, :, 2] += warm; f[:, :, 0] -= warm * 0.6           # warmth ramp (B,G,R order)
    return np.clip(f, 0, 255).astype(np.uint8)

for s in range(len(CFG)):
    rd = os.path.join(WORK, f"raw{s}"); fd = os.path.join(WORK, f"fin{s}")
    os.makedirs(fd, exist_ok=True)
    for f in os.listdir(fd):
        os.remove(os.path.join(fd, f))
    n = raw_counts[s]
    warm = -4 + 12 * (s / (len(CFG) - 1))                  # cool -> warm across story
    for i in range(n):
        bgr = cv2.imread(os.path.join(rd, f"r{i:04d}.png"))
        try:
            big = resrgan(bgr)
        except Exception:
            big = cv2.resize(bgr, (W * 2, H * 2), interpolation=cv2.INTER_LANCZOS4)
        up = cv2.resize(big, (W, H), interpolation=cv2.INTER_AREA)
        e = i / max(1, n - 1)
        ease = 0.5 - 0.5 * math.cos(math.pi * e)
        dx = 3 * math.sin(i * 0.18 + s) + PAN[s][0] * ease
        dy = 2.5 * math.sin(i * 0.14 + s) + PAN[s][1] * ease
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0.12 * math.sin(i * 0.11), 1.0 + 0.09 * ease)
        M[0, 2] += dx; M[1, 2] += dy
        f = cv2.warpAffine(up, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        f = grade(f, warm)
        g = cv2.resize(rng.standard_normal((H // 2, W // 2, 1)).astype(np.float32), (W, H),
                       interpolation=cv2.INTER_LINEAR)[..., None]
        f = np.clip(f.astype(np.float32) + g * 3.0, 0, 255).astype(np.uint8)
        cv2.imwrite(os.path.join(fd, f"s{i:04d}.png"), f)
    print(f"   shot{s} finished", flush=True)

# ---------- phase 3: encode each shot to 5s ----------
print("[3] encode shots", flush=True)
# blend interpolation = NO geometric warping (fixes the "guny" cat); low motion keeps it clean
vf = "[0:v]minterpolate=fps=30:mi_mode=blend[v]"
shot_mp4s = []
for s in range(len(CFG)):
    fd = os.path.join(WORK, f"fin{s}")
    in_fps = raw_counts[s] / SHOT_SEC
    mp4 = os.path.join(WORK, f"shot{s}.mp4")
    cmd = ["ffmpeg", "-y", "-framerate", f"{in_fps:.4f}", "-i", os.path.join(fd, "s%04d.png"),
           "-filter_complex", vf, "-map", "[v]", "-c:v", "libx264", "-preset", "veryslow",
           "-crf", "13", "-pix_fmt", "yuv420p", "-r", "30", mp4]
    subprocess.run(cmd, check=True)
    shot_mp4s.append(mp4)

# ---------- phase 4: emotional audio (pad + rain) ----------
print("[4] build 30s audio", flush=True)
SR = 44100; DUR = 30.0; n = int(SR * DUR); tt = np.linspace(0, DUR, n)
def bf(x, cut, bt):
    b, a = butter(2, np.atleast_1d(cut) / (SR / 2), btype=bt); return lfilter(b, a, x)
# chord progression Am -> F -> C -> G -> C (emotional, resolving warm)
chords = [[220.00,261.63,329.63],[174.61,220.00,261.63],[261.63,329.63,392.00],
          [196.00,246.94,392.00],[261.63,329.63,392.00],[261.63,329.63,392.00]]
pad = np.zeros(n)
seg = n // len(chords)
for k, ch in enumerate(chords):
    a, b = k * seg, min(n, (k + 1) * seg)
    t = tt[a:b]
    sig = sum(0.5*np.sin(2*math.pi*f*t) + 0.5*np.sign(np.sin(2*math.pi*f*t))*0.04 for f in ch) / len(ch)
    env = np.ones(b - a); xf = int(SR * 0.8)
    env[:xf] *= np.linspace(0, 1, xf); env[-xf:] *= np.linspace(1, 0, xf)
    pad[a:b] += sig * env
pad *= 0.22
rain = bf(rng.standard_normal(n), [600, 9000], "band")
rain_env = np.interp(tt, [0, 24, 30], [0.22, 0.22, 0.06])   # rain fades indoors at the end
rain *= rain_env
amb = pad + rain
fade = np.ones(n); fl = int(SR * 1.5)
fade[:fl] = np.linspace(0, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
amb *= fade; amb = amb / (np.max(np.abs(amb)) + 1e-9) * 0.7
wavp = os.path.join(WORK, "story_audio.wav")
with wave.open(wavp, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.stack([amb, amb], 1) * 32767).astype(np.int16).tobytes())

# ---------- phase 5: concat + mux ----------
print("[5] concat + mux", flush=True)
listf = os.path.join(WORK, "list.txt")
with open(listf, "w") as f:
    for m in shot_mp4s:
        f.write(f"file '{m}'\n")
joined = os.path.join(WORK, "joined.mp4")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listf, "-c", "copy", joined], check=True)
final = os.path.join(OUT, "cat_story_30s.mp4")
subprocess.run(["ffmpeg", "-y", "-i", joined, "-i", wavp, "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", final], check=True)
print("DONE ->", final, flush=True)
