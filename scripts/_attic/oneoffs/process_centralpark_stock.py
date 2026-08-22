"""EP50 rebuild: process usable free-stock clips into 1920x1080 ~3s cuts for the motion pool.
Curated (thematic, real motion, no green-screen/modern/illustrative)."""
import subprocess, glob, os
from pathlib import Path
FF=r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
SRC=sorted(glob.glob(r"E:/pd-media/assets/stock/video/*.mp4"))
OUT=Path(r"E:/pd-media/assets/ai_video/centralpark/stock"); OUT.mkdir(parents=True,exist_ok=True)
PUB=Path(r"C:/Users/aab15/Documents/prime-documentary/remotion/public/centralpark/stock"); PUB.mkdir(parents=True,exist_ok=True)
USABLE=[4,6,7,8,9,12,15,17,18,19,21,24,27,29,30,36,37,38,41,48,51,52,54,57,58,59,60,61,62,66,67,68,71,72]
made=0
for idx in USABLE:
    if idx>=len(SRC): continue
    src=SRC[idx]; name=f"ST{idx:02d}"
    outp=OUT/f"{name}.mp4"
    if outp.exists() and outp.stat().st_size>100000: made+=1; continue
    # take a 3s window starting at 1s, scale+crop to 1920x1080, mute, 30fps
    cmd=[FF,"-y","-hide_banner","-loglevel","error","-ss","1","-t","3.2","-i",src,
         "-vf","scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30",
         "-an","-c:v","libx264","-crf","18","-pix_fmt","yuv420p",str(outp)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if outp.exists() and outp.stat().st_size>50000:
        import shutil; shutil.copy(outp, PUB/f"{name}.mp4"); made+=1
        print(f"  {name} <- {os.path.basename(src)}",flush=True)
    else:
        print(f"  FAIL {name}: {r.stderr[-150:]}",flush=True)
print(f"DONE stock processed = {made}/{len(USABLE)}")
