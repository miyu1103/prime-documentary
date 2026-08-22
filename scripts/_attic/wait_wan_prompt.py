"""Wait for a ComfyUI prompt to finish; report elapsed time + outputs. Read-only polling."""
from __future__ import annotations
import json, sys, time, urllib.request

COMFY = "http://127.0.0.1:8188"

def get(path: str):
    with urllib.request.urlopen(COMFY + path, timeout=15) as r:
        return json.loads(r.read())

def main(pid: str) -> int:
    t0 = time.time()
    print(f"[wait] polling prompt {pid} ...", flush=True)
    last = ""
    while True:
        try:
            hist = get(f"/history/{pid}")
        except Exception as e:
            hist = {}
        if pid in hist:
            elapsed = time.time() - t0
            outs = hist[pid].get("outputs", {})
            imgs = []
            for node_id, nd in outs.items():
                for im in nd.get("images", []) or []:
                    imgs.append(im.get("filename"))
            status = hist[pid].get("status", {})
            print(f"[wait] DONE prompt {pid}", flush=True)
            print(f"[wait] elapsed_since_watch_start = {elapsed:.0f}s ({elapsed/60:.1f} min)", flush=True)
            print(f"[wait] status = {status.get('status_str', status)}", flush=True)
            print(f"[wait] output images = {len(imgs)}", flush=True)
            if imgs:
                print(f"[wait] first/last = {imgs[0]} .. {imgs[-1]}", flush=True)
            return 0 if imgs else 3
        # still running/pending
        try:
            q = get("/queue")
            run = len(q.get("queue_running", []))
            pend = len(q.get("queue_pending", []))
            msg = f"running={run} pending={pend} t={time.time()-t0:.0f}s"
            if msg != last:
                print(f"[wait] {msg}", flush=True); last = msg
        except Exception:
            pass
        time.sleep(20)

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
