# 35 — Capacity Planning and Bottleneck Control

## 1. 結論

制作本数は最も遅い工程で決まる。上流の生成能力を増やしても、編集・承認・公開が詰まれば仕掛品とコストが増えるだけ。

## 2. Capacity units

工程ごとに：
- jobs/day
- accepted minutes/day
- GPU minutes
- API characters/tokens
- render minutes
- human review minutes
- queue wait

を計測する。

## 3. Cost per publishable minute

`total episode cost ÷ final duration`

分解：
- research
- LLM
- visual generation
- TTS
- music
- storage
- render
- human review
- rework

## 4. Rework rate

- topic rejection after research
- script revision count
- visual acceptance rate
- voice chunk regeneration rate
- edit revision count
- package change count

## 5. Little’s Law

WIP、throughput、cycle timeの関係を監視する。実装で数式を強制する必要はないが、仕掛品増加を「進捗」と誤認しない。

## 6. Initial WIP

- approved/pre_research: 5
- researching: 3
- scripting: 2
- visual generation: 2 episodes or GPU-capability based
- audio: 2
- edit assembly: 1
- edit review: 2
- package ready: 3

実測により調整。

## 7. Bottleneck detection

- queue age
- utilization
- wait/process ratio
- blocked duration
- rework loop count
- human approval delay
- provider throttling

## 8. Bottleneck response

編集がボトルネック：
- template coverage
- proxy workflow
- scene-plan quality
- motion automation
- exception-only review
- lower WIP upstream

人間承認がボトルネック：
- batch review
- risk ranking
- diff display
- sampled audit
- approval SLA

画像がボトルネック：
- candidate count by priority
- reuse library
- lower-cost drafts
- model routing
- parallel GPU only after queue evidence

## 9. Scaling order

1. Remove rework
2. Reduce human touches
3. Improve job scheduling
4. Reuse assets
5. Optimize models
6. Add compute
7. Add people

計算資源追加を最初の解決策にしない。

## 10. Production forecast

episode開始前に：
- expected duration
- scene count
- hero scenes
- visual difficulty
- research risk
- TTS characters
- edit complexity
- expected review time

を予測し、実績との差でモデルを校正する。
