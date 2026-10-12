# EP79 alaska261 — 差し替え 6枚

> **192枚は納品済み・全数測定済み・6枚のコンタクトシート＋専用検査シート2枚を目視済みです。**
> 実測: 192/192・全て 1672x941・300KB未満なし。
> 明るさ中央値 **67.8**（EP77は43.1、EP78は65.2）、90超が **48枚**、暗いのは **11%**。**今までで最良です。**
>
> 差し替えは **6枚**。保存先は同じ `E:\pd-media\05_visuals\alaska261\img\`

**`[STYLE]`** — 各プレートの前に付ける:

> cinematic documentary reconstruction, one practical light source visible in the frame, high contrast, photorealistic, 16:9,

**`[NEG]`** — 各プレートの後ろに付ける:

> Avoid: text, lettering, handwriting, cursive, signature, numerals, numbers, seals, emblems, logos, badge, insignia, human face, facial features, portrait, identifiable person, airline livery, airline tail markings, company colour scheme, low-resolution.

---

### ACT_3

| id | beat | prompt | flags |
|---|---|---|---|
| K193 | K193 | A wide airline maintenance base in brilliant daylight, snow-capped mountains behind, open hangar doors, and **aircraft that are entirely plain unpainted white with completely bare grey tail fins carrying no picture, no symbol and no colour of any kind**, wet apron reflecting the sky | |
| K194 | K194 | An engineer seen from **directly behind, the back of the head filling the frame and no part of the face in view**, leaning over a lit drafting board covered in technical linework, an angled lamp blazing across the paper | P |
| K195 | K195 | Two mechanics **photographed from directly behind, both heads turned away from the camera and no face visible**, working a measurement together inside an aircraft tail cavity, one holding a torque wrench and the other watching a dial gauge, a work lamp blazing between them | P |

### ACT_4

| id | beat | prompt | flags |
|---|---|---|---|
| K196 | K196 | Airline ground crew **seen from directly behind**, arms raised holding illuminated marshalling wands, facing away toward an aircraft on a sunlit apron, hard shadows on the concrete, **the aircraft entirely plain unpainted white with a completely bare tail fin, no picture, no symbol, no colour** | P |

### ENDING

| id | beat | prompt | flags |
|---|---|---|---|
| K197 | K197 | The tail fin of an airliner against a brilliant dawn sky seen from the apron, the fin catching the first light — **the fin is bare polished metal and plain white, completely blank, carrying no picture, no symbol, no stripe and no colour of any kind** | |

### SPARE

| id | beat | prompt | flags |
|---|---|---|---|
| K198 | K198 | An apron in brilliant rain-washed daylight, reflections of parked aircraft in standing water, **every aircraft entirely plain unpainted white with completely bare tail fins carrying no picture, no symbol and no colour of any kind** | |

---

## なぜこの6枚か

### ① K102 / K134 / K163 → K193 / K197 / K198 — **実在ロゴが写っています**

原寸で3枚とも確認しました。**アラスカ航空の実際の尾翼ロゴ（人物の顔の意匠）**が入っています。K163 は5機、K102 は2機＋胴体の文字、K134 は大きく1機。

**これは EP78 のアメリカン航空より重い問題です。**

- **この作品が扱っている当の航空会社です。** 実在の塗装を出すと、実写記録に見えます
- ロゴ自体が**人物の顔の意匠**で、`[NEG]` の顔禁止にも触れます
- 商標です

### ② K146 / K147 / K188 → K194 / K196 / K195 — **顔が写っています**

- **K188** — 整備士2人の顔が両方とも見えています
- **K146** — 製図台の技術者、顔が斜め前から見えています
- **K147** — 誘導員がカメラを向いています（発注書は「後ろ姿」指定）

420pxの専用シートで確定しました。**320pxのコンタクトシートでは判定できません**（EP78で2回誤判定した反省）。

---

## 今回いちばん重要な発見

**この発注書には、生成前から `[NEG]` に `airline livery, airline tail markings, company colour scheme` を入れてありました。**

**それでも実在ロゴが3枚出ました。**

理由ははっきりしています。**slug が `alaska261` なので、モデルが文脈から実在の航空会社を描きます。** 禁止語を後ろに足すだけでは、その引力に勝てません。

**対策は、主題の側に「無地」と書くことです。** EP78 の C167 はそれで一発で直りました。

この差し替え6枚は全部その形で書いてあります ── **「完全に無地の白い機体、尾翼に絵も記号も色も一切なし」**。

**EP80（コンコルディア）にも同じ手当てを先に入れました。** 船なので、実在クルーズ会社の煙突マークが同じ罠になります。

## 納品後（こちらで実行します）

```
py -3.11 scripts/build_plate_contact_sheet.py --slug alaska261 --src E:\pd-media\05_visuals\alaska261\img --per-sheet 32 --cols 8 --cell 260x146
```
そのうえで、**差し替えた6枚は420pxで個別に開いて確認します。**
