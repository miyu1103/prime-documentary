# 03 — Topic and Portfolio System

## 1. Topic Object

```yaml
topic_id:
subject:
angle:
central_question:
viewer_promise:
surprise:
stakes:
target_audience:
evergreen_horizon:
timeliness:
series_cluster:
evidence_of_demand:
competition:
differentiation:
research_feasibility:
visual_feasibility:
risk:
estimated_cost:
score:
status:
```

## 2. テーマの採用条件

- 一文で説明できる強い問い
- 視聴者に「知らない」「なぜ」「本当か」を生む
- 15〜40分程度の情報密度
- 視覚化できる
- 時間が経っても価値が残る
- 英語圏で理解可能
- 競合と異なる切り口
- 信頼できる資料へ到達可能
- 広告・権利上の重大リスクが過度でない
- チャンネルブランドへ蓄積効果がある

## 3. Candidate Generation Sources

- 自チャンネル上位動画の隣接質問
- 高維持率チャプターの深掘り
- コメントの未解決質問
- 競合の高再生だが低品質なテーマ
- 競合が扱っていない原因・構造
- 大きな出来事の長期背景
- 歴史・科学・経済・心理の交差領域
- 国際比較
- 誤解されている有名テーマ
- 視覚的に強いが説明が弱いテーマ
- 検索需要が強く動画供給が弱いテーマ
- 過去動画のシリーズ化

## 4. Angle Library

- hidden cause
- hidden system
- myth correction
- origin
- rise and collapse
- unintended consequence
- incentive structure
- technology behind
- forgotten person
- decision chain
- comparison
- scale reveal
- what changed
- why it failed
- why it survived
- what everyone gets wrong

## 5. 100点採点

- 視聴需要：20
- クリック可能性：15
- 視聴維持可能性：15
- エバーグリーン性：10
- 差別化可能性：10
- 映像化可能性：10
- 信頼できる資料：8
- シリーズ展開性：5
- 収益適合性：4
- 制作効率：3

リスク控除：

- 権利リスク：最大-20
- 事実・名誉リスク：最大-20
- 映像再現困難：最大-10
- 競合飽和：最大-10
- 一過性：最大-10

採用目安：

- 80以上：優先制作
- 70〜79：制作候補
- 60〜69：切り口再設計
- 59以下：原則保留

## 6. Score Explainability

各項目は点数だけでなく以下を返す。

- score
- reason
- evidence
- confidence
- uncertainty
- downside
- improvement action

## 7. Duplicate Control

タイトル文字列ではなくsemantic similarityで検出。

- same subject + same angle：原則重複
- same subject + different causal angle：別候補
- different subject + same generic template：過度な型化を警告
- sequel：既存動画との差分を必須記述

## 8. Portfolio Rule

- 70%：実績のあるコア領域
- 20%：隣接領域
- 10%：高不確実性の実験

追加制約：

- 同一週に類似テーマを集中させない。
- 高リスクテーマを複数同時に抱えない。
- 編集負荷の高い動画を重ねない。
- 同じビジュアルスタイルだけにしない。
- evergreenを基盤、timelyを限定。
- シリーズと探索を混ぜる。

## 9. Priority Formula

概念式：

`priority = expected_value × readiness × strategic_fit ÷ remaining_cost ÷ risk`

expected_valueは再生数だけでなく、シリーズ価値、チャンネル学習価値、動画寿命を含む。

## 10. Kill Criteria

予備調査後に次のいずれかなら棄却。

- 中心命題を支える資料がない。
- 競合との差が説明できない。
- 視覚化すると誤認を避けられない。
- 権利コストが高過ぎる。
- 15分以上へ水増しが必要。
- 一動画で扱えないほど広い。
- 主要情報が一つの利害関係資料へ依存。
- advertiser suitabilityが低く合理性がない。
- チャンネルブランドを散らす。

## 11. Scoring Calibration

予測スコアは公開結果で校正する。

- 予測CTRと実績
- 予測維持率と実績
- topic cluster別誤差
- human予測とmodel予測の差
- 楽観バイアス
- 新規領域の不確実性

一動画の成功で重みを大きく変えない。
