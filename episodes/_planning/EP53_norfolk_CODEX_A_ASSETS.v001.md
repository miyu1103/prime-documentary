# EP53 norfolk — Codex スレッドA「素材生成」引き継ぎプロンプト v001（30分・4幕・payoff 末尾積み上げ）

> ## ★★ 2026-07-26 更新 — 既に生成を始めている場合は必ず読む ★★
> 本書 §5.6 のプロンプトのうち **下記39枚は本日差し替え済み**（モチーフ反復排除・オーナー指示）。
> **旧プロンプトで生成済みでも、この39枚は `rejected/` へ退避してから新プロンプトで再生成すること**（「ファイルが有るからスキップ」禁止）。他のS番号は生成済みならそのまま有効。
> S002 S003 S004 S006 S007 S008 S017 S019 S020 S021 S045 S048 S050 S077 S078 S079 S082 S084 S086 S108 S109 S110 S111 S113 S115 S116 S117 S118 S119 S127 S129 S130 S145 S171 S191 S193 S197 S198 S200
> （factory covers 変更2件は §4.4 反映済み: F014→null / F071→S080。新ルール §5.5a も必読。）

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN_ARCHITECTURE）も実装スレッドB（CODEX_B）も**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> ★30分尺。素材点数は EP52 morton とほぼ同スケール。**「だいたい」で決めず §3 の確定値と §3.3 の検算をそのまま使う。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP53 / Episode ID: PD-2026-053-norfolk / slug: norfolk
Composition id: Ep53Norfolk（B が Root.tsx に登録・A は staging まで）／1920x1080 / fps30 / 30:00
事件:       The Norfolk Four（1997 バージニア州ノーフォーク・Michelle Moore-Bosko 殺害事件の冤罪）
            1997-07-08、海軍の町 Norfolk で、18歳の海軍兵の妻 Michelle Moore-Bosko が自宅アパートで
            殺害されているのが見つかった（夫 Billy Bosko が艦から戻って発見）。現場の物証は「単独犯」を
            示していたのに、刑事 Robert Glenn Ford の取調べが、無関係の海軍水兵4人
            （Danial Williams / Joseph Dick / Derek Tice / Eric Wilson）から次々に虚偽自白を引き出した。
            Williams は約11時間の徹夜取調べ（死刑の威嚇・ポリグラフ「不合格」の虚偽通告）で自白→
            DNA 不一致→警察は釈放せず「次の男」を作る→Dick 自白→DNA 不一致→Wilson・Tice…と
            「ドミノ」が続き、物証ゼロのまま「7〜8人の集団犯行」説まで膨張（追加起訴の3人は後に取り下げ）。
            1999、同じ団地で女性を襲って服役中だった Omar Ballard が「自分が一人でやった」と手紙で自白。
            現場 DNA に一致したのは Ballard ただ一人。Ballard は 2000 に有罪答弁（単独犯行と供述）。
            それでも4人は釈放されず（Williams/Dick は死刑威嚇下の有罪答弁で終身、Tice は2度の裁判で終身、
            Wilson はレイプのみ有罪で約8年半）。約30人の元FBI捜査官らが赦免を求めて運動し、
            2009 Kaine 知事の条件付き恩赦で3人が出所（前科は残置）。2010 PBS Frontline "The Confessions"。
            Ford 刑事は（別件の）恐喝と連邦捜査官への虚偽供述で有罪→連邦刑務所 12年6か月。
            2016 連邦地裁 Gibney 判事が Williams/Dick の有罪を破棄、2011 に Tice も破棄済み。
            2017 McAuliffe 知事が4人全員に absolute pardon（完全赦免）。2018 州+市の和解 計約$8.4M。
            ★主題は【自白の連鎖という悪夢・DNA が外れるたび「無罪」ではなく「新しい容疑者」が生まれた・
              そして末尾に積み上がる真実の連鎖（破棄→完全赦免→$8.4M→刑事本人が連邦刑務所へ）】。
            ★4人（Williams/Dick/Tice/Wilson）は【存命・有罪破棄＋完全赦免済み】＝無実は事実として断定してよい。
            ★★被害者 Michelle Moore-Bosko は【実在の殺害被害者】＝レイプ・殺害・現場・遺体の描写/再現を
              一切作らない（dignity・アパートは absence のみ）。被害者の両親は長年4人を有罪と信じた＝
              家族を悪役化しない（尊厳をもって扱う）。実在人物（4人の水兵/Ford/Ballard/Michelle/Billy/
              家族/検察官/判事）の顔・肖像・likeness を一切作らない。匿名・非識別の一般人は可。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ・30分スケール）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**205本の固有プロンプト×1枚＝205枚**・バリエーション0） | `H:\pd-media\assets\ai\norfolk\S<NNN>.png` | 5–8時間（GPU） |
| A-1b | i2v 種画像の生成（**42本の固有プロンプト×1枚＝42枚**・バリエーション0） | `H:\pd-media\assets\ai\norfolk\M<NN>_src.png` | 1.5–2.5時間（GPU） |
| A-1c | サムネ用 emotive-face 静止画（**3枚**・CTR・非実在の illustrative face・§5.12） | `H:\pd-media\assets\ai\norfolk\T<NN>_face.png` | 20分（GPU） |
| A-2 | 静止画のQCと目視（**全250枚を目視必須**＝205 body + 42 i2v種 + 3 thumb_face） | `05_visuals/still_qc.v001.json` + コンタクトシート | 2.5–4時間 |
| A-3 | ~~depth map~~ **不要（本作は depth treatment を使わない・§6.4）** | — | — |
| A-4 | factory 実写クリップ **232本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | 4–6時間（うち目視だけで2時間以上） |
| A-5 | i2v モーション化 **42本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\norfolk\M<NN>_rife.mp4` | 18–48時間（GPU・**複数日**） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **30本** | `05_stock/overlay_selection.v001.json` | 1時間 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 30分 |
| A-8 | Remotion public への staging | `remotion/public/norfolk/{img,factory,motion,overlay,thumb}/` | 40分 |

> **★★ 最重要の前提（EP42–52 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 205本＝205行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **variants 指定なし（＝1枚）** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 205 + i2v 種 42 + thumb_face 3 = 250枚（各1回）。** factory 232本は生成でなく在庫からの選抜。
> ★**`--only S001` のログで `shots=250` を確認**してから本番を回す（205 body + 42 i2v種 + 3 thumb_face = 250）。
> ★i2v 42本は**複数日GPU**。**開始前にマシン状態を確認**（heavy-job preflight）。夜間・分割で回す。
>
> **★★ 反復の規律（owner directive 2026-07-26「似たシーンの機械的な繰り返し禁止」・1シーン1枚と同格の拘束）★★**
> 1. **同一ストーリービート内の同一モチーフは最大2バリエーション。** 同じ被写体の3構図以上を同じビートに並べない（例: 取調室の椅子・タリー壁・手紙の接写を1ビートに3枚以上置かない）。
> 2. **幕をまたぐ spine-motif の再登場は必ず「見える状態変化」を伴う**（タリー: 1本目→2本目→4本→拭われる→1本だけ残る／手紙: 白紙→書かれる→畳まれる→署の棚に届く→脇へ押される→擦り切れて保管／電球: 点灯→受刑の合間に待機→消灯→昼光の中で死んでいる／gel: 現像中→空レーン→唯一の一致→cream 点火）。**状態変化のない再登場は禁止。意味のある反復のみ可**（channel canon）。各再登場行のプロンプトに状態変化の語句を明記する。
> 3. **Codex one-shot 原則:** Codex は各プロンプトを1発で当てる前提（SDXL 的な「量産して選ぶ」思考をしない）。再生成は QC 不合格時のみ（§6.3）。**「選ぶための near-variant」を作らない。**

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-053-norfolk/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を **A(producer)とB(consumer/validator)で一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 232 エントリ、`motion` 配列は 42 エントリ、`overlay` 配列は 30 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5／§4.6 に全 232 + 42 + 30 を列挙済み。build スクリプトはこの列挙を消費するだけで、空配列を書かない）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\norfolk\**` / `H:\pd-media\assets\ai_video\norfolk\**` | **A** | 読み書き |
| `episodes/PD-2026-053-norfolk/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-053-norfolk/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/norfolk/{img,factory,motion,overlay,thumb}/**` | **A** | 読み書き |
| `episodes/PD-2026-053-norfolk/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_norfolk_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-052-*/**` および EP39〜52 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を読む） | `PD-2026-053-norfolk`（variants 指定なし） / `53 --only S001` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-053-norfolk --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit N --exclude-used --ep PD-2026-053-norfolk --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-053-norfolk` |

> **★`gen_depth_maps.py` は使わない**（本作は depth treatment を使わない＝depth map 不要・§6.4／DESIGN §1「footage treatment は bleed/parallax、depth 禁止」）。

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（実在確認してから・直近の `*morton*`(EP52) を優先、無ければ `*centralpark*`(EP50)） |
|---|---|---|
| `scripts/qc_norfolk_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_morton_stills.py`（無ければ `qc_centralpark_stills.py`） |
| `scripts/select_norfolk_factory.py` | §7 の factory 232本の確定選定・EP39〜52 sha256 除外検証 | `scripts/select_morton_factory.py`（無ければ `select_centralpark_factory.py`） |
| `scripts/comfy_wan_norfolk.py` | §8 の i2v 42本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_morton.py`（無ければ `comfy_wan_centralpark.py`） |
| `scripts/rife_norfolk.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_morton.py`（無ければ `rife_centralpark.py`） |
| `scripts/build_norfolk_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_morton_asset_manifest.py` |
| `scripts/stage_norfolk_assets.py` | §10 の staging | `scripts/stage_morton_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.9 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_norfolk_facts.py`（B が clone して実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の制約に一致し、`check_norfolk_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_norfolk_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==232 / motion 配列長==42 / overlay 配列長==30 が非空で実体化していること（EP45 事故回避の必須不変条件）

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_norfolk_asset_manifest.py --reuse-feasibility
#   → still >=205 / motion >=42 / factory >=232 / distinct 合計 >=479 / first-use >=0.70 / avg-uses/source <=1.4

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_norfolk_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全232本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-053-norfolk

# [A-DONE-5] EP39〜EP52 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_norfolk_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39〜EP52 の十四話すべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（正確性制約・ガードレール）★★★

**Norfolk Four の4人（Danial Williams / Joseph Dick / Derek Tice / Eric Wilson）は【存命・有罪破棄（2011/2016 連邦裁）＋2017 absolute pardon（完全赦免）済み】＝4人の無実を事実として断定してよい。二人の実在の villain も record の範囲で断定してよい:（1）Omar Ballard＝現場 DNA に一致した唯一の人物・2000 に有罪答弁し「単独犯行」と供述した真犯人（美化しない・lurid にしない）、（2）Robert Glenn Ford＝虚偽自白を主導した刑事で、のちに（別件の）恐喝と連邦捜査官への虚偽供述で連邦有罪・12年6か月収監（内心の embellish をしない・連邦有罪と裁判所の認定の範囲のみ）。被害者 Michelle Moore-Bosko は【実在の殺害被害者・18歳】＝レイプ・暴行・殺害・現場・遺体を一切描かない（dignity・アパートは absence のみ）。被害者の両親は長年4人を有罪と信じた＝家族を悪役化しない。全ての実在人物（Williams/Dick/Tice/Wilson/Ford/Ballard/Michelle/Billy Bosko/両親/Tamika Taylor/検察官/Gibney 判事/Kaine/McAuliffe 両知事）の顔・肖像・likeness を作らない。匿名・非識別の一般人は可。数値（約11時間・7〜8人説・約30人の元FBI・12年6か月・約$8.4M・各人の服役年数）は hedged。捏造引用禁止・可読の偽公文書禁止（自白調書・Ballard の手紙・判決文・新聞の可読文字を作らない）。**

## 1.1 R1/R2（生成ビジュアル全般）

1. **★R-FACE: 匿名・非識別の人物は可／実在人物の likeness は不可。** 匿名の一般人（実在の誰にも似せない・非識別のドラマ化スタンドイン）＝顔・身体を出してよい（§5.11 の H シリーズ・専用 `[HSTYLE]`/`[HNEG]`・§5.12 の thumb_face・§5.13 の F シリーズ）。ただし **実在人物の顔・likeness・肖像は作らない**＝Danial Williams・Joseph Dick・Derek Tice・Eric Wilson・Robert Glenn Ford・Omar Ballard・Michelle Moore-Bosko・Billy Bosko・被害者の両親・Tamika Taylor・実在の検察官/判事/知事を**似せて描かない**。実在人物が示唆される所（水兵・刑事・受刑者等）は非識別（背向き/影/逆光/目から下でクロップ/ソフト/hands-only）を既定に保つ。**被害者（Michelle）の描写・レイプ/暴行/殺害/遺体の imagery を一切作らない（不変）。**
2. **可読の偽公文書を再現しない。** 本件は「自白調書」と「手紙」の物語＝**自白書面・Ballard の手紙・ポリグラフ結果・DNA レポート・判決文・新聞・赦免状の可読文字を一切再現しない**（雰囲気のみ・"blurred into an unreadable smear"）。日付（1997/1999/2009/2016/2017 等）・年齢（18）・金額（$8.4M）・服役年数・タリー以外の数字を**画像に描かない**（AE/figures のタイポで出す＝B の担当）。
3. **被害者・レイプ・暴行・殺害・現場・遺体・凶器を一切描かない。** アパートは **empty rooms of absence（cold・無人・遺体なし・血なし・凶器なし・ナイフなし）** のみ。玄関・廊下・外観・置き去りの日常の静物で「不在」を語る。**襲撃の再現を誰の視点でも作らない。**
4. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **R-FOUR-INNOCENT:** 4人が犯人であるかのような絵・語を作らない。彼らは **wrongfully convicted・exonerated・innocent・fully pardoned**。"the sailors did it / guilty four / Williams killed / Dick raped"（断定として）を書かない（"the police theory / the state claimed" の帰属枠は可）。
2. **R-VICTIM:** Michelle Moore-Bosko に dignity。姿・likeness・遺体・暴行・レイプ・血・凶器・ナイフを描かない。"rape scene / stabbing / stabbed body / murder scene / blood / knife" を書かない。empty apartment of absence のみ。
3. **R-FAMILY:** 被害者の両親・夫 Billy を悪役化しない・likeness を作らない。"the family was wrong / foolish parents" 等を書かない（両親が4人を有罪と信じたことは narration=B の領分であり、絵では家族を特定しない）。
4. **R-VILLAIN-FACT:** Ford と Ballard は record 上の事実のみ。Ford＝虚偽自白の取調べを主導・のちに別件の恐喝と虚偽供述で連邦有罪・12年6か月（"corrupt monster" 等の内心断定を書かない・record の言葉のみ）。Ballard＝唯一の DNA 一致・有罪答弁・単独犯行と供述（美化しない・lurid にしない）。**likeness は作らない**（非識別 silhouette）。
5. **R-NUM:** hedged 数値を断定で焼かない。約11時間（"roughly eleven hours"）・7〜8人説（"seven or eight"）・約30人の元FBI（"some thirty"）・12年6か月（"twelve and a half years"）・約$8.4M（"roughly"）・各人の服役年数（"about/nearly"）を**画像に可読で描かない**（AE/figures＝B）。断定表現を書かない。
6. **R-FACE:** **匿名・非識別の人物は可**（§5.11/§5.12/§5.13）。**実在人物の likeness ゼロ**＝"likeness of <Williams/Dick/Tice/Wilson/Ford/Ballard/Michelle/Bosko> / face of <those names> / recognizable real person / mugshot of a real person / deepfake" を書かない。**匿名一般人（"anonymous / generic / non-identifiable person, face turned or in shadow"）は許可。**
7. **R-READABLE:** 可読の偽公文書（自白調書/手紙/ポリグラフ/DNAレポート/判決文/新聞/赦免状/日付/案件番号）を描かない。"legible confession / readable letter / readable court document" を正プロンプトに書かない（雰囲気は "unreadable smear"）。
8. **R-DOCHL:** **dochighlight（黒バー/box/underline の figure）を作らない・言及しない。** `tags`/`caption_hint`/`notes`/ファイル名に `dochighlight` の文字列を書かない（grep で 0 を保つ）。
9. **R-QUOTE:** 捏造引用禁止。verbatim は FACTS_LEDGER の VERIFIED-VERBATIM 2件（Ballard の手紙の一節／Gibney 判事 2016 意見の一節・いずれも attribution 付き・AE＝B の担当）のみ。画像に可読の引用を描かない。

## 1.3 機械ゲート（`build_norfolk_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
# 匿名・非識別の人物は許可。実在人物の likeness だけを弾く。
BANNED_PORTRAIT = re.compile(
    r"likeness of (a )?(real|specific|named) person|real[- ]person likeness|"
    r"face of (danial|williams|joseph|joe|dick|derek|tice|eric|wilson|robert|glenn|ford|omar|ballard|michelle|moore|bosko|billy|tamika|taylor|gibney|kaine|mcauliffe)|"
    r"likeness of (danial|williams|joseph|joe|dick|derek|tice|eric|wilson|robert|glenn|ford|omar|ballard|michelle|moore|bosko|billy|tamika|taylor|gibney|kaine|mcauliffe)|"
    r"recognizable (real person|celebrity)|identifiable real person|"
    r"mugshot of (a )?real person|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"(williams|dick|tice|wilson) (killed|did it|is guilty|raped|murdered|stabbed)|the sailors did it(?! \(the (state|police|prosecution|theory))|"
    r"guilty (four|sailors)|"
    r"(rape|assault|stabbing) (scene|re-?enactment|depicted)|raped woman|stabbed (body|woman|victim)|murder scene|dead body|corpse|the knife|blood on|"
    r"(glorified|heroic|admirable) ballard|lurid|"
    r"(?<!il)legible (confession|letter|document|case file|report|newspaper|lab report|pardon)|(?<!un)readable (confession|letter|document|case file|report)|"
    r"dochighlight",
    re.IGNORECASE)
```

> **許容:** "wrongfully convicted / false confession / coerced confession / exonerated / innocent / fully pardoned / the only DNA match / Ballard confessed he acted alone / the detective was later convicted in federal court / anonymous, non-identifiable person, face turned or in shadow / empty apartment of absence / chalk tally marks / an unreadable letter on cream paper"。禁止は「4人の有罪化」「被害者/レイプ/暴行/遺体の描写」「家族の悪役化」「Ballard 美化/lurid」「Ford の record 外の断定」「hedged 数値の断定」「可読の偽公文書（自白調書・手紙・判決文）」「実在人物 likeness」「dochighlight」。

---

# 2. 台本の語数と尺の確定値（Aが素材点数を積算する根拠）

```
words_total          = 4,645（LOCKED script・fact-locked・check_script_length --lo 1740 --hi 1860 = PASS）
narration_seconds    = 1564.9（= 26.08分 @ 178.1 wpm・provisional・FINAL は measured TTS forced-align で上書き）
wpm_used             = 178.1（channel measured median）
gap_ratio_design     = 1.150（息継ぎ/designed breath/OP/ED を含む finished/narration 比・実測帯 1.04–1.30 の内側）
★HOOK-AUDIO 標準（owner・CODEX_B §5.1.2）: Brian の声が 0:00 から鳴る（silent runway なし）。
  narration（COLD OPEN 行から）を 0:00 に置き、hook/opening 秒は加算しない。
total_seconds        = 1799.6（narration 1564.9 × 1.150 ≈ 1799.6・endcard 9.0 を内包）= 30:00（band 29:00–31:00 内）
durationInFrames     = 53,988（provisional・fps30 = round(1799.6×30)・VO onset 0.0）
mean_shot            = 1790.6 / 536 = 3.341秒/カット（film body = total 1799.6 − endcard 9）
視覚 acts             = 4（+ HOOK/OPENING/ENDING は別区）
Act 語数配分（★2026-07-28 実測に更新）:
  HOOK 110 / OP 163 / ACT1 950 / ACT2 1,038 / ACT3 968 / ACT4 1,233 / ENDING 300 = 4,762
  （旧 provisional 950/1050/950/1100+300+300 = 4,650 とは 2.4% 以内で一致。★実測の最密は ACT4（1,233語））
★TTS 実測（2026-07-28）: master 1,673.888s・speech 1,573.99s・304 chunks・181.5 wpm。
  provisional 1,564.9s に対し +9.1s のみ。×1.150 の設計 gap が吸収し、
  total_seconds 1799.6 / durationInFrames 53,988 / mean_shot 3.341 は全て不変（再ロック不要）。
```

**Aにとっての意味は1つ:** > **総カット 536 / distinct 479 / 初出 89.37% = still 205 + factory 232 + motion 42。**（§3 で積算）

> **注意（命名差）:** 視覚 act は **0=HOOK/OPENING, 1=ACT I, 2=ACT II, 3=ACT III, 4=ACT IV, 5=ENDING**（6値）。**still は 205 本の固有プロンプトを持つ**ため、still の資産 ID は **S001..S205**（1プロンプト＝1枚）。`covers_scene_id` は still 資産 ID 空間（S001..S205）を指す（§7.3）。

---

# 3. ★素材構成の確定値（この値で調達する・勝手に変えない）

## 3.1 内訳（★勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **205枚** | 220カット | 1.073回(≤2) | **205本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **232本** | 232カット | **各1回(1)** | 在庫11,000本超＋stock から選抜（§7）・全点目視・EP39〜52 と sha256 被りゼロ |
| **i2v モーション** | **42本** | 84カット | 各2回(≤2) | 42本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **479点** | **536カット** | | |
| 合成レイヤー（particle/light/vfx） | 30本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |
| サムネ emotive-face（thumb_face） | 3枚 | — | 本編カットに出ない | **distinct/cuts に数えない**（§5.12・thumbnail 専用） |

**SDXL の生成バッチ（本編カットに出ない i2v 種・thumb_face を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **205枚** | 205プロンプト × 1枚 |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **42枚** | 42種プロンプト × 1枚 |
| サムネ face（`role:"thumb_face"`・§5.12） | **3枚** | 3プロンプト × 1枚 |
| **SDXL 生成バッチ合計** | **205 + 42 + 3 = 250枚（各1回）** | **variants 指定なし（＝1枚）** |

> **本編サムネの背景 anchor は body 205枚から4枚を `also_thumb:true` で流用選抜**（§4.3a）。**emotive-face（前景の顔）は §5.12 の thumb_face 3枚**（B が `NorfolkThumbnails.tsx` で face＋hook text を合成）。**role=thumb / still_thumb を作らない。**

## 3.2 幕別配分（★still は確定・factory/i2v は目安。合計だけが確定）

| 区間(act) | still（S番号・確定） | factory（目安） | i2v（確定合計42） | thumb anchor |
|---|---|---|---|---|
| HOOK+OPENING (0) | **15**（S001–S015） | 12 | 3（M01–M03） | S001 |
| ACT1「The First Confession」(1) | **45**（S016–S060） | 44 | 8（M04–M11） | S060 |
| ACT2「The Domino」(2)（engine・最密） | **45**（S061–S105） | 40 | 9（M12–M20） | — |
| ACT3「The Letter」(3) | **40**（S106–S145） | 48 | 8（M21–M28） | S121 |
| ACT4「The Long Undoing」(4)（climax・最密②） | **45**（S146–S190） | 44 | 10（M29–M38） | S170 |
| ENDING (5) | **15**（S191–S205） | 14 | 4（M39–M42） | — |
| 繋ぎ（covers_scene_id:null） | — | 30 | — | — |
| **合計** | **205** | **232** | **42** | **4** |

> **still の per-act 数（15/45/45/40/45/15＝205）は確定**（§5 の motif ライブラリがこの配分で組まれている）。ACT2（ドミノの engine）と ACT4（undoing の cascade）が最厚45＋motion 最多。**幕別の factory/i2v 内訳は目安値**（合計 232 / 42 のみ確定）。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 536 = still 220 + factory 232 + i2v 84
[2] 平均ショット長 = film body 1790.6 / 536 = 3.341秒/カット  ✓ (≤7.0)
[3] 静止画占有率(check_animation_mix) = 220/536 = 41.04%  ✓ ≤45%（余裕 3.96%pt）
[4] motion coverage = (232+84)/536 = 316/536 = 58.96%     ✓ ≥45%
[5] per-asset 上限: still 220/205=1.073(≤2) / factory 232/232=1.0(≤1) / motion 84/42=2.0(≤2)  ✓
[6] first-use share = 479/536 = 0.8937                    ✓ ≥0.70
[7] avg uses/source = 536/479 = 1.119                     ✓ ≤1.4（EP49 は 1.8 で flag された）
[8] factory 下限 = 1790.6/30 = 59.7 → ≥60本。設計値 232本 ✓（still-share≤0.45 を守る）
```

> **[3] の余裕は 3.96%pt。** still が205本を割ったら §6.3 の再生成で回復させ、**still-cut 220 を増やさない**（B側の shotlist が220で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-053-norfolk/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `norfolk_assets.v1`（固定文字列）
**生産者:** `scripts/build_norfolk_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を一字一致。** role enum は **`body | i2v_source | thumb_face | reject` のみ**。also_thumb は body still **ちょうど4枚**。thumb_face は **ちょうど3枚**。overlay は **ちょうど30本**。

## 4.1 スキーマ（`norfolk_assets.v1`）

```jsonc
{
  "schema_version": "norfolk_assets.v1",
  "episode_id": "PD-2026-053-norfolk",
  "slug": "norfolk",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_norfolk_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 205,        // ==205
    "still_i2v_source": 42,   // ==42
    "motion": 42,             // ==42
    "factory": 232,           // ==232
    "overlay": 30,            // ==30（distinct 素材に数えない）
    "thumb_face": 3           // ==3（thumbnail 専用・distinct/cuts に数えない）
  },
  "stills":  [ /* §4.3: body 205 (NOR-S001..S205) + i2v_source 42 (NOR-MS01..MS42) + thumb_face 3 (NOR-T01..T03) */ ],
  "motion":  [ /* §4.5: NOR-M01..M42 全42本・public_path 必須（★非空） */ ],
  "factory": [ /* §4.4: 232本・public_path 必須（★非空・EP45事故回避の核心） */ ],
  "overlay": [ /* §4.6: 30本 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例・★depth_path なし）

```jsonc
{
  "asset_id": "NOR-S001",                 // body: ^NOR-S\d{3}$（001..205）/ i2v種: ^NOR-MS\d{2}$ / thumb: ^NOR-T\d{2}$
  "scene_id": "S001",                     // still 資産 ID 空間（§5.9 のプロンプト行に対応・S001..S205）
  "role": "body",                         // body|i2v_source|thumb_face|reject
  "also_thumb": false,                    // body から4枚だけ true（§4.3a・追加生成しない）
  "act": 0,                               // 0=HOOK/OPENING, 1..4=ACT I..IV, 5=ENDING
  "path": "H:/pd-media/assets/ai/norfolk/S001.png",
  "public_path": "norfolk/img/S001.png",  // role=="body" のみ非null / i2v種・thumb_face は null
  "width": 3840, "height": 2160,          // 長辺>=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 21.0,
  "tags": ["tally_marks","interrogation_bulb","harbor_slate","symbolic","no_face","no_readable_text"],
  "caption_hint": "five chalk tally marks on a dark interrogation-room wall under one bare bulb, four of them struck through, symbolic, no people, no readable text",
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

1. `schema_version=="norfolk_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 205 / i2v_source 42 / motion 42 / factory 232 / overlay 30 / thumb_face 3）に**一致**
3. 全 `path`/`public_path` がディスクに実在（**depth_path は要求しない**）
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `public_path` が非null かつ実在（**depth_path は不要**）。`role=="i2v_source"`/`role=="thumb_face"` は `public_path==null`
7. **★reject 条件:** `qc.has_readable_text==true` **または** `qc.has_identifiable_real_person==true` **または** `qc.has_victim_or_violence==true` は `role=="reject"`。**`qc.has_human_body==true` は reject 条件ではない**（匿名人体は可）。`qc.has_identifiable_face` は「実在人物として識別可能な顔」を意味する（匿名・非識別の顔は可）。H シリーズ（§5.11）・thumb_face（§5.12）・F シリーズ（§5.13）は `has_human_body:true`/`has_identifiable_real_person:false`/`has_readable_text:false`/`has_victim_or_violence:false`
8. `role=="i2v_source"` は `role=="body"`/`role=="thumb_face"` と**同一 asset_id を共有しない**（i2v_source は `^NOR-MS\d{2}$` / thumb_face は `^NOR-T\d{2}$`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39〜EP52（十四話）の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど4**、かつ `scene_id` 集合が §4.3a の4枚集合と完全一致（**CODEX_B と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|thumb_face|reject のみ）
16. `overlay` 配列長が**ちょうど30**
17. ★**`factory` 配列長==232 かつ全エントリ `public_path` が非空**（EP45 事故回避）
18. ★**`motion` 配列長==42 かつ全エントリ `public_path` が非空**（同上）
19. **★どの still/motion にも `depth_path` キーを要求しない・生成しない**（depth treatment 不使用・§6.4）

`--reuse-feasibility` では §3.3 [5][6][7][8] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 205枚（S001..S205）= §5.6 の205プロンプトの生成物。各1枚。
2. i2v_source 42枚（MS01..MS42 / 種画像 M01_src..M42_src）= §8.1a の42種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. thumb_face 3枚（T01..T03 / T01_face..T03_face）= §5.12 の3プロンプトの生成物。public_path==null。
4. also_thumb : body のうち §4.3a の4枚に true（追加生成しない）
5. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

### 4.3a ★also_thumb 集合（ちょうど4枚・CODEX_B と一字一致必須）

```
{ NOR-S001 (five chalk tally marks, four struck through, under one bare bulb — the hook signature),
  NOR-S060 (the interrogation room wide: one bare bulb, steel table, one empty chair — confession #1),
  NOR-S121 (the letter alone in a shaft of cream light on a dark desk — the ignored truth),
  NOR-S170 (the DNA gel ladder igniting: one lane matches, four lanes clear — the Act IV hinge) }
```

> ★この4集合は §5.6 の該当 S番号に必ず該当 motif を置くこと（§5.6 の motif ライブラリで anchor 指定済み）。**前景の emotive face は §5.12 の thumb_face（T01–T03）＝これらは背景 anchor。**

## 4.4 ★`factory[]` 全232エントリ（★必ず実体化・public_path 非空。EP45事故回避の核心）

> `select_norfolk_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id）/`path`（`H:/pd-media/assets/factory/...` or `H:/pd-media/assets/stock/...`）/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`origin`(`factory`|`stock`)/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。** 各 public_path は `norfolk/factory/F0NN_<subtype>.mp4`。`type:"backgrounds"`, `kind:"video"`。**subtype の `_02`/`_03` は「同一検索テーマの別クリップ」の意で、別 sha256・別素材（同一ファイルの重複ではない）。**

```jsonc
// HOOK+OPENING (act 0) — 12
{ "public_path":"norfolk/factory/F001_dark_interrogation_room_dim.mp4", "act":0, "covers_scene_id":"S005", "subtype":"dark_interrogation_room_dim" }
{ "public_path":"norfolk/factory/F002_institutional_corridor_night.mp4", "act":0, "covers_scene_id":null, "subtype":"institutional_corridor_night" }
{ "public_path":"norfolk/factory/F003_harbor_night_lights.mp4", "act":0, "covers_scene_id":"S009", "subtype":"harbor_night_lights" }
{ "public_path":"norfolk/factory/F004_warship_silhouette_dawn.mp4", "act":0, "covers_scene_id":"S010", "subtype":"warship_silhouette_dawn" }
{ "public_path":"norfolk/factory/F005_records_archive_shelves.mp4", "act":0, "covers_scene_id":null, "subtype":"records_archive_shelves" }
{ "public_path":"norfolk/factory/F006_evidence_room_dim.mp4", "act":0, "covers_scene_id":null, "subtype":"evidence_room_dim" }
{ "public_path":"norfolk/factory/F007_chalkboard_dark_texture.mp4", "act":0, "covers_scene_id":null, "subtype":"chalkboard_dark_texture" }
{ "public_path":"norfolk/factory/F008_file_cabinet_room_dim.mp4", "act":0, "covers_scene_id":null, "subtype":"file_cabinet_room_dim" }
{ "public_path":"norfolk/factory/F009_police_station_exterior_night.mp4", "act":0, "covers_scene_id":null, "subtype":"police_station_exterior_night" }
{ "public_path":"norfolk/factory/F010_gray_sea_dawn_wide.mp4", "act":0, "covers_scene_id":null, "subtype":"gray_sea_dawn_wide" }
{ "public_path":"norfolk/factory/F011_dark_interrogation_room_dim_02.mp4", "act":0, "covers_scene_id":null, "subtype":"dark_interrogation_room_dim_02" }
{ "public_path":"norfolk/factory/F012_harbor_night_lights_02.mp4", "act":0, "covers_scene_id":null, "subtype":"harbor_night_lights_02" }
// ACT1 The First Confession (act 1) — 44
{ "public_path":"norfolk/factory/F013_norfolk_naval_harbor_day.mp4", "act":1, "covers_scene_id":"S016", "subtype":"norfolk_naval_harbor_day" }
{ "public_path":"norfolk/factory/F014_gray_warship_hull_closeup.mp4", "act":1, "covers_scene_id":null, "subtype":"gray_warship_hull_closeup" }
{ "public_path":"norfolk/factory/F015_dockyard_cranes_dawn.mp4", "act":1, "covers_scene_id":"S018", "subtype":"dockyard_cranes_dawn" }
{ "public_path":"norfolk/factory/F016_navy_pier_morning.mp4", "act":1, "covers_scene_id":null, "subtype":"navy_pier_morning" }
{ "public_path":"norfolk/factory/F017_brick_apartment_complex_90s.mp4", "act":1, "covers_scene_id":"S022", "subtype":"brick_apartment_complex_90s" }
{ "public_path":"norfolk/factory/F018_apartment_corridor_dim.mp4", "act":1, "covers_scene_id":"S024", "subtype":"apartment_corridor_dim" }
{ "public_path":"norfolk/factory/F019_apartment_stairwell_shadow.mp4", "act":1, "covers_scene_id":null, "subtype":"apartment_stairwell_shadow" }
{ "public_path":"norfolk/factory/F020_apartment_parking_lot_dusk.mp4", "act":1, "covers_scene_id":null, "subtype":"apartment_parking_lot_dusk" }
{ "public_path":"norfolk/factory/F021_apartment_door_closed_cold.mp4", "act":1, "covers_scene_id":"S028", "subtype":"apartment_door_closed_cold" }
{ "public_path":"norfolk/factory/F022_police_lights_night_apartment.mp4", "act":1, "covers_scene_id":"S036", "subtype":"police_lights_night_apartment" }
{ "public_path":"norfolk/factory/F023_patrol_car_street_night.mp4", "act":1, "covers_scene_id":null, "subtype":"patrol_car_street_night" }
{ "public_path":"norfolk/factory/F024_detective_office_dim.mp4", "act":1, "covers_scene_id":"S045", "subtype":"detective_office_dim" }
{ "public_path":"norfolk/factory/F025_interrogation_mirror_room_empty.mp4", "act":1, "covers_scene_id":"S046", "subtype":"interrogation_mirror_room_empty" }
{ "public_path":"norfolk/factory/F026_wall_clock_no_time_dim.mp4", "act":1, "covers_scene_id":"S047", "subtype":"wall_clock_no_time_dim" }
{ "public_path":"norfolk/factory/F027_rain_on_window_night.mp4", "act":1, "covers_scene_id":null, "subtype":"rain_on_window_night" }
{ "public_path":"norfolk/factory/F028_styrofoam_cup_table_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"styrofoam_cup_table_dim" }
{ "public_path":"norfolk/factory/F029_chesapeake_water_gray.mp4", "act":1, "covers_scene_id":null, "subtype":"chesapeake_water_gray" }
{ "public_path":"norfolk/factory/F030_navy_base_gate_day.mp4", "act":1, "covers_scene_id":null, "subtype":"navy_base_gate_day" }
{ "public_path":"norfolk/factory/F031_barracks_exterior_90s.mp4", "act":1, "covers_scene_id":null, "subtype":"barracks_exterior_90s" }
{ "public_path":"norfolk/factory/F032_seagulls_gray_sky.mp4", "act":1, "covers_scene_id":null, "subtype":"seagulls_gray_sky" }
{ "public_path":"norfolk/factory/F033_norfolk_naval_harbor_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"norfolk_naval_harbor_day_02" }
{ "public_path":"norfolk/factory/F034_gray_warship_hull_closeup_02.mp4", "act":1, "covers_scene_id":null, "subtype":"gray_warship_hull_closeup_02" }
{ "public_path":"norfolk/factory/F035_dockyard_cranes_dawn_02.mp4", "act":1, "covers_scene_id":null, "subtype":"dockyard_cranes_dawn_02" }
{ "public_path":"norfolk/factory/F036_brick_apartment_complex_90s_02.mp4", "act":1, "covers_scene_id":null, "subtype":"brick_apartment_complex_90s_02" }
{ "public_path":"norfolk/factory/F037_apartment_corridor_dim_02.mp4", "act":1, "covers_scene_id":null, "subtype":"apartment_corridor_dim_02" }
{ "public_path":"norfolk/factory/F038_apartment_door_closed_cold_02.mp4", "act":1, "covers_scene_id":null, "subtype":"apartment_door_closed_cold_02" }
{ "public_path":"norfolk/factory/F039_police_lights_night_apartment_02.mp4", "act":1, "covers_scene_id":null, "subtype":"police_lights_night_apartment_02" }
{ "public_path":"norfolk/factory/F040_patrol_car_street_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"patrol_car_street_night_02" }
{ "public_path":"norfolk/factory/F041_detective_office_dim_02.mp4", "act":1, "covers_scene_id":null, "subtype":"detective_office_dim_02" }
{ "public_path":"norfolk/factory/F042_interrogation_mirror_room_empty_02.mp4", "act":1, "covers_scene_id":null, "subtype":"interrogation_mirror_room_empty_02" }
{ "public_path":"norfolk/factory/F043_rain_on_window_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"rain_on_window_night_02" }
{ "public_path":"norfolk/factory/F044_chesapeake_water_gray_02.mp4", "act":1, "covers_scene_id":null, "subtype":"chesapeake_water_gray_02" }
{ "public_path":"norfolk/factory/F045_navy_base_gate_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"navy_base_gate_day_02" }
{ "public_path":"norfolk/factory/F046_barracks_exterior_90s_02.mp4", "act":1, "covers_scene_id":null, "subtype":"barracks_exterior_90s_02" }
{ "public_path":"norfolk/factory/F047_norfolk_naval_harbor_day_03.mp4", "act":1, "covers_scene_id":null, "subtype":"norfolk_naval_harbor_day_03" }
{ "public_path":"norfolk/factory/F048_apartment_corridor_dim_03.mp4", "act":1, "covers_scene_id":null, "subtype":"apartment_corridor_dim_03" }
{ "public_path":"norfolk/factory/F049_brick_apartment_complex_90s_03.mp4", "act":1, "covers_scene_id":null, "subtype":"brick_apartment_complex_90s_03" }
{ "public_path":"norfolk/factory/F050_police_lights_night_apartment_03.mp4", "act":1, "covers_scene_id":null, "subtype":"police_lights_night_apartment_03" }
{ "public_path":"norfolk/factory/F051_gray_warship_hull_closeup_03.mp4", "act":1, "covers_scene_id":null, "subtype":"gray_warship_hull_closeup_03" }
{ "public_path":"norfolk/factory/F052_dockyard_cranes_dawn_03.mp4", "act":1, "covers_scene_id":null, "subtype":"dockyard_cranes_dawn_03" }
{ "public_path":"norfolk/factory/F053_apartment_door_closed_cold_03.mp4", "act":1, "covers_scene_id":null, "subtype":"apartment_door_closed_cold_03" }
{ "public_path":"norfolk/factory/F054_detective_office_dim_03.mp4", "act":1, "covers_scene_id":null, "subtype":"detective_office_dim_03" }
{ "public_path":"norfolk/factory/F055_rain_on_window_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"rain_on_window_night_03" }
{ "public_path":"norfolk/factory/F056_chesapeake_water_gray_03.mp4", "act":1, "covers_scene_id":null, "subtype":"chesapeake_water_gray_03" }
// ACT2 The Domino (act 2) — 40
{ "public_path":"norfolk/factory/F057_dna_lab_interior_cold.mp4", "act":2, "covers_scene_id":"S061", "subtype":"dna_lab_interior_cold" }
{ "public_path":"norfolk/factory/F058_gel_electrophoresis_equipment.mp4", "act":2, "covers_scene_id":"S063", "subtype":"gel_electrophoresis_equipment" }
{ "public_path":"norfolk/factory/F059_lab_vials_rack_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"lab_vials_rack_cold" }
{ "public_path":"norfolk/factory/F060_lab_centrifuge_detail.mp4", "act":2, "covers_scene_id":null, "subtype":"lab_centrifuge_detail" }
{ "public_path":"norfolk/factory/F061_police_station_corridor_dim.mp4", "act":2, "covers_scene_id":"S071", "subtype":"police_station_corridor_dim" }
{ "public_path":"norfolk/factory/F062_lineup_room_empty.mp4", "act":2, "covers_scene_id":null, "subtype":"lineup_room_empty" }
{ "public_path":"norfolk/factory/F063_corkboard_string_wall_unreadable.mp4", "act":2, "covers_scene_id":"S087", "subtype":"corkboard_string_wall_unreadable" }
{ "public_path":"norfolk/factory/F064_norfolk_courthouse_brick_exterior.mp4", "act":2, "covers_scene_id":"S102", "subtype":"norfolk_courthouse_brick_exterior" }
{ "public_path":"norfolk/factory/F065_empty_courtroom_wide.mp4", "act":2, "covers_scene_id":"S103", "subtype":"empty_courtroom_wide" }
{ "public_path":"norfolk/factory/F066_jury_box_empty_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"jury_box_empty_cold" }
{ "public_path":"norfolk/factory/F067_court_hallway_marble.mp4", "act":2, "covers_scene_id":null, "subtype":"court_hallway_marble" }
{ "public_path":"norfolk/factory/F068_files_stack_desk_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"files_stack_desk_dim" }
{ "public_path":"norfolk/factory/F069_phone_90s_office_desk.mp4", "act":2, "covers_scene_id":null, "subtype":"phone_90s_office_desk" }
{ "public_path":"norfolk/factory/F070_folder_drawer_closing_dim.mp4", "act":2, "covers_scene_id":"S067", "subtype":"folder_drawer_closing_dim" }
{ "public_path":"norfolk/factory/F071_metal_chairs_row_dim.mp4", "act":2, "covers_scene_id":"S080", "subtype":"metal_chairs_row_dim" }
{ "public_path":"norfolk/factory/F072_city_street_norfolk_90s.mp4", "act":2, "covers_scene_id":null, "subtype":"city_street_norfolk_90s" }
{ "public_path":"norfolk/factory/F073_dna_lab_interior_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"dna_lab_interior_cold_02" }
{ "public_path":"norfolk/factory/F074_gel_electrophoresis_equipment_02.mp4", "act":2, "covers_scene_id":null, "subtype":"gel_electrophoresis_equipment_02" }
{ "public_path":"norfolk/factory/F075_lab_vials_rack_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"lab_vials_rack_cold_02" }
{ "public_path":"norfolk/factory/F076_police_station_corridor_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"police_station_corridor_dim_02" }
{ "public_path":"norfolk/factory/F077_lineup_room_empty_02.mp4", "act":2, "covers_scene_id":null, "subtype":"lineup_room_empty_02" }
{ "public_path":"norfolk/factory/F078_corkboard_string_wall_unreadable_02.mp4", "act":2, "covers_scene_id":null, "subtype":"corkboard_string_wall_unreadable_02" }
{ "public_path":"norfolk/factory/F079_norfolk_courthouse_brick_exterior_02.mp4", "act":2, "covers_scene_id":null, "subtype":"norfolk_courthouse_brick_exterior_02" }
{ "public_path":"norfolk/factory/F080_empty_courtroom_wide_02.mp4", "act":2, "covers_scene_id":null, "subtype":"empty_courtroom_wide_02" }
{ "public_path":"norfolk/factory/F081_jury_box_empty_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"jury_box_empty_cold_02" }
{ "public_path":"norfolk/factory/F082_court_hallway_marble_02.mp4", "act":2, "covers_scene_id":null, "subtype":"court_hallway_marble_02" }
{ "public_path":"norfolk/factory/F083_files_stack_desk_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"files_stack_desk_dim_02" }
{ "public_path":"norfolk/factory/F084_folder_drawer_closing_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"folder_drawer_closing_dim_02" }
{ "public_path":"norfolk/factory/F085_metal_chairs_row_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"metal_chairs_row_dim_02" }
{ "public_path":"norfolk/factory/F086_city_street_norfolk_90s_02.mp4", "act":2, "covers_scene_id":null, "subtype":"city_street_norfolk_90s_02" }
{ "public_path":"norfolk/factory/F087_dna_lab_interior_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"dna_lab_interior_cold_03" }
{ "public_path":"norfolk/factory/F088_gel_electrophoresis_equipment_03.mp4", "act":2, "covers_scene_id":null, "subtype":"gel_electrophoresis_equipment_03" }
{ "public_path":"norfolk/factory/F089_empty_courtroom_wide_03.mp4", "act":2, "covers_scene_id":null, "subtype":"empty_courtroom_wide_03" }
{ "public_path":"norfolk/factory/F090_norfolk_courthouse_brick_exterior_03.mp4", "act":2, "covers_scene_id":null, "subtype":"norfolk_courthouse_brick_exterior_03" }
{ "public_path":"norfolk/factory/F091_corkboard_string_wall_unreadable_03.mp4", "act":2, "covers_scene_id":null, "subtype":"corkboard_string_wall_unreadable_03" }
{ "public_path":"norfolk/factory/F092_metal_chairs_row_dim_03.mp4", "act":2, "covers_scene_id":null, "subtype":"metal_chairs_row_dim_03" }
{ "public_path":"norfolk/factory/F093_files_stack_desk_dim_03.mp4", "act":2, "covers_scene_id":null, "subtype":"files_stack_desk_dim_03" }
{ "public_path":"norfolk/factory/F094_jury_box_empty_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"jury_box_empty_cold_03" }
{ "public_path":"norfolk/factory/F095_police_station_corridor_dim_03.mp4", "act":2, "covers_scene_id":null, "subtype":"police_station_corridor_dim_03" }
{ "public_path":"norfolk/factory/F096_lab_vials_rack_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"lab_vials_rack_cold_03" }
// ACT3 The Letter (act 3) — 48
{ "public_path":"norfolk/factory/F097_prison_exterior_day.mp4", "act":3, "covers_scene_id":"S106", "subtype":"prison_exterior_day" }
{ "public_path":"norfolk/factory/F098_razor_wire_fence_distant.mp4", "act":3, "covers_scene_id":null, "subtype":"razor_wire_fence_distant" }
{ "public_path":"norfolk/factory/F099_cell_block_window_exterior.mp4", "act":3, "covers_scene_id":"S107", "subtype":"cell_block_window_exterior" }
{ "public_path":"norfolk/factory/F100_prison_corridor_long.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_corridor_long" }
{ "public_path":"norfolk/factory/F101_prison_yard_empty_nonsensational.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_yard_empty_nonsensational" }
{ "public_path":"norfolk/factory/F102_mail_sorting_room.mp4", "act":3, "covers_scene_id":"S115", "subtype":"mail_sorting_room" }
{ "public_path":"norfolk/factory/F103_letter_envelope_closeup_unreadable.mp4", "act":3, "covers_scene_id":"S116", "subtype":"letter_envelope_closeup_unreadable" }
{ "public_path":"norfolk/factory/F104_mailbox_row_dim.mp4", "act":3, "covers_scene_id":null, "subtype":"mailbox_row_dim" }
{ "public_path":"norfolk/factory/F105_desk_lamp_paper_dim.mp4", "act":3, "covers_scene_id":"S119", "subtype":"desk_lamp_paper_dim" }
{ "public_path":"norfolk/factory/F106_stack_of_files_office.mp4", "act":3, "covers_scene_id":null, "subtype":"stack_of_files_office" }
{ "public_path":"norfolk/factory/F107_courtroom_defense_table.mp4", "act":3, "covers_scene_id":"S136", "subtype":"courtroom_defense_table" }
{ "public_path":"norfolk/factory/F108_gavel_bench_empty_cold.mp4", "act":3, "covers_scene_id":"S140", "subtype":"gavel_bench_empty_cold" }
{ "public_path":"norfolk/factory/F109_law_books_shelf_dim.mp4", "act":3, "covers_scene_id":null, "subtype":"law_books_shelf_dim" }
{ "public_path":"norfolk/factory/F110_courthouse_steps_gray.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_steps_gray" }
{ "public_path":"norfolk/factory/F111_vault_door_closed_heavy.mp4", "act":3, "covers_scene_id":"S131", "subtype":"vault_door_closed_heavy" }
{ "public_path":"norfolk/factory/F112_visiting_room_empty.mp4", "act":3, "covers_scene_id":null, "subtype":"visiting_room_empty" }
{ "public_path":"norfolk/factory/F113_prison_gate_closed_day.mp4", "act":3, "covers_scene_id":"S143", "subtype":"prison_gate_closed_day" }
{ "public_path":"norfolk/factory/F114_gray_winter_sky_slow.mp4", "act":3, "covers_scene_id":null, "subtype":"gray_winter_sky_slow" }
{ "public_path":"norfolk/factory/F115_prison_exterior_day_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_exterior_day_02" }
{ "public_path":"norfolk/factory/F116_razor_wire_fence_distant_02.mp4", "act":3, "covers_scene_id":null, "subtype":"razor_wire_fence_distant_02" }
{ "public_path":"norfolk/factory/F117_cell_block_window_exterior_02.mp4", "act":3, "covers_scene_id":null, "subtype":"cell_block_window_exterior_02" }
{ "public_path":"norfolk/factory/F118_prison_corridor_long_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_corridor_long_02" }
{ "public_path":"norfolk/factory/F119_prison_yard_empty_nonsensational_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_yard_empty_nonsensational_02" }
{ "public_path":"norfolk/factory/F120_mail_sorting_room_02.mp4", "act":3, "covers_scene_id":null, "subtype":"mail_sorting_room_02" }
{ "public_path":"norfolk/factory/F121_letter_envelope_closeup_unreadable_02.mp4", "act":3, "covers_scene_id":null, "subtype":"letter_envelope_closeup_unreadable_02" }
{ "public_path":"norfolk/factory/F122_desk_lamp_paper_dim_02.mp4", "act":3, "covers_scene_id":null, "subtype":"desk_lamp_paper_dim_02" }
{ "public_path":"norfolk/factory/F123_stack_of_files_office_02.mp4", "act":3, "covers_scene_id":null, "subtype":"stack_of_files_office_02" }
{ "public_path":"norfolk/factory/F124_courtroom_defense_table_02.mp4", "act":3, "covers_scene_id":null, "subtype":"courtroom_defense_table_02" }
{ "public_path":"norfolk/factory/F125_gavel_bench_empty_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"gavel_bench_empty_cold_02" }
{ "public_path":"norfolk/factory/F126_law_books_shelf_dim_02.mp4", "act":3, "covers_scene_id":null, "subtype":"law_books_shelf_dim_02" }
{ "public_path":"norfolk/factory/F127_courthouse_steps_gray_02.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_steps_gray_02" }
{ "public_path":"norfolk/factory/F128_vault_door_closed_heavy_02.mp4", "act":3, "covers_scene_id":null, "subtype":"vault_door_closed_heavy_02" }
{ "public_path":"norfolk/factory/F129_visiting_room_empty_02.mp4", "act":3, "covers_scene_id":null, "subtype":"visiting_room_empty_02" }
{ "public_path":"norfolk/factory/F130_prison_gate_closed_day_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_gate_closed_day_02" }
{ "public_path":"norfolk/factory/F131_gray_winter_sky_slow_02.mp4", "act":3, "covers_scene_id":null, "subtype":"gray_winter_sky_slow_02" }
{ "public_path":"norfolk/factory/F132_mailbox_row_dim_02.mp4", "act":3, "covers_scene_id":null, "subtype":"mailbox_row_dim_02" }
{ "public_path":"norfolk/factory/F133_prison_exterior_day_03.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_exterior_day_03" }
{ "public_path":"norfolk/factory/F134_cell_block_window_exterior_03.mp4", "act":3, "covers_scene_id":null, "subtype":"cell_block_window_exterior_03" }
{ "public_path":"norfolk/factory/F135_prison_corridor_long_03.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_corridor_long_03" }
{ "public_path":"norfolk/factory/F136_letter_envelope_closeup_unreadable_03.mp4", "act":3, "covers_scene_id":null, "subtype":"letter_envelope_closeup_unreadable_03" }
{ "public_path":"norfolk/factory/F137_desk_lamp_paper_dim_03.mp4", "act":3, "covers_scene_id":null, "subtype":"desk_lamp_paper_dim_03" }
{ "public_path":"norfolk/factory/F138_courtroom_defense_table_03.mp4", "act":3, "covers_scene_id":null, "subtype":"courtroom_defense_table_03" }
{ "public_path":"norfolk/factory/F139_gavel_bench_empty_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"gavel_bench_empty_cold_03" }
{ "public_path":"norfolk/factory/F140_vault_door_closed_heavy_03.mp4", "act":3, "covers_scene_id":null, "subtype":"vault_door_closed_heavy_03" }
{ "public_path":"norfolk/factory/F141_prison_yard_empty_nonsensational_03.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_yard_empty_nonsensational_03" }
{ "public_path":"norfolk/factory/F142_razor_wire_fence_distant_03.mp4", "act":3, "covers_scene_id":null, "subtype":"razor_wire_fence_distant_03" }
{ "public_path":"norfolk/factory/F143_courthouse_steps_gray_03.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_steps_gray_03" }
{ "public_path":"norfolk/factory/F144_prison_gate_closed_day_03.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_gate_closed_day_03" }
// ACT4 The Long Undoing (act 4) — 44
{ "public_path":"norfolk/factory/F145_federal_courthouse_columns.mp4", "act":4, "covers_scene_id":"S173", "subtype":"federal_courthouse_columns" }
{ "public_path":"norfolk/factory/F146_marble_corridor_power.mp4", "act":4, "covers_scene_id":"S155", "subtype":"marble_corridor_power" }
{ "public_path":"norfolk/factory/F147_virginia_capitol_richmond.mp4", "act":4, "covers_scene_id":"S177", "subtype":"virginia_capitol_richmond" }
{ "public_path":"norfolk/factory/F148_us_flag_slow_wave.mp4", "act":4, "covers_scene_id":null, "subtype":"us_flag_slow_wave" }
{ "public_path":"norfolk/factory/F149_press_cameras_no_faces.mp4", "act":4, "covers_scene_id":"S160", "subtype":"press_cameras_no_faces" }
{ "public_path":"norfolk/factory/F150_documentary_light_rig.mp4", "act":4, "covers_scene_id":null, "subtype":"documentary_light_rig" }
{ "public_path":"norfolk/factory/F151_prison_gate_opening_day.mp4", "act":4, "covers_scene_id":"S167", "subtype":"prison_gate_opening_day" }
{ "public_path":"norfolk/factory/F152_gray_dawn_release_sky.mp4", "act":4, "covers_scene_id":"S163", "subtype":"gray_dawn_release_sky" }
{ "public_path":"norfolk/factory/F153_dna_lab_modern_cold.mp4", "act":4, "covers_scene_id":"S170", "subtype":"dna_lab_modern_cold" }
{ "public_path":"norfolk/factory/F154_city_hall_norfolk_exterior.mp4", "act":4, "covers_scene_id":"S181", "subtype":"city_hall_norfolk_exterior" }
{ "public_path":"norfolk/factory/F155_waterfront_sunrise_warm.mp4", "act":4, "covers_scene_id":"S178", "subtype":"waterfront_sunrise_warm" }
{ "public_path":"norfolk/factory/F156_open_sea_dawn_cream.mp4", "act":4, "covers_scene_id":null, "subtype":"open_sea_dawn_cream" }
{ "public_path":"norfolk/factory/F157_courtroom_daylight_bright.mp4", "act":4, "covers_scene_id":null, "subtype":"courtroom_daylight_bright" }
{ "public_path":"norfolk/factory/F158_desk_pen_paper_unreadable.mp4", "act":4, "covers_scene_id":null, "subtype":"desk_pen_paper_unreadable" }
{ "public_path":"norfolk/factory/F159_handcuffs_on_table_evidence.mp4", "act":4, "covers_scene_id":"S184", "subtype":"handcuffs_on_table_evidence" }
{ "public_path":"norfolk/factory/F160_badge_on_table_dim.mp4", "act":4, "covers_scene_id":"S185", "subtype":"badge_on_table_dim" }
{ "public_path":"norfolk/factory/F161_federal_prison_exterior.mp4", "act":4, "covers_scene_id":"S188", "subtype":"federal_prison_exterior" }
{ "public_path":"norfolk/factory/F162_cell_door_closing_dim.mp4", "act":4, "covers_scene_id":"S189", "subtype":"cell_door_closing_dim" }
{ "public_path":"norfolk/factory/F163_federal_courthouse_columns_02.mp4", "act":4, "covers_scene_id":null, "subtype":"federal_courthouse_columns_02" }
{ "public_path":"norfolk/factory/F164_marble_corridor_power_02.mp4", "act":4, "covers_scene_id":null, "subtype":"marble_corridor_power_02" }
{ "public_path":"norfolk/factory/F165_virginia_capitol_richmond_02.mp4", "act":4, "covers_scene_id":null, "subtype":"virginia_capitol_richmond_02" }
{ "public_path":"norfolk/factory/F166_us_flag_slow_wave_02.mp4", "act":4, "covers_scene_id":null, "subtype":"us_flag_slow_wave_02" }
{ "public_path":"norfolk/factory/F167_press_cameras_no_faces_02.mp4", "act":4, "covers_scene_id":null, "subtype":"press_cameras_no_faces_02" }
{ "public_path":"norfolk/factory/F168_prison_gate_opening_day_02.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_gate_opening_day_02" }
{ "public_path":"norfolk/factory/F169_gray_dawn_release_sky_02.mp4", "act":4, "covers_scene_id":null, "subtype":"gray_dawn_release_sky_02" }
{ "public_path":"norfolk/factory/F170_dna_lab_modern_cold_02.mp4", "act":4, "covers_scene_id":null, "subtype":"dna_lab_modern_cold_02" }
{ "public_path":"norfolk/factory/F171_waterfront_sunrise_warm_02.mp4", "act":4, "covers_scene_id":null, "subtype":"waterfront_sunrise_warm_02" }
{ "public_path":"norfolk/factory/F172_open_sea_dawn_cream_02.mp4", "act":4, "covers_scene_id":null, "subtype":"open_sea_dawn_cream_02" }
{ "public_path":"norfolk/factory/F173_courtroom_daylight_bright_02.mp4", "act":4, "covers_scene_id":null, "subtype":"courtroom_daylight_bright_02" }
{ "public_path":"norfolk/factory/F174_badge_on_table_dim_02.mp4", "act":4, "covers_scene_id":null, "subtype":"badge_on_table_dim_02" }
{ "public_path":"norfolk/factory/F175_federal_prison_exterior_02.mp4", "act":4, "covers_scene_id":null, "subtype":"federal_prison_exterior_02" }
{ "public_path":"norfolk/factory/F176_cell_door_closing_dim_02.mp4", "act":4, "covers_scene_id":null, "subtype":"cell_door_closing_dim_02" }
{ "public_path":"norfolk/factory/F177_city_hall_norfolk_exterior_02.mp4", "act":4, "covers_scene_id":null, "subtype":"city_hall_norfolk_exterior_02" }
{ "public_path":"norfolk/factory/F178_handcuffs_on_table_evidence_02.mp4", "act":4, "covers_scene_id":null, "subtype":"handcuffs_on_table_evidence_02" }
{ "public_path":"norfolk/factory/F179_federal_courthouse_columns_03.mp4", "act":4, "covers_scene_id":null, "subtype":"federal_courthouse_columns_03" }
{ "public_path":"norfolk/factory/F180_virginia_capitol_richmond_03.mp4", "act":4, "covers_scene_id":null, "subtype":"virginia_capitol_richmond_03" }
{ "public_path":"norfolk/factory/F181_prison_gate_opening_day_03.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_gate_opening_day_03" }
{ "public_path":"norfolk/factory/F182_waterfront_sunrise_warm_03.mp4", "act":4, "covers_scene_id":null, "subtype":"waterfront_sunrise_warm_03" }
{ "public_path":"norfolk/factory/F183_open_sea_dawn_cream_03.mp4", "act":4, "covers_scene_id":null, "subtype":"open_sea_dawn_cream_03" }
{ "public_path":"norfolk/factory/F184_gray_dawn_release_sky_03.mp4", "act":4, "covers_scene_id":null, "subtype":"gray_dawn_release_sky_03" }
{ "public_path":"norfolk/factory/F185_us_flag_slow_wave_03.mp4", "act":4, "covers_scene_id":null, "subtype":"us_flag_slow_wave_03" }
{ "public_path":"norfolk/factory/F186_marble_corridor_power_03.mp4", "act":4, "covers_scene_id":null, "subtype":"marble_corridor_power_03" }
{ "public_path":"norfolk/factory/F187_dna_lab_modern_cold_03.mp4", "act":4, "covers_scene_id":null, "subtype":"dna_lab_modern_cold_03" }
{ "public_path":"norfolk/factory/F188_federal_prison_exterior_03.mp4", "act":4, "covers_scene_id":null, "subtype":"federal_prison_exterior_03" }
// ENDING (act 5) — 14
{ "public_path":"norfolk/factory/F189_harbor_sunrise_cream.mp4", "act":5, "covers_scene_id":"S195", "subtype":"harbor_sunrise_cream" }
{ "public_path":"norfolk/factory/F190_pier_dawn_warm.mp4", "act":5, "covers_scene_id":"S196", "subtype":"pier_dawn_warm" }
{ "public_path":"norfolk/factory/F191_empty_room_daylight.mp4", "act":5, "covers_scene_id":"S202", "subtype":"empty_room_daylight" }
{ "public_path":"norfolk/factory/F192_quiet_street_dawn.mp4", "act":5, "covers_scene_id":null, "subtype":"quiet_street_dawn" }
{ "public_path":"norfolk/factory/F193_sea_horizon_cream_band.mp4", "act":5, "covers_scene_id":"S205", "subtype":"sea_horizon_cream_band" }
{ "public_path":"norfolk/factory/F194_harbor_sunrise_cream_02.mp4", "act":5, "covers_scene_id":null, "subtype":"harbor_sunrise_cream_02" }
{ "public_path":"norfolk/factory/F195_pier_dawn_warm_02.mp4", "act":5, "covers_scene_id":null, "subtype":"pier_dawn_warm_02" }
{ "public_path":"norfolk/factory/F196_empty_room_daylight_02.mp4", "act":5, "covers_scene_id":null, "subtype":"empty_room_daylight_02" }
{ "public_path":"norfolk/factory/F197_quiet_street_dawn_02.mp4", "act":5, "covers_scene_id":null, "subtype":"quiet_street_dawn_02" }
{ "public_path":"norfolk/factory/F198_sea_horizon_cream_band_02.mp4", "act":5, "covers_scene_id":null, "subtype":"sea_horizon_cream_band_02" }
{ "public_path":"norfolk/factory/F199_harbor_sunrise_cream_03.mp4", "act":5, "covers_scene_id":null, "subtype":"harbor_sunrise_cream_03" }
{ "public_path":"norfolk/factory/F200_pier_dawn_warm_03.mp4", "act":5, "covers_scene_id":null, "subtype":"pier_dawn_warm_03" }
{ "public_path":"norfolk/factory/F201_quiet_street_dawn_03.mp4", "act":5, "covers_scene_id":null, "subtype":"quiet_street_dawn_03" }
{ "public_path":"norfolk/factory/F202_sea_horizon_cream_band_03.mp4", "act":5, "covers_scene_id":null, "subtype":"sea_horizon_cream_band_03" }
// 繋ぎ (covers_scene_id:null・情景) — 30
{ "public_path":"norfolk/factory/F203_sky_gradient_slate_slow.mp4", "act":3, "covers_scene_id":null, "subtype":"sky_gradient_slate_slow" }
{ "public_path":"norfolk/factory/F204_water_reflection_harbor.mp4", "act":1, "covers_scene_id":null, "subtype":"water_reflection_harbor" }
{ "public_path":"norfolk/factory/F205_brick_wall_texture_pan.mp4", "act":1, "covers_scene_id":null, "subtype":"brick_wall_texture_pan" }
{ "public_path":"norfolk/factory/F206_institutional_corridor_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"institutional_corridor_cold" }
{ "public_path":"norfolk/factory/F207_marble_floor_reflection.mp4", "act":2, "covers_scene_id":null, "subtype":"marble_floor_reflection" }
{ "public_path":"norfolk/factory/F208_file_cabinets_row_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"file_cabinets_row_dim" }
{ "public_path":"norfolk/factory/F209_fog_over_harbor.mp4", "act":3, "covers_scene_id":null, "subtype":"fog_over_harbor" }
{ "public_path":"norfolk/factory/F210_gulls_over_gray_sky.mp4", "act":1, "covers_scene_id":null, "subtype":"gulls_over_gray_sky" }
{ "public_path":"norfolk/factory/F211_rain_glass_bokeh_night.mp4", "act":1, "covers_scene_id":null, "subtype":"rain_glass_bokeh_night" }
{ "public_path":"norfolk/factory/F212_norfolk_cityscape_distant.mp4", "act":4, "covers_scene_id":null, "subtype":"norfolk_cityscape_distant" }
{ "public_path":"norfolk/factory/F213_virginia_landscape_wide.mp4", "act":4, "covers_scene_id":null, "subtype":"virginia_landscape_wide" }
{ "public_path":"norfolk/factory/F214_dock_ropes_detail.mp4", "act":1, "covers_scene_id":null, "subtype":"dock_ropes_detail" }
{ "public_path":"norfolk/factory/F215_anchor_chain_rust_detail.mp4", "act":1, "covers_scene_id":null, "subtype":"anchor_chain_rust_detail" }
{ "public_path":"norfolk/factory/F216_streetlight_night_cone.mp4", "act":1, "covers_scene_id":null, "subtype":"streetlight_night_cone" }
{ "public_path":"norfolk/factory/F217_sky_gradient_slate_slow_02.mp4", "act":3, "covers_scene_id":null, "subtype":"sky_gradient_slate_slow_02" }
{ "public_path":"norfolk/factory/F218_water_reflection_harbor_02.mp4", "act":3, "covers_scene_id":null, "subtype":"water_reflection_harbor_02" }
{ "public_path":"norfolk/factory/F219_brick_wall_texture_pan_02.mp4", "act":2, "covers_scene_id":null, "subtype":"brick_wall_texture_pan_02" }
{ "public_path":"norfolk/factory/F220_institutional_corridor_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"institutional_corridor_cold_02" }
{ "public_path":"norfolk/factory/F221_marble_floor_reflection_02.mp4", "act":4, "covers_scene_id":null, "subtype":"marble_floor_reflection_02" }
{ "public_path":"norfolk/factory/F222_file_cabinets_row_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"file_cabinets_row_dim_02" }
{ "public_path":"norfolk/factory/F223_fog_over_harbor_02.mp4", "act":3, "covers_scene_id":null, "subtype":"fog_over_harbor_02" }
{ "public_path":"norfolk/factory/F224_gulls_over_gray_sky_02.mp4", "act":5, "covers_scene_id":null, "subtype":"gulls_over_gray_sky_02" }
{ "public_path":"norfolk/factory/F225_rain_glass_bokeh_night_02.mp4", "act":2, "covers_scene_id":null, "subtype":"rain_glass_bokeh_night_02" }
{ "public_path":"norfolk/factory/F226_norfolk_cityscape_distant_02.mp4", "act":4, "covers_scene_id":null, "subtype":"norfolk_cityscape_distant_02" }
{ "public_path":"norfolk/factory/F227_dock_ropes_detail_02.mp4", "act":5, "covers_scene_id":null, "subtype":"dock_ropes_detail_02" }
{ "public_path":"norfolk/factory/F228_streetlight_night_cone_02.mp4", "act":2, "covers_scene_id":null, "subtype":"streetlight_night_cone_02" }
{ "public_path":"norfolk/factory/F229_sky_gradient_slate_slow_03.mp4", "act":4, "covers_scene_id":null, "subtype":"sky_gradient_slate_slow_03" }
{ "public_path":"norfolk/factory/F230_water_reflection_harbor_03.mp4", "act":5, "covers_scene_id":null, "subtype":"water_reflection_harbor_03" }
{ "public_path":"norfolk/factory/F231_institutional_corridor_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"institutional_corridor_cold_03" }
{ "public_path":"norfolk/factory/F232_fog_over_harbor_03.mp4", "act":3, "covers_scene_id":null, "subtype":"fog_over_harbor_03" }
```

**検算:** 12 + 44 + 40 + 48 + 44 + 14 + 30 = 232 ✓・全 public_path 非空 ✓（不変条件17）・各1回使用（cap 1）。**暗いクリップは全体の1/3=約77本まで**（harbor 昼光・waterfront sunrise・lab の実用光・daylight courtroom を混ぜる）。**gavel/天秤系の汎用象徴は合計≤2本**（footage_diversity ゲート・F108/F125/F139 のうち実際に cut に出すのは≤2）。

## 4.5 ★`motion[]` 全42エントリ（★必ず実体化・public_path 非空）

> エントリ形は §4.1a 準拠 + 動画フィールド。`asset_id ^NOR-M\d{2}$`。`source_still` は §8.1a の種画像、`source_scene_id`=`MS<NN>`。runtime で `sha256`/`width 1280`/`height 720`/`fps 48`/`frames`/`duration_sec`/`qc` を埋める（§8.4）。**空配列を書かない。**

```jsonc
{ "asset_id":"NOR-M01", "source_scene_id":"MS01", "source_still":"H:/pd-media/assets/ai/norfolk/M01_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M01_rife.mp4", "public_path":"norfolk/motion/M01_rife.mp4", "act":0, "storyboard":"hook", "tags":["tally_strokes_appear"] }
{ "asset_id":"NOR-M02", "source_scene_id":"MS02", "source_still":"H:/pd-media/assets/ai/norfolk/M02_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M02_rife.mp4", "public_path":"norfolk/motion/M02_rife.mp4", "act":0, "storyboard":"A0-01", "tags":["bulb_cone_shifts"] }
{ "asset_id":"NOR-M03", "source_scene_id":"MS03", "source_still":"H:/pd-media/assets/ai/norfolk/M03_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M03_rife.mp4", "public_path":"norfolk/motion/M03_rife.mp4", "act":0, "storyboard":"A0-02", "tags":["harbor_dawn_warship_drift"] }
{ "asset_id":"NOR-M04", "source_scene_id":"MS04", "source_still":"H:/pd-media/assets/ai/norfolk/M04_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M04_rife.mp4", "public_path":"norfolk/motion/M04_rife.mp4", "act":1, "storyboard":"A1-01", "tags":["man_led_down_corridor_backs","H001_anon"] }
{ "asset_id":"NOR-M05", "source_scene_id":"MS05", "source_still":"H:/pd-media/assets/ai/norfolk/M05_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M05_rife.mp4", "public_path":"norfolk/motion/M05_rife.mp4", "act":1, "storyboard":"A1-02", "tags":["apartment_door_absence_light"] }
{ "asset_id":"NOR-M06", "source_scene_id":"MS06", "source_still":"H:/pd-media/assets/ai/norfolk/M06_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M06_rife.mp4", "public_path":"norfolk/motion/M06_rife.mp4", "act":1, "storyboard":"A1-03", "tags":["interrogation_leanin_silhouette","H002_anon"] }
{ "asset_id":"NOR-M07", "source_scene_id":"MS07", "source_still":"H:/pd-media/assets/ai/norfolk/M07_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M07_rife.mp4", "public_path":"norfolk/motion/M07_rife.mp4", "act":1, "storyboard":"A1-04", "tags":["suspect_head_in_hands_back","H003_anon"] }
{ "asset_id":"NOR-M08", "source_scene_id":"MS08", "source_still":"H:/pd-media/assets/ai/norfolk/M08_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M08_rife.mp4", "public_path":"norfolk/motion/M08_rife.mp4", "act":1, "storyboard":"A1-05", "tags":["polygraph_needle_smear"] }
{ "asset_id":"NOR-M09", "source_scene_id":"MS09", "source_still":"H:/pd-media/assets/ai/norfolk/M09_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M09_rife.mp4", "public_path":"norfolk/motion/M09_rife.mp4", "act":1, "storyboard":"A1-06", "tags":["hand_signs_unreadable_page","H004_anon"] }
{ "asset_id":"NOR-M10", "source_scene_id":"MS10", "source_still":"H:/pd-media/assets/ai/norfolk/M10_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M10_rife.mp4", "public_path":"norfolk/motion/M10_rife.mp4", "act":1, "storyboard":"A1-07", "tags":["clock_hands_blur_eleven_hours"] }
{ "asset_id":"NOR-M11", "source_scene_id":"MS11", "source_still":"H:/pd-media/assets/ai/norfolk/M11_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M11_rife.mp4", "public_path":"norfolk/motion/M11_rife.mp4", "act":1, "storyboard":"A1-08", "tags":["hand_chalks_first_tally","H005_anon"] }
{ "asset_id":"NOR-M12", "source_scene_id":"MS12", "source_still":"H:/pd-media/assets/ai/norfolk/M12_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M12_rife.mp4", "public_path":"norfolk/motion/M12_rife.mp4", "act":2, "storyboard":"A2-01", "tags":["gel_bands_one_lane_empty"] }
{ "asset_id":"NOR-M13", "source_scene_id":"MS13", "source_still":"H:/pd-media/assets/ai/norfolk/M13_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M13_rife.mp4", "public_path":"norfolk/motion/M13_rife.mp4", "act":2, "storyboard":"A2-02", "tags":["exclusion_strip_filed_drawer"] }
{ "asset_id":"NOR-M14", "source_scene_id":"MS14", "source_still":"H:/pd-media/assets/ai/norfolk/M14_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M14_rife.mp4", "public_path":"norfolk/motion/M14_rife.mp4", "act":2, "storyboard":"A2-03", "tags":["new_suspect_corridor_escort","H006_anon"] }
{ "asset_id":"NOR-M15", "source_scene_id":"MS15", "source_still":"H:/pd-media/assets/ai/norfolk/M15_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M15_rife.mp4", "public_path":"norfolk/motion/M15_rife.mp4", "act":2, "storyboard":"A2-04", "tags":["chairs_multiply_under_bulb"] }
{ "asset_id":"NOR-M16", "source_scene_id":"MS16", "source_still":"H:/pd-media/assets/ai/norfolk/M16_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M16_rife.mp4", "public_path":"norfolk/motion/M16_rife.mp4", "act":2, "storyboard":"A2-05", "tags":["second_man_in_chair_silhouette","H007_anon"] }
{ "asset_id":"NOR-M17", "source_scene_id":"MS17", "source_still":"H:/pd-media/assets/ai/norfolk/M17_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M17_rife.mp4", "public_path":"norfolk/motion/M17_rife.mp4", "act":2, "storyboard":"A2-06", "tags":["corkboard_strings_spread"] }
{ "asset_id":"NOR-M18", "source_scene_id":"MS18", "source_still":"H:/pd-media/assets/ai/norfolk/M18_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M18_rife.mp4", "public_path":"norfolk/motion/M18_rife.mp4", "act":2, "storyboard":"A2-07", "tags":["lineup_figures_step_out","H008_anon"] }
{ "asset_id":"NOR-M19", "source_scene_id":"MS19", "source_still":"H:/pd-media/assets/ai/norfolk/M19_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M19_rife.mp4", "public_path":"norfolk/motion/M19_rife.mp4", "act":2, "storyboard":"A2-08", "tags":["tallies_two_three_four"] }
{ "asset_id":"NOR-M20", "source_scene_id":"MS20", "source_still":"H:/pd-media/assets/ai/norfolk/M20_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M20_rife.mp4", "public_path":"norfolk/motion/M20_rife.mp4", "act":2, "storyboard":"A2-09", "tags":["empty_evidence_table_sweep"] }
{ "asset_id":"NOR-M21", "source_scene_id":"MS21", "source_still":"H:/pd-media/assets/ai/norfolk/M21_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M21_rife.mp4", "public_path":"norfolk/motion/M21_rife.mp4", "act":3, "storyboard":"A3-01", "tags":["hand_writes_letter_cell","H009_anon"] }
{ "asset_id":"NOR-M22", "source_scene_id":"MS22", "source_still":"H:/pd-media/assets/ai/norfolk/M22_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M22_rife.mp4", "public_path":"norfolk/motion/M22_rife.mp4", "act":3, "storyboard":"A3-02", "tags":["envelope_dropped_mailbin","H010_anon"] }
{ "asset_id":"NOR-M23", "source_scene_id":"MS23", "source_still":"H:/pd-media/assets/ai/norfolk/M23_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M23_rife.mp4", "public_path":"norfolk/motion/M23_rife.mp4", "act":3, "storyboard":"A3-03", "tags":["letter_unfolds_cream_light"] }
{ "asset_id":"NOR-M24", "source_scene_id":"MS24", "source_still":"H:/pd-media/assets/ai/norfolk/M24_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M24_rife.mp4", "public_path":"norfolk/motion/M24_rife.mp4", "act":3, "storyboard":"A3-04", "tags":["letter_set_aside_under_stack"] }
{ "asset_id":"NOR-M25", "source_scene_id":"MS25", "source_still":"H:/pd-media/assets/ai/norfolk/M25_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M25_rife.mp4", "public_path":"norfolk/motion/M25_rife.mp4", "act":3, "storyboard":"A3-05", "tags":["gel_lane_snaps_match"] }
{ "asset_id":"NOR-M26", "source_scene_id":"MS26", "source_still":"H:/pd-media/assets/ai/norfolk/M26_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M26_rife.mp4", "public_path":"norfolk/motion/M26_rife.mp4", "act":3, "storyboard":"A3-06", "tags":["plea_head_bows_shadow","H011_anon"] }
{ "asset_id":"NOR-M27", "source_scene_id":"MS27", "source_still":"H:/pd-media/assets/ai/norfolk/M27_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M27_rife.mp4", "public_path":"norfolk/motion/M27_rife.mp4", "act":3, "storyboard":"A3-07", "tags":["vault_handle_turns_stays_shut"] }
{ "asset_id":"NOR-M28", "source_scene_id":"MS28", "source_still":"H:/pd-media/assets/ai/norfolk/M28_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M28_rife.mp4", "public_path":"norfolk/motion/M28_rife.mp4", "act":3, "storyboard":"A3-08", "tags":["four_cell_doors_close"] }
{ "asset_id":"NOR-M29", "source_scene_id":"MS29", "source_still":"H:/pd-media/assets/ai/norfolk/M29_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M29_rife.mp4", "public_path":"norfolk/motion/M29_rife.mp4", "act":4, "storyboard":"A4-01", "tags":["cell_window_seasons_shift"] }
{ "asset_id":"NOR-M30", "source_scene_id":"MS30", "source_still":"H:/pd-media/assets/ai/norfolk/M30_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M30_rife.mp4", "public_path":"norfolk/motion/M30_rife.mp4", "act":4, "storyboard":"A4-02", "tags":["veterans_rise_backs","H012_anon"] }
{ "asset_id":"NOR-M31", "source_scene_id":"MS31", "source_still":"H:/pd-media/assets/ai/norfolk/M31_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M31_rife.mp4", "public_path":"norfolk/motion/M31_rife.mp4", "act":4, "storyboard":"A4-03", "tags":["family_hands_sort_letters","H013_anon"] }
{ "asset_id":"NOR-M32", "source_scene_id":"MS32", "source_still":"H:/pd-media/assets/ai/norfolk/M32_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M32_rife.mp4", "public_path":"norfolk/motion/M32_rife.mp4", "act":4, "storyboard":"A4-04", "tags":["doc_light_flickers_chair","H014_anon"] }
{ "asset_id":"NOR-M33", "source_scene_id":"MS33", "source_still":"H:/pd-media/assets/ai/norfolk/M33_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M33_rife.mp4", "public_path":"norfolk/motion/M33_rife.mp4", "act":4, "storyboard":"A4-05", "tags":["gates_half_open_gray"] }
{ "asset_id":"NOR-M34", "source_scene_id":"MS34", "source_still":"H:/pd-media/assets/ai/norfolk/M34_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M34_rife.mp4", "public_path":"norfolk/motion/M34_rife.mp4", "act":4, "storyboard":"A4-06", "tags":["men_walk_out_gray_dawn","H015_anon"] }
{ "asset_id":"NOR-M35", "source_scene_id":"MS35", "source_still":"H:/pd-media/assets/ai/norfolk/M35_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M35_rife.mp4", "public_path":"norfolk/motion/M35_rife.mp4", "act":4, "storyboard":"A4-07", "tags":["ladder_ignites_cream_flood"] }
{ "asset_id":"NOR-M36", "source_scene_id":"MS36", "source_still":"H:/pd-media/assets/ai/norfolk/M36_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M36_rife.mp4", "public_path":"norfolk/motion/M36_rife.mp4", "act":4, "storyboard":"A4-08", "tags":["badge_laid_down_cuffs","H016_anon"] }
{ "asset_id":"NOR-M37", "source_scene_id":"MS37", "source_still":"H:/pd-media/assets/ai/norfolk/M37_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M37_rife.mp4", "public_path":"norfolk/motion/M37_rife.mp4", "act":4, "storyboard":"A4-09", "tags":["corridor_walk_in_cuffs","H017_anon"] }
{ "asset_id":"NOR-M38", "source_scene_id":"MS38", "source_still":"H:/pd-media/assets/ai/norfolk/M38_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M38_rife.mp4", "public_path":"norfolk/motion/M38_rife.mp4", "act":4, "storyboard":"A4-10", "tags":["cream_light_across_opinion_page"] }
{ "asset_id":"NOR-M39", "source_scene_id":"MS39", "source_still":"H:/pd-media/assets/ai/norfolk/M39_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M39_rife.mp4", "public_path":"norfolk/motion/M39_rife.mp4", "act":5, "storyboard":"A5-01", "tags":["tallies_washed_one_remains"] }
{ "asset_id":"NOR-M40", "source_scene_id":"MS40", "source_still":"H:/pd-media/assets/ai/norfolk/M40_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M40_rife.mp4", "public_path":"norfolk/motion/M40_rife.mp4", "act":5, "storyboard":"A5-02", "tags":["four_figures_pier_dawn_caps","H018_anon"] }
{ "asset_id":"NOR-M41", "source_scene_id":"MS41", "source_still":"H:/pd-media/assets/ai/norfolk/M41_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M41_rife.mp4", "public_path":"norfolk/motion/M41_rife.mp4", "act":5, "storyboard":"A5-03", "tags":["letter_folded_kept"] }
{ "asset_id":"NOR-M42", "source_scene_id":"MS42", "source_still":"H:/pd-media/assets/ai/norfolk/M42_src.png", "path":"H:/pd-media/assets/ai_video/norfolk/M42_rife.mp4", "public_path":"norfolk/motion/M42_rife.mp4", "act":5, "storyboard":"A5-04", "tags":["harbor_dawn_cream_band_widens"] }
```

**検算:** 42エントリ ✓・全 public_path 非空 ✓（不変条件18）・`^NOR-M\d{2}$` ✓・**★H001–H018（匿名人物・18本）は M04/M06/M07/M09/M11/M14/M16/M18/M21/M22/M26/M30/M31/M32/M34/M36/M37/M40 の内数 ✓**（＝42 motion のうち 18 が人物・84 cuts のうち最大36が人物）。残り24本が抽象/象徴。幕別 3/8/9/8/10/4 = 42 ✓。

## 4.6 `overlay[]` 30エントリ（distinct 素材に数えない・15 particle / 10 light / 5 vfx）

```jsonc
{ "public_path":"norfolk/overlay/P01_cold_room_dust.mp4", "type":"particle_assets", "subtype":"cold_room_dust", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P02_interrogation_dust_cone.mp4", "type":"particle_assets", "subtype":"interrogation_dust_cone", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P03_archive_dust_cold.mp4", "type":"particle_assets", "subtype":"archive_dust_cold", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P04_harbor_mist_motes.mp4", "type":"particle_assets", "subtype":"harbor_mist_motes", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P05_lab_dust_motes.mp4", "type":"particle_assets", "subtype":"lab_dust_motes", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P06_courtroom_dust.mp4", "type":"particle_assets", "subtype":"courtroom_dust", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P07_prison_dust_cold.mp4", "type":"particle_assets", "subtype":"prison_dust_cold", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P08_paper_fiber_drift.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P09_night_air_drift.mp4", "type":"particle_assets", "subtype":"night_air_drift", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P10_chalk_dust_drift.mp4", "type":"particle_assets", "subtype":"chalk_dust_drift", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P11_cold_room_dust_02.mp4", "type":"particle_assets", "subtype":"cold_room_dust_02", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P12_interrogation_dust_cone_02.mp4", "type":"particle_assets", "subtype":"interrogation_dust_cone_02", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P13_harbor_mist_motes_02.mp4", "type":"particle_assets", "subtype":"harbor_mist_motes_02", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P14_lab_dust_motes_02.mp4", "type":"particle_assets", "subtype":"lab_dust_motes_02", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/P15_paper_fiber_drift_02.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift_02", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/L01_harbor_slate_shaft.mp4", "type":"light_assets", "subtype":"harbor_slate_shaft", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/L02_cold_window_light_bar.mp4", "type":"light_assets", "subtype":"cold_window_light_bar", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/L03_bare_bulb_glow_harsh_white.mp4", "type":"light_assets", "subtype":"bare_bulb_glow_harsh_white", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/L04_slate_edge_glow.mp4", "type":"light_assets", "subtype":"slate_edge_glow", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/L05_letter_cream_edge_glow.mp4", "type":"light_assets", "subtype":"letter_cream_edge_glow", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/L06_lab_panel_glow_cold.mp4", "type":"light_assets", "subtype":"lab_panel_glow_cold", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/L07_cold_key_light_sweep.mp4", "type":"light_assets", "subtype":"cold_key_light_sweep", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/L08_harbor_slate_shaft_02.mp4", "type":"light_assets", "subtype":"harbor_slate_shaft_02", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/L09_letter_cream_edge_glow_02.mp4", "type":"light_assets", "subtype":"letter_cream_edge_glow_02", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/L10_bare_bulb_glow_harsh_white_02.mp4", "type":"light_assets", "subtype":"bare_bulb_glow_harsh_white_02", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/V01_film_grain_fine.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine", "blend_hint":"overlay" }
{ "public_path":"norfolk/overlay/V02_cold_light_noise.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/V03_film_grain_fine_02.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine_02", "blend_hint":"overlay" }
{ "public_path":"norfolk/overlay/V04_cold_light_noise_02.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise_02", "blend_hint":"screen" }
{ "public_path":"norfolk/overlay/V05_slate_glitch_min.mp4", "type":"vfx_overlays", "subtype":"slate_glitch_min", "blend_hint":"screen" }
```

**検算:** 15 + 10 + 5 = 30 ✓。runtime で `asset_id`/`path`/`sha256`/`license`/`eyeballed_content`/`qc` を埋める。**overlay は `cuts[].src` に出さない。★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない（DESIGN §1）。scanline/CRT/vignette-wash の overlay を選ばない。** 発色は B が accent `#56707F`（harbor-slate）に寄せる想定・letter-cream `#E4D5A3` の light（L05/L09）は ACT3 の手紙と ACT4 後半〜ENDING の truth ビート用のみ。他話色（electric blue/sodium gold/porch amber/teal/crimson/forest-green/civil-violet/somber-plum/steel-cyan/**EP52 evidence-blue #3F5E8C**）を選ばない。

---

# 5. A-1: SDXL 静止画のバッチ生成（205本 × 1枚・バリエーション0）— ★全行 literal（1行1固有プロンプト）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-053-norfolk/04_scenes/ai_prompts.v001.md   ← A が §5.9 の形式で書く
出力:  H:\pd-media\assets\ai\norfolk\S<NNN>.png（+ remotion/public/norfolk/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★205本の構成＝2レーン（EP52 と同じ・EP48/49「人がいない」却下を潰す・★R3+ owner directive 2026-07-26「人間が映った画像は結構必要」で 55→85 に増量）

- **object/symbolic レーン（120枚）＝ `[STYLE]`+`[NEG]`（人物なし）:** タリー壁・裸電球の取調室・空の椅子・Navy caps・港/軍艦・アパートの absence・DNA gel・手紙（cream）・封筒・独房窓・vault door・バッジ/手錠・dawn 等。**spine motif（タリー壁・手紙・裸電球・DNA gel・椅子の増殖・4つの caps・アパート absence）は object のまま**（象徴の純度を守る）。
- **★human-present レーン（85枚＝41.5%）＝ `[HSTYLE]`+`[HNEG]`（匿名・非識別の人物）:** narration に人がいるビート（捜査官・被疑者の背中・法廷・受刑者・家族・元FBI・記者・釈放の歩み・Navy の日常・待つ家族）に **匿名・非識別の人物（背向き/影/silhouette/hands・adults only）** を入れる。該当行は §5.6 で **★HP** と明記（ACT1 21／ACT2 21／ACT3 17／ACT4 26 = 85。ACT0/ACT5 は象徴のみ）。**★anti-samey（似たような画像を作らない）:** ★HP 85行は shot distance（CU hands／medium／wide／over-shoulder／group）・pose（seated／standing／walking／slumped／embracing）・angle（back／profile-in-shadow／high／low／through-aperture）・年齢/体格/服装・幕別ライティングを分散させ、**subject+composition+lighting の3点が同じ ★HP 行を2行作らない**（§6.1 Q4 の ★HP クラスタで phash 監視）。
- **HARD BAN（両レーン共通）: 実在人物（4人の水兵/Ford/Ballard/Michelle/Billy/家族/Taylor/判事/知事）の likeness なし・被害者/レイプ/暴行/遺体/凶器/ナイフの描写なし・可読テキスト（自白調書/手紙の文字/判決文/新聞/日付/数字）なし。** タリー（チョークの線）は文字ではない＝可。

## 5.3 共通スタイル `[STYLE]`（object/symbolic 120 ＋ 抽象 i2v 種に連結・DESIGN §1 と一字一致）

```
, cinematic still, somber documentary grade, a cold harbor-slate blue-gray key light as the one recurring cool note, near-black ink institutional gravity, one bare interrogation bulb as a harsh blown-white cone of light in darkness, chalk tally marks on a dark wall as the confession-count motif, a folded letter on cream paper as the buried-truth motif reserved for the letter and the finale, a gray Navy harbor of warship silhouettes and wet piers, a small 1990s brick apartment rendered as cold quiet absence never any victim or violence, cold slate gel-electrophoresis bands as the forensic motif, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, backs and hands and objects only
```

> **EP39〜EP52 の色語（1語も含めない）:** electric blue / sodium prison gold / porch-amber / teal-green hospital / crimson kitchen / forest-green / civil-violet Texas road / glover / somber-plum Utah / steel-cyan（EP50）/ **cold evidence-blue #3F5E8C（EP52）** / Texas homecoming-gold #D19A3E（EP52）。**EP53 の色は harbor-slate `#56707F`（INK `#0A0C0E`）＋手紙と真実の帰結のみ letter-cream `#E4D5A3`＋裸電球の blown-white。** EP52 morton と法廷/監獄/ラボの被写体が重なるが、EP52=Texas 郊外×evidence-blue、EP53=**大西洋の軍港×harbor-slate×レンガ**＝別レーン。cyan と混同しない（本作は脱彩度の slate gray-blue）。

## 5.4 共通ネガティブ `[NEG]`（各 `Avoid:` の後に全文付ける・A/B 同一）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible confession, legible letter, legible handwriting, legible police report, legible newspaper, legible lab report, legible date, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, front-facing person, victim, murder victim, dead body, corpse, wounds, injury, blood, gore, knife, weapon, stabbing, strangulation, assault, rape, sexual content, nudity, crime scene, re-enactment, crying woman, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, saturated indigo evidence-blue, milky haze, foggy wash, scanline, CRT texture, vignette wash
```

> 文字/紙面が必要な絵は「blurred into an unreadable smear」で判読不能に。**被害者・暴行・遺体・凶器・可読の偽公文書を NEG で明示抑制。** この `[NEG]` は象徴 120 ＋ 抽象 i2v 種にのみ使う。**人物ビート（§5.11 H・§5.6 ★HP・§5.12 thumb_face・§5.13 F）には使わない**（人物を弾くため）。H/★HP は `[HNEG]`、thumb は `[TNEG]`、F は `[FNEG]`。

## 5.5 プロンプトの絶対ルール（205本すべてに適用）

- **body 205 は2レーン（§5.2）:** object/symbolic 120枚＝§5.3/§5.4、★HP 85枚＝§5.11 `[HSTYLE]`/`[HNEG]`（匿名・非識別・背向き/影/silhouette/hands・adults only）。
- **可読文字なし。** 自白調書・手紙・封筒の宛名・ポリグラフ紙・DNAレポート・判決文・新聞・日付・金額を描かない（タリーのチョーク線は文字でない＝可）。
- **被害者・レイプ・暴行・殺害・遺体・現場・凶器（ナイフ）を一切描かない。** アパートは empty rooms of absence のみ。**襲撃の再現を誰の視点でも作らない。**
- **4人の innocence（制約1）:** 4人が犯人に見える絵を作らない（取調室の被疑者は「壊されていく無実の男」として dignity をもって・lurid にしない）。
- **Ballard を美化しない（制約4）:** cold・distance・非識別 silhouette。Ford の記章/バッジは「権力→収監」の mirror としてのみ。
- **harbor-slate system（`#56707F`）を基調に、letter-cream `#E4D5A3` は ACT3 の手紙初出〜ACT4 後半/ENDING の truth ビートのみ**（§5.6 の per-motif 指定に従う）。裸電球は blown-white（色でなく光として）。
- **★footage treatment は bleed/parallax（DESIGN §1）。depth 前提の絵作りをしない**（平面的でクリアな構図でよい）。
- **dochighlight を作らない・書かない（制約8）。** milky wash / scanline を描かない。

## 5.6 ★全205行の literal プロンプト表（幕別・S001..S205 穴なし・★HP 行は `[HSTYLE]`/`[HNEG]`）

> **このまま `ai_prompts.v001.md` へ転記する**（§5.9 の2行形式）。各行末尾の `[STYLE]`/`[NEG]`/`[HSTYLE]`/`[HNEG]` は §5.3/§5.4/§5.11 の全文に展開して連結すること。

### ACT 0 — HOOK + OPENING（15枚・S001–S015）

**hook_signature_objects — 4 — S001–S004**（S001 = also_thumb・hook signature tally。反復規律によりタリーは S001 の1枚のみ・S002–S004 は COLD OPEN の別要素を担う新規 distinct）
```
- `S001.png`
Five chalk tally marks on a dark interrogation-room wall lit by one bare bulb, four of the strokes struck through with a hard diagonal line, chalk dust drifting in the cone of light, the confession count, no letters or numerals, no people, no readable text [STYLE] Avoid: [NEG]
- `S002.png`
A street map of a gray harbor city rendered as an unreadable blur under a low desk lamp, four push-pins clustered tight around one small block and a fifth pin standing far alone at the map's edge, the men they chose and the man they missed, no legible names, no people [STYLE] Avoid: [NEG]
- `S003.png`
A detective's brass desk nameplate lying face-down beside a 1990s rotary telephone on a dim squad-room desk, its engraving pressed into the blotter, the man to keep your eye on introduced as an object, macro, cold slate light, no legible characters, no people [STYLE] Avoid: [NEG]
- `S004.png`
Four cheap ballpoint pens lined up on dark steel under a harsh bulb, caps chewed and clips bent, the instruments of four signed lies, macro still-life, no paper in frame, no hands, no people, no readable text [STYLE] Avoid: [NEG]
```

**the_room_and_the_town — 4 — S005–S008**（bulb/room は S005 の1枚のみ〔点灯・待機状態〕・S006–S008 は OPENING の Navy 町を担う新規 distinct）
```
- `S005.png`
A bare incandescent bulb hanging from a cord over an empty steel table and two metal chairs, a hard blown-white cone of light cutting near-black darkness, a small windowless room implied by shadow, no people, no readable text [STYLE] Avoid: [NEG]
- `S006.png`
Eight steel lockers in a narrow Navy berthing passage, seven doors shut flush and one standing ajar into darkness, cold slate light down the row, eight names the case would claim, no legible stencils, no people [STYLE] Avoid: [NEG]
- `S007.png`
An unmarked 1990s police sedan parked alone under a streetlight at night, rain beading on its hood and windshield, the watcher's car waiting outside ordinary lives, no people, no readable plates, no readable text [STYLE] Avoid: [NEG]
- `S008.png`
A warship's boarding gangway at night with a single chain hooked across its foot, wet steel steps rising into darkness, the husband gone to sea, quiet foreboding, no people, no readable text [STYLE] Avoid: [NEG]
```

**navy_caps_harbor — 4 — S009–S012**
```
- `S009.png`
Four white US Navy sailor caps set in a row on a dark steel table under cold harbor-slate light, one small cone of warmer bulb light grazing them, the four men rendered as objects, no insignia readable, no people, no text [STYLE] Avoid: [NEG]
- `S010.png`
Gray warship silhouettes on a Norfolk harbor horizon before dawn, cranes and masts as black cutouts against a slate sky, wet pier in the foreground reflecting cold light, no people, no readable text [STYLE] Avoid: [NEG]
- `S011.png`
A single white sailor cap resting upside down on wet pier planks at night, harbor lights blurred beyond, rain-damp sheen on the wood, quiet foreboding, no people, no readable text [STYLE] Avoid: [NEG]
- `S012.png`
Close on the gray riveted hull of a Navy warship filling the frame like a wall, cold slate light sliding across the steel plates, the institution as texture, no markings readable, no people, no text [STYLE] Avoid: [NEG]
```

**opening_title_abstract — 3 — S013–S015**
```
- `S013.png`
An abstract near-black field with one horizontal band of cold harbor-slate light across the lower third like a sea horizon at night, minimal title underlay, fine film grain, no objects, no people, no text [STYLE] Avoid: [NEG]
- `S014.png`
Dark water surface at night filling the frame, small slate-gray ripples catching a distant cold light, depth and dread without any subject, abstract underlay, no people, no readable text [STYLE] Avoid: [NEG]
- `S015.png`
A slow gradient from ink black up into desaturated harbor-slate gray with a faint suggestion of distant dock cranes at the bottom edge, atmospheric abstract underlay, no people, no readable text [STYLE] Avoid: [NEG]
```

### ACT 1 — THE FIRST CONFESSION（45枚・S016–S060）

**norfolk_navy_town_1997 — 6 — S016–S021**（★HP: S016–S017, S020 の3行。harbor-scape は S016/S018 の2枚に集約・S017/S019–S021 は「不在の町」の暮らしを担う新規 distinct）
```
- `S016.png`
A wide Norfolk naval harbor at gray dawn, rows of warship silhouettes and dock cranes under a low slate sky, a scatter of anonymized sailor figures walking the distant pier as small dark shapes, a Navy town waking, all figures far and non-identifiable, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S017.png`
An anonymized young sailor stand-in seen only from behind at a bank of 1990s pay phones on a Navy pier at dusk, receiver pressed to his ear, shoulders hunched against the harbor wind, a town of absences calling home, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S018.png`
Dockyard gantry cranes against a pale slate sky at first light, geometric black frames over still harbor water, industry asleep, no people, no readable text [STYLE] Avoid: [NEG]
- `S019.png`
A small naval base chapel interior, short rows of empty wooden pews in cold slate window light, a simple altar table with a model ship, where the young marriages of a Navy town begin, no people, no readable text [STYLE] Avoid: [NEG]
- `S020.png`
Two anonymized young women stand-ins seen from behind sitting close together on an exterior apartment stairwell at dusk, coffee mugs in hand, the neighbors who become your whole world when the ships are out, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S021.png`
A small 1990s coin laundromat near the base at night, one machine's round window glowing mid-cycle, a basket of folded Navy whites on the counter, the town of absences after dark, no people, no readable signage [STYLE] Avoid: [NEG]
```

**apartment_ordinary_life — 6 — S022–S027**
```
- `S022.png`
A modest 1990s two-story brick apartment building near a naval base at dusk, identical doors and thin railings, one window lit warm among dark ones, ordinary life before everything, no people, no readable signage [STYLE] Avoid: [NEG]
- `S023.png`
A young married couple's small kitchen table with two coffee mugs, one washed and turned down, one waiting, morning light through a thin curtain, tender ordinary absence, no people, no readable text [STYLE] Avoid: [NEG]
- `S024.png`
A narrow apartment-block corridor with identical doors receding under a buzzing fluorescent tube, worn carpet, cold institutional quiet, no people, no readable numbers on the doors [STYLE] Avoid: [NEG]
- `S025.png`
A wall calendar rendered as an unreadable smear beside a hallway phone in a small 1990s apartment, seven days circled only as a soft blur, the length of a deployment, no legible characters, no people [STYLE] Avoid: [NEG]
- `S026.png`
A pair of white Navy dress shoes by an apartment door beside a small pair of women's sneakers, the doormat worn, domestic and quiet, cold slate light from a window, no people, no readable text [STYLE] Avoid: [NEG]
- `S027.png`
A thin gold wedding band resting on a windowsill in pale morning light, out-of-focus brick apartment courtyard beyond the glass, a marriage measured in weeks, macro, no people, no readable text [STYLE] Avoid: [NEG]
```

**the_return — 4 — S028–S031**（発見の朝＝restraint・不在のみ・内部の crime detail ゼロ）
```
- `S028.png`
A Navy seabag dropped upright in an apartment-block stairwell, its shadow long under a cold fluorescent light, the homecoming interrupted, nothing else in frame, no people, no readable text [STYLE] Avoid: [NEG]
- `S029.png`
An apartment front door standing slightly ajar into darkness at the end of a dim corridor, one cold blade of slate light across the floor, absolute stillness, nothing visible inside, no people, no readable text [STYLE] Avoid: [NEG]
- `S030.png`
A brass apartment door key still hanging in the lock of a closed door, the corridor around it dim and silent, the moment before the world ends held forever, macro, no people, no readable text [STYLE] Avoid: [NEG]
- `S031.png`
The brick apartment building exterior at midday under a bleached overcast sky, every window dark and curtained, the building itself gone quiet, slight low angle, no people, no readable text [STYLE] Avoid: [NEG]
```

**apartment_absence — 4 — S032–S035**（被害者・暴行・遺体・血・凶器なし＝absence のみ）
```
- `S032.png`
An empty, tidy 1990s apartment living room rendered as cold absence, a couch and a small television dark and still, thin light through closed blinds striping the floor, no person, no victim, no violence, no readable text [STYLE] Avoid: [NEG]
- `S033.png`
A small apartment hallway interior, undisturbed, family photos on the wall thrown to soft unreadable blur, the quiet of a place where something has already happened, no person, no violence, no blood, no readable text [STYLE] Avoid: [NEG]
- `S034.png`
A closed white bedroom door at the end of a short apartment hall, dim slate light, the camera keeping a respectful distance, nothing shown beyond, absence as grief, no person, no violence, no readable text [STYLE] Avoid: [NEG]
- `S035.png`
A woman's cardigan folded over the back of a kitchen chair in an empty apartment, morning light gone cold across it, a life interrupted mid-week, dignity and stillness, no person, no violence, no readable text [STYLE] Avoid: [NEG]
```

**★HP police_arrive — 6 — S036–S041**（匿名の警官/隣人・backs/silhouette・adults only）
```
- `S036.png`
Anonymized police officers and stunned neighbors seen only from behind and in cold silhouette outside a 1990s brick apartment building washed in red-and-blue light at dusk, small figures under the building's dark mass, no faces, no crime imagery, no readable text [HSTYLE] Avoid: [HNEG]
- `S037.png`
An anonymized uniformed officer's back filling the left of frame as yellow barrier tape rendered as an unreadable blur crosses an apartment courtyard, cold evening light, procedure descending on ordinary life, no face, no legible text [HSTYLE] Avoid: [HNEG]
- `S038.png`
Two anonymized detectives in plain jackets seen from behind at a distance, standing before an apartment stairwell in cold light, notebooks in hand rendered unreadable, deciding the story early, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S039.png`
A cluster of anonymized neighbors in silhouette at the edge of a parking lot at dusk, arms crossed, watching police lights play across brick walls, grief and rumor beginning, all backs and shadows, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S040.png`
An anonymized young sailor stand-in seen only from behind, standing very still between two patrol cars under cold flashing light, shoulders rigid, the husband's world ending kept at a dignified distance, no face, no crime imagery, no readable text [HSTYLE] Avoid: [HNEG]
- `S041.png`
An anonymized officer's gloved hands closing a patrol car door in the foreground while apartment windows glow cold beyond, night settling on the complex, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

**★HP first_knock — 3 — S042–S044**（隣人 Williams が連行される・匿名・backs）
```
- `S042.png`
Knuckles of an anonymized detective's hand raised to knock on an apartment door in a dim corridor, seen over the shoulder so no face reads, the knock that starts everything, cold fluorescent light, no readable text [HSTYLE] Avoid: [HNEG]
- `S043.png`
An anonymized young man stand-in in a plain t-shirt seen only from behind, being walked between two suited detectives down an apartment breezeway at night toward a waiting car, compliant and confused, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S044.png`
Through a rain-flecked car window, an anonymized man's silhouette in the back seat looking toward a police station's cold entrance lights, all shapes and reflections, no face readable, no readable text [HSTYLE] Avoid: [HNEG]
```

**interrogation_night_and_its_cost — 6 — S045–S050**（★HP: S045–S046, S048–S049 の4行。部屋そのものの絵は S046/S047/S049 に集約・S045/S048/S050 は同ビートの別要素を担う新規 distinct）
```
- `S045.png`
An anonymized detective stand-in seen from behind at a cluttered 1990s squad-room desk deep in the night, one desk lamp burning over spread folders rendered unreadable, a telephone cord pulled taut, a case being decided within hours, seated, medium, no face, no legible text [HSTYLE] Avoid: [HNEG]
- `S046.png`
An anonymized observer's dark silhouette seen close from behind at a wide one-way observation mirror, his faint reflection hanging over the lit empty table and bulb cone beyond the glass, the watcher and the machine in one frame, over-shoulder, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S047.png`
A round institutional wall clock with its hands and numerals thrown to a soft unreadable blur, high on a dark interrogation-room wall above the light cone, time made meaningless, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S048.png`
An anonymized detective's hands threading a fresh microcassette into a tape recorder at the edge of the steel interrogation table, the suspect's slumped silhouette soft in the cone beyond, the statement about to be taken again until it fits, cropped to hands and dark cuffs, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S049.png`
The interrogation table seen from directly above, an anonymized young man stand-in seated with his head bowed so only hair and shoulders read, hands flat on the steel, the bulb's cone pinning him like a specimen, high-angle crucible geometry, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S050.png`
An empty county-jail visiting booth, a scratched plexiglass pane and a stool bolted to the floor, a telephone handset hanging dead on its cradle, the seat he could not leave while his wife was dying, cold fluorescent light, no people, no readable text [STYLE] Avoid: [NEG]
```

**★HP eleven_hours — 3 — S051–S053**（消耗する被疑者と迫る取調官・匿名・dignity）
```
- `S051.png`
An anonymized exhausted young man stand-in seated at a steel interrogation table, head bowed deep into his hands so no face reads, shoulders collapsed under a harsh bulb cone, hour after hour made visible, dignified and terrible, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S052.png`
An anonymized detective stand-in seen from behind leaning far across the interrogation table into the light cone, his shadow swallowing the slumped silhouette of a young man opposite, the pressure of the room made physical, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S053.png`
Two anonymized silhouettes at a steel table in a dark room, the standing one gesturing with a folder rendered unreadable, the seated one shrunken small in the chair, the eleventh hour, all backs and shadow, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```

**polygraph_lie — 3 — S054–S056**（「不合格」の嘘・可読数字なし・★HP: S054 の1行＝匿名 examiner・他2行は object）
```
- `S054.png`
An anonymized examiner's hands adjusting the dials of a vintage polygraph machine, seen over a dark-suited shoulder so no face reads, needles resting against paper rendered as an unreadable smear, cables coiled like restraints, the lie-detector being prepared to tell a lie, no face, no legible marks [HSTYLE] Avoid: [HNEG]
- `S055.png`
Extreme close-up of a polygraph needle mid-swing, scratching a jagged unreadable line onto rolling paper, harsh white side light, menace in a machine, no legible characters, no people [STYLE] Avoid: [NEG]
- `S056.png`
A strip of polygraph chart paper torn off and left curling on a steel table under the bulb cone, its traces blurred to illegibility, the verdict nobody was shown, no readable text, no people [STYLE] Avoid: [NEG]
```

**signature_unreadable — 2 — S057–S058**（自白書面への署名・hands-only・可読文字なし・★HP: S057 の1行＝hands を [HSTYLE] レーンへ・S058 は object）
```
- `S057.png`
Close on an anonymized trembling hand signing the bottom of a typed page whose every line is blurred into an unreadable smear, a cheap pen, harsh bulb light, the moment a life is signed away, hands only, no face, no legible words [HSTYLE] Avoid: [HNEG]
- `S058.png`
A signed statement rendered entirely as an unreadable smear lying squared on a steel table beside a pen, the bulb cone centering it like an altar piece, cold and final, no legible characters, no people [STYLE] Avoid: [NEG]
```

**first_tally — 2 — S059–S060**（confession #1・S060 = also_thumb）
```
- `S059.png`
A single fresh chalk tally stroke on the dark interrogation-room wall, chalk dust still falling from its tail, caught in the edge of the bulb cone, the first false confession counted, no letters, no people [STYLE] Avoid: [NEG]
- `S060.png`
The interrogation room seen wide from a low corner, one bare bulb, the steel table, and one empty chair facing camera inside the blown-white cone, darkness pressing in on every side, the machine at rest between victims, no people, no readable text [STYLE] Avoid: [NEG]
```

### ACT 2 — THE DOMINO（45枚・S061–S105・engine・最密）

**dna_lab_cold — 6 — S061–S066**（★HP: S061, S064 の2行＝ラボの人間・他4行は object）
```
- `S061.png`
An anonymized forensic technician stand-in in a white lab coat seen from behind at a DNA laboratory bench in cold slate light, racked vials and a gel tray before them, the one honest witness in the case at work, wide and clinical, no face, no readable labels [HSTYLE] Avoid: [HNEG]
- `S062.png`
Extreme close-up of a sealed evidence vial of clear fluid held in a steel rack, cold rim light tracing the glass, clinical purity against darkness, no readable label, no people [STYLE] Avoid: [NEG]
- `S063.png`
A gel-electrophoresis tray glowing faint harbor-slate in a dark lab, ladders of pale bands beginning to resolve, science speaking quietly, abstract, no readable numerals, no people [STYLE] Avoid: [NEG]
- `S064.png`
An anonymized technician's gloved hands seating sample tubes into an open centrifuge rotor under a cold task lamp, the machinery of certainty being loaded by hand, macro, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S065.png`
A wall of cold steel lab refrigerators with their indicator lights as small slate points in darkness, evidence sleeping for years, wide symmetrical composition, no people, no readable text [STYLE] Avoid: [NEG]
- `S066.png`
A micropipette suspended over an open tube, one clear drop caught mid-fall in hard side light, the exact instant of testing, macro freeze, no people, no readable text [STYLE] Avoid: [NEG]
```

**exclusion_strip_ignored — 4 — S067–S070**（不一致という真実が引き出しへ・★HP: S068 の1行＝人の手が真実を仕舞う・他3行は object）
```
- `S067.png`
A DNA gel ladder with one lane conspicuously empty where a match should be, the surrounding bands pale slate, the word no written in biology, abstract, no readable numerals, no people [STYLE] Avoid: [NEG]
- `S068.png`
An anonymized clerk's hand sliding a lab result sheet rendered entirely as an unreadable smear into a plain manila folder on a dark desk, cold light, the exclusion filed by a human hand instead of obeyed, cropped to hand and sleeve, no face, no legible characters [HSTYLE] Avoid: [HNEG]
- `S069.png`
A manila folder dropping into a deep metal file drawer among dozens of identical folders, motion frozen at the instant of burial, slate gloom, no readable labels, no people [STYLE] Avoid: [NEG]
- `S070.png`
A heavy metal file drawer pushed almost shut, one pale folder edge still catching a thin blade of cold light inside, truth going dark by inches, macro, no readable text, no people [STYLE] Avoid: [NEG]
```

**★HP new_suspect_recruited — 6 — S071–S076**（除外のたびに「次の男」・匿名・backs）
```
- `S071.png`
An anonymized young sailor stand-in seen only from behind being led down a police-station corridor by two suited figures, fluorescent tubes overhead, the next name on the list, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S072.png`
Knuckles of an anonymized detective's hand knocking on a barracks-room door, seen over the shoulder in cold institutional light, the domino falling on another innocent man, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S073.png`
An anonymized slight young man stand-in alone in the interrogation chair seen from behind through the doorway, small inside the bulb's white cone, the room waiting to begin again, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S074.png`
Two anonymized detectives' silhouettes conferring in a dark observation room, watching a lit interrogation window beyond, planning the next eleven hours, all backs and shadow, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S075.png`
An anonymized young man stand-in seen from behind in a Navy work jacket, hands flat on the steel table, head lowered, the second confession being grown, dignity kept, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S076.png`
An anonymized figure fingerprinted by anonymized hands at a booking counter, everything cropped to hands and dark sleeves, ink pad and card rendered unreadable, the machine stamping another innocent man, no faces, no legible text [HSTYLE] Avoid: [HNEG]
```

**domino_engine_objects — 6 — S077–S082**（椅子は S080/S081 の2枚に集約〔7脚の act peak＋倒れた1脚＝証拠が言い続けた答え・DESIGN §1/§2 指定〕・増殖の過程は M15 モーションが担う・S077–S079/S082 は同ビートの新規 distinct）
```
- `S077.png`
Two metal bunks in a small shared barracks room, one bed stripped to its bare frame and the other still made taut, a footlocker between them, the roommate the theory reached for next, cold slate light, no people, no readable text [STYLE] Avoid: [NEG]
- `S078.png`
A destroyer's long white wake stretching across black night water toward the horizon, seen from the stern rail, the alibi written on the sea itself, no people, no readable text [STYLE] Avoid: [NEG]
- `S079.png`
A witness-stand microphone in a dark 1990s courtroom, one hard shaft of cold light on its steel neck, borrowed words waiting to be spoken against innocent men, no people, no readable text [STYLE] Avoid: [NEG]
- `S080.png`
Seven empty metal chairs jammed into the small interrogation room, some outside the cone in half dark, the multi-attacker theory as furniture, wide claustrophobic composition, no people, no readable text [STYLE] Avoid: [NEG]
- `S081.png`
A single overturned metal chair lying on the dark floor at the edge of the bulb cone, the one chair the evidence ever needed, quiet accusation, no people, no readable text [STYLE] Avoid: [NEG]
- `S082.png`
Black fingerprint powder dusted across an apartment doorframe and light switch, revealing nothing, the spent brush lying below, seven charged men and not one trace, forensic macro, cold light, no people, no readable text [STYLE] Avoid: [NEG]
```

**count_rises — 4 — S083–S086**（タリーは S083/S085 の2枚〔2本目が加わる→4本そろう＝状態変化〕・S084/S086 は同ビートの新規 distinct）
```
- `S083.png`
A second chalk tally stroke being added beside the first on the dark wall, rendered as the fresh stroke alone with drifting chalk dust, no hand visible, the count rising, no letters, no people [STYLE] Avoid: [NEG]
- `S084.png`
A brown accordion case file swollen to bursting, its elastic band straining, standing alone on a steel shelf, a theory growing heavier exactly as it grew more false, cold slate light, no legible labels, no people [STYLE] Avoid: [NEG]
- `S085.png`
Four hard chalk tally marks filling the wall's light patch, aggressive and clustered, the bulb cone shaking slightly off-axis, four false confessions counted, no letters, no people [STYLE] Avoid: [NEG]
- `S086.png`
A wall-mounted fire-alarm pull station on an institutional corridor wall, its paint dulled dark in cold slate light, a fine skin of dust on the handle no one ever pulled, each exclusion an alarm nobody answered, macro, no people, no readable text [STYLE] Avoid: [NEG]
```

**theory_web — 5 — S087–S091**（膨張する「集団犯行」説・可読文字なし・★HP: S088 の1行＝説を育てる手・他4行は object）
```
- `S087.png`
A police corkboard where blank silhouette cards multiply outward, connected by taut red string into a spreading web, every card faceless and unreadable, the theory metastasizing, no legible text, no real faces [STYLE] Avoid: [NEG]
- `S088.png`
An anonymized detective's fingers driving a pushpin through a blank silhouette card into a corkboard, red string pulled tight across frame, one more man added to the story by hand, macro tension, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S089.png`
A tangle of red string crossing itself so densely over a dark corkboard that the board beneath disappears, a theory with more connections than evidence, abstract, no readable text, no people [STYLE] Avoid: [NEG]
- `S090.png`
Seven blank silhouette cards pinned in an arc around one empty center space on a corkboard, the missing eighth man nobody was looking for, cold slate light, no readable text, no faces [STYLE] Avoid: [NEG]
- `S091.png`
A corkboard web sagging under its own string, several cards hanging loose at angles, the story too heavy to hold its own shape, slate gloom, no readable text, no people [STYLE] Avoid: [NEG]
```

**zero_evidence — 4 — S092–S095**（★HP: S093 の1行＝空箱を運ぶ人・他3行は object）
```
- `S092.png`
A bare forensic examination table under one cold lamp with absolutely nothing on it, the physical case against seven men rendered exactly, symbolic emptiness, no people, no readable text [STYLE] Avoid: [NEG]
- `S093.png`
An anonymized evidence clerk stand-in seen from behind carrying an open, visibly empty evidence box down a dim institutional corridor, the lid balanced on top, the entire physical case against seven men held in two hands, walking, no face, no readable labels [HSTYLE] Avoid: [HNEG]
- `S094.png`
A small tidy 1990s apartment interior seen wide and undisturbed, nothing broken, nothing overturned, the scene that said one attacker all along, cold absence, no person, no violence, no readable text [STYLE] Avoid: [NEG]
- `S095.png`
A magnifying loupe lying on a dark tabletop reflecting only the bulb's white point, nothing beneath it to find, the investigation as an empty lens, macro, no people, no readable text [STYLE] Avoid: [NEG]
```

**★HP three_charged_dropped — 6 — S096–S101**（追加起訴の3人＝自白ゼロ・のち取り下げ）
```
- `S096.png`
Three anonymized sailor stand-ins seen only from behind standing in a bare lineup room, shoulders squared under cold light, charged on other men's coerced words, no faces, no height-chart markings readable [HSTYLE] Avoid: [HNEG]
- `S097.png`
An anonymized man stand-in seen from behind at a bus-station-style bench under fluorescent light, a duffel at his feet, three hundred miles from a crime he was charged with, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S098.png`
Anonymized hands fanning out time cards and bank slips rendered as unreadable smears across a kitchen table under a warm lamp going cold, an ordinary alibi that should have ended it, no face, no legible characters [HSTYLE] Avoid: [HNEG]
- `S099.png`
An anonymized figure seen from behind walking out of a courthouse door into gray daylight, unshackled, charges evaporating as quietly as they came, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S100.png`
Two anonymized sailor stand-ins from behind at a rail overlooking gray harbor water, caps in hands, men the state almost destroyed on words alone, still and small, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S101.png`
An anonymized man's hands unclenching around a chain-link fence outside a jail at dusk, cropped to hands and dark cuffs of a work jacket, release without apology, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

**★HP courtroom_thin — 4 — S102–S105**（4行すべて★HP＝法廷と待つ家族。空の法廷/空の陪審席は factory F065/F066 系が担う）
```
- `S102.png`
Two anonymized women stand-ins seen from behind in winter coats at the foot of a Norfolk brick courthouse's steps under a heavy slate sky, waiting close together, the families' vigil beginning outside the building where confessions would outweigh science, standing, group, no faces, no readable signage [HSTYLE] Avoid: [HNEG]
- `S103.png`
An empty wood-paneled courtroom seen from the back doors with a single anonymized clerk stand-in tiny at the far bench laying out papers rendered unreadable, one cold shaft on the witness stand, the stage being set for testimony written in an interrogation room, wide, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S104.png`
A row of anonymized jurors seen from behind and above filing into the jury box, dark coats and gray shoulders settling into twelve chairs in raking slate light, the audience the confession was built for taking its seats, high angle, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S105.png`
An anonymized defense lawyer stand-in seated alone at the defense table, seen in profile with the face lost to shadow, one hand resting on a blank legal pad under courtroom light, the thin side of the room occupied at last, quiet dread, no identifiable face, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 3 — THE LETTER（40枚・S106–S145）

**letter_cream_first — 6 — S106–S111**（cream の初出＝真実の色・★HP: S106 の1行＝面会日の訪問者。手紙そのものは S107 の1枚のみ〔白紙＝初期状態〕・S108–S111 は同ビートの新規 distinct〔待っていた物証/封じられた扉/こじ開けられていない錠/家族の vigil〕）
```
- `S106.png`
A state prison's long exterior wall and razor-wire crown under a gray winter sky, an anonymized woman stand-in seen from behind waiting small at the visitors' gate with a paper bag under her arm, the place the truth was living, wide, no face, no readable signage [HSTYLE] Avoid: [HNEG]
- `S107.png`
A bare prison cell interior with a steel desk shelf, a single sheet of cream paper on it glowing softly warm against the cold slate room, the first warm note in the film, no person, no readable text [STYLE] Avoid: [NEG]
- `S108.png`
Three sealed forensic evidence bags laid side by side on a cold laboratory counter, their labels soft unreadable smears, the swabs and scrapings that had waited two years to be believed, clinical slate light, no person, no legible characters [STYLE] Avoid: [NEG]
- `S109.png`
A 1990s apartment door sealed with a sagging, weathered strip of barrier tape rendered as an unreadable blur, dust and dead leaves gathered at the threshold, seasons passing over a closed truth, no person, no legible text [STYLE] Avoid: [NEG]
- `S110.png`
An intact apartment deadbolt and strike plate in extreme close-up, brass worn but unscratched, no splinter in the frame, the door that was opened from the inside, macro, cold slate light, no person, no readable text [STYLE] Avoid: [NEG]
- `S111.png`
A single small candle flame in a dark apartment window at dusk, the room behind it lost to shadow, a family's vigil kept with dignity, restrained and quiet, no person, no readable text [STYLE] Avoid: [NEG]
```

**★HP hand_writes_and_receives — 3 — S112–S114**（書く手 S112 →畳む手 S114＝状態変化の2枚のみ・S113 は受け取った女性＝新規 distinct・匿名・no face）
```
- `S112.png`
An anonymized inmate's hand gripping a pencil stub, mid-stroke across cream paper on a steel cell shelf, every written line blurred to an unreadable smear, cropped tight to hand and sleeve, no face, no legible words [HSTYLE] Avoid: [HNEG]
- `S113.png`
An anonymized woman stand-in seen only from behind at a small Norfolk kitchen table, holding a just-opened cream envelope very still, the taunt that became the truth arriving in her hands, warm paper against slate gloom, no face, no legible words [HSTYLE] Avoid: [HNEG]
- `S114.png`
An anonymized hand folding the finished cream letter in thirds with a slow careful crease, cell gloom around the warm paper, cropped to hands, the taunt sealed, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

**the_letter_enters_the_system — 4 — S115–S118**（郵便で届く真実。封筒の close は S116 の1枚のみ〔署に届いた状態〕・投函は M22/H010 モーションが担う・開封は M23 が担う・S115/S117/S118 は同ビートの新規 distinct）
```
- `S115.png`
A prison mailroom seen wide, canvas carts heaped with white mail under twin fluorescent tubes, a long steel sorting table, the ordinary room the truth had to pass through, no people, no readable addresses [STYLE] Avoid: [NEG]
- `S116.png`
A wall of wooden mail pigeonholes in a 1990s police department, one cream envelope corner protruding from a single slot among ranks of gray, easy to miss forever, wide frontal composition, no people, no readable labels [STYLE] Avoid: [NEG]
- `S117.png`
An empty press-briefing podium crowded with 1990s microphones in a bare municipal room, the seal on its front a soft unreadable blur, the machine that would announce an eighth man instead of an error, no people, no legible text [STYLE] Avoid: [NEG]
- `S118.png`
A closed office door with a frosted glass pane at the end of a dark corridor, no light behind the glass, a thin gleam dying on the linoleum, the room where nothing happened, no people, no legible characters [STYLE] Avoid: [NEG]
```

**letter_ignored — 3 — S119–S121**（S121 = also_thumb・置き去りの真実。手紙の close は S120/S121 の2枚〔押しやられる→独り残る＝状態変化〕・S119 は新規 distinct・埋葬は M24 が担う）
```
- `S119.png`
A wide 1990s government office floor at night, ranks of dark desks and dead terminals, one desk lamp burning far at the back over a pale page, a building asleep on the truth, no people, no legible writing [STYLE] Avoid: [NEG]
- `S120.png`
An anonymized hand pushing the cream letter to the far corner of a dark desk, fingers flat on the page mid-shove, the physical gesture of nothing happens, cropped to hand and sleeve only, no face, no person beyond the hand, no legible words [STYLE] Avoid: [NEG]
- `S121.png`
The folded cream letter alone on a vast dark desk in one narrow shaft of warm light, everything else swallowed by slate blackness, the ignored truth as the loneliest object in Virginia, no people, no legible writing [STYLE] Avoid: [NEG]
```

**ballard_silhouette — 4 — S122–S125**（真犯人＝cold silhouette・美化なし・likeness なし・★HP: S122, S124 の2行＝人物 silhouette を [HSTYLE] レーンへ・他2行は object）
```
- `S122.png`
A single anonymized male silhouette seen from behind at a distance through prison-visitation glass, dark against a pale wall, the man the DNA named, cold and unglorified, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S123.png`
A dark figure's shadow thrown long across a prison dayroom floor from out of frame, the man himself never shown, presence as absence, slate gloom, no face, no person visible, no readable text [STYLE] Avoid: [NEG]
- `S124.png`
An anonymized silhouette seated alone at a steel table in an empty prison visiting room, seen from behind and far away, hands folded, the only guilty man in the story, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S125.png`
A cell door's small observation hatch glowing faint slate in a dark corridor, the occupant unseen, threat contained and waiting, no person visible, no readable text [STYLE] Avoid: [NEG]
```

**the_match — 5 — S126–S130**（唯一の一致。gel ladder は S126 の1枚のみ〔一致＝状態変化・S063 現像中→S067 空レーン→S126 一致→S170 点火の evolving chain〕・★HP: S128 の1行＝深夜の分析者・S127/S129/S130 は同ビートの新規 distinct・一致の瞬間は M25 が担う）
```
- `S126.png`
A DNA gel ladder in a dark lab where one single lane aligns into a bright column while four neighboring lanes stay empty, the only match the case ever had, abstract slate glow, no readable numerals, no people [STYLE] Avoid: [NEG]
- `S127.png`
A dot-matrix printer in a dark laboratory, a long accordion-folded report spilling into its out-tray, every line a soft unreadable smear, the answer arriving as ordinary paperwork, cold slate light, no people, no legible characters [STYLE] Avoid: [NEG]
- `S128.png`
An anonymized lab analyst stand-in hunched at a workstation lamp over a sealed vial and a gel plate at night, seen from behind with the coat collar high, everything else dark, the machine that never lied working late in human hands, seated, medium, no face, no readable labels [HSTYLE] Avoid: [HNEG]
- `S129.png`
A laboratory cold-storage door standing open at last, a single sealed sample box carried off, its slot dark among the racked rows, evidence waking after two years asleep, no readable labels, no people [STYLE] Avoid: [NEG]
- `S130.png`
A small interview room with its door standing wide open, two paper coffee cups still steaming on the table beside a small tape machine, the confession that needed no eleven hours, calm cold light, no people, no readable text [STYLE] Avoid: [NEG]
```

**nothing_happens — 5 — S131–S135**（システムは手放さない・★HP: S134 の1行＝承認を押す人間の手・他4行は object）
```
- `S131.png`
A massive institutional vault door shut flush with a dark wall, its wheel and bolts catching cold slate light, the case that would not open, frontal symmetrical composition, no people, no readable text [STYLE] Avoid: [NEG]
- `S132.png`
A vault wheel mid-turn rendered as a frozen blur, yet every bolt still seated, motion without opening, the appeal that changes nothing, macro, no people, no readable text [STYLE] Avoid: [NEG]
- `S133.png`
Interlocking bureaucratic gears of dark steel filling the frame, all turning one direction, a small cream paper corner caught and crumpling between two teeth, the machine digesting the truth, abstract, no readable text, no people [STYLE] Avoid: [NEG]
- `S134.png`
An anonymized clerk's hand pressing a rubber date stamp onto an unreadable smeared form, the stamp's face turned away so no characters read, approval descending on the wrong story by an ordinary human hand, macro cold light, no face, no legible text [HSTYLE] Avoid: [HNEG]
- `S135.png`
The cream letter re-filed edge-on between hundreds of gray folders in a records shelf, one warm sliver almost vanished in slate ranks, the truth archived alive, no people, no readable labels [STYLE] Avoid: [NEG]
```

**★HP plea_under_threat — 4 — S136–S139**（死刑の影の下の答弁・匿名）
```
- `S136.png`
An anonymized young defendant stand-in at a defense table viewed from the gallery, chin dropped to his chest, palms pressed to the tabletop, one cold shaft crossing his shoulders, the surrender learned under the bulb now repeated before a judge, the plea-or-death arithmetic, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S137.png`
An anonymized defendant's hands clasped so tight the knuckles pale, cropped at the defense table's edge under courtroom light, choosing life over truth, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S138.png`
Two anonymized silhouettes — lawyer and client — leaning together at a defense table in a dark courtroom, the whispered advice that innocence is a fatal bet, all backs, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S139.png`
An anonymized young man stand-in from behind, standing to face an unseen bench, shoulders braced for the word life, dignity under the machine, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

**★HP trials_grind — 3 — S140–S142**（Wilson/Tice の裁判・匿名の法廷）
```
- `S140.png`
A 1990s courtroom seen from the back, anonymized jurors in the box and gallery spectators as shadowed non-identifiable backs, a witness silhouette small at the stand, verdicts built on borrowed words, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S141.png`
An anonymized jury forewoman's silhouette rising in the box, paper in hand rendered unreadable, the room's shadows leaning toward her, the moment of the split verdict, no face, no legible text [HSTYLE] Avoid: [HNEG]
- `S142.png`
An anonymized defendant stand-in seen from behind being turned by anonymized deputies toward a side door of the courtroom, the second trial ending like the first, all backs and shadow, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```

**four_doors_and_the_years — 3 — S143–S145**（4人とも収監・★HP: S144–S145 の2行。prison motif は S143/S144 の2枚〔4枚の扉→ハッチ越しの男〕・S145 は新規 distinct〔作業場の歳月〕）
```
- `S143.png`
Four identical steel cell doors in a row down a dark prison corridor, each with its small hatch shut, cold slate light pooling before them, four innocent men filed away, no people, no readable numbers [STYLE] Avoid: [NEG]
- `S144.png`
Seen through a cell door's small open food hatch, the blurred shoulder and clasped hands of an anonymized inmate stand-in seated deep in the cell's gloom, one of four men filed away behind identical steel, framed tight by the hatch, dignified and non-sensational, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S145.png`
An anonymized inmate stand-in seen from behind at an industrial sewing machine in a prison workshop, rows of empty stations receding into gloom, years measured out in piecework, seated, wide, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 4 — THE LONG UNDOING（45枚・S146–S190・climax・cascade・最密②）

**years_seasons — 5 — S146–S150**（★HP: S147・S148・S150 の3行＝[HSTYLE]/[HNEG]・他2行は object）
```
- `S146.png`
A single cell window abstracted to a pale rectangle of cold light, the color temperature shifting from winter gray toward thin summer across it, seasons passing with no calendar and no person, no readable text [STYLE] Avoid: [NEG]
- `S147.png`
An anonymized inmate stand-in seen from behind standing full-figure at a chain-link fence topped with razor wire, gray harbor water and a free horizon cut into diamonds beyond him, a Navy man a mile from the sea and unreachable from it, standing, wide, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S148.png`
An anonymized inmate stand-in seen from far behind, sitting alone on a bench in a walled prison exercise yard in flat winter light, one square of sky above him, a decade rendered as a courtyard, dignified and non-sensational, no face, no gore, no readable text [HSTYLE] Avoid: [HNEG]
- `S149.png`
Extreme close-up of institutional paint layers chipped on a steel bunk frame, years counted in coats of gray, macro texture in slate light, no people, no readable text [STYLE] Avoid: [NEG]
- `S150.png`
An anonymized woman stand-in seen only from behind, seated at a prison visiting-room window with one hand raised to the glass, an empty plastic chair reflected beside her, the family that keeps coming, cold fluorescent stillness, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

**★HP families_fight — 4 — S151–S154**（家族と支援者の机上の戦い・匿名）
```
- `S151.png`
Anonymized family hands sorting a kitchen table drifted deep with folders and envelopes rendered unreadable, a late lamp burning, the outside war of paperwork, cropped to hands and sleeves, no faces, no legible text [HSTYLE] Avoid: [HNEG]
- `S152.png`
An anonymized woman stand-in seen from behind at a kitchen window at night, one hand on a stack of case files, the years of writing letters nobody answers, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S153.png`
Anonymized hands sealing dozens of stamped envelopes fanned across a dark table, addresses rendered as smears, petitions going out again, warm lamp against slate gloom, no faces, no legible text [HSTYLE] Avoid: [HNEG]
- `S154.png`
An anonymized lawyer stand-in from behind at a desk stacked with bound transcripts, one desk lamp, the pro-bono decade, papers unreadable, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

**★HP fbi_revolt — 5 — S155–S159**（元FBIらの反乱・匿名・marble corridor of power）
```
- `S155.png`
A long marble government corridor with rows of anonymized suited figures seen only from behind walking toward tall doors, the professionals coming to object, cold institutional grandeur, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S156.png`
Anonymized older hands in a dark suit sleeve signing a letter rendered as an unreadable smear at a heavy desk, a career's authority spent on two smeared pages, macro, no face, no legible words [HSTYLE] Avoid: [HNEG]
- `S157.png`
Two dozen anonymized suited figures standing in loose ranks on marble steps seen from behind and below, retired authority assembled in gray light, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S158.png`
An anonymized hand placing a thick unreadable petition on a vast polished desk beneath a tall cold window, the ask laid before power, cropped to hand and document smear, no face, no legible text [HSTYLE] Avoid: [HNEG]
- `S159.png`
A row of anonymized silhouettes seated at a long hearing table seen from behind, microphones catching slate light, the system being asked to read its own file, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```

**★HP frontline_light — 3 — S160–S162**（全国区の光・doc クルー・匿名）
```
- `S160.png`
Anonymized documentary crew silhouettes behind a camera rig and a soft key light in a darkened room, an empty interview chair waiting in the glow, the country about to look, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S161.png`
An anonymized figure seen from behind seated in an interview chair under a single soft light, hands folded, about to say eleven hours out loud, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S162.png`
Anonymized press photographers as backs and raised cameras outside a brick courthouse in cold daylight, the story going national, no faces, no readable logos [HSTYLE] Avoid: [HNEG]
```

**conditional_halfdoor — 4 — S163–S166**（条件付き恩赦＝半開きの扉・gray のまま・★HP: S166 の1行＝夜明けに待つ家族・他3行は object）
```
- `S163.png`
A prison gate rolled exactly halfway open onto a flat gray dawn, neither shut nor free, cold slate light on wet asphalt, the conditional pardon as architecture, no people, no readable text [STYLE] Avoid: [NEG]
- `S164.png`
A heavy door standing open but with its chain lock still stretched taut across the gap, gray daylight through the slot, freedom with the accusation still attached, macro, no people, no readable text [STYLE] Avoid: [NEG]
- `S165.png`
An inked stamp pad and a government seal embosser on a dark desk beside an unreadable smeared document, mercy issued on paper that still says guilty, cold light, no legible text, no people [STYLE] Avoid: [NEG]
- `S166.png`
Anonymized family figures seen from behind waiting beside a parked car in a prison parking lot at gray dawn, sodium lamps still burning weakly against the light, the morning of a release that is not an exoneration, standing, group, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```

**★HP walk_out_2009 — 3 — S167–S169**（出所・ただし gray dawn・cream はまだ）
```
- `S167.png`
Three anonymized men seen only from behind walking out through a prison gate into flat gray dawn light, small duffels in hand, eleven years later, free but not cleared, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S168.png`
An anonymized man stand-in from behind stopping on wet asphalt outside a prison fence, head tilted up at open gray sky, the first unwalled morning, dignity and damage, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S169.png`
Anonymized family figures seen from behind embracing a just-released man at a chain-link gate in gray light, all backs and shoulders, joy with a condition attached, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```

**dna_truth_ignites — 3 — S170–S172**（S170 = also_thumb・ladder が cream へ点火。gel は S170 の1枚のみ〔点火＝最終状態変化・flood は M35 が担う〕・S171 は新規 distinct〔one name clean〕・S172 はタリーの状態変化〔cream に洗われ色あせ始める〕）
```
- `S170.png`
A DNA gel ladder igniting across a near-black frame, one lane blazing into warm letter-cream light while four lanes stand cold, clear, and empty, the whole case in one image, abstract, no readable numerals, no people [STYLE] Avoid: [NEG]
- `S171.png`
One of four worn court-record jackets withdrawn from a steel shelf rack and lying flat on the counter below, a clean gap of pale light where it stood, the first name coming clean, mixed slate and early cream, no legible labels, no people [STYLE] Avoid: [NEG]
- `S172.png`
The tally wall washed in rising cream light from off frame, four chalk strokes beginning to pale inside it, the count losing its power, no letters, no people, no readable text [STYLE] Avoid: [NEG]
```

**vacatur_2016 — 4 — S173–S176**（連邦地裁・actual innocence・★HP: S173–S174 の2行＝階段を上る弁護団/匿名 robed judge stand-in・実在判事に似せない・他2行は object）
```
- `S173.png`
A small group of anonymized lawyer stand-ins with briefcases seen from behind and below, climbing wide granite steps between a federal courthouse's towering columns in cold light, small figures against the architecture, the file finally being carried in, low angle, group, no faces, no readable inscription [HSTYLE] Avoid: [HNEG]
- `S174.png`
An anonymized robed judge stand-in seen only from behind at a dark wooden federal bench, bowed over a thick open file under one narrow shaft of warming light, the whole nineteen-year record finally being read, generic figure resembling no real judge, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S175.png`
A thick legal opinion lying open on dark wood, its lines rendered as unreadable smears, warm letter-cream light breaking across the pages from a tall window, the words that ended nineteen years, no legible characters, no people [STYLE] Avoid: [NEG]
- `S176.png`
A gavel at rest beside the smeared opinion in mixed slate and cream light, no strike needed, the quietest possible thunder, macro, no people, no readable text [STYLE] Avoid: [NEG]
```

**absolute_pardons_cream — 4 — S177–S180**（完全赦免＝cream flood・★HP: S177 の1行のみ＝four men from behind）
```
- `S177.png`
Four anonymized men seen only from behind, standing shoulder to shoulder before a pale classical capitol portico as the first warm cream of day breaks across its columns against a clearing slate sky, the state about to say the word innocent, all backs, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S178.png`
Waterfront sunrise over the Norfolk harbor, one broad band of letter-cream light laid across gray water toward camera, warships gone soft in haze, the morning the record was wiped, no people, no readable text [STYLE] Avoid: [NEG]
- `S179.png`
Four white Navy sailor caps on a dark table now washed in warm letter-cream window light, the four men as objects redeemed, shallow focus, no insignia readable, no people [STYLE] Avoid: [NEG]
- `S180.png`
A registry-style file drawer standing open and empty in warm cream light, its folders gone, the list that no longer carries their names, symbolic release, no people, no readable labels [STYLE] Avoid: [NEG]
```

**settlement_weight — 3 — S181–S183**（$8.4M・数字は絵に描かない・★HP: S181–S182 の2行＝小切手を書きに来た制度/静かな署名・S183 は object）
```
- `S181.png`
Two anonymized official stand-ins in dark overcoats seen from behind pushing through the heavy doors of a brick city-hall facade in flat morning light, shoulders squared, the institution arriving to finally write a check, standing, no faces, no readable signage [HSTYLE] Avoid: [HNEG]
- `S182.png`
An anonymized counsel's steady hand signing a settlement document rendered as an unreadable smear with a fountain pen, cream paper on dark leather in mixed slate and cream light, the calm mirror of a trembling signature made years ago under a bulb, money standing in for apology, no face, no legible characters [HSTYLE] Avoid: [HNEG]
- `S183.png`
An old brass balance scale with a small stack of paper on one pan and a pocket watch on the other, the pan with the watch sunk low, years outweighing money, dark backdrop, cream key light, no readable text, no people [STYLE] Avoid: [NEG]
```

**★HP ford_mirror — 6 — S184–S189**（badge → cuffs・権力の鏡像・匿名・record の範囲・★HP は S186–S187 の2行のみ＝他4行は object）
```
- `S184.png`
A pair of steel handcuffs open on a dark federal-courtroom table beside an evidence bag rendered unreadable, cold light, the instruments turned around, macro, no people, no readable text [STYLE] Avoid: [NEG]
- `S185.png`
A detective's badge laid face-down on a dark table at the edge of a hard white light cone, its shape unmistakable and its detail unreadable, authority set down for the last time, macro, no people, no readable text [STYLE] Avoid: [NEG]
- `S186.png`
An anonymized man in a suit seen only from behind at a federal defense table, shoulders squared the way he once squared suspects, the questioner now answering, cold light, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S187.png`
An anonymized figure seen from behind being escorted down a marble federal corridor by two suited silhouettes, the walk he had marched others through, all backs, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S188.png`
A federal prison's clean beige exterior under a wide flat sky, orderly fences and a distant gate, bureaucratic and pitiless, the destination of the interrogator, no people, no readable signage [STYLE] Avoid: [NEG]
- `S189.png`
A cell door closing along its track, caught in the final inches with a slate corridor light narrowing on the wall, the sound the four men knew by heart now made for him, no people, no readable text [STYLE] Avoid: [NEG]
```

**room_empty_final — 1 — S190**
```
- `S190.png`
The interrogation room with the bulb switched off, gray daylight leaking under the door across an empty table and one chair, the machine unplugged, quiet and spent, no people, no readable text [STYLE] Avoid: [NEG]
```

### ACT 5 — ENDING（15枚・S191–S205・the count resolved・strip to essentials）

**the_count_resolved — 4 — S191–S194**（タリーは S192/S194 の2枚〔拭われていく→1本だけ残る＝最終状態変化・洗い流しは M39 が担う〕・S191/S193 は同ビートの新規 distinct）
```
- `S191.png`
A small bunch of fresh flowers laid at the foot of a brick apartment building wall in soft morning light, dew on the paper wrapping, remembrance without spectacle, no people, no readable text [STYLE] Avoid: [NEG]
- `S192.png`
An anonymized hand with a damp cloth mid-wipe across chalk tally marks, the strokes dissolving into pale streaks, cropped to hand only, the false count coming off the wall, no face, no readable text [STYLE] Avoid: [NEG]
- `S193.png`
One worn pencil stub lying apart from a tight cluster of cheap ballpoint pens on dark wood, the one true instrument separated from the false, mixed slate and cream key light, still-life of the resolved count, no paper, no people, no readable text [STYLE] Avoid: [NEG]
- `S194.png`
The wall bare except for one remaining chalk stroke inside a soft cream glow, singular and quiet, the only confession that was ever true, no letters, no people, no readable text [STYLE] Avoid: [NEG]
```

**harbor_absolved — 4 — S195–S198**（harbor/caps は S195/S196 の2枚〔灰色だった港が cream で赦される＝S010/S016 からの状態変化〕・S197/S198 は同ビートの新規 distinct）
```
- `S195.png`
A wide Norfolk harbor sunrise, cream light flooding across calm water and softening the gray hulls, the town seen kindly for the first time, no people, no readable text [STYLE] Avoid: [NEG]
- `S196.png`
Four white Navy sailor caps set side by side on weathered pier planks in warm dawn light, the harbor breathing behind them, four names clean, no insignia readable, no people [STYLE] Avoid: [NEG]
- `S197.png`
A Navy seabag set down upright inside an open front door full of warm morning light, keys resting on top, the homecoming finally completed, quiet wide composition, no people, no readable text [STYLE] Avoid: [NEG]
- `S198.png`
A battered street-corner mail collection box on a quiet Norfolk sidewalk at dawn, its paint gone gray with age, one long band of cream light laid across it, the humble machine that carried the truth, no people, no readable text [STYLE] Avoid: [NEG]
```

**letter_kept — 3 — S199–S201**（手紙は S199/S201 の2枚〔擦り切れて保管＝最終状態→チョークと並ぶ全編の still-life〕・S200 は新規 distinct〔vigil の朝＝S111 からの状態変化〕）
```
- `S199.png`
The cream letter folded closed on dark wood, its creases worn soft with handling, kept as the exhibit that mattered, warm key light against slate shadow, no legible writing, no people [STYLE] Avoid: [NEG]
- `S200.png`
The apartment window at first light, the vigil candle burned down to a low steady stub on the sill, morning finally arriving on a long grief, quiet macro, no people, no readable text [STYLE] Avoid: [NEG]
- `S201.png`
The letter resting beside the piece of white chalk on a dark table, the two instruments of the count together at rest, still-life of the whole film, cream key light, no readable text, no people [STYLE] Avoid: [NEG]
```

**final_breath — 4 — S202–S205**
```
- `S202.png`
An empty room in plain gray daylight, a window without bars, a chair that is only a chair, ordinariness returned, quiet wide composition, no people, no readable text [STYLE] Avoid: [NEG]
- `S203.png`
The bare bulb hanging dark and dead in the abandoned interrogation room, daylight from the open door reaching it for the first time, power ended, no people, no readable text [STYLE] Avoid: [NEG]
- `S204.png`
A last look at the dark water of the harbor at first light, one long cream band widening on the horizon line, patient and clean, no people, no readable text [STYLE] Avoid: [NEG]
- `S205.png`
A near-black final frame with a single horizontal cream band of dawn over dark water, minimal and resolved, the closing underlay, no objects, no people, no text [STYLE] Avoid: [NEG]
```

## 5.7 幕別 motif 枚数の検算（★Codex は書き終えたら足して確認）

```
ACT0  : 4+4+4+3 = 15
ACT1  : 6+6+4+4+6+3+6+3+3+2+2 = 45
ACT2  : 6+4+6+6+4+5+4+6+4 = 45
ACT3  : 6+3+4+3+4+5+5+4+3+3 = 40
ACT4  : 5+4+5+3+4+3+3+4+4+3+6+1 = 45
ACT5  : 4+4+3+4 = 15
合計   : 15+45+45+40+45+15 = 205 ✓
★human-present(★HP) body: 21(ACT1: S016–S017, S020, S036–S046, S048–S049, S051–S054, S057)
                          +21(ACT2: S061, S064, S068, S071–S076, S088, S093, S096–S105)
                          +17(ACT3: S106, S112–S114, S122, S124, S128, S134, S136–S142, S144–S145)
                          +26(ACT4: S147–S148, S150–S162, S166–S169, S173–S174, S177, S181–S182, S186–S187) = 85 / 205 = 41.5%
（R3 検証済み55 → **R3+ owner directive 2026-07-26「人間が映った画像は結構必要」で object→★HP を30行転換＝85**。
 転換30行 = S016 S017 S020 S045 S046 S048 S049 S054 S057 / S061 S064 S068 S088 S093 S102 S103 S104 S105 /
 S106 S122 S124 S128 S134 S144 S145 / S147 S166 S173 S181 S182。[HSTYLE] 行の実数 = 21+21+17+26 = 85）
（残り120は object/symbolic。S120/S192 等の hands-only は「backs and hands and objects only」の範囲＝レーン表記は各行の [STYLE]/[HSTYLE] 記載が正）
```
> **S001..S205 の連番が穴なく205行**そろっていることを `--only S001` の `shots=250`（205 body + 42 i2v種 + 3 thumb_face）で確認する。**★HP 85枚は `[HSTYLE]`/`[HNEG]`、残り120枚は `[STYLE]`/`[NEG]` を全文連結。**

## 5.8 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_norfolk_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.9 パーサ契約（`read_prompts()` はこの2行形式しか読まない）

```
- `S001.png`
<positive prompt> Avoid: <negative>
```
- **1行目:** `` - `S001.png` ``（バッククォート囲み・行末は `.png` の直後）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト（`[STYLE]`/`[NEG]`/`[HSTYLE]`/`[HNEG]` は §5.3/§5.4/§5.11 の全文へ展開してから書く）
- `ai_prompts.v001.md` は **body 205行（S001..S205）＋ i2v 種 42行（M01_src..M42_src、§8.1a）＋ thumb_face 3行（T01_face..T03_face、§5.12）＝ 250 エントリ**を書く。すべて1枚生成。

## 5.10 生成コマンド（★variants 指定なし。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=250 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 53 --only S001
#   → ログ "episode=... shots=250 ... -> N images" の shots が 250 であること（205 body + 42 i2v種 + 3 thumb_face）

# 全250枚（body 205 + i2v種 42 + thumb_face 3・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-053-norfolk
```
> QC で落ちたシーンの再生成は `--only S###`（同じプロンプトで別シードを1枚）。**基準を下げない・水増ししない。**

## 5.11 ★人物画像（匿名・ドラマ化スタンドイン）— HUMAN-FIGURE prompts（★18本・i2v 種の内数）＋ ★HP body still の style

> **owner directive（EP48/49「空/寂しい・人がいない」却下を潰す）: 匿名・非識別の人物を増やす。** 実在人物（Williams/Dick/Tice/Wilson/Ford/Ballard/Michelle/Billy/両親/Taylor/判事/知事）の **likeness を作らない**。実在人物が示唆される所は顔を非識別（背向き/横顔を影に/逆光でシルエット化/目から下でクロップ/浅い被写界深度でソフト・**adults only**）。**被害者・レイプ・暴行・殺害・遺体を絶対に描かない（R-VICTIM 不変）。**
> **★この `[HSTYLE]`/`[HNEG]` は (a) 18本の i2v 人物種、(b) §5.6 の ★HP body still 85枚、の両方に使う。**

### ★lane 定義（人物は動かす＝紙芝居にしない → H は motion レーンへ・locked counts 不変）

**H001–H018 は「新規の静止カット」ではなく、既存 42本の i2v 種のうち 18本の中身（＝人物ビート）として作る。additive にしない。**
- **role = `i2v_source`**（body には回さない）。**42本の i2v 種のうち ★18本を人物ビート**に充て、残り **24本を抽象/象徴種**（§8.1a）。per-act の人物種 = **ACT1×5・ACT2×3・ACT3×3・ACT4×6・ACT5×1 ＝18**（§4.5 の M04/M06/M07/M09/M11・M14/M16/M18・M21/M22/M26・M30/M31/M32/M34/M36/M37・M40）。ACT0 は象徴のまま。
- **asset_id は既存の i2v 種 ID 空間（`^NOR-MS\d{2}$`）の 18本を占有**する（H001–H018 は本書内のラベル）。種画像ファイルは `M<NN>_src.png`。`public_path==null`。
- 各人物種は **Wan → RIFE（§8）で motion 化**され、**42本の motion のうち 18本**になり、**84 motion カットのうち最大 36カット**に出る＝**人物が動く**。
- **QC フラグ:** `has_human_body:true`（許可）・`has_identifiable_real_person:false`（必須）・`has_readable_text:false`（必須）・`has_victim_or_violence:false`（必須）。
- **★locked counts は1つも変わらない:** still_body **205**（object 120 ＋ ★HP 85）/ still_i2v_source **42**（抽象 24 ＋ 人物 18）/ motion **42** / factory **232** / overlay **30** / thumb_face **3**；cuts **220/232/84 = 536**。

**共通スタイル `[HSTYLE]`（各 H/★HP プロンプト末尾に全文連結・匿名/非識別/photoreal/harbor-slate）:**
```
, cinematic photoreal still, documentary reenactment stand-in, a generic anonymized person who resembles no real individual, face kept non-identifiable — turned away, in profile lost to shadow, back-lit to a silhouette, cropped below the eyes, or thrown soft in shallow focus, a cold harbor-slate blue-gray key light as the one recurring cool note, one bare interrogation bulb as a harsh blown-white cone where the beat is the room, near-black ink institutional gravity, low-key deep-shadow lighting, telephoto compression, shallow depth of field, restrained dignified framing, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no readable documents, a single warm letter-cream note only where the beat is the letter, the truth prevailing, or the finale
```
**共通ネガティブ `[HNEG]`（各 `Avoid:` の後に全文連結・匿名人体は許可、実在 likeness/被害者/暴行/可読テキストは禁止）:**
```
recognizable real person, likeness of a specific person, Danial Williams, Joseph Dick, Derek Tice, Eric Wilson, Robert Glenn Ford, Omar Ballard, Michelle Moore-Bosko, Billy Bosko, Tamika Taylor, any real judge or governor or prosecutor, celebrity, mugshot, deepfake, text, words, letters, numbers, captions, watermark, logo, readable document, legible confession, legible letter, legible report, legible date, license plate, the victim, murder victim, dead body, corpse, any depiction of the murder or the rape or an attack, violence, blood, gore, injury, knife, weapon, sexual content, nudity, crime scene, re-enactment of the attack, an identifiable child, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, saturated indigo evidence-blue, milky haze, scanline
```

### 人物ビート（★18本・全て匿名・非識別・実在 likeness なし・adults only・i2v 種として motion 化）
```
- `H001.png`  (= M04_src.png · ACT1 · Williams is walked in)
An anonymized young sailor stand-in in a plain t-shirt seen only from behind, being walked between two suited detectives down a dim police-station corridor toward a lit doorway, compliant and unknowing, cold fluorescent light, poised mid-stride, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H002.png`  (= M06_src.png · ACT1 · the lean-in)
An anonymized detective stand-in seen from behind leaning across a steel interrogation table into a harsh bulb cone, his shadow poised to swallow the slumped silhouette of a young man opposite, the instant before the next accusation, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H003.png`  (= M07_src.png · ACT1 · hour after hour)
An anonymized exhausted young man stand-in at the interrogation table, head sinking toward his hands so no face reads, shoulders poised at the point of collapse under the white cone, dignified and terrible, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H004.png`  (= M09_src.png · ACT1 · the signature)
Close on an anonymized trembling hand holding a cheap pen poised above the signature line of a typed page blurred into an unreadable smear, harsh bulb light, a life about to be signed away, hands only, no face, no legible words [HSTYLE] Avoid: [HNEG]
- `H005.png`  (= M11_src.png · ACT1 · the first tally)
An anonymized hand holding a stub of chalk poised against the dark interrogation-room wall, the first stroke just beginning, chalk dust waiting to fall, cropped to hand and sleeve, no face, no letters, no readable text [HSTYLE] Avoid: [HNEG]
- `H006.png`  (= M14_src.png · ACT2 · the next man)
An anonymized slight young sailor stand-in seen only from behind being led down a police corridor by two suited figures, poised at the threshold of the same lit room, the domino mid-fall, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H007.png`  (= M16_src.png · ACT2 · the second man in the chair)
An anonymized young man stand-in seen from behind seated small in the interrogation chair, hands flat on the steel table, the detective's silhouette poised at the cone's edge, the room beginning again, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H008.png`  (= M18_src.png · ACT2 · charges dropped)
Three anonymized sailor stand-ins seen from behind poised at the moment of stepping apart out of a lineup room's cold light toward a gray doorway, charges evaporating, all backs, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H009.png`  (= M21_src.png · ACT3 · the letter is written)
An anonymized inmate's hand gripping a pencil stub poised at the top of a sheet of cream paper on a steel cell shelf, the first stroke about to land, warm paper in slate gloom, cropped to hand and sleeve, no face, no legible words [HSTYLE] Avoid: [HNEG]
- `H010.png`  (= M22_src.png · ACT3 · the letter is mailed)
Anonymized hands holding a sealed cream envelope poised above the slot of a dented prison mail bin, the truth a centimeter from the system, cold institutional light, cropped to hands, no face, no legible address [HSTYLE] Avoid: [HNEG]
- `H011.png`  (= M26_src.png · ACT3 · the plea)
An anonymized young man stand-in seen from behind at a defense table, head poised at the top of a slow bow as a blade of cold courtroom light crosses his shoulders, the word guilty about to be spoken to survive, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H012.png`  (= M30_src.png · ACT4 · the professionals rise)
Rows of anonymized suited veteran figures seen from behind in a hearing room, poised mid-rise from their chairs in cold institutional light, decades of authority standing up against the file, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H013.png`  (= M31_src.png · ACT4 · the family's war)
Anonymized family hands poised over a kitchen table drifted with folders and stamped envelopes rendered unreadable, one hand mid-reach for the next petition, a late lamp burning, cropped to hands and sleeves, no faces, no legible text [HSTYLE] Avoid: [HNEG]
- `H014.png`  (= M32_src.png · ACT4 · the country looks)
Anonymized documentary-crew silhouettes poised behind a camera rig as a soft key light warms an empty interview chair, the red tally about to blink on, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H015.png`  (= M34_src.png · ACT4 · the walk out)
Three anonymized men seen only from behind poised at the first step through a half-open prison gate into flat gray dawn, duffels in hand, free but not yet cleared, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H016.png`  (= M36_src.png · ACT4 · the badge goes down)
An anonymized suited man's hands poised in the act of laying a badge face-down on a dark table at the edge of a hard white cone, authority a breath from surrendered, cropped to hands and dark sleeves, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H017.png`  (= M37_src.png · ACT4 · the interrogator's walk)
An anonymized figure seen from behind poised mid-step between two escorting silhouettes in a marble federal corridor, the walk he had marched others through now his own, all backs, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H018.png`  (= M40_src.png · ACT5 · four men, one pier)
Four anonymized men seen only from behind standing along a pier rail in warm letter-cream dawn light, white Navy caps held in their hands, poised in stillness before the open harbor, cleared and quiet, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
> **★H↔M 対応（§4.5 と一致・18本）:** H001=M04 · H002=M06 · H003=M07 · H004=M09 · H005=M11 · H006=M14 · H007=M16 · H008=M18 · H009=M21 · H010=M22 · H011=M26 · H012=M30 · H013=M31 · H014=M32 · H015=M34 · H016=M36 · H017=M37 · H018=M40。`ai_prompts.v001.md` では**新規行を足さず**、該当する 18本の `M<NN>_src.png` 行を上記の人物内容で書く（`shots=250` 維持）。§8.5 で目視確認（adults only・被害者/暴行なし・実在 likeness なし）。

## 5.12 ★サムネ用 emotive-face 静止画（3枚・thumb_face・CTR）

> **サムネは単一の AI 生成・非実在・illustrative/dramatized な顔**を peak emotion で。**実在人物（4人/Ford/Ballard 等）の likeness を作らない**＝clearly illustrative（semi-painterly, cinematic-render）にして「実在被告/刑事の実写」に読ませない＝likeness firewall。**被害者・子供の顔を作らない。** これらは**本編カットに出ない thumbnail 専用**（role=thumb_face・public_path null・distinct/cuts に数えない・§3.1）。B が `NorfolkThumbnails.tsx` で face＋2–4語 hook text を合成。

**共通スタイル `[TSTYLE]`:**
```
, thumbnail key art, a single non-real dramatized generic human character rendered in a clearly illustrative semi-painterly cinematic style so it never reads as a real photograph of a real person, face occupying 50 to 65 percent of frame height with eyes on the upper third, bright key light on the face and a rim light separating it from a dark desaturated blurred background of an interrogation room or a gray Navy harbor at dusk, skin warm, background cool harbor-slate, high contrast and vivid, one clean quadrant of negative space for text, 1280x720, ultra-detailed
```
**共通ネガティブ `[TNEG]`:**
```
photoreal photograph of a real person, likeness of Danial Williams or Joseph Dick or Derek Tice or Eric Wilson or Robert Glenn Ford or Omar Ballard or Michelle Moore-Bosko or any real sailor or detective or judge, recognizable real celebrity, deepfake, a child, the victim, murder victim, blood, gore, violence, knife, weapon, text, words, letters, numbers, watermark, logo, two faces, tiny face, neutral expression, dark muddy low-contrast mush, cartoon flatness, extra limbs, deformed, warped
```
```
- `T01_face.png`
A non-real dramatized generic young sailor's face in an illustrative cinematic style at peak emotion — hollow, sleep-starved, wrongly-accused dread gazing slightly off-camera under a harsh interrogation bulb, the look of a man being talked into a murder, pushed to the right third over a dark blurred interrogation-room background, hard white key light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
- `T02_face.png`
A non-real dramatized generic middle-aged detective archetype's face in an illustrative cinematic style with a cold, certain, immovable stare looking directly at the viewer, the interrogator who has already decided, pushed to the left third over a dark blurred one-way-mirror background, hard rim light, clean negative space on the right [TSTYLE] Avoid: [TNEG]
- `T03_face.png`
A non-real dramatized generic man's face in an illustrative cinematic style with stunned relief and one silent tear at the moment of absolute pardon, gray years dissolving in warm cream dawn light, pushed to the right third over a dark blurred harbor-sunrise background, clean negative space on the left [TSTYLE] Avoid: [TNEG]
```
> ★これら3枚は `role:"thumb_face"`・`public_path:null`・`has_human_body:true`・`has_identifiable_real_person:false`。§6 の目視で「実在 likeness でない・illustrative・被害者/子供なし」を確認。B のサムネ案はこの T01–T03 を前景に、§4.3a の also_thumb body（背景）＋ 2–4語 hook（例: ALL 4 CONFESSED / 0 WERE GUILTY）で組む。

## 5.13 ★EMOTIVE FACES — VISIBLE faces（EP52 §5.13 の owner 方針を継続・F シリーズ 12枚・additive）

生成済みセットの人物は背向き/影/手のみ。オーナー方針＝**見える感情的な顔**（顔は維持率・CTRを上げる）を織り込む。F-series（見える顔）を既存の匿名図に**加えて**生成する（distinct/cuts に数えない・B が採否判断）。

**2レーン、いずれも「実在の誰にも似せない・非実在の人物」：**
- **(a) generic-photoreal** — 特定の実在人物に紐づかない役（陪審員・傍聴人・記者・匿名の科学者/弁護士・退役捜査官）。
- **(b) dramatized-illustrative** — 中心的実在人物に隣接するビート（追い詰められる水兵・出所する男）は**明らかにイラスト調・半絵画的**で写真に見えないスタイル（実在人物の写真に絶対見えないように）。実在人物として名指し/キャプションしない。

**HARD BANS（不変）：** 4人/Ford/Ballard/Michelle/Billy/両親/Taylor/実在判事の**肖像を作らない**；被害者の描写・暴力・遺体なし；子供の顔なし；可読テキストなし。QCフラグ：`has_human_body:true`・`has_identifiable_real_person:false`・`has_identifiable_face:false`・`has_victim_or_violence:false`・`has_readable_text:false`。

**★ FACE（EP52 owner choice A 準拠）:** 顔は**LIGHT + EXPRESSION で目立たせ、サイズで目立たせない** — medium-close-up **顔は画面高の~30–45%**、目は上1/3、正面〜やや斜め、強い単一感情、暗く抑制された背景に劇的なキー＋リムライト。60%超の顔面アップ禁止・そむけ顔禁止・影に沈む顔禁止・hands-only 禁止。

`[FSTYLE]` = `a clearly-visible emotive human face in a strong medium-close-up filling ~30-45 percent of the frame, eyes on the upper third, front or slight three-quarter view looking near camera, one strong unmistakable {EXPRESSION}, dramatic key light plus rim light on the face against a dark moody background, restrained saturation, a generic anonymized non-real person resembling no real individual, cinematic documentary grade, cold harbor-slate with a single warm letter-cream note only where the beat is truth or release, ultra-detailed skin and eyes, high contrast, {photoreal | clearly illustrative semi-painterly non-photographic}, 16:9, adults only, no text, no watermark, no logo`
`[FNEG]` = `likeness of a real or named person, Danial Williams, Joseph Dick, Derek Tice, Eric Wilson, Robert Glenn Ford, Omar Ballard, Michelle, Bosko, recognizable real person, mugshot, deepfake, child, the victim, dead body, corpse, blood, injury, knife, weapon, violence, readable text, document, caption`

Files `F001.png … F012.png`. Act-mapped beats:
- **F001** (b · ACT1) an illustrative young-sailor everyman face at hour eleven — exhausted, hollow, breaking. NOT a Williams likeness.
- **F002** (a · ACT1) a detective archetype's hard, already-decided face across a table — generic, not Ford.
- **F003** (b · ACT2) a second illustrative sailor face — stunned disbelief at "you failed the polygraph." NOT a Dick likeness.
- **F004** (a · ACT2) jurors' uncertain faces in the box — a conviction on borrowed words.
- **F005** (b · ACT3) an illustrative face behind prison glass, years etched in — the wait. NOT a likeness.
- **F006** (a · ACT3) an anonymous prosecutor's unmoved face as a letter lies before him — the refusal, generic.
- **F007** (a · ACT4) a retired investigator's grave, resolved face — the professionals' revolt.
- **F008** (b · ACT4) an illustrative face at the half-open gate in gray dawn — relief withheld, conditional. NOT a likeness.
- **F009** (a · ACT3) the real attacker as a distant, cold, generic face mostly in shadow — NOT a Ballard likeness, no glorification.
- **F010** (a · ACT4) courtroom gallery faces at the innocence ruling — the exhale.
- **F011** (b · ACT4-5) an illustrative face in warm cream dawn at the absolute pardon — release. NOT a likeness.
- **F012** (a · ACT4) a federal judge archetype's grave face — generic, not Gibney.

Generate all 12; QC each visually (visible emotive face · non-real · no likeness/child/victim/text) before manifest.

---

# 6. A-2/A-3: 静止画のQC・目視（★depth map なし）

## 6.1 機械QC（body 205 + i2v種 42 + thumb_face 3 = 全250枚・`qc_norfolk_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `18.0<=mean_luma<=225.0`（near-black ink・低照度が多い→黒潰れ注意。cream ビートは白飛び注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**★反復規律（§0.1・2026-07-26）適用後の縮小 spine クラスタを重点監視（各行は状態変化つきの意図的再登場のみ・同ビート内最大2）: bulb/room(S005/S046–S047/S049/S060 ＋消灯状態の S190/S203)・tally(S001/S059/S083/S085/S192/S194 ＋cream に洗われる S172)・chairs(S080–S081)・gel(S063/S067/S126/S170)・letter(S107/S112–S114/S116/S120–S121/S199/S201)・harbor(S010/S016/S018/S195–S196)・prison(S106/S143–S144)。★HP figure クラスタも監視: police/interrogation figures(S045–S046/S049/S051–S053/S073–S075)・cell figures(S122/S124/S144–S145/S148)・courtroom gallery(S102–S105/S136–S142)・lab figures(S061/S064/S128)・pier/sailor/town figures(S016–S017/S020/S100)・waiting families(S102/S106/S113/S150/S166/S169)・hands CU(S048/S054/S057/S064/S068/S088/S098/S101/S112/S114/S134/S137/S151/S153/S156/S158/S182/S192)＝subject+composition+lighting が同じ2枚を出さない（§5.2 anti-samey）** | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・日付(1997/1999/2009/2016/2017)・年齢(18)・金額・住所・自白調書/手紙/新聞のロゴが写っていないか（**チョークのタリー線は文字ではない＝可。ただし線が文字に化けていないか見る**） | `has_readable_text=true`→reject |
| Q6 | **実在人物**の顔の混入 | **目視。** 実在人物として識別可能な顔（Williams/Dick/Tice/Wilson/Ford/Ballard/Michelle/Billy/Taylor/判事/知事に**似た**顔）が写っていないか。**匿名・非識別の顔（★HP/H/thumb_face/F）は OK。** | `has_identifiable_real_person=true`→reject |
| Q7 | 被害者/暴行/遺体/凶器 | **目視。** 被害者の描写・レイプ/暴行/殺害の再現・遺体・血・ナイフ/凶器・泣き叫ぶ女性が写っていないか。**★匿名の人体は OK（`has_human_body=true` 単独では reject しない）。** | あれば reject |

**Q5/Q6/Q7 は機械で判定しない。全250枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-053-norfolk --media image
#   → runs/qc/norfolk_footage_contact_NN.png（20枚/シート・約13シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-52 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** 特に **S032–S035/S094(apartment absence)に被害者/血/遺体が写らないこと、S054–S056(polygraph)/S107・S121・S199(手紙)/S175(判決文)に読める文字が無いこと、S001系のタリーが文字化けしていないこと、S122–S124(Ballard 影)/S052/S186–S187(detective 影)が実在 likeness に転じないこと、T01–T03/F001–F012 が illustrative で実在人物に似ていないこと、を必ず目で確認する。**

## 6.2 出力
```
episodes/PD-2026-053-norfolk/05_visuals/still_qc.v001.json     # 250枚全部の行（reject も残す）
```

## 6.3 accepted が (body205 / i2v42 / thumb3) に届かなかったとき
```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 53 --only S###   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_norfolk_stills.py
```
accepted body >= 205 かつ i2v_source >= 42 かつ thumb_face >= 3 になるまで繰り返す。**基準を下げない・水増ししない。**

## 6.4 ★depth map は生成しない（本作は depth treatment 不使用）
**DESIGN §1 の hard rule により footage/still treatment は `bleed`/`parallax`/`duotone`/`focus` のみ・`depth` を使わない**（depth displacement は被写体を melt/warp させる＝EP48/49 の warp 欠陥）。したがって **`gen_depth_maps.py` を回さない・`<stem>_depth.png` を作らない・マニフェストに `depth_path` を持たせない**（§4.1a/§4.2-19）。

---

# 7. A-4: factory 実写クリップ 232本の選定と全点目視QC

## 7.1 在庫の実態
```
H:\pd-media\assets\factory\   フラット構成（backgrounds 11,000本超・light_assets・particle_assets・vfx_overlays・texture_assets・loops）
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json（★必ず encoding="utf-8" で開く）
★棚のラベルは全面的に壊れている実績あり（evidence_bag=カートゥーン事故）。ラベルで選ばず、必ず目視で選ぶ。
```

## 7.2 選定条件
- **`kind=="video"` のみ。** 静止画 factory は使わない
- **232本ちょうど**（§3.3[3] still-share≤0.45 を守る設計値）
- **各1回しか使わない**（`MAX_USES_FACTORY=1`）
- 幕別割り当て（§4.4）: HOOK+OPENING=12 / ACT1=44 / ACT2=40 / ACT3=48 / ACT4=44 / ACT5=14 ＋ 繋ぎ=30 ＝ 232
- **EP39〜EP52 の絵柄を選ばない（§7.7 の分離語）。** EP53 は gray Navy harbor/warship/dockyard・1990s brick apartment（外観/廊下のみ）・police station/interrogation 系 institutional room・DNA lab・brick courthouse・prison exterior（非扇情）・mail/letter・federal courthouse/marble・Virginia capitol・harbor dawn。**被害者/暴行/泣く人/遺体/実在の顔が写るニュース映像を選ばない。ナイフ/凶器のクリップを選ばない。EP52 Texas 郊外/Texas capitol・EP47 two-lane road/pickup・EP41 sodium prison corridor・EP44 病院・EP49 Utah 駐車場を選ばない。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query naval_harbor --limit 60 --exclude-used --ep PD-2026-053-norfolk --json
```
`--exclude-used` は出荷ゲート `arc_nonrepeat` と同じ指紋集合を使う。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・§4.4 に pre-assign 済み）
> **★`covers_scene_id` は still 資産 ID 空間（S001..S205）を指す。** §4.4 の各エントリに pre-assign 済み（約30本が covers 付き、残りは null の繋ぎ/情景）。

| covers（例） | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S005/S009/S010 | interrogation room・harbor night・warship dawn | `dark_room_bulb` / `harbor_night` / `warship_silhouette` | 0 |
| S016/S022/S028/S036/S045 | naval harbor day・brick apartment・corridor・police lights・detective office | `naval_harbor` / `brick_apartment` / `apartment_corridor` / `police_lights_night` / `office_dim` | 1 |
| S061/S063/S071/S087/S102 | DNA lab・gel・police corridor・corkboard・brick courthouse | `dna_lab` / `gel_electrophoresis` / `police_corridor` / `corkboard_wall` / `brick_courthouse` | 2 |
| S106/S115/S119/S131/S136/S140/S143 | prison・mail room・desk lamp・vault・defense table・gavel・prison gate | `prison_exterior` / `mail_sorting` / `desk_lamp_paper` / `vault_door` / `courtroom` / `gavel` / `prison_gate` | 3 |
| S155/S160/S163/S167/S170/S173/S177/S181/S184/S185/S188/S189 | marble corridor・press・gray dawn・prison gate open・DNA modern・federal court・VA capitol・city hall・handcuffs・badge・federal prison・cell door | `marble_corridor` / `press_cameras` / `dawn_sky` / `prison_gate_open` / `dna_lab` / `federal_courthouse` / `virginia_capitol` / `city_hall` / `handcuffs` / `police_badge` / `federal_prison` / `cell_door` | 4 |
| S195/S196/S202/S205 | harbor sunrise・pier dawn・empty room daylight・sea horizon | `harbor_sunrise` / `pier_dawn` / `bright_empty_room` / `sea_horizon` | 5 |

**残りは covers を持たない繋ぎ・情景**（sky gradient・water reflection・brick texture・corridor・marble・file cabinets・fog harbor・gulls・rain glass・cityscape）。**暗いクリップに偏りすぎない**（暗側は約77本まで＝1/3・harbor 昼光・waterfront sunrise・daylight courtroom・lab の実用光を混ぜる）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）
```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.4a ★★★ 実写ストックライブラリを必ず使う（EP48/49 の burned lesson＝実写0本を潰す）★★★
- **ストックライブラリ:** `H:\pd-media\assets\stock`（マニフェスト `STOCK_MANIFEST.json`・動画74本＋静止155本・pexels/pixabay・商用可）。
- **調達方針（★counts は固定・factory 232 を変えない。レーン内の調達源を広げるだけ）:**
  1. `STOCK_MANIFEST.json` を読み、**意味（§7.3 の covers カテゴリ: harbor/apartment/lab/courthouse/prison/mail/capitol/dawn 等）に一致し §7.5 の全点目視 QC と R-FACE/R-VICTIM を通る実写動画を優先採用**。
  2. 残り枠を `H:\pd-media\assets\factory` 在庫で埋める。
  3. 各エントリの出所（`origin`: `stock` or `factory`）を `factory_selection.v001.json`（§7.6）と `stock_ledger.v001.json`（§10.2）に記録。
  4. **ストック静止155本は本編 body still（AI 205）レーンに混ぜない。**
- **★R-FACE/R-VICTIM を絶対順守:** 実在の判事/警官/水兵/被害者が写るニュース映像・被害者/暴行/遺体/gore・ナイフを含むクリップは**ストックでも使わない**。EP39〜52 との sha256 被りゼロ（§7.7）はストック由来にも適用。
- **★カラーマッチは B が担当:** pexels/pixabay の発色バラつきは B が harbor-slate `#56707F` の neutral グレードで AI still に合わせる（**milky wash にしない**）。

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★
> **実際に起きた事故（EP36 大聖堂・EP38 牛・factory 棚ラベル全面破損）。** `subtype` は「その検索語で取った」記録であって中身の保証ではない。**232本は分割して全点見る。**

**選抜232本は例外なく次を経る:**
```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-053-norfolk --media video --dir "<232本の staging フォルダ>"
```
1. コンタクトシートを開き **232本すべてを1本ずつ見る**
2. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて選定から外す（差替え）
3. 実写シネマティックB-roll・EP53テーマ・ウォーターマークなし・識別可能な実在人物なしを確認
4. **★制約2/3の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。**被害者/暴行/遺体/泣く人/gore・ナイフ・実在の顔が読めるニュース映像を使わない。**
5. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=42.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。**暗いクリップは約77本（1/3）までに抑える。**

## 7.6 出力
```
episodes/PD-2026-053-norfolk/05_stock/factory_selection.v001.json   # 選定理由・幕割り当て・origin
episodes/PD-2026-053-norfolk/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP52 との重複ゼロ（BLOCKING）
```bash
./.venv/Scripts/python.exe scripts/select_norfolk_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-052-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP53 の232本の積集合が**空**であることを確認。1件でも exit 1。**EP39〜EP52 のファイルは読むだけ。**

**分離レーン（色・素材・語）:** EP41 gold（監獄）／EP42 blue（ankle monitor）／EP43 amber／EP44 teal（病院）／EP45 crimson／EP46 green／EP47 civil-violet（Texas road/pickup）／EP48 glover／EP49 somber-plum（Utah）／EP50 steel-cyan／EP51 willingham／**EP52 evidence-blue #3F5E8C（Texas 郊外/courthouse/prison/lab/capitol）**。**EP53 = harbor-slate `#56707F`（INK `#0A0C0E`）＋ letter-cream `#E4D5A3`＋blown-white bulb＝大西洋の軍港・レンガ・郵便。** これら他話の絵柄・色・被写体を1本も選ばない（法廷/監獄/ラボは「レンガ・海・slate」の EP53 レーンで別物に見えること）。

---

# 8. A-5: i2v モーション化 42本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする42本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）
種画像は §5 と同じ `generate_sdxl_4k.py`（variants なし）で `M<NN>_src.png` として生成（`ai_prompts.v001.md` に §8.1a の42行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `NOR-MS01..MS42`、モーション成果物は `NOR-M01..M42`。**幕別配分は §4.5 に pre-assign 済み**（ACT0 3 / ACT1 8 / ACT2 9 / ACT3 8 / ACT4 10 / ACT5 4 = 42）。
> **★このうち ★18本は §5.11 の匿名人物ビート（H001–H018）＝42本の内数**（M04/M06/M07/M09/M11/M14/M16/M18/M21/M22/M26/M30/M31/M32/M34/M36/M37/M40）。**残り24本が抽象/象徴種（下記に全行 literal）。**

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの42行を追加・各1枚・**poised-still の source**＋ Wan モーションノート）
> 各種プロンプトは「動く直前の poised-still」。末尾に §5.3 `[STYLE]` ＋ `Avoid:` §5.4 `[NEG]`（人物種18本は §5.11 の H プロンプト全文＝`[HSTYLE]`/`[HNEG]`）を連結。**→Wan** はモーションノート（B のカット設計と §8.3 の positive に反映する意図）。

```
- `M01_src.png`
Five chalk tally marks on a dark interrogation-room wall under one bare bulb, the fifth stroke only half drawn and poised, chalk dust hanging motionless in the light cone, no letters, no people, no readable text [STYLE] Avoid: [NEG]
  →Wan: chalk dust drifts down through the cone; the half stroke seems to finish; light breathes.
- `M02_src.png`
A bare incandescent bulb on its cord over an empty steel table, poised at the top of a tiny swing, its blown-white cone tilted a degree off plumb, darkness around, no people, no readable text [STYLE] Avoid: [NEG]
  →Wan: the bulb swings slowly; the cone of light sweeps a few degrees; shadows lean.
- `M03_src.png`
Gray warship silhouettes on a Norfolk harbor horizon at first light, water surface poised glass-still, one gull hanging mid-air, no people, no readable text [STYLE] Avoid: [NEG]
  →Wan: slow drift of water ripples and the gull's glide; imperceptible push-in.
- `M04_src.png`  (= H001 · §5.11 の全文を使う)
  →Wan: the escorted figure takes two slow steps deeper toward the lit doorway; no face ever turns to camera.
- `M05_src.png`
An apartment front door standing slightly ajar into darkness at the end of a dim corridor, one cold blade of slate light poised across the floor, absolute stillness, nothing visible inside, no people, no readable text [STYLE] Avoid: [NEG]
  →Wan: the light blade lengthens almost imperceptibly; dust motes drift; the door never moves.
- `M06_src.png`  (= H002 · §5.11 の全文を使う)
  →Wan: the leaning silhouette presses a few centimeters closer; the seated shadow shrinks; bulb flickers once.
- `M07_src.png`  (= H003 · §5.11 の全文を使う)
  →Wan: the head sinks the last inch into the hands; shoulders tremble subtly; cone light steady.
- `M08_src.png`
A vintage polygraph needle poised at the top of a violent swing above rolling chart paper rendered as an unreadable smear, hard side light, menace in a machine, no legible characters, no people [STYLE] Avoid: [NEG]
  →Wan: the needle whips and scratches; the paper feeds; traces stay unreadable.
- `M09_src.png`  (= H004 · §5.11 の全文を使う)
  →Wan: the pen descends and drags one slow unreadable stroke; the hand trembles.
- `M10_src.png`
A round institutional wall clock high on a dark wall, hands and numerals blurred unreadable, poised as if between seconds, the bulb cone below, no legible numbers, no people [STYLE] Avoid: [NEG]
  →Wan: the blurred hands smear forward unnaturally fast; light crawls across the wall — eleven hours passing.
- `M11_src.png`  (= H005 · §5.11 の全文を使う)
  →Wan: the chalk bites the wall and pulls one full stroke; dust falls through the cone.
- `M12_src.png`
A gel-electrophoresis ladder glowing faint harbor-slate in darkness, bands poised half-resolved, one lane conspicuously empty, abstract, no readable numerals, no people [STYLE] Avoid: [NEG]
  →Wan: bands sharpen and rise like developing film; the empty lane stays empty — the exclusion.
- `M13_src.png`
A lab result sheet rendered as an unreadable smear poised at the lip of a manila folder on a dark desk, a deep file drawer open below, cold light, no legible characters, no people [STYLE] Avoid: [NEG]
  →Wan: the sheet slides into the folder and the drawer glides shut; darkness closes.
- `M14_src.png`  (= H006 · §5.11 の全文を使う)
  →Wan: the escorted figure crosses the threshold into the lit room; the door begins to close behind.
- `M15_src.png`
Two empty metal chairs under the interrogation bulb cone with the shadow of a third chair poised at the light's edge, stark symbolic staging, no people, no readable text [STYLE] Avoid: [NEG]
  →Wan: a third chair slides silently into the cone; shadows multiply — the theory grows.
- `M16_src.png`  (= H007 · §5.11 の全文を使う)
  →Wan: the detective's silhouette circles slowly behind the seated man; the room tightens.
- `M17_src.png`
A police corkboard of blank silhouette cards and taut red string, one new string poised half-stretched toward an empty corner, the web mid-growth, no legible text, no faces [STYLE] Avoid: [NEG]
  →Wan: the string pulls taut and two more cards shudder; the web spreads outward.
- `M18_src.png`  (= H008 · §5.11 の全文を使う)
  →Wan: the three figures step apart and walk out of the cold light toward the gray doorway.
- `M19_src.png`
Three tally strokes of chalk on near-black brick, a fourth just begun and frozen mid-line, loose powder hanging in the beam, the count still rising toward four false confessions, no letters, no people, no readable text [STYLE] Avoid: [NEG]
  →Wan: the fourth stroke completes; powder falls; the wall holds its silence.
- `M20_src.png`
A bare forensic examination table under one cold lamp with nothing on it, the lamp poised mid-flicker, symbolic emptiness about to be swept by light, no people, no readable text [STYLE] Avoid: [NEG]
  →Wan: the lamp's beam sweeps slowly across the empty surface and finds nothing.
- `M21_src.png`  (= H009 · §5.11 の全文を使う)
  →Wan: the pencil lands and writes one slow unreadable line across the cream page.
- `M22_src.png`  (= H010 · §5.11 の全文を使う)
  →Wan: the envelope drops through the slot; the bin swallows it; quiet.
- `M23_src.png`
A folded cream letter on a dark government desk poised at the first centimeter of unfolding, warm paper light against slate gloom, writing an unreadable smear, no people, no legible words [STYLE] Avoid: [NEG]
  →Wan: the letter unfolds petal-slow; cream light blooms across the desk.
- `M24_src.png`
The open cream letter in a desk lamp's circle with a dark stack of case files poised at frame edge, about to be pushed over it, cold office night, no people, no legible writing [STYLE] Avoid: [NEG]
  →Wan: the file stack slides across and buries the letter; the lamp circle goes empty.
- `M25_src.png`
A DNA gel ladder in a dark lab, one lane poised a breath away from snapping into a single bright aligned column, four neighboring lanes cold and empty, abstract, no numerals, no people [STYLE] Avoid: [NEG]
  →Wan: the lane snaps into alignment and flares — the only match the case ever had.
- `M26_src.png`  (= H011 · §5.11 の全文を使う)
  →Wan: the head completes its slow bow; the blade of light crosses the shoulders.
- `M27_src.png`
A massive institutional vault door, its wheel poised mid-turn, every bolt still seated, cold slate light on steel, frontal symmetry, no people, no readable text [STYLE] Avoid: [NEG]
  →Wan: the wheel turns a full revolution — and the bolts never move; motion without opening.
- `M28_src.png`
Four identical steel cell doors down a dark corridor, the nearest poised in the last inches of closing, slate light narrowing on the wall, no people, no readable numbers [STYLE] Avoid: [NEG]
  →Wan: the doors close in sequence, one after another, the light dying door by door.
- `M29_src.png`
A single cell window as a pale rectangle of winter light, poised at the first shift of color temperature, seasons stacked inside one aperture, no calendar, no person, no readable text [STYLE] Avoid: [NEG]
  →Wan: the light warms and cools across the rectangle — years crossing in seconds.
- `M30_src.png`  (= H012 · §5.11 の全文を使う)
  →Wan: the rows of suited figures rise together; authority standing up against the file.
- `M31_src.png`  (= H013 · §5.11 の全文を使う)
  →Wan: hands gather and square the envelopes; one more petition sealed.
- `M32_src.png`  (= H014 · §5.11 の全文を使う)
  →Wan: the key light blooms on; the empty interview chair warms; the crew silhouettes settle.
- `M33_src.png`
A prison gate poised rolled exactly halfway open onto flat gray dawn, wet asphalt reflecting slate light, neither shut nor free, no people, no readable text [STYLE] Avoid: [NEG]
  →Wan: the gate grinds a few more inches and stops short of open — the conditional pardon.
- `M34_src.png`  (= H015 · §5.11 の全文を使う)
  →Wan: the three men take their first slow steps through the gap into gray light.
- `M35_src.png`
A DNA gel ladder poised at ignition, one lane beginning to burn letter-cream while four lanes stand cold and clear, near-black frame, abstract, no numerals, no people [STYLE] Avoid: [NEG]
  →Wan: cream light floods outward from the burning lane and washes the frame — truth louder than the file.
- `M36_src.png`  (= H016 · §5.11 の全文を使う)
  →Wan: the badge is laid face-down; the hands withdraw into darkness.
- `M37_src.png`  (= H017 · §5.11 の全文を使う)
  →Wan: the escorted figure recedes down the marble corridor, step by step, smaller and smaller.
- `M38_src.png`
A thick legal opinion open on dark wood, lines rendered as unreadable smears, a tall window's warm cream light poised at the page's edge, no legible characters, no people [STYLE] Avoid: [NEG]
  →Wan: the cream light slides across the smeared pages like dawn crossing a floor.
- `M39_src.png`
The tally wall with four chalk strokes poised under a rising wash of warm light, a damp cloth's shadow entering frame, the false count about to come off, no letters, no people [STYLE] Avoid: [NEG]
  →Wan: four strokes dissolve into pale streaks; one sharp stroke remains.
- `M40_src.png`  (= H018 · §5.11 の全文を使う)
  →Wan: dawn light widens over the four still figures; a cap lifts slightly in the breeze; no one turns.
- `M41_src.png`
The cream letter poised at the last centimeter of being folded closed on dark wood, creases worn soft, warm key light, no legible writing, no people [STYLE] Avoid: [NEG]
  →Wan: the fold completes gently; the letter rests; light settles.
- `M42_src.png`
Dark harbor water at first light with one narrow letter-cream band poised on the horizon line, minimal and resolved, no objects, no people, no text [STYLE] Avoid: [NEG]
  →Wan: the cream band widens slowly across the water toward camera; the film exhales.
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_morton.py`（無ければ `comfy_wan_centralpark.py`）を下敷きにパスと SHOTS だけ差し替え）
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
STILL_DIR     = H:\pd-media\assets\ai\norfolk
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\norfolk
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, melting, text, watermark, identifiable face, real person likeness, child face, crying person, victim, corpse, assault, gore, blood, knife, weapon"
```
**ゲート:** `dry_validate`（length=5）/ `assert_loaded_completely` / `assert_frame_math`。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す・★42本は複数日）
```bash
py -3.11 scripts/comfy_wan_norfolk.py --build
py -3.11 scripts/comfy_wan_norfolk.py --run --shot M01
py -3.11 scripts/comfy_wan_norfolk.py --run-all
```
1本 24–73 GPU分・42本で 18–48時間。**夜間分割で回す。開始前にマシン状態を確認（heavy-job preflight）。A1111 と VRAM 競合＝`unload-checkpoint` で解放してから回す。**

## 8.4 RIFE で 48fps 化（`rife_norfolk.py`・`rife_morton.py`/`rife_centralpark.py` と同手順）
```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番 → RIFE 2x を2回（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. フレーム数検証 `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC
- **被害者・暴行・遺体・泣く人・gore・ナイフ**が生成されていないこと（必ず目視・制約2/3）
- モーフィング/ちらつき/ワープ/melt が無いこと → あれば別シードで再生成
- H シリーズ・detective/Ballard 影が**識別可能な実在 likeness**に転じていないこと
- gel ladder（M12/M25/M35）に**可読の数字**が出ていないこと／letter（M21–M24/M41）に**読める文字**が出ていないこと／tally（M01/M19/M39）が文字に化けていないこと
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（42本 × 2回 = 84カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど30本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **15本** | cold room dust・interrogation dust cone・archive/lab dust・harbor mist motes・chalk dust drift・paper fiber。黒背景 drift を screen 合成 |
| `light_assets` | **10本** | harbor-slate shaft・cold window bar・**bare-bulb harsh-white glow（L03/L10）**・**letter-cream edge（L05/L09＝ACT3 手紙と ACT4 後半〜ENDING のみ）** |
| `vfx_overlays` | **5本** | 微細な grain・cold light noise・slate glitch min |
| **合計** | **30本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/norfolk/overlay/` に置き、`norfolk_film.json` の `cuts[].src` には**出さない**。**★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない・周回する淡い光/scanline/CRT/vignette-wash を選ばない。** 黒背景でループするものを選び `blend_hint` を書く。他話色を選ばない（§7.7）。§7.5 の目視QC対象（30本）。

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_norfolk_assets.py`）
```
remotion/public/norfolk/img/     ← role=body の静止画205枚（★depth なし）
remotion/public/norfolk/factory/ ← 選定 factory .mp4 232本（§4.4 の F001..F232 名で）
remotion/public/norfolk/motion/  ← i2v M<NN>_rife.mp4 42本
remotion/public/norfolk/overlay/ ← 合成レイヤー 30本（§4.6 の P/L/V 名で）
remotion/public/norfolk/thumb/   ← thumb_face T01..T03（B の NorfolkThumbnails が参照）
```
- `public_path` はマニフェストの値（§4.4/§4.5/§4.6）と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）
- **★depth の同名ペアは作らない・置かない**（§6.4）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する）:**
- factory の `public_path` は必ず `norfolk/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も含めない
- 合成レイヤーは `norfolk/overlay/` に置き `cuts[].src` に出さない

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`
全静止画・i2v・factory・overlay・thumb_face を1行ずつ: `asset_id`/`path`/`source`(`ai_codex`|`factory`|`stock`)/`origin`/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力
```bash
./.venv/Scripts/python.exe scripts/build_norfolk_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_norfolk_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_norfolk_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**★factory 232 / motion 42 / overlay 30 が非空で実体化しているか（不変条件17/18/16）を必ず確認。**

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
EP53 の設計値: still 220/205=1.073(≤2) / factory 232/232=1.0(≤1) / motion 84/42=2.0(≤2) / first-use 479/536=0.8937(≥0.70) / avg-uses 536/479=1.119(≤1.4)。**全て達成可能。**

---

# 12. 絶対にやらないこと
- **EP39〜EP52 のファイル・素材に触らない。** 読み取りのみ可。素材・色・音のレーンも分離（§7.7）。EP53 の accent は **harbor-slate #56707F**（INK #0A0C0E・letter-cream #E4D5A3 は手紙/真実ビートのみ・A は絵で他話色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない**（`remotion/src/**` `scripts/ae/**` `scripts/build_norfolk_film.py` `manifest.json` `04_scenes/shotlist*` `figures`）。ただし `04_scenes/ai_prompts.v001.md` は A が書く。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness をどこにも作らない**（Williams/Dick/Tice/Wilson/Ford/Ballard/Michelle/Billy/両親/Taylor/判事/知事）。**匿名・非識別の一般人は可。被害者の描写・レイプ/暴行/遺体 imagery・ナイフ/凶器を一切作らない。**
- **制約に反する文言・絵を作らない**（§1.2/§1.3）: 4人の有罪化／被害者/暴行/遺体の描写／家族の悪役化／Ballard 美化/lurid／Ford の record 外の断定／hedged 数値の断定／可読の偽公文書（自白調書・手紙・判決文・新聞・赦免状）／実在人物 likeness／dochighlight／捏造/可読引用／milky wash/scanline。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。（factory の subtype `_02`/`_03` は別素材の意で別物・混同しない。）
- **role=thumb / still_thumb を作らない・overlay を30本以外にしない・thumb_face を3枚以外にしない。** also_thumb は body 4枚（§4.3a）。
- **★factory 232 / motion 42 / overlay 30 の配列を空・stub のまま出荷しない**（EP45/EP38 事故・§4.4/§4.5/§4.6 を実体化）。
- **★depth map を生成しない・`depth_path` を持たせない**（§6.4・DESIGN §1）。
- **★dochighlight figure を作らない・言及しない**（grep で 0）。
- **枚数を「だいたい」で決めない。** §3 の確定値（still 205 / factory 232 / i2v 42 / thumb_face 3 / distinct 479 / first-use 0.8937 / still-share 0.4104 / avg-uses 1.119 / overlay 30）と §3.3 の検算をそのまま使う。合わなければ本書を疑って報告。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** 生成物・在庫クリップを実際に見る。

---

# 13. 完了報告に含めるもの
```
1. accepted 静止画の枚数と内訳（body 205 [＝object 120 ＋ ★HP human-present 85 = 41.5%] / i2v_source 42 [＝抽象 24 ＋ ★人物 18] / thumb_face 3 / F-series 12 / also_thumb 4 [§4.3a] / reject N）
2. factory 選定 232本のリスト（asset_id / subtype / origin / eyeballed_content）と、subtype と食い違って外した本数、
   letter/gel/prison/apartment クリップの「no readable text / no logo / no face / no victim / no knife / no gore」確認、stock 由来の本数
3. EP39〜EP52（十四話）重複ゼロの確認結果
4. i2v 42本の frames / duration_sec と、SHORT? の有無、**★H001–H018（18本）の匿名・非識別・adults-only・no-victim 確認**、★HP body 85枚が匿名・非識別・実在 likeness なしの確認、★HP 85枚が §5.2 の anti-samey variety matrix（subject+composition+lighting の同一2枚なし）を満たす目視確認
5. 合成レイヤー30本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code）＋ factory 232/motion 42/overlay 30 が非空で実体化した確認 ＋ depth_path をどこにも生成していない確認
7. §3.3 の検算 [1]〜[8] を自分で再計算した結果（avg-uses/source 1.119≤1.4 を含む）
8. asset_manifest.v001.json の counts ブロック（still_body 205 / still_i2v_source 42 / motion 42 / factory 232 / overlay 30 / thumb_face 3）
9. 制約・1枚前提の自己申告（4人の有罪化なし・被害者/遺体/ナイフ graphic なし・家族の悪役化なし・Ballard 美化なし・
   hedged 数値の可読断定なし・実在の顔/likeness ゼロを目視確認・dochighlight 文字列ゼロ・捏造/可読引用なし・
   milky wash/scanline なし・depth なし・バリエーション0・A↔B同一スキーマ
   [schema norfolk_assets.v1 / role enum body|i2v_source|thumb_face|reject / counts / also_thumb 集合 4 / overlay 30 / thumb_face 3]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**








