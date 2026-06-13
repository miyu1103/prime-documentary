# 15 — Implementation Roadmap

## 1. 戦略

最大の失敗は、全サービス連携を先に作り、一本も完成しないこと。

最初に「一本を最後まで流す薄い縦断」を作り、その後、各工程の品質と自動化率を高める。

## Phase 0：Discovery

成果物：

- repository inventory
- current workflow map
- time study
- provider inventory
- secrets inventory
- representative episode
- current file naming map
- bottleneck analysis
- risk register

完了条件：

- 現状と理想の差分を説明できる。
- 既存機能を壊さない移行方針がある。

## Phase 1：Core Domain

実装：

- schemas
- IDs
- manifest
- state machine
- event log
- artifact registry
- CLI
- validators
- config
- logging
- tests

外部APIはまだ不要。

完了条件：

- sample episodeを状態遷移できる。
- invalid transitionを拒否。
- 中断後にresume。
- revisionsとstale propagationが動く。

## Phase 2：Content Planning Vertical Slice

実装：

- topic brief
- research plan
- source registry
- claim ledger
- thesis
- outline
- script
- scene plan
- QC reports

完了条件：

- topicからscene planまで追跡。
- factual spanのclaim coverage 100%。
- review diffが出る。

## Phase 3：Asset Vertical Slice

実装：

- generation request
- SDXL adapter
- local queue
- asset registry
- image QC
- selective regeneration
- previews/contact sheets

完了条件：

- scene planから必要画像が揃う。
- 一シーンのみ再生成可能。
- generation settingsを再現可能。

## Phase 4：Audio

実装：

- voice profile
- pronunciation dictionary
- chunker
- ElevenLabs adapter
- audio QC
- music ingest
- music analysis
- cue selection

完了条件：

- script revisionからaffected chunksだけ再生成。
- rights metadataが残る。
- draft/masterを分離。

## Phase 5：Edit Assembly

実装：

- edit plan
- media mapping
- timeline adapter
- subtitle
- markers
- review render
- technical QC

完了条件：

- 人間がゼロから並べず、レビュー可能な粗編集ができる。
- 一素材差替えから限定再renderできる。

## Phase 6：Approval and Publish Package

実装：

- approval records
- dashboard/CLI
- thumbnail variants
- title scorer
- metadata
- rights manifest
- package QC
- private upload adapter

完了条件：

- 承認後にprivate uploadまで自動。
- publicはまだ手動。
- approval revision mismatchを拒否。

## Phase 7：Production L3

実装：

- scheduler
- WIP limits
- multiple episodes
- cost ledger
- circuit breaker
- notifications
- worker health
- cross-machine sync
- analytics collector

完了条件：

- 週次複数本を安定処理。
- 人間作業は承認・例外中心。
- daily statusが自動生成。

## Phase 8：Learning Loop

実装：

- feature extraction
- retention-scene join
- hypothesis registry
- experiment tracking
- playbook updates
- prediction calibration

完了条件：

- 公開結果がtopic/script/edit rulesへ戻る。
- ルール更新に根拠と期限がある。

## Phase 9：Selective L4

対象：

- evergreen
- low-risk
- proven format
- stable rights
- predictable cost

canary：

- private upload
- unlisted
- delayed scheduled public
- automated rollback alert
- sampled human audit

## 2. 優先順位

1. Domain/state/data
2. Research/claims
3. Script/scenes
4. Asset generation
5. Audio
6. Edit
7. Package
8. Publish
9. Analytics
10. Full autonomy

## 3. 90日イメージ

### Week 1–2

現状調査、schema、manifest、CLI、sample。

### Week 3–4

research→script→scene縦断。

### Week 5–6

SDXL、asset QC、限定再生成。

### Week 7–8

TTS、music library、audio QC。

### Week 9–10

DaVinci assembly、review render。

### Week 11–12

package、approval、private upload、analytics基礎。

日付より完了条件で管理する。

## 4. 最初の縦断MVP

入力：

- 手動で選んだtopic brief

出力：

- research plan
- sample source registry
- claim ledger
- thesis
- outline
- English script
- scene plan
- placeholder assets
- draft narration
- edit plan
- publish package draft
- QC report

外部公開はしない。

## 5. MVPでやらないこと

- 複数チャンネル
- 複雑なweb UI
- Kubernetes
- 高度な自動サムネA/B
- public auto-publish
- 全provider対応
- 完璧な映像品質判定
- 自動権利判断の全面信頼

## 6. 技術的負債の許容

許容：

- CLI中心
- SQLite
- 単一orchestrator
- local queue
- manual approval JSON

許容しない：

- stateをファイル名だけで管理
- secret直書き
- one giant script
- output上書き
- retry無限
- publish guardなし
- schemaなしの自由JSON
