# EP59 robosigning — Codex スレッドA「素材生成」引き継ぎプロンプト v001（30分・5幕・reveal ladder）

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN_ARCHITECTURE）も実装スレッドB（CODEX_B）も**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> ★30分尺。素材点数は EP55 burge / EP56 postoffice と同スケール。**「だいたい」で決めず §3 の確定値と §3.3 の検算をそのまま使う。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP59 / Episode ID: PD-2026-059-robosigning / slug: robosigning
Composition id: Ep59Robosigning（B が Root.tsx に登録・A は staging まで）／1920x1080 / fps30 / 30:00
事件:       The foreclosure forgery machine（米国の住宅差押え書類偽造・2009-2013）
            2008年の住宅危機のあと、米国の大手モーゲージ・サービサー（住宅ローンの回収代行会社）は
            差押え裁判に出す【宣誓供述書 affidavit】を工場のように量産した。署名者は中身を読まず、
            公証人は立ち会わず、それでも書類には「私は自分の personal knowledge に基づき述べる」と
            書かれていた。GMAC Mortgage の Jeffrey Stephan は 2009-12-10（フロリダ州パームビーチ郡）と
            2010-06-07（メイン州 Federal National Mortgage Association v. Bradbury）の宣誓証言で、
            自分のチームが月に約1万通を自分のところへ回し、自分はそれを読まずに署名していたと認めた
            ＝おおよそ【労働1分に1通】。ジョージア州アルファレッタの DocX 社では、Linda Green という
            一人の実在従業員の名前が、何十通りもの筆跡で数十万通の抵当権譲渡証書に「署名」され、
            彼女は何十もの銀行の役員として肩書きを付け替えられていた。
            2010年9-10月、GMAC/Ally・JPMorgan Chase・Bank of America が相次いで差押えを停止し、
            10-13 に全50州の司法長官が合同調査を開始。
            2012-02-09、5大サービサーと49州＋連邦が【$25 billion の National Mortgage Settlement】で和解。
            2011-04-13 に OCC と連邦準備制度が14社へ consent order を出し、Independent Foreclosure Review
            が始まったが 2013-01-07 に打ち切られ、和解金に置き換えられた。結果として、誤って家を失った
            世帯が受け取った金額は数百ドル〜千数百ドル規模で、最初の小切手の一部は不渡りになった。
            刑事責任を負った人間はごく僅かで、DocX の社長 Lorraine Brown が連邦で実刑を受けた。
            ★主題は【誰も読まなかった署名が、100万世帯の家を合法に見せた】。
            ★★実在人物（Cardoso 夫妻等の一般市民・Jeffrey Stephan・Linda Green・Lorraine Brown・
              判事・司法長官・銀行幹部）の顔・肖像・likeness を一切作らない。匿名・非識別の一般人は可。
            ★★★【署名】は本作の主役オブジェクトだが、**判読できる名前・文字を一切描かない**。
              署名は常に「抽象的なインクの筆致（abstract ink mark / illegible stroke）」として描く。
              可読の偽公文書（affidavit・deed・notice・小切手・判決文・銀行明細）を作らない。
              銀行のロゴ・実在の企業名・実在の州章/連邦印章を描かない。流血・暴力・遺体なし。
            ★時代考証 1998-2026 の米国（2005-2013 が主戦場）。スマホは 2010 以降のビートのみ。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ・30分スケール）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**210本の固有プロンプト×1枚＝210枚**・バリエーション0） | `H:\pd-media\assets\ai\robosigning\S<NNN>.png` | 5–8時間（GPU） |
| A-1b | i2v 種画像の生成（**42本の固有プロンプト×1枚＝42枚**・バリエーション0） | `H:\pd-media\assets\ai\robosigning\M<NN>_src.png` | 1.5–2.5時間（GPU） |
| A-1c | サムネ用 emotive-face 静止画（**3枚**・CTR §4A・非実在の illustrative face・§5.12） | `H:\pd-media\assets\ai\robosigning\T<NN>_face.png` | 20分（GPU） |
| A-2 | 静止画のQCと目視（**全255枚を目視必須**＝210 body + 42 i2v種 + 3 thumb_face、＋F系12枚） | `05_visuals/still_qc.v001.json` + コンタクトシート | 2.5–4時間 |
| A-3 | ~~depth map~~ **不要（本作は depth treatment を使わない・§6.4）** | — | — |
| A-4 | factory 実写クリップ **235本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | 4–6時間（うち目視だけで2時間以上） |
| A-5 | i2v モーション化 **42本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\robosigning\M<NN>_rife.mp4` | 18–48時間（GPU・**複数日**） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **30本** | `05_stock/overlay_selection.v001.json` | 1時間 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 30分 |
| A-8 | Remotion public への staging | `remotion/public/robosigning/{img,factory,motion,overlay,thumb}/` | 40分 |

> **★★ 最重要の前提（EP42–56 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 210本＝210行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **variants 指定なし（＝1枚）** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 210 + i2v 種 42 + thumb_face 3 = 255枚（各1回）＋ F系 12枚（§5.13・後追い追記）= 267枚。** factory 235本は生成でなく在庫からの選抜。
> ★**`--only S001` のログで `shots=255` を確認**してから本番を回す（210 body + 42 i2v種 + 3 thumb_face = 255）。F系12行は §5.13 の手順どおり **後から追記**して `shots=267`。
> ★i2v 42本は**複数日GPU**。**開始前にマシン状態を確認**（heavy-job preflight）。夜間・分割で回す。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-059-robosigning/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を **A(producer)とB(consumer/validator)で一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 235 エントリ、`motion` 配列は 42 エントリ、`overlay` 配列は 30 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5／§4.6 に全 235 + 42 + 30 を列挙済み。build スクリプトはこの列挙を消費するだけで、空配列を書かない）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\robosigning\**` / `H:\pd-media\assets\ai_video\robosigning\**` | **A** | 読み書き |
| `episodes/PD-2026-059-robosigning/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-059-robosigning/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/robosigning/{img,factory,motion,overlay,thumb}/**` | **A** | 読み書き |
| `episodes/PD-2026-059-robosigning/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_robosigning_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-058-*/**` および EP39〜58 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を読む） | `PD-2026-059-robosigning`（variants 指定なし） / `59 --only S001` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-059-robosigning --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit N --exclude-used --ep PD-2026-059-robosigning --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-059-robosigning` |

> **★`gen_depth_maps.py` は使わない**（本作は depth treatment を使わない＝depth map 不要・§6.4／DESIGN §1「footage treatment は bleed/parallax、depth 不可」）。

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（実在確認してから・直近の `*postoffice*`(EP56) を優先、無ければ `*burge*`(EP55)） |
|---|---|---|
| `scripts/qc_robosigning_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_postoffice_stills.py`（無ければ `qc_burge_stills.py`） |
| `scripts/select_robosigning_factory.py` | §7 の factory 235本の確定選定・EP39〜58 sha256 除外検証 | `scripts/select_postoffice_factory.py`（無ければ `select_burge_factory.py`） |
| `scripts/comfy_wan_robosigning.py` | §8 の i2v 42本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_postoffice.py`（実在確認） |
| `scripts/rife_robosigning.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_postoffice.py`（実在確認） |
| `scripts/build_robosigning_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_postoffice_asset_manifest.py` |
| `scripts/stage_robosigning_assets.py` | §10 の staging | `scripts/stage_postoffice_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.9 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_robosigning_facts.py`（B が clone して実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の制約に一致し、`check_robosigning_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_robosigning_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==235 / motion 配列長==42 / overlay 配列長==30 が非空で実体化していること（EP45事故回避の必須不変条件）

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_robosigning_asset_manifest.py --reuse-feasibility
#   → still >=210 / motion >=42 / factory >=235 / distinct 合計 >=487 / first-use >=0.70 / avg-uses/source <=1.4

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_robosigning_stills.py --check-resolution

# ★★ [A-DONE-6] 可読テキスト / 可読署名ゲート（R3 BLOCKER FIX 2026-07-29）
#   v001 にはこの行がなかった——つまり本作最大のリスクである「読める署名」に対する赤/緑判定が
#   完了条件のどこにも存在しなかった（§6.1 Q5/Q6 は定義されていたがどのゲートにも繋がっていない）。
#   依存導入をここで明示的に許可する（§0.3 の「これ以外を新規に作らない」の明示例外）:
#     pip install opencv-python-headless imagehash pillow
./.venv/Scripts/python.exe scripts/qc_robosigning_stills.py --check-text --check-signature
#   → Q5 fail=0 / Q6 fail=0。267枚すべてで exit 0 でなければ未完了。
#   → 加えて **署名モチーフを含む全行の 100% 目視**を必須とする。機械検査だけでは筆記体を捕まえられない。

# [A-DONE-4] factory の視覚QCゲート（★全235本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-059-robosigning

# [A-DONE-5] EP39〜EP58 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_robosigning_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39〜EP58 のすべてに対して）
```

---


# 1. ★★★ 最優先の絶対条件（正確性制約・ガードレール）★★★

**本作の悪役は【会社と工程】であって個人ではない。銀行・サービサー・書類代行会社に対しては【裁判所・規制当局が認定した事実と和解内容】のみを扱う。実在する一般市民の住宅所有者は【尊厳第一】＝公に語られた範囲のみ。Jeffrey Stephan は【生存・低い職位の従業員】＝彼自身の宣誓証言の言葉だけで描き、"architect / mastermind / criminal" と書かない。Linda Green は【被害者側に近い＝名前を他人に使われた人】であって加害者ではない——署名が最初に画面に出る同じ場面でそれを明示する。Lorraine Brown は【連邦で有罪判決・実刑】＝有罪と認定事実は断定してよい（判決の範囲を超えない）。刑事処罰の広がりについては FACTS_LEDGER の permitted-wording 行を厳守する。数値は台帳のヘッジどおり。捏造引用禁止・可読の偽公文書禁止・実在ロゴ禁止・時代考証 1998–2026。**

## 1.1 R1/R2（生成ビジュアル全般）

1. **★R-FACE: 匿名・非識別の人物は可／実在人物の likeness は不可。** 匿名の一般人（実在の誰にも似せない・非識別のドラマ化スタンドイン）＝顔・身体を出してよい（§5.11 H シリーズ・`[HSTYLE]`/`[HNEG]`・§5.12 thumb_face・§5.13 F シリーズ）。ただし **実在人物の顔・likeness・肖像は作らない**＝本件の住宅所有者夫妻・Jeffrey Stephan・Linda Green・Lorraine Brown・Chris Pendley・実在の判事/州司法長官/連邦規制当局者/銀行 CEO を**似せて描かない**。実在人物が示唆される所（署名者・公証人・サービサー幹部・弁護士・判事・被害世帯）は非識別（背向き/影/逆光/目から下でクロップ/hands-only）を既定に保つ。
   > ★★ **R3 MAJOR FIX 2026-07-29 — v001 はここで §5.12 / §5.13 と真っ向から衝突しており、解決規則がなかった。** §5.13 は owner 承認（2026-07-25）を根拠に F系12枚の「見える顔」を要求するが、本行を修正していないので、上から順に読むオペレータは矛盾にぶつかる。**例外をここに明記する:** §5.12 thumb_face 3枚 と §5.13 F系 12枚 は、**【非実在・誰にも似せない】を前提に見える顔を作ってよい**。ただし **中心的実在人物に隣接する役（署名者・公証人・幹部・被害世帯）は §5.13(b) の semi-painterly illustrative レーンに限る**。★**これにより F007（generic notary の photoreal medium-close-up）は (a) photoreal レーンから (b) illustrative レーンへ移すこと** — 公証人は本作で実在人物（Shawanna Crite）が直接対応する役であり、F系の中で最も露出が大きい行だった。
2. **★R-SIGNATURE-ILLEGIBLE（本作の最重要禁止）: 署名・書類の文字を一切判読可能に描かない。** 署名は常に **abstract ink mark / illegible looping stroke / a wet dark stroke with no letterforms**。**実在・架空を問わず、人名として読める署名を1枚も作らない。** 人名の綴りをプロンプトに書かない。affidavit・deed・mortgage assignment・notice of default・小切手・判決文・銀行明細は**全て "blurred into an unreadable smear"**。金額・件数（$139,000 / $25 billion / $300 / 10,000 / one per minute 等）を**画像に描かない**（AE/figures のタイポで出す＝B の担当）。
3. **★R-NO-LOGO: 実在の銀行・サービサー・政府機関のロゴ、名称、州章、連邦印章、通貨の可読の額面を描かない。** 建物は generic。封筒・書類は無地。
4. **★R-NO-DISTRESS-PORN: 立ち退きの扇情的描写を作らない。** 手錠・保安官の強制排除・泣き崩れる家族・路上に投げ出された家財を作らない。**家は常に aftermath＝無人・静か・鍵が掛かっている。** 人物ビートは待つ・見る・数える・運ぶ・鍵を握る等の抑制された行為に限る。
5. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **R-SIGN-ILLEGIBLE:** "legible signature", "readable signature", "signature reading", "readable name on the document" を**正プロンプトと manifest の文字列値に**書かない。★ **R3 BLOCKER FIX 2026-07-29 — ネガティブプロンプト（`Avoid:` 以降）は本ルールの適用外。** 本ルールは v001 で無スコープだったが、`legible signature` は `[NEG]`/`[HNEG]`/`[TNEG]`/`[FNEG]` に合計8回登場する（禁止語をわざと列挙するのがネガの仕事だから）。上の BLOCKER FIX でマクロを展開した瞬間、スコープなしだと **267行全部が `check_robosigning_facts.py` で確実に落ちる**。だからスコープは必須。署名は `an abstract illegible ink stroke` 系のみ。実在人物名の綴りを署名の内容として書かない。
2. **R-READABLE:** "legible affidavit / readable deed / readable notice / readable cheque / legible court record / legible bank statement / readable dollar figure" を正プロンプトに書かない。全て `unreadable smear`。
3. **R-GREEN-VICTIM:** 名前を使われた実在従業員を "forger / fraudster / criminal" と書かない。署名モチーフの注記は常に「a name used by other hands」枠。
4. **R-STEPHAN-EMPLOYEE:** 署名担当の従業員を "mastermind / architect / crime boss" と書かない。彼は **evidence**（自分の宣誓証言）であって設計者ではない。
5. **R-BROWN-SCOPE:** 有罪判決を受けた経営者について、判決が認定した範囲を超える表現（"the woman who took a million homes" 等）を書かない。
6. **R-NO-LOGO:** 実在ロゴ/社名/州章/連邦印章/可読の通貨額面を書かない（§1.1-3）。
7. **R-NO-EVICTION-VIOLENCE:** "family being dragged out / handcuffed homeowner / sheriff forcing a crying woman / belongings thrown on the street / weeping face at an eviction" を書かない（§1.1-4）。
8. **R-FACE:** 実在人物 likeness ゼロ（§1.1-1）。匿名一般人（"anonymous / generic / non-identifiable person, face turned or in shadow"）は許可。
9. **R-NUM:** 台帳がヘッジしている数値を断定文で書かない・**画像に可読で描かない**。exact-of-record は AE/figures（B）へ。
10. **R-QUOTE:** 捏造引用禁止。verbatim は FACTS_LEDGER の VERIFIED-VERBATIM 系統のみ・AE（B）の担当。画像に可読の引用を描かない。
11. **R-DOCHL:** **dochighlight を作らない・書かない・言及しない**（grep で 0 を保つ・レンダリングバグに見えるため恒久禁止）。同様に **DATE_STAMP レイアウトは存在しないので使わない**（日付カードは `CENTER_STACK`）。
12. **R-DATE/時代考証:** 1998–2026 の米国。2005–2007 のビートにスマホ・LED街灯・現代車・現代UIを混ぜない。CRT モニタは 2007 以前のオフィスのみ。
13. **R-NO-GAVEL-SPAM:** gavel（小槌）・天秤（scales of justice）・Lady Justice 像は **全素材合計2枚以下**（オーナーの常設苦情・`footage_diversity` の generic symbols ≤2）。法廷は建物・席・扉・書記官の机・傍聴席で表す。

## 1.3 機械ゲート（`build_robosigning_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

> ★★ **R3 2026-07-29 — 適用範囲を二つ直す。**
> **(a) ネガティブは除外する。** `BANNED_ACCURACY` / `check_robosigning_facts.py` は **正プロンプト側と manifest の文字列値にのみ**適用する。`Avoid:` 以降のネガティブプロンプトは禁止語を意図的に列挙するため、除外しないと全行が偽陰性で落ちる（§1.2-1 と同じ fix）。実装例：`pos, _, neg = row.partition("Avoid:")` して `pos` だけを検査する。
> **(b) 正プロンプト本文を manifest に入れる。** v001 の §4.1a エントリは `prompt_id` / `tags` / `caption_hint` / `eyeballed_content` / `notes` しか持たないので、この正規表現は **画像を生んだ指示文を一度も見ていない**（メタデータだけを監査していた）。§4.1a の stills エントリに `"prompt": "<正プロンプト全文（マクロ展開後）>"` を追加し、§4.2 不変条件6 の適用範囲に含めること。

```python
import re
# 匿名・非識別の人物は許可。実在人物の likeness だけを弾く。
BANNED_PORTRAIT = re.compile(
    r"likeness of (a )?(real|specific|named) person|real[- ]person likeness|"
    r"face of (jeffrey )?(stephan|linda green|lorraine brown|pendley|cardoso|nyerges|grodensky)|"
    r"likeness of (stephan|green|brown|pendley|cardoso|nyerges|grodensky)|"
    r"recognizable (real person|celebrity)|identifiable real person|"
    r"mugshot of (a )?real person|deepfake",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"legible signature|readable signature|signature reading|"
    r"legible (affidavit|deed|notice|cheque|check|court record|bank statement|mortgage)|"
    r"readable (affidavit|deed|notice|dollar|amount|figure|document|name)|"
    r"(bank|servicer|federal|state) (logo|seal|crest)|"
    r"handcuffed homeowner|family (being )?dragged|belongings thrown on the street|"
    r"weeping (family|woman|man) at an eviction|sheriff forcing|"
    r"(forger|fraudster|criminal) (named|called)|the (mastermind|architect) of the fraud|"
    r"dochighlight",
    re.IGNORECASE)
```

---

# 2. 台本の語数と尺の確定値（Aが素材点数を積算する根拠）

```
words_total          = 4,675 MEASURED（script.en.v001 のゲート同一 regex 実測・DESIGN §5 が正典）
wpm_model            = 178.1（gate model）／★実測は 170–176 wpm に落ちる実績（EP55 -71.2s / EP56 -71.8s）
narration_seconds    = 4,675 / 178.1 * 60 = 1,575.0 PROVISIONAL
★HOOK-AUDIO 標準（owner・EP52 継続）: Brian の声が 0:00 から鳴る（silent runway なし）。
designed_gap_seconds = 199.0 PROVISIONAL（幕転換の息・AEカード下の music hold・earned breaths ≤3・OST 着地。
                       check_padding を通る設計ギャップ＝dead air でない）
total_seconds        = 1,575.0 + 199.0 + endcard 9.0 = 1,783.0（29:43・band 1740–1860 内）
speech ratio         = 1783.0 / 1575.0 = 1.132（実測帯 1.04–1.30 内）
durationInFrames     = 53,490（fps30 = 1783 x 30・VO onset 0.0）★PROVISIONAL
★★ measured-VO re-lock 後の値が正典（DESIGN §5 の手順）。A は素材点数の積算にしか使わないので、
   re-lock で total が動いても【素材の点数（210/42/235/30/3/12）は変えない】。
mean_shot            = 3.151秒/カット（picture 1774.0 = total 1783.0 - endcard 9 / 563 cuts）
視覚 acts             = 5（+ HOOK/OPENING と ENDING は別区）
Act 語数配分（★MEASURED・script.en.v001 を機械集計）:
  HOOK 159 / OP 60 / ACT1 491 / ACT2 547 / ACT3 822 / ACT4 930 / ACT5 1,200 / ENDING 466 = 4,675
  ★ACT5 が最密（1,200語）＝清算の算数。ACT4（930語）が次点＝署名工場。still の per-act 数（§3.2）は
    ACT4/ACT5 を各38枚で最密にしてあり、この実測配分と整合している。
```

**Aにとっての意味は1つ:** > **総カット 563 / distinct 487 / 初出 86.50% = still 210 + factory 235 + motion 42。**（§3 で積算）

> **注意（命名差）:** 視覚 act は **0=HOOK/OPENING, 1=ACT I, 2=ACT II, 3=ACT III, 4=ACT IV, 5=ACT V, 6=ENDING**（7値）。**still は 210 本の固有プロンプトを持つ**ため、still の資産 ID は **S001..S210**（1プロンプト＝1枚）。`covers_scene_id` は still 資産 ID 空間（S001..S210）を指す（§7.3）。

---

# 3. ★素材構成の確定値（この値で調達する・勝手に変えない）

## 3.1 内訳（★勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **実写 archive/factory クリップ（Layer 1）** | **235本** | 235カット | **各1回(1)** | 111,821点アーカイブ／88,740点 factory 棚から選抜（§7）・全点目視・EP39〜58 と sha256 被りゼロ |
| **SDXL静止画（Layer 3・本編 body）** | **210枚** | 244カット | 1.162回(≤2) | **210本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **i2v モーション（Layer 4）** | **42本** | 84カット | 各2回(≤2) | 42本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **487点** | **563カット** | | |
| 合成レイヤー（particle/light/vfx・Layer 4） | 30本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |
| AE hero cards（Layer 2） | 17枚 | カットの上に合成 | — | **B の担当**（DESIGN §3）・A は素材を出さない |
| サムネ emotive-face（thumb_face） | 3枚 | — | 本編カットに出ない | **distinct/cuts に数えない**（§5.12・thumbnail 専用） |
| F系 emotive face（§5.13） | 12枚 | B が挿入判断 | — | **distinct/cuts に数えない**（補助レーン） |

**SDXL の生成バッチ（本編カットに出ない i2v 種・thumb_face を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **210枚** | 210プロンプト x 1枚 |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **42枚** | 42種プロンプト x 1枚 |
| サムネ face（`role:"thumb_face"`・§5.12） | **3枚** | 3プロンプト x 1枚 |
| **SDXL 生成バッチ合計（base）** | **210 + 42 + 3 = 255枚（各1回）** | **variants 指定なし（＝1枚）** |
| F系 emotive face（§5.13・後追い追記） | **12枚** | 12プロンプト x 1枚（追記後 `shots=267`） |

> **本編サムネの背景 anchor は body 210枚から4枚を `also_thumb:true` で流用選抜**（§4.3a）。**emotive-face（前景の顔）は §5.12 の thumb_face 3枚**（CTR §4A・B が `RobosigningThumbnails.tsx` で face＋hook text を合成）。**role=thumb / still_thumb を作らない。**

## 3.2 幕別配分（★still は確定・factory/i2v は目安。合計だけが確定）

| 区間(act) | still（S番号・確定） | archive/factory（目安） | i2v（確定合計42） | thumb anchor |
|---|---|---|---|---|
| HOOK+OPENING (0) | **15**（S001–S015） | 14 | 3（M01–M03） | S002 |
| ACT1「The House They Owned」(1) | **34**（S016–S049） | 38 | 6（M04–M09） | — |
| ACT2「Nobody Was Reading」(2) | **34**（S050–S083） | 34 | 6（M10–M15） | S061 |
| ACT3「What a Sworn Statement Is」(3) | **36**（S084–S119） | 36 | 7（M16–M22） | S104 |
| ACT4「The Signature Factory」(4)（engine・最密） | **38**（S120–S157） | 38 | 8（M23–M30） | — |
| ACT5「The Price of a Million Homes」(5)（climax） | **38**（S158–S195） | 36 | 8（M31–M38） | S181 |
| ENDING (6) | **15**（S196–S210） | 14 | 4（M39–M42） | — |
| 繋ぎ（covers_scene_id:null） | — | 25 | — | — |
| **合計** | **210** | **235** | **42** | **4** |

> **still の per-act 数（15/34/34/36/38/38/15＝210）は確定**（§5.6 の motif ライブラリがこの配分で組まれている）。**幕別の archive/i2v 内訳は目安値**（合計 235 / 42 のみ確定）。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 563 = still 244 + factory 235 + i2v 84
[2] 平均ショット長 = picture 1774.0（total 1783.0 - endcard 9）/ 563 = 3.151秒/カット  OK (<=7.0)
[3] 静止画占有率(check_animation_mix) = 244/563 = 43.34%  OK <=45%（余裕 1.66%pt）
[4] motion coverage = (235+84)/563 = 319/563 = 56.66%     OK >=45%
[5] per-asset 上限: still 244/210=1.162(<=2) / factory 235/235=1.0(<=1) / motion 84/42=2.0(<=2)  OK
[6] first-use share = 487/563 = 0.8650                    OK >=0.70
[7] avg uses/source = 563/487 = 1.156                     OK <=1.4（EP49 は 1.8 で flag された）
[8] factory 下限 = picture 1774.0/30 = 59.1 -> >=60本。設計値 235本 OK（still-share <=0.45 を守る）
[9] 四層予算（DESIGN §1a と一字一致）:
      Layer 1 archive/factory 実写 235カット = 41.7% of 563
      Layer 2 AE hero cards 17枚（カットの上に重ねる・合計 ~105秒。cut 数には数えない）
      Layer 3 Codex still      244カット = 43.3% of 563
      Layer 4 i2v 84カット = 14.9% of 563（+ overlay 30本は重ね掛け・cut 数に数えない）
      -> 実写 41.7% + i2v 14.9% = 動く素材 56.6% >= 45% の下限
```

> **★ re-lock 注意:** DESIGN §5 の measured-VO re-lock で total が動いたら [2] と [8] だけ再導出する。[1][3][4][5][6][7][9] は「点数の比」なので不変。

---


# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-059-robosigning/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `robosigning_assets.v1`（固定文字列）
**生産者:** `scripts/build_robosigning_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を一字一致。** role enum は **`body | i2v_source | thumb_face | emotive_face | reject`**。★**R3 MAJOR FIX 2026-07-29: `emotive_face` を追加した。** v001 の enum に F系の値がなく、`stills` は 255 固定、`counts` に F フィールドがなく、§10.1 のステージング一覧に `F*.png` がなかったので、**B は構造的に F001–F012 を見られなかった**——生成し QC もした12枚が死に素材になる、§4.4 が防ぐために書かれた EP45 の失敗クラスそのものだった。**あわせて: `stills` 配列長 = 267、`counts` に `"emotive_face": 12` を追加、§10.1 に `remotion/public/robosigning/face/F001.png .. F012.png（12）` を追加すること。**also_thumb は body still **ちょうど4枚**。thumb_face は **ちょうど3枚**。overlay は **ちょうど30本**。

## 4.1 スキーマ（`robosigning_assets.v1`）

```jsonc
{
  "schema_version": "robosigning_assets.v1",
  "episode_id": "PD-2026-059-robosigning",
  "slug": "robosigning",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_robosigning_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 210,        // ==210
    "still_i2v_source": 42,   // ==42
    "motion": 42,             // ==42
    "factory": 235,           // ==235
    "overlay": 30,            // ==30
    "thumb_face": 3,          // ==3
    "also_thumb": 4           // ==4
  },
  "stills":  [ /* 210 body + 42 i2v_source + 3 thumb_face + 12 emotive_face = 267 entries ★R3 */ ],
  "factory": [ /* 235 entries — SECTION 4.4 — public_path 非空 */ ],
  "motion":  [ /* 42 entries  — SECTION 4.5 — public_path 非空 */ ],
  "overlay": [ /* 30 entries  — SECTION 4.6 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例・★depth_path なし）

```jsonc
{
  "asset_id": "ROB-S001",
  "role": "body",                       // body | i2v_source | thumb_face | emotive_face | reject  ★R3
  "act": 0,
  "src_path": "H:/pd-media/assets/ai/robosigning/S001.png",
  "public_path": "robosigning/img/S001.png",
  "prompt_id": "S001",
  "sha256": "<64hex>",
  "phash": "<16hex>",
  "long_edge": 3840,
  "mean_luma": 0.0-1.0,
  "also_thumb": false,
  "ai_disclosure_required": true,
  "has_human_body": false,              // ★HP lane は true
  "has_identifiable_real_person": false,// 必ず false
  "has_readable_text": false,           // 必ず false
  "has_legible_signature": false,       // ★本作固有・必ず false
  "prompt": "<★R3必須: 正プロンプト全文（マクロ展開後・Avoid: 以前）>",
  "tags": ["hook","lockbox","house"],
  "caption_hint": "<= 60 chars, section 1.2 準拠",
  "eyeballed_content": "<A が実際に見たものを一文で>",
  "qc": { "accepted": true, "reasons": [] }
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `counts` が §3.1 の確定値と**完全一致**（210 / 42 / 42 / 235 / 30 / 3 / 4）。
2. `stills` 配列長 == 255、`factory` == 235、`motion` == 42、`overlay` == 30。**空配列は即 FAIL**（EP45 事故）。
3. 全 `src_path` / `public_path` が**実在**（`Path.exists()`）。`i2v_source` と `thumb_face` の `public_path` は `null`。
4. `sha256` の**重複ゼロ**（全レーン横断）。
5. `role` は enum **5値**のみ（★R3: `emotive_face` 追加）。`also_thumb:true` は body ちょうど4枚（§4.3a と一致）。
6. **全文字列値に §1.3 の `BANNED_PORTRAIT` / `BANNED_ACCURACY` を適用して 0 hit。**
7. 全 still の `has_identifiable_real_person == false` かつ `has_readable_text == false` かつ `has_legible_signature == false`。
8. `long_edge >= 3840`（body/i2v_source）。thumb_face は 1280x720 で可。
9. EP39〜EP58 の素材 sha256 と**交差ゼロ**。

## 4.3 `role` の割り当て（機械的に決める）

| ファイル | role | public_path | cuts に出るか |
|---|---|---|---|
| `S001..S210.png` | `body` | `robosigning/img/S<NNN>.png` | 出る（244カット） |
| `M01_src..M42_src.png` | `i2v_source` | `null` | 出ない（種画像） |
| `T01_face..T03_face.png` | `thumb_face` | `null` | 出ない（サムネ専用） |
| QCで落ちた再生成前の画像 | `reject` | `null` | 出ない |

### 4.3a ★also_thumb 集合（ちょうど4枚・CODEX_B と一字一致必須）

| S番号 | 何の絵か | サムネでの役割 |
|---|---|---|
| **S002** | 玄関ドアに掛かった不動産用キーボックス、夜の porch light 一灯 | メイン背景（hook の literal first shot・R-6） |
| **S061** | 無人の深夜オフィスフロア、机の上に積み上がった書類の山 | 代替背景（工場の絵） |
| **S104** | 誰も座っていない証人席と、その前に置かれた書類の束 | 代替背景（宣誓の絵） |
| **S181** | 郵便受けから覗く一通の封筒、朝の光 | 代替背景（清算の絵） |

## 4.4 ★`factory[]` 全235エントリ（★必ず実体化・public_path 非空。EP45事故回避の核心）

> `select_robosigning_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id・`AF-BG-*` 等）/`path`（`H:/pd-media/assets/factory/...` / `E:/pd-archive/...` / `F:/pd-archive/...`）/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`origin`(`factory`|`archive`|`stock`)/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。**
> **★命名注意（EP55/EP56 からの改良）: factory の public_path 接頭辞は `FC`（`FC001`…`FC235`）。** EP55/EP56 は factory の public_path に「Fに続く3桁」を使っていたため、§5.13 の emotive-face（F001–F012）と ID 空間が衝突していた。本作は `FC` 接頭辞にして衝突をゼロにする。`type:"backgrounds"`, `kind:"video"`。

```jsonc

// HOOK+OPENING (act 0) -- 14
{ "public_path":"robosigning/factory/FC001_suburban_street_dawn_wide.mp4", "act":0, "covers_scene_id":"S001", "subtype":"suburban_street_dawn_wide" }
{ "public_path":"robosigning/factory/FC002_mailbox_row_morning.mp4", "act":0, "covers_scene_id":"S002", "subtype":"mailbox_row_morning" }
{ "public_path":"robosigning/factory/FC003_front_door_lockbox_cu.mp4", "act":0, "covers_scene_id":"S003", "subtype":"front_door_lockbox_cu" }
{ "public_path":"robosigning/factory/FC004_empty_living_room_bare.mp4", "act":0, "covers_scene_id":"S004", "subtype":"empty_living_room_bare" }
{ "public_path":"robosigning/factory/FC005_window_blinds_light_slats.mp4", "act":0, "covers_scene_id":"S005", "subtype":"window_blinds_light_slats" }
{ "public_path":"robosigning/factory/FC006_porch_light_night_moth.mp4", "act":0, "covers_scene_id":"S006", "subtype":"porch_light_night_moth" }
{ "public_path":"robosigning/factory/FC007_headlights_driveway_night.mp4", "act":0, "covers_scene_id":"S007", "subtype":"headlights_driveway_night" }
{ "public_path":"robosigning/factory/FC008_keys_in_hand_macro.mp4", "act":0, "covers_scene_id":"S008", "subtype":"keys_in_hand_macro" }
{ "public_path":"robosigning/factory/FC009_paper_stack_edge_macro.mp4", "act":0, "covers_scene_id":"S009", "subtype":"paper_stack_edge_macro" }
{ "public_path":"robosigning/factory/FC010_pen_nib_ink_macro.mp4", "act":0, "covers_scene_id":"S010", "subtype":"pen_nib_ink_macro" }
{ "public_path":"robosigning/factory/FC011_office_fluorescent_ceiling_pan.mp4", "act":0, "covers_scene_id":"S011", "subtype":"office_fluorescent_ceiling_pan" }
{ "public_path":"robosigning/factory/FC012_clock_second_hand_cu.mp4", "act":0, "covers_scene_id":"S012", "subtype":"clock_second_hand_cu" }
{ "public_path":"robosigning/factory/FC013_highway_night_florida_drive.mp4", "act":0, "covers_scene_id":"S013", "subtype":"highway_night_florida_drive" }
{ "public_path":"robosigning/factory/FC014_title_bed_paper_grain.mp4", "act":0, "covers_scene_id":"S014", "subtype":"title_bed_paper_grain" }

// ACT I (act 1) -- 38
{ "public_path":"robosigning/factory/FC015_new_england_street_winter.mp4", "act":1, "covers_scene_id":"S016", "subtype":"new_england_street_winter" }
{ "public_path":"robosigning/factory/FC016_moving_boxes_stacked_room.mp4", "act":1, "covers_scene_id":"S016", "subtype":"moving_boxes_stacked_room" }
{ "public_path":"robosigning/factory/FC017_cash_bundle_counting_hands.mp4", "act":1, "covers_scene_id":"S017", "subtype":"cash_bundle_counting_hands" }
{ "public_path":"robosigning/factory/FC018_teller_counter_generic.mp4", "act":1, "covers_scene_id":"S018", "subtype":"teller_counter_generic" }
{ "public_path":"robosigning/factory/FC019_handshake_over_table_closing.mp4", "act":1, "covers_scene_id":"S019", "subtype":"handshake_over_table_closing" }
{ "public_path":"robosigning/factory/FC020_deed_folder_closing_desk.mp4", "act":1, "covers_scene_id":"S020", "subtype":"deed_folder_closing_desk" }
{ "public_path":"robosigning/factory/FC021_palm_trees_residential_street.mp4", "act":1, "covers_scene_id":"S021", "subtype":"palm_trees_residential_street" }
{ "public_path":"robosigning/factory/FC022_florida_stucco_house_day.mp4", "act":1, "covers_scene_id":"S022", "subtype":"florida_stucco_house_day" }
{ "public_path":"robosigning/factory/FC023_lawn_sprinkler_morning.mp4", "act":1, "covers_scene_id":"S023", "subtype":"lawn_sprinkler_morning" }
{ "public_path":"robosigning/factory/FC024_garage_door_opening_slow.mp4", "act":1, "covers_scene_id":"S024", "subtype":"garage_door_opening_slow" }
{ "public_path":"robosigning/factory/FC025_kitchen_window_light_empty.mp4", "act":1, "covers_scene_id":"S024", "subtype":"kitchen_window_light_empty" }
{ "public_path":"robosigning/factory/FC026_photo_frames_shelf_generic.mp4", "act":1, "covers_scene_id":"S025", "subtype":"photo_frames_shelf_generic" }
{ "public_path":"robosigning/factory/FC027_older_couple_backs_walking.mp4", "act":1, "covers_scene_id":"S026", "subtype":"older_couple_backs_walking" }
{ "public_path":"robosigning/factory/FC028_suitcase_wheels_driveway.mp4", "act":1, "covers_scene_id":"S027", "subtype":"suitcase_wheels_driveway" }
{ "public_path":"robosigning/factory/FC029_for_sale_sign_being_removed.mp4", "act":1, "covers_scene_id":"S028", "subtype":"for_sale_sign_being_removed" }
{ "public_path":"robosigning/factory/FC030_mailbox_flag_up_cu.mp4", "act":1, "covers_scene_id":"S029", "subtype":"mailbox_flag_up_cu" }
{ "public_path":"robosigning/factory/FC031_county_records_office_counter.mp4", "act":1, "covers_scene_id":"S030", "subtype":"county_records_office_counter" }
{ "public_path":"robosigning/factory/FC032_recorder_stamp_press_macro.mp4", "act":1, "covers_scene_id":"S031", "subtype":"recorder_stamp_press_macro" }
{ "public_path":"robosigning/factory/FC033_deed_book_shelves_row.mp4", "act":1, "covers_scene_id":"S032", "subtype":"deed_book_shelves_row" }
{ "public_path":"robosigning/factory/FC034_microfilm_reader_glow.mp4", "act":1, "covers_scene_id":"S033", "subtype":"microfilm_reader_glow" }
{ "public_path":"robosigning/factory/FC035_plat_map_paper_unrolled.mp4", "act":1, "covers_scene_id":"S033", "subtype":"plat_map_paper_unrolled" }
{ "public_path":"robosigning/factory/FC036_surveyor_stake_in_grass.mp4", "act":1, "covers_scene_id":"S034", "subtype":"surveyor_stake_in_grass" }
{ "public_path":"robosigning/factory/FC037_street_number_plate_cu.mp4", "act":1, "covers_scene_id":"S035", "subtype":"street_number_plate_cu" }
{ "public_path":"robosigning/factory/FC038_neighbourhood_aerial_slow.mp4", "act":1, "covers_scene_id":"S036", "subtype":"neighbourhood_aerial_slow" }
{ "public_path":"robosigning/factory/FC039_house_across_the_street_dusk.mp4", "act":1, "covers_scene_id":"S037", "subtype":"house_across_the_street_dusk" }
{ "public_path":"robosigning/factory/FC040_hurricane_shutters_closed.mp4", "act":1, "covers_scene_id":"S038", "subtype":"hurricane_shutters_closed" }
{ "public_path":"robosigning/factory/FC041_lawn_chairs_backyard_empty.mp4", "act":1, "covers_scene_id":"S039", "subtype":"lawn_chairs_backyard_empty" }
{ "public_path":"robosigning/factory/FC042_screened_porch_evening.mp4", "act":1, "covers_scene_id":"S040", "subtype":"screened_porch_evening" }
{ "public_path":"robosigning/factory/FC043_ceiling_fan_slow_rotation.mp4", "act":1, "covers_scene_id":"S041", "subtype":"ceiling_fan_slow_rotation" }
{ "public_path":"robosigning/factory/FC044_fridge_calendar_magnets.mp4", "act":1, "covers_scene_id":"S041", "subtype":"fridge_calendar_magnets" }
{ "public_path":"robosigning/factory/FC045_landline_telephone_cu.mp4", "act":1, "covers_scene_id":"S042", "subtype":"landline_telephone_cu" }
{ "public_path":"robosigning/factory/FC046_answering_machine_blink.mp4", "act":1, "covers_scene_id":"S043", "subtype":"answering_machine_blink" }
{ "public_path":"robosigning/factory/FC047_letterbox_mail_pile.mp4", "act":1, "covers_scene_id":"S044", "subtype":"letterbox_mail_pile" }
{ "public_path":"robosigning/factory/FC048_certified_envelope_macro.mp4", "act":1, "covers_scene_id":"S045", "subtype":"certified_envelope_macro" }
{ "public_path":"robosigning/factory/FC049_kitchen_table_paperwork_spread.mp4", "act":1, "covers_scene_id":"S046", "subtype":"kitchen_table_paperwork_spread" }
{ "public_path":"robosigning/factory/FC050_reading_glasses_on_paper.mp4", "act":1, "covers_scene_id":"S047", "subtype":"reading_glasses_on_paper" }
{ "public_path":"robosigning/factory/FC051_interstate_sign_north_night.mp4", "act":1, "covers_scene_id":"S048", "subtype":"interstate_sign_north_night" }
{ "public_path":"robosigning/factory/FC052_windshield_long_drive_night.mp4", "act":1, "covers_scene_id":"S049", "subtype":"windshield_long_drive_night" }

// ACT II (act 2) -- 34
{ "public_path":"robosigning/factory/FC053_call_centre_headset_backs.mp4", "act":2, "covers_scene_id":"S050", "subtype":"call_centre_headset_backs" }
{ "public_path":"robosigning/factory/FC054_phone_bank_cubicles_wide.mp4", "act":2, "covers_scene_id":"S051", "subtype":"phone_bank_cubicles_wide" }
{ "public_path":"robosigning/factory/FC055_phone_receiver_on_hold.mp4", "act":2, "covers_scene_id":"S052", "subtype":"phone_receiver_on_hold" }
{ "public_path":"robosigning/factory/FC056_fax_machine_feeding_paper.mp4", "act":2, "covers_scene_id":"S053", "subtype":"fax_machine_feeding_paper" }
{ "public_path":"robosigning/factory/FC057_photocopier_light_bar_pass.mp4", "act":2, "covers_scene_id":"S054", "subtype":"photocopier_light_bar_pass" }
{ "public_path":"robosigning/factory/FC058_printer_output_tray_stack.mp4", "act":2, "covers_scene_id":"S055", "subtype":"printer_output_tray_stack" }
{ "public_path":"robosigning/factory/FC059_mail_sorting_trays_office.mp4", "act":2, "covers_scene_id":"S056", "subtype":"mail_sorting_trays_office" }
{ "public_path":"robosigning/factory/FC060_courier_box_of_files.mp4", "act":2, "covers_scene_id":"S057", "subtype":"courier_box_of_files" }
{ "public_path":"robosigning/factory/FC061_warehouse_of_boxes_aisle.mp4", "act":2, "covers_scene_id":"S058", "subtype":"warehouse_of_boxes_aisle" }
{ "public_path":"robosigning/factory/FC062_barcode_scanner_macro.mp4", "act":2, "covers_scene_id":"S059", "subtype":"barcode_scanner_macro" }
{ "public_path":"robosigning/factory/FC063_conveyor_paper_flow.mp4", "act":2, "covers_scene_id":"S060", "subtype":"conveyor_paper_flow" }
{ "public_path":"robosigning/factory/FC064_shredder_teeth_macro.mp4", "act":2, "covers_scene_id":"S061", "subtype":"shredder_teeth_macro" }
{ "public_path":"robosigning/factory/FC065_rubber_stamp_ink_pad.mp4", "act":2, "covers_scene_id":"S062", "subtype":"rubber_stamp_ink_pad" }
{ "public_path":"robosigning/factory/FC066_stamp_wheel_rotate_macro.mp4", "act":2, "covers_scene_id":"S063", "subtype":"stamp_wheel_rotate_macro" }
{ "public_path":"robosigning/factory/FC067_signature_line_blank_macro.mp4", "act":2, "covers_scene_id":"S064", "subtype":"signature_line_blank_macro" }
{ "public_path":"robosigning/factory/FC068_pen_passing_between_hands.mp4", "act":2, "covers_scene_id":"S065", "subtype":"pen_passing_between_hands" }
{ "public_path":"robosigning/factory/FC069_clipboard_stack_desk.mp4", "act":2, "covers_scene_id":"S066", "subtype":"clipboard_stack_desk" }
{ "public_path":"robosigning/factory/FC070_in_tray_overflowing.mp4", "act":2, "covers_scene_id":"S067", "subtype":"in_tray_overflowing" }
{ "public_path":"robosigning/factory/FC071_desk_lamp_late_night_office.mp4", "act":2, "covers_scene_id":"S068", "subtype":"desk_lamp_late_night_office" }
{ "public_path":"robosigning/factory/FC072_empty_office_floor_night.mp4", "act":2, "covers_scene_id":"S069", "subtype":"empty_office_floor_night" }
{ "public_path":"robosigning/factory/FC073_cubicle_maze_overhead.mp4", "act":2, "covers_scene_id":"S070", "subtype":"cubicle_maze_overhead" }
{ "public_path":"robosigning/factory/FC074_keyboard_typing_hands_cu.mp4", "act":2, "covers_scene_id":"S071", "subtype":"keyboard_typing_hands_cu" }
{ "public_path":"robosigning/factory/FC075_monitor_glow_face_shadow.mp4", "act":2, "covers_scene_id":"S072", "subtype":"monitor_glow_face_shadow" }
{ "public_path":"robosigning/factory/FC076_server_rack_lights.mp4", "act":2, "covers_scene_id":"S073", "subtype":"server_rack_lights" }
{ "public_path":"robosigning/factory/FC077_spreadsheet_screen_blur.mp4", "act":2, "covers_scene_id":"S074", "subtype":"spreadsheet_screen_blur" }
{ "public_path":"robosigning/factory/FC078_folder_cart_wheeled_corridor.mp4", "act":2, "covers_scene_id":"S075", "subtype":"folder_cart_wheeled_corridor" }
{ "public_path":"robosigning/factory/FC079_office_elevator_doors_closing.mp4", "act":2, "covers_scene_id":"S076", "subtype":"office_elevator_doors_closing" }
{ "public_path":"robosigning/factory/FC080_lobby_revolving_door_backs.mp4", "act":2, "covers_scene_id":"S077", "subtype":"lobby_revolving_door_backs" }
{ "public_path":"robosigning/factory/FC081_badge_reader_door.mp4", "act":2, "covers_scene_id":"S078", "subtype":"badge_reader_door" }
{ "public_path":"robosigning/factory/FC082_water_cooler_corridor.mp4", "act":2, "covers_scene_id":"S079", "subtype":"water_cooler_corridor" }
{ "public_path":"robosigning/factory/FC083_whiteboard_wiped_clean.mp4", "act":2, "covers_scene_id":"S080", "subtype":"whiteboard_wiped_clean" }
{ "public_path":"robosigning/factory/FC084_office_wall_clock_cu.mp4", "act":2, "covers_scene_id":"S081", "subtype":"office_wall_clock_cu" }
{ "public_path":"robosigning/factory/FC085_paper_coffee_cup_desk.mp4", "act":2, "covers_scene_id":"S082", "subtype":"paper_coffee_cup_desk" }
{ "public_path":"robosigning/factory/FC086_night_cleaner_corridor_backs.mp4", "act":2, "covers_scene_id":"S083", "subtype":"night_cleaner_corridor_backs" }

// ACT III (act 3) -- 36
{ "public_path":"robosigning/factory/FC087_courthouse_exterior_stone_day.mp4", "act":3, "covers_scene_id":"S084", "subtype":"courthouse_exterior_stone_day" }
{ "public_path":"robosigning/factory/FC088_courthouse_steps_empty.mp4", "act":3, "covers_scene_id":"S085", "subtype":"courthouse_steps_empty" }
{ "public_path":"robosigning/factory/FC089_courthouse_corridor_marble.mp4", "act":3, "covers_scene_id":"S086", "subtype":"courthouse_corridor_marble" }
{ "public_path":"robosigning/factory/FC090_courtroom_bench_empty_wide.mp4", "act":3, "covers_scene_id":"S087", "subtype":"courtroom_bench_empty_wide" }
{ "public_path":"robosigning/factory/FC091_courtroom_gallery_seats_empty.mp4", "act":3, "covers_scene_id":"S088", "subtype":"courtroom_gallery_seats_empty" }
{ "public_path":"robosigning/factory/FC092_witness_chair_empty.mp4", "act":3, "covers_scene_id":"S089", "subtype":"witness_chair_empty" }
{ "public_path":"robosigning/factory/FC093_clerk_counter_stack_filings.mp4", "act":3, "covers_scene_id":"S090", "subtype":"clerk_counter_stack_filings" }
{ "public_path":"robosigning/factory/FC094_case_file_boxes_trolley.mp4", "act":3, "covers_scene_id":"S091", "subtype":"case_file_boxes_trolley" }
{ "public_path":"robosigning/factory/FC095_stenotype_machine_cu.mp4", "act":3, "covers_scene_id":"S092", "subtype":"stenotype_machine_cu" }
{ "public_path":"robosigning/factory/FC096_deposition_room_table_wide.mp4", "act":3, "covers_scene_id":"S093", "subtype":"deposition_room_table_wide" }
{ "public_path":"robosigning/factory/FC097_water_pitcher_glasses_table.mp4", "act":3, "covers_scene_id":"S094", "subtype":"water_pitcher_glasses_table" }
{ "public_path":"robosigning/factory/FC098_exhibit_sticker_on_folder.mp4", "act":3, "covers_scene_id":"S095", "subtype":"exhibit_sticker_on_folder" }
{ "public_path":"robosigning/factory/FC099_raised_hand_oath_silhouette.mp4", "act":3, "covers_scene_id":"S096", "subtype":"raised_hand_oath_silhouette" }
{ "public_path":"robosigning/factory/FC100_notary_journal_blank_page.mp4", "act":3, "covers_scene_id":"S097", "subtype":"notary_journal_blank_page" }
{ "public_path":"robosigning/factory/FC101_seal_embosser_macro.mp4", "act":3, "covers_scene_id":"S098", "subtype":"seal_embosser_macro" }
{ "public_path":"robosigning/factory/FC102_rubber_band_document_bundle.mp4", "act":3, "covers_scene_id":"S099", "subtype":"rubber_band_document_bundle" }
{ "public_path":"robosigning/factory/FC103_legal_pad_pen_notes_blur.mp4", "act":3, "covers_scene_id":"S100", "subtype":"legal_pad_pen_notes_blur" }
{ "public_path":"robosigning/factory/FC104_law_library_stacks_wide.mp4", "act":3, "covers_scene_id":"S101", "subtype":"law_library_stacks_wide" }
{ "public_path":"robosigning/factory/FC105_statute_volume_page_turn.mp4", "act":3, "covers_scene_id":"S102", "subtype":"statute_volume_page_turn" }
{ "public_path":"robosigning/factory/FC106_docket_board_hallway.mp4", "act":3, "covers_scene_id":"S103", "subtype":"docket_board_hallway" }
{ "public_path":"robosigning/factory/FC107_courthouse_flagpole_wind.mp4", "act":3, "covers_scene_id":"S104", "subtype":"courthouse_flagpole_wind" }
{ "public_path":"robosigning/factory/FC108_security_entry_backs.mp4", "act":3, "covers_scene_id":"S105", "subtype":"security_entry_backs" }
{ "public_path":"robosigning/factory/FC109_attorney_briefcase_walking.mp4", "act":3, "covers_scene_id":"S106", "subtype":"attorney_briefcase_walking" }
{ "public_path":"robosigning/factory/FC110_empty_jury_box_light.mp4", "act":3, "covers_scene_id":"S107", "subtype":"empty_jury_box_light" }
{ "public_path":"robosigning/factory/FC111_wooden_bench_grain_macro.mp4", "act":3, "covers_scene_id":"S108", "subtype":"wooden_bench_grain_macro" }
{ "public_path":"robosigning/factory/FC112_lectern_microphone_empty.mp4", "act":3, "covers_scene_id":"S109", "subtype":"lectern_microphone_empty" }
{ "public_path":"robosigning/factory/FC113_transcript_pages_riffle.mp4", "act":3, "covers_scene_id":"S110", "subtype":"transcript_pages_riffle" }
{ "public_path":"robosigning/factory/FC114_margin_marks_red_blur.mp4", "act":3, "covers_scene_id":"S111", "subtype":"margin_marks_red_blur" }
{ "public_path":"robosigning/factory/FC115_reel_tape_recorder_period.mp4", "act":3, "covers_scene_id":"S112", "subtype":"reel_tape_recorder_period" }
{ "public_path":"robosigning/factory/FC116_courthouse_dome_low_angle.mp4", "act":3, "covers_scene_id":"S113", "subtype":"courthouse_dome_low_angle" }
{ "public_path":"robosigning/factory/FC117_rain_on_courthouse_window.mp4", "act":3, "covers_scene_id":"S114", "subtype":"rain_on_courthouse_window" }
{ "public_path":"robosigning/factory/FC118_file_room_dark_aisle.mp4", "act":3, "covers_scene_id":"S115", "subtype":"file_room_dark_aisle" }
{ "public_path":"robosigning/factory/FC119_sealed_envelope_generic.mp4", "act":3, "covers_scene_id":"S116", "subtype":"sealed_envelope_generic" }
{ "public_path":"robosigning/factory/FC120_binder_row_shelf.mp4", "act":3, "covers_scene_id":"S117", "subtype":"binder_row_shelf" }
{ "public_path":"robosigning/factory/FC121_gavel_block_resting.mp4", "act":3, "covers_scene_id":"S118", "subtype":"gavel_block_resting" }
{ "public_path":"robosigning/factory/FC122_courthouse_lights_on_evening.mp4", "act":3, "covers_scene_id":"S119", "subtype":"courthouse_lights_on_evening" }

// ACT IV (act 4) -- 38
{ "public_path":"robosigning/factory/FC123_industrial_park_lowrise_day.mp4", "act":4, "covers_scene_id":"S120", "subtype":"industrial_park_lowrise_day" }
{ "public_path":"robosigning/factory/FC124_office_park_lot_empty.mp4", "act":4, "covers_scene_id":"S121", "subtype":"office_park_lot_empty" }
{ "public_path":"robosigning/factory/FC125_warehouse_loading_dock.mp4", "act":4, "covers_scene_id":"S122", "subtype":"warehouse_loading_dock" }
{ "public_path":"robosigning/factory/FC126_fluorescent_tube_flicker.mp4", "act":4, "covers_scene_id":"S123", "subtype":"fluorescent_tube_flicker" }
{ "public_path":"robosigning/factory/FC127_assembly_line_generic.mp4", "act":4, "covers_scene_id":"S124", "subtype":"assembly_line_generic" }
{ "public_path":"robosigning/factory/FC128_factory_floor_overhead_wide.mp4", "act":4, "covers_scene_id":"S125", "subtype":"factory_floor_overhead_wide" }
{ "public_path":"robosigning/factory/FC129_rows_of_identical_desks.mp4", "act":4, "covers_scene_id":"S126", "subtype":"rows_of_identical_desks" }
{ "public_path":"robosigning/factory/FC130_pallet_of_paper_reams.mp4", "act":4, "covers_scene_id":"S127", "subtype":"pallet_of_paper_reams" }
{ "public_path":"robosigning/factory/FC131_paper_ream_wrapper_macro.mp4", "act":4, "covers_scene_id":"S128", "subtype":"paper_ream_wrapper_macro" }
{ "public_path":"robosigning/factory/FC132_boxes_of_pens_open.mp4", "act":4, "covers_scene_id":"S129", "subtype":"boxes_of_pens_open" }
{ "public_path":"robosigning/factory/FC133_hands_signing_repetition_macro.mp4", "act":4, "covers_scene_id":"S130", "subtype":"hands_signing_repetition_macro" }
{ "public_path":"robosigning/factory/FC134_wrist_writing_motion_loop.mp4", "act":4, "covers_scene_id":"S131", "subtype":"wrist_writing_motion_loop" }
{ "public_path":"robosigning/factory/FC135_stopwatch_face_cu.mp4", "act":4, "covers_scene_id":"S132", "subtype":"stopwatch_face_cu" }
{ "public_path":"robosigning/factory/FC136_counter_display_incrementing.mp4", "act":4, "covers_scene_id":"S133", "subtype":"counter_display_incrementing" }
{ "public_path":"robosigning/factory/FC137_wall_of_filing_boxes.mp4", "act":4, "covers_scene_id":"S134", "subtype":"wall_of_filing_boxes" }
{ "public_path":"robosigning/factory/FC138_mail_bin_full_envelopes.mp4", "act":4, "covers_scene_id":"S135", "subtype":"mail_bin_full_envelopes" }
{ "public_path":"robosigning/factory/FC139_postal_sorting_machine.mp4", "act":4, "covers_scene_id":"S136", "subtype":"postal_sorting_machine" }
{ "public_path":"robosigning/factory/FC140_truck_leaving_dock_night.mp4", "act":4, "covers_scene_id":"S137", "subtype":"truck_leaving_dock_night" }
{ "public_path":"robosigning/factory/FC141_freight_highway_night.mp4", "act":4, "covers_scene_id":"S138", "subtype":"freight_highway_night" }
{ "public_path":"robosigning/factory/FC142_records_public_counter.mp4", "act":4, "covers_scene_id":"S139", "subtype":"records_public_counter" }
{ "public_path":"robosigning/factory/FC143_recorded_page_being_stamped.mp4", "act":4, "covers_scene_id":"S140", "subtype":"recorded_page_being_stamped" }
{ "public_path":"robosigning/factory/FC144_microfiche_drawer_pull.mp4", "act":4, "covers_scene_id":"S141", "subtype":"microfiche_drawer_pull" }
{ "public_path":"robosigning/factory/FC145_press_lectern_empty.mp4", "act":4, "covers_scene_id":"S142", "subtype":"press_lectern_empty" }
{ "public_path":"robosigning/factory/FC146_state_capitol_exterior.mp4", "act":4, "covers_scene_id":"S143", "subtype":"state_capitol_exterior" }
{ "public_path":"robosigning/factory/FC147_government_building_columns_day.mp4", "act":4, "covers_scene_id":"S144", "subtype":"government_building_columns_day" }
{ "public_path":"robosigning/factory/FC148_monitor_wall_newsroom_blur.mp4", "act":4, "covers_scene_id":"S145", "subtype":"monitor_wall_newsroom_blur" }
{ "public_path":"robosigning/factory/FC149_newspaper_press_rolling.mp4", "act":4, "covers_scene_id":"S146", "subtype":"newspaper_press_rolling" }
{ "public_path":"robosigning/factory/FC150_newsprint_bundles_stack.mp4", "act":4, "covers_scene_id":"S147", "subtype":"newsprint_bundles_stack" }
{ "public_path":"robosigning/factory/FC151_screen_wall_static_blur.mp4", "act":4, "covers_scene_id":"S148", "subtype":"screen_wall_static_blur" }
{ "public_path":"robosigning/factory/FC152_bank_branch_exterior_generic.mp4", "act":4, "covers_scene_id":"S149", "subtype":"bank_branch_exterior_generic" }
{ "public_path":"robosigning/factory/FC153_atm_vestibule_night.mp4", "act":4, "covers_scene_id":"S150", "subtype":"atm_vestibule_night" }
{ "public_path":"robosigning/factory/FC154_vault_door_generic.mp4", "act":4, "covers_scene_id":"S151", "subtype":"vault_door_generic" }
{ "public_path":"robosigning/factory/FC155_boardroom_empty_long_table.mp4", "act":4, "covers_scene_id":"S152", "subtype":"boardroom_empty_long_table" }
{ "public_path":"robosigning/factory/FC156_conference_phone_speaker_cu.mp4", "act":4, "covers_scene_id":"S153", "subtype":"conference_phone_speaker_cu" }
{ "public_path":"robosigning/factory/FC157_hearing_room_dais_empty.mp4", "act":4, "covers_scene_id":"S154", "subtype":"hearing_room_dais_empty" }
{ "public_path":"robosigning/factory/FC158_reporters_backs_gallery.mp4", "act":4, "covers_scene_id":"S155", "subtype":"reporters_backs_gallery" }
{ "public_path":"robosigning/factory/FC159_microphone_cluster_press.mp4", "act":4, "covers_scene_id":"S156", "subtype":"microphone_cluster_press" }
{ "public_path":"robosigning/factory/FC160_capital_facade_dusk.mp4", "act":4, "covers_scene_id":"S157", "subtype":"capital_facade_dusk" }

// ACT V (act 5) -- 36
{ "public_path":"robosigning/factory/FC161_cheque_printing_machine.mp4", "act":5, "covers_scene_id":"S158", "subtype":"cheque_printing_machine" }
{ "public_path":"robosigning/factory/FC162_envelope_stuffing_machine.mp4", "act":5, "covers_scene_id":"S159", "subtype":"envelope_stuffing_machine" }
{ "public_path":"robosigning/factory/FC163_postal_mailbag_pile.mp4", "act":5, "covers_scene_id":"S160", "subtype":"postal_mailbag_pile" }
{ "public_path":"robosigning/factory/FC164_apartment_mailbox_bank.mp4", "act":5, "covers_scene_id":"S161", "subtype":"apartment_mailbox_bank" }
{ "public_path":"robosigning/factory/FC165_cheque_in_hand_macro_blur.mp4", "act":5, "covers_scene_id":"S162", "subtype":"cheque_in_hand_macro_blur" }
{ "public_path":"robosigning/factory/FC166_deposit_counter_slip.mp4", "act":5, "covers_scene_id":"S163", "subtype":"deposit_counter_slip" }
{ "public_path":"robosigning/factory/FC167_returned_envelope_marked_macro.mp4", "act":5, "covers_scene_id":"S164", "subtype":"returned_envelope_marked_macro" }
{ "public_path":"robosigning/factory/FC168_calculator_tape_printing.mp4", "act":5, "covers_scene_id":"S165", "subtype":"calculator_tape_printing" }
{ "public_path":"robosigning/factory/FC169_adding_machine_period.mp4", "act":5, "covers_scene_id":"S166", "subtype":"adding_machine_period" }
{ "public_path":"robosigning/factory/FC170_coin_stack_macro.mp4", "act":5, "covers_scene_id":"S167", "subtype":"coin_stack_macro" }
{ "public_path":"robosigning/factory/FC171_banknotes_fanned_blur.mp4", "act":5, "covers_scene_id":"S168", "subtype":"banknotes_fanned_blur" }
{ "public_path":"robosigning/factory/FC172_bank_vault_interior_generic.mp4", "act":5, "covers_scene_id":"S169", "subtype":"bank_vault_interior_generic" }
{ "public_path":"robosigning/factory/FC173_sentencing_courtroom_empty.mp4", "act":5, "covers_scene_id":"S170", "subtype":"sentencing_courtroom_empty" }
{ "public_path":"robosigning/factory/FC174_federal_building_exterior.mp4", "act":5, "covers_scene_id":"S171", "subtype":"federal_building_exterior" }
{ "public_path":"robosigning/factory/FC175_fence_daylight_neutral.mp4", "act":5, "covers_scene_id":"S172", "subtype":"fence_daylight_neutral" }
{ "public_path":"robosigning/factory/FC176_institutional_corridor_door.mp4", "act":5, "covers_scene_id":"S173", "subtype":"institutional_corridor_door" }
{ "public_path":"robosigning/factory/FC177_visitor_room_chairs_empty.mp4", "act":5, "covers_scene_id":"S174", "subtype":"visitor_room_chairs_empty" }
{ "public_path":"robosigning/factory/FC178_podium_press_paper.mp4", "act":5, "covers_scene_id":"S175", "subtype":"podium_press_paper" }
{ "public_path":"robosigning/factory/FC179_hearing_seats_row.mp4", "act":5, "covers_scene_id":"S177", "subtype":"hearing_seats_row" }
{ "public_path":"robosigning/factory/FC180_audit_binders_row.mp4", "act":5, "covers_scene_id":"S178", "subtype":"audit_binders_row" }
{ "public_path":"robosigning/factory/FC181_consultant_office_glass_wall.mp4", "act":5, "covers_scene_id":"S179", "subtype":"consultant_office_glass_wall" }
{ "public_path":"robosigning/factory/FC182_invoice_stack_macro.mp4", "act":5, "covers_scene_id":"S180", "subtype":"invoice_stack_macro" }
{ "public_path":"robosigning/factory/FC183_printed_report_charts_blur.mp4", "act":5, "covers_scene_id":"S181", "subtype":"printed_report_charts_blur" }
{ "public_path":"robosigning/factory/FC184_deadline_calendar_blur.mp4", "act":5, "covers_scene_id":"S182", "subtype":"deadline_calendar_blur" }
{ "public_path":"robosigning/factory/FC185_abandoned_house_overgrown.mp4", "act":5, "covers_scene_id":"S183", "subtype":"abandoned_house_overgrown" }
{ "public_path":"robosigning/factory/FC186_boarded_window_plywood.mp4", "act":5, "covers_scene_id":"S184", "subtype":"boarded_window_plywood" }
{ "public_path":"robosigning/factory/FC187_notice_taped_to_door_blur.mp4", "act":5, "covers_scene_id":"S185", "subtype":"notice_taped_to_door_blur" }
{ "public_path":"robosigning/factory/FC188_lockbox_on_doorknob_cu.mp4", "act":5, "covers_scene_id":"S186", "subtype":"lockbox_on_doorknob_cu" }
{ "public_path":"robosigning/factory/FC189_realtor_key_safe_macro.mp4", "act":5, "covers_scene_id":"S187", "subtype":"realtor_key_safe_macro" }
{ "public_path":"robosigning/factory/FC190_empty_pool_leaves.mp4", "act":5, "covers_scene_id":"S188", "subtype":"empty_pool_leaves" }
{ "public_path":"robosigning/factory/FC191_moving_truck_ramp_down.mp4", "act":5, "covers_scene_id":"S189", "subtype":"moving_truck_ramp_down" }
{ "public_path":"robosigning/factory/FC192_street_of_empty_houses_dusk.mp4", "act":5, "covers_scene_id":"S190", "subtype":"street_of_empty_houses_dusk" }
{ "public_path":"robosigning/factory/FC193_rain_on_empty_driveway.mp4", "act":5, "covers_scene_id":"S191", "subtype":"rain_on_empty_driveway" }
{ "public_path":"robosigning/factory/FC194_mailbox_stuffed_flyers.mp4", "act":5, "covers_scene_id":"S192", "subtype":"mailbox_stuffed_flyers" }
{ "public_path":"robosigning/factory/FC195_leaning_sold_sign.mp4", "act":5, "covers_scene_id":"S193", "subtype":"leaning_sold_sign" }
{ "public_path":"robosigning/factory/FC196_sunset_suburb_wide.mp4", "act":5, "covers_scene_id":"S194", "subtype":"sunset_suburb_wide" }

// ENDING (act 6) -- 14
{ "public_path":"robosigning/factory/FC197_dawn_over_suburb_wide.mp4", "act":6, "covers_scene_id":"S196", "subtype":"dawn_over_suburb_wide" }
{ "public_path":"robosigning/factory/FC198_kitchen_light_on_morning.mp4", "act":6, "covers_scene_id":"S197", "subtype":"kitchen_light_on_morning" }
{ "public_path":"robosigning/factory/FC199_key_turning_in_lock_cu.mp4", "act":6, "covers_scene_id":"S198", "subtype":"key_turning_in_lock_cu" }
{ "public_path":"robosigning/factory/FC200_curtains_opening_light.mp4", "act":6, "covers_scene_id":"S199", "subtype":"curtains_opening_light" }
{ "public_path":"robosigning/factory/FC201_front_door_opening_inward.mp4", "act":6, "covers_scene_id":"S200", "subtype":"front_door_opening_inward" }
{ "public_path":"robosigning/factory/FC202_photo_rehung_on_wall_blur.mp4", "act":6, "covers_scene_id":"S201", "subtype":"photo_rehung_on_wall_blur" }
{ "public_path":"robosigning/factory/FC203_mower_morning_backs.mp4", "act":6, "covers_scene_id":"S202", "subtype":"mower_morning_backs" }
{ "public_path":"robosigning/factory/FC204_mailbox_flag_down.mp4", "act":6, "covers_scene_id":"S203", "subtype":"mailbox_flag_down" }
{ "public_path":"robosigning/factory/FC205_paper_stack_being_boxed.mp4", "act":6, "covers_scene_id":"S204", "subtype":"paper_stack_being_boxed" }
{ "public_path":"robosigning/factory/FC206_archive_shelf_closing.mp4", "act":6, "covers_scene_id":"S205", "subtype":"archive_shelf_closing" }
{ "public_path":"robosigning/factory/FC207_modern_office_2020s_screens.mp4", "act":6, "covers_scene_id":"S206", "subtype":"modern_office_2020s_screens" }
{ "public_path":"robosigning/factory/FC208_new_envelope_on_mat.mp4", "act":6, "covers_scene_id":"S207", "subtype":"new_envelope_on_mat" }
{ "public_path":"robosigning/factory/FC209_city_skyline_dusk_neutral.mp4", "act":6, "covers_scene_id":"S208", "subtype":"city_skyline_dusk_neutral" }
{ "public_path":"robosigning/factory/FC210_empty_desk_chair_endcard.mp4", "act":6, "covers_scene_id":"S209", "subtype":"empty_desk_chair_endcard" }

// CONNECTORS (covers_scene_id:null) -- 25
{ "public_path":"robosigning/factory/FC211_abstract_paper_texture_drift.mp4", "act":null, "covers_scene_id":null, "subtype":"abstract_paper_texture_drift" }
{ "public_path":"robosigning/factory/FC212_ink_bleed_macro.mp4", "act":null, "covers_scene_id":null, "subtype":"ink_bleed_macro" }
{ "public_path":"robosigning/factory/FC213_dust_motes_light_beam.mp4", "act":null, "covers_scene_id":null, "subtype":"dust_motes_light_beam" }
{ "public_path":"robosigning/factory/FC214_ceiling_fluorescent_hum.mp4", "act":null, "covers_scene_id":null, "subtype":"ceiling_fluorescent_hum" }
{ "public_path":"robosigning/factory/FC215_rain_on_glass_neutral.mp4", "act":null, "covers_scene_id":null, "subtype":"rain_on_glass_neutral" }
{ "public_path":"robosigning/factory/FC216_clouds_timelapse_neutral.mp4", "act":null, "covers_scene_id":null, "subtype":"clouds_timelapse_neutral" }
{ "public_path":"robosigning/factory/FC217_asphalt_road_lines_moving.mp4", "act":null, "covers_scene_id":null, "subtype":"asphalt_road_lines_moving" }
{ "public_path":"robosigning/factory/FC218_power_lines_passing_car.mp4", "act":null, "covers_scene_id":null, "subtype":"power_lines_passing_car" }
{ "public_path":"robosigning/factory/FC219_generic_flag_wind_slow.mp4", "act":null, "covers_scene_id":null, "subtype":"generic_flag_wind_slow" }
{ "public_path":"robosigning/factory/FC220_institutional_stairwell_down.mp4", "act":null, "covers_scene_id":null, "subtype":"institutional_stairwell_down" }
{ "public_path":"robosigning/factory/FC221_corridor_walk_backs_blur.mp4", "act":null, "covers_scene_id":null, "subtype":"corridor_walk_backs_blur" }
{ "public_path":"robosigning/factory/FC222_door_closing_slow_dark.mp4", "act":null, "covers_scene_id":null, "subtype":"door_closing_slow_dark" }
{ "public_path":"robosigning/factory/FC223_office_window_reflection.mp4", "act":null, "covers_scene_id":null, "subtype":"office_window_reflection" }
{ "public_path":"robosigning/factory/FC224_highway_overpass_traffic.mp4", "act":null, "covers_scene_id":null, "subtype":"highway_overpass_traffic" }
{ "public_path":"robosigning/factory/FC225_suburban_treeline_wind.mp4", "act":null, "covers_scene_id":null, "subtype":"suburban_treeline_wind" }
{ "public_path":"robosigning/factory/FC226_sprinkler_water_arc.mp4", "act":null, "covers_scene_id":null, "subtype":"sprinkler_water_arc" }
{ "public_path":"robosigning/factory/FC227_chain_link_fence_shadow.mp4", "act":null, "covers_scene_id":null, "subtype":"chain_link_fence_shadow" }
{ "public_path":"robosigning/factory/FC228_paper_falling_slow.mp4", "act":null, "covers_scene_id":null, "subtype":"paper_falling_slow" }
{ "public_path":"robosigning/factory/FC229_desk_drawer_opening_dark.mp4", "act":null, "covers_scene_id":null, "subtype":"desk_drawer_opening_dark" }
{ "public_path":"robosigning/factory/FC230_light_switch_off_room.mp4", "act":null, "covers_scene_id":null, "subtype":"light_switch_off_room" }
{ "public_path":"robosigning/factory/FC231_ceiling_tile_grid_pan.mp4", "act":null, "covers_scene_id":null, "subtype":"ceiling_tile_grid_pan" }
{ "public_path":"robosigning/factory/FC232_lobby_escalator_slow.mp4", "act":null, "covers_scene_id":null, "subtype":"lobby_escalator_slow" }
{ "public_path":"robosigning/factory/FC233_revolving_file_wheel.mp4", "act":null, "covers_scene_id":null, "subtype":"revolving_file_wheel" }
{ "public_path":"robosigning/factory/FC234_window_blinds_closing_slats.mp4", "act":null, "covers_scene_id":null, "subtype":"window_blinds_closing_slats" }
{ "public_path":"robosigning/factory/FC235_street_lamp_flicker_night.mp4", "act":null, "covers_scene_id":null, "subtype":"street_lamp_flicker_night" }

```

> **★被り禁止（`footage_diversity`）:** 上の 235 subtype は**すべて別物**。同一 subtype 名は1本もない。`gavel_block_resting` は本作唯一の gavel カットで、天秤・Lady Justice 像は **1本も採らない**（§1.2 R-NO-GAVEL-SPAM・generic symbols ≤2 を 1 で使い切る設計）。

## 4.5 ★`motion[]` 全42エントリ（★必ず実体化・public_path 非空）

> 各行は §8.1a の種プロンプト（`M<NN>_src.png`）→ Wan 2.2 A14B → RIFE 48fps の成果物。`public_path` は `robosigning/motion/M<NN>_rife.mp4`。**★HUMAN 印**の18本は §5.11 の匿名人物ビート（動く人間＝紙芝居回避の主戦力）。

```jsonc
// HOOK+OPENING (act 0) -- 3
{ "public_path":"robosigning/motion/M01_rife.mp4", "act":0, "covers_scene_id":"S002", "seed":"M01_src", "human":false }
{ "public_path":"robosigning/motion/M02_rife.mp4", "act":0, "covers_scene_id":"S006", "seed":"M02_src", "human":false }
{ "public_path":"robosigning/motion/M03_rife.mp4", "act":0, "covers_scene_id":"S012", "seed":"M03_src", "human":false }
// ACT I (act 1) -- 6
{ "public_path":"robosigning/motion/M04_rife.mp4", "act":1, "covers_scene_id":"S018", "seed":"M04_src", "human":true }
{ "public_path":"robosigning/motion/M05_rife.mp4", "act":1, "covers_scene_id":"S023", "seed":"M05_src", "human":false }
{ "public_path":"robosigning/motion/M06_rife.mp4", "act":1, "covers_scene_id":"S029", "seed":"M06_src", "human":true }
{ "public_path":"robosigning/motion/M07_rife.mp4", "act":1, "covers_scene_id":"S035", "seed":"M07_src", "human":false }
{ "public_path":"robosigning/motion/M08_rife.mp4", "act":1, "covers_scene_id":"S041", "seed":"M08_src", "human":true }
{ "public_path":"robosigning/motion/M09_rife.mp4", "act":1, "covers_scene_id":"S047", "seed":"M09_src", "human":false }
// ACT II (act 2) -- 6
{ "public_path":"robosigning/motion/M10_rife.mp4", "act":2, "covers_scene_id":"S052", "seed":"M10_src", "human":true }
{ "public_path":"robosigning/motion/M11_rife.mp4", "act":2, "covers_scene_id":"S057", "seed":"M11_src", "human":false }
{ "public_path":"robosigning/motion/M12_rife.mp4", "act":2, "covers_scene_id":"S063", "seed":"M12_src", "human":true }
{ "public_path":"robosigning/motion/M13_rife.mp4", "act":2, "covers_scene_id":"S069", "seed":"M13_src", "human":false }
{ "public_path":"robosigning/motion/M14_rife.mp4", "act":2, "covers_scene_id":"S075", "seed":"M14_src", "human":true }
{ "public_path":"robosigning/motion/M15_rife.mp4", "act":2, "covers_scene_id":"S081", "seed":"M15_src", "human":false }
// ACT III (act 3) -- 7
{ "public_path":"robosigning/motion/M16_rife.mp4", "act":3, "covers_scene_id":"S086", "seed":"M16_src", "human":false }
{ "public_path":"robosigning/motion/M17_rife.mp4", "act":3, "covers_scene_id":"S091", "seed":"M17_src", "human":true }
{ "public_path":"robosigning/motion/M18_rife.mp4", "act":3, "covers_scene_id":"S096", "seed":"M18_src", "human":false }
{ "public_path":"robosigning/motion/M19_rife.mp4", "act":3, "covers_scene_id":"S101", "seed":"M19_src", "human":true }
{ "public_path":"robosigning/motion/M20_rife.mp4", "act":3, "covers_scene_id":"S106", "seed":"M20_src", "human":false }
{ "public_path":"robosigning/motion/M21_rife.mp4", "act":3, "covers_scene_id":"S111", "seed":"M21_src", "human":true }
{ "public_path":"robosigning/motion/M22_rife.mp4", "act":3, "covers_scene_id":"S116", "seed":"M22_src", "human":false }
// ACT IV (act 4) -- 8
{ "public_path":"robosigning/motion/M23_rife.mp4", "act":4, "covers_scene_id":"S121", "seed":"M23_src", "human":false }
{ "public_path":"robosigning/motion/M24_rife.mp4", "act":4, "covers_scene_id":"S125", "seed":"M24_src", "human":true }
{ "public_path":"robosigning/motion/M25_rife.mp4", "act":4, "covers_scene_id":"S130", "seed":"M25_src", "human":false }
{ "public_path":"robosigning/motion/M26_rife.mp4", "act":4, "covers_scene_id":"S134", "seed":"M26_src", "human":true }
{ "public_path":"robosigning/motion/M27_rife.mp4", "act":4, "covers_scene_id":"S139", "seed":"M27_src", "human":false }
{ "public_path":"robosigning/motion/M28_rife.mp4", "act":4, "covers_scene_id":"S143", "seed":"M28_src", "human":true }
{ "public_path":"robosigning/motion/M29_rife.mp4", "act":4, "covers_scene_id":"S148", "seed":"M29_src", "human":false }
{ "public_path":"robosigning/motion/M30_rife.mp4", "act":4, "covers_scene_id":"S153", "seed":"M30_src", "human":true }
// ACT V (act 5) -- 8
{ "public_path":"robosigning/motion/M31_rife.mp4", "act":5, "covers_scene_id":"S159", "seed":"M31_src", "human":false }
{ "public_path":"robosigning/motion/M32_rife.mp4", "act":5, "covers_scene_id":"S163", "seed":"M32_src", "human":true }
{ "public_path":"robosigning/motion/M33_rife.mp4", "act":5, "covers_scene_id":"S168", "seed":"M33_src", "human":false }
{ "public_path":"robosigning/motion/M34_rife.mp4", "act":5, "covers_scene_id":"S172", "seed":"M34_src", "human":true }
{ "public_path":"robosigning/motion/M35_rife.mp4", "act":5, "covers_scene_id":"S177", "seed":"M35_src", "human":false }
{ "public_path":"robosigning/motion/M36_rife.mp4", "act":5, "covers_scene_id":"S181", "seed":"M36_src", "human":true }
{ "public_path":"robosigning/motion/M37_rife.mp4", "act":5, "covers_scene_id":"S186", "seed":"M37_src", "human":false }
{ "public_path":"robosigning/motion/M38_rife.mp4", "act":5, "covers_scene_id":"S191", "seed":"M38_src", "human":true }
// ENDING (act 6) -- 4
{ "public_path":"robosigning/motion/M39_rife.mp4", "act":6, "covers_scene_id":"S197", "seed":"M39_src", "human":false }
{ "public_path":"robosigning/motion/M40_rife.mp4", "act":6, "covers_scene_id":"S201", "seed":"M40_src", "human":true }
{ "public_path":"robosigning/motion/M41_rife.mp4", "act":6, "covers_scene_id":"S205", "seed":"M41_src", "human":false }
{ "public_path":"robosigning/motion/M42_rife.mp4", "act":6, "covers_scene_id":"S209", "seed":"M42_src", "human":false }
```

> **★HUMAN 18本 = M04 M06 M08 · M10 M12 M14 · M17 M19 M21 · M24 M26 M28 M30 · M32 M34 M36 M38 · M40。** §5.11 の H001–H018 と一対一で対応（§5.11 末尾の対応表）。

## 4.6 `overlay[]` 30エントリ（distinct 素材に数えない・15 particle / 10 light / 5 vfx）

```jsonc
// particle 15
{ "public_path":"robosigning/overlay/OV01_paper_dust_slow.mp4",       "class":"particle" }
{ "public_path":"robosigning/overlay/OV02_paper_dust_dense.mp4",      "class":"particle" }
{ "public_path":"robosigning/overlay/OV03_office_dust_beam.mp4",      "class":"particle" }
{ "public_path":"robosigning/overlay/OV04_toner_speck_drift.mp4",     "class":"particle" }
{ "public_path":"robosigning/overlay/OV05_lint_float_dark.mp4",       "class":"particle" }
{ "public_path":"robosigning/overlay/OV06_pollen_outdoor_warm.mp4",   "class":"particle" }
{ "public_path":"robosigning/overlay/OV07_rain_specks_glass.mp4",     "class":"particle" }
{ "public_path":"robosigning/overlay/OV08_ash_fine_fall.mp4",         "class":"particle" }
{ "public_path":"robosigning/overlay/OV09_grain_fine_neutral.mp4",    "class":"particle" }
{ "public_path":"robosigning/overlay/OV10_grain_coarse_neutral.mp4",  "class":"particle" }
{ "public_path":"robosigning/overlay/OV11_ink_particle_bloom.mp4",    "class":"particle" }
{ "public_path":"robosigning/overlay/OV12_fibre_paper_macro.mp4",     "class":"particle" }
{ "public_path":"robosigning/overlay/OV13_night_insects_porch.mp4",   "class":"particle" }
{ "public_path":"robosigning/overlay/OV14_sea_haze_particle.mp4",     "class":"particle" }
{ "public_path":"robosigning/overlay/OV15_static_speck_screen.mp4",   "class":"particle" }
// light 10
{ "public_path":"robosigning/overlay/OV16_fluorescent_flicker.mp4",   "class":"light" }
{ "public_path":"robosigning/overlay/OV17_window_slat_sweep.mp4",     "class":"light" }
{ "public_path":"robosigning/overlay/OV18_headlight_pass_sweep.mp4",  "class":"light" }
{ "public_path":"robosigning/overlay/OV19_porch_lamp_bloom.mp4",      "class":"light" }
{ "public_path":"robosigning/overlay/OV20_desk_lamp_falloff.mp4",     "class":"light" }
{ "public_path":"robosigning/overlay/OV21_morning_warm_edge.mp4",     "class":"light" }
{ "public_path":"robosigning/overlay/OV22_teal_edge_glow.mp4",        "class":"light" }
{ "public_path":"robosigning/overlay/OV23_photocopier_bar_pass.mp4",  "class":"light" }
{ "public_path":"robosigning/overlay/OV24_streetlamp_halo_night.mp4", "class":"light" }
{ "public_path":"robosigning/overlay/OV25_screen_glow_soft.mp4",      "class":"light" }
// vfx 5
{ "public_path":"robosigning/overlay/OV26_paper_edge_wipe.mp4",       "class":"vfx" }
{ "public_path":"robosigning/overlay/OV27_ink_bleed_transition.mp4",  "class":"vfx" }
{ "public_path":"robosigning/overlay/OV28_stack_shuffle_wipe.mp4",    "class":"vfx" }
{ "public_path":"robosigning/overlay/OV29_stamp_impact_shake.mp4",    "class":"vfx" }
{ "public_path":"robosigning/overlay/OV30_slow_dissolve_grain.mp4",   "class":"vfx" }
```

> **overlay は screen/add で薄く重ねる補助。単独カットにしない・`distinct` に数えない。** 全体の screen-wash 不透明度は **≤0.07**（DESIGN §0-4 の "no wash" 規定）。milky haze / scanline / CRT テクスチャ / 黄色ウォッシュは**作らない**。

---


# 5. A-1: SDXL 静止画のバッチ生成（210本 × 1枚・バリエーション0）— ★motif ライブラリ方式

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-059-robosigning/04_scenes/ai_prompts.v001.md   <- A が §5.9 の形式で書く
出力:  H:\pd-media\assets\ai\robosigning\S<NNN>.png（+ remotion/public/robosigning/ に自動コピー）
2段パイプライン: txt2img 1536x864 -> hires 3072x1728 -> extras R-ESRGAN 4x+ -> 3840x2160（長辺>=3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★210本の作り方＝「motif ライブラリ」テンプレート方式

210 の固有プロンプトを**幕×motifで体系化**する。各 motif に (a) **確定 distinct 枚数**、(b) **S番号レンジ**、(c) **literal プロンプト** を与える。**§5.6 は S001–S210 の全210行を literal 化済み。Codex は各行の**創作部分をそのまま**`ai_prompts.v001.md` に転記する（変奏を新たに書かない・行を増減しない・S番号を並べ替えない）。**
> ★★ **R3 BLOCKER FIX 2026-07-29 — マクロは必ず展開する。** 行末の `[STYLE]`/`[HSTYLE]`/`[TSTYLE]`/`[FSTYLE]` と `Avoid:` 直後の `[NEG]`/`[HNEG]`/`[TNEG]`/`[FNEG]` は、**§5.3 / §5.4 / §5.11 / §5.12 / §5.13 の全文に展開して書く**こと。`scripts/generate_sdxl_4k.py` はマクロ置換を一切行わない（L74–87 で `Avoid:` を分割してそのまま渡すだけ）ので、トークンのまま転記すると **267枚全部で「判読不能化」指示と 155語の禁止リストが丸ごと消える**（残るのはスクリプト内の `DEFAULT_NEG` だけで、`letters` / `numerals` / `legible affidavit` / `government seal` / `handcuffs` / `child` を含まない）。§5.10 の smoke test（`--only S001` → `shots=255`）は **展開してもしなくても同じく通る**ので、これを捕まえるゲートは下の grep しかない。
> ```
> # 展開確認（必須・§5.10 と [A-DONE-3] の直前に実行）
> grep -c '\[STYLE\]\|\[NEG\]\|\[HSTYLE\]\|\[HNEG\]\|\[TSTYLE\]\|\[TNEG\]\|\[FSTYLE\]\|\[FNEG\]' episodes/PD-2026-059-robosigning/04_scenes/ai_prompts.v001.md
> #   → **0 以外なら形式が壊れている。生成を開始してはいけない。**
> ```

> ★**1シーン1枚・variants 0。** 各プロンプト末尾に §5.3 の `[STYLE]`（人物なし象徴 still）**または** §5.11 の `[HSTYLE]`（匿名人物 still）を**全文連結**、`Avoid:` の後に §5.4 `[NEG]`（象徴）**または** §5.11 `[HNEG]`（匿名人物）を**全文連結**。
> **★2レーン構成: 210 body = object/symbolic 122枚（`[STYLE]`+`[NEG]`・人物なし）＋ ★human-present 88枚（41.9%・`[HSTYLE]`+`[HNEG]`・匿名/非識別・背向き/影/silhouette/hands・adults only）。** 該当 S-range は §5.6 で `★HP` と明記。
> **HARD BAN（不変・両レーン共通）: 判読可能な署名/文字/金額なし・実在人物 likeness なし・実在ロゴ/印章なし・強制退去の扇情描写なし・識別可能な子供顔なし。**

## 5.3 共通スタイル `[STYLE]`（body の象徴 still ＋ 抽象 i2v 種に連結・DESIGN §1 と一字一致）

```
, cinematic still, somber documentary grade, a deep recorder's-stamp teal as the one recurring system colour used on ink, stamps, type surfaces and paper edges, near-black ink institutional gravity, American 1998-2026 rendered in period-correct detail, a flat printed notice-orange reserved strictly for a posted notice, an auction placard, a lockbox tag or a returned envelope and never flooding the frame, a single warm paid-in-full morning note reserved only for the cash-purchase beats and the restored-house ending, every sheet of paper and every signature rendered as an abstract illegible smear with no letterforms and no numerals, a small realtor lockbox hanging on a door handle as the dread object, a stack of identical documents as the accumulating object, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, empty rooms as aftermath, objects and shadows only
```

> **EP39〜EP58 の色語（1語も含めない）:** electric blue / sodium prison gold / porch-amber / teal-green hospital（**淡い病院内装のグリーンティール。本作の recorder's-stamp teal は濃く飽和した"インクの"ティールで、内装ではなく紙・スタンプ・タイポにしか乗らない**）/ crimson kitchen / forest-green / civil-violet / somber-plum / steel-cyan（EP50）/ cold evidence bandana-blue（EP52）/ interrogation fluorescent green-gray（EP55）/ post-office signage red・phantom-ledger phosphor green・shop-lamp amber（EP56）。
> **EP59 の色 = recorder's-stamp teal `#0F6E68`（INK `#0A0B0D` / bone `#EDEAE2`）＋ 掲示物のみ notice-orange `#D4692A`（≤8枚）＋ 冒頭と末尾のみ paid-in-full morning `#F0DFB4`。**

## 5.4 共通ネガティブ `[NEG]`（各 `Avoid:` の後に全文付ける・A/B 同一）

```
text, words, letters, numbers, numerals, captions, watermark, logo, brand mark, bank logo, corporate name, government seal, state seal, federal seal, readable document, legible affidavit, legible deed, legible notice, legible cheque, legible court record, legible bank statement, legible date, legible signature, readable signature, a signature with recognisable letters, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, front-facing person, handcuffs, police restraint, sheriff forcing a door on a family, family being dragged out, belongings thrown on the street, weeping face, screaming face, blood, gore, injury, corpse, violence, weapon, re-enactment of an arrest, child, identifiable child face, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, evidence-blue bandana, interrogation green-gray, signage red, phosphor green, shop-lamp amber, milky haze, foggy wash, yellow wash, scanline, CRT texture, vignette wash
```

> 文字/紙面が必要な絵は「blurred into an unreadable smear」で判読不能に。**署名は "an abstract illegible ink stroke" のみ。** この `[NEG]` は象徴 body ＋ 抽象 i2v 種にのみ使う。**人物ビート（§5.11 H シリーズ・§5.12 thumb_face・§5.13 F シリーズ）には使わない**（人物を弾くため）。H/thumb/F は `[HNEG]`/`[TNEG]`/`[FNEG]` を使う。

## 5.5 プロンプトの絶対ルール（210本すべてに適用）

- **body 210 は2レーン（§5.2）:** object/symbolic 122枚＝§5.3/§5.4（人物なし）、**human-present 88枚（41.9%）＝§5.11 `[HSTYLE]`/`[HNEG]`**。
- **可読文字・可読数字なし。** affidavit/deed/notice/小切手/判決/明細/ロゴ/印章/金額を描かない。
- ★★ **R3 2026-07-29 — 末尾の `no readable text` だけに依存しないこと（生成前の必須スイープ）。** 監査で、ページの表面が画面に入るのに本文側の判読不能化指示がなく、末尾の `no readable text` だけで受けている行が **約15行**見つかった（S042 / S046 / S069 / S071 / S111 / S123 / S128 / S129 / S162 / S174 / S181 / S204 / M14_src / M17_src / M34_src。うち S071・S162 は R3 で修正済み、S181 は `also_thumb` アンカーで特に危険）。**残りの行は生成前に本文へ `, every page an unreadable smear`（単一の紙なら `, its printed surface an unreadable smear`）を挿入すること。** 判読不能化を `[STYLE]`/`[HSTYLE]` サフィックスの末尾句に任せると、CLIP のチャンク3以降に落ちて先頭の `page` / `sheet` 名詞への結合が弱くなる。
- ★ **`DEFAULT_NEG` の罠。** `scripts/generate_sdxl_4k.py` は全行のネガに無条件でトークン `signature` を追加する。**インクのストロークそのものが主題の行（S007 / S127 / S130 / S138 / S159 / S165 / M01_src / M23_src / M25_src）ではこれが主題を押し潰す。** だから正プロンプト側では `signature` という語を使わず、`wet abstract ink stroke` / `looping ink mark with no letterforms` で書くこと（既存行はこの形になっている——崩さない）。
- **★署名は常に抽象。** "an abstract illegible ink stroke", "a looping wet ink mark with no letterforms" 等のみ。**人名として読める形を作らない。**
- **強制退去・手錠・泣き崩れる家族・路上の家財を描かない。** 家は常に aftermath（無人・施錠・静か）。
- **recorder's-stamp teal `#0F6E68` 基調。notice-orange `#D4692A` は掲示物モチーフのみ（≤8枚）。paid-in-full morning `#F0DFB4` は ACT1 の現金購入ビートと ENDING のみ**（§5.6 の per-act motif で指定）。
- **時代考証:** 1998–2026。2005–2007 のビートにスマホ/現代車/LED/現代UIを混ぜない。
- **★footage treatment は bleed/parallax（DESIGN §1）。depth 前提の絵作りをしない。**
- **dochighlight を作らない・書かない。** milky wash / scanline / 黄色ウォッシュを描かない。
- **gavel / 天秤 / Lady Justice は生成しない**（実写側で1本だけ使う・§1.2 R-NO-GAVEL-SPAM）。

## 5.5a ★反復禁止ルール（owner directive「似たシーンの機械的繰り返しをやめる」・BINDING・**誕生時から適用**）

1. **1ビート内は同一 motif のバリエーション最大2枚。** 3枚以上の同一被写体ブロックを作らない。§5.6 は最初からこの制約で組んである（EP55 のように後から61行を差し替える事態を起こさない）。
2. **幕をまたぐ motif の再登場は「目に見える状態変化」必須。同状態の撮り直しは禁止。**
   > ★★ **R3 MAJOR FIX 2026-07-29 — この連鎖表は v001 で 6本中 4本が間違っていた。** 実行を 1行ずつ読んで照合した結果、§5.7 の連鎖が正しく、ここの記述が誤りだった（S064 は「overflowing tray」でなく **台車**、overflowing tray は **S113**、S128 はトロリーでなく **署名する手**、S086 は家でなく **郡の窓口**、S174 は家でなく **道端の郵便受け**、S066 は壁時計でなく **卓上カレンダー**、S135 はストップウォッチでなく **2脚の椅子と署名済みの1枚**）。この節は BINDING で「この状態以外の行を作らない」と書いてあるため、直訳するオペレータは **正当な行（S002 / S180 / S113 / S115 / S136 / S182）を削除してしまう**。下の表が正典であり、**行は1つも削らない**。
   - **the lockbox（6状態）** = 夜のドアハンドルに掛かる・オレンジのタグ付き(S002・hook) -> 同じロックボック・日中・周りの家は明らかに人が住んでいる(S003) -> 同じ家が日沒後に真っ暗でロックボックだけが光る(S009) -> 施錠されたドアに手をついた後ろ姿の人物の指の横(S180) -> 切断されてマットに落ちている(S196) -> 消えて塗装に2つの痕だけが残る(S197)。
   - **the signature（4状態）** = one wet mark alone on a blank line(S007) -> 九つの同形の書類角に互いに一致しないストローク(S130) -> a wall of mismatched marks(S138) -> one mark under an exhibit sticker(S165)。
   - **the stack（5状態・フィルム順）** = a thin file in a hand(S045) -> 廊下に放置された台車一台(S064) -> 縁を越えて崩れかけた入レ(S113) -> a pallet on a loading dock(S141) -> one box carried out of a courthouse(S190)。⚠ **S064（台車）が S113（入レ）より前に来るので、量のエスカレーションが一度だけ逆行する。再生成ではなく CODEX_B の配置で吸収すること（両方とも良い絵で、どちらも別のビートに使える）。**
   - **the paid-in-full deed（5状態）** = signed at a closing table in warm light(S021) -> folded into a drawer at home(S026) -> pulled out again under a kitchen lamp(S073) -> laid flat on an exhibit table(S168) -> back in the drawer at the end(S203)。
   - **the empty house（4状態）** = lit and lived-in(S016) -> dark with the lockbox(S009) -> 窓越しに見える家具の痕だけの居間(S182) -> lights back on at dawn(S199)。
   - **the clock / the minute（5状態）** = a second hand crossing(S011) -> 日付を消し込んだ卓上カレンダー(S066) -> 夜の事務所の白い壁時計(S115) -> 手元の機械式カウンター(S136) -> a calendar page(S177)。
3. **Codex one-shot 原則:** 各行1枚・一発で決める。再生成は §6 の QC fail 時のみ（同一プロンプト・別シード1枚・§6.3）。**「複数枚から選ぶ」ためのバリエーション生成は禁止**（variants 0・§5.10 と同義）。
4. **★HP anti-samey 変化マトリクス（88枚全体に適用）:**
   - **軸を必ず散らす:** 距離（hands macro／medium／wide／far-wide）×角度（背後正対／後方斜め／low angle／over-the-shoulder）×年代 wardrobe（1990s／2000s／2010s／2020s）×光（cold office fluorescent／flat Florida daylight／night porch／paid-in-full morning）×setting（house／kitchen／records office／call floor／signing floor／courthouse／hearing room／loading dock／mailroom／street）×人数（solo／2–4人／列／群衆）×姿勢（座って待つ／立つ／歩く／署名する手元／箱を運ぶ／鍵を握る）。
   - **HARD: どの2枚の ★HP も「被写体タイプ＋構図＋光」の3要素同時一致を禁止**（例:「机で署名する手元×over-the-shoulder×office fluorescent」は全88枚中1枚だけ）。88行を書き終えたら軸の表で自己監査してから生成に入る。
   - **クラスタは §6.1 Q4 phash watch-list に反映済み**（**R3修正:** lockbox 6状態・signature 4状態・stack 5状態・deed 5状態・house 4状態・clock 5状態・hands-macro 群・queue/waiting 群・corridor 群・mailbox 群・suburban-exterior 群）。**同状態ペアが phash で衝突したら「削る」でなく §5.5a のルールで作り直す。**

---

## 5.6 ★motif ライブラリ（幕別・distinct 数確定・S番号レンジ・**全210行 literal**）

> 各 motif ブロックは `motif名 — 枚数 — S番号レンジ`。**S001–S210 の全210行を literal 化済み。Codex は各行の**創作部分をそのまま**転記する（変奏を新たに書かない・行を増減しない・S番号を並べ替えない）。**
> ★★ **行末の `[HSTYLE]` と `Avoid:` 直後の `[HNEG]` はトークンのまま書かず、必ず §5.11 の全文に展開する（R3 BLOCKER FIX — §5.2 参照）。**
> **★`[STYLE]`/`[NEG]`＝人物なし象徴。`★HP`＝§5.11 `[HSTYLE]`/`[HNEG]`（匿名・非識別の人物）。** ★HP 合計 = **88枚（41.9%・実測）**。S番号集合は §5.7 に列挙。
> **★全210行に共通する不変条件:** 判読可能な文字・数字ゼロ／**判読可能な署名ゼロ**（署名は常に `an abstract ink stroke ... no letterforms`）／実在ロゴ・州章・連邦印章ゼロ／実在人物 likeness ゼロ／手錠・強制退去・泣き崩れる人物ゼロ／識別可能な子供の顔ゼロ／gavel・天秤・Lady Justice ゼロ（実写側で1本のみ）。


### ACT 0 — HOOK + OPENING（15枚・S001–S015）
- **the_house_at_night — 2 — S001–S002**（S002 は also_thumb・**hook signature**・literal first shot）
```
- `S001.png`
A plain single-storey American house seen from the opposite kerb at night, every window black, one porch bulb burning over the front step, a dry lawn and an empty driveway, the ordinariness of it exact and total, no people, no readable text [STYLE] Avoid: [NEG]
- `S002.png`
A realtor lockbox hanging from the handle of a front door at night, photographed close and slightly low, the porch bulb throwing a hard rim along its steel shackle and a long shadow down the door, a small flat orange tag on it with no characters, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_lockbox_by_day — 1 — S003**（★lockbox 状態①: 空き家ではない家に掛かっている＝不調和）
```
- `S003.png`
The same lockbox on the same door handle in flat late-morning daylight, and now the house around it is plainly lived in — a mown lawn edge, a coiled hose, a doormat squared to the step, two chairs on the porch, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_bare_room — 2 — S004–S005**（中が空いている・★HP S005）
```
- `S004.png`
A living room stripped to bare carpet with four deep indentations where a sofa stood, one uncovered bulb burning in the ceiling fitting, a window with no curtain and the blue-black street beyond, no people, no readable text [STYLE] Avoid: [NEG]
- `S005.png`
An anonymized hand flat against the inside of a front door in a dark hallway, cropped at the wrist, the other hand holding a house key down at the thigh, a hard line of porch light under the door, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_owner_on_the_step — 1 — S006**（夜、自分の家の前に立つ）
```
- `S006.png`
An anonymized figure standing on a concrete front step at night with their back fully to camera, shoulders squared, one hand at the door frame, the porch bulb above turning them into a dark shape, quiet rather than desperate, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_first_mark — 1 — S007**（★signature 状態①: たった一つのインクの筆致）
```
- `S007.png`
Extreme macro of one wet abstract ink stroke sitting alone on a blank ruled line, its loop thick and glossy and still drying, no letterforms anywhere in it, the rest of the page a soft grey smear, one hard light from the left, no person [STYLE] Avoid: [NEG]
```
- **the_deed_that_was_true — 1 — S008**（権利証の角と浮き出し印）
```
- `S008.png`
The corner of a stiff folded document with a raised embossed seal, photographed in raking warm morning light so the blank ring of the seal casts its own shadow, the body of the page an unreadable smear, the truest object in the film, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_house_dark — 1 — S009**（★house 状態②: 同じ家が暗く空になる）
```
- `S009.png`
The same house wide in the blue minute after sunset with every window dark and the porch bulb out, the lockbox a small hard glint on the door, the hose gone, the lawn a week past cutting, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_edge_of_the_stack — 1 — S010**（紙の断面＝量の予告）
```
- `S010.png`
Extreme macro along the cut edge of a thick stack of identical sheets, hundreds of page edges compressed into a striped wall of fibre, a single hard light grazing across them, depth falling off into black, no readable text, no person [STYLE] Avoid: [NEG]
```
- **the_minute — 1 — S011**（★minute 状態①: 秒針）
```
- `S011.png`
Extreme macro of a second hand sweeping across a plain dial, the hand slightly motion-blurred at its tip, the dial's markings soft and indistinct, everything beyond the glass falling to black, no person, no readable text [STYLE] Avoid: [NEG]
```
- **opening_title_beds — 2 — S012–S013**（タイトル下地・別テクスチャ2枚）
```
- `S012.png`
Macro of the surface of heavy laid paper raked by one low light, its fibre and deckle texture filling the frame, a near-black falloff at the edges, pure atmosphere for a title, no objects, no people, no readable text [STYLE] Avoid: [NEG]
- `S013.png`
A slow bloom of deep teal ink dispersing in still water against black, its filaments spreading in soft branching threads, abstract and cold, a title bed of pure motion held still, no objects, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_drive — 1 — S014**（夜の移動）
```
- `S014.png`
A lone petrol station forecourt on a dark highway at three in the morning, its canopy lights blazing over empty pumps and wet concrete, moths circling, one unlit road running away past it into blackness, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_street_at_first_light — 1 — S015**（タイトル用ネガティブスペース）
```
- `S015.png`
A wide suburban street photographed at first light with a flat pale sky occupying the upper two thirds, low roofs and mailboxes reduced to a dark band along the bottom, vast negative space above for type, no people, no readable text [STYLE] Avoid: [NEG]
```


### ACT 1 — THE HOUSE THEY OWNED（34枚・S016–S049）
- **the_house_before — 2 — S016–S017**（★house 状態①: 灯りの入った家・★HP S017）
```
- `S016.png`
A plain single-storey house at dusk with warm light in three windows, a car in the driveway and a hose coiled by the tap, the lawn cut and the shrubs squared, the whole frame quietly, unspectacularly owned, no people, no readable text [STYLE] Avoid: [NEG]
- `S017.png`
Two anonymized figures standing side by side on a front porch seen from the garden path behind them, one hand resting on the porch rail, evening warmth on their backs, both cropped above the shoulders, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_move — 2 — S018–S019**（北の街を出る・箱を詰める）
```
- `S018.png`
A street of clapboard houses under bare trees on a grey northern winter morning, salt stains on the kerb, a rented box truck parked with its ramp down outside one of them, no people, no readable text [STYLE] Avoid: [NEG]
- `S019.png`
An anonymized pair of hands running packing tape across the seam of a cardboard box, cropped at the forearms, a stack of sealed boxes behind, cold window light in a half-emptied room, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_money — 3 — S020–S022**（★deed 状態①: 現金で払い切る・paid-in-full morning 初出）
```
- `S020.png`
Anonymized hands counting a thick band of banknotes onto a polished closing table in warm morning light, both figures cropped at the cuffs, the denominations and portraits blurred beyond reading, a leather folder open beside the money, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S021.png`
A stiff document lying open on a closing table in warm morning light with a raised blank embossed seal on its face and one abstract ink stroke already on its signature line, the body text an unreadable smear, a pen laid across the corner, no people, no readable text [STYLE] Avoid: [NEG]
- `S022.png`
Two anonymized hands meeting in a handshake above a closing table, cropped mid-forearm on both sides, papers and a set of keys on the wood beneath them, warm window light from the left, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_bank_counter — 2 — S023–S024**（銀行の窓口・★HP S024）
```
- `S023.png`
A bank teller counter of pale stone and brushed steel photographed from the customer's side in flat lobby light, a closed till drawer, a chained pen on a bead chain, a blank deposit rack, nobody behind the glass, no people, no readable text [STYLE] Avoid: [NEG]
- `S024.png`
An anonymized figure walking out through a heavy glass bank door into white daylight, seen from behind and slightly low, a document folder under one arm, the lobby dark behind them, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_recorder — 4 — S025–S028**（登記所で公文書になる・★HP S027）
```
- `S025.png`
A county records counter of scarred varnished oak in flat institutional light, a deep steel intake tray, a rubber date wheel and an ink pad, a bell push worn smooth, no people, no readable text [STYLE] Avoid: [NEG]
- `S026.png`
A wooden desk drawer at home standing open with a stiff folded document and its raised blank seal laid on top of a small stack of papers, a chequebook and a set of spare keys beside it, one shaft of afternoon light, no people, no readable text [STYLE] Avoid: [NEG]
- `S027.png`
An anonymized clerk's hands pressing a heavy mechanical stamp onto the corner of a page at a records counter, cropped at the forearms, the impression forming as a blurred teal ring with no characters in it, flat overhead light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S028.png`
An aisle of bound recorder's volumes shelved from floor to ceiling, spines uniform and unlettered, a rolling ladder parked against them, one long strip light overhead, the public memory of who owns what, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_land — 2 — S029–S030**（境界と区画・★HP S030）
```
- `S029.png`
A plat map unrolled flat on a table and held down at two corners by a stapler and a mug, its parcel lines drawn crisp but every label and dimension dissolved into an illegible smear, cold overhead light, no people, no readable text [STYLE] Avoid: [NEG]
- `S030.png`
An anonymized figure walking a property boundary through long grass at the side of a house, seen from far behind and small in frame, a surveyor's stake in the foreground, flat morning light, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_address — 2 — S031–S032**（番地という識別子・★HP S032）
```
- `S031.png`
A roadside mailbox on a wooden post photographed close in flat daylight, its house numbers deliberately soft and indistinct, a dry hedge behind and the kerb running out of frame, no people, no readable text [STYLE] Avoid: [NEG]
- `S032.png`
An anonymized pair of hands pressing soil around a plant in a bed beside a front step, cropped at the wrists, a trowel and a watering can within reach, warm late-afternoon light, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_life_in_it — 3 — S033–S035**（暮らしの手触り・★HP S035）
```
- `S033.png`
A screened porch at evening with two empty folding chairs and a small table between them, the mesh throwing a fine grey grid over the garden beyond, a fan still on the floor, no people, no readable text [STYLE] Avoid: [NEG]
- `S034.png`
A kitchen in early morning with a kettle on the hob, two mugs upturned on a cloth, and a slab of warm light lying across the worktop from an east window, entirely ordinary, no people, no readable text [STYLE] Avoid: [NEG]
- `S035.png`
Two anonymized figures at a kitchen counter seen from behind, one reaching to a high cupboard and the other at the sink, both cropped above the shoulders, morning light flattening across their backs, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_house_across_the_street — 3 — S036–S038**（取り違えの物理的な土台・★HP S037）
```
- `S036.png`
A near-identical house directly opposite seen from a driveway apron at dusk, the same roofline and the same porch posts, one window lit, the road between them empty, no people, no readable text [STYLE] Avoid: [NEG]
- `S037.png`
An anonymized neighbour standing on their own front step across the street, seen at a distance as a small dark shape against a lit doorway, hand raised in a half wave that is cropped by a hedge, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S038.png`
Two roadside mailboxes on adjacent posts photographed together in one frame, their numbers deliberately soft and unreadable, identical hedges and identical kerb behind each, sameness as a mechanism, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_first_envelope — 3 — S039–S041**（最初の通知・★HP S040）
```
- `S039.png`
A single window envelope lying alone on a doormat inside a front door, its address panel a blank smear, a hard slot of daylight from the letter flap falling across it, the hall dark beyond, no people, no readable text [STYLE] Avoid: [NEG]
- `S040.png`
An anonymized hand picking an envelope off a doormat in a dim hallway, cropped at the forearm, a thin bright line of daylight under the front door, the posture unhurried, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S041.png`
An opened letter lying flat on a kitchen table with its fold lines standing up, every line of its body dissolved into a uniform grey smear, the torn envelope beside it, one cold overhead lamp, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_reading — 3 — S042–S044**（読む・理解できない・受話器へ・★HP S042 S044）
```
- `S042.png`
An anonymized figure standing still in a hallway holding a single sheet at reading distance, seen from behind and slightly to one side, weight on one foot, the front door and its bright glass panel beyond them, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S043.png`
A corded telephone mounted on a kitchen wall with its coiled cord hanging slack, a small pad and a pencil on a shelf beneath it, flat afternoon light, the room empty, no people, no readable text [STYLE] Avoid: [NEG]
- `S044.png`
An anonymized hand lifting a receiver off a wall telephone, cropped at the wrist, the coiled cord swinging out of the bottom of frame, kitchen light flat and cool, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_file — 2 — S045–S046**（★stack 状態①: すべてを一つの薄い束に・★HP 両方）
```
- `S045.png`
An anonymized hand holding a thin manila file at chest height, cropped at the wrist, no more than a dozen sheets in it, the edge squared, cool hallway light behind, the whole of a life's paperwork still small enough to carry in one hand, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S046.png`
An anonymized pair of hands squaring a small stack of documents against a kitchen table, cropped at the forearms, a pen and a pair of reading glasses beside them, warm lamp light from the right, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_drive — 2 — S047–S048**（南へ向かう長い移動・★HP S048）
```
- `S047.png`
A night interstate seen through a windscreen from the driver's eye line, wet asphalt throwing back the headlights, reflector studs running away into black, no other traffic, no readable signage, no people [STYLE] Avoid: [NEG]
- `S048.png`
An anonymized figure standing at a motel window at night with the curtain held back a hand's width, seen from inside and behind, the car park lights beyond throwing a hard edge along their shoulder, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_arrival — 1 — S049**（★HP 夜明けに自分の家の前に立つ）
```
- `S049.png`
An anonymized figure standing at the end of a driveway at first light with their back to camera, a travel bag set down beside them, looking at a house whose windows are all dark, quiet and composed, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 2 — NOBODY WAS READING（34枚・S050–S083）
- **★HP the_first_letter — 2 — S050–S051**（誤りを知らせる・投函する）
```
- `S050.png`
An anonymized pair of hands sealing a plain envelope at a kitchen table, cropped at the wrists, a written page folded beside it with its lines reduced to grey strokes, a mug and a pen within reach, flat morning window light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S051.png`
A blue kerbside collection box photographed close in flat daylight, its pull handle worn bright, a bare pole and a strip of pavement behind, the ordinary machine for being heard, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_phone_tree — 3 — S052–S054**（電話に入る・分岐する）
```
- `S052.png`
An anonymized hand holding a corded kitchen telephone receiver to the shoulder while the other hand flattens a page on the counter, both cropped below the chin, the page an unreadable smear, afternoon light through a blind, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S053.png`
An anonymized finger pressing a numbered key on a landline handset in close macro, the keypad legends soft and indistinct, the coiled cord looping out of focus below, cold kitchen light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S054.png`
A corded telephone lying off its cradle on a kitchen counter with the coiled cord pulled taut off the frame edge, a pad of paper beside it covered in illegible strokes, nobody in the room, no readable text, no person [STYLE] Avoid: [NEG]
```
- **★HP the_hold — 2 — S055–S056**（保留の時間）
```
- `S055.png`
An anonymized figure seated sideways on a kitchen chair with a receiver against one ear, seen from behind and slightly above, one elbow on the table, the posture of a very long wait, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S056.png`
A kitchen wall clock and a telephone in the same frame, shot from across the room in flat afternoon light, the receiver off its hook and lying on the counter, the room otherwise motionless, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_call_floor — 3 — S057–S059**（受ける側の風景）
```
- `S057.png`
A wide view of a telephone call floor from the back, forty anonymized headset-wearing workers seen only as heads and shoulders above low partitions, all facing the same way under a bank of ceiling lights, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S058.png`
An anonymized worker's hands adjusting a headset boom while the other hand scrolls a mouse wheel, cropped at the collar, a monitor beyond showing only soft indistinct blocks, cubicle grey all around, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S059.png`
Two anonymized figures at adjacent cubicle desks seen in profile lost to shadow, both leaning back, both wearing headsets, a partition wall between them, cold overhead light, no readable faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_script_on_the_screen — 2 — S060–S061**（S061 は also_thumb）
```
- `S060.png`
An anonymized worker's face reduced to a silhouette edge against a monitor whose content is a soft unreadable block of pale colour, the head cropped below the eyes, one hand on a keyboard, the room dark beyond, no readable text [HSTYLE] Avoid: [HNEG]
- `S061.png`
An empty night office floor seen down the aisle between desks, and on the nearest desk a leaning tower of identical document folders lit by one surviving overhead panel, the rest of the floor in darkness, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_reply_that_answers_nothing — 2 — S062–S063**（返信・定型）
```
- `S062.png`
A wire letter rack screwed to the wall beside a front door holding three identical unopened window envelopes wedged in together, their address panels blank smears, cold hallway light from a side pane, no people, no readable text [STYLE] Avoid: [NEG]
- `S063.png`
A form reply pinned to a kitchen corkboard among receipts and appointment cards, its printed paragraphs a uniform grey smear, the drawing pin catching one hard highlight, warm lamp light from the side, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_cart — 2 — S064–S065**（★stack 状態②: 台車で運ばれる束）
```
- `S064.png`
A tall wheeled office cart loaded with banded document folders parked alone in a corridor under a run of ceiling lights, its shelves bowed slightly under the weight, the corridor receding to a closed door, no people, no readable text [STYLE] Avoid: [NEG]
- `S065.png`
An anonymized worker pushing that loaded cart away down the corridor, seen from directly behind and cropped above the shoulders, one wheel slightly canted, motion implied in the shoulders, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_calendar — 2 — S066–S067**（★minute 状態②: 日が消えていく）
```
- `S066.png`
A desk calendar on an office blotter with a run of days struck through in ballpoint, the numerals and the strokes both soft and illegible, a pen lying across the pad, cold morning light from a window, no people, no readable text [STYLE] Avoid: [NEG]
- `S067.png`
A kitchen noticeboard layered with pinned envelopes and slips, all of them blank smears, the cork visible only at the edges, one warm lamp from the side, the accumulation of unanswered months, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_fax_and_the_copier — 3 — S068–S070**（機械が紙を吐き続ける）
```
- `S068.png`
A desktop fax machine feeding a page out into its catch tray, the emerging sheet curling and entirely illegible, a small indicator glowing, the office around it dark, no people, no readable text [STYLE] Avoid: [NEG]
- `S069.png`
An anonymized hand lifting a copier lid and laying a page on the platen, cropped at the cuff, the scan bar's light already sweeping beneath the glass in a hard teal line, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S070.png`
A photocopier output tray with a stepped stack of finished pages fanning out of it, the topmost sheet still sliding, every printed surface a uniform smear, cold machine-room light, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_kitchen_table — 3 — S071–S073**（★deed 状態③: 家で紙を広げる）
```
- `S071.png`
An anonymized pair of forearms spread across a kitchen table covered edge to edge in loose paperwork, every page an unreadable smear, hands flat on two separate sheets, the figure cropped at the elbows, one lamp low and warm over the mess, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S072.png`
An anonymized figure seen from behind seated at a kitchen table late at night, head slightly bowed over spread papers, a mug at the elbow, the window behind them black, quiet endurance rather than despair, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S073.png`
A stiff folded deed with a raised blank seal pulled out and opened flat under a kitchen lamp, its body text an unreadable smear, the ordinary clutter of a kitchen table pushed back around it, the proof that was always there, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_second_letter — 2 — S074–S075**（もう一度書く）
```
- `S074.png`
An anonymized hand writing on a lined pad at a kitchen table, cropped at the wrist, the handwriting reduced to grey strokes with no letterforms, three earlier torn-off sheets crumpled at the edge of frame, warm lamp light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S075.png`
A stack of six sealed envelopes squared on a hall table beside a set of car keys, all address panels blank smears, cold morning light through a side window, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_wrong_address — 2 — S076–S077**（隣か向かいの家が本当の対象だった）
```
- `S076.png`
An anonymized figure standing at the end of a driveway looking across the street, seen from behind at a distance, two similar houses opposite with only their numbers distinguishing them, both numbers too far to read, flat overcast light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S077.png`
Two adjacent house-number plates photographed as a tight diptych in one frame, the digits deliberately soft and indistinct, identical siding and identical porch posts behind each, sameness as the mechanism, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_night_office — 2 — S078–S079**（誰も読んでいない時間）
```
- `S078.png`
An anonymized cleaner pushing a trolley along a dark office aisle at night, seen from far behind, the only light a wedge from a service door, rows of empty desks with paper still stacked on them, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S079.png`
An office floor after hours with every monitor dark and one desk lamp still burning over an open unread folder, chairs pushed in, a window wall showing a black car park, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_machine_does_not_stop — 3 — S080–S082**（人が伝えても止まらない）
```
- `S080.png`
A mail sorting machine running at speed, envelopes flicking through its guides into ranked pigeonholes, every address panel a blur, the operator's station empty, no people, no readable text [STYLE] Avoid: [NEG]
- `S081.png`
An anonymized worker's hands loading a fresh hopper of envelopes onto a sorting machine without breaking rhythm, cropped at the forearms, the machine already pulling them through, cold industrial light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S082.png`
A conveyor of stacked document bundles moving left to right through an otherwise empty processing hall, motion blur along the belt, high bay lamps receding, nothing human in frame, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_notice_on_the_door — 1 — S083**（掲示物・notice-orange の初出）
```
- `S083.png`
A printed notice taped square to the glass of a front door, its whole text dissolved into an unreadable smear and only its flat printed orange border reading clearly, the dark hallway visible past it, evening light, no people, no readable text [STYLE] Avoid: [NEG]
```

### ACT 3 — WHAT A SWORN STATEMENT IS（36枚・S084–S119）
- **the_courthouse_that_relied — 2 — S084–S085**（判決を出す側の建物・外観と入口・無人）
```
- `S084.png`
A modest American county courthouse of pale limestone photographed straight on in flat overcast noon light, shallow steps and four plain columns, no signage legible anywhere, a wide empty apron of pavement in front of it, the building that would rely on the paper, no people, no readable text [STYLE] Avoid: [NEG]
- `S085.png`
The double doors of a courthouse entrance seen from inside a dim vestibule at a low angle, daylight burning white through the glass, brass handles worn smooth by decades of hands, a bare bulletin frame beside them holding nothing, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_clerk_counter — 2 — S086–S087**（受付カウンターに積まれる申立て・受け取る手）
```
- `S086.png`
A long wooden filing counter in a county clerk's office under flat ceiling light, three unequal towers of banded document folders waiting on it for collection, a rubber-tipped date wheel and an ink pad pushed aside, every page an unreadable smear, no person, no readable text [STYLE] Avoid: [NEG]
- `S087.png`
An anonymized clerk's hands seen from the customer's side of a filing counter, sliding a thick banded bundle across the varnished wood without looking up, the clerk cropped at the collarbone so no face reads, fluorescent light flattening everything, pages an unreadable smear [HSTYLE] Avoid: [HNEG]
```
- **the_empty_courtroom — 2 — S088–S089**（誰も検証しない部屋・傍聴席と法壇）
```
- `S088.png`
An empty American courtroom photographed from the back row at bench height, rows of blond wooden pews receding toward a plain raised bench, houselights half up, dust hanging in one shaft from a high window, nobody present, no readable text [STYLE] Avoid: [NEG]
- `S089.png`
A raised judicial bench seen from directly in front and slightly below, its wooden face scuffed at shoe height, an empty high-backed chair behind it, a bare blotter and a dark microphone gooseneck, the seat of reliance standing vacant, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_witness_chair — 2 — S090–S091**（宣誓の席・挙げられた手）
```
- `S090.png`
A witness box of pale wood standing empty beside a bench, one small swing gate ajar, a paper cup left on the ledge, hard side light from a tall window carving the grain, the chair where a person is supposed to have knowledge, no people, no readable text [STYLE] Avoid: [NEG]
- `S091.png`
An anonymized adult's right hand raised palm-out in the act of taking an oath, framed tightly from the shoulder up but cropped below the eyes so no face reads, backlit against a bright courtroom window until the hand is almost a silhouette, still and formal, no readable text [HSTYLE] Avoid: [HNEG]
```
- **what_a_sworn_page_is — 2 — S092–S093**（宣誓供述書の物理・署名欄と余白）
```
- `S092.png`
A single sheet of legal-size paper lying alone on a dark desk under one hard lamp, its body text dissolved into an unreadable grey smear, only the ruled signature line and the blank notary block standing out sharp and empty, the anatomy of a sworn statement, no person [STYLE] Avoid: [NEG]
- `S093.png`
Extreme macro of a blank ruled signature line running across a sheet of paper, the fibre of the stock visible, a faint recorder's-stamp teal guide rule beneath it, nothing written yet, the whole frame waiting, no letters anywhere, no person [STYLE] Avoid: [NEG]
```
- **★HP the_words_of_the_oath — 2 — S094–S095**（宣誓の言葉が意味するもの＝読む行為）
```
- `S094.png`
An anonymized person's hands holding an open manila file at reading distance under a desk lamp, thumb marking a place partway down, the pages an unreadable smear, the figure cropped at the wrists and forearms only, the act of actually reading a file, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S095.png`
A pair of reading glasses folded and set down on a closed file on a dark desk, one lens catching a cold ceiling light, the chair pushed back and empty behind, nobody came back to the page, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_notary_apparatus — 3 — S096–S098**（公証の道具・印璽・押されない台帳）
```
- `S096.png`
A brass seal embosser standing closed on a bare desk in raking side light, its jaws shut on nothing, deep shadow behind, the machine that certifies presence, no paper in it, no person, no readable text [STYLE] Avoid: [NEG]
- `S097.png`
An anonymized notary's hands pressing an embosser onto the corner of a page, seen from directly above and cropped at the cuffs so no face or body reads, the page an unreadable smear, the impression forming as a raised blank ring, cold overhead light [HSTYLE] Avoid: [HNEG]
- `S098.png`
An open bound notary journal on a counter, its ruled columns entirely blank and its ribbon marker lying flat, a pen resting in the gutter, one shaft of window light across the empty page, the record of who was present, unwritten, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_file_nobody_opened — 2 — S099–S100**（読まれるべき束・封のまま）
```
- `S099.png`
A thick banded stack of files sitting on the floor beside a desk leg, the top band still factory-tight, a coffee ring on the topmost cover, nobody has cut it open, flat office light, no person, no readable text [STYLE] Avoid: [NEG]
- `S100.png`
An anonymized figure's back filling the left third of the frame as they walk away down an office aisle, an unopened bundle of files left behind on the desk in sharp focus at the right, shallow depth of field, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_court_relies — 2 — S101–S102**（法廷が紙を信じる瞬間）
```
- `S101.png`
An anonymized robed figure seen only from behind and above the shoulders, seated at a bench, one hand resting flat on a closed folder, backlit by a tall window so the head is a dark shape, the moment a page is taken as true, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S102.png`
A rubber stamp lying on its side beside a fresh impression on a file cover, the impression rendered as a blurred teal ring with no legible characters inside it, hard directional light, the instant paper becomes a fact, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_deposition_room — 3 — S103–S105**（S104 は also_thumb・証言が録られる部屋）
```
- `S103.png`
An anonymized pair of forearms and clasped hands resting on a long polished conference table, a water glass and a legal pad within reach, the person cropped entirely below the collar, cold window light from the left, waiting to be asked, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S104.png`
An empty upholstered chair at the head of a long deposition table, a neat squared bundle of documents placed in front of it and a carafe beside them, a wall of vertical blinds behind throwing hard bars of light, the seat where the question will be answered, no people, no readable text [STYLE] Avoid: [NEG]
- `S105.png`
A wall of vertical office blinds half open, seen from inside a bare conference room in late afternoon, a single chair turned away from the table in the foreground, a hotel-grade carpet pattern receding, nobody here yet, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_record_being_taken — 2 — S106–S107**（速記・回るテープ）
```
- `S106.png`
An anonymized court reporter's hands on the keys of a stenotype machine, framed from directly above, a narrow paper ribbon spooling out into a tray in illegible fold, the operator cropped at the elbows, cold tabletop light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S107.png`
A small reel-to-reel recorder turning on a side table, its two reels catching a low warm lamp, the counter window showing a blur of digits too soft to read, cables coiled beside it, the room's memory being made, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_question — 2 — S108–S109**（質問の重さ・微弱な照明）
```
- `S108.png`
A single microphone on a short desk stand at the centre of an otherwise empty tabletop, hard specular highlight along its grille, everything beyond it falling to black, the question about to be put, no person, no readable text [STYLE] Avoid: [NEG]
- `S109.png`
A legal pad on a table seen at a steep angle, a single pen laid diagonally across it, the handwriting on the page reduced to soft grey strokes with no letterforms, one page corner turned up, cold overhead light, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_admission — 3 — S110–S112**（答えの後の空気）
```
- `S110.png`
A tall glass of water on a conference table, half drunk, condensation running down and pooling on the varnish, the room around it thrown deep out of focus, a long pause made physical, no person, no readable text [STYLE] Avoid: [NEG]
- `S111.png`
An anonymized person seated at a deposition table seen from behind and to one side, shoulders squared, head slightly lowered, the whole figure rimmed by window light so no face can read, a stack of documents untouched in front of them, no readable text [HSTYLE] Avoid: [HNEG]
- `S112.png`
An empty chair pushed back from a conference table at an angle, the seat cushion still compressed, a pen left uncapped on the wood beside a squared bundle, the moment after an answer, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_volume — 2 — S113–S114**（月に何通か＝量の物象化）
```
- `S113.png`
A metal office in-tray on a desk filled far past its lip with identical sheets, the pile leaning and about to slide, more trays stacked behind it in soft focus, flat fluorescent light, every page an unreadable smear, no person [STYLE] Avoid: [NEG]
- `S114.png`
An anonymized pair of arms carrying a bankers box level with the chest along a corridor, the carrier cropped at the neck so no face reads, three more identical boxes stacked against the wall behind, motion slight and steady, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_minute — 2 — S115–S116**（1分に1通・時間の単位）
```
- `S115.png`
A plain white office wall clock photographed dead on in cold night-office light, its second hand caught mid-sweep and slightly motion-blurred, the numerals rendered as soft indistinct marks, nothing else in the frame, no person [STYLE] Avoid: [NEG]
- `S116.png`
A mechanical stopwatch lying face up on a dark desk, its crystal throwing a hard highlight, the dial markings dissolved into indistinct ticks, a single sheet of paper just visible at the frame edge, the unit of the work, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_room_goes_quiet — 2 — S117–S118**（証言が終わった部屋）
```
- `S117.png`
An anonymized figure standing at a window with their back fully to camera, blinds half drawn, one hand at their side holding a rolled bundle of paper, a bare conference room behind them, evening light going flat, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S118.png`
A conference room seen from the doorway after everyone has gone, chairs at eight different angles, a forgotten paper cup, the overhead lights already switched off and only corridor light spilling in, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_transcript_becomes_evidence — 1 — S119**（証言録が証拠になる）
```
- `S119.png`
A bound deposition transcript lying closed on a dark table, a numbered exhibit sticker on its cover rendered as a blank teal rectangle with no characters, one corner of the cover curling, hard low light from the left, no person, no readable text [STYLE] Avoid: [NEG]
```

### ACT 4 — THE SIGNATURE FACTORY（38枚・S120–S157・engine・最密）
- **the_building_that_made_them — 2 — S120–S121**（郊外オフィスパークの匿名性）
```
- `S120.png`
A two-storey suburban office building of tinted glass and beige panel, photographed from across an empty parking lot in flat midday glare, a bare sign frame by the entrance holding no lettering, clipped shrubs and painted bays, the most ordinary building in America, no people, no readable text [STYLE] Avoid: [NEG]
- `S121.png`
The service side of a low-rise office building at dusk, a roll shutter half down over a bay, a dumpster and two bollards, one security lamp already burning against the pale sky, nothing announcing what happens inside, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_signing_floor — 3 — S122–S124**（同じ机が並ぶ床・人は後ろ姿と手だけ）
```
- `S122.png`
An open-plan office floor of identical grey desks photographed over the shoulder of an anonymized worker in the near foreground, that figure cropped at the back of the head and out of focus, twenty more seated backs receding under ceiling fluorescents, everyone facing the same way, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S123.png`
Two anonymized seated workers photographed from directly behind at desk height, each bent over a squared stack of identical sheets, shoulders and elbows only, chair backs cutting the frame, flat overhead light with no shadows to hide in, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S124.png`
A far-wide overhead view of a signing floor, eight anonymized figures at eight identical desks reduced to small dark shapes on a grey carpet grid, each with a pale rectangle of paper in front of them, geometry rather than people, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_supply — 2 — S125–S126**（ペンと紙の在庫＝工業製品としての宣誓）
```
- `S125.png`
An anonymized hand reaching into an open carton of identical ballpoint pens on a supply shelf, the arm cropped at the sleeve, dozens of pens standing on end in the box, a second unopened carton behind, cold stockroom light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S126.png`
A shrink-wrapped pallet stack of paper reams in a storeroom, the plastic catching a hard overhead strip light, the ream wrappers printed with nothing legible, a hand truck parked against it, raw material for sworn statements, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_wrist — 3 — S127–S129**（署名する手・反復・速度）
```
- `S127.png`
Extreme macro of an anonymized hand signing, framed so only fingers, pen and the last third of a wet dark ink stroke are visible, the stroke an abstract loop with no letterforms, the paper beneath an unreadable smear, hard raking desk light, no face [HSTYLE] Avoid: [HNEG]
- `S128.png`
An anonymized wrist and forearm caught mid-motion above a page with slight motion blur on the pen tip, a second identical page already sliding in from the frame edge, the rhythm of repetition made visible, cold light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S129.png`
An anonymized hand lifting the top sheet off a squared stack while the other hand holds a pen poised, both cropped at the cuffs, the discarded sheet falling away out of focus, a metronome made of paper, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **one_page_many_hands — 2 — S130–S131**（★signature 状態②: 一致しない筆致が並ぶ）
```
- `S130.png`
A grid of nine identical document corners laid edge to edge on a dark surface, each carrying an abstract ink stroke on its signature line, and every one of the nine strokes a visibly different shape and pressure and slant, no letterforms anywhere, one cold overhead light, no person [STYLE] Avoid: [NEG]
- `S131.png`
Macro comparison of two signature lines side by side on adjacent pages, the left stroke thin and upright, the right stroke fat and raked over, the same claimed hand made impossible, paper fibre sharp, no letters, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_title_that_the_signature_claims — 2 — S132–S133**（役職欄・肩書きの付け替え）
```
- `S132.png`
An anonymized hand pressing a small rubber title stamp onto the block beneath a signature line, cropped at the wrist, the impression forming as a blurred teal bar with no characters inside it, a row of six other title stamps waiting in a tray beside, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S133.png`
A tray of a dozen small rubber stamps standing in ranks on a desk, each mounted on a plain wooden handle, their rubber faces worn and unreadable, an ink pad open beside them, one lamp low and hard from the right, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_notary_who_was_not_there — 2 — S134–S135**（立ち会いのない公証）
```
- `S134.png`
An anonymized hand stamping a notary block onto a page that already carries one abstract illegible ink stroke with no letterforms, the impression forming as a blurred teal ring with no characters inside it, the signer's chair empty and visible in the background out of focus, the hand cropped at the cuff, certification happening in an absence, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S135.png`
Two office chairs at one desk, one pushed in and one turned away, a single page between them carrying an abstract ink stroke and an empty stamped block, dust in the ceiling light, the presence that never happened, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_quota — 2 — S136–S137**（時間当たりの目標）
```
- `S136.png`
An anonymized hand resting on a mechanical desk counter with a thumb on the tally lever, the counter window showing indistinct soft digits, a squared stack of pages beside it, cropped at the wrist, cold flat office light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S137.png`
A wall-mounted whiteboard in an office bay wiped almost clean, faint ghosted marker strokes still visible but entirely illegible, a marker resting in the tray, a chair back at the frame edge, the target that was never written down, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_wall_of_marks — 2 — S138–S139**（★signature 状態③: 壁一面の筆致）
```
- `S138.png`
A wall covered corner to corner with pinned document corners, each showing one abstract ink stroke on a signature line, hundreds of strokes in hundreds of different shapes filling the entire frame, shot straight on in flat even light, no letterforms anywhere, no person [STYLE] Avoid: [NEG]
- `S139.png`
Oblique raking view along that same pinned wall, the pages receding into shallow focus, the ink strokes reduced to a texture of dark marks like a crowd seen from above, one work lamp at the far end, no letters, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_pallet — 3 — S140–S142**（★stack 状態④: 出荷単位になった宣誓）
```
- `S140.png`
An anonymized worker's back and gloved hands strapping a shrink-wrapped block of documents to a wooden pallet, cropped above the shoulders, the block waist high and perfectly square, a warehouse aisle receding behind, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S141.png`
A full pallet of banded document bundles standing alone on a concrete warehouse floor under one high bay lamp, the bundles stacked in even courses like brick, a forklift fork just entering the frame, the day's sworn statements as freight, no people, no readable text [STYLE] Avoid: [NEG]
- `S142.png`
Macro of the corner of a shrink-wrapped document block, the plastic taut and creased, hundreds of page edges compressed into a striped mass, a strapping band biting into the corner, no readable text, no person [STYLE] Avoid: [NEG]
```
- **★HP the_dock — 2 — S143–S144**（積み込みと出発）
```
- `S143.png`
Two anonymized figures in silhouette on a loading dock at night pushing a wheeled cage of document bundles toward an open trailer, seen from inside the dark trailer looking out at the lit apron, no faces, cold sodium spill kept far in the background, no readable text [HSTYLE] Avoid: [HNEG]
- `S144.png`
The rear doors of a box truck closing on a load of banded bundles, photographed from ground level at night on a wet dock apron, one overhead lamp, the last inch of light narrowing on the cargo, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_recorder_receives — 3 — S145–S147**（郡の登記所が受け取り、公文書になる）
```
- `S145.png`
A public records counter with a deep steel intake tray, three sacks of mail slumped against its base, a chained pen on a bead chain, the doorway light behind harsh and white, no people, no readable text [STYLE] Avoid: [NEG]
- `S146.png`
An anonymized clerk's hands feeding page after page into a mechanical recording stamp, cropped at the forearms, the pages an unreadable smear, a stack already done leaning to one side, flat institutional light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S147.png`
A wall of shallow steel map drawers in a records vault with one drawer pulled fully out, a large folded parcel plan lying inside it with every line and label indistinct, one caged bulb overhead, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_halt — 3 — S148–S150**（差押えが止まる・機械が停止する）
```
- `S148.png`
A document conveyor stopped mid-run, one sheet frozen half over the roller and slightly buckled, the belt still, the machine housing catching a hard cold light, everything that was moving has stopped, no people, no readable text [STYLE] Avoid: [NEG]
- `S149.png`
An anonymized figure standing at the end of a stilled signing floor with their back to camera, hands loose at their sides, twenty empty chairs pushed in around them, half the ceiling lights already off, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S150.png`
A tall wheeled cage of unprocessed document bundles parked against a wall with a plain yellow-taped barrier across it, the tape flat and unmarked, cold corridor light, nothing moving, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_states_line_up — 2 — S151–S152**（州が並ぶ・制度側の反応）
```
- `S151.png`
An anonymized figure ascending the wide granite steps of a state capitol seen from far behind and below, reduced to a small dark shape against the pale stone, columns and a dome cropped at the top of frame, flat morning light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S152.png`
An empty hearing-room dais of dark wood with fifteen identical high-backed chairs and fifteen identical microphones, name-plate holders standing blank, house lights up, nobody seated, no readable text, no person [STYLE] Avoid: [NEG]
```
- **★HP the_press — 3 — S153–S155**（発表される・報じられる）
```
- `S153.png`
The backs of a press pool packed shoulder to shoulder in a low-ceilinged room, cameras and boom poles raised, everyone facing away toward a lit lectern that is cropped out of frame, no faces, hard practical light from the front, no readable text [HSTYLE] Avoid: [HNEG]
- `S154.png`
An anonymized reporter's hands writing in a flip notebook at chest height in a crowded room, the shorthand reduced to grey strokes with no letterforms, other raised recorders soft in the background, cropped below the eyes, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S155.png`
A newspaper press running at speed, the web of paper a blurred river through the rollers, ink smell implied by the wet sheen, the printed surface entirely illegible at this shutter speed, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_mill_closes — 2 — S156–S157**（工場が閉じる）
```
- `S156.png`
An anonymized pair of arms carrying a single cardboard box of personal effects out through a glass office door into daylight, cropped at the neck, the office behind already dark, a plant leaf poking from the box, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S157.png`
An emptied office suite with carpet indentations where desks stood, cable stubs taped to the floor, one abandoned chair on its side, late light through uncovered windows, the factory gone, no people, no readable text [STYLE] Avoid: [NEG]
```

### ACT 5 — THE PRICE OF A MILLION HOMES（38枚・S158–S195・climax・清算の算数）
- **★HP the_settlement_table — 2 — S158–S159**（和解の席・署名する側が変わる）
```
- `S158.png`
Six anonymized pairs of hands resting on a long boardroom table at intervals, every figure cropped below the collar, closed folders squared in front of each place, a carafe centred, cold ceiling light with no shadows, the other side of the paperwork, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S159.png`
An anonymized hand signing a single page at the head of a boardroom table, the mark an abstract dark stroke with no letterforms, the arm cropped at the cuff, out-of-focus backs of standing figures ranged behind, a settlement rather than a verdict, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_headline_number — 2 — S160–S161**（発表された総額の抽象化）
```
- `S160.png`
A bank vault door standing open in a marble lobby, its polished wheel and boltwork catching hard light, the space beyond it entirely dark, scale without contents, no people, no readable text [STYLE] Avoid: [NEG]
- `S161.png`
A single strapped brick of banknotes photographed from directly above on a plain dark surface, denominations and portraits deliberately blurred into an unreadable smear, one hard specular edge, nothing else in frame, no person [STYLE] Avoid: [NEG]
```
- **★HP the_review_that_was_bought — 3 — S162–S164**（独立審査という名の外注）
```
- `S162.png`
Two anonymized consultants in shirtsleeves seen from behind at a glass partition, one pointing at a wall of pinned pages whose every sheet is an unreadable smear with no letterforms, while the other holds a clipboard, both cropped above the shoulders, an open-plan floor beyond, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S163.png`
An anonymized figure seated alone at a desk stacked with identical ring binders, seen from behind and slightly above, one binder open and unread in front of them, late-evening office light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S164.png`
A shelf run of forty identical ring binders in a consultant's office, spines uniform and unlabelled, a stepladder folded against the end, cold even light, the audit as furniture, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_exhibit — 2 — S165–S166**（★signature 状態④: 証拠になった筆致）
```
- `S165.png`
Macro of a single abstract ink stroke on a signature line with a numbered exhibit sticker placed beside it, the sticker rendered as a blank teal rectangle with no characters, the page beneath an unreadable smear, hard evidence-table light, no letters, no person [STYLE] Avoid: [NEG]
- `S166.png`
A grey evidence carton with its lid off standing on a long table, banded document bundles visible inside packed upright, a chain-of-custody label rendered as a blank strip, one work lamp, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_deed_returns — 2 — S167–S168**（★deed 状態④: 証拠台の上の権利証）
```
- `S167.png`
An anonymized pair of hands unfolding a stiff document with a raised seal, cropped at the wrists, the body text an unreadable smear and the seal an unlettered embossed ring, a plain table beneath, cold overhead light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S168.png`
A folded deed with a raised blank seal lying flat and alone at the centre of a long evidence table, a soft warm morning note falling across only the paper while the room stays cold, the document that was always true, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_cheque_is_printed — 3 — S169–S171**（救済が印刷される）
```
- `S169.png`
An anonymized operator's hands loading a tray of blank cheque stock into a high-speed printer, cropped at the forearms, the machine housing open, a stack of finished sheets already fanning into the catch tray, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S170.png`
An anonymized hand lifting one printed cheque from a catch tray to eye level, the arm cropped at the elbow and the figure out of frame, every printed field on the cheque dissolved into an unreadable smear, cold machine-room light, no face [HSTYLE] Avoid: [HNEG]
- `S171.png`
A cheque printer running at speed, sheets fanning out into a stepped stack, the printed surface entirely illegible, a green machine indicator throwing a small hard highlight, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_envelope — 2 — S172–S173**（封入され、送り出される）
```
- `S172.png`
An anonymized worker's hands feeding a hopper of window envelopes on an inserting machine, cropped at the cuffs, sealed envelopes streaming out onto a belt below in a continuous ribbon, flat industrial light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S173.png`
A canvas mail hamper filled to the brim with identical window envelopes, photographed from directly above in a bare sorting hall, the address windows all blank smears, one wheel of the hamper visible, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_mailbox — 2 — S174–S175**（受け取る側）
```
- `S174.png`
An anonymized hand reaching into a roadside mailbox and drawing out a single window envelope, cropped at the forearm, flat suburban afternoon light, the street soft behind, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S175.png`
A bank of apartment mailboxes in a dim lobby, one small door hanging open on an empty slot, brass numbers rendered as indistinct marks, a floor of scuffed tile, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_amount — 2 — S176–S177**（金額の実寸）
```
- `S176.png`
An anonymized pair of hands holding one small cheque flat on a kitchen table, cropped at the wrists, the printed amount an unreadable smear, a coffee mug and a set of keys beside it, plain morning light through a window, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S177.png`
A wall calendar hanging in a kitchen with a single day ringed in ballpoint, the numerals and the ring both soft and illegible, the pages of earlier months curling behind it, flat daylight, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_cheque_that_came_back — 2 — S178–S179**（不渡り）
```
- `S178.png`
An anonymized hand holding an envelope that has been returned, cropped at the wrist, a rubber-stamped block across its face rendered as a blurred orange bar with no characters, a kitchen counter edge beneath, cold window light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S179.png`
A returned window envelope propped upright against a windowpane with hard afternoon light shining straight through the paper, the fibre and the ghost of an inner sheet showing but nothing readable, a bare sill beneath, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_house_that_stayed_empty — 3 — S180–S182**（S181 は also_thumb）
```
- `S180.png`
An anonymized figure standing on a concrete front step with their back to camera, one hand flat against a locked front door, a lockbox hanging from the handle beside their fingers, flat overcast daylight, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S181.png`
A roadside mailbox with a single window envelope standing proud of the slot, photographed close in early morning light with a plain suburban house soft and dark behind it, dew on the post, the smallest possible object at the end of the largest possible machine, no people, no readable text [STYLE] Avoid: [NEG]
- `S182.png`
A bare living room seen through an uncurtained front window from outside, carpet indentations where furniture stood, one bulb burning in the ceiling fitting, reflections of the street doubling across the glass, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_street_that_emptied — 2 — S183–S184**（一軒ではなく一区画）
```
- `S183.png`
An anonymized figure walking a dog along a suburban pavement at dusk, seen far behind and small, four houses on the far side dark and lawns overgrown while two others are lit, the ordinary and the vacant side by side, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S184.png`
A cul-de-sac photographed from a low drone height at last light, three driveways empty and stained, one pool cover sagging with leaves, the geometry of a subdivision holding fewer people than it was built for, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_prosecution — 3 — S185–S187**（刑事の道が一本だけ通る）
```
- `S185.png`
An anonymized figure in a dark suit walking away down a wide federal-building corridor of pale stone, seen from far behind and low, tall doors receding on both sides, hard clerestory light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S186.png`
Two anonymized figures seated at a plain counsel table seen from directly behind, a squared stack of documents between them, an empty bench beyond in soft focus, shoulders and chair backs only, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S187.png`
A federal courthouse facade of pale stone photographed from across the street in flat afternoon light, tall bronze doors closed, a bare flagpole, wide steps with nobody on them, no readable text, no people [STYLE] Avoid: [NEG]
```
- **the_sentence — 2 — S188–S189**（実刑という一点）
```
- `S188.png`
An empty institutional corridor of painted block with one steel door standing closed at the far end, a single caged ceiling light, the floor waxed to a hard shine, sober and non-sensational, no people, no readable text [STYLE] Avoid: [NEG]
- `S189.png`
A plain visiting-room table with two moulded chairs facing each other under a high barred window, both chairs empty, flat daylight, restrained and unsensational, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_box_carried_out — 2 — S190–S191**（★stack 状態⑤: 法廷から運び出される一箱）
```
- `S190.png`
An anonymized pair of arms carrying a single banded evidence box down courthouse steps, cropped at the neck, the box level with the chest, wide stone steps and a bright overcast sky, one box standing for a million pages, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S191.png`
An anonymized figure loading a banded box into the boot of a plain sedan at the kerb outside a courthouse, seen from behind at street level, the boot lid framing them, flat daylight, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_company_that_paid_instead — 2 — S192–S193**（会社は金で終わる）
```
- `S192.png`
An anonymized executive's hands closing a leather folder on a boardroom table, cropped at the cuffs, an empty chair on either side, a wall of glass showing a blank sky behind, the matter concluded without a person, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S193.png`
A corporate lobby of polished stone photographed after hours, an unlit reception desk and a blank sign wall behind it, one security lamp, the revolving door still, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_ledger_of_what_was_lost — 2 — S194–S195**（残る算数）
```
- `S194.png`
An anonymized pair of hands working an adding machine on a kitchen table, cropped at the wrists, a narrow paper tape curling out of the top with its printed figures reduced to indistinct marks, a small stack of envelopes at the elbow, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S195.png`
A long paper tape from an adding machine coiled loose across a dark tabletop, its printed column entirely illegible, one lamp low and hard from the left, the arithmetic left over, no people, no readable text [STYLE] Avoid: [NEG]
```

### ACT 6 — ENDING（15枚・S196–S210・現在時制で終わる）
- **the_lockbox_cut_off — 2 — S196–S197**（★lockbox 状態③）
```
- `S196.png`
A realtor lockbox lying cut open on a doormat just inside a front door, its shackle severed and its little door swinging, a house key on the mat beside it, a hard slot of morning light across both, no people, no readable text [STYLE] Avoid: [NEG]
- `S197.png`
A front door handle photographed close with the lockbox gone and only two bright unweathered marks left on the paint where it hung, morning light raking across the surface, the absence as the point, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_key_and_the_door — 2 — S198–S199**（鍵が戻る・家に灯が入る）
```
- `S198.png`
An anonymized hand turning a key in a front-door deadbolt, cropped at the wrist, the brass cylinder catching a warm low morning sun, the door's paint chalky and sun-worn, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S199.png`
A plain single-storey house seen from the street at dawn with two windows newly lit from inside, a car back in the driveway, the lawn cut, the paid-in-full morning colour allowed to reach the whole frame for the first time, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_morning — 2 — S200–S201**（生活が戻る・抑制した温かさ）
```
- `S200.png`
Two anonymized figures seen from behind through a kitchen doorway, standing at a counter in warm early light, one filling a kettle, the other setting a mug down, both cropped above the shoulders, ordinary and unremarkable, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S201.png`
An anonymized pair of hands hanging a framed photograph back on a wall hook, cropped at the wrists, the image inside the frame entirely soft and unreadable, a faint rectangle of unfaded paint behind it, warm morning light, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_paper_that_kept_moving — 2 — S202–S203**（★deed 状態⑤: 引き出しに戻る）
```
- `S202.png`
A grey fireproof document box on a hallway closet shelf with its lid ajar, the corner of a stiff folded page and a blank embossed seal just visible inside, folded towels stacked beside it, one shaft of afternoon light, no people, no readable text [STYLE] Avoid: [NEG]
- `S203.png`
The same drawer sliding shut on the folded deed, caught with a trace of motion blur on the drawer front, the room beyond dark, the document put away where it always should have been enough, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_new_letter — 2 — S204–S205**（同じ紙がまた動き出す）
```
- `S204.png`
An anonymized hand sliding a thin paper knife under the flap of a window envelope at a kitchen counter, cropped at the wrist, the blade catching one hard morning highlight, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S205.png`
A window envelope propped unopened against a kitchen fruit bowl in flat morning light, its address panel a blank smear, a set of keys and a pen beside it, the next one already here, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_same_machine_today — 2 — S206–S207**（2020年代のフロア・紙は画面になった）
```
- `S206.png`
A modern open-plan office of light wood and dual flat monitors, four anonymized workers seen from behind at standing desks, the screens showing only soft indistinct blocks of colour, bright contemporary daylight, the same work in new furniture, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S207.png`
A rack of server hardware behind glass in a cool corridor, ranked indicator lights receding, cable runs combed flat, the filing cabinet of the present, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_counter_still_open — 2 — S208–S209**（登記所は今日も開いている）
```
- `S208.png`
A public records counter photographed at opening time with the shutter just raised, an empty queue rail and a fresh intake tray, morning light flooding the tiled floor, the machine ready for another day, no people, no readable text [STYLE] Avoid: [NEG]
- `S209.png`
A suburban street at dusk seen from a driveway apron, mailboxes receding into distance along the kerb, porch lights coming on one by one down the row, unresolved and ordinary, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_last_frame — 1 — S210**（最後の静止）
```
- `S210.png`
A single sheet of paper lying alone on a bare dark floor in a stripe of late light, its surface entirely blank and unmarked, deep shadow filling the rest of the frame, room above for closing type, no people, no readable text [STYLE] Avoid: [NEG]
```

## 5.7 幕別 motif 枚数の検算（★Codex は書き終えたら足して確認）

```
ACT0  : 2+1+2+1+1+1+1+1+1+2+1+1 = 15   (S001-S015)
ACT1  : 34                            (S016-S049)
ACT2  : 2+3+2+3+2+2+2+2+3+3+2+2+2+3+1 = 34   (S050-S083)
ACT3  : 2+2+2+2+2+2+3+2+2+3+2+2+3+2+2+2+1 = 36   (S084-S119)
ACT4  : 2+3+2+3+2+2+2+2+2+3+2+3+3+2+3+2 = 38   (S120-S157)
ACT5  : 2+2+3+2+2+3+2+2+2+2+3+2+3+2+2+2+2 = 38   (S158-S195)
ACT6  : 2+2+2+2+2+2+2+1 = 15           (S196-S210)
合計   : 15+34+34+36+38+38+15 = 210  OK
★human-present(★HP) body: 2(ACT0)+17(ACT1)+16(ACT2)+11(ACT3)+18(ACT4)+19(ACT5)+5(ACT6)
                        = 88 / 210 = 41.9%（残り122は object/symbolic）  OK >=85 / >=40%
   ※この内訳は完成した §5.6 本文を機械集計した実測値（[HSTYLE] 行を S番号レンジで数えた）。
★HP の S番号（88枚・この集合以外に [HSTYLE] を使わない）:
  ACT0 (2)  S005 S006
  ACT1 (17) S017 S019 S020 S022 S024 S027 S030 S032 S035 S037 S040 S042 S044 S045 S046 S048 S049
  ACT2 (16) S050 S052 S053 S055 S057 S058 S059 S060 S065 S069 S071 S072 S074 S076 S078 S081
  ACT3 (11) S087 S091 S094 S097 S100 S101 S103 S106 S111 S114 S117
  ACT4 (18) S122 S123 S124 S125 S127 S128 S129 S132 S134 S136 S140 S143 S146 S149 S151 S153 S154 S156
  ACT5 (19) S158 S159 S162 S163 S167 S169 S170 S172 S174 S176 S178 S180 S183 S185 S186 S190 S191 S192 S194
  ACT6 (5)  S198 S200 S201 S204 S206
★also_thumb 4枚（S002 / S061 / S104 / S181）は §4.3a と一字一致・転換しない。
★spine motif の状態連鎖（§5.5a）に使う S番号は固定:
  lockbox   S003 -> S002 -> S180 -> S196
  signature S007 -> S130 -> S138 -> S165
  stack     S045 -> S064 -> S113 -> S141 -> S190
  deed      S021 -> S026 -> S073 -> S168 -> S203
  house     S016 -> S009 -> S182 -> S199
  minute    S011 -> S066 -> S115 -> S136 -> S177
```
> **S001..S210 の連番が穴なく210行**そろっていることを `--only S001` の `shots=255`（210 body + 42 i2v種 + 3 thumb_face）で確認する。

## 5.8 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_robosigning_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.9 パーサ契約（`read_prompts()` はこの2行形式しか読まない）

```
- `S001.png`
<positive prompt> Avoid: <negative>
```
- **1行目:** `` - `S001.png` ``（バッククォート囲み・行末は `.png` の直後）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト
- `ai_prompts.v001.md` は **body 210行（S001..S210）＋ i2v 種 42行（M01_src..M42_src、§8.1a）＋ thumb_face 3行（T01_face..T03_face、§5.12）＝ 255 エントリ**を書く。すべて1枚生成。F系12行は §5.13 の手順で**後から追記**（追記後 267）。

## 5.10 生成コマンド（★variants 指定なし。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=255 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 59 --only S001
#   -> ログ "episode=... shots=255 ... -> N images" の shots が 255 であること

# 全255枚（body 210 + i2v種 42 + thumb_face 3・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-059-robosigning
```
> QC で落ちたシーンの再生成は `--only S###`（同じプロンプトで別シードを1枚）。**基準を下げない・水増ししない。**

## 5.11 ★人物画像（匿名・ドラマ化スタンドイン）— `[HSTYLE]` / `[HNEG]`

> **owner directive（EP48/49「空/寂しい」却下の恒久対策）: 匿名・非識別の人物を増やし、動かす。** 実在人物（住宅所有者夫妻・署名担当従業員・名前を使われた従業員・有罪判決を受けた経営者・判事・州司法長官・銀行幹部）の **likeness を作らない**。顔は非識別（背向き/影の横顔/逆光 silhouette/目から下クロップ/浅い被写界深度・**adults only**）。**手錠・強制退去・泣き崩れる家族・路上の家財を絶対に作らない。可読の署名を絶対に作らない。**
> **★この `[HSTYLE]`/`[HNEG]` は (a) §8.1a の18本の人物 i2v 種、(b) §5.6 の ★HP body still 88枚、の両方に使う。**

**共通スタイル `[HSTYLE]`（各 H プロンプト末尾に全文連結）:**
```
, cinematic photoreal still, documentary reenactment stand-in, a generic anonymized person who resembles no real individual, face kept non-identifiable — turned away, in profile lost to shadow, back-lit to a silhouette, cropped below the eyes, or thrown soft in shallow focus, a deep recorder's-stamp teal as the one recurring system colour on ink and paper surfaces, near-black institutional gravity, period-correct American 1998-2026, low-key deep-shadow lighting or flat office fluorescent, telephoto compression, shallow depth of field, restrained dignified framing, homeowners always composed and upright and never in distress poses, every document and every signature an abstract illegible smear with no letterforms, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no readable documents, no handcuffs, no eviction, a single warm paid-in-full morning note only on the cash-purchase beats and the ending
```
**共通ネガティブ `[HNEG]`（各 `Avoid:` の後に全文連結）:**
```
recognizable real person, likeness of a specific person, celebrity, mugshot, deepfake, identifiable face, front-facing portrait, text, words, letters, numbers, numerals, captions, watermark, logo, brand mark, bank logo, corporate name, government seal, state seal, federal seal, readable document, legible affidavit, legible deed, legible notice, legible cheque, legible signature, readable signature, a signature with recognisable letters, legible date, license plate, handcuffs, restrained person, police forcing a door, sheriff eviction, family being dragged out, belongings thrown on the street, weeping face, screaming face, cowering figure, blood, gore, injury, corpse, weapon, violence, identifiable child face, child, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, evidence-blue bandana, interrogation green-gray, signage red, phosphor green, shop-lamp amber, milky haze, yellow wash, scanline
```

**QC フラグ:** `has_human_body:true`（許可）・`has_identifiable_real_person:false`（必須）・`has_readable_text:false`（必須）・`has_legible_signature:false`（必須）。

## 5.12 ★サムネ用 emotive-face 静止画（3枚・CTR §4A・thumb_face）

> **owner directive（CTR_PLAYBOOK §4A・emotive face が lane の #1 CTR driver）:** サムネは **単一の AI 生成・非実在・illustrative/dramatized な顔**を peak emotion で。**実在人物の likeness を作らない**＝clearly illustrative（semi-painterly, cinematic-render）にして実写に読ませない＝likeness firewall。**傷・暴力・子供の顔を作らない。** これらは **本編カットに出ない thumbnail 専用**（role=thumb_face・public_path null・distinct/cuts に数えない・§3.1）。B が `RobosigningThumbnails.tsx` で face＋2–4語 hook text を合成。

**共通スタイル `[TSTYLE]`:**
```
, thumbnail key art, a single non-real dramatized generic human character rendered in a clearly illustrative semi-painterly cinematic style so it never reads as a real photograph of a real person, face occupying 50 to 65 percent of frame height with eyes on the upper third, bright key light on the face and a rim light separating it from a dark desaturated blurred American suburban background, skin warm, background cool deep teal, high contrast and vivid, one clean quadrant of negative space for text, 1280x720, ultra-detailed
```
**共通ネガティブ `[TNEG]`:**
```
photoreal photograph of a real person, likeness of any real homeowner or executive or judge or official, recognizable real celebrity, deepfake, a child, wounds, blood, gore, violence, handcuffs, weapon, text, words, letters, numbers, watermark, logo, legible signature, readable document, two faces, tiny face, neutral expression, dark muddy low-contrast mush, cartoon flatness, extra limbs, deformed, warped
```
```
- `T01_face.png`
A non-real dramatized generic man in his sixties in an illustrative cinematic style at peak emotion — flat, disbelieving, wide-eyed incomprehension aimed straight at the viewer, the look of someone told they owe money on a thing they already own outright, pushed to the right third over a dark blurred suburban house at night with one porch light, warm rim light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
- `T02_face.png`
A non-real dramatized generic office worker in their thirties in an illustrative cinematic style, seen at peak emotion of blank institutional indifference — eyes flat and slightly lowered as if reading nothing, mouth neutral, the face of a process rather than a person, pushed to the left third over a dark blurred rows-of-desks office background, hard cool rim light, clean negative space on the right [TSTYLE] Avoid: [TNEG]
- `T03_face.png`
A non-real dramatized generic woman in her sixties in an illustrative cinematic style, eyes closing in stunned exhausted relief with the first warm morning light on one cheek, the moment a front door opens again, pushed to the right third over a dark blurred porch background with a band of dawn, clean negative space on the left [TSTYLE] Avoid: [TNEG]
```
> ★これら3枚は `role:"thumb_face"`・`public_path:null`・`has_human_body:true`・`has_identifiable_real_person:false`。§6 の目視で「実在 likeness でない・illustrative・子供なし・可読文字なし」を確認。B のサムネ案は T01–T03 を前景に、§4.3a の also_thumb body（背景）＋ 2–4語 hook（例 `THEY PAID CASH` / `NOBODY READ IT`）で組む。

## 5.13 ★EMOTIVE FACES — VISIBLE faces（F-series 12枚・per owner 2026-07-25 standard）

匿名図だけでは「顔がほぼ無い」状態になる。オーナー方針＝**見える感情的な顔**を織り込む（顔は維持率・CTRを上げる）。F-series（見える顔）を既存の匿名図に**加えて**生成する（★distinct/cuts に数えない補助レーン・cuts への採用は B に委ねる）。

**2レーン、いずれも「実在の誰にも似せない・非実在の人物」:**
- **(a) generic-photoreal** — 特定の実在人物に紐づかない役（受付係・書記官・記者・郵便局員・審査コンサルタント・近隣住民）。
- **(b) dramatized-illustrative** — 中心的実在人物に隣接するビート（家を失った所有者・署名担当者・経営者 archetype）は**明らかにイラスト調・半絵画的**で写真に見えないスタイルに。実在人物として名指し/キャプションしない。

**HARD BANS（不変）:** 実在の住宅所有者・署名担当従業員・名前を使われた従業員・有罪判決を受けた経営者・判事・州司法長官の**肖像を作らない**；**識別可能な子供の顔は不可**；手錠・強制退去・暴力・流血なし；**可読の署名・可読テキストなし**。QCフラグ: `has_human_body:true`・`has_identifiable_real_person:false`・`has_legible_signature:false`・`has_readable_text:false`。

**★ FACE 標準（data-driven・owner choice A）:** 全F画像は**LIGHT + EXPRESSION で目立つ顔**（サイズで盛らない）— **medium-close-up ~30–45% of frame height, eyes on the upper third, front or slight three-quarter, one strong unmistakable emotion, dramatic key + rim light against a DARK moody restrained background**。60%超の顔面充填・背向き・影に沈む・hands-only は不可。

`[FSTYLE]` = `a clearly-visible emotive human face in a strong medium-close-up filling ~30-45 percent of the frame, eyes on the upper third, front or slight three-quarter view looking near camera, one strong unmistakable expression, dramatic key light plus rim light on the face against a dark moody background, restrained saturation, a generic anonymized non-real person resembling no real individual, cinematic documentary grade, deep recorder's-stamp teal with a single warm paid-in-full morning note only on the closing and ending beats, ultra-detailed skin and eyes, high contrast, 16:9, adults only, no text, no watermark, no logo, no readable document, no legible signature`
`[FNEG]` = `likeness of a real or named person, recognizable real person, celebrity, mugshot, deepfake, child, toddler, wounds, blood, injury, handcuffs, eviction, weapon, violence, readable text, legible signature, readable document, caption, logo, bank logo, government seal`

Files `F001.png … F012.png`. Act-mapped beats:
```
- `F001.png`
A clearly illustrative semi-painterly face of a generic man in his sixties at a closing table, quiet uncomplicated satisfaction in the eyes and jaw, warm morning key light and a cool rim, a dark blurred office interior behind, the face of someone who has just paid for something outright, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
- `F002.png`
Photoreal medium-close-up of a generic county records clerk in her fifties behind a counter, brisk procedural neutrality in the expression, eyes on a page just below frame, flat institutional key light and a dark shelved background, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F003.png`
A clearly illustrative semi-painterly face of a generic woman in her sixties reading a letter at a kitchen table, the exact moment confusion turns into alarm, warm lamp key from below and a cold window rim, dark kitchen behind, not a likeness of any real homeowner [FSTYLE] Avoid: [FNEG]
- `F004.png`
Photoreal medium-close-up of a generic call-centre worker in his twenties wearing a headset, expression pleasant and completely disengaged, monitor glow on one cheek, a dark blurred bank of cubicles behind, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F005.png`
Photoreal medium-close-up of a generic court clerk in his forties at a filing counter, tired patient neutrality, eyes down on an unseen stack, hard overhead key and a cool rim, dark wood bokeh behind, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F006.png`
A clearly illustrative semi-painterly face of a generic man in his thirties being questioned across a table, the flat unbothered stillness of someone answering truthfully about work they never thought about, cold window key, dark conference room behind, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
- `F007.png`
Photoreal medium-close-up of a generic notary in her fifties mid-task, mouth set, eyes fixed on a stamp just out of frame, desk-lamp key and a hard cool rim, dark office behind, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F008.png`
Photoreal medium-close-up of a generic document-floor worker in her twenties looking up from a desk with the blank fatigue of repetition, fluorescent key flattening the face, rows of dark desks bokeh behind, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F009.png`
A clearly illustrative semi-painterly face of a generic executive in her fifties in three-quarter shadow, composed and unreadable and entirely untroubled, hard cool key with no warmth anywhere, a dark boardroom behind, no glorification, not a likeness of any real executive [FSTYLE] Avoid: [FNEG]
- `F010.png`
Photoreal medium-close-up of a generic reporter in his forties in a crowded room, sceptical focus, eyes tracking something past the camera, hard practical key and a cool rim, blurred raised recorders behind, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F011.png`
A clearly illustrative semi-painterly face of a generic man in his seventies holding a small cheque just below frame, the eyebrows lifted in flat disbelieving arithmetic, warm kitchen key from the left, dark room behind, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
- `F012.png`
A clearly illustrative semi-painterly face of a generic woman in her sixties on her own front step at dawn, eyes closed, exhausted relief without triumph, warm low morning key and a cold rim from the street, dark porch behind, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
```
Generate all 12; QC each visually (visible emotive face · non-real · no likeness/child/wounds/text/legible signature) before manifest.

> **★shots カウントとの整合:** F001–F012 の12行は、**base 255 行（S001..S210 + M01_src..M42_src + T01_face..T03_face）の `shots=255` 検証が通った後に** `ai_prompts.v001.md` の末尾へ追記して生成する。**追記後の `shots=267`（255+12）が正**。§5.9/§5.10 の「255」は F-series 追記前の base セットの検算値。F-series は distinct/cuts に数えない。

---


# 6. A-2/A-3: 静止画のQC・目視（★depth map なし）

## 6.1 機械QC（body 210 + i2v種 42 + thumb_face 3 = 全255枚 ＋ F系12枚・`qc_robosigning_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 長辺 >= 3840（thumb_face と F系は 1280x720 で可） | 未達=reject | §6.3 で再生成 |
| Q2 | `mean_luma` が 0.06–0.62（暗すぎ/白飛び検出） | 範囲外=flag | 目視で判定 |
| Q3 | sha256 重複ゼロ（全レーン横断・EP39〜58 とも） | 重複=reject | 再生成 |
| Q4 | **phash クラスタ watch-list**（下記）で近接ペアを列挙 | 近接=目視必須 | §5.5a のルールで**作り直す**（削らない） |
| Q5 | **可読テキスト検出** — ★**R3 BLOCKER FIX 2026-07-29: OCR ではなくテキスト*領域*検出（EAST / CRAFT）を使う**。文字を読む必要がなく「文字らしい領域が立ったか」だけを見るので、小さい活字を見逃さず、紙の繊維で偽陽性を出しにくい。スコア >=0.5 のテキスト領域が1つでも立てば fail | 検出=reject | プロンプトの `unreadable smear` / `no letterforms` を強めて再生成 |
| Q6 | **★署名の可読性検査** — ★**R3 BLOCKER FIX 2026-07-29: 「OCR ＋ 目視」という v001 の規定を廃止する。Tesseract 系の OCR は筆記体を読めない**ので、本作が唯一恐れている失敗モード（読める筆記体の偽名が署名線に乗る）を**原理上捕まえられない**。代替: （a）署名帯に Q5 のテキスト領域検出をかける、（b）**署名モチーフを含む全行を 100% 目視**（サンプリング禁止・小さくても筆記体に見えたら fail）。どちらかで引っかかったら fail | 検出=reject | `abstract illegible ink stroke` へ書き換えて再生成 |
| Q7 | ロゴ/印章検出（目視） | 検出=reject | 再生成 |
| Q8 | ★HP レーンの人物が非識別か（背向き/影/逆光/目下クロップ/浅い被写界深度のいずれか） | 顔が識別可能=reject | 再生成 |
| Q9 | 識別可能な子供の顔ゼロ | 検出=reject | 再生成 |
| Q10 | 強制退去の扇情描写ゼロ（手錠・引き摺り・泣き顔・路上の家財） | 検出=reject | 再生成 |

**★Q4 phash watch-list（同一クラスタ内は必ず目視で見比べる）:**
`lockbox 3状態` / `signature 4状態` / `stack 5状態` / `paid-in-full deed 5状態` / `empty house 4状態` / `clock 4状態` / `hands-macro 群` / `queue・waiting 群` / `institutional corridor 群` / `mailbox 群` / `suburban exterior 群` / `desk-with-paper 群` / `records-counter 群`。

```bash
# 全255枚 + F系12枚のコンタクトシート（20枚/シート・約14シート）。全シートを開いて1枚ずつ見る
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-059-robosigning --media image
#   -> runs/qc/robosigning_footage_contact_NN.png
```

## 6.2 出力

`episodes/PD-2026-059-robosigning/05_visuals/still_qc.v001.json`:
各画像の `prompt_id` / `sha256` / `phash` / `mean_luma` / `long_edge` / `ocr_text_found`(bool) / `signature_legible`(bool) / `has_human_body` / `has_identifiable_real_person` / `accepted` / `reasons[]` / `eyeballed_content`（**A が実際に見たものを一文で**）。

## 6.3 accepted が (body210 / i2v42 / thumb3) に届かなかったとき

**同じプロンプトで別シードを1枚**だけ回す（`--only S###`）。**基準を下げない・水増ししない・別プロンプトに差し替えない**（差し替えると §5.5a の状態連鎖が壊れる）。3回失敗したらプロンプト本文の該当語（例: `unreadable smear` の強度、`no letterforms` の明示）だけを直して再度1枚。

## 6.4 ★depth map は生成しない（本作は depth treatment 不使用）

DESIGN §1 の footage treatment は **bleed / parallax / duotone / focus**。`depth` は EP48/49 の warp 事故で恒久禁止。したがって `gen_depth_maps.py` を回さない・`depth_path` をマニフェストに書かない。

---

# 7. A-4: 実写クリップ 235本の選定と全点目視QC（★Layer 1 — 本作の第一素材層）

## 7.1 在庫の実態（2026-07-29 実測・A は着手前に自分で `--stats` を回して確認する）

```
アーカイブ総数     : 112,692 items（ledger: H:\pd-media\assets\archive\_ledger\*.jsonl）
  kind:image 92,709 / kind:video 17,834 / kind:audio 2,149
  license: free_commercial 91,461 / pd 17,833 / cc0 2,580 / review_required 789
  source: pixabay 53,836 / pexels 34,911 / nypl 9,400 / nasa 6,411 / noaa 981
          nara 1,319 / loc 612 / smithsonian 412 / ia 347 / mixkit 178 / unsplash 91
factory 棚（サブセット）: 88,850 items（うち video 15,683 が本作のフィルタ後の母集団）
本作に効くテーマ  : documents_paper 3,933 / finance_money 4,268 / property_home 2,982 /
                    legal_court 3,104 / courtroom_justice 360 / urban_night 8,281 /
                    government_buildings 166 / money_banking 196 / americana_1930s_1970s 9,517
```

## 7.2 ★★★ 選定は必ず `search_archive.py` ＋ ラベル付きコンタクトシート経由 ★★★

```bash
# 検索（ANDキーワード・theme/source/license/kind でフィルタ）
./.venv/Scripts/python.exe scripts/search_archive.py signature pen --limit 30
./.venv/Scripts/python.exe scripts/search_archive.py --theme property_home --kind video --limit 40
./.venv/Scripts/python.exe scripts/search_archive.py --stats

# 台帳ベースの確定選抜（★必ずコンタクトシートを出す。--no-sheet は配管用途のみ）
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme documents_paper --kind video --limit 40
#   -> runs/qc/factory_selection/<stamp>__<label>/selection.v001.json + *_footage_contact_NN.png
#   -> シートが作れなければ exit 3（＝選定は無効）
```

> ## ★★★ 棚のフォルダ名を信用してはいけない（BLOCKING・実測値）★★★
> **`FACTORY_LABEL_AUDIT.v001`（2026-07-28）の実測: 棚の claim-bearing ラベルの 40.0% が、ファイル自身の復元されたプロバイダ・タイトルと矛盾する。**ラベルだけを見て盲目的に選ぶと、実測で **約47%** の確率で被写体を取り違える。実例（このスレッドが本日再現した）:
> - `AF-BG-0519__courtroom_interior.mp4` の実タイトルは **"woman reading documents"**（法廷ではない）
> - `AF-BG-2379__bank_building_columns.jpg` の実タイトルは **"supreme court of united states in washington dc"**（銀行ではない）
> - `AF-BG-2204__warehouse_interior_dark.jpg` の実タイトルは **"room empty abandoned window"**（倉庫ではない）
> - `AF-BG-6460__us_constitution_document.jpg` の実タイトルは **"filing cabinet invoices accounting"**（憲法ではない）
> - `AF-BG-6237__courthouse_steps.mp4` の実タイトルは **"historic university campus building exterior"**（裁判所ではない）
> - 既知の監査例: `evidence_bag` = 革の財布 / `prison_corridor` = ハンブルクのエルベ・トンネル / `server_room_red_alert` = 猫
> **したがって: (1) 生のフォルダ名で選ばない。(2) `search_archive.py` か `select_factory_assets.py --theme`（監査済み台帳を読む）を使う。(3) 修正後のラベルでも正解率は70%なので、**ラベル付きコンタクトシートの目視は省略不可**。(4) 補正済みブラウズ木 `D:\pd-media-browse\factory_browse\<theme>\` を使ってよいが、`_mislabeled\` 配下は「別テーマへ再ホームされた実体」なので、必ず実タイトルを見る。**

## 7.3 本作で実写に任せるビート（`covers_scene_id` は §4.4 に pre-assign 済み）

| ビート | 実写に任せる理由 | 代表 subtype |
|---|---|---|
| 郊外住宅の外観・玄関・郵便受け | 本物の質感が生成画像より強い。棚に `property_home` 2,982点 | `suburban_street_dawn_wide` `front_door_lockbox_cu` `for_sale_sign_being_removed` |
| 現金・札束・カウンター | `finance_money` 4,268点。実写の手と紙幣は生成より説得力が高い | `cash_bundle_counting_hands` `banknotes_fanned_blur` |
| 紙・書類・署名する手 | `documents_paper` 3,933点。**実タイトルに "person signing on the documents" / "man signing the paper" / "woman signing the contract" が実在**（本日確認: `AF-BG-1276` `AF-BG-1280` `AF-BG-1284`） | `hands_signing_repetition_macro` `printer_output_tray_stack` |
| 裁判所の外観・廊下・傍聴席 | `legal_court` 3,104 ＋ `courtroom_justice` 360（**loc の実物庁舎写真 199件**） | `courthouse_exterior_stone_day` `courthouse_corridor_marble` |
| 記録所・公文書の棚 | `loc` / `nara` に実物の記録保管の写真がある（例: `nara__122213787-122213788__unloading-of-treasury-records-at-archives-building.jpg`） | `county_records_office_counter` `deed_book_shelves_row` |
| 夜の街・道路・移動 | `urban_night` 8,281点 | `highway_night_florida_drive` `freight_highway_night` |

> **★loc / nara の licence 注意:** `nara` の `money_banking` 行は **`license: review_required` かつ `_quarantine\` 配下**（例: `nara__18519593-79435363__photograph-of-records-of-comptroller-of-the-currency-divisio.jpg`）。**`review_required` は §7.4 の許可リストに入っていないので採らない。** `loc` の `free_commercial` 行（例: `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg`）は採ってよい。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）

`pd` / `cc0` / `free_commercial` のみ。**`review_required` は選ばない**（789件・`_quarantine\` 配下）。各行の `license` を `stock_ledger.v001.json` に転記し、`origin` を `factory` / `archive` / `stock` で区別する。

## 7.5 ★★★ 実写を必ず使う（EP48/49 の burned lesson＝実写0本を潰す）★★★

**本作の実写は「余裕があれば入れる素材」ではなく、563カット中 235カット（41.7%）を担当する第一層。** 実写が235本そろわないまま生成画像で埋めるのは**設計違反**。足りない場合は §7.2 の検索語を変えて掘る（`--theme` を変える・`--kind image` も許容してBが Ken Burns ではなく parallax/bleed で動かす・connector 25本を別テーマから採る）。

## 7.6 ★★★ ファイル名とサブタイプは信用できない（§7.2 の再掲・運用手順）★★★

1. `search_archive.py` / `select_factory_assets.py` の出力にある **`real title:` 行だけを信じる**。
2. コンタクトシートを開き、**235本すべてを1本ずつ見る**。見た内容を `eyeballed_content` に一文で書く（「見た記録」がないものは採用不可）。
3. `subtype`（§4.4 の pre-assign）と実際の中身が食い違ったら、**subtype を書き換えるのではなく別クリップを探す**（subtype は台本ビートに紐づく契約値）。
4. **本作固有の目視除外:** 実在の銀行ロゴ・実在の社名看板・実在の州章/連邦印章・可読の書類/小切手・可読のナンバープレート・手錠/逮捕・泣き崩れる人物・gavel と天秤（1本の例外を除く）。

## 7.7 EP39〜EP58 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_robosigning_factory.py --verify-no-prior-overlap
#   -> EP39〜EP58 の全 stock_ledger / asset_manifest に対して sha256 交差 = 0
```
**色語の分離（§5.3 のリストと同じ）も実写側に適用**: 前作の accent 色が支配的なクリップ（EP56 の赤い看板・EP55 の緑灰の蛍光灯・EP52 の青いバンダナ等）は、同じ画に見えるので採らない。

## 7.8 出力

- `episodes/PD-2026-059-robosigning/05_stock/factory_selection.v001.json`（選定＋`real_title`＋`license`＋`origin`）
- `episodes/PD-2026-059-robosigning/05_visuals/factory_clip_qc.v001.json`（**235本の `eyeballed_content` 全部**）
- `episodes/PD-2026-059-robosigning/05_stock/stock_ledger.v001.json`（権利台帳）

---


# 8. A-5: i2v モーション化 42本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする42本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

**選定原則:** 「動くことで意味が増える絵」だけを i2v にする。静止で足りる絵は still に残す。本作で動きが意味を持つのは (a) **インクが紙に置かれる瞬間**、(b) **同じ動作の反復**、(c) **止まる／止まらない機械**、(d) **人が待つ・運ぶ・鍵を回す**。

## 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの42行を追加・各1枚・**poised-still の source**）

> **★18本は §5.11 の匿名人物ビート（`[HSTYLE]`/`[HNEG]`）**、残り24本は抽象/象徴（`[STYLE]`/`[NEG]`）。**新規行を足さない**（42行ちょうど）。

```
- `M01_src.png`
Extreme macro of a single wet abstract ink stroke sitting alone on a blank ruled line, the ink still glossy and beginning to spread into the paper fibre, no letterforms anywhere, one hard raking light, shallow focus falling off to black, no person [STYLE] Avoid: [NEG]
- `M02_src.png`
Extreme macro along the cut edge of a thick stack of identical sheets with fine paper dust suspended in a shaft of hard light above it, hundreds of compressed page edges filling the frame, deep black falloff behind, no readable text, no person [STYLE] Avoid: [NEG]
- `M03_src.png`
Extreme macro of a plain watch dial with the second hand poised a fraction before the top of its sweep, the dial markings soft and indistinct, the crystal throwing one hard highlight, everything beyond falling to black, no person, no readable text [STYLE] Avoid: [NEG]
- `M04_src.png`
An anonymized hand sliding a ring of house keys across a polished closing table toward another waiting hand, both cropped at the cuffs, warm morning light raking the wood, a leather folder open at the frame edge, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M05_src.png`
A stiff folded document with a raised blank embossed seal lying open on a table in warm morning light, one corner of the page just lifting where a hand has released it, the body text an unreadable smear, no person, no readable text [STYLE] Avoid: [NEG]
- `M06_src.png`
Two anonymized figures carrying cardboard boxes through a bright empty doorway into a sunlit bare room, seen from inside and behind so only backs and forearms read, dust in the light, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M07_src.png`
A wooden desk drawer open on a folded document with a raised blank seal, the drawer front caught at the instant it begins to travel shut, a dim room beyond, one shaft of afternoon light, no person, no readable text [STYLE] Avoid: [NEG]
- `M08_src.png`
An anonymized hand posting a slim folder into one numbered pigeonhole in a floor-to-ceiling wall of pigeonholes, cropped at the sleeve, flat institutional light, dozens of identical compartments receding, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M09_src.png`
A lawn sprinkler throwing a wide arc of water across grass in flat morning light, droplets caught mid-flight, a plain house wall soft behind, the ordinary maintenance of an owned thing, no people, no readable text [STYLE] Avoid: [NEG]
- `M10_src.png`
An anonymized hand holding a corded telephone receiver at a kitchen counter, the coiled cord swinging slightly below the frame, the hand cropped at the wrist, afternoon light through a slatted blind, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M11_src.png`
A photocopier platen seen from above with the scan bar's hard teal line partway through its sweep beneath the glass, a page pressed flat above it entirely illegible, the machine housing dark around, no person [STYLE] Avoid: [NEG]
- `M12_src.png`
A telephone call floor seen from the back, thirty anonymized headset-wearing workers as heads and shoulders above low partitions, one nearer figure turning slightly in their chair, all faces away from camera, no readable text [HSTYLE] Avoid: [HNEG]
- `M13_src.png`
A printer catch tray with a finished sheet mid-fall onto a stepped stack below, the printed surface a uniform smear, a small machine indicator glowing, cold machine-room light, no people, no readable text [STYLE] Avoid: [NEG]
- `M14_src.png`
An anonymized figure seen from behind at a kitchen table late at night turning a page in a spread of loose paperwork, head slightly bowed, one warm lamp above, the window behind them black, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M15_src.png`
A tall wheeled office cart loaded with banded folders caught mid-roll in a lit corridor, one caster slightly canted, the corridor receding to a closed door, no people, no readable text [STYLE] Avoid: [NEG]
- `M16_src.png`
A heavy courtroom door of dark wood swinging almost closed on a lit corridor, a narrowing wedge of light across the floor tiles, brass kickplate catching it, no people, no readable text [STYLE] Avoid: [NEG]
- `M17_src.png`
An anonymized hand laying a bound transcript down onto a bare table and releasing it, cropped at the cuff, the cover settling flat, hard window light from one side, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M18_src.png`
A narrow stenotype paper ribbon spooling out of a machine and folding into a tray, its printed characters entirely indistinct, the keys and the operator out of frame, hard tabletop light, no person, no readable text [STYLE] Avoid: [NEG]
- `M19_src.png`
An anonymized person's hands holding an open manila file at reading distance under a desk lamp, a thumb about to turn a page, cropped at the forearms, the pages an unreadable smear, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M20_src.png`
A tall glass of water on a conference table with a bead of condensation running down its side, the room beyond thrown deep out of focus, a long pause made physical, no people, no readable text [STYLE] Avoid: [NEG]
- `M21_src.png`
An anonymized hand tipping a carafe to pour water into a glass at a long conference table, cropped at the wrist, the stream catching cold window light, the far end of the table falling out of focus, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M22_src.png`
A plain white office wall clock in cold night-office light with the second hand a fraction from the top of its sweep, the numerals soft indistinct marks, the wall around it bare, no person, no readable text [STYLE] Avoid: [NEG]
- `M23_src.png`
Extreme macro of a ballpoint tip touching down on a blank ruled line and beginning to lay an abstract loop of ink, no letterforms, the paper fibre sharp beneath, one hard light, no face, no readable text [STYLE] Avoid: [NEG]
- `M24_src.png`
An anonymized wrist and forearm mid-motion above a page with the pen tip slightly blurred, a second identical page already sliding in from the frame edge, cropped at the cuff, cold flat office light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M25_src.png`
A grid of nine identical document corners on a dark surface, each carrying one abstract ink stroke, the nearest corner just being laid down by an unseen hand so the grid is completing itself, every stroke a different shape, no letterforms, no person [STYLE] Avoid: [NEG]
- `M26_src.png`
An anonymized hand turning the crank of a microfilm reader while the film advances across the illuminated screen as an unreadable blur, cropped at the forearm, the dim reading room dark behind, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M27_src.png`
A pallet of banded document bundles being shrink-wrapped, the plastic film drawing taut around the corner of the block, a high bay lamp above, a concrete warehouse floor, no people, no readable text [STYLE] Avoid: [NEG]
- `M28_src.png`
Anonymized gloved hands hauling a roller shutter down over a loading bay at night, cropped at the forearms, corrugated steel descending across a lit apron, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M29_src.png`
A document conveyor at the instant it stops, one sheet frozen half over the roller and buckling slightly, the belt going still, hard cold machine light, nothing human in frame, no readable text [STYLE] Avoid: [NEG]
- `M30_src.png`
An anonymized worker's hands unplugging a desk lamp and coiling its flex on an otherwise stripped desk, cropped at the cuffs, a bare cubicle partition behind, half the ceiling lights already off, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M31_src.png`
A guillotine cutter blade descending through a thick stack of freshly printed sheets, the blade edge catching one hard highlight and the cut face of the stack compressing, every printed surface illegible, no people, no readable text [STYLE] Avoid: [NEG]
- `M32_src.png`
An anonymized hand tipping a bundle of envelopes into the mouth of a canvas mail sack that a second anonymized hand holds open, both cropped at the cuffs, a bare sorting bench beneath, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M33_src.png`
A canvas mail hamper heaped with identical window envelopes in a bare sorting hall, the topmost envelopes shifting as the hamper is nudged, address panels all blank smears, no people, no readable text [STYLE] Avoid: [NEG]
- `M34_src.png`
An anonymized thumb working open the flap of a window envelope over a kitchen worktop, cropped at the wrist, the torn paper fibre lifting, flat morning light from a side window, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M35_src.png`
A returned window envelope lying face up on a doormat with a blurred flat orange stamped bar across it, a widening slot of daylight from an opening front door moving across it, no people, no readable text [STYLE] Avoid: [NEG]
- `M36_src.png`
An anonymized figure crouching to lift the corner of a doormat on a concrete front step, seen from behind, one knee down and one hand under the mat, nothing beneath it, flat overcast daylight, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M37_src.png`
A grey evidence carton with its lid being lowered onto banded document bundles packed upright inside, one work lamp above, a long bare table beneath, no people, no readable text [STYLE] Avoid: [NEG]
- `M38_src.png`
An anonymized figure pushing a loaded hand truck of stacked cartons across a polished stone floor, seen from behind at low height, the wheels just beginning to turn, tall windows throwing long bars of light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M39_src.png`
A pair of long bolt cutters lying open on a concrete front step beside a severed steel shackle, the cut ends bright where the metal parted, hard early light across the concrete, no people, no readable text [STYLE] Avoid: [NEG]
- `M40_src.png`
An anonymized hand pushing a front door inward from outside, fingers spread against the chalky paint, the dark hall widening beyond as warm morning light spills past, cropped at the wrist, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M41_src.png`
A pair of curtains parting on a bare front window from inside, warm dawn light spilling across an empty carpeted floor and up the wall, dust turning in the beam, no people, no readable text [STYLE] Avoid: [NEG]
- `M42_src.png`
A screen door swinging on its spring across an empty porch at dusk, the mesh catching the last light, two folding chairs still and a strip of unlit garden beyond, no people, no readable text [STYLE] Avoid: [NEG]
```

> **★H↔M 対応（§4.5 と一致・18本）:** H001=M04 · H002=M06 · H003=M08 · H004=M10 · H005=M12 · H006=M14 · H007=M17 · H008=M19 · H009=M21 · H010=M24 · H011=M26 · H012=M28 · H013=M30 · H014=M32 · H015=M34 · H016=M36 · H017=M38 · H018=M40。`ai_prompts.v001.md` では**新規行を足さず**、この18本が `[HSTYLE]`/`[HNEG]` で書かれていることを確認する（`shots=255` 維持）。§8.5 で目視確認（adults only・子供顔なし・実在 likeness なし・可読署名なし）。


## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_postoffice.py` を下敷きにパスと SHOTS だけ差し替え）

```
ComfyUI: http://127.0.0.1:8188
model  : Wan 2.2 A14B (i2v)
frames : 81 / fps 16 -> 約5.06秒
size   : 832x480（生成）-> RIFE 4x -> 48fps -> B 側で 1920x1080 へアップスケール
steps  : 30 / cfg 5.0 / sampler: uni_pc / scheduler: simple
seed   : 固定（`M<NN>` の連番から導出・再現性のため記録）
motion : "poised-still" — 種画像の構図を保ったまま、1つの要素だけが動く
```

> **★A1111（7860）と ComfyUI（8188）は VRAM 競合する。** i2v を回す前に A1111 を `unload-checkpoint` するか落とす。**42本は複数日。** 夜間・分割で回し、1本ごとに mp4 の実在とサイズを確認してから次へ。

## 8.3 実行手順（まず1本で通す・★42本は複数日）

```bash
# 1本だけ通す
./.venv/Scripts/python.exe scripts/comfy_wan_robosigning.py --only M01
# 全42本（冪等・既存の mp4 はスキップ）
./.venv/Scripts/python.exe scripts/comfy_wan_robosigning.py
```

## 8.4 RIFE で 48fps 化（`rife_robosigning.py`・`rife_postoffice.py` と同手順）

```bash
./.venv/Scripts/python.exe scripts/rife_robosigning.py
#   -> H:\pd-media\assets\ai_video\robosigning\M<NN>_rife.mp4（16fps -> 48fps・4x補間）
```

## 8.5 i2v の QC（★42本すべて目視）

- **連続フレーム差分**で「本当に動いているか」を数値で確認（静止＝紙芝居は不合格）。
- **顔・手の破綻**が出ていないか（Wan は手が壊れやすい。★HUMAN 18本は特に注意）。
- **§1.2 の全禁止**が守られているか: 実在 likeness ゼロ / 可読テキストゼロ / **可読署名ゼロ** / ロゴ・印章ゼロ / 強制退去の扇情描写ゼロ / 識別可能な子供顔ゼロ。
- **adults only。**
- 落ちたら **同じ種画像・別シードで1本だけ**再生成。基準を下げない。

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど30本）

§4.6 の 30本（particle 15 / light 10 / vfx 5）を棚から選ぶ。**単独カットにしない。** screen/add で薄く重ね、全体の screen-wash 不透明度は **≤0.07**。**milky haze / foggy wash / 黄色ウォッシュ / scanline / CRT テクスチャは作らない・選ばない**（オーナーの恒久指摘）。

```bash
./.venv/Scripts/python.exe scripts/search_archive.py --theme particle --kind video --limit 40
./.venv/Scripts/python.exe scripts/search_archive.py --theme light --kind video --limit 40
./.venv/Scripts/python.exe scripts/search_archive.py --theme vfx --kind video --limit 40
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_robosigning_assets.py`）

```
remotion/public/robosigning/img/S001.png .. S210.png          （210）
remotion/public/robosigning/factory/FC001_*.mp4 .. FC235_*.mp4（235）
remotion/public/robosigning/motion/M01_rife.mp4 .. M42_rife.mp4（42）
remotion/public/robosigning/overlay/OV01_*.mp4 .. OV30_*.mp4  （30）
remotion/public/robosigning/thumb/                             （B がサムネ合成に使う・thumb_face は public に置かない）
```

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

実写235本 ＋ overlay 30本の `source` / `real_title` / `license` / `license_decision` / `origin` / `sha256` / 取得元URL（あれば）。**AI生成物（still 210 / i2v 42 / thumb 3 / F系 12）は `ai_disclosure_required: true` で別欄。**

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_robosigning_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_robosigning_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_robosigning_asset_manifest.py --reuse-feasibility
```

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）

| 指標 | 下限/上限 | 本作の設計値 |
|---|---|---|
| distinct 素材数 | >= 400 | **487** |
| first-use share | >= 0.70 | **0.8650** |
| avg uses / source | <= 1.4 | **1.156** |
| still-share | <= 0.45 | **0.4334** |
| motion coverage | >= 0.45 | **0.5666** |
| 汎用象徴（gavel/天秤/Lady Justice）の合計 | <= 2 | **1**（`gavel_block_resting` のみ） |
| 同一 subtype の重複 | 0 | **0**（§4.4 の235 subtype は全て別物） |

---

# 12. 絶対にやらないこと

1. **ElevenLabs TTS を回さない**（音声はBの担当・課金）。
2. **課金画像APIを使わない**（ローカル SDXL / ComfyUI のみ）。
3. **YouTube へ何もアップロードしない・予約しない。**
4. **B の所有ファイル（`03_script/**`・`04_scenes/shotlist*`・`08_edit/**`・`09_package/**`・`remotion/src/**`）を触らない。**
5. **EP39〜EP58 の素材・エピソードディレクトリを書き換えない**（読み取りのみ）。
6. **`--variants` を使わない**（1シーン1枚・バリエーション0）。
7. **`_02` / `_03` のような選択用の複数枚を作らない。**
8. **実在人物の顔・肖像・likeness を作らない。**
9. **可読の署名・可読の偽公文書・実在ロゴ・実在の印章を作らない。**
10. **強制退去の扇情描写（手錠・引き摺り・泣き崩れる家族・路上の家財）を作らない。**
11. **dochighlight を作らない・言及しない。DATE_STAMP レイアウトを使わない。**
12. **`gen_depth_maps.py` を回さない・`depth_path` を書かない。**
13. **棚のフォルダ名だけで実写を選ばない**（40%が誤ラベル・§7.2）。**コンタクトシート目視なしで staging しない。**
14. **counts（210/42/235/30/3/12/4）を勝手に変えない。**

---

# 13. 完了報告に含めるもの

1. `build_robosigning_asset_manifest.py --verify` の**実出力**（exit code 含む）。
2. `--reuse-feasibility` の**実出力**（distinct / first-use / avg-uses）。
3. `qc_robosigning_stills.py --check-resolution` の**実出力**。
4. `check_visual_asset_qc.py --ep PD-2026-059-robosigning` の**実出力**。
5. `select_robosigning_factory.py --verify-no-prior-overlap` の**実出力**（重複 sha256 = 0）。
6. **コンタクトシートのファイル一覧**（画像14枚分＋実写12枚分）と、**全点目視した旨**。
7. **Q5/Q6（可読テキスト・可読署名）で reject した枚数と、再生成後の結果。**
8. **★HP 88枚の変化マトリクス自己監査結果**（3要素同時一致がゼロであること）。
9. 実写235本のうち **`search_archive.py` 経由で選んだ本数** と、**`real title` と `subtype` が食い違って差し替えた本数**。
10. 未達・妥協した点があれば**正直に列挙**（「全部できました」だけの報告は不可）。
