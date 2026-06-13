# 12 — Quality Gates and Acceptance

## 1. Quality Philosophy

平均点だけで通さない。重大欠陥は一つでもblocker。

Severity：

- S0：情報
- S1：軽微、公開可
- S2：修正推奨
- S3：公開前に修正必須
- S4：重大、工程差戻し
- S5：公開事故・法的・アカウントリスク

## 2. Topic Gate

- [ ] central question is specific
- [ ] viewer promise is credible
- [ ] channel fit
- [ ] demand evidence
- [ ] differentiated angle
- [ ] sufficient depth
- [ ] research feasible
- [ ] visual feasible
- [ ] risk acceptable
- [ ] economics acceptable

## 3. Research Gate

- [ ] source registry complete
- [ ] critical claims A/B support
- [ ] dates verified
- [ ] numbers verified
- [ ] quotes contextualized
- [ ] counterevidence included
- [ ] uncertainty captured
- [ ] current facts timestamped
- [ ] rights notes
- [ ] no E claims intended for script

## 4. Script Gate

- [ ] thesis in one sentence
- [ ] hook opens a real question
- [ ] promise is paid off
- [ ] each chapter has function
- [ ] causal logic
- [ ] counterargument
- [ ] factual spans linked
- [ ] no unsupported certainty
- [ ] natural English
- [ ] speakable
- [ ] no repetitive filler
- [ ] duration justified
- [ ] conclusion creates insight

## 5. Visual Gate

- [ ] every required scene covered
- [ ] semantic match
- [ ] continuity
- [ ] no obvious anatomy defects
- [ ] no accidental text/watermark
- [ ] no anachronism
- [ ] no misleading evidence portrayal
- [ ] crop safe
- [ ] adequate diversity
- [ ] correct rights status
- [ ] important visuals reviewed

## 6. Audio Gate

- [ ] exact script coverage
- [ ] pronunciation
- [ ] no missing/duplicate phrase
- [ ] consistent voice
- [ ] clean seams
- [ ] no clipping
- [ ] target loudness
- [ ] music rights
- [ ] narration intelligible
- [ ] no distracting SFX

## 7. Edit Gate

- [ ] no offline media
- [ ] scene timing
- [ ] visuals support narration
- [ ] no excessive repeated shot
- [ ] no black frames
- [ ] no accidental logos/text
- [ ] subtitles complete
- [ ] chapter markers
- [ ] citations/disclosure
- [ ] audio mix
- [ ] technical render
- [ ] opening quality
- [ ] ending quality

## 8. Package Gate

- [ ] title clear
- [ ] thumbnail clear at mobile size
- [ ] title and thumbnail complement
- [ ] promise matches video
- [ ] description accurate
- [ ] chapters correct
- [ ] subtitle language correct
- [ ] playlist correct
- [ ] rights manifest complete
- [ ] approval revision matches
- [ ] privacy/schedule correct

## 9. Automation Acceptance Tests

新機能は以下を検証。

- happy path
- validation failure
- retryable provider failure
- terminal failure
- interrupted process resume
- duplicate request
- budget limit
- permission denial
- stale input
- schema migration
- log redaction
- documentation example
- dry-run
- rollback

## 10. Golden Episode

代表的な一話をgolden fixtureとして保持。

比較：

- manifest validity
- claim coverage
- scene coverage
- asset count
- timeline duration
- missing media
- audio duration
- package completeness
- cost estimate
- deterministic outputs

クリエイティブ出力の完全一致は要求しない。

## 11. Human Review Design

人間へ全成果物を漫然と見せず、以下を優先表示。

- blocker
- low confidence
- revision diff
- high-risk claims
- top candidate comparisons
- repeated failures
- budget exceptions
- visual inconsistencies
- publish-impacting changes

## 12. Quality Promotion

工程をL3/L4へ昇格する時：

- sample size
- false pass rate
- false fail rate
- human override rate
- severity distribution
- rollback success
- cost stability
- provider stability

を確認する。
