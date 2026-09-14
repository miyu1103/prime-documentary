# EP66 openfields — Codex 画像生成 **バッチD 再発注** v001（**4枚**・1プロンプト1枚）

> ## ★★★ この4枚は、**同じ ID の既存ファイルを上書きします。** ★★★
> 保存先も名前もバッチB／Cと同一（`H:\pd-media\assets\ai\openfields\L###.png`）。
> **新しい ID を作らないでください。** `_v2` も `_02` も `_D` も作らないでください。
> 上書きされた時点で、`mandatory_stills` / `people_plates` の宣言はそのまま有効です。
>
> ## ★★★ バッチA（`L001`–`L069`）は引き続き**廃棄**です。 ★★★
> 棚には残っていますが、`mandatory_stills` に入れず、生成もせず、ID も再利用しません。

**由来:** `runs/qc/openfields_plate_verdicts_batchC.v001.md`（バッチC 21枚の目視QC・**15 ACCEPT / 3 FLAG / 3 REJECT**）。この発注書はその REJECT 3枚と、QCが範囲外で見つけた `L096` の**計4枚だけ**を作り直します。
**バッチCの他の17枚には触りません。**

> ### ★`L173` は作り直しません★
> QC判定は **FLAG**（グリルもボンネットも12倍で無地・修正は着地済み）。唯一の指摘は `L096` との**車の向きの不一致**でした。**その不一致は `L096` 側を `L173` に合わせることで解消します**（§5 `L096` 参照）。合格しているプレートを再生成すると、直ったばかりのグリルの楕円が戻るリスクの方が高い。
>
> ### ★`L259` / `L099` も作り直しません★
> `L259` は 261 clear rows で 150px の見出しが 87px の余裕付きで載る（合格済みの `L258` は 274 行目で切れる）。`L099` はカードが上1/3を丸ごと必要とする場合のオーナー判断事項で、QCは「上約17%は平ら」と実測しています。**どちらも今回の対象外。**

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**「良いのが出るまで回す」を禁止する。
3. **既存の同名ファイルを上書きする。**別名で出すと、どちらが正典か分からなくなります。

## 1. ★絶対条件（バッチB §1・バッチC §1 と同一。緩和はありません）

正典は `episodes/PD-2026-066-openfields/episode_spec.v001.json` の `forbidden_subjects` です。
**`face` / `portrait` / `headshot` は禁止語ではありません**（オーナー決定 2026-07-04・`people_plates` は `L235`–`L254`）。以下は再掲です。

- **人物は入れる。顔も描く。禁じられているのは「実在する特定の人物に似ていること」だけ。**
  完全に架空の一般人であること。有名人・公人・実在の誰かに似せない。カメラ目線の作り笑い・広告のモデル顔にしない。**働いている人の、作っていない顔。**
- **読める文字・数字・手書き・印章・記章・ロゴを描かない。**
  **車体のバッジ・文字マーク・ネームプレート・グリルの楕円・ナンバープレートもここに含まれます**（`L146` / `L173` / `L096` はこれで落ちました）。
- **制服・記章・パトカー・手錠・銃・仕留められた動物・血を描かない。** 職員は一人も登場しません。
- **監視スリラーの意匠を作らない。** トレイルカメラは**幹にベルトで留めた小さくて安っぽい艶消しオリーブの樹脂の箱**です。
- **実在と特定できる土地・建物を描かない。法廷を描かない。広告調にしない。黒つぶれさせない。**
- **手は指が数えられること。** 融合した指・6本指・親指の欠落は不可。

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]` も `[NEG]` もバッチC と1バイト違いません。**バッチCの本文から機械的に読み出してこの発注書に書き込んでいます（§6に照合結果）。**この2ブロックを1語も変えずに展開してください。**

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, muted natural colour, flat overcast daylight of a late Appalachian autumn, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing, rural Pennsylvania and Middle Tennessee between 2019 and 2026, ordinary working farmland and unmanaged second-growth woodland, worn unglamorous surfaces, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> text, lettering, numerals, digits, house numbers, handwriting, cursive writing, legible signature, seals, emblems, logos, insignia, badge, name plates, readable words on a sign, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, police officer, sheriff, trooper, uniform, patrol car, flashing lights, handcuffs, rifle, shotgun, firearm, holster, dead animal, carcass, blood, taxidermy, mounted antlers, courtroom interior, gavel, judge's bench, prison bars, razor wire, scales of justice, hourglass, a handshake, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, aerial view from above the treetops, golden hour, sunset glow, postcard scenery, autumn colour explosion, Christmas, tropical, modern smartphones, laptops, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

> ### ★プレートごとの `[NEG]` 追記について★
> 4枚すべてが `Avoid: [NEG], …` と、`[NEG]` の後ろに読点で語を続けています。
> **これは上の正典 `[NEG]` を展開したうえで、その末尾にさらに続ける、という意味です。**
> **正典 `[NEG]` の語を1語も削らないでください。**追記だけが増えます。
>
> ### ★`[NEG]` は「人」を禁じていません★
> 禁じているのは **`recognisable person, identifiable person, likeness of a real individual,`**
> **`portrait of a named person, celebrity, public figure, deepfake`** ——**実在の誰かに似ること**だけです。
> バッチAの `[NEG]` は `human face, facial features, eyes …` と書いて**人が写ること自体**を止めており、
> **191枚を作り直す羽目になった原因がそれです。元に戻さないでください。**

## 3. 命名と保存先

- ファイル名は**元と同じ**（`L170.png` など）。**連番を新規に振らない。**
- 保存先 `H:\pd-media\assets\ai\openfields\`。**同名で上書き。**
- 長辺 3840px 以上・16:9・PNG。

## 4. 対象一覧（4枚）

| # | ID | 区分 | 前回QC | 何回目 | 作り直す理由（1行） |
|---:|---|---|---|---|---|
| 1 | `L170` | ACT_5 / 回収対A | REJECT | **3回目** | まだ丸柱。`L075` の角材と合わない。形状名（`SQUARED` / `round pole post`）は2回とも効かなかったので、名前をやめて**輪郭・平らな天面・稜で段差になる二面の陰影**で書き、`[NEG]` は丸柱の**視覚的特徴**を禁じる。 |
| 2 | `L146` | ACT_4 | REJECT | **3回目** | テールゲート右下に 53x12 px のバッジが再発。禁止語は2回効かなかった。**距離（画面幅の1/10以下）を主たる指示にし**、3/4後方の角度を保ってテールゲートを短縮させる。 |
| 3 | `L236` | PEOPLE | REJECT | **3回目** | 上げた手の指がまだ融合（親指なし）。加えて発注が RIGHT HAND を指定していたが**柵は彼女の左**で、指定は成立しない。**手を上げるのをやめ**、`L247` で通った「平らな面に置いた手」の幾何に置き換える。 |
| 4 | `L096` | ACT_1 | （範囲外で発見） | **初回** | **未発注。このままだと出荷される。** 14倍で後部バンパーに白いナンバープレート＋暗い文字グリフ5〜6個。`L173` に合わせて**正面向き**にし、プレートの載る面ごとフレームから外す。 |

> ### ★回収対は「似た絵」ではなく「同じ絵」を要求します★
> `L170` の本文は **`L075` の実画像を 3840x2160 のまま開いて書き起こしました。**
> `L096` の本文は **`L173` の実納品画を開いて、その向き・レーン・光に合わせて書きました。**
> **生成前に相手の1枚を横に置いてください。**カメラ高・画角・被写体の位置が違えば回収が成立しません。

## 5. プロンプト（各1枚）

### `L170.png` — ACT_5 / 回収対A・第3回目

**作り直す理由:** PAIR A STILL BROKEN（2回連続）: 納品はいまだ**丸柱**。`L075` は角材で、平らな挽き口の天面・全高を走る硬い縦稜・稜で段差になる二面の陰影を持つ。`SQUARED` の大文字と `[NEG]` の `round pole post` は**2回とも効かなかった**ので、**形状名で呼ぶのをやめ**、輪郭・天面・二面の陰影という「見え方」だけで書き、`[NEG]` は丸柱の**名前ではなく視覚的な特徴**を禁じる。

**実画像で見たこと:** **`L075` と `L170` を自分で開いて（3840x2160 のまま拡大して）書き起こした。**`L075`: 天面が平らな四辺形の面として見え、遠い辺は右へわずかに下がる直線。柱の幅の約4/5がカメラ向きの広い面（苔と地衣で暗い緑と灰）、右端の約1/5が**より暗い**二枚目の面で、その境の縦稜で輝度が段差になる（native y=400 の行で 55 → 18 と1段で落ちる）。左右の輪郭は上下とも同じ幅の直線。`L170`: 天面が**楕円の弧**、輪郭が両側とも内側に曲がり、陰影が柱をぐるりと連続で回っていて、稜がどこにもない（同じ行を測っても段差が出ず 26〜67 の間をなめらかに揺れるだけ）。

- `L170.png`
A WOODEN GATE POST WHOSE WHOLE OUTLINE IS MADE OF STRAIGHT LINES: its left edge and its right edge are two straight vertical lines the same distance apart all the way from the top of the post down to the bottom of the frame, with no taper, no bulge and no curve in either of them, and the top of the post is closed off by a STRAIGHT HORIZONTAL EDGE. The camera sits below the top of the post, so THE FLAT SAWN TOP IS VISIBLE AS A FLAT PLANE: a four-sided figure with straight edges and sharp corners, its far edge a straight line running slightly downhill to the right, paler and greyer than the sides because rain stands on it. The post shows TWO FACES AT ONCE and they meet at ONE HARD VERTICAL EDGE that runs the full height of the post: the broad face turned to the camera fills about four fifths of the post's width and is mottled dark green and grey with moss and lichen, the narrow face beyond that edge fills the remaining fifth along the RIGHT and is markedly darker, and THE TONE DROPS IN ONE STEP AT THAT EDGE, light on one side of the line and dark on the other with no blend between them, so the edge reads as a line ruled down the post. Straight vertical saw grain runs down the broad face parallel to the two outer edges. This is the identical framing as the empty field at the head of the film: the post stands upright about a tenth of the frame width in from the LEFT EDGE with a narrow strip of field visible to the left of it, its top just below the top edge of the frame and its foot running out of the bottom edge, and on it now nothing but a loop of loose rusted wire hanging down its left face where a chain used to hang, the same flat low line of bare winter trees running level across the middle of the frame with one faint hazy low wooded ridge far behind them on the right almost lost in the haze, the same brown winter field of tufted dead grass running from the foot of the post to that tree line, the same even pale cool grey overcast sky filling the upper third, camera at the height a small box strapped to a trunk would sit [STYLE] Avoid: [NEG], curved top on the post, domed crown, rounded crown, elliptical top, curved silhouette, tapering post, cylindrical post, barrel-shaped post, shading wrapping continuously around the post, tone fading smoothly from the middle of the post out to both edges, post with no corner edge anywhere on it, smooth unbroken curved surface all round the post, round pole post, bare hillside filling the background, wooded slope rising close behind the field, post set in toward the middle of the frame, warm colour grade, mown pasture

**保存先:** `H:\pd-media\assets\ai\openfields\L170.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, curved top on the post, domed crown, rounded crown, elliptical top, curved silhouette, tapering post, cylindrical post, barrel-shaped post, shading wrapping continuously around the post, tone fading smoothly from the middle of the post out to both edges, post with no corner edge anywhere on it, smooth unbroken curved surface all round the post, round pole post, bare hillside filling the background, wooded slope rising close behind the field, post set in toward the middle of the frame, warm colour grade, mown pasture` を足す。**正典側は1語も削らない。**

### `L146.png` — ACT_4・第3回目

**作り直す理由:** BADGE STILL PRESENT: テールゲート右下に **53x12 native px** の暗いバッジが戻った（文字構造あり）。本文でも `[NEG]` でもバッジは既に禁じてあり、**禁止語は効いていない**。今回は**禁止ではなく距離を効かせる**。前回の納品はトラックが画面幅の約29%を占めており、発注の「a hundred yards away」は無視されていた。バッジが解像しない大きさを**数値と構図の両方で強制**する。

**実画像で見たこと:** **`L146` を native で開いてテールゲートを拡大した。** バッジはテールゲート右下、テールランプの内側。それ以外の面は無地の白で、中央上のくぼんだハンドルとその下の横プレスラインだけ。バンパーはクロームで無地、ナンバープレートは無い。トラックは画面幅 x≈645–1015/1280（約29%）を占め、3/4後方から見た角度。**距離を効かせる際に 3/4 の角度は保つ**——真後ろに回すとテールゲートが画面いっぱいに正対して、小さくしても面積が稼がれてしまう（`L096` がその実例）。

- `L146.png`
A plain unmarked pickup truck parked on the gravel shoulder of a public road at the edge of hardwood timber, empty and shut, with nobody near it and nobody in the frame. THE FRAME IS A WIDE VIEW OF THE ROAD AND NOT A VIEW OF THE TRUCK: the camera stands in the middle of the empty road at eye height, the full width of the carriageway with its painted centre line, both gravel shoulders and the timber standing over the road on both sides all fit inside the frame, the road runs away from the camera and bends out of sight, and THE TRUCK IS A SMALL PALE SHAPE FAR DOWN IT, no wider than a tenth of the frame width and no taller than a seventh of the frame height, far enough off that nothing smaller than a wing mirror can be made out on it. It is seen from behind and from slightly to one side, so the tailgate is turned away from the camera and foreshortened to a narrow sliver instead of facing the camera square on. At that size the tailgate is A SINGLE UNBROKEN SHEET OF WHITE PAINT running from one tail light to the other, the only shapes anywhere on it are the recessed handle at its centre and one horizontal press-line below that, and the lower right corner of the tailgate is bare white paint exactly like the rest of it. Empty wet road surface fills the whole foreground [STYLE] Avoid: [NEG], truck close to the camera, truck filling the frame, close view of the tailgate, badge on the tailgate, wordmark on the tailgate, chrome nameplate, manufacturer lettering, model name, raised letters on a panel, sticker, decal, licence plate, registration plate

**保存先:** `H:\pd-media\assets\ai\openfields\L146.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, truck close to the camera, truck filling the frame, close view of the tailgate, badge on the tailgate, wordmark on the tailgate, chrome nameplate, manufacturer lettering, model name, raised letters on a panel, sticker, decal, licence plate, registration plate` を足す。**正典側は1語も削らない。**

### `L236.png` — PEOPLE・第3回目

**作り直す理由:** 手の破綻 ＋ 発注の自己矛盾: 上げた手の指はいまだ融合（長い指1本＋鈍い突起2本、親指なし）。さらに前回の発注は RIGHT HAND を指定していたが、**柵は彼女の左側にある**ので、指定された手は針金に届く手ではありえなかった。**両方を直す。**

**実画像で見たこと:** **`L236` を native で開いて手を拡大した。** 手は宙に伸ばされ、有刺鉄線の上に浮いている。指は1本の長い指と2つの鈍い突起に融合し、親指が無い。柵は画面の右半分にあり、彼女は正面を向いているので、伸びているのは**彼女の左手**である。

### 構図の選択と理由（上げた手をやめた）

**選んだのは「上げた手」でも「フレーム外」でもなく、『すでに柵柱の平らな天面に置かれた手』である。**

1. **破綻の原因そのものを消せる。** 失敗しているのは「宙に浮いた、指を開いた手」という、この生成器が最も苦手な形。天面に伏せれば手は宙に浮かない。
2. **同じ発注内で成功した形をそのまま使い回せる。** `L247` は「上桟に平らに置いた手、甲を上に、指を向こう側へ」でACCEPTになり、QCは *4本の指がそれぞれ爪付きで分離* していることを native で確認している。**この生成器で通ったことのある幾何**を別プレートに移す方が、新しい文言を考えるより確実。
3. **左右の矛盾が自動的に消える。** 柱は柵側に立っているので、届く手は「柵に近い方の手」で決まる。**RIGHT / LEFT を一切書かない。**
4. **有刺鉄線を握らせない。** 納品画の最上段は有刺鉄線で、人は有刺鉄線を握らない。QCが挙げた「上の針金に置いた手」案はここで不自然になる。
5. **『自分の境界に触れる』というビートは残る。** フレーム外にすると絵の意味が消える。

副作用として、もう一方の手は**ポケットに入れる**（破綻しうる面をもう1つ減らす）。膝上のフレーミングにして手を前回より大きく写す。

- `L236.png`
An invented woman in her fifties in a quilted work jacket standing at her own fence line, framed from the knees up and seen from the front at about twelve feet at eye height, the wire fence running away from her through the RIGHT half of the frame and a stubble field beyond it. Beside her, on the fence side of her, stands a weathered wooden fence post cut off flat across the top at about the height of her hip. THE HAND NEAREST THE FENCE IS ALREADY AT REST ON THE FLAT TOP OF THAT POST, not raised and not held in the air: the palm is laid flat down on the sawn top, the wrist is straight, the FOUR FINGERS LIE SIDE BY SIDE AND SEPARATE along the wood pointing away from her with the last joint of each one hooked down over the far edge of the post, EACH FINGER SHOWING ITS OWN NAIL AND CASTING ITS OWN SHADOW ON THE WOOD, and the thumb is down the near side of the post clearly apart from the fingers. Her other hand is in her jacket pocket. The barbed top strand of the fence is stapled to the side of the post well below her hand and she is not touching it. Her face is lit evenly by flat cloud with no expression put on for the camera, and the hand on the post is large enough in the frame and sharp enough to be read clearly [STYLE] Avoid: [NEG], raised hand, hand held up in the air, fingers splayed in the air, mitten hand, fingers fused into one mass, fingers merged, webbed fingers, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, blurred hand, hand out of focus, hand gripping barbed wire, fist

**保存先:** `H:\pd-media\assets\ai\openfields\L236.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, raised hand, hand held up in the air, fingers splayed in the air, mitten hand, fingers fused into one mass, fingers merged, webbed fingers, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, blurred hand, hand out of focus, hand gripping barbed wire, fist` を足す。**正典側は1語も削らない。**

### `L096.png` — ACT_1・**今回が初回の発注**

**作り直す理由:** LICENCE PLATE: **これは前回まで一度も作り直していない、既に合格扱いのプレートである。このまま出荷される。** 14倍で見ると後部バンパーに**白いナンバープレートがあり、暗い文字グリフが5〜6個**並び、その上下に細かい模様の帯がある。特定の文字としては読めないが、文字を載せたプレートであることは間違いない——`L146` と `L173` を落としたのと同じ欠陥クラスであり、`[NEG]` の `numerals, digits, name plates` に触れる。

**実画像で見たこと:** **`L096` と `L173` を並べて開いた。** `L096` はトラックを**真後ろから**見ており（テールゲートがカメラに正対、両フロントドアが開、後部バンパーに白いプレート）、`L173` は**正面から**見ている（グリルがカメラ向き、両フロントドアが開、12倍でグリルもボンネットも無地）。**車が回転してしまっており、回収が「同じ画の後の瞬間」ではなく「別の場面」に読める。**

### 向きをどちらに揃えたか、と理由

> ### ★`L096` と `L173` は**車の向きが一致していなければならない**★
> 2枚は設計上の回収対である。片方が前・片方が後ろだと、同じレーンの同じ車の
> 別の瞬間ではなく、別の場面に見える。**この発注は `L096` を `L173` の向き
> （正面）に合わせる。`L173` は作り直さない。**

**`L096` を正面向きにする。** 理由:

1. **プレートが載る面そのものがフレームから消える。** 禁止語を足すのではなく、後部バンパーを画面から外す**構図の変更**で消す。`L146` の教訓は「禁止語は効かない」。
2. **`L173` は既に正面で納品され、12倍でグリルもボンネットも無地だった。** 合格したプレートを作り直す方がリスクが高い（グリルの楕円が戻る）。
3. **前面にプレートが無いのは物理的に正しい。** 舞台のペンシルベニアもテネシーも**後部のみ**の交付州で、前面プレートは存在しない方が自然。生成器の prior と戦わない。

**この1枚では距離を効かせない。** `L096` の納品はすでにトラックが画面幅の**約10%**（3840換算で約390px）しかないのに、そこにグリフ付きのプレートが出た。**つまり「画面幅の1/10」は、真後ろ正対の構図では単独では足りない。** `L146` で距離が効くのは、あちらが 3/4 後方の角度でテールゲートが短縮されるからである（だから `L146` では角度を保つよう本文に書いた）。

**副作用（オーナー判断が要るなら記載）:** バッチB の原文は *"both cab doors and the tailgate left open"* だった。**正面からだとテールゲートは写らないので、この指定は落とした。** 本文に「テールゲートは倒してあるが横から線として見える」と書くことも検討したが、同じ本文で「後部は一切フレームに入れない」と書いた直後に矛盾する指示になる（`L236` の RIGHT HAND と同じ自己矛盾の型）ので**書かない**。「捜索された車」であることは**開け放たれた両ドア**だけで担う。

- `L096.png`
A dark modern crew-cab pickup standing in a mown green grass field lane, SEEN HEAD-ON FROM IN FRONT OF IT so that the grille, the windscreen and both headlights face the camera and NO PART OF THE BACK OF THE VEHICLE IS ANYWHERE IN THE FRAME: no tailgate, no rear bumper and no tail light can be seen from this angle. BOTH CAB DOORS STAND WIDE OPEN, one on each side, as though the cab has just been gone through, and the bed behind them is empty. Nobody is in it and nobody is near it. It sits small in the frame, no wider than a tenth of the frame width, with the mown lane running away from the camera to it, a brown worked field on the left of the lane, a line of bare trees and rough grass on the right, low wooded hills faint in the far distance and a pale grey overcast sky, at eye height in flat light. The front of the vehicle is bare: the grille is a plain dark mesh panel WITH NOTHING MOUNTED AT ITS CENTRE, the bonnet above it is one unbroken sheet of dark paint, and the front bumper below it is a single plain bar with nothing fixed to it and nothing hanging from it, no oval, no emblem, no badge, no wordmark, no nameplate and no plate of any kind on any part of the vehicle [STYLE] Avoid: [NEG], rear of the vehicle, back of the truck, tailgate facing the camera, rear bumper, tail lights, licence plate, registration plate, number plate, plate mounted on a bumper, oval badge on the grille, manufacturer emblem, chrome nameplate, raised letters on a panel, sticker, decal, truck close to the camera, truck filling the frame, white truck, light-coloured truck, small old pickup, 1990s pickup

**保存先:** `H:\pd-media\assets\ai\openfields\L096.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, rear of the vehicle, back of the truck, tailgate facing the camera, rear bumper, tail lights, licence plate, registration plate, number plate, plate mounted on a bumper, oval badge on the grille, manufacturer emblem, chrome nameplate, raised letters on a panel, sticker, decal, truck close to the camera, truck filling the frame, white truck, light-coloured truck, small old pickup, 1990s pickup` を足す。**正典側は1語も削らない。**

---

## 6. 発注書の検査

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP66_openfields_CODEX_BATCH_D.v001.md
```

顔／実在人物・読める文字・手書き・紋章／記章・数字の**五族すべて**が `[NEG]` に入っていることを機械が確認します。**`[NEG]` を1語でも削ったら、必ず再実行すること。**

`[STYLE]` / `[NEG]` はバッチCの本文から機械的に読み出して埋め込んであり、生成時に次で照合できます:

```
py -3.11 -c "import sys;c=open('episodes/_planning/EP66_openfields_CODEX_BATCH_C.v001.md',encoding='utf-8').read().split(chr(10));d=open('episodes/_planning/EP66_openfields_CODEX_BATCH_D.v001.md',encoding='utf-8').read().split(chr(10));print('STYLE',c[48][2:] in d);print('NEG',c[52][2:] in d)"
```

## 7. 生成後にやること（発注者側）

1. **4枚を1枚ずつ native（3840x2160のまま）で目視**する。縮小コンタクトシートでは**前回もバッジが見えませんでした**（372px では見えず、4倍で初めて出た）。
   - `L170`: **`L075` と並べて**、天面が平らな四辺形か（楕円の弧ではないか）、全高を走る縦稜が1本あるか、その稜で輝度が**段差**になっているかを見る。
   - `L146`: トラックが**画面幅の1/10以下**かを測り、そのうえでテールゲートを**8倍以上**に拡大してバッジが無いことを確かめる。
   - `L236`: 手を **native で拡大**し、**4本の指と親指が別々に数えられる**こと、指が柱の向こう端に掛かっていること、爪が4つ見えることを確かめる。
   - `L096`: **`L173` と並べて**、両方が**正面向き**であることを確かめ、そのうえで車体前面を**8倍以上**に拡大してグリル中央・ボンネット・前バンパーに何も無いことを確かめる。
2. 合格したら、`mandatory_stills` / `people_plates` は**変更不要**（ID が同じため）。
3. `L096` は `mandatory_stills` に入っています（`episode_spec.v001.json`）。**上書き後に再度QCを通すこと。**

