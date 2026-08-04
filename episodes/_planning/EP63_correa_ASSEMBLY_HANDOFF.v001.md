# EP63 correa — 組み立て側への引き継ぎ v001

**2026-08-04 · 設計スレッドから** · 対象: `PD-2026-063-correa` / *Correa v. Hospital San Francisco*, 69 F.3d 1184 (1st Cir. 1995)

> **一行**：契約・台本・発注書・事実台帳は揃っている。**画像は227枚中122枚しか存在せず、いまも生成中。ナレーション・filmconfig・カット表・Remotion合成は未着手で、そこからが組み立て側。**
>
> **state は `script_review` であって `script_verified` ではない。**`manifest.json` の `state_note` に経緯が残っている（一度 `script_verified` と書かれ、事実でなかったので戻された）。**この文書は state を進めない。**

> ⚠️ **先に §3-1 を読むこと。**`check_script_length` が「速い読みだと 22.4 分＝27分の下限割れ」と警告している。**声の速度を固定し、最初のナレーションを実測してから画像作業に一切コミットしないこと。**

---

## 0. いま何が本当なのか（すべて 2026-08-04 21:58 JST に実測）

| | 状態 | 実測値 |
|---|---|---|
| 契約 `episode_spec.v001.json` | ✅ valid | 1620–1920s（27–32分）/ 5,100–5,600語 / 8区分 / figure beats 13–17 per act / `distinct_video_assets` **234** / `people_plates_min` 10 / `mandatory_stills` **223** / `thumbnail_candidates_min` 3 / `audio_layers` 2 / `forbidden_subjects` 10 / `forbidden_claims` 10 |
| `manifest.json` | ✅ | `target_duration_minutes: 30` · `runtime_band_minutes: [27.0, 32.0]` · **state = `script_review`** |
| 台本 `script.en.v002.md` | ✅ 3ゲート緑 | `check_script_length` **5,306語** PASS ／ `check_script_craft` ナレーション **5,281語 = 30.53分**（173.0 wpm）PASS ／ `check_episode_spec` valid |
| 台本の重複 | ✅ 欠陥0 | 機械掃引で**修理バッチ由来の重複は1件も無い**（§2-1） |
| 引用 | ⚠️ 欠陥1・台帳欠落3 | 帰属付き53文中40文が判決原文と6語以上一致。**出典不明はゼロ**。改変1件・台帳の穴3件（§2-2） |
| figure beats | ✅ **98個** | HOOK 4 / OP 3 / ACT_1 16 / ACT_2 17 / ACT_3 17 / ACT_4 17 / ACT_5 16 / ENDING 8。**5幕すべて契約帯 13–17 の内側** |
| 発注書のプレート | ✅ **227枚** | `C001`–`C227` 連番・**欠番0・重複0** |
| `mandatory_stills` | ✅ **223件** | 全件が発注書に存在・重複0。**除外4枚は `C221` `C222` `C223` `C227`＝THUMB**（§3-2） |
| 画像の生成 | 🔄 **122 / 227** | `C001`–`C122` 連続・欠番0・**全枚 3840×2160**。**105枚が未生成で、いま約50〜55秒に1枚のペースで生成継続中**（`C122` 書き込み 21:57:38） |
| 画像の配置 | ❌ **未着手** | `remotion\public\correa\img` は**ディレクトリごと存在しない**。staged stills 0 / `P###` 顔登録 0 |
| 実写プール | ⚠️ **8 / 54** | 54本取り込み → **46本却下**（目視43＋`scan_video_shape` 3）。契約 `distinct_video_assets` 234 に対し薄い |
| filmconfig | ❌ 未作成 | `episodes\_planning\EP63_correa_filmconfig.v001.json` が無い |
| Remotion 合成 | ❌ 未登録 | `Root.tsx` に `Ep63` で始まる composition が無い |
| `check_episode_inputs` | ❌ NOT READY | **8件の不足**（§4に全文） |
| **R15（音読）** | ❌ **未実施** | 誰も声に出して読んでいない |

---

## 1. ファイル一覧（全部フルパス・存在を1件ずつ確認済み）

**契約と状態** — すべて存在する
```
episodes\PD-2026-063-correa\episode_spec.v001.json           ✅ 数値の唯一の出所。ツールはここしか読まない
episodes\PD-2026-063-correa\manifest.json                    ✅ target 30分 / state script_review / state_note あり
```

**台本と設計** — すべて存在する
```
episodes\_planning\EP63_correa_script.en.v002.md             ✅ ★確定版。v001 は使わない
episodes\_planning\EP63_correa_FILM_BIBLE.v001.md            ✅ 73,137 bytes。なぜこの順で語るか
episodes\_planning\EP63_correa_FACTS_LEDGER.v001.md          ✅ 51,616 bytes。✓/VERBATIM 以外は使用不可
episodes\_planning\measurements\EP63_correa_RAW.md           ✅ 判決文全文 8,359語。**引用の最終照合先はここ**
episodes\_planning\EP63_correa_beats.v001.json               ✅ 演出データ98個
episodes\_planning\EP63_correa_REREVIEW.v001.md              ✅ 30,821 bytes。再採点記録
episodes\PD-2026-063-correa\01_research\fact_recheck.v001.md ✅
```

**画像**
```
episodes\_planning\EP63_correa_CODEX_BATCH_A.v001.md         ✅ 発注書。C001–C227（§7 と §「サムネ用C227」に追記あり）
episodes\PD-2026-063-correa\04_scenes\thumb_prompts.v001.md  ✅ サムネ4案 C221/C222/C223/C227
H:\pd-media\assets\ai\correa\                                ✅ 存在。**C001.png–C122.png の122枚のみ**（3840×2160）
H:\pd-media\assets\ai\correa\_rejected\                      ✅ 2枚（C072_text-like-lines.png / C074_text-like-lines.png）
H:\pd-media\assets\ai\correa\_qc_candidates\                 ✅ 存在するが**空**
remotion\public\correa\img\                                  ❌ **存在しない。**組み立て側が作って配置する
```

**素材（実写）** — すべて存在する
```
remotion\public\correa\factory\                              ✅ 54本。**うち採用8本**
runs\qc\correa_clip_verdicts.v001.json                       ✅ 却下46本の理由つき・目視記録つき
runs\qc\correa_shape.json                                    ✅ ndjson 54行（幅高さ尺）
runs\qc\correa_title_staging.v001.json                       ✅ 取り込み元の台帳
episodes\PD-2026-063-correa\05_visuals\factory_clip_qc.v001.json  ✅
runs\qc\correa_factory\factory_footage_contact_01..03.png    ✅ 目視した3枚のコンタクトシート
runs\imagegen\contact_correa_C001_C025.jpg ほか計4枚          ✅ **C001–C100 のみ。C101以降のシートは無い**
remotion\public\correa\factory_pruned_offtopic\              ✅ 存在するが**空**
```

**ショート** — すべて存在する
```
episodes\_planning\SHORTS_SLATE_EP62-65.v001.md              ✅ short262 / short263 / short264 の設計
episodes\_planning\SHORTS_SLATE_EP62-65_QUOTE_AUDIT.v001.md  ✅
episodes\PD-2026-063-correa\09_package\short262_funnel.v001.json  ✅（263 / 264 も同じ場所に存在）
```

**存在しないもの（作るのは組み立て側）**
```
episodes\_planning\EP63_correa_filmconfig.v001.json          ❌
episodes\PD-2026-063-correa\06_audio\narration_index.v001.json ❌
remotion\public\correa\narration.mp3                         ❌
remotion\public\correa\img\                                  ❌
episodes\PD-2026-063-correa\08_edit\captions.final.v001.srt  ❌
```

---

## 2. 設計スレッドが今回やった検査と、その結果

### 2-1. 重複掃引 — **欠陥0件**

`manifest.json` の `state_note` は「修理で2箇所の重複節が入った」と記録している。
**v002 の実ファイルを機械掃引した結果、その類の欠陥は1件も残っていない。**

掃引した内容（すべて `EP63_correa_script.en.v002.md` 全410行に対して）：

| 掃引 | 定義 | ヒット |
|---|---|---|
| A | 1文の中に同じ4語以上の句が2回 | 2件（いずれも修辞・後述） |
| B | 同一文が40行以内に逐語で再出現 | **0件** |
| C | 隣接する節が逐語で反復（`X, X.` 型＝修理バッチの事故形） | **0件** |
| D | 5語以上の節が全文中2回以上 | 1件（意図的な呼び戻し） |
| E | 語の二重打ち（`the the` 等） | **0件** |

`state_note` が例に挙げた `and said so in a footnote, and said so in a footnote.` は、
L325 に**1回しか出てこない**（＝すでに修理済み）。

**`pd_edit.py` による修正は1件も行っていない。直すべきものが無かったため。**

**意図的な反復として残したもの（触っていない）**

| 行 | 反復 | なぜ残すか |
|---|---|---|
| L123 | `one hundred thousand apiece for the three children, and fifty thousand apiece for the four grandchildren` | 賠償額の対句。金額の対比がそのまま構造 |
| L137 | `the Emergency Medical Treatment and Active Labor Act` ×2 | 1回目は語の定義、2回目は**判決冒頭文の引用**。別物 |
| L227 / L387 | `A hospital that examines you badly … A hospital that examines you differently` | この映画の中心命題のアナフォラ。ENDING で意図的に再演される |
| L347 | `It omitted it from its submissions for the initial scheduling conference. It omitted it from its submissions for the pretrial conference.` | 放棄の積み上げを列挙するアナフォラ。同文中の `at the close of …` ×2 も同じ意図 |
| L52↔L268 / L56↔L266 / L247↔L395 / L251↔L389 | 判決文の同じ引用が ACT_1 と ACT_4／ENDING に再出 | **コールバック設計**。ENDING は判決の限定条項を数え直す構造で、原文を再掲する必要がある |
| L9 | `176 words per finished minute` ×2 | ナレーションされない `【】` メタ行 |

### 2-2. 引用の機械照合 — **出典不明ゼロ・改変1件・台帳の穴3件**

**まず前提**：**この台本には引用符が1つも無い**（`"` `“” ` `「」` の出現数 0）。
引用は地の文に溶かして帰属だけで示す文体（`The evidence is conflicted, the court wrote, as to whom she saw…`）。
したがって `"…"` の正規表現抽出では**0件しか採れない**（実際 0 件だった。唯一の `*…*` は L38 の事件名 `Correa v. Hospital San Francisco`）。

そこで、**帰属マーカー（`the court wrote` / `the panel said` / `the opinion records` / `testified` / `in footnote` 等）で文を機械抽出し、事実台帳と判決原文の両方に対して語境界つき n-gram 完全一致を取った。**
略語（`Ms.` `Dr.` `p.m.` 等）で文分割が壊れる問題と、`, the court wrote,` の挿入句が n-gram を割る問題は、どちらも補正済み。

| | 件数 |
|---|---|
| 帰属付き文（抽出） | **53** |
| 事実台帳の引用符つき断片（照合先プール） | **154** |
| **A 判決原文と6語以上完全一致** | **40** |
| **B 改変あり（near miss）** | **1** |
| **C 出典が見つからない** | **0** |
| うち「原文にはあるが事実台帳に無い」＝台帳の穴 | **3** |

**B — 改変されている引用（1件）**

| 行 | 台本 | 判決原文（`EP63_correa_RAW.md`）・事実台帳 DM-13 |
|---|---|---|
| **L365** | The sums awarded, the court said, **do not shock our collective conscience.** | the sums awarded **do not shock or even vellicate** our collective conscience |

`or even vellicate` が省略されている。省略記号は無く、`the court said` で直接引用として提示されている。
**意図的な可読性優先（`vellicate` は耳で分からない語）かもしれないので、こちらでは直していない。**
組み立て側かオーナーの判断で、①原文どおりに戻す ②帰属を `the court put it` 等の間接話法に緩める ③そのまま、のいずれかを選ぶこと。**判決原文に無い語を足して「直す」ことは絶対にしない。**

**穴 — 判決原文には逐語であるが、事実台帳に載っていない（3件）**

台本は**正しい**。落ちているのは監査証跡のほうである。

| 行 | 台本の引用 | 判決原文での一致長 | 台帳 |
|---|---|---|---|
| L179 | …the **predicate fact: that HSF had accepted the federal government's carrot and agreed to come under** the statute | 16語一致 | 無し |
| L197 | Angel testified that he told the receptionist **his mother was experiencing chest pains** | 6語一致 | 無し（CR-07 は別の言い回し） |
| L201 | **There is no principled way in which we can accommodate HSF's request**, the court replied | 13語一致 | 無し |

ほかに、原文にあるが語数が短くて自動一致しなかったもの（すべて逐語で存在する）：
`That ends the matter`（L256・原文4語）／`We need go no further`（L379・原文5語）／
`both disingenuous and unpersuasive`（L363・台帳 HA-14 にあり）。

**唯一の語の入れ替え**：L149 `For patients such as Ms. Gonzalez, the court said, the statute has two linchpin provisions.`
原文は `for purposes of patients such as Ms. Gonzalez, **EMTALA** has two linchpin provisions`。
`EMTALA` → `the statute` の置換。意味は変わらないが、`the court said` の枠内にあるので厳密には逐語ではない。

**結論：この台本には、記録に無い言葉を裁判所の言葉として提示している箇所は1つも無い。**

---

## 3. この話に固有の罠（先に読むと事故が減る）

### 3-1. ★★ 尺のリスク — **これが最大の地雷。画像作業の前にナレーションを実測すること**

`check_script_length` の実出力（そのまま）：

```
PASS script_length: 5,306 words (need 3,699-5,480)
  narration estimate  slow 32.4m | median 29.8m | fast 22.4m
  target band         27.0-32.0 min
  ! RISK: at the fast end of the measured pace (237.4 wpm, seen on williams/florence)
    this lands at 22.4 min -- under the floor. Either pin the voice speed or write to 6,410 words.
```

読み替えるとこうなる：

- 中央値の読み（176語/分・gap込み）なら **29.8分**で契約帯のど真ん中。設計はこの前提で組んである。
- **williams / florence で実測された速い読み（237.4 wpm）が出ると 22.4 分**。契約下限 27 分を **4.6 分**割る。
- EP61 は「帯の内側の語数」で書いたのに実測 wpm が設計値を否定して **25.0 分**の master になり、**組み立て不能で作り直しになった**。同じ壊れ方が再現しうる。

**したがって、この順を守ること：**

1. **声の速度を固定する。**`nPczCjzI2devNBz1zQrb` / `eleven_multilingual_v2` で、stability・similarity・**speed を明示的に指定**して記録に残す。既定値任せにしない。
2. **最初のナレーションを1本通しで生成し、実尺を秒で測る。**
3. **その実測が 27.0–32.0 分に入るまで、画像の配置・`motion/` 書き出し・レンダーに一切コミットしない。**
   画像を動かす作業は最も高価な工程で、台本が伸縮すればカット表ごと作り直しになる。
4. 実測が下限を割った場合、**台本を削るのではなく足す**（`check_script_length` の言う 6,410語 は「速い読みでも 27 分を保つ語数」）。ただし語数を足すと `script_words` 契約帯 [5100, 5600] を破るので、**契約側を直すかオーナー承認（APR）を取るか**を先に決めること。

### 3-2. `mandatory_stills` は223件。**THUMB は `C221` `C222` `C223` `C227` の4枚で、これは入っていない**

ここは番号が直感に反するので、実測の対応表を置く。

| プレート | 役 | `mandatory_stills` |
|---|---|---|
| `C001`–`C210` | 本編の絵 | ✅ 入っている |
| `C211`–`C220` | PEOPLE（顔なし人物・`people_plates_min: 10`） | ✅ 入っている（カットに出るため） |
| **`C221` `C222` `C223`** | **THUMB（発注書 §5「THUMB（3枚）」）** | ❌ **意図的に除外** |
| `C224` `C225` `C226` | **本編の絵**（発注書 §7 の増補。水槽／受付へ歩く二人／開くエレベーター扉） | ✅ 入っている |
| **`C227`** | **THUMB 4枚目**（`thumb_prompts.v001.md` §3 で追加。明るい直射光の「記録の不在」） | ❌ **意図的に除外** |

220 + 3 = **223**。除外4枚はすべてサムネ候補である。

**`check_spec_satisfied.py` は「宣言された静止画がどのカットにも出てこない」で落ちる。**サムネはカットではないので、
**`C221` `C222` `C223` `C227` を `mandatory_stills` に足し戻さないこと。**
`episode_spec.v001.json` の `notes` 末尾にも同じ趣旨が明記してある。

> ⚠️ 発注書 `EP63_correa_CODEX_BATCH_A.v001.md` の L700 は「`mandatory_stills` に **C001〜C223 を全部書く**」と書いているが、
> これは §7 と `C227` が追記される前の記述で、**いまは古い**。実ファイルの223件のほうが正しい。

### 3-3. 画像が**まだ105枚足りない**。しかも生成は今も走っている

実測（2026-08-04 21:58 JST）：`H:\pd-media\assets\ai\correa\` に `C001.png`–`C122.png` の **122枚**。
すべて 3840×2160、欠番なし。直近の書き込みは `C122.png` が 21:57:38 で、**約50〜55秒に1枚**のペース。
**残り105枚。このペースなら概ね90分前後で揃う見込みだが、これは推定であって測定値ではない。**

- **コンタクトシートは `C001`–`C100` の4枚しか無い。**`C101` 以降は**まだ誰も1枚も目視していない。**
- `_rejected\` に2枚（`C072_text-like-lines.png` / `C074_text-like-lines.png`）＝**文字規則違反で一度差し戻した実績がある**。同じ事故が未検査帯にも起きうる。
- EP62 では「226枚揃った」と書いたあとの全枚目視で**14枚の作り直し**が出た（`EP62_greene_ASSEMBLY_ADDENDUM.v001.md`）。**枚数が揃うことと使えることは別。**

**組み立て側は、全227枚が揃ってから配置すること。**そのうえで `C101` 以降を必ず目視してから `remotion\public\correa\img` に入れる。

### 3-4. 実写が8本しかない。**これは欠陥ではなく設計**

`check_episode_inputs` はこう言う：

```
asset_reuse will FAIL: 8+0 distinct video assets vs ~234 footage cuts, so ~226 clip(s) must repeat
```

**そのとおりで、想定内。**実測の内訳（`runs\qc\correa_clip_verdicts.v001.json` の記録）：

- **54本取り込み → 46本却下**（目視43本＋`scan_video_shape` が3本＝縦向きまたは1920×1080未満）
- 却下理由の実例：汎用ボケ玉、夜の空撮、法人ストック、ビーチ、鹿、読める店舗看板、**`reception` で検索したら「受信できていないテレビ」が3本**
- 生き残った8本は「待つ」レジスターのみ：待合室の水槽の前・白いベンチのパン・明るい診療所受付・エレベーター扉2本・蛍光灯・モノクロの雨・ベンチで話す二人
- **トリアージ室も整理券も番号表示も1本も無い**

> **決定的な事実：`check_spec_satisfied.py` の `distinct_video_assets` は、実写と `remotion\public\correa\motion\*.mp4` だけを数える。静止画は1枚も数えない。**

**つまり227枚は、動かして初めて資産になる。**
i2v（Wan2.2 5B / `ae-demo\comfy_wan.py`）か深度パララックス（`gen_depth_maps.py` → `DepthImage`）で `motion\` に書き出すこと。
**ズーム／パンだけは不可**（オーナーが紙芝居として却下済み）。動いているかは連続フレーム差分で実測してから出すこと。

なお `episode_spec.v001.json` の `notes` には、設計時点の想定として
**「`check_episode_inputs.py` は accepted(8) + motion ≥ 234 と読むこと。accepted(11) ではない」**と明記されている。

### 3-5. `waiting room` レジスターは**このチャンネルで一度も使っていない**

`episode_spec` の `notes` の実測：`waiting room` の burn rate は **0/24**。61話で待合室クリップを1本も使っていない。
逆に法廷 23/24・独房 20/24・刑務所 18/24・手錠 7/7 は使い切っている。
**だから `forbidden_subjects` が法廷と独房を禁じている。**在庫があるからといって法廷に逃げないこと。

### 3-6. `check_script_length` は前書きの散文も数える

実測差：`check_script_length` **5,306語** ／ `check_script_craft` のナレーション **5,281語** ／ 台本 L9 の自己申告 **5,278語**。
差は `【】` のメタ行と見出しの数え方の違い。**上限 5,480 に対して余裕は約174語しかない。**
台本ファイルに解説を書き足すと、映画本体が押し出されて落ちる。

---

## 4. そちらの作業（この順で）

### ① ナレーション生成 — **ここが最初で、ここで一度止まる**

- 声 `nPczCjzI2devNBz1zQrb` / モデル `eleven_multilingual_v2`
- stability ≈ 0.35 / similarity ≈ 0.80（EP62 と同条件）
- **speed を明示指定し、値を記録に残す**（§3-1）
- 台本は **`EP63_correa_script.en.v002.md` のみ**。`v001` は残置してあるが使わない
- **生成したら実尺を秒で測り、27.0–32.0 分に入ることを確認するまで次へ進まない**
- ElevenLabs はオーナー承認済み（確認不要）。ただし cost/character は記録すること

### ② `filmconfig` を作る（これが無いと何も始まらない）

`episodes\_planning\EP63_correa_filmconfig.v001.json` は**存在しない**。EP61 / EP62 のものが雛形。

| 欄 | 状態 |
|---|---|
| `slug` / `episode_id` / `out` | すぐ書ける（`correa` / `PD-2026-063-correa`） |
| `hookSeconds` | **8.0**（オーナー決定 2026-08-04・`PD_SCREENPLAY_STANDARD` §16.5） |
| `hookLine` | 台本 HOOK（L23–）の20語をそのまま。**4カット × 約1.7秒**の設計 |
| `assets` → `05_visuals\asset_manifest.vNNN.json` | **未作成。**画像227枚が揃って配置されるまで作れない |
| `narration_index` → `06_audio\narration_index.v001.json` | ①の生成物 |
| `narration` → `remotion\public\correa\narration.mp3` | ①の生成物 |
| `captions` → `08_edit\captions.final.v001.srt` | 強制アラインメントの生成物 |

### ③ カット表は**生成する。手で書かない**

```
py -3.11 scripts\build_case_film_generic.py --config episodes\_planning\EP63_correa_filmconfig.v001.json
```
→ `04_scenes\correa_beatsheet.v001.json` と `correa_build_manifest.v001.json` が出る。
**`shotlist` を手書きしないこと。**EP38 で廃止済みで、二重実装（CLAUDE.md 不変条件14）になる。

### ④ figure beats を書き込む

```
.venv\Scripts\python.exe scripts\set_figure_beats.py --config <filmconfig> --beats episodes\_planning\EP63_correa_beats.v001.json --min-per-act 13
```
データは既に98個・5幕すべて 16–17 で契約帯 13–17 の内側。**config ができるまで書き込めないだけ。**

### ⑤ 画像を配置し、動かす

1. 227枚が揃うまで待つ（§3-3）
2. `C101`–`C227` を目視する（コンタクトシートが無い帯）
3. `remotion\public\correa\img\` を作って配置
4. `scripts\register_face_stills.py --slug correa` で `P###` を10枚以上登録
5. `motion\` に i2v か深度パララックスで書き出す（§3-4）

### ⑥ Remotion 合成を登録

`remotion\src\Root.tsx` に `Ep63` で始まる composition が**無い**。`npm run typecheck` を緑にすること。
WebGL を使うなら長尺は `--concurrency=4`。

### ⑦ レンダー前の必須検査

```
.venv\Scripts\python.exe scripts\check_episode_inputs.py --slug correa      ← 8件の不足を全部潰してから
.venv\Scripts\python.exe scripts\check_spec_satisfied.py --slug correa      ← film.json 生成後・レンダー前
```

**いまの `check_episode_inputs --slug correa` の実出力（8件）：**

```
- no filmconfig: expected episodes/_planning/EP63_correa_filmconfig.v001.json
- no narration index: episodes\PD-2026-063-correa\06_audio\narration_index.v001.json
- no narration audio: remotion/public/correa/narration.mp3
- only 0 still(s) in remotion/public/correa/img (need >= 40)
- only 0 P### people still(s) ... against the 10 this episode declares
- 223 of 223 mandatory_stills are not in remotion/public/correa/img
- only 8 clip(s) survived visual QC ... (46 were rejected)
- no Remotion composition id starting with Ep63 in Root.tsx
```

---

## 5. 「間違って見えるが直してはいけないもの」

| | 理由 |
|---|---|
| state が `script_review` | **`script_verified` にしない。**再レビューが「MEETS THE STANDARD」を返すまで進めない（`manifest.state_note`） |
| 実写が8本 | §3-4。画像を動かして埋める設計 |
| `mandatory_stills` が227でも226でもなく **223** | §3-2。THUMB 4枚（`C221`–`C223` と `C227`）を意図的に外してある |
| `C224` `C225` `C226` が `mandatory_stills` に**入っている** | §3-2。この3枚は THUMB ではなく**本編の絵**（§7 増補）。番号だけ見て外さない |
| 発注書 L700 の「C001〜C223 を全部書く」 | §3-2。`C227` 追加前の古い記述。実ファイルが正 |
| 台本に引用符が1つも無い | §2-2。**この話の文体**。引用符を足すと語数と字幕分割が変わる |
| ACT_1 と ENDING に同じ判決文が出る | §2-1。ENDING が判決の限定条項を数え直す構造。コールバック設計 |
| L227 と L387 の `A hospital that examines you…` の反復 | §2-1。この映画の中心命題のアナフォラ |
| 「病院は彼女を**追い返していない**」 | `forbidden_claims` 冒頭。**追い返しではなく、番号を呼ばなかった。**この区別が映画そのもの |
| 「遅れが彼女を**殺した**」と言わない | `forbidden_claims`。死因は別施設での hypovolemic shock。認容された賠償は**待たされた間の苦痛と遺族の悲嘆** |
| 「裁判所が不当移送を違法と判断した」と言わない | 第1巡回区は**脚注7で移送の認定の審査を明示的に見送っている**（台本 L121 が正しくそう言っている） |
| `C211`–`C220` を含め**顔が判別できる絵を1枚も出さない** | 発注書 L88。`forbidden_subjects` と invariant 11 |

---

## 6. 未解決（正直に・そちらの判断が要る）

### 6-1. ★ 尺が速い読みで下限を割る — **§3-1。この文書で一番重い未解決**

対処法は決めていない。**ナレーションを実測してから決める**のが唯一の正しい順序で、
設計スレッドは実測していない（ナレーションを1度も回していない）。

### 6-2. ★ 画像が105枚未生成、うち `C101` 以降は1枚も目視していない

生成は継続中（§3-3）。**揃ったあとの全枚目視が必須。**
EP62 は「揃った」と書いたあとの目視で14枚の作り直しが出ている。
特に見るべき点：①文字が1文字も無いか（`C072` `C074` で一度落ちている）②顔が判別できないか
③平均輝度が33以上か（`C227` は狙い38以上）④モチーフ7状態（整理券）が**同じ一枚の紙**に見えるか。

> **モチーフ連鎖は EP62 で壊れた実績がある。**Codex は 1プロンプト＝1枚で走り**前の枚を参照できない**ため、
> 「the same ticket」とだけ書いたプレートは別物になる。`C001` / `C099` / `C100` / `C136` / `C137` / `C207` / `C208` を
> **並べて見る**こと。ここが崩れていると ENDING（L397 の `motif 7 completes · C208`）が閉じない。

### 6-3. R15（音読）が未実施

**誰も声に出して読んでいない。**「R15は省略しない。リズムは黙読では測れない」が基準。
①の本番VO生成が、そのまま音読の代わりになる。**生成したら必ず一度通しで聴くこと。**
聴かずに次工程へ進むと、EP61 の轍（VO生成後に台本が伸びて作り直し）を踏む。

### 6-4. 引用の改変1件と台帳の穴3件（§2-2）

- **L365 の `or even vellicate` 省略**：直すか残すかの判断が要る。設計スレッドは触っていない。
- **台帳の穴3件**：台本は判決原文に対して正しいが、`FACTS_LEDGER.v001.md` に対応行が無い。
  台帳は「ここに無い文は script に入らない」を不変条件にしているので、**厳密には台帳側を補うべき**。
  補うなら `EP63_correa_RAW.md` から逐語で起こすこと。**新しい文言を作らない。**

### 6-5. 再レビューが修理後に再実行されていない

`EP63_correa_REREVIEW.v001.md` は**修理前**の採点。
`state_note` が言うとおり、**ディスク上の実ファイルに対する再レビューが返るまで state は `script_review`。**

### 6-6. ショート3本は導線が意図的に不合格

`check_short_funnel.py --short 262`（263 / 264 も）は落ちる。
**長尺の video ID が無いから**で、正しい挙動。長尺を非公開アップロードした時点で解ける。

### 6-7. 実写8本のまま行くのか、追加取り込みするのか

`check_episode_inputs` は「約117本必要（reuse cap）」と言い、`distinct_video_assets` 契約は 234。
**画像を動かして埋める前提**（§3-4）だが、`stage_episode_footage.py --slug correa` で足す選択肢もある。
ただし棚のラベルは全面的に信用できない（`evidence_bag` がカートゥーンだった実績）ので、
**足すなら必ずコンタクトシートで目視してから。**検索語ではなくラベルを引くこと。

---

## 7. 検査コマンドまとめ（期待値つき）

```bash
cd C:/Users/aab15/Documents/prime-documentary

.venv/Scripts/python.exe scripts/check_episode_spec.py --slug correa
# 期待: [spec] correa: valid -- runtime 1620-1920s, script 5100-5600 words, 8 sections,
#       beats 13-17/act, 234 distinct video assets, 10 people plates, 223 mandatory still(s),
#       10 forbidden subject(s)

.venv/Scripts/python.exe scripts/check_script_length.py episodes/_planning/EP63_correa_script.en.v002.md --lo 1620 --hi 1920
# 期待: PASS script_length: 5,306 words (need 3,699-5,480)
#       slow 32.4m | median 29.8m | fast 22.4m
#       ! RISK ... 22.4 min -- under the floor   ← この警告が出るのが正常。消えたら台本が変わっている

.venv/Scripts/python.exe scripts/check_script_craft.py episodes/_planning/EP63_correa_script.en.v002.md --words 5100 5600
# 期待: PASS  every mechanical craft gate is green.
#       narration 5281 words -> 30.53 min at 173.0 wpm
#       emotion 0 / AI-smell 0 / CTA 0 / you-your 0.76 / questions 0.57 /
#       short-sentences 28.6% / longest bare stretch 19.1s / specific 11.04 / quarantined 0

.venv/Scripts/python.exe scripts/check_episode_inputs.py --slug correa
# 期待（現時点）: NOT READY -- 8 problem(s)。§4-⑦ の8件と一致すること

.venv/Scripts/python.exe scripts/check_spec_satisfied.py --slug correa      # film.json 生成後
.venv/Scripts/python.exe scripts/check_final_acceptance.py PD-2026-063-correa --render <mp4> --emit-receipt
```

**プレート数の確認（発注書側）**
```bash
.venv/Scripts/python.exe -c "import re,pathlib;t=pathlib.Path('episodes/_planning/EP63_correa_CODEX_BATCH_A.v001.md').read_text(encoding='utf-8');s=sorted({int(x) for x in re.findall(r'\bC(\d{3})\b',t)});print(len(s), 'C%03d-C%03d'%(s[0],s[-1]), 'gaps:', [n for n in range(s[0],s[-1]+1) if n not in set(s)])"
# 期待: 227 C001-C227 gaps: []
```

**`mandatory_stills` の確認**
```bash
.venv/Scripts/python.exe -c "import json,re;s=json.load(open('episodes/PD-2026-063-correa/episode_spec.v001.json',encoding='utf-8'))['mandatory_stills'];ids={re.search(r'C\d{3}',x).group(0) for x in s};print(len(s), len(ids), sorted({'C221','C222','C223','C227'} & ids))"
# 期待: 223 223 []      ← 末尾が [] であること。THUMB 4枚が入っていない証明
```

**画像の生成状況**
```bash
.venv/Scripts/python.exe -c "import os,re;d=r'H:\pd-media\assets\ai\correa';p=sorted(x for x in os.listdir(d) if re.fullmatch(r'C\d{3}\.png',x));n={int(x[1:4]) for x in p};print(len(p),'of 227  missing:',len([i for i in range(1,228) if i not in n]))"
# 2026-08-04 21:58 JST の実測: 122 of 227  missing: 105
# 2026-08-04 22:01 JST の再測: 127 of 227  missing: 100  ← 3分で5枚。生成が走っていることの確認
# 期待（完了時）: 227 of 227  missing: 0
```

**実写の採用数**
```bash
.venv/Scripts/python.exe -c "import json,os;d=json.load(open('runs/qc/correa_clip_verdicts.v001.json',encoding='utf-8'));a=set(os.listdir('remotion/public/correa/factory'));print('staged',len(a),'rejected',len(d['rejected']),'accepted',len(a-set(d['rejected'])))"
# 期待: staged 54 rejected 46 accepted 8
```

**受領書が緑になるまで予約も投稿もしない**（`.claude/rules/19-ship-gate.md`）。

---

*v001 · 2026-08-04 · 設計スレッドから。**この文書に書いていない数字は、私が測っていない数字。***
*画像の枚数と生成ペースは 2026-08-04 21:58 JST の実測で、読む時点では変わっている。必ず §7 のコマンドで測り直すこと。*
