r"""Batch depth-map generator for the CaseFilm `depth` treatment.
For every image in a folder, writes <name>_depth.png (near=white/far=black) beside it.
Run with the ComfyUI venv python (torch+transformers, DPT cached in HF hub):
  C:\Users\aab15\ComfyUI\venv\Scripts\python.exe tools/depth/gen_depth.py remotion/public/forfeiture
Use Intel/dpt-large (safetensors): transformers 5.x refuses .bin on torch<2.6 (CVE-2025-32434).
"""
import sys, os, glob
import numpy as np, torch
from PIL import Image, ImageFilter
from transformers import pipeline

IN = sys.argv[1]
MODEL = sys.argv[2] if len(sys.argv) > 2 else "Intel/dpt-large"
device = 0 if torch.cuda.is_available() else -1
print("device", device, "model", MODEL)
pipe = pipeline("depth-estimation", model=MODEL, device=device)

if os.path.isfile(IN):
    imgs = [IN]
else:
    imgs = sorted(p for ext in ("jpg", "jpeg", "png", "webp") for p in glob.glob(os.path.join(IN, f"*.{ext}")))

for p in imgs:
    base, _ = os.path.splitext(p)
    if base.endswith("_depth"):
        continue
    outp = base + "_depth.png"
    if os.path.exists(outp):
        print("skip", outp); continue
    img = Image.open(p).convert("RGB")
    d = np.asarray(pipe(img)["depth"]).astype("float32")
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)
    Image.fromarray((d * 255).astype("uint8"), "L").resize(img.size).filter(ImageFilter.GaussianBlur(2)).save(outp)
    print("depth", outp)
print("done", len(imgs))
