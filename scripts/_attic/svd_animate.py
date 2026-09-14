"""
Real generative motion (local, free): Stable Video Diffusion on RTX 4090.
Animates the actual scene content (aurora, light, atmosphere) from a still.
Clean finish: motion-compensated interpolation -> 1080p Lanczos -> libx264 CRF16.
No film grain, no parallax warping.
"""
import os, subprocess
import torch
from PIL import Image
from diffusers import StableVideoDiffusionPipeline

SRC   = r"C:\Users\aab15\Documents\prime-documentary\_sdxl_test\wonder.png"
OUT   = r"C:\Users\aab15\Documents\prime-documentary\_demo"
FR    = os.path.join(OUT, "svd_frames")
AUDIO = os.path.join(OUT, "wonder_audio.wav")
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR):
    os.remove(os.path.join(FR, f))

print("[1/4] load image (1024x576 for SVD)", flush=True)
img = Image.open(SRC).convert("RGB").resize((1024, 576), Image.LANCZOS)

print("[2/4] load SVD-XT (first run downloads ~9.5GB)", flush=True)
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16, variant="fp16")
pipe.enable_model_cpu_offload()

print("[3/4] generate motion (25 frames)", flush=True)
gen = torch.manual_seed(7)
frames = pipe(img, decode_chunk_size=8, motion_bucket_id=160,
              noise_aug_strength=0.02, num_frames=25, generator=gen).frames[0]
for i, fr in enumerate(frames):
    fr.save(os.path.join(FR, f"s{i:03d}.png"))
print(f"  saved {len(frames)} frames", flush=True)

print("[4/4] interpolate -> 1080p -> encode (clean, CRF16)", flush=True)
mp4 = os.path.join(OUT, "svd_wonder.mp4")
vf = ("[0:v]minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1,"
      "scale=1920:1080:flags=lanczos[v]")
cmd = ["ffmpeg", "-y", "-framerate", "7", "-i", os.path.join(FR, "s%03d.png"),
       "-i", AUDIO, "-filter_complex", vf, "-map", "[v]", "-map", "1:a",
       "-c:v", "libx264", "-preset", "veryslow", "-crf", "16",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k", "-shortest", mp4]
subprocess.run(cmd, check=True)
print("DONE ->", mp4, flush=True)
