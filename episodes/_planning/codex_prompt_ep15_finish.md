# Codexプロンプト — 第15話(Theranos / United States v. Holmes) **仕上げ／FINISH編・シリーズ最終回**

> このブロックを丸ごと Codex スレッドに貼る。EP15の**右側工程の“完成”**専用プロンプト。
> **重要：15話はゼロからではない。** `TheranosPremium.tsx` も review-proxy 動画(v003)も**既に存在**する。あなたの主タスクは「**既存の約10.42分の構成を、新しい仕上げ設計 v002 の尺バジェット通りに作り直して 11.5〜12.5分の窓に入れ、字幕・音・加飾・パッケージを本番品質で完成させる**」こと。
>
> **★14話(lange)の失敗を繰り返さない（オーナー実視聴の指摘）。** 14話の“最終”は実物が **①声がいつものElevenLabsでなくSAPIプロキシ声 ②最終字幕なし ③黒画面=画像が出ていない（実測で連続58秒の黒）④フックから始まる4部構成でない** という不適合だったのに、QC json には `four_part_structure/all_shots_filled/captions_burned_in=true` と**手書きで true**にされて素通りした。**QCを自分で true と書くのは禁止。** 最終は必ず独立検証スクリプト `scripts/check_final_acceptance.py`（実ファイルを機械測定）の **PASS** を関門にする（§3 STEP F/G）。
> **本話は R3（存命の有罪確定者）＝法的高リスク。公開前に法務レビュー必須。** 表現の不変条項（後述§2）を1つでも侵したら即STOP・日本語報告。

---

あなたは Codex です。Prime Documentary リポジトリ（branch `claude/vibrant-archimedes-2mmr5h`）で作業します。
**着手前に必ず**読む：`CLAUDE.md`（特に不変項2・6・11・12）/ `episodes/_planning/VIDEO_RULES.md`（§4・§6・§8・§10〜13）/ `docs/motion-design-language.md` / `docs/motion-quality-gate.md` / `.claude/rules/16-approval-boundaries.md`。
作業前に `git fetch` → `git pull --rebase --autostash`（並行クラウドワーカーが居る）。各ステップ完了ごとに commit + push。**SSD実体メディア（`H:\pd-media`）と `runs/` は絶対にコミットしない。**

## 0. 現在地（重要）
- 台本＝**完成・承認済み(APR-0001)・`script_verified`・ロック**。本文 `[VO:]` は**一字一句変更禁止**。台本/claims/shotlist も Read専用。
- **AI画像＝生成完了**（`H:\pd-media\assets\ai\theranos\SPN-XXXX*.png`、1スパン複数バリアントあり。proxy v003 で `SPN-0012`/`SPN-0020` の一部画像を差し替え済み）。
- **実写stock／ファクトリ素材＝DL・権利確認済み**（割り当ては `04_scenes/asset_map.v001.md` と `08_edit/edit_design.v002.md §7.2`）。
- **`TheranosPremium.tsx`＝実装済み**（`VerdictBoard`/`ValuationGraph` 等の専用ビズ含む）。**review-proxy v003＝書き出し済み**だが **624.96秒＝10.42分** で、標準の 11.5〜12.5分に**届いていない**（フックと幕間の“ひと呼吸”が未実装）。← **ここを直すのが今回の主目的。**
- **サムネ候補＝生成済み**（`H:\pd-media\assets\ai\thumbs\theranos\THUMB-01..06.png` ＋ `10_thumbnail\`）。
- → **あなたの仕事＝尺の作り直し → ナレ本番化(ElevenLabs) → 字幕 → 音4層 → ファクトリ加飾 → 品質ゲート → 最終レンダー → パッケージ。** 停止点は**オーナー承認ゲート（§3 STEP H）だけ**。重大な事実誤り・権利/法務リスク・BANリスクを見つけた時のみ即STOPして日本語報告。

## 1. 正典（設計の真実。矛盾時はこの順で優先・勝手に解釈しない）
1. `episodes/PD-2026-015-theranos/08_edit/edit_design.v002.md` … **仕上げ設計書 v002**。**§1＝尺の拘束バジェット表（最重要）／§1.1＝なぜ尺が足りなくなるか／§2＝全24ショットの“意味あるアニメ”／§3＝テロップ・字幕・出典レイアウト／§4＝品質ゲート／§5＝R3編集ポリシー／§6＝TheranosPremium実装＋ショット→部品割当／§7＝ファクトリ三層加飾／完成定義**。← **実装はこれに従う。v001 は参照しない（v002が最新）。**
2. `06_audio/audio_cue_sheet.v001.md` … 音4層＋ダッキング＋章別キュー＋実在音源ファイル名。
3. `04_scenes/shotlist.v001.json` … 24ショット・各 `estimated_seconds`・素材種別・テロップ（本編の尺基準＝合計≒612.4秒）。
4. `04_scenes/asset_map.v001.md` … 各SPNの使用ファイル（✅実写／🎨AI画像／🔤グラフィック）。
- 読むだけ（変更禁止）：`03_script/script.en.v001.md`・`script.annotated.v001.json`・`01_research/claims.v001.json`・`manifest.json`。

## 2. 絶対に侵さない不変条項（R3・NEGOTIABLE禁止。1つでも侵したら即STOP）
1. **★評決表記（最重要・load-bearing）**：
   - **投資家詐欺の4件＝有罪（GUILTY）は判決事実として断定してよい**（1件 conspiracy ＋ 3件 wire fraud／2022-01-03 評決）。
   - **患者関連＝無罪（ACQUITTED / not guilty）**。**3件＝評決不成立（mistrial / no verdict）**。**この2つを絶対に「有罪」と書かない・言わない・色やテロップで示唆しない。**
   - **無罪 ≠ 潔白（acquittal ≠ exoneration）／無罪 ≠「技術は機能した」**（CLM-0010）。「合理的疑いを超える立証に至らなかった」だけ。
   - **意図・認識は陪審／裁判所に帰属**させ、ナレーター（チャンネル）が断定しない。
   - 評決ボード（`VerdictBoard`）は **4件のみ GUILTY 点灯**・患者は ACQUITTED・3件は NO VERDICT を**別色**で。GUILTY表記を患者/3件側に出さない。
2. **数字・事実の正確さ**：Holmes 量刑＝**135か月＝約11年3か月**。Balwani＝**別裁判で全12件有罪（患者関連含む）・約155か月＝ほぼ13年**。ピーク評価額＝**約90億ドル（~$9B）**。**Walgreens は限定展開（主にアリゾナ）＝全米展開と示唆しない**。SEC 2018＝**民事・認否なし和解**（有罪の自認ではない）。
3. **実在人物の肖像なし**（Holmes／Balwani 等）。**ディープフェイク不可・実写人物不可**。雑誌表紙・記者の顔・実機(Edison)・実ロゴ・特定本社/施設を出さない＝**象徴的・一般化**のみ。AI画像は全て **AI開示（`symbolic reconstruction` ラベル常時）＋rights manifest登録＋ブランド準拠**（不変項11）。
4. ファクトリ/ストックは一般素材。**「Theranosの実物・実機・本社」等として提示しない**（symbolic/illustrative のみ）。R3＝**実在人物を想起させる素材は使わない**。商用OK・license=allowed のみ。1点ずつ「出典URL・作者・ライセンス・取得日・使用シーン・sha256」を `05_stock/stock_ledger.v001.json` に記録。
5. **中立**：「失敗 or 詐欺」に肩入れしない。検察主張・弁護主張・評決（有罪/無罪/評決不成立）を公平に。崩落/破壊の過剰演出で詐欺側に寄せない。
6. **台本/claims/shotlist 不改変**（Read専用）。誤りを見つけたら直さず**STOP報告**。
7. 課金API・公開はオーナー承認＋冪等キー＋予算チェックなしに実行しない。ただし**ナレ生成（ElevenLabs）は生成OK＝この話でも課金承認待ち不要・止まらず進める**（VIDEO_RULES §8／§11）。

## 3. 仕上げパイプライン（この順で実行・各ステップ後にcommit+push）

### STEP A — 尺の作り直し（★今回の主目的・edit_design.v002 §1 のバジェットを厳密実装）
現行 proxy v003 は **本編612.4s＋オープニング3.5s＋エンドカード9s＝624.9s（10.42分）** で、フックと幕間が無いため窓に届かない。§1の表どおり**不足分の約90秒を既存素材のみ**で足して **690〜750秒（狙い≈715秒＝11.9分）** に入れる：
- **① フック（30秒・最低25秒以上）**＝本編の山場 約10カット（各1〜2秒）の高速ハイライト＋riser SFX。**新規制作しない**（既存本編映像＋既存VO断片の流用）。候補＝`SPN-0001`(一滴の血＋$9B→$0)/`0008`(他社機で検査)/`0013`(2022・4件有罪の評決ボード)/`0014`(患者無罪・3件評決なし)/`0015`(無罪≠潔白／Balwani全12件)/`0016`(量刑~11y3m)/`0012`(詐欺＝欺く意図)/`0024`(検察vs弁護)/`0002`(最終回の問い)/`0021`(総括への引き)。**R3：フックで断定有罪の含意や患者=有罪の誤読を作らない。** 最後は無音ぎみ→`BrandOpening` へブリッジ(約2秒)。
- **② 幕間の“ひと呼吸”×4（各約8秒・計32秒）**＝act1→2 / 2→3 / 3→4 / 4→ending の転換に**ナレなしの held ビジュアル＋音楽スウェル**。
- **③ 山場の余韻（約8秒）**＝評決ボード確定後（`SPN-0013`→`0014`）の“ため→開放”。
- **④ 主要グラフの間（計約12秒）**＝評価額 $9B→$0 崩落の着地／4件 count-up／境界の等式の組み上がりに小さな held。
- **⑤ CTA hold（約6秒）**＝`SPN-0022` Subscribe を少し長く持つ。
- 増やす尺は**すべてナレを足さない**（held＋音楽＋既存VO断片のみ）。**章順注意**（§1注記）：shotlistは`span_id`昇順だが、`SPN-0023`(act1)は`0005`と`0006`の間、`SPN-0024`(act3)は`0012`と`0013`の間に配置（台本順）。長尺スパン（**0012=45s・0015=43s・0002=40s・0020=36s**）は**約4.5秒ごとに別カット/別バリアントへ切替**して静止・長居を避ける。
- 実装は `TheranosPremium.tsx` を拡張（フック/幕間/余韻の `kind` を持つ scene を追加）。`Root.tsx` の `theranosPremiumDurationInFrames` 等を新尺に合わせて更新。**汎用RoughCutでは出ない演出なので必ず `TheranosPremium` で**。

### STEP B — ナレ本番化（ElevenLabs・止まらない）
- proxy は Windows SAPI のローカル音声。**最終は ElevenLabs マスターへ差し替える**：`script.en.v001.md` の `[VO:]` を**そのまま** ElevenLabs → draft `H:\pd-media\episodes\PD-2026-015-theranos\06_audio\draft\VC-XXXX.mp3` → master `…\06_audio\master\VC-XXXX.mp3`。
- 計画/索引(git)：`06_audio/voice_plan.v001.json` / `narration_index.v001.json` を実値で更新（proxy版とは別 revision）。発音注意：`Theranos`／`Holmes`／`Balwani`／`Carreyrou`／`Edison`／`Walgreens`／`Stanford`／数字（"135 months"＝"one hundred thirty-five months" 等）。
- ナレ生成ゲートでは停止しない。**公開可否(APR-0004)は後段のオーナー承認**で、生成自体は進める。

### STEP C — 字幕（forced alignment・edit_design §3）
- 本番ナレ全文を語単位で強制アライン → `08_edit/captions.v001.srt`(+`.json`)。**ズレ≤約120ms・一字一句一致**。
- 見やすさ（VIDEO_RULES §13）：48〜60px・本文太字・白＋濃い縁取り/影＋半透明黒帯(55〜70%)・最大2行・中央寄せ・下部安全帯。
- **3者を位置で分離**：字幕=下部安全帯／テロップ(on_screen_text)=上・中央／出典(金ライン 例 `United States v. Holmes (N.D. Cal.) — verdict Jan 3, 2022` / `SEC charges 2018 (settled, no admission)`)=右下固定。AI画像に `symbolic reconstruction` ラベル常時。一度も被らせない。

### STEP D — 音4層ミックス＋ダッキング（audio_cue_sheet 準拠）
- 4層＝**VO（最優先）/ BGM（章ごと1曲）/ SFX / ambience**。音源は `H:\pd-media\library\`（`music_registry.v001.json`/`sfx_registry.v001.json`）。
- 章別キューは cue sheet §2の表どおり。**決定的ビート**：$9B→$0 崩落に `soft_impact`+`sub_drop`、**SPN-0013 評決ボード確定に `gavel_knock`+`low_boom`（“ため→開放”同期）**、出典確定に `stamp_seal`。各テロップ出現にSFX同期。
- **ダッキング必須**：VOサイドチェインでナレ区間 BGM −16〜−18dB / ambience −26〜−30dB、ナレ頭16フレーム前に先行ダッキング。整音 **−14 LUFS / true peak ≤ −1 dBTP**、VOが常に明瞭。**R3：音演出で断定有罪・患者被害の断定を足さない（中立）。**

### STEP E — ファクトリ三層加飾（edit_design §7・過剰回避・R3）
- DL済みファクトリ棚（`assets/asset_manifest.v001.json`／`FACTORY_INVENTORY.md`）から**トーン（黒/紺/青/金）に合うものだけ** `scripts/select_factory_assets.py` で抽出 → `remotion/public/theranos/factory/`。
- 三層＝**背景プレート(bg・薄く)＋light/particle/vfxオーバーレイ(screen/add)＋texture(overlay)**。**意味あるアニメ（コード演出）が主役・ファクトリは加飾**（1カット1〜2レイヤ）。割当は §7.2 の表（**実在subtypeのみ**＝`modern_medical_lab`/`balance_scale_brass`/`courtroom_interior`/`stock_chart_crashing_red`/`documents_on_desk` 等）。
- 山場 SPN-0013 は `god_rays`＋`smoke_on_black`＋`LightSweep`色=**GOLD** で“ため→開放”。**R3：実在人物想起素材・実機・実ロゴ・雑誌表紙は不可。** license=allowed のみ・出典/sha256記録。

### STEP F — 品質ゲート（書き出し直前に全✓・edit_design「完成定義」）
**★最初に独立受け入れゲートを実行（自己申告QC禁止）**：`./.venv/Scripts/python.exe scripts/check_final_acceptance.py 15 --render <final.mp4>` が **RESULT: PASS（exit 0）** であること。これは実ファイルを測定し **声(ElevenLabs本番か／SAPI proxyでないか)・最終字幕の有無・黒画面=画像なし・尺** を機械検出する（14話の二の舞防止）。**QC json に true を手書きして通すのは不可。** 以下は人手目視の併用チェック：
- [ ] **【声・不可侵】最終音声＝ElevenLabs本番ナレ**（STEP Bで生成したmaster）。proxyのWindows SAPI声で書き出していない。`check_final_acceptance.py` の `voice_is_master` PASS。
- [ ] **【字幕・不可侵】最終字幕（非proxy `captions.v001.srt`）が存在し全編同期**・焼き込み/サイドカー。`captions_final` PASS。
- [ ] **【画像・不可侵】全カットに絵がある**（黒画面/空カードなし）。`images_present` PASS。
- [ ] **【尺・不可侵】最終実尺＝690〜750秒（11.5〜12.5分）**。`check_runtime_band.py <final.mp4>` または acceptance の `runtime_band` が **PASS**（`duration_positive` だけのPASSでは不可）。
- [ ] **フックが25秒以上**の実montage＋幕間“ひと呼吸”×4・山場の余韻が §1 バジェット通り組み込まれている。
- [ ] 4部構成（フック→BrandOpening→本編act1–4→エンディング→Endcard）。
- [ ] `coded/cards = 0`（全24ショットが実写/AI画像/図解で充填・空カードなし）。
- [ ] 全カットが動く（静止画ゼロ・Ken Burns一辺倒でない・映画的カメラ＝寄り引き/パララックス＋spring/ease、リニア禁止）。
- [ ] 字幕＝語単位同期(≤120ms)・一字一句一致、字幕/テロップ/出典/`symbolic reconstruction`ラベルが位置分離で非重複。
- [ ] 音4層＋ダッキング・−14 LUFS / TP≤−1、$9B→$0 崩落＆9–0…ではなく**4件有罪リビール**にSFX同期。
- [ ] **★評決の区別が正確**（投資家詐欺4件＝GUILTY可／患者＝ACQUITTED／3件＝NO VERDICT・「有罪」表記なし／無罪≠潔白／意図は陪審・裁判所に帰属）。数字（$9B・4件・約11年3か月・Balwani全12件~13年・Walgreens限定）正確。
- [ ] 中立・**実在人物の肖像/実写/ディープフェイクなし**・台本/claims/shotlist 不改変。
- [ ] ファクトリ三層加飾が実在subtype・allowed・記録済み・主役を食わない・**実在人物想起素材なし**。

### STEP G — 最終レンダー → パッケージ
- **書き出し＝`TheranosPremium`**（quality-first・**CPU/libx264**・NVENCに切替えない）→ `H:\pd-media\episodes\PD-2026-015-theranos\08_edit\renders\final\`。**書き出し後に `scripts/check_final_acceptance.py 15 --render <final.mp4>` を再実行し RESULT: PASS（exit 0）を確認**。FAILなら最終としない＝原因（声/字幕/画像/尺）を直して書き出し直す。その出力(JSON)を `08_edit/renders/final.vNNN.acceptance.json` として保存し、QC json の数値は**この独立測定の結果を転記**する（手書きの true を作らない）。
- 既存 review-proxy パッケージ（`09_package\`）を本番版へ更新：`youtube_meta` / `chapters` / `tags` / `rights_manifest`（全AI画像・ファクトリ・stockを登録）/ `final_delivery` / サムネ選定。タイトルは仮 `"When Does a Bold Promise Become a Crime? The Rise and Fall of Theranos"`、サムネは THUMB-01..06／A-C から提案（**評決表記・R3を侵さない**）。
- `manifest.json` の state/active_revisions/artifacts(checksum) を**新revision**で更新（承認済みは上書きせず新版＝不変項6）。

### STEP H — STOP（オーナー承認 ＋ R3法務レビュー・ここでだけ止まる）
- **ここで必ずSTOP**：`OWNER_REVIEW_REQUEST` を更新し、以下の**オーナー承認待ち**にする（アップロード/公開/スケジュールは**絶対に実行しない**）：
  - APR-0002 初号レビュー動画（exact hash）／ APR-0003 タイトル・サムネ ／ APR-0004 最終ナレ公開可否 ／ **APR-0005 専用の法務／権利レビュー（R3・本話の不可侵ゲート）** ／ APR-0006 公開・スケジュール。
- **R3：法務レビュー記録（exact revision/hash）が無い限り `publish_approved` へ進めない**（CLAUDE.md 不変項2／§3 高リスク承認／`.claude/rules/16`）。`09_package/legal_rights_review_packet` を最終ハッシュで更新し、レビュー対象を明示する。

## 4. 最初のアクション
正典4つ（特に `edit_design.v002.md §1`）＋ロック入力＋VIDEO_RULES/motion-design を読み、**実装に入る前に**「STEP A〜H の実行計画＋**4部構成の尺タイムライン（各章→ショット→使用素材種別→画面テキスト→秒）で合計が690〜750秒に入ることを数値で示す**＋評決表記/中立/R3（肖像なし・法務レビュー）の遵守方針」を**日本語の短い要約**でオーナーレビュー用に投稿。その後ノンストップで STEP A→G を進め、**STEP H のオーナー承認＋R3法務レビューゲートでのみ停止**する。
