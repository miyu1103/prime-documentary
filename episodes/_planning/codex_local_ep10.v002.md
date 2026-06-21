# ローカルCodex プロンプト — 第10話(kelo) ラフカット〜仕上げ【確定版 v002 / このブロックをそのまま貼る】

> 確定状況（2026-06-22 時点で Claude 側が確認済み）
> - 第10話 `PD-2026-010-kelo`（Kelo v. New London / 収用権）は **state=script_verified**・`validate_episode 10` **PASS**（10 claims / 28 spans / QC pass）。
> - **本編のSPN別AI画像は生成済み**（`H:\pd-media\assets\ai\kelo\` に複数バリアント。AI画像18スパン＋実写動画ほか10スパン）。
> - **サムネのヒーローショット6案も生成済み前提**（`H:\pd-media\assets\ai\thumbs\kelo\THUMB-01..06.png`）。このパスでは生成せず、選定1枚にタイトルを重ねて書き出すだけ。
> - **ストック取り込み済みで `import_to_remotion.py 10` は全28ショットを実素材にbind＝カード0**（今ある素材だけで隙間なく組める。共有素材棚=factoryのDL完了を待つ必要はない）。
> - **ナレーション(ElevenLabs)は課金を気にせず実行してよい**（都度の課金承認待ちは不要）。
> - 仕上げ設計は `08_edit/edit_design.v001.md`（4部構成＋全28ショットの意味あるアニメ＋字幕/テロップ/出典レイアウト＋§6 Premium実装ガイド）、音声設計は `06_audio/audio_cue_sheet.v001.md`（4層＋ダッキング）に確定済み。**この2本に従う**。
> - **アニメは Premium級コード演出で作る**（`KeloPremium.tsx` を新規作成。SceneArt/Motion 等のコード部品を使用）。汎用RoughCutでは“意味あるアニメ”は出ない。**今DL中の共有素材棚(factory: vfx/light/particle/loops)はこのEP10では使わない**（コード演出で代替・将来用）。

あなたはローカルのCodexです。作業フォルダ `C:\Users\aab15\Documents\prime-documentary`（ブランチ `claude/vibrant-archimedes-2mmr5h`）。
**第10話 PD-2026-010-kelo のラフカット制作〜仕上げ**を進めてください。slug = `kelo`。

---

## ★最重要（必ず先に）
- **Codexは最初からフルアクセス（全権限・自動承認）で起動。** 都度の許可待ちで止まらない運用にする。
- **動画は必ずこの4部構成**（10話以降は厳守）：
  1. **フック**（冒頭 約20〜30秒）＝本編の“盛り上がる瞬間”を約10個、各1〜2秒の速いカットで集めたハイライト集。**フック専用の新規制作はしない**（本編の最高映像・決め所のナレ断片/名ゼリフを流用して編集で組む）。音楽＋効果音で煽り、最後にオープニングへ繋ぐ。
  2. **オープニング**＝従来エピソードと同じスタイル（`remotion/src/compositions/Opening.tsx`／既存EPの定番タイトル）。作り直さない。
  3. **本編**＝台本の各幕。
  4. **エンディング**＝結末＋次回予告/CTA＋フォロー誘導。
- **先に4部の骨組み（空シーケンス）を置いてから中身を埋める。最後に「フック→オープニング→本編→エンディングの4部になっているか」を必ず確認**してから書き出す。

## まず読む（台本・claims・注釈はロック＝変更禁止。誤りはSTOPして報告）
- **`episodes/PD-2026-010-kelo/08_edit/edit_design.v001.md`（仕上げ設計＝4部構成・全ショットのモーション・字幕/テロップ/出典レイアウト）** ←最重要
- **`episodes/PD-2026-010-kelo/06_audio/audio_cue_sheet.v001.md`（音声設計＝4層＋ダッキング）**
- `episodes/_planning/VIDEO_RULES.md`（§10〜13＝構成・音・アニメ・字幕の全ルール）
- `episodes/PD-2026-010-kelo/03_script/script.en.v001.md`（`[VO:]` がナレ本文）
- `episodes/PD-2026-010-kelo/04_scenes/shotlist.v001.json` ／ `04_scenes/asset_map.v001.md` ／ `04_scenes/ai_prompts.v001.md`
- `docs/thumbnail-and-title-system.md`（サムネ/タイトル規則）

## 仕上げ仕様（必須・VIDEO_RULES §10〜13）
- **構成（約10.5分）＝フック → オープニング → 本編(4幕) → エンディング。**
- **音は4層**：ナレ＋BGM(Suno・控えめ)＋効果音(SFX：カット/リビール/数字/テロップ出現)＋環境音(ambience：法廷ざわめき/街/夜/オフィス等を薄く)。**ダッキング必須**（ナレ中はBGM・環境音を下げ、ナレ最優先で常に明瞭）。
- **意味のあるアニメ**：Ken Burnsだけにしない。天秤が傾く／地図に軌跡／票が並ぶ／年表が進む／図解が組み上がる等。画像は必ず動かす。
- **字幕＝ナレと完全同期(forced alignment)＋テロップと被らせない**：字幕は画面下部の帯、テロップ(キーワード=on_screen_text)は上/中央、出典(金ライン)は別位置。同じ場所に重ねない。

---

## 手順と【保存先】

### 1. 素材ステージング（AI画像/実写を public へ）
```
./.venv/Scripts/python.exe scripts/import_to_remotion.py 10 --write
```
- AI画像（`H:\pd-media\assets\ai\kelo\SPN-XXXX*.png`）と実写が `remotion/public/kelo/` にコピーされる（**KeloPremium がここを参照**）。
- 副産物の `remotion/src/data/kelo_roughcut.ts` は**下見/素材一覧用**（最終はこれではなくPremiumコンポ）。`coded/cards=0` を確認。

### 2. ★KeloPremium を作る（Premium級コード演出＝最重要）
- **汎用RoughCutでは §2 の“意味あるアニメ”は出ない。** `remotion/src/compositions/KeloPremium.tsx` を新規作成し、`CarpenterPremium.tsx`/`RileyPremium.tsx` を雛形にする。
- 既存部品を再利用：`SceneArt`（小槌/天秤/年表/USマップ/書類＋印章）, `Motion`(`MovingStage`/`Particles`/`LightSweep`/`Vignette`), `Grain`, `Bookends`(`BrandOpening`/`BrandEndcard`), Carpenterの `Vote`(5–4)/`MapGrid`/`TwoColumn`/`Doors`/`BigNumber`。
- **割り当ては `08_edit/edit_design.v001.md` §6 の表に従う**（SPN別に画像Ken Burns or コード演出を指定済み）。
- `Root.tsx` に `KeloPremium`（`id="KeloPremium"`）を登録（ハイフンのみ）。

### 3. プレビュー確認
```
cd remotion && npm run studio   # → KeloPremium
```
- §2の各演出（山場SPN-0014の年表→5–4→印章、SPN-0019のUSマップ40+ 等）が出る／4部構成／**字幕とテロップが被らない**を確認。
- **【STOPゲート①】無ナレの `KeloPremium` をオーナーに提示してレビュー依頼**（先へ進む前に1度）。

### 4. ナレーション（課金は気にせず実行してよい）
- `script.en.v001.md` の `[VO:]` を ElevenLabs で生成。**課金承認待ちは不要**（止まらず進める）。
- **保存先**：
  - ドラフト → `H:\pd-media\episodes\PD-2026-010-kelo\06_voice\draft\VC-XXXX.mp3`(+ `.json`)
  - マスター → `H:\pd-media\episodes\PD-2026-010-kelo\06_voice\master\VC-XXXX.mp3`
  - インデックス/計画 → `episodes/PD-2026-010-kelo/06_audio\narration_index.v001.json` ／ `voice_plan.v001.json`（git管理）
  - `kelo_roughcut.ts` の `narrationSrc` にマスター連結を反映。

### 5. 音＆字幕
- BGM(Suno)＋SFX＋環境音を**ダッキング**込みでミックス。
- 字幕は forced alignment（`scripts/gen_captions_forced.py` 系）で**ナレに語単位同期**して焼き込み（テロップと被らせない）。
- **保存先**：
  - 字幕 → `episodes/PD-2026-010-kelo/08_edit\captions.v001.srt`(+ `.json`)（git管理）
  - 音源（BGM/SFX/環境音の実体）→ `H:\pd-media\library\...`（既存の共有ライブラリを参照）＋話別が要るなら `H:\pd-media\episodes\PD-2026-010-kelo\07_audio\`
  - ナレタイムライン → `episodes/PD-2026-010-kelo/08_edit\narration_timeline.v001.json`

### 6. サムネ（★ヒーロー6案は生成済み前提。ここでは選定＋タイトル合成のみ）
- **生成済み素材**：`H:\pd-media\assets\ai\thumbs\kelo\THUMB-01.png` 〜 `THUMB-06.png`（無ければオーナーに連絡）。
- オーナーが1枚選択 → `thumb_prompts.v001.md` の**タイトル3案(A/B/C)**から選び、既存 `ThumbnailFrame`/`*Thumbnails` で **1280×720** Still 書き出し（**実在人物の肖像なし・広告安全・ブランド配色**）。
- **保存先（タイトル乗せ完成サムネ）**：`episodes/PD-2026-010-kelo/10_thumbnail\kelo_thumbnail_optNN.v001.png`（候補）→ 採用1枚。候補メタは `09_package/title_thumbnail_candidates.v001.json`。
- **【STOPゲート＝タイトル・サムネ承認】**。A/Bテストして勝者に差し替え。

### 7. 書き出し（最終レンダー）
```
cd remotion && npm run render KeloPremium out/kelo_premium.mp4 --crf=16
```
- **CPU/libx264・1920×1080・NVENC不可**（品質最優先）。
- **保存先（最終）**：`H:\pd-media\episodes\PD-2026-010-kelo\08_edit\kelo_premium_v001.mp4`（既存EPと同じ命名規約）。レビュー用QCは `episodes/PD-2026-010-kelo/08_edit\renders\rough.v001.qc.json`。

### 8. コミット
各ステップでコミット。**重メディア（`H:\pd-media`）と `remotion/public` はGit管理外**。コミットするのは台本/設計/`*_roughcut.ts`/captions/manifest等の軽量成果物のみ。

---

## 止まるゲート（承認境界・勝手に越えない）
- **①無ナレ初稿レビュー** ／ **②タイトル・サムネ承認** ／ **③公開予約（6/24以降）**。
- ※ナレーション課金ゲートは今回**無効**（課金を気にせず実行してよい）。

## この話の厳守事項
- **中立**（公共の用 vs 個人の家のどちらにも寄らない）。
- **実在人物・判事の肖像なし**（象徴的に）。ディープフェイクなし。
- 台本・claims・注釈は**変更禁止**。VIDEO_RULES 準拠。

## 最初のアクション
**手順1（`import_to_remotion.py 10 --write` で素材を public/kelo へ）→ 手順2（`KeloPremium.tsx` を作成し `edit_design §6` の割り当てで演出を実装）** → `npm run studio` で `KeloPremium` を無ナレ確認 → オーナーに提示して【STOPゲート①】のレビュー依頼。
