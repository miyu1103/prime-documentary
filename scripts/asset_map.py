#!/usr/bin/env python
"""Write a human-readable asset map for an episode: which visual(s) each span uses.

Reads the generated rough-cut data (remotion/src/data/<slug>_roughcut.ts), the annotated script
(for the narration line of each span), and the rights ledger + shared library (for what each file
depicts). Emits episodes/<ep>/04_scenes/asset_map.v001.md so a human/Codex can see, scene by
scene, the planned footage and swap anything off-topic. Read-only inputs; --write saves the .md.

Usage:
  .venv/Scripts/python.exe scripts/asset_map.py 9 --write
"""
from __future__ import annotations
import sys, os, json, glob, tempfile
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPDIR = os.path.join(ROOT, "episodes")
DATA = os.path.join(ROOT, "remotion", "src", "data")

# Per-shot directive so Codex knows: USE the downloaded asset, or GENERATE its own AI image.
PLAN = {
    "stock_video": "✅ 既存の実写動画を使う（下の素材／ダウンロード済み）",
    "stock_image": "✅ 既存の写真を使う（下の素材／ダウンロード済み）",
    "archival_pd": "✅ 既存の資料/写真を使う（ダウンロード済み）",
    "ai_image": "🎨 Codexが画像を生成（下の写真は“仮置き”。AIで作って差しかえる）",
    "motion_graphic": "🔤 文字グラフィック（Remotionのテロップ。素材不要）",
}


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


def load_data(slug: str) -> dict[str, Any] | None:
    p = os.path.join(DATA, f"{slug}_roughcut.ts")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8").read()
    return json.loads(t[t.index("= {") + 2: t.rindex("}") + 1])


def depicts_index(ep: str) -> dict[str, str]:
    idx: dict[str, str] = {}
    sources = [os.path.join(EPDIR, ep, "05_stock", "stock_ledger.v001.json"),
               os.path.join(ROOT, "references", "stock_manifest.json")]
    for sp in sources:
        if not os.path.exists(sp):
            continue
        data = json.load(open(sp, encoding="utf-8"))
        items = data["assets"] if isinstance(data, dict) and "assets" in data else data
        for a in items:
            bn = os.path.basename(a.get("file") or a.get("uri") or "")
            if bn:
                idx[bn] = a.get("depicts") or a.get("query") or a.get("attribution") or ""
    return idx


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    argv = sys.argv[1:]
    write = "--write" in argv
    pos = [a for a in argv if not a.startswith("--")]
    if not pos:
        raise SystemExit("usage: asset_map.py <episode> [--write]")
    ep = resolve_ep(pos[0])
    ep_id = os.path.basename(ep)
    slug = slug_of(ep_id)
    data = load_data(slug)
    if not data:
        raise SystemExit(f"no rough-cut data for {ep_id}; run import_to_remotion.py {pos[0]} --write first")
    ann = json.load(open(os.path.join(EPDIR, ep, "03_script", "script.annotated.v001.json"), encoding="utf-8"))
    span_text = {s["span_id"]: s.get("text", "") for s in ann["spans"]}
    span_chapter = {sp: c["chapter_id"] for c in ann["chapters"] for sp in c["span_ids"]}
    dep = depicts_index(ep)

    def label(src: str) -> str:
        bn = os.path.basename(src)
        d = dep.get(bn, "")
        return f"{bn}" + (f" — {d}" if d else "")

    cnt = {"generate": 0, "use": 0, "text": 0}
    for sh in data["shots"]:
        cnt["generate" if sh["assetType"] == "ai_image" else "text" if sh["assetType"] == "motion_graphic" else "use"] += 1
    lines = [f"# 素材マップ — {ep_id}", "",
             f"各場面（スパン）に、どの映像・写真を使うか／Codexが何を生成するかの一覧。タイトル「{data.get('title','')}」。", "",
             "**Codexへ — 担当の見方**",
             "- ✅ = 既にダウンロード済みの素材を使う（下に列挙）。",
             "- 🎨 = **Codexが画像を生成**する場面（今は仮の写真が入っているので、AIで作って差しかえる）。",
             "- 🔤 = 文字グラフィック（素材不要、Remotionのテロップ）。",
             "",
             f"**この話の内訳**：🎨生成 {cnt['generate']} 場面 ／ ✅既存素材 {cnt['use']} 場面 ／ 🔤文字 {cnt['text']} 場面。",
             "※自動で選んだ仮の割り当てです。合わないものは差しかえてOK（動画=複数を数秒ずつ切替／写真=Ken Burnsで動かす）。", ""]
    for sh in data["shots"]:
        sid = sh["spanId"]
        ch = span_chapter.get(sid, "")
        words = " ".join(span_text.get(sid, "").split()[:14])
        lines.append(f"## {sid}  [{ch}]  〜{sh['seconds']:.0f}秒")
        lines.append(f"- 担当: {PLAN.get(sh['assetType'], sh['assetType'])}")
        if words:
            lines.append(f"- ナレ: 「{words}…」")
        if sh.get("telop"):
            lines.append(f"- テロップ: {sh['telop'][0]}")
        vis = []
        if sh.get("clips"):
            vis += [f"🎬 {label(c['src'])}" for c in sh["clips"]]
        if sh.get("images"):
            vis += [f"🖼 {label(s)}" for s in sh["images"]]
        if not vis and sh.get("src"):
            vis = [label(sh["src"])]
        tag = "仮置き写真（AIで生成して差しかえ）" if sh["assetType"] == "ai_image" else "使う素材"
        lines.append(f"- {tag}: " + ("、".join(vis) if vis else "（文字カード）"))
        lines.append("")

    out = os.path.join(EPDIR, ep, "04_scenes", "asset_map.v001.md")
    text = "\n".join(lines)
    print(f"{ep_id}: {len(data['shots'])} 場面 -> 04_scenes/asset_map.v001.md")
    if write:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(out), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, out)
        print(f"WROTE {os.path.relpath(out, ROOT)}")
    else:
        print("(dry-run) pass --write to save")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
