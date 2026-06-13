# 14 — Claude Code Operating Model

## 1. 情報の階層

### CLAUDE.md

毎回必要な短い原則。長大な手順を詰め込まない。

### `.claude/rules/`

特定領域の不変ルール。Python、schema、secrets、provider、artifact等。

### `.claude/skills/`

繰り返し使う多段手順。必要時だけ読み込む。

### `.claude/agents/`

専門役割。独立コンテキストで調査・監査・設計を行う。

### `docs/`

詳細仕様。作業前に該当文書を読む。

### `schemas/`, `examples/`, `tests/`

自然言語より強いデータ契約。

## 2. Claude Codeへの依頼形式

悪い例：

> 自動化して。

良い例：

> `docs/08_EDITING_DAVINCI_AUTOMATION.md`と既存実装を確認し、scene planからreview timeline planを生成する縦断機能を実装してください。既存機能を壊さず、schema、validator、fixture、unit tests、CLI、migration notesを含めてください。外部DaVinci操作はadapter interfaceまでとし、まずdry-runでtimeline planを検証してください。

## 3. 実装前報告

- understanding
- assumptions
- files inspected
- current behavior
- target behavior
- gap
- risks
- proposed changes
- tests
- non-goals

ただし、明確な小修正では過度な報告で止まらず実装する。

## 4. 実装後報告

- changed files
- behavior
- commands run
- test results
- migrations
- remaining risks
- manual steps
- rollback
- next priority

## 5. Subagent Use

推奨：

- 並列可能な調査を分ける。
- 同じファイルを複数agentが同時編集しない。
- agent出力を親が検証する。
- fact checkerはwriterを独立監査。
- architecture変更はautomation architect。
- 完了前にqa auditor。
- agent memoryへ長期的コード知識だけ保存。

## 6. Context Control

巨大文書を毎回全部読ませない。

- task-specific docs
- skill body
- exact file references
- structured summary
- schema
- relevant tests

を使う。

## 7. Skillsの設計

Skillは次を含む。

- いつ使うか
- 必須参照文書
- 入力
- 実行手順
- 出力
- quality gates
- failure behavior
- prohibited actions

例：

- `/pd-audit`
- `/pd-new-episode`
- `/pd-run-pipeline`
- `/pd-research`
- `/pd-script`
- `/pd-scenes`
- `/pd-generate-assets`
- `/pd-build-edit`
- `/pd-qc`
- `/pd-retro`
- `/pd-resume`
- `/pd-migrate`

## 8. Hooksの役割

LLM判断に任せず必ず行うもの：

- secret scan
- protected file guard
- destructive command guard
- schema validation
- manifest validation
- format/lint/test
- status report
- approval boundary guard

CLAUDE.mdは強制機構ではないため、禁止操作はhook/permissionで止める。

## 9. Permission Design

通常許可：

- repository read
- non-destructive local write
- tests/lint
- dry-run
- validators

要承認：

- network write
- external API cost
- upload
- delete
- git history rewrite
- credentials
- production DB
- public publish

禁止：

- secret exfiltration
- blanket dangerous bypass
- unscoped delete
- unknown binary execution
- public upload without approval

## 10. Claude Codeに期待しないこと

- 曖昧な口頭ルールを永続的に正確に覚えること
- 外部サービス仕様が永遠に変わらないこと
- 一度の巨大プロンプトで完璧な制作物を出すこと
- 人間の意図を未定義のまま推測し続けること
- 品質スコアだけで権利や事実責任を負うこと

そのため、schema、test、hook、approval、event logを使う。

## 11. Claude Codeの推奨開始手順

1. `BOOTSTRAP_PROMPT.txt`を実行。
2. 現状調査のみ。
3. 差分報告。
4. Phase 1の縦断実装。
5. sample episodeで検証。
6. qa-auditorレビュー。
7. docs更新。
8. 次Phaseへ進む。
