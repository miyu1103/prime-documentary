# EP65 marmet — サムネ ヒーローショット & タイトル v001

**Episode:** `PD-2026-065-marmet` · *Marmet Health Care Center, Inc. v. Brown*, 565 U. S. 530 (2012) (per curiam)
**Status:** 設計。**Codex が下のヒーロープレートを生成 → オーナーが1枚選択 → 合成側で 1280×720 に文字を乗せて書き出し。**
**Binding:** `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` 行11・12・13 ／ `episodes/PD-2026-065-marmet/episode_spec.v001.json`
（`thumbnail_candidates_min: 3` · `forbidden_subjects` · `forbidden_claims`）
**Art source:** `episodes/_planning/EP65_marmet_CODEX_BATCH_A.v001.md` §5 の **THUMB 3枚 = `R217` `R218` `R219`**（既発注）
＋ 本書で追加する **`R224`**（§7 へ追記が必要・下の §6）
**保存先（生成物）:** `H:\pd-media\assets\ai\marmet\R217.png` … `R219.png` `R224.png`（長辺3840px以上・16:9・PNG）
**保存先（合成物）:** `episodes/PD-2026-065-marmet/10_thumbnail/thumbnail.optionN.v001.png`（1280×720）
選択1枚を `episodes/PD-2026-065-marmet/09_package/thumbnail.selected.v001.png` へコピー。

---

## 0. この話に固有の絶対条件（1枚でも破ったら全部作り直し）

行11–13 の一般則に、EP65 の記録が課す制約を足したものが下の表である。**上から順に強い。**

| # | 条件 | 根拠 |
|---|---|---|
| T1 | **罫線の上の一筆は、絶対に文字として読めてはならない。**筆記体・イニシャル・文字らしい形は即不合格。ヒーローは「**罫線と、字に見えない一筆**」か「**ペンだけ**」の二択である | spec `forbidden_subjects`（readable text …）／ BATCH_A §1 Q2 ／ FILM_BIBLE §3 |
| T2 | **プロンプト本文に、書かれた名前を表す英単語（sign- 系の名詞）を一語も書かない。**BATCH_A の223本は設計としてその語を0回に保っている。本書の `R224` も0回である | spec `notes`（"the word for a written name still appears zero times in any prompt body"） |
| T3 | 患者・傷害・死・看護・病室・臨床機材を**一切描かない**。人物を出す場合も**顔を写さない** | spec `forbidden_subjects` 1・4 ／ 台帳 ⛔-07 |
| T4 | 実在と特定できる施設・建物・看板・ロゴ・印章を出さない。**実在人物の肖像なし** | spec `forbidden_subjects` 3・9 ／ CLAUDE invariant 11 |
| T5 | 生成画に**文字・数字を焼き込まない**。文字は合成側でのみ乗せる | 行11（背景画＋見出しは別レイヤー） |
| T6 | 見出しは **UPPERCASE・3〜4語**。巨大な主体・非常に高いコントラスト・**320px で読める** | 行12 |
| T7 | 地色は **黒／濃紺**、アクセントは **ゴールド `#E5B53A` か エレクトリック `#1F6BFF`**、文字は **白／シルバー** | 行12 |
| T8 | 選択済みサムネの **mean luma ≥ 33** かつ **contrast (luma stddev) ≥ 40**。両方 HARD | `scripts/check_final_acceptance.py` `THUMB_MIN_MEAN_LUMA=33.0` / `THUMB_MIN_CONTRAST_STD=40.0` |
| T9 | タイトルは **60字以内・フック先頭**。**A/B ペアを最低2組**出す（本書は4組） | 行13 |

### T8 についての注意（この話だけの衝突）

BATCH_A §2 の `[STYLE]` は本編の統一トーンとして *"flat overcast Appalachian daylight, low contrast, low-key"* を課している。
**これは行12 の「非常に高いコントラスト」と T8 の輝度床に正面から衝突する。**扱いは次のとおりに固定する。

- `R217` `R218` `R219` は **本編プレートとして発注済みであり、プロンプト本文を1文字も変えない**
  （spec `notes`：R001–R219 は ids・prompt bodies ともに byte-identical で機械検証済み）。
  → **明るさとコントラストは合成側で作る**（§4 のグレード指定）。
- `R224` は**サムネ専用に新規発注する**ので、**`[STYLE]` を使わず、スタイルを本文に書き切る**（§3 の `R224`）。
  `[NEG]` だけは BATCH_A §2 のものを**逐語で**使う。§7 が `R220`/`R221` で1語だけ外したのと同じ「記録された逸脱」である。
- **輝度リスクが最も高いのは `R219`**（暗い室内＋冬窓）。合成後に T8 を測って落ちたら、`R219` は候補から外す。
  **グレードで無理に持ち上げて眠い絵にしない。**

---

## 1. タイトル 4組（A/B・英語・本編用）

**すべて 60字以内・フック先頭。**下の「根拠」列は台帳ID／Brown II の該当箇所であり、
**この4組はいずれも `forbidden_claims` のどれにも触れていない**（§1.1 で機械的に確認する項目を列挙）。

| 組 | 案 | 字数 | 対になるサムネ | 根拠 |
|---|---|---:|---|---|
| **1** | **A**: `Everything Went to Arbitration — Except Their Own Bill` | **54** | THUMB-A (`R217`) | MB-23／MB-25（*"all disputes, other than claims to collect late payments owed by the patient"*） |
| | **B**: `The Only Claim Left in Court Was the Nursing Home's` | **51** | THUMB-A (`R217`) | 同上。カーブアウトの主語を明示した言い換え |
| **2** | **A**: `Arbitrate the Death Claim, Litigate the Debt Claim` | **50** | THUMB-B (`R218`) | MB-23＋MB-08。台本 L80 の平叙をそのまま短縮 |
| | **B**: `One Line on an Admission Form Sent a Death Claim Away` | **53** | THUMB-B (`R218`) | MB-07＋MB-23。「一行」はモチーフ（罫線）そのもの |
| **3** | **A**: `A Family Member Signed. The Record Never Says Who.` | **50** | THUMB-C (`R219`) | MB-07／MB-10（続柄も同一人物性も判決文に無い） |
| | **B**: `Five Pages Long — and Only One Patient Is Named` | **47** | THUMB-C (`R219`) | MB-19（Willett のみ・しかもキャプションだけ）＋ 判決文5ページ |
| **4** | **A**: `The Supreme Court Never Said the Clause Was Valid` | **49** | THUMB-D (`R224`) | MB-53／⛔-01。**本編の訂正命題そのもの** |
| | **B**: `It Was Vacated, Not Upheld — What Marmet v. Brown Decided` | **57** | THUMB-D (`R224`) | MB-34／MB-50 |

### 1.1 タイトルで**絶対に書かない**こと（機械チェック項目）

出す前に、8案すべてに対して次を確認する。**1件でもヒットしたらその案を捨てる。**

1. `upheld / valid / enforced / forced into arbitration / lost their day in court` を**肯定文で**含まない
   → 最高裁は条項を有効と判断していないし、誰にも仲裁を命じていない（⛔-01／MB-53）。
   （4B の *"Not Upheld"* は否定形であり、これは可）。
2. `unanimous` / 判事名（`Roberts` `Scalia` ほか）を含まない → **per curiam。著者名も票も記録が無い**（⛔-10）。
3. 数字による統計（`%` / `1 in N` / `millions of residents`）を含まない → この判決文に該当数字はゼロ（⛔-03）。
4. `your mother` / `your parent` / `the mother` / `daughter` / `widow` を含まない
   → 判決文は続柄を一度も書かない。**記録が支えない**（⛔-05／spec `forbidden_claims` 末項）。
5. 三家族を一括りにする語（`the three widows` / `all three signed the same contract`）を含まない
   → **Marchio の紙は例外条項も手数料条項も無い別の紙である**（MB-21／⛔-05）。
6. `they never sued again` など**その後**に触れない → Brown II で記録は終わっている（⛔-06）。

---

## 2. サムネ候補 4案（`thumbnail_candidates_min: 3` に対し +1）

見出しは **UPPERCASE・3〜4語**（行12）。キッカーは別レイヤーの短いタグで、見出しの語数には数えない。
**画には文字を焼き込まない。**下の見出し／キッカーは**すべて合成側**で乗せる。

### THUMB-A — `R217` ／ ペンが罫線を横切っている

- **見出し**: `EVERYTHING BUT THE BILL` — **4語 / 23字**
- **キッカー**: `NURSING HOME CONTRACT`（赤タグ）
- **アクセント**: ゴールド `#E5B53A`（`BILL` をゴールド、上2語を白）
- **主体**: 画面中央、**フレーム高の 55〜65%** をペンと罫線が占める。文字用の余白は**上3分の1**。
- **なぜクリックされるか（正直な形で）**: 「請求書だけが例外」という**契約書の設計そのもの**を一語で見せる。
  本編 L78–L80 がその通りに展開するので、**約束は本編で支払われる**（行13 promise-payoff）。
- **輝度**: 紙が画面の大半なので T8 は素で通る見込み。**最も安全な第一候補。**

### THUMB-B — `R218` ／ 罫線の上の、字に見えない一筆（極寄り）

- **見出し**: `ONE LINE, ONE EXCEPTION` — **4語 / 23字**
- **キッカー**: `THE CARVE-OUT`（赤タグ）
- **アクセント**: エレクトリック `#1F6BFF`（`ONE EXCEPTION` をブルー、`ONE LINE,` を白）
- **主体**: 一筆が**フレーム幅の 70% 以上**。極端なマクロ。余白は**上3分の1**。
- **なぜクリックされるか**: 映画の主人公（罫線）そのもの。HOOK 冒頭 `R001` と最終画 `R223` の**ループの中心**であり、
  サムネ・冒頭・結末が同じ画で閉じる。
- **T1 の最重要チェック点**: 一筆が文字・イニシャル・筆記体に見えたら**即不合格**。ここだけは拡大して見る。

### THUMB-C — `R219` ／ 冬窓のそばの空いた肘掛け椅子、座面に閉じたファイル

- **見出し**: `SIGNED FOR SOMEONE ELSE` — **4語 / 23字**
- **キッカー**: `A FAMILY MEMBER`（赤タグ）
- **アクセント**: ゴールド `#E5B53A`（`SOMEONE ELSE` をゴールド）
- **主体**: 椅子とファイルで**フレーム高の 60%**。余白は**上3分の1**。
- **なぜクリックされるか**: *"on behalf of the patient"*（MB-07）の四語を、続柄を作らずに絵にした唯一の案。
  **座らなかった側の席**が主題であり、FILM_BIBLE §3 のプラント（二脚目の椅子）と同じ論理に乗る。
- **輝度リスク（既知）**: 暗い室内＋冬窓＝**T8 で落ちる可能性が最も高い**。
  合成後に mean luma < 33 または stddev < 40 なら、**この案は捨てる**。持ち上げない。

### THUMB-D — `R224` ／ ペンだけ、硬い光、長い影（**新規発注**）

- **見出し**: `VACATED, NOT UPHELD` — **3語 / 19字**
- **キッカー**: `PER CURIAM, 2012`（赤タグ）
- **アクセント**: エレクトリック `#1F6BFF`（`NOT UPHELD` をブルー、`VACATED,` を白）
- **主体**: ペン1本のみ。紙は無い。**硬い横からの主光**で長く硬い影を落とす。余白は**上3分の1**。
- **なぜクリックされるか**: 本編の訂正命題（最高裁は有効と言っていない）を**見出しだけで**運ぶ唯一の案。
  タイトル4A/4B とセットで、CTR ではなく**誤解の少なさ**で勝ちにいく変種。
- **輝度**: **サムネ専用スタイルで発注するので、素で T8 を満たす設計**（明るいカウンター＋黒いペン＝高 stddev）。

---

## 3. プロンプト（各1枚・`_02` を作らない）

`[STYLE]` と `[NEG]` は **`EP65_marmet_CODEX_BATCH_A.v001.md` §2 のものを逐語で展開する。**本書では再掲しない
（再掲すると必ずドリフトする）。

### 既発注の3枚 — **本文を1文字も変えない**（`mandatory_stills` 済み・byte-identical で機械検証済み）

- `R217.png`
The foot of a printed form with a plain pen resting across the ruled line, shot dead centre and close, hard directional light, the upper third of the frame left clear [STYLE] Avoid: [NEG]
- `R218.png`
One unreadable stroke of ink on a ruled line, extreme close, strong contrast, the stroke not resembling any letter, the upper third of the frame left clear [STYLE] Avoid: [NEG]
- `R219.png`
An empty armchair beside a winter window with a closed folder on the seat, dramatic side light, the upper third of the frame left clear [STYLE] Avoid: [NEG]

### 新規 — `R224`

> ### ★`R224` は `[STYLE]` を使わない★
> サムネ専用プレートなので、**スタイルを本文に書き切ってある**（本編の低コントラスト指定を持ち込むと T8 に落ちるため）。
> **`[NEG]` だけは BATCH_A §2 のものを逐語で**連結する。1語も足さず、1語も引かない。
> これは §7 が `R220`/`R221` で `[NEG]` から1語だけ外したのと同種の、**記録された逸脱**である。

- `R224.png`
A single ballpoint pen lying alone on a bare pale counter, nothing else anywhere in the frame, shot dead centre and close from just above the surface, one hard directional key light from the left throwing a long hard-edged shadow of the pen across the counter, the pen dark against the pale surface, deep black falloff at the edges of the frame, very high contrast, bright overall exposure, no paper and no form of any kind in shot, the upper third of the frame left clear, cinematic still, restrained documentary framing, worn unglamorous surfaces, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage Avoid: [NEG]

---

## 4. 合成仕様（1280×720）

行11 は「Remotion `<Still>` で 1280×720、Codex が背景画を先に生成」を要求する。既存の正典レンダラは
`scripts/build_case_thumbnails_v002.py`（明るいヒーロー＋焦点グロー＋赤キッカー＋黒縁の特大見出し＋ゴールド）で、
**EP25–27 でオーナーの「しょぼい／派手じゃない」却下を通過した唯一の実績構成**である。EP65 もこの構成に従う。

| 層 | 指定 |
|---|---|
| 地 | 黒〜濃紺（`#05070D` → `#0C1526` の縦グラデ）。**フラット navy 一色にしない**（v001 却下の原因） |
| ヒーロー | 選択プレートを短辺合わせで敷き、**主体が中央〜下寄り**。焦点グローを主体に1つ |
| スクリム | 上3分の1に濃いスクリム（不透明度 0.55〜0.70）。文字はこの上に乗る |
| キッカー | 赤 `#D22628` のベタタグ・白文字・**上端**。見出しの語数には数えない |
| 見出し | 特大・UPPERCASE・**黒の太いストローク付き**。1行目=白 `#FAFAFA` / 2行目=ゴールド `#E5B53A` またはブルー `#1F6BFF` |
| 判読 | **1280×720 を 320px 幅に縮小して読めること。**読めなければ語を削る（増やさない） |
| PDマーク | 右下・小さく |

**受入（両方 HARD・選択済み1枚に対して測る）**

```
py -3.11 scripts/check_final_acceptance.py 65 --render <mp4> --emit-receipt
# thumbnail_present        : 1280x720 の PNG が3枚以上 + selected 1枚
# thumbnail_visibility     : mean luma >= 33.0  かつ  luma stddev >= 40.0
```

`thumbnail_visibility` は `09_package/thumbnail.selected*.png` の**最後の1枚だけ**を測る。
候補を全部測りたい場合は同じ指標（PIL `ImageStat` の L 平均と標準偏差）を候補4枚に手で当ててから選ぶ。

---

## 5. 生成後・選択前の目視QC（**プロンプトIDで選ばない**）

`R217` `R218` `R219` `R224` を**ラベル付きコンタクトシート**にして、1枚ずつ潰す。

| # | 不合格条件 |
|---|---|
| Q1 | 罫線の上の一筆が**文字・イニシャル・筆記体に見える**（`R217` `R218`）。拡大して見ること |
| Q2 | 画のどこかに**読める文字・数字・ロゴ・印章・室名札**がある |
| Q3 | 人物・顔・手が写っている／医療機器・ベッド・点滴・モニタが写っている |
| Q4 | 実在と特定できる建物・看板が写っている |
| Q5 | `R224` に**紙・書式が写り込んでいる**（ペンだけの絵でなければ不合格） |
| Q6 | 主体が小さい（フレーム高の 55% 未満）／上3分の1が空いていない |
| Q7 | 合成後 320px で見出しが読めない |
| Q8 | 合成後 mean luma < 33 または stddev < 40（`R219` は特に要測定） |
| Q9 | 既存の他話のサムネと構図が実質同じ |

**選択の順序**：QC を通った候補のうち、**THUMB-A → THUMB-B → THUMB-D → THUMB-C** の順で推す。
`R219`（THUMB-C）は輝度で落ちやすく、かつ「空いた椅子」は他話でも使われた register なので最後に置く。

---

## 6. `R224` の登録（**これをやらないと `check_spec_satisfied.py` が落ちる**）

`R224` は本書で新規に立てた ID である。**次の2つを必ず行う。**

1. `episodes/_planning/EP65_marmet_CODEX_BATCH_A.v001.md` の **§7 の末尾に `R224` を追記**する
   （§7 は「後から足した4枚」の節であり、`R220`–`R223` の直後が正しい位置。**§5 は触らない**）。
   追記時に §7 の合計行「合計は **223枚**になります」を **224枚** に直す。
2. `episodes/PD-2026-065-marmet/episode_spec.v001.json` の `mandatory_stills` に `"R224.png"` を追加し、
   `distinct_video_assets` との整合（実写採用11本 + プレート224 = 235）を `notes` に記録する。
   **`mandatory_stills` を空や欠番のまま出荷しない**（EP54 でここが空だったため、棚に無いから作らせた14枚が
   完成品から消えたのに誰も気づかなかった）。

> **`R224` はサムネ専用プレートであり、本編のカットには使わない。**
> 本編に入れると `[STYLE]` を持たない1枚だけがトーンから浮く。
