# P00 EVIDENCE REPORT — PD Visual System v2

- Episode: `PD-2026-009-timbs` / Phase `P00` (環境・リポジトリ監査)
- By: `claude-code` / 2026-07-12 (JST)
- 種別: read-only 監査。install/upgrade/download/render/H:書込/git変更 は **一切なし**。

## 1. 完了状態
- P00 = **candidate_complete**（`current_phase` は P00 のまま変更せず。human 承認待ち）。

## 2. 成果物（すべて `docs/pd-visual-system/`）
- `ENVIRONMENT_AUDIT.md` — OS/CPU/RAM/GPU/CUDA/ドライブ/ツール/Remotion設定/リスク（実測）
- `REPOSITORY_AUDIT.md` — Git状態・safety・ビルド/レンダ手順・エピソード資産・baseline原本ffprobe・28ショット・候補・リスク
- `P01_CHANGE_PLAN.md` — baseline候補A/B/C・作成/保護ファイル・コマンド・8軸枠・rollback
- `IMPLEMENTATION_STATUS.md` — 更新（環境サマリ verified・完了物・次アクション・rollback）
- 本 `P00_EVIDENCE.md`

## 3. 実行コマンドと主な出力（証拠）
```
phase_gate.py assert --phase P00        → OK: P00 is current; status=not_started (exit0)
phase_gate.py start  --phase P00        → Started P00（history 1件・重複なし, in_progress）
git rev-parse --abbrev-ref HEAD         → claude/vibrant-archimedes-2mmr5h
git log -1 --oneline                    → 97dd18df EP34 rolin: schedule ...
git status --short | 集計               → 修正(M) 75 / 未追跡(??) 928
python --version                        → 3.10.11
node/npm/pnpm --version                 → v24.16.0 / 11.13.0 / 9.12.0
git --version                           → 2.55.0.windows.2
ffmpeg -version / ffprobe -version      → 8.1.1-full_build (gyan.dev)
nvidia-smi ...                          → RTX 4090, 24564 MiB, driver 591.86, CUDA 13.1
nvcc --version                          → CUDA toolkit 11.8 (V11.8.89)
Win32_OperatingSystem/Processor/...     → Win11 Pro 26200 / i9-13900KF 24C32T / 127.8GB
Win32_LogicalDisk                       → C:280.4 / D:1548.4 / E:1577.2 / F:1548.4 / H:3222.7 GB free
Test-Path H:\pd-media                   → True（assets/brand/downloads/episodes/library）
Test-Path Resolve.exe / Blender5.1 exe  → True / True ; ~/ComfyUI 存在
ffprobe timbs_premium_review_v001.mp4   → h264 1920x1080 30/1fps 21975f dur=732.522667s ; aac 48k stereo 317k ; 559MB
validate_kit.py --project-root .        → exit1（既知の想定内: kit専用REQUIRED欠落＋auth model＋scene-plan/qc-report 同名衝突。INSTALLATION_REPORT §10）
```

## 4. baseline 候補（60〜90秒・shotlist相対／実mp4はP01で再確定）
- **A（推奨）** 106.6–191.0s ≈84s: $10,000罰金 vs ~$42,000車 →"grossly disproportionate"（PenaltyVsProperty+QuoteUnderExamination+EvidenceReveal）
- B 412.1–485.4s ≈73s: 州編入→2019 9–0 / 586 U.S. 146（VerdictReversal+CaseJourney）
- C 207.5–278.9s ≈71s: in rem / One 2012 Land Rover（CaseJourney/EvidenceReveal）

## 5. 保護状況
- 未コミット 修正75・未追跡928 を保護（本Phaseで stage/commit/revert なし）。バックアップ `.pd-visual-system-backup_20260712_023308/` 健在。
- `remotion/**`・`H:\pd-media\**`・`episodes/**`・`.git` 未接触。

## 6. blocker / 未確認
- blocker なし。scene-plan/qc-report スキーマ同名衝突3件は P03+ 前に owner 解決要（本Phase無関係）。
- Remotion `node_modules` 実バージョン未確認（非起動）。P01 冒頭で読み取り確認推奨。

## 7. rollback
- 4文書＋本証拠を編集前へ戻し、`PHASE_STATE.json` を not_started/history:[] へ。既存資産・Git履歴・75変更に影響なし。

## 8. 判定
- **Conditional Go（P01）**: 環境は健全・baseline原本あり。条件＝(1) owner の候補A承認、(2) `/pd-phase-advance P01`。schemas衝突は P01（docs/outputs/templatesのみ）には非ブロッキング。
