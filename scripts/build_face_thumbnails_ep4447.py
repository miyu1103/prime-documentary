#!/usr/bin/env python3
r"""EP44-47 EMOTIVE FACE thumbnails -- CTR_PLAYBOOK.v001 sec 4A, 2-stage face recipe.

Matches the EP42 "young" face proof look:
  face pushed to the RIGHT third (~55-60% frame, eyes on the upper-third line), dark cool
  blurred background, warm rim-lit face, clean dark NEGATIVE SPACE on the left for text,
  Anton ALL-CAPS headline with a thick black stroke (RED bar OR white + one YELLOW shock
  word), a small kicker chip top-left, the PD logo bottom-right on a dark chip. 1280x720.

PROVEN 2-STAGE FACE RECIPE (the likeness firewall):
  Stage 1  JuggernautXL (photoreal) txt2img -> a cinematic portrait, subject on the right,
           dark cool bg, warm rim light, second object baked into the scene.
  Stage 2  DreamShaperXL img2img, denoise ~0.55 -> semi-painterly / illustrative render so
           the face reads as a DRAMATIZED NON-REAL character, never a photoreal likeness of
           the real defendant/victim.  R2 likeness guardrail satisfied.

All four faces are AI-generated generic characters. EP46 tlo uses a deliberately generic,
clearly-illustrative older teen (ad-safety: no resemblance to any identifiable real minor).

    py -3.11 scripts/build_face_thumbnails_ep4447.py [ep_slug ...] [--seeds N]
"""
from __future__ import annotations

import base64
import io
import json
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ImageStat


def _post(path, payload):
    req = urllib.request.Request(
        f"{API}{path}", data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read().decode())

ROOT = Path(__file__).resolve().parents[1]
API = "http://127.0.0.1:7860"
JUGG = "juggernautXL_ragnarokBy.safetensors [dd08fa32f9]"
DREAM = "dreamshaperXL_alpha2Xl10.safetensors [0f1b80cfe8]"

W, H = 1280, 720
GEN_W, GEN_H = 1216, 832  # SDXL landscape, fit -> 16:9

FONT_ANTON = str(ROOT / "remotion" / "public" / "fonts" / "Anton.ttf")
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
LOGO = ROOT / "remotion" / "public" / "pd_logo.png"

WHITE = (247, 249, 252)
YELLOW = (255, 209, 41)     # shock word
RED = (211, 40, 40)         # urgency bar
INK = (8, 12, 20)
CLAMP_LUMA = 190.0
MAX_BYTES = 2 * 1024 * 1024

STYLE1 = ("cinematic character portrait, dramatic low-key lighting, warm golden rim light "
          "tracing the face and shoulders, deep teal and navy blurred background, strong "
          "shallow depth of field, moody film still, volumetric haze, high detail, 85mm, "
          "subject framed on the RIGHT side of the frame, large empty dark negative space "
          "on the LEFT side, head and shoulders, face in the upper third")
STYLE2 = ("semi-painterly cinematic digital illustration, dramatic concept-art render, "
          "painterly brushwork, illustrative, stylized non-photographic, matte painting, "
          "cinematic color grade")
NEG = ("text, letters, words, watermark, signature, logo, caption, subtitle, frame, border, "
       "extra fingers, deformed hands, mutated, extra limbs, lowres, jpeg artifacts, blurry face, "
       "disfigured, bad anatomy, cloned face, split frame, collage, nsfw, nudity, "
       "specific real celebrity, recognizable real politician")

# slug -> (seed_base, subject_prompt, [text spec])
EPS = {
    "PD-2026-044-tekoh": dict(
        seed=44144,
        subject=("a Black man in his mid-30s sitting under a single harsh interrogation lamp "
                 "in a bare dark interrogation room, quiet controlled anger and disbelief on "
                 "his face, jaw set, brow tense, eyes glistening, looking slightly off to the "
                 "side away from the camera, hard overhead key light, cold shadows, a plain "
                 "steel table edge in the foreground"),
        kicker="THEY SKIPPED YOUR RIGHTS",
        lines=[("NO WARNING", WHITE), ("CAN'T SUE", YELLOW)],
        redbar=False, accent=YELLOW,
    ),
    "PD-2026-045-cleveland": dict(
        seed=45611,
        subject=("a distressed African American woman in her late 30s standing close on the right "
                 "side of the frame just inside a jail cell, her face clearly visible and lit, "
                 "cold steel bars beside her and one bar in front of her shoulder, one hand "
                 "gripping a bar, tears on her face, fear and helplessness, looking off to the "
                 "side away from the camera, dim blue jail light, the vertical steel bars catching "
                 "a cold rim light, her face not covered by the bars"),
        neg_extra="bars across the face, obscured face, hidden face",
        zoom=1.06, cx=0.72, cy=0.44,
        kicker="DEBTORS' PRISON",
        lines=[("JAILED FOR", WHITE), ("BEING POOR", WHITE)],
        redbar=True, accent=RED,
    ),
    "PD-2026-046-tlo": dict(
        seed=46330,
        subject=("a generic fictional older teenage high-school student, clearly stylized and "
                 "illustrative, anxious and violated expression, worried wide eyes, standing at a "
                 "row of metal school lockers clutching an open backpack, one locker open beside "
                 "them, looking off to the side away from the camera, dim cool school hallway, "
                 "fully clothed in a plain hoodie, non-sexual, ambiguous generic face"),
        kicker="NO WARRANT NEEDED",
        lines=[("SEARCHED", WHITE), ("AT SCHOOL", WHITE)],
        redbar=False, accent=YELLOW,
    ),
    "PD-2026-047-atwater": dict(
        seed=47820,
        subject=("an ordinary frightened civilian woman in her mid-30s wearing a plain casual "
                 "beige cardigan over a t-shirt, being arrested, her wrists locked in steel "
                 "handcuffs behind her back, a uniformed police officer standing behind her "
                 "gripping her upper arm, she has wide disbelieving eyes and a shocked open "
                 "mouth, humiliation and disbelief, looking off to the side away from the camera, "
                 "night, cold blue and red patrol-car light bokeh in the dark background; she is "
                 "a civilian, plain clothes, no badge, no uniform on the woman"),
        neg_extra=("police uniform on the woman, badge on the woman, the woman is a police officer, "
                   "epaulettes on the woman, duty belt on the woman, she is a cop"),
        kicker="OVER A $50 FINE",
        lines=[("JAILED OVER", WHITE), ("A SEATBELT", YELLOW)],
        redbar=False, accent=YELLOW,
    ),
    "PD-2026-048-glover": dict(
        seed=48513,
        subject=("a tight cinematic close-up head-and-shoulders portrait of an anxious worried "
                 "civilian man in his late 30s being pulled over at night, his face large and "
                 "clearly visible filling the right side of the frame, wide fearful worried eyes, "
                 "tense jaw, dread and disbelief, cold blue and red patrol-car lights washing over "
                 "his face, warm rim light tracing his cheek and shoulder, looking off to the side "
                 "away from the camera toward the police lights, plain casual shirt, an ordinary "
                 "driver, no uniform, a dark blurred rural roadside and the tail of a pickup truck "
                 "behind him, deep dark negative space on the LEFT"),
        neg_extra=("police uniform on the man, badge on the man, the man is a police officer, "
                   "duty belt, readable license plate, readable text, numbers on screen, "
                   "tiny face, small face, wide shot, full car interior"),
        zoom=1.12, cx=0.66, cy=0.40,
        kicker="THEY RAN YOUR PLATE",
        lines=[("STOPPED FOR", WHITE), ("A NAME", YELLOW)],
        redbar=False, accent=YELLOW,
    ),
    "PD-2026-050-centralpark": dict(
        seed=50219,
        subject=("a generic fictional teenage boy, clearly stylized and illustrative, NOT a real "
                 "person and not resembling any specific individual, frightened and exhausted, "
                 "glassy eyes welling with tears, sitting alone under a single harsh cold "
                 "interrogation lamp in a bare dark interrogation room, a bare steel table edge in "
                 "the foreground, hard overhead cold cyan key light, deep teal and navy shadows, "
                 "head and shoulders framed on the right side of the frame, face in the upper "
                 "third, ambiguous non-specific generic young face, dramatized non-real character, "
                 "deep dark negative space on the LEFT"),
        neg_extra=("photoreal likeness of a real person, recognizable individual, celebrity, "
                   "documentary photo, tiny face, huge face filling the frame, wide shot"),
        zoom=1.04, cx=0.66, cy=0.40,
        kicker="CENTRAL PARK, 1989",
        lines=[("5 CONFESSIONS", WHITE), ("0 EVIDENCE", (65, 190, 220))],
        redbar=False, accent=(47, 159, 196),
    ),
}


def b64_to_img(b):
    return Image.open(io.BytesIO(base64.b64decode(b))).convert("RGB")


def img_to_b64(im):
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def txt2img(prompt, seed, neg_extra=""):
    payload = {
        "prompt": prompt, "negative_prompt": NEG + (", " + neg_extra if neg_extra else ""),
        "width": GEN_W, "height": GEN_H, "steps": 34, "cfg_scale": 6.5,
        "sampler_name": "DPM++ 2M", "seed": seed,
        "override_settings": {"sd_model_checkpoint": JUGG},
        "override_settings_restore_afterwards": False,
    }
    return b64_to_img(_post("/sdapi/v1/txt2img", payload)["images"][0])


def img2img(init_img, prompt, seed, neg_extra=""):
    payload = {
        "init_images": [img_to_b64(init_img)], "denoising_strength": 0.55,
        "prompt": prompt, "negative_prompt": NEG + (", " + neg_extra if neg_extra else ""),
        "width": GEN_W, "height": GEN_H, "steps": 32, "cfg_scale": 6.5,
        "sampler_name": "DPM++ 2M", "seed": seed + 7,
        "override_settings": {"sd_model_checkpoint": DREAM},
        "override_settings_restore_afterwards": False,
    }
    return b64_to_img(_post("/sdapi/v1/img2img", payload)["images"][0])


def two_stage(subject, seed, neg_extra=""):
    p1 = f"{subject}, {STYLE1}"
    p2 = f"{subject}, {STYLE2}, {STYLE1}"
    stage1 = txt2img(p1, seed, neg_extra)
    stage2 = img2img(stage1, p2, seed, neg_extra)
    return stage2


def clamp_highlights(img):
    px = img.load()
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            L = 0.299 * r + 0.587 * g + 0.114 * b
            if L > CLAMP_LUMA:
                s = CLAMP_LUMA / L
                px[x, y] = (int(r * s), int(g * s), int(b * s))
    return img


def left_scrim(img, width_frac=0.50, strength=210):
    """Feathered dark-cool gradient over the left side -> clean negative space for text."""
    grad = Image.new("L", (W, H), 0)
    gd = grad.load()
    edge = int(W * width_frac)
    for x in range(W):
        if x < edge:
            gd0 = int(strength * (1 - (x / edge) ** 1.5))
        else:
            gd0 = 0
        for y in range(H):
            gd[x, y] = gd0
    grad = grad.filter(ImageFilter.GaussianBlur(24))
    dark = Image.new("RGB", (W, H), INK)
    return Image.composite(dark, img, grad)


def subject_luma(img):
    """Mean luma of the RIGHT 45% (the face) -- want it bright/rim-lit."""
    crop = img.crop((int(W * 0.55), int(H * 0.15), W, int(H * 0.95))).convert("L")
    return ImageStat.Stat(crop).mean[0]


def draw_kicker(d, text, x, y, accent):
    kf = ImageFont.truetype(FONT_BOLD, 30)
    tw = d.textlength(text, font=kf)
    d.rectangle([x - 14, y - 10, x + tw + 14, y + 40], fill=(6, 10, 18))
    d.text((x, y), text, font=kf, fill=WHITE, stroke_width=2, stroke_fill=(0, 0, 0))
    d.rectangle([x - 14, y + 44, x - 14 + tw + 28, y + 52], fill=accent)


def headline(img, spec):
    d = ImageDraw.Draw(img)
    MX = 60
    max_w = int(W * 0.50)
    lines = spec["lines"]
    # auto-fit Anton
    size = 168
    while size > 96:
        f = ImageFont.truetype(FONT_ANTON, size)
        widest = max(d.textlength(t, font=f) for t, _ in lines)
        if widest <= max_w:
            break
        size -= 4
    f = ImageFont.truetype(FONT_ANTON, size)
    asc, desc = f.getmetrics()
    adv = int((asc + desc) * 0.86)
    block_h = len(lines) * adv
    top = (H - block_h) // 2 + 14
    # kicker above the block
    draw_kicker(d, spec["kicker"], MX + 4, top - 74, spec["accent"])
    y = top
    stroke = max(10, size // 9)
    for text, color in lines:
        if spec["redbar"]:
            tw = d.textlength(text, font=f)
            d.rectangle([MX - 12, y + int(desc * 0.55), MX + tw + 22, y + adv - int(desc * 0.15)], fill=RED)
            d.text((MX, y), text, font=f, fill=WHITE, stroke_width=4, stroke_fill=(90, 0, 0))
        else:
            d.text((MX, y), text, font=f, fill=color, stroke_width=stroke, stroke_fill=(0, 0, 0))
        y += adv
    if not spec["redbar"]:
        d.rectangle([MX + 2, y + 4, MX + 2 + int(max_w * 0.62), y + 20], fill=spec["accent"])
    return img


def place_logo(img):
    if not LOGO.exists():
        return img
    lg = Image.open(LOGO).convert("RGBA")
    lw = 120
    lg = lg.resize((lw, int(lg.height * lw / lg.width)))
    lx, ly = W - lw - 34, H - lg.height - 28
    chip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(chip)
    pad = 15
    cd.rounded_rectangle([lx - pad, ly - pad, lx + lw + pad, ly + lg.height + pad],
                         radius=16, fill=(4, 6, 12, 195))
    img = Image.alpha_composite(img.convert("RGBA"), chip).convert("RGB")
    img.paste(lg, (lx, ly), lg)
    return img


def compose(face_img, spec):
    # zoom-crop toward the subject (right third, face on upper third) so the face reads big
    z = spec.get("zoom", 1.24)
    sw, sh = face_img.size
    cw, ch = int(sw / z), int(sh / z)
    cx, cy = int(sw * spec.get("cx", 0.66)), int(sh * spec.get("cy", 0.42))
    l = max(0, min(sw - cw, cx - cw // 2))
    t = max(0, min(sh - ch, cy - ch // 2))
    face_img = face_img.crop((l, t, l + cw, t + ch))
    img = ImageOps.fit(face_img, (W, H), method=Image.LANCZOS, centering=(0.62, 0.40))
    img = ImageEnhance.Contrast(img).enhance(1.06)
    img = ImageEnhance.Color(img).enhance(1.08)
    img = clamp_highlights(img)
    img = left_scrim(img)
    img = headline(img, spec)
    img = place_logo(img)
    return img


def save_under_cap(img, dst):
    for edge in (1280, 1180, 1080, 980, 880):
        im = img.resize((edge, int(H * edge / W)), Image.LANCZOS) if edge != W else img
        im.save(dst, format="PNG", optimize=True)
        if dst.stat().st_size <= MAX_BYTES:
            return edge, dst.stat().st_size
    return edge, dst.stat().st_size


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    seeds = 2
    argv = sys.argv[1:]
    if "--seeds" in argv:
        i = argv.index("--seeds")
        seeds = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    slugs = args or list(EPS.keys())
    scratch = Path(r"C:\Users\aab15\AppData\Local\Temp\claude\C--Users-aab15-OneDrive-Desktop\2fa81074-5db3-40a1-8cda-403c929c15de\scratchpad")
    scratch.mkdir(parents=True, exist_ok=True)
    for slug in slugs:
        spec = EPS[slug]
        print(f"\n=== {slug} ===", flush=True)
        best, best_luma = None, -1
        for i in range(seeds):
            sd = spec["seed"] + i * 101
            t0 = time.time()
            face = two_stage(spec["subject"], sd, spec.get("neg_extra", ""))
            lum = subject_luma(face)
            print(f"  seed {sd}: subject_luma={lum:.1f}  ({time.time()-t0:.0f}s)", flush=True)
            face.save(scratch / f"{slug}_raw_seed{sd}.png")
            if lum > best_luma:
                best, best_luma = face, lum
        comp = compose(best, spec)
        pkg = ROOT / "episodes" / slug / "09_package"
        pkg.mkdir(parents=True, exist_ok=True)
        out = pkg / "thumbnail.face.v001.png"
        edge, nbytes = save_under_cap(comp, out)
        # preview copy in scratch for eyeballing
        comp.save(scratch / f"{slug}_composite.png")
        print(f"  -> {out}  ({edge}px, {nbytes/1024:.0f} KB, subject_luma={best_luma:.1f})", flush=True)


if __name__ == "__main__":
    main()
