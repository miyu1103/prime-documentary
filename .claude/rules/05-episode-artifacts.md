---
paths:
  - "episodes/**/*"
  - "examples/episode/**/*"
---
# Episode Artifact Rules

- `manifest.json`を中心にする。
- 承認済み成果物を上書きせず新revisionを作る。
- `final`, `latest`, `new`, `fixed`を版名に使わない。
- scene、claim、asset、voice chunk間の参照を保つ。
- stale artifactを削除せず再計算対象として示す。
- raw、candidate、approved、rejectedを分離する。
- temporary fileを正式成果物として扱わない。
- approved assetの削除には参照確認と承認が必要。
