# EP60 surfside — Codex 画像生成 **バッチA** v001（56枚・1プロンプト1枚）

> ## ✅ これは今すぐ着手してよいファイルです。
> 台本（v002）はまだ書いている最中ですが、**このバッチだけは台本の結論に左右されません。**
> 理由：この映画の主題は「四十年かけて腐っていくコンクリート」で、実写素材の棚には**それが一枚も無い**（台帳17万行に対して実測 `rebar` 1件・`corrosion` 0件・`spalling` 0件・`condominium` 0件・`surfside` 0件）。台本がどう転んでも、この56枚は必ず画面に出ます。
>
> **バッチB（残り約56枚）は台本とカット表の確定後**に出します。あちらは「どのビートに何を置くか」で内容が変わるので、先に作ると捨てる絵が出ます。

**題材:** 2021年6月24日、フロリダ州サーフサイドのシャンプレンタワー南棟が部分崩落し98人が亡くなった件。2026年6月22日にNISTが技術的知見を公表。
**この映画は再現映像ではありません。崩落そのものは描きません。**

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

**オーナー指示 2026-07-31。**

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。** 候補を並べて選ぶ工程は存在しない。
3. **「良いのが出るまで回す」を禁止。** 「◯枚に達するまで繰り返す」「3回失敗したら再度1枚」といった指示は**このファイルには無い**。持ち込まない。
4. **作り直してよいのは §1 の禁止に触れたときだけ。** そのときも**プロンプトの文言を直してから1枚**。同じ文で引き直さない。

> なぜこの規則があるか（実測）: 過去のある話は257枚の仕様に対して**628枚**書き出され、355枚が捨てられていた。さらに全話共通で、指定した210枚のうち**約100枚が1カットも使われずに終わっていた**。このバッチは56枚を求め、56枚すべてが画面に出る。

---

## 1. ★絶対条件（触れた絵は使用不可）

- **崩落・瓦礫・救助・遺体を描かない。** 一切。
- **実在の建物「シャンプレンタワー南棟」の肖像を作らない。** 建物は**類型**として描く。実物の写真と見紛うものを作らない。
- **実在人物の顔を作らない。** 人が要る場合は**手元・後ろ姿・シルエット・顔が判別できない距離**のみ。
- **読める文字・数字を一切描かない。** 書類・図面・標識の文字は、線の連なりに潰れて読めない状態にする。
- **印章・紋章・ロゴ・企業マークを描かない。**
- **本物の報告書や公文書に見える画像を作らない。**

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字・署名がある |
| Q3 | 印章・紋章・ロゴらしきものがある |
| Q4 | 顔が判別できる人物がいる |
| Q5 | 崩落・瓦礫・負傷者が写っている |
| Q6 | 他の絵と実質同じ構図 |

---

## 2. スタイル（★必ず展開してから生成）

過去に `[STYLE]` を展開しないまま267枚を生成し、**禁止事項155語が全部の絵から消える**事故がある。**1枚目で展開されているか必ず目視確認すること。**

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, cold institutional grey-blue concrete as the base palette, one warm amber note reserved strictly for morning light, corrosion stain and warning — never flooding the frame, near-black falloff at the edges, telephoto compression, shallow depth of field, restrained documentary framing, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no seal, no emblem, no readable documents, no identifiable face

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> readable text, letterforms, numerals, signage, captions, watermarks, logos, seals, emblems, crests, identifiable faces, portraits of real people, collapsed buildings, rubble, debris fields, rescue scenes, injured people, bodies, gore, dramatic explosion, disaster movie lighting, cartoon, illustration, painterly, oversaturated, HDR halo

---

## 3. 出力

- 出力先: `H:\pd-media\assets\ai\surfside\`
- ファイル名は下記のとおり **S001.png 〜 S056.png**。番号は動かさない（バッチBは S057 以降を使う）

---

## 4. プロンプト（56行・各1枚）

### 4.1 デッキとその裏側 — 健全な状態（S001–S014 / 14枚）

```
- `S001.png`
The underside of a thick concrete deck slab seen from directly below in near-darkness, a shallow grid of beams receding, one cold strip of light grazing the soffit [STYLE] Avoid: [NEG]
- `S002.png`
A square concrete column head meeting a deck slab from below, the thickened panel around it catching a low raking light [STYLE] Avoid: [NEG]
- `S003.png`
An empty underground parking level at night, rows of concrete columns receding into blackness, a single fluorescent tube far down the row [STYLE] Avoid: [NEG]
- `S004.png`
A concrete column standing floor to ceiling in a garage, photographed straight on in flat light, unremarkable and sound [STYLE] Avoid: [NEG]
- `S005.png`
Reinforcing steel bars laid in a clean orthogonal grid inside timber formwork before a concrete pour, seen from above [STYLE] Avoid: [NEG]
- `S006.png`
Reinforcing bars bundled and wired together where they pass over a column head, dense and orderly [STYLE] Avoid: [NEG]
- `S007.png`
A cut edge of a concrete slab showing the pale aggregate face, a line of reinforcement running through it in section [STYLE] Avoid: [NEG]
- `S008.png`
Wet concrete being screeded flat across a deck at night, a chute at the frame edge, workers only as distant silhouettes [STYLE] Avoid: [NEG]
- `S009.png`
A freshly finished concrete deck surface, uniform and pale, seen at a low raking angle in early light [STYLE] Avoid: [NEG]
- `S010.png`
A dark waterproof membrane rolled out across a flat concrete deck, its seams lapped and sealed, before the paving goes on [STYLE] Avoid: [NEG]
- `S011.png`
The junction where a flat deck meets a low upstand wall, the waterproofing turned up the face and dressed in [STYLE] Avoid: [NEG]
- `S012.png`
Paving slabs bedded on sand over a waterproof deck, one slab lifted at the corner to show the layers beneath [STYLE] Avoid: [NEG]
- `S013.png`
A drainage outlet set into a concrete deck, its grating clean, the surface falling gently towards it [STYLE] Avoid: [NEG]
- `S014.png`
A tiled pool deck at first light, empty, a heavy planter of tropical greenery standing on the slab [STYLE] Avoid: [NEG]
```

### 4.2 水と塩 — 進行が始まる（S015–S026 / 12枚）

```
- `S015.png`
Shallow water standing in a sheet across a flat concrete deck after rain, the sky reflected in it [STYLE] Avoid: [NEG]
- `S016.png`
A drainage outlet sitting slightly proud of the deck around it, water pooled against its rim and not entering [STYLE] Avoid: [NEG]
- `S017.png`
A drain choked with wind-blown sand and leaf litter, standing water held behind it [STYLE] Avoid: [NEG]
- `S018.png`
The lapped seam of a waterproof membrane lifting very slightly at one edge, a dark line of moisture beneath it [STYLE] Avoid: [NEG]
- `S019.png`
Salt bloom crystallised white on a coastal steel rail at dawn, macro, the sea a pale blur behind [STYLE] Avoid: [NEG]
- `S020.png`
Efflorescence — a chalky white deposit — bleeding from a hairline crack on a concrete soffit [STYLE] Avoid: [NEG]
- `S021.png`
A damp patch on a garage ceiling with a mineral trail running down the column below it [STYLE] Avoid: [NEG]
- `S022.png`
Water dripping from the lowest point of a crack in a concrete ceiling, caught mid-fall [STYLE] Avoid: [NEG]
- `S023.png`
A shallow puddle on a garage floor with fine grey sediment settled at its edges [STYLE] Avoid: [NEG]
- `S024.png`
The underside of a deck where a heavy planter sits above, the soffit stained in a broad oval beneath its footprint [STYLE] Avoid: [NEG]
- `S025.png`
Sand and grit accumulated in the joints between deck pavers, packed hard by years of rain [STYLE] Avoid: [NEG]
- `S026.png`
A garage ramp descending into darkness, wet tyre tracks polished into the concrete [STYLE] Avoid: [NEG]
```

### 4.3 コンクリートが壊れていく（S027–S042 / 16枚）

```
- `S027.png`
A torch beam raking across a concrete garage ceiling, catching a spreading map of hairline cracks [STYLE] Avoid: [NEG]
- `S028.png`
A single hairline crack in a concrete soffit photographed very close, running out of frame in both directions [STYLE] Avoid: [NEG]
- `S029.png`
The same order of crack but open enough to admit a coin, its edges crumbling to powder [STYLE] Avoid: [NEG]
- `S030.png`
Concrete spalling from a soffit, a fist-sized piece gone, the void pale at its centre and stained at its rim [STYLE] Avoid: [NEG]
- `S031.png`
Spalling on the face of a concrete column, the reinforcement behind it exposed and heavily rust-stained [STYLE] Avoid: [NEG]
- `S032.png`
A corroded reinforcing bar emerging from broken concrete, its surface flaked into layers like pastry [STYLE] Avoid: [NEG]
- `S033.png`
Macro of a steel reinforcing bar reduced by rust to a fraction of its original section, against pale concrete [STYLE] Avoid: [NEG]
- `S034.png`
Rust weeping from a hairline crack in a concrete ceiling, a brown tear-track running a metre down [STYLE] Avoid: [NEG]
- `S035.png`
A wide patch of soffit where the cover concrete has gone entirely, parallel reinforcing bars exposed across it [STYLE] Avoid: [NEG]
- `S036.png`
Delaminated concrete on a ceiling, the surface bulging outward in a shallow dome before it lets go [STYLE] Avoid: [NEG]
- `S037.png`
Concrete dust and small fragments lying in a cone on a garage floor directly beneath a ceiling defect [STYLE] Avoid: [NEG]
- `S038.png`
A gloved hand held flat against a spalled concrete surface, not touching the deepest part, cropped at the wrist [STYLE] Avoid: [NEG]
- `S039.png`
A hammer resting against a column base after a sounding survey, fresh dust on the floor beneath [STYLE] Avoid: [NEG]
- `S040.png`
A plain surveyor's chalk cross marked on a concrete column, no letters, no numbers [STYLE] Avoid: [NEG]
- `S041.png`
A patch of newer, paler repair concrete set into an older garage ceiling in one bay only [STYLE] Avoid: [NEG]
- `S042.png`
A camera flash lighting one small area of a vast dark garage ceiling, the rest falling away to black [STYLE] Avoid: [NEG]
```

### 4.4 接合部 — 破壊の場所（S043–S050 / 8枚）

```
- `S043.png`
A slab-column connection seen from below at a steep angle, the drop panel filling the upper frame, geometry as subject [STYLE] Avoid: [NEG]
- `S044.png`
A faint continuous fracture ring in a concrete surface encircling a column head, barely visible in raking light [STYLE] Avoid: [NEG]
- `S045.png`
A concrete deck surface from above holding a shallow depression of water where the slab has moved out of plane [STYLE] Avoid: [NEG]
- `S046.png`
Deck paving lifted very slightly out of plane along one continuous line, seen at a low raking angle [STYLE] Avoid: [NEG]
- `S047.png`
A column head where the slab above has begun to dish around the connection, the geometry no longer flat [STYLE] Avoid: [NEG]
- `S048.png`
Two concrete columns in the middle distance of a dark garage, one of them lit slightly differently from the other [STYLE] Avoid: [NEG]
- `S049.png`
An abstract dark diagram of columns supporting a flat slab, pure geometry, no annotation and no letters [STYLE] Avoid: [NEG]
- `S050.png`
The junction of two structural elements photographed head on, the smaller one carrying the larger [STYLE] Avoid: [NEG]
```

### 4.5 場所としてのガレージ（S051–S056 / 6枚）

```
- `S051.png`
An empty underground garage at two in the morning, one column filling the foreground, the far end unlit [STYLE] Avoid: [NEG]
- `S052.png`
A single parked car in an underground bay seen from behind, dust settled on the boot lid, a column at the frame edge [STYLE] Avoid: [NEG]
- `S053.png`
Painted parking bay lines on garage concrete, worn to a ghost, seen from a low angle [STYLE] Avoid: [NEG]
- `S054.png`
A garage stair door standing closed under a single caged bulb, cold light, nothing else in frame [STYLE] Avoid: [NEG]
- `S055.png`
The whole underside of a deck seen wide, columns marching away, light falling off to black at every edge [STYLE] Avoid: [NEG]
- `S056.png`
An ordinary concrete column in a working garage somewhere else entirely, in daylight, sound and unremarkable [STYLE] Avoid: [NEG]
```

---

## 5. 完了条件（全部緑で完了）

```
[A-1] H:\pd-media\assets\ai\surfside\ に S001..S056 = 56枚
[A-2] _02 / _03 が0件
[A-3] 全56枚の長辺 >= 3840px
[A-4] §1 の Q1–Q6 を全56枚で目視。1枚も該当なし
[A-5] sha256 重複ゼロ
[A-6] 1枚目で [STYLE] / [NEG] が展開済みであることを確認した記録
```

**56枚に届かないまま先へ進まない。基準を下げない。水増ししない。**

---

*2026-08-01 作成。バッチAは台本非依存の56枚。バッチB（S057以降・約56枚：建物の類型と書類の象徴）は台本v002とカット表の確定後に出す。配分の根拠は `EP60_surfside_ASSET_DESIGN.v001.md`、事実は `EP60_surfside_FACTS_LEDGER.v001.md`。*
