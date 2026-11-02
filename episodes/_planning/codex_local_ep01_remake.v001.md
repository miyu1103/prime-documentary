# ローカルCodex プロンプト — 第1話(miranda) 作り直し（旧アニマティック→Premium）超巨大版【確定版 v001 / そのまま貼る】

> 目的：公開済みの第1話を、最新Premium水準で**作り直して旧動画と差し替える**。台本は良好（約11:33・4部構成・claim付き）＝**変更しない**。旧版がしょぼい原因＝アニマティック（タイポ中心・AI画像10枚）。新版＝SDXL大量画像＋ファクトリb-roll＋コード演出。
> 確定状況（2026-06-23・Claude準備済み）
> - `04_scenes/shotlist.v001.json`（**24ショット・691秒≒11:31**・schema検証PASS。ai_image 19／motion_graphic 3／stock_video 2）
> - `04_scenes/ai_prompts.v001.md`（**SDXL生成リスト 103枚**・JuggernautXL想定・実在人物の肖像なし）
> - `04_scenes/thumb_prompts.v001.md`（**CTR最大化サムネ6案＋タイトル3案**）
> - 既存：台本 `03_script/script.en.v001.md`（[VO:]・[CLM]）／旧 `Animatic.tsx`＋`miranda_animatic.ts`（参考・差し替え対象）。
> - ファクトリ棚 88,740点（商用OK）を**ふんだん活用**。miranda題材ど真ん中＝crime_police / legal_court / atmosphere_symbolic。
> - ナレ＝**ElevenLabsで生成OK（課金承認待ち不要）**。

あなたはローカルのCodexです。作業フォルダ `C:\Users\aab15\Documents\prime-documentary`（ブランチ `claude/vibrant-archimedes-2mmr5h`）。
**第1話 PD-2026-001-miranda を最新Premium水準で作り直し、最終動画＋パッケージを用意するところまで一気通貫（ノンストップ）で**進めてください。slug=`miranda`。
**唯一の停止点は「旧YouTube動画の差し替え/公開」**（破壊的・公開操作＝オーナーのみ。完成動画を提示して停止）。それ以外の中間レビューでは止まらない。

---

## ★最重要
- フルアクセス（全権限・自動承認）で起動。中間レビュー・ナレ課金待ちで**止まらない**。
- **4部構成・尺 約12分（11.5〜12.5分）**：①フック(本編ハイライト・新規制作しない)→②オープニング(`BrandOpening`)→③本編(act1〜act4)→④エンディング(結末＋次回予告=弁護士/Gideon＋CTA)。台本は変えず、約12分に。
- **作り直しの核心**＝旧アニマティックの「タイポ中心」を脱し、**SDXL大量画像＋ファクトリb-roll＋コード演出**でリッチに。先に骨組み→中身→最後に「4部か・約12分か・実在人物の肖像が無いか」を確認。

## まず読む（台本・claims・注釈はロック＝変更禁止）
- `episodes/PD-2026-001-miranda/04_scenes/shotlist.v001.json`（全24ショットの spine）
- `episodes/PD-2026-001-miranda/04_scenes/ai_prompts.v001.md`（**SDXL 103枚**の生成リスト）
- `episodes/PD-2026-001-miranda/04_scenes/thumb_prompts.v001.md`（CTRサムネ6案＋タイトル3案）
- `episodes/PD-2026-001-miranda/03_script/script.en.v001.md`（[VO:]＝ナレ本文）
- `episodes/_planning/VIDEO_RULES.md`（§0/§4/§8/§10/§12/§13）, `episodes/_planning/FACTORY_INVENTORY.md`
- 雛形：`remotion/src/compositions/CarpenterPremium.tsx`（Vote/MapGrid/TwoColumn/Doors/BigNumber/CourtColumns/Boundary/Triptych/SceneShell/Lower/ReconLabel）。既存 `GideonPremium.tsx`/`MappPremium.tsx` も参考。

## 仕上げ仕様
- **意味のあるアニメ（コード演出が主役）**：論点＝「取調室の非対称（取調官 vs 一人）」「権利を“持つ”と“知る”の差」を可視化。Ken Burns一辺倒にしない。
- **美しくダイナミック**：全カットに `MovingStage`/`CameraRig`（寄り/引き/パララックス＋spring/easeイージング）。山場（SPN-0012 5–4判決）は**ため→開放**＋SFX同期。上品で速いトランジション。
- **ファクトリふんだん（三層・§FACTORY_INVENTORY）**：背景プレート＋light/vfx/particleオーバーレイ(screen/add)＋texture(overlay)。テーマ＝crime_police(police_interrogation_room_empty / one_way_mirror_room / jail_cell_bars / police_badge_close_up)・legal_court(supreme_court_building / courtroom_interior / judge_gavel_wooden / us_constitution_document / law_library_books)・atmosphere_symbolic(clock_ticking_macro / single_chair_empty_room / long_shadow_of_a_person)。1カット1〜2層・主役を食わない。
- **音4層＋ダッキング**：ナレ＋BGM(Suno)＋SFX＋環境音。ナレ最優先・−14 LUFS / TP≤−1。取調室の緊張＝低いトーン＋clock_tick。
- **字幕＝ナレと“ぴったり同期”＋見やすい**：forced alignment・語単位・一字一句一致・**ズレ≤約120ms**。**≈48〜60px・太字・白＋濃い縁取り/影＋半透明黒帯(~55〜70%)・最大2行・中央・下部安全帯・1〜2行送り**（高速点滅しない）。テロップ(上/中央)・出典(金・右下)・AI開示(右上)とゾーン分離し非重複。

## 手順（0〜9はノンストップ。止まるのは10だけ）

### 0. SDXL画像 生成（103枚・★まず画力を作る）
- ローカルSDXL（A1111・主力 **JuggernautXL**・API 7860／venv python直起動）で `04_scenes/ai_prompts.v001.md` の**全103枚**を生成。
- **保存先**：`H:\pd-media\assets\ai\miranda\SPN-XXXX.png`（_02,_03…の命名どおり）。PNG・長辺2048px以上・16:9・最高画質。
- 各 `05_stock/stock_ledger.v001.json` に1行記録（source=ai_sdxl, commercial_use=allowed, sha256）。**実在人物の肖像が出ていないか**を目視で弾く（Miranda/Warren/各判事＝象徴のみ）。

### 0b. サムネ6案 生成
- `thumb_prompts.v001.md` のヒーロー6案を生成 → `H:\pd-media\assets\ai\thumbs\miranda\THUMB-01..06.png`（文字なし）。

### 1. 素材ステージング
```
./.venv/Scripts/python.exe scripts/import_to_remotion.py 1 --write
```
→ AI画像/実写を `remotion/public/miranda/` へ。`coded/cards=0` 確認。

### 2. ファクトリ素材をふんだん取り込み
```
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme crime_police --kind video
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme legal_court --kind video
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme atmosphere_symbolic --kind video
# 質感=--theme texture / 光=--category light_assets / 粒子=--category particle_assets / 煙等=--category vfx_overlays / ループ=--theme abstract_loop
```
→ トーンの合う商用OK(license=allowed)を `remotion/public/miranda/factory/` へコピー。

### 3. ★MirandaPremium 作成（最重要・コード演出が主役）
`remotion/src/compositions/MirandaPremium.tsx` を新規（CarpenterPremium雛形・private部品移植）。`scenes[]` に24スパン＋hook/opening/ending を `kind` 付きで定義。AI画像=`miranda/SPN-XXXX*.png`、ファクトリ=`miranda/factory/*`。`Root.tsx` に `MirandaPremium`（id="MirandaPremium"・ハイフンのみ）登録（旧 `Animatic.tsx`/`miranda_animatic.ts` は差し替え対象だが消さず残す）。
**SPN→演出→部品→ファクトリ（この通り実装）**：
- 0001 hook: 本編ハイライト集（ランプ/取調室/4警告カード/独房/俯くシルエット）を各1〜2秒の速いカット＋riser/low_boom。背景=police_interrogation_room_empty。
- 0002 opening: 「Not a courtesy. A repair.」机上ランプ＋修正5条の羊皮紙（`SceneArt motifHint="document/constitution"`）。texture=parchment。
- 0003 act1: 「1963 — Phoenix, Arizona」AI＋`SceneArt motifHint="timeline"`(1963)。b-roll=urban_night/desert。
- 0004 act1: 「Never told he could stay silent.」取調室で俯くシルエット（顔なし）へ寄り。背景=one_way_mirror_room。particle=dust_motes。
- 0005 act1: 取調室の非対称（取調官側 vs 空き椅子）。`TwoColumn`相当＋single_chair_empty_room。clock_ticking。
- 0006 act1: 「"Did he know he had a choice?"」中心の問い＋疑問符＋軽ズーム。
- 0007 act2: 自白→証拠→有罪。紙とペン＝“自分の言葉”。case_files_stack_desk。
- 0008 act2: 上訴「自白は数えるべきでない」。law_library_books＋寄り。
- 0009 act2【図解】「Four cases. One question.（Vignera/Westover/California v. Stewart＋Miranda）」**4つの取調室/ドアが中央で1つに集まる**（`Doors`/手組み）。
- 0010 act2: 最高裁が“パターン”を見る。supreme_court_building 薄く。
- 0011 act2: 争点が“あらゆる取調室”へ拡大＝「権利を持つと知るの差」。
- 0012 act3【山場・図解】「June 13, 1966 — 5–4 / Miranda v. Arizona, 384 U.S. 436」**年表1966→`Vote`(5–4)→出典を金ライン確定**（`SceneArt timeline`＋`Vote`＋`seal/document`）。`LightSweep`=GOLD・god_rays＋smoke_on_black で**ため→開放**＋`gavel_knock`+`low_boom`→`stamp_seal`。背景=courtroom_interior。
- 0013 act3【図解】「The four warnings」**4点が順に点灯**（Silent / Used against you / Lawyer / Appointed）＝`Doors labels`。壁のカード風。
- 0014 act3: 「No forced self-incrimination.」修正5条に接地（`SceneArt document`）。
- 0015 act3: 「Dissent —"reached too far"」Harlan & White＝**少数の反対**（肖像なし・タイポ/票の陰影）。
- 0016 act4: 「Printed on cards. Recited at arrest.」カードが印刷され壁にテープ留め→定着（police_badge/警察署）。
- 0017 act4: 力の移譲＝閉じた取調室の扉が開く（`Doors`1枚開＋`LightSweep`）。
- 0018 act4: 「Retried — convicted again.」逆転→再審→再有罪＝独房（jail_cell_bars/prison_corridor）。寄りで余白。
- 0019 act4: 「Mirandaのためでなく“次の人”のため」空き椅子に次の人物の含意。
- 0020 act4【実写】現代の逮捕b-roll（crime_police 実写・数秒切替）。
- 0021 ending: 「Structural — not set dressing.」総括＝あなたの“自分の言葉”に引かれた線。
- 0022 ending: 名を与えた男は刑務所へ＝独房の余韻（payoff）。
- 0023 ending: 「Next: who gets a lawyer?」次回(Gideon)への引き＋タイトル示唆。
- 0024 ending【実写/CTA】「Subscribe」CTAボタン＋`BrandEndcard` へブリッジ。
> ※`Vote` は 5–4 のまま（改変不要）。実在人物（Ernesto Miranda・Earl Warren・Harlan/White 等）の肖像は**一切出さない**（象徴・シルエット・手・後ろ姿・タイポのみ）。長尺SPNは約4.5秒ごとに別バリアントへ切替。

### 4. 自己確認（止まらない）
```
cd remotion && npm run studio   # → MirandaPremium
```
演出（山場0012の5–4＋出典確定／0009の4ケース統合／0013の4警告点灯）・4部・約12分・**字幕とテロップ非重複**・**実在人物の肖像が無い**・タイポ過多になっていない を自分で確認。OKなら次へ。

### 5. ナレーション（ElevenLabsで生成OK・課金気にせず）
`script.en.v001.md` の `[VO:]` を ElevenLabs 生成（**課金承認待ち不要**）。
- ドラフト → `H:\pd-media\episodes\PD-2026-001-miranda\06_voice\draft\VC-XXXX.mp3`、マスター → `…\06_voice\master\VC-XXXX.mp3`。索引 → `06_audio/narration_index.v001.json`。`MirandaPremium` にナレ連結。

### 6. 音＆字幕（VIDEO_RULES §11/§13）
- BGM(Suno)＋SFX＋環境音をダッキング（−14LUFS/TP≤−1）。取調室＝低トーン＋clock_tick、山場0012＝reveal系＋gavel/low_boom/stamp_seal。
- **字幕＝forced alignment でナレと“ぴったり同期”**（語単位・一字一句一致・ズレ≤約120ms）→ `08_edit/captions.v001.srt`(+.json)。見やすさ仕様厳守・非重複。音源は `H:\pd-media\library\`。

### 7. サムネ（CTR最大化が選定基準・止まらない）
`THUMB-01..06` を **CTR最大化の観点**（高コントラスト/単一明快な主被写体/感情・葛藤/タイトル余白/モバイル可読/ブランド配色/正確さ）で評価し最強の1枚を自動選定。`thumb_prompts.v001.md` の**タイトル3案(A/B/C)を全部** `ThumbnailFrame` で 1280×720 書き出し → `10_thumbnail/`、メタ＋各案CTR評価 → `09_package/title_thumbnail_candidates.v001.json`。全候補を残しA/B差し替え可。

### 8. 最終レンダー
```
cd remotion && npm run render MirandaPremium out/miranda_premium.mp4 --crf=14
```
CPU/libx264・1920×1080・30fps・NVENC不可。
- 最終 → `H:\pd-media\episodes\PD-2026-001-miranda\08_edit\miranda_premium_v001.mp4`。QC（尺≒12分/−14LUFS/字幕同期/肖像なし/タイポ過多でない）→ `08_edit/renders/final.v001.qc.json`。

### 9. パッケージ（pd-package・差し替え用メタ）
タイトル(A/B/C)/説明/チャプター/字幕/タグ/権利マニフェスト/`youtube_meta` を `09_package/`（新リビジョン）に作成。商用OK・実在人物の肖像なし・AI開示を `rights_manifest` で確認。**ここで停止し「新動画 完成・差し替え準備OK」を完成動画＋パッケージのパス付きで報告。**

### 10.【唯一のSTOP＝旧動画の差し替え/公開】※オーナーのみ・破壊的
**公開済みの旧第1話を差し替える操作（旧動画の非公開化/削除＋新規アップロード、または再アップロード）は、オーナーが完成動画を確認した後に、オーナー操作/承認でのみ実行**（invariant 2・公開動画の削除/非公開化＝破壊的・承認境界）。Codexは自動で越えない。

> 各ステップでコミット（`H:\pd-media` と `remotion/public` はGit管理外。軽量成果物のみ）。

---

## ノンストップ運用
- 手順0〜9はオーナー確認を挟まず一気に通す。詰まっても止めず自分で判断して進め、最後にまとめて報告。
- 止まるのは手順10（旧動画の差し替え/公開）だけ。承認なしに越えない。
- 例外で即STOP：台本/claimsの重大な事実誤り、権利・**実在人物の肖像リスク**（Miranda/Warren/判事を描いてしまう恐れ）。

## この話の厳守
- **中立**（公共安全 vs 個人の権利のどちらにも寄らない）。多数意見（Warren）と反対意見（Harlan/White）を公平に。
- **実在人物・判事の肖像なし**（象徴・シルエット・タイポで代替）。ディープフェイク不可。AI画像は必ず開示（`ReconLabel`）。一般ストックは「事件の実物」として提示しない。
- **台本・claims 不改変**。旧アニマティック資産は消さず残す（差し替えはレンダー成果物で行う）。

## 最初のアクション
手順0（SDXL 103枚生成）から開始 → 0b（サムネ6案）→ 1〜9をノンストップ実行（取り込み→ファクトリ→MirandaPremium→自己確認→ナレ→音/字幕→CTRサムネ→最終レンダー→パッケージ）→ 手順10の手前で停止して「新動画 完成・差し替え準備OK」を報告。
