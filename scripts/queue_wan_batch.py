"""Queue the remaining EP38 Wan hero cuts to ComfyUI, then poll until the queue drains.
Reports per-shot output frame counts. Read-mostly (queues via the driver, then polls)."""
from __future__ import annotations
import json, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
DRIVER = ROOT / "scripts" / "comfy_wan_kidsforcash.py"
COMFY = "http://127.0.0.1:8188"
# S07 already done; queue the other 11 hero cuts.
SHOTS = ["S03", "S05", "S08", "S10", "S12", "S14", "S16", "S22", "S23", "S29", "S37"]


def get(path: str):
    with urllib.request.urlopen(COMFY + path, timeout=15) as r:
        return json.loads(r.read())


def main() -> int:
    t0 = time.time()
    pids: dict[str, str] = {}
    for sid in SHOTS:
        r = subprocess.run(["py", "-3.11", str(DRIVER), "--run", "--shot", sid],
                           capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        pid = ""
        for line in out.splitlines():
            if "prompt_id=" in line:
                pid = line.split("prompt_id=", 1)[1].split(" ", 1)[0].strip()
        if pid:
            pids[sid] = pid
            print(f"[batch] queued {sid} prompt_id={pid}", flush=True)
        else:
            print(f"[batch] FAILED to queue {sid}:\n{out[-400:]}", flush=True)
        time.sleep(1)
    print(f"[batch] {len(pids)}/{len(SHOTS)} queued. polling until drained ...", flush=True)

    last = ""
    while True:
        try:
            q = get("/queue")
            run = len(q.get("queue_running", []))
            pend = len(q.get("queue_pending", []))
        except Exception:
            run, pend = -1, -1
        msg = f"running={run} pending={pend} t={(time.time()-t0)/60:.1f}min"
        if msg != last:
            print(f"[batch] {msg}", flush=True); last = msg
        if run == 0 and pend == 0:
            break
        time.sleep(30)

    print(f"[batch] queue drained at {(time.time()-t0)/60:.1f}min. collecting results ...", flush=True)
    ok = 0
    for sid, pid in pids.items():
        try:
            h = get(f"/history/{pid}")
            outs = h.get(pid, {}).get("outputs", {})
            n = sum(len(nd.get("images", []) or []) for nd in outs.values())
            st = h.get(pid, {}).get("status", {}).get("status_str", "?")
            print(f"[batch] {sid}: {n} frames status={st}", flush=True)
            if n >= 40:
                ok += 1
        except Exception as e:
            print(f"[batch] {sid}: history error {e}", flush=True)
    print(f"[batch] DONE {ok}/{len(pids)} shots produced >=40 frames. total {(time.time()-t0)/60:.1f}min", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
