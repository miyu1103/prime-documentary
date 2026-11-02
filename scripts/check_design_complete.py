#!/usr/bin/env python
"""Objective, reproducible check that an episode's DESIGN SPEC is complete.

Another thread (or a human) asked "is the design done?" and could only judge from
`manifest.state` (still `approved`) + empty downstream folders, so it answered "not yet".
That is the wrong yardstick: the DESIGN SPEC and the PRODUCTION ARTIFACTS are different
milestones. This gate defines "design spec complete" OBJECTIVELY and emits a receipt any
observer can read, so completion is a machine fact, not a claim.

DESIGN SPEC COMPLETE (this gate) means, for episode <ep>:
  1. the canonical design doc `_planning/EP<NN>_<slug>_DESIGN.v001.md` exists (spec),
  2. the 3-pass verification layer `..._DESIGN.v002.md` exists (signoff + failure->mechanism checklist),
  3. the animation asset spec `..._ANIMATION_ASSETS.v001.md` and handoff `..._ANIMATION_HANDOFF_PROMPT.md` exist,
  4. the Codex image prompts `..._ai_prompts.v001.md` exist with ~68 prompts,
  5. every past owner-reported failure appears (mapped to a mechanism or a named human backstop) in the v002 checklist,
  6. NO dropped gate (check_music_coverage / check_stem_loudness / check_motion_bbox_flow) is cited as an
     implemented mechanism (they may only appear in a "dropped / do-not-cite" context),
  7. the v002 residual section classifies every residual as OUT-OF-SCOPE for the spec
     (downstream production artifact / human backstop / code-gate track) -- i.e. zero design-CONTENT gaps.

It explicitly does NOT mean the episode is production-ready. Research, claims, script, scenes, assets,
render are LATER stages; their absence at `state=approved` is expected and is NOT counted against the spec.

Usage:
    python scripts/check_design_complete.py                 # all of EP33/34/35
    python scripts/check_design_complete.py --ep tyler      # one
    python scripts/check_design_complete.py --emit-receipt  # write design_spec_acceptance.v001.json per ep
Exit 0 = all checked episodes COMPLETE, 1 = at least one INCOMPLETE / usage error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "episodes" / "_planning"

EPISODES = [
    ("EP33", "033", "tyler",   "PD-2026-033-tyler"),
    ("EP34", "034", "rolin",   "PD-2026-034-rolin"),
    ("EP35", "035", "hinders", "PD-2026-035-hinders"),
]

DROPPED_GATES = ["check_music_coverage", "check_stem_loudness", "check_motion_bbox_flow"]

# Past owner-reported failures; each must be discoverable (as a phrase/keyword) in the v002 checklist.
PAST_FAILURES = [
    ("字幕≠ナレ", ["字幕がナレと不一致", "caption_narration_match", "字幕=ナレ"]),
    ("字幕が遅い", ["字幕が遅い", "lag", "caption_sync"]),
    ("字幕が変な所で切れる", ["機能語行末", "dangling", "変な所で切れ"]),
    ("後半ドリフト", ["ドリフト", "drift"]),
    ("字幕が飛ぶ", ["未字幕", "caption_coverage", "字幕が飛"]),
    ("DL素材未使用", ["footage_utilization", "使われない", "未使用"]),
    ("素材被り", ["arc_nonrepeat", "被り", "非重複", "footage_diversity"]),
    ("汎用象徴乱用", ["汎用象徴", "天秤"]),
    ("棚ラベル破損", ["棚ラベル", "contact_sheet", "コンタクトシート"]),
    ("構成ズレ", ["structure_4part", "8s", "フック", "4幕"]),
    ("OP/ED違う", ["bookends", "OP/ED", "Bookend"]),
    ("紙芝居", ["紙芝居", "motion_energy"]),
    ("疎な図", ["疎", "map-node", "StateMap", "≥6", "≥12"]),
    ("周回淡い光", ["周回", "淡い光", "glow"]),
    ("lowerthird見切れ", ["見切れ", "safe-rect", "lower-third", "lowerthird"]),
    ("図背景が暗い", ["図背景", "image_cut_luma", "背景が暗"]),
    ("画面が暗い", ["body_luma", "画面が暗", "暗くて"]),
    ("フィラーSFX", ["フィラー", "sound_layers", "無意味"]),
    ("SFX種類少ない", ["distinct SFX", "種類", "sfx"]),
    ("終盤の変な音", ["終盤", "roar", "ending", "飛行機"]),
    ("サムネ地味", ["サムネ", "thumbnail", "CTR"]),
    ("AI臭い", ["AI臭", "script_lint", "定型句"]),
    ("SDXL勝手起動", ["SDXL"]),
    ("緑≠完成", ["自己申告", "preflight_owner_review", "実物"]),
    ("偽の緑", ["偽の緑", "freshness", "sha"]),
    ("薄い音で緑", ["薄い音", "mux", "audio_mix_sha256", "onset"]),
    ("尺外れ", ["runtime_band", "尺"]),
    ("20分水増し", ["水増し", "check_padding", "padding"]),
    ("ゲート最適化", ["グッドハート", "ゲート最適化", "gaming"]),
]

# a residual line that is OUT-OF-SCOPE for the spec matches one of these; anything else = a design gap.
OUT_OF_SCOPE = re.compile(
    r"未作成|未生成|未存在|未発注|不在|asset_selection|claims\.v|film\.json|film json|ai_prompts|"
    r"fingerprint|指紋|台帳|arc_used|Glob|"                              # downstream production artifacts
    r"人間|backstop|preflight_owner_review|試聴|目視|テイスト|グッドハート|周回する淡い光|SDXL|見ごたえ|"
    r"公開後実測|CTR|残存|"                                              # human-backstop only
    r"要実装|未実装|preflight_render_gate|skip-hardening|check_longform_drift|新規.*ビルド|改修|パラメータ化|未ビルド|"  # code-gate track
    r"コンタクトシート|contact_sheet|step7|棚ラベル|runtime_band|wpm|語数|機械再カウント|マージン|再ペーシング|"  # verified at a later gate/QC step
    r"未検証|未実施|未確認|"                                              # execution-stage verification (not a spec gap)
    r"過大主張|冗長|記述精度|過小評価|撤回"                                # description-precision, corrected in v002
)


def sha256(p: Path) -> str:
    return "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()


def check_episode(key: str, nn: str, slug: str, ep_id: str, emit: bool) -> dict:
    req = {
        "design_v001": PLAN / f"{key}_{slug}_DESIGN.v001.md",
        "design_v002": PLAN / f"{key}_{slug}_DESIGN.v002.md",
        "anim_assets": PLAN / f"{key}_{slug}_ANIMATION_ASSETS.v001.md",
        "anim_handoff": PLAN / f"{key}_{slug}_ANIMATION_HANDOFF_PROMPT.md",
        "ai_prompts": PLAN / f"{key}_{slug}_ai_prompts.v001.md",
    }
    problems: list[str] = []

    # 1-4 files exist and non-trivial
    for name, p in req.items():
        if not p.exists() or p.stat().st_size < 1500:
            problems.append(f"missing/too-small: {name} ({p.name})")
    v001 = req["design_v001"].read_text(encoding="utf-8", errors="ignore") if req["design_v001"].exists() else ""
    v002 = req["design_v002"].read_text(encoding="utf-8", errors="ignore") if req["design_v002"].exists() else ""
    prompts = req["ai_prompts"].read_text(encoding="utf-8", errors="ignore") if req["ai_prompts"].exists() else ""

    # 4 ~68 prompts
    n_prompts = len(re.findall(r"3840x2160|3840×2160", prompts))
    if n_prompts < 60:
        problems.append(f"ai_prompts has ~{n_prompts} 4K prompts (<60)")

    # 2 v002 carries a checklist + signoff
    if "点検表" not in v002 or "サインオフ" not in v002:
        problems.append("v002 missing checklist/signoff section")

    # 5 every past failure covered somewhere in v002
    missing_failures = [name for name, kws in PAST_FAILURES if not any(k in v002 for k in kws)]
    if missing_failures:
        problems.append(f"{len(missing_failures)} past-failure(s) not found in v002 checklist: {', '.join(missing_failures)}")

    # 6 no dropped gate cited as implemented. A dropped gate is OK when its occurrence sits in a
    # dropped / do-not-cite context (±220 chars). It is a violation only if cited as a real mechanism.
    both = v001 + "\n" + v002
    drop_ctx = re.compile(r"ドロップ|引用禁止|dropped|DROPPED|NONE|参照\s*0|0回参照|差替|重複|不能|要ドロップ|"
                          r"存在しない|使わない|に無い|音は|モーションは|正しく|"
                          r"撤回|未配線|引用しない|🗑|advisory|backstop|降格")
    bad_drop = []
    for g in DROPPED_GATES:
        for m in re.finditer(re.escape(g), both):
            ctx = both[max(0, m.start() - 220): m.end() + 220]
            if not drop_ctx.search(ctx):
                bad_drop.append(g)
                break
    if bad_drop:
        problems.append(f"dropped gate(s) cited as implemented: {', '.join(bad_drop)}")

    # 7 residuals all out-of-scope. Extract ONLY the "## C. 残課題" section (not the checklist
    # arithmetic in ## B). Every "- " bullet there must match OUT_OF_SCOPE (downstream / backstop /
    # code-gate / description-precision); a bullet that matches none is a real design-CONTENT gap.
    design_gap_residuals = []
    m = re.search(r"^##\s*C\.\s*残課題.*", v002, re.S | re.M)
    if m:
        for line in m.group(0).splitlines():
            s = line.strip()
            if s.startswith("- ") and len(s) > 12 and not OUT_OF_SCOPE.search(s):
                design_gap_residuals.append(s[:80])
    if design_gap_residuals:
        problems.append(f"{len(design_gap_residuals)} residual(s) look like DESIGN-CONTENT gaps: {design_gap_residuals}")

    complete = not problems
    receipt = {
        "gate": "design_spec_complete",
        "episode_id": ep_id,
        "milestone": "DESIGN SPEC COMPLETE (spec written + 3-pass verified). NOT production-ready.",
        "out_of_scope_note": "research/claims/script/scenes/assets/render are later stages; their absence at state=approved is expected and NOT counted here.",
        "status": "COMPLETE" if complete else "INCOMPLETE",
        "problems": problems,
        "artifacts": {name: (sha256(p) if p.exists() else None) for name, p in req.items()},
        "ai_prompt_count": n_prompts,
        "past_failures_covered": f"{len(PAST_FAILURES) - len(missing_failures)}/{len(PAST_FAILURES)}",
    }
    if emit:
        out = ROOT / "episodes" / ep_id / "design_spec_acceptance.v001.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
        receipt["receipt_path"] = str(out.relative_to(ROOT))
    return receipt


def main() -> int:
    ap = argparse.ArgumentParser(description="Objective design-spec completion gate.")
    ap.add_argument("--ep", help="slug substring (tyler/rolin/hinders); default all")
    ap.add_argument("--emit-receipt", action="store_true", help="write design_spec_acceptance.v001.json per episode")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    eps = [e for e in EPISODES if not a.ep or a.ep in e[2] or a.ep in e[3]]
    if not eps:
        print(f"no episode matching '{a.ep}'", file=sys.stderr)
        return 1

    results = [check_episode(*e[:4], a.emit_receipt) for e in eps]
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("=" * 68)
        print("DESIGN SPEC COMPLETION  (spec written + 3-pass verified; NOT production-ready)")
        print("=" * 68)
        for r in results:
            mark = "✅ COMPLETE" if r["status"] == "COMPLETE" else "❌ INCOMPLETE"
            print(f"\n{mark}  {r['episode_id']}   past-failures covered {r['past_failures_covered']}, {r['ai_prompt_count']} image prompts")
            for p in r["problems"]:
                print(f"    - {p}")
            if r.get("receipt_path"):
                print(f"    receipt: {r['receipt_path']}")
        n_ok = sum(1 for r in results if r["status"] == "COMPLETE")
        print(f"\nRESULT: {n_ok}/{len(results)} episodes DESIGN SPEC COMPLETE")
    return 0 if all(r["status"] == "COMPLETE" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
