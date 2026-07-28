"""PD PRE-RENDER GATE (BLOCKING). Run BEFORE any expensive Remotion render.
Exit 0 = PASS (render allowed). Exit 1 = FAIL (render FORBIDDEN — fix first).

Catches the exact defects that forced EP50 rework AFTER a 6h render:
  kamishibai (too many static stills), warp/scanline treatments, missing/black-stub
  assets, over-repeated images, >2-line captions, broken asset references.

Usage: py -3.11 scripts/pd_prerender_gate.py <film.json> <public_dir> [--min-motion 0.62]
Generic across episodes (reads the film.json schema: cuts[].{kind,src,treatment}, captions[]).
"""
import sys, json, argparse, collections, subprocess
from pathlib import Path
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---- tunables (measured from the passing EP50 motion-first build) ----
MIN_MOTION_SHARE   = 0.62   # footage+motion cuts / all cuts (still <=38%)
MIN_DISTINCT_RATIO = 0.50   # distinct src / total cuts
MAX_REUSE          = 3      # any single src used at most this many times
MAX_CAPTION_CHARS  = 84     # hard cap; >2 lines on mobile big-caption box
CHARS_PER_LINE     = 42     # mobile big-caption wrap estimate -> lines = ceil(len/this)
MAX_CAPTION_LINES  = 2
BANNED_TREATMENTS  = {"depth", "scan", "card"}   # warp / scanline / 2.5D tilt
STILL_KINDS        = {"still", "kenburns", "static"}   # kinds that are NOT real motion
MIN_IMG_BYTES      = 50_000     # smaller => black stub / failed gen
MIN_LUMA           = 8.0        # mean luma; below => black frame

def ffprobe_dur(p):
    try:
        out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                              "-of","default=nk=1:nw=1", str(p)], capture_output=True, text=True, timeout=30)
        return float(out.stdout.strip() or 0)
    except Exception:
        return -1.0

def img_luma(p):
    try:
        from PIL import Image
        b = Image.open(p).convert("L").resize((64,36)).tobytes()
        return sum(b)/len(b)
    except Exception:
        return -1.0

def vid_luma(p, t):
    """Mean luma of one decoded video frame at time t (-1 if it cannot be decoded)."""
    try:
        import io
        from PIL import Image
        r = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.2f}","-i",str(p),"-frames:v","1",
                            "-f","image2pipe","-vcodec","png","-"], capture_output=True, timeout=60)
        if not r.stdout: return -1.0
        b = Image.open(io.BytesIO(r.stdout)).convert("L").resize((64,36)).tobytes()
        return sum(b)/len(b)
    except Exception:
        return -1.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film"); ap.add_argument("public")
    ap.add_argument("--min-motion", type=float, default=MIN_MOTION_SHARE)
    a = ap.parse_args()
    film = json.load(open(a.film, encoding="utf-8"))
    pub = Path(a.public)
    cuts = film["cuts"]; caps = film.get("captions", [])
    fails, warns = [], []

    # 1) MOTION-FIRST (anti-kamishibai): TRUE motion = src is a real video clip
    #    (i2v / stock .mp4), NOT a still image even with a parallax treatment.
    VID_EXT = (".mp4", ".mov", ".webm")
    n = len(cuts)
    def is_video(c): return str(c.get("src","")).lower().endswith(VID_EXT) or c.get("kind")=="footage"
    vid = sum(1 for c in cuts if is_video(c))
    still = n - vid
    motion_share = vid / n if n else 0
    if motion_share < a.min_motion:
        fails.append(f"MOTION-FIRST: real-video share {motion_share:.3f} < {a.min_motion} (still-image cuts={still}/{n}) = kamishibai risk")

    # 2) BANNED TREATMENTS (warp/scanline)
    bad_t = collections.Counter(c.get("treatment") for c in cuts if c.get("treatment") in BANNED_TREATMENTS)
    if bad_t:
        fails.append(f"TREATMENT: banned warp/scanline treatments present: {dict(bad_t)}")

    # 3) VARIETY (anti-repetition)
    srcs = [c["src"] for c in cuts]
    distinct = len(set(srcs)); ratio = distinct/len(srcs) if srcs else 0
    if ratio < MIN_DISTINCT_RATIO:
        fails.append(f"VARIETY: distinct src ratio {ratio:.3f} < {MIN_DISTINCT_RATIO}")
    over = {s:c for s,c in collections.Counter(srcs).items() if c > MAX_REUSE}
    if over:
        fails.append(f"VARIETY: {len(over)} src reused > {MAX_REUSE}x (worst {max(over.values())}x)")

    # 4) CAPTIONS <= 2 lines
    long_caps = []
    for c in caps:
        t = c.get("text",""); import math
        lines = t.count("\n")+1 if "\n" in t else math.ceil(len(t)/CHARS_PER_LINE)
        if len(t) > MAX_CAPTION_CHARS or lines > MAX_CAPTION_LINES:
            long_caps.append((len(t), lines, t[:50]))
    if long_caps:
        worst = max(long_caps)
        fails.append(f"CAPTIONS: {len(long_caps)} cues >2 lines / >{MAX_CAPTION_CHARS} chars (worst {worst[0]}ch/{worst[1]}ln: {worst[2]!r})")

    # 5) ASSET INTEGRITY (exist + not black-stub) — sample-check every DISTINCT src
    missing, stub, dark = [], [], []
    for s in sorted(set(srcs)):
        fp = pub / s
        if not fp.exists():
            missing.append(s); continue
        sz = fp.stat().st_size
        if fp.suffix.lower() in (".png",".jpg",".jpeg"):
            if sz < MIN_IMG_BYTES: stub.append(f"{s}({sz}B)"); continue
            l = img_luma(fp)
            if 0 <= l < MIN_LUMA: dark.append(f"{s}(luma{l:.1f})")
        elif fp.suffix.lower() in (".mp4",".mov",".webm"):
            if sz < MIN_IMG_BYTES: stub.append(f"{s}({sz}B)"); continue
            d = ffprobe_dur(fp)
            if d <= 0: stub.append(f"{s}(0dur)"); continue
            # A cut fills the frame for its whole duration, so sample HEAD/MID/TAIL and judge
            # by the MINIMUM. EP54 shipped a 4.7s black hole from AF-LIGHT-0498, which reads
            # 31.8 at mid but fades to 2.2 at its tail -- one mid sample cannot see that.
            lums = [vid_luma(fp, t) for t in (min(0.15, d*0.05), d*0.5, max(0.0, d-0.15))]
            ok = [x for x in lums if x >= 0]
            if ok and min(ok) < MIN_LUMA:
                dark.append(f"{s}(min luma {min(ok):.1f} of {[round(x,1) for x in ok]})")
    if missing: fails.append(f"ASSET MISSING: {len(missing)} referenced srcs absent under {pub} e.g. {missing[:3]}")
    if stub:    fails.append(f"ASSET STUB: {len(stub)} black-stub/empty assets e.g. {stub[:3]}")
    if dark:    fails.append(f"ASSET DARK: {len(dark)} near-black images e.g. {dark[:3]}")

    # 6) NARRATION referenced + present
    nar = film.get("narration")
    if nar:
        np_ = pub / nar
        if not np_.exists() and not Path(nar).exists():
            warns.append(f"NARRATION file not under public ({nar}) — ensure the render bundles audio")

    # 7) BUNDLE-REACHABLE: Remotion COPIES the public dir into its bundle and does NOT
    #    follow junctions/symlinks, so anything behind a reparse point is a 404 at render
    #    time even though every check above (which does follow them) says it exists.
    #    EP54 lost two render attempts to exactly this. Materialise with hardlinks instead.
    import os as _os
    reparse = []
    for root_, dirs_, _files in _os.walk(pub):
        for d in dirs_:
            fp = Path(root_) / d
            try:
                if _os.path.islink(fp) or bool(getattr(_os.stat(fp, follow_symlinks=False),
                                                       "st_file_attributes", 0) & 0x400):
                    reparse.append(str(fp))
            except OSError:
                continue
    if reparse:
        fails.append(f"PUBLIC DIR: {len(reparse)} junction/symlink dir(s) under {pub} — Remotion "
                     f"will NOT copy them into the bundle (404 at render). Use hardlinks. "
                     f"e.g. {reparse[:3]}")

    # 8) BRAND/STATIC assets the compositions request by literal name must be present too.
    for must in ("banner_sunrise.png", "fonts/Anton.ttf", "fonts/Archivo.ttf", "fonts/Oswald.ttf"):
        if not (pub / must).is_file():
            fails.append(f"STATIC ASSET MISSING: {must} not under {pub} (staticFile 404 at render)")

    # ---- report ----
    print("="*70); print(f"PD PRE-RENDER GATE  {a.film}")
    print(f"cuts={n} motion_share={motion_share:.3f} distinct={ratio:.3f} caps={len(caps)}")
    print("-"*70)
    for w in warns: print("  [warn]", w)
    if fails:
        for f in fails: print("  [FAIL]", f)
        print("-"*70); print(f"RESULT: FAIL ({len(fails)}) -- RENDER FORBIDDEN. Fix, then re-run this gate.")
        sys.exit(1)
    print("RESULT: PASS -- render allowed."); sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        # FAIL-CLOSED: any gate error blocks the render (never silently pass)
        print(f"RESULT: FAIL -- gate crashed ({type(e).__name__}: {e}) -- RENDER FORBIDDEN", flush=True)
        sys.exit(1)
