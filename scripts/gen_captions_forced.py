#!/usr/bin/env python3
r"""Frame-accurate captions via forced alignment (faster-whisper word timestamps) — 0004 §E3.

Fixes QC-0007 / the owner's note (captions broke at odd points + drifted): transcribe the narration
master with WORD timestamps, align those times to the exact script words (voice_plan, in order, per
chunk window from timing), then re-segment into clean 5-8 word lines that break at sentence/clause
punctuation. Text stays the scripted narration; timing comes from when each word is actually spoken.
    py -3.11 scripts/gen_captions_forced.py            -> 08_edit/captions.v002.srt
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-002-gideon"
VOICE_PLAN = ROOT / "episodes" / EP / "06_audio" / "voice_plan.v001.json"
TIMING = ROOT / "episodes" / EP / "08_edit" / "timing.v001.json"
OUT = ROOT / "episodes" / EP / "08_edit" / "captions.v002.srt"
MAX_WORDS, MAX_CHARS = 8, 44


def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())


def srt_ts(t):
    h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int(round((t-int(t))*1000))
    if ms==1000: s+=1; ms=0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def transcribe(master):
    from faster_whisper import WhisperModel
    print("loading faster-whisper small.en (cpu/int8)...")
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(str(master), word_timestamps=True, vad_filter=False,
                               beam_size=5, language="en")
    words = []
    for s in segs:
        for w in (s.words or []):
            words.append({"w": w.word.strip(), "n": norm(w.word), "start": w.start, "end": w.end})
    print(f"  whisper words: {len(words)}")
    return words


def split_lines(tokens):
    """tokens: list of original-text words (with punctuation). -> list of (line_str, idx_start, idx_end)."""
    lines=[]; cur=[]; cs=0
    for i,w in enumerate(tokens):
        trial=" ".join([t for t,_ in cur]+[w]) if cur else w
        if cur and (len(cur)>=MAX_WORDS or len(trial)>MAX_CHARS):
            lines.append(([t for t,_ in cur], cur[0][1], cur[-1][1])); cur=[]
        cur.append((w,i))
        # break at strong punctuation (sentence) or em-dash; soft-break at comma if line already long
        if re.search(r"[.?!—]$", w) or (w.endswith(",") and len(cur)>=5):
            lines.append(([t for t,_ in cur], cur[0][1], cur[-1][1])); cur=[]
    if cur: lines.append(([t for t,_ in cur], cur[0][1], cur[-1][1]))
    return [(" ".join(ws), a, b) for ws,a,b in lines]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    vp=json.loads(VOICE_PLAN.read_text("utf-8")); tm=json.loads(TIMING.read_text("utf-8"))
    master = Path(json.loads((ROOT/"config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])/"episodes"/EP/"06_voice"/"master"/"vc_master_v001.mp3"
    words = transcribe(master)
    starts = {s["chunk_id"]: s for s in tm["scenes"]}
    wi = 0  # pointer into whisper words (global, advances per chunk)
    entries=[]; idx=1
    for c in vp["chunks"]:
        cid=c["chunk_id"]; seg=starts.get(cid)
        if not seg: continue
        wstart, wend = seg["start"], seg["end"]
        # whisper words whose center is in this chunk window
        cw=[w for w in words if wstart-0.2 <= (w["start"]+w["end"])/2 <= wend+0.2]
        toks=c["spoken_text"].replace("—","—").split()
        # align script tokens to chunk whisper words by sequential normalized match
        times=[None]*len(toks); j=0
        for ti,tk in enumerate(toks):
            tn=norm(tk)
            if not tn: continue
            # search a small window ahead in cw for a matching normalized token
            k=j; found=None
            while k < min(j+4, len(cw)):
                if cw[k]["n"]==tn or cw[k]["n"].startswith(tn[:4] or "~"):
                    found=k; break
                k+=1
            if found is not None:
                times[ti]=(cw[found]["start"], cw[found]["end"]); j=found+1
            elif j < len(cw):
                times[ti]=(cw[j]["start"], cw[j]["end"]); j+=1
        # fill gaps by interpolation within the chunk window
        for ti in range(len(toks)):
            if times[ti] is None:
                frac=(ti+0.5)/len(toks); t=wstart+frac*(wend-wstart); times[ti]=(t,t+0.3)
        # segment into clean lines, time each line by its first/last token
        for line, a, b in split_lines(toks):
            s=times[a][0]; e=times[b][1]
            if e<=s: e=s+0.6
            entries.append((idx, s, e, line)); idx+=1
    # enforce monotonic, no overlap
    fixed=[]
    for i,(n,s,e,ln) in enumerate(entries):
        if fixed and s < fixed[-1][2]: s=fixed[-1][2]+0.001
        if e<=s: e=s+0.5
        fixed.append((n,s,e,ln))
    OUT.write_text("\n".join(f"{n}\n{srt_ts(s)} --> {srt_ts(e)}\n{ln}\n" for n,s,e,ln in fixed), "utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(fixed)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
