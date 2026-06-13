# 23 — Creator Control Center and Approval UX

## 1. 結論

自動化の最終ボトルネックは生成ではなく、人間の確認である。

承認画面が悪いと、各工程を自動化しても、阪本が大量の文章、画像、音声、動画を一から見直すことになる。したがって、PDの管理画面は「全成果物を表示する画面」ではなく、**意思決定を圧縮する画面**として設計する。

## 2. Control Centerの主要画面

### 2.1 Portfolio Board

表示項目：
- 候補テーマ
- 一文企画
- central question
- viewer promise
- 需要根拠
- 競合密度
- PDとの差別化
- 制作コスト
- 予想総尺
- 人間確認時間
- risk class
- expected value range
- score uncertainty
- series relation
- kill condition

操作：
- approve
- approve with condition
- reframe
- hold
- reject
- merge
- move to experiment bucket

### 2.2 Episode Command Center

一画面に以下を集約する。
- current state
- active revision
- progress by stage
- blockers
- stale artifacts
- cost to date / forecast
- human review minutes
- next decision
- critical claims
- high-risk scenes
- failed jobs
- provider status
- latest review render
- package variants

### 2.3 Script Approval

全文を最初から読ませるだけでは不十分。

表示：
- thesis
- hook
- chapter purpose
- claim coverage
- unsupported/low-confidence spans
- changes from previous revision
- repeated ideas
- difficult pronunciation
- estimated duration
- expected retention risks
- exact sources for critical claims

承認対象はrevision固定。承認後に一文字でも意味のある変更が入った場合、対象範囲の承認を失効させる。

### 2.4 Visual Review

シーン順に以下を表示する。
- narration span
- scene purpose
- selected asset
- alternative candidates
- prompt and seed
- fact/continuity warning
- neighboring shots
- crop preview
- motion preview
- regeneration reason options

人間のフィードバックは自由文だけでなく、failure taxonomyを選択できるようにする。

### 2.5 Edit Review

レビュー動画に自動マーカーを重ねる。

- blocker
- low-confidence visual
- source-sensitive claim
- repeated visual
- pacing anomaly
- audio seam
- subtitle mismatch
- music transition
- thumbnail candidate

人間はマーカー単位でapprove/fix/commentできる。修正要求は該当scene/jobへ変換される。

### 2.6 Package Review

同一画面で比較する。
- title candidates
- thumbnail candidates
- title-thumbnail pair score
- mobile preview
- promise-to-video consistency
- sensitivity flags
- description
- chapters
- selected playlist
- publication settings

タイトル単体、サムネ単体ではなく「組」を承認する。

## 3. Review by exception

人間へ出す優先順位：

1. S4/S5 blocker
2. 新しい高リスク種類
3. 自動QC間の不一致
4. confidence below threshold
5. 大きなrevision差分
6. 予算超過
7. 重要シーン
8. サンプリング監査

通常passした低リスク成果物を毎回全件確認しない。

## 4. Approval SLA

初期目標：
- portfolio：週1回、30分以内
- thesis/script：1本20〜40分
- visual exceptions：1本15分以内
- first cut：実尺＋15分以内
- package：10分以内

SLAを超える場合、品質問題かUI問題かを分解する。

## 5. Approval object

必須項目：
- approval_id
- target_type
- target_id
- target_revision
- decision
- conditions
- evidence_snapshot_hash
- requested_at
- decided_at
- decided_by
- expires_at
- invalidated_by
- notes

## 6. Bulk approval

同一条件を満たす低リスク項目は一括承認可能。ただし以下は一括不可：
- critical claims
- public figures
- rights exceptions
- publish visibility
- hard-budget override
- destructive action

## 7. UIの失敗指標

- 承認に必要なクリック数
- 一承認あたりの時間
- 承認後の差戻し率
- 人間が見落とした重大欠陥
- 不要な警告率
- 同じ問題の再発率
- 自由文フィードバック比率

自由文が多い場合、分類体系またはUIが不足している。
