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
    fixed=[]
    for (n,s,e,ln) in entries:
        if fixed and s < fixed[-1][2]: s=fixed[-1][2]+0.001
        if e<=s: e=s+0.5
        fixed.append((n,s,e,ln))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(f"{n}\n{srt_ts(s)} --> {srt_ts(e)}\n{ln}\n" for n,s,e,ln in fixed), "utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(fixed)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
