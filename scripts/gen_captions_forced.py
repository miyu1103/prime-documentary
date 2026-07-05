#!/usr/bin/env python3
r"""Frame-accurate captions via forced alignment (faster-whisper word timestamps) — 0004 §E3.

Fixes QC-0007 / the owner's #1/#2 recurring failure (captions broke at odd points + drifted, and
did not match the narration): transcribe the narration master with WORD timestamps, align those
times to the exact SPOKEN words, then re-segment into clean 5-8 word lines that break at
sentence/clause punctuation. Text stays the verbatim narration; timing comes from when each word is
actually spoken.

Text source (the "字幕=ナレ一致" fix):
  - GENERAL episodes: the VERBATIM narration_index (prefer 06_audio/narration_index.v002.json, else
    v001) chunk `text` — explicitly NOT the condensed 03_script script.annotated visual layer
    (deriving captions from the annotated layer is the documented desync trap).
  - LEGACY fallback (e.g. PD-2026-002-gideon, whose narration_index has no `text` field): the
    06_audio/voice_plan.v001.json `spoken_text`, aligned inside 08_edit/timing.v001.json chunk
    windows. This path is preserved byte-for-byte so existing episodes are unaffected.

Usage:
  py -3.11 scripts/gen_captions_forced.py                         # default ep = PD-2026-002-gideon
  py -3.11 scripts/gen_captions_forced.py --ep PD-2026-032-carsearch
  py -3.11 scripts/gen_captions_forced.py --ep PD-2026-032-carsearch --dry-run   # segment only, no audio
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-002-gideon"
MAX_WORDS, MAX_CHARS = 8, 44  # ~7-8 words / ~42-44 chars per caption line


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


def glue_punct(tokens):
    """General-path token prep: glue a pure-punctuation token (e.g. a lone em-dash, whose norm() is
    empty) onto the previous word so captions never show a standalone '—' line. norm() ignores
    non-alphanumerics, so this does NOT change the word-for-word 字幕=ナレ QC. The legacy path does
    not use this (gideon's shipped captions intentionally keep lone-dash lines)."""
    out = []
    for t in tokens:
        if out and not norm(t):
            out[-1] = out[-1] + " " + t
        else:
            out.append(t)
    return out


def split_lines(tokens):
    """tokens: list of original-text words (with punctuation). -> list of (line_str, idx_start, idx_end).

    Breath-unit / clause segmentation: break on strong sentence punctuation (. ? !), em-dash, and
    soft-break on commas once the line is already long; also hard-cap at MAX_WORDS / MAX_CHARS so no
    line runs past ~7-8 words / ~44 chars. Never breaks mid-phrase (a break only lands after a token).
    idx_start/idx_end are indices into `tokens`.
    """
    lines=[]; cur=[]
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


# ---------------------------------------------------------------------------
# text-source resolution (verbatim narration, never the annotated visual layer)
# ---------------------------------------------------------------------------

def resolve_text_source(ep_dir):
    """Return (chunks, source_label). chunks = [{"id": str, "text": str}, ...] in spoken order.

    Preference order (per the 字幕=ナレ rule):
      1. 06_audio/narration_index.v002.json chunk `text` (verbatim spoken narration)
      2. 06_audio/narration_index.v001.json chunk `text`
      3. 06_audio/voice_plan.v001.json `spoken_text` (LEGACY fallback; used when the narration_index
         carries no `text`, e.g. PD-2026-002-gideon).
    """
    for name in ("narration_index.v002.json", "narration_index.v001.json"):
        p = ep_dir / "06_audio" / name
        if not p.exists():
            continue
        data = json.loads(p.read_text("utf-8"))
        chunks = []
        for c in data.get("chunks", []):
            cid = c.get("voice_chunk_id") or c.get("chunk_id")
            txt = c.get("text")
            if txt and txt.strip():
                chunks.append({"id": cid, "text": txt.strip()})
        if chunks:
            return chunks, name
    vp = ep_dir / "06_audio" / "voice_plan.v001.json"
    if vp.exists():
        data = json.loads(vp.read_text("utf-8"))
        chunks = [{"id": c["chunk_id"], "text": c["spoken_text"]}
                  for c in data.get("chunks", []) if c.get("spoken_text")]
        if chunks:
            return chunks, "voice_plan.v001.json"
    raise SystemExit(f"no caption text source found under {ep_dir/'06_audio'} "
                     f"(need narration_index.v002/v001 with `text`, or voice_plan.v001.json)")


def resolve_master(slug, override):
    if override:
        return Path(override)
    media_root = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))
                      ["roots"]["media"]["path"])
    master_dir = media_root / "episodes" / slug / "06_voice" / "master"
    # prefer the long-form full-episode master vc_master_v*.mp3 (highest version)
    cands = sorted(master_dir.glob("vc_master_v*.mp3"))
    if cands:
        return cands[-1]
    return master_dir / "vc_master_v001.mp3"


# ---------------------------------------------------------------------------
# alignment QC — the "字幕=ナレ一致" gate
# ---------------------------------------------------------------------------

def alignment_qc(caption_lines, chunks):
    """caption_lines: list of line strings. chunks: text-source chunks.

    (1) Verify the concatenated caption text equals the verbatim narration text word-for-word
        (normalized). (2) Flag any line over the char/word cap. Returns True iff both pass.
    """
    cap_words = [norm(w) for ln in caption_lines for w in ln.split() if norm(w)]
    nar_words = [norm(w) for c in chunks for w in c["text"].split() if norm(w)]
    ok = True
    if cap_words == nar_words:
        print(f"  QC 字幕=ナレ一致: PASS  ({len(cap_words)} words match verbatim narration)")
    else:
        ok = False
        # locate first divergence for a loud, actionable message
        n = min(len(cap_words), len(nar_words)); d = next((i for i in range(n)
              if cap_words[i] != nar_words[i]), n)
        ctx_c = " ".join(cap_words[max(0, d-4):d+4]); ctx_n = " ".join(nar_words[max(0, d-4):d+4])
        print("  !! QC 字幕=ナレ一致: FAIL — caption text diverged from the narration_index verbatim text")
        print(f"     caption words={len(cap_words)}  narration words={len(nar_words)}  first diff @ word {d}")
        print(f"     caption : ...{ctx_c}...")
        print(f"     narration: ...{ctx_n}...")
    # count spoken words only (ignore glued trailing punctuation like '—', consistent with norm())
    def wc_of(ln): return sum(1 for w in ln.split() if norm(w))
    over = [(i+1, wc_of(ln), len(ln), ln) for i, ln in enumerate(caption_lines)
            if wc_of(ln) > MAX_WORDS or len(ln) > MAX_CHARS]
    if over:
        ok = False
        print(f"  !! QC line-cap: {len(over)} line(s) exceed {MAX_WORDS} words / {MAX_CHARS} chars:")
        for ln_no, wc, cc, ln in over[:20]:
            print(f"     line {ln_no}: {wc}w {cc}c  {ln!r}")
    else:
        print(f"  QC line-cap: PASS  (all lines <= {MAX_WORDS} words / {MAX_CHARS} chars)")
    return ok


# ---------------------------------------------------------------------------
# legacy alignment (voice_plan + timing windows) — preserved byte-for-byte
# ---------------------------------------------------------------------------

def align_legacy(ep_dir, chunks, master):
    """Original per-chunk-window algorithm (timing.v001.json). Returns list of (start, end, line)."""
    tm = json.loads((ep_dir / "08_edit" / "timing.v001.json").read_text("utf-8"))
    words = transcribe(master)
    starts = {s["chunk_id"]: s for s in tm["scenes"]}
    out = []
    for c in chunks:
        cid = c["id"]; seg = starts.get(cid)
        if not seg:
            continue
        wstart, wend = seg["start"], seg["end"]
        cw = [w for w in words if wstart-0.2 <= (w["start"]+w["end"])/2 <= wend+0.2]
        toks = c["text"].replace("—", "—").split()
        times = [None]*len(toks); j = 0
        for ti, tk in enumerate(toks):
            tn = norm(tk)
            if not tn:
                continue
            k = j; found = None
            while k < min(j+4, len(cw)):
                if cw[k]["n"] == tn or cw[k]["n"].startswith(tn[:4] or "~"):
                    found = k; break
                k += 1
            if found is not None:
                times[ti] = (cw[found]["start"], cw[found]["end"]); j = found+1
            elif j < len(cw):
                times[ti] = (cw[j]["start"], cw[j]["end"]); j += 1
        for ti in range(len(toks)):
            if times[ti] is None:
                frac = (ti+0.5)/len(toks); t = wstart+frac*(wend-wstart); times[ti] = (t, t+0.3)
        for line, a, b in split_lines(toks):
            s = times[a][0]; e = times[b][1]
            if e <= s:
                e = s+0.6
            out.append((s, e, line))
    return out


# ---------------------------------------------------------------------------
# general alignment (narration_index, no timing file): global sequential match
# ---------------------------------------------------------------------------

def align_general(chunks, master):
    """Flatten all chunk tokens in spoken order, align globally against the whisper word stream,
    interpolate gaps between anchors, then segment each chunk. Returns list of (start, end, line)."""
    words = transcribe(master)
    total = words[-1]["end"] if words else 0.0
    # flat token list with chunk membership
    chunk_toks = [glue_punct(c["text"].split()) for c in chunks]
    flat = [tk for toks in chunk_toks for tk in toks]
    times = [None]*len(flat); j = 0
    for ti, tk in enumerate(flat):
        tn = norm(tk)
        if not tn:
            continue
        k = j; found = None
        while k < min(j+6, len(words)):
            wn = words[k]["n"]
            if wn == tn or (len(tn) >= 4 and wn.startswith(tn[:4])) or (len(wn) >= 4 and tn.startswith(wn[:4])):
                found = k; break
            k += 1
        if found is not None:
            times[ti] = (words[found]["start"], words[found]["end"]); j = found+1
        elif j < len(words):
            times[ti] = (words[j]["start"], words[j]["end"]); j += 1
    # fill None runs by linear interpolation between known anchors
    anchors = [i for i, t in enumerate(times) if t is not None]
    if not anchors:
        for i in range(len(flat)):
            t = (i/len(flat))*total; times[i] = (t, t+0.3)
    else:
        first, last = anchors[0], anchors[-1]
        for i in range(first):
            t = (i/max(first, 1))*times[first][0]; times[i] = (t, t)
        for a, b in zip(anchors, anchors[1:]):
            if b-a <= 1:
                continue
            sa = times[a][1]; sb = times[b][0]
            for i in range(a+1, b):
                f = (i-a)/(b-a); t = sa+f*(sb-sa); times[i] = (t, t)
        tail = times[last][1]
        for i in range(last+1, len(flat)):
            f = (i-last)/max(len(flat)-last, 1); t = tail+f*max(total-tail, 0.0); times[i] = (t, t+0.3)
    # segment per chunk, mapping local token indices to the flat/global index
    out = []; base = 0
    for toks in chunk_toks:
        for line, a, b in split_lines(toks):
            s = times[base+a][0]; e = times[base+b][1]
            if e <= s:
                e = s+0.6
            out.append((s, e, line))
        base += len(toks)
    return out


def segment_only(chunks):
    """--dry-run: split the text source into caption lines with no audio. Returns list of line strings."""
    return [line for c in chunks for line, _a, _b in split_lines(glue_punct(c["text"].split()))]


def write_srt(out_path, entries):
    """entries: list of (start, end, line). Enforce monotonic, non-overlapping times; write SRT."""
    fixed = []
    for s, e, ln in entries:
        if fixed and s < fixed[-1][1]:
            s = fixed[-1][1]+0.001
        if e <= s:
            e = s+0.5
        fixed.append((s, e, ln))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(f"{i+1}\n{srt_ts(s)} --> {srt_ts(e)}\n{ln}\n"
                                  for i, (s, e, ln) in enumerate(fixed)), "utf-8")
    return fixed


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Forced-alignment captions from verbatim narration.")
    ap.add_argument("--ep", default=DEFAULT_EP, help=f"episode slug (default {DEFAULT_EP})")
    ap.add_argument("--master", default=None, help="override narration master audio path")
    ap.add_argument("--out", default=None, help="override output SRT path")
    ap.add_argument("--dry-run", action="store_true",
                    help="segment the narration_index into caption lines only; no audio / no whisper")
    args = ap.parse_args()

    slug = args.ep
    ep_dir = ROOT / "episodes" / slug
    if not ep_dir.exists():
        raise SystemExit(f"episode dir not found: {ep_dir}")
    chunks, source = resolve_text_source(ep_dir)
    out_path = Path(args.out) if args.out else ep_dir / "08_edit" / "captions.v002.srt"
    nwords = sum(len(c["text"].split()) for c in chunks)
    print(f"ep={slug}  text-source={source}  chunks={len(chunks)}  words={nwords}")

    # segment (used for the dry-run preview and for the QC text-equality check)
    lines = segment_only(chunks)

    if args.dry_run:
        print(f"[dry-run] would produce {len(lines)} caption lines (segment-only, no audio)")
        alignment_qc(lines, chunks)
        print("first 15 caption lines:")
        for i, ln in enumerate(lines[:15], 1):
            print(f"  {i:>2}: {ln}")
        return 0

    # full run: align verbatim narration words to the rendered master audio
    master = resolve_master(slug, args.master)
    if not master.exists():
        raise SystemExit(f"master audio not found: {master}\n"
                         f"(use --dry-run to preview segmentation before narration exists, "
                         f"or pass --master <path>)")
    legacy = (source == "voice_plan.v001.json") and (ep_dir / "08_edit" / "timing.v001.json").exists()
    entries = align_legacy(ep_dir, chunks, master) if legacy else align_general(chunks, master)
    fixed = write_srt(out_path, entries)
    print(f"wrote {out_path.relative_to(ROOT) if out_path.is_relative_to(ROOT) else out_path}  "
          f"({len(fixed)} lines)  [{'legacy timing-window' if legacy else 'global'} alignment]")
    alignment_qc([ln for _s, _e, ln in fixed], chunks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
