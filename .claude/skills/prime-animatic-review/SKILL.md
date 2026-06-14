---
name: Prime Documentary Animatic Review P0
description: Implement the P0 local animatic review interface for Prime Documentary, including playback, timecoded markers, Japanese comments, JSON saving, autosave, resume, keyboard shortcuts, one-command local launch, tests, and smoke test. Use only when explicitly invoked for the Prime Documentary animatic review workflow.
disable-model-invocation: true
---

# Prime Documentary Animatic Review P0

You are working on the Prime Documentary local production repository.
The immediate goal is not to build a full production dashboard. The immediate goal is to let the owner safely watch the Miranda v. Arizona Episode 1 animatic locally and record structured review feedback.

## Full contract

Read this full implementation contract before making changes:

- [Prime Documentary Claude Code implementation spec 100](reference/PRIME_DOCUMENTARY_CLAUDE_CODE_IMPLEMENTATION_SPEC_100.md)

Treat that reference file as the task contract for this workflow.
If the reference file and actual repository conflict, the actual repository is the source of truth for paths, existing commands, schemas, and tests.

## Required behavior before editing

Do not start implementation immediately. First inspect the repository and report in Japanese:

1. Animaticの現在の起動方法
2. Remotion / React / TypeScript / Python / schema / tests の既存構成
3. 最小レビュー画面を追加する最も安全な場所
4. 変更予定ファイル
5. 新規作成予定ファイル
6. 既存機能への影響
7. 実装しない項目
8. テスト方法
9. ロールバック方法
10. 進行上のリスクと回避策

After reporting, proceed with the P0 minimum implementation unless a stop condition applies.

## Stop conditions

Stop and ask the owner before any of the following:

- Paid API or paid service execution
- External publishing, external upload, or YouTube operation
- Changes to approved script, claims, sources, factual/legal content, or portrayal of real people
- Brand or channel strategy changes
- Destructive operation, data deletion, force push, history rewrite, or irreversible migration
- Displaying, storing, transmitting, or modifying secrets, API keys, or `.env` contents
- Security compromise or relaxation
- Scope expansion beyond P0

## P0 acceptance criteria

Implement only the minimum local review workflow:

- Animatic playback
- Current timecode capture
- First-pass markers: `good`, `confusing`, `needs_fix`, `check_later`
- Second-pass Japanese comments with `category` and `severity`
- JSON as source of truth
- Draft autosave
- Resume after interruption
- Keyboard shortcuts
- One-command local launch
- Browser auto-open when reasonable in the existing stack
- Existing tests remain green
- New focused tests for schema/save logic where appropriate
- Smoke test instructions and result report

Do not implement Phase 1+ items such as full dashboard, SQLite, paid media generation, YouTube integration, Midjourney/Runway/ElevenLabs automation, 2.5D pipeline, or backup-system productionization.

## Final report requirements

Report in Japanese:

- 操作方法
- local URL
- 保存されるJSONファイル
- backup/autosave behavior
- keyboard shortcuts
- tests run and results
- known limitations
- rollback method
- next owner action
