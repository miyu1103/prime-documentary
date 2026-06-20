# Codexプロンプト — 第13話(Maryland v. King / 逮捕時のDNA)— このブロックをそのままCodexスレッドに貼る

あなたはCodexです。Prime Documentaryリポジトリ(branch `claude/vibrant-archimedes-2mmr5h`)で作業。
着手前に `CLAUDE.md`・`episodes/_planning/EP6-8_HANDOFF.md`・`references/README.md` を読む。分担・ツール・ゲートはEP6-12と同じ。

## 担当
Claudeが左側完了。**あなたは右側=シーン→画像→ナレ→音楽→編集→書き出し。** 台本は**完成・承認済み(APR-0001)・検証済み・
`script_verified`・ロック。書き換え禁止。** 誤りはSTOPして報告。

## ロック入力(読むだけ)
- `episodes/PD-2026-013-king/03_script/script.en.v001.md` / `script.annotated.v001.json`(23スパン・約10.1分)
- `episodes/PD-2026-013-king/01_research/claims.v001.json` / `manifest.json`

## ツール & 実素材
画像=Codex生成＋SDXL。編集=Remotion+FFmpeg。ナレ=ElevenLabs(課金=要承認)。音楽=Suno。
**実写の使用可素材を活用**:`H:\pd-media\assets\stock`＋`references/README.md`。1点ずつライセンス確認＋クレジット＋rights manifest記録。重メディア→`H:\pd-media`。

## 厳守ルール
1. 全AI画像:AI開示・rights manifest登録・ブランド準拠・実在人物の肖像/ディープフェイク禁止(Alonzo King等)。
2. 課金API・公開はオーナー承認＋冪等＋予算なしに禁止。各ステップでコミット。
3. **★枠組み(最重要):Kingは“暴行”で逮捕(相当の理由あり)。強姦は後のDB照合の結果。映像も語りも「DNA採取が逮捕の目的/口実」だと
   絶対に示唆しない。** 性犯罪の題材は扇情的にせず冷静に。中立(身元確認・公共安全 vs プライバシー、両論公平)。

## パイプライン
`pd-scenes` → `pd-generate-assets`(Codex画像＋SDXL＋実写、QC＋権利登録)→ ナレ(ElevenLabs・課金前に承認)＋音楽＋Remotion
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
