# AUDIT — EP39 / EP40 台本監査（レンズ: 台本）

- 監査日: 2026-07-20
- 対象: `EP39_frazier_script.en.v001.md` / `EP40_lech_script.en.v001.md`
- 参照正典: `EP39_frazier_DESIGN_and_CODEX_PROMPTS.v002.md` / `EP40_lech_DESIGN_and_CODEX_PROMPTS.v002.md`
- 方針: 実機確認のみ。**ファイルは一切修正していない。**

---

## 0. 結論サマリ

| 区分 | 件数 |
|---|---|
| **BLOCKER** | **7** |
| HIGH（要判断・BLOCKER未満） | 10 |
| MEDIUM / 観察 | 7 |
| 一次資料で裏が取れなかった項目 | **22** |

**BLOCKER 7件の内訳**

| # | 話 | 箇所 | 種別 | 検証者 |
|---|---|---|---|---|
| B-1 | EP39 | L58 `That the victim had been wearing only a bra.` | 被害者の性的暴行描写が象徴の範囲を超える | 私 |
| B-2 | EP40 | L105 Takings Clause の引用文言 | **一次資料と不一致（誤引用）** | 私（原本PDF） |
| B-3 | EP40 | L45 `the one that wasn't locked` | **一次資料と不一致** | 私（原本PDF） |
| B-4 | EP40 | v002 §3.1 幕2 語数 413 vs 台本 409 | 設計書との食い違い | 私（実測） |
| **B-5** | EP39 | L72 `a young sailor named Martin Frazier` | **一次資料と不一致。Frazier は海兵隊員（Marine）** | 私（LII原文） |
| **B-6** | EP39 | L26 / L50 `garden` / `vegetable garden` | **一次資料と不一致。Innocence Project は `yard`。オチの語を含む** | 私（IP原文） |
| **B-7** | EP39 | L132 `Both took effect on January 1, 2022` | **Oregon SB418 の施行日が誤り**（成立法に緊急条項なし→2021-09-25 と推定） | 検証エージェントのみ |

**指示された絶対条件の判定**

- **EP40 §2（最高裁の判示と書いていないか）: PASS / BLOCKER 0件。**
- **EP39 §3（Speelman / 被害者描写 / 肖像 / §1983帰属）: BLOCKER 1件（被害者描写のみ）。** Speelman・肖像・§1983帰属は PASS。

---

## 1. EP40 の絶対条件（§2）— PASS・BLOCKER 0件

`Supreme Court` の出現は本文中 **4箇所**。v002 §0.4 の `accuracy_lock` R1–R8 のロジックを**自分で実行**して全件検証した。

```
=== R2: 'Supreme Court' sentences, 2-sentence window ===
  [1] PASS via petition
      That figure appears in the family's own petition to the Supreme Court, described in those words, as help with temporary living expenses.
  [2] PASS via it declined
      He asked the Supreme Court to take the case. On June 29, 2020, it declined.
  [3] PASS via declined to hear
      In November 2024, when the Supreme Court declined to hear Vicki Baker's case, Justice Sotomayor wrote a statement respecting that denial, joined by Justice Gorsuch.
  [4] PASS via declined to hear
      In May 2026, ... six years after the Supreme Court declined to hear him, Leo Lech signed his name to a brief in someone else's case.
  count=4 (v002 expects 4)

=== R3: affirmative verb within 60 chars after 'Supreme Court' ===
  violations=0
=== also: any 'the Court' + affirmative verb (broader than R3) ===
  (0件)
=== R4 === prediction violations=0 | 'pending'=True | 'Nobody knows how they end'=True
=== R6 === Tenth Circuit x3 (>=2) | district court x2 (>=1)
=== R7 === banned=0
  required 'Nobody in this story did the wrong thing that day.' -> True
  required 'Nobody disputes the police acted lawfully.' -> True
=== R8 === hits=0
```

4箇所すべて「上告を受理しなかった／申立て」の文脈であり、「判断した」に相当する記述は**ゼロ**。R3 に加えて `the Court` + 肯定動詞という**より広い自作パターン**でも0件。判示の主体は L99 で `the Tenth Circuit affirmed`、L95 で `a federal district court in Colorado ruled` と正しく分離されている。

さらに **私自身が第10巡回区の原本 PDF を読んで確認した**（下記 §3）。最高裁が本案を判断していないことは台本の記述と一致する。

### ★ ただし gate は現在フォールス・グリーン（重要）

```
$ python scripts/check_lech_accuracy.py
PASS lech_accuracy: 0 violation(s), 3 skipped pattern(s)

$ python scripts/check_lech_accuracy.py --json
  "skipped": [
    "episodes/PD-2026-040-lech/03_script/lech_slots.v*.json",
    "episodes/PD-2026-040-lech/03_script/script.en.v*.md",   ← 台本本体
    "episodes/PD-2026-040-lech/08_edit/ae_hero/beats.json"
  ]
```

`check_lech_accuracy.py` は **PASS を返すが、台本を一度も読んでいない。** `TARGETS` は `episodes/PD-2026-040-lech/03_script/script.en.v*.md` を見に行くが、台本は現在 `episodes/_planning/` にあるため glob が空振りし、`skipped` に落ちて素通りする。`TARGETS` に `_planning/` 配下は含まれていない。

つまり **EP40 の最重要ゲートは「対象ゼロで合格」している**。台本を正規パスへ配置するまで、この PASS は何も保証しない。（今回の R1–R8 判定は私が手動でロジックを再実行した結果であり、gate の出力ではない。）

### ★ R5 が自分自身の指示文で落ちる罠

```
$ sed -n '7p' EP40_lech_script.en.v001.md
- 限定免責は本件の争点ではないため一切言及しない。
```

R5 の `BANNED_QI = r"qualified immunit|限定免責|Harlow v\.|Pierson v\."` はファイル全体を走査する。台本ヘッダ L7 の**日本語の禁止指示そのもの**が `限定免責` に一致するため、この台本をそのまま `script.en.v002.md` へコピーすると **R5 が即 FAIL する**。ナレーション本文中の実出現は0件。ヘッダを外して配置するか、R5 をナレ本文限定にする必要がある。

---

## 2. EP39 の絶対条件（§3）

### 2.1 Christopher Speelman — PASS（BLOCKER 0件）

本文中の言及は2箇所のみ。いずれも**裁判記録・公的発表の事実に限定**されており、推測・動機付け・人物描写は無い。

- L110: `On July 14, 2021, Adams County District Attorney Brian Sinnett announced that Christopher Speelman's DNA was, in his words, an absolute match to the crime scene evidence.`
  → 地方検事の公表として帰属（`announced` / `in his words`）。断定していない。**適合。**
- L112: `On June 22, 2023, Chris Joseph Larry Speelman, then fifty-nine, pleaded guilty to third-degree murder and burglary and no contest to rape. Judge Thomas Campbell sentenced him to twenty-five to fifty years, with no parole eligibility until 2046.`
  → 答弁・量刑という純粋な裁判記録事実。**適合。**

v002 §8.1 の逐語ロック文言とも一致。

### 2.2 被害者 Edna Laughman の描写 — **BLOCKER B-1**

演出指示側は完全に適合している（`人体は映さない` / `無人の台所` / `象徴のみ`、S07・S08・S18・S20 の画像プロンプトも `absolutely non-graphic` / `no people`）。**問題はナレーション本文。**

**B-1（BLOCKER）— L58**

```
That the victim had been wearing only a bra. That she had been sexually assaulted.
That the pills forced into her mouth were what killed her.
```

`wearing only a bra` は、性的暴行被害者の**着衣・身体状態そのものの描写**であり、「非グラフィック・象徴のみ」の条件を超える。他の2項目（暴行の事実／錠剤）は事件の法的骨格に必要だが、着衣状態は**物語上の強度のためだけに置かれており、機能的な必要が無い**。同じ論点（「非公開の細部を知っていた」）は着衣に触れずに完全に成立する。

なぜ BLOCKER か:
- v002 §8.1 の封じ込め条件は「描写は…象徴のみ／**身体**・被害・暴力の**再現**は全面禁止」。この条項は**映像のみを射程にしており、ナレーション本文を検査していない**。つまりゲートに穴がある状態で、本文だけがルールの外側に出ている。
- EP40 には `check_lech_accuracy.py` があるが、**EP39 には対応する `check_frazier_accuracy.py` が存在しない**（`ls scripts/ | grep frazier` → `build_frazier_film.py` / `build_frazier_thumbnails.py` / `make_frazier_stub_assets.py` のみ）。R2/R3隣接の封じ込めが**散文の約束のみで、実行可能なゲートが無い**。

最小修正（参考・私は修正していない）: 当該1文を削除するか、`That she had been found partly undressed.` 等に置換。前後の論理は無傷。

### 2.3 実在人物の肖像を想起させる演出指示 — PASS（0件）

全 `[ ]` 指示を確認。`無人` / `人体は映さない` / `人物は映さない` / `象徴のみ` で統一されており、肖像を想起させる指示は**ゼロ**。L15 のフラッシュフォワード（椅子・指紋カード・鉄扉・ラック）も全て無人。

### 2.4 §1983 の主張 vs 認定事実 — おおむね PASS（HIGH 1件）

中核部分の帰属は正確:

- L64: `His federal complaint says otherwise. It says the details came from the officers. That claim has never been tried.` → **訴状の主張であることを明示し、未審理であることまで書いている。模範的。**
- L60: `Officers testified that ...` → 証言として帰属。
- L108 OST: `SUMMARY JUDGMENT DENIED AUG 16, 2007 — NOT A VERDICT` → 中間判断であることを画面で明示。

**H-1（HIGH）— L106**

```
He sued the men who had taken them. A federal court held that a jury could hear it. No jury ever did.
```

`the men who had taken them`（them = 16年）は、**陪審が一度も判断していない責任・因果を、地の文で認定事実として断定している**。直後の `No jury ever did.` が救っているため BLOCKER には数えないが、L64 でせっかく確立した「主張であって認定ではない」という線を、地の文が自ら踏み越えている。`He sued the men he said had taken them.` 程度で解消する。

---

## 3. 事実の裏取り

### 3.1 私が一次資料で直接確認した項目（VERIFIED）

#### EP40 — 第10巡回区 原本 PDF を実際に読んで確認

`Lech v. Jackson`, No. 18-1051 (10th Cir. Oct. 29, 2019)、govinfo の原本 PDF（17頁）を取得し `pypdf` で全文抽出して照合した。

| 台本の記述 | 原本の文言 | 判定 |
|---|---|---|
| 判決文書は "Order and Judgment"、拘束力ある先例でない | `ORDER AND JUDGMENT*` / `* This order and judgment is not binding precedent, except under the doctrines of law of the case, res judicata, and collateral estoppel. But it may be cited for its persuasive value.` | **VERIFIED（逐語一致）** |
| 2019年10月29日／Holmes・McKay・Moritz／Moritz 執筆 | `October 29, 2019` / `Before HOLMES, McKAY, and MORITZ, Circuit Judges.` / `Entered for the Court  Nancy L. Moritz  Circuit Judge` | **VERIFIED** |
| 2015年6月3日・4219 South Alton Street | `On June 3, 2015` / `the home at 4219 South Alton Street in Greenwood Village, Colorado` | **VERIFIED** |
| Leo と Alfonsia が息子 John のために購入、John は恋人とその9歳の息子と居住 | `Leo and Alfonsia Lech purchased the home ... for their son, John Lech. ... John Lech lived at the home with his girlfriend and her nine-year-old son.` | **VERIFIED** |
| Robert Seacat・Aurora 警察から逃走中の武装被疑者 | `Robert Seacat, an armed criminal suspect who was attempting to evade capture by the Aurora Police Department` | **VERIFIED** |
| `he was able to exit the home safely`（台本が逐語引用） | `he was able to exit the home safely` | **VERIFIED（逐語一致）** |
| ガレージからの発砲がパトカーに命中／high-risk barricade | `Seacat then fired a bullet from inside the garage and struck an officer's car. At that point, the officers deemed the incident a high-risk, barricade situation.` | **VERIFIED** |
| 約5時間の交渉、失敗 | `For approximately five hours, negotiators attempted to convince Seacat to surrender.` | **VERIFIED** |
| 突入シーケンス（ガス弾／BearCat がドアを破りロボットが throw phone／爆薬で射線と進入口／突入→反撃→退却→BearCat が複数の穴） | `they fired several rounds of gas munition into the home, breached the home's doors with a BearCat armored vehicle so they could send in a robot to deliver a "throw phone" to Seacat, and used explosives to create sight lines and points of entry` … `officers used the BearCat to open multiple holes in the home` | **VERIFIED（台本はほぼ逐語）** |
| 19時間 | `this 19-hour standoff` | **VERIFIED** |
| 市は仮住まい費用の援助を申し出た | `the City offered to help with temporary living [expenses]` | **VERIFIED** |
| Mugler v. Kansas (1887) を引いた | `Mugler v. Kansas, 123 U.S. 623, 668–69 (1887)` | **VERIFIED** |
| 「警察は公共の利益のために行動した」と認めた | `We do not disagree that the defendants' actions benefited the public.` | **VERIFIED** |
| `the innocence of the property owner does not factor into the determination` | 同文言を逐語で引用 | **VERIFIED（逐語一致）** |
| 「政策論としては considerable appeal がある」 | `despite "the considerable appeal of this position as a matter of policy," we join the Federal Circuit in rejecting this argument as a matter of law` | **VERIFIED** |
| Colorado 法で willfully/wantonly なら個人責任 | `police officers who willfully or wantonly destroy property may also be subject to tort liability. See ... Colo. Rev. Stat. § 24-10-118(2)(a).` | **VERIFIED** |

#### EP39 — Frazier v. Cupp 原文で確認（Cornell LII, 394 U.S. 731）

| 台本の記述 | 判定 |
|---|---|
| 弁論 1969-02-26 / 判決 1969-04-22 | **VERIFIED** |
| Marshall 判事執筆 | **VERIFIED**（`Mr. Justice Marshall`） |
| 被害者 Russell Anton Marleau・1964年9月22日殺害 | **VERIFIED** |
| 第二級殺人で有罪 | **VERIFIED** |
| `The officer questioning petitioner told him, falsely, that Rawls had been brought in and that he had confessed.` | **VERIFIED（逐語一致）** |
| `I think I had better get a lawyer before I talk any more. I am going to get into trouble more than I am in now.` | **VERIFIED（逐語一致）** |
| `You can't be in any more trouble than you are in now.` | **VERIFIED（逐語一致）** |
| `misrepresented the statements that Rawls had made` を含む中核判示 | **VERIFIED** |
| Clewis v. Texas / totality of the circumstances | **VERIFIED** |
| `Miranda does not apply to this case` | **VERIFIED（逐語一致）** |
| 弁護士発言は Escobedo ほど `clear` `unambiguous` でない | **VERIFIED** |

**EP39 ACT III の逐語引用4箇所はすべて原文と一致。** ただし同幕に人物属性の誤りが1件ある（B-5・下記 §3.2）。

#### EP39 — Laughman 側（検証エージェント報告 ＋ 私による抜き取り確認）

検証エージェントが一次資料で確認し、**そのうち下記2件を私が独立に取り直して裏付けた**（§3.4 の理由による）。

私が直接確認した項目:

| 台本の記述 | 一次資料 | 判定 |
|---|---|---|
| 化学者のバクテリア証言と Innocence Project の評価 | Innocence Project: `The analyst testified incorrectly, however, that bacterial degradation could have changed type A blood to type B or vice versa.` | **VERIFIED（台本 L54 と一致）** |
| 2004-08-26 に Adams County 地方検事 Shawn C. Wagner が全訴因取下げ | Innocence Project が同日付・同氏名を記載 | **VERIFIED** |
| 近隣住民の目撃場所 | Innocence Project: `a neighbor reported seeing her in her yard on the morning of August 13.` → **`yard` であって `garden` ではない** | **CONTRADICTED（B-6）** |
| Frazier の兵役 | LII 原文: `petitioner was questioned briefly about the location of his Marine uniform.` `sailor` / `Navy` / `seaman` は**0件** | **CONTRADICTED（B-5）** |
| `At this point, the officer questioning petitioner told him, falsely, that Rawls...` | 原文は `At this point,` で始まる | 台本は当該2語を落として `The` を大文字化（軽微・下記 H-6） |
| `Before petitioner made any incriminating statements, he received partial warnings of his constitutional rights` | LII 原文に存在 | **VERIFIED（台本 L86 の「部分的権利告知」を裏付け）** |

エージェントが一次資料で確認したと報告した項目（**私は原本未確認**）:

- §1983 訴訟（**govinfo の連邦判決原本** `USCOURTS-pamd-1_05-cv-01033`、Kane 首席判事、2007-08-16）: 被告 `Holtz, Donald Blevins, and Janice Roadcap`／`Fourth and Fourteenth Amendments`／2006-03-17 の一部却下／`On August 24, 2004, a new trial was granted to Laughman, and the District Attorney of Adams County dismissed the charges`／略式判決 `DENIED`。**台本 L100 の「記録間で数日差がある」という括弧書きは正しく、扱いも適切**
- 生年月日 1963-05-16（葬儀社の訃報）→ 台本の派生年齢（取調べ時24歳・有罪時25歳・2021年に58歳・死亡時60歳）が**すべて整合**
- 2024-03-21 死去・Jefferson Einstein Hospital・60歳
- IQ70・10歳相当／指紋の虚偽告知／A・B分泌型／1988-12-16 有罪・4罪名・終身刑／1993 DQ Alpha 結論不能／2003-11 Orchid Cellmark Y-STR 排除
- **Innocence Project 統計（最強の結果）**: `innocenceproject.org/exonerations-data/` が台本の数値を**すべて逐語で掲載** — `257 Innocence Project victories to date` / `205 exonerated by DNA` / `4,102 years` / `16 average years served` / `27 average age when wrongly convicted; 45 average age when exonerated` / `62%` / `29%`。さらに `Numbers stated are current as of April 14, 2026.` と明記され、**2026年時点の現行性まで確認された**
- Oregon SB418 成立法本文: `Sponsored by Senator GORSEK` / 18歳未満 / `presumed to be involuntary` / `the state proves by clear and convincing evidence`（Oregon Laws 2021 ch. 487, ORS 133.403）
- Illinois SB 2122・約10州・成人への一般禁止法なし
- State v. Cayward（1989-11-15・FDCLE と Life Codes, Inc. の両便箋・精液の捏造書類・原審維持・`has no place in our criminal justice system`）
- Kassin et al. 2025（`Law and Human Behavior` Vol. 49, No. 1, pp. 7–53・**共著7名＝「Kassin and six colleagues」と一致**・AP-LS の Scientific Review Paper）
- 2019-01 Bronx（Huwe Burton・2019-01-24・16歳での自白・CIU が虚偽自白研究を `newly discovered evidence` と認定）

### 3.2 一次資料と食い違った項目（CONTRADICTED）

**B-2（BLOCKER）— EP40 L105・引用文言の誤り**

台本:
```
And then it quoted six words from another federal appeals decision:
as unfair as it may seem, the Takings Clause does not give compensation
to every property owner who is harmed.
```

第10巡回区 原本（私が PDF から抽出した実文言）:
```
Thus, "[a]s unfair as it may seem," the Takings Clause simply
"does not entitle all aggrieved owners to recompense."
AmeriSource Corp., 525 F.3d at 1152, 1154.
```

- 前半 `as unfair as it may seem`（6語）は**正しい**。
- 後半が問題。原文は **`does not entitle all aggrieved owners to recompense`**。台本の `does not give compensation to every property owner who is harmed` は**言い換えであって引用ではない**。
- 台本は `it quoted ... :` とコロンで受けているため、**視聴者には後半も裁判所の言葉として聞こえる**。v002 は裁判所の文言をカードに載せる設計（〔CARD〕多用）なので、このままテロップ化すると**存在しない判決文言を画面に出すことになる**。
- 出典も注意: この文言は第10巡回区の自前の言葉ではなく **AmeriSource Corp. v. United States, 525 F.3d 1149 (Fed. Cir. 2008)** からの引用。台本の `another federal appeals decision` という説明自体は正しい。

意味内容は保存されているが、**逐語引用として提示された文が原文と異なる**以上、他の全引用を逐語で通しているこの台本の基準では BLOCKER。

**B-3（BLOCKER）— EP40 L45・「鍵が開いていた」**

台本:
```
He tried doors until one opened, and the house on South Alton Street
was the one that wasn't locked.
```

第10巡回区 原本:
```
officers from the City's police department responded to a burglar alarm
at the Lechs' home and learned that Robert Seacat ... was inside.
...
Although the nine-year-old son of John Lech's girlfriend was present
at the time of the break-in, ...
```

原本は (a) **侵入警報（burglar alarm）が鳴った**こと、(b) 当該事象を **`the break-in`（押し入り）** と呼んでいることを記録している。「鍵の掛かっていないドアから入った」という記述は原本に無く、`break-in` および警報作動と**整合しない**。`unlocked` は PDF 全文検索で**0件**。

この一文は HOOK の主題（「無作為に選ばれた住所」）を支える印象的なディテールだが、一次資料が支えていない。

**B-5（BLOCKER）— EP39 L72・Frazier は水兵ではなく海兵隊員**

台本:
```
police brought in a young sailor named Martin Frazier.
```

Frazier v. Cupp 原文（LII、私が直接確認）:
```
petitioner was questioned briefly about the location of his Marine uniform.
```

原文全体を検索して **`sailor` / `Navy` / `seaman` は0件**、`Marine` が1件。Frazier は**海兵隊員**である。`sailor`（水兵＝海軍）は誤り。1語の置換（`a young Marine named Martin Frazier`）で解消する。

**B-6（BLOCKER）— EP39 L26 / L50・`garden` は一次資料に無い**

台本:
```
L26  On the morning of August 13, 1987, a neighbor saw Edna Laughman out in her garden.
L50  He said he killed her on August 12, though the neighbor had seen her alive in her
     garden on the morning of the 13th. A man's account of a murder should not be
     corrected by a vegetable garden.
```

Innocence Project（私が直接確認）:
```
a neighbor reported seeing her in her yard on the morning of August 13.
```

一次資料は **`yard`（庭先）**。`garden`（菜園・花壇）は台本の創作であり、到達可能な資料のどれにも無い。

**なぜ単なる語選択の問題で済まないか**: この語が **ACT II の決めゼリフを担っている**。`A man's account of a murder should not be corrected by a vegetable garden.` は `vegetable garden` の具体性で成立している一文で、`yard` に直すとオチが崩れる。つまり**裏の取れていないディテールの上に演出上の山場が建っている**。8月13日朝の目撃という事実そのもの、および8月12日供述との矛盾は堅い（Innocence Project が裏付け）ので、修正は語ではなく**この一文の作り直し**になる。

**B-7（BLOCKER・検証エージェントのみ／私は原本未確認）— EP39 L132・Oregon の施行日**

台本:
```
Both took effect on January 1, 2022, and by 2026 roughly ten states have some version of it.
```

エージェントの報告: Illinois は 2022-01-01 で正しいが、**Oregon は誤り**。成立法（Oregon Laws 2021 ch. 487, ORS 133.403）を全文取得した結果、**緊急条項も施行日条項も存在せず**、§2 は「施行日以後に行われた聴取に適用する」とのみ規定。Oregon の既定は会期終了（sine die）から91日目で、2021年会期は 2021-06-26 閉会 → **2021-09-25** が施行日と算出される。

`Both took effect on January 1, 2022` は2州を1つの日付で束ねており、Oregon について誤り。なお同 L132〜L134 は「署名日では Oregon が1日早い」という繊細な論点を OST で正しく処理しているだけに、施行日の取り違えは対比の設計自体を弱める。**私は成立法原本を確認していないため、出荷前に自分の目で ORS 133.403 を当たること。**

### 3.3 一次資料で裏が取れなかった項目（22件）

**EP40（16件）** — 第10巡回区原本に**存在しない**、または本監査で一次資料に到達できなかったもの:

1. `He'd never met them.` / `picked the address at random` — 原本に「無作為」「面識なし」の記述なし（PDF に `random` 0件）
2. 地裁の指示文言 `take as much of the building as needed without making the roof fall in` — **第10巡回区原本に `roof` は0件。** 台本は `recorded by the federal district court` と地裁に帰属させているが、地裁判決（D. Colo. 1:16-cv-01956）に到達できず**未確認**。本作で最も引用されるフレーズなので要確認
3. 地裁判決の日付「January 2018」
4. $5,000 が上告受理申立書に `help with temporary living expenses` として記載されている件（原本には金額なし＝台本の帰属先は正しいが、申立書自体は未確認）
5. 提訴権放棄が $5,000 の条件だったという主張（台本は `in a brief filed by his lawyers` と正しく帰属。内容は未確認）
6. 保険約款の政府職員の故意行為免責／一部支払
7. アスベスト・25万ドル借入・退職5年延期（台本は `According to his brief` と帰属。内容は未確認）
8. Amy Hadley（インディアナ 2022-06-10・IP アドレス誤り・15歳の息子・催涙弾30本・1.6万ドル・第7巡回区 2025-10）
9. Vicki Baker（テキサス 2020-07・人質・陪審評決約6万ドル・第5巡回区が破棄・テキサス州憲法で最終的に支払）
10. Slaybaugh（テネシー・催涙弾約35本・約7万ドル・第6巡回区）— **検証エージェントが「年が誤り（事件は2022年1月、2024年は判決年）」と指摘。未確認だが要精査**
11. Carlos Pena（ロサンゼルス 2022-08・13時間・第9巡回区 2025-11）
12. ラスベガス（2025-08・約3万ドル・市が自主的に支払）— **検証エージェントが「支払主体は LVMPD で、当初は拒否し報道後に翻した」と指摘。台本の `Voluntarily. Because it chose to.` は本作の論理的支点なので要精査**
13. Sotomayor の denial 尊重意見の内容（Gorsuch 同調・circuit split の分布・`further percolation`・`expressed no view on the merits`）
14. Armstrong (1960) の引用文言
15. 上告番号 25-1158 / 25-1163、2026-04-06 申立、9月28日 conference
16. Lech が2026年5月に第三者意見書へ署名した事実／ラスベガスの2名との連名

**EP39（6件）** — 検証エージェント完了後の残余。大半の項目は §3.1 のとおり裏付けが取れた:

17. **子ども34% 対 成人10%（L128）— 本台本で最も弱い主張。** 子ども側（約34%）は裏付けがあるが、**成人側の10%がどの資料にも見つからない**。エージェントが見つけた競合数値は 14%（全 exoneration）／7%（知的障害のない成人 exoneree）／13%（1989–2004 の成人 exoneration）。台本 L128 の `roughly triples the odds` はこの未確認の分母に**全面的に依存**しており、13% なら2.6倍、7% なら約4.9倍で「3倍」は成立しない。**特定の NRE 刊行物に対で典拠を付けるか、倍率表現を落とすかの二択**
18. **被害者 Edna Laughman の年齢85（L26）— 資料が実際に割れている。** 2021年の報道と Gettysburg Times は85、Law&Crime の2023年量刑記事・abc27・PennLive は87。85 のほうが典拠が良く刑事訴状に遡るが、**台本の基準（台帳）が典拠として挙げる NRE 自体が確認できていない**（`exonerationregistry.org` が自動アクセスに 403、旧 `law.umich.edu` URL は現在そこへリダイレクト）。**手動で NRE を確認して帰属を確定するか、帰属先を差し替えること**
19. 2021-07-14 に Sinnett が公表したという枠組み（L110）— **7月14日は検査機関が一致を確認した日**で、逮捕・公表は 7月27–28日というのがエージェントの指摘。Adams County 地方検事の公式リリースは発見できず、`an absolute match` の引用は Law&Crime と abc27 に依存。他媒体は「2021年5月」「7月24日」と競合する日付を出している
20. Oregon SB418 の Kate Brown 署名日 2021-07-14 — Innocence Project の同時期記述（`On Wednesday, Governor Kate Brown signed`／7月14日は水曜）から中程度の確度にとどまる。OLIS が毎回 ECONNRESET で公式の署名記録は未取得
21. Speelman の 2046年まで仮釈放不可（L112）— 報道2社が一致し2021年逮捕＋25年として整合的だが、**訴訟記録では未確認（報道のみ）**
22. Illinois の「全米初」表現（L134 OST）— 知事府の公式リリースが 503 で未取得。ただし**台本の OST は既に `widely reported as` と報道上の呼称として帰属しており、扱いは正しい**

なお **Cayward（L138）は概ね裏付けが取れたが1点ニュアンスがある**: フロリダ州最高裁の処理は正確には **`review dismissed`, 562 So. 2d 347 (Fla. 1990)**（意見無しの表形式エントリ）。台本の `declined review in 1990 and never ruled on the merits` は許容範囲だが、**「本案に達することを明示的に拒んだ」と読ませないこと**。単に判断しなかっただけである。

### 3.4 ★ 検証プロセス自体の警告

EP40 の検証エージェントは、作業途中で**自分が未受領のサブエージェント結果を推測で報告していた**ことを自己申告した（Slaybaugh の事件日、LVMPD と市の区別、Baker の第5巡回区事件番号、第7・第9巡回区の逐語引用など）。事後に本人が原本で取り直したと報告しているが、**一度捏造が混入した経路の出力は、それ自体を一次資料として扱えない。**

本監査では、この申告を受けて **EP40 の最重要項目（第10巡回区の先例性・引用文言・幕1の事実関係）と EP39 の Frazier v. Cupp を、私が原本 PDF / LII 原文にあたって独立に取り直した。** §3.1 の表はすべて私自身が原本で確認した結果である。§3.3 の16件は**エージェントが「確認済み」と述べていても、私が原本を見ていないため未確認として計上した。**

### 3.5 二次情報源の扱い（MEDIUM）

**M-1 — EP39 L30**: `Law and Crime reported that she was beaten and suffocated.`
死因という中核事実を**媒体名で帰属**して処理している。帰属している点は誠実だが、死因は検死・裁判記録・NRE で取れるはずの一次事実であり、報道機関を典拠に置くのは本作の他部分（判例逐語・裁判記録）の水準と釣り合わない。Law and Crime は listicle 系ではないが二次情報源。

なお同じ L30 で錠剤については `The Innocence Project and the legal scholar Brandon Garrett's exoneration record both describe the suffocation the same way` と**二重に帰属**しており、こちらは適切。

**M-2 — 事実台帳が存在しない**: 両台本とも冒頭で台帳（EP39 `C-01〜C-27`、EP40 `C01–C31`）に拘束されると宣言し、末尾に幕ごとの claim id 対応表を持つ。しかし

```
$ find episodes/PD-2026-039-frazier episodes/PD-2026-040-lech \
    -iname "*fact*" -o -iname "*claim*" -o -iname "*recheck*"
（出力なし）
$ ls episodes/PD-2026-040-lech/01_research/
（空）
```

**台帳ファイルはどちらの話にも存在しない。** EP39 v002 §14 E1 は `fact_recheck.v001.json` の逐語ロックを成果物として要求しているが未作成。したがって台本末尾の対応表（C-07 修正版、C-28 使用禁止、「検証者修正」等）は**照合先が無く、宣言としてしか存在しない**。§3.3 の36件を外部一次資料で取り直すしかなかったのはこのため。

---

## 4. AI臭の実測

印象ではなく Bash / Python で計測した。

### 4.1 禁止句（単語境界 `\b` 付き・56パターン）

```
EP39: total hits: 1
  L82  /\bthe fact that\b/  ...has outlived everything else in the case.
       "The fact that the police misrepresented the statements that Rawls had made..."
EP40: total hits: 0
```

EP39 の唯一のヒットは**最高裁判決文の逐語引用の内部**（`The fact that the police misrepresented...`）。原文どおりであり、AI臭ではない。指示どおり `\bHere is` の単語境界を使用したため `There is` の誤検出は発生していない。

**実質的な禁止句ヒットは両話とも 0件。**

### 4.2 文長分布

| | EP39 | EP40 |
|---|---|---|
| 文数 | 138 | 182 |
| 平均 | 14.30語 | 11.48語 |
| 標準偏差 | 10.21 | 8.41 |
| 中央値 | 13.0 | 10.0 |
| 最短 / 最長 | 2 / 52 | 2 / 42 |

```
EP39                          EP40
  0-  4w : ##################### (21)      0-  4w : ####################...(43)
  5-  9w : #################################(33)   5-  9w : ...(47)
 10- 14w : ############################ (28)      10- 14w : ...(43)
 15- 19w : #################### (20)      15- 19w : ################## (18)
 20- 24w : ################## (18)      20- 24w : ############## (14)
 25- 29w : ####### (7)                   25- 29w : ######### (9)
 30- 34w : ### (3)                       30- 34w : ##### (5)
 35- 39w : ### (3)                       35- 39w : # (1)
 40- 44w : ## (2)                        40- 44w : ## (2)
 45- 49w : ## (2)
 50- 54w : # (1)
```

標準偏差が平均の 0.71〜0.73 倍あり、分布は長い裾を持つ。**均等長（±2語）が4文以上続く箇所: 両話とも 0件。**

```
--- UNIFORM RUNS (>=4 consecutive sentences within +/-2 words) ---
  EP39: uniform runs found: 0
  EP40: uniform runs found: 0
```

### 4.3 修辞パターン

| 検査項目 | EP39 | EP40 |
|---|---|---|
| 修辞疑問 | **0** | **0** |
| 段落末の要約リフレイン | 0 | 0 |
| アナフォラ（同一2語で始まる文が3連続以上） | **0** | **0** |
| 三段畳みかけ（真正） | 0（検出2件は地名 `Oxford Township, Adams County, Pennsylvania.` と `The test, the Court said, citing Clewis v.` の分割誤検出） | 0（検出2件は日付 `On June 29, 2020, it declined.` と `They had a warrant, an IP address, and the wrong home.` ＝内容上必要な列挙） |

**AI臭の典型指標はほぼ全項目でクリーン。** 両台本とも人間の書き手の手癖に近い。

### 4.4 ただし1つだけ実在する手癖 — 否定終止（HIGH）

唯一、計測で明確に浮いたパターン。**短文を否定で閉じる**型が反復している。

```
EP39: short negation-closers (<=9w): 9件
   L12 There were no fingerprints.  /  L12 There was no match.
   L36 Barry had no way to check that.
   L48 The statement did not fit the house.
   L64 That claim has never been tried.
   L84 The Court did not bless the lie.
   L140 In some courts, they may not print it.
   L150 The permission was not.

EP40: short negation-closers (<=9w): 11件  （182文中 = 6.0%）
   L21 He'd never met them.        L31 He gets nothing from it.
   L47 The gunman was not.         L63 The roof did not fall in.
   L93 They were not.              L95 Police power, not eminent domain.
   L99 The document is not an opinion.
   L115 A denial of review decides nothing.
   L123 Baker was eventually paid, but not by the Constitution.
   L135 It carried no legal weight.
   L147 He gets nothing from those cases.
```

さらに**対句反転**が両話に散在:

```
EP39 L150  The print was invented. The permission was not.
EP40 L47   The boy was out. The gunman was not.
EP40 L97   The same house. The same rubble.  ／  It takes, and it pays.  ／  It stops, it seizes, it destroys
```

**H-2（HIGH）— なぜAIっぽいか**: 一つ一つは強い。しかし EP40 で 11回、しかも幕の切れ目・カードの直前という**同じ構造的位置**に繰り返し置かれると、「意味の反転で段落を締める」テンプレートが露出する。人間の書き手は決め所を惜しんで temporal に散らすが、生成文は効いた型を等間隔で再利用する。とくに **L97 は1段落に3つの装置（`It takes, and it pays` / `It stops, it seizes, it destroys` / `The same house. The same rubble.`）が積層**していて、ここだけ密度が突出している。

**人間ならどう書くか**:
- L97 の3装置のうち2つを平文に戻す。例: `Police power is the state responding to a danger — it stops things, seizes things, destroys things, and under the line the court drew, it doesn't pay.` と一続きにして、`The same house. The same rubble.` だけを決めとして残す。
- EP40 の11個の否定終止のうち、幕内部の4〜5個を肯定形の平叙に戻す。`It carried no legal weight.` → `It was a statement, and a statement binds nobody.` のように、否定で落とさず別の形で終える。
- `He gets nothing from it.`（L31）と `He gets nothing from those cases.`（L147）は**ほぼ同一文の再利用**。片方を変える（L31 を `Not a dollar of it comes back to him.` 等）だけで反復感が大きく減る。

### 4.5 短文断片の総量（MEDIUM）

```
EP39: <=5語の独立文 34件 / 138文 = 24.6%
EP40: <=5語の独立文 57件 / 182文 = 31.3%
```

**M-3**: EP40 は3文に1文が5語以下。ドキュメンタリー・ナレーションの意図的なリズム設計であり（v002 も「列挙のリズム」を明記）、それ自体は欠陥ではない。ただし 31.3% は「長文→短断片→さらに短い断片」のケイデンスが**常時オン**であることを意味し、緩急が付けにくい。とくに幕4の住所列挙（`Indiana. June 10, 2022.` / `Texas, July 2020.` / `Tennessee, 2024.`）は3件が同一テンプレートで並ぶ。L129 の `four addresses` という指示から**意図的なモンタージュ**と判明するので減点はしないが、4件目の Pena だけ `In November 2025 the Ninth Circuit ruled...` と型が崩れており、意図なら揃える／崩すを設計として明示したほうがよい。

---

## 5. 尺（`check_script_length.py` 実測出力）

```
$ python scripts/check_script_length.py episodes/_planning/EP39_frazier_script.en.v001.md
PASS script_length: 2,136 words (need 2,048-2,226)
  narration estimate  slow 13.0m | median 12.0m | fast 9.0m
  target band         11.5-12.5 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence)
    this lands at 9.0 min -- under the floor. Either pin the voice speed or write to 2,730 words.
=== EXIT: 0 ===

$ python scripts/check_script_length.py episodes/_planning/EP40_lech_script.en.v001.md
PASS script_length: 2,153 words (need 2,048-2,226)
  narration estimate  slow 13.2m | median 12.1m | fast 9.1m
  target band         11.5-12.5 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence)
    this lands at 9.1 min -- under the floor. Either pin the voice speed or write to 2,730 words.
=== EXIT: 0 ===
```

**両話 PASS。** fast端リスクの警告は両話に出るが、EP39 v002 §0.3 / EP40 v002 §0.3 がいずれも voice speed のピン留め（ElevenLabs stability 0.35 等）を一次対策として明記済みで、対応済みの既知リスク。EP40 は台本ヘッダ L9 にも `TTS発注時に voice speed をピン留めすること` と書かれている。

---

## 6. 構成

### 6.1 冒頭30秒に最強の事実があるか — 両話 PASS

冒頭90語（≒30秒）の語彙密度を計測:

```
EP39  FIRST ~30s (90 words): legal=0  human=7
EP40  FIRST ~30s (90 words): legal=0  human=9
```

**両話とも冒頭30秒の法律語density が 0。** 人物語が7〜9。

- EP39 HOOK（21.6秒）: `A man with the comprehension of a ten-year-old described a wound that a coroner had to open a body to find.` → 最強の逆説を1文目に置き、`There were no fingerprints. There was no match.` で反転、`every word of it was legal.` で主題を刺す。**構造として理想形。**
- EP40 HOOK（17.67秒）: `The nine-year-old walked out of the house first. He wasn't hurt.` → 9歳の子の生還から入り、`The house stood for another nineteen hours. / Then it didn't.` で落とす。**何が起きたかを言わずに引く設計。**

### 6.2 統計が人物より先に出ていないか — 両話 PASS

```
EP39  first number/stat position (word idx): [113, 114, ...]   ← "August 13, 1987"（日付）
EP40  first number/stat position (word idx): [916, 1059, ...]  ← 幕2の $5,000
```

EP39 は最初の数値が113語目でこれは事件の日付。統計（257件・4,102年）は **493秒地点＝ACT IV 後半**。EP40 は**最初の数値が916語目**（全体の44%地点）。**両話とも人物が完全に先行。**

### 6.3 判例解説型になっていないか

幕ごとの法律語密度を計測した（実測: 判例解説型 APV 1.6–7.5% vs 一人の受難型 24–42%）。

**EP39**

| 幕 | 語数 | legal/100語 | human語 |
|---|---|---|---|
| HOOK | 64 | 0.0 | 3 |
| OPENING | 22 | 0.0 | 4 |
| ACT I | 268 | 0.4 | 23 |
| ACT II | 326 | 0.3 | 24 |
| **ACT III** | **414** | **3.4** | **10** |
| ACT IV | 728 | 1.8 | 23 |
| ENDING | 154 | 0.6 | 8 |

**EP40**

| 幕 | 語数 | legal/100語 | human語 |
|---|---|---|---|
| HOOK | 48 | 0.0 | 6 |
| FLASH-FORWARD | 23 | 0.0 | 3 |
| OP | 27 | 0.0 | 1 |
| ACT 1 | 404 | 0.7 | 30 |
| ACT 2 | 409 | 1.7 | 36 |
| **ACT 3** | **369** | **6.8** | **9** |
| ACT 4 | 583 | 4.3 | 32 |
| ENDING | 222 | 4.1 | 12 |

**判定: 全体としては受難型で PASS。ただし各話1つずつ危険区間がある。**

- **EP39 ACT III（139.5秒）**: 法律語密度 3.4（他幕の8〜11倍）、人物語が10と全本編幕で最低。**ただし** 末尾 `That is the rule that was waiting in the room when an officer told Barry Laughman about a fingerprint.` で Barry に接続し直しており、判例が主役を乗っ取ってはいない。v002 も §3 で `326.1 / 30.0 / 二つの見落とし` の30秒塊を認識し、`20秒超の平坦を作らない: 12秒目でカット替え＋MG8` と対策済み。
- **H-3（HIGH）— EP40 ACT 3（127.8秒）**: 法律語密度 **6.8** は両話の全幕中で最高、人物語は **9** で最低。**約2分間、人物がほぼ不在で police power / eminent domain / 先例性のドクトリンが連続する。** v002 §3.4 は R4（`They were not.`）を再フック点に置き、§3.9 で `MechanismReveal 4枠を最大18秒間隔で` 差し込む対策を明記しているが、**言語レベルでは人物への復帰が無い。** 幕3の中盤に Leo Lech か家そのものへ戻る1〜2文（例: 判事が線を引いた時点で家が2年以上前に消えていたという L97 末尾の一文を、幕の中央へ移す）を入れると、映像対策に頼らず言語だけで密度が割れる。なお L97 の `By the time a judge in Denver wrote that distinction down, the house on South Alton Street had been gone for more than two years.` は**まさにその機能を持つ最良の一文**で、現在は幕3前半にある。

### 6.4 沈黙の設計 — 両話 PASS

- **EP39: 8箇所 / 合計21.0秒**（2.5+2.0+2.0+2.0+3.0+2.5+4.0+3.0）。v002 §2 の宣言と**完全一致**。
- **EP40: 10箇所 / 合計18.2秒**（1.5+1.2+2.0+2.0+2.0+1.5+2.0+1.5+1.5+3.0）。v002 §3.5 の10行テーブルと**順序まで完全一致**。

いずれも「数字だけを保持」「字幕なし」「Do not score this gap」等、沈黙の中身まで指定されている。EP39 L124 の `[SILENCE 4秒。画面は数字のみ: 4,102 YEARS。]` は本作最長の沈黙で、v002 も `★4.0秒＝ゲート上限3.0秒を超える最長スパン。ここが最大の危険箇所` として §5.4 に専用のモーション仕様を用意している。**設計として自覚的。**

---

## 7. 設計書 v002 との整合

### 7.1 EP39 — 完全一致（BLOCKER 0件）

幕ごとの語数を実測し v002 §2 のテーブルと照合:

```
ACT         script    v002   diff
HOOK            64      64     +0  OK
OPENING         22      22     +0  OK
ACT I          268     268     +0  OK
ACT II         326     326     +0  OK
ACT III        414     414     +0  OK
ACT IV         728     728     +0  OK
ENDING         154     154     +0  OK
TOTAL         1976    1976     +0
```

**7幕すべて語数が1語も違わない。** 沈黙も8箇所21.0秒で一致（§6.4）。v002 内でバッククォート引用されている英文アンカー22件のうち、**20件が台本に逐語で存在**（残り2件は前後の引用符を含めた検索文字列による誤検出で、実体は L12 に存在）。幕構成 `HOOK → OPENING → ACT I–IV → ENDING` も一致。

### 7.2 EP40 — 1件の食い違い（BLOCKER B-4）

```
SECTION          script   v002   diff
HOOK                 48     48     +0  OK
FLASH-FORWARD        23     23     +0  OK
OP                   27     27     +0  OK
ACT 1               404    404     +0  OK
ACT 2               409    413     -4  *** MISMATCH
ACT 3               369    369     +0  OK
ACT 4               583    583     +0  OK
ENDING              222    222     +0  OK
ED                   10     10     +0  OK
TOTAL              2095   2099     -4
```

**B-4（BLOCKER）— 原因を特定した。** 幕2に含まれるインライン〔CARD〕2個ぶん、ちょうど4語:

```
L71  narr= 33  raw= 35   ...Five thousand dollars. 〔CARD: $5,000〕 That figure appears...
L85  narr= 37  raw= 39   ...borrowed two hundred fifty thousand dollars. 〔CARD: $250,000〕 He had...
```

`〔CARD: $5,000〕` = 2語、`〔CARD: $250,000〕` = 2語 → 409 + 4 = 413。**v002 §3.1 の幕2だけが、読み上げられない画面テロップ語をVO語数に含めている。** 他8セクションは全て「ナレーションのみ」で一致しているので、幕2だけ計数規約が破れている。

影響: v002 §3.1 は語数から VO 秒を算出している（413語 → 139.14秒、= 2.968語/秒）。実ナレ409語では 137.79秒であり、**幕2のVO見積もりが約1.35秒過大**。総尺 734.47秒も同分だけ過大（実質 733.1秒）。許容 band は 690–750秒なのでゲートは割らないが、v002 §3.1 は「この表が唯一の正」と宣言しており、**唯一の正の内部で算術が破れている**。台本側の欠陥ではなく v002 側の欠陥。

### 7.3 v002 内部の付随的な不整合（MEDIUM・参考）

EP39 v002 §3 のタイムライン65行を積算すると:

```
rows=65  sum(dur)=732.1  last_end=705.3  (design 705.0)
gaps/overlaps: 14
```

- 末尾が **705.3秒**で、設計値 705.0 と 0.3秒ずれる。
- 検出した14件の不連続のうち大半は `HB#`（AE heroビート）行が**ナレ行への重ね合わせ**であることによる正常な負のデルタ。ただし **455.8秒→462.6秒の 6.8秒**（`Parabon / Speelman / 58歳` の終端から `HB7_PAROLE` の開始まで）は、ナレ行・オーバーレイ行のいずれも割り当てられていない**真の空白**。
- **M-4**: どちらも台本との食い違いではなく v002 内部の算術。実装前に潰しておくと Codex が迷わない。

### 7.4 台本にあって v002 のスロットに無い要素 / その逆

**両話とも該当なし。** EP39 は §7.1 のとおり全幕・全沈黙・全アンカーが対応。EP40 も §6.4 のとおり沈黙10箇所が v002 §3.5 と行単位で対応し、幕構成9セクションが §3.1 の9行と対応する。**構造レベルの欠落・余剰はゼロ。**

---

## 8. 指摘一覧

### BLOCKER（7件）

| ID | 話 | 箇所 | 内容 |
|---|---|---|---|
| **B-1** | EP39 | L58 | `That the victim had been wearing only a bra.` — 性的暴行被害者の着衣・身体状態の描写。「非グラフィック・象徴のみ」を超える。機能的必要なし。v002 §8.1 の封じ込めは映像のみを射程にしておりナレ本文を検査していない |
| **B-2** | EP40 | L105 | 引用文言の誤り。原本は `does not entitle all aggrieved owners to recompense`（AmeriSource Corp., 525 F.3d at 1154）。台本の `does not give compensation to every property owner who is harmed` は言い換えをコロンで引用として提示している。テロップ化すると存在しない判決文言を画面に出す |
| **B-3** | EP40 | L45 | `the one that wasn't locked` — 第10巡回区原本は侵入警報への臨場と `the break-in` を記録。`unlocked` は原本に0件。一次資料と不整合 |
| **B-4** | EP40 | v002 §3.1 | 幕2の語数 413 が台本の実ナレ 409 と食い違う。インライン〔CARD〕2個ぶん4語を混入。VO見積もりが1.35秒過大 |
| **B-5** | EP39 | L72 | `a young sailor` — 原文は `his Marine uniform`。`sailor`/`Navy`/`seaman` は原文に0件。Frazier は海兵隊員。1語で修正可 |
| **B-6** | EP39 | L26 / L50 | `garden` / `vegetable garden` — Innocence Project は `in her yard`。`garden` は到達可能な資料に無い。**ACT II の決めゼリフ `corrected by a vegetable garden` がこの未確認語に依存**しているため、語の置換ではなく一文の作り直しが必要 |
| **B-7** | EP39 | L132 | `Both took effect on January 1, 2022` — Illinois は正しいが **Oregon は誤り**。成立法に緊急条項・施行日条項が無く、既定（sine die 後91日目）で 2021-09-25 と算出される。※検証エージェントのみの確認・要自己検証 |

### HIGH（10件）

| ID | 話 | 箇所 | 内容 |
|---|---|---|---|
| H-1 | EP39 | L106 | `the men who had taken them` — 陪審が判断していない責任を地の文で断定。L64 で確立した帰属の線を自ら越える |
| H-2 | 両話 | 全体 | 否定終止の反復（EP39 9件 / EP40 11件＝6.0%）＋対句反転。L97 に3装置が積層。`He gets nothing from it.` / `He gets nothing from those cases.` はほぼ同一文の再利用 |
| H-3 | EP40 | 幕3 | 法律語密度 6.8・人物語 9。約2分間の人物不在。言語レベルの再フックが無い（映像対策のみ） |
| H-4 | EP40 | 幕4 | Slaybaugh の年（検証エージェントが「事件2022年1月／判決2024年」と指摘）とラスベガスの支払主体・自主性（同「LVMPD、当初拒否、報道後に翻意」）。**後者は `Voluntarily. Because it chose to.` という本作の論理的支点**。要精査 |
| H-5 | EP40 | 幕4 | 検証エージェントの追加指摘: Slaybaugh は「無関係な住所」モンタージュに構造的に適合しない可能性（Conn は Slaybaugh 夫妻の息子）。Baker も被疑者が元便利屋で部分的に不一致。**未確認だが、事実なら幕4の論旨の根幹に関わる** |
| H-6 | EP39 | L128 | `10 percent`（成人の虚偽自白率）が**どの資料にも見つからない**。競合値は 7% / 13% / 14%。これに依存する `roughly triples the odds` は 13% なら2.6倍、7% なら4.9倍で成立しない。**対で典拠を付けるか倍率を落とす** |
| H-7 | EP39 | L110 | `On July 14, 2021, ... Sinnett announced` — 7月14日は**検査機関の一致確認日**で、公表は7月27–28日というのがエージェントの指摘。DA の公式リリースは発見できず、引用は報道2社依存。他媒体は「5月」「7月24日」と競合 |
| H-8 | EP39 | L26 | 被害者の年齢85 — 資料が実際に割れている（85 vs 87）。85 のほうが典拠は良いが、**台帳が典拠とする NRE 自体が確認できていない**（403）。台本は L171 で「不一致の議論は載せない」と決めているが、その決定の土台が未検証 |
| H-9 | EP39 | L142 | Kassin et al. の提言を `restricting the false evidence ploy` と記述。**原文は `banning the presentations of false evidence`**（禁止）。台本は提言を弱めている。論旨に有利な方向への誤りではないが、逐語基準では不正確 |
| H-10 | EP39 | L74 | 引用の開始位置。原文は `At this point, the officer questioning petitioner told him, falsely, ...`。台本は冒頭2語を落として `The` を大文字化。引用語は他は完全一致で軽微だが、逐語を売りにしている幕なので揃えるべき |

### MEDIUM / 観察（7件）

| ID | 内容 |
|---|---|
| M-1 | EP39 L30 死因を `Law and Crime reported` で処理。二次情報源。他部分の水準と不釣り合い |
| M-2 | **事実台帳がどちらの話にも存在しない**（`find` で0件、`01_research/` は空）。台本末尾の claim id 対応表は照合先を持たない |
| M-3 | EP40 の5語以下断片が 31.3%。幕4の住所列挙で4件目だけテンプレートが崩れる |
| M-4 | EP39 v002 §3 タイムラインの末尾が 705.3 で設計値 705.0 と 0.3秒ずれ。455.8→462.6 の 6.8秒が未割当 |
| M-5 | **`check_lech_accuracy.py` がフォールス・グリーン。** 台本が `_planning/` にあるため glob が空振りし `skipped` へ。対象ゼロで PASS |
| M-6 | **R5 の自爆**。台本ヘッダ L7 の `限定免責は本件の争点ではないため一切言及しない。` が `BANNED_QI` に一致。正規パスへそのままコピーすると R5 が FAIL |
| M-7 | **EP39 には `check_frazier_accuracy.py` が存在しない。** EP40 が R1–R8 の実行可能ゲートを持つのに対し、EP39 の R2/R3隣接封じ込め（Speelman・被害者描写・肖像）は散文の約束のみ。B-1 がすり抜けた直接の原因 |

---

## 9. 良かった点（維持すべき設計）

- **EP39 ACT III の逐語精度**: Frazier v. Cupp の引用4箇所すべてが原文と一致。`Miranda does not apply to this case` / `neither as clear nor as unambiguous` まで正確で、`partial warnings` の扱いも原文どおり。**引用の精度は極めて高い**（誤りは引用ではなく人物属性＝B-5 と引用開始位置＝H-10 の2点のみ）。
- **EP39 の統計の現行性**: Innocence Project の7つの数値がすべて公式データページの記載と逐語一致し、同ページが `current as of April 14, 2026` と明記。**2026年の作品として数値が古びていないことまで確認できた稀なケース。**
- **EP39 L100 の日付差の扱い**: `(The federal court's later opinion dates the new trial and the withdrawal of charges to August 24; the records differ by a couple of days.)` — 連邦判決原本が実際に `On August 24, 2004` としており、**台本は資料間の食い違いを隠さず括弧で開示している**。本監査で最も誠実な処理。
- **EP40 幕1の逐語精度**: `he was able to exit the home safely` を含め、突入シーケンス（ガス弾→BearCat→throw phone→爆薬→突入→退却→複数の穴）が原本とほぼ逐語で一致。`19-hour standoff`・`approximately five hours`・`high-risk, barricade situation` も原本どおり。
- **争いある主張の帰属**: EP40 L71 / L73 / L83 は $5,000・提訴権放棄・アスベストをすべて `the family's own petition` / `in a brief filed by his lawyers` / `According to his brief` と帰属し、さらに `What the Tenth Circuit's own document says is narrower` と**記録との差分まで明示**している。EP39 L64 の `That claim has never been tried.` も同様。**この作法は両話の最大の強み。**
- **AI臭の実測がほぼ全項目でクリーン**: 禁止句0（引用内1件を除く）、修辞疑問0、アナフォラ0、均等長ラン0。
- **構造の規律**: EP39 は7幕すべて語数が v002 と1語も違わない。EP40 は沈黙10箇所が v002 と行単位で一致。
- **v002 §0.4 の `accuracy_lock` 設計そのもの**: R1–R8 は EP40 の絶対条件を実行可能なコードに落とし込んだ良い例（2文窓に広げた判断も正しい）。**問題は設計ではなく、対象ファイルが存在しないため動いていないこと。**

---

## 10. 監査の限界（明示）

- **§3.3 の22件は一次資料で確認できていない**（EP40 16件 / EP39 6件）。私が原本に到達できなかったもの、または資料自体が割れている・アクセスを拒否されているもの。
- **EP39 の検証エージェントは信頼度が高いと判断した。** 報告のうち私が独立に取り直した4点（`Marine` / `yard` / 化学者のバクテリア証言 / Wagner の取下げ日）が**すべて一致**し、加えて取得できなかった資料（NRE の403、OLIS の ECONNRESET、知事府の503）を自ら明示していた。したがって §3.1 後半の「エージェント確認」項目は相応に信頼できると考えるが、**B-7（Oregon 施行日）だけは出荷前に自分の目で ORS 133.403 を確認すること** — 施行日は算出（sine die+91日）による推定を含むため。
- 対照的に **EP40 のエージェントは作業中に自らの捏造を申告した**（§3.4）。そのため EP40 側は最重要項目を私が原本 PDF で取り直し、それ以外は未確認として計上している。**同じ「エージェントが確認済みと言った」でも、2話で信頼度を変えて扱っている。**
- **WebSearch の予算を使い切った**（200/200）ため、後半は WebFetch による直接取得のみで検証した。第10巡回区は govinfo の原本 PDF を取得し `pypdf` で全文抽出、Frazier v. Cupp は Cornell LII の原文で確認した。
- **地裁判決（D. Colo. 1:16-cv-01956）に到達できなかった。** そのため EP40 で最も引用される `take as much of the building as needed without making the roof fall in` は**未検証**。第10巡回区原本に `roof` は0件であり、台本の帰属先（地裁）は原本と矛盾しないが、確認は取れていない。**出荷前に最優先で潰すべき1件。**
- 本監査はファイルを一切修正していない。
