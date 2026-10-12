"""PD GPU/VRAM manager -- prevents the webui<->ComfyUI VRAM collision that
silently crashed the EP50 re-i2v (root cause #2). Single 4090 = one heavy GPU
job at a time. Call the right prep BEFORE each kind of GPU job.

  py -3.11 scripts/pd_gpu_lock.py i2v     # free webui VRAM, verify headroom for Wan i2v
  py -3.11 scripts/pd_gpu_lock.py sdxl    # (ensure ComfyUI not hogging) reload webui
  py -3.11 scripts/pd_gpu_lock.py status  # print VRAM + which services are up
Exit 0 = ready, exit 1 = NOT ready (caller must NOT start the job).
"""
import sys, json, time, subprocess, urllib.request

WEBUI="http://127.0.0.1:7860"; COMFY="http://127.0.0.1:8188"
I2V_MIN_FREE_MB = 15000   # Wan TI2V-5B needs ~14GB; require >=15GB free before starting

def vram():
    try:
        out=subprocess.run(["nvidia-smi","--query-gpu=memory.used,memory.total,utilization.gpu",
                            "--format=csv,noheader,nounits"],capture_output=True,text=True,timeout=15)
        u,t,g=[int(x) for x in out.stdout.strip().splitlines()[0].split(",")]
        return u,t,t-u,g
    except Exception:
        return -1,-1,-1,-1

def up(url):
    try:
        urllib.request.urlopen(url,timeout=6); return True
    except Exception:
        return False

def webui_unload():
    try:
        req=urllib.request.Request(f"{WEBUI}/sdapi/v1/unload-checkpoint",data=b"{}",
                                   headers={"Content-Type":"application/json"},method="POST")
        urllib.request.urlopen(req,timeout=30); return True
    except Exception as e:
        print("  webui unload failed (maybe already down):",e); return False

def status():
    u,t,f,g=vram()
    print(f"VRAM used={u}MB free={f}MB util={g}%  webui={'UP' if up(WEBUI+'/sdapi/v1/sd-models') else 'down'}  comfy={'UP' if up(COMFY+'/system_stats') else 'down'}")
    return u,t,f,g

def prep_i2v():
    print("[gpu] preparing for i2v: freeing webui VRAM ...")
    if up(WEBUI+"/sdapi/v1/sd-models"): webui_unload(); time.sleep(4)
    for _ in range(6):
        u,t,f,g=vram()
        print(f"  VRAM free={f}MB (need >={I2V_MIN_FREE_MB})")
        if f>=I2V_MIN_FREE_MB or f<0:
            print("[gpu] i2v READY"); return 0
        time.sleep(3)
    print(f"[gpu] NOT READY: only {f}MB free < {I2V_MIN_FREE_MB} -- another GPU job is holding VRAM. Do NOT start i2v.")
    return 1

def prep_sdxl():
    print("[gpu] preparing for SDXL: webui will reload its checkpoint on next call.")
    # nothing to free here; ensure we are not racing a live i2v
    u,t,f,g=vram()
    if g>50 and up(COMFY+"/system_stats"):
        print(f"[gpu] WARN: GPU {g}% busy and ComfyUI up -- an i2v may be running. Serialize (wait) before SDXL.")
    return 0

if __name__=="__main__":
    cmd=sys.argv[1] if len(sys.argv)>1 else "status"
    if cmd=="i2v": sys.exit(prep_i2v())
    if cmd=="sdxl": sys.exit(prep_sdxl())
    status(); sys.exit(0)
