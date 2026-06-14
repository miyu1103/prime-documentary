# Prime Documentary
# Claude Code 実装指示書 100点版
## Animaticレビュー基盤・量産パイプライン・品質自動化 統合仕様

- 最終更新日: 2026-06-13 JST
- 対象プロジェクト: Prime Documentary
- 対象リポジトリ: 現在の `main` ブランチ上の既存プロジェクト
- 主担当AI: Claude Code
- 実装方針: 既存コードベース・既存設計・既存テストを最優先する
- 会話・報告言語: 日本語
- コード・スキーマ・ファイル名・コメント: 原則英語
- 動画本編・字幕・公開物: US English
- この文書の最優先目的: **オーナーが第1話のAnimaticを安全にレビューできる最小環境を作ること**

---

# 0. Claude Codeへの最重要指示

この文書は、Prime Documentary制作システムに対する**実装契約書**である。  
Claude Codeは、この文書を読んだ直後に大規模実装へ入ってはならない。

まず必ず、既存リポジトリの調査を行い、以下を日本語で報告すること。

```text
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
```

その後、以下の条件に該当しない限り、**確認質問で止まらずP0の最小実装へ進む**。

Claude Codeが必ず停止してオーナー確認を取るべきもの:

- 有料APIまたは有料サービスの実行
- 外部公開、外部アップロード、YouTube操作
- 既存承認済み台本、claim、source、法的事実の変更
- ブランド・チャンネル方針の大幅変更
- 破壊的操作、データ削除、履歴破壊、force push
- secrets / API keys / `.env` の表示・保存・送信
- 不可逆なmigration
- セキュリティ上の妥協
- 実在人物に関する事実・描写方針の変更

軽微なUI、命名、配置、依存の選択は、既存プロジェクトの慣習に従って合理的に判断してよい。  
ただし判断理由は完了報告に残すこと。

---

# 1. 判断優先順位

仕様が衝突した場合は、次の順で優先する。

1. 既存データ・既存機能を壊さない
2. secrets、外部公開、有料処理を発生させない
3. オーナーが第1話Animaticを実際に見られる状態を最短で作る
4. JSON正本で安全にレビュー情報を保存する
5. Claude Codeが後続修正計画に使える構造にする
6. UIの見た目を整える
7. 将来構想を先取りする

特に重要な原則:

- **今作るのは制作ダッシュボードではない。Animaticレビュー画面である。**
- **今のゴールは、レビュー前の開発を増やすことではなく、レビューを始めること。**
- **将来便利な機能でも、P0に不要なら実装しない。**

---

# 2. 現在のプロジェクト状態

## 2.1 チャンネル情報

- Channel: Prime Documentary
- Handle: `@PrimeDocumentary0`
- Status: exists, unmonetized
- Target market: United States / English-speaking audience
- Genre:
  - US landmark court cases
  - hidden systems
  - legal decisions that changed everyday life
- Tone:
  - neutral
  - authoritative
  - plain US English
  - cinematic but not sensational
- Visual identity:
  - black
  - navy
  - electric blue
  - silver
  - gold
  - PD logo
  - sunrise motif

## 2.2 チャンネル目的

Prime Documentaryは、単発制作ではなく、以下を満たすAI動画制作工場を目指す。

- YouTube monetizationを目指す
- AI-heavy production
- low human labor
- high factual reliability
- repeatable batch production
- ownerは重要判断だけを行う
- 第2話以降のowner作業は、おおむね30分以内を目標にする

## 2.3 第1話の状態

- Episode: Miranda v. Arizona
- Working title concept: `Why Do Police Read You Your Rights?`
- Current priority: **owner watches full animatic**
- Paid cost so far: USD 0.00
- Current state: `scene_planned`

完了済み:

- topic approved
- research plan approved
- sources approved
- claims approved
- script approved
- scene plan completed
- voice plan completed
- pre-render QC passed with warnings
- full approximately 745-second animatic completed

未完了または未生成:

```text
05_visuals/
06_audio/ narration master
07_music/
08_edit/ final render
09_publish/
10_analytics/
```

## 2.4 既存成果物の想定パス

既存の命名規則や実パスが異なる場合は、リポジトリ内の実物を正とする。

```text
00_topic/topic.v001.json

01_research/
  research_plan.v001.json
  sources.v001.json
  claims.v001.json

03_script/
  script.en.v001.md
  script.annotated.v001.json
  script.review.ja.md

04_scenes/
  scene_plan.v001.json
  midjourney_prompts.v001.md

06_audio/
  voice_plan.v001.json

08_qc/
  qc_report.v001.json
  qc_report.review.ja.md

approvals/
  APR-0001.json
```

## 2.5 既存Remotion要素

想定される既存コンポーネント:

- Brand
- KineticType
- Parallax
- OpenCaption
- Transition
- CitationLowerThird
- DiagramFlow
- Grain
- ThumbnailFrame

想定される既存composition:

- Opening
- StyleTest
- Episode
- Animatic

既存検証:

- `tsc --noEmit` clean
- thumbnail still rendered
- `node_modules` excluded

Claude Codeは、上記を鵜呑みにせず、必ず実リポジトリで確認すること。

## 2.6 既存Python core

想定領域:

```text
src/pd_factory/research/
src/pd_factory/library/
schemas/
tests/
```

想定要素:

- research fetcher
- preflight
- providers
- sanitize
- build
- untrusted-input defense
- egress allowlist
- budget gate
- music selection
- visual selection
- music-track schema
- visual-motif schema

既存テストの参考値:

- 57 passed
- `validate_all_v2` passed

Claude Codeは、実際のテストコマンドと件数を確認し、報告時は実測値を書くこと。

## 2.7 外部ツールと制約

未接続または未使用想定:

- CourtListener token
- ElevenLabs API
- Runway API
- YouTube OAuth
- Midjourney manual web
- Suno manual web

絶対条件:

- API keyが存在しても自動課金してはならない
- 第1話は有料処理ごとにowner確認が必要
- 第2話以降の自動化は将来課題であり、P0では実装しない
- P0では外部API実行、外部アップロード、課金処理を行わない

---

# 3. 今すぐ実装するもの

## 3.1 結論

今すぐ実装するものは、**最小Animaticレビュー画面のみ**。

実装対象:

- Animatic再生
- 現在タイムコード表示
- 1回目視聴用の簡易マーカー
- 2回目視聴用の日本語コメント
- JSON正本への安全保存
- draft autosave
- 中断・再開
- keyboard shortcuts
- 1コマンド起動
- ブラウザ自動表示
- 最小テスト
- smoke test

実装しないもの:

- SQLite
- 本格ダッシュボード
- YouTube OAuth
- YouTube upload / publish / scheduled publish
- Midjourney自動操作
- Suno自動化
- ElevenLabs生成実行
- Runway生成実行
- 本格2.5D
- SAM / Depth Anything導入
- SFX収集
- OneDrive自動バックアップ
- Robocopy定期実行
- analytics ingestion
- サムネA/B運用システム
- 複雑なタイムライン編集UI
- デスクトップアプリ化
- 外部アクセス
- スマホ対応
- 英語ネイティブテスト連携
- 公開後学習の自動反映

## 3.2 P0の目的

ownerが以下を簡単にできる状態にする。

1. Claude Codeへ一文で起動指示する
2. 開発サーバーが起動する
3. ブラウザが自動で開く
4. Animatic画面が表示される
5. 1回目は通し視聴しながら簡易マーカーだけ残す
6. 2回目はタイムコード付きで日本語コメントを残す
7. コメントと状態がJSONへ保存される
8. ブラウザを閉じても復元できる
9. Claude Codeが後からJSONを読み、修正計画を作れる

---

# 4. 実装前の必須調査

## 4.1 読むべきファイル

最低限:

```text
AGENTS.md
package.json
remotion.config.*
remotion/src/**
src/pd_factory/**
schemas/**
tests/**
decisions/**
approvals/**
```

存在しないものがある場合は、存在しないことを報告すればよい。

加えて以下を検索する。

```text
Animatic
Composition
localhost:3000
registerRoot
Player
calculateMetadata
edit_plan
scene_plan
approval
review
qc_report
validate_all_v2
```

## 4.2 調査時の安全確認

コード変更前に必ず確認する。

```text
git status --short
```

未コミット変更がある場合:

- 変更内容を把握する
- ownerまたは既存作業の変更を上書きしない
- 必要なら自分の変更ファイルを限定する
- 完了報告で未コミット変更との関係を明記する

禁止:

- `git reset --hard` を勝手に実行する
- `git clean -fd` を勝手に実行する
- force push
- `rm -rf` による広範削除
- secretを含むファイルの表示・保存・送信

## 4.3 技術選定の原則

- 既存Remotion Previewを壊さない
- 既存compositionロジックを複製しない
- UIのために大規模フレームワークを追加しない
- 既存がReact/TypeScriptならそれを使う
- 永続化のために最初からDBを導入しない
- JSONを正本とする
- ローカルPCのみで動作する
- 外部ネットワークへ公開しない
- 認証機能はP0では不要
- 依存関係追加は最小限
- ブラウザから任意ファイルを書き込める実装は禁止
- 必要ならローカル専用の軽量APIを追加する

## 4.4 実装方針の選び方

優先順位:

1. 既存dev server / routing / build構成に自然に追加できる方法
2. 既存Remotion/React環境内で完結する方法
3. 既存package scriptに最小追加する方法
4. 軽量Node serverを併設する方法
5. 新規フレームワーク導入

5は原則避ける。既存構成上どうしても必要な場合のみ、理由を報告する。

---

# 5. 最小レビュー画面の仕様

## 5.1 画面構成

単一画面でよい。

推奨レイアウト:

```text
+--------------------------------------------------------------+
| Prime Documentary / Episode / Review State / Save Status     |
+--------------------------------------------------------------+
|                                                              |
|                     Animatic Player                           |
|                                                              |
+--------------------------------------------------------------+
| Current Time | Duration | Playback Rate | Review Mode         |
+--------------------------------------------------------------+
| Quick Markers | Comment Form | Severity | Category | Save      |
+--------------------------------------------------------------+
| Session Summary | Last Saved | Resume Info | Shortcuts        |
+--------------------------------------------------------------+
```

UIの優先順位:

1. Animaticが見える
2. 現在位置が分かる
3. マーカー・コメントが迷わず残せる
4. 保存状態が分かる
5. 再開できる
6. 見た目が整っている

豪華なUIより、レビューを止めない操作性を優先する。

## 5.2 Animatic再生

必須:

- 既存 `Animatic` compositionを再利用
- 再生
- 一時停止
- シーク
- 現在タイムコード表示
- 総尺表示
- 2倍速再生
- 1倍速へ戻す
- 既存compositionロジックの複製禁止

可能なら対応:

- 0.5倍速
- 5秒戻る / 5秒進む
- marker一覧から該当位置へジャンプ
- comment一覧から該当位置へジャンプ

## 5.3 タイムコード取得

markerまたはcomment作成時に、以下を記録する。

- frame
- seconds
- formatted timecode
- fps

fpsは既存composition/metadataから取得する。  
取得できない場合のみ、既存設定を確認したうえでfallback値を使う。

例:

```json
{
  "frame": 2385,
  "seconds": 79.5,
  "timecode": "00:01:19.500",
  "fps": 30
}
```

`duration_seconds` や `duration_frames` も、可能な限りmetadataから取得する。  
約745秒という情報をハードコードしない。

## 5.4 レビュー状態

最低限の状態:

```text
not_started
first_pass
second_pass
completed
```

日本語表示:

```text
未開始
1回目の通し視聴中
2回目のコメント入力中
レビュー完了
```

基本遷移:

```text
not_started -> first_pass -> second_pass -> completed
```

後戻りは許可してよい。ただし `state_history` に履歴を残す。

## 5.5 1回目視聴モード

状態:

```text
first_pass
```

目的:

- 全体テンポを見る
- 冒頭の引力を見る
- 12分見続けられるか判断する
- 違和感の位置だけ素早く残す

原則:

- コメント入力を前面に出さない
- 視聴リズムを優先する
- ワンクリックまたはショートカットでmarkerを記録する

marker種別:

| marker_type | 日本語 | 意味 |
|---|---|---|
| `boring` | 退屈 | テンポ低下、同じ絵が長い、集中が切れる |
| `unclear` | 分かりにくい | 意味・因果・視覚説明が伝わりにくい |
| `awkward` | 違和感 | 絵、音、字幕、演出に不自然さがある |
| `blocker` | 公開不可 | 事実・法務・品質上、そのまま公開できない |

1回目では通常、timecodeとmarker種別だけ保存する。  
`blocker`のみ任意で緊急コメントを入力できる。

## 5.6 2回目コメントモード

状態:

```text
second_pass
```

目的:

- 具体的な修正指示をタイムコード付きで残す
- Claude Codeが後で修正計画に変換できる構造にする

comment必須項目:

- category
- severity
- original_comment_ja
- timecode
- frame
- seconds
- fps
- status
- timestamps

可能なら記録:

- marker_id
- scene_id
- nearby narration/caption reference

category:

| category | 日本語 | 主な用途 |
|---|---|---|
| `pacing` | テンポ | 長い、短い、間が悪い、展開が遅い |
| `visual` | 画像 | 画像、構図、動き、使い回し、視覚理解 |
| `caption` | 字幕 | 改行、位置、読みやすさ、表示量 |
| `audio` | 音声 | ナレーション、BGM、SFX、音量 |
| `direction` | 演出 | 緊張感、見せ方、場面転換、印象 |
| `fact_check` | 事実確認 | 法的事実、引用、誤認リスク |
| `other` | その他 | 上記以外 |

severity:

| severity | 日本語 | 意味 |
|---|---|---|
| `minor` | 軽微 | 直せるなら直す。公開可否には直結しない |
| `needs_fix` | 要修正 | 公開前に直したい |
| `blocker` | 公開不可 | 解消まで公開不可 |

## 5.7 日本語原文の扱い

- commentは日本語で入力する
- `original_comment_ja` を正本として保存する
- 日本語原文は上書きしない
- 初期実装では英訳APIを呼ばない
- 外部APIが必要な翻訳はP0で実装しない
- 将来の翻訳用フィールドだけ用意してよい

例:

```json
{
  "original_comment_ja": "この場面は同じ画像が長く続いて少し退屈",
  "instruction_en": null,
  "translation_status": "pending"
}
```

## 5.8 自動保存

必須:

- 入力中のdraftを数秒ごとに保存
- コメント確定時に正式保存
- ブラウザを閉じても復元可能
- 保存成功・保存失敗を画面上に表示
- 書き込み失敗時は警告を出す

推奨:

- draft autosave debounce: 1〜3秒
- formal save: explicit action
- JSONファイルを正本とする
- localStorageは補助に限定する
- localStorageだけを正本にしない

## 5.9 中断・再開

保存対象:

- review state
- current playback position
- playback rate
- current draft
- unsaved draft status
- markers
- comments
- session started time
- last saved time

再開時に表示する情報:

```text
前回のレビュー状態:
- 1回目視聴中
- 08:42 で中断
- 未確定下書きあり

[続きから再開]
[最後の確定コメントから再開]
[最初から開始]
```

## 5.10 キーボード操作

必須候補:

| Key | Action |
|---|---|
| `Space` | 再生 / 一時停止 |
| `ArrowLeft` | 5秒戻る |
| `ArrowRight` | 5秒進む |
| `M` | 現在位置へmarkerまたはcomment開始 |
| `1` | severity: minor |
| `2` | severity: needs_fix |
| `3` | severity: blocker |
| `Ctrl + Enter` | comment確定保存 |
| `Esc` | comment UIを閉じ、playerへfocusを戻す |

1回目視聴用marker shortcutの推奨:

| Key | marker_type |
|---|---|
| `B` | boring |
| `U` | unclear |
| `A` | awkward |
| `X` | blocker |

既存ブラウザ操作またはRemotion操作と衝突する場合は変更してよい。  
ただし画面内にショートカット一覧を表示すること。

## 5.11 音声入力

P0では専用音声認識を実装しない。

- Windows標準 `Win + H` が使える通常のtextarea/inputにする
- ローカルWhisperは将来候補
- 音声入力機能を理由にP0実装を遅延させない

---

# 6. 保存ファイル仕様

## 6.1 保存場所

既存artifact構成に合わせる。

推奨:

```text
08_qc/reviews/
  animatic_review.v001.json
  animatic_review.draft.v001.json
  backups/
```

既存のepisode別ディレクトリ構成がある場合は、それを優先する。  
ただし、保存先は必ずリポジトリ内のallowlistされた場所に限定する。

## 6.2 JSON正本

P0ではJSONのみを正本とする。  
SQLiteは導入しない。

既存ファイルがある場合:

- 上書き前にbackupを作る
- 既存comments / markersを消さない
- schema_versionが古い場合は安全にmigrateする
- migrateが危険なら停止して報告する

## 6.3 Review JSON schema 推奨形

既存schema規約がある場合は、そちらに合わせてよい。  
ただし以下の情報は保持すること。

```json
{
  "schema_version": "1.0.0",
  "review_id": "REV-EP001-ANIMATIC-001",
  "episode_id": "EP001",
  "episode_slug": "miranda-v-arizona",
  "composition_id": "Animatic",
  "source_revision": {
    "script": "v001",
    "scene_plan": "v001",
    "animatic": "v001"
  },
  "review_state": "not_started",
  "language": {
    "input": "ja-JP",
    "execution": "en-US"
  },
  "player_state": {
    "fps": 30,
    "duration_frames": null,
    "duration_seconds": null,
    "current_frame": 0,
    "current_seconds": 0,
    "playback_rate": 1.0
  },
  "session": {
    "started_at": null,
    "updated_at": null,
    "completed_at": null,
    "last_saved_at": null
  },
  "draft": {
    "active": false,
    "category": null,
    "severity": null,
    "original_comment_ja": "",
    "timecode": null,
    "frame": null,
    "seconds": null,
    "updated_at": null
  },
  "markers": [],
  "comments": [],
  "state_history": [],
  "save_status": {
    "last_result": null,
    "last_error": null
  }
}
```

## 6.4 Marker schema

```json
{
  "marker_id": "MRK-0001",
  "marker_type": "boring",
  "severity": "minor",
  "frame": 1200,
  "seconds": 40.0,
  "timecode": "00:00:40.000",
  "fps": 30,
  "scene_id": "SCN-004",
  "note_ja": null,
  "created_at": "2026-06-13T00:00:00+09:00"
}
```

## 6.5 Comment schema

```json
{
  "comment_id": "CMT-0001",
  "marker_id": "MRK-0001",
  "category": "pacing",
  "severity": "needs_fix",
  "frame": 1215,
  "seconds": 40.5,
  "timecode": "00:00:40.500",
  "fps": 30,
  "scene_id": "SCN-004",
  "original_comment_ja": "この場面は少し長い。3秒程度短縮したい。",
  "instruction_en": null,
  "translation_status": "pending",
  "status": "open",
  "created_at": "2026-06-13T00:00:00+09:00",
  "updated_at": "2026-06-13T00:00:00+09:00"
}
```

## 6.6 State history schema

```json
{
  "from": "first_pass",
  "to": "second_pass",
  "changed_at": "2026-06-13T00:00:00+09:00",
  "reason": "owner_completed_first_pass"
}
```

## 6.7 Scene ID解決

可能であれば、現在frameから `scene_plan.v001.json` の対応sceneを解決する。

ただしP0の優先順位は以下。

1. レビュー画面を動かす
2. タイムコードを保存する
3. JSONを壊さず保存する
4. scene_idを自動解決する

scene_id解決が安全にできない場合:

```json
"scene_id": null
```

としてよい。  
scene_idの未解決を理由にP0を止めない。

---

# 7. ローカル保存API

## 7.1 原則

ブラウザUIからJSONへ保存するために、既存構成に合うローカル専用手段を選ぶ。

候補:

- 既存dev serverのAPI route
- 既存Vite middleware
- 軽量Node server
- Remotion Studioと併用できるlocal API

最小実装なら、以下だけでもよい。

```text
GET /api/review
PUT /api/review
```

将来の拡張候補:

```text
POST /api/review/marker
POST /api/review/comment
POST /api/review/state
```

## 7.2 セキュリティ要件

必須:

- `127.0.0.1` または `localhost` のみでlisten
- `0.0.0.0` へ公開しない
- クライアントから任意file pathを指定させない
- 保存対象episodeをallowlistで解決する
- `..` を拒否する
- 絶対パス入力を拒否する
- secretを返さない
- `.env` を読み出すAPIを作らない
- command execution APIを作らない
- shell文字列を受け取らない
- JSON最大サイズを設定する
- 破損時に既存正本を上書きしない

## 7.3 Atomic write

推奨手順:

1. request payload size check
2. JSON parse
3. schema validation
4. temp fileへwrite
5. 可能ならfsync相当
6. 既存ファイルのbackup作成
7. renameで置換
8. success response

失敗時:

- 既存正本を保持する
- temp fileを安全に処理する
- UIへclear errorを返す
- logにsecretを出さない

## 7.4 破損JSONへの対応

既存review JSONが壊れている場合:

1. 壊れたファイルをbackupへ退避
2. 可能ならread-onlyで内容を表示
3. 新規初期ファイルを作るかどうかを判断
4. データ損失があり得る場合はowner確認

P0では、自動修復を頑張りすぎない。  
既存データ保護を優先する。

---

# 8. 起動体験

## 8.1 owner操作

ownerがClaude Codeへ一文で指示できる状態にする。

想定指示:

```text
Prime DocumentaryのMiranda Animaticレビュー画面を起動して、エラー確認後にブラウザで自動表示して。
```

## 8.2 Claude Codeの実行内容

1. 正しいディレクトリへ移動
2. `git status --short` を確認
3. 必要依存を確認
4. サーバー起動
5. 起動ログ確認
6. review JSONの読込確認
7. Animatic compositionの読込確認
8. ブラウザ自動起動
9. 正しいURLを表示
10. エラーがあれば自動修正または原因提示

## 8.3 起動スクリプト

可能なら追加する。

Windows向け:

```text
scripts/start-review.ps1
```

またはpackage script:

```json
{
  "scripts": {
    "review:animatic": "..."
  }
}
```

目標:

```powershell
npm run review:animatic
```

だけで起動できること。

## 8.4 ブラウザ自動起動

Windows環境で安全に実行する。

例:

```powershell
Start-Process "http://localhost:3000/review/animatic"
```

ポートやURLは既存環境に合わせる。  
ブラウザ自動起動に失敗しても、サーバーとURLが正常ならP0を失敗扱いにしない。  
その場合は手動で開けるURLを明示する。

---

# 9. レビュー運用

## 9.1 1回目視聴

目的:

- 全体のテンポ
- 物語の理解
- 冒頭の引力
- 単調さ
- 約束と回収
- 12分を見続けられるか

ルール:

- 基本的に止めない
- 長文コメントを書かない
- markerだけ使う
- blockerだけ緊急コメント可

確認ポイント:

1. 最初の5秒で何の動画か分かるか
2. 30秒以内に続きを見たくなるか
3. ナレーションだけでも理解できるか
4. 同じ画像・同じ動きが長く続かないか
5. 重要な転換点が視覚的に分かるか
6. 法律説明が難しすぎないか
7. Miranda判決の意味が後半で回収されるか
8. 終了時に「今の警察手続きとつながった」と理解できるか

## 9.2 2回目視聴

目的:

- 具体的修正をタイムコード付きで残す

操作:

1. marker位置へ移動
2. 前後を再生
3. category選択
4. severity選択
5. 日本語コメント入力
6. 確定保存

## 9.3 レビュー完了

レビュー完了時:

- `review_state` を `completed` にする
- `completed_at` を保存
- 未確定draftがある場合は警告
- blocker未解決数を表示
- comment件数を表示
- category別件数を表示
- severity別件数を表示
- JSON pathを表示

---

# 10. P0受け入れ基準

以下を満たしたら、P0完了。

## 10.1 起動

- 1コマンドでレビュー画面が起動する
- ブラウザが自動表示される、またはURLが明示される
- Animaticが正常に表示される
- 既存Remotion compositionsが壊れていない

## 10.2 再生

- 再生 / 一時停止できる
- シークできる
- タイムコードが表示される
- 2倍速再生できる
- 1倍速に戻せる
- 音声またはAnimatic音声が存在する場合、正常に再生される

## 10.3 marker

- 1回目モードで4種markerを追加できる
- 正しいtimecode / frame / seconds / fpsが保存される
- reload後も残る
- marker一覧から確認できる

## 10.4 comment

- categoryを選べる
- severityを選べる
- 日本語入力できる
- `Ctrl + Enter` で保存できる
- 正しいtimecode / frame / seconds / fpsが保存される
- reload後も残る

## 10.5 autosave

- 入力途中のdraftが保存される
- ブラウザを閉じて再度開くと復元される
- 保存成功 / 保存失敗が画面で分かる

## 10.6 resume

- 再生位置が保存される
- review stateが保存される
- 続きから再開できる

## 10.7 JSON

- schemaに沿って保存される
- JSONが破損しない
- atomic writeされる
- 既存データを意図せず消さない
- backupが作成される

## 10.8 品質

- TypeScript compile clean
- lintがある場合pass
- 既存tests pass
- 新規tests pass
- `validate_all_v2` が存在する場合pass
- Windowsで動作する

---

# 11. 最小テスト要件

## 11.1 Unit test

最低限:

- timecode conversion
- marker validation
- comment validation
- review state transition
- autosave serialization
- path allowlist
- atomic write helper

## 11.2 Integration test

最低限:

- empty review fileから読み込み
- marker追加
- comment追加
- state更新
- reload後の復元
- invalid payload拒否
- malformed existing JSON時の安全動作

## 11.3 Manual smoke test

Claude Code自身が確認:

1. review起動
2. Animatic再生
3. 10秒位置にmarker追加
4. 20秒位置にcomment追加
5. draft作成
6. reload
7. position / marker / comment / draft復元
8. review state変更
9. JSON確認
10. server終了

テスト用に作ったmarker/commentが本番review JSONへ残る場合は、`test` と分かる内容にするか、完了前に安全に削除する。  
削除する場合も、既存ownerデータを消さないこと。

---

# 12. 実装完了時の報告形式

Claude Codeは、P0完了後に以下の形式で日本語報告すること。

```text
# 実装結果

## 1. 結論
レビュー画面が利用可能か

## 2. 起動方法
実行コマンド
表示URL

## 3. 実装した機能
一覧

## 4. 変更ファイル
新規 / 変更 / 削除

## 5. 保存先
review JSONのパス
backupのパス

## 6. 操作方法
1回目
2回目
ショートカット
中断・再開

## 7. テスト結果
TypeScript
Unit
Integration
Existing tests
validate_all_v2
Manual smoke test

## 8. 既知の制約
P0で未対応のもの
回避策

## 9. 実装判断の理由
なぜその実装場所・方式にしたか
依存を追加した場合は理由

## 10. ロールバック方法
戻すコマンドまたは戻すファイル
review JSON保護方針

## 11. Git
branch
commit hash または未commit理由
作業前から存在した未コミット変更

## 12. 次にownerが行うこと
Animaticを1回目から視聴する
```

---

# 13. Phase 1で実装してはいけないもの

Animaticレビュー完了前に、以下を本実装しない。

```text
SQLite
Full dashboard
YouTube OAuth
Automatic upload
Scheduled publish
Analytics ingestion
Midjourney browser automation
CAPTCHA handling
Suno automation
ElevenLabs paid generation
Runway paid generation
Full 2.5D
SAM / Depth Anything
SFX collection workflow
OneDrive automatic backup
Robocopy scheduled backup
Monthly restore test automation
Thumbnail A/B operation system
Complex timeline editor
Desktop app packaging
External access
Mobile-specific support
Native English tester workflow
Automatic post-publish learning loop
```

将来設計のためのinterface、schema、TODOは置いてよい。  
ただしP0の作業量・依存・リスクを増やす実装はしない。

---

# 14. レビュー後のPhase 2

ownerがAnimaticをレビューし、review JSONが完成した後に実施する。

## 14.1 コメント整理

Claude Codeはreview JSONを読み、以下を行う。

1. scene別分類
2. category別分類
3. severity別分類
4. 重複統合
5. 矛盾検出
6. 修正案作成
7. 影響範囲特定
8. 再レンダリング範囲特定
9. 実行順提案
10. リスク分類

## 14.2 修正分類

低リスク、一括承認候補:

- 字幕改行
- 字幕位置
- BGM音量
- SFX音量
- scene尺微調整
- 同じanimation連続回避
- zoom / pan強度
- 再利用画像のcrop変更
- transition微調整

高リスク、個別承認必須:

- 冒頭構成
- script変更
- claim変更
- factual wording
- narration再生成
- critical visual差し替え
- AI動画カット変更
- 全体尺変更
- chapter構成変更
- real person portrayal変更

## 14.3 修正計画の推奨形式

```json
{
  "plan_id": "FIXPLAN-EP001-001",
  "source_review_id": "REV-EP001-ANIMATIC-001",
  "summary_ja": "...",
  "low_risk_changes": [],
  "high_risk_changes": [],
  "conflicts": [],
  "render_scope": [],
  "estimated_owner_checks": [],
  "rollback_point": "..."
}
```

## 14.4 修正実行

Claude Code:

1. snapshot
2. code/data変更
3. tests
4. affected preview render
5. fail時rollback
6. 原因説明
7. 代替案提示

修正後:

- 修正箇所の前後10〜20秒を連結したreview reelを生成
- ownerがreview reel確認
- 最終承認前に全編2倍速確認

---

# 15. 将来の制作確認ダッシュボード

Phase 1完了後、必要に応じて段階実装する。  
P0では実装しない。

## 15.1 アーキテクチャ

- UIは独立ローカルWebアプリ
- Remotionのdata / preview / render機能を共有
- 編集エンジンとの二重実装を避ける
- RTX 4090 Windows PC上のみ
- 外部公開なし

## 15.2 2層UI

Timeline view:

- scene
- narration
- caption
- image
- animation
- music
- SFX
- claim
- warning
- approval

Scene card:

- preview
- selected visual
- alternatives
- animation template
- narration
- caption
- citation
- music
- SFX
- quality score
- warnings
- approve
- reject
- request fix

## 15.3 直接編集してよいもの

- image replacement
- animation template
- zoom intensity
- pan intensity
- scene duration
- caption line break
- caption position
- music volume
- SFX volume
- approve
- reject
- regenerate request

複雑な変更:

- Claude Codeへの自然文指示
- 定型指示＋自由入力
- Claudeが影響範囲を示す
- owner承認後に実行

## 15.4 Undo / Redo

- 通常は変更セット単位snapshot
- 重大変更は個別snapshot
- dashboardでUndo / Redo
- 重要承認地点のみGit commit

---

# 16. 制作方針メモ

この章は将来方針であり、P0の実装対象ではない。

## 16.1 Midjourney

基本:

- 第2話以降もMidjourney継続
- 画像品質を優先
- 生成自体はmanual web
- 半自動から開始
- 安定部分のみ段階的に自動化
- CAPTCHA回避や制限回避は禁止
- 利用規約違反を前提にしない

生成方針:

- 第1話は広めに生成
- 最初の数sceneでstyle確認
- style固定後に残りをまとめて生成
- 枚数固定なし
- 採用上限目安: 25枚
- 必要に応じて再利用
- 同一画像の連続使用は禁止
- 再利用時はcrop / motion / treatmentを変更

採点基準:

- scene relevance
- composition
- face / hand integrity
- text contamination
- period consistency
- legal setting consistency
- color palette
- brand fit
- reuse potential
- animation suitability
- 2.5D suitability
- misleading portrayal risk
- real-person risk

実在人物:

- 実在人物らしさは出す
- 精密な本人再現を避ける
- Miranda: back / side profile / hands / silhouette優先
- judges: institution-first / symbolic
- 感情表現は顔の近接再現ではなく、lighting / posture / compositionで表現

## 16.2 アニメーション

基本:

- 映画的静止画演出
- 図解・テキスト演出
- 両方をバランスよく使用
- 毎回手作りしない
- 12種類の再利用テンプレートを第1話で基準化

推奨template catalog:

1. Cinematic Parallax
2. Slow Push In
3. Slow Pull Out
4. Horizontal / Vertical Pan
5. Subject Focus Reveal
6. Event Timeline
7. Relationship / Institution Diagram
8. Map / Location Transition
9. Legal Document Reveal
10. Kinetic Quote
11. Numeric / Comparison Emphasis
12. Chapter / Climax Transition

単調検出例:

- same template 3 times consecutively
- same image within too short interval
- no meaningful visual change for 8+ seconds in high-energy scene
- excessive motion during complex explanation
- repeated direction pattern
- no reset before key conclusion

## 16.3 2.5D

ハイブリッド方針:

- 重要画像: RTX 4090ローカル処理、segmentation、depth estimation、layered export
- 通常画像: Remotion擬似2.5D、zoom、blur、offset、crop、differential motion

本格2.5D候補:

- subject clearly separated
- foreground/background separation
- simple edges
- limited overlap
- no embedded text
- important scene
- high emotional value

Fallback:

```text
full 2.5D -> simplified 2-layer -> pseudo 2.5D -> slow pan / push
```

## 16.4 AI動画

- 1本2〜3カット
- 全編動画化しない
- Runway等は有料gate
- 第1話は実行前にowner確認
- exact animated faceを避ける
- hand / chair / shadow / hallway / document / court building / symbolic movementを優先

## 16.5 字幕・テキスト

- burned open captions
- full English captions
- 1〜2 lines
- short phrase chunks
- tempo-based switching
- readable on mobile
- avoid covering key subject
- preserve safe margins

Caption QC:

- line too long
- orphan word
- punctuation-only line
- reading speed
- collision
- safe area
- color contrast
- subtitle vs citation overlap
- subtitle vs face overlap

## 16.6 ナレーション

- ElevenLabs
- middle-aged male
- low
- calm
- authoritative
- not theatrical
- US English

速度:

- opening: slightly faster, short pauses
- normal: standard
- complex legal explanation: slightly slower
- key conclusion: deliberate pause before and after
- ending: slower, reflective

## 16.7 音楽

1episode 3〜5 tracks:

1. opening tension
2. investigation / narrative propulsion
3. legal analysis
4. ruling / transition
5. reflective ending

Suno library初期:

- 各用途2〜3曲
- total 10〜15 tracks
- 実際の5話を通じて不足を追加
- metadata必須
- loopability
- loudness
- emotional tags
- license record
- source prompt
- version

## 16.8 効果音・環境音

方針:

- 全編へ大量投入しない
- 重要場面のみ
- scene typeで自動候補
- Claude一次配置
- ownerは違和感箇所のみ

分類:

```text
Police/
Interrogation/
Courtroom/
Documents/
Typewriter/
City/
Exterior/
Transitions/
Impacts/
Atmosphere/
RoomTone/
```

## 16.9 サムネイル・タイトル

制作タイミング:

- 初期に仮案
- 完成映像を見て最終調整

採点:

- topic clarity
- curiosity
- title-thumbnail complement
- no redundant wording
- no misleading claim
- mobile readability
- brand consistency
- hook consistency
- US cultural fit
- emotional specificity

判断データ:

- 500 impressions: anomaly only
- 1,000: provisional
- 2,000〜3,000: main judgment

時間だけで判断しない。

## 16.10 公開後分析

指標の役割:

- CTR: title / thumbnail
- 30-second retention: hook
- average view duration: overall content
- average percentage viewed: pacing and structure
- retention drops: exact scene issue
- likes / comments: satisfaction and topic fit

自動反映禁止または慎重:

- factual wording
- hook content
- title claim
- real-person portrayal
- legal interpretation

## 16.11 公開管理

最初の3本:

- private uploadまで自動化候補
- publishはmanual approval

最終承認画面の将来項目:

- final video
- thumbnail 3
- title 3
- description
- scheduled time
- tags
- chapters
- disclaimer
- citations
- AI warnings
- change history
- alternatives
- approve
- request fix
- hold

Disclaimer候補:

- dramatized reconstruction
- not legal advice

最終文言はchannel standardとして別途承認する。

---

# 17. 有料処理と予算

## 17.1 第1話

有料処理ごとにowner確認。

対象:

- ElevenLabs
- Runway
- paid SFX
- paid tester
- other paid API

## 17.2 第2話以降

第1話の実コストが分かった後:

- episode budgetを設定
- budget内自動実行を検討
- budget超過時:
  1. automatic cost optimization
  2. still exceeds
  3. owner approval with expected benefit

## 17.3 削ってはいけないもの

- factual QC
- critical citations
- hook quality
- final audio intelligibility
- real-person review
- publish approval

---

# 18. バックアップ方針

注意: バックアップ本実装はAnimaticレビュー後。  
P0では設計を壊さないことだけ意識する。

将来の保存構成:

- T7 SSD 4TB: active heavy media
- internal physical SSD 4TB+: local backup
- OneDrive 100GB: public version / final approved / final script / citations / settings / approvals / restore manifest
- GitHub: code / schemas / config excluding secrets / decisions / lightweight artifacts

削除方針:

- deletionはnever automatic
- show list and size
- owner batch approval

---

# 19. Git・変更管理

## 19.1 原則

- `main`を壊さない
- 大きな変更前に現状確認
- force push禁止
- `rm -rf`禁止
- secret commit禁止
- generated heavy media commit禁止
- `node_modules`禁止
- binary mediaは原則SSD

## 19.2 重要commit地点

- review feature completed
- owner review completed
- first-cut approved
- final approved
- publish package approved

## 19.3 Commit message例

```text
feat(review): add local animatic review workspace
fix(review): persist draft and resume playback state
chore(review): add schema validation and atomic save
```

## 19.4 ロールバック

各実装について、以下を明示する。

- changed files
- migration有無
- rollback instructions
- data backup path

---

# 20. セキュリティ

## 20.1 Secrets

- `.env` はgitignored
- keysを出力しない
- logへ出さない
- UIへ出さない
- backupしない
- JSON artifactへ入れない
- screenshotへ入れない

## 20.2 External access

- allowlist
- budget gate
- request logging without secrets
- timeout
- retry limit
- no arbitrary URL
- no untrusted command
- no external upload without approval

## 20.3 Midjourney

- terms-compliant operation
- no CAPTCHA bypass
- no rate-limit bypass
- no stealth automation designed to evade controls

## 20.4 Real persons

- visual warning
- scene review
- no implication Miranda was acquitted or released
- correct sequence:
  - conviction overturned
  - later reconvicted
- dramatization notice

---

# 21. 実装優先順位

## P0: 今回必須

1. 現状調査
2. 最小review UI
3. JSON autosave
4. resume
5. keyboard shortcuts
6. tests
7. smoke test
8. owner watches Animatic

## P1: レビュー後

1. review comments整理
2. fix plan
3. low/high risk approval
4. preview reel
5. first revision

## P2: 第1話完成へ

1. visual selection workflow
2. animation template assignment
3. Midjourney asset intake
4. narration generation plan
5. music / SFX
6. first full cut

## P3: 量産化

1. full production dashboard
2. publishing workflow
3. analytics workflow
4. backup automation
5. 2.5D automation

---

# 22. Claude Codeの行動原則

## 22.1 質問しすぎない

軽微な仕様は合理的な仮定で進める。  
質問が必要なのは、停止条件に該当する場合のみ。

## 22.2 過剰実装しない

今の目的はレビュー画面でAnimaticを見ること。  
「将来便利だから」という理由でP2/P3を先に作らない。

## 22.3 既存を使う

優先:

- existing Remotion components
- existing schemas
- existing validation
- existing approval model
- existing git rhythm
- existing safety hooks

## 22.4 失敗時

禁止:

- silent failure
- existing data overwrite
- secret leakage
- broad destructive cleanup

提示すること:

- cause
- scope
- affected files
- rollback
- next proposal

## 22.5 報告

日本語で簡潔かつ具体的に報告する。

必ず明確化:

- 何を確認したか
- 何を変えたか
- なぜ変えたか
- 何が未対応か
- ownerが次に何をするか

---

# 23. 最初の実行指示

この文書を読んだClaude Codeは、以下の順で進める。

```text
1. AGENTS.mdと既存プロジェクト構造を確認する。
2. git status --short を確認する。
3. Animaticの起動方法、Remotion構成、既存のdata読込方法を調査する。
4. 最小レビュー画面の安全な実装方針を作る。
5. 変更予定ファイル、影響範囲、テスト、ロールバック方法を日本語で報告する。
6. 停止条件に該当しない限り、P0のみ実装する。
   - Animatic player
   - current timecode
   - review state
   - 4種marker
   - category/severity付き日本語comment
   - JSON autosave
   - draft recovery
   - resume playback
   - keyboard shortcuts
   - one-command launch
   - browser auto-open
7. 新旧テストを実行する。
8. 実際にレビュー画面を起動してsmoke testする。
9. 完了後、操作方法とURLを日本語で報告する。
10. 有料API、外部公開、YouTube、Midjourney自動化、2.5D、本格ダッシュボードには着手しない。
11. ownerがAnimaticを視聴できる状態で停止する。
```

---

# 24. Claude Codeへそのまま渡す開始メッセージ

以下をClaude Codeへの最初のメッセージとして使える。

```text
このリポジトリのPrime Documentary制作システムについて、添付の
「PRIME_DOCUMENTARY_CLAUDE_CODE_IMPLEMENTATION_SPEC_100.md」
を最上位の実装指示として読んでください。

今回の目的は、Miranda v. Arizonaの約12分Animaticを、ownerがローカルPCで安全にレビューできる最小画面を作ることです。

最初にAGENTS.md、既存decision、schema、Remotion、Python core、tests、git statusを調査してください。
いきなり変更せず、以下を日本語で報告してください。

1. Animaticの現在の起動方法
2. Remotionとdataの構造
3. 最小レビュー画面を追加する最適な場所
4. 変更予定ファイル
5. 影響範囲
6. テスト方法
7. ロールバック方法
8. 今回は実装しないもの
9. 停止条件に該当するリスクの有無

その後、停止条件に該当しない限り、P0だけを実装してください。

必要機能は以下です。
- Animatic再生
- 現在タイムコード取得
- 1回目視聴用の4種marker
- 2回目用のcategory / severity付き日本語comment
- JSON正本
- draft autosave
- 中断再開
- keyboard shortcuts
- 1コマンド起動
- ブラウザ自動表示

Phase 1を超える過剰実装は禁止です。
有料API実行、外部公開、YouTube連携、Midjourney自動化、2.5D、本格ダッシュボード、SQLite、バックアップ本実装には着手しないでください。

既存機能を壊さず、既存テストと新規テストを通し、smoke testまで行ってください。
最後に、操作方法、URL、保存ファイル、backup、テスト結果、既知の制約、ロールバック方法、次にownerが行うことを日本語で報告してください。
```

---

# 25. 完了の定義

この指示書の直近タスクが完了した状態とは、以下である。

- ownerがWindows PCへ戻る
- Claude Codeへ起動を指示する
- review画面がブラウザで開く
- Animaticが再生される
- 1回目はmarkerだけで通し視聴できる
- 2回目は日本語commentを残せる
- 中断しても復元できる
- review JSONが安全に保存される
- Claude CodeがそのJSONを使って次の修正計画を作れる
- それ以上の機能開発をせず、実物レビューへ進める

以上。
