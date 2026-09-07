# PD Visual System Implementation Status

> このファイルは現状の正本です。実装済みと予定を混ぜないでください。

## Current phase

- Phase: `P12`（結果分析と全編展開判断）
- Status: `candidate_complete` — **全13フェーズ P00-P12 完了**。
- **判定=Go(EP37展開)**。進化版パイプライン中核（検索/コア5/語同期/2.5D/Evidence Room/仕上げ）を timbs test-bench で1変更ずつ実証。総括=`P12_DECISION.md`。
- Wan2.2実生成はDL完了後（穴埋め限定）。既存環境は全工程無傷。
- Episode(実験台): `PD-2026-009-timbs` / **本番適用対象: EP37以降**（DEC-20260712-002）
- Last verified: `2026-07-12 (JST)` by `claude-code`（実測・実レンダ目視）
- **進行**: owner「全部やって・止めずに進めて」で P00→P05 を実行。P03=PySceneDetect隔離導入、P04=OpenCLIP意味検索、**P05=コア5部品実装（typecheck exit0＋5部品を実レンダ目視確認）**。既存環境は無傷。方針=過去話は作り直さず進化版はEP37から（DEC-20260712-002）。
- **経緯（統合）**: 本セッションで owner「go/P02 go」により機械的に P00→P01→P02 まで前進。その後 owner が詳細ブリーフで「今回はP00だけ・自動で先へ進むな」を再指示 → **P02 Web作業を破棄し current_phase を P00 に再スコープ**（履歴は保持）。P01 baseline(候補A) と関連成果物は先行完了分として保持。
- **P00成果物4点**: `ENVIRONMENT_AUDIT.md`(AIツール監査§9追補) / `TOOL_INSTALLATION_PLAN.md` / `P01_CHANGE_PLAN.md` / `RISK_REGISTER.md`。

## Environment summary

| Item | Verified value | Evidence | Status |
|---|---|---|---|
| OS | Windows 11 Pro 10.0.26200 (64-bit) | `Get-CimInstance Win32_OperatingSystem` | verified |
| CPU | i9-13900KF 24C/32T | `Win32_Processor` | verified |
| RAM | 127.8 GB | `Win32_ComputerSystem` | verified |
| GPU / VRAM | RTX 4090 / 24564 MiB, driver 591.86 | `nvidia-smi` | verified |
| CUDA | driver 13.1 / toolkit(nvcc) 11.8 | `nvidia-smi`, `nvcc --version` | verified |
| Python | 3.10.11 | `python --version` | verified |
| Node / package manager | Node v24.16.0 / npm 11.13.0 / pnpm 9.12.0 | `--version` | verified |
| Remotion | 宣言 `^4.0.0`（motion-blur ^4.0.476） | `remotion/package.json` | declared（実版は非起動で未確認） |
| FFmpeg / ffprobe | 8.1.1-full (gyan.dev) | `-version` | verified |
| DaVinci / Blender / ComfyUI | 全て存在（Resolve.exe / Blender 5.1 / `~/ComfyUI`） | `Test-Path` | verified（存在のみ） |
| Media root | `H:\pd-media` 存在（assets/brand/downloads/episodes/library） | `Test-Path` | verified |
| Free disk | C:280.4GB / H:3222.7GB(T7) / D/E/F ~1.5TB | `Win32_LogicalDisk` | verified |
| Baseline render | `H:\...\timbs_premium_review_v001.mp4` 1920×1080/30fps/732.52s/559MB/aac48k | `ffprobe` | verified |

## Completed deliverables

- **P00**: `ENVIRONMENT_AUDIT.md` / `REPOSITORY_AUDIT.md` / `P01_CHANGE_PLAN.md` / `P00_EVIDENCE.md`（実測監査）
- **P01**: `outputs/pd-visual-system/PD-2026-009-timbs/baseline/{baseline_A.mp4, render_manifest.json, baseline_shots.json}` ＋ `docs/pd-visual-system/BASELINE_DIAGNOSIS.md`
  - baseline_A = 候補A（110.1–190.5s / 80.4s / 30fps）。原本read-only・非破壊抽出（CRF16）。
  - 実測: 全体motion YAVG 2.27 / カット29(≈2.8s毎) / near-still 11.77s(14.6%)。主役A(SPN-0006)=motion 0.87・SPN-0007=0.63＝**主役級が近静止**（紙芝居の実数裏付け）。
  - 8軸合計 51/96（53%）。hard blocker=SPN-0006主役A近静止 / SPN-0005末尾freeze。
- **P02**: `BENCHMARK_FINDINGS.md` / `COPY_BOUNDARY.md` / `benchmarks/benchmark_shots.jsonl`（repo正典ベース・9原理・一次タイムコードは要検証明示）/ `P02_EVIDENCE.md`
- **P03**: `scripts/pd-visual-system/scene_index_poc.py` ＋ `data/pd_vs_scene_index.sqlite` ＋ サムネ861枚(H:previews) ＋ `asset_index_report.md`。**PySceneDetect 0.7 を `D:\PD_AI_Tools\PySceneDetect\.venv` に隔離導入**。150点/0エラー/287カット/2.68s per点。再開・エラー継続・VFR保持を実証。
- **P04**: `scripts/pd-visual-system/clip_search_poc.py` ＋ `data/pd_vs_clip_{index.npz,manifest.json,eval.json}` ＋ `semantic_search_report.md` ＋ `MODEL_LICENSE_RECORD.md`。**OpenCLIP ViT-B/32**（既存GPU env・重み605MBのみDL・sha記録）。287フレーム埋め込み・20クエリ評価（目視4件・実用≈80%）。
- **P05**: `remotion/src/components/core5/{index,preview}.tsx` ＋ Root.tsx `PDCore5` 登録 ＋ `core5_report.md`。**コア5部品**（motionkit合成）。typecheck exit0＋5部品を実レンダ目視（`outputs/pd-visual-system/core5_check/`）。
- 本 `IMPLEMENTATION_STATUS.md` 更新

## Current blockers

- なし（進行上のブロッカー無し）。ただし後続 P03+ で schemas を触る前に **scene-plan / qc-report スキーマ同名衝突3件**（INSTALLATION_REPORT §9）の owner 解決が前提。

## Assumptions

- 事前仮定（Windows/RTX4090/Remotion/`H:\pd-media`）は **P00 で実測確認済み**。RTX4090=24GB, fps30, media root 実在を確認。
- baseline のフレーム窓は shotlist 相対の近似（実レンダ +≈12.5s のブランド枠）。**P01 冒頭に実mp4で再確定**。

## Decisions

- 新しい総合管理アプリは作らない。
- 実行はPhase別Skill、詳細思想はMASTER_REFERENCEを正本とする。
- Phaseは自動で進めない。
- コアRemotion部品は5つに固定する。

## Pending approvals

- なし

## Next safe actions

1. Owner が P01 baseline（`baseline_A.mp4` と `BASELINE_DIAGNOSIS.md`）を確認し、Go / No-Go を判定する。
2. Go の場合のみ owner 承認のもと P02（`pd-phase-02-benchmark`）へ前進（`/pd-phase-advance P02` 相当）。
3. それまで P02 以降へは進めない（自動着手しない）。

## Rollback notes

- P00 の変更は `docs/pd-visual-system/` の 4 文書追記／更新 と `PHASE_STATE.json` のステータス（not_started→in_progress→candidate_complete）のみ。
- Rollback: (a) 追加/更新した4文書を編集前へ戻す、(b) `PHASE_STATE.json` を `not_started` / `history:[]` に戻す。既存 remotion / H: / episode 資産・Git 履歴・未コミット75変更には未接触のため他影響なし。

## Experiment results

| Variant | Change from previous | Understanding | Paper-theater reduction | Trust | Reuse | Human minutes | GPU minutes | Decision |
|---|---|---:|---:|---:|---:|---:|---:|---|
| A | Current baseline |  |  |  |  |  |  | pending |
| B1 | Asset search + core 5 |  |  |  |  |  |  | pending |
| B2 | + word sync |  |  |  |  |  |  | pending |
| B3 | + one 2.5D shot |  |  |  |  |  |  | pending |
| C1 | + one Evidence Room shot |  |  |  |  |  |  | pending |
| C2 | + one AI B-roll shot |  |  |  |  |  |  | pending |
| C3 | + finishing |  |  |  |  |  |  | pending |
