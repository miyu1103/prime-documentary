# Thumbnail and Title System（サムネイル＆タイトル完璧設計書）

ステータス: 設計（draft）

前提・仮定:

- 本書は CANON / `CLAUDE.md` / `.claude/rules/` に従う。新規有料ツール・素材サブスクは前提にしない。
- 本書は `docs/27_THUMBNAIL_AND_TITLE_EXPERIMENT_SYSTEM.md`（以下「doc27」）の**実装・運用ガイド**である。doc27 が方針（package hypothesis / pair scoring / experiment record / decision rule）を定義し、本書はそれを「タイトルの型」「サムネの型」「制作フロー」「品質ゲート」「per-episode 雛形」に落とす。doc27 と矛盾する判定はしない。
- 本書は `docs/motion-quality-gate.md`（以下「motion gate」）と整合する下位・特化ゲートである。motion gate が動き（モーション）を判定し、本書は静止サムネ＋タイトルを判定する。Severity は新設せず、`docs/12_QUALITY_GATES_AND_ACCEPTANCE.md`（以下「12」）の S0〜S5 を流用する。
- サムネは **1280×720**（`BRAND.thumb`）。本編動画は 1920×1080（`BRAND.video`）。サムネは Remotion `<Still>` で書き出す。
- ブランドトークンの単一情報源は `remotion/src/brand.ts`（後述）。ハードコード hex を増やさず、原則 `BRAND.color` を読む。
- **実在人物の肖像は使わない**（`CLAUDE.md` 不変条件11 / doc27 §8）。匿名シルエット・象徴オブジェ・劇的キー画像で「顔の代わり」を作る。
- 生成画像は証拠ではない。事件被害者を刺激的に使わない。実在ロゴ・商標の偶発生成を確認する（doc27 §8）。
- タイトル英語が本編、必要に応じ日本語メモを併記（内部運用用、サムネ上には日本語を載せない）。

---

## 0. 既存サムネ部品の正確な参照（壊さず統合）

本書は新規コンポーネントを作らない。以下の**既存部品をそのまま使う**。各話のサムネは「データ（variant 配列）の追加」と「`<Still>` / `<Composition>` 登録」だけで増やす。

| 部品 | パス | 役割 | 主な props |
|---|---|---|---|
| `ThumbnailFrame` | `remotion/src/components/ThumbnailFrame.tsx` | 汎用1行タイトル型。黒地＋gold horizon＋白大文字＋PD mark。背景は任意の still、無ければグラデ。 | `title: string`／`backgroundSrc?: string\|null`（http or staticFile相対）／`variant?: 'left'\|'center'` |
| `ThumbConcept` | `remotion/src/compositions/ThumbConcept.tsx` | 好奇心ギャップ2行型（line1 白＋line2 gold）＋象徴シンボル。背景 still があればシンボルは自動で隠れる。 | `kicker?`／`line1`／`line2`／`sub?`／`symbol: 'gavel'\|'bars'\|'scales'\|'letter'`／`backgroundSrc?: string\|null`／`showSymbol?: boolean` |
| `CarpenterThumbnail` | `remotion/src/compositions/CarpenterThumbnails.tsx` | 各話量産型。背景写真＋暗幕＋coded motif（Phone/Trail）＋kicker＋2行見出し＋PDフッタ＋"SYMBOLIC RECONSTRUCTION"表記。 | `variantIndex?: number`（`thumbnailVariants[]` を参照） |
| `RileyThumbnail` | `remotion/src/compositions/RileyThumbnails.tsx` | 同上。`motif: 'search'\|'warrant'\|'police'\|'life'\|'locked'\|'premium'`。`splitHeadline` で自動改行、`primarySize` 自動縮小。 | `variantIndex?: number`（`rileyThumbnailVariants[]`） |
| `TerryThumbnail` | `remotion/src/compositions/TerryThumbnails.tsx` | 同上。`motif: 'gap'\|'frisk'\|'scale'\|'street'\|'phone'\|'dense'\|'cinematic'\|'codexKeyart'`。背景なし variant はグラデにフォールバック。 | `variantIndex?: number`（`terryThumbnailVariants[]`） |

各話の `ThumbVariant` 型（量産型の共通形）:

```ts
type ThumbVariant = {
  id: string;        // 'thumb01' ...
  headline: string;  // 大文字3〜4語。splitHeadline が自動改行
  kicker: string;    // 上部の小見出し（事件名 or 賭け金）
  image?: string;    // staticFile 相対パス（省略可＝グラデ）
  motif: ...;        // coded 図形（実在人物なしの「顔の代わり」）
  accent: 'blue' | 'gold';
};
```

共通の描画作法（3部品で統一済み・本書の「型」の根拠）:

- 背景 still は `objectFit:'cover'` + `transform:scale(1.08)` + `brightness↓ contrast↑ saturate↑`。
- 左側に強い暗幕（`linear-gradient(90deg, 黒→透明)`）で文字可読性を確保。
- 右側に accent の radial glow。`Vignette` + `Grain` で実写質感（AIっぽさ低減、`feedback_video_natural_style` と整合）。
- 見出しは `BRAND.font.display`（Impact）大文字、最終行を accent 色に。kicker は `BRAND.font.body`。
- 左下に `PRIME DOCUMENTARY`、量産型は "symbolic reconstruction" 表記（合成/再現の正直表示）。

登録パターン（`remotion/src/carpenter_index.tsx` 実例）: `thumbnailVariants.map(...)` で `id={`Carpenter-${variant.id}`}`、`durationInFrames={1}`、`width/height = BRAND.thumb` の `<Composition>` を生成。汎用2種（`ThumbConcept` / `ThumbnailFrame`）は `remotion/src/Root.tsx` に `<Still>` 登録済み。

---

## 1. 狙い / 原則

**目的: CTR と「正直さ（誇張しすぎない）」の両立。** サムネ＆タイトルは動画の装飾ではなく企画仮説の最終表現（doc27 §1）。本編が約束を回収できないパッケージは、たとえ CTR が高くても勝者にしない（doc27 §10）。

チャンネルの声 = **米国の法廷・権利を「自分ごと」に**。視聴者の日常（あなたのスマホ、あなたの逮捕、あなたのお金）と憲法判例を一直線で結ぶ。

原則（一目で守れる短い形）:

1. **1サムネ = 1メッセージ。** 焦点は1つ（主役画像1つ）。複数の主張を載せない（doc27 §4 single focal idea）。
2. **モバイル最優先。** 小さく・速いスクロールで一瞬で伝わる。10%縮小・グレースケール・1秒認識テスト（doc27 §7）を必ず通す。
3. **正直さ。** 内容と一致。釣り（本編にない驚き）を載せない。実在人物の表情・行為を捏造しない（doc27 §8）。
4. **サムネとタイトルは補完。** 同じ情報を重複させない。サムネが「驚き」、タイトルが「認識（自分ごと化）」を担う（`ThumbConcept` の設計コメントどおり）。
5. **シリーズ統一と各話差別化の両立。** 一目で PD と分かる（黒地・gold horizon・Impact大文字・PDフッタ）。各話は主役画像と motif で差別化。
6. **広告安全・中立。** 扇情・断定・差別的含意を避ける。生成画像を証拠に見せない。

---

## 2. タイトル設計（完璧な型）

### 2.1 タイトルの公式

良いタイトルは次の4レバーのうち**1〜2個**を効かせる（全部入りは散漫＝減点）。doc27 §3 の title dimensions に対応。

| レバー | 定義 | 効かせ方 | 対応 doc27 dimension |
|---|---|---|---|
| **好奇心ギャップ** | 答えを言わず疑問を立てる | "Why…?" "Can police…?" 形。前提と結論の間に裂け目を作る | causal tension / novelty |
| **衝撃の1事実** | 検証済みの驚く1事実 | 数字・年・判決比（5-4, 8-1）・期間（127 days）を1つだけ | specificity / consequence |
| **自分ごと "You/Your"** | 視聴者の所有物・身体・権利に接続 | "Your phone" "Your rights" "You" を主語/目的語に | familiarity / search language |
| **賭け金（数字）** | 失う/賭かるものを具体化 | 金額・日数・人数・票差。曖昧な「衝撃」より具体数字 | consequence / specificity |

良い例 / 悪い例:

- 良: `Can Police Search Your Phone Without a Warrant?`（好奇心＋自分ごと、内容一致）
- 悪: `SHOCKING Truth They Don't Want You To Know!!!`（中身なし・釣り・煽りすぎ＝policy risk、doc27 §6 で減点）
- 良: `127 Days of Your Location — No Warrant`（衝撃事実＋賭け金、Carpenter の実数）
- 悪: `The Most INSANE Supreme Court Case EVER`（誇張・非中立・promise mismatch）

### 2.2 ルール（チェック可能な制約）

- **文字数:** YouTube モバイル truncation を想定し、**前半 ~40〜50文字に意味が完結**するよう強い語を前に置く（doc27 mobile truncation）。全体は概ね 60 文字以内を目標。
- **前半に強い語:** "Your phone" "Can police" "127 days" 等を文頭へ。ブランド名や前置きを先頭に置かない。
- **煽りすぎない:** 全部大文字連打・感嘆符乱用・"INSANE/SHOCKING" 系を避ける。1つの強い事実で勝つ。
- **釣り禁止 = 内容一致:** タイトルの約束は本編が回収する範囲のみ（promise accuracy）。回収できない案は kill（doc27 §12）。
- **自然な英語:** ネイティブが書く語順。検索語（case名・"warrant"・"search"）を自然に含める。
- **中立:** 当事者を断定的に有罪/無罪と書かない。判例の論点で釣る。

### 2.3 運用: 1エピソードにつき A/B 用に**3案**

- 各話で **3タイトル案**を作る（公式の効かせ方を変える：好奇心型 / 衝撃事実型 / 自分ごと型 のように軸をずらす）。
- doc27 §6 の `pair_score` でサムネ3案と掛け合わせ、最良 pair を A、対照を B として実験に出す。
- タイトルは英語本編タイトル＋（内部用）日本語メモを per-episode レシピに記録（§6）。

### 2.4 既存EP向け 具体タイトル案（各2〜3案）

英語が本編タイトル。括弧内は日本語メモ（内部用、サムネ非掲載）。

**Miranda v. Arizona（黙秘権）**
1. `Why Do Police Have to Read You Your Rights?`（なぜ警察は権利を読み上げる？／好奇心＋自分ごと）
2. `He Won His Case — and Stayed in Prison`（勝訴したのに収監／衝撃ギャップ。本編で回収可なら採用）
3. `4 Words That Changed Every U.S. Arrest`（逮捕を変えた4語／衝撃事実）

**Gideon v. Wainwright（弁護人の権利）**
1. `He Defended Himself — and Lost. Then He Wrote One Letter.`（独力で敗訴、そして手紙1通）
2. `Can the State Put You on Trial With No Lawyer?`（弁護士なしで裁けるか／自分ごと）
3. `One Pencil Letter Reached the Supreme Court`（鉛筆の手紙が最高裁へ／衝撃事実）

**Mapp v. Ohio（違法収集証拠）**
1. `Can Police Use Evidence They Found Illegally?`（違法に得た証拠は使える？）
2. `No Warrant. They Searched Anyway.`（令状なしで捜索／衝撃事実）
3. `The Rule That Throws Out Illegal Evidence`（違法証拠を捨てるルール）

**FTX（暗号通貨の破綻）**
1. `How $8 Billion in Customer Money Vanished`（顧客資金80億ドルが消えた／賭け金）
2. `Your Crypto Was on Their Balance Sheet`（あなたの暗号資産が彼らの帳簿に／自分ごと）
3. `From $32 Billion to Zero in Days`（数日で320億→ゼロ／衝撃事実）

**Madoff（史上最大のポンジ）**
1. `The $65 Billion Lie That Lasted Decades`（数十年続いた650億ドルの嘘）
2. `Where Did the Money Actually Go?`（お金は実際どこへ？／好奇心）
3. `Your Statement Said You Were Rich. It Was Fake.`（明細は富裕、それは偽り／自分ごと）

**Terry v. Ohio（停止と所持品検査）**
1. `Stopped. Frisked. Was It Legal?`（停止・検査、合法か／好奇心）
2. `Police Can Search You Without a Warrant — Here's the Catch`（令状なしの検査、その条件）
3. `The 8-1 Decision That Lowered the Bar`（基準を下げた8対1判決／衝撃事実）

**Riley v. California（携帯の捜索）**
1. `Can Police Open Your Locked Phone?`（ロック中の携帯を開けるか／自分ごと）
2. `Your Phone Is Your Whole Life — Get a Warrant`（携帯＝人生のすべて、令状を）
3. `One Word From the Court: "Get a Warrant."`（裁判所の一言「令状を取れ」）

**Carpenter v. United States（位置情報）**
1. `127 Days of Your Location — No Warrant`（127日分の位置、令状なし／賭け金）
2. `Your Phone Is a Map of Everywhere You Go`（携帯はあなたの行動地図／自分ごと）
3. `Police Wanted This Map. The Court Said No.`（警察が欲した地図、裁判所はNo）

**Timbs v. Indiana（過大な没収）**
1. `They Took His $42,000 Car for a $400 Crime`（400ドルの罪で4.2万ドルの車を没収／賭け金）
2. `Can the State Seize Far More Than Your Fine?`（罰金以上に没収できる？／自分ごと）
3. `The "Excessive Fines" Rule Reaches the States`（「過大な罰金」禁止が州へ）

---

## 3. サムネ設計（完璧な型）

### 3.1 視覚階層（一目で1メッセージ）

優先順位（上から強く・大きく）:

1. **主役1つ**（画面右〜中央）: 匿名シルエット／象徴オブジェ（携帯・天秤・令状スタンプ・手紙）／劇的キー画像のいずれか1つ。実在人物の顔は使わない。
2. **見出し文字 最大3〜4語**（画面左、Impact 極太大文字）。最終行を accent 色（gold/blue）に。
3. **kicker**（事件名 or 賭け金、小さく上部）＋ accent の下線バー。
4. **ブランド要素**（gold horizon／PDフッタ／"symbolic reconstruction" 表記）。

これは既存3部品の実装そのもの（左テキスト＋右モチーフ＋暗幕＋vignette/grain）。新規構図は作らず、この階層に各話を流し込む。

### 3.2 「顔の代わり」の作り方（実在人物の肖像なし）

| 手法 | いつ使う | 既存実装での例 |
|---|---|---|
| **象徴オブジェ** | 抽象的な権利・制度 | `ThumbConcept` の gavel/bars/scales/letter、Riley の locked phone、Timbs の押収車（生成キー画像） |
| **匿名シルエット** | 「人」の存在を示すが個人を特定しない | 後ろ姿・手元・影。生成キー画像は顔を写さない構図で発注 |
| **劇的キー画像（背景）** | 場面の雰囲気（夜の街・取調室・データの光） | Carpenter の location bloom 背景、Terry の codex keyart 背景 |
| **データ可視化 motif** | 数字・期間・票差 | Carpenter の Trail（移動軌跡）、Terry の hunch→suspicion→proof スケール、Riley の life grid |

原則: **顔ではなく「象徴 × データ × 雰囲気」で感情を作る。** 生成画像は `symbolic reconstruction` と明示（捏造に見せない）。

### 3.3 文字（モバイル可読の絶対条件）

- **最大3〜4語**。`splitHeadline`（Riley/Terry 実装）が自動で2行化、長い語は `primarySize` を自動縮小。
- **極太・高コントラスト:** Impact 900。白 or gold を、暗幕＋`textShadow:'0 6px 24px #000'` の上に。背景写真には必ず左暗幕（既存実装で担保）。
- **セーフゾーン:** 端から十分内側（既存は left 46〜56px / top 48px）。**右下はタイムスタンプ回避**のため文字を置かない（PD mark/フッタは左下 or 右下小さく）。
- **色:** 1サムネで accent は1色（gold か blue）。最終行のみ accent、他は白。

### 3.4 配色・ライティング・スケール・感情

- **配色:** 黒/navy 地（`BRAND.color.ink/navy`）＋ accent（gold `#E5B53A` か electric `#1F6BFF`）＋白/silver 文字。3部品で統一済み。
- **ライティング:** 右側 accent の radial glow＋vignette で被写体に視線誘導。背景は `brightness↓ contrast↑` で文字を浮かせる。
- **被写体スケール:** 主役は画面の 1/3〜1/2 を占める大きさ（小さすぎるとモバイルで消える）。
- **感情表現:** 緊張（暗幕・vignette）、重大さ（gold＝判決・お金）、監視/技術（blue＝携帯・データ）。色で感情を出し、扇情画像に頼らない。

### 3.5 シリーズ統一 × 各話差別化

- **統一（一目でPD）:** 黒地・gold horizon・Impact大文字・左テキスト＋右motif・PDフッタ・grain/vignette。
- **差別化:** 主役画像（各話固有のキー画像）＋ motif（各話の core object）＋ accent 選択。

### 3.6 運用: 1エピソードにつきサムネ**3コンセプト（A/B/C）**

doc27 §5 の concept 群から**異なる切り口**で3つ作る（同構図の色違いは禁止＝量産の悪い例）:

- **A = human consequence**（自分ごと・賭け金。例「YOUR PHONE IS A MAP」）
- **B = system / rule**（制度・判決比。例「POLICE WANTED THIS MAP」＋"5-4 · THE WARRANT LINE"）
- **C = scale / hidden-object**（数字・隠れた事実。例「127 DAYS NO WARRANT」）

各コンセプトは既存 variant 配列に1要素追加するだけ（`id/headline/kicker/image/motif/accent`）。

### 3.7 既存EPごとの 主役画像＋文字案（各2〜3パターン・言葉で記述）

**Miranda**（`ThumbConcept` 流用、symbol=bars）
- A: 主役=独房の鉄格子シルエット／文字「WON. / STILL JAILED.」kicker "MIRANDA v. ARIZONA"（gold）
- B: 主役=空の取調室の椅子＋blueライト／文字「STAY / SILENT?」kicker "YOUR RIGHTS"（blue）
- C: 主役=4語の吹き出し記号／文字「4 WORDS / ONE RULE」（gold）

**Gideon**（`ThumbConcept`、symbol=letter）
- A: 主役=手書き手紙＋鉛筆／文字「ONE / LETTER」kicker "GIDEON v. WAINWRIGHT"（gold）
- B: 主役=空の弁護人席／文字「NO / LAWYER?」kicker "YOUR DEFENSE"（blue）

**Mapp**（symbol=scales or door）
- A: 主役=押し開けられたドア＋令状なし記号／文字「NO / WARRANT」（gold）
- B: 主役=証拠袋にバツ／文字「THROWN / OUT」kicker "ILLEGAL EVIDENCE"（blue）

**FTX**（背景=暗い取引画面の光、データ motif）
- A: 主役=溶けるコイン記号／文字「\$8B / GONE」kicker "CUSTOMER MONEY"（gold）
- B: 主役=右肩下がりチャート／文字「\$32B / TO ZERO」（blue）

**Madoff**（背景=高級だが冷たいオフィス）
- A: 主役=偽の明細書＋虫眼鏡／文字「THE / \$65B LIE」（gold）
- B: 主役=ピラミッド図／文字「WHERE'S / THE MONEY?」kicker "DECADES OF FRAUD"（blue）

**Terry**（既存 TerryThumbnails 流用）
- A: motif=gap、文字「NO / WARRANT?」kicker "HERE IS THE CATCH"（gold）
- B: motif=scale、文字「SUSPICION / IS ENOUGH?」kicker "THE 1968 RULE"（gold）
- C: motif=cinematic/codexKeyart、文字「NO / WARRANT?」kicker "TERRY STOP · 1968 · 8-1"（gold）

**Riley**（既存 RileyThumbnails 流用）
- A: motif=locked、文字「CAN POLICE / OPEN THIS?」kicker "LOCKED PHONE"（blue）
- B: motif=life、文字「YOUR PHONE / IS YOUR LIFE」kicker "RILEY v. CALIFORNIA"（gold）
- C: motif=warrant、文字「GET A / WARRANT」kicker "PHONE SEARCH"（gold）

**Carpenter**（既存 CarpenterThumbnails 流用）
- A: 背景=location bloom、文字「YOUR PHONE / IS A MAP」kicker "127 DAYS · NO WARRANT"（gold）
- B: 文字「POLICE WANTED / THIS MAP」kicker "CARPENTER v. UNITED STATES"（blue）
- C: 文字「127 DAYS / NO WARRANT」kicker "PHONE LOCATION RECORDS"（gold）

**Timbs**（symbol=押収車/天秤）
- A: 主役=高級車に押収タグ／文字「\$400 CRIME / \$42K CAR」（gold）
- B: 主役=傾いた天秤／文字「TOO / MUCH?」kicker "EXCESSIVE FINES"（blue）

---

## 4. 制作フロー

doc27（hypothesis→pair→experiment）と motion gate（Asset First）に接続する。

1. **素材棚（Asset Factory）から thumbnail 向けキー画像を選ぶ。** 顔なし・symbolic・rights-tracked・brand一致のキー画像（Codex/SDXL生成、`CLAUDE.md` §11）。新規生成は棚に無い時のみ（motion gate の Asset First と同じ）。
2. **3タイトル × 3サムネ を生成。** §2.3 / §3.6 のとおり軸をずらして作る。データは各話の `*ThumbnailVariants[]` に追加（量産型）、または `ThumbConcept`/`ThumbnailFrame` の props で（汎用型）。
3. **選定（pair scoring）。** doc27 §6 `pair_score = clarity + curiosity + complementarity + promise_match + differentiation − confusion − policy_risk`。重複 pair は減点。
4. **Remotion Still 書き出し（既存部品で）。** 量産型は `*_index.tsx` の `variants.map(...)` で `<Composition durationInFrames={1} width/height=BRAND.thumb>` を登録し PNG 書き出し。汎用型は `Root.tsx` の `<Still id="ThumbConcept"/"ThumbnailFrame">` を props 差し替えで書き出し。**新規描画コンポーネントは作らない。**
   - 書き出し例（コピー可・破壊操作なし）:
     ```bash
     # 量産型（Carpenter の variant をすべて Still 書き出し）
     npx remotion still src/carpenter_index.tsx Carpenter-thumb01 out/carp_thumb01.png
     # 汎用2行型（props 差し替えで A/B/C）
     npx remotion still src/Root.tsx ThumbConcept out/miranda_A.png \
       --props='{"line1":"WON.","line2":"STILL JAILED.","kicker":"MIRANDA v. ARIZONA","symbol":"bars"}'
     ```
5. **レビューゲート（§5）。** チェックリスト合格のみ次へ。title/thumbnail pair は人間承認境界（`.claude/rules/16-approval-boundaries.md`）。
6. **A/Bテスト（doc27 の実験系に接続）。** `experiment_id / variant IDs / impressions / CTR / watch time per impression / first 30s retention`（doc27 §9）を記録。
7. **勝者で差し替え。** 決定規則は doc27 §10（CTR 高でも初期離脱悪化なら不採用、主評価＝watch time per impression）。学習は doc27 §11 の構造で library 化（「赤文字が勝つ」のような表層ルールにしない）。

---

## 5. 品質ゲート（サムネ/タイトル専用チェックリスト）

motion gate と整合（Severity は 12 の S0〜S5 を流用、軸=不可は blocker）。public 前に title/thumbnail pair は人間承認が必須。

```
# Thumbnail & Title Quality Gate — Review Checklist
対象EP: PD-____-___-____    pair: A / B / C
タイトル案: ____________________________________
サムネ部品: ThumbnailFrame / ThumbConcept / *Thumbnail(variantIndex __)

## 一目で読めるか（Readability・mobile）
[ ] 10%縮小で1秒で主役と文字が認識できる
[ ] グレースケールでもコントラストが保たれる
[ ] 文字は最大3〜4語、極太・高コントラスト
[ ] セーフゾーン内（端から内側／右下タイムスタンプ回避）

## 内容と一致するか（正直さ・promise）
[ ] タイトルの約束を本編が回収する（釣りでない）
[ ] サムネとタイトルが補完（同一情報の重複でない）
[ ] 誇張しすぎていない（INSANE/!!! 乱用なし・中立）

## 実在人物の肖像なし・広告安全か（policy）
[ ] 実在人物の顔・表情・行為を使っていない/捏造していない
[ ] 生成画像を証拠写真として提示していない（symbolic reconstruction 表記）
[ ] 事件被害者を刺激的に利用していない
[ ] 実在ロゴ・商標の偶発生成がない／画像内文字に誤りがない

## ブランド統一か（consistency）
[ ] 黒/navy地＋accent1色（gold/blue）＋白/silver文字
[ ] Impact大文字・gold horizon・PDフッタ・grain/vignette
[ ] 一目でPDと分かりつつ各話で差別化（主役画像/motif）

## モバイルで強いか（competition）
[ ] 隣接競合サムネ並びでも目を引く（adjacent simulation）
[ ] dark/light UI 両方でタイトル truncation を確認

## A/B 3案あるか（experiment）
[ ] タイトル3案・サムネ3コンセプト（異なる切り口）がある
[ ] pair_score を算出し A/B を選定（doc27 §6）

## 判定
[ ] 合格   [ ] 不合格（Severity: S__ / blocker: __________）
コメント: ______________________________________________
```

blocker（軸=不可）例: 読めない／内容と不一致（釣り）／実在人物肖像・捏造／policy risk。これらは 12 の Visual/Package Gate も自動不合格。

---

## 6. per-episode レシピ雛形（コピペ用）

各話の `thumbnail_recipe` を per-episode に保存（`sceneType` 的な構造）。コピペして埋める。`image` は staticFile 相対パス、`motif`/`symbol` は使う部品に合わせる。

```jsonc
{
  "episode_id": "PD-YYYY-NNN-slug",
  "thumbnail_recipe": {
    "component": "TerryThumbnail",          // ThumbnailFrame | ThumbConcept | *Thumbnail
    "key_image_candidates": [               // Asset Factory の顔なし symbolic キー画像
      "terry/PD-2026-006-terry-S004-IMG-001.v001.png"
    ],
    "lead_subject": "anonymous silhouette | symbolic object | dramatic key image",
    "no_real_person_likeness": true,
    "symbolic_reconstruction_label": true,

    "titles": [                             // A/B用に3案（英語本編＋日本語メモ）
      {"id": "T-A", "lever": "self|curiosity|fact|stake",
       "en": "Stopped. Frisked. Was It Legal?", "ja_memo": "停止・検査、合法か"},
      {"id": "T-B", "lever": "fact",
       "en": "The 8-1 Decision That Lowered the Bar", "ja_memo": "基準を下げた8対1判決"},
      {"id": "T-C", "lever": "self",
       "en": "Police Can Search You Without a Warrant — Here's the Catch", "ja_memo": "令状なしの検査、その条件"}
    ],

    "palette": {"ground": "ink|navy", "accent": "gold|blue", "text": "white"},

    "variants": [                           // サムネ3コンセプト A/B/C（切り口を変える）
      {"id": "thumb-A", "concept": "human_consequence",
       "headline": "NO WARRANT?", "kicker": "HERE IS THE CATCH",
       "image": "terry/PD-2026-006-terry-S004-IMG-001.v001.png",
       "motif": "gap", "accent": "gold"},
      {"id": "thumb-B", "concept": "system_rule",
       "headline": "SUSPICION IS ENOUGH?", "kicker": "THE 1968 RULE",
       "image": null, "motif": "scale", "accent": "gold"},
      {"id": "thumb-C", "concept": "scale_hidden",
       "headline": "THE 8-1 EXCEPTION", "kicker": "NO WARRANT · LOWER STANDARD",
       "image": "terry/PD-2026-006-terry-S003-IMG-001.v001.png",
       "motif": "street", "accent": "blue"}
    ],

    "pair_scoring": {                       // doc27 §6（A/B 選定）
      "formula": "clarity + curiosity + complementarity + promise_match + differentiation - confusion - policy_risk",
      "chosen_A": {"title": "T-A", "thumb": "thumb-A"},
      "chosen_B": {"title": "T-B", "thumb": "thumb-C"}
    },

    "experiment": {                         // doc27 §9（記録）
      "experiment_id": null, "impressions": null, "ctr": null,
      "watch_time_per_impression": null, "first_30s_retention": null,
      "decision": null, "confidence": null
    }
  }
}
```

表形式の簡易版（軽い話用）:

| 項目 | A | B | C |
|---|---|---|---|
| concept | human_consequence | system_rule | scale_hidden |
| headline (≤3-4語) | NO WARRANT? | SUSPICION IS ENOUGH? | THE 8-1 EXCEPTION |
| kicker | HERE IS THE CATCH | THE 1968 RULE | NO WARRANT · LOWER STANDARD |
| key image | S004 keyart | (gradient) | S003 keyart |
| motif/symbol | gap | scale | street |
| accent | gold | gold | blue |
| title pair | T-A | T-B | T-C |

---

## 7. 参照ドキュメント

- `docs/27_THUMBNAIL_AND_TITLE_EXPERIMENT_SYSTEM.md` — 方針（hypothesis / pair scoring / experiment / decision rule / learning library）。
- `docs/motion-quality-gate.md` — モーション下位ゲート（Asset First、12 の S0〜S5 流用）。
- `docs/12_QUALITY_GATES_AND_ACCEPTANCE.md` — 全工程ゲートの上位。
- `remotion/src/brand.ts` — ブランドトークン（色・フォント・1280×720）。
- `remotion/src/components/ThumbnailFrame.tsx`／`remotion/src/compositions/ThumbConcept.tsx`／`CarpenterThumbnails.tsx`／`RileyThumbnails.tsx`／`TerryThumbnails.tsx` — 既存サムネ描画部品。
- `remotion/src/Root.tsx`／`remotion/src/carpenter_index.tsx` 他 `*_index.tsx` — Still / Composition 登録パターン。
