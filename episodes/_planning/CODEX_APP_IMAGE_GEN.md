# Codexアプリ（クラウド）で AI画像を事前生成する — 設計書

ローカルでは画像生成できないため、**Codexアプリで先にAI画像をまとめて生成**しておく。
生成した画像を決まった場所に保存すれば、ローカルの取り込みツールが**自動で各場面にはめ込む**（仮の写真と差しかわる）。

## どこを見ればいいか（Codexアプリへ）
各話の **生成リスト** に、画像ごとの「プロンプト・保存ファイル名・保存先」が全部書いてある：
- `episodes/PD-2026-009-timbs/04_scenes/ai_prompts.v001.md`
- `episodes/PD-2026-010-kelo/04_scenes/ai_prompts.v001.md`
- `episodes/PD-2026-011-mahanoy/04_scenes/ai_prompts.v001.md`
- `episodes/PD-2026-012-arbitration/04_scenes/ai_prompts.v001.md`
- `episodes/PD-2026-013-king/04_scenes/ai_prompts.v001.md`
- `episodes/PD-2026-014-lange/04_scenes/ai_prompts.v001.md`
- `episodes/PD-2026-015-theranos/04_scenes/ai_prompts.v001.md`

スタイル・安全ルールは `episodes/_planning/VIDEO_RULES.md`（美しさ最優先・ブランド配色・実在人物の肖像/ディープフェイク禁止・テロップ無し）。

## 保存先（厳守・あとで自動で取り込む）
各画像を **このフォルダ** に、生成リストの **指定ファイル名** で保存する：
```
H:\pd-media\assets\ai\<話名>\<場面ID>.png
  例: H:\pd-media\assets\ai\mahanoy\SPN-0004.png
```
- `<話名>` = timbs / kelo / mahanoy / arbitration / king / lange / theranos
- 1場面に複数枚なら `SPN-0004_02.png`, `SPN-0004_03.png` と連番。
- PNG・1920×1080以上・16:9。フォルダが無ければ作成。

## 取り込み（ローカル側＝あとで実行）
画像が保存されたら、各話で `./.venv/Scripts/python.exe scripts/import_to_remotion.py <話番号> --write` を回すと、
`<場面ID>.png` が自動でその場面に入る（仮の写真より**AI画像が優先**）。`RoughCut-<話名>` で確認できる。

---

## ▼ Codexアプリにそのまま貼るプロンプト（これ一つで完結）

```
あなたはCodexです。リポジトリ prime-documentary（ブランチ claude/vibrant-archimedes-2mmr5h）で作業します。
目的：ドキュメンタリー動画「Prime Documentary」第9〜15話の各場面に使う、美しいAI画像を生成して保存すること。

【まず読む】
- episodes/_planning/VIDEO_RULES.md（動画の全ルール）
- 各話の生成リスト：episodes/<話フォルダ>/04_scenes/ai_prompts.v001.md
  → 画像ごとに「下書きプロンプト・保存ファイル名・保存先」が書いてある。

【生成する画像】
各話の ai_prompts.v001.md にある項目すべて（🎨の場面ぶん）。合計およそ145枚。
1場面に複数欲しいときは連番（例 SPN-0004_02.png）で追加してよい。

【スタイル（全画像共通・厳守）】
cinematic documentary still, ドラマチックで重厚な照明, 配色は「黒・濃紺・エレクトリックブルー・金」,
写実的, 高精細, 浅い被写界深度, 16:9, 美しく映画的。
下書きプロンプトは土台。より良く具体化してよいが、上のスタイルと下の安全ルールは必ず守る。

【安全（厳守）】
画面内の文字なし・透かしなし・ロゴなし。実在人物の肖像やディープフェイクは作らない（象徴的・代表的に表現）。
第15話(theranos)はElizabeth Holmes / Sunny Balwani 本人を描かない。

【保存先（必ずここに・ファイル名はリスト記載のとおり）】
H:\pd-media\assets\ai\<話名>\<場面ID>.png
  ・timbs       → 第9話   : H:\pd-media\assets\ai\timbs\
  ・kelo        → 第10話  : H:\pd-media\assets\ai\kelo\
  ・mahanoy     → 第11話  : H:\pd-media\assets\ai\mahanoy\
  ・arbitration → 第12話  : H:\pd-media\assets\ai\arbitration\
  ・king        → 第13話  : H:\pd-media\assets\ai\king\
  ・lange       → 第14話  : H:\pd-media\assets\ai\lange\
  ・theranos    → 第15話  : H:\pd-media\assets\ai\theranos\
PNG・1920×1080以上・16:9。フォルダが無ければ作成。例: H:\pd-media\assets\ai\mahanoy\SPN-0004.png

【終わったら】
話ごとに「保存枚数・保存先フォルダ」を報告。課金が発生する生成はオーナー承認・予算内で。
（保存後、ローカル側で import_to_remotion.py を回すと各場面へ自動で入るので、生成と保存に専念してOK）
```
