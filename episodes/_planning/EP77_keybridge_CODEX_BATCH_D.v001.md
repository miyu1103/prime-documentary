# EP77 · KEYBRIDGE — IMAGE ORDER (BATCH D) v001 — 未着5枚

**5 plates: `H132` `H133` `H134` `H135` `H140`.**

BATCH C で16枚を発注し、**11枚が届きました**（H136–H139, H141–H147）。
この5枚だけ未着です（2026-08-26 実測、`E:\pd-media\05_visuals\keybridge\img_raw_codex_batch_c_v001\`）。
**内容は BATCH C と同一です。作り直しではなく、届かなかった分の再発注です。**

## なぜこの5枚が要るか

元の H009 / H024 / H055 / H057 / H099 を落としました。理由は1つだけです。

> **2024年の港なのに、絵が1940年代になっている。**

蒸気タグ、真鍮のエンジンテレグラフ、石油ランプ、リベット打ちの蒸気船。
原因は**発注文に年代が書いていなかったこと**なので、下の subject には全部
`present-day 2024` と具体的な現代機材名が入っています。**ここを外さないでください。**

## サイズ

- Codex の生成サイズ **1672×941 のままで構いません**（4K化はこちらでやります）。
- **16:9 ちょうど**（幅÷高さ = 1.778）。2.35:1 などのシネスコは不可。
- **1プロンプト＝1枚。** variant も b 版も要りません。
- 納品先 `E:\pd-media\05_visuals\keybridge\img_raw_codex_batch_c_v001\`
  （BATCH C の11枚と同じ場所。**既存ファイルは上書きしないこと**）。

## 絶対禁止（`episode_spec.v001.json`）

衝突の瞬間・崩落・水中の残骸／遺体・負傷・救助・葬儀／実在人物と分かる顔
（人物は可、肖像は不可。背中・手・シルエット・遠景）／読める文書（紙は可、**文字が解像しない**こと）／
外国と分かる場所（舞台はボルチモア）。

## 発注表

| ID | 差し替え元 | セクション | subject（`[STYLE]` と `[NEG]` を後ろに付けて生成） |
|---|---|---|---|
| H132 | H009 | ACT_1 | Close on a **present-day 2024** hot-tar patching kit on a highway deck at night — a modern asphalt lute, a steel tamper, a plastic sealant pail — under a battery LED work light |
| H133 | H024 | ACT_1 | A **modern present-day 2024** harbour tugboat under way at night seen from a ship's rail, white LED deck floodlights burning, rubber fendered bow, wake churning |
| H134 | H055 | ACT_2 | A **present-day 2024** ship's engine control console at night, backlit rocker switches and a dark digital readout panel, one warm lamp raking across it, no characters resolving |
| H135 | H057 | ACT_3 | A **modern present-day 2024** container terminal quayside at dusk, a welded steel accommodation ladder down from a modern hull, an anonymous crew member in hard hat and hi-vis walking up it seen from behind, LED floodlights |
| H140 | H099 | ACT_4 | A **modern present-day 2024** revolving crane barge on a river at first light, diesel-hydraulic house, wire falls and hooks, no wreck visible |

## [STYLE] — subject の直後に付ける

```
present day, 2020s, modern equipment, cinematic documentary reconstruction, one practical light source visible in the frame throwing a directional beam, atmospheric haze and river mist catching the light, deep shadow on one side only, restrained colour with a single dominant accent, high contrast, ultra high resolution, hyper-detailed, razor-sharp focus, photorealistic, volumetric light, shallow depth of field, 16:9,
```

## [NEG] — 最後に付ける

```
Avoid: steam ship, steamship, steam tug, funnel smoke, smokestack, brass fittings, brass telegraph, riveted hull, oil lantern, kerosene lamp, gas lamp, vintage, antique, sepia, 1900s, 1920s, 1930s, 1940s, period piece, wooden traffic cone, sailing ship, square rigger, suspension bridge, gothic spire, church steeple, European old town, cobblestone street, stone arch bridge, text, lettering, legible text, readable text, captions, subtitles, handwriting, cursive, signature, numerals, numbers, digits, house numbers, readable documents, signage lettering, watermark, seal, seals, emblem, emblems, logo, logos, badge, insignia, human face, facial features, portrait, identifiable person, recognisable person, looking at the camera, bodies, corpse, injuries, blood, rescue operations, the moment of collision, the bridge collapsing, wreckage in water, children, gavel, handcuffs, prison bars, police uniform, patrol car, golden hour, drone shot, cartoon, oversaturated, flat evenly-dark image, muted grey wash, desaturated, low-resolution, distorted anatomy, extra fingers.
```

## 納品後

設計レーンが12枚（BATCH C の11枚＋これ5枚のうち届いた分）をまとめて目視判定し、
合格分を 4K化 → 深度生成 → `remotion/public/keybridge/img/` へ配置します。
枚数は毎回ディスクを数え直すので、途中経過の報告は不要です。
