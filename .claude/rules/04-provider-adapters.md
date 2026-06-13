---
paths:
  - "src/**/adapters/**/*"
  - "src/**/providers/**/*"
---
# Provider Adapter Rules

- provider固有型をdomainへ漏らさない。
- external request IDとidempotency keyを保存する。
- timeout、rate limit、auth、5xx、rejectionを区別する。
- retry前に外部side effectの有無を確認する。
- estimated/actual usageとcostを記録する。
- raw metadataはredactして別参照へ保存する。
- fallbackは品質、権利、費用差を明示する。
- API仕様は実装時点の公式文書を確認する。
- 非公式UI automationは既定で無効。
- provider termsの確認日を記録する。
