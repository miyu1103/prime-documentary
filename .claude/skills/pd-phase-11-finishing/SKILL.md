---
name: pd-phase-11-finishing
description: Execute PD Visual System P11 (音響・カラー・C3版) only. Use when the user explicitly requests this phase for a specific episode.
argument-hint: "[episode-id]"
disable-model-invocation: true
---

# P11 音響・カラー・C3版

Episode argument: `$ARGUMENTS`. If omitted, read it from `PHASE_STATE.json`.

## Objective

音響、章転換、カラー、ラウドネスを追加し、C2との差だけを評価する。

## Mandatory start

1. Read `CLAUDE.md`.
2. Read `docs/pd-visual-system/PHASE_STATE.json` and `IMPLEMENTATION_STATUS.md`.
3. Run `python scripts/pd-visual-system/phase_gate.py assert --phase P11`.
4. Record `git status --short`, current branch, and relevant existing rules.
5. State the planned file changes and rollback before editing.

## Entry criteria
- C2が比較可能
- 既存PDの音量・カラー規則を確認済み

## Allowed scope
- 既存ルール内の音響・カラー
- ffmpeg検査
- 必要に応じ Remotion + FFmpeg 側の仕上げ検証（DaVinci は 2026-06-20 に退役・記録としてのみ残す）

## Forbidden in this phase
- GUI座標自動操作
- 音圧の過剰化
- 事実映像と再現映像の色による混同

## Required deliverables
- C3 preview
- audio/color manifest
- ffmpeg QC report

## Acceptance criteria
- 黒画面/無音/ピーク/ラウドネス検査
- C2→C3の寄与が評価可能


## Completion protocol

1. Run the phase-specific tests and validators.
2. Update `docs/pd-visual-system/IMPLEMENTATION_STATUS.md` with facts, evidence, changed files, performance, risks, limitations, rollback, and next prerequisites.
3. Update `PHASE_STATE.json` status to `candidate_complete`; do **not** change `current_phase`.
4. Run `python scripts/pd-visual-system/validate_kit.py --project-root .`.
5. Show the user the exact evidence and pending approvals. Do not invoke the next phase.
