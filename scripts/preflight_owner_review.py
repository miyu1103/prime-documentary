#!/usr/bin/env python
"""Owner-review bundle: mechanizes the "look/listen as the owner would BEFORE saying done".

The recurring failure was declaring a render "complete" on green gates alone, then the
owner watching it through and finding lag / murk / weird audio in seconds. This produces,
in ONE command, the exact artifacts the owner check needs -- so "完成" is never said until
the real numbers and frames have been put in front of the owner.

Generates under runs/owner_review/<slug>/ :
  1. contact_sheet.png   -- 16 evenly-spaced frames (see the whole film at a glance)
  2. luma.json           -- per-render brightness (median YAVG + dark-frame share)   [F: 明るさ]
  3. caption_sync.json   -- independent caption-timing report (lag/drift/fword)       [A: 字幕]
  4. audio/*.mp3         -- the last 12s + 4 evenly-spaced 6s clips (hear the mix/ending) [B: 音]
  5. SUMMARY.md          -- the numbers + the owner checklist (A字幕/B音/C動き/D素材/E明るさ)

Read-only w.r.t. the episode; writes only under runs/owner_review/. No paid calls.

Usage:
    python scripts/preflight_owner_review.py --ep PD-2026-031-unlock
    python scripts/preflight_owner_review.py --ep tyler --render path/to/final.mp4
"""
from __future__ import annotations

import argparse
import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPISODES = ROOT / "episodes"


def _fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def resolve_episode(arg: str) -> Path:
    p = EPISODES / arg
    if p.is_dir():
        return p
    hits = sorted(d for d in EPISODES.glob("PD-2026-*") if d.is_dir() and arg in d.name)
    if not hits:
        _fail(f"no episode matching '{arg}'")
    return hits[-1]


def resolve_render(epdir: Path, override: str | None) -> Path | None:
    if override:
        return Path(override)
    cands = sorted(epdir.glob("08_edit/renders/*.mp4"), key=lambda p: p.stat().st_mtime)
    finals = [p for p in cands if "final" in p.name.lower()] or cands
    if finals:
        return finals[-1]
    for fd in reversed(sorted(epdir.glob("09_package/final_delivery.v*.json"))):
        d = json.loads(fd.read_text(encoding="utf-8", errors="ignore")) if fd.exists() else {}
        fv = (d or {}).get("final_video")
        if fv:
            return Path(fv.replace("file://", ""))
    return None


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nk=1:nw=1", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def make_contact_sheet(render: Path, dur: float, out: Path, frames: int = 16) -> bool:
    cols = 4
    rows = (frames + cols - 1) // cols
    rate = frames / dur if dur > 0 else 1.0
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-nostats", "-i", str(render),
             "-vf", f"fps={rate},scale=480:-1,tile={cols}x{rows}",
             "-frames:v", "1", str(out)],
            capture_output=True, check=True)
        return out.exists()
    except Exception as exc:  # noqa: BLE001
        print(f"  contact sheet failed: {exc}")
        return False


def luma_report(render: Path, out: Path) -> dict:
    import re
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(render),
         "-vf", "fps=0.5,signalstats,metadata=print:file=-", "-f", "null", "-"],
        capture_output=True, text=True, check=True)
    vals = sorted(float(m) for m in re.findall(r"lavfi\.signalstats\.YAVG=([0-9.]+)",
                                               proc.stdout + proc.stderr))
    rep: dict = {"samples": len(vals)}
    if vals:
        rep.update({
            "median_yavg": round(vals[len(vals) // 2], 1),
            "mean_yavg": round(sum(vals) / len(vals), 1),
            "min_yavg": round(vals[0], 1),
            "frac_below_30": round(sum(1 for v in vals if v < 30) / len(vals), 3),
            "frac_below_40": round(sum(1 for v in vals if v < 40) / len(vals), 3),
            "assessment": ("DARK -- likely hard to see" if vals[len(vals) // 2] < 48
                           else "bright enough"),
        })
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    return rep


def audio_clips(render: Path, dur: float, outdir: Path) -> list[str]:
    outdir.mkdir(parents=True, exist_ok=True)
    made: list[str] = []
    spots = [("ending_last12s", max(0.0, dur - 12.0), 12.0)]
    for i in range(1, 5):
        spots.append((f"clip{i}_{int(dur*i/5)}s", dur * i / 5.0, 6.0))
    for name, ss, ln in spots:
        dest = outdir / f"{name}.mp3"
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-hide_banner", "-nostats", "-ss", f"{ss:.2f}",
                 "-t", f"{ln:.2f}", "-i", str(render), "-vn", "-q:a", "4", str(dest)],
                capture_output=True, check=True)
            if dest.exists():
                made.append(dest.name)
        except Exception:  # noqa: BLE001
            pass
    return made


def caption_sync_report(epdir: Path, out: Path) -> dict:
    _dir = str(Path(__file__).resolve().parent)
    if _dir not in sys.path:
        sys.path.insert(0, _dir)
    try:
        vcs = importlib.import_module("verify_caption_sync")
        r = vcs.evaluate(epdir)
    except Exception as exc:  # noqa: BLE001
        r = {"gate": "caption_sync", "skipped": True, "reason": f"could not run: {exc}"}
    out.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    return r


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate the owner-review bundle before saying done.")
    ap.add_argument("--ep", required=True, help="episode id / slug / substring")
    ap.add_argument("--render", help="explicit final .mp4 (else newest 08_edit/renders/*final*.mp4)")
    ap.add_argument("--frames", type=int, default=16)
    a = ap.parse_args()

    epdir = resolve_episode(a.ep)
    slug = epdir.name.split("-")[-1]
    render = resolve_render(epdir, a.render)
    outdir = ROOT / "runs" / "owner_review" / epdir.name
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"[owner-review] {epdir.name}")
    print(f"  out: {outdir}")

    cap = caption_sync_report(epdir, outdir / "caption_sync.json")
    print(f"  A captions: ", end="")
    if cap.get("skipped"):
        print(f"skipped ({cap.get('reason','')})")
    else:
        print(f"p50 {cap.get('lag_p50'):+.3f}s exact {cap.get('exact_pct',0):.0f}% "
              f"late {cap.get('late_pct',0):.0f}% drift {cap.get('segment_drift',0):+.3f}s "
              f"fword-ends {cap.get('function_word_line_ends',0)} -> {cap.get('verdict')}")

    lu: dict = {}
    cs_ok = False
    clips: list[str] = []
    dur = 0.0
    if render and Path(render).is_file():
        try:
            dur = ffprobe_duration(render)
        except Exception as exc:  # noqa: BLE001
            print(f"  ffprobe failed: {exc}")
        cs_ok = make_contact_sheet(Path(render), dur, outdir / "contact_sheet.png", a.frames)
        print(f"  C contact sheet: {'contact_sheet.png' if cs_ok else 'FAILED'}")
        lu = luma_report(Path(render), outdir / "luma.json")
        print(f"  E brightness: median YAVG {lu.get('median_yavg','?')} "
              f"({lu.get('assessment','?')}), {lu.get('frac_below_40','?')} frames < 40")
        clips = audio_clips(Path(render), dur, outdir / "audio")
        print(f"  B audio clips: {len(clips)} (incl. ending_last12s)")
    else:
        print(f"  render not found (looked in 08_edit/renders and final_delivery) -- "
              f"contact sheet / luma / audio skipped. Pass --render.")

    summary = outdir / "SUMMARY.md"
    lines = [
        f"# Owner review — {epdir.name}", "",
        f"- render: `{render}`" + (f"  ({dur:.0f}s)" if dur else "  (not found)"),
        f"- generated artifacts in `{outdir}`", "",
        "## 実数（自己申告でなく実測）", "",
        "### A 字幕（ぴったり一致が最優先）",
    ]
    if cap.get("skipped"):
        lines.append(f"- caption_sync: skipped — {cap.get('reason','')}")
    else:
        lines += [
            f"- 中央ラグ **{cap.get('lag_p50'):+.3f}s**（0に近いほど良／+は遅い）  exact(|lag|≤0.15s) **{cap.get('exact_pct',0):.0f}%**",
            f"- late(>0.12s) {cap.get('late_pct',0):.0f}%  区間ドリフト {cap.get('segment_drift',0):+.3f}s  機能語行末 {cap.get('function_word_line_ends',0)}",
            f"- verdict: **{cap.get('verdict')}**",
        ]
    lines += ["", "### E 明るさ"]
    if lu:
        lines.append(f"- 中央輝度 **{lu.get('median_yavg')}** / 平均 {lu.get('mean_yavg')} — {lu.get('assessment')}  （40未満の割合 {lu.get('frac_below_40')}）")
    else:
        lines.append("- (render無しで未測定)")
    lines += [
        "", "### B 音", f"- 試聴クリップ {len(clips)}本（`audio/` … 特に `ending_last12s.mp3` の変な音チェック）",
        "", "### C 動き / D 素材", "- `contact_sheet.png` を目視: ①周回光ゼロ ②図/文字が動く ③見切れ/疎/暗すぎ無し ④場違い/被り素材無し",
        "", "## オーナー確認チェックリスト（これを見せてから『完成』と言う）",
        "- [ ] A 字幕がナレとぴったり（中央ラグ ~0・late低・drift無・機能語行末0）",
        "- [ ] B ending含め変な音が無い・音量一定",
        "- [ ] C 図/文字が実際に動く・周回光うざくない",
        "- [ ] D 場違い/被り素材が無い（コンタクトシート目視）",
        "- [ ] E 画面が暗すぎず画像が見える（中央輝度≥48目安）",
        "",
    ]
    summary.write_text("\n".join(lines), encoding="utf-8")
    print(f"  SUMMARY: {summary}")
    print("  -> このバンドルを見せてから『完成』と言うこと（自己申告禁止）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
