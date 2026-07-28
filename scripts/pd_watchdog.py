"""PD WATCHDOG -- kills the silent-stall failure mode (root cause #3): a GPU job
that is 'running' but produces nothing (ComfyUI hung, GPU idle) and nobody notices
until the owner asks. Watches an output dir's file count + GPU utilisation; if there
is NO new output for --stall-min minutes AND the GPU is idle, it force-restarts
ComfyUI (so a robust chain's ensure_comfy relaunches the job) and writes an ALERT.

  py -3.11 scripts/pd_watchdog.py --glob "C:/Users/aab15/ae-demo/wan_frames_cp_P*" \
       --target 76 --stall-min 8 --alert out_WATCHDOG_ALERT.log
Run alongside a long i2v/gen job. Exits when target reached or after --max-min.
"""
import sys, time, glob, argparse, subprocess, urllib.request

COMFY="http://127.0.0.1:8188"
def gpu_util():
    try:
        o=subprocess.run(["nvidia-smi","--query-gpu=utilization.gpu","--format=csv,noheader,nounits"],
                         capture_output=True,text=True,timeout=15)
        return int(o.stdout.strip().splitlines()[0])
    except Exception: return -1
def comfy_up():
    try: urllib.request.urlopen(COMFY+"/system_stats",timeout=6); return True
    except Exception: return False
def kill_comfy():
    try:
        o=subprocess.run(["netstat","-ano"],capture_output=True,text=True,timeout=15)
        for ln in o.stdout.splitlines():
            if ":8188" in ln and "LISTENING" in ln:
                pid=ln.split()[-1]
                subprocess.run(["taskkill","/F","/PID",pid],capture_output=True,timeout=15)
                return pid
    except Exception: pass
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--glob",required=True); ap.add_argument("--target",type=int,default=0)
    ap.add_argument("--stall-min",type=float,default=8.0); ap.add_argument("--max-min",type=float,default=720)
    ap.add_argument("--poll",type=int,default=60); ap.add_argument("--alert",default="out_WATCHDOG_ALERT.log")
    a=ap.parse_args()
    t0=time.time(); last_n=len(glob.glob(a.glob)); last_change=time.time(); restarts=0
    def log(m):
        line=f"[watchdog] {m}"
        print(line,flush=True)
        try: open(a.alert,"a",encoding="utf-8").write(line+"\n")
        except Exception: pass
    log(f"start glob={a.glob} target={a.target} stall={a.stall_min}min start_n={last_n}")
    while (time.time()-t0) < a.max_min*60:
        time.sleep(a.poll)
        n=len(glob.glob(a.glob)); g=gpu_util()
        if a.target and n>=a.target: log(f"TARGET reached n={n} -- watchdog exit"); return
        if n>last_n: last_n=n; last_change=time.time(); continue
        stalled_s=time.time()-last_change
        if stalled_s >= a.stall_min*60 and (g<10 or not comfy_up()):
            restarts+=1
            log(f"STALL DETECTED: n={n} unchanged {int(stalled_s)}s, gpu={g}%, comfy_up={comfy_up()} -> RESTART #{restarts} ComfyUI")
            pid=kill_comfy()
            log(f"killed comfy pid={pid}; robust chain's ensure_comfy will relaunch. (if no chain, restart job manually)")
            last_change=time.time()  # give it time to recover
    log("watchdog max-min reached, exiting")

if __name__=="__main__":
    main()
