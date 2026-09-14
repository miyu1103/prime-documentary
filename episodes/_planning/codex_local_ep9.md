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

## 仕上げ仕様（必須・VIDEO_RULES §10〜13）
- **構成（約12分）＝フック → オープニング → 本編(4幕) → エンディング。**
  - **フック(冒頭 約20〜30秒)＝本編の“盛り上がる瞬間”を約10個、各1〜2秒の速いカットで集めたハイライト集**。
    フック専用に新規制作しない。**本編の最高の映像・決め所のナレ断片/名ゼリフを流用**して編集で組む。音楽＋効果音で煽り、最後にオープニングへ繋ぐ。台本テキストは変えない。
  - **オープニング＝従来エピソードと同じスタイル**（`remotion/src/compositions/Opening.tsx` / 既存EPの定番タイトル演出）。新規に作り直さない。
- **音は4層しっかり**：ナレ＋BGM(Suno・控えめ)＋**効果音(SFX：カット/リビール/数字/テロップ出現にwhoosh/impact/tick・要所のみ)**＋**環境音(ambience：法廷のざわめき/街/夜/オフィス 等を薄く)**。**ダッキング必須**（ナレ中はBGM・環境音を自動で下げ、ナレ最優先・常に明瞭）。
- **意味のあるアニメ**：Ken Burnsだけにしない。**天秤が傾く／地図に軌跡が描かれる／票が並ぶ／年表が進む／図解が組み上がる**等のモーショングラフィック（飾りだけにしない）。画像は必ず動かす。
- **字幕＝ナレと完全同期(forced alignment)＋テロップと被らせない**：字幕は**画面下部の帯**、テロップ(キーワード=`on_screen_text`)は**上/中央**、出典(金ライン)は別位置。**同じ場所に重ねない**（読めない/被るのはNG）。

## 手順
1. **取り込み（AI画像を各場面へ自動配置）**：`./.venv/Scripts/python.exe scripts/import_to_remotion.py 9 --write`
   - `H:\pd-media\assets\ai\timbs\SPN-XXXX.png` が各場面に優先で入り（仮写真と差替）、実写動画は動画場面に残り、`remotion/src/data/timbs_roughcut.ts` 再生成。`coded/cards` が 0 を確認。
2. **ラフカット確認**：`cd remotion && npm run studio` → `RoughCut-timbs`。画像が動く/実写再生/約4.5秒切替/**字幕とテロップが被らない**を確認。カクつき(fps/連番/差替)は直す。
3. **構成を組む**：上の仕上げ仕様どおり **フック(ハイライト約10) → オープニング(従来スタイル) → 本編 → エンディング** に並べる。
4. **ナレーション（★課金ゲート）**：`03_script/script.en.v001.md` の `[VO:]` から ElevenLabs で生成（**課金前に承認**・冪等）。master を `narrationSrc` に設定。
5. **音＆字幕**：BGM(Suno)＋SFX＋環境音を**ダッキング**込みでミックス。字幕は `gen_captions_forced.py` 系で**ナレに語単位同期**して焼き込み（テロップと被らせない）。
6. **書き出し（最高画質）**：`npm run render RoughCut-timbs out/timbs_rough.mp4 --crf=16`（CPU/libx264・1920×1080・NVENC不可）。
7. **各ステップでコミット**（重メディアは `H:\pd-media`、`remotion/public` はGit管理外）。

## サムネ（Codex生成→複数から選択）
- **サムネのキー画像はCodexアプリで生成する**。`04_scenes/thumb_prompts.v001.md` の**ヒーローショット6案を全部生成**し、`H:\pd-media\assets\ai\thumbs\timbs\THUMB-01..06.png` に保存。
- **最高画質・CTR重視**。神ショット/ヒーローショットを複数出し、オーナーが1枚を選ぶ。
- 選んだ1枚を背景に `thumb_prompts.v001.md` のタイトル3案(A/B/C)から選び、既存 `ThumbnailFrame`/`*Thumbnails` で 1280×720 Still 書き出し。詳細は `docs/thumbnail-and-title-system.md`。

## 止まるゲート（必ず停止して承認を待つ）
- ナレ課金の前 / **初稿(ラフカット)レビュー** / タイトル・サムネ / 公開予約（**6/24以降**から）。

## 厳守
- 実在人物の肖像・ディープフェイクなし。中立。広告安全。VIDEO_RULES に従う。
- 台本・claims は変更しない（左工程はClaude担当）。問題があればSTOPして報告。

## 最初のアクション
手順1を実行し、`RoughCut-timbs` のラフカット（無ナレでも可）をオーナーに見せてレビューを依頼。そこから音・ナレ・書き出しへ。
