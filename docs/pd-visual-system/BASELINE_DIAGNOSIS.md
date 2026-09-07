# P01 BASELINE DIAGNOSIS — PD-2026-009-timbs / candidate A

- Phase: `P01`（Baseline保存・紙芝居診断）
- By: `claude-code` / 2026-07-12 (JST)
- Baseline clip: `outputs/pd-visual-system/PD-2026-009-timbs/baseline/baseline_A.mp4`
  （1920×1080 / 30fps / **80.4s** / 2412f / sha256 `598c6dea…ed63`）
- 原本: `H:\...\timbs_premium_review_v001.mp4`（read-only, sha `d6d1cc4d…e69f`）。抽出区間 **110.1–190.5s**（本編の $10,000 vs $42,000 → "grossly disproportionate"）。
- 同一ナレーションを内包 → 後続 B/C 版と直接比較可能（受入基準①充足）。

## 1. 測定方法（客観プロキシ・全て baseline_A.mp4 に対し実測）
- **near-still**: `ffmpeg freezedetect=n=-50dB:d=0.7`（厳密フリーズ）
- **cut density**: `select='gt(scene,0.30)'` のヒット数
- **動きの大きさ**: `tblend=all_mode=difference → extractplanes=y → signalstats` の **YAVG(0–255) 平均**（フレーム間輝度差の平均＝擬似オプティカルフロー）
- 数値の一次ソースは `baseline_shots.json`。

## 2. 実測サマリ
| 指標 | 値 | 解釈 |
|---|---:|---|
| 全体 動きの大きさ YAVG | **2.27** | 低め（実写1点が牽引） |
| カット数 (>0.30) | 29 / 80.4s | 約2.77s/カット＝密度は十分 |
| near-still(freeze) | **11.77s（14.6%）** | SPN-0005末尾に集中 |

| shot | 種別 | 動きYAVG | 8軸合計/32 |
|---|---|---:|---:|
| SPN-0005 | stock_video | 5.49（末尾freeze） | 18 |
| **SPN-0006** | **motion_graphic（主役A: $10k vs $42k）** | **0.87** | 15 |
| SPN-0007 | ai_image ken_burns（"grossly disproportionate"） | **0.63** | 13 |
| **合計** | | | **51 / 96（53%）** |

## 3. 紙芝居8軸の所見
| 軸 | 判定 | 根拠 |
|---|---|---|
| 時間変化 | ✗弱 | 主役の motion_graphic/ken_burns が YAVG<1.0＝画面内がほぼ動かない |
| 意味変化 | △ | 情報(数量・引用)は伝わるが、映像でなくテロップ依存 |
| 奥行き | ✗弱 | SPN-0007 は単層AI画像で前景/中景/背景が無い |
| 視線誘導 | △ | 二値比較(0006)は焦点あり、他は汎用B-rollで焦点弱 |
| 音声同期 | ✗弱 | 数量/引用の"語出し"と演出の同期が無い（リビール不在） |
| 素材の時間性 | △ | 0005は動画で適切、末尾freeze。0007は静止画に逃げている |
| 編集文法 | ○ | カット密度は十分（29カット）。ただし"意味あるトランジション"は弱い |
| 感情・緊張 | ✗弱 | 本編の山場（不均衡の提示）に山谷が無く平坦 |

## 4. 中核所見（オーナー既知の課題の実数裏付け）
- **主役A（SPN-0006, $10,000 vs $42,000）が『動く図解』を名乗りながら motion_yavg=0.87 でほぼ静止。** これは [[feedback_animation_still_too_little]]（density緑でも動きが少ない）と [[feedback_perceptual_motion_and_verify]] が指す典型。
- ken_burns の AI 画像（SPN-0007）も 0.63 で近静止＋単層。**"意味あり かつ 美しくダイナミック"（VIDEO_RULES §12）を満たしていない。**
- カット密度は問題ではない（十分）。**問題は"画面内部の動きの大きさ"と"音声同期リビール"と"奥行き"。**

## 5. 改善仮説（P05+ の B/C 変種で検証する対象）
1. **SPN-0006 → core-5 `PenaltyVsProperty`**：$10,000 と $42,000 を数量バーで**ため→開放**、比率ラベル、**語出し（"maximum fine" / "forty-two thousand"）に同期**。目標 motion_yavg を実写帯（≥ 一定下限）へ。
2. **SPN-0007 → core-5 `QuoteUnderExamination`**：引用をキネティックタイポ＋2.5D奥行き（前景引用/背景法廷）で提示、語単位同期。
3. **SPN-0005 末尾 freeze 解消**：動画素材の続き再生 or 差し替えで near-still を 0 へ。
4. 機構化候補（[[feedback_prevent_by_mechanism]]）：optical-flow(YAVG)の**正の下限**・near-still率上限・caption語同期を後続ゲートに。

## 6. baseline としての妥当性（受入基準）
- ① 同一ナレで後続版と比較可能 → **充足**（区間内ナレ内包・manifestで再現可能）。
- ② 各ショットに visual question と start/end state → **充足**（`baseline_shots.json`）。
- ③ 紙芝居要因8軸が採点済み → **充足**（本書§3・shots JSON）。

## 7. 保護・rollback
- H: 原本・`remotion/**`・`episodes/**`・`.git` は未変更。出力は `outputs/pd-visual-system/...` のみ。
- rollback: `outputs/.../baseline/*` と本書を削除、`PHASE_STATE.json`/`IMPLEMENTATION_STATUS.md` を P01 開始前へ。
