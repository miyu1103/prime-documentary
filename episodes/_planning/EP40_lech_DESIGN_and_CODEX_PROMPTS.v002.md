# EP40 — Lech v. Jackson — 制作設計書 ＋ Codex引き継ぎプロンプト（v002・確定台本版）

- Episode ID: `PD-2026-040-lech` / slug: `lech` / EP40
- 中心の問い（英語・二人称）: **"Can the police destroy your house and pay you nothing?"**
- 判例: **Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019)**, cert. denied (2020)
- リスク区分: **R2**（実在私人が主役 = 肖像・実映像・ディープフェイク全面禁止／未成年は象徴表現のみ）
- 尺プロファイル: **standard**（`manifest.target_duration_minutes: 12`・band 11.5–12.5分 = 690–750秒）
- Status: **BINDING**。上位正典は `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（v2）と `docs/PD_WINNING_PATTERN.md`。衝突時は v2 のハードGATEが勝つ。

## ★v001 からの差分（v001 は本書で完全に置き換える。v001 を読んで実装してはならない）

v001 は台本未確定の状態で書かれており、確定台本 v002（2,153語・`check_script_length` PASS）と **事実面で衝突する箇所がある**。以下は v001 の**削除・訂正**であり、Codex は必ず本書の値を使う。

| # | v001 の記述 | 本書での処置 | 理由 |
|---|---|---|---|
| 1 | AEビート `b03` = 「万引きの被害額 vs 家の損害額」（SPLIT_COMPARE） | **削除** | 確定台本は**罪数内訳・万引き額を一切使わない**（台本 事実対応表「不使用: 罪数内訳」）。台帳外の数字を画面に出すのは事実性違反 |
| 2 | AEビート `b07` = 補償率（F04÷F03） | **削除** | 「家の損害額」の確定値が台帳に無い。除算の分母が存在しないので計算値を作れない |
| 3 | AEビート `b06` = CT_COUNTDOWN（損害額→受領額へ減少） | **削除** | 同上。出発値が無い |
| 4 | F01–F09 の未検証テーブル | **廃止**。確定台本の台帳 C01–C31 由来の確定値表（§0.5）に置換 | 台本確定により検証済み |
| 5 | `accuracy_lock` R2/R3（`Supreme Court` を含む文の文脈制限） | **書き換え**（§0.4）。1文窓 → **2文窓**に緩和し、代わりに**係属中2件の結果断定**と**限定免責への言及**を新たに禁止 | 旧R2 は確定台本の "He asked the Supreme Court to take the case." を誤検知して FAIL させる |
| 6 | `accuracy_lock` R4（ナレ本文に判例引用の完全一致行を要求） | **本文からは削除**し、`09_package/*`（概要欄）側の要件に移す | 確定台本は意図的に引用形式を読み上げない |
| 7 | 総尺 741.4秒 / 2,140語 / 幕配分 350-505-510-575 | **全面置換**（§3）。確定台本の実測語数から再計算した **734.47秒 = 12:14** / 幕配分 404-413-369-583 | 台本が確定した |
| 8 | 画像 S01–S22（22シーン） | **S01–S25（25シーン）に置換**（§5.6）。確定台本の `[Sxx]` 割当に1:1対応 | 台本が S01–S25 を参照している |
| 9 | 素材配分 factory 54 / distinct 130 / first-use 0.575 | **置換**（§5.1）: factory **70** / distinct **167** / first-use **0.746** | v001 の 0.575 は `check_asset_reuse` の first-use ≥0.70 を満たさない（v001 §5.1.2[3] は自己矛盾していた） |

---

# 0. 受入条件の再掲 ＋ 事実の取り扱い（ACCURACY LOCK）

## 0.1 満たすべき v2 row と verify コマンド（Codexプロンプト冒頭に必ず再掲すること）

**対象 row: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16**

```bash
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 40 --json
```

**THE ONE RULE:** 「validator PASS = done」ではない。独立した受入スクリプトが**実 `final.mp4` を測って**全ハードGATEを通って初めて done。自作の品質ゲートを手書きするのは禁止。GATEを緩めて通すのも禁止。予約は `--emit-receipt` で出た receipt（`video_sha256` 一致）が無い限り不可。

## 0.2 確定台本（唯一の正）

```
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP40_lech_script.en.v001.md
（ファイル内ヘッダは "v002"。ファイル名の v001 が正・中身の v002 が改稿番号。両方このまま扱う）
```

**本番配置先:** `episodes/PD-2026-040-lech/03_script/script.en.v002.md`（上記を**1バイトも変えずに**コピー）。

**ナレ本文は完成済み。Codex は台本本文を1文字も改変してはならない。** 語順・短縮形・句読点の「整形」も禁止（em-dash 0本・短縮形23箇所・セミコロン0は意図的な改稿結果であり、触ると AI臭の再発と語数ゲートの再計算が必要になる）。

**尺ゲートの実測（PASS済み・そのまま記録）:**
```
PASS script_length: 2,153 words (need 2,048-2,226)
  narration estimate  slow 13.2m | median 12.1m | fast 9.1m
  target band         11.5-12.5 min
```

## 0.3 【最重要】fast端リスクの唯一の対処 = voice speed のピン留め

尺ゲートは fast端（237.4 wpm）で **9.1分**＝band下限割れを警告している。2,730語に増量すれば解消するが**上限2,226語を超えるため両立不可能**。したがって**運用側で潰す**。

**ElevenLabs 発注時の確定値（`voice_is_master` row2・この値以外で発注しない）:**

| 項目 | 確定値 |
|---|---|
| `VOICE_ID` | `nPczCjzI2devNBz1zQrb` |
| model | `eleven_multilingual_v2` |
| `stability` | **0.35** |
| `similarity_boost` | **0.80** |
| `style` | **0** |
| `use_speaker_boost` | **on** |
| **`speed`** | **1.0（既定値を明示指定する。省略してはならない）** |

**発注後の検証（BLOCKING・これを通さずにミックスへ進まない）:**
```bash
# 生成した全 VC-*.mp3 の実時間合計を測り、実測 wpm を出す
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep lech --json
```
- **合格条件: 実測 wpm が 168.0 – 190.0 の範囲内**（= 総VO 680–770秒相当）。
- **190.0 を超えたら、その音声は破棄して再発注する**（`speed` を 0.95 に下げて再生成）。SAPI/local TTS はタイミング下書きのみに使い、マスターにしない。
- このチェックが無いと fast端で 9.1分になり `runtime_band` が落ちる。**音声を作った後・ミックス前に必ず測る。**

## 0.4 `accuracy_lock`（EP40固有ゲート・BLOCKING・v001 から全面書き換え）

`scripts/check_lech_accuracy.py` を実装する。exit != 0 で出荷を止める。

**検査対象ファイル:**
- `episodes/PD-2026-040-lech/03_script/script.en.v002.md`
- `episodes/PD-2026-040-lech/03_script/lech_slots.v002.json`（全文字列フィールド）
- `episodes/PD-2026-040-lech/08_edit/ae_hero/beats.json`（`top` / `bottom` / `caption` / `footnote`）
- `episodes/PD-2026-040-lech/09_package/*.json` / `*.txt`（title / description / thumbnail headlines / pinned comment）
- `remotion/props/lech*.json`（`subtitle`）
- `remotion/src/data/lech_film.json` の `figures[].text` / `figures[].lines[]`

### ルール（R1–R8）

**R1 — パッケージゾーンでの `Supreme Court` 全面禁止**
`title_candidates[]`, `thumb_headlines[]`, `package.title`, `figures[].text`（`ActTitle` kind のみ）に以下が部分一致で1回でも出たら FAIL。
```python
BANNED_ZONE = re.compile(r"supreme\s*court|最高裁|SCOTUS", re.IGNORECASE)
```
> 理由: 本件は最高裁が本案判断していない。サムネ/タイトルで「最高裁」を匂わせると誤認を売ることになる。

**R2 — 本文の文脈制限（★2文窓。v001 の1文窓は誤検知するので使うな）**
本編ナレ本文で `Supreme Court` を含む文について、**その文＋直後の1文**を連結した窓の中に、次のいずれかが含まれること。含まなければ FAIL。
```python
ALLOWED_CONTEXT = re.compile(
    r"declined to hear|refused to hear|denied review|denial of review|"
    r"did not take the case|cert(iorari)?\s+(was\s+)?denied|let the ruling stand|"
    r"never ruled on|it declined|expressed no view|petition", re.IGNORECASE)
```
> 確定台本の該当4箇所はすべてこの2文窓で pass する（"He asked the Supreme Court to take the case. On June 29, 2020, it declined." が1文窓では落ちるため窓を2文に広げた）。

**R3 — 肯定的動詞の禁止**
本文全体で `Supreme Court` の**後 60文字以内**に次が現れたら FAIL。
```python
BANNED_VERB = re.compile(r"\b(ruled|held|decided|upheld|affirmed|found|concluded|sided)\b", re.IGNORECASE)
```

**R4 — 係属中2件の結果断定の禁止（★新設・最重要）**
`Hadley` / `Pena` / `25-1158` / `25-1163` / `conference` を含む文で、次が現れたら FAIL。
```python
BANNED_PREDICT = re.compile(
    r"will (rule|decide|grant|deny|hear|reverse|overturn)|"
    r"is expected to|likely to (grant|rule|win|lose)|"
    r"the Court will|going to (rule|decide)|should win|will finally", re.IGNORECASE)
```
さらに、本文中に `pending` または `Nobody knows how they end` が**最低1回**存在すること（係属中である旨の明示）。確定台本は "Both still pending." と "Nobody knows how they end" の両方を持つ。

**R5 — 限定免責への言及の全面禁止（★新設）**
全対象ファイルで次が1回でも出たら FAIL。
```python
BANNED_QI = re.compile(r"qualified immunit|限定免責|Harlow v\.|Pierson v\.", re.IGNORECASE)
```
> 理由: 台帳 C31 は「本件の争点ではない」。確定台本は実測0回。v001 の記述（背景ドクトリンに限定免責を挙げていた）は誤りなので破棄する。

**R6 — 裁判所名の明示**
本文に `Tenth Circuit` が**最低2回**（確定台本は3回）、`district court` が**最低1回**出現すること。

**R7 — 適法性の断定禁止 / 中立**
次が現れたら FAIL。
```python
BANNED_NEUTRAL = re.compile(
    r"police (acted |were )?(illegal|unlawful)|violated the law|"
    r"the police were wrong|excessive force|innocent means (he|she) was", re.IGNORECASE)
```
確定台本は逆に "Nobody in this story did the wrong thing that day." / "Nobody disputes the police acted lawfully." を持つ。**この2文を削除・改変したら FAIL とする**（存在チェック）。

**R8 — 未成年・被害者の匿名化**
全対象ファイル（画像プロンプト `05_visuals/ai_prompts.v002.md` を含む）で、9歳男児・15歳の子の**実名**、および年齢+性別+外見を同時に特定する描写語が現れたら FAIL。
```python
BANNED_MINOR = re.compile(
    r"\b(boy|girl|child|kid)\b.{0,40}\b(face|portrait|smiling|eyes|hair colou?r)\b|"
    r"\bnine-year-old\b.{0,30}\b(named|called)\b", re.IGNORECASE)
```
> ナレ本文の "the nine-year-old" / "fifteen-year-old son" は**役割の記述であり合法**。禁止するのは**名前**と**顔の描写**。

**出力:** `episodes/PD-2026-040-lech/09_package/accuracy_lock.v002.json`（`{"pass": bool, "violations": [{"file","rule","line","excerpt"}]}`）。
`pass: true` でない限り `check_final_acceptance.py` に進んではならない。

## 0.5 画面に出してよい確定数値（台帳 C01–C31 由来。★この表以外の数字を画面に出すな）

| ID | 値 | 台本での表現 | 使用先 |
|---|---|---|---|
| N01 | **June 3, 2015** | 〔CARD: JUNE 3, 2015〕 | HOOK カード（Remotion figure `f01`） |
| N02 | **nineteen hours** | "The house stood for another nineteen hours." / "Nineteen hours." | AE **b02** |
| N03 | **about five hours**（交渉） | "For about five hours, negotiators tried to talk him out." | Remotion figure |
| N04 | **$5,000** | 〔CARD: $5,000〕仮住まい費用 | AE **b03** |
| N05 | **$250,000** | 〔CARD: $250,000〕借入額 | AE **b05** |
| N06 | **five years**（退職延期） | "He pushed it back five years." | Remotion figure |
| N07 | **January 2018** 地裁 | "In January 2018, a federal district court in Colorado ruled against him" | Remotion timeline |
| N08 | **October 29, 2019** 第10巡回区 | "On October 29, 2019, the Tenth Circuit affirmed" | AE **b06** |
| N09 | **June 29, 2020** 不受理 | "On June 29, 2020, it declined." | Remotion timeline |
| N10 | **1887 Mugler v. Kansas** | 引用 | Remotion QuoteCard |
| N11 | **June 10, 2022 / 30 canisters / $16,000 / Oct 2025 / 7th Cir** | Hadley | AE **b08**（列1） |
| N12 | **July 2020 / ~$60,000 / 5th Cir** | Baker | AE **b08**（列2） |
| N13 | **2024 / ~35 canisters / ~$70,000 / 6th Cir** | Slaybaugh | AE **b08**（列3） |
| N14 | **Aug 2022 / Nov 2025 / 9th Cir** | Pena | AE **b08**（列4） |
| N15 | **Aug 2025 / $30,000 / paid** | Las Vegas | AE **b08**（列5・唯一の GOLD） |
| N16 | **November 2024** Sotomayor statement（Gorsuch 同調） | 個別意見。法廷意見でも反対意見でもない | Remotion QuoteCard |
| N17 | **1960 Armstrong** | 引用 | Remotion QuoteCard（ED） |
| N18 | **April 6, 2026 提出 / September 28 conference / 25-1158 / 25-1163** | 両件係属中 | Remotion timeline（ED） |
| N19 | **May 2026** Lech の第三者意見書署名 | 〔CARD: MAY 2026〕 | FLASH-FORWARD カード |

**禁止（台帳外・画面にもナレにも出さない）:** 68発という発射数、報道由来の再建費用、Seacat の罪数内訳・量刑年数・動機・薬物関連の記述、家の市場価値、補償率（%）、万引き被害額。

---

# 1. 企画の適合（house rules §1）

**1問の形:** 「**警察は、あなたの家を壊して、一円も払わずに済むのか？**」

| 必須3要素 | 充足 |
|---|---|
| ① 二人称 | タイトルA/B・OP・幕2 "your house"・CTA すべて YOU/YOUR |
| ② 自分事の脅威 | **持ち家・賃貸を問わず全視聴者が「住所」を持つ**。しかも本件の一家は落ち度ゼロ = 視聴者に自己弁護の余地がない |
| ③ 司法の線引き | Takings Clause の police power 例外。第10巡回区が線を引き、最高裁は本案を判断していない |

**強い束との一致:** 第4修正の「令状・捜索・押収・私財没収」束の隣接領域（**私財の破壊と補償**）。実績上位（Warrant to Search Your Phone / Tracked His Phone）と同じ「国家 vs あなたの所有物」型。**弱い束（純・金融史）ではない**。

**語り口:** 実測で判例解説型は APV 1.6–7.5%、一人の受難型は 24–42%。**EP40 は 100% 受難型**。確定台本は「9歳の子が最初に家から歩いて出た」で始まり、Takings Clause の説明は幕2末まで出てこない。

---

# 2. 視覚・音響レーンの分離（EP39 frazier との衝突回避）

> **EP39 のファイルには一切触らない。** レーンは以下で機械的に分離する。

| 軸 | **EP39 frazier** | **EP40 lech** |
|---|---|---|
| 舞台 | 取調室 / 密室 | **郊外の一軒家 / 屋外の広がり** |
| 時間帯 | 夜 | **昼（真昼〜夕方）＋ 1箇所だけ夜明け**（幕1末の2.0秒） |
| 支配的な出来事 | 心理的圧迫・言葉 | **物理的破壊と、その後の空白** |
| アクセント色 | electric `#1F6BFF` | **gold/amber `#E5B53A`（EP40専用）** |
| ベース色 | 深い navy / 黒 | **褪せた昼光の白 + コンクリート灰 + 木の裂けたタン + 埃のアンバー** |
| 影の色 | 青寄りの黒 | **わずかに緑がかった灰（屋外の日陰）** |
| レンズ感 | 望遠・浅い被写界深度 | **広角気味・引き・"失われた体積"** |
| 楽器 | （EP39側で定義） | **ソロピアノ（疎・単音）＋低弦のサステイン＋金属的パーカッション** |
| 画像保存先 | （EP39側） | `H:\pd-media\assets\ai\lech\` |
| Remotion データ | （EP39側） | `remotion/src/data/lech_film.json` |
| Remotion コンポ | （EP39側） | `Ep40Lech` |
| AE 作業ディレクトリ | （EP39側） | `episodes/PD-2026-040-lech/08_edit/ae_hero/` |

**素材被り禁止（row7）:** EP39 と同一の factory clip / AI画像を**1点も**使わない。生成・選定前に `episodes/PD-2026-039-*/05_stock/stock_ledger*.json` を読み、sha256 の重複を除外すること。

**ブランド（`remotion/src/brand.ts` から import・ハードコード禁止）:** 黒 / 紺 / エレクトリックブルー `#1F6BFF` / シルバー / 金 `#E5B53A`。見出し Impact系・本文 Trebuchet系。EP40 の主アクセントは**金**。

---

# 3. 尺と構成 — 確定台本の実測から算出

## 3.1 全区間タイムライン（★この表が唯一の正。v001 の 741.4秒版は破棄）

**算出基準: 実測ナレ速度の中央値 178.1 wpm**（VO秒 = 語数 ÷ 178.1 × 60）。**秒は fps から算出し、フレーム直書き禁止**（fps = 30 → frame = `Math.round(30 * sec)`）。

| # | ブロック | 役割(row9/10) | 語数 | VO秒 | 台本指定の沈黙 | 固定尺 | 区間長 | **開始–終了（秒）** | 表示 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | **HOOK** | `hook` | 48 | 16.17 | 1.5 | — | 17.67 | **0.00 – 17.67** | 0:00 |
| 1 | **FLASH-FORWARD** | `hook`（続き） | 23 | 7.75 | 1.2 | — | 8.95 | **17.67 – 26.62** | 0:17 |
| 2 | **BrandOpening** | `opening` | 0 | — | — | **3.50** | 3.50 | **26.62 – 30.12** | 0:26 |
| 3 | **OP ナレ** | `opening` | 27 | 9.10 | — | — | 9.10 | **30.12 – 39.22** | 0:30 |
| 4 | **幕1** 4219 South Alton Street | `body` | 404 | 136.10 | 2.0 | — | 138.10 | **39.22 – 177.32** | 0:39 |
| 5 | **幕2** What it costs to be the address | `body` | 413 | 139.14 | 2.0 | — | 141.14 | **177.32 – 318.46** | 2:57 |
| 6 | **幕3** Police power | `body` | 369 | 124.31 | 3.5 | — | 127.81 | **318.46 – 446.27** | 5:18 |
| 7 | **幕4** The address is the only qualification | `body` | 583 | 196.41 | 3.5 | — | 199.91 | **446.27 – 646.18** | 7:26 |
| 8 | **ENDING**（payoff → CTA） | `ending` | 222 | 74.79 | 4.5 | — | 79.29 | **646.18 – 725.47** | 10:46 |
| 9 | **BrandEndcard**（+ 次回引き10語をVOで重ねる） | `ending` | 10 | 3.37※ | — | **9.00** | 9.00 | **725.47 – 734.47** | 12:05 |

※ ED の10語（"Next: the search that begins before you are a suspect."）は **BrandEndcard の9.0秒の中に収める**（3.37秒 + 5.63秒の余韻）。尺を追加しない。

### 検算（Codex は必ず自分で再計算して一致を確認すること）

```
[1] 語数（ナレ本文のみ・[SOUND]/〔CARD〕/*(silence)* を除く）
    48 + 23 + 27 + 404 + 413 + 369 + 583 + 222 + 10 = 2,099 語
    ※ check_script_length.py の計数は 2,153 語（見出し行等を含む方式）。
      ゲートの判定は 2,153 = band 2,048–2,226 内で PASS 済み。
      本表の 2,099 は「ナレとして声になる語」であり、尺計算にはこちらを使う。

[2] VO秒合計 = 2,099 / 178.1 × 60 = 707.10 秒
[3] 台本指定の沈黙合計 = 1.5+1.2+2.0+2.0+3.5+3.5+4.5 = 18.20 秒
[4] Bookends = OPENING_SEC 3.50 + ENDCARD_SEC 9.00 = 12.50 秒
    （ただし ED の VO 3.37秒は ENDCARD の内側なので二重計上しない）

[5] 総尺 = 707.10 − 3.37(ED VOはENDCARD内) + 18.20 + 12.50 = 734.43
    ブロック積み上げでの実値 = 734.47 秒（丸め差 0.04）
    ★ 採用値 = 734.47 秒 = 12:14.5

[6] runtime_band 判定
    690 ≤ 734.47 ≤ 750     ✓ PASS（上限まで 15.5秒の余裕）

[7] fast端リスク（237.4 wpm）
    2,099/237.4×60 + 18.2 + 12.5 = 561.2秒 = 9:21   ✗ band外
    → §0.3 の voice speed ピン留め + measure_vo_wpm.py で運用側で潰す。
      実測 wpm が 190.0 を超えた音声は破棄・再発注（BLOCKING）。
```

**`lech_film.json` に入れる値:**
```
hookSeconds        =  26.62   （HOOK 17.67 + FLASH-FORWARD 8.95）
OPENING_SEC        =   3.50   （Bookends 定数・変更禁止）
narrationSeconds   = 695.35   （OPナレ 9.10 + 幕1〜ED 686.25）
ENDCARD_SEC        =   9.00   （Bookends 定数・変更禁止）
------------------------------------------------
合計                 734.47 秒
caseFilmDurationInFrames = round(30 × 734.47) = 22,034
```

## 3.2 `structure_4part`（row9/10）の充足

| 要件 | 充足 |
|---|---|
| hook / opening / body / ending が存在し順序通り | ✓ 上表の `役割` 列 |
| **hook がヘッド 6–10秒に存在** | ✓ HOOK は **0.00 秒開始・17.67秒まで連続**。ヘッド 6.0–10.0秒の窓は完全に HOOK の内側 |
| `BrandOpening` が frame 0 ではなくフックの後 | ✓ **26.62秒**から（フック＋フラッシュフォワードの後） |
| CTA が末尾30秒以内 | ✓ CTA "Hadley and Pena go to conference on September 28. Subscribe if you want to know what they're told." は **719.4–725.47秒**に置く（末尾から 9.0–15.1秒） |
| ナレ入りフック・語同期字幕（無音フック廃止） | ✓ HOOK は48語のナレ入り。faster-whisper 語タイムで語同期 |
| フックは本編の決めカット流用（新規制作しない） | ✓ HOOK は `[S02 S05 S09]`＝幕1・幕2で使う画の流用。**HOOK 専用に新規生成する画は無い** |

## 3.3 promise-payoff 対応表（row9/13・フックで見せた reveal が本編後半に必ず出る）

| # | フック/冒頭で開いたもの | 回収位置（秒） | 回収内容 |
|---|---|---|---|
| P1 | "The house stood for another nineteen hours. / Then it didn't."（何が起きたか言わない） | **幕1 150.0–177.3** | 突入シーケンスの逐語 →「Nineteen hours.」→「The roof did not fall in.」 |
| P2 | FLASH-FORWARD「11年後、赤の他人の事件に署名する男。彼は何も得ない」 | **ENDING 646.2–672.0** | "He gets nothing from those cases. He isn't a party." で完全回収 |
| P3 | 〔CARD: MAY 2026〕 | **ENDING 646.2** | "In May 2026 ... Leo Lech signed his name to a brief in someone else's case." |
| P4 | OP「2つのドア。片方は払われ、片方は払われない」 | **幕3 318.5–360.0** | eminent domain（払う）vs police power（払わない） |
| P5 | OP「どのドアから緊急事態が来るかは誰も選べない」 | **幕4 446.3–554.5** | 5つの住所・5つの巡回区・同じ緊急事態で結論が割れる |
| P6 | タイトル/サムネの約束「壊されて、払われない」 | **幕2 177.3 / 幕3 360.0** | $5,000 のみ／"Nothing owed." |

> **サムネT2 が `$5,000 FOR THIS` と約束するので、$5,000 は幕2の冒頭 4秒以内（181秒付近）に必ず画面に出る**（AE b03）。約束の回収が10分後では packaging QC の意図に反する。

## 3.4 リテンションマップ（row16・再フック位置を秒で確定）

**コールドオープンの未解決の問い（0:00 で開き、12:05 まで閉じない）:**
> "Who pays for a house that was destroyed correctly?"

| # | 秒 | 表示 | 再フックの機能 | トリガーとなるナレ |
|---|---|---|---|---|
| R1 | 94.0 | 1:34 | 事態の命名 | "the situation acquired a name. High-risk barricade." |
| R2 | 150.0 | 2:30 | 数字の殴打 | "Nineteen hours." |
| R3 | 227.5 | 3:47 | 逃げ場の消滅 | 〔CARD: INTENTIONAL ACTS BY GOVERNMENT OFFICIALS — EXCLUDED〕 |
| R4 | 318.5 | 5:18 | 二語の断罪 | "They were not."（幕3の1行目） |
| R5 | 372.5 | 6:12 | 制度の自白 | 〔CARD: NOT BINDING PRECEDENT〕 |
| R6 | 446.3 | 7:26 | 射程の拡大 | "If this happened once, it would be a tragedy about one house." |
| R7 | 547.0 | 9:07 | 分裂の可視化 | 5つの住所の対比（AE b08） |
| R8 | 646.2 | 10:46 | 最後の転回 | "There is one more filing." |

**間隔の検算:** 0:00→1:34 / →0:56 / →1:17 / →1:31 / →0:54 / →1:14 / →1:41 / →1:39 / →終端1:28
→ **最大間隔 1:41 < 3:00** ✓（row16「約2–3分ごとに最低1回」を大幅に満たす）

**オープンループ（3本・遅く閉じる）:**
| ID | 開く | 閉じる |
|---|---|---|
| L1 | 0:00 HOOK「誰が払うのか」 | **360.0（6:00）** "Police power, not eminent domain. That was the ruling. Nothing owed." ＋ **725.4（12:05）** 主題文で最終的に閉じる |
| L2 | 0:17 FF「なぜ何も得られない訴訟に署名するのか」 | **660.0（11:00）** "He wrote it anyway" |
| L3 | 2:37「屋根は落ちなかった」＝正しく実行された、その代償は誰が | **300.0（5:00）** "The entire cost of all that correctness landed on one family" |

**平坦区間の禁止（20秒超ゼロ）:** ドクトリン説明（police power / eminent domain）は幕3に集中するが、**単独で20秒を超える説明ブロックを作らない**。§6.10 の Remotion MGビート（`MechanismReveal` 4枠）を幕3の説明区間に**最大18秒間隔で**差し込み、説明の途中で必ず画が動くようにする。

## 3.5 台本指定の沈黙 18.2秒の扱い（`bgm_present` row1 との関係）

台本の `*(silence — Xs)*` は **ナレの沈黙であって、音の沈黙ではない**。

| 位置 | 秒 | 鳴らすもの |
|---|---|---|
| HOOK 内 | 1.5 | ルームトーンのみ（台本 [SOUND] 指定）。BGM は無し |
| FF 後 | 1.2 | ルームトーン + 2015へのハードカット直前の低域プリロール |
| 幕1末（夜明け・埃） | 2.0 | 環境音（鳥・遠い車）+ BGMベッド |
| 幕2 カード保持 | 2.0 | BGMベッドのみ（ピアノ単音） |
| 幕3 カード保持 | 2.0 | BGMベッドのみ |
| 幕3 "Considerable appeal." 後 | 1.5 | BGMベッドのみ |
| 幕4 4件終了後 | 2.0 | 低弦サステインのみ |
| 幕4 percolation カード後 | 1.5 | BGMベッドのみ |
| ED Armstrong 引用後 | 1.5 | BGMベッドのみ |
| ED CTA 前 | 3.0 | **台本指定「Do not score this gap」→ BGMは -34 LUFS まで落とすが無音にしない**。環境音ベッド（遠い屋外の広いリバーブ）を残す |

**最長の無音候補は 3.0秒 << 25秒** ✓ `bgm_present` PASS。
> **罠:** 台本の [SOUND] 指定「strip everything except the bullhorn」（幕1・交渉5時間）と「sound pulled out from under it」（突入シーケンス）を**デジタル無音として実装してはならない**。前者は拡声器の遠鳴りベッド、後者は低域ランブル（40–90Hz）を残す。**この2区間は台本上いずれも20秒以上あり、無音にすると `bgm_present` が即FAILする。**

---

# 4. 音の4層設計（ナレ / BGM / SFX / 環境音）

## 4.1 ラウドネス（row6・確定値）

| 項目 | 確定値 |
|---|---|
| 統合ラウドネス（完成 mp4） | **-14.0 LUFS**（許容 -16〜-12） |
| True peak | **≤ -1.0 dBTP** |
| ナレ（VO）単体 | -18.0 LUFS 目標 |
| BGM ベッド（VO下・ダッキング後） | **-22.0 LUFS**（無音まで落とさない） |
| BGM ベッド（VO無し区間） | -17.0 LUFS |
| 環境音ベッド | -30.0 LUFS |
| SFX ピーク | -12.0 LUFS（単発） |
| ダッキング | threshold VO検出時、**リダクション 5.0 dB / attack 120ms / release 450ms** |

## 4.2 章ごとのBGM割当（8カテゴリ・1章1トラック）

| 区間（秒） | ブロック | トラック性格 | 楽器 |
|---|---|---|---|
| 0.0 – 17.7 | HOOK | **なし**（台本 [SOUND]: 最初の3行に音楽を敷かない）。17.0秒からピアノ単音がフェードイン | — |
| 17.7 – 26.6 | FF | 単音ピアノ・不解決 | ピアノ |
| 26.6 – 39.2 | OP | ブランドスティンガー（`BrandOpening` 付属） | — |
| 39.2 – 94.0 | 幕1前半 | 静かな朝・持続する低弦 | 低弦サステイン |
| 94.0 – 177.3 | 幕1後半 | 圧の増大。**94–150秒の交渉区間は拡声器ベッドのみ・音楽を退かせる（-30 LUFS）** | 低弦 + 拡声器 |
| 177.3 – 318.5 | 幕2 | 疎なピアノ・単音の反復 | ピアノ |
| 318.5 – 446.3 | 幕3 | 冷たい持続音・金属的パーカッション（法の機械性） | 低弦 + メタルパーカス |
| 446.3 – 646.2 | 幕4 | 列挙のリズム。5つの住所ごとに同じ音型を移調 | ピアノ + 低弦 |
| 646.2 – 722.5 | ENDING | 解決しない和音 → Armstrong 引用でだけ開く | ピアノ + 弦 |
| 722.5 – 734.5 | CTA/ENDCARD | ブランドED（`BrandEndcard` 付属） | — |

## 4.3 SFX（カット・リビール・数字出現）

| 種別 | 使用位置 | 音 |
|---|---|---|
| whoosh | 全 MGビート（36枠）の in | 短い空気音・80ms・-14 LUFS |
| impact | AE b02 / b05 / b08 の数値着地 | 低域インパクト・-12 LUFS |
| tick | カウントアップ中の桁変化 | 微細クリック・-24 LUFS |
| wood splinter | 幕1 突入シーケンス（150秒付近）3箇所 | 木材の裂け・-16 LUFS |
| paper | 幕2 保険約款カード / 幕3 脚注カード | 紙の擦れ・-22 LUFS |
| room tone | 全編ベッド | 屋外の広いリバーブ・-30 LUFS |

**ダッキング必須。** SFX も VO と衝突する場合は VO を優先し、SFX を -6 dB 追加で下げる。

---

# 5. ビジュアル — 素材積算と画像プロンプト

## 5.1 素材の積算（★確定台本 734.47秒で再計算）

```
[0] 絵が必要な区間
    734.47 − BrandOpening 3.50 − BrandEndcard 9.00 = 721.97 秒

[1] 総カット数 = 224
    721.97 / 224 = 3.22 秒/カット          ✓ 平均ショット長 ≤約6秒（row8）

[2] 素材の内訳（★first-use share ≥0.70 を満たす配分）
    factory 実写クリップ  70本 × 1回 =  70 カット
    i2v クリップ          18本 × 2回 =  36 カット
    静止画（distinct）    79枚 →       118 カット（39枚が2回使用・40枚が1回）
    ------------------------------------------------
    合計                 167素材 →     224 カット

[3] first-use share = 167 / 224 = 0.746     ✓ ≥0.70（check_asset_reuse）
[4] footage_diversity distinct/total = 167/224 = 0.746   ✓ ≥0.40
[5] 同一素材の最大使用回数 = 2回            ✓ ≤4回（設計目標 ≤3回・factory は1回厳守）
[6] 静止画占有率 = 118 × 2.05秒 = 241.9秒 → 241.9/734.47 = 32.9%   ✓ ≤45%
[7] 動画カットの平均長 = (721.97 − 241.9) / 106 = 4.53 秒   ✓ ≤6秒
[8] factory 下限 = 734.47/30 = 24.5 → ≥25本。設計値 70本   ✓
    734.47 / 70 = 10.5秒に1本
[9] 汎用シンボル（天秤・gavel 等）= 0回      ✓ ≤2回
    → 本作は法廷シンボルを使わない。**天秤・木槌・目隠しの女神像は生成も使用も禁止**
[10] 空 span = 0（shotlist の全 span に asset_id を入れる）
```

**生成プール:** 25シーン × 6バリエーション = **150枚**。本編で使う distinct 静止画 79枚はここから選抜（残りはサムネ / Shorts / 差し替え）。
> 枚数ぴったりに生成すると「合わない画を仕方なく使う」＝紙芝居の原因になる。プールを必ず多めに作る。

## 5.2 保存先とレジャー

- 保存: `H:\pd-media\assets\ai\lech\<SPN-ID>.png`（`import_to_remotion.py` が取り込む）
- 連番規則: `S01.png`, `S01_02.png`, `S01_03.png` … `S01_06.png`
- 解像度: **長辺 3840px 以上**（生成 → upscale target 3840。最低でも2048だが本作は3840を必須とする）
- 1画像 1行を `episodes/PD-2026-040-lech/05_stock/stock_ledger.v002.json` に記録
  （`source=ai_codex` / `commercial_use=allowed` / `sha256` / `acquired_at` / `used_in_span`）

## 5.3 共通スタイル接尾（各プロンプト末尾に必ず付ける）

```
, cinematic still, harsh midday sunlight and airborne dust, wide-angle sense of open suburban space, bleached daylight whites with concrete grey, splintered pale wood and warm amber dust motes, faintly green-grey outdoor shadows, deep shadow detail retained, shallow-to-medium depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo
```

> **EP39 との分離:** 接尾に `navy`, `electric blue`, `night`, `interrogation`, `low-key` を**一切含めない**。

## 5.4 共通ネガティブ（各プロンプトに必ず付ける）

```
text, words, letters, numbers, captions, watermark, logo, street address, house number, mailbox lettering, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, child face, cartoon, illustration, low quality, blurry, deformed, extra limbs, gore, blood, corpse, weapon pointed at camera, night scene, dark navy interior, interrogation room, courtroom gavel, scales of justice, blindfolded statue
```

## 5.5 R2 安全ルール（絶対・§0.4 R8 とセットで機械検査）

1. **実在人物の肖像を作らない/使わない。** Leo / Alfonsia / John Lech、Vicki Baker、Amy Hadley、Carlos Pena、Robert Seacat、実名の警察官全員。**サムネにも使わない。**
2. **9歳の男児は未成年かつ被害者。** 姿・年齢・性別が特定できる描写を避け、**「家から出てくる小さな人影のシルエット（逆光・輪郭のみ・顔なし）」**に限る。名前は報道にあっても使わない。15歳の子（Hadley / Baker のケース）も同じ扱い。
3. 当事者の表現は **後ろ姿 / シルエット / 顔を外したフレーミング / 手元のみ / 無人の空間の象徴** に限る。
4. **警察官は個人が特定できない装備越し**（ヘルメット、シルエット、装甲車の車体）に限る。実名officerを画面に列挙しない。
5. **実在の住所を再現しない。** 番地・表札・道路標識・郵便受けの文字を生成しない。
6. **読める判決文・書類を作らない。** 書類は雰囲気のみ（文字は判読不能）。
7. **流血・遺体・生々しい暴力を描かない。** 破壊は**建物に対してのみ**。Baker のケースの自死は**画で描かない**（ナレのみ・カットは閉じたドアの外観）。
8. **Lech の amicus brief に含まれる実際の被害写真（p.6-7）は使用禁止**（最高裁提出書面の写真・権利関係不明）。実在の Lech 邸の報道写真・ニュース映像も**禁止取得元**。

## 5.6 AI開示（強め・毎回）

本作は「実在の歴史的場面の再現」「実在人物の行動」「証拠写真に見える画」に該当する。したがって:

- **AI生成の静止画・i2v が画面に出ている間、常時**、右下に開示テロップを出す。
- 文字列: **`AI-assisted visualization`**（破壊された家屋の再現画は **`Artistic reconstruction — AI-assisted`** に強める）
- スタイル: Trebuchet系 / 20px / `#C9CDD4` / opacity 70% / 位置 `[W-32, H-28]` 右下揃え
- **字幕帯（下部）と縦に 56px 以上離す**（§7 ゾーン分離）
- 概要欄にも1行で開示: `Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.`

## 5.7 シーンプロンプト S01–S25（★台本の `[Sxx]` 割当に1:1対応）

台本の割当:
```
HOOK          : S02 S05 S09
FLASH-FORWARD : S23
幕1           : S01 S02 S03 S04 S06
幕2           : S07 S08 S10 S11 S12
幕3           : S13 S14 S15 S16 S17
幕4           : S18 S19 S20 S21 S22
ENDING        : S23 S24 S25
```

**各プロンプトを、構図 / カメラ角度 / 寄り引き / 光の向き / 被写体位置 を変えて 6枚ずつ 出力。upscale target 長辺 3840px。**

---

**S01 — 郊外の街路（Greenwood Village の基調）**
An ordinary American suburban street at mid-morning, edged lawns and curving sidewalks with no reason for the curve, two-story houses set back evenly, one bicycle lying on a driveway, deep ordinary quiet, no people, no visible house numbers + [共通スタイル]

**S02 — その家（ふつうの二階建て）**
A plain two-story suburban house seen from across the street in warm late-morning light, closed garage, neat trimmed hedge, ordinary and entirely unremarkable, the kind of house nobody photographs, no people, generic architecture with no identifying features + [共通スタイル]

**S03 — 開いていたドア**
A residential side door standing slightly ajar in bright daylight, the interior beyond it dim and unreadable, an ordinary doormat, no damage yet, the quiet wrongness of a door that should have been locked, no people + [共通スタイル]

**S04 — 包囲が組み上がる（昼）**
A wide high-angle view of a suburban block in flat midday sun with police vehicles converging from several directions, tape stretched across lawns, distant small silhouettes in tactical gear whose faces cannot be seen, neighbouring houses untouched + [共通スタイル]

**S05 — 最初に出てきた小さな人影（HOOK・象徴）**
A very small human silhouette walking away from a house across a sunlit lawn, seen from far behind and strongly backlit so only the outline exists, no facial features, no discernible clothing detail, protective distance, the loneliest possible framing of safety + [共通スタイル]

**S06 — 装甲車（BearCat）が芝生の上に**
A heavy armored police vehicle parked on a residential front lawn under a bright afternoon sky, its bulk absurdly out of scale beside a family house and a garden hose, dust hanging in the air, no people visible, no unit markings + [共通スタイル]

**S07 — 市の側（制度の建物）**
A modest American municipal building exterior in flat daylight, clean symmetrical facade, an empty flagpole shadow falling across the steps, institutional and impersonal, no people, no readable signage + [共通スタイル]

**S08 — 保険約款（判読不能）**
A close-up of a thick insurance policy booklet open on a kitchen table in hard window light, dense grey blocks of unreadable text, a pair of reading glasses folded beside it, one page corner lifted by air, no people, no legible words + [共通スタイル]

**S09 — 穴の空いた家（HOOK の決め画）**
A suburban two-story house in flat daylight with multiple large ragged holes punched clean through its exterior walls, the roof line still intact above them, splintered timber edges, blue sky visible through the openings, no people, catastrophic and strangely quiet + [共通スタイル]

**S10 — 粉塵と光（アスベスト）**
Dense pale dust suspended in hard shafts of sunlight inside a wrecked domestic room, particles glowing amber against deep shadow, the air itself made visible and clearly unbreathable, abstract and beautiful and wrong, no people + [共通スタイル]

**S11 — 手元だけ（救い出した物）**
Close-up of two adult hands, cropped at the wrists, holding a dust-covered fragment of a framed photograph whose image side is turned away from camera, white dust in the creases of the knuckles, raking sunlight, no face anywhere in frame + [共通スタイル]

**S12 — 子どもの部屋が空に開いている**
A child's bedroom with one wall entirely gone, open to bright sky, a small bed frame under fallen drywall, a shelf still holding two toys covered in white dust, no people, no readable text, devastating in its ordinariness + [共通スタイル]

**S13 — 連邦地裁（デンバー・昼）**
A federal district courthouse facade in strong afternoon sun, plain mid-century government stone, hard shadows from a deep entrance recess, monumental and indifferent, seen from a low angle, no people, no readable inscriptions + [共通スタイル]

**S14 — eminent domain の側（払われる収用）**
A wide empty highway right-of-way cut through open land under a bright sky, survey stakes with orange ribbon in a straight receding line, machinery parked far off, the state taking land in the open and on the record, no people + [共通スタイル]

**S15 — 第10巡回区控訴裁判所**
A stone appellate courthouse facade in raking late-afternoon light, tall columns casting hard parallel shadows across empty steps, closed doors, monumental and unmoved, no people, no readable inscriptions + [共通スタイル]

**S16 — 脚注（拘束力を持たない文書）**
Extreme close-up of the bottom edge of a single sheet of legal paper on a dark desk, one small block of unreadable footnote text isolated in a pool of light while the rest of the page falls into shadow, no legible words, no people + [共通スタイル]

**S17 — 2年後の空き地**
An empty flat lot of bare dirt and weeds between two intact suburban houses under a wide bright sky, a concrete foundation outline still faintly visible in the ground, ordinary life continuing on both sides, no people + [共通スタイル]

**S18 — Indiana（割れた窓・催涙弾の跡）**
A modest single-story house in flat overcast daylight with every front window broken out, pale residue streaking the siding beneath the openings, spent canisters scattered on the grass, a garden ornament untouched, no people + [共通スタイル]

**S19 — Texas（吹き飛ばされたドアと倒れたフェンス）**
A suburban house with its front door and garage door blown open and hanging, a wooden backyard fence pushed flat in a straight line toward the camera by something heavy, hard Texas sun, no people, no vehicles in frame + [共通スタイル]

**S20 — Tennessee（ポーチに散った缶）**
A covered wooden porch of a rural house in hazy afternoon light, dozens of spent gas canisters scattered across the boards and steps, a screen door hanging off one hinge, rocking chair still upright, no people + [共通スタイル]

**S21 — Los Angeles（印刷工場）**
The interior of a small commercial print shop lit only by daylight coming through fresh holes in the roof and walls, printing equipment covered in pale residue, paper stock scattered, an industrial roll-up door standing open to a bright alley, no people, no readable print + [共通スタイル]

**S22 — Las Vegas（払われた側）**
A desert-suburb stucco house in flat harsh sunlight with a section of freshly patched wall in a slightly different shade than the rest, new mortar clean and bright, repair completed and invisible from the street, palm shadow across the driveway, no people + [共通スタイル]

**S23 — 署名（FF と ED の共通画）**
Extreme close-up of one adult hand, cropped at the wrist, resting a pen at the foot of a thick legal document on a plain table in cool window light, the page text completely unreadable, deliberate and unhurried, no face, no signature legible + [共通スタイル]

**S24 — 「some people alone」（公の負担の象徴）**
A long aerial row of near-identical suburban rooftops under an even bright sky, every roof intact except one in the middle which is torn open to the interior, the pattern broken at exactly one point, no people + [共通スタイル]

**S25 — ED / 未解決の余韻**
A single suburban street at late dusk with warm light in every window except one house that stands dark and empty, the sky still holding the last blue, quiet and unresolved, no people, no visible address + [共通スタイル]

*(S01–S25 を各6枚 = 150枚)*

## 5.8 scene_plan（row8/row7・「ナレが言っている事を、その画で示す」）

`04_scenes/scene_plan.v002.json` に **1ビート（1文）ごとに**次の8フィールドを**全て**埋める。空欄・「等」「など」は禁止。

```jsonc
{
  "beat_id": "A1-014",
  "sentence": "The nine-year-old got out.",         // 台本の1文（逐語）
  "start_sec": 71.20, "end_sec": 73.05,
  "visual_question": "何が画面で答えられるべきか = 子が家の外に出た瞬間",
  "visual_verb": "walk-away",                        // 画の中で起きる動詞
  "start_state": "家の玄関が画面中央・人影なし",
  "end_state": "小さな人影が画面右下に抜け、玄関だけが残る",
  "eye_target": "玄関の暗がり → 右下の輪郭",          // 視線をどこからどこへ運ぶか
  "sync_words": ["got", "out"],                      // faster-whisper 語タイムに合わせる語
  "source_type": "ai_still",                         // ai_still|i2v|factory|figure|ae_beat
  "asset_id": "S05_03",
  "truth_status": "record"                           // record|attributed|symbolic
}
```

**`truth_status` の3値（R2 の帰属を機械的に担保する）:**
- `record` = 判決文・公的記録にある事実（例: 19時間・$5,000・日付）
- `attributed` = 当事者の主張（例: 5千ドルに放棄条件が付いていたという Lech の主張、アスベスト、$250,000）→ **画面テロップに `ACCORDING TO LECH'S BRIEF` を必ず添える**
- `symbolic` = 象徴表現（人影・空き地・屋根の列）→ **AI開示テロップ必須**

**語同期の決め所（faster-whisper の語タイムでフレーム一致させる）:**
`"nineteen hours"` / `"Then it didn't"` / `"five thousand dollars"` / `"excluded"` / `"two hundred fifty thousand"` / `"Nothing owed"` / `"Considerable appeal"` / `"the Tenth Circuit"` / `"it declined"` / `"further percolation"` / `"Some people alone"` / `"the address"`

---

# 6. モーション設計（row8 `animation_density`）

## 6.1 ハード要件と設計値

| 要件 | 閾値 | 設計値 |
|---|---|---|
| ゼロモーション区間 | **0** | 0（全静止画に Ken Burns またはパララックス） |
| 準静止（near-still） | ≤ 全尺の10% | **≤6%**（目標） |
| 単一ホールド | ≤3秒（設計上限 **2秒**） | 最長 2.0秒 = 幕間の余韻カット4箇所のみ |
| トランジション無しのハードカット | **0** | 0（全カット境界に 0.3–0.5秒クロスフェード） |
| 平均ショット長 | ≤約6秒 | **3.22秒** |
| 5秒超の長止め | ≤8箇所 | **0箇所** |

## 6.2 全 span に付けるモーション（shotlist の必須フィールド）

**静止画（Ken Burns ベクトル）— 最低 6% のスケール変化を必ず入れる:**

| motion_id | 内容 | 数値 |
|---|---|---|
| `KB_IN` | 押し込み | scale `1.000 → 1.075` / `Easing.out(Easing.cubic)` / 区間全長 |
| `KB_OUT` | 引き | scale `1.075 → 1.000` / `Easing.out(Easing.cubic)` |
| `KB_DRIFT_L` | 左流し | scale `1.06` 固定 / x `+28px → -28px` / `Easing.inOut(Easing.sin)` |
| `KB_DRIFT_R` | 右流し | scale `1.06` 固定 / x `-28px → +28px` / `Easing.inOut(Easing.sin)` |
| `KB_RISE` | 迫り上がり | scale `1.02 → 1.08` / y `+18px → -18px` / `Easing.out(Easing.cubic)` |
| `PARALLAX_2P` | 2.5Dパララックス（前景/背景を分離） | 前景 x `±34px` / 背景 x `∓12px` / `spring{damping: 26, stiffness: 90}` |

**割当ルール（機械判定可能に書く）:**
- 幕1・幕2の「家」「生活」の画 → `KB_IN` または `PARALLAX_2P`
- 破壊の画（S09 S10 S12 S18–S21）→ `KB_RISE`（下から迫る = 圧）
- 制度の画（S07 S13 S15 S16）→ `KB_OUT`（引く = 遠さ・冷たさ）
- 空白の画（S17 S24 S25）→ `KB_DRIFT_L` / `KB_DRIFT_R`
- **同じ motion_id を3カット以上連続させない**（ゲートには無いが紙芝居感の主因）

**トランジション（全カット境界・例外なし）:**

| transition_id | 秒 | 使用位置 |
|---|---|---|
| `XF_030` | 0.30 | 通常のカット間（既定） |
| `XF_050` | 0.50 | 幕内のセクション境界 |
| `DIP_BLACK_060` | 0.60 | 幕の変わり目 4箇所のみ |
| `HARD_2015` | 0.00 → **例外的にハードカット1箇所のみ許可** | FF → 幕1（台本 "then hard cut to 2015" の指定）。**この1箇所だけ `animation_density` の例外として shotlist に `"hardcut_reason": "script_directed"` を明記する** |

> **禁止演出（ship-gate で落ちる）:** 紙芝居（静止画放置）／左→右の縦スイープライン／全画面の黄・金ウォッシュ／ただのズーム・パンのみ／ハードカットの「かくっ」（速度リセット）／リニアイージング／opacity単独の演出。
> **`opacity` を動かすときは必ず `translateY` / `scale` / `scaleX` のいずれかと対にする。単独禁止。**

## 6.3 高速な動きのモーションブラー

`@remotion/motion-blur` の `Trail` を次の箇所に適用する（`npm i @remotion/motion-blur`）:

| 適用先 | パラメータ |
|---|---|
| MGビートの数値カウントアップ | `layers={6} lagInFrames={1.2} trailOpacity={0.45}` |
| タイトル文字のスタッガー切れ上がり | `layers={6} lagInFrames={1.2} trailOpacity={0.45}` |
| `DIP_BLACK_060` 直前の画の抜け | `layers={4} lagInFrames={0.9} trailOpacity={0.35}` |

---

# 7. レイヤー構成 と ゾーン分離

## 7.1 本編カットのレイヤー構成（下 → 上・最低3レイヤー要件に対し6レイヤー）

| L | 名前 | 内容 | EP40 の値 |
|---|---|---|---|
| **L0** | ルート背景 | `AbsoluteFill` 単色 | `#0d0b08`（暖色寄りの黒） |
| **L1** | **グラデ背景** | 放射グラデーション | `radial-gradient(120% 120% at 50% 35%, #3a2f1c 0%, #1c1710 45%, #0d0b08 100%)` |
| **L2** | **グリッド/ライン** | 縦横 64px の反復線＋放射マスク＋ドリフト | `repeating-linear-gradient(0deg / 90deg, #E5B53A22 0px 1px, transparent 1px 64px)`、`maskImage: radial-gradient(120% 90% at 50% 45%, black 35%, transparent 80%)`、`translateY 0 → 48px` / `Easing.inOut(Easing.sin)` |
| **L3** | **グロー** | 主役裏の放射グロー | `width*0.62 × height*0.36`、`radial-gradient(closest-side, #E5B53A88 0%, #E5B53A22 45%, transparent 75%)`、`filter: blur(28px)` |
| **L4** | **主役**（静止画 / i2v / factory） | §6.2 のモーション | — |
| **L5** | **テロップゾーン**（`on_screen_text` / 出典テロップ） | 上部 or 中央 | §7.2 |
| **L6** | **字幕ゾーン** | 下部帯 | §7.2 |

## 7.2 ゾーン分離（VIDEO_RULES §13・**一度も重ねない**）

| ゾーン | 縦位置（1080基準） | 内容 | スタイル |
|---|---|---|---|
| **テロップ見出し** | `y = 96 – 260`（上部） | `on_screen_text`・幕タイトル・`ACCORDING TO LECH'S BRIEF` | Impact系 / 64px / `#F5F7FA` / letterSpacing 4 |
| **中央テロップ** | `y = 420 – 660` | 〔CARD〕タイポ（§8）・AEヒーロービート | §8/§9 |
| **出典テロップ（金ライン）** | `y = 742 – 786` | 出典表示。**金 `#E5B53A` の 3px 下線付き** | Trebuchet系 / 28px |
| **字幕帯** | `y = 872 – 1010`（下部帯） | `.srt` の描画 | 下記 |
| **AI開示** | `y = 1024 – 1052`（右下） | `AI-assisted visualization` | Trebuchet系 / 20px / `#C9CDD4` / opacity 70% |

**字幕の確定スタイル:**
- 最大2行 / **1行 ≤42字** / フォントサイズ **54px**（範囲48–60px内）
- 白文字 `#FFFFFF` + 濃い縁取り（`textShadow: 0 0 6px #000, 0 2px 4px #000`）
- 半透明黒帯 `rgba(6,8,12,0.62)`（不透明度62% = 55–70%の範囲内）
- 中央寄せ / `lineHeight: 1.28`
- **出典テロップ（y=742–786）と字幕帯（y=872）は縦に 86px 離れている** ✓ 重ならない

## 7.3 Caption QC（row3/4・確定値）

| 項目 | 確定値 |
|---|---|
| ナレとのトークン一致 | **≥99%**（faster-whisper 強制アラインメント） |
| `.srt` のランタイムカバー率 | **≥95%**（734.47秒 × 0.95 = 697.7秒以上） |
| 1キュー | **1息継ぎ**（台本の段落・句読点で分割済み） |
| 行数 / 行長 | ≤2行 / 1行 ≤42字 |
| キュー長 | **1.0秒 ≤ x ≤ 6.0秒** |
| キュー間 | **≥2フレーム**（= 66.7ms @30fps） |
| CPS | **≤17** |
| 単語割り | **禁止** |
| 1語孤立キュー | **禁止**（"Then it didn't." は3語で1キュー・OK。"Considerable appeal." は2語で1キュー・OK） |
| 音とのズレ | **≤120ms** |

> **注意:** 台本の `*(silence — Xs)*` 区間には**字幕キューを置かない**。ここにキューを置くとナレとの一致率が落ち、`.srt` カバー率の分母だけ増える。
> **`〔CARD〕` は字幕ではなく中央テロップゾーンに描く**（§8）。`.srt` には入れない。

---

# 8. 〔CARD〕タイポグラフィ（Remotion 実装・6枚）

台本の `〔CARD: ...〕` は**画面タイポであり、ナレは読み上げない**。以下6枚を Remotion の `CardTypo` コンポーネントで実装する（新規コンポーネント1つのみ。ビートとは別枠）。

| ID | 秒 | 文字列 | レイアウト |
|---|---|---|---|
| `c01` | **4.20 – 7.20** | `JUNE 3, 2015` | 中央・Impact系 96px・`#F5F7FA`・下に金の 320×4 ライン |
| `c02` | **24.10 – 26.62** | `MAY 2026` | 同上（`c01` と同一レイアウト＝対句として機能させる） |
| `c03` | **181.60 – 185.60** | `$5,000` | 中央・Impact系 **180px**・金 `#E5B53A`。**AE b03 と同一区間なので AE 側で描く（Remotion 側は空ける）** |
| `c04` | **227.50 – 234.50** | `INTENTIONAL ACTS BY GOVERNMENT OFFICIALS — EXCLUDED` | 中央・Impact系 **52px**・2行分割（`INTENTIONAL ACTS BY` / `GOVERNMENT OFFICIALS — EXCLUDED`）。**AE b04 が描く** |
| `c05` | **372.50 – 379.50** | `NOT BINDING PRECEDENT — MAY BE CITED FOR ITS PERSUASIVE VALUE` | **AE b07 が描く**（2行分割） |
| `c06` | **628.00 – 632.50** | `FURTHER PERCOLATION` | 中央・Impact系 110px・シルバー `#96A0AE`・**アニメは文字間 letterSpacing `18 → 4` の収束のみ**（打ち消されていく語感） |

**c01 / c02 / c06 の共通アニメーション（数値確定）:**

| 要素 | 開始 | 手法 | 変化量 | イージング |
|---|---|---|---|---|
| 文字 translateY | f0 | `spring` | `110% → 0`（`overflow:hidden` マスク切れ上がり） | `{damping: 16, mass: 1}` |
| 文字 opacity | f0 | `interpolate(springVal,[0,0.25],[0,1])` | 0 → 1 | clamp（**translateY と併用**） |
| 文字スタッガー | — | — | **2フレーム/文字**（`Math.max(1, round(fps*0.067))` @30fps） | — |
| 金ライン scaleX | f0 + 12 | `spring` | `0 → 1`・`transformOrigin: 'left center'` | `{damping: 16, mass: 0.8}` |
| 退場 | 区間末 -0.4秒 | `interpolate` | scale `1.00 → 1.04` + opacity `1 → 0` | `Easing.out(Easing.cubic)`（**scale と併用**） |

**マスク切れ上がりの必須構造（テキストの基本形）:**
```tsx
<span style={{display:'inline-block', overflow:'hidden', paddingBottom:'0.12em'}}>
  <span style={{display:'inline-block', transform:`translateY(${y}%)`, opacity:charOpacity, whiteSpace:'pre'}}>
    {ch}
  </span>
</span>
```

---

# 9. After Effects ヒーロービート（8枠）

## 9.1 パイプライン（EP38 で measured 済み・2026-07-18）

```
[1] Remotion で本編を完成 → lech_final_bgm.v002.mp4（音声ミックス済み）
[2] build_lech_hero_jsx.py が beats.json と lech_hero.jsx を生成
[3] AfterFX -noui -r lech_hero.jsx → 各ビートを 1920x1080@30fps の不透明 mp4 で書き出し
[4] composite_lech_hero.py が ffmpeg overlay + enable='between(t,start,end)' で焼き込み
[5] 出力 → lech_final_bgm.v003_ae.mp4（v002 は絶対に上書きしない）
```

## 9.2 スロット確定表（★v001 の b01–b08 は破棄。以下が確定値）

| ID | 内容 | 数値ID | レイアウト | カウント型 | **start – end（秒）** | 尺 | 対応する台本の行 |
|---|---|---|---|---|---|---|---|
| **b01** | 事態の命名 | — | **E: LABEL_STAMP** | なし | **94.00 – 99.00** | 5.0 | "the situation acquired a name. High-risk barricade." |
| **b02** | 立てこもり時間 | N02 | **A: CENTER_STACK** | `CT_INT` | **150.00 – 156.50** | 6.5 | "Nineteen hours." |
| **b03** | 仮住まい費用 | N04 | **A: CENTER_STACK** | `CT_MONEY` | **181.00 – 187.50** | 6.5 | 〔CARD: $5,000〕 |
| **b04** | 保険の免責事由 | — | **F: CLAUSE_STRIKE** | なし | **227.50 – 234.50** | 7.0 | 〔CARD: INTENTIONAL ACTS…EXCLUDED〕 |
| **b05** | 借入額 | N05 | **A: CENTER_STACK** | `CT_MONEY` | **278.00 – 285.00** | 7.0 | 〔CARD: $250,000〕 |
| **b06** | 控訴審の日付と裁判所 | N08 | **C: DATE_STAMP** | `CT_DATE` | **358.00 – 364.00** | 6.0 | "On October 29, 2019, the Tenth Circuit affirmed" |
| **b07** | 拘束力なき文書 | — | **F: CLAUSE_STRIKE** | なし | **372.50 – 379.50** | 7.0 | 〔CARD: NOT BINDING PRECEDENT…〕 |
| **b08** | 5つの住所・5つの結論 | N11–N15 | **G: SPLIT_TALLY** | `CT_MONEY`×5 | **547.00 – 554.50** | 7.5 | 幕4の5件の総括 |

### 検算
```
[1] 単調増加・重複ゼロ
    94.0<99.0 < 150.0<156.5 < 181.0<187.5 < 227.5<234.5
  < 278.0<285.0 < 358.0<364.0 < 372.5<379.5 < 547.0<554.5     ✓

[2] HOOK(0–26.62) / BrandOpening(26.62–30.12) / ENDING payoff(646.18–) /
    BrandEndcard(725.47–734.47) に1秒も重ならない
    最小 94.0 > 30.12  ✓        最大 554.5 < 646.18  ✓

[3] b06 と b07 の間隔 = 372.5 − 364.0 = 8.5秒   ✓ 連続データカードにならない
[4] 合計 52.5秒 / 734.47 = 7.1%                 ✓ 過剰でない
[5] レイアウト種類 = A, C, E, F, G = 5種         ✓ ≥3種
```

## 9.3 `beats.json` スキーマ

**パス:** `episodes/PD-2026-040-lech/08_edit/ae_hero/beats.json`

```jsonc
{
  "schema_version": "lech_beats.v2",
  "episode_id": "PD-2026-040-lech",
  "fps": 30, "width": 1920, "height": 1080,
  "beats": [{
    "id": "b02",                                 // ^b0[1-8]$
    "layout": "CENTER_STACK",                    // CENTER_STACK|DATE_STAMP|LABEL_STAMP|CLAUSE_STRIKE|SPLIT_TALLY
    "count_type": "CT_INT",                      // CT_INT|CT_MONEY|CT_DATE|null
    "num_id": "N02",                             // §0.5 の数値ID。表に無い ID は exit 1
    "start": 150.000, "end": 156.500, "dur": 6.500,
    "still": "H:/pd-media/assets/ai/lech/S09_04.png",  // 絶対パス・スラッシュ区切り・長辺≥3840
                                                       // 本編の同区間で使う画像と重複しないこと
    "top": "THE BARRICADE",                      // 全大文字 1..24字。§0.4 の検査対象
    "bottom": "AND THE HOUSE STOOD",              // 全大文字 1..28字。§0.4 の検査対象
    "caption": "The house stood for nineteen hours.",  // 1行・改行禁止・最大50字
    "footnote": null,                            // 1行・最大44字・null可
    "value": 19, "value_b": null,
    "decimals": 0, "thousands": false,
    "prefix": "", "suffix": " HOURS",
    "tally": null,                               // SPLIT_TALLY のときのみ配列（§9.4.5）
    "numKeys": [[0.55,"0"],[0.61,"3"]],          // Python が全事前計算した (時刻, 表示文字列)
                                                 // JS 側で数値整形を一切しないこと（EP38の確定ルール）
    "numReveal": 0.45,
    "head": 0.1333, "tail": 0.1333,              // = 4/30 の黒シーム
    "out": "C:/.../08_edit/ae_hero/render/b02.mp4"
  }]
}
```

**不変条件（`validate_lech_beats.py` が検査・BLOCKING）:**
1. `start` 昇順・区間の重なりゼロ
2. 全区間が §9.2 検算[2]の禁止帯に重ならない
3. `end <= 734.47`
4. `still` が実在し長辺 ≥3840px、かつ**本編の同区間で使う asset と別物**
5. `top` / `bottom` / `caption` / `footnote` が §0.4 の R1–R8 を通る
6. `num_id` が §0.5 の表に存在する（存在しない数字を画面に出させない）
7. **Remotion の `figures[]` 28枠と1秒でも重ならない**（両方を突き合わせて検査）

## 9.4 レイアウト定義（5種）

**共通レイヤースタック（下 → 上）。EP38 `build_kfc_hero_jsx.py` の実証構成を踏襲する:**

| L | 内容 | 実装 |
|---|---|---|
| L9 | 黒ソリッド背景 | `addSolid([0,0,0])` |
| L8 | 静止画 | scale `fill → fill*1.08`（0→dur・ease 25）、position `[W/2-18, H/2+10] → [W/2+18, H/2-10]`（ease 20） |
| L7 | グレードウォッシュ | **暖色** `addSolid([0.14,0.11,0.06])` / MULTIPLY / opacity **30** |
| L6 | 羽根付き楕円ビネット | 黒ソリッド + SUBTRACT マスク・feather `[260,260]`・opacity 62 |
| L5 | グロー（下中央からの ADD ランプ） | Ramp: start `[W/2, H*0.42]` GOLD → end `[W/2, H*0.95]` 黒 / radial(2) / opacity 0→22→14 |
| L4 | ライトスイープ | 白ソリッド 360×H*1.6 / ADD / `"ADBE Rotate Z"` = 18 / position `-300 → W+300`（0.5s→1.25s・ease 45）/ opacity 0→18→0 |
| L3 | 上ラベル（Oswald） | 各レイアウトの座標 |
| L2b | アクセントライン（GOLD・scaleX ワイプ） | `[0,100] → [100,100]`（0.55s→1.05s・ease 90）/ `motionBlur = true` |
| L2 | 主数値（Anton・GOLD） | §9.5 のカウントアップ / `motionBlur = true` |
| L1b | 下ラベル（Oswald・WHITE） | reveal 1.15s |
| L1 | 字幕ロワーサード | バー `[0.02,0.04,0.08]` W×130 / opacity 0→64→0 |
| L0 | 黒シームディップ | head/tail 各4フレーム・opacity 100→0 / 0→100・ease 40 |

**色定数（0..1 float）:**
```python
GOLD   = [0.898, 0.710, 0.227]   # #E5B53A — EP40 アクセント
WHITE  = [0.961, 0.969, 0.980]
SILVER = [0.588, 0.627, 0.682]
DUST   = [0.827, 0.769, 0.667]   # 弱い側・非主役
RED    = [0.780, 0.290, 0.250]   # CLAUSE_STRIKE の取り消し線のみ
```

**フォント:** 数値 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**
（`C:\Users\aab15\AppData\Local\Microsoft\Windows\Fonts\Anton.ttf` / `Oswald.ttf` に実在確認済み）
必ず EP38 と同じ `psName()` ランタイム解決を使い、無言の代替フォント置換を防ぐ。

### 9.4.1 LAYOUT A — CENTER_STACK（b02 / b03 / b05）

| 要素 | 位置 | フォント/サイズ | トラッキング | 色 |
|---|---|---|---|---|
| 上ラベル | `[W/2, H*0.205]` | Oswald 44 | 340 | SILVER |
| アクセントライン | `[W/2, H*0.485]`・460×6 | — | — | GOLD |
| 主数値 | `[W/2, H*0.42]` | Anton **250** | 0 | GOLD |
| 下ラベル | `[W/2, H*0.60]` | Oswald 64 | 120 | WHITE |
| 字幕バー | `[W/2, H*0.90]`・W×130 | Oswald 42 | 20 | WHITE |

**確定ラベル:**
```
b02: top="THE BARRICADE"      bottom="AND THE HOUSE STOOD"   value=19   suffix=" HOURS"
b03: top="WHAT THE CITY OFFERED" bottom="TEMPORARY LIVING EXPENSES" value=5000 prefix="$" thousands=true
b05: top="WHAT HE BORROWED"   bottom="TO REBUILD IT"         value=250000 prefix="$" thousands=true
```
> `b03` の `bottom` は **"COMPENSATION" と書かない**。台本・第10巡回区の記録はいずれも「仮住まい費用の援助」であり、補償と断定すると帰属違反になる。

### 9.4.2 LAYOUT C — DATE_STAMP（b06）

| 要素 | 位置 | フォント/サイズ | 色 |
|---|---|---|---|
| 上ラベル | `[W/2, H*0.30]` | Oswald 44 / tracking 340 | SILVER |
| 年（主数値） | `[W/2, H*0.46]` | Anton **190** | GOLD |
| 横罫 | `[W/2, H*0.545]`・620×4 | — | GOLD opacity 92 |
| 下ラベル | `[W/2, H*0.63]` | Oswald 52 / tracking 120 | WHITE |
| `footnote` | `[W/2, H*0.72]` | Oswald 34 / tracking 90 | SILVER・opacity 0→88（3.6→3.9s・ease 70） |

**b06 の確定値（accuracy_lock 準拠・この文字列を使う）:**
```
top      = "OCTOBER 29, 2019"
value    = 2019          （thousands=false 必須。2,019 と出たら即バグ）
bottom   = "THE TENTH CIRCUIT AFFIRMED"
footnote = "AN ORDER AND JUDGMENT, NOT AN OPINION"
```
> **`footnote` に "SUPREME COURT" を書かない。** 不受理の事実は幕3のナレと Remotion timeline 図版で扱う。

### 9.4.3 LAYOUT E — LABEL_STAMP（b01・数値なし）

事態が制度上の呼称を得た瞬間を刻印する。数値レイヤーを持たない。

| 要素 | 位置 | フォント/サイズ | 色 |
|---|---|---|---|
| 上ラベル | `[W/2, H*0.38]` | Oswald 40 / tracking 340 | SILVER |
| 主ラベル | `[W/2, H*0.50]` | Anton **120** / tracking 8 | WHITE |
| 下罫 | `[W/2, H*0.585]`・780×5 | — | GOLD |
| 字幕バー | LAYOUT A と同一 | | |

**確定値:** `top = "WHAT IT WAS NOW CALLED"` / 主ラベル = `"HIGH-RISK BARRICADE"` / `bottom = null`

**タイミング（5.0s）:** 0.20s 上ラベル reveal → 0.55s 主ラベルが `scale 1.06 → 1.00` + opacity `0→1`（**scale と併用**・`ease 60`）→ 0.95s 下罫 `scaleX [0,100]→[100,100]`（`transformOrigin` 左端・ease 90）→ 以降ホールド。

### 9.4.4 LAYOUT F — CLAUSE_STRIKE（b04 / b07・数値なし）

**条項の文言を出し、その上に線を引く。** EP40 の「逃げ場が順に閉まる」構造の視覚化。

| 要素 | 位置 | フォント/サイズ | 色 |
|---|---|---|---|
| 上ラベル | `[W/2, H*0.24]` | Oswald 40 / tracking 340 | SILVER |
| 条項テキスト（1行目） | `[W/2, H*0.42]` | Oswald **58** / tracking 40 | WHITE |
| 条項テキスト（2行目） | `[W/2, H*0.52]` | Oswald **58** / tracking 40 | WHITE |
| 取り消し線 | `[W/2, H*0.47]`・幅 1180×5 | — | **RED** |
| 下ラベル | `[W/2, H*0.66]` | Oswald 52 / tracking 120 | WHITE |

**タイミング（7.0s）:**
- 0.20s: 上ラベル reveal
- 0.45–0.95s: 条項1行目が `translateY 40px → 0` + opacity `0→1`（**併用**・`ease 65`）
- 0.75–1.25s: 条項2行目（**0.30秒のスタッガー**）
- **1.90–2.60s: 取り消し線が `scaleX [0,100]→[100,100]`（`transformOrigin` 左端・ease 92・`motionBlur = true`）**
- 2.75s: 条項テキスト opacity `100 → 46`（0.35s・ease 60）＝ 無効化された感
- 3.10s: 下ラベル reveal
- 以降ホールド（≥1.20秒）

**確定値:**
```
b04: top="HIS HOMEOWNER'S POLICY"
     line1="INTENTIONAL ACTS BY"
     line2="GOVERNMENT OFFICIALS - EXCLUDED"     ← ハイフン。em-dash は AE で文字化けするため使わない
     bottom="NO COVERAGE"
b07: top="THE COURT'S OWN FIRST-PAGE FOOTNOTE"
     line1="NOT BINDING PRECEDENT"
     line2="MAY BE CITED FOR ITS PERSUASIVE VALUE"
     bottom="THIS IS THE DOCUMENT THAT DECIDED IT"
```

### 9.4.5 LAYOUT G — SPLIT_TALLY（b08・EP40 で最も重要な1枚）

**5つの住所を横に並べ、4つが黒（払われない）、1つだけ金（払われた）にする。**「憲法ではなく、どの市に住んでいるか」という主題の一撃。

| 要素 | 位置 | フォント/サイズ | 色 |
|---|---|---|---|
| 上ラベル | `[W/2, H*0.14]` | Oswald 40 / tracking 340 | SILVER |
| 列（5本）| x = `W*0.14, 0.32, 0.50, 0.68, 0.86` | — | — |
| 各列 州名 | `y = H*0.30` | Oswald 34 / tracking 120 | SILVER |
| 各列 金額 | `y = H*0.44` | Anton **86** | 列1–4 **DUST** / 列5 **GOLD** |
| 各列 巡回区 | `y = H*0.56` | Oswald 30 / tracking 90 | SILVER |
| 各列 結論 | `y = H*0.66` | Oswald 38 / tracking 60 | 列1–4 SILVER opacity 60 / 列5 **GOLD** |
| 下ラベル | `[W/2, H*0.80]` | Oswald 52 / tracking 120 | WHITE |

**`tally` 配列の確定値（§0.5 N11–N15 由来。この5行以外を足さない）:**
```jsonc
"tally": [
  {"place":"INDIANA",   "value":16000, "circuit":"SEVENTH CIRCUIT", "verdict":"NOTHING"},
  {"place":"TEXAS",     "value":60000, "circuit":"FIFTH CIRCUIT",   "verdict":"NOTHING"},
  {"place":"TENNESSEE", "value":70000, "circuit":"SIXTH CIRCUIT",   "verdict":"NOTHING"},
  {"place":"CALIFORNIA","value":null,  "circuit":"NINTH CIRCUIT",   "verdict":"NOTHING"},
  {"place":"NEVADA",    "value":30000, "circuit":"NO COURT",        "verdict":"PAID"}
]
```
> **列4（California / Pena）の `value` は `null`。** 台本は Pena の金額を出していない（台帳外）。**金額欄は空白のまま描く**（0 と書いたら事実誤り）。
> `top = "SAME EMERGENCY. SAME DAMAGE."` / `bottom = "THE DIFFERENCE IS THE CITY"`

**タイミング（7.5s）:**
- 0.20s: 上ラベル reveal
- 0.55s / 0.85s / 1.15s / 1.45s / 1.75s: 各列が **0.30秒スタッガー**で `translateY 34px → 0` + opacity `0→1`（**併用**・`ease 62`）
- 各列の金額は列の出現から 0.10秒後にカウントアップ（`CT_MONEY`・窓 0.80秒）。列4はカウントせず罫線のみ
- 3.30s: 列1–4 の `verdict` が opacity `100→60` に沈む（0.40s・ease 55）
- **3.70s: 列5 の `verdict` "PAID" が GOLD で `scale 1.12 → 1.00` + opacity `0→1`（0.50s・ease 70）**
- 4.60s: 下ラベル reveal
- 以降ホールド（≥1.20秒）

## 9.5 カウントアップ型（すべて Python 側で全キーを事前計算）

EP38 で実証済みの `count_keys()` を踏襲（ease-out cubic・最後に正確値へ settle）。

| 型ID | 用途 | decimals | thousands | prefix | suffix | キー数 | 窓 |
|---|---|---|---|---|---|---|---|
| `CT_INT` | 時間・回数 | 0 | false | "" | " HOURS" | 18 | 0.55→1.55s |
| `CT_MONEY` | ドル | 0 | **true** | `"$"` | "" | **24** | 0.55→1.85s |
| `CT_DATE` | 年 | 0 | **false** | "" | "" | **12** | 0.55→1.25s |

**`CT_DATE` の注意:** `thousands=false` 必須。`2,019` と出たら即バグ。

## 9.6 カウント窓と区間の関係

```
0.000                      dur
|--head--|--reveal--|--count--|--hold--|--tail--|
  4/30s              §9.5の窓          ≥1.20s   4/30s
```
**カウント終了から区間終端まで最低 1.20 秒のホールドを確保する。** `dur < (count_end + 1.20 + tail)` になったら `build_lech_hero_jsx.py` は **exit 1**（黙って詰めない）。

## 9.7 コンポジタ（`scripts/ae/composite_lech_hero.py`）

EP38 の `composite_kfc_hero.py` をベースに、パスと定数のみ差し替える。**SKIP ロジックは1行も削らない。**

```
BASE     = episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v002.mp4
OUT      = episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v003_ae.mp4
FFMPEG   = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W, H, FPS = 1920, 1080, 30
```

**SKIP条件（この4つを必ず実装する。1つでも欠けると作品が壊れる）:**
1. `render/<id>.mp4` が存在しない → SKIP
2. 解像度が `1920x1080` でない → SKIP
3. 実測尺 `< dur - 0.3` → SKIP
4. `beat.end > base_dur` → SKIP

**ffmpeg 呼び出し（実証済みの形）:**
```
[k:v] setpts=PTS-STARTPTS+<start>/TB, format=yuv420p [bk]
[prev][bk] overlay=0:0:eof_action=pass:enable='between(t,<start>,<end>)' [vk]
-map [vN] -map 0:a -r 30 -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy
```
**出荷済みファイルを絶対に上書きしない。** 出力は必ず `_v003_ae` サフィックス。

## 9.8 このマシン固有の罠（EP38 で実際に踏んで潰した。1つでも忘れると無言で品質が落ちる）

| # | 罠 | 正しい対処 |
|---|---|---|
| 1 | **イーズが無言で効かず等速になる** | `setTemporalEaseAtKey` の配列次元は spatial プロパティ（Position）では**1個**。`var dim = prop.isSpatial ? 1 : (prop.value instanceof Array ? prop.value.length : 1);` |
| 2 | **テンプレート名が英語だと失敗する** | AE 2026・日本語ロケール。RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**。英語名は try/catch のフォールバックに置くだけ |
| 3 | **字幕に `\n` を入れると literal で表示される** | AE の TextDocument の改行は `\n` ではない。**`caption` は1行に保つ**（§9.3 で最大50字・改行禁止としている理由）。CLAUSE_STRIKE の2行は**別レイヤー**にする（改行文字を使わない） |
| 4 | **`app.newProject()` が headless でハングする** | `-noui` では保存プロンプトで固まる。**使うな。** 既存の同名コンプを防御的に削除: `for (i=numItems; i>=1; i--) if (item instanceof CompItem && name.indexOf("LECH_")===0) item.remove();` |
| 5 | **ビルドが遅く、早期killしてしまう** | ビルド ~100–120秒 / レンダは速い。**jsx 末尾が書く完了マーカー `render/_build_ok.txt` をポーリングせよ。** タイムアウトは最低 300秒 |
| 6 | **AfterFX/aerender の起動がブロックする** | **デタッチ起動 + 出力ファイルのポーリング**。jsx の末尾で必ず `app.quit()` |
| 7 | **モーションブラーが効かない** | `comp.motionBlur = true` **だけでは無効**。動かすレイヤー個別に `layer.motionBlur = true`（数値・アクセントライン・取り消し線・列） |
| 8 | **`"ADBE Rotation"` が null を返す** | 2Dレイヤーの回転は **`"ADBE Rotate Z"`**（ライトスイープの18度で使う） |
| 9 | **レイヤーの outPoint がコンプ末尾に残る** | `inPoint` だけ設定すると尻が残る。**inPoint と outPoint の両方を設定する** |
| 10 | **画像シーケンスの fps が 30 にならない** | 読み込み後に必ず `item.mainSource.conformFrameRate = 30;` |
| 11 | 実行パス | `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe` / `aerender.exe`（実在確認済み） |
| 12 | GPU | RTX4090 だが**ソフトウェアレンダで固定**（`proj.gpuAccelType = GpuAccelType.SOFTWARE`）。安定性優先・EP38で実証 |
| 13 | **em-dash / 全角記号が AE で豆腐になる** | ラベル・条項テキストは **ASCII のみ**。`—` は `-` に置換（§9.4.4 の b04 line2 参照） |

## 9.9 実行コマンド（そのまま使える形）

```bash
# [1] beats.json と jsx を生成
"C:/Users/aab15/Documents/prime-documentary/.venv/Scripts/python.exe" \
  "C:/Users/aab15/Documents/prime-documentary/scripts/ae/build_lech_hero_jsx.py"

# [2] AE でビルド＋レンダ（デタッチ起動。マーカーをポーリングする）
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-040-lech/08_edit/ae_hero/lech_hero.jsx"
# → render/_build_ok.txt が出るまで待つ（最大300秒）
# → 続いて render/b0*.mp4 が8本揃うまで待つ（最大600秒）

# [3] 本編に焼き込み（v002 は不変・v003_ae を新規作成）
"C:/Users/aab15/Documents/prime-documentary/.venv/Scripts/python.exe" \
  "C:/Users/aab15/Documents/prime-documentary/scripts/ae/composite_lech_hero.py"
```

---

# 10. Remotion MGビート 28枠（`figures` 契約）— AEの8枠と合わせて36枠

**実装:** 既存の `remotion/src/components/FigureBeats.tsx` の `FigureSpec` をそのまま使う（**新規コンポーネントを作らない**）。`lech_film.json` の `figures[]` に28要素を入れる。

## 10.1 種類の配分（7種）

| kind | 枠数 | EP40 での用途 |
|---|---|---|
| `ActTitle` | 4 | 幕1〜幕4の幕頭（39.2 / 177.3 / 318.5 / 446.3 秒） |
| `timeline` | 5 | 事件当日の時系列（幕1）／訴訟の経過 2018→2019→2020（幕3）／2026の2件と 9/28 conference（ED） |
| `stat` | 6 | AE に載せない副次数値（about five hours・five years・1887・2 years gone・fourteen words・November 2024） |
| `ComparisonBars` | 3 | eminent domain（払う）vs police power（払わない）／保険が払う事由 vs 払わない事由／州憲法 vs 連邦憲法（Baker） |
| `QuoteCard` | 6 | ①「take as much of the building as needed without making the roof fall in」②「as unfair as it may seem…」③「The innocence of the property owner does not factor into the determination.」④ Sotomayor「an important question that divides the courts of appeals」⑤ Armstrong 1960 ⑥ 修正第5条の14語 |
| `MechanismReveal` | 2 | **police power と eminent domain の分岐**（幕3・EP40のドクトリン説明の主役） |
| `PinDropMap` | 2 | 幕4の5つの住所（Indiana / Texas / Tennessee / California / Nevada）／Aurora→Greenwood Village の位置関係 |
| **合計** | **28** | |

## 10.2 配置ルール

1. **AEの8区間（§9.2）と1秒でも重ならないこと。** `validate_lech_beats.py` が両方を突き合わせて検査する。
2. 幕あたりの配分: **幕1 = 6枠 / 幕2 = 5枠 / 幕3 = 8枠 / 幕4 = 7枠 / ED = 2枠**
3. **同じ kind を連続させない**。
4. 1枠の長さは **4.0–8.0秒**。28枠 × 平均5.5秒 = 154秒 = 全体の21.0%。
5. **幕3の説明区間（318.5–446.3秒）に `MechanismReveal` 2枠 + `QuoteCard` 3枠 + `timeline` 1枠を分散配置**し、20秒超の平坦区間をゼロにする（§3.4）。
6. `QuoteCard` の引用文は §0.4 の accuracy_lock 検査対象（`figures[].text` を対象パスに含める）。
7. **`QuoteCard` の引用は逐語のみ。要約を引用符に入れない。** ⑥（修正第5条）は "Nor shall private property be taken for public use, without just compensation." を1文字も変えずに出す。

## 10.3 密度の最終検算

```
AEヒーロービート        8
Remotion FigureBeats   28
〔CARD〕タイポ           6（§8。うち c03/c04/c05 は AE が描くので図版としては重複計上しない → +3）
------------------------
MGビート合計           36 枠（AE 8 + Remotion 28）

734.47秒 = 12.24分
下限 = 12.24 × 2.5 = 30.6 → ≥31枠
36 / 12.24 = 2.94 /分        ✓ ≥2.5/分
種類 = AE 5レイアウト + Remotion 7種 = 12種   ✓ ≥3種
```

---

# 11. オープニング（OP）設計 — 完全仕様

## 11.0 v2 row14 との関係 — 二重OPを作らない

v2 row14 は「本編内のOP/EDの正典は `remotion/src/components/Bookends.tsx`（`BrandOpening` / `BrandEndcard`）」と定め、fork/再実装を禁止している（invariant 14）。

- **本編（`Ep40Lech` コンポジション）のOPは `BrandOpening` を import したまま。変更しない。** `OPENING_SEC = 3.5` / `ENDCARD_SEC = 9` を変更しない。
- 本節で定義する `OpeningLech` は**独立したタイトルバンパー成果物**（`out/lech_opening.mp4`）。用途は (a) 再利用可能部品、(b) Shorts / 予告 / SNS 用の頭。
- **`OpeningLech` を本編に ffmpeg で焼き込んではならない**（オーナー承認なしに row14 の見え方を変えない）。

## 11.1 セクション0 — 環境・Remotion設定

### Composition 設定（`OpeningLech`）

| 項目 | 値 |
|---|---|
| `id` | **`OpeningLech`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60** |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `remotion/src/compositions/OpeningLech.tsx` |

### 本編 `Ep40Lech` の Composition 設定（★こちらが本編の正）

| 項目 | 値 |
|---|---|
| `id` | **`Ep40Lech`** |
| 解像度 | **1920 × 1080** |
| `fps` | **30** |
| `durationInFrames` | **22034**（= `Math.round(30 × 734.47)`） |
| data | `remotion/src/data/lech_film.json` |

### 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur
```

### `remotion.config.ts`（正典値・この通りにする）

```ts
import {Config} from '@remotion/cli/config';
import os from 'os';

Config.setVideoImageFormat('png');
Config.setConcurrency(os.cpus().length);       // 全コア
Config.setCodec('h264');                        // libx264。NVENC 禁止
Config.setCrf(16);                              // ≤17
Config.setX264Preset('slow');
Config.setPixelFormat('yuv420p');
Config.setColorSpace('bt709');
Config.setAudioCodec('aac');
Config.setAudioBitrate('320k');
Config.setChromiumOpenGlRenderer('angle');      // GPU=angle
```

> **NVENC 禁止**（VIDEO_RULES §7）。`crf 16 / preset slow / yuv420p / bt709 / aac 320k` をレンダーログで必ず確認する（row6）。

## 11.2 セクション1 — 秒数ベースのタイムライン（`OpeningLech` 全区間）

**fps = 60。以下の「フレーム」は全て `Math.round(fps * 秒)` で算出する。コード内にフレーム数を直書きしてはならない。**

| 秒 | フレーム | 起きること |
|---|---|---|
| **0.00–0.10** | f0–f6 | 画面は `#0d0b08`。**L1** グラデ背景の opacity が 0→1（0.40秒）、同時に scale 1.08 が180フレームかけて 1.00 へ（`Easing.out(Easing.cubic)`）。**opacity 単独ではなく scale と併用** |
| **0.10–0.15** | f6–f9 | **L6 ロゴ**（`hasLogo` true 時）が左上 `top:64 / left:72` に spring で出現。scale 0.4→1.0・opacity 0→1（**併用**） |
| **0.15–0.25** | f9–f15 | **L2** グリッドが spring（`damping:200, mass:1`, `durationInFrames = round(fps*0.8) = 48`）で reveal。最終 opacity = `gridReveal * 0.18`。同時にグリッド全体が180フレームで `translateY 0→48px`（`Easing.inOut(Easing.sin)`） |
| **0.25–0.30** | f15–f18 | **L3** グローが spring（`damping:18, mass:1.2`）で立ち上がる。scale 0.6→1.15 / opacity 0→0.85（**併用**）。サイズ `width*0.62 × height*0.36`、`filter: blur(28px)` |
| **0.30–0.86** | f18–f52 | **L4 主役タイトル**が1文字ずつ切れ上がる。各文字 spring（`damping:16, mass:1`）で `translateY 110% → 0`、opacity は `interpolate(springVal,[0,0.25],[0,1])`。**スタッガー = `Math.max(1, round(fps*0.04)) = 2フレーム/文字**。`title="LECH"`（4文字）なら最終文字の開始は f18+3×2 = **f24**、収束は約 f52。全体を `Trail`（`layers=6, lagInFrames=1.2, trailOpacity=0.45`）で包む |
| **0.55–1.15** | f33–f69 | **L2b フラクチャーライン**（EP40固有）。画面中央からタイトル背後を横切る亀裂状の線が `scaleX 0→1` + `opacity 0→0.55`（spring `damping:22, mass:1.1`、`transformOrigin:'center'`）。**破壊のモチーフ**。opacity 単独禁止のため scaleX と併用 |
| **0.95–1.35** | f57–f81 | **L5a** アクセント下線が左から `scaleX 0→1`（spring `damping:16, mass:0.8`、`transformOrigin:'left center'`）。幅 240px・高さ6px・`boxShadow: 0 0 24px #E5B53Aaa` |
| **1.10–1.55** | f66–f93 | **L5b** サブタイトルが `translateY 24px→0` + opacity 0→1（spring `damping:20, mass:1`・**併用**） |
| **1.55–2.20** | f93–f132 | 全要素が settle。背景 scale は 1.02 付近を緩やかに進行中（`Easing.out(Easing.cubic)` の減速域）。グリッドのドリフトも継続。**完全な静止フレームが1枚も無いこと** |
| **2.20–3.00** | f132–f180 | ホールド。背景 scale が 1.00 に着地、グリッド translateY が 48px に着地。**フェードアウトはしない** |

## 11.3 セクション2 — イージング・ディレイ・移動量・damping（数値表）

```ts
const T = {
  bgIn:        0.00,
  logoIn:      0.10,
  gridIn:      0.15,
  glowIn:      0.25,
  titleIn:     0.30,
  charStagger: 0.04,   // 60fps で 2フレーム
  fractureIn:  0.55,
  accentIn:    0.95,
  subIn:       1.10,
} as const;

const sec = (fps: number, s: number) => Math.round(fps * s);
export const openingLechDurationInFrames = (fps: number) => Math.round(fps * 3.0);  // = 180 @60fps
```

| 要素 | 開始 | 終了 | 手法 | 移動量 / 変化量 | イージング・パラメータ |
|---|---|---|---|---|---|
| 背景 scale | f0 | f180 | `interpolate` | **1.08 → 1.00** | `Easing.out(Easing.cubic)`・両端 clamp |
| 背景 opacity | f0 | f24 | `interpolate` | 0 → 1 | clamp（**scale と併用**） |
| グリッド translateY | f0 | f180 | `interpolate` | **0 → 48px** | `Easing.inOut(Easing.sin)` |
| グリッド reveal | f9 | f57 | `spring` | opacity 0 → **0.18** | `{damping: 200, mass: 1, durationInFrames: sec(fps,0.8)=48}` |
| グロー scale | f15 | — | `spring` | **0.6 → 1.15** | `{damping: 18, mass: 1.2}` |
| グロー opacity | f15 | — | 同 spring | 0 → **0.85** | 同上（**scale と併用**） |
| タイトル各文字 translateY | f18 + i×2 | — | `spring` | **110% → 0** | `{damping: 16, mass: 1}` |
| タイトル各文字 opacity | 同上 | — | `interpolate(springVal,[0,0.25],[0,1])` | 0 → 1 | clamp（**translateY と併用**） |
| タイトル Trail | 全域 | — | `@remotion/motion-blur` | — | `layers={6} lagInFrames={1.2} trailOpacity={0.45}` |
| フラクチャー scaleX | f33 | — | `spring` | **0 → 1** | `{damping: 22, mass: 1.1}`・`transformOrigin:'center'` |
| フラクチャー opacity | f33 | — | 同 spring | 0 → **0.55** | 同上（**scaleX と併用**） |
| アクセント下線 scaleX | f57 | — | `spring` | **0 → 1** | `{damping: 16, mass: 0.8}`・`transformOrigin:'left center'` |
| サブタイトル translateY | f66 | — | `spring` | **24px → 0** | `{damping: 20, mass: 1}` |
| サブタイトル opacity | f66 | — | 同 spring | 0 → 1 | 同上（**translateY と併用**） |
| ロゴ scale | f6 | — | `spring` | **0.4 → 1.0** | `{damping: 14, mass: 0.9}` |
| ロゴ opacity | f6 | — | 同 spring | 0 → 1 | 同上（**scale と併用**） |

> **等速線形は1箇所も使わない。** すべて `spring` か `Easing.out(Easing.cubic)` / `Easing.inOut(Easing.sin)`。
> **opacity 単独の演出は1箇所も無い。** 全ての opacity が translateY / scale / scaleX と対になっている。

## 11.4 セクション3 — レイヤー構成（下 → 上）

| L | 名前 | EP40 の値 |
|---|---|---|
| **L0** | ルート背景 | `backgroundColor: '#0d0b08'` |
| **L1** | **グラデ背景** | `radial-gradient(120% 120% at 50% 35%, #3a2f1c 0%, #1c1710 45%, #0d0b08 100%)` |
| **L2** | **グリッド/ライン** | `repeating-linear-gradient(0deg / 90deg, ${accent}22 0px 1px, transparent 1px 64px)`、`maskImage: radial-gradient(120% 90% at 50% 45%, black 35%, transparent 80%)` |
| **L2b** | **フラクチャーライン** | 幅 `width*0.78` / 高さ 3px / `background: linear-gradient(90deg, transparent 0%, ${accent}00 8%, ${accent}cc 34%, ${accent}55 52%, ${accent}cc 71%, ${accent}00 92%, transparent 100%)` / `transform: translateY(-6px) scaleX(...)` |
| **L3** | **グロー** | `width*0.62 × height*0.36`、`radial-gradient(closest-side, ${accent}88 0%, ${accent}22 45%, transparent 75%)`、`filter: blur(28px)` |
| **L4** | **主役タイトル** | `Trail` で包んだ文字スタッガー。各文字は `overflow:hidden` の span + 内側 span を `translateY`。`fontWeight: 800` / `fontSize: 150` / `letterSpacing: -2` / `color: '#ffffff'` / `lineHeight: 1.05` / 外側 `translateY(-70px)` / 各 span に `paddingBottom: '0.12em'` |
| **L5** | **アクセント下線 + サブタイトル** | 縦並び（`flexDirection:'column'`, `gap:18`）、`translateY(55px)`。下線 240×6・`borderRadius:3`。サブタイトル `fontWeight:500` / `fontSize:38` / `letterSpacing:6` / `textTransform:'uppercase'` / `color:'#c8d2e6'` |
| **L6** | **ロゴ**（`hasLogo` 時） | `top:64 / left:72 / 84×84 / borderRadius:20`、`background: linear-gradient(135deg, ${accent}, #ffffff22)`、`border: 2px solid ${accent}`、`boxShadow: 0 0 30px ${accent}66` |

> **主役（L4）の裏に最低3レイヤー**という要件: L1 / L2 / L2b / L3 = **4レイヤー**で満たす。

## 11.5 セクション4 — props 定義と型

```ts
export type OpeningLechProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる。推奨 3–8文字（fontSize 150 前提）
  subtitle: string;   // サブタイトル。UPPERCASE 表示
  accent: string;     // アクセントカラー（HEX 6桁・"#" 込み）。グリッド/フラクチャー/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true のとき左上にロゴバッジを出す
};
```

**EP40 の確定 props（`remotion/props/lech.json`）:**
```json
{ "title": "LECH", "subtitle": "POLICE POWER", "accent": "#E5B53A", "hasLogo": true }
```

> `subtitle` は §0.4 の accuracy_lock 検査対象（`remotion/props/lech*.json` を対象パスに追加する）。
> **EP39 は `#1F6BFF` を使う。`props/` 配下でファイルを分けるので衝突しない。**

## 11.6 セクション5 — 確認方法と量産レンダリング

**プレビュー:**
```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio
```
→ composition `OpeningLech` を選び、0→180 フレームでスクラブして §11.2 の各時刻に指定の動きが起きていることを目視確認する。

**単体レンダリング:**
```bash
npx remotion render OpeningLech out/lech_opening.mp4 --props=./props/lech.json
```

**props 差し替えによる量産:**
```bash
npx remotion render OpeningLech out/lech_opening.mp4  --props=./props/lech.json
npx remotion render OpeningLech out/lech_short_op.mp4 --props=./props/lech_short.json
npx remotion render OpeningLech out/lech_teaser.mp4   --props=./props/lech_teaser.json
```

**`remotion/props/lech_short.json`:**
```json
{ "title": "LECH", "subtitle": "THE TENTH CIRCUIT", "accent": "#E5B53A", "hasLogo": false }
```

**本編のレンダリング:**
```bash
npx remotion render Ep40Lech out/lech_final.mp4 --props=./src/data/lech_film.json
```

---

# 12. パッケージング（row11/12/13）

## 12.1 タイトル A/B（≤60字・二人称必須・「最高裁」を含まない）

| variant | 文字列 | 字数 |
|---|---|---|
| **A** | `Can Police Destroy Your House And Pay You Nothing?` | **49** |
| **B** | `Police Can Destroy Your Home. You Pay To Rebuild It.` | **51** |

> A は house rules §1 の勝ちパターン「◯◯は、あなたに △△ できるのか？」に完全一致。B は断定形で CTR の A/B 比較用。
> 両案とも §0.4 R1 を通る（`Supreme Court` を含まない）。

## 12.2 サムネイル3案（実測CTR 2.31% → 目標4%）

**共通要件:**
- Remotion `<Still>` で **1280×720** PNG レンダ。`remotion/src/compositions/LechThumbnails.tsx` に3案を実装し Root.tsx に3 Still 登録
- 見出しは**全て大文字・4語以内**・**320px で判読可能**
- **実在人物の肖像を使わない**（§5.5）
- **「最高裁 / Supreme Court / SCOTUS」を書かない**（§0.4 R1）
- `thumbnail_visibility` ゲート: **選択サムネの luma 平均 ≥33** ＋ コントラスト下限
  → **EP40 は昼のシーンなので luma は余裕がある。むしろ白飛びに注意**し、ハイライトを **245以下**に抑える
- 3枚レンダ後、**T1 を `selected` にする**（`09_package/thumbnail_selected.png`）

### T1 — 「穴の空いた家」（★selected・情報量最小）

| 項目 | 内容 |
|---|---|
| 背景素材 | **S09**（穴の空いた家・屋根は無傷）のバリエーションから、穴が中心に来るもの |
| 構図 | 家は**画面の右 60%**。左 40% に文字。最大の穴が画面のほぼ中心 |
| 文字 | **`YOUR HOUSE. THEIR CALL.`**（**4語**） |
| 文字スタイル | Impact系・白 `#F5F7FA`・文字高 = 画面高の **19%**・下端に `#E5B53A` の 8px 下線 |
| 色/コントラスト | 昼光の白 + コンクリート灰 + **穴の中の黒**（最大コントラスト点）+ 金の下線1本のみ |
| 狙い | 「家に穴」＝説明不要の異常。二人称 "YOUR" で自分事化。**勝っている「警察はあなたに何ができるか」型の視覚版** |

### T2 — 「$5,000 FOR THIS」（数字勝負）

| 項目 | 内容 |
|---|---|
| 背景素材 | **S09 または S12**（子どもの部屋が空に開いている）。輝度を 55% まで落とす |
| 構図 | 上 2/3 に破壊、下 1/3 に数字。`$5,000` を Impact系で画面幅の 62% |
| 文字 | **`$5,000 FOR THIS`**（**3語**） |
| 文字スタイル | `$5,000` を金 `#E5B53A`・`FOR THIS` を白。**最も明るい点が数字**になるようにする |
| 事実性 | **$5,000 は §0.5 N04 の確定値**（第10巡回区の記録・一家の上告申立書に記載）。`FOR THIS` は評価語ではなく指示語なので帰属違反にならない |
| 狙い | 桁の落差を1秒で。**幕2冒頭 181秒で回収される**（§3.3 P6） |

### T3 — 「WRONG ADDRESS. YOUR BILL.」（射程の恐怖）

| 項目 | 内容 |
|---|---|
| 背景素材 | **S18**（Indiana・割れた窓と催涙弾の跡）または S02 と S09 の左右分割 |
| 構図 | 中央に細い金の縦線。左＝無傷のふつうの家、右＝破壊された家。**同じアングル・同じ光** |
| 文字 | **`WRONG ADDRESS. YOUR BILL.`**（**4語**） |
| 文字スタイル | Impact系・白・`YOUR BILL.` だけ金 `#E5B53A`。文字は画面上部 |
| 色/コントラスト | 昼だが沈んだ露出。金は2語のみ |
| 狙い | 「落ち度ゼロでも来る」という射程の恐怖。**T1 が効かなかった場合の差し替え第1候補** |

## 12.3 概要欄（1行目 = 問い）

```
If the police destroy your house to catch someone who has nothing to do with you, who pays to rebuild it?

Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019), cert. denied (2020).
The Supreme Court has never decided the underlying question. Two petitions raising it — Hadley (25-1158) and Pena (25-1163) — were distributed for conference on September 28 and are still pending.

Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.
```
> **判例引用の完全一致行はここに置く**（§0.4 で本文からは外し、package 側の要件に移した）。
> `check_lech_accuracy.py` の R4 は `09_package/description.txt` に対して
> `Lech v\. Jackson, 791 F\. App'x 711 \(10th Cir\. 2019\)` の完全一致行を**最低1つ**要求する。

## 12.4 固定コメント（オーナーが公開時に投稿）

`episodes/PD-2026-040-lech/09_package/pinned_comment.v002.txt`:

```
Two things this case turns on, and neither is obvious:

(1) The Tenth Circuit held this was an exercise of police power, not a taking — so the Takings Clause never kicks in. That ruling came in an Order and Judgment the court itself labeled "not binding precedent."

(2) The Supreme Court declined to hear the appeal in 2020. That is not agreement. It just means the Tenth Circuit's decision stands.

Two petitions raising the same question, Hadley and Pena, go to conference on September 28. Nobody knows how they end.

If it were your house — should the city pay, or should you?
```

> この文面も §0.4 の accuracy_lock 検査対象（`09_package/*.txt` を対象パスに含める）。

## 12.5 連動 Short（日次・縦9:16・35–45秒）

| 項目 | 確定値 |
|---|---|
| 解像度 / fps | **1080×1920 / 30fps** |
| 尺 | **38秒**（35–45秒の範囲内） |
| 内容 | 同じ問いの30秒版。HOOK の48語 + 「19時間」+ 「$5,000」+ 「Nothing owed」の4ビートのみ |
| **CTA** | **1つだけ = 「続きは本編で」**。登録の直請けはしない |
| 固定コメント | 問いを1つだけ: `If it were your house — should the city pay, or should you?` |
| 概要欄1行目 | 本編パーマリンク |
| 素材 | **本編で使う画から流用**（Shorts 専用に新規生成しない）。ただし本編のカット再利用は `check_asset_reuse` の対象外（別ファイル） |

---

# 13. 工程分担 — Codex単体で可能な範囲 / Claude別工程

## 13.1 Codex が単体で実装できる範囲（★台本は確定済みなので全て着手可能）

| # | 作業 | 成果物 | 依存 |
|---|---|---|---|
| **C1** | エピソードディレクトリ生成 | `episodes/PD-2026-040-lech/{00_topic,01_research,03_script,04_scenes,05_stock,05_visuals,06_audio,08_edit,09_package,approvals,events}` + `manifest.json`（**`target_duration_minutes: 12`** / `duration_profile: "standard"`） | なし |
| **C2** | 確定台本の本番配置 | `03_script/script.en.v002.md`（§0.2 のファイルを**1バイトも変えずにコピー**） | なし |
| **C3** | **`accuracy_lock` ゲート実装** | `scripts/check_lech_accuracy.py`（§0.4 R1–R8） | C2 |
| **C4** | **スロット契約 + バリデータ** | `scripts/validate_lech_slots.py` / `03_script/lech_slots.v002.json` | §0.5 / §3.1 |
| **C5** | **画像生成 150枚**（§5.7 S01–S25 × 6） | `H:\pd-media\assets\ai\lech\*.png`（長辺 ≥3840）+ `05_stock/stock_ledger.v002.json` | **オーナーGO後**（§13.4） |
| **C6** | factory 素材の選定 **70本** | `05_stock/factory_selection.v002.json`（EP39 と sha256 重複除外・`search_keywords` 記録） | なし |
| **C7** | **shotlist 224 span** | `04_scenes/shotlist.v002.json`（全 span に asset_type / motion / transition in-out / factory `search_keywords` / caption span。「等」「など」禁止） | C2, C6 |
| **C8** | **scene_plan** | `04_scenes/scene_plan.v002.json`（§5.8 の8フィールドを全ビート） | C2, C7 |
| **C9** | **`CardTypo` 実装**（§8・6枚） | `remotion/src/components/CardTypo.tsx` | なし |
| **C10** | **`figures[]` 28枠**（§10） | `remotion/src/data/lech_film.json` の `figures[]` | C2 |
| **C11** | **本編コンポジション** | `remotion/src/compositions/Ep40Lech.tsx`（`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を **import**。fork 禁止） | C7, C9, C10 |
| **C12** | **OP実装**（§11 全仕様） | `remotion/src/compositions/OpeningLech.tsx` + `remotion/props/lech.json` + Root.tsx 登録 + `out/lech_opening.mp4` | なし |
| **C13** | **サムネ実装 3案**（§12.2） | `remotion/src/compositions/LechThumbnails.tsx` + Root.tsx に3 Still 登録 + `09_package/thumb_{1,2,3}.png` + `thumbnail_selected.png` | C5 |
| **C14** | **AEビルダ実装** | `scripts/ae/build_lech_hero_jsx.py`（5レイアウト・3カウント型・§9.8 の罠13件すべて対処） | §9 |
| **C15** | **AEコンポジタ実装** | `scripts/ae/composite_lech_hero.py`（SKIP 4条件） | §9.7 |
| **C16** | **beats バリデータ** | `scripts/validate_lech_beats.py`（§9.3 の不変条件7件・`figures[]` との衝突検査を含む） | C10, C14 |
| **C17** | **VO速度検証ツール** | `scripts/measure_vo_wpm.py`（§0.3・合格帯 168.0–190.0 wpm） | なし |
| **C18** | **stub 通しドライラン** | `episodes/PD-2026-040-lech/08_edit/_dryrun/` に AE 8ビート + コンポジット結果 | C14–C16 |
| **C19** | パッケージ生成 | `09_package/description.txt` / `pinned_comment.v002.txt` / `title_candidates.json` | §12 |

**→ C1–C4, C6–C19 は課金なしで完結する。** C5（画像生成）のみオーナーGOを待つ。

## 13.2 Claude 別工程（DSP / ゲート）

| # | 作業 | 備考 |
|---|---|---|
| **D1** | ナレーション生成（ElevenLabs `nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2` / stability 0.35 / similarity_boost 0.80 / style 0 / speaker_boost on / **speed 1.0 明示**） | **有料。オーナー承認済みの範囲でのみ実行。本設計フェーズでは起動しない** |
| **D2** | **VO速度検証**（`measure_vo_wpm.py`・168–190 wpm） | 範囲外なら破棄・再発注（BLOCKING・§0.3） |
| **D3** | 強制アラインメント字幕（faster-whisper 語タイム・ズレ ≤120ms） | `caption_narration_match` ≥99% / `.srt` カバー率 ≥95% |
| **D4** | **4層ミックス**（ナレ / BGM / SFX / 環境音・ダッキング -22 LUFS フロア・統合 -14 LUFS） | §4。**[SOUND] 指定区間をデジタル無音にしない**（§3.5 の罠） |
| **D5** | 全ゲート実行 | `motion_density` / `animation_mix` / `caption_integrity` / `visual_asset_qc` / `footage_diversity` / `check_asset_reuse` / `accuracy_lock` |
| **D6** | 最終受入 | `check_final_acceptance.py 40 --render <final> --emit-receipt` → exit 0 |
| **D7** | アップロード / 予約 | **オーナー操作のみ**。receipt（`video_sha256` 一致）が無い限り不可 |

## 13.3 唯一の停止点

制作はノンストップで**YouTubeアップロード直前まで**進める（ナレ課金・ラフカット・タイトル/サムネの中間ゲートでは止まらない）。
**唯一の停止点 = アップロード直前のオーナー確認。**

**即時停止する例外（この3つだけ）:**
1. 台本/claims に重大な事実誤り — 特に **「最高裁が判断した」と書かれた場合**、および **係属中2件（25-1158 / 25-1163）の結果を断定した場合**
2. 権利・実在人物の肖像リスクの発見（特に9歳男児・15歳の子の特定可能な描写）
3. R3 相当への逸脱（Seacat を主題化した／動機・精神状態に踏み込んだ）

## 13.4 本フェーズの禁止事項

- **有料プロバイダジョブを一切起動しない**（画像生成の課金API・TTS・アップロード）。§13.1 C5 の画像生成は**オーナーが明示的にGOを出した後**に実行する。設計段階は**プロンプトの確定まで**。
- 公開済み mp4 を再レンダリング/上書きしない。
- **EP39 のファイルに触れない。**
- 台本本文を改変しない（§0.2）。

---

# 14. 受入基準（EP40 の Definition of Done）

**ゲートは以下の順で走らせる。★語数ゲートが最初** — TTS とレンダーに課金する前に落とすため。

```bash
cd C:\Users\aab15\Documents\prime-documentary

# 0. ★語数ゲート（最優先。課金の前に必ずここで止める）
./.venv/Scripts/python.exe scripts/check_script_length.py \
  episodes/PD-2026-040-lech/03_script/script.en.v002.md --json
#    → 2,048–2,226語の外なら exit != 0。確定台本は 2,153語で PASS 済み

# 1. 水増しゲート
./.venv/Scripts/python.exe scripts/check_padding.py --ep lech --json

# 2. 事実性ゲート（EP40固有・§0.4）
./.venv/Scripts/python.exe scripts/check_lech_accuracy.py --json

# 3. スロット / ビート契約
./.venv/Scripts/python.exe scripts/validate_lech_slots.py
./.venv/Scripts/python.exe scripts/validate_lech_beats.py

# 4. ★VO速度検証（ナレ生成直後・ミックス前）
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep lech --json
#    → 168.0–190.0 wpm の外なら音声を破棄して再発注

# 5. レンダ前プリフライト
./.venv/Scripts/python.exe scripts/preflight_render_gate.py --ep lech

# 6. 本編の最終受入（v2 の全ハードゲート）
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 40 \
  --render episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v003_ae.mp4 --emit-receipt
```

**全て exit 0 でなければ `package_ready` にしない。自己申告のQCは無効。**

| ゲート（row） | 閾値 | **EP40 の設計値** |
|---|---|---|
| `check_script_length`（★最優先） | 2,048–2,226語 | **2,153語 PASS 済み** |
| `check_padding` | violation 0 | 幕内部に2秒超の間を作らない（沈黙は全て台本指定位置のみ） |
| `runtime_band`（row6） | 690–750秒（standard） | **734.47秒 = 12:14.5** |
| `loudness`（row6） | -16〜-12 LUFS | **-14.0 LUFS** / true peak ≤ -1.0 dBTP |
| レンダー設定（row6） | crf≤17 / preset slow / yuv420p / bt709 / aac 320k / NVENC禁止 | **crf 16 / slow / yuv420p / bt709 / aac 320k / libx264** |
| `voice_is_master`（row2） | 指定 voice/model/params | **§0.3 の表 + speed 1.0 明示 + 実測 168–190 wpm** |
| `bgm_present`（row1） | 無音 >25秒 の区間ゼロ | 最長無音 **3.0秒** / BGMベッド -22 LUFS フロア |
| `structure_4part`（row9/10） | 4役割が順に存在・hook はヘッド6–10秒・CTA は末尾30秒以内 | **HOOK 0.00開始 / CTA 719.4–725.5（末尾から9.0–15.1秒）** |
| promise-payoff（row9/13） | フックの reveal が本編後半に出現 | **§3.3 の P1–P6 全て対応済み** |
| retention map（row16） | 再フック ≤3分間隔・平坦区間 20秒超ゼロ | **最大間隔 1:41** / §3.4 R1–R8 |
| `animation_density`（row8） | ゼロモーション0 / 準静止 ≤10% / 単一ホールド ≤3秒 / ハードカット0 / 平均ショット ≤6秒 | **準静止 ≤6% / 最長ホールド 2.0秒 / ハードカット 1箇所（台本指定・理由明記）/ 平均 3.22秒** |
| MGビート密度 | ≥2.5/分 かつ 種類3以上 | **36枠 / 2.94per分 / 12種** |
| `footage_diversity`（row7） | distinct/total ≥0.40 / 再利用 ≤4回 / 汎用シンボル ≤2回 / 30秒に1本のfactory / 空span 0 | **0.746 / 最大2回 / 汎用シンボル 0回 / factory 70本（10.5秒に1本）/ 空span 0** |
| `check_asset_reuse` | first-use share ≥0.70 / factory 1回 / i2v ≤2回 / 静止画 ≤2回 | **0.746 / factory 1回 / i2v 2回 / 静止画 2回** |
| 静止画占有率 | ≤45% | **32.9%** |
| `image_resolution`（row5） | 長辺 ≥3840px / NEG違反0 | 全150枚 ≥3840 |
| `caption_integrity`（row3/4） | 一致 ≥99% / カバー ≥95% / ≤2行42字 / 1.0–6.0秒 / ≤17cps / ズレ ≤120ms | §7.3 |
| `thumbnail_present`/`visibility`（row11/12） | ≥3枚 1280×720 + selected / 見出し ≤4語 / luma ≥33 | **3案 + T1 selected / 4語・3語・4語 / 昼景で luma 余裕（ハイライト ≤245）** |
| packaging QC（row13） | タイトル ≤60字・A/B 2案 | **A 49字 / B 51字** |
| `op_ed_bookends`（row14） | `BrandOpening`/`BrandEndcard` を import・`OPENING_SEC=3.5`/`ENDCARD_SEC=9` 不変 | ✓ import。`OpeningLech` は本編に焼き込まない（§11.0） |
| **`accuracy_lock`（EP40固有）** | violations = 0 | §0.4 R1–R8 |

---

# 15. premortem（この設計が失敗するとしたらここ）

| # | 失敗モード | 予兆 | 事前対処 |
|---|---|---|---|
| 1 | **fast端でVOが速く、9分台に落ちる** | `measure_vo_wpm` が 190 超 | §0.3。**speed 1.0 明示 + 生成直後の実測**。190超は破棄・0.95で再発注。**ミックス後に気づくと全工程やり直し** |
| 2 | **[SOUND] 指定をデジタル無音で実装し `bgm_present` が落ちる** | 交渉5時間区間・突入区間 | §3.5 の罠。拡声器ベッド / 低域ランブルを必ず残す |
| 3 | **v001 の b03/b07（万引き額・補償率）を実装してしまう** | beats.json に台帳外の数字 | §0.4 R6（`num_id` が §0.5 の表に無ければ exit 1）。**機械で止まる** |
| 4 | **旧 accuracy_lock R2 が確定台本を誤検知して FAIL** | "He asked the Supreme Court to take the case." | §0.4 R2 を**2文窓**に変更済み。実装時に1文窓に戻さない |
| 5 | **first-use share 0.70 を割る** | 静止画を3回以上使い回す | §5.1 の配分（factory 70 / i2v 18 / 静止画 79）を shotlist 生成時に**機械で割り当てる**。手で並べない |
| 6 | **AE の em-dash 豆腐** | b04 の `—` | §9.8 罠13。ASCII ハイフンに置換済み |
| 7 | **9歳男児の描写が特定可能になる** | 画像に子どもの顔・服装の細部 | §0.4 R8 + §5.4 ネガティブ `child face`。**生成後に全150枚を目視確認**（EP38 retro「filenameを信じるな」） |
| 8 | **係属中2件の結果を断定してしまう**（Shorts / 概要欄 / 固定コメントで起きやすい） | 「最高裁がついに判断」等 | §0.4 R4。`09_package/*` と Shorts の台本も検査対象に含める |
| 9 | **`figures[]` 28枠が AE の8区間と重なる** | 二重描画 | §9.3 不変条件7。`validate_lech_beats.py` が両方を突き合わせる |
| 10 | **EP39 と素材が被る** | sha256 重複 | §2 + C6 で生成/選定前に EP39 の stock_ledger を読む |

---

# 16. Codex 引き継ぎプロンプト（★このブロックをそのまま Codex に貼る）

```
あなたは Prime Documentary EP40 の実装担当です。

【唯一の設計書】
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md
これを全文読んでから着手すること。同ディレクトリの v001 は破棄済みで、事実面で v002 と衝突する。
v001 を読んで実装してはならない。

【確定台本（1バイトも変えない）】
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP40_lech_script.en.v001.md
語順・短縮形・句読点の整形も禁止。em-dash 0本 / 短縮形23箇所 / セミコロン0 は意図的な改稿結果。

【満たすべき受入 row】
row 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16

【verify コマンド（最後の壁。自己申告のQCは無効）】
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 40 --json

【絶対条件（違反したら他が完璧でも出荷不可）】
1. Lech v. Jackson は最高裁判決ではない。判断したのは第10巡回区（2019）。最高裁は2020年に
   上告を受理しなかっただけで、本案を判断していない。
2. Hadley (25-1158) と Pena (25-1163) は係属中。結果の断定・予測を一切書かない。
3. 限定免責 / qualified immunity に一切言及しない（争点外）。
4. 実在人物の肖像・実映像・ディープフェイクを作らない/使わない。サムネにも使わない。
   9歳男児と15歳の子は完全な象徴表現のみ（逆光シルエット・輪郭のみ・顔なし）。名前を書かない。
5. 設計書 §0.5 の確定数値表に無い数字を画面に出さない（万引き額・補償率・発射数・再建費は禁止）。
6. AI画像は毎回 "AI-assisted visualization" を画面表示する。
7. 有料ジョブ（画像生成API・TTS・アップロード）はオーナーGOが出るまで起動しない。
8. EP39 のファイルに触れない。公開済み mp4 を上書きしない。

【今すぐ着手する順序】
設計書 §13.1 の C1→C2→C3→C4→C6→C7→C8→C9→C10→C11→C12→C13→C14→C15→C16→C17→C18→C19。
C5（画像生成150枚）だけはオーナーGOを待つ。プロンプトは §5.7 で確定済み。

【止まってよい唯一の点】
アップロード直前のオーナー確認。それ以外は止まらずに進める。
ただし次の3つは即時停止:
 (a) 「最高裁が判断した」と書かれた／係属中2件の結果を断定した
 (b) 実在人物の肖像リスク（特に未成年の特定可能な描写）
 (c) Seacat を主題化した／動機・精神状態に踏み込んだ

【解釈の余地について】
設計書に数値が書いてある箇所は、その数値を使うこと。「だいたい」「良い感じに」で決めない。
設計書に無い判断が必要になったら、実装を止めて質問すること。推測で埋めない。
```
