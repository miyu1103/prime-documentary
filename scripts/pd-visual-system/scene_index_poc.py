#!/usr/bin/env python
"""PD Visual System — P03 Asset Scene-Index PoC (PySceneDetect).

READ-ONLY on source media. Writes only a SQLite index (repo data/) and small
JPEG thumbnails (external approved write root H:/pd-media/previews/...).

Design goals (P03 acceptance):
- limit to 100-500 assets (never process all 85k)
- keep VFR info incl. PTS/time_base/avg vs r frame rate (via ffprobe)
- represent each cut with 3 frames at 25/50/75 %
- resumable: skip assets already 'done' with unchanged mtime/size
- error-continue: one bad file never aborts the run
- never move/delete/overwrite/re-encode source

Run with the ISOLATED venv:
  D:\\PD_AI_Tools\\PySceneDetect\\.venv\\Scripts\\python.exe \
    scripts/pd-visual-system/scene_index_poc.py --limit 150
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

import cv2  # from isolated venv (opencv-python)
from scenedetect import ContentDetector, SceneManager, open_video

VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi"}


def ffprobe_meta(path: str) -> dict:
    """Return VFR-aware metadata (PTS/time_base preserved) or {'error':...}."""
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries",
        "stream=codec_name,width,height,r_frame_rate,avg_frame_rate,"
        "time_base,start_pts,nb_frames,duration",
        "-show_entries", "format=duration",
        "-of", "json", path,
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        return {"error": f"ffprobe rc={out.returncode}: {out.stderr.strip()[:180]}"}
    data = json.loads(out.stdout or "{}")
    st = (data.get("streams") or [{}])[0]
    fmt = data.get("format") or {}

    def _rate(s):
        try:
            n, d = s.split("/")
            return round(float(n) / float(d), 4) if float(d) else None
        except Exception:
            return None

    r_fr = _rate(st.get("r_frame_rate", "0/0"))
    avg_fr = _rate(st.get("avg_frame_rate", "0/0"))
    dur = st.get("duration") or fmt.get("duration")
    return {
        "codec": st.get("codec_name"),
        "width": st.get("width"),
        "height": st.get("height"),
        "r_frame_rate": st.get("r_frame_rate"),
        "avg_frame_rate": st.get("avg_frame_rate"),
        "r_fps": r_fr,
        "avg_fps": avg_fr,
        "time_base": st.get("time_base"),
        "start_pts": st.get("start_pts"),
        "nb_frames": st.get("nb_frames"),
        "duration_sec": float(dur) if dur else None,
        # VFR heuristic: nominal (r) and average frame rate diverge
        "is_vfr": bool(r_fr and avg_fr and abs(r_fr - avg_fr) > 0.30),
    }


def detect_cuts(path: str, threshold: float):
    video = open_video(path)
    sm = SceneManager()
    sm.add_detector(ContentDetector(threshold=threshold))
    sm.auto_downscale = True  # speed: downscale big frames automatically
    sm.detect_scenes(video, show_progress=False)
    scenes = sm.get_scene_list()
    if not scenes:  # single continuous shot -> treat whole clip as one cut
        base = video.base_timecode
        scenes = [(base, video.duration)]
    return scenes


def grab_frame(cap, frame_no, out_path, width=360):
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, int(frame_no)))
    ok, frame = cap.read()
    if not ok or frame is None:
        return False
    h, w = frame.shape[:2]
    if w > width:
        frame = cv2.resize(frame, (width, int(h * width / w)))
    return bool(cv2.imwrite(out_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 82]))


def init_db(db_path: str) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    con.execute("""CREATE TABLE IF NOT EXISTS assets(
        asset_id TEXT PRIMARY KEY, path TEXT, size INTEGER, mtime REAL,
        codec TEXT, width INTEGER, height INTEGER,
        r_frame_rate TEXT, avg_frame_rate TEXT, r_fps REAL, avg_fps REAL,
        time_base TEXT, start_pts TEXT, nb_frames TEXT, duration_sec REAL,
        is_vfr INTEGER, n_cuts INTEGER, status TEXT, error TEXT,
        processed_at REAL, proc_sec REAL)""")
    con.execute("""CREATE TABLE IF NOT EXISTS cuts(
        cut_id TEXT PRIMARY KEY, asset_id TEXT, idx INTEGER,
        start_sec REAL, end_sec REAL, dur_sec REAL,
        start_frame INTEGER, end_frame INTEGER,
        thumb25 TEXT, thumb50 TEXT, thumb75 TEXT)""")
    con.commit()
    return con


def enumerate_assets(root: str, limit: int):
    found = []
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            if Path(f).suffix.lower() in VIDEO_EXTS:
                found.append(os.path.join(dp, f))
    found.sort()
    if len(found) <= limit:
        return found, len(found)
    # strided sample for folder variety, deterministic
    step = len(found) / limit
    return [found[int(i * step)] for i in range(limit)], len(found)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--media-root", default=r"H:\pd-media\assets")
    ap.add_argument("--limit", type=int, default=150)
    ap.add_argument("--threshold", type=float, default=27.0)
    ap.add_argument("--db", default=r"data\pd_vs_scene_index.sqlite")
    ap.add_argument("--thumbs-dir",
                    default=r"H:\pd-media\previews\pd-visual-system\scene_index")
    args = ap.parse_args()

    if args.limit > 500:
        print("REFUSE: --limit>500 (PoC is 100-500 only).", file=sys.stderr)
        return 2

    Path(args.db).parent.mkdir(parents=True, exist_ok=True)
    Path(args.thumbs_dir).mkdir(parents=True, exist_ok=True)
    con = init_db(args.db)

    assets, total = enumerate_assets(args.media_root, args.limit)
    print(f"media_root={args.media_root} total_videos={total} "
          f"sampled={len(assets)} limit={args.limit}")

    done = skipped = errored = 0
    t0 = time.time()
    for i, path in enumerate(assets, 1):
        asset_id = os.path.relpath(path, args.media_root).replace("\\", "/")
        try:
            stt = os.stat(path)
        except OSError as e:
            errored += 1
            con.execute("INSERT OR REPLACE INTO assets(asset_id,path,status,error,processed_at) "
                        "VALUES(?,?,?,?,?)", (asset_id, path, "error", f"stat:{e}", time.time()))
            con.commit()
            continue

        row = con.execute("SELECT status,size,mtime FROM assets WHERE asset_id=?",
                          (asset_id,)).fetchone()
        if row and row[0] == "done" and row[1] == stt.st_size and abs((row[2] or 0) - stt.st_mtime) < 1:
            skipped += 1
            continue  # resumable / diff-update: unchanged -> skip

        a_t0 = time.time()
        try:
            meta = ffprobe_meta(path)
            if "error" in meta:
                raise RuntimeError(meta["error"])
            cuts = detect_cuts(path, args.threshold)
            cap = cv2.VideoCapture(path)
            con.execute("DELETE FROM cuts WHERE asset_id=?", (asset_id,))
            adir = os.path.join(args.thumbs_dir, asset_id.replace("/", "__"))
            os.makedirs(adir, exist_ok=True)
            for idx, (s_tc, e_tc) in enumerate(cuts):
                sf, ef = s_tc.frame_num, e_tc.frame_num
                ss, es = s_tc.seconds, e_tc.seconds
                thumbs = []
                for pct in (0.25, 0.50, 0.75):
                    fno = sf + (ef - sf) * pct
                    tp = os.path.join(adir, f"cut{idx:03d}_{int(pct*100)}.jpg")
                    thumbs.append(tp if grab_frame(cap, fno, tp) else None)
                con.execute(
                    "INSERT OR REPLACE INTO cuts(cut_id,asset_id,idx,start_sec,end_sec,"
                    "dur_sec,start_frame,end_frame,thumb25,thumb50,thumb75) "
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (f"{asset_id}#c{idx:03d}", asset_id, idx, ss, es, es - ss,
                     sf, ef, thumbs[0], thumbs[1], thumbs[2]))
            cap.release()
            con.execute(
                "INSERT OR REPLACE INTO assets(asset_id,path,size,mtime,codec,width,height,"
                "r_frame_rate,avg_frame_rate,r_fps,avg_fps,time_base,start_pts,nb_frames,"
                "duration_sec,is_vfr,n_cuts,status,error,processed_at,proc_sec) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (asset_id, path, stt.st_size, stt.st_mtime, meta["codec"], meta["width"],
                 meta["height"], meta["r_frame_rate"], meta["avg_frame_rate"], meta["r_fps"],
                 meta["avg_fps"], meta["time_base"], str(meta["start_pts"]), str(meta["nb_frames"]),
                 meta["duration_sec"], int(meta["is_vfr"]), len(cuts), "done", None,
                 time.time(), time.time() - a_t0))
            con.commit()
            done += 1
        except Exception as e:  # error-continue
            errored += 1
            con.execute("INSERT OR REPLACE INTO assets(asset_id,path,size,mtime,status,error,processed_at) "
                        "VALUES(?,?,?,?,?,?,?)",
                        (asset_id, path, stt.st_size, stt.st_mtime, "error", f"{type(e).__name__}:{e}"[:200], time.time()))
            con.commit()
        if i % 20 == 0:
            print(f"  {i}/{len(assets)} done={done} skip={skipped} err={errored} "
                  f"elapsed={time.time()-t0:.1f}s")

    total_cuts = con.execute("SELECT COUNT(*) FROM cuts").fetchone()[0]
    vfr = con.execute("SELECT COUNT(*) FROM assets WHERE is_vfr=1").fetchone()[0]
    print(f"FINISHED done={done} skipped={skipped} errored={errored} "
          f"total_cuts={total_cuts} vfr_assets={vfr} wall={time.time()-t0:.1f}s")
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
