#!/usr/bin/env python3
"""Slow EP2 narration (atempo) and derive the master timeline: per-scene timing + SRT captions.

EP1 method (owner): uniformly slow the narration, then conform captions/images/assets to that
timing. Steps:
  1. atempo-slow each VC-*.mp3 -> 06_voice/slowed/
  2. concat (with a small inter-scene pad) -> 06_voice/master/vc_master_v001.mp3
  3. write timing.v001.json (each scene start/end/dur on the master timeline)
  4. write captions.v001.srt (word-for-word narration, line-split, timed from real slowed durations)

Output is the single timing source the Remotion assembly + caption burn-in conform to.
Usage: py -3.11 scripts/slow_and_time_gideon.py [--atempo 0.84] [--pad 0.25]
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-002-gideon"
VOICE_PLAN = ROOT/"episodes"/EP/"06_audio"/"voice_plan.v001.json"

def media_root() -> Path:
    cfg = json.loads((ROOT/"config/storage.local.json").read_text(encoding="utf-8"))
    return Path(cfg["roots"]["media"]["path"])

def dur(p: Path) -> float:
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],
                       capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except Exception: return 0.0

def srt_ts(t: float) -> str:
    h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int(round((t-int(t))*1000))
    if ms==1000: s+=1; ms=0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def split_lines(text: str, max_words=8, max_chars=46):
    # sentence-aware greedy packing into <=max_words / <=max_chars caption lines
    words = text.replace("—","-").split()
    lines=[]; cur=[]
    for w in words:
        trial = " ".join(cur+[w])
        if cur and (len(cur)>=max_words or len(trial)>max_chars):
            lines.append(" ".join(cur)); cur=[w]
        else:
            cur.append(w)
        if w.endswith((".","?","!")) and len(" ".join(cur))>=18:
            lines.append(" ".join(cur)); cur=[]
    if cur: lines.append(" ".join(cur))
    return lines

def main(argv)->int:
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    ap=argparse.ArgumentParser(); ap.add_argument("--atempo",type=float,default=0.84); ap.add_argument("--pad",type=float,default=0.25)
    a=ap.parse_args(argv)

    vp=json.loads(VOICE_PLAN.read_text(encoding="utf-8")); chunks=vp["chunks"]
    mr=media_root(); draft=mr/"episodes"/EP/"06_voice"/"draft"
    slowed=mr/"episodes"/EP/"06_voice"/"slowed"; slowed.mkdir(parents=True,exist_ok=True)
    master_dir=mr/"episodes"/EP/"06_voice"/"master"; master_dir.mkdir(parents=True,exist_ok=True)

    # 1. slow each chunk
    parts=[]
    for c in chunks:
        cid=c["chunk_id"]; src=draft/f"{cid}.mp3"
        if not src.exists(): print(f"MISSING {src}"); return 1
        out=slowed/f"{cid}.mp3"
        subprocess.run(["ffmpeg","-y","-i",str(src),"-filter:a",f"atempo={a.atempo}","-c:a","libmp3lame","-q:a","2",str(out)],
                       capture_output=True)
        parts.append((c, out, dur(out)))

    # 2. build a silence pad + concat list
    pad=slowed/"_pad.mp3"
    subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-t",str(a.pad),"-c:a","libmp3lame","-q:a","2",str(pad)],
                   capture_output=True)
    listf=slowed/"_concat.txt"
    lines=[]
    for i,(c,out,d) in enumerate(parts):
        lines.append(f"file '{out.as_posix()}'")
        if i<len(parts)-1: lines.append(f"file '{pad.as_posix()}'")
    listf.write_text("\n".join(lines)+"\n", encoding="utf-8")
    master=master_dir/"vc_master_v001.mp3"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listf),"-c:a","libmp3lame","-q:a","2",str(master)],
                   capture_output=True)

    # 3. timing map + 4. SRT (timed from real slowed durations)
    timing=[]; srt=[]; t=0.0; idx=1
    for i,(c,out,d) in enumerate(parts):
        start=t; end=t+d
        timing.append({"scene_id":c.get("scene_id"),"chunk_id":c["chunk_id"],"section":c.get("section"),
                       "delivery":c.get("delivery"),"start":round(start,3),"end":round(end,3),"dur":round(d,3)})
        # captions across [start,end] proportional to characters
        clines=split_lines(c["spoken_text"])
        tot=sum(len(x) for x in clines) or 1
        ct=start
        for ln in clines:
            seg=d*(len(ln)/tot)
            srt.append((idx, ct, ct+seg, ln)); idx+=1; ct+=seg
        t=end+(a.pad if i<len(parts)-1 else 0.0)

    total=round(t,3)
    tj=ROOT/"episodes"/EP/"08_edit"; tj.mkdir(parents=True,exist_ok=True)
    (tj/"timing.v001.json").write_text(json.dumps({"episode_id":EP,"atempo":a.atempo,"pad_sec":a.pad,
        "master":"artifact://episodes/"+EP+"/06_voice/master/vc_master_v001.mp3",
        "total_seconds":total,"scenes":timing}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

    srt_txt=[]
    for n,s,e,ln in srt:
        srt_txt.append(f"{n}\n{srt_ts(s)} --> {srt_ts(e)}\n{ln}\n")
    (tj/"captions.v001.srt").write_text("\n".join(srt_txt), encoding="utf-8")

    print(f"atempo={a.atempo} pad={a.pad}s")
    print(f"master -> 06_voice/master/vc_master_v001.mp3  ({total:.1f}s = {int(total//60)}:{int(total%60):02d})")
    print(f"timing -> 08_edit/timing.v001.json   captions -> 08_edit/captions.v001.srt ({len(srt)} lines)")
    return 0

if __name__=="__main__":
    raise SystemExit(main(sys.argv[1:]))
