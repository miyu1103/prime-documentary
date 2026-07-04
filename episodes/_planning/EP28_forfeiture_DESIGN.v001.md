# EP28 制作設計書 — "They Took the House" (民事没収)

**Episode ID:** `PD-2026-028-forfeiture`  ·  **slug:** `forfeiture`
**Series arc:** *They Did Nothing Wrong*（普通の人 vs システムの暴走）1/3
**Duration profile:** standard — target **12:00 (720s)**, band **690–750s** · **AS-BUILT (2026-07-05): 706.6s = 11.78min（band内）**
**R-rating:** **R2**（実在・存命人物＋実際の刑事事件。fact_recheck と公開前法務ゲート必須）
**Binding spec:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（本設計書は§A表 rows 1–16 のインスタンス）

---

## 0. ログライン / なぜ勝てるか

> 息子がわずか **$40 分の麻薬** を売った。その罰として市が奪おうとしたのは——**両親の家そのもの**だった。誰も有罪になっていないのに。

- **データ勝ち筋との一致**：`[[pd-analytics-findings]]` の「これは他人事じゃない × 権力(警察・政府)の暴走 × 家/財産」に完全一致。既出で刺さった "あなたの家" テーマ（Kelo/Kyllo）の**実話版**。政府が悪役＝名誉毀損リスク低め。
- **感情設計**：怒り（理不尽）→ 逆転（勝訴・改革）。拡散する2大感情を両方積む。
- **入口ショート（別制作）**：`Your Kid Sells $40 of Drugs — The City Takes Your House? #Shorts`

> **オーナー厳命(2026-07-04)：見ごたえ最優先。「普通の情報提供」は禁止。** 事実の羅列・平板な解説にしない。一流のドキュメンタリー作家が書く**物語**として、緊張・謎・人物・転換・ペイオフで引っ張る（row15/16 を満たさない台本は不合格）。**台本は最低3回レビューする（§10a）**。

---

## ✅ 制作ステータス（AS-BUILT 2026-07-05）

左工程＋ナレ音声＋字幕まで完成・機械ゲート緑。**残るは画像→組立のみ**。
- **事実**: `fact_recheck.v001`（多出典・GUARDRAILS）で確定（★は逐語ロック済）。
- **台本**: `script.annotated.v001.json`（正典スキーマ）＝確定ナレ源・**2,054語**（3パス済）。
- **ナレ音声**: ElevenLabs master **686.1s**（`voice_is_master` PASS）。
- **字幕**: 強制アライン `captions.final.v001.srt`（一致100%／format／カバー **全PASS**）。
- **尺**: 総尺 **706.6s = 11.8分**（band 690–750 内）。式＝hook8＋opening3.5＋ナレ＋endcard9。
- **カット割**: `shotlist.v001.json`（**257カット**・平均2.8s・treatmentローテ・密度≥23）。
- **残**: 画像40枚(Codex・`ai_prompts.v001`)→`remotion/public/forfeiture`ステージ→`data/forfeiture_film.json`→Remotion組立→`check_final_acceptance` exit0→MotionSample目視。

---

## 1. 事実の骨子（**FACTS LOCKED**: `fact_recheck.v001` で多出典確定・GUARDRAILS拘束）

実話ベース：**Sourovelis v. City of Philadelphia**（フィラデルフィアの民事没収）。

- ★ 2014年、Christos & Markela Sourovelis 夫妻の息子が、自宅付近で少量の麻薬（★$40相当）を売り逮捕。
- ★ 市は **民事没収（civil forfeiture）** で一家の家を没収しようとし、一家は一時**自宅から締め出された**。
- ★ フィラデルフィアは全米屈指の没収マシンを運用（★年間規模・件数、押収金を検察/警察が保持する**利益相反**、令状フロア "Courtroom 478" で弁護人なしの所有者）。
- ★ 2014年8月、**Institute for Justice** が連邦**集団訴訟**を提起。
- ★ 2018年、**同意判決（consent decree）**で市は濫用的運用の終了と、被害者補償の**★約$300万基金**設置に合意。一家は家を守った。

> **不変項1/10/13：** 上記★はすべて公開記録（IJ／連邦地裁／全国報道）から**逐語ロック**するまで台本に本文として書かない。ドラマは事実の上に立てる。事実を創作しない。存命人物・未成年の逮捕に触れるため、**共感の焦点は両親と制度**に置き、息子の件は事実を最小限・中立に扱う。

---

## 2. 4部構成 — 秒割タイムライン（**AS-BUILT: fps=30（CaseFilm／BRAND.video.fps）／全長 706.6s** ／ 数値は定数）

> **AS-BUILT SYNC (2026-07-05)** — 真実源は `episodes/PD-2026-028-forfeiture/03_script/script.annotated.v001.json`（この .md は当初ドラフト）。実測: ナレ **686.1s**・**33 spans / 2,054語**・**28 の on_screen_text**（キネティックビート）・字幕 **348キュー / 最悪22cps**・factory **96本ステージ済**（6テーマ分散）・総尺 **706.6s**（hook8+OP3.5+686.1+ED9）。CaseFilmは **30fps**（旧記載の fps=60 は誤り。fps=60 はルートCLAUDE.mdのオープニング実演用で、長尺CaseFilmエンジンには適用されない）。組立=`CaseFilm-forfeiture`（プレミアム・エンジン＋別スレのAmbientMotion/派手Bookendsで統一予定）→ ship-gate 受領書緑まで（`docs/PD_SHIP_GATE.md`）。

| Part | 区間(s) | 尺 | 役割 | ナレ語数(≈173wpm) |
|---|---|---|---|---|
| **HOOK** | 0.0–8.0 | 8.0s | フラッシュフォワード：締め出された玄関前の一家。開く問い。**最後に書く** | ~23w |
| **BrandOpening** | 8.0–11.5 | 3.5s (`OPENING_SEC`) | 金の `BrandOpening`（フックの後）。シリーズ名+タイトル | 0（音楽のみ） |
| **ACT I 家** | 11.5–~180 | ~2.8min | 普通の一家／$40の逮捕／最初のノック | ~480w |
| **ACT II 機械** | ~180–~360 | ~3.0min | 民事没収の仕組み。"家が被告"(in rem)。Courtroom 478。利益相反 | ~520w |
| **ACT III 抵抗** | ~360–~560 | ~3.3min | IJの集団訴訟／他の被害者（＝これは他人事じゃない拡張）／規模 | ~575w |
| **ACT IV 決着+ペイオフ** | ~560–711 | ~2.5min | 2018同意判決／改革／**フック回収**（家は守られた）／稼いだ Like への CTA | ~430w |
| **BrandEndcard** | 711–720 | 9.0s (`ENDCARD_SEC`) | `BrandEndcard`（CTA/cadence）。末尾 | 0 |

**ナレ合計 ≈ 2,030w** → **AS-BUILT 2,054w**（ElevenLabsマスター実測 **686.1s**）。当初 kyllo=1,775w基準からやや厚め。**band 内へ調整済**（annotated を +約300語＝出典内で拡張し総尺706.6sで確定・声/字幕ゲート全PASS）。
**リテンション（row16）**：フックの謎（家は奪われたのか？）を**ラストまで開いたまま保持**。オープンループ「だが、そうはならなかった…」を ACT III 末で。**再フックを ~2:30 ごと**（ACT境界＝新しい問い/転換）。20秒を超える平坦説明を作らない。

---

## 3. HOOK（0:00–0:08）— 最後に書く・ペイオフ検証必須（row 9）

- **画**：4カット×~2.0s のパンチ編集（本編の最強ビート先出し）。
  1) 施錠された自宅玄関に貼られた告知（書類マクロ、寄り）
  2) 回転する赤青のパトランプが夜の連棟住宅を舐める（フッテージ、暗め+ネイビー）
  3) 「$40」の数字が巨大キネティックタイポで叩き込まれる（モーショングラフィックス）
  4) 玄関前に立ちすくむ家族の姿（**匿名の代表的人物**・実在の誰かに似せない）
- **フック文（★暫定・確定は台本ロック時）**：`He sold forty dollars of drugs. So the city tried to take his parents' house.`
- **ペイオフ**：ACT IV で「家は守られた／制度が変わった」を必ず提示（promise-payoff QC = true）。

---

## 4. FILM BIBLE（Academy 級・row 15/16）ビート

- **コールドオープンの問い**：有罪ですらない家族が、なぜ家を失いかけたのか。
- **三幕の上げ**：個の理不尽（ACT I）→ 仕組みの正体（ACT II：これは設計された制度だ）→ 規模と反撃（ACT III：あなたにも起こりうる）→ 逆転と代償（ACT IV）。
- **人間の縦糸**：普通の親。「悪いのは誰か」を問い続ける。
- **モチーフ**：**鍵・ドア・敷居**（家＝安全の境界が破られる）。数字（$40 ↔ 家の価値 ↔ ★$300万基金）。
- **ナレの節度**：説明しすぎない。画に語らせる。断定は事実のみ。
- **テーマ**：「処罰の前に、証明を。」— 有罪認定なき財産剥奪への問い。

---

## 5. ビジュアル/アニメ・システム（row 8・`MotionSample.tsx` 準拠＝**紙芝居禁止**）

**土台テンプレ**：`remotion/src/compositions/CaseFilm.tsx`（`data/forfeiture_film.json` 駆動）。承認済み `MotionSample` の作り。

- **カット**：平均 **2.5–3.0s**（速いテンポ・常に画が変化）。ハードカット裸禁止＝**0.35s クロスディゾルブ**でシーケンスを重ねる（1フレーム黒/ジャンプを作らない）。
- **静止画（Codex生成）を動かす手法をローテーション**（同一手法の連続禁止）：
  - `bleed`＝2.5Dパララックス（前景/被写体/背景を深度分離、別速度）
  - `scan`＝微グリッド/走査光（書類・地図に情報系の質感）
  - `duotone`＝ネイビー基調の雰囲気ショット
  - `focus`＝ラックフォーカス送り
  - 斜め2.5D "card" は**稀に**のみ（全カード単調はNG）
- **モーショングラフィックス**：`$40` / `in rem` の法理 / 押収規模の数字カウント / 年表を、**大型キネティックタイポ＋spring＋scale＋Trailモーションブラー**で。上部1/5レイヤー（下部字幕と別）。`script.annotated` の `on_screen_text`/`visual_intent` を**必ず実装**。
- **フッテージ（factory棚）**：主役。**強め暗く＋ネイビー寄せ＋ビネット**で統一。素の霧/空/抽象など featureless クリップは除外。
- **オーバーレイ**：塵/フィルムグレイン/揺らぐ照明を薄く常時。
- **Runway（契約内・点で使用）**：フック冒頭 or ACT IV の決定的1–2カットのみ img2vid で生かす。使いすぎない。
- **禁止エフェクト（使わない）**：金の縦スイープ（`WipeTransition`）／黄・金の全画面ウォッシュ・フラッシュ／ただのズーム・左右パン（`CameraRig`）。`StyleTest` は手本にしない。

> **不変項11＋オーナー指示(2026-07-04)**：**人物の姿は描いてよい**——役者的な"代表的人物"（匿名の一般人の像）はOK。むしろ人を映して画面を生かす。**禁じるのは実在・特定できる本人の肖像だけ**（Sourovelis家本人・実名個人の顔の再現）。よって Codex画像は「敷居に立つ父親」「引越し箱を運ぶ家族」「令状フロアで待つ所有者たち」等の**匿名の人物**で描く（実在の誰かに似せない・特定顔の一致を避ける）。実写の本人アーカイブ素材は権利未クリアなので使わない（factory棚＝権利クリア汎用のみ）。シルエット/後ろ姿/手元は"手法の一つ"であって縛りではない。

---

## 6. 素材プラン（row 7・**集めて未使用ゼロ**）

- **密度**：`distinct_factory_used ≥ runtime/30` → **≥ 24 distinct クリップ**。単一クリップ再利用 **≤ 3回**。空スパン 0。
- **画像:フッテージ ≒ 4:6**（kyllo v002 の学び）。全素材を no-repeat（MIN_GAP~22）で散らす。
- **factory 抽出テーマ**（`select_factory_assets.py --theme`）：`property`（連棟住宅/玄関/鍵/引越し）, `crime`（パトランプ/夜の街/証拠袋）, `legal`（法廷/書類/ガベル/ファイル）, `finance`（現金/帳簿/数字）, Philadelphia の街。cf. `[[reference_factory_shelf]]`。
- **Codex 生成ヒーロー静止画**（`ai_prompts.v001`・**計40枚**・1画像=1プロンプト・長辺≥3840・**匿名人物OK/実在本人の肖像なし**・使い回し単調回避）：敷居に立つ父親（匿名）／引越し箱を抱える家族（匿名）／令状フロアで待つ所有者たち（匿名群衆）／施錠告知の書類マクロ／夜の連棟住宅／空の法廷（Courtroom 478 の雰囲気）／敷居に置かれた鍵／没収書類の山／$の帳簿。各プロンプトに negative（**specific real person / celebrity likeness**, on-image text, bad anatomy…）と upscale≥3840 を明記。人物像は自然な実写調で、特定の実在人物に似せない。

---

## 7. OP/ED（row 14・**正典 Bookends・作り直さない**）

- `remotion/src/components/Bookends.tsx` の **`BrandOpening{seriesLabel,title,subtitle}` / `BrandEndcard{channel?,ctaLine?,cadenceLine?}`** を import（`OPENING_SEC=3.5` / `ENDCARD_SEC=9` 固定）。フォーク禁止（不変項14）。
- 金 `BrandOpening` は**フックの後**（8.0s〜）に着地、`BrandEndcard` は末尾。
- `seriesLabel="Prime Documentary"` / `title`（短縮タイトル）/ `subtitle`（サブ）。
- **ED CTA（稼いだ Like・row10）**：`If you didn't know the government could do this — hit like, so more people do.`（汎用のお願いにしない）。

### 7a. 音声エンディング（オーナー指示2026-07-04・row1関連）
- EDのBGMは**切りのいい所（musicalな終止）で終わる**。末尾9秒 `BrandEndcard` を**アウトロ専用枠**にする。
- **エンディング用キュー（自然に解決する曲）**を、**"曲自身の終わり"が動画終端に一致するよう align-to-end 配置**（ループを途中でブツ切りしない）。最後は拍/終止に合わせ**1.5–2sのクリーンフェードで無音着地**。
- **ナレ長・間は一切変えない**（尺は台本が主。曲をこの枠に収める側で合わせる）。
- ゲート＝**`bgm_ending`**（終端が全音量チョップでない＝解決/フェードしている・実装済）。musicalに"収まったか"は最終**耳チェック（末尾10秒）**で確認（機械では測れない部分）。

---

## 8. サムネ（rows 11–13・派手・CTR最優先・肖像なし）3案

全案：1280×720、UPPERCASE ≤4語、巨大主題、超高コントラスト、黒/ネイビー背景＋**gold `#E5B53A` or electric `#1F6BFF`**、白/銀文字、320pxで可読。Codex で背景アート事前生成。`selected` を1つ。

1. **`THEY TOOK THE HOUSE`** — 夜の連棟住宅にパトランプのゴールドグロー、玄関に赤い封印。
2. **`$40 → YOUR HOME`** — 左に握られた少額紙幣、右に施錠された家。矢印はネイビー。
3. **`NO CRIME. NO HOUSE.`** — 空の法廷＋鍵、白文字＋gold下線。

タイトル（≤60字・フック先頭・A/B 2案）：
- A `They Took Their House Over $40 — And Never Charged Anyone`
- B `The City Tried to Seize a Family's Home for a $40 Crime`

---

## 9. 通過必須ゲート（Done の定義・§D）

`./.venv/Scripts/python.exe scripts/check_final_acceptance.py 28 --json` が **exit 0**。ハードゲート（実ファイル測定）：
- `runtime_band` 690–750s / `render_resolution` ≥1920×1080 / `images_present`（黒過多なし）/ `bgm_present`（無音>25s なし・VO下も可聴フロア）/ `bgm_ending`（終端が切りよく解決）
- `motion_present`（freeze なし）＋ **`animation_density`**（near-still ≤10%／単一ホールド≤3s＝スロー・ケンバーンズ/紙芝居を検出。freezeだけでは抜けるやつ）
- `voice_is_master`（ElevenLabs・SAPI不可）/ `captions_final`（≥90%カバー）/ `caption_format`
- `caption_narration_match`：焼き込み字幕 ↔ narration `spoken_text` の**トークン一致 ≥90%**（字幕とナレ不一致を機械で阻止）
- `structure_4part`：narration 章立てが **HOOK→OPENING→body→ENDING**＋`forfeiture_film.json` に実フック（hookSeconds≥5・hookLine非空）
- `op_ed_bookends`：コンポジションが正典 `BrandOpening`+`BrandEndcard` を使用
- **【新規・素材/サムネもコード化(2026-07-04)】**
  - `footage_diversity`：distinct/total ≥0.40・1クリップ再利用≤4・天秤等の汎用象徴≤2（**同じ素材の使い回し**を機械で阻止）
  - `thumbnail_visibility`：selectedサムネの輝度 mean ≥33＋コントラスト下限（**暗い/しょぼい/CTR低下**を阻止）
- `thumbnail_ready`（≥3×1280×720＋selected）/ `image_resolution`（長辺≥3840）/ `factory_used`（≥runtime/45 かつ参照）

**Ship-gate（`docs/PD_SHIP_GATE.md`）**：`check_final_acceptance.py 28 --render <mp4> --emit-receipt` で**動画sha256に紐づく受領書**を発行 → `upload_schedule_case_v001.py --ep forfeiture` は**緑の受領書（sha一致・許容不合格はruntime_bandのみ）が無ければ物理的に投稿不可**。自己申告Done不可。

**手動実測（未コード化・飛ばさない）**：row5 画質/sharpness・row13 タイトル≤60/A-B・row15 film-bible クラフト・**目視で失敗1〜9が消えたか**（MotionSample と並べて見比べ／on_screen_text 全実装確認）。

---

## 10. Codex 前に Claude がロックする成果物（§B・左工程ゲート）

1. `EP28_FILM_BIBLE.v001` + `script.annotated.v001.json`（Academy級・フック最後・4部ロール・語数173wpm band・`on_screen_text`/`visual_intent` 付き）
   - **§10a 台本レビュー＝最低3パス（オーナー指示2026-07-04・全パス通過まで handoff しない）**：
     - **Pass 1 — 事実/因果(R2/R3)**：全★を出典で逐語ロック・causation lock・存命人物/未成年の扱いを法務チェック・捏造ゼロ。
     - **Pass 2 — ドラマ/クラフト(row15)**：コールドオープンの問い→三幕の上げ→ペイオフが効いているか。**「普通の情報提供」になっていないか**を1文ずつ点検し、平板箇所を書き直す。
     - **Pass 3 — リテンション/字幕(row16)**：再フック~2:30ごと・20秒超の平坦なし・オープンループ回収・語数173wpm band・**息継ぎ単位で字幕分割**できる文か。
2. `shotlist.v001.json`（全スパン：asset_type+motion+transition+factory `search_keywords`・平均≤6s・0.35s クロスフェード）
3. `ai_prompts.v001`（1画像1プロンプト・肖像なし・≥3840）
4. `thumb_prompts.v001` + 見出し/キッカー候補
5. **`fact_recheck.v001`（R2）**：★の固有名詞・金額・日付・和解条件を逐語ロック＋法務レビュー（存命人物・未成年逮捕の扱い）
6. `manifest.target_duration_minutes = 12`（standard band）

> **順序**：まず **fact_recheck（R2）** で★を確定 → FILM_BIBLE/script → shotlist/prompts → Codex 画像生成 → Remotion 組み立て（Claude）→ acceptance exit0 →**目視で失敗1〜9消滅を確認** → first-cut / title-thumb / pre-publish の各オーナーゲート → `package_ready`。**1本ずつ**（EP29/30 は本設計書の同テンプレで順次）。
