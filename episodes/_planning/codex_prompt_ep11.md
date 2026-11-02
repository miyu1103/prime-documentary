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

## ツール & 素材方針（2026-06-20改定 — 紙芝居回避・実写動画を主軸・権利ゲート厳守）
- **しょぼい動画にしない＝“静止で見せない”。** AI画像(Codex/SDXL)は主役級に**たくさん使ってOK**。ただし全カット必ず動かす（寄り引き/パララックス/微ズーム/グレイン/被写界深度）。さらに実写の動画クリップを要所に混ぜて単調を回避。Runwayは高コストなので決め所だけ。
- 編集=Remotion+FFmpeg。AI画像=Codex生成＋SDXL（見せ場用）。ナレ=ElevenLabs(課金=要承認)。音楽=Suno。
- **無料動画素材を主軸に**：Pexels / Pixabay / Mixkit。必要に応じ Wikimedia Commons / NASA、音は YouTube Audio Library も可。既存ライブラリ=`H:\pd-media\assets\stock`(STOCK_MANIFEST.json)＋`references/README.md`・`references/stock_manifest.json`。
- **権利管理（最重要・厳守）**：商用利用可の素材のみ使用。1点ずつ「出典URL・作者・ライセンス・取得日・使用シーン・sha256」をrights台帳に記録。
  - **禁止取得元**＝通常のYouTube/TikTok/Instagram/X・ニュース番組/TV番組・映画・アニメ・MV・スポーツ映像・まとめサイト・Google画像検索 からの無断取得は使わない。
  - **権利が曖昧な素材はRemotionのタイムラインに自動投入しない**（review送り）。OKの素材だけ投入。有料サイト(Storyblocks/Artlist/Envato/Adobe Stock)連携は今は不要。
- ラフカット=Remotionで「実写動画＋画像＋ナレ＋BGM＋SFX＋字幕＋テロップ」を合成→**人間が確認・修正して完成**（完全自動にしない）。重メディア→`H:\pd-media`。

## 厳守ルール
1. 全AI画像:AI開示・rights manifest登録・ブランド準拠・**実在人物の肖像/ディープフェイク禁止**(Brandi Levy等)。
2. 課金API・公開はオーナー承認＋冪等＋予算なしに禁止。フック尊重。各ステップでコミット。
3. **★広告安全(最重要):投稿のキャプションは罵倒語。ナレーションは絶対に読まない(描写のみ)。画面テキストは伏字/ぼかし。**
4. 中立(学校 vs 生徒のどちらにも寄らない。学校側の秩序維持の言い分も公平に)。

## パイプライン
`04_scenes/shotlist.v001.json`(`scripts/plan_scenes.py`で生成済=各スパンの推奨素材種別/動き/検索キーワード/秒数/テロップ) → `pd-generate-assets`(**AI画像(Codex/SDXL)を大量に＋実写動画を要所に・全カット動かす**、QC＋**権利台帳登録・OK素材のみ採用**)→ ナレーション(ElevenLabs・**課金前に承認**)
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
