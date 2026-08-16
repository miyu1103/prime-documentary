#!/usr/bin/env python3
"""Watch the watcher. Runs from Windows Task Scheduler, so it survives a dead shell and a reboot.

2026-08-16. `_supervise_tonight.sh` restarts the i2v chain and starts the render queue, which
covers the failure that cost 08-14 to 08-16 -- a chain that finished correctly and left the next
step as a sentence in a log. But nothing restarted the supervisor itself, and a bash process is
exactly the thing that does not survive a reboot or a closed terminal. This is the layer under it.

It also answers the question the supervisor cannot: **is anything actually moving?** A queue that
is running and producing nothing reads as healthy to a liveness check. Progress is counted from
frame directories and master files on disk, compared against the previous run, and a stall is
written down as a stall.

It never starts two of anything: an unreadable process probe is treated as "running".

    py -3.11 scripts/pd_watchdog.py            # one pass, prints a line, updates state
    py -3.11 scripts/pd_watchdog.py --install  # register the Task Scheduler job (every 15 min)
    py -3.11 scripts/pd_watchdog.py --remove   # unregister it
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AE_DEMO = Path("C:/Users/aab15/ae-demo")
STATE = ROOT / "runs" / "watchdog_state.v001.json"
ALERT = ROOT / "runs" / "WATCHDOG_ALERT.txt"
LOG = ROOT / "runs" / "watchdog.log"
TASK = "PD-Watchdog"

# slug: how many i2v frame dirs mean that episode is converted
TARGETS = {"openfields": 53, "ramirez": 50, "pinto": 54, "hyatt": 32}
DISK_FLOOR_GB = 30          # the i2v run needs about 25; below this it will fail mid-clip
STALL_MINUTES = 90          # a Wan clip takes ~5 min and a render step far less


def running(pattern: str) -> bool:
    """True when a process matching `pattern` exists. Unreadable -> True, never double-launch.

    The probe excludes its own query text: on 2026-08-16 a probe of this shape matched the
    powershell running it and reported 1 process on a completely idle machine.
    """
    ps = (f"@(Get-CimInstance Win32_Process | Where-Object {{ $_.CommandLine -like '*{pattern}*' "
          f"-and $_.CommandLine -notlike '*Get-CimInstance*' }}).Count")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=60)
        return int((r.stdout or "").strip()) > 0
    except Exception:
        return True


def progress() -> dict:
    """Everything that counts as forward motion, measured on disk."""
    out = {f"i2v:{s}": len(list(AE_DEMO.glob(f"wan_frames_{s}_*"))) for s in TARGETS}
    for slug in TARGETS:
        masters = list((ROOT / "episodes").glob(f"PD-2026-0*-{slug}/08_edit/{slug}_final_bgm.v*.mp4"))
        out[f"master:{slug}"] = len(masters)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--install", action="store_true")
    ap.add_argument("--remove", action="store_true")
    a = ap.parse_args()

    if a.install or a.remove:
        if a.remove:
            subprocess.run(["schtasks", "/Delete", "/TN", TASK, "/F"], check=False)
            print(f"removed scheduled task {TASK}")
            return 0
        # `py -3.11` resolves through a WindowsApps alias that Task Scheduler cannot see: the
        # first registration ran and returned 0x80070002 (file not found). Use the launcher's
        # real path, and cd first so relative paths in this script resolve.
        py = Path.home() / "AppData/Local/Programs/Python/Launcher/py.exe"
        if not py.is_file():
            raise SystemExit(f"py launcher not at {py} -- find it before registering the task")
        cmd = f'cmd /c cd /d "{ROOT}" && "{py}" -3.11 scripts\\pd_watchdog.py'
        subprocess.run(["schtasks", "/Create", "/TN", TASK, "/TR", cmd, "/SC", "MINUTE",
                        "/MO", "15", "/F", "/RL", "LIMITED"], check=True)
        print(f"registered {TASK}: every 15 minutes. Remove with --remove.")
        return 0

    now = datetime.now(timezone.utc)
    prev = json.loads(STATE.read_text(encoding="utf-8")) if STATE.is_file() else {}
    cur = progress()
    i2v_done = all(cur[f"i2v:{s}"] >= t for s, t in TARGETS.items())
    free_gb = shutil.disk_usage(ROOT.anchor).free / 1024**3
    notes: list[str] = []

    # 1. the supervisor must exist while there is anything left to supervise
    sup = running("_supervise_tonight")
    if not sup and not i2v_done:
        subprocess.Popen(["bash", "scripts/_supervise_tonight.sh"], cwd=str(ROOT),
                         stdout=open(ROOT / "out_supervisor_0816.log", "ab"),
                         stderr=subprocess.STDOUT)
        notes.append("supervisor was DEAD with i2v work remaining -- relaunched")

    # 2. disk: the i2v run needs headroom it cannot get back mid-clip
    if free_gb < DISK_FLOOR_GB:
        notes.append(f"DISK {free_gb:.1f} GB free, below the {DISK_FLOOR_GB} GB floor")

    # 3. is anything actually moving? liveness is not progress.
    changed = cur != prev.get("progress")
    if changed:
        last_move = now.isoformat()
    else:
        last_move = prev.get("last_move") or now.isoformat()
        idle_min = (now - datetime.fromisoformat(last_move)).total_seconds() / 60
        busy = running("_chain_i2v") or running("queue_unattended") or running("remotion")
        if busy and idle_min > STALL_MINUTES and not i2v_done:
            notes.append(f"STALLED: a job is running but nothing has advanced for "
                         f"{idle_min:.0f} min (last change {last_move})")

    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"checked": now.isoformat(), "progress": cur,
                                 "last_move": last_move, "free_gb": round(free_gb, 1),
                                 "i2v_done": i2v_done, "notes": notes}, indent=1) + "\n",
                     encoding="utf-8")
    line = (f"{now.strftime('%m-%d %H:%M')} free={free_gb:.0f}GB i2v_done={i2v_done} "
            f"sup={sup} " + " ".join(f"{k}={v}" for k, v in cur.items() if k.startswith("i2v"))
            + ("  || " + " || ".join(notes) if notes else ""))
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line)

    if notes:
        ALERT.write_text(f"{now.isoformat()}\n" + "\n".join(notes) + "\n", encoding="utf-8")
    elif ALERT.is_file():
        ALERT.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
