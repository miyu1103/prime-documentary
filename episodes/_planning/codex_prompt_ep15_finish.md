# Codex 超巨大プロンプト — 第15話(Theranos / United States v. Holmes) **完成編・SERIES FINALE**

> このブロックを丸ごと Codex スレッドに貼る。第15話を **`08_edit/edit_design.v002.md`（＝完璧な設計書・正典）** に厳密に従って**最終動画まで完成**させるための、self-contained な完成専用プロンプト。
> **正典は edit_design.v002。** 本プロンプトと設計書が食い違ったら **edit_design.v002 を優先**。台本/claims/shotlist は Read専用・不改変。
> **本話は R3（存命の有罪確定者 Holmes/Balwani）＝法的高リスク。** 公開前に法務レビュー必須。評決表記の不変条項（§2）を1つでも侵したら即STOP・日本語報告。
> **★QCを自分で true と書くのは禁止。** 最終は必ず独立検証 `scripts/check_final_acceptance.py 15 --render <final.mp4>` の **RESULT: PASS（exit 0）** を関門にする。
> **★出荷基準の正典＝`docs/PD_ONE_PASS_PRODUCTION_SPEC.v1.md`（ONE-PASS PRODUCTION SPEC v1）。** BGM/声/字幕/改行/画質/Max品質/素材活用/アニメ/フック/4部構成/サムネ/タイトルCTR の全失敗モードが「仕様＋ゲート」で固定されている。最初のレンダーから同表を満たし、`check_final_acceptance.py` が exit 0 になるまで完成としない。未コードの行（画像≥3840・素材活用）はスペック§Cどおり手動測定で0違反。

---

あなたは Codex です。Prime Documentary リポジトリ（branch `claude/vibrant-archimedes-2mmr5h`）で作業します。
**着手前に必ず読む**：`CLAUDE.md`（不変項2/6/11/12/13）/ `episodes/PD-2026-015-theranos/08_edit/edit_design.v002.md`（**正典・全節**）/ `episodes/_planning/VIDEO_RULES.md`（§4・§6・§8・§10〜13）/ `docs/motion-design-language.md` / `docs/motion-quality-gate.md` / `docs/audio-sfx-bgm-library-plan.md` / `.claude/rules/16-approval-boundaries.md`。
作業前に `git fetch` → `git pull --rebase --autostash`（並行クラウドワーカーが居る）。各ステップ完了ごとに commit + push。**SSD実体メディア（`H:\pd-media`）と `runs/` は絶対にコミットしない。**

---

## 0. 現在地（2026-06-27時点・重要：ゼロからではない）

- **台本＝完成・承認済み(APR-0001)・`script_verified`・ロック**。`03_script/script.en.v001.md` の `[VO:]` は**一字一句変更禁止**。
- **★ナレ＝ElevenLabs本番生成 完了（このプロンプトで再生成しない＝二重課金禁止）**。
  - master: `H:\pd-media\episodes\PD-2026-015-theranos\06_voice\master\vc_master_v001.mp3`（**実VO合計 556.16秒**・チャンネル共通の声 `nPczCjzI2devNBz1zQrb`）
  - 索引(git): `06_audio/narration_index.v001.json`（**provider=ElevenLabs**・25チャンク・各VCの `section/start/end/seconds`）
  - 章別チャンク → §3 STEP A の表参照。**視覚の再タイミングはこの実チャンク尺で行う**（shotlist推定612.4sではない）。
- **AI画像＝生成完了**（`H:\pd-media\assets\ai\theranos\SPN-XXXX*.png`・1スパン複数バリアント）。
- **shotlist / asset_map / ai_prompts / thumb_prompts＝あり**（`04_scenes/`）。サムネ候補も生成済み（`H:\pd-media\assets\ai\thumbs\theranos\THUMB-01..06.png` ＋ `10_thumbnail/`）。
- **`TheranosPremium.tsx`＝現状は汎用 `CasePremiumFromRoughCut` のラッパー**（＝§6の専用演出 VerdictBoard/ValuationGraph 等は**未実装**）。review-proxy v003 は SAPI音声・BGMなし・10.42分で**不適合**（捨てる）。
- → **あなたの仕事＝STEP A〜H**：①視覚を bespoke `TheranosPremium` に作り込む（§6）②実VOに再タイミング＋7秒フック＋幕間で 11.5〜12.5分 ③BGM4層ミックス ④字幕 ⑤ファクトリ加飾 ⑥独立ゲートPASS ⑦最終レンダー ⑧パッケージ → **STEP H のオーナー承認＋R3法務レビューでのみ停止**。

### ★14話(lange)の5失敗を絶対に繰り返さない（オーナー実視聴の指摘・実測で確認済み）
14話の“最終”は実物が **①声がSAPIプロキシ ②最終字幕なし ③黒画面=画像が出ない（連続58秒の黒）④フックから始まる4部構成でない ⑤BGM(音楽)なし（無音109秒＝ナレだけ）** だったのに、QC json に `four_part/all_shots_filled/captions/4層=true` と**手書きで true**にされ素通りした。**設計書(cue sheet/edit_design)に書いてあっても、実レンダーに適用されていなければ不合格。** 最終は §3 STEP F の独立ゲート（実ファイルを機械測定＝声/字幕/画像/BGM/尺）の PASS を必須にする。

---

## 1. 正典（矛盾時はこの順で優先・勝手に解釈しない）
1. `08_edit/edit_design.v002.md` … **仕上げ設計書 v002（最重要・全節）**。§1＝尺の拘束バジェット＋実測補正／§1.1＝14話の教訓／§2＝全24ショットの“意味あるアニメ”／§3＝テロップ・字幕・出典レイアウト／§4＝独立受け入れゲート＋品質ゲート／§5＝R3編集ポリシー／§6＝**TheranosPremium実装＋ショット→部品割当**／§7＝ファクトリ三層加飾／完成定義。
2. `06_audio/audio_cue_sheet.v001.md` … 音4層＋ダッキング＋**章別BGM/ambience/SFXの実ファイル名**。
3. `06_audio/narration_index.v001.json` … **実VOチャンク尺（再タイミングの基準）**。
4. `04_scenes/shotlist.v001.json` / `asset_map.v001.md` … 各SPNの素材種別・テロップ・使用ファイル（**尺は実VO優先**・素材割当はこれ）。
- 読むだけ（変更禁止）：`03_script/script.en.v001.md`・`script.annotated.v001.json`・`01_research/claims.v001.json`・`manifest.json`。

---

## 2. 絶対に侵さない不変条項（R3・NEGOTIABLE禁止。1つでも侵したら即STOP・日本語報告）
1. **★評決表記（最重要・load-bearing）**
   - **投資家詐欺の4件＝有罪（GUILTY）は判決事実として断定してよい**（1件 conspiracy＋3件 wire fraud／2022-01-03 評決）。
   - **患者関連＝無罪（ACQUITTED / not guilty）**。**3件＝評決不成立（mistrial / no verdict）**。**この2つを絶対に「有罪」と書かない・言わない・色やテロップで示唆しない。**
   - **無罪 ≠ 潔白／無罪 ≠「技術は機能した」**（CLM-0010）。「合理的疑いを超える立証に至らなかった」だけ。
   - **意図・認識は陪審／裁判所に帰属**させ、ナレーター（チャンネル）が断定しない。
   - `VerdictBoard` は **4件のみ GUILTY 点灯**・患者は ACQUITTED・3件は NO VERDICT を**別色**で。GUILTY表記を患者/3件側に出さない。
2. **数字・事実の正確さ**：Holmes 量刑＝**135か月＝約11年3か月**。Balwani＝別裁判で**全12件有罪（患者含む）・約155か月＝ほぼ13年**。ピーク評価額＝**約90億ドル(~$9B)**。**Walgreensは限定展開（主にアリゾナ）＝全米と示唆しない**。SEC 2018＝**民事・認否なし和解**（有罪の自認ではない）。
3. **実在人物の肖像なし**（Holmes/Balwani 等）。**ディープフェイク不可・実写人物不可**。雑誌表紙・記者の顔・実機(Edison)・実ロゴ・特定本社/施設を出さない＝**象徴的・一般化**のみ。AI画像は全て **AI開示（`symbolic reconstruction` ラベル常時）＋rights manifest登録＋ブランド準拠**（不変項11）。
4. ファクトリ/ストックは一般素材。**「Theranosの実物・実機・本社」等として提示しない**（symbolic/illustrative のみ）。R3＝**実在人物を想起させる素材は使わない**。商用OK・license=allowed のみ。1点ずつ「出典URL・作者・ライセンス・取得日・使用シーン・sha256」を `05_stock/stock_ledger.v001.json` に記録。
5. **中立**：「失敗 or 詐欺」に肩入れしない。検察主張・弁護主張・評決を公平に。崩落/破壊の過剰演出で詐欺側に寄せない。
6. **台本/claims/shotlist 不改変**（Read専用）。誤りを見つけたら直さず**STOP報告**。
7. 課金API・公開はオーナー承認＋冪等キー＋予算チェックなしに実行しない。**ナレは生成済みなので追加生成しない**（master を使う）。新たな課金が要るとき(画像再生成等)は最小限＋idempotency。

---

## 3. 完成パイプライン（STEP A〜H・各ステップ後に commit + push）

### STEP A — bespoke `TheranosPremium.tsx` を実装（★本丸・edit_design §6/§2 に厳密準拠）
- **現状の汎用ラッパーを置き換え**、`remotion/src/compositions/TheranosPremium.tsx` を **bespokeコンポジションに作り直す**。雛形＝`CarpenterPremium.tsx`（主）、参照＝`MadoffPremium.tsx`。**汎用 `CasePremiumFromRoughCut` / `RoughCut` は使わない**（§6の意味あるアニメが描画されない）。`THERANOS_ROUGHCUT` はステージング下見用に残してよいが、**最終書き出しは bespoke `TheranosPremium`**。
- **再利用部品（新規実装を最小化・実在確認済み）**
  - `components/Motion.tsx`：`MovingStage`/`Particles`/`LightSweep`/`Vignette`/`CameraRig`（**全カットに映画的カメラ＝寄り引き/パララックス＋spring/ease・リニア禁止**）。
  - `components/Grain.tsx`：`Grain`。`components/Bookends.tsx`：`BrandOpening`/`BrandEndcard`（`OPENING_SEC=3.5`/`ENDCARD_SEC=9`）。
  - `components/SceneArt.tsx`：`visualMode="timeline"`（年表マーカー）/`motifHint="scales"|"gavel"|"document"|"court"`（天秤/小槌/書類＋印章/法廷）。
  - `CarpenterPremium.tsx` 内のビズをコピー移植：`SceneShell`（多画像Ken Burns＋光＋粒子＋`Lower`＋`ReconLabel`）/`TwoColumn`/`Doors`/`BigNumber`/`Boundary`/`Triptych`/`Vote`。
  - **新規小コンポ2つ**（SVG/CSS・$0・実在人物を描かない専用ビズ）：
    - **`VerdictBoard`**（`Vote` を改変）：2022/1/3 count-by-count で **投資家詐欺4件 GUILTY を1件ずつ金ラインで確定**→続いて **患者=ACQUITTED・3件=NO VERDICT を別色**で。GUILTY表記を患者/3件に出さない。山場 SPN-0013→0014。
    - **`ValuationGraph`**：評価額が **~$9B へ上昇→$0 へ崩落**。SPN-0001/0005/0010 で使用。
- **ショット→実装の割り当ては edit_design §6 の表をそのまま実装**（要点）：0001 一滴の血＋ValuationGraph崩落／0002 矢印「国家→個人」反転／0003 timeline 2003／0023 Doors(著名肩書き)＋虫眼鏡縮小／0004 一滴 vs 採血針・黒箱／0005 ValuationGraph(~$9B)＋ロゴ壁＋Walgreens限定／0007 timeline 2015 調査報道／0008 自社機→他社機 TwoColumn＋差替／0010 timeline 2018 SEC和解(認否なし)→解散・$9B→0／0011 Failure vs Fraud TwoColumn／0012 詐欺=欺く意図 定義カード＋天秤／0024 検察 vs 弁護 TwoColumn／**0013 timeline 2022→VerdictBoard 4件GUILTY（山場・GOLD `LightSweep`）**／0014 VerdictBoard 続き ACQUITTED/NO VERDICT 別色／0015 無罪≠潔白 TwoColumn＋Balwani全12件／0016 BigNumber「~11y 3m」／0017 “Fake it…”標語＋"usually legal"／0018 境界の等式 `Boundary`／0019 アプリ損失 vs 検査の損失 TwoColumn／0020 Triptych シリーズ総括／0022 Subscribe CTA。
- **章順**（§1注記・台本順に再配列）：shotlist は span_id 昇順だが、**SPN-0023(act1) は 0005 と 0006 の間**、**SPN-0024(act3) は 0012 と 0013 の間**。長尺スパンは**約4.5秒ごとに別カット/別バリアントへ切替**（静止・長居しない）。
- **4部構成＋尺（§1 実測補正後）**。実VO=556.16s。窓 **690〜750秒（狙い約700〜710秒＝11.7分）**。VOが短い分、尺は主に幕間と余韻で作る：
  | 部 | 内容 | 秒 |
  |---|---|---|
  | ① フック | 本編ハイライト **約3〜4カットの短いtease**＋riser SFX（**約7秒・punchy・長尺化しない＝オーナー指定**）。新規制作しない。候補=0001(血+$9B→$0)/0013(4件有罪ボード)/0016(量刑)。VO断片0〜1個 | 7 |
  | ② ブリッジ→Opening | riser余韻→`BrandOpening` | 1.5＋3.5 |
  | ③ 本編(VO 556s ＋ 間) | VC-0001〜0025 を **実チャンク尺(narration_index)で配置**＋**幕間"ひと呼吸"×6（各約10〜12秒・ナレなしhold＋音楽）＋山場の余韻(0013→0014 約15秒)＋主要グラフの間(評価額崩落/4件count-up/等式 計約20秒)** で **合計約120〜130秒**を足す | ≈680 |
  | ④ `BrandEndcard` | 既存 | 9 |
  | | **合計** | **≈700〜710秒＝11.7分 ✓** |
  - **増やす尺はすべてナレを足さない**（hold＋音楽＋既存VO断片のみ）。間延びさせず密度で（カット切替≒4.5秒）。R3：間/余韻/フックで断定有罪の含意を足さない。
- `Root.tsx` の `TheranosPremium` 登録を維持（`id="TheranosPremium"`・ハイフンなし）。`durationInFrames` を新尺(実VO＋間)に合わせて更新。`npm run studio` で目視確認。

### STEP B — 音声（再生成しない・masterを使う）
- ナレ master `vc_master_v001.mp3`（556.16s・ElevenLabs）を**そのまま使用**。**ElevenLabs を再度叩かない。**
- VOチャンク章割り当て（narration_index・再タイミングと音楽配置の基準）：
  - HOOK段落 VC-0001(0–27.7s) ／ OPENING VC-0002(28–64s) ／ ACT I VC-0003〜0007(64–169s) ／ ACT II VC-0008〜0012(169–261s) ／ ACT III VC-0013〜0019(261–428s, **0013–0014が評決山場**) ／ ACT IV VC-0020〜0022(428–491s) ／ ENDING VC-0023〜0025(491–556s)。
- ※映像の「①フック montage(7s)」は VO本編より前。VOのHOOK段落(VC-0001)は**本編の冒頭**であって montage ではない（取り違えない）。

### STEP C — 字幕（forced alignment・新VOで作り直し・edit_design §3）
- master VO を語単位で強制アライン → `08_edit/captions.v001.srt`(+`.json`)。**ズレ≤約120ms・台本と一字一句一致**。proxy字幕は使わない（`captions.review_proxy.*` は破棄）。
- Remotion用に `remotion/src/data/theranos_captions.ts` の `THERANOS_CAPTIONS` を**新VOのキューで再生成**（build_kelo_audio_v001.py の `write_captions()` がキュー→.ts を書く実装。これを theranos 用に流用）。
- 見やすさ（VIDEO_RULES §13）：48〜60px・本文太字・白＋濃い縁取り/影＋半透明黒帯(55〜70%)・最大2行・中央寄せ・下部安全帯。
- **3者を位置で分離**：字幕=下部安全帯／テロップ(on_screen_text)=上・中央／出典(金ライン 例 `United States v. Holmes (N.D. Cal.) — verdict Jan 3, 2022` / `SEC charges 2018 (settled, no admission)`)=右下固定。AI画像に `symbolic reconstruction` ラベル常時。一度も被らせない。

### STEP D — BGM 4層ミックス＋ダッキング（★BGMなし失敗の解決・audio_cue_sheet 準拠）
- **`scripts/build_kelo_audio_v001.py` を雛形に `scripts/build_theranos_audio_v001.py` を作成**（4層＝VO/BGM/SFX/ambience を ffmpeg で合成。`build_music()`/`build_ambience()`/`build_sfx()`/ducking の構造を流用）。音源棚＝`H:\pd-media\library\`（`music/<mood>/`・`ambience/amb_*.mp3`・`sfx/sfx_*.mp3`／`music_registry.v001.json`/`sfx_registry.v001.json`）。
- **★BGMは全編“常時鳴らす”**（ナレの合間も帯が途切れない）。cue sheet §2 の章別 mood の実ファイルを敷く：
  - フック=`tension_build`→`hook`／act1=`explainer_bed`／act2=`tension_build`／act3=`tension_build`→**`reveal`(0013 `verdict_at_dawn`・山場)**／act4=`somber`／ending=`outro`。境界は STEP B の章タイミング(VC start/end)に合わせる。
- **ダッキング必須**：VOサイドチェインでナレ区間 BGM −16〜−18dB / ambience −26〜−30dB、ナレ頭16フレーム前に先行ダッキング。整音 **−14 LUFS / true peak ≤ −1 dBTP**、VOが常に明瞭。
- **決定的SFX同期**：$9B→$0崩落に `soft_impact`+`sub_drop`、**SPN-0013 評決4件確定に `gavel_knock`+`low_boom`（“ため→開放”）**、出典/0016量刑確定に `stamp_seal`。各テロップ出現にSFX。
- 出力＝**完全ミックス master**（VO＋BGM＋SFX＋amb・ダッキング済）を `H:\pd-media\episodes\PD-2026-015-theranos\06_voice\master\theranos_mix_v001.mp3` に。`TheranosPremium` の音声入力をこの mix に向ける（`narrationSrc`/`<Audio>` を mix に）。**R3：音演出で断定有罪・患者被害の断定を足さない（中立）。**

### STEP E — ファクトリ三層加飾（edit_design §7・過剰回避・R3）
- DL済みファクトリ棚（`assets/asset_manifest.v001.json`／`FACTORY_INVENTORY.md`）から**トーン（黒/紺/青/金）に合うものだけ** `scripts/select_factory_assets.py --theme <…>` で抽出 → `remotion/public/theranos/factory/`。
- 三層＝**背景プレート(bg・薄く)＋light/particle/vfx(screen/add)＋texture(overlay)**。**意味あるアニメ（コード演出）が主役・ファクトリは加飾**（1カット1〜2レイヤ）。割当は §7.2 の表（実在subtypeのみ＝`modern_medical_lab`/`balance_scale_brass`/`courtroom_interior`/`stock_chart_crashing_red`/`documents_on_desk` 等）。
- 山場 SPN-0013 は `god_rays`＋`smoke_on_black`＋`LightSweep`色=**GOLD** で“ため→開放”。**R3：実在人物想起素材・実機・実ロゴ・雑誌表紙は不可。** license=allowed のみ・出典/sha256 を `05_stock/stock_ledger.v001.json` に記録。

### STEP F — 独立受け入れゲート（★書き出し前後に必ず・自己申告QC禁止）
**実ファイルを機械測定する独立検証を関門にする**：
```
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 15 --render <final.mp4>   # RESULT: PASS / exit 0 必須
./.venv/Scripts/python.exe scripts/check_runtime_band.py <final.mp4>                    # 690-750s
```
PASSすべき hard チェック（FAILなら最終にしない＝原因を直して再書き出し）：
- [ ] `voice_is_master`：ElevenLabs本番（既に narration_index=elevenlabs。mixがmaster由来であること）。
- [ ] `captions_final`：非proxy `captions.v001.srt` が存在し尺の90%以上カバー。
- [ ] `images_present`：長い黒画面なし（全カットに絵）。
- [ ] `bgm_present`：**BGMの帯が常時**（無音合計≤25s。ナレだけ＝不可）。
- [ ] `runtime_band`：690〜750秒。
人手目視の併用（edit_design §4/完成定義）：4部構成／`coded/cards=0`／全カット映画的カメラ（静止画ゼロ）／字幕・テロップ・出典・`symbolic reconstruction`が位置分離で非重複／**評決の区別が正確（4件GUILTY可・患者ACQUITTED・3件NO VERDICT・無罪≠潔白・意図は陪審/裁判所に帰属）**／実在人物の肖像/実写/ディープフェイクなし／ファクトリ実在subtype・allowed・記録済み／中立・不改変。

### STEP G — 最終レンダー → パッケージ
- **書き出し＝bespoke `TheranosPremium`**（quality-first・**CPU/libx264**・NVENCに切替えない）→ `H:\pd-media\episodes\PD-2026-015-theranos\08_edit\renders\final\theranos_premium_final_v001.mp4`。例：`cd remotion && npx remotion render TheranosPremium <out.mp4> --codec=h264 --crf=16`（既存話の書き出し設定に合わせる）。
- **書き出し後に STEP F の2スクリプトを再実行し PASS を確認**。FAILなら原因(声/字幕/画像/BGM/尺)を直して再書き出し。acceptance の JSON 出力を `08_edit/renders/final.v001.acceptance.json` に保存し、**QC json の数値はこの独立測定の結果を転記**（手書きの true を作らない）。
- パッケージ（`09_package/`）を本番版へ更新：`youtube_meta`/`chapters`/`tags`/`rights_manifest`（全AI画像・ファクトリ・stock・**ナレ provenance**を登録）/`final_delivery`/サムネ選定。タイトル仮 `"When Does a Bold Promise Become a Crime? The Rise and Fall of Theranos"`、サムネは THUMB-01..06／A-C から提案（**評決表記・R3を侵さない**）。
- `manifest.json` の state/active_revisions/artifacts(checksum) を**新revision**で更新（承認済みは上書きせず新版＝不変項6）。events.jsonl に記録。

### STEP H — STOP（オーナー承認＋R3法務レビュー・ここでだけ止まる）
- **必ずSTOP**。`OWNER_REVIEW_REQUEST` を更新し、以下の**オーナー承認待ち**（アップロード/公開/スケジュールは**絶対に実行しない**）：
  - APR-0002 初号レビュー動画(exact hash)／APR-0003 タイトル・サムネ／APR-0004 最終ナレ公開可否／**APR-0005 専用の法務/権利レビュー（R3・不可侵）**／APR-0006 公開・スケジュール。
- **R3：法務レビュー記録(exact revision/hash)が無い限り `publish_approved` へ進めない**（不変項2／`.claude/rules/16`）。`09_package/legal_rights_review_packet` を最終ハッシュで更新。

---

## 4. 最初のアクション（実装前に必ず投稿）
正典（特に `edit_design.v002.md` 全節）＋ロック入力＋`narration_index.v001.json`＋VIDEO_RULES/motion-design/audio-library を読み、**実装に入る前に**次を**日本語の短い要約**でオーナーレビュー用に投稿：
1. STEP A〜H の実行計画。
2. **4部構成の尺タイムライン**（フック→Opening→本編 act1–4(各VC start/end＋幕間/余韻)→Ending→Endcard）で **合計が690〜750秒に入ることを数値で示す**（実VO556s＋間≈120〜130s）。
3. §6 の bespoke 実装方針（`VerdictBoard`/`ValuationGraph` 新規＋CarpenterPremium流用部品）。
4. **評決表記/中立/R3（肖像なし・法務レビュー）の遵守方針**と、STEP F 独立ゲートで PASS を取る計画。
その後ノンストップで STEP A→G を進め、**STEP H のオーナー承認＋R3法務レビューゲートでのみ停止**する。重大な事実誤り・権利/法務リスク・BANリスクを見つけた時のみ即STOPして日本語報告。
