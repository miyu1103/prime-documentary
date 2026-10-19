# Codexプロンプト — 第14話(Lange v. California) **仕上げ／FINISH編**（画像生成は完了済み）

> このブロックを丸ごと Codex スレッドに貼る。EP14の**右側工程のうち「画像より後ろ＝編集→音→レンダー→パッケージ」**だけを実行する完成専用プロンプト。
> （シーン計画〜画像生成は完了済み。シーン計画段階からやり直すための旧版は `codex_prompt_ep14.md`。）

---

あなたは Codex です。Prime Documentary リポジトリ（branch `claude/vibrant-archimedes-2mmr5h`）で作業します。
**着手前に必ず**次を読む：`CLAUDE.md` / `episodes/_planning/EP6-8_HANDOFF.md` / `episodes/_planning/VIDEO_RULES.md`（§4・§10〜13）/ `docs/motion-design-language.md` / `docs/motion-quality-gate.md` / `references/README.md`。
作業前に `git fetch` → `git pull --rebase --autostash`（並行クラウドワーカーが居る）。各ステップ完了ごとに commit + push。**SSD実体メディア（`H:\pd-media`）と `runs/` は絶対にコミットしない。**

## 0. 現在地（重要）
- 台本＝**完成・承認済み(APR-0001)・`script_verified`・ロック**。本文 `[VO:]` は**一字一句変更禁止**。
- **AI画像＝生成完了**（`H:\pd-media\assets\ai\lange\SPN-XXXX*.png`、1スパン複数バリアントあり）。
- **実写stock＝DL・権利確認済み**（`H:\pd-media\episodes\PD-2026-014-lange\stock\*.mp4` ／割り当ては `asset_map.v001.md`）。
- **サムネ候補＝生成済み**（`H:\pd-media\assets\ai\thumbs\lange\` ＋ `10_thumbnail\thumbnail.lange_option_A/B/C`）。
- → **あなたの仕事＝ここから先：素材ステージング → ナレ生成 → `LangePremium.tsx` 実装 → 字幕 → 音4層ミックス → ファクトリ加飾 → 品質ゲート → 最終レンダー → パッケージ。**
- 停止点は **YouTubeアップロード/公開の直前のみ**（中間の確認待ちで止まらない＝ノンストップ運用 VIDEO_RULES §8）。重大な事実誤り・権利リスク・BANリスクを見つけた時だけ即STOPして日本語で報告。

## 1. 正典（この4つが設計の真実。矛盾時はこの順で優先、勝手に解釈しない）
1. `episodes/PD-2026-014-lange/08_edit/edit_design.v001.md` … **仕上げ設計書（§1 4部構成／§2 全23ショットの“意味あるアニメ”／§3 テロップ・字幕・出典レイアウト／§4 品質ゲート／§5 編集ポリシー／§6 LangePremium実装方針＋ショット→部品割当／§7 ファクトリ三層加飾／完成定義チェックリスト）**。← **最重要・実装はこれに従う。**
2. `06_audio/audio_cue_sheet.v001.md` … 音4層＋ダッキング＋章別キュー＋実在音源ファイル名。
3. `04_scenes/shotlist.v001.json` … 23ショット・各 `estimated_seconds`・素材種別・テロップ（尺の基準＝合計≒619.6秒）。
4. `04_scenes/asset_map.v001.md` … 各SPNの使用ファイル（✅実写／🎨AI画像／🔤文字グラフィック）。
- 読むだけ（変更禁止）：`03_script/script.en.v001.md`・`script.annotated.v001.json`・`01_research/claims.v001.json`・`manifest.json`。

## 2. 絶対に侵さない不変条項（NEGOTIABLE禁止）
1. **★評決表記**：「**9–0＝判決（破棄差戻し／vacate & remand）の全員一致**」であって「**全員一致の“意見”ではない**」。**Roberts（＋Alito）は結論同意だが、より広い hot-pursuit 立入ルールを主張**＝Kagan法廷意見と両論を**公平に**。本編・テロップ・サムネ・字幕すべてで取り違えない。`Vote` 流用時は9マス全点灯＋テキスト `"9–0"`＋注記 `"in judgment"`。
2. **争点は「軽犯罪での逃走の追跡で、令状なく自宅に立ち入れるか」**であって **DUIの有罪/無罪ではない**（SPN-0006で明示）。California の主張も“悪役化”せず一立場として中立提示。住居プライバシー vs 警察の安全はどちらにも肩入れしない（映像でも音でも煽り過ぎない）。
3. **実在人物の肖像なし**（Arthur Lange／各判事＝Kagan/Roberts/Alito 等）。象徴的表現のみ。ディープフェイク不可。AI画像は全て **AI開示＋rights manifest登録＋ブランド準拠**。
4. ファクトリ/ストックは一般素材。**「Langeの自宅」「当該パトカー」等の“実物”として提示しない**（symbolic/illustrative のみ）。権利は商用OK・license=allowed のみ。1点ずつ「出典URL・作者・ライセンス・取得日・使用シーン・sha256」をrights台帳に記録。
5. **台本/claims/shotlist 不改変**（Read専用）。誤りを見つけたら直さずSTOP報告。
6. 課金API・公開はオーナー承認＋冪等キー＋予算チェックなしに実行しない。ただし**ナレ生成（ElevenLabs）は生成OK＝この話では課金承認待ち不要・止まらず進める**（VIDEO_RULES §8／§11）。

## 3. 仕上げパイプライン（この順で実行・各ステップ後にcommit+push）

### STEP A — 素材ステージング（Remotion public へ）
- AI画像 `H:\pd-media\assets\ai\lange\SPN-XXXX*.png` → `remotion/public/lange/`、実写 `…\stock\*.mp4` → `remotion/public/lange/stock/` へコピー。
- `sceneImages('s..')` 相当のヘルパでスパン毎のバリアント連番を束ねる。長尺スパン（**SPN-0015=50秒・0011=38秒・0009=38.4秒・0017=33.6秒・0014=32.8秒・0006=32.8秒**）は **約4.5秒ごとに別カット/別バリアントへ切替**して静止・長居を避ける（edit_design §2末尾）。
- 実素材が足りないスパンは仮を置かず**STOP報告**（`coded/cards = 0` を守る）。

### STEP B — ナレ生成（ElevenLabs・止まらない）
- `script.en.v001.md` の `[VO:]` を **そのまま** ElevenLabs へ → draft `H:\pd-media\episodes\PD-2026-014-lange\06_voice\draft\VC-XXXX.mp3` → master `…\06_voice\master\VC-XXXX.mp3`。
- 計画/索引(git)：`06_audio/voice_plan.v001.json` / `narration_index.v001.json` を実値で更新。発音注意は annotated の pronunciation メモに従う（"Lange"・"Sonoma"・"594 U.S. 295"＝"five ninety-four U-S two ninety-five" 等を確認）。
- ナレ生成ゲートでは停止しない。

### STEP C — `LangePremium.tsx` 実装（★本丸・edit_design §6/§2 に厳密準拠）
- **`remotion/src/compositions/LangePremium.tsx` を新規作成**。雛形＝`CarpenterPremium.tsx`（主）、参照＝`RileyPremium.tsx`/`MadoffPremium.tsx`。汎用 `RoughCut` は**使わない**（意味あるアニメが出ない）。`RoughCut-lange` は下見用に残してよいが**最終書き出しは `LangePremium`**。
- 再利用部品（新規実装を最小化）：
  - `components/Motion.tsx`：`MovingStage`（カメラ＋粒子＋光）/`Particles`/`LightSweep`/`Vignette`/`CameraRig`。**全カットに映画的カメラ（寄り引き/パララックス＋イージング・リニア禁止）**。
  - `components/Grain.tsx`：`Grain`。`components/Bookends.tsx`：`BrandOpening`/`BrandEndcard`（`OPENING_SEC`/`ENDCARD_SEC`）。
  - `components/SceneArt.tsx`：`visualMode="map"`（USマップ＋ピン波紋）/`"timeline"`（年表マーカー）/`motifHint="scales"|"gavel"|"document"|"seal"|"court"`。
  - `CarpenterPremium.tsx` 内のビズを必要分コピー移植：`SceneShell`（多画像Ken Burns＋光＋粒子＋下部テロップ `Lower`＋`ReconLabel`）/`Vote`/`MapGrid`/`TwoColumn`/`Doors`/`BigNumber`/`CourtColumns`/`Boundary`/`Triptych`。
  - **`Vote` を 9–0 用に改修**（現状 `i<5`＝5–4固定／テキスト"5–4"）：**全9マス点灯＋テキスト"9–0"＋注記"in judgment"**。または `VoteUnanimous` を `LangePremium` 内に新規。SPN-0013で使用。
- **ショット→実装の割り当ては edit_design §6 の表をそのまま実装**（要点）：
  - 0001 ガレージ扉＋足が止まる瞬間＝実写`<Video>`＋`Vignette`/`Grain`、カット頭＝足の瞬間。
  - 0002 `"warrant required"` 下線強調＝AI画像＋`SceneShell`。
  - 0003 Sonoma ロケーター＝`SceneArt visualMode="map"`（ピンが落ちて地名描画）。
  - 0005 扉の下の足＝立入＝実写`<Video>`、短く速い。0006 `"ENTRY"` 強調＋`"the DUI"` 取り消し線（`whoosh_short`同期）。
  - 0007 `any flight = automatic entry` の等式/矢印が組み上がる（州主張）。
  - 0009 exigency 3アイコン（danger/evidence/escape）順次フェード＝`Doors`。0022 軽犯罪の振れ幅（assault↔noise）ラベルスライド。
  - 0011 `TwoColumn`（左 "Don't let suspects escape" / 右 "Don't gut the home"）＋背後に天秤 `motifHint="scales"`。
  - **0013（山場）**＝`SceneArt visualMode="timeline"`（2021へ）＋`VoteUnanimous`(9–0・"in judgment")＋`motifHint="seal"`（594 U.S. 295）。`LightSweep` 色=**GOLD**。“ため→開放”をSFX同期。
  - 0014 `TwoColumn`（"A FACTOR" / "NOT A TRIGGER"・trigger側に×）。0023 年表が過去（コモンロー）へ遡る＋巻物/印章。
  - 0015 同じ結論→だが理由分岐の二股線＋`motifHint="court"`（Roberts+Alitoを公平に明示）。0016 押印＋下級審へ戻る矢印（`stamp_seal`同期＝Vacated & remanded）。
  - 0018 `Boundary`（揺れる境界線・ラベル "CASE-BY-CASE"）。0020 系譜を点で連結（Terry→Riley→Carpenter…→自宅）。0021 予告タイポ→`BrandEndcard`（Subscribe）。
- **4部構成（edit_design §1）**：①フック（本編priority Aハイライト約10カット・各1〜2秒の高速集＝**新規制作しない**・候補＝0001/0005/0013/0014/0015/0016/0023/0020/0021/0006）約30秒 → ②`BrandOpening` → ③本編 act1–4（SPN-0001〜0023・約9.5分） → ④エンディング（SPN-0019〜0021・約75〜90秒）→ `BrandEndcard`。
  - 尺目標 **約12分（11.5〜12.5分）**。`TOTAL_SEC` は shotlist 実値（≒619.6秒）＋オープニング/エンドカード＋幕間の“ひと呼吸”（0013リビール後の余韻）で寄せる。間延びさせず密度で（カット切替≒4.5秒維持）。
- `Root.tsx` に `<Composition id="LangePremium" .../>` を登録（ハイフン無し）。`npm run studio` で目視確認。

### STEP D — 字幕（forced alignment・edit_design §3）
- ナレ全文を語単位で強制アライン（`gen_captions_forced.py` 系）→ `08_edit/captions.v001.srt`(+`.json`)。**ズレ≤約120ms・一字一句一致**。
- 見やすさ（VIDEO_RULES §13）：48〜60px・本文太字・白＋濃い縁取り/影＋半透明黒帯(55〜70%)・最大2行・中央寄せ・下部安全帯。
- **3者を位置で分離**：字幕=下部安全帯／テロップ(on_screen_text)=上・中央／出典(金ライン `Lange v. California, 594 U.S. 295 (2021)`)=右下固定。一度も被らせない。

### STEP E — 音4層ミックス＋ダッキング（audio_cue_sheet 準拠）
- 4層＝**VO（最優先）/ BGM（章ごと1曲）/ SFX / ambience**。音源は `H:\pd-media\library\`（`music_registry.v001.json`/`sfx_registry.v001.json`）。
- 章別キューは cue sheet §2の表どおり（フック=`tension_build`→`hook`／act1=追跡の緊張／act2=`explainer_bed`／act3=`tension_build`→**`reveal`(0013山場)**／act4=`somber`／ending=`outro`）。
- **決定的ビート**：SPN-0001/0005「扉の下の足＝立入」に `soft_impact`+`sub_drop`。SPN-0013 9–0リビールに `gavel_knock`+`low_boom`、出典確定/0016押印に `stamp_seal`。各テロップ出現にSFX同期。
- **ダッキング必須**：VOサイドチェインでナレ区間 BGM −16〜−18dB / ambience −26〜−30dB、ナレ頭16フレーム前に先行ダッキング。整音 **−14 LUFS(integrated) / true peak ≤ −1 dBTP**、VOが常に明瞭。**9–0を“意見の全員一致”と誤認させる音演出をしない**（中立）。

### STEP F — ファクトリ三層加飾（edit_design §7・過剰回避）
- DL済みファクトリ棚（`assets/asset_manifest.v001.json`／`FACTORY_INVENTORY.md`）から**トーン（黒/紺/青/金）に合うものだけ** `scripts/select_factory_assets.py` で抽出 → `remotion/public/lange/factory/`。
- 三層＝**背景プレート(bg・薄く下地)＋light/particle/vfxオーバーレイ(screen/add)＋texture(overlay)**。**意味あるアニメ（コード演出）が主役・ファクトリは加飾**（1カット1〜2レイヤ・主役を食わない）。割当は §7.2 の表（**実在subtypeのみ**＝`front_door_house`/`police_strobe_red_and_blue`/`headlights_in_rain`/`courtroom_interior`/`balance_scale_brass`/`us_constitution_document`/`empty_parking_garage` 等）。
- 山場 SPN-0013 は `police_strobe` を使わず **GOLD系 `LightSweep`＋上品なvfx**。license=allowed のみ・出典/sha256記録。

### STEP G — 品質ゲート（書き出し直前に全✓・edit_design「完成定義」）
1つでも未達なら書き出さない：
- [ ] 4部構成（フック→BrandOpening→本編act1–4→エンディング→Endcard）
- [ ] `coded/cards = 0`（全23ショットが実写/AI画像/図解で充填・空カードなし）
- [ ] 全カットが動く（静止画ゼロ・Ken Burns一辺倒でない・映画的カメラ）
- [ ] 字幕＝語単位同期(≤120ms)・一字一句一致、字幕/テロップ/出典が位置分離で非重複
- [ ] 音4層＋ダッキング・−14 LUFS / TP≤−1、扉の足ビート＆9–0リビールにSFX
- [ ] **9–0表記が正確**（判決の全員一致≠意見の全員一致／Roberts+Alitoの別意見を公平に・`Vote`は9マス全点灯+"9–0"+"in judgment"）
- [ ] 中立・実在人物の肖像なし・争点は立入であってDUIでない・台本/claims/shotlist 不改変
- [ ] ファクトリ三層加飾が実在subtype・allowed・記録済み・主役を食わない
- [ ] 約12分（11.5〜12.5分）

### STEP H — 最終レンダー → パッケージ → STOP
- **書き出し＝`LangePremium`**（quality-first・**CPU/libx264**・NVENCに切替えない）→ `H:\pd-media\episodes\PD-2026-014-lange\08_edit\renders\final\`。
- 既存 review-proxy パッケージ（`09_package\`）を本番版へ更新：`youtube_meta` / `chapters` / `tags` / `rights_manifest`（全AI画像・ファクトリ・stockを登録）/ `final_delivery` / サムネ選定。タイトルは仮 `"Can a Police Officer Follow You Into Your Own Home?"`、サムネは A/B/C から提案（評決表記を侵さない）。
- `manifest.json` の state/active_revisions/artifacts(checksum) を新revisionで更新（承認済みは上書きせず新版）。
- **ここでSTOP**：`OWNER_REVIEW_REQUEST` を更新し、初号レビュー動画・タイトル/サムネ・最終ナレ公開可否・公開スケジュールの**オーナー承認待ち**（APR-0002〜0005）。**アップロード/公開/スケジュールは絶対に実行しない。**

## 4. 最初のアクション
正典4つ＋ロック入力＋handoff＋VIDEO_RULES/motion-design を読み、**実装に入る前に**「STEP A〜H の実行計画＋4部構成のタイムライン（各章→ショット→使用素材種別→画面テキスト→尺）＋9–0表記と中立の遵守方針」を**日本語の短い要約**でオーナーレビュー用に投稿。その後ノンストップで STEP A→H を進め、STEP H 末尾のオーナー承認ゲートでのみ停止する。
