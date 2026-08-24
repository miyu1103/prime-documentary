# EP80 concordia — 差し替え 4枚

> **181枚は納品済み・全数測定済み・専用検査シート2枚を目視済みです。**
> 明るさ中央値 **94.6**（EP79は67.8）、90超が **97枚**、暗いのは **14枚**。**過去最高です。**
> **人物プレート25枚は全数合格** ── 全部後ろ姿かシルエットで、顔は1枚もありません。
>
> 差し替えは **4枚**。保存先は同じ `E:\pd-media\05_visuals\concordia\img\`

**`[STYLE]`** — 各プレートの前に付ける:

> cinematic documentary reconstruction, one practical light source visible in the frame, high contrast, photorealistic, 16:9,

**`[NEG]`** — 各プレートの後ろに付ける:

> Avoid: text, lettering, handwriting, cursive, signature, numerals, numbers, seals, emblems, logos, badge, insignia, human face, facial features, portrait, identifiable person, yellow funnel, coloured funnel, ship funnel markings, company colour scheme, low-resolution.

---

### ACT_1

| id | beat | prompt | flags |
|---|---|---|---|
| N182 | N182 | The lit superstructure of a very large cruise ship at night seen from the sea, every deck window blazing, calm dark water, **the funnel is plain matt white from base to cap, exactly the same white as the hull, with no yellow, no black band, no symbol and no colour anywhere on it** | |
| N183 | N183 | A very large cruise ship at a Mediterranean quay in brilliant daylight, gangways down, the white hull blown out where the sun strikes, **the funnel plain matt white from base to cap, the same white as the hull, with no yellow, no black band, no symbol and no colour anywhere on it** | |
| N184 | N184 | A cruise ship seen from directly astern at night, her wake glowing white under the deck floodlights, open sea, **the funnel plain matt white from base to cap with no yellow, no black band, no symbol and no colour anywhere on it** | |

### ACT_4

| id | beat | prompt | flags |
|---|---|---|---|
| N185 | N185 | An engineering render of a ship's watertight subdivision, two compartments picked out in bright colour against a dark hull profile, edge-lit, no lettering, **a clean technical diagram only — no photographic ship, no funnel, no livery, no vessel in the background** | |

---

## なぜこの4枚か

**N003 / N009 / N019 / N111 の煙突が、コスタ社の色になっています。**

原寸で N009 を確認しました。**船体は真っ白・社名なし・記号なし** ── そこまでは指示どおりです。**ただし煙突が黄色＋黒帽**で、これはコスタ・クルーズの識別色そのものです。

**EP79 のアラスカ航空ロゴほど重くはありません。** 商標のマークも社名も出ていません。**色だけ**です。

ただし発注書は「**煙突も含めて会社色を一切入れない**」と明記していたので、指示からは外れています。**4枚だけ直します。**

---

## 今回わかったこと（EP79 の対策は「半分」効きました）

EP80 は生成前に、船の外観が写る8枚のプロンプト本体へ
「**船体も煙突も完全に無地、社名・記号・会社色を一切入れない**」を書き足してありました。

**結果：船体は8枚とも無地・社名なしになりました。煙突だけが会社色を拾いました。**

理由は書き方だと考えています。**「無地」「マークなし」は効きましたが、「色」という指示語が弱かった**。今回の差し替えでは、そこを具体語に置き換えてあります ──

> **the funnel is plain matt white from base to cap, exactly the same white as the hull, with no yellow, no black band**

**「黄色にするな」ではなく「船体と同じ白にしろ」**と、正の指定にしました。

`[NEG]` にも `yellow funnel, coloured funnel` を追加しています。

---

## 納品後（こちらで実行します）

```
py -3.11 scripts/build_plate_contact_sheet.py --slug concordia --src E:\pd-media\05_visuals\concordia\img --per-sheet 32 --cols 8 --cell 260x146
```
そのうえで、**差し替えた4枚は460pxで開いて煙突を確認します。**

---

# 納品確認（2026-08-24 実測・460px目視済み）

| | 明るさ | 煙突 |
|---|---|---|
| N182 | 39.5 | **無地の白** |
| N183 | 155.9 | **無地の白** |
| N184 | 44.1 | **無地の白** |
| N185 | 14.9 | 該当なし（純粋な技術図。写真の船が消えた） |

**4枚とも会社色が消えました。** 「船体と同じ白にしろ」という正の指定が効いています。

N185 の明るさ14.9は黒地のワイヤーフレーム図として正常で、線は明瞭です。

古い4枚（N003 / N009 / N019 / N111）は `E:\pd-media\05_visuals\concordia\_superseded\` へ移動しました。削除ではありません。
**本編に入るのは181枚。**
