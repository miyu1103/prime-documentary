---
paths:
  - "schemas/**/*.json"
  - "**/migrations/**/*"
  - "examples/**/*.json"
---
# Schema and Migration Rules

- schemaには`schema_version`を持たせる。
- breaking changeはversionを上げ、migrationを用意する。
- requiredとoptionalを曖昧にしない。
- enumは将来拡張と未知値の扱いを設計する。
- sampleは常にvalidatorを通す。
- approval対象revisionが変わる変更では承認失効を考慮する。
- ID formatを変える場合は全参照とfilenameへの影響を調査する。
- 既存episodeを無言で書き換えない。
- migrationはdry-run、backup、rollback noteを持つ。
