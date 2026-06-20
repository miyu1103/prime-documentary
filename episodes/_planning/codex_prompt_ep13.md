# Codexプロンプト — 第13話(Maryland v. King / 逮捕時のDNA)— このブロックをそのままCodexスレッドに貼る

あなたはCodexです。Prime Documentaryリポジトリ(branch `claude/vibrant-archimedes-2mmr5h`)で作業。
着手前に `CLAUDE.md`・`episodes/_planning/EP6-8_HANDOFF.md`・`references/README.md` を読む。分担・ツール・ゲートはEP6-12と同じ。

## 担当
Claudeが左側完了。**あなたは右側=シーン→画像→ナレ→音楽→編集→書き出し。** 台本は**完成・承認済み(APR-0001)・検証済み・
`script_verified`・ロック。書き換え禁止。** 誤りはSTOPして報告。

## ロック入力(読むだけ)
- `episodes/PD-2026-013-king/03_script/script.en.v001.md` / `script.annotated.v001.json`(23スパン・約10.1分)
- `episodes/PD-2026-013-king/01_research/claims.v001.json` / `manifest.json`

## ツール & 素材方針（2026-06-20改定 — 紙芝居回避・実写動画を主軸・権利ゲート厳守）
- **静止画の羅列で“紙芝居”にしない。** B-rollは原則「実写の動画クリップ」を主役に。AI生成(Codex/SDXL/Runway)は**見せ場だけ**（Runwayはコスト都合で全カット不可）。
- 編集=Remotion+FFmpeg。AI画像=Codex生成＋SDXL（見せ場用）。ナレ=ElevenLabs(課金=要承認)。音楽=Suno。
- **無料動画素材を主軸に**：Pexels / Pixabay / Mixkit。必要に応じ Wikimedia Commons / NASA、音は YouTube Audio Library も可。既存ライブラリ=`H:\pd-media\assets\stock`(STOCK_MANIFEST.json)＋`references/README.md`・`references/stock_manifest.json`。
- **権利管理（最重要・厳守）**：商用利用可の素材のみ使用。1点ずつ「出典URL・作者・ライセンス・取得日・使用シーン・sha256」をrights台帳に記録。
  - **禁止取得元**＝通常のYouTube/TikTok/Instagram/X・ニュース番組/TV番組・映画・アニメ・MV・スポーツ映像・まとめサイト・Google画像検索 からの無断取得は使わない。
  - **権利が曖昧な素材はRemotionのタイムラインに自動投入しない**（review送り）。OKの素材だけ投入。有料サイト(Storyblocks/Artlist/Envato/Adobe Stock)連携は今は不要。
- ラフカット=Remotionで「実写動画＋画像＋ナレ＋BGM＋SFX＋字幕＋テロップ」を合成→**人間が確認・修正して完成**（完全自動にしない）。重メディア→`H:\pd-media`。

## 厳守ルール
1. 全AI画像:AI開示・rights manifest登録・ブランド準拠・実在人物の肖像/ディープフェイク禁止(Alonzo King等)。
2. 課金API・公開はオーナー承認＋冪等＋予算なしに禁止。各ステップでコミット。
3. **★枠組み(最重要):Kingは“暴行”で逮捕(相当の理由あり)。強姦は後のDB照合の結果。映像も語りも「DNA採取が逮捕の目的/口実」だと
   絶対に示唆しない。** 性犯罪の題材は扇情的にせず冷静に。中立(身元確認・公共安全 vs プライバシー、両論公平)。

## パイプライン
`pd-scenes`(各スパンの検索キーワード/秒数/テロップを整理) → `pd-generate-assets`(**実写動画を主役**＋見せ場のみAI(Codex/SDXL)、QC＋**権利台帳登録・OK素材のみ採用**)→ ナレ(ElevenLabs・課金前に承認)＋音楽＋Remotion
→ `pd-build-edit`(Remotion+FFmpeg)→ **初稿・タイトル/サムネのゲートでSTOP。公開しない。**

## 第13話の固有指定
- 仮タイトル:"The Police Can Take Your DNA When They Arrest You"(サムネゲートで3〜5案)。
- リスク **R2・中立厳守・冷静**。
- ビジュアル一本筋(現在形/「体から取る」):冒頭=頬の綿棒スワブ＋DNA二重らせんがDBへ。第1幕=2009メリーランド、暴行で逮捕→
   booking でスワブ(**逮捕理由ではない**)→DBで2003年の未解決事件に一致。第2幕=指紋/写真=身元確認 vs DNA=証拠の捜索?、CODIS。
  第3幕=2013/5–4/"569 U.S. 435"、Kennedy多数(指紋類似)、Scalia反対(＋Ginsburg/Sotomayor/Kagan＝党派横断)、
  「rightly or wrongly, and for whatever reason」、bench読み上げ。第4幕=逮捕＝DNA提出が常態、両論の現実。結末=次回EP14(自宅への追跡)へ。
- 配色:黒/紺/エレクトリックブルー/金。

## 最初のアクション
ロック入力＋handoff＋references/READMEを読み、**画像生成の前に**シーン計画の要約(章→ショット→実素材/生成の別→画面テキスト)を
オーナーレビュー用に投稿。その後パイプラインを進め、各ゲートで停止。
