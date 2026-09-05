#!/usr/bin/env python3
r"""Frame-accurate captions for any PD case episode via forced alignment (generic --ep).

Same logic as gen_captions_kyllo.py, parameterized by episode. Transcribes the narration
master with faster-whisper word timestamps, aligns to the scripted words per narration
chunk, re-segments into clean cues, enforces <=27 cps (merge/extend, small overlap) and
<=2 wrapped lines (<=50 chars). Output: <ep>/08_edit/captions.final.v001.srt

    py -3.11 scripts/gen_captions_case.py --ep PD-2026-026-katz
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_WORDS, MAX_CHARS = 7, 42
STOP = {"a","an","the","of","to","in","on","at","by","for","from","into","with","as","than",
        "and","or","but","nor","so","yet","is","are","was","were","be","been","being","am",
        "his","her","its","their","my","your","our","this","that","these","those","it","he",
        "she","we","they","you","i","not","no","if","then","when","where","which","who","up"}


def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())


def srt_ts(t):
    h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int(round((t-int(t))*1000))
    if ms==1000: s+=1; ms=0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def transcribe(master, cache):
    if cache.exists():
        print(f"  cached whisper: {cache.name}")
        return json.loads(cache.read_text("utf-8"))
    from faster_whisper import WhisperModel
    print("loading faster-whisper small.en (cpu/int8)...")
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(str(master), word_timestamps=True, vad_filter=False, beam_size=5, language="en")
    words=[]
    for s in segs:
        for w in (s.words or []):
            words.append({"w": w.word.strip(), "n": norm(w.word), "start": w.start, "end": w.end})
    print(f"  whisper words: {len(words)}")
    cache.parent.mkdir(parents=True, exist_ok=True); cache.write_text(json.dumps(words), "utf-8")
    return words


def split_lines(tokens):
    lines=[]; cur=[]
    def flush(seq):
        if seq: lines.append(([t for t,_ in seq], seq[0][1], seq[-1][1]))
    def flush_sentence_end(seq):
        # A 1-2 word sentence tail becomes an orphan cue ("the specification.") and
        # check_caption_breaks rejects any such cue. Borrow words back from the
        # previously flushed line so the tail reads as a phrase (2026-08-25).
        if len(seq)<3 and lines:
            ptoks=[(t,i) for t,i in zip(lines[-1][0], range(lines[-1][1], lines[-1][2]+1))]
            combined=ptoks+seq
            if 3<len(combined)<=2*MAX_WORDS:
                # head=combined[:cut+1], tail=combined[cut+1:], so the tail gets 3 words
                # only when cut = len-4 (len-3 recreated the 2-word tail it was fixing).
                cut=len(combined)-4
                while cut>0 and norm(combined[cut][0]) in STOP: cut-=1
                if cut>0:
                    lines.pop()
                    flush(combined[:cut+1]); flush(combined[cut+1:])
                    return
        flush(seq)
    for i,w in enumerate(tokens):
        cur.append((w,i)); wl=len(" ".join(t for t,_ in cur))
        if re.search(r"[.?!—:;]$", w):
            flush_sentence_end(cur); cur=[]; continue
        if w.endswith(",") and len(cur)>=4:
            flush(cur); cur=[]; continue
        if len(cur)>=MAX_WORDS or wl>=MAX_CHARS:
            cut=len(cur)-1
            while cut>0 and norm(cur[cut][0]) in STOP: cut-=1
            if cut<=0: cut=len(cur)-1
            head=cur[:cut+1]; cur=cur[cut+1:]; flush(head)
    flush(cur)
    return [(re.sub(r"\s+([.,;:?!])", r"\1", " ".join(ws)), a, b) for ws,a,b in lines]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap=argparse.ArgumentParser(); ap.add_argument("--ep", required=True); args=ap.parse_args()
    ep=args.ep
    INDEX=ROOT/"episodes"/ep/"06_audio"/"narration_index.v001.json"
    OUT=ROOT/"episodes"/ep/"08_edit"/"captions.final.v001.srt"
    CACHE=OUT.parent/"_whisper_words.v001.json"
    media=Path(json.loads((ROOT/"config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
    master=media/"episodes"/ep/"06_voice"/"master"/"vc_master_v001.mp3"
    idx=json.loads(INDEX.read_text("utf-8"))
    words=transcribe(master, CACHE)
    entries=[]; i=1
    for c in idx["chunks"]:
        wstart, wend = c["start"], c["end"]
        cw=[w for w in words if wstart-0.2 <= (w["start"]+w["end"])/2 <= wend+0.2]
        # EP77 (2026-08-25): the v3 scripts cite inline -- "The lane opens. <!-- KB-004 -->" --
        # and those chunks reach the index verbatim. The voice never speaks them (verified:
        # zero KB- hits in the whisper transcript) but this aligner was writing them into the
        # srt: 103 citation comments in EP77's first captions.final.v001.srt.
        toks=re.sub(r"<!--.*?-->", " ", c["spoken_text"]).split(); times=[None]*len(toks); j=0
        for ti,tk in enumerate(toks):
            tn=norm(tk)
            if not tn: continue
            k=j; found=None
            while k < min(j+4, len(cw)):
                if cw[k]["n"]==tn or (len(tn)>=4 and cw[k]["n"].startswith(tn[:4])): found=k; break
                k+=1
            if found is not None: times[ti]=(cw[found]["start"], cw[found]["end"]); j=found+1
            elif j < len(cw): times[ti]=(cw[j]["start"], cw[j]["end"]); j+=1
        for ti in range(len(toks)):
            if times[ti] is None:
                frac=(ti+0.5)/max(len(toks),1); t=wstart+frac*(wend-wstart); times[ti]=(t,t+0.3)
        for line,a,b in split_lines(toks):
            s=times[a][0]; e=times[b][1]
            if e<=s: e=s+0.6
            entries.append((i,s,e,line)); i+=1
    cues=[]
    for (n,s,e,ln) in entries:
        if cues and s < cues[-1][1]: s=cues[-1][1]+0.001
        if e<=s: e=s+0.5
        cues.append([s,e,ln])
    for k in range(len(cues)):
        s,e,t=cues[k]; need=max(0.9, len(t)/19.0)
        limit=(cues[k+1][0]-0.03) if k+1<len(cues) else e+need
        cues[k][1]=min(max(e, s+need), max(e, limit))
    out=[]; k=0
    while k<len(cues):
        s,e,t=cues[k]; cps=len(t)/max(e-s,0.001)
        if cps>22 and k+1<len(cues) and len(t)+len(cues[k+1][2])+1 <= 92:
            ns,ne,nt=cues[k+1]; cues[k+1]=[s,ne,(t+" "+nt).strip()]; k+=1; continue
        out.append([s,e,t]); k+=1
    # orphan merge (2026-08-25): check_caption_breaks rejects any cue under 3 words that does
    # not both end a sentence and start uppercase -- a two-word tail like "wants it." alone on
    # screen. Fold such cues back into the cue they grammatically belong to.
    merged=[]
    for s,e,t in out:
        ws=re.findall(r"[A-Za-z0-9'’]+", t)
        if merged and len(ws)<3 and (not t or t[-1] not in ".?!—-:;" or not t[0].isupper()) \
           and len(merged[-1][2])+len(t)+1<=92:
            merged[-1][1]=e; merged[-1][2]=(merged[-1][2]+" "+t).strip()
        else:
            merged.append([s,e,t])
    out=merged
    for k in range(len(out)):
        s,e,t=out[k]; need=len(t)/24.0
        if e-s<need:
            cap=(out[k+1][0]+0.9) if k+1<len(out) else s+need
            out[k][1]=min(s+need, cap)
    def wrap2(t, maxc=44):
        # Grammar-aware since 2026-08-25: the old midpoint split ended line 1 on function
        # words ("...the bridge was in the" / "river") and check_caption_breaks rejects
        # exactly that. Prefer the split nearest the midpoint whose first line does NOT end
        # on a no-dangle word; fall back to the plain midpoint only if none qualifies.
        if len(t)<=maxc: return t
        from fix_caption_dangling import NO_DANGLE_END as _ND
        words2=t.split(); half=len(t)/2
        kk=next((k for k in range(1,len(words2)) if len(" ".join(words2[:k]))>=half), None)
        if kk is None: return t
        best=None
        for z in sorted(range(1,len(words2)), key=lambda z: abs(z-kk)):
            aa=" ".join(words2[:z]); bb=" ".join(words2[z:])
            if len(aa)<=50 and len(bb)<=50:
                if norm(words2[z-1]) not in _ND:
                    return aa+"\n"+bb
                if best is None: best=aa+"\n"+bb
        return best or t
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(f"{k+1}\n{srt_ts(s)} --> {srt_ts(e)}\n{wrap2(t)}\n" for k,(s,e,t) in enumerate(out)), "utf-8")
    worst=max((len(t)/max(e-s,0.001) for s,e,t in out), default=0)
    print(f"[{ep}] wrote {OUT.relative_to(ROOT)}  ({len(out)} lines, worst {worst:.0f}cps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
