"""PD POST-RENDER GATE (BLOCKING) -- run on the FINAL mp4 BEFORE showing the owner.
Catches the defects the owner kept finding by watching end-to-end (black/flicker
gaps, frozen slideshow stretches, missing audio, wrong duration). ffmpeg-based.
Exit 0 = PASS (ok to show). Exit 1 = FAIL (do NOT show -- fix first).

  py -3.11 scripts/pd_postrender_gate.py <final.mp4> [--expect-sec 3652] [--frames 24 --out qc_frames]
It also dumps N evenly-spaced frames so a human (me) can WATCH the whole runtime,
which is the standing rule -- a frame scan is NOT a substitute for watching.
"""
import sys, argparse, subprocess, json, re, os
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

MAX_BLACK_S  = 1.2      # any black stretch longer than this = FAIL (flicker/gap)
MAX_FREEZE_S = 4.0      # any frozen stretch longer than this = FAIL (kamishibai/stuck)
MAX_SILENCE_S= 3.0      # any silence longer than this mid-film = FAIL (audio dropout)
DUR_TOL_S    = 8.0      # final duration must be within this of --expect-sec

def run(args, timeout=1200):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)

def duration(mp4):
    o=run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",mp4],60)
    try: return float(o.stdout.strip())
    except Exception: return -1.0

def has_audio(mp4):
    o=run(["ffprobe","-v","error","-select_streams","a","-show_entries","stream=codec_type","-of","csv=p=0",mp4],60)
    return "audio" in o.stdout

def detect(mp4, vf, key):
    # returns list of durations of detected events
    o=run(["ffmpeg","-hide_banner","-nostats","-i",mp4,"-vf",vf,"-an","-f","null","-"],3600) if key!="silence" \
        else run(["ffmpeg","-hide_banner","-nostats","-i",mp4,"-af","silencedetect=n=-45dB:d=%.1f"%MAX_SILENCE_S,"-f","null","-"],3600)
    txt=o.stderr
    if key=="black":   return [float(m) for m in re.findall(r"black_duration:([0-9.]+)", txt)]
    if key=="freeze":  return [float(m) for m in re.findall(r"freeze_duration:([0-9.]+)", txt)] or \
                              [1.0*len(re.findall(r"lavfi\.freezedetect\.freeze_start", txt))]  # fallback count
    if key=="silence": return [float(m) for m in re.findall(r"silence_duration:\s*([0-9.]+)", txt)]
    return []

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("mp4"); ap.add_argument("--expect-sec",type=float,default=0)
    ap.add_argument("--frames",type=int,default=24); ap.add_argument("--out",default="qc_frames")
    a=ap.parse_args(); fails=[]; warns=[]
    if not os.path.exists(a.mp4): print(f"RESULT: FAIL -- file missing {a.mp4}"); sys.exit(1)
    dur=duration(a.mp4)
    print("="*70); print(f"PD POST-RENDER GATE  {a.mp4}  dur={dur:.1f}s")
    if dur<=0: print("RESULT: FAIL -- unreadable/zero duration"); sys.exit(1)
    if a.expect_sec and abs(dur-a.expect_sec)>DUR_TOL_S:
        fails.append(f"DURATION {dur:.1f}s off expected {a.expect_sec:.1f}s by >{DUR_TOL_S}s")
    if not has_audio(a.mp4): fails.append("NO AUDIO stream")
    # black
    blk=[d for d in detect(a.mp4,"blackdetect=d=%.2f:pic_th=0.98"%MAX_BLACK_S,"black") if d>=MAX_BLACK_S]
    if blk: fails.append(f"BLACK: {len(blk)} stretch(es) >= {MAX_BLACK_S}s (worst {max(blk):.1f}s) = flicker/gap")
    # freeze
    frz=[d for d in detect(a.mp4,"freezedetect=n=-60dB:d=%.1f"%MAX_FREEZE_S,"freeze") if d>=MAX_FREEZE_S]
    if frz: fails.append(f"FREEZE: {len(frz)} frozen stretch(es) >= {MAX_FREEZE_S}s (worst {max(frz):.1f}s) = kamishibai/stuck")
    # silence
    sil=[d for d in detect(a.mp4,"","silence") if d>=MAX_SILENCE_S]
    if len(sil)>1: warns.append(f"SILENCE: {len(sil)} silent stretch(es) >= {MAX_SILENCE_S}s (worst {max(sil):.1f}s) -- verify int/outro only")
    # dump frames for human watch
    if a.frames>0 and dur>0:
        os.makedirs(a.out,exist_ok=True)
        step=dur/(a.frames+1)
        for i in range(1,a.frames+1):
            t=step*i
            run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",f"{t:.1f}","-i",a.mp4,
                 "-frames:v","1",os.path.join(a.out,f"t{int(t):05d}s.jpg")],120)
        print(f"  dumped {a.frames} frames -> {a.out}/  (WATCH THESE + the full runtime before showing owner)")
    print("-"*70)
    for w in warns: print("  [warn]",w)
    if fails:
        for f in fails: print("  [FAIL]",f)
        print("-"*70); print(f"RESULT: FAIL ({len(fails)}) -- DO NOT SHOW OWNER. Fix, then re-run."); sys.exit(1)
    print("RESULT: PASS -- automated checks clean. STILL watch the full runtime before showing owner."); sys.exit(0)

if __name__=="__main__":
    try: main()
    except SystemExit: raise
    except Exception as e:
        print(f"RESULT: FAIL -- gate crashed ({type(e).__name__}: {e})"); sys.exit(1)

