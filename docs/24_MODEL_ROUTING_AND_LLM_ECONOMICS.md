# 24 — Model Routing and LLM Economics

## 1. 結論

すべてを最上位モデルへ送る設計も、すべてを安価なモデルへ送る設計も誤り。

PDは、作業の価値、不可逆性、文脈量、検証可能性、失敗コストに応じてモデルを選ぶ。

## 2. タスク分類

### Tier A — 高判断価値
- 企画の最終比較
- 中心命題
- 構造的台本設計
- 矛盾する根拠の評価
- 高リスク事実・表現
- 複雑なアーキテクチャ変更

高能力モデル＋独立レビュー。

### Tier B — 高品質生成
- 台本初稿
- 章構成
- scene purpose
- visual strategy
- title concepts
- retrospective synthesis

高品質モデル。構造化出力とrubricを使用。

### Tier C — 大量構造化
- entity extraction
- source metadata
- claim candidate extraction
- tagging
- format conversion
- prompt field compilation
- basic lint repair

安価・高速モデル＋決定論的validator。

### Tier D — 決定論処理
- schema validation
- hash
- duration calculation
- text diff
- loudness analysis
- duplicate detection
- state transition

LLMを使用しない。

## 3. Routing inputs

- task_type
- risk_class
- expected_output_value
- input_tokens
- output_tokens
- latency sensitivity
- structured-output reliability
- historical acceptance rate
- model availability
- privacy constraints
- budget remaining

## 4. Fallback

fallbackは品質を黙って下げない。

- preferred model unavailable
- approved fallback model
- reduced scope
- confidence penalty
- mandatory review flag
- retry schedule

高リスクタスクでfallbackモデルへ切り替えた場合、自動承認を禁止する。

## 5. Prompt caching and reuse

固定情報を毎回巨大に送らない。
- channel constitution
- editorial style
- schema
- episode context summary
- source evidence packets

を分離し、必要なコンテキストだけ渡す。

## 6. Context budgeting

長い資料を一括投入しない。

1. source ingest
2. chunk metadata
3. retrieval
4. evidence packet
5. claim evaluation
6. synthesis

重要箇所へ原文位置を残し、要約だけを再要約し続けない。

## 7. Model evaluation

モデル切替前にgolden setで評価：
- claim extraction precision/recall
- unsupported assertion rate
- English naturalness
- narrative structure score
- JSON validity
- correction acceptance
- cost per accepted output
- human review time

最安単価ではなく、**accepted outputあたりの総コスト**で比較する。

## 8. Cost formula

`Total task cost = API cost + retry cost + validator cost + human review cost + downstream rework cost`

安いモデルが誤りを増やし、画像・音声・編集を再生成させる場合、全体では高い。

## 9. Prompt/version registry

- prompt_id
- version
- task
- model_profile
- schema_version
- evaluation_set
- baseline
- observed metrics
- change rationale
- rollback version
- approved_by

## 10. Hallucination containment

- evidence-constrained generation
- claim IDs
- explicit unknown state
- independent checker
- deterministic number/date validation
- unsupported sentence detector
- no factual synthesis from model memory alone
