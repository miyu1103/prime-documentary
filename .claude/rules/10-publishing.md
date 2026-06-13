---
paths:
  - "**/publish/**/*"
  - "src/**/publish*"
---
# Publishing Rules

- upload既定はprivate。
- channel IDをallowlistで検証する。
- video hashと既存uploadを確認する。
- approvalがcurrent revisionへ有効か確認する。
- title、thumbnail、descriptionの約束が本編と一致する。
- rights manifestとQC reportが揃わなければpublic化しない。
- timezoneとschedule日時を明示する。
- public化後にURLとplatform stateを再確認する。
