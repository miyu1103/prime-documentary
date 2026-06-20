# Codexプロンプト — 第15話(最終話 / Theranos・Elizabeth Holmes)— このブロックをそのままCodexスレッドに貼る

あなたはCodexです。Prime Documentaryリポジトリ(branch `claude/vibrant-archimedes-2mmr5h`)で作業。
着手前に `CLAUDE.md`・`episodes/_planning/EP6-8_HANDOFF.md`・`references/README.md` を読む。分担・ツール・ゲートはEP6-14と同じ。

## 担当
Claudeが左側完了。**あなたは右側=シーン→画像→ナレ→音楽→編集→書き出し。** 台本は**完成・承認済み(APR-0001)・検証済み・
`script_verified`・ロック。書き換え禁止。** 誤りはSTOPして報告。

## ロック入力(読むだけ)
- `episodes/PD-2026-015-theranos/03_script/script.en.v001.md` / `script.annotated.v001.json`(24スパン・約10.2分)
- `episodes/PD-2026-015-theranos/01_research/claims.v001.json` / `manifest.json`

## ★★ R3 — 最重要(存命の有罪確定者)★★
本話は **Elizabeth Holmes(および Ramesh Balwani)= 存命・刑事有罪確定者**。
1. **公開前に専用の権利/法務レビューが必須**(manifest `rights_status=conditional`)。**初稿後、必ずオーナーゲートで停止**し、勝手に公開しない。
2. **表現の厳格さ**:投資家詐欺の **4件は有罪=事実**として述べる。患者関連は **「無罪/not guilty」**、評決不能の3件は **「ミストライアル/評決に至らず」**。
   **絶対に「有罪」と言わない。** 無罪は「合理的疑いを超えて立証されなかった」意味で、**潔白でも「技術が機能した」でもない**(CLM-0010)。
   故意・認識の判断は**陪審/裁判所に帰属**させ、ナレーターの断定にしない。
3. **実在人物の肖像・ディープフェイク禁止**(Holmes/Balwani)。雑誌表紙・法廷などは**象徴的・AI開示**で。数字厳守(Holmes 135ヶ月≒11年3ヶ月、
   Balwani≒155ヶ月「13年近く」)。Walgreens展開は限定的(主にアリゾナ)=全国展開と示唆しない。

## ツール & 実素材
画像=Codex生成＋SDXL。編集=Remotion+FFmpeg。ナレ=ElevenLabs(課金=要承認)。音楽=Suno。実写は `H:\pd-media\assets\stock`＋
`references/README.md`(1点ずつライセンス確認＋クレジット＋rights manifest記録)。重メディア→`H:\pd-media`。

## パイプライン
`pd-scenes` → `pd-generate-assets`(Codex画像＋SDXL＋実写、QC＋権利登録)→ ナレ(課金前に承認)＋音楽＋Remotion
→ `pd-build-edit`(Remotion+FFmpeg)→ **初稿・タイトル/サムネ・そして R3 法務レビューのゲートでSTOP。公開しない。**

## 第15話の固有指定
- 仮タイトル:"When Does a Bold Promise Become a Crime? The Rise and Fall of Theranos"(サムネゲートで3〜5案)。
- ビジュアル一本筋(シリーズ最終話/視点反転):冒頭=一滴の血＋象徴的な雑誌表紙モンタージュ(顔なし)＋$9B→$0グラフ。
  第1幕=2003 Holmes、Edison(一滴で多項目)、$9B・著名取締役会・Walgreens(限定)、名声のハロー。第2幕=2015 WSJ/Carreyrou暴露、
  他社製機器で検査、精度問題、2018 SEC(和解・非自認)・解散。第3幕=US v. Holmes、詐欺=故意の立証、2022/1/3 評決
  (**投資家4件=有罪/患者4件=無罪/3件=評決不能**)、Balwani全12件(患者含む)、Holmes 135ヶ月。第4幕=「fake it till you make it」と
  犯罪の境界=故意＋依拠。結末=シリーズ総括(見る/追う/奪う/言える/DNA/自宅→そして詐欺)＋CTA「one line at a time」。
- 配色:黒/紺/エレクトリックブルー/金。

## 最初のアクション
ロック入力＋handoff＋references/READMEを読み、**画像生成の前に**シーン計画の要約(章→ショット→実素材/生成の別→画面テキスト)＋
**R3表現チェックリスト**をオーナーレビュー用に投稿。その後パイプラインを進め、各ゲート(特にR3法務)で停止。
