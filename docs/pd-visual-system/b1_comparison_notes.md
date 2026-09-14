# P06 B1 COMPARISON NOTES — A vs B1 (timbs 80.4s test-bench)

- Phase `P06` / 2026-07-12 (JST) / by claude-code
- 同一区間（source 110.1–190.5s）・**同一ナレーション**・同一尺（2412f/80.4s）で A（現状）と B1（コア5＋既存素材）を比較。
- B1 構成: `remotion/src/compositions/TimbsB1.tsx`（`TimbsB1` composition）。プレビュー: `outputs/pd-visual-system/b1_check/`（stills＋mp4）。

## 変更点（B1で加えたのは「素材検索＋コア5部品」のみ・新ツールなし）
| beat | A（baseline） | B1 | 主要動詞 |
|---|---|---|---|
| SPN-0005 | 実写だが末尾**11.8s freeze** | 押し込み実写＋マスクスライドのテロップ＋出典 | Reveal |
| **SPN-0006** | motion_graphic だが **motion_yavg 0.87＝近静止** | **PenaltyVsProperty**（$10k青 vs $42k金のバー＋比率リビール） | Compare |
| SPN-0007 | ken_burns AI画像 **0.63＝近静止** | **QuoteUnderExamination**（語ごと切り上がり＋examine＋出典） | Isolate |

## 人間評価（暫定・実レンダ目視／owner確認枠）
| 指標 | A | B1 | 根拠 |
|---|---|---|---|
| 紙芝居感 | 高（主役2ショットが近静止） | 低（バー伸長・語切り上がり・押し込み） | 実レンダ目視（b1_check/*.png） |
| 理解しやすさ | テロップ依存 | 数量・引用が映像自体で構築 | ComparisonBarsが差を視覚化 |
| 視線誘導 | 弱 | 強（バー長さ／引用語／examineスポット） | 単一eye_target/シーン |
| 事実性 | 同じ数値 | 同じ数値（$10k/$42k/9-0は不変） | scene_planのtruth_status |
| 高級感 | 中 | 高（brand配色・出典ライン・atmosphere） | 目視 |
| 破綻 | freeze | なし（typecheck0・レンダ成功） | 検証済 |

> 定量: A の主役 motion_yavg 0.87/0.63（P01実測）に対し、B1 は動的コンポーネント（バー伸長・語アニメ）で近静止を除去。**B1のoptical-flow再測定は mp4 完成後に実施**（背景レンダ中）。

## 限界 / 次
- beat1 のB-roll選定は素材検索(P04)を使えるが、現状は既存 public clip を使用（H:検索素材の public 取り込みは後続）。
- テロップ可読性: 実写上の白文字は帯の濃さを要調整（B1で軽微）。
- **語同期は未（B2/WhisperX）**、**2.5Dは未（B3）**。1変更ずつ効果を測る方針（ブリーフ§7）。
- rollback: `TimbsB1.tsx` 削除＋Root.tsx の TimbsB1 追記2箇所を戻す。既存構成に非干渉。
