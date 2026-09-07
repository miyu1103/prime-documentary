# P02 BENCHMARK FINDINGS — 参考チャンネルの機能分析

- Phase `P02` / 2026-07-12 (JST) / by claude-code
- 方針: 外見（ロゴ・配色・フォント・固有セット・素材・ショット順）はコピーしない。**機能（情報設計・タイミング・音・再利用原理）**だけを抽出しPDへ翻訳（`BENCHMARK_METHOD.md` / `MASTER_REFERENCE.md §4`）。
- **正直な範囲宣言（重要）**: 私（AI）は動画フレームを一次視聴できないため、本Phaseの一次ソースは **repo正典 `MASTER_REFERENCE.md §4`（採用骨格を既に文書化済み）** と、これを timbs baseline(P01) に結びつけた分析です。**個々のショットのフレーム精密タイムコードは捏造しません**。`benchmarks/benchmark_shots.jsonl` は原理レベルで記録し、フレーム単位の一次観察は「要 human/web 検証」と明示（受入基準の 45ショット×実タイムコードは principle-level で部分充足、フル一次観察は後続タスク）。この限界は tool フェーズ(P03+)を**ブロックしない**。

## 1. 採用する機能（表皮でなく骨格）
| チャンネル | 採用する機能原理 | timbsでの適用先 |
|---|---|---|
| MagnatesMedia | 危機→利害→逆転の物語構造、章末の引き | 幕構成・ending次回予告（既存VIDEO_RULES §10と一致） |
| Vox | 情報を**一つずつ**積み上げる視線設計 | PenaltyVsProperty で $10k→$42k を1要素ずつ提示 |
| Search Party | 調査素材を**地図・関係・時系列**へ変換 | CaseJourney（裁判経路）・EvidenceReveal |
| Wendover | 全カットを豪華にせず**要所へ予算集中** | 主役A(SPN-0006)等の山場にモーション予算を寄せる |
| fern / neo | 要所の**空間再現と立体カメラ** | 2.5D(P08)・Evidence Room(P09) を山場1カットに限定投入 |

## 2. timbs baseline への含意（P01実測と接続）
- P01計測で **主役A(SPN-0006 $10k vs $42k)の動き量 YAVG=0.87＝近静止**、SPN-0007=0.63。
- Vox原理（一つずつ構築）＋Wendover原理（要所集中）＝**この山場に情報アニメの予算を寄せ、数量を1ステップずつリビール**すれば「density緑でも紙芝居」を解消できる、が本Phaseの結論。
- Search Party原理＝判決経路(州→連邦→最高裁)を CaseJourney で軌跡描画。

## 3. 各観察の必須一文（method §採用判断）
> このショットの価値は「見た目」ではなく、視聴者の理解を ____ から ____ へ変えた点にある。
- 例(PenaltyVsProperty)：理解を「財産が没収された（規模不明）」→「罰金上限$10kに対し車$42k＝約4倍の不均衡」へ変えた点にある。

## 4. Visual Verb 対応（ブリーフ§5）
Reveal/Compare/Trace/Connect/Isolate/Reconstruct/Escalate/Overturn。timbs主要山場＝Compare(不均衡)/Reveal(証拠)/Trace(裁判経路)/Overturn(9–0逆転)。

## 5. 限界・次アクション
- フル一次観察（3ch×3動画×5ショットの実タイムコード）は、owner視聴 or 専用web調査パスで追補（`benchmark_shots.jsonl` に追記）。tool フェーズは先行可。
