import os, numpy as np, cv2
P = r"E:\pd-media\assets\characters\pino\expressions"
OUT = r"C:\Users\aab15\Documents\prime-documentary\_demo\pino"
os.makedirs(OUT, exist_ok=True)

def key_pino(path):
    bgr = cv2.imread(path).astype(np.float32)
    h, w = bgr.shape[:2]
    lum = (0.114*bgr[:,:,0] + 0.587*bgr[:,:,1] + 0.299*bgr[:,:,2]) / 255.0
    # dark teal bg -> 0, bright fluffy Pino + glow -> 1 (smoothstep)
    lo, hi = 0.10, 0.45
    a = np.clip((lum - lo) / (hi - lo), 0, 1)
    a = a*a*(3 - 2*a)                          # smoothstep feather
    a = cv2.GaussianBlur(a, (0,0), 1.2)
    return bgr, a

def composite(bgr, a, bg):
    a3 = a[..., None]
    return (bgr * a3 + bg * (1 - a3)).astype(np.uint8)

# animated dark-teal background sample
H, W = 1080, 1920
yy = np.linspace(0, 1, H)[:, None]
bg = np.zeros((H, W, 3), np.float32)
bg[:, :, 0] = 40 - 18*yy[:,0][:,None].repeat(W,1)   # B
bg[:, :, 1] = 30 - 14*yy[:,0][:,None].repeat(W,1)   # G
bg[:, :, 2] = 12 - 6*yy[:,0][:,None].repeat(W,1)    # R

samples = ["neutral_v001.png", "waving_v001.png", "talking_v001.png"]
tiles = []
for s in samples:
    bgr, a = key_pino(os.path.join(P, s))
    # center Pino on bg by alpha bbox
    ys, xs = np.where(a > 0.3)
    if len(xs):
        cy, cx = int(ys.mean()), int(xs.mean())
    else:
        cy, cx = bgr.shape[0]//2, bgr.shape[1]//2
    canvas = bg.copy()
    ph, pw = bgr.shape[:2]
    oy, ox = H//2 - cy, W//2 - cx
    # paste with offset
    ys0, ys1 = max(0, oy), min(H, oy+ph)
    xs0, xs1 = max(0, ox), min(W, ox+pw)
    sy0, sx0 = ys0-oy, xs0-ox
    sub = canvas[ys0:ys1, xs0:xs1]
    comp = composite(bgr[sy0:sy0+(ys1-ys0), sx0:sx0+(xs1-xs0)],
                     a[sy0:sy0+(ys1-ys0), sx0:sx0+(xs1-xs0)], sub)
    canvas[ys0:ys1, xs0:xs1] = comp
    tiles.append(cv2.resize(canvas, (480, 270)))
sheet = np.hstack(tiles)
cv2.imwrite(os.path.join(OUT, "_key_test.png"), sheet)
# also save alpha preview of neutral
_, a = key_pino(os.path.join(P, "neutral_v001.png"))
cv2.imwrite(os.path.join(OUT, "_alpha.png"), (a*255).astype(np.uint8))
print("done")
