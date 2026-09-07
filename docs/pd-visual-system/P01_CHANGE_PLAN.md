# P01 CHANGE PLAN — PD Visual System v2

> **統合メモ(2026-07-12)**: 本書はP00監査の一部。P01=「現在版60〜90秒baseline保存」。
> 本セッションで **baseline候補A（110.1–190.5s）は既に非破壊抽出済み**（`outputs/pd-visual-system/PD-2026-009-timbs/baseline/` ＋ `BASELINE_DIAGNOSIS.md`）＝P01実作業の先行完了分。
> ツール導入を伴う後続（P03素材検索〜P10 AI B-roll）の計画は `TOOL_INSTALLATION_PLAN.md`、リスクは `RISK_REGISTER.md` を正とする。**P01自体は新ツール不要**（既存ffmpeg/ffprobeのみ）。

- Episode: `PD-2026-009-timbs`
- Authored during: **P00** (計画。P01 baseline は既に先行実行済み・後続は自動着手しない)
- P01 名称: **Baseline保存・紙芝居診断**（`.claude/skills/pd-phase-01-baseline`）
- P01 目的: 比較価値の高い連続60〜90秒を選び、現在版(baseline)を保存し、紙芝居要因8軸を測定する。
- P01 書き込み許可範囲（safety-policy）: **`docs/pd-visual-system` / `outputs/pd-visual-system` / `templates/pd-visual-system` のみ**。

## 1. baseline 候補（60〜90秒）と選定理由

原本: `H:\pd-media\...\08_edit\renders\timbs_premium_review_v001.mp4`（1920×1080 / 30fps / 732.52s）。
> タイムコードは shotlist 相対。実レンダは +≈12.5s のブランド枠があるため、**P01 の最初の作業で実mp4に対しフレーム窓を再確定**（ffprobe/場面境界の目視）してから抽出する。

| 候補 | 区間(相対) | 長さ | 内容 | core-5 マッピング | 推奨度 |
|---|---|---:|---|---|---|
| **A** | SPN-0005–0007 ≈106.6–191.0s | ≈84s | No prison → **$10,000罰金 vs ~$42,000車** → "grossly disproportionate" | `PenaltyVsProperty`＋`QuoteUnderExamination`＋`EvidenceReveal` | ★推奨 |
| B | SPN-0017–0018 ≈412.1–485.4s | ≈73s | 「州を拘束?Indianaはno」→「2019 9–0, 586 U.S. 146」 | `VerdictReversal`＋`CaseJourney` | 次点 |
| C | SPN-0009–0011 ≈207.5–278.9s | ≈71s | 「訴訟は財産に対して」/「in rem / One 2012 Land Rover」 | `CaseJourney`／`EvidenceReveal` | 予備 |

**推奨=A**。理由:
1. **本編の主張の核**（罰金上限と車価値の不均衡＝Excessive Fines 条項の争点）で、視聴維持の山場。改善効果が最も可視化しやすい。
2. **core-5 の当たりが最も密**（金額対比＝`PenaltyVsProperty`、判事の "grossly disproportionate" 引用＝`QuoteUnderExamination`）。B/C は 1〜2 部品。
3. 現状が **motion_graphic 1点＋Ken Burns 静止画中心**で、紙芝居→意味あるモーションへの Before/After 比較が明快。
4. 84s は 60〜90s 帯内で、A/B/C いずれも**ナレーション区切りが自然**（同一ナレで後続版と比較可能＝P01受入基準を満たす）。

## 2. P01 で作成するファイル（`outputs` と `docs` のみ）

| ファイル | 内容 | 書込先(許可範囲内) |
|---|---|---|
| `outputs/pd-visual-system/PD-2026-009-timbs/baseline/baseline_A.mp4` | 候補Aを **無劣化抽出**（H:原本を read、ffmpeg で切り出し） | outputs/pd-visual-system ✅ |
| `outputs/pd-visual-system/PD-2026-009-timbs/baseline/render_manifest.json` | 再現可能な抽出manifest（原本パス/sha256・区間・fps・コマンド） | outputs ✅ |
| `outputs/pd-visual-system/PD-2026-009-timbs/baseline/baseline_shots.json` | 区間内ショットの visual question / start-end state / 8軸スコア | outputs ✅ |
| `docs/pd-visual-system/BASELINE_DIAGNOSIS.md` | 紙芝居要因8軸の採点・所見・改善仮説 | docs ✅ |
| `docs/pd-visual-system/IMPLEMENTATION_STATUS.md`（更新） | P01 結果反映 | docs ✅ |
| `docs/pd-visual-system/PHASE_STATE.json`（ステータスのみ→candidate_complete） | current_phase は変えない | docs ✅ |

## 3. P01 で **変更しない / 触らない** ファイル（保護）

- `remotion/**`（`TimbsPremium.tsx`, `CasePremiumFromRoughCut`, `timbs_roughcut.ts`, `remotion.config.ts`, `brand.ts` 等）— **一切変更しない**。P01は診断のみ。
- `H:\pd-media\**`（assets/renders 含む）— **read-only**。抽出出力は repo `outputs/` へ。原本 mp4 も上書きしない。
- `episodes/PD-2026-009-timbs/**`（台本・shotlist・captions・renders・manifest）— 変更しない。
- `schemas/**`, `src/**`, `config/**`, `.claude/**` — P01 範囲外。
- Git 履歴 — commit/push/merge/rebase/reset/clean 無し。

## 4. 想定コマンド（P01・すべて非破壊）

- 抽出: `ffmpeg -ss <in> -to <out> -i <H:原本> -c copy <outputs/.../baseline_A.mp4>`（stream copy でGOP境界に丸め／必要なら再エンコードは CRF16 libx264 で repo outputs にのみ書く）。
  - 注: `ffmpeg -y` は safety-policy で **ask**。出力は新規パスなので `-y` 不要（上書きしない）。
- 解析: `ffprobe`（区間確定）、`ffmpeg` の `signalstats`/`freezedetect`/`select`+optical-flow で 8軸測定（メトリクスは MASTER_REFERENCE の紙芝居定義／既存 `check_*` 指標に整合させる）。

## 5. 紙芝居 8軸（P01 で採点予定・BASELINE_DIAGNOSIS.md の枠）

MASTER_REFERENCE / ship-gate（`animation_density`, near-still, mean-luma, optical-flow, footage_diversity）に整合した8軸で採点する。一次観察（P00時点・未計測の仮説）:
- 区間A は motion_graphic 1（SPN-0006）＋ Ken Burns 静止画中心 → **optical-flow が低い区間が混在する疑い**。P01 で実測して確定。

## 6. P01 の受入基準（skillより）

- 同一ナレーションで後続版と比較できる（baseline mp4 or 再現manifest）。
- 各ショットに visual question と start/end state。
- 紙芝居要因8軸が採点済み。

## 7. rollback（P01）

- 追加した `outputs/pd-visual-system/PD-2026-009-timbs/baseline/*` と `docs/.../BASELINE_DIAGNOSIS.md` を削除。
- `PHASE_STATE.json` / `IMPLEMENTATION_STATUS.md` を P01 開始前へ戻す。
- 既存 remotion / H: / episode 資産は不変のため、他への影響なし。

## 8. P01 開始前の前提確認

- P00 が `candidate_complete`（本書はその状態で提出）。**owner の Go 判定と `/pd-phase-advance P01` が P01 着手の前提**（本Phaseでは実行しない）。
- Remotion 実インストール版の読み取り確認（ENVIRONMENT_AUDIT §8-3）を P01 冒頭に実施推奨。
