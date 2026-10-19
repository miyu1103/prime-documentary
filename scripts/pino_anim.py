"""
Pino 60s cutout animation — GUARANTEED no morphing / on-model.
Uses the REAL Pino assets (Midjourney IP). Background keyed out, each expression
size/position-normalized into a sprite, then animated by rigid transform (float,
drift, breathe) + soft crossfades between expression beats. Animated blue light
particles + gentle whimsical audio. Local / free. 1080p, libx264 CRF15.
"""
import os, math, wave, subprocess
import numpy as np, cv2
from scipy.signal import butter, lfilter

EXPR = r"E:\pd-media\assets\characters\pino\expressions"
OUT  = r"C:\Users\aab15\Documents\prime-documentary\_demo\pino"
FR   = os.path.join(OUT, "frames")
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR):
    os.remove(os.path.join(FR, f))

W, H, FPS, DUR = 1920, 1080, 30, 60.0
N = int(FPS * DUR)
SPR = 900
CX, CY = W / 2, H / 2 + 30

# ---- key + normalize each used expression into a fixed sprite ----
def key(path):
    bgr = cv2.imread(path).astype(np.float32)
    lum = (0.114*bgr[:,:,0] + 0.587*bgr[:,:,1] + 0.299*bgr[:,:,2]) / 255.0
    a = np.clip((lum - 0.10) / 0.35, 0, 1); a = a*a*(3-2*a)
    a = cv2.GaussianBlur(a, (0,0), 1.2)
    return bgr, a

def sprite(fn):
    bgr, a = key(os.path.join(EXPR, fn))
    ys, xs = np.where(a > 0.25)
    y0,y1,x0,x1 = ys.min(),ys.max(),xs.min(),xs.max()
    cb, ca = bgr[y0:y1,x0:x1], a[y0:y1,x0:x1]
    sc = min((0.82*SPR) / (y1-y0), (0.86*SPR) / (x1-x0))   # fit within sprite both ways
    nw,nh = int((x1-x0)*sc), int((y1-y0)*sc)
    rb = cv2.resize(cb,(nw,nh)); ra = cv2.resize(ca,(nw,nh))
    sb = np.zeros((SPR,SPR,3),np.float32); sa = np.zeros((SPR,SPR),np.float32)
    oy,ox = (SPR-nh)//2,(SPR-nw)//2
    sb[oy:oy+nh,ox:ox+nw]=rb; sa[oy:oy+nh,ox:ox+nw]=ra
    return sb, sa

USED = {"neutral":"neutral_v001.png","wave":"waving_v001.png","happy":"happy_v002.png",
        "talk":"talking_v001.png","idea":"idea_v003.png","point":"pointing_v001.png",
        "think":"thinking_v002.png"}
SPRITES = {k: sprite(v) for k, v in USED.items()}
print("sprites ready", flush=True)

# beats: (start_sec, key) ; held with 0.4s crossfades
BEATS = [(0.0,"neutral"),(2.0,"wave"),(8.0,"happy"),(13.0,"talk"),
         (30.0,"idea"),(37.0,"point"),(44.0,"think"),(51.0,"happy"),(56.0,"wave")]
XF = 0.4
def beat_at(t):
    cur = BEATS[0]; nxt = None
    for b in BEATS:
        if b[0] <= t: cur = b
        elif nxt is None: nxt = b
    # crossfade into the next beat over its first XF seconds
    for b in BEATS:
        if 0 <= (t - b[0]) < XF and b is not BEATS[0]:
            prev = BEATS[BEATS.index(b)-1]
            f = (t - b[0]) / XF
            return prev[1], b[1], f
    return cur[1], cur[1], 0.0

# ---- particles (deterministic) ----
rng = np.random.default_rng(21)
NP = 70
px = rng.uniform(0, W, NP); py = rng.uniform(0, H, NP)
psp = rng.uniform(8, 26, NP); prad = rng.uniform(2, 6, NP); pph = rng.uniform(0, 6.28, NP)
def dot(rad):
    s = int(rad*6) | 1
    g = cv2.getGaussianKernel(s, rad).astype(np.float32)
    k = g @ g.T; return k / k.max()
DOTS = {r: dot(r) for r in range(2, 9)}

def particles(t, boost):
    layer = np.zeros((H, W, 3), np.float32)
    for i in range(NP):
        y = (py[i] - psp[i]*t) % (H+80) - 40
        x = px[i] + 12*math.sin(0.5*t + pph[i])
        r = int(prad[i]); k = DOTS[max(2,min(8,r))]
        s = k.shape[0]; yy,xx = int(y-s/2), int(x-s/2)
        y0,y1 = max(0,yy),min(H,yy+s); x0,x1 = max(0,xx),min(W,xx+s)
        if y1<=y0 or x1<=x0: continue
        ky0,kx0 = y0-yy, x0-xx
        amp = (0.5 + 0.5*math.sin(1.3*t+pph[i])) * (0.6+0.5*boost)
        sub = k[ky0:ky0+(y1-y0), kx0:kx0+(x1-x0)] * amp
        layer[y0:y1, x0:x1, 0] += sub*255      # blue
        layer[y0:y1, x0:x1, 1] += sub*150
        layer[y0:y1, x0:x1, 2] += sub*40
    return layer

# ---- background ----
yyc = np.linspace(0,1,H)[:,None].repeat(W,1)
bg0 = np.zeros((H,W,3),np.float32)
bg0[:,:,0]=42-20*yyc; bg0[:,:,1]=30-14*yyc; bg0[:,:,2]=13-7*yyc

# vignette
yy,xx = np.mgrid[0:H,0:W].astype(np.float32)
rr = np.sqrt(((xx-CX)/(W*0.6))**2 + ((yy-CY)/(H*0.6))**2)
vig = np.clip(1-0.5*np.clip(rr-0.4,0,1)**2,0,1)[...,None]

print("rendering frames", flush=True)
for i in range(N):
    t = i / FPS
    ka, kb, f = beat_at(t)
    sa_b, aa = SPRITES[ka]; sb_b, ab = SPRITES[kb]
    if f > 0:
        spr = sa_b*(1-f) + sb_b*f; alp = aa*(1-f) + ab*f
    else:
        spr, alp = sa_b, aa
    talking = 1.0 if (13.0 <= t < 30.0) else 0.0
    # transform: float + drift + breathe
    fx = CX + 130*math.sin(2*math.pi*0.018*t) + 10*math.sin(2*math.pi*0.05*t)
    fy = CY + 26*math.sin(2*math.pi*0.2*t)
    sc = 0.86 * (1 + 0.018*math.sin(2*math.pi*0.5*t) + 0.02*talking*math.sin(2*math.pi*2.2*t))
    M = np.array([[sc,0, fx - sc*SPR/2],[0,sc, fy - sc*SPR/2]], np.float32)
    lr = cv2.warpAffine(spr, M, (W,H))
    la = cv2.warpAffine(alp, M, (W,H))[...,None]
    # soft radial glow behind Pino (pulses when talking)
    glow = np.zeros((H,W,3),np.float32)
    gr = int(260*sc); cv2.circle(glow,(int(fx),int(fy)),gr,(255,150,40),-1)
    glow = cv2.GaussianBlur(glow,(0,0),120) * (0.10+0.06*talking*(0.5+0.5*math.sin(2*math.pi*1.5*t)))
    frame = bg0 + glow
    frame = frame*(1-la) + lr*la
    frame = frame + particles(t, talking)*0.7
    frame = np.clip(frame,0,255)*vig
    # fades
    if t < 1.0: frame *= t/1.0
    if t > DUR-1.2: frame *= max(0,(DUR-t)/1.2)
    cv2.imwrite(os.path.join(FR, f"f{i:05d}.png"), np.clip(frame,0,255).astype(np.uint8))
    if i % 150 == 0: print(f"  {i}/{N}", flush=True)

# ---- audio: whimsical curious pad + sparkles ----
print("audio", flush=True)
SR=44100; n=int(SR*DUR); tt=np.linspace(0,DUR,n)
def env_seg(a,b,al,rl):
    e=np.ones(b-a); fa=int(SR*al); fr=int(SR*rl)
    e[:fa]*=np.linspace(0,1,fa); e[-fr:]*=np.linspace(1,0,fr); return e
prog=[[261.63,329.63,392.00,493.88],[220.00,261.63,329.63,392.00],
      [174.61,261.63,349.23,440.00],[196.00,246.94,392.00,587.33]]
pad=np.zeros(n); seg=n//8
for k in range(8):
    ch=prog[k%len(prog)]; a=k*seg; b=min(n,(k+1)*seg); t=tt[a:b]
    sig=sum(np.sin(2*math.pi*fz*t) for fz in ch)/len(ch)
    pad[a:b]+=sig*env_seg(a,b,0.6,0.6)
pad*=0.18
# sparkles (bells) deterministic
bells=np.zeros(n)
for j in range(40):
    st=int((j*1.5+0.7)%DUR*SR); fz=523.25*(1+ (j%4)*0.16)
    L=int(SR*0.5);
    if st+L<n:
        seg2=np.sin(2*math.pi*fz*np.linspace(0,0.5,L))*np.exp(-np.linspace(0,7,L))
        bells[st:st+L]+=seg2*0.12
low=lfilter(*butter(2,120/(SR/2),btype='low'),np.cumsum(rng.standard_normal(n)))
low/=(np.max(np.abs(low))+1e-9); low*=0.12
amb=pad+bells+low
fade=np.ones(n); fl=int(SR*1.0); fade[:fl]*=np.linspace(0,1,fl); fade[-fl:]*=np.linspace(1,0,fl)
amb*=fade; amb=amb/(np.max(np.abs(amb))+1e-9)*0.7
wavp=os.path.join(OUT,"pino_audio.wav")
with wave.open(wavp,"wb") as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
    w.writeframes((np.stack([amb,amb],1)*32767).astype(np.int16).tobytes())

print("encode", flush=True)
mp4=os.path.join(r"C:\Users\aab15\Documents\prime-documentary\_demo","pino_60s.mp4")
subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",os.path.join(FR,"f%05d.png"),
    "-i",wavp,"-map","0:v","-map","1:a","-c:v","libx264","-preset","veryslow","-crf","15",
    "-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-shortest",mp4],check=True)
print("DONE ->",mp4,flush=True)
