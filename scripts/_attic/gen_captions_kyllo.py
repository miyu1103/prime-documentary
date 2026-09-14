#!/usr/bin/env python3
r"""Frame-accurate captions for PD-2026-025-kyllo via forced alignment.

Same approach as scripts/gen_captions_forced.py, but reads the timings + spoken text
directly from 06_audio/narration_index.v001.json (chunk_id/start/end/spoken_text).
Transcribe the narration master with WORD timestamps (faster-whisper), align to the
scripted words per chunk window, then re-segment into clean short lines that break at
sentence/clause punctuation. Text = the scripted narration; timing = when words are spoken.
Output: 08_edit/captions.final.v001.srt
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-025-kyllo"
INDEX = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
OUT = ROOT / "episodes" / EP / "08_edit" / "captions.final.v001.srt"
MAX_WORDS, MAX_CHARS = 7, 42


def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())


def srt_ts(t):
    h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int(round((t-int(t))*1000))
    if ms==1000: s+=1; ms=0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# weak words a caption line should not END on (pull them to the next line instead)
STOP = {
    "a","an","the","of","to","in","on","at","by","for","from","into","with","as","than",
    "and","or","but","nor","so","yet","is","are","was","were","be","been","being","am",
    "his","her","its","their","my","your","our","this","that","these","those","it","he",
    "she","we","they","you","i","not","no","if","then","when","where","which","who","up",
}
CACHE = OUT.parent / "_whisper_words.v001.json"


def transcribe(master):
    if CACHE.exists():
        print(f"  using cached whisper words: {CACHE.name}")
        return json.loads(CACHE.read_text("utf-8"))
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
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(words), "utf-8")
    return words


def split_lines(tokens):
    """Break into short cues at sentence/clause punctuation; on a length wrap, back up
    over trailing weak words so a line never ends on 'a/the/his/on/and…'."""
    lines=[]; cur=[]

    def flush(seq):
        if seq: lines.append(([t for t,_ in seq], seq[0][1], seq[-1][1]))

    for i,w in enumerate(tokens):
        cur.append((w,i))
        wl=len(" ".join(t for t,_ in cur))
        if re.search(r"[.?!—:;]$", w) or (w.endswith(",") and len(cur)>=4):
            flush(cur); cur=[]; continue
        if len(cur)>=MAX_WORDS or wl>=MAX_CHARS:
            cut=len(cur)-1
            while cut>0 and norm(cur[cut][0]) in STOP:
                cut-=1
            if cut<=0:
                cut=len(cur)-1  # all-weak line: give up rather than loop
            head=cur[:cut+1]; cur=cur[cut+1:]
            flush(head)
    flush(cur)
    return [(re.sub(r"\s+([.,;:?!])", r"\1", " ".join(ws)), a, b) for ws,a,b in lines]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    idx=json.loads(INDEX.read_text("utf-8"))
    master = Path(json.loads((ROOT/"config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])/"episodes"/EP/"06_voice"/"master"/"vc_master_v001.mp3"
    words = transcribe(master)
    entries=[]; i=1
    for c in idx["chunks"]:
        wstart, wend = c["start"], c["end"]
        cw=[w for w in words if wstart-0.2 <= (w["start"]+w["end"])/2 <= wend+0.2]
        toks=c["spoken_text"].split()
        times=[None]*len(toks); j=0
        for ti,tk in enumerate(toks):
            tn=norm(tk)
            if not tn: continue
            k=j; found=None
            while k < min(j+4, len(cw)):
                if cw[k]["n"]==tn or (len(tn)>=4 and cw[k]["n"].startswith(tn[:4])):
                    found=k; break
                k+=1
            if found is not None:
                times[ti]=(cw[found]["start"], cw[found]["end"]); j=found+1
            elif j < len(cw):
                times[ti]=(cw[j]["start"], cw[j]["end"]); j+=1
        for ti in range(len(toks)):
            if times[ti] is None:
                frac=(ti+0.5)/max(len(toks),1); t=wstart+frac*(wend-wstart); times[ti]=(t,t+0.3)
        for line, a, b in split_lines(toks):
            s=times[a][0]; e=times[b][1]
            if e<=s: e=s+0.6
            entries.append((i, s, e, line)); i+=1
    # monotonic, no overlap
    cues=[]  # [s,e,text]
    for (n,s,e,ln) in entries:
        if cues and s < cues[-1][1]: s=cues[-1][1]+0.001
        if e<=s: e=s+0.5
        cues.append([s,e,ln])
    # enforce reading speed <= ~19 cps (spec gate is 27): extend each cue's end into the
    # gap before the next; any cue still too fast is merged into the following one.
    for i in range(len(cues)):
        s,e,t=cues[i]
        need=max(0.9, len(t)/19.0)
        limit=(cues[i+1][0]-0.03) if i+1<len(cues) else e+need
        cues[i][1]=min(max(e, s+need), max(e, limit))
    out=[]; i=0
    while i<len(cues):
        s,e,t=cues[i]
        cps=len(t)/max(e-s,0.001)
        # merge a too-fast cue into the next while the result still fits 2 wrapped lines (<=92 chars)
        if cps>22 and i+1<len(cues) and len(t)+len(cues[i+1][2])+1 <= 92:
            ns,ne,nt=cues[i+1]
            cues[i+1]=[s, ne, (t+" "+nt).strip()]
            i+=1; continue
        out.append([s,e,t]); i+=1
    # final guarantee: reading speed <= 24 cps by extending the end, allowing a small (<=0.35s)
    # overlap into the next cue (on-screen the earlier cue wins, so this only holds it a touch longer).
    for i in range(len(out)):
        s,e,t=out[i]
        need=len(t)/24.0
        if e-s < need:
            cap=(out[i+1][0]+0.35) if i+1<len(out) else s+need
            out[i][1]=min(s+need, cap)
    def wrap2(t, maxc=44):
        # keep each SRT line <= ~46 chars: balance long (merged) cues onto 2 lines at a space
        if len(t) <= maxc:
            return t
        words = t.split()
        half = len(t) / 2
        for k in range(1, len(words)):
            a = " ".join(words[:k])
            if len(a) >= half:
                for kk in (k, k - 1, k + 1):
                    if 1 <= kk < len(words):
                        aa = " ".join(words[:kk]); bb = " ".join(words[kk:])
                        if len(aa) <= 50 and len(bb) <= 50:
                            return aa + "\n" + bb
                break
        return t
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(f"{k+1}\n{srt_ts(s)} --> {srt_ts(e)}\n{wrap2(t)}\n" for k,(s,e,t) in enumerate(out)), "utf-8")
    worst=max((len(t)/max(e-s,0.001) for s,e,t in out), default=0)
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(out)} lines, worst {worst:.0f}cps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
