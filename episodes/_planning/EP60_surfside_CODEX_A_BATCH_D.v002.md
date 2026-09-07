# EP60 surfside — Codex 画像生成 **バッチD：第1幕・第2幕** v002（40枚・1プロンプト1枚）

> **v002（2026-08-02）で直したのは参照値だけです。プロンプト40行は1文字も変えていません。**
> 台本は v003 → v004 になりましたが、変更は **第5幕と「あの夜」だけ**（崩落時刻と1分・プールデッキがタワーの4分以上前に落ちていた事実）。
> **このバッチが担当する第1幕・第2幕は無変更**なので、絵の内容に影響はありません。

> ## ✅ 今すぐ着手してよいファイルです。
> **なぜ4本目が必要になったか（正直な記録）:**
> バッチB は **ACT III（第3幕）から始まって**います。バッチA はコンクリートの破壊そのもの、バッチC は顔。
> つまり **第1幕（1:10–7:00）と第2幕（7:00–16:00）に専用の絵が一枚もありません。**
> この2幕で **35.6分中の約14.8分＝映画の42%**。しかも第2幕には、この映画で**唯一の「場面」**（2018年11月の理事会）があります。
> このファイルはその穴だけを埋めます。**S111–S150 の40枚。**

**題材:** 2021年6月24日、フロリダ州サーフサイドのシャンプレンタワー南棟が部分崩落し98人が亡くなった件。
**この映画は再現映像ではありません。崩落そのものを描かず、犠牲者を描きません。**

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。** 候補を並べて選ぶ工程は存在しない。
3. **「良いのが出るまで回す」を禁止。**
4. **作り直してよいのは §1 の禁止に触れたときだけ。** そのときも**文言を直してから1枚**。

バッチA・B・C はこの規則で **139枚・変種0・指定外のファイル0** を達成済みです（実測確認済み）。
再生成はバッチC の2件のみで、どちらも**同じプロンプトを回し直したのではなく、文言を直してから1枚**でした（T03：驚き顔に見えた / T04：怖がって見えた）。
**このバッチも同じ水準で。**

---

## 1. ★絶対条件（触れた絵は使用不可）

- **崩落・瓦礫・救助・遺体を描かない。**
- **実在の建物「シャンプレンタワー南棟」の肖像を作らない。** 建物は**1981年前後のフロリダ海岸の分譲高層住宅という類型**として描く。実物の写真と見紛うものを作らない。
- **顔を作らない。** このバッチに顔はありません（顔はバッチCが担当）。人が要る場面は**手元・後ろ姿・シルエット・顔が判別できない距離**のみ。
  とくに **技師・理事・建築主任・理事長は全員実在の名前つき人物**なので、**顔を絶対に作らないでください。**
- **読める文字・数字を一切描かない。** 報告書・図面・議事録・掲示物の文字は、線の連なりに潰れて読めない状態にする。
- **印章・紋章・ロゴを描かない。**
- **本物の報告書・公文書に見える画像を作らない。**

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字・署名がある |
| Q3 | 印章・紋章・ロゴらしきものがある |
| Q4 | **顔が写っている**（このバッチは顔ゼロが正しい） |
| Q5 | 崩落・瓦礫・負傷が写っている |
| Q6 | 既存の S001–S110・T01–T05・F001–F024（**すでに139枚現物がある**）と実質同じ構図 |

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, cold institutional grey-blue concrete as the base palette, one warm amber note reserved strictly for morning light, corrosion stain and warning — never flooding the frame, near-black falloff at the edges, telephoto compression, shallow depth of field, restrained documentary framing, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no seal, no emblem, no readable documents, no identifiable face

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> readable text, letterforms, numerals, signage, captions, watermarks, logos, seals, emblems, crests, faces, identifiable faces, portraits of real people, collapsed buildings, rubble, debris fields, rescue scenes, injured people, bodies, gore, dramatic explosion, disaster movie lighting, cartoon, illustration, painterly, oversaturated, HDR halo

1枚目で展開されているか必ず目視確認すること。

---

## 3. 出力

- 出力先: `H:\pd-media\assets\ai\surfside\`
- **S111.png 〜 S150.png（40枚・3840×2160）**
- 既存の S001–S110・T01–T05・F001–F024 は上書きしない。

---

## 4. プロンプト（40行・各1枚）

### 4.1 第1幕 — 建物、そして共有されているもの（S111–S126 / 16枚）

台本：*「その建物の人たちは所有者だった。借り手ではない。…共有されているもののうち、デッキは人が実際に使う場所だった」* ／ *「37年間、誰も見なくてよかった。そして建物は40年目を迎え、フロリダが放っておかなくなった」*

```
- `S111.png`
A twelve-storey 1981-era beachfront residential tower seen from the wet sand at dusk as a generic architectural type, stacked balconies in silhouette, no identifying features [STYLE] Avoid: [NEG]
- `S112.png`
The same order of tower photographed flat-on from across a quiet coastal street in hard midday light, ranks of identical balcony rails [STYLE] Avoid: [NEG]
- `S113.png`
Looking straight up the face of a coastal residential tower from its base, twelve floors of balconies converging, flat white sky above [STYLE] Avoid: [NEG]
- `S114.png`
A swimming pool and its tiled deck seen from a balcony four floors up, loungers set out in a row, the garage entrance ramp just visible at one edge [STYLE] Avoid: [NEG]
- `S115.png`
The same pool deck at first light with nobody on it, long shadows across the tiles, a heavy planter of tropical greenery at the frame edge [STYLE] Avoid: [NEG]
- `S116.png`
A cutaway-style composition showing a tiled deck surface and, directly beneath it, the top of a concrete column in shadow — the two worlds in one frame, no annotation [STYLE] Avoid: [NEG]
- `S117.png`
A residential lobby seen from the entrance doors, polished stone floor, a seating group nobody is using, cold daylight from the street behind [STYLE] Avoid: [NEG]
- `S118.png`
A bank of brass mailboxes in that lobby photographed straight on, every door shut, every nameplate blank [STYLE] Avoid: [NEG]
- `S119.png`
A residential corridor at night with identical doors receding, carpet worn along the centre line, one ceiling fixture dark [STYLE] Avoid: [NEG]
- `S120.png`
A lift lobby with the floor indicator unlit and the doors closed, stone threshold worn dull by four decades of feet [STYLE] Avoid: [NEG]
- `S121.png`
A poolside gate standing open onto the deck, the dark bulk of the tower rising out of focus behind it [STYLE] Avoid: [NEG]
- `S122.png`
Sun loungers and folded umbrellas stacked against a wall at the end of the day, the pool water still beyond them [STYLE] Avoid: [NEG]
- `S123.png`
A garage entrance ramp seen from street level, descending into darkness beneath a residential building, midday glare above [STYLE] Avoid: [NEG]
- `S124.png`
A concrete column head meeting the underside of a deck slab, photographed from below at a steep angle in poor light, nothing else in frame [STYLE] Avoid: [NEG]
- `S125.png`
A calendar page pinned in a management office with its grid and numerals dissolved to unreadable marks, one corner curled [STYLE] Avoid: [NEG]
- `S126.png`
A small town hall exterior in flat coastal daylight, low civic architecture, palms motionless, no signage legible [STYLE] Avoid: [NEG]
```

### 4.2 第2幕 — 技師の一日、報告書、そしてあの部屋（S127–S150 / 24枚）

台本：*「彼はデッキを歩いた。ランプを降りてガレージに入った。そしてコンクリートについて最も多くを教えるもの — 叩くこと — をやった」* ／ *「議事録によれば、建物は非常に良い状態だと彼は言った」* ／ *「その2日前、理事の一人が報告書を組合の外へ持ち出し、町に送っていた」*

```
- `S127.png`
An anonymised engineer's hand swinging a small hammer against a concrete garage ceiling, cropped at the wrist, fine dust caught in the light [STYLE] Avoid: [NEG]
- `S128.png`
The same hand held flat against a spalled patch of soffit, not touching the deepest part, torch raking from the side [STYLE] Avoid: [NEG]
- `S129.png`
Work boots and a set-down torch on a garage floor beside a column base, seen from behind at knee height [STYLE] Avoid: [NEG]
- `S130.png`
A clipboard resting on a car bonnet in a garage, its form covered in unreadable marks, a pen laid across it [STYLE] Avoid: [NEG]
- `S131.png`
A folding measuring rule opened flat against a cracked concrete surface, its graduations blurred to nothing [STYLE] Avoid: [NEG]
- `S132.png`
A camera and lens cap set down on a concrete ledge in a garage, the wall behind marked with a plain chalk cross [STYLE] Avoid: [NEG]
- `S133.png`
An engineer's back and shoulder in the far distance of a long dark garage aisle, walking away between columns, unrecognisable [STYLE] Avoid: [NEG]
- `S134.png`
A pool deck photographed from the level of the tiles with a survey tripod leg at the frame edge, ordinary and sunlit [STYLE] Avoid: [NEG]
- `S135.png`
An entrance driveway of a residential building seen from a low angle, tyre-polished concrete, a manhole cover set into it [STYLE] Avoid: [NEG]
- `S136.png`
A row of heavy planters along the edge of a deck, soil damp and dark at the surface, seen at a raking angle [STYLE] Avoid: [NEG]
- `S137.png`
The underside of the same deck directly beneath those planters, the soffit stained in a broad oval, seen from the garage [STYLE] Avoid: [NEG]
- `S138.png`
A sheet of bond paper still rolled in a typewriter platen in a small office, the typed paragraphs an unreadable smear, one desk lamp lit [STYLE] Avoid: [NEG]
- `S139.png`
A bound engineering report lying closed on a desk, plain cover, a paperclip at one corner, cold morning light [STYLE] Avoid: [NEG]
- `S140.png`
The same report open under a lamp with a hand at the frame edge turning a page, every line dissolved to an unreadable band [STYLE] Avoid: [NEG]
- `S141.png`
Survey photographs laid out in a grid on a desk, all of them face down, only blank backs showing [STYLE] Avoid: [NEG]
- `S142.png`
A thick manila envelope lying on a hall table beneath a set of keys, its face turned to an unreadable smear [STYLE] Avoid: [NEG]
- `S143.png`
A wire out-tray on an office desk holding a single sealed envelope, cold fluorescent light overhead [STYLE] Avoid: [NEG]
- `S144.png`
A municipal counter with a bell on the surface and closed shutters behind it, flat institutional light, nobody attending [STYLE] Avoid: [NEG]
- `S145.png`
A municipal office corridor with closed doors receding, a run of fluorescent tubes overhead, linoleum worn along the middle [STYLE] Avoid: [NEG]
- `S146.png`
An empty condominium meeting room set out for the evening: folding chairs in uneven rows, a plain jug of water and glasses on a side table, overhead strip light [STYLE] Avoid: [NEG]
- `S147.png`
The long table at the front of that room with a bound report lying on it, chairs pushed back, nobody yet arrived [STYLE] Avoid: [NEG]
- `S148.png`
The same room from the back row during the meeting, seen over the shoulders of seated attendees rendered as dark shapes, no faces, the front of the room lit [STYLE] Avoid: [NEG]
- `S149.png`
The room after the meeting has emptied, chairs at angles, one folded flat on the floor, the report still lying where it was left, lights still on [STYLE] Avoid: [NEG]
- `S150.png`
An institutional file drawer sliding shut over a bound document, cold fluorescent light, the pages an unreadable smear [STYLE] Avoid: [NEG]
```

---

## 5. 完了条件（全部緑で完了）

```
[D-1] H:\pd-media\assets\ai\surfside\ に S111..S150 = 40枚
[D-2] _02 / _03 が0件
[D-3] 全40枚の長辺 >= 3840px
[D-4] §1 の Q1–Q6 を全40枚で目視。1枚も該当なし
[D-5] Q4（顔）は特に厳格に。このバッチに顔は一枚も無いのが正しい
[D-6] sha256 重複ゼロ（S001–S150 / T01–T05 / F001–F024 の全体で）
[D-7] 1枚目で [STYLE] / [NEG] が展開済みであることを確認した記録
[D-8] BATCH_D_QC_v001.json を A/B/C と同じ形式で出力
      （schema は pd.surfside.batch_d_qc.v001。deliverable_count / generation_attempts /
        regeneration_count / rejections / checks を含める。
        checks に all_179_present と all_179_sha256_duplicates_zero を入れる）
```

**40枚に届かないまま先へ進まない。基準を下げない。水増ししない。**

---

## 6. これで EP60 の画像は完結します

| バッチ | 枚数 | 守備範囲 |
|---|---|---|
| A | 56 | S001–S056：コンクリートの破壊、接合部、ガレージ |
| B | 56 | S057–S110＋T01–T02：第3幕の金額、第4幕の春、第5幕の設計と調査、その夜、結末 |
| C | 27 | F001–F024＋T03–T05：払う側の住民の顔、サムネイル用の顔 |
| **D** | **40** | **S111–S150：第1幕の建物と所有、第2幕の技師とあの部屋** |
| **合計** | **179** | |

本編は約520カット。実写素材が約330カット、断面図（Blender）が4〜6ショット、AEカードが12〜16枚。残りをこの179枚が担います。**すべて1カットずつ使い切る前提**で、余りを作らない設計です。

---

*v001 作成 2026-08-01。**v002 更新 2026-08-02**。
台本は `EP60_surfside_script.en.v004.md`（6,304語・36.4分）の第1幕・第2幕から積算。事実は `EP60_surfside_FACTS_LEDGER.v002.md`。
実写素材で代替できるものは除外している。その本数は 2026-08-02 に再計測済み：法廷871・書類752・実験室638・海岸450・夜明け242・工事219・クレーン99・会議室66・ガレージ61。
逆に、この映画の主役である**劣化した鉄筋コンクリートは棚に存在しない**（spalling 0・reinforced concrete 0・corrosion 0・rebar 1）。だからAI静止画を使う。*
