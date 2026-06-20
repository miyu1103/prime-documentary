# Codexプロンプト — 第14話(Lange v. California / 自宅への追跡)— このブロックをそのままCodexスレッドに貼る

あなたはCodexです。Prime Documentaryリポジトリ(branch `claude/vibrant-archimedes-2mmr5h`)で作業。
着手前に `CLAUDE.md`・`episodes/_planning/EP6-8_HANDOFF.md`・`references/README.md` を読む。分担・ツール・ゲートはEP6-13と同じ。

## 担当
Claudeが左側完了。**あなたは右側=シーン→画像→ナレ→音楽→編集→書き出し。** 台本は**完成・承認済み(APR-0001)・検証済み・
`script_verified`・ロック。書き換え禁止。** 誤りはSTOPして報告。

## ロック入力(読むだけ)
- `episodes/PD-2026-014-lange/03_script/script.en.v001.md` / `script.annotated.v001.json`(23スパン・約10.3分)
- `episodes/PD-2026-014-lange/01_research/claims.v001.json` / `manifest.json`

## ツール & 実素材
画像=Codex生成＋SDXL。編集=Remotion+FFmpeg。ナレ=ElevenLabs(課金=要承認)。音楽=Suno。
**実写の使用可素材を活用**:`H:\pd-media\assets\stock`(パトカー `pexels_police_car.jpg` が好適)＋`references/README.md`。1点ずつライセンス確認＋クレジット＋rights manifest記録。重メディア→`H:\pd-media`。

## 厳守ルール
1. 全AI画像:AI開示・rights manifest登録・ブランド準拠・実在人物の肖像/ディープフェイク禁止(Arthur Lange等)。
2. 課金API・公開はオーナー承認＋冪等＋予算なしに禁止。各ステップでコミット。
3. **★評決の表記(重要):「判決(結論)は全員一致=9-0で破棄差戻し」であって「全員一致の意見」ではない。Roberts(＋Alito)は結論同意だが
   より広い追跡立入ルールを主張=両論を公平に。** 争点は「軽罪逃走の追跡」でありDUIではない。中立(自宅のプライバシー vs 警官の安全)。

## パイプライン
`pd-scenes` → `pd-generate-assets`(Codex画像＋SDXL＋実写、QC＋権利登録)→ ナレ(ElevenLabs・課金前に承認)＋音楽＋Remotion
→ `pd-build-edit`(Remotion+FFmpeg)→ **初稿・タイトル/サムネのゲートでSTOP。公開しない。**

## 第14話の固有指定
- 仮タイトル:"Can a Police Officer Follow You Into Your Own Home?"(サムネゲートで3〜5案)。
- リスク **R2・中立厳守**。
- ビジュアル一本筋(現在形/「最後の砦=自宅」):冒頭=**降りるガレージ扉に足を差し込む**瞬間(顔なし)。第1幕=Sonoma、騒音/クラクション→
   ライト点灯→約100フィート先の自宅ガレージへ→足で扉を止め立入→DUI(=立入の結果)。第2幕=自宅の最強保護、exigent circumstances
   (危険/証拠隠滅/逃走)、「軽罪」の幅(暴行〜騒音)。第3幕=2021/9–0(判決)/"594 U.S. 295"、Kagan(個別判断)、Roberts+Alito(結論同意・広い
   ルール志向)、破棄差戻し。第4幕=実務的含意(原則入れない・真の緊急時のみ)。結末=シリーズ総括、次回EP15(Theranos=最終話・視点反転)へ。
- 配色:黒/紺/エレクトリックブルー/金。

## 最初のアクション
ロック入力＋handoff＋references/READMEを読み、**画像生成の前に**シーン計画の要約(章→ショット→実素材/生成の別→画面テキスト)を
オーナーレビュー用に投稿。その後パイプラインを進め、各ゲートで停止。
