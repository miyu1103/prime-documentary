---
paths:
  - "**/*.py"
---
# Python Rules

- Python 3.11+相当を想定し、型注釈を付ける。
- domain、application、adapter、infrastructureを可能な範囲で分離する。
- provider SDKをdomainへ直接漏らさない。
- dataclass/Pydantic等で入出力を明示する。
- 例外を握りつぶさず、error taxonomyへ変換する。
- structured loggingを使い、secretや本文全体を無警戒に記録しない。
- side effectを関数名とinterfaceで明確にする。
- retryは呼出し箇所へ散在させず共通化する。
- file writeは可能ならatomicに行う。
- timezone-aware datetimeを使う。
- OS固有パスをDBの真実にしない。
- CLIは明確なexit codeと`--dry-run`を持つ。
- public functionにはdocstringまたは明確な型・命名を持つ。
