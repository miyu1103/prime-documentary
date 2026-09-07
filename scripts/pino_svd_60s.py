"""
Pino 60s — SVD organic motion (alive) composited on a polished 4K scene.
10 shots from multiple expressions: SVD motion -> key -> R-ESRGAN -> composite over
animated dark-teal bg + blue particles + glow -> gentle camera -> concat + music.
Local / free. 4K30, libx264 veryslow CRF12.
"""
import os, math, base64, subprocess, wave
import numpy as np, cv2, torch, requests
from PIL import Image
from diffusers import StableVideoDiffusionPipeline
from scipy.signal import butter, lfilter

EXPR = r"E:\pd-media\assets\characters\pino\expressions"
OUT  = r"C:\Users\aab15\Documents\prime-documentary\_demo\pino"
WORK = os.path.join(OUT, "svd60_work")
API  = "http://127.0.0.1:7860/sdapi/v1/extra-single-image"
os.makedirs(WORK, exist_ok=True)
W, H, FPS, SHOT = 3840, 2160, 30, 6.0
CX, CY = W/2, H*0.60
rng = np.random.default_rng(21)

SHOTS = [("neutral_v001.png",5),("waving_v001.png",7),("happy_v002.png",3),
         ("talking_v001.png",11),("talking_v001.png",19),("idea_v003.png",4),
         ("pointing_v001.png",8),("thinking_v002.png",2),("happy_v003.png",6),
         ("waving_v002.png",13)]
MB = 115

def key(bgr):
    lum=(0.114*bgr[:,:,0]+0.587*bgr[:,:,1]+0.299*bgr[:,:,2])/255.0
    a=np.clip((lum-0.10)/0.35,0,1); a=a*a*(3-2*a); a=cv2.GaussianBlur(a,(0,0),2.0)
    return a

def svd_input(fn):
    bgr=cv2.imread(os.path.join(EXPR,fn)).astype(np.float32); a=key(bgr)
    ys,xs=np.where(a>0.25); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
    crop=bgr[y0:y1,x0:x1]; ca=a[y0:y1,x0:x1]
    CW,CH=1024,576; th=int(CH*0.80); sc=th/(y1-y0); tw=int((x1-x0)*sc)
    crop=cv2.resize(crop,(tw,th)); ca=cv2.resize(ca,(tw,th))[...,None]
    canvas=np.zeros((CH,CW,3),np.float32); canvas[:,:,0]=40;canvas[:,:,1]=28;canvas[:,:,2]=12
    ox,oy=(CW-tw)//2,(CH-th)//2
    canvas[oy:oy+th,ox:ox+tw]=canvas[oy:oy+th,ox:ox+tw]*(1-ca)+crop*ca
    return Image.fromarray(cv2.cvtColor(np.clip(canvas,0,255).astype(np.uint8),cv2.COLOR_BGR2RGB))

# ---- phase A: SVD generate ----
print("[A] SVD generate 10 shots",flush=True)
pipe=StableVideoDiffusionPipeline.from_pretrained(
  "stabilityai/stable-video-diffusion-img2vid-xt",torch_dtype=torch.float16,variant="fp16")
pipe.enable_model_cpu_offload()
for s,(fn,seed) in enumerate(SHOTS):
    img=svd_input(fn); frames=[]; cur=img
    for c in range(2):
        out=pipe(cur,decode_chunk_size=8,motion_bucket_id=MB,noise_aug_strength=0.02,
                 num_frames=25,generator=torch.manual_seed(seed+c)).frames[0]
        frames+=out if c==0 else out[1:]; cur=out[-1]
    rd=os.path.join(WORK,f"raw{s}"); os.makedirs(rd,exist_ok=True)
    for f in os.listdir(rd): os.remove(os.path.join(rd,f))
    for j,fr in enumerate(frames): fr.save(os.path.join(rd,f"r{j:03d}.png"))
    print(f"  shot{s} {len(frames)}f",flush=True)
del pipe; torch.cuda.empty_cache()

# ---- shared bg / particles / glow ----
yyc=np.linspace(0,1,H)[:,None].repeat(W,1)
bg0=np.zeros((H,W,3),np.float32); bg0[:,:,0]=44-22*yyc;bg0[:,:,1]=31-15*yyc;bg0[:,:,2]=13-7*yyc
bg0+=rng.uniform(-1.3,1.3,(H,W,1))
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
rr=np.sqrt(((xx-CX)/(W*0.62))**2+((yy-CY)/(H*0.62))**2)
vig=np.clip(1-0.5*np.clip(rr-0.42,0,1)**2,0,1)[...,None]
GS=int(W*0.42)|1; gk=cv2.getGaussianKernel(GS,GS*0.17).astype(np.float32); gk=gk@gk.T; gk/=gk.max()
GLOW=np.stack([gk*255,gk*150,gk*42],2)
NP=140; ppx=rng.uniform(0,W,NP);ppy=rng.uniform(0,H,NP);psp=rng.uniform(14,46,NP)
prad=rng.uniform(3,12,NP);pph=rng.uniform(0,6.28,NP)
def dot(r):
    s=int(r*6)|1; g=cv2.getGaussianKernel(s,r).astype(np.float32);k=g@g.T;return k/k.max()
DOTS={r:dot(r) for r in range(3,15)}
def add(dst,rgb,x,y,g):
    h,w=rgb.shape[:2]; x0,y0=max(0,x),max(0,y);x1,y1=min(W,x+w),min(H,y+h)
    if x1<=x0 or y1<=y0:return
    sx,sy=x0-x,y0-y; dst[y0:y1,x0:x1]+=rgb[sy:sy+(y1-y0),sx:sx+(x1-x0)]*g
def over(dst,rgb,a,x,y):
    h,w=rgb.shape[:2]; x0,y0=max(0,x),max(0,y);x1,y1=min(W,x+w),min(H,y+h)
    if x1<=x0 or y1<=y0:return
    sx,sy=x0-x,y0-y; r=rgb[sy:sy+(y1-y0),sx:sx+(x1-x0)];al=a[sy:sy+(y1-y0),sx:sx+(x1-x0)][...,None]
    dst[y0:y1,x0:x1]=dst[y0:y1,x0:x1]*(1-al)+r*al
def resrgan(bgr):
    ok,buf=cv2.imencode(".png",bgr)
    r=requests.post(API,json={"image":base64.b64encode(buf).decode(),"upscaling_resize":4,
        "upscaler_1":"R-ESRGAN 4x+","upscaler_2":"None"},timeout=240)
    return cv2.imdecode(np.frombuffer(base64.b64decode(r.json()["image"]),np.uint8),cv2.IMREAD_COLOR)

# ---- phase B: composite + encode each shot ----
print("[B] composite + encode",flush=True)
vf="[0:v]minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1:scd=none[v]"
shot_mp4s=[]
for s in range(len(SHOTS)):
    rd=os.path.join(WORK,f"raw{s}"); fd=os.path.join(WORK,f"fin{s}");os.makedirs(fd,exist_ok=True)
    for f in os.listdir(fd):os.remove(os.path.join(fd,f))
    raws=sorted(os.listdir(rd)); n=len(raws)
    for i,rf in enumerate(raws):
        big=resrgan(cv2.imread(os.path.join(rd,rf)))          # ~4096x2304
        a=key(big.astype(np.float32))
        ys,xs=np.where(a>0.25); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
        pino=big[y0:y1,x0:x1].astype(np.float32); pa=a[y0:y1,x0:x1]
        th=int(H*0.62); sc=th/(y1-y0); tw=int((x1-x0)*sc)
        pino=cv2.resize(pino,(tw,th)); pa=cv2.resize(pa,(tw,th))
        t=i/max(1,n-1)
        fx=CX+90*math.sin(2*math.pi*0.12*t+s)+ (s-4.5)*12
        fy=CY+22*math.sin(2*math.pi*0.25*t)
        frame=bg0.copy()
        add(frame,GLOW,int(fx-GS/2),int(fy-th*0.5-GS/2+th*0.5),0.12)
        over(frame,pino,pa,int(fx-tw/2),int(fy-th))
        for j in range(NP):
            y=(ppy[j]-psp[j]*(i/FPS+s*SHOT))%(H+120)-60; x=ppx[j]+22*math.sin(0.5*(i/FPS)+pph[j])
            r=max(3,min(14,int(prad[j])));k=DOTS[r]
            amp=(0.5+0.5*math.sin(1.3*(i/FPS)+pph[j]))*0.55
            add(frame,np.stack([k*255,k*150,k*40],2),int(x-k.shape[1]/2),int(y-k.shape[0]/2),amp)
        frame=np.clip(frame,0,255)*vig
        cv2.imwrite(os.path.join(fd,f"f{i:03d}.png"),np.clip(frame,0,255).astype(np.uint8))
    in_fps=n/SHOT
    mp4=os.path.join(WORK,f"shot{s}.mp4")
    subprocess.run(["ffmpeg","-y","-framerate",f"{in_fps:.4f}","-i",os.path.join(fd,"f%03d.png"),
      "-filter_complex",vf,"-map","[v]","-c:v","libx264","-preset","veryslow","-crf","12",
      "-pix_fmt","yuv420p","-r","30",mp4],check=True)
    shot_mp4s.append(mp4); print(f"  shot{s} encoded",flush=True)

# ---- phase C: audio ----
print("[C] audio",flush=True)
SR=44100;DUR=SHOT*len(SHOTS);n=int(SR*DUR);tt=np.linspace(0,DUR,n)
def eseg(a,b,al,rl):
    e=np.ones(b-a);fa=int(SR*al);fr=int(SR*rl);e[:fa]*=np.linspace(0,1,fa);e[-fr:]*=np.linspace(1,0,fr);return e
prog=[[261.63,329.63,392.0,493.88],[220.0,261.63,329.63,392.0],[174.61,261.63,349.23,440.0],[196.0,246.94,392.0,587.33]]
pad=np.zeros(n);seg=n//10
for k in range(10):
    ch=prog[k%4];a=k*seg;b=min(n,(k+1)*seg);t=tt[a:b]
    pad[a:b]+=sum(np.sin(2*math.pi*fz*t) for fz in ch)/len(ch)*eseg(a,b,0.5,0.5)
pad*=0.18
bells=np.zeros(n)
for j in range(int(DUR/1.5)):
    st=int((j*1.5+0.7)%DUR*SR);fz=523.25*(1+(j%4)*0.16);L=int(SR*0.5)
    if st+L<n: bells[st:st+L]+=np.sin(2*math.pi*fz*np.linspace(0,0.5,L))*np.exp(-np.linspace(0,7,L))*0.1
low=lfilter(*butter(2,120/(SR/2),btype='low'),np.cumsum(rng.standard_normal(n)));low/=(np.max(np.abs(low))+1e-9);low*=0.12
amb=pad+bells+low;fd=np.ones(n);fl=int(SR*1.0);fd[:fl]*=np.linspace(0,1,fl);fd[-fl:]*=np.linspace(1,0,fl)
amb*=fd;amb=amb/(np.max(np.abs(amb))+1e-9)*0.7
wavp=os.path.join(WORK,"audio.wav")
with wave.open(wavp,"wb") as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
    w.writeframes((np.stack([amb,amb],1)*32767).astype(np.int16).tobytes())

# ---- phase D: concat + mux ----
print("[D] concat",flush=True)
listf=os.path.join(WORK,"list.txt")
with open(listf,"w") as f:
    for m in shot_mp4s: f.write(f"file '{m}'\n")
joined=os.path.join(WORK,"joined.mp4")
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",listf,"-c","copy",joined],check=True)
final=os.path.join(r"C:\Users\aab15\Documents\prime-documentary\_demo","pino_60s_FINAL.mp4")
subprocess.run(["ffmpeg","-y","-i",joined,"-i",wavp,"-map","0:v","-map","1:a",
                "-c:v","copy","-c:a","aac","-b:a","320k","-shortest",final],check=True)
print("DONE ->",final,flush=True)
