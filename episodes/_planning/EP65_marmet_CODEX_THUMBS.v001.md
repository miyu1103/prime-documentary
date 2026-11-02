# EP65 marmet — Codex 画像生成 **サムネイル専用 再発注** v001（**6枚**・1プロンプト1枚）

> ## ★★★ この6枚は **新規 ID** です。既存ファイルを1枚も上書きしません。 ★★★
> 新しい ID は **`R234`–`R239`** の6つだけ。棚は `R001`–`R233` まで埋まっています（実測: `H:\pd-media\assets\ai\marmet\` に `R001.png`–`R233.png` の233枚）。
> **`R234` より先の番号を勝手に伸ばさないでください。`_v2` も `_02` も作らないでください。**
>
> ## ★★★ 本編の224枚・再発注の9枚（`R225`–`R233`）は一切触りません。 ★★★
> このバッチが触るのは **`R234`–`R239` の6枚だけ**です。

**由来:** 既存のサムネ候補4枚（`thumbnail.marmet.01`–`04.v001.png`）と採用中の `thumbnail.selected.v005.png` を1枚ずつ開いて確認した結果、**5枚とも「ぼかした紙かクリップボードの上に文字を置いた絵」**でした。コピーは強い。**絵が無い。**

機械ゲートはこれを止められません。`check_thumb_subject_luma.py` が測るのは輝度・文字の高さ・縁取りの3つで、**「知らない人がスクロールを止めるか」は測れません。**実測でも全枚が床を越えています（`thumbnail.selected.v005.png` = mean 111.2 / stddev 82.6）。**通っているのに地味**——オーナーが常々言う「サムネが地味でCTRが下がる」はこの状態のことです。

**この6枚に手間をかける根拠（本日の実測）:** このチャンネルの天井は**タイトルではなくサムネ**です。`Enok7A7wGBA` は規則に完全準拠したタイトルで **1,090 impressions / CTR 0.46%**。チャンネル全体の CTR は **1.39%**（目標 4–6%）。タイトルは旧作まで全部書き直したばかりです。**残っているのは絵です。**

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**「良いのが出るまで回す」を禁止する。
3. 作り直してよいのは §1 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。
4. **6枚とも新規ファイル。**既存の `R001`–`R233` を1枚も上書きしない。

### 0.5 なぜ6枚なのか

`episodes/PD-2026-065-marmet/episode_spec.v001.json` の `thumbnail_candidates_min` は **3**（発注時点の実測値。4ではありません）。
既存候補は4枚あって数の上では足りていますが、**4枚とも絵の質で落ちている**ので、数を満たしていることに意味がありません。
**6枚出すのは、目視QCで半分落ちても3枚の床を割らないため**です。

---

## 1. ★絶対条件（触れた絵は使用不可）

正典は `episodes/PD-2026-065-marmet/episode_spec.v001.json` の `forbidden_subjects` です。以下は再掲＋サムネ固有の追加です。**上から順に強い。**

- **人物は入れる。顔も描く。禁じられているのは「実在する特定の人物に似ていること」だけ。**
  完全に架空の一般人であること。有名人・公人・実在の誰かに似せない。
  カメラ目線の作り笑い・広告のモデル顔にしない。**その場にいる人の、作っていない顔。**
  **6枚のうち4枚（`R234` `R236` `R238` `R239`）は人物必須・顔がはっきり見えること。**
- **読める文字・数字・手書き・印章・ロゴを描かない。**
  > ### ★このバッチで最も事故が起きるのはここです★
  > この映画の主役は**受付の紙**です。生成器に「契約書」「書式」と言うと、**必ず紙の上に単語を書きます。**
  > 紙の上の印刷は **「均一で密な灰色の罫線の塊」** としてのみ描いてよい。**行にも語にも見えないところまで潰す。**
  > 文字（見出し・キッカー）は**すべて合成側で後から焼き込みます。**プレートには1文字も要りません。
  > **プロンプト本文に、書かれた名前を表す英単語（sign- 系の名詞）を一語も書いていません。これは意図的です。復活させないでください。**
- **患者・怪我・死・介護・臨床の場面を一切描かない。** 人が寝ているベッド・人工呼吸器・点滴・酸素マスク・モニタ波形・注射器・薬・車椅子。
  **医療スタッフも描かない**（白衣・スクラブ・聴診器・名札・制服）。受付の向こう側は**空**です。
- **実在と特定できる施設・建物を描かない。** Marmet も Clarksburg も描かない。看板・紋章・特徴的な建築で場所が割れる絵は不可。
  **実在の医療ブランド・ロゴ・施設名を一切出さない。実在人物の名前をどこにも書かない。**
- **法廷内観・木槌・判事席を描かない。監獄・鉄格子・手錠を描かない。お金（紙幣・硬貨）を描かない。**
- **同情の演出を禁止する。** 肩に置かれた手、涙、カウントダウンする時計、寂しげに照らされた老人。
- **第三者素材を前提にしない。**すべて生成物1枚で完結すること。**実在の未成年が特定できる絵を作らない。**
- **黒つぶれさせない。**このバッチは**明るさとコントラストが発注の中身**です（§2・§3）。

---

## 2. スタイル（★必ず展開してから生成）

> ### ★本編の `[STYLE]` は使いません（記録された逸脱）★
> `EP65_marmet_CODEX_BATCH_A.v001.md` §2 の `[STYLE]` は本編トーンとして *"flat overcast Appalachian daylight, **low contrast, low-key**"* を課しています。
> **これはサムネの輝度床（§3）と正面から衝突します。**既存候補が地味な直接の原因もここです。
> したがって本書は **サムネ専用の `[STYLE]` を新しく定義**します。`R224` が同じ理由で本編スタイルを外したのと同種の、**記録された逸脱**です。
> **`[NEG]` のほうは逸脱しません**——`EP66_openfields_CODEX_BATCH_C.v001.md` §2 のものを**1語も変えずに**使います。

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, ONE hard directional key light from one side, very high contrast, bright overall exposure, the subject markedly brighter than everything behind it, crisp hard-edged shadows that still hold detail, a plain uncluttered evenly lit pale background, restrained documentary framing, an ordinary American care facility and ordinary domestic interiors in West Virginia between 2009 and 2012, institutional but never clinical, worn unglamorous surfaces, nothing staged for advertising, reads clearly when the frame is shrunk to 320 pixels wide, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結（**EP66 バッチC §2 と1語も違いません**）:

> text, lettering, numerals, digits, house numbers, handwriting, cursive writing, legible signature, seals, emblems, logos, insignia, badge, name plates, readable words on a sign, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, police officer, sheriff, trooper, uniform, patrol car, flashing lights, handcuffs, rifle, shotgun, firearm, holster, dead animal, carcass, blood, taxidermy, mounted antlers, courtroom interior, gavel, judge's bench, prison bars, razor wire, scales of justice, hourglass, a handshake, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, aerial view from above the treetops, golden hour, sunset glow, postcard scenery, autumn colour explosion, Christmas, tropical, modern smartphones, laptops, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

> ### ★`[NEG]` は「人」を禁じていません★
> 禁じているのは **`recognisable person, identifiable person, likeness of a real individual,`**
> **`portrait of a named person, celebrity, public figure, deepfake`** ——**実在の誰かに似ること**だけです。
> **`human face` / `facial features` / `eyes` を絶対に足さないでください。**
> EP65 のバッチAはそれを書いて**人が写ること自体**を止めており、**本日191枚を作り直す羽目になった原因がそれです。**
> `scripts/check_image_order_neg.py` を通過済み（§6）。**1語でも削ったら再実行すること。**

### 2.1 ★EP65 共通の `[NEG]` 追記（6枚すべてに必ず付く）

本編の `[NEG]` が持っていた**臨床・同情・低輝度**の禁止語は、EP66 の `[NEG]` には入っていません。
そこで **6枚すべての `Avoid: [NEG]` の直後に、次の語列をそのまま足します。**（各プロンプト行に**展開済みで書いてあります**。）

```
, hospital bed, a person lying in a hospital bed, ventilator, oxygen mask, IV drip, monitor trace, syringe, medication, nurse, doctor, scrubs, stethoscope, clinical scene, operating theatre, laboratory, wheelchair, room numbers, signage, banknotes, cash, coins, a hand on a shoulder, a tear, crying, a lonely old person lit for pity, wall clock, cosy fireplace, low contrast, low-key, dim interior, underexposed, murky, muddy shadows
```

**正典 `[NEG]` の語を1語も削らないでください。**追記だけが増えます。プレートごとの追加語は §5 の各枚に書いてあります。

---

## 3. 数値でしか書かない（★このバッチの本体）

「かっこよく」「印象的に」では既存の5枚と同じものが出ます。**6枚すべてに、被写体の位置・画面を占める割合・光の来る方向を数値で書いてあります。削らないでください。**

### 3.1 ★見出し帯（6枚すべてに逐語で同じ文が入っています）

EP66 のサムネ4枚は、幹や門柱が**全高を貫いて**見出しを置く場所が無くなり全滅しました（`L255`–`L257` `L259`）。
直し方は「上を空けて」ではなく、**上40%に何が入ってはいけないかを列挙する**ことでした。**本書はその文を、6枚すべてに1文字も変えずに入れてあります。**

```
the ENTIRE UPPER 40% OF THE FRAME an unbroken field of plain, evenly lit, pale bright wall with nothing whatever entering it: no head, no hair, no shoulder, no hand, no door frame, no window, no lamp, no shelf, no picture frame, no cable, no ceiling line, no furniture edge and no horizon line anywhere within that upper 40%
```

### 3.2 ★明るさとコントラストの床（測って落ちたら作り直し）

| 対象 | 指標 | 床 | 測り方 |
|---|---|---:|---|
| **プレート単体**（文字を焼く前） | whole mean luma | **≥ 38** | `PIL ImageStat` の L 平均 |
| **プレート単体** | whole luma stddev | **≥ 45** | 同 標準偏差 |
| **合成後サムネ**（1280×720） | mean luma | **≥ 33** | `check_final_acceptance.py` `THUMB_MIN_MEAN_LUMA` |
| **合成後サムネ** | contrast (luma stddev) | **≥ 40** | 同 `THUMB_MIN_CONTRAST_STD` |
| **合成後サムネ** | subject-region mean luma | **≥ 60** | `check_thumb_subject_luma.py` |
| **合成後サムネ** | tallest connected component | **≥ 150 px**（1280幅換算） | 同（**見出しを焼いた後**にしか意味が無い） |

**プレート段階で意味があるのは上2行と `subject luma` だけです。** `text height` と `outline` は見出しを焼く前なので0で正常です。
EP66 の6枚は**硬いキーライト1灯**で mean 111–178 を余裕で越えました。**同じやり方でいきます。**
床を割ったら**グレードで持ち上げない**。**発注文を直してもう1枚**です（眠い絵をつくるくらいなら捨てる）。

---

## 4. 見出しとキッカー（★第二ビートの決定と、その理由）

### 4.1 本編タイトル（サムネはこれを繰り返さない）

```
Three Patients Died Under Its Care. The Only Claim It Let a Court Hear Was Its Own Bill.
```
（`09_package/youtube_meta.v001.json`）

**サムネの見出しは、このタイトルが言っていないことを言います。**同じ命題を絵と文字で二度言うと、サムネの一行が無駄になります。

### 4.2 ★見つけた欠陥（実測）

`scripts/build_ep62_65_thumbnails.py` の `SPEC` を機械的に走査した結果（16組）:

- **キッカーが自分の見出しに逐語で含まれている組が2件。** `greene G222`（`THE PAPER` / `THE PAPER CAME OFF`）と、**`marmet R224`（`NOT UPHELD` / `VACATED, NOT UPHELD`）**。
- **同じ語句が別候補で見出しとキッカーに使い回されている組が1件。** `correa C239` のキッカー `NEVER REFUSED` は `C222` の見出しそのもの。

キッカーは**第二の事実を置ける唯一の場所**です。そこに見出しを写経すると、**1枚のサムネで運べる事実が2つから1つに減ります。**
marmet 自身がその1件です。**この6組では、キッカーは必ず見出しが言っていない事実を足します。**

### 4.3 6組（見出しは2行・大文字・キッカーは3語以内）

| # | プレート | 見出し（2行） | キッカー（第二ビート） | アクセント | キッカーが**足している**事実 |
|---:|---|---|---|---|---|
| 1 | `R234` | `SIGNED FOR` / `SOMEONE ELSE` | `AUTHORITY NEVER DECIDED` | gold `#E5B53A` | 家族が本人に代わって署名した、という見出しに対し、**その家族に署名する権限があったのかは、この判決が一度も判断していない**ことを足す |
| 2 | `R235` | `EVERY DISPUTE` / `BUT ONE` | `SAME SENTENCE` | electric `#1F6BFF` | 例外が別紙でも別条項でもなく、**同じ一文の中に書かれていた**ことを足す |
| 3 | `R236` | `ONLY ONE` / `PATIENT NAMED` | `IN THE CAPTION` | gold `#E5B53A` | 名前が出るのが本文ですらなく、**事件名の行だけ**であることを足す |
| 4 | `R237` | `VACATED,` / `NOT UPHELD` | `NOTHING WAS ORDERED` | electric `#1F6BFF` | 破棄・差戻しという結論に対し、**最高裁は誰にも仲裁を命じていない**ことを足す |
| 5 | `R238` | `ONE FORM` / `WAS DIFFERENT` | `NO EXCEPTIONS` | red `#D22628` | 3枚が同じ紙ではなかったという見出しに対し、**その1枚には例外条項が1つも無かった**ことを足す |
| 6 | `R239` | `CREATED FROM` / `WHOLE CLOTH` | `WEST VIRGINIA SAID` | gold `#E5B53A` | 強い引用に対し、**それを言ったのは州の最高裁であって連邦最高裁ではない**という帰属を足す |

**キッカーと見出しの語の重なりはゼロです**（6組すべて機械照合済み・§7 の検証項目）。

### 4.4 6組が `forbidden_claims` に触れていないこと

| # | 主張 | 根拠 | 触れていないこと |
|---:|---|---|---|
| 1 | 家族が本人に代わって署名／権限は未判断 | MB-07／Brown II（州最高裁は権限の論点を「まず地裁で」と判断を回避） | 続柄を書いていない（`mother` `daughter` `widow` を使わない）。**拘束するともしないとも言っていない** |
| 2 | すべての紛争が仲裁、例外は延滞金の取立てだけ、同じ一文の中 | MB-23／MB-25 | 「有効」「強制された」を含まない。§5 の5枚目が**3人を一括りにしない**訂正を担当する |
| 3 | 名前のある患者は1人だけ・キャプションのみ | MB-19 | 統計を含まない。患者の描写をしない |
| 4 | 破棄・差戻し／誰にも命じていない | MB-34／MB-50／MB-53 | `upheld` `valid` は**否定形でのみ**使う（`NOT UPHELD` は可）。判事名も `unanimous` も無い（per curiam） |
| 5 | Marchio の紙は別文書・例外条項なし | MB-21 | 3家族を一括りにしない。むしろこの1枚が**一括りを打ち消す** |
| 6 | 州最高裁が連邦最高裁の読み方を "created from whole cloth" と呼んだ | 判決記録・meta 本文 | **連邦最高裁の言葉として提示しない**（キッカーが帰属を明示する） |

---

## 5. プロンプト（各1枚）

> `[STYLE]` は §2 のサムネ専用スタイルを、`[NEG]` は §2 の EP66 バッチC 逐語版を展開する。
> `Avoid: [NEG]` の直後の語列は**そのまま続けて足す**（正典 `[NEG]` からは1語も削らない）。

### `R234.png` — PERSON・受付のカウンター（第1候補）

**見出し:** `SIGNED FOR` / `SOMEONE ELSE`　**キッカー:** `AUTHORITY NEVER DECIDED`　**アクセント:** gold

- `R234.png`
An entirely invented ordinary man in his late sixties in a plain buttoned work shirt standing at the visitor's side of a plain admission counter in an ordinary care facility, photographed from behind the counter at chest height from about six feet away, his head and shoulders held WHOLLY WITHIN THE LOWER 60% of the frame and set slightly LEFT of centre with his face filling about a sixth of the frame width, his weathered face clearly visible and turned three-quarters toward the camera, HIS EYES DIRECTED DOWN AT THE COUNTER TOP AND NOT AT THE CAMERA, mouth closed, no smile and no expression put on for the camera, ONE hard directional key light from the LEFT so his face and the pale counter top are the brightest things in the picture while the shadow side of his face stays deep and clean, the wall behind him plain, pale and evenly lit, his right hand resting FLAT AND OPEN on the counter with five clearly separated fingers and his other arm out of frame below the counter edge, on the counter in front of him one plain printed sheet whose printing is a DENSE FLAT GREY BLOCK OF UNREADABLE RULED LINES with no characters, no words, no marks and no shapes of any kind on it, and one plain dark ballpoint pen lying beside the sheet, nobody else anywhere in the picture, no plaque, no notice and no plate of any kind on the counter or the wall, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of plain, evenly lit, pale bright wall with nothing whatever entering it: no head, no hair, no shoulder, no hand, no door frame, no window, no lamp, no shelf, no picture frame, no cable, no ceiling line, no furniture edge and no horizon line anywhere within that upper 40% [STYLE] Avoid: [NEG], hospital bed, a person lying in a hospital bed, ventilator, oxygen mask, IV drip, monitor trace, syringe, medication, nurse, doctor, scrubs, stethoscope, clinical scene, operating theatre, laboratory, wheelchair, room numbers, signage, banknotes, cash, coins, a hand on a shoulder, a tear, crying, a lonely old person lit for pity, wall clock, cosy fireplace, low contrast, low-key, dim interior, underexposed, murky, muddy shadows, fused fingers, extra fingers, malformed hand, clasped hands, posed smile, advertising model

**保存先:** `H:\pd-media\assets\ai\marmet\R234.png`（**新規。既存を上書きしない**）

### `R235.png` — 二つの扉（人物なし）

**見出し:** `EVERY DISPUTE` / `BUT ONE`　**キッカー:** `SAME SENTENCE`　**アクセント:** electric

- `R235.png`
Two identical plain flush doors side by side in the bare pale corridor of an ordinary institutional building, seen straight on and square from about twelve feet away at chest height, the LEFT door SHUT and dark against the pale wall and the RIGHT door standing WIDE OPEN with hard daylight from the room beyond pouring out through the opening and lying as one bright hard-edged shape across the corridor floor, the two doors and their frames occupying the LOWER 60% of the frame with the TOP OF BOTH DOOR FRAMES no higher than 55% down from the top of the frame, the lit floor and the shut door reading as opposites at a glance, no handrail, no notice, no plaque, no number and no plate of any kind on either door or anywhere on the wall, nobody in the picture and no furniture in the corridor, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of plain, evenly lit, pale bright wall with nothing whatever entering it: no head, no hair, no shoulder, no hand, no door frame, no window, no lamp, no shelf, no picture frame, no cable, no ceiling line, no furniture edge and no horizon line anywhere within that upper 40% [STYLE] Avoid: [NEG], hospital bed, a person lying in a hospital bed, ventilator, oxygen mask, IV drip, monitor trace, syringe, medication, nurse, doctor, scrubs, stethoscope, clinical scene, operating theatre, laboratory, wheelchair, room numbers, signage, banknotes, cash, coins, a hand on a shoulder, a tear, crying, a lonely old person lit for pity, wall clock, cosy fireplace, low contrast, low-key, dim interior, underexposed, murky, muddy shadows, handrail, notice board, fire extinguisher, trolley, exit light

**保存先:** `H:\pd-media\assets\ai\marmet\R235.png`（**新規**）

### `R236.png` — PERSON・空席の列にひとり

**見出し:** `ONLY ONE` / `PATIENT NAMED`　**キッカー:** `IN THE CAPTION`　**アクセント:** gold

- `R236.png`
An entirely invented ordinary woman in her fifties in a plain buttoned coat sitting alone in the middle of a straight row of eight identical empty waiting chairs against a plain pale wall in an ordinary care facility, photographed square on from about ten feet away from slightly ABOVE her eye level so that her head sits at about 52% down from the top of the frame and her head, shoulders and the whole row of chairs are held WHOLLY WITHIN THE LOWER 60% of the frame, she sits slightly RIGHT of centre, her face clearly visible and lit hard from the RIGHT by ONE directional key light so her face is the brightest thing in the picture while the shadow side stays deep and clean, HER EYES DIRECTED ACROSS THE ROOM AND NOT AT THE CAMERA, mouth closed, no smile, both hands resting SEPARATELY and flat on her knees a hand's width apart with fingers relaxed and clearly separated, not crossed and not clasped, every other chair in the row conspicuously empty, nobody else anywhere in the picture, no plaque, no notice and no plate of any kind on the wall, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of plain, evenly lit, pale bright wall with nothing whatever entering it: no head, no hair, no shoulder, no hand, no door frame, no window, no lamp, no shelf, no picture frame, no cable, no ceiling line, no furniture edge and no horizon line anywhere within that upper 40% [STYLE] Avoid: [NEG], hospital bed, a person lying in a hospital bed, ventilator, oxygen mask, IV drip, monitor trace, syringe, medication, nurse, doctor, scrubs, stethoscope, clinical scene, operating theatre, laboratory, wheelchair, room numbers, signage, banknotes, cash, coins, a hand on a shoulder, a tear, crying, a lonely old person lit for pity, wall clock, cosy fireplace, low contrast, low-key, dim interior, underexposed, murky, muddy shadows, fused fingers, extra fingers, malformed hand, clasped hands, posed smile, advertising model

**保存先:** `H:\pd-media\assets\ai\marmet\R236.png`（**新規**）

### `R237.png` — 空いた小部屋（人物なし）

**見出し:** `VACATED,` / `NOT UPHELD`　**キッカー:** `NOTHING WAS ORDERED`　**アクセント:** electric

- `R237.png`
A small plain private meeting room with one bare wooden table and two empty upright chairs, one chair drawn out and turned slightly away from the table and the other pushed in square, photographed square on from the open doorway at chest height from about eight feet away, the table and both chairs occupying the LOWER 60% of the frame and set slightly RIGHT of centre, ONE hard directional key light from an unseen window on the LEFT raking straight across the bare tabletop so the wood grain and the empty chair backs stand out bright and throw two long hard-edged shadows across the floor, the table surface completely bare with no paper, no folder, no cup and no object of any kind on it, the walls plain, pale and evenly lit, nobody in the picture and nobody in the doorway, no plaque, no notice and no plate of any kind anywhere in the room, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of plain, evenly lit, pale bright wall with nothing whatever entering it: no head, no hair, no shoulder, no hand, no door frame, no window, no lamp, no shelf, no picture frame, no cable, no ceiling line, no furniture edge and no horizon line anywhere within that upper 40% [STYLE] Avoid: [NEG], hospital bed, a person lying in a hospital bed, ventilator, oxygen mask, IV drip, monitor trace, syringe, medication, nurse, doctor, scrubs, stethoscope, clinical scene, operating theatre, laboratory, wheelchair, room numbers, signage, banknotes, cash, coins, a hand on a shoulder, a tear, crying, a lonely old person lit for pity, wall clock, cosy fireplace, low contrast, low-key, dim interior, underexposed, murky, muddy shadows, filing cabinets, stacked paperwork, bookcase, conference table, boardroom

**保存先:** `H:\pd-media\assets\ai\marmet\R237.png`（**新規**）

### `R238.png` — PERSON・三枚のうち一枚だけ違う

**見出し:** `ONE FORM` / `WAS DIFFERENT`　**キッカー:** `NO EXCEPTIONS`　**アクセント:** red

- `R238.png`
An entirely invented ordinary man in his seventies in a plain knitted cardigan sitting at an ordinary kitchen table with THREE plain stapled paper documents laid out side by side and squared in front of him, the MIDDLE one visibly THINNER than the other two and on paper of a plainly different colour, photographed from slightly ABOVE and square on from about five feet away so that his head sits at about 50% down from the top of the frame and his head, shoulders and all three documents are held WHOLLY WITHIN THE LOWER 60% of the frame, he sits slightly LEFT of centre, his face clearly visible and lit hard from the RIGHT by ONE directional key light through a window out of shot so his face and the pale paper are the brightest things in the picture, HIS EYES DIRECTED DOWN AT THE MIDDLE DOCUMENT AND NOT AT THE CAMERA, mouth closed, no smile, one hand resting FLAT AND OPEN on the table beside the documents with five clearly separated fingers and the other arm down out of frame, the printing on all three documents a DENSE FLAT GREY BLOCK OF UNREADABLE RULED LINES with no characters, no words, no marks and no shapes of any kind on any of them, nobody else in the picture, no cup, no plate, no bowl and no clutter on the table, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of plain, evenly lit, pale bright wall with nothing whatever entering it: no head, no hair, no shoulder, no hand, no door frame, no window, no lamp, no shelf, no picture frame, no cable, no ceiling line, no furniture edge and no horizon line anywhere within that upper 40% [STYLE] Avoid: [NEG], hospital bed, a person lying in a hospital bed, ventilator, oxygen mask, IV drip, monitor trace, syringe, medication, nurse, doctor, scrubs, stethoscope, clinical scene, operating theatre, laboratory, wheelchair, room numbers, signage, banknotes, cash, coins, a hand on a shoulder, a tear, crying, a lonely old person lit for pity, wall clock, cosy fireplace, low contrast, low-key, dim interior, underexposed, murky, muddy shadows, fused fingers, extra fingers, malformed hand, clasped hands, posed smile, advertising model, spectacles glare, magnifying glass

**保存先:** `H:\pd-media\assets\ai\marmet\R238.png`（**新規**）

### `R239.png` — PERSON・反物（"whole cloth"）

**見出し:** `CREATED FROM` / `WHOLE CLOTH`　**キッカー:** `WEST VIRGINIA SAID`　**アクセント:** gold

- `R239.png`
An entirely invented ordinary woman in her fifties in a plain dark work apron sitting behind a wide bare wooden table with a long roll of plain UNDYED WOVEN CLOTH half unrolled across the table in front of her, the loose end of the cloth lying flat toward the camera with one soft fold standing up in it, the weave plain and completely without pattern, print or marking of any kind, photographed square on from about six feet away from slightly ABOVE her eye level so that her head sits at about 52% down from the top of the frame and her head, shoulders, the roll and the unrolled cloth are held WHOLLY WITHIN THE LOWER 60% of the frame, she sits slightly RIGHT of centre, her face clearly visible and lit hard from the LEFT by ONE directional key light so her face and the pale cloth are the brightest things in the picture while the shadow side of her face stays deep and clean, HER EYES DIRECTED DOWN AT THE CLOTH AND NOT AT THE CAMERA, mouth closed, no smile, both hands resting SEPARATELY and flat on the cloth a hand's width apart with fingers relaxed and clearly separated, not crossed and not clasped, no scissors, no pins and no other object anywhere on the table, nobody else in the picture, the wall behind her plain, pale and evenly lit, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of plain, evenly lit, pale bright wall with nothing whatever entering it: no head, no hair, no shoulder, no hand, no door frame, no window, no lamp, no shelf, no picture frame, no cable, no ceiling line, no furniture edge and no horizon line anywhere within that upper 40% [STYLE] Avoid: [NEG], hospital bed, a person lying in a hospital bed, ventilator, oxygen mask, IV drip, monitor trace, syringe, medication, nurse, doctor, scrubs, stethoscope, clinical scene, operating theatre, laboratory, wheelchair, room numbers, signage, banknotes, cash, coins, a hand on a shoulder, a tear, crying, a lonely old person lit for pity, wall clock, cosy fireplace, low contrast, low-key, dim interior, underexposed, murky, muddy shadows, fused fingers, extra fingers, malformed hand, clasped hands, posed smile, advertising model, bedding, bed sheets, hospital linen, patterned fabric, sewing machine

**保存先:** `H:\pd-media\assets\ai\marmet\R239.png`（**新規**）

---

## 6. 命名と保存先

- ファイル名は **`R234.png` `R235.png` `R236.png` `R237.png` `R238.png` `R239.png`** の6つだけ。
- 保存先 `H:\pd-media\assets\ai\marmet\`（本編プレートと同じ棚）。**同名の既存ファイルはありません。上書きは発生しません。**
- 長辺 3840px 以上・16:9・PNG。
- ⛔ **`mandatory_stills` には追加しない。** サムネプレートは本編のカットになりません。宣言すると `check_spec_satisfied.py` が「宣言された静止画がどのカットにも無い」で落ちます（`R217`–`R219`・`R224` と同じ扱い）。

---

## 7. 発注書の検査（生成を始める前に済ませてある）

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP65_marmet_CODEX_THUMBS.v001.md
```

顔／実在人物・読める文字・手書き・紋章／記章・数字の**五族すべて**が `[NEG]` に入っていることを機械が確認します。**`[NEG]` を1語でも削ったら、必ず再実行すること。**

さらに、貼り付けファイル `episodes/_planning/EP65_marmet_CODEX_PASTE_THUMBS/batch_01.txt` について、渡す前に**開いて目で読む**こと。本日、`[STYLE]` にシェルコマンドが入り `[NEG]` が空のまま出荷された貼り付けファイルがあります（生成側が blockquote ではなく ``` フェンスを拾った）。人が開いて初めて分かりました。確認項目:

1. `[STYLE]` が空でない
2. `[NEG]` が空でなく、`recognisable person` / `identifiable person` / `likeness of a real individual` / `portrait of a named person` を含む
3. `[NEG]` に **`human face` / `facial features` / `eyes` が入っていない**
4. プロンプトがちょうど6本・保存名が6つとも別
5. §3.1 の上40%の文が**6本すべてに逐語で**入っている

---

## 8. 生成後にやること（発注者側・Codex の作業ではない）

1. **6枚を1枚ずつ native で目視**する。落とす条件:

| # | 不合格条件 |
|---|---|
| Q1 | 紙・書類の上に**文字・行・単語に見えるもの**がある（灰色の塊まで潰れていない） |
| Q2 | 画のどこかに読める文字・数字・ロゴ・印章・室名札がある |
| Q3 | 人物プレート（`R234` `R236` `R238` `R239`）で**顔が見えない**／カメラ目線／作り笑い／広告のモデル顔 |
| Q4 | 手の指が数えられない・融合している・6本ある |
| Q5 | 臨床の要素（ベッド・点滴・車椅子・白衣）が写り込んでいる |
| Q6 | 上40%に何かが入っている（1280×720 に縮小して測る） |
| Q7 | プレート単体で mean luma < 38 または stddev < 45 |
| Q8 | 既存の他話のサムネと構図が実質同じ／marmet の既存5枚と同じ「紙の上の文字」になっている |

2. 上40%と輝度の測定:
```
py -3.11 scripts/check_thumb_subject_luma.py --thumb <file>
```
**`outline` と `text height` は見出しを焼く前なので無意味。`subject luma` と `whole luma` だけ読む。**

3. 合成（`scripts/build_ep62_65_thumbnails.py` の `SPEC["marmet"]` を6組に差し替える）。**§4.3 の表がそのまま入力**である:

```python
    "marmet": ("PD-2026-065-marmet", [
        ("R234", "AUTHORITY NEVER DECIDED", ["SIGNED FOR", "SOMEONE ELSE"], GOLD),
        ("R235", "SAME SENTENCE",           ["EVERY DISPUTE", "BUT ONE"],    BLUE),
        ("R236", "IN THE CAPTION",          ["ONLY ONE", "PATIENT NAMED"],   GOLD),
        ("R237", "NOTHING WAS ORDERED",     ["VACATED,", "NOT UPHELD"],      BLUE),
        ("R238", "NO EXCEPTIONS",           ["ONE FORM", "WAS DIFFERENT"],   RED),
        ("R239", "WEST VIRGINIA SAID",      ["CREATED FROM", "WHOLE CLOTH"], GOLD),
    ]),
```

4. 合成後に `check_final_acceptance.py` の `thumbnail_visibility` と `check_thumb_subject_luma.py` を候補6枚に当て、**通った中からオーナーが1枚選ぶ**。選択1枚を `09_package/thumbnail.selected.v006.png` へ置く（**v005 を上書きしない**）。
5. 旧候補（`thumbnail.marmet.01`–`04.v001.png`・`thumbnail.selected.v001`–`v005.png`）は**削除しない**。差し替えるだけ。
