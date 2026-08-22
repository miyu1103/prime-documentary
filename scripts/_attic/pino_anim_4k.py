"""
Pino 60s cutout animation — MAX QUALITY. 4K (3840x2160) @ 60fps.
Real Pino assets R-ESRGAN-4x upscaled, background keyed, size/pos normalized,
animated by rigid transform + soft crossfades. Optimized glow (precomputed stamp),
dithered gradient bg (no banding), animated blue particles. libx264 veryslow CRF12.
GUARANTEED no morphing / on-model. Local / free.
"""
import os, math, wave, subprocess
import numpy as np, cv2
from scipy.signal import butter, lfilter

EXPR = r"C:\Users\aab15\Documents\prime-documentary\_demo\pino\hires"
OUT  = r"C:\Users\aab15\Documents\prime-documentary\_demo\pino"
FR   = os.path.join(OUT, "frames4k")
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR):
    os.remove(os.path.join(FR, f))

W, H, FPS, DUR = 3840, 2160, 60, 60.0
N = int(FPS * DUR)
SPR = 1900
CX, CY = W / 2, H / 2 + 60
rng = np.random.default_rng(21)

# ---------- key + normalize sprites ----------
def key(path):
    bgr = cv2.imread(path).astype(np.float32)
    lum = (0.114*bgr[:,:,0] + 0.587*bgr[:,:,1] + 0.299*bgr[:,:,2]) / 255.0
    a = np.clip((lum - 0.10) / 0.35, 0, 1); a = a*a*(3-2*a)
    a = cv2.GaussianBlur(a, (0,0), 2.0)
    return bgr, a

def sprite(fn):
    bgr, a = key(os.path.join(EXPR, fn))
    ys, xs = np.where(a > 0.25)
    y0,y1,x0,x1 = ys.min(),ys.max(),xs.min(),xs.max()
    cb, ca = bgr[y0:y1,x0:x1], a[y0:y1,x0:x1]
    sc = min((0.82*SPR)/(y1-y0), (0.86*SPR)/(x1-x0))
    nw,nh = int((x1-x0)*sc), int((y1-y0)*sc)
    rb = cv2.resize(cb,(nw,nh),interpolation=cv2.INTER_AREA)
    ra = cv2.resize(ca,(nw,nh),interpolation=cv2.INTER_AREA)
    sb = np.zeros((SPR,SPR,3),np.float32); sa = np.zeros((SPR,SPR),np.float32)
    oy,ox=(SPR-nh)//2,(SPR-nw)//2; sb[oy:oy+nh,ox:ox+nw]=rb; sa[oy:oy+nh,ox:ox+nw]=ra
    return sb, sa

USED = {"neutral":"neutral_v001.png","wave":"waving_v001.png","happy":"happy_v002.png",
        "talk":"talking_v001.png","idea":"idea_v003.png","point":"pointing_v001.png",
        "think":"thinking_v002.png"}
SPRITES = {k: sprite(v) for k, v in USED.items()}
print("sprites ready", flush=True)

BEATS = [(0.0,"neutral"),(2.0,"wave"),(8.0,"happy"),(13.0,"talk"),
         (30.0,"idea"),(37.0,"point"),(44.0,"think"),(51.0,"happy"),(56.0,"wave")]
XF = 0.5
def beat_at(t):
    cur = BEATS[0]
    for b in BEATS:
        if b[0] <= t: cur = b
    for b in BEATS:
        if 0 <= (t - b[0]) < XF and b is not BEATS[0]:
            prev = BEATS[BEATS.index(b)-1]
            return prev[1], b[1], (t - b[0]) / XF
    return cur[1], cur[1], 0.0

# ---------- precomputed glow stamp ----------
GS = 2600
gk = cv2.getGaussianKernel(GS, GS*0.17).astype(np.float32); gk = gk @ gk.T; gk /= gk.max()
GLOW = np.stack([gk*255, gk*150, gk*42], 2)   # warm-blue radial

# ---------- particles ----------
NP = 150
px = rng.uniform(0,W,NP); py = rng.uniform(0,H,NP)
psp = rng.uniform(14,46,NP); prad = rng.uniform(3,12,NP); pph = rng.uniform(0,6.28,NP)
def dot(r):
    s=int(r*6)|1; g=cv2.getGaussianKernel(s,r).astype(np.float32); k=g@g.T; return k/k.max()
DOTS={r:dot(r) for r in range(3,15)}

# ---------- bg (dithered gradient) ----------
yyc = np.linspace(0,1,H)[:,None].repeat(W,1)
bg0 = np.zeros((H,W,3),np.float32)
bg0[:,:,0]=44-22*yyc; bg0[:,:,1]=31-15*yyc; bg0[:,:,2]=13-7*yyc
bg0 += rng.uniform(-1.3,1.3,(H,W,1))          # static dither kills banding
yy,xx = np.mgrid[0:H,0:W].astype(np.float32)
rr = np.sqrt(((xx-CX)/(W*0.62))**2 + ((yy-CY)/(H*0.62))**2)
vig = np.clip(1-0.5*np.clip(rr-0.42,0,1)**2,0,1)[...,None]

def over(dst, rgb, a, x, y):
    h,w = rgb.shape[:2]
    x0,y0=max(0,x),max(0,y); x1,y1=min(W,x+w),min(H,y+h)
    if x1<=x0 or y1<=y0: return
    sx,sy=x0-x,y0-y
    r=rgb[sy:sy+(y1-y0),sx:sx+(x1-x0)]; al=a[sy:sy+(y1-y0),sx:sx+(x1-x0)][...,None]
    dst[y0:y1,x0:x1]=dst[y0:y1,x0:x1]*(1-al)+r*al

def add(dst, rgb, x, y, gain):
    h,w = rgb.shape[:2]
    x0,y0=max(0,x),max(0,y); x1,y1=min(W,x+w),min(H,y+h)
    if x1<=x0 or y1<=y0: return
    sx,sy=x0-x,y0-y
    dst[y0:y1,x0:x1]+=rgb[sy:sy+(y1-y0),sx:sx+(x1-x0)]*gain

print("rendering 4K frames", flush=True)
for i in range(N):
    t = i / FPS
    ka,kb,f = beat_at(t)
    sA,aA = SPRITES[ka]; sB,aB = SPRITES[kb]
    spr = sA*(1-f)+sB*f if f>0 else sA
    alp = aA*(1-f)+aB*f if f>0 else aA
    talking = 1.0 if (13.0 <= t < 30.0) else 0.0
    fx = CX + 260*math.sin(2*math.pi*0.018*t) + 20*math.sin(2*math.pi*0.05*t)
    fy = CY + 52*math.sin(2*math.pi*0.2*t)
    sc = 1.0*(1+0.016*math.sin(2*math.pi*0.5*t)+0.018*talking*math.sin(2*math.pi*2.2*t))
    frame = bg0.copy()
    gi = 0.11 + 0.07*talking*(0.5+0.5*math.sin(2*math.pi*1.5*t))
    add(frame, GLOW, int(fx-GS/2), int(fy-GS/2), gi)
    dh = int(SPR*sc)
    rs = cv2.resize(spr,(dh,dh),interpolation=cv2.INTER_AREA if sc<1 else cv2.INTER_CUBIC)
    ra = cv2.resize(alp,(dh,dh),interpolation=cv2.INTER_AREA if sc<1 else cv2.INTER_CUBIC)
    over(frame, rs, ra, int(fx-dh/2), int(fy-dh/2))
    for j in range(NP):
        y=(py[j]-psp[j]*t)%(H+120)-60; x=px[j]+22*math.sin(0.5*t+pph[j])
        r=max(3,min(14,int(prad[j]))); k=DOTS[r]
        amp=(0.5+0.5*math.sin(1.3*t+pph[j]))*(0.6+0.5*talking)
        stamp=np.stack([k*255,k*150,k*40],2)
        add(frame, stamp, int(x-k.shape[1]/2), int(y-k.shape[0]/2), amp*0.6)
    frame = np.clip(frame,0,255)*vig
    if t<1.0: frame*=t/1.0
    if t>DUR-1.2: frame*=max(0,(DUR-t)/1.2)
    cv2.imwrite(os.path.join(FR,f"f{i:05d}.png"), np.clip(frame,0,255).astype(np.uint8))
    if i%120==0: print(f"  {i}/{N}", flush=True)

# ---------- audio ----------
print("audio", flush=True)
SR=44100; n=int(SR*DUR); tt=np.linspace(0,DUR,n)
def eseg(a,b,al,rl):
    e=np.ones(b-a); fa=int(SR*al); fr=int(SR*rl); e[:fa]*=np.linspace(0,1,fa); e[-fr:]*=np.linspace(1,0,fr); return e
prog=[[261.63,329.63,392.00,493.88],[220.00,261.63,329.63,392.00],
      [174.61,261.63,349.23,440.00],[196.00,246.94,392.00,587.33]]
pad=np.zeros(n); seg=n//8
for k in range(8):
    ch=prog[k%4]; a=k*seg; b=min(n,(k+1)*seg); t=tt[a:b]
    pad[a:b]+=sum(np.sin(2*math.pi*fz*t) for fz in ch)/len(ch)*eseg(a,b,0.6,0.6)
pad*=0.18
bells=np.zeros(n)
for j in range(40):
    st=int((j*1.5+0.7)%DUR*SR); fz=523.25*(1+(j%4)*0.16); L=int(SR*0.5)
    if st+L<n: bells[st:st+L]+=np.sin(2*math.pi*fz*np.linspace(0,0.5,L))*np.exp(-np.linspace(0,7,L))*0.12
low=lfilter(*butter(2,120/(SR/2),btype='low'),np.cumsum(rng.standard_normal(n))); low/=(np.max(np.abs(low))+1e-9); low*=0.12
amb=pad+bells+low
fd=np.ones(n); fl=int(SR*1.0); fd[:fl]*=np.linspace(0,1,fl); fd[-fl:]*=np.linspace(1,0,fl)
amb*=fd; amb=amb/(np.max(np.abs(amb))+1e-9)*0.7
wavp=os.path.join(OUT,"pino_audio.wav")
with wave.open(wavp,"wb") as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
    w.writeframes((np.stack([amb,amb],1)*32767).astype(np.int16).tobytes())

print("encode 4K CRF12 veryslow", flush=True)
mp4=os.path.join(r"C:\Users\aab15\Documents\prime-documentary\_demo","pino_60s_4K.mp4")
subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",os.path.join(FR,"f%05d.png"),
    "-i",wavp,"-map","0:v","-map","1:a","-c:v","libx264","-preset","veryslow","-crf","12",
    "-pix_fmt","yuv420p","-x264-params","aq-mode=3:psy-rd=1.0","-c:a","aac","-b:a","320k",
    "-shortest",mp4],check=True)
print("DONE ->",mp4,flush=True)
