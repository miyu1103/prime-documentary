# EP65 marmet — Codex 画像生成 **1本で完結する発注** v001（219枚・1プロンプト1枚）

> ⚠ **2026-08-04 追記：末尾に §7 として4枚(R220-R223)を追加しました。R001-R219 は変更ありません。**

> ## ✅ 今すぐ着手してよいファイルです。**追加バッチは出ません。**
> EP60はバッチが5本に膨らみました。原因は3つとも同じで、**発注時点で構造が決まっていなかった**
> ことです。今回は逆順にしました。**実写を先に測り（57本取り込み・全タイル目視・使えるのは15本）、
> 台本の実語数を数え、8区分に比例配分し、区分ごとに枚数を確定させてから**この発注を書いています。
> **どの区分にも絵があります。**下の §4 の表がその証明です。
> 枚数の根拠は `EP62_65_IMAGE_BUDGET.v001.md`：契約 `distinct_video_assets` 234 − 実写採用15 = **219**。

**題材:** *Marmet Health Care Center, Inc. v. Brown*, 565 U.S. 530 (2012)（per curiam）と、
差戻し後の西バージニア州最高裁 *Brown II*（229 W. Va. 382, 2012-06-13）。
西バージニアで、3つの家族が入所の受付で、患者本人に代わって入所契約に署名した。
その紙は**すべての紛争を仲裁に送り、ただ一つだけ例外を置いていた** —— 施設側が延滞金を取り立てる請求。
死をめぐる紛争は私設の仲裁人へ、未払いの請求書は裁判所へ。

**この映画は「悪徳介護施設」の話ではありません。**主役は**受付の机に置かれた一枚の紙**です。
判決文は5ページで、患者3人について書かれているのは2文だけ。
**その空白を絵で埋めてはいけません。**埋めるのは紙・机・ペン・廊下・冬の窓であって、人の苦しみではありません。

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**
3. **「良いのが出るまで回す」を禁止する。**
4. 作り直してよいのは §1 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。

EP60はこの規則で **279枚・変種0・指定外0・sha256重複0・知覚的近似重複0** を達成済み。

### 0.5 絵の水準（オーナー指示 2026-08-04）

このシリーズの工芸基準は**アカデミー／パルムドール級の脚本水準**に置かれました。画像側の意味は一つです。

- **カタログ写真を作らない。** 「机」「廊下」「窓」ではなく、**どの光で・どの距離から・どの瞬間を**見るのかを
  書いてあります。プロンプトの副詞句（`at four in the afternoon` / `from where a visitor would stand` /
  `the cushion pressed flat by long use`）は装飾ではなく**指定**です。削らずに生成してください。
- **視点のない絵は不合格。** きれいだが誰も立っていない絵より、平凡だが**誰かの目の高さ**にある絵を採ります。
- **象徴を足さない。** 天秤・砂時計・崩れる書類の山。この映画にはどれも要りません。

---

## 1. ★絶対条件（触れた絵は使用不可）

`episodes/PD-2026-065-marmet/episode_spec.v001.json` の `forbidden_subjects` がこの節の正典です。

- **3人の患者を描かない。** 本人・その怪我・その死・その介護。一切。判決文が書いていないものを絵にしない。
- **人が寝ているベッドを描かない。** 人工呼吸器・点滴・酸素マスク・モニタ波形・注射器・薬。
  **臨床の場面はこの映画に一つも要りません。**（棚の臨床映像を却下したのと同じ理由です）
- **医療スタッフを描かない。** 白衣・スクラブ・聴診器・名札・制服。名前や性格を持った職員は登場しません。
  受付の向こう側は**空**です。手が写る場合も、袖は無地・記章なし・顔なし。
- **実在と特定できる施設を描かない。** Marmet も Clarksburg も描きません。看板・紋章・特徴的な建築で
  場所が割れる絵は不可。**平凡な低層レンガの施設**であること。
- **読める文字・数字・署名・印章・ロゴを描かない。**
  > ### ★このバッチで最も事故が起きるのはここです★
  > この話の主役画像は**署名欄**です。生成器は「署名」と書くと必ず筆記体の英字を描きます。
  > **署名は次の2通りでしか描いてはいけません。**
  > **(a) 罫線だけの空欄**（まだ何も書かれていない）、
  > **(b) 文字として読めない一筆のインクの痕**（うねり1本。字に見えたら不合格）。
  > もしくは **(c) ペンだけを写す**。プロンプトに `signature` という語を一切書いていないのは意図的です。
  > 紙の上の印刷も同様に、**灰色の帯・灰色の面**として描き、行や単語に見えないところまで潰します。
- **法廷内観・木槌・判事席を描かない。** 棚の法廷映像は24本中23本を使い切っており、絵も作りません。
  **裁判所は外観のみ可。**（`R187` `R200` の「執務室」は机と椅子だけの部屋であり、法廷ではありません）
- **監獄を描かない。** 鉄格子・有刺鉄線・独房・手錠。この話は収監の話ではありません。
- **お金を描かない。** 紙幣・硬貨・札束。棚の money-stock を却下したのと同じ理由で、絵も作りません。
  「延滞金」は**金**ではなく**紙**で表します。
- **同情の演出を禁止する。** 肩に置かれた手、涙、カウントダウンする時計、寂しげに照らされた老人。
  **老いはこの映画では「気分」ではなく「ただの事実」です。**手、背中、空いた椅子で表します。
- **広告調にしない。** 黄金色の夕陽、絵葉書の風景、クリスマス、南国、ドローンの映え、暖炉のくつろぎループ。
- **黒つぶれさせない。** スマホで見て何が写っているか分かること。

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字がある（**紙の上も含む**）／**署名が字に見える**（許されるのは空の罫線・読めない一筆・ペンのみ） |
| Q3 | 印章・紋章・ロゴ・名札らしきものがある |
| Q4 | 人が寝ているベッド、または人工呼吸器・点滴・モニタ・注射器などの医療機器が写っている |
| Q5 | 医療スタッフらしき人物（白衣・スクラブ・聴診器・制服）が写っている／顔が判別できる |
| Q6 | 法廷内観・木槌・判事席・鉄格子・手錠・紙幣が写っている |
| Q7 | 同情の演出（肩に置かれた手・涙・寂しげに照らされた老人）である |
| Q8 | 施設や建物が実在と特定できる（看板・紋章・特徴的な建築） |
| Q9 | 視点がない（カタログ写真になっている）／広告調である／画面全体が暗すぎる／既存の他話と実質同じ構図 |

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, muted natural colour, flat overcast Appalachian daylight, low contrast, low-key but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing, West Virginia between 2009 and 2012, an ordinary care facility and ordinary domestic interiors, institutional but never clinical, worn unglamorous surfaces, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> text, lettering, numerals, handwriting, legible signature, cursive writing, seals, emblems, logos, signage, name plates, room numbers, a person lying in a hospital bed, hospital bed, ventilator, oxygen mask, IV drip, monitor trace, syringe, medication, nurse, doctor, scrubs, stethoscope, uniform, badge, clinical scene, operating theatre, laboratory, wheelchair, courtroom interior, gavel, judge's bench, prison bars, razor wire, handcuffs, banknotes, cash, coins, scales of justice, hourglass, a hand on a shoulder, a tear, crying, a lonely old person lit for pity, golden hour, sunset glow, postcard scenery, drone shot, cosy fireplace, Christmas, tropical, modern smartphones, laptops, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated

---

## 3. 命名と保存先

- ファイル名 `R001.png` … `R219.png`。**欠番を作らない。**
- 保存先 `H:\pd-media\assets\ai\marmet\`。
- 長辺 3840px 以上・16:9・PNG。

---

## 4. 区分と枚数（合計219枚）— **台本の実語数から比例配分**

配分の根拠は `episodes/_planning/EP65_marmet_script.en.v001.md` の**ナレーション語数の実測**です
（見出し・ロック行・`⟨HELD⟩`・`【…】`を除いた本文のみ／実測合計 **5,434語**）。
219枚から **PEOPLE 10枚**（`people_plates_min`）と **THUMB 3枚**（`thumbnail_candidates_min`）を先に確保し、
残る **206枚**を語数比で最大剰余法により配分しました。

> ### ★HOOKは**8秒**です（オーナー決定 2026-08-04・`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` 行9）★
> 冒頭は60秒の導入ではなく、**約8秒のフラッシュフォワード**です。**最も強い絵を3〜4カット・約2秒刻み**で
> 見せ、決め台詞1本と、開いたままの問いを置いて本編に入ります。台本のHOOK節はオーナーが別途書き直します。
> したがってHOOKには **5枚しか割きません**（比例配分は6枚、上限は5枚）。そのぶんは各ACTへ戻しました。
> **HOOKの5枚は、この219枚のうち最も強い絵でなければなりません。**視聴者が最初に見る5枚です。
> そして **行9の「約束→回収」規則により、HOOKの各プレートは本編のどこかで必ずもう一度出ます**
> （下の回収表）。フラッシュフォワードは本編にある絵しか見せてはいけません。

| 区分 | 秒（目安） | 実語数 | 語数比 | 比例配分 | **確定** | ID範囲 | 中身 |
|---|---|---|---|---|---|---|---|
| HOOK | 0:00–0:08 | — | — | 6 | **5** | `R001`–`R005` | フラッシュフォワード。全編で最も強い5枚 |
| OP | — | 67 | 1.23% | 3 | **5** | `R006`–`R010` | ブランド。無地のテクスチャ |
| ACT_1 | — | 932 | 17.15% | 35 | **35** | `R011`–`R045` | 3つの訴え・2つの施設・1つの州／記録が止まる場所／紙そのもの |
| ACT_2 | — | 1,020 | 18.77% | 39 | **38** | `R046`–`R083` | Brown I の3つの判断／入所日という日／附合契約 |
| ACT_3 | — | 971 | 17.87% | 37 | **37** | `R084`–`R120` | 「まるごと織り上げた」／5ページの per curiam ／vacate |
| ACT_4 | — | 873 | 16.07% | 33 | **33** | `R121`–`R153` | 差戻しの意味／Part Two ／Charleston へ帰る書類 |
| ACT_5 | — | 957 | 17.61% | 36 | **36** | `R154`–`R189` | Brown II ／overrule と reaffirm ／海図も羅針盤もない |
| ENDING | — | 445 | 8.19% | 17 | **17** | `R190`–`R206` | 紙は何だったのか／2つの未解決の問い／ループ |
| PEOPLE | — | — | — | — | **10** | `R207`–`R216` | 人物プレート（顔なし規則・`people_plates_min: 10`） |
| THUMB | — | — | — | — | **3** | `R217`–`R219` | サムネ候補（`thumbnail_candidates_min: 3`） |
| | | **5,434** | 100% | 206 | **219** | | |

> 語数はHOOK書き直し前の実測です。HOOKの169語は8秒へ圧縮されるため語数比から外し、
> HOOKは「枚数上限5」で先に確定させ、残り206枚を **OP以降の5,265語**の比で配ってから
> OPに下駄（+2）を履かせ、その2枚をACT_2とACT_3から1枚ずつ引きました。秒数は台本改稿後に確定します。

### HOOKの約束 → 本編での回収（行9の必須要件）

| HOOKプレート | 何を約束するか | 回収される場所 |
|---|---|---|
| `R001` ペンと読めない一筆 | 「受付で署名した紙」＝この映画の主題そのもの | ENDING `R191` `R192` `R205` `R206`（同一構図で閉じる）／ACT_1 `R035` |
| `R002` 無人の入所受付 | 机の向こう側には誰もいない | ACT_2 `R059` `R060`（同じ机の朝と夕）／ENDING `R190` `R205` |
| `R003` 一つだけ離れた行＝カーブアウト | 「延滞金の請求だけが例外」 | ACT_1 `R036` `R037`（2枚同一・1枚だけ違う紙）／ENDING `R193` `R194` |
| `R004` 窓辺の空いた肘掛け椅子 | 署名しなかった人の不在 | ACT_2 `R075`／ACT_5 `R176`／ENDING `R201` |
| `R005` 手すりのある廊下 | 場所は施設であって病院ではない | ACT_2 `R079`／ACT_5 `R175`／ENDING `R202` |

### 棚が供給できないもの（検索ヒット0・実測）

`armchair` / `care home corridor` / `winter window` / `handrail` / `walking frame` / `stack of documents`
は**全て0件**でした。**入所受付の机・紙・ペン・空いた椅子は、まるごとこちらで作ります。**

逆に**棚が持っているもの**（`runs/qc/marmet_clip_verdicts.v001.json` の採用15本）は、
**汎用の廊下4本・空いた椅子・窓辺の肘掛け椅子1脚・誰もいない食卓・顔を写していない車椅子3本**です。
そのため **車椅子のプレートは1枚も発注しません**（`[NEG]` にも入れてあります）。廊下は
「手すりのある廊下」「二つの扉が向き合う廊下」など**棚の汎用廊下では代替できない具体性を持つものだけ**を
発注しています。

---

## 5. プロンプト（各1枚）

### HOOK（0:00–0:08・5枚） — フラッシュフォワード。**全編で最も強い5枚。**

- `R001.png`
A ballpoint pen lying across the ruled line at the foot of an admission form, and on that line one unreadable stroke of ink that does not resemble any letter, seen from directly above at close range in the flat grey light of a reception counter at four in the afternoon [STYLE] Avoid: [NEG]
- `R002.png`
An admission desk photographed straight on from exactly where a visitor would stand, at waist height, nobody behind it, one form squared on the counter and the chair on the far side pushed neatly in [STYLE] Avoid: [NEG]
- `R003.png`
A page held flat under raking window light: a short block of grey print, then a wide empty gap, then one line of grey standing entirely alone beneath it, no readable letterforms anywhere on the sheet [STYLE] Avoid: [NEG]
- `R004.png`
An empty upholstered armchair turned three-quarters toward a tall window on a white winter afternoon, the cushion pressed flat by long use, the room behind it unlit [STYLE] Avoid: [NEG]
- `R005.png`
A carpeted corridor in a care facility seen from one end at eye height, a wooden handrail running the whole length of the left wall into grey light, every door shut and nobody in it [STYLE] Avoid: [NEG]

### OP（5枚） — ブランド。無地。

- `R006.png`
Five plain sheets of paper stacked and seen edge on at extreme magnification, the edges just out of true, side light picking out each one separately [STYLE] Avoid: [NEG]
- `R007.png`
A flat field of grey pressed card filling the frame, one shallow crease running off centre, the light falling from the left [STYLE] Avoid: [NEG]
- `R008.png`
Paper fibre at extreme magnification, raised and soft on a plain pale ground, the focus falling away at both edges of the frame [STYLE] Avoid: [NEG]
- `R009.png`
A flat overcast sky over the crest of a wooded Appalachian ridge, the tree line a single dark band low in the frame [STYLE] Avoid: [NEG]
- `R010.png`
Worn institutional linoleum in flat overhead light, the pattern rubbed through along one walked path, no walls and no furniture in frame [STYLE] Avoid: [NEG]

### ACT_1（35枚） — 3つの訴え、2つの施設、1つの州。そして紙そのもの。

- `R011.png`
A two-storey brick care facility seen from across a wet car park on a flat grey morning, the whole building held small in the frame, nothing written anywhere on it [STYLE] Avoid: [NEG]
- `R012.png`
The same kind of low brick building from the far side of a county road at dusk, bare trees standing between the camera and it, three windows lit out of twenty [STYLE] Avoid: [NEG]
- `R013.png`
A single-storey care building of a different and plainer make under a white sky, its entrance canopy casting no shadow at all, no lettering anywhere on it [STYLE] Avoid: [NEG]
- `R014.png`
A two-lane state road running between wooded West Virginia hills under low cloud, the surface wet, no vehicle on it in either direction [STYLE] Avoid: [NEG]
- `R015.png`
A county courthouse in flat daylight photographed from the pavement opposite, stone steps and plain columns, no emblems and nothing written on it [STYLE] Avoid: [NEG]
- `R016.png`
A second county courthouse of different stone and different proportion, seen down a narrow main street with parked cars of the period in front of it [STYLE] Avoid: [NEG]
- `R017.png`
A pair of heavy public doors closed, brass push plates worn bright at hand height, the stone around them darkened by rain [STYLE] Avoid: [NEG]
- `R018.png`
A single sheet carrying one short paragraph of grey print and nothing else, lying square on a desk blotter beneath an unlit lamp [STYLE] Avoid: [NEG]
- `R019.png`
The same sheet lifted and held at an angle so the light crosses it, that one paragraph still the only mark anywhere on the page [STYLE] Avoid: [NEG]
- `R020.png`
A wire in-tray on a plain desk with exactly one thin folder in it, seen at desk height from a foot away [STYLE] Avoid: [NEG]
- `R021.png`
A second thin folder set down beside the first, the two closed and identical and unmarked, the desk otherwise bare [STYLE] Avoid: [NEG]
- `R022.png`
A metal filing cabinet drawer pulled out to show a row of identical unlabelled tabs, light from a high window falling across them at an angle [STYLE] Avoid: [NEG]
- `R023.png`
A record room of grey shelving seen straight down its centre aisle, boxes to the ceiling, one strip light out halfway along [STYLE] Avoid: [NEG]
- `R024.png`
A plain closed envelope squared on a desk beside a closed folder, the front of it bare, morning light arriving from the left [STYLE] Avoid: [NEG]
- `R025.png`
A stairwell in a public building seen from the bottom step looking up, painted metal rail, daylight arriving two floors above [STYLE] Avoid: [NEG]
- `R026.png`
A wooden bench in a public corridor outside a closed door, one folded coat left on it, the corridor otherwise empty in both directions [STYLE] Avoid: [NEG]
- `R027.png`
A domestic kitchen in an ordinary West Virginia house at mid-morning, formica table, one mug left out, nobody there [STYLE] Avoid: [NEG]
- `R028.png`
A living room with a worn sofa and the curtains half drawn, a lamp burning in the afternoon because the day never got light [STYLE] Avoid: [NEG]
- `R029.png`
A made bed in a small domestic bedroom, the cover pulled tight and square, a chair beside it with clothes folded on the seat [STYLE] Avoid: [NEG]
- `R030.png`
A hallway with three closed doors off it and a runner rug down the middle, one light on at the far end and the rest in shadow [STYLE] Avoid: [NEG]
- `R031.png`
A pair of house slippers set together on a mat inside a front door, seen from standing height looking down [STYLE] Avoid: [NEG]
- `R032.png`
A coat and a scarf on a hook by a back door, the paint behind them worn through to bare wood by years of the same gesture [STYLE] Avoid: [NEG]
- `R033.png`
A shelf of ordinary household things in flat daylight — a plain jug, a folded cloth, a clock face carrying only its hands [STYLE] Avoid: [NEG]
- `R034.png`
A porch on a modest frame house under an overcast sky, two empty chairs turned slightly toward each other, the yard beyond it plain and unfenced [STYLE] Avoid: [NEG]
- `R035.png`
A pen resting in the gutter of an open ring binder, the pages a soft grey field with no readable marks, close and from directly above [STYLE] Avoid: [NEG]
- `R036.png`
Two identical printed forms laid side by side on a table, both reduced to grey tone, with nothing at all to tell one from the other [STYLE] Avoid: [NEG]
- `R037.png`
A third form laid well apart from those two, visibly shorter than either of them, in the same grey tone [STYLE] Avoid: [NEG]
- `R038.png`
A hand flattening a folded form against a table, the crease still standing up under the palm, plain sleeve, no face [STYLE] Avoid: [NEG]
- `R039.png`
A thick roll of blank forms standing on a counter with a rubber band round the middle of it, close [STYLE] Avoid: [NEG]
- `R040.png`
A closed hardbound volume of state statutes on a desk, its spine plain and unmarked, an unlit lamp beside it [STYLE] Avoid: [NEG]
- `R041.png`
The same volume open at a single short paragraph, the print a grey band, a pencil laid along the gutter [STYLE] Avoid: [NEG]
- `R042.png`
A row of identical bound volumes on a shelf, every spine blank, one pulled half out of the row and left [STYLE] Avoid: [NEG]
- `R043.png`
A legislative chamber standing empty, curved rows of desks receding, no flags and no emblems anywhere in it [STYLE] Avoid: [NEG]
- `R044.png`
The dome of a state capitol seen from far off through winter trees, too distant and too soft to identify [STYLE] Avoid: [NEG]
- `R045.png`
A door standing open at the end of a domestic hallway with nobody holding it, the room beyond bright and empty [STYLE] Avoid: [NEG]

### ACT_2（38枚） — Brown I の3つの判断。入所日という日。附合契約。

- `R046.png`
A tall state judicial building of plain grey stone under low cloud, its steps wide and empty, nothing written on it [STYLE] Avoid: [NEG]
- `R047.png`
Three thick briefs stacked on a desk and tied with cotton tape, the covers blank, side light from a window at the left [STYLE] Avoid: [NEG]
- `R048.png`
A shelf of law reports in matching binding, every spine blank, raking light running the length of them [STYLE] Avoid: [NEG]
- `R049.png`
A hand lifting one volume down out of a full shelf, plain sleeve, no face, the gap opening beside it [STYLE] Avoid: [NEG]
- `R050.png`
A statute volume closed with a paper marker still standing proud of the pages, alone on a bare desk [STYLE] Avoid: [NEG]
- `R051.png`
A page with one line of grey print struck through by a single ruled stroke, seen close, no readable letterforms [STYLE] Avoid: [NEG]
- `R052.png`
An empty lectern in a plain panelled room, no bench and no public seating anywhere in it, one window bright behind [STYLE] Avoid: [NEG]
- `R053.png`
Five empty chairs in a shallow curve behind a plain table in a panelled room, seen from exactly where a speaker would stand [STYLE] Avoid: [NEG]
- `R054.png`
A tall window in a stone public building with rain running down the glass, the town below reduced to grey blocks [STYLE] Avoid: [NEG]
- `R055.png`
A corridor of frosted glass office doors, nobody in it, the floor polished but worn through along the middle [STYLE] Avoid: [NEG]
- `R056.png`
A closed door with a blank brass plate where a name would be, the corridor light falling across it at a slant [STYLE] Avoid: [NEG]
- `R057.png`
Two doors side by side in one wall, one standing open onto light and the other shut [STYLE] Avoid: [NEG]
- `R058.png`
A desk calendar block with its grid blank, half the leaves turned back and creased flat [STYLE] Avoid: [NEG]
- `R059.png`
A reception counter at the start of a working day, a fresh stack of identical forms squared on it, the light still cold [STYLE] Avoid: [NEG]
- `R060.png`
The same counter at the end of the same day, the stack much lower, the light gone flat and grey [STYLE] Avoid: [NEG]
- `R061.png`
A rubber stamp resting face up on an ink pad, the face of it bare, close [STYLE] Avoid: [NEG]
- `R062.png`
A wire out-tray holding one completed form, the print on it a grey field [STYLE] Avoid: [NEG]
- `R063.png`
A drawer of identical blank forms pulled fully out, seen from directly above [STYLE] Avoid: [NEG]
- `R064.png`
A hand sliding a form across a counter toward the camera, plain cuff, no face and nothing pinned to the sleeve [STYLE] Avoid: [NEG]
- `R065.png`
A second hand taking that same form on the visitor's side of the counter, no face [STYLE] Avoid: [NEG]
- `R066.png`
A pen offered across a counter, held out by the barrel, both hands cropped at the wrist [STYLE] Avoid: [NEG]
- `R067.png`
A shallow bowl of plain ballpoint pens standing on the corner of a reception counter [STYLE] Avoid: [NEG]
- `R068.png`
A clipboard held out flat toward the camera, a bare hand and a plain cuff only, the form on it empty [STYLE] Avoid: [NEG]
- `R069.png`
A single page being turned in a thick set of forms, two fingers at the corner, the print a grey wash [STYLE] Avoid: [NEG]
- `R070.png`
An overcoat and a handbag set on a chair beside a reception counter, nobody in the chair [STYLE] Avoid: [NEG]
- `R071.png`
Two visitors' chairs against a corridor wall with a low table between them, both empty, afternoon light across the seats [STYLE] Avoid: [NEG]
- `R072.png`
A wheeled trolley of folded linen parked against a corridor wall, nobody attending it [STYLE] Avoid: [NEG]
- `R073.png`
A door held open from behind by a hand at its edge, the room beyond plain and empty, no face [STYLE] Avoid: [NEG]
- `R074.png`
A tray with two cups on it set down on a low table, both cups full and untouched and going cold [STYLE] Avoid: [NEG]
- `R075.png`
A day room with chairs around all four walls in the middle of the afternoon, every chair empty [STYLE] Avoid: [NEG]
- `R076.png`
A dining table laid for a meal with nobody at it, plain crockery, flat overhead light [STYLE] Avoid: [NEG]
- `R077.png`
A stairwell window in a care building, the ridge outside grey with winter, the glass cold to look at [STYLE] Avoid: [NEG]
- `R078.png`
A folded walking frame standing against a corridor wall, unused, seen at floor height [STYLE] Avoid: [NEG]
- `R079.png`
A handrail turning a corner in a corridor, the wall paint scuffed the whole way along it at hand height [STYLE] Avoid: [NEG]
- `R080.png`
A short flight of interior steps with a rail on both sides, the carpet worn down the middle of every tread [STYLE] Avoid: [NEG]
- `R081.png`
A wall of pigeonholes behind a counter, most of them empty, nothing written on any of them [STYLE] Avoid: [NEG]
- `R082.png`
A telephone handset on a counter, off its cradle and left lying, the cord slack across the surface [STYLE] Avoid: [NEG]
- `R083.png`
Two thin petitions squared side by side on a desk, both covers blank, one lamp lit above them [STYLE] Avoid: [NEG]

### ACT_3（37枚） — 「まるごと織り上げた」。5ページ。vacate。

- `R084.png`
A bolt of plain woven cloth being unrolled across a wide table, the leading fold lifting, low side light raking the weave [STYLE] Avoid: [NEG]
- `R085.png`
The same cloth unrolled flat and filling the frame, the weave sharp and no pattern in it at all [STYLE] Avoid: [NEG]
- `R086.png`
A pair of heavy shears lying open on a table beside a folded length of cloth [STYLE] Avoid: [NEG]
- `R087.png`
A cut edge of cloth fraying, threads standing free of the weave, extreme close [STYLE] Avoid: [NEG]
- `R088.png`
A single thread pulled clear of a woven edge and held taut between two fingers, no face [STYLE] Avoid: [NEG]
- `R089.png`
The bolt half rolled again on an empty table, the light going out of the room [STYLE] Avoid: [NEG]
- `R090.png`
A shelf of unlabelled bound reporters filling the frame, spines identical and blank [STYLE] Avoid: [NEG]
- `R091.png`
Two heavy law books stood open and facing each other across a table, nobody at either of them [STYLE] Avoid: [NEG]
- `R092.png`
A reading desk under one lamp in a library at night, a single closed book on it, nobody there [STYLE] Avoid: [NEG]
- `R093.png`
A wooden library ladder leaning against tall shelves, unattended, dust visible in the lamplight [STYLE] Avoid: [NEG]
- `R094.png`
A hand closing a heavy book, plain sleeve, no face, the pages still settling [STYLE] Avoid: [NEG]
- `R095.png`
A corridor with two plain doors facing each other across it, both shut [STYLE] Avoid: [NEG]
- `R096.png`
A stairwell seen between two floors, the rail turning away below, nobody on it [STYLE] Avoid: [NEG]
- `R097.png`
A neoclassical stone facade in flat overcast light, plain columns, no emblems and nothing written on it [STYLE] Avoid: [NEG]
- `R098.png`
The same facade from below with the steps rising out of frame, the stone dark with rain [STYLE] Avoid: [NEG]
- `R099.png`
A wide flight of stone steps photographed from the top looking down, empty, the street small at the bottom [STYLE] Avoid: [NEG]
- `R100.png`
Five thin sheets held together at one corner and fanned slightly, all of them blank [STYLE] Avoid: [NEG]
- `R101.png`
The same five sheets squared into one thin stack on a bare desk, seen almost edge on [STYLE] Avoid: [NEG]
- `R102.png`
A sheet of paper falling flat through still air against a plain dark ground [STYLE] Avoid: [NEG]
- `R103.png`
A page carrying two short lines of grey print separated by a wide gap and nothing else at all [STYLE] Avoid: [NEG]
- `R104.png`
A single unreadable mark of ink alone in the middle of a blank page, magnified, not resembling any letter [STYLE] Avoid: [NEG]
- `R105.png`
One ruled underline drawn beneath a band of grey print, close, the paper slightly bowed [STYLE] Avoid: [NEG]
- `R106.png`
A pencil laid across an open volume, the page a grey field, the lamp above it switched off [STYLE] Avoid: [NEG]
- `R107.png`
Four identical closed volumes stood upright in a row on a desk [STYLE] Avoid: [NEG]
- `R108.png`
A hand setting a fourth volume down beside three others, no face [STYLE] Avoid: [NEG]
- `R109.png`
A brass handle on a heavy public door, worn bright by use, the paint around it chipped back [STYLE] Avoid: [NEG]
- `R110.png`
A stone corridor with a coffered ceiling, empty, flat daylight arriving from one end only [STYLE] Avoid: [NEG]
- `R111.png`
A wheeled trolley of tied paper bundles standing in a service corridor after hours [STYLE] Avoid: [NEG]
- `R112.png`
A window of a stone building at dusk with one room lit behind it, seen from the street below [STYLE] Avoid: [NEG]
- `R113.png`
A plain wooden desk with one closed folder set exactly at its centre and nothing else on the surface [STYLE] Avoid: [NEG]
- `R114.png`
A blank printed form lying alone on a wide desk, framed square and held still, the room silent around it [STYLE] Avoid: [NEG]
- `R115.png`
The same blank form seen from directly above, the edges of the desk entirely out of frame [STYLE] Avoid: [NEG]
- `R116.png`
A pen laid down beside that blank form, not touching it [STYLE] Avoid: [NEG]
- `R117.png`
A wide grey sky over a river valley in winter, the far bank bare, no built thing anywhere in the frame [STYLE] Avoid: [NEG]
- `R118.png`
An empty panelled room with the lights off and one window burning white [STYLE] Avoid: [NEG]
- `R119.png`
A folded state map lying closed on a table, the folds sharp, nothing printed on the visible face [STYLE] Avoid: [NEG]
- `R120.png`
A wall clock in a plain room carrying its hands and no markings at all on the dial [STYLE] Avoid: [NEG]

### ACT_4（33枚） — 差戻しの意味。Charleston へ帰る書類。

- `R121.png`
A closed envelope travelling back across a desk toward the camera, the front of it bare [STYLE] Avoid: [NEG]
- `R122.png`
A file being pushed back into its own gap on a shelf, a hand at the spine, no face [STYLE] Avoid: [NEG]
- `R123.png`
The same shelf a moment later with the file flush in the row and no mark on it anywhere [STYLE] Avoid: [NEG]
- `R124.png`
A stairway seen from the bottom looking up, plain treads, a rail on one side, daylight at the turn [STYLE] Avoid: [NEG]
- `R125.png`
A door swinging closed on a long corridor, a hand's width of gap left [STYLE] Avoid: [NEG]
- `R126.png`
A bench outside a closed door in a public building, nobody on it, the light coming from a high window [STYLE] Avoid: [NEG]
- `R127.png`
A page with one whole paragraph struck through by a single stroke, the print a grey band, no readable marks [STYLE] Avoid: [NEG]
- `R128.png`
An outline map of a single state on plain paper on a table, no borders drawn inside it and nothing named [STYLE] Avoid: [NEG]
- `R129.png`
Stone steps of a public building in flat daylight, wet from rain, empty from bottom to top [STYLE] Avoid: [NEG]
- `R130.png`
A folder standing open on a desk with nothing at all inside it [STYLE] Avoid: [NEG]
- `R131.png`
The same folder closed and a hand withdrawing from it, no face [STYLE] Avoid: [NEG]
- `R132.png`
A one-page sheet lying beside a thick bound volume, the difference in bulk between them plain [STYLE] Avoid: [NEG]
- `R133.png`
Two identical papers on a table with a third set well apart from them, all in the same grey tone [STYLE] Avoid: [NEG]
- `R134.png`
A rubber band lying loose beside the stack it no longer holds [STYLE] Avoid: [NEG]
- `R135.png`
A calendar page with its grid blank, one square marked only by a pencil ring [STYLE] Avoid: [NEG]
- `R136.png`
A roadside sign post with the plate taken off it, only the empty bracket standing against a grey sky [STYLE] Avoid: [NEG]
- `R137.png`
A two-lane road climbing between wooded ridges under low cloud, going away from the camera and out of sight [STYLE] Avoid: [NEG]
- `R138.png`
A river town seen from a hillside on an overcast day, no landmark in it that could be named [STYLE] Avoid: [NEG]
- `R139.png`
A mail sack standing open on a floor with plain closed envelopes inside it [STYLE] Avoid: [NEG]
- `R140.png`
A row of pigeonholes with one envelope standing upright in one of them [STYLE] Avoid: [NEG]
- `R141.png`
A hand posting a plain envelope through a slot, no face [STYLE] Avoid: [NEG]
- `R142.png`
A doormat inside a front door with one envelope on it, the address dissolved to grey [STYLE] Avoid: [NEG]
- `R143.png`
A wire tray on a counter holding one thin document and nothing else [STYLE] Avoid: [NEG]
- `R144.png`
A desk lamp burning over an empty blotter at night [STYLE] Avoid: [NEG]
- `R145.png`
An office block at night with one room lit, seen from the street below [STYLE] Avoid: [NEG]
- `R146.png`
An overcoat on a stand in the corner of a plain office [STYLE] Avoid: [NEG]
- `R147.png`
A briefcase standing closed against a chair leg [STYLE] Avoid: [NEG]
- `R148.png`
A long plain table with the chairs pushed in on both sides, the room empty and the blinds half down [STYLE] Avoid: [NEG]
- `R149.png`
A jug of water and two upturned glasses on a plain table, nobody in the room [STYLE] Avoid: [NEG]
- `R150.png`
A microphone on a plain table pointing at an empty chair [STYLE] Avoid: [NEG]
- `R151.png`
A ring binder open at a divider tab with nothing filed behind it [STYLE] Avoid: [NEG]
- `R152.png`
A hand pressing a stack of blank sheets square against a desk, no face [STYLE] Avoid: [NEG]
- `R153.png`
A closed door at the end of a corridor with a strip of daylight under it [STYLE] Avoid: [NEG]

### ACT_5（36枚） — overrule と reaffirm。海図も羅針盤もない。

- `R154.png`
A heavy book being closed by two hands, the last page still lifting, no face [STYLE] Avoid: [NEG]
- `R155.png`
A single page taken cleanly out of a stitched binding and set aside, the page blank [STYLE] Avoid: [NEG]
- `R156.png`
The same volume closed with one page gone from the block, the gap visible along the fore edge [STYLE] Avoid: [NEG]
- `R157.png`
A shelf of bound state reporters with one gap in the row, the light falling straight into it [STYLE] Avoid: [NEG]
- `R158.png`
Two chairs of very different heights drawn up to the same plain table [STYLE] Avoid: [NEG]
- `R159.png`
A plank resting across a low block, one end down on the floor and the other in the air [STYLE] Avoid: [NEG]
- `R160.png`
A table with one chair on one side of it and none at all on the other [STYLE] Avoid: [NEG]
- `R161.png`
A folded nautical chart opened out on a wooden table with no places printed on it [STYLE] Avoid: [NEG]
- `R162.png`
A brass compass lying on that open chart, its dial bare [STYLE] Avoid: [NEG]
- `R163.png`
A grey sea horizon in fog with nothing else at all in the frame [STYLE] Avoid: [NEG]
- `R164.png`
A ship's rail with fog beyond it and no shore anywhere [STYLE] Avoid: [NEG]
- `R165.png`
An empty file drawer standing open, the runners bare [STYLE] Avoid: [NEG]
- `R166.png`
A plain hearing room with a table, two chairs and a jug of water, nobody in it [STYLE] Avoid: [NEG]
- `R167.png`
A shuttered service counter with the roller down and a bare ledge beneath it [STYLE] Avoid: [NEG]
- `R168.png`
A door with a blank plate, shut, in a corridor where the lights have been turned off [STYLE] Avoid: [NEG]
- `R169.png`
An office window seen from the street with the blinds down and the room dark behind them [STYLE] Avoid: [NEG]
- `R170.png`
A telephone on an empty desk in an unlit office [STYLE] Avoid: [NEG]
- `R171.png`
A stack of unopened plain envelopes on a hall table [STYLE] Avoid: [NEG]
- `R172.png`
A dust sheet thrown over a desk in a cleared office [STYLE] Avoid: [NEG]
- `R173.png`
A plain reception counter with nothing on it at all and the chair behind it taken away [STYLE] Avoid: [NEG]
- `R174.png`
A hand laying a pen down on a closed folder and leaving the frame, no face [STYLE] Avoid: [NEG]
- `R175.png`
A corridor with a handrail seen from the far end, a window at the near end letting in grey light [STYLE] Avoid: [NEG]
- `R176.png`
An empty armchair with the cushion pressed flat by long use, nobody near it, the room in shadow [STYLE] Avoid: [NEG]
- `R177.png`
A pair of reading glasses folded on a side table beside a closed folder [STYLE] Avoid: [NEG]
- `R178.png`
A window in winter seen from inside with condensation standing across the lower panes [STYLE] Avoid: [NEG]
- `R179.png`
A wooden chair pushed back from a kitchen table at an angle, as if somebody had just got up [STYLE] Avoid: [NEG]
- `R180.png`
A single form on a kitchen table with a mug beside it, the print on it a grey field [STYLE] Avoid: [NEG]
- `R181.png`
A hand turning that form over and finding the reverse blank as well, no face [STYLE] Avoid: [NEG]
- `R182.png`
Two closed folders of unequal thickness set side by side on a desk [STYLE] Avoid: [NEG]
- `R183.png`
A shelf of identical box files with one box missing from the run [STYLE] Avoid: [NEG]
- `R184.png`
A stairwell landing between two floors with a window onto a grey hillside [STYLE] Avoid: [NEG]
- `R185.png`
A county courthouse from across a street in winter, bare trees in front of it, nothing on it to name it [STYLE] Avoid: [NEG]
- `R186.png`
A second courthouse of different stone in the same weather, seen end on from the corner [STYLE] Avoid: [NEG]
- `R187.png`
A plain working desk in a private office of a county courthouse, two thick files set on it and the chair empty [STYLE] Avoid: [NEG]
- `R188.png`
A ledger of ruled columns lying open with every column empty, the ruling grey and faint [STYLE] Avoid: [NEG]
- `R189.png`
A pen standing upright in a jar on an empty desk at the end of the day [STYLE] Avoid: [NEG]

### ENDING（17枚） — 紙は何だったのか。そしてループ。

- `R190.png`
An admission desk seen from the visitor's side in late afternoon light, nobody behind it, one form squared on the counter [STYLE] Avoid: [NEG]
- `R191.png`
A pen lying alone on that counter beside the ruled foot of the form [STYLE] Avoid: [NEG]
- `R192.png`
The ruled line at the foot of the form carrying one unreadable stroke of ink, close, the stroke not resembling any letter [STYLE] Avoid: [NEG]
- `R193.png`
A form with a short paragraph and one separated line below it, held flat under raking light [STYLE] Avoid: [NEG]
- `R194.png`
A shorter form with no separated line at all, laid beside the first one for comparison [STYLE] Avoid: [NEG]
- `R195.png`
A bound volume of federal statutes closed on a desk, the spine plain [STYLE] Avoid: [NEG]
- `R196.png`
The same volume open at one long paragraph, the print a grey band, a thumb holding the page flat [STYLE] Avoid: [NEG]
- `R197.png`
A stone building facade under a flat sky, plain columns, no emblems and nothing written on it [STYLE] Avoid: [NEG]
- `R198.png`
A road running between two counties through winter woods under low cloud [STYLE] Avoid: [NEG]
- `R199.png`
A record room aisle with two boxes set out on the floor at the far end of it [STYLE] Avoid: [NEG]
- `R200.png`
Two empty chairs facing a plain working desk in a private office, the desk cleared [STYLE] Avoid: [NEG]
- `R201.png`
An empty armchair beside a winter window at dusk, the room unlit behind it [STYLE] Avoid: [NEG]
- `R202.png`
A corridor with a handrail at the end of the day, one light left on at the far end [STYLE] Avoid: [NEG]
- `R203.png`
A closed folder on a bare desk with a pen laid across it [STYLE] Avoid: [NEG]
- `R204.png`
A tray with two cups on it, both drunk down and left, on a low table in an empty day room [STYLE] Avoid: [NEG]
- `R205.png`
The admission desk straight on with the form squared on the counter, framed exactly as the opening image [STYLE] Avoid: [NEG]
- `R206.png`
The same desk with the form gone and only the pen left on the counter, the loop closed [STYLE] Avoid: [NEG]

### PEOPLE（10枚） — 人物プレート。**全員実在しない一般人。顔は写さない。老いは気分ではなく事実。**

- `R207.png`
A woman in her sixties in a plain winter coat standing at a reception counter with her back to the camera, face not visible [STYLE] Avoid: [NEG]
- `R208.png`
The hands of a man in his forties resting flat on a counter on either side of a printed form, no face in frame [STYLE] Avoid: [NEG]
- `R209.png`
Two adults seated side by side in corridor chairs seen from behind, only their backs and the backs of their heads in frame [STYLE] Avoid: [NEG]
- `R210.png`
An older person's hands resting on the arms of an upholstered chair, knuckles and veins plain in ordinary daylight, no face and no jewellery [STYLE] Avoid: [NEG]
- `R211.png`
A person in a plain cardigan seen from behind at a window, looking out at a grey hillside [STYLE] Avoid: [NEG]
- `R212.png`
A man's back at the foot of a stairwell with one hand on the rail, face not visible [STYLE] Avoid: [NEG]
- `R213.png`
Two hands, one older and one younger, resting apart from each other on a formica kitchen table, no faces [STYLE] Avoid: [NEG]
- `R214.png`
A figure standing in a doorway against grey daylight, features not resolvable [STYLE] Avoid: [NEG]
- `R215.png`
A woman's hands folded over a closed folder in her lap, seen from above, no face [STYLE] Avoid: [NEG]
- `R216.png`
A person in an overcoat walking away down a corridor with a handrail, seen from far behind [STYLE] Avoid: [NEG]

### THUMB（3枚） — サムネ候補。**縦横比は16:9のまま。文字は焼き込まない。**

- `R217.png`
The foot of a printed form with a plain pen resting across the ruled line, shot dead centre and close, hard directional light, the upper third of the frame left clear [STYLE] Avoid: [NEG]
- `R218.png`
One unreadable stroke of ink on a ruled line, extreme close, strong contrast, the stroke not resembling any letter, the upper third of the frame left clear [STYLE] Avoid: [NEG]
- `R219.png`
An empty armchair beside a winter window with a closed folder on the seat, dramatic side light, the upper third of the frame left clear [STYLE] Avoid: [NEG]

---

## 5.5 ショート3本のプレートは、この219枚の**内数**です

`SHORTS_SLATE_EP62-65.v001.md` の `short268` / `short269` / `short270` が要求するモチーフを、上のプロンプトに
1つずつ突き合わせた表です。**ショート用の二度目の発注は出しません。**各ショートは **16枚以上の distinct plate**
を要求します（`R-A`）。下の表はいずれもそれを満たしています。

| short268「訴えられるのは、向こうが金を取り立てる話だけだった」 | 使うプレート |
|---|---|
| 署名欄＝ペンと読めない一筆（フック＝`frame 0`） | `R001` |
| 無人の入所受付（＝机の向こうに誰もいない） | `R002` |
| 一つだけ離れた行＝カーブアウト | `R003` `R193` |
| ペンの入った器 / 差し出されるクリップボード / めくられるページ | `R067` `R068` `R069` |
| カウンター越しに滑る紙 / 受け取る手 / 差し出されるペン | `R064` `R065` `R066` |
| 朝のカウンターと夕方のカウンター | `R059` `R060` |
| 手すりのある廊下 / 窓辺の空いた肘掛け椅子 / 冬の窓 | `R005` `R004` `R178` |
| 入所書類の束 / 誰もいない食卓 / 背後から押さえられた扉 | `R039` `R076` `R073` |
| 盆の上の2つのカップ（＝落ち） | `R074` |
| ループ結合＝1コマ目に戻る | `R074` → `R191` → `R001` |

| short269「最高裁は一度も『有効だ』と言っていない」 | 使うプレート |
|---|---|
| 戻ってくる封筒（フック＝`frame 0`） | `R121` |
| 棚に戻される書類 / 戻り切った棚 | `R122` `R123` |
| 下から見上げる階段 / 廊下で閉まる扉 | `R124` `R125` |
| 閉じた扉の前のベンチ | `R126` |
| 一段落が一本線で消されたページ | `R127` `R051` |
| 地名のない州の輪郭図 | `R128` |
| 裁判所の石段（**外観のみ**） | `R129` `R099` |
| 空の書類フォルダと、閉じて離れる手 | `R130` `R131` |
| 1ページと厚い巻の対比 / 2枚と離れた1枚 | `R132` `R133` |
| プレートを外された標識柱（＝名前の消えた判断） | `R136` |
| 仕切りの奥に何も無いバインダー / 1通だけの書類受け | `R151` `R143` |
| 廊下の突き当りの扉 | `R153` |
| ループ結合 | `R122` → `R123` → `R121` |

| short270「州の裁判所が『まるごと織り上げた』と書いた」 | 使うプレート |
|---|---|
| 広げられる布地（フック＝`frame 0`） | `R084` |
| 広がった布地の織り目 | `R085` |
| 台の上の裁ちばさみ | `R086` |
| 切り口のほつれ / 引き抜かれた一本の糸 | `R087` `R088` |
| ラベルのない判例集の棚 / 一冊分の空き | `R090` `R157` |
| 向かい合う2冊の法律書 | `R091` |
| 無人の演台 | `R052` |
| 階と階のあいだの階段室 | `R096` `R184` |
| 向かい合う2つの扉の廊下 | `R095` |
| 石造りの正面（外観のみ・見上げと見下ろし） | `R097` `R098` |
| 本を閉じる手（＝落ち） | `R154` `R094` |
| ループ結合 | `R154` → `R089` → `R084` |

> **縦位置の制約。** ショートは 1080×1920 です。上の表に出るプレートは**すべて主題が画面中央にあり、
> 左右を切っても意味が壊れない**構図で発注しています。生成後の目視で、**9:16に切ったサムネイルも並べて確認**
> してください。端に寄った構図が出てしまったプレートはショートに使わず、長尺のみに使います。
>
> **`frame 0` の3枚（`R001` `R121` `R084`）だけは、失敗が即ショート3本の作り直しになります。**
> `R001` は「読める署名」が出たら即不合格。`R084` は布に柄や文字が出たら即不合格。
> この3枚は**中央寄せを厳守**してください。`R001` はHOOKの1枚目でもあり、この発注で最も重要な1枚です。

---

## 6. 生成後にやること（発注者側）

1. **全219枚をラベル付きコンタクトシートで目視**する。プロンプトIDで選ばない
   （short60は3枚がプロンプト一覧どおりに選んで別の絵だった）。
   **特に §1 の Q2（紙の上の文字・署名）と Q4（医療機器）を1枚ずつ潰す。**
2. **HOOKの5枚（`R001`–`R005`）は最初に見て、最初に作り直す。**最初の8秒に出る絵であり、
   ここが平凡なら残り214枚の出来は関係ありません。
3. `episodes/PD-2026-065-marmet/episode_spec.v001.json` の `mandatory_stills` に **R001〜R219 を全部書く**。
   空のままだと `check_spec_satisfied.py` の唯一の保護が無効になります（EP54はここが空で、
   棚に無いから作らせた14枚が完成品から消えたのに誰も気づきませんでした）。
4. 1枚 = 1モーションクリップとして `remotion/public/marmet/motion/` に書き出す
   （i2v または深度パララックス。**ズーム/パンだけは不可**）。
5. `python scripts/check_episode_inputs.py --slug marmet` で
   **accepted(15) + motion ≥ 234** をレンダー前に確認する。
6. 組み立て時、**HOOKの5枚は §4 の回収表のとおり本編でもう一度カットインする**
   （`PD_ONE_PASS_PRODUCTION_SPEC.v2` 行9 の約束→回収）。

---

## 7. ★追加発注（2026-08-04・v001 に後から足した4枚）

**R001–R219 は一枚も変わりません。**この §7 は**追加だけ**です。合計は **223枚**になります。

設計マニュアル §2① が名指しする2つのツールを後から流したところ、**採用実写15本が11本に落ちました。**
`scan_video_shape` が3本（`AR-22240__woman_opening_dark_curtains` 1280x720 /
`AR-8132371__person_sitting_on_wheelchair` 1280x720 / `AR-8543191__people_riding_their_wheelchairs` 1366x720）を
解像度で落とし、`check_cross_episode_reuse` が1本（`AR-2996079__a_dining_room_with_wooden_chairs_and_table`＝**lech で使用済み**）を
話またぎの被りで落としました。**どちらの欠陥もコンタクトシートには写りません。**
契約 `distinct_video_assets` 234 − 実写採用11 = **223**。

**枚数より重いのは、消えた register です。**

- **顔の写っていない車椅子3本のうち2本が消えました。** §4 は「棚がその register を持っているから
  **車椅子のプレートは1枚も発注しない**」と明記しています。**その前提はもう成り立ちません。**
  → `R220` `R221` で作ります。**車椅子には顔を写しません。**
- **誰もいない食卓が消えました。**これは「**そこに誰も座らなかった**」の画でした。
  → `R222`（ACT_1・約4:30 のプラント＝二脚目の椅子）と `R223`（ENDING 最終画＝その椅子の回収）で作ります。
  台本 `EP65_marmet_script.en.v002.md` L60 と L367、`EP65_marmet_FILM_BIBLE.v001.md` §3 の
  **プラント→ペイオフ（距離約26分）**がこの2枚に乗ります。
- `AR-22240` の窓辺（重いカーテンを引いた窓の光）は `R221` が同時に引き受けます。

**§1 の絶対条件は一字も変わりません。**患者を描かない・臨床の場面を作らない・実在と特定できる施設を出さない・
読める文字を出さない。**罫線の上は「空の罫線」か「字に見えない一筆」だけ**であり、
プロンプト本文にその語（署名を表す英単語）は **v001 と同じく一度も書いていません**。

> ### ★`R220` `R221` だけ `[NEG]` を1語だけ外して展開する★
> `[NEG]` には v001 の方針として `wheelchair,` が入っています。**この2枚に限り、その1語だけを削って**展開してください
> （他の語は一切変えない）。**削り忘れると、指定した被写体を打ち消したまま生成されます。**
> `R222` `R223` は `[NEG]` をそのまま使います。

### プロンプト（各1枚・`_02` を作らない）

- `R220.png`
Two empty wheelchairs parked side by side against a corridor wall in a care facility, brakes on and nobody attending them, seen at seated height from a few feet away in flat grey afternoon light, the walls bare of any equipment [STYLE] Avoid: [NEG]
- `R221.png`
A person seated in a wheelchair seen from directly behind at a tall window, only the back of the chair and the shoulders in frame and the face not visible, the heavy curtain drawn back to one side, a grey winter hillside beyond the glass, nothing medical anywhere in the room [STYLE] Avoid: [NEG]
- `R222.png`
An admission desk seen from the visitor's side at waist height with two chairs in the frame, the near one drawn out and turned slightly away, the far one pushed in square and empty, one form squared on the counter between them, the light flat and grey [STYLE] Avoid: [NEG]
- `R223.png`
The foot of an admission form lying on a counter, its ruled line bare and no pen anywhere on it, and beyond the counter and slightly out of focus the far chair still pushed in square, the late afternoon light gone flat [STYLE] Avoid: [NEG]

### この4枚が乗る拍（組み立て側への指定）

| ID | 区分 | 台本の位置 | 役割 |
|---|---|---|---|
| `R220` | ACT_2 | L132「One side of that desk does this every working day. The other side does it once.」 | 施設は人がいなくても続く。**制度の反復** |
| `R221` | ACT_5 | L313–321「There was no evidence to weigh, because nobody had been permitted to take any.」 | 誰も証拠を取らないまま待っている側 |
| `R222` | ACT_1 | L60 のプラント（**ナレーションなし・3秒ホールド**） | 二脚目の椅子。片方は空 |
| `R223` | ENDING | L367 の最終画（モチーフ状態7） | 空の罫線＋**まだ押し込まれたままの二脚目の椅子** |

### 生成後のチェック（§1 の表に追加する1行）

| # | 不合格条件 |
|---|---|
| Q10 | `R220` `R221` に**顔が写っている**／医療機器・点滴・モニタが写っている／車椅子が広告調に演出されている。`R222` `R223` で**二脚目の椅子が引き出されている**（押し込まれたまま・空でなければ不合格） |

`episodes/PD-2026-065-marmet/episode_spec.v001.json` の `mandatory_stills` は
**R001〜R223（223件）**へ更新済みです。

### ★追加（2026-08-04・サムネ用のR224）

thumb_prompts.v001.md の THUMB-D。この話の [STYLE] は low contrast / low-key で、輝度ゲートと正面から衝突する。この1枚は硬いキーライトで発注し、**署名を一切描かずペンだけ**で主題を出す。

**この1枚はパッケージング専用で、本編のカットには入らない。したがって `mandatory_stills` には追加しない**（check_spec_satisfied.py は「宣言された静止画がどのカットにも無い」で落ちる）。

- `R224.png`
A single ballpoint pen lying alone on a bare pale counter, nothing else anywhere in the frame, shot dead centre and close from just above the surface, one hard directional key light from the left throwing a long hard-edged shadow of the pen across the counter, the pen dark against the pale surface, the counter clean and empty, the upper third of the frame left clear [STYLE] Avoid: [NEG]

合計 **224枚**（うち本編 220枚 + PEOPLE 10 + THUMB 4）。
★ **サムネプレートだけは本編の低輝度指定を上書きし、平均輝度38以上・標準偏差45以上を狙うこと。**
