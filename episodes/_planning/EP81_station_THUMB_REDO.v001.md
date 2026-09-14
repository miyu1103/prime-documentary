# EP81 station サムネ作り直し — 3枚だけ **v001**（2026-08-24）

> 経緯: v004納品分の選定（`EP77-82_THUMB_SELECTION.v001.md`）で、station だけ選定保留になった。
> 合格3枚はどれも「きれいなクラブ照明」で、事件（防音フォーム・出口）が1秒で読めない。
> 唯一意味が強かった旧03（緑非常口＋暗い廊下）は5バンド全部帯外で救済不能を実測済み。
> **この発注はその置き換え3枚。他の話数は触らない。**

保存先: `E:\pd-media\05_visuals\thumbs\station_v3\`
ファイル名: **THUMB-06.png / THUMB-07.png / THUMB-08.png**（既存01〜05と別番号。上書き禁止）

---

## 数値目標（`check_thumb_punch.py` がこの帯域で判定）

```
明るさ      42〜78     ← 生成の狙いは 45〜65
コントラスト 60〜95     ← 55以上あれば残りはローカル補正で仕上がる
明るい画素   3〜16 %    ← 狙いは 6〜10 %。3%未満は補正でも救えない＝再生成
暗い画素    35〜72 %
彩度        30〜85
```

**旧03が死んだ理由: 主題が「暗い廊下」だったから。** 今回の3枚はどれも
**光っている面そのものを主題**にする。画面の1/5以上が白飛びしていること。

## `[STYLE]` — 各主題の後ろに貼る

```
, the light source itself is IN the frame and is BLOWN OUT PURE WHITE, a large blazing
highlight filling at least a fifth of the picture with visible lens flare and light shafts,
the subject filling roughly half the picture and brightly lit, saturated colour, extreme
contrast between the blown highlight and one deep shadow side, ultra high resolution,
hyper-detailed, razor-sharp focus, photorealistic, volumetric light, 16:9 thumbnail hero shot,
scroll-stopping
```

## `[NEG]` — 最後に貼る

```
Avoid: on-screen text, letters, numerals, readable documents, watermark, logo, identifiable
real person, faces, bodies, injuries, fire, flames, smoke, burn marks, the moment of the
accident, dim scene, dark room, night interior with a small lamp, evenly dark image, flat
lighting, low contrast, monochrome, desaturated, muted colours, empty black frame, small
distant subject, low-resolution.
```

**⛔ この話は特に: 火・炎・煙・焦げ跡は絶対に出さない**（v003から継続の禁止事項）。
**⛔ 文字は絵に入れない**（オンサムネ文字は後工程でローカル合成する）。

---

## 主題3枚

| # | 主題 | 狙い |
|---|---|---|
| 06 | A single square tile of grey pyramid-pattern acoustic foam held up in a black-gloved hand, a hard work lamp blazing directly into the lens behind it and blown out pure white, every foam pyramid razor sharp and brightly lit, one deep shadow side | 正体不明の物体＝これが100人を殺した（物体ミステリー）。 |
| 07 | A green emergency exit sign at very close range filling the upper third of the frame, its face blazing and blown out white at the core, the corridor below flooded in brilliant green light, walls and floor brightly lit, a huge lens flare from the sign | 旧03の露出改善版。廊下は明るく、サインは至近距離で白飛びさせる。 |
| 08 | An unlit silver pyrotechnic gerb fountain tube clamped to a stage stand at close range, a single hard white stage light blazing directly into the lens behind it with a huge starburst, the metal tube brilliantly rim-lit, empty stage floor brightly lit below | 出火原因の装置（未点火）。火を出さずに火を語る。 |

---

## 手順

```
1. 3枚を生成して保存
2. py -3.11 scripts/check_thumb_punch.py E:\pd-media\05_visuals\thumbs\station_v3
3. 「コントラストだけ不足・明るい画素3%以上」→ そのまま残す（Claude側が
   scripts/thumb_autograde.py で仕上げる）。再生成しない
4. 「明るい画素3%未満」or「明るさ42未満」→ 光源を大きくして、その枚だけ再生成
5. py -3.11 scripts/thumb_feed_sheet.py E:\pd-media\05_visuals\thumbs\station_v3
```

## 正直に書くこと

- 帯域は勝った2枚由来。n=2。検査は光と色しか見ない。意味は見ない
- 06のフォームと08のgerbが「事件の物」として読めるかは、納品後にフィードサイズの
  目視で判定する。読めなければ主題を差し替える（その判断はClaude側）
