# Codexプロンプト — 第8話(Carpenter v. United States)— このブロックをそのままCodexスレッドに貼る

あなたはCodexです。Prime Documentaryリポジトリ(github.com/miyu1103/prime-documentary、ブランチ
`claude/vibrant-archimedes-2mmr5h`)で作業します。着手前に必ず `CLAUDE.md` と
`episodes/_planning/EP6-8_HANDOFF.md` を読んでください。

## あなたの担当
分担(オーナー決定):Claudeが左側(topic → research → claims → 台本)を完了済み。
**あなたは右側=シーン → 画像 → ナレーション → 音楽 → 編集 → 書き出し を担当します。**

この話の台本は**完成・オーナー承認済み(APR-0001)・スキーマ検証済み・`state = script_verified`・ロック済み**です。
**台本・注釈台本・claimsを書き換え/要約し直し/作り直してはいけません。** 事実の誤りに気づいたら、自分で
直さずSTOPしてオーナーに報告(編集すると承認ゲートが再オープンします)。

## ロック入力(読むだけ。変更不可)
- `episodes/PD-2026-008-carpenter/03_script/script.en.v001.md` — ナレーション([VO:]=読み上げ)
- `episodes/PD-2026-008-carpenter/03_script/script.annotated.v001.json` — claim連結の30スパン。各スパンに
  `visual_intent` と `on_screen_text` あり。これに沿ってシーンを作り、章順と `estimated_duration_seconds`
  (約11分)を尊重する。
- `episodes/PD-2026-008-carpenter/01_research/claims.v001.json` — 各スパンの根拠(出典つき事実)
- `episodes/PD-2026-008-carpenter/manifest.json` — 現在のstate / active revisions

## ツールチェーン(正:CLAUDE.md §11 + handoff §0A)
- 画像:**Codex画像生成=主力**。量産バリエは ローカルSDXL/SVD。
- モーション/図版:Remotion。ナレーション:ElevenLabs(課金)。音楽/SFX:Suno再利用ライブラリ。
- 編集・書き出し:**Remotion + FFmpeg**(CPU/libx264・品質最優先)。サムネ:Remotion。
- 重メディア(画像/動画/音声/レンダ)→ `H:\pd-media`(git対象外)。リポジトリは頭脳(設計)のみ。

## 厳守ルール(交渉不可)
1. すべてのAI画像:AI生成と開示、rights manifestに登録(origin/creator/license/verified_at)、ブランド準拠
   (`remotion/src/brand.ts`)、**実在人物の肖像・ディープフェイク禁止**(Timothy Carpenterを識別可能な実在人物
   として描かない/invariant 11)。
2. 課金API(ElevenLabs/Runway)・アップロード・公開は、**オーナーの明示承認**＋冪等キー＋予算チェックなしに実行禁止。
   `guard_destructive` / `check_secrets` フックを尊重。
3. 映像はすべて象徴的再構成であり、本物の記録映像として提示しない。YouTubeの改変/合成コンテンツ開示を設定し、
   画面上に「symbolic reconstruction」表示を残す。
4. トーンは中立・広告に安全・教育的。各ステップごとにブランチへコミット。

## 実行パイプライン(この話)
1. `pd-scenes` → 注釈スパンから シーン/ショット/ビジュアル/画面テキスト計画を作成(連続性＋生成仕様)。
   各スパンの `visual_intent` と `on_screen_text` を流用。
2. `pd-generate-assets` → 画像生成(Codex主力＋SDXL/SVDでバリエ)、QC、権利メタデータ登録。
3. ナレーション(ElevenLabs。**課金実行前にオーナー承認を取る**)＋音楽(Sunoライブラリ)＋Remotionモーション。
4. `pd-build-edit` → Remotion + FFmpeg で組み立て＆レンダ、QC。
5. **初稿(first-cut)レビューゲート、続いてタイトル/サムネのゲートでSTOPし、オーナー承認を待つ。公開はしない。**

## 第8話の固有指定
- 仮タイトル:"Your Phone Is Tracking You — and the Police Wanted the Map."(タイトル/サムネのゲートで3〜5案を検証)
- リスク区分:**R2 — Carpenterは公的記録上の有罪確定者。中立・事実ベースで、記録を超えて有罪を論評しない。**
- 画面テキストの正確性:評決は **5–4**(CLM-0002)。**「6–3」とする要約は無視**(AI生成の誤要約。正しくは5–4)。
- ビジュアルの一本筋(現在形フレーム/シリーズの締め):冒頭は暗い地図上に位置トレイルが広がる「127日・令状なし」。
  第1幕=デトロイトの2010–2011年の店舗強盗(象徴)→ 基地局へのping が経路になる →「約12,898点」。
  第2幕=細い1本の発信番号リスト vs 生活全体を地図化する位置トレイル(第三者法理:Smith 1979 / Miller 1976)。
  第3幕=2018 / 5–4 / "Carpenter v. United States, 585 U.S. 296" の下部テロップ。
  第4幕=「位置は最初の扉にすぎない」(検索/購入/メッセージ/センサー)。
  結末=三部作のペイオフ:Terry(身体)→ Riley(電話の中身)→ Carpenter(位置)を回収し、視聴者自身の端末に着地。
- ブランド配色:黒 / 紺 / エレクトリックブルー / 金(`remotion/src/brand.ts` 参照)。

## 最初のアクション
上のロック入力4ファイルと `CLAUDE.md` §11 + handoff を読み、**画像生成の前に**シーン計画の要約(章 → ショット →
画像プロンプト → 画面テキスト)をオーナーレビュー用に投稿する。その後パイプラインを進め、各ゲートで停止する。
