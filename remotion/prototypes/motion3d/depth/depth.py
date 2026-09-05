import sys, numpy as np
import torch
from PIL import Image, ImageFilter
from transformers import pipeline

inp, outp = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "Intel/dpt-hybrid-midas"
device = 0 if torch.cuda.is_available() else -1
print("device", device, "model", model)

pipe = pipeline("depth-estimation", model=model, device=device)
img = Image.open(inp).convert("RGB")
res = pipe(img)
depth = res["depth"]  # PIL image (near = bright)

# normalize to full 0..255 and lightly blur so the displaced mesh isn't jagged
d = np.asarray(depth).astype(np.float32)
d = (d - d.min()) / (d.max() - d.min() + 1e-6)
dimg = Image.fromarray((d * 255).astype(np.uint8), mode="L")
dimg = dimg.resize(img.size).filter(ImageFilter.GaussianBlur(2))
dimg.save(outp)
print("saved", outp, dimg.size)
