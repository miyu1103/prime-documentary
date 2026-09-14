# EP62 greene — Codex 画像生成 **バッチB 新規発注** v001（**70枚**・1プロンプト1枚）

> ## ★★★ この70枚は **すべて新規 ID** です。既存ファイルを1つも上書きしません。 ★★★
> 保存先は既存と同じ `H:\pd-media\assets\ai\greene\` ですが、**`G243`–`G312` はまだ存在しない番号**です。
> 棚の実測: `G001.png`–`G242.png` の242枚（欠番なし・最大 `G242`）。**次の空き番から取りました。**
> **`G001`–`G242` には触らないでください。** 再生成もしません。
>
> ## ★★★ この70枚は **i2v（静止画→動画）の元絵** です。 ★★★
> 静止画のまま使う絵ではありません。生成後に Wan i2v で全枚を 5.03秒のクリップにします。
> **だから、動く余地のない絵を描かないでください。** 各プロンプトには `MOVING ELEMENT` の一文があり、
> **シャッターが開いた時点で既に動いている物**を1つ名指ししています。**この一文を削らないでください。**
> 完全に静止した構図は動かない i2v クリップになり、`animation_density` がそれで落ちます（EP65 はこれで3回作り直しました）。

**由来:** `check_spec_satisfied.py --slug greene` が `distinct_video_assets` でレンダーを止めている。棚の追加ステージングは3波とも失敗した（最後の波は未ステージ候補1,740本を実測したが、上位は外国の国旗・水中のインク・橋・鳥で、登録語が偶然タグに入っているだけだった）。**1975年ルイビルの公営住宅は棚に存在しない。**生成プレートなら**構造的に時代が合う**——時代違いはこのエピソードを3回刺した欠陥である（現代の米国投票用紙・2011年式 Range Rover Evoque・他作品のショットリストカード。3件とも`config/footage_blocklist.v001.json` に登録済み）。

---

## 1. なぜ70枚なのか（引き算ではなく `solve_totals` から導いた）

**ゲートの出力（現状）**

```
[satisfied] greene: cuts=389 distinct_video=196 stills_in_film=117 mandatory=224
  - distinct_video_assets: 196 distinct footage+motion source(s) across 272 video cut(s),
    against a declared 234 -- 38 short
```

**「234 − 197 = 37」は成立しない。** 理由は3つあり、いずれも実測で確認した。

1. **プールは 197 ではなく 196。** `asset_manifest.v003.json` の実数は factory **73** ・
   motion **123** ・stills **117**。`greene/factory/` にはファイルが74個あるが、そのうち
   `AR-6041714` は `overlay` 区分でカット素材ではない。フィルム側の distinct 196 = 73 + 123 と
   完全一致しており、**プールの映像素材は1本残らず既にフィルムに入っている。**
2. **新規プレートを足すと factory と motion の配分そのものが動く。** `solve_totals` は
   `video = ceil(round(total_sec / 4.6) * 0.68) = ceil(400 * 0.68) = 272` を固定したうえで、
   **factory と motion の cap の比で 272 を割り振る**。motion プールを増やすと factory 側の
   取り分が減り、`_CAP_FACTORY = 1` では減った分だけ **archive クリップがフィルムから落ちる**。
   だから「足した枚数 = 増える distinct」にはならない。
3. **いま盤上にあるフィルムは、いまのビルダーでは再現できない。**
   `remotion/src/data/greene_film.json` は **01:46**、`build_case_film_generic.py` は **01:51**。
   その5分の間に、プランナが factory を **2回使える前提から `check_asset_reuse.MAX_USES_FACTORY = 1`
   を import する形に変わった**。実測でも、盤上のフィルム（factory 73本すべてを使い 28本を2回使用）は
   `cap_f = 2` の解とバイト単位で一致し、`cap_f = 1` の解とは一致しない。**次のビルドは `cap_f = 1`
   で走る。** memphis のフィルム（02:42・distinct 242）は `cap_f = 1` の解と一致しており、これが
   いまの正しい挙動である。

**実測スイープ**（`solve_totals` を実際に呼び、`repeated()` の round-robin まで再現した）:

| 追加枚数 N | motion プール | factory cuts | motion cuts | distinct_video | 234 |
|---:|---:|---:|---:|---:|:--|
| 0 | 123 | 62 | 210 | **185** | fail |
| 37 | 160 | 51 | 221 | 211 | fail |
| 38 | 161 | 50 | 222 | 211 | fail |
| 66 | 189 | 44 | 228 | 233 | fail |
| **67** | **190** | **44** | **228** | **234** | **PASS（最小）** |
| 70 | 193 | 43 | 229 | **236** | PASS |

**導出値 = 67枚。** これが `check_spec_satisfied.py` を通す最小である。
（参考：もし `cap_f` が 2 のままだったなら 38枚で足りた。37 では `cap_f = 2` でも 233 で1本足りない。）

**この発注は 70枚。** 67 は**余裕ゼロ**で、i2v に持ち込めなかったプレートが1枚出た瞬間に
233 に落ちて再びレンダーが止まる。+3 は**その脱落分の余裕**であり、70枚全部が実際にフィルムに
入る（`m = 229 >= 193`）。3枚まで脱落しても 234 を維持する。

**この計算が前提にしている実測値**（変わったら再計算すること）:
`total_sec = 1841.006` · factory プール 73 · motion プール 123 · stills 117 ·
`TARGET_CUT_SEC = 4.6`（greene は `target_cut_sec` を宣言していない）· `MIN_VIDEO_SHARE = 0.68` ·
`_CAP_FACTORY = 1` · `_CAP_MOTION = 2`。

---

## 2. どの区分を増やしたか（id が配置を決める）

**均等には配らない。**そして「配る」の意味がこの pipeline では特殊なので、先に仕組みを書く。

`build_case_film_generic.py` は motion プールを**ソート順で1本のキューに積み**、区分ごとに
`per_m[section]`（＝区分の秒数比）だけ先頭から取っていく。**つまり id の順番が区分を決める。**
盤上のフィルムでも実際にそうなっている（G001→HOOK, G002→OP, G003〜→ACT_1 …）。

追加70枚は既存 `G001`–`G224` の**後ろ**に並ぶので、キューの後半に入る。実測（`solve_totals` +
`split_by_section` を再現）した配置:

| 区分 | 秒数 | 現在の distinct video | 追加後の新規プレート |
|---|---:|---:|---:|
| HOOK | 8.4 | 1 | 0 |
| OP | 10.0 | 2 | 0 |
| ACT_1 | 373.3 | 55 | 0 |
| ACT_2 | 209.8 | 31 | 0 |
| ACT_3 | 297.1 | 43 | 0 |
| **ACT_4** | 287.4 | 43 | **25**（`G243`–`G267`） |
| **ACT_5** | 590.0 | 87 | **45**（`G268`–`G312`） |
| ENDING | 65.1 | 10 | 0 |

**増やしたのは ACT_4 と ACT_5 である。**これは機構の結果であると同時に、カットリストから見ても
正しい：ACT_5 は 590秒・124カット（映画の32%）で**全区分中いちばん長く**、キューが尽きて
折り返し（同じクリップの2回目）が出るのは **ACT_5 の後半と ENDING** である。ACT_4 と ACT_5 を
合わせると 877秒・映像カット130本＝**映画のほぼ半分**で、そこが実際に薄い。

> **★境界は ±3 id ほど動きうる。** 上の内訳はいまのプール実数（factory 73 / motion 123 /
> stills 117 / `total_sec` 1841.006）での計算である。生成までに素材が増減すると区切りが数枚ずれる。
> **ACT_4 と ACT_5 は本編で隣り合っており画づくりの語彙も共通なので、数枚ずれても破綻しない。**
> 破綻するのは「ACT_1 用の絵を ACT_5 に置く」ような大きなずれだけで、それは起きない。

---

## 3. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` / `_v2` を作らない。**「良いのが出るまで回す」を禁止する。
3. **ファイル名は ■ のとおりちょうど。** 別名で出すと、どれが正典か分からなくなります。
4. 作り直してよいのは §4 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。

## 4. ★絶対条件

正典は `episodes/PD-2026-062-greene/episode_spec.v001.json` の `forbidden_subjects` と `era_setting` です。

- **人物は入れる。顔も描いてよい。**（オーナー決定 2026-07-04）禁じられているのは**実在する特定の人物に似ていること**だけ。
  完全に架空の一般人であること。**Linnie Lindsey / Barbara Hodgens / Pamela Ray の3人、および執行官に似せない。**
  カメラ目線の作り笑い・広告のモデル顔にしない。**働いている人の、作っていない顔。**
- **読める文字・数字・手書き・署名・印章・記章・ロゴを描かない。**
  ★**この話で最大の事故源はここです。** 中心にある物は「ドアに貼られた召喚状」であり、生成器はそれを見ると**必ず何か書きます**。
  だから本発注は、`[NEG]` に頼らず**ポジティブ側で紙の形を指定**しています——「完全な白紙」か「均一な灰色の横棒が等間隔に並ぶだけで文字の形が1つも無い面」。
  **バッチCで `[NEG]` だけの禁止が効かないことは実証済み**（`L146` の文字マークが2回戻った）。**この指定文を削らないでください。**
- **時代と場所は 1975–1982年・米国ケンタッキー州ルイビル。**
  現代の車・電話・画面・スニーカー・電動キックボード・EUの標識・ラテン文字以外の文字は不可。
- **立ち退きの最中を描かない。** 歩道に出された家具・追い出される家族・ドアの前の制服の執行官。
- **家主というキャラクターを描かない。** 被告は政府機関（ルイビル住宅公社）です。
- **法廷内観・木槌・判事席・監獄・鉄格子・手錠を描かない。**
- **実在と特定できる建物を描かない。**
- **子どもの顔を描かない。** 子どもは痕跡でのみ表す（本発注では `G254` のチョークだけ）。
- **手は指が数えられること。** 融合した指・6本指・親指の欠落は不可。
  **手が主役のときは必ず「平らな面に伏せて置いた手」**（EP66 `L236` が3回落ちた形と、`L247` で通った形）。
- **黒つぶれさせない。** スマホで見て何が写っているか分かること。

## 5. スタイル（★必ず展開してから生成）

**`[NEG]` は EP66 バッチD の `[NEG]` と1バイト違いません。**この発注書は生成時に `EP66_openfields_CODEX_BATCH_D.v001.md` の本文から**機械的に読み出して**埋め込んでいます（`check_image_order_neg.py` の `neg_block()` そのものを使用）。**1語も変えずに展開してください。**

**`[STYLE]`** ＝ 末尾にそのまま連結（**greene 自身のもの**。バッチDのものは「late Appalachian autumn / rural Pennsylvania and Middle Tennessee」で、ルイビルの映画には天候も州も違う。既存242枚と絵を揃えるためにも greene の正典を使う）:

> , cinematic still, muted natural colour, flat humid Ohio Valley light, low contrast, low-key but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing, mid-1970s to early-1980s American public housing period detail, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> text, lettering, numerals, digits, house numbers, handwriting, cursive writing, legible signature, seals, emblems, logos, insignia, badge, name plates, readable words on a sign, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, police officer, sheriff, trooper, uniform, patrol car, flashing lights, handcuffs, rifle, shotgun, firearm, holster, dead animal, carcass, blood, taxidermy, mounted antlers, courtroom interior, gavel, judge's bench, prison bars, razor wire, scales of justice, hourglass, a handshake, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, aerial view from above the treetops, golden hour, sunset glow, postcard scenery, autumn colour explosion, Christmas, tropical, modern smartphones, laptops, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

> ### ★プレートごとの `[NEG]` 追記について★
> 70枚すべてが `Avoid: [NEG], …` と、`[NEG]` の後ろに読点で語を続けています。
> **これは上の正典 `[NEG]` を展開したうえで、その末尾にさらに続ける、という意味です。**
> **正典 `[NEG]` の語を1語も削らないでください。**追記だけが増えます。
>
> ### ★`[NEG]` は「人」を禁じていません★
> 禁じているのは **`recognisable person, identifiable person, likeness of a real individual,`**
> **`portrait of a named person, celebrity, public figure, deepfake`** ——**実在の誰かに似ること**だけです。
> greene のバッチA の `[NEG]` は `human face, face, facial features, eyes …` と書いて**人が写ること自体**を止めていました。
> EP66 では同じ書き方が **191枚の作り直し**を招いています。**戻さないでください。**
>
> ### ★この発注では `[STYLE]` に時代が入っています★
> greene の `[STYLE]` は `mid-1970s to early-1980s American public housing period detail` を含みます。
> それに加えて**各プロンプト本文にも**「1975–1982年のルイビル」を明記し、`[NEG]` 追記でも現代物を止めています。**三重にしてあるのは、時代違いが実際に出荷されたからです。**

## 6. 命名と保存先

- ファイル名は **■ のとおりちょうど**（`G243.png` など）。**`_v2` / `_02` を付けない。**
- 保存先 `H:\pd-media\assets\ai\greene\`。**既存の `G001`–`G242` を上書きしない。**
- 長辺 3840px 以上・16:9・PNG。

## 7. 対象一覧（70枚）

### ACT_4 — 25枚（`G243`–`G267`）

| # | ID | 台本のビート | 動く要素 |
|---:|---|---|---|
| 1 | `G243` | There was no door left to knock on. | the loose rubber draught strip along the bottom of the door is lifted clear of the floor and curling |
| 2 | `G244` | So they went to federal court, filing a class action ... under section 1983. | the cover of the topmost folder stands half open and is rocking back on itself |
| 3 | `G245` | if posting was constitutionally inadequate on these doors, it was inadequate on every door | the net curtains at three separate windows are all belling outward through their open sashes at once in the same gust |
| 4 | `G246` | It came from that 1950 case, Mullane, and it was already thirty-two years old. | the loose upper pages have stood up off the block and are turning over one at a time in the draught |
| 5 | `G247` | They lost. | the chair is up on its two back legs and tilting |
| 6 | `G248` | the District Court granted judgment for the sheriff and his deputies, in an unreported opinion | the free upper edge of the sheet is curled forward and trembling |
| 7 | `G249` | a case called Weber, decided by the Sixth Circuit some seventy years earlier | dust is lifting off the shelf edge in the slant of light and travelling to the right |
| 8 | `G250` | That was 1909. The presumption was doing all the work. | the volume is tipping: its far end is already lifted clear of the wood and its loose pages have begun to slide out of square |
| 9 | `G251` | It acknowledged that conditions had changed since Weber. | the dry grass growing out of the crack is bent flat along the concrete in a gust and grit is skittering across the slab in the same direction |
| 10 | `G252` | there was undisputed testimony in this case | both reels are turning and the slack loop of tape between them is swinging out of plane |
| 11 | `G253` | notices posted on the apartment doors of tenants are often removed by other tenants | the whole ragged edge is lifting and rippling away from the door and one strip of it has folded right back |
| 12 | `G254` | the depositions in the footnote had said children | the scrap is up on its edge and mid-skitter |
| 13 | `G255` | we always put them up high | the free lower edge of the sheet has lifted right away from the door in the draught and is standing out from the paint |
| 14 | `G256` | posting only comes into play after the officer directed to serve notice cannot find the defendant on the premises | the coat sleeve is out of line with the arm and still swinging |
| 15 | `G257` | So how can a step that happens on the first visit be a last resort? | rainwater is running off the lip of the step in a thin unbroken thread and the dust at the edge of the print is being carried away with it |
| 16 | `G258` | The Sixth Circuit reversed, and overruled Weber to do it. | the door is mid-swing with its leading edge smeared |
| 17 | `G259` | There may have been a time ... That time has passed. | the pendulum is at the far end of its travel and its bob has smeared |
| 18 | `G260` | It reversed the grant of summary judgment and remanded the case for further proceedings. | the folder is mid-slide with its trailing edge lifted off the counter and two of its leaves fanning out behind it |
| 19 | `G261` | Requiring Kentucky to provide notice by mail ... will not be overly burdensome. | the pan has not settled: it is still swinging below its rest and the envelope on it has slid to one side |
| 20 | `G262` | a copy of the petition must be sent by registered or certified mail within a day | the stamp is mid-lift and a thread of ink is drawing away from the pad and breaking |
| 21 | `G263` | The remedy was a stamp, and another State was already buying them. | the lifted corner is rippling in the draught from an open door and the whole sheet has begun to slide on the polished counter |
| 22 | `G264` | The Supreme Court took the appeal in 1981. | the rain is bouncing off the treads in a fine broken veil and a film of water is running down over the nosing of each step |
| 23 | `G265` | It heard argument on the twenty-third of February 1982. | rain is running down the outside of the glass in moving threads and the panel of light on the floor is rippling with them |
| 24 | `G266` | Two lawyers argued it. Two more filed briefs as friends of the court. | the two nearest coats are still swinging on their pegs with their hems well out of vertical and one empty peg is turning |
| 25 | `G267` | Money got a person served. The apartment did not. | the drawer is still travelling out on its runners and the coins in the near compartment are sliding back against its rim |

### ACT_5 — 45枚（`G268`–`G312`）

| # | ID | 台本のビート | 動く要素 |
|---:|---|---|---|
| 1 | `G268` | The opinion was delivered by Justice Brennan. | the fanned pages are riffling from one side to the other and four of them are lifted clear of the block at once |
| 2 | `G269` | notice reasonably calculated, under all the circumstances | one unfolded arm of the rule is still rocking on the concrete and has not come to rest |
| 3 | `G270` | deprived of a significant interest in property — indeed, of the right to continued residence in their homes | the net curtain is travelling across the lit window and the long grass in the foreground is being laid flat in the same gust |
| 4 | `G271` | The sufficiency of notice must be tested with reference to its ability to inform people | the door has swung four inches off its latch and the strip of dark interior beside her is widening |
| 5 | `G272` | its practical application to the affairs of men as they are ordinarily conducted | the worn linen on the line is full of wind and lifting together |
| 6 | `G273` | he usually arranges means to learn of any direct attack upon his possessory or proprietary rights | the loose end of the chain is swinging against the metal and the gate leaf itself is rocking on its hinge |
| 7 | `G274` | Entry upon real estate in the name of law may reasonably be expected to come promptly to the owner's attention. | the gate is mid-swing with its far edge smeared |
| 8 | `G275` | the secure posting of a notice on the property of a person is likely to offer that property owner sufficient warning | the sheet is drum-tight against the glass and vibrating in the wind |
| 9 | `G276` | merely posting notice on an apartment door does not satisfy minimum standards of due process | the sheet is mid-fall with its trailing corner still turning over |
| 10 | `G277` | reliance on posting ... results in a failure to provide actual notice to the tenant concerned | the nearest scraps are mid-skitter down the walkway |
| 11 | `G278` | cannot be considered ... a reliable means of acquainting interested parties of the fact that their rights are before the courts | the tape is falling and turning over |
| 12 | `G279` | Failure to effect personal service on the first visit ... hardly suggests that the tenant has abandoned his interest in the apartment | the door is swinging slowly inward and the hem of the coat is moving with the draught it makes |
| 13 | `G280` | The mails ... provide an efficient and inexpensive means of communication. | the slack mouth of the sack is sagging further open and the top envelopes are sliding down its side |
| 14 | `G281` | Notice by mail in the circumstances of this case would surely go a long way | the free corner of the envelope is lifting off the palm in the moving air and the cuff at the cropped elbow is out of line |
| 15 | `G282` | the subject matter of the action also happens to be the mailing address of the defendant | the open box door is swinging on its hinge and the envelope is sliding out of the slot |
| 16 | `G283` | The apartment they were trying to take was the place they would have got the letter. | the slot's metal flap is clapping open and shut in the wind and the bottom corner of the sheet above it is lifting on the same gusts |
| 17 | `G284` | The State's continued exclusive reliance on an ineffective means of service | the drum is turning with its surface smeared and one sheet is caught halfway out of the machine |
| 18 | `G285` | the State has deprived them of property without the due process of law | the door is moving on its hinge and the shape of daylight it lays on the bare floor is sliding across the boards |
| 19 | `G286` | we hold only that posted notice pursuant to section 454.030 is constitutionally inadequate | the beam is narrowing as the door drifts closed and its edge is travelling across the boards |
| 20 | `G287` | It is not our responsibility to prescribe the form of service that the Commonwealth should adopt. | one loose sheet standing on edge in a hole halfway down the rack is buckling and about to fall out of it |
| 21 | `G288` | even conceding that process served by mail is far from the ideal means | rain rings are spreading across the puddle and the envelope's free corner is lifting and floating on the moving water |
| 22 | `G289` | posted service accompanied by mail service is constitutionally preferable to posted service alone | both papers are moving in the same gust and out of phase with each other |
| 23 | `G290` | ⟨HELD⟩ | the scrap lies still except for one corner that is ticking up and down |
| 24 | `G291` | Affirmed does not mean three tenants walked out holding a key. | the key's steel ring is still spinning flat on the formica beside it |
| 25 | `G292` | It simply stops. | grit and one pale scrap of paper are blowing along the walkway and piling up against the foot of the brick |
| 26 | `G293` | Three Justices did not agree, and the dissent is not a footnote. | the nearest of the three chairs is still rocking on its back legs and a curtain at the window is travelling across the light |
| 27 | `G294` | the Court holds that the Constitution prefers the use of the Postal Service to posted notice | the envelope is mid-push under the grille and the grille's loose chain is swinging against the bars |
| 28 | `G295` | despite the total absence of any evidence in the record regarding the speed and reliability of the mails | dust is turning in the shaft of light and the free corner of the blotter is lifting off the desk |
| 29 | `G296` | The sole ground for the Court's result is the scant and conflicting testimony of a handful of process servers in Kentucky. | two of the pages are lifting at once in a draught |
| 30 | `G297` | the Court confidently overturns the work of the Kentucky Legislature, and, by implication, that of at least 10 other States | one door far down the line is mid-swing and is the only thing in the frame that is not still |
| 31 | `G298` | does not cite a single case, other than the decision below | dust is lifting along the shelf toward the camera and the book's front cover is standing up and dropping back in the draught |
| 32 | `G299` | at least 11 States authorizing notice in summary eviction proceedings solely by posting | steam is rising from every one of them and drifting the same way across the table |
| 33 | `G300` | Both opinions read the same three clauses. One read the words. The other read the depositions. | both pages are bowing and rattling in the draught from the open sash |
| 34 | `G301` | we decline to resolve the constitutional question based upon the determination whether the particular action is more properly characterized as one in rem or in personam | a loose sheet of paper is caught on the rim of the nearer crate and is flapping hard |
| 35 | `G302` | What the paper did was the question. | water is creeping visibly across the sheet and one corner has lifted clear of the wet and is curling up |
| 36 | `G303` | The Court gives lipservice to the principle ... but then goes on to do just that. | the door is pressing and easing against the wedge in the wind and the wedge's loose outer leaves are fanning open |
| 37 | `G304` | we have long since discarded the concept that due process authorizes courts to hold laws unconstitutional when they believe the legislature has acted unwisely | one pale scrap of paper is travelling down the flight and is caught mid-bounce between two treads |
| 38 | `G305` | It is no secret, after all, that unattended mailboxes are subject to plunder by thieves. | the hanging door is swinging on its one hinge and the caught paper is flicking with it |
| 39 | `G306` | posting notice at least gives assurance that the notice has gotten as far as the tenant's door | the whole free edge of the sheet is standing right off the door in the wind and its shadow is sweeping across the paint |
| 40 | `G307` | The dissent misconstrues the constitutional standard. | the string is vibrating and the shadow line has smeared into a band |
| 41 | `G308` | a summary proceeding for quickly determining whether or not a landlord has the right to immediate possession | rain is blowing across the open side of the stairwell in visible bands and water is running down the rail past the hand |
| 42 | `G309` | Many expenses of the landlord continue to accrue whether a tenant pays his rent or not. | one drop is caught mid-fall below the spout and the ring it made a moment ago is still spreading in the standing water on the grate |
| 43 | `G310` | The means chosen for making service of process ... must be prompt and certain | the closer's arm is mid-travel and folding |
| 44 | `G311` | it is difficult to see how a means of serving process that fails to afford actual notice ... can be deemed either prompt or certain | a shadow is crossing the bar of daylight under the door and passing on |
| 45 | `G312` | That is where the two opinions stop talking to each other. | both doors are breathing against their latches in the same draught and one is a finger's width further open than the other |

---

## 8. プロンプト（各1枚）

### ── ACT_4 ──

#### `G243.png` — ACT_4

**台本のビート:** There was no door left to knock on.

**動く要素（i2v が動かす対象）:** the loose rubber draught strip along the bottom of the door is lifted clear of the floor and curling, and a bare bulb on a flex hangs well out of vertical so the shadows of the door frame are sliding across the wall

- `G243.png`
A shut painted door at the far end of a narrow public corridor, photographed from twelve paces at chest height, the only light a high dirty window halfway down the corridor that lays one pale panel across the floor and leaves the door itself in flat shadow, nobody in the corridor. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the loose rubber draught strip along the bottom of the door is lifted clear of the floor and curling, and a bare bulb on a flex hangs well out of vertical so the shadows of the door frame are sliding across the wall [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, bright cheerful corridor, hotel corridor, hospital corridor, office suite

**保存先:** `H:\pd-media\assets\ai\greene\G243.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, bright cheerful corridor, hotel corridor, hospital corridor, office suite` を足す。**正典側は1語も削らない。**

#### `G244.png` — ACT_4

**台本のビート:** So they went to federal court, filing a class action ... under section 1983.

**動く要素（i2v が動かす対象）:** the cover of the topmost folder stands half open and is rocking back on itself, its loose leaves fanned and out of line, driven by a desk fan whose blades are turning in the soft background

- `G244.png`
A shallow wire tray of plain unmarked buff folders standing on a public counter, photographed from counter height at half a metre with the counter running out of frame to both sides, flat window light from the left. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the cover of the topmost folder stands half open and is rocking back on itself, its loose leaves fanned and out of line, driven by a desk fan whose blades are turning in the soft background [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note

**保存先:** `H:\pd-media\assets\ai\greene\G244.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note` を足す。**正典側は1語も削らない。**

#### `G245.png` — ACT_4

**台本のビート:** if posting was constitutionally inadequate on these doors, it was inadequate on every door

**動く要素（i2v が動かす対象）:** the net curtains at three separate windows are all belling outward through their open sashes at once in the same gust, and the balustrade's loose safety rope is swinging

- `G245.png`
An open-air concrete walkway of identical painted doors along the first floor of a low-rise dark red brick block, photographed from the walkway itself at a low three-quarter angle at hip height so the doors and the balustrade both run away to a point, flat overcast midday light, nobody on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the net curtains at three separate windows are all belling outward through their open sashes at once in the same gust, and the balustrade's loose safety rope is swinging [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, identical modern apartment block, glass balustrade, motel corridor, self-storage units, roller shutters

**保存先:** `H:\pd-media\assets\ai\greene\G245.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, identical modern apartment block, glass balustrade, motel corridor, self-storage units, roller shutters` を足す。**正典側は1語も削らない。**

#### `G246.png` — ACT_4

**台本のビート:** It came from that 1950 case, Mullane, and it was already thirty-two years old.

**動く要素（i2v が動かす対象）:** the loose upper pages have stood up off the block and are turning over one at a time in the draught, three of them in the air at once and out of line with each other

- `G246.png`
A thick bound volume lying open on a plain wooden table directly beneath a sash window that stands open four inches, photographed from the far side of the table at tabletop level at one metre in cold flat daylight. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the loose upper pages have stood up off the block and are turning over one at a time in the draught, three of them in the air at once and out of line with each other [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note

**保存先:** `H:\pd-media\assets\ai\greene\G246.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note` を足す。**正典側は1語も削らない。**

#### `G247.png` — ACT_4

**台本のビート:** They lost.

**動く要素（i2v が動かす対象）:** the chair is up on its two back legs and tilting, not yet settled, and the dust in the shaft of light is turning in a slow column

- `G247.png`
A plain wooden chair pushed back hard from a bare table in an otherwise empty room, photographed from the open doorway at eight paces at standing height, one window on the far wall throwing a single slanted shaft across the floorboards. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the chair is up on its two back legs and tilting, not yet settled, and the dust in the shaft of light is turning in a slow column [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, dining room, restaurant, staged interior

**保存先:** `H:\pd-media\assets\ai\greene\G247.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, dining room, restaurant, staged interior` を足す。**正典側は1語も削らない。**

#### `G248.png` — ACT_4

**台本のビート:** the District Court granted judgment for the sheriff and his deputies, in an unreported opinion

**動く要素（i2v が動かす対象）:** the free upper edge of the sheet is curled forward and trembling, and a thin curtain at the window behind is travelling across the light

- `G248.png`
A manual typewriter of the period on a plain desk with a single sheet rolled into the platen, photographed from the side at forty centimetres so the sheet stands up against a bright window that is out of focus behind it. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the free upper edge of the sheet is curled forward and trembling, and a thin curtain at the window behind is travelling across the light [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, electric typewriter, modern keyboard

**保存先:** `H:\pd-media\assets\ai\greene\G248.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, electric typewriter, modern keyboard` を足す。**正典側は1語も削らない。**

#### `G249.png` — ACT_4

**台本のビート:** a case called Weber, decided by the Sixth Circuit some seventy years earlier

**動く要素（i2v が動かす対象）:** dust is lifting off the shelf edge in the slant of light and travelling to the right, and one ledger stands proud of the row and is tilting out of it

- `G249.png`
A run of old worn leather ledger spines packed on a low shelf, photographed square on at half a metre in a hard slant of window light that rakes across their ribs and leaves the shelf below them dark. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: dust is lifting off the shelf edge in the slant of light and travelling to the right, and one ledger stands proud of the row and is tilting out of it [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, gilt titles, spine labels, library classification

**保存先:** `H:\pd-media\assets\ai\greene\G249.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, gilt titles, spine labels, library classification` を足す。**正典側は1語も削らない。**

#### `G250.png` — ACT_4

**台本のビート:** That was 1909. The presumption was doing all the work.

**動く要素（i2v が動かす対象）:** the volume is tipping: its far end is already lifted clear of the wood and its loose pages have begun to slide out of square

- `G250.png`
One heavy bound volume balanced on the edge of a plain table with three quarters of its length overhanging the drop, photographed from table height at sixty centimetres so the overhang runs at the camera, one hard light raking from the left. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the volume is tipping: its far end is already lifted clear of the wood and its loose pages have begun to slide out of square [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note

**保存先:** `H:\pd-media\assets\ai\greene\G250.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note` を足す。**正典側は1語も削らない。**

#### `G251.png` — ACT_4

**台本のビート:** It acknowledged that conditions had changed since Weber.

**動く要素（i2v が動かす対象）:** the dry grass growing out of the crack is bent flat along the concrete in a gust and grit is skittering across the slab in the same direction

- `G251.png`
A wide crack running right across a poured concrete walkway slab, photographed from ankle height at close range so the crack opens toward the camera and the walkway runs away out of focus behind it, flat grey daylight. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the dry grass growing out of the crack is bent flat along the concrete in a gust and grit is skittering across the slab in the same direction [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, earthquake damage, disaster scene, rubble

**保存先:** `H:\pd-media\assets\ai\greene\G251.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, earthquake damage, disaster scene, rubble` を足す。**正典側は1語も削らない。**

#### `G252.png` — ACT_4

**台本のビート:** there was undisputed testimony in this case

**動く要素（i2v が動かす対象）:** both reels are turning and the slack loop of tape between them is swinging out of plane

- `G252.png`
A reel-to-reel tape deck of the period standing on a plain table, photographed at a steep three-quarter from above at seventy centimetres with the take-up reel half full, one warm desk lamp low to the left and the rest of the room dark but never black. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: both reels are turning and the slack loop of tape between them is swinging out of plane [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, recording studio, mixing desk, modern audio equipment

**保存先:** `H:\pd-media\assets\ai\greene\G252.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, recording studio, mixing desk, modern audio equipment` を足す。**正典側は1語も削らない。**

#### `G253.png` — ACT_4

**台本のビート:** notices posted on the apartment doors of tenants are often removed by other tenants

**動く要素（i2v が動かす対象）:** the whole ragged edge is lifting and rippling away from the door and one strip of it has folded right back

- `G253.png`
A sheet on a painted apartment door whose lower two thirds have already been torn away, the ragged edge standing out from the paint, photographed at thirty centimetres from just below the tear so the flat light off the walkway comes past it and lights the torn fibres. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character -- and the grey bars stop where the tear runs. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the whole ragged edge is lifting and rippling away from the door and one strip of it has folded right back [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note

**保存先:** `H:\pd-media\assets\ai\greene\G253.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note` を足す。**正典側は1語も削らない。**

#### `G254.png` — ACT_4

**台本のビート:** the depositions in the footnote had said children

**動く要素（i2v が動かす対象）:** the scrap is up on its edge and mid-skitter, about to blow clear of the door, and chalk dust is drifting off the concrete with it

- `G254.png`
Chalk marks left low on the concrete at the foot of a painted apartment door, drawn at the height of somebody very small, with a scrap of pale paper caught against the kick plate, photographed from knee height at one metre in flat overcast light, nobody in the frame. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the scrap is up on its edge and mid-skitter, about to blow clear of the door, and chalk dust is drifting off the concrete with it [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, a child in frame, a face, a toy, playground equipment

**保存先:** `H:\pd-media\assets\ai\greene\G254.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, a child in frame, a face, a toy, playground equipment` を足す。**正典側は1語も削らない。**

#### `G255.png` — ACT_4

**台本のビート:** we always put them up high

**動く要素（i2v が動かす対象）:** the free lower edge of the sheet has lifted right away from the door in the draught and is standing out from the paint

- `G255.png`
The flat of one adult hand pressed against a painted apartment door high above the handle, holding a sheet flat to the paint, photographed from the side at forty-five centimetres at that same height, the arm cropped at the elbow and no other part of the person in the frame, flat walkway light. THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE AND SEPARATE with a line of shadow between each pair and one nail showing on each, and the thumb clearly apart from the fingers along the near side -- here the surface is the door itself and the paper under the palm. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the free lower edge of the sheet has lifted right away from the door in the draught and is standing out from the paint [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, uniform sleeve, epaulette, cuff braid

**保存先:** `H:\pd-media\assets\ai\greene\G255.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, uniform sleeve, epaulette, cuff braid` を足す。**正典側は1語も削らない。**

#### `G256.png` — ACT_4

**台本のビート:** posting only comes into play after the officer directed to serve notice cannot find the defendant on the premises

**動く要素（i2v が動かす対象）:** the coat sleeve is out of line with the arm and still swinging, and a pale corner of paper at the top edge of the frame is lifting

- `G256.png`
Seen from the open walkway below and behind, one arm reaching up into the top of the frame toward a door, cropped at the shoulder with no other part of the person visible and no face anywhere in the picture, the concrete soffit and the underside of the walkway filling the upper corner, photographed at two metres in flat grey light. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the coat sleeve is out of line with the arm and still swinging, and a pale corner of paper at the top edge of the frame is lifting [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, uniform sleeve, epaulette, cuff braid, full figure in frame

**保存先:** `H:\pd-media\assets\ai\greene\G256.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, uniform sleeve, epaulette, cuff braid, full figure in frame` を足す。**正典側は1語も削らない。**

#### `G257.png` — ACT_4

**台本のビート:** So how can a step that happens on the first visit be a last resort?

**動く要素（i2v が動かす対象）:** rainwater is running off the lip of the step in a thin unbroken thread and the dust at the edge of the print is being carried away with it

- `G257.png`
A concrete doorstep carrying one single fresh shoe print in wet dust and no second print anywhere on it, photographed obliquely from one metre at knee height so the step runs across the frame, flat wet daylight. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: rainwater is running off the lip of the step in a thin unbroken thread and the dust at the edge of the print is being carried away with it [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, footprint in snow, crime scene, forensic marker

**保存先:** `H:\pd-media\assets\ai\greene\G257.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, footprint in snow, crime scene, forensic marker` を足す。**正典側は1語も削らない。**

#### `G258.png` — ACT_4

**台本のビート:** The Sixth Circuit reversed, and overruled Weber to do it.

**動く要素（i2v が動かす対象）:** the door is mid-swing with its leading edge smeared, and the wedge of light on the floor is travelling with it

- `G258.png`
A heavy timber door of a plain public building swinging inward, the widening wedge of daylight sweeping across a worn stone floor, photographed from inside at four paces at waist height with the room beyond dark but holding its detail. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the door is mid-swing with its leading edge smeared, and the wedge of light on the floor is travelling with it [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, courthouse portico, carved motto, memorial plaque, church interior

**保存先:** `H:\pd-media\assets\ai\greene\G258.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, courthouse portico, carved motto, memorial plaque, church interior` を足す。**正典側は1語も削らない。**

#### `G259.png` — ACT_4

**台本のビート:** There may have been a time ... That time has passed.

**動く要素（i2v が動かす対象）:** the pendulum is at the far end of its travel and its bob has smeared, and the bob's shadow is running across the wall behind it

- `G259.png`
A pendulum wall clock in a plain hallway seen from below and well to one side so the dial is turned away from the camera and only the case, the glass door and the swinging pendulum are in view, photographed at two paces at chest height in cold daylight from a window out of frame. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the pendulum is at the far end of its travel and its bob has smeared, and the bob's shadow is running across the wall behind it [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, clock face, dial in view, hands of a clock, hourglass, stopwatch

**保存先:** `H:\pd-media\assets\ai\greene\G259.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, clock face, dial in view, hands of a clock, hourglass, stopwatch` を足す。**正典側は1語も削らない。**

#### `G260.png` — ACT_4

**台本のビート:** It reversed the grant of summary judgment and remanded the case for further proceedings.

**動く要素（i2v が動かす対象）:** the folder is mid-slide with its trailing edge lifted off the counter and two of its leaves fanning out behind it

- `G260.png`
A plain unmarked folder being slid back across a wooden public counter toward the camera by one flat hand, photographed at counter height at half a metre, the hand cropped at the wrist. THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE AND SEPARATE with a line of shadow between each pair and one nail showing on each, and the thumb clearly apart from the fingers along the near side -- here the surface is the folder. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character on the loose leaves that have come out of it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the folder is mid-slide with its trailing edge lifted off the counter and two of its leaves fanning out behind it [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand

**保存先:** `H:\pd-media\assets\ai\greene\G260.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand` を足す。**正典側は1語も削らない。**

#### `G261.png` — ACT_4

**台本のビート:** Requiring Kentucky to provide notice by mail ... will not be overly burdensome.

**動く要素（i2v が動かす対象）:** the pan has not settled: it is still swinging below its rest and the envelope on it has slid to one side

- `G261.png`
A small brass postal balance on a wooden counter with one plain envelope lying in its pan, photographed at pan height at thirty centimetres with the dial turned away from the camera so only the back of its case shows, one soft window light from the left. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the pan has not settled: it is still swinging below its rest and the envelope on it has slid to one side [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, dial in view, gauge markings, kitchen scales, digital scales

**保存先:** `H:\pd-media\assets\ai\greene\G261.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, dial in view, gauge markings, kitchen scales, digital scales` を足す。**正典側は1語も削らない。**

#### `G262.png` — ACT_4

**台本のビート:** a copy of the petition must be sent by registered or certified mail within a day

**動く要素（i2v が動かす対象）:** the stamp is mid-lift and a thread of ink is drawing away from the pad and breaking

- `G262.png`
A rubber stamp lifted clear of an open ink pad with wet ink glistening on its face, the face itself an even bare rubber pad with nothing cut into it, photographed from the side at twenty centimetres against a dark wooden counter under one hard low light. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the stamp is mid-lift and a thread of ink is drawing away from the pad and breaking [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, cut lettering on the stamp face, date stamp, official seal, monogram

**保存先:** `H:\pd-media\assets\ai\greene\G262.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, cut lettering on the stamp face, date stamp, official seal, monogram` を足す。**正典側は1語も削らない。**

#### `G263.png` — ACT_4

**台本のビート:** The remedy was a stamp, and another State was already buying them.

**動く要素（i2v が動かす対象）:** the lifted corner is rippling in the draught from an open door and the whole sheet has begun to slide on the polished counter

- `G263.png`
A sheet of small perforated paper squares lying on a wooden counter with one corner lifted, each square an even field of one flat faded colour with nothing figured on it at all, photographed at thirty centimetres at a low oblique so the perforations catch the raking light. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the lifted corner is rippling in the draught from an open door and the whole sheet has begun to slide on the polished counter [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, portrait on a banknote, engraved head on currency, engraved head on a stamp, denomination, printed value, stamp design, portrait

**保存先:** `H:\pd-media\assets\ai\greene\G263.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, portrait on a banknote, engraved head on currency, engraved head on a stamp, denomination, printed value, stamp design, portrait` を足す。**正典側は1語も削らない。**

#### `G264.png` — ACT_4

**台本のビート:** The Supreme Court took the appeal in 1981.

**動く要素（i2v が動かす対象）:** the rain is bouncing off the treads in a fine broken veil and a film of water is running down over the nosing of each step

- `G264.png`
The wet stone steps of a plain public building seen from the bottom at a steep upward angle in heavy rain, nobody on them, photographed at one metre in flat grey light with the treads running up out of the top of the frame. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the rain is bouncing off the treads in a fine broken veil and a film of water is running down over the nosing of each step [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, courthouse portico, columns, carved motto, statue, flag

**保存先:** `H:\pd-media\assets\ai\greene\G264.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, courthouse portico, columns, carved motto, statue, flag` を足す。**正典側は1語も削らない。**

#### `G265.png` — ACT_4

**台本のビート:** It heard argument on the twenty-third of February 1982.

**動く要素（i2v が動かす対象）:** rain is running down the outside of the glass in moving threads and the panel of light on the floor is rippling with them

- `G265.png`
A tall window in the bare lobby of a plain public building seen from inside at six paces at chest height, low February daylight coming through it and lying in one long panel on the stone floor, nobody in the lobby. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: rain is running down the outside of the glass in moving threads and the panel of light on the floor is rippling with them [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, courtroom, judge's bench, gallery seating, stained glass, church

**保存先:** `H:\pd-media\assets\ai\greene\G265.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, courtroom, judge's bench, gallery seating, stained glass, church` を足す。**正典側は1語も削らない。**

#### `G266.png` — ACT_4

**台本のビート:** Two lawyers argued it. Two more filed briefs as friends of the court.

**動く要素（i2v が動かす対象）:** the two nearest coats are still swinging on their pegs with their hems well out of vertical and one empty peg is turning

- `G266.png`
Four heavy overcoats hung on a row of pegs in a cold public cloakroom, photographed square on at three paces at chest height in flat light from a high window. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the two nearest coats are still swinging on their pegs with their hems well out of vertical and one empty peg is turning [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, uniform coat, braid, epaulette, hat with a badge, school cloakroom

**保存先:** `H:\pd-media\assets\ai\greene\G266.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, uniform coat, braid, epaulette, hat with a badge, school cloakroom` を足す。**正典側は1語も削らない。**

#### `G267.png` — ACT_4

**台本のビート:** Money got a person served. The apartment did not.

**動く要素（i2v が動かす対象）:** the drawer is still travelling out on its runners and the coins in the near compartment are sliding back against its rim

- `G267.png`
One flat hand laid on a wooden shop counter beside a small brass cash drawer that stands half open on its runners, the compartments holding worn coins seen edge on, photographed at counter height at thirty centimetres, the hand cropped at the wrist. THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE AND SEPARATE with a line of shadow between each pair and one nail showing on each, and the thumb clearly apart from the fingers along the near side -- here the surface is the counter. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the drawer is still travelling out on its runners and the coins in the near compartment are sliding back against its rim [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, portrait on a banknote, engraved head on currency, engraved head on a stamp, banknotes face up, currency portrait, cash register display

**保存先:** `H:\pd-media\assets\ai\greene\G267.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, portrait on a banknote, engraved head on currency, engraved head on a stamp, banknotes face up, currency portrait, cash register display` を足す。**正典側は1語も削らない。**

### ── ACT_5 ──

#### `G268.png` — ACT_5

**台本のビート:** The opinion was delivered by Justice Brennan.

**動く要素（i2v が動かす対象）:** the fanned pages are riffling from one side to the other and four of them are lifted clear of the block at once

- `G268.png`
One bound volume standing open on a plain reading stand, photographed edge on at eye height at eighty centimetres so the block of pages fans toward the camera, a single high window light behind and above it. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the fanned pages are riffling from one side to the other and four of them are lifted clear of the block at once [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, lectern in a church, bible, illuminated manuscript

**保存先:** `H:\pd-media\assets\ai\greene\G268.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, lectern in a church, bible, illuminated manuscript` を足す。**正典側は1語も削らない。**

#### `G269.png` — ACT_5

**台本のビート:** notice reasonably calculated, under all the circumstances

**動く要素（i2v が動かす対象）:** one unfolded arm of the rule is still rocking on the concrete and has not come to rest

- `G269.png`
A folding wooden rule lying half unfolded on a concrete step, its faces worn smooth and bare of any marking at all, photographed at thirty centimetres at step level in flat grey daylight. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: one unfolded arm of the rule is still rocking on the concrete and has not come to rest [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, measurement markings, graduations, tape measure, ruler with numbers

**保存先:** `H:\pd-media\assets\ai\greene\G269.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, measurement markings, graduations, tape measure, ruler with numbers` を足す。**正典側は1語も削らない。**

#### `G270.png` — ACT_5

**台本のビート:** deprived of a significant interest in property — indeed, of the right to continued residence in their homes

**動く要素（i2v が動かす対象）:** the net curtain is travelling across the lit window and the long grass in the foreground is being laid flat in the same gust

- `G270.png`
One lit kitchen window in a low-rise dark red brick block seen from the communal grass at thirty paces at the blue end of dusk with no sun anywhere in the sky, the room behind the net curtain warm and the brick around it cold. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the net curtain is travelling across the lit window and the long grass in the foreground is being laid flat in the same gust [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, golden window glow, cosy interior, Christmas lights, postcard dusk, city skyline

**保存先:** `H:\pd-media\assets\ai\greene\G270.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, golden window glow, cosy interior, Christmas lights, postcard dusk, city skyline` を足す。**正典側は1語も削らない。**

#### `G271.png` — ACT_5

**台本のビート:** The sufficiency of notice must be tested with reference to its ability to inform people

**動く要素（i2v が動かす対象）:** the door has swung four inches off its latch and the strip of dark interior beside her is widening

- `G271.png`
An invented woman in her thirties in a plain 1970s coat standing at her own painted apartment door in three-quarter view, photographed from three paces at eye height, her face lit evenly by flat cloud with no expression put on for the camera and not looking at the lens, one open hand laid flat against the paint beside the door frame. THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE AND SEPARATE with a line of shadow between each pair and one nail showing on each, and the thumb clearly apart from the fingers along the near side -- here the surface is the door. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the door has swung four inches off its latch and the strip of dark interior beside her is widening [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, posed model, advertising smile, eye contact with the lens, glamour lighting

**保存先:** `H:\pd-media\assets\ai\greene\G271.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, posed model, advertising smile, eye contact with the lens, glamour lighting` を足す。**正典側は1語も削らない。**

#### `G272.png` — ACT_5

**台本のビート:** its practical application to the affairs of men as they are ordinarily conducted

**動く要素（i2v が動かす対象）:** the worn linen on the line is full of wind and lifting together, and the line itself is bowing

- `G272.png`
An invented woman in her forties in a plain housecoat working along a communal washing line strung between two brick blocks, seen in three-quarter from four paces at chest height, her face lit evenly by flat cloud with no expression put on for the camera and not looking at the lens, one open hand laid flat along the linen she is straightening. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the worn linen on the line is full of wind and lifting together, and the line itself is bowing [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, posed model, advertising smile, eye contact with the lens, sunlit meadow

**保存先:** `H:\pd-media\assets\ai\greene\G272.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, posed model, advertising smile, eye contact with the lens, sunlit meadow` を足す。**正典側は1語も削らない。**

#### `G273.png` — ACT_5

**台本のビート:** he usually arranges means to learn of any direct attack upon his possessory or proprietary rights

**動く要素（i2v が動かす対象）:** the loose end of the chain is swinging against the metal and the gate leaf itself is rocking on its hinge

- `G273.png`
A chain and padlock threaded through the bars of a yard gate, photographed at twenty centimetres in cold flat light with the yard behind it out of focus. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the loose end of the chain is swinging against the metal and the gate leaf itself is rocking on its hinge [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, prison gate, razor wire, security fence, padlock with a brand

**保存先:** `H:\pd-media\assets\ai\greene\G273.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, prison gate, razor wire, security fence, padlock with a brand` を足す。**正典側は1語も削らない。**

#### `G274.png` — ACT_5

**台本のビート:** Entry upon real estate in the name of law may reasonably be expected to come promptly to the owner's attention.

**動く要素（i2v が動かす対象）:** the gate is mid-swing with its far edge smeared, and dust lifted off the gravel is travelling across the drive

- `G274.png`
A plain front gate standing open onto a gravel drive, photographed from the house side at ten paces at chest height in flat overcast light with nobody in the frame. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the gate is mid-swing with its far edge smeared, and dust lifted off the gravel is travelling across the drive [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, suburban mansion, ornamental garden, wrought iron crest, gated community

**保存先:** `H:\pd-media\assets\ai\greene\G274.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, suburban mansion, ornamental garden, wrought iron crest, gated community` を足す。**正典側は1語も削らない。**

#### `G275.png` — ACT_5

**台本のビート:** the secure posting of a notice on the property of a person is likely to offer that property owner sufficient warning

**動く要素（i2v が動かす対象）:** the sheet is drum-tight against the glass and vibrating in the wind, and its bottom corner has come away from the tape

- `G275.png`
A sheet taped flat against the glass panel of a communal stair door, photographed from inside the stairwell at one metre so the sheet is back-lit by the daylight outside and its fibres and the tape's shadow show through it. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the sheet is drum-tight against the glass and vibrating in the wind, and its bottom corner has come away from the tape [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, shop window notice, poster, advertisement

**保存先:** `H:\pd-media\assets\ai\greene\G275.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, shop window notice, poster, advertisement` を足す。**正典側は1語も削らない。**

#### `G276.png` — ACT_5

**台本のビート:** merely posting notice on an apartment door does not satisfy minimum standards of due process

**動く要素（i2v が動かす対象）:** the sheet is mid-fall with its trailing corner still turning over, and the free tape ends on the door are lifting

- `G276.png`
A sheet in the air a foot clear of a painted apartment door, already off its tape and caught side on so it reads as a thin bright edge, the door and its two strips of tape soft behind it, photographed at one metre in flat overcast walkway light. The sheet is falling. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the sheet is mid-fall with its trailing corner still turning over, and the free tape ends on the door are lifting [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, confetti, flying papers everywhere, storm of paper

**保存先:** `H:\pd-media\assets\ai\greene\G276.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, confetti, flying papers everywhere, storm of paper` を足す。**正典側は1語も削らない。**

#### `G277.png` — ACT_5

**台本のビート:** reliance on posting ... results in a failure to provide actual notice to the tenant concerned

**動く要素（i2v が動かす対象）:** the nearest scraps are mid-skitter down the walkway, one of them up on its edge and turning over

- `G277.png`
A run of apartment doors down an open walkway at flat midday with pale scraps of torn paper lying along the concrete at their feet, photographed from one end at knee height so the scraps run away into the distance. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the nearest scraps are mid-skitter down the walkway, one of them up on its edge and turning over [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, litter-strewn slum, refuse sacks, vandalism, graffiti

**保存先:** `H:\pd-media\assets\ai\greene\G277.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, litter-strewn slum, refuse sacks, vandalism, graffiti` を足す。**正典側は1語も削らない。**

#### `G278.png` — ACT_5

**台本のビート:** cannot be considered ... a reliable means of acquainting interested parties of the fact that their rights are before the courts

**動く要素（i2v が動かす対象）:** the tape is falling and turning over, and the two clean unfaded rectangles it has left on the paint are exposed behind it

- `G278.png`
A curled strip of adhesive tape that has let go at both ends, caught in the air just clear of the painted door it came off, photographed at fifteen centimetres in raking light so its curl throws a shadow on the paint. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the tape is falling and turning over, and the two clean unfaded rectangles it has left on the paint are exposed behind it [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, sticky tape dispenser, packing tape, brand on the tape

**保存先:** `H:\pd-media\assets\ai\greene\G278.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, sticky tape dispenser, packing tape, brand on the tape` を足す。**正典側は1語も削らない。**

#### `G279.png` — ACT_5

**台本のビート:** Failure to effect personal service on the first visit ... hardly suggests that the tenant has abandoned his interest in the apartment

**動く要素（i2v が動かす対象）:** the door is swinging slowly inward and the hem of the coat is moving with the draught it makes

- `G279.png`
A worn doormat with a pair of shoes set neatly against the wall beside it and a coat still on its hook just inside a half-open front door, photographed from three paces at knee height in flat daylight from the walkway. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the door is swinging slowly inward and the hem of the coat is moving with the draught it makes [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, welcome mat with words, holiday wreath, staged hallway

**保存先:** `H:\pd-media\assets\ai\greene\G279.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, welcome mat with words, holiday wreath, staged hallway` を足す。**正典側は1語も削らない。**

#### `G280.png` — ACT_5

**台本のビート:** The mails ... provide an efficient and inexpensive means of communication.

**動く要素（i2v が動かす対象）:** the slack mouth of the sack is sagging further open and the top envelopes are sliding down its side

- `G280.png`
An invented man in his fifties in plain post-room clothes standing over a canvas mail sack filled to its mouth with plain envelopes, seen in three-quarter from a metre at sack height, his face lit evenly by an overhead lamp with no expression put on for the camera and not looking at the lens, both hands laid flat on the sack's rim. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it on the envelopes. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the slack mouth of the sack is sagging further open and the top envelopes are sliding down its side [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, postal uniform, cap with a badge, courier branding, advertising smile, eye contact with the lens

**保存先:** `H:\pd-media\assets\ai\greene\G280.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, postal uniform, cap with a badge, courier branding, advertising smile, eye contact with the lens` を足す。**正典側は1語も削らない。**

#### `G281.png` — ACT_5

**台本のビート:** Notice by mail in the circumstances of this case would surely go a long way

**動く要素（i2v が動かす対象）:** the free corner of the envelope is lifting off the palm in the moving air and the cuff at the cropped elbow is out of line

- `G281.png`
A plain envelope carried flat on one open upturned palm along an open walkway, the arm cropped at the elbow and no other part of the person in frame, photographed from the side at fifty centimetres with the walkway running away out of focus behind. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the free corner of the envelope is lifting off the palm in the moving air and the cuff at the cropped elbow is out of line [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand

**保存先:** `H:\pd-media\assets\ai\greene\G281.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand` を足す。**正典側は1語も削らない。**

#### `G282.png` — ACT_5

**台本のビート:** the subject matter of the action also happens to be the mailing address of the defendant

**動く要素（i2v が動かす対象）:** the open box door is swinging on its hinge and the envelope is sliding out of the slot

- `G282.png`
A bank of plain apartment letter boxes photographed from directly beneath at a steep upward angle at forty centimetres so the boxes loom over the camera, one small door hanging open and an envelope half out of it, cold stairwell light. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the open box door is swinging on its hinge and the envelope is sliding out of the slot [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, apartment numbers, name plates on the boxes, intercom panel

**保存先:** `H:\pd-media\assets\ai\greene\G282.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, apartment numbers, name plates on the boxes, intercom panel` を足す。**正典側は1語も削らない。**

#### `G283.png` — ACT_5

**台本のビート:** The apartment they were trying to take was the place they would have got the letter.

**動く要素（i2v が動かす対象）:** the slot's metal flap is clapping open and shut in the wind and the bottom corner of the sheet above it is lifting on the same gusts

- `G283.png`
A painted front door with a letter slot in it and a sheet taped above the slot at head height, photographed from two paces at chest height square on in flat overcast light. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character on the sheet. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the slot's metal flap is clapping open and shut in the wind and the bottom corner of the sheet above it is lifting on the same gusts [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, house number, name plate, door knocker with a face

**保存先:** `H:\pd-media\assets\ai\greene\G283.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, house number, name plate, door knocker with a face` を足す。**正典側は1語も削らない。**

#### `G284.png` — ACT_5

**台本のビート:** The State's continued exclusive reliance on an ineffective means of service

**動く要素（i2v が動かす対象）:** the drum is turning with its surface smeared and one sheet is caught halfway out of the machine, bowed and not yet in the tray

- `G284.png`
A crank-driven duplicator of the period turning out sheets into a wire receiving tray, photographed from the side at forty centimetres under one hard work light, nobody in frame. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character on the delivered sheets. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the drum is turning with its surface smeared and one sheet is caught halfway out of the machine, bowed and not yet in the tray [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, photocopier, laser printer, modern office machine

**保存先:** `H:\pd-media\assets\ai\greene\G284.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, photocopier, laser printer, modern office machine` を足す。**正典側は1語も削らない。**

#### `G285.png` — ACT_5

**台本のビート:** the State has deprived them of property without the due process of law

**動く要素（i2v が動かす対象）:** the door is moving on its hinge and the shape of daylight it lays on the bare floor is sliding across the boards

- `G285.png`
An emptied apartment room with its front door standing wide open onto a bright walkway, photographed from deep inside at eight paces at chest height, the interior holding its detail and never going black. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the door is moving on its hinge and the shape of daylight it lays on the bare floor is sliding across the boards [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, furniture on a pavement, removal boxes, a family leaving, ransacked room

**保存先:** `H:\pd-media\assets\ai\greene\G285.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, furniture on a pavement, removal boxes, a family leaving, ransacked room` を足す。**正典側は1語も削らない。**

#### `G286.png` — ACT_5

**台本のビート:** we hold only that posted notice pursuant to section 454.030 is constitutionally inadequate

**動く要素（i2v が動かす対象）:** the beam is narrowing as the door drifts closed and its edge is travelling across the boards

- `G286.png`
One narrow beam of daylight through a partly closed door falling on a single small patch of bare floorboard, photographed at floor level at one metre with the rest of the room dark but holding detail. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the beam is narrowing as the door drifts closed and its edge is travelling across the boards [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, light beam special effect, god rays, smoke machine, horror lighting

**保存先:** `H:\pd-media\assets\ai\greene\G286.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, light beam special effect, god rays, smoke machine, horror lighting` を足す。**正典側は1語も削らない。**

#### `G287.png` — ACT_5

**台本のビート:** It is not our responsibility to prescribe the form of service that the Commonwealth should adopt.

**動く要素（i2v が動かす対象）:** one loose sheet standing on edge in a hole halfway down the rack is buckling and about to fall out of it

- `G287.png`
A wooden pigeonhole rack with every hole bare, photographed at a steep angle from one side at a metre so the holes run away to a point, cold flat light from a window out of frame. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: one loose sheet standing on edge in a hole halfway down the rack is buckling and about to fall out of it [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, hotel key rack, room numbers, pigeon holes with labels

**保存先:** `H:\pd-media\assets\ai\greene\G287.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, hotel key rack, room numbers, pigeon holes with labels` を足す。**正典側は1語も削らない。**

#### `G288.png` — ACT_5

**台本のビート:** even conceding that process served by mail is far from the ideal means

**動く要素（i2v が動かす対象）:** rain rings are spreading across the puddle and the envelope's free corner is lifting and floating on the moving water

- `G288.png`
A plain envelope lying in a puddle on a concrete walkway with its edge already swollen and dark, photographed at ten centimetres at puddle level in flat rain light. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: rain rings are spreading across the puddle and the envelope's free corner is lifting and floating on the moving water [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, flood, storm drama, dramatic reflection of a skyline

**保存先:** `H:\pd-media\assets\ai\greene\G288.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, flood, storm drama, dramatic reflection of a skyline` を足す。**正典側は1語も削らない。**

#### `G289.png` — ACT_5

**台本のビート:** posted service accompanied by mail service is constitutionally preferable to posted service alone

**動く要素（i2v が動かす対象）:** both papers are moving in the same gust and out of phase with each other, the sheet's corner up and the envelope's free end down

- `G289.png`
A sheet taped to a painted apartment door with a plain envelope wedged behind the door handle of the same door, photographed dead on at one metre in flat overcast light. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character on the taped sheet. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: both papers are moving in the same gust and out of phase with each other, the sheet's corner up and the envelope's free end down [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note

**保存先:** `H:\pd-media\assets\ai\greene\G289.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note` を足す。**正典側は1語も削らない。**

#### `G290.png` — ACT_5

**台本のビート:** ⟨HELD⟩

**動く要素（i2v が動かす対象）:** the scrap lies still except for one corner that is ticking up and down, and a loose downpipe bracket further along is swinging

- `G290.png`
An open-air walkway empty from end to end at the flattest hour of the day, photographed from one end at knee height so the balustrade and the run of doors both go away to a point, one single scrap of pale paper on the concrete halfway down. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the scrap lies still except for one corner that is ticking up and down, and a loose downpipe bracket further along is swinging [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, motel corridor, modern apartment block, glass balustrade

**保存先:** `H:\pd-media\assets\ai\greene\G290.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, motel corridor, modern apartment block, glass balustrade` を足す。**正典側は1語も削らない。**

#### `G291.png` — ACT_5

**台本のビート:** Affirmed does not mean three tenants walked out holding a key.

**動く要素（i2v が動かす対象）:** the key's steel ring is still spinning flat on the formica beside it, and the shadow of a moving curtain is crossing the table

- `G291.png`
A single door key lying alone on a bare formica table top, photographed at twenty centimetres at table level with one window out of frame to the left. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the key's steel ring is still spinning flat on the formica beside it, and the shadow of a moving curtain is crossing the table [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, bunch of keys, key fob with a logo, estate agent key tag, new brass key

**保存先:** `H:\pd-media\assets\ai\greene\G291.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, bunch of keys, key fob with a logo, estate agent key tag, new brass key` を足す。**正典側は1語も削らない。**

#### `G292.png` — ACT_5

**台本のビート:** It simply stops.

**動く要素（i2v が動かす対象）:** grit and one pale scrap of paper are blowing along the walkway and piling up against the foot of the brick

- `G292.png`
An open walkway that ends at a blank brick wall, photographed from six paces at chest height so the wall closes the frame, flat grey light and nobody in it. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: grit and one pale scrap of paper are blowing along the walkway and piling up against the foot of the brick [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, dead end alley, graffiti, urban decay cliché

**保存先:** `H:\pd-media\assets\ai\greene\G292.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, dead end alley, graffiti, urban decay cliché` を足す。**正典側は1語も削らない。**

#### `G293.png` — ACT_5

**台本のビート:** Three Justices did not agree, and the dissent is not a footnote.

**動く要素（i2v が動かす対象）:** the nearest of the three chairs is still rocking on its back legs and a curtain at the window is travelling across the light

- `G293.png`
Three plain wooden chairs pushed back from one side of a long bare table, photographed from the far end of the table at table height at three metres, one window light falling across the wood. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the nearest of the three chairs is still rocking on its back legs and a curtain at the window is travelling across the light [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, jury box, courtroom, boardroom, conference room, dining room

**保存先:** `H:\pd-media\assets\ai\greene\G293.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, jury box, courtroom, boardroom, conference room, dining room` を足す。**正典側は1語も削らない。**

#### `G294.png` — ACT_5

**台本のビート:** the Court holds that the Constitution prefers the use of the Postal Service to posted notice

**動く要素（i2v が動かす対象）:** the envelope is mid-push under the grille and the grille's loose chain is swinging against the bars

- `G294.png`
A post office counter grille seen from the public side with a plain envelope halfway under it, photographed at counter height at half a metre, the space behind the grille dim but holding its detail. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the envelope is mid-push under the grille and the grille's loose chain is swinging against the bars [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, bank teller, security glass, queue barrier, opening hours notice

**保存先:** `H:\pd-media\assets\ai\greene\G294.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, bank teller, security glass, queue barrier, opening hours notice` を足す。**正典側は1語も削らない。**

#### `G295.png` — ACT_5

**台本のビート:** despite the total absence of any evidence in the record regarding the speed and reliability of the mails

**動く要素（i2v が動かす対象）:** dust is turning in the shaft of light and the free corner of the blotter is lifting off the desk

- `G295.png`
An empty wire in-tray on a bare desk with nothing whatever in it, photographed at desk height at thirty centimetres with one shaft of window light lying across the tray and the blotter beneath it, and that blotter is bare of any marking. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: dust is turning in the shaft of light and the free corner of the blotter is lifting off the desk [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, office clutter, modern desk accessories, computer, telephone with buttons

**保存先:** `H:\pd-media\assets\ai\greene\G295.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, office clutter, modern desk accessories, computer, telephone with buttons` を足す。**正典側は1語も削らない。**

#### `G296.png` — ACT_5

**台本のビート:** The sole ground for the Court's result is the scant and conflicting testimony of a handful of process servers in Kentucky.

**動く要素（i2v が動かす対象）:** two of the pages are lifting at once in a draught, out of phase with each other, and one has already slid over the edge of the table

- `G296.png`
Five or six loose pages laid out side by side on a plain table so that how few of them there are is the subject of the picture, photographed at a low table-level angle at half a metre with the empty wood running away past them. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: two of the pages are lifting at once in a draught, out of phase with each other, and one has already slid over the edge of the table [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, stack of files, mountain of paperwork, archive shelves

**保存先:** `H:\pd-media\assets\ai\greene\G296.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, stack of files, mountain of paperwork, archive shelves` を足す。**正典側は1語も削らない。**

#### `G297.png` — ACT_5

**台本のビート:** the Court confidently overturns the work of the Kentucky Legislature, and, by implication, that of at least 10 other States

**動く要素（i2v が動かす対象）:** one door far down the line is mid-swing and is the only thing in the frame that is not still

- `G297.png`
A long corridor of identical closed public-building doors, photographed at a steep raking angle from chest height so the doors compress into a single receding band, flat institutional daylight and nobody in it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: one door far down the line is mid-swing and is the only thing in the frame that is not still [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, hotel corridor, hospital ward, prison landing, cell doors, office suite

**保存先:** `H:\pd-media\assets\ai\greene\G297.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, hotel corridor, hospital ward, prison landing, cell doors, office suite` を足す。**正典側は1語も削らない。**

#### `G298.png` — ACT_5

**台本のビート:** does not cite a single case, other than the decision below

**動く要素（i2v が動かす対象）:** dust is lifting along the shelf toward the camera and the book's front cover is standing up and dropping back in the draught

- `G298.png`
A long empty shelf with one single book lying flat and alone at its far end, photographed along the shelf at shelf height at forty centimetres so the emptiness runs at the camera, raking light. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: dust is lifting along the shelf toward the camera and the book's front cover is standing up and dropping back in the draught [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, library, bookshop, gilt spines, book titles

**保存先:** `H:\pd-media\assets\ai\greene\G298.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, library, bookshop, gilt spines, book titles` を足す。**正典側は1語も削らない。**

#### `G299.png` — ACT_5

**台本のビート:** at least 11 States authorizing notice in summary eviction proceedings solely by posting

**動く要素（i2v が動かす対象）:** steam is rising from every one of them and drifting the same way across the table

- `G299.png`
Eleven identical plain enamel cups set out along a long bare table in an empty room, photographed from one end at table height at two metres so they run away in a line, cold daylight from a high window. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: steam is rising from every one of them and drifting the same way across the table [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, café, restaurant, tea party, branded mugs, coffee shop

**保存先:** `H:\pd-media\assets\ai\greene\G299.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, café, restaurant, tea party, branded mugs, coffee shop` を足す。**正典側は1語も削らない。**

#### `G300.png` — ACT_5

**台本のビート:** Both opinions read the same three clauses. One read the words. The other read the depositions.

**動く要素（i2v が動かす対象）:** both pages are bowing and rattling in the draught from the open sash, and they are bowing out of time with each other

- `G300.png`
Two separate pages held side by side flat against the same window pane, one open hand pressed flat on each of them, photographed from forty centimetres from inside the room so both are back-lit and the daylight comes through them. THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE AND SEPARATE with a line of shadow between each pair and one nail showing on each, and the thumb clearly apart from the fingers along the near side -- here the surface is the glass with the page against it. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character on both pages. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: both pages are bowing and rattling in the draught from the open sash, and they are bowing out of time with each other [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand

**保存先:** `H:\pd-media\assets\ai\greene\G300.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand` を足す。**正典側は1語も削らない。**

#### `G301.png` — ACT_5

**台本のビート:** we decline to resolve the constitutional question based upon the determination whether the particular action is more properly characterized as one in rem or in personam

**動く要素（i2v が動かす対象）:** a loose sheet of paper is caught on the rim of the nearer crate and is flapping hard, half in and half out of it

- `G301.png`
Two empty wooden crates set side by side on a bare floor, both open and both empty, photographed from above and to one side at two paces at chest height in flat light. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: a loose sheet of paper is caught on the rim of the nearer crate and is flapping hard, half in and half out of it [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, removal boxes, packing up a home, shipping containers

**保存先:** `H:\pd-media\assets\ai\greene\G301.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, removal boxes, packing up a home, shipping containers` を足す。**正典側は1語も削らない。**

#### `G302.png` — ACT_5

**台本のビート:** What the paper did was the question.

**動く要素（i2v が動かす対象）:** water is creeping visibly across the sheet and one corner has lifted clear of the wet and is curling up

- `G302.png`
A sheet lying on wet concrete, soaked right through so the light comes up through it and the grain of the concrete shows behind, photographed at fifteen centimetres at ground level. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character, softened and running where the water has taken it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: water is creeping visibly across the sheet and one corner has lifted clear of the wet and is curling up [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, ink running into legible words, watermark, blood

**保存先:** `H:\pd-media\assets\ai\greene\G302.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, ink running into legible words, watermark, blood` を足す。**正典側は1語も削らない。**

#### `G303.png` — ACT_5

**台本のビート:** The Court gives lipservice to the principle ... but then goes on to do just that.

**動く要素（i2v が動かす対象）:** the door is pressing and easing against the wedge in the wind and the wedge's loose outer leaves are fanning open

- `G303.png`
A door held open by a wedge of folded paper jammed under its leading edge, photographed at ten centimetres at floor level so the wedge fills the lower frame. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the door is pressing and easing against the wedge in the wind and the wedge's loose outer leaves are fanning open [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, rubber door stop, modern fire door, push bar

**保存先:** `H:\pd-media\assets\ai\greene\G303.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, rubber door stop, modern fire door, push bar` を足す。**正典側は1語も削らない。**

#### `G304.png` — ACT_5

**台本のビート:** we have long since discarded the concept that due process authorizes courts to hold laws unconstitutional when they believe the legislature has acted unwisely

**動く要素（i2v が動かす対象）:** one pale scrap of paper is travelling down the flight and is caught mid-bounce between two treads

- `G304.png`
A flight of worn public steps seen from the side, the treads dished in the middle by years of use, photographed at step height at one metre in flat grey light. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: one pale scrap of paper is travelling down the flight and is caught mid-bounce between two treads [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, grand staircase, marble, red carpet, courthouse steps with columns

**保存先:** `H:\pd-media\assets\ai\greene\G304.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, grand staircase, marble, red carpet, courthouse steps with columns` を足す。**正典側は1語も削らない。**

#### `G305.png` — ACT_5

**台本のビート:** It is no secret, after all, that unattended mailboxes are subject to plunder by thieves.

**動く要素（i2v が動かす対象）:** the hanging door is swinging on its one hinge and the caught paper is flicking with it

- `G305.png`
A letter box whose small door hangs by one hinge with torn paper caught in the hinge, photographed from the side at fifteen centimetres at night, lit only by a single stair bulb above and to the left, the metal holding its detail and never going black. The paper is completely bare: an unbroken field of off-white with no print, no ruling, no letterform, no number and no mark of any kind anywhere on it. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the hanging door is swinging on its one hinge and the caught paper is flicking with it [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, burglary scene, crowbar, forensic tape, horror lighting

**保存先:** `H:\pd-media\assets\ai\greene\G305.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note, burglary scene, crowbar, forensic tape, horror lighting` を足す。**正典側は1語も削らない。**

#### `G306.png` — ACT_5

**台本のビート:** posting notice at least gives assurance that the notice has gotten as far as the tenant's door

**動く要素（i2v が動かす対象）:** the whole free edge of the sheet is standing right off the door in the wind and its shadow is sweeping across the paint

- `G306.png`
A sheet taped to a painted door seen at a very shallow angle from the side so the door runs away out of the frame and the sheet stands out from the plane of the paint, photographed at thirty centimetres. The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes and no gaps between words anywhere along it, so it is recognisable as a printed page purely by its rhythm of grey and white and carries not one readable character. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the whole free edge of the sheet is standing right off the door in the wind and its shadow is sweeping across the paint [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note

**保存先:** `H:\pd-media\assets\ai\greene\G306.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, readable document, printed words on paper, letterforms, typed lines, printed paragraph, letterhead, form fields, rubber stamp with words, handwritten note` を足す。**正典側は1語も削らない。**

#### `G307.png` — ACT_5

**台本のビート:** The dissent misconstrues the constitutional standard.

**動く要素（i2v が動かす対象）:** the string is vibrating and the shadow line has smeared into a band

- `G307.png`
The single line of shadow cast by a taut string across a bare plaster wall, photographed square on at one metre in hard side light with nothing else in the frame. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the string is vibrating and the shadow line has smeared into a band [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, laser line, minimal art installation, gallery wall

**保存先:** `H:\pd-media\assets\ai\greene\G307.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, laser line, minimal art installation, gallery wall` を足す。**正典側は1語も削らない。**

#### `G308.png` — ACT_5

**台本のビート:** a summary proceeding for quickly determining whether or not a landlord has the right to immediate possession

**動く要素（i2v が動かす対象）:** rain is blowing across the open side of the stairwell in visible bands and water is running down the rail past the hand

- `G308.png`
An outdoor concrete stairwell seen from the landing above with the treads running away below, one flat hand on the steel handrail at the very edge of the frame and no other part of the person in the picture, photographed at one metre in flat wet daylight. THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE AND SEPARATE with a line of shadow between each pair and one nail showing on each, and the thumb clearly apart from the fingers along the near side -- here the surface is the handrail. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: rain is blowing across the open side of the stairwell in visible bands and water is running down the rail past the hand [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, prison landing, fire escape drama, vertigo shot, drone view

**保存先:** `H:\pd-media\assets\ai\greene\G308.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, hand held up in the air, blurred hand, prison landing, fire escape drama, vertigo shot, drone view` を足す。**正典側は1語も削らない。**

#### `G309.png` — ACT_5

**台本のビート:** Many expenses of the landlord continue to accrue whether a tenant pays his rent or not.

**動く要素（i2v が動かす対象）:** one drop is caught mid-fall below the spout and the ring it made a moment ago is still spreading in the standing water on the grate

- `G309.png`
A dripping outdoor tap over an iron drain grate set into a brick wall, photographed at twenty centimetres in cold flat light. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: one drop is caught mid-fall below the spout and the ring it made a moment ago is still spreading in the standing water on the grate [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, modern mixer tap, chrome fitting, kitchen sink, water feature

**保存先:** `H:\pd-media\assets\ai\greene\G309.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, modern mixer tap, chrome fitting, kitchen sink, water feature` を足す。**正典側は1語も削らない。**

#### `G310.png` — ACT_5

**台本のビート:** The means chosen for making service of process ... must be prompt and certain

**動く要素（i2v が動かす対象）:** the closer's arm is mid-travel and folding, and the leading edge of the door below it has smeared

- `G310.png`
A spring door closer at the top of a plain public door with the door itself mid-close, photographed from below at forty centimetres so the closer's arm and the top of the door fill the frame. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: the closer's arm is mid-travel and folding, and the leading edge of the door below it has smeared [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, modern aluminium door, push bar, fire exit sign, automatic door

**保存先:** `H:\pd-media\assets\ai\greene\G310.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, modern aluminium door, push bar, fire exit sign, automatic door` を足す。**正典側は1語も削らない。**

#### `G311.png` — ACT_5

**台本のビート:** it is difficult to see how a means of serving process that fails to afford actual notice ... can be deemed either prompt or certain

**動く要素（i2v が動かす対象）:** a shadow is crossing the bar of daylight under the door and passing on, and the net curtain at the side window is moving

- `G311.png`
The inside of a front door seen from a chair in a dim room, the bar of daylight under the door the brightest thing in the frame, photographed from seat height at four paces with the room dark but holding all its detail. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: a shadow is crossing the bar of daylight under the door and passing on, and the net curtain at the side window is moving [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, horror scene, silhouette of an intruder, thriller lighting, black crushed shadows

**保存先:** `H:\pd-media\assets\ai\greene\G311.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, horror scene, silhouette of an intruder, thriller lighting, black crushed shadows` を足す。**正典側は1語も削らない。**

#### `G312.png` — ACT_5

**台本のビート:** That is where the two opinions stop talking to each other.

**動く要素（i2v が動かす対象）:** both doors are breathing against their latches in the same draught and one is a finger's width further open than the other

- `G312.png`
Two painted doors facing each other across a narrow landing, both shut, photographed from the middle of the landing at chest height in flat light from a stair window. Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and 1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere in the picture. MOVING ELEMENT, already mid-movement when the shutter opens: both doors are breathing against their latches in the same draught and one is a finger's width further open than the other [STYLE] Avoid: [NEG], modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, hotel corridor, symmetrical art photograph, hall of mirrors

**保存先:** `H:\pd-media\assets\ai\greene\G312.png`（**新規。既存を上書きしない**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, modern car, modern van, modern smartphone, computer screen, television screen, trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, non-Latin script, LED lighting, composite decking, modern kitchen, furniture on a pavement, people being evicted, a removal van being loaded, crying, a hand on a shoulder, a uniformed officer at a door, a landlord character, a completely static arrangement with nothing caught mid-movement, everything locked and settled, studio-locked still life, hotel corridor, symmetrical art photograph, hall of mirrors` を足す。**正典側は1語も削らない。**

---

## 9. 発注書の検査

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP62_greene_CODEX_BATCH_B.v001.md
```

顔／実在人物・読める文字・手書き・紋章／記章・数字の**五族すべて**が `[NEG]` に入っていることを機械が確認します。

この発注書とペーストファイルは**1つの Python データソース**から生成されており、本文がずれることは構造上ありえません:

```
py -3.11 scripts/build_ep62_greene_image_order.py --verify
```

## 10. 生成後にやること（発注者側）

1. **70枚を1枚ずつ native（3840x2160のまま）で目視。** 縮小コンタクトシートでは紙の上の文字も車のバッジも**見えません**（EP66 で 372px では見えず4倍で初めて出た）。
   - 紙が写る全プレート: 紙面を**8倍以上**に拡大し、**文字の形が1つも無い**ことを確かめる。
   - 人物が写る3枚（`G271` `G272` `G280`）: 実在の誰かに似ていないこと、手の指が数えられることを確かめる。
   - 全枚: **1975–1982年に無い物**が1つも無いこと（車・電話・画面・スニーカー・プラスチック建材）。
2. **i2v に回す。** `EP62_greene_I2V_RESUME.v001.md` §3 のコマンド。**`--length 121` を守る**（81フレームだと 4.6秒カットの中で `<Loop>` が巻き戻る）。
   - `G271` `G272` `G280` は**顔が写るプレート**です。i2v の人物レジーム `N2` は `face turning toward camera, visible facial features, recognisable face` をネガティブに持っており、**顔が既に写っている元絵と喧嘩します**。この3枚だけは その3語を外し、`face changing identity, features morphing, second face` に置き換えて回してください。
   - `I2V_RESUME` §6 の鉄則をそのまま守ること: **i2v プロンプトに「動く物」を名詞で書かない**。動く物はこの発注書の**元絵の側**に入れてあります。
3. **i2v 後**に `build_asset_manifest_motionfirst.py --slug greene` → `build_case_film_generic.py` → `check_spec_satisfied.py --slug greene`。**distinct_video が 234 以上になっていることを数字で確認してからレンダーする。**
4. `mandatory_stills` について: この70枚は **`mandatory_stills` に足さないでください。**足すと「宣言した静止画がカットに無い」で落ちる可能性が増えるだけで、`distinct_video_assets` の充足には一切関係ありません（§11）。

## 11. この発注を書いていて見つけた、仕様側の2点（変更していない・報告のみ）

1. **`target_cut_sec` が未宣言。** greene の `episode_spec.v001.json` にこのキーは**存在しません**（`null` ですらなく不在）。`build_case_film_generic.py` は宣言が無いとビルダー定数 4.6 を使います。CLAUDE.md §4.6 は**「宣言されていない値はエラーであって、推定される既定値ではない」**と定めており、これはその規定に反した既定値フォールバックです。EP65 marmet は `3.7` を宣言しており、62/63/64 だけが未宣言です。
2. **`distinct_video_assets: 234` に導出が無い。** EP62–65 の4本が**同じ 234** を宣言し、`notes` にその数の出どころが書かれていません（写した数に見えます）。`schemas/episode_spec.v001.json` の定義は **「footage cuts として計算せよ。cuts ÷ reuse cap ではない」**であり、greene の実測 `total_sec = 1841.006` からその定義どおり導くと **`ceil(round(1841.006 / 4.6) * 0.68) = ceil(400 * 0.68) = 272`** です。**234 は導出値より 38 低い。** ただし memphis が 234 を満たしているので「明らかに誤り」とは言えず、**本発注では変更していません**。変えるなら4本まとめて、`target_cut_sec` の宣言と同時にやるべきです。
3. **`mandatory_stills` が 224 なのにフィルムの静止画は 117。これは問題ではありません。**`check_spec_satisfied.py` は **拡張子ではなく stem で照合**します（`G045.png` は `G045.mp4` でも満たされる）。実測すると 224件の内訳は**PNGカットとして 102 ・MP4（i2v化）カットとして 122 ・どちらにも無い 0**。**224件すべてが画面に出ており**、だからゲートは何も言いません。「117 しか無い」は静止画のまま出ている枚数であって、欠落ではありません。

