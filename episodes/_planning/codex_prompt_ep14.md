# Codexプロンプト — 第14話(Lange v. California / 自宅への追跡)— このブロックをそのままCodexスレッドに貼る

あなたはCodexです。Prime Documentaryリポジトリ(branch `claude/vibrant-archimedes-2mmr5h`)で作業。
着手前に `CLAUDE.md`・`episodes/_planning/EP6-8_HANDOFF.md`・`references/README.md` を読む。分担・ツール・ゲートはEP6-13と同じ。

## 担当
Claudeが左側完了。**あなたは右側=シーン→画像→ナレ→音楽→編集→書き出し。** 台本は**完成・承認済み(APR-0001)・検証済み・
`script_verified`・ロック。書き換え禁止。** 誤りはSTOPして報告。

## ロック入力(読むだけ)
- `episodes/PD-2026-014-lange/03_script/script.en.v001.md` / `script.annotated.v001.json`(23スパン・約10.3分)
- `episodes/PD-2026-014-lange/01_research/claims.v001.json` / `manifest.json`

## ツール & 素材方針（2026-06-20改定 — 紙芝居回避・実写動画を主軸・権利ゲート厳守）
- **しょぼい動画にしない＝“静止で見せない”。** AI画像(Codex/SDXL)は主役級に**たくさん使ってOK**。ただし全カット必ず動かす（寄り引き/パララックス/微ズーム/グレイン/被写界深度）。さらに実写の動画クリップを要所に混ぜて単調を回避。Runwayは高コストなので決め所だけ。
- 編集=Remotion+FFmpeg。AI画像=Codex生成＋SDXL（見せ場用）。ナレ=ElevenLabs(課金=要承認)。音楽=Suno。
- **無料動画素材を主軸に**：Pexels / Pixabay / Mixkit。必要に応じ Wikimedia Commons / NASA、音は YouTube Audio Library も可。既存ライブラリ=`H:\pd-media\assets\stock`(STOCK_MANIFEST.json)＋`references/README.md`・`references/stock_manifest.json`（パトカー `pexels_police_car.jpg` も流用可）。
- **権利管理（最重要・厳守）**：商用利用可の素材のみ使用。1点ずつ「出典URL・作者・ライセンス・取得日・使用シーン・sha256」をrights台帳に記録。
  - **禁止取得元**＝通常のYouTube/TikTok/Instagram/X・ニュース番組/TV番組・映画・アニメ・MV・スポーツ映像・まとめサイト・Google画像検索 からの無断取得は使わない。
  - **権利が曖昧な素材はRemotionのタイムラインに自動投入しない**（review送り）。OKの素材だけ投入。有料サイト(Storyblocks/Artlist/Envato/Adobe Stock)連携は今は不要。
- ラフカット=Remotionで「実写動画＋画像＋ナレ＋BGM＋SFX＋字幕＋テロップ」を合成→**人間が確認・修正して完成**（完全自動にしない）。重メディア→`H:\pd-media`。

## 厳守ルール
1. 全AI画像:AI開示・rights manifest登録・ブランド準拠・実在人物の肖像/ディープフェイク禁止(Arthur Lange等)。
2. 課金API・公開はオーナー承認＋冪等＋予算なしに禁止。各ステップでコミット。
3. **★評決の表記(重要):「判決(結論)は全員一致=9-0で破棄差戻し」であって「全員一致の意見」ではない。Roberts(＋Alito)は結論同意だが
   より広い追跡立入ルールを主張=両論を公平に。** 争点は「軽罪逃走の追跡」でありDUIではない。中立(自宅のプライバシー vs 警官の安全)。

## パイプライン
`04_scenes/shotlist.v001.json`(`scripts/plan_scenes.py`で生成済=各スパンの推奨素材種別/動き/検索キーワード/秒数/テロップ) → `pd-generate-assets`(**AI画像(Codex/SDXL)を大量に＋実写動画を要所に・全カット動かす**、QC＋**権利台帳登録・OK素材のみ採用**)→ ナレ(ElevenLabs・課金前に承認)＋音楽＋Remotion
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
