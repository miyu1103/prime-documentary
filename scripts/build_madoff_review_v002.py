#!/usr/bin/env python3
"""Build PD-2026-005 Madoff review cut v002 with moving visuals + BGM/SFX.

No paid APIs, no upload. Uses the existing local draft narration for now.
Output:
  H:/pd-media/episodes/PD-2026-005-madoff/08_edit/madoff_review_v002_local_audio.mp4
  episodes/PD-2026-005-madoff/08_edit/renders/review.proxy.v002.mp4
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-005-madoff"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EPM = MEDIA / "episodes" / EP
LIB = MEDIA / "library"
FFMPEG = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
FFPROBE = Path(r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe")
if not FFMPEG.exists():
    FFMPEG = Path("ffmpeg")
if not FFPROBE.exists():
    FFPROBE = Path("ffprobe")

W, H, FPS = 1920, 1080, 30
INK = (7, 8, 12)
NAVY = (12, 20, 32)
GOLD = (212, 165, 82)
GOLD2 = (246, 205, 118)
SILVER = (208, 213, 221)
MUTED = (120, 126, 138)
RED = (128, 38, 32)


def run(cmd: list[str | os.PathLike[str]], desc: str) -> None:
    print(f">> {desc}")
    p = subprocess.run([str(x) for x in cmd], capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print((p.stderr or "")[-3000:])
        raise RuntimeError(desc)


def probe_duration(path: Path) -> float:
    p = subprocess.run(
        [str(FFPROBE), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
    )
    return float(p.stdout.strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = [
        r"C:\Windows\Fonts\georgiab.ttf" if bold else r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for n in names:
        if Path(n).exists():
            return ImageFont.truetype(n, size=size)
    return ImageFont.load_default()


F_TITLE = font(76, True)
F_BIG = font(124, True)
F_MED = font(42, True)
F_BODY = font(31, False)
F_SMALL = font(24, False)


def base(seed: int) -> Image.Image:
    random.seed(seed)
    img = Image.new("RGB", (W, H), INK)
    px = img.load()
    for y in range(H):
        for x in range(W):
            rx = (x - W * 0.58) / W
            ry = (y - H * 0.42) / H
            glow = max(0, 1 - math.sqrt(rx * rx * 3.0 + ry * ry * 5.0) * 2.6)
            vign = max(0, 1 - math.sqrt(((x - W / 2) / W) ** 2 + ((y - H / 2) / H) ** 2) * 1.9)
            noise = random.randint(-4, 4)
            r = int(INK[0] + NAVY[0] * 0.25 + glow * 50 + vign * 7 + noise)
            g = int(INK[1] + NAVY[1] * 0.30 + glow * 35 + vign * 7 + noise)
            b = int(INK[2] + NAVY[2] * 0.36 + glow * 18 + vign * 7 + noise)
            px[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    return img.filter(ImageFilter.GaussianBlur(0.25))


def text_center(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt, fill, anchor="mm") -> None:
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def add_brand(draw: ImageDraw.ImageDraw, chapter: str, citation: str | None = None) -> None:
    draw.text((54, 42), "PRIME DOCUMENTARY", font=F_SMALL, fill=(190, 168, 116))
    draw.line((54, 78, 320, 78), fill=GOLD, width=2)
    draw.text((54, 92), chapter.upper(), font=F_SMALL, fill=MUTED)
    if citation:
        draw.rounded_rectangle((54, 970, 960, 1022), radius=8, fill=(5, 6, 9, 190), outline=(135, 105, 54), width=1)
        draw.text((76, 984), citation, font=F_SMALL, fill=SILVER)


def smooth_line(draw: ImageDraw.ImageDraw, box=(230, 270, 1690, 790), jagged: bool = False, label: str = "") -> None:
    x0, y0, x1, y1 = box
    draw.line((x0, y1, x1, y1), fill=(75, 70, 60), width=2)
    draw.line((x0, y0, x0, y1), fill=(75, 70, 60), width=2)
    pts = []
    for i in range(80):
        t = i / 79
        x = x0 + t * (x1 - x0)
        if jagged:
            y = y1 - (0.18 + t * 0.62 + math.sin(t * 28) * 0.075 + math.sin(t * 71) * 0.025) * (y1 - y0)
        else:
            y = y1 - (0.15 + t * 0.68 + math.sin(t * 6) * 0.012) * (y1 - y0)
        pts.append((x, y))
    for w, col in [(14, (80, 54, 18)), (7, GOLD2), (3, (255, 239, 172))]:
        draw.line(pts, fill=col, width=w, joint="curve")
    for p in pts[::12]:
        draw.ellipse((p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5), fill=(255, 230, 160))
    if label:
        draw.text((x0, y0 - 56), label, font=F_MED, fill=SILVER)


def silhouette(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1.0, color=(8, 8, 10)) -> None:
    r = int(45 * scale)
    draw.ellipse((cx - r, cy - int(160 * scale), cx + r, cy - int(70 * scale)), fill=color)
    draw.rounded_rectangle((cx - int(82 * scale), cy - int(72 * scale), cx + int(82 * scale), cy + int(140 * scale)), radius=45, fill=color)


def doc_stack(draw: ImageDraw.ImageDraw, x: int, y: int, n: int = 6) -> None:
    for i in range(n):
        off = i * 18
        draw.rounded_rectangle((x + off, y + off, x + 430 + off, y + 570 + off), radius=14, fill=(226, 213, 180), outline=(89, 64, 31), width=3)
        draw.line((x + 55 + off, y + 100 + off, x + 360 + off, y + 100 + off), fill=(70, 55, 38), width=5)
        for k in range(8):
            yy = y + 160 + off + k * 42
            draw.line((x + 55 + off, yy, x + 355 + off, yy), fill=(100, 89, 70), width=2)
        smooth_line(draw, (x + 58 + off, y + 385 + off, x + 355 + off, y + 520 + off))


def vault(draw: ImageDraw.ImageDraw, empty: bool = False) -> None:
    draw.ellipse((520, 190, 1400, 930), fill=(21, 24, 28), outline=(95, 82, 55), width=18)
    draw.ellipse((650, 300, 1270, 820), fill=(6, 7, 10), outline=(126, 100, 57), width=9)
    for a in range(0, 360, 30):
        x = 960 + math.cos(math.radians(a)) * 260
        y = 560 + math.sin(math.radians(a)) * 215
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(151, 128, 78))
    if empty:
        draw.text((960, 560), "EMPTY", font=F_BIG, fill=(162, 126, 66), anchor="mm")
    else:
        draw.text((960, 560), "NO TRADES", font=F_BIG, fill=(162, 126, 66), anchor="mm")


def coin_loop(draw: ImageDraw.ImageDraw) -> None:
    cx, cy, rad = 960, 550, 270
    for a in range(0, 360, 45):
        x = cx + math.cos(math.radians(a)) * rad
        y = cy + math.sin(math.radians(a)) * rad
        silhouette(draw, int(x), int(y) + 80, 0.45, (10, 10, 12))
        draw.ellipse((x - 28, y - 28, x + 28, y + 28), fill=GOLD, outline=(255, 233, 158), width=4)
    for a in range(0, 360, 45):
        a2 = a + 28
        p1 = (cx + math.cos(math.radians(a)) * rad, cy + math.sin(math.radians(a)) * rad)
        p2 = (cx + math.cos(math.radians(a2)) * rad, cy + math.sin(math.radians(a2)) * rad)
        draw.line((p1, p2), fill=(184, 139, 64), width=8)
    draw.text((960, 550), "NEW MONEY\nPAYS OLD\nPAYOUTS", font=F_MED, fill=SILVER, anchor="mm", align="center")


def number_morph(draw: ImageDraw.ImageDraw) -> None:
    draw.text((410, 345), "$65B", font=F_BIG, fill=GOLD2, anchor="mm")
    draw.text((410, 455), "on statements", font=F_BODY, fill=SILVER, anchor="mm")
    draw.line((590, 405, 1250, 405), fill=(148, 111, 50), width=8)
    draw.polygon([(1250, 405), (1210, 382), (1210, 428)], fill=(148, 111, 50))
    draw.text((1510, 345), "$17.5B", font=F_BIG, fill=(232, 202, 135), anchor="mm")
    draw.text((1510, 455), "real principal", font=F_BODY, fill=SILVER, anchor="mm")
    draw.rounded_rectangle((575, 625, 1345, 715), radius=14, fill=(38, 26, 12), outline=GOLD, width=2)
    draw.text((960, 670), "THE GAP WAS THE ILLUSION", font=F_MED, fill=GOLD2, anchor="mm")


def timeline(draw: ImageDraw.ImageDraw, items: list[tuple[str, str]], title: str) -> None:
    y = 590
    draw.text((960, 300), title, font=F_TITLE, fill=GOLD2, anchor="mm")
    draw.line((280, y, 1640, y), fill=(140, 111, 63), width=6)
    for i, (year, text) in enumerate(items):
        x = 280 + i * (1360 / max(1, len(items) - 1))
        draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill=GOLD2)
        draw.line((x, y, x, y + 120), fill=(100, 84, 54), width=3)
        draw.text((x, y - 70), year, font=F_MED, fill=SILVER, anchor="mm")
        draw.text((x, y + 150), text, font=F_SMALL, fill=SILVER, anchor="mm")


def draw_scene(scene_id: str, title: str, subtitle: str, kind: str, chapter: str, citation: str | None, path: Path) -> None:
    img = base(abs(hash(scene_id)) % 10000)
    draw = ImageDraw.Draw(img, "RGBA")
    add_brand(draw, chapter, citation)
    if kind == "line":
        smooth_line(draw, label="THE LINE THAT NEVER BLINKED")
        draw.text((960, 880), "too smooth to be safe", font=F_MED, fill=GOLD2, anchor="mm")
    elif kind == "trust":
        for i, x in enumerate([430, 720, 1020, 1320, 1540]):
            silhouette(draw, x, 660, 0.9 + i * 0.03)
        smooth_line(draw, (360, 170, 1560, 360))
        draw.text((960, 820), "TRUST MADE THE QUESTIONS QUIET", font=F_MED, fill=GOLD2, anchor="mm")
    elif kind == "statements":
        doc_stack(draw, 520, 180, 4)
        draw.text((1190, 510), "FABRICATED\nCONFIRMATIONS", font=F_TITLE, fill=GOLD2, anchor="mm", align="center")
    elif kind == "vault":
        vault(draw, empty=False)
    elif kind == "loop":
        coin_loop(draw)
    elif kind == "number":
        number_morph(draw)
    elif kind == "math":
        draw.rounded_rectangle((500, 210, 1420, 820), radius=22, fill=(214, 202, 171), outline=(93, 71, 38), width=4)
        smooth_line(draw, (610, 355, 1310, 650), label="")
        draw.line((700, 430, 1220, 520), fill=RED, width=8)
        draw.text((960, 720), "IMPOSSIBLE", font=F_BIG, fill=RED, anchor="mm")
        draw.ellipse((310, 300, 460, 450), fill=(12, 12, 14))
        draw.rounded_rectangle((260, 430, 510, 870), radius=90, fill=(10, 10, 12))
    elif kind == "warnings":
        timeline(draw, [("2000", "warning"), ("2001", "warning"), ("2005", "report"), ("2007", "warning"), ("2008", "collapse")], "WARNINGS IGNORED")
    elif kind == "empty":
        vault(draw, empty=True)
    elif kind == "court":
        for x in range(460, 1500, 170):
            draw.rectangle((x, 310, x + 70, 805), fill=(46, 44, 42), outline=(155, 125, 72), width=3)
        draw.polygon([(400, 310), (1520, 310), (1380, 180), (540, 180)], fill=(45, 43, 42), outline=GOLD)
        draw.rectangle((350, 805, 1570, 855), fill=(65, 59, 48))
        draw.text((960, 925), "GUILTY TO 11 FELONIES", font=F_MED, fill=GOLD2, anchor="mm")
    elif kind == "prison":
        for x in range(520, 1410, 110):
            draw.rectangle((x, 180, x + 38, 940), fill=(16, 17, 20))
            draw.rectangle((x + 6, 180, x + 14, 940), fill=(73, 61, 44))
        draw.text((960, 540), "150 YEARS", font=F_BIG, fill=GOLD2, anchor="mm")
    elif kind == "recovery":
        draw.rectangle((470, 730, 680, 790), fill=(85, 73, 45))
        draw.rectangle((760, 610, 970, 790), fill=(129, 103, 54))
        draw.rectangle((1050, 470, 1260, 790), fill=GOLD)
        draw.text((960, 330), ">90%", font=F_BIG, fill=GOLD2, anchor="mm")
        draw.text((960, 405), "of real losses recovered", font=F_MED, fill=SILVER, anchor="mm")
    elif kind == "compare":
        smooth_line(draw, (230, 310, 860, 760), jagged=False, label="SMOOTH")
        smooth_line(draw, (1060, 310, 1690, 760), jagged=True, label="REAL")
        draw.text((960, 875), "SMOOTHNESS IS A WARNING SIGN", font=F_MED, fill=GOLD2, anchor="mm")
    else:
        text_center(draw, (960, 475), title, F_TITLE, GOLD2)
    draw.text((960, 136), title, font=F_TITLE, fill=GOLD2, anchor="mm")
    if subtitle:
        draw.text((960, 210), subtitle, font=F_BODY, fill=SILVER, anchor="mm")
    draw.rounded_rectangle((1515, 56, 1840, 104), radius=8, fill=(5, 6, 9, 150), outline=(115, 95, 55))
    draw.text((1535, 68), "symbolic reconstruction", font=F_SMALL, fill=SILVER)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=94)


SCENES = [
    ("S01", "LOOK AT THIS LINE", "It goes up when everything else falls.", "line", "hook", "CLM-0006 - return smoothness red flag", 28),
    ("S02", "THE TRUSTED NAME", "Prestige made the risk feel invisible.", "trust", "opening", "symbolic reconstruction; not financial advice", 46),
    ("S03", "THE PRIVATE CLUB", "Invitation felt like proof.", "statements", "act I", None, 46),
    ("S04", "THE QUESTIONS MELTED AWAY", "Professional investors saw safety.", "trust", "act I", "CLM-0006 - unusually steady returns", 50),
    ("S05", "NO REAL TRADES", "The money did not go where people thought.", "vault", "act II", "Trustee findings - investment advisory operation", 58),
    ("S06", "THE PONZI LOOP", "New money paid old payouts.", "loop", "act II", "CLM-0003 - Ponzi mechanism", 58),
    ("S07", "$65B WAS PAPER", "The illusion and the real cash were different things.", "number", "act II", "CLM-0004 - SIPA Trustee estimate", 58),
    ("S08", "THE FATAL MATH", "It could never stop growing.", "loop", "act II", None, 42),
    ("S09", "THE MAN WHO DID THE MATH", "The smoothness was the evidence.", "math", "act III", "CLM-0005 / CLM-0006", 62),
    ("S10", "WARNINGS IGNORED", "The watchdog had the answer and missed it.", "warnings", "act III", "CLM-0011 - SEC OIG report", 68),
    ("S11", "THE WATCHDOG SLEPT", "Trust, calm, and paperwork were enough.", "statements", "act III", None, 42),
    ("S12", "2008", "When money wanted out, there was no vault.", "empty", "act IV", None, 48),
    ("S13", "THE COURTROOM", "He pleaded guilty. There was no trial.", "court", "act IV", "CLM-0001 / CLM-0007", 42),
    ("S14", "150 YEARS", "A symbolic sentence for a hollowed-out fraud.", "prison", "act IV", "CLM-0002 - sentence", 32),
    ("S15", "THE RECOVERY", "The ending was not as simple as total loss.", "recovery", "act IV", "CLM-0009 - trustee recoveries", 42),
    ("S16", "THE LESSON", "If a chart looks too perfect, ask it.", "compare", "ending", "not financial advice", 64),
]


def render_visuals(tmp: Path, total_target: float) -> Path:
    still_dir = EPM / "05_visuals" / "coded_madoff_v002"
    seg_dir = tmp / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    durations = [s[-1] for s in SCENES]
    scale = total_target / sum(durations)
    segs = []
    for idx, (sid, title, sub, kind, chapter, citation, dur) in enumerate(SCENES):
        img = still_dir / f"{idx+1:02d}_{sid}_{kind}.jpg"
        draw_scene(sid, title, sub, kind, chapter, citation, img)
        out = seg_dir / f"{idx+1:02d}_{sid}.mp4"
        d = max(3.0, dur * scale)
        zoom = "zoompan=z='min(zoom+0.00045,1.115)':x='iw/2-(iw/zoom/2)+sin(on/55)*18':y='ih/2-(ih/zoom/2)+cos(on/70)*12':d=%d:s=1920x1080:fps=30" % int(round(d * FPS))
        vf = f"scale=2240:-1,{zoom},format=yuv420p"
        run([FFMPEG, "-y", "-loop", "1", "-i", img, "-vf", vf, "-t", f"{d:.3f}", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out], f"visual {sid}")
        segs.append(out)
    concat = tmp / "concat.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), "utf-8")
    video = tmp / "visuals.mp4"
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat, "-c", "copy", video], "concat moving visuals")
    return video


def build_music(tmp: Path, total: float) -> Path:
    tracks = [
        LIB / "music/hook/mus_20260614_hook_glass_air_bed_v1.mp3",
        LIB / "music/opening/mus_20260614_opening_measured_arpeggio_v1.mp3",
        LIB / "music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v1.mp3",
        LIB / "music/reveal/mus_20260614_reveal_hidden_system_clicks_v1.mp3",
        LIB / "music/tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3",
        LIB / "music/somber/mus_20260614_somber_ledger_of_ash_v1.mp3",
        LIB / "music/outro/mus_20260614_outro_last_frame_v1.mp3",
    ]
    weights = [0.09, 0.10, 0.18, 0.21, 0.18, 0.12, 0.12]
    inputs, filters, labels = [], [], []
    cur = 0.0
    for i, (tr, w) in enumerate(zip(tracks, weights)):
        dur = total * w if i < len(tracks) - 1 else total - cur
        inputs += ["-stream_loop", "-1", "-i", str(tr)]
        delay = int(cur * 1000)
        fade_out = max(dur - 1.4, 0.1)
        filters.append(
            f"[{i}:a]atrim=0:{dur:.3f},afade=t=in:st=0:d=1.0,afade=t=out:st={fade_out:.3f}:d=1.2,adelay={delay}|{delay}[m{i}]"
        )
        labels.append(f"[m{i}]")
        cur += dur
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,volume=0.22[music]")
    out = tmp / "music.m4a"
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[music]", "-t", f"{total:.3f}", "-c:a", "aac", "-b:a", "192k", out], "music bed")
    return out


def build_sfx(tmp: Path, total: float) -> Path:
    sfx_files = [
        "sfx_whoosh_short.mp3", "sfx_ui_tick.mp3", "sfx_data_blip.mp3", "sfx_page_turn.mp3",
        "sfx_soft_impact.mp3", "sfx_paper_rustle.mp3", "sfx_stamp_seal.mp3", "sfx_low_boom.mp3",
        "sfx_riser_2s.mp3", "sfx_sub_drop.mp3", "sfx_binder_lock.mp3", "sfx_gavel_knock.mp3",
    ]
    cues = []
    t = 1.2
    i = 0
    while t < total - 2:
        cues.append((LIB / "sfx" / sfx_files[i % len(sfx_files)], t, 0.38 if i % 5 else 0.58))
        t += 6.2 + (i % 4) * 1.7
        i += 1
    for special_t, name, gain in [
        (27, "sfx_sub_drop.mp3", 0.75), (210, "sfx_low_boom.mp3", 0.65), (330, "sfx_stamp_seal.mp3", 0.7),
        (390, "sfx_riser_2s.mp3", 0.6), (540, "sfx_sub_drop.mp3", 0.8), (620, "sfx_gavel_knock.mp3", 0.7),
    ]:
        if special_t < total:
            cues.append((LIB / "sfx" / name, special_t, gain))
    inputs, filters, labels = [], [], []
    for i, (f, t, g) in enumerate(cues):
        inputs += ["-i", str(f)]
        d = int(t * 1000)
        filters.append(f"[{i}:a]volume={g},adelay={d}|{d}[s{i}]")
        labels.append(f"[s{i}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,volume=0.55[sfx]")
    out = tmp / "sfx.m4a"
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[sfx]", "-t", f"{total:.3f}", "-c:a", "aac", "-b:a", "160k", out], f"sfx bed ({len(cues)} cues)")
    return out


def finish(video: Path, narration: Path, music: Path, sfx: Path, out: Path, total: float) -> None:
    amb = LIB / "ambience/amb_institutional_drone.mp3"
    srt = (EPDIR / "08_edit" / "captions.review_proxy.v001.srt").as_posix().replace(":", "\\:")
    style = (
        "FontName=Segoe UI,FontSize=23,PrimaryColour=&H00F5F7FA,OutlineColour=&H00070709,"
        "BackColour=&H80000000,Bold=0,Outline=2,Shadow=1,MarginV=42"
    )
    vf = (
        "eq=contrast=1.07:saturation=1.05:gamma=0.98,"
        f"subtitles='{srt}':force_style='{style}'"
    )
    fc = (
        f"[3:a]atrim=0:{total:.3f},volume=0.06[amb];"
        "[1:a]volume=1.0[vo];[2:a]volume=1.0[mus];[4:a]volume=1.0[sfx];"
        "[vo][mus][amb][sfx]amix=inputs=4:normalize=0:duration=longest:dropout_transition=0,"
        f"alimiter=limit=0.94,afade=t=out:st={max(total-2.0, 1):.3f}:d=2[a]"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp_out = out.with_suffix(".tmp.mp4")
    run([FFMPEG, "-y", "-i", video, "-i", narration, "-i", music, "-stream_loop", "-1", "-i", amb, "-i", sfx,
         "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-vf", vf,
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", tmp_out], "final mix + captions")
    tmp_out.replace(out)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    master_voice = EPM / "06_voice" / "master" / "vc_master_v001.mp3"
    draft_voice = EPDIR / "06_audio" / "draft" / "narration.local_tts.v001.wav"
    narration = master_voice if master_voice.exists() else draft_voice
    if not narration.exists():
        raise FileNotFoundError(narration)
    total = probe_duration(narration)
    EPM.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pd_madoff_v002_") as td:
        tmp = Path(td)
        video = render_visuals(tmp, total)
        music = build_music(tmp, total)
        sfx = build_sfx(tmp, total)
        suffix = "elevenlabs" if narration == master_voice else "local_audio"
        out_media = EPM / "08_edit" / f"madoff_review_v002_{suffix}.mp4"
        finish(video, narration, music, sfx, out_media, total)
    out_repo = EPDIR / "08_edit" / "renders" / "review.proxy.v002.mp4"
    out_repo.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_media, out_repo)
    h = sha256(out_repo)
    qc = {
        "episode_id": EP,
        "render": "08_edit/renders/review.proxy.v002.mp4",
        "sha256": h,
        "duration_seconds": round(probe_duration(out_repo), 3),
        "video": "moving coded noir visuals, Ken Burns motion, citation lower-thirds, burned captions",
        "audio": ("ElevenLabs channel voice + library music + ambience + SFX" if narration == master_voice else "local draft VO + library music + ambience + SFX; ElevenLabs master still pending owner approval"),
        "paid_generation_performed": False,
        "external_upload_performed": False,
        "known_limitations": [
            "Voice is ElevenLabs channel voice." if narration == master_voice else "Voice is still local draft TTS, not channel ElevenLabs master.",
            "Visuals are coded symbolic placeholders, not final SDXL/Runway assets.",
            "Captions are approximate from review proxy timing."
        ],
    }
    (EPDIR / "08_edit" / "renders" / "review.proxy.v002.qc.json").write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"OUT {out_repo}")
    print(f"SHA256 {h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
