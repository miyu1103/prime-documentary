# 26 — Retention Engineering

## 1. 結論

視聴維持率は「テンポを速くすること」ではない。

維持率は、視聴者が次の数十秒を見る合理的理由を連続して持てるかで決まる。PDでは、情報の価値、理解負荷、未回収の問い、視覚変化、感情の起伏を設計対象にする。

## 2. Retention unit

分析単位：
- hook beat
- claim beat
- example beat
- reveal beat
- transition beat
- chapter
- scene
- shot

動画全体の平均だけでは改善できない。

## 3. Open-loop ledger

台本段階で管理：
- loop_id
- question opened
- opened_at
- expected payoff
- payoff_at
- partial payoff
- risk of frustration

問いを開き過ぎない。未回収のまま放置しない。

## 4. First 60 seconds

必要要素：
- recognizable subject
- anomaly or tension
- clear stakes
- specific promise
- evidence of credibility
- forward motion

避ける：
- 長い背景説明
- チャンネル挨拶
- 意味のない映画的映像
- 抽象的な煽り
- 同じ内容の言い換え

## 5. Cognitive load

負荷を上げる要因：
- 固有名詞密度
- 日付密度
- 数字密度
- 抽象概念
- 長い従属節
- 画面と音声の競合
- unfamiliar geography

高負荷箇所では：
- visual simplification
- comparison
- recap
- on-screen label
- slower pacing
- concrete example

を使用する。

## 6. Pattern interruption

一定時間ごとに機械的にカットを変えるのではない。

意味の節目で以下を使う：
- scale change
- map
- diagram
- archival texture
- silence
- sound change
- human detail
- numerical reveal
- viewpoint reversal

## 7. Chapter transition

章末に次を行う。
- current answer
- unresolved complication
- next chapter necessity

「次に〜を見ていきます」のような形式的予告を乱用しない。

## 8. Retention risk prediction

台本・scene planから予測する。
- exposition length
- novelty gap
- repeated visual mode
- high noun density
- weak causal link
- delayed promise
- unsupported emotional claim
- chapter without escalation
- long static image
- audio monotony

予測は警告であり、真実ではない。公開後データで校正する。

## 9. Post-publication mapping

retention curveをscene rangesへ結合。

記録：
- entry retention
- exit retention
- local slope
- relative performance
- traffic source
- viewer segment
- scene features
- narration pace
- visual mode
- music state
- cut density

## 10. Interpretation rules

- ドロップがscene原因とは限らない
- 前sceneの約束不履行が遅れて出る場合がある
- chapter markerによるskipを区別
- external trafficは行動が異なる
- 少数サンプルでルール化しない
- 再生数と維持率のトレードオフを考慮

## 11. Retention experiments

一度に一要素を変えることが理想だが、動画制作では完全統制が難しい。そこで、仮説と変更点を記録する。

例：
- hook duration
- reveal timing
- chapter count
- narrator pace
- visual mode mix
- average shot duration
- title promise specificity

最低複数動画で評価する。

## 12. Success metrics

- first 30s survival
- 60s survival
- relative retention by segment
- chapter transition loss
- completion rate
- rewatch spikes
- returning viewer behavior
- watch time per impression

CTRだけ、平均視聴率だけに最適化しない。
