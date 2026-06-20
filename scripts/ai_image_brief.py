#!/usr/bin/env python
"""Write the AI-image generation brief (design doc) for an episode's 🎨 shots.

For every shot the plan marks `ai_image`, emit a ready-to-use image prompt + the EXACT save
filename and folder, into episodes/<ep>/04_scenes/ai_prompts.v001.md. The Codex app reads this,
generates each image, and saves it to <media>/assets/ai/<slug>/<spanId>.png. Then re-running
import_to_remotion.py picks those up automatically (they replace the stock placeholders).

Read-only inputs; --write saves the brief.
Usage: .venv/Scripts/python.exe scripts/ai_image_brief.py 9 --write
"""
from __future__ import annotations
import sys, os, json, glob, re, tempfile, math
from typing import Any

SECONDS_PER_IMAGE = 4.5  # cut to a new image ~every 4.5s -> dynamic; long spans need several images
# Distinct angles so the multiple images of one span differ (real-coverage feel, not a repeat).
ANGLES = ["wide establishing shot", "close-up detail", "low-angle dramatic shot",
          "overhead top-down view", "soft-focus atmospheric background", "silhouette against light",
          "abstract symbolic composition", "medium shot, shallow focus"]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPDIR = os.path.join(ROOT, "episodes")

STYLE = ("cinematic documentary still, dramatic moody lighting, deep navy-and-black palette with "
         "electric-blue and gold accents, photorealistic, shallow depth of field, 16:9, "
         "ultra high resolution 4K, masterpiece quality, razor-sharp focus, exquisite fine detail")
SAFETY = ("No on-screen text or captions, no watermark, no logos, and no identifiable real person "
          "(symbolic / representative only).")
_JARGON = ("symbolic", "rights-clean", "ai-disclosed", "disclosed", "no real", "no face", "motif",
           "remotion", "verbatim", "stock", "placeholder", "censor", "blur", "no readable", "no brand")


def resolve_ep(arg: str) -> str:
    if os.path.isdir(os.path.join(EPDIR, arg)):
        return arg
    hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"PD-*-{int(arg):03d}-*"))] if arg.isdigit() else []
    if not hits:
        hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"*{arg}*")) if os.path.isdir(p)]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"Could not resolve episode '{arg}'. Matches: {hits}")


def slug_of(ep_id: str) -> str:
    parts = ep_id.split("-", 3)
    return parts[3] if len(parts) > 3 else ep_id


def clean(visual_intent: str) -> str:
    s = re.sub(r"\([^)]*\)", " ", visual_intent or "")     # drop production notes
    parts = re.split(r"[;—]", s)
    keep = [p.strip() for p in parts if p.strip() and not any(j in p.lower() for j in _JARGON)]
    out = "; ".join(keep) if keep else s.strip()
    return re.sub(r"\s+", " ", out).strip(" .;")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:]
    write = "--write" in argv
    pos = [a for a in argv if not a.startswith("--")]
    if not pos:
        raise SystemExit("usage: ai_image_brief.py <episode> [--write]")
    ep = resolve_ep(pos[0])
    ep_id = os.path.basename(ep)
    slug = slug_of(ep_id)
    shotlist = json.load(open(os.path.join(EPDIR, ep, "04_scenes", "shotlist.v001.json"), encoding="utf-8"))
    ann = json.load(open(os.path.join(EPDIR, ep, "03_script", "script.annotated.v001.json"), encoding="utf-8"))
    text = {s["span_id"]: s.get("text", "") for s in ann["spans"]}
    try:
        subject = json.load(open(os.path.join(EPDIR, ep, "00_topic", "topic.v001.json"), encoding="utf-8")).get("subject", ep_id)
    except Exception:
        subject = ep_id
    save_dir = f"H:\\pd-media\\assets\\ai\\{slug}\\"

    ai_shots = [s for s in shotlist["shots"] if s["suggested_asset_type"] == "ai_image"]
    counts = {s["span_id"]: max(1, math.ceil(s["estimated_seconds"] / SECONDS_PER_IMAGE)) for s in ai_shots}
    total = sum(counts.values())
    lines = [f"# AI画像 生成リスト（設計書） — {ep_id}", "",
             f"題材: {subject}", "",
             f"**保存先フォルダ（必ずここに保存）**: `{save_dir}`",
             f"各画像を **指定のファイル名** で上のフォルダに保存すること。保存後 `import_to_remotion.py {pos[0]} --write` を回すと、各場面へ自動で入る（仮の写真と差しかわる）。",
             "フォルダが無ければ作成可。PNG推奨・1920x1080以上。",
             "", "**全画像 共通スタイル**:",
             f"> {STYLE}. {SAFETY}",
             "", f"**生成枚数: {total} 枚**（🎨 {len(ai_shots)} 場面 ぶん。長い場面は約6秒ごとに切り替えるため複数枚＝下記の連番で）。", ""]
    for s in ai_shots:
        sid = s["span_id"]
        subj = clean(s.get("visual_intent", "")) or (s.get("on_screen_text") or [""])[0] or " ".join(text.get(sid, "").split()[:14])
        n = counts[sid]
        lines.append(f"## {sid}  〜{s['estimated_seconds']:.0f}秒  → {n}枚")
        lines.append(f"- 場面: 「{' '.join(text.get(sid, '').split()[:18])}…」")
        if s.get("on_screen_text"):
            lines.append(f"- テロップ: {s['on_screen_text'][0]}")
        for i in range(n):
            fname = f"{sid}.png" if i == 0 else f"{sid}_{i + 1:02d}.png"
            angle = ANGLES[i % len(ANGLES)]
            lines.append(f"  - `{fname}` ← {subj}, {angle}")
        lines.append("")

    out = os.path.join(EPDIR, ep, "04_scenes", "ai_prompts.v001.md")
    print(f"{ep_id}: 🎨 {len(ai_shots)} prompts -> 04_scenes/ai_prompts.v001.md  (save to {save_dir})")
    if write:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(out), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        os.replace(tmp, out)
        print(f"WROTE {os.path.relpath(out, ROOT)}")
    else:
        print("(dry-run) pass --write to save")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
