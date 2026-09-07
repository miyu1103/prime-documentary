# P01 EVIDENCE REPORT — PD-2026-009-timbs (candidate A)

- Phase `P01`（Baseline保存・紙芝居診断） / by `claude-code` / 2026-07-12 (JST)
- 非破壊。install/download/H:書込/git変更/remotion変更 は **なし**。既存 ffmpeg/ffprobe のみ使用（新ツール導入なし）。

## 1. 完了状態
- P01 = **candidate_complete**（`current_phase=P01` 不変。P02 へ進めていない）。
- P00→P01 前進は owner「go」承認により `phase_gate.py advance --to P01 --human-approved`（代理実行）。

## 2. 成果物
- `outputs/pd-visual-system/PD-2026-009-timbs/baseline/baseline_A.mp4`（1920×1080/30fps/80.4s/sha `598c6dea…ed63`）
- `.../render_manifest.json`（再現可能な抽出manifest：原本sha `d6d1cc4d…e69f`・区間110.1–190.5s・コマンド）
- `.../baseline_shots.json`（visual question・start/end state・8軸・実測値）
- `docs/pd-visual-system/BASELINE_DIAGNOSIS.md`（診断）

## 3. 実行コマンドと出力（証拠）
```
phase_gate advance --to P01 --human-approved   → Advanced P00 -> P01
phase_gate assert --phase P01                  → OK: P01 is current; status=not_started
phase_gate start  --phase P01                  → Started P01
ffmpeg -n -ss 110.1 -to 190.5 -i <H:原本> -c:v libx264 -crf16 -preset medium ... baseline_A.mp4  → EXIT0
ffprobe baseline_A.mp4                          → 1920x1080 30/1fps 2412f 80.4s 57,523,331B
ffmpeg freezedetect=n=-50dB:d=0.7               → freeze 13.433–25.2s (計 11.77s)
ffmpeg select='gt(scene,0.30)' 数               → 29 cuts
ffmpeg tblend=difference+signalstats YAVG平均    → overall 2.269 / SPN-0005 5.491 / SPN-0006 0.872 / SPN-0007 0.625
```

## 4. 主要発見
- 主役A `SPN-0006`（$10,000 vs $42,000・motion_graphic）が **motion YAVG=0.872＝ほぼ静止**。`SPN-0007` ken_burns=0.625。カット密度は十分(29)。
- ＝「density緑でも紙芝居」の実数裏付け（[[feedback_animation_still_too_little]] / [[feedback_perceptual_motion_and_verify]]）。8軸合計 51/96(53%)。

## 5. 保護・rollback
- H:原本・remotion/**・episodes/**・.git 未変更。出力は outputs/pd-visual-system のみ。
- rollback: outputs baseline/* と診断/証拠を削除、PHASE_STATE/IMPLEMENTATION_STATUS を P01 開始前へ。

## 6. 判定
- **Go(P02) 候補**：baseline 保存・8軸採点・改善対象特定まで完了。次は P02（`pd-phase-02-benchmark`）で参照ショットの目標値化。**P02 着手は owner 承認が前提**。
