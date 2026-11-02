# EP37 — Florence v. Board of Chosen Freeholders — 設計 ＋ Codex画像プロンプト

- Episode ID: `PD-2026-037-florence` / slug `florence`
- 題材: Florence v. Board of Chosen Freeholders of the County of Burlington (2012, **5–4**, Kennedy majority)
- 事実の骨子: Albert Florence は**既に払い終えた罰金**の令状で車中で逮捕され、6日間・2つの拘置所に勾留、**両方で身体（裸）検査**を受けた。最高裁は、罪の軽重に関わらず**一般収容前の一律ボディチェックは合憲**と判断。
- テーマ: 第4修正 × **身体のプライバシー・尊厳** × 「軽微な逮捕でここまで？」
- 勝ち筋適合: 身体プライバシー系＝当ch最高残存(King APV92%)。未掘り。「え、それ合法？」最大。
- リスク: **R2**（公開判例・実在人物は肖像/顔を出さない・裸検査は**象徴表現のみ・非グラフィック**・広告安全）。
- 尺: 11–12分（フック→OP→4幕→ED）。

## 構成（ナレ入りフック＝新方針）
- **フックは本編を全部作ってから最後に組む**（§10踏襲＝新規制作せず、**本編の最高の決めカット/名ゼリフを流用**して再構成）。今回の新点＝**そこにナレを乗せる＋語同期字幕**（無音フックをやめる）。
  - フックナレ(約12–15秒・叩き台):「払い終えた罰金の令状で逮捕。そして裸にされ、身体検査された、二度も。2012年、最高裁の答えは"合法"。これは、国家があなたの身体にどこまで踏み込めるかを決めた事件だ。」
- OP: ブランドタイトル
- 幕1: 逮捕の夜（払い済みの罰金・書類の誤り）
- 幕2: 拘置所2か所・身体検査（象徴表現）・尊厳の問題
- 幕3: 最高裁へ・5–4・多数意見（安全 vs 尊厳）と反対意見
- 幕4: 射程（誰にでも起きうる）・ED・次回引き

## 画像枚数（密度・重要）
- 過去は**枚数不足＝紙芝居**の一因。11–12分は**約4.5秒ごとに別画像**へ切替＝**合計 約100〜120枚**を狙う。
- 方法: 下記の**各シーンにつき5〜6バリエーション生成**（角度・構図・寄り/引き・光の向き・被写体位置を変える）。20シーン×5〜6＝**約110枚**。
- Codexへ: 「各プロンプトを、構図/カメラ/ライティングを変えて**5〜6枚ずつ**出力。`<SPN-ID>.png`, `<SPN-ID>_02.png`… と連番保存」。

## 台本＝作品賞級（最重要・binding）
> オーナー厳命: **台本はかなりこだわる。パルムドール級の内容に。** 正典=`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（アカデミー脚本基準）。
- 一流ノンフィクション作家の筆致（AI臭ゼロ）。**一人の人間の尊厳の物語**として書く（判例解説でなく、Albert という個人に起きた不条理→普遍へ）。
- 構造: 強いフック(問い)→人物と日常→事件(逮捕の理不尽)→拘置所と検査(尊厳の喪失)→最高裁の緊張(安全 vs 尊厳・5-4)→**転回**(それが"合法")→普遍化(誰にでも)→余韻。因果で繋ぐ。
- 事実性厳守: claim台帳で1文1典拠。争点は中立帰属(多数/反対)。数字/年号/条文/事件番号は要レビュー。
- **台本は3回書く**（初稿→批評→改稿）。ナレ本文は完成後に変えない。

## 意味の一致（最重要・binding）— 「ナレが言っている事を、その画で示す」
> オーナー指摘: これまで**素材を適当に並べてナレをあてこんでいた＝意味が繋がっていない/雑**。今回はこれを仕組みで直す。参照 feedback: [[feedback_animation_still_too_little]] [[feedback_perceptual_motion_and_verify]] [[feedback_pd_craft_directives]] [[feedback_video_natural_style]]。
- **台本が先。次に scene_plan で 1文（1ビート）ごとに**: `visual_question / visual_verb / start_state / end_state / eye_target / sync_words / source_type / truth_status` を必ず埋める。**その文が言っている内容を、そのまま示す画/動画/アニメを割り当てる**（汎用B-rollの流し込み禁止）。
- **語同期を接着剤に**: 決め所の語（"strip-searched" "already paid" "the Supreme Court" "9-4/5-4" "your body" 等）を faster-whisper の語タイムに合わせ、**その語が発せられた瞬間に対応する画/リビールが出る**。
- **意味の流れ＝ナレの論理と一致**: 逮捕→書類の誤り→拘置所→身体検査→尊厳→最高裁→5-4→射程→権利の線、の順で画も進む（下記S01-S20はこの順＝ナレのビート順に対応）。飾りだけの画・脈絡ない転換は禁止。
- **素材の被り禁止**（話またぎ/話内とも）。意味のある反復のみ可。
- 各カットは静止で止めない（2.5D/意味あるモーション）＝紙芝居ゲート＋knowledgeの動き量下限を満たす。

## 新ツール活用 ＋ アニメ必須（binding）
> オーナー指摘: EP37は**新導入ツールをフル活用**。**アニメが今まで全く使われていない**問題もここで解消。
- **全カットに意味あるモーション**（静止画のKen Burnsだけで止めない＝紙芝居ゼロ）。動きの大きさ下限を機械ゲート化。
- 割り当ての目安（意味に合わせて）:
  - **ヒーロー静止画 → 2.5D（Depth V2＋SAM2の精密切り抜き・自然ドリー）**：S03手錠, S05検査室, S06尊厳, S08最高裁, S13権利の線, S14/S20 等。
  - **数字/対比/票/引用/判決 → コア5部品**：罰金 vs 拘留日数=PenaltyVsProperty、"strip search legal?"=QuoteUnderExamination、**5–4**=VerdictReversal、逮捕→2拘置所→最高裁の経路=CaseJourney、書類/証拠=EvidenceReveal。
  - **法廷/章の舞台 → 3D Evidence Room（Blender・カメラ移動）**：幕頭・判決の場・章転換。
  - **薄い空気感 → Wan2.2 AI下地**（雨/霧/光・冒頭やトランジションのみ・破綻しない題材）。
  - **実景B-roll → OpenCLIP意味検索**で意味の合う実写を選ぶ（手選び廃止）。
  - **字幕 → faster-whisper語同期**（発話語ハイライト）。ナレ入りフックも語同期。
- 受入: `animation_density`＋動き量(optical-flow)下限＋footage_diversity＋caption同期 の各ゲートを通す。

## Codex 画像プロンプト共通ルール
- **共通スタイル接尾**（各プロンプト末尾に付ける）:
  `, cinematic still, dramatic volumetric lighting, moody, deep blacks and navy blue with electric-blue and gold accents, silver highlights, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, film grain, no text, no watermark, no logo`
- **共通ネガティブ**:
  `text, words, letters, captions, watermark, logo, real celebrity, recognizable real person, identifiable face, cartoon, low quality, deformed, extra limbs, nudity, explicit, gore`
- **安全**: 実在人物の肖像/認識可能な顔は出さない（後ろ姿・シルエット・顔を外す）。裸検査は**絶対に非グラフィック**（閉まる鉄扉・無人の検査室・外された靴紐やベルト・孤独なシルエット等の象徴）。読める判決文/書類は作らない（雰囲気のみ）。人物像はOK（実在肖像のみ禁止）。
- 保存: `H:\pd-media\assets\ai\florence\<SPN-ID>.png`（`import_to_remotion.py`が取り込み）。各画像 stock_ledger に source=ai_codex/commercial_use=allowed/sha256 を1行記録。

---

## 画像プロンプト（Codexへ）

**S01 — フック/逮捕の夜**
Night traffic stop on an empty American highway, a lone dark SUV pulled over, red and blue police lights flaring through light fog, a silhouetted figure seen from behind stepping out, tense cinematic mood + [共通スタイル]

**S02 — 払い済みの罰金（書類の誤り）**
A single official-looking paper document lying under a desk lamp in the dark, a faint "PAID" stamp impression (illegible), a court gavel and a pen beside it, a subtle red error-mark, symbolic of a bureaucratic mistake + [共通スタイル]

**S03 — 手錠**
Close-up of handcuffed hands in the dark, cold steel catching a sliver of blue light, anonymous, tense, no face + [共通スタイル]

**S04 — 拘置所入口（intake）**
A stark jail intake corridor at night, harsh overhead lights, a heavy steel door at the end, long shadows, cold institutional atmosphere, empty, foreboding + [共通スタイル]

**S05 — 身体検査（象徴・非グラフィック）**
An empty, clinical search room seen through a doorway, a single hanging fluorescent light, a lone metal chair, a discarded belt and shoelaces on a cold floor, a closed steel door, deeply symbolic of loss of dignity, no person, restrained and tasteful + [共通スタイル]

**S06 — 尊厳 vs 国家（象徴）**
A single vulnerable human silhouette standing small inside a vast dark institutional hall, one shaft of pale light from above, overwhelming scale of the state around the tiny figure, no face, powerful and somber + [共通スタイル]

**S07 — 2つの拘置所（移送）**
A prison transport van on a dark road between two distant fenced facilities, cold blue night, razor-wire fences catching light, sense of being moved and processed + [共通スタイル]

**S08 — 最高裁 外観**
The U.S. Supreme Court building at dusk, dramatic low angle, marble columns lit gold against a deep navy sky, solemn and monumental, cinematic + [共通スタイル]

**S09 — 法廷内（無人・象徴）**
An empty grand courtroom interior, the raised judicial bench in shadow, one beam of light across nine empty high-backed chairs, dust motes, solemn, no people + [共通スタイル]

**S10 — 5–4（僅差）**
Abstract symbolic image of a balance scale tipping just barely to one side, five gold weights versus four silver, dramatic single spotlight, dark background, tension of a narrow decision + [共通スタイル]

**S11 — 安全 vs 尊厳（多数意見の論理）**
A symbolic split composition: on one side cold orderly rows of jail cells implying safety and control, on the other a single soft human silhouette implying dignity, a thin line of light dividing them, moody + [共通スタイル]

**S12 — 射程（誰にでも）**
A long line of anonymous silhouetted people waiting under institutional lights, each faceless, implying "any one of us," cold blue tone with a single warm light, somber crowd + [共通スタイル]

**S13 — 権利の線（テーマ）**
A single stark line of golden light drawn across a dark marble floor, a bare footprint approaching it, symbolic of the constitutional limit on the body, minimal and powerful + [共通スタイル]

**S14 — ED/次回引き**
A dark doorway opening onto a faint distant light, a lone figure walking away seen from behind, contemplative, open-ended, cinematic epilogue mood + [共通スタイル]

**S15 — 連行（車内後部）**
Interior of a police car at night from behind, an anonymous silhouetted figure in the back seat behind a mesh divider, red and blue light washing across, rain on the window, no face, tense and quiet + [共通スタイル]

**S16 — 独房の孤独**
A bare jail cell at night, a thin mattress on a metal bunk, a small barred window casting a cold blue grid of light on the floor, utterly empty and lonely, no person + [共通スタイル]

**S17 — 官僚機構の誤り（システム）**
Abstract symbolic image of an endless dark filing/records system, rows of identical drawers vanishing into shadow, one drawer glowing red implying a single fatal clerical error, cold and impersonal + [共通スタイル]

**S18 — 多数意見 vs 反対意見（対比）**
Symbolic diptych of two facing lecterns in a dark hall, one lit cold institutional blue (order/safety), one lit warm gold (dignity/dissent), a beam of light between them, tension of a divided court, no people + [共通スタイル]

**S19 — 平穏な日常が一変**
A calm ordinary suburban American street in soft morning light, warm and safe, but with a single distant police car approaching, foreshadowing that this could happen to anyone, cinematic contrast of safety and threat + [共通スタイル]

**S20 — 第4修正/憲法（象徴）**
A weathered parchment of the Bill of Rights lit by a single warm light in the dark, the Fourth Amendment area glowing faintly (illegible), a silver quill and a shaft of gold light, reverent and constitutional + [共通スタイル]

*(各 S01–S20 を 5〜6 枚ずつ連番出力＝合計 約110枚。)*

---

## Claude側の残工程（画像と並行）
研究→claim台帳→検証済み台本(script_verified)→shotlist/asset_map→**新パイプライン(2.5D/3D/語同期/ナレ入りフック)で制作**→ship-gate受領。データ土台=Studioクッキー再取得＋`audienceRetention`計測を仕込む。
