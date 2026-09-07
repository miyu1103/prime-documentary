# EP52 morton — Codex スレッドA「素材生成」引き継ぎプロンプト v001（30分・4幕・payoff 末尾積み上げ）

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN_ARCHITECTURE）も実装スレッドB（CODEX_B）も**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> ★30分尺。素材点数は EP50（60分）の約半分・12分エピの約2.5倍。**「だいたい」で決めず §3 の確定値と §3.3 の検算をそのまま使う。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP52 / Episode ID: PD-2026-052-morton / slug: morton
Composition id: Ep52Morton（B が Root.tsx に登録・A は staging まで）／1920x1080 / fps30 / 30:00
事件:       The Michael Morton Case（1986 妻 Christine 撲殺→1987 夫 Michael を誤って有罪・life→
            25年服役→2011 DNA で exonerate→真犯人 Mark Norwood 有罪→検事 Ken Anderson 収監）
            1986-08-13 朝、テキサス州 Williamson County で Christine Morton が自宅ベッドで撲殺された。
            夫 Michael（32・スーパー店長）は当朝6時ごろ出勤しており、帰宅して遺体を発見。
            3歳の息子 Eric は「monster が mommy を襲った・daddy はいなかった」と祖母 Rita に語ったが、
            捜査陣（検事 Ken Anderson）は【夫が犯人】と決めつけ、Eric の証言・緑のバン・血のバンダナ・
            盗まれたカード（San Antonio 使用）・不明の指紋を全て弁護側に隠して有罪にした（物証ゼロ）。
            Michael は約25年服役。2005 pro-bono の John Raley と Innocence Project（Nina Morrison）が
            DNA 検査を求め、後任 DA John Bradley が約6年争ったが、2011-06 に裁判所がバンダナ検査を命令。
            バンダナから Christine の血＋別の男の DNA＝Mark Alan Norwood。2011-10-04 釈放・2011-12-19 無罪確定。
            Norwood は Christine 殺害で有罪（2013-03-27・life）。さらに DNA が 1988-01 の Debra Baker 殺害にも一致
            ＝Michael が服役中に Norwood が第二の殺人を犯した。Norwood は Baker 殺害でも 2016-09 有罪。
            Anderson は Court of Inquiry で 2013-04-19 逮捕命令・criminal contempt・10日収監（実質約5日）・
            弁護士資格を返上。2013 the Michael Morton Act（証拠開示改革法）が Perry 知事の署名で成立。
            ★主題は【証拠を隠された冤罪・25年・二人の実在の villain・そして末尾に積み上がる真実の連鎖】。
            ★Michael Morton は【存命・法的に完全に無罪確定】＝彼の無実は事実として断定してよい。
            ★★被害者 Christine Morton と Debra Baker は【実在の殺害被害者】＝暴行/殺害の描写・再現を一切作らない。
              3歳の証人 Eric は【最大限の配慮】。実在人物（Morton/Christine/Eric/Rita/Norwood/Anderson/Bradley/
              Raley/Morrison/判事）の顔・肖像・likeness を一切作らない。匿名・非識別の一般人は可。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ・30分スケール）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**215本の固有プロンプト×1枚＝215枚**・バリエーション0） | `H:\pd-media\assets\ai\morton\S<NNN>.png` | 5–8時間（GPU） |
| A-1b | i2v 種画像の生成（**43本の固有プロンプト×1枚＝43枚**・バリエーション0） | `H:\pd-media\assets\ai\morton\M<NN>_src.png` | 1.5–2.5時間（GPU） |
| A-1c | サムネ用 emotive-face 静止画（**3枚**・CTR §4A・非実在の illustrative face・§5.12） | `H:\pd-media\assets\ai\morton\T<NN>_face.png` | 20分（GPU） |
| A-2 | 静止画のQCと目視（**全261枚を目視必須**＝215 body + 43 i2v種 + 3 thumb_face） | `05_visuals/still_qc.v001.json` + コンタクトシート | 2.5–4時間 |
| A-3 | ~~depth map~~ **不要（本作は depth treatment を使わない・§6.4）** | — | — |
| A-4 | factory 実写クリップ **240本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | 4–6時間（うち目視だけで2時間以上） |
| A-5 | i2v モーション化 **43本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\morton\M<NN>_rife.mp4` | 18–50時間（GPU・**複数日**） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **30本** | `05_stock/overlay_selection.v001.json` | 1時間 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 30分 |
| A-8 | Remotion public への staging | `remotion/public/morton/{img,factory,motion,overlay,thumb}/` | 40分 |

> **★★ 最重要の前提（EP42–51 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 215本＝215行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **variants 指定なし（＝1枚）** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 215 + i2v 種 43 + thumb_face 3 = 261枚（各1回）。** factory 240本は生成でなく在庫からの選抜。
> ★**`--only S001` のログで `shots=261` を確認**してから本番を回す（215 body + 43 i2v種 + 3 thumb_face = 261）。
> ★i2v 43本は**複数日GPU**。**開始前にマシン状態を確認**（heavy-job preflight）。夜間・分割で回す。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-052-morton/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を **A(producer)とB(consumer/validator)で一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 240 エントリ、`motion` 配列は 43 エントリ、`overlay` 配列は 30 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5／§4.6 に全 240 + 43 + 30 を列挙済み。build スクリプトはこの列挙を消費するだけで、空配列を書かない）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\morton\**` / `H:\pd-media\assets\ai_video\morton\**` | **A** | 読み書き |
| `episodes/PD-2026-052-morton/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-052-morton/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/morton/{img,factory,motion,overlay,thumb}/**` | **A** | 読み書き |
| `episodes/PD-2026-052-morton/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_morton_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-051-*/**` および EP39〜51 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を読む） | `PD-2026-052-morton`（variants 指定なし） / `52 --only S001` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-052-morton --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit N --exclude-used --ep PD-2026-052-morton --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-052-morton` |

> **★`gen_depth_maps.py` は使わない**（本作は depth treatment を使わない＝depth map 不要・§6.4／DESIGN §1「footage treatment は bleed/parallax、depth 禁止」）。

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（実在確認してから・直近の `*centralpark*`(EP50) を優先、無ければ `*cleveland*`/`*strieff*`） |
|---|---|---|
| `scripts/qc_morton_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_centralpark_stills.py`（無ければ `qc_strieff_stills.py`） |
| `scripts/select_morton_factory.py` | §7 の factory 240本の確定選定・EP39〜51 sha256 除外検証 | `scripts/select_centralpark_factory.py`（無ければ `select_strieff_factory.py`） |
| `scripts/comfy_wan_morton.py` | §8 の i2v 43本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_centralpark.py`（実在確認） |
| `scripts/rife_morton.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_centralpark.py`（実在確認） |
| `scripts/build_morton_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_centralpark_asset_manifest.py` |
| `scripts/stage_morton_assets.py` | §10 の staging | `scripts/stage_centralpark_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.9 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_morton_facts.py`（B が clone して実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の制約に一致し、`check_morton_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_morton_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==240 / motion 配列長==43 / overlay 配列長==30 が非空で実体化していること（EP45 事故回避の必須不変条件）

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_morton_asset_manifest.py --reuse-feasibility
#   → still >=215 / motion >=43 / factory >=240 / distinct 合計 >=498 / first-use >=0.70 / avg-uses/source <=1.4

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_morton_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全240本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-052-morton

# [A-DONE-5] EP39〜EP51 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_morton_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39〜EP51 の十三すべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（正確性制約・ガードレール）★★★

**Michael Morton は【存命・法的に完全に無罪確定】＝彼の無実を事実として断定してよい（court が innocent と宣告・DNA が真犯人を特定）。二人の実在の villain も断定してよい:（1）Mark Alan Norwood＝DNA で特定され両女性の殺害で有罪の真犯人、（2）Ken Anderson＝証拠隠匿が record 上確立し criminal contempt で収監・弁護士資格を返上した検事。被害者 Christine Morton と Debra Baker は【実在の殺害被害者】＝暴行・殺害・現場・遺体を一切描かない（dignity）。3歳の証人 Eric は【最大限の配慮】＝documented な "monster/big mustache/daddy wasn't home" 以上に踏み込まない・襲撃を彼の視点でも一切再現しない・識別可能な子供の顔を作らない。全ての実在人物（Morton/Christine/Eric/Rita/Norwood/Anderson/Bradley/Raley/Morrison/判事）の顔・肖像・likeness を作らない。匿名・非識別の一般人は可。数値（25年・約6年・約5日・約100ヤード・$1.96M 等）は hedged。捏造引用禁止・可読の偽公文書禁止。**

## 1.1 R1/R2（生成ビジュアル全般）

1. **★R-FACE: 匿名・非識別の人物は可／実在人物の likeness は不可。** 匿名の一般人（実在の誰にも似せない・非識別のドラマ化スタンドイン）＝顔・身体を出してよい（§5.11 の H シリーズ・専用 `[HSTYLE]`/`[HNEG]`・§5.12 の thumb_face）。ただし **実在人物の顔・likeness・肖像は作らない**＝Michael Morton・Christine Morton・Eric・Rita Kirkpatrick・Mark Norwood・Ken Anderson・John Bradley・John Raley・Nina Morrison・実在の判事/陪審員を**似せて描かない**。実在人物が示唆される所（夫・検事・弁護士等）は非識別（背向き/影/逆光/目から下でクロップ/ソフト/hands-only）を既定に保つ。**被害者（Christine/Debra）の描写・暴行/殺害/遺体の imagery を一切作らない（不変）。** **3歳の Eric は識別可能な子供の顔にしない**＝小さな手・crayon の "monster" scrawl のみ（象徴レーン限定・§1.1-3）。
2. **可読の偽公文書を再現しない。** 自白調書ではなく本件は「隠された sheriff の file」＝file/report/newspaper/DA memo/DNA lab 数値/日付/案件番号/ID の**可読文字を再現しない**（雰囲気のみ・"blurred into an unreadable smear"）。日付（1986/1987/1988/2011/2013 等）・年齢（3/32）・金額（$1.96M/$5,000/$500）・DNA・服役年数は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。
3. **被害者・暴行・殺害・現場・遺体を一切描かない。** 寝室は **empty bed of absence（cold・無人・遺体なし・血なし・凶器なし）** のみ。"objects piled on the body" を描かない。park/wooded area は abstract treeline のみ。Debra Baker の Austin の家も empty room of absence のみ。**3歳 Eric の目を通した襲撃の再現を作らない。**
4. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **R-MORTON-INNOCENT:** Michael Morton が犯人であるかのような絵・語を作らない。彼は **wrongfully convicted・exonerated・innocent**。"Morton killed / the husband did it（断定として）/ guilty Morton" を書かない（"the state claimed / the theory that the husband did it" の帰属枠は可）。
2. **R-VICTIM:** Christine Morton・Debra Baker に dignity。姿・likeness・遺体・暴行・血・凶器を描かない。"beaten body / bludgeoned corpse / murder scene / blood on the bed / the weapon" を書かない。empty bed/room of absence のみ。
3. **R-CHILD:** Eric（3歳）は最大限の配慮。"child witnessing the attack / the boy sees the murder / traumatized child's face / crying toddler closeup" を書かない。documented account（crayon monster・big mustache・daddy not home）を象徴で。**識別可能な子供の顔を作らない。**
4. **R-VILLAIN-FACT:** Norwood と Anderson は record 上の事実のみ。Norwood＝DNA で特定・両殺害で有罪の drifter（美化しない・lurid にしない）。Anderson＝証拠隠匿・contempt・収監・資格返上（内心の embellish をしない・record の言葉のみ）。**likeness は作らない**（非識別 silhouette）。
5. **R-NUM:** hedged 数値を断定で焼かない。25年（"nearly/about 25"）・Bradley の約6年（"roughly six"）・Anderson の実質約5日（"about five"）・バンダナの約100ヤード（"roughly 100 yards / about a block"）・$1.96M（"roughly"）・$5,000 fine（soft-cite）を**画像に可読で描かない**（AE/figures＝B）。断定表現を書かない。
6. **R-FACE:** **匿名・非識別の人物は可**（§5.11/§5.12）。**実在人物の likeness ゼロ**＝"likeness of <Morton/Christine/Eric/Norwood/Anderson/Bradley/Raley/a real judge> / face of <those names> / recognizable real person / mugshot of a real person / deepfake" を書かない。**匿名一般人（"anonymous / generic / non-identifiable person, face turned or in shadow"）は許可。**
7. **R-READABLE:** 可読の偽公文書（file/report/newspaper/DA memo/DNA数値/日付/案件番号）を描かない。"legible document / readable case file / readable lab report" を正プロンプトに書かない（雰囲気は "unreadable smear"）。
8. **R-DOCHL:** **dochighlight（黒バー/box/underline の figure）を作らない・言及しない。** `tags`/`caption_hint`/`notes`/ファイル名に `dochighlight` の文字列を書かない（grep で 0 を保つ）。
9. **R-QUOTE:** 捏造引用禁止。verbatim は verified 2件（"the other side can't have access to those reports."／"…a more intentionally harmful act…"）のみ・attribution 付き（AE＝B の担当）。画像に可読の引用を描かない。

## 1.3 機械ゲート（`build_morton_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
# 匿名・非識別の人物は許可。実在人物の likeness だけを弾く。
BANNED_PORTRAIT = re.compile(
    r"likeness of (a )?(real|specific|named) person|real[- ]person likeness|"
    r"face of (michael|christine|morton|eric|rita|mark|norwood|ken|anderson|bradley|raley|morrison)|"
    r"likeness of (michael|christine|morton|eric|rita|mark|norwood|ken|anderson|bradley|raley|morrison)|"
    r"recognizable (real person|celebrity)|identifiable real person|"
    r"mugshot of (a )?real person|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"morton (killed|did it|is guilty|murdered|bludgeoned)|the husband did it(?! \(the (state|prosecution|theory))|"
    r"guilty morton|"
    r"(beaten|bludgeoned) (body|corpse|victim|woman|wife)|murder scene|blood on the bed|dead body|the weapon in|"
    r"child (witnessing|seeing) the (attack|murder)|the boy sees the murder|traumatized child'?s face|"
    r"(glorified|heroic|admirable) norwood|lurid|"
    r"legible (document|case file|report|newspaper|lab report)|readable (document|case file|report)|"
    r"nearly (25|twenty-five) years exact|dochighlight",
    re.IGNORECASE)
```

> **許容:** "wrongfully convicted / exonerated / innocent / evidence withheld from the defense / buried file / the blue bandana / the green van / DNA matched another man / Mark Norwood convicted of both murders / prosecutor found in contempt / the Michael Morton Act / anonymous, non-identifiable person, face turned or in shadow / empty bed of absence / crayon monster scrawl"。禁止は「Morton の有罪化」「被害者/暴行/遺体の描写」「Eric の襲撃視点/識別可能な子供顔」「Norwood 美化/lurid」「hedged 数値の断定」「可読の偽公文書」「実在人物 likeness」「dochighlight」。

---

# 2. 台本の語数と尺の確定値（Aが素材点数を積算する根拠）

```
words_total          = 5,350 MEASURED（voice_plan 実測。旧記載 5,326 は −24 のズレ）
narration_seconds    = 1785.803 MEASURED（ffprobe・vc_master_v001.mp3・319 chunks・
                       speech 1681.404s + in-master gaps 104.399s・実測 190.9 wpm）
wpm_used             = 190.9（MEASURED。178 から何も再導出しないこと）
★HOOK-AUDIO 標準（owner・CODEX_B §5.1.2）: Brian の声が 0:00 から鳴る（silent runway なし）。
  narration（COLD OPEN 行から）を 0:00 に置き、hook/opening 秒は加算しない。
total_seconds        = 1794.833（narration 1785.803 + endcard 9.0）= 29:54.8（band 1740–1860 内 ✓）
durationInFrames     = 53,845（★RE-LOCKED 2026-07-28・fps30 = ceil(1785.803*30)=53575 + 270・VO onset 0.0）
   （旧 CaseFilm 式 54,474 は 11.5s の silent runway を前置＝HOOK-AUDIO で除去。
     旧 provisional 54,129 は narration 1795.3 前提＝実測より 9.5s 長い＝音のない絵が 9.5s 出る。使わない）
mean_shot            = 3.100秒/カット（narration 1785.803 / 576。旧 3.117 は provisional 由来）
speech ratio         = 1794.833 / 1681.404 = 1.0675（実測帯 1.04–1.30 内 ✓）
視覚 acts             = 4（+ HOOK/OPENING/ENDING は別区）
Act 語数配分（★MEASURED 2026-07-28・voice_plan 実測）:
  HOOK 117 / OP 140 / ACT1 1,144 / ACT2 1,190 / ACT3 936 / ACT4 1,462 / ENDING 361 = 5,350
  （旧 provisional「ACT1 ~1250 / ACT2 ~1500 最密 / ACT3 ~1000 / ACT4 ~1500」は本文を約 518語 過大に見積もり、
    かつ最密幕を誤っていた。★実測の最密は ACT4（1,462語・477.4s）、次が ACT2（1,190語・375.5s）。
    このテーブルから素材密度を割り付けた箇所は再配分すること）
```

**Aにとっての意味は1つ:** > **総カット 576 / distinct 498 / 初出 86.46% = still 215 + factory 240 + motion 43。**（§3 で積算）

> **注意（命名差）:** 視覚 act は **0=HOOK/OPENING, 1=ACT I, 2=ACT II, 3=ACT III, 4=ACT IV, 5=ENDING**（6値）。**still は 215 本の固有プロンプトを持つ**ため、still の資産 ID は **S001..S215**（1プロンプト＝1枚）。`covers_scene_id` は still 資産 ID 空間（S001..S215）を指す（§7.3）。

---

# 3. ★素材構成の確定値（この値で調達する・勝手に変えない）

## 3.1 内訳（★勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **215枚** | 250カット | 1.163回(≤2) | **215本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **240本** | 240カット | **各1回(1)** | 在庫11,000本超＋stock 74本から選抜（§7）・全点目視・EP39〜51 と sha256 被りゼロ |
| **i2v モーション** | **43本** | 86カット | 各2回(≤2) | 43本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **498点** | **576カット** | | |
| 合成レイヤー（particle/light/vfx） | 30本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |
| サムネ emotive-face（thumb_face） | 3枚 | — | 本編カットに出ない | **distinct/cuts に数えない**（§5.12・thumbnail 専用） |

**SDXL の生成バッチ（本編カットに出ない i2v 種・thumb_face を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **215枚** | 215プロンプト × 1枚 |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **43枚** | 43種プロンプト × 1枚 |
| サムネ face（`role:"thumb_face"`・§5.12） | **3枚** | 3プロンプト × 1枚 |
| **SDXL 生成バッチ合計** | **215 + 43 + 3 = 261枚（各1回）** | **variants 指定なし（＝1枚）** |

> **本編サムネの背景 anchor は body 215枚から4枚を `also_thumb:true` で流用選抜**（§4.3a）。**emotive-face（前景の顔）は §5.12 の thumb_face 3枚**（CTR §4A・B が `MortonThumbnails.tsx` で face＋hook text を合成）。**role=thumb / still_thumb を作らない。**

## 3.2 幕別配分（★still は確定・factory/i2v は目安。合計だけが確定）

| 区間(act) | still（S番号・確定） | factory（目安） | i2v（確定合計43） | thumb anchor |
|---|---|---|---|---|
| HOOK+OPENING (0) | **15**（S001–S015） | 12 | 3（M01–M03） | S001 |
| ACT1「The Husband Did It」(1) | **45**（S016–S060） | 45 | 8（M04–M11） | S060 |
| ACT2「The Trial」(2)（engine・最密） | **55**（S061–S115） | 40 | 9（M12–M20） | — |
| ACT3「Twenty-Five Years」(3) | **40**（S116–S155） | 50 | 8（M21–M28） | S155 |
| ACT4「What the Bandana Knew」(4)（climax・最密②） | **45**（S156–S200） | 45 | 11（M29–M39） | S170 |
| ENDING (5) | **15**（S201–S215） | 15 | 4（M40–M43） | — |
| 繋ぎ（covers_scene_id:null） | — | 33 | — | — |
| **合計** | **215** | **240** | **43** | **4** |

> **still の per-act 数（15/45/55/40/45/15＝215）は確定**（§5 の motif ライブラリがこの配分で組まれている）。ACT2（隠された証拠の engine）が最厚55、ACT4（bandana DNA cascade）は climax で45＋motion 最多11。**幕別の factory/i2v 内訳は目安値**（合計 240 / 43 のみ確定）。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 576 = still 250 + factory 240 + i2v 86
[2] 平均ショット長 = narration 1785.803（MEASURED）/ 576 = 3.100秒/カット  ✓ (≤7.0)   ［旧 1795.3 → 3.117］
[3] 静止画占有率(check_animation_mix) = 250/576 = 43.40%  ✓ ≤45%（余裕 1.60%pt）
[4] motion coverage = (240+86)/576 = 326/576 = 56.60%     ✓ ≥45%
[5] per-asset 上限: still 250/215=1.163(≤2) / factory 240/240=1.0(≤1) / motion 86/43=2.0(≤2)  ✓
[6] first-use share = 498/576 = 0.8646                    ✓ ≥0.70
[7] avg uses/source = 576/498 = 1.157                     ✓ ≤1.4（EP49 は 1.8 で flag された）
[8] factory 下限 = 1785.803（MEASURED）/30 = 59.5 → ≥60本。設計値 240本 ✓（still-share≤0.45 を守る）
```

> **★ MEASURED 再検算（2026-07-28）:** narration 1795.3 → **1785.803**（−9.5s）。[1][3][4][5][6][7] は「点数の比」なので不変。[2][8] のみ再導出済み。結論（still-share 43.40% ≤45 / first-use 0.8646 ≥0.70 / avg-uses 1.157 ≤1.4）は全て不変。

> **[3] の余裕は 1.60%pt。** still が215本を割ったら §6.3 の再生成で回復させ、**still-cut 250 を増やさない**（B側の shotlist が250で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-052-morton/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `morton_assets.v1`（固定文字列）
**生産者:** `scripts/build_morton_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を一字一致。** role enum は **`body | i2v_source | thumb_face | reject` のみ**。also_thumb は body still **ちょうど4枚**。thumb_face は **ちょうど3枚**。overlay は **ちょうど30本**。

## 4.1 スキーマ（`morton_assets.v1`）

```jsonc
{
  "schema_version": "morton_assets.v1",
  "episode_id": "PD-2026-052-morton",
  "slug": "morton",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_morton_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 215,        // ==215
    "still_i2v_source": 43,   // ==43
    "motion": 43,             // ==43
    "factory": 240,           // ==240
    "overlay": 30,            // ==30（distinct 素材に数えない）
    "thumb_face": 3           // ==3（thumbnail 専用・distinct/cuts に数えない）
  },
  "stills":  [ /* §4.3: body 215 (MOR-S001..S215) + i2v_source 43 (MOR-MS01..MS43) + thumb_face 3 (MOR-T01..T03) */ ],
  "motion":  [ /* §4.5: MOR-M01..M43 全43本・public_path 必須（★非空） */ ],
  "factory": [ /* §4.4: 240本・public_path 必須（★非空・EP45事故回避の核心） */ ],
  "overlay": [ /* §4.6: 30本 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例・★depth_path なし）

```jsonc
{
  "asset_id": "MOR-S001",                 // body: ^MOR-S\d{3}$（001..215）/ i2v種: ^MOR-MS\d{2}$ / thumb: ^MOR-T\d{2}$
  "scene_id": "S001",                     // still 資産 ID 空間（§5.9 のプロンプト行に対応・S001..S215）
  "role": "body",                         // body|i2v_source|thumb_face|reject
  "also_thumb": false,                    // body から4枚だけ true（§4.3a・追加生成しない）
  "act": 0,                               // 0=HOOK/OPENING, 1..4=ACT I..IV, 5=ENDING
  "path": "H:/pd-media/assets/ai/morton/S001.png",
  "public_path": "morton/img/S001.png",   // role=="body" のみ非null / i2v種・thumb_face は null
  "width": 3840, "height": 2160,          // 長辺>=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 22.0,
  "tags": ["child_hand","crayon_monster","cold_blue_edge","buried","symbolic","no_face","no_readable_text"],
  "caption_hint": "a small child's hand and an abstract crayon scrawl of a monster found by a single cold evidence-blue edge, non-graphic, no identifiable child, no readable text",
  "seed": 0, "model": "juggernautXL_ragnarokBy",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
         "has_identifiable_real_person": false, "has_human_body": false,
         "has_identifiable_face": false, "has_victim_or_violence": false, "notes": ""}
  // ★depth_path は無い（本作は depth treatment 不使用・§6.4）。
  // ★reject トリガは has_readable_text / has_identifiable_real_person / has_victim_or_violence のみ。
  //   匿名人体（has_human_body:true）は reject しない。
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="morton_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 215 / i2v_source 43 / motion 43 / factory 240 / overlay 30 / thumb_face 3）に**一致**
3. 全 `path`/`public_path` がディスクに実在（**depth_path は要求しない**）
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `public_path` が非null かつ実在（**depth_path は不要**）。`role=="i2v_source"`/`role=="thumb_face"` は `public_path==null`
7. **★reject 条件:** `qc.has_readable_text==true` **または** `qc.has_identifiable_real_person==true` **または** `qc.has_victim_or_violence==true` は `role=="reject"`。**`qc.has_human_body==true` は reject 条件ではない**（匿名人体は可）。`qc.has_identifiable_face` は「実在人物として識別可能な顔」を意味する（匿名・非識別の顔は可）。H シリーズ（§5.11）・thumb_face（§5.12）は `has_human_body:true`/`has_identifiable_real_person:false`/`has_readable_text:false`/`has_victim_or_violence:false`
8. `role=="i2v_source"` は `role=="body"`/`role=="thumb_face"` と**同一 asset_id を共有しない**（i2v_source は `^MOR-MS\d{2}$` / thumb_face は `^MOR-T\d{2}$`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39〜EP51（十三話）の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど4**、かつ `scene_id` 集合が §4.3a の4枚集合と完全一致（**CODEX_B と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|thumb_face|reject のみ）
16. `overlay` 配列長が**ちょうど30**
17. ★**`factory` 配列長==240 かつ全エントリ `public_path` が非空**（EP45 事故回避）
18. ★**`motion` 配列長==43 かつ全エントリ `public_path` が非空**（同上）
19. **★どの still/motion にも `depth_path` キーを要求しない・生成しない**（depth treatment 不使用・§6.4）

`--reuse-feasibility` では §3.3 [5][6][7][8] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 215枚（S001..S215）= §5.9 の215プロンプトの生成物。各1枚。
2. i2v_source 43枚（MS01..MS43 / 種画像 M01_src..M43_src）= §8.1a の43種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. thumb_face 3枚（T01..T03 / T01_face..T03_face）= §5.12 の3プロンプトの生成物。public_path==null。
4. also_thumb : body のうち §4.3a の4枚に true（追加生成しない）
5. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

### 4.3a ★also_thumb 集合（ちょうど4枚・CODEX_B と一字一致必須）

```
{ MOR-S001 (child's hand + crayon "monster" scrawl — the hook signature),
  MOR-S060 (a strip of blue cloth in a dark evidence drawer — the buried truth),
  MOR-S155 (a single cell window with seasons crossing — the 25-year anchor),
  MOR-S170 (cold evidence-blue DNA gel bands flooding the frame — the Act IV hinge) }
```

> ★この4集合は §5 の該当 S番号に必ず該当 motif を置くこと（§5 の motif ライブラリで anchor 指定済み）。**前景の emotive face は §5.12 の thumb_face（T01–T03）＝これらは背景 anchor。**

## 4.4 ★`factory[]` 全240エントリ（★必ず実体化・public_path 非空。EP45事故回避の核心）

> `select_morton_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id）/`path`（`H:/pd-media/assets/factory/...` or `H:/pd-media/assets/stock/...`）/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`origin`(`factory`|`stock`)/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。** 各 public_path は `morton/factory/F0NN_<subtype>.mp4`。`type:"backgrounds"`, `kind:"video"`。**subtype の `_02`/`_03` は「同一検索テーマの別クリップ」の意で、別 sha256・別素材（同一ファイルの重複ではない）。**

```jsonc
// HOOK+OPENING (act 0) — 12
{ "public_path":"morton/factory/F001_cold_evidence_room_dim.mp4", "act":0, "covers_scene_id":"S005", "subtype":"cold_evidence_room_dim" }
{ "public_path":"morton/factory/F002_records_archive_shelves.mp4", "act":0, "covers_scene_id":"S008", "subtype":"records_archive_shelves" }
{ "public_path":"morton/factory/F003_file_cabinet_room_dim.mp4", "act":0, "covers_scene_id":null, "subtype":"file_cabinet_room_dim" }
{ "public_path":"morton/factory/F004_sheriff_office_interior_dim.mp4", "act":0, "covers_scene_id":null, "subtype":"sheriff_office_interior_dim" }
{ "public_path":"morton/factory/F005_dark_institutional_room_cold.mp4", "act":0, "covers_scene_id":null, "subtype":"dark_institutional_room_cold" }
{ "public_path":"morton/factory/F006_unlit_records_hall.mp4", "act":0, "covers_scene_id":null, "subtype":"unlit_records_hall" }
{ "public_path":"morton/factory/F007_evidence_locker_shelves.mp4", "act":0, "covers_scene_id":null, "subtype":"evidence_locker_shelves" }
{ "public_path":"morton/factory/F008_county_building_night.mp4", "act":0, "covers_scene_id":null, "subtype":"county_building_night" }
{ "public_path":"morton/factory/F009_cold_evidence_room_dim_02.mp4", "act":0, "covers_scene_id":null, "subtype":"cold_evidence_room_dim_02" }
{ "public_path":"morton/factory/F010_records_archive_shelves_02.mp4", "act":0, "covers_scene_id":null, "subtype":"records_archive_shelves_02" }
{ "public_path":"morton/factory/F011_file_cabinet_room_dim_02.mp4", "act":0, "covers_scene_id":null, "subtype":"file_cabinet_room_dim_02" }
{ "public_path":"morton/factory/F012_sheriff_office_interior_dim_02.mp4", "act":0, "covers_scene_id":null, "subtype":"sheriff_office_interior_dim_02" }
// ACT1 The Husband Did It (act 1) — 45
{ "public_path":"morton/factory/F013_texas_suburban_house_1986_day.mp4", "act":1, "covers_scene_id":"S016", "subtype":"texas_suburban_house_1986_day" }
{ "public_path":"morton/factory/F014_quiet_suburban_street_dawn.mp4", "act":1, "covers_scene_id":"S024", "subtype":"quiet_suburban_street_dawn" }
{ "public_path":"morton/factory/F015_supermarket_exterior_day.mp4", "act":1, "covers_scene_id":"S027", "subtype":"supermarket_exterior_day" }
{ "public_path":"morton/factory/F016_empty_bedroom_cold_light.mp4", "act":1, "covers_scene_id":"S030", "subtype":"empty_bedroom_cold_light" }
{ "public_path":"morton/factory/F017_police_lights_night_cold.mp4", "act":1, "covers_scene_id":"S036", "subtype":"police_lights_night_cold" }
{ "public_path":"morton/factory/F018_texas_hill_country_landscape.mp4", "act":1, "covers_scene_id":"S042", "subtype":"texas_hill_country_landscape" }
{ "public_path":"morton/factory/F019_wooded_treeline_behind_house.mp4", "act":1, "covers_scene_id":"S057", "subtype":"wooded_treeline_behind_house" }
{ "public_path":"morton/factory/F020_suburban_cul_de_sac_dusk.mp4", "act":1, "covers_scene_id":null, "subtype":"suburban_cul_de_sac_dusk" }
{ "public_path":"morton/factory/F021_dry_lawn_yard_day.mp4", "act":1, "covers_scene_id":null, "subtype":"dry_lawn_yard_day" }
{ "public_path":"morton/factory/F022_texas_sky_dusk_wide.mp4", "act":1, "covers_scene_id":null, "subtype":"texas_sky_dusk_wide" }
{ "public_path":"morton/factory/F023_neighborhood_porch_dawn.mp4", "act":1, "covers_scene_id":null, "subtype":"neighborhood_porch_dawn" }
{ "public_path":"morton/factory/F024_kitchen_window_early_light.mp4", "act":1, "covers_scene_id":null, "subtype":"kitchen_window_early_light" }
{ "public_path":"morton/factory/F025_driveway_predawn_dark.mp4", "act":1, "covers_scene_id":null, "subtype":"driveway_predawn_dark" }
{ "public_path":"morton/factory/F026_grocery_aisle_interior_cold.mp4", "act":1, "covers_scene_id":null, "subtype":"grocery_aisle_interior_cold" }
{ "public_path":"morton/factory/F027_suburban_street_day_1980s.mp4", "act":1, "covers_scene_id":null, "subtype":"suburban_street_day_1980s" }
{ "public_path":"morton/factory/F028_hallway_home_interior_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"hallway_home_interior_dim" }
{ "public_path":"morton/factory/F029_patrol_car_exterior_cold.mp4", "act":1, "covers_scene_id":null, "subtype":"patrol_car_exterior_cold" }
{ "public_path":"morton/factory/F030_wind_in_dry_grass.mp4", "act":1, "covers_scene_id":null, "subtype":"wind_in_dry_grass" }
{ "public_path":"morton/factory/F031_texas_suburban_house_1986_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"texas_suburban_house_1986_day_02" }
{ "public_path":"morton/factory/F032_quiet_suburban_street_dawn_02.mp4", "act":1, "covers_scene_id":null, "subtype":"quiet_suburban_street_dawn_02" }
{ "public_path":"morton/factory/F033_supermarket_exterior_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"supermarket_exterior_day_02" }
{ "public_path":"morton/factory/F034_empty_bedroom_cold_light_02.mp4", "act":1, "covers_scene_id":null, "subtype":"empty_bedroom_cold_light_02" }
{ "public_path":"morton/factory/F035_police_lights_night_cold_02.mp4", "act":1, "covers_scene_id":null, "subtype":"police_lights_night_cold_02" }
{ "public_path":"morton/factory/F036_texas_hill_country_landscape_02.mp4", "act":1, "covers_scene_id":null, "subtype":"texas_hill_country_landscape_02" }
{ "public_path":"morton/factory/F037_wooded_treeline_behind_house_02.mp4", "act":1, "covers_scene_id":null, "subtype":"wooded_treeline_behind_house_02" }
{ "public_path":"morton/factory/F038_suburban_cul_de_sac_dusk_02.mp4", "act":1, "covers_scene_id":null, "subtype":"suburban_cul_de_sac_dusk_02" }
{ "public_path":"morton/factory/F039_dry_lawn_yard_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"dry_lawn_yard_day_02" }
{ "public_path":"morton/factory/F040_texas_sky_dusk_wide_02.mp4", "act":1, "covers_scene_id":null, "subtype":"texas_sky_dusk_wide_02" }
{ "public_path":"morton/factory/F041_neighborhood_porch_dawn_02.mp4", "act":1, "covers_scene_id":null, "subtype":"neighborhood_porch_dawn_02" }
{ "public_path":"morton/factory/F042_kitchen_window_early_light_02.mp4", "act":1, "covers_scene_id":null, "subtype":"kitchen_window_early_light_02" }
{ "public_path":"morton/factory/F043_driveway_predawn_dark_02.mp4", "act":1, "covers_scene_id":null, "subtype":"driveway_predawn_dark_02" }
{ "public_path":"morton/factory/F044_grocery_aisle_interior_cold_02.mp4", "act":1, "covers_scene_id":null, "subtype":"grocery_aisle_interior_cold_02" }
{ "public_path":"morton/factory/F045_suburban_street_day_1980s_02.mp4", "act":1, "covers_scene_id":null, "subtype":"suburban_street_day_1980s_02" }
{ "public_path":"morton/factory/F046_hallway_home_interior_dim_02.mp4", "act":1, "covers_scene_id":null, "subtype":"hallway_home_interior_dim_02" }
{ "public_path":"morton/factory/F047_patrol_car_exterior_cold_02.mp4", "act":1, "covers_scene_id":null, "subtype":"patrol_car_exterior_cold_02" }
{ "public_path":"morton/factory/F048_wind_in_dry_grass_02.mp4", "act":1, "covers_scene_id":null, "subtype":"wind_in_dry_grass_02" }
{ "public_path":"morton/factory/F049_texas_suburban_house_1986_day_03.mp4", "act":1, "covers_scene_id":null, "subtype":"texas_suburban_house_1986_day_03" }
{ "public_path":"morton/factory/F050_quiet_suburban_street_dawn_03.mp4", "act":1, "covers_scene_id":null, "subtype":"quiet_suburban_street_dawn_03" }
{ "public_path":"morton/factory/F051_empty_bedroom_cold_light_03.mp4", "act":1, "covers_scene_id":null, "subtype":"empty_bedroom_cold_light_03" }
{ "public_path":"morton/factory/F052_police_lights_night_cold_03.mp4", "act":1, "covers_scene_id":null, "subtype":"police_lights_night_cold_03" }
{ "public_path":"morton/factory/F053_texas_hill_country_landscape_03.mp4", "act":1, "covers_scene_id":null, "subtype":"texas_hill_country_landscape_03" }
{ "public_path":"morton/factory/F054_wooded_treeline_behind_house_03.mp4", "act":1, "covers_scene_id":null, "subtype":"wooded_treeline_behind_house_03" }
{ "public_path":"morton/factory/F055_supermarket_exterior_day_03.mp4", "act":1, "covers_scene_id":null, "subtype":"supermarket_exterior_day_03" }
{ "public_path":"morton/factory/F056_texas_sky_dusk_wide_03.mp4", "act":1, "covers_scene_id":null, "subtype":"texas_sky_dusk_wide_03" }
{ "public_path":"morton/factory/F057_suburban_street_day_1980s_03.mp4", "act":1, "covers_scene_id":null, "subtype":"suburban_street_day_1980s_03" }
// ACT2 The Trial (act 2) — 40
{ "public_path":"morton/factory/F058_williamson_county_courthouse.mp4", "act":2, "covers_scene_id":"S061", "subtype":"williamson_county_courthouse" }
{ "public_path":"morton/factory/F059_courthouse_marble_columns.mp4", "act":2, "covers_scene_id":"S065", "subtype":"courthouse_marble_columns" }
{ "public_path":"morton/factory/F060_empty_courtroom_wide.mp4", "act":2, "covers_scene_id":"S069", "subtype":"empty_courtroom_wide" }
{ "public_path":"morton/factory/F061_jury_box_empty_cold.mp4", "act":2, "covers_scene_id":"S073", "subtype":"jury_box_empty_cold" }
{ "public_path":"morton/factory/F062_evidence_locker_shelves_cold.mp4", "act":2, "covers_scene_id":"S083", "subtype":"evidence_locker_shelves_cold" }
{ "public_path":"morton/factory/F063_file_drawers_closing_dim.mp4", "act":2, "covers_scene_id":"S088", "subtype":"file_drawers_closing_dim" }
{ "public_path":"morton/factory/F064_da_office_corridor_cold.mp4", "act":2, "covers_scene_id":"S109", "subtype":"da_office_corridor_cold" }
{ "public_path":"morton/factory/F065_document_archive_illegible.mp4", "act":2, "covers_scene_id":null, "subtype":"document_archive_illegible" }
{ "public_path":"morton/factory/F066_courthouse_dome_texas.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_dome_texas" }
{ "public_path":"morton/factory/F067_records_room_shelves_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"records_room_shelves_dim" }
{ "public_path":"morton/factory/F068_courthouse_hallway_marble.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_hallway_marble" }
{ "public_path":"morton/factory/F069_witness_stand_empty.mp4", "act":2, "covers_scene_id":null, "subtype":"witness_stand_empty" }
{ "public_path":"morton/factory/F070_gavel_bench_empty_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"gavel_bench_empty_cold" }
{ "public_path":"morton/factory/F071_law_books_shelf_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"law_books_shelf_dim" }
{ "public_path":"morton/factory/F072_courthouse_steps_exterior.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_steps_exterior" }
{ "public_path":"morton/factory/F073_williamson_county_courthouse_02.mp4", "act":2, "covers_scene_id":null, "subtype":"williamson_county_courthouse_02" }
{ "public_path":"morton/factory/F074_courthouse_marble_columns_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_marble_columns_02" }
{ "public_path":"morton/factory/F075_empty_courtroom_wide_02.mp4", "act":2, "covers_scene_id":null, "subtype":"empty_courtroom_wide_02" }
{ "public_path":"morton/factory/F076_jury_box_empty_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"jury_box_empty_cold_02" }
{ "public_path":"morton/factory/F077_evidence_locker_shelves_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"evidence_locker_shelves_cold_02" }
{ "public_path":"morton/factory/F078_file_drawers_closing_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"file_drawers_closing_dim_02" }
{ "public_path":"morton/factory/F079_da_office_corridor_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"da_office_corridor_cold_02" }
{ "public_path":"morton/factory/F080_document_archive_illegible_02.mp4", "act":2, "covers_scene_id":null, "subtype":"document_archive_illegible_02" }
{ "public_path":"morton/factory/F081_courthouse_dome_texas_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_dome_texas_02" }
{ "public_path":"morton/factory/F082_records_room_shelves_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"records_room_shelves_dim_02" }
{ "public_path":"morton/factory/F083_courthouse_hallway_marble_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_hallway_marble_02" }
{ "public_path":"morton/factory/F084_witness_stand_empty_02.mp4", "act":2, "covers_scene_id":null, "subtype":"witness_stand_empty_02" }
{ "public_path":"morton/factory/F085_gavel_bench_empty_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"gavel_bench_empty_cold_02" }
{ "public_path":"morton/factory/F086_law_books_shelf_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"law_books_shelf_dim_02" }
{ "public_path":"morton/factory/F087_courthouse_steps_exterior_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_steps_exterior_02" }
{ "public_path":"morton/factory/F088_williamson_county_courthouse_03.mp4", "act":2, "covers_scene_id":null, "subtype":"williamson_county_courthouse_03" }
{ "public_path":"morton/factory/F089_empty_courtroom_wide_03.mp4", "act":2, "covers_scene_id":null, "subtype":"empty_courtroom_wide_03" }
{ "public_path":"morton/factory/F090_evidence_locker_shelves_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"evidence_locker_shelves_cold_03" }
{ "public_path":"morton/factory/F091_file_drawers_closing_dim_03.mp4", "act":2, "covers_scene_id":null, "subtype":"file_drawers_closing_dim_03" }
{ "public_path":"morton/factory/F092_courthouse_marble_columns_03.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_marble_columns_03" }
{ "public_path":"morton/factory/F093_records_room_shelves_dim_03.mp4", "act":2, "covers_scene_id":null, "subtype":"records_room_shelves_dim_03" }
{ "public_path":"morton/factory/F094_da_office_corridor_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"da_office_corridor_cold_03" }
{ "public_path":"morton/factory/F095_courthouse_hallway_marble_03.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_hallway_marble_03" }
{ "public_path":"morton/factory/F096_gavel_bench_empty_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"gavel_bench_empty_cold_03" }
{ "public_path":"morton/factory/F097_courthouse_dome_texas_03.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_dome_texas_03" }
// ACT3 Twenty-Five Years (act 3) — 50
{ "public_path":"morton/factory/F098_texas_prison_exterior_day.mp4", "act":3, "covers_scene_id":"S116", "subtype":"texas_prison_exterior_day" }
{ "public_path":"morton/factory/F099_prison_fence_razor_distant.mp4", "act":3, "covers_scene_id":"S119", "subtype":"prison_fence_razor_distant" }
{ "public_path":"morton/factory/F100_cell_block_window_exterior.mp4", "act":3, "covers_scene_id":"S130", "subtype":"cell_block_window_exterior" }
{ "public_path":"morton/factory/F101_long_institutional_corridor.mp4", "act":3, "covers_scene_id":"S138", "subtype":"long_institutional_corridor" }
{ "public_path":"morton/factory/F102_lawyer_office_desk_lamp.mp4", "act":3, "covers_scene_id":"S142", "subtype":"lawyer_office_desk_lamp" }
{ "public_path":"morton/factory/F103_law_library_stacks_dim.mp4", "act":3, "covers_scene_id":"S145", "subtype":"law_library_stacks_dim" }
{ "public_path":"morton/factory/F104_dna_lab_exterior_cold.mp4", "act":3, "covers_scene_id":"S152", "subtype":"dna_lab_exterior_cold" }
{ "public_path":"morton/factory/F105_prison_yard_empty_nonsensational.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_yard_empty_nonsensational" }
{ "public_path":"morton/factory/F106_seasons_over_building_timelapse.mp4", "act":3, "covers_scene_id":null, "subtype":"seasons_over_building_timelapse" }
{ "public_path":"morton/factory/F107_cold_sky_slow_clouds.mp4", "act":3, "covers_scene_id":null, "subtype":"cold_sky_slow_clouds" }
{ "public_path":"morton/factory/F108_concrete_wall_shadow_move.mp4", "act":3, "covers_scene_id":null, "subtype":"concrete_wall_shadow_move" }
{ "public_path":"morton/factory/F109_courthouse_steps_day_appeal.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_steps_day_appeal" }
{ "public_path":"morton/factory/F110_barrier_gate_locked_cold.mp4", "act":3, "covers_scene_id":null, "subtype":"barrier_gate_locked_cold" }
{ "public_path":"morton/factory/F111_desk_files_stack_lamp.mp4", "act":3, "covers_scene_id":null, "subtype":"desk_files_stack_lamp" }
{ "public_path":"morton/factory/F112_lab_bench_equipment_cold.mp4", "act":3, "covers_scene_id":null, "subtype":"lab_bench_equipment_cold" }
{ "public_path":"morton/factory/F113_texas_prison_exterior_day_02.mp4", "act":3, "covers_scene_id":null, "subtype":"texas_prison_exterior_day_02" }
{ "public_path":"morton/factory/F114_prison_fence_razor_distant_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_fence_razor_distant_02" }
{ "public_path":"morton/factory/F115_cell_block_window_exterior_02.mp4", "act":3, "covers_scene_id":null, "subtype":"cell_block_window_exterior_02" }
{ "public_path":"morton/factory/F116_long_institutional_corridor_02.mp4", "act":3, "covers_scene_id":null, "subtype":"long_institutional_corridor_02" }
{ "public_path":"morton/factory/F117_lawyer_office_desk_lamp_02.mp4", "act":3, "covers_scene_id":null, "subtype":"lawyer_office_desk_lamp_02" }
{ "public_path":"morton/factory/F118_law_library_stacks_dim_02.mp4", "act":3, "covers_scene_id":null, "subtype":"law_library_stacks_dim_02" }
{ "public_path":"morton/factory/F119_dna_lab_exterior_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"dna_lab_exterior_cold_02" }
{ "public_path":"morton/factory/F120_prison_yard_empty_nonsensational_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_yard_empty_nonsensational_02" }
{ "public_path":"morton/factory/F121_seasons_over_building_timelapse_02.mp4", "act":3, "covers_scene_id":null, "subtype":"seasons_over_building_timelapse_02" }
{ "public_path":"morton/factory/F122_cold_sky_slow_clouds_02.mp4", "act":3, "covers_scene_id":null, "subtype":"cold_sky_slow_clouds_02" }
{ "public_path":"morton/factory/F123_concrete_wall_shadow_move_02.mp4", "act":3, "covers_scene_id":null, "subtype":"concrete_wall_shadow_move_02" }
{ "public_path":"morton/factory/F124_courthouse_steps_day_appeal_02.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_steps_day_appeal_02" }
{ "public_path":"morton/factory/F125_barrier_gate_locked_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"barrier_gate_locked_cold_02" }
{ "public_path":"morton/factory/F126_desk_files_stack_lamp_02.mp4", "act":3, "covers_scene_id":null, "subtype":"desk_files_stack_lamp_02" }
{ "public_path":"morton/factory/F127_lab_bench_equipment_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"lab_bench_equipment_cold_02" }
{ "public_path":"morton/factory/F128_texas_prison_exterior_day_03.mp4", "act":3, "covers_scene_id":null, "subtype":"texas_prison_exterior_day_03" }
{ "public_path":"morton/factory/F129_cell_block_window_exterior_03.mp4", "act":3, "covers_scene_id":null, "subtype":"cell_block_window_exterior_03" }
{ "public_path":"morton/factory/F130_long_institutional_corridor_03.mp4", "act":3, "covers_scene_id":null, "subtype":"long_institutional_corridor_03" }
{ "public_path":"morton/factory/F131_lawyer_office_desk_lamp_03.mp4", "act":3, "covers_scene_id":null, "subtype":"lawyer_office_desk_lamp_03" }
{ "public_path":"morton/factory/F132_dna_lab_exterior_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"dna_lab_exterior_cold_03" }
{ "public_path":"morton/factory/F133_prison_fence_razor_distant_03.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_fence_razor_distant_03" }
{ "public_path":"morton/factory/F134_seasons_over_building_timelapse_03.mp4", "act":3, "covers_scene_id":null, "subtype":"seasons_over_building_timelapse_03" }
{ "public_path":"morton/factory/F135_prison_yard_empty_nonsensational_03.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_yard_empty_nonsensational_03" }
{ "public_path":"morton/factory/F136_cold_sky_slow_clouds_03.mp4", "act":3, "covers_scene_id":null, "subtype":"cold_sky_slow_clouds_03" }
{ "public_path":"morton/factory/F137_law_library_stacks_dim_03.mp4", "act":3, "covers_scene_id":null, "subtype":"law_library_stacks_dim_03" }
{ "public_path":"morton/factory/F138_concrete_wall_shadow_move_03.mp4", "act":3, "covers_scene_id":null, "subtype":"concrete_wall_shadow_move_03" }
{ "public_path":"morton/factory/F139_desk_files_stack_lamp_03.mp4", "act":3, "covers_scene_id":null, "subtype":"desk_files_stack_lamp_03" }
{ "public_path":"morton/factory/F140_lab_bench_equipment_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"lab_bench_equipment_cold_03" }
{ "public_path":"morton/factory/F141_texas_prison_exterior_day_04.mp4", "act":3, "covers_scene_id":null, "subtype":"texas_prison_exterior_day_04" }
{ "public_path":"morton/factory/F142_cell_block_window_exterior_04.mp4", "act":3, "covers_scene_id":null, "subtype":"cell_block_window_exterior_04" }
{ "public_path":"morton/factory/F143_long_institutional_corridor_04.mp4", "act":3, "covers_scene_id":null, "subtype":"long_institutional_corridor_04" }
{ "public_path":"morton/factory/F144_cold_sky_slow_clouds_04.mp4", "act":3, "covers_scene_id":null, "subtype":"cold_sky_slow_clouds_04" }
{ "public_path":"morton/factory/F145_lawyer_office_desk_lamp_04.mp4", "act":3, "covers_scene_id":null, "subtype":"lawyer_office_desk_lamp_04" }
{ "public_path":"morton/factory/F146_dna_lab_exterior_cold_04.mp4", "act":3, "covers_scene_id":null, "subtype":"dna_lab_exterior_cold_04" }
{ "public_path":"morton/factory/F147_prison_yard_empty_nonsensational_04.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_yard_empty_nonsensational_04" }
// ACT4 What the Bandana Knew (act 4) — 45
{ "public_path":"morton/factory/F148_dna_lab_interior_cold.mp4", "act":4, "covers_scene_id":"S156", "subtype":"dna_lab_interior_cold" }
{ "public_path":"morton/factory/F149_gel_electrophoresis_equipment.mp4", "act":4, "covers_scene_id":"S166", "subtype":"gel_electrophoresis_equipment" }
{ "public_path":"morton/factory/F150_evidence_cloth_on_table_abstract.mp4", "act":4, "covers_scene_id":"S162", "subtype":"evidence_cloth_on_table_abstract" }
{ "public_path":"morton/factory/F151_prison_gate_opening_day.mp4", "act":4, "covers_scene_id":"S185", "subtype":"prison_gate_opening_day" }
{ "public_path":"morton/factory/F152_courthouse_steps_day_release.mp4", "act":4, "covers_scene_id":"S186", "subtype":"courthouse_steps_day_release" }
{ "public_path":"morton/factory/F153_empty_austin_room_absence.mp4", "act":4, "covers_scene_id":"S180", "subtype":"empty_austin_room_absence" }
{ "public_path":"morton/factory/F154_texas_capitol_exterior.mp4", "act":4, "covers_scene_id":"S196", "subtype":"texas_capitol_exterior" }
{ "public_path":"morton/factory/F155_legislative_chamber_empty.mp4", "act":4, "covers_scene_id":"S198", "subtype":"legislative_chamber_empty" }
{ "public_path":"morton/factory/F156_warm_texas_dawn_sky.mp4", "act":4, "covers_scene_id":"S189", "subtype":"warm_texas_dawn_sky" }
{ "public_path":"morton/factory/F157_open_road_home_dawn.mp4", "act":4, "covers_scene_id":null, "subtype":"open_road_home_dawn" }
{ "public_path":"morton/factory/F158_lab_microscope_slides_cold.mp4", "act":4, "covers_scene_id":null, "subtype":"lab_microscope_slides_cold" }
{ "public_path":"morton/factory/F159_courthouse_columns_day_bright.mp4", "act":4, "covers_scene_id":null, "subtype":"courthouse_columns_day_bright" }
{ "public_path":"morton/factory/F160_capitol_dome_texas_day.mp4", "act":4, "covers_scene_id":null, "subtype":"capitol_dome_texas_day" }
{ "public_path":"morton/factory/F161_horizon_field_dawn_warm.mp4", "act":4, "covers_scene_id":null, "subtype":"horizon_field_dawn_warm" }
{ "public_path":"morton/factory/F162_prison_exterior_receding_day.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_exterior_receding_day" }
{ "public_path":"morton/factory/F163_dna_lab_interior_cold_02.mp4", "act":4, "covers_scene_id":null, "subtype":"dna_lab_interior_cold_02" }
{ "public_path":"morton/factory/F164_gel_electrophoresis_equipment_02.mp4", "act":4, "covers_scene_id":null, "subtype":"gel_electrophoresis_equipment_02" }
{ "public_path":"morton/factory/F165_evidence_cloth_on_table_abstract_02.mp4", "act":4, "covers_scene_id":null, "subtype":"evidence_cloth_on_table_abstract_02" }
{ "public_path":"morton/factory/F166_prison_gate_opening_day_02.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_gate_opening_day_02" }
{ "public_path":"morton/factory/F167_courthouse_steps_day_release_02.mp4", "act":4, "covers_scene_id":null, "subtype":"courthouse_steps_day_release_02" }
{ "public_path":"morton/factory/F168_empty_austin_room_absence_02.mp4", "act":4, "covers_scene_id":null, "subtype":"empty_austin_room_absence_02" }
{ "public_path":"morton/factory/F169_texas_capitol_exterior_02.mp4", "act":4, "covers_scene_id":null, "subtype":"texas_capitol_exterior_02" }
{ "public_path":"morton/factory/F170_legislative_chamber_empty_02.mp4", "act":4, "covers_scene_id":null, "subtype":"legislative_chamber_empty_02" }
{ "public_path":"morton/factory/F171_warm_texas_dawn_sky_02.mp4", "act":4, "covers_scene_id":null, "subtype":"warm_texas_dawn_sky_02" }
{ "public_path":"morton/factory/F172_open_road_home_dawn_02.mp4", "act":4, "covers_scene_id":null, "subtype":"open_road_home_dawn_02" }
{ "public_path":"morton/factory/F173_lab_microscope_slides_cold_02.mp4", "act":4, "covers_scene_id":null, "subtype":"lab_microscope_slides_cold_02" }
{ "public_path":"morton/factory/F174_courthouse_columns_day_bright_02.mp4", "act":4, "covers_scene_id":null, "subtype":"courthouse_columns_day_bright_02" }
{ "public_path":"morton/factory/F175_capitol_dome_texas_day_02.mp4", "act":4, "covers_scene_id":null, "subtype":"capitol_dome_texas_day_02" }
{ "public_path":"morton/factory/F176_horizon_field_dawn_warm_02.mp4", "act":4, "covers_scene_id":null, "subtype":"horizon_field_dawn_warm_02" }
{ "public_path":"morton/factory/F177_prison_exterior_receding_day_02.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_exterior_receding_day_02" }
{ "public_path":"morton/factory/F178_dna_lab_interior_cold_03.mp4", "act":4, "covers_scene_id":null, "subtype":"dna_lab_interior_cold_03" }
{ "public_path":"morton/factory/F179_gel_electrophoresis_equipment_03.mp4", "act":4, "covers_scene_id":null, "subtype":"gel_electrophoresis_equipment_03" }
{ "public_path":"morton/factory/F180_prison_gate_opening_day_03.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_gate_opening_day_03" }
{ "public_path":"morton/factory/F181_courthouse_steps_day_release_03.mp4", "act":4, "covers_scene_id":null, "subtype":"courthouse_steps_day_release_03" }
{ "public_path":"morton/factory/F182_texas_capitol_exterior_03.mp4", "act":4, "covers_scene_id":null, "subtype":"texas_capitol_exterior_03" }
{ "public_path":"morton/factory/F183_warm_texas_dawn_sky_03.mp4", "act":4, "covers_scene_id":null, "subtype":"warm_texas_dawn_sky_03" }
{ "public_path":"morton/factory/F184_open_road_home_dawn_03.mp4", "act":4, "covers_scene_id":null, "subtype":"open_road_home_dawn_03" }
{ "public_path":"morton/factory/F185_empty_austin_room_absence_03.mp4", "act":4, "covers_scene_id":null, "subtype":"empty_austin_room_absence_03" }
{ "public_path":"morton/factory/F186_horizon_field_dawn_warm_03.mp4", "act":4, "covers_scene_id":null, "subtype":"horizon_field_dawn_warm_03" }
{ "public_path":"morton/factory/F187_legislative_chamber_empty_03.mp4", "act":4, "covers_scene_id":null, "subtype":"legislative_chamber_empty_03" }
{ "public_path":"morton/factory/F188_lab_microscope_slides_cold_03.mp4", "act":4, "covers_scene_id":null, "subtype":"lab_microscope_slides_cold_03" }
{ "public_path":"morton/factory/F189_capitol_dome_texas_day_03.mp4", "act":4, "covers_scene_id":null, "subtype":"capitol_dome_texas_day_03" }
{ "public_path":"morton/factory/F190_courthouse_columns_day_bright_03.mp4", "act":4, "covers_scene_id":null, "subtype":"courthouse_columns_day_bright_03" }
{ "public_path":"morton/factory/F191_prison_gate_opening_day_04.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_gate_opening_day_04" }
{ "public_path":"morton/factory/F192_warm_texas_dawn_sky_04.mp4", "act":4, "covers_scene_id":null, "subtype":"warm_texas_dawn_sky_04" }
// ENDING (act 5) — 15
{ "public_path":"morton/factory/F193_empty_bedroom_absence_cold.mp4", "act":5, "covers_scene_id":"S201", "subtype":"empty_bedroom_absence_cold" }
{ "public_path":"morton/factory/F194_file_drawer_dim_close.mp4", "act":5, "covers_scene_id":"S209", "subtype":"file_drawer_dim_close" }
{ "public_path":"morton/factory/F195_evidence_room_minimal_cold.mp4", "act":5, "covers_scene_id":"S213", "subtype":"evidence_room_minimal_cold" }
{ "public_path":"morton/factory/F196_texas_dawn_edge_quiet.mp4", "act":5, "covers_scene_id":"S215", "subtype":"texas_dawn_edge_quiet" }
{ "public_path":"morton/factory/F197_quiet_neighborhood_dawn.mp4", "act":5, "covers_scene_id":null, "subtype":"quiet_neighborhood_dawn" }
{ "public_path":"morton/factory/F198_empty_bedroom_absence_cold_02.mp4", "act":5, "covers_scene_id":null, "subtype":"empty_bedroom_absence_cold_02" }
{ "public_path":"morton/factory/F199_file_drawer_dim_close_02.mp4", "act":5, "covers_scene_id":null, "subtype":"file_drawer_dim_close_02" }
{ "public_path":"morton/factory/F200_evidence_room_minimal_cold_02.mp4", "act":5, "covers_scene_id":null, "subtype":"evidence_room_minimal_cold_02" }
{ "public_path":"morton/factory/F201_texas_dawn_edge_quiet_02.mp4", "act":5, "covers_scene_id":null, "subtype":"texas_dawn_edge_quiet_02" }
{ "public_path":"morton/factory/F202_quiet_neighborhood_dawn_02.mp4", "act":5, "covers_scene_id":null, "subtype":"quiet_neighborhood_dawn_02" }
{ "public_path":"morton/factory/F203_empty_bedroom_absence_cold_03.mp4", "act":5, "covers_scene_id":null, "subtype":"empty_bedroom_absence_cold_03" }
{ "public_path":"morton/factory/F204_file_drawer_dim_close_03.mp4", "act":5, "covers_scene_id":null, "subtype":"file_drawer_dim_close_03" }
{ "public_path":"morton/factory/F205_evidence_room_minimal_cold_03.mp4", "act":5, "covers_scene_id":null, "subtype":"evidence_room_minimal_cold_03" }
{ "public_path":"morton/factory/F206_texas_dawn_edge_quiet_03.mp4", "act":5, "covers_scene_id":null, "subtype":"texas_dawn_edge_quiet_03" }
{ "public_path":"morton/factory/F207_quiet_neighborhood_dawn_03.mp4", "act":5, "covers_scene_id":null, "subtype":"quiet_neighborhood_dawn_03" }
// 繋ぎ (covers_scene_id:null・情景) — 33
{ "public_path":"morton/factory/F208_institutional_corridor_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"institutional_corridor_cold" }
{ "public_path":"morton/factory/F209_marble_floor_reflection.mp4", "act":2, "covers_scene_id":null, "subtype":"marble_floor_reflection" }
{ "public_path":"morton/factory/F210_file_cabinets_row_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"file_cabinets_row_dim" }
{ "public_path":"morton/factory/F211_dry_brush_texture_pan.mp4", "act":1, "covers_scene_id":null, "subtype":"dry_brush_texture_pan" }
{ "public_path":"morton/factory/F212_sky_gradient_cold_slow.mp4", "act":3, "covers_scene_id":null, "subtype":"sky_gradient_cold_slow" }
{ "public_path":"morton/factory/F213_records_wall_shelves.mp4", "act":2, "covers_scene_id":null, "subtype":"records_wall_shelves" }
{ "public_path":"morton/factory/F214_austin_cityscape_distant.mp4", "act":4, "covers_scene_id":null, "subtype":"austin_cityscape_distant" }
{ "public_path":"morton/factory/F215_texas_landscape_wide_day.mp4", "act":1, "covers_scene_id":null, "subtype":"texas_landscape_wide_day" }
{ "public_path":"morton/factory/F216_water_reflection_cold.mp4", "act":3, "covers_scene_id":null, "subtype":"water_reflection_cold" }
{ "public_path":"morton/factory/F217_courthouse_ambient_wide.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_ambient_wide" }
{ "public_path":"morton/factory/F218_institutional_corridor_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"institutional_corridor_cold_02" }
{ "public_path":"morton/factory/F219_marble_floor_reflection_02.mp4", "act":2, "covers_scene_id":null, "subtype":"marble_floor_reflection_02" }
{ "public_path":"morton/factory/F220_file_cabinets_row_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"file_cabinets_row_dim_02" }
{ "public_path":"morton/factory/F221_dry_brush_texture_pan_02.mp4", "act":1, "covers_scene_id":null, "subtype":"dry_brush_texture_pan_02" }
{ "public_path":"morton/factory/F222_sky_gradient_cold_slow_02.mp4", "act":3, "covers_scene_id":null, "subtype":"sky_gradient_cold_slow_02" }
{ "public_path":"morton/factory/F223_records_wall_shelves_02.mp4", "act":2, "covers_scene_id":null, "subtype":"records_wall_shelves_02" }
{ "public_path":"morton/factory/F224_austin_cityscape_distant_02.mp4", "act":4, "covers_scene_id":null, "subtype":"austin_cityscape_distant_02" }
{ "public_path":"morton/factory/F225_texas_landscape_wide_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"texas_landscape_wide_day_02" }
{ "public_path":"morton/factory/F226_water_reflection_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"water_reflection_cold_02" }
{ "public_path":"morton/factory/F227_courthouse_ambient_wide_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_ambient_wide_02" }
{ "public_path":"morton/factory/F228_institutional_corridor_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"institutional_corridor_cold_03" }
{ "public_path":"morton/factory/F229_marble_floor_reflection_03.mp4", "act":2, "covers_scene_id":null, "subtype":"marble_floor_reflection_03" }
{ "public_path":"morton/factory/F230_file_cabinets_row_dim_03.mp4", "act":2, "covers_scene_id":null, "subtype":"file_cabinets_row_dim_03" }
{ "public_path":"morton/factory/F231_sky_gradient_cold_slow_03.mp4", "act":3, "covers_scene_id":null, "subtype":"sky_gradient_cold_slow_03" }
{ "public_path":"morton/factory/F232_dry_brush_texture_pan_03.mp4", "act":1, "covers_scene_id":null, "subtype":"dry_brush_texture_pan_03" }
{ "public_path":"morton/factory/F233_records_wall_shelves_03.mp4", "act":2, "covers_scene_id":null, "subtype":"records_wall_shelves_03" }
{ "public_path":"morton/factory/F234_texas_landscape_wide_day_03.mp4", "act":4, "covers_scene_id":null, "subtype":"texas_landscape_wide_day_03" }
{ "public_path":"morton/factory/F235_austin_cityscape_distant_03.mp4", "act":4, "covers_scene_id":null, "subtype":"austin_cityscape_distant_03" }
{ "public_path":"morton/factory/F236_water_reflection_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"water_reflection_cold_03" }
{ "public_path":"morton/factory/F237_courthouse_ambient_wide_03.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_ambient_wide_03" }
{ "public_path":"morton/factory/F238_institutional_corridor_cold_04.mp4", "act":3, "covers_scene_id":null, "subtype":"institutional_corridor_cold_04" }
{ "public_path":"morton/factory/F239_sky_gradient_cold_slow_04.mp4", "act":4, "covers_scene_id":null, "subtype":"sky_gradient_cold_slow_04" }
{ "public_path":"morton/factory/F240_marble_floor_reflection_04.mp4", "act":2, "covers_scene_id":null, "subtype":"marble_floor_reflection_04" }
```

**検算:** 12 + 45 + 40 + 50 + 45 + 15 + 33 = 240 ✓・全 public_path 非空 ✓（不変条件17）・各1回使用（cap 1）。**暗いクリップは全体の1/3=約80本まで**（courthouse 昼光・warm dawn・lab の実用光を混ぜる）。

## 4.5 ★`motion[]` 全43エントリ（★必ず実体化・public_path 非空）

> エントリ形は §4.1a 準拠 + 動画フィールド。`asset_id ^MOR-M\d{2}$`。`source_still` は §8.1a の種画像、`source_scene_id`=`MS<NN>`。runtime で `sha256`/`width 1280`/`height 720`/`fps 48`/`frames`/`duration_sec`/`qc` を埋める（§8.4）。**空配列を書かない。**

```jsonc
{ "asset_id":"MOR-M01", "source_scene_id":"MS01", "source_still":"H:/pd-media/assets/ai/morton/M01_src.png", "path":"H:/pd-media/assets/ai_video/morton/M01_rife.mp4", "public_path":"morton/motion/M01_rife.mp4", "act":0, "storyboard":"A0-01", "tags":["child_hand_crayon_monster"] }
{ "asset_id":"MOR-M02", "source_scene_id":"MS02", "source_still":"H:/pd-media/assets/ai/morton/M02_src.png", "path":"H:/pd-media/assets/ai_video/morton/M02_rife.mp4", "public_path":"morton/motion/M02_rife.mp4", "act":0, "storyboard":"A0-02", "tags":["monster_scrawl_buried_drawer"] }
{ "asset_id":"MOR-M03", "source_scene_id":"MS03", "source_still":"H:/pd-media/assets/ai/morton/M03_src.png", "path":"H:/pd-media/assets/ai_video/morton/M03_rife.mp4", "public_path":"morton/motion/M03_rife.mp4", "act":0, "storyboard":"hook", "tags":["cold_blue_edge_finds"] }
{ "asset_id":"MOR-M04", "source_scene_id":"MS04", "source_still":"H:/pd-media/assets/ai/morton/M04_src.png", "path":"H:/pd-media/assets/ai_video/morton/M04_rife.mp4", "public_path":"morton/motion/M04_rife.mp4", "act":1, "storyboard":"A1-01", "tags":["doorway_predawn_leave","H001_anon"] }
{ "asset_id":"MOR-M05", "source_scene_id":"MS05", "source_still":"H:/pd-media/assets/ai/morton/M05_src.png", "path":"H:/pd-media/assets/ai_video/morton/M05_rife.mp4", "public_path":"morton/motion/M05_rife.mp4", "act":1, "storyboard":"A1-02", "tags":["empty_bed_absence_light"] }
{ "asset_id":"MOR-M06", "source_scene_id":"MS06", "source_still":"H:/pd-media/assets/ai/morton/M06_src.png", "path":"H:/pd-media/assets/ai_video/morton/M06_rife.mp4", "public_path":"morton/motion/M06_rife.mp4", "act":1, "storyboard":"A1-03", "tags":["father_child_return_backs","H002_anon"] }
{ "asset_id":"MOR-M07", "source_scene_id":"MS07", "source_still":"H:/pd-media/assets/ai/morton/M07_src.png", "path":"H:/pd-media/assets/ai_video/morton/M07_rife.mp4", "public_path":"morton/motion/M07_rife.mp4", "act":1, "storyboard":"A1-04", "tags":["police_lights_cold_arrive","H009_anon"] }
{ "asset_id":"MOR-M08", "source_scene_id":"MS08", "source_still":"H:/pd-media/assets/ai/morton/M08_src.png", "path":"H:/pd-media/assets/ai_video/morton/M08_rife.mp4", "public_path":"morton/motion/M08_rife.mp4", "act":1, "storyboard":"A1-05", "tags":["husband_assumption_gears"] }
{ "asset_id":"MOR-M09", "source_scene_id":"MS09", "source_still":"H:/pd-media/assets/ai/morton/M09_src.png", "path":"H:/pd-media/assets/ai_video/morton/M09_rife.mp4", "public_path":"morton/motion/M09_rife.mp4", "act":1, "storyboard":"A1-06", "tags":["stomach_clock_reverse_engineer","H010_anon"] }
{ "asset_id":"MOR-M10", "source_scene_id":"MS10", "source_still":"H:/pd-media/assets/ai/morton/M10_src.png", "path":"H:/pd-media/assets/ai_video/morton/M10_rife.mp4", "public_path":"morton/motion/M10_rife.mp4", "act":1, "storyboard":"A1-07", "tags":["child_account_written","H011_anon"] }
{ "asset_id":"MOR-M11", "source_scene_id":"MS11", "source_still":"H:/pd-media/assets/ai/morton/M11_src.png", "path":"H:/pd-media/assets/ai_video/morton/M11_rife.mp4", "public_path":"morton/motion/M11_rife.mp4", "act":1, "storyboard":"A1-08", "tags":["account_thrown_drawer"] }
{ "asset_id":"MOR-M12", "source_scene_id":"MS12", "source_still":"H:/pd-media/assets/ai/morton/M12_src.png", "path":"H:/pd-media/assets/ai_video/morton/M12_rife.mp4", "public_path":"morton/motion/M12_rife.mp4", "act":2, "storyboard":"A2-01", "tags":["no_physical_evidence_cursor"] }
{ "asset_id":"MOR-M13", "source_scene_id":"MS13", "source_still":"H:/pd-media/assets/ai/morton/M13_src.png", "path":"H:/pd-media/assets/ai_video/morton/M13_rife.mp4", "public_path":"morton/motion/M13_rife.mp4", "act":2, "storyboard":"A2-02", "tags":["hands_file_into_drawer","H004_anon"] }
{ "asset_id":"MOR-M14", "source_scene_id":"MS14", "source_still":"H:/pd-media/assets/ai/morton/M14_src.png", "path":"H:/pd-media/assets/ai_video/morton/M14_rife.mp4", "public_path":"morton/motion/M14_rife.mp4", "act":2, "storyboard":"A2-03", "tags":["green_van_glimpsed_cold","H012_anon"] }
{ "asset_id":"MOR-M15", "source_scene_id":"MS15", "source_still":"H:/pd-media/assets/ai/morton/M15_src.png", "path":"H:/pd-media/assets/ai_video/morton/M15_rife.mp4", "public_path":"morton/motion/M15_rife.mp4", "act":2, "storyboard":"A2-04", "tags":["blue_bandana_in_drawer_ignored"] }
{ "asset_id":"MOR-M16", "source_scene_id":"MS16", "source_still":"H:/pd-media/assets/ai/morton/M16_src.png", "path":"H:/pd-media/assets/ai_video/morton/M16_rife.mp4", "public_path":"morton/motion/M16_rife.mp4", "act":2, "storyboard":"A2-05", "tags":["stolen_checks_san_antonio_abstract","H013_anon"] }
{ "asset_id":"MOR-M17", "source_scene_id":"MS17", "source_still":"H:/pd-media/assets/ai/morton/M17_src.png", "path":"H:/pd-media/assets/ai_video/morton/M17_rife.mp4", "public_path":"morton/motion/M17_rife.mp4", "act":2, "storyboard":"A2-06", "tags":["prints_footprints_unclaimed"] }
{ "asset_id":"MOR-M18", "source_scene_id":"MS18", "source_still":"H:/pd-media/assets/ai/morton/M18_src.png", "path":"H:/pd-media/assets/ai_video/morton/M18_rife.mp4", "public_path":"morton/motion/M18_rife.mp4", "act":2, "storyboard":"A2-07", "tags":["house_of_cards_case"] }
{ "asset_id":"MOR-M19", "source_scene_id":"MS19", "source_still":"H:/pd-media/assets/ai/morton/M19_src.png", "path":"H:/pd-media/assets/ai_video/morton/M19_rife.mp4", "public_path":"morton/motion/M19_rife.mp4", "act":2, "storyboard":"A2-08", "tags":["prosecutor_podium_shadow","H003_anon"] }
{ "asset_id":"MOR-M20", "source_scene_id":"MS20", "source_still":"H:/pd-media/assets/ai/morton/M20_src.png", "path":"H:/pd-media/assets/ai_video/morton/M20_rife.mp4", "public_path":"morton/motion/M20_rife.mp4", "act":2, "storyboard":"A2-09", "tags":["conviction_life_doors_close","H014_anon"] }
{ "asset_id":"MOR-M21", "source_scene_id":"MS21", "source_still":"H:/pd-media/assets/ai/morton/M21_src.png", "path":"H:/pd-media/assets/ai_video/morton/M21_rife.mp4", "public_path":"morton/motion/M21_rife.mp4", "act":3, "storyboard":"A3-01", "tags":["cell_window_seasons_shift"] }
{ "asset_id":"MOR-M22", "source_scene_id":"MS22", "source_still":"H:/pd-media/assets/ai/morton/M22_src.png", "path":"H:/pd-media/assets/ai_video/morton/M22_rife.mp4", "public_path":"morton/motion/M22_rife.mp4", "act":3, "storyboard":"A3-02", "tags":["twentyfive_years_weight","H016_anon"] }
{ "asset_id":"MOR-M23", "source_scene_id":"MS23", "source_still":"H:/pd-media/assets/ai/morton/M23_src.png", "path":"H:/pd-media/assets/ai_video/morton/M23_rife.mp4", "public_path":"morton/motion/M23_rife.mp4", "act":3, "storyboard":"A3-03", "tags":["bunk_figure_back","H005_anon"] }
{ "asset_id":"MOR-M24", "source_scene_id":"MS24", "source_still":"H:/pd-media/assets/ai/morton/M24_src.png", "path":"H:/pd-media/assets/ai_video/morton/M24_rife.mp4", "public_path":"morton/motion/M24_rife.mp4", "act":3, "storyboard":"A3-04", "tags":["lawyer_file_desklamp","H006_anon"] }
{ "asset_id":"MOR-M25", "source_scene_id":"MS25", "source_still":"H:/pd-media/assets/ai/morton/M25_src.png", "path":"H:/pd-media/assets/ai_video/morton/M25_rife.mp4", "public_path":"morton/motion/M25_rife.mp4", "act":3, "storyboard":"A3-05", "tags":["bradley_wall_six_years","H015_anon"] }
{ "asset_id":"MOR-M26", "source_scene_id":"MS26", "source_still":"H:/pd-media/assets/ai/morton/M26_src.png", "path":"H:/pd-media/assets/ai_video/morton/M26_rife.mp4", "public_path":"morton/motion/M26_rife.mp4", "act":3, "storyboard":"A3-06", "tags":["dna_test_denied_loop"] }
{ "asset_id":"MOR-M27", "source_scene_id":"MS27", "source_still":"H:/pd-media/assets/ai/morton/M27_src.png", "path":"H:/pd-media/assets/ai_video/morton/M27_rife.mp4", "public_path":"morton/motion/M27_rife.mp4", "act":3, "storyboard":"A3-07", "tags":["order_to_test_2011"] }
{ "asset_id":"MOR-M28", "source_scene_id":"MS28", "source_still":"H:/pd-media/assets/ai/morton/M28_src.png", "path":"H:/pd-media/assets/ai_video/morton/M28_rife.mp4", "public_path":"morton/motion/M28_rife.mp4", "act":3, "storyboard":"A3-08", "tags":["bandana_to_lab"] }
{ "asset_id":"MOR-M29", "source_scene_id":"MS29", "source_still":"H:/pd-media/assets/ai/morton/M29_src.png", "path":"H:/pd-media/assets/ai_video/morton/M29_rife.mp4", "public_path":"morton/motion/M29_rife.mp4", "act":4, "storyboard":"A4-01", "tags":["bandana_tested_two_people"] }
{ "asset_id":"MOR-M30", "source_scene_id":"MS30", "source_still":"H:/pd-media/assets/ai/morton/M30_src.png", "path":"H:/pd-media/assets/ai_video/morton/M30_rife.mp4", "public_path":"morton/motion/M30_rife.mp4", "act":4, "storyboard":"A4-02", "tags":["dna_bands_ignite_blue_flood"] }
{ "asset_id":"MOR-M31", "source_scene_id":"MS31", "source_still":"H:/pd-media/assets/ai/morton/M31_src.png", "path":"H:/pd-media/assets/ai_video/morton/M31_rife.mp4", "public_path":"morton/motion/M31_rife.mp4", "act":4, "storyboard":"A4-03", "tags":["second_dna_unknown_man"] }
{ "asset_id":"MOR-M32", "source_scene_id":"MS32", "source_still":"H:/pd-media/assets/ai/morton/M32_src.png", "path":"H:/pd-media/assets/ai_video/morton/M32_rife.mp4", "public_path":"morton/motion/M32_rife.mp4", "act":4, "storyboard":"A4-04", "tags":["norwood_named_cold_silhouette"] }
{ "asset_id":"MOR-M33", "source_scene_id":"MS33", "source_still":"H:/pd-media/assets/ai/morton/M33_src.png", "path":"H:/pd-media/assets/ai_video/morton/M33_rife.mp4", "public_path":"morton/motion/M33_rife.mp4", "act":4, "storyboard":"A4-05", "tags":["baker_killed_while_imprisoned_gutpunch"] }
{ "asset_id":"MOR-M34", "source_scene_id":"MS34", "source_still":"H:/pd-media/assets/ai/morton/M34_src.png", "path":"H:/pd-media/assets/ai_video/morton/M34_rife.mp4", "public_path":"morton/motion/M34_rife.mp4", "act":4, "storyboard":"A4-06", "tags":["morton_walks_gate_warm","H007_anon"] }
{ "asset_id":"MOR-M35", "source_scene_id":"MS35", "source_still":"H:/pd-media/assets/ai/morton/M35_src.png", "path":"H:/pd-media/assets/ai_video/morton/M35_rife.mp4", "public_path":"morton/motion/M35_rife.mp4", "act":4, "storyboard":"A4-07", "tags":["homecoming_gold_bleeds","H017_anon"] }
{ "asset_id":"MOR-M36", "source_scene_id":"MS36", "source_still":"H:/pd-media/assets/ai/morton/M36_src.png", "path":"H:/pd-media/assets/ai_video/morton/M36_rife.mp4", "public_path":"morton/motion/M36_rife.mp4", "act":4, "storyboard":"A4-08", "tags":["anderson_arrested_scale_tips"] }
{ "asset_id":"MOR-M37", "source_scene_id":"MS37", "source_still":"H:/pd-media/assets/ai/morton/M37_src.png", "path":"H:/pd-media/assets/ai_video/morton/M37_rife.mp4", "public_path":"morton/motion/M37_rife.mp4", "act":4, "storyboard":"A4-09", "tags":["scale_25y_vs_5d"] }
{ "asset_id":"MOR-M38", "source_scene_id":"MS38", "source_still":"H:/pd-media/assets/ai/morton/M38_src.png", "path":"H:/pd-media/assets/ai_video/morton/M38_rife.mp4", "public_path":"morton/motion/M38_rife.mp4", "act":4, "storyboard":"A4-10", "tags":["morton_act_podium","H008_anon"] }
{ "asset_id":"MOR-M39", "source_scene_id":"MS39", "source_still":"H:/pd-media/assets/ai/morton/M39_src.png", "path":"H:/pd-media/assets/ai_video/morton/M39_rife.mp4", "public_path":"morton/motion/M39_rife.mp4", "act":4, "storyboard":"A4-11", "tags":["the_act_passes_warm","H018_anon"] }
{ "asset_id":"MOR-M40", "source_scene_id":"MS40", "source_still":"H:/pd-media/assets/ai/morton/M40_src.png", "path":"H:/pd-media/assets/ai_video/morton/M40_rife.mp4", "public_path":"morton/motion/M40_rife.mp4", "act":5, "storyboard":"A5-01", "tags":["back_to_child_voice"] }
{ "asset_id":"MOR-M41", "source_scene_id":"MS41", "source_still":"H:/pd-media/assets/ai/morton/M41_src.png", "path":"H:/pd-media/assets/ai_video/morton/M41_rife.mp4", "public_path":"morton/motion/M41_rife.mp4", "act":5, "storyboard":"A5-02", "tags":["monster_scrawl_unburied"] }
{ "asset_id":"MOR-M42", "source_scene_id":"MS42", "source_still":"H:/pd-media/assets/ai/morton/M42_src.png", "path":"H:/pd-media/assets/ai_video/morton/M42_rife.mp4", "public_path":"morton/motion/M42_rife.mp4", "act":5, "storyboard":"A5-03", "tags":["strip_to_essentials"] }
{ "asset_id":"MOR-M43", "source_scene_id":"MS43", "source_still":"H:/pd-media/assets/ai/morton/M43_src.png", "path":"H:/pd-media/assets/ai_video/morton/M43_rife.mp4", "public_path":"morton/motion/M43_rife.mp4", "act":5, "storyboard":"A5-04", "tags":["truth_never_missing_close"] }
```

**検算:** 43エントリ ✓・全 public_path 非空 ✓（不変条件18）・`^MOR-M\d{2}$` ✓・**★H001–H018（匿名人物・18本）は M04/M06/M07/M09/M10/M13/M14/M16/M19/M20/M22/M23/M24/M25/M34/M35/M38/M39 の内数 ✓**（＝43 motion のうち 18 が人物・86 cuts のうち最大36が人物）。残り25本が抽象/象徴。

## 4.6 `overlay[]` 30エントリ（distinct 素材に数えない・15 particle / 10 light / 5 vfx）

```jsonc
{ "public_path":"morton/overlay/P01_cold_room_dust.mp4", "type":"particle_assets", "subtype":"cold_room_dust", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P02_archive_dust_cold.mp4", "type":"particle_assets", "subtype":"archive_dust_cold", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P03_evidence_room_dust.mp4", "type":"particle_assets", "subtype":"evidence_room_dust", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P04_dry_texas_dust_motes.mp4", "type":"particle_assets", "subtype":"dry_texas_dust_motes", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P05_fine_grain_dust.mp4", "type":"particle_assets", "subtype":"fine_grain_dust", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P06_lab_dust_motes.mp4", "type":"particle_assets", "subtype":"lab_dust_motes", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P07_courtroom_dust.mp4", "type":"particle_assets", "subtype":"courtroom_dust", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P08_prison_dust_cold.mp4", "type":"particle_assets", "subtype":"prison_dust_cold", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P09_paper_fiber_drift.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P10_night_air_drift.mp4", "type":"particle_assets", "subtype":"night_air_drift", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P11_cold_room_dust_02.mp4", "type":"particle_assets", "subtype":"cold_room_dust_02", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P12_archive_dust_cold_02.mp4", "type":"particle_assets", "subtype":"archive_dust_cold_02", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P13_dry_texas_dust_motes_02.mp4", "type":"particle_assets", "subtype":"dry_texas_dust_motes_02", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P14_lab_dust_motes_02.mp4", "type":"particle_assets", "subtype":"lab_dust_motes_02", "blend_hint":"screen" }
{ "public_path":"morton/overlay/P15_evidence_room_dust_02.mp4", "type":"particle_assets", "subtype":"evidence_room_dust_02", "blend_hint":"screen" }
{ "public_path":"morton/overlay/L01_cold_blue_shaft.mp4", "type":"light_assets", "subtype":"cold_blue_shaft", "blend_hint":"screen" }
{ "public_path":"morton/overlay/L02_cold_window_light_bar.mp4", "type":"light_assets", "subtype":"cold_window_light_bar", "blend_hint":"screen" }
{ "public_path":"morton/overlay/L03_single_lamp_glow_cold.mp4", "type":"light_assets", "subtype":"single_lamp_glow_cold", "blend_hint":"screen" }
{ "public_path":"morton/overlay/L04_evidence_blue_edge_glow.mp4", "type":"light_assets", "subtype":"evidence_blue_edge_glow", "blend_hint":"screen" }
{ "public_path":"morton/overlay/L05_homecoming_gold_edge_glow.mp4", "type":"light_assets", "subtype":"homecoming_gold_edge_glow", "blend_hint":"screen" }
{ "public_path":"morton/overlay/L06_lab_panel_glow_cold.mp4", "type":"light_assets", "subtype":"lab_panel_glow_cold", "blend_hint":"screen" }
{ "public_path":"morton/overlay/L07_cold_key_light_sweep.mp4", "type":"light_assets", "subtype":"cold_key_light_sweep", "blend_hint":"screen" }
{ "public_path":"morton/overlay/L08_cold_blue_shaft_02.mp4", "type":"light_assets", "subtype":"cold_blue_shaft_02", "blend_hint":"screen" }
{ "public_path":"morton/overlay/L09_homecoming_gold_edge_glow_02.mp4", "type":"light_assets", "subtype":"homecoming_gold_edge_glow_02", "blend_hint":"screen" }
{ "public_path":"morton/overlay/L10_lab_panel_glow_cold_02.mp4", "type":"light_assets", "subtype":"lab_panel_glow_cold_02", "blend_hint":"screen" }
{ "public_path":"morton/overlay/V01_film_grain_fine.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine", "blend_hint":"overlay" }
{ "public_path":"morton/overlay/V02_cold_light_noise.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise", "blend_hint":"screen" }
{ "public_path":"morton/overlay/V03_film_grain_fine_02.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine_02", "blend_hint":"overlay" }
{ "public_path":"morton/overlay/V04_cold_light_noise_02.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise_02", "blend_hint":"screen" }
{ "public_path":"morton/overlay/V05_blue_glitch_min.mp4", "type":"vfx_overlays", "subtype":"blue_glitch_min", "blend_hint":"screen" }
```

**検算:** 15 + 10 + 5 = 30 ✓。runtime で `asset_id`/`path`/`sha256`/`license`/`eyeballed_content`/`qc` を埋める。**overlay は `cuts[].src` に出さない。★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない（DESIGN §1・CODEX_B §5.9）。scanline/CRT/vignette-wash の overlay を選ばない。** 発色は B が accent `#3F5E8C`（cold evidence-blue）に寄せる想定・homecoming-gold `#D19A3E` の light（L05/L09）は exoneration/close 用のみ。他話色（gold/blue/amber/teal/crimson/green/violet/plum/cyan）を選ばない。

---

# 5. A-1: SDXL 静止画のバッチ生成（215本 × 1枚・バリエーション0）— ★motif ライブラリ方式

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-052-morton/04_scenes/ai_prompts.v001.md   ← A が §5.9 の形式で書く
出力:  H:\pd-media\assets\ai\morton\S<NNN>.png（+ remotion/public/morton/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★215本の作り方＝「motif ライブラリ」テンプレート方式

215 の固有プロンプトを**幕×motifで体系化**する。各 motif に (a) **確定 distinct 枚数**、(b) **S番号レンジ**、(c) **literal 例プロンプト** を与える。**各 motif の例プロンプトを下敷きに、割り当てられた枚数ぶんの固有プロンプトを、被写体・角度・光・寄り引き・オブジェの状態を1枚ずつ変えて書き切る**（同一構図の量産＝禁止・1枚1固有）。**motif 合計が幕の確定 still 数（§3.2）に一致し、全幕合計 215 になることを最後に検算。**

> ★**1シーン1枚・variants 0。** 各プロンプト末尾に §5.3 の `[STYLE]`（人物なし象徴 still）**または** §5.11 の `[HSTYLE]`（匿名人物 still）を**全文連結**、`Avoid:` の後に §5.4 `[NEG]`（象徴）**または** §5.11 `[HNEG]`（匿名人物）を**全文連結**。
> **★owner directive（EP48/49 の「空/寂しい・人がいない」却下を潰す）: 215 body を2レーンに分ける。**
> - **object/symbolic レーン（157枚）＝ `[STYLE]`+`[NEG]`（人物なし）:** empty bed of absence・bandana・green van の遠景・DNA bands・drawer・crayon monster・cell window・courthouse/prison 外観・sky 等、**人物がいない/いるべきでない象徴ビート**。
> - **★human-present レーン（58枚＝27%）＝ `[HSTYLE]`+`[HNEG]`（匿名・非識別の人物）:** narration に人がいるビート（捜査官・検事・法廷の陪審/傍聴・弁護士・囚人/看守・記者・homecoming の群衆・立法府 等）に **匿名・非識別の人物（背向き/影/silhouette/hands・adults only）** を入れる。**該当 S-range は §5.6 で `★HP` と明記。**
> **HARD BAN（不変・両レーン共通）: 識別可能な Eric（子供）の顔なし（小さな手/crayon のみ）・被害者(Christine/Debra)の描写と暴行/遺体/現場なし・実在人物(Morton/Norwood/Anderson 等)の likeness なし・可読テキストなし。**匿名人物は§5.11 の H 種と同じ扱い（人体そのものは可・`has_human_body:true` は reject でない）。

## 5.3 共通スタイル `[STYLE]`（body 215 の象徴 still ＋ 抽象 i2v 種に連結・DESIGN §1 と一字一致）

```
, cinematic still, somber documentary grade, a cold forensic evidence-blue key light as the one recurring cool note, near-black ink institutional gravity, a Texas suburban home rendered as cold quiet absence, an empty made bed in cold light never any victim or violence, a strip of blue bandana cloth as the buried-truth motif glimpsed in a dark evidence drawer, a green van as a cold distant shape behind a house never any crime, a child's small hand and an abstract crayon monster scrawl handled with restraint, a file drawer sliding shut over the truth, cold evidence-blue gel-electrophoresis bands as the forensic motif, a single warm Texas homecoming-gold note reserved for the very end, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, backs and hands and objects only
```

> **EP39〜EP51 の色語（1語も含めない）:** electric blue / midday suburban demolition / sodium prison gold / warrant-blue ankle monitor / porch-amber ambulance / teal-green hospital / warm-tungsten crimson kitchen / forest-green / civil-violet two-lane Texas road pickup / glover / somber-plum Utah / cold steel-cyan（EP50）。**EP52 の色は cold evidence/bandana-blue `#3F5E8C` ＋ 末端のみ Texas homecoming-gold `#D19A3E`。** ★EP47 も「Texas」だが EP47 は two-lane road/pickup/civil-violet＝**本作の Williamson County suburb / evidence-blue とは別レーン**。EP50 cyan と混同しない（本作は cyan ではなく muted indigo-blue #3F5E8C）。

## 5.4 共通ネガティブ `[NEG]`（各 `Avoid:` の後に全文付ける・A/B 同一）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible case file, legible police report, legible newspaper, legible lab report, legible DNA figures, legible date, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, front-facing person, Michael Morton, Christine Morton, Eric, Mark Norwood, Ken Anderson as a person, victim, murder victim, beaten body, corpse, bludgeoned, assault, murder scene, violence, blood, gore, injury, weapon, wooden club, child witnessing an attack, crying toddler, sexual content, nudity, crime scene, re-enactment, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, milky haze, foggy wash, scanline, CRT texture, vignette wash
```

> 文字/紙面が必要な絵は「blurred into an unreadable smear」で判読不能に。**被害者・暴行・遺体・凶器・現場・可読の偽公文書を NEG で明示抑制。** この `[NEG]` は象徴 body 215 ＋ 抽象 i2v 種にのみ使う。**人物ビート（§5.11 H シリーズ・§5.12 thumb_face）には使わない**（人物を弾くため）。H/thumb は `[HNEG]`/`[TNEG]` を使う。

## 5.5 プロンプトの絶対ルール（215本すべてに適用）

- **body 215 は2レーン（§5.2）:** object/symbolic 157枚＝§5.3/§5.4（人物なし）、**human-present 58枚（27%）＝§5.11 `[HSTYLE]`/`[HNEG]`（匿名・非識別の人物＝背向き/影/silhouette/hands・adults only）**。**★どの body still にも実在人物 likeness を作らない・識別可能な Eric の顔を作らない・被害者/暴行/遺体を描かない。** 動く人物ビートは §5.11 の H シリーズ（i2v 種・18本）で別途。
- **可読文字なし。** file/report/newspaper/lab/日付/金額/DNA数値/ロゴを描かない。
- **被害者・暴行・殺害・遺体・現場・凶器を一切描かない。** 寝室は empty bed of absence のみ。**3歳 Eric は小さな手・crayon monster scrawl のみ（識別可能な子供顔なし・襲撃視点なし）。**
- **Morton の innocence（制約1）:** Morton が犯人に見える絵を作らない（"the husband did it" は state の theory の帰属枠のみ）。
- **Norwood を美化しない（制約4）:** cold・distance・非識別 silhouette で。lurid にしない。
- **cold evidence-blue system（`#3F5E8C`）を基調に、Texas homecoming-gold `#D19A3E` は ACT4 後半/close/exoneration の該当 motif のみ**（§5.6 の per-act motif で指定）。
- **★footage treatment は bleed/parallax（DESIGN §1）。depth 前提の絵作りをしない**（極端な前後分離＝depth 用の抜けを想定しない・平面的でクリアな構図でよい）。
- **dochighlight を作らない・書かない（制約8）。** milky wash / scanline を描かない（制約・DESIGN §1）。

## 5.6 ★motif ライブラリ（幕別・distinct 数確定・S番号レンジ・literal 例プロンプト）

> 各 motif ブロックは `motif名 — 枚数 — S番号レンジ`。**例で示した S番号は必ずその内容で作り、残りの枚数はその motif の変奏で埋める。**
> **★`[STYLE]`/`[NEG]`（§5.3/§5.4）= 人物なし象徴ブロック。`★HP` マーク付きブロック= §5.11 `[HSTYLE]`/`[HNEG]`（匿名・非識別の人物＝背向き/影/silhouette/hands・adults only）。** ★HP 合計 = **58枚（27%）**: ACT1 11（S036–S041, S052–S056）／ACT2 15（S069–S076, S109–S115）／ACT3 10（S120–S123, S142–S147）／ACT4 22（S174–S200）。ACT0/ACT5 は象徴のまま（0）。**★HP でも Eric は識別可能顔にしない（adults only／子供は小さな手のみ）・被害者/暴行/遺体なし・実在 likeness なし。**

### ACT 0 — HOOK + OPENING（15枚・S001–S015）
- **child_hand_crayon_monster — 4 — S001–S004**（S001 は also_thumb・**hook signature**・3歳 Eric の証言を restraint で）
```
- `S001.png`
A small child's hand beside an abstract crayon scrawl of a monster on paper, found by a single cold forensic evidence-blue edge of light in near-black, a three-year-old's testimony rendered with restraint, non-graphic, no identifiable child, no face, no readable text [STYLE] Avoid: [NEG]
```
- **monster_buried_drawer — 3 — S005–S007**（crayon scrawl が closing file drawer の下に埋まる＝they buried it）
```
- `S005.png`
A child's crayon monster drawing on a page being covered as a dark institutional file drawer slides shut over it in cold evidence-blue light, the truth buried, symbolic, no person, no face, no readable text [STYLE] Avoid: [NEG]
```
- **cold_blue_edge_finds — 4 — S008–S011**（黒→冷 evidence-blue の一筋が object を見つける・bandana strip / bed / file）
- **opening_title_abstract — 4 — S012–S015**（冷 evidence-blue の abstract field・title 下地・distant Texas treeline の遠い予兆）

### ACT 1 — THE HUSBAND DID IT（45枚・S016–S060）
- **texas_morning_house — 8 — S016–S023**（1986 Williamson County の quiet suburban house・pre-dawn・cold・無人）
```
- `S016.png`
A quiet 1986 Texas suburban single-story house exterior before dawn in cold evidence-blue light, still and ordinary, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
```
- **predawn_doorway_clock — 6 — S024–S029**（doorway pre-dawn・a clock with no readable time＝6am の alibi）
- **empty_bed_absence — 6 — S030–S035**（**empty made bed in cold light・被害者なし・暴行なし・遺体なし・血なし**・the room as absence）
```
- `S030.png`
An empty, neatly made bed in a cold, still bedroom rendered as absence in evidence-blue light, no person, no victim, no violence, no blood, no weapon, only a quiet emptied room, no readable text [STYLE] Avoid: [NEG]
```
- **★HP police_lights_cold — 6 — S036–S041**（anonymized officers and worried neighbors seen from behind/in shadow as a suburban home fills with cold police lights・adults only・no identifiable face）
```
- `S036.png`
Anonymized police officers and neighbors seen only from behind and in cold silhouette gathering outside a suburban Texas house ringed by police lights at dusk, small figures dwarfed by the moment, no faces, no crime imagery, no readable text [HSTYLE] Avoid: [HNEG]
```
- **husband_assumption_mechanism — 6 — S042–S047**（"the husband did it" を abstract mechanism に＝conclusion written first・gears）
- **stomach_clock_debunked — 4 — S048–S051**（time-of-death を bent の clock hand で象徴＝discredited science・可読数字なし）
- **★HP child_account_written_thrown — 5 — S052–S056**（an anonymized ADULT investigator's hands writing the account into a record, then it drops into a drawer; **the child only as a small non-identifiable hand near a crayon monster scrawl — never a child's face**）
```
- `S052.png`
An anonymized adult investigator's hands seen from behind writing a statement into a record book under cold light, a child's small crayon monster drawing beside it, the account being taken down before it is thrown away, no identifiable child, no face, the writing an unreadable smear, no readable text [HSTYLE] Avoid: [HNEG]
```
- **green_van_foreshadow — 2 — S057–S058**（a cold distant green van shape behind a house・abstract・no plate・no face）
```
- `S057.png`
A cold, distant dark-green van parked behind a suburban house near a wooded treeline at dusk, seen only as a far shape in evidence-blue light, a stranger's vehicle, no license plate, no person, no readable text [STYLE] Avoid: [NEG]
```
- **bandana_foreshadow — 2 — S059–S060**（S060 は also_thumb・**a strip of blue bandana cloth glimpsed cold in a dark evidence drawer, ignored＝the buried truth**）
```
- `S060.png`
A folded strip of blue bandana cloth lying in a dark forensic evidence drawer, caught by a single cold evidence-blue edge of light and then ignored, the untested object, not bloody or graphic, no person, no readable text [STYLE] Avoid: [NEG]
```

### ACT 2 — THE TRIAL（55枚・S061–S115・engine・最密）
- **county_courthouse — 8 — S061–S068**（Williamson County courthouse exterior/columns・cold institutional）
- **★HP courtroom_thin_case — 8 — S069–S076**（a 1987 courtroom with anonymized jurors in the box and a gallery seen from behind/soft-focus・a defense table・thin case・adults only・no identifiable face・no likeness）
```
- `S069.png`
A 1987 Texas courtroom seen from the back, anonymized jurors in the jury box and a gallery of spectators rendered as shadowed non-identifiable backs and soft-focus shapes, a cold thin case, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **no_physical_evidence — 6 — S077–S082**（the absence of physical evidence＝an empty evidence table・a blinking cursor・nothing tying Morton）
```
- `S077.png`
An empty forensic evidence table under one cold evidence-blue light with nothing on it, the absence of any physical evidence, symbolic emptiness, no person, no readable text [STYLE] Avoid: [NEG]
```
- **buried_file_drawer — 10 — S083–S092**（the sheriff's file full of the true story kept in the dark・drawers closing・folders in shadow＝the mechanism image）
- **withheld_the_boy — 4 — S093–S096**（Eric's crayon-monster account kept from the jury・drawer closing over the scrawl）
- **withheld_green_van — 4 — S097–S100**（the green van sighting hidden・a far van shape sealed in a folder）
- **withheld_bandana — 4 — S101–S104**（the blue bandana untested・~100 yds near a construction site・sealed away・not graphic）
- **withheld_stolen_checks — 4 — S105–S108**（missing purse・a credit card/checkbook used far away in San Antonio＝a stranger's robbery・abstract・no readable numbers）
- **★HP anderson_power_shadow — 4 — S109–S112**（an anonymized powerful prosecutor stand-in as a cold back-lit silhouette at a podium・**NOT a likeness**・非識別・adults only）
```
- `S109.png`
An anonymized prosecutor stand-in at a courtroom podium, seen from behind and back-lit to a hard cold silhouette so no face reads, a figure of institutional power addressing an unseen court, no likeness of any real person, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP conviction_life — 3 — S113–S115**（Feb 1987 conviction・life・an anonymized figure at a defense table seen from behind as heavy doors close・adults only・no face）

### ACT 3 — TWENTY-FIVE YEARS（40枚・S116–S155・slow・earned breaths）
- **prison_exterior_nonsensational — 8 — S116–S123**（S116–S119 = 象徴 exterior [STYLE]/[NEG]・daytime concrete/fence・非扇情・no gore／**★HP S120–S123 = anonymized inmates and a guard seen from behind in a yard/corridor** [HSTYLE]/[HNEG]・adults only・non-sensational・no face・no violence）
```
- `S120.png`
Anonymized prison inmates and a guard seen only from behind and in cold silhouette in a bare daytime yard, small still figures, non-sensational and dignified, no faces, no gore, no violence, no readable text [HSTYLE] Avoid: [HNEG]
```
- **twentyfive_years_scale — 6 — S124–S129**（the weight of 25 years・abstract・a long institutional passage of time）
- **cell_window_seasons — 8 — S130–S137**（**a single cell window・seasons crossing・color-temp shift・calendar-flip 禁止**・earned breath）
```
- `S130.png`
A single institutional cell window abstracted to a pale rectangle of cold light, the color temperature shifting from winter to thin summer across it, seasons passing with no calendar and no person, no readable text [STYLE] Avoid: [NEG]
```
- **son_grows_absence — 4 — S138–S141**（the son growing up in absence＝empty chairs of missed years・**no identifiable child**）
- **★HP lawyer_wont_quit — 6 — S142–S147**（anonymized lawyers who won't quit・a pro-bono figure at a desk seen from behind + hands on a case file under a desk lamp・adults only・非識別・no likeness）
```
- `S142.png`
An anonymized lawyer stand-in seen from behind at a desk late at night, hands on an open case file under a single lamp, the pro-bono fight that would not quit, no face, the papers an unreadable smear, cold evidence-blue light, no readable text [HSTYLE] Avoid: [HNEG]
```
- **bradley_wall_six_years — 4 — S148–S151**（the six-year wall against the DNA test・a cold barrier・a locked gate）
- **order_to_test_and_anchor — 4 — S152–S155**（S155 は also_thumb・S152–S154 the June 2011 order to test the bandana / S155 = **a single cell window with seasons crossing, the quarter-century anchor**）
```
- `S155.png`
A single prison cell window as a cold pale rectangle with the faint trace of seasons crossing it, the quarter-century rendered as one quiet aperture of light, no person, no calendar, no readable text [STYLE] Avoid: [NEG]
```

### ACT 4 — WHAT THE BANDANA KNEW（45枚・S156–S200・climax・cascade・最密②）
- **bandana_tested — 6 — S156–S161**（the blue bandana finally in a lab・tested・cold evidence-blue）
- **two_people_on_it — 4 — S162–S165**（two people's biology on the cloth＝Christine + an unknown man・abstract・no gore）
- **dna_bands_flood_blue — 8 — S166–S173**（S170 は also_thumb・**cold evidence-blue gel-electrophoresis bands igniting and FLOODING the frame＝the visual climax**）
```
- `S170.png`
A ladder of cold evidence-blue gel-electrophoresis bands igniting and flooding a near-black frame with cold blue light, one lane resolving to a single match, the forensic hinge, abstract, no readable numerals, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP norwood_named — 6 — S174–S179**（Mark Norwood＝a separate anonymized cold silhouette・a drifter the evidence described・convicted・**NOT a likeness・no glorification・no lurid**・non-identifiable）
```
- `S174.png`
A single separate anonymized silhouette of a drifter standing apart in a cold, hard evidence-blue light, seen only as a dark back at a distance, the man the DNA identified, no face, no likeness, no glorification, no readable text [HSTYLE] Avoid: [HNEG]
```
- **baker_gutpunch — 5 — S180–S184**（**Debra Baker・a second real victim・killed Jan 1988 while Morton was already imprisoned**・an empty Austin home of absence・dignity・**no violence・no victim depiction**）
```
- `S180.png`
An empty, quiet Austin home interior rendered as cold absence, standing for a second life lost while the wrong man sat in prison, no person, no victim, no violence, dignified emptiness, no readable text [STYLE] Avoid: [NEG]
```
- **★HP morton_walks_free_gold — 5 — S185–S189**（**Morton walks free・the FIRST Texas homecoming-gold**・S185 = a gate/threshold opening to warm light [STYLE]/[NEG]／**S186–S189 = an anonymized man seen from behind walking out into warm homecoming-gold** [HSTYLE]/[HNEG]・非識別・no face）
```
- `S186.png`
A single anonymized man seen only from behind walking out through an opening prison gate into a wide band of warm Texas homecoming-gold light breaking a cold blue morning, free and dignified, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP anderson_reckoning — 6 — S190–S195**（the Court of Inquiry・an anonymized figure led away seen from behind・**the scale tipping** (25 years ↔ days)・Anderson's fall・license surrendered・非識別・NOT a likeness）
```
- `S190.png`
An anonymized man in a suit seen only from behind being led away down a cold courthouse corridor, a figure of authority brought to account, no face, no likeness of any real person, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP morton_act — 5 — S196–S200**（**the Michael Morton Act**・an anonymized man seen from behind at a Texas capitol legislative podium・the law that protects the innocent・warm homecoming-gold・非識別）
```
- `S198.png`
An anonymized man stand-in seen only from behind at a legislative podium in a warm Texas capitol chamber, anonymized legislators as soft-focus backs beyond him, turning stolen years into reform, homecoming-gold light, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 5 — ENDING（15枚・S201–S215・the truth lands last・strip to essentials）
- **back_to_child — 4 — S201–S204**（back to the three-year-old's voice・the crayon monster un-buried・the drawer opening again）
- **everything_true — 4 — S205–S208**（every word the boy said was true＝the monster, the mustache, daddy not home・symbolic）
- **truth_never_missing — 4 — S209–S212**（the truth was in the file the whole time・a folder in a shaft of cold light・waiting to be believed）
- **final_breath — 3 — S213–S215**（strip to essentials＝the drawer・the blue bandana・a dawn edge・restraint returns・冷 blue に homecoming-gold の一筋）

## 5.7 幕別 motif 枚数の検算（★Codex は書き終えたら足して確認）

```
ACT0  : 4+3+4+4 = 15
ACT1  : 8+6+6+6+6+4+5+2+2 = 45
ACT2  : 8+8+6+10+4+4+4+4+4+3 = 55
ACT3  : 8+6+8+4+6+4+4 = 40
ACT4  : 6+4+8+6+5+5+6+5 = 45
ACT5  : 4+4+4+3 = 15
合計   : 15+45+55+40+45+15 = 215 ✓
★human-present(★HP) body: 11(ACT1)+15(ACT2)+10(ACT3)+22(ACT4) = 58 / 215 = 27.0%（残り157は object/symbolic）
```
> **S001..S215 の連番が穴なく215行**そろっていることを `--only S001` の `shots=261`（215 body + 43 i2v種 + 3 thumb_face）で確認する。**★HP 58枚は `[HSTYLE]`/`[HNEG]`（匿名人物）、残り157枚は `[STYLE]`/`[NEG]`（人物なし）を連結。**

## 5.8 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_morton_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.9 パーサ契約（`read_prompts()` はこの2行形式しか読まない）

```
- `S001.png`
<positive prompt> Avoid: <negative>
```
- **1行目:** `` - `S001.png` ``（バッククォート囲み・行末は `.png` の直後）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト
- `ai_prompts.v001.md` は **body 215行（S001..S215）＋ i2v 種 43行（M01_src..M43_src、§8.1a）＋ thumb_face 3行（T01_face..T03_face、§5.12）＝ 261 エントリ**を書く。すべて1枚生成。

## 5.10 生成コマンド（★variants 指定なし。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=261 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 52 --only S001
#   → ログ "episode=... shots=261 ... -> N images" の shots が 261 であること（215 body + 43 i2v種 + 3 thumb_face）

# 全261枚（body 215 + i2v種 43 + thumb_face 3・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-052-morton
```
> QC で落ちたシーンの再生成は `--only S###`（同じプロンプトで別シードを1枚）。**基準を下げない・水増ししない。**

## 5.11 ★人物画像（匿名・ドラマ化スタンドイン）— HUMAN-FIGURE prompts（★18本・i2v 種の内数）＋ ★HP body still の style

> **owner directive（EP48/49 の「空/寂しい・人がいない」却下を潰す）: 匿名・非識別の人物を増やす。** 実在人物（Morton/Christine/Eric/Norwood/Anderson/Bradley/Raley/判事）の **likeness を作らない**。実在人物が示唆される所は顔を非識別（背向き/横顔を影に/逆光でシルエット化/目から下でクロップ/浅い被写界深度でソフト・**adults only**）。**被害者・暴行・殺害・遺体を絶対に描かない（R-VICTIM 継続）。3歳 Eric は本シリーズに出さない**（子供の識別可能な顔を作らない＝Eric は小さな手のみ・§5.6 の象徴レーン限定）。
> **★この `[HSTYLE]`/`[HNEG]` は (a) 18本の i2v 人物種、(b) §5.6 の ★HP body still 58枚、の両方に使う。**

### ★lane 定義（人物は動かす＝紙芝居にしない → H は motion レーンへ・★8→18 に増量・locked counts 不変）

**H001–H018 は「新規の静止カット」ではなく、既存 43本の i2v 種のうち 18本の中身（＝人物ビート）として作る。additive にしない（object 種を人物種に転換）。**
- **role = `i2v_source`**（body には回さない）。**43本の i2v 種のうち ★18本を人物ビートに充て**、残り **25本を抽象/象徴種**（§8.1a）。per-act の内数として人物種を **ACT1×5・ACT2×5・ACT3×4・ACT4×4 ＝18** 充てる（§4.5 の M04/M06/M07/M09/M10・M13/M14/M16/M19/M20・M22/M23/M24/M25・M34/M35/M38/M39）。ACT0/ACT5 は象徴のまま。
- **asset_id は既存の i2v 種 ID 空間（`^MOR-MS\d{2}$`）の 18本を占有**する（H001–H018 は本書内のラベル）。種画像ファイルは `M<NN>_src.png`。`public_path==null`。
- 各人物種は **Wan → RIFE（§8）で motion 化**され、**43本の motion のうち 18本**になり、**86 motion カットのうち最大 36カット**に出る＝**人物が動く**（＝「空/寂しい」を潰す）。
- **QC フラグ:** `has_human_body:true`（許可）・`has_identifiable_real_person:false`（必須）・`has_readable_text:false`（必須）・`has_victim_or_violence:false`（必須）。§8.5 で「実在 likeness/被害者/暴行なし・顔は非識別・adults only（子供顔なし）」を確認。
- **★locked counts は1つも変わらない（object→human の転換のみ・additive しない）:** still_body **215**（＝object 157 ＋ ★HP human-present 58）/ still_i2v_source **43**（＝抽象 25 ＋ 人物 18）/ motion **43** / factory **240** / overlay **30** / thumb_face **3**；cuts **250/240/86 = 576**；still-share **0.4340**；first-use **0.8646**；avg-uses **1.157**。**H は 43 i2v 種の内数なので新規行を増やさない。**

**共通スタイル `[HSTYLE]`（各 H プロンプト末尾に全文連結・匿名/非識別/photoreal/cold evidence-blue）:**
```
, cinematic photoreal still, documentary reenactment stand-in, a generic anonymized person who resembles no real individual, face kept non-identifiable — turned away, in profile lost to shadow, back-lit to a silhouette, cropped below the eyes, or thrown soft in shallow focus, a cold forensic evidence-blue key light as the one recurring cool note, near-black ink institutional gravity, low-key deep-shadow lighting, telephoto compression, shallow depth of field, restrained dignified framing, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no readable documents, a single warm Texas homecoming-gold note only where the beat is release or exoneration
```
**共通ネガティブ `[HNEG]`（各 `Avoid:` の後に全文連結・匿名人体は許可、実在 likeness/被害者/暴行/可読テキストは禁止）:**
```
recognizable real person, likeness of a specific person, Michael Morton, Christine Morton, Eric, Mark Norwood, Ken Anderson, John Bradley, John Raley, any real judge or juror, celebrity, mugshot, deepfake, text, words, letters, numbers, captions, watermark, logo, readable document, legible case file, legible newspaper, legible report, legible date, license plate, the victim, murder victim, beaten body, corpse, any depiction of the murder or attack, violence, blood, gore, injury, weapon, sexual content, nudity, crime scene, re-enactment of the attack, an identifiable child, crying toddler, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, milky haze, scanline
```

### 人物ビート（★18本・全て匿名・非識別・実在 likeness なし・adults only・i2v 種として motion 化）
```
- `H001.png`  (= M04_src.png · ACT1 · Michael leaves for work ~6am)
A single anonymous man stand-in stepping out of a suburban house doorway into pre-dawn darkness, seen from behind and back-lit so no face reads, an ordinary morning departure, cold evidence-blue light, no identifiable features, no readable text [HSTYLE] Avoid: [HNEG]
- `H002.png`  (= M06_src.png · ACT1 · father returns, child's hand)
An anonymous man seen from behind holding a small child's hand outside a suburban house ringed by cold police lights at a distance, both non-identifiable, the moment an ordinary life ended, no faces, no crime imagery, no readable text [HSTYLE] Avoid: [HNEG]
- `H003.png`  (= M19_src.png · ACT2 · the prosecutor)
An anonymous prosecutor stand-in standing at a courtroom podium, seen from behind and three-quarter with the face lost to shadow, addressing an unseen jury in a cold Texas courtroom, dignified and grave, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `H004.png`  (= M13_src.png · ACT2 · hands bury the file)
Close on a pair of anonymous hands sliding a plain file folder into a dark drawer and pushing it shut under cold evidence-blue light, the evidence being kept from the defense, no face, no legible document [HSTYLE] Avoid: [HNEG]
- `H005.png`  (= M23_src.png · ACT3 · the years)
A lone anonymous man stand-in sitting on the edge of a bunk in a bare prison cell, seen from behind with the face lost to shadow, small and still in the frame, the stolen years, dignified and non-sensational, cold light, no gore, no readable text [HSTYLE] Avoid: [HNEG]
- `H006.png`  (= M24_src.png · ACT3 · the lawyer who won't quit)
Anonymous lawyer's hands on an open case file under a single desk lamp late at night, seen over the shoulder so no face reads, the pro-bono fight that would not quit, the papers blurred illegible, cold light, no readable text [HSTYLE] Avoid: [HNEG]
- `H007.png`  (= M34_src.png · ACT4 · Morton walks free)
A single anonymous man stand-in walking out through an opening prison gate into warm Texas homecoming-gold light, seen from behind facing the light, free and dignified, no face visible, no readable text [HSTYLE] Avoid: [HNEG]
- `H008.png`  (= M38_src.png · ACT4 · testifying for the Act)
An anonymous man stand-in at a legislative podium in a Texas capitol chamber, seen from behind addressing an unseen chamber, turning his stolen years into reform, warm homecoming-gold light at the edge, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H009.png`  (= M07_src.png · ACT1 · police arrive)
Anonymized police officers and worried neighbors seen only from behind and in cold silhouette gathering outside a suburban house ringed by police lights at dusk, small figures, no faces, no crime imagery, no readable text [HSTYLE] Avoid: [HNEG]
- `H010.png`  (= M09_src.png · ACT1 · the time-of-death is estimated)
Anonymized investigators' hands and shadowed backs over a clipboard and a chart under cold light, reverse-engineering a time of death, seen from behind so no face reads, the papers an unreadable smear, no readable text [HSTYLE] Avoid: [HNEG]
- `H011.png`  (= M10_src.png · ACT1 · the boy's account is written down)
An anonymized adult investigator's hands seen from behind writing a statement into a record book, a child's small crayon monster drawing beside it, taking down the account, no identifiable child, no face, unreadable writing, no readable text [HSTYLE] Avoid: [HNEG]
- `H012.png`  (= M14_src.png · ACT2 · the stranger in the green van)
A single anonymized man seen only from behind at a cold distance getting out of a dark-green van behind a house and walking toward a wooded treeline at dusk, the stranger the evidence described, no face, no license plate, no readable text [HSTYLE] Avoid: [HNEG]
- `H013.png`  (= M16_src.png · ACT2 · the stolen card is used far away)
Anonymized hands using a card at a store counter far away in cold light, a stranger spending a dead woman's money, seen over the shoulder so no face reads, the card and receipt an unreadable smear, no readable text [HSTYLE] Avoid: [HNEG]
- `H014.png`  (= M20_src.png · ACT2 · the verdict lands)
A 1987 courtroom seen from the back as a verdict lands, anonymized jurors in the box and a gallery of spectators as shadowed non-identifiable backs and soft shapes, cold light, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H015.png`  (= M25_src.png · ACT3 · lawyers fight over the DNA test)
Two groups of anonymized lawyers seen from behind and in silhouette arguing across a cold conference table, a six-year fight over a simple test, no faces, no likeness, the documents an unreadable smear, no readable text [HSTYLE] Avoid: [HNEG]
- `H016.png`  (= M22_src.png · ACT3 · the years inside)
Anonymized prison inmates and a guard seen only from behind and in cold silhouette in a bare daytime yard, small still figures across a quarter-century, non-sensational, no faces, no gore, no violence, no readable text [HSTYLE] Avoid: [HNEG]
- `H017.png`  (= M35_src.png · ACT4 · the homecoming)
A small anonymized family and crowd seen only from behind reaching toward a man walking into warm Texas homecoming-gold light, a homecoming, all non-identifiable, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `H018.png`  (= M39_src.png · ACT4 · the Act passes)
An anonymized legislative chamber seen from the back, rows of legislators as soft-focus non-identifiable backs rising as a reform bill passes, warm homecoming-gold light, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
> **★H↔M 対応（§4.5 と一致・18本）:** H001=M04 · H002=M06 · H003=M19 · H004=M13 · H005=M23 · H006=M24 · H007=M34 · H008=M38 · **H009=M07 · H010=M09 · H011=M10 · H012=M14 · H013=M16 · H014=M20 · H015=M25 · H016=M22 · H017=M35 · H018=M39**。`ai_prompts.v001.md` では**新規行を足さず**、該当する 18本の `M<NN>_src.png` 行を上記の人物内容＋`[HSTYLE]`/`[HNEG]` で書く（`shots=261` 維持）。§8.5 で目視確認（adults only・子供顔なし・被害者/暴行なし・実在 likeness なし）。

## 5.12 ★サムネ用 emotive-face 静止画（3枚・CTR §4A・thumb_face）

> **owner directive（CTR_PLAYBOOK §4A・emotive face が lane の #1 CTR driver）:** サムネは **単一の AI 生成・非実在・illustrative/dramatized な顔**を peak emotion で。**実在人物（Morton/Anderson 等）の likeness を作らない**＝clearly illustrative（semi-painterly, cinematic-render）にして「実在被告/検事の実写」に読ませない＝likeness firewall。**被害者・暴行・子供の顔を作らない。** これらは **本編カットに出ない thumbnail 専用**（role=thumb_face・public_path null・distinct/cuts に数えない・§3.1）。B が `MortonThumbnails.tsx` で face＋2–4語 hook text を合成。

**共通スタイル `[TSTYLE]`:**
```
, thumbnail key art, a single non-real dramatized generic human character rendered in a clearly illustrative semi-painterly cinematic style so it never reads as a real photograph of a real person, face occupying 50 to 65 percent of frame height with eyes on the upper third, bright key light on the face and a rim light separating it from a dark desaturated blurred Texas background of a courthouse or prison at dusk, skin warm, background cool, high contrast and vivid, one clean quadrant of negative space for text, 1280x720, ultra-detailed
```
**共通ネガティブ `[TNEG]`:**
```
photoreal photograph of a real person, likeness of Michael Morton or Christine Morton or Mark Norwood or Ken Anderson or any real defendant or prosecutor or judge, recognizable real celebrity, deepfake, a real child, the victim, murder victim, blood, gore, violence, weapon, text, words, letters, numbers, watermark, logo, two faces, tiny face, neutral expression, dark muddy low-contrast mush, cartoon flatness, extra limbs, deformed, warped
```
```
- `T01_face.png`
A non-real dramatized generic middle-aged man's face in an illustrative cinematic style at peak emotion — a hollow, dread-filled, wronged stare gazing slightly off-camera, the look of a man convicted of a crime he did not commit, pushed to the right third over a dark blurred prison-fence background at dusk, warm rim light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
- `T02_face.png`
A non-real dramatized generic older man's face in an illustrative cinematic style with a cold, smug, unrepentant authority glare looking directly at the viewer, the corrupt-prosecutor archetype, pushed to the left third over a dark blurred courthouse-columns background, hard rim light, clean negative space on the right [TSTYLE] Avoid: [TNEG]
- `T03_face.png`
A non-real dramatized generic man's face in an illustrative cinematic style with a single silent tear and a stunned, released expression, the moment of exoneration, pushed to the right third over a dark blurred courthouse background with a first band of warm dawn light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
```
> ★これら3枚は `role:"thumb_face"`・`public_path:null`・`has_human_body:true`・`has_identifiable_real_person:false`。§6 の目視で「実在 likeness でない・illustrative・被害者/子供なし」を確認。B のサムネ案（§CODEX_B §12）はこの T01–T03 を前景に、§4.3a の also_thumb body（背景）＋ 2–4語 hook（CTR §4A・red bar or yellow caps）で組む。

---

# 6. A-2/A-3: 静止画のQC・目視（★depth map なし）

## 6.1 機械QC（body 215 + i2v種 43 + thumb_face 3 = 全261枚・`qc_morton_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `18.0<=mean_luma<=225.0`（near-black ink・cold-blue の低照度が多い→黒潰れ注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**衝突は house/bed(S016/S030系)・drawer(S005/S083系/S194)・bandana(S060/S101/S156系)・DNA band(S166–S173/S170)・cell window(S130–S137/S155)・courthouse(S061–S068)・prison(S116–S123) の被りに注意** | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・日付(1986/1987/1988/2011/2013)・年齢(3/32)・金額($1.96M)・DNA・file/report/newspaper のロゴが写っていないか | `has_readable_text=true`→reject |
| Q6 | **実在人物**の顔の混入 | **目視。** 実在人物として識別可能な顔（Morton/Christine/Eric/Norwood/Anderson/Bradley/Raley/判事に**似た**顔）が写っていないか。**匿名・非識別の顔（H/thumb_face）は OK。** | `has_identifiable_real_person=true`→reject |
| Q7 | 被害者/暴行/遺体/子供 | **目視。** 被害者の描写・暴行/殺害/injury/blood/凶器・**識別可能な子供の顔**が写っていないか。**★匿名の人体は OK（`has_human_body=true` 単独では reject しない）。** | 被害者/暴行/遺体/識別可能子供があれば reject |

**Q5/Q6/Q7 は機械で判定しない。全261枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-052-morton --media image
#   → runs/qc/morton_footage_contact_NN.png（20枚/シート・約14シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-51 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** 特に **S030系(empty bed)は被害者/血/遺体が写らないこと、S001/S052(crayon monster)は識別可能な子供顔が無いこと、S060/S101/S156(bandana)は blood-graphic でないこと、S170(DNA band)は読める数字が無いこと、S109/S174/H003(prosecutor/Norwood 影)は実在 likeness に転じないこと、T01–T03(thumb face)は illustrative で実在被告/検事に似ていないこと、を必ず目で確認する。**

## 6.2 出力
```
episodes/PD-2026-052-morton/05_visuals/still_qc.v001.json     # 261枚全部の行（reject も残す）
```

## 6.3 accepted が (body215 / i2v43 / thumb3) に届かなかったとき
```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 52 --only S###   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_morton_stills.py
```
accepted body >= 215 かつ i2v_source >= 43 かつ thumb_face >= 3 になるまで繰り返す。**基準を下げない・水増ししない。**

## 6.4 ★depth map は生成しない（本作は depth treatment 不使用）
**DESIGN §1 の hard rule により footage/still treatment は `bleed`/`parallax`/`duotone`/`focus` のみ・`depth` を使わない**（depth displacement は被写体を melt/warp させる＝EP48/49 の warp 欠陥）。したがって **`gen_depth_maps.py` を回さない・`<stem>_depth.png` を作らない・マニフェストに `depth_path` を持たせない**（§4.1a/§4.2-19）。B の render も depth を参照しない（CODEX_B §5.3）。

---

# 7. A-4: factory 実写クリップ 240本の選定と全点目視QC

## 7.1 在庫の実態
```
H:\pd-media\assets\factory\   フラット構成（backgrounds 11,000本超・light_assets・particle_assets・vfx_overlays・texture_assets・loops）
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json（★必ず encoding="utf-8" で開く）
```

## 7.2 選定条件
- **`kind=="video"` のみ。** 静止画 factory は使わない
- **240本ちょうど**（§3.3[8] より still-share≤0.45 を守る設計値）
- **各1回しか使わない**（`MAX_USES_FACTORY=1`）
- 幕別割り当て（§4.4）: HOOK+OPENING=12 / ACT1=45 / ACT2=40 / ACT3=50 / ACT4=45 / ACT5=15 ＋ 繋ぎ=33 ＝ 240
- **EP39〜EP51 の絵柄を選ばない（§7.7 の分離語）。** EP52 は 1986 Texas suburban house/street・supermarket exterior・Williamson County courthouse/records/evidence room・Texas prison exterior（非扇情）・DNA lab・Texas capitol/legislature・warm dawn。**被害者/暴行/泣く人/遺体/実在の顔が写るニュース映像を選ばない。鉄格子内部の gore を選ばない。EP47 の two-lane road/pickup・EP41 の sodium prison corridor・EP44 病院・EP49 Utah 駐車場を選ばない。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query williamson_county_courthouse --limit 60 --exclude-used --ep PD-2026-052-morton --json
```
`--exclude-used` は出荷ゲート `arc_nonrepeat` と同じ指紋集合を使う。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・§4.4 に pre-assign 済み）
> **★`covers_scene_id` は still 資産 ID 空間（S001..S215）を指す。** §4.4 の各エントリに pre-assign 済み（約24本が covers 付き、残りは null の繋ぎ/情景）。

| covers（例） | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S005/S008 | evidence/records room・cold | `evidence_room` / `records_archive` | 0 |
| S016/S024/S030 | Texas suburban house/street/empty bedroom | `texas_suburban_house` / `suburban_street_dawn` / `empty_bedroom` | 1 |
| S061/S069/S083 | Williamson County courthouse/courtroom/evidence locker | `county_courthouse` / `empty_courtroom` / `evidence_locker` | 2 |
| S116/S130/S142 | Texas prison exterior/cell window/lawyer desk | `prison_exterior_day` / `cell_block_window` / `lawyer_office_lamp` | 3 |
| S156/S166/S185/S196 | DNA lab/gel equipment/prison gate/Texas capitol | `dna_lab` / `gel_electrophoresis` / `prison_gate` / `texas_capitol` | 4 |
| S201/S215 | empty bedroom/file drawer/Texas dawn edge | `empty_bedroom` / `file_drawer` / `dawn_edge` | 5 |

**残りは covers を持たない繋ぎ・情景**（institutional 廊下・marble・file cabinets・dry-brush texture・sky gradient・cityscape・landscape・water reflection）。**暗いクリップに偏りすぎない**（暗側は約80本まで＝1/3・courthouse 昼光・warm dawn・lab の実用光を混ぜる）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）
```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.4a ★★★ 実写ストックライブラリを必ず使う（EP48/49 の burned lesson＝実写0本を潰す）★★★
> **owner directive:** EP48/49 は本編を AI still + AI-i2v で組み、**ダウンロード済みの実写ストックを1本も使わなかった**。本作はこれを潰す。**factory 240レーンの調達源に、既存 factory 在庫だけでなく下記ストックを必ず含める。**
- **ストックライブラリ:** `H:\pd-media\assets\stock`（マニフェスト `STOCK_MANIFEST.json`・**動画 74本 ＋ 静止 155本**・pexels/pixabay・**商用可**）。
- **調達方針（★counts は固定・factory 240 を変えない。レーン内の調達源を広げるだけ）:**
  1. `STOCK_MANIFEST.json` を読み、**意味（§7.3 の covers カテゴリ: courthouse/Texas suburb/prison/lab/records/capitol/dawn 等）に一致し §7.5 の全点目視 QC と R-FACE/R-VICTIM を通る実写動画を優先採用**（目標: 通る限りの stock 動画 74本を factory 240 に組み込む・無理な水増しはしない）。
  2. 残り枠を `H:\pd-media\assets\factory` 在庫で埋める。
  3. 各 factory エントリの出所（`origin`: `stock` or `factory`）を `factory_selection.v001.json`（§7.6）と `stock_ledger.v001.json`（§10.2）に記録。
  4. **ストック静止 155本は本編 body still（AI 215）レーンに混ぜない。** 使う場合は face-free/text-free のもののみ factory/情景レーン扱いに限る。
- **★R-FACE/R-VICTIM を絶対順守:** 実在の判事/警官/Morton/Norwood/Anderson/被害者が写るニュース映像・被害者/暴行/遺体/gore を含むクリップは**ストックでも使わない**。EP39〜51 との sha256 被りゼロ（§7.7）はストック由来にも適用。
- **★カラーマッチは B が担当:** pexels/pixabay の発色バラつきは B が cold evidence-blue の neutral グレードで AI still に合わせる（CODEX_B §5.8(d)・**milky wash にしない**）。

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★
> **実際に起きた事故（EP36 大聖堂・EP38 牛）。** `subtype` は「その検索語で取った」記録であって中身の保証ではない。**240本は分割して全点見る。**

**選抜240本は例外なく次を経る:**
```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-052-morton --media video --dir "<240本の staging フォルダ>"
```
1. コンタクトシートを開き **240本すべてを1本ずつ見る**
2. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて選定から外す（差替え）
3. 実写シネマティックB-roll・EP52テーマ・ウォーターマークなし・識別可能な実在人物なしを確認
4. **★制約2/3の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。**被害者/暴行/遺体/泣く人/gore・実在の判事/警官/Morton/Norwood/Anderson の顔が写るニュース映像・鉄格子内部の gore を使わない。EP47 two-lane/pickup・EP41 sodium prison・EP44 病院・EP49 Utah を含むクリップを使わない。**
5. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=42.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。**暗いクリップは約80本（1/3）までに抑え、courthouse 昼光・warm dawn・lab の実用光を混ぜる。**

## 7.6 出力
```
episodes/PD-2026-052-morton/05_stock/factory_selection.v001.json   # 選定理由・幕割り当て・origin
episodes/PD-2026-052-morton/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP51 との重複ゼロ（BLOCKING）
```bash
./.venv/Scripts/python.exe scripts/select_morton_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-051-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP52 の240本の積集合が**空**であることを確認。1件でも exit 1。**EP39〜EP51 のファイルは読むだけ。**

**分離レーン（色・素材・語）:** EP41 gold（監獄）／EP42 blue（ankle monitor）／EP43 amber／EP44 teal（病院）／EP45 crimson／EP46 green／EP47 civil-violet（two-lane Texas road/pickup）／EP48 glover／EP49 somber-plum（Utah）／EP50 steel-cyan。**EP52 = cold evidence/bandana-blue `#3F5E8C`（INK `#0B0C10`）＋末端のみ Texas homecoming-gold `#D19A3E`。** これら他話の絵柄・色・被写体を1本も選ばない。

---

# 8. A-5: i2v モーション化 43本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする43本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）
種画像は §5 と同じ `generate_sdxl_4k.py`（variants なし）で `M<NN>_src.png` として生成（`ai_prompts.v001.md` に §8.1a の43行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `MOR-MS01..MS43`、モーション成果物は `MOR-M01..M43`。**幕別配分は §4.5 に pre-assign 済み**（ACT0 3 / ACT1 8 / ACT2 9 / ACT3 8 / ACT4 11 / ACT5 4 = 43）。
> **★このうち ★18本は §5.11 の匿名人物ビート（H001–H018）＝43本の内数**（M04/M06/M07/M09/M10/M13/M14/M16/M19/M20/M22/M23/M24/M25/M34/M35/M38/M39）。**残り 25本が抽象/象徴種。**

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの43行を追加・各1枚・**poised-still の source**）
> 各種プロンプトは §5.6/§4.5 の対応 tag の「動く直前の poised-still」版。**動きが意味を持つ絵**（DNA bands が ignite する直前・drawer が閉じる直前・crayon monster が埋まる直前・green van が動く直前・gate が開く直前 等）。末尾に §5.3 `[STYLE]` ＋ `Avoid:` §5.4 `[NEG]`（人物種は `[HSTYLE]`/`[HNEG]`）を全文連結。**下記は代表6例。残り37行は §4.5 の各 storyboard/tags を「poised, still, about to move」で SDXL 化**（M01_src..M43_src を穴なく）。

```
- `M01_src.png`
A small child's hand beside an abstract crayon monster scrawl held still and poised under a single cold evidence-blue edge of light in near-black, a moment before a shadow moves, restraint, no identifiable child, no face, no readable text [STYLE] Avoid: [NEG]
- `M02_src.png`
A child's crayon monster drawing on a page with a dark institutional file drawer poised just above it about to slide shut, held motionless a moment before it buries the page, cold evidence-blue light, no person, no readable text [STYLE] Avoid: [NEG]
- `M15_src.png`
A folded strip of blue bandana cloth in a dark evidence drawer under a cold evidence-blue edge, held still and poised, the untested object a moment before the drawer closes, not bloody, no person, no readable text [STYLE] Avoid: [NEG]
- `M30_src.png`
A ladder of cold evidence-blue gel-electrophoresis bands in near-black held poised with one lane about to snap into a single aligned bright band and flood the frame, the DNA hinge frozen a moment before it resolves, abstract, no numerals, no people [STYLE] Avoid: [NEG]
- `M33_src.png`
An empty, quiet Austin home interior rendered as cold absence, held still and poised, standing for a second life lost while the wrong man sat in prison, no person, no victim, no violence, no readable text [STYLE] Avoid: [NEG]
- `M35_src.png`
A prison gate poised half-open onto a first band of warm Texas homecoming-gold light breaking a cold blue morning, held a moment before it opens fully, no identifiable person, no readable text [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_centralpark.py` を下敷きにパスと SHOTS だけ差し替え）
```python
HOST = "http://127.0.0.1:8188"
HIGH = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"
LOW  = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"
VAE  = "wan_2.1_vae.safetensors"       # ★2.1（2.2 ではない）
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
WIDTH, HEIGHT = 1280, 720
FRAMES = 41
STEPS = 40 / SPLIT = 20 / SHIFT = 5.0   # ★SHIFT 5.0（8.0 はバグ）
CFG = 3.5 / SAMPLER,SCHEDULER = "euler","simple" / FPS = 16
STILL_DIR     = H:\pd-media\assets\ai\morton
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\morton
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, melting, text, watermark, identifiable face, real person likeness, child face, crying person, victim, corpse, assault, gore, blood"
```
**ゲート:** `dry_validate`（length=5）/ `assert_loaded_completely` / `assert_frame_math`。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す・★43本は複数日）
```bash
py -3.11 scripts/comfy_wan_morton.py --build
py -3.11 scripts/comfy_wan_morton.py --run --shot M01
py -3.11 scripts/comfy_wan_morton.py --run-all
```
1本 24–73 GPU分・43本で 18–50時間。**夜間分割で回す。開始前にマシン状態を確認。**

## 8.4 RIFE で 48fps 化（`rife_morton.py`・`rife_centralpark.py` と同手順）
```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番 → RIFE 2x を2回（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. フレーム数検証 `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC
- 顔・身体・**被害者・暴行・遺体・泣く人・gore**が生成されていないこと（必ず目視・制約2/3/6）
- モーフィング/ちらつき/ワープ/melt が無いこと → あれば別シードで再生成
- Norwood 影・prosecutor 影・H シリーズは**識別可能な実在 likeness**に転じていないこと・**識別可能な子供顔**が出ていないこと
- DNA ladder（M30系）は**可読の数字**が出ていないこと／green van（M14）は plate が出ていないこと／gate（M35）は開く動きが自然なこと
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（43本 × 2回 = 86カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど30本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **15本** | cold room dust・archive/lab dust・dry Texas dust・night air drift。黒背景 drift を screen 合成 |
| `light_assets` | **10本** | cold evidence-blue shaft・cold window bar・cyan-free single lamp・**homecoming-gold edge（exoneration/close 用の少数=L05/L09）** |
| `vfx_overlays` | **5本** | 微細な grain・cold light noise・blue glitch min |
| **合計** | **30本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/morton/overlay/` に置き、`morton_film.json` の `cuts[].src` には**出さない**。**★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない・scanline/CRT/vignette-wash を選ばない（DESIGN §1・CODEX_B §5.9）。** 黒背景でループするものを選び `blend_hint` を書く。発色は B が accent `#3F5E8C` に寄せる想定・homecoming-gold は close 用のみ。他話色を選ばない。§7.5 の目視QC対象（30本）。

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_morton_assets.py`）
```
remotion/public/morton/img/     ← role=body の静止画215枚（★depth なし）
remotion/public/morton/factory/ ← 選定 factory .mp4 240本（§4.4 の F001..F240 名で）
remotion/public/morton/motion/  ← i2v M<NN>_rife.mp4 43本
remotion/public/morton/overlay/ ← 合成レイヤー 30本（§4.6 の P/L/V 名で）
remotion/public/morton/thumb/   ← thumb_face T01..T03（B の MortonThumbnails が参照）
```
- `public_path` はマニフェストの値（§4.4/§4.5/§4.6）と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）
- **★depth の同名ペアは作らない・置かない**（§6.4）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する）:**
- factory の `public_path` は必ず `morton/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も含めない
- 合成レイヤーは `morton/overlay/` に置き `cuts[].src` に出さない

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`
全静止画・i2v・factory・overlay・thumb_face を1行ずつ: `asset_id`/`path`/`source`(`ai_codex`|`factory`|`stock`)/`origin`/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力
```bash
./.venv/Scripts/python.exe scripts/build_morton_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_morton_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_morton_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**★factory 240 / motion 43 / overlay 30 が非空で実体化しているか（不変条件17/18/16）を必ず確認。**

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）
```python
MAX_USES_FACTORY = 1
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
MAX_AVG_USES_PER_SOURCE = 1.4   # ★EP49 は 1.8 で flag された
```
種別判定は**パス文字列**（`kind_of()`）。§10.1 の命名規則を守る。
EP52 の設計値: still 250/215=1.163(≤2) / factory 240/240=1.0(≤1) / motion 86/43=2.0(≤2) / first-use 498/576=0.8646(≥0.70) / avg-uses 576/498=1.157(≤1.4)。**全て達成可能。**

---

# 12. 絶対にやらないこと
- **EP39〜EP51 のファイル・素材に触らない。** 読み取りのみ可。素材・色・音のレーンも分離（§7.7）。EP52 の accent は **cold evidence/bandana-blue #3F5E8C**（INK #0B0C10・末端 homecoming-gold #D19A3E・A は絵で流用色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない**（`remotion/src/**` `scripts/ae/**` `scripts/build_morton_film.py` `manifest.json` `04_scenes/shotlist*` `figures`）。ただし `04_scenes/ai_prompts.v001.md` は A が書く。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness をどこにも作らない**（Morton/Christine/Eric/Norwood/Anderson/Bradley/Raley/Morrison/判事）。**匿名・非識別の一般人は可**（人体そのものは禁止でない）。**被害者の描写・暴行/殺害/遺体 imagery・識別可能な子供顔を一切作らない。**
- **制約に反する文言・絵を作らない**（§1.2/§1.3）: Morton の有罪化／被害者/暴行/遺体の描写／Eric の襲撃視点・識別可能子供顔／Norwood 美化/lurid／hedged 数値の断定／可読の偽公文書／実在人物 likeness／dochighlight／捏造/可読引用／milky wash/scanline。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。（factory の subtype `_02`/`_03` は別素材の意で別物・混同しない。）
- **role=thumb / still_thumb を作らない・overlay を30本以外にしない・thumb_face を3枚以外にしない。** also_thumb は body 4枚（§4.3a）。
- **★factory 240 / motion 43 / overlay 30 の配列を空・stub のまま出荷しない**（EP45/EP38 事故・§4.4/§4.5/§4.6 を実体化）。
- **★depth map を生成しない・`depth_path` を持たせない**（§6.4・DESIGN §1）。
- **★dochighlight figure を作らない・言及しない**（grep で 0）。
- **枚数を「だいたい」で決めない。** §3 の確定値（still 215 / factory 240 / i2v 43 / thumb_face 3 / distinct 498 / first-use 0.8646 / still-share 0.4340 / avg-uses 1.157 / overlay 30）と §3.3 の検算をそのまま使う。合わなければ本書を疑って報告。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** 生成物・在庫クリップを実際に見る。

---

# 13. 完了報告に含めるもの
```
1. accepted 静止画の枚数と内訳（body 215 [＝object 157 ＋ ★HP human-present 58 = 27%] / i2v_source 43 [＝抽象 25 ＋ ★人物 18] / thumb_face 3 / also_thumb 4 [§4.3a] / reject N）
2. factory 選定 240本のリスト（asset_id / subtype / origin / eyeballed_content）と、subtype と食い違って外した本数、
   bandana/DNA band/prison/empty-bed クリップの「no readable text / no logo / no face / no victim / no gore」確認、stock 由来の本数
3. EP39〜EP51（十三話）重複ゼロの確認結果
4. i2v 43本の frames / duration_sec と、SHORT? の有無、**★H001–H018（18本）の匿名・非識別・adults-only・no-victim 確認**、★HP body 58枚が匿名・非識別・実在 likeness なし・識別可能子供顔なしの確認
5. 合成レイヤー30本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code）＋ factory 240/motion 43/overlay 30 が非空で実体化した確認 ＋ depth_path をどこにも生成していない確認
7. §3.3 の検算 [1]〜[8] を自分で再計算した結果（avg-uses/source 1.157≤1.4 を含む）
8. asset_manifest.v001.json の counts ブロック（still_body 215 / still_i2v_source 43 / motion 43 / factory 240 / overlay 30 / thumb_face 3）
9. 制約・1枚前提の自己申告（Morton の有罪化なし・被害者/遺体 graphic なし・Eric 識別可能子供顔なし・Norwood 美化なし・
   hedged 数値の可読断定なし・実在の顔/likeness ゼロを目視確認・dochighlight 文字列ゼロ・捏造/可読引用なし・
   milky wash/scanline なし・depth なし・バリエーション0・A↔B同一スキーマ
   [schema morton_assets.v1 / role enum body|i2v_source|thumb_face|reject / counts / also_thumb 集合 4 / overlay 30 / thumb_face 3]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**

---

## 5.13 ★EMOTIVE FACES — VISIBLE faces (ADDED per owner 2026-07-25)

生成済みセットは顔をそむける/影/手のみで「顔がほぼ無い」状態。オーナー方針＝**見える感情的な顔**を織り込む（顔は維持率・CTRを上げる）。このF-series（見える顔）を既存の匿名図に**加えて**生成する。

**2レーン、いずれも「実在の誰にも似せない・非実在の人物」：**
- **(a) generic-photoreal** — 特定の実在人物に紐づかない役（陪審員・町の人・大人の弔問客・記者・看守・一般の科学者/弁護士）。ここでの見える感情顔は誰も特定しない→実写OK。
- **(b) dramatized-illustrative** — 中心的実在人物に隣接するビート（苦悩する everyman）は、**明らかにイラスト調・半絵画的で写真に見えない**スタイルで（実在人物の写真に絶対見えないように）。実在人物として名指し/キャプションしない。

**HARD BANS（不変）：** Morton・Christine・Norwood・Anderson・Bradley・Raley・Morrison・実在の判事/陪審員の**肖像を作らない**；**3歳のEricの識別可能な顔は不可（子ども描写なし）**；被害者（Christine/Debra）の描写・暴力・遺体なし；可読テキストなし。QCフラグ：`has_human_body:true`・`has_identifiable_real_person:false`・`has_identifiable_face:false`・`has_victim_or_violence:false`・`has_readable_text:false`。

**★ FACE (data-driven, per owner choice A · 2026-07-25 thumbnail research):** every F-image shows a CLEARLY-VISIBLE, instantly-readable emotive face — prominent by **LIGHT + EXPRESSION, not by raw size** (in-lane data: a huge face-filling head correlates with FLOPS/clickbait; a composed face in a dark cinematic scene correlates with winners). Face a strong **medium-close-up at ~30–45% of frame height, eyes on the upper third, front or slight three-quarter view looking near camera**, one strong unmistakable emotion, dramatic key + rim light on the face against a **DARK, moody, restrained-saturation** background. NOT a 60%+ face-filling head, NOT turned away, NOT lost in shadow, NOT hands-only. (Bans hold: no real-person likeness of Morton/Norwood/Anderson/etc., no identifiable child face for Eric, no victim/violence.)

`[FSTYLE]` = `a clearly-visible emotive human face in a strong medium-close-up filling ~30-45 percent of the frame, eyes on the upper third, front or slight three-quarter view looking near camera, one strong unmistakable {EXPRESSION}, dramatic key light plus rim light on the face against a dark moody background, restrained saturation, a generic anonymized non-real person resembling no real individual, cinematic documentary grade, cold evidence-blue with a single warm homecoming note, ultra-detailed skin and eyes, high contrast, {photoreal | clearly illustrative semi-painterly non-photographic}, 16:9, adults only, no text, no watermark, no logo`
`[FNEG]` = `likeness of a real or named person, Michael Morton, Christine, Norwood, Anderson, recognizable real person, mugshot, deepfake, child, toddler, Eric, victim, beaten body, corpse, blood, injury, weapon, readable text, document, caption`

Files `F001.png … F012.png`. Act-mapped beats:
- **F001** (b · ACT1) grieving illustrative everyman husband's face, hollow shock — the morning everything broke. NOT a Morton likeness.
- **F002** (a · ACT1-2) detectives' hard, decided faces — "the husband did it."
- **F003** (a · ACT2) a prosecutor's stern face at a podium — generic, not Anderson.
- **F004** (a · ACT2) jurors' faces, uncertain — a conviction on a thin case.
- **F005** (b · ACT3) an illustrative face behind prison glass, years etched in — 25 years. NOT a likeness.
- **F006** (a · ACT3) a pro-bono lawyer's determined, tired face over a case file — generic, not Raley.
- **F007** (b · ACT4) an illustrative face at the gate in warm homecoming light, disbelief + relief — freedom. NOT a likeness.
- **F008** (a · ACT4) reporters/news faces, cameras — the story turning.
- **F009** (a · ACT4) the real killer as a distant, cold, generic face in shadow — NOT a Norwood likeness, no glorification.
- **F010** (a · ACT4) a courtroom gallery of emotive adult faces — the reckoning.
- **F011** (a · ACT2) an appellate/defense figure's resolute face — generic.
- **F012** (a · ACT4) a legislator's grave face (the Michael Morton Act) — generic.

Generate all 12; QC each visually (visible emotive face · non-real · no likeness/child/victim/text) before manifest.

