# 05 — Script, Story and English Style

## 1. 台本は情報の集合ではない

良い動画は、一つの認識変化を提供する。

中心命題の基本形：

> 多くの人はXだと思っている。しかしYを理解すると、実際にはZであることが分かる。

または：

> Aが起きたのはBのせいだと説明される。しかし、より深い原因はCとDの相互作用にある。

## 2. Script Package

- `thesis.json`
- `outline.json`
- `script.en.md`
- `script.annotated.json`
- `pronunciation.json`
- `onscreen_text.json`
- `script_qc.json`
- `revision_diff.md`

一つのMarkdownへ制作指示、出典、読み、字幕を混在させない。

## 3. Thesis Test

- 何が一般的理解か。
- 何が不足しているか。
- 新しい説明は何か。
- その機構は何か。
- なぜ重要か。
- 反論は何か。
- 最後に何が残るか。

一文で言えない場合、テーマが広過ぎるか、切り口が定まっていない。

## 4. 視聴者への約束

冒頭30〜60秒で以下を伝える。

- 何についての動画か。
- なぜ重要か。
- 何が意外か。
- 最後まで見ると何が分かるか。

すべてを隠して意味不明にしない。一方で、結論を全部先に言って緊張を失わない。

## 5. Hook Patterns

- paradox
- impossible number
- hidden cause
- consequence before cause
- ordinary object, extraordinary system
- myth versus evidence
- moment before collapse
- unanswered question
- map or scale reveal
- human decision with systemic consequence

禁止：

- 毎回“This is the story of…”
- 内容と無関係な恐怖
- 長いチャンネル挨拶
- 空の予告
- 事実ではない極端な断定

## 6. 標準構造

1. Cold open
2. Central question
3. Common explanation
4. Hidden complication
5. Historical/systemic context
6. Escalation
7. Turning point
8. Counterargument
9. Synthesis
10. Consequence
11. Final insight
12. Resonant ending

テーマに応じて変えてよいが、単なる時系列羅列は禁止。

## 7. Chapter Design

各章：

- function
- question opened
- question answered
- new tension
- claims
- visual opportunities
- emotional tone
- transition
- target duration

役割のない章は削除。

## 8. English Style Profile

- intelligent but accessible
- authoritative but not omniscient
- cinematic but restrained
- concrete before abstract
- active voice preferred
- varied rhythm
- no fake intimacy
- no empty hype
- no generic AI filler
- no repeated rhetorical questions
- no excessive em dash
- no unsupported superlative
- no unnecessary “in conclusion”

## 9. AIっぽさを抑える

頻出定型句をlintする。

例：

- But here’s the thing.
- What happened next changed everything.
- The answer may surprise you.
- It wasn’t just X. It was Y.
- In a world where...
- Little did they know...
- The truth is more complicated.

使用禁止ではないが、繰り返しと空疎な使い方を避ける。

## 10. Narration Readability

自動検査：

- sentence length distribution
- paragraph breath length
- difficult proper noun density
- acronym expansion
- number pronunciation
- repeated n-grams
- discourse marker repetition
- passive voice overuse
- vague pronouns
- unsupported certainty
- scene-unfriendly abstractions

## 11. 情報密度

- 一文一機能
- 一段落一論点
- 一シーン一つの視覚責任
- 固有名詞を連続投入しない
- 数字に比較対象を与える
- 抽象概念の後に具体例
- 原因と相関を区別
- 主張後に「なぜ」を回収
- 重要点は形を変えて再提示
- 同義反復を削る

## 12. 台本の多層構造

分離する：

- narration_text
- claim/source annotations
- pronunciation hints
- pacing/emotion notes
- on-screen text
- visual intent
- music intent
- editor notes

ナレーション本文へ`[show map]`等を混ぜない。

## 13. Revision Passes

1. Structural pass
2. Evidence pass
3. Logic pass
4. Audience comprehension pass
5. English naturalness pass
6. Narration performance pass
7. Compression pass
8. Final claim-link audit

一回のプロンプトで全部を直さない。

## 14. Compression Rules

削る：

- 同義反復
- 情報のない予告
- 映像で明白な説明
- 重要でない固有名詞
- 結論へ影響しない脇道
- 例が多過ぎる箇所
- 抽象的な美辞麗句
- 章間の重複

残す：

- 因果をつなぐ文
- 誤解を防ぐ限定
- 反証
- スケール感
- 人間的な具体
- 結論を支える証拠

## 15. 長さ

固定時間に文章を無理に合わせない。

想定時間は読み上げ速度から計算し、シーン設計とdraft voiceで検証する。情報密度が低いなら長くせず、構成を再設計する。
