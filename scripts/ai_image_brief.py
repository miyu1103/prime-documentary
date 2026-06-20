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
import sys, os, json, glob, re, tempfile
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPDIR = os.path.join(ROOT, "episodes")

STYLE = ("cinematic documentary still, dramatic moody lighting, deep navy-and-black palette with "
         "electric-blue and gold accents, photorealistic, highly detailed, shallow depth of field, 16:9")
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
    lines = [f"# AI画像 生成リスト（設計書） — {ep_id}", "",
             f"題材: {subject}", "",
             f"**保存先フォルダ（必ずここに保存）**: `{save_dir}`",
             f"各画像を **指定のファイル名** で上のフォルダに保存すること。保存後 `import_to_remotion.py {pos[0]} --write` を回すと、各場面へ自動で入る（仮の写真と差しかわる）。",
             "フォルダが無ければ作成可。PNG推奨・1920x1080以上。",
             "", "**全画像 共通スタイル**:",
             f"> {STYLE}. {SAFETY}",
             "", f"生成枚数: {len(ai_shots)} 枚（🎨の場面ぶん）。1場面に複数欲しいときは `<ID>_02.png` のように連番で追加可。", ""]
    for s in ai_shots:
        sid = s["span_id"]
        subj = clean(s.get("visual_intent", "")) or (s.get("on_screen_text") or [""])[0] or " ".join(text.get(sid, "").split()[:14])
        prompt = f"{subj}. {STYLE}. {SAFETY}"
        lines.append(f"## {sid}  → 保存名 `{sid}.png`")
        lines.append(f"- 場面: 「{' '.join(text.get(sid, '').split()[:18])}…」")
        if s.get("on_screen_text"):
            lines.append(f"- テロップ: {s['on_screen_text'][0]}")
        lines.append(f"- **プロンプト**: {prompt}")
        lines.append(f"- 保存先: `{save_dir}{sid}.png`")
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
