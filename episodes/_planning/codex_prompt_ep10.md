# Codexプロンプト — 第10話(Kelo v. New London / 収用)— このブロックをそのままCodexスレッドに貼る

あなたはCodexです。Prime Documentaryリポジトリ(github.com/miyu1103/prime-documentary、ブランチ
`claude/vibrant-archimedes-2mmr5h`)で作業。着手前に `CLAUDE.md` と `episodes/_planning/EP6-8_HANDOFF.md`、
`references/README.md`(使用可の実素材)を読む。分担・ツール・ゲートはEP6-9と同じ。

## あなたの担当
Claudeが左側(topic→research→claims→台本)を完了済み。**あなたは右側=シーン→画像→ナレーション→音楽→編集→
書き出し。** 台本は**完成・承認済み(APR-0001)・検証済み・`state=script_verified`・ロック。書き換え禁止。**
誤りに気づいたら自分で直さずSTOPして報告。

## ロック入力(読むだけ・変更不可)
- `episodes/PD-2026-010-kelo/03_script/script.en.v001.md` / `script.annotated.v001.json`(28スパン・約10.5分)
- `episodes/PD-2026-010-kelo/01_research/claims.v001.json` / `manifest.json`

## ツールチェーン & 実素材(重要)
- 画像=Codex生成(主力)＋SDXL量産。編集=Remotion+FFmpeg。ナレ=ElevenLabs(課金=要承認)。音楽=Suno。
- **実写の使用可素材を積極活用**(B-roll・導入):`H:\pd-media\assets\stock`(`STOCK_MANIFEST.json`参照)に
  PD/CC0/Pexels素材あり(売家・建物解体の映像、最高裁庁舎、法廷の木槌、憲法/権利章典、$1札 等)。
  さらに `references/README.md` の承認ソースから追加可。**1点ずつライセンス確認＋クレジット＋rights manifest記録**。
- 生成画像は象徴的再構成のみ。重メディア→`H:\pd-media`。

## 厳守ルール
1. 全AI画像:AI開示・rights manifest登録・ブランド準拠・**実在人物の肖像/ディープフェイク禁止**(Susette Kelo等)。
2. 課金API・アップロード・公開はオーナー明示承認＋冪等＋予算なしに禁止。フック尊重。
3. 映像は象徴的再構成。YouTube合成開示＋「symbolic reconstruction」表示。実写は使用可素材のみ。
4. **中立・非政治・広告安全**(Keloの反発は超党派。市の経済開発の言い分も公平に出す)。各ステップでコミット。

## パイプライン
1) `pd-scenes` → 2) `pd-generate-assets`(Codex画像＋SDXL、実写素材の配置、QC＋権利登録)→ 3) ナレーション
(ElevenLabs・**課金前に承認**)＋音楽＋Remotionモーション → 4) `pd-build-edit`(Remotion+FFmpeg)→ 5) **初稿・
タイトル/サムネのゲートでSTOP・承認待ち。公開しない。**

## 第10話の固有指定
- 仮タイトル:"The Government Took Their Homes for a Developer — Then the Plan Collapsed"(サムネゲートで3〜5案)。
- リスク **R2**:中立厳守。**州の改革数(CLM-0008)は“約40州以上”の範囲＋Institute for Justice帰属**、多くは「弱い」批判ありと併記。
  実在人物は役割で中立。**NLDC=市の開発代理(独立した民間が単独で収用したのではない)**。
- ビジュアル一本筋(現在形/「奪う」クラスターの締め):冒頭=更地に1軒だけ残る家(＝“pink house”、顔なし)。第1幕=
  Fort Trumbullの普通の家並み(実写B-roll可)。第2幕=「public use」2語のズーム/「狭い解釈 vs 広い解釈(public purpose)」図。
  第3幕=2005/5–4/"545 U.S. 469"テロップ、O'Connor反対の核「“for public use”が消される」。第4幕=**更地のまま/2009年Pfizer撤退**の皮肉(解体映像・空地の実写可)、ピンクの家は移設され現存。結末=シリーズ連結「見る→奪う→次は“言える”」、次回EP11(言論の自由)へ。
- 配色:黒/紺/エレクトリックブルー/金。

## 最初のアクション
ロック入力＋handoff＋references/READMEを読み、**画像生成の前に**シーン計画の要約(章→ショット→実素材/生成画像の別→画面テキスト)を
オーナーレビュー用に投稿。その後パイプラインを進め、各ゲートで停止。
