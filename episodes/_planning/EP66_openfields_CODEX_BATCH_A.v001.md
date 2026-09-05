# EP66 openfields — Codex 画像生成 **バッチA発注** v001（**69枚**・1プロンプト1枚）

> **プレート 69枚（L001–L069、欠番なし）・`mandatory_stills` 65件（THUMB の L066/L067/L068/L069 を除く）**

> ## ⚠ このバッチだけでは完結しません。**バッチBが出ます。**
> EP65 は「追加バッチは出ません」と書けました。**台本があったから**です。**EP66 にはまだ台本がありません。**
> 台本の実語数が無い状態で区分別の比例配分を書けば、それは根拠のない数字であり、
> このプロジェクトが最も多く記録してきた失敗（もっともらしい仮置きが、後から決定として読まれる）そのものです。
> **したがってこのバッチAは、台本に依存しない register だけを発注します** ——
> 場所（gate / boundary / fence / track / woods / field / farmhouse）、人物、パッケージング。
> **区分別（HOOK/OP/ACT_1..ACT_5/ENDING）の配分と、その枚数は、台本が `script_verified` になってから
> バッチBで確定します。**枚数の根拠になる算術は `episodes/PD-2026-066-openfields/episode_spec.v001.json`
> の `notes` に全部書いてあります（要点：契約 `distinct_video_assets` 350 − 実写採用 = i2v 用プレート、
> ＋ 静止画カット 164）。**実写採用数はまだ測っていません。**

**題材:** 開かれた野（open-fields doctrine）。
*Punxsutawney Hunting Club v. Pennsylvania Game Commission*（ペンシルベニア州最高裁・2026-07-21）と
*Rainwaters v. Tennessee Wildlife Resources Agency*（テネシー州控訴裁・2024-05-09）。
主役は**土地所有者**である。掲示（posted）され、門（gate）で閉じられた私有地に、
職員が令状なしで立ち入り、幹にトレイルカメラを残していった。

> ### ★事実についての警告（発注者・生成者の双方へ）
> **この時点で判決文はこのリポジトリに1本も入っていません。**上の2行（裁判所名・日付・当事者の立場）
> より先の事実は、`EP66_openfields_FACTS_LEDGER.v001.md`（**未作成・TODO**）が出来るまで**誰も知りません**。
> **判断内容・結論・理由づけを絵にしない。**このバッチの絵は一枚残らず「場所・境界・器具」であって、
> 「誰が勝った」でも「職員が何を考えていたか」でもありません。契約の `forbidden_claims` 7 が
> 「台帳ができるまで、いかなる判示も主張してはならない」と定めています。**絵も同じ拘束を受けます。**

**この映画は「悪徳役人」の話ではありません。**主役は**境界そのもの** —— 門・掲示・紫の塗り・鉄条網・
そして幹に留められた小さなプラスチックの箱です。**その箱が何を撮ったかは、絵で語ってはいけません。**

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**
3. **「良いのが出るまで回す」を禁止する。**
4. 作り直してよいのは §1 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。

EP60はこの規則で **279枚・変種0・指定外0・sha256重複0・知覚的近似重複0** を達成済み。

### 0.5 絵の水準（オーナー指示 2026-08-04）

このシリーズの工芸基準は**アカデミー／パルムドール級の脚本水準**に置かれています。画像側の意味は一つです。

- **カタログ写真を作らない。** 「門」「柵」「林」ではなく、**どの光で・どの距離から・誰の目の高さで**
  見るのかを書いてあります。プロンプトの副詞句（`from the public road side` /
  `at the height of someone standing in front of it` / `with a long lens from two hundred yards`）は
  装飾ではなく**指定**です。削らずに生成してください。
- **視点のない絵は不合格。** きれいだが誰も立っていない絵より、平凡だが**誰かの目の高さ**にある絵を採ります。
  この映画では「**道路の側から見た門**」と「**敷地の側から見た同じ門**」が別の意味を持ちます。
- **象徴を足さない。** 天秤・砂時計・十字に組んだ枝・崩れる書類の山。どれも要りません。
- **風景写真にしない。** 紅葉の絶景・朝靄の名所・ドローンの俯瞰は全部却下です。
  ここは**働いている土地**であって、観光地ではありません。

---

## 1. ★絶対条件（触れた絵は使用不可）

`episodes/PD-2026-066-openfields/episode_spec.v001.json` の `forbidden_subjects` がこの節の正典です。

- **実在の人物を描かない。** 土地所有者も、職員も、裁判官も。**生成される人間は全員、顔が写りません。**
  背中・手・長靴・霧の中の遠い人影。袖は無地・記章なし。
- **読める文字・数字・手書き・印章・ロゴを描かない。**
  > ### ★このバッチで最も事故が起きるのはここです★
  > この話の主役画像のひとつは**掲示（posted sign）**です。生成器に「posted sign」と書けば、
  > **必ず POSTED / NO TRESPASSING と書きます。**
  > **掲示は次の3通りでしか描いてはいけません。**
  > **(a) 風雨で退色・膨れ上がり、面が完全に読めなくなった無地の板、**
  > **(b) 紫の塗りの帯（Pennsylvania / Tennessee の purple paint law の register）、**
  > **(c) かつて板が留まっていた釘穴と、色の抜けた樹皮の矩形。**
  > プロンプト本文に **posted / no trespassing / keep out という語を一度も書いていないのは意図的です。**
  > 板の上の印刷も同様に、**灰色の面・退色したにじみ**として描き、行や単語に見えないところまで潰します。
  > **実写アーカイブに実在の看板の文字が写っていること**は別問題であり、
  > それは footage QC で判定します。**ここで拘束されるのは生成画だけです。**
- **制服・記章・パトカー・手錠を描かない。** 職員は一人も登場しません。
  「立ち入った」は**人**ではなく、**残っていったもの**（轍・カメラ・切られた鎖）で表します。
- **銃と獲物を描かない。** 猟銃・散弾銃・ホルスター・仕留められた動物・血・剥製・壁の角。
  原告は狩猟クラブですが、**これは狩猟の映画ではなく財産権の映画です。**
- **監視スリラーの意匠を作らない。** 暗視の緑・サーモグラフィの偽色・十字線・CCTVの分割画面。
  **トレイルカメラは、幹にベルトで留められた小さくて安っぽいプラスチックの箱です。それが全部です。**
- **実在と特定できる土地・建物を描かない。** 農場名・道路番号・郡章・特徴的な建築。
  **ありふれたアパラチアと中部テネシーの農地**であること。
- **法廷内観・木槌・判事席・鉄格子を描かない。** 棚の法廷映像は24本中23本を使い切っており、絵も作りません。
- **広告調にしない。** 黄金色の夕陽、絵葉書の紅葉、クリスマス、ドローンの映え、HDRの縁光。
- **黒つぶれさせない。** スマホで見て何が写っているか分かること。

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字がある（**板の上・樹皮の上・車体も含む**）／掲示の面に語や行が見える |
| Q3 | 印章・紋章・ロゴ・記章・ナンバープレートらしきものがある |
| Q4 | 顔が判別できる人物が写っている（**人を一言も書いていないプロンプトでも起きます。EP65 の L相当 R019/R041 がそれです**） |
| Q5 | 制服・パトカー・手錠・銃・仕留められた動物・血が写っている |
| Q6 | 暗視の緑・サーモの偽色・十字線・CCTV分割画面になっている |
| Q7 | 法廷内観・木槌・判事席・鉄格子が写っている |
| Q8 | 実在と特定できる（農場名・道路番号・郡章・特徴的建築）／ドローン俯瞰になっている |
| Q9 | 視点がない（カタログ写真・観光写真になっている）／広告調である／画面全体が暗すぎる／既存の他話と実質同じ構図 |
| Q10 | **THUMB 4枚のみ**：上1/3に枝・幹・地平線・被写体の一部が入り込んでいる／上1/3が暗い |

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, muted natural colour, flat overcast daylight of a late Appalachian autumn, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing, rural Pennsylvania and Middle Tennessee between 2019 and 2026, ordinary working farmland and unmanaged second-growth woodland, worn unglamorous surfaces, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> text, lettering, numerals, digits, house numbers, handwriting, cursive writing, legible signature, seals, emblems, logos, insignia, badge, name plates, readable words on a sign, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, police officer, sheriff, trooper, uniform, patrol car, flashing lights, handcuffs, rifle, shotgun, firearm, holster, dead animal, carcass, blood, taxidermy, mounted antlers, courtroom interior, gavel, judge's bench, prison bars, razor wire, scales of justice, hourglass, a handshake, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, aerial view from above the treetops, golden hour, sunset glow, postcard scenery, autumn colour explosion, Christmas, tropical, modern smartphones, laptops, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

> **★ `[NEG]` に顔の語が入っている理由**（消さないこと）：EP65 で **正典 `[NEG]` に顔を抑える語が1つも無く**、
> 発注が「紙」「法令集」だった2枚が**完全に識別可能な顔**で戻ってきました（invariant 11 違反）。
> 守っていたのは個々の本文の「no face」だけで、**人を一言も書いていない発注には保護がゼロ**でした。
> `scripts/check_image_order_neg.py` は、顔・文字・手書き・紋章・数字の**五族すべて**を欠く発注書を拒否します。
> この `[NEG]` はそのチェックを通過済みです（§6-0 に実行結果）。

---

## 3. 命名と保存先

- ファイル名 `L001.png` … `L069.png`。**欠番を作らない。**
- 保存先 `H:\pd-media\assets\ai\openfields\`。
- 長辺 3840px 以上・16:9・PNG。
- 接頭辞 `L`（land）は既存話と衝突しません（使用済み：C / F / G / H / M / P / R / S / W）。

---

## 4. 区分と枚数（合計69枚）— **台本に依存しない register のみ**

**比例配分は行っていません。**台本が無いからです（冒頭の警告を参照）。
下の8つは「この映画がどの拍を撮ろうと必ず要る絵」であり、**枚数は register の内部的な必要数**
（同じ門を道路側／敷地側の両方から、境界を外側／内側の両方から、等）で決めています。

| 区分 | 枚数 | ID範囲 | 中身 | 決め方 |
|---|---|---|---|---|
| GATES | 8 | `L001`–`L008` | 閉じた門・鎖と錠・蝶番・門の無い門柱・轍 | 同じ門を**道路側と敷地側**の両方から要る（この映画の中心的対比）。距離3種（正対・膝下・遠望） |
| BOUNDARY | 8 | `L009`–`L016` | 読めない板・紫の塗り・落ちた板・釘穴 | 掲示の register は**文字を出さずに**3通り（板／塗り／痕）で描き分ける必要がある |
| FENCE | 7 | `L017`–`L023` | 有刺鉄線・隅の控え柱・木に飲まれた柵・切れた線 | 「線」を空間として見せるのに、走る・角・破れの3態が要る |
| CAMERA | 8 | `L024`–`L031` | 幹の箱・ベルト・見上げ・箱が見ている画・外した痕 | **器具そのもの**と**器具の視点**と**器具が去った後**の3層 |
| TRACK | 6 | `L032`–`L037` | 砂利道・分岐・轍の重なり・林へ消える道 | 「入った」を人なしで示す唯一の register |
| WOODS_FIELD | 8 | `L038`–`L045` | 二次林の内部・獣道・刈り跡・林縁・溜まり水 | open field と woodland は法理の用語そのもの。両方の内部が要る |
| DUSK | 5 | `L046`–`L050` | 薄暮の空き地（中央から・門から・霧・柵越し） | この映画の情緒はここだけで作る。**朝夕の映えは禁止**、薄暮の平らな光のみ |
| FARMHOUSE | 5 | `L051`–`L055` | 遠くから見た母屋（＝curtilage の外から見た家） | **家は必ず小さく**。近づいた瞬間にこの映画の主題が壊れる |
| PEOPLE | 10 | `L056`–`L065` | 人物プレート（顔なし規則・`people_plates_min: 10`） | 契約の最小値ちょうど |
| THUMB | 4 | `L066`–`L069` | サムネ候補（`thumbnail_candidates_min: 4`） | 契約の最小値ちょうど。§5 THUMB の輝度指定は本編と別 |
| | **69** | | | |

> ### ★ curtilage の一線（この発注全体を貫く構図規則）★
> 開かれた野の法理は「家のまわり（curtilage）」と「その外の野」を分けます。
> **したがってこの69枚には、家に近づいた絵が1枚もありません。**`L051`–`L055` はすべて
> **数フィールド以上離れた遠望**です。玄関・ポーチ・窓の中・庭の道具は**バッチBでも発注しません**。
> 近づいた瞬間、絵が主題と矛盾します。

### まだ決まっていないこと（バッチBで決まる・ここで仮置きしない）

| 未確定 | 何が決めるか |
|---|---|
| HOOK 5枚が**どの絵**か | 台本の HOOK（約8秒・オーナーが書く）。**約束→回収**表は台本確定後に書く |
| 区分別（ACT_1..ACT_5 / ENDING）の枚数 | `EP66_openfields_script.en.v001.md` の**節ごとの実ナレ語数** |
| i2v 用プレートの総数 | `350 − 実写採用本数`。実写採用本数は `scripts/search_archive.py` の実測＋目視QC後にしか出ない |
| 静止画プレートの総数 | 164（契約の算術より）。うちバッチAが 65 を供給する |
| ショート用プレートの内数表 | `SHORTS_SLATE_EP66` が存在しない。**ショートの発注はまだ出さない** |

---

## 5. プロンプト（各1枚）

### GATES（8枚） — 閉じている、ということ。

- `L001.png`
A steel tube farm gate closed across the mouth of a track, chained shut at the latch post, photographed head-on from the public road side at the height of someone standing directly in front of it, wet gravel in the foreground and bare second-growth woodland behind, flat grey afternoon light [STYLE] Avoid: [NEG]
- `L002.png`
The same kind of tube gate seen from the private side looking back out toward the road, the track running away beneath it, the horizontal bars cutting the view of the road into flat strips, nobody on either side of it [STYLE] Avoid: [NEG]
- `L003.png`
A gate hinge post set in a block of concrete, seen close at knee height from one side, the paint gone entirely to rust around the pin, dead grass grown up around the base and pressed flat by rain [STYLE] Avoid: [NEG]
- `L004.png`
A length of chain wrapped twice around a gate post and closed with a plain padlock, seen close from the side at hand height, the links beaded with water, the shackle smooth and unmarked [STYLE] Avoid: [NEG]
- `L005.png`
A wooden farm gate sagging off its hinges where two fields meet, standing half open and stuck that way, grass grown up through the bottom rail, seen from a few feet away at waist height [STYLE] Avoid: [NEG]
- `L006.png`
A closed gate at the far end of a mown lane, photographed from two hundred yards away with a long lens so the gate sits small and flat in the middle of the frame and the lane converges toward it, low cloud above [STYLE] Avoid: [NEG]
- `L007.png`
A gap in a hedgerow where a gate once hung: two weathered posts still standing upright with nothing between them, the ground worn bare between the posts, seen straight on at eye height [STYLE] Avoid: [NEG]
- `L008.png`
Tyre ruts pressed deep into soft mud on the private side of a closed gate, seen from directly above at waist height, the ruts holding standing rainwater and the tread pattern soft at the edges [STYLE] Avoid: [NEG]

### BOUNDARY（8枚） — 掲示と紫の塗り。**面は読めない。**

- `L009.png`
A weathered rectangular placard nailed to a tree trunk at head height, its printed face bleached and blistered by years of weather until the surface is an even faded blur with no characters or lines discernible anywhere on it, the nail heads run with rust, plain grey woodland behind [STYLE] Avoid: [NEG]
- `L010.png`
Three identical blank weathered placards on three successive trunks along a boundary, receding away from the camera into the wood, each one turned squarely to face the camera, their faces uniformly faded to blank [STYLE] Avoid: [NEG]
- `L011.png`
A single vertical stripe of purple paint brushed onto the trunk of an oak at chest height, the paint thick and slightly run at its lower edge, bark texture standing through it, seen close and straight on in flat light [STYLE] Avoid: [NEG]
- `L012.png`
Two purple painted stripes on two trunks some yards apart, photographed along the line so that the near stripe and the far stripe align vertically in the frame, the wood behind them falling out of focus [STYLE] Avoid: [NEG]
- `L013.png`
A purple painted stripe weathered to a chalky bloom, seen at extreme close range, pale lichen creeping over its lower edge and into the bark [STYLE] Avoid: [NEG]
- `L014.png`
A blank weathered placard curled away from its trunk by years of frost and hanging by a single remaining nail, seen from slightly below in grey light [STYLE] Avoid: [NEG]
- `L015.png`
A marked boundary seen from outside it looking in: a line of blazed trunks stepping away into thin mist, each carrying the same purple stripe, the ground between them uncleared [STYLE] Avoid: [NEG]
- `L016.png`
A blank weathered placard lying face up where it fell in wet leaf litter, one bent nail still through it, seen from above at waist height [STYLE] Avoid: [NEG]

### FENCE（7枚） — 線。

- `L017.png`
A four-strand barbed wire fence running away across a stubble field toward a wooded ridge, photographed from ground level immediately beside the first post so the wires converge into the distance [STYLE] Avoid: [NEG]
- `L018.png`
A fence corner post braced with two diagonal struts, seen from outside the field at chest height, the strained wires pulling visibly on the brace, mud churned at its foot [STYLE] Avoid: [NEG]
- `L019.png`
Barbed wire stapled to a split locust post, seen at extreme close range, the staples driven deep and rusted through, the strands running out of true above and below [STYLE] Avoid: [NEG]
- `L020.png`
A fence line crossing a shallow creek, the wire dipping to the water on a rusted stay, the creek bed pale with gravel, seen from the bank at knee height [STYLE] Avoid: [NEG]
- `L021.png`
An old woven-wire fence swallowed halfway up its height by the trunk of the tree it was nailed to, the bark grown around and over the wire, seen close and level [STYLE] Avoid: [NEG]
- `L022.png`
A fence corner where three fields meet, the posts leaning three different ways and the wire slack between them, flat grey light and no building anywhere in view [STYLE] Avoid: [NEG]
- `L023.png`
A stretch of fence with its top wire broken and curled back on itself in two tight coils, seen from the outside at chest height [STYLE] Avoid: [NEG]

### CAMERA（8枚） — 幹の上の箱。**それ以上に演出しない。**

- `L024.png`
A small dull olive plastic box strapped to a tree trunk at chest height with a black webbing strap, seen from a few feet away and slightly below, its lens face turned off to the left of the frame, the bark rough around the strap [STYLE] Avoid: [NEG]
- `L025.png`
The same kind of box seen from behind its tree so that only the webbing strap and its plain buckle are visible around the trunk, the box itself hidden on the far side [STYLE] Avoid: [NEG]
- `L026.png`
A small plastic box strapped high on a trunk, photographed from the ground looking straight up, the box small and dark against a flat pale sky seen through bare branches [STYLE] Avoid: [NEG]
- `L027.png`
The view such a box would have: a narrow game trail through thin saplings, framed low and dead centre at about knee height, nothing and nobody on the trail, flat grey light throughout [STYLE] Avoid: [NEG]
- `L028.png`
A webbing strap cinched hard around bark, seen at extreme close range, the webbing frayed at the edge and the plain buckle bedded into the trunk's surface [STYLE] Avoid: [NEG]
- `L029.png`
Two small plastic boxes on two separate trunks at a junction of two woodland tracks, both turned to face down the same lane, seen from the lane at eye height [STYLE] Avoid: [NEG]
- `L030.png`
A small plastic camera box lying on the open tailgate of a pickup truck among wet leaves and a loose coil of webbing strap, seen from above at waist height [STYLE] Avoid: [NEG]
- `L031.png`
The pale unweathered rectangle of bark left on a trunk where a box has been strapped for years and has now been taken off, seen close and straight on, two small nail holes at its upper corners [STYLE] Avoid: [NEG]

### TRACK（6枚） — 入った、ということ。**人は写さない。**

- `L032.png`
A gravel farm track running straight away from the camera between two hedgerows under low cloud, the wheel ruts standing with rainwater, seen from the middle of the track at eye height [STYLE] Avoid: [NEG]
- `L033.png`
The same kind of track seen from the crown of a rise looking down along it, the pale gravel standing out against wet grass, the far end of it lost in the tree line [STYLE] Avoid: [NEG]
- `L034.png`
A fork in a farm track where the left branch has grassed over completely and the right branch is bare and used, seen from the fork itself at waist height [STYLE] Avoid: [NEG]
- `L035.png`
Fresh vehicle tracks pressed over older ones in wet gravel, seen from close to the ground at waist height so the two sets of tread cross in the middle of the frame [STYLE] Avoid: [NEG]
- `L036.png`
A concrete culvert pipe running under a farm track, the gravel worn thin over the crown of it, seen from the ditch below at ground level [STYLE] Avoid: [NEG]
- `L037.png`
A track passing from open ground into standing timber, the light dropping away as it goes in, seen from the open side at eye height [STYLE] Avoid: [NEG]

### WOODS_FIELD（8枚） — 「野」と「林」そのもの。

- `L038.png`
The inside of an unmanaged second-growth wood at midday under heavy overcast, straight bare trunks receding in every direction, no undergrowth and no path, seen at eye height [STYLE] Avoid: [NEG]
- `L039.png`
A narrow deer trail worn through leaf litter in a wood, seen from knee height along its length, the trail disappearing between two trunks [STYLE] Avoid: [NEG]
- `L040.png`
A stand of hardwood on a hillside seen from below the slope, the ground rising steeply so the trunks stand out of vertical across the frame [STYLE] Avoid: [NEG]
- `L041.png`
A field of frost-killed stubble running flat to a dark tree line, seen from the middle of the field at eye height under a white sky [STYLE] Avoid: [NEG]
- `L042.png`
A mown hay field seen along the cut stripes so they converge, the windrows still lying, low cloud above and no machinery in the frame [STYLE] Avoid: [NEG]
- `L043.png`
The edge of a wood where the field stops and the trunks begin, photographed along the edge so that open ground fills the left half and closed timber the right [STYLE] Avoid: [NEG]
- `L044.png`
Rainwater standing in the low corner of a ploughed field, the sky reflected flat and grey in it, seen from the field at waist height [STYLE] Avoid: [NEG]
- `L045.png`
A brush pile of cut limbs heaped at a field corner and greying with age, seen from a few yards away at eye height [STYLE] Avoid: [NEG]

### DUSK（5枚） — 薄暮。**夕陽の色は禁止。**

- `L046.png`
An empty field at dusk seen from the middle of it, the tree line a single flat dark band low in the frame and the sky above it still pale and colourless, no artificial light anywhere [STYLE] Avoid: [NEG]
- `L047.png`
The same empty field at dusk seen from just inside its gate, the gate's top rail crossing the bottom of the frame, the far tree line almost gone to black [STYLE] Avoid: [NEG]
- `L048.png`
The last flat light of the day lying on a wooded rise beyond a field, seen from the field at eye height, the colour drained out of everything and no lamp burning anywhere [STYLE] Avoid: [NEG]
- `L049.png`
A field at dusk with ground mist gathering in the low centre of it, the mist level and about waist deep, the tree line standing above it [STYLE] Avoid: [NEG]
- `L050.png`
A field at dusk seen through a wire fence from outside it, the strands of wire crossing the pale sky in the upper part of the frame, everything beyond the wire in silhouette [STYLE] Avoid: [NEG]

### FARMHOUSE（5枚） — **必ず遠い。**curtilage には入らない。

- `L051.png`
A plain two-storey farmhouse and a low barn seen from three fields away at dusk, the buildings held small near the centre of the frame with one window lit, bare hedgerows stepping away between camera and house [STYLE] Avoid: [NEG]
- `L052.png`
The same kind of farmstead in flat daylight from the crown of a rise, the house and barn small against a broad pale sky, ploughed ground filling the foreground [STYLE] Avoid: [NEG]
- `L053.png`
A farm lane running away toward a distant house, the house kept small at the end of it and never approached, wet grass either side, seen from the road end of the lane at eye height [STYLE] Avoid: [NEG]
- `L054.png`
A farmhouse roofline just visible over a ridge of bare trees from a neighbouring field, only the roof and one chimney showing, everything else screened by timber [STYLE] Avoid: [NEG]
- `L055.png`
A single yard light burning on a pole at a distant farmstead at dusk, the buildings around it dark and small, seen from far out in an empty field [STYLE] Avoid: [NEG]

### PEOPLE（10枚） — 人物プレート。**全員実在しない一般人。顔は写さない。**

- `L056.png`
A man's back in a heavy canvas work coat, standing at a closed farm gate with both hands resting on the top rail, seen from a few feet behind him at his own shoulder height, face not visible [STYLE] Avoid: [NEG]
- `L057.png`
A pair of worn rubber boots standing still on wet gravel, seen from directly above at chest height so only the boots and the ground are in frame [STYLE] Avoid: [NEG]
- `L058.png`
A single bare hand closing a padlock through a chain on a gate post, a plain unmarked sleeve entering the frame at the lower edge and nothing else of the person visible, no arm above the wrist and no face anywhere [STYLE] Avoid: [NEG]
- `L059.png`
A figure walking away along a fence line, held small in the frame and seen from far behind, the fence running out ahead of them into flat grey light [STYLE] Avoid: [NEG]
- `L060.png`
Two adults standing several yards apart at the edge of a field, both seen from behind at distance, neither turned toward the camera and neither face visible [STYLE] Avoid: [NEG]
- `L061.png`
An older person's hands resting on the top rail of a wooden fence, knuckles and veins plain in ordinary daylight, no face in the frame and no jewellery [STYLE] Avoid: [NEG]
- `L062.png`
A person in a hooded coat standing at the edge of a wood with their back to the camera, looking in among the trunks, features not visible at all [STYLE] Avoid: [NEG]
- `L063.png`
A hand and forearm reaching up to a webbing strap around a tree trunk, only the hand, the forearm and a plain dark sleeve in the frame, no shoulder and no head [STYLE] Avoid: [NEG]
- `L064.png`
A figure standing in the open doorway of a barn against flat grey daylight, seen from outside at distance, the features not resolvable at all [STYLE] Avoid: [NEG]
- `L065.png`
The back of a person seated on the open tailgate of a pickup truck parked at a field gate, seen from behind at distance, head turned away and no face in the frame [STYLE] Avoid: [NEG]

### THUMB（4枚） — サムネ候補。**縦横比は16:9のまま。文字は焼き込まない。**

> ### ★上1/3は空けたまま生成する — これは構図の好みではなく、実測された寸法要件です★
> **空けるのは「フレーム上端から高さの 33%」（1280×720 なら上端から 240px の帯）。**
> その帯には**枝・幹・地平線・柵の線・被写体の一部を一切入れない**こと。
> 根拠（実測値・`scripts/check_thumb_subject_luma.py` と `check_final_acceptance.py`）:
> - 見出し文字は **1280px 幅換算で「連結成分の高さ 150px 以上」**（`TEXT_MIN_HEIGHT = 150`）。
>   150px の1行に上下の縁取り **12px 以上**（`OUTLINE_MIN_PX = 12`）が付くと **174px**。
>   240px の帯なら上下に 33px ずつ余白が残る。**枝が1本でも横切ると縁取りが切れて落ちます。**
> - **帯は明るいこと。** 被写体判定の箱は縦 `y = 0.12〜0.88` と定義されていて**上1/3を含みます**。
>   その箱の平均輝度が **60以上**（`SUBJECT_MIN_LUMA = 60`）必要なので、
>   上を暗い樹冠で埋めると被写体が明るくても落ちます。**上は淡い曇天の空か、明るい霧で埋める。**
> - 完成サムネ全体で **平均輝度 33以上・コントラスト（輝度標準偏差）40以上**
>   （`THUMB_MIN_MEAN_LUMA = 33.0` / `THUMB_MIN_CONTRAST_STD = 40.0`）。
>   **この映画の `[STYLE]` は low contrast なので、この4枚だけは正面から衝突します。**
>   よって**この4枚に限り硬いキーライトで発注**し、**平均輝度 55以上・標準偏差 45以上**を狙います
>   （EP65 は本編と同じ低輝度で発注してしまい、あとから硬いキーライトの1枚を追加する羽目になりました）。
> - 主題は**下2/3の中に置き、水平方向はやや中心から外す**。見出しが2行に折れた場合に
>   上 40% まで使えるようにするためで、**上 33%〜40% の間には主題の芯を置かない**。
>
> **生成後、この4枚は必ず 1280×720 に縮小して**、上1/3が本当に空で明るいかを目で確認すること。

- `L066.png`
A closed steel tube farm gate with a chain and a plain padlock at its latch post, shot dead centre and close from directly in front at chest height, one hard directional key light raking from the left so the wet metal stands out bright against the darker ground, a broad even field of pale bright overcast sky filling the entire upper third of the frame with no branch, no trunk, no wire and no horizon line entering that upper third, the gate and its chain sitting wholly within the lower two thirds and set slightly right of centre [STYLE] Avoid: [NEG]
- `L067.png`
A small dull olive plastic box strapped to a tree trunk with a black webbing strap, seen at very close range from slightly below and set into the lower two thirds of the frame slightly left of centre, one hard directional key light from the right throwing a crisp shadow of the box across the bark, and above it the whole upper third of the frame given over to an even pale bright sky with nothing whatever crossing it [STYLE] Avoid: [NEG]
- `L068.png`
A thick vertical stripe of purple paint on the trunk of a tree, seen close and straight on with the trunk filling the lower two thirds of the frame and standing slightly right of centre, hard light raking across the bark from the left so the paint reads bright and saturated against the grey wood, the upper third of the frame left entirely open as flat pale bright sky with no branch or foliage in it [STYLE] Avoid: [NEG]
- `L069.png`
A blank weathered placard nailed to a tree at head height, its face faded to an even featureless pale surface with no characters or lines on it anywhere, shot dead centre and close with the placard and trunk occupying the lower two thirds of the frame, one hard key light from the left so the board is markedly brighter than the wood behind it, the upper third of the frame an unbroken field of pale bright overcast sky with nothing entering it [STYLE] Avoid: [NEG]

---

## 5.5 ショートのプレートは、この発注には含まれていません

EP65 は §5.5 でショート3本のモチーフを本編プレートの**内数**として突き合わせました。
**EP66 ではそれができません。**`SHORTS_SLATE_EP66` が存在せず、ショートのフックも落ちも決まっていないからです。
**ショート用の発注を先に出さないこと。**先に出せば、後から台本が決まった時点で
「使われないプレート」と「足りないプレート」が同時に生まれます（EP60 でバッチが5本に膨らんだ原因の一つ）。

ショートのスレートが書かれたら、**バッチBの内数として**同じ形式の突き合わせ表を作ります。
各ショートは **16枚以上の distinct plate** を要求します。

---

## 6. 生成後にやること（発注者側）

### 6-0. 発注書そのものの検査（**生成を始める前に済ませてある**）

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP66_openfields_CODEX_BATCH_A.v001.md
```

顔・読める文字・手書き・紋章／記章・数字の**五族すべて**が `[NEG]` に入っていることを機械が確認します。
**`[NEG]` を1語でも削ったら、必ず再実行すること。**

### 6-1. 生成後

1. **全69枚をラベル付きコンタクトシートで目視**する。プロンプトIDで選ばない
   （short60 は3枚がプロンプト一覧どおりに選んで別の絵だった）。
   **特に §1 の Q2（板・樹皮・車体の文字）と Q4（書いていないのに出る顔）を1枚ずつ潰す。**
2. **`L066`–`L069` は 1280×720 に縮小して**上1/3を確認する（§5 THUMB の枠内の要件）。
   4枚とも落ちたら、**本編の絵からサムネを作ろうとしない。**硬いキーライトで再発注する。
3. `episodes/PD-2026-066-openfields/episode_spec.v001.json` の `mandatory_stills` は
   **`L001`–`L065` の65件で既に書いてある。**`L066`–`L069` は**入れない**
   （サムネは本編のカットにならないので、宣言すると `check_spec_satisfied.py` が
   「宣言された静止画がどのカットにも無い」で落ちる。EP65 はこれを後から直した）。
   **QCで不合格になった枚を差し替えたら、その場で `mandatory_stills` も差し替える。**
4. 1枚 = 1モーションクリップとして `remotion/public/openfields/motion/` に書き出す
   （i2v または深度パララックス。**ズーム/パンだけは不可**）。
5. **i2v クリップは書き出した直後に測る。**
   ```
   py -3.11 scripts/check_motion_clip_stillness.py --slug openfields --quarantine
   ```
   ほとんど動いていない 4.8 秒のクリップは、長いスロットに入れられた瞬間にループして
   **near-still 判定で受領書を落とします**（EP65 は 18:53 の 4.03 秒でこれをやりました）。
   契約の `target_cut_sec` は 3.5 に下げてありますが、**それはスロット長の話であって、
   もともと動いていないクリップは別に殺す必要があります。**
6. `py -3.11 scripts/check_episode_inputs.py --slug openfields` を**レンダー前に**通す。
   契約は `distinct_video_assets: 350` を宣言しており、このツールは
   **実写採用 175本**を下限として要求し、`accepted + motion < 350` なら asset_reuse の警告を出します。
   **足りないなら、それはバッチBの枚数が決まったということです**（契約 `notes` の算術を参照）。

### 6-2. バッチBに進む前提（この順に潰す）

| # | 前提 | 出力 |
|---|---|---|
| 1 | 両判決文を CourtListener から取得 | `measurements/EP66_*_RAW.md` |
| 2 | 事実台帳 | `episodes/_planning/EP66_openfields_FACTS_LEDGER.v001.md` |
| 3 | 台本 v001 → `script_verified` | 節ごとの実ナレ語数が確定 |
| 4 | 棚の実測（register ごと） | 実写採用本数 → i2v プレート数が確定 |
| 5 | バッチB発注 | 区分別配分・HOOK 5枚・約束→回収表・ショート内数表 |
| 6 | `mandatory_stills` に追記 | 65 → 最終件数 |
