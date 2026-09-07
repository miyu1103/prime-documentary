"""Assemble completed Wan i2v frame-dirs into 1920x1080 mp4 motion clips for the pool.
Idempotent: skips already-assembled. Run repeatedly as i2v progresses."""
import subprocess, glob, os
from pathlib import Path
FF=r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
SRC_DIRS=glob.glob(r"C:/Users/aab15/ae-demo/wan_frames_cp_*")
OUT=Path(r"E:/pd-media/assets/ai_video/centralpark/motion2"); OUT.mkdir(parents=True,exist_ok=True)
PUB=Path(r"C:/Users/aab15/Documents/prime-documentary/remotion/public/centralpark/motion2"); PUB.mkdir(parents=True,exist_ok=True)
made=skip=0
for d in SRC_DIRS:
    name=os.path.basename(d).replace("wan_frames_","")  # cp_P05
    frames=sorted(glob.glob(os.path.join(d,"*.png")))
    if len(frames)<40: continue
    outp=OUT/f"{name}.mp4"
    if outp.exists() and outp.stat().st_size>100000: skip+=1; continue
    # frames -> 24fps 1080p mp4 (81 frames ~3.4s)
    pat=os.path.join(d, os.path.basename(frames[0]).replace("00001","%05d").replace("_00001_","_%05d_"))
    # robust: use glob concat via a temp list
    import tempfile
    lst=tempfile.NamedTemporaryFile("w",suffix=".txt",delete=False,dir=str(OUT))
    for f in frames: lst.write(f"file '{f}'\n"); 
    lst.write("")  # ensure flush
    lst.close()
    cmd=[FF,"-y","-hide_banner","-loglevel","error","-r","24","-f","concat","-safe","0","-i",lst.name,
         "-vf","scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30",
         "-c:v","libx264","-crf","18","-pix_fmt","yuv420p",str(outp)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    os.unlink(lst.name)
    if outp.exists() and outp.stat().st_size>50000:
        import shutil; shutil.copy(outp,PUB/f"{name}.mp4"); made+=1
    else:
        print(f"FAIL {name}: {r.stderr[-160:]}",flush=True)
print(f"assembled={made} skipped={skip} (of {len(SRC_DIRS)} frame-dirs)")
