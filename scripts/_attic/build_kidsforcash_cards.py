"""Render the 7 EP38 motion-graphic 'card' shots as animated 1920x1080@48fps clips.
Brand-styled (navy ground, gold/white/electric, Anton/Oswald). Real animation:
bars grow, numbers count up, stamp slams, gauge fills, records scan/clear.
Writes into 08_edit/shots/NNNN.mp4 (same slots the still/wan builder skipped)."""
from __future__ import annotations
import math, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
OUTDIR = ROOT / "episodes" / EP / "08_edit" / "shots"
FONTS = ROOT / "remotion" / "public" / "fonts"
TMP = Path(r"C:/Users/aab15/AppData/Local/Temp/kfc_cards")
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FPS = 48; W, H = 1920, 1080
NAVY = (11, 26, 43); INK = (8, 9, 13); GOLD = (229, 181, 58)
WHITE = (245, 247, 250); SILVER = (140, 150, 165); ELEC = (31, 107, 255)

def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)

def ease(p: float) -> float:      # easeOutCubic
    p = max(0.0, min(1.0, p)); return 1 - (1 - p) ** 3

def bg() -> Image.Image:
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    for r in range(0, 700, 4):     # cheap radial vignette
        a = int(60 * (r / 700))
        d.ellipse([W//2 - (900 - r), H//2 - (520 - r*0.55), W//2 + (900 - r), H//2 + (520 - r*0.55)],
                  outline=(max(NAVY[0]-a//3,0), max(NAVY[1]-a//4,0), max(NAVY[2]-a//4,0)))
    return im

def ctext(d, cx, y, s, fnt, fill, anchor="mm"):
    d.text((cx, y), s, font=fnt, fill=fill, anchor=anchor)

# ---- per-type renderers: draw(img, t01) -------------------------------------
def r_bars(im, t):
    d = ImageDraw.Draw(im)
    ctext(d, W/2, 150, "CHILDREN SENT TO A LOCKED FACILITY", font("Oswald.ttf", 46), SILVER)
    grow = ease(t/0.7) if t < 0.7 else 1.0
    base = 820
    for i, (label, pct, col) in enumerate([("STATEWIDE", 8.4, SILVER), ("CIAVARELLA'S COURT", 50.0, GOLD)]):
        cx = W*0.32 + i*W*0.36
        hgt = int((pct/50.0) * 480 * grow)
        d.rectangle([cx-150, base-hgt, cx+150, base], fill=col)
        val = pct * grow
        ctext(d, cx, base-hgt-70, f"{val:.1f}%", font("Anton.ttf", 130), col)
        ctext(d, cx, base+55, label, font("Oswald.ttf", 44), WHITE)

def r_money(im, t):
    d = ImageDraw.Draw(im)
    ctext(d, W/2, 150, "PRIVATE JAIL", font("Oswald.ttf", 52), SILVER)
    ctext(d, W/2, H-150, "THE JUDGES", font("Oswald.ttf", 52), WHITE)
    # flowing gold dots along a vertical path
    for k in range(7):
        ph = (t*1.6 + k/7.0) % 1.0
        y = 230 + ph*(H-460); x = W/2 + math.sin(ph*6.28)*12
        rad = 10 + 6*math.sin(ph*3.14)
        d.ellipse([x-rad, y-rad, x+rad, y+rad], fill=GOLD)
    val = 2.8 * ease(t/0.45)
    ctext(d, W/2, H/2, f"${val:.1f} MILLION", font("Anton.ttf", 150), GOLD)
    ctext(d, W/2, H/2+110, "IN KICKBACKS", font("Oswald.ttf", 50), WHITE)

def r_stamp(im, t):
    d = ImageDraw.Draw(im)
    ctext(d, W/2, H/2-140, "THEY CALLED IT A", font("Oswald.ttf", 48), SILVER)
    ctext(d, W/2, H/2-40, "FINDER'S FEE", font("Anton.ttf", 130), WHITE)
    if t > 0.45:
        p = ease((t-0.45)/0.25)
        sz = int(200 - 60*p); ang = -12
        stamp = Image.new("RGBA", (900, 320), (0,0,0,0)); sd = ImageDraw.Draw(stamp)
        f = font("Anton.ttf", sz)
        sd.text((450, 160), "BRIBE", font=f, fill=(211,47,47, int(255*p)), anchor="mm")
        sd.rectangle([120, 40, 780, 280], outline=(211,47,47, int(255*p)), width=10)
        stamp = stamp.rotate(ang, expand=True, resample=Image.BICUBIC)
        im.paste(stamp, (W//2 - stamp.width//2, int(H*0.62) - stamp.height//2), stamp)

def r_gauge(im, t):
    d = ImageDraw.Draw(im)
    cx, cy, R = W/2, H/2+40, 260
    d.arc([cx-R, cy-R, cx+R, cy+R], 135, 405, fill=(40,52,70), width=40)
    sweep = ease(t/0.8) * 270
    d.arc([cx-R, cy-R, cx+R, cy+R], 135, 135+sweep, fill=GOLD, width=40)
    ctext(d, cx, cy-30, "7-11x", font("Anton.ttf", 150), GOLD)
    ctext(d, cx, cy+80, "MORE OFTEN, NO LAWYER", font("Oswald.ttf", 44), WHITE)

def r_mech(im, t):
    d = ImageDraw.Draw(im)
    cols, rows = 16, 7; mx, my = 360, 300; gx, gy = 78, 70
    n = int(cols*rows * ease(t/0.85))
    for k in range(n):
        r, c = divmod(k, cols); x = mx + c*gx; y = my + r*gy
        col = GOLD if (k % 9 == 0) else (70, 84, 104)
        d.ellipse([x-16, y-26, x+16, y+26], fill=col)   # tiny figures
        d.ellipse([x-10, y-40, x+10, y-20], fill=col)
    ctext(d, W/2, 150, "HUNDREDS OF CHILDREN. THE SAME, EVERY TIME.", font("Oswald.ttf", 46), WHITE)

def r_records(im, t):
    d = ImageDraw.Draw(im)
    ctext(d, W/2, 140, "THE COURT ERASED THEM", font("Oswald.ttf", 46), SILVER)
    rows = 12; top = 250; rh = 46
    scan = ease(t/0.85)
    for i in range(rows):
        y = top + i*rh
        cleared = (i/rows) < scan
        col = (30,38,52) if cleared else (90,104,126)
        w = int(1200 * (0.3 + 0.7*abs(math.sin(i*1.3))))
        d.rectangle([W/2-600, y, W/2-600+w, y+22], fill=col)
    # scan line
    sy = top + scan*rows*rh
    d.rectangle([W/2-640, sy-3, W/2+640, sy+3], fill=ELEC)
    val = int(2251 * ease(t/0.5))
    ctext(d, W/2, H-190, "THOUSANDS", font("Anton.ttf", 130), GOLD)
    ctext(d, W/2, H-95, "CONVICTIONS VACATED", font("Oswald.ttf", 48), WHITE)

def r_ticker(im, t):
    d = ImageDraw.Draw(im)
    val = 200 * ease(t/0.5)
    ctext(d, W/2, H/2-30, f"${val:.0f} MILLION+", font("Anton.ttf", 170), GOLD)
    ctext(d, W/2, H/2+110, "ORDERED TO PAY THE FAMILIES", font("Oswald.ttf", 52), WHITE)

CARDS = {
    12: ("bars",    3.52, r_bars),
    30: ("money",   6.12, r_money),
    32: ("stamp",   7.70, r_stamp),
    35: ("gauge",   5.52, r_gauge),
    57: ("mech",    8.84, r_mech),
    64: ("records", 5.70, r_records),
    71: ("ticker",  5.76, r_ticker),
}

def render(idx: int, name: str, dur: float, fn) -> bool:
    work = TMP / f"{idx:04d}"
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True)
    nframes = max(2, round(dur*FPS))
    base = bg()
    for f in range(nframes):
        t = f / (nframes-1)
        im = base.copy()   # navy ground is ALWAYS present (no black fade -> no black flash)
        fn(im, t)
        im.save(work / f"f{f:05d}.png")
    out = OUTDIR / f"{idx:04d}.mp4"
    r = subprocess.run([FFMPEG, "-y", "-hide_banner", "-framerate", str(FPS),
                        "-i", str(work / "f%05d.png"), "-r", str(FPS),
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-pix_fmt", "yuv420p", str(out)], capture_output=True, text=True)
    shutil.rmtree(work, ignore_errors=True)
    ok = r.returncode == 0 and out.exists()
    print(f"  [{idx:04d}] card {name} {dur:.2f}s -> {'OK' if ok else 'FAIL'}", flush=True)
    return ok

def main() -> int:
    TMP.mkdir(parents=True, exist_ok=True)
    good = 0
    for idx, (name, dur, fn) in CARDS.items():
        if render(idx, name, dur, fn): good += 1
    print(f"\ncards done: {good}/{len(CARDS)}")
    return 0 if good == len(CARDS) else 1

if __name__ == "__main__":
    raise SystemExit(main())
