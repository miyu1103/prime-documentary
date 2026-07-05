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
# Reading-speed ceiling. The acceptance gate (scripts/check_final_acceptance.py
# check_caption_format) hard-fails a cue whose chars/second exceeds MAX_CPS = 27.0,
# measuring chars = sum(len(body line)). We target a stricter, standard-readability
# ceiling (17 cps) so every cue clears the gate with margin; GATE_CPS is kept only for
# reporting residuals against the actual hard limit. Cues too fast are held longer by
# extending ONLY their END time into the gap before the next cue (never overlapping,
# never shrinking, never moving a start) so the audio stays in sync. MIN_CUE_SECONDS is
# an absolute on-screen floor so even a short cue does not flash.
TARGET_CPS = 17.0        # readability ceiling we aim for (stricter than the gate)
GATE_CPS = 27.0          # the hard gate limit (check_final_acceptance MAX_CPS); reporting only
MIN_CUE_SECONDS = 0.8    # absolute minimum on-screen time per cue
CUE_GAP = 0.001          # keep a hair of separation so cues never overlap (monotonic)
# A cue's end may be extended at most this far past its forced-alignment end (and, via the
# cascade, a cue's start may lag its aligned start by at most this much). This HARD-BOUNDS
# desync: without it, a long contiguous run of mis-timed tiny cues would cascade an
# ever-growing lag (observed ~28 s). Capped, drift can never exceed MAX_LAG_SECONDS and
# self-resets at the next cue with slack; genuinely un-holdable dense runs stay as residual
# cps violations rather than desyncing the whole track (the top priority is audio sync).
# 1.0 s is within normal subtitle tolerance (a caption may trail its word by up to a second,
# never lead it); larger budgets give diminishing returns (see the MAX_LAG sweep) and only add
# desync, so this is the safe knee of the curve for the READABILITY target (17 cps). A second,
# larger budget (HARD_MAX_LAG_SECONDS) is spent ONLY on the handful of cues that would otherwise
# breach the gate ceiling (GATE_CPS) -- i.e. real unreadability -- so nearly all cues keep <=1 s
# lag and only the few genuinely-cramped cues borrow more to clear the hard gate.
MAX_LAG_SECONDS = 1.0
HARD_MAX_LAG_SECONDS = 2.0  # extra budget used only to pull a cue under the GATE ceiling
# A hair under GATE_CPS so an enforced cue lands strictly inside the gate (which fails on > MAX_CPS).
ENFORCE_GATE_CPS = 26.0
# align_general only lets a word MATCH AHEAD of the current whisper cursor (skip intervening
# whisper words) when the token is distinctive (>= this many chars). Short/common words ("the",
# "a", "of") were matching a *later* occurrence within the +6 lookahead and skipping real words,
# so the whisper cursor drained ~260 words too fast and the whole outro was left unanchored --
# collapsing ~40 caption cues onto the audio-end timestamp (the dominant cps-violation source).
# Requiring distinctiveness for a forward skip keeps legitimate re-sync (after a whisper
# insertion of a content word) while removing the spurious short-word jumps. A match at the
# current cursor is always allowed; this only constrains skipping ahead. Verbatim text/order is
# unchanged, so the 字幕=ナレ equality check is unaffected (it is timing-independent).
SKIP_AHEAD_MIN_CHARS = 6


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
            matches = (wn == tn or (len(tn) >= 4 and wn.startswith(tn[:4]))
                       or (len(wn) >= 4 and tn.startswith(wn[:4])))
            # allow a match at the cursor always; only allow SKIPPING ahead for a distinctive
            # token, so short/common words cannot drain the whisper cursor early (drift fix)
            if matches and (k == j or len(tn) >= SKIP_AHEAD_MIN_CHARS):
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


def _cps(ln, dur):
    """Reading speed of a cue, measured exactly as the acceptance gate does: cue char
    count (len of the on-screen text, spaces included) divided by on-screen seconds."""
    return (len(ln) / dur) if dur > 0 else float("inf")


def enforce_reading_speed(fixed):
    """Hold too-fast cues on screen long enough to read, WITHOUT letting a caption lead its
    audio or overlap a neighbour.

    Two mechanisms, applied left-to-right in one pass:
      1. GAP FILL (the safe, no-side-effect case): a too-fast cue's END is extended into any
         silent gap before the next cue starts. This alone fixes cues that are followed by a
         pause and never shifts anything.
      2. BOUNDED FORWARD REFLOW (needed for contiguous dense speech, where there is no gap):
         when a cue still cannot reach a readable speed / the MIN_CUE_SECONDS floor, it may
         push the NEXT cue's START later -- but only LATER, never earlier, so a caption never
         appears before its words are spoken (it can lag slightly, never lead). The push is
         absorbed by the next cue's surplus reading time: because most cues run far longer
         than they need (median ~1.9 s here), the lag self-resets to zero at the very next
         slack cue (its original start is already past our end, so no push carries forward).
         Drift is therefore bounded to a single dense burst, and every cue keeps its verbatim
         text and breath-unit segmentation -- only its on-screen window moves, forward, a
         fraction of a second.

    A cue's START is only ever moved LATER (cascaded from the previous cue's end), never
    earlier than the forced-alignment start, so sync to the audio is preserved (captions
    never precede speech). Returns (new_list, residual_target, residual_gate, max_lag) where
    the residuals count cues still over TARGET_CPS / GATE_CPS (should be ~0 for the gate),
    and max_lag is the largest forward start shift introduced (seconds)."""
    out = []
    max_lag = 0.0
    n = len(fixed)
    prev_end = None            # running end of the previously emitted cue (may be pushed later)
    for i, (s, e, ln) in enumerate(fixed):
        orig_s = s
        # cascade: this cue can only start at/after the previous (possibly-extended) cue's end,
        # and never earlier than its own aligned start -> a caption never leads its audio. No
        # explicit lag clamp is needed here: the END cap below bounds each cue's extension to
        # MAX_LAG past the NEXT cue's start, which in turn bounds this start's lag to ~MAX_LAG
        # and guarantees non-overlap without ever forcing s below the previous end.
        if prev_end is not None and s < prev_end + CUE_GAP:
            s = prev_end + CUE_GAP
        max_lag = max(max_lag, s - orig_s)
        next_start = fixed[i + 1][0] if i + 1 < n else e
        # how long this cue WANTS to stay up: enough for TARGET_CPS AND the min on-screen floor
        want_end = s + max(len(ln) / TARGET_CPS, MIN_CUE_SECONDS)
        # extension ceiling: up to MAX_LAG_SECONDS past the NEXT cue's ORIGINAL start. When a
        # silent gap follows, this consumes the whole gap first (that part shifts nothing -> zero
        # desync); only the last MAX_LAG seconds ever borrow into the next cue, bounding how far
        # its start is pushed. The last cue has no successor -> cap at its own end + MAX_LAG.
        cap = next_start + MAX_LAG_SECONDS
        new_e = min(max(e, want_end), cap)
        # If the cue is STILL over the hard gate ceiling (genuinely unreadable), spend the larger
        # HARD budget -- but only as much as needed to clear the gate -- so gate failures are
        # eliminated while >1 s lag stays confined to these few cramped cues.
        if _cps(ln, new_e - s) > GATE_CPS:
            hard_cap = next_start + HARD_MAX_LAG_SECONDS
            new_e = min(max(new_e, s + len(ln) / ENFORCE_GATE_CPS), hard_cap)
        if new_e <= s:                       # degenerate aligned window: give it a readable floor
            new_e = s + max(len(ln) / GATE_CPS, MIN_CUE_SECONDS)
        out.append((s, new_e, ln))
        prev_end = new_e
    residual_target = sum(1 for s, e, ln in out if _cps(ln, e - s) > TARGET_CPS)
    residual_gate = sum(1 for s, e, ln in out if _cps(ln, e - s) > GATE_CPS)
    return out, residual_target, residual_gate, max_lag


def write_srt(out_path, entries):
    """entries: list of (start, end, line). Enforce monotonic, non-overlapping times, then
    a readable reading speed (hold too-fast cues longer into the following gap); write SRT."""
    fixed = []
    for s, e, ln in entries:
        if fixed and s < fixed[-1][1]:
            s = fixed[-1][1]+0.001
        if e <= s:
            e = s+0.5
        fixed.append((s, e, ln))
    before_gate = sum(1 for s, e, ln in fixed if _cps(ln, e - s) > GATE_CPS)
    before_target = sum(1 for s, e, ln in fixed if _cps(ln, e - s) > TARGET_CPS)
    fixed, residual_target, residual_gate, max_lag = enforce_reading_speed(fixed)
    print(f"  cps: before {before_gate} over gate({GATE_CPS:.0f}) / "
          f"{before_target} over target({TARGET_CPS:.0f})  ->  after "
          f"{residual_gate} over gate / {residual_target} over target"
          f"  (max forward lag {max_lag:.2f}s, self-resetting)"
          + ("" if residual_gate == 0 else "  !! residual gate violations remain"))
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
