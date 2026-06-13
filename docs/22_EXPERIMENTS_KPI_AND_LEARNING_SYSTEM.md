# 22 — Experiments, KPI and Learning System

## 1. KPI階層

### Business

- revenue
- watch hours
- subscribers
- video asset value
- channel growth
- payback

### Content

- CTR
- average view duration
- average percentage viewed
- first 30s retention
- chapter retention
- returning viewers
- suggested/browse/search mix

### Production

- cycle time
- published episodes/week
- human review minutes
- cost/episode
- cost/published minute
- rework rate
- WIP

### Quality

- fact defect rate
- rights defect rate
- script rejection
- asset acceptance
- voice regeneration
- edit defects
- post-publish correction

### System

- job success
- retry
- resume success
- duplicate side effect
- queue wait
- worker health
- provider failures

## 2. Feature Store

各動画の特徴を保存。

- topic cluster
- angle
- title pattern
- thumbnail pattern
- hook type
- duration
- chapter count
- words/minute
- visual mode ratio
- average shot duration
- music profile
- upload timing
- risk class
- production tier

## 3. Experiment Registry

- experiment_id
- hypothesis
- primary metric
- guardrail metrics
- variants
- assignment
- start/end
- sample assumptions
- confounders
- result
- decision
- expiry

## 4. Guardrail Metrics

CTRを上げても以下を悪化させない。

- first 30s retention
- satisfaction signals
- negative comments
- unsubscribes
- policy risk
- channel trust

## 5. Learning Rule

```yaml
rule_id:
observation:
hypothesis:
evidence:
confidence:
applicable_scope:
exceptions:
recommended_action:
created_at:
review_at:
status:
```

## 6. Rule Promotion

- single observation：note
- repeated pattern：hypothesis
- controlled/strong evidence：candidate rule
- stable across cluster：production rule
- degraded/outdated：retired

## 7. Avoiding False Learning

- 小サンプル
- 季節性
- 外部ニュース
- チャンネル成長段階
- 競合公開
- recommendation volatility
- title-topic interaction
- audience mix

を考慮する。

## 8. Retention Diagnosis

離脱箇所の候補要因：

- promise already fulfilled
- confusing proper nouns
- abstract section
- visual repetition
- slow pacing
- aggressive music
- weak transition
- irrelevant tangent
- sponsor/CTA
- conclusion too long

自動で原因確定せず、候補として提示。

## 9. Monthly Learning Review

- top/bottom episodes
- prediction error
- topic cluster performance
- packaging patterns
- hook patterns
- retention failures
- production cost
- human bottlenecks
- QC misses
- rules to add/update/retire

## 10. Long-term Asset View

初動だけで動画を評価しない。

- 28d
- 90d
- 180d
- 365d

の長尾を確認し、evergreenテーマの価値を別評価する。
