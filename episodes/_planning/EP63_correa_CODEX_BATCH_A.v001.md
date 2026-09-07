# EP63 correa — Codex 画像生成 **1本で完結する発注** v001（223枚・1プロンプト1枚）

> ⚠ **2026-08-04 追記：末尾に §7 として3枚(C224-C226)を追加しました。C001-C223 は変更ありません。**

> ## ✅ 今すぐ着手してよいファイルです。**追加バッチは出ません。**
> EP60はバッチが5本に膨らみました。原因は3つとも同じで、**発注時点で構造が決まっていなかった**
> ことです。今回は逆順にしました。**実写を先に測り（54本取り込み・全タイル目視・使えるのは11本）、
> 台本を実測して8区分の語数を出し、区分ごとに枚数を確定させてから**この発注を書いています。
> **どの区分にも絵があります。**§4の表がその証明で、割付は台本の実語数そのものです。
> 枚数の根拠は `EP62_65_IMAGE_BUDGET.v001.md`：契約 `distinct_video_assets` 234 − 実写採用11 = **223**。

**題材:** *Correa v. Hospital San Francisco*, 69 F.3d 1184 (1st Cir. 1995)。プエルトリコ、1991年9月6日。
65歳の女性が胸痛を訴えて救急室に入り、**番号を渡された**。誰も彼女を断らなかった。誰もその番号を呼ばなかった。

**この映画は「医療事故」の話ではありません。**遅れが死因だと判決はどこにも書いていません。死因は
別の施設で医師の管理下に起きた **hypovolemic shock** です。この映画が扱うのは、**何も起こらなかった部屋**です。

> ### ★この発注が普通と違う点。**「何も起きていない絵」を発注しています。**
> 並んだ空の椅子。手の中の紙片。廊下。番号が出るはずの、何も出ていない壁。誰もいない受付。
> 何時間か経って床を移動していく光。**棚には「無人の受付カウンター」も「番号表示」も1本もありません。**
> ここは全部この発注で作ります。人物・事件・処置を描く発注ではありません。

> ### ★★ 品質水準（オーナー指示 2026-08-04）：**脚本賞の水準で撮る**
> 1枚ごとに**視点がある**こと。「何が写っているか」ではなく、**どの距離から・どの光で・どの瞬間に**
> 見ているかを指定してあります。プロンプトのその部分を削らないでください。
> **ストックカタログ調は全枚不合格です。**均等に明るい、正面から、意味の中心が真ん中で説明的、
> という絵は作らない。**光は片側から。奥は落とす。時刻が分かる。**

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**
3. **「良いのが出るまで回す」を禁止する。**
4. 作り直してよいのは §1 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。

EP60はこの規則で **279枚・変種0・指定外0・sha256重複0・知覚的近似重複0** を達成済み。

---

## 1. ★絶対条件（触れた絵は使用不可）

`episodes/PD-2026-063-correa/episode_spec.v001.json` の `forbidden_subjects` がこの節の正典です。

- **Gonzalez 氏本人を描かない。**その死・最期の数時間・遺体、いずれも一切描かない。
  年配の女性が主役に見える絵を作らない。彼女は**画面に出ません**。
- **医療緊急事態を演出しない。**倒れる人・救命カート・心肺蘇生・波形が平坦になったモニター。全部不可。
  **緊迫した処置の絵は1枚もありません。**この映画に緊急事態の絵はありません。
- **人体への臨床行為を描かない。**出血・傷・手術・注射・腕に刺さった点滴・搬送中の患者。
  医療機器は**人から離れて、単体で、使われていない状態**でのみ描く。
- **実在と特定できる病院・建物を描かない。**この病院はプエルトリコに実在します。特徴的な建築・紋章・
  ファサードで場所が割れる絵は不可。
- **読める文字・数字・署名・印章・ロゴ・案内表示を描かない。**★この話で最も事故が起きやすいのは
  **紙の整理券**です。整理券には**何も印字されていない**状態で描くこと。数字を書かせない。
  壁の番号表示も**消灯した空のパネル**として描く。
- **法廷内観を描かない。**木槌・判事席・傍聴席。棚の法廷映像は61話で使い切っています。**裁判所は外観のみ可。**
- **監獄を描かない。**鉄格子・有刺鉄線・独房・手錠。この話は収監の話ではありません。
- **記録の人物（Correa 家・Rojas 医師・病院職員）の肖像を描かない。**人物は全員「実在しない一般人」。
  **職員を人格として描かない**（判決も誰一人特定していません）。
- **同情の演出を禁止する。**肩に置かれた手、涙、カウントダウンする時計、寄り添う家族の顔。
- **1991年である。**現代のスマホ・液晶モニター・LED照明・現代の車・現代的な光る病院建築は不可。
- **リゾート広告にしない。**ヤシ並木のビーチ、絵葉書、黄金色の夕陽、ドローンの映え。
  舞台は熱帯ですが、**湿って曇った公共施設の熱帯**です。
- **黒つぶれさせない。**スマホで見て何が写っているか分かること。

> **2点だけ、明示的に許可します（誤って弾かないこと）。**
> ① **静止した文字盤の壁時計**は可（`C031`）。禁止なのは「カウントダウンする時計」という演出であって、
>   壁に掛かって止まって見える時計ではありません。文字盤は**無地**にすること。
> ② **天秤ではない「同一の計量皿2枚」**は可（`C098`）。チャンネルは司法の天秤を使いすぎており
>   （`footage_diversity` の汎用象徴 ≤2）、この発注に**司法の天秤は1枚もありません**。
>   `C098` は「even-handedly（等しく扱う）」の絵であって、正義の象徴ではありません。

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字・署名がある（**整理券・カルテ・カレンダー・時計の文字盤を特に見る**） |
| Q3 | 印章・紋章・ロゴ・館内案内表示らしきものがある |
| Q4 | 人物に対する臨床行為（点滴・注射・蘇生・搬送・診察）が写っている |
| Q5 | 倒れている人・救命カート・波形モニター・救急車内の患者が写っている |
| Q6 | 出血・傷・包帯・手術野が写っている |
| Q7 | 法廷内観・木槌・鉄格子・手錠が写っている |
| Q8 | 実在の病院と特定できる建築・ファサード・紋章がある |
| Q9 | 現代の機材（液晶・スマホ・LED・現代の車）が写っている／またはリゾート広告調・ストックカタログ調である |

**顔について。**`C211`〜`C220` を含め、**全223枚で識別できる顔を出さない。**背中・手・シルエット・
遠景の人影のみ。1枚でも正面顔が出たらその枚は不合格です。

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, Puerto Rico in September 1991, humid Caribbean daylight diffused through high white cloud, muted desaturated colour, low contrast, low-key but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, painted concrete and terrazzo surfaces, louvred jalousie windows, ceiling fans, worn institutional pale green and cream paint, early-1990s public-hospital and modest domestic period detail, humidity visible in the air and on the surfaces, nothing glossy and nothing modern, single-source directional light with the far side of the room allowed to fall away, restrained observational documentary framing, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> text, lettering, numerals, digits, handwriting, signatures, seals, emblems, logos, signage, wayfinding arrows, room numbers, brand marks, a person collapsing, a patient on a gurney, a stretcher with a person on it, crash cart, defibrillator, CPR, chest compressions, flatline monitor, heart trace, ECG, blood, wounds, bandages, surgery, injections, a drip line in an arm, a body, a corpse, doctors or nurses treating a person, medical distress, courtroom interior, gavel, judge's bench, prison bars, razor wire, handcuffs, a hand on a shoulder, tears, crying, a clock counting down, modern smartphone, flat-screen monitor, LED lighting, modern cars, glossy modern hospital architecture, palm-fringed resort, beach, postcard scenery, golden hour, sunset glow, drone shot, oversaturated, flat CGI, cartoon, illustration, stock photography, catalogue lighting, evenly lit product shot, stock-photo smiling, human face, face, facial features, eyes, eye contact, looking at the camera, portrait, headshot, close-up of a person, recognisable person, identifiable person, a person facing camera, profile of a face, smiling, expression
>
> **★ 2026-08-05 追加（ここから先の生成に適用）**：上の `[NEG]` には **顔を抑える語が1つも入っていなかった**。制服・バッジ・ロゴは禁じていたが、人を描かせない語は無かった。
> 守っていたのは個々のプロンプト本文の「no face」だけで、**人を一言も書いていない発注には保護がゼロ**だった。
> 実際に EP62 `G174`（発注＝記録室）と EP65 `R019`（発注＝紙）`R041`（発注＝法令集）が、**完全に識別可能な顔**で戻ってきた（invariant 11 違反）。
> この追加は**今後生成する枚にのみ効く**。既存の枚は `runs/qc/` の目視記録で判定する。

---

## 3. 命名と保存先

- ファイル名 `C001.png` … `C223.png`。**欠番を作らない。**
- 保存先 `H:\pd-media\assets\ai\correa\`。
- 長辺 3840px 以上・16:9・PNG。

---

## 4. 区分と枚数（合計223枚）— **台本の実語数で割り付け**

台本 `EP63_correa_script.en.v001.md` を機械計測（ナレーション語のみ・`【】` と `⟨HELD⟩` を除外）:
**総計 5,360語**。

> ### ★ HOOK は**8秒**です（オーナー変更 2026-08-04）
> `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` row 9 により、HOOK は50秒の導入部ではなく
> **本編の最強ビートを2秒刻みで3〜4枚見せる flash-forward** になりました。台本のHOOK節は
> 別途書き換えられます（この発注では台本に触れません）。
> したがって **HOOK は5枚**、`C001`–`C005`。**この5枚は223枚中で最も強い絵**で、視聴者が最初に見る
> 5枚です。そして row 9 の promise-payoff により、**5枚とも本編に「同じモチーフの後続プレート」を
> 必ず持っています**（下の対応表）。フックが約束した絵は、必ず本編で回収されます。

| HOOK プレート | 何の約束か | 本編での回収先 |
|---|---|---|
| `C001` 手の中の白紙の整理券 | 彼女が受け取った唯一のもの | `C136` `C137` `C207` `C221` |
| `C002` 空の待合椅子の列 | 2時間半 | `C138` `C163` `C210` `C222` |
| `C003` 何も出ていない番号表示 | 呼ばれなかった番号 | `C162` `C206` `C223` |
| `C004` 誰もいない受付カウンター | 誰も断らなかった | `C014` `C133` |
| `C005` 湿気で曇った救急入口の扉 | 中に入った、という事実だけ | `C197` `C209` |

223 − HOOK 5 − OP 5 − PEOPLE 10 − THUMB 3 = **200枚**を ACT_1〜ENDING へ、実語数 5,177語で
最大剰余法により按分しています。

| 区分 | 秒 | 台本語数 | 全体比 | 枚数 | ID | 中身 |
|---|---|---|---|---|---|---|
| HOOK | 0:00–0:08 | — | — | 5 | `C001`–`C005` | **8秒の flash-forward。**本編最強の5枚。全て後で回収 |
| OP | — | 44 | 0.8% | 5 | `C006`–`C010` | ブランド。無地のテクスチャ |
| ACT_1 | 1:15–6:45 | 772 | 14.4% | 30 | `C011`–`C040` | 朝。争いのある証言。番号と保険証。待つこと。診療所。1時の電話 |
| ACT_2 | 6:45–12:15 | 1,074 | 20.0% | 41 | `C041`–`C081` | 原告7人。評決と金額。EMTALAという法律の作り |
| ACT_3 | 12:15–17:45 | 1,129 | 21.1% | 44 | `C082`–`C125` | 「適切な」という語。病院自身の4つの規則。**記録が1枚も無い** |
| ACT_4 | 17:45–23:45 | 998 | 18.6% | 39 | `C126`–`C164` | 灰色。列に並んでいただけ、という主張。constructive dumping |
| ACT_5 | 23:45–27:35 | 828 | 15.5% | 32 | `C165`–`C196` | 放棄された抗弁。納屋の戸。家族という幹 |
| ENDING | 27:35–30:00 | 376 | 7.0% | 14 | `C197`–`C210` | 何を決めていないか。方法。そして番号へ戻る |
| PEOPLE | — | — | — | 10 | `C211`–`C220` | 人物プレート（顔なし規則・`people_plates_min: 10`） |
| THUMB | — | — | — | 3 | `C221`–`C223` | サムネ候補（`thumbnail_candidates_min: 3`） |
| **計** | | **5,360** | **100%** | **223** | | |

**実写11本が埋める場所（＝ここに絵を厚くしなくてよい唯一の帯）:** 待合の広い引き・白いベンチのパン・
明るい受付ロビー・エレベーター前の扉4種・蛍光灯・モノクロの雨。**それ以外は全部この223枚です。**

---

## 5. プロンプト（各1枚）

### HOOK（0:00–0:08・5枚） — ★**この5枚が全体で最も強い絵**。2秒刻みで最初に出る。

- `C001.png`
A small paper ticket standing upright between a thumb and a forefinger held close to the lens, the ragged fibres along its top edge catching a single hard sidelight, its face completely blank and unprinted, the waiting room behind it falling away into soft green shadow, centred in the frame [STYLE] Avoid: [NEG]
- `C002.png`
A row of linked steel-and-vinyl waiting chairs photographed at seat height straight down its whole length, every seat empty, one shaft of window light falling across the third seat and the far end of the row swallowed by humid haze, centred in the frame [STYLE] Avoid: [NEG]
- `C003.png`
A wall-mounted display panel where a number should be, its glass dead black and reflecting only the empty room, the painted concrete around it bleached white by a strip light just outside the frame, shot square on and close, centred in the frame [STYLE] Avoid: [NEG]
- `C004.png`
A reception counter of chipped laminate seen from the exact height of somebody standing at it, nobody behind it, the chair beyond pushed back and empty, a hand bell sitting out of reach on the far side, centred in the frame [STYLE] Avoid: [NEG]
- `C005.png`
The double swing doors of an emergency entrance from outside at one o'clock in the afternoon, the glass so fogged with humidity that the room beyond is only a smear of green light, the handles worn bright, centred in the frame [STYLE] Avoid: [NEG]

### OP（5枚） — ブランド。無地。

- `C006.png`
A flat expanse of worn terrazzo floor filling the frame at a grazing angle, one soft band of window light lying across it, no horizon and no object [STYLE] Avoid: [NEG]
- `C007.png`
A painted concrete wall in institutional pale green filling the frame, one hairline crack running off the top edge and a damp bloom rising from the bottom [STYLE] Avoid: [NEG]
- `C008.png`
A flat white overcast tropical sky filling the frame with a single sagging utility line crossing one corner, no ground [STYLE] Avoid: [NEG]
- `C009.png`
The ribbed underside of a concrete entrance canopy seen from directly below against pale sky, rust bleeding from the joints [STYLE] Avoid: [NEG]
- `C010.png`
Extreme close texture of woven vinyl chair upholstery worn through to the padding at one corner, raking light across the weave [STYLE] Avoid: [NEG]

### ACT_1（1:15–6:45・30枚） — 朝。争いのある証言。待つこと。1時の電話。

- `C011.png`
A bedroom at first light with a louvred jalousie window, a glass of water and a folded handkerchief on the nightstand, the bed empty with the sheet thrown back, the room still half in blue shadow [STYLE] Avoid: [NEG]
- `C012.png`
The open passenger door of a plain early-1990s sedan at a kerb seen from the pavement, nobody in it, the vinyl seat cracked and the footwell dark, morning heat already on the road [STYLE] Avoid: [NEG]
- `C013.png`
A low concrete public hospital building seen from the far side of an empty car park under white cloud, the frame held wide and flat, nothing on the building to identify the institution, no people [STYLE] Avoid: [NEG]
- `C014.png`
A reception counter photographed from the queue side at shoulder height, the counter surface empty and the station behind it unoccupied, waiting-room light falling across the laminate from the left, centred in the frame [STYLE] Avoid: [NEG]
- `C015.png`
Two identical plastic chairs side by side against a painted wall, a folded coat on one of them and the other empty, flat frontal light, centred in the frame [STYLE] Avoid: [NEG]
- `C016.png`
A hand resting flat on the edge of a laminate counter in the foreground, the far side of the counter empty and out of focus, no face and nothing beyond the forearm [STYLE] Avoid: [NEG]
- `C017.png`
The frosted glass panel of a reception hatch pulled shut, seen from the waiting side, a shape moving behind it that cannot be resolved into a person [STYLE] Avoid: [NEG]
- `C018.png`
A plastic insurance card lying face down on a laminate counter, edges worn soft, nothing printed visible on the back, one hard reflection sliding off the plastic [STYLE] Avoid: [NEG]
- `C019.png`
A plastic card being set down on laminate by two fingers, caught at the moment it touches, no face in frame, the card face blank [STYLE] Avoid: [NEG]
- `C020.png`
A card wallet lying open on a table with every sleeve empty, the vinyl cracked white along the fold [STYLE] Avoid: [NEG]
- `C021.png`
A wire basket of blank paper slips standing on a counter, the slips unprinted and lifted at the corners by the humidity [STYLE] Avoid: [NEG]
- `C022.png`
A steel spike file on a counter with a dozen blank slips impaled on it, the lowest ones yellowed, shot low so the spike breaks the skyline of the counter [STYLE] Avoid: [NEG]
- `C023.png`
A large ledger book lying open on a counter, its pages ruled into columns and entirely unwritten, one page lifting in the fan draught [STYLE] Avoid: [NEG]
- `C024.png`
A wall payphone in a tiled corridor with the handset off the cradle and hanging on its steel cord, still swinging, nobody near it [STYLE] Avoid: [NEG]
- `C025.png`
A wall payphone with a single coin resting on the ledge beneath it and the cord hanging slack, close, the tiles behind it sweating [STYLE] Avoid: [NEG]
- `C026.png`
A terrazzo floor with a long parallelogram of window light lying across it, dust turning slowly in the beam, nothing else in the frame [STYLE] Avoid: [NEG]
- `C027.png`
The same terrazzo floor with the parallelogram of light moved a metre along and narrowed to a blade, later in the afternoon [STYLE] Avoid: [NEG]
- `C028.png`
A pedestal electric fan standing in the corner of a waiting room, its cage furred grey with dust, the blades completely still [STYLE] Avoid: [NEG]
- `C029.png`
A ceiling fan turning slowly seen from directly below against a ceiling stained brown by old water [STYLE] Avoid: [NEG]
- `C030.png`
Louvred jalousie slats half open, humid white light coming through them and lying in flat stripes across a painted sill [STYLE] Avoid: [NEG]
- `C031.png`
A plain round wall clock high on painted concrete in a waiting room, its face blank and unmarked and the hands still, dust along the top of the rim, shot from below, centred in the frame [STYLE] Avoid: [NEG]
- `C032.png`
A waiting room seen from a high corner, half the chairs empty and the few distant figures too far away and too soft to resolve, the light dropping off toward the back wall [STYLE] Avoid: [NEG]
- `C033.png`
An empty corridor of closed doors receding, a fluorescent strip overhead and the far end falling into shadow, centred in the frame [STYLE] Avoid: [NEG]
- `C034.png`
A fluorescent ceiling fitting with one tube dead and the other caught mid-flicker, the painted ceiling stained around it, centred in the frame [STYLE] Avoid: [NEG]
- `C035.png`
A doorway into an examination room seen from the corridor, the room empty, the couch bare, the light inside switched off and only corridor light reaching the floor, centred in the frame [STYLE] Avoid: [NEG]
- `C036.png`
A stainless steel trolley standing empty against a corridor wall, one castor turned outward, a long reflection of the strip light down its side [STYLE] Avoid: [NEG]
- `C037.png`
A small storefront clinic doorway on an ordinary humid street, the roller shutter half up and the interior dark, nothing on the frontage to identify it [STYLE] Avoid: [NEG]
- `C038.png`
A narrow clinic corridor with a row of plastic chairs against one wall, all empty, a floor fan at the far end and the light coming only from a doorway [STYLE] Avoid: [NEG]
- `C039.png`
A wheeled drip stand standing alone in the corner of an empty room, no bag and no line on it, its shadow long across the tiles [STYLE] Avoid: [NEG]
- `C040.png`
A plain white van parked at a kerb with its rear doors standing open, the load space completely empty, nothing on the panels, late afternoon [STYLE] Avoid: [NEG]

### ACT_2（6:45–12:15・41枚） — 原告7人。評決と金額。法律の作り。

- `C041.png`
A long kitchen table laid with plates and glasses for many people, every chair empty, shot straight down its length in humid afternoon light, centred in the frame [STYLE] Avoid: [NEG]
- `C042.png`
A stack of plain white plates on a bare tabletop, the top one slightly off square, shot at table height so the stack breaks the horizon, centred in the frame [STYLE] Avoid: [NEG]
- `C043.png`
Seven mismatched chairs drawn up around one table, all of them empty, seen from directly above [STYLE] Avoid: [NEG]
- `C044.png`
Four small child-sized chairs in a row against a painted wall, nobody near them, flat frontal light, centred in the frame [STYLE] Avoid: [NEG]
- `C045.png`
A doorway looking through into an empty living room with a sofa, a floor fan and a switched-off television set of the period, the room lit only from a window off frame, centred in the frame [STYLE] Avoid: [NEG]
- `C046.png`
A framed photograph lying face down on a sideboard, only its paper backing board and the turned clips visible, dust around where it stood [STYLE] Avoid: [NEG]
- `C047.png`
A hook beside a door carrying one plain coat and one straw hat, the wall behind them rubbed dark by years of use, centred in the frame [STYLE] Avoid: [NEG]
- `C048.png`
An empty pew of plain varnished wood in a small church, light coming through a shuttered window from the side in slats, centred in the frame [STYLE] Avoid: [NEG]
- `C049.png`
A federal courthouse exterior in flat overcast daylight, plain stone and tall windows, unadorned, nothing on it to identify it, shot square on from across the street [STYLE] Avoid: [NEG]
- `C050.png`
The wide steps of a public building seen from the bottom looking up, empty, still dark and wet from rain [STYLE] Avoid: [NEG]
- `C051.png`
A pair of heavy exterior doors closed, brass handles worn bright by hands, no markings of any kind on them [STYLE] Avoid: [NEG]
- `C052.png`
A corridor of a public building with a wooden bench along one wall, nobody sitting on it, the light coming from a window at the far end [STYLE] Avoid: [NEG]
- `C053.png`
A bench outside a closed door with one folded jacket left on it, shot square on, centred in the frame [STYLE] Avoid: [NEG]
- `C054.png`
A closed office door with a blank metal plate on it where a name would be, the screws standing proud, close and slightly low [STYLE] Avoid: [NEG]
- `C055.png`
A legal brief squared on a desk under a lamp, its cover blank, a paperclip biting the top corner [STYLE] Avoid: [NEG]
- `C056.png`
A stack of case files tied with cotton tape, every cover blank, the tape frayed where it has been knotted and cut many times [STYLE] Avoid: [NEG]
- `C057.png`
A manual typewriter on a desk with a sheet in the platen, the typing on it dissolved into grey texture, the keys catching a low lamp [STYLE] Avoid: [NEG]
- `C058.png`
A wire out-tray on a desk holding a single folder and nothing beneath it [STYLE] Avoid: [NEG]
- `C059.png`
Two hands closing a card folder flat on a table, caught at the moment the cover meets the paper, no face in frame, the cover blank, centred in the frame [STYLE] Avoid: [NEG]
- `C060.png`
A metal filing cabinet drawer half open with unlabelled folders standing in it, the drawer front dented at knee height [STYLE] Avoid: [NEG]
- `C061.png`
A row of identical bound volumes on a shelf, every spine blank, raking light picking out the ribs [STYLE] Avoid: [NEG]
- `C062.png`
One volume drawn half out of a shelf of identical volumes, the gap behind it black [STYLE] Avoid: [NEG]
- `C063.png`
A reading desk under a single lamp at night with one closed book on it, nobody there, the rest of the room gone to dark [STYLE] Avoid: [NEG]
- `C064.png`
Twelve plain wooden chairs arranged in two rows in an otherwise empty panelled room, no bench and no gallery, one window's light across them [STYLE] Avoid: [NEG]
- `C065.png`
A plain lectern standing alone in an empty panelled room, no bench, no gallery and no flags, shot from the back of the room [STYLE] Avoid: [NEG]
- `C066.png`
A plain table with three empty chairs behind it in a bare room, flat light from one side, the wall behind unmarked [STYLE] Avoid: [NEG]
- `C067.png`
Coins and folded banknotes counted out on a wooden table, the denominations not legible, no hands in frame, one hard lamp above [STYLE] Avoid: [NEG]
- `C068.png`
A paper envelope of banknotes lying on a bare table with the notes half out, nothing printed on the envelope [STYLE] Avoid: [NEG]
- `C069.png`
Seven small stacks of coins standing in a line on a wooden surface, three tall and four short, shot at surface level so they read as a skyline [STYLE] Avoid: [NEG]
- `C070.png`
A rubber date stamp resting face down on a dried-out ink pad, the wooden handle worn to the grain, centred in the frame [STYLE] Avoid: [NEG]
- `C071.png`
A wire tray of blank forms on an office counter, the office behind it plain and unbranded and out of focus [STYLE] Avoid: [NEG]
- `C072.png`
A bound statute volume lying open on a desk, the type on both pages dissolved into grey texture, the gutter deep in shadow [STYLE] Avoid: [NEG]
- `C073.png`
A single page held up to a window so the light comes through it, the print reduced to soft grey texture and the paper's fibres showing, centred in the frame [STYLE] Avoid: [NEG]
- `C074.png`
A dictionary open flat on a table under a lamp, the columns of words reduced to unreadable grey, one page held down by a thumb at the edge, centred in the frame [STYLE] Avoid: [NEG]
- `C075.png`
An office corridor of the period with frosted glass doors down both sides, nobody in it, one door lit from within [STYLE] Avoid: [NEG]
- `C076.png`
A ceiling fan and two fluorescent fittings in a government office seen from directly below, the plaster cracked between them [STYLE] Avoid: [NEG]
- `C077.png`
A hospital corridor at night with warm light spilling from one open doorway onto the floor and nothing else lit [STYLE] Avoid: [NEG]
- `C078.png`
A pair of corridor swing doors caught mid-swing as they close, the panels blurred with the movement, nobody visible on either side, centred in the frame [STYLE] Avoid: [NEG]
- `C079.png`
A closed lift door in a tiled lobby, the call plate blank and unlit, scuff marks along the bottom edge where trolleys have hit it [STYLE] Avoid: [NEG]
- `C080.png`
A stairwell of poured concrete seen from the bottom step looking up, the treads chipped, daylight only at the top [STYLE] Avoid: [NEG]
- `C081.png`
A telephone handset lying off its cradle on a desk with the coiled cord pulled taut off the edge of the table [STYLE] Avoid: [NEG]

### ACT_3（12:15–17:45・44枚） — 「適切な」という語。4つの規則。記録が1枚も無い。

- `C082.png`
A policy manual lying closed on a desk, its cover plain and unmarked, a lamp switched off beside it, the room grey [STYLE] Avoid: [NEG]
- `C083.png`
A ring binder open flat on a table, its pages ruled and completely blank, the rings sprung open and empty [STYLE] Avoid: [NEG]
- `C084.png`
A corridor noticeboard with nothing pinned to it, only the holes left by drawing pins in the sun-bleached cork [STYLE] Avoid: [NEG]
- `C085.png`
A staff room table with the chairs pushed in and a jug and a stack of cups on it, nobody there, the light off [STYLE] Avoid: [NEG]
- `C086.png`
Rows of folding chairs facing a blank painted wall in a bare training room, every one of them empty [STYLE] Avoid: [NEG]
- `C087.png`
A blank flip-chart pad on an easel in an otherwise empty room, the first sheet curling forward [STYLE] Avoid: [NEG]
- `C088.png`
A microphone on a stand on a plain table pointing at an empty chair, shot from the chair's side of the table [STYLE] Avoid: [NEG]
- `C089.png`
Two hands folded on a plain table in a bare room, ordinary sleeves, no face and no insignia, one lamp from the left [STYLE] Avoid: [NEG]
- `C090.png`
A glass of water half drunk standing beside a closed folder on a table, the condensation ring already spreading [STYLE] Avoid: [NEG]
- `C091.png`
A reel-to-reel tape recorder on a table with the reels turning, no labels anywhere on it, close on the moving tape [STYLE] Avoid: [NEG]
- `C092.png`
A stenotype machine on its stand with a ribbon of blank paper folding into a basket beneath it [STYLE] Avoid: [NEG]
- `C093.png`
A wall of a hundred identical small ceramic tiles with exactly one of them chipped away at the corner, shot square on and flat [STYLE] Avoid: [NEG]
- `C094.png`
A concrete facade of identical windows with one shutter closed among all the open ones, shot flat from across the street [STYLE] Avoid: [NEG]
- `C095.png`
A dictionary page at extreme magnification, the letterforms dissolved into grey fibre texture, the paper's tooth raised by sidelight, centred in the frame [STYLE] Avoid: [NEG]
- `C096.png`
A shapeless cloud front seen from the ground with its edges shifting, humid white sky filling the frame, no land [STYLE] Avoid: [NEG]
- `C097.png`
The same white sky reflected in a shallow puddle on cracked concrete, the reflection breaking as a drop lands [STYLE] Avoid: [NEG]
- `C098.png`
Two identical steel weighing trays side by side on a plain bench, exactly level and both empty, hard sidelight, centred in the frame [STYLE] Avoid: [NEG]
- `C099.png`
A fan of identical blank paper tickets spread across a counter, none of them printed, centred in the frame [STYLE] Avoid: [NEG]
- `C100.png`
A wall-mounted ticket dispenser with a blank tongue of paper hanging from its slot, close, the paint around it worn by fingers, centred in the frame [STYLE] Avoid: [NEG]
- `C101.png`
A clipboard hanging on a hook beside a doorway with the form clipped to it entirely blank, centred in the frame [STYLE] Avoid: [NEG]
- `C102.png`
A rubber stamp standing on end on a desk, its rubber face blank and uncut, one hard light behind it, centred in the frame [STYLE] Avoid: [NEG]
- `C103.png`
A pen resting across a blank printed form on a desk, not touching the paper's edge, shot close and low, centred in the frame [STYLE] Avoid: [NEG]
- `C104.png`
A corridor with two doors facing each other, one shut and one standing open onto a dark room, centred in the frame [STYLE] Avoid: [NEG]
- `C105.png`
An examination couch with fresh paper unrolled across it in an otherwise empty room, nobody in the room, the paper still curling from the roll, centred in the frame [STYLE] Avoid: [NEG]
- `C106.png`
A sphygmomanometer cuff coiled on a metal shelf beside a folded towel, unused, nobody near it, close [STYLE] Avoid: [NEG]
- `C107.png`
An aneroid gauge hanging on a wall bracket with its dial face blank and unmarked, the glass dusty [STYLE] Avoid: [NEG]
- `C108.png`
A wooden chart rack on a corridor wall with every slot standing empty, the wood worn pale along the top edge [STYLE] Avoid: [NEG]
- `C109.png`
An empty document trolley parked against the wall of a records corridor, one shelf bowed from years of weight [STYLE] Avoid: [NEG]
- `C110.png`
A records room of steel shelving with every shelf bare, lit only by a single high window at the far end [STYLE] Avoid: [NEG]
- `C111.png`
A single cardboard document box standing open on a floor with nothing inside it, shot from above [STYLE] Avoid: [NEG]
- `C112.png`
A filing drawer pulled fully out and completely empty, the runner exposed beneath it, close [STYLE] Avoid: [NEG]
- `C113.png`
A hand running along an empty shelf edge with the dust line visible where it has passed, no face in frame [STYLE] Avoid: [NEG]
- `C114.png`
A bare metal hook at the foot of an empty bed frame where a chart would hang, nothing on it, shallow focus [STYLE] Avoid: [NEG]
- `C115.png`
A hospital bed with a bare striped mattress in an empty room, the curtain rail above it stripped, one window's light across the foot [STYLE] Avoid: [NEG]
- `C116.png`
A painted wall with four clean rectangles where notices once hung, the paint around them faded by years of sun [STYLE] Avoid: [NEG]
- `C117.png`
A wall with four empty picture hooks in a row and nothing on any of them, shot square on [STYLE] Avoid: [NEG]
- `C118.png`
A blank paper form curling upward on a counter in the humidity, unprinted on both visible faces [STYLE] Avoid: [NEG]
- `C119.png`
A wastepaper basket holding crumpled blank sheets, seen from directly above [STYLE] Avoid: [NEG]
- `C120.png`
A basket of shredded paper ribbons beneath a desk, no print visible on any strip, one shaft of light across it [STYLE] Avoid: [NEG]
- `C121.png`
A doorway into a records office with the light off inside, seen from a lit corridor, the threshold sharp against the dark [STYLE] Avoid: [NEG]
- `C122.png`
A desk with an empty in-tray on one side, an empty out-tray on the other, and nothing at all between them [STYLE] Avoid: [NEG]
- `C123.png`
A glass jar of cotton wool and a kidney dish on a bare metal tray, nothing else on the tray, hard overhead light [STYLE] Avoid: [NEG]
- `C124.png`
An empty vehicle bay outside a low building marked only by worn paint on the concrete, no vehicle in it, shot flat and wide [STYLE] Avoid: [NEG]
- `C125.png`
A fluorescent strip flickering over an empty corridor with half the tube dark, the floor pooled with uneven light, centred in the frame [STYLE] Avoid: [NEG]

### ACT_4（17:45–23:45・39枚） — 灰色。列に並んでいただけ、という主張。

- `C126.png`
A single empty wooden bench in a waiting room held wide and dead still, the room silent around it, one window's light reaching only the near end, centred in the frame [STYLE] Avoid: [NEG]
- `C127.png`
The same bench close, the varnish worn through to pale wood exactly where people sit [STYLE] Avoid: [NEG]
- `C128.png`
A flat grey humid sky with no sun and no horizon, filling the entire frame [STYLE] Avoid: [NEG]
- `C129.png`
Wet terrazzo reflecting a soft grey rectangle of window and nothing else at all [STYLE] Avoid: [NEG]
- `C130.png`
A corridor lit only by daylight from one end, the far end falling away into grey shadow, shot from the dark end [STYLE] Avoid: [NEG]
- `C131.png`
A stack of grey card folders with their edges uneven, seen from the side against a plain wall [STYLE] Avoid: [NEG]
- `C132.png`
A chair pulled back from a table at an angle, as if somebody had just stood up from it, the light already going [STYLE] Avoid: [NEG]
- `C133.png`
A counter position with a stool behind it and nobody on the stool, the surface bare, shot from the public side, centred in the frame [STYLE] Avoid: [NEG]
- `C134.png`
A queue barrier of two posts with the rope hanging slack between them and nobody in the line [STYLE] Avoid: [NEG]
- `C135.png`
A worn strip of floor paint marking where a queue stands, the paint rubbed away in patches by feet, nobody on it [STYLE] Avoid: [NEG]
- `C136.png`
A blank paper ticket lying face up on an empty chair seat, unprinted, one hard light across the vinyl, centred in the frame [STYLE] Avoid: [NEG]
- `C137.png`
The same ticket on the floor beneath the chair with one edge curled up by the humidity [STYLE] Avoid: [NEG]
- `C138.png`
The row of waiting chairs seen from the far end with one chair pushed out of line and all of them empty, the floor scuffed pale in front of them, centred in the frame [STYLE] Avoid: [NEG]
- `C139.png`
A wall telephone in a corridor with the handset in its cradle and the cord looped once over the box [STYLE] Avoid: [NEG]
- `C140.png`
A hand lifting a telephone handset from a wall cradle, caught at the moment it clears the hook, no face and nothing beyond the forearm [STYLE] Avoid: [NEG]
- `C141.png`
A telephone cord stretched taut across a doorway at knee height, nobody visible at either end of it [STYLE] Avoid: [NEG]
- `C142.png`
A desk telephone on an empty clinic desk with the receiver lying off beside it, the desk lamp still on [STYLE] Avoid: [NEG]
- `C143.png`
An open doorway seen from inside a dim room onto a bright humid street, the figures outside burnt out by the light and unidentifiable [STYLE] Avoid: [NEG]
- `C144.png`
A car key and a folded handbag left on a plastic waiting-room chair, nobody near them [STYLE] Avoid: [NEG]
- `C145.png`
A car pulling away from a kerb seen from behind through heat haze, the registration indistinct, the road empty ahead [STYLE] Avoid: [NEG]
- `C146.png`
An empty parking bay with old oil marks on the concrete and weeds pushing through the joint [STYLE] Avoid: [NEG]
- `C147.png`
A road seen through a car windscreen in rain with the wipers caught mid-sweep, the street beyond dissolved [STYLE] Avoid: [NEG]
- `C148.png`
The doorway of a small clinic seen from a car window across a wet street, framed by the door pillar [STYLE] Avoid: [NEG]
- `C149.png`
Rain beginning on hot concrete, the dark spots spreading and joining into each other, close and flat [STYLE] Avoid: [NEG]
- `C150.png`
A downpour on a flat concrete roof with water sheeting off the edge in an unbroken curtain [STYLE] Avoid: [NEG]
- `C151.png`
A covered concrete walkway between two buildings in heavy rain, nobody in it, the far end lost in spray [STYLE] Avoid: [NEG]
- `C152.png`
An empty waiting room seen from outside through a window streaked with running rain, the chairs softened to shapes [STYLE] Avoid: [NEG]
- `C153.png`
A door with a chain and padlock across it and nothing hanging on the door itself [STYLE] Avoid: [NEG]
- `C154.png`
A clean rectangle of paint on a wall where a board was taken down, the empty bracket still bolted in place [STYLE] Avoid: [NEG]
- `C155.png`
A wall bracket with no plate in it, the screw holes open and the metal streaked with rust [STYLE] Avoid: [NEG]
- `C156.png`
A plain white envelope lying alone on a counter, unaddressed and unopened, one hard light from the side [STYLE] Avoid: [NEG]
- `C157.png`
A plastic card lying alone on a dark counter with its face blank, hard side light raking across the scratches [STYLE] Avoid: [NEG]
- `C158.png`
A card being drawn out of a wallet by two fingers with nothing printed on it, no face in frame [STYLE] Avoid: [NEG]
- `C159.png`
A cash drawer standing half open with coins loose in the trays and nobody behind it [STYLE] Avoid: [NEG]
- `C160.png`
A payment window with the metal shutter pulled down from the inside and the ledge below it bare [STYLE] Avoid: [NEG]
- `C161.png`
A corridor of doors with one standing wide open onto a completely empty room, shot from the far end [STYLE] Avoid: [NEG]
- `C162.png`
The wall display panel again at dusk, the glass dark and the face still entirely blank, corridor light behind it, centred in the frame [STYLE] Avoid: [NEG]
- `C163.png`
The row of waiting chairs at dusk with the room lights not yet switched on and every seat empty, the windows the brightest thing left, centred in the frame [STYLE] Avoid: [NEG]
- `C164.png`
The entrance doors seen at dusk from the far side of the car park with nobody going in or coming out [STYLE] Avoid: [NEG]

### ACT_5（23:45–27:35・32枚） — 放棄された抗弁。納屋の戸。家族という幹。

- `C165.png`
A wooden barn door standing half open on its iron hinges with the interior beyond it black, shot square on, centred in the frame [STYLE] Avoid: [NEG]
- `C166.png`
The same barn door caught swinging, motion smeared through the planks, the yard beyond it empty, centred in the frame [STYLE] Avoid: [NEG]
- `C167.png`
An empty stall inside a barn with straw scattered on the floor and the far door standing open to daylight [STYLE] Avoid: [NEG]
- `C168.png`
A padlock hanging open on a hasp, the door it was meant to hold already ajar behind it [STYLE] Avoid: [NEG]
- `C169.png`
A horseshoe half buried in dry cracked earth with no hoofprints anywhere around it [STYLE] Avoid: [NEG]
- `C170.png`
A row of empty coat pegs in a hallway with one straw hat left on the end peg [STYLE] Avoid: [NEG]
- `C171.png`
A desk diary lying open flat with its ruled pages entirely blank and a pen beside it untouched [STYLE] Avoid: [NEG]
- `C172.png`
A conference table with eight chairs, one pushed back, blank papers squared in front of every place [STYLE] Avoid: [NEG]
- `C173.png`
An empty chair at the head of a long polished table seen straight down its length [STYLE] Avoid: [NEG]
- `C174.png`
A folded agenda sheet lying on a table, unprinted on every visible face [STYLE] Avoid: [NEG]
- `C175.png`
A hand pushing a stack of paper across a table toward the far edge, no face in frame, caught mid-slide [STYLE] Avoid: [NEG]
- `C176.png`
A chain of paperclips lying across a blank page on a desk, close [STYLE] Avoid: [NEG]
- `C177.png`
A thick trial bundle standing upright on a shelf with its spine blank, leaning slightly against the next [STYLE] Avoid: [NEG]
- `C178.png`
A wooden gate left standing open into an empty yard with the latch hanging free [STYLE] Avoid: [NEG]
- `C179.png`
The front of a modest house of the period with jalousie windows and a low painted wall, nothing on it to identify the address, shot flat from the street [STYLE] Avoid: [NEG]
- `C180.png`
The front room of a family home with one empty armchair and a floor fan, curtains half drawn, the fan not turning [STYLE] Avoid: [NEG]
- `C181.png`
A sideboard with a lace runner and a glass vase on it and no photographs anywhere along its length [STYLE] Avoid: [NEG]
- `C182.png`
A kitchen with a covered pot standing on the stove and nobody attending it, the window open onto white sky [STYLE] Avoid: [NEG]
- `C183.png`
A dining table with the cloth on and no places laid, every chair pushed right in [STYLE] Avoid: [NEG]
- `C184.png`
A sewing basket open on a chair with thread, scissors and a folded cloth in it [STYLE] Avoid: [NEG]
- `C185.png`
A doorway between two rooms with a printed cotton curtain half drawn across it and light on the far side [STYLE] Avoid: [NEG]
- `C186.png`
The corridor of a family house with three doors, one of them ajar and lit from within, the rest dark [STYLE] Avoid: [NEG]
- `C187.png`
A bed made up tight with a folded blanket at its foot, the room otherwise bare, one window's light across the cover [STYLE] Avoid: [NEG]
- `C188.png`
A pair of house slippers set neatly side by side beside a bed on a tiled floor [STYLE] Avoid: [NEG]
- `C189.png`
A large tree trunk cut clean through, the pale fresh face of the stump raw in the light, the ground around it cleared [STYLE] Avoid: [NEG]
- `C190.png`
The same stump seen from directly above with the growth rings clear and nothing marked on it [STYLE] Avoid: [NEG]
- `C191.png`
A felled trunk lying across dry ground with every branch already taken off it [STYLE] Avoid: [NEG]
- `C192.png`
A family group standing together in a doorway photographed from behind, every face away from camera, plain clothes of the period, centred in the frame [STYLE] Avoid: [NEG]
- `C193.png`
Four pairs of children's sandals lined up by a door with no children anywhere in the frame [STYLE] Avoid: [NEG]
- `C194.png`
An empty rocking chair on a tiled porch, completely still, the light going out of the yard behind it [STYLE] Avoid: [NEG]
- `C195.png`
A hallway light left burning in an otherwise dark house, seen from the street through a louvred jalousie [STYLE] Avoid: [NEG]
- `C196.png`
A stack of unopened envelopes on a hall table, none of them addressed legibly, dust along the top one [STYLE] Avoid: [NEG]

### ENDING（27:35–30:00・14枚） — 何を決めていないか。そして番号へ戻る。

- `C197.png`
A wide view of the low hospital building at dawn under a pale sky, no people anywhere, nothing on it to identify it [STYLE] Avoid: [NEG]
- `C198.png`
An empty waiting room at first light with the chairs in their rows and the entrance doors shut, the strip lights still off [STYLE] Avoid: [NEG]
- `C199.png`
Four blank paper forms laid side by side on a counter, every one of them unprinted, shot from directly above [STYLE] Avoid: [NEG]
- `C200.png`
An empty document tray standing beside those four forms with nothing in it at all [STYLE] Avoid: [NEG]
- `C201.png`
A single sheet of blank paper falling through still air against a dark neutral ground, caught halfway down [STYLE] Avoid: [NEG]
- `C202.png`
An open ledger with ruled lines and no entries on either page and a pen lying beside it untouched [STYLE] Avoid: [NEG]
- `C203.png`
An empty chart rack on a wall with every slot open, the wood worn smooth at the top edge [STYLE] Avoid: [NEG]
- `C204.png`
A hand pulling open a filing drawer that is completely empty, caught at full extension, no face in frame [STYLE] Avoid: [NEG]
- `C205.png`
A corridor with every door shut and the lights off, daylight reaching only the far end, shot from the dark end, centred in the frame [STYLE] Avoid: [NEG]
- `C206.png`
The dark blank display panel filling the frame, close, the glass reflecting only the empty corridor, centred in the frame [STYLE] Avoid: [NEG]
- `C207.png`
A blank paper ticket lying alone on an empty chair seat, seen from directly above, centred in the frame [STYLE] Avoid: [NEG]
- `C208.png`
The same chair seen from the front with the ticket gone and the seat empty [STYLE] Avoid: [NEG]
- `C209.png`
The entrance doors seen from inside with daylight beyond them and nobody coming through, centred in the frame [STYLE] Avoid: [NEG]
- `C210.png`
The row of waiting chairs photographed straight on in flat morning light with every seat empty, identical framing to the opening image, centred in the frame [STYLE] Avoid: [NEG]

### PEOPLE（10枚） — 人物プレート。**全員実在しない一般人。顔は絶対に出さない。**

- `C211.png`
A woman in her sixties in a plain print dress of the period seated at the far end of a row of waiting chairs, seen from directly behind, face not visible, the room dropping into shadow around her [STYLE] Avoid: [NEG]
- `C212.png`
The hands of an older woman resting in her lap holding a folded blank paper slip, no face in frame, one window's light on the knuckles [STYLE] Avoid: [NEG]
- `C213.png`
A man in his forties in a plain short-sleeved shirt standing at a reception counter with his back to camera, face not visible, shot from the waiting room behind him [STYLE] Avoid: [NEG]
- `C214.png`
A woman's silhouette against a louvred jalousie window in a dim room, features not resolvable at all [STYLE] Avoid: [NEG]
- `C215.png`
Two adults seated side by side on a waiting-room bench seen from behind, only shoulders and the backs of their heads, one leaning forward [STYLE] Avoid: [NEG]
- `C216.png`
A pair of working hands resting on a laminate counter top, no face, no jewellery, sleeves plain, hard light from one side [STYLE] Avoid: [NEG]
- `C217.png`
A person in a plain pale tunic walking away down a corridor seen from far behind, no badge and no insignia anywhere, already half in shadow [STYLE] Avoid: [NEG]
- `C218.png`
An adult's hand and an older person's hand resting side by side on the arm of a chair, both cropped at the wrist, no faces [STYLE] Avoid: [NEG]
- `C219.png`
The back of a woman's head and shoulders in a doorway looking into a lit corridor, face not visible [STYLE] Avoid: [NEG]
- `C220.png`
A family of several people on a porch at dusk photographed from behind, every face away from camera, plain clothes of the period, centred in the frame [STYLE] Avoid: [NEG]

### THUMB（3枚） — サムネ候補。**縦横比は16:9のまま。文字は焼き込まない。**

- `C221.png`
A blank paper ticket held up close in a hand, dead centre in the frame, hard directional light and deep shadow behind it, the composition leaving the upper third of the frame clear for a headline [STYLE] Avoid: [NEG]
- `C222.png`
One empty chair in a row of empty waiting chairs, shot dead centre and low, strong side light raking across the seats, upper third of the frame clear [STYLE] Avoid: [NEG]
- `C223.png`
A dark blank display panel on a painted wall, dead centre, hard raking light across the wall texture, upper third of the frame clear [STYLE] Avoid: [NEG]

---

## 5.5 ショート3本のプレートは、この223枚の**内数**です

`SHORTS_SLATE_EP62-65.v001.md` の `short262` / `short263` / `short264` が要求するモチーフを、上のプロンプトに
1つずつ突き合わせた表です。**ショート用の二度目の発注は出しません。**
下表に出るプレートは**主題が画面中央**にあり、左右を切っても意味が壊れないように文言を書いてあります
（該当プロンプトには `centred in the frame` が入っています）。

| `short262`「病院は断らなかった。番号を呼ばなかっただけ」 | 使うプレート |
|---|---|
| 手の中の整理券（フック＝frame 0・**印字なし**） | `C001` |
| 並んだ空の待合椅子 | `C002` `C138` |
| 何も出ていない番号表示 | `C003` `C162` `C206` |
| 誰もいない受付カウンター | `C004` `C014` `C133` |
| 閉じた扉が続く廊下 | `C033` `C205` |
| 上着が1つ残ったベンチ | `C053` |
| 文字盤が無地の壁時計 | `C031` |
| 閉じていくスイングドア | `C078` |
| 明滅する蛍光灯 | `C034` `C125` |
| 戸口から見た無人の処置室 | `C035` `C105` |
| 列から少しずれた椅子 | `C138` |
| 同じ部屋の、暗くなった後 | `C163` |
| **ループ結合** | `C163` → `C001` |

| `short263`「Appropriate は辞書で最も見事なごまかし語だ」 | 使うプレート |
|---|---|
| 活字が灰色に溶けた条文ページ（フック＝frame 0） | `C073` |
| 開いた辞書・読めない語 | `C074` `C095` |
| 白紙の書式に置かれたペン | `C103` |
| 水平な同一の計量皿2枚（＝even-handedly。**司法の天秤ではない**） | `C098` |
| 同一の椅子2脚・片方に上着 | `C015` |
| 同じ整理券が並ぶ | `C099` `C100` |
| 二つの扉が向き合う廊下、片方だけ開いている | `C104` |
| フックに掛かった白紙のクリップボード | `C101` |
| 文字の無いスタンプ | `C102` `C070` |
| **ループ結合** | `C101` → `C073` |

| `short264`「その金は死に対してではない。待ち時間に対してだ」 | 使うプレート |
|---|---|
| 大人数分の食卓、誰もいない（フック＝frame 0） | `C041` |
| 重ねた皿 | `C042` |
| 無人の居間への戸口 | `C045` |
| 子ども用の小さな椅子4脚 | `C044` |
| フックの上着 | `C047` |
| 後ろ姿の家族（顔なし） | `C192` `C220` |
| 揺れる納屋の戸（判決自身の比喩） | `C165` `C166` |
| 無人の教会の長椅子 | `C048` |
| フォルダを閉じる手 | `C059` |
| **ループ結合** | `C059` → `C041` |

> **縦位置の制約。** ショートは 1080×1920 です。生成後の目視で、**9:16に切ったサムネイルも並べて確認**して
> ください。端に寄った構図（例：`C113` の画面端の手、`C143` の遠景の人影）はショートに使わず、長尺のみに
> 使います。
> **`short264` の縛り:** `$200,000` は「待っている間の苦痛」に対する賠償です。**死に対する対価として
> 見える絵**（棺・墓・遺影）はこの発注に1枚もありません。作らないでください。

---

## 6. 生成後にやること（発注者側）

1. **全223枚をラベル付きコンタクトシートで目視**する。プロンプトIDで選ばない
   （short60は3枚がプロンプト一覧どおりに選んで別の絵だった）。
   **特に整理券・時計・カルテ・カレンダーの写った枚は、数字が出ていないか1枚ずつ拡大して見る。**
2. **`C001`–`C005` を最初に見る。**8秒のフックはこの5枚で決まります。5枚のうち1枚でも凡庸なら、
   その枚だけ文言を強めて作り直す（§0の「回す」禁止はこれに優先されません — 作り直しは1回、1枚）。
3. `episodes/PD-2026-063-correa/episode_spec.v001.json` の `mandatory_stills` は **現在 223件で確定済み**。
   プレートは全部で 227枚だが、**THUMB の4枚（`C221` `C222` `C223` `C227`）は意図的に外してある**。
   サムネは本編のカットにならないので、宣言すると `check_spec_satisfied.py` が
   「宣言された静止画がどのカットにも無い」で落ちる。**書き直さないこと。**
   空のままだと `check_spec_satisfied.py` の唯一の保護が無効になります（EP54はここが空で、
   棚に無いから作らせた14枚が完成品から消えました）。
4. 1枚 = 1モーションクリップとして `remotion/public/correa/motion/` に書き出す
   （i2v または深度パララックス。**ズーム/パンだけは不可＝紙芝居**）。
5. `python scripts/check_episode_inputs.py --slug correa` で
   **accepted(11) + motion ≥ 234** をレンダー前に確認する。

---

## 7. ★追加発注（2026-08-04・v001 に後から足した3枚）

設計マニュアル §2① が名指しする二つのツール（`scan_video_shape` と `check_cross_episode_reuse`）を
実写プールに通した結果、**コンタクトシートでは絶対に見えない理由で 3本が落ちました**。720p が2本
（`AR-6997951` クリニック受付へ歩く二人 / `AR-9384` 待合室の水槽）と、縦位置が1本
（`AR-v_171138` エレベーター扉の開き）です。**絵の良し悪しではなく画枠の問題**なので、目視 QC では
検出できません。採用実写は **11本 → 8本**、したがって発注枚数は契約 `distinct_video_assets` 234 −
実写採用8 = **223枚 → 226枚**になります。

**失われた2つの register は、プール中で最も良い絵でした。**待合室の**水槽**はこのプール唯一の
「待合室の中で動いている物」であり、**クリニックの受付**は受付の絵2本のうちの1本でした。
以下の3枚は、**その register を作り直すための発注**です。C001–C223 は一枚も変わっていません。
§5.5 のショート対応表にも入りません（`centred in the frame` を付けていないのはそのためです）。

| ID | 置く場所（台本 v002 の実ビート） | どの実写 register の代わりか |
|---|---|---|
| `C224` | **ACT_1**「Then the waiting.」以降の待機帯（`C026`/`C027` の光の移動と同じ列） | `AR-9384` 待合室の水槽＝**部屋の中で唯一動いている物** |
| `C225` | **ACT_1** 到着（"She was inside no later than one o'clock in the afternoon."） | `AR-6997951` **受付へ歩いていく二人**（受付 register の2本目） |
| `C226` | **ACT_4**「No refusal required. No words required. Nothing has to be said to anybody.」 | `AR-v_171138` **開くエレベーター扉**（誰の決定も要らずに開く扉） |

- `C224.png`
A glass aquarium tank on a painted metal stand against the wall of a waiting room, the water lit from within and slightly clouded, one thread of bubbles and a frond of weed drifting in it, the rest of the room fallen away into green shadow with the empty chairs showing only as shapes in the glass, shot low from the height of a seat [STYLE] Avoid: [NEG]
- `C225.png`
Two figures seen from well behind crossing a wide terrazzo floor toward a reception counter at the far end of a room, both small in the frame and turned away, the second half a step behind the first, one shaft of doorway light lying across the floor between them and the counter, the counter itself unattended, faces not visible at all [STYLE] Avoid: [NEG]
- `C226.png`
A lift door standing fully open onto an empty car in a tiled lobby, the interior of the car lit and completely bare, the call plate beside it blank and unlit, nobody waiting on the landing and no hand anywhere near the button, the landing in shadow so the open car is the brightest thing in the frame, shot square on from a few paces back [STYLE] Avoid: [NEG]

> ⚠ **§6-5 の読み替え（本文は直していません）。**`check_episode_inputs.py --slug correa` の合格条件は
> **accepted(11) + motion ≥ 234** ではなく、**accepted(8) + motion(226) ≥ 234** です。§1〜§6 は
> Codex が走っている最中なので一字も触っていません。**差分はこの §7 と冒頭1行だけです。**

**この3枚にも §0〜§3 がそのまま適用されます。**1プロンプト1枚・`_02` を作らない・顔を出さない・
読める文字と数字を出さない・長辺3840px以上・保存先 `H:\pd-media\assets\ai\correa\`。
生成後は §1 の Q1–Q9 と §6-1 の目視を **C224–C226 にも**通してください。

### ★追加（2026-08-04・サムネ用のC227）

thumb_prompts.v001.md の THUMB-04。既存の THUMB 3枚（C221–C223）はこの話の低輝度な [STYLE] を継いでおり、thumbnail_visibility（平均輝度33以上）を割る危険がある。この1枚は明るい直射光で発注する。

**この1枚はパッケージング専用で、本編のカットには入らない。したがって `mandatory_stills` には追加しない**（check_spec_satisfied.py は「宣言された静止画がどのカットにも無い」で落ちる）。

- `C227.png`
A shallow wooden filing drawer pulled fully open on a painted metal cabinet and completely empty inside, the bare board of its base showing, the runners and the dust line where files used to stand still visible, one hard shaft of daylight falling squarely into the open drawer so the inside of it is the brightest thing in the frame, the cabinet and the room around it a stop down but keeping their detail, no paper anywhere and nobody in the room, the upper third of the frame left clear [STYLE] Avoid: [NEG]

合計 **227枚**（うち本編 223枚 + PEOPLE 10 + THUMB 4）。
★ **サムネプレートだけは本編の低輝度指定を上書きし、平均輝度38以上・標準偏差45以上を狙うこと。**

### ★再発注（2026-08-05・目視QCの結果、必須）

モチーフの連鎖（**一つの物の八つの状態**）を目視した。**状態4 と 状態7 の「同じ座席」が3脚とも別の椅子だった。**

| プレート | 指定 | 生成されたもの |
|---|---|---|
| `C136` 状態4 | その座席 | 茶色レザーの胘なし椅子・目線 |
| `C207` 状態7 | **同じ座席を真上から** | オリーブ色のプラ椅子。しかも切符が**切り込み入りの映画チケット**に変わっている |
| `C208` 状態7完了 | **同じ座席を真上から・切符が消えている** | 緑のビニール胘掛け椅子・目線の引き。**真上ですらない** |

つまり **状態7 が完成せず、ループの落ちが存在しない**。EP62 の `G226` と同じ失敗で、原因も同じ——発注文が「同じ座席」としか書いておらず、**1プロンプト＝1枚では前の枚を参照できない**。

以下は **座席と切符の特徴を毎回全部書き下す**。`C136` は良いので残し、その椅子を正典とする。

| 新 | 置き換え |
|---|---|
| `C228` | C207 の代替（状態7・切符あり） |
| `C229` | C208 の代替（状態7完了・**映画の落ち**） |

- `C228.png`
Looking straight down from directly overhead onto the SAME seat as C136 and no other: a single mid-century waiting-room side chair with no arms, its seat and its low rounded back upholstered in dark reddish-brown leatherette scuffed pale along the front edge, carried on a slim black tubular steel frame with four splayed legs, standing on a grey terrazzo floor in a Puerto Rican municipal clinic with pale green dado paint on the wall behind, the chair filling the frame square to the camera, and lying face-up at the centre of the seat a small blank slip of pale cream paper, a plain rectangle with four straight cut edges, no notches, no perforations, no scalloped ends, no printing, no numerals and no writing of any kind on it, flat humid daylight from a window out of frame, nobody in the picture and no other chair in the picture [STYLE] Avoid: [NEG]

- `C229.png`
Looking straight down from directly overhead onto the SAME seat as C136 and no other: a single mid-century waiting-room side chair with no arms, its seat and its low rounded back upholstered in dark reddish-brown leatherette scuffed pale along the front edge, carried on a slim black tubular steel frame with four splayed legs, standing on a grey terrazzo floor in a Puerto Rican municipal clinic with pale green dado paint on the wall behind, the chair filling the frame square to the camera in exactly the same position and at exactly the same distance as before, the seat now completely empty with no paper and no slip anywhere in the frame, the worn pale patch on the leatherette where things are set down still showing, flat humid daylight from a window out of frame, nobody in the picture and no other chair in the picture [STYLE] Avoid: [NEG]

**`C207` `C208` は廃止。カットに使わない**（削除はしない）。`mandatory_stills` は `C228` `C229` に差し替え済み。

※ 目視QCのもう一件（差し替えなし・要確認）：`C099`（状態2・同じ切符が扇に広げられている）は、廃建物の廀下の引きの中で小さく放射状に並んでおり、**装飾模様に見える**。使えなくはないが弱い。

### ★再発注 2（2026-08-05・全229枚目視QCの不合格10枚）

全229枚を目視した（`runs/qc/correa_plate_verdicts.v001.md`）。**ACCEPT 192 / FLAG 25 / REJECT 10**。寸法不合格0枚、平均輝度25未満も0枚（最暗は `C050` の 48.4）。**10枚とも機械ゲートでは捕まらない。**

- `C223`（サムネ候補）は**数値が全部緑**（平坧62.1・sd48.1）ながら、発注の「暗い無地の表示パネル」に対して**顔がはっきり分かる女性と幼児**で戻ってきた。顔禁止・胖像禁止・**死の演出禁止**を一枚で破っている。
- `C169` `C189` `C191` は**病院の内部にひび割れた大地や倒木が入っている**合成不能の画。`C189` は ACT_5 で最も重い「家系図の幹」のビートである。
- `C137`（モチーフ状態5）は `C207`/`C208` を廃止したのと**同じ欠陥**——胘付きの別の椅子で、切符も影の中の細片。
- `C099`（状態2）は弱いだけでなく、拡大すると**切り込み入りの映画チケット**（`C207` を廃止したのと同じ物）が放射状に並んでいる。

※ `C221` と `C223` を失うとサムネ候補が2枚になり、契約の `thumbnail_candidates_min: 3` を割る。**`C238` `C239` の生成は任意ではない。**

| 新 | 廃止 | 却下理由 |
|---|---|---|
| `C230` | `C095` | ACT_3, the word *appropriate* |
| `C231` | `C099` | ACT_1, motif state 2, the identical blanks |
| `C232` | `C128` | ACT_4, the grey |
| `C233` | `C137` | ACT_2, motif state 5, the ticket on the floor |
| `C234` | `C169` | ACT_5, the barn-door group |
| `C235` | `C189` | ACT_5, *the trunk of the family tree* |
| `C236` | `C191` | ACT_5, the felled trunk |
| `C237` | `C206` | ENDING, the number display, close |
| `C238` | `C221` | THUMB, headline `NOBODY CALLED 47` |
| `C239` | `C223` | THUMB, headline `NOBODY SAID NO` |

本文の `[STYLE]` / `[NEG]` は §2 の定義を展開すること（§2 の `[NEG]` には 2026-08-05 に**顔の語を追加済み**）。

- `C230.png`
An extreme macro photograph of a single page of a printed dictionary, the paper filling the entire frame edge to edge with no desk, no room and no background visible at all, the columns of type reduced to soft grey fibrous bands with no letterform anywhere resolvable and no numeral and no word readable, the tooth and fibre of the cheap paper raised into relief by a hard light raking across the sheet from the left, the fold of the gutter running down one side into deep shadow, one corner of the sheet lifted very slightly by humidity, shot square on and so close that the depth of field falls away at the edges of the frame [STYLE] Avoid: [NEG]

- `C231.png`
A loose overlapping row of eight identical small paper slips spread across a chipped laminate counter top and shot close and low from the public side of the counter so the slips fill most of the frame, every slip a plain rectangle of pale cream paper with four straight cut edges and no notches, no perforations, no scalloped or serrated ends and no rounded corners, every slip completely blank and unprinted with no numeral, no letter and no mark of any kind on any of them, the slips fanned unevenly by hand rather than laid in any pattern and slightly curled at the corners by the humidity, one hard shaft of window light from the left raking across the paper so the edges throw small shadows onto the slips beneath, the waiting room behind the counter falling away out of focus into green shadow, nobody in the picture [STYLE] Avoid: [NEG]

- `C232.png`
A flat featureless expanse of grey humid tropical overcast filling the entire frame from edge to edge with no sun, no horizon, no ground, no building, no bird and no object of any kind anywhere in the picture, the cloud a single unbroken sheet with only the faintest tonal drift from very slightly brighter at the lower left to very slightly denser at the upper right, the air visibly heavy with moisture, no break and no edge and nothing to give the eye a scale, photographed straight up at a shallow angle with a long lens so the frame is entirely sky [STYLE] Avoid: [NEG]

- `C233.png`
Looking down at a steep angle from standing height onto the grey terrazzo floor directly beneath a single mid-century waiting-room side chair with no arms, its seat and its low rounded back upholstered in dark reddish-brown leatherette scuffed pale along the front edge, carried on a slim black tubular steel frame with four splayed legs, standing against a wall with pale green dado paint in a Puerto Rican municipal clinic, the chair's legs and the underside of its seat framing the top of the picture and the floor filling the lower two thirds, and lying on the terrazzo beneath the chair a small blank slip of pale cream paper, a plain rectangle with four straight cut edges and no notches, no perforations and no scalloped ends, no printing and no numeral and no writing of any kind on it, one long edge of the slip curled upward by the humidity so it stands slightly clear of the floor, the slip large enough in the frame to be unmistakably a slip of paper, one shaft of flat humid daylight from a window out of frame falling across it so it is the brightest thing in the picture, nobody in the picture and no other furniture in the picture [STYLE] Avoid: [NEG]

- `C234.png`
A worn iron horseshoe lying half buried in bare dry cracked earth in an open yard outdoors under flat white tropical cloud, the ground baked and split into a wide pattern of shallow cracks running out of the frame in every direction, no hoofprint and no track anywhere in the earth around it, a low weathered timber fence and rough dry grass just visible far behind at the top of the frame and nothing else, shot very low from ground level with a long lens so the cracked earth fills the picture and the background is soft, one hard directional light from the side throwing the horseshoe's shadow across the cracks, nobody in the picture and no building in the picture [STYLE] Avoid: [NEG]

- `C235.png`
A large tree stump cut clean through low to the ground outdoors in an open cleared yard of bare earth, the pale raw fresh-cut face of the stump broad and flat and turned toward the camera, its growth rings and the darker heartwood at the centre clearly visible, the dark fissured bark still on its edge and a scatter of pale sawdust and cut chips on the earth around it, the ground around the stump cleared and swept bare with no branches and no leaves left on it, low green scrub and a plain painted concrete boundary wall far behind under flat white tropical cloud, shot from a low kneeling height square on to the cut face with a single hard directional light from the left so the rings are raked and the far side of the stump falls away, nobody in the picture and no building interior in the picture [STYLE] Avoid: [NEG]

- `C236.png`
A long felled tree trunk lying across bare dry ground outdoors in an open yard, every branch already cut away so only the pale round scars where the limbs were remain along its length, the bark dark and fissured and beginning to lift in places, the trunk running diagonally across the frame from the near lower left into the distance and out of focus at the far end, dry cut grass and a few pale wood chips on the ground beside it, a low painted concrete boundary wall and green scrub far behind under flat white tropical cloud, shot from a low height with one hard directional light from the side so the trunk's shadow lies long across the ground, nobody in the picture and no building interior in the picture [STYLE] Avoid: [NEG]

- `C237.png`
A wall-mounted number display panel filling almost the whole frame, shot square on and very close from a few inches back so its steel surround runs off all four edges of the picture, the glass of the panel completely dead black and entirely unlit with no digit, no numeral, no letter, no segment and no glow of any kind anywhere on it, the black glass holding only a very faint dim reflection of an empty unlit corridor and a row of empty chairs, so soft and so dark that nothing in the reflection can be identified, the painted concrete wall around the surround worn and marked by hands at the edges of the frame, a single weak light from one side grazing the steel surround so the panel itself stays the darkest thing in the picture while the surround holds detail, nobody in the picture [STYLE] Avoid: [NEG]

- `C238.png`
A single small blank paper slip held upright between a thumb and a forefinger and raised into the lower middle of the frame, the slip a plain rectangle of pale cream paper with four straight cut edges and no notches, no perforations, no scalloped or serrated ends and no rounded corners, its face completely blank and unprinted with no numeral, no letter and no mark of any kind on it, the ragged fibres along its top edge catching the light, the hand an ordinary adult hand cropped at the wrist with no face and no watch and no ring anywhere in the picture, the slip and the hand together occupying only the lower two thirds of the frame and the entire upper third of the frame left completely clear and empty of any object, a waiting room of empty chairs falling away behind into deep soft shadow, hard directional light from one side striking the slip squarely, , the subject itself brightly and evenly lit and clearly the brightest thing in the frame, the background dark but never crushed and still holding visible detail, high local contrast between the subject and the ground, graded up for legibility on a phone screen at 320 pixels wide [STYLE] Avoid: [NEG]

- `C239.png`
A wall-mounted number display panel on a painted concrete wall, dead centre in the frame and large in it, its glass completely blank and unlit with no digit, no numeral, no letter, no segment and no glow of any kind anywhere on it and no reflection in which anything can be identified, its plain steel surround dented at one corner, the pale green and cream painted wall around it raked hard from one side by a single directional light so the trowel marks, the damp bloom and the flaking paint of the concrete stand out in relief, the panel sitting in the lower two thirds of the frame with the entire upper third of the frame left completely clear and empty of any object, no person anywhere in the picture, no hand, no face, no figure and no reflection of a figure, , the subject itself brightly and evenly lit and clearly the brightest thing in the frame, the background dark but never crushed and still holding visible detail, high local contrast between the subject and the ground, graded up for legibility on a phone screen at 320 pixels wide [STYLE] Avoid: [NEG]

**廃止：`C095` `C099` `C128` `C137` `C169` `C189` `C191` `C206` `C221` `C223`。カットに使わない（削除はしない）。**
※ **`C238` `C239` はサムネ専用なので `mandatory_stills` には追加しない。** 本編の 8枚は差し替え済み。

### ★再発注 3（2026-08-06・新規10枚の目視の結果）

`C230` と `C232` は**まったく別の画**が来た。どちらも発注は「**X だけで画面を埋める**」であり、モデルはそれを無視して**情景を作った**。

| 新 | 廃止 | 何が起きたか |
|---|---|---|
| `C240` | `C230` | 発注は「辞書の1ページの極接写・部屋も背景も写さない」だったが、**診療所の廊下**が来た |
| `C241` | `C232` | 発注は「灰色の曇天が画面全体・地平線も建物も無い」だったが、**街と海の遠景**が来た |

対策は2つ。一つは **「画面を埋める質感」として肯定形で書く**こと、もう一つは **モデルが実際に手を伸ばした情景の語（部屋・廊下・建物・街・海・地平線）を Avoid に入れる**こと。旧発注にはどちらも無かった。

- `C240.png`
A macro photograph of the surface of a single page of cheap printed paper, so close that the paper's own fibres and tooth are the subject and the sheet fills every part of the frame from edge to edge with nothing else in the picture at all, the printed columns present only as soft grey fibrous bands with no letterform, no numeral and no word resolvable anywhere, one hard light raking across the surface from the left so the fibre stands up in relief and the shallow valley of the gutter falls away into shadow at one side, one corner of the sheet very slightly lifted by humidity, the focus falling off at the extreme edges of the frame. The paper is the ONLY thing in the photograph. cinematic still, muted natural colour, humid tropical Caribbean light, low contrast, restrained documentary framing, Puerto Rico in 1991, worn unglamorous surfaces, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage. Avoid: text, lettering, numerals, digits, handwriting, signatures, seals, emblems, logos, signage, wayfinding arrows, room numbers, brand marks, human face, facial features, eye contact, portrait, identifiable person, people, hands, golden hour, sunset glow, drone shot, oversaturated, flat CGI, cartoon, illustration, stock photography, a room, an interior, a corridor, a hallway, a doorway, a wall, a floor, furniture, a desk, a table, a window, a building, a city, rooftops, a street, a coastline, the sea, a horizon, a landscape, sky with anything in it, any object at all, any scene, any depth, any background whatever

- `C241.png`
A photograph of nothing but overcast cloud, the grey humid tropical sky filling every part of the frame from edge to edge as one unbroken sheet, no sun and no bright spot anywhere in it, the tone drifting only very faintly from a little lighter at the lower left to a little heavier at the upper right, the cloud's texture soft and almost featureless with no defined edge and no break. The camera is pointed straight up at the sky and nothing else is in the photograph. cinematic still, muted natural colour, humid tropical Caribbean light, low contrast, restrained documentary framing, Puerto Rico in 1991, worn unglamorous surfaces, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage. Avoid: text, lettering, numerals, digits, handwriting, signatures, seals, emblems, logos, signage, wayfinding arrows, room numbers, brand marks, human face, facial features, eye contact, portrait, identifiable person, people, hands, golden hour, sunset glow, drone shot, oversaturated, flat CGI, cartoon, illustration, stock photography, a room, an interior, a corridor, a hallway, a doorway, a wall, a floor, furniture, a desk, a table, a window, a building, a city, rooftops, a street, a coastline, the sea, a horizon, a landscape, sky with anything in it, any object at all, any scene, any depth, any background whatever

