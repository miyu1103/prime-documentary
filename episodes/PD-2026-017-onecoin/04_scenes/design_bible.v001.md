# EP17 「ONECOIN / THE MISSING CRYPTOQUEEN」 — Design Bible (30分・作家性最優先)

> Episode ID (予定): `PD-2026-017-onecoin` · Topic ID: `TOP-20260627-017`
> Format: **mid-feature**（中尺・約30分）／ Language: **English narration**（ElevenLabs master）
> Status: **DESIGN DRAFT**（未承認。topic/thesis/final-script/first-cut/title-thumb/公開 は人間ゲート）
> Owner note: この文書は「設計の確定版骨子」＝Titan design_bible と同じ位置づけ。実制作は `/new-episode` で workspace を切ってから。
> Ambition: **「情報を伝える動画」ではなく「賞を狙える1本の短編映画」。** その判断基準＝§3 SIGNATURE と §7 ACCEPTANCE CONTRACT。

---

## 0. なぜこの題材か（一行で）

OneCoin／ルジャ・イグナトヴァ。**40億ドル超を集め、2017年に消え、今もFBI最重要指名手配。**
**暗号通貨の話ではない。「あなたはまだ間に合う」という希望を売った女と、それを一番熱心に守った被害者たちの話——"乗り遅れる恐怖"が、検証しない理由になる話。**

---

## 1. CORE（背骨）

- **Thesis**: *A lie that gives people hope will always outsell a truth that offers them nothing. The crowd did not fall for the con despite being warned — it defended the con because of what believing it made them feel.*
- **Viewer promise**: By the end you will understand why a coin with **no blockchain at all** spread across the world, why the victims fought hardest to protect it — and why the same hunger lives in you.
- **Controlling emotion**: 嘲笑ではなく**自己認識の不安**。「騙された愚かな他人」ではなく「**間に合いたかった自分**」。
- **Logline**: *She built a global empire on a coin that did not exist; the more impossible the promise, the harder people fought to believe it. Then she vanished — and the believers kept paying.*
- **The fact that IS the theme**: OneCoin に**ブロックチェーンは存在しなかった**。検証するものが何も無かった。なのに史上最大級の詐欺になった。
- **観客の鏡（"意味"の核）**：FOMOと所属欲求が、検証を省かせ、嘘を"自分の物語"にする。**Titanの「信念 vs 警告」の双子**。

### タイトル候補（English / 映画として）
1. **"Nothing"** — *The Woman Who Sold a Coin That Did Not Exist* ★本命（"無"を冠に）
2. **"You Are Not Too Late"**（嘘の標語をそのまま冠に）
3. **"The Queen of Nothing"**
> 実在人物の顔は使わない（invariant 11）。象徴物＋余白＋大きな1フレーズでCTRと品位を両立。

---

## 2. FORM（形式の発明）＋ STRUCTURE（30分・3楽章）

### 2.1 形式の発明 — 「映画そのものを、あの詐欺と同じ構造にする」
観客を**信者と同じ順序で誘惑し→信じさせ→"そこには何も無かった"と落とす**。形式が主題を演じる。
- 第1楽章では**まだ批判を言わない**。あなたが少し信じたくなることが、第3楽章の証拠になる。

### 2.2 三楽章（色と音で語る）
検証は **mid プロファイル**（§8）で **27–33分** / 約 **4,100–4,700語**（150wpm）+ 設計された沈黙・映像。

| # | 時間 | 章 (chapter_id) | function | 色 | 観客の感情 | 章末の崖 |
|---|------|------------------|----------|----|-----------|----------|
| — | 0:00–1:30 | `cold_open` | hook | 黒→金 | 喉元をつかむ | タイトル "Nothing" |
| 1 | 1:30–11:00 | `the_promise` | seduction | **黄金** | 高揚・欲望 | 最初に「証拠を見せて」と言った者が現れる |
| 2 | 11:00–21:00 | `the_crack` | turn | **蛍光灯の白** | 不安・苛立ち | 群衆は**警告者の方を憎む** |
| 3 | 21:00–28:30 | `the_void` | reveal | **黒** | 戦慄・自己認識 | 種明かし＝"無" |
| — | 28:30–30:00 | `coda` | mirror | 白い光 | 余韻・問い | 空港の白へ消える後ろ姿／暗転 |

### 2.3 連結ルール（受賞作の裏ルール）
- 章は **「だから／しかし」** で繋ぐ（"それから"＝AI-filler禁止）。
- **未回収の問い（open loop）を常時1–2本**：冒頭「満員のステージはなぜ空になったのか」を§3で爆発。
- 結末を**解決しない**：彼女は今もどこかにいる。サスペンスは「捕まるか」でなく「**なぜ我々は信じたか**」。

### 各楽章の中身
**COLD OPEN (0:00–1:30)** — ロンドンの満員アリーナ、黄金のドレス、万雷の拍手、"You are not too late." → プライベートジェット → **無音** → FBI手配ポスター。死は見せない、ここでは"消失"を見せる。→ TITLE: **"Nothing"**。

**第1楽章 THE PROMISE (金)** — ルジャは何者か。Oxford的経歴・TED的舞台・"Bitcoin killer"。なぜ普通の人が全財産を入れたか＝**乗り遅れた後悔の救済**。MLM構造（紹介で増える"家族"）。*まだ嘘とは言わない。* *崖：一人が「ブロックチェーンを見せて」と言う。*

**第2楽章 THE CRACK (白)** — 技術者が内部から見たもの（"作るべきブロックチェーンが存在しない"）。調査記者・規制当局の最初の警告。だが**群衆は警告者を裏切り者として攻撃する**＝信仰の自己防衛。*崖：警告は黙殺され、ルジャは増資を続ける。*

**第3楽章 THE VOID (黒)** — 種明かし：**台帳は空だった**。数字は手で打ち替えられていた。2017年、彼女は登壇予定の会場に**現れず消える**。画面が文字通り"空"になる。*あなたが第1楽章で感じた高揚＝証拠。*

**CODA (白い光)** — 被害者は今も払い続ける者がいる。FBI手配だけが残る。空港の白へ消える後ろ姿、**到着の記録は無い**。最後の一行→暗転：*"How late are you willing to be — to be sure?"*

---

## 3. SIGNATURE DEVICES（"受賞シーン"＝単独でトロフィー級）

台本・絵・音をここに集中。**顔なし＝抽象＝アート映画の文法**を武器に。

1. **空の台帳（The Empty Ledger）** — 存在しないブロックチェーン。何も書かれていない帳簿／リンクの無い鎖。全編に回帰する中心モチーフ。
2. **穴の空いたコイン** — 中心が"無"の通貨。光が穴を抜ける。
3. **黄金→白→黒** — 楽章を色で語る（誘惑→直視→空虚）。
4. **満員→無人のステージ** — 同じ構図の前後対比。拍手→静寂。
5. **音の腐敗（The Curdle）** — 歓声のうねり → ホワイトノイズ／静電気 → たった一人の声 → **無音**（Titanの沈黙の系譜）。
6. **手で打ち替わる数字** — 台帳が"計算"でなく"創作"である一瞬。
7. **空港の白い光** — 到着記録の無い消失。終幕の一枚。

---

## 4. VISUAL DESIGN（三層：象徴SDXL × 確立b-roll × 意味グラフィック）

VIDEO_RULES準拠。1カット1–2レイヤ。配色＝楽章ごと（金/白/黒）。**実在人物の肖像なし・実物を"その事件の実物"として提示しない（illustrative/disclosed）。画面内テキストはRemotion側。**

### 4.1 Factory 素材棚（`select_factory_assets.py`）
| 用途 | theme | 使いどころ |
|---|---|---|
| 群衆・高揚 | event_stage / crowd / spotlight（無ければ urban_night, light: stage_glow） | 満員アリーナ・拍手・舞台の金 |
| 富と特権 | `finance_money`: stack_of_hundred_dollar_bills / gold_bars / open_briefcase | "希望を金で買う" |
| データ/虚構 | `surveillance_tech`: server_room_blue / data_center / world_map_dark | "ブロックチェーン"の見立て→第3楽章で"空"に反転 |
| 書類/帳簿 | `documents_paper`: contract_signing / magnifying_glass / newspaper_macro；texture: aged_document | 台帳・契約・報道 |
| 喪失/空虚 | `atmosphere_symbolic`: single_chair_empty_room / candle_in_dark / shattered_mirror；light: tv_screen_glow | 無人のステージ・被害 |
| 移動/消失 | urban_night: airport / drone_city_aerial_night；particle: bokeh / static_noise | 失踪・白い光・comms static |

### 4.2 SDXL ヒーロー画像（Codex / A1111 :7860 / juggernautXL）
house style 踏襲（cinematic documentary still, chiaroscuro, **NEGに identifiable face / recognizable real person / brand markings を維持**）。楽章の色（金/白/黒）をプロンプトに織り込む。中核10枚は §9（別途 ai_prompts で76枚に展開）。

### 4.3 意味グラフィック（Remotion code＝"意味"の層）
- **空の台帳アニメ**：行が増えるはずが、何も書かれない。
- **MLM増殖ツリー**：紹介で指数増殖→崩壊で一斉に消える。
- **"集めた額" vs "実在した額(=0)"** の対比バー。
- 失踪のタイムライン（2014設立→2016ピーク→2017消失→指名手配→現在）。
日付・数値は claims と一致。顔・ブランド無し。

---

## 5. AUDIO DESIGN（4層・narration master = テンポ）

| 層 | 設計 |
|---|---|
| **Narration（EN）** | 第1楽章は**美しく誘う**トーン（あなたを共犯にする）。第3楽章で温度を落とす。English, ElevenLabs master。|
| **Music（Suno取込・素材として）** | M1 誘惑（高揚する上昇）→ M2 不穏（低い脈動）→ M3 空虚（崩れて消えるドローン）→ Coda（ピアノ一音＋無音）。|
| **Ambience** | アリーナの残響・空調・空港・群衆のざわめき・静電気。|
| **SFX** | 拍手の壁／通知音（紹介報酬）／キーボード打鍵（数字の創作）／**歓声→ホワイトノイズの腐敗**／**種明かしの完全無音**。|

**原則**：山場は「ため→開放」。**"無"は無音で抜く**。群衆の喧騒と、検証の沈黙をコントラスト。

---

## 6. 品格・FACT・RIGHTS・BAN-SAFETY（R3想定）

1. **被害者を見下さない**。全財産を失った普通の人々＝**道徳の中心**。"ざまあ"厳禁。
2. **存命の逃亡者（ルジャ）は断定しない**＝起訴・指名手配・公的記録ベースで「**alleged / charged / according to the indictment**」。**曖昧さは芸術であって中傷ではない、の線を厳守**。
3. **共犯とされる存命者**（関係者・MLM上位）は documented のみ。未確定の動機を創作しない。
4. **実在人物の肖像・声の再現なし**（invariant 11）。象徴物のみ。
5. **stock/AIは"実物"として提示しない**（illustrative/disclosed）。
6. **要確認リスト（一次ソースで埋める）**：OneCoinに実blockchainが無い旨の専門家/技術者証言・US DOJ起訴状・FBI手配・各国規制当局の警告/摘発・集金総額の推計レンジ・失踪の日時/場所・関係者の有罪認否。**公開前に再検証＋法務レビュー**（Theranos R3と同格の扱い）。

---

## 7. ACCEPTANCE CONTRACT（手直しゼロ設計＝この設計書を100点にする中核）

> **過去の事実**：手直しは前工程でなく**後工程に集中**（Riley v007 / Carpenter v008 / Madoff v010 / Miranda v005 / Lange v005、events内 "caption" 85回）。原因＝**「validator PASS」を"完成"と誤認**し、**実ファイルでしか分からない欠陥**（字幕・音声・絵の被覆・尺・黒画面）を後で発見していたから。
> **対策**：その欠陥クラスを**全部、設計段階で受け入れ基準として事前登録**し、**実ファイルの独立測定**でしか合格にしない。Definition of Done を引き上げる。

**正典（拘束）：`docs/PD_ONE_PASS_PRODUCTION_SPEC.v1.md`** ＝ 全失敗モード（BGM/声/字幕/画質/Maxクオリティ/素材活用/アニメ/フック/4部構成/サムネ/CTR…）の「具体仕様→ゲート→検証コマンド」一覧。本§7はそのEP17インスタンス。矛盾時は正典が優先。

**鉄則：Definition of Done ＝「validator PASS」ではない。「正典の全ハードゲートを実レンダ済みファイルで独立測定し通過（`check_final_acceptance.py <NN>` exit 0）」。自己申告QC禁止。**

| # | 過去に手直しを生んだ欠陥 | 教えた話 | 事前登録ゲート（実ファイル測定） |
|---|---|---|---|
| G1 | **字幕**（最頻・85回） | 全話 | 字幕がナレ100%を被覆／±120ms以内で同期／空・重複・はみ出し無し。`captions` QC json で合否。|
| G2 | **声がSAPI/低品質** | EP14 | 本番声＝**ElevenLabs master**であること（SAPIはタイミング下書きのみ）。波形/メタで検証。|
| G3 | **黒画面・絵の穴** | EP14 | 全スパンに**動く絵**（静止画禁止＝Ken Burns/parallax/MovingVideo）。設計沈黙ビート以外に黒フレーム無し。コンタクトシートで全カット確認。|
| G4 | **実尺が帯外** | EP14 / runtime-band | **mid帯 27–33分**（目標~30）を**実mp4で**測定（`check_runtime_band.py`）。ナレだけで尺を満たさない＝設計沈黙/映像で帯に入れる。|
| G5 | **命名衝突** | shorts | Remotion composition id / data ファイル / public パスは `onecoin` 名前空間で固定。衝突チェックをレンダ前に。|
| G6 | **リビジョン増殖**（v007/v008/v010） | 全話 | 後工程の手戻りは「初版で基準未達」のサイン。**初レンダ前に G1–G4 を満たす設計**（字幕台本・声・被覆・尺）を確定してからレンダ。|
| G7 | **サムネ/公開API** | PD-001 | thumbnails.set はAPI不可＝**手動アップロード前提**で設計。|
| G8 | **事実の後出し修正**（EP16 v002） | EP16 | 研究段階で**引用は逐語固定・claim台帳とscriptの数値を一致**。公開前ファクト再検証パケットを最初から作る。|

**この契約の意味**：Codexの**初回レンダがG1–G8を狙って作られる**ので、「作ってから直す」ではなく「**基準を満たして初めて出す**」。これが v002→v010 の連鎖を断つ唯一の方法。

---

## 8. PRODUCTION PIPELINE

### 8.1 中尺プロファイル（新規ADR — Claude先行）
`validate_episode.py` は standard(10.0–12.8) と feature(55–65) を持つ。**30分は未定義**。Titan の `decisions/0003-feature-duration-profile.md` と同型で **`mid` プロファイル（27–33分 / wpm150）** を1本ADRに起こし、`manifest.target_duration_minutes=30` をキーに参照させる（検証の弱体化でなく明示的追加・invariant 15）。**台本検証の前に用意**。

### 8.2 分担（Claude左 / Codex右）
- **Claude（左）**：topic → research(`pd-research`, §6要確認) → claims/sources → thesis(本書) → outline(3楽章) → **script.en + script.annotated**（~4.5k語）→ `validate_episode.py`(mid) で script_verified → shotlist + ai_prompts + thumb_prompts + **fact_recheck パケット**。
- **Codex（右）**：SDXL生成 → factory抽出 → code-graphics → Remotion `OneCoinPremium`（`onecoin_roughcut.ts`/`onecoin_captions.ts`、Root.tsx登録）→ audio 4層(`build_onecoin_audio_v001.py`)→ libx264 render → §7ゲート測定 → package。

### 8.3 Remotion / Render
- `OneCoinPremium`（`RoughCut.tsx`/`*Premium.tsx`系を拡張、~54,000 frames @30fps＝30分）。章＝chapterIdでグルーピング。動かない絵禁止。
- 章単位レンダ→FFmpeg concat→`libx264 -preset slow -crf 17 -pix_fmt yuv420p`、音別ミックス→`aac 192k`。NVENC不可（quality-first）。出力＝`H:\pd-media\episodes\PD-2026-017-onecoin\07_edit\v001.mp4`（hash登録）。

---

## 9. SDXL PROMPT PACK（中核10枚・house style）

共通 STYLE：`, cinematic documentary still, dramatic chiaroscuro lighting, photorealistic, ultra detailed, volumetric light, subtle film grain, shallow depth of field, masterpiece, ultra high resolution, 16:9`（楽章色を追加：gold rim light / cold fluorescent white / deep black）
共通 NEG：`text, letters, words, watermark, logo, signature, caption, brand markings, identifiable face, recognizable real person, celebrity likeness, deformed, extra fingers, bad anatomy, low quality, blurry, cartoon, anime, oversaturated`

1. `a vast arena bathed in golden light, a single empty spotlight on a stage where a figure once stood, thousands of empty seats, awe and absence` — cold open / 満員→無人
2. `an open ledger book with blank glowing pages, a chain of links dissolving into nothing, cold light` — empty ledger（中心モチーフ）
3. `a single coin with a hole bored through its center, light passing through the void, macro` — coin of nothing
4. `a golden cascade of one-hundred-dollar bills falling into an open briefcase, warm seductive light` — the promise (gold)
5. `a branching tree of glowing nodes multiplying exponentially, a pyramid of light` — MLM growth
6. `a hand typing numbers into a glowing spreadsheet in a dark room, the numbers invented not calculated, cold fluorescent white` — fabricated ledger
7. `a lone analyst lit by a cold monitor in a dark room, asking a question the crowd does not want answered` — the warning (white)
8. `a server room going dark, racks of blank black screens, the data that was never there` — the void (black)
9. `an empty private jet stair under a white airport light, no figure, no arrival recorded` — the vanishing
10. `a single FBI-style wanted poster pinned in darkness, the face left as blank silhouette (no real likeness), one cold light` — still at large

各6バリエ→QC→usableのみ採用→manifest登録。

---

## 10. 次アクション（承認ゲート順）

1. **題材＆thesis承認**（owner gate）：EP17=OneCoin/mid/30分/本thesis を採択 → `/new-episode` で `PD-2026-017-onecoin` workspace 生成。
2. **mid プロファイル ADR**：`validate_episode.py` 拡張（Claude）。
3. **Research**（`pd-research`）：§6要確認リストを一次ソースで。
4. **Script**：3楽章 ~4.5k語、script_verified(mid) まで。
5. **fact_recheck パケット**を最初から作成（R3・法務レビュー前提）。
6. **Codex引き継ぎ**：§7 ACCEPTANCE CONTRACT を満たす初レンダ → 各ゲート実測 → first cut。
7. 人間ゲート：final script / first cut / title・thumb（手動）/ 公開予約。

---
*この設計の100点性は「美しいだけ」では成立しない。§3（作家性）と §7（手直しゼロの受け入れ契約）の両方を満たすこと＝再現可能・再開可能・改善可能。実値（事実・尺・hash）は各工程で確定し、合否は常に実ファイルの独立測定で決める。*
