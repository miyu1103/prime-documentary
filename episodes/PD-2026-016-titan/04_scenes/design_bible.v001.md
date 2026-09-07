# EP16 「TITAN」 — Design Bible (60分・旗艦作)

> Episode ID (予定): `PD-2026-016-titan`
> Format: **feature**（旗艦・60分）／ Language: **English narration**（米国バズ狙い・ElevenLabs master）
> Status: DESIGN DRAFT（未承認。topic/thesis/final-script は人間ゲート）
> Owner working note: この文書は「設計の確定版骨子」。実制作は pd-new-episode で workspace を切ってから。

---

## 0. なぜこの題材か（一行で）

オーシャンゲート「タイタン」号圧壊事故（2023年6月）。
**潜水艇事故の話ではない。「ルールは自分には当てはまらない」と言う男を、なぜ賢く成功した大人たちが信じたのか——アメリカの“天才信仰”の悲劇。**

---

## 1. CORE（脚本の背骨）

- **Thesis**: A culture that worships the rule-breaking founder will, eventually, follow him past the point where physics stops negotiating. The ocean is the one investor that always does its own due diligence.
- **Viewer promise**: By the end you will understand why five intelligent people sealed themselves inside a vessel they had been warned would fail — and why that decision was not stupidity, but belief.
- **Controlling emotion**: 怒りと哀悼の同居。最後は「なぜ我々は信じたのか」という観客自身への問い。
- **Logline**: A safety test of one small submersible became, through one man's faith in himself and a culture that rewarded it, the death of five people at the most famous monument to hubris on Earth — the wreck of the Titanic.

### タイトル候補（English / 米国CTR）
1. **"Pure Waste"** — *The Last Dive of the Titan*（悪役自身の言葉を冠に）★本命
2. **"They Were Warned"**
3. **"The Man Who Said Safety Was a Waste"**
4. **"96 Hours"**（カウントダウンの皮肉）

### サムネ方向（※thumbnails.set は PD-001 でAPI不可。手動アップロード）
- A案：漆黒の深海に、豆粒のような潜水艇のシルエット＋光の筋。文字 **"THEY WERE WARNED"**。
- B案：外から締められる17本のボルト（ハッチ）。文字 **"PURE WASTE"**。
- C案（情感）：暗闇に浮かぶルービックキューブ。文字 **"HE WAS 19"**。
- → 実在人物の顔は使わない（invariant 11）。象徴物＋余白＋大きな1フレーズでCTRを取る。

---

## 2. STRUCTURE（60分・5楽章＋前後）

検証は **feature プロファイル**（後述§8）で 55–65分 / 約8,200–9,500語（150wpm）。

| # | 時間 | 章 (chapter_id) | function | 観客の感情 | 章末の崖（再フック） |
|---|------|-----------------|----------|-----------|----------------------|
| — | 0:00–1:30 | `cold_open` | cold_open_tease | 喉元をつかむ | タイトル |
| 1 | 1:30–13:00 | `the_dream` | thesis_and_promise / system | 誘惑・畏れ | 最初の警告者が去る |
| 2 | 13:00–28:00 | `the_warnings` | event / turn | 不安・苛立ち | 5人が乗り込む |
| 3 | 28:00–40:00 | `the_dive` | event | 緊張・無力 | 交信、途絶 |
| 4 | 40:00–52:00 | `the_search` | impact | 哀悼 | 残骸の発見 |
| 5 | 52:00–58:00 | `the_truth` | reveal / ruling | 慟哭と問い | テーマ着地 |
| — | 58:00–60:00 | `coda` | payoff_and_cta | 余韻 | 暗転 |

### 連結ルール（賞レベルの裏ルール）
- 章は **「だから／しかし」** で繋ぐ（“それから”禁止＝AI-fillerにもなる）。因果の鎖＝宿命感。
- 各章に **未回収の問い（open loop）** を1–2個キープ。冒頭の「外からの封印」は§3で爆発させる。
- 結末は全員が知っている。だから **サスペンスは「どうなる?」でなく「なぜ止められなかった?」**。サプライズではなく悲劇。

### 各楽章の中身

**COLD OPEN (0:00–1:30)** — ハッチが外から閉じられる。17本のボルト。内側からは開かない。ラッシュの声（引用）"At some point, safety is just pure waste." 最後のボルトが締まる→暗転→TITLE。死は見せない。

**第1楽章 THE DREAM (1:30–13:00)** — ストックトン・ラッシュとは誰か。「規制は進歩の敵」というシリコンバレー的信仰。なぜ富豪・専門家が$250,000を払いタイタニックを見に行くのか。タイタニックの引力＝「不沈神話」という最初の傲慢の伏線。*崖：ある技術責任者が「これは危険だ」と言い、会社を去る。*

**第2楽章 THE WARNINGS (13:00–28:00)** — カサンドラたち（David Lochridge／業界団体MTSの警告書／炭素繊維船体の疲労問題／認証拒否）。ラッシュは doubles down。乗客紹介：Paul‑Henri Nargeolet＝"Mr. Titanic"（数十回潜った世界一の専門家ですら乗る＝誘惑は専門家を飲む）、Shahzada Dawood と息子 Suleman(19)。少年は怖がっていた。父の日に、父を喜ばせるため乗ったと母は語る。*崖：5人が乗り込む。*

**第3楽章 THE DIVE (28:00–40:00)** — 2023年6月18日。降下。冒頭の「外からの封印」の回収。最後の交信。1時間45分で連絡途絶。海の沈黙。*観客はもう知っている。*山場の演出＝**全音を切る一瞬の完全な無音**。*崖：交信、途絶。*

**第4楽章 THE SEARCH (40:00–52:00)** — 世界が4日間祈る。"96 hours of oxygen" の報道カウントダウン。検知された謎の「叩く音」＝偽りの希望。支援船の上で待つ母クリスティン。*知っている観客の哀悼を最大化する。サプライズではなくエレジー（哀歌）。*崖：残骸の発見。*

**第5楽章 THE TRUTH (52:00–58:00)** — 彼らは初日に、1000分の1秒で即死していた。圧壊の物理（簡潔・尊厳をもって・遺体や恐怖は描かない）。全員が警告されていた。テーマ着地＝**なぜ我々は天才を信じたかったのか**。ルービックキューブの回収。

**CODA (58:00–60:00)** — 母クリスティンの言葉（公開済み発言ベース）。海の沈黙。111年前、同じ海域で「不沈」が沈んだ。最後の一行→暗転。

---

## 3. SIGNATURE DEVICES（“受賞シーン”＝具体的見せ場）

各々が単独でトロフィー級。台本・絵・音をここに集中する。

1. **誓約書（The Waiver）** — 一枚目に "death" の語が3回。淡々と読み上げるだけ。乗客全員がこれを読んでサインした。
   - 絵：factory `documents_paper/contract_paperwork_signing` + `atmosphere_symbolic` の `magnifying_glass_on_document`、下地に texture `aged_document_texture`。"death" の語だけ on-screen でハイライト。
2. **30ドルのゲームコントローラー** — 笑える→数秒後に凍る。喜劇から恐怖への転調。
   - 絵：SDXL hero（generic game controller in shadow、ブランド非特定）。
3. **"Safety is just pure waste."** — 悪役自身がテーマを宣言。説明しない、彼に言わせる。引用は documented quote のみ。
4. **ルービックキューブ** — 映画で最も残酷な小道具。少年の愛の証拠。§5で回収。
   - 絵：SDXL hero（a Rubik's cube resting in cold blue darkness）。
5. **Mr. Titanic の手** — タイタニックに数十回触れた手が、タイタニックのそばで止まる。
   - 絵：SDXL hero（elderly hands, no face）＋factory `atmosphere_symbolic/elderly_hands_close_up`。
6. **“叩く音”（The Bangs）** — 捜索中に検知された正体不明の音。世界に偽りの希望を与えた。
   - 音：SFX 規則的なノック→ニュース室の高揚→真実で意味が反転。
7. **96時間カウントダウン** — `clock_ticking_macro` ＋ tick SFX を全編の通奏低音に。最後に「実は最初から0だった」で機能反転。
8. **完全な無音（§3 圧壊点）** — 全レイヤーを一瞬カット。沈黙＝最大の音。

---

## 4. VISUAL DESIGN（三層構成：象徴SDXL × 確立b-roll × 意味グラフィック）

VIDEO_RULES準拠。1カット1–2レイヤ。配色＝黒/紺/電光青/金（house style）。**実在人物の肖像なし・実物を「その事件の実物」として提示しない（illustrative/symbolic）**。

### 4.1 Factory 素材棚（H:\pd-media\assets\factory）からの本格採用
抽出：`./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme <T> --kind <image|video>` → `remotion/public/titan/factory/` へコピー。

| 用途 | theme / subtype | 使いどころ |
|---|---|---|
| 海・畏れ | `nature_landscape`: ocean_horizon_moody / storm_clouds_dramatic / lighthouse_in_storm / harbor | 全編の“海”＝沈黙の敵役。章扉・転換・間。|
| 深海の質感 | vfx: **ink_in_water / ink_drop_in_water_slow_motion** | 降下・深海・圧壊前の暗黒（最強の見立て）。screen/add。|
| 探索オペ | `surveillance_tech`: satellite_earth_at_night / world_map_dark_glowing / radio_tower_at_night / server_room_blue / data_center | 第4楽章の捜索・世界の注視。|
| 時間の皮肉 | `atmosphere_symbolic`: clock_ticking_macro / single_chair_empty_room / padlock_and_chain / candle_in_dark / shattered_mirror / elderly_hands_close_up | 96h・空席・封印・喪。|
| 富と特権 | `finance_money`: stack_of_hundred_dollar_bills / gold_bars_stacked / open_briefcase_of_cash | $250kの席＝「金で買う死」。第1–2楽章。|
| 書類/設計欠陥 | `documents_paper`: contract_paperwork_signing / magnifying_glass_on_document / newspaper_macro；texture: blueprint_paper / aged_document_texture | 誓約書・設計図・報道。|
| 報道/世界の目 | light: tv_screen_glow_on_face；urban_night: city_skyline_dusk / drone_city_aerial_night | 捜索の世界同時中継。|
| 光と喪失 | light: god_rays / warm_window_light_rays（降下で消える光）；particle: ash_falling / static_noise_particles / bokeh_particles_dark | 表層の光が深海で失われる。残骸＝灰。comms loss＝static。|
| 章扉/データ | loops: looping_gradient_navy / data_stream_loop / atmospheric_loop | 章扉・捜索データ場面の動く背景。|

### 4.2 SDXL ヒーロー画像（Codex／A1111 :7860 / juggernautXL）
`scripts/generate_factory_sdxl.py` の STYLE/NEG を踏襲（cinematic documentary still, chiaroscuro, navy/electric-blue/gold, **NEGに identifiable face/recognizable real person を維持**）。出力→`H:\pd-media\episodes\PD-2026-016-titan\05_stock\` → manifest登録。
プロンプト・パックは §9。中核10枚：①外から締まるハッチ＆ボルト ②深淵へ降る小型潜水艇のシルエット ③押し潰す水圧の暗黒 ④ゴーストのようなTitanic残骸（象徴・disclosed） ⑤影の中のゲームコントローラー ⑥冷たい青闇のルービックキューブ ⑦ソナー画面/捜索船 ⑧北大西洋の荒れた海面 ⑨5脚の空席（no likeness） ⑩降下で消えゆく水面の光。

### 4.3 意味グラフィック（Remotion code＝“意味”の層）
- 降下の深度ゲージ（0m→3,800m）と、Titanicの深さの対照。
- 96:00:00 → 00:00:00 のカウントダウン（最後に「Day 1で既に0」と反転）。
- 警告のタイムライン（2018 Lochridge / 2018 MTS letter / …）。
- 「炭素繊維 vs 水圧」の単純図解（疲労破壊を1枚で）。

---

## 5. AUDIO DESIGN（4層・narration master = テンポ）

`pd-audio` / `scripts/build_*_audio_v00X.py` 準拠。narration=English（ElevenLabs master、SAPI下書き可）。music=Suno由来を**素材として取り込み**（invariant: 生成と仮定しない・rights tracking）。

| 層 | 設計 |
|---|---|
| **Narration** | 抑制したトーン。煽らない。少年の章だけ間を多く取る。English。|
| **Music（Suno取込）** | 楽章ごと：M1 awe/wonder（弦の畏怖）→ M2 warning（低い脈動）→ M3 descent（深いドローン）→ M4 search/elegy（喪のピアノ＋弦）→ M5 truth（慟哭、最小限）→ Coda（ピアノ一音＋無音）。|
| **Ambience** | 海面・船上甲板・北大西洋の風・水中の超低周波・船体のきしみ（不穏）・ソナー・comms static。|
| **SFX** | 冒頭ボルト締め／ソナーping／“叩く音”（偽りの希望）／メッセージ着信音／コントローラのクリック／時計のtick／**圧壊点の完全無音**。|

**演出原則**：山場は「ため（光＋ink_in_water）→ 開放」。圧壊は **無音**で抜く。海は一度も“答えない”＝BGM/SEを引かせ、人間側の喧騒（報道・自己顕示）とコントラストを付ける。

---

## 6. 品格ガードレール（最重要・全シーンの基準）

一歩間違えば「死をネタにした“ざまあみろ”動画」になる。これだけは絶対NG。

1. **基準点はスレマン少年（19）**。彼への敬意を全カットの判断基準に。嘲笑は禁止。
2. **実在人物の肖像・声の再現なし**（invariant 11）。シルエット・象徴物・documented quoteのみ。
3. **遺体・恐怖・圧壊の生々しい描写なし**。圧壊は無音と暗転で“描かない”ことで描く。
4. **存命者（Christine Dawood, David Lochridge ほか）は公開済み発言のみ**で表現。創作の台詞を付けない。
5. **ラッシュも単なる悪役にしない**。彼の信念の論理を見せる＝観客を共犯にするため。断罪より「なぜ信じたか」。
6. **stock/AIは“その事件の実物”として提示しない**（illustrative表示・disclosure）。

---

## 7. FACT / RIGHTS / BAN-SAFETY

- **事実性**（invariant 1, rule 13）：核となる事実は一次ソースで。要確認リスト＝[誓約書に"death"×3／Logitech系コントローラ／Lochridgeの警告と解雇/訴訟／MTS書簡(2018)／Nargeoletの潜航回数／Sulemanの"terrified"とルービックキューブ（母Christineのインタビュー）／圧壊が6/18・捜索6/18–22／米沿岸警備隊MBIの認定]。**公開直前に再検証**（current factsは再チェック要）。
- **故人**：Stockton Rush・乗客は故人＝米法では名誉毀損の対象外。ただし遺族感情に配慮（品格§6）。
- **存命者・企業**：OceanGate（事業停止）。存命の警告者・遺族は documented のみ。憶測の動機付けをしない。
- **BAN/収益化**：歴史・報道に基づくドキュメンタリーとして安全。gore回避。タイトル/サムネは過度な煽り回避（“ざまあ”臭を出さない＝品格と一致）。
- **R-rating**：R2想定（公開前レビュー）。R3級の法務必須ではない（cf. EP15 Theranos R3）。

---

## 8. PRODUCTION PIPELINE（実システムへの接地）

### 8.1 60分問題（feature プロファイル）— invariant 15を守って解く
`scripts/validate_episode.py` の duration 10.0–12.8分は **standard 用ハードコード**。これを**こっそり緩めない**。代わりに：
- `manifest.json` に `format: "feature"` と `duration_profile: {min_min: 55, max_min: 65, wpm: 150}` を持たせる。
- validator を「プロファイル参照」に拡張（standard のデフォルトは現状維持）。＝明示的な新プロファイル追加であって検証の弱体化ではない。
- 語数目安：60分×150wpm ≒ 9,000語。5楽章×約1,600–1,900語。AI-filler ban / FK readability は据え置き。
- これは ADR 級の変更 → `decisions/` か `architecture/adrs/` に1本起こしてから実装（Codex右工程の前にClaudeが用意）。

### 8.2 分担（Claude左工程 / Codex右工程）
- **Claude（左）**：topic → research(`pd-research`) → claims/sources → thesis → outline → **script.en + script.annotated**（5楽章・9k語）→ `pd-script`/`validate_episode.py`(feature) で **script_verified** → scene_plan(`pd-scenes`) → shotlist + ai_prompts(§9) + thumb_prompts。
- **Codex（右）**：SDXL生成(:7860)→ factory抽出→ rights gate→ Remotion `TitanFeature` composition（RoughCut拡張）→ audio 4層(`build_titan_audio_v001.py`)→ libx264 render→ QC。
- 引き継ぎ：Claudeが `script.annotated.v001.json` + `shotlist.v001.json` + `ai_prompts.v001.md` を確定 → 「script verified」宣言 → Codex が scenes stage 開始（codex-prompt形式）。

### 8.3 Remotion
- 新規 composition **`TitanFeature`**（`Episode.tsx`/`RoughCut.tsx`系を拡張、~108,000 frames @30fps＝60分）。RoughCutDataを feature 長尺に対応（章＝chapterIdでグルーピング、長尺メモリ/分割レンダ考慮）。
- 動かない絵は禁止（MovingImage Ken Burns / MovingVideo / ink_in_water overlay）。GraphicCardで欠損を仮埋め。

### 8.4 Render（quality-first / 据え置き）
- `npx remotion render TitanFeature` →（必要なら章分割→結合）→ FFmpeg libx264 `-preset slow -crf 17 -pix_fmt yuv420p`、音は別ミックス→`-c:a aac -b:a 192k`。
- 出力：`H:\pd-media\episodes\PD-2026-016-titan\07_edit\v001.mp4`（hash登録）。NVENCに切替えない（render quality-first方針）。
- 60分×crf17×preset slow は長時間。章単位レンダ→結合を前提に、夜間バッチ。

### 8.5 状態遷移（§9 PD states）
`idea → screening → approved(topic gate) → researching → … → script_review → script_verified → scene_planned → … → edit_review(first-cut gate) → … → package_ready → publish_approved(title/thumb + scheduling gate) → uploading → scheduled → published`
人間ゲート：topic承認・thesis(高リスク)・final script・first cut・title/thumb・公開予約。

---

## 9. SDXL PROMPT PACK（Codex用・house style）

共通 STYLE 付与：`, cinematic documentary still, dramatic chiaroscuro lighting, deep navy and black palette with electric blue and gold rim light, photorealistic, ultra detailed, volumetric light, subtle film grain, masterpiece, high resolution, 16:9`
共通 NEG：`text, letters, words, watermark, logo, signature, caption, identifiable face, recognizable real person, celebrity likeness, brand markings, deformed, extra fingers, bad anatomy, low quality, blurry, cartoon, anime, oversaturated`

1. `a heavy circular hatch being sealed shut from outside with rows of bolts, cold steel, claustrophobic, single overhead light` — COLD OPEN
2. `a tiny lone deep-sea submersible silhouette descending into an immense black abyss, faint shaft of surface light fading above` — descent
3. `crushing deep-ocean darkness, immense water pressure, suspended particles, a faint blue glow swallowed by black` — pressure
4. `the ghostly bow of a vast sunken ocean liner emerging from cold blue gloom, illustrative, ethereal, debris field` — Titanic (disclosed/symbolic)
5. `a generic black video game controller resting in shadow on a metal surface, single cold light, ominous` — the controller
6. `a single Rubik's cube resting in cold blue darkness, soft rim light, melancholic, shallow depth of field` — the boy
7. `green sonar and radar screens glowing in a dark ship operations room, rain on a porthole, tense` — search
8. `a violent dark North Atlantic sea at dusk, towering cold waves, lone horizon, moody, desolate` — the sea
9. `five empty chairs in a cold dark void, soft single light, absence, no people` — the five (no likeness)
10. `a fading shaft of sunlight from the ocean surface dissolving into deep blackness, god rays, lonely` — light lost

各6枚バリエ→QC(`pd-generate-assets`)→usableのみ採用→manifest(license/sourceTool/hash)。

---

## 10. 次アクション（承認ゲート順）

1. **題材＆スレート承認**（topic gate）：EP16=Titan/feature/60分 を正式採択 → `pd-new-episode` で `PD-2026-016-titan` workspace 生成。
2. **feature プロファイル ADR**：`validate_episode.py` 拡張方針を1本起こす（Claude）。
3. **Research**（`pd-research`）：§7要確認リストを一次ソースで埋める。
4. **Thesis/Script**：5楽章9k語、script_verified(feature) まで（Claude左工程）。
5. **Codex引き継ぎ**：scenes→assets(SDXL+factory)→audio→edit→render。
6. 人間ゲート：final script / first cut / title・thumb / 公開予約。

---
*この設計は「再現可能・再開可能・改善可能」を満たす範囲で最大化した骨子。実値（事実・尺・hash）は各工程で確定する。*
