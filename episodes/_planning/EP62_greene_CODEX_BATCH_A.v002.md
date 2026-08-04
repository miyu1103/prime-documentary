# EP62 greene — Codex 画像生成 **1本で完結する発注** v002（**現在 241枚**・1プロンプト1枚）

> # ★ このファイルの現在の真実（2026-08-04・ここだけが正）
> 本文は修正を五層追記してある。**以下と矛盾する記述が本文中に残っているが、全部古い。**
>
> - **プレート 241枚**（`G001`–`G241`、欠番なし）。本文中の「222枚」「225枚」「226枚」「239枚」はすべて途中経過。
> - **`mandatory_stills` 224件**。THUMB 4枚（`G220` `G221` `G222` `G240`）は除外する。
> - **モチーフ（同じ一枚のドアの七つの状態）**：状態1 = `G241`（HOOK 1枚目・完全に平ら）・状態2 = `G001`（角が浮く）・状態1の帰り = `G227`・状態3 = `G228`・状態5 = `G229`・状態6 = `G230`・**状態7（映画の最後の画）= `G231`**。
> - **廃止プレート（生成済みだがカットに使わない）**：`G206` `G207` `G208` `G209` `G226` `G073` `G121` `G125` `G140` `G174` `G175` `G178` `G183`。**景観カットとしても使わない。**（`G174` は識別可能な顔なのでテスト書き出しでも画に出さない。）
> - **これから生成するのは末尾3ブロックの 15枚だけ**：`G227`–`G239`・`G240`・`G241`。`G001`–`G226` は再生成しない。
> - 詳細は `EP62_greene_ASSEMBLY_ADDENDUM.v001.md`。

> ⚠ **2026-08-04 追記：末尾に §7 として3枚(G223-G225)を追加しました。G001-G222 は変更ありません。**

> ## ✅ 今すぐ着手してよいファイルです。**追加バッチは出ません。**
>
> ### v001 との違い（読んでから着手すること）
> **v001 は台本が存在しない時点で、事実台帳（FACTS LEDGER）と一般的な8区分の形だけから書かれました。**
> つまり v001 のプレートは「たぶんこういうビートが来るはず」という**推測**です。オーナーがこれを指摘しました。
> 台本 `EP62_greene_script.en.v002.md` は現在**実在します（実測5,318語・8区分）**。
> **v002 はその台本の実ビートから再導出したものです。** 枚数配分も章ごとの実測語数から算出し直しました（§4）。
> v001 はディスク上に残置します（削除・上書き禁止）。v001 のプロンプトのうち**実在のビートに当たるものだけ**を
> 引き継ぎ、残りは捨てました。**着手するのは本ファイル v002 です。**
>
> ### さらに v002 で変わった2点（オーナー決定・2026-08-04）
> 1. **HOOKは約8秒になりました**（従来の約50秒ではない）。`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` 行9の
>    フラッシュフォワード方式：本編最強のビートを3〜4個、約2秒刻みで見せ、決め台詞1つと未解決の問いを置く。
>    よって **HOOKの枚数は12枚→5枚**。浮いた7枚は各ACTへ配り直しました。
>    **HOOKの5枚は本発注中で最も強い5枚**であり、かつ**全て本編の後段でもう一度使われます**（約束と回収）。
> 2. **画づくりの水準はアカデミー／パルムドール級の脚本と同じ基準です。**「一般的なカバレッジ」を禁止します。
>    各プロンプトは**視点を持つ**こと——**具体的な光・具体的な距離・具体的な瞬間**を必ず書く。
>    ストックフォト調（誰の目でもない、いつでもない、どこからでもない絵）は不合格です。
>    §5のプロンプトはすべてその形式で書いてあります。**距離・光・瞬間の指定を削らないでください。**

**題材:** *Greene v. Lindsey*, 456 U.S. 444 (1982)。ケンタッキー州ルイビルの公営住宅で、立ち退きの
通知が**ドアに貼られただけ**だった。住人は見ていないと主張し、欠席判決が確定した。

**この映画は「強欲な家主」の話ではありません。**訴えられた側は**ルイビル住宅公社＝政府機関**です。
主題は**誰も読まなかった一枚の紙**であり、立ち退きそのものではありません。

**この話のマクロ・ループは「紙」、仕込み物は「テープ」です**（台本の構造ロック）。ACT_2 で置かれたテープが
ENDING で回収されます。だから紙とテープのプレートは**同じドア・同じ画角・同じ光**で複数枚あります。
これは被りではなく、**時間経過を見せるための同一画角の連番**です。指定どおり同じ画角で作ってください。

枚数の根拠は `EP62_65_IMAGE_BUDGET.v001.md`：契約 `distinct_video_assets` 234 − 実写採用12 = **222**。

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**
3. **「良いのが出るまで回す」を禁止する。**
4. 作り直してよいのは §1 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。

EP60はこの規則で **279枚・変種0・指定外0・sha256重複0・知覚的近似重複0** を達成済み。

---

## 1. ★絶対条件（触れた絵は使用不可）

`episodes/PD-2026-062-greene/episode_spec.v001.json` の `forbidden_subjects` がこの節の正典です。

- **立ち退きの最中を描かない。** 歩道に出された家具・追い出される家族・**ドアの前の保安官**。一切。
- **制服の執行官・保安官・警官を描かない。** この映画に「来た人」は映りません。映るのは**紙**です。
- **家主というキャラクターを描かない。** 被告は政府機関です。
- **実在の3人（Linnie Lindsey / Barbara Hodgens / Pamela Ray）とその住居を描かない。** 人物は全員
  「実在しない一般人」として描く。台本にある「三つのドア」は**匿名の一般的な集合住宅**として描くこと。
- **法廷内観を描かない。** 木槌・判事席・傍聴席。棚の法廷映像は61話で使い切っています。
  **裁判所は外観のみ可。**
- **監獄を描かない。** 鉄格子・有刺鉄線・独房・手錠。この話は収監の話ではありません。
- **読める文字・数字・署名・印章・ロゴを描かない。** 通知の紙も**文字が判別できない状態**で描く。
  ★**この話で最大の事故源はここです。** ドアに貼られる紙は全222枚のうち約30枚に出ます。
  1枚でも読める文字が乗ると、その絵は「実際の令状の偽造」になります。**紙は必ず白紙・または印字が
  灰色の帯に溶けた状態**にしてください。プロンプト本文には一切の文字要素を書いていません。
- **実在と特定できる建物を描かない。** 看板・紋章・特徴的な建築で場所が割れる絵は不可。
- **子どもの顔を描かない。** 子どもは「痕跡」でのみ表す（自転車・チョーク・ボール・低い位置の手）。
- **広告調にしない。** 黄金色の夕陽、絵葉書の風景、クリスマス、南国、砂漠、ドローンの映え、暖炉のくつろぎ。
- **同情の演出を禁止する。** 肩に置かれた手、涙、時計のカウントダウン、寄り添う老夫婦。
- **黒つぶれさせない。** スマホで見て何が写っているか分かること。

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字・署名がある（**紙の上も含む**） |
| Q3 | 印章・紋章・ロゴらしきものがある |
| Q4 | 制服・バッジ・パトカー・法廷内観・鉄格子が写っている |
| Q5 | 立ち退きの最中（歩道の家具・運び出される荷物・泣いている人）が写っている |
| Q6 | 既存の他話の画像と実質同じ構図 |
| Q7 | 広告調（黄金色の映え・絵葉書・くつろぎ暖炉）である |
| Q8 | 画面全体が暗すぎる |
| Q9 | 子どもの顔が判別できる |

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, muted natural colour, flat humid Ohio Valley light, low contrast, low-key but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing, mid-1970s to early-1980s American public housing period detail, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> text, lettering, numerals, handwriting, signatures, seals, emblems, logos, signage, house numbers, street signs, police uniform, sheriff badge, patrol car, courtroom interior, gavel, judge's bench, prison bars, razor wire, handcuffs, furniture on a pavement, people being evicted, crying, a hand on a shoulder, golden hour, sunset glow, postcard scenery, drone shot, cosy fireplace, Christmas, tropical, modern smartphones, modern cars, flat CGI, cartoon, illustration, oversaturated

> **注意（v002で厳格化）。** §5 のプロンプト本文には、`text` / `lettering` / `sign` / `signage` / `numbers` /
> `uniform` / `badge` / `gavel` / `courtroom` / `bars` / `handcuffs` を**一語も書いていません**。禁止語は
> `[NEG]` 側にだけ置きます。拡散モデルは本文中の否定形（"no signage"）をしばしば無視して逆に描くためです。
> v001 の本文には "no signage" "no lettering" "grey texture"（= `text` を含む）が散在していました。v002 では
> すべて排除し、印字は `dissolved to soft grey banding` と表現しています。**この語を書き換えないでください。**

---

## 3. 命名と保存先

- ファイル名 `G001.png` … `G222.png`。**欠番を作らない。重複させない。**
- 保存先 `H:\pd-media\assets\ai\greene\`。
- 長辺 3840px 以上・16:9・PNG。

---

## 4. 区分と枚数（合計222枚）— **台本の実測語数から導出**

`EP62_greene_script.en.v002.md` を機械カウントした語数（ナレーション行のみ。`【】`ディレクション・
`⟨HELD⟩`・見出し・注記を除外）：**合計 5,318語**。

**HOOKは特例です。**オーナー決定により HOOK は**約8秒のフラッシュフォワード**になりました
（`PD_ONE_PASS_PRODUCTION_SPEC.v2.md` 行9）。よって HOOK の枚数は語数比例では決めません。
**本編最強のビートから5枚**を選び、それを冒頭に置きます（詳細は §5 HOOK 冒頭の回収表）。
台本の HOOK 区分はコーディネーターが別途書き直します。**この発注は書き直しを待たずに着手できます。**

まず 222 − PEOPLE 10 − THUMB 3 = **209枚**。そこから HOOK 5・OP 4・ENDING 14 を先に確定し、
残り **186枚**を ACT_1–ACT_5 に語数比例（≒26語/枚）で配る。

| 区分 | 台本語数 | 全体比 | 比例値 | **確定枚数** | 語/枚 | ID範囲 |
|---|---:|---:|---:|---:|---:|---|
| HOOK（約8秒・特例） | 142 | 2.67% | — | **5** | — | `G001`–`G005` |
| OP | 51 | 0.96% | 2.0 | **4** | 12.8 | `G006`–`G009` |
| ACT_1 | 1,006 | 18.92% | 38.7 | **39** | 25.8 | `G010`–`G048` |
| ACT_2 | 664 | 12.49% | 25.6 | **27** | 24.6 | `G049`–`G075` |
| ACT_3 | 836 | 15.72% | 32.2 | **32** | 26.1 | `G076`–`G107` |
| ACT_4 | 871 | 16.38% | 33.5 | **33** | 26.4 | `G108`–`G140` |
| ACT_5 | 1,456 | 27.38% | 56.0 | **55** | 26.5 | `G141`–`G195` |
| ENDING | 292 | 5.49% | 11.5 | **14** | 20.9 | `G196`–`G209` |
| — 小計 | 5,318 | 100% | — | **209** | | |
| PEOPLE | — | — | — | **10** | | `G210`–`G219` |
| THUMB | — | — | — | **3** | | `G220`–`G222` |
| **合計** | | | | **222** | | `G001`–`G222` |

配分の調整理由（比例値からのズレはここだけ）：

- **HOOK 5**：8秒 ÷ 約2秒刻み ＝ 4カット。ループ末尾ぶんを足して5枚。v001 は12枚でした。
  浮いた7枚は ACT_1 +2 / ACT_2 +1 / ACT_3 +1 / ACT_4 +1 / ACT_5 +2 に配り直し済み。
- **OP 4**：15秒・51語。無地テクスチャのみで、意味のあるモチーフを消費しない。**最も薄い区分**。
- **ACT_2 +1.4**：ここが「掲示という機構」そのものの章で、**仕込み物（テープ）が置かれる章**です。
  画鋲・テープ・一度きりの訪問・リセットビートと、実物の点数が最も要ります。
- **ACT_5 −1.0**：語数は最大ですが、内容の比重が長い引用と対比（多数意見 対 反対意見）に寄るため、
  1枚あたりの持ち時間を長く取れます。
- **ENDING +2.5**：最後の4枚（`G206`–`G209`）が**同一ドアの4段階**で、台本の
  「その紙がまだそこにあるという、たった一つの仮定」を段階で見せるため。

---

## 5. プロンプト（各1枚）

### HOOK（約8秒・5枚・`G001`–`G005`）— **本発注で最も強い5枚。手を抜かない。**

これは最初の8秒に出る絵です。**視聴者がこの映画で最初に見る5枚であり、離脱の半分はここで決まります。**
フラッシュフォワードなので、**5枚とも本編の後段でもう一度使われます**（約束と回収）。
下の表の「回収先」は編集側の再カット指示です。**画像の生成は1プロンプト1枚のまま**で、
同じ絵を2枚作る必要はありません。

| プレート | 何を約束するか | 回収先（本編での再カット） |
|---|---|---|
| `G001` | ドアに貼られた紙そのもの＝マクロ・ループ | ACT_2 `G059` の直前／ENDING `G206` |
| `G002` | 子どもの手が角にかかる＝事件の核心 | ACT_3 `G082` の直前 |
| `G003` | 紙が消えテープと破れた角だけが残る＝結論 | ACT_3 `G084`／ENDING `G203` |
| `G004` | 同じドアが延々続く通路＝これは3戸の話ではない | ACT_2 リセットビート `G067`／ACT_4 `G119` |
| `G005` | 証言録取の部屋＝この事件を決めた場所 | ACT_3 冒頭 `G076` |

- `G001.png`
A blank sheet of plain paper taped square to a painted apartment door, shot dead on from one metre in flat overcast light, the lower left corner lifted a centimetre clear of the paint and holding there [STYLE] Avoid: [NEG]
- `G002.png`
A small hand entering from the bottom edge of frame and closing on the free corner of a taped blank sheet, shot from the side at thirty centimetres, the rest of the child outside the frame and the painted door filling everything else [STYLE] Avoid: [NEG]
- `G003.png`
The same painted door twenty minutes later, bare except for two strips of adhesive tape and the two torn white corners still held under them, shot dead on from one metre in the same flat overcast light [STYLE] Avoid: [NEG]
- `G004.png`
A hundred metres of open-air walkway on a two-storey brick block, shot from waist height at one end with a long lens so the identical closed doors stack and compress into one another, a single small pale rectangle of paper on a door far down the line, nobody on it, eleven in the morning [STYLE] Avoid: [NEG]
- `G005.png`
Two wooden chairs facing each other across a plain table in a bare room, one of them pushed back at an angle, a jug of water sweating between them, shot from the open doorway in cold north light [STYLE] Avoid: [NEG]

### OP（15秒・4枚・`G006`–`G009`）— ブランド。無地。

台本51語のみ。ここは**ブランド用の無地素材**で、意味のあるモチーフを消費しない。

- `G006.png`
A flat expanse of painted breeze-block wall filling the frame, shot square on in even overcast light, a single hairline crack running from the top edge to the bottom [STYLE] Avoid: [NEG]
- `G007.png`
The torn edge of a sheet of ordinary paper at extreme magnification, lit from one side so the raised fibres throw their own small shadows, plain grey ground behind [STYLE] Avoid: [NEG]
- `G008.png`
Weathered brick in hard raking side light at the end of the afternoon, the mortar joints picked out in relief, no window and no corner of the building in frame [STYLE] Avoid: [NEG]
- `G009.png`
A painted door surface filling the frame from twenty centimetres, the paint chipped through to the primer in two places, one dry rectangle of old adhesive residue still showing where something was held there for years [STYLE] Avoid: [NEG]

### ACT_1（1:05–6:45・39枚・`G010`–`G048`）

台本ビート：1975年・公社が3人に手続き開始 → 記録は名前と住所しか残していない（年齢も職も家族も無い）→
FED（略式占有回復）は速さが目的 → 送達は保安官事務所 → 代執行者は記録上「名前が無い」 →
一方は3人、他方は住宅公社・郡保安官・州法 → 全部を State がやった → ⟨HELD⟩ だから憲法問題になった →
"as applied" → 略式立ち退きが人に要求するもの（日付・出廷・仕事を休む・子どもを預ける）→
その前提が notice → Grannis 1914 / Mullane 1950 → 454.030 の三文 → 三段の梯子 →
真ん中の段（16歳以上の家族・説明して手渡す＝玄関先の会話）→ 最後の一文（開廷の日時と場所）→
上告人の説明する梯子 → 3人とも最下段まで行った・玄関先の会話はゼロ → 最高裁はその説明を採らなかった

- `G010.png`
A low-rise brick public housing development seen from across an open lawn on a flat grey morning, shot from ground level with a long lens so the blocks flatten into a single plane [STYLE] Avoid: [NEG]
- `G011.png`
Two parallel brick blocks with a strip of worn grass between them and washing lines strung across it, shot from the gap at one end so the lines run away from the camera, nobody about [STYLE] Avoid: [NEG]
- `G012.png`
A view down onto the same development from the rail of an upper walkway, plain cars of the period parked in rows below, morning shadow cutting the frame in half [STYLE] Avoid: [NEG]
- `G013.png`
A painted apartment door from three paces back with the open-air walkway running away empty on both sides of it, flat overcast light and no figure anywhere [STYLE] Avoid: [NEG]
- `G014.png`
A wire tray of blank forms on a plain municipal counter, shot from the public side at chest height, the room behind it bare and unbranded [STYLE] Avoid: [NEG]
- `G015.png`
A metal filing cabinet drawer pulled half open in a dim office, the folders inside plain and unmarked, one shaft of window light lying across the top edges [STYLE] Avoid: [NEG]
- `G016.png`
A card index standing open on a desk, shot from directly above, every ruled card in it entirely empty [STYLE] Avoid: [NEG]
- `G017.png`
An empty brass frame screwed beside a closed office door where a name plate would sit, nothing in it, shot close and slightly below eye level [STYLE] Avoid: [NEG]
- `G018.png`
A kitchen in a modest mid-1970s apartment at eight in the morning, enamel sink, a kettle on the stove, low sun coming through the window and nobody in the room [STYLE] Avoid: [NEG]
- `G019.png`
A living room with a worn sofa and drawn curtains, a table lamp on and the room still dim, shot from the doorway, nobody in frame [STYLE] Avoid: [NEG]
- `G020.png`
A concrete stoop of two steps with a metal handrail worn shiny by use, the door beyond it shut, shot from the walkway at knee height [STYLE] Avoid: [NEG]
- `G021.png`
A desk diary lying open on a plain office desk with both pages blank, half the block of pages turned over, shot from above in flat fluorescent light [STYLE] Avoid: [NEG]
- `G022.png`
A trolley of thin case folders standing in a plain corridor, every cover blank, shot from the far end so the corridor runs away behind it [STYLE] Avoid: [NEG]
- `G023.png`
A clipboard held at waist height with a blank form under the clip and a pen pushed through it, shot from just over the holder's shoulder, no face in frame [STYLE] Avoid: [NEG]
- `G024.png`
A plain sedan of the period at the kerb beside a brick block with the driver's door standing open, shot from the walkway above it, nobody visible [STYLE] Avoid: [NEG]
- `G025.png`
A stack of blank papers held flat under a rubber band on a worn vinyl car seat, shot from the open passenger door in hard midday light [STYLE] Avoid: [NEG]
- `G026.png`
A gloved hand holding a folded blank sheet flat against a painted door, plain dark sleeve, shot from the side at close range, no face and no cuff markings [STYLE] Avoid: [NEG]
- `G027.png`
The empty driver's seat of a period sedan seen through the open door, the vinyl split along one seam and the stuffing showing [STYLE] Avoid: [NEG]
- `G028.png`
A plain dark coat hanging alone on a hook in a bare municipal room, the wall behind it grubby at shoulder height, shot square on [STYLE] Avoid: [NEG]
- `G029.png`
A wide low view of the brick development with a plain civic office block rising beyond its rooflines, shot in the last flat light before dusk [STYLE] Avoid: [NEG]
- `G030.png`
A public counter of the period with its shutter pulled down and a worn wooden ledge in front of it, one overhead strip light still on, nobody there [STYLE] Avoid: [NEG]
- `G031.png`
A statute volume closed on a desk, the boards plain and the spine bare, shot at a low angle so the fore-edge fills the lower half of the frame [STYLE] Avoid: [NEG]
- `G032.png`
A civic corridor of the period with frosted glass doors down one side, shot straight down its length from the far end, nobody in it [STYLE] Avoid: [NEG]
- `G033.png`
A board of hooks holding four worn key rings with most of the hooks empty, shot square on in flat light [STYLE] Avoid: [NEG]
- `G034.png`
An outdoor stairwell of poured concrete seen from the bottom step looking up, the treads chipped and the daylight blowing out at the top [STYLE] Avoid: [NEG]
- `G035.png`
A communal stairwell landing of poured concrete with a low wall, one shaft of flat daylight crossing it at an angle, nobody on it [STYLE] Avoid: [NEG]
- `G036.png`
A heavy stone doorway of a public building shot from outside from six paces in flat winter daylight, the doors shut, the stonework plain and unmarked [STYLE] Avoid: [NEG]
- `G037.png`
An open book resting on a plain reading stand under a single lamp, the print dissolved to soft grey banding with no readable forms [STYLE] Avoid: [NEG]
- `G038.png`
A calendar on a kitchen wall with its grid blank and unreadable, low afternoon light crossing it from the left [STYLE] Avoid: [NEG]
- `G039.png`
A bus stop shelter on an ordinary city street at dawn, empty, the road wet and the sky still blue-grey [STYLE] Avoid: [NEG]
- `G040.png`
A time clock on a workplace wall with its face blank and a rack of plain cards beside it, shot square on under a bare bulb [STYLE] Avoid: [NEG]
- `G041.png`
A pair of very small shoes set side by side under a kitchen chair, shot from floor level with the room falling out of focus behind them [STYLE] Avoid: [NEG]
- `G042.png`
An empty chair drawn up to a plain table in a bare room with the table cleared, shot from the far side in flat window light [STYLE] Avoid: [NEG]
- `G043.png`
A single sheet of plain paper lying alone at the centre of a wide bare wooden floor, shot from standing height looking straight down [STYLE] Avoid: [NEG]
- `G044.png`
An old bound report open flat under a desk lamp late at night, the print dissolved to soft grey banding, the rest of the room dark [STYLE] Avoid: [NEG]
- `G045.png`
A single page held up at an angle in one hand against a window, the print reduced to three soft grey bands, the daylight coming through the sheet [STYLE] Avoid: [NEG]
- `G046.png`
An open front doorway seen from inside a modest apartment with flat daylight beyond it and nobody standing in it, shot from the dim end of the hall [STYLE] Avoid: [NEG]
- `G047.png`
A modest apartment interior in the middle of a working day, the kettle cold, the chairs pushed in, the curtains open, a hard slab of light on the floor and nobody there [STYLE] Avoid: [NEG]
- `G048.png`
A walkway of identical closed doors at midday with three of them carrying a small pale rectangle of paper, shot from waist height at a shallow angle so the three read as a run [STYLE] Avoid: [NEG]

### ACT_2（6:45–10:30・27枚・`G049`–`G075`）

台本ビート：脚注の定義（画鋲・粘着テープ・その他の手段）→ その機構で市民は告知された →
上告人自身の順序 → 「留守なら、相当の割合でそうだが、掲示が直ちに続く」 → forthwith・同じ訪問 →
「二度目の試みの定めが無い」 → 翌朝も5時以降も週末も無い → 「上告人の説明を採らない」 →
⟨HELD⟩ 梯子には段が一つしか無かった → 【リセットビート：通路を4秒ホールド】 →
"a good percentage" は上告人自身の見積もり → 火曜の午前11時にドアの向こうにいる人 →
それでも掲示自体は違憲ではない（多くの場合むしろ singularly appropriate）→
「所有者は自分の物件を見張るものだ」 → 問いは狭まる：この建物の、このドアで、紙は読まれるまで残ったか

- `G049.png`
Extreme close on a brass drawing pin driven through paper into painted wood, shot at ten centimetres, the head bright and the paint split in a star around it [STYLE] Avoid: [NEG]
- `G050.png`
A box of brass drawing pins tipped over on a car seat with the pins spilled across the worn vinyl, hard sun coming through the windscreen [STYLE] Avoid: [NEG]
- `G051.png`
A roll of adhesive tape standing on end on a car dashboard with its cut end lifted and curling, shot at twenty centimetres against a blown-out windscreen [STYLE] Avoid: [NEG]
- `G052.png`
A strip of adhesive tape pulled taut between two fingers and a thumb, shot at close range against a plain dark ground, no face in frame [STYLE] Avoid: [NEG]
- `G053.png`
A drawing pin, a short strip of tape and a bent wire laid side by side on a plain grey surface, shot from directly above in even light [STYLE] Avoid: [NEG]
- `G054.png`
A thumb pressing the corner of a blank sheet flat against a painted door, shot at fifteen centimetres, no face and nothing else in frame [STYLE] Avoid: [NEG]
- `G055.png`
A knuckle arrested a few centimetres from a painted door, shot from the side at close range, no face and no body beyond the forearm [STYLE] Avoid: [NEG]
- `G056.png`
A doorbell push worn smooth in its cracked plastic surround, shot at fifteen centimetres, nothing written beside it [STYLE] Avoid: [NEG]
- `G057.png`
The gap under a closed door seen from outside at floor level with the camera resting on the concrete, darkness beyond it [STYLE] Avoid: [NEG]
- `G058.png`
Two hands pressing tape onto the top corners of a blank sheet against a painted door, shot from just behind and above the hands, no face and no sleeve markings [STYLE] Avoid: [NEG]
- `G059.png`
The same door two seconds later with the hands gone and the blank sheet flat against the paint, shot dead on from one metre [STYLE] Avoid: [NEG]
- `G060.png`
A strip of adhesive tape peeling away from a painted door with half a blank sheet hanging from it, shot from the side so the paper reads as one curl of white against the flat paint [STYLE] Avoid: [NEG]
- `G061.png`
The rear of a plain period sedan pulling away along a kerb beside a brick block, shot from the walkway with a slow shutter so the car smears and the block stays sharp [STYLE] Avoid: [NEG]
- `G062.png`
A wristwatch on a forearm held over a steering wheel, the dial blank and unreadable, shot from the passenger seat in flat midday light [STYLE] Avoid: [NEG]
- `G063.png`
An open-air walkway at eleven in the morning with every door shut, hard overhead light and short black shadows under each threshold [STYLE] Avoid: [NEG]
- `G064.png`
The same painted door in the blue light twenty minutes before sunrise, the pale rectangle of paper already on it, everything else still dark [STYLE] Avoid: [NEG]
- `G065.png`
The same painted door after dark under a single walkway bulb, the paper a hard white shape in the pool of light, nobody on the walkway [STYLE] Avoid: [NEG]
- `G066.png`
A wooden stepladder standing against a bare wall with only one rung left in its frame, shot square on in flat light [STYLE] Avoid: [NEG]
- `G067.png`
A long open-air concrete walkway held straight on and centred from the middle of its width, everything still, flat overcast light, no figure anywhere in it [STYLE] Avoid: [NEG]
- `G068.png`
A page of a brief lying at an angle on a desk with one phrase underlined in pencil, the print dissolved to soft grey banding [STYLE] Avoid: [NEG]
- `G069.png`
An industrial laundry room with the machines tumbling and nobody attending them, shot from the doorway through the steam [STYLE] Avoid: [NEG]
- `G070.png`
A cleaner's trolley parked in an office corridor at night, shot from the far end with only the emergency lighting on [STYLE] Avoid: [NEG]
- `G071.png`
A queue rope threaded between posts in a plain civic waiting area with the chairs behind it empty, shot at the height of the rope [STYLE] Avoid: [NEG]
- `G072.png`
A bed with the covers thrown back in a curtained room in flat daylight, nobody in it, shot from the doorway [STYLE] Avoid: [NEG]
- `G073.png`
The front door of an ordinary suburban house with a blank sheet taped neatly to it and a clipped hedge beside the step, shot from the path in flat daylight [STYLE] Avoid: [NEG]
- `G074.png`
A hand turning a key in a plain cylinder lock, shot at twenty centimetres from the side, no face in frame [STYLE] Avoid: [NEG]
- `G075.png`
A painted door shot dead on in flat light and filling the frame with nothing at all on it, the paint sound and freshly washed [STYLE] Avoid: [NEG]

### ACT_3（10:30–15:10・32枚・`G076`–`G107`）

台本ビート：記録は送達人自身の**証言録取**でできている → 1人目「子どもが剥がす問題？ ああ、さんざん困った」 →
「見たことは？ 剥がすのを見て、貼り直せと言った。あの子らは分かっていない」 → 「大半は Village West だった」 →
2人目（Carter Bacon）「多くはない、一箇所で数回」 → 同じ開発名が別々の録取で出る →
3人目「公社が剥がされると言うので、いつも高い位置に貼っていた」 → ⟨HELD⟩「公社がそう言った」 →
剥がれると知らせた上で貼り続けた → 最高裁の要約「送達人はよく承知していた／稀ではない頻度で撤去された」 →
「よく承知していた」の2語 → 割合は書かなかった（誰も数えていない）→
反対側の証言もある：Gilbert Brutscher「6か月、一度も見ていない」 → 同じ仕事・同じドア・逆の答え →
別の送達人「小さい子の手が届かない高さに貼っていた／苦情も見たことも無い」 →
一握りの男たちが別々の建物で別々に見た → 住人側の主張は狭い（見ていない・占有令状で初めて知った・
控訴期間は過ぎていた）→「claim」「stated」という動詞 → ⟨HELD⟩ 誰もその点を審理していない →
サマリージャジメントで来た事件・確定しているのは慣行のほう

- `G076.png`
A deposition room: a plain table with two chairs facing each other across it and a jug of water between them, shot from the open doorway in cold north light, nobody in the room [STYLE] Avoid: [NEG]
- `G077.png`
A stenotype machine on its stand with a ribbon of blank paper folding into a wire basket, shot from above and behind the keys [STYLE] Avoid: [NEG]
- `G078.png`
A reel-to-reel tape recorder on a plain table with the reels turning and the spools unmarked, shot at close range in low tungsten light [STYLE] Avoid: [NEG]
- `G079.png`
A microphone on a short stand on a plain table pointing across at an empty chair, shot at the level of the tabletop [STYLE] Avoid: [NEG]
- `G080.png`
Two working hands folded together on a table in a plain room with the shirt cuffs pushed back, shot from directly across the table, no face in frame [STYLE] Avoid: [NEG]
- `G081.png`
A glass of water half drunk on a table beside a closed unmarked folder, shot at tabletop level with the room falling away out of focus behind [STYLE] Avoid: [NEG]
- `G082.png`
A small hand at the very edge of frame reaching up toward the bottom corner of a taped sheet, shot from the side at door height, no face and no body visible [STYLE] Avoid: [NEG]
- `G083.png`
A painted door shot at knee height so the taped sheet on it reads from a small child's eye level, the sheet centred and the ceiling of the walkway leaning in above [STYLE] Avoid: [NEG]
- `G084.png`
Two torn paper corners still held under strips of tape on an otherwise bare painted door, shot dead on at forty centimetres [STYLE] Avoid: [NEG]
- `G085.png`
A sheet of plain paper lying face down on a concrete step below a closed door with one edge dark with damp, shot from standing height [STYLE] Avoid: [NEG]
- `G086.png`
Torn scraps of white paper turning over on concrete in the wind, shot with a slow shutter so they smear against the sharp ground [STYLE] Avoid: [NEG]
- `G087.png`
A hand pressing a blank sheet back onto a door higher than before with the arm at full stretch, shot from below and behind, no face [STYLE] Avoid: [NEG]
- `G088.png`
A group of small bicycles left against a brick wall in late afternoon light, no children present [STYLE] Avoid: [NEG]
- `G089.png`
A ball at rest in the corner where two concrete surfaces meet, shot at ground level with the corner running away behind it [STYLE] Avoid: [NEG]
- `G090.png`
A skipping rope lying in a loose loop on a concrete walkway, shot from standing height looking straight down [STYLE] Avoid: [NEG]
- `G091.png`
Chalk marks faded almost to nothing on a concrete slab, a hopscotch grid half washed away by rain, shot from above in flat light [STYLE] Avoid: [NEG]
- `G092.png`
Faint small handprints on a painted wall at low height, shot at a raking angle so they catch the light and stand out from the flat paint [STYLE] Avoid: [NEG]
- `G093.png`
A second low brick housing block seen across a patch of open ground, identical to the first, under a flat white sky [STYLE] Avoid: [NEG]
- `G094.png`
The same second block from the opposite corner in different weather, the grass soaked and the light gone dull [STYLE] Avoid: [NEG]
- `G095.png`
A housing office of the period: a plain counter with a wooden gate set into it, shot from the public side, nobody behind it [STYLE] Avoid: [NEG]
- `G096.png`
A telephone handset lying off its cradle on a plain desk with the cord hanging straight down out of frame, shot close in tungsten light [STYLE] Avoid: [NEG]
- `G097.png`
The same painted door with the blank sheet placed unusually high on it, well above the handle, shot dead on from two metres [STYLE] Avoid: [NEG]
- `G098.png`
An arm at full stretch above head height with the flat of the hand against a painted door, shot from below so the reach fills the frame, no face [STYLE] Avoid: [NEG]
- `G099.png`
A bound transcript closed on a table, its cover plain, shot at a low angle so the block of pages fills the lower half of the frame [STYLE] Avoid: [NEG]
- `G100.png`
A stack of bound transcripts on a shelf with every spine plain, shot square on in flat library light [STYLE] Avoid: [NEG]
- `G101.png`
A single transcript page at an angle with one paragraph marked by a pencil line, the print dissolved to soft grey banding [STYLE] Avoid: [NEG]
- `G102.png`
Two identical unmarked folders lying side by side on a table, one open and one shut, shot from directly above in even light [STYLE] Avoid: [NEG]
- `G103.png`
Six blank pages fanned out across a plain desk, shot from above in flat window light [STYLE] Avoid: [NEG]
- `G104.png`
A doormat with nothing on it, shot from directly above at standing height [STYLE] Avoid: [NEG]
- `G105.png`
The inside face of an apartment door with nothing on it, the paint scratched in an arc near the handle, the hallway behind the camera dim [STYLE] Avoid: [NEG]
- `G106.png`
An interior hallway seen from the back of an empty apartment with the front door standing wide open onto flat daylight, nobody in frame [STYLE] Avoid: [NEG]
- `G107.png`
An empty chair pushed back from a table at an angle as if just left, the rest of the room bare, shot from the far side of the table [STYLE] Avoid: [NEG]

### ACT_4（15:10–20:05・33枚・`G108`–`G140`）

台本ビート：州裁判所で再開する手立てが無い（"thus without recourse"・叩くドアがもう無い）→
連邦地裁へ・§1983 のクラスアクション（レコンストラクション期の法律）→ 求めたのは金でなく宣言的・差止的救済 →
Mullane の最低基準 → クラスアクションである理由（同じやり方の全てのドア）→ **敗訴** →
未公刊の判決 → 依拠したのは1909年の Weber（推定が全部の仕事をしていた）→
それでも地裁は「状況は変わった／争いのない証言／しばしば撤去される」と認めた → それでも合憲とした →
「最後の手段は本当に最後の手段だ」という同じ仮定 → 第6巡回区が破棄し Weber を覆した
（「掲示が郵便より確実だった時代はあったかもしれない。その時代は過ぎた」）→
差し戻し（決着ではない）→ 費用の算術「過度の負担にならない・費用は最小限」 →
ニューヨークの対応規定（掲示のときは郵送も）→ 切手一枚の話・別の州はもう買っていた →
1981年に管轄・1982年2月23日弁論・5月17日判決・第81-341号 → 弁論した人々と法廷助言者 →
上告人の譲歩：滞納家賃なら人的送達が必要だった → 金なら人を探す・家ならそうしない →
⟨HELD⟩ 州は、あなたの金を欲しいときのほうが、家を欲しいときより丁寧にあなたを探した

- `G108.png`
A heavy public-building door closed at the top of a flight of stone steps, shot from the pavement in flat daylight, the stonework plain and worn at the nosing [STYLE] Avoid: [NEG]
- `G109.png`
A stone stair rail and worn treads shot from the bottom step looking up, nobody on them, the light dropping away at the top [STYLE] Avoid: [NEG]
- `G110.png`
A wire out-tray on a desk with a single closed folder in it, the office beyond it empty and the overhead light off [STYLE] Avoid: [NEG]
- `G111.png`
A federal courthouse exterior in flat daylight with wide steps and plain columns, shot from across the street with a long lens, the stonework bare [STYLE] Avoid: [NEG]
- `G112.png`
A typewriter on a desk with a sheet in the platen, the typing dissolved to soft grey banding, shot at keyboard level so the keys run away to the paper [STYLE] Avoid: [NEG]
- `G113.png`
A carbon sheet lifted away from a typed page by two fingers, both dissolved to soft grey banding, shot from the reader's side [STYLE] Avoid: [NEG]
- `G114.png`
A nineteenth-century bound statute volume open flat with the pages foxed brown at the edges, the print dissolved to soft grey banding [STYLE] Avoid: [NEG]
- `G115.png`
A legal brief squared on a desk with a paperclip on one corner and the cover plain, shot from above in raking lamplight [STYLE] Avoid: [NEG]
- `G116.png`
A stack of briefs tied together with cotton tape, every cover plain, shot from the side so the string bites down into the paper [STYLE] Avoid: [NEG]
- `G117.png`
A row of law reports on a shelf with the spines identical and plain, shot square on and filling the frame edge to edge [STYLE] Avoid: [NEG]
- `G118.png`
A single volume pulled half out of a shelf of identical volumes, shot slightly below its level so it juts toward the camera [STYLE] Avoid: [NEG]
- `G119.png`
A long view down a whole facade of identical apartment doors receding to a vanishing point, shot with a long lens so the doors stack into one another [STYLE] Avoid: [NEG]
- `G120.png`
A high view over the rooflines of a housing development with the blocks repeating away under flat overcast, shot from an upper landing [STYLE] Avoid: [NEG]
- `G121.png`
A reading desk under a lamp in a library at night with one closed book on it, shot from six paces back so the dark surrounds the pool of light, nobody there [STYLE] Avoid: [NEG]
- `G122.png`
An unmarked folder closed on a desk with the lamp beside it switched off, shot in the last of the window light [STYLE] Avoid: [NEG]
- `G123.png`
A very old bound reporter lying closed on a table, the boards scuffed through at the corners and the spine plain, shot at a low angle [STYLE] Avoid: [NEG]
- `G124.png`
A brick tenement facade of the 1900s in flat light with plain windows, a sepia cast across the whole frame [STYLE] Avoid: [NEG]
- `G125.png`
A horse-drawn delivery cart of the 1900s stopped at a kerb, blurred with movement while the buildings behind stay sharp, sepia cast [STYLE] Avoid: [NEG]
- `G126.png`
Dust turning slowly in a shaft of light above a closed book on a library table, shot against the light [STYLE] Avoid: [NEG]
- `G127.png`
A page with one paragraph bracketed in pencil, the print reduced to soft grey banding, shot at twenty centimetres [STYLE] Avoid: [NEG]
- `G128.png`
Two pages of a bound volume held apart by a thumb, both dissolved to soft grey banding, shot from the reader's side under a lamp [STYLE] Avoid: [NEG]
- `G129.png`
A wooden stepladder lying on its side on a bare floor, shot from floor level down the length of it [STYLE] Avoid: [NEG]
- `G130.png`
An appellate courthouse exterior in plain mid-century stone, wet from rain, shot from the pavement opposite, the facade bare [STYLE] Avoid: [NEG]
- `G131.png`
A plain envelope and a taped blank sheet lying side by side on a plain table, shot from directly above in even light [STYLE] Avoid: [NEG]
- `G132.png`
A file being pushed back across a wooden counter by a hand, shot from the far side at counter height, no face in frame [STYLE] Avoid: [NEG]
- `G133.png`
A bench along the wall of a public corridor with one coat left on it, shot from the far end so the corridor runs to it, nobody waiting [STYLE] Avoid: [NEG]
- `G134.png`
A sheet of postage stamps on a desk with the printing dissolved to flat colour and no readable forms, shot at close range [STYLE] Avoid: [NEG]
- `G135.png`
A postal sorting frame of pigeonholes with most of the compartments empty, shot square on in flat overhead light [STYLE] Avoid: [NEG]
- `G136.png`
A mail sack open on a floor with plain envelopes spilling from it, none of them readable, shot from standing height [STYLE] Avoid: [NEG]
- `G137.png`
A plain white envelope resting on a doormat, shot from directly above with the daylight coming in from the door behind it [STYLE] Avoid: [NEG]
- `G138.png`
The marble steps of a great public building shot straight on from the bottom in flat winter light, empty and bare [STYLE] Avoid: [NEG]
- `G139.png`
An empty lectern in a plain wood-panelled room with no raised bench and no public seating, shot from exactly where a speaker would stand [STYLE] Avoid: [NEG]
- `G140.png`
Coins and folded currency counted out on a plain counter beside a closed unmarked ledger, the denominations not readable, shot from above [STYLE] Avoid: [NEG]

### ACT_5（20:05–28:20・55枚・`G141`–`G195`）

台本ビート：Brennan 判事の法廷意見・基準は1950年の信託受益者通知の事件から（"reasonably calculated,
under all the circumstances"）→ 二つの条件・この事件は後者に生きる → 「重大な財産的利益＝住み続ける権利を
奪われた」 → 十分性は「知らせる能力」で試される・「通常営まれている人の営みへの実際の適用」で判断する →
転回：「このドアに貼るだけでは最低基準を満たさない／相当数の事案で実際の告知に失敗する」 →
⟨HELD⟩「信頼できる手段とは言えない」 → 一度会えなかったことは放棄を示さない →
郵便については比較的・慎重に（効率的で安価／目的物がそのまま宛先である）→ 取ろうとした部屋こそ手紙の届く場所 →
「無効な手段への継続的・排他的依拠」 → 判示（最終命令の前に十分な告知を欠いた＝適正手続なしの財産剥奪）→
誤解される部分：掲示を禁じていない（"we hold only that…"）→ 郵便を命じてもいない・
「郵便が理想の手段からほど遠いことを認めてすら」 → 最も遠くまで行っても「掲示＋郵送のほうが憲法上好ましい」 →
事件は終わっていない（差し戻しの是認・3人が鍵を持って出てきたわけではない・記録はそこで止まる）→
反対意見（O'Connor・首席判事・Rehnquist／票数は書かれていない）→
「今日、法廷は憲法が郵便を選好すると判示する／郵便の速度と信頼性についての証拠は皆無なのに」 →
「唯一の根拠はケンタッキーの一握りの送達人の乏しく矛盾した証言／この脆弱な基礎で立法府の仕事を覆す」 →
「下級審判決以外に一件も引用していない」 → 少なくとも11州 → 同じ三つの節を、一方は条文で、他方は録取で読んだ →
「郵便受けが盗人に荒らされるのは周知の事実だ／掲示は少なくともドアまでは届いたことを保証する」 →
多数意見は郵便が優れていることを証明していない・このドアが劣ることを証明した →
反対意見の第二の攻撃（FED は迅速性が設計そのもの）→ 多数意見の答え「借主の視点からは、相当数の事案で
実際の告知を与えない送達が適切とは考えにくい、その手続が何と呼ばれていようと」 →
対人／対物の分類を決めることを拒んだ → ⟨HELD⟩ 分類は問いではない・紙が何をしたかが問い →
反対意見の最後は制度論 → 多数意見の一行「反対意見は憲法上の基準を読み違えている」 →
⟨HELD⟩ 二つの意見はそこで話すのをやめる

- `G141.png`
A marble corridor of a great public building, plain and empty, shot straight down its length in cold flat light, the walls bare [STYLE] Avoid: [NEG]
- `G142.png`
A bound volume of mid-century reports open flat under a lamp, the print dissolved to soft grey banding, the desk around it dark [STYLE] Avoid: [NEG]
- `G143.png`
A heavy vault door standing part open in a plain stone room, the wheel and dial plain and unreadable, shot from four paces in even light [STYLE] Avoid: [NEG]
- `G144.png`
A ruled ledger lying open on a desk with the columns empty and the entries dissolved to soft grey, shot from above [STYLE] Avoid: [NEG]
- `G145.png`
A plain brass balance at rest and dead level on a bare wooden surface with no ornament on it, shot at its own height so the beam runs across the frame [STYLE] Avoid: [NEG]
- `G146.png`
A set of house keys lying on a bare kitchen counter, shot at thirty centimetres in flat window light [STYLE] Avoid: [NEG]
- `G147.png`
A lit window of a brick block at dusk with the curtains drawn and a single shadow crossing them, shot from the ground with a long lens [STYLE] Avoid: [NEG]
- `G148.png`
The hallway of an occupied apartment with coats on hooks and shoes by the door and a warm lamp on, shot from just inside the front door, nobody in frame [STYLE] Avoid: [NEG]
- `G149.png`
An open-air walkway in the middle of the working day with every door shut, hard light and hard shadow, shot from one end at eye level [STYLE] Avoid: [NEG]
- `G150.png`
A blank sheet taped to a painted door shot dead on and centred from one metre, flat and unmarked, filling the frame [STYLE] Avoid: [NEG]
- `G151.png`
The same door with the sheet gone and two strips of tape left behind on the paint, identical framing and identical light [STYLE] Avoid: [NEG]
- `G152.png`
A single sheet of plain paper falling through still air against a dark neutral ground, caught halfway down with the edges just beginning to soften [STYLE] Avoid: [NEG]
- `G153.png`
An empty open-air walkway at first light with every door bare, everything still, shot from waist height at one end [STYLE] Avoid: [NEG]
- `G154.png`
A bed made up tight in a curtained room at midday, nobody in it, shot from the doorway with the light coming through the curtain [STYLE] Avoid: [NEG]
- `G155.png`
A kettle standing cold on a gas ring in a small kitchen with the window bright behind it, shot at counter height against the light [STYLE] Avoid: [NEG]
- `G156.png`
An adult hand lifting a coat down from a hook beside a front door, shot from the side at shoulder height, no face in frame [STYLE] Avoid: [NEG]
- `G157.png`
A bank of plain apartment mail boxes on a wall with every door shut and no readable markings on any of them, shot square on and close [STYLE] Avoid: [NEG]
- `G158.png`
An unbranded postal van of the period stopped at a kerb with its doors shut, shot from across the road in flat light [STYLE] Avoid: [NEG]
- `G159.png`
A hand posting a plain envelope into a public post box, shot from behind and to one side, no face in frame [STYLE] Avoid: [NEG]
- `G160.png`
A public post box on a street corner in the rain, shot from four paces with the road behind it going soft [STYLE] Avoid: [NEG]
- `G161.png`
A plain envelope halfway through a post slot in a door, shot from inside a dim hallway with the daylight cutting round the edges of it [STYLE] Avoid: [NEG]
- `G162.png`
A front door seen from inside with a plain envelope resting on the mat below it and daylight under the door, shot from halfway down the hall [STYLE] Avoid: [NEG]
- `G163.png`
A painted door carrying a blank taped sheet with an unopened plain envelope on the mat below it, shot from three paces in flat light [STYLE] Avoid: [NEG]
- `G164.png`
A single strip of adhesive tape alone on a bare painted door with nothing held under it, shot dead on at forty centimetres [STYLE] Avoid: [NEG]
- `G165.png`
An interior door standing open onto an empty room in flat daylight, shot from the dim side of the threshold [STYLE] Avoid: [NEG]
- `G166.png`
An empty room with pale rectangles on the wall where pictures used to hang, shot from a corner in flat afternoon light [STYLE] Avoid: [NEG]
- `G167.png`
A bare mattress on a bedstead in an otherwise empty room, shot from the doorway [STYLE] Avoid: [NEG]
- `G168.png`
A kitchen with the cupboard doors standing open and every shelf empty, shot square on from the middle of the room [STYLE] Avoid: [NEG]
- `G169.png`
A blank sheet of paper being folded in half by two hands with both faces of it plain, shot from directly above the hands [STYLE] Avoid: [NEG]
- `G170.png`
The same sheet unfolded and creased, lying flat on a plain table, shot from directly above [STYLE] Avoid: [NEG]
- `G171.png`
A pen held above a blank page and not touching it, shot from the side at close range, no face in frame [STYLE] Avoid: [NEG]
- `G172.png`
A wooden desk drawer pulled open to show plain unmarked stationery, shot from above and slightly in front [STYLE] Avoid: [NEG]
- `G173.png`
A plain envelope in one hand and a blank taped sheet in the other, held at the same height against a plain ground, no face in frame [STYLE] Avoid: [NEG]
- `G174.png`
A file being returned to a gap on an otherwise full shelf, shot from the side at shelf height [STYLE] Avoid: [NEG]
- `G175.png`
A front door seen from deep inside a dim apartment, the band of daylight beneath it the only bright thing in the frame [STYLE] Avoid: [NEG]
- `G176.png`
A single unmarked folder lying alone in the middle of a wide empty table, shot from one end so the tabletop runs away to it [STYLE] Avoid: [NEG]
- `G177.png`
Three empty chairs in a row against a plain panelled wall, shot square on in even light [STYLE] Avoid: [NEG]
- `G178.png`
A page with the lower third left blank below the print, the print dissolved to soft grey banding, shot from above [STYLE] Avoid: [NEG]
- `G179.png`
A plain white envelope alone on a wide dark surface, lit hard from one side so it throws a long shadow across the frame [STYLE] Avoid: [NEG]
- `G180.png`
An empty postal sorting hall at night with the frames of pigeonholes receding away, nobody working, shot down the middle aisle [STYLE] Avoid: [NEG]
- `G181.png`
A thin sheaf of loose pages held edge on between finger and thumb with very few leaves in it, shot against a plain dark ground [STYLE] Avoid: [NEG]
- `G182.png`
A single wooden chair alone in an empty plain room lit from one high window, shot from the far corner [STYLE] Avoid: [NEG]
- `G183.png`
An empty legislative chamber with the seats in curved rows and the walls bare, shot from the back of the highest row [STYLE] Avoid: [NEG]
- `G184.png`
A shelf of bound reporters with one gap in the row where no volume stands, shot square on and close [STYLE] Avoid: [NEG]
- `G185.png`
Eleven plain pebbles laid out in a line on a bare wooden surface, shot from directly above in even light [STYLE] Avoid: [NEG]
- `G186.png`
A plain outline map lying on a table with no borders drawn on it and nothing written, shot from above [STYLE] Avoid: [NEG]
- `G187.png`
A page of three clauses reduced to three soft grey bands, held at an angle in one hand against the light from a window [STYLE] Avoid: [NEG]
- `G188.png`
A mail box with its door forced and hanging open and nothing inside it, shot at close range from slightly below [STYLE] Avoid: [NEG]
- `G189.png`
Plain envelopes scattered loose on the ground beneath a bank of mail boxes, shot from standing height [STYLE] Avoid: [NEG]
- `G190.png`
A hand reaching into an empty mail box, shot from the side at its own height, no face in frame [STYLE] Avoid: [NEG]
- `G191.png`
A single sheet pinned flat against a painted door by a gust of wind with one corner torn free and standing out from the paint, shot dead on [STYLE] Avoid: [NEG]
- `G192.png`
An open-air walkway seen from the far end at dusk with one pale rectangle still on a door, shot with a long lens so the doors compress toward it [STYLE] Avoid: [NEG]
- `G193.png`
A trolley of thin case folders caught mid-movement in a plain corridor, shot with a slow shutter so the trolley smears and the corridor stays sharp [STYLE] Avoid: [NEG]
- `G194.png`
A sorting table with two empty wooden trays side by side and one plain sheet lying between them belonging to neither, shot from directly above [STYLE] Avoid: [NEG]
- `G195.png`
Two closed books lying face to face on a table and touching along their fore-edges, shot at tabletop level with bare wood behind each of them [STYLE] Avoid: [NEG]

### ENDING（28:20–30:00・14枚・`G196`–`G209`）

台本ビート：残ったのは評判より小さく救済より長持ちする「方法」 → 告知したと扱う前に、
その伝え方が実際に機能するかを問え → 答えは証拠の問題・ここでは7〜8人の男の巡回と、公社の一言 →
条文に対して置くには非常に小さな紙の山（反対意見はそう言った）→ それでも他に何も無かった →
条文が書いた梯子は三段・登った男たちは一段と言った → 法廷は実際にドアまで歩いた者の記述を採った →
【コールバック：テープの角】 → 1975年のどこかで、代執行者は塗装されたドアにテープを押しつけ、次の住所へ走った →
紙は敷地上にあった・送達は完了した → その後のすべては、たった一つの仮定から正しく導かれた →
その紙がまだそこにあるという仮定

**`G206`–`G209` は同一のドア・同一の画角・同一のレンズで、光と時間だけを変えた4枚です。**
`G209` は `G001`（HOOK冒頭）と同じ構図でなければなりません。ここでループが閉じます。

- `G196.png`
A wide flat evening sky over the rooflines of a low brick development with no sun visible, shot from the ground so the blocks sit along the bottom edge of the frame [STYLE] Avoid: [NEG]
- `G197.png`
An open-air walkway seen end-on with every door bare, flat morning light, shot from the middle of its width at eye level [STYLE] Avoid: [NEG]
- `G198.png`
A thin pile of loose pages beside a single thick bound volume on a plain table, the pile far the smaller of the two, shot at tabletop level so the difference in height reads [STYLE] Avoid: [NEG]
- `G199.png`
The same thin pile of loose pages alone on the table with the volume gone, identical framing and identical light [STYLE] Avoid: [NEG]
- `G200.png`
A wooden stepladder with three rungs standing against a bare wall, shot square on from four paces in flat light [STYLE] Avoid: [NEG]
- `G201.png`
The same stepladder close in with only the bottom rung left in place, shot at the height of that one rung [STYLE] Avoid: [NEG]
- `G202.png`
A pair of worn work boots at the foot of a concrete stairwell with nobody in them, shot from floor level [STYLE] Avoid: [NEG]
- `G203.png`
The torn top corner of a sheet still held under a strip of tape on an otherwise bare painted door, shot at fifteen centimetres in raking light [STYLE] Avoid: [NEG]
- `G204.png`
A thumb pressing a strip of adhesive tape flat onto a painted door, shot at fifteen centimetres from the side, no face in frame [STYLE] Avoid: [NEG]
- `G205.png`
The rear of a plain period sedan drawing away along a kerb beside a brick block, shot with a slow shutter so the car smears out of the frame [STYLE] Avoid: [NEG]
- `G206.png`
A blank sheet taped square and flat to a painted door, shot dead on and centred from one metre, the walkway behind the camera empty [STYLE] Avoid: [NEG]
- `G207.png`
The same door at dusk with the sheet still on it and one corner lifted by the wind, identical framing and lens [STYLE] Avoid: [NEG]
- `G208.png`
The same door the next morning with the sheet gone and two strips of tape left on the paint, identical framing and lens [STYLE] Avoid: [NEG]
- `G209.png`
The same door in full daylight, entirely bare with the tape gone too, framed exactly as the first image of the film [STYLE] Avoid: [NEG]

### PEOPLE（10枚・`G210`–`G219`）— **全員実在しない一般人。顔が判別できてはならない。**

`people_plates_min: 10`。背中・手・シルエットのみ。台本は Linnie Lindsey / Barbara Hodgens / Pamela Ray に
ついて「三つの名前と共通の住所」以外を何も述べていないので、**特定の誰かに見えてはいけません**。

- `G210.png`
A woman in her thirties in a plain 1970s coat standing at an apartment door with her back to camera and one hand on the handle, shot from six paces down the walkway, her face not visible [STYLE] Avoid: [NEG]
- `G211.png`
The hands of a woman in her fifties holding a folded blank sheet at a kitchen table, shot from directly across the table at tabletop level, no face in frame [STYLE] Avoid: [NEG]
- `G212.png`
A man in his forties in plain work clothes seen from behind at the foot of a concrete stairwell, shot from the walkway above and behind him, his face not visible [STYLE] Avoid: [NEG]
- `G213.png`
A woman's silhouette against a net curtain seen from inside a dim room, her features not resolvable, shot from the far corner of the room [STYLE] Avoid: [NEG]
- `G214.png`
Two adults seated at a kitchen table seen from behind, shoulders and the backs of their heads only, shot from the doorway [STYLE] Avoid: [NEG]
- `G215.png`
A pair of working hands at rest on a formica table top, shot from directly above in flat light, no face and no jewellery [STYLE] Avoid: [NEG]
- `G216.png`
A woman in a plain dress standing at a window with her back to camera looking out at a brick block, shot from the middle of the room in low afternoon light [STYLE] Avoid: [NEG]
- `G217.png`
An adult hand and a child's hand held together at waist height, both cropped at the wrist, shot from the side at close range, no faces in frame [STYLE] Avoid: [NEG]
- `G218.png`
A person in an overcoat walking away down an empty open-air walkway, shot from far behind with a long lens so the figure sits small against the run of doors [STYLE] Avoid: [NEG]
- `G219.png`
The back of a woman's head and shoulders in a hallway facing an open front door, shot from behind at head height, her face not visible [STYLE] Avoid: [NEG]

### THUMB（3枚・`G220`–`G222`）— サムネ候補。**縦横比は16:9のまま。文字は焼き込まない。**

`thumbnail_candidates_min: 3`。見出しを後乗せするため**上1/3を空ける**こと。

- `G220.png`
A single blank sheet of paper taped to a plain painted door, shot dead centre and close under hard directional light from the left, the upper third of the frame left clear [STYLE] Avoid: [NEG]
- `G221.png`
A woman's silhouette on the inside of a drawn curtain with a pale rectangle of paper visible on the door beside the window, hard side light, the upper third of the frame left clear [STYLE] Avoid: [NEG]
- `G222.png`
A torn corner of paper still held under tape on an otherwise bare painted door, shot extreme close under strong contrast, the upper third of the frame left clear [STYLE] Avoid: [NEG]

---

## 5.5 ショート3本のプレートは、この222枚の**内数**です

`SHORTS_SLATE_EP62-65.v001.md` の `short259` / `short260` / `short261` が要求するモチーフを、
上のプロンプトに1つずつ突き合わせた表です。**ショート用の二度目の発注は出しません。**

**★印のプレートはショートに使うため、主題を画面中央に置くこと。** ショートは 1080×1920 なので、
16:9 の左右を切り落としても意味が壊れない構図でなければなりません。生成後の目視では、
**9:16 に切ったサムネイルも並べて確認**してください。端に寄った構図（例：`G082` の画面端の小さな手）は
ショートに使わず、長尺のみに使います。

### short259「通知は剥がれた。貼っていた男たちは知っていた」

| ショートのビート | プレート | 中央配置 |
|---|---|---|
| フック＝frame 0：角の浮いた紙がドアに貼られている | `G001` | ★ |
| 掲示とは物理的に何か：画鋲 / テープの剥がれ | `G049` `G060` | ★ ★ |
| 場所：低層レンガの集合住宅 / 同じドアが並ぶ通路 | `G010` `G004` | ★ ★ |
| 子どもの手が角にかかる / 子どもの目線のドア | `G002` `G083` | ★ ★ |
| 段の下に落ちた紙 / 風に舞う紙片 | `G085` `G086` | ★ ★ |
| 手の届かない高さに貼り直す手 / 腕を伸ばしきった手 | `G087` `G098` | ★ ★ |
| 階段室の踊り場 / 静止した通路 | `G035` `G067` | ★ ★ |
| 灯った窓のカーテンを横切る影 / 網カーテンのシルエット | `G147` `G213` | ★ ★ |
| 証言録取の部屋（椅子2脚） / テープで括られた記録の束 | `G076` `G116` | ★ ★ |
| 落ち：何も貼られていないドア | `G075` | ★ |
| **loop_join**：素のドア → 紙が戻り角が浮く＝frame 0 | `G209` → `G001` | ★ |

distinct = 19（下限16をクリア）。`G209` と `G001` は**同一画角**で作ること。ループはここで閉じます。

### short260「一度叩いて、留守。それで手続きは終わりだった」

| ショートのビート | プレート | 中央配置 |
|---|---|---|
| フック＝frame 0：触れる直前の拳 | `G055` | ★ |
| ドアから見た無人の通路 / 三歩下がったドア | `G063` `G013` | ★ ★ |
| ドアの下の隙間（外から）/ 部屋の奥から見た光の帯 | `G057` `G175` | ★ ★ |
| 真昼の腕時計 / 昼間の無人の部屋 | `G062` `G047` | ★ ★ |
| 勤務中である痕跡：タイムレコーダー / 洗濯工場 / 清掃台車 | `G040` `G069` `G070` | ★ ★ ★ |
| 夜勤明けの空のベッド / 夜明けのバス停 | `G072` `G039` | ★ ★ |
| 空白のカレンダー / 手袋の手が押さえる白紙 | `G038` `G026` | ★ ★ |
| 紙が貼られる / 記録の棚 / 閉じたドアの前の踏み段 | `G058` `G117` `G020` | ★ ★ ★ |
| **loop_join**：ドアから見た無人の通路 → 拳が左から再入場 | `G063` → `G055` | ★ |

distinct = 17。

### short261「反対意見の答え＝郵便受けは荒らされる」

| ショートのビート | プレート | 中央配置 |
|---|---|---|
| フック＝frame 0：へこんだ郵便受けの列 | `G157` | ★ |
| こじ開けられた郵便受け / 空の郵便受けに伸びる手 / 散らばる封筒 | `G188` `G190` `G189` | ★ ★ ★ |
| 玄関マットの封筒 / 郵便車 / 投函する手 / 雨の郵便ポスト | `G137` `G158` `G159` `G160` | ★ ★ ★ ★ |
| 夜の無人の郵便区分室 / 暗い面に置かれた一通 | `G180` `G179` | ★ ★ |
| ラベルの無い地図 / 11個の小石 / 無人の議場 | `G186` `G185` `G183` | ★ ★ ★ |
| 「乏しい証言」＝薄い紙束 / 「一件も引用が無い」＝棚の欠番 | `G181` `G184` | ★ ★ |
| 準備書面の束 / 紙の上に浮くペン | `G116` `G171` | ★ ★ |
| 紙と封筒が両方あるドア（多数意見の到達点） | `G163` | ★ |
| **loop_join**：マットの封筒を手が持ち上げ、背後に郵便受けの列 | `G137` → `G157` | ★ |

distinct = 18。

> **ショート間で共有するプレートは `G116` の1枚のみ**（short259 と short261）。公開は
> `SHORTS_SLATE` §6 のとおり E+1 / E+4 / E+7 と離れているので `footage_diversity` 上の問題はありません。

---

## 6. 生成後にやること（発注者側）

1. **全222枚をラベル付きコンタクトシートで目視**する。プロンプトIDで選ばない
   （short60は3枚がプロンプト一覧どおりに選んで別の絵だった）。
   特に **Q2（紙の上の読める文字）** を全枚数で確認する。紙が写るプレートは約30枚あります。
2. **HOOKの5枚（`G001`–`G005`）は最初に目視する。** ここが弱ければ他が全部良くても映画は死にます。
   5枚とも「これは誰の目で、いつ、どの距離から見た絵か」が一目で言えること。言えなければ作り直し。
3. `episodes/PD-2026-062-greene/episode_spec.v001.json` の `mandatory_stills` は
   **すでに G001〜G222 の222件で埋まっています**。ID体系を変えないでください。変えると
   `check_spec_satisfied.py` の唯一の保護が外れます。
4. 1枚 = 1モーションクリップとして `remotion/public/greene/motion/` に書き出す
   （i2v または深度パララックス。**ズーム/パンだけは不可**＝紙芝居判定）。
5. `python scripts/check_episode_inputs.py --slug greene` で
   **accepted(12) + motion ≥ 234** をレンダー前に確認する。
6. ショート3本は §5.5 の表のプレートを **9:16 に切って**から `remotion/public/shorts/short<NNN>/` へ
   コピーし、`gen_depth_maps.py --dir …` を通す。**二度目の画像発注は出しません。**

---

## 7. ★追加発注（2026-08-04・v002 に後から足した3枚）

設計マニュアル `docs/PD_EPISODE_DESIGN_MANUAL.v001.md` §2① が名指ししている二つのツール
`scan_video_shape.py` と `check_cross_episode_reuse.py` を、この発注書を書いた時点では通していませんでした。
通した結果、greene の実写素材から3本が落ちました。**3本とも高さ720pxで、1080に満たない**ため
コンタクトシートでは絶対に発見できません（`AR-4333439` 1280x720・`AR-5630871` 1126x720・
`AR-6944071` 1366x720）。よって実写採用は **12本 → 9本**、生成枚数は
`distinct_video_assets` 234 − 9 = **225枚**になります。§4 の表と §5.5 のショート対応表は
**一行も変えていません**。`G001`–`G222` は既存のまま、下の3枚だけを足します。

落ちた3本が運んでいたのは**「風」「時の経過」「中に人がいる」**の三つの register で、
これは映画がまだ必要としているものです（`EP62_greene_FILM_BIBLE.v001.md` §3 の紙の七状態のうち
状態3「風に持ち上がる」、および §10「窓の内側の影」）。3枚はその三つを1枚ずつ引き受けます。
**ID は `G223`–`G225` ですが、置かれる区分は ACT_1 / ACT_2 / ACT_4 です**（既存IDを一つも
動かさないため、番号だけが THUMB の後ろに続きます）。生成の順序も保存先も他の222枚と同じです。

| 新ID | 入る区分 | 台本の実ビート（`EP62_greene_script.en.v003.md`） | 引き継ぐ register | 落ちた素材 |
|---|---|---|---|---|
| `G223` | **ACT_1** | 「A member of the defendant's family over sixteen years of age. **Somebody home.**」／「The statute is written for a household with somebody in it.」 | 中に人がいる | `AR-6944071` back view of a man opening the curtains |
| `G224` | **ACT_2** | 【reset beat: motif 3 — wind lifts the sheet, nobody in frame, no narration, 4s】 | 風（誰の意思でもなく） | `AR-4333439` tree leaves dancing with the blowing wind |
| `G225` | **ACT_4** | 「there may have been a time when posting provided a surer means of giving notice than did mailing. **That time has passed.**」 | 時の経過 | `AR-5630871` a curtain with embroidery edges |

- `G223.png`
A net curtain at a ground-floor window held back a hand's width from the inside, only the fingers of one hand at the fabric and no other part of the person in frame, the empty walkway beyond going soft, flat mid-morning light [STYLE] Avoid: [NEG]
- `G224.png`
A scrub tree at the edge of a housing project turned over by a single gust, every pale leaf underside showing at once, shot from below against a flat white sky with no building and no figure in frame [STYLE] Avoid: [NEG]
- `G225.png`
An old embroidered curtain hanging at an apartment window seen from inside, the outer fold bleached almost white by years of daylight and the colour still whole where the fabric has been folded back on itself, shot at close range in flat afternoon light [STYLE] Avoid: [NEG]

**この3枚についての注記**

- `G223` は §5 の `G213`（暗い部屋の奥から見た女性のシルエット）とは**別の絵**です。こちらは
  真昼・手のみ・カーテンの隙間の向こうに無人の通路。ACT_1 の梯子の**真ん中の段**が前提にしている
  「家に誰かいる」を1枚で言うためのものです。ACT_1 の既存プレート（`G018` `G019` `G046` `G047`）は
  全部**無人の部屋**なので、この register は ACT_1 に一枚もありません。
- `G224` はリセットビート専用です。ACT_2 には風のプレートが**一枚もありません**
  （`G191` は ACT_5、`G207` は ENDING）。紙を出さないのは、その2枚と被らせないためです。
  風だけの4秒——「誰も剥がしていないのに剥がれる」を台詞なしで言う画です。
- `G225` は「時間そのものが写っている1枚」です。日に焼けて白く抜けた外側の折りと、
  折り返しの内側に残った元の色。**褪せ方が経過時間を示す**——ENDING の motif 7
  （貼られていた四角い跡が褪せていない）と同じ物理で、ACT_4 の「その時代は過ぎた」に当たります。
- **正直な但し書き。** 残った実写9本のうち3本（`AR-6944084` カーテンを閉める男・`AR-8516592`
  カーテンを横切る人影・`AR-8909763` 窓を見る人）は「中に人がいる」を今も運べます。ただし全て
  **暗い／夜／雨**です。`G223` が埋めるのは**真昼の、代執行者が来る時刻の**在宅であり、そこは空白のままです。
  一方 **「風」と「時の経過」は残り9本に一本もありません**（雪の街灯・破れた網戸・廃屋・空室のパン・
  雨の窓×2・レンガ）。`G224` と `G225` はその二つを丸ごと引き受けます。
- ~~`mandatory_stills` は `G001`–`G225` の **225件**~~ → **古い。現在は 224件**（冗長な内訳は冗頭の★ブロック）。
- レンダー前の確認は **accepted(9) + motion ≥ 234** になります（§6-5 の 12 は 9 に読み替え）。

### ★追加2（2026-08-04・映画の最後の画にプレートが無かった）

再レビューで判明：台本 `EP62_greene_script.en.v003.md` の ENDING 最終行が
`【motif 7: an unfaded square where the paper was】` を指定しているのに、
この発注書には該当プレートが**1枚も存在しない**（`unfaded` の語がファイル全体で0件）。
`G209` は「テープごと消えた完全な無地」で、モチーフ7とは別の状態。
**この1枚が無いと、映画は最後の画を持たないままレンダーされる。**

- `G226.png`
The same painted door in flat daylight, bare, but with a clean rectangle of unfaded paint where a sheet was fixed for a long time and then removed, the surrounding paint faded a shade lighter by weather and sun, framed exactly as the first image of the film, nobody in frame [STYLE] Avoid: [NEG]

合計 **226枚**（G001–G226）。`mandatory_stills` は THUMB 3枚を除いた **223件**。

### ★追加3（2026-08-04・台本 v003 第三パスの修理バッチで確定・**新規プレートは無し**）

`EP62_greene_REREVIEW.v001.md` §8 と `EP62_greene_SECOND_OPINION.v001.md` が、この発注書と台本が
**別々の絵を指している**箇所を三つ挙げた。台本 `EP62_greene_script.en.v003.md` を正典として、
ここで読み替えを確定する。**プロンプト本文は一行も変えない。生成枚数も 226枚のままである。**

**(1) HOOK は 5カットではなく 4カット。**
`PD_SCREENPLAY_STANDARD.v001.md` §16.5（オーナー決定・再議論しない）は **3〜4カット**である。
台本の 【HOOK cuts】 が正典で、採用は `G001` `G002` `G004` `G005` の4枚。
**`G003` は HOOK から外す。**理由は枚数だけではない：`G003`（テープ2本と破れた角だけが残るドア）は
**結論の画**であり、8秒で答えを見せてしまう。`G003` は §5 の回収先どおり ACT_3 `G084` と
ENDING `G203` で使う。**生成は従来どおり必要**（5枚とも作る）。
あわせて台本側の `G004` の説明を「遠くのドアに**紙がまだ貼られている**」と書き直した。
以前の台本は「pale rectangle」とだけ書いており、モチーフ7（褪せていない四角）と読めたが、
`G004` のプロンプトは元から「a single small pale rectangle of paper on a door」＝紙である。
**プロンプトは正しく、台本の記述が不正確だった。**

**(2) ループを閉じるプレートは `G209` ではなく `G206`。**
§5 ENDING の注記「`G209` は `G001`（HOOK冒頭）と同じ構図でなければなりません。ここでループが閉じます」は
**この項で置き換える**。台本 ENDING の 【callback】 はモチーフ1＝**紙が平らに貼られたドア**であり、
`G209`（テープごと消えた完全な無地）は**別の状態**である。したがって：

- ループは **`G206`**（紙が平らに貼られたドア）で閉じる。**`G206` を `G001` と同一画角・同一レンズで作る。**
- 映画の**最後の画**は **`G226`**（モチーフ7・褪せていない四角）。★追加2のとおり。
- ※ **これも撤回（2026-08-04）。`G209` は廃止で、ENDING にも使わない。**代替は `G230`。
- `G206`–`G209` が同一ドア・同一画角・同一レンズという条件は変更なし。

**(3) §5 ENDING のビートブロックは古い台本の写しである。以下に読み替える。**
（プロンプトは変更なし。ビート記述だけが v003 と食い違っている。）

| 発注書の記述 | 読み替え | 理由 |
|---|---|---|
| 「答えは証拠の問題・ここでは**7〜8人の男**の巡回」 | 「**数人の男**（a handful of men）が**自分の仕事**を述べた」 | 判決文は人数を印刷していない。契約のロック「no count of process servers」に違反する。台本からは削除済み |
| 「**巡回**」 | 「**自分の仕事**」 | 判決文に routes / rounds は一語も無い |
| 「登った男たちは**一段と言った**」 | 「登った男たちは、**互いに同じようには述べなかった**」 | 証言は割れている。片方を選ぶと反対意見が消える |
| 「テープを押しつけ、**次の住所へ走った**」 | 「代執行者はドアに令状を**留めた**——**画鋲か、粘着テープか、その他の手段か。判決文はどれとは言っていない**」 | 判決文 n.1 は thumbtack, adhesive tape, or other means としか書かず、このドアで何が使われたかを書いていない。塗装されたドアという記述も無い。**画（`【】`）はテープでよい。ナレーションは断定しない** |
| 「【コールバック：**テープの角**】」 | 「【コールバック：**モチーフ1＝紙が平らに貼られたドア（`G206`）**】」 | (2) と同じ |
| 「残ったのは**評判より**小さく」 | 「残ったのは**一つの規則より**小さく、**一つの救済より**長持ちする」 | 台本はこの事件の「評判」を主張しない（立証していない主張になる） |

**(4) §4 の区分時間は v002 の語数から導出されている。**現行 v003 の実測（176 wpm）は次のとおり。
**ID も枚数も変更しない。**区分境界の目安としてのみ使うこと。

HOOK 25語 0:00–0:09 · OP 25語 0:09–0:17 · ACT_1 1,057語 0:17–6:17 · ACT_2 608語 6:17–9:45 ·
ACT_3 853語 9:45–14:35 · ACT_4 842語 14:35–19:22 · ACT_5 1,645語 19:22–28:43 · ENDING 195語 28:43–29:50 ·
**合計 5,250語 = 29:50**（`runtime_seconds` [1620, 1920] の内側）。

**(5) `mandatory_stills` はこの項では変更しない。**現在 223件（`G001`–`G219` ＋ `G223`–`G226`）で、
★追加2 の `G226` は登録済み。上の三件はいずれも**新規プレートを要求していない**。

### ★再発注（2026-08-04・目視QCの結果、必須）

226枚を全枚目視した（`runs/qc/greene_plate_verdicts_sheets1to6.v001.md` と `...7to12.v001.md`）。
文字規則はほぼ守られていたが、**映画の骨格に関わる欠陥が出た**。

**最重——一枚のドアの連鎖が作られていない。**
この映画のモチーフは「**同じ一枚のドアの七つの状態**」である。しかし実物は：

- `G001` = セージ色の木製パネルドア・**縦長**の紙・テープ**2箇所**・真鍮のノブ
- `G206` = **青緑の平滑なドア**・**横長**の紙・テープ**四隅**（相関 0.741）
- `G207` / `G208` / `G209` = さらに別のドア
- `G226`（**映画の最後の画**）= ドアですらなく奥へ続く外廆下。褐せていない四角は無く、**中ほどのドアに紙がまだ貼られている**（「取り除かれたあと」と正反対）

原因は発注側にある。`G206`以降の文言は「The same door」としか書いておらず、**1プロンプト＝1枚の規則では前の枚を参照できない**。以下はドアの特徴を**毎回全部書き下す**。

| 新 | 置き換え | 内容 |
|---|---|---|
| `G227` | G206 の代替 | モチーフ1 の帰り（ループを閉じる）—— G206 の代替 |
| `G228` | G207 の代替 | モチーフ3 風で持ち上がる —— G207 の代替 |
| `G229` | G208 の代替 | モチーフ5 紙は無く、破れた角とテープだけ —— G208 の代替 |
| `G230` | G209 の代替 | モチーフ6 何も無いドア —— G209 の代替 |
| `G231` | G226 の代替・**映画の最後の画** | モチーフ7 褐せていない四角い跡 —— G226 の代替・**映画の最後の画** |
| `G232` | — | G073 の代替（年代違いの一戸建て） |
| `G233` | — | G140 の代替（紙幣に文字と紋章） |
| `G234` | — | G183 の代替（議場が法廷に見える） |
| `G235` | — | G125 の代替（1900〜1930年代に見える） |
| `G236` | — | G178 の代替（ドローン調・下40%が白飛び） |
| `G237` | — | G121 の代替（平均輝度 12.6・携帯で真っ黒） |
| `G238` | — | G175 の代替（平均輝度 23.5） |
| `G239` | — | G174 の代替（**完全に識別可能な女性の顔**） |

- `G227.png`
A single sheet of plain paper taped flat and square to the SAME door as G001 and no other: a sage-green painted wooden panelled door with a raised outer stile, the paint crazed and flaking to bare wood in two patches at the lock rail, a plain brass knob low at frame left, shot dead-on and square from about one metre in flat overcast daylight, the door filling the frame with a sliver of pale jamb at each side, the sheet PORTRAIT format with two short tabs of masking tape at its top corners only and its whole lower edge lying dead flat against the paint with no curl and no lift anywhere, the sheet blank and its surface bearing no printing of any kind [STYLE] Avoid: [NEG]

- `G228.png`
The same sheet on the SAME door as G001 and no other: a sage-green painted wooden panelled door with a raised outer stile, the paint crazed and flaking to bare wood in two patches at the lock rail, a plain brass knob low at frame left, shot dead-on and square from about one metre in flat overcast daylight, the door filling the frame with a sliver of pale jamb at each side, now lifted clear of the paint along its whole lower edge as if caught by a gust, the two top tabs still holding, dusk light, the sheet blank [STYLE] Avoid: [NEG]

- `G229.png`
the SAME door as G001 and no other: a sage-green painted wooden panelled door with a raised outer stile, the paint crazed and flaking to bare wood in two patches at the lock rail, a plain brass knob low at frame left, shot dead-on and square from about one metre in flat overcast daylight, the door filling the frame with a sliver of pale jamb at each side, the sheet gone, and only two short tabs of masking tape left on the paint with a small triangle of torn paper still trapped under each, morning light [STYLE] Avoid: [NEG]

- `G230.png`
the SAME door as G001 and no other: a sage-green painted wooden panelled door with a raised outer stile, the paint crazed and flaking to bare wood in two patches at the lock rail, a plain brass knob low at frame left, shot dead-on and square from about one metre in flat overcast daylight, the door filling the frame with a sliver of pale jamb at each side, entirely bare, the tape gone too and only a faint adhesive shadow where it had been, full daylight [STYLE] Avoid: [NEG]

- `G231.png`
the SAME door as G001 and no other: a sage-green painted wooden panelled door with a raised outer stile, the paint crazed and flaking to bare wood in two patches at the lock rail, a plain brass knob low at frame left, shot dead-on and square from about one metre in flat overcast daylight, the door filling the frame with a sliver of pale jamb at each side, entirely bare, and where the sheet used to be there is a rectangle of paint a clear shade greener and less chalked than the weathered paint all around it, its edges sharp, the fade differential itself being the subject of the picture, no paper and no tape anywhere in frame [STYLE] Avoid: [NEG]

- `G232.png`
A two-storey brick public housing block of the early 1970s seen from across a strip of worn communal grass in flat overcast light, plain steel doors on a concrete walkway, no vinyl siding, no storm doors, no modern window frames, nobody in frame [STYLE] Avoid: [NEG]

- `G233.png`
A folded rent book and a few worn coins lying on a formica kitchen table under a low lamp, shot close from above, every surface of the book blank and the coins turned edge-on so that no face, no lettering and no device is visible [STYLE] Avoid: [NEG]

- `G234.png`
An empty public meeting room of the period with rows of plain wooden chairs facing a bare front wall, no raised bench, no dais, no seal, no flag, no gallery, flat daylight through high windows [STYLE] Avoid: [NEG]

- `G235.png`
A plain panel van of the early 1970s parked at a kerb on a residential street, unbranded and unlettered, its rear doors shut, overcast light, no horses, no period earlier than 1970 [STYLE] Avoid: [NEG]

- `G236.png`
The same housing development seen from the ground at eye level in flat overcast light, the walkways receding to one side, exposure held so that no part of the frame is blown to white and the concrete keeps its detail [STYLE] Avoid: [NEG]

- `G237.png`
An interior hallway of a modest apartment at night with one door ajar and a light burning beyond it, exposed so the walls and the floor keep their detail and nothing in the frame reads as pure black [STYLE] Avoid: [NEG]

- `G238.png`
A concrete outdoor stairwell seen from the bottom step at dusk, the treads chipped, a bulb burning on the landing above, exposed so the concrete keeps its texture throughout and nothing reads as pure black [STYLE] Avoid: [NEG]

- `G239.png`
A records room of the period with a shelf of unlabelled box files, one person standing at the shelf seen entirely from behind with the back of the head to camera, no part of the face visible at any angle, plain overhead light [STYLE] Avoid: [NEG]

合計 **239枚**（G001–G239）。**既存の G001–G226 は1枚も変更しない**。
置き換えられた旧プレートは削除せず、**そのビートでは使わない**だけとする
（※ **これは撤回。`G206`–`G209` は景観カットとしても使わない。**同じドアに見えない別のドアが画面に出ること自体がモチーフを壊すからである。）

**`mandatory_stills` は再導出が必要**：G227–G239 を加え、カットに入らなくなった旧プレートを外すこと。

### ★追加（2026-08-04・サムネ用の G240）

`thumb_prompts.v001.md` の第4候補。既存の THUMB 3枚（`G220`–`G222`）は**3枚とも寄りで低照度**で、thumbnail_visibility（平均輝度33以上）を確実に満たす明るい引きの候補が1枚も無い。この1枚で埋める。

**この1枚はパッケージング専用で、本編のカットには入らない。したがって `mandatory_stills` には追加しない**（check_spec_satisfied.py は「宣言された静止画がどのカットにも無い」で落ちる）。

下の本文は **展開済みの完全形**。`[STYLE]` の low contrast / low-key をこの1枚に限って打ち消しているので、**`[STYLE]` トークンに戻さないこと**。

- `G240.png`
A long run of identical apartment doors along an open-air concrete walkway seen down its length under bright flat overcast daylight, one single pale rectangle of paper on one door far down the line, the concrete and the painted doors bright and clearly separated, the upper third of the frame left clear, bright even key light, the subject clearly separated from the ground, deep blacks kept but the subject held well above mid-grey, high micro-contrast, cinematic still, muted natural colour, flat humid Ohio Valley light, soft falloff toward the edges, shallow depth of field, restrained documentary framing, mid-1970s to early-1980s American public housing period detail, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage. Avoid: text, lettering, numerals, handwriting, signatures, seals, emblems, logos, signage, house numbers, street signs, police uniform, sheriff badge, patrol car, courtroom interior, gavel, judge's bench, prison bars, razor wire, handcuffs, furniture on a pavement, people being evicted, crying, a hand on a shoulder, golden hour, sunset glow, postcard scenery, drone shot, cosy fireplace, Christmas, tropical, modern smartphones, modern cars, flat CGI, cartoon, illustration, oversaturated.

### ★再発注 2（2026-08-04・状態1 が存在しない）

再レビューで R6 が落ちた。`G001` の本文は *the lower left corner lifted a centimetre clear of the paint* で、**これは状態1（平らに貼られた直後）ではなく状態2 である**。
つまりこの映画は **七つの状態の最初の一歩（平ら→浮き始める）を一度も映さない**まま進んでいた。
紙が剥がれていくというこの映画の論旨そのものの出発点が欠けている。

**`G241` は HOOK の1枚目であり、`G227` と**同じ構図・同じドア・同じ平らさ**でなければならない。** ループはこの2枚が重なって初めて閉じる。
`G001`（角が浮いている）は廃棄せず、**状態2 として HOOK の2枚目に回る**。

- `G241.png`
A single sheet of plain paper taped flat and square to the SAME door as G001 and no other: a sage-green painted wooden panelled door with a raised outer stile, the paint crazed and flaking to bare wood in two patches at the lock rail, a plain brass knob low at frame left, shot dead-on and square from about one metre in flat overcast daylight, the door filling the frame with a sliver of pale jamb at each side, the sheet PORTRAIT format with two short tabs of masking tape at its top corners only, the paper lying dead flat against the paint across its whole surface with no curl, no lift and no shadow under any edge, the sheet blank and its surface bearing no printing of any kind [STYLE] Avoid: [NEG]
