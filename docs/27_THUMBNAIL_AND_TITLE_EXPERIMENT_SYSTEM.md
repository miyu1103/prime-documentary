# 27 — Thumbnail and Title Experiment System

## 1. 結論

タイトルとサムネイルは動画完成後の装飾ではなく、企画仮説の最終表現。

企画時点で複数のpackage hypothesisを作り、本編がその約束を回収できるか確認する。

## 2. Package hypothesis

各案に：
- target curiosity
- viewer prior belief
- information gap
- emotional tone
- central object
- promised reveal
- excluded interpretations
- matching scenes
- risk

## 3. Title dimensions

- clarity
- specificity
- novelty
- consequence
- causal tension
- familiarity
- search language
- mobile truncation
- natural English
- promise accuracy
- channel distinctiveness

## 4. Thumbnail dimensions

- single focal idea
- object/face readability
- contrast
- anomaly
- visual hierarchy
- negative space
- small-size legibility
- title complementarity
- authenticity
- no misleading evidence

## 5. Concept before execution

悪い量産：同じ構図の色違いを10枚。

良い比較：
- system concept
- human consequence concept
- before/after concept
- scale concept
- hidden-object concept

各conceptから2案程度を作る。

## 6. Pair scoring

titleとthumbnailを別々に最高得点へしない。

`pair_score = clarity + curiosity + complementarity + promise_match + differentiation - confusion - policy_risk`

同じ情報を重複するpairは減点。

## 7. Mobile test

- 10%縮小
- grayscale check
- 1-second recognition
- title truncation preview
- dark/light interface preview
- adjacent competitor simulation

## 8. AI thumbnail safety

- 実在人物の表情・行為を捏造しない
- 架空画像を証拠写真のように見せない
- 事件被害者を刺激的に利用しない
- 画像内文字の誤りを残さない
- 実在ロゴ・商標の偶発生成を確認

## 9. Experiment record

- experiment_id
- episode_id
- variant IDs
- start/end
- change type
- audience exposure
- impressions
- CTR
- watch time per impression
- first 30s retention
- traffic source
- confounders
- result
- confidence
- decision

## 10. Decision rule

CTRが高くても、期待と本編がずれて初期離脱が悪化する案は勝者ではない。

主要評価：
`watch time per impression` と `viewer satisfaction proxies`

## 11. Learning library

記録するのは「赤文字が勝つ」のような表層ルールではない。

- theme familiarity
- focal object type
- human vs object
- scale contrast
- question type
- title syntax
- specificity
- emotional promise
- channel maturity

## 12. Preproduction kill signal

強いpackage hypothesisを一つも作れないテーマは、企画自体が弱い可能性がある。調査開始前にreframeまたはholdする。
