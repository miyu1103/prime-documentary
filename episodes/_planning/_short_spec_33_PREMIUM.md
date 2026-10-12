# 縦型ショート 完全設計書（PREMIUM tier）— 第33話 Tyler v. Hennepin County（Home-Equity Theft）

第33話（本編 `PD-2026-033-tyler`）に1対1で対応する縦型ショート **1本**。**この設計書だけで単体制作できるよう、仕様・数値・言い回しロックをすべて本文に書ききる。** 従来の `_short_spec_25〜31.md`（画像＋2.5D＋テロップ）を土台にしつつ、**「いままでより豪華」＝プレミアム・モーション層を全面採用**した上位版。EP34/35 は本書 §0/§4/§5/§10 を共通土台に、§2・§3・§6 の数値・事実だけ差し替える。

> **プレミアム化の背骨（本書が従来ショートと違う点）**
> 1. **全静止画に“本物の3D深度パララックス”**（`DepthImageV`／DPT深度マップ）。疑似2.5Dは廃止。＝紙芝居を物理的に殺す。
> 2. **数字は必ず“動く”**：没収額・投票・年号は `NumberTicker`／`MoneyFlow`／`StackedProportion`／`VoteTally`／`YearSweep`（motionkit v002）で0→値・フロー・比率アニメ。静止テロップで金額を出さない。
> 3. **映画的ブックエンド＋転換**：`CinematicTitle`（掴み）＋ `IrisTransition`／`FocusPull`（幕転換）。ただの硬いカット切替をしない。
> 4. **引用は `QuoteCard`**（Roberts の "render unto Caesar…" を打鍵表示＋帰属）。
> 5. **プレミアム背景層**：`AuroraField`／`LightRays`／`DepthParticles` を主役の裏に常時（最低3レイヤーを機械的に担保）。
> 6. すべての動きにイージング必須・等速線形禁止・opacity単独禁止（translateY/scale と併用）・複数要素はスタッガー・速い動きは motion-blur `Trail`。

---

## §0. 環境・Remotion設定（EP33-35 共通）

- **Composition**：`Short-short33-yt`（YouTube）／`Short-short33-tt`（TikTok・CTA文言のみ差替）。**1080×1920 / fps 60 / `durationInFrames = round(totalSec × 60)`**（尺はナレ実測駆動＝`shortDurationInFrames(SHORT33, 60)`）。目標尺 **62〜72秒**（法務ロックを削らず自然に。`build_short_mix.py` の実測が真値）。
- **依存パッケージ**（導入済みだが明記）：
  ```
  npm i @remotion/three @react-three/fiber three @remotion/motion-blur @remotion/media-utils
  ```
  プレミアム部品は `remotion/src/components/motionkit/`（CATALOG.md・二重実装禁止＝invariant 14）と `remotion/src/components/ShortVerticalArt.tsx` を使う。**新規に同機能を作らない。**
- **remotion.config.ts（基準値）**：`setImageFormat('png')` / `setColorSpace('bt709')` / `setPixelFormat('yuv420p')` / `setCodec('h264')` / `setCrf(16)`（サムネStillはCRF不問）。**WebGL（深度・motionkit背景）を含むレンダは `--concurrency=4`**（安定・過去のクラッシュ回避）。音声 `aac 320k`。GPU=angle。
- **音声**：ElevenLabs `VOICE_ID nPczCjzI2devNBz1zQrb / eleven_multilingual_v2`。delivery=intense(stability0.44/style0.36)・building(0.50/0.26)・calm(0.58/0.14)。生成は承認済（追加確認不要）。
- **音ミックス**：4層（BGMベッド／緊張／環境／SFX）＋ダッキング＋**2パス静的 -14 LUFS**（`build_short_mix.py` short17〜設定＝中盤の音量痩せ対策 speechnorm＋グルー圧縮）。VO間 `GAP≈1.20s`。
- **保存先**：画像＝`H:\pd-media\assets\ai\shorts\short33\` → `remotion/public/shorts/short33/` に画像と `_depth.png` を同居。音＝`…/07_audio/short33_final_mix_v002_en_us.mp3` → `public/shorts/short33/audio/`。

---

## §1. 公開ゲート・リスク

- **リスク＝低**。Tyler v. Hennepin County は **9–0 の公開SCOTUS判例**。政府（郡）は中立事実記述。**実在肖像なし**（94歳女性 Geraldine Tyler・Roberts 長官ら判事の顔/似顔/声真似 禁止＝invariant 11）。画像内に**可読な実在テキスト・ロゴ・州章・裁判所印・法典タイトルを描かない**（テロップは Remotion で焼く）。
- **1日1本・12:00 JST 予約**（`publishAt`）。新規予約前に全 `publishAt` 監査 → 空き日。**予約枠：短33 = 7/28**（34=7/29・35=7/30）。
- 出荷は **§11 実測チェックリスト全項目PASS** が条件（自己申告QC禁止＝invariant 13）。

---

## §2. FACTS LOCKED（言い回しロック・EP33 §1 準拠。逸脱禁止）

| ロック | 内容 |
|---|---|
| 事件・判決 | **Tyler v. Hennepin County, 598 U.S. 631 (2023)**。**9 to 0**。**Chief Justice Roberts** 執筆。（「600 U.S.」は誤り・使用禁止） |
| 数値（焼込可・grade A） | **94** 歳／滞納元本 **≈$2,300**／利息等含む債務 **≈$15,000**／コンド売却 **$40,000**／郡は **$40,000 全額保持**／余剰 **≈$25,000** 没収 |
| 判旨 | 債務超過分（余剰）の保持は**正当補償なき Taking＝第5修正違反**。**第8修正（過大な罰金）は判断せず**（「第8修正に違反した」と言わない） |
| 引用（逐語・QuoteCard） | Roberts：**"render unto Caesar what is Caesar's, but no more."**（カンマ含む） |
| 州フレーミング | **"most states already required the surplus be returned"**。**具体数「36」は焼かない・言わない**（意見本文未確認扱い）。保持側は "more than a dozen states still allowed it"（`Est.—PLF` 帰属）。**50−36 の算術で導出しない** |
| 用語 | "home equity theft" は批判側の呼称 → **"what critics call home equity theft"** と帰属 |
| 禁止焼込 | 購入年1999・cert日・PLF統計（`Est.`帰属なし）・州法改正の州名断定・**Hall事件の人物/金額/所在**（別事件・未裏取り）・「36」 |

---

## §3. 秒数タイムライン（全区間・VO／テロップ／プレミアム演出／深度画像／数値）

**5 VOビート構成**（実尺は下の narration が真値。以下は設計意図と割当）。各行 `[開始–終了] VO要約｜TELOP（マスク切上げ）｜PREMIUM演出（部品名・数値）｜深度画像`。

- **HOOK 0.0–7.0（intense）**
  VO: "You owe the county fifteen thousand dollars. They take your home, sell it for forty thousand — and keep every last dollar. Can they really do that?"
  TELOP: `THEY KEPT\nALL OF IT`（fast・Trail layers5/lag1.2）
  PREMIUM: 冒頭 `CinematicTitle`（0.0–2.0で章題を奥からドリーイン・spring damping18）→ **`NumberTicker` で $15,000 と $40,000 を左右に0→値（1.0秒・Easing.out(cubic)）**、その差額帯が赤く残る。背景 `LightRays`（強度1.15）。
  深度画像: **01**（夜の一軒家＋差押え札のシルエット）

- **BEAT1 0.0–? / L2（building）— 事件**
  VO: "That's what happened to Geraldine Tyler. At ninety-four, she owed about fifteen thousand … Hennepin County … seized it, sold it for forty thousand — and kept the entire amount, including roughly twenty-five thousand that had nothing to do with the debt."
  TELOP: `$15K OWED` → `$40K SOLD` → `$25K TAKEN`（3枚をカット毎にスタッガー・各 frame−i*5）
  PREMIUM: **`MoneyFlow`**＝債務$15,000ぶんだけ郡へ流れ、**余剰$25,000が“戻らず”郡側に留まる**フロー（矢印＋滞留・2.4秒）。**`StackedProportion`**＝$40,000 のうち「借金37.5%／余剰62.5%」を積み棒で提示（62.5%側を強調色）。数値は `NumberTicker`。
  深度画像: **02**（郡庁舎/公的窓口の抽象・書類の束）→ **03**（空き家のコンド・鍵）→ **04**（$の山＝没収の象徴）

- **BEAT2 ?–? / L3（building）— 憲法**
  VO: "The Constitution's Fifth Amendment says if the government takes your property, it has to pay for it. That extra twenty-five thousand was hers, not the county's. Keeping it … was the government taking far more than it was owed."
  TELOP: `TAKE IT →\nPAY FOR IT` → `THE SURPLUS\nWAS HERS`
  PREMIUM: **`DocHighlight`**＝第5修正 Takings 条項の“意味”をハイライト（実法文テキストは描かない・語句カードで）→ **`MechanismReveal`**＝「差押→売却→余剰は本人へ戻るべき」の3段機構をステップ点灯（`ProcessSteps`可）。背景 `AuroraField`（低速）。
  深度画像: **05**（天秤/秤＝“more than owed”の象徴・ただし天秤の使い過ぎ回避＝本話は1回だけ）→ **02**再掲（別モーション）

- **BEAT3 ?–? / L4（intense）— 判決（クライマックス）**
  VO: "In 2023, the Supreme Court agreed — nine to zero. Chief Justice Roberts wrote that a taxpayer must render unto Caesar what is Caesar's, but no more. Pocketing the surplus was an unconstitutional taking. Most states already banned what critics call home equity theft — now it's the rule everywhere."
  TELOP: `9 – 0\n(2023)` → `CAESAR —\nBUT NO MORE` → `THE RULE\nEVERYWHERE`
  PREMIUM: **`YearSweep` 2023**（時間軸を2023へスイープ・0.8秒）→ **`VoteTally` 9–0**（9枚が順に点灯・スタッガー各3f・最後に確定パルス）→ **`QuoteCard`**（Roberts 逐語を打鍵＝TerminalType風・帰属 "Chief Justice Roberts, 2023"）→ 締めに `RegionHighlightMap`（"most states already required return"・**点灯数は具体化しない**・全米が満たされる示唆で締め）。転換は `IrisTransition`。
  深度画像: **06**（最高裁の抽象・列柱と光）→ **07**（家に戻る鍵／余剰が本人へ戻る象徴・bright-line motif）

- **CTA ?–end / L5（calm）**
  VO: "Watch the full story on the channel. Follow for more."（TikTok版=`Full story on our profile`）
  PREMIUM: `CinematicTitle` の逆再生的なアウトロ＋ `DepthParticles` を強め（count22）。
  深度画像: **07**

---

## §4. プレミアム演出仕様（数値付き・品質ルール反映）

**全ビート共通の“動きの契約”（等速線形禁止）**
- 深度スチル `DepthImageV`：`planeGeometry(2.25,4.0,220,380)` / `scale 1.2` / `displacementScale 0.5`（fast=0.62）/ camera `fov42 z5.2`、dolly `interpolate(f,[0,dur],[0,1],Easing.out(cubic))`、`Math.sin(dolly·π)·0.14·dir` の微小オービット。**全静止画に適用（例外なし）**。
- カット・イン（各ビュー先頭）：`spring(damping200,stiffness140,mass0.5)` で `scale 1.05→1.0`・`opacity 0→1`（opacity単独禁止＝scaleと併用）。
- テロップ（上部ゾーン y≈120–430）：**overflow:hidden＋translateY(110%→0)** のマスク切上げ、行ごとに `frame − i*5` スタッガー、`Easing.out(cubic)`、常時 `Math.sin` の微小フロート。金額・年号・投票は**テロップに数字を置かず** §4数値部品側で動かす。
- 速いカット（hook・9–0点灯）：`@remotion/motion-blur` `Trail(layers5,lag1.2,opacity0.4)`。
- 数値部品（motionkit v002）：`NumberTicker` 0→値 1.0s `Easing.out(cubic)` ＋アクセント下線。`MoneyFlow`/`StackedProportion`/`VoteTally`/`YearSweep`/`Price/Donut`系は本話では **MoneyFlow・StackedProportion・NumberTicker・VoteTally・YearSweep** を採用。色は series 色でなく中立トークン（白 #fff／副 #c8d2e6／地 #6b7688）＋アクセント1色。
- 転換：`IrisTransition`（幕間0.5s）・`FocusPull`（被写体送り）。`GlitchCut` は本話の格に合わないので不使用。

**豪華さの機械フロア（本話・実測対象＝§11）**
- 深度カット率 **100%**（全 image ビューが `DepthImageV`）。
- 動く数値/データ部品 **≥5種**（NumberTicker・MoneyFlow・StackedProportion・VoteTally・YearSweep）。
- プレミアム背景層 常時 **≥1**（LightRays/AuroraField/DepthParticles のいずれか）。
- 平坦（無モーション）フレーム **0**。

---

## §5. レイヤー構成（下→上・各ビート最低5層＝豪華担保）

1. **地色** `BRAND.color.ink`（全面）
2. **プレミアム背景** `AuroraField` or `LightRays`（screen/soft-light・低速ドリフト）
3. **深度スチル主役** `DepthImageV`（3Dメッシュ変位＋カメラdolly）
4. **モーショングラフィック中景** `MoneyFlow`/`StackedProportion`/`VoteTally`/`YearSweep`/`QuoteCard`/`MechanismReveal`（ビート別）
5. **粒子/発光** `DepthParticles`（screen）
6. **グレード＋グレイン＋ヴィネット**（`grade` / `Grain opacity0.05` / `Vignette`）
7. **テロップ（上）** マスク切上げ／**字幕（下 y1280–1560）** ナレ同期（両ゾーン厳密分離・重ねない）

> 最低3レイヤー要件を、実際には **背景＋深度主役＋モーショングラフィック＋粒子** の4層以上で常時満たす。

---

## §6. 画像リスト＋プロンプト（7枚・text-free 象徴・肖像/文字/印章なし）

共通スタイル接尾辞（各プロンプト末尾に付与）：
*"museum-grade cinematic symbolic documentary still, vertical 9:16 full-frame, black and deep-navy base, electric-blue signal light, silver highlights, restrained muted-gold accent, film grain, dramatic moody lighting, photorealistic, shallow depth of field, symbolic reconstruction not authentic footage. No on-screen text, no watermark, no logo, no identifiable real person, no readable letters or numerals, no government seal."*

| stem | 内容（symbolic・no likeness/text） |
|---|---|
| short33_01 | 夜、静かな郊外の一軒家（またはコンド）に無地の差押え札が下がるシルエット、窓に一つだけ灯り、冷たい月光。人物なし・可読文字なし |
| short33_02 | 冷たい公的カウンター／官庁の窓口の抽象、無地の書類束と1本のペン、青い実務照明、顔なし・書類に文字なし |
| short33_03 | 空き家のコンドの玄関、鍵が一つ、埃と斜光、無人。プレート/番地なし |
| short33_04 | 積み上がった無地の紙幣束の山を上から冷光が照らす、うち一部だけが暗く沈む（＝没収の象徴）、通貨記号/額面なし |
| short33_05 | 精密な真鍮の天秤が大きく傾き、一方の皿が過剰に重い（＝“more than owed”）、深い余白、文字なし（天秤は本話で1回のみ） |
| short33_06 | 最高裁を思わせる抽象的な大理石の列柱と一条の光、荘厳・静謐、看板/文字/印章なし |
| short33_07 | 家の玄関に鍵と一条の暖かい光が戻ってくる象徴（＝余剰が本人へ戻る／bright-line motif）、広い負空間、文字なし |
| short33_thumb | 家のシルエットと、そこから流れ出て戻らない冷たい光の帯＝“取られた余剰”。高コントラストのキービジュアル、顔/文字なし（見出しは ShortThumb で焼く） |

深度マップ：`C:\Users\aab15\ComfyUI\venv\Scripts\python.exe tools/depth/gen_depth.py remotion/public/shorts/short33`（`Intel/dpt-large`・`_depth.png` を同居生成）。

---

## §7. props / 型定義（データファイル `remotion/src/data/short33.ts`）

`ShortData`（既存型）に準拠：`shortId:'short33'` / `episodeId:'PD-2026-033-tyler'` / `durationSec` / `narrationSrc` / `captions`(=`short33_timing` 自動生成) / `bgmSrc:null` / `ctaTextYT` / `ctaTextTT` / `beats`（`buildBeats()` が `LINE_WINDOWS×CUTS` から生成）。
`Cut`：`{line,id,src(=img('0N')),kind:'image',motion:'pushin'|'kenburns'|'parallax',telop?,fast?,art?}`。**`art` に §3 のプレミアム部品を割当**（`{kind:'bignum'|'vote'|'diagram'|'doors'|'citation'}` ＋必要なら motionkit を `art` 拡張で追加）。Root 登録は **深度版を本番**にする：`Short-short33-yt`/`-tt` は `defaultProps` に `depth:true`。

---

## §8. 音設計

4層＝(1)BGMベッド（factory棚・厳粛/希望の2部）(2)緊張レイヤー（判決前）(3)環境（室内/官庁の静寂）(4)SFX（札の軋み・書類・数値点灯ブリップ・9–0確定インパクト・引用の打鍵）。ダッキング＋2パス静的 -14 LUFS。ED（CTA）は BGM を**切りよく**終わらせる（尺いじらない）。

---

## §9. サムネ（A/B＋coverfirst）

- **A**：`ShortThumb-short33`／見出し `THEY KEPT\n$25,000`／badge `9–0`／背景 `short33_thumb.png`
- **B**：見出し `A $15K DEBT.\nA $40K HOME.`／badge `TAKEN`
- Shorts公開時は**先頭1.5sにカバー焼き込み**（coverfirst・libx264 crf18）。カスタムサムネはAPI設定（検索/関連/動画タブで表示・Shorts系は動画コマ仕様＝coverfirstで担保／確実化はアプリ/Studioでカバー選択）。

---

## §10. 確認方法・レンダ・予約コマンド

```bash
# 1) ナレ → ミックス（字幕タイミング自動生成）
.venv/Scripts/python.exe scripts/gen_short33_narration.py
.venv/Scripts/python.exe scripts/build_short_mix.py --short 33 --ep PD-2026-033-tyler
# 2) 画像（ローカルSDXL/SD3.5）→ public 配置 → 深度マップ
.venv/Scripts/python.exe scripts/gen_short33_images.py
#   （画像を public/shorts/short33/ にコピー後）
C:\Users\aab15\ComfyUI\venv\Scripts\python.exe tools/depth/gen_depth.py remotion/public/shorts/short33
# 3) プレビュー
cd remotion && npm run studio   # Short-short33-yt を選択
# 4) レンダ（WebGL含むので concurrency=4）
npx remotion still  src/index.ts ShortThumb-short33 out/short33_thumb.png
npx remotion render src/index.ts Short-short33-yt out/short33_yt.mp4 --concurrency=4
npx remotion render src/index.ts Short-short33-tt out/short33_tt.mp4 --concurrency=4
# 5) coverfirst（先頭1.5sサムネ焼込）→ 予約 7/28
bash scratchpad/coverfirst.sh 33
.venv/Scripts/python.exe scripts/schedule_short_youtube.py --short 33 --publish-at 2026-07-28T03:00:00Z --dry-run
.venv/Scripts/python.exe scripts/schedule_short_youtube.py --short 33 --publish-at 2026-07-28T03:00:00Z
```

---

## §11. 出荷前チェックリスト（実測・自己申告禁止／フレーム目視）

1. **深度**：全 image ビューが `DepthImageV`（深度カット率100%・`_depth.png` 全枚存在）。歪み（ラバーシート）目視なし。
2. **豪華フロア**：動く数値/データ部品 ≥5種が実在（NumberTicker/MoneyFlow/StackedProportion/VoteTally/YearSweep をフレームで確認）。平坦フレーム0。
3. **法務ロック**：`9–0 (2023)`・第5修正Takings（第8修正に触れない）・余剰~$25,000・Roberts引用逐語・「36」不使用・"home equity theft"帰属 — テロップ/字幕/説明文で確認。
4. **テロップ×字幕**：上下ゾーン非重複。金額はテロップに焼かず数値部品で提示。
5. **偽テキスト/印章/肖像**：SDXL画像に可読の偽テキスト・州章・裁判所印・実在肖像なし（1枚ずつ目視）。
6. **尺**：62–72秒band。字幕はナレに一致・切れ目自然。
7. **カバー**：coverfirst 先頭＝サムネ一致。thumbnail_set true。
8. **予約**：private＋publishAt 7/28、他 publishAt と衝突なし。sha照合一致。

---

### EP34/35 差し替えメモ
- **EP34 rolin**（空港・現金・民事没収／R2）：§2 を EP34 §1 の事実ロックに、§6 を「空港/現金/旅行」レーン画像に、数値部品は没収額＋“無起訴”の強調（`MoneyFlow`＋`StampReveal`＝NO CHARGES）。予約 7/29。
- **EP35 hinders**（自営・銀行・IRS・structuring／R2）：レーン「自営/銀行/IRS」、`RecordsScan`＋`ProcessSteps`（分割入金→構造化認定）＋立法逆転。予約 7/30。
- 素材・色・音は3話で**完全分離**（話またぎ被り禁止）。

---

## §12. 設計書ファイルの契約（機械が検査する）

本書は**1本ぶんの演出仕様**を書ききるためのもの。それとは別に、**話ごとの設計データ**を
`episodes/_planning/short_designs/<EPID>.design.v001.json` に置く。ここが台本・キネティック・
角度の唯一の真実で、`build_tiktok_queue.py` も `gen_short_publish_config.py` もここを読む。

```
py -3.11 scripts/check_short_design.py <design.json>     # 1本
py -3.11 scripts/check_short_design.py --all             # 全部
```

### 何を検査するか

| 検査 | なぜ在るか |
|---|---|
| `source_lines` の各行が**脚本に逐語で存在する** | 不変条件1。ショートも台本である。捏造した一文は、上流で書かれ検証された一文を指せない |
| `source_lines` が空でない | 出典なしの断定を作らない |
| 行IDが `L1..L8` で連番・8行 | レンダーが8行の背骨を前提にしている |
| キネティック文字の `anchor` が**そのセリフに実在する語** | 存在しない語で切ると、誰も言っていない所に文字が乗る |
| 同じ話の中で `angle` が重複しない | 3本が同じ話をしない |

### 実測（2026-08-11 初回実行）

既存63本を通したところ **99件**の問題が出た。内訳は `source_lines` 空が54件、脚本と
一致しないものが41件。後者は**言い換えや脚本改訂によるずれを含み、そのまま捏造とは限らない**
——判定には個別確認が要る。**新しい設計書はこの検査を通してから着手すること。**

EP66 の設計書を書いたときも、この検査が自分のミスを1件捕まえた（`short273` のキネティック
文字が、そのセリフに無い語を指していた）。書いた本人が読み返しても見つからなかった種類の
間違いで、機械にしか見えない。

