# P00 REPOSITORY AUDIT — PD Visual System v2

- Episode: `PD-2026-009-timbs`
- Phase: `P00` (環境・リポジトリ監査)
- Audited at: 2026-07-12 (JST) by `claude-code`
- Method: read-only（`git status/log/diff` 参照、ファイル読み取り、ffprobe）。commit/push/merge/rebase/reset/clean は **未実行**。

## 1. Git 状態（保護対象）

| Item | Value |
|---|---|
| Branch | `claude/vibrant-archimedes-2mmr5h` |
| Last commit | `97dd18df` EP34 rolin: schedule private upload for 2026-07-19 12:00 JST (owner GO) |
| Working tree | **dirty**: 修正(tracked) **75**、未追跡 **928**（`git status --short` 集計） |

- 修正75 = INSTALLATION_REPORT 記載の baseline 72 ＋ kit統合で deep-merge した 3（`CLAUDE.md` / `.claude/settings.json` / `.gitignore`）。
- 未追跡928 = 主に kit 導入分（`docs/pd-visual-system/`, `config/pd-visual-system/`, `scripts/pd-visual-system/`, `.claude/{agents,hooks,rules,skills/pd-*}`, `schemas/*`, `tests/pd-visual-system/`, `templates/`）＋既存の各話生成物。
- **すべて未コミットのまま保護**。P00 は commit/stage/revert を行わない。

### 未コミット変更の保護状況
- INSTALLATION_REPORT §10 の検証で「baseline 72/72 present（path-by-path で消失/stage/revert 無し）」を確認済み。
- 統合バックアップ `.pd-visual-system-backup_20260712_023308/` に `CLAUDE.md` / `.claude\settings.json` / `.gitignore` の変更前コピー（hash一致）が保存済み。
- 本Phaseの追記（`docs/pd-visual-system/*.md` 4点＋`PHASE_STATE.json` ステータス）以外、tracked/untracked いずれのファイルも新規変更しない。

## 2. Safety / ルール（有効）

- PreToolUse: `.claude/hooks/pd_safety_gate.py`（policy `.claude/pd-safety-policy.json`, fail-closed）＋ 既存 `guard_destructive.py`。PostToolUse: `check_secrets.py`。
- protected_paths: `${PROJECT_ROOT}/.git`, `H:/pd-media/assets`, `H:/pd-media/renders/baseline`。
- 承認ゲート正規表現: pip/npm/pnpm install, winget/choco/scoop, curl/wget/hf download, git push/merge/rebase/commit, `ffmpeg -y`, upload/publish 等 → **ask**。`git reset --hard` / `git clean -fd` / `rm -rf <root>` / `Remove-Item -Recurse -Force` / format/diskpart → **deny**。
- phase_repository_write_allow: **P00 = `docs/pd-visual-system` のみ**（本Phaseの書き込みはここに限定）。
- 関連 `.claude/rules/*.md`（読了）: 00-core / 03-secrets / 05-episode-artifacts / 07-docs / 08-destructive / 11-idempotency / 12-revisions / 13-research-input / 14-cross-platform-paths / 15-llm-output / 16-approval / 17-observability / 18-no-overengineering / 19-ship-gate / docs-state / media-truth-license / remotion-motion。
  - remotion-motion: 既存 fps/解像度/Root構成/レンダ手順を先に確認、**コア5部品限定・alias増設禁止**、決定論、seed固定、秒→frame変換。
  - 19-ship-gate: 実レンダのバイト測定で緑受領書が出るまで予約/投稿しない。`animation_density`/`footage_diversity` が機械フロア。

## 3. ビルド / レンダー方法（判明）

- Remotion プロジェクト: `remotion/`（唯一の `package.json` + `remotion.config.ts`）。
- scripts: `studio`=`remotion studio`（プレビュー）, `render`=`remotion render`, `still`, `typecheck`=`tsc --noEmit`, `lint`。
- 長尺の一話は Root.tsx に **2構成**が登録される: `TimbsPremium`（本番, `CasePremiumFromRoughCut` 経由）と `RoughCut-timbs`（ラフ）。
- データ駆動: `remotion/src/data/timbs_roughcut.ts`（`scripts/import_to_remotion.py` が `04_scenes/shotlist.v001.json` + `05_stock/usable_assets.v001.json` から**自動生成**。手編集禁止）＋ `timbs_captions.ts`。
- メディア実体は `remotion/public/timbs/`（narration `timbs_final_mix_v001.mp3` 等）と `H:\pd-media`。リポジトリには大容量メディアを置かない方針（manifest warning）。

## 4. 対象エピソード PD-2026-009-timbs（実測）

`episodes/PD-2026-009-timbs/manifest.json`:
- title: "Police Can Take Your Car Without Convicting You — The Supreme Court Drew a Line"
- **state: `scheduled`**、risk_class **R2**、tier B、autonomy 3、target 12分。
- 承認: APR-0001 / APR-0002。**既に private upload 済み・公開予約**: video_id **`m-uWzgWHGPg`**、公開 2026-06-24 12:00 JST、`containsSyntheticMedia=true`。
- warnings 要点: forfeiture 批判（CLM-0008/0009）は IJ/ACLU 系＝**帰属**・中立必須・公開前R3検討；実在人物 Tyson Timbs は役割参照のみ・**AI肖像不可**；処分＝vacated & remanded（最高裁自身は没収を過大と判断せず、差戻後にIndianaが返還 CLM-0010）。

### エピソード資産（存在確認）
| 区分 | ファイル |
|---|---|
| 台本 | `03_script/script.en.v001.md`, `script.annotated.v001.json`(approved,sha一致), `script_qc.v001.json`(PASS FK7.3 ~10.3min) |
| シーン | `04_scenes/shotlist.v001.json`, `asset_map.v001.md`, `ai_prompts.v001.md`, `thumb_prompts.v001.md` |
| ストック | `05_stock/{usable_assets,stock_ledger,review_queue}.v001.json` |
| 音声 | `06_audio/{voice_plan,narration_index,audio_cue_sheet}...`（+short09系混在） |
| 編集 | `08_edit/{captions.v001.json/srt, narration_timeline.v001.json, renders/}` |
| パッケージ | `09_package/{youtube_meta,rights_manifest,title_thumbnail_candidates,youtube_schedule_result,...}` |
| メディア(H:) | `H:\pd-media\episodes\PD-2026-009-timbs\{05_stock,06_voice,07_audio,08_edit,09_package}` |

> 注: `06_audio` / `09_package` に `short09_*` 系が混在。この題材はショート版(short09)も派生している。**長尺(TimbsPremium)がP01baseline対象**。

## 5. 現行レンダー（baseline 原本・実測 ffprobe）

**`H:\pd-media\episodes\PD-2026-009-timbs\08_edit\renders\timbs_premium_review_v001.mp4`**（2026-06-24, 559 MB）

| 項目 | 値 |
|---|---|
| codec | h264 |
| 解像度 | 1920×1080 |
| fps | 30/1 |
| frames | 21975 |
| duration | **732.522667 s（≒12.2分）** |
| audio | aac, 48000 Hz, stereo, 317 kbps |

- ランタイム帯（11.5–12.5分 = 690–750s）内。ship-gate 帯適合。
- リポジトリ側 `episodes/.../08_edit/renders/` には mp4 は無く `premium_qc/`（フレームPNG・contact.jpg・review.qc.json）と `rough.v001.qc.json` のみ。**完成mp4はH:上が唯一**。

## 6. ショット構成（timbs_roughcut.ts・全28ショット / shotlist相対秒）

チャプター: `hook → opening → act1 → act2 → act3 → act4 → ending`。`seconds` 合計 ≈ 720.0s。実レンダ 732.5s との差 ≈ **+12.5s** は `CasePremiumFromRoughCut` のブランド枠（OP/ED bookend 等）付加分と推定。**baseline の正確なフレーム窓は P01 で実mp4に対し再検証**（本書のタイムコードは shotlist 相対の近似）。

| SPN | chapter | 秒 | 累積開始(相対) | assetType/motion | telop 主旨 |
|---|---|---:|---:|---|---|
| 0001 | hook | 20.0 | 0.0 | stock_video 10クリップ | ハイライト集 |
| 0002 | opening | 43.3 | 20.0 | ai_image ken_burns | Civil asset forfeiture |
| 0003 | act1 | 20.0 | 63.3 | ai_image | $73k保険→$42k SUV |
| 0004 | act1 | 23.3 | 83.3 | motion_graphic | — |
| 0005 | act1 | 25.2 | 106.6 | stock_video | No prison |
| **0006** | act1 | 28.6 | **131.8** | motion_graphic | **Max fine $10,000 vs car ~$42,000** |
| 0007 | act1 | 26.6 | 160.4 | ai_image | "grossly disproportionate" |
| 0008 | act1 | 20.5 | 187.0 | ai_image | — |
| 0009 | act2 | 14.8 | 207.5 | stock_video | 訴訟は財産に対して |
| 0010 | act2 | 41.4 | 222.3 | motion_graphic | US v. One 2012 Land Rover (in rem) |
| 0011 | act2 | 15.2 | 263.7 | ai_image | — |
| 0012 | act2 | 26.6 | 278.9 | ai_image | 擁護:犯罪利益を断つ |
| 0013 | act2 | 34.3 | 305.5 | stock_video | 批判(IJ):policing for profit |
| 0014 | act2 | 27.1 | 339.8 | ai_image | 批判は超党派 |
| 0015 | act3 | 17.1 | 366.9 | ai_image | 8th Amendment |
| 0016 | act3 | 28.1 | 384.0 | motion_graphic | Magna Carta 1215 |
| 0017 | act3 | 41.4 | 412.1 | stock_video | 州を拘束?Indianaはno |
| **0018** | act3 | 31.9 | **453.5** | motion_graphic | **2019 — 9–0 / 586 U.S. 146** |
| 0019 | act3 | 24.3 | 485.4 | ai_image | — |
| 0020 | act3 | 32.8 | 509.7 | ai_image | 限界であって終わりでない |
| 0021 | act4 | 25.7 | 542.5 | stock_video | — |
| 0022 | act4 | 22.8 | 568.2 | ai_image | 差戻で車を維持 |
| 0023 | act4 | 35.2 | 591.0 | ai_image | — |
| 0024 | act4 | 18.6 | 626.2 | stock_video | 使える人がいてこその限界 |
| 0025 | ending | 32.8 | 644.8 | ai_image | See → Take |
| 0026 | ending | 8.1 | 677.6 | ai_image | — |
| 0027 | ending | 32.4 | 685.7 | stock_video | 次回:家も奪える? |
| 0028 | ending | 1.9 | 718.1 | ai_image | Subscribe |

> 紙芝居リスクの一次観察: 28ショット中 **ai_image ken_burns が 15**（静止画のKen Burns主体）。VIDEO_RULES §1/§12 の「意味あるモーショングラフィック」が効くのは motion_graphic の SPN-0004/0006/0010/0016/0018 に限られ、静止画区間の"動きの大きさ"は P01 で optical-flow 実測が要る。

## 7. baseline 候補（連続60〜90秒・詳細は P01_CHANGE_PLAN.md §baseline）

- **候補A（推奨）** 不均衡の核心（act1）: SPN-0005–0007 ≈ 相対 106.6–191.0s（**≈84s**）。$10,000 罰金 vs ~$42,000 車の対比＝本編のシグネチャ。core-5 の `PenaltyVsProperty`+`QuoteUnderExamination`+`EvidenceReveal` が最も密に当たる。
- **候補B** 判決/編入（act3）: SPN-0017–0018 ≈ 相対 412.1–485.4s（**≈73s**）。「州を拘束?」→「2019 9–0, 586 U.S. 146」。`VerdictReversal`+`CaseJourney`。
- **候補C** in rem 概念（act2）: SPN-0009–0011 ≈ 相対 207.5–278.9s（**≈71s**）。「訴訟は財産に対して」/「in rem」。`CaseJourney`/`EvidenceReveal`。

## 8. リポジトリ側リスク / 制約

1. `git status` に **未追跡928**。将来 commit する際、kit導入分と各話生成物が混ざるため、**選択的 add** が必須（本Phaseでは何もコミットしない）。
2. `timbs_roughcut.ts` は **自動生成**。P01 以降でショット構成を変える場合は `shotlist.v001.json` 側を直し importer を再実行する（直接編集はルール違反）。
3. kit validator/tests は scene-plan/qc-report スキーマ **同名衝突（3件・INSTALLATION_REPORT §9 未解決）** により exit1。P00/P01 の成果物には無関係だが、schemas を触る後続Phase（P03+）前に owner 解決が必要。
4. 完成mp4はH:上のみ。baseline 抽出（P01）は **H:を読み取り、出力は repo `outputs/pd-visual-system/`** へ（H:へは書かない）。
