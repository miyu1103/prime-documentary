# EP66 openfields — Codex 画像生成 **バッチB発注** v001（**191枚**・1プロンプト1枚）

> **プレート 191枚（`L070`–`L260`、欠番なし）**
> **`L070`–`L254` の185件を `mandatory_stills` に入れる（THUMB `L255`–`L260` の6件は入れない）**

## ★★★ バッチA（`L001`–`L069`）は廃棄されました。**この一冊だけで完結します。** ★★★

**オーナー決定（2026-08-10）：**「70枚目以降のファイルに必要な内容を入れて。69枚目までのものは無駄になってもいい」。

**したがってバッチA を開く必要はありません。**この発注書が EP66 に要る絵を**全部**持っています。
`EP66_openfields_CODEX_PASTE_B/` の paste ファイルだけを順に流せば、映画に必要なプレートが揃います。

### なぜ廃棄したか — バッチAの `[NEG]` が**規則より広く**人を禁じていた

バッチAの `[NEG]` はこう書いていました：
`human face, facial features, eyes, eye contact, looking at the camera, portrait, headshot,`
`close-up of a person, a person facing camera, profile of a face, smiling, expression`。

**これは invariant 11 ではありません。**invariant 11 が禁じるのは
**「実在する特定の人物の肖像」**であって、**人が写ること**でも**顔が写ること**でもありません。
オーナーは 2026-07-04 に「**画像の人物像はOK（実在肖像のみ禁止）**」と明示しています。

結果として何が起きたか。**バッチAの PEOPLE プレート10枚は、人が写らずに戻ってきます。**
背中・手・長靴・霧の中の遠い影しか発注していないからです。
そして台本のドラマ読みは既に警告を出していました——**この映画には11分過ぎまで人間が一人も現れない。**
実測のリテンションはそれを罰します。

**オーナーの本日の指示：**「画像にはちゃんと人間を入れてね」。

### 直したもの

| | 旧（バッチA） | 新（この発注書・§2） |
|---|---|---|
| `[NEG]` の人物条項 | `human face, facial features, eyes, … smiling, expression` | `recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake` |
| PEOPLE プレート | 10枚・**全員顔なし** | **20枚・顔が写る**（`L235`–`L254`）＋各区分に配る |
| THUMB | 4枚・人物なし | **6枚**（`L255`–`L260`）・うち2枚は**人の顔** |

`scripts/check_image_order_neg.py` は新しい `[NEG]` でも**通過します**（§6-0 に実行結果）。
`identifiable person` / `recognisable person` / `portrait`（`portrait of a named person` 内）が
face / likeness 族を満たすためです。**保護は失われていません。狭くなっただけです。**

## ★このバッチが出せるようになった理由

バッチAは「**台本が無い**」という理由で、台本に依存しない register だけを 69枚発注した。
**台本ができた。**`EP66_openfields_script.en.v003.md`（narration 実測 **4,262語**・8区分）。
したがってバッチAが §4 の表で「バッチBで決まる」と書いた四つが、**いま全部決まる**——
区分別の枚数、HOOK の5枚が何の絵か、約束→回収表、そして枚数そのものの根拠。

**枚数は仮置きしていない。**§4 に算術を全部書いた。1800秒の設計値ではなく、
**書き上がった台本の実語数**から尺を出し、そこから cut 数、still 数、motion 数の順に降ろしてある。

**題材:** 開かれた野（open-fields doctrine）。
*Punxsutawney Hunting Club v. Pennsylvania Game Commission*（ペンシルベニア州最高裁・2026-07-21）と
*Rainwaters v. Tennessee Wildlife Resources Agency*（テネシー州控訴裁・2024-05-09）。

> ### ★事実についての警告（バッチAから変わった点・変わらない点）
> **変わった点：**事実台帳 `EP66_openfields_FACTS_LEDGER.v001.md` は**存在する**。
> したがってこのバッチのプレートは、台帳の行に裏付けられた台本の**特定の一行**に紐づいている。
> §5 の各区分の冒頭に「どの行に付くか」の突合表を置いた。**引用のない絵は一枚も無い。**
>
> **変わらない点：****判断内容・結論・理由づけを絵にしない。**台帳 §9 の ⛔ 15件が全プロンプトを拘束する。
> とくに ⛔-07／⛔-08（Mark Gritzer・Kevin Hoofman の**動機・人格・違法性を描かない**）、
> ⛔-11（**実在の土地・実在の記録・実在のトレイルカメラ写真として提示しない**）、
> ⛔-01（二つの事件を**一つの運動として繋げない**）。
> Gritzer に当たる絵（L146）は**公道脇に停まった無標の空のピックアップ**であって、人ではない。
> **ここでも絵は「場所・境界・器具・その後に残ったもの」だけである。**

**この映画は「悪徳役人」の話ではありません。**主役は**境界そのもの** —— そして FILM_BIBLE §3 が定めた
**鎖に掛かった南京錠の七つの状態**である。§4.5 にどのプレートがどの状態かを書いた。

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**
3. **「良いのが出るまで回す」を禁止する。**
4. 作り直してよいのは §1 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。

EP60はこの規則で **279枚・変種0・指定外0・sha256重複0・知覚的近似重複0** を達成済み。

### 0.5 絵の水準（オーナー指示 2026-08-04）

このシリーズの工芸基準は**アカデミー／パルムドール級の脚本水準**に置かれています。画像側の意味は一つです。

- **カタログ写真を作らない。** 「門」「柵」「林」ではなく、**どの光で・どの距離から・誰の目の高さで**
  見るのかを書いてあります。プロンプトの副詞句（`from the public road side` /
  `at the height of someone standing in front of it` / `with a long lens from two hundred yards`）は
  装飾ではなく**指定**です。削らずに生成してください。
- **視点のない絵は不合格。** きれいだが誰も立っていない絵より、平凡だが**誰かの目の高さ**にある絵を採ります。
  この映画では「**道路の側から見た門**」と「**敷地の側から見た同じ門**」が別の意味を持ちます。
- **象徴を足さない。** 天秤・砂時計・十字に組んだ枝・崩れる書類の山。どれも要りません。
- **風景写真にしない。** 紅葉の絶景・朝靄の名所・俯瞰の映えは全部却下です。
  ここは**働いている土地**であって、観光地ではありません。

### 0.6 このバッチ特有の規則：**同一構図の反復は指定である**

バッチAには無かった規則です。この映画は同じ画を**意味を変えて three 回返す**設計で書かれています。

| 対 | 一枚目 | 二枚目 | 何が変わるか |
|---|---|---|---|
| 錠 | `L082`（状態1・朝・閉じている） | `L175`（状態7・**完全同一構図**） | 何も変わらない。**観客の意味だけが変わる** |
| 空の畑 | `L075`（HOOK 最終画・門柱に鎖） | `L170`（状態6・**同一の高さ・同一の画角**・柱に何も無い） | 鎖が消え、針金の輪が垂れている |
| 切られた枝 | `L073`+`L074`（HOOK） | `L172`（ACT_5・26分ぶり） | 切り口が灰色に風化している |

**この三対は「似た絵」ではなく「同じ絵」を要求します。**二枚目を生成するときは
**一枚目を横に置いて、カメラ高・画角・被写体の位置を合わせてください。**構図が違えば回収が成立しません。

---

## 1. ★絶対条件（触れた絵は使用不可）

`episodes/PD-2026-066-openfields/episode_spec.v001.json` の `forbidden_subjects` がこの節の正典です。
バッチA §1 と**同一**です。変更点はありません。以下は再掲であり、緩和ではありません。

- **人物は入れる。顔も描く。禁じられているのは「実在する特定の人物に似ていること」だけ。**
  > ### ★ここはバッチAから反転しています。読み飛ばさないでください★
  > バッチAは「生成される人間は全員、顔が写りません」と書いていました。**それは誤りでした。**
  > 契約 `forbidden_subjects` の散文規則が禁じるのは
  > **`no likeness of any real person -- not the named landowners, not the officers, not the judges`**
  > であって、**人物一般でも顔一般でもありません**（invariant 11）。
  >
  > **したがって：**
  > - **顔の見える普通の人を積極的に入れてください。**年齢も体格もばらけさせてください。
  > - **完全に架空の人物**であること。実在の誰か・有名人・公人に似せない。
  > - カメラ目線・作り笑い・広告のモデル顔にしない。**働いている人の、作っていない顔。**
  > - **制服・記章・警察・銃器は依然として禁止**（§1 の別項）。職員は一人も登場しません。
  >
  > ### ★ただし一つだけ例外がある：**名前のある実在当事者に紐づくカットには人を入れない**★
  > Hunter Hollingsworth・Terry Rainwaters・Mark Gritzer・Kevin Hoofman は
  > **実在し、存命で、名前が判決文に載っている人物**です（台帳 ⛔-07・⛔-08・⛔-11）。
  > 「彼のカット」に架空の人物を立てれば、**それは彼の肖像として読まれます。**
  > よって次の各カットは**意図的に人物なし**のままです（変更しないこと）：
  > `L071`（HOOK・台本の【】が *"boots passing behind, no face"* と指定）／
  > `L077`（*"The man is Hunter Hollingsworth."*）／`L090`（恋人と過ごす場所）／
  > `L096`・`L173`（車内捜索）／`L146`（Gritzer）／`L148`・`L149`（Gritzer が付けたカメラ）。
  > **それ以外のカットには人を入れてよく、`L235`–`L254` の20枚はそのために発注しています。**
- **読める文字・数字・手書き・印章・ロゴを描かない。**
  > ### ★このバッチで最も事故が起きるのはここです★
  > この話の主役画像のひとつは**掲示（posted sign）**です。生成器に「posted sign」と書けば、
  > **必ず POSTED / NO TRESPASSING と書きます。**
  > **掲示は次の3通りでしか描いてはいけません。**
  > **(a) 風雨で退色・膨れ上がり、面が完全に読めなくなった無地の板、**
  > **(b) 紫の塗りの帯（Pennsylvania / Tennessee の purple paint law の register）、**
  > **(c) かつて板が留まっていた釘穴と、色の抜けた樹皮の矩形。**
  > プロンプト本文に **posted / no trespassing / keep out という語を一度も書いていないのは意図的です。**
  > 板の上の印刷も同様に、**灰色の面・退色したにじみ**として描き、行や単語に見えないところまで潰します。
  > **このバッチには「ACT_2 の四語カード」「日付カード」「憲法条文の朗読」の背景板が7枚あります
  > （`L099`–`L102`・`L111`・`L112`・`L125`）。それらは文字を載せるための「空き」を作る絵であって、
  > 文字そのものは Remotion 側でタイポグラフィとして乗せます。生成画に文字を焼かないでください。**
- **制服・記章・パトカー・手錠を描かない。** 職員は一人も登場しません。
  「立ち入った」は**人**ではなく、**残っていったもの**（轍・カメラ・切られた鎖・足跡）で表します。
  **`L146`（Gritzer に当たるカット）は無標の空のピックアップです。標識も回転灯もありません。**
- **銃と獲物を描かない。** 猟銃・散弾銃・ホルスター・仕留められた動物・血・剥製・壁の角。
  **`L152`（*Russo* の熊）と `L150`（elk feeding）と `L094`（deer baiting）には動物が一頭も写りません。**
  写るのは**朝の光**と**地面に落ちた餌**だけです。原告は狩猟クラブですが、
  **これは狩猟の映画ではなく財産権の映画です。**
- **監視スリラーの意匠を作らない。** 暗視の緑・サーモグラフィの偽色・十字線・CCTVの分割画面。
  **トレイルカメラは、幹にベルトで留められた小さくて安っぽいプラスチックの箱です。それが全部です。**
- **実在と特定できる土地・建物を描かない。** 農場名・道路番号・郡章・特徴的な建築。
  **ありふれたアパラチアと中部テネシーの農地**であること。
- **法廷内観・木槌・判事席・鉄格子を描かない。** このバッチには判決の日（`L115`）と
  下級審（`L154`）に当たるカットがありますが、**どちらも法廷ではなく土地と小屋です。**
- **広告調にしない。** 黄金色の夕陽、絵葉書の紅葉、クリスマス、俯瞰の映え、HDRの縁光。
- **黒つぶれさせない。** スマホで見て何が写っているか分かること。

> ### ★航空カットについて（`L070`・`L078`・`L138` の3枚だけ）★
> 契約 `forbidden_subjects` に **`drone`** が入っており、`check_spec_satisfied.py` は
> **カット名に `drone` を含む全カットを落とします。**したがって
> **プロンプトにも成果物名にも `drone` と書かないでください。**書くのは `a low oblique aerial` です。
> 同時に `[NEG]` は `aerial view from above the treetops` を禁じています。これは矛盾ではありません。
> **禁じられているのは「樹冠の上からの真俯瞰」であって、「地平線が画面に残る低い斜め俯瞰」ではありません。**
> 3枚とも本文に **`with the horizon kept high in the frame`** と書いてあります。**この句を削らないでください。**
> 地平線が消えた瞬間、その絵は `[NEG]` に触れます。

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字がある（**板の上・樹皮の上・車体も含む**）／掲示の面に語や行が見える |
| Q3 | 印章・紋章・ロゴ・記章・ナンバープレートらしきものがある |
| Q4 | **実在の特定人物に似ている**（有名人・公人・見覚えのある顔）。**顔が写っていること自体は不合格ではありません** |
| Q4b | **人物カット（`L235`–`L254`・`L258`・`L259`）で人が写っていない**／顔が潰れている／カメラ目線の作り笑いになっている |
| Q5 | 制服・パトカー・手錠・銃・仕留められた動物・血が写っている |
| Q6 | 暗視の緑・サーモの偽色・十字線・CCTV分割画面になっている |
| Q7 | 法廷内観・木槌・判事席・鉄格子が写っている |
| Q8 | 実在と特定できる（農場名・道路番号・郡章・特徴的建築）／**地平線の無い真俯瞰**になっている |
| Q9 | 視点がない（カタログ写真・観光写真になっている）／広告調である／画面全体が暗すぎる／既存の他話と実質同じ構図 |
| Q10 | **§0.6 の三対のみ**：二枚目が一枚目と**同一構図でない**（カメラ高・画角・被写体位置がずれている） |
| Q11 | **カード背景7枚のみ**（`L099`–`L102`・`L111`・`L112`・`L125`）：文字を置く帯に枝・幹・柵線が入り込んでいる |

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]` はバッチAと同一。`[NEG]` は人物条項だけを是正した最新版です（冒頭の表）。**
`scripts/check_image_order_neg.py` を通過済み（§6-0）。**この2ブロックを1語も変えずに展開してください。**

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, muted natural colour, flat overcast daylight of a late Appalachian autumn, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing, rural Pennsylvania and Middle Tennessee between 2019 and 2026, ordinary working farmland and unmanaged second-growth woodland, worn unglamorous surfaces, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> text, lettering, numerals, digits, house numbers, handwriting, cursive writing, legible signature, seals, emblems, logos, insignia, badge, name plates, readable words on a sign, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, police officer, sheriff, trooper, uniform, patrol car, flashing lights, handcuffs, rifle, shotgun, firearm, holster, dead animal, carcass, blood, taxidermy, mounted antlers, courtroom interior, gavel, judge's bench, prison bars, razor wire, scales of justice, hourglass, a handshake, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, aerial view from above the treetops, golden hour, sunset glow, postcard scenery, autumn colour explosion, Christmas, tropical, modern smartphones, laptops, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

> **★ `[NEG]` の人物条項が「顔」から「実在人物」に変わった理由**（元に戻さないこと）
>
> **守るべきもの（変わっていない）：**EP65 で正典 `[NEG]` に人物を抑える語が1つも無く、
> 発注が「紙」「法令集」だった2枚が**完全に識別可能な顔**で戻ってきました（invariant 11 違反）。
> `scripts/check_image_order_neg.py` は、顔／実在人物・文字・手書き・紋章・数字の
> **五族すべて**を欠く発注書を拒否します。この `[NEG]` はそのチェックを通過済みです（§6-0）。
>
> **直したもの：**旧 `[NEG]` は `human face, facial features, eyes, … smiling, expression` と書いており、
> **人が写ること自体**を止めていました。それは invariant 11 より広く、
> **オーナー決定（2026-07-04「画像の人物像はOK・実在肖像のみ禁止」）に反しています。**
> `recognisable person, identifiable person, likeness of a real individual, portrait of a named person,`
> `celebrity, public figure, deepfake` は、**実在の誰かに似ることだけ**を止めます。
> **架空の人物が顔を見せて働いている絵は、これで通ります。それがこの改訂の目的です。**

---

## 3. 命名と保存先

- ファイル名 `L070.png` … `L260.png`（**191枚・欠番なし**）。
  **バッチAの `L001`–`L069` は廃棄済み。ID を再利用せず、生成もしない。**
- 保存先 `H:\pd-media\assets\ai\openfields\`（バッチAと同じ棚）。
- 長辺 3840px 以上・16:9・PNG。
- 接頭辞 `L`（land）は既存話と衝突しません（使用済み：C / F / G / H / M / P / R / S / W）。

---

## 4. 枚数（**110枚**）— 算術を全部書く

**仮置きは一つもありません。**下の6段は、書き上がった台本の実測から順に降ろした値です。

### 4-1. 台本の実測（この発注の唯一の起点）

`EP66_openfields_script.en.v003.md` のナレーション行のみを数える
（`<!--` で始まる行・`【】` の演出指示・見出し・表・引用符号を除外）。

| 区分 | 語数 | 全体比 | ナレ行数 |
|---|---|---|---|
| HOOK | 38 | 0.89% | 5 |
| OP | 3 | 0.07% | 1 |
| ACT_1 | 908 | 21.30% | 41 |
| ACT_2 | 659 | 15.46% | 31 |
| ACT_3 | 810 | 19.01% | 31 |
| ACT_4 | 940 | 22.06% | 38 |
| ACT_5 | 690 | 16.19% | 21 |
| ENDING | 214 | 5.02% | 7 |
| **計** | **4,262** | 100% | **175** |

> 台本の見出しは「4,256 words」と書いている。差の6語は em-dash を挟む行の分かち書きの違いであり、
> **下のどの数字も動かない**（4,256 で計算しても cut 数は同じ 459 になる）。
> 契約の `script_words` は [4225, 5247]。**4,262 は帯の中**である。

### 4-2. 尺（契約 `notes` の測定値だけを使う。176 wpm は使わない）

EP65 marmet の完成 ElevenLabs マスターの実測 **162.4 wpm**（4,262語 → 1,574.6秒）。
これに台本が明示している非ナレーション分を足す。

```
ナレーション            4,262 / 162.4 × 60 = 1,574.6 s
設計された沈黙（4本）                  +18.0 s   （台本 DEPARTURES 3：4+5+4+5秒）
BrandEndcard                            +9.0 s   （ENDCARD_SEC = 9）
測定済みオーバーヘッド                  +6.0 s   （契約 notes：EP65 は 1902.2 − 1896.2）
                                    ───────────
                                       1,607.6 s = 26:48
```

実測ペース帯の両端でも確認する：159.5 wpm → 1,636 s（27:16）／169.7 wpm → 1,540 s（25:40）。
**契約 `runtime_seconds` [1500, 1980] の中。**設計点は **1,607.6 秒**を採る。

### 4-3. カット数と still / video の内訳

契約 `target_cut_sec` = **3.1**（2026-08-11 改定。旧値は 3.5 だったが、FOOTAGE_PLAN v002 §5.2 の Path A を採って引き下げた。理由は契約 notes と同 §5.2）。
`scripts/build_case_film_generic.py` の `MIN_VIDEO_SHARE` = **0.68**。

```
総カット   1,607.6 / 3.5            = 459.3 → 459 cuts
video cut  ceil(459 × 0.68)         = 313 cuts
still cut  459 − 313                = 146 cuts
```

> **契約が 1800秒の設計値から出した 164 stills は、いま 146 に下がる。**
> 台本が 1800秒ではなく 1,608秒だからである。**契約の数字を書き換えるのではなく、
> 契約の算術を実測入力で回し直しただけ**であることに注意（`distinct_video_assets: 350` は動かさない）。

### 4-4. still プレートの必要数

`build_case_film_generic.py` は **still の再利用上限を 1**（1枚 = 1カット）に取る。したがって

```
必要な distinct still     = 146
バッチA が供給する         =  65   （L001–L065。L066–L069 は THUMB なので含まない）
────────────────────────────────
バッチB の still プレート  =  81
```

### 4-5. motion プレートの必要数

契約 `distinct_video_assets` = **350**（`check_spec_satisfied.py` が下限として測る）。
`scripts/check_episode_inputs.py` は **350 // 2 = 175本の accepted アーカイブ実写**を
ハード下限として要求し、`accepted + motion < 350` で asset_reuse を警告する。

**このエピソードの実写採用本数はまだ測られていない**（`footage_review_required: true`・棚の実測は未実施）。
未測定の値を有利に見積もるのは、このプロジェクトが最も高くついた失敗である。
よって**契約自身のハード下限だけを前提に置く**：

```
実写（accepted）      175   （契約の pre-flight 下限。これ以上を仮定しない）
motion（i2v）         350 − 175 = 175
```

i2v モーションクリップ1本には**元プレートが1枚**要る。プレートは still カットにも i2v にも使えるので：

```
プレート総数（A + B）  = 65 + 81 = 146  → これで motion 146本
不足する motion        = 175 − 146 = 29 → **motion 専用プレート 29枚**
```

### 4-6. 合計（**バッチA廃棄後**の再計算）

```
台本に紐づくプレート（§4-7）              110 枚   L070–L179
バッチAが持っていた register の作り直し     55 枚   L180–L234  （§4-8）
人物プレート（顔が写る・新規）              20 枚   L235–L254  （§4-8）
サムネ候補（新規・うち2枚は人の顔）           6 枚   L255–L260  （§4-8）
                                        ────────
合計                                      191 枚   L070–L260
　うち非THUMB（＝mandatory_stills に入れる） 185 枚
```

**照合：**
- still カット **146**（§4-3）≤ 非THUMB 185 ✓（146枚が still カットにも入る）
- motion クリップ **185本**（1プレート = 1本）≥ 契約下限 **175本** ✓（**余裕10本**）
- 実写 accepted が下限の175本を割っても、**プレート側の余裕10本が先に吸収する**

> ### ★訂正：`distinct_video_assets: 350` は**この尺では満たせない**（オーナー判断が要る）★
> **先の報告で私は「175（実写）＋175（motion）= 350 ✓ 契約と一致」と書きました。これは誤りです。**
> `check_spec_satisfied.py` が数えるのは**完成映画の中にある distinct な映像ソース数**です。
> §4-3 の video カットは **313本**しかありません。**313カットの中に350ソースは入りません。**
> 350 は契約が **1800秒**設計から出した値であり、台本が **1,608秒**で上がった時点で到達不能になりました。
>
> **法的な選択肢は三つで、どれもオーナー判断です（黙って動かさない）：**
> | | 手 | 影響 |
> |---|---|---|
> | (a) | `distinct_video_assets` を **313** に再導出 | 契約の書き換え1行。プレート発注は**このままで足りる** |
> | (b) | `target_cut_sec` を **3.5 → 3.1** に下げる | 総カット 519・video 353・still 166。スロットは**短くなる**ので near-still 側は悪化しない |
> | (c) | 台本を伸ばす（`script_words` の上限は 5,247・いま 4,262） | 尺 1,800秒台に戻り 350 が成立。**台本の書き直し** |
>
> **この発注書は (a)(b)(c) のどれを採っても足ります。**(b) の 166 still も 185枚で賄えます。
> **プレートが足りなくなる分岐はありません。**そこだけは先に潰してあります。

### 4-7. 区分別の配分（**実ナレ語数比**・仮置きなし）

HOOK は PACKAGING §3 が絵を4群に固定しており、バッチAが「HOOK 5枚」を未決事項として残していた。
**5枚を固定値として先に取る。**OP は語数3語だが**ブランド帯が3.5秒乗る**ので 2枚を先に取る。
残り **103枚**を ACT_1–ENDING の語数比（合計 99.04%）で按分する。

| 区分 | 語数比 | 算術 | 枚数 | ID範囲 |
|---|---|---|---|---|
| HOOK | — | PACKAGING §3 固定 | **5** | `L070`–`L074` |
| OP | — | ブランド帯の下敷き | **2** | `L075`–`L076` |
| ACT_1 | 21.30% | 21.30/99.04 × 103 = 22.15 | **22** | `L077`–`L098` |
| ACT_2 | 15.46% | 15.46/99.04 × 103 = 16.08 | **16** | `L099`–`L114` |
| ACT_3 | 19.01% | 19.01/99.04 × 103 = 19.77 | **20** | `L115`–`L134` |
| ACT_4 | 22.06% | 22.06/99.04 × 103 = 22.94 | **23** | `L135`–`L157` |
| ACT_5 | 16.19% | 16.19/99.04 × 103 = 16.84 | **17** | `L158`–`L174` |
| ENDING | 5.02% | 5.02/99.04 × 103 = 5.22 | **5** | `L175`–`L179` |
| | | | **110** | `L070`–`L179` |

### 4-8. バッチAの register の作り直し（`L180`–`L260`・81枚）

バッチAの**プロンプト本文は健全でした。壊れていたのは `[NEG]` だけです。**
よって `L180`–`L234` の55枚は、**バッチA `L001`–`L055` の本文をそのまま**引き継ぎ、
是正済みの `[NEG]` の下で作り直します。**人物と THUMB だけは作り直しません。作り直します。**

| 区分 | 枚数 | ID範囲 | 由来 | 決め方 |
|---|---|---|---|---|
| GATES | 8 | `L180`–`L187` | A `L001`–`L008` 本文流用 | 同じ門を**道路側と敷地側**の両方から。距離3種 |
| BOUNDARY | 8 | `L188`–`L195` | A `L009`–`L016` 本文流用 | 掲示を**文字を出さずに**3通り（板／塗り／痕）で描き分ける |
| FENCE | 7 | `L196`–`L202` | A `L017`–`L023` 本文流用 | 「線」を走る・角・破れの3態で |
| CAMERA | 8 | `L203`–`L210` | A `L024`–`L031` 本文流用 | 器具そのもの／器具の視点／器具が去った後 |
| TRACK | 6 | `L211`–`L216` | A `L032`–`L037` 本文流用 | 「入った」を人なしで示す register |
| WOODS_FIELD | 8 | `L217`–`L224` | A `L038`–`L045` 本文流用 | open field と woodland は法理の用語そのもの |
| DUSK | 5 | `L225`–`L229` | A `L046`–`L050` 本文流用 | 情緒はここだけで作る。**朝夕の映えは禁止** |
| FARMHOUSE | 5 | `L230`–`L234` | A `L051`–`L055` 本文流用 | **家は必ず小さく**（curtilage の外から） |
| **PEOPLE** | **20** | `L235`–`L254` | **全面的に新規** | **顔が写る。**理由は下 |
| **THUMB** | **6** | `L255`–`L260` | **全面的に新規** | **うち2枚は人の顔。**理由は §5 THUMB |
| | **81** | | | |

#### PEOPLE を 10 → 20 に増やし、顔を出す理由（これがこの改訂の本体）

1. **契約の下限は 20 だが、下限は目標ではない。**`people_plates_min: 20` は落ちない最低線です（2026-08-11 改定。旧値 10 から、PEOPLE 20枚 L235-L254 の発注に合わせて引き上げ）。
   実測の兄弟話は 7–16枚を積んでいます。
2. **台本のドラマ読みが「11分過ぎまで人間が一人も出ない」と警告している。**
   実測リテンションは 10秒→15秒で毎秒2.13ポイント落ち、30分時点でほとんど残りません。
   **人のいない30分は、この落ち方を説明します。**
3. **20枚は「人物の塊」ではありません。全区分に配ります。**

| 区分 | 最低限入れる人物カット |
|---|---|
| HOOK | 1（`L071` の長靴。**ここは台本指定で顔なし**） |
| ACT_1 | **4**（土地を使っている人。11分の空白を潰す最優先区間） |
| ACT_2 | **3** |
| ACT_3 | **3** |
| ACT_4 | **4**（クラブの会員＝人がいる場所として記録されている） |
| ACT_5 | **3** |
| ENDING | **2**（`L179` を含む） |

> **`L235`–`L254` は特定の台本行に紐づけていません。**紐づけると
> 「名前のある実在当事者のカット」に架空の顔が入る事故が起きます（§1 の例外規則）。
> **一般的な「土地を使っている人」として発注し、編集時に上の配分で配ってください。**

### 4.5 モチーフ（南京錠の七つの状態）とプレートの対応

FILM_BIBLE §3 が固定した7状態。**バッチAには一枚も入っていない**（台本が無いと置き場所が決まらないため）。
**7状態すべてがこのバッチにある。**

| 状態 | 台本の位置 | プレート | 内容 |
|---|---|---|---|
| 1 | ACT_1 冒頭【motif state 1】 | **`L082`** | 農道を横切る鎖。錠は閉じている。朝の光 |
| 2 | ACT_1【motif state 2】 | **`L097`** | 同じ錠が閉じたまま。向こう側の泥に足跡 |
| 3 | ACT_3 末【motif state 3】 | **`L133`** | 雨。錠が濡れている。誰も来ない |
| 4 | ACT_4 冒頭【motif state 4】 | **`L136`** | 別の錠・別の造り・別の門。背後の樹相が違う |
| 5 | ACT_4 後半【motif state 5】 | **`L157`** | 平板な記録光で正面から。証拠品のような画 |
| 6 | ACT_5 認知【motif state 6】 | **`L170`** | 何も掛かっていない門柱。針金の輪。奥は空の畑 |
| 7 | ENDING【motif state 7】 | **`L175`** | 状態1と**同一構図**。閉じた錠。朝の光 |

### 4.6 約束 → 回収（バッチAが「台本確定後に書く」と留保した表）

| 約束 | プレート | 台本の位置 | 回収 | プレート | 距離 |
|---|---|---|---|---|---|
| HOOK 最終画：空の畑と、鎖の掛かった門柱 | `L075` | 0:18 | 柱に何も無い。針金の輪だけ（脚注24） | `L170` | 約 24分 |
| 切られた枝と、その跡に留められた箱 | `L073`+`L074` | 0:10 | 「枝も、カメラも、争点ではなかった」 | `L172` | 約 25分 |
| コメント質問「何日で気づくか」 | （絵は `L074`） | 1:1x | **78日**ぶんの風化が乗った箱 | `L149` | 約 19分 |
| OP：教義を映画自身の言葉で | `L076` | 0:22 | PA-21 の原文が ACT_4 の冒頭で鳴る | `L137` | 約 16分 |
| 錠は閉じている（状態1） | `L082` | 0:44 | 同一構図（状態7）。意味だけが反転する | `L175` | 約 26分 |
| *Welch* が除いた「wild or waste lands」 | `L106` | ACT_2 | 「これは荒蕪地ではない」 | `L124` | 約 6分 |

### 4-9. 台本の行と register プレートの対応（**バッチAを開かずに済ませるための表**）

台本の行に紐づくプレートは §5 の各区分表にあります。下は、**特定の行ではなく register 全体**を
支える絵がどこにあるかの索引です。**すべてこの発注書の中にあります。**

| 必要なもの | このバッチのどこ |
|---|---|
| *"fenced all the way around"*（69エーカー）・柵一般 | `L196`–`L202`（FENCE 7枚） |
| *"a chained gate of his own"* の細部・門一般 | `L180`–`L187`（GATES 8枚） |
| 掲示の register 全般（無地の板・紫の塗り・落ちた板・釘穴） | `L188`–`L195`（BOUNDARY 8枚） |
| トレイルカメラの器具そのもの | `L203`–`L210`（CAMERA 8枚） |
| 砂利道・轍・分岐 | `L211`–`L216`（TRACK 6枚） |
| 二次林・林縁・刈り跡 | `L217`–`L224`（WOODS_FIELD 8枚） |
| 薄暮 | `L225`–`L229`（DUSK 5枚） |
| 遠望の母屋（curtilage の外から） | `L230`–`L234`（FARMHOUSE 5枚） |
| **顔の見える人物** | **`L235`–`L254`（PEOPLE 20枚）** |
| サムネ | `L255`–`L260`（THUMB 6枚・`thumbnail_candidates_min: 4` を超過） |

> ### ★ curtilage の一線（バッチAから継続する構図規則）★
> **このバッチにも、家に近づいた絵は1枚もありません。**`L084`・`L100`・`L107`・`L113`・`L154` は
> すべて**数フィールド以上離れた遠望**です。玄関・ポーチ・窓の中・庭の道具は発注しません。
> 唯一の内観は `L141`（ハンティングキャンプの一室）と `L163`（納屋の戸口）で、
> **どちらも住居ではありません。**近づいた瞬間、絵が主題と矛盾します。

---

## 5. プロンプト（各1枚）

### HOOK（5枚） — 0:00から声がある。20.3秒。**PACKAGING §3 の絵の割付に従う。**

| ID | 付く台本の行 |
|---|---|
| `L070` | *"West Tennessee. 2017."* — 冒頭の 6% プッシュイン |
| `L071` | *"A state wildlife officer is on the land."* — 板 → 背後を長靴が通る（顔なし） |
| `L072` | *"He walks out to a tree."* |
| `L073` | *"He cuts a branch off it…"* |
| `L074` | *"…and installs a camera on it."* — カット3が最も長く保持され、レンズで終わる |

- `L070.png`
A low oblique aerial over flat West Tennessee cropland at low winter sun with the horizon kept high in the frame, hedgerows and field boundaries dividing the ground into plain rectangles, one pale gravel track crossing them, no building near enough to identify and no vehicle anywhere [STYLE] Avoid: [NEG]
- `L071.png`
A blank weathered placard wired flat to the top bar of a steel farm gate, its face bleached and blistered to an even featureless surface with no characters or lines discernible on it, and behind the gate a pair of worn work boots and plain trouser legs passing left to right out of focus, nothing of the person visible above the knee [STYLE] Avoid: [NEG]
- `L072.png`
A single hardwood trunk standing alone in the middle ground of an open second-growth wood, the leaf litter bare between camera and trunk, seen at eye height from about thirty feet away in flat grey light [STYLE] Avoid: [NEG]
- `L073.png`
A freshly cut branch stub on a tree trunk at chest height, the exposed wood pale and wet against dark bark, the severed limb lying in the leaf litter directly below it, seen close and straight on [STYLE] Avoid: [NEG]
- `L074.png`
A small dull olive plastic box strapped to a trunk immediately beside a pale freshly cut branch stub, the black webbing strap passing over the raw wood, its lens face turned off to the left of the frame, seen from a few feet away and slightly below [STYLE] Avoid: [NEG]

### OP（2枚） — 0:20.5–0:24.0 にブランド帯が乗る。**画も声も止まらない。**

| ID | 付く台本の行 |
|---|---|
| `L075` | HOOK 最終画の保持 →【OP】*"Nobody has to."* — **26分後に `L170` が同一構図で返る** |
| `L076` | ブランド帯の下敷き。上半分を空けた「開かれた野」そのもの |

- `L075.png`
An empty field seen from just inside its boundary at the height a small box strapped to a trunk would sit, a single squared gate post standing at the left edge of the frame with a chain looped over its top, the far tree line low and flat under a pale sky, nothing moving anywhere in the frame [STYLE] Avoid: [NEG]
- `L076.png`
A wide flat expanse of working farmland under an even white sky with no fence, no gate, no track and no building anywhere in it, the horizon held low so that the whole upper half of the frame is unbroken pale cloud [STYLE] Avoid: [NEG]

### ACT_1（22枚） — **THE LINE IS NOT WHERE YOU THINK IT IS**

| ID | 付く台本の行 |
|---|---|
| `L077` | *"The man is Hunter Hollingsworth."*（**肖像なし**・彼のいた場所だけ） |
| `L078` | *"His land runs to approximately ninety-three acres, crossing Benton and Henry Counties."* |
| `L079` | *"He and his guests use it for fishing…"* |
| `L080` | *"…camping…"* |
| `L081` | *"He reaches it through his neighbour's private gravel drive and gate…"* |
| `L082` | *"…then through a chained gate of his own"* — **motif state 1** |
| `L083` | *"That gate is not the line."* |
| `L084` | *"The law draws a narrow ring around a house and calls it the curtilage."* |
| `L085` | *"Outside that ring the land is what the law calls an open field."* |
| `L086` | *"There is a second farm, and a second man. Terry Rainwaters…"* |
| `L087` | *"Two men who go to their own ground less than they used to."* |
| `L088` | *"…hesitant to use his properties or invite guests due to fear of surveillance"* |
| `L089` | *"He testified that he felt exposed…"* |
| `L090` | *"Hollingsworth also uses the property to spend time alone with his girlfriend."* |
| `L091` | *"…he has reduced his visits to his land, where he previously more regularly camped and fished."* |
| `L092` | *"…hunters should know the location of everyone else on the property."* |
| `L093` | *"…entered onto Mr Rainwaters's Harmon Creek property…"* |
| `L094` | *"…to investigate deer baiting, and he took photographs."* |
| `L095` | *"A camera… went onto Rainwaters's property that same November and came off it in December."* |
| `L096` | *"…entered Mr Hollingsworth's property and searched his vehicle"* |
| `L097` | *"The agency does not create records… and does not provide notice"* — **motif state 2** |
| `L098` | *"Officers enter private property, sometimes conceal themselves thereupon…"* |

- `L077.png`
A heavy canvas work coat hanging from a nail just inside an open barn doorway, the bright empty yard beyond it burnt out slightly against the dim interior, seen from inside at chest height with nobody in the frame [STYLE] Avoid: [NEG]
- `L078.png`
A low oblique aerial over a block of Middle Tennessee farmland with the horizon kept high in the frame, three differently worked fields meeting along hedgerows and a bare creek line of trees crossing the middle of it [STYLE] Avoid: [NEG]
- `L079.png`
The bank of a small farm pond where the grass is worn to bare mud at the one spot people stand to fish, a grey plank laid flat at the water's edge, the water still and colourless beyond, seen from the bank at waist height with nobody there [STYLE] Avoid: [NEG]
- `L080.png`
A ring of blackened stones holding cold wet ash at the edge of a field, two folding chairs left standing beside it and weathered pale, the grass around them flattened, seen from a few feet away at chest height [STYLE] Avoid: [NEG]
- `L081.png`
A private gravel drive running away between two fields toward a second gate visible far down it, the near gate standing open and the far one closed, seen from the road end of the drive at eye height [STYLE] Avoid: [NEG]
- `L082.png`
A chain drawn across the mouth of a farm track between two posts with a plain padlock closed on it, low morning light raking across the wet gravel, the track running away empty behind it, photographed head-on at chest height [STYLE] Avoid: [NEG]
- `L083.png`
A closed farm gate seen from directly alongside so its bars run away from the camera, the boundary it stands in continuing past it in both directions with open ground at either end and nothing to stop anyone walking around it [STYLE] Avoid: [NEG]
- `L084.png`
A farmhouse and one outbuilding held small in the middle distance with a tight mown ring of yard around them and unbroken open field on every side of that ring, seen from far out in the field at eye height [STYLE] Avoid: [NEG]
- `L085.png`
Worked open ground running from the foreground to a distant tree line, the crop rows still readable in the stubble, no fence, no post and no building anywhere between camera and the trees, seen at eye height under an even pale sky [STYLE] Avoid: [NEG]
- `L086.png`
A different farm's gate: a wooden five-bar gate hung between stone-set posts with a chain and a padlock at the latch end and a blank weathered placard wired to its middle rail, its face faded to nothing, seen head-on from the road at chest height [STYLE] Avoid: [NEG]
- `L087.png`
A farm track that has grassed over from disuse, the two wheel lines only just visible under the sward, running away toward a closed gate, seen from the middle of the track at eye height [STYLE] Avoid: [NEG]
- `L088.png`
A plain wooden picnic table at the edge of a field, greyed and lifting at the joints, wet leaves lying undisturbed across its top and benches, seen from a few feet away at chest height [STYLE] Avoid: [NEG]
- `L089.png`
The view out from the last of the cover at a wood edge across a completely open field, no tree, no hedge and no fold in the ground anywhere between the camera and the far boundary, seen at eye height [STYLE] Avoid: [NEG]
- `L090.png`
Two camp chairs set side by side facing an empty field at the end of the day, both unoccupied, the grass pressed flat where they stand, seen from behind them at chest height [STYLE] Avoid: [NEG]
- `L091.png`
A small flat-bottomed boat pulled up on a pond bank and left there, rainwater standing inside it with leaves floating on the surface, the paint chalked by sun, seen from the bank at waist height [STYLE] Avoid: [NEG]
- `L092.png`
Two people standing far apart on either side of one large open field, one in the near foreground turned to look across at the other and their weathered face plainly visible in flat light, the second figure small and distant on the far side, each plainly aware of where the other is standing [STYLE] Avoid: [NEG]
- `L093.png`
A shallow creek running through a wooded bottom with a gravel bar where a person could cross dry-footed, the near bank cut away and undermined, seen from the water at knee height [STYLE] Avoid: [NEG]
- `L094.png`
A scatter of shelled corn lying on bare wet ground beneath hardwoods, the kernels sunk into the mud and some beginning to sprout, seen from directly above at waist height, no animal anywhere in the frame [STYLE] Avoid: [NEG]
- `L095.png`
A black webbing strap left hanging loose around a tree trunk with nothing attached to it any longer, the free end lifted slightly by wind, the bark beneath it paler than the rest, seen close and level in flat light [STYLE] Avoid: [NEG]
- `L096.png`
A pickup truck standing in a field lane with both cab doors and the tailgate left open, seen from sixty feet away at eye height, nobody in it and nobody near it, the contents of the cab not resolvable at that distance [STYLE] Avoid: [NEG]
- `L097.png`
The same chain and closed padlock across the same farm track in the same low morning light, still fastened, and beyond it in the soft mud on the far side a line of boot prints coming and going, photographed head-on at chest height [STYLE] Avoid: [NEG]
- `L098.png`
A hollow at the edge of a wood where leaf litter and grass have been pressed flat in a body-sized oval, screened from the field by low brush, seen from a few feet away at knee height with nobody in the frame [STYLE] Avoid: [NEG]

### ACT_2（16枚） — **WHAT THE STATE SAYS IT MAY DO**

> `L099`–`L102` は台本【】が指定する**四語カード**（persons / houses / papers / possessions）の下敷き、
> `L111`・`L112` は**日付カード**（21 December 2016 · November 2018）の下敷きである。
> **文字は Remotion が乗せる。生成画に焼かない。**帯を空けること（Q11）。

| ID | 付く台本の行 |
|---|---|
| `L099` | *"…names four things a person is secure in: **persons**…"* |
| `L100` | *"…**houses**…"* |
| `L101` | *"…**papers**…"* ／ *"The Fourth Amendment says effects. Tennessee wrote possessions."* |
| `L102` | *"…and **possessions**."* |
| `L103` | *"It wrote its first constitution in 1796 and did not take the federal word."* |
| `L104` | *"In 1834 it wrote a new constitution and kept possessions. In 1870…"* |
| `L105` | *"…property, real or personal, actually possessed or occupied."*（Welch 1926） |
| `L106` | *"It would not include wild or waste lands, or other lands that were unoccupied."* — **プラント** |
| `L107` | *"…a robust history of protecting land outside the curtilage of a home as a possession."* |
| `L108` | *"Officers enter private property only when — and only in areas where — they believe hunting activity is taking place"* |
| `L109` | *"The agency enters upon the property of non-hunters as part of its enforcement activities."* |
| `L110` | *"Mr Hollingsworth's hunting license was suspended for three years…"* |
| `L111` | 日付カード **21 December 2016** |
| `L112` | 日付カード **November 2018** ／ *"The entry came twenty-three months earlier."* |
| `L113` | *"Terry Rainwaters owns a hundred and thirty-six acre home property with two homes on it…"* |
| `L114` | *"…they should desist in hunting thereupon."* — 幕の閉じ |

- `L099.png`
A single line of boot prints crossing wet bare ground from the lower left of the frame away into the distance, the upper half of the frame nothing but flat empty field and pale sky with no branch, wire or horizon feature in it [STYLE] Avoid: [NEG]
- `L100.png`
A plain farmhouse held very small and low in the frame at a great distance across ploughed ground, the whole upper half of the frame given over to unbroken pale overcast sky [STYLE] Avoid: [NEG]
- `L101.png`
A wide low horizon of flat farmland with a single bare hedgerow running along it, the lower quarter of the frame ground and the upper three quarters an unbroken bed of even pale cloud with nothing crossing it [STYLE] Avoid: [NEG]
- `L102.png`
A closed gate, a fence line and a blank weathered placard all held small together in the lower third of a wide frame with the working field behind them, and a broad even pale sky filling everything above [STYLE] Avoid: [NEG]
- `L103.png`
A hand-laid dry stone field wall, generations old and slumped in places, running away along a boundary into bare trees, seen from alongside at chest height [STYLE] Avoid: [NEG]
- `L104.png`
A squared chestnut corner post, split and silvered with great age and still standing in its own stone-packed hole, with newer wire stapled to it near the top, seen close and straight on [STYLE] Avoid: [NEG]
- `L105.png`
Ground that is plainly worked: a ploughed field with the furrows still sharp, a gate at its corner and a track worn to that gate, seen from the field at chest height [STYLE] Avoid: [NEG]
- `L106.png`
Unmanaged waste ground gone entirely to briar and sapling with no fence, no post, no track and no cut edge anywhere in it, seen from its margin at chest height in flat light [STYLE] Avoid: [NEG]
- `L107.png`
The far edge of a farmyard seen from out in the field: the last of the mown ground in the foreground and the unmown field running away from it, the buildings small and pushed off to one side of the frame [STYLE] Avoid: [NEG]
- `L108.png`
A worn footpath leaving a field and entering standing timber at one particular gap in the tree line, the ground bare at that gap and grassed everywhere else along the edge, seen from the field at eye height [STYLE] Avoid: [NEG]
- `L109.png`
A hay farm with round bales left standing in a mown field and no woodland anywhere in the frame, seen from the field edge at eye height under low cloud [STYLE] Avoid: [NEG]
- `L110.png`
A closed farm gate with the track behind it unused for a whole season, grass standing tall and seeded across both wheel lines right up to the bars, seen head-on at chest height [STYLE] Avoid: [NEG]
- `L111.png`
A bare winter field under a hard flat white sky, frost still lying in the furrow shadows and the tree line stripped, the lower third of the frame ground and everything above it empty sky [STYLE] Avoid: [NEG]
- `L112.png`
A late autumn field with the last leaves off the hedgerow and the ground wet and dark, low cloud lying along the tree line, the upper half of the frame plain unbroken grey [STYLE] Avoid: [NEG]
- `L113.png`
Two separate plain houses standing on one farm, both held small in the same frame at a distance across worked ground, bare hedgerows stepping away between camera and buildings [STYLE] Avoid: [NEG]
- `L114.png`
A plain wooden ladder stand fixed against a hardwood trunk at the edge of a field, empty and weathered pale with its lowest rungs rotted away, seen from the field at eye height in flat light [STYLE] Avoid: [NEG]

### ACT_3（20枚） — **THE ANSWER, AND ITS SIZE**

| ID | 付く台本の行 |
|---|---|
| `L115` | *"On May 9, 2024, the Tennessee Court of Appeals answered."*（**法廷は描かない**） |
| `L116` | *"…no set of circumstances exist under which the Act would be valid."* |
| `L117` | *"…the statute authorizes entries upon wild waste land areas"* |
| `L118` | *"…a person commits criminal trespass if the person enters or remains on property"* |
| `L119` | *"Their lands were secured by gates, accessible only through private drives, and posted…"* |
| `L120` | *"The Plaintiffs used and occupied their land by **farming**…"* |
| `L121` | *"…**fishing**…"* |
| `L122` | *"…**camping**…"* |
| `L123` | *"…and **hunting**."* ／ *"recreational though they may be, constitute actual use"* |
| `L124` | *"These were not wild or waste lands… but instead possessions"* — `L106` の回収 |
| `L125` | Article I, Section 7 の全文朗読の下敷き（長い一枚） |
| `L126` | *"…general warrants, whereby an officer may be commanded to search suspected places…"* |
| `L127` | *"Each agent is empowered with the discretionary authority to determine for himself or herself…"* |
| `L128` | *"There is no clear system of judicial review…"* |
| `L129` | *"…the arbitrary discretionary entries of customs officials more than two centuries ago…"* |
| `L130` | *"Colonial Boston."* |
| `L131` | *"Plaintiffs are awarded one dollar in nominal damages"* ／ *"One dollar."* |
| `L132` | ⟨HELD⟩【4 seconds. The empty track, still.】 |
| `L133` | 【motif state 3: rain. The padlock wet, the chain wet, the track empty.】 |
| `L134` | *"The statute is still in the Tennessee code. On its face it is constitutional."* |

- `L115.png`
A closed farm gate photographed flat and frontal in even record light with the frame square to it, the whole gate in shot from post to post and nothing else in the picture but the ground and a plain grey field behind [STYLE] Avoid: [NEG]
- `L116.png`
A boundary walked from outside: a fence line running unbroken from the left edge of the frame to the right edge with no gap, gate or break anywhere along it, the private ground beyond it flat and featureless [STYLE] Avoid: [NEG]
- `L117.png`
Waste ground with standing water in it, dead reed and sapling growing out of the shallows, no fence, post, track or worked edge anywhere in the frame, seen from the margin at knee height [STYLE] Avoid: [NEG]
- `L118.png`
A boundary fence seen from the public side with a wide grass verge and the edge of a metalled road in the foreground, the private ground beyond it flat and empty under low cloud [STYLE] Avoid: [NEG]
- `L119.png`
A private gravel drive, a closed chained gate across it and a blank weathered placard wired to the gate's top bar, all three in one frame from the public road at eye height, the land beyond running away out of focus [STYLE] Avoid: [NEG]
- `L120.png`
A field freshly worked to a fine tilth with the implement marks still crossing it in even lines, a bare hedgerow along the far side, seen from the headland at chest height [STYLE] Avoid: [NEG]
- `L121.png`
A rod rest pushed into a pond bank with nothing resting on it, the water flat and grey beyond, the grass around its foot trodden down, seen from behind at waist height [STYLE] Avoid: [NEG]
- `L122.png`
A patch of dead flattened grass the size and shape of a tent floor at the edge of a wood, four peg holes still in the ground at its corners, seen from directly above at chest height [STYLE] Avoid: [NEG]
- `L123.png`
A narrow path worn through grass and leaf litter by repeated use, running from a field corner into the trees, the bare earth of it standing pale against everything around it, seen from knee height along its length [STYLE] Avoid: [NEG]
- `L124.png`
One frame carrying both kinds of ground at once: unmanaged briar and sapling filling the left half up to a straight fence line, and mown worked field filling the right half, the fence running away down the middle of the frame [STYLE] Avoid: [NEG]
- `L125.png`
A very wide flat field under a completely even pale sky, the tree line a thin dark band across the lowest fifth of the frame and everything above it unbroken cloud, nothing else in the picture at all [STYLE] Avoid: [NEG]
- `L126.png`
A farm track entering standing timber and turning out of sight after thirty yards, the light dropping away where it goes in, seen from the open side at eye height [STYLE] Avoid: [NEG]
- `L127.png`
One single set of boot prints in soft mud leading away from the camera and out of the frame, no second set anywhere and no vehicle track, seen from above at chest height [STYLE] Avoid: [NEG]
- `L128.png`
A junction where two farm tracks meet with nothing at all standing at it — no post, no board, no marker of any kind — the ground bare in both directions, seen from the junction itself at eye height [STYLE] Avoid: [NEG]
- `L129.png`
A hand-forged iron hasp and staple on a door of hand-hewn oak boards weathered to grey, the iron pitted with age, the hasp swung open with nothing through it, seen close and straight on [STYLE] Avoid: [NEG]
- `L130.png`
A very old squared timber door frame standing in a stone wall with the door long gone, the opening giving onto plain daylight and nothing beyond it but rough grass [STYLE] Avoid: [NEG]
- `L131.png`
A single bare open hand held palm up at waist height with nothing in it, a plain unmarked sleeve entering at the lower frame edge, no arm above the wrist and nothing else in the picture [STYLE] Avoid: [NEG]
- `L132.png`
A farm track running straight away from the camera and standing completely empty, no vehicle, no person and nothing moving anywhere in it, held flat and square at eye height under even cloud [STYLE] Avoid: [NEG]
- `L133.png`
The same chain and closed padlock across the same farm track in heavy rain, the links and the shackle running with water, the gravel dark and pocked with drops, the track behind it empty, photographed head-on at chest height [STYLE] Avoid: [NEG]
- `L134.png`
The same closed gate as before, unchanged and still shut, seen from the same distance in the same flat light with the land behind it exactly as it was [STYLE] Avoid: [NEG]

### ACT_4（23枚） — **THE OTHER ANSWER**。ハードカット。**別の州。**

> **ここから樹相と地形が変わる。**中部テネシーの平らな農地から、**アパラチアの硬材と傾斜**へ。
> `[STYLE]` は変えない（同じ晩秋の曇天）。変わるのは**土地の起伏・樹種・岩・道の性格**である。

| ID | 付く台本の行 |
|---|---|
| `L135` | *"Clearfield County, Pennsylvania. July 21, 2026."* — THE TURN の着地 |
| `L136` | *"We hereby overrule Russo."* ⟨HELD⟩ — **motif state 4** |
| `L137` | *"…includes land."* ／ *"Includes land."* |
| `L138` | *"…two private, member-owned hunting clubs that own four thousand four hundred acres and eleven hundred acres"* |
| `L139` | *"a private place — a sanctuary — where they can come to escape…"* |
| `L140` | *"…strangers will not unexpectedly walk in… or accidentally step into their line of fire."* |
| `L141` | *"Family matters, marital problems, work stressors, romantic feelings, and faith in God."* |
| `L142` | *"…posted their properties' boundary lines with clearly visible no trespassing signs and purple paint…"* |
| `L143` | *"…installed locked gates at all public entrances…"* |
| `L144` | *"…and fenced some of their properties' boundaries with waist-high, metal wire"* |
| `L145` | *"Pennsylvania landowners… have the option to use purple paint"* |
| `L146` | *"Mark Gritzer works as a game warden for the Commission…"*（**⛔-07：行為のみ。人は写さない**） |
| `L147` | *"…have entered the Hunting Clubs' land… at least fifteen to twenty-two times"* |
| `L148` | *"Warden Gritzer even placed a trail camera on Punxsutawney's property…"* |
| `L149` | *"That camera remained on Punxsutawney's property for seventy-eight days."* — 1:1x の回収 |
| `L150` | *"…in an attempt to develop probable cause for charges of illegal elk feeding."* |
| `L151` | *"The sign is named in the statute, and it is named in order to be disregarded."* |
| `L152` | *"A bear was killed on private wooded land… approximately nine minutes after the opening…"*（**動物は写さない**） |
| `L153` | *"…found several large piles of apple mash as well as a corn feeder…"* |
| `L154` | *"…close to Russo's cabin."* ／ *"the Commonwealth Court, sitting en banc, concluded that it was bound"* |
| `L155` | *"Russo is only a little over 18 years old"* ／ *"its reasoning and result have not aged well"* |
| `L156` | *"Slavish adherence to our decision in Russo must give way…"* |
| `L157` | *"…by taking sufficient steps to exclude intruders therefrom."* — **motif state 5** |

- `L135.png`
A steep Appalachian hardwood ridge, oak and maple trunks standing out of a slope that rises sharply away from the camera, grey rock breaking through the leaf litter, the light thinner and higher here than on flat farmland, seen from below the slope at eye height [STYLE] Avoid: [NEG]
- `L136.png`
A heavy cast padlock of an older pattern closed through a chain on a pipe gate across a forest road, the gate hung between rock-set posts with hardwood timber crowding both sides of the road behind it, photographed head-on at chest height [STYLE] Avoid: [NEG]
- `L137.png`
A broad wooded plateau seen from a high point along a ridge, ranks of bare and half-bare hardwood running away over folded ground to a far ridge line, no building and no clearing anywhere in it [STYLE] Avoid: [NEG]
- `L138.png`
A low oblique aerial over unbroken Appalachian hardwood forest with the horizon kept high in the frame, one narrow forest road threading through the timber and no other break in the canopy [STYLE] Avoid: [NEG]
- `L139.png`
A small level clearing deep inside hardwood timber with the trunks standing close around it and the ground clear of brush, no structure and nobody in it, seen at eye height in soft flat light [STYLE] Avoid: [NEG]
- `L140.png`
A long open sight line down a wooded lane, the trunks stepping back on both sides and the ground clear for two hundred yards to a point of pale light at the far end, seen from the lane at eye height [STYLE] Avoid: [NEG]
- `L141.png`
The inside of a plain hunting camp room: a ring of worn wooden chairs pulled around a cold cast-iron stove, bare board walls, daylight coming flat through one window, nobody in the room [STYLE] Avoid: [NEG]
- `L142.png`
A band of purple paint brushed around the trunk of a beech at chest height, the smooth grey bark taking the paint unevenly, the wood behind falling away out of focus, seen close and straight on [STYLE] Avoid: [NEG]
- `L143.png`
A locked gate where a forest road meets a public highway, closed square across the entrance with the metalled road running past it in the foreground and hardwood standing close behind it [STYLE] Avoid: [NEG]
- `L144.png`
A waist-high metal wire fence running along the foot of a wooded slope, the mesh sagging slightly between posts and leaf litter drifted against its base, seen from outside at waist height [STYLE] Avoid: [NEG]
- `L145.png`
A run of purple painted blazes stepping up a hardwood hillside on successive trunks, each at the same height on its own tree, photographed along the line so they recede in order into the wood [STYLE] Avoid: [NEG]
- `L146.png`
A plain unmarked pickup truck parked on the gravel shoulder of a public road at the edge of hardwood timber, empty and shut, seen from a hundred yards away at eye height with nobody near it [STYLE] Avoid: [NEG]
- `L147.png`
One patch of soft mud at a gateway carrying many overlaid boot prints of different ages, some sharp and some half filled with water, seen from directly above at chest height [STYLE] Avoid: [NEG]
- `L148.png`
A small plastic box strapped to a hardwood trunk on a steep slope, its lens face turned away down the hill, the strap pulled hard into moss on the bark, seen from a few feet away and slightly below [STYLE] Avoid: [NEG]
- `L149.png`
The same kind of small plastic box after a long season on the tree: drifted leaves lodged on top of it, a spider web strung from its corner to the bark, the webbing strap faded stiff and bleached, seen very close and level [STYLE] Avoid: [NEG]
- `L150.png`
A worn hollow in the leaf litter beneath hardwoods where feed has repeatedly been put down, a few grains still lying in the churned mud and the ground bare around it, no animal anywhere in the frame [STYLE] Avoid: [NEG]
- `L151.png`
The back of a blank weathered placard on a trunk seen from inside the property, the nail points standing through the board and the open wood running away beyond it, seen close and slightly from one side [STYLE] Avoid: [NEG]
- `L152.png`
First light in bare hardwood on a cold morning, frost on the leaf litter and the trunks still half in shadow, the sky between the branches only just gone pale, no person and no animal in the frame [STYLE] Avoid: [NEG]
- `L153.png`
A heap of rotting apple mash collapsing into the leaf litter under bare trees, the fruit browned and broken open and the ground stained around it, seen from a few feet away at waist height [STYLE] Avoid: [NEG]
- `L154.png`
A plain single-storey timber cabin standing at the edge of hardwood timber, held small at a distance across a clearing, its shutters closed and no light in it [STYLE] Avoid: [NEG]
- `L155.png`
A wooden fence post snapped off level with the ground and lying where it fell, the buried end rotted hollow and packed with soil, the wire it once carried slack on the ground beside it [STYLE] Avoid: [NEG]
- `L156.png`
A whole run of old fence pushed flat by the growth of the wood behind it, the posts lying at an angle and saplings standing up through the wire, seen from alongside at chest height [STYLE] Avoid: [NEG]
- `L157.png`
A padlock and the chain it closes, photographed flat and frontal in even shadowless light against the plain grey of a gate post, the whole object filling the middle of the frame with nothing else around it [STYLE] Avoid: [NEG]

### ACT_5（17枚） — **HOW FAR THE NO REACHES**

| ID | 付く台本の行 |
|---|---|
| `L158` | *"We, therefore, do not discuss and/or question the federal open fields doctrine further."* |
| `L159` | *"The federal doctrine stands where it stood."* |
| `L160` | *"…warrantless searches of private property that is not posted, fenced, or otherwise marked…"* |
| `L161` | *"…to observe evidence of Code violations that occur in plain view…"* |
| `L162` | *"…to obtain a warrant to search private property that is posted, fenced, or otherwise marked…"* |
| `L163` | *"…administrative searches conducted pursuant to an appropriate statutory framework…"* |
| `L164` | *"…appears to confuse the open fields doctrine with the administrative search exception."* |
| `L165` | *"…the conservation, maintenance, and protection of wildlife."* |
| `L166` | *"…not a suburban one-acre plot or a nine-acre tract of land upon one acre…"* |
| `L167` | *"Truly open fields — that is, private land that is unposted and unbounded…"* |
| `L168` | *"…conspicuously posted with no trespassing signs and purple paint and/or bounded by fences, gates…"* |
| `L169` | *"Government officials, therefore, must obtain a warrant based upon probable cause…"* |
| `L170` | *"…or even no steps, to exclude intruders from their properties."* — **motif state 6**・⟨HELD⟩ 5秒 |
| `L171` | *"What put these two farms inside it in 2024 was gates, private drives, posted signs…"* |
| `L172` | 【the film's title image returns: the cut branch, the housing, the lens.】 |
| `L173` | *"The branch, the camera, the vehicle search and the video are all in the record."* |
| `L174` | *"…two provisions struck from the Code, no remand…"* |

- `L158.png`
A distant ridge line seen across a valley from a wooded height, unchanged and unmarked, no road, no clearing and no boundary visible anywhere on it, low cloud lying along its top [STYLE] Avoid: [NEG]
- `L159.png`
A single squared stone boundary marker standing upright in rough grass with no inscription or mark of any kind on any of its faces, lichen over its top, seen close and straight on at knee height [STYLE] Avoid: [NEG]
- `L160.png`
A stretch of private ground carrying nothing at all — no fence, no post, no blaze, no gate and no track — running from the camera to a far tree line under flat cloud, seen at eye height [STYLE] Avoid: [NEG]
- `L161.png`
A clear uninterrupted view from a public road verge straight into a field, no hedge and no screen anywhere along the boundary, the whole field lying open to the road, seen from the verge at eye height [STYLE] Avoid: [NEG]
- `L162.png`
The public road side of a marked boundary: a blank weathered placard, a wire fence and a closed gate all in one frame from the metalled road with the verge in the foreground [STYLE] Avoid: [NEG]
- `L163.png`
The open doorway of a plain farm building seen straight on from outside in flat daylight, the inside dim and empty and the threshold worn hollow, nobody in the frame [STYLE] Avoid: [NEG]
- `L164.png`
One frame holding two different kinds of boundary at once: a wire field fence running across the foreground and the blank wall of a farm building standing behind it, the ground between them bare [STYLE] Avoid: [NEG]
- `L165.png`
A narrow game trail running undisturbed through hardwood leaf litter, the ground printed with small tracks, no animal and no person in the frame, seen from knee height along its length [STYLE] Avoid: [NEG]
- `L166.png`
The ragged edge where the back fences of ordinary houses meet a working field, the plain rear boundaries of three lots in a row and the crop ground beginning immediately beyond them, seen from the field at eye height [STYLE] Avoid: [NEG]
- `L167.png`
Open unposted ground running away in every direction with no fence, no blaze, no gate and no worked edge anywhere, seen from the middle of it turning toward a low tree line under a flat sky [STYLE] Avoid: [NEG]
- `L168.png`
Everything an owner can put up, in one frame from the road: a closed gate, a purple painted blaze on the trunk beside it, a blank weathered placard on the next trunk along, and a wire fence running away from all three [STYLE] Avoid: [NEG]
- `L169.png`
A closed gate seen flat and frontal from the public road in even light, square to the frame, the boundary running out of both edges and the private ground behind it plainly enclosed [STYLE] Avoid: [NEG]
- `L170.png`
The identical framing as the empty field at the head of the film — the same field, the same camera height, the same squared gate post at the left edge of the frame — but with nothing on the post now, only a loop of loose wire hanging from it, the far tree line and the pale sky unchanged [STYLE] Avoid: [NEG]
- `L171.png`
A private gravel drive with a closed gate at its head and worked field on both sides, the wheel lines in the gravel bright with use, seen from the road end of the drive at eye height [STYLE] Avoid: [NEG]
- `L172.png`
The pale cut branch stub and the small plastic box on the same trunk, seen closer and squarer than before in colder light, the cut wood weathered grey now and the webbing strap gone slack around the bark [STYLE] Avoid: [NEG]
- `L173.png`
The same pickup truck standing in the same field lane with its doors open, later in the day and in flatter light, still empty and still with nobody near it [STYLE] Avoid: [NEG]
- `L174.png`
Two empty post holes in a fence line where two posts have been pulled out, the wire lying slack across the gap and both holes standing with rainwater, seen from alongside at waist height [STYLE] Avoid: [NEG]

### ENDING（5枚） — **新事実ゼロ。**閉じた錠に戻る。

| ID | 付く台本の行 |
|---|---|
| `L175` | 【motif state 7, final image: the identical framing as the head of ACT_1】 — **`L082` と完全同一構図** |
| `L176` | *"Wildlife is what both of these records are filed under."* |
| `L177` | *"The conduct was the same in both states…"*（テネシー側） |
| `L178` | *"…and it met two constitutions and two answers."*（ペンシルベニア側） |
| `L179` | *"A man standing on his own field is protected, or he is not…"* |

- `L175.png`
The identical framing as the head of the film: the same chain drawn across the same farm track between the same two posts, the same plain padlock closed on it, the same low morning light on the wet gravel, the track running away empty behind it, photographed head-on at chest height [STYLE] Avoid: [NEG]
- `L176.png`
A game trail crossing a farm track at right angles, the small pressed line of it coming out of the grass on one side and going into the grass on the other, seen from the track at knee height [STYLE] Avoid: [NEG]
- `L177.png`
A fence line running away across flat Middle Tennessee ground to a low tree line, the posts even and the wire straight, seen from beside the first post at chest height [STYLE] Avoid: [NEG]
- `L178.png`
A fence line running away across a steep Appalachian hardwood slope, the posts stepping up out of the frame and the wire following the fall of the ground, seen from beside the first post at chest height [STYLE] Avoid: [NEG]
- `L179.png`
An invented ordinary man in his sixties standing out in the middle of his own empty field in a worn canvas coat, seen from the front at about forty feet at eye height, his lined face clear and unhurried in flat overcast light and not turned to the camera, the boundary of the field running around him at a distance on every side [STYLE] Avoid: [NEG]

### GATES（8枚） — 閉じている、ということ。

- `L180.png`
A steel tube farm gate closed across the mouth of a track, chained shut at the latch post, photographed head-on from the public road side at the height of someone standing directly in front of it, wet gravel in the foreground and bare second-growth woodland behind, flat grey afternoon light [STYLE] Avoid: [NEG]
- `L181.png`
The same kind of tube gate seen from the private side looking back out toward the road, the track running away beneath it, the horizontal bars cutting the view of the road into flat strips, nobody on either side of it [STYLE] Avoid: [NEG]
- `L182.png`
A gate hinge post set in a block of concrete, seen close at knee height from one side, the paint gone entirely to rust around the pin, dead grass grown up around the base and pressed flat by rain [STYLE] Avoid: [NEG]
- `L183.png`
A length of chain wrapped twice around a gate post and closed with a plain padlock, seen close from the side at hand height, the links beaded with water, the shackle smooth and unmarked [STYLE] Avoid: [NEG]
- `L184.png`
A wooden farm gate sagging off its hinges where two fields meet, standing half open and stuck that way, grass grown up through the bottom rail, seen from a few feet away at waist height [STYLE] Avoid: [NEG]
- `L185.png`
A closed gate at the far end of a mown lane, photographed from two hundred yards away with a long lens so the gate sits small and flat in the middle of the frame and the lane converges toward it, low cloud above [STYLE] Avoid: [NEG]
- `L186.png`
A gap in a hedgerow where a gate once hung: two weathered posts still standing upright with nothing between them, the ground worn bare between the posts, seen straight on at eye height [STYLE] Avoid: [NEG]
- `L187.png`
Tyre ruts pressed deep into soft mud on the private side of a closed gate, seen from directly above at waist height, the ruts holding standing rainwater and the tread pattern soft at the edges [STYLE] Avoid: [NEG]

### BOUNDARY（8枚） — 掲示と紫の塗り。**面は読めない。**

- `L188.png`
A weathered rectangular placard nailed to a tree trunk at head height, its printed face bleached and blistered by years of weather until the surface is an even faded blur with no characters or lines discernible anywhere on it, the nail heads run with rust, plain grey woodland behind [STYLE] Avoid: [NEG]
- `L189.png`
Three identical blank weathered placards on three successive trunks along a boundary, receding away from the camera into the wood, each one turned squarely to face the camera, their faces uniformly faded to blank [STYLE] Avoid: [NEG]
- `L190.png`
A single vertical stripe of purple paint brushed onto the trunk of an oak at chest height, the paint thick and slightly run at its lower edge, bark texture standing through it, seen close and straight on in flat light [STYLE] Avoid: [NEG]
- `L191.png`
Two purple painted stripes on two trunks some yards apart, photographed along the line so that the near stripe and the far stripe align vertically in the frame, the wood behind them falling out of focus [STYLE] Avoid: [NEG]
- `L192.png`
A purple painted stripe weathered to a chalky bloom, seen at extreme close range, pale lichen creeping over its lower edge and into the bark [STYLE] Avoid: [NEG]
- `L193.png`
A blank weathered placard curled away from its trunk by years of frost and hanging by a single remaining nail, seen from slightly below in grey light [STYLE] Avoid: [NEG]
- `L194.png`
A marked boundary seen from outside it looking in: a line of blazed trunks stepping away into thin mist, each carrying the same purple stripe, the ground between them uncleared [STYLE] Avoid: [NEG]
- `L195.png`
A blank weathered placard lying face up where it fell in wet leaf litter, one bent nail still through it, seen from above at waist height [STYLE] Avoid: [NEG]

### FENCE（7枚） — 線。

- `L196.png`
A four-strand barbed wire fence running away across a stubble field toward a wooded ridge, photographed from ground level immediately beside the first post so the wires converge into the distance [STYLE] Avoid: [NEG]
- `L197.png`
A fence corner post braced with two diagonal struts, seen from outside the field at chest height, the strained wires pulling visibly on the brace, mud churned at its foot [STYLE] Avoid: [NEG]
- `L198.png`
Barbed wire stapled to a split locust post, seen at extreme close range, the staples driven deep and rusted through, the strands running out of true above and below [STYLE] Avoid: [NEG]
- `L199.png`
A fence line crossing a shallow creek, the wire dipping to the water on a rusted stay, the creek bed pale with gravel, seen from the bank at knee height [STYLE] Avoid: [NEG]
- `L200.png`
An old woven-wire fence swallowed halfway up its height by the trunk of the tree it was nailed to, the bark grown around and over the wire, seen close and level [STYLE] Avoid: [NEG]
- `L201.png`
A fence corner where three fields meet, the posts leaning three different ways and the wire slack between them, flat grey light and no building anywhere in view [STYLE] Avoid: [NEG]
- `L202.png`
A stretch of fence with its top wire broken and curled back on itself in two tight coils, seen from the outside at chest height [STYLE] Avoid: [NEG]

### CAMERA（8枚） — 幹の上の箱。**それ以上に演出しない。**

- `L203.png`
A small dull olive plastic box strapped to a tree trunk at chest height with a black webbing strap, seen from a few feet away and slightly below, its lens face turned off to the left of the frame, the bark rough around the strap [STYLE] Avoid: [NEG]
- `L204.png`
The same kind of box seen from behind its tree so that only the webbing strap and its plain buckle are visible around the trunk, the box itself hidden on the far side [STYLE] Avoid: [NEG]
- `L205.png`
A small plastic box strapped high on a trunk, photographed from the ground looking straight up, the box small and dark against a flat pale sky seen through bare branches [STYLE] Avoid: [NEG]
- `L206.png`
The view such a box would have: a narrow game trail through thin saplings, framed low and dead centre at about knee height, nothing and nobody on the trail, flat grey light throughout [STYLE] Avoid: [NEG]
- `L207.png`
A webbing strap cinched hard around bark, seen at extreme close range, the webbing frayed at the edge and the plain buckle bedded into the trunk's surface [STYLE] Avoid: [NEG]
- `L208.png`
Two small plastic boxes on two separate trunks at a junction of two woodland tracks, both turned to face down the same lane, seen from the lane at eye height [STYLE] Avoid: [NEG]
- `L209.png`
A small plastic camera box lying on the open tailgate of a pickup truck among wet leaves and a loose coil of webbing strap, seen from above at waist height [STYLE] Avoid: [NEG]
- `L210.png`
The pale unweathered rectangle of bark left on a trunk where a box has been strapped for years and has now been taken off, seen close and straight on, two small nail holes at its upper corners [STYLE] Avoid: [NEG]

### TRACK（6枚） — 入った、ということ。

- `L211.png`
A gravel farm track running straight away from the camera between two hedgerows under low cloud, the wheel ruts standing with rainwater, seen from the middle of the track at eye height [STYLE] Avoid: [NEG]
- `L212.png`
The same kind of track seen from the crown of a rise looking down along it, the pale gravel standing out against wet grass, the far end of it lost in the tree line [STYLE] Avoid: [NEG]
- `L213.png`
A fork in a farm track where the left branch has grassed over completely and the right branch is bare and used, seen from the fork itself at waist height [STYLE] Avoid: [NEG]
- `L214.png`
Fresh vehicle tracks pressed over older ones in wet gravel, seen from close to the ground at waist height so the two sets of tread cross in the middle of the frame [STYLE] Avoid: [NEG]
- `L215.png`
A concrete culvert pipe running under a farm track, the gravel worn thin over the crown of it, seen from the ditch below at ground level [STYLE] Avoid: [NEG]
- `L216.png`
A track passing from open ground into standing timber, the light dropping away as it goes in, seen from the open side at eye height [STYLE] Avoid: [NEG]

### WOODS_FIELD（8枚） — 「野」と「林」そのもの。

- `L217.png`
The inside of an unmanaged second-growth wood at midday under heavy overcast, straight bare trunks receding in every direction, no undergrowth and no path, seen at eye height [STYLE] Avoid: [NEG]
- `L218.png`
A narrow deer trail worn through leaf litter in a wood, seen from knee height along its length, the trail disappearing between two trunks [STYLE] Avoid: [NEG]
- `L219.png`
A stand of hardwood on a hillside seen from below the slope, the ground rising steeply so the trunks stand out of vertical across the frame [STYLE] Avoid: [NEG]
- `L220.png`
A field of frost-killed stubble running flat to a dark tree line, seen from the middle of the field at eye height under a white sky [STYLE] Avoid: [NEG]
- `L221.png`
A mown hay field seen along the cut stripes so they converge, the windrows still lying, low cloud above and no machinery in the frame [STYLE] Avoid: [NEG]
- `L222.png`
The edge of a wood where the field stops and the trunks begin, photographed along the edge so that open ground fills the left half and closed timber the right [STYLE] Avoid: [NEG]
- `L223.png`
Rainwater standing in the low corner of a ploughed field, the sky reflected flat and grey in it, seen from the field at waist height [STYLE] Avoid: [NEG]
- `L224.png`
A brush pile of cut limbs heaped at a field corner and greying with age, seen from a few yards away at eye height [STYLE] Avoid: [NEG]

### DUSK（5枚） — 薄暮。**夕陽の色は禁止。**

- `L225.png`
An empty field at dusk seen from the middle of it, the tree line a single flat dark band low in the frame and the sky above it still pale and colourless, no artificial light anywhere [STYLE] Avoid: [NEG]
- `L226.png`
The same empty field at dusk seen from just inside its gate, the gate's top rail crossing the bottom of the frame, the far tree line almost gone to black [STYLE] Avoid: [NEG]
- `L227.png`
The last flat light of the day lying on a wooded rise beyond a field, seen from the field at eye height, the colour drained out of everything and no lamp burning anywhere [STYLE] Avoid: [NEG]
- `L228.png`
A field at dusk with ground mist gathering in the low centre of it, the mist level and about waist deep, the tree line standing above it [STYLE] Avoid: [NEG]
- `L229.png`
A field at dusk seen through a wire fence from outside it, the strands of wire crossing the pale sky in the upper part of the frame, everything beyond the wire in silhouette [STYLE] Avoid: [NEG]

### FARMHOUSE（5枚） — **必ず遠い。**curtilage には入らない。

- `L230.png`
A plain two-storey farmhouse and a low barn seen from three fields away at dusk, the buildings held small near the centre of the frame with one window lit, bare hedgerows stepping away between camera and house [STYLE] Avoid: [NEG]
- `L231.png`
The same kind of farmstead in flat daylight from the crown of a rise, the house and barn small against a broad pale sky, ploughed ground filling the foreground [STYLE] Avoid: [NEG]
- `L232.png`
A farm lane running away toward a distant house, the house kept small at the end of it and never approached, wet grass either side, seen from the road end of the lane at eye height [STYLE] Avoid: [NEG]
- `L233.png`
A farmhouse roofline just visible over a ridge of bare trees from a neighbouring field, only the roof and one chimney showing, everything else screened by timber [STYLE] Avoid: [NEG]
- `L234.png`
A single yard light burning on a pole at a distant farmstead at dusk, the buildings around it dark and small, seen from far out in an empty field [STYLE] Avoid: [NEG]

### PEOPLE（20枚） — ★**顔の見える人間を入れる。**この20枚がこの改訂の本体です★

> **全員、完全に架空の一般人です。**実在の誰か・有名人・公人に似せないでください。
> **カメラ目線の作り笑いは禁止。**広告のモデルではなく、**働いている人の、作っていない顔**を撮ります。
> 年齢・体格・性別をばらけさせてください。**制服・記章・銃器は依然として禁止**です。
> 服装は無地の作業着（キャンバス地のコート、キルティングのベスト、ネルシャツ、長靴）。
> **どの一枚も、台本の特定の実在当事者のカットとして使ってはいけません**（§1 の例外規則）。

- `L235.png`
An entirely invented ordinary man in his sixties in a heavy canvas work coat closing a steel tube farm gate across a track, both hands on the top rail, turned three-quarters toward the camera so his weathered face is clearly visible in flat overcast light, no expression put on for the camera [STYLE] Avoid: [NEG]
- `L236.png`
An invented woman in her fifties in a quilted work jacket walking a fence line with one hand trailing along the top wire, seen from the front at about twenty feet at eye height, her face lit evenly by flat cloud, a stubble field running away behind her [STYLE] Avoid: [NEG]
- `L237.png`
An invented farmer standing at the edge of a mown field looking out across it, seen from the side at chest height with his face in clear three-quarter profile, mud dried on his boots and knees, low cloud behind him [STYLE] Avoid: [NEG]
- `L238.png`
Two invented ordinary men standing either side of a closed farm gate talking, both faces plainly visible in flat daylight, one leaning on the top rail and the other with his hands in his coat pockets, the track running away behind them [STYLE] Avoid: [NEG]
- `L239.png`
A pair of bare hands closing a padlock through a chain on a gate post, the person's forearms and the front of their canvas coat in frame and their invented ordinary face visible above, looking down at what their hands are doing [STYLE] Avoid: [NEG]
- `L240.png`
An invented man in his forties in a plain flannel shirt and quilted vest standing in the open doorway of a barn, flat daylight from behind the camera falling on his face, the dim interior behind him and nothing staged [STYLE] Avoid: [NEG]
- `L241.png`
An invented older man sitting on the open tailgate of a pickup truck parked at a field gate, his boots on the ground and his hands loose between his knees, looking off to one side, his face clearly visible in even light [STYLE] Avoid: [NEG]
- `L242.png`
An invented woman crouched down to look at a fresh boot print in the mud of a farm track, one knee to the ground, her face turned down toward it but plainly visible in profile, the track running away out of focus behind her [STYLE] Avoid: [NEG]
- `L243.png`
An invented man walking away down a gravel farm track seen from behind at about fifty yards, held small in the frame, the hedgerows and wheel ruts converging past him under low cloud [STYLE] Avoid: [NEG]
- `L244.png`
An invented young man in his twenties in a canvas coat looking up at a tree trunk above head height, chin lifted and his face fully lit by flat overcast, bare second-growth woodland standing around him [STYLE] Avoid: [NEG]
- `L245.png`
An invented man and woman in their sixties standing together on the bank of a farm pond, both facing the flat grey water and seen from the side so both faces are visible, two rods propped unused against a post beside them [STYLE] Avoid: [NEG]
- `L246.png`
An invented person in a hooded coat standing at the edge of a wood with the hood pushed back and their face clearly visible, looking in among the trunks, hands at their sides and nothing in them [STYLE] Avoid: [NEG]
- `L247.png`
An invented older man's hands and forearms resting on the top rail of a wooden fence with his face visible above them looking out across the field, deep lines and grey stubble, flat daylight and no jewellery [STYLE] Avoid: [NEG]
- `L248.png`
An invented man in his fifties driving a pickup truck at walking pace down a farm lane, seen from in front and slightly to one side through the open driver's window, his face visible and one forearm resting on the sill [STYLE] Avoid: [NEG]
- `L249.png`
An invented farmer standing alone in the middle of a wide stubble field, seen from about thirty yards at eye height so that he is small in the frame but his face and the set of his shoulders still read, hands at his sides [STYLE] Avoid: [NEG]
- `L250.png`
Two invented people walking a boundary together along a hedgerow, seen from in front at about forty feet, both faces visible under flat cloud, one of them pointing off to the side at something out of frame [STYLE] Avoid: [NEG]
- `L251.png`
An invented woman in her forties crouched at a fence corner with one hand on a strained wire, her face turned up toward the camera's direction without acknowledging it, mud on her gloves and the brace post beside her [STYLE] Avoid: [NEG]
- `L252.png`
An invented man sitting on an upturned bucket beside a cold fire ring at the edge of a field at dusk, elbows on his knees, his face lit by the last flat daylight and no fire burning [STYLE] Avoid: [NEG]
- `L253.png`
An invented man in a canvas coat coming through a farm gate toward the camera and pulling it shut behind him with one hand, seen from in front at about twenty feet at eye height, his face clearly visible [STYLE] Avoid: [NEG]
- `L254.png`
An invented older couple standing side by side at the head of their own gravel drive, seen from in front at about thirty feet so both weathered faces are visible under flat cloud, the closed gate and the drive running away behind them [STYLE] Avoid: [NEG]

### THUMB（6枚） — サムネ候補。**縦横比は16:9のまま。文字は焼き込まない。**

> ### ★上1/3は空けたまま生成する — これは構図の好みではなく、実測された寸法要件です★
> **空けるのは「フレーム上端から高さの 33%」（1280×720 なら上端から 240px の帯）。**
> その帯には**枝・幹・地平線・柵の線・被写体の一部を一切入れない**こと。
> 根拠（実測値・`scripts/check_thumb_subject_luma.py` と `check_final_acceptance.py`）:
> - 見出し文字は **1280px 幅換算で「連結成分の高さ 150px 以上」**（`TEXT_MIN_HEIGHT = 150`）。
>   150px の1行に上下の縁取り **12px 以上**（`OUTLINE_MIN_PX = 12`）が付くと **174px**。
>   240px の帯なら上下に 33px ずつ余白が残る。**枝が1本でも横切ると縁取りが切れて落ちます。**
> - **帯は明るいこと。** 被写体判定の箱は縦 `y = 0.12〜0.88` と定義されていて**上1/3を含みます**。
>   その箱の平均輝度が **60以上**（`SUBJECT_MIN_LUMA = 60`）必要なので、
>   上を暗い樹冠で埋めると被写体が明るくても落ちます。**上は淡い曇天の空か、明るい霧で埋める。**
> - 完成サムネ全体で **平均輝度 33以上・コントラスト（輝度標準偏差）40以上**
>   （`THUMB_MIN_MEAN_LUMA = 33.0` / `THUMB_MIN_CONTRAST_STD = 40.0`）。
>   **この映画の `[STYLE]` は low contrast なので、この6枚だけは正面から衝突します。**
>   よって**この6枚に限り硬いキーライトで発注**し、**平均輝度 55以上・標準偏差 45以上**を狙います
>   （EP65 は本編と同じ低輝度で発注してしまい、あとから硬いキーライトの1枚を追加する羽目になりました）。
> - 主題は**下2/3の中に置き、水平方向はやや中心から外す**。見出しが2行に折れた場合に
>   上 40% まで使えるようにするためで、**上 33%〜40% の間には主題の芯を置かない**。
>
> **`L258` と `L259` は人の顔です。**顔のあるサムネは CTR に効き、かつ輝度・コントラストの床を
> 最も楽に超えます（肌は面として明るく、目と影がコントラストを作る）。
> **ただしカメラ目線にはしない**——視線は画面内の対象へ向けます。
>
> **生成後、この6枚は必ず 1280×720 に縮小して**、上1/3が本当に空で明るいかを目で確認すること。

- `L255.png`
A closed steel tube farm gate with a chain and a plain padlock at its latch post, shot dead centre and close from directly in front at chest height, one hard directional key light raking from the left so the wet metal stands out bright against the darker ground, a broad even field of pale bright overcast sky filling the entire upper third of the frame with no branch, no trunk, no wire and no horizon line entering that upper third, the gate and its chain sitting wholly within the lower two thirds and set slightly right of centre [STYLE] Avoid: [NEG]
- `L256.png`
A small dull olive plastic box strapped to a tree trunk with a black webbing strap, seen at very close range from slightly below and set into the lower two thirds of the frame slightly left of centre, one hard directional key light from the right throwing a crisp shadow of the box across the bark, and above it the whole upper third of the frame given over to an even pale bright sky with nothing whatever crossing it [STYLE] Avoid: [NEG]
- `L257.png`
A thick vertical stripe of purple paint on the trunk of a tree, seen close and straight on with the trunk filling the lower two thirds of the frame and standing slightly right of centre, hard light raking across the bark from the left so the paint reads bright and saturated against the grey wood, the upper third of the frame left entirely open as flat pale bright sky with no branch or foliage in it [STYLE] Avoid: [NEG]
- `L258.png`
The head and shoulders of an entirely invented ordinary man in his sixties in a canvas work coat standing at a closed farm gate, his weathered face brightly and hardly lit by one directional key light from the left and his eyes directed off to the right of frame rather than at the camera, his head and the gate held wholly within the lower two thirds and set slightly left of centre, the whole upper third of the frame an unbroken field of pale bright overcast sky with nothing entering it [STYLE] Avoid: [NEG]
- `L259.png`
An invented ordinary person's hands closing a padlock through a chain on a gate post with their face visible above the hands looking down at them, one hard key light from the right so both the hands and the face stand out bright against the darker gate, hands and head together occupying the lower two thirds slightly right of centre, the upper third of the frame nothing but even pale bright sky [STYLE] Avoid: [NEG]
- `L260.png`
A blank weathered placard nailed to a tree at head height, its face faded to an even featureless pale surface with no characters or lines on it anywhere, shot dead centre and close with the placard and trunk occupying the lower two thirds of the frame, one hard key light from the left so the board is markedly brighter than the wood behind it, the upper third of the frame an unbroken field of pale bright overcast sky with nothing entering it [STYLE] Avoid: [NEG]

---

## 5.5 ショートのプレートは、このバッチにも含まれていません

`SHORTS_SLATE_EP66` は**まだ存在しません**（`episodes/_planning/` にあるのは EP53-56 / EP57-59 / EP62-65 の3本）。
バッチA §5.5 の判断はそのまま生きています。**ショートのフックも落ちも決まっていないので、発注を先に出しません。**
先に出せば、スレートが書かれた時点で「使われないプレート」と「足りないプレート」が同時に生まれます。

スレートが書かれたら**バッチC**として、同じ形式で発注します。各ショートは **16枚以上の distinct plate** を要求します。
ただしこの映画の場合、ショートの落ちになりうる素材は既にこのバッチの中にあります
（`L149` の78日／`L170` の空の門柱／`L131` の空の手のひら）。**まず流用可否を測ってから追加発注してください。**

---

## 6. 生成後にやること（発注者側）

### 6-0. 発注書そのものの検査（**生成を始める前に済ませてある**）

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP66_openfields_CODEX_BATCH_B.v001.md
```

実行結果（2026-08-10）:

```
[neg] ok   EP66_openfields_CODEX_BATCH_B.v001.md

[neg] 1 order(s): every [NEG] carries all 5 required token families
```

顔・読める文字・手書き・紋章／記章・数字の**五族すべて**が `[NEG]` に入っていることを機械が確認しました。
**`[NEG]` を1語でも削ったら、必ず再実行すること。**

### 6-1. 生成後

1. **全191枚をラベル付きコンタクトシートで目視**する。プロンプトIDで選ばない
   （short60 は3枚がプロンプト一覧どおりに選んで別の絵だった）。
   **特に §1 の Q2（板・樹皮・車体の文字）・Q4（実在人物に似ていないか）・
   Q4b（人物カット22枚に人がちゃんと写っているか）を1枚ずつ潰す。**
2. **§0.6 の三対を横に並べて見る**（`L082`/`L175`・`L075`/`L170`・`L073`+`L074`/`L172`）。
   **構図がずれていたら、二枚目だけ文言を直して1枚だけ作り直す。**回収が成立しない絵は使えません。
3. **カード背景7枚**（`L099`–`L102`・`L111`・`L112`・`L125`）は、実際にタイポグラフィを仮置きして
   文字が読める明るさ・空きがあるかを確認する。
4. `episodes/PD-2026-066-openfields/episode_spec.v001.json` の `mandatory_stills` を
   **`L001`–`L065` の65件を全部消し、`L070`–`L254` の185件で置き換える**（THUMB `L255`–`L260` は入れない）。
   - **バッチAの ID を残さないこと。**生成しない絵を宣言すると
     `check_spec_satisfied.py` が「宣言された静止画がどのカットにも無い」で落ちます。
   - `check_spec_satisfied.py` は **stem 一致**なので、i2v 後に `L127.mp4` として映画に入っても
     `L127.png` の宣言を満たします。
   - **QCで不合格になった枚を差し替えたら、その場で `mandatory_stills` も差し替える。**
5. `people_plates` を **`L235`–`L254` の20件**に差し替える（旧 `L056`–`L065` は廃棄）。
   `people_plates_min` は **10 のまま**でよい（20 は下限を超えているだけで、契約変更は不要）。
   `L092`・`L179`・`L258`・`L259` にも人が写りますが、**people register には数えません**
   （前二者は本編カット、後二者はサムネ）。**実質の人物カットは 24枚**になります。
6. 1枚 = 1モーションクリップとして `remotion/public/openfields/motion/` に書き出す
   （i2v または深度パララックス。**ズーム/パンだけは不可**）。
7. **i2v クリップは書き出した直後に測る。**
   ```
   py -3.11 scripts/check_motion_clip_stillness.py --slug openfields --quarantine
   ```
   ほとんど動いていない 4.8 秒のクリップは、長いスロットに入れられた瞬間にループして
   **near-still 判定で受領書を落とします**（EP65 は 18:53 の 4.03 秒でこれをやりました）。
8. `py -3.11 scripts/check_episode_inputs.py --slug openfields` を**レンダー前に**通す。
   `distinct_video_assets: 350` に対し **実写採用 175本**が下限。
   **棚の実測（§4-5 の未測定項目）はここで初めて数字になります。**

### 6-2. このバッチが解いた未確定と、まだ残っている未確定

| バッチA §4 の未確定 | 状態 |
|---|---|
| HOOK 5枚がどの絵か | **解決**（`L070`–`L074`・§5 HOOK） |
| 区分別（ACT_1..ACT_5 / ENDING）の枚数 | **解決**（§4-7・実ナレ語数比） |
| 約束→回収表 | **解決**（§4.6） |
| 静止画プレートの総数 | **解決**（146。契約の 164 は 1800秒設計値・§4-3） |
| i2v 用プレートの総数 | **契約下限で確定**（175）。**実写採用本数の実測でのみ動く** |
| ショート用プレートの内数表 | **未解決。**`SHORTS_SLATE_EP66` が無い（§5.5） |

| 新しく残る宿題 | 誰が解くか |
|---|---|
| 棚の実測（register ごとの accepted 本数） | `scripts/search_archive.py` ＋ **目視QC**。350 に届くかはここで決まる |
| `mandatory_stills` 185 への追記（旧 65／中間案 175 から、Batch B・C の全非THUMB idを追記して完了） | 生成完了・目視QC通過の直後（6-1 の 4） |
| 実写が 175本に届かない場合の処置 | **オーナー判断**（契約 notes の (a) 追加発注 / (b) `target_cut_sec` を上げる）。黙って動かさない |
