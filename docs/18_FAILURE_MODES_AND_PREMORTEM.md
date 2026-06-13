# 18 — Failure Modes and Premortem

## 1. 事業失敗：映像は綺麗だが見られない

原因：

- 需要が弱い
- タイトルが曖昧
- 中心命題がない
- 視聴者利益がない
- 競合との差がない

対策：

- topic-angle scoring
- packaging hypotheses before production
- thesis gate
- competition map
- analytics loop

## 2. 投稿できない

原因：

- 完璧主義
- 工程過多
- 編集ボトルネック
- 承認待ち
- 全体再生成

対策：

- WIP limits
- quality tiers
- assembly automation
- batch approval
- partial rerun
- SLA

## 3. チャンネルが散る

原因：

- 短期需要を追う
- シリーズ設計なし
- ブランド定義不足

対策：

- content pillars
- portfolio constraints
- topic clusters
- monthly strategy review

## 4. LLM Hallucination

対策：

- claim ledger
- source requirement
- independent fact checker
- E claim prohibition
- current facts timestamp
- citation location

## 5. 退屈な台本

対策：

- central tension
- chapter function
- unanswered question tracking
- compression pass
- narration test
- visual feasibility check

## 6. AI臭い英語

対策：

- style profile
- repeated phrase lint
- banned filler catalog
- independent English edit
- read-aloud test

## 7. 同じような画像

対策：

- visual mode mix
- neighboring shot diversity
- reuse metrics
- map/diagram/object shots
- composition planning

## 8. 歴史的誤り

対策：

- material culture constraints
- risk flags
- uncertainty labels
- diagrams when uncertain
- source-linked visual notes

## 9. 人物連続性崩壊

対策：

- character bible
- reference assets
- recurring IDs
- face-minimizing shot design
- continuity QC

## 10. 発音ミス

対策：

- dictionary
- preflight
- phonetic review
- chunk rerun
- named-entity pronunciation tests

## 11. 一つの巨大スクリプト

対策：

- stage boundaries
- schemas
- worker interfaces
- provider adapters
- tests

## 12. 再開できない

対策：

- checkpoints
- event log
- idempotency
- leases
- external request IDs

## 13. 二重課金

対策：

- input hash
- idempotency key
- provider request lookup
- budget reservation
- result polling before retry

## 14. 二重公開

対策：

- video hash
- channel allowlist
- publish idempotency
- existing upload lookup
- approval revision check

## 15. 人間確認が増える

原因：

- 低品質候補の大量生成
- 全例外を通知
- 比較UIがない

対策：

- confidence thresholds
- ranked shortlist
- actionable alerts only
- review diffs
- batch review

## 16. 自動化がブラックボックス

対策：

- provenance
- structured logs
- explainable scores
- revision diff
- evidence links
- deterministic validators

## 17. 早すぎるL4

対策：

- promotion criteria
- canary
- sampled audit
- rollback
- low-risk scope

## 18. Provider Lock-in

対策：

- adapter interfaces
- provider-neutral core schema
- exportable assets
- profile aliases
- fallback providers
- terms registry

## 19. コストが再生価値を上回る

対策：

- expected value gate
- cost estimate
- tiered generation quality
- library reuse
- early kill
- postmortem by stage

## 20. 大量生成が目的化

対策：

- published asset utilization
- unused asset cost
- music coverage matrix
- generation tied to approved demand
- WIP limits
