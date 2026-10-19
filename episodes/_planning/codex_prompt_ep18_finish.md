# Codex 仕上げプロンプト — 第18話(2010 Flash Crash / United States v. Sarao) 完成編・FEATURE ~30min

> このブロックを丸ごと Codex スレッドに貼る。第18話を **検証済みの左工程一式**に従って最終動画まで完成させる self-contained プロンプト。
> **正典（この順で優先・勝手に解釈しない）**：① `docs/PD_ONE_PASS_PRODUCTION_SPEC.v1.md`（出荷基準・行1-13）② `episodes/PD-2026-018-flashcrash/08_edit/edit_design.v001.md`（仕上げ設計）③ `03_script/script.en.v001.md`（ナレ本文＝`[VO:]`・**変更禁止**）④ `04_scenes/shotlist.v001.json` / `ai_prompts.v001.md` / `thumb_prompts.v001.md` ⑤ `01_research/claims.v001.json`（事実・**因果ロック**）。
> **本話は R3（存命・有罪答弁者 Navinder Sarao）＝法的高リスク。公開前に専用 法務/権利レビュー必須。**
> **★QCを自分で true と書くのは禁止。** 完成＝`./.venv/Scripts/python.exe scripts/check_final_acceptance.py 18 --json` が **exit 0（全hard PASS）**。実ファイルを機械測定する。

---

あなたは Codex です。branch `claude/vibrant-archimedes-2mmr5h`。着手前に正典①〜⑤＋`CLAUDE.md`(不変項2/6/11/12/13)＋`VIDEO_RULES.md`＋`docs/motion-*`＋`.claude/rules/16` を読む。作業前に `git fetch && git pull --rebase --autostash`。各ステップ後に commit+push。**SSD実体メディア(`H:\pd-media`)と`runs/`はコミットしない。**

## 0. 現在地（左工程＝検証済み・あなたは右工程＝視覚/音/レンダー）
- **脚本＝検証済み**（`validate_episode.py 18` PASS・51 spans・~25.1分ナレ）。`[VO:]`は一字一句変更禁止。
- **claims/sources/shotlist/ai_prompts/thumb_prompts/edit_design＝あり**（検証済み）。
> **★左工程＋持ち越せる素材は完了済＝5ゲートが既にPASS。** `voice_is_master`／`captions_final`／`caption_format`／`image_resolution`／`thumbnail_ready`。**これらは作り直さない（特にナレ＝ElevenLabs再課金禁止）。**
- **AI画像＝完了（78枚・全て3840×2160・4K）**：`remotion/public/flashcrash/S01..S26(.._02/.._03).png`（＋`H:\pd-media\assets\ai\flashcrash`）。`image_resolution` PASS。コンタクトシート＝`09_package/EVIDENCE/contact_sheet.jpg`。R3目視OK（顔/ロゴなし）。
- **★ナレ＝生成済（使うだけ・再生成禁止＝二重課金）**：`H:\pd-media\episodes\PD-2026-018-flashcrash\06_voice\master\vc_master_v001.mp3`（ElevenLabs本番・チャンネル声・~21.8分）＋`06_audio/narration_index.v001.json`（provider=ElevenLabs）。`voice_is_master` PASS。
- **★字幕＝生成済（使うだけ）**：`08_edit/captions.v001.srt` ＋ `remotion/src/data/flashcrash_captions.ts`（`FLASHCRASH_CAPTIONS`・437キュー・≤17cps）。`captions_final`＋`caption_format` PASS。最終尺でVO再タイミング時のみ `scripts/align_flashcrash_captions.py` 再実行。
- **サムネ＝3案＋選定済**：`10_thumbnail/thumbnail.flashcrash_option_A/B/C.v001.png`（1280×720）＋`09_package/thumbnail.selected.v001.png`（A＝「$1 TRILLION / GONE IN 36 MINUTES」）。`thumbnail_ready` PASS。`09_package/EVIDENCE/titles.md`＝CTRタイトル5案。**作り直し不要（必要なら微調整のみ・因果断定しない）。**
- → あなたの仕事＝**残りの右工程**：① bespoke `FlashCrashPremium` 実装（視覚）② **BGM4層ミックス**（最終尺に紐づくのでここで）③ ファクトリ加飾 ④ 独立ゲート全PASS ⑤ 最終レンダー ⑥ パッケージ → STEP H 停止。**未達ゲート＝`bgm_present`・`images_present`・`motion_present`・`render_resolution`/Max品質・`factory_used`・`runtime_band`** を最初のレンダーで満たす。

### ★過去話の失敗を繰り返さない（オーナー実視聴の指摘）
声がSAPI／字幕なし／黒画面／BGMなし／フックがハイライトでない／4部構成でない／画像が荒い／素材未活用／アニメしょぼい／サムネ無い・派手でない——**全て正典 row1-13 で固定済**。最初のレンダーから満たし、**`check_final_acceptance.py 18` が exit 0 になるまで完成としない**。設計書に書いてあっても実レンダーに入っていなければ不合格。

## 2. 絶対に侵さない不変条項（R3・1つでも侵したら即STOP・日本語報告）
1. **★因果ロック（最重要・load-bearing）**：Saraoの**有罪答弁（wire fraud + spoofing）は事実として提示可**。だが暴落については **`contributed to / exacerbated / significantly responsible for the order imbalance` 止まり**。**`caused the crash` / `single-handedly` / `one man broke the market` を事実として出さない**（ナレ・テロップ・サムネ・タイトル全て）。必ず他要因（運用会社の大口売り75,000枚/約41億ドル・HFTの流動性引き上げ・ギリシャ危機の不安）と併置。意図/評価は当局/報告書に帰属（claims CLM-0006/0007/0013）。
2. **実在人物の肖像なし**（Sarao/家族/個別トレーダー）。実写・ディープフェイク不可。後ろ姿・空席・象徴のみ。AI画像に `symbolic reconstruction` ラベル常時＋AI開示（不変項11）。
3. **数値正確**：$1兆・998.5pt・約36分／75,000枚・約41億ドル／$12.8M自認・>$40M主張／$12.9M没収／2009-2014・2016答弁・2020在宅拘禁1年。単位/年/主体を確認（claims・fact_recheck）。
4. **中立**：「彼か、システムか」に肩入れしない。英雄化も悪魔化もしない。実在企業を名指しで悪役化しない（合法な大口売り）。自閉は専門家鑑定に帰属・尊厳をもって。
5. 台本/claims/shotlist 不改変（Read専用）。誤りはSTOP報告。公開・課金はオーナー承認＋冪等キー＋予算チェックなしに実行しない。

## 3. パイプライン（各ステップ後 commit+push）

### STEP A — ナレ＝完了済（何もしない・再生成禁止）
- master `vc_master_v001.mp3`（ElevenLabs本番・~21.8分）＋ `narration_index.v001.json`（provider=ElevenLabs）が既にある。**そのまま使う。ElevenLabsを再度叩かない（二重課金）。** 音声入力は STEP D の4層ミックス master に向ける。

### STEP B — bespoke `FlashCrashPremium.tsx`（edit_design §6・row8/9/10）
- 雛形＝`CarpenterPremium.tsx`/参照`MadoffPremium.tsx`。汎用RoughCut不可。再利用：`Motion.tsx`/`Grain.tsx`/`Bookends.tsx`(`BrandOpening`/`BrandEndcard`)/`SceneArt.tsx`/`SceneShell`/`TwoColumn`/`BigNumber`/`Boundary`。
- **新規小コンポ3つ（SVG/CSS・$0・実在人物を描かない）**：`ValuationCollapse`（市場ライン崩落＋$0.01／S02,S17,S18）・`OrderBook`（買売二列＋見せ玉の壁積み上げ／S10）・`GhostWall`（巨大な壁が迫る→消滅→隙間に本物1注文／S11,S12,S13＝スプーフィングを“完全に理解できる”図解）。
- **4部構成（row10）**：① フック＝本編山場の速いカット集（約20〜30秒・row9＝本編が約束を果たす）→ ② `BrandOpening`＋thesis「Did one man break the market?」→ ③ 本編 act1-6（実VO=narration_indexで再タイミング）→ ④ Ending＋CTA「Subscribe」（最後30秒）→ `BrandEndcard`。**尺＝mid 27〜33分**（`check_final_acceptance` runtime_band）。VO~25分＋幕間/factory b-roll/山場S17の余韻で寄せる（ナレは足さない）。全カット映画的カメラ（静止2秒超なし）。

### STEP C — 字幕＝完了済（使うだけ）
- `08_edit/captions.v001.srt` ＋ `remotion/src/data/flashcrash_captions.ts`（`FLASHCRASH_CAPTIONS`・437キュー・≤17cps・`caption_format` PASS）が既にある。`FlashCrashPremium` で焼き込み（位置分離＝字幕下/テロップ上/出典右下 例`United States v. Sarao`・`CFTC-SEC report, May 6 2010`・AI画像に`symbolic reconstruction`）。**最終尺でVOを再タイミングした場合のみ** `scripts/align_flashcrash_captions.py`（VOICEを最終mix/再タイミング後の音声へ向けて）を再実行。

### STEP D — BGM 4層ミックス（row1・★BGM常時）
- `build_kelo_audio_v001.py` 雛形→`build_flashcrash_audio_v001.py`（VO/BGM/SFX/ambience＋VOサイドチェインダッキング）。**BGM全編常時（無音≤25s）**。章別mood：hook=tension_build→hook／act1-2=explainer_bed→tension_build／act3=tension_build／**act4=tension_build→(S17暴落)低域ドローン＋ほぼ無音の数秒**／act5=somber／ending=outro。決定的SFX：$9B/$1T崩落に sub_drop+low_boom、S17 plunge “ため→開放”。整音 −14 LUFS / TP≤−1。完全ミックスmasterを `FlashCrashPremium` の音声入力に。

### STEP E — ファクトリ三層加飾（row7・edit_design §7）
- `select_factory_assets.py --theme finance_money/tech/legal_court/atmosphere_symbolic` でトーン適合のみ→`remotion/public/flashcrash/factory/`。shotlistの`search_keywords`使用。三層＝背景(薄)＋light/vfx(screen/add)＋texture。意味はコード演出が主役。**実在人物想起素材・実ロゴ・実取引所は不可。** license=allowed のみ・`05_stock/stock_ledger.v001.json`に出典/sha256記録。

### STEP F — 独立ゲート（★書き出し前後・自己申告禁止）
`./.venv/Scripts/python.exe scripts/check_final_acceptance.py 18 --render <final.mp4>` が **RESULT: PASS / exit 0** 必須。hard：voice_is_master／bgm_present／captions_final／caption_format／image_resolution(≥3840)／render_resolution／images_present／motion_present／factory_used／thumbnail_ready(≥3案1280×720)／runtime_band(27-33)。サムネは `thumb_prompts.v001.md` の3案をRemotion `<Still>`で出力＋selected、タイトルはCTR候補から（**因果を断定しない**）。EVIDENCE一式を `09_package/EVIDENCE/` に。

### STEP G — 最終レンダー → パッケージ
- 書き出し＝`FlashCrashPremium`（**CPU/libx264・crf≤16・preset slow・yuv420p・NVENC不可**）→`H:\pd-media\episodes\PD-2026-018-flashcrash\08_edit\renders\final\`。書き出し後 STEP F 再実行→PASS確認。acceptance JSONを保存し**QC数値はその転記**（手書きtrue禁止）。`09_package` 本番化（youtube_meta/chapters/tags/rights_manifest/final_delivery/サムネ選定）。manifest を新revisionで更新。

### STEP H — STOP（オーナー承認＋R3法務レビュー）
- 必ずSTOP。`OWNER_REVIEW_REQUEST` 更新。承認待ち：内容(APR-0001)／初号レビュー／タイトル・サムネ／ナレ公開可否／**専用 法務/権利レビュー(R3・不可侵)**／公開・スケジュール。**法務レビュー記録(exact hash)なしに `publish_approved` 不可。** アップロード/公開/スケジュールは絶対に実行しない。

## 4. 最初のアクション
正典①〜⑤を読み、**実装前に**「STEP A〜H計画＋4部構成の尺タイムライン（合計27〜33分の数値根拠）＋因果ロック/中立/R3(肖像なし・法務)の遵守方針＋STEP F でPASSを取る計画」を**日本語の短い要約**で投稿。その後ノンストップで STEP A→G、**STEP H のオーナー承認＋R3法務レビューでのみ停止**。
