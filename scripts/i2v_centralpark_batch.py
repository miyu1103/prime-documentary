"""EP50 rebuild: i2v the people (P) + diverse scenes (V) into REAL MOTION via Wan (comfy_wan.py).
Output frames -> ComfyUI output; then assembled to mp4. Subtle, natural, documentary motion."""
import subprocess, sys, glob, os, time
from pathlib import Path
DRIVER=r"C:/Users/aab15/ae-demo/comfy_wan.py"
AI=Path("H:/pd-media/assets/ai/centralpark")
# motion prompt per prefix type
def mprompt(name):
    if name.startswith("P"):
        return ("subtle natural human motion, the person breathes and shifts slightly, tiny head movement, "
                "living cinematic documentary shot, camera very slowly pushes in, shallow depth of field")
    return ("subtle cinematic camera motion, slow push-in or drift, atmospheric living environment, "
            "gentle light flicker, documentary footage, no morphing")
imgs=sorted(glob.glob(str(AI/"P*.png")))+sorted(glob.glob(str(AI/"V*.png")))
only=sys.argv[1] if len(sys.argv)>1 else None
if only: imgs=[x for x in imgs if only in x]
# I2V_MAX: do at most N NON-SKIPPED clips then exit, so the driving chain can
# restart ComfyUI FRESH between chunks (Wan leaks VRAM -> hard crash ~every 20-30
# clips). Chunking + fresh comfy per chunk = no leak-crash. Default: all.
I2V_MAX=int(os.environ.get("I2V_MAX","0")) or None
print(f"i2v batch: {len(imgs)} images"+(f" (max {I2V_MAX}/run)" if I2V_MAX else ""), flush=True)
done=0
for i,img in enumerate(imgs):
    name=Path(img).stem
    # frames are collected by comfy_wan into ae-demo/wan_frames_cp_<name>/ (this is what the
    # assembler reads). The skip-check MUST look here -- checking ComfyUI/output/wanout/cp_<name>
    # (a dir that never exists; frames are flat files) made the batch NEVER skip => every restart
    # re-generated all done clips from P01. Fixed 2026-07-28.
    outdir=Path(r"C:/Users/aab15/ae-demo")/f"wan_frames_cp_{name}"
    # skip if already produced frames
    if outdir.exists() and len(list(outdir.glob("*.png")))>=40:
        print(f"skip {name}",flush=True); continue
    cmd=["py","-3.11",DRIVER,"--image",img,"--prompt",mprompt(name),"--prefix",f"cp_{name}",
         "--w","1280","--h","704","--length","81","--steps","30","--shift","8.0","--cfg","5.0","--seed",str(1000+i)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    ok="prompt_id" in (r.stdout+r.stderr)
    done+=1
    print(f"[{done}/{len(imgs)}] {name} {'ok' if ok else 'FAIL: '+(r.stdout+r.stderr)[-200:]}",flush=True)
    if I2V_MAX and done>=I2V_MAX:
        print(f"CHUNK done ({done}) -- exiting so chain can restart ComfyUI fresh",flush=True); break
print(f"DONE queued {done}",flush=True)
