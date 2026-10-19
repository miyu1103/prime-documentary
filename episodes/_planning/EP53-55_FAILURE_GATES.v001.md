# EP53-55 FAILURE GATES v001 — 全記録失敗カタログ → 拘束チェックリスト

- 対象: EP53 Norfolk Four / EP54 Curtis Flowers / EP55 Jon Burge（全話30分尺・オーナー指示）
- 現在地: 台本+音声=done、Codex画像生成中。以降 build→mix→render→package→ship が本書に拘束される。
- 作成: 2026-07-26。ソースは各項目末尾に `[...]` で明記（docs/、episodes/_planning/、memory 2系統）。
- 追記: 2026-07-28 — 新規失敗 **#53a（棚ラベル40%誤りのまま theme で素材選択）** を F節に追加し、STEP 3 を対応版に更新。実測ソース = `episodes/_planning/measurements/FACTORY_LABEL_AUDIT.v001.md`。
- 正典の親: `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（rows 1-16）＋ `docs/PD_EP32_POSTMORTEM_AND_ONE_PASS_PREVENTION.md` ＋ `docs/PD_SHIP_GATE.md` ＋ `.claude/rules/19-ship-gate.md`。本書はそれらの「EP53-55実行版」であり、緩和はしない（invariant 15）。

## STATUS 凡例
- **PASSED** = 本セッションで実測検証済み（プリプロ段階のみ）。
- **ARMED** = 既存の自動ゲートが build/preflight/acceptance/ship-lock で自動実行される（scripts/ に実在をGlob確認済み。配線はメモリ記録に基づく＝ビルド初回に1度だけ実配線をgrepで再確認すること）。
- **MANUAL** = 目視/試聴/手順の必須ステップ。担当と実施タイミングを明記。
- **GAP** = 機構が存在しない（正直に）。§GAPに最小実装案。

---

# 第1部 カタログ（工程別・通し番号）

## A. TOPIC / PLANNING（企画）

1. 題材重複 — EP46=Kelo/EP47=Mahanoy が EP10/11 と完全重複、基盤構築後に発覚・~6エージェント浪費 → 全在庫grep（slug＋事件名＋当事者名）を提案時に実施 → **PASSED**（EP53-55は28候補×EP1-52在庫で重複ゼロ確認済） [pd-topic-novelty-gate / pd-ep53-55-topic-slate]
2. 実在しない引用の混入 — EP53-55 R3で "By any measure, extraordinary" が捏造引用と判明（v002修正済） → R3独立レビューで全引用を一次ソース照合 → **PASSED**（3話ともR1/R2/R3計39欠陥修正済） [pd-ep53-55-topic-slate]
3. フックが8秒枠外 — EP54で R3 検出（修正済） → `check_planning_package.py` F-gate → **PASSED** [pd-ep53-55-topic-slate]
4. 尺不足の根本＝語数不足 — 実測178wpmに対し150wpm時代の語数のまま、38話中30話が自己申告ターゲット未達（titan 58分予定→35.5分） → `check_script_length.py`（preflight最初のチェック・課金前ブロック）＋30分帯=4,600-4,750語 → **PASSED**（EP53-55=4,645-4,696語・29-31分帯PASS。EP52の5,797語=LONG判定の教訓込み） [pd-runtime-shortfall-rootcause / pd-ep53-55-topic-slate]
5. R2/R3の安全ロックが下流成果物の後に発覚（EP23 自殺表現重複・"35 years"無限定） → 感情・死・存命者の扱いは台本段階でロック、公開前にオーナーR3最終レビュー → **PASSED**（台本段階）＋**MANUAL**（公開前R3レビュー=オーナー、予約実行前） [EP21-24_INCIDENT_RETRO_20260703 #1/#2]
6. 存命者・実在肖像リスク — EP54 Evans（存命DA）はSCOTUS動詞 "strongly suggests" 厳守済み。EP53-55とも存命者多数 → FACTS_LEDGERの動詞ロックを画面テキスト/サムネ/タイトルまで貫通 → **PASSED**（台本）＋**ARMED**（`verify_onscreen_text.py`=画面内数値のclaim照合）＋**MANUAL**（サムネ/タイトル文言はClaudeがship前に照合） [pd-ep53-55-topic-slate / feedback_prevent_by_mechanism]
7. 27-36分帯はデータ上弱い（Swartz 4.0%等）のに30分指示 — 矛盾はゲートでなく設計で解消：フック/再フック/開幕30秒を最優先設計 → **MANUAL**（Claude、ビルド時にretention設計を再確認。オーナー指示が正） [pd-analytics-2026-07 / spec v2 row16]

## B. SCRIPT（台本）

8. AI臭い文章（EP21-24 #8「いかにもAI」） → 3回レビュー（事実/クラフト/リテンション）＋`verify_script_lint.py` → **PASSED**（3本全文通読しAI臭3箇所駆除済：\"But here's the thing\"等）＋**ARMED** [pd-ep21-24-incident / feedback_pd_craft_directives / pd-ep53-55-topic-slate]
9. 水増し・paddingで尺を騙す（20分水増し/沈黙尾/言い換え反復） → `check_padding.py`（実音声尺 generated_seconds 優先） → **ARMED** [feedback_prevent_by_mechanism / reference_pd_finalize_and_gate_fixes]
10. 英語台本への日本語インライン注釈 → ナレ抽出が日本語含み行を丸ごと捨て、EP38でAct3感情の核~979字がVOから完全欠落 → 抽出文字数と原稿を必ずdiff、masterの文字起こしで欠落確認 → **MANUAL**（Claude、音声は生成済みなので build 開始時に narration_index 総語数 vs 台本語数を照合。乖離>2%で停止） [feedback_retro_ep38_kidsforcash]
11. 「正しいが退屈」な台本 → FILM_BIBLE/アカデミー脚本方式・コールドオープンの謎・2-3分ごと再フック → **PASSED**（DESIGN_ARCHITECTURE作成済・R2でクラフトpass実施） [spec v2 row15/16]
12. 反復7-gram等の言語的な癖 → `check_padding.py`＋script lint → **ARMED** [feedback-execution-style]

## C. AUDIO / TTS（音声）

13. SAPI声が本番に混入 — EP14（そもそもSAPIで出荷）、EP48（並行SAPIプロセスがnarration_indexを上書き、153/617チャンク汚染） → `check_narration_voice.py`（voice_id=Brian・source構造フィールド・尺±1s） → **ARMED**＋**MANUAL**（Claude、build開始時に3話のchunk sidecar voice_idを監査） [feedback_final_acceptance / feedback-thread-retro-20260723 ★]
14. indexゲートでは捕まらない第2のSAPIロック — EP48は `build_glover_bgm_real.py` にSAPI masterパスがハードコード（BGM工程が `-map 1:a` で全音声差し替え） → 各 `build_<slug>_bgm*.py` をgrep＋**最終動画のVOをvc_masterと相互相関（≥0.5=Brian、実測0.97-0.99）** → **MANUAL**（Claude、mux後・受領前に毎話実施）／自動化は**GAP**（§G-6） [feedback-thread-retro-20260723 ★★]
15. 声設定ドリフト（williams 237wpm等・正典=stability0.35/similarity0.80） → 生成スクリプトの設定値を正典と照合 → **MANUAL**（Claude、音声は生成済み→実測wpmを検算：総語数/master実尺が163-185wpmに入るか） [pd-runtime-shortfall-rootcause / feedback_start_from_canon_pipeline]
16. MP3多数連結の破損（EP50 \"invalid new backstep\"） → WAV中間で連結（gen_narration_centralpark系に実装済） → **ARMED**（クローン元に含む・生成済み音声のffprobe健全性確認は**MANUAL**） [pd-ep50-status]
17. ナレ自体が未生成（Codex CODEX_B・EP44/45） → vc_master 実在＋実尺＋chunk数を確認してから一切のbuild → **MANUAL**（Claude、build初手） [feedback-codex-codexb-unreliable]
18. **BGMが最終muxに無い** — EP14で無音109秒＝ナレのみ → `bgm_present`（無音>25s禁止・VO下でも-22LUFS可聴フロア）＋mux は `build_case_film_mux.py` の4層WAVのみ → **ARMED** [feedback_final_acceptance / spec v2 row1]
19. **EDのBGMがブツ切り** — 全音量チョップで終わる → `bgm_ending`ゲート＋曲はalign-to-endで枠に収める（尺は台本が主・伸縮禁止）＋末尾10秒の耳チェック → **ARMED**＋**MANUAL**（Claude試聴、受領前） [feedback_pd_craft_directives / feedback_prevent_by_mechanism]
20. **音量が低い/中盤で下がる** — ショートで繰り返し指摘（単一パスloudnormのポンピング＋integrated未達） → speechnorm＋グルー圧縮＋2パス静的-14LUFS（build_short_mix実装済）／長尺は4層ミックス-14LUFS＋`check_loudness`(-16〜-12) → **ARMED** [feedback_shorts_volume_consistency / spec v2 row6]
21. **無意味SFXフィラー** — EP32でゲート通過のためピコピコ326個投入（グッドハート） → フィラー恒久禁止・SFXは台本`(SFX:)`意味キューのみ・密度は本物で満たす → **ARMED**（build_case_film_audio）＋方針=ゲートを騙さない [PD_EP32_POSTMORTEM A1/C1 / feedback_keep_promises_no_gaming]
22. **変なSFX** — EP32終盤「飛行機みたいな音」（VO \"open road\"→roarベッド自動選択） → `FORCED_DEFAULT_CHAPTERS={\"ending\"}`＋roar/broadbandタグ回避＋自動選択ログの最終確認 → **ARMED**＋**MANUAL**（Claude、各章境界+終盤10秒を試聴、受領前） [feedback_anim_caption_polish #4 / PD_EP32_POSTMORTEM C3]
23. SFXの種類が少ない・違和感（Kurzgesagt/Veritasium水準に未達） → distinct SFX≥12＋意味タグ → **ARMED**（床のみ。`verify_sfx_manifest.py`はWEAK＝深い偽装耐性なし）＋質は**GAP**（§G-1） [feedback_prevent_by_mechanism / PD_EP32_POSTMORTEM C2]
24. 尊厳の静寂 — 情感カット（EP53自死・EP55拷問証言等）はnear-silent、装飾音禁止 → cue sheetで明示 → **MANUAL**（Claude、音design時） [feedback_sfx_meaningful_only]

## D. CAPTIONS（字幕）

25. **字幕とナレの不一致**（EP14/EP21-24の最重要実害#1） → 実音声から強制アライン（台本流用禁止）＋`caption_narration_match`（token一致100%級） → **ARMED** [pd-ep21-24-incident #1 / PD_SHIP_GATE]
26. **whisper長尺ドリフト** — EP32 v008で8:45以降+1.4〜2.8s遅れ。定数リードでは直らない → `align_windowed`（チャンク窓別whisper=ドリフト構造的に不能・medium.en）＋`verify_caption_sync.py` HARD（p90≤0.35/median≤0.10/区間ドリフト/late%） → **ARMED** [feedback_anim_caption_polish #2 / PD_EP32_POSTMORTEM B1/B3]
27. **変な所で途切れる字幕**（EP21-24 #2、旧_balanced_splitが「on the / floorboards」を割る） → `_smart_split`（機能語行末禁止）＋dangling=0許容 → **ARMED** [feedback_anim_caption_polish #3 / PD_EP32_POSTMORTEM B2]
28. dangling修正の副作用でcps回帰（EP35: 20→41） → cue間でテキストを動かす修正は必ず `check_caption_format`（≤2行/≤50字/≤27cps）を再実行してから確定 → **MANUAL手順**（Claude、字幕修正のたび） [feedback_retro_ep35_finalize_publish]
29. **字幕がレンダに焼かれていない** — EP36/EP38（SRTサイドカーは正常なのに映像に出ない、オーナーが発見） → `check_caption_integrity.py`（comp配線＋kinetic重複≤40%＋下部衝突なし） → **ARMED** [feedback-lessons-must-be-gates / feedback_retro_ep38_kidsforcash]
30. **4行字幕**（EP50） → ビルダー `_split_caption_text`（>84字を≤2行サブcueへ分割） → **ARMED**（builder既定・EP53-55ビルダーがクローン元から継承しているかbuild時にgrep） [feedback-thread-retro-20260725]
31. 字幕がデカい/黒箱/高すぎ（EP21/22/24）・カラオケ字幕却下（EP37） → 落ち着いたフレーズ字幕・中サイズ・低位置・黒箱なし・スマホで読めるサイズ → **MANUAL**（Claude、初回レンダのフレームでスマホ想定目視） [EP21-24_INCIDENT_RETRO #6 / feedback_retro_ep37_florence]
32. 字幕リード（遅れ体感） → CAPTION_LEAD 0.60s 早め寄り＋一律0.18s前倒しの実績レシピ → **ARMED**（既定値） [feedback_anim_caption_polish / reference_pd_finalize_and_gate_fixes]
33. 字幕ゲートがv001をハードコード → 修正はv001に上書き＋film.json.captions[]を1:1ミラー＋**字幕はfilm.jsonに焼くので再レンダ必須** → **MANUAL手順**（Claude） [reference_pd_finalize_and_gate_fixes]
34. verify_caption_syncの再検証は0.3秒キャッシュ → 高価な再レンダ前にSRTだけで反復検証 → **MANUAL手順**（Claude） [feedback_retro_ep35_finalize_publish]

## E. IMAGES（画像 — 今Codexが生成中の工程）

35. **画像が揃う前にbuild開始** — EP21(45枚欠)/EP22(74枚待ち3回)/EP23(42枚欠)でブロック連発 → 画像count+寸法preflightが通るまでrender/assembly進入禁止 → **MANUAL**（Claude、Codex納品受領時に3話とも全数照合） [EP21-24_INCIDENT_RETRO #5]
36. **Codexのスタブ納品** — EP50は動画630本中全部9KB黒スタブ・EP52はfactory 240中227が11KBスタブ（manifestは存在を宣言＝存在チェックは素通り）／EP54 flowersは7/25時点でS025以降カートゥーン反復破損の記録があったが、**2026-07-26にClaudeが現物を直接目視（S025/S030/S100=3/3良品・写実・ブリーフ整合）＝Codexが再生成済みと確認**。ただし全数監査は受領時に必ず実施 → 受領時にサイズ監査（`find -size -50k`）＋luma probe＋実サンプル目視。manifestの`is_stub:false`を信じない → **MANUAL**（Claude、受領時）／自動ゲート化は**GAP**（§G-2） [feedback-thread-retro-20260725 #1 / pd-shorts-52-59-scheduled / feedback-codex-codexb-unreliable]
37. **似た画像ばかりで飽きる**（EP50 #7） → プロンプト全ペアJaccardゲート`check_prompt_diversity.py`＋phash監視クラスタ → **PASSED**（プロンプト段階・3話PASS）＋**MANUAL**（受領画像でphash実測、Claude） [pd-ep53-55-topic-slate / feedback-thread-retro-20260725]
38. **人間の顔が全く出ない**（EP50 #6） → 人物入り画像を各話85枚(40%超)に設計済（object→human転換） → **PASSED**（プロンプト段階）＋**MANUAL**（受領時に人物比率実測） [pd-ep53-55-topic-slate]
39. 実在肖像・被害の直接描写 → 匿名人物のみ可・実在特定人物/暴行描写は禁止（invariant 11）・シルエットルール → **PASSED**（プロンプトに反映）＋**MANUAL**（受領時目視） [CLAUDE.md / feedback_pd_craft_directives]
40. 偽テキスト/偽印章（SDXL/KODAK罠 — 書類・新聞・ラベル系は必ず捏造文字が入る） → 表題面のない題材へ設計＋書類系画像は1枚ずつ目視 → **MANUAL**（Claude、受領時） [feedback_shorts_production_retro / pd-ctr-packaging-wave1]
41. 解像度不足 — EP35でCodex元1672px混入 → `image_resolution`ゲート（長辺≥3840）＋**render-truth: レンダが読む `remotion/public/<slug>/img/` 自体を4K化**（別ディレクトリだけ検証するのは不正直） → **ARMED**＋**MANUAL**（img/差し替え時） [reference_pd_finalize_and_gate_fixes / spec v2 row5]
42. 暗すぎて見えない画像（EP31 median46・EP32 F1） → `check_body_luma`（median YAVG≥48/暗フレーム率≤22%）＋`check_image_cut_luma.py` → **ARMED** [feedback_prevent_by_mechanism / PD_EP32_POSTMORTEM F]
43. 素のSDXL/FLUX-dev使用・長尺でのSDXL勝手起動（EP21-24 #9） → 長尺画像=Codexのみ（例外=修正/緊急追加にSD3.5/gen_max）・FLUX-dev成果物禁止 → **方針ARMED**（rule 19）＋**MANUAL遵守** [pd-ep21-24-incident #9 / feedback_image_quality_standard]
44. 権利未確認の外部素材DL（AST-0014/0017差し替え事故） → DL前に商用ライセンス確認 → **MANUAL**（Claude、素材追加時） [feedback_rights_check_before_download]
45. SDXL並走で低品質版が混入（EP50: 25/36低品質） → 生成プロセスは1本ずつ・skip guardは height≥2000 判定 → **MANUAL手順**（緊急ローカル生成時のみ） [feedback-thread-retro-20260725]

## F. FOOTAGE / STOCK（実写素材）

46. **DL素材が1つも使われない**（EP21-24 #3・EP32で未使用101件検出） → `check_footage_utilization.py` → **ARMED** [pd-ep21-24-incident #3 / feedback_prevent_by_mechanism]
47. **factory棚のラベル全面破損** — evidence_bag=カウボーイ、EP36の1カット目に「監視カメラ」ラベルの大聖堂、cows=\"documents_on_desk\"。機械ゲートでは意味不一致を検出不可（EP30は20/20緑でカウボーイ入り） → **staging後に必ずラベル付きコンタクトシート生成→全クリップ目視→BLOCK_IDS追記**（`build_footage_contact_sheet.py`）＋`check_visual_asset_qc.py`（レビュー済みQC manifestが無いとFAIL） → **ARMED**（QC manifest強制）＋**MANUAL**（目視そのもの=Claude、staging直後・初回レンダ前） [pd-factory-shelf-mislabeled / feedback-lessons-must-be-gates / retro-ep36-assembly]
48. 話内の素材使い回し（天秤クリップ乱用） → `footage_diversity`（distinct≥0.40/再利用≤4/汎用象徴≤2） → **ARMED** [feedback_footage_diversity / PD_SHIP_GATE]
49. 話またぎの素材被り（EP32で21件検出） → `check_arc_nonrepeat.py`（使用クリップ指紋の持ち越し）※EP53/54/55は連続予約想定＝3話相互でも実行 → **ARMED** [feedback_prevent_by_mechanism / feedback_footage_diversity]
50. featureless素材（素の霧/空/抽象）が浮く → staging時に除去 → **MANUAL**（コンタクトシート目視と同時） [pd-ep21-24-incident]
51. **実ストック0本**（EP50: H:/pd-media/assets/stock 74本を1本も未使用→紙芝居の一因） → stock-first: 実ストック＋i2v人物モーションを織り込む（inject/weaveスクリプト系） → **MANUAL**（Claude、film build時にstock使用数を数えて報告） [pd-footage-quality-fixes #4 / feedback-thread-retro-20260725]
52. 映像とナレの意味不一致（汎用B-roll流し込み） → scene_planで1文ごとに割当・語同期で接着・脈絡ない転換禁止 → **PASSED**（DESIGN_ARCHITECTURE段階）＋**MANUAL**（build時にscene_plan↔film.json対応を確認） [feedback_visual_narration_meaning_match]
53. arc_nonrepeatの偽陽性（共有 sNN.png 名で26枚を誤検出） → 画像はエピソードprefix命名 → **MANUAL手順**（build時） [feedback-ep38-retro #4/#5]
53a. **40%誤りのラベルで素材を選ぶ**（#47の上流・実測 FACTORY_LABEL_AUDIT.v001: claim付きラベルの **40.0%** が当該ファイル自身の復元プロバイダタイトルと矛盾・**17.5%** は確定誤り。目視40件で棚ラベルの的中は **52.5%**＝ブラインド選択はほぼ半分ハズレ。`select_factory_assets.py --theme` はファイル名から `theme_of()` でテーマを導いており、その40%そのもの＋substringバグ（`tree`⊂s**tree**t等で1,968件誤配）を抱えていた。実例: `evidence_bag`=革財布 / `courtroom_interior`=ベトナムのバス / `prison_corridor`=ハンブルクのエルベトンネル / `server_room_red_alert`=猫。※採番は末尾追番、節はF） → ①theme選択を監査済み台帳（`factory.jsonl` の `theme_recovered`＋`label_verdict`）へ切替＝新モジュール `scripts/factory_ledger_themes.py`（match優先→cross_theme復元分→weak、`cross_theme`は誤テーマ側から**不可視**化、`off_label`は `--allow-off-label` 時のみ最終手段、台帳欠落時は大警告付きでファイル名にフォールバック）②`factory_themes.theme_of()` を語境界一致に修正＋回帰テスト `scripts/tests/test_factory_themes.py`（street/lighthouse/warehouse/atmosphere/microphone）③選択・stagingは**必ず**ラベル付きコンタクトシートを出力し、生成失敗は exit 3 で選択自体を失敗させる → **ARMED**（台帳選択＋シート強制。`select_factory_assets.py` / `stage_case_factory_assets.py`）＋**MANUAL**（復元ラベルでも的中70%＝#47の全クリップ目視は今まで通り必須。tierが `cross_theme->here` / `off_label` のタイルは特に疑う） [FACTORY_LABEL_AUDIT.v001 / pd-factory-shelf-mislabeled]

## G. ANIMATION / MOTION（アニメ・動き）

54. **紙芝居**（EP21-24 #6、最頻出のオーナー激怒ポイント） → `animation_density`（near-still≤10%/hold≤3s）＋`check_animation_mix.py`（still-share≤45%・animated-coverage≥45%・>5s hold≤8・opening≤12s）＋`check_motion_density.py`（premium beats≥2.5/min・coverage≥25%・variety≥3） → **ARMED**（preflight＋acceptance両方） [pd-ep21-24-incident #6 / feedback-lessons-must-be-gates]
55. **ゲート緑でも「アニメまた少ない」**（EP30/31/28で3連発） → 知覚モーション予算をビルダーで先に確保：画像カットの≥40%にモーションtreatment・FigureBeats≥6・ヒーロー面≥2/章 → **MANUAL**（Claude、film build時に数値で確保→報告） [feedback_animation_still_too_little / feedback_perceptual_motion_and_verify]
56. **Ken Burnsだけ＝紙芝居のまま**（ズーム/パンは動きと認めない・オーナー明言） → 本物の動き=実写フッテージ＋i2v（SDXL→Wan2.2 TI2V-5B→RIFEの非破綻レシピ実証済）＋モーショングラフィック → **MANUAL**（build設計。動いてるかは連続フレーム差分で実測） [feedback_ken_burns_is_kamishibai / pd-footage-quality-fixes]
57. **ゆがみ/溶け（warp）** — EP48/49/50でオーナー指摘。真因=depth treatment（Three.js深度displacement） → treatments=`[\"bleed\",\"duotone\",\"focus\"]` のみ。**depth/scan/card は禁止**（builderレベルで修正済＝EP53-55ビルダーが継承しているか要grep） → **ARMED(builder)**＋**MANUAL検証**（build時grep＋初回レンダ目視）／warp自動検出は**GAP**（§G-3） [pd-footage-quality-fixes #1 / feedback-thread-retro-20260725]
58. **白っぽい曇り（haze）** — BodyGrade screen-wash 0.18が原因 → 0.07＋contrast1.14＋grain0.06 → **ARMED(コード修正済)**＋**MANUAL**（初回レンダで実フレーム確認） [pd-footage-quality-fixes #2]
59. **斜めスキャンライン** — DriftLightの~63°線テクスチャ → 撤去済 → **ARMED(コード修正済)**＋**MANUAL**（初回レンダ確認。バックカタログ7話に残存=別件） [pd-footage-quality-fixes #3 / pd-ep48-52-status]
60. **周回する淡い光**（EP32「使い過ぎ・うざい」＝freeze対策の装飾） → 円/lissajous周回光源は禁止・freeze床は単調等速で作る → **ARMED(撤去済)** [feedback_anim_caption_polish #1 / PD_EP32_POSTMORTEM E2]
61. **縦スイープ線・黄/金全画面ウォッシュ**（EP21-24で明示却下。WipeTransition/CameraRigは地雷部品） → 禁止リスト（ship gateに明記）・該当部品を使わない → **ARMED(方針)**＋**MANUAL**（目視1周で確認） [pd-ep21-24-incident / PD_SHIP_GATE]
62. **dochighlight＝バグに見える**（EP40黒帯/EP41砂時計/EP42黄箱、3回指摘→禁止） → film.jsonの figures[] に `\"kind\": \"dochighlight\"` が0件であることをgrep → **MANUAL**（Claude、film build直後）／preflightゲート化は**GAP**（§G-4） [pd-dochighlight-reads-as-bug]
63. **DATE_STAMP等の幻レイアウトでAEビルドがクラッシュ**（EP48/49） → `check_AE_layouts.py`（実装済みallowlist照合） → **ARMED** [feedback-thread-retro-20260723 / pd-ep50-status]
64. **figureスキーマ不正でレンダクラッシュ**（EP44/45: pins欠落・items vs data） → 全figureを FigureBeats.tsx のunion型と照合してからレンダ → **MANUAL**（Claude、film build後）／汎用ゲートは**GAP**（§G-5） [feedback-codex-codexb-unreliable]
65. **年号が \"2,001\" 表示**（atwater/tlo） → `check_year_grouping.py` → **ARMED** [feedback-thread-retro-20260723]
66. カウントアップ数値はsettleフレームで判定（中間フレームで誤読・EP41） → 目視はsettle時刻で → **MANUAL手順** [feedback-ep3941-eyeball-final-render]
67. キネティック文字の見切れ（EP40 NOBODY→\"NOBOD\"、punch scaleがoverflow:hidden内） → 3層分離＋対称マージン修正済／中央寄せ（EP32左見切れ根絶） → **ARMED(コード)**＋**MANUAL**（強調ビートのsettleフレーム目視） [feedback-ep3941-eyeball-final-render / feedback_prevent_by_mechanism]
68. LowerThird左端見切れ（EP32 E3） → 短スライド入場(-200px)＋パネルクリップ修正済 → **ARMED(コード)** [PD_EP32_POSTMORTEM E3]
69. 疎な図（2点地図）・暗い図背景（EP32 E4） → 図の要素密度・背景輝度の下限 → **GAP**（§G-7、目視で代替） [PD_EP32_POSTMORTEM E4/VI]
70. **静止ヒーロー動画がカットを覆い、ゲートFAILの真因になる**（EP34: 修正6連発ゼロ効果→フレーム1枚見て即判明） → 修正が効かない/byte一致なら**即・実ピクセル目視**（`ffmpeg select=eq(n,N)`）。heroCutにはKen Burns付与済（共有CaseFilm） → **ARMED(コード)**＋**MANUAL鉄則** [feedback_retro_ep34_rolin / pd-ep34-rolin-done]
71. **フックの画像連射フリッカー**（EP50: 22カット/11.5s＝0.17-0.45s/カット） → HOOK/OPのSECTION_TARGETSカット数を窓尺に対して適正化（最小カット尺~0.8s目安） → **MANUAL**（build時に確認）／最小カット尺ゲートは**GAP**（§G-8） [feedback-thread-retro-20260725]
72. モーション部品の重なり/見切れ（MOTIONKIT 8部品、Trail絶対配置で親高さ0） → 実レンダ休止フレームで可読性確認 → **MANUAL** [feedback_dynamic_motionkit_standard]
73. 二重実装（既存部品があるのに独自ffmpeg/新規実装 — EP38の根本） → **最初から正典CaseFilm＋既存部品**（MOTIONKIT CATALOG.md→presets）。独自組み立て禁止（invariant 14） → **方針ARMED**＋**MANUAL遵守** [feedback_start_from_canon_pipeline / pd-motionkit-library]

## H. STRUCTURE / OP-ED（構成）

74. **フック→OP→本編→EDの4部構成でない**（EP14/EP38） → `structure_4part`ゲート＋フック=本編ハイライト~8秒（最後に書く・payoff検証） → **ARMED**（＋台本段階はPASSED） [pd-ep21-24-incident #4 / spec v2 rows 9-10]
75. **OP/EDがいつものテイストでない**（EP21-24 #5・EP38） → 正典 `Bookends.tsx`（BrandOpening/BrandEndcard・OPENING_SEC3.5/ENDCARD_SEC9不変・フォーク禁止）＋`op_ed_bookends`ゲート → **ARMED** [feedback_opening_ending_taste / spec v2 row14]
76. **金のBrandOpeningを削ってしまう**（EP50コールドオープンtrimでブランド消失→オーナー指摘#1） → 音声0:00開始はtrimでなく設計で（HOOK-AUDIO標準: BODY_START 0）＋**goldオープニングは残す** → **MANUAL**（build時。EP53-55のビルダー設定を確認） [feedback-thread-retro-20260725 / pd-ep48-52-status]
77. 冒頭無音11.5秒（音声からでなくカードから始まる） → 音声/ハイライトを0:00から（オーナー標準） → **MANUAL**（初回レンダでsilencedetect実測） [pd-ep50-status / pd-ep48-52-status]
78. 終わりが止まる/切りが悪い（EP38） → EDはBGM解決＋エンドカードで切りよく（bgm_ending＋耳） → **ARMED**＋**MANUAL**（#19と同じ試聴） [feedback_retro_ep38_kidsforcash]

## I. AFTER EFFECTS（AE差し込みを行う場合）

79. **クラッシュ修復ダイアログが全起動をブロック**（強制終了連発→セーフモードモーダル） → `%APPDATA%\\Adobe\\After Effects\\26.x\\PriorSafeMode.txt` 削除＋スクリプト末尾は必ず `app.quit()`・Stop-Process常用禁止 → **MANUAL手順** [reference_after_effects_automation]
80. **AEが起動するか確認せずAE前提計画**（EP38で数時間浪費） → ダミーjsxでsmoke起動→即quitを先に確認。壊れていたらAE前提を組まない → **MANUAL**（Claude、AE工程の初手） [feedback_retro_ep38_kidsforcash]
81. **英語OMテンプレ名が日本語版AEで不発** → `om.templates`部分一致 or 日本語名をPowerShellから渡す（RS=\"最良設定\"/OM=\"H.264 - レンダリング設定を一致 - 15 Mbps\"） → **MANUAL手順** [reference_after_effects_automation / pd-ae-hero-beat-pipeline]
82. **別事件のAEデッキ**（EP45: Bearden話にHudson v. Michiganデッキを幻覚生成） → aerender前に必ずデッキ内容を読み、当該事件と照合 → **MANUAL**（Claude、毎回） [feedback-codex-codexb-unreliable ★]
83. **.aepが.jsxより古いままレンダ**（EP40: \"undefined\"文字が2回の修正をすり抜け） → aerender前に .aep mtime > .jsx mtime をassert → **MANUAL**（Claude、毎回）／wrapperへの自動assertは**GAP**（§G-6） [feedback-ep3941-eyeball-final-render]
84. **フォント無言置換**（EP38出荷事故: allFonts[i]がwrapper→family名不一致→既定sansへ） → `getFontsByFamilyNameAndStyleName`＋ミス時throw＋完了markerにPostScript名をecho（Anton-Regular/Oswald-Medium確認） → **ARMED(builder修正済)**＋**MANUAL**（marker確認） [pd-ae-hero-beat-pipeline]
85. テキストのbox溢れ（EXCLUDED→\":XCLUDEI\"、推定advance-width） → `sourceRectAtTime`実測でfit → **ARMED(修正済)** [feedback-ep3941-eyeball-final-render]
86. TextDocumentに\\n（画面に文字として出る）／Impact表示名指定で死ぬ／app.newProject()がヘッドレスでハング／setTemporalEase spatial dim → 各回避策（単一行・PS名・newProject回避・dim=1） → **MANUAL手順集** [pd-ae-hero-beat-pipeline / reference_after_effects_automation]
87. fps罠（48fpsコンプが50fpsタグで尺化け） → 出力fps明示ロック＋ffprobe検算 → **MANUAL** [reference_after_effects_automation]
88. **修正カードがrenderされたが最終動画に未合成**（EP40: fixed/に出力しただけで出荷ファイルは旧カードのまま） → 最終成果物が修正を運んでいるかを合成後フレームで確認 → **MANUAL**（Claude、composite後） [feedback-ep3941-eyeball-final-render]
89. AE GUIプロセス残留1.7GB → 次のaerender前に正常終了確認 → **MANUAL手順** [reference_after_effects_automation]

## J. MIX / RENDER（レンダ・合成）

90. **並列レンダでVRAM枯渇→無言クラッシュ**（EP48/49並走＋i2v同時→strieff出力ゼロ・1時間損失。EP33はconcurrency32でクラッシュ） → 重いRemotion/WebGL/i2vは**1本ずつ直列**・開始前に`nvidia-smi`＋他プロセス確認・長尺WebGLは`--concurrency=4` → **MANUAL手順**（Claude、毎レンダ前） [feedback-serialize-heavy-renders / feedback-execution-style / feedback_perceptual_motion_and_verify]
91. レンダ監視の誤殺 — tailパイプで0バイトに見え「止まってる」と誤認→59%の正常レンダを何度も殺した → 出力はredirect直、`grep 'Rendered N/'`監視、node生存＋CPU伸びで健全性判定、**完走前にkillしない** → **MANUAL手順** [reference_remotion_render_ops]
92. サイレントクラッシュの検知遅れ → 監視は `remotion/out/`（08_editではない）＋renderノード生存確認 → **MANUAL手順** [feedback-serialize-heavy-renders]
93. public/ 25-50GBの毎回コピーでレンダ開始が数分死ぬ・3回レンダ失敗 → `--public-dir=public_slim`（エピソード+fonts+root assetsのみ） → **MANUAL手順**（build時にpublic_slim staging） [feedback-ep38-retro #3 / feedback_retro_ep37_florence]
94. delayRenderフォント読込でクラッシュ（EP38 frame411 EPIPE） → CSS @font-face → **ARMED(修正済)** [feedback_retro_ep38_kidsforcash]
95. **偽の緑（fake-green）** — EP29: 再レンダがクラッシュ→muxが旧v003を掴んで緑受領を誤報 → 再レンダ後は「実ファイル存在＋sha≠前回sha」を確認してからmux/受領書。受領書sha=実ファイルsha照合 → **MANUAL鉄則**（Claude、毎レンダ後）※ship-lock側のsha照合は**ARMED** [feedback_perceptual_motion_and_verify / feedback_gate_not_done]
96. BGMを古いレンダから作る（EP50 v001=2日前の別レンダ） → BGM/muxは**必ず最新レンダから**再構築 → **MANUAL手順** [pd-ep50-status]
97. 受領書を未muxファイルに発行（bgm/loudness落ち） → 受領は必ずmux後ファイル・`--render-started-at`はレンダ開始前にepoch記録 → **MANUAL手順** [reference_pd_finalize_and_gate_fixes]
98. **再レンダ回数の浪費**（EP37=5回・EP34=3回・EP35=2回） → 着手時に実受領ゲートを1回フルで回して**全hard-failを先に把握**→render影響修正を1バッチ→**再レンダは原則1回** → **MANUAL鉄則**（Claude） [feedback_retro_ep35_finalize_publish ★ / feedback_retro_ep34_rolin #6 / feedback_retro_ep37_florence]
99. 本レンダ前の安価な実証 — 60-90秒スライスprobe（animation/black/freeze＋目視）＋1カットで機構実証してから全体適用 → **MANUAL手順** [feedback_gate_not_done / feedback_retro_ep34_rolin #7]
100. ゲートの実装を読まずに直す（EP34: PIL輝度≠signalstats YAVGで40枚無駄補正未遂） → 失敗ゲートはコードを読み、**ゲート自身の関数で**測ってから修正 → **MANUAL鉄則** [feedback_retro_ep34_rolin #3/#4]
101. `--json`フットガン — check系CLIの`--json`は**出力先**。film.jsonを渡すと上書き破壊（thompson 195カット消失。film.jsonはgit未追跡＝builderで再生成が唯一の復旧） → 入力は`--ep`のみ → **MANUAL手順** [pd-gate-json-footgun]
102. film.json書き込み競合（EP33-35で他スレと衝突） → 同一ファイルへ並行builderを走らせない・1話ずつ → **MANUAL手順** [pd-ep33-35-production-state]
103. cp932 UnicodeEncodeError（~5回/セッション） → 全スクリプト頭で `sys.stdout.reconfigure(encoding='utf-8')`・print/pathにem-dash回避 → **MANUAL手順** [feedback-ep38-retro #3]
104. `nohup … &`二重バックグラウンドで子が孤児化/追跡不能（EP37/EP38） → run_in_background単体で直接実行 → **MANUAL手順** [feedback_retro_ep37_florence #5 / feedback-ep38-retro]
105. mp4は非標準タグを捨てる → `-movflags use_metadata_tags` 必須（audio_mix_sha256刻印） → **MANUAL手順** [feedback_retro_ep37_florence #6]

## K. PACKAGE / SHIP（受領・パッケージ・予約）

106. **自己申告QC＝最大の事故源**（EP14: QC jsonにtrue手書きでSAPI声/字幕なし/黒画面58秒/BGMなしが素通り） → 独立測定 `check_final_acceptance.py <ep> --render <mp4> --emit-receipt`（sha束縛受領書）以外に「完成」なし → **ARMED** [feedback_final_acceptance / PD_SHIP_GATE]
107. **受領書なしの予約・投稿** → `upload_schedule_case_v001.py` がsha一致受領書なしをhard-refuse（許容偏差=runtime_bandのみ、追加偏差はAPR union） → **ARMED** [PD_SHIP_GATE / reference_pd_finalize_and_gate_fixes]
108. ゲート/閾値を通すために緩める → 禁止（invariant 15）。偏差はAPRで正直に記録して通す（EP35/36/37の実績方式） → **方針ARMED** [feedback_keep_promises_no_gaming / retro-ep36-assembly]
109. 最終ファイル同一性の曖昧化（EP23: final.mp4 vs final.motionfix、wrong-video upload危機） → versioned名＋final_delivery.v*.json（canonical sha）から予約が読む → **ARMED**（uploader要件）＋**MANUAL**（final_delivery作成） [EP21-24_INCIDENT_RETRO #3/#10]
110. メタデータ/manifest/checksumが実出力より遅れる（EP23/24） → 仕上げ時にmanifest/delivery/receiptを一括更新 → **MANUAL手順** [EP21-24_INCIDENT_RETRO #11]
111. **地味・暗いサムネ**（EP21-24 #7） → `thumbnail_visibility`（luma mean≥33+contrast）＋`check_thumb_subject_luma.py`＋≥3案1280×720＋selected → **ARMED**＋**MANUAL**（320px縮小での目視。ゲート合格のCG-blobサムネがCTRを殺した実例=EP40） [pd-ep21-24-incident #7 / feedback-ep3941-eyeball-final-render #5]
112. **人種・実在者ミスリードのサムネ顔**（EP50: 生成顔4案が全部白人少年＝Central Park Fiveを誤表象→棄却） → 人種が主題/存命者事件は**シルエット/雰囲気**を既定に。**EP53(黒人含む水兵4人)/EP54(Flowers=存命黒人男性)/EP55(被害者=黒人多数)は全話該当** → **MANUAL**（Claude設計→オーナー承認） [feedback-thread-retro-20260725 #3]
113. 文学的タイトルはCTR負債（\"Thirty Years in the Dark\"型・Hinton CTR1.35%） → 時間ジャンプ数字/ショック動詞を頭3語に・≤60字・A/B・タイトル=事実側/サムネ=問い（重複禁止）・根拠はCTR_PLAYBOOK/CTR_GROWTH_REFERENCE → **MANUAL**（Claude、エビデンス提示→オーナー承認） [feedback-ctr-evidence-first / pd-ctr-packaging-wave1 / pd-ep53-55-topic-slate]
114. サムネ文言の法的リスク（EP22 \"98 CHARGES\"→\"6 PLEAS\"、EP23 \"35 YEARS\"禁止） → 話別禁止フレーズをFACTS_LEDGERから抽出しサムネ/タイトルlint → **MANUAL**（Claude、package時） [EP21-24_INCIDENT_RETRO #2/#14]
115. タイトル/サムネはオーナー承認必須（rule 16・実画像を見せてから） → dry-run→実画像提示→APR記録→本実行 → **MANUAL**（オーナー、予約直前） [reference_pd_finalize_and_gate_fixes / feedback_retro_ep35_finalize_publish]
116. R2/R3の一括予約（EP21-24を1バッチで処理→状態管理崩壊） → 高リスク話は1話ずつ予約→各回検証 → **MANUAL手順**（EP53-55は3話とも冤罪/拷問/存命者＝全話該当） [EP21-24_INCIDENT_RETRO #12 / Root Cause A]
117. **予約カレンダー衝突**（1日2本事故） → 予約前に全publishAtを監査して空き日に（長尺は12:00 JST枠・**shorts57-59が8/19-21を既に占有**＝ショートは1日1本ルールと突き合わせ） → **MANUAL**（Claude、予約時に`yt_full_audit.py`＋schedule結果JSON全数） [feedback_shorts_one_per_day / pd-shorts-52-59-scheduled]
118. **P0Dスタックアップロード**を「健全」と誤報（privacyStatusだけ見た） → 予約後 `uploadStatus==processed && duration!=P0D` をポーリング → **MANUAL**（Claude、各アップロード後） [feedback-thread-retro-20260723 #2]
119. 壊れた予約の差し替えで旧動画を再掴み → 置換は**先にdelete（安全assert付き）→fresh upload** → **MANUAL手順** [feedback-thread-retro-20260723 #6]
120. **AI開示フラグ** — containsSyntheticMediaはData APIで設定不能（送っても無視・0/98）。ensure_youtube_ai_disclosure.pyは偽成功no-op → 新規アップロードごとにStudio側トグルをオーナーに依頼（説明文のAI開示行は自動で入れる）＋bulk status編集は必ずpublishAtを再送（落とすと予約解除） → **MANUAL**（オーナー=Studioトグル／Claude=説明文行＋publishAt保全） [pd-ai-disclosure-api-limit]
121. manifest stateと実チャンネルの乖離（EP05/07-15を「未公開」と誤答） → 公開状況の正はAPI（yt_full_audit.py＋publishAt） → **MANUAL手順** [feedback_channel_status_source_of_truth]
122. 外部副作用スクリプトの構文バグ（thumbnails.set の TypeError/true≠True） → 外部writeの前に py_compile＋read-only dry-run → **MANUAL手順** [EP21-24_INCIDENT_RETRO #13]
123. API quota枯渇でwriteが403（researchハーベストが10k units食い潰し） → write優先・≥2-3k units温存・search.list=100units注意 → **MANUAL手順** [feedback-thread-retro-20260723 #8]
124. secrets混入 → コミット/ログにkey・cookie・token禁止（rule 03）＋`check_secrets.py`＋コミット毎secret scan → **ARMED**＋**MANUAL**（コミット時） [.claude/rules/03 / feedback_retro_ep35_finalize_publish]
125. git汚染 — SSD媒体/runs/をコミットしない・他スレ作業混在ツリーでは外科的コミット → **MANUAL手順** [git-sync-workflow / feedback_retro_ep35_finalize_publish]
126. 公開済みfinalの上書き再レンダ禁止（invariant 6） → 新revisionのみ → **方針ARMED** [CLAUDE.md invariant 6]

## L. OPS / PROCESS（横断プロセス）

127. **1フレームで「完成」宣言**（EP39-41: オーナーが通し視聴で6+欠陥発見。EP50: 技術QC後にオーナーが9欠陥） → **全尺を自分で観る**：8点以上のグリッド＋~30秒毎サンプル＋全強調/AEビートのsettleフレーム。確認観点=文字切れ/衝突・安っぽい背景・空バー・カウント値・字幕欠落・フォント置換・色被り・スタブ素材・ゆがみ/曇り/スキャンライン・顔と多様性・ペーシング → **MANUAL**（Claude、受領後〜オーナー提示前。preflight_owner_review.pyの成果物提示とセット） [feedback-ep3941-eyeball-final-render / feedback-thread-retro-20260725 ★★]
128. **見せる前のオーナー基準セルフレビュー1周**（EP37/38で同じ反省を2回） → チェックリスト＝①スマホで字幕可読 ②OP/ED=Bookends ③先頭8秒ハイライトフック＋音声0:00 ④完全静止なし ⑤素材/画像被りなし ⑥終わり切りよし ⑦却下済み演出ゼロ（周回光/スイープ/黄ウォッシュ/dochighlight/カラオケ字幕）。1つでも×なら見せない → **MANUAL**（Claude、毎提示前） [feedback_retro_ep38_kidsforcash #5 / feedback_retro_ep37_florence]
129. **エージェントの偽\"done\"**（\"3×eyeball PASS\"が2,001バグ見逃し・\"all cards verified\"が未合成・0バイト.output誤読） → サブエージェント報告は事実として中継しない。実アーティファクトを自分で抽出して見る。.output空でもjsonl/成果物で判定 → **MANUAL鉄則**（Claude） [feedback-thread-retro-20260723 #4 / feedback-ep3941-eyeball-final-render / pd-gate-json-footgun]
130. 測る前に断定（「未実装」「ブロック」「完成」を実測なしで言い撤回連発） → 負の状態/完成の断定文の前に必ず1コマンド（grep/ls/実行） → **MANUAL鉄則** [feedback_session_retro_ep33_35 / feedback_measure_before_explaining]
131. ゲートの偽RED（caption_integrityがCaseFilm艦隊を偽FAIL・arc_nonrepeat偽陽性・check_script_length初版の帯域バグ） → REDが出たら「計器が壊れてないか」を先に検証。既知良品エピソードで定期較正 → **MANUAL手順** [feedback-ep38-retro #4 / pd-runtime-shortfall-rootcause]
132. 一発目ツールのバグ（mkstemp/regex 0x08/typo） → 自作ツールは--selftest/スモーク後に投入。生成コード(regex/jsx)はファイルに書いて実行（シェル多重quote禁止） → **MANUAL手順** [feedback_session_retro_ep33_35 / feedback-ep3941-eyeball-final-render]
133. ゲートコードを読まずに見積もり（\"30-60分\"→実2時間） → 見積もり前にゲート/パイプライン実コードを読む。ETAは範囲＋リスク → **MANUAL手順** [feedback-ep38-retro #2 / feedback-execution-style]
134. 着手前にパイプライン正典を読まない（EP38の根本） → build開始前に `PD_ONE_PASS_PRODUCTION_SPEC.v2` 全行＋`PD_SHIP_GATE`＋`reference_longform_assembly_pipeline`＋ship-gateギャップ表を通読 → **MANUAL**（本ラン・シート§3の step 0） [feedback_start_from_canon_pipeline / feedback_retro_ep37_florence]
135. 連動ゲートの副作用を後追い（narration_index.chunks→structure_4part起動・dangling修正→cps回帰） → ゲート依存を修正前に予測し、修正後は関連ゲートを束で再実行 → **MANUAL手順** [feedback_retro_ep37_florence #2 / feedback_retro_ep35_finalize_publish]
136. 重複エージェント起動（atwater二重finish→TaskStop） → spawn前に既存エージェント/成果物を確認 → **MANUAL手順** [feedback-thread-retro-20260723 #5]
137. 課金境界 — 契約内は自由・超過のみ確認（ElevenLabsは常時承認済・文字数記録は継続） → **方針** [cost-policy / feedback_elevenlabs_standing_approval]
138. 品質>速度・トップ1%基準 — 「無難な平均」を出さない。ゲート緑=床、見ごたえ=目標 → **方針**（全工程） [feedback_quality_over_speed / feedback-top-1-percent-not-average]

---

# 第2部 GAP — 機構が無い失敗モード（正直リスト）＋EP53-55向け最小チェック案

> ルール: コードは今実装しない。ビルドセッションで下記の「最小チェック」を必ず手で実行し、可能ならその場でスクリプト化する（lessons-must-be-gates）。

**G-1. SFXの「意味・質」監査（SFX-tag audit）** — `verify_sfx_manifest.py` はWEAK（存在と数しか守れない）。EP32の教訓（フィラー326個・jet音）以来、音の意味はゲート化できていない。最小チェック: build_case_film_audio の cue sheet を dump し、各SFXキューに「どのナレ/映像ビートを補強するか」の理由フィールドが埋まっているかを目で確認（理由なし=削除）＋章境界5点と終盤10秒の試聴を受領前の固定手順にする。密度キャップ=平均≤1モチベート音/60-90秒。 [feedback_sfx_meaningful_only / PD_EP32_POSTMORTEM C]

**G-2. Codexスタブ/破損画像の受領ゲート** — 現状は手打ちの `find -size -50k` とluma probe。EP50(630本)/EP52(227本)/EP54(S025以降破損)と3回続いた最頻出のCodex欠陥なのに自動ゲートが無い。最小チェック: 受領直後に3話それぞれで (a) manifest宣言数 vs 実ファイル数、(b) `-size -50k` の本数=0、(c) ランダム12枚のYAVG≥40、(d) phashで同一クラスタ≥5枚をFAIL、をワンライナーで実測し結果を数値で記録。**EP54の7/25破損は2026-07-26のスポット目視（3/3良品）で再生成済みと確認——それでも受領時の全数監査は3話とも必須（スポット≠全数）。** [feedback-thread-retro-20260725 #1 / pd-shorts-52-59-scheduled]

**G-3. warp/haze/scanlineの自動QC** — pd-footage-quality-fixes が「QCゲートを足す」と明記したまま未実装。treatments修正で発生源は塞いだが、EP50では「修正したはず」のwarpが残存した実績あり。最小チェック: 初回レンダから深度系treatmentが乗るはずのカット10点＋人物カット10点のフレームを抽出してReadで目視（溶け顔・61-63°斜線・白曇り）。1件でも出たらbuilderのtreatments配列をgrepして真因を特定してから直す（カット側対症療法禁止=EP34教訓）。 [pd-footage-quality-fixes / feedback_retro_ep34_rolin]

**G-4. dochighlight preflightゲート** — 禁止決定済みだがgrep頼み。最小チェック: film build直後に `grep '\"kind\": \"dochighlight\"' remotion/src/data/<slug>_film.json` = 0件をビルドログに記録（3話とも）。クローン元builderのfigure_payloads()にdochighlightが残っていないかも同時にgrep。 [pd-dochighlight-reads-as-bug]

**G-5. figureスキーマの汎用バリデーション** — validate_*_beats はcentralpark専用。EP44/45ではスキーマ不正がレンダを実クラッシュさせた。最小チェック: レンダ前に film.json の figures[] 全件の kind と必須キー（pins/data/…）を FigureBeats.tsx のunion定義と突き合わせる読み合わせを1回実施（jq で kind別のキー一覧を出し、FigureBeats.tsxの型と目視照合）。 [feedback-codex-codexb-unreliable]

**G-6. 声の最終同一性（x-corr）とAE鮮度のship組込み** — SAPI相互相関チェック（≥0.5）と `.aep newer than .jsx` assertは手順であってゲートでない。EP48は**2箇所目**のSAPIロックがindexゲートをすり抜けた。最小チェック: 受領書発行の直前に (a) 最終mp4のVO 6秒を vc_master と np.corrcoef（実測値を受領記録に残す）、(b) `build_<slug>_bgm*.py` をgrepしてVOパスが narration master を指すこと、(c) AEを使った場合は aep/jsx のmtime比較、の3点を毎話実施。 [feedback-thread-retro-20260723 ★★ / feedback-ep3941-eyeball-final-render]

**G-7. 図の密度・背景輝度の下限（E-nosparse）** — EP32 postmortem ☆のまま。最小チェック: FigureBeats採用一覧をdumpし、2要素以下の地図/図をリストアップして手で差し替え。図タイプの同種連続もここで確認。 [PD_EP32_POSTMORTEM E4/VI]

**G-8. フック区間の最小カット尺** — EP50のフリッカー（0.17s/カット）を止める機械床が無い。最小チェック: film.json の HOOK/OP 区間カットを jq で数え、窓尺/カット数≥0.8s を確認してからレンダ。 [feedback-thread-retro-20260725]

**G-9. 「豊かな動き」の正の下限の較正** — motion_energy（within-shot mean≥12）は存在するが、EP30/31/36/50と「緑なのに物足りない」が繰り返された＝較正が実感に追いついていない。最小チェック: 知覚モーション予算（#55）をビルダー出力の実数（depth系treatment%・FigureBeats数・hero面数・stock本数・still-share%）で表にしてオーナー提示資料に載せる。数字が床ギリギリなら上げてからレンダ。 [feedback_animation_still_too_little / feedback-lessons-must-be-gates]

**G-10. AI開示の自動化** — Data APIでは物理的に不可能（Studio-only）。最小チェック: 予約完了報告に「Studioで『改変コンテンツ=はい』を3話分トグルしてください」をオーナー宛タスクとして毎回明記（説明文のAI開示行はClaudeが自動で維持）。 [pd-ai-disclosure-api-limit]

**G-11. 全尺視聴の機構化** — preflight_owner_review.py（16枚シート/字幕ラグ/音抜き出し/輝度）はあるが、「通しで観る」自体は自動化不能＝永続MANUAL。最小チェック: §3ラン・シートの W ステップ（全尺ウォッチ）を受領書発行の**前提条件**として毎話チェックボックス化（本書がその台帳）。 [PD_EP32_POSTMORTEM 第IV部 / feedback-thread-retro-20260725]

---

# 第3部 EP53-55 ビルド・ラン・シート（film.json組み立て→予約まで・この順で実行）

> 3話は**1話ずつ直列**で仕上げる（EP21-24バッチ事故の教訓 #116、レンダ直列 #90）。各ステップの[]をこのファイルには書き込まず、セッションログで✔を記録すること（本書はread-only運用）。

**STEP 0. 正典再読＋ギャップ表**（#134）
- `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` / `docs/PD_SHIP_GATE.md` / `.claude/rules/19-ship-gate.md` / memory `reference_longform_assembly_pipeline` を通読。
- `check_final_acceptance.py` と `preflight_render_gate.py` の現行ハードゲート一覧をgrepし、本書STATUS=ARMEDの配線を1度だけ実確認（メモリ記録と実コードの乖離チェック #130）。

**STEP 1. Codex画像 受領監査**（各話・Codex完了連絡の当日）
- 枚数 vs manifest全数照合（#35）／スタブ監査 `-size -50k`=0＋luma probe（#36, G-2）／EP54の旧破損は再生成済み確認（7/26スポット3/3良品）——全数監査は必須のまま。
- phash類似クラスタ（#37）／人物比率~40%実測（#38）／実在肖像・偽テキスト目視、書類系は1枚ずつ（#39, #40）。
- `remotion/public/<slug>/img/` に4K実体を配置（render-truth #41）。

**STEP 2. 音声の再検証**（生成済みでも必ず）
- vc_master実在＋ffprobe（#16, #17）／`check_narration_voice.py`＋chunk sidecar voice_id監査（#13）／実測wpm=総語数÷master実尺が163-185に入るか（#15）。
- narration_index総語数 vs 台本語数 diff（欠落パッセージ検出 #10）／予測尺が27-33分帯に入るか。

**STEP 3. 実写素材 staging＋目視QC**
- `select_factory_assets.py --theme <t> --kind video`（**台帳ベース**。`--allow-off-label` は原則使わない。#53a）で広く staging。コンタクトシートは選択・staging時に**自動生成**され `runs/qc/factory_selection/<stamp>__<theme>-video/` に出る（`--no-sheet` は配管用途のみ・使ったら未レビュー扱い） → **全クリップ目視**・場違いをBLOCK_IDS（#47）／featureless除去（#50）。外したIDは `selection.v001.json` の `review.rejected_ids` に記録。
- タイル下段の `tier | theme | 実タイトル` を必ず読む。`cross_theme->here` と `off_label` は誤りの当たりが高い。theme名で狙わずサブタイプ語で狙う場合は `--query` でよいが、その結果にも同じ台帳注記が付く。
- 実ストック（H:/pd-media/assets/stock）とi2v人物モーションを織り込み、stock使用数を記録（#51, #56）。
- `check_arc_nonrepeat.py` を EP1-52＋EP53-55相互で（#49）。

**STEP 4. film.json ビルド**
- 正典builderのみ（独自ffmpeg禁止 #73）。builderの継承確認grep: treatments=bleed/duotone/focusのみ（#57）・BodyGrade0.07（#58）・DriftLight線なし（#59）・`_split_caption_text`2行（#30）・dochighlight=0（#62, G-4）・BODY_START/音声0:00＋goldオープニング維持（#76, #77）。
- HOOK/OPカット尺≥0.8s（#71, G-8）／figuresスキーマ照合（#64, G-5）／年号group:false（#65）。
- 知覚モーション予算の実数を確保して記録: モーションtreatment≥40%・FigureBeats≥6・hero面≥2・still-share（#55, G-9）。
- scene_plan↔film.json の意味対応スポット確認（#52）／runtime_bandの正典帯を `remotion_plan.motion_budget.runtime_band_seconds`=[1620,1980] と `manifest.target_duration_minutes=30` に明記（EP34の帯域バグ回避）。

**STEP 5. 字幕**
- `gen_captions_forced.py`（align_windowed/medium.en/LEAD0.60）→ `verify_caption_sync.py`（キャッシュで反復 #34）→ `check_caption_format`／dangling修正時はcps再確認（#28）→ v001に確定＋film.jsonミラー（#33）。

**STEP 6. 音 design/mix**
- `build_case_film_audio.py`（フィラーなし・distinct≥12・ending固定ベッド #21-23）→ cue sheetの理由フィールド確認（G-1）→ `--render` 4層WAV -14LUFS。

**STEP 7. PREFLIGHT（レンダ前・課金/GPU前に全部緑）**
- `preflight_render_gate.py`: script_length / motion_density / animation_mix / caption_integrity / visual_asset_qc / narration_voice / AE_layouts / year_grouping ほか全チェック。REDが出たら計器の健全性も疑う（#131）。

**STEP 8. probe → 本レンダ**
- 60-90秒スライスprobe＋目視（#99）→ 修正があれば全部束ねる。
- 本レンダ: **直列1本・concurrency=4・public_slim・nvidia-smi事前確認**（#90, #93）／`--render-started-at`を先に記録（#97）／tail監視禁止・完走前kill禁止（#91, #92）。
- 完了後: 出力sha≠前回shaを確認（fake-green #95）。

**STEP 9. AEヒーロー差し込み（行う場合のみ）**
- smoke起動→PriorSafeMode確認（#79, #80）／デッキ内容を読み当該事件と照合（#82）／.aep mtime>.jsx assert（#83）／フォントPS名marker確認（#84）／日本語OMテンプレ（#81）／合成後、最終ファイルが修正カードを運んでいるかフレーム確認（#88）。

**STEP 10. mux → 受領**
- BGM/muxは**この最新レンダから**（#96）→ `build_case_film_mux.py`（use_metadata_tags #105）→ mux後ファイルへ `check_final_acceptance.py <ep> --render <muxed> --emit-receipt`（#106）。
- FAILが出たら: 全fail根本診断（コード読み＋フレーム目視 #70, #100）→ render影響修正を1バッチ→再レンダ1回（#98）。
- 受領直前3点セット: VO x-corr≥0.5＋bgm builderのVOパスgrep＋（AE時）鮮度assert（G-6）。

**STEP 11. オーナー基準セルフレビュー（受領書が緑でも必須）**
- `preflight_owner_review.py` 一式（コンタクトシート/字幕ラグ/音5本/輝度）＋**全尺ウォッチ**（8+グリッド・30秒毎・settleフレーム #127, G-11）。
- 7点チェック: スマホ字幕/Bookends/8秒フック＋音声0:00/静止なし/被りなし/切りよい終わり/却下済み演出ゼロ（#128）。試聴: 章境界＋終盤10秒（#19, #22）。
- 1つでも×なら見せない。実数（still-share/FigureBeats/stock本数/字幕ラグp90等）を添えてオーナー提示。

**STEP 12. パッケージ**
- サムネ≥3案1280×720＋visibility/subject_lumaゲート＋320px目視（#111）。**3話ともシルエット/雰囲気既定**（人種・存命者 #112）。
- タイトル: 数字/ショック動詞先頭・≤60字・A/B・FACTS_LEDGERの禁止フレーズlint（#113, #114）。
- final_delivery.v*.json（canonical sha）＋manifest/receipt一括同期（#109, #110）。

**STEP 13. 予約（1話ずつ・オーナーゲート）**
- py_compile＋dry-run（#122）→ タイトル+サムネ実画像をオーナー提示・承認＋偏差APR記録（#115, #108）→ `upload_schedule_case_v001.py`（受領書ロック #107）。
- 予約前カレンダー監査: 長尺12:00 JST枠の全publishAt＋shorts57-59(8/19-21)との整合（#117）。
- 予約後: `uploadStatus==processed && duration!=P0D` ポーリング（#118）／yt_full_auditで実チャンネル確認（#121）／**オーナーへStudio AI開示トグル依頼**（#120, G-10）。
- R3最終レビュー（EP53自死未遂・EP54死刑/存命DA・EP55拷問）をオーナーが公開前に（#5）。

**STEP 14. クローズ**
- 外科的コミット（媒体/runs除外・secret scan #124, #125）／本書のGAPのうちその場でスクリプト化できたものを記録／メモリ更新。

---
*本書は read-only の台帳。ゲートを通すための緩和・偏差の隠蔽は行わない（invariant 15 / no-gaming）。新しい失敗が出たら「row追加＋ゲート追加」で本書を v002 に上げる。*
