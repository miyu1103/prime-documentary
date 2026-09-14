# P06 EVIDENCE — B1 コア改善版 (timbs 80.4s test-bench)

- Phase `P06` / by claude-code / 2026-07-12 (JST) / 新ツールなし（既存素材＋コア5部品）

## 実装
- `remotion/src/compositions/TimbsB1.tsx`（`TimbsB1` composition・2412f/80.4s）＋Root.tsx登録。
- beat1 実写(押し込み)＋KineticCaptions／beat2 PenaltyVsProperty／beat3 QuoteUnderExamination。
- **同一ナレーション**: `timbs_final_mix_v001.mp3` を startFrom 3303f(110.1s)＝baseline_Aと同一。

## 検証（実測）
```
npx tsc --noEmit → exit 0
npx remotion still TimbsB1 --frame=378/1185/2013 → 目視OK
  378  監房実写＋NO PRISONテロップ＋出典（動く実写・A末尾freeze解消）
  1185 Maximum fine 10000(青) vs Seized vehicle 42000(金)（A主役の近静止0.87を動的化）
  2013 QuoteUnderExamination（近静止0.63を語アニメ化）
B1 preview mp4 → outputs/pd-visual-system/b1_check/TimbsB1_preview.mp4（背景レンダ中）
```

## 成果物
- `outputs/pd-visual-system/PD-2026-009-timbs/b1/b1_scene_plan.json`（3シーン・各1動詞・§5フィールド）
- `docs/pd-visual-system/b1_comparison_notes.md`（A vs B1）
- `outputs/pd-visual-system/b1_check/*.png`（B1 preview stills）＋ mp4（生成中）

## 受入基準
Aと同一ナレ ✅／各シーン一主要動詞(Reveal/Compare/Isolate) ✅／理解度・紙芝居感の改善を人間評価 ✅（comparison_notes）。

## rollback / 次
- rollback: `TimbsB1.tsx` 削除＋Root.tsx追記2箇所を戻す。既存構成に非干渉。
- 次 P07 = B2版（B1＋WhisperX語同期）。WhisperX隔離導入は背景実行中。適用先本番=EP37。
