"""Quick test: does SVD give Pino believable, NON-broken organic life?"""
import os, numpy as np, cv2, torch, subprocess
from PIL import Image
from diffusers import StableVideoDiffusionPipeline

SRC = r"E:\pd-media\assets\characters\pino\expressions\neutral_v001.png"
OUT = r"C:\Users\aab15\Documents\prime-documentary\_demo\pino"
FR  = os.path.join(OUT, "svd_test_frames")
os.makedirs(FR, exist_ok=True)
for f in os.listdir(FR): os.remove(os.path.join(FR, f))

# build 1024x576 landscape input: Pino keyed, centered on dark-teal canvas
bgr = cv2.imread(SRC).astype(np.float32)
lum=(0.114*bgr[:,:,0]+0.587*bgr[:,:,1]+0.299*bgr[:,:,2])/255.0
a=np.clip((lum-0.10)/0.35,0,1); a=a*a*(3-2*a)
ys,xs=np.where(a>0.25); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
crop=bgr[y0:y1,x0:x1]; ca=a[y0:y1,x0:x1]
CW,CH=1024,576
th=int(CH*0.78); sc=th/(y1-y0); tw=int((x1-x0)*sc)
crop=cv2.resize(crop,(tw,th)); ca=cv2.resize(ca,(tw,th))[...,None]
canvas=np.zeros((CH,CW,3),np.float32)
canvas[:,:,0]=40; canvas[:,:,1]=28; canvas[:,:,2]=12
ox,oy=(CW-tw)//2,(CH-th)//2
canvas[oy:oy+th,ox:ox+tw]=canvas[oy:oy+th,ox:ox+tw]*(1-ca)+crop*ca
inp=np.clip(canvas,0,255).astype(np.uint8)
cv2.imwrite(os.path.join(OUT,"_svd_input.png"),inp)
img=Image.fromarray(cv2.cvtColor(inp,cv2.COLOR_BGR2RGB))

pipe=StableVideoDiffusionPipeline.from_pretrained(
  "stabilityai/stable-video-diffusion-img2vid-xt",torch_dtype=torch.float16,variant="fp16")
pipe.enable_model_cpu_offload()
frames=pipe(img,decode_chunk_size=8,motion_bucket_id=127,noise_aug_strength=0.02,
            num_frames=25,generator=torch.manual_seed(5)).frames[0]
for i,fr in enumerate(frames): fr.save(os.path.join(FR,f"s{i:03d}.png"))
print("frames",len(frames),flush=True)

# strip of 6
idx=[0,4,8,12,16,24]
strip=np.hstack([cv2.resize(cv2.cvtColor(np.array(frames[k]),cv2.COLOR_RGB2BGR),(320,180)) for k in idx])
cv2.imwrite(os.path.join(OUT,"_svd_test_strip.png"),strip)
# quick mp4
mp4=os.path.join(r"C:\Users\aab15\Documents\prime-documentary\_demo","pino_svd_test.mp4")
subprocess.run(["ffmpeg","-y","-framerate","7","-i",os.path.join(FR,"s%03d.png"),
  "-vf","minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc,scale=1280:720:flags=lanczos",
  "-c:v","libx264","-crf","16","-pix_fmt","yuv420p",mp4],check=True)
print("DONE",mp4,flush=True)
