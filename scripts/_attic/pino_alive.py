"""
Pino — ALIVE cutout animation (squash/stretch, hops, secondary motion, anticipation).
Real Pino assets (R-ESRGAN hires), keyed, deformed each frame by SHAPE-PRESERVING
warps => feels animated, never morphs identity.
TEST=True -> quick 1080p/8s preview;  TEST=False -> full 4K/60s.
"""
import os, math, wave, subprocess
import numpy as np, cv2
from scipy.signal import butter, lfilter

TEST = True

EXPR = r"C:\Users\aab15\Documents\prime-documentary\_demo\pino\hires"
OUT  = r"C:\Users\aab15\Documents\prime-documentary\_demo\pino"
FR   = os.path.join(OUT, "frames_alive")
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR):
    os.remove(os.path.join(FR, f))

if TEST:
    W, H, FPS, DUR = 1280, 720, 30, 8.0
    SPR = 720
    OUTNAME = "pino_alive_test.mp4"
else:
    W, H, FPS, DUR = 3840, 2160, 60, 60.0
    SPR = 1900
    OUTNAME = "pino_60s_4K_alive.mp4"
N = int(FPS * DUR)
CX, CY = W/2, H*0.60
rng = np.random.default_rng(21)

def key(path):
    bgr = cv2.imread(path).astype(np.float32)
    lum = (0.114*bgr[:,:,0]+0.587*bgr[:,:,1]+0.299*bgr[:,:,2])/255.0
    a = np.clip((lum-0.10)/0.35,0,1); a=a*a*(3-2*a); a=cv2.GaussianBlur(a,(0,0),2.0)
    return bgr,a
def sprite(fn):
    bgr,a=key(os.path.join(EXPR,fn))
    ys,xs=np.where(a>0.25); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
    cb,ca=bgr[y0:y1,x0:x1],a[y0:y1,x0:x1]
    sc=min((0.80*SPR)/(y1-y0),(0.84*SPR)/(x1-x0))
    nw,nh=int((x1-x0)*sc),int((y1-y0)*sc)
    rb=cv2.resize(cb,(nw,nh),cv2.INTER_AREA); ra=cv2.resize(ca,(nw,nh),cv2.INTER_AREA)
    sb=np.zeros((SPR,SPR,3),np.float32); sa=np.zeros((SPR,SPR),np.float32)
    oy,ox=(SPR-nh)//2,(SPR-nw)//2; sb[oy:oy+nh,ox:ox+nw]=rb; sa[oy:oy+nh,ox:ox+nw]=ra
    # feet line (bottom of opaque region) for squash pivot
    foot = oy+nh
    return sb,sa,foot
USED={"neutral":"neutral_v001.png","wave":"waving_v001.png","happy":"happy_v002.png",
      "talk":"talking_v001.png","idea":"idea_v003.png","point":"pointing_v001.png",
      "think":"thinking_v002.png"}
SP={k:sprite(v) for k,v in USED.items()}
print("sprites ready",flush=True)

# beats: (t, key, x_fraction)  Pino hops between spots
BEATS=[(0.0,"neutral",0.50),(2.0,"wave",0.50),(8.0,"happy",0.40),(13.0,"talk",0.50),
       (30.0,"idea",0.62),(37.0,"point",0.68),(44.0,"think",0.36),(51.0,"happy",0.50),(56.0,"wave",0.50)]
if TEST:
    BEATS=[(0.0,"neutral",0.40),(1.2,"wave",0.40),(3.5,"happy",0.60),(5.5,"talk",0.60)]
XF=0.45
def smooth(a): return a*a*(3-2*a)
def state(t):
    cur=BEATS[0]
    for b in BEATS:
        if b[0]<=t: cur=b
    ka=kb=cur[1]; f=0.0
    for b in BEATS:
        if 0<=(t-b[0])<XF and b is not BEATS[0]:
            prev=BEATS[BEATS.index(b)-1]; ka,kb,f=prev[1],b[1],(t-b[0])/XF
    # x position eased across beats
    ts=[b[0] for b in BEATS]; xs=[b[2] for b in BEATS]
    if t<=ts[0]: xf=xs[0]
    elif t>=ts[-1]: xf=xs[-1]
    else:
        for j in range(len(ts)-1):
            if ts[j]<=t<ts[j+1]:
                u=smooth((t-ts[j])/(ts[j+1]-ts[j])); xf=xs[j]+(xs[j+1]-xs[j])*u; break
    return ka,kb,f,xf

# secondary-motion grid (top wobble shear)
gy,gx=np.mgrid[0:SPR,0:SPR].astype(np.float32)
topmask=np.clip((SPR*0.5-gy)/(SPR*0.5),0,1)        # 1 at top -> 0 at center

# glow stamp
GS=int(SPR*1.5)|1
gk=cv2.getGaussianKernel(GS,GS*0.17).astype(np.float32); gk=gk@gk.T; gk/=gk.max()
GLOW=np.stack([gk*255,gk*150,gk*42],2)
# particles
NP=120 if not TEST else 60
ppx=rng.uniform(0,W,NP); ppy=rng.uniform(0,H,NP); psp=rng.uniform(14,46,NP)
prad=rng.uniform(3,12,NP); pph=rng.uniform(0,6.28,NP)
def dot(r):
    s=int(r*6)|1; g=cv2.getGaussianKernel(s,r).astype(np.float32); k=g@g.T; return k/k.max()
DOTS={r:dot(r) for r in range(3,15)}
# bg
yyc=np.linspace(0,1,H)[:,None].repeat(W,1)
bg0=np.zeros((H,W,3),np.float32)
bg0[:,:,0]=44-22*yyc; bg0[:,:,1]=31-15*yyc; bg0[:,:,2]=13-7*yyc
bg0+=rng.uniform(-1.3,1.3,(H,W,1))
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
rr=np.sqrt(((xx-CX)/(W*0.62))**2+((yy-CY)/(H*0.62))**2)
vig=np.clip(1-0.5*np.clip(rr-0.42,0,1)**2,0,1)[...,None]

def over(dst,rgb,a,x,y):
    h,w=rgb.shape[:2]; x0,y0=max(0,x),max(0,y); x1,y1=min(W,x+w),min(H,y+h)
    if x1<=x0 or y1<=y0: return
    sx,sy=x0-x,y0-y; r=rgb[sy:sy+(y1-y0),sx:sx+(x1-x0)]; al=a[sy:sy+(y1-y0),sx:sx+(x1-x0)][...,None]
    dst[y0:y1,x0:x1]=dst[y0:y1,x0:x1]*(1-al)+r*al
def add(dst,rgb,x,y,g):
    h,w=rgb.shape[:2]; x0,y0=max(0,x),max(0,y); x1,y1=min(W,x+w),min(H,y+h)
    if x1<=x0 or y1<=y0: return
    sx,sy=x0-x,y0-y; dst[y0:y1,x0:x1]+=rgb[sy:sy+(y1-y0),sx:sx+(x1-x0)]*g

HOP = 0.10*H        # hop height
print(f"rendering ({'TEST' if TEST else 'FULL'}) {N} frames",flush=True)
dt=1.0/FPS
def xfrac_of(t):
    return state(t)[3]
for i in range(N):
    t=i*dt
    ka,kb,f,xf=state(t)
    sA,aA,ftA=SP[ka]; sB,aB,ftB=SP[kb]
    spr=sA*(1-f)+sB*f if f>0 else sA
    alp=aA*(1-f)+aB*f if f>0 else aA
    wave_on=1.0 if ka in("wave",) or kb in("wave",) else 0.0
    talk=1.0 if (ka=="talk" or kb=="talk") else 0.0
    # bounce (hops). faster/bigger while moving horizontally
    vx=(xfrac_of(min(DUR,t+dt))-xfrac_of(max(0,t-dt)))/(2*dt)   # horiz velocity (frac/s)
    moving=min(1.0,abs(vx)*3.0)
    hopf=1.1+0.6*moving
    b=abs(math.sin(math.pi*hopf*t))                # 0 landing .. 1 apex
    bob=-(HOP*(0.35+0.65*moving))*b
    # squash/stretch (volume preserving), squashed at landing, stretched at apex
    sq=1.0+0.10*(b-0.5)+0.03*talk*math.sin(2*math.pi*3.0*t)
    sy=sq; sx=1.0/sq
    base=1.0
    # secondary wobble: top shear lagging motion + idle sway
    shear=(0.06*math.sin(2*math.pi*0.9*t-1.0)+0.10*vx)
    dispx=shear*topmask*SPR*0.18
    mapx=(gx+dispx).astype(np.float32); mapy=gy
    sprw=cv2.remap(spr,mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
    alpw=cv2.remap(alp,mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
    # anticipation lean into movement
    lean=-7.0*vx
    # placement
    fx=CX+(xf-0.5)*W*0.9
    fy=CY+bob
    foot=ftA*(1-f)+ftB*f
    # affine: lean(rot) + anisotropic squash about feet, then translate so feet stay at fy
    M=cv2.getRotationMatrix2D((SPR/2,foot),lean,base)
    M=np.vstack([M,[0,0,1]])
    S=np.array([[sx,0,SPR/2*(1-sx)],[0,sy,foot*(1-sy)],[0,0,1]],np.float32)
    A=(M@S)[:2]
    A[0,2]+=fx-SPR/2; A[1,2]+=fy-foot
    lr=cv2.warpAffine(sprw,A,(W,H),flags=cv2.INTER_CUBIC)
    la=cv2.warpAffine(alpw,A,(W,H),flags=cv2.INTER_LINEAR)[...,None]
    # frame
    frame=bg0.copy()
    gi=0.11+0.06*talk*(0.5+0.5*math.sin(2*math.pi*1.5*t))+0.05*wave_on*b
    add(frame,GLOW,int(fx-GS/2),int(fy-GS/2),gi)
    frame=frame*(1-la)+lr*la
    pboost=0.6+0.6*wave_on*b+0.4*talk
    for j in range(NP):
        y=(ppy[j]-psp[j]*t)%(H+120)-60; x=ppx[j]+22*math.sin(0.5*t+pph[j])
        r=max(3,min(14,int(prad[j]))); k=DOTS[r]
        amp=(0.5+0.5*math.sin(1.3*t+pph[j]))*pboost*0.55
        st=np.stack([k*255,k*150,k*40],2)
        add(frame,st,int(x-k.shape[1]/2),int(y-k.shape[0]/2),amp)
    frame=np.clip(frame,0,255)*vig
    if t<0.8: frame*=t/0.8
    if t>DUR-1.0: frame*=max(0,(DUR-t)/1.0)
    cv2.imwrite(os.path.join(FR,f"f{i:05d}.png"),np.clip(frame,0,255).astype(np.uint8))
    if i%60==0: print(f"  {i}/{N}",flush=True)

# audio
print("audio",flush=True)
SR=44100; n=int(SR*DUR); tt=np.linspace(0,DUR,n)
def eseg(a,b,al,rl):
    e=np.ones(b-a); fa=int(SR*al); fr=int(SR*rl); e[:fa]*=np.linspace(0,1,fa); e[-fr:]*=np.linspace(1,0,fr); return e
prog=[[261.63,329.63,392.0,493.88],[220.0,261.63,329.63,392.0],[174.61,261.63,349.23,440.0],[196.0,246.94,392.0,587.33]]
pad=np.zeros(n); ns=8 if not TEST else 2; seg=n//ns
for k in range(ns):
    ch=prog[k%4]; a=k*seg; b=min(n,(k+1)*seg); t=tt[a:b]
    pad[a:b]+=sum(np.sin(2*math.pi*fz*t) for fz in ch)/len(ch)*eseg(a,b,0.5,0.5)
pad*=0.18
low=lfilter(*butter(2,120/(SR/2),btype='low'),np.cumsum(rng.standard_normal(n))); low/=(np.max(np.abs(low))+1e-9); low*=0.12
amb=pad+low; fd=np.ones(n); fl=int(SR*0.8); fd[:fl]*=np.linspace(0,1,fl); fd[-fl:]*=np.linspace(1,0,fl)
amb*=fd; amb=amb/(np.max(np.abs(amb))+1e-9)*0.7
wavp=os.path.join(OUT,"pino_audio2.wav")
with wave.open(wavp,"wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.stack([amb,amb],1)*32767).astype(np.int16).tobytes())

print("encode",flush=True)
crf="16" if TEST else "12"
mp4=os.path.join(r"C:\Users\aab15\Documents\prime-documentary\_demo",OUTNAME)
subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",os.path.join(FR,"f%05d.png"),
  "-i",wavp,"-map","0:v","-map","1:a","-c:v","libx264","-preset","veryslow" if not TEST else "medium",
  "-crf",crf,"-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-shortest",mp4],check=True)
print("DONE ->",mp4,flush=True)
