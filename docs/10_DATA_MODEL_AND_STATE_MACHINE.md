# 10 — Data Model and State Machine

## 1. Core Entities

- Channel
- ContentStrategy
- Topic
- Episode
- ResearchPlan
- Source
- Claim
- Thesis
- Outline
- Script
- ScriptSpan
- Scene
- Shot
- Asset
- GenerationRequest
- NarrationChunk
- MusicTrack
- Cue
- Timeline
- Render
- PublishPackage
- Approval
- Job
- Event
- CostEntry
- AnalyticsSnapshot
- Experiment
- LearningRule

## 2. ID Rules

- episode_id：`PD-YYYY-NNN-slug`
- topic_id：`TOP-YYYYMMDD-NNN`
- source_id：`SRC-NNNN`
- claim_id：`CLM-NNNN`
- script_span_id：`SPN-NNNN`
- scene_id：`S001`
- shot_id：`S001-SH001`
- asset_id：`PD-YYYY-NNN-S001-IMG-001`
- narration_chunk_id：`VO-001`
- music_track_id：`MUS-YYYY-NNNN`
- job_id：UUID/ULID
- revision：`v001`

## 3. Episode States

`idea`
→ `screening`
→ `approved`
→ `researching`
→ `research_ready`
→ `outline_ready`
→ `script_draft`
→ `script_verified`
→ `scene_planned`
→ `assets_generating`
→ `assets_ready`
→ `voice_ready`
→ `music_ready`
→ `edit_assembly`
→ `edit_review`
→ `package_ready`
→ `publish_approved`
→ `scheduled`
→ `published`
→ `analytics_reviewed`
→ `archived`

## 4. State Entry/Exit Examples

### idea
entry：topic candidate created  
exit：screening job complete

### screening
entry：candidate ready  
exit：approved / rejected / needs_reframe

### approved
entry：portfolio approval  
exit：research plan created

### researching
entry：research jobs active  
exit：research gate pass

### research_ready
entry：claim ledger validated  
exit：thesis accepted

### outline_ready
entry：outline gate pass  
exit：draft script created

### script_draft
entry：draft exists  
exit：verification pass

### script_verified
entry：claims linked and script approved  
exit：scene plan valid

### scene_planned
entry：all script spans allocated  
exit：generation jobs emitted

### assets_generating
entry：generation active  
exit：required assets pass QC

### assets_ready
entry：visual package complete  
exit：audio dependencies ready

### voice_ready
entry：narration pass  
exit：music ready

### music_ready
entry：cue sheet pass  
exit：timeline job starts

### edit_assembly
entry：timeline building  
exit：review render exists

### edit_review
entry：review package ready  
exit：approved or revision jobs emitted

### package_ready
entry：final render and metadata pass  
exit：publish approval

### publish_approved
entry：approval valid  
exit：upload/schedule succeeds

### scheduled
entry：platform scheduled  
exit：public observed

### published
entry：public URL confirmed  
exit：minimum analytics review complete

## 5. Invalid Transitions

- idea → published
- research_ready → assets_generating without script
- script_draft → voice_ready without verification
- assets_ready → scheduled without package
- package_ready → published without approval
- published → script_draft without correction workflow

## 6. Revision Semantics

- entity_id：概念上の同一物
- revision_id：正確な内容版
- approvalはrevision_idへ紐付く
- successorはsuperseded revisionを参照
- content hashで検証
- job inputはrevision IDsを保存

承認済み成果物を上書きしない。

## 7. Dependency and Staleness

claim revisionが変わると：

- linked script spans stale
- linked scenes stale
- linked assets/on-screen text may be stale
- voice chunks stale
- timeline stale
- render stale
- package approval invalidated

staleは削除ではない。再計算が必要な状態。

## 8. Job States

- queued
- leased
- running
- succeeded
- failed_retryable
- failed_terminal
- blocked
- awaiting_approval
- cancelled
- superseded
- dead_letter

## 9. Job Lease

worker crashを考慮し、lease timeout後に再取得可能にする。外部side effectがあったかprovider request IDで確認してから再実行する。

## 10. Error Taxonomy

- INPUT_INVALID
- DEPENDENCY_MISSING
- PROVIDER_AUTH
- PROVIDER_RATE_LIMIT
- PROVIDER_OUTAGE
- PROVIDER_REJECTED
- BUDGET_EXCEEDED
- RIGHTS_BLOCK
- FACT_BLOCK
- QUALITY_FAIL
- STORAGE_FULL
- FILE_CORRUPT
- GPU_OOM
- EDITOR_UNAVAILABLE
- PUBLISH_DUPLICATE
- APPROVAL_REQUIRED
- INTERNAL_BUG
- UNKNOWN

各error classにretry policyを紐付ける。

## 11. Manifest First

個別エピソードの中心は`manifest.json`。

- identity
- strategy
- state
- approvals
- research refs
- claim refs
- script refs
- scene refs
- asset refs
- audio refs
- edit refs
- publish refs
- analytics refs
- costs
- warnings
- provenance
- revisions

ファイルの存在だけでは状態を判断しない。

## 12. Artifact Immutability

- 新revisionを作る。
- supersedes関係を保存。
- 旧版を保持。
- manifestがactive revisionを指す。
- storage節約はretention policyで行う。

## 13. Event Log

イベント例：

- EPISODE_CREATED
- TOPIC_APPROVED
- RESEARCH_COMPLETED
- CLAIM_REJECTED
- SCRIPT_REVISION_CREATED
- ASSET_GENERATED
- ASSET_REJECTED
- VOICE_REGENERATED
- TIMELINE_BUILT
- HUMAN_APPROVAL_GRANTED
- VIDEO_SCHEDULED
- ANALYTICS_SNAPSHOT_CAPTURED

追記型で保存する。
