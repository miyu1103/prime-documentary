# 17 — Prompt and Agent Design

## 1. Prompt Components

- role
- objective
- context
- inputs
- constraints
- process
- output schema
- quality rubric
- failure behavior
- examples
- forbidden behavior

## 2. Structured Output

自由文の後処理を避ける。

- JSON Schema
- explicit null
- enums
- IDs
- confidence
- evidence refs
- warnings
- validation notes

## 3. Generator–Reviewer Pattern

1. generator
2. deterministic validator
3. independent reviewer
4. repair
5. final validator

同一agentの自己批評だけでは不十分。

## 4. Confidence

confidenceを飾りにしない。

- evidence basis
- uncertainty reason
- threshold action
- historical calibration
- confidence interval where possible

## 5. Research Prompt Requirements

必ず含める。

- What evidence would disprove the thesis?
- Which claims rely on one interested source?
- Which terms are ambiguous?
- Which facts may have changed?
- What is genuinely unknown?
- Which visual reconstructions risk overstating certainty?

## 6. Writing Prompt Requirements

- viewer promise
- thesis
- claims
- uncertainty wording
- chapter functions
- target style
- banned filler
- narration constraints
- output annotations

出典情報を本文へ過剰に漏らさず、claim IDsをannotationへ保持。

## 7. Visual Prompt Requirements

- factual certainty
- visual intent
- period/geography
- unknown details
- continuity refs
- forbidden elements
- candidate count
- QC profile

不明な部分を勝手に具体化しない。構図で隠す、抽象化する、図解へ変更。

## 8. Repair Prompt

全出力を書き直さず、以下を渡す。

- failed fields
- failure category
- validator message
- immutable fields
- allowed changes
- previous attempts
- cost budget

## 9. Prompt Versioning

- prompt_id
- version
- model
- date
- purpose
- input schema
- output schema
- evaluation set
- change note
- performance
- rollback version

## 10. Prompt Evaluation

- schema pass rate
- hallucination rate
- claim coverage
- human acceptance
- edit distance after review
- retry count
- cost
- latency
- style violations
- output variance

## 11. Prompt Injection Defense

外部資料は命令ではなくデータ。

- untrusted delimiters
- embedded instruction ignore
- no tool execution from source text
- URL/content sanitation
- source provenance
- restricted tools for research agent
- no secret access
- no shell access unless necessary

## 12. Agent Boundaries

### Topic Strategist

企画候補と採点。事実確定はしない。

### Research Director

調査計画と資料構造化。最終台本を書かない。

### Fact Checker

主張監査。物語上の都合で基準を下げない。

### Documentary Writer

承認済みclaimを物語化。新事実を勝手に追加しない。

### Visual Director

scene intentを視覚仕様へ。史実を確定しない。

### Audio Director

読み、声、音楽、ミックス。台本の意味を変更しない。

### Edit Engineer

timeline assembly。content approvalを代行しない。

### QA Auditor

独立監査。実装者の説明を鵜呑みにしない。

### Automation Architect

再開性、冪等性、依存関係、コスト、安全性。

### Analytics Strategist

公開結果から仮説。単一動画から断定しない。
