# EP62 greene — 組み立て側へ・緊急追補 v001

**2026-08-04 · 設計スレッドから** · 対象: `PD-2026-062-greene`
**本書は `EP62_greene_ASSEMBLY_HANDOFF.v001.md` に優先する。**矛盾があれば本書が正。

---

## 0. 一行

**画像は「揃った」と書いたが、揃っていなかった。** 226枚を全枚目視した結果、
**この映画のモチーフの連鎖（同じ一枚のドアの七つの状態）が作られておらず、最後の画が存在しない。**
13枚を差し替え発注し、サムネ用に1枚、さらに**存在していなかったモチーフ状態1** に1枚を追加した。**合計15枚がまだ生成されていない。**

**組み立ては止めなくていい。** 止まるのは最後の数カットだけで、
ナレーション・filmconfig・カット表・Remotion合成は今すぐ進められる（§4）。

---

## 1. 何が起きたか（事実）

`H:\pd-media\assets\ai\greene\` の226枚を1枚ずつ開いて判定した。記録は
`runs/qc/greene_plate_verdicts_sheets1to6.v001.md`（106 ACCEPT / 1 REJECT / 13 FLAG）と
`runs/qc/greene_plate_verdicts_sheets7to12.v001.md`（85 ACCEPT / 28 FLAG / 7 REJECT）。

文字規則（`no text, no lettering`）はほぼ守られていた。壊れていたのは**映画の骨格**のほうである。

この映画のモチーフは「**同じ一枚のドアに貼られた紙の、七つの状態**」で、
HOOK の1枚目に戻ってくることでループが閉じる。実物はこうなっていた：

| プレート | 設計上の役 | 生成されたもの |
|---|---|---|
| `G001` | 状態1（貼られた直後）・HOOK 1枚目 | セージ色の**木製パネルドア**・**縦長**の紙・テープ**2箇所**・真鍮のノブ |
| `G206` | 状態1の帰り（ループを閉じる） | **青緑の平滑なドア**・**横長**の紙・テープ**四隅**（`G001` との相関 0.741） |
| `G207` `G208` `G209` | 状態3・5・6 | さらに**別のドア**が3枚 |
| `G226` | 状態7 = **映画の最後の画**。褪せていない四角い跡だけが残る | ドアですらない。**奥へ receding していく屋外廊下**。褪せていない四角は**どこにも無い**。しかも**中ほどのドアに紙がまだ貼られている** |

最後の一行が致命的である。ENDING のナレーションは紙が**取り除かれたあと**を語っており、
画は正反対のことを言っている。**そのままでは映画が終われない。**

### 原因は発注側にある（私の設計ミス）

`G206` 以降のプロンプト本文は「**The same door**」としか書いていなかった。
Codex は**1プロンプト＝1枚**で走るので、**前の枚を参照できない**。
「同じドア」は、毎回ドアの特徴を全部書き下ろさない限り成立しない。

再発注では **DOOR の記述（セージ色・木製パネル・上桟の出っ張り・錠前レールの2箇所の剥離・
低い位置の真鍮ノブ・1mからの正対・曇天の平坦光・両端に淡い枠が少し見える構図）を毎回全文書いている。**

---

## 2. 差し替え表（発注は `EP62_greene_CODEX_BATCH_A.v002.md` §「★再発注」に追記済み）

### 2-1. モチーフ連鎖 — 5枚

| 新 | 廃止 | 役 |
|---|---|---|
| `G227` | `G206` | 状態1の帰り。**ループはここで閉じる** |
| `G228` | `G207` | 状態3（風で下端が持ち上がる） |
| `G229` | `G208` | 状態5（紙は無く、破れた角がテープの下に残る） |
| `G230` | `G209` | 状態6（テープも消えた無地） |
| `G231` | `G226` | 状態7・**映画の最後の画**（褪せていない四角い跡） |

### 2-2. 単発の欠陥 — 8枚

| 新 | 廃止 | 却下理由（目視で確認済み） |
|---|---|---|
| `G232` | `G073` | 年代違い。ビニールサイディング／現代のサッシ |
| `G233` | `G140` | 紙幣に**文字と紋章**が写っている（文字規則違反） |
| `G234` | `G183` | 議場が**法廷**に読める（`forbidden_subjects`） |
| `G235` | `G125` | **馬車**。1900〜1930年代に見える |
| `G236` | `G178` | ドローン調＋下40%が白飛び |
| `G237` | `G121` | 平均輝度 **12.6**。携帯では真っ黒 |
| `G238` | `G175` | 平均輝度 **23.5** |
| `G239` | `G174` | **完全に識別可能な女性の顔**（invariant 11・`forbidden_subjects`）。Haar cascade はこれを検出せず、代わりに壁のテクスチャ20箇所で誤発火していた |

### 2-3. サムネ用 — 1枚

| 新 | 内容 |
|---|---|
| `G240` | 明るい引きの候補。既存 THUMB 3枚（`G220`–`G222`）は3枚とも寄りで低照度で、輝度ゲート（平均33以上）を確実に超える候補が1枚も無かった |

**`G240` は `mandatory_stills` に入れない。** サムネは本編のカットにならないので、
宣言すると `check_spec_satisfied.py` が「宣言された静止画がどのカットにも無い」で落ちる。

---

## 3. 私が更新したもの（組み立て側は再取得すること）

| ファイル | 変更 |
|---|---|
| `episodes/PD-2026-062-greene/episode_spec.v001.json` | `mandatory_stills` の13件を新番号に差し替え、`G241` を追加して **224件**（`check_episode_spec.py --slug greene` = valid） |
| `episodes/_planning/EP62_greene_CODEX_BATCH_A.v002.md` | 末尾に「★再発注」13枚＋`G240`（サムネ）＋`G241`（モチーフ状態1）= **241枚**。冗頭に現在の真実をまとめた★ブロックを立て、古い指示3件を撤回 |
| `episodes/_planning/EP62_greene_script.en.v003.md` | L11 のモチーフ宣言と L357 の ENDING コールバックを `G227` / `G230` / `G231` に |
| `episodes/_planning/EP62_greene_FILM_BIBLE.v001.md` | マクロ・ループの記述を `G227` → 状態7 `G231` に訂正（旧記述の `G208→G209` は状態5→6で、そもそも誤りだった） |
| `episodes/PD-2026-062-greene/04_scenes/thumb_prompts.v001.md` | 第4候補を `G226` → `G240` に。§4 を「発注済み・`mandatory_stills` に入れるな」に書き換え |
| `EP62_greene_ASSEMBLY_HANDOFF.v001.md` | §3-4 とファイル一覧を新番号に |

すべて `scripts/pd_edit.py` 経由（アンカー0件なら適用せず中止するので、無音の空振りは起きない）。

---

## 4. 組み立て側がいま**できること**（14枚を待たない）

止まるのは ENDING の最後の数カットと、モチーフが出る4箇所だけである。

1. **ナレーション生成**（ElevenLabs `nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2`）。
   台本は確定している。差し替えは**画像だけで、一語も台本を変えていない**。
2. **filmconfig / 生成カット表 / beats**。プレートIDだけ新番号を使う（§2 の表）。
   **beats は `EP62_greene_beats.v002.json` を使うこと（v001 は破棄・理由は §8）。**
3. **Remotion 合成と字幕**。
4. **素材（実写）**は9/47 accepted のまま。ここは今回の差し替えと無関係。

**やってはいけないこと：**

- `G206` `G207` `G208` `G209` `G226` `G073` `G121` `G125` `G140` `G174` `G175` `G178` `G183`
  を**カットに使わない**。ファイルは `remotion/public/greene/img` にまだ置いてあるが**廃止済み**である。
  （`G174` は識別可能な顔なので、テスト書き出しであっても画に出さない。）
- `G240` を `mandatory_stills` に**足さない**。

---

## 5. 生成側（Codex）への発注

`episodes/_planning/EP62_greene_CODEX_BATCH_A.v002.md` の末尾2ブロック（「★再発注」「★追加」）だけを回す。
**`G001`–`G226` は一語も触らない**（226枚はそのまま残す。廃止13枚は使わないだけで、消さない＝
`.claude/rules/05-episode-artifacts.md`「stale artifact を削除せず再計算対象として示す」）。

- 出力先: `H:\pd-media\assets\ai\greene\G227.png` … `G241.png`（15枚）
- 長辺3840px以上・16:9・PNG
- 生成後に `remotion/public/greene/img/` へ配置（現在240ファイル = 旧226 + P001–P014。追加後 255）

生成後の検査（1枚ずつ）:

1. `G241` と `G227`–`G231` の6枚が**互いに同じドアに見えるか**。`G001` と並べて見る。ここが今回の全部である。
   とくに **`G241` と `G227` は完全に平ら**（角も下端も浮いていない）であること。この2枚が重なって初めてループが閉じる。
2. `G231` に**褪せていない四角い跡**があり、**紙もテープも画面のどこにも無い**か。
3. 文字が1文字も無いか。`G233` は特に紙幣なので注意。
4. 顔が判別できないか。`G239` は後頭部のみ。
5. 平均輝度。`G237` `G238` は前任が 12.6 / 23.5 で落ちた枚である。`G240` は33以上（狙いは38以上）。

---

## 6. まだ残っている未解決（正直に）

- **R15（音読）が4話とも未実施。** 下読みTTSを回してオーナーが聴く工程がまだ無い。
- 再レビューは **実行済み**（`EP62_greene_REREVIEW.v002.md`）。判定は **DOES NOT MEET IT**で、残るのは **R15（音読）未実施** のみ。
  （R6 のモチーフ状態1 と §12 の92%規則違反は両方修正済み。）
- **台本は v004 が正典**。v003 は3回上書きされていたので凍結した。
- ~~`EP62_greene_beats.v001.json` は **台本より古い**~~ → **作り直した。正典は `EP62_greene_beats.v002.json`（96個）。** 詳細は §8。
- 実写素材 9/47 accepted は契約の distinct_video 234 に対して薄い。画像を動かして稼ぐ前提のままである。
- 目視QCの FLAG 41件のうち、上の13件以外は「使えるが弱い」判定で、差し替えていない。

---

## 7. 検算コマンド

```bash
cd C:/Users/aab15/Documents/prime-documentary
.venv/Scripts/python.exe scripts/check_episode_spec.py --slug greene
.venv/Scripts/python.exe scripts/check_episode_inputs.py --slug greene
```

プレート数の確認（発注ファイル側）:

```bash
.venv/Scripts/python.exe -c "import re,pathlib;t=pathlib.Path('episodes/_planning/EP62_greene_CODEX_BATCH_A.v002.md').read_text(encoding='utf-8');i=re.findall(r'^- .(G\d{3})\.png.\s*$',t,re.M);print(len(i),len(set(i)),i[-1])"
```

期待値: `241 241 G241`

---

## 8. figure beats を作り直した（2026-08-05）— v001 は使わない

**正典: `episodes/_planning/EP62_greene_beats.v002.json`（96個 / HOOK 3・OP 3・ACT_1 17・ACT_2 15・ACT_3 16・ACT_4 17・ACT_5 17・ENDING 8）。**
契約 `figure_beats_per_act` 13–17 を全幕で満たす。`set_figure_beats.py --dry-run` exit 0（96 beat valid）。
**`beats.v001.json` は上書きせず残す**（`.claude/rules/05` `12`）。**組み立てでは参照しない。**

### 8-1. なぜ作り直したか（仕組みの話）

`build_case_film_generic.py::build_figures` は beats に時刻を与えない。**区間の中で等間隔に置く**：

```
start = lo + span * (i + 0.5) / N      # N = その区間の beat 数
```

つまり **配列の何番目にあるかが、そのまま画面に出る秒**になる。
v001 は「語りの順番」では正しかったが「語りの**語数の位置**」では合っておらず、
ACT_1 以降でカードが 1〜5 スロット遅れて出ていた。実測（台本 v004 の語位置で照合）：

| v001 の beat | 実際に出る位置 | そこで語られていること |
|---|---|---|
| ACT_5 [12] `JUSTICE O'CONNOR, DISSENTING` | w1211/1647 | **多数意見**が in rem / in personam を判断しないと言っている所 |
| ACT_5 [14] 反対意見の「引用ゼロ」stat | w1405/1647 | 郵便受けの比喩の**後**・「それは本物の議論だ」 |
| ACT_5 [15] 「11州」ticker | w1502/1647 | 反対意見の**第二の攻撃**（迅速性）の途中 |
| ACT_5 [16] 郵便受けの引用（反対意見） | w1599/1647 | **多数意見**の脚注の反論（prompt or certain） |
| ACT_5 [9] `THE HOLDING` | w920/1647 | 反対意見の書き手の紹介 |
| ACT_1 [11] Grannis 引用 | w718/1062 | 条文を半速で読んでいる最中（音楽なしの指定箇所） |
| ACT_1 [7] `JOSEPH GREENE` | w469/1062 | 「立ち退きが相手に何を要求するか」 |
| ACT_4 [2] `WESTERN DISTRICT OF KENTUCKY` | w124/845 | Mullane 基準の主張 |

v002 は全 96 個を語数位置で置き直した。上の8件はすべて自分の一節の上に乗っている。

### 8-2. 直した文字列（照合先は `measurements/EP62_greene_RAW.md` のみ）

| 場所 | v001（画面に焼かれる予定だった） | v002（RAW 逐語） |
|---|---|---|
| ACT_5 最終 | "It is no secret … by thieves. **Posting, at least, gives assurance** that the notice has gotten as far as the tenant's door." | "It is no secret … by thieves. **Moreover, unlike the use of the mails, posting notice at least gives assurance** that the notice has gotten as far as the tenant's door." |
| ACT_5 | "**A procedure's** effect must be judged in the light of its practical application…" ／ 出典 "Greene v. Lindsey (1982), stating the test" | 削除（別スロットへ）。**"its effect must be judged…" は North Laramie Land Co. v. Hoffman (1925) の語**であり、Greene 自身の文ではない |
| ACT_5 | "…deprived of a significant interest in property **—** indeed…" | "…in property**:** indeed…"（原文はコロン） |
| ACT_5 | 反対意見の告発を "…the work of the Kentucky Legislature." で切る | "…the work of the Kentucky Legislature **and, by implication, that of at least 10 other States.**" |
| ACT_5 | ticker 11 = "States, at least, **authorising notice by posting alone**" | "States, at least, authorizing notice in summary eviction proceedings **solely by posting or by leaving it at the tenant's residence** — the dissent's count"（原文は二択） |
| ACT_2 | "If no one is at home…posting follows forthwith." 出典 = **"Brief for the appellants"** | 出典 = **Greene v. Lindsey (1982)・裁判所自身の文**（"good percentage" だけが n.8 の宣誓証言からの引用） |
| ACT_2 | highlightring "a good percentage" — **the appellants' own estimate** | "quoted from a deposition, not the Court's own estimate"（台本 L128・n.8 = App. 76） |
| ACT_2 | "**it is** reasonable to assume that a property owner…" | "**It is, of course,** reasonable to assume that a property owner…" |
| ACT_2 | "…second attempt at personal service **—** perhaps at some time of day…" | "…personal service**,** perhaps at some time of day…"（原文はコンマ） |
| ACT_3 | "I have seen them take them off of the door**,** and I would go back…" | "…off of the door and I would go back…"（原文にコンマなし） |
| ACT_3 | "…no occasion where I saw anyone tear the **writs** off of the door" | "…tear the **Writs** off of the door"（原文の大文字） |
| ACT_4 | "**conditions had changed since Weber, and there was** undisputed testimony…" | "**there is** undisputed testimony in this case that notices posted on the apartment doors of tenants are often removed by other tenants"（地裁の原文） |
| ACT_4 | "**There may have been** a time when posting provided a surer means…" | "a time when posting provided a surer means of giving notice than did mailing. That time has passed."（"while there may have been" は最高裁の地の文） |

### 8-3. 事実として間違っていた図版（引用ではないもの）

| 場所 | v001 | 直した理由 |
|---|---|---|
| ACT_1 `SECTION 454.030` | "**Three sentences.**" | 条文は**二文**（台本 L78・RAW）。三は「節（clause）」の数 |
| ACT_1 kinetic | "THREE NAMES AND **A SHARED ADDRESS**" | 判決文は "tenants in a Louisville housing project" としか言わない。同一住所は記録にない → "同じ housing project" として下三分に統合 |
| ACT_1 kinetic | "USUALLY A DEPUTY. **NEVER A NAME.**" | 台本 L60 は「二人は後で、反対意見でだけ名前を取り戻す」。**NEVER は台本と矛盾** → "UNNAMED IN THE CAPTION." |
| ACT_3 `VILLAGE WEST` | "The development **two servers** named, **deposed separately**" | 台本のロック「n.7 の3つの抜粋の背後にいる証言者を数えない」に違反。記録は別人とも別調書とも言っていない → "Named twice in the same footnote." |
| ACT_3 `CARTER BACON` | "**The second server.**" | 同上（数えている）→ VILLAGE WEST の下三分に統合し「"probably a couple of times" と言った男に反対意見が名前を与える」 |
| ACT_3 `GILBERT BRUTSCHER` | "Same job, **same doors**, opposite answer" | 台本 L186 は「**反対意見は同じ建物で働いたとは言っていない**」。真逆 → 台本の一文をそのまま採用 |
| ACT_3 kinetic | "**CLAIMED. STATED.**" | 最高裁の動詞は現在形の claim / state（台本 L198「Not *did suffer*」）→ "CLAIM. STATE. / NOT DID SUFFER." |
| ACT_3 stat | "Counts, surveys or studies anywhere in this opinion. **Nobody had counted.**" | 台本 L176 の範囲に合わせて "Studies, surveys or counts the majority weighed against the depositions" |
| ACT_4 下三分 | "A class action under section 1983, the **Reconstruction-era statute**" | 台本にも台帳にも無い。1871年という属性はこの映画のどこにも出てこない → 台本 L212 の言い方に統一 |
| ACT_4 下三分 | "Summary judgment for the sheriff and **the officials**" | 台本 L220 は "the sheriff and his deputies"（下三分ごと削除・語数位置に空きが無いため） |
| HOOK stat | "Second attempts provided for … = 0" | HOOK の25語はこの事実を語らない（ACT_2 の事実）。**フックで本編の事実を先出ししない** → 削除（ACT_2 の逐語引用 GL-21 が担う） |
| HOOK kinetic | "THE MEN WHO TAPED IT UP / WERE ASKED, UNDER OATH…" | 同上。宣誓証言は ACT_3 で初めて出る |
| ENDING `casetimeline_c` | 1975→1981→1982→After の年表 | `PD_SCREENPLAY_STANDARD` §12「ENDING は要約ではなく再フレーム」。年表は要約そのもの → 削除（年表は ACT_4 に一つ残る） |
| ENDING 下三分 | "LINNIE LINDSEY · BARBARA HODGENS · PAMELA RAY" | v004 の ENDING は三人の名を**呼ばない**（名は ACT_5 で終わっている）。語っていない所に名前を出さない → 削除 |
| ENDING kinetic | "THE COURT CHOSE / THE MEN **WHO WALKED / TO THE DOOR.**" | 台本 L358 は「**紙が剥がれたと言った**男たちを選んだ」→ "THE MEN WHO SAID / THE PAPER CAME OFF." |

### 8-4. 数字の裏づけ（台帳の行）

| beat | 数 | 根拠 |
|---|---|---|
| ACT_4 numberticker | 1909 | **GL-31**（Weber, 169 F. 522 (1909)・"some 70 years earlier"） |
| ACT_5 numberticker | 11 | **GL-75**（反対意見「at least 11 States」＋ n.1 の11州リスト） |
| ACT_1 stat | 0（玄関先の会話） | **GL-19 / 台本 L96**「In each instance, notice took the form of posting…」＝三戸とも投函に至った |
| ACT_3 stat | 0（調査・統計・計数） | **Q-04**（判決文に量的な数字は無い）＋台本 L176 |
| ENDING stat | 0（同上・再フレーム） | 同上。**新事実ではない**（§12） |
| ACT_2 / ACT_4 / ENDING compbars | 3 対 1 | 条文の三段（GL-18/19）と GL-20/21（一回の訪問で投函）。映画自身の読みであって判決文の数字ではない |

**支えられなかったので落とした数字はゼロ。**（v001 の "0 second attempts" は事実としては GL-21 で支えられるが、置かれていた HOOK でその話を語っていないので落とした。）

### 8-5. ACT_5 の並べ替え（92%規則で本文が動いたため）

**v001 の順**（多数意見 11 → 反対意見 6。反対意見のカードが多数意見の上に落ちていた）

```
acttitle · BRENNAN · Mullane基準 · 財産的利益 · practical application · WHAT THE THING DOES ·
転回 · IN A SIGNIFICANT NUMBER · continued exclusive reliance · THE HOLDING · hold only ·
DID NOT BAN · O'CONNOR DISSENTING · sole ground · stat 0件 · ticker 11州 · 郵便受け
```

**v002 の順**（本文 v004 の語位置に合わせた。話者が入れ替わる箇所を守る）

```
 0 acttitle
 1 財産的利益（多数）        2 secure posting（多数・反対側を最強の形で）
 3 転回（多数）              4 IN A SIGNIFICANT NUMBER（多数）
 5 郵便について（多数）      6 continued exclusive reliance（多数）
 7 hold only（多数 n.9）     8 IT DID NOT BAN POSTING / IT DID NOT ORDER THE MAIL
 9 O'CONNOR, DISSENTING     10 sole ground / flimsy basis（反対）
11 ticker 11州（反対）       12 **in rem / in personam を判断しない（多数）** ← 動いた区画
13 Ferguson v. Skrupa（反対・制度論）
14 郵便受け（反対）          15 SPEED IS THE DESIGN（反対の第二の攻撃）
16 prompt or certain（多数 n.4 の反論）
```

12 の「判断しない」区画が一つ上がったので、**その前後で話者が三回入れ替わる**。
v002 はその三回をカードの側でも守っている（11 反対 → 12 多数 → 13 反対）。

### 8-6. 仕掛けの副作用（v001 が踏んでいた罠）

`build_figures` は最後に **`figures[0]` と `figures[-1]` を AI開示の下三分で上書きする**。
つまり映画の**最初の1枚と最後の1枚は、何を書いても開示カードになる**。
v001 は ENDING の最後に決め台詞 "THAT THE PAPER WOULD STILL BE THERE" を置いていたので、
**それは画面に出ないはずだった**（台本 L372 の `【OST: STILL THERE】` は figure beat ではないので、そちらをどう実装するかは組み立て側の判断）。
v002 は両端に開示カードを明示的に置き、決め台詞の枠を無駄にしていない。

HOOK は 4 → 3。8.6秒の区間に3秒カードを4枚置くと約0.9秒ずつ重なる（3枚なら0.1秒）。
