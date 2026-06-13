# 01 — Autonomy and Architecture

## 1. 結論

PDは、単一の万能エージェントではなく、**オーケストレーター＋専門ワーカー＋品質ゲート＋承認サービス**で構築する。

万能エージェントに全工程を任せると、文脈肥大、責任境界の曖昧化、再試行単位の粗大化、評価困難、コスト予測不能が起きる。

## 2. 自律レベル

| Level | 状態 | 人間の役割 | PDでの位置づけ |
|---|---|---|---|
| L0 | 全手動 | 全工程を操作 | 目標外 |
| L1 | AI補助 | 人間が工程を進め、AIが生成 | 移行元 |
| L2 | 工程自動 | 工程ごとに人間が開始・確認 | MVP |
| L3 | ほぼ自動 | バッチ承認、最終責任、例外 | 標準目標 |
| L4 | 無人運転 | 方針と監査のみ | 成熟後の目標 |
| L5 | 自律事業運営 | 資本配分まで自動 | 現時点では対象外 |

### 2.1 L3の標準像

自動：

- 需要収集
- テーマ候補生成
- スコアリング
- 予備調査
- 深掘り調査
- 主張台帳
- 構成
- 台本
- シーン設計
- 画像プロンプト
- 画像生成
- 自動QCと限定再生成
- 音声生成
- 音楽選定
- 仮編集
- 技術QC
- タイトル・サムネ案
- 公開パッケージ
- 分析収集
- 改善仮説

人間：

- 週次テーマポートフォリオ承認
- 中心命題または高リスク切り口の承認
- 最終英語台本承認
- 編集初稿承認
- タイトル・サムネイル承認
- 公開承認
- 予算超過
- 権利・重大事実の例外判断

### 2.2 L4昇格条件

- 同じ形式で20〜30本以上を完走
- 重大な事実事故ゼロ
- 権利事故ゼロ
- 自動QCと人間QCの一致率が安定
- 人間差戻し率が工程別閾値以下
- ジョブ再開成功率95%以上
- コスト予測誤差20%以内
- 自動公開のロールバックを実証
- 低リスクコンテンツ型に限定

## 3. システムコンポーネント

### 3.1 Control Plane

- チャンネル戦略
- 許可・禁止テーマ
- 品質閾値
- 予算
- provider設定
- voice profile
- brand profile
- 公開権限
- 自律レベル
- 承認ポリシー
- 実験設定
- 緊急停止

### 3.2 Orchestrator

責務：

- episode状態を読む
- 次に実行可能なstageを判定
- 依存ジョブを作る
- workerへ投入
- 結果を検証
- 状態を遷移
- retry/dead-letter
- 予算を確認
- 承認を要求
- 通知
- イベントを記録

Orchestratorはクリエイティブ判断そのものをしない。判断は専門agentやQCへ委譲し、状態とポリシーを管理する。

### 3.3 Workers

- topic worker
- research worker
- fact-check worker
- script worker
- scene planner
- image generation worker
- visual QC worker
- narration worker
- audio QC worker
- music selector
- edit plan worker
- DaVinci adapter worker
- render QC worker
- packaging worker
- publish worker
- analytics worker

### 3.4 Artifact Store

- 調査資料メタデータ
- 台本
- 画像
- 音声
- 音楽
- タイムライン
- レンダー
- サムネイル
- 公開パッケージ
- 分析スナップショット

### 3.5 Metadata DB

- episode
- topic
- claim
- source
- scene
- asset
- job
- approval
- cost
- event
- analytics

### 3.6 QC Engine

- deterministic validation
- model-based review
- cross-artifact consistency
- quality score
- blocker detection
- repair recommendation

## 4. Worker原則

各workerは以下を満たす。

- 一つの明確な責務
- 機械可読入力
- 機械可読出力
- side effectの明示
- timeout
- retry class
- cost estimate
- deterministic validation
- provider metadata
- input/output hash
- structured error

## 5. Approval Service

承認をチャットの口頭返答だけにしない。

Approval record：

- approval_id
- target_type
- target_id
- target_revision
- requested_at
- requested_by
- decision
- decided_at
- decided_by
- notes
- conditions
- expires_at
- evidence snapshot

承認後に対象revisionが変わった場合、承認は自動失効する。

## 6. 工程別Autonomy Policy

各工程は以下のモードを持つ。

- manual
- suggest
- auto_with_review
- auto_unless_flagged
- fully_auto
- disabled

初期例：

| 工程 | 初期モード | 将来 |
|---|---|---|
| topic discovery | fully_auto | fully_auto |
| portfolio selection | auto_with_review | auto_unless_flagged |
| research | fully_auto | fully_auto |
| critical claim approval | auto_unless_flagged | auto_unless_flagged |
| script | auto_with_review | auto_unless_flagged |
| image generation | fully_auto | fully_auto |
| expensive regeneration | auto_unless_flagged | fully_auto within budget |
| rough edit | fully_auto | fully_auto |
| final edit | auto_with_review | auto_unless_flagged |
| private upload | auto_with_review | fully_auto |
| public publish | manual | auto_unless_flagged |
| analytics | fully_auto | fully_auto |

## 7. Event-driven Design

イベント例：

- TopicCandidateCreated
- TopicApproved
- ResearchPlanCreated
- SourceRegistered
- ClaimLedgerValidated
- ThesisApproved
- ScriptVerified
- ScenePlanValidated
- AssetGenerated
- AssetRejected
- NarrationReady
- TimelineBuilt
- HumanReviewRequested
- PublishApproved
- VideoScheduled
- VideoPublished
- AnalyticsWindowReached

イベントにはschema versionとcorrelation IDを持たせる。

## 8. Cross-machine Architecture

Windows生成機とMac編集機を分ける場合：

- メタデータDBは単一のsource of truth
- 大容量ファイルはNASまたはobject storage
- workerはOS固有パスではなくlogical URIを受け取る
- local cacheを使う
- checksumで同期確認
- 編集機がオフラインでも上流は進める
- edit queueにWIP上限
- 両機の時刻同期
- file lockまたはlease

Logical URI例：

`artifact://PD-2026-001/S013/IMG/approved/v002`

Windows local：

`D:\PD_CACHE\PD-2026-001\...`

Mac local：

`/Volumes/PD_CACHE/PD-2026-001/...`

DBへOS固有パスを真実として保存しない。

## 9. 可用性と障害前提

長時間ジョブが多いため、以下を通常障害として扱う。

- process crash
- machine reboot
- provider outage
- GPU OOM
- corrupt asset
- storage full
- network断
- DaVinci未起動
- credential expiry
- timeout後に外部処理だけ完了
- MacとWindowsの同期遅延

## 10. 最小推奨技術構成

過剰な分散システムを避ける。

- Python
- SQLiteまたはPostgreSQL
- local filesystem + NAS/object storage
- 軽量job queue
- Pydantic / JSON Schema
- CLI
- structured logging
- pytest
- ffmpeg / ffprobe
- provider adapters
- DaVinci scripting adapter
- optional web dashboard

一本も流れていない段階でKubernetesを導入しない。
