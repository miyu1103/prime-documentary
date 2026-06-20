# Codexプロンプト — 第12話(強制仲裁 / Concepcion 2011 + Epic 2018)— このブロックをそのままCodexスレッドに貼る

あなたはCodexです。Prime Documentaryリポジトリ(branch `claude/vibrant-archimedes-2mmr5h`)で作業。
着手前に `CLAUDE.md`・`episodes/_planning/EP6-8_HANDOFF.md`・`references/README.md` を読む。分担・ツール・ゲートはEP6-11と同じ。

## 担当
Claudeが左側(topic→research→claims→台本)完了。**あなたは右側=シーン→画像→ナレ→音楽→編集→書き出し。**
台本は**完成・承認済み(APR-0001)・検証済み・`script_verified`・ロック。書き換え禁止。** 誤りはSTOPして報告。

## ロック入力(読むだけ)
- `episodes/PD-2026-012-arbitration/03_script/script.en.v001.md` / `script.annotated.v001.json`(25スパン・約10.2分)
- `episodes/PD-2026-012-arbitration/01_research/claims.v001.json` / `manifest.json`

## ツール & 実素材
画像=Codex生成＋SDXL。編集=Remotion+FFmpeg。ナレ=ElevenLabs(課金=要承認)。音楽=Suno。
**実写の使用可素材を活用**:`H:\pd-media\assets\stock`(契約書サイン `pexels_signing_contract.jpg` が好適)＋`references/README.md`。
1点ずつライセンス確認＋クレジット＋rights manifest記録。重メディア→`H:\pd-media`。

## 厳守ルール
1. 全AI画像:AI開示・rights manifest登録・ブランド準拠・実在人物の肖像/ディープフェイク禁止。
2. 課金API・公開はオーナー承認＋冪等＋予算なしに禁止。各ステップでコミット。
3. **★中立(最重要):これは政策論争。「強制仲裁(forced arbitration)」は批判側の用語=中立の「義務的/事前仲裁」と併記。
   批判側/擁護側の主張は必ず帰属(「批判者は…」「擁護者は…」)。コスト・速さ等の実証は事実として断定しない。**
4. 企業(AT&T, Epic Systems)は事件事実のみ・論評しない。

## パイプライン
`pd-scenes` → `pd-generate-assets`(Codex画像＋SDXL＋実写、QC＋権利登録)→ ナレ(ElevenLabs・課金前に承認)＋音楽＋Remotion
→ `pd-build-edit`(Remotion+FFmpeg)→ **初稿・タイトル/サムネのゲートでSTOP。公開しない。**

## 第12話の固有指定
- 仮タイトル:"The Fine Print That Took Away Your Right to Sue"(サムネゲートで3〜5案)。
- リスク **R2・中立厳守**。
- ビジュアル一本筋(現在形/「自分で手放す権利」):冒頭=「I Agree」をタップ＋細字が流れる。第1幕=「無料」の電話＋$30の税、
  1件の$30 vs 群衆×$30=巨額(集団訴訟の図)。第2幕=1925年FAA、クラス免除の一文、批判vs擁護を**左右対称の天秤**で。
  第3幕=2011/5–4/"563 U.S. 333"、Scalia多数・Breyer反対、2018 Epic(Gorsuch多数・Ginsburg反対)で職場へ拡大。
  第4幕=スマホ/銀行/アプリ/職場に遍在、論争は継続。結末=シリーズ連結、次回EP13(DNA採取)へ。
- 配色:黒/紺/エレクトリックブルー/金。

## 最初のアクション
ロック入力＋handoff＋references/READMEを読み、**画像生成の前に**シーン計画の要約(章→ショット→実素材/生成の別→画面テキスト)を
オーナーレビュー用に投稿。その後パイプラインを進め、各ゲートで停止。
