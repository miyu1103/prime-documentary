# EP78 colgan — 差し替え 2枚

> **166枚は納品済み・全数測定済み・6枚のコンタクトシートを目視済みです。作り直しではありません。**
> 実測: 166/166・全て 1672x941・300KB未満なし・読める文字なし・顔なし。
> 明るさ中央値 **65.2**（EP77は43.1）、90超が **45枚**（EP77は3枚）。**昼の絵の指示は効きました。**
>
> 差し替えが要るのは**2枚だけ**です。保存先は同じ `E:\pd-media\05_visuals\colgan\img\`

**`[STYLE]`** — 各プレートの前に付ける:

> cinematic documentary reconstruction, one practical light source visible in the frame, high contrast, photorealistic, 16:9,

**`[NEG]`** — 各プレートの後ろに付ける:

> Avoid: text, lettering, handwriting, cursive, signature, numerals, numbers, seals, emblems, logos, badge, insignia, human face, facial features, portrait, identifiable person, airline livery, airline tail markings, company colour scheme, low-resolution.

---

### ACT_4

| id | beat | prompt | flags |
|---|---|---|---|
| C167 | C167 | An airport terminal interior in full daylight, a tall glass wall blowing out bright, two travellers in the foreground seen from behind as dark silhouettes, and beyond the glass **plain unpainted white aircraft with bare metal tails carrying no colour scheme and no markings of any kind**, pale winter sky | P |

### ENDING

| id | beat | prompt | flags |
|---|---|---|---|
| C168 | C168 | A single aircraft navigation light burning against a deep blue pre-dawn sky, blown out white at its core with a visible star flare, the faint silhouette of a wing tip and a band of pale light along the horizon behind it | |

---

## なぜこの2枚か

### ① C123 → C167 — **実在の航空会社の塗装が写っています（最優先）**

納品された C123 には、**アメリカン航空の尾翼塗装をした機体が4機**写っています。赤・白・青の縞の尾翼で、原寸で確認しました。

**問題は2つあります。**

**権利**: 実在企業の識別マークです。

**そしてこちらの方が重い** ── この作品は **Colgan Air が Continental Connection として運航した便**の事故です。**無関係な実在航空会社の機体を映すと、その会社が関係しているように見えます。**

差し替え版では **「塗装も標識も一切ない、素の白い機体」** を明示的に指定しました。

### ② C135 → C168 — 明るさ 3.9

「暗い空に航法灯だけ」という私の指示どおりではあるのですが、**明るさ3.9は事実上の黒画面**です。編集で使えません。

夜明け前の空にして、**灯り以外にも見えるもの**を入れました。

---

## 判断を保留したもの（記録として）

**C014** — 雨に濡れた窓ごしの夜の空港。尾翼が濃紺＋赤で、特定の会社に見えなくもありません。**雨で滲んでいて判別できないため、差し替えません。** 記録だけ残します。

**C157（明るさ10.2）** — 予備プレートなので実害なし。そのまま。

## 目視QCで私が2回間違えました（記録）

コンタクトシート（320px）で **C110（公聴会の傍聴席）と C164（砂漠を歩く2人）に顔が写っている**と判断しました。

**原寸で確認したら、どちらも全員が完全な後ろ姿でした。**

**縮小版では顔の有無は判定できません。** 疑わしい場合は必ず原寸を開くこと。

## この先の発注書に入れた対策

`[NEG]` に **`airline livery, airline tail markings, company colour scheme`** を追加しました。EP79・EP80 の発注書（まだ生成していない）にも同じ行を入れてあります。

---

# 納品確認（2026-08-24 実測・原寸目視済み）

| | 実測 |
|---|---|
| C167 | 1672x941 / 明るさ **123.3** / コントラスト 80.6 |
| C168 | 1672x941 / 明るさ **42.9**（元の C135 は 3.9） |

**C167 は塗装が完全に消えました。** 機体2機とも真っ白で、尾翼に一切マークがありません。人物2人は後ろ姿。

**C168 は翼端灯の星芒＋夜明け前のオレンジの地平線。** 黒画面ではなくなりました。

## 古い2枚を機械的に外しました

`C123.png` と `C135.png` を **`E:\pd-media\05_visuals\colgan\_superseded\` へ移動**しました。削除ではありません。

組み立てはこの `img` フォルダを読むので、**移動しておけば誤って切り込まれません。**
散文の申し送りは実行時に読まれない、という規則に沿った対処です。

そのため `check_plate_delivery --require-all` は **C123 と C135 を「欠品」として報告します。それが正しい状態です。**

**本編に入るのは 166 枚**（166 納品 ＋ 差し替え 2 − 旧 2）。
