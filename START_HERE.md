# START HERE — Prime Documentary Edition 2

## 結論

このパッケージは、Claude Codeへ「PDの動画を作って」と依頼するための巨大プロンプトではない。

目的は、Prime Documentaryを次の構造へ変えること。

> 人間が制作工程を操作するのではなく、人間が事業方針、承認、例外だけを判断し、通常ケースは構造化されたジョブとして自動で流れる制作システム。

## 最初に行うこと

1. このパッケージをPD開発リポジトリのルートへ配置する。
2. 既存コードがある場合は上書きせず、Gitブランチまたはコピーを作る。
3. `CLAUDE.md`をルートに置く。
4. `.claude/`をルートに置く。
5. Claude Codeをリポジトリルートで起動する。
6. `BOOTSTRAP_PROMPT.txt`をそのまま渡す。
7. 最初の回答では実装させず、現状監査と差分分析だけをさせる。
8. 最初の実装は一本の縦断MVPに限定する。

## 読み方

### 経営・制作方針を理解する

- `decisions/0001-PD_STRATEGY_AND_SCOPE.md`
- `PD_AUTONOMOUS_STUDIO_MASTER_SPEC_V2.md`
- `docs/00_PROJECT_CONTEXT.md`
- `docs/21_PRODUCTION_ECONOMICS_AND_CAPACITY.md`

### システムを作る

- `docs/01_AUTONOMY_AND_ARCHITECTURE.md`
- `docs/10_DATA_MODEL_AND_STATE_MACHINE.md`
- `contracts/`
- `schemas/`
- `architecture/adrs/`
- `backlog/`

### 動画品質を作る

- `docs/03_TOPIC_AND_PORTFOLIO_SYSTEM.md`
- `docs/04_RESEARCH_FACT_CHECK_AND_CITATION.md`
- `docs/05_SCRIPT_STORY_AND_ENGLISH_STYLE.md`
- `docs/06_VISUAL_SYSTEM_SDXL_AND_CONTINUITY.md`
- `docs/07_AUDIO_NARRATION_MUSIC_AND_MIX.md`
- `docs/08_EDITING_DAVINCI_AUTOMATION.md`
- `docs/26_RETENTION_ENGINEERING.md`
- `docs/27_THUMBNAIL_AND_TITLE_EXPERIMENT_SYSTEM.md`

### 安全に運用する

- `docs/12_QUALITY_GATES_AND_ACCEPTANCE.md`
- `docs/13_RIGHTS_SAFETY_AND_PUBLISH_RISK.md`
- `docs/16_OPERATIONS_RUNBOOK.md`
- `docs/29_SECURITY_THREAT_MODEL.md`
- `runbooks/`

## 最初に作らせるべき機能

外部API連携ではなく、次を先に成立させる。

```text
Topic JSON
  ↓
Research Plan JSON
  ↓
Source Registry JSON
  ↓
Claim Ledger JSON
  ↓
Thesis JSON
  ↓
Annotated Script JSON
  ↓
Scene Plan JSON
  ↓
Asset Plan JSON
  ↓
Draft Voice Plan JSON
  ↓
Edit Plan JSON
  ↓
QC Report JSON
```

これが中断・再開・部分再実行・revision管理できてから、SDXL、ElevenLabs、DaVinci、YouTubeを接続する。

## 完成ではないもの

以下だけでは制作工場は完成していない。

- 一括プロンプトで台本が出る
- SDXL画像が自動生成される
- TTSが作れる
- DaVinciへ画像を並べられる
- YouTubeへアップロードできる

完成条件は、依存関係と品質を保ったまま複数episodeを安全に流し、問題箇所だけ再実行し、公開結果から次回判断が改善すること。
