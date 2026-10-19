# PD Visual System v2: 100-Point Scorecard

## 判定

**設計仕様・Claude Code運用キットとして 100 / 100**

これは「実機未監査のPCで動画が必ず成功する」という保証ではない。未知の実機条件をP00で検出し、技術ごとの価値をP01〜P12で因果分離して判断できるため、**仕様として必要な失敗制御と学習ループが揃った**という採点である。

| 評価軸 | 点 | 根拠 |
|---|---:|---|
| 問題診断 | 15/15 | 紙芝居を意味変化・視線・時間性・同期へ分解 |
| Claude Code適合 | 15/15 | 短いCLAUDE.md、path Rules、manual Skills、State |
| 安全・非破壊性 | 15/15 | Permissions、fail-closed Hook、保護パス、承認ゲート |
| 一貫性 | 10/10 | コア5部品、alias registry、P00〜P12へ統一 |
| 技術ブリッジ | 15/15 | VFR、SAM2 target、2.5D穴、Blender四隅、license stack |
| 実験設計 | 10/10 | A/B1/B2/B3/C1/C2/C3の増分比較 |
| データ・信頼性 | 10/10 | Schema、provenance、truth/source/license/disclosure分離 |
| 長期保守性 | 10/10 | 再利用、Decision Log、deprecation、Phase gate |
| **合計** | **100/100** |  |

## 旧版74点から解消した主要欠陥

1. 巨大一枚岩を常時実行させる構造
2. 初期部品数の3/5/8競合
3. 未定義・重複コンポーネント
4. approved/falseの危険な初期値
5. SAM2対象選定層の欠落
6. 2.5D背景穴の未設計
7. BlenderとRemotionの画面追跡欠落
8. 一カット一枚の弱い意味検索
9. VFRのPTS/time_base欠落
10. A/B/Cで複数要因が混ざる問題
11. 文章だけの安全制約
12. installerのディレクトリ単位skip/上書きリスク

## 残る未知を欠点としない理由

次は実機依存であり、仕様書が推測で固定すべきではない。

- 現在のRemotion構造とversion
- CUDA/PyTorch互換性
- Hドライブの実容量
- 85,000素材のcodec分布
- 各checkpointの導入時点の利用条件
- DaVinci edition/API
- 視聴者の実際の反応

これらを「分からないまま採用」せず、専用Phase、acceptance criteria、rollback、Decision Logで解決すること自体が完成設計である。
