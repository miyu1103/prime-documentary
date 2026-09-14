# EP77 · KEYBRIDGE — IMAGE ORDER (BATCH C) v001 — 差し替え16枚

**16 replacement plates, `H132`–`H147`.** Every prompt is the subject in the table plus
`[STYLE]` plus `[NEG]`, in that order.

## 0. なぜこの発注が出ているか（読んでから作ってください）

BATCH A/B で納品された131枚のうち **16枚を落としました**。理由は1つだけです。

> **2024年の港なのに、絵が1940年代になっている。**

具体例: Eric McAllister は現代のタグボートなのに **石炭焚きの蒸気タグ**が来た。路面のコーンが
**木製**だった。橋が **吊り橋**で来た（Francis Scott Key Bridge は連続トラス）。真鍮のエンジン
テレグラフ、リベット打ちの蒸気船、石油ランプ、ヨーロッパの旧市街。

原因は**発注文に年代の指定が無かったこと**です。`[STYLE]` の "cinematic documentary
reconstruction / 一灯 / 霧" が、そのまま古い絵に引っ張りました。**唯一の例外が H055 で、これは
発注文自体が誤り**でした（"A ship's telegraph, brass and glass" — Dali にエンジンテレグラフは
存在しません）。

なので今回は **すべてのプロンプトに `present-day 2024` と具体的な現代機材名が入っています。**
`[NEG]` にも時代語を追加してあります。**ここを外さないでください。**

## 1. 番号について（絶対）

**H132–H147 は新しい番号です。落とした16枚の番号（H009, H024, H055, H057, H058, H079, H086,
H097, H099, H109, H110, H114, H116, H117, H118, H120）を再利用しないでください。**
既存IDで納品すると、すでに本編に入っている板を上書きします（EP72 で実際に起きました）。
落とした16枚は `remotion/public/keybridge/img/rejected/` に退避済みで、そのままにします。

## 2. サイズ

- **長辺 3840 px 以上・16:9 ちょうど**（幅÷高さ = 1.778）。`remotion/public/keybridge/img` が
  render truth で、レンダー前ゲートがこれ未満を拒否します。
- Codex の生成は 1672×941 固定です。native-4K が使えないなら
  **Real-ESRGAN x4plus → 6688×3764 → LANCZOS で 3840×2160 ちょうど**に落としてください。
  **2倍拡大では床を越えません。**
- **1プロンプト＝1枚。** variant も b 版も要りません。
- 納品先 `E:\pd-media\05_visuals\keybridge\img\`。**既存ファイルは上書きしないこと。**

## 3. この話数の絶対禁止（`episode_spec.v001.json` / FACTS_LEDGER）

| never | why |
|---|---|
| 衝突の瞬間・崩落・水中の残骸 | `forbidden_subjects`。この番組は事故そのものを映しません |
| 亡くなった6人。遺体・負傷・救助・葬儀 | `forbidden_subjects`、invariant 11 |
| 実在人物と分かる顔（船長・水先人・機関長・被告・当局者） | invariant 11。**人物は可、肖像は不可。** 背中・手・シルエット・遠景 |
| 読める文書（起訴状・報告書・ログ・海図の文字） | invariant 11。紙は可、**文字が解像してはいけない** |
| 外国と分かる場所（日本・中国・台北・モスクワ・パリ・ロンドン・ヴェネツィア・ニューヨーク・ヨーロッパ旧市街 …） | 舞台はボルチモア |

## 4. 発注表

| 新ID | 差し替え元 | セクション | subject（`[STYLE]` と `[NEG]` を後ろに付けて生成） |
|---|---|---|---|
| H132 | H009 | ACT_1 | Close on a **present-day 2024** hot-tar patching kit on a highway deck at night — a modern asphalt lute, a steel tamper, a plastic sealant pail — under a battery LED work light |
| H133 | H024 | ACT_1 | A **modern present-day 2024** harbour tugboat under way at night seen from a ship's rail, white LED deck floodlights burning, rubber fendered bow, wake churning |
| H134 | H055 | ACT_2 | A **present-day 2024** ship's engine control console at night, backlit rocker switches and a dark digital readout panel, one warm lamp raking across it, no characters resolving |
| H135 | H057 | ACT_3 | A **modern present-day 2024** container terminal quayside at dusk, a welded steel accommodation ladder down from a modern hull, an anonymous crew member in hard hat and hi-vis walking up it seen from behind, LED floodlights |
| H136 | H058 | ACT_3 | A **present-day 2024** exhaust gas scrubber unit on a modern container ship's funnel casing, painted steel pipework and grating platforms, one lamp |
| H137 | H079 | ACT_3 | An anonymous figure in a **modern business suit** at a lectern seen from behind against a lit projection screen showing an abstract block diagram, **present-day 2024** conference room |
| H138 | H086 | ACT_3 | A **modern** container ship passing under a long steel **continuous-truss** road bridge at dusk seen from far off, flat American tidewater estuary, low wooded shoreline, calm |
| H139 | H097 | ACT_4 | A **present-day 2024** port authority service counter at night, laminate desk, closed roller shutter, nobody present, one ceiling panel light |
| H140 | H099 | ACT_4 | A **modern present-day 2024** revolving crane barge on a river at first light, diesel-hydraulic house, wire falls and hooks, no wreck visible |
| H141 | H109 | ACT_4 | A **present-day 2024** harbour at dusk with a road bridge under construction, **modern crawler cranes** on the span, container terminal behind, warm sky |
| H142 | H110 | ACT_4 | A wide aerial of a **modern present-day 2024** container port at night, ship-to-shore gantry cranes, LED light masts, ships at berth, a steel truss bridge in the distance |
| H143 | H114 | ENDING | A **modern concrete** bridge pier at dawn with new sheet-pile and concrete protective dolphins in the water around it, flat American tidewater, no skyline |
| H144 | H116 | ENDING | A **present-day 2024** family car crossing a long modern bridge over water in early morning light, seen from far away, no readable plate |
| H145 | H117 | ENDING | An anonymous driver's hands on a **present-day 2024** car steering wheel with a modern airbag boss, bridge truss members passing overhead, dawn |
| H146 | H118 | ENDING | Anonymous gloved hands stacking **modern orange reflective plastic highway traffic cones** onto a pickup truck bed at the end of a shift, **present-day 2024**, dawn light, no face |
| H147 | H120 | ENDING | A wide dawn view of a **modern present-day 2024 American** working harbour with a steel truss road bridge in the middle distance, container gantries, calm water, low wooded shoreline |

## 5. [STYLE] — 全プロンプト共通、subject の直後に付ける

```
present day, 2020s, modern equipment, cinematic documentary reconstruction, one practical light source visible in the frame throwing a directional beam, atmospheric haze and river mist catching the light, deep shadow on one side only, restrained colour with a single dominant accent, high contrast, ultra high resolution, hyper-detailed, razor-sharp focus, photorealistic, volumetric light, shallow depth of field, 16:9,
```

## 6. [NEG] — 全プロンプト共通、最後に付ける

BATCH A の NEG に、今回落ちた16枚の原因である**時代語を追加**しています。

```
Avoid: steam ship, steamship, steam tug, funnel smoke, smokestack, brass fittings, brass telegraph, riveted hull, oil lantern, kerosene lamp, gas lamp, vintage, antique, sepia, 1900s, 1920s, 1930s, 1940s, period piece, wooden traffic cone, sailing ship, square rigger, suspension bridge, gothic spire, church steeple, European old town, cobblestone street, stone arch bridge, text, lettering, legible text, readable text, captions, subtitles, handwriting, cursive, signature, numerals, numbers, digits, house numbers, readable documents, signage lettering, watermark, seal, seals, emblem, emblems, logo, logos, badge, insignia, human face, facial features, portrait, identifiable person, recognisable person, looking at the camera, bodies, corpse, injuries, blood, rescue operations, the moment of collision, the bridge collapsing, wreckage in water, children, gavel, handcuffs, prison bars, police uniform, patrol car, golden hour, drone shot, cartoon, oversaturated, flat evenly-dark image, muted grey wash, desaturated, low-resolution, distorted anatomy, extra fingers.
```

## 7. 納品後

設計レーンが `check_plate_verdicts.py --slug keybridge --scaffold` を回し直して16枚を判定します。
枚数は毎回ディスクを数え直すので、途中経過の報告は不要です。
