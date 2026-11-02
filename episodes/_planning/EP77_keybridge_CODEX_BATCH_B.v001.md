# EP77 keybridge — 追加バッチ B（10枚）

> **本編121枚は納品済み・全数検査済み。作り直しではありません。**
> 実測: 121/121・全て 1672x941・300KB未満なし・読める文字なし・顔なし。
> 明るさは HOOK 30.8 → ENDING 49.0 と**上がっていく**。狙いどおりです。
> 追加はこの10枚だけ。保存先は同じ `E:\pd-media\05_visuals\keybridge\img\`

**`[STYLE]`** — 各プレートの前に付ける:

> cinematic documentary reconstruction, one practical light source visible in the frame, high contrast, photorealistic, 16:9,

**`[NEG]`** — 各プレートの後ろに付ける:

> Avoid: text, lettering, handwriting, cursive, signature, numerals, numbers, seals, emblems, logos, badge, insignia, human face, facial features, portrait, identifiable person, low-resolution.

---

### ENDING

| id | beat | prompt | flags |
|---|---|---|---|
| H122 | H122 | A wide dawn view of an American east-coast industrial harbour, a long steel truss bridge low across the water in the middle distance, container cranes behind it, calm grey water, no towers, no spires, no stone arches | |

### ACT_3

| id | beat | prompt | flags |
|---|---|---|---|
| H123 | H123 | A steel equipment cabinet photographed from a low three-quarter angle in a bright machine room, its door standing open, rows of grey relays inside, daylight from a window at the left | |
| H128 | H128 | A government hearing room in full daylight, empty raked seating, a long bench, tall windows with grey daylight flooding in | |
| H129 | H129 | A wide bright office floor in daytime, rows of empty desks, ceiling panels lit, grey light through a glass wall | |

### ACT_4

| id | beat | prompt | flags |
|---|---|---|---|
| H130 | H130 | A steel truss bridge span in flat overcast midday light seen from the riverbank, grey sky filling the upper half, no fog | |
| H131 | H131 | An open marshalling yard in daylight, stacked shipping containers under a pale sky, wet tarmac reflecting the cloud | |

### HOOK

| id | beat | prompt | flags |
|---|---|---|---|
| H124 | H124 | A steel truss bridge lit end to end by its own roadway lamps against a deep blue pre-dawn sky, seen wide from across the water, the lights burning bright and doubled in the surface | |
| H125 | H125 | The lit deck of a container ship at night seen from above, floodlights blazing across the stacked boxes, the whole frame brightly lit | |
| H126 | H126 | A harbour control room at night, several screens glowing bright, ceiling lights on, an empty chair, no one present | |
| H127 | H127 | A wet roadway on a bridge deck at night under a run of sodium lamps, every lamp lit, the surface throwing the light back brightly | P |

---

## なぜこの10枚か（実測値つき）

**① H122 — 場所が違う（1枚・最重要）**

H120 は**石造アーチの橋と尖塔**で、ヨーロッパの街に見えます。ボルチモアはパタプスコ川に架かる**鋼トラス橋**です。しかもこれは ENDING、**映画の最後の絵**です。

**② H123 — 絵が重複している（1枚）**

H018 と H066 の知覚ハッシュ距離が **5**（16以下で類似、5はほぼ同一）。どちらも「暗い盤面」で、ACT_1 と ACT_3 に離れて入っています。H066 を明るい別アングルに差し替えます。

**③ H124-H127 — HOOK の明るい選択肢（4枚）**

HOOK 6枚の明るさ中央値が **30.8**、うち4枚が35未満です。最初の30秒が離脱を決めます。

**これは欠陥ではありません。夜の事故なので暗いのは正しい。** ただし編集時に「暗い6枚しかない」状態にしたくないので、**明るい候補を4枚持たせます**。使うかどうかは絵を並べてから決めます。

**④ H128-H131 — 昼の絵（4枚）**

121枚のうち明るさ70超が**5枚だけ**、90超は**3枚**です。ACT_3・ACT_4 は法廷と役所の話で、**夜である必要がありません**。全編夜霧＋一灯だと単調になります。

---

## 追加**しない**もの（あえて書きます）

- **H030（明るさ11）は直しません。** 船の停電そのもので、暗いことが事実です
- **H021（15.5）も直しません。** 計器の光だけの操舵室で、指示どおりです
- **H076・H088** も夜の無人室内で、意図どおりです

**暗い＝欠陥ではありません。** 直すのは「場所が違う」「絵が被った」の2枚と、選択肢を増やす8枚だけです。

---

## 納品後

```
py -3.11 scripts/build_plate_contact_sheet.py --slug keybridge --src E:\pd-media\05_visuals\keybridge\img --per-sheet 30 --cols 6 --cell 320x180
```

シートを開いて目で見ます。機械は明るさしか測れません。
