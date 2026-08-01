# EP60 surfside — Codex 画像生成 **バッチC：顔** v001（27枚・1プロンプト1枚）

> ## ✅ 今すぐ着手してよいファイルです。
> バッチA（S001–S056・コンクリートの破壊）とバッチB（S057–S110＋T01・T02・場所と書類）は納品済み。
> これは**人の顔**だけを扱う3本目です。**F001–F024（本編用24枚）＋ T03–T05（サムネイル用3枚）= 27枚。**

**題材:** 2021年6月24日、フロリダ州サーフサイドのシャンプレンタワー南棟が部分崩落し98人が亡くなった件。
**この映画は再現映像ではありません。崩落そのものを描かず、犠牲者を描きません。**

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。** 候補を並べて選ぶ工程は存在しない。
3. **「良いのが出るまで回す」を禁止。**
4. **作り直してよいのは §1 の禁止に触れたときだけ。** そのときも**文言を直してから1枚**。

バッチA・Bはこの規則で 112枚・変種0・再生成0 を達成しています。同じ水準で。

---

## 1. ★★ 顔だけに掛かる絶対条件 ★★

このバッチは肖像の問題に最も近いので、他の2本より制約が強くなります。

### 1.1 誰の顔なら作ってよいか

**⭕ 作ってよい：名前の出ない住民・区分所有者。**
この映画で顔を持つのは、**払うかどうかを迫られた側の人たち**だけです。彼らは映画の中で名前を呼ばれません。誰か特定の実在人物ではなく、**その立場にいた人**を描きます。

**❌ 作ってはいけない：名前の出る人物の顔。**
技師、理事、町の建築主任、理事長 — 映画はこの4人を実名で扱います。**全員実在の人物なので、その役どころの顔を作ると肖像になります。**
この4人は本編では**手元・後ろ姿・シルエット**のみで描かれます（バッチAのS038・S073などが担当）。**このバッチで彼らの顔を作らないでください。**

**❌ 亡くなった98人の誰も描かない。** 悲嘆・救助・負傷・遺体・追悼の表情を作らない。

### 1.2 表情の方向

この映画の顔は**悲劇の顔ではありません。書類を前にした顔**です。

作ってよい感情：**当惑／信じられないという顔／徒労／不安／黙って考え込む／腹をくくる**
作ってはいけない感情：**号泣・悲嘆・恐怖の絶叫・パニック・追悼**

### 1.3 描き方（肖像との防火帯）

**明らかにイラスト／半絵画的／シネマティック・レンダーの質感で描く。実写写真に見えてはいけない。**
これは「実在人物の写真ではない」と一目で分かるようにするための社内規則です。写実に寄せすぎたものは不合格。

### 1.4 その他

- **子どもの顔を作らない。**
- **読める文字・数字・署名・印章・ロゴを描かない。**（手紙は線の連なりに潰す）
- **崩落・瓦礫・救助・負傷を描かない。**
- 実在の建物「シャンプレンタワー南棟」を描かない。背景は**類型**として。

### 1.5 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 実写写真に見える（イラスト調でない） |
| Q2 | 実在の特定人物に似ている |
| Q3 | 技師・理事・建築主任・理事長など**名前の出る役**として読める |
| Q4 | 号泣・悲嘆・パニックなど §1.2 の禁止感情 |
| Q5 | 子どもの顔がある |
| Q6 | 読める文字・数字・署名・印章がある |
| Q7 | 崩落・瓦礫・負傷が写っている |
| Q8 | F系で長辺3840px未満／T系で1920×1080でない |

---

## 2. スタイル

**`[FSTYLE]`**（F001–F024・本編用）＝ 末尾にそのまま連結:

> , clearly illustrative semi-painterly cinematic character render that never reads as a photograph of a real person, a generic non-real individual resembling nobody, cold institutional grey-blue palette with one warm amber note from a lamp or morning window, near-black falloff at the edges, restrained documentary framing, shallow depth of field, ultra-detailed, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no logo, no seal

**`[TSTYLE]`**（T03–T05・サムネイル用）＝ 末尾にそのまま連結:

> , clearly illustrative semi-painterly cinematic character render that never reads as a photograph of a real person, a generic non-real individual resembling nobody, face occupying 50 to 65 percent of frame height with the eyes on the upper third, bright key light on the face and a rim light separating it from a dark desaturated background, skin warm, background cool deep grey-blue, high contrast and vivid, one clean quadrant of negative space for text, 1920x1080, ultra-detailed, no text, no lettering, no numerals, no logo, no seal

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> photorealistic portrait, likeness of a real person, celebrity likeness, identifiable individual, children, minors, crying, weeping, grief, mourning, panic, screaming, terror, injuries, blood, rescue workers, rubble, debris, collapsed buildings, readable text, letterforms, numerals, signage, watermarks, logos, seals, emblems, oversaturated, HDR halo, cartoon, anime, caricature

★**必ず展開してから生成。1枚目で展開されているか目視確認すること。**

---

## 3. 出力

- 出力先: `H:\pd-media\assets\ai\surfside\`
- **F001.png 〜 F024.png**（3840×2160）
- **T03.png 〜 T05.png**（1920×1080）
- 既存の S001–S110・T01・T02 は上書きしない。

---

## 4. プロンプト（27行・各1枚）

### 4.1 本編用の顔 — 払う側の人たち（F001–F024 / 24枚）

台本の第3幕：*「1ベッドルームの所有者は80,190ドル。…年金生活の所有者が、見たこともないコンクリートのために六桁を求められていた」*

```
- `F001.png`
A generic non-real man in his seventies seated at a kitchen table at night, an unfolded letter held in both hands, reading it a second time, flat disbelief rather than shock, one warm lamp, the room ordinary and dim [FSTYLE] Avoid: [NEG]
- `F002.png`
At the same kind of table, a generic non-real woman in her sixties with reading glasses pushed up onto her forehead, one hand flat on the paper, thinking rather than reacting [FSTYLE] Avoid: [NEG]
- `F003.png`
A generic non-real man in his late sixties standing in an underground garage looking up at the ceiling, torchlight from below, unease he cannot name [FSTYLE] Avoid: [NEG]
- `F004.png`
A generic non-real woman in her fifties at a condominium meeting, arms folded, listening to something she does not accept, other attendees behind her thrown fully out of focus [FSTYLE] Avoid: [NEG]
- `F005.png`
A generic non-real man in his seventies at a meeting, elbow on the table and fingers at his temple, exhausted by an argument that has run for three years [FSTYLE] Avoid: [NEG]
- `F006.png`
A generic non-real woman in her seventies on a coastal balcony at dusk, looking out at the water, composed, holding a folded page down at her side [FSTYLE] Avoid: [NEG]
- `F007.png`
A generic non-real man in his sixties at a desk with a chequebook open in front of him, pen in hand and not yet writing, deciding [FSTYLE] Avoid: [NEG]
- `F008.png`
A generic non-real couple in their seventies seen close at a kitchen table, both looking at the same page between them, neither speaking, warm lamp, cool window behind [FSTYLE] Avoid: [NEG]
- `F009.png`
A generic non-real woman in her forties standing at a lobby mailbox bank with an opened envelope, reading in the doorway rather than waiting to get upstairs [FSTYLE] Avoid: [NEG]
- `F010.png`
A generic non-real man in his eighties seated alone in a row of folding chairs after a meeting has emptied, still holding his copy of the paperwork [FSTYLE] Avoid: [NEG]
- `F011.png`
A generic non-real man in his fifties in an underground garage with one hand flat against a concrete column, head tilted back, looking at something above him he does not like [FSTYLE] Avoid: [NEG]
- `F012.png`
In morning light at a poolside table, a generic non-real woman in her sixties, papers weighted down against the breeze, reading rather than swimming [FSTYLE] Avoid: [NEG]
- `F013.png`
A generic non-real man in his seventies standing in a residential corridor holding an envelope, his own front door half open behind him, not yet gone inside [FSTYLE] Avoid: [NEG]
- `F014.png`
A generic non-real woman in her eighties in an armchair with a page resting on her lap, looking away from it towards a window, composed [FSTYLE] Avoid: [NEG]
- `F015.png`
A generic non-real man in his forties in a concrete stairwell with a phone to his ear, the back of his other hand against his forehead, listening rather than speaking [FSTYLE] Avoid: [NEG]
- `F016.png`
At a desk with a calculator and a stack of paper, a generic non-real woman in her fifties, mid-sum, every figure on every page an unreadable blur [FSTYLE] Avoid: [NEG]
- `F017.png`
Two generic non-real neighbours in their sixties standing in a residential lobby mid-conversation, one holding paperwork at his side, neither performing emotion [FSTYLE] Avoid: [NEG]
- `F018.png`
From a balcony rail, a generic non-real man in his sixties looking straight down at the pool deck below, seen from behind and to the side, face in three-quarter view [FSTYLE] Avoid: [NEG]
- `F019.png`
A generic non-real woman in her seventies locking her apartment door with an envelope held under one arm, caught mid-action in corridor light [FSTYLE] Avoid: [NEG]
- `F020.png`
A generic non-real man in his seventies sitting in the driver's seat of a parked car in a garage bay, hands in his lap, engine not started, cold light through the windscreen [FSTYLE] Avoid: [NEG]
- `F021.png`
A generic non-real woman in her sixties at a condominium meeting with one hand half raised to speak, the rest of the room thrown out of focus [FSTYLE] Avoid: [NEG]
- `F022.png`
A generic non-real man in his fifties leaning against a garage wall with his arms folded, listening to somebody out of frame, unconvinced [FSTYLE] Avoid: [NEG]
- `F023.png`
A generic non-real woman in her forties crossing a residential lobby with a folder held against her chest, moving with purpose, seen slightly from the front [FSTYLE] Avoid: [NEG]
- `F024.png`
A generic non-real man in his eighties standing at a window at first light with his back mostly to the room, face just catching the dawn, holding nothing [FSTYLE] Avoid: [NEG]
```

### 4.2 サムネイル用の顔（T03–T05 / 3枚）

社内CTR実測：同ジャンル69本中**81%（56/69）に人の顔**があり、**顔＋感情がCTRの第1ドライバー**。顔なしは explainer/mystery 系の外れ値。**顔は必須。ただし §1 の防火帯は全部かかります。**

文字は後から合成するので、**画像に文字を描かないでください。** 余白だけ確保します。

```
- `T03.png`
A generic non-real man in his sixties at peak emotion aimed straight at the viewer — flat, disbelieving incomprehension, the look of someone who has just read a number he cannot pay for something he cannot see, an unfolded page low in the frame, dark blurred domestic interior behind, clean negative space on the left for text [TSTYLE] Avoid: [NEG]
- `T04.png`
A generic non-real woman in her seventies looking up and slightly past the camera with dawning unease, lit from below as if by a torch in a garage, the dark ribbed underside of a concrete ceiling out of focus above her, clean negative space on the right for text [TSTYLE] Avoid: [NEG]
- `T05.png`
A generic non-real man in his seventies seen close in a dim meeting room, hand at his temple, worn down rather than distressed, empty folding chairs falling away behind him into darkness, clean negative space on the left for text [TSTYLE] Avoid: [NEG]
```

---

## 5. 完了条件（全部緑で完了）

```
[C-1] H:\pd-media\assets\ai\surfside\ に F001..F024 (24枚) + T03..T05 (3枚) = 27枚
[C-2] _02 / _03 が0件
[C-3] F001..F024 の長辺 >= 3840px / T03..T05 が 1920x1080
[C-4] §1.5 の Q1–Q8 を全13枚で目視。1枚も該当なし
[C-5] とくに Q2・Q3 は1枚ずつ声に出して確認する
      （「これは実在の誰かに見えないか」「技師・理事・建築主任・理事長に見えないか」）
[C-6] sha256 重複ゼロ
[C-7] 1枚目で [FSTYLE]/[TSTYLE]/[NEG] が展開済みであることを確認した記録
```

**27枚に届かないまま先へ進まない。基準を下げない。水増ししない。**

---

## 6. なぜこのバッチが後から追加されたか（記録）

当初、この映画は**顔をひとつも使わない**方針で設計されていました。98人を名指しも描写もしないという判断からです。

それは行き過ぎでした。実測（社内CTRプレイブック・同ジャンル69本を実見して分類）では、**顔のあるサムネが81%**、**顔＋感情がCTRの第1ドライバー**、顔なしは「我々の競合ではない外れ値」。加えて「サムネに顔を出さない」という旧規則は**オーナーが既に撤廃済み**でした。

正しい線は「人間を描かない」ではなく「**実在の人物の肖像を作らない**」です。この映画で名前が出るのは書き残した4人で、彼らは手と後ろ姿のまま。顔を持つのは**名前の出ない、払うかどうかを迫られた住民**です。

副次的に、脚本の批評が指摘していた最大の欠落 —「この映画は住民に一度も『いやだ』と言わせていない」— にも、この13枚が効きます。

---

*2026-08-01 作成。台本 `EP60_surfside_script.en.v003.md`、事実は `EP60_surfside_FACTS_LEDGER.v001.md`、CTRの根拠は `episodes/_planning/CTR_PLAYBOOK.v001.md`。バッチA・Bと合わせて EP60 の画像は 139枚（S110 + T5 + F24）で完結します。24枚は既存30分話のF系12枚を引き伸ばした値ではなく、カット数からの積算です：本編約520カットのうちAI静止画が約110カット、そのおよそ2割を顔が担う想定。*
