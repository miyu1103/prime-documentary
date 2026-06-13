# 11 — Orchestration, Retries, Costs and Observability

## 1. Orchestrator Loop

1. runnable episodes取得
2. stale/blocked確認
3. policy評価
4. dependency確認
5. cost estimate
6. budget reserve
7. job create
8. worker lease
9. execution heartbeat
10. result validate
11. artifact register
12. cost finalize
13. state transition
14. next jobs
15. notification

## 2. Idempotency

例：

`sha256(stage + episode_id + input_revision_ids + config_revision + provider_profile)`

同じkeyでsucceededがあれば原則再利用。force rerunは理由を必須にする。

防止対象：

- 二重API課金
- 二重画像生成
- 二重音声生成
- 二重アップロード
- 二重公開
- 重複イベント

## 3. Retry Matrix

- HTTP 429：provider指示に従いbackoff
- HTTP 5xx：限定retry
- timeout：外部結果照会後retry
- invalid prompt：prompt repair
- content rejection：visual strategy変更
- GPU OOM：batch/size削減
- corrupt file：再download/再生成
- quality fail：variation policy
- fact fail：researchへ戻す
- rights fail：代替素材
- budget：approval待ち
- auth：停止して通知

無限retry禁止。

## 4. Circuit Breaker

provider単位：

- closed
- open
- half-open

連続失敗時にopenし、全episodeが同じ障害で失敗するのを防ぐ。

## 5. Dead Letter Queue

次を保存：

- original job
- all attempts
- last error
- artifacts created
- side effects
- recommended action
- owner
- deadline

## 6. Cost Ledger

- provider
- service
- model
- unit
- quantity
- estimated cost
- actual cost
- currency
- exchange rate date
- episode
- scene
- job
- timestamp
- billing evidence

ローカルGPUも無料とみなさず、時間・電力・占有を記録可能にする。

## 7. Budget Hierarchy

- episode soft limit
- episode hard limit
- daily provider limit
- weekly production limit
- monthly channel limit
- emergency shutdown limit

## 8. Preflight Cost Estimate

- LLM tokens
- research retrieval
- image count × GPU time
- TTS characters
- music credits
- render time
- storage
- upload bandwidth
- human review estimate

## 9. Budget Exceeded Policy

順序：

1. 低優先シーンの候補数削減
2. 既存音楽を再利用
3. 類似画像の派生
4. 高価モデルを重要箇所へ限定
5. 不要章を構造的に削除
6. hard limit超過は承認待ち

## 10. Structured Logs

- timestamp
- severity
- correlation_id
- episode_id
- job_id
- stage
- event
- duration
- retry
- provider
- input hash
- output refs
- redaction status

## 11. Metrics

- queue depth
- stage throughput
- success rate
- retry rate
- median/p95 duration
- cost per stage
- human review minutes
- approval wait
- GPU utilization
- asset acceptance rate
- provider error rate
- publish cycle time
- stale artifact count
- dead-letter count

## 12. Tracing

episode全体のcritical pathを追跡する。

例：

- 調査待ち
- 人間承認待ち
- GPU待ち
- 編集待ち
- render待ち
- platform processing待ち

総時間と実作業時間を分ける。

## 13. Dashboard

最低限：

- episodes by state
- blockers
- approvals
- today/weekly cost
- queue
- worker health
- provider health
- WIP
- predicted completion order
- quality failure hotspots
- human review backlog

## 14. Notifications

即時：

- accidental public risk
- rights/fact blocker
- hard budget
- destructive action attempt
- repeated provider failure
- data loss risk
- credential compromise

まとめ通知：

- normal QC failures
- completed drafts
- daily status
- weekly analytics

通知過多で人間の注意を浪費しない。
