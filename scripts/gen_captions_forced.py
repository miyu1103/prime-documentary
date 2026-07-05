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
MAX_WORDS, MAX_CHARS = 8, 44  # LEGACY caption caps (gideon split_lines / legacy QC). DO NOT CHANGE:
                             # they define the shipped gideon segmentation and must stay byte-stable.
# GENERAL-path caps (narration_index episodes, e.g. carsearch). Raised so a whole clause/short
# sentence stays on ONE line instead of being sliced at an 8-word count boundary (the owner's
# "warrant." orphan). 52-char intent is realised as 50 to stay inside the acceptance gate's
# MAX_LINE_CHARS = 50 hard ceiling (single-line cues), while ~10 words keeps a clause whole.
SEG_MAX_WORDS, SEG_MAX_CHARS = 10, 50
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
MERGE_MAX_SECONDS = 6.8  # general path: a dense cue may merge with a neighbour into a 2-line cue
                         # only if the union window stays under this (< the gate's 7.0s ceiling)
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
# clause-based segmentation (GENERAL path) — breaks ONLY at clean boundaries
# ---------------------------------------------------------------------------
# Owner rejection of EP32 captions: lines were cut mid-phrase and short tails were orphaned
# (e.g. "...search your car without a" | "warrant.") because the old splitter flushed at a hard
# 8-word / 44-char slice regardless of grammar. This segmenter instead breaks ONLY at clean
# boundaries: PRIMARY at sentence / strong punctuation (. ? ! ; : and em-dash), SECONDARY at
# clause commas, packing whole clauses up to SEG_MAX_WORDS / SEG_MAX_CHARS. A clause is never
# sliced mid-phrase; a clause is sub-split (balanced, no 1-2 word tail) only when it ALONE
# exceeds the caps (an unavoidable comma-less run). Verbatim word order is unchanged, so the
# 字幕=ナレ equality gate is unaffected.

_ABBREV = {"mr", "mrs", "ms", "dr", "st", "vs", "etc", "no", "inc", "co", "ltd", "jr", "sr",
           "sgt", "lt", "gen", "sen", "rep", "gov", "col", "capt", "dept", "fig", "al"}
_TRAIL = "\"')]}”’"  # trailing quotes/brackets to ignore when reading final punctuation


def _strong_end(tok):
    """True iff `tok` ends a sentence / hard break unit (. ? ! ; : or em-dash), NOT counting an
    abbreviation period (U.S., Dr., etc.) which must not trigger a false sentence break."""
    core = tok.rstrip(_TRAIL)
    if not core:
        return False
    if core[-1] in "?!;:—":  # — = em-dash
        return True
    if core.endswith("."):
        if re.fullmatch(r"(?:[A-Za-z]\.)+[A-Za-z]?", core):   # U.S., U.S.A., J.
            return False
        if norm(core[:-1]) in _ABBREV:                        # Dr. Mr. etc.
            return False
        return True
    return False


def _comma_end(tok):
    """True iff `tok` ends a clause (comma), a soft/secondary break boundary."""
    return tok.rstrip(_TRAIL).endswith(",")


def _wc(idx_toks):
    """Spoken-word count of [(token, idx), ...] (ignores glued pure-punctuation like a lone dash)."""
    return sum(1 for t, _ in idx_toks if norm(t))


def _line_of(idx_toks):
    return " ".join(t for t, _ in idx_toks)


def _balanced_split(seg):
    """seg: [(token, idx), ...] for a single clause that ALONE exceeds the caps. Split at word
    boundaries into the fewest, size-balanced pieces so each piece is within SEG caps and no
    piece is a 1-2 word orphan (balanced pieces differ by <=1 word)."""
    n = len(seg)
    if n <= 1:
        return [seg]
    k = max((n + SEG_MAX_WORDS - 1) // SEG_MAX_WORDS,
            (len(_line_of(seg)) + SEG_MAX_CHARS - 1) // SEG_MAX_CHARS, 1)
    while True:
        base, rem = divmod(n, k)
        pieces = []
        idx = 0
        ok = True
        for p in range(k):
            size = base + (1 if p < rem else 0)
            piece = seg[idx:idx + size]
            idx += size
            pieces.append(piece)
            if len(_line_of(piece)) > SEG_MAX_CHARS:
                ok = False
        if ok or k >= n:
            return pieces
        k += 1


def split_lines_clause(tokens):
    """tokens: list of original-text words (with punctuation). -> [(line_str, idx_start, idx_end)].

    Clean-boundary segmentation for the general path (see the block comment above)."""
    idx_toks = [(tok, i) for i, tok in enumerate(tokens)]
    # 1) split the stream into sentences at strong punctuation
    sentences = []
    cur = []
    for tok, i in idx_toks:
        cur.append((tok, i))
        if _strong_end(tok):
            sentences.append(cur)
            cur = []
    if cur:
        sentences.append(cur)

    lines = []
    for sent in sentences:
        # whole sentence fits on one line -> keep it whole (the "warrant." fix)
        if _wc(sent) <= SEG_MAX_WORDS and len(_line_of(sent)) <= SEG_MAX_CHARS:
            lines.append(sent)
            continue
        # 2) split the sentence into clause segments at commas
        segs = []
        cur = []
        for tok, i in sent:
            cur.append((tok, i))
            if _comma_end(tok):
                segs.append(cur)
                cur = []
        if cur:
            segs.append(cur)
        # 3) any clause too big on its own -> balanced sub-split (no mid-phrase orphan)
        norm_segs = []
        for seg in segs:
            if _wc(seg) <= SEG_MAX_WORDS and len(_line_of(seg)) <= SEG_MAX_CHARS:
                norm_segs.append(seg)
            else:
                norm_segs.extend(_balanced_split(seg))
        # 4) greedily pack whole clauses into lines within caps (clauses stay whole)
        buf = []
        for seg in norm_segs:
            trial = buf + seg
            if buf and (_wc(trial) > SEG_MAX_WORDS or len(_line_of(trial)) > SEG_MAX_CHARS):
                lines.append(buf)
                buf = list(seg)
            else:
                buf = trial
        if buf:
            lines.append(buf)
    return [(_line_of(l), l[0][1], l[-1][1]) for l in lines]


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

def alignment_qc(caption_lines, chunks, max_words=MAX_WORDS, max_chars=MAX_CHARS):
    """caption_lines: list of line strings. chunks: text-source chunks.

    (1) Verify the concatenated caption text equals the verbatim narration text word-for-word
        (normalized) -- the 字幕=ナレ gate. (2) Flag any line over the char/word cap. Returns True
        iff both pass. Caps default to the legacy limits; the general path passes SEG_* caps.
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
            if wc_of(ln) > max_words or len(ln) > max_chars]
    if over:
        ok = False
        print(f"  !! QC line-cap: {len(over)} line(s) exceed {max_words} words / {max_chars} chars:")
        for ln_no, wc, cc, ln in over[:20]:
            print(f"     line {ln_no}: {wc}w {cc}c  {ln!r}")
    else:
        print(f"  QC line-cap: PASS  (all lines <= {max_words} words / {max_chars} chars)")
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
    # segment per chunk (clean-boundary clause segmentation), mapping local token indices to the
    # flat/global index. Each cue's start = first word's aligned start, end = last word's aligned
    # end -> the caption tracks the spoken words (no forward hold; tight sync enforced in write_srt).
    out = []; base = 0
    for toks in chunk_toks:
        for line, a, b in split_lines_clause(toks):
            s = times[base+a][0]; e = times[base+b][1]
            if e <= s:
                e = s+0.6
            out.append((s, e, line))
        base += len(toks)
    return out


def segment_only(chunks, clause=True):
    """--dry-run: split the text source into caption lines with no audio. Returns list of line
    strings. `clause` selects the general clean-boundary segmenter (default) vs the legacy one."""
    seg = split_lines_clause if clause else split_lines
    return [line for c in chunks for line, _a, _b in seg(glue_punct(c["text"].split()))]


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


def tight_sync(entries):
    """TIGHT audio-video sync (general path). Each cue's START stays at its forced-alignment start
    -- it is NEVER pushed later -- so a caption never lags the spoken word (fixes the owner's
    "字幕が少し遅い"). This replaces the old forward hold/extend-and-cascade, which slowed reading by
    delaying starts.

    Rules, applied in order:
      1. Guarantee e > s (degenerate/interpolated zero-length windows get a small floor).
      2. Resolve any overlap by trimming the PREVIOUS cue's END back to the next start -- never by
         delaying the next start. Starts are sacrosanct.
      3. Extend a cue's END only into the SILENT gap before the next cue, and only as far as the
         readability need (max of MIN_CUE_SECONDS and the TARGET_CPS duration), so a short cue does
         not flash yet clears once its readable time is spent. This moves no start -> adds zero lag.

    Returns (list, residual_gate, residual_target, max_lag). max_lag is the largest forward START
    shift introduced; it is 0.0 by construction (starts are never moved forward)."""
    ents = [[float(s), float(e), ln] for s, e, ln in entries]
    n = len(ents)
    orig_starts = [s for s, _e, _ln in ents]
    for i in range(n):
        if ents[i][1] <= ents[i][0]:
            ents[i][1] = ents[i][0] + MIN_CUE_SECONDS
    # non-overlap: trim previous END back to this start (keep starts tight)
    for i in range(n - 1):
        nxt_s = ents[i + 1][0]
        if ents[i][1] > nxt_s - CUE_GAP:
            ents[i][1] = max(ents[i][0] + CUE_GAP, nxt_s - CUE_GAP)
    # gentle end-fill into following silence only (never past the next start -> never lags)
    for i in range(n):
        s, e, ln = ents[i]
        want = s + max(len(ln) / TARGET_CPS, MIN_CUE_SECONDS)
        if i + 1 < n:
            ceil = ents[i + 1][0] - CUE_GAP
            new_e = min(max(e, want), ceil) if ceil > e else e
        else:
            new_e = max(e, want)
        ents[i][1] = new_e if new_e > s else s + MIN_CUE_SECONDS
    fixed = [(s, e, ln) for s, e, ln in ents]
    residual_gate = sum(1 for s, e, ln in fixed if _cps(ln, e - s) > GATE_CPS)
    residual_target = sum(1 for s, e, ln in fixed if _cps(ln, e - s) > TARGET_CPS)
    max_lag = max((fs - os for (fs, _e, _l), os in zip(fixed, orig_starts)), default=0.0)
    return fixed, residual_gate, residual_target, max(max_lag, 0.0)


def _cue_cps(lines, dur):
    """Reading speed of a (possibly 2-line) cue, measured exactly as the acceptance gate does:
    the SUM of on-screen line lengths (no inter-line newline counted) over the on-screen seconds."""
    return (sum(len(x) for x in lines) / dur) if dur > 0 else float("inf")


def merge_cps_pass(cues):
    """cues: list of [start, end, [lines]]. Where a cue's reading speed still exceeds the gate
    ceiling because its clause is spoken fast in a short window, MERGE it with an adjacent cue into
    a standard 2-line caption. The merged window is the UNION of the two adjacent windows, so:
      - no start is ever moved LATER (no lag; the top-priority audio sync is preserved), and
      - the merged cue starts at its first line's first spoken word (no cue-start lead).
    This buys reading time via SEGMENTATION (two clean clause lines stacked), never by delaying a
    cue. A merge is allowed only if the result is <= 2 lines, each <= SEG_MAX_CHARS, the union is
    <= MERGE_MAX_SECONDS, and it actually clears the gate. The NEXT neighbour is preferred (keeps
    the fast clause's own words on time); the PREVIOUS one is used only if next cannot. Verbatim
    word order is preserved, so the 字幕=ナレ equality gate is unaffected."""
    cues = [[s, e, list(lines)] for s, e, lines in cues]

    def cps(c):
        return _cue_cps(c[2], c[1] - c[0])

    def try_merge(a, b):
        """a precedes b in spoken order. Return merged [s,e,lines] iff it is legal and clears gate."""
        lines = a[2] + b[2]
        if len(lines) > 2 or any(len(x) > SEG_MAX_CHARS for x in lines):
            return None
        s = min(a[0], b[0]); e = max(a[1], b[1])
        if e - s > MERGE_MAX_SECONDS:
            return None
        m = [s, e, lines]
        return m if cps(m) <= ENFORCE_GATE_CPS else None

    i = 0
    while i < len(cues):
        if cps(cues[i]) > ENFORCE_GATE_CPS:
            # prefer merging with the NEXT cue (fast clause stays on time), else the PREVIOUS
            merged, lo = None, i
            if i + 1 < len(cues):
                m = try_merge(cues[i], cues[i + 1])
                if m:
                    merged, lo = m, i
            if merged is None and i - 1 >= 0:
                m = try_merge(cues[i - 1], cues[i])
                if m:
                    merged, lo = m, i - 1
            if merged is not None:
                cues[lo:lo + 2] = [merged]
                i = max(lo - 1, 0)      # re-check around the merge (handles adjacent violators)
                continue
        i += 1
    return cues


def write_srt(out_path, entries, tight=False):
    """entries: list of (start, end, line). `tight=True` (general path) keeps captions tightly
    synced to the spoken words (starts never delayed). `tight=False` (legacy path) preserves the
    original monotonic + reading-speed-hold behavior byte-for-byte."""
    if tight:
        before_gate = sum(1 for s, e, ln in entries if _cps(ln, (e - s) if e > s else 1e-9) > GATE_CPS)
        synced, _rg, _rt, max_lag = tight_sync(entries)
        cues = merge_cps_pass([[s, e, [ln]] for s, e, ln in synced])
        residual_gate = sum(1 for s, e, lines in cues if _cue_cps(lines, e - s) > GATE_CPS)
        residual_target = sum(1 for s, e, lines in cues if _cue_cps(lines, e - s) > TARGET_CPS)
        print(f"  cps (tight-sync): before {before_gate} over gate({GATE_CPS:.0f})  ->  after "
              f"{residual_gate} over gate / {residual_target} over target({TARGET_CPS:.0f})"
              f"  (max caption lag behind narration {max_lag:.3f}s; starts kept at forced alignment; "
              f"{len(synced) - len(cues)} dense cue(s) merged to 2-line)"
              + ("" if residual_gate == 0 else "  !! residual gate violations remain"))
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            "\n".join(f"{i+1}\n{srt_ts(s)} --> {srt_ts(e)}\n" + "\n".join(lines) + "\n"
                      for i, (s, e, lines) in enumerate(cues)), "utf-8")
        return [(s, e, "\n".join(lines)) for s, e, lines in cues]
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
    # The legacy path (gideon: voice_plan source + per-chunk timing windows) keeps its original
    # segmenter, caps, and reading-speed-hold timing untouched. Every other (narration_index)
    # episode uses the clean-boundary clause segmenter + tight sync.
    legacy = (source == "voice_plan.v001.json") and (ep_dir / "08_edit" / "timing.v001.json").exists()
    is_general = not legacy
    qc_words, qc_chars = (SEG_MAX_WORDS, SEG_MAX_CHARS) if is_general else (MAX_WORDS, MAX_CHARS)
    print(f"ep={slug}  text-source={source}  chunks={len(chunks)}  words={nwords}  "
          f"path={'general clause/tight-sync' if is_general else 'legacy'}")

    # segment (used for the dry-run preview and for the QC text-equality check)
    lines = segment_only(chunks, clause=is_general)

    if args.dry_run:
        print(f"[dry-run] would produce {len(lines)} caption lines (segment-only, no audio)")
        alignment_qc(lines, chunks, qc_words, qc_chars)
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
    entries = align_legacy(ep_dir, chunks, master) if legacy else align_general(chunks, master)
    fixed = write_srt(out_path, entries, tight=is_general)
    print(f"wrote {out_path.relative_to(ROOT) if out_path.is_relative_to(ROOT) else out_path}  "
          f"({len(fixed)} cues)  [{'legacy timing-window' if legacy else 'global'} alignment]")
    # QC on PHYSICAL lines (a general-path cue may be a 2-line caption after the cps merge)
    alignment_qc([pl for _s, _e, ln in fixed for pl in ln.split("\n")], chunks, qc_words, qc_chars)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
