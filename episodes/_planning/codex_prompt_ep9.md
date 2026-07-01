# Codexプロンプト — 第9話(Timbs v. Indiana / 民事資産没収)— このブロックをそのままCodexスレッドに貼る

あなたはCodexです。Prime Documentaryリポジトリ(github.com/miyu1103/prime-documentary、ブランチ
`claude/vibrant-archimedes-2mmr5h`)で作業します。着手前に必ず `CLAUDE.md` と
`episodes/_planning/EP6-8_HANDOFF.md` を読んでください(分担・ツール・ゲートはEP6-8と同じ)。

## あなたの担当
Claudeが左側(topic → research → claims → 台本)を完了済み。**あなたは右側=シーン → 画像 → ナレーション →
音楽 → 編集 → 書き出し を担当。** 台本は**完成・承認済み(APR-0001)・スキーマ検証済み・`state=script_verified`・
ロック済み。書き換え/作り直し禁止。** 事実の誤りに気づいたら自分で直さずSTOPしてオーナーに報告。

## ロック入力(読むだけ・変更不可)
- `episodes/PD-2026-009-timbs/03_script/script.en.v001.md` — ナレーション([VO:]=読み上げ)
- `episodes/PD-2026-009-timbs/03_script/script.annotated.v001.json` — claim連結28スパン(`visual_intent`/`on_screen_text`付き。章順と `estimated_duration_seconds` 約10.3分を尊重)
- `episodes/PD-2026-009-timbs/01_research/claims.v001.json` — 出典つき事実
- `episodes/PD-2026-009-timbs/manifest.json` — state / active revisions

## ツールチェーン
画像=**Codex生成**(主力)＋ローカルSDXL/SVD(量産)。モーション/図版=Remotion。ナレーション=ElevenLabs(課金)。
音楽=Suno再利用ライブラリ。編集・書き出し=**Remotion+FFmpeg**(CPU/libx264・品質最優先)。サムネ=Remotion。
重メディア→ `H:\pd-media`(git対象外)。

## 厳守ルール
1. 全AI画像:AI開示・rights manifest登録・ブランド準拠(`remotion/src/brand.ts`)・**実在人物の肖像/ディープフェイク禁止**
   (Tyson Timbsを識別可能に描かない/invariant 11)。
2. 課金API・アップロード・公開は**オーナー明示承認**＋冪等＋予算なしに禁止。`guard_destructive`/`check_secrets` 尊重。
3. 映像は象徴的再構成・本物の記録映像として出さない。YouTube合成開示＋画面に「symbolic reconstruction」表示。
4. **中立・非政治・広告安全**を厳守。各ステップでコミット。

## パイプライン
1) `pd-scenes`(注釈スパンから計画、visual_intent/on_screen_text流用)→ 2) `pd-generate-assets`(Codex画像＋SDXLバリエ、
QC＋権利登録)→ 3) ナレーション(ElevenLabs。**課金前にオーナー承認**)＋音楽＋Remotionモーション → 4) `pd-build-edit`
(Remotion+FFmpegで組立＆レンダ、QC)→ 5) **初稿ゲート、続いてタイトル/サムネゲートでSTOP・オーナー承認待ち。公開しない。**

## 第9話の固有指定(特に重要)
- 仮タイトル:"Police Can Take Your Car Without Convicting You — The Supreme Court Drew a Line"(サムネゲートで3〜5案検証)。
- リスク **R2 — ただし扱いはセンシティブ**:
  - **「policing for profit(没収で稼ぐ)」等の批判は必ず帰属**(「Institute for Justice / 批判者が主張」)、**擁護側の見解も画面に出す**。
    一方的・党派的にしない(批判は超党派である点を保つ)。**公開前にR3(専門レビュー)を推奨。**
  - Tyson Timbs は中立・役割で。薬物の文脈は控えめ・非扇情的に。**実刑なし(在宅拘禁+保護観察)を強調**。
  - 処分は **「vacated and remanded(破棄・差戻し)」**。最高裁は没収自体を違憲と断じていない。差戻し後にTimbsは車を取り戻した(CLM-0010)。
- ビジュアル一本筋(現在形/「国家が“奪える”もの」クラスターの開幕):
  冒頭=押収/レッカーのシルエット(顔なし)。第1幕=保険金→ランドローバー、**$10,000の上限罰金 vs 約$42,000の車**の天秤アニメ。
  第2幕=「合衆国 対 一台の車」=**物そのものを訴える(in rem)**モチーフ。第3幕=**マグナカルタ(1215)→2019**の年表、2019/9–0/"586 U.S. 146"テロップ。
  第4幕=差戻しでTimbsは車を保持。結末=シリーズ連結「**見る → 奪う**」、次回(EP10=Kelo/家の収用)へ。
- 配色:黒/紺/エレクトリックブルー/金。

## 最初のアクション
ロック入力4ファイル＋CLAUDE.md §11＋handoffを読み、**画像生成の前に**シーン計画の要約(章→ショット→画像プロンプト→画面テキスト)を
オーナーレビュー用に投稿。その後パイプラインを進め、各ゲートで停止。
