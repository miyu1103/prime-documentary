# 第18話 flashcrash 仕上げ設計書（Edit / Finish Design） v001 — FEATURE (~30 min)

対象: `PD-2026-018-flashcrash`（2010 Flash Crash / United States v. Sarao）。Codex がこの設計に従ってラフカット→仕上げを行う。
入力: `04_scenes/shotlist.v001.json`（26ヒーローショット）, `03_script/script.en.v001.md`（`[VO:]`=ナレ本文・**変更禁止**）, `04_scenes/ai_prompts.v001.md`（生成済み4K画像 `H:\pd-media\assets\ai\flashcrash\S**.png` / `remotion/public/flashcrash/`）, `04_scenes/thumb_prompts.v001.md`。

> **★出荷基準の正典＝`docs/PD_ONE_PASS_PRODUCTION_SPEC.v1.md`（ONE-PASS PRODUCTION SPEC v1）。** BGM/声/字幕/改行/画質≥3840/Max品質crf16/素材活用/アニメ/フック/4部構成/サムネ/タイトルCTR の全失敗モードが「仕様＋ゲート」で固定。**最初のレンダーから同表を満たし、`./.venv/Scripts/python.exe scripts/check_final_acceptance.py 18 --json` が exit 0（全hard PASS）になるまで完成としない。** 自己申告QC（true手書き）禁止。
>
> **⚠ R3 / 法的高リスク（存命・有罪答弁者 Sarao）。公開前に専用 法務/権利レビュー必須。** 実在人物の肖像・実写・ディープフェイク不可（象徴のみ）。**因果は `contributed / exacerbated / significantly responsible` 止まり。`caused / single-handedly / one man broke the market` と断定しない**（claims CLM-0006/0013）。有罪答弁(wire fraud + spoofing)は事実。実在企業（売り注文を出した運用会社等）を名指しで悪役化しない（合法な大口売りとして中立）。

---

## 1. 完成尺と4部構成（FEATURE・mid profile）
- **尺バンド＝mid（27〜33分）**。`manifest.target_duration_minutes=30`。**実尺は `check_final_acceptance.py` の runtime_band（profile）でゲート。**
- 4部（正典 row10）：**① フック（本編ハイライトの速いカット集・約20〜30秒・row9＝最後に作る/本編が約束を果たす）→ ② オープニング（`BrandOpening`＋thesis「Did one man break the market?」）→ ③ 本編 act1〜act6（台本順）→ ④ エンディング（payoff＋CTA「Subscribe」＝最後30秒にCTA）→ `BrandEndcard`**。
- **尺の作り方**：本編VO（ElevenLabs生成後に確定）＋幕間“ひと呼吸”＋山場（S17 plunge）の余韻＋主要グラフの間。VOが短ければ held/factory b-roll で27〜33分に収める（ナレは足さない）。**Codexは shotlist推定でなく実VO(narration_index)で再タイミング**。

## 2. モーション設計（静止画ゼロ・row8）
- **全カットに映画的カメラ**（寄り/引き/パララックス＋spring/ease・リニア禁止）。静止2秒超なし。
- **bespokeコード演出（“意味あるアニメ”・row8）**＝本話の主役グラフィック：
  - **`ValuationCollapse`**：市場ラインが崩落→一兆ドルが消える（S02/S17）。`$0.01`カウンタ（S18）。
  - **`OrderBook`**：買い/売りの二列の光。見せ玉の壁が積み上がる（S10）。
  - **`GhostWall`**：巨大な半透明の壁が迫る→一瞬で消滅→隙間に本物の1注文（S11/S12/S13）＝スプーフィングの核を“完全に理解できる”図解に。
  - 補助：`HighScore`カウンタ（S09）、コードスクロール（S08）。
- AI画像（S03/05/06/07/14/15/19/20/21/23/24）は `SceneShell`相当（多画像Ken Burns＋光＋粒子＋`ReconLabel`）。長尺スパンは約4.5秒ごとに別カット/バリアント切替。

## 3. テロップ／字幕／出典（被らせない・row4）
- **字幕**：強制アライン・ズレ≤120ms・台本と一字一句一致・**≤2行/≤42字/1.0〜6.0秒/≤17cps・単語の途中で切らない**（row3/row4）。下部安全帯。
- テロップ(on_screen_text)=上/中央。出典(金ライン 例 `United States v. Sarao` / `CFTC-SEC report, May 6 2010`)=右下固定。AI画像に `symbolic reconstruction` ラベル常時。3者を位置で分離。

## 4. 品質ゲート（書き出し前後・正典準拠）
**`scripts/check_final_acceptance.py 18 --render <final.mp4>` が RESULT: PASS（exit 0）必須。** 主要hard：
- voice_is_master（ElevenLabs本番声）／bgm_present（BGM常時・無音≤25s）／loudness（−16〜−12 LUFS）
- captions_final（≥95%網羅）／caption_format（≤2行/≤42字/1-6s/≤17cps）
- image_resolution（**全ヒーロー画像 長辺≥3840**）／render_resolution（1920×1080）／render Max品質（libx264 crf≤16 preset slow・NVENC不可）
- images_present（黒なし）／motion_present（静止/スライドショー検出）
- factory_used（factory非空＋参照＋密度）／thumbnail_ready（≥3案1280×720＋selected）
- runtime_band（mid 27-33分）
EVIDENCE（`09_package/EVIDENCE/`）：contact_sheet・motion・hook.mp4・alignment_report・thumbs(≥3)・titles.md・mix_report。

## 5. この話の編集ポリシー（★R3・最重要）
- **中立**：「彼か、システムか」に肩入れしない。検察/規制当局の評価・他要因（運用会社の大口売り・HFTの引き・ギリシャ不安）を**公平に併置**。崩落の過剰演出で“単独犯”に寄せない。
- **因果を断定しない**：ナレ/テロップ/サムネで `caused / one man broke the market` を**事実として出さない**。疑問形・`contributed`に留める。意図/評価は当局/報告書に帰属。
- **実在人物の肖像なし**（Sarao/家族/個別トレーダー）。象徴・後ろ姿・空席のみ。自閉は専門家鑑定に帰属し尊厳をもって（見世物にしない）。
- **数値**：$1兆・998.5pt・約36分・75,000枚/約41億ドル・$12.8M自認/>$40M主張・$12.9M没収・2009-2014・2016答弁・2020在宅拘禁1年＝単位/年/主体を確認（claims・fact_recheckで再確認）。
- 台本/claims/shotlist 不改変（Read専用）。

## 6. 実装方針（bespoke `FlashCrashPremium.tsx`）
- 雛形＝`CarpenterPremium.tsx`／参照＝`MadoffPremium.tsx`。汎用RoughCutは使わない（row8の意味あるアニメが出ない）。
- 再利用：`Motion.tsx`(`MovingStage`/`Particles`/`LightSweep`/`Vignette`/`CameraRig`)、`Grain.tsx`、`Bookends.tsx`(`BrandOpening`/`BrandEndcard`)、`SceneArt.tsx`、`CarpenterPremium`の`SceneShell`/`TwoColumn`/`BigNumber`/`Boundary`。
- **新規小コンポ3つ**（SVG/CSS・$0・実在人物を描かない）：`ValuationCollapse`／`OrderBook`／`GhostWall`（§2）。
- `Root.tsx` に `FlashCrashPremium`（`id="FlashCrashPremium"`）登録・`durationInFrames` を実VO＋間に合わせる。音声入力は4層ミックス master（VO＋BGM＋SFX＋amb・ダッキング）に向ける。

## 7. ファクトリ三層加飾（row7・テーマ＝finance/tech/legal/atmosphere）
- `scripts/select_factory_assets.py --theme <…>` で**トーン適合のみ**抽出→`remotion/public/flashcrash/factory/`。三層＝背景プレート(薄)＋light/vfx/particle(screen/add)＋texture(overlay)。**意味はコード演出が主役・ファクトリは加飾**（1カット1〜2レイヤ）。
- shotlist の `search_keywords` を使用：finance_money(stock_chart_crashing_red, stock_market_screen)／tech(server room, data center, code)／legal_court(courtroom_interior)／atmosphere_symbolic(empty_road, dust_motes, looping_gradient_navy)。山場 S17 plunge は `god_rays`+`smoke_on_black`+赤系で“ため→開放”。license=allowed のみ・出典/sha256を `05_stock/stock_ledger.v001.json` に記録。**実在人物想起素材・実ロゴ・実取引所は不可（R3）。**

---

## 完成定義（書き出し前に全✓・＋公開前法務レビュー）
- [ ] `check_final_acceptance.py 18` exit 0（全hard・正典 row1-13）＋EVIDENCE一式。
- [ ] 4部構成／フック=本編ハイライト/全カット動く/画像長辺≥3840/Max品質crf≤16/BGM常時/字幕同期・改行OK/factory三層/サムネ≥3案/タイトルCTR。
- [ ] **R3表現**：因果は contributed 止まり・断定しない／実在人物の肖像なし／中立／数値正確。
- [ ] **公開前 専用 法務/権利レビュー（exact hash）** ＝最終・不可侵ゲート。記録なしに `publish_approved` 不可。
