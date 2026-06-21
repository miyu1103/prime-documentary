# ローカルCodex プロンプト — 第9話(timbs) 制作開始（このブロックをそのまま貼る）

あなたはローカルのCodexです。作業フォルダ `C:\Users\aab15\Documents\prime-documentary`（Gitリポジトリ・ブランチ `claude/vibrant-archimedes-2mmr5h`）。
**第9話 PD-2026-009-timbs（Timbs v. Indiana / 民事資産没収）のラフカット制作を開始**してください。AI画像は生成済み(72枚)です。

## まず読む（設計書）
- `episodes/_planning/VIDEO_RULES.md`（動画の全ルール＝美しさ最優先・静止禁止・約4.5秒で切替・30fps・最高画質・権利・中立・広告安全）
- `episodes/PD-2026-009-timbs/04_scenes/asset_map.v001.md`（各場面で ✅既存素材 / 🎨AI画像 / 🔤文字 のどれを使うか）
- `episodes/PD-2026-009-timbs/03_script/script.en.v001.md`（台本＝ナレ原稿）／ `04_scenes/shotlist.v001.json`（秒数・テロップ）
- **台本・注釈はロック。書き換え禁止。** 誤りはSTOPして報告。

## 素材の状態
- **AI画像（生成済・72枚）**：`H:\pd-media\assets\ai\timbs\SPN-XXXX.png`（連番 _02.. 含む）。
- **実写動画＋写真（取得済）**：`build_usable_assets`/`import` で取り込み済み（共有棚234点＋話別95点）。

## 手順
1. **取り込み（AI画像を各場面へ自動配置）**
   `./.venv/Scripts/python.exe scripts/import_to_remotion.py 9 --write`
   - これで `H:\pd-media\assets\ai\timbs\SPN-XXXX.png` が**各場面に優先で入り**（仮の写真と差し替え）、実写動画は動画場面に残り、`remotion/src/data/timbs_roughcut.ts` が再生成される。
   - 出力の「bound to real assets」がほぼ全場面、`coded/cards` が 0 なのを確認。
2. **ラフカット確認**：`cd remotion && npm run studio` → `RoughCut-timbs` を開く（Root.tsx 登録済）。
   - 画像は必ず動く（Ken Burns/parallax）・実写は再生・約4.5秒で切替・テロップ表示を確認。静止やカクつきがあれば原因（fps/連番/差替）を直す。
3. **ナレーション（★課金ゲート）**：`03_script/script.en.v001.md` の `[VO:]` 行から ElevenLabs でナレを生成。
   - **課金が発生するのでオーナー承認を得てから**。冪等・キー管理。masterを作り、`timbs_roughcut.ts` の `narrationSrc` に public 相対パスで設定。
4. **音・字幕**：BGM（Sunoライブラリ・控えめ）を `bgmSrc` に。SFXは要所。字幕/テロップは `gen_captions`/`gen_srt` 系で焼き込み。
5. **書き出し（最高画質）**：`npm run render RoughCut-timbs out/timbs_rough.mp4 --crf=16`（CPU/libx264, 1920×1080, NVENC不可）。
6. **各ステップでコミット**（重メディアは `H:\pd-media`＝Git管理外。`remotion/public` はGit管理外）。

## 止まるゲート（必ず停止して承認を待つ）
- ナレ課金の前 / **初稿(ラフカット)レビュー** / タイトル・サムネ / 公開予約（**6/24以降**から）。

## 厳守
- 実在人物の肖像・ディープフェイクなし。中立。広告安全。VIDEO_RULES に従う。
- 台本・claims は変更しない（左工程はClaude担当）。問題があればSTOPして報告。

## 最初のアクション
手順1を実行し、`RoughCut-timbs` のラフカット（無ナレでも可）をオーナーに見せてレビューを依頼。そこから音・ナレ・書き出しへ。
