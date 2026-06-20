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

## ▼ Codexアプリにそのまま貼るプロンプト

> あなたはCodexです。リポジトリ `prime-documentary`（ブランチ `claude/vibrant-archimedes-2mmr5h`）で作業します。
> 目的：**第9〜15話ぶんのAI画像を生成して保存**すること（動画の各場面に使う）。
>
> 手順：
> 1. `episodes/_planning/VIDEO_RULES.md` と `episodes/_planning/CODEX_APP_IMAGE_GEN.md` を読む。
> 2. 各話の `04_scenes/ai_prompts.v001.md`（生成リスト）を開く。各項目に「プロンプト・保存名・保存先」がある。
> 3. 各項目について、**美しい画像を1枚生成**する。プロンプトは記載のものを土台に、より良くしてよい（ただし共通スタイルと安全ルールは厳守）。
>    - 共通スタイル：cinematic documentary still, ドラマチックな照明, 紺×黒＋エレクトリックブルー＋金, 写実的, 高精細, 浅い被写界深度, 16:9。
>    - 安全：**画面の文字なし・透かしなし・ロゴなし・実在人物の肖像/ディープフェイクなし**（象徴的に）。第15話(Theranos)は特に本人を描かない。
> 4. 生成した画像を **`H:\pd-media\assets\ai\<話名>\<場面ID>.png`** に、リスト記載のファイル名で保存する。
> 5. 全話・全項目を生成。1場面に複数欲しい時は `<場面ID>_02.png` で追加。
>
> 注意：課金が発生する生成はオーナーの承認・予算内で。終わったら、話ごとに「何枚保存したか・保存先」を報告して。
