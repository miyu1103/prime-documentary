# Codexプロンプト — 第11話(Mahanoy v. B.L. / 学校とSNS言論)— このブロックをそのままCodexスレッドに貼る

あなたはCodexです。Prime Documentaryリポジトリ(github.com/miyu1103/prime-documentary、ブランチ
`claude/vibrant-archimedes-2mmr5h`)で作業。着手前に `CLAUDE.md`・`episodes/_planning/EP6-8_HANDOFF.md`・
`references/README.md`(使用可の実素材)を読む。分担・ツール・ゲートはEP6-10と同じ。

## 担当
Claudeが左側(topic→research→claims→台本)完了。**あなたは右側=シーン→画像→ナレ→音楽→編集→書き出し。**
台本は**完成・承認済み(APR-0001)・検証済み・`script_verified`・ロック。書き換え禁止。** 誤りはSTOPして報告。

## ロック入力(読むだけ)
- `episodes/PD-2026-011-mahanoy/03_script/script.en.v001.md` / `script.annotated.v001.json`(28スパン・約10.1分)
- `episodes/PD-2026-011-mahanoy/01_research/claims.v001.json` / `manifest.json`

## ツール & 実素材
画像=Codex生成＋SDXL。編集=Remotion+FFmpeg。ナレ=ElevenLabs(課金=要承認)。音楽=Suno。
**実写の使用可素材を活用**(B-roll・導入):`H:\pd-media\assets\stock`(STOCK_MANIFEST.json)＋`references/README.md`。
**1点ずつライセンス確認＋クレジット＋rights manifest記録**。重メディア→`H:\pd-media`。

## 厳守ルール
1. 全AI画像:AI開示・rights manifest登録・ブランド準拠・**実在人物の肖像/ディープフェイク禁止**(Brandi Levy等)。
2. 課金API・公開はオーナー承認＋冪等＋予算なしに禁止。フック尊重。各ステップでコミット。
3. **★広告安全(最重要):投稿のキャプションは罵倒語。ナレーションは絶対に読まない(描写のみ)。画面テキストは伏字/ぼかし。**
4. 中立(学校 vs 生徒のどちらにも寄らない。学校側の秩序維持の言い分も公平に)。

## パイプライン
`pd-scenes` → `pd-generate-assets`(Codex画像＋SDXL＋実写配置、QC＋権利登録)→ ナレーション(ElevenLabs・**課金前に承認**)
＋音楽＋Remotion → `pd-build-edit`(Remotion+FFmpeg)→ **初稿・タイトル/サムネのゲートでSTOP。公開しない。**

## 第11話の固有指定
- 仮タイトル:"Can Your School Punish You for a Post You Made Off Campus?"(サムネゲートで3〜5案)。
- リスク **R2**。Brandi Levy(B.L.)は本人がACLUと共に公表済み=実名可・中立描写。**実刑等の話ではない**。
- ビジュアル一本筋(現在形/「言える」クラスター開幕):冒頭=夜のスマホ画面に投稿が打たれる(**キャプションは伏字**)。
  第1幕=Mahanoy PA・JVチア・コンビニ前の週末・消えるはずのSnapが**スクショで残る**。第2幕=Tinker(1969)の「schoolhouse gate」と
  「substantial disruption」、スマホで“校門”が消える図。第3幕=2021/8–1/"594 U.S. 180"テロップ、Breyerの「nurseries of democracy」、
  Thomas単独反対、残された例外(いじめ/脅迫/カンニング)。第4幕=曖昧なグレーゾーン。結末=シリーズ連結「見る→奪う→言える」、
  次回EP12(強制仲裁=自分で手放す権利)へ。
- 配色:黒/紺/エレクトリックブルー/金。

## 最初のアクション
ロック入力＋handoff＋references/READMEを読み、**画像生成の前に**シーン計画の要約(章→ショット→実素材/生成の別→画面テキスト[伏字含む])を
オーナーレビュー用に投稿。その後パイプラインを進め、各ゲートで停止。
