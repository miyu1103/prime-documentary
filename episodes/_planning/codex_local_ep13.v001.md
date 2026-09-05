# ローカルCodex プロンプト — 第13話(king) 制作〜YouTubeアップロード直前までノンストップ【確定版・詳細版 v001 / そのまま貼る】

> 確定状況（2026-06-23・Claude確認済み）
> - 第13話 `PD-2026-013-king`（Maryland v. King 2013 / 逮捕時のDNA採取は「身元確認」か「捜索」か・569 U.S. 435・5–4）。state=script_verified・validate_episode 13 PASS。23ショット。
> - 本編AI画像 生成済み前提：`H:\pd-media\assets\ai\king\SPN-XXXX*.png`（13スパン）。実写動画＝asset_map の `🎬 *.mp4`（6スパン・DL済み）。サムネ6案 生成済み前提：`H:\pd-media\assets\ai\thumbs\king\THUMB-01..06.png`。
> - 仕上げ設計＝`08_edit/edit_design.v001.md`（§1 4部構成/尺12分・§2 全23ショットのアニメ・§3 字幕レイアウト/可読性・§6 Premium実装・§7 ファクトリ本格活用）、音声＝`06_audio/audio_cue_sheet.v001.md`。**この2本＋ `VIDEO_RULES.md` ＋ `FACTORY_INVENTORY.md` に従う**。
> - アニメは **Premium級コード演出（`KingPremium.tsx`）が主役**＋**DL済みファクトリ素材（66,844点）をふんだんに加飾**（テーマ別b-roll/背景/光・粒子・vfx/質感）で“美しくダイナミック”に。
> - **題材の節度（厳守）**：King は**暴行(assault)で逮捕**。レイプは事後のDB照合ヒット。**綿棒採取が逮捕理由であるかのように示唆しない**。性犯罪題材はソバー（生々しい描写・被害再現は不可）。実在人物・判事の肖像なし。

あなたはローカルのCodexです。作業フォルダ `C:\Users\aab15\Documents\prime-documentary`（ブランチ `claude/vibrant-archimedes-2mmr5h`）。
**第13話 PD-2026-013-king を、制作から"YouTubeアップロード直前"まで一気通貫（ノンストップ）で**仕上げてください。slug=`king`。
**唯一の停止点は「YouTubeアップロード直前」**（最終動画＋パッケージを用意して停止→オーナーが1回確認→アップロード/公開はオーナー操作）。それ以外の中間レビューでは止まらない。

---

## ★最重要（必ず最初に）
- **フルアクセス（全権限・自動承認）で起動。** 許可待ち・中間レビュー待ち・ナレ課金待ちで**止まらない**。
- **4部構成・尺 約12分（11.5〜12.5分）**：①フック(本編ハイライト約8〜10カット・各1〜2秒・新規制作しない)→②オープニング(`BrandOpening`・約3.5秒)→③本編(act1〜act4)→④エンディング(結末＋シリーズ統合＋次回予告=家への追跡＋CTA・約80〜90秒)。台本（ナレ本文）は変えず、フック＋エンディング＋幕間の“ひと呼吸”（山場SPN-0012判決リビール後の余韻・act転換の間）で約12分に寄せる。間延びさせず密度で。
- **先に4部の骨組み（空シーケンス）→中身→最後に「4部か・約12分か・綿棒≠逮捕理由が守れているか」を確認**してから書き出す。

## まず読む（台本・claims・注釈はロック＝変更禁止。誤りはSTOP報告）
- `episodes/PD-2026-013-king/08_edit/edit_design.v001.md`（**最重要**＝§2 全23ショットのアニメ表／§3 字幕レイアウト・可読性／§6 Premium実装の SPN→部品割り当て／§7 ファクトリ本格活用の SPN→theme/subtype 割り当て）
- `episodes/PD-2026-013-king/06_audio/audio_cue_sheet.v001.md`（音声4層＋ダッキングの章別キュー）
- `episodes/_planning/VIDEO_RULES.md`（§0 最優先／§4 ファクトリ活用／§8 ノンストップ＆停止点／§10 尺12分／§12 美しくダイナミック／§13 字幕同期・可読性）
- `episodes/_planning/FACTORY_INVENTORY.md`（棚のテーマ/サブタイプ・取り出し方）
- `episodes/PD-2026-013-king/03_script/script.en.v001.md`（`[VO:]`＝ナレ本文）, `04_scenes/shotlist.v001.json`, `04_scenes/asset_map.v001.md`
- 雛形：`remotion/src/compositions/CarpenterPremium.tsx`（同シリーズ・同論点系。`Vote`/`MapGrid`/`TwoColumn`/`Doors`/`BigNumber`/`CourtColumns`/`Boundary`/`Triptych`/`SceneShell`/`Lower`/`ReconLabel` を移植）

## 仕上げ仕様（必須）
- **意味のあるアニメ（コード演出が主役）**：Ken Burns一辺倒にしない。論点＝「**fingerprint（身元確認）vs search（捜索）**」の対比と、**逮捕→綿棒→DB照合→一致**の因果線を視覚化（§2の表どおり）。
- **美しくダイナミック**：全カットに `MovingStage`/`CameraRig` で寄り/引き/パララックス＋イージング（spring/ease・リニア禁止）。山場（SPN-0012）は**ため→開放**＋SFX同期。上品で速いトランジション（光ワイプ/クロスディゾルブ）。
- **ファクトリをふんだん加飾（三層・§7）**：背景プレート（forensics_dna/crime_police/legal_court/surveillance_tech）＋light/vfx/particleオーバーレイ(screen/add)＋texture(overlay)。加飾は控えめ・1カット1〜2層・主役を食わない。
- **音は4層＋ダッキング**：ナレ＋BGM(Suno)＋SFX＋環境音。ナレ中はBGM/環境音を自動で下げ、ナレ最優先。−14 LUFS / true peak ≤ −1 dBTP。
- **字幕＝ナレと“ぴったり同期”＋見やすい**：forced alignment で語単位・一字一句一致・**ズレ≤約120ms**。**≈48〜60px・本文太字・白文字＋濃い縁取り/影＋半透明黒帯(不透明度~55〜70%)・最大2行・中央寄せ・下部安全帯・1〜2行ずつ送り**（高速点滅切替しない）。**テロップ(上/中央)・出典(金ライン・右下)・AI開示(右上)とゾーンで分離し一度も被らせない。**

## 手順（1〜9はノンストップ。止まるのは10だけ）

### 1. 素材ステージング
```
./.venv/Scripts/python.exe scripts/import_to_remotion.py 13 --write
```
→ AI画像/実写を `remotion/public/king/` へコピー。`coded/cards=0` を確認（`mahanoy_roughcut.ts` 相当の `king_roughcut.ts` は下見用）。

### 2. ファクトリ素材をふんだん取り込み（§7 の割り当てどおり）
テーマ別に動画/静止を抽出 → `remotion/public/king/factory/` へコピー（**license=allowed のみ**・出典/sha256記録）：
```
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme forensics_dna --kind video
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme crime_police --kind video
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme legal_court --kind video
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme surveillance_tech --kind video
# 質感: --theme texture / 光: --category light_assets / 粒子: --category particle_assets / 煙等: --category vfx_overlays / 抽象ループ: --theme abstract_loop
```
主な実在subtype（FACTORY_INVENTORY準拠）：forensics_dna=dna_double_helix_render / dna_laboratory_blue / fingerprint_scan_blue / fingerprint_dust_lift / blood_sample_vial。crime_police=evidence_bag / evidence_locker_shelves / police_interrogation_room_empty / police_badge_close_up / jail_cell_bars / prison_corridor / case_files_stack_desk。legal_court=courtroom_interior / courtroom_empty_wide / judge_gavel_wooden / balance_scale_brass / antique_brass_scales / law_library_books / us_constitution_document。surveillance_tech=data_center / server_room_blue / circuit_data_flow / world_map_dark_glowing（＋loops=data_stream_loop）。

### 3. ★KingPremium 作成（最重要・コード演出が主役）
`remotion/src/compositions/KingPremium.tsx` を新規（CarpenterPremium雛形・private部品を移植）。`scenes[]` に23スパン＋hook/opening/ending を `kind` 付きで**章順**に定義。AI画像は `king/SPN-XXXX*.png`、実写は `king/<*.mp4>`、ファクトリは `king/factory/<file>` を参照。`Root.tsx` に `KingPremium`（id="KingPremium"・ハイフンのみ）登録（既存 `RoughCut-king` は残す）。
**SPN→演出→部品→ファクトリ（§2/§6/§7 の要約・この通り実装）**：
- 0001 hook: 綿棒→DNA二重らせんがDB格子へ吸い込まれる（手組みSVG＋`MovingStage`）。背景=forensics_dna(dna_laboratory_blue)、texture下地、AI開示`ReconLabel`。「Arrested — not convicted」。
- 0002 opening: 「Identification / Search」が "or" で左右分岐（`TwoColumn`＋タイポ）。背景=us_constitution_document、light=soft_golden。
- 0003 act1: USマップ→Maryland ピン波紋＋年表2009（`SceneArt map`＋`timeline`）。テロップ "assault"。b-roll=courthouse/urban_night。
- 0004 act1: 綿棒/booking へ寄り "NOT the reason for arrest" を赤系強調（AI＋`Lower`）。背景=police_interrogation_room_empty 薄く。
- 0005 act1: DB走査→1セルMATCH点灯（`MapGrid`＋手組み・`data_blip`同期・ソバー）。背景=server_room_blue/data_center、loops=data_stream_loop。年表2003小さく。
- 0006 act1: 解決 vs 嫌疑なき捜索の左右対比（実写`<Video>`＋`TwoColumn`）。b-roll=crime_police。
- 0007 act1: 「両方とも真実」へ転換（AI＋微パララックス＋フェード）。particle=dust_motes 薄く。
- 0008 act2: 「fingerprint or search?」中心の問い（AI＋指紋/虫眼鏡アイコン＋軽ズーム）。
- 0009 act2: booking実写＋「fingerprints+photo=identify」等式カード（`<Video>`＋手組み）。
- 0010 act2: 指紋→DNAへモーフ「21世紀の指紋」（AI＋手組みモーフ＋ラベル）。背景=fingerprint_scan_blue。
- 0011 act2: CODIS=全米DNA DBのネットワーク図（多数ノード点灯→中央収束）。背景=world_map_dark_glowing/data_center、loops=abstract_network_nodes_loop。
- 0022 act2: 指紋(点集合) vs 遺伝子設計図の左右対比（`TwoColumn`＋手組み）。
- 0012 act3【山場】: 年表2013→**`Vote`(5–4)**→出典 569 U.S. 435 を金ラインで確定（`SceneArt timeline`＋`Vote`＋`SceneArt seal/document`）。**`LightSweep`=GOLD・god_rays＋smoke_on_black で ため→開放**＋`gavel_knock`+`low_boom`→`stamp_seal`。背景=courtroom_interior。
- 0013 act3: 多数意見Kennedy「指紋・写真撮影と同様」（実写法廷/小槌＋引用句テロップ）。b-roll=legal_court(judge_gavel_wooden)。
- 0023 act3: Kennedyの「identification は名より広い」注記カラム（AI＋手組み）。
- 0014 act3: 異色連合（Scalia＋リベラル3名の名が中央で1本に合流）。**肖像不可・タイポのみ**。
- 0015 act3: Scalia反対句「rightly or wrongly, and for whatever reason」を1語ずつ刻むタイポ。重い寄り（誇張せず）。
- 0016 act4: 「全米で逮捕＝DNA提供」へ（実写数秒切替）。b-roll=jail_cell_bars/prison_corridor 落ち着いて。
- 0017 act4: 天秤の両皿「事件解決 / 単に逮捕された人々の登録」どちらにも傾けすぎない（`SceneArt scales`/`balance_scale_brass`）。
- 0018 act4: 「一票で決まった取引」寄りで余白・中立に締める（AI＋particle薄く）。
- 0019 ending: 「Identify you / investigate you?」を最後にもう一度左右対比（実写＋`TwoColumn`）。
- 0020 ending: シリーズ統合「pockets→phone→property→contracts→body」5語が順に積み上がり "body" で確定（`Doors`/手組み）。
- 0021 ending: 次回予告「can a cop follow you into your home?」家のドアへ引き＋タイトル示唆（AI＋property_home(front_door_house) 薄く）。
> ※`Vote` は CarpenterPremium 内 5–4 固定（9マス・i<5 着色・"5–4"）。本話はそのまま 5–4 でよい（改変不要）。実写スパン（0006/0009/0013/0016/0019/0022）は **人物の顔・実在人物を出さない**（象徴素材のみ）。長尺（0011=47s/0015=49s）は約4.5秒ごとに別カット/別バリアントへ切替。

### 4. 自己確認（止まらない）
```
cd remotion && npm run studio   # → KingPremium
```
§2の各演出（0001 DNA吸込／0005 MATCH／**0012 5–4＋出典確定**／0014 異色連合／0017 天秤）が出る／4部構成／約12分／**字幕とテロップ非重複**／**「綿棒＝逮捕理由」と誤読させる演出が無い**／実在人物の肖像が無い を自分で確認。OKならそのまま次へ（オーナー確認待ちで止まらない）。

### 5. ナレーション（課金気にせず実行）
`script.en.v001.md` の `[VO:]` を ElevenLabs 生成（**課金承認待ち不要**）。
- ドラフト → `H:\pd-media\episodes\PD-2026-013-king\06_voice\draft\VC-XXXX.mp3`(+.json)、マスター → `…\06_voice\master\VC-XXXX.mp3`。
- 索引/計画 → `episodes/PD-2026-013-king/06_audio\narration_index.v001.json` / `voice_plan.v001.json`。`KingPremium` にマスター連結。

### 6. 音＆字幕（audio_cue_sheet 準拠）
- BGM(Suno)＋SFX＋環境音を**ダッキング**込みでミックス（−14LUFS/TP≤−1）。山場0012は `reveal` 系BGM＋`gavel_knock`/`low_boom`/`stamp_seal`。性犯罪題材の章はソバーなトーン。
- **字幕＝forced alignment でナレと“ぴったり同期”**（語単位・一字一句一致・ズレ≤約120ms）→ `08_edit/captions.v001.srt`(+.json)。見やすさ仕様（上記）厳守。テロップ/出典/AI開示と非重複。
- ナレタイムライン → `08_edit/narration_timeline.v001.json`。音源は `H:\pd-media\library\`。

### 7. サムネ（CTR最大化が選定基準・止まらない）
`THUMB-01..06` を**クリック率最大化の観点で評価して最強の1枚を自動選定**。評価軸＝(a)高コントラスト・一目で分かる単一の主被写体 (b)強い感情/葛藤 (c)タイトルを置く明快な余白 (d)モバイル小サイズでの可読 (e)ブランド配色(黒/紺/青/金) (f)誇張しすぎない正確さ（綿棒≠逮捕理由を誤認させない）。`thumb_prompts.v001.md` の**タイトル3案(A/B/C)を全部** `ThumbnailFrame` で **1280×720** 書き出し。
- 保存 → `episodes/PD-2026-013-king/10_thumbnail/king_thumbnail_optNN.v001.png`、候補メタ＋各案のCTR評価 → `09_package/title_thumbnail_candidates.v001.json`。暫定勝者を採用にしつつ**全候補を残しA/B差し替え可**。実在人物の肖像なし・広告安全。

### 8. 最終レンダー
```
cd remotion && npm run render KingPremium out/king_premium.mp4 --crf=14
```
CPU/libx264・1920×1080・30fps・**NVENC不可**（品質最優先）。
- 最終 → `H:\pd-media\episodes\PD-2026-013-king\08_edit\king_premium_v001.mp4`。QC（尺≒12分/−14LUFS/字幕同期/綿棒≠逮捕理由/肖像なし）→ `08_edit/renders/final.v001.qc.json`。

### 9. パッケージ（pd-package）
タイトル(A/B/C)/説明/チャプター/字幕(SRT)/タグ/権利マニフェスト/`youtube_meta` を `09_package/` に作成。
- **公開予約は `2026-06-28T12:00:00+09:00`（JST 6/28 12:00 ／ UTC `2026-06-28T03:00:00Z`）** を `youtube_meta`（`scheduled_at_local`/`scheduled_at_utc`・privacy=private→公開予約）に設定。
- 商用OK・実在人物の肖像なし・AI開示を `rights_manifest` で確認。**ここで停止し「アップロード準備完了」を完成動画＋パッケージのパス付きで報告。**

### 10.【唯一のSTOP＝YouTubeアップロード】※オーナー承認が必須
**アップロード／公開予約（6/28 12:00 JST）は、オーナーが完成動画を確認した後に、オーナー操作/承認でのみ実行**（invariant 2・YouTube予約は6/24以降OK）。Codexは自動で越えない。

> 各ステップでコミット（`H:\pd-media` と `remotion/public` はGit管理外。コミットは台本/設計/`*.tsx`/`*_roughcut.ts`/captions/manifest/package 等の軽量成果物のみ）。

---

## ノンストップ運用
- 手順1〜9はオーナー確認を挟まず一気に通す。詰まっても止めず自分で判断して進め、最後にまとめて報告。
- 止まるのは手順10（アップロード）だけ。承認なしに越えない。
- 例外で即STOP：台本/claimsの重大な事実誤り、権利・実在人物の肖像リスク、**「綿棒＝逮捕理由」と誤認させる/性犯罪題材が過度になる恐れ**。

## この話の厳守
- **節度**：King の逮捕理由（暴行）と事後のDB照合（レイプ事件の解決）を**明確に分離**。被害再現・センセーショナルな描写は不可。綿棒採取を逮捕理由のように示唆しない。
- **中立**：公共安全 vs プライバシーのどちらにも肩入れしない。Kennedy多数意見と Scalia反対意見を公平に。
- **実在人物・判事の肖像なし**（象徴・タイポで代替）。ディープフェイク不可。AI画像は必ず開示（`ReconLabel`）。一般ストックは「事件の実物」として提示しない。台本・claims・shotlist 不改変（章順並べ替えのみ編集側で）。

## 最初のアクション
手順1から開始し、手順1→9をノンストップで実行（素材ステージング→ファクトリふんだん取り込み→KingPremium実装→自己確認→ナレ→音/字幕→CTR最大サムネ→最終レンダー→パッケージ※予約6/28 12:00 JST）→ 手順10の手前で停止して「アップロード準備完了」を報告。
