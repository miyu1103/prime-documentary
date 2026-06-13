# 36 — Model and Prompt Evaluation Harness

## 1. 目的

プロンプト改善を主観で判断せず、代表データで比較する。

## 2. Evaluation sets

- topic ranking set
- source classification set
- claim extraction set
- contradiction set
- thesis set
- outline set
- English script set
- scene decomposition set
- visual prompt set
- title/package set

## 3. Golden labels

人間正解が作れるもの：
- JSON validity
- source type
- date/number extraction
- claim-source link
- duplicate detection
- pronunciation list

主観的なもの：
- narrative strength
- natural English
- visual usefulness
- curiosity

はrubricと複数評価で扱う。

## 4. Metrics

- schema pass rate
- factual precision
- factual recall
- unsupported addition rate
- critical omission rate
- reviewer score
- pairwise preference
- repair success
- latency
- cost
- human review minutes
- downstream rework

## 5. Evaluation protocol

1. freeze dataset
2. blind candidate versions
3. run deterministic validators
4. independent review
5. compare cost and quality
6. inspect failure clusters
7. approve/rollback

## 6. LLM-as-judge

使用可能だが、単独の真実にしない。
- judge prompt version
- position randomization
- multiple judges where valuable
- human spot check
- known bias tests

## 7. Regression

prompt/model/schema変更時に：
- previous baseline
- new candidate
- no critical regression
- cost change
- acceptance change

を記録する。

## 8. Production feedback

実際のhuman correctionsをevaluation setへ追加。ただし個別episodeの特殊事情を一般化し過ぎない。

## 9. Promotion criteria

- statistically or operationally meaningful improvement
- no increase in critical error
- acceptable cost
- rollback ready
- prompt registry updated
