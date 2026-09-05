"""EP38 FINAL assembly v2 (owner-feedback fixes).
Structure: hook -> OP title (overlaid ~24s, florence-style, no re-time) -> body -> ED endcard.
- Captions: styled ASS (low position, longer lines, kinetic entrance, suppressed over cards).
- 7 overlay number-card PNGs + OP title overlay.
- Audio: 4-layer mix; body trimmed to mix length; ED endcard appended with outro-music tail.
Output: kidsforcash_final.v003.mp4 @1920x1080/48fps."""
from __future__ import annotations
import shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
EDIT = ROOT / "episodes" / EP / "08_edit"
SCENES = ROOT / "episodes" / EP / "04_scenes"
FONTS = ROOT / "remotion" / "public" / "fonts"
LIB = Path(r"E:/pd-media/library")
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"
W, H, FPS = 1920, 1080, 48
GOLD = (229, 181, 58); WHITE = (245, 247, 250); SILVER = (150, 160, 174); NAVY = (11, 26, 43)

# overlay number cards (ride on image/wan shots): (start, headline, sublabel)
CARDS = [
    (11.76, "3 MONTHS", None), (13.92, "90 SECONDS", "NO LAWYER"),
    (53.44, "WAIVER OF COUNSEL", None), (235.96, "INVENTORY", None),
    (442.18, "17.5 YEARS", "MICHAEL CONAHAN"), (457.32, "28 YEARS", "MARK CIAVARELLA"),
    (516.16, "SUBSCRIBE", "ONE TRUE STORY EVERY WEEK"),
]
DUR = 3.0
OP_START, OP_LEN = 23.6, 3.6     # OP title overlaid after the hook


def anton(sz): return ImageFont.truetype(str(FONTS / "Anton.ttf"), sz)
def oswald(sz): return ImageFont.truetype(str(FONTS / "Oswald.ttf"), sz)

def _probe(f):
    r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(r.stdout.strip())


def render_card(headline, sublabel, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    size = 150 if len(headline) <= 11 else 92
    fh = anton(size); cy = 340
    for off in (6, 3):
        d.text((W/2+off, cy+off), headline, font=fh, fill=(0, 0, 0, 170), anchor="mm")
    d.text((W/2, cy), headline, font=fh, fill=GOLD + (255,), anchor="mm")
    tw = d.textlength(headline, font=fh)
    d.rectangle([W/2 - min(tw, 620)/2, cy + size*0.55, W/2 + min(tw, 620)/2, cy + size*0.55 + 6],
                fill=GOLD + (255,))
    if sublabel:
        d.text((W/2, cy + size*0.7 + 55), sublabel, font=oswald(50), fill=WHITE + (255,), anchor="mm")
    im.save(path)


def render_op(path):
    """Brand opening title overlay: transparent w/ a soft centered scrim + series label + title."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(scrim)
    sd.rectangle([0, H//2 - 220, W, H//2 + 220], fill=(6, 12, 22, 150))
    im = Image.alpha_composite(im, scrim)
    d = ImageDraw.Draw(im)
    d.text((W/2, H/2 - 120), "P R I M E   D O C U M E N T A R Y", font=oswald(46),
           fill=SILVER + (255,), anchor="mm")
    for off in (5, 2):
        d.text((W/2+off, H/2+10+off), "KIDS FOR CASH", font=anton(150), fill=(0, 0, 0, 170), anchor="mm")
    d.text((W/2, H/2 + 10), "KIDS FOR CASH", font=anton(150), fill=WHITE + (255,), anchor="mm")
    d.rectangle([W/2 - 300, H/2 + 110, W/2 + 300, H/2 + 116], fill=GOLD + (255,))
    im.save(path)


def render_endcard(path):
    """6s ED endcard clip (navy, brand, subscribe) with outro-music audio."""
    tmp = EDIT / "_ec";
    if tmp.exists(): shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    dur = 6.0; n = int(dur * FPS)
    base = Image.new("RGB", (W, H), NAVY)
    for f in range(n):
        t = f / (n - 1); im = base.copy(); d = ImageDraw.Draw(im)
        a = min(1.0, t / 0.15); ao = min(1.0, (1 - t) / 0.12); al = min(a, ao)
        def col(c): return tuple(int(NAVY[i] + (c[i]-NAVY[i]) * al) for i in range(3))
        d.text((W/2, 360), "P R I M E   D O C U M E N T A R Y", font=oswald(58), fill=col(WHITE), anchor="mm")
        d.rectangle([W/2-260, 430, W/2+260, 435], fill=col(GOLD))
        d.text((W/2, 520), "TRUE STORIES OF POWER, THE LAW,", font=oswald(40), fill=col(SILVER), anchor="mm")
        d.text((W/2, 572), "AND THE PEOPLE CAUGHT BETWEEN", font=oswald(40), fill=col(SILVER), anchor="mm")
        d.text((W/2, 720), "SUBSCRIBE", font=anton(96), fill=col(GOLD), anchor="mm")
        im.save(tmp / f"f{f:05d}.png")
    # audio: outro music, 6s, faded
    mus = LIB / "music/outro/mus_20260614_outro_last_frame_v1.mp3"
    subprocess.run([FFMPEG, "-y", "-hide_banner", "-framerate", str(FPS), "-i", str(tmp / "f%05d.png"),
                    "-i", str(mus), "-t", "6", "-vf", "format=yuv420p",
                    "-af", "afade=t=in:st=0:d=0.5,afade=t=out:st=5.2:d=0.8,volume=0.5",
                    "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "256k",
                    "-r", str(FPS), str(path)], capture_output=True, text=True)
    shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    cards_dir = EDIT / "cards"; cards_dir.mkdir(parents=True, exist_ok=True)
    ass = SCENES / "captions.final.v001.ass"
    mix = EDIT / "kidsforcash_audio_mix.v001.wav"
    vis = EDIT / "visual_track.mp4"
    for f in (ass, mix, vis):
        if not f.exists(): print(f"MISSING {f}", file=sys.stderr); return 2

    # assets
    png = []
    for i, (st, hl, sub) in enumerate(CARDS):
        p = cards_dir / f"ov{i}.png"; render_card(hl, sub, p); png.append((st, p))
    op_png = cards_dir / "op_title.png"; render_op(op_png)
    endcard = EDIT / "endcard.mp4"; render_endcard(endcard)

    # local fonts + captions for libass (relative path avoids colon-escape)
    (EDIT / "fonts").mkdir(exist_ok=True)
    for fn in ("Oswald.ttf", "Anton.ttf"): shutil.copy2(FONTS / fn, EDIT / "fonts" / fn)
    shutil.copy2(ass, EDIT / "captions.ass")
    mix_len = _probe(mix)

    # ---- body: visual + ASS captions + OP overlay + number cards, audio muxed, trimmed ----
    inputs = ["-i", "visual_track.mp4", "-i", "kidsforcash_audio_mix.v001.wav"]
    inputs += ["-loop", "1", "-i", f"cards/{op_png.name}"]
    for st, p in png:
        inputs += ["-loop", "1", "-i", f"cards/{p.name}"]
    parts = [f"[0:v]subtitles=captions.ass:fontsdir=fonts[v0]"]
    # OP overlay (input index 2)
    en = OP_START + OP_LEN
    parts.append(f"[2:v]format=rgba,fade=t=in:st={OP_START:.2f}:d=0.4:alpha=1,"
                 f"fade=t=out:st={en-0.4:.2f}:d=0.4:alpha=1[op]")
    parts.append(f"[v0][op]overlay=0:0:enable='between(t,{OP_START:.2f},{en:.2f})'[vb0]")
    cur = "vb0"
    for i, (st, p) in enumerate(png):
        inp = 3 + i; e = st + DUR
        parts.append(f"[{inp}:v]format=rgba,fade=t=in:st={st:.2f}:d=0.3:alpha=1,"
                     f"fade=t=out:st={e-0.3:.2f}:d=0.3:alpha=1[c{i}]")
        parts.append(f"[{cur}][c{i}]overlay=0:0:enable='between(t,{st:.2f},{e:.2f})'[v{i+1}]")
        cur = f"v{i+1}"
    fg = ";".join(parts)
    body = EDIT / "body_final.mp4"
    cmd = [FFMPEG, "-y", "-hide_banner", *inputs, "-filter_complex", fg,
           "-map", f"[{cur}]", "-map", "1:a", "-t", f"{mix_len:.3f}",
           "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", str(body)]
    print("[final] rendering body (long pass) ...", flush=True)
    r = subprocess.run(cmd, cwd=str(EDIT), capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2500:], file=sys.stderr); return 3

    # ---- concat body + endcard ----
    lst = EDIT / "final_concat.txt"
    lst.write_text(f"file '{body.as_posix()}'\nfile '{endcard.as_posix()}'\n", encoding="utf-8")
    out = EDIT / "kidsforcash_final.v003.mp4"
    r2 = subprocess.run([FFMPEG, "-y", "-hide_banner", "-f", "concat", "-safe", "0",
                         "-i", str(lst), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", str(out)],
                        capture_output=True, text=True)
    if r2.returncode != 0:
        print(r2.stderr[-2000:], file=sys.stderr); return 4
    pr = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
                         "stream=width,height,r_frame_rate,nb_frames", "-show_entries",
                         "format=duration", "-of", "default=noprint_wrappers=1", str(out)],
                        capture_output=True, text=True)
    print("[final] OK ->", out); print(pr.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
