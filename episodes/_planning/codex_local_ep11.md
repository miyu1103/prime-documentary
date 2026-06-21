# ローカルCodex プロンプト — 第11話(mahanoy) 制作開始（このブロックをそのまま貼る）

あなたはローカルのCodexです。作業フォルダ `C:\Users\aab15\Documents\prime-documentary`（ブランチ `claude/vibrant-archimedes-2mmr5h`）。
**第11話 PD-2026-011-mahanoy（Mahanoy v. B.L. / 校外SNS言論）のラフカット制作**を開始してください。

## 前提
- **AI画像が `H:\pd-media\assets\ai\mahanoy\SPN-XXXX.png` に生成済み**であること（未生成なら先に `04_scenes/ai_prompts.v001.md` のプロンプトでCodexアプリ生成→指定名で保存）。
- 実写動画＋写真は取り込み済み（共有棚＋話別）。

## まず読む
- `episodes/_planning/VIDEO_RULES.md`（§10〜13＝構成・音・アニメ・字幕も含む全ルール）
- `episodes/PD-2026-011-mahanoy/04_scenes/asset_map.v001.md` ／ `03_script/script.en.v001.md` ／ `04_scenes/shotlist.v001.json`
- **台本・注釈はロック・変更禁止。** 誤りはSTOPして報告。

## 仕上げ仕様（必須・VIDEO_RULES §10〜13）
- **構成（約12分）＝フック → オープニング → 本編(4幕) → エンディング。**
  - **フック(冒頭 約20〜30秒)＝本編の“盛り上がる瞬間”を約10個、各1〜2秒の速いカットで集めたハイライト集**。フック専用に新規制作しない（本編の最高の映像・決め所のナレ断片/名ゼリフを流用して編集で組む）。音楽＋効果音で煽り、最後にオープニングへ繋ぐ。台本テキストは変えない。
  - **オープニング＝従来エピソードと同じスタイル**（`remotion/src/compositions/Opening.tsx`／既存EPの定番タイトル演出）。新規に作り直さない。
- **音は4層しっかり**：ナレ＋BGM(Suno・控えめ)＋効果音(SFX：カット/リビール/数字/テロップ出現)＋環境音(ambience：法廷ざわめき/街/夜/オフィス 等を薄く)。**ダッキング必須**（ナレ中はBGM・環境音を下げ、ナレ最優先で常に明瞭）。
- **意味のあるアニメ**：Ken Burnsだけにしない。天秤が傾く／地図に軌跡が描かれる／票が並ぶ／年表が進む／図解が組み上がる 等。画像は必ず動かす。
- **字幕＝ナレと完全同期(forced alignment)＋テロップと被らせない**：字幕は画面下部の帯、テロップ(キーワード=on_screen_text)は上/中央、出典(金ライン)は別位置。同じ場所に重ねない（読めない/被るのはNG）。

## 手順
1. **取り込み**：`./.venv/Scripts/python.exe scripts/import_to_remotion.py 11 --write`
   - AI画像が各場面へ優先で入り（仮写真と差替）、実写動画は動画場面に残り、`remotion/src/data/mahanoy_roughcut.ts` 再生成。`coded/cards` が 0 を確認。
2. **ラフカット確認**：`cd remotion && npm run studio` → `RoughCut-mahanoy`。画像が動く/実写再生/約4.5秒切替/**字幕とテロップが被らない**を確認。
3. **構成を組む**：フック(ハイライト約10)→オープニング(従来スタイル)→本編→エンディング。
4. **ナレ（★課金ゲート）**：`script.en.v001.md` の `[VO:]` から ElevenLabs（**課金前に承認**）→ master → `narrationSrc`。
5. **音＆字幕**：BGM(Suno)＋SFX＋環境音を**ダッキング**込みでミックス。字幕は `gen_captions_forced.py` 系で**ナレに語単位同期**して焼き込み（テロップと被らせない）。
6. **書き出し**：`npm run render RoughCut-mahanoy out/mahanoy_rough.mp4 --crf=16`（CPU/libx264・1920×1080・NVENC不可）。
7. **各ステップでコミット**（重メディアは `H:\pd-media`、`remotion/public` はGit管理外）。

## 止まるゲート
- ナレ課金前 ／ 初稿レビュー ／ タイトル・サムネ ／ 公開予約（**6/24以降**）。

## この話の厳守事項
- ★広告安全：投稿の罵倒語はナレで読まない（描写のみ）・画面テキストは伏字。
- 本人(Brandi Levy)の肖像なし。中立（学校 vs 生徒のどちらにも寄らない）。
- 実在人物の肖像・ディープフェイクなし。VIDEO_RULES 準拠。台本・claims は変更しない。

## 最初のアクション
手順1を実行し、`RoughCut-mahanoy` のラフカット（無ナレ可）をオーナーに見せてレビュー依頼。
