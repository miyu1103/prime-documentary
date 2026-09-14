# EP54 flowers — Codex スレッドA「素材生成」引き継ぎプロンプト v001（30分・4幕・payoff 末尾積み上げ・numbers-thriller）

> ## ★★ 2026-07-26 更新 — 既に生成を始めている場合は必ず読む ★★
> 本書 §5.6 のプロンプトのうち **下記42枚は本日差し替え済み**（モチーフ反復排除37枚＋F顔差別化5枚・オーナー指示）。
> **旧プロンプトで生成済みでも、この42枚は `rejected/` へ退避してから新プロンプトで再生成すること**（「ファイルが有るからスキップ」禁止）。他のS番号は生成済みならそのまま有効。
> S002 S003 S004 S006 S008 S009 S011 S012 S015 S023 S026 S030 S031 S053 S063 S064 S066 S075 S076 S077 S080 S082 S083 S087 S093 S094 S104 S116 S124 S125 S163 S168 S197 S198 S199 S201 S202 ＋F顔: S109 S110 S153 S192 S193
> （新ルール §5.5a 必読。）

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN_ARCHITECTURE）も実装スレッドB（CODEX_B）も**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> ★30分尺。**「だいたい」で決めず §3 の確定値と §3.3 の検算をそのまま使う。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP54 / Episode ID: PD-2026-054-flowers / slug: flowers
Composition id: Ep54Flowers（B が Root.tsx に登録・A は staging まで）／1920x1080 / fps30 / 30:00
事件:       The Six Trials of Curtis Flowers（1996–2020・Mississippi）
            1996-07-16 朝、ミシシッピ州 Winona（人口約5,000・黒人と白人がほぼ半々の小さな町）の家具店
            Tardy Furniture で4人が射殺された: 店主 Bertha Tardy(59)・Carmen Rigby(45)・Robert Golden(42)・
            16歳の新人 Derrick "Bobo" Stewart（6日後に死亡）。凶器は未発見・目撃者なし・物証ほぼゼロ。
            地区検事 Doug Evans は、事件の約2週間前に店を解雇された黒人のゴスペル歌手 Curtis Flowers(26・
            前科なし)に即座に照準を合わせ、1997-01 に逮捕。以後 Evans は【同一人物を同じ事件で6回】起訴・
            訴追した。Trial1(1997 Tupelo・Tardy 単独訴因・全員白人陪審)＝死刑→2000 検察側不正行為で破棄。
            Trial2(1999 Gulf Coast・Stewart 単独訴因・白11黒1)＝死刑→2003 不正行為で再破棄。
            Trial3(2004 Winona・4訴因・白11黒1)＝死刑→2007 Batson違反（人種による陪審排除）で破棄
            （州最高裁「われわれが見た中で最も強力な人種差別の一応の証明」）。Trial4(2007・白7黒5)＝
            7対5で評決不能（人種線で分裂）。Trial5(2008・白9黒3)＝評決不能・唯一の無罪派 James Bibbs
            （黒人陪審員）が法廷で手錠・偽証罪で訴追→州司法長官が取り下げ。Trial6(2010-06・白11黒1)＝
            約30分の評議で有罪・4度目の死刑。
            州の「直接証拠」は獄中証言者 Odell "Cookie" Hallmon ただ一人（4つの trial で「Flowers が
            獄中で自白した」と証言）。Hallmon は 2016 年に3人（元交際相手 Marquita Hill・その母
            Carolyn Ann Sanders・Kenneth Loggins）を殺害し2週間後に有罪答弁＝終身刑。2018 年、
            APM のポッドキャスト In the Dark（Madeleine Baran ら・Winona に約1年）が事件を解体:
            ルート証言の崩壊・弾道学の過大証明・残渣1粒の無意味さ・そして陪審記録の集計＝Evans 管内
            225 trial・6,700人超・四半世紀で黒人候補を白人の約4.4倍の率で排除（黒人50% vs 白人11%）。
            Hallmon は録音された獄中通話で証言を撤回（「そんなこと一度も言ってない。あれは嘘だ」）。
            2019-06-21 連邦最高裁 Flowers v. Mississippi（7対2・Kavanaugh 法廷意見）が第6 trial を破棄:
            「6つの trial を通じ、州は行使し得た黒人陪審候補42人中41人を排除した」
            「陪審から黒人を排除しようとする執拗で断固たる（relentless, determined）努力」。
            2019-12-16 保釈（23年で初・$250,000・足首モニター）。2020-01 Evans が事件から recuse →
            州司法長官府へ。2020-09-04 全訴追取り下げ（with prejudice＝再訴不能）。
            2021-03 州の法定上限 $500,000（$50,000×10年・失われた23年の半分未満）の補償を裁判所が命令。
            2021-09 Flowers が Evans らを連邦提訴→2023 和解（条件非公開）。2022-11-29 Evans は
            巡回裁判官選挙の決選投票で 70%対30% の大差で敗北。2023-06-30 検事を退職（30年超）。
            2025-03 元 Wisconsin 弁護士懲戒当局トップが Evans の弁護士資格停止をミシシッピ州最高裁に
            請願＝**現在も未決着（結果を断定しない）**。Evans は刑事訴追も懲戒も一度も受けていない。
            ★★Tardy Furniture 事件は今も公式に未解決＝他に起訴された者はいない。
            ★主題は【6回の trial そのものが幕エンジン＝数字で語るスリラー。カウント（I–VI・41/42・
            7-5・70-30）が証言する】。
            ★Curtis Flowers は【存命・訴追は with prejudice で消滅・州が補償＝無実を事実として断定してよい】。
            ★★Doug Evans は【存命・刑事処罰なし】＝性格描写は最高裁/州最高裁/記録上の事実の引用のみ。
              資格停止請願は「未決着」以上を絶対に言わない・描かない。
            ★★被害者4人（16歳を含む）と Hallmon の被害者3人は【実在の殺害被害者】＝殺害・遺体・現場・
              暴力の描写を一切作らない。★★別の容疑者を示唆する画・語を一切作らない（存命・未起訴）。
            ★★人種が憲法上の核心＝数字で冷静に。実在人物（Flowers/Evans/Hallmon/被害者/陪審員 Bibbs/
              判事/記者/州司法長官/対立候補）の顔・肖像・likeness を一切作らない。匿名・非識別の一般人は可。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ・30分スケール）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**210本の固有プロンプト×1枚＝210枚**・バリエーション0） | `H:\pd-media\assets\ai\flowers\S<NNN>.png` | 5–8時間（GPU） |
| A-1b | i2v 種画像の生成（**44本の固有プロンプト×1枚＝44枚**・バリエーション0） | `H:\pd-media\assets\ai\flowers\M<NN>_src.png` | 1.5–2.5時間（GPU） |
| A-1c | サムネ用 emotive-face 静止画（**3枚**・CTR・非実在の illustrative face・§5.12） | `H:\pd-media\assets\ai\flowers\T<NN>_face.png` | 20分（GPU） |
| A-2 | 静止画のQCと目視（**全257枚を目視必須**＝210 body + 44 i2v種 + 3 thumb_face） | `05_visuals/still_qc.v001.json` + コンタクトシート | 2.5–4時間 |
| A-3 | ~~depth map~~ **不要（本作は depth treatment を使わない・§6.4）** | — | — |
| A-4 | factory 実写クリップ **236本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | 4–6時間（うち目視だけで2時間以上） |
| A-5 | i2v モーション化 **44本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\flowers\M<NN>_rife.mp4` | 18–50時間（GPU・**複数日**） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **30本** | `05_stock/overlay_selection.v001.json` | 1時間 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 30分 |
| A-8 | Remotion public への staging | `remotion/public/flowers/{img,factory,motion,overlay,thumb}/` | 40分 |

> **★★ 最重要の前提（EP42–52 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 210本＝210行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **variants 指定なし（＝1枚）** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 210 + i2v 種 44 + thumb_face 3 = 257枚（各1回）。** factory 236本は生成でなく在庫からの選抜。
> ★**`--only S001` のログで `shots=257` を確認**してから本番を回す（210 body + 44 i2v種 + 3 thumb_face = 257）。
> ★i2v 44本は**複数日GPU**。**開始前にマシン状態を確認**（heavy-job preflight）。夜間・分割で回す。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-054-flowers/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を **A(producer)とB(consumer/validator)で一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 236 エントリ、`motion` 配列は 44 エントリ、`overlay` 配列は 30 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5／§4.6 に全 236 + 44 + 30 を列挙済み。build スクリプトはこの列挙を消費するだけで、空配列を書かない）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\flowers\**` / `H:\pd-media\assets\ai_video\flowers\**` | **A** | 読み書き |
| `episodes/PD-2026-054-flowers/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-054-flowers/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/flowers/{img,factory,motion,overlay,thumb}/**` | **A** | 読み書き |
| `episodes/PD-2026-054-flowers/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_flowers_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-053-*/**` および EP39〜53 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を読む） | `PD-2026-054-flowers`（variants 指定なし） / `54 --only S001` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-054-flowers --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit N --exclude-used --ep PD-2026-054-flowers --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-054-flowers` |

> **★`gen_depth_maps.py` は使わない**（本作は depth treatment を使わない＝depth map 不要・§6.4／DESIGN §1「footage treatment は bleed/parallax/duotone/focus、depth 禁止」）。

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（実在確認してから・直近の `*morton*`(EP52) を優先、無ければ `*centralpark*`(EP50)） |
|---|---|---|
| `scripts/qc_flowers_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_morton_stills.py`（無ければ `qc_centralpark_stills.py`） |
| `scripts/select_flowers_factory.py` | §7 の factory 236本の確定選定・EP39〜53 sha256 除外検証 | `scripts/select_morton_factory.py`（無ければ `select_centralpark_factory.py`） |
| `scripts/comfy_wan_flowers.py` | §8 の i2v 44本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_morton.py`（実在確認） |
| `scripts/rife_flowers.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_morton.py`（実在確認） |
| `scripts/build_flowers_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_morton_asset_manifest.py` |
| `scripts/stage_flowers_assets.py` | §10 の staging | `scripts/stage_morton_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.9 の2行形式で書く**だけ（本書 §5.6/§5.11/§5.12/§8.1a の全行をそのまま転記）。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_flowers_facts.py`（B が clone して実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の制約に一致し、`check_flowers_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_flowers_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==236 / motion 配列長==44 / overlay 配列長==30 が非空で実体化していること（EP45 事故回避の必須不変条件）

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_flowers_asset_manifest.py --reuse-feasibility
#   → still >=210 / motion >=44 / factory >=236 / distinct 合計 >=490 / first-use >=0.70 / avg-uses/source <=1.4

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_flowers_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全236本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-054-flowers

# [A-DONE-5] EP39〜EP53 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_flowers_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39〜EP53 のすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（正確性制約・ガードレール）★★★

**Curtis Flowers は【存命・with prejudice で訴追消滅・州が誤収監の補償を命令】＝彼の無実を事実として断定してよい。Doug Evans は【存命・刑事処罰なし・懲戒なし】＝彼に関する全表現は連邦最高裁/州最高裁/記録上の出来事（3度の破棄・Batson・41/42・Bibbs 訴追・70対30の落選・退職・和解・未決着の資格請願）の範囲内のみ。内心の断定・記録外の侮辱・「処罰された/資格を失った」の示唆は BLOCKER。Odell Hallmon は【3人殺害で有罪・終身刑】＝記録どおり断定可・ただし美化も lurid も禁止・彼の被害者3人にも dignity。被害者4人（Bertha Tardy・Carmen Rigby・Robert Golden・16歳 Derrick Stewart）＝殺害・遺体・血・凶器・現場・再現を一切描かない。★別の容疑者を示唆する画・語を一切作らない（存命・未起訴＝「real killer」等の文字列も禁止）。陪審の数字（12-0/11-1/7-5/9-3/41/42/36/145対12/7対2/70対30）は台帳値のみ・画像には可読数字を描かない（数字は AE/figures＝B の担当）。捏造引用禁止・可読の偽公文書禁止。実在人物の顔・肖像・likeness ゼロ。匿名・非識別の一般人は可。**

## 1.1 R1/R2（生成ビジュアル全般）

1. **★R-FACE: 匿名・非識別の人物は可／実在人物の likeness は不可。** 匿名の一般人（実在の誰にも似せない・非識別のドラマ化スタンドイン）＝顔・身体を出してよい（§5.11 の H シリーズ・§5.13 の F シリーズ・§5.12 の thumb_face）。ただし **実在人物の顔・likeness・肖像は作らない**＝Curtis Flowers・Doug Evans・Odell Hallmon・Bertha Tardy・Carmen Rigby・Robert Golden・Derrick Stewart・Marquita Hill・Carolyn Ann Sanders・Kenneth Loggins・James Bibbs・Madeleine Baran・実在の判事/検事/州司法長官/対立候補/陪審員を**似せて描かない**。実在人物が示唆される所（被告・検事・証言者・陪審員等）は非識別（背向き/影/逆光/目から下でクロップ/ソフト/hands-only）を既定に保つ。**被害者7人の描写・暴行/殺害/遺体 imagery を一切作らない（不変）。16歳 Derrick Stewart は未成年＝識別可能な子供/少年の顔・「現場に残された少年の持ち物」プロップも作らない（象徴は「4脚の椅子・1脚だけ小さい」のみ）。**
2. **可読の偽公文書を再現しない。** 起訴状・判決文・陪審名簿・strike カード・新聞・弾道レポート・獄中通話記録・投票集計の**可読文字を再現しない**（雰囲気のみ・"blurred into an unreadable smear"）。日付（1996/1997/2010/2019/2020 等）・年齢（16/26/49）・金額（$30/$500,000）・比率（41/42・7-5・70-30）は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。
3. **被害者・暴行・殺害・現場・遺体を一切描かない。** 家具店は **storefront/interior of absence（無人・遺体なし・血なし・凶器なし・規制線クリシェなし）** のみ。Hallmon の事件も「3つの灯りが消える」象徴のみ。**Flowers が「歩いて店に向かう」画を作らない**（route は「州の再構成」として断片化・消去される抽象のみ＝R-FLOWERS-INNOCENT）。
4. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **R-FLOWERS-INNOCENT:** Flowers が犯人であるかのような絵・語を作らない。彼は **wrongfully imprisoned・fully cleared・innocent**。"flowers killed / the fired employee did it（断定）/ guilty flowers / flowers walking to the store with a gun" を書かない（"the state's theory / the prosecution claimed" の帰属枠は可）。
2. **R-VICTIM:** Tardy・Rigby・Golden・Stewart＋Hill・Sanders・Loggins に dignity。姿・likeness・遺体・暴行・血・凶器を描かない。"shot victims / bodies on the floor / murder scene / blood / the gun firing / crime scene tape" を書かない。storefront/interior of absence・4脚の椅子・3つの灯りのみ。
3. **R-CHILD-ADJ:** Derrick Stewart は16歳＝識別可能な未成年の顔・少年の私物プロップ（グローブ・帽子等）を作らない。「1脚だけ小さい椅子」の象徴のみ。
4. **R-EVANS-RECORD:** Evans は記録上の事実のみ。"evans punished / evans disbarred / evans lost his license / racist evans" を書かない（懲戒・処罰は起きていない。資格請願は "still open" のみ）。内心語（hate/racist heart 等）禁止。非識別 silhouette のみ。
5. **R-ALTSUSPECT:** **"real killer / actual killer / alternative suspect / the man who really did it / who actually killed" を全文字列で禁止。** 未解決は "officially unsolved / no one else was ever charged" のみ。銃の持ち主（実在・未起訴）の名前も書かない（"a parked car at the garment plant" まで）。
6. **R-JURYNUM:** 陪審・strike・票の数字は台帳値のみ（12-0/11-1/11-1/7-5/9-3/11-1・41/42・36/36・5/6・145対12・7対2・70対30）。それを**画像に可読で描かない**。"13 years on death row" を書かない（未検証＝"most of nearly 23 years"）。
7. **R-FACE:** **匿名・非識別の人物は可**（§5.11/§5.12/§5.13）。**実在人物の likeness ゼロ**＝"likeness of <Flowers/Evans/Hallmon/Tardy/Stewart/Bibbs/...> / face of <同> / recognizable real person / mugshot of a real person / deepfake" を書かない。
8. **R-READABLE:** 可読の偽公文書・名前カード・新聞・集計板を描かない。strike カードは "an unreadable smeared name card"。
9. **R-DOCHL:** **dochighlight（黒バー/box/underline の figure）を作らない・言及しない。** 全文字列 grep で 0。
10. **R-QUOTE:** 捏造引用禁止。verbatim は verified 6件（台帳 F17/F26/F32 系）のみ・attribution 付き（AE＝B の担当）。画像に可読の引用を描かない。

## 1.3 機械ゲート（`build_flowers_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
# 匿名・非識別の人物は許可。実在人物の likeness だけを弾く。
BANNED_PORTRAIT = re.compile(
    r"likeness of (a )?(real|specific|named) person|real[- ]person likeness|"
    r"face of (curtis|flowers|doug|evans|odell|hallmon|bertha|tardy|carmen|rigby|robert|golden|derrick|stewart|bibbs|baran|fitch|loper|lancaster|marquita|hill|sanders|loggins)|"
    r"likeness of (curtis|flowers|doug|evans|odell|hallmon|tardy|rigby|golden|stewart|bibbs|baran|hill|sanders|loggins)|"
    r"recognizable (real person|celebrity)|identifiable real person|"
    r"mugshot of (a )?real person|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"flowers (killed|did it|is guilty|murdered|shot)|the fired employee did it(?! \(the (state|prosecution|theory))|"
    r"guilty flowers|flowers walking to the store|"
    r"(shot|dead|slain) (victim|body|bodies|woman|man|boy)|murder scene|crime scene tape|blood on|corpse|the gun firing|"
    r"real killer|actual killer|alternative suspect|the man who really|who actually killed|"
    r"identifiable (child|minor|teenager)|boy'?s (glove|cap|belongings)|"
    r"evans (punished|disbarred|convicted|jailed)|lost his (law )?license|license (was )?suspended|racist evans|"
    r"(glorified|heroic|admirable) hallmon|lurid|"
    r"legible (document|indictment|jury list|strike card|newspaper|ballistics report|tally board)|readable (document|case file|report)|"
    r"13 years on death row|dochighlight",
    re.IGNORECASE)
```

> **許容:** "wrongfully imprisoned / fully cleared / innocent / tried six times by the same prosecutor / struck from the jury / hung jury / deadlocked along racial lines / the state's star witness recanted on a recorded call / convicted of three murders (Hallmon) / officially unsolved / no one else was ever charged / anonymous, non-identifiable person, face turned or in shadow / storefront of absence / four chairs one smaller / roman numeral counter"。禁止は「Flowers の有罪化」「被害者/暴行/遺体/現場の描写」「未成年の識別可能顔・私物プロップ」「Evans の処罰/資格喪失の示唆・内心断定」「別容疑者の示唆語」「陪審数字の捏造・可読描画」「可読の偽公文書」「実在人物 likeness」「dochighlight」。

---

# 2. 台本の語数と尺の確定値（Aが素材点数を積算する根拠）

```
words_total          = 4,688（LOCKED script・fact-locked・R1/R2/R3 済み）
narration_seconds    = 1579.3（= 26.32分 @178.1wpm・provisional・FINAL は measured TTS forced-align で上書き）
designed_pause_budget= 195.0（HOOK 打点・幕間 counter beat・earned breaths×3・QUOTE 着地・ending ambience）
body_seconds         = 1774.3（narration + pauses）
★HOOK-AUDIO 標準（owner・CODEX_B §5.1.2）: Brian の声が 0:00 から鳴る（silent runway なし）。
total_seconds        = 1783.3（body 1774.3 + endcard 9.0）= 29:43
durationInFrames     = 53,499（provisional・fps30 = ceil(1774.3*30)=53229 + 270・VO onset 0.0）
mean_shot            = 1774.3 / 554 = 3.203秒/カット
視覚 acts             = 4（+ HOOK/OPENING/ENDING は別区）
Act 語数配分（★2026-07-28 修正・voice_plan 実測）:
  HOOK 146 / OP 184 / ACT1 1,081 / ACT2 975 / ACT3 1,012 / ACT4 1,102 / ENDING 321 = 4,821
  （旧記載「実測: ACT1 ~1220 / ACT2 ~1180 / ACT3 ~1100 / ACT4 ~1120 + COLD/OPEN/ENDING ~1050」= 5,670 は
    "実測" と書いてあるが実測ではなく、本文 4,821語に対し +849語(+17.6%) 過大。全幕を過大評価しており、
    特に ACT2 は +205語。この表から素材密度を割り付けた箇所は再配分すること）
★TTS 実測（2026-07-28）: master 1,711.093s・speech 1,608.485s・313 chunks・179.8 wpm。
  designed_pause_budget 195.0 → 165.8 に吸収。total_seconds 1783.3 / durationInFrames 53,499 は不変（再ロック不要）。
```

**Aにとっての意味は1つ:** > **総カット 554 / distinct 490 / 初出 88.45% = still 210 + factory 236 + motion 44。**（§3 で積算）

> **注意（命名差）:** 視覚 act は **0=HOOK/OPENING, 1=ACT I, 2=ACT II, 3=ACT III, 4=ACT IV, 5=ENDING**（6値）。**still は 210 本の固有プロンプトを持つ**ため、still の資産 ID は **S001..S210**（1プロンプト＝1枚）。`covers_scene_id` は still 資産 ID 空間（S001..S210）を指す（§7.3）。

---

# 3. ★素材構成の確定値（この値で調達する・勝手に変えない）

## 3.1 内訳（★勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **210枚** | 230カット | 1.095回(≤2) | **210本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **236本** | 236カット | **各1回(1)** | 在庫11,000本超＋stock から選抜（§7）・全点目視・EP39〜53 と sha256 被りゼロ |
| **i2v モーション** | **44本** | 88カット | 各2回(≤2) | 44本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **490点** | **554カット** | | |
| 合成レイヤー（particle/light/vfx） | 30本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |
| サムネ emotive-face（thumb_face） | 3枚 | — | 本編カットに出ない | **distinct/cuts に数えない**（§5.12・thumbnail 専用） |

**SDXL の生成バッチ（本編カットに出ない i2v 種・thumb_face を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **210枚** | 210プロンプト × 1枚 |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **44枚** | 44種プロンプト × 1枚 |
| サムネ face（`role:"thumb_face"`・§5.12） | **3枚** | 3プロンプト × 1枚 |
| **SDXL 生成バッチ合計** | **210 + 44 + 3 = 257枚（各1回）** | **variants 指定なし（＝1枚）** |

> **本編サムネの背景 anchor は body 210枚から4枚を `also_thumb:true` で流用選抜**（§4.3a）。**emotive-face（前景の顔）は §5.12 の thumb_face 3枚**（B が `FlowersThumbnails.tsx` で face＋hook text を合成）。**role=thumb / still_thumb を作らない。**

## 3.2 幕別配分（★still は確定・factory/i2v は目安。合計だけが確定）

| 区間(act) | still（S番号・確定） | 内訳（object/★HP/★F） | factory（目安） | i2v（確定合計44） | thumb anchor |
|---|---|---|---|---|---|
| HOOK+OPENING (0) | **15**（S001–S015） | 15/0/0 | 12 | 3（M01–M03） | S001 |
| ACT1「The Crime and the Choosing」(1) | **45**（S016–S060） | 22/21/2 | 42 | 7（M04–M10） | S028 |
| ACT2「Trial, Reverse, Repeat」(2)（engine・最密） | **50**（S061–S110） | 23/24/3 | 45 | 9（M11–M19） | — |
| ACT3「The Hung Years and the Liar」(3) | **45**（S111–S155） | 25/17/3 | 45 | 11（M20–M30） | S117 |
| ACT4「The Ninth Inning」(4)（climax・cascade・最密②） | **40**（S156–S195） | 15/21/4 | 42 | 10（M31–M40） | S170 |
| ENDING (5) | **15**（S196–S210） | 13/2/0 | 15 | 4（M41–M44） | — |
| 繋ぎ（covers_scene_id:null・act 1〜4 に配分） | — | — | 35 | — | — |
| **合計** | **210** | **113/85/12** | **236** | **44** | **4** |

> **still の per-act 数（15/45/50/45/40/15＝210）は確定**（§5 の motif ライブラリがこの配分で組まれている）。ACT2（trial/reverse エンジン）が最厚50＋★HP 最多24、ACT4（numbers cascade）は climax で40＋★HP 21。**幕別の factory/i2v 内訳は目安値**（合計 236 / 44 のみ確定）。★人物3レーン（EP52 §5.13 の owner directive を本作はネイティブ実装）: **object/symbolic 113（[STYLE]/[NEG]）・★HP 匿名人物 85＝40%（[HSTYLE]/[HNEG]）・★F 可視の感情顔 12（[FSTYLE]/[FNEG]・非実在）**。
> **★R3+ owner directive 2026-07-26（「人間が映った画像は結構必要」・EP52 morton 前例と同型＝object→HP 転換のみ・additive しない・locked counts 不変）:** object 28行を ★HP に転換（HP 57→85）。転換行＝ACT1: S017/S018/S020/S021/S033/S034/S035/S045/S046/S047・ACT2: S062/S066/S068/S069/S071/S076/S078/S089・ACT3: S112/S114/S115/S118/S129・ACT4: S157/S158/S159・ACT5: S204/S206。**背骨 motif（tally strokes I–VI・strike cards・courthouse facade キーショット・four chairs・storefront of absence・also_thumb 4枚）は object のまま維持。** still 210 / i2v 44 / thumb 3 / factory 236 / overlay 30 / cuts 554 / §3.3 の検算はすべて不変。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 554 = still 230 + factory 236 + i2v 88
[2] 平均ショット長 = body 1774.3 / 554 = 3.203秒/カット  ✓ (≤7.0)
[3] 静止画占有率(check_animation_mix) = 230/554 = 41.52%  ✓ ≤45%（余裕 3.48%pt）
[4] motion coverage = (236+88)/554 = 324/554 = 58.48%     ✓ ≥45%
[5] per-asset 上限: still 230/210=1.095(≤2) / factory 236/236=1.0(≤1) / motion 88/44=2.0(≤2)  ✓
[6] first-use share = 490/554 = 0.8845                    ✓ ≥0.70
[7] avg uses/source = 554/490 = 1.131                     ✓ ≤1.4（EP49 は 1.8 で flag された）
[8] factory 下限 = 1774.3/30 = 59.1 → ≥60本。設計値 236本 ✓（still-share≤0.45 を守る）
```

> **[3] の余裕は 3.48%pt。** still が210本を割ったら §6.3 の再生成で回復させ、**still-cut 230 を増やさない**（B側の shotlist が230で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-054-flowers/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `flowers_assets.v1`（固定文字列）
**生産者:** `scripts/build_flowers_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を一字一致。** role enum は **`body | i2v_source | thumb_face | reject` のみ**。also_thumb は body still **ちょうど4枚**。thumb_face は **ちょうど3枚**。overlay は **ちょうど30本**。

## 4.1 スキーマ（`flowers_assets.v1`）

```jsonc
{
  "schema_version": "flowers_assets.v1",
  "episode_id": "PD-2026-054-flowers",
  "slug": "flowers",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_flowers_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 210,        // ==210
    "still_i2v_source": 44,   // ==44
    "motion": 44,             // ==44
    "factory": 236,           // ==236
    "overlay": 30,            // ==30（distinct 素材に数えない）
    "thumb_face": 3           // ==3（thumbnail 専用・distinct/cuts に数えない）
  },
  "stills":  [ /* §4.3: body 210 (FLW-S001..S210) + i2v_source 44 (FLW-MS01..MS44) + thumb_face 3 (FLW-T01..T03) */ ],
  "motion":  [ /* §4.5: FLW-M01..M44 全44本・public_path 必須（★非空） */ ],
  "factory": [ /* §4.4: 236本・public_path 必須（★非空・EP45事故回避の核心） */ ],
  "overlay": [ /* §4.6: 30本 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例・★depth_path なし）

```jsonc
{
  "asset_id": "FLW-S001",                 // body: ^FLW-S\d{3}$（001..210）/ i2v種: ^FLW-MS\d{2}$ / thumb: ^FLW-T\d{2}$
  "scene_id": "S001",                     // still 資産 ID 空間（§5.9 のプロンプト行に対応・S001..S210）
  "role": "body",                         // body|i2v_source|thumb_face|reject
  "also_thumb": false,                    // body から4枚だけ true（§4.3a・追加生成しない）
  "act": 0,                               // 0=HOOK/OPENING, 1..4=ACT I..IV, 5=ENDING
  "path": "H:/pd-media/assets/ai/flowers/S001.png",
  "public_path": "flowers/img/S001.png",  // role=="body" のみ非null / i2v種・thumb_face は null
  "width": 3840, "height": 2160,          // 長辺>=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 24.0,
  "tags": ["roman_numeral_counter","dust_gold","tally_scar","symbolic","no_face","no_readable_text"],
  "caption_hint": "a single dust-gold roman numeral seared into near-black like a tally scar, the first of six, abstract, no people, no readable text",
  "seed": 0, "model": "juggernautXL_ragnarokBy",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
         "has_identifiable_real_person": false, "has_human_body": false,
         "has_identifiable_face": false, "has_victim_or_violence": false, "notes": ""}
  // ★depth_path は無い（本作は depth treatment 不使用・§6.4）。
  // ★reject トリガは has_readable_text / has_identifiable_real_person / has_victim_or_violence のみ。
  //   匿名人体（has_human_body:true）は reject しない。★F シリーズは has_identifiable_face:false のまま
  //   （＝「実在人物として識別可能」ではない、の意。非実在の可視顔は可）。
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="flowers_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 210 / i2v_source 44 / motion 44 / factory 236 / overlay 30 / thumb_face 3）に**一致**
3. 全 `path`/`public_path` がディスクに実在（**depth_path は要求しない**）
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `public_path` が非null かつ実在。`role=="i2v_source"`/`role=="thumb_face"` は `public_path==null`
7. **★reject 条件:** `qc.has_readable_text==true` **または** `qc.has_identifiable_real_person==true` **または** `qc.has_victim_or_violence==true` は `role=="reject"`。**`qc.has_human_body==true` は reject 条件ではない**（匿名人体は可）。`qc.has_identifiable_face` は「実在人物として識別可能な顔」を意味する（匿名・非識別・非実在の顔は可）。H（§5.11）・F（§5.13）・thumb_face（§5.12）は `has_human_body:true`/`has_identifiable_real_person:false`/`has_readable_text:false`/`has_victim_or_violence:false`
8. `role=="i2v_source"` は `role=="body"`/`role=="thumb_face"` と**同一 asset_id を共有しない**（i2v_source は `^FLW-MS\d{2}$` / thumb_face は `^FLW-T\d{2}$`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39〜EP53 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど4**、かつ `scene_id` 集合が §4.3a の4枚集合と完全一致（**CODEX_B と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|thumb_face|reject のみ）
16. `overlay` 配列長が**ちょうど30**
17. ★**`factory` 配列長==236 かつ全エントリ `public_path` が非空**（EP45 事故回避）
18. ★**`motion` 配列長==44 かつ全エントリ `public_path` が非空**（同上）
19. **★どの still/motion にも `depth_path` キーを要求しない・生成しない**（depth treatment 不使用・§6.4）

`--reuse-feasibility` では §3.3 [5][6][7][8] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 210枚（S001..S210）= §5.6 の210プロンプトの生成物。各1枚。
2. i2v_source 44枚（MS01..MS44 / 種画像 M01_src..M44_src）= §8.1a の44種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. thumb_face 3枚（T01..T03 / T01_face..T03_face）= §5.12 の3プロンプトの生成物。public_path==null。
4. also_thumb : body のうち §4.3a の4枚に true（追加生成しない）
5. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

### 4.3a ★also_thumb 集合（ちょうど4枚・CODEX_B と一字一致必須）

```
{ FLW-S001 (the six dust-gold roman numerals accumulating in near-black — the hook signature),
  FLW-S028 (four straight-back chairs in warm light, one smaller — the victims held as dignity),
  FLW-S117 (a slate death-row cell window with seasons shifting — the 23-year anchor),
  FLW-S170 (the wall of struck, unreadable juror cards igniting dust-gold — the 41-of-42 hinge) }
```

> ★この4集合は §5 の該当 S番号に必ず該当 motif を置くこと（§5.6 で anchor 指定済み）。**前景の emotive face は §5.12 の thumb_face（T01–T03）＝これらは背景 anchor。**

## 4.4 ★`factory[]` 全236エントリ（★必ず実体化・public_path 非空。EP45事故回避の核心）

> `select_flowers_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id）/`path`（`H:/pd-media/assets/factory/...` or `H:/pd-media/assets/stock/...`）/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`origin`(`factory`|`stock`)/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。** 各 public_path は `flowers/factory/F0NN_<subtype>.mp4`。`type:"backgrounds"`, `kind:"video"`。**subtype の `_02`/`_03` は「同一検索テーマの別クリップ」の意で、別 sha256・別素材（同一ファイルの重複ではない）。**

```jsonc
// HOOK+OPENING (act 0) — 12
{ "public_path":"flowers/factory/F001_dim_records_storeroom.mp4", "act":0, "covers_scene_id":"S010", "subtype":"dim_records_storeroom" }
{ "public_path":"flowers/factory/F002_courthouse_archive_shelves.mp4", "act":0, "covers_scene_id":null, "subtype":"courthouse_archive_shelves" }
{ "public_path":"flowers/factory/F003_empty_jury_box_dim.mp4", "act":0, "covers_scene_id":"S007", "subtype":"empty_jury_box_dim" }
{ "public_path":"flowers/factory/F004_smalltown_mainstreet_night.mp4", "act":0, "covers_scene_id":null, "subtype":"smalltown_mainstreet_night" }
{ "public_path":"flowers/factory/F005_dust_motes_light_shaft.mp4", "act":0, "covers_scene_id":null, "subtype":"dust_motes_light_shaft" }
{ "public_path":"flowers/factory/F006_courtroom_dark_oak.mp4", "act":0, "covers_scene_id":null, "subtype":"courtroom_dark_oak" }
{ "public_path":"flowers/factory/F007_file_boxes_stacks_dim.mp4", "act":0, "covers_scene_id":null, "subtype":"file_boxes_stacks_dim" }
{ "public_path":"flowers/factory/F008_county_courthouse_night.mp4", "act":0, "covers_scene_id":null, "subtype":"county_courthouse_night" }
{ "public_path":"flowers/factory/F009_dim_records_storeroom_02.mp4", "act":0, "covers_scene_id":null, "subtype":"dim_records_storeroom_02" }
{ "public_path":"flowers/factory/F010_empty_jury_box_dim_02.mp4", "act":0, "covers_scene_id":null, "subtype":"empty_jury_box_dim_02" }
{ "public_path":"flowers/factory/F011_courthouse_archive_shelves_02.mp4", "act":0, "covers_scene_id":null, "subtype":"courthouse_archive_shelves_02" }
{ "public_path":"flowers/factory/F012_dust_motes_light_shaft_02.mp4", "act":0, "covers_scene_id":null, "subtype":"dust_motes_light_shaft_02" }
// ACT1 The Crime and the Choosing (act 1) — 42
{ "public_path":"flowers/factory/F013_mississippi_mainstreet_1996_day.mp4", "act":1, "covers_scene_id":"S016", "subtype":"mississippi_mainstreet_1996_day" }
{ "public_path":"flowers/factory/F014_brick_storefront_smalltown.mp4", "act":1, "covers_scene_id":"S022", "subtype":"brick_storefront_smalltown" }
{ "public_path":"flowers/factory/F015_furniture_store_interior_empty.mp4", "act":1, "covers_scene_id":"S023", "subtype":"furniture_store_interior_empty" }
{ "public_path":"flowers/factory/F016_southern_church_exterior_day.mp4", "act":1, "covers_scene_id":"S032", "subtype":"southern_church_exterior_day" }
{ "public_path":"flowers/factory/F017_church_pews_light_shafts.mp4", "act":1, "covers_scene_id":"S033", "subtype":"church_pews_light_shafts" }
{ "public_path":"flowers/factory/F018_cotton_field_dawn_wide.mp4", "act":1, "covers_scene_id":null, "subtype":"cotton_field_dawn_wide" }
{ "public_path":"flowers/factory/F019_dirt_road_heat_haze.mp4", "act":1, "covers_scene_id":"S040", "subtype":"dirt_road_heat_haze" }
{ "public_path":"flowers/factory/F020_garment_plant_parking_distant.mp4", "act":1, "covers_scene_id":"S043", "subtype":"garment_plant_parking_distant" }
{ "public_path":"flowers/factory/F021_railroad_tracks_divide_town.mp4", "act":1, "covers_scene_id":"S044", "subtype":"railroad_tracks_divide_town" }
{ "public_path":"flowers/factory/F022_smalltown_police_station.mp4", "act":1, "covers_scene_id":null, "subtype":"smalltown_police_station" }
{ "public_path":"flowers/factory/F023_patrol_car_night_lights.mp4", "act":1, "covers_scene_id":null, "subtype":"patrol_car_night_lights" }
{ "public_path":"flowers/factory/F024_jail_corridor_dim.mp4", "act":1, "covers_scene_id":"S056", "subtype":"jail_corridor_dim" }
{ "public_path":"flowers/factory/F025_water_tower_smalltown.mp4", "act":1, "covers_scene_id":null, "subtype":"water_tower_smalltown" }
{ "public_path":"flowers/factory/F026_front_porch_summer_dusk.mp4", "act":1, "covers_scene_id":null, "subtype":"front_porch_summer_dusk" }
{ "public_path":"flowers/factory/F027_mississippi_mainstreet_1996_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"mississippi_mainstreet_1996_day_02" }
{ "public_path":"flowers/factory/F028_brick_storefront_smalltown_02.mp4", "act":1, "covers_scene_id":null, "subtype":"brick_storefront_smalltown_02" }
{ "public_path":"flowers/factory/F029_furniture_store_interior_empty_02.mp4", "act":1, "covers_scene_id":null, "subtype":"furniture_store_interior_empty_02" }
{ "public_path":"flowers/factory/F030_southern_church_exterior_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"southern_church_exterior_day_02" }
{ "public_path":"flowers/factory/F031_church_pews_light_shafts_02.mp4", "act":1, "covers_scene_id":null, "subtype":"church_pews_light_shafts_02" }
{ "public_path":"flowers/factory/F032_cotton_field_dawn_wide_02.mp4", "act":1, "covers_scene_id":null, "subtype":"cotton_field_dawn_wide_02" }
{ "public_path":"flowers/factory/F033_dirt_road_heat_haze_02.mp4", "act":1, "covers_scene_id":null, "subtype":"dirt_road_heat_haze_02" }
{ "public_path":"flowers/factory/F034_garment_plant_parking_distant_02.mp4", "act":1, "covers_scene_id":null, "subtype":"garment_plant_parking_distant_02" }
{ "public_path":"flowers/factory/F035_railroad_tracks_divide_town_02.mp4", "act":1, "covers_scene_id":null, "subtype":"railroad_tracks_divide_town_02" }
{ "public_path":"flowers/factory/F036_smalltown_police_station_02.mp4", "act":1, "covers_scene_id":null, "subtype":"smalltown_police_station_02" }
{ "public_path":"flowers/factory/F037_patrol_car_night_lights_02.mp4", "act":1, "covers_scene_id":null, "subtype":"patrol_car_night_lights_02" }
{ "public_path":"flowers/factory/F038_jail_corridor_dim_02.mp4", "act":1, "covers_scene_id":null, "subtype":"jail_corridor_dim_02" }
{ "public_path":"flowers/factory/F039_water_tower_smalltown_02.mp4", "act":1, "covers_scene_id":null, "subtype":"water_tower_smalltown_02" }
{ "public_path":"flowers/factory/F040_front_porch_summer_dusk_02.mp4", "act":1, "covers_scene_id":null, "subtype":"front_porch_summer_dusk_02" }
{ "public_path":"flowers/factory/F041_mississippi_mainstreet_1996_day_03.mp4", "act":1, "covers_scene_id":null, "subtype":"mississippi_mainstreet_1996_day_03" }
{ "public_path":"flowers/factory/F042_brick_storefront_smalltown_03.mp4", "act":1, "covers_scene_id":null, "subtype":"brick_storefront_smalltown_03" }
{ "public_path":"flowers/factory/F043_furniture_store_interior_empty_03.mp4", "act":1, "covers_scene_id":null, "subtype":"furniture_store_interior_empty_03" }
{ "public_path":"flowers/factory/F044_southern_church_exterior_day_03.mp4", "act":1, "covers_scene_id":null, "subtype":"southern_church_exterior_day_03" }
{ "public_path":"flowers/factory/F045_church_pews_light_shafts_03.mp4", "act":1, "covers_scene_id":null, "subtype":"church_pews_light_shafts_03" }
{ "public_path":"flowers/factory/F046_cotton_field_dawn_wide_03.mp4", "act":1, "covers_scene_id":null, "subtype":"cotton_field_dawn_wide_03" }
{ "public_path":"flowers/factory/F047_dirt_road_heat_haze_03.mp4", "act":1, "covers_scene_id":null, "subtype":"dirt_road_heat_haze_03" }
{ "public_path":"flowers/factory/F048_garment_plant_parking_distant_03.mp4", "act":1, "covers_scene_id":null, "subtype":"garment_plant_parking_distant_03" }
{ "public_path":"flowers/factory/F049_railroad_tracks_divide_town_03.mp4", "act":1, "covers_scene_id":null, "subtype":"railroad_tracks_divide_town_03" }
{ "public_path":"flowers/factory/F050_smalltown_police_station_03.mp4", "act":1, "covers_scene_id":null, "subtype":"smalltown_police_station_03" }
{ "public_path":"flowers/factory/F051_patrol_car_night_lights_03.mp4", "act":1, "covers_scene_id":null, "subtype":"patrol_car_night_lights_03" }
{ "public_path":"flowers/factory/F052_jail_corridor_dim_03.mp4", "act":1, "covers_scene_id":null, "subtype":"jail_corridor_dim_03" }
{ "public_path":"flowers/factory/F053_water_tower_smalltown_03.mp4", "act":1, "covers_scene_id":null, "subtype":"water_tower_smalltown_03" }
{ "public_path":"flowers/factory/F054_front_porch_summer_dusk_03.mp4", "act":1, "covers_scene_id":null, "subtype":"front_porch_summer_dusk_03" }
// ACT2 Trial, Reverse, Repeat (act 2) — 45
{ "public_path":"flowers/factory/F055_county_courthouse_columns.mp4", "act":2, "covers_scene_id":"S061", "subtype":"county_courthouse_columns" }
{ "public_path":"flowers/factory/F056_courthouse_steps_wide.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_steps_wide" }
{ "public_path":"flowers/factory/F057_empty_courtroom_oak.mp4", "act":2, "covers_scene_id":"S067", "subtype":"empty_courtroom_oak" }
{ "public_path":"flowers/factory/F058_jury_box_empty_oak.mp4", "act":2, "covers_scene_id":"S073", "subtype":"jury_box_empty_oak" }
{ "public_path":"flowers/factory/F059_witness_stand_empty.mp4", "act":2, "covers_scene_id":null, "subtype":"witness_stand_empty" }
{ "public_path":"flowers/factory/F060_judge_bench_empty_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"judge_bench_empty_dim" }
{ "public_path":"flowers/factory/F061_law_books_shelf.mp4", "act":2, "covers_scene_id":null, "subtype":"law_books_shelf" }
{ "public_path":"flowers/factory/F062_marble_hallway_courthouse.mp4", "act":2, "covers_scene_id":null, "subtype":"marble_hallway_courthouse" }
{ "public_path":"flowers/factory/F063_appellate_court_facade.mp4", "act":2, "covers_scene_id":"S101", "subtype":"appellate_court_facade" }
{ "public_path":"flowers/factory/F064_court_records_room_shelves.mp4", "act":2, "covers_scene_id":"S088", "subtype":"court_records_room_shelves" }
{ "public_path":"flowers/factory/F065_docket_ledgers_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"docket_ledgers_dim" }
{ "public_path":"flowers/factory/F066_courtroom_doors_oak.mp4", "act":2, "covers_scene_id":null, "subtype":"courtroom_doors_oak" }
{ "public_path":"flowers/factory/F067_courthouse_clock_tower.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_clock_tower" }
{ "public_path":"flowers/factory/F068_gallery_benches_empty.mp4", "act":2, "covers_scene_id":null, "subtype":"gallery_benches_empty" }
{ "public_path":"flowers/factory/F069_courthouse_lawn_day.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_lawn_day" }
{ "public_path":"flowers/factory/F070_county_courthouse_columns_02.mp4", "act":2, "covers_scene_id":null, "subtype":"county_courthouse_columns_02" }
{ "public_path":"flowers/factory/F071_courthouse_steps_wide_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_steps_wide_02" }
{ "public_path":"flowers/factory/F072_empty_courtroom_oak_02.mp4", "act":2, "covers_scene_id":null, "subtype":"empty_courtroom_oak_02" }
{ "public_path":"flowers/factory/F073_jury_box_empty_oak_02.mp4", "act":2, "covers_scene_id":null, "subtype":"jury_box_empty_oak_02" }
{ "public_path":"flowers/factory/F074_witness_stand_empty_02.mp4", "act":2, "covers_scene_id":null, "subtype":"witness_stand_empty_02" }
{ "public_path":"flowers/factory/F075_judge_bench_empty_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"judge_bench_empty_dim_02" }
{ "public_path":"flowers/factory/F076_law_books_shelf_02.mp4", "act":2, "covers_scene_id":null, "subtype":"law_books_shelf_02" }
{ "public_path":"flowers/factory/F077_marble_hallway_courthouse_02.mp4", "act":2, "covers_scene_id":null, "subtype":"marble_hallway_courthouse_02" }
{ "public_path":"flowers/factory/F078_appellate_court_facade_02.mp4", "act":2, "covers_scene_id":null, "subtype":"appellate_court_facade_02" }
{ "public_path":"flowers/factory/F079_court_records_room_shelves_02.mp4", "act":2, "covers_scene_id":null, "subtype":"court_records_room_shelves_02" }
{ "public_path":"flowers/factory/F080_docket_ledgers_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"docket_ledgers_dim_02" }
{ "public_path":"flowers/factory/F081_courtroom_doors_oak_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courtroom_doors_oak_02" }
{ "public_path":"flowers/factory/F082_courthouse_clock_tower_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_clock_tower_02" }
{ "public_path":"flowers/factory/F083_gallery_benches_empty_02.mp4", "act":2, "covers_scene_id":null, "subtype":"gallery_benches_empty_02" }
{ "public_path":"flowers/factory/F084_courthouse_lawn_day_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_lawn_day_02" }
{ "public_path":"flowers/factory/F085_county_courthouse_columns_03.mp4", "act":2, "covers_scene_id":null, "subtype":"county_courthouse_columns_03" }
{ "public_path":"flowers/factory/F086_courthouse_steps_wide_03.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_steps_wide_03" }
{ "public_path":"flowers/factory/F087_empty_courtroom_oak_03.mp4", "act":2, "covers_scene_id":null, "subtype":"empty_courtroom_oak_03" }
{ "public_path":"flowers/factory/F088_jury_box_empty_oak_03.mp4", "act":2, "covers_scene_id":null, "subtype":"jury_box_empty_oak_03" }
{ "public_path":"flowers/factory/F089_witness_stand_empty_03.mp4", "act":2, "covers_scene_id":null, "subtype":"witness_stand_empty_03" }
{ "public_path":"flowers/factory/F090_judge_bench_empty_dim_03.mp4", "act":2, "covers_scene_id":null, "subtype":"judge_bench_empty_dim_03" }
{ "public_path":"flowers/factory/F091_law_books_shelf_03.mp4", "act":2, "covers_scene_id":null, "subtype":"law_books_shelf_03" }
{ "public_path":"flowers/factory/F092_marble_hallway_courthouse_03.mp4", "act":2, "covers_scene_id":null, "subtype":"marble_hallway_courthouse_03" }
{ "public_path":"flowers/factory/F093_appellate_court_facade_03.mp4", "act":2, "covers_scene_id":null, "subtype":"appellate_court_facade_03" }
{ "public_path":"flowers/factory/F094_court_records_room_shelves_03.mp4", "act":2, "covers_scene_id":null, "subtype":"court_records_room_shelves_03" }
{ "public_path":"flowers/factory/F095_docket_ledgers_dim_03.mp4", "act":2, "covers_scene_id":null, "subtype":"docket_ledgers_dim_03" }
{ "public_path":"flowers/factory/F096_courtroom_doors_oak_03.mp4", "act":2, "covers_scene_id":null, "subtype":"courtroom_doors_oak_03" }
{ "public_path":"flowers/factory/F097_courthouse_clock_tower_03.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_clock_tower_03" }
{ "public_path":"flowers/factory/F098_gallery_benches_empty_03.mp4", "act":2, "covers_scene_id":null, "subtype":"gallery_benches_empty_03" }
{ "public_path":"flowers/factory/F099_courthouse_lawn_day_03.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_lawn_day_03" }
// ACT3 The Hung Years and the Liar (act 3) — 45
{ "public_path":"flowers/factory/F100_prison_exterior_farmland_flat.mp4", "act":3, "covers_scene_id":"S111", "subtype":"prison_exterior_farmland_flat" }
{ "public_path":"flowers/factory/F101_razor_wire_fence_distant.mp4", "act":3, "covers_scene_id":null, "subtype":"razor_wire_fence_distant" }
{ "public_path":"flowers/factory/F102_cell_block_window_light.mp4", "act":3, "covers_scene_id":"S113", "subtype":"cell_block_window_light" }
{ "public_path":"flowers/factory/F103_long_prison_corridor.mp4", "act":3, "covers_scene_id":null, "subtype":"long_prison_corridor" }
{ "public_path":"flowers/factory/F104_prison_yard_empty_nonsensational.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_yard_empty_nonsensational" }
{ "public_path":"flowers/factory/F105_visitation_booth_glass_dim.mp4", "act":3, "covers_scene_id":"S131", "subtype":"visitation_booth_glass_dim" }
{ "public_path":"flowers/factory/F106_slate_sky_slow_clouds.mp4", "act":3, "covers_scene_id":null, "subtype":"slate_sky_slow_clouds" }
{ "public_path":"flowers/factory/F107_jury_room_table_empty.mp4", "act":3, "covers_scene_id":"S118", "subtype":"jury_room_table_empty" }
{ "public_path":"flowers/factory/F108_smalltown_dusk_quiet.mp4", "act":3, "covers_scene_id":null, "subtype":"smalltown_dusk_quiet" }
{ "public_path":"flowers/factory/F109_prison_phone_wall_dim.mp4", "act":3, "covers_scene_id":"S139", "subtype":"prison_phone_wall_dim" }
{ "public_path":"flowers/factory/F110_concrete_wall_shadow.mp4", "act":3, "covers_scene_id":null, "subtype":"concrete_wall_shadow" }
{ "public_path":"flowers/factory/F111_delta_flat_horizon.mp4", "act":3, "covers_scene_id":null, "subtype":"delta_flat_horizon" }
{ "public_path":"flowers/factory/F112_courthouse_steps_evening.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_steps_evening" }
{ "public_path":"flowers/factory/F113_lawyer_office_desk_lamp.mp4", "act":3, "covers_scene_id":null, "subtype":"lawyer_office_desk_lamp" }
{ "public_path":"flowers/factory/F114_county_jail_exterior.mp4", "act":3, "covers_scene_id":null, "subtype":"county_jail_exterior" }
{ "public_path":"flowers/factory/F115_prison_exterior_farmland_flat_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_exterior_farmland_flat_02" }
{ "public_path":"flowers/factory/F116_razor_wire_fence_distant_02.mp4", "act":3, "covers_scene_id":null, "subtype":"razor_wire_fence_distant_02" }
{ "public_path":"flowers/factory/F117_cell_block_window_light_02.mp4", "act":3, "covers_scene_id":null, "subtype":"cell_block_window_light_02" }
{ "public_path":"flowers/factory/F118_long_prison_corridor_02.mp4", "act":3, "covers_scene_id":null, "subtype":"long_prison_corridor_02" }
{ "public_path":"flowers/factory/F119_prison_yard_empty_nonsensational_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_yard_empty_nonsensational_02" }
{ "public_path":"flowers/factory/F120_visitation_booth_glass_dim_02.mp4", "act":3, "covers_scene_id":null, "subtype":"visitation_booth_glass_dim_02" }
{ "public_path":"flowers/factory/F121_slate_sky_slow_clouds_02.mp4", "act":3, "covers_scene_id":null, "subtype":"slate_sky_slow_clouds_02" }
{ "public_path":"flowers/factory/F122_jury_room_table_empty_02.mp4", "act":3, "covers_scene_id":null, "subtype":"jury_room_table_empty_02" }
{ "public_path":"flowers/factory/F123_smalltown_dusk_quiet_02.mp4", "act":3, "covers_scene_id":null, "subtype":"smalltown_dusk_quiet_02" }
{ "public_path":"flowers/factory/F124_prison_phone_wall_dim_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_phone_wall_dim_02" }
{ "public_path":"flowers/factory/F125_concrete_wall_shadow_02.mp4", "act":3, "covers_scene_id":null, "subtype":"concrete_wall_shadow_02" }
{ "public_path":"flowers/factory/F126_delta_flat_horizon_02.mp4", "act":3, "covers_scene_id":null, "subtype":"delta_flat_horizon_02" }
{ "public_path":"flowers/factory/F127_courthouse_steps_evening_02.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_steps_evening_02" }
{ "public_path":"flowers/factory/F128_lawyer_office_desk_lamp_02.mp4", "act":3, "covers_scene_id":null, "subtype":"lawyer_office_desk_lamp_02" }
{ "public_path":"flowers/factory/F129_county_jail_exterior_02.mp4", "act":3, "covers_scene_id":null, "subtype":"county_jail_exterior_02" }
{ "public_path":"flowers/factory/F130_prison_exterior_farmland_flat_03.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_exterior_farmland_flat_03" }
{ "public_path":"flowers/factory/F131_razor_wire_fence_distant_03.mp4", "act":3, "covers_scene_id":null, "subtype":"razor_wire_fence_distant_03" }
{ "public_path":"flowers/factory/F132_cell_block_window_light_03.mp4", "act":3, "covers_scene_id":null, "subtype":"cell_block_window_light_03" }
{ "public_path":"flowers/factory/F133_long_prison_corridor_03.mp4", "act":3, "covers_scene_id":null, "subtype":"long_prison_corridor_03" }
{ "public_path":"flowers/factory/F134_prison_yard_empty_nonsensational_03.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_yard_empty_nonsensational_03" }
{ "public_path":"flowers/factory/F135_visitation_booth_glass_dim_03.mp4", "act":3, "covers_scene_id":null, "subtype":"visitation_booth_glass_dim_03" }
{ "public_path":"flowers/factory/F136_slate_sky_slow_clouds_03.mp4", "act":3, "covers_scene_id":null, "subtype":"slate_sky_slow_clouds_03" }
{ "public_path":"flowers/factory/F137_jury_room_table_empty_03.mp4", "act":3, "covers_scene_id":null, "subtype":"jury_room_table_empty_03" }
{ "public_path":"flowers/factory/F138_smalltown_dusk_quiet_03.mp4", "act":3, "covers_scene_id":null, "subtype":"smalltown_dusk_quiet_03" }
{ "public_path":"flowers/factory/F139_prison_phone_wall_dim_03.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_phone_wall_dim_03" }
{ "public_path":"flowers/factory/F140_concrete_wall_shadow_03.mp4", "act":3, "covers_scene_id":null, "subtype":"concrete_wall_shadow_03" }
{ "public_path":"flowers/factory/F141_delta_flat_horizon_03.mp4", "act":3, "covers_scene_id":null, "subtype":"delta_flat_horizon_03" }
{ "public_path":"flowers/factory/F142_courthouse_steps_evening_03.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_steps_evening_03" }
{ "public_path":"flowers/factory/F143_lawyer_office_desk_lamp_03.mp4", "act":3, "covers_scene_id":null, "subtype":"lawyer_office_desk_lamp_03" }
{ "public_path":"flowers/factory/F144_county_jail_exterior_03.mp4", "act":3, "covers_scene_id":null, "subtype":"county_jail_exterior_03" }
// ACT4 The Ninth Inning (act 4) — 42
{ "public_path":"flowers/factory/F145_supreme_court_columns_dc.mp4", "act":4, "covers_scene_id":"S164", "subtype":"supreme_court_columns_dc" }
{ "public_path":"flowers/factory/F146_marble_steps_wide_dc.mp4", "act":4, "covers_scene_id":null, "subtype":"marble_steps_wide_dc" }
{ "public_path":"flowers/factory/F147_archive_boxes_dusty_shelves.mp4", "act":4, "covers_scene_id":"S156", "subtype":"archive_boxes_dusty_shelves" }
{ "public_path":"flowers/factory/F148_microfilm_reader_glow.mp4", "act":4, "covers_scene_id":null, "subtype":"microfilm_reader_glow" }
{ "public_path":"flowers/factory/F149_audio_recorder_closeup.mp4", "act":4, "covers_scene_id":"S174", "subtype":"audio_recorder_closeup" }
{ "public_path":"flowers/factory/F150_radio_studio_dim_mic.mp4", "act":4, "covers_scene_id":null, "subtype":"radio_studio_dim_mic" }
{ "public_path":"flowers/factory/F151_december_morning_sky_cold.mp4", "act":4, "covers_scene_id":null, "subtype":"december_morning_sky_cold" }
{ "public_path":"flowers/factory/F152_prison_gate_opening_dawn.mp4", "act":4, "covers_scene_id":"S172", "subtype":"prison_gate_opening_dawn" }
{ "public_path":"flowers/factory/F153_polling_place_exterior_dusk.mp4", "act":4, "covers_scene_id":"S188", "subtype":"polling_place_exterior_dusk" }
{ "public_path":"flowers/factory/F154_voting_booth_curtain.mp4", "act":4, "covers_scene_id":null, "subtype":"voting_booth_curtain" }
{ "public_path":"flowers/factory/F155_mississippi_state_capitol.mp4", "act":4, "covers_scene_id":null, "subtype":"mississippi_state_capitol" }
{ "public_path":"flowers/factory/F156_morning_blue_sky_clouds.mp4", "act":4, "covers_scene_id":null, "subtype":"morning_blue_sky_clouds" }
{ "public_path":"flowers/factory/F157_courthouse_pediment_detail.mp4", "act":4, "covers_scene_id":null, "subtype":"courthouse_pediment_detail" }
{ "public_path":"flowers/factory/F158_paper_archive_stacks.mp4", "act":4, "covers_scene_id":null, "subtype":"paper_archive_stacks" }
{ "public_path":"flowers/factory/F159_supreme_court_columns_dc_02.mp4", "act":4, "covers_scene_id":null, "subtype":"supreme_court_columns_dc_02" }
{ "public_path":"flowers/factory/F160_marble_steps_wide_dc_02.mp4", "act":4, "covers_scene_id":null, "subtype":"marble_steps_wide_dc_02" }
{ "public_path":"flowers/factory/F161_archive_boxes_dusty_shelves_02.mp4", "act":4, "covers_scene_id":null, "subtype":"archive_boxes_dusty_shelves_02" }
{ "public_path":"flowers/factory/F162_microfilm_reader_glow_02.mp4", "act":4, "covers_scene_id":null, "subtype":"microfilm_reader_glow_02" }
{ "public_path":"flowers/factory/F163_audio_recorder_closeup_02.mp4", "act":4, "covers_scene_id":null, "subtype":"audio_recorder_closeup_02" }
{ "public_path":"flowers/factory/F164_radio_studio_dim_mic_02.mp4", "act":4, "covers_scene_id":null, "subtype":"radio_studio_dim_mic_02" }
{ "public_path":"flowers/factory/F165_december_morning_sky_cold_02.mp4", "act":4, "covers_scene_id":null, "subtype":"december_morning_sky_cold_02" }
{ "public_path":"flowers/factory/F166_prison_gate_opening_dawn_02.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_gate_opening_dawn_02" }
{ "public_path":"flowers/factory/F167_polling_place_exterior_dusk_02.mp4", "act":4, "covers_scene_id":null, "subtype":"polling_place_exterior_dusk_02" }
{ "public_path":"flowers/factory/F168_voting_booth_curtain_02.mp4", "act":4, "covers_scene_id":null, "subtype":"voting_booth_curtain_02" }
{ "public_path":"flowers/factory/F169_mississippi_state_capitol_02.mp4", "act":4, "covers_scene_id":null, "subtype":"mississippi_state_capitol_02" }
{ "public_path":"flowers/factory/F170_morning_blue_sky_clouds_02.mp4", "act":4, "covers_scene_id":null, "subtype":"morning_blue_sky_clouds_02" }
{ "public_path":"flowers/factory/F171_courthouse_pediment_detail_02.mp4", "act":4, "covers_scene_id":null, "subtype":"courthouse_pediment_detail_02" }
{ "public_path":"flowers/factory/F172_paper_archive_stacks_02.mp4", "act":4, "covers_scene_id":null, "subtype":"paper_archive_stacks_02" }
{ "public_path":"flowers/factory/F173_supreme_court_columns_dc_03.mp4", "act":4, "covers_scene_id":null, "subtype":"supreme_court_columns_dc_03" }
{ "public_path":"flowers/factory/F174_marble_steps_wide_dc_03.mp4", "act":4, "covers_scene_id":null, "subtype":"marble_steps_wide_dc_03" }
{ "public_path":"flowers/factory/F175_archive_boxes_dusty_shelves_03.mp4", "act":4, "covers_scene_id":null, "subtype":"archive_boxes_dusty_shelves_03" }
{ "public_path":"flowers/factory/F176_microfilm_reader_glow_03.mp4", "act":4, "covers_scene_id":null, "subtype":"microfilm_reader_glow_03" }
{ "public_path":"flowers/factory/F177_audio_recorder_closeup_03.mp4", "act":4, "covers_scene_id":null, "subtype":"audio_recorder_closeup_03" }
{ "public_path":"flowers/factory/F178_radio_studio_dim_mic_03.mp4", "act":4, "covers_scene_id":null, "subtype":"radio_studio_dim_mic_03" }
{ "public_path":"flowers/factory/F179_december_morning_sky_cold_03.mp4", "act":4, "covers_scene_id":null, "subtype":"december_morning_sky_cold_03" }
{ "public_path":"flowers/factory/F180_prison_gate_opening_dawn_03.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_gate_opening_dawn_03" }
{ "public_path":"flowers/factory/F181_polling_place_exterior_dusk_03.mp4", "act":4, "covers_scene_id":null, "subtype":"polling_place_exterior_dusk_03" }
{ "public_path":"flowers/factory/F182_voting_booth_curtain_03.mp4", "act":4, "covers_scene_id":null, "subtype":"voting_booth_curtain_03" }
{ "public_path":"flowers/factory/F183_mississippi_state_capitol_03.mp4", "act":4, "covers_scene_id":null, "subtype":"mississippi_state_capitol_03" }
{ "public_path":"flowers/factory/F184_morning_blue_sky_clouds_03.mp4", "act":4, "covers_scene_id":null, "subtype":"morning_blue_sky_clouds_03" }
{ "public_path":"flowers/factory/F185_courthouse_pediment_detail_03.mp4", "act":4, "covers_scene_id":null, "subtype":"courthouse_pediment_detail_03" }
{ "public_path":"flowers/factory/F186_paper_archive_stacks_03.mp4", "act":4, "covers_scene_id":null, "subtype":"paper_archive_stacks_03" }
// ENDING (act 5) — 15
{ "public_path":"flowers/factory/F187_church_window_dawn_light.mp4", "act":5, "covers_scene_id":"S204", "subtype":"church_window_dawn_light" }
{ "public_path":"flowers/factory/F188_smalltown_dawn_quiet_street.mp4", "act":5, "covers_scene_id":"S208", "subtype":"smalltown_dawn_quiet_street" }
{ "public_path":"flowers/factory/F189_dirt_road_morning_blue.mp4", "act":5, "covers_scene_id":"S207", "subtype":"dirt_road_morning_blue" }
{ "public_path":"flowers/factory/F190_storefront_quiet_dawn.mp4", "act":5, "covers_scene_id":null, "subtype":"storefront_quiet_dawn" }
{ "public_path":"flowers/factory/F191_dust_motes_settling_gold.mp4", "act":5, "covers_scene_id":"S210", "subtype":"dust_motes_settling_gold" }
{ "public_path":"flowers/factory/F192_church_window_dawn_light_02.mp4", "act":5, "covers_scene_id":null, "subtype":"church_window_dawn_light_02" }
{ "public_path":"flowers/factory/F193_smalltown_dawn_quiet_street_02.mp4", "act":5, "covers_scene_id":null, "subtype":"smalltown_dawn_quiet_street_02" }
{ "public_path":"flowers/factory/F194_dirt_road_morning_blue_02.mp4", "act":5, "covers_scene_id":null, "subtype":"dirt_road_morning_blue_02" }
{ "public_path":"flowers/factory/F195_storefront_quiet_dawn_02.mp4", "act":5, "covers_scene_id":null, "subtype":"storefront_quiet_dawn_02" }
{ "public_path":"flowers/factory/F196_dust_motes_settling_gold_02.mp4", "act":5, "covers_scene_id":null, "subtype":"dust_motes_settling_gold_02" }
{ "public_path":"flowers/factory/F197_church_window_dawn_light_03.mp4", "act":5, "covers_scene_id":null, "subtype":"church_window_dawn_light_03" }
{ "public_path":"flowers/factory/F198_smalltown_dawn_quiet_street_03.mp4", "act":5, "covers_scene_id":null, "subtype":"smalltown_dawn_quiet_street_03" }
{ "public_path":"flowers/factory/F199_dirt_road_morning_blue_03.mp4", "act":5, "covers_scene_id":null, "subtype":"dirt_road_morning_blue_03" }
{ "public_path":"flowers/factory/F200_storefront_quiet_dawn_03.mp4", "act":5, "covers_scene_id":null, "subtype":"storefront_quiet_dawn_03" }
{ "public_path":"flowers/factory/F201_dust_motes_settling_gold_03.mp4", "act":5, "covers_scene_id":null, "subtype":"dust_motes_settling_gold_03" }
// 繋ぎ (bridge・covers null・act 1〜4 に配分) — 35
{ "public_path":"flowers/factory/F202_institutional_corridor_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"institutional_corridor_dim" }
{ "public_path":"flowers/factory/F203_ceiling_fan_slow_period.mp4", "act":1, "covers_scene_id":null, "subtype":"ceiling_fan_slow_period" }
{ "public_path":"flowers/factory/F204_oak_texture_macro.mp4", "act":1, "covers_scene_id":null, "subtype":"oak_texture_macro" }
{ "public_path":"flowers/factory/F205_heat_shimmer_asphalt.mp4", "act":1, "covers_scene_id":null, "subtype":"heat_shimmer_asphalt" }
{ "public_path":"flowers/factory/F206_flat_field_wind.mp4", "act":1, "covers_scene_id":null, "subtype":"flat_field_wind" }
{ "public_path":"flowers/factory/F207_telephone_lines_dusk.mp4", "act":1, "covers_scene_id":null, "subtype":"telephone_lines_dusk" }
{ "public_path":"flowers/factory/F208_brick_wall_texture_warm.mp4", "act":1, "covers_scene_id":null, "subtype":"brick_wall_texture_warm" }
{ "public_path":"flowers/factory/F209_streetlamp_night_moths.mp4", "act":1, "covers_scene_id":null, "subtype":"streetlamp_night_moths" }
{ "public_path":"flowers/factory/F210_kudzu_treeline_wind.mp4", "act":2, "covers_scene_id":null, "subtype":"kudzu_treeline_wind" }
{ "public_path":"flowers/factory/F211_freight_train_passing_distant.mp4", "act":2, "covers_scene_id":null, "subtype":"freight_train_passing_distant" }
{ "public_path":"flowers/factory/F212_marble_texture_macro.mp4", "act":2, "covers_scene_id":null, "subtype":"marble_texture_macro" }
{ "public_path":"flowers/factory/F213_window_blinds_light_bars.mp4", "act":2, "covers_scene_id":null, "subtype":"window_blinds_light_bars" }
{ "public_path":"flowers/factory/F214_paper_stack_closeup_unreadable.mp4", "act":2, "covers_scene_id":null, "subtype":"paper_stack_closeup_unreadable" }
{ "public_path":"flowers/factory/F215_dust_in_light_macro.mp4", "act":2, "covers_scene_id":null, "subtype":"dust_in_light_macro" }
{ "public_path":"flowers/factory/F216_courthouse_flagpole_lawn.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_flagpole_lawn" }
{ "public_path":"flowers/factory/F217_institutional_corridor_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"institutional_corridor_dim_02" }
{ "public_path":"flowers/factory/F218_oak_texture_macro_02.mp4", "act":2, "covers_scene_id":null, "subtype":"oak_texture_macro_02" }
{ "public_path":"flowers/factory/F219_rain_on_window_slate.mp4", "act":3, "covers_scene_id":null, "subtype":"rain_on_window_slate" }
{ "public_path":"flowers/factory/F220_chain_link_fence_closeup.mp4", "act":3, "covers_scene_id":null, "subtype":"chain_link_fence_closeup" }
{ "public_path":"flowers/factory/F221_bare_lightbulb_dim_room.mp4", "act":3, "covers_scene_id":null, "subtype":"bare_lightbulb_dim_room" }
{ "public_path":"flowers/factory/F222_clock_hands_slow_macro.mp4", "act":3, "covers_scene_id":null, "subtype":"clock_hands_slow_macro" }
{ "public_path":"flowers/factory/F223_winter_trees_bare_flat.mp4", "act":3, "covers_scene_id":null, "subtype":"winter_trees_bare_flat" }
{ "public_path":"flowers/factory/F224_flat_field_wind_02.mp4", "act":3, "covers_scene_id":null, "subtype":"flat_field_wind_02" }
{ "public_path":"flowers/factory/F225_window_blinds_light_bars_02.mp4", "act":3, "covers_scene_id":null, "subtype":"window_blinds_light_bars_02" }
{ "public_path":"flowers/factory/F226_dust_in_light_macro_02.mp4", "act":3, "covers_scene_id":null, "subtype":"dust_in_light_macro_02" }
{ "public_path":"flowers/factory/F227_rain_on_window_slate_02.mp4", "act":3, "covers_scene_id":null, "subtype":"rain_on_window_slate_02" }
{ "public_path":"flowers/factory/F228_city_night_traffic_long_lens.mp4", "act":4, "covers_scene_id":null, "subtype":"city_night_traffic_long_lens" }
{ "public_path":"flowers/factory/F229_capitol_dome_dusk.mp4", "act":4, "covers_scene_id":null, "subtype":"capitol_dome_dusk" }
{ "public_path":"flowers/factory/F230_newspaper_press_rolling_unreadable.mp4", "act":4, "covers_scene_id":null, "subtype":"newspaper_press_rolling_unreadable" }
{ "public_path":"flowers/factory/F231_sunrise_over_flat_land.mp4", "act":4, "covers_scene_id":null, "subtype":"sunrise_over_flat_land" }
{ "public_path":"flowers/factory/F232_marble_texture_macro_02.mp4", "act":4, "covers_scene_id":null, "subtype":"marble_texture_macro_02" }
{ "public_path":"flowers/factory/F233_paper_stack_closeup_unreadable_02.mp4", "act":4, "covers_scene_id":null, "subtype":"paper_stack_closeup_unreadable_02" }
{ "public_path":"flowers/factory/F234_telephone_lines_dusk_02.mp4", "act":4, "covers_scene_id":null, "subtype":"telephone_lines_dusk_02" }
{ "public_path":"flowers/factory/F235_sunrise_over_flat_land_02.mp4", "act":4, "covers_scene_id":null, "subtype":"sunrise_over_flat_land_02" }
{ "public_path":"flowers/factory/F236_capitol_dome_dusk_02.mp4", "act":4, "covers_scene_id":null, "subtype":"capitol_dome_dusk_02" }
```

**検算:** act0 12 + act1 42 + act2 45 + act3 45 + act4 42 + act5 15 = 201、＋繋ぎ 35（act1×8 / act2×9 / act3×9 / act4×9）= **236** ✓。covers 付き 22本・残り null。**暗いクリップは約78本（1/3）まで**＝courthouse 昼光・July の日中・dawn/morning blue を混ぜる（§7.5）。

## 4.5 ★`motion[]` 全44エントリ（★必ず実体化・public_path 非空）

> エントリ形は §4.1a 準拠 + 動画フィールド。`asset_id ^FLW-M\d{2}$`。`source_still` は §8.1a の種画像、`source_scene_id`=`MS<NN>`。runtime で `sha256`/`width 1280`/`height 720`/`fps 48`/`frames`/`duration_sec`/`qc` を埋める（§8.4）。**空配列を書かない。** `H0NN_anon` タグ＝§5.11 の匿名人物種（18本・44の内数）。

```jsonc
{ "asset_id":"FLW-M01", "source_scene_id":"MS01", "source_still":"H:/pd-media/assets/ai/flowers/M01_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M01_rife.mp4", "public_path":"flowers/motion/M01_rife.mp4", "act":0, "storyboard":"hook", "tags":["numerals_accumulate_I_to_VI"] }
{ "asset_id":"FLW-M02", "source_scene_id":"MS02", "source_still":"H:/pd-media/assets/ai/flowers/M02_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M02_rife.mp4", "public_path":"flowers/motion/M02_rife.mp4", "act":0, "storyboard":"A0-01", "tags":["strike_line_draws_across_card"] }
{ "asset_id":"FLW-M03", "source_scene_id":"MS03", "source_still":"H:/pd-media/assets/ai/flowers/M03_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M03_rife.mp4", "public_path":"flowers/motion/M03_rife.mp4", "act":0, "storyboard":"A0-02", "tags":["jury_chair_lights_going_out"] }
{ "asset_id":"FLW-M04", "source_scene_id":"MS04", "source_still":"H:/pd-media/assets/ai/flowers/M04_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M04_rife.mp4", "public_path":"flowers/motion/M04_rife.mp4", "act":1, "storyboard":"A1-01", "tags":["investigators_corkboard_hands","H001_anon"] }
{ "asset_id":"FLW-M05", "source_scene_id":"MS05", "source_still":"H:/pd-media/assets/ai/flowers/M05_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M05_rife.mp4", "public_path":"flowers/motion/M05_rife.mp4", "act":1, "storyboard":"A1-02", "tags":["storefront_four_lights_dimming"] }
{ "asset_id":"FLW-M06", "source_scene_id":"MS06", "source_still":"H:/pd-media/assets/ai/flowers/M06_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M06_rife.mp4", "public_path":"flowers/motion/M06_rife.mp4", "act":1, "storyboard":"A1-03", "tags":["gospel_choir_sway_backlit","H002_anon"] }
{ "asset_id":"FLW-M07", "source_scene_id":"MS07", "source_still":"H:/pd-media/assets/ai/flowers/M07_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M07_rife.mp4", "public_path":"flowers/motion/M07_rife.mp4", "act":1, "storyboard":"A1-04", "tags":["heat_shimmer_mainstreet"] }
{ "asset_id":"FLW-M08", "source_scene_id":"MS08", "source_still":"H:/pd-media/assets/ai/flowers/M08_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M08_rife.mp4", "public_path":"flowers/motion/M08_rife.mp4", "act":1, "storyboard":"A1-05", "tags":["arrest_walk_from_behind_slate","H003_anon"] }
{ "asset_id":"FLW-M09", "source_scene_id":"MS09", "source_still":"H:/pd-media/assets/ai/flowers/M09_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M09_rife.mp4", "public_path":"flowers/motion/M09_rife.mp4", "act":1, "storyboard":"A1-06", "tags":["route_fragmenting_erased"] }
{ "asset_id":"FLW-M10", "source_scene_id":"MS10", "source_still":"H:/pd-media/assets/ai/flowers/M10_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M10_rife.mp4", "public_path":"flowers/motion/M10_rife.mp4", "act":1, "storyboard":"A1-07", "tags":["hands_writing_statement_drawer","H004_anon"] }
{ "asset_id":"FLW-M11", "source_scene_id":"MS11", "source_still":"H:/pd-media/assets/ai/flowers/M11_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M11_rife.mp4", "public_path":"flowers/motion/M11_rife.mp4", "act":2, "storyboard":"A2-01", "tags":["numeral_I_sears_then_cracks"] }
{ "asset_id":"FLW-M12", "source_scene_id":"MS12", "source_still":"H:/pd-media/assets/ai/flowers/M12_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M12_rife.mp4", "public_path":"flowers/motion/M12_rife.mp4", "act":2, "storyboard":"A2-02", "tags":["prosecutor_silhouette_podium_rises","H005_anon"] }
{ "asset_id":"FLW-M13", "source_scene_id":"MS13", "source_still":"H:/pd-media/assets/ai/flowers/M13_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M13_rife.mp4", "public_path":"flowers/motion/M13_rife.mp4", "act":2, "storyboard":"A2-03", "tags":["twelve_chairs_light_12_0"] }
{ "asset_id":"FLW-M14", "source_scene_id":"MS14", "source_still":"H:/pd-media/assets/ai/flowers/M14_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M14_rife.mp4", "public_path":"flowers/motion/M14_rife.mp4", "act":2, "storyboard":"A2-04", "tags":["verdict_backs_rising_1997","H006_anon"] }
{ "asset_id":"FLW-M15", "source_scene_id":"MS15", "source_still":"H:/pd-media/assets/ai/flowers/M15_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M15_rife.mp4", "public_path":"flowers/motion/M15_rife.mp4", "act":2, "storyboard":"A2-05", "tags":["strike_cards_stacking"] }
{ "asset_id":"FLW-M16", "source_scene_id":"MS16", "source_still":"H:/pd-media/assets/ai/flowers/M16_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M16_rife.mp4", "public_path":"flowers/motion/M16_rife.mp4", "act":2, "storyboard":"A2-06", "tags":["appellate_bench_silhouettes","H007_anon"] }
{ "asset_id":"FLW-M17", "source_scene_id":"MS17", "source_still":"H:/pd-media/assets/ai/flowers/M17_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M17_rife.mp4", "public_path":"flowers/motion/M17_rife.mp4", "act":2, "storyboard":"A2-07", "tags":["numerals_II_III_crack_cascade"] }
{ "asset_id":"FLW-M18", "source_scene_id":"MS18", "source_still":"H:/pd-media/assets/ai/flowers/M18_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M18_rife.mp4", "public_path":"flowers/motion/M18_rife.mp4", "act":2, "storyboard":"A2-08", "tags":["transport_corridor_walk","H008_anon"] }
{ "asset_id":"FLW-M19", "source_scene_id":"MS19", "source_still":"H:/pd-media/assets/ai/flowers/M19_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M19_rife.mp4", "public_path":"flowers/motion/M19_rife.mp4", "act":2, "storyboard":"A2-09", "tags":["reserve_folder_pulled_drawer","H009_anon"] }
{ "asset_id":"FLW-M20", "source_scene_id":"MS20", "source_still":"H:/pd-media/assets/ai/flowers/M20_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M20_rife.mp4", "public_path":"flowers/motion/M20_rife.mp4", "act":3, "storyboard":"A3-01", "tags":["faultsplit_frame_straining"] }
{ "asset_id":"FLW-M21", "source_scene_id":"MS21", "source_still":"H:/pd-media/assets/ai/flowers/M21_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M21_rife.mp4", "public_path":"flowers/motion/M21_rife.mp4", "act":3, "storyboard":"A3-02", "tags":["jury_room_backs_split_apart","H010_anon"] }
{ "asset_id":"FLW-M22", "source_scene_id":"MS22", "source_still":"H:/pd-media/assets/ai/flowers/M22_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M22_rife.mp4", "public_path":"flowers/motion/M22_rife.mp4", "act":3, "storyboard":"A3-03", "tags":["chair_map_7_5_ignites"] }
{ "asset_id":"FLW-M23", "source_scene_id":"MS23", "source_still":"H:/pd-media/assets/ai/flowers/M23_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M23_rife.mp4", "public_path":"flowers/motion/M23_rife.mp4", "act":3, "storyboard":"A3-04", "tags":["single_chair_spotlight_shadow","H011_anon"] }
{ "asset_id":"FLW-M24", "source_scene_id":"MS24", "source_still":"H:/pd-media/assets/ai/flowers/M24_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M24_rife.mp4", "public_path":"flowers/motion/M24_rife.mp4", "act":3, "storyboard":"A3-05", "tags":["clock_hands_half_hour"] }
{ "asset_id":"FLW-M25", "source_scene_id":"MS25", "source_still":"H:/pd-media/assets/ai/flowers/M25_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M25_rife.mp4", "public_path":"flowers/motion/M25_rife.mp4", "act":3, "storyboard":"A3-06", "tags":["numeral_VI_sears_fast"] }
{ "asset_id":"FLW-M26", "source_scene_id":"MS26", "source_still":"H:/pd-media/assets/ai/flowers/M26_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M26_rife.mp4", "public_path":"flowers/motion/M26_rife.mp4", "act":3, "storyboard":"A3-07", "tags":["inmate_bunk_light_ages","H012_anon"] }
{ "asset_id":"FLW-M27", "source_scene_id":"MS27", "source_still":"H:/pd-media/assets/ai/flowers/M27_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M27_rife.mp4", "public_path":"flowers/motion/M27_rife.mp4", "act":3, "storyboard":"A3-08", "tags":["silhouette_behind_ribbed_glass"] }
{ "asset_id":"FLW-M28", "source_scene_id":"MS28", "source_still":"H:/pd-media/assets/ai/flowers/M28_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M28_rife.mp4", "public_path":"flowers/motion/M28_rife.mp4", "act":3, "storyboard":"A3-09", "tags":["prison_phone_figure_behind","H013_anon"] }
{ "asset_id":"FLW-M29", "source_scene_id":"MS29", "source_still":"H:/pd-media/assets/ai/flowers/M29_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M29_rife.mp4", "public_path":"flowers/motion/M29_rife.mp4", "act":3, "storyboard":"A3-10", "tags":["three_lights_extinguish_dignity"] }
{ "asset_id":"FLW-M30", "source_scene_id":"MS30", "source_still":"H:/pd-media/assets/ai/flowers/M30_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M30_rife.mp4", "public_path":"flowers/motion/M30_rife.mp4", "act":3, "storyboard":"A3-11", "tags":["recorder_toward_glass_waveform","H014_anon"] }
{ "asset_id":"FLW-M31", "source_scene_id":"MS31", "source_still":"H:/pd-media/assets/ai/flowers/M31_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M31_rife.mp4", "public_path":"flowers/motion/M31_rife.mp4", "act":4, "storyboard":"A4-01", "tags":["docket_pages_turning_unreadable"] }
{ "asset_id":"FLW-M32", "source_scene_id":"MS32", "source_still":"H:/pd-media/assets/ai/flowers/M32_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M32_rife.mp4", "public_path":"flowers/motion/M32_rife.mp4", "act":4, "storyboard":"A4-02", "tags":["reporters_walk_winona_backs","H015_anon"] }
{ "asset_id":"FLW-M33", "source_scene_id":"MS33", "source_still":"H:/pd-media/assets/ai/flowers/M33_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M33_rife.mp4", "public_path":"flowers/motion/M33_rife.mp4", "act":4, "storyboard":"A4-03", "tags":["bars_ignite_50_vs_11_abstract"] }
{ "asset_id":"FLW-M34", "source_scene_id":"MS34", "source_still":"H:/pd-media/assets/ai/flowers/M34_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M34_rife.mp4", "public_path":"flowers/motion/M34_rife.mp4", "act":4, "storyboard":"A4-04", "tags":["strike_card_wall_ignites"] }
{ "asset_id":"FLW-M35", "source_scene_id":"MS35", "source_still":"H:/pd-media/assets/ai/flowers/M35_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M35_rife.mp4", "public_path":"flowers/motion/M35_rife.mp4", "act":4, "storyboard":"A4-05", "tags":["lectern_advocate_backs_marble","H016_anon"] }
{ "asset_id":"FLW-M36", "source_scene_id":"MS36", "source_still":"H:/pd-media/assets/ai/flowers/M36_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M36_rife.mp4", "public_path":"flowers/motion/M36_rife.mp4", "act":4, "storyboard":"A4-06", "tags":["numeral_row_fractures"] }
{ "asset_id":"FLW-M37", "source_scene_id":"MS37", "source_still":"H:/pd-media/assets/ai/flowers/M37_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M37_rife.mp4", "public_path":"flowers/motion/M37_rife.mp4", "act":4, "storyboard":"A4-07", "tags":["december_gate_opens_blue"] }
{ "asset_id":"FLW-M38", "source_scene_id":"MS38", "source_still":"H:/pd-media/assets/ai/flowers/M38_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M38_rife.mp4", "public_path":"flowers/motion/M38_rife.mp4", "act":4, "storyboard":"A4-08", "tags":["walkout_morning_blue_crowd_backs","H017_anon"] }
{ "asset_id":"FLW-M39", "source_scene_id":"MS39", "source_still":"H:/pd-media/assets/ai/flowers/M39_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M39_rife.mp4", "public_path":"flowers/motion/M39_rife.mp4", "act":4, "storyboard":"A4-09", "tags":["six_numerals_collapse_to_dust"] }
{ "asset_id":"FLW-M40", "source_scene_id":"MS40", "source_still":"H:/pd-media/assets/ai/flowers/M40_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M40_rife.mp4", "public_path":"flowers/motion/M40_rife.mp4", "act":4, "storyboard":"A4-10", "tags":["voting_booth_curtain_lever","H018_anon"] }
{ "asset_id":"FLW-M41", "source_scene_id":"MS41", "source_still":"H:/pd-media/assets/ai/flowers/M41_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M41_rife.mp4", "public_path":"flowers/motion/M41_rife.mp4", "act":5, "storyboard":"A5-01", "tags":["four_chairs_light_crossing"] }
{ "asset_id":"FLW-M42", "source_scene_id":"MS42", "source_still":"H:/pd-media/assets/ai/flowers/M42_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M42_rife.mp4", "public_path":"flowers/motion/M42_rife.mp4", "act":5, "storyboard":"A5-02", "tags":["numeral_row_stands_dark_road"] }
{ "asset_id":"FLW-M43", "source_scene_id":"MS43", "source_still":"H:/pd-media/assets/ai/flowers/M43_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M43_rife.mp4", "public_path":"flowers/motion/M43_rife.mp4", "act":5, "storyboard":"A5-03", "tags":["hymnal_pages_stir_dawn"] }
{ "asset_id":"FLW-M44", "source_scene_id":"MS44", "source_still":"H:/pd-media/assets/ai/flowers/M44_src.png", "path":"H:/pd-media/assets/ai_video/flowers/M44_rife.mp4", "public_path":"flowers/motion/M44_rife.mp4", "act":5, "storyboard":"A5-04", "tags":["dust_motes_settle_final"] }
```

**検算:** 44エントリ ✓・全 public_path 非空 ✓（不変条件18）・`^FLW-M\d{2}$` ✓・幕別 3/7/9/11/10/4 = 44 ✓・**★H001–H018（匿名人物・18本）は M04/M06/M08/M10・M12/M14/M16/M18/M19・M21/M23/M26/M28/M30・M32/M35/M38/M40 の内数 ✓**（＝44 motion のうち 18 が人物・88 cuts のうち最大36が人物）。残り26本が抽象/象徴。

## 4.6 `overlay[]` 30エントリ（distinct 素材に数えない・15 particle / 10 light / 5 vfx）

```jsonc
{ "public_path":"flowers/overlay/P01_courtroom_dust.mp4", "type":"particle_assets", "subtype":"courtroom_dust", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P02_storeroom_dust_gold.mp4", "type":"particle_assets", "subtype":"storeroom_dust_gold", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P03_heat_haze_particles.mp4", "type":"particle_assets", "subtype":"heat_haze_particles", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P04_church_light_motes.mp4", "type":"particle_assets", "subtype":"church_light_motes", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P05_dry_field_dust.mp4", "type":"particle_assets", "subtype":"dry_field_dust", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P06_archive_dust_drift.mp4", "type":"particle_assets", "subtype":"archive_dust_drift", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P07_prison_dust_slate.mp4", "type":"particle_assets", "subtype":"prison_dust_slate", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P08_night_air_drift.mp4", "type":"particle_assets", "subtype":"night_air_drift", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P09_paper_fiber_drift.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P10_gold_dust_drift.mp4", "type":"particle_assets", "subtype":"gold_dust_drift", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P11_courtroom_dust_02.mp4", "type":"particle_assets", "subtype":"courtroom_dust_02", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P12_storeroom_dust_gold_02.mp4", "type":"particle_assets", "subtype":"storeroom_dust_gold_02", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P13_heat_haze_particles_02.mp4", "type":"particle_assets", "subtype":"heat_haze_particles_02", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P14_church_light_motes_02.mp4", "type":"particle_assets", "subtype":"church_light_motes_02", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/P15_prison_dust_slate_02.mp4", "type":"particle_assets", "subtype":"prison_dust_slate_02", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/L01_dust_gold_shaft.mp4", "type":"light_assets", "subtype":"dust_gold_shaft", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/L02_oak_window_light_bar.mp4", "type":"light_assets", "subtype":"oak_window_light_bar", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/L03_slate_window_light.mp4", "type":"light_assets", "subtype":"slate_window_light", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/L04_courtroom_lamp_glow.mp4", "type":"light_assets", "subtype":"courtroom_lamp_glow", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/L05_morning_blue_edge_glow.mp4", "type":"light_assets", "subtype":"morning_blue_edge_glow", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/L06_pew_light_shaft.mp4", "type":"light_assets", "subtype":"pew_light_shaft", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/L07_marble_light_sweep.mp4", "type":"light_assets", "subtype":"marble_light_sweep", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/L08_dust_gold_shaft_02.mp4", "type":"light_assets", "subtype":"dust_gold_shaft_02", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/L09_morning_blue_edge_glow_02.mp4", "type":"light_assets", "subtype":"morning_blue_edge_glow_02", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/L10_slate_window_light_02.mp4", "type":"light_assets", "subtype":"slate_window_light_02", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/V01_film_grain_fine.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine", "blend_hint":"overlay" }
{ "public_path":"flowers/overlay/V02_warm_light_noise.mp4", "type":"vfx_overlays", "subtype":"warm_light_noise", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/V03_film_grain_fine_02.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine_02", "blend_hint":"overlay" }
{ "public_path":"flowers/overlay/V04_warm_light_noise_02.mp4", "type":"vfx_overlays", "subtype":"warm_light_noise_02", "blend_hint":"screen" }
{ "public_path":"flowers/overlay/V05_slate_glitch_min.mp4", "type":"vfx_overlays", "subtype":"slate_glitch_min", "blend_hint":"screen" }
```

**検算:** 15 + 10 + 5 = 30 ✓。runtime で `asset_id`/`path`/`sha256`/`license`/`eyeballed_content`/`qc` を埋める。**overlay は `cuts[].src` に出さない。★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない。scanline/CRT/vignette-wash の overlay を選ばない。** 発色は B が accent `#B98A33`（dust-gold）/slate `#5C6670` に寄せる想定・morning-blue の light（L05/L09）は保釈以降/close 用のみ。他話色（EP41 sodium gold/EP42 blue/EP43 amber/EP44 teal/EP45 crimson/EP46 green/EP47 violet/EP49 plum/EP50 cyan/EP52 evidence-indigo）を選ばない。

---

# 5. A-1: SDXL 静止画のバッチ生成（210本 × 1枚・バリエーション0）— ★全210行 literal プロンプト同梱

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-054-flowers/04_scenes/ai_prompts.v001.md   ← A が §5.9 の形式で書く（本書 §5.6/§5.11/§5.12/§8.1a を転記）
出力:  H:\pd-media\assets\ai\flowers\S<NNN>.png（+ remotion/public/flowers/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★210本の構成＝3レーン（EP52 §5.13 の owner directive をネイティブ実装）

- **object/symbolic レーン（113枚）＝ `[STYLE]`+`[NEG]`（人物なし）:** counter tally・jury chairs・strike card・storefront of absence・four chairs・courthouse/prison・docket・waveform 等。
- **★HP 匿名人物レーン（85枚＝40%・R3+ owner directive 2026-07-26 で 57→85）＝ `[HSTYLE]`+`[HNEG]`:** 背向き/影/silhouette/hands・adults only・非識別。該当 S-range は §5.6 で `★HP` と明記。
  **★HP 85枚の全数（機械照合用・[HSTYLE] 行数と一致すること）:**
  ACT1×21 = S017 S018 S020 S021 S033 S034 S035 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 ／
  ACT2×24 = S062 S066 S068 S069 S071 S076 S078 S089 S092 S093 S094 S095 S096 S097 S098 S099 S100 S101 S102 S103 S104 S105 S106 S107 ／
  ACT3×17 = S112 S114 S115 S118 S129 S141 S142 S143 S144 S145 S146 S147 S148 S149 S150 S151 S152 ／
  ACT4×21 = S157 S158 S159 S174 S175 S176 S177 S178 S179 S180 S181 S182 S183 S184 S185 S186 S187 S188 S189 S190 S191 ／
  ACT5×2 = S204 S206 → **合計 85**。
  **★anti-samey variety matrix（owner: 似たような画像を作らない・全85枚に適用）:** ①ショット距離（macro hands／medium／full／wide crowd／extreme long を混在）②ポーズ（seated/standing/walking/filing/reaching/sweeping/robing/singing/waiting）③アングル（frontal-silhouette/behind/side/overhead/high-corner/low）④年齢（elderly sweeper・grandmother hands・young researchers・mixed gallery）⑤wardrobe（apron/Sunday suit/choir robe/shirtsleeves/uniform/coats+hats）⑥lighting-per-act（ACT1 dust-gold 昼/朝/dusk・ACT2 oak warm+slate・ACT3 slate・ACT4 lamp gold+slate→blue・ACT5 morning blue）⑦setting（street/church/courtroom/records/prison/polling/marble）。**同一の subject+composition+lighting の組を2枚作らない**（例: 「backs at a table」は S145=陪審団クラスタ／S157=overhead 両手×2 のように必ず2軸以上ずらす）。近似が出たら §6.3 でプロンプトを直して再生成。phash 監視クラスタは §6.1 Q4。
- **★F 可視感情顔レーン（12枚）＝ `[FSTYLE]`+`[FNEG]`（owner 2026-07-25 directive・§5.13）:** 非実在の見える感情顔（medium close-up 30–45%・dark cinematic 背景）。該当 S-range は §5.6 で `★F` と明記。
- **HARD BAN（3レーン共通・不変）: 実在人物 likeness ゼロ・被害者/暴行/遺体/現場ゼロ・識別可能な未成年ゼロ・可読テキストゼロ・別容疑者示唆ゼロ。**
- ★counter motif の注意: 画像内は**抽象の tally 状ストローク（彫り込まれた光の縦画）**まで。**読める Roman numeral のタイポは B が Remotion/AE で重ねる**（R-READABLE 保護）。

## 5.3 共通スタイル `[STYLE]`（object/symbolic 113 ＋ 抽象 i2v 種に連結・DESIGN §1 と一字一致）

```
, cinematic still, somber documentary grade, Mississippi July heat rendered in dust-gold key light as the dominant note, warm near-black ink institutional gravity, death-row slate gray-blue as the cold counter-note, a single pale free-air morning blue reserved only for release and ending beats, courtroom oak and small-town brick textures, dust motes hanging in light shafts, a furniture storefront rendered as quiet absence never any crime, four straight-back chairs one smaller as the victims held in dignity, an empty twelve-chair jury box as the film's battleground, an unreadable smeared name card with a heavy strike line as the mechanism image, carved tally strokes of light accumulating like a count, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, backs and hands and objects only
```

> **EP39〜EP53 の色語（1語も含めない）:** electric blue / sodium prison gold（EP41）/ porch-amber / teal-green hospital / crimson kitchen / forest-green / civil-violet two-lane Texas road pickup（EP47）/ somber-plum Utah（EP49）/ steel-cyan（EP50）/ cold forensic evidence-blue・green van・bandana（EP52）。**EP54 の色は Mississippi dust-gold `#B98A33` ＋ death-row slate `#5C6670` ＋ 保釈以降のみ free-air morning blue `#7FA8C9`。** ★EP41 の「監獄の gold」と混同しない（EP41=ナトリウム灯の橙・廊下、EP54=乾いた砂金色の熱と法廷オーク）。EP52 の evidence 引き出し/バンダナ/緑バンの絵柄を1枚も作らない。

## 5.4 共通ネガティブ `[NEG]`（各 `Avoid:` の後に全文付ける・A/B 同一）

```
text, words, letters, numbers, roman numeral typography, captions, watermark, logo, readable document, legible indictment, legible jury list, legible name card, legible newspaper, legible ballistics report, legible tally board, legible date, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, front-facing person, Curtis Flowers, Doug Evans, Odell Hallmon, Bertha Tardy, Derrick Stewart, James Bibbs, victim, murder victim, dead body, corpse, shot person, wounded person, assault, murder scene, crime scene tape, chalk outline of a body, violence, blood, gore, injury, gun firing, muzzle flash, pistol in hand, identifiable child, teenager's face, child's belongings at a crime scene, sexual content, nudity, re-enactment, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, forensic evidence-blue drawer, green van, blue bandana, milky haze, foggy wash, scanline, CRT texture, vignette wash
```

> 文字/紙面が必要な絵は「blurred into an unreadable smear」で判読不能に。**被害者・暴行・遺体・凶器・現場・可読の偽公文書・別容疑者示唆を NEG で明示抑制。** この `[NEG]` は object 113 ＋ 抽象 i2v 種にのみ使う。**人物ビート（§5.11 H・§5.13 F・§5.12 thumb）には使わない**（人物を弾くため）。H は `[HNEG]`・F は `[FNEG]`・thumb は `[TNEG]`。

## 5.5 プロンプトの絶対ルール（210本すべてに適用）

- **3レーン厳守（§5.2）**: `★HP`/`★F` マークのない S番号はすべて object/symbolic（人物なし）。
- **可読文字なし。** 文書/新聞/名簿/数字/日付/ロゴを描かない。tally は抽象ストロークのみ。
- **被害者・暴行・殺害・遺体・現場・凶器・規制線を一切描かない。** 店内は absence のみ。Hallmon の事件は「3つの灯り」のみ。
- **Flowers の innocence（制約1）:** Flowers が犯人に見える絵（店へ歩く男・銃を持つ手）を作らない。route は「再構成が崩れる」抽象のみ。
- **Evans の記録の範囲（制約4）:** prosecutor stand-in は非識別 silhouette・記録上の行為の象徴のみ。処罰/資格喪失を示唆する絵を作らない。
- **別容疑者示唆ゼロ（制約5）:** 「立ち去る謎の男」「暗がりの真犯人」類の画を作らない。unsolved は「答えのない count」「空の椅子」で。
- **dust-gold `#B98A33` 基調・slate `#5C6670` は row/年月・free-air blue `#7FA8C9` は S171 以降の該当 motif（保釈/自由/ending）のみ**（§5.6 の per-act motif で指定）。
- **★footage treatment は bleed/parallax/duotone/focus（DESIGN §1）。depth 前提の絵作りをしない。**
- **dochighlight を作らない・書かない。** milky wash / scanline を描かない。

### 5.5a ★★ 反復禁止ルール（R3++++ owner directive 2026-07-26・BINDING・全210行に適用）★★

> **背景:** Codex は1発で決まる。同じ motif の近似バリエーションを量産すると視聴者が飽きる（機械的な繰り返しの禁止）。§5.6 はこのルール適用済み＝**同状態の再撮 37行を新規 distinct scene に転換済み**（lane 不変・S番号不変・counts 不変）。

1. **1ビート内の同一 motif は最大2バリエーション。** 3枚以上並べない（例: hook の tally は S001/S005 の2枚のみ）。
2. **幕をまたぐ再登場は必ず可視の STATE CHANGE を持つ。** 同状態の再撮は禁止。各再登場プロンプトに state-change 句を明記する。
   - tally I–VI（本作の SPINE）: **1 trial = 1 state**（ストローク数の増加／reversal での亀裂 S084→S085→S086／trial6 完成 S130／SCOTUS で崩壊 S173／ending で未解決のまま残存 S200→S203）。
   - jury box: 台帳の構成変化をそのまま鏡映（S007 空 → S073 12-0 → S074 11-1 → S119 7-5 → S122 9-3 → S209 at rest）。
   - four chairs: S028/S029 warm light → S196 morning blue。storefront: S019/S022 1996 → S116 years later。four lamps: S024→S025 → S202 porch lights。
3. **Codex one-shot 原則:** 再生成は QC fail（§6.3）の時のみ。variants から選ぶ運用（pick-from-variants）は禁止（§0.1 の 1シーン1枚・バリエーション0 と同義）。

**R3++++ 転換 37行（旧 motif → 新 scene・lane 不変）:** ACT0: S002 tally→gap-in-the-wall／S003 tally→water tower dusk／S004 tally→six aged transcripts／S006 tally→newspaper bundle／S008 jury chairs→church piano／S009 jury chairs→stenotype at rest／S011 strike cards→empty record folder／S012 strike cards→crossroads dawn／S015 tally latent→empty witness stand。ACT1: S023 store aisle→price tags in AC draft／S026 register→back-office rotary phone／S030 chairs overhead→store keys／S031 chairs doorway→adding machine／S053(HP) hymnal pew→guitar case into trunk。ACT2: S063 courthouse facade→venue highway／S064 clock tower→Parchman guard tower distant／S066(HP) door queue→gallery paper fans／S075 shadowed chair close→jury wheel drum／S076(HP) seated jurors→stenotype hands／S077 box door ajar→courthouse clockwork gears／S080 card stack→empty exhibit easel／S082 falling card→marble appellate staircase／S083 graphite macro→courtroom reset／S087 gold dust residue→lit kitchen window／S093(HP) same silhouette ¾→jury-pool feet／S094(HP) pacing back→car radio at dusk／S104(HP) corridor escorts→post-office letters。ACT3: S116 cell window seasons→storefront years later／S124 armrest close→deliberation door ajar／S125 chair overhead→sun-faded case folder。ACT4: S163 tall bar→reporters' yarn corkboard／S168 static wall→microfilm reader。ACT5: S197 small chair close→empty choir risers night／S198 chairs overhead→new brass key／S199 chairs light→archive boxes wired glass／S201 strokes reflected→sealed case box／S202 strokes fading→four porch lights。

## 5.6 ★全210行 literal プロンプト（幕別 motif・S番号確定・このまま `ai_prompts.v001.md` へ転記）

> 形式は §5.9 のパーサ契約（2行1組）。`[STYLE]`/`[NEG]`/`[HSTYLE]`/`[HNEG]`/`[FSTYLE]`/`[FNEG]` は §5.3/§5.4/§5.11/§5.13 の全文をその位置に**展開して**書くこと（プレースホルダのまま渡さない）。

### ACT 0 — HOOK + OPENING（15枚・S001–S015・全て object）
**hook_count_and_town — 6 — S001–S006**（tally 2: S001 also_thumb hook signature／S005 fracture 予告・★R3++++ 2026-07-26 de-repetition: S002/S003/S004/S006 を新規 distinct scene に転換）
```
- `S001.png`
Six tall carved strokes of dust-gold light accumulating left to right across a warm near-black field like tally scars seared into the dark, the count itself as the image, abstract, no letterforms, no people, no readable text [STYLE] Avoid: [NEG]
- `S002.png`
A monumental dark wall filling the frame edge to edge, one narrow vertical breach cut through it spilling dust-gold light onto worn stone, the gap in the law rendered as architecture, abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `S003.png`
A small-town Mississippi water tower silhouetted against a dust-gold dusk sky, dark tank and thin legs above rooftops and July trees, heat still rising off the shingles, period detail, no people, no readable signage, no readable text [STYLE] Avoid: [NEG]
- `S004.png`
Six thick bound trial transcripts stacked on dark oak, each volume in a different age of paper from crisp to yellowed to brittle, spines blurred into unreadable smears, one warm lamp glow, a quarter-century in a single stack, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S005.png`
A row of six carved light strokes shuddering with hairline fractures spreading through them, the count about to fail, dust-gold against warm near-black, abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `S006.png`
A twine-bound bundle of 1990s newspapers dropped on a dark storefront step before dawn, every front page blurred into an unreadable smear, streetlamp glow and long shadows, a town saturated with one story, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
```
**jury_foreshadow_and_before — 3 — S007–S009**（jury box 1: S007・R3++++ 転換: S008 church piano／S009 stenotype at rest）
```
- `S007.png`
An empty twelve-chair jury box in deep darkness with a single chair caught in one dust-gold shaft of light, oak wood grain, quiet menace of an argument not yet made, no people, no readable text [STYLE] Avoid: [NEG]
- `S008.png`
An old upright piano in the corner of a small church, worn ivory keys catching warm morning light, a closed hymnal on the music rest blurred unreadable, the life of a gospel singer before any of it, no people, no legible characters, no readable text [STYLE] Avoid: [NEG]
- `S009.png`
A court stenography machine standing silent on its tripod in an empty dark courtroom at night, narrow keys unlabeled and worn blank, a thin slate shaft across it, the device that will hold every number, no people, no legible characters, no readable text [STYLE] Avoid: [NEG]
```
**strike_foreshadow_and_record — 3 — S010–S012**（strike card 1: S010・R3++++ 転換: S011 empty record folder／S012 crossroads dawn）
```
- `S010.png`
A single paper name card lying on dark oak, its writing blurred into an unreadable smear, a heavy dark pencil line struck through it, one cold slate edge of light, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S011.png`
A single manila case folder lying open on dark oak, completely empty inside, its tab blank, one clean shaft of dust-gold light across the emptiness, a record with nothing in it, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S012.png`
A small Mississippi town's central crossroads at first light, one traffic signal hanging from a cable over the empty intersection, brick corners and awnings still dark, the crossroads of the state, no people, no readable signage, no readable text [STYLE] Avoid: [NEG]
```
**opening_field — 3 — S013–S015**（R3++++ 転換: S015 empty witness stand — S068 の occupied stand と before/after の evolution pair）
```
- `S013.png`
An abstract field of Mississippi heat, dust-gold light breathing over warm near-black like air over July asphalt, minimal and cinematic, a base for opening type, no people, no readable text [STYLE] Avoid: [NEG]
- `S014.png`
A flat Mississippi horizon at first light, dark fields under a thin band of dust-gold sky, immense stillness, no people, no buildings close, no readable text [STYLE] Avoid: [NEG]
- `S015.png`
An empty witness stand in a vast dark courtroom, one narrow dust-gold shaft on the vacant chair and the worn rail, the seat every number in this story must pass through, no people, no readable text [STYLE] Avoid: [NEG]
```

### ACT 1 — THE CRIME AND THE CHOOSING（45枚・S016–S060）
**front_street_1996 — 6 — S016–S021**（object 2: S016/S019・★HP 4: S017/S018/S020/S021 — Winona town life・R3+ 2026-07-26 転換）
```
- `S016.png`
A quiet 1996 Mississippi small-town main street in July midday heat, brick storefronts and awnings, dust-gold light and long shadows, a period sedan parked far away, no people, no readable signage, no readable text [STYLE] Avoid: [NEG]
- `S017.png`
Anonymized townspeople as small sun-struck figures crossing a 1996 Mississippi main street at midday, seen from far down the block, summer hats and dresses rendered as distant non-identifiable shapes, dust-gold glare and long shadows, all backs and distance, no faces, no readable signage, no readable text [HSTYLE] Avoid: [HNEG]
- `S018.png`
An anonymized shopkeeper in an apron seen squarely from behind cranking open a striped storefront awning in early 1990s morning light, warm gold rim on the shoulders, a water tower distant down the street, no face, no readable signage, no readable text [HSTYLE] Avoid: [HNEG]
- `S019.png`
A furniture store's display window seen from the sidewalk at a distance, sofas and lamps behind sun-struck glass, ordinary July commerce a moment before history, no people, no readable signage, no readable text [STYLE] Avoid: [NEG]
- `S020.png`
An anonymized elderly resident seen in full figure from behind sweeping the brick sidewalk in front of a small-town shop at morning, broom mid-stroke, long shadow down the side street, dust hanging in the raked light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S021.png`
Two anonymized neighbors standing in quiet conversation under a storefront awning at first dark, warm window glow and streetlamp halos wrapping their silhouettes, seen from across the street in humid July air, unhurried town life, no faces, no readable signage, no readable text [HSTYLE] Avoid: [HNEG]
```
**storefront_absence — 6 — S022–S027**（object・被害者/現場を一切描かない・four lamps S024→S025 は state-change pair・R3++++ 転換: S023 price tags in the draft／S026 back-office telephone）
```
- `S022.png`
A furniture store interior rendered as pure quiet absence, empty aisles between sofas and dressers in dim dust-gold light, nothing disturbed, nothing shown, a held breath of a room, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
- `S023.png`
Inside the furniture showroom, paper price tags hanging from sofa arms and lamp shades swaying faintly in the draft of a rattling window air conditioner, every tag blurred into an unreadable smear, dust-gold light through the display glass, July commerce mid-breath, no legible characters, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
- `S024.png`
Four small warm points of lamp light inside a dim furniture store, seen wide and far, the moment before they matter, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
- `S025.png`
The same four lamp points with one already faded to slate gray, a store interior dimming, symbolic and restrained, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
- `S026.png`
A wall-mounted rotary telephone in the store's small back office, receiver at rest, cord hanging still beside a desk of papers blurred into unreadable smears, bright nine-o'clock morning light through a dusty window, the ordinary call before everything, no legible characters, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
- `S027.png`
The furniture store's front door from inside, July light burning white through the glass into a dark hushed interior, threshold between an ordinary morning and after, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
```
**four_chairs — 4 — S028–S031**（object・chairs 2: S028 also_thumb／S029 close・R3++++ 転換: S030 store keys＝Bertha の店／S031 adding machine＝Carmen の帳簿。被害者は象徴でのみ）
```
- `S028.png`
Four straight-back wooden chairs standing together in a warm shaft of dust-gold light against deep darkness, one chair slightly smaller than the rest, held with dignity like a memorial, no people, no readable text [STYLE] Avoid: [NEG]
- `S029.png`
Close on the smaller of four wooden chairs in soft warm light, its seat empty, grain and dust, grief rendered as furniture, no people, no readable text [STYLE] Avoid: [NEG]
- `S030.png`
A worn ring of brass keys on a leather fob hanging from the lock of the store's heavy back door, decades of hands polished into the metal, warm dust-gold light, a family business held in hardware, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
- `S031.png`
A period mechanical adding machine on a bookkeeper's wooden desk, its blank paper roll curling gently over the edge, pencil cup and reading glasses beside it, morning light and dust, the store's quiet arithmetic, no legible characters, no numbers visible, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
```
**gospel_pew_light — 4 — S032–S035**（object 1: S032・★HP 3: S033–S035 — gospel-choir silhouettes・R3+ 2026-07-26 転換）
```
- `S032.png`
A small wooden Mississippi Baptist church exterior in morning light, white clapboard against a wide sky, modest steeple, dust-gold warmth, no people, no readable signage, no readable text [STYLE] Avoid: [NEG]
- `S033.png`
A gospel choir seen from the side of the choir loft as a row of robed anonymized silhouettes mid-hymn, faces lost to shadow and backlight, long shafts of warm morning light crossing the risers, worn pews below, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S034.png`
A pair of anonymized weathered adult hands holding an open hymnal in a pew, pages blurred into unreadable smears, warm dust-gold light across paper and knuckles, hands only, no face, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `S035.png`
An anonymized choir member seen from behind pulling a deep red-brown robe over Sunday clothes in a dim church back room, mid-gesture, dust-gold edge light on the fabric and shoulders, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
**thin_case_objects — 8 — S036–S043**（object・「証拠の薄さ」を象徴で・銃も route も断定しない）
```
- `S036.png`
The faint chalk-like outline of a pistol shape dissolving into dust on a dark evidence table, the weapon that was never found rendered as an absence, abstract, no real gun, no people, no readable text [STYLE] Avoid: [NEG]
- `S037.png`
One single microscopic mote of dust glowing in a narrow slate light shaft over darkness, the entire particle of proof, vast emptiness around it, abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `S038.png`
A sneaker tread pattern pressed faintly in pale dust on dark flooring, already blurring at the edges as if evaporating, a common shoe in a common size, non-graphic, no blood, no people, no readable text [STYLE] Avoid: [NEG]
- `S039.png`
A dawn sidewalk route across a small town rendered as torn misaligned photographic fragments that no longer line up, a path assembled from memory coming apart, abstract collage, no people, no readable text [STYLE] Avoid: [NEG]
- `S040.png`
A dirt road at dawn dissolving into heat haze, its far end erased into white, the state's route ending in nothing, no walking figure, no people, no readable text [STYLE] Avoid: [NEG]
- `S041.png`
A public notice board with a single sheet blurred into an unreadable smear, dusk light, the shape of a reward without a word of it, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S042.png`
A dark garment-factory parking lot seen from far across the asphalt at early morning, a few period cars as distant shapes, sodium-free dust-gold dawn, no people, no license plates, no readable text [STYLE] Avoid: [NEG]
- `S043.png`
A car's side window in deep shadow at a distance, nothing visible within, the question of what was taken left unanswered, cold slate reflections, no person, no license plate, no readable text [STYLE] Avoid: [NEG]
```
**town_split_frame — 4 — S044–S047**（object 1: S044・★HP 3: S045–S047 — 分断の町を人で・R3+ 2026-07-26 転換・dignity 必須/caricature 禁止）
```
- `S044.png`
Railroad tracks running straight through a small Mississippi town, one side in warm dust-gold light and the other fallen into cold slate shadow, a town divided by a line, no people, no readable text [STYLE] Avoid: [NEG]
- `S045.png`
Two small groups of anonymized townspeople on opposite sidewalks of one small-town street, all backs and distant non-identifiable shapes, one sidewalk in warm dust-gold light and the other in cold slate shadow, the divide rendered in people and light with dignity, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S046.png`
Two small congregations of anonymized figures dispersing outside two modest churches at opposite ends of a wide small-town street at dusk, seen from very far as warm silhouette clusters under one shared sky, no faces, no readable signage, no readable text [HSTYLE] Avoid: [HNEG]
- `S047.png`
Distant anonymized figures on a small-town main street at noon wavering in rising heat shimmer like mirages, forms bent by hot air into unreadable shapes, dust-gold glare, division rendered as distortion, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP investigators_choosing — 4 — S048–S051**
```
- `S048.png`
Anonymized investigators seen only from behind in shirtsleeves before a corkboard of photographs and papers all blurred into unreadable smears, one hand pinning a blank card at the center, cold lamplight, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S049.png`
An anonymized detective's hands seen from above sliding one blank smeared card to the center of a bare desk, the choosing rendered as a gesture, warm lamp against ink shadow, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S050.png`
A lone anonymized figure in silhouette at the end of a dim small-town police corridor, hat and shoulders only, institutional light, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S051.png`
Anonymized adult hands writing on a legal pad under a desk lamp, the writing an unreadable smear, a case assembling itself, seen over the shoulder so no face reads, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP gospel_family — 3 — S052–S054**（R3++++ 転換: S053 guitar case into the trunk＝巡回する家族グループ。S034 の hymnal hands との同型反復を解消）
```
- `S052.png`
A gospel choir of anonymized adult figures seen entirely from behind, backlit to warm silhouettes mid-song in a small church, hands lifted, dust-gold light flooding past them, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S053.png`
An anonymized man in Sunday clothes seen from behind lifting a battered guitar case into the open trunk of a period sedan outside a small church at dawn, gravel churchyard and dew, a family known across the county for its music heading out to sing, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S054.png`
A small congregation of anonymized backs in wooden pews under shafts of warm light, heads bowed, community rendered without a single face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP arrest_slate — 4 — S055–S058**（Flowers 示唆は背向き非識別のみ・有罪含意なし）
```
- `S055.png`
An anonymized man seen only from behind at a slate-gray institutional doorway, escorted by two anonymized officers also from behind, dignified posture, cold light swallowing the warm street behind them, no faces, no likeness, no handcuff closeup, no readable text [HSTYLE] Avoid: [HNEG]
- `S056.png`
A county jail corridor in cold slate light with two anonymized figures walking away from camera far down its length, scale of the institution over the individual, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S057.png`
An anonymized officer's back beside a period patrol car at night, red-blue glow kept far and soft on brick walls, restrained, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S058.png`
A booking-hallway bench in slate light with one anonymized man's back and bowed head at its far end, small in frame, presumption of innocence held in the composition's dignity, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
**★F visible_faces_act1 — 2 — S059–S060**（§5.13 の lane 定義に従う）
```
- `S059.png`
F01: a clearly illustrative semi-painterly face of a generic grieving Southern townsperson, middle-aged, hollow shock and sorrow, medium close-up about forty percent of frame height, eyes upper third, dramatic warm key and rim light against a dark blurred main-street dusk, resembling no real individual, adults only [FSTYLE] Avoid: [FNEG]
- `S060.png`
F02: a photoreal generic investigator's hard, already-decided face in half shadow, jaw set, medium close-up about thirty-five percent of frame height, cold slate key light with a warm rim, dark blurred office behind, resembling no real individual, adults only [FSTYLE] Avoid: [FNEG]
```

### ACT 2 — TRIAL, REVERSE, REPEAT（50枚・S061–S110・engine・最密）
**courthouse_and_venues — 6 — S061–S066**（object 2 facade states: S061 home county／S065 Gulf Coast venue change・★HP 2: S062 steps crowd／S066 gallery fans(R3++++ 転換)・R3++++ 転換: S063 venue highway／S064 Parchman guard tower distant）
```
- `S061.png`
A Mississippi county courthouse with white columns under hard July light, oak trees and a still lawn, dust-gold and deep shade, institutional permanence, no people, no readable signage, no readable text [STYLE] Avoid: [NEG]
- `S062.png`
A crowd of anonymized townspeople seen entirely from behind gathered on courthouse steps waiting for word, hats held in hands, raking afternoon light throwing their long shadows up the stairs, trial day as a town event, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S063.png`
A long empty two-lane highway running dead straight across flat Mississippi cotton country in gray first light, mile markers small and unreadable, the hundred miles a trial travels when its own town has already decided, no people, no license plates, no readable text [STYLE] Avoid: [NEG]
- `S064.png`
A lone prison guard tower on the horizon at dusk, seen from a public road at extreme telephoto compression, heat shimmer over cotton rows between, a small dark vertical against a wide pale evening, period Mississippi, restrained, no people, no gore, no readable text [STYLE] Avoid: [NEG]
- `S065.png`
A Gulf Coast courthouse exterior with palms at frame edge, brighter flatter light, the same architecture in a changed venue, the road-show of trials moving town to town, no people, no readable signage, no readable text [STYLE] Avoid: [NEG]
- `S066.png`
Anonymized hands working paper funeral-home fans in a sweltering courtroom gallery, seen close over a shoulder from behind, the fans' printed faces blurred into unreadable smears, July heat and dust-gold window light, a town sitting through its own trial, no faces, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
```
**courtroom_oak — 6 — S067–S072**（object 3: S067/S070/S072・★HP 3: S068/S069/S071 — 法廷ベンチと傍聴席・R3+ 2026-07-26 転換）
```
- `S067.png`
An empty 1990s Southern courtroom in warm oak and dust-gold window light, benches and rail and bar all silent, frontal symmetry, no people, no readable text [STYLE] Avoid: [NEG]
- `S068.png`
An anonymized witness stand-in seated small and distant in the witness chair, seen from the far end of the gallery, face lost entirely to distance and shadow, one pale shaft of light on the worn oak rails and dust hanging in it, the chair the whole case sits on, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S069.png`
Two anonymized figures seated side by side at the defense table seen squarely from behind, one suited and one in shirtsleeves, upright and motionless in a cold slate pool of light while the courtroom around them holds warm gold, isolation rendered in color, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S070.png`
The judge's bench looming empty in dim light, dark oak mass against a pale wall, authority as furniture, no people, no readable text [STYLE] Avoid: [NEG]
- `S071.png`
Gallery benches filled with anonymized spectators seen from a high rear corner of the courtroom, rows of hats, gray hair and Sunday collars receding into warm shadow, mixed ages rendered non-identifiable, dust in the window light, the town's seats taken, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S072.png`
Extreme close on courtroom oak grain scarred by decades of use, one bright line of dust-gold light across it, texture as history, no people, no readable text [STYLE] Avoid: [NEG]
```
**jury_box_maps — 6 — S073–S078**（object 2 chair-map states: S073＝12-0 の第1 seating／S074＝11-1 へ state change・★HP 2: S076 stenotype hands(R3++++ 転換・S009 の at-rest との evolution pair)／S078 filing in・R3++++ 転換: S075 jury wheel／S077 clockwork gears。陪審構成は台帳値のみ・人物側には数の配分を描かない）
```
- `S073.png`
Twelve empty jury chairs all lit the same flat pale white-gold, the first trial's seating with no chair different from another, uniformity as an argument, frontal scoreboard composition, no people, no readable text [STYLE] Avoid: [NEG]
- `S074.png`
Twelve empty jury chairs with exactly one chair fallen into cold slate shadow while eleven hold warm light, the uniform row of the first seating now broken by a single dark seat, the arithmetic of a seating rendered in light, no people, no readable text [STYLE] Avoid: [NEG]
- `S075.png`
An old wooden jury-wheel drum on a courthouse table, hand crank at rest, small folded paper slips visible through its slot each blurred into an unreadable smear, cold slate light on the barrel, the machine that draws names before anyone can strike them, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S076.png`
An anonymized court reporter's hands working the narrow blank keys of a stenotype machine mid-testimony, folded paper accumulating in the tray, warm oak courtroom light, seen over the shoulder so no face reads, the record growing word by word, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `S077.png`
Heavy antique clockwork gears turning in the dark behind a courthouse clock face seen from inside the tower, brass teeth meshing, dust-gold light glowing through the translucent dial with its numerals only soft shapes, the machine that keeps running, no legible numerals, no people, no readable text [STYLE] Avoid: [NEG]
- `S078.png`
A line of anonymized Black and white jurors filing into the jury box, a dignified procession of backs and shoulders seen from behind the last chair, faint motion blur in the nearest figure, oak half-light, the seating that decides everything, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
**strike_mechanism — 5 — S079–S083**（object・strike 2: S079 the act／S081 pattern emerging・R3++++ 転換: S080 empty exhibit easel／S082 marble appellate staircase／S083 courtroom reset）
```
- `S079.png`
A heavy dark pencil line mid-stroke across an unreadable smeared name card, motion blur in the stroke, the strike as an act, macro, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S080.png`
An empty wooden exhibit easel standing in the well of a dark courtroom, holding nothing, one dust-gold shaft falling where proof should be, oak gloom around it, an argument made of air, no people, no readable text [STYLE] Avoid: [NEG]
- `S081.png`
A wall beginning to fill with struck unreadable cards pinned in rows, dust-gold light grazing them, the pattern emerging, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S082.png`
A vast marble courthouse staircase turning upward into cold gloom, worn brass rail and a single high band of slate window light, the long climb every verdict in this story must make, no people, no readable text [STYLE] Avoid: [NEG]
- `S083.png`
A courtroom reset overnight for a new trial, chairs squared to the counsel tables, fresh unmarked legal pads and refilled water pitchers, everything identical again in pre-dawn slate light, the same room ready to run the same play, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
```
**tally_cracks — 4 — S084–S087**（object・破棄＝ストロークの亀裂。cracks 3: S084 一本目/S085 二本目/S086 三本目＝1 trial 1 state の spine 進化（reversal 2000/2003/2007）・R3++++ 転換: S087 lit kitchen window）
```
- `S084.png`
A single carved stroke of dust-gold light fracturing down its length, the first of the six to break, cracks glowing cold slate, a verdict failing, abstract, no letterforms, no people, no readable text [STYLE] Avoid: [NEG]
- `S085.png`
Two carved light strokes side by side, both split by slate fractures, the second failure echoing the first, warm near-black field, abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `S086.png`
A third carved stroke shattering into slate shards that hang suspended, the strongest break yet, abstract violence of light only, no people, no readable text [STYLE] Avoid: [NEG]
- `S087.png`
One lit kitchen window far down a dark Winona street at night, every other house asleep, moths in the small warm glow, a question staying up late, no people, no readable text [STYLE] Avoid: [NEG]
```
**reserve_counts — 4 — S088–S091**（object 3: S088/S090/S091・★HP 1: S089・R3+ 2026-07-26 転換）
```
- `S088.png`
Four plain case folders in a dim drawer, one pulled halfway out into dust-gold light while three wait in shadow, the counts held in reserve, unreadable labels, no people, no readable text [STYLE] Avoid: [NEG]
- `S089.png`
An anonymized courthouse clerk's back pushing a cart of boxed files down a tall records-room aisle, one cold slate strip of light overhead, decades of paper looming on either side, the machine's stagehand, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S090.png`
A drawer of docket ledgers with spines blurred to unreadable smears, one thin band of warm light across them, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S091.png`
An old ballot box standing alone on a table in a dark room, one edge caught in dust-gold light, a foreshadowed verdict of another kind, no people, no readable text [STYLE] Avoid: [NEG]
```
**★HP prosecutor_and_pool — 4 — S092–S095**（NOT a likeness・非識別・podium 2: S092 full silhouette／S095 hands macro・R3++++ 転換: S093 jury-pool feet／S094 car radio at dusk）
```
- `S092.png`
An anonymized prosecutor stand-in at a courtroom podium seen squarely from behind, back-lit to a hard silhouette so no face can read, addressing an unseen jury, institutional power in posture alone, no likeness of any real person, no readable text [HSTYLE] Avoid: [HNEG]
- `S093.png`
A waiting row of anonymized prospective jurors framed strictly below the waist, period shoes and work boots on worn courthouse tile, folded summons papers held at knees blurred into unreadable smears, cold institutional light, the pool before the strikes, no faces, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `S094.png`
Anonymized hands tuning a period car radio at dusk, dial glow warm on fingers and dashboard, its numbers only soft unreadable shapes, a town parked and listening for a verdict, framed inside the car with no face in frame, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `S095.png`
Anonymized hands gripping both edges of a podium under one hard light, knuckles and cufflinks only, ownership of a room, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP courtroom_trials — 5 — S096–S100**
```
- `S096.png`
A 1997 Southern courtroom seen from the very back, anonymized jurors in the box and a gallery of spectators all rendered as non-identifiable backs and soft-focus shapes, warm oak and dust, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S097.png`
A courtroom gallery split down its center aisle, anonymized backs seated on both sides in different light, warm on one side and slate on the other, a town divided in pews, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S098.png`
An anonymized figure seen from behind at a defense table, upright and still, dwarfed by the room around him, cold slate pool of light, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S099.png`
A bailiff's anonymized silhouette by the courtroom doors, keys and stillness, warm light leaking under the door, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S100.png`
The moment a verdict lands rendered as anonymized gallery backs rising in unison, motion blur in shoulders, no faces anywhere, oak and dust-gold, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP appellate_court — 3 — S101–S103**
```
- `S101.png`
Nine anonymized robed figures as distant dark silhouettes behind a long elevated bench in marble gloom, the state's highest court as geometry, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S102.png`
A lone anonymized clerk's back walking a vast marble corridor carrying a box of files, echo rendered visually in scale, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S103.png`
Anonymized hands placing a bound opinion on a desk, its text an unreadable smear, one cold slate shaft of light, reversal as a quiet act of paper, no face, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP row_transfers — 4 — S104–S107**（R3++++ 転換: S104 post-office letters＝S056 の corridor 歩行との同型反復を解消・獄中の23年を外から支える手）
```
- `S104.png`
An anonymized woman's hands pressing a thick envelope into a brass mailbox slot at a small-town post office, the address blurred into an unreadable smear, rows of little brass box doors catching warm light, one letter of hundreds across the years, no face, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `S105.png`
A transport van's slatted window from outside with only darkness within, cold slate morning, movement between courtrooms and cells, no visible person, no license plate, no readable text [HSTYLE] Avoid: [HNEG]
- `S106.png`
Two anonymized guards' backs at a steel processing door, one hand raised to the buzzer, institutional choreography, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S107.png`
An anonymized man's back seated alone on a bench in a bare holding room, shoulders straight, small in the slate frame, the years beginning to stack, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
**★F visible_faces_act2 — 3 — S108–S110**
```
- `S108.png`
F03: a photoreal generic Southern prosecutor-archetype face, stern and certain at a podium, cold eyes past camera, medium close-up about thirty-five percent of frame height, hard key light and rim against dark oak blur, resembling no real individual and explicitly not any real district attorney, adults only [FSTYLE] Avoid: [FNEG]
- `S109.png`
F04: a photoreal generic middle-aged woman juror's uncertain face in three-quarter profile in the box, doubt held in the brow, eyes down and away, tight close-up about a quarter of frame height set off-center left, cool slate key with a faint warm fill, resembling no real individual, adults only [FSTYLE] Avoid: [FNEG]
- `S110.png`
F05: a clearly illustrative semi-painterly face of a generic wrongly accused young everyman in his late twenties, frontal under a harsh top light behind the courtroom rail, dread held in the set of the jaw, large close-up about sixty percent of frame height, deep shadow pooled under the brow, unmistakably a painted illustration resembling no real individual, adults only [FSTYLE] Avoid: [FNEG]
```

### ACT 3 — THE HUNG YEARS AND THE LIAR（45枚・S111–S155）
**parchman_slate — 7 — S111–S117**（object 4: S111/S113/S116/S117・★HP 3: S112/S114/S115 — death-row corridor figures／visitation・family waiting・R3+ 2026-07-26 転換。S117 は also_thumb＝object 不変。R3++++ 転換: S116 storefront years later＝「The store changed」・cell window は S113→S117 の 2-state evolution に整理）
```
- `S111.png`
A flat Mississippi prison complex seen from far across bare farmland, low buildings under an enormous slate sky, non-sensational and still, no people, no gore, no readable text [STYLE] Avoid: [NEG]
- `S112.png`
An anonymized corrections officer as a tiny distant silhouette walking the razor-wire fence line under an enormous slate sky, kept very far, geometry and scale over menace, non-sensational, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S113.png`
A single cell window as a pale slate rectangle in a dark wall, light without view, the row rendered as an aperture, no people, no readable text [STYLE] Avoid: [NEG]
- `S114.png`
An anonymized guard seated motionless at a small desk at the far end of a long slate death-row corridor, a single caged bulb above him, doors repeating into dark toward the camera, stillness as the job, institutional infinity, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S115.png`
Anonymized family members seated waiting on a bench in a bare prison visitation waiting room, a grandmother's folded hands and a man's bowed shoulders seen from behind, coats on laps, slate light through wired glass, patience measured in years, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S116.png`
The old furniture storefront years later, repainted in another color under a different awning, its new lettering blurred into an unreadable smear, the display window showing someone else's goods, the town moved on around what never resolved, no people, no legible characters, no readable text [STYLE] Avoid: [NEG]
- `S117.png`
A slate death-row cell window with the faint trace of many seasons crossing it at once, layered light like sediment, twenty-three years rendered as one quiet aperture, no person, no calendar, no readable text [STYLE] Avoid: [NEG]
```
**deadlock_faultsplit — 5 — S118–S122**（object 4: S119–S122＝7-5/9-3 の光の算術は不変・★HP 1: S118 — family waiting・R3+ 2026-07-26 転換）
```
- `S118.png`
An anonymized family group standing close together at the far end of a marble courthouse hallway during deliberations, seen from very far as one tight warm silhouette cluster against a tall window, arms held, the wait rendered as distance, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S119.png`
Twelve empty chairs around a table with seven caught in warm light and five in cold slate shadow, the deadlock rendered exactly, no people, no readable text [STYLE] Avoid: [NEG]
- `S120.png`
The frame itself split as two halves of one room straining apart along a hairline crack of light, abstract deadlock, oak and slate, no people, no readable text [STYLE] Avoid: [NEG]
- `S121.png`
A heavy rope pulled taut across darkness fraying at its center strand by strand, tension made physical, macro, no people, no readable text [STYLE] Avoid: [NEG]
- `S122.png`
Twelve chairs with nine in warm light and three in slate, a second arithmetic of a second seating, scoreboard composition, no people, no readable text [STYLE] Avoid: [NEG]
```
**holdout_chair — 4 — S123–S126**（object・Bibbs は椅子の象徴のみ・chair 2 states: S123 pulled into spotlight→S126 returned out of line・R3++++ 転換: S124 deliberation door ajar／S125 sun-faded case folder）
```
- `S123.png`
A single juror's chair pulled out of line into a hard cold spotlight on a dark floor, isolated from eleven others in shadow, the price of holding out, no people, no readable text [STYLE] Avoid: [NEG]
- `S124.png`
A jury deliberation-room door left ajar at the end of a dark courthouse hallway at night, a thin blade of cold light spilling across the floor from inside, the argument over without an answer, no people, no readable text [STYLE] Avoid: [NEG]
- `S125.png`
A manila case folder gone brittle and sun-faded on a courthouse windowsill, edges curled, its label bleached to nothing, fourteen years of light having passed through the same glass, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S126.png`
The chair returned to the jury box but left slightly out of line, its light gone slate, a message left in furniture, no people, no readable text [STYLE] Avoid: [NEG]
```
**trial6_clock — 4 — S127–S130**（object 3: S127/S128/S130・★HP 1: S129・R3+ 2026-07-26 転換）
```
- `S127.png`
A courtroom wall clock in dim oak shadow, its hands soft unreadable shapes barely moved, half an hour rendered as almost nothing, no numerals legible, no people, no readable text [STYLE] Avoid: [NEG]
- `S128.png`
A thin wedge of window light crossing a courtroom floor like a sundial's half-hour, oak and dust, time as the only witness, no people, no readable text [STYLE] Avoid: [NEG]
- `S129.png`
Two anonymized bailiffs' hands and forearms pushing the heavy oak courtroom doors closed from inside, the gap of warm light narrowing to a blade across their knuckles, finality as a gesture, hands only, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S130.png`
A sixth carved stroke of dust-gold light searing in fast beside five older scarred ones, the count completed, abstract, no letterforms, no people, no readable text [STYLE] Avoid: [NEG]
```
**hallmon_glass — 5 — S131–S135**（object・美化も lurid も禁止）
```
- `S131.png`
A dark human silhouette behind heavily ribbed prison visitation glass, shape without any face, slate light, the state's whole case as a blur behind glass, no likeness, no readable text [STYLE] Avoid: [NEG]
- `S132.png`
Plain manila folders stacking impossibly high on a small table in slate light, a career of charges rendered as paper, unreadable labels, no people, no readable text [STYLE] Avoid: [NEG]
- `S133.png`
A prison wall phone hanging on painted cinderblock in dim slate light, receiver at rest, the instrument of both the lie and the truth, no people, no readable text [STYLE] Avoid: [NEG]
- `S134.png`
An old ledger open with running tallies blurred into unreadable smears, one column absurdly long, a tab kept in favors, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S135.png`
The ribbed-glass silhouette again but closer and darker, the shape leaning toward the glass, menace held abstract and unglorified, no face, no likeness, no readable text [STYLE] Avoid: [NEG]
```
**three_lights_out — 3 — S136–S138**（object・Hallmon の被害者3人＝最大 dignity・暴力ゼロ）
```
- `S136.png`
Three small warm points of light in a vast dark field, steady and gentle, three lives rendered only as light, maximum dignity, no people, no violence, no readable text [STYLE] Avoid: [NEG]
- `S137.png`
The same three points of light guttering low, darkness pressing in, grief without depiction, abstract, no people, no violence, no readable text [STYLE] Avoid: [NEG]
- `S138.png`
The dark field after, three thin trails of fading warmth where the lights were, absence with weight, abstract, no people, no violence, no readable text [STYLE] Avoid: [NEG]
```
**tape_waveform — 2 — S139–S140**（object）
```
- `S139.png`
A small cassette recorder on a bare table in slate light, reels still, a phone handset beside it, the machine that will hold the truth, unreadable labels, no people, no readable text [STYLE] Avoid: [NEG]
- `S140.png`
An abstract audio waveform of pale slate light stretched across darkness with one violent spike mid-line, a sentence that changes everything rendered as signal, no words, no people, no readable text [STYLE] Avoid: [NEG]
```
**★HP years_inside — 4 — S141–S144**
```
- `S141.png`
An anonymized man seen from behind sitting on the edge of a bunk in a bare cell, face fully lost to shadow, small and upright in the slate frame, dignified and non-sensational, no gore, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S142.png`
A pair of anonymized hands resting through a food-slot of light, aged and patient, hands only, slate gray around one warm band, no face, no gore, no readable text [HSTYLE] Avoid: [HNEG]
- `S143.png`
Distant anonymized inmates as small still silhouettes across an empty prison yard, non-sensational, scale over incident, no faces, no gore, no readable text [HSTYLE] Avoid: [HNEG]
- `S144.png`
An anonymized visitor's back at ribbed visitation glass, hand raised to the pane, the years measured in glass thickness, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP hung_juries — 4 — S145–S148**
```
- `S145.png`
Anonymized jurors seen only as backs around a deliberation table, two clusters leaning apart, gulf of table between them, warm and slate split light, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S146.png`
An anonymized foreperson's hands folding a small note at the head of a jury table, the writing an unreadable smear, cold light, no face, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `S147.png`
Anonymized jurors filing out of a courtroom rendered as a line of backs in mixed warm and slate light, no agreement in their spacing, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S148.png`
An anonymized deputy's silhouette in a doorway watching the jury room, keys at the belt, quiet institutional pressure, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP witness_and_recorder — 4 — S149–S152**
```
- `S149.png`
An anonymized witness stand-in at the courtroom stand seen from behind and back-lit so no face reads, one hand raised, the single pillar of the case, no likeness of any real person, no readable text [HSTYLE] Avoid: [HNEG]
- `S150.png`
An anonymized inmate's back at a prison wall phone, shoulders hunched into the receiver, slate light, the call that unmakes four verdicts, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S151.png`
Two anonymized figures far apart on a prison tier walkway, distance and shadow between them, the alleged confession rendered as sheer distance, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S152.png`
Anonymized hands holding a small recorder toward ribbed glass, journalist's notebook beneath blurred unreadable, the truth being captured, no face, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
```
**★F visible_faces_act3 — 3 — S153–S155**
```
- `S153.png`
F06: a clearly illustrative semi-painterly face of a generic man in his fifties seen in forty-five-degree profile through prison visitation glass, years etched into it, grief without theater, a fluorescent strip reflected across the pane bisecting the composition, medium shot about a third of frame height right of center, cold green-gray key, unmistakably an illustration resembling no real individual, adults only [FSTYLE] Avoid: [FNEG]
- `S154.png`
F07: a clearly illustrative semi-painterly face of a generic lone holdout juror, frightened but resolute, chin lifted, medium close-up about thirty-five percent of frame height, one hard spotlight key against darkness, unmistakably an illustration resembling no real individual and not any real juror, adults only [FSTYLE] Avoid: [FNEG]
- `S155.png`
F08: a photoreal generic radio journalist's intent listening face lit by a console glow, headphones on, eyes fixed mid-revelation, medium close-up about thirty percent of frame height, dark studio blur behind, resembling no real individual, adults only [FSTYLE] Avoid: [FNEG]
```

### ACT 4 — THE NINTH INNING（40枚・S156–S195・climax・cascade）
**docket_books — 4 — S156–S159**（object 1: S156・★HP 3: S157–S159 — the count built by hands・R3+ 2026-07-26 転換）
```
- `S156.png`
A courthouse storeroom of tall shelves stacked with old docket books and boxes, dust hanging in one gold shaft, the raw material of the count, unreadable spines, no people, no readable text [STYLE] Avoid: [NEG]
- `S157.png`
Two pairs of anonymized hands at opposite sides of a huge open docket ledger seen from directly above, one finger tracing a smeared column while the other pair steadies a small recorder, browned pages blurred unreadable, warm lamp light, no faces, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `S158.png`
An anonymized archivist's back carrying a heavy bankers box of juror records down a dim aisle of stacked boxes, dust swirling in one gold shaft ahead, labels smeared unreadable, a quarter-century of paper, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S159.png`
Anonymized researchers' hands with sleeves rolled sorting loose index cards into piles across a work table in slate lamplight, every card an unreadable smear, the count being built by hand, no faces, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
```
**data_ignites — 4 — S160–S163**（object・数字は描かない＝抽象バーのみ・R3++++ 転換: S163 reporters' yarn corkboard＝S048 の 1996 corkboard が2018年に解体される evolution）
```
- `S160.png`
Two abstract vertical bars of light on darkness, one tall dust-gold and one short pale, a disparity rendered without a single numeral, clean data-graphic minimalism, no numbers, no people, no readable text [STYLE] Avoid: [NEG]
- `S161.png`
A field of small card-shapes scattered on dark, a large cluster struck through with slate lines and a small cluster untouched, pattern visible at a glance, abstract, no numbers, no people, no readable text [STYLE] Avoid: [NEG]
- `S162.png`
Rows of faint bar-glows rising across a dark field like a chart catching fire from left to right, dust-gold ignition, abstract analytics with no numerals, no people, no readable text [STYLE] Avoid: [NEG]
- `S163.png`
A corkboard dense with index cards, small photographs and lengths of yarn re-tracing the state's claimed route, every card and picture blurred into an unreadable smear, a hanging work lamp in a dim rented room, the old case being taken apart pin by pin, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
```
**scotus_marble — 4 — S164–S167**（object）
```
- `S164.png`
Towering marble columns of a supreme court facade in cold morning light, monumental verticality, dwarfing scale, no people, no readable inscription, no readable text [STYLE] Avoid: [NEG]
- `S165.png`
Wide marble steps rising toward great bronze doors, pale light and long shadows, the top of American law, no people, no readable text [STYLE] Avoid: [NEG]
- `S166.png`
An empty elevated court bench of dark wood behind which nine tall chairs stand in gloom, highest authority as furniture, no people, no readable text [STYLE] Avoid: [NEG]
- `S167.png`
A marble frieze abstracted to soft-focus figures of stone in raking light, justice as sculpture only, no readable inscription, no identifiable faces, no readable text [STYLE] Avoid: [NEG]
```
**strike_wall_41 — 3 — S168–S170**（object・S170 は also_thumb・wall 2 states: S169 the one unstruck／S170 igniting・R3++++ 転換: S168 microfilm reader＝紙の集計の実務）
```
- `S168.png`
A microfilm reader glowing alone in a dark county records room, its projected page an unreadable smear of columns, dust drifting through the lamp cone, decades of jury paper feeding through one small window of light, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S169.png`
Close on the one unstruck card in a row of struck ones, standing intact in a thin shaft of pale light, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S170.png`
The great wall of struck unreadable juror cards igniting in dust-gold light from one corner as if the pattern itself has caught fire, the hinge of the whole film, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
```
**freedom_objects — 3 — S171–S173**（object・ここから free-air morning blue 解禁）
```
- `S171.png`
A prison gate standing half open onto a pale free-air morning blue sky, December light thin and clean, the first cool open color after an hour of heat, no people, no readable text [STYLE] Avoid: [NEG]
- `S172.png`
The open gate seen from inside, a rectangle of soft morning blue cut into slate darkness, threshold out, no people, no readable text [STYLE] Avoid: [NEG]
- `S173.png`
Six carved strokes of light collapsing into drifting gold dust against a dawning blue field, the count dissolving, abstract, no letterforms, no people, no readable text [STYLE] Avoid: [NEG]
```
**★HP reporters_winona — 4 — S174–S177**
```
- `S174.png`
Two anonymized reporters seen from behind walking a small-town Mississippi street with recorder bags on their shoulders, July light, outsiders arriving, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S175.png`
Anonymized hands turning the pages of a huge docket book on a storeroom table, pages unreadable smears, a small recorder beside, over-the-shoulder framing so no face reads, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `S176.png`
An anonymized reporter's back on a front porch at dusk speaking with an anonymized resident's back, both non-identifiable, screen door light, town testimony, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S177.png`
The interior of a car on a flat rural road at dawn, two anonymized figures from behind, recorder on the dash, the investigation in motion, no faces, no license plate, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP scotus_argument — 3 — S178–S180**
```
- `S178.png`
An anonymized advocate's back at a lectern before an elevated bench in marble gloom, nine distant silhouettes above, the smallest figure and the tallest room, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S179.png`
A marble gallery of anonymized backs seated in rows beneath columns, hush rendered in posture, cold light, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S180.png`
Anonymized hands opening a slim bound opinion, text an unreadable smear, one line caught in a blade of light, the decision arriving, no face, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP bail_walkout — 4 — S181–S184**（free-air blue 帯）
```
- `S181.png`
An anonymized man seen only from behind stepping out of a jail door into thin December morning-blue light, first unescorted step, posture tall, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S182.png`
A small crowd of anonymized family figures from behind reaching toward an arriving man, all backs and hands, morning blue and warm coats, joy without a single face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S183.png`
Anonymized hands only, fitting a small monitoring device at an ankle in flat institutional light, freedom with a tether, non-sensational, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S184.png`
An anonymized man's silhouette standing still in open winter air facing a pale blue morning sky, breath visible, twenty-three years exhaled, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
**★HP dismissal_and_votes — 7 — S185–S191**
```
- `S185.png`
An anonymized official's hands laying a single motion paper on a bench, its text an unreadable smear, a courtroom empty behind, the case ending as quietly as paper, no face, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `S186.png`
A wide empty courtroom with the defense table cleared and chairs pushed in, warm light entering high windows for the first time, aftermath as peace, no people visible beyond one distant anonymized back at the door, no readable text [HSTYLE] Avoid: [HNEG]
- `S187.png`
An anonymized clerk's back stamping a file closed, dust rising in gold light, with prejudice rendered as finality of gesture, no face, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `S188.png`
Anonymized voters seen from behind in line outside a small-town polling place at dusk, jackets and caps, patient civic queue, morning-blue dusk sky, no faces, no readable signage, no readable text [HSTYLE] Avoid: [HNEG]
- `S189.png`
A voting booth curtain half drawn with an anonymized figure's shoes and shadow beneath, the town's verdict in progress, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S190.png`
An anonymized hand pulling a lever inside a booth, close on hand and lever only, decisive motion, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S191.png`
An empty small-town polling hall after closing, folded chairs and one unreadable tally sheet far out of focus, dusk blue through the windows, the answer already given, no faces, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
```
**★F visible_faces_act4 — 4 — S192–S195**
```
- `S192.png`
F09: a clearly illustrative semi-painterly face of a generic freed man with gray-streaked hair tilted up toward the open sky at a gate in thin morning-blue light, disbelief melting into relief, eyes wet and lifted, low-angle close-up about half of frame height, wind lifting the collar, unmistakably an illustration resembling no real individual, adults only [FSTYLE] Avoid: [FNEG]
- `S193.png`
F10: a photoreal generic elderly woman spectator's tear-streaked face caught over a stranger's shoulder in the gallery, hand pressed to her mouth, small in the frame about a fifth of frame height and low, dim cool gallery with a single warm practical glow behind her, resembling no real individual, adults only [FSTYLE] Avoid: [FNEG]
- `S194.png`
F11: a photoreal generic small-town voter's face at dusk, quiet resolve after a long decision, weathered features, medium close-up about thirty percent of frame height, cool dusk key with warm porch rim, resembling no real individual, adults only [FSTYLE] Avoid: [FNEG]
- `S195.png`
F12: a photoreal generic young Black prospective juror's composed, dignified face in half light, the seat finally kept, calm direct gaze near camera, medium close-up about thirty-five percent of frame height, dust-gold key and clean rim against dark oak blur, resembling no real individual, adults only [FSTYLE] Avoid: [FNEG]
```

### ACT 5 — ENDING（15枚・S196–S210・object 13 ＋ ★HP 2（S204/S206・R3+ 2026-07-26 転換）・the count that never resolves）
**four_chairs_return — 4 — S196–S199**（chairs 1: S196＝morning-blue への state change・R3++++ 転換: S197 empty choir risers at night／S198 new key morning blue／S199 uncounted archive boxes）
```
- `S196.png`
The four straight-back chairs again, now in gentle morning-blue window light with one warm gold edge, one chair still smaller, held in stillness, no people, no readable text [STYLE] Avoid: [NEG]
- `S197.png`
Empty wooden choir risers in a dark church at night, moonlight through the tall window laying pale bars across them, closed hymnals resting along the rail, the silence the singing returns to, no people, no legible characters, no readable text [STYLE] Avoid: [NEG]
- `S198.png`
A single new brass key seated in the front-door lock of a modest house, thin morning-blue light and one warm gold edge on the metal, an ordinary door that opens from the inside now, no people, no readable text [STYLE] Avoid: [NEG]
- `S199.png`
Stacked archive boxes seen through the wired-glass window of a locked records-room door, dust settled thick on their lids, labels faded to unreadable smears, the paper no one has counted yet, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
```
**unsolved_count — 4 — S200–S203**（tally 2 states: S200 standing unresolved／S203 the last lone mark・R3++++ 転換: S201 sealed case box／S202 four porch lights＝S024–S025 の four lamps の evolution）
```
- `S200.png`
Six carved strokes of dulled gold light standing in a row over a dark empty road at night, the count still standing with nothing beneath it, abstract, no letterforms, no people, no readable text [STYLE] Avoid: [NEG]
- `S201.png`
A single sealed cardboard case box alone on a bottom steel shelf in a dark records room, its label blank where a closed case's stamp would go, one cold slate edge of light, a file that cannot be closed, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S202.png`
Four porch lights burning at dusk along a quiet small-town street, one to a house, small and steady against the coming dark, the four lamps of the store kept lit somewhere else now, no people, no readable text [STYLE] Avoid: [NEG]
- `S203.png`
One last single stroke of light remaining as the others sink into dark, the unanswered question as a lone mark, abstract, no people, no readable text [STYLE] Avoid: [NEG]
```
**gospel_morning — 4 — S204–S207**（object 2: S205/S207・★HP 2: S204/S206 — singing again・R3+ 2026-07-26 転換）
```
- `S204.png`
A gospel choir of anonymized robed figures standing in the choir loft at dawn rehearsal, seen from the empty pews below as dark warm silhouettes against a tall window pouring pale morning-blue and thin gold light, singing again, the thread the state could not take, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S205.png`
An open hymnal on a pew in morning light, pages stirring slightly as if breathed on, blurred unreadable, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `S206.png`
A handful of anonymized churchgoers seen from far behind crossing a dirt churchyard toward a small white church at dawn, long coats and Sunday hats against a huge clean morning-blue sky, dawn gold at the treeline, quiet endurance, no faces, no readable signage, no readable text [HSTYLE] Avoid: [HNEG]
- `S207.png`
A dirt road running toward a soft blue morning horizon, mist low over the fields, a road that finally leads somewhere, no people, no readable text [STYLE] Avoid: [NEG]
```
**final_breath — 3 — S208–S210**
```
- `S208.png`
The small-town main street at dawn, empty and washed in pale blue and first gold, storefront glass catching the sky, quiet after everything, no people, no readable signage, no readable text [STYLE] Avoid: [NEG]
- `S209.png`
The twelve-chair jury box at rest in soft even morning light, no chair singled out, no shadow arithmetic, what the room should always have looked like, no people, no readable text [STYLE] Avoid: [NEG]
- `S210.png`
Fine gold dust settling slowly through a last shaft of morning light onto dark oak, the film's final breath, macro, abstract, no people, no readable text [STYLE] Avoid: [NEG]
```

## 5.7 幕別 motif 枚数の検算（★Codex は書き終えたら足して確認）

```
（R3+ owner directive 2026-07-26: object→★HP 28行転換後の per-act 内訳）
ACT0  : 6+3+3+3 = 15（all object）
ACT1  : 2+6+4+1+8+1 (object 22) + [4+3+3 転換] + 4+3+4 (★HP 21) + 2 (★F) = 45
ACT2  : 4+3+4+5+4+3 (object 23) + [2+3+2+1 転換] + 4+5+3+4 (★HP 24) + 3 (★F) = 50
ACT3  : 4+4+4+3+5+3+2 (object 25) + [3+1+1 転換] + 4+4+4 (★HP 17) + 3 (★F) = 45
ACT4  : 1+4+4+3+3 (object 15) + [3 転換] + 4+3+4+7 (★HP 21) + 4 (★F) = 40
ACT5  : 4+4+2+3 (object 13) + 2 (★HP: S204/S206) = 15
合計   : 15+45+50+45+40+15 = 210 ✓
lane  : object 113 + ★HP 85 (40.5%) + ★F 12 = 210 ✓
★HP 85 の全数リストは §5.2（[HSTYLE] の行数＝85 と一致すること）
```
> **R3++++ 2026-07-26 注:** §5.5a の de-repetition は **in-place の内容差し替えのみ**（37行・object→object 31／HP→HP 6）。S番号・act・lane・block 枚数は一切動いていないため、上の検算・§5.2 の ★HP 85 全数リスト・§3.2/§3.3 はそのまま有効。
> **S001..S210 の連番が穴なく210行**そろっていることを `--only S001` の `shots=257`（210 body + 44 i2v種 + 3 thumb_face）で確認する。

## 5.8 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_flowers_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.9 パーサ契約（`read_prompts()` はこの2行形式しか読まない）

```
- `S001.png`
<positive prompt> Avoid: <negative>
```
- **1行目:** `` - `S001.png` ``（バッククォート囲み・行末は `.png` の直後）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト（**`[STYLE]` 等のプレースホルダは全文展開して書く**）
- `ai_prompts.v001.md` は **body 210行（S001..S210）＋ i2v 種 44行（M01_src..M44_src、§8.1a）＋ thumb_face 3行（T01_face..T03_face、§5.12）＝ 257 エントリ**を書く。すべて1枚生成。

## 5.10 生成コマンド（★variants 指定なし。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=257 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 54 --only S001
#   → ログ "episode=... shots=257 ... -> N images" の shots が 257 であること（210 body + 44 i2v種 + 3 thumb_face）

# 全257枚（body 210 + i2v種 44 + thumb_face 3・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-054-flowers
```
> QC で落ちたシーンの再生成は `--only S###`（同じプロンプトで別シードを1枚）。**基準を下げない・水増ししない。**

## 5.11 ★匿名人物 style（★HP body 85枚 ＋ 人物 i2v 種 18本 に共通）— `[HSTYLE]`/`[HNEG]`

> **実在人物（Flowers/Evans/Hallmon/被害者/Bibbs/Baran/判事/州司法長官/候補者）の likeness を作らない。** 実在人物が示唆される所は顔を非識別（背向き/横顔を影に/逆光シルエット/目から下クロップ/浅い被写界深度・**adults only**）。**被害者・暴行・殺害・遺体を絶対に描かない。16歳 Derrick Stewart を人物として出さない（椅子の象徴のみ）。**
> **★人物 i2v 種 18本（H001–H018）は「新規カット」ではなく §4.5 の M04/M06/M08/M10/M12/M14/M16/M18/M19/M21/M23/M26/M28/M30/M32/M35/M38/M40 の中身**（44 i2v の内数・additive しない・locked counts 不変）。各 H の内容は §4.5 の tags と §8.1a のプロンプトで確定済み。

**共通スタイル `[HSTYLE]`（全文連結）:**
```
, cinematic photoreal still, documentary reenactment stand-in, a generic anonymized person who resembles no real individual, face kept non-identifiable — turned away, in profile lost to shadow, back-lit to a silhouette, cropped below the eyes, or thrown soft in shallow focus, Mississippi dust-gold key light with warm near-black ink and death-row slate as the cold note, a pale free-air morning blue only where the beat is bail or freedom or ending, low-key deep-shadow lighting, telephoto compression, shallow depth of field, restrained dignified framing, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no readable documents, adults only
```
**共通ネガティブ `[HNEG]`（全文連結）:**
```
recognizable real person, likeness of a specific person, Curtis Flowers, Doug Evans, Odell Hallmon, Bertha Tardy, Carmen Rigby, Robert Golden, Derrick Stewart, James Bibbs, Madeleine Baran, any real judge or attorney general or juror, celebrity, mugshot, deepfake, text, words, letters, numbers, captions, watermark, logo, readable document, legible case file, legible newspaper, legible report, legible date, license plate, victim, murder victim, dead body, corpse, any depiction of the murders or an attack, violence, blood, gore, injury, weapon, gun in hand, crime scene, re-enactment of a crime, identifiable child, teenager's face, minor, sexual content, nudity, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, evidence-blue drawer, green van, blue bandana, milky haze, scanline
```

## 5.12 ★サムネ用 emotive-face 静止画（3枚・thumb_face）

> **CTR ドライバ＝単一の AI 生成・非実在・illustrative/dramatized な顔**を peak emotion で。**実在人物（Flowers/Evans 等）の likeness を作らない**＝clearly illustrative（semi-painterly, cinematic-render）にして実写に読ませない＝likeness firewall。**被害者・暴行・未成年の顔を作らない。** 本編カットに出ない thumbnail 専用（role=thumb_face・public_path null・distinct/cuts に数えない・§3.1）。B が `FlowersThumbnails.tsx` で face＋2–4語 hook text（例: TRIED 6 TIMES）を合成。

**共通スタイル `[TSTYLE]`:**
```
, thumbnail key art, a single non-real dramatized generic human character rendered in a clearly illustrative semi-painterly cinematic style so it never reads as a real photograph of a real person, face occupying 50 to 65 percent of frame height with eyes on the upper third, bright key light on the face and a rim light separating it from a dark desaturated blurred background, skin warm, background cool, high contrast and vivid, one clean quadrant of negative space for text, 1280x720, ultra-detailed
```
**共通ネガティブ `[TNEG]`:**
```
photoreal photograph of a real person, likeness of Curtis Flowers or Doug Evans or Odell Hallmon or any real defendant or prosecutor or judge or juror, recognizable real celebrity, deepfake, a real child, a teenager, the victims, murder victim, blood, gore, violence, weapon, text, words, letters, numbers, watermark, logo, two faces, tiny face, neutral expression, dark muddy low-contrast mush, cartoon flatness, extra limbs, deformed, warped
```
```
- `T01_face.png`
A non-real dramatized generic middle-aged Black man's face in an illustrative cinematic style at peak emotion — a wronged, enduring, dread-filled stare gazing slightly off-camera, the look of a man tried again and again for a crime he did not commit, pushed to the right third over a dark blurred row of six glowing tally strokes, warm rim light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
- `T02_face.png`
A non-real dramatized generic older white man's face in an illustrative cinematic style with a cold, certain, unrepentant authority glare looking directly at the viewer, the relentless-prosecutor archetype, pushed to the left third over a dark blurred courthouse-columns background in dust-gold dusk, hard rim light, clean negative space on the right [TSTYLE] Avoid: [TNEG]
- `T03_face.png`
A non-real dramatized generic man's face in an illustrative cinematic style with eyes closing in stunned release, a single tear, the moment every charge disappears after twenty-three years, pushed to the right third over a dark blurred prison gate opening onto pale morning-blue light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
```
> ★これら3枚は `role:"thumb_face"`・`public_path:null`・`has_human_body:true`・`has_identifiable_real_person:false`。§6 の目視で「実在 likeness でない・illustrative・被害者/未成年なし」を確認。B のサムネ案はこの T01–T03 を前景に、§4.3a の also_thumb body（背景）＋ 2–4語 hook（TRIED 6 TIMES / 41 OF 42 等・数字が CTR 資産）で組む。

## 5.13 ★F シリーズ（可視の感情顔・12枚＝210 body の内数・owner directive 2026-07-25 ネイティブ実装）— `[FSTYLE]`/`[FNEG]`

**2レーン、いずれも「実在の誰にも似せない・非実在の人物」：**
- **(a) generic-photoreal** — 特定の実在人物に紐づかない役（捜査官 S060・検事アーキタイプ S108・陪審員 S109・記者 S155・傍聴人 S193・有権者 S194・陪審候補 S195）→ 実写調OK。
- **(b) dramatized-illustrative** — 中心的実在人物に隣接するビート（悲嘆の町の人 S059・被告 everyman S110・ガラス越しの男 S153・ホールドアウト陪審員 S154・ゲートの解放 S192）は**明らかにイラスト調・半絵画的**（実在人物の写真に絶対見えない）。実在人物として名指し/キャプションしない。

**HARD BANS（不変）：** Flowers・Evans・Hallmon・被害者・Bibbs・Baran・実在の判事/陪審員の**肖像を作らない**；**未成年の顔は一切不可**；被害者の描写・暴力・遺体なし；可読テキストなし。QCフラグ：`has_human_body:true`・`has_identifiable_real_person:false`・`has_identifiable_face:false`・`has_victim_or_violence:false`・`has_readable_text:false`。

**★ FACE 規格（in-lane data 準拠）:** 顔は**大きさでなく光と表情で**目立たせる — **medium close-up・フレーム高の30–45%・目は上1/3・正面〜軽い3/4・カメラ近くを見る**、強い単一感情、dark moody 背景に dramatic key + rim。60%超の顔面充填・背向き・影に沈む・hands-only は F では不可。

**共通スタイル `[FSTYLE]`（全文連結）:**
```
, a clearly-visible emotive human face in a strong medium-close-up filling 30 to 45 percent of the frame, eyes on the upper third, front or slight three-quarter view looking near camera, one strong unmistakable emotion, dramatic key light plus rim light on the face against a dark moody background, restrained saturation, a generic anonymized non-real person resembling no real individual, cinematic documentary grade, Mississippi dust-gold and slate palette with morning blue only on freedom beats, ultra-detailed skin and eyes, high contrast, 16:9, adults only, no text, no watermark, no logo
```
**共通ネガティブ `[FNEG]`（全文連結）:**
```
likeness of a real or named person, Curtis Flowers, Doug Evans, Odell Hallmon, Bertha Tardy, Derrick Stewart, James Bibbs, Madeleine Baran, recognizable real person, mugshot, deepfake, child, teenager, minor, victim, dead body, corpse, blood, injury, weapon, violence, readable text, document, caption, watermark, logo, cartoon flatness, extra limbs, deformed, warped, milky haze
```

Files = §5.6 の `★F` 行（S059/S060・S108–S110・S153–S155・S192–S195 = 12枚）。全12枚を目視QC（見える感情顔・非実在・likeness/未成年/被害者/文字なし）してからマニフェストへ。

---

# 6. A-2/A-3: 静止画のQC・目視（★depth map なし）

## 6.1 機械QC（body 210 + i2v種 44 + thumb_face 3 = 全257枚・`qc_flowers_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `18.0<=mean_luma<=225.0`（warm near-black ＋ slate の低照度が多い→黒潰れ注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**（R3++++ 2026-07-26 更新・§5.5a 転換後のクラスタ）衝突は tally strokes(S001/S005/S084–S086/S130/S173/S200/S203＝各行が別 state。同 state に見えたら reject)・jury chairs(S007/S073/S074/S119/S122/S209＝台帳の構成違いが読めること)・strike cards(S010/S079/S081/S161/S169/S170)・four chairs(S028/S029/S196)・courthouse facades(S061/S065)・cell window(S113/S117)・storefront interior(S019/S022–S025/S027/S116)・four lights(S024/S025/S202)・prison exteriors(S064/S111/S112)・roads(S040/S063/S207/S208)・stenotype(S009/S076)・corkboard(S048/S163)・folders/paper(S004/S011/S088/S125/S132/S134/S156/S199/S201) の被りに注意。★HP クラスタ（85枚の anti-samey 監視）: choir/congregation(S033/S035/S052–S054/S204/S206)・gallery/steps crowds(S062/S071/S096/S097/S100/S179/S182)・jury figures(S078/S145/S147)・corridor/institutional figures(S050/S056/S089/S102/S114/S118)・waiting families(S115/S118/S176/S182)・town life(S017/S018/S020/S021/S045/S046/S047/S174)・hands closeups(S034/S049/S051/S066/S076/S093/S094/S095/S103/S104/S129/S142/S146/S152/S157/S159/S175/S180/S183/S185/S187/S190)** | 片方 reject＋プロンプト見直し（§5.5a: 同ビート内の同一 motif は最大2） |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・日付(1996/2010/2019)・Roman numeral のタイポ・名前・新聞/文書のロゴが写っていないか | `has_readable_text=true`→reject |
| Q6 | **実在人物**の顔の混入 | **目視。** 実在人物として識別可能な顔（Flowers/Evans/Hallmon/被害者/Bibbs/Baran/判事に**似た**顔）が写っていないか。**匿名・非識別・非実在の顔（HP/F/thumb_face）は OK。** | `has_identifiable_real_person=true`→reject |
| Q7 | 被害者/暴行/遺体/未成年 | **目視。** 被害者の描写・暴行/殺害/injury/blood/凶器・現場・規制線・**識別可能な未成年**が写っていないか。**★匿名の成人人体は OK。** | 1つでもあれば reject |

**Q5/Q6/Q7 は機械で判定しない。全257枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-054-flowers --media image
#   → runs/qc/flowers_footage_contact_NN.png（20枚/シート・約13シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-53 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** 特に **S022–S027(storefront absence)に遺体/血/規制線が出ていないこと、S036(銃の輪郭)が実銃に転じていないこと、S038(靴跡)が blood-print でないこと、S055–S058(arrest)が「有罪の男」に読めないこと（dignity 必須）、S092–S095/S108(prosecutor)が実在 DA に似ていないこと、S131/S135(ガラス越し)が lurid でないこと、S136–S138(3つの灯り)に人物・暴力が出ていないこと、S195(陪審候補の顔)が dignified であること、T01–T03 が illustrative で実在人物に似ていないこと、を必ず目で確認する。**

## 6.2 出力
```
episodes/PD-2026-054-flowers/05_visuals/still_qc.v001.json     # 257枚全部の行（reject も残す）
```

## 6.3 accepted が (body210 / i2v44 / thumb3) に届かなかったとき
```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 54 --only S###   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_flowers_stills.py
```
accepted body >= 210 かつ i2v_source >= 44 かつ thumb_face >= 3 になるまで繰り返す。**基準を下げない・水増ししない。**

## 6.4 ★depth map は生成しない（本作は depth treatment 不使用）
**DESIGN §1 の hard rule により footage/still treatment は `bleed`/`parallax`/`duotone`/`focus` のみ・`depth` を使わない**（depth displacement は被写体を melt/warp させる＝EP48/49 の warp 欠陥）。したがって **`gen_depth_maps.py` を回さない・`<stem>_depth.png` を作らない・マニフェストに `depth_path` を持たせない**（§4.1a/§4.2-19）。B の render も depth を参照しない。

---

# 7. A-4: factory 実写クリップ 236本の選定と全点目視QC

## 7.1 在庫の実態
```
H:\pd-media\assets\factory\   フラット構成（backgrounds 11,000本超・light_assets・particle_assets・vfx_overlays・texture_assets・loops）
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json（★必ず encoding="utf-8" で開く）
★棚のラベルは全面的に信用できない（過去実測: evidence_bag=カートゥーン）。ラベルで選ばず必ず目視（§7.5）。
```

## 7.2 選定条件
- **`kind=="video"` のみ。** 静止画 factory は使わない
- **236本ちょうど**（§3.3[8] より still-share≤0.45 を守る設計値）
- **各1回しか使わない**（`MAX_USES_FACTORY=1`）
- 幕別割り当て（§4.4）: HOOK+OPENING=12 / ACT1=42+8 / ACT2=45+9 / ACT3=45+9 / ACT4=42+9 / ACT5=15 ＝ 236
- **EP39〜EP53 の絵柄を選ばない（§7.7 の分離語）。** EP54 は 1990s Mississippi small town・furniture storefront・Southern church/gospel（非識別）・county courthouse/records・prison exterior farmland（非扇情）・supreme court marble・radio/recorder・polling place・morning-blue dawn。**被害者/暴行/泣き崩れる遺族/遺体/実在の顔が写るニュース映像を選ばない。crime scene tape・銃の実写・法廷内の実在人物を選ばない。EP52 の evidence drawer/green van/bandana、EP47 の two-lane road/pickup、EP41 の sodium prison corridor、EP44 病院、EP49 Utah 駐車場、EP50 cyan を選ばない。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query county_courthouse --limit 60 --exclude-used --ep PD-2026-054-flowers --json
```
`--exclude-used` は出荷ゲート `arc_nonrepeat` と同じ指紋集合を使う。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・§4.4 に pre-assign 済み）
> **★`covers_scene_id` は still 資産 ID 空間（S001..S210）を指す。** §4.4 の各エントリに pre-assign 済み（22本が covers 付き、残りは null の繋ぎ/情景）。

| covers（例） | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S007/S010 | jury box・records storeroom | `jury_box` / `records_room` | 0 |
| S016/S022/S032/S044 | Mississippi main street・storefront・church・railroad | `small_town_mainstreet` / `furniture_store` / `southern_church` / `railroad_tracks` | 1 |
| S061/S067/S073/S088/S101 | courthouse/courtroom/jury box/records/appellate | `county_courthouse` / `empty_courtroom` / `court_records` | 2 |
| S111/S113/S118/S131/S139 | prison farmland/cell window/jury room/visitation glass/prison phone | `prison_exterior` / `cell_window` / `jury_room` / `visitation` | 3 |
| S156/S164/S172/S174/S188 | archive boxes/supreme court/gate dawn/recorder/polling place | `archive_shelves` / `supreme_court` / `prison_gate` / `audio_recorder` / `polling_place` | 4 |
| S204/S207/S208/S210 | church dawn/dirt road blue/main street dawn/dust settling | `church_window_dawn` / `dirt_road_morning` / `town_dawn` | 5 |

**残りは covers を持たない繋ぎ・情景**（institutional 廊下・oak/marble texture・sky・flat field・heat shimmer・telephone lines・freight train）。**暗いクリップに偏りすぎない**（暗側は約78本まで＝1/3・July 昼光・courthouse 昼・morning blue を混ぜる）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）
```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.4a ★★★ 実写ストックライブラリを必ず使う（EP48/49 の burned lesson）★★★
- **ストックライブラリ:** `H:\pd-media\assets\stock`（マニフェスト `STOCK_MANIFEST.json`・pexels/pixabay・**商用可**）。
- **調達方針（★counts は固定・factory 236 を変えない。レーン内の調達源を広げるだけ）:**
  1. `STOCK_MANIFEST.json` を読み、**意味（§7.3 の covers カテゴリ）に一致し §7.5 の全点目視 QC と R-FACE/R-VICTIM を通る実写動画を優先採用**（無理な水増しはしない）。
  2. 残り枠を `H:\pd-media\assets\factory` 在庫で埋める。
  3. 各エントリの出所（`origin`: `stock` or `factory`）を `factory_selection.v001.json`（§7.6）と `stock_ledger.v001.json`（§10.2）に記録。
  4. **ストック静止画は本編 body still（AI 210）レーンに混ぜない。**
- **★R-FACE/R-VICTIM/R-ALTSUSPECT を絶対順守:** 実在の判事/警官/被告/記者が識別可能に写るニュース映像・被害者/暴行/遺体/gore・「立ち去る謎の男」に読める素材は**ストックでも使わない**。EP39〜53 との sha256 被りゼロ（§7.7）はストック由来にも適用。
- **★カラーマッチは B が担当:** pexels/pixabay の発色バラつきは B が dust-gold/slate の neutral グレードで AI still に合わせる（**milky wash にしない**）。

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★
> **実際に起きた事故（EP36 大聖堂・EP38 牛・factory棚ラベル全面破損）。** `subtype` は「その検索語で取った」記録であって中身の保証ではない。**236本は分割して全点見る。**

**選抜236本は例外なく次を経る:**
```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-054-flowers --media video --dir "<236本の staging フォルダ>"
```
1. コンタクトシートを開き **236本すべてを1本ずつ見る**
2. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて選定から外す（差替え）
3. 実写シネマティックB-roll・EP54テーマ・ウォーターマークなし・識別可能な実在人物なしを確認
4. **★制約の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。**被害者/暴行/遺体/泣く人/gore・実在の顔が写るニュース映像・crime scene tape・銃の実写を使わない。EP52 evidence drawer/green van・EP47 two-lane/pickup・EP41 sodium prison・EP44 病院・EP49 Utah を含むクリップを使わない。**
5. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=42.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。**暗いクリップは約78本（1/3）までに抑え、July 昼光・courthouse 昼・morning blue を混ぜる。**

## 7.6 出力
```
episodes/PD-2026-054-flowers/05_stock/factory_selection.v001.json   # 選定理由・幕割り当て・origin
episodes/PD-2026-054-flowers/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP53 との重複ゼロ（BLOCKING）
```bash
./.venv/Scripts/python.exe scripts/select_flowers_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-053-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP54 の236本の積集合が**空**であることを確認。1件でも exit 1。**EP39〜EP53 のファイルは読むだけ。**

**分離レーン（色・素材・語）:** EP41 sodium gold（監獄廊下）／EP42 blue（ankle monitor）／EP43 amber／EP44 teal（病院）／EP45 crimson／EP46 green／EP47 civil-violet（two-lane Texas road/pickup）／EP48 glover／EP49 somber-plum（Utah）／EP50 steel-cyan／EP52 evidence-indigo（drawer/bandana/green van）。**EP54 = Mississippi dust-gold `#B98A33`（INK `#0C0B09`）＋ death-row slate `#5C6670` ＋ 保釈以降のみ free-air morning blue `#7FA8C9`。** これら他話の絵柄・色・被写体を1本も選ばない。

---

# 8. A-5: i2v モーション化 44本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする44本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）
種画像は §5 と同じ `generate_sdxl_4k.py`（variants なし）で `M<NN>_src.png` として生成（`ai_prompts.v001.md` に §8.1a の44行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `FLW-MS01..MS44`、モーション成果物は `FLW-M01..M44`。**幕別配分は §4.5 に pre-assign 済み**（ACT0 3 / ACT1 7 / ACT2 9 / ACT3 11 / ACT4 10 / ACT5 4 = 44）。
> **★このうち ★18本は匿名人物ビート（H001–H018）＝44本の内数**（M04/M06/M08/M10・M12/M14/M16/M18/M19・M21/M23/M26/M28/M30・M32/M35/M38/M40）＝`[HSTYLE]`/`[HNEG]` を使う。**残り26本が抽象/象徴種**＝`[STYLE]`/`[NEG]`。

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの44行を追加・各1枚・**poised-still の source**・全行 literal）
```
- `M01_src.png`
Five carved strokes of dust-gold light standing in near-black with the space for a sixth glowing faintly, the count poised a breath before it grows, abstract, no letterforms, no people, no readable text [STYLE] Avoid: [NEG]
- `M02_src.png`
A heavy pencil tip touching the top corner of an unreadable smeared name card, poised the instant before the strike line is drawn, macro, cold slate light, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `M03_src.png`
Twelve jury chairs each under its own small warm light, the first lamp already dimming, poised a moment before the box goes dark chair by chair, no people, no readable text [STYLE] Avoid: [NEG]
- `M04_src.png`  (= H001 · ACT1 · the choosing)
Anonymized investigators' backs before a corkboard of unreadable smeared papers, one hand lifted holding a pin a breath away from the central blank card, cold lamplight, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M05_src.png`
Four small warm lamp points inside a dim furniture store held perfectly still, the first already trembling, poised before they dim, wide and far, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
- `M06_src.png`  (= H002 · ACT1 · gospel before)
A gospel choir of anonymized backlit silhouettes mid-breath, hands just beginning to rise, warm dust-gold light flooding past them, poised at the top of a note, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M07_src.png`
A small-town Mississippi main street at noon with heat shimmer barely beginning to bend the far storefronts, poised summer stillness, no people, no readable signage, no readable text [STYLE] Avoid: [NEG]
- `M08_src.png`  (= H003 · ACT1 · the arrest)
An anonymized man's back at a slate institutional doorway flanked by two anonymized officer backs, one foot lifted mid-step over the threshold, dignity in posture, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M09_src.png`
A dawn route across a small town rendered as photographic fragments just beginning to slide out of alignment, poised at the first tear, abstract collage, no people, no readable text [STYLE] Avoid: [NEG]
- `M10_src.png`  (= H004 · ACT1 · the statement)
Anonymized adult hands with a pen a hair above a legal pad, a drawer standing open in shadow beside, poised between writing and burying, unreadable smears, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M11_src.png`
A single carved stroke of dust-gold light with one hairline fracture just appearing at its top edge, poised a breath before it cracks to slate, abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `M12_src.png`  (= H005 · ACT2 · the prosecutor)
An anonymized prosecutor stand-in silhouetted from behind at a podium, one arm just beginning to rise mid-argument, hard back-light so no face reads, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M13_src.png`
Twelve empty jury chairs in darkness with the first chair's light just blooming, poised before all twelve ignite the same flat gold, scoreboard frontal, no people, no readable text [STYLE] Avoid: [NEG]
- `M14_src.png`  (= H006 · ACT2 · the verdict)
A courtroom gallery of anonymized backs caught at the first instant of rising, shoulders lifting in unison, motion poised, warm oak light, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M15_src.png`
A stack of struck unreadable name cards with one more card hanging in the air above it mid-fall, poised, cold slate light, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `M16_src.png`  (= H007 · ACT2 · the reversal)
Nine anonymized robed silhouettes behind a long elevated bench in marble gloom, one distant figure leaning forward a fraction, judgment poised, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M17_src.png`
Two carved strokes of light already fractured and a third just beginning to split, cracks glowing slate, poised mid-cascade, abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `M18_src.png`  (= H008 · ACT2 · back to the row)
An anonymized man's back mid-stride down a long slate corridor between two escort backs, the far door a pale rectangle, poised in motion, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M19_src.png`  (= H009 · ACT2 · counts in reserve)
Anonymized hands gripping one of four plain folders in a dim drawer, the folder lifted an inch into dust-gold light, poised between kept and used, unreadable labels, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M20_src.png`
A frame split into warm gold and cold slate halves along a hairline crack of light that is just beginning to widen, deadlock poised at breaking, abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `M21_src.png`  (= H010 · ACT3 · the jury splits)
Anonymized jurors' backs around a deliberation table, two clusters leaning away from each other a degree further, gulf widening, split warm and slate light, poised, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M22_src.png`
Twelve chairs with seven in warm light and five in cold slate, the two colors pressing against each other along a trembling line, poised, no people, no readable text [STYLE] Avoid: [NEG]
- `M23_src.png`  (= H011 · ACT3 · the holdout)
A single juror chair in a hard cold spotlight with an anonymized deputy's long shadow just entering the light's edge, poised menace by geometry only, no faces, no handcuffs, no readable text [HSTYLE] Avoid: [HNEG]
- `M24_src.png`
A courtroom wall clock in oak shadow, its minute hand a soft unreadable shape poised at the last instant of a half hour, dust in light, no numerals, no people, no readable text [STYLE] Avoid: [NEG]
- `M25_src.png`
Five scarred carved strokes with a sixth just beginning to sear in beside them, fast heat at its base, poised at completion, abstract, no letterforms, no people, no readable text [STYLE] Avoid: [NEG]
- `M26_src.png`  (= H012 · ACT3 · the years)
An anonymized man seen from behind on the edge of a bunk in a bare cell, the window light on his shoulders poised between winter slate and thin summer gold, still and dignified, no face, no gore, no readable text [HSTYLE] Avoid: [HNEG]
- `M27_src.png`
A dark human silhouette behind heavily ribbed visitation glass leaning a degree closer, shape without a face, poised, slate light, unglorified, no likeness, no readable text [STYLE] Avoid: [NEG]
- `M28_src.png`  (= H013 · ACT3 · the call)
An anonymized inmate's back at a prison wall phone, receiver just lifted off the hook, cord swinging slightly, poised before the words, slate light, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M29_src.png`
Three small warm points of light in a vast dark field, the first just beginning to gutter, poised with maximum dignity, abstract, no people, no violence, no readable text [STYLE] Avoid: [NEG]
- `M30_src.png`  (= H014 · ACT3 · the recording)
Anonymized hands holding a small recorder toward ribbed glass, its reels just starting to turn, a waveform of pale light poised flat before the spike, no face, no legible characters, no readable text [HSTYLE] Avoid: [HNEG]
- `M31_src.png`
A huge docket ledger lying open in a gold dust shaft, one heavy page lifted mid-turn and poised, columns unreadable smears, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `M32_src.png`  (= H015 · ACT4 · the reporters)
Two anonymized reporters' backs mid-stride down a small-town street with recorder bags, July light hard ahead of them, poised arrival, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M33_src.png`
Two abstract vertical bars of light on darkness, the tall dust-gold one still climbing and poised to tower over the short pale one, no numerals, no people, no readable text [STYLE] Avoid: [NEG]
- `M34_src.png`
The great dark wall of struck unreadable cards with the first corner just catching dust-gold fire, ignition poised to sweep, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `M35_src.png`  (= H016 · ACT4 · the argument)
An anonymized advocate's back at a lectern beneath nine distant bench silhouettes, head just lifting to speak, marble hush poised, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M36_src.png`
Six carved strokes of light standing in a row with fractures leaping between them, the whole count poised at the instant of shattering, abstract, no letterforms, no people, no readable text [STYLE] Avoid: [NEG]
- `M37_src.png`
A prison gate poised half open onto a pale free-air morning-blue December sky, thin clean light through the widening gap, no people, no readable text [STYLE] Avoid: [NEG]
- `M38_src.png`  (= H017 · ACT4 · the walkout)
An anonymized man seen only from behind mid-step out of a jail doorway into morning-blue light, a small crowd of anonymized backs beyond just beginning to surge toward him, poised joy, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M39_src.png`
Six carved strokes of dulled gold light beginning to crumble at their tops into drifting dust against a dawning blue field, collapse poised, abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `M40_src.png`  (= H018 · ACT4 · the town votes)
A voting booth curtain drawn to a hand's width with an anonymized figure's shadow inside and one hand poised on the lever, civic finality a second away, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M41_src.png`
The four straight-back chairs in still morning light, a slow band of pale blue and gold poised at the frame's edge about to cross them, one chair smaller, no people, no readable text [STYLE] Avoid: [NEG]
- `M42_src.png`
Six faded carved strokes of light standing over a dark empty road, night air just beginning to move through them, unresolved and poised, abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `M43_src.png`
An open hymnal on a pew in dawn light, one page lifted a centimeter by moving air and poised mid-stir, blurred unreadable, no legible characters, no people, no readable text [STYLE] Avoid: [NEG]
- `M44_src.png`
Fine gold dust hanging in a last shaft of morning light above dark oak, poised in the instant before settling, macro, abstract, no people, no readable text [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_morton.py` を下敷きにパスと SHOTS だけ差し替え）
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
STILL_DIR     = H:\pd-media\assets\ai\flowers
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\flowers
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, melting, text, watermark, identifiable face, real person likeness, child face, teenager, crying person, victim, corpse, assault, gore, blood, gun"
```
**ゲート:** `dry_validate`（length=5）/ `assert_loaded_completely` / `assert_frame_math`。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す・★44本は複数日）
```bash
py -3.11 scripts/comfy_wan_flowers.py --build
py -3.11 scripts/comfy_wan_flowers.py --run --shot M01
py -3.11 scripts/comfy_wan_flowers.py --run-all
```
1本 24–73 GPU分・44本で 18–54時間。**夜間分割で回す。開始前にマシン状態を確認（heavy-job preflight）。A1111 と ComfyUI の VRAM 競合に注意（同時フルロード禁止・`unload-checkpoint`）。**

## 8.4 RIFE で 48fps 化（`rife_flowers.py`・`rife_morton.py` と同手順）
```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番 → RIFE 2x を2回（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. フレーム数検証 `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC
- 顔・**被害者・暴行・遺体・泣く人・gore・銃**が生成されていないこと（必ず目視・制約2/3/5）
- モーフィング/ちらつき/ワープ/melt が無いこと → あれば別シードで再生成
- prosecutor 影（M12）・ガラス越し silhouette（M27）・H シリーズは**識別可能な実在 likeness**に転じていないこと・**未成年の顔**が出ていないこと
- tally strokes（M01/M11/M17/M25/M36/M39/M42）に**読める文字/数字**が出ていないこと／booth（M40）に可読の紙が出ていないこと／gate（M37）は開く動きが自然なこと
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（44本 × 2回 = 88カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど30本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **15本** | courtroom/storeroom dust・heat haze・church motes・field dust・prison slate dust・night drift。黒背景 drift を screen 合成 |
| `light_assets` | **10本** | dust-gold shaft・oak window bar・slate window light・**morning-blue edge（保釈以降/close 用の少数=L05/L09）**・pew shaft・marble sweep |
| `vfx_overlays` | **5本** | 微細な grain・warm light noise・slate glitch min |
| **合計** | **30本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/flowers/overlay/` に置き、`flowers_film.json` の `cuts[].src` には**出さない**。**★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない・scanline/CRT/vignette-wash を選ばない（DESIGN §1）。** 黒背景でループするものを選び `blend_hint` を書く。発色は B が accent `#B98A33`/slate `#5C6670` に寄せる想定・morning-blue は保釈以降のみ。他話色を選ばない。§7.5 の目視QC対象（30本）。

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_flowers_assets.py`）
```
remotion/public/flowers/img/     ← role=body の静止画210枚（★depth なし）
remotion/public/flowers/factory/ ← 選定 factory .mp4 236本（§4.4 の F001..F236 名で）
remotion/public/flowers/motion/  ← i2v M<NN>_rife.mp4 44本
remotion/public/flowers/overlay/ ← 合成レイヤー 30本（§4.6 の P/L/V 名で）
remotion/public/flowers/thumb/   ← thumb_face T01..T03（B の FlowersThumbnails が参照）
```
- `public_path` はマニフェストの値（§4.4/§4.5/§4.6）と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）
- **★depth の同名ペアは作らない・置かない**（§6.4）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する）:**
- factory の `public_path` は必ず `flowers/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も含めない
- 合成レイヤーは `flowers/overlay/` に置き `cuts[].src` に出さない

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`
全静止画・i2v・factory・overlay・thumb_face を1行ずつ: `asset_id`/`path`/`source`(`ai_codex`|`factory`|`stock`)/`origin`/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力
```bash
./.venv/Scripts/python.exe scripts/build_flowers_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_flowers_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_flowers_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**★factory 236 / motion 44 / overlay 30 が非空で実体化しているか（不変条件17/18/16）を必ず確認。**

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
EP54 の設計値: still 230/210=1.095(≤2) / factory 236/236=1.0(≤1) / motion 88/44=2.0(≤2) / first-use 490/554=0.8845(≥0.70) / avg-uses 554/490=1.131(≤1.4)。**全て達成可能。**

---

# 12. 絶対にやらないこと
- **EP39〜EP53 のファイル・素材に触らない。** 読み取りのみ可。素材・色・音のレーンも分離（§7.7）。EP54 の accent は **Mississippi dust-gold #B98A33**（INK #0C0B09・slate #5C6670・保釈以降のみ morning blue #7FA8C9・A は絵で他話の流用色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない**（`remotion/src/**` `scripts/ae/**` `scripts/build_flowers_film.py` `manifest.json` `04_scenes/shotlist*` `figures`）。ただし `04_scenes/ai_prompts.v001.md` は A が書く。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness をどこにも作らない**（Flowers/Evans/Hallmon/Tardy/Rigby/Golden/Stewart/Hill/Sanders/Loggins/Bibbs/Baran/判事/州司法長官/候補者）。**匿名・非識別の一般人は可**。**被害者7人の描写・暴行/殺害/遺体 imagery・識別可能な未成年・「立ち去る真犯人」類の別容疑者示唆を一切作らない。**
- **制約に反する文言・絵を作らない**（§1.2/§1.3）: Flowers の有罪化／被害者/暴行/遺体/現場の描写／未成年顔・少年の私物プロップ／Evans の処罰・資格喪失の示唆・内心断定／"real killer" 等の別容疑者語／陪審数字の捏造・可読描画／"13 years on death row"／可読の偽公文書／実在人物 likeness／dochighlight／捏造/可読引用／milky wash/scanline。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。（factory の subtype `_02`/`_03` は別素材の意で別物・混同しない。）
- **role=thumb / still_thumb を作らない・overlay を30本以外にしない・thumb_face を3枚以外にしない。** also_thumb は body 4枚（§4.3a）。
- **★factory 236 / motion 44 / overlay 30 の配列を空・stub のまま出荷しない**（EP45/EP38 事故・§4.4/§4.5/§4.6 を実体化）。
- **★depth map を生成しない・`depth_path` を持たせない**（§6.4・DESIGN §1）。
- **★dochighlight figure を作らない・言及しない**（grep で 0）。
- **枚数を「だいたい」で決めない。** §3 の確定値（still 210 / factory 236 / i2v 44 / thumb_face 3 / distinct 490 / first-use 0.8845 / still-share 0.4152 / avg-uses 1.131 / overlay 30）と §3.3 の検算をそのまま使う。合わなければ本書を疑って報告。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** 生成物・在庫クリップを実際に見る。

---

# 13. 完了報告に含めるもの
```
1. accepted 静止画の枚数と内訳（body 210 [＝object 113 ＋ ★HP 85 = 40% ＋ ★F 12・R3+ 2026-07-26] / i2v_source 44 [＝抽象 26 ＋ ★人物 18] / thumb_face 3 / also_thumb 4 [§4.3a] / reject N）
2. factory 選定 236本のリスト（asset_id / subtype / origin / eyeballed_content）と、subtype と食い違って外した本数、
   storefront/prison/church/polling クリップの「no readable text / no logo / no face / no victim / no gore / no crime tape」確認、stock 由来の本数
3. EP39〜EP53 重複ゼロの確認結果
4. i2v 44本の frames / duration_sec と、SHORT? の有無、★H001–H018（18本）の匿名・非識別・adults-only・no-victim 確認、
   ★HP body 85枚・★F 12枚が実在 likeness なし・未成年顔なし・被害者/暴行なしの確認、★HP 85枚の anti-samey（§5.2 variety matrix・同一 subject+composition+lighting の組ゼロ）確認
5. 合成レイヤー30本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code）＋ factory 236/motion 44/overlay 30 が非空で実体化した確認 ＋ depth_path をどこにも生成していない確認
7. §3.3 の検算 [1]〜[8] を自分で再計算した結果（avg-uses/source 1.131≤1.4 を含む）
8. asset_manifest.v001.json の counts ブロック（still_body 210 / still_i2v_source 44 / motion 44 / factory 236 / overlay 30 / thumb_face 3）
9. 制約・1枚前提の自己申告（Flowers の有罪化なし・被害者/遺体/現場 graphic なし・未成年顔なし・別容疑者示唆なし・
   Evans の処罰/資格喪失示唆なし・hedged 数値の可読断定なし・実在の顔/likeness ゼロを目視確認・dochighlight 文字列ゼロ・
   捏造/可読引用なし・milky wash/scanline なし・depth なし・バリエーション0・A↔B同一スキーマ
   [schema flowers_assets.v1 / role enum body|i2v_source|thumb_face|reject / counts / also_thumb 集合 4 / overlay 30 / thumb_face 3]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
