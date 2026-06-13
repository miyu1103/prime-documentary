---
paths:
  - "tests/**/*"
  - "**/test_*.py"
---
# Testing Rules

- happy pathだけでなくresume、duplicate、budget、stale、permission、provider failureを試験する。
- 外部APIはunit testで実課金しない。
- integration testは明示フラグと予算上限を持つ。
- fixtureに実secret・個人情報を入れない。
- golden episodeでcross-artifact consistencyを検証する。
- flaky testを無言でskipしない。
- destructive operationはdry-run testを必須にする。
