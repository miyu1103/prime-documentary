# EP38 — Kids for Cash（少年を金で売った判事）— 設計 ＋ Codex画像プロンプト

- Episode ID: `PD-2026-038-kidsforcash` / slug `kidsforcash`
- 題材: ペンシルベニア州ルザーン郡「Kids for Cash」スキャンダル（2003–2009頃／少年裁判所判事 Mark Ciavarella と管理判事 Michael Conahan による司法汚職）
- 事実の骨子（**数字・年号・人数・量刑・氏名は全て claim台帳で要検証＝review_required**）:
  - 2人の判事が、新設の**営利少年拘置施設**（PA Child Care／Western PA Child Care）の関係者（建設=Robert Mericle／運営=Robert Powell）から**3年で総額 約$2.8M**の金銭を受領（$2.6Mとする出典もあり＝台帳で確定。数字カードは$2.8Mで統一）。
  - 見返りに、Conahan が郡営の少年拘置所を実質閉鎖して財源を断ち、Ciavarella が**軽微な非行の子供たち**（学校でのふざけ・SNSの悪ふざけ・万引き等）を、**多くは弁護士なし・数十秒〜数分の"審理"**で次々と施設送りにした。
  - 象徴的被害者（確定）: **Hillary Transue（審理時17歳・2007年4月）**が副校長を揶揄する偽ウェブページを作り**3か月**の収容判決（実際は約1か月で弁護士の助けで釈放）。**Edward Kenzakoski（17歳・薬物付属品所持・ブートキャンプ30日だがPA Child Care系施設に数か月）**は後に**23歳で自死**、母 **Sandy Fonzo** が法廷前でCiavarellaを面罵。
  - 発覚後、ペンシルベニア州最高裁は**約数千件の少年審判を取消・記録抹消**。Ciavarella は**RICO（組織的恐喝）**で有罪・**約28年**、Conahan は司法取引で**約17.5年**の実刑（いずれも要検証）。
- テーマ: **司法という最後の砦が、子供を換金した** × 「え、判事が子供を"売って"いた？」× 権力の腐敗 vs 無力な個人（＝当chの核）
- 勝ち筋適合: 実話・大衆が食いつく・**有名すぎない**・「え？なにそれ？」サムネ最強・被害者が子供＝感情の引きが最大。判例解説ではなく**一人（と一家）の物語**として描ける＝実測で最長視聴だった"物語もの"（Titan 471s / 裏口入学 337s）と同系。
- リスク: **R2（要・公開前レビュー）**。理由=(1) 実在の被害者は**未成年の私人**→肖像・実名の顔出し厳禁、匿名シルエットのみ。(2) **自死の要素**→方法・遺体・グラフィックは一切描かない（象徴のみ）。オーナー判断で相談ホットライン系の配慮も検討。(3) 加害判事は**有罪確定の公人**だが認識可能な顔は出さない（公的記録に基づく中立記述に限定）。
- 尺: 11–12分（フック→OP→4幕→ED）。中身が持てば 13–14分まで許容の余地（要オーナー相談）。

---

## 0) 今回のアナリティクス反映（binding・データ土台）

> 2026-07-16 実測（YouTube Analytics API）で確定した事実を、この回で仕組みとして拾う。

- **最大のボトルネックは"変換（登録）"**: ショート累計1,322再生→登録0／本編累計541再生→登録1。入口は動くが出口が繋がっていない。
  - 対策(この回で必須): (a) ED直前に**明確な登録CTA**（「あなたの街でも起きうる。次の判例も見逃さないで」系・語同期）。(b) 公開後に**固定コメント**で登録導線＋関連本編リンク。(c) 説明欄トップに登録＋シリーズ導線。
- **長く見られるのは"物語もの"**: 本編の平均視聴秒数トップは Titan(471s)/ミルケン(376s)/裏口入学(337s)/D.B.クーパー(303s)＝いずれも人物・事件のナラティブ。純粋な判例解説（Miranda/Gideon/Kelo）は1–5再生。→ **本件は判事の解説にせず、子供と親の物語に徹する。**
- **本件はショート適合が高い**: 伸びたショートは全て「権力 × あなた/家族」。本件の縦ショート（例:「彼女がやったのは、先生をからかう投稿だけ。判決は3か月だった #Shorts」）は入口として強い。ショートは別途 SHORTS 系仕様で1本作る（本設計書の対象外だが導線として明記）。
- **計測の仕込み**: Studioクッキー再取得後に `audienceRetention`（イントロ離脱・30s残存）を本件で計測できるようにする。フック8秒の効き目を次回改善に回す。

---

## 1) 構成（ナレ入りフック＝新方針／EP37踏襲）

- **フックは本編を全部作ってから最後に組む**（新規制作せず、**本編の最高の決めカット/名ゼリフを流用**して再構成）。そこに**ナレを乗せる＋語同期字幕**（無音フックにしない）。フックは**先頭**（オーナー標準）。
  - フックナレ（約12–15秒・叩き台）: 「15歳の少女がやったのは、先生をからかうページをネットに作っただけ。判事は、彼女を3か月、施設に送った。審理にかかった時間は、90秒。——そして判事は、送った子供の数だけ、金を受け取っていた。」
- OP: ブランドタイトル（Bookends正典）。
- 幕1: **普通の子供たち**（軽微な"非行"・平穏な日常）→ 90秒の審理・弁護士なしで施設へ（不条理の提示）
- 幕2: **仕組み**（Conahan が郡の拘置所を潰す → 営利施設へ子供が流れる → 判事に金が入る）。子供の身柄が"商品"になる構造を、causalに解剖。
- 幕3: **崩壊した一家**（自死した少年と母／記録に残る少数の名前）。数字の裏の"一人"を描く＝感情の頂点。
- 幕4: **暴かれる**（Juvenile Law Center らの追及 → 州最高裁が数千件を抹消 → RICO有罪・28年）。転回＝「司法が司法を裁いた」。ED＋**登録CTA**＋次回引き。
- ED: 余韻＋Bookends正典（BGMは切りよく／尺はいじらない）。

---

## 2) 画像枚数（1枚運用に更新）

- **方針変更（オーナー2026-07-16）**: Codexは一発で当たるので、同一場面を5〜6枚も刷らない。**各場面1枚**（重要場面のみ保険で2枚）。
- ただし紙芝居回避は**「静止画を動かす（§5.5 Wan/motion）」＋「別々の場面数を確保」**で担保する（同じ絵の枚数稼ぎではない）。
- 11–12分を絵で持たせるため、**別々の場面を約40**に増やす（S01–S20＋台本v002で追加のS21〜）。**最終 ≒ 40枚前後 × 各1枚**。
- Codexへ: 「各プロンプトを**1枚**出力（重要のみ2枚）。`S01.png`, `S02.png`…と保存」。

---

## 3) 台本＝作品賞級（最重要・binding）

> 正典=`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（アカデミー脚本基準／EP19以降拘束）。オーナー厳命: 台本はかなりこだわる。パルムドール級に。

- 一流ノンフィクション作家の筆致（**AI臭ゼロ**）。**判例解説ではなく、子供と親の尊厳の物語**として書く（一人の子→普遍へ）。
- 構造: 強いフック(問い)→普通の子供と日常→不条理(90秒の審理)→仕組みの解剖(金の流れ)→**最も暗い底**(壊れた一家・自死)→転回(暴露と司法の断罪)→普遍化(あなたの街でも)→余韻。**因果で繋ぐ**（時系列の羅列にしない）。
- 事実性厳守: **claim台帳で1文1典拠**。争点・評価は中立帰属。**数字/年号/条文/量刑/人数/氏名は要レビュー**。判事の動機は立証事実に限定し、憶測を断定しない。
- **自死の描写規範**: 方法・手段・遺体・グラフィック描写を一切しない。喪失は象徴（空の椅子・消えた光・母の沈黙）で表す。センセーショナルにしない。
- **台本は3回書く**（初稿→批評→改稿）。ナレ本文は完成後に変えない。

---

## 4) 意味の一致（最重要・binding）— 「ナレが言っている事を、その画で示す」

> これまで素材を適当に並べてナレをあてこんでいた＝意味が繋がらない/雑。仕組みで直す。参照: [[feedback_visual_narration_meaning_match]] [[feedback_animation_still_too_little]] [[feedback_perceptual_motion_and_verify]] [[feedback_pd_craft_directives]] [[feedback_video_natural_style]] [[feedback_footage_diversity]]。

- **台本が先。次に scene_plan で 1文（1ビート）ごとに**: `visual_question / visual_verb / start_state / end_state / eye_target / sync_words / source_type / truth_status` を必ず埋める。**その文が言っている内容を、そのまま示す画/動画/アニメを割り当てる**（汎用B-rollの流し込み禁止）。
- **語同期を接着剤に**: 決め所の語（"ninety seconds" / "no lawyer" / "for cash" / "two-point-six million" / "a for-profit jail" / "twenty-eight years" / "thousands of children" / "your child" 等）を faster-whisper の語タイムに合わせ、**その語の瞬間に対応する画/リビールが出る**。
- **意味の流れ＝ナレの論理と一致**: 子供の日常→審理→施設→金の流れ→壊れた一家→暴露→断罪→射程、の順に画も進む（下記 S01–S20 はこの順＝ナレのビート順）。飾りだけの画・脈絡ない転換は禁止。
- **素材の被り禁止**（話またぎ/話内とも・`footage_diversity`）。天秤等の汎用象徴は≤2。意味のある反復のみ可。
- 各カットは静止で止めない（2.5D/意味あるモーション）＝紙芝居ゲート＋動き量下限を満たす。

---

## 5) 動きの方針（今回の目玉・binding）— 「絵を本当に動かす」＋After Effectsを本気で使う

> オーナー方針(2026-07-16): 今回はAfter Effectsなど新ツールを**本気で使う**（失敗してもよいので挑戦する）。動きを今までよりはっきり増やす。参照: [[feedback_ken_burns_is_kamishibai]]（ズームだけ＝紙芝居として却下）[[feedback_animation_still_too_little]]（緑でも「また少ない」）[[pd-motionkit-library]] [[pd-motion-toolkit]] [[reference_after_effects_automation]]。

**大原則: ズーム/パンだけの静止画は禁止。絵そのものが動くこと。**

動きの4段構え（意味に合わせて割り当て）:
1. **絵を動画に変える（本命の“脱・紙芝居”）** — Codexの静止画を img2video で**本当に動かす**（雨/霧/光/人の気配/煙が実際に流れる）。実証済み手段=SVD（`scripts/svd_natural_hq.py` ほか）。背景・環境主体のカットで使う（人物シルエットは動きすぎ注意）。VRAM競合はA1111を`unload-checkpoint`で解放。
   - 対象例: S01廊下の空気, S02モニタの明滅, S05施設の光, S06独房の光, S09消えていく灯り, S19近づく車, S10喪失の光。
2. **After Effectsで“見せ場”を本気で作り込む（今回の挑戦・大きく使う）** — 番組級の作り込みで頂点カットを仕上げる。まず**1カットで道具の動作確認（スモークテスト）→ 問題なければ見せ場に展開**。
   - 最優先の見せ場: (a) **お金が判事に渡る流れ**（S07/S15）, (b) **子供が“数字/商品”にされる**（S08）, (c) **判決28年・数千件抹消**（S13/S14）, (d) **OP/EDタイトルと章転換**。
   - 実務メモ: `AfterFX -r <jsx>`でビルド→`aerender`で書き出し。強制終了後の**クラッシュ修復ダイアログが全起動をブロックする罠**＝`PriorSafeMode.txt`削除＋正常終了(app.quit)。GPU不安定は`gpuAccelType=SOFTWARE`。**新規導入ゆえ最初に必ずスモークテストで実挙動を確認**。
3. **動く図（もう出来ている部品）** — 数字/対比/金/判決を motionkit で見せる:
   - 「軽微な非行 → 収容月数」= **PenaltyVsProperty**（罰の不均衡）
   - 「施設オーナー → 判事へ 2.6M」= **MoneyFlow / CaseJourney**（金と子供の経路）
   - 「仕組みの解剖」= **MechanismReveal**、「数千件の記録抹消」= **RecordsScan**
   - 「"90秒でなぜ有罪？"」= **QuoteUnderExamination**、「有罪28年／抹消」= **VerdictReversal / StampReveal**
   - 「押収金・契約書」= **EvidenceReveal / EvidenceCard**
4. **奥行き＋3D舞台** — ヒーロー静止画は Depth V2＋SAM2で奥行きを付けカメラを進める（2.5D）。法廷/章の舞台は3D（Blender・カメラ移動）。※あくまで①②の補助。単独で“動いた事にしない”。

- 実景B-roll → OpenCLIP意味検索で意味の合う実写を選ぶ。factory棚は**ラベル破損に注意し必ず目視QC**（参照 [[pd-factory-shelf-mislabeled]]）。
- 字幕 → faster-whisper語同期（発話語ハイライト・リード0.60s・文法分割）。ナレ入りフックも語同期。
- **切り替えを速く・多彩に**（クロスフェード一辺倒をやめる）。カット刻みを詰める。
- 受入: `animation_density`（凍り検出）に加え、**動きの“大きさ”の正の下限**（`measure_motion_energy.py` の optical-flow エネルギー）を満たす＝「凍ってない」だけでなく「ちゃんと動いてる」を数値で確認してから出す（自己申告禁止）。`footage_diversity` ＋ caption同期 も通す（ship-gate rule 19）。

---

## 5.5) モーション・パイプライン強化（docs/42反映・実数値転記・binding）

> 出典: `docs/42_AI_MOTION_PIPELINE_HARDENING_AND_GATES.md`（PDリポ @ 12b15db2）＋生ログ `ae-demo/POSTMORTEM.md`。一晩のR&Dで見つけた**エラーを出さず静かに品質を落とす罠**を、消費（GPU/レンダー/公開）の前に落とすゲートに変換した成果。ここは**実際の数値**を書き切る（Codex/実装者がdocs/42を読まなくても動くように）。

### 設計思想（4原則・ツール非依存・全工程に適用）
1. **動く≠正しい**: 「動いた」で止めない。実データで端から端まで通し、出力を**目視＋計測**で確認してから次へ。
2. **驚いたらまず測定器を疑う**: 期待と違う数字が出たら、発見よりツール/指標を先に疑う（例: PILが16bit PNGを8bitで読む）。
3. **消費の前に落とす**: 重い生成/レンダーの前に軽い検証（グラフのdry validate・コンポのdry-run・フレーム数の事前計算）を必ず挟む。
4. **成功報告を信じない**: 副作用（実VRAM・実フレーム・実再生）を見る。停止は必ずプロセス一覧＋PIDで実確認。

### Known-good 設定レジストリ（この値を使う。表外の値は出典を1つ付けてから使う＝憶測禁止）
- **AI動画生成エンジン＝Wan2.2 I2V-A14B（14B）**。5Bより指示追従・顔/衣装保持が明確に上（実測 h5 vs k4）。
  - `shift = 5.0`（**5Bの8.0を流用しない**）／`cfg = 3.5`／`steps = 40`／**エキスパート切替 = 50%地点**。出典: ComfyUI同梱 `video_wan2_2_14B_i2v.json` ＋実測（蒸留LoRA不使用）。
  - **VAE = wan_2.1_vae**（2.2ではない）。生成解像度 = **1280×720**（A14Bの学習域）。
  - **4090で完全ロードできるのは ≤41フレーム@720p まで**（`loaded completely`）。**81フレームは部分ロードで約3倍遅い**（41f=約24分/カット、81f=約73分/カット）。
  - → **長尺は「81×少数」を諦め、「41フレーム×多数カット＋補間」に割る**。ヒーローはRIFEでスロー化。
- **補間＝RIFE v4.6、2x（ヒーローのみ4x）**。原本を画素完全保存（max_diff=0）。出力は **f0001始まり**（f0000はパス無効）。
- **静止画の元＝今回はCodex**（R&DはSDXL RealVisXL V5.0だったが、本作の絵はCodex指示。Codexの絵→Wanへ入力＝下記フローで置換）。
- **合成＝After Effects：32bit float**（`proj.bitsPerChannel=32` ＋ RenderSetting「Color Depth: 32 bits per channel」）。中間H.264を挟まない（PNG連番を直接AEへ・4:2:0の色間引きを合成前に入れない）。
- **16bitマスター出力＝隠しテンプレ `_HIDDEN X-Factor 16`**（PNG/16bpc）。**可視テンプレは全部8bit、OMのDepthはスクリプトから読み取り専用**なので唯一の経路。32bit floatは `_HIDDEN X-Factor 32`。
- **配信は二本立て＝10bit HEVC マスター ＋ 8bit H.264 互換版**（Windows標準でHEVC非対応があるため保険）。**ship-gate/受領に載せるのは8bit H.264**。
- モデル置き場＝**D:（内蔵NVMe・空き潤沢）**。C:（空き僅少）とH:（USB外付け）はモデル常用置き場に不適。16bitマスターは720フレームで約5.2GBを要計上。

### 想定フロー（本作）
`Codex静止画（16:9）→ 720pにconform → Wan2.2 A14B i2v（41フレーム/カット・上記数値）→ RIFE 2x/4x → After Effects 32bit float合成（見せ場の作り込み）→ 16bit PNGマスター → 10bit HEVC＋8bit H.264 の二本書き出し`

### 消費前に必ず通すゲート（実数値つき・プロンプト判断に委ねない）
- **G-GEN-2（配線）**: 本生成の前に `length=最小(5)` で1回だけ検証実行。**HTTPエラー本文(node_errors)を必ず展開してログ**。i2v系ノードの出力（**0=positive / 1=negative / 2=latent**）が正しく接続されているか静的検査（latentにconditioningを繋ぐミス／生CLIPを渡して開始画像がサンプラーに届かないミスを防ぐ）。skip代償=最大3.5hのGPU時間が無駄。
- **G-CAP-1（容量）**: 生成前に、起動直後ログが `loaded completely` か `loaded partially` かを読む。partialならフレーム数を落とすかカット分割。着手前に**カット数×24分**で総時間を先に見積る。
- **G-TIME-1（尺）**: 各カットで `必要フレーム = 尺×fps` と `供給フレーム = 生成×補間倍率` を**算術検算**し、**供給 ≥ 必要 + 3フレーム**をassert（緩い閾値禁止＝末尾の黒画面を防ぐ）。補間後の実フレーム数も厳密チェック。
- **G-TIME-2（fps）**: AEは連番を**既定30fpsで読む**。取り込み後に各フッテージ `conformFrameRate = 目標fps` を必須化（放置で全カット早回し＋全ビートずれ）。
- **G-COMP-1（コンポ健全性）**: 本レンダー前に代役フッテージでコンポを組み、**全レイヤー** `outPoint <= comp.duration` を機械検査（1件で止めず全走査）。回転は `"ADBE Rotate Z"`（2Dで `"ADBE Rotation"` はnull）、`motionBlur`はレイヤー個別に立てる、`quality==BEST` を検査。
- **G-DEPTH-1（ビット深度）**: 深度検証は**PIL禁止**。PNGの**IHDR(byte24)直読み**か **ffprobe（`rgba64be`）**で確認。暗部ヘイズ＋glow/soft-light/multiply積層は8bitで必ず縞（16bit=約65万色 vs 8bit=約9,238色）。
- **G-OUT-1（最終結合）**: 完成mp4を ffprobe で `duration`／`r_frame_rate`／`pix_fmt`（10bit=`yuv420p10le`／8bit=`yuv420p`）／解像度を機械検査。**末尾0.5sが黒画面でないこと**＋コンタクトシートで全カット目視。
- **G-ENV-1（環境）**: ログのprintは**ASCIIのみ**か `PYTHONIOENCODING=utf-8`（cp932で非ASCII「—」等が全死）。git-bashに`bc`無し→`awk`。停止はプロセス一覧＋PIDで実確認。
- 優先度（費用対効果）: **G-GEN-2 > G-CAP-1 > G-TIME-1 > G-COMP-1 > G-DEPTH-1**。

### ✅ 決定事項（オーナー確認済 2026-07-17）
1. **AI動画エンジン=Wan2.2 A14B**（SVDから切替確定）。§5.5数値で運用。
2. **静止画の元=Codex**（40場面・生成済）。Codex絵を720pにconformしてWan i2v入力に使う。
3. **出力=32bit float合成＋16bitマスター＋10bit/8bit二本立て。fps=48**（なめらか優先）。ship-gate/受領=8bit H.264版。
4. **動かす範囲（決定）**: 「見せ場は本当に動かす（Wan）＋残りは奥行き2.5D＋滑らかな動く文字」。**Wan i2v=約12カット（見せ場）**、残り約28カットは Depth 2.5D（意味あるドリー・視差）＋motionkit/AEのキネティック文字で**静止させない**。紙芝居ゼロが受入基準。
5. **文字=Oswald/Anton に格上げ（全話統一）**。全カット「動く文字」を滑らかに（§5.6）。

---

## 5.6) 文字・タイポグラフィ設計（オーナー要望「文字にこだわる」・binding）

> 既存の単一情報源 `remotion/src/brand.ts` と `motionkit/KineticCaptions`・数字部品に**合わせる**（新規フォント体系を勝手に作らない＝二重実装禁止）。AEの見せ場カットもこの色・字形に一致させる。

### 実ブランド値（brand.ts＝この値で組む）
- 色: 本文=白 `#F5F7FA` ／ 強調=ゴールド `#E5B53A` ／ アクセント=電光ブルー `#1F6BFF` ／ 地=黒 `#0A0A0C`・紺 `#0B1A2B` ／ 補助=シルバー `#C8CDD6`。
- **フォント（オーナー承認2026-07-17で格上げ済・全話統一）**: 表示/本文=**Oswald**（条件ゴシック）／数字カード・特大見出し=**Anton**／代替=**Archivo**。すべてOFL・商用OK。`remotion/public/fonts/` に配置＋Windowsインストール済（AE用）。`brand.ts` の `font.display/number/body` 更新済。旧Impact/Trebuchetはフォールバックのみ。ライセンス=`public/fonts/LICENSE_FONTS.md`。
- **fps=48**（オーナー承認・なめらか優先）。解像度1920×1080。※brand.video.fpsは全話共有=30のままにし、**EP38コンポジションを48fpsで登録**（他話に影響させない）。音声尺は不変・フレーム数のみ増える。

### キネティック字幕（本文の読み）
- 既存 `KineticCaptions` を使用。既定 `style='maskslide'`（overflow:hidden マスク切り上がり＝落ち着き字幕）。決め語のみ `emphasis`（ゴールド＋スケールパンチ＋グロー）。
- 落ち着き字幕ルール（[[feedback_anim_caption_polish]]）: **リード0.60s**・**文法単位で分割**（`_smart_split`）・medium.en 語同期・ボトムセーフ配置・白本文＋強いドロップシャドウ。速い登場は `Trail`（モーションブラー）。opacity単独禁止（translateY/scale併用）。線形なし（spring/ease）。

### 数字カード 〔CARD〕（この回の主役演出・語同期）
台本の `〔CARD: …〕` を、発話語ちょうどでキネティックに出す。**motionkitの既存部品**で組む（新規実装しない）:
- 対象と部品:
  - `90 SECONDS` / `28 YEARS` → **NumberTicker**（カウントアップ・ease）＋単位を `emphasis`。
  - `8.4%` / `7–11×` → **NumberTicker**＋`RadialGauge`/`ComparisonBars`（州平均8.4% vs 実質50%の対比が刺さる＝**ComparisonBars**推奨）。
  - `$2.8 MILLION` → **NumberTicker**＋`StampReveal`（"FINDER'S FEE"を打刻→消して真名"BRIBE"に置換の演出可）。
  - `3 MONTHS` / `NO LAWYER` / `THOUSANDS VACATED` → **StampReveal**／マスク切り上がり大見出し。
- 動きの型（全カード共通）: マスク切り上がり登場 → 数字カウントアップ（ease・0.6–0.9s）→ 保持中は微ブレス（静止させない）→ 退場はワイプ or フェード＋わずかなpush。ゴールド強調＋グロー。速い登場に `Trail`。
- 配置: フルフレーム中央 or 下三分の一。背後の映像を殺さない不透明度・シャドウ。セーフマージン=左右90px/上下60px。

### タイトル/章/名前
- OP・幕頭タイトル → `ActTitle`/`CinematicTitle`（文字スタッガー＋マスク切り上がり）。ゴールド1語強調。
- 事実の下三分の一（例: "Luzerne County, PA" / "Mark Ciavarella — Juvenile Court Judge" / "Juvenile Law Center, Philadelphia"）→ `LowerThird`。**実名は事実のみ・肖像/顔は出さない**（テキストのみ）。日付・出典表記もここ。
- 判決の瞬間（28 YEARS / 17.5 YEARS）→ `VerdictReversal` に数字カードを重ねる。

### 品質ゲート（文字にも適用）
- 線形アニメ禁止・opacity単独禁止・マスク切り上がり基本・速い登場はTrail・保持中も微動・タイミングはfpsから算出（`Math.round(fps*sec)`）。`animation_mix`/`caption_integrity` ゲートを通す。
- **可読性実測**: カード表示中に背景と本文のコントラスト比を確認（白#F5F7FA on 暗部で AA以上）。語同期ズレは faster-whisper 語タイムで±1フレーム以内。

---

## 6) Codex 画像プロンプト共通ルール

- **共通スタイル接尾**（各プロンプト末尾に付ける）:
  `, cinematic still, dramatic volumetric lighting, moody, deep blacks and navy blue with electric-blue and gold accents, silver highlights, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, film grain, no text, no watermark, no logo`
- **共通ネガティブ**:
  `text, words, letters, captions, watermark, logo, real celebrity, recognizable real person, identifiable face, child face, cartoon, low quality, deformed, extra limbs, nudity, explicit, gore, blood, weapon, self-harm`
- **安全（本件特有・厳守）**:
  - 実在人物（判事・被害者・家族）の肖像/認識可能な顔は**出さない**（後ろ姿・シルエット・顔を外す・手元）。
  - **子供は必ず匿名化**（後ろ姿・シルエット・遠景・持ち物のみ）。特定個人を想起させる描写をしない。**露出・危害・拘束のグラフィック禁止**。
  - **自死は象徴のみ**（空の椅子・消えた光・畳まれた上着・母の沈黙）。方法・手段・遺体・手首・首・薬・高所などを一切描かない。
  - 読める判決文/警察文書/実在施設名の看板は作らない（雰囲気のみ）。人物像はOK（実在肖像のみ禁止）。
- 保存: `H:\pd-media\assets\ai\kidsforcash\<SPN-ID>.png`（`import_to_remotion.py` が取り込み）。各画像 stock_ledger に source=ai_codex / commercial_use=allowed / sha256 を1行記録。

---

## 7) 画像プロンプト（Codexへ）

**S01 — フック/学校の廊下（普通の子供）**
An empty American high school hallway in cold morning light, rows of lockers, a lone teenage figure seen only from behind walking away, ordinary and innocent, faint unease in the shadows, no face + [共通スタイル]

**S02 — 悪ふざけの投稿（軽微な"非行"）**
A dim bedroom at night lit only by an old computer monitor glow, a silhouetted teenager from behind at a desk, a generic glowing screen (no readable text), utterly mundane, symbolic of a small harmless prank + [共通スタイル]

**S03 — 90秒の審理（弁護士なし）**
A small, cold juvenile courtroom, a towering empty judge's bench in shadow above, a tiny lone child-sized silhouette standing far below it, one harsh overhead light, overwhelming imbalance of power, no faces + [共通スタイル]

**S04 — 手錠 / 連行（匿名）**
Close-up of small handcuffed wrists in the dark, cold steel catching a sliver of blue light, anonymous, no face, quiet and wrong + [共通スタイル]

**S05 — 営利拘置施設（外観）**
A stark modern for-profit detention facility at dusk behind tall chain-link and razor wire, cold institutional building, security lights, a corporate coldness to it, empty, foreboding + [共通スタイル]

**S06 — 独房の孤独（子供）**
A bare juvenile cell at night, a thin mattress on a metal bunk, a small barred window casting a cold blue grid on the floor, a child-sized empty space, utterly lonely, no person + [共通スタイル]

**S07 — 金の流れ（象徴・汚職）**
Symbolic image of shadowed hands exchanging a thick envelope of cash under a desk in the dark, a judge's gavel resting nearby out of focus, corruption and secrecy, cold light, no faces + [共通スタイル]

**S08 — "子供＝商品"（最も重い象徴）**
A powerful symbolic composition: a cold institutional conveyor or ledger of small anonymous silhouettes being processed into a building, each faceless child reduced to a number, a faint gold price-tag motif, deeply unsettling and restrained, no graphic content + [共通スタイル]

**S09 — 郡の拘置所が閉じる（財源を断つ）**
An old public county juvenile facility with its lights going dark, a chain and padlock on a gate, "closing" mood, cold blue abandonment versus the bright private facility in the far background + [共通スタイル]

**S10 — 空の椅子（喪失／自死は象徴のみ）**
A single empty chair by a window in a quiet family home at dusk, soft fading light, a folded jacket left on it, profound absence and grief, restrained and tasteful, no person, nothing graphic + [共通スタイル]

**S11 — 母の沈黙（悲嘆）**
A lone adult silhouette seen from behind standing in a doorway of a modest home, shoulders heavy, warm light ahead and cold shadow behind, quiet unbearable grief, no face + [共通スタイル]

**S12 — 最高裁 / 州最高裁（外観）**
A courthouse building at dusk, dramatic low angle, marble columns lit gold against a deep navy sky, solemn and monumental, the weight of the law returning, cinematic + [共通スタイル]

**S13 — 記録の抹消（数千件）**
Symbolic image of countless case files and juvenile records dissolving into light, dark drawers of paper being cleared, thousands of small records lifted away, a sense of wrongs being erased and undone, cold-to-warm light shift + [共通スタイル]

**S14 — 司法が司法を裁く（転回）**
A symbolic image of a judge's empty robe hanging in shadow while a single shaft of accusing light falls on it, the accuser becomes the accused, powerful reversal, no person, no face + [共通スタイル]

**S15 — 押収 / 証拠（EvidenceReveal下地）**
Abstract dark composition of stacked cash bundles, a signed contract (illegible), and a gavel under a single hard light, evidence of a bribery scheme laid out, cold and forensic + [共通スタイル]

**S16 — 手錠をかけられる側（加害判事・匿名）**
An anonymous figure in a suit seen from behind having handcuffs applied, cold courthouse steps at dusk, press-light flare implied but no readable text, the powerful brought low, no face + [共通スタイル]

**S17 — 官僚機構 / システムの腐敗**
Abstract symbolic image of an endless dark records system, rows of identical drawers vanishing into shadow, several drawers glowing red implying systemic corruption rather than a single error, cold and impersonal + [共通スタイル]

**S18 — 権力 vs 子供（対比）**
Symbolic diptych: on one side a vast cold institutional structure implying power and money, on the other a single small child-sized silhouette implying helplessness, a thin line of light dividing them, moody, no faces + [共通スタイル]

**S19 — 平穏な日常が一変（射程・誰にでも）**
A calm ordinary American suburban street in soft morning light, warm and safe, children's bicycles on a lawn, but a single distant unmarked official car approaching, foreshadowing that this could happen to any family, cinematic contrast + [共通スタイル]

**S20 — 正義/権利の線（テーマ・ED）**
A single stark line of golden light drawn across a dark marble courthouse floor, small footprints approaching it, symbolic of the promise that the law is supposed to protect the powerless, minimal, reverent, open-ended epilogue mood + [共通スタイル]

*(各 S01–S20 を 5〜6 枚ずつ連番出力＝合計 約110枚。)*

---

## 8) props / 型（Bookends・CTA）

- OP/ED は既存テイスト軸（Bookends正典）を流用・ブラッシュアップ可（参照 [[feedback_opening_ending_taste]]）。深海シアンのOpening.tsxは技術デモで不採用。
- タイトル候補（英語・LEGAL帯・要オーナー承認／A案推し）:
  - A: **"The Judges Who Sold Children"**
  - B: **"He Was Paid to Send Kids to Jail"**
  - C: **"A Judge Got $2.6 Million to Lock Up Children"**
- サムネ案（LEGAL帯・「え？なにそれ？」）: 法服の判事のシルエット＋小さな子供の後ろ姿＋札束/「$2.6M」モチーフ、コピー「SOLD FOR CASH」系。実在肖像・実名施設は不可。数字は要検証確定後に焼く。
- **登録CTA（変換対策・必須）**: ED直前ナレ＋固定コメント＋説明欄トップ。文言は語同期で自然に。

---

## 9) Claude側の残工程（画像と並行）

研究 → **claim台帳（数字/年号/量刑/人数/氏名/施設名を1文1典拠で確定）** → 検証済み台本(script_verified) → shotlist/asset_map → 新パイプライン(2.5D/3D/語同期/ナレ入りフック)で制作 → ship-gate受領（`check_final_acceptance.py --emit-receipt`）。

- データ土台: Studioクッキー再取得 ＋ `audienceRetention` 計測を本件で仕込む。
- 事実確認の最重要点（review_required・出荷前に潰す）:
  1. 受領金額（2.6M か 2.8M か・誰から誰へ）
  2. 量刑（Ciavarella 約28年 / Conahan 約17.5年）と罪名（RICO 等）
  3. 抹消された審判の件数・対象人数（"約数千件/約2,500件"の別）
  4. 象徴被害者の事実関係（15歳少女の偽ページ・3か月／自死した少年と母の面罵）——**私人・未成年・自死**につき、事実の正確性と描写の節度を最優先。
  5. 施設名・時系列（スキーム期間・起訴年・判決年）。
- リスク再確認: **R2**。公開前にオーナー/法務レビュー（未成年・自死・実名判事）。ship-lockはAPR記載の許容偏差のみ通す。

---

### 付記（この設計書の位置づけ）
- 本書は Codex が単体で画像生成に着手できるよう、画像プロンプトと安全規範を本文に書ききっている。台本・尺・アニメ・受入の拘束仕様は `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` と `.claude/rules/19-ship-gate.md` に従う。
- **未確定はオーナー承認事項**: 最終タイトル/サムネ、13–14分への尺拡張、自死描写の配慮レベル、公開スケジュール。
