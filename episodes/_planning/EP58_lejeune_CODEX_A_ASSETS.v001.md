# EP58 lejeune — Codex スレッドA「素材生成」引き継ぎプロンプト v001（30分・5幕・payoff 末尾積み上げ）

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN_ARCHITECTURE）も実装スレッドB（CODEX_B）も**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> ★30分尺。素材点数は EP55 burge / EP56 postoffice と同スケール。**「だいたい」で決めず §3 の確定値と §3.3 の検算をそのまま使う。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP58 / Episode ID: PD-2026-058-lejeune / slug: lejeune
Composition id: Ep58Lejeune（B が Root.tsx に登録・A は staging まで）／1920x1080 / fps30 / 30:00

事件（日本語サマリ）:
  米海兵隊基地 Camp Lejeune（ノースカロライナ州ジャクソンビル）の飲料水汚染。
  1953-08 から 1987-12 まで、基地の二つの給水系統——Tarawa Terrace（家族住宅地区）と
  Hadnot Point（基地中枢）——の井戸水が工業溶剤で汚染されていた。Tarawa Terrace の主汚染物質は
  基地外のドライクリーニング店 ABC One-Hour Cleaners 由来の PCE（テトラクロロエチレン）、
  Hadnot Point の主汚染物質は基地の整備廠・廃棄場由来の TCE（トリクロロエチレン）で、
  ほかにベンゼン、塩化ビニル、trans-1,2-DCE が検出されている。いずれも当時の連邦基準
  （EPA の最大許容濃度）が定められる前後の時期に、基準をはるかに超える濃度で検出された。
  1980-1981 年、陸軍の試験機関と外部の民間ラボが「水が有機溶剤で高度に汚染されている」旨を
  分析票・報告書に書いて基地へ返している。にもかかわらず汚染井戸が実際に閉鎖されたのは
  1984 年末から 1985 年初頭にかけてであり、基地に住んでいた家族には長く知らされなかった。
  ★主人公は二人の「記録を掘る素人」。
   (1) Jerry Ensminger — 海兵隊の master sergeant（drill instructor）。9歳の娘 Janey を
       白血病で 1985 年に亡くし、10年以上あとにテレビのニュース報道で初めて基地の水と
       小児がんの関連を知る。以後、情報公開請求で基地自身の書類を集め続け、2007 年に
       連邦議会下院の公聴会で宣誓証言した。
   (2) Mike Partain — 基地の病院で生まれた「基地の子」。30代で男性乳がんと診断され、
       同じ基地に関係する男性乳がん患者を自力で集めて名簿にした。
  ★制度側の経過: 1997 年の公衆衛生評価は 2009 年に ATSDR 自身が撤回。2012 年に
   Janey Ensminger Act（退役軍人省の医療給付）、2022 年に PACT Act に含まれる
   Camp Lejeune Justice Act（提訴の道を開いた）。以後、行政請求と訴訟が大量に積み上がり、
   支払いは極めて少ない。裁判所は当事者双方に大量事件の解決計画の提出を命じており、
   その期限が 2026 年 10 月末——本作の「現在時制」の締切である。
   ★★★ 数値・日付・引用は本書に書かれた形でのみ扱う。プロンプト本文には数値を描かない。

センシティビティ（★本作で最も重い制約・§1 に完全版）:
  ★実在人物の顔・肖像・likeness を一切作らない（Jerry Ensminger / Janey Ensminger /
    Mike Partain / 議員 / 将校 / ATSDR 職員 / 弁護士 / 判事 — 全員）。匿名・非識別の一般人は可。
  ★★病気の子ども・死にゆく子どもを一切描かない。本作最大の禁止線。
    病室のベッドの子ども・点滴・脱毛・小児患者・葬儀の棺・墓前で泣く人物 — すべて不可。
    悲嘆は「物」「不在」「大人の姿」だけで運ぶ（空のベッド、片付いた子ども部屋、
    使われない三輪車、キッチンの空いた椅子、名前の書かれたバインダー）。
  ★医療行為・治療・診察・手術・注射・カルテの描写を作らない（成人でも不可）。
  ★可読の偽公文書を作らない（分析票・報告書・判決文・議事録・法案の可読文字は禁止）。
  ★軍の実在の部隊章・エンブレム・旗・階級章・実在ロゴを描かない。
  ★時代考証 1953–2026。1980年代のビートに現代車・スマホ・LED・現代の看板を混ぜない。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ・30分スケール）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**210本の固有プロンプト×1枚＝210枚**・バリエーション0） | `H:\pd-media\assets\ai\lejeune\S<NNN>.png` | 5–8時間（GPU） |
| A-1b | i2v 種画像の生成（**42本の固有プロンプト×1枚＝42枚**・バリエーション0） | `H:\pd-media\assets\ai\lejeune\M<NN>_src.png` | 1.5–2.5時間（GPU） |
| A-1c | サムネ用 emotive-face 静止画（**3枚**・CTR §4A・非実在の illustrative face・§5.12） | `H:\pd-media\assets\ai\lejeune\T<NN>_face.png` | 20分（GPU） |
| A-2 | 静止画のQCと目視（**全255枚を目視必須**＝210 body + 42 i2v種 + 3 thumb_face） | `05_visuals/still_qc.v001.json` + コンタクトシート | 2.5–4時間 |
| A-3 | ~~depth map~~ **不要（本作は depth treatment を使わない・§6.4）** | — | — |
| A-4 | factory 実写クリップ **235本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | 4–6時間（うち目視だけで2時間以上） |
| A-5 | i2v モーション化 **42本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\lejeune\M<NN>_rife.mp4` | 18–48時間（GPU・**複数日**） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **30本** | `05_stock/overlay_selection.v001.json` | 1時間 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 30分 |
| A-8 | Remotion public への staging | `remotion/public/lejeune/{img,factory,motion,overlay,thumb}/` | 40分 |

> **★★ 最重要の前提（EP42–56 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 210本＝210行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **variants 指定なし（＝1枚）** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 210 + i2v 種 42 + thumb_face 3 = 255枚（各1回）。** factory 235本は生成でなく在庫からの選抜。
> ★**`--only S001` のログで `shots=255` を確認**してから本番を回す（210 body + 42 i2v種 + 3 thumb_face = 255）。
> ★i2v 42本は**複数日GPU**。**開始前にマシン状態を確認**（heavy-job preflight）。夜間・分割で回す。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-058-lejeune/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を **A(producer)とB(consumer/validator)で一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 235 エントリ、`motion` 配列は 42 エントリ、`overlay` 配列は 30 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5／§4.6 に全列挙済み）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\lejeune\**` / `H:\pd-media\assets\ai_video\lejeune\**` | **A** | 読み書き |
| `episodes/PD-2026-058-lejeune/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-058-lejeune/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/lejeune/{img,factory,motion,overlay,thumb}/**` | **A** | 読み書き |
| `episodes/PD-2026-058-lejeune/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_lejeune_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-057-*/**` および EP39〜57 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を読む） | `PD-2026-058-lejeune`（variants 指定なし） / `58 --only S001` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-058-lejeune --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit N --exclude-used --ep PD-2026-058-lejeune --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-058-lejeune` |

> **★`gen_depth_maps.py` は使わない**（本作は depth treatment を使わない＝depth map 不要・§6.4）。

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（実在確認してから・直近の `*postoffice*`(EP56) を優先、無ければ `*burge*`(EP55)） |
|---|---|---|
| `scripts/qc_lejeune_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_postoffice_stills.py`（無ければ `qc_burge_stills.py`） |
| `scripts/select_lejeune_factory.py` | §7 の factory 235本の確定選定・EP39〜57 sha256 除外検証 | `scripts/select_postoffice_factory.py`（無ければ `select_burge_factory.py`） |
| `scripts/comfy_wan_lejeune.py` | §8 の i2v 42本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_postoffice.py`（実在確認） |
| `scripts/rife_lejeune.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_postoffice.py`（実在確認） |
| `scripts/build_lejeune_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_postoffice_asset_manifest.py` |
| `scripts/stage_lejeune_assets.py` | §10 の staging | `scripts/stage_postoffice_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.9 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_lejeune_facts.py`（B が clone して実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の制約に一致し、`check_lejeune_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_lejeune_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==235 / motion 配列長==42 / overlay 配列長==30 が非空で実体化していること

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_lejeune_asset_manifest.py --reuse-feasibility
#   → still >=210 / motion >=42 / factory >=235 / distinct 合計 >=487 / first-use >=0.70 / avg-uses/source <=1.4

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_lejeune_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全235本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-058-lejeune

# [A-DONE-5] EP39〜EP57 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_lejeune_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39〜EP57 のすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（正確性制約・ガードレール）★★★

**Jerry Ensminger と Mike Partain は【存命の公人】であり、二人とも自分の名前で数十年にわたりこの件を語り、連邦議会で証言している＝存在・立場・行動は事実として断定してよい。ただし【顔・肖像・likeness を作らない】。Janey Ensminger は【1985年に9歳で死亡した子ども】＝本作で最も重い扱いを要する。★★★病気の子ども・死にゆく子ども・子どもの遺体・葬儀・墓前の嘆きを一切描かない。悲嘆は物・不在・大人の姿だけで運ぶ。医療行為（点滴・注射・診察・手術・処置・カルテ）を一切描かない。因果関係の断定を絵にも文字にもしない＝汚染物質と特定個人の病気を「原因」で結ぶ表現を書かない（"associated with" の水準を絵でも越えない）。合衆国政府の法的責任は【いかなる裁判所も認定していない】＝「有罪」「責任を認めた」の含意を作らない。個人の officer/officialを悪役として名指ししない（悪役は制度）。実在の部隊章・エンブレム・旗・階級章・実在企業ロゴを描かない。可読の偽公文書を作らない。数値は画像に描かない（AE/figures で B が出す）。時代考証 1953–2026。**

## 1.1 R1/R2（生成ビジュアル全般）

1. **★R-FACE: 匿名・非識別の人物は可／実在人物の likeness は不可。** 匿名の一般人（実在の誰にも似せない・非識別のドラマ化スタンドイン）＝顔・身体を出してよい（§5.11 H シリーズ・`[HSTYLE]`/`[HNEG]`・§5.12 thumb_face・§5.13 F シリーズ）。ただし **実在人物の顔・likeness・肖像は作らない**＝Jerry Ensminger・Janey Ensminger・Mike Partain・その家族・実在の議員・将官・基地司令官・ATSDR/CDC の職員・実在の弁護士・実在の判事を**似せて描かない**。実在人物が示唆される所（父・娘・生存者・証人・司令官・医師・研究者）は非識別（背向き/影/逆光/目から下でクロップ/hands-only）を既定に保つ。
2. **★R-CHILD-HARM（本作の最重要禁止）: 病気の子ども・死にゆく子どもを一切描かない。** 「病院のベッドの子ども」「点滴/カテーテル/機械につながれた子ども」「脱毛した子ども」「痩せた子ども」「泣く子ども」「子どもの棺・遺体・墓・墓石の名前」「墓前で泣く大人」を**正プロンプトにもネガにも構図にも作らない**。子どもの存在は **不在の痕跡のみ**＝使われない三輪車、片付いたベッド、閉じたカーテン、玄関に残る小さな長靴、キッチンの空いた椅子。**遠景・非識別・後ろ姿の健康な子どもも本作では作らない**（誤読リスクが高すぎる）。
3. **★R-MEDICAL: 医療行為・医療機器・診療の描写を作らない。** 診察室・処置室・点滴スタンド・注射器・手術灯・カルテ・スキャン画像・病室のベッド（成人でも）を描かない。医療の気配が必要な場所は「無人の待合の椅子列」「消灯した廊下の遠景」「窓の外の朝」までに留める。
4. **可読の偽公文書を再現しない。** 分析票・ラボ報告・情報公開の開示紙・議事録・法案・訴状・和解通知・小切手の**可読文字を再現しない**（"blurred into an unreadable smear"）。日付・数値・署名・宛名を**画像に描かない**（AE/figures のタイポで出す＝B の担当）。
5. **★R-INSIGNIA: 実在の軍の部隊章・エンブレム・旗・階級章・基地名の看板・実在企業ロゴを描かない。** 制服が要る所は「無地の作業服/ユーティリティ」「肩から下でクロップ」「後ろ姿」で処理する。
6. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **R-CAUSATION:** "the water killed her / caused her leukemia / poisoned the child / the Marines murdered" を書かない。許容は "associated with" の水準まで＝"the water system", "the contaminated wells", "the family that lived there"。**個人の病気と汚染を因果で結ぶ語を書かない。**
2. **R-CHILD-HARM:** "sick child, dying child, child in a hospital bed, child with IV, bald child, child's coffin, child's grave, weeping at a grave, funeral of a child, hospice" を書かない（§1.1-2）。
3. **R-MEDICAL:** "IV drip, syringe, hospital bed, examination room, operating theatre, medical chart, X-ray, scan, chemotherapy, oncology ward, patient" を書かない（§1.1-3）。
4. **R-LIABILITY:** "the government was found liable / guilty / admitted fault / covered it up as a proven crime" を書かない。許容は "the record", "the report", "the wells were closed", "the claims", "the deadline"。
5. **R-NOBODY-NAMED:** 実在の officer・official・企業役員を悪役として名指ししない。"an anonymous duty officer / a base engineer / a laboratory technician" のみ。
6. **R-FACE:** 実在人物 likeness ゼロ（§1.1-1）。匿名一般人（"anonymous / generic / non-identifiable person, face turned or in shadow"）は許可。
7. **R-READABLE:** 可読の偽公文書禁止（§1.1-4）。"legible form / readable report / readable document / legible newspaper / readable name on a binder tab" を正プロンプトに書かない。
8. **R-INSIGNIA:** "unit patch, insignia, rank device, service emblem, base sign with readable name, corporate logo" を書かない（§1.1-5）。
9. **R-NUM:** 数値（年・件数・金額・濃度）を画像に可読で描かない。AE/figures（B）へ。
10. **R-DOCHL:** `dochighlight` という figure は**存在しない・作らない・言及しない**（BANNED・grep で 0 件）。
11. **R-DATESTAMP:** `DATE_STAMP` レイアウトは AE に**存在しない＝使用禁止**（BANNED・ビルドがクラッシュする）。日付カードは `CENTER_STACK` で作る。

## 1.3 機械ゲート（`build_lejeune_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
# 匿名・非識別の人物は許可。実在人物の likeness だけを弾く。
BANNED_PORTRAIT = re.compile(
    r"likeness of (a )?(real|specific|named) person|real[- ]person likeness|"
    r"face of (jerry |janey |mike )?(ensminger|partain)|"
    r"likeness of (ensminger|partain|a senator|a congressman|a general|a base commander)|"
    r"recognizable (real person|celebrity)|identifiable real person|"
    r"portrait of a real marine|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"the water (killed|murdered|poisoned) |caused (her|his|the) (leukemia|cancer)|"
    r"(sick|dying|ill|terminally ill) child|child (in a )?(hospital bed|hospital)|"
    r"bald child|child with (an )?iv|child'?s (coffin|casket|grave|funeral)|"
    r"weeping at a grave|graveside|headstone|hospice|"
    r"iv drip|syringe|hospital bed|examination room|operating theatre|medical chart|"
    r"x-ray|scan image|chemotherapy|oncology|patient in a bed|"
    r"government (found )?(liable|guilty)|admitted fault|proven cover-?up|"
    r"unit patch|military insignia|rank device|service emblem|readable base sign|"
    r"legible (form|document|report|newspaper|record|letter)|readable (form|document|report)|"
    r"dochighlight|DATE_STAMP",
    re.IGNORECASE)
```

> **許容:** "a kitchen tap running into a plain glass at night / a chain-link fence and a pine treeline at the base perimeter / a capped well head in long grass, unmanned / a carbon-copy analytical form on a clipboard, every mark an unreadable smear / a thick three-ring binder of tabbed pages closed on a kitchen table / an empty chair at a family table / a tricycle left on a concrete walkway, no child / rows of grey file boxes on steel shelving / a hearing-room table with a glass of water"。禁止は「病気の子ども/死にゆく子ども」「医療行為・医療機器」「因果の断定」「政府の責任認定の含意」「実在人物 likeness」「実在の部隊章/ロゴ」「可読の偽公文書」「数値の可読描画」「dochighlight」「DATE_STAMP」。

---

# 2. 台本の語数と尺の確定値（Aが素材点数を積算する根拠）

```
words_total          = 4,737（narration・確定。ゲート出力は review_log に貼付）
wpm_provisional      = 178.1（チャンネル中央値モデル）→ narration 1,595.9 s
wpm_expected_measured= ~175（EP55 実測 170.4 / EP56 実測 175.1。★178.1 をそのまま信じない）
★HOOK-AUDIO 標準（owner・EP52 から継続）: Brian の声が 0:00 から鳴る（silent runway なし）。
designed_gap_seconds = 185.1（PROVISIONAL。幕転換の息・AEカード下の music hold・
                       earned breaths ≤3・OST 着地。check_padding を通る設計ギャップ＝dead air でない）
endcard              = 9.0
total_seconds        = 1,790.0（1,595.9 + 185.1 + 9.0）= 29:50（band 1740–1860 内 ✓）
speech ratio         = 1790.0 / 1595.9 = 1.122（実測帯 1.04–1.30 内 ✓）
durationInFrames     = 53,700（PROVISIONAL・fps30 = 1790×30・VO onset 0.0）
mean_shot            = 3.164秒/カット（picture 1781.0 = total 1790.0 − endcard 9 / 563 cuts）
視覚 act              = 7区（0=HOOK+OPENING / 1..5=ACT I..V / 6=ENDING）
Act 語数配分（PROVISIONAL）:
  HOOK 150 / OP 57 / ACT1 800 / ACT2 745 / ACT3 905 / ACT4 915 / ACT5 900 / ENDING 265 = 4,737
```

> **★★ measured-VO re-lock（A も必ず理解しておくこと・DESIGN §5 が正典）:** ElevenLabs マスターを実測したら
> narration 秒数は必ず動く（EP55 +71.2s・EP56 +71.8s）。**そのとき台本を書き直さない・再TTSしない。
> ドリフトは designed_gap_seconds で吸収し、`durationInFrames` を再ロックする。** A の素材点数
> （still 210 / factory 235 / i2v 42 / cuts 563）は **秒数でなく点数の比**で決まっているので、
> re-lock しても **1点も変わらない**。変わるのは §3.3 の [2] mean_shot と [8] factory 下限だけ。

**Aにとっての意味は1つ:** > **総カット 563 / distinct 487 / 初出 86.50% = still 210 + factory 235 + motion 42。**（§3 で積算）

> **注意（命名差）:** **still は 210 本の固有プロンプトを持つ**ため、still の資産 ID は **S001..S210**（1プロンプト＝1枚）。`covers_scene_id` は still 資産 ID 空間（S001..S210）を指す（§7.3）。

---

# 3. ★素材構成の確定値（この値で調達する・勝手に変えない）

## 3.1 内訳（★勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **210枚** | 244カット | 1.162回(≤2) | **210本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **235本** | 235カット | **各1回(1)** | 在庫11,000本超＋stock から選抜（§7）・全点目視・EP39〜57 と sha256 被りゼロ |
| **i2v モーション** | **42本** | 84カット | 各2回(≤2) | 42本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **487点** | **563カット** | | |
| 合成レイヤー（particle/light/vfx） | 30本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |
| サムネ emotive-face（thumb_face） | 3枚 | — | 本編カットに出ない | **distinct/cuts に数えない**（§5.12・thumbnail 専用） |

**SDXL の生成バッチ（本編カットに出ない i2v 種・thumb_face を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **210枚** | 210プロンプト × 1枚 |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **42枚** | 42種プロンプト × 1枚 |
| サムネ face（`role:"thumb_face"`・§5.12） | **3枚** | 3プロンプト × 1枚 |
| **SDXL 生成バッチ合計** | **210 + 42 + 3 = 255枚（各1回）** | **variants 指定なし（＝1枚）** |

> **本編サムネの背景 anchor は body 210枚から4枚を `also_thumb:true` で流用選抜**（§4.3a）。**emotive-face（前景の顔）は §5.12 の thumb_face 3枚**。**role=thumb / still_thumb を作らない。**

## 3.2 幕別配分（★still は確定・factory/i2v は目安。合計だけが確定）

| 区間(act) | still（S番号・確定） | factory（目安） | i2v（確定合計42） | thumb anchor |
|---|---|---|---|---|
| HOOK+OPENING (0) | **15**（S001–S015） | 12 | 3（M01–M03） | S001 |
| ACT1「The Base」(1) | **36**（S016–S051） | 40 | 7（M04–M10） | — |
| ACT2「August 1997」(2) | **34**（S052–S085） | 34 | 6（M11–M16） | S058 |
| ACT3「What the Lab Wrote」(3)（engine・最密） | **40**（S086–S125） | 42 | 8（M17–M24） | S104 |
| ACT4「The Man Born on the Base」(4)（最密②） | **40**（S126–S165） | 42 | 8（M25–M32） | — |
| ACT5「The Two-Year Window」(5) | **30**（S166–S195） | 30 | 6（M33–M38） | S186 |
| ENDING (6) | **15**（S196–S210） | 14 | 4（M39–M42） | — |
| 繋ぎ（covers_scene_id:null） | — | 21 | — | — |
| **合計** | **210** | **235** | **42** | **4** |

> **still の per-act 数（15/36/34/40/40/30/15＝210）は確定**（§5 の motif ライブラリがこの配分で組まれている）。**幕別の factory/i2v 内訳は目安値**（合計 235 / 42 のみ確定）。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 563 = still 244 + factory 235 + i2v 84
[2] 平均ショット長 = picture 1781.0（total 1790.0 − endcard 9）/ 563 = 3.164秒/カット  ✓ (≤7.0)
[3] 静止画占有率(check_animation_mix) = 244/563 = 43.34%  ✓ ≤45%（余裕 1.66%pt）
[4] motion coverage = (235+84)/563 = 319/563 = 56.66%     ✓ ≥45%
[5] per-asset 上限: still 244/210=1.162(≤2) / factory 235/235=1.0(≤1) / motion 84/42=2.0(≤2)  ✓
[6] first-use share = 487/563 = 0.8650                    ✓ ≥0.70
[7] avg uses/source = 563/487 = 1.156                     ✓ ≤1.4（EP49 は 1.8 で flag された）
[8] factory 下限 = picture 1781.0/30 = 59.4 → ≥60本。設計値 235本 ✓（still-share≤0.45 を守る）
```

> **[3] の余裕は 1.66%pt。** still が210本を割ったら §6.3 の再生成で回復させ、**still-cut 244 を増やさない**（B側の shotlist が244で固定）。
> **★measured-VO re-lock 後の再検算:** [2] と [8] だけ picture 秒数を差し替えて再計算する。[1][3][4][5][6][7] は点数の比なので不変。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

## 4.1 スキーマ（`lejeune_assets.v1`）

```jsonc
{
  "schema": "lejeune_assets.v1",
  "episode_id": "PD-2026-058-lejeune",
  "slug": "lejeune",
  "generated_at": "<ISO8601>",
  "counts": { "still_body": 210, "still_i2v_source": 42, "motion": 42,
              "factory": 235, "overlay": 30, "thumb_face": 3 },
  "stills":  [ /* 210 body + 42 i2v_source + 3 thumb_face = 255 entries */ ],
  "motion":  [ /* 42 entries — 空配列禁止 */ ],
  "factory": [ /* 235 entries — 空配列禁止 */ ],
  "overlay": [ /* 30 entries — 空配列禁止 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例・★depth_path なし）

```jsonc
{
  "asset_id": "LEJ-S001",
  "role": "body",                       // body | i2v_source | thumb_face | reject
  "act": 0,
  "storyboard": "hook",
  "path": "H:/pd-media/assets/ai/lejeune/S001.png",
  "public_path": "lejeune/img/S001.png",
  "sha256": "<64hex>",
  "phash": "<16hex>",
  "width": 3840, "height": 2160, "long_edge": 3840,
  "mean_luma": 42.7,
  "also_thumb": true,
  "has_human_body": true,
  "has_identifiable_real_person": false,
  "has_readable_text": false,
  "has_child_depiction": false,
  "has_medical_imagery": false,
  "has_military_insignia": false,
  "ai_disclosure_required": true,
  "tags": ["kitchen_tap_glass_night", "hook_signature"],
  "eyeballed_content": "a kitchen tap filling a plain glass at night, one overhead fixture, an anonymized adult figure turned away at the counter",
  "qc": { "eyeballed": true, "verdict": "accept" }
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `counts` が §3.1 の確定値と一致（still_body 210 / still_i2v_source 42 / motion 42 / factory 235 / overlay 30 / thumb_face 3）。
2. `stills[]` の長さ = 255。`role` の分布が 210 / 42 / 3。
3. `motion[]` 42・`factory[]` 235・`overlay[]` 30 が**すべて非空**で `public_path` を持つ。
4. `asset_id` は `^LEJ-S\d{3}$`（body）/ `^LEJ-MS\d{2}$`（i2v_source）/ `^LEJ-T\d{2}$`（thumb_face）/ `^LEJ-M\d{2}$`（motion）/ `^LEJ-F\d{3}$`（factory）/ `^LEJ-O\d{2}$`（overlay）。
5. 全 `path` が実在し、`sha256` が重複しない。
6. body の `long_edge >= 3840`。
7. `also_thumb:true` は**ちょうど4件**（§4.3a）。
8. `role:"i2v_source"` は `public_path:null`・body に流用されない。
9. 全エントリで `has_identifiable_real_person:false` / `has_readable_text:false` / `has_child_depiction:false` / `has_medical_imagery:false` / `has_military_insignia:false`。
10. `qc.eyeballed:true` が 255/255・235/235。
11. **`depth_path` フィールドがどのエントリにも存在しない**（§6.4）。
12. 全文字列値が §1.3 の2本の正規表現に**1件もヒットしない**。

## 4.3 `role` の割り当て（機械的に決める）

- `S001..S210` → `body`（`public_path` あり）
- `M01_src..M42_src` → `i2v_source`（`public_path: null`）
- `T01_face..T03_face` → `thumb_face`（`public_path: null`）
- QC で落ちたものは `reject`（残す・数に入れない）

### 4.3a ★also_thumb 集合（ちょうど4枚・CODEX_B と一字一致必須）

```
{ LEJ-S001 (the kitchen tap filling a glass at night, an adult turned away at the counter — the hook signature),
  LEJ-S058 (a television's cold light thrown across a dark kitchen wall, screen unreadable — the broadcast),
  LEJ-S104 (a carbon-copy analytical form on a clipboard under one desk lamp, every mark an unreadable smear — the record),
  LEJ-S186 (a thick tabbed binder standing on a hearing-room table beside a glass of water — the archive) }
```

> ★この4集合は §5 の該当 S番号に必ず該当 motif を置くこと。**前景の emotive face は §5.12 の thumb_face（T01–T03）＝これらは背景 anchor。**

## 4.4 ★`factory[]` 全235エントリ（★必ず実体化・public_path 非空）

> **★LAYER 1（実写アーカイブ）/ LAYER 4 の中核。** `select_lejeune_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id）/`path`/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`origin`(`factory`|`archive`|`stock`)/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。** 各 public_path は `lejeune/factory/F0NN_<subtype>.mp4`。`type:"backgrounds"`, `kind:"video"`。**subtype の `_02` は「同一検索テーマの別クリップ」の意で、別 sha256・別素材（同一ファイルの重複ではない）。**

```jsonc
// HOOK+OPENING (act 0) — 12
{ "public_path":"lejeune/factory/F001_kitchen_tap_running_close.mp4", "act":0, "covers_scene_id":"S001", "subtype":"kitchen_tap_running_close" }
{ "public_path":"lejeune/factory/F002_glass_filling_backlit.mp4", "act":0, "covers_scene_id":"S002", "subtype":"glass_filling_backlit" }
{ "public_path":"lejeune/factory/F003_dark_kitchen_window_night.mp4", "act":0, "covers_scene_id":"S003", "subtype":"dark_kitchen_window_night" }
{ "public_path":"lejeune/factory/F004_television_glow_on_wall.mp4", "act":0, "covers_scene_id":null, "subtype":"television_glow_on_wall" }
{ "public_path":"lejeune/factory/F005_pine_treeline_dusk_wind.mp4", "act":0, "covers_scene_id":"S006", "subtype":"pine_treeline_dusk_wind" }
{ "public_path":"lejeune/factory/F006_coastal_marsh_fog_still.mp4", "act":0, "covers_scene_id":"S007", "subtype":"coastal_marsh_fog_still" }
{ "public_path":"lejeune/factory/F007_water_surface_black_slow.mp4", "act":0, "covers_scene_id":null, "subtype":"water_surface_black_slow" }
{ "public_path":"lejeune/factory/F008_steel_shelving_file_boxes.mp4", "act":0, "covers_scene_id":"S009", "subtype":"steel_shelving_file_boxes" }
{ "public_path":"lejeune/factory/F009_rural_two_lane_road_dusk.mp4", "act":0, "covers_scene_id":null, "subtype":"rural_two_lane_road_dusk" }
{ "public_path":"lejeune/factory/F010_kitchen_tap_running_close_02.mp4", "act":0, "covers_scene_id":null, "subtype":"kitchen_tap_running_close_02" }
{ "public_path":"lejeune/factory/F011_overcast_sky_low_cloud.mp4", "act":0, "covers_scene_id":"S014", "subtype":"overcast_sky_low_cloud" }
{ "public_path":"lejeune/factory/F012_empty_hallway_domestic_dim.mp4", "act":0, "covers_scene_id":null, "subtype":"empty_hallway_domestic_dim" }

// ACT I — THE BASE (act 1) — 40
{ "public_path":"lejeune/factory/F013_brick_duplex_row_morning.mp4", "act":1, "covers_scene_id":"S016", "subtype":"brick_duplex_row_morning" }
{ "public_path":"lejeune/factory/F014_concrete_walkway_lawn_wide.mp4", "act":1, "covers_scene_id":"S017", "subtype":"concrete_walkway_lawn_wide" }
{ "public_path":"lejeune/factory/F015_clothesline_sheets_wind.mp4", "act":1, "covers_scene_id":"S018", "subtype":"clothesline_sheets_wind" }
{ "public_path":"lejeune/factory/F016_screen_door_porch_light.mp4", "act":1, "covers_scene_id":null, "subtype":"screen_door_porch_light" }
{ "public_path":"lejeune/factory/F017_period_sedan_parked_kerb.mp4", "act":1, "covers_scene_id":"S021", "subtype":"period_sedan_parked_kerb" }
{ "public_path":"lejeune/factory/F018_parade_ground_empty_dawn.mp4", "act":1, "covers_scene_id":"S023", "subtype":"parade_ground_empty_dawn" }
{ "public_path":"lejeune/factory/F019_boots_on_asphalt_marching.mp4", "act":1, "covers_scene_id":"S024", "subtype":"boots_on_asphalt_marching" }
{ "public_path":"lejeune/factory/F020_water_tower_silhouette_sky.mp4", "act":1, "covers_scene_id":"S026", "subtype":"water_tower_silhouette_sky" }
{ "public_path":"lejeune/factory/F021_kitchen_sink_daylight_wide.mp4", "act":1, "covers_scene_id":"S028", "subtype":"kitchen_sink_daylight_wide" }
{ "public_path":"lejeune/factory/F022_kettle_steam_stovetop.mp4", "act":1, "covers_scene_id":null, "subtype":"kettle_steam_stovetop" }
{ "public_path":"lejeune/factory/F023_bathtub_filling_slow.mp4", "act":1, "covers_scene_id":"S030", "subtype":"bathtub_filling_slow" }
{ "public_path":"lejeune/factory/F024_garden_hose_grass_arc.mp4", "act":1, "covers_scene_id":"S031", "subtype":"garden_hose_grass_arc" }
{ "public_path":"lejeune/factory/F025_tricycle_still_on_concrete.mp4", "act":1, "covers_scene_id":"S033", "subtype":"tricycle_still_on_concrete" }
{ "public_path":"lejeune/factory/F026_swing_set_empty_wind.mp4", "act":1, "covers_scene_id":"S034", "subtype":"swing_set_empty_wind" }
{ "public_path":"lejeune/factory/F027_school_corridor_empty_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"school_corridor_empty_dim" }
{ "public_path":"lejeune/factory/F028_chain_link_fence_perimeter.mp4", "act":1, "covers_scene_id":"S036", "subtype":"chain_link_fence_perimeter" }
{ "public_path":"lejeune/factory/F029_pine_treeline_dusk_wind_02.mp4", "act":1, "covers_scene_id":null, "subtype":"pine_treeline_dusk_wind_02" }
{ "public_path":"lejeune/factory/F030_coastal_inlet_grey_water.mp4", "act":1, "covers_scene_id":"S038", "subtype":"coastal_inlet_grey_water" }
{ "public_path":"lejeune/factory/F031_red_clay_shoulder_roadside.mp4", "act":1, "covers_scene_id":"S039", "subtype":"red_clay_shoulder_roadside" }
{ "public_path":"lejeune/factory/F032_gymnasium_folding_chairs.mp4", "act":1, "covers_scene_id":null, "subtype":"gymnasium_folding_chairs" }
{ "public_path":"lejeune/factory/F033_family_table_set_empty.mp4", "act":1, "covers_scene_id":"S041", "subtype":"family_table_set_empty" }
{ "public_path":"lejeune/factory/F034_wall_calendar_pages_turn.mp4", "act":1, "covers_scene_id":"S042", "subtype":"wall_calendar_pages_turn" }
{ "public_path":"lejeune/factory/F035_ceiling_fan_slow_domestic.mp4", "act":1, "covers_scene_id":null, "subtype":"ceiling_fan_slow_domestic" }
{ "public_path":"lejeune/factory/F036_venetian_blinds_light_bars.mp4", "act":1, "covers_scene_id":"S044", "subtype":"venetian_blinds_light_bars" }
{ "public_path":"lejeune/factory/F037_bedroom_curtain_drawn_dim.mp4", "act":1, "covers_scene_id":"S045", "subtype":"bedroom_curtain_drawn_dim" }
{ "public_path":"lejeune/factory/F038_hallway_night_light_low.mp4", "act":1, "covers_scene_id":null, "subtype":"hallway_night_light_low" }
{ "public_path":"lejeune/factory/F039_rain_on_window_grey.mp4", "act":1, "covers_scene_id":"S047", "subtype":"rain_on_window_grey" }
{ "public_path":"lejeune/factory/F040_church_pews_empty_light.mp4", "act":1, "covers_scene_id":"S048", "subtype":"church_pews_empty_light" }
{ "public_path":"lejeune/factory/F041_winter_field_bare_trees.mp4", "act":1, "covers_scene_id":null, "subtype":"winter_field_bare_trees" }
{ "public_path":"lejeune/factory/F042_grass_verge_wind_grey.mp4", "act":1, "covers_scene_id":"S050", "subtype":"grass_verge_wind_grey" }
{ "public_path":"lejeune/factory/F043_kitchen_chair_empty_wide.mp4", "act":1, "covers_scene_id":"S051", "subtype":"kitchen_chair_empty_wide" }
{ "public_path":"lejeune/factory/F044_laundry_room_machines_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"laundry_room_machines_dim" }
{ "public_path":"lejeune/factory/F045_pavement_puddle_reflection.mp4", "act":1, "covers_scene_id":null, "subtype":"pavement_puddle_reflection" }
{ "public_path":"lejeune/factory/F046_flagpole_halyard_wind.mp4", "act":1, "covers_scene_id":null, "subtype":"flagpole_halyard_wind" }
{ "public_path":"lejeune/factory/F047_barracks_window_row_dusk.mp4", "act":1, "covers_scene_id":"S025", "subtype":"barracks_window_row_dusk" }
{ "public_path":"lejeune/factory/F048_asphalt_heat_shimmer_far.mp4", "act":1, "covers_scene_id":null, "subtype":"asphalt_heat_shimmer_far" }
{ "public_path":"lejeune/factory/F049_mailbox_row_small_town.mp4", "act":1, "covers_scene_id":null, "subtype":"mailbox_row_small_town" }
{ "public_path":"lejeune/factory/F050_dishes_drying_rack_window.mp4", "act":1, "covers_scene_id":"S029", "subtype":"dishes_drying_rack_window" }
{ "public_path":"lejeune/factory/F051_ice_cubes_in_a_glass.mp4", "act":1, "covers_scene_id":"S032", "subtype":"ice_cubes_in_a_glass" }
{ "public_path":"lejeune/factory/F052_lawn_sprinkler_evening.mp4", "act":1, "covers_scene_id":null, "subtype":"lawn_sprinkler_evening" }

// ACT II — AUGUST 1997 (act 2) — 34
{ "public_path":"lejeune/factory/F053_crt_television_static_dark.mp4", "act":2, "covers_scene_id":"S052", "subtype":"crt_television_static_dark" }
{ "public_path":"lejeune/factory/F054_television_glow_on_wall_02.mp4", "act":2, "covers_scene_id":"S058", "subtype":"television_glow_on_wall_02" }
{ "public_path":"lejeune/factory/F055_kitchen_night_single_bulb.mp4", "act":2, "covers_scene_id":"S059", "subtype":"kitchen_night_single_bulb" }
{ "public_path":"lejeune/factory/F056_plate_set_down_on_table.mp4", "act":2, "covers_scene_id":"S060", "subtype":"plate_set_down_on_table" }
{ "public_path":"lejeune/factory/F057_telephone_handset_lifted.mp4", "act":2, "covers_scene_id":"S062", "subtype":"telephone_handset_lifted" }
{ "public_path":"lejeune/factory/F058_typewriter_keys_striking.mp4", "act":2, "covers_scene_id":"S064", "subtype":"typewriter_keys_striking" }
{ "public_path":"lejeune/factory/F059_envelope_sealed_by_hand.mp4", "act":2, "covers_scene_id":"S065", "subtype":"envelope_sealed_by_hand" }
{ "public_path":"lejeune/factory/F060_post_box_slot_letter_drop.mp4", "act":2, "covers_scene_id":null, "subtype":"post_box_slot_letter_drop" }
{ "public_path":"lejeune/factory/F061_office_corridor_fluorescent.mp4", "act":2, "covers_scene_id":"S067", "subtype":"office_corridor_fluorescent" }
{ "public_path":"lejeune/factory/F062_filing_cabinet_drawer_slide.mp4", "act":2, "covers_scene_id":"S068", "subtype":"filing_cabinet_drawer_slide" }
{ "public_path":"lejeune/factory/F063_photocopier_light_bar_pass.mp4", "act":2, "covers_scene_id":"S069", "subtype":"photocopier_light_bar_pass" }
{ "public_path":"lejeune/factory/F064_paper_stack_growing_desk.mp4", "act":2, "covers_scene_id":"S071", "subtype":"paper_stack_growing_desk" }
{ "public_path":"lejeune/factory/F065_ring_binder_pages_flip.mp4", "act":2, "covers_scene_id":"S072", "subtype":"ring_binder_pages_flip" }
{ "public_path":"lejeune/factory/F066_index_tabs_close_macro.mp4", "act":2, "covers_scene_id":"S073", "subtype":"index_tabs_close_macro" }
{ "public_path":"lejeune/factory/F067_desk_lamp_switched_on_night.mp4", "act":2, "covers_scene_id":"S074", "subtype":"desk_lamp_switched_on_night" }
{ "public_path":"lejeune/factory/F068_pickup_truck_gravel_drive.mp4", "act":2, "covers_scene_id":null, "subtype":"pickup_truck_gravel_drive" }
{ "public_path":"lejeune/factory/F069_mailbox_flag_raised_rural.mp4", "act":2, "covers_scene_id":"S077", "subtype":"mailbox_flag_raised_rural" }
{ "public_path":"lejeune/factory/F070_government_building_steps.mp4", "act":2, "covers_scene_id":"S078", "subtype":"government_building_steps" }
{ "public_path":"lejeune/factory/F071_reception_counter_empty_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"reception_counter_empty_dim" }
{ "public_path":"lejeune/factory/F072_wall_clock_second_hand.mp4", "act":2, "covers_scene_id":"S080", "subtype":"wall_clock_second_hand" }
{ "public_path":"lejeune/factory/F073_cardboard_boxes_stacked_hall.mp4", "act":2, "covers_scene_id":"S081", "subtype":"cardboard_boxes_stacked_hall" }
{ "public_path":"lejeune/factory/F074_pen_on_ruled_page_macro.mp4", "act":2, "covers_scene_id":"S082", "subtype":"pen_on_ruled_page_macro" }
{ "public_path":"lejeune/factory/F075_dust_in_a_light_shaft.mp4", "act":2, "covers_scene_id":null, "subtype":"dust_in_a_light_shaft" }
{ "public_path":"lejeune/factory/F076_garage_workbench_dim.mp4", "act":2, "covers_scene_id":"S084", "subtype":"garage_workbench_dim" }
{ "public_path":"lejeune/factory/F077_night_porch_moths_lamp.mp4", "act":2, "covers_scene_id":"S085", "subtype":"night_porch_moths_lamp" }
{ "public_path":"lejeune/factory/F078_answering_machine_red_light.mp4", "act":2, "covers_scene_id":null, "subtype":"answering_machine_red_light" }
{ "public_path":"lejeune/factory/F079_road_at_night_headlights.mp4", "act":2, "covers_scene_id":null, "subtype":"road_at_night_headlights" }
{ "public_path":"lejeune/factory/F080_grey_dawn_over_rooftops.mp4", "act":2, "covers_scene_id":null, "subtype":"grey_dawn_over_rooftops" }
{ "public_path":"lejeune/factory/F081_coffee_cup_steam_kitchen.mp4", "act":2, "covers_scene_id":null, "subtype":"coffee_cup_steam_kitchen" }
{ "public_path":"lejeune/factory/F082_newspaper_press_rollers.mp4", "act":2, "covers_scene_id":"S066", "subtype":"newspaper_press_rollers" }
{ "public_path":"lejeune/factory/F083_microfilm_reader_screen_glow.mp4", "act":2, "covers_scene_id":"S070", "subtype":"microfilm_reader_screen_glow" }
{ "public_path":"lejeune/factory/F084_library_stacks_low_light.mp4", "act":2, "covers_scene_id":null, "subtype":"library_stacks_low_light" }
{ "public_path":"lejeune/factory/F085_rubber_stamp_pressed_paper.mp4", "act":2, "covers_scene_id":"S076", "subtype":"rubber_stamp_pressed_paper" }
{ "public_path":"lejeune/factory/F086_empty_chair_at_desk_night.mp4", "act":2, "covers_scene_id":null, "subtype":"empty_chair_at_desk_night" }

// ACT III — WHAT THE LAB WROTE (act 3) — 42
{ "public_path":"lejeune/factory/F087_laboratory_glassware_rack.mp4", "act":3, "covers_scene_id":"S086", "subtype":"laboratory_glassware_rack" }
{ "public_path":"lejeune/factory/F088_sample_bottles_on_bench.mp4", "act":3, "covers_scene_id":"S087", "subtype":"sample_bottles_on_bench" }
{ "public_path":"lejeune/factory/F089_pipette_drop_into_vial.mp4", "act":3, "covers_scene_id":"S088", "subtype":"pipette_drop_into_vial" }
{ "public_path":"lejeune/factory/F090_chart_recorder_pen_trace.mp4", "act":3, "covers_scene_id":"S090", "subtype":"chart_recorder_pen_trace" }
{ "public_path":"lejeune/factory/F091_analytical_instrument_dials.mp4", "act":3, "covers_scene_id":"S091", "subtype":"analytical_instrument_dials" }
{ "public_path":"lejeune/factory/F092_clipboard_carbon_form_macro.mp4", "act":3, "covers_scene_id":"S104", "subtype":"clipboard_carbon_form_macro" }
{ "public_path":"lejeune/factory/F093_ballpoint_writing_margin.mp4", "act":3, "covers_scene_id":"S105", "subtype":"ballpoint_writing_margin" }
{ "public_path":"lejeune/factory/F094_carbon_paper_lifted_macro.mp4", "act":3, "covers_scene_id":"S106", "subtype":"carbon_paper_lifted_macro" }
{ "public_path":"lejeune/factory/F095_valve_wheel_turning_rust.mp4", "act":3, "covers_scene_id":"S095", "subtype":"valve_wheel_turning_rust" }
{ "public_path":"lejeune/factory/F096_pipework_junction_industrial.mp4", "act":3, "covers_scene_id":"S096", "subtype":"pipework_junction_industrial" }
{ "public_path":"lejeune/factory/F097_pump_house_exterior_grass.mp4", "act":3, "covers_scene_id":"S097", "subtype":"pump_house_exterior_grass" }
{ "public_path":"lejeune/factory/F098_capped_well_head_field.mp4", "act":3, "covers_scene_id":"S098", "subtype":"capped_well_head_field" }
{ "public_path":"lejeune/factory/F099_storage_tank_seam_close.mp4", "act":3, "covers_scene_id":"S099", "subtype":"storage_tank_seam_close" }
{ "public_path":"lejeune/factory/F100_rusted_drum_in_grass.mp4", "act":3, "covers_scene_id":"S100", "subtype":"rusted_drum_in_grass" }
{ "public_path":"lejeune/factory/F101_industrial_barrels_row_yard.mp4", "act":3, "covers_scene_id":"S101", "subtype":"industrial_barrels_row_yard" }
{ "public_path":"lejeune/factory/F102_dry_cleaner_shopfront_dusk.mp4", "act":3, "covers_scene_id":"S092", "subtype":"dry_cleaner_shopfront_dusk" }
{ "public_path":"lejeune/factory/F103_garment_conveyor_moving.mp4", "act":3, "covers_scene_id":"S093", "subtype":"garment_conveyor_moving" }
{ "public_path":"lejeune/factory/F104_steam_press_release_cloud.mp4", "act":3, "covers_scene_id":"S094", "subtype":"steam_press_release_cloud" }
{ "public_path":"lejeune/factory/F105_back_lot_drain_grate_wet.mp4", "act":3, "covers_scene_id":"S102", "subtype":"back_lot_drain_grate_wet" }
{ "public_path":"lejeune/factory/F106_soil_cross_section_dig.mp4", "act":3, "covers_scene_id":"S103", "subtype":"soil_cross_section_dig" }
{ "public_path":"lejeune/factory/F107_groundwater_ripple_dark.mp4", "act":3, "covers_scene_id":null, "subtype":"groundwater_ripple_dark" }
{ "public_path":"lejeune/factory/F108_rain_soaking_into_ground.mp4", "act":3, "covers_scene_id":null, "subtype":"rain_soaking_into_ground" }
{ "public_path":"lejeune/factory/F109_drain_pipe_outfall_grey.mp4", "act":3, "covers_scene_id":null, "subtype":"drain_pipe_outfall_grey" }
{ "public_path":"lejeune/factory/F110_water_meter_dial_close.mp4", "act":3, "covers_scene_id":"S107", "subtype":"water_meter_dial_close" }
{ "public_path":"lejeune/factory/F111_control_panel_switches_old.mp4", "act":3, "covers_scene_id":"S108", "subtype":"control_panel_switches_old" }
{ "public_path":"lejeune/factory/F112_padlock_on_gate_closing.mp4", "act":3, "covers_scene_id":"S109", "subtype":"padlock_on_gate_closing" }
{ "public_path":"lejeune/factory/F113_kitchen_tap_shut_off_close.mp4", "act":3, "covers_scene_id":"S110", "subtype":"kitchen_tap_shut_off_close" }
{ "public_path":"lejeune/factory/F114_glass_of_water_untouched.mp4", "act":3, "covers_scene_id":"S111", "subtype":"glass_of_water_untouched" }
{ "public_path":"lejeune/factory/F115_office_in_out_tray_papers.mp4", "act":3, "covers_scene_id":"S113", "subtype":"office_in_out_tray_papers" }
{ "public_path":"lejeune/factory/F116_memo_pinned_to_board.mp4", "act":3, "covers_scene_id":"S114", "subtype":"memo_pinned_to_board" }
{ "public_path":"lejeune/factory/F117_steel_shelving_file_boxes_02.mp4", "act":3, "covers_scene_id":"S116", "subtype":"steel_shelving_file_boxes_02" }
{ "public_path":"lejeune/factory/F118_records_trolley_pushed_hall.mp4", "act":3, "covers_scene_id":"S117", "subtype":"records_trolley_pushed_hall" }
{ "public_path":"lejeune/factory/F119_ceiling_strip_light_flicker.mp4", "act":3, "covers_scene_id":null, "subtype":"ceiling_strip_light_flicker" }
{ "public_path":"lejeune/factory/F120_stairwell_concrete_descend.mp4", "act":3, "covers_scene_id":null, "subtype":"stairwell_concrete_descend" }
{ "public_path":"lejeune/factory/F121_map_table_lamp_overhead.mp4", "act":3, "covers_scene_id":"S120", "subtype":"map_table_lamp_overhead" }
{ "public_path":"lejeune/factory/F122_aerial_coastal_plain_slow.mp4", "act":3, "covers_scene_id":"S121", "subtype":"aerial_coastal_plain_slow" }
{ "public_path":"lejeune/factory/F123_river_estuary_from_above.mp4", "act":3, "covers_scene_id":"S122", "subtype":"river_estuary_from_above" }
{ "public_path":"lejeune/factory/F124_pine_canopy_from_above.mp4", "act":3, "covers_scene_id":null, "subtype":"pine_canopy_from_above" }
{ "public_path":"lejeune/factory/F125_hydrant_on_a_verge_grey.mp4", "act":3, "covers_scene_id":"S124", "subtype":"hydrant_on_a_verge_grey" }
{ "public_path":"lejeune/factory/F126_manhole_cover_wet_street.mp4", "act":3, "covers_scene_id":null, "subtype":"manhole_cover_wet_street" }
{ "public_path":"lejeune/factory/F127_water_surface_black_slow_02.mp4", "act":3, "covers_scene_id":null, "subtype":"water_surface_black_slow_02" }
{ "public_path":"lejeune/factory/F128_empty_meeting_room_chairs.mp4", "act":3, "covers_scene_id":"S125", "subtype":"empty_meeting_room_chairs" }

// ACT IV — THE MAN BORN ON THE BASE (act 4) — 42
{ "public_path":"lejeune/factory/F129_hospital_exterior_far_dusk.mp4", "act":4, "covers_scene_id":"S126", "subtype":"hospital_exterior_far_dusk" }
{ "public_path":"lejeune/factory/F130_waiting_room_chairs_empty.mp4", "act":4, "covers_scene_id":"S127", "subtype":"waiting_room_chairs_empty" }
{ "public_path":"lejeune/factory/F131_corridor_window_morning_far.mp4", "act":4, "covers_scene_id":null, "subtype":"corridor_window_morning_far" }
{ "public_path":"lejeune/factory/F132_birth_record_book_shelf.mp4", "act":4, "covers_scene_id":"S129", "subtype":"birth_record_book_shelf" }
{ "public_path":"lejeune/factory/F133_suburban_street_afternoon.mp4", "act":4, "covers_scene_id":"S130", "subtype":"suburban_street_afternoon" }
{ "public_path":"lejeune/factory/F134_home_office_desk_evening.mp4", "act":4, "covers_scene_id":"S131", "subtype":"home_office_desk_evening" }
{ "public_path":"lejeune/factory/F135_crt_monitor_cursor_blink.mp4", "act":4, "covers_scene_id":"S132", "subtype":"crt_monitor_cursor_blink" }
{ "public_path":"lejeune/factory/F136_dial_up_modem_lights.mp4", "act":4, "covers_scene_id":null, "subtype":"dial_up_modem_lights" }
{ "public_path":"lejeune/factory/F137_map_pins_corkboard_close.mp4", "act":4, "covers_scene_id":"S134", "subtype":"map_pins_corkboard_close" }
{ "public_path":"lejeune/factory/F138_index_cards_spread_table.mp4", "act":4, "covers_scene_id":"S135", "subtype":"index_cards_spread_table" }
{ "public_path":"lejeune/factory/F139_ring_binder_pages_flip_02.mp4", "act":4, "covers_scene_id":"S136", "subtype":"ring_binder_pages_flip_02" }
{ "public_path":"lejeune/factory/F140_telephone_cord_twisted_close.mp4", "act":4, "covers_scene_id":"S137", "subtype":"telephone_cord_twisted_close" }
{ "public_path":"lejeune/factory/F141_conference_table_long_empty.mp4", "act":4, "covers_scene_id":"S139", "subtype":"conference_table_long_empty" }
{ "public_path":"lejeune/factory/F142_microphone_on_a_table_close.mp4", "act":4, "covers_scene_id":"S140", "subtype":"microphone_on_a_table_close" }
{ "public_path":"lejeune/factory/F143_water_carafe_and_glasses.mp4", "act":4, "covers_scene_id":"S141", "subtype":"water_carafe_and_glasses" }
{ "public_path":"lejeune/factory/F144_wood_panelled_hall_dim.mp4", "act":4, "covers_scene_id":"S142", "subtype":"wood_panelled_hall_dim" }
{ "public_path":"lejeune/factory/F145_gallery_seating_rows_empty.mp4", "act":4, "covers_scene_id":"S143", "subtype":"gallery_seating_rows_empty" }
{ "public_path":"lejeune/factory/F146_stenograph_keys_close.mp4", "act":4, "covers_scene_id":null, "subtype":"stenograph_keys_close" }
{ "public_path":"lejeune/factory/F147_capitol_dome_dusk_wide.mp4", "act":4, "covers_scene_id":"S145", "subtype":"capitol_dome_dusk_wide" }
{ "public_path":"lejeune/factory/F148_government_corridor_marble.mp4", "act":4, "covers_scene_id":null, "subtype":"government_corridor_marble" }
{ "public_path":"lejeune/factory/F149_press_camera_shutters_row.mp4", "act":4, "covers_scene_id":"S147", "subtype":"press_camera_shutters_row" }
{ "public_path":"lejeune/factory/F150_report_binding_spiral_close.mp4", "act":4, "covers_scene_id":"S148", "subtype":"report_binding_spiral_close" }
{ "public_path":"lejeune/factory/F151_document_shredder_teeth.mp4", "act":4, "covers_scene_id":null, "subtype":"document_shredder_teeth" }
{ "public_path":"lejeune/factory/F152_redaction_marker_on_page.mp4", "act":4, "covers_scene_id":"S150", "subtype":"redaction_marker_on_page" }
{ "public_path":"lejeune/factory/F153_statistics_printout_fanfold.mp4", "act":4, "covers_scene_id":"S151", "subtype":"statistics_printout_fanfold" }
{ "public_path":"lejeune/factory/F154_lecture_hall_empty_seats.mp4", "act":4, "covers_scene_id":null, "subtype":"lecture_hall_empty_seats" }
{ "public_path":"lejeune/factory/F155_laboratory_glassware_rack_02.mp4", "act":4, "covers_scene_id":"S153", "subtype":"laboratory_glassware_rack_02" }
{ "public_path":"lejeune/factory/F156_centrifuge_spinning_slow.mp4", "act":4, "covers_scene_id":null, "subtype":"centrifuge_spinning_slow" }
{ "public_path":"lejeune/factory/F157_data_screen_scrolling_rows.mp4", "act":4, "covers_scene_id":"S155", "subtype":"data_screen_scrolling_rows" }
{ "public_path":"lejeune/factory/F158_veterans_hall_flags_dim.mp4", "act":4, "covers_scene_id":"S156", "subtype":"veterans_hall_flags_dim" }
{ "public_path":"lejeune/factory/F159_town_hall_folding_chairs.mp4", "act":4, "covers_scene_id":"S157", "subtype":"town_hall_folding_chairs" }
{ "public_path":"lejeune/factory/F160_parking_lot_dusk_cars.mp4", "act":4, "covers_scene_id":null, "subtype":"parking_lot_dusk_cars" }
{ "public_path":"lejeune/factory/F161_motel_sign_night_flicker.mp4", "act":4, "covers_scene_id":null, "subtype":"motel_sign_night_flicker" }
{ "public_path":"lejeune/factory/F162_interstate_at_night_long.mp4", "act":4, "covers_scene_id":null, "subtype":"interstate_at_night_long" }
{ "public_path":"lejeune/factory/F163_kitchen_table_papers_spread.mp4", "act":4, "covers_scene_id":"S161", "subtype":"kitchen_table_papers_spread" }
{ "public_path":"lejeune/factory/F164_wall_of_photographs_frames.mp4", "act":4, "covers_scene_id":"S162", "subtype":"wall_of_photographs_frames" }
{ "public_path":"lejeune/factory/F165_names_list_scrolling_paper.mp4", "act":4, "covers_scene_id":"S163", "subtype":"names_list_scrolling_paper" }
{ "public_path":"lejeune/factory/F166_envelope_pile_unopened.mp4", "act":4, "covers_scene_id":null, "subtype":"envelope_pile_unopened" }
{ "public_path":"lejeune/factory/F167_coastal_storm_cloud_build.mp4", "act":4, "covers_scene_id":null, "subtype":"coastal_storm_cloud_build" }
{ "public_path":"lejeune/factory/F168_hydrant_on_a_verge_grey_02.mp4", "act":4, "covers_scene_id":null, "subtype":"hydrant_on_a_verge_grey_02" }
{ "public_path":"lejeune/factory/F169_paper_stack_growing_desk_02.mp4", "act":4, "covers_scene_id":"S164", "subtype":"paper_stack_growing_desk_02" }
{ "public_path":"lejeune/factory/F170_window_reflection_dusk_room.mp4", "act":4, "covers_scene_id":"S165", "subtype":"window_reflection_dusk_room" }

// ACT V — THE TWO-YEAR WINDOW (act 5) — 30
{ "public_path":"lejeune/factory/F171_capitol_steps_daylight_wide.mp4", "act":5, "covers_scene_id":"S166", "subtype":"capitol_steps_daylight_wide" }
{ "public_path":"lejeune/factory/F172_pen_signing_document_close.mp4", "act":5, "covers_scene_id":"S167", "subtype":"pen_signing_document_close" }
{ "public_path":"lejeune/factory/F173_flag_and_podium_far_wide.mp4", "act":5, "covers_scene_id":null, "subtype":"flag_and_podium_far_wide" }
{ "public_path":"lejeune/factory/F174_courthouse_exterior_stone.mp4", "act":5, "covers_scene_id":"S170", "subtype":"courthouse_exterior_stone" }
{ "public_path":"lejeune/factory/F175_courtroom_interior_empty.mp4", "act":5, "covers_scene_id":"S171", "subtype":"courtroom_interior_empty" }
{ "public_path":"lejeune/factory/F176_judges_bench_empty_wide.mp4", "act":5, "covers_scene_id":null, "subtype":"judges_bench_empty_wide" }
{ "public_path":"lejeune/factory/F177_docket_pages_turning_fast.mp4", "act":5, "covers_scene_id":"S173", "subtype":"docket_pages_turning_fast" }
{ "public_path":"lejeune/factory/F178_claim_forms_stack_tall.mp4", "act":5, "covers_scene_id":"S174", "subtype":"claim_forms_stack_tall" }
{ "public_path":"lejeune/factory/F179_mail_sorting_trays_volume.mp4", "act":5, "covers_scene_id":"S175", "subtype":"mail_sorting_trays_volume" }
{ "public_path":"lejeune/factory/F180_server_room_lights_rows.mp4", "act":5, "covers_scene_id":null, "subtype":"server_room_lights_rows" }
{ "public_path":"lejeune/factory/F181_television_advert_glow_late.mp4", "act":5, "covers_scene_id":"S177", "subtype":"television_advert_glow_late" }
{ "public_path":"lejeune/factory/F182_remote_control_on_arm_chair.mp4", "act":5, "covers_scene_id":null, "subtype":"remote_control_on_arm_chair" }
{ "public_path":"lejeune/factory/F183_law_office_corridor_night.mp4", "act":5, "covers_scene_id":"S179", "subtype":"law_office_corridor_night" }
{ "public_path":"lejeune/factory/F184_cheque_book_on_a_desk.mp4", "act":5, "covers_scene_id":"S180", "subtype":"cheque_book_on_a_desk" }
{ "public_path":"lejeune/factory/F185_bank_counter_glass_dim.mp4", "act":5, "covers_scene_id":null, "subtype":"bank_counter_glass_dim" }
{ "public_path":"lejeune/factory/F186_calendar_month_page_torn.mp4", "act":5, "covers_scene_id":"S182", "subtype":"calendar_month_page_torn" }
{ "public_path":"lejeune/factory/F187_hourglass_sand_running.mp4", "act":5, "covers_scene_id":null, "subtype":"hourglass_sand_running" }
{ "public_path":"lejeune/factory/F188_care_home_window_evening.mp4", "act":5, "covers_scene_id":"S184", "subtype":"care_home_window_evening" }
{ "public_path":"lejeune/factory/F189_walking_stick_by_a_chair.mp4", "act":5, "covers_scene_id":null, "subtype":"walking_stick_by_a_chair" }
{ "public_path":"lejeune/factory/F190_hearing_table_binder_glass.mp4", "act":5, "covers_scene_id":"S186", "subtype":"hearing_table_binder_glass" }
{ "public_path":"lejeune/factory/F191_gavel_block_on_bench_close.mp4", "act":5, "covers_scene_id":null, "subtype":"gavel_block_on_bench_close" }
{ "public_path":"lejeune/factory/F192_stack_of_case_files_tall.mp4", "act":5, "covers_scene_id":"S188", "subtype":"stack_of_case_files_tall" }
{ "public_path":"lejeune/factory/F193_office_window_blinds_dusk.mp4", "act":5, "covers_scene_id":null, "subtype":"office_window_blinds_dusk" }
{ "public_path":"lejeune/factory/F194_deposition_room_chairs_pale.mp4", "act":5, "covers_scene_id":"S190", "subtype":"deposition_room_chairs_pale" }
{ "public_path":"lejeune/factory/F195_courthouse_corridor_bench.mp4", "act":5, "covers_scene_id":"S191", "subtype":"courthouse_corridor_bench" }
{ "public_path":"lejeune/factory/F196_rain_on_car_windscreen.mp4", "act":5, "covers_scene_id":null, "subtype":"rain_on_car_windscreen" }
{ "public_path":"lejeune/factory/F197_flag_at_half_staff_far.mp4", "act":5, "covers_scene_id":"S193", "subtype":"flag_at_half_staff_far" }
{ "public_path":"lejeune/factory/F198_memorial_lawn_far_wide.mp4", "act":5, "covers_scene_id":"S194", "subtype":"memorial_lawn_far_wide" }
{ "public_path":"lejeune/factory/F199_ring_binder_closed_table.mp4", "act":5, "covers_scene_id":"S195", "subtype":"ring_binder_closed_table" }
{ "public_path":"lejeune/factory/F200_grey_sky_gulls_coastal.mp4", "act":5, "covers_scene_id":null, "subtype":"grey_sky_gulls_coastal" }

// ENDING (act 6) — 14
{ "public_path":"lejeune/factory/F201_kitchen_dawn_light_slow.mp4", "act":6, "covers_scene_id":"S196", "subtype":"kitchen_dawn_light_slow" }
{ "public_path":"lejeune/factory/F202_empty_glass_on_a_table.mp4", "act":6, "covers_scene_id":"S197", "subtype":"empty_glass_on_a_table" }
{ "public_path":"lejeune/factory/F203_tap_dripping_once_close.mp4", "act":6, "covers_scene_id":"S198", "subtype":"tap_dripping_once_close" }
{ "public_path":"lejeune/factory/F204_binder_spine_row_shelf.mp4", "act":6, "covers_scene_id":"S199", "subtype":"binder_spine_row_shelf" }
{ "public_path":"lejeune/factory/F205_pine_treeline_first_light.mp4", "act":6, "covers_scene_id":"S201", "subtype":"pine_treeline_first_light" }
{ "public_path":"lejeune/factory/F206_coastal_marsh_dawn_still.mp4", "act":6, "covers_scene_id":"S202", "subtype":"coastal_marsh_dawn_still" }
{ "public_path":"lejeune/factory/F207_brick_duplex_row_dawn.mp4", "act":6, "covers_scene_id":"S203", "subtype":"brick_duplex_row_dawn" }
{ "public_path":"lejeune/factory/F208_calendar_page_still_autumn.mp4", "act":6, "covers_scene_id":"S205", "subtype":"calendar_page_still_autumn" }
{ "public_path":"lejeune/factory/F209_courthouse_door_closed_dawn.mp4", "act":6, "covers_scene_id":"S206", "subtype":"courthouse_door_closed_dawn" }
{ "public_path":"lejeune/factory/F210_water_glass_backlit_still.mp4", "act":6, "covers_scene_id":"S207", "subtype":"water_glass_backlit_still" }
{ "public_path":"lejeune/factory/F211_kitchen_chair_empty_dawn.mp4", "act":6, "covers_scene_id":"S208", "subtype":"kitchen_chair_empty_dawn" }
{ "public_path":"lejeune/factory/F212_wide_sky_clearing_slow.mp4", "act":6, "covers_scene_id":"S209", "subtype":"wide_sky_clearing_slow" }
{ "public_path":"lejeune/factory/F213_road_out_of_town_dawn.mp4", "act":6, "covers_scene_id":null, "subtype":"road_out_of_town_dawn" }
{ "public_path":"lejeune/factory/F214_still_water_horizon_grey.mp4", "act":6, "covers_scene_id":"S210", "subtype":"still_water_horizon_grey" }

// BRIDGING (covers_scene_id:null) — 21
{ "public_path":"lejeune/factory/F215_dust_motes_slow_drift.mp4", "act":null, "covers_scene_id":null, "subtype":"dust_motes_slow_drift" }
{ "public_path":"lejeune/factory/F216_paper_edge_turning_macro.mp4", "act":null, "covers_scene_id":null, "subtype":"paper_edge_turning_macro" }
{ "public_path":"lejeune/factory/F217_condensation_on_glass_run.mp4", "act":null, "covers_scene_id":null, "subtype":"condensation_on_glass_run" }
{ "public_path":"lejeune/factory/F218_water_ring_on_wood_table.mp4", "act":null, "covers_scene_id":null, "subtype":"water_ring_on_wood_table" }
{ "public_path":"lejeune/factory/F219_fluorescent_tube_warming.mp4", "act":null, "covers_scene_id":null, "subtype":"fluorescent_tube_warming" }
{ "public_path":"lejeune/factory/F220_ceiling_tile_grid_looking_up.mp4", "act":null, "covers_scene_id":null, "subtype":"ceiling_tile_grid_looking_up" }
{ "public_path":"lejeune/factory/F221_linoleum_floor_reflection.mp4", "act":null, "covers_scene_id":null, "subtype":"linoleum_floor_reflection" }
{ "public_path":"lejeune/factory/F222_door_closing_slow_interior.mp4", "act":null, "covers_scene_id":null, "subtype":"door_closing_slow_interior" }
{ "public_path":"lejeune/factory/F223_venetian_blinds_light_bars_02.mp4", "act":null, "covers_scene_id":null, "subtype":"venetian_blinds_light_bars_02" }
{ "public_path":"lejeune/factory/F224_rain_gutter_overflow_close.mp4", "act":null, "covers_scene_id":null, "subtype":"rain_gutter_overflow_close" }
{ "public_path":"lejeune/factory/F225_puddle_ripple_single_drop.mp4", "act":null, "covers_scene_id":null, "subtype":"puddle_ripple_single_drop" }
{ "public_path":"lejeune/factory/F226_grass_seedheads_backlit.mp4", "act":null, "covers_scene_id":null, "subtype":"grass_seedheads_backlit" }
{ "public_path":"lejeune/factory/F227_power_lines_against_sky.mp4", "act":null, "covers_scene_id":null, "subtype":"power_lines_against_sky" }
{ "public_path":"lejeune/factory/F228_gravel_underfoot_texture.mp4", "act":null, "covers_scene_id":null, "subtype":"gravel_underfoot_texture" }
{ "public_path":"lejeune/factory/F229_curtain_moving_in_a_draught.mp4", "act":null, "covers_scene_id":null, "subtype":"curtain_moving_in_a_draught" }
{ "public_path":"lejeune/factory/F230_clock_face_no_readable_time.mp4", "act":null, "covers_scene_id":null, "subtype":"clock_face_no_readable_time" }
{ "public_path":"lejeune/factory/F231_stack_of_boxes_silhouette.mp4", "act":null, "covers_scene_id":null, "subtype":"stack_of_boxes_silhouette" }
{ "public_path":"lejeune/factory/F232_night_window_from_outside.mp4", "act":null, "covers_scene_id":null, "subtype":"night_window_from_outside" }
{ "public_path":"lejeune/factory/F233_car_interior_dashboard_dusk.mp4", "act":null, "covers_scene_id":null, "subtype":"car_interior_dashboard_dusk" }
{ "public_path":"lejeune/factory/F234_wind_over_open_water_grey.mp4", "act":null, "covers_scene_id":null, "subtype":"wind_over_open_water_grey" }
{ "public_path":"lejeune/factory/F235_first_light_on_a_wall.mp4", "act":null, "covers_scene_id":null, "subtype":"first_light_on_a_wall" }
```

**検算:** 12 + 40 + 34 + 42 + 42 + 30 + 14 + 21 = **235** ✓

## 4.5 ★`motion[]` 全42エントリ（★必ず実体化・public_path 非空）

> エントリ形は §4.1a 準拠 + 動画フィールド。`asset_id ^LEJ-M\d{2}$`。`source_still` は §8.1a の種画像、`source_scene_id`=`MS<NN>`。runtime で `sha256`/`width 1280`/`height 720`/`fps 48`/`frames`/`duration_sec`/`qc` を埋める（§8.4）。**空配列を書かない。**

```jsonc
{ "asset_id":"LEJ-M01", "source_scene_id":"MS01", "source_still":"H:/pd-media/assets/ai/lejeune/M01_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M01_rife.mp4", "public_path":"lejeune/motion/M01_rife.mp4", "act":0, "storyboard":"hook", "tags":["tap_about_to_run_over_a_glass","H001_anon"] }
{ "asset_id":"LEJ-M02", "source_scene_id":"MS02", "source_still":"H:/pd-media/assets/ai/lejeune/M02_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M02_rife.mp4", "public_path":"lejeune/motion/M02_rife.mp4", "act":0, "storyboard":"A0-02", "tags":["television_light_about_to_change"] }
{ "asset_id":"LEJ-M03", "source_scene_id":"MS03", "source_still":"H:/pd-media/assets/ai/lejeune/M03_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M03_rife.mp4", "public_path":"lejeune/motion/M03_rife.mp4", "act":0, "storyboard":"A0-03", "tags":["pine_treeline_breathing_dusk"] }
{ "asset_id":"LEJ-M04", "source_scene_id":"MS04", "source_still":"H:/pd-media/assets/ai/lejeune/M04_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M04_rife.mp4", "public_path":"lejeune/motion/M04_rife.mp4", "act":1, "storyboard":"A1-01", "tags":["family_walking_to_base_quarters","H002_anon"] }
{ "asset_id":"LEJ-M05", "source_scene_id":"MS05", "source_still":"H:/pd-media/assets/ai/lejeune/M05_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M05_rife.mp4", "public_path":"lejeune/motion/M05_rife.mp4", "act":1, "storyboard":"A1-02", "tags":["sheets_on_a_line_before_the_gust"] }
{ "asset_id":"LEJ-M06", "source_scene_id":"MS06", "source_still":"H:/pd-media/assets/ai/lejeune/M06_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M06_rife.mp4", "public_path":"lejeune/motion/M06_rife.mp4", "act":1, "storyboard":"A1-03", "tags":["instructor_back_on_the_parade_deck","H003_anon"] }
{ "asset_id":"LEJ-M07", "source_scene_id":"MS07", "source_still":"H:/pd-media/assets/ai/lejeune/M07_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M07_rife.mp4", "public_path":"lejeune/motion/M07_rife.mp4", "act":1, "storyboard":"A1-04", "tags":["hands_filling_a_glass_at_a_sink","H004_anon"] }
{ "asset_id":"LEJ-M08", "source_scene_id":"MS08", "source_still":"H:/pd-media/assets/ai/lejeune/M08_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M08_rife.mp4", "public_path":"lejeune/motion/M08_rife.mp4", "act":1, "storyboard":"A1-05", "tags":["water_tower_against_a_moving_sky"] }
{ "asset_id":"LEJ-M09", "source_scene_id":"MS09", "source_still":"H:/pd-media/assets/ai/lejeune/M09_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M09_rife.mp4", "public_path":"lejeune/motion/M09_rife.mp4", "act":1, "storyboard":"A1-06", "tags":["tricycle_still_the_walkway_empty"] }
{ "asset_id":"LEJ-M10", "source_scene_id":"MS10", "source_still":"H:/pd-media/assets/ai/lejeune/M10_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M10_rife.mp4", "public_path":"lejeune/motion/M10_rife.mp4", "act":1, "storyboard":"A1-07", "tags":["adult_sitting_alone_at_a_table","H005_anon"] }
{ "asset_id":"LEJ-M11", "source_scene_id":"MS11", "source_still":"H:/pd-media/assets/ai/lejeune/M11_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M11_rife.mp4", "public_path":"lejeune/motion/M11_rife.mp4", "act":2, "storyboard":"A2-01", "tags":["a_man_standing_still_before_a_screen","H006_anon"] }
{ "asset_id":"LEJ-M12", "source_scene_id":"MS12", "source_still":"H:/pd-media/assets/ai/lejeune/M12_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M12_rife.mp4", "public_path":"lejeune/motion/M12_rife.mp4", "act":2, "storyboard":"A2-02", "tags":["a_plate_set_down_and_not_picked_up"] }
{ "asset_id":"LEJ-M13", "source_scene_id":"MS13", "source_still":"H:/pd-media/assets/ai/lejeune/M13_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M13_rife.mp4", "public_path":"lejeune/motion/M13_rife.mp4", "act":2, "storyboard":"A2-03", "tags":["hands_typing_a_records_request","H007_anon"] }
{ "asset_id":"LEJ-M14", "source_scene_id":"MS14", "source_still":"H:/pd-media/assets/ai/lejeune/M14_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M14_rife.mp4", "public_path":"lejeune/motion/M14_rife.mp4", "act":2, "storyboard":"A2-04", "tags":["an_envelope_poised_over_a_post_slot"] }
{ "asset_id":"LEJ-M15", "source_scene_id":"MS15", "source_still":"H:/pd-media/assets/ai/lejeune/M15_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M15_rife.mp4", "public_path":"lejeune/motion/M15_rife.mp4", "act":2, "storyboard":"A2-05", "tags":["a_filing_drawer_poised_to_shut"] }
{ "asset_id":"LEJ-M16", "source_scene_id":"MS16", "source_still":"H:/pd-media/assets/ai/lejeune/M16_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M16_rife.mp4", "public_path":"lejeune/motion/M16_rife.mp4", "act":2, "storyboard":"A2-06", "tags":["the_first_binder_opened_on_a_table","H008_anon"] }
{ "asset_id":"LEJ-M17", "source_scene_id":"MS17", "source_still":"H:/pd-media/assets/ai/lejeune/M17_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M17_rife.mp4", "public_path":"lejeune/motion/M17_rife.mp4", "act":3, "storyboard":"A3-01", "tags":["a_sample_bottle_held_to_a_lamp","H009_anon"] }
{ "asset_id":"LEJ-M18", "source_scene_id":"MS18", "source_still":"H:/pd-media/assets/ai/lejeune/M18_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M18_rife.mp4", "public_path":"lejeune/motion/M18_rife.mp4", "act":3, "storyboard":"A3-02", "tags":["a_pen_poised_in_a_form_margin","H010_anon"] }
{ "asset_id":"LEJ-M19", "source_scene_id":"MS19", "source_still":"H:/pd-media/assets/ai/lejeune/M19_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M19_rife.mp4", "public_path":"lejeune/motion/M19_rife.mp4", "act":3, "storyboard":"A3-03", "tags":["a_chart_recorder_needle_about_to_jump"] }
{ "asset_id":"LEJ-M20", "source_scene_id":"MS20", "source_still":"H:/pd-media/assets/ai/lejeune/M20_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M20_rife.mp4", "public_path":"lejeune/motion/M20_rife.mp4", "act":3, "storyboard":"A3-04", "tags":["a_solvent_drum_lid_in_long_grass"] }
{ "asset_id":"LEJ-M21", "source_scene_id":"MS21", "source_still":"H:/pd-media/assets/ai/lejeune/M21_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M21_rife.mp4", "public_path":"lejeune/motion/M21_rife.mp4", "act":3, "storyboard":"A3-05", "tags":["a_valve_wheel_a_breath_before_turning","H011_anon"] }
{ "asset_id":"LEJ-M22", "source_scene_id":"MS22", "source_still":"H:/pd-media/assets/ai/lejeune/M22_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M22_rife.mp4", "public_path":"lejeune/motion/M22_rife.mp4", "act":3, "storyboard":"A3-06", "tags":["a_tap_closing_over_a_dry_sink"] }
{ "asset_id":"LEJ-M23", "source_scene_id":"MS23", "source_still":"H:/pd-media/assets/ai/lejeune/M23_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M23_rife.mp4", "public_path":"lejeune/motion/M23_rife.mp4", "act":3, "storyboard":"A3-07", "tags":["a_form_sliding_into_a_folder"] }
{ "asset_id":"LEJ-M24", "source_scene_id":"MS24", "source_still":"H:/pd-media/assets/ai/lejeune/M24_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M24_rife.mp4", "public_path":"lejeune/motion/M24_rife.mp4", "act":3, "storyboard":"A3-08", "tags":["records_carton_lifted_from_a_shelf","H012_anon"] }
{ "asset_id":"LEJ-M25", "source_scene_id":"MS25", "source_still":"H:/pd-media/assets/ai/lejeune/M25_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M25_rife.mp4", "public_path":"lejeune/motion/M25_rife.mp4", "act":4, "storyboard":"A4-01", "tags":["a_man_alone_at_a_lit_home_desk","H013_anon"] }
{ "asset_id":"LEJ-M26", "source_scene_id":"MS26", "source_still":"H:/pd-media/assets/ai/lejeune/M26_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M26_rife.mp4", "public_path":"lejeune/motion/M26_rife.mp4", "act":4, "storyboard":"A4-02", "tags":["index_cards_laid_out_one_by_one","H014_anon"] }
{ "asset_id":"LEJ-M27", "source_scene_id":"MS27", "source_still":"H:/pd-media/assets/ai/lejeune/M27_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M27_rife.mp4", "public_path":"lejeune/motion/M27_rife.mp4", "act":4, "storyboard":"A4-03", "tags":["map_pins_pushed_into_a_corkboard","H015_anon"] }
{ "asset_id":"LEJ-M28", "source_scene_id":"MS28", "source_still":"H:/pd-media/assets/ai/lejeune/M28_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M28_rife.mp4", "public_path":"lejeune/motion/M28_rife.mp4", "act":4, "storyboard":"A4-04", "tags":["a_microphone_and_an_untouched_glass"] }
{ "asset_id":"LEJ-M29", "source_scene_id":"MS29", "source_still":"H:/pd-media/assets/ai/lejeune/M29_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M29_rife.mp4", "public_path":"lejeune/motion/M29_rife.mp4", "act":4, "storyboard":"A4-05", "tags":["a_hearing_gallery_settling_into_stillness","H016_anon"] }
{ "asset_id":"LEJ-M30", "source_scene_id":"MS30", "source_still":"H:/pd-media/assets/ai/lejeune/M30_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M30_rife.mp4", "public_path":"lejeune/motion/M30_rife.mp4", "act":4, "storyboard":"A4-06", "tags":["a_report_withdrawn_from_a_shelf"] }
{ "asset_id":"LEJ-M31", "source_scene_id":"MS31", "source_still":"H:/pd-media/assets/ai/lejeune/M31_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M31_rife.mp4", "public_path":"lejeune/motion/M31_rife.mp4", "act":4, "storyboard":"A4-07", "tags":["a_wall_of_names_growing_in_a_room","H017_anon"] }
{ "asset_id":"LEJ-M32", "source_scene_id":"MS32", "source_still":"H:/pd-media/assets/ai/lejeune/M32_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M32_rife.mp4", "public_path":"lejeune/motion/M32_rife.mp4", "act":4, "storyboard":"A4-08", "tags":["storm_light_moving_over_a_coast"] }
{ "asset_id":"LEJ-M33", "source_scene_id":"MS33", "source_still":"H:/pd-media/assets/ai/lejeune/M33_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M33_rife.mp4", "public_path":"lejeune/motion/M33_rife.mp4", "act":5, "storyboard":"A5-01", "tags":["a_pen_poised_above_a_signing_page","H018_anon"] }
{ "asset_id":"LEJ-M34", "source_scene_id":"MS34", "source_still":"H:/pd-media/assets/ai/lejeune/M34_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M34_rife.mp4", "public_path":"lejeune/motion/M34_rife.mp4", "act":5, "storyboard":"A5-02", "tags":["claim_forms_stacking_higher"] }
{ "asset_id":"LEJ-M35", "source_scene_id":"MS35", "source_still":"H:/pd-media/assets/ai/lejeune/M35_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M35_rife.mp4", "public_path":"lejeune/motion/M35_rife.mp4", "act":5, "storyboard":"A5-03", "tags":["a_docket_page_about_to_turn"] }
{ "asset_id":"LEJ-M36", "source_scene_id":"MS36", "source_still":"H:/pd-media/assets/ai/lejeune/M36_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M36_rife.mp4", "public_path":"lejeune/motion/M36_rife.mp4", "act":5, "storyboard":"A5-04", "tags":["a_late_night_television_glow_alone"] }
{ "asset_id":"LEJ-M37", "source_scene_id":"MS37", "source_still":"H:/pd-media/assets/ai/lejeune/M37_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M37_rife.mp4", "public_path":"lejeune/motion/M37_rife.mp4", "act":5, "storyboard":"A5-05", "tags":["an_empty_courtroom_waiting"] }
{ "asset_id":"LEJ-M38", "source_scene_id":"MS38", "source_still":"H:/pd-media/assets/ai/lejeune/M38_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M38_rife.mp4", "public_path":"lejeune/motion/M38_rife.mp4", "act":5, "storyboard":"A5-06", "tags":["a_calendar_page_lifting_at_a_corner"] }
{ "asset_id":"LEJ-M39", "source_scene_id":"MS39", "source_still":"H:/pd-media/assets/ai/lejeune/M39_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M39_rife.mp4", "public_path":"lejeune/motion/M39_rife.mp4", "act":6, "storyboard":"A6-01", "tags":["a_binder_closing_on_a_kitchen_table"] }
{ "asset_id":"LEJ-M40", "source_scene_id":"MS40", "source_still":"H:/pd-media/assets/ai/lejeune/M40_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M40_rife.mp4", "public_path":"lejeune/motion/M40_rife.mp4", "act":6, "storyboard":"A6-02", "tags":["one_drop_gathering_at_a_tap"] }
{ "asset_id":"LEJ-M41", "source_scene_id":"MS41", "source_still":"H:/pd-media/assets/ai/lejeune/M41_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M41_rife.mp4", "public_path":"lejeune/motion/M41_rife.mp4", "act":6, "storyboard":"A6-03", "tags":["dawn_reaching_a_row_of_quarters"] }
{ "asset_id":"LEJ-M42", "source_scene_id":"MS42", "source_still":"H:/pd-media/assets/ai/lejeune/M42_src.png", "path":"H:/pd-media/assets/ai_video/lejeune/M42_rife.mp4", "public_path":"lejeune/motion/M42_rife.mp4", "act":6, "storyboard":"A6-04", "tags":["still_water_holding_the_last_light"] }
```

**検算:** act0 3 + act1 7 + act2 6 + act3 8 + act4 8 + act5 6 + act6 4 = **42** ✓ ／ 人物種（H001–H018）= **18本** ✓

## 4.6 `overlay[]` 30エントリ（distinct 素材に数えない・15 particle / 10 light / 5 vfx）

```jsonc
{ "public_path":"lejeune/overlay/P01_kitchen_dust_slow.mp4", "type":"particle_assets", "subtype":"kitchen_dust_slow", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P02_archive_dust_cold.mp4", "type":"particle_assets", "subtype":"archive_dust_cold", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P03_coastal_mist_drift.mp4", "type":"particle_assets", "subtype":"coastal_mist_drift", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P04_fine_rain_vertical.mp4", "type":"particle_assets", "subtype":"fine_rain_vertical", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P05_paper_fiber_drift.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P06_water_caustics_faint.mp4", "type":"particle_assets", "subtype":"water_caustics_faint", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P07_pine_pollen_air.mp4", "type":"particle_assets", "subtype":"pine_pollen_air", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P08_steam_wisp_dim.mp4", "type":"particle_assets", "subtype":"steam_wisp_dim", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P09_fine_grain_dust.mp4", "type":"particle_assets", "subtype":"fine_grain_dust", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P10_dawn_dust_pale.mp4", "type":"particle_assets", "subtype":"dawn_dust_pale", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P11_kitchen_dust_slow_02.mp4", "type":"particle_assets", "subtype":"kitchen_dust_slow_02", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P12_archive_dust_cold_02.mp4", "type":"particle_assets", "subtype":"archive_dust_cold_02", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P13_coastal_mist_drift_02.mp4", "type":"particle_assets", "subtype":"coastal_mist_drift_02", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P14_paper_fiber_drift_02.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift_02", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/P15_dawn_dust_pale_02.mp4", "type":"particle_assets", "subtype":"dawn_dust_pale_02", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/L01_kitchen_window_light_bar.mp4", "type":"light_assets", "subtype":"kitchen_window_light_bar", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/L02_fluorescent_office_wash.mp4", "type":"light_assets", "subtype":"fluorescent_office_wash", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/L03_single_desk_lamp_glow.mp4", "type":"light_assets", "subtype":"single_desk_lamp_glow", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/L04_television_flicker_cold.mp4", "type":"light_assets", "subtype":"television_flicker_cold", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/L05_record_daylight_pale.mp4", "type":"light_assets", "subtype":"record_daylight_pale", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/L06_water_reflected_ceiling.mp4", "type":"light_assets", "subtype":"water_reflected_ceiling", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/L07_headlight_sweep_night.mp4", "type":"light_assets", "subtype":"headlight_sweep_night", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/L08_kitchen_window_light_bar_02.mp4", "type":"light_assets", "subtype":"kitchen_window_light_bar_02", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/L09_record_daylight_pale_02.mp4", "type":"light_assets", "subtype":"record_daylight_pale_02", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/L10_fluorescent_office_wash_02.mp4", "type":"light_assets", "subtype":"fluorescent_office_wash_02", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/V01_film_grain_fine.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine", "blend_hint":"overlay" }
{ "public_path":"lejeune/overlay/V02_cold_light_noise.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/V03_film_grain_fine_02.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine_02", "blend_hint":"overlay" }
{ "public_path":"lejeune/overlay/V04_water_ripple_min.mp4", "type":"vfx_overlays", "subtype":"water_ripple_min", "blend_hint":"screen" }
{ "public_path":"lejeune/overlay/V05_paper_edge_light_min.mp4", "type":"vfx_overlays", "subtype":"paper_edge_light_min", "blend_hint":"screen" }
```

**検算:** 15 + 10 + 5 = 30 ✓。runtime で `asset_id`/`path`/`sha256`/`license`/`eyeballed_content`/`qc` を埋める。**overlay は `cuts[].src` に出さない。★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない（screen-wash ≤0.07）。scanline/CRT/vignette-wash の overlay を選ばない。** **record-daylight の light（L05/L09）は 2007 公聴会 / 2012 / 2022 / ENDING 用のみ。** 他話色（electric blue / sodium prison gold / porch amber / teal-green hospital / crimson kitchen / forest-green / civil-violet / somber-plum / steel-cyan / evidence-blue / interrogation green-gray / signage red / phosphor green / shop-lamp amber）を選ばない。

---

# 5. A-1: SDXL 静止画のバッチ生成（210本 × 1枚・バリエーション0）— ★motif ライブラリ方式

## 5.0 ★★ 四層構成の中での LAYER 3 という位置づけ（owner directive 2026-07-29）★★

本作は **4レイヤー**で組む。Codex 静止画（本書 §5）は**そのうちの一層**であり、「主役」ではない。

| Layer | 中身 | 担当カット（設計値） | 全カット 563 に対する比率 |
|---|---|---|---|
| **L1 実写アーカイブ / factory** | 111,821点のアーカイブ（NARA 1,319 / LoC 610 / NASA / NOAA / IA / NYPL 等）＋ factory 棚 88,740点から選抜した **235本** | **235カット** | **41.7%** |
| **L2 After Effects ヒーローカード** | 6種の実装済みレイアウトのみ・**17枚**・各カードが台帳の実数を「動くタイポ」で運ぶ | 合成レイヤー（カットに数えない・約100秒占有） | 上乗せ |
| **L3 Codex AI 静止画** | **210枚**（うち ★人物在席 85枚 = 40.5%）— **アーカイブで撮れないもの専用**（描いてはいけない対象・実在人物の肖像リスクがある対象・象徴） | **244カット** | **43.3%** |
| **L4 i2v モーション + overlay** | i2v **42本**（→84カット）＋ overlay **30本** | **84カット** | **14.9%** |

> **L3 の役割は「穴埋め」に変わった。** アーカイブ・factory に**実物がある絵は L1 で撮る**（水道・グラス・松林・湿地・書類箱・法廷・議事堂・研究室ガラス器具・ドラム缶・住宅街）。
> **L3 が担うのは、(a) 実写では絶対に撮ってはいけないもの**（病気の子ども＝そもそも描かない／不在と物で運ぶ構図）、**(b) 実在人物の肖像リスクがあるもの**（父・娘・議員・司令官）、**(c) 現実に存在しない象徴**（bury/unbury の状態連鎖、名簿の増殖、時間の圧縮）。
> **L3 の点数（210）は減らさない。** 本節は L1 に置き換えられるのではなく、**L1 が加わったぶん L3 の一枚あたりの意味が重くなる**。

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-058-lejeune/04_scenes/ai_prompts.v001.md   ← A が §5.9 の形式で書く
出力:  H:\pd-media\assets\ai\lejeune\S<NNN>.png（+ remotion/public/lejeune/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★210本の作り方＝「motif ライブラリ」テンプレート方式

210 の固有プロンプトを**幕×motifで体系化**する。各 motif に (a) **確定 distinct 枚数**、(b) **S番号レンジ**、(c) **literal プロンプト** を与える。**S001–S210 の全210行は本書 §5.6 に literal で書き切ってある。Codex はそのまま `ai_prompts.v001.md` に転記する**（変奏を新たに書かない・行を増減しない・S番号を並べ替えない）。

> ★**1シーン1枚・variants 0。** 各プロンプト末尾に §5.3 の `[STYLE]`（人物なし象徴 still）**または** §5.11 の `[HSTYLE]`（匿名人物 still）を**全文連結**、`Avoid:` の後に §5.4 `[NEG]`（象徴）**または** §5.11 `[HNEG]`（匿名人物）を**全文連結**。
> **★2レーン構成: 210 body = object/symbolic 125枚（`[STYLE]`+`[NEG]`・人物なし）＋ ★human-present 85枚（40.5%・`[HSTYLE]`+`[HNEG]`・匿名/非識別・背向き/影/silhouette/hands・adults only）。** 該当 S-range は §5.6 で `★HP` と明記。
> **HARD BAN（不変・両レーン共通）: 病気/死にゆく子どもの描写なし・子どもの遺体/棺/墓なし・医療行為/医療機器なし・実在人物 likeness なし・実在の部隊章/エンブレム/ロゴなし・可読テキストなし・因果の断定なし。**

## 5.3 共通スタイル `[STYLE]`（object/symbolic 125枚 ＋ 抽象 i2v 種に連結・DESIGN §1 と一字一致）

```
, cinematic still, somber documentary grade, humid Carolina coastal-plain light as the base register, a chlorinated tap-water aqua as the one recurring cool system note carried by water taps glasses pipes and valves, pine-and-clay dusk reserved strictly for exteriors and treelines and roadside earth, a solvent-drum ochre reserved only for degreaser drums and disposal-yard metal, a pale record-daylight note reserved only for hearing rooms and signing tables and the final dawn, period-correct United States 1953 to 2026 with era-correct domestic fittings where interiors appear, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key soft-shadow lighting, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, no children, no medical equipment, empty rooms as aftermath, objects and water as witnesses
```

> **EP39〜EP57 の色語（1語も含めない）:** electric blue / sodium prison gold（EP41）/ porch-amber（EP43）/ teal-green hospital / crimson kitchen（EP45）/ forest-green / civil-violet / somber-plum / steel-cyan（EP50）/ evidence-blue #3F5E8C（EP52）/ interrogation green-gray #7C9082（EP55）/ signage red #C8102E・phosphor green #3FA66A・shop-lamp amber #E4B96B（EP56）。
> **EP58 の色 = humid coastal grey（基調）＋ tap-water aqua `#4FA3B4`（水の系統色・タイポと figures の accent）＋ pine-and-clay dusk `#7A5236`（屋外環境のみ）＋ solvent-drum ochre `#B0762A`（ドラム缶と廃棄場の金属のみ・≤6枚）＋ record-daylight `#D6E0E4`（公聴会/署名/ENDING のみ）。INK `#090B0C`。**

## 5.4 共通ネガティブ `[NEG]`（各 `Avoid:` の後に全文付ける・A/B 同一）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible form, legible report, legible newspaper, legible court record, legible date, license plate, military insignia, unit patch, rank device, service emblem, readable base sign, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, front-facing person, child, children, toddler, baby, sick child, dying child, hospital bed, patient, IV drip, syringe, medical chart, x-ray, scan image, chemotherapy, oncology ward, examination room, operating theatre, doctor examining, nurse, wheelchair with a person, coffin, casket, funeral, grave, headstone, cemetery close-up, mourner weeping, wounds, blood, gore, corpse, violence, re-enactment of harm, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, evidence-blue bandana, interrogation green-gray, signage red, phosphor green, shop-lamp amber, milky haze, foggy wash, scanline, CRT texture, vignette wash
```

> 文字/紙面が必要な絵は「blurred into an unreadable smear」で判読不能に。**子ども・医療・墓・遺体・実在の軍章を NEG で明示抑制。** この `[NEG]` は象徴 body ＋ 抽象 i2v 種にのみ使う。**人物ビート（§5.11 H シリーズ・§5.12 thumb_face・§5.13 F シリーズ）には使わない**（人物を弾くため）。H/thumb/F は `[HNEG]`/`[TNEG]`/`[FNEG]` を使う。

## 5.5 プロンプトの絶対ルール（210本すべてに適用）

- **body 210 は2レーン（§5.2）:** object/symbolic 125枚＝§5.3/§5.4（人物なし）、**human-present 85枚（40.5%）＝§5.11 `[HSTYLE]`/`[HNEG]`**。
- **可読文字なし。** 分析票・報告書・新聞・判決・法案・訴状・小切手・バインダーのタブ・基地の看板を**読める形で描かない**。
- **★病気の子ども・死にゆく子ども・子どもの遺体/棺/墓を一切描かない。健康な子どもも本作では描かない**（誤読リスク）。子どもの存在は**不在の痕跡のみ**（三輪車・空いた椅子・片付いたベッド・玄関の小さな長靴）。
- **★医療行為・医療機器を一切描かない。** 病室・処置室・点滴・注射器・カルテ・スキャンを描かない。医療の気配は「無人の待合椅子列」「消灯した廊下の遠景」まで。
- **R-CAUSATION:** 「水が殺した」「がんの原因」の含意を絵にも語にも作らない。物・場所・記録だけを描く。
- **R-INSIGNIA:** 実在の部隊章・エンブレム・旗の意匠・階級章・企業ロゴを描かない。制服は無地・肩から下・後ろ姿で処理。
- **tap-water aqua `#4FA3B4` 基調。pine-and-clay dusk `#7A5236` は屋外のみ。solvent-drum ochre `#B0762A` はドラム/廃棄場の金属のみ（≤6枚）。record-daylight `#D6E0E4` は ACT4 後半の公聴会 ＋ ACT5 の署名 ＋ ENDING のみ。**
- **時代考証:** 1953–2026。1970–80年代のビートに現代車/スマホ/LED/現代の看板/現代のキッチンを混ぜない。
- **★footage treatment は bleed/parallax。depth 前提の絵作りをしない。**
- **`dochighlight` を作らない・書かない（BANNED）。`DATE_STAMP` レイアウトを使わない（BANNED・存在しない）。milky wash / scanline を描かない。**

## 5.5a ★反復禁止ルール（motif de-repetition・BINDING）

1. **1ビート内は同一 motif のバリエーション最大2枚。** 3枚以上の同一被写体ブロックを作らない。
2. **幕をまたぐ motif の再登場は「目に見える状態変化」必須。同状態の撮り直しは禁止。** spine motif の状態連鎖（各状態1–2枚まで・状態語を各プロンプト本文に内蔵済み）:
   - **tap & glass** = ordinary and running(S001–S002) → filled and unremarked in daylight(S027–S028) → still full and untouched while the form exists(S111) → shut off over a dry sink(S110) → standing on a hearing table(S186) → empty in dawn light(S197/S207)。
   - **the form (carbon-copy analytical record)** = blank on a clipboard(S086) → written in the margin(S104–S105) → carbon lifted(S106) → slid into a folder(S112) → boxed(S116) → requested and returned redacted(S150) → stacked as an exhibit(S188)。**この7状態以外の form 行を作らない。**
   - **the binder** = first empty binder opened(S072) → tabs multiplying(S073) → a shelf of them(S136) → carried to a table(S186) → closed at dawn(S199/S204)。
   - **base quarters exterior** = 1970s morning(S016) → winter dusk mid-film(S045) → dawn now(S203)。**3状態のみ。**
   - **the well head / pump house** = running(S097) → capped(S098) → padlocked(S109)。
3. **Codex one-shot 原則:** 各行1枚・一発で決める。再生成は §6 の QC fail 時のみ（同一プロンプト・別シード1枚・§6.3）。**「複数枚から選ぶ」ためのバリエーション生成は禁止**（variants 0・§5.10 と同義）。
4. **CHILD GATE 不変:** 子どもを描かない・医療を描かない・墓を描かない。§1.1-2/§1.1-3/§1.2 はこの再構成で1文字も緩めていない。
5. **★HP anti-samey 変化マトリクス（85枚全体に適用）:** 距離（hands macro／medium／wide／far-wide）×角度（背後正対／後方斜め／low angle／over-the-shoulder）×年代 wardrobe（1950s／60s／70s／80s／90s／2000s／2020s）×光（humid daylight／kitchen tungsten／fluorescent office／night exterior／record-daylight）×setting（quarters／parade deck／kitchen／office／records room／lab／hearing room／courthouse／town hall／roadside）×人数（solo／2–4人／列／群衆）×姿勢（座って待つ／立つ／歩く／読む／書く／手元作業）。**HARD: どの2枚の ★HP も「被写体タイプ＋構図＋光」の3要素同時一致を禁止。**

## 5.6 ★motif ライブラリ（幕別・distinct 数確定・S番号レンジ・literal プロンプト全210行）

> **★S001–S210 の全210行を literal 化済み。Codex は各行をそのまま `ai_prompts.v001.md` に転記する**（変奏を新たに書かない・行を増減しない・S番号を並べ替えない）。
> **★`[STYLE]`/`[NEG]`＝人物なし象徴。`★HP`＝§5.11 `[HSTYLE]`/`[HNEG]`（匿名・非識別の人物）。** ★HP 合計 = **85枚（40.5%）**:
> ACT0 **3**（S001, S004, S010）／ACT1 **16**（S017, S019, S020, S022, S024, S028, S029, S035, S037, S040, S042, S043, S046, S047, S048, S049）／ACT2 **14**（S053, S057, S059, S061, S062, S064, S068, S071, S074, S077, S079, S082, S083, S085）／ACT3 **15**（S087, S091, S093, S095, S097, S103, S105, S108, S111, S113, S115, S117, S119, S123, S125）／ACT4 **16**（S127, S131, S135, S137, S138, S143, S144, S147, S152, S154, S156, S157, S159, S161, S163, S165）／ACT5 **18**（S166, S167, S169, S171, S172, S174, S176, S178, S179, S181, S183, S185, S187, S189, S190, S191, S192, S195）／ACT6 **3**（S200, S204, S209）。

### ACT 0 — HOOK + OPENING（15枚・S001–S015）
- **tap_and_glass_hook — 2 — S001–S002**（S001 は also_thumb・**hook signature**）
```
- `S001.png`
A kitchen tap running hard into a plain drinking glass on a worn enamel sink at night, one overhead fixture throwing a hard pool of light, the water reading faintly wrong under it, an anonymised adult in a plain shirt turned three-quarters away at the counter so no face reads, ordinary domestic clutter beyond, era-correct fittings, no readable text [HSTYLE] Avoid: [HNEG]
- `S002.png`
A single plain drinking glass filled to the brim standing alone on a dark kitchen counter, backlit so the water body glows a cold aqua and the meniscus catches one hard edge of light, everything else falling to near-black, an ordinary object about to become the whole story, no person, no readable text [STYLE] Avoid: [NEG]
```
- **night_kitchen_interior — 2 — S003, S005**
```
- `S003.png`
A dark kitchen window seen from inside at night, condensation beading the lower panes, the black yard beyond giving nothing back, a dish towel folded over the rail below, the room lit only by what spills from another doorway, no person, no readable text [STYLE] Avoid: [NEG]
- `S005.png`
A dinner plate set down on a laminate table and left untouched, the food gone matte and cold, a fork laid across the rim, one low lamp raking the surface, the chair beyond pushed slightly back, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_man_who_stopped — 2 — S004, S010**
```
- `S004.png`
An anonymised adult man standing motionless in a doorway, shoulders squared and head slightly turned, the cold flicker of a television washing across his back and the wall beside him, his face lost entirely to shadow, the corridor behind him dark, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **treeline_and_marsh — 2 — S006–S007**
```
- `S006.png`
A dense loblolly pine treeline at dusk under a bruised coastal sky, the trunks black and the canopy still holding one last band of pine-and-clay light, a flat cleared verge in front, the air heavy and humid, no people, no readable text [STYLE] Avoid: [NEG]
- `S007.png`
A wide brackish coastal marsh at first dark, low fog lying flat on standing water, spartina grass in silhouette, a channel cutting through the middle and reflecting the last of the sky, immense and quiet, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_buried_record — 2 — S008–S009**
```
- `S008.png`
A carbon-copy analytical result form lying face up in the bottom of an opened steel drawer, every typed line and every handwritten mark dissolved into an unreadable smear, one cold edge of light across the paper, the drawer front cutting the top of the frame, no person, no readable text [STYLE] Avoid: [NEG]
- `S009.png`
A long aisle of grey steel archive shelving receding into blackness, records cartons stacked to the ceiling on both sides, a single fluorescent tube burning near the camera and nothing beyond, symmetrical one-point perspective, no people, no readable text [STYLE] Avoid: [NEG]
```
```
- `S010.png`
An anonymised adult's forearms and hands resting flat on the closed cover of a thick three-ring binder on a kitchen table at night, knuckles heavy, wedding band catching one point of lamplight, the rest of the man out of frame above, the binder tabs blank, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **quarters_at_night — 1 — S011**
```
- `S011.png`
A long row of low brick base-housing duplexes at night, identical stoops and identical screen doors, a single upstairs window lit yellow in the whole row, cropped lawns going blue-black, no signage anywhere, no people, no readable text [STYLE] Avoid: [NEG]
```
- **title_beds — 4 — S012–S015**
```
- `S012.png`
An abstract near-black field crossed by soft horizontal bands of cold aqua luminance, like light coming through frosted wire glass, fine grain, a pure atmosphere bed built for type, no objects, no people, no readable text [STYLE] Avoid: [NEG]
- `S013.png`
Extreme macro of the surface tension at the rim of a glass of water, the meniscus curving up as a thin bright line against near-black, one suspended bubble clinging beneath, cold aqua refraction, abstract and clinical, no people, no readable text [STYLE] Avoid: [NEG]
- `S014.png`
A low ceiling of unbroken overcast pressing down on a flat coastal plain, the horizon a single grey rule near the bottom of the frame, vast negative space above, humid haze softening everything, no people, no readable text [STYLE] Avoid: [NEG]
- `S015.png`
A municipal water tower standing as a pure black silhouette against a night sky faintly lit from below, its legs splayed and its tank a heavy ellipse, enormous empty sky around it for type, no signage on the tank, no people, no readable text [STYLE] Avoid: [NEG]
```

### ACT 1 — THE BASE（36枚・S016–S051）
- **quarters_by_day — 2 — S016, S021**
```
- `S016.png`
A row of low brick family quarters on a military base on a bright 1970s morning, mown grass strips and concrete stoops, aluminium storm doors, a folded newspaper on one step, period-correct and entirely ordinary, no signage, no people, no readable text [STYLE] Avoid: [NEG]
- `S021.png`
A long period American sedan parked at a kerb outside base family housing in the late 1970s, chrome bumper dulled by salt air, vinyl roof, a child's chalk line faded on the concrete beside it, afternoon light flat and humid, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP arriving_family — 2 — S017, S040**
```
- `S017.png`
Two anonymised adults carrying cardboard cartons along a concrete walkway toward base family quarters, seen from well behind and at a distance so no face can read, a duffel bag propped against a stoop, humid morning light, period clothing of the middle 1970s, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S040.png`
An anonymised adult carrying two paper grocery sacks up the concrete walk to a base duplex, shot from directly behind at hip height so only the back and the sacks read, the storm door standing open ahead, late afternoon shadows long across the grass, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **laundry_line — 1 — S018 ／ ★HP laundry_hands — 1 — S019**
```
- `S018.png`
Bed sheets pegged along a clothesline between two base quarters, bellying and snapping in a coastal wind, the light coming through the cotton so the whole frame glows white against the brick, a wicker basket tipped on the grass, no people, no readable text [STYLE] Avoid: [NEG]
- `S019.png`
An anonymised woman's hands pegging a sheet to a line, seen from behind and slightly below so the sheet fills most of the frame and her head is hidden entirely by the fabric, a peg bag hanging beside her wrist, wind moving everything, period 1970s clothing, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP screen_door_figure — 1 — S020**
```
- `S020.png`
An anonymised adult standing just inside a screen door seen from the porch outside, the mesh reducing the figure to a soft grey shape with no readable features, one hand on the frame, the yellow interior light behind turning the doorway into a warm rectangle in a blue dusk, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP mailbox_row — 1 — S022**
```
- `S022.png`
Three anonymised adults standing at a bank of communal metal mailboxes on a base housing street, all seen from behind at a distance, one reaching up to a high box, another turning away with envelopes, flat humid midday light, blank box doors with nothing readable, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **parade_deck — 1 — S023 ／ ★HP formation_legs — 1 — S024**
```
- `S023.png`
An enormous empty asphalt parade deck at dawn, freshly painted white alignment lines running away to a vanishing point, a low treeline at the far edge, mist still lying in the hollows, absolutely nobody on it, no signage, no readable text [STYLE] Avoid: [NEG]
- `S024.png`
Ranks of boots and trouser legs moving in step across wet asphalt, framed tightly from the knee down so no torso and no face enters the frame at all, plain unmarked utility trousers, the shadow of the formation stretching sideways in low sun, no insignia of any kind visible, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **barracks_and_tower — 2 — S025–S026**
```
- `S025.png`
A long plain barracks facade at dusk, a repeating grid of identical windows, most dark and a scattering lit, a concrete walkway and clipped hedge at its foot, utterly institutional, no signage or emblem anywhere on the building, no people, no readable text [STYLE] Avoid: [NEG]
- `S026.png`
A steel water tower rising over a pine treeline at midday, its tank pale and blank, ladder and railing sharp against a hot white sky, heat shimmer at the base of the legs, the whole plant of a base water system reduced to one object, no lettering on the tank, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_tap_by_day — 1 — S027 ／ ★HP filling_hands — 1 — S028**
```
- `S027.png`
A kitchen tap running steadily into a stainless sink in flat daylight, the stream twisting and catching a cold aqua highlight, a sponge and a bar of soap at the rim, a window above showing an ordinary lawn, entirely unremarkable, no person, no readable text [STYLE] Avoid: [NEG]
- `S028.png`
An anonymised adult's hands holding a plain glass under a running kitchen tap in daylight, framed from the wrists so nothing else of the person appears, the glass almost full, small bubbles clinging to its inside wall, a dish rack out of focus behind, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP dishes — 1 — S029**
```
- `S029.png`
An anonymised adult's hands stacking rinsed plates into a wire drying rack beside a kitchen window, shot from behind the shoulder so the head sits above the frame line, water still beading on the crockery, mid-morning light coming flat through net curtains, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **domestic_water — 3 — S030–S032**
```
- `S030.png`
A tiled bathroom in a base quarters filling with steam as a bath runs, small square 1970s tiles, a folded towel on the closed lid, the water surface trembling under the tap, nobody in the room at all, no person, no readable text [STYLE] Avoid: [NEG]
- `S031.png`
A garden hose thrown across a mown lawn with a fine arc of water hanging in late afternoon sun, droplets catching as hard points of light, a brick duplex wall behind in shadow, a sprinkler head lying on its side in the grass, no people, no readable text [STYLE] Avoid: [NEG]
- `S032.png`
Ice cubes crowding the top of a glass of water on a boomerang-pattern formica table, condensation running down the outside and pooling into a ring, a chrome table edge catching the window, high summer indoors, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_absent_child_as_object — 2 — S033–S034**（★人物なし・子どもは描かない）
```
- `S033.png`
A small tricycle standing perfectly still on a concrete walkway outside base quarters, its front wheel turned, one pedal at the top of its arc, the grass beyond needing cutting, late flat light and a long shadow, absolutely nobody in the frame, no readable text [STYLE] Avoid: [NEG]
- `S034.png`
An empty swing set on a patch of worn grass behind base housing, the chains moving very slightly in a coastal wind, the seats hanging level and unoccupied, a treeline of pines closing the background, overcast and still, absolutely nobody in the frame, no readable text [STYLE] Avoid: [NEG]
```
- **★HP porch_and_fence — 2 — S035, S037**
```
- `S035.png`
An anonymised adult sitting alone on a concrete porch step at dusk, elbows on knees and head lowered, seen from behind and to one side so no face reads, a screen door dark behind him, the street beyond emptying of light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S037.png`
Two anonymised adults standing on opposite sides of a low wire fence between back yards, talking, both framed from well behind and far enough that neither face can be read, laundry on a line to one side, the flat humid light of a Carolina afternoon, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **perimeter_and_ground — 2 — S036, S039**
```
- `S036.png`
A chain-link perimeter fence running straight across the frame with dense pine woods pressing up behind it, the mesh sharp in the foreground and the trees soft beyond, a mown strip of grass at its foot, no gate and no signage, no people, no readable text [STYLE] Avoid: [NEG]
- `S039.png`
The raw red-clay shoulder of a two-lane road cut through pine woods, the earth wet and rutted from a grader, weeds coming back at the edges, the asphalt running away to a shimmer, pine-and-clay dusk colour dominating, no people, no readable text [STYLE] Avoid: [NEG]
```
- **grey_water_and_verge — 2 — S038, S050**
```
- `S038.png`
A wide grey coastal inlet under flat overcast, the water absolutely still and holding no colour, a thin dark line of marsh and pine on the far side, a broken piling standing alone in the shallows, immense emptiness, no people, no readable text [STYLE] Avoid: [NEG]
- `S050.png`
Tall roadside grass and seed heads bending together in a steady wind, shot at ground level against a blown-out grey sky, everything moving in one direction, the blur of motion in the stems, no horizon detail, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_table — 2 — S041, S051**
```
- `S041.png`
A family dining table laid for a meal in a base quarters, four places set with mismatched crockery, one place with its chair still tucked in and its plate untouched, a jug of water in the middle catching the window, warm domestic light, no people, no readable text [STYLE] Avoid: [NEG]
- `S051.png`
A single kitchen chair pushed back at an angle from an empty table, the seat cushion still slightly compressed, a cup left on the far side, the room otherwise tidied and cold, one hard shaft of afternoon light across the floor, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP calendar_hand — 1 — S042**
```
- `S042.png`
An anonymised adult's hand lifting the corner of a wall calendar page beside a kitchen doorway, only the hand and forearm entering the frame, the grid of the month reduced to an unreadable grey texture, a pencil hanging on a string beside it, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP reading_at_the_table — 1 — S043**
```
- `S043.png`
An anonymised adult sitting alone at a kitchen table under a single low-hung lamp, head bent over papers so the face is entirely lost in shadow, one hand flat on the table edge, the rest of the room falling away into darkness, night outside the window, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **blinds_and_curtains — 2 — S044, S045**
```
- `S044.png`
Hard bars of light thrown by venetian blinds across a papered interior wall and a doorframe, the slats cutting the room into stripes, a hallway running off into darkness beyond, dust visible in the beams, no people, no readable text [STYLE] Avoid: [NEG]
- `S045.png`
The same row of low brick base quarters in a raw winter dusk, bare crape myrtles in the front strips, lights on in three windows, the sky drained to a hard steel grey and the brick gone cold, wet concrete underfoot, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP doorway_and_window — 2 — S046, S047**
```
- `S046.png`
An anonymised adult standing in a bedroom doorway with one hand on the frame, seen from inside the dark room so the figure reads only as a silhouette against the lit hallway behind, the bed in the foreground made and untouched, absolute stillness, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S047.png`
An anonymised adult's reflection held in a rain-streaked window pane, the figure soft and doubled and unreadable, the wet glass sharp in front and the grey yard beyond soft, the room behind dim, a hand raised near the frame, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP church_and_grass — 2 — S048, S049**
```
- `S048.png`
A handful of anonymised adults seated far apart in the back rows of a plain chapel, photographed from behind the rearmost pew so only shoulders and the backs of heads read, one high window putting a pale shaft down the aisle, everything else grey, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S049.png`
A scattering of anonymised adults in dark coats standing apart on wet winter grass, seen from a great distance so the figures are small and no face can read, bare trees behind, flat white sky, nothing else in the frame, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 2 — AUGUST 1997（34枚・S052–S085）
- **the_news_that_travelled — 3 — S052, S056, S058**（S058 は also_thumb）
```
- `S052.png`
A wood-veneer console television standing in a dark 1990s living room, the screen a featureless blue-white glow with nothing readable on it, a doily and a lamp on top, the carpet lit only by what the tube throws, no person, no readable text [STYLE] Avoid: [NEG]
- `S056.png`
A narrow domestic hallway photographed from its dark end, a doorway at the far side pulsing with the cold changing light of a television in another room, coats on hooks in silhouette, nobody in the corridor, no readable text [STYLE] Avoid: [NEG]
- `S058.png`
The cold moving light of a television thrown across the wall and cabinets of a dark kitchen, the set itself out of frame, the light finding a kettle and a row of mugs and the edge of a doorframe, an ordinary room receiving news, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_stillness — 2 — S053, S059**
```
- `S053.png`
An anonymised adult standing dead still in a dim room with the changing light of a television washing over one shoulder and the side of a jaw, the head turned so no face resolves, one arm hanging, the room otherwise unlit, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S059.png`
An anonymised adult sitting on the very edge of an armchair with elbows on knees and hands clasped, photographed squarely from behind so only the back and the set of the shoulders read, a lamp burning low beyond, absolute stillness, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **cold_food_and_night_room — 3 — S054, S055, S060**
```
- `S054.png`
A plate of food congealing on a side table beside an armchair, a fork abandoned across it, a folded newspaper under the plate with all print reduced to grey noise, one lamp low and warm, nobody in the room, no readable text [STYLE] Avoid: [NEG]
- `S055.png`
A television remote control lying on the worn upholstered arm of a chair, buttons rubbed blank, the fabric nap catching a single hard sidelight, the room around it entirely black, an object of ordinary evenings, no person, no readable text [STYLE] Avoid: [NEG]
- `S060.png`
A small kitchen at night lit by one bare bulb, two chairs pulled out from a table, a dish towel over the oven rail, everything ordinary and everything paused, deep shadow in the corners, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_first_notes — 2 — S057, S061**
```
- `S057.png`
An anonymised adult's hands flat either side of a blank ruled notepad on a kitchen table, a ballpoint uncapped beside them, nothing written yet, the paper the brightest thing in a dark room, framed from the elbows so no face appears, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S061.png`
An anonymised adult standing beside a wall-mounted telephone with the coiled cord looping down, cropped at the chest so no face reads, one hand resting on the receiver without lifting it, a kitchen doorway dark behind, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_call_and_the_keys — 2 — S062, S064**
```
- `S062.png`
An anonymised adult's hand lifting a heavy telephone handset off its cradle, shot tight so only the hand, the cuff and the instrument occupy the frame, the coiled cord swinging, a kitchen wall out of focus behind, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S064.png`
An anonymised adult's hands resting on the keys of a manual typewriter with a single sheet curled in the platen, framed from the wrists down, the typed lines an unreadable grey band, a desk lamp raking across the keys, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_letter_leaves — 2 — S063, S065**
```
- `S063.png`
A round institutional wall clock at night with its hands lost in shadow and its face reduced to a pale disc, the wall around it bare and dim, time present but unreadable, no people, no readable text [STYLE] Avoid: [NEG]
- `S065.png`
An envelope being pressed closed along its flap, macro, the paper fibres and the glue line sharp, no address and no marking of any kind on the face, a thumb edge just leaving the frame, cold desk light, no readable text [STYLE] Avoid: [NEG]
```
- **the_press_and_the_reel — 2 — S066, S070**
```
- `S066.png`
The rollers of a newspaper press running at speed, paper webbing through in a blur, the printed columns smeared into pure grey motion with nothing legible anywhere, ink light on steel, industrial and loud, no people, no readable text [STYLE] Avoid: [NEG]
- `S070.png`
The illuminated screen of a microfilm reader in an otherwise dark research room, the projected page a bright rectangle of unreadable grey, the crank and carriage in shadow, dust suspended in the projector beam, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_machinery_of_records — 3 — S067, S069, S075**
```
- `S067.png`
An empty institutional office corridor under a long run of fluorescent tubes, identical closed doors on both sides, buffed vinyl flooring throwing the light back, receding to a blank far wall, nobody in it, no signage, no readable text [STYLE] Avoid: [NEG]
- `S069.png`
The light bar of a photocopier travelling under a closed lid, a hard white line escaping around the seam of the platen, the machine's grey casing lit from within, a dark office beyond, no people, no readable text [STYLE] Avoid: [NEG]
- `S075.png`
A metal wastebasket beside a desk leg, crammed with crumpled paper and overflowing onto the carpet tile, the crumples catching one low raking light, nothing legible on any sheet, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_drawer_and_the_stack — 2 — S068, S071**
```
- `S068.png`
An anonymised adult's hand pulling open the drawer of a battered steel filing cabinet, framed so only the forearm and the loaded folders read, the folder tabs blank and pale, fluorescent light flat and unkind, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S071.png`
A tall stack of loose paper on a desk in the foreground, sharp, with an anonymised adult sitting well behind it thrown completely out of focus, the paper edges catching lamplight, the person reduced to a shape, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_binder_is_born — 2 — S072–S073**
```
- `S072.png`
An empty three-ring binder lying open on a kitchen table, rings sprung and bare, one pale untouched sheet slid into the first pocket, a lamp throwing a hard ellipse on the vinyl cover, the beginning of an archive, no person, no readable text [STYLE] Avoid: [NEG]
- `S073.png`
Macro along a row of coloured index tabs standing proud of a binder's pages, every label blank, the plastic edges catching light in a receding line, depth falling off fast, an archive learning to divide itself, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_lamp_and_the_pen — 2 — S074, S082**
```
- `S074.png`
An anonymised adult's hand and forearm reaching in to switch on a gooseneck desk lamp at night, the bulb blooming as it lights, the desk beneath suddenly readable as texture only, everything above the elbow out of frame, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S082.png`
An anonymised adult's hand writing steadily down a ruled page, macro, the pen nib and the knuckles sharp, the script itself an unreadable running grey line, the page lit hard from one side, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_correspondence — 2 — S076, S078**
```
- `S076.png`
A rubber stamp pressed down onto a sheet of paper, macro from a low angle, the wooden handle and the ink pad beside it, the impression itself a solid unreadable smudge, an official gesture with no legible content, no person, no readable text [STYLE] Avoid: [NEG]
- `S078.png`
The broad shallow steps of a mid-century federal office building under flat grey daylight, brass handrails dulled, plate-glass doors giving back the sky, no signage anywhere on the facade, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP waiting_and_the_flag — 2 — S077, S079**
```
- `S077.png`
An anonymised adult's hand raising the red flag on a rural roadside mailbox, cropped at the sleeve, the box door shut on whatever went in, a gravel drive and pine woods soft behind, morning light low and cold, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S079.png`
An anonymised adult sitting alone on a bench in a long government corridor, photographed from far down the hall so the figure is small and unresolvable, a folder on the knee, identical doors marching away on both sides, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_counter_and_the_boxes — 2 — S080, S081**
```
- `S080.png`
A public service counter closed for the day, a bell on the laminate top and a shuttered window behind it, a clock high on the wall with unreadable hands, chairs stacked against the far side, nobody there, no readable text [STYLE] Avoid: [NEG]
- `S081.png`
Cardboard records cartons stacked shoulder-high along both sides of a narrow corridor, lids ill-fitting, hand-written box labels reduced to grey scribble, a strip light overhead, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_map_table — 1 — S083**
```
- `S083.png`
Two anonymised adults leaning over a large paper map spread on a table, both photographed from behind and above so only backs and shoulders and pointing hands appear, the map's contours and labels an unreadable grey wash, one low lamp, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_workbench — 1 — S084 ／ ★HP the_night_porch — 1 — S085**
```
- `S084.png`
A garage workbench under a caged bulb, loose papers weighted flat by a wrench and a coffee can of screws, sawdust in the grain, the roll-up door black behind, a working man's second office, no people, no readable text [STYLE] Avoid: [NEG]
- `S085.png`
An anonymised adult standing on a night porch beneath a single bulb with moths turning around it, seen from behind and below so the head is against the dark, one hand on a railing, the yard beyond entirely black, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 3 — WHAT THE LAB WROTE（40枚・S086–S125）
- **the_blank_form — 1 — S086 ／ ★HP the_samples — 1 — S087**
```
- `S086.png`
A blank carbon-copy analytical result form clipped to a metal clipboard on a laboratory bench, the printed grid crisp but every word and heading dissolved into an unreadable smear, a pen laid across it, cold bench light, no person, no readable text [STYLE] Avoid: [NEG]
- `S087.png`
An anonymised technician's gloved hands settling glass sample bottles into the slots of a wooden field crate, framed from the forearms, the bottles capped and unlabelled, condensation beading the glass, a tailgate and grass out of focus behind, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_bench — 3 — S088, S089, S090**
```
- `S088.png`
A single drop falling from a glass pipette into a narrow vial, caught mid-air, the meniscus below trembling, everything else in the frame dark, refraction throwing a cold aqua highlight through the glass, clinical and precise, no person, no readable text [STYLE] Avoid: [NEG]
- `S089.png`
A laboratory bench photographed at night with nobody present, retort stands and racked glassware in silhouette, one instrument's pilot lamp burning, stools pushed under, the room holding its breath, no people, no readable text [STYLE] Avoid: [NEG]
- `S090.png`
A chart recorder pen drawing a jagged trace across a slowly rolling paper drum, macro, the ink line glossy and wet, the drum's ruling reduced to unreadable grey, the mechanism's brass gearing catching light, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_dial — 1 — S091**
```
- `S091.png`
An anonymised technician's fingers turning a knurled dial on a heavy analytical instrument, framed tight on the hand and the instrument face so no person reads, the meter needle swinging, the panel's markings an unreadable smear, cold light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_dry_cleaner — 2 — S092, S094 ／ ★HP the_conveyor — 1 — S093**
```
- `S092.png`
A small dry cleaner's shopfront at dusk on a two-lane road, plate glass fogged from within, a hand-lettered board in the window reduced to an unreadable grey block, a strip of cracked asphalt in front, period American storefront, no people, no readable text [STYLE] Avoid: [NEG]
- `S093.png`
An anonymised worker seen from behind operating a garment conveyor in a small cleaning plant, plastic-sheathed clothes swinging past on the rail, the figure cropped at the shoulders and lost among the hanging shapes, humid interior light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S094.png`
A commercial steam press opening and releasing a hard white cloud into a low-ceilinged workroom, the cloud lit from one side, the machine's scorched padding visible beneath, nobody in frame, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_valve — 1 — S095 ／ the_pipework — 1 — S096**
```
- `S095.png`
An anonymised worker's gloved hands closing on the spokes of a large rusted valve wheel on an outdoor pipe run, framed from the forearms only, flakes of ochre paint lifting under the grip, the pipe disappearing into grass, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S096.png`
A junction of heavy industrial pipework painted a chipped ochre, elbows and flanges bolted together, a pressure gauge with an unreadable face, the whole assembly standing in weeds against a blank concrete wall, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_pump_house — 1 — S097 ／ the_well_states — 2 — S098, S109**
```
- `S097.png`
An anonymised figure standing far off in the open doorway of a small brick pump house set in long grass, too distant to resolve, the machinery inside a black rectangle, a worn path leading to the door, humid overcast, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S098.png`
A capped steel well head standing alone in a field of long grass, its flange bolted shut and its paint blistered, no pipework running from it any more, pines closing the horizon, flat grey light, no people, no readable text [STYLE] Avoid: [NEG]
- `S109.png`
A heavy padlock and chain drawn through the gate of a small fenced well compound, the hasp swinging shut, the enclosure behind holding one silent capped pipe, weeds through the mesh, cold overcast, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_storage_and_the_drums — 3 — S099, S100, S101**（solvent-drum ochre はここ）
```
- `S099.png`
The riveted seam of a large steel storage tank filling the frame, the ochre paint blistered and streaked with run-off, a weld line running vertically through the middle, rust bleeding from the fixings, no people, no readable text [STYLE] Avoid: [NEG]
- `S100.png`
A single rusted steel drum lying on its side in long grass at the edge of a service yard, its lid gone and its rim eaten through, ochre paint surviving in patches, the grass around it dying back in a ring, no people, no readable text [STYLE] Avoid: [NEG]
- `S101.png`
A row of industrial drums standing on a cracked concrete apron behind a maintenance shop, some upright and some tipped, ochre and grey, a puddle spreading between them and catching the sky, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_ground_takes_it — 2 — S102 ／ ★HP the_soil_sample — 1 — S103**
```
- `S102.png`
A drain grate set into wet concrete behind a commercial building, water sliding across the slab and disappearing between the bars, an iridescent film riding the surface, the loading door shut above, no people, no readable text [STYLE] Avoid: [NEG]
- `S103.png`
An anonymised worker's hands lowering a soil auger into a narrow trench, framed from the forearms, the cut face of the trench showing pale sand over red clay in clean bands, spoil heaped beside it, flat field light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★THE MID REVEAL — the_form_written — 1 — S104（also_thumb） ／ ★HP the_margin — 1 — S105 ／ the_carbon — 1 — S106**
```
- `S104.png`
A carbon-copy analytical result form on a metal clipboard beneath a single desk lamp at night, the printed grid receding into shadow, one handwritten line running across the remarks box as an unreadable urgent scrawl, a pen thrown down beside it, the whole frame built around a piece of paper, no person, no readable text [STYLE] Avoid: [NEG]
- `S105.png`
An anonymised hand pressing a ballpoint hard into the margin of a printed form, extreme macro so only fingertips, pen and paper fill the frame, the writing digging a visible groove, the letters themselves an unreadable smear, hard raking light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S106.png`
A sheet of purple carbon paper being lifted away from the copy beneath it, macro, the transferred marks showing as soft violet ghosts with nothing legible, the two sheets separating in a slow peel, cold light through the paper, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_meter — 1 — S107 ／ ★HP the_switch — 1 — S108**
```
- `S107.png`
A brass water meter dial set flush in a concrete pit, its glass fogged and its numerals reduced to an unreadable ring, wet leaves pushed into the pit around it, the lid lying open on the grass beside, no people, no readable text [STYLE] Avoid: [NEG]
- `S108.png`
An anonymised hand resting on a heavy bakelite toggle on an old control panel, framed tight so only the hand and the panel appear, rows of unmarked indicator lamps beside it, the metal fascia scratched and dulled, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_tap_closes — 1 — S110 ／ ★HP the_untouched_glass — 1 — S111**
```
- `S110.png`
A kitchen tap turned hard off above a completely dry stainless sink, one last bead hanging from the spout without falling, the plug chain still, the window above showing a grey afternoon, an ordinary appliance made final, no person, no readable text [STYLE] Avoid: [NEG]
- `S111.png`
A full glass of water standing untouched on a counter with an anonymised adult standing beside it, cropped at chest height so no face appears, the hand near the glass but not taking it, the room's light cold and even, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_form_is_filed — 2 — S112, S116**
```
- `S112.png`
A single form sliding down into a manila folder, macro at the folder's mouth, the paper's edge bowing as it goes, the tab above blank, a desk surface and a sleeve of other folders beyond, cold office light, no person, no readable text [STYLE] Avoid: [NEG]
- `S116.png`
A run of grey archive boxes on steel shelving with one box pulled half out, its lid askew and its packed file edges showing as a dense pale block, the shelf label holders empty, a fluorescent tube overhead, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_office_machine — 3 — S113, S115, S117**
```
- `S113.png`
An anonymised adult's hand laying a sheet into a stacked wire in-tray on a government desk, framed at the wrist, the out-tray beside it already loaded, a rubber stamp and an ink pad in the corner, flat fluorescent light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S115.png`
Two anonymised adults standing in an office doorway mid-conversation, both photographed from well down the corridor and slightly behind so neither face resolves, one holding a folder against the chest, a strip light directly overhead, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S117.png`
An anonymised figure pushing a loaded records trolley away down a long institutional corridor, seen from behind at distance, boxes stacked above the handle, the corridor's perspective swallowing them, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_pinned_memo — 1 — S114 ／ the_shut_doors — 1 — S118 ／ ★HP the_far_figure — 1 — S119**
```
- `S114.png`
A single typed memo pinned to a cork board by one brass drawing pin, curling at the corners, the type reduced to a grey band, other pin holes scattered around it from documents long gone, side light, no people, no readable text [STYLE] Avoid: [NEG]
- `S118.png`
A corridor of identical closed office doors receding into darkness, each with a blank plate where a name would go, the floor waxed and reflecting the ceiling lights back in a doubled line, nobody anywhere, no readable text [STYLE] Avoid: [NEG]
- `S119.png`
An anonymised adult standing alone at the far end of a long fluorescent-lit corridor, tiny in the frame and completely unresolvable, hands at the sides, the perspective lines of the ceiling driving toward the figure, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_land — 3 — S120, S121, S122**
```
- `S120.png`
A large survey map spread across a table under a low hanging lamp, contour lines and hatching visible as pattern only with every label an unreadable smear, a straight edge and a pair of dividers lying across it, deep shadow beyond the lamp's reach, no people, no readable text [STYLE] Avoid: [NEG]
- `S121.png`
A high aerial view of a flat coastal plain, a river system branching across it in dull silver, pine blocks and cleared rectangles alternating to the horizon, thin haze softening the far distance, no people, no readable text [STYLE] Avoid: [NEG]
- `S122.png`
An aerial of a wide tidal estuary at low water, the channel cutting a dark S through pale exposed flats, marsh grass in blocks along the edges, a single line of pine on the far bank, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_survey_crew — 1 — S123 ／ the_hydrant — 1 — S124 ／ ★HP the_empty_meeting — 1 — S125**
```
- `S123.png`
Two anonymised figures far out in an open field beside a tripod-mounted instrument, so distant that they read as marks against the treeline, long shadows behind them, an equipment case open in the grass, flat afternoon light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S124.png`
A squat fire hydrant standing on a grass verge beside a kerb, its paint chalked and its caps chained, the grass around it neatly mown, a blank residential street receding out of focus, overcast, no people, no readable text [STYLE] Avoid: [NEG]
- `S125.png`
An anonymised adult sitting alone at the far end of an emptied meeting room with all the other chairs pushed neatly in, photographed from the doorway so the figure is small and turned away, a jug and tumblers untouched on the table, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 4 — THE MAN BORN ON THE BASE（40枚・S126–S165）
- **the_place_he_began — 2 — S126, S129 ／ ★HP the_waiting_row — 1 — S127 ／ the_far_corridor — 1 — S128**
```
- `S126.png`
A low mid-century naval hospital block seen from across a lawn at dusk, its window bands lit in an even grid, a service road curving past, no signage or emblem anywhere on the building, pines closing the sky behind, no people, no readable text [STYLE] Avoid: [NEG]
- `S127.png`
An anonymised adult sitting alone at one end of a long row of moulded plastic waiting chairs, photographed from the far end of the row so the figure is small and turned toward the wall, a magazine table untouched, cold overhead light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S128.png`
A long institutional corridor seen from its dark end with morning light coming in through one distant window and lying in a pale rectangle on the floor, doors closed all the way along, absolutely nothing else in the frame, no people, no readable text [STYLE] Avoid: [NEG]
- `S129.png`
A shelf of heavy bound ledgers with cracked spines and no legible lettering, packed tight and pushed to the back of a wooden case, a gap where one volume has been taken out, dust along the top edge, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_ordinary_life — 1 — S130 ／ ★HP the_night_desk — 1 — S131 ／ the_screen — 2 — S132, S133**
```
- `S130.png`
A quiet residential street of low ranch houses in the early 2000s, sprinklers off, a basketball hoop over a garage, the asphalt pale in flat afternoon sun, palms and live oak at the ends of the drives, no people, no readable text [STYLE] Avoid: [NEG]
- `S131.png`
An anonymised adult seated at a cluttered home-office desk at night with his back to the camera, the monitor's glow outlining his shoulders and the edge of an ear, papers fanned around the keyboard, the rest of the room black, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S132.png`
A boxy computer monitor alone in a dark room showing a single blinking cursor in the corner of an otherwise empty field of light, the phosphor glow spilling onto a desk edge and a coffee mug, nothing readable anywhere on the screen, no person, no readable text [STYLE] Avoid: [NEG]
- `S133.png`
The status lamps of a desktop modem blinking in near-darkness, macro, the plastic case reflecting nothing else, a tangle of cable running out of focus behind, the only light in a sleeping house, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_list_being_built — 2 — S134, S136 ／ ★HP the_cards — 1 — S135**
```
- `S134.png`
Coloured map pins pushed into a large cork board, clustering thickly in one region and scattering elsewhere, the map beneath reduced to unreadable pale shapes, pin shadows raking across it under a desk lamp, no people, no readable text [STYLE] Avoid: [NEG]
- `S135.png`
An anonymised adult's hands laying index cards out in rows across a dining table, framed from the wrists, dozens already down and more in the left hand, every card's writing an unreadable grey scribble, one warm overhead light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S136.png`
A domestic shelf carrying a solid run of identical thick ring binders, spines out and all labels blank, the row bowing the shelf slightly in the middle, a stepladder edge at the frame's border, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_long_calls — 2 — S137, S138**
```
- `S137.png`
An anonymised adult's hand gripping and twisting a coiled telephone cord, macro, the knuckles pale and the cord stretched into a tight helix, a kitchen wall out of focus behind, nothing else in the frame, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S138.png`
An anonymised adult standing at a window at night with a cordless handset to one ear, rendered as a flat silhouette against the glass with the street lights beyond, one shoulder against the frame, no facial detail at all, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_hearing_room — 4 — S139, S140, S141, S142**
```
- `S139.png`
A long committee table in an empty hearing room, chairs squared behind it, a run of unplugged microphone stems down its length, the surface polished and holding the ceiling lights, pale record-daylight from tall windows, no people, no readable text [STYLE] Avoid: [NEG]
- `S140.png`
A single gooseneck microphone standing on a witness table, macro from below so the head fills the upper frame, a folded card base with no legible marking, the room beyond thrown soft, cool even light, no person, no readable text [STYLE] Avoid: [NEG]
- `S141.png`
A water carafe and two inverted tumblers standing on a coaster at a witness table, the glass throwing a cold aqua highlight, a legal pad squared beside them with a blank top sheet, pale window light, no person, no readable text [STYLE] Avoid: [NEG]
- `S142.png`
A wood-panelled committee hall photographed empty from the rear, the raised dais curving across the far end, brass fittings dull, the room's whole width lit by one bank of tall windows, nobody in any seat, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_gallery_and_the_hands — 2 — S143, S144**
```
- `S143.png`
Rows of anonymised adults seated in a hearing gallery photographed from the very back, only shoulders and the backs of heads showing, a few grey heads among them, everyone facing the same way and completely still, pale record-daylight, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S144.png`
An anonymised adult's hands folded on a witness table beside the closed cover of a thick binder, framed from the forearms so no face appears, one thumb pressed over the other, the wood grain and the vinyl cover both catching the same cold light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_capital — 2 — S145, S146 ／ ★HP the_press_line — 1 — S147**
```
- `S145.png`
A capitol dome standing pale against a deep dusk sky, floodlit from below, bare branches crossing the lower frame, the plaza in front emptied and blue, a monumental building at the end of a working day, no people, no readable text [STYLE] Avoid: [NEG]
- `S146.png`
An empty marble government corridor with a vaulted ceiling and a receding line of pendant lamps, the polished floor doubling everything, heavy doors shut on both sides, no signage of any kind, no people, no readable text [STYLE] Avoid: [NEG]
- `S147.png`
A tight row of press cameras and shoulders along a rope line, framed from behind and cropped above the shoulders so no face appears, lenses raised in a jagged line, a hearing-room doorway bright beyond them, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_report_and_its_withdrawal — 3 — S148, S149, S150**
```
- `S148.png`
A thick spiral-bound report lying closed on a bare table, its cover a plain pale stock with all lettering dissolved into a grey smear, the wire binding catching a single hard light, nothing else on the table at all, no person, no readable text [STYLE] Avoid: [NEG]
- `S149.png`
A bound report being pushed back into a gap on a shelf between other volumes, macro at the spine, the gap closing, the surrounding spines uniform and blank, the shelf's shadow swallowing it, no person, no readable text [STYLE] Avoid: [NEG]
- `S150.png`
A released page with three heavy black redaction bars laid across it, macro at a steep angle, the surviving text between them reduced to an unreadable grey, the paper's photocopy grain visible, cold light from one side, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_data — 2 — S151, S155 ／ ★HP the_sorting — 1 — S152 ／ the_glassware — 1 — S153**
```
- `S151.png`
Continuous fanfold printout paper spilling from a printer and concertinaing onto the floor, the perforated edges sharp, the printed columns reduced to grey banding with nothing legible, an office at night behind, no people, no readable text [STYLE] Avoid: [NEG]
- `S152.png`
An anonymised researcher's hands squaring a thick sheaf of printout sheets against a desk, framed from the forearms, the pages fanning and settling, a highlighter and a ruler beside them, cold overhead light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S153.png`
A rack of clean laboratory glassware standing in flat daylight on a white bench, flasks and cylinders empty and dry, their curves throwing cold aqua refractions onto the surface, an unlit window beyond, no people, no readable text [STYLE] Avoid: [NEG]
- `S155.png`
A data screen filled with dense scrolling rows of figures reduced entirely to unreadable grey banding, the monitor bezel dark, a reflected ceiling light riding across the glass, an analyst's chair empty in front, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_rooms_where_it_was_told — 3 — S154, S156, S157**
```
- `S154.png`
An anonymised adult standing at a lectern seen entirely from behind, shoulders squared, facing a shallow arc of mostly empty seating, one hand resting on the lectern edge, a projector beam crossing above, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S156.png`
A veterans' hall interior with anonymised adults seated at long tables, all photographed from behind, plain unmarked flags on stands along the wall, folding chairs, coffee urns on a side table, warm low light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S157.png`
A town-hall meeting room half filled with anonymised adults on folding chairs, shot from the very back so every face is turned away, coats over chair backs, a bare microphone stand at the front, harsh ceiling light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_road_years — 3 — S158, S160 ／ ★HP the_parked_car — 1 — S159**
```
- `S158.png`
A half-empty parking lot at dusk with a scatter of cars, light standards just coming on and pooling orange on the asphalt, a low commercial block behind, the sky drained, no people, no readable text [STYLE] Avoid: [NEG]
- `S159.png`
An anonymised adult sitting alone in a parked car at night seen through the windscreen from outside, the face entirely lost in shadow behind the reflected street, hands on the wheel, papers on the passenger seat, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S160.png`
An interstate at night photographed from an overpass with a long exposure, tail lights drawn into continuous red ribbons and headlights into white, the road disappearing into the dark, the sky a flat starless grey, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_kitchen_archive — 1 — S161 ／ the_frames — 1 — S162 ／ ★HP the_names — 1 — S163 ／ the_stack — 1 — S164 ／ ★HP the_reflection — 1 — S165**
```
- `S161.png`
An anonymised adult's hand flattening a curled page among dozens of documents spread edge to edge across a kitchen table, framed from the elbow, every sheet's content an unreadable grey, one low pendant lamp above, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S162.png`
A domestic wall crowded with picture frames of every size, every photograph inside them thrown so far out of focus that no image or face can be made out, the glass catching a window, the arrangement grown over years, no readable text [STYLE] Avoid: [NEG]
- `S163.png`
An anonymised adult's finger running down a long printed list held flat on a table, macro, the entries reduced to an unreadable grey column, the paper's fold lines standing up, the finger stopping partway, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S164.png`
A stack of paper grown to an unstable tower on the corner of a desk, leaning slightly, more sheaves wedged in sideways, the edges catching a single lamp, the desk beneath long since invisible, no people, no readable text [STYLE] Avoid: [NEG]
- `S165.png`
An anonymised adult's reflection standing in a darkened window at dusk with the lit room repeated behind it, the figure doubled and softened past recognition, one hand up near the glass, the street outside almost gone, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 5 — THE TWO-YEAR WINDOW（30枚・S166–S195）
- **★HP the_steps — 1 — S166 ／ ★HP the_signature — 1 — S167 ／ the_podium — 1 — S168**
```
- `S166.png`
A scatter of anonymised adults standing and walking on broad capitol steps in flat daylight, all far enough away and turned enough that no face reads, coats and folders, the balustrade running across the lower frame, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S167.png`
An anonymised hand drawing a heavy pen across the signature line of a document, extreme macro so only the pen, the fingers and the paper appear, the printed text above reduced to an unreadable band, pale record-daylight, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S168.png`
An empty lectern with a plain unmarked flag on a stand beside it, photographed wide from the back of a bare hall, a single microphone and a glass of water on the top, the seating in front all vacant, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_queue — 1 — S169 ／ the_courthouse — 1 — S170 ／ ★HP the_empty_court — 1 — S171 ／ ★HP the_bench_wait — 1 — S172**
```
- `S169.png`
A line of anonymised adults waiting along the outside wall of a government office, all photographed from behind at a shallow angle so no face can resolve, folders and envelopes held against chests, morning shadow along the pavement, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S170.png`
A federal courthouse exterior in flat grey light, heavy stone piers and deep-set doors, wide steps worn hollow at the centre, an empty flagpole, no signage legible anywhere on the facade, no people, no readable text [STYLE] Avoid: [NEG]
- `S171.png`
An anonymised adult seated alone in the public rows of an otherwise empty courtroom, photographed from behind and above so only the back of a head and shoulders show, the bench and counsel tables vacant beyond, cool even light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S172.png`
An anonymised adult sitting on a wooden bench in a courthouse corridor with a folder across the knees, photographed from far along the corridor so the figure is small and faceless, marble and shut doors, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_volume — 2 — S173, S175 ／ ★HP the_clerk — 1 — S174 ／ ★HP the_kitchen_form — 1 — S176**
```
- `S173.png`
The pages of a thick docket turning rapidly under an unseen hand, motion blurring the print into pure grey, the block of paper visibly enormous, a desk edge and a lamp beyond, no person, no readable text [STYLE] Avoid: [NEG]
- `S174.png`
An anonymised clerk's hands squaring a tall stack of identical claim forms on a counter, framed from the forearms, the stack rising above the wrists, more stacks waiting behind it out of focus, hard overhead light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S175.png`
Mail sorting trays overflowing with envelopes on a steel rack, tray after tray receding, the addresses reduced to grey noise, a strap of rubber bands hanging from the frame, institutional light, no people, no readable text [STYLE] Avoid: [NEG]
- `S176.png`
An anonymised adult's hands filling in a printed form at a kitchen table, framed from the wrists, a reading magnifier and a cup pushed to one side, the form's boxes and instructions an unreadable smear, warm lamp light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_advertising_hours — 1 — S177 ／ ★HP the_sleeper — 1 — S178 ／ ★HP the_law_corridor — 1 — S179**
```
- `S177.png`
A television playing to an empty room deep in the night, the screen a saturated blur with nothing readable on it, the light hitting a recliner and a side table with a cold glass on it, curtains drawn, no person, no readable text [STYLE] Avoid: [NEG]
- `S178.png`
An anonymised adult asleep in a recliner with the television still on, the head fallen sideways and away from camera so no face reads, a blanket slipped to the floor, the screen's changing light washing the room, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S179.png`
An anonymised figure standing at the far end of a law-office corridor at night, small and unresolvable, glass-walled rooms on both sides with their lamps still burning, carpet swallowing the sound, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_money — 1 — S180 ／ ★HP the_envelope — 1 — S181 ／ the_calendar — 1 — S182**
```
- `S180.png`
A chequebook lying open on a desk beside a capped pen, the stub column blank and the numerals dissolved, a coffee ring on the blotter beside it, one lamp low and warm, nothing else on the desk, no person, no readable text [STYLE] Avoid: [NEG]
- `S181.png`
An anonymised adult's hands opening a windowed envelope at a kitchen table, framed from the forearms, the folded sheet half withdrawn with all print an unreadable grey, the discarded envelope beside a cup, morning light flat, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S182.png`
A wall calendar with a torn-away page hanging by one corner and the next month exposed beneath, the grid legible only as pattern, a thumb tack and a shadow, a bare kitchen wall around it, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_waiting_bodies — 3 — S183, S185 ／ the_window — 1 — S184**
```
- `S183.png`
An anonymised older adult standing at a window with one hand on a walking stick and the other on the frame, rendered as a silhouette against a pale evening, shoulders slightly stooped, the room behind unlit, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S184.png`
A single lit window of a low care residence seen from the lawn outside in the evening, the curtain half drawn and the room beyond showing only a lamp and a chair back, hedges dark in the foreground, nobody visible, no readable text [STYLE] Avoid: [NEG]
- `S185.png`
An anonymised older adult's hands resting on the worn wooden arms of a chair, extreme macro, veins and knuckles and a loose wedding band sharp, the upholstery nap catching a low side light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_archive_arrives — 1 — S186（also_thumb） ／ ★HP the_room — 1 — S187 ／ the_files — 1 — S188**
```
- `S186.png`
A thick tabbed ring binder standing upright on a hearing-room table beside a glass of water, the tabs blank and the cover scuffed from years of handling, pale record-daylight from a tall window, the room beyond soft and empty, no person, no readable text [STYLE] Avoid: [NEG]
- `S187.png`
A hearing room seen from the back with anonymised adults seated through the middle rows, every head turned forward and away, pale record-daylight falling across shoulders, the front of the room out of focus, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S188.png`
A tower of bound case files stacked on a courtroom counsel table, redweld folders and boxes wedged together, every spine label an unreadable smear, the stack tall enough to hide the chair behind it, cool light, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP the_corridor_talk — 1 — S189 ／ ★HP the_deposition — 1 — S190 ／ ★HP the_folder_wait — 1 — S191 ／ ★HP the_steps_group — 1 — S192**
```
- `S189.png`
Two anonymised adults standing apart in a courthouse corridor mid-conversation, both turned away from the lens, one leaning against the marble wainscot and the other holding a briefcase, the corridor long and bright behind them, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S190.png`
An anonymised adult sitting alone at the end of a long deposition table with the chair beside them empty, photographed from the opposite end so the figure is small and turned away, a recorder and a water jug on the surface, pale walls, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S191.png`
An anonymised adult waiting on a corridor bench with a thick folder held upright on the knees like a shield, seen at a distance and from behind one shoulder, the corridor's window light falling short of them, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S192.png`
A small group of anonymised adults standing together at the top of courthouse steps with their backs to the camera, looking out at a grey street, coats and folders, the stone balustrade framing them, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_losses — 2 — S193, S194 ／ ★HP the_closed_binder — 1 — S195**
```
- `S193.png`
A flag hanging at half height on a plain pole against an overcast sky, photographed from far enough that no device or marking on the fabric can be made out, the halyard slack, bare ground below, no people, no readable text [STYLE] Avoid: [NEG]
- `S194.png`
A wide flat memorial lawn photographed from a great distance in flat grey light, rows of small pale markers reduced to a repeating texture with nothing legible on any of them, a treeline closing the far edge, no people, no readable text [STYLE] Avoid: [NEG]
- `S195.png`
An anonymised adult's hand resting flat on the closed cover of a heavily used ring binder, framed at the wrist, the vinyl cracked at the corners and the tabs blank, a table edge and a cold window beyond, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 6 — ENDING（15枚・S196–S210）
- **the_kitchen_at_dawn — 2 — S196, S208**
```
- `S196.png`
A small kitchen at first light with everything put away, the counters bare and wiped, a chair squared to the table, the window over the sink going from blue to grey, absolute quiet, no people, no readable text [STYLE] Avoid: [NEG]
- `S208.png`
An empty kitchen chair standing squarely at a bare table in dawn light, the seat worn pale in the middle from years of use, one long shadow reaching away from it across the floor, nobody in the room, no readable text [STYLE] Avoid: [NEG]
```
- **the_glass_and_the_tap_resolved — 3 — S197, S198, S207**
```
- `S197.png`
An empty drinking glass standing alone on a table in first light, dry inside, a faint ring on the wood where it has stood many times, the window beyond a pale rectangle, the object that began the film returned emptied, no person, no readable text [STYLE] Avoid: [NEG]
- `S198.png`
A kitchen tap with a single drop gathering slowly at the lip of the spout and not yet falling, macro, the metal cold and the sink below dry, the whole frame held on one bead of water, no person, no readable text [STYLE] Avoid: [NEG]
- `S207.png`
A plain drinking glass photographed backlit and empty against a pale dawn window, the glass throwing a thin cold aqua edge, dust visible in the air around it, the counter beneath in shadow, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_archive_closes — 2 — S199, S204 ／ ★HP the_hands_closing — 1 — S204**
```
- `S199.png`
A long row of thick ring binders on a domestic shelf photographed straight on in dawn light, spines uniform and unlabelled, decades of the same work standing shoulder to shoulder, the shelf bowed slightly, no people, no readable text [STYLE] Avoid: [NEG]
- `S204.png`
An anonymised adult's hands bringing the cover of a thick binder down and closed on a kitchen table, framed from the forearms, the rings clicking shut, first light across the vinyl, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_last_figures — 2 — S200, S209**
```
- `S200.png`
An anonymised adult standing at a kitchen window at dawn with his back fully to the camera, one hand on the sill, the light outside just reaching the glass and rimming his shoulders, the room behind still dark, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S209.png`
An anonymised adult walking away down a concrete walkway between low buildings at dawn, small in the frame and receding, long shadow behind, nothing else moving anywhere in the shot, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_land_at_dawn — 3 — S201, S202, S203**
```
- `S201.png`
A pine treeline catching the first horizontal light of the day, the trunks separating out of the mass, mist lying in the rows between them, the sky above still colourless, no people, no readable text [STYLE] Avoid: [NEG]
- `S202.png`
A coastal marsh at dawn, the water absolutely unmoving and holding the whole sky, spartina standing in still ranks, a single channel running out toward a pale horizon, no people, no readable text [STYLE] Avoid: [NEG]
- `S203.png`
The same row of low brick family quarters photographed at dawn, dew on the grass, every window dark, the brick warming very slightly at the top course, the street beyond empty, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_unfinished — 3 — S205, S206, S210**
```
- `S205.png`
A wall calendar hanging undisturbed with an autumn month showing, the grid a pale pattern with nothing legible, one corner curled, a nail head and a hairline crack in the plaster beside it, low morning light, no people, no readable text [STYLE] Avoid: [NEG]
- `S206.png`
The heavy doors of a courthouse photographed closed at dawn, brass handles cold, the steps empty and wet, the stone still holding the night, nothing open yet, no signage legible, no people, no readable text [STYLE] Avoid: [NEG]
- `S210.png`
Absolutely still water running out to a flat grey horizon with no land and no boat anywhere in it, the surface holding a single band of early light, the frame divided almost exactly in half, no people, no readable text [STYLE] Avoid: [NEG]
```

## 5.7 幕別 motif 枚数の検算（★Codex は書き終えたら足して確認）

```
ACT0  : 2+2+2+2+2+1+4 = 15                                  （S001–S015）
ACT1  : 2+2+1+1+1+1+1+1+2+1+1+3+2+2+2+2+1+1+2+2+1+1+2+1 = 36 （S016–S051）
ACT2  : 3+2+3+2+2+2+2+3+2+2+2+2+2+2+1+1+1 = 34               （S052–S085）
ACT3  : 1+1+3+1+2+1+1+1+1+2+3+2+1+1+1+1+3+2+1+1+3+1+1+1+1+1+1+1 = 40 （S086–S125）
ACT4  : 2+1+1+1+1+2+2+2+1+2+4+2+2+1+3+2+1+1+2+1+1+1+1+1+1 = 40 （S126–S165）
ACT5  : 1+1+1+1+1+1+1+2+1+1+1+1+1+1+3+1+1+1+1+1+1+1+1+1+1+1+1+1+1 = 30 （S166–S195）
ACT6  : 2+3+2+2+3+3 = 15                                     （S196–S210）
合計   : 15+36+34+40+40+30+15 = 210 ✓
★human-present(★HP) body: 3(ACT0)+16(ACT1)+14(ACT2)+15(ACT3)+16(ACT4)+18(ACT5)+3(ACT6) = 85 / 210 = 40.5%（残り125は object/symbolic）
★HP の S番号（全85）:
  ACT0: S001, S004, S010
  ACT1: S017, S019, S020, S022, S024, S028, S029, S035, S037, S040, S042, S043, S046, S047, S048, S049
  ACT2: S053, S057, S059, S061, S062, S064, S068, S071, S074, S077, S079, S082, S083, S085
  ACT3: S087, S091, S093, S095, S097, S103, S105, S108, S111, S113, S115, S117, S119, S123, S125
  ACT4: S127, S131, S135, S137, S138, S143, S144, S147, S152, S154, S156, S157, S159, S161, S163, S165
  ACT5: S166, S167, S169, S171, S172, S174, S176, S178, S179, S181, S183, S185, S187, S189, S190, S191, S192, S195
  ACT6: S200, S204, S209
also_thumb 4枚 = S001 / S058 / S104 / S186（§4.3a と一字一致）
```
> **S001..S210 の連番が穴なく210行**そろっていることを `--only S001` の `shots=255`（210 body + 42 i2v種 + 3 thumb_face）で確認する。

## 5.8 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_lejeune_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.9 パーサ契約（`read_prompts()` はこの2行形式しか読まない）

```
- `S001.png`
<positive prompt> Avoid: <negative>
```
- **1行目:** `` - `S001.png` ``（バッククォート囲み・行末は `.png` の直後）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト
- `ai_prompts.v001.md` は **body 210行（S001..S210）＋ i2v 種 42行（M01_src..M42_src、§8.1a）＋ thumb_face 3行（T01_face..T03_face、§5.12）＝ 255 エントリ**を書く。すべて1枚生成。

## 5.10 生成コマンド（★variants 指定なし。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=255 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 58 --only S001
#   → ログ "episode=... shots=255 ... -> N images" の shots が 255 であること

# 全255枚（body 210 + i2v種 42 + thumb_face 3・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-058-lejeune
```
> QC で落ちたシーンの再生成は `--only S###`（同じプロンプトで別シードを1枚）。**基準を下げない・水増ししない。**

## 5.11 ★人物画像（匿名・ドラマ化スタンドイン）— HUMAN-FIGURE の style ＋ i2v 人物種18本

> **owner directive（EP48/49「空/寂しい」却下の恒久対策）: 匿名・非識別の人物を増やし、動かす。** 実在人物（Jerry Ensminger / Janey Ensminger / Mike Partain / その家族 / 議員 / 将官 / 基地司令官 / ATSDR・CDC 職員 / 弁護士 / 判事）の **likeness を作らない**。顔は非識別（背向き/影の横顔/逆光 silhouette/目から下クロップ/浅い被写界深度・**adults only**）。
> **★★本作固有の追加不変条件: 子どもを一切登場させない（健康な子どもも含む）。医療行為・医療機器を一切出さない。墓・棺・葬儀を出さない。実在の部隊章・エンブレム・階級章を出さない。**
> **★この `[HSTYLE]`/`[HNEG]` は (a) 18本の i2v 人物種、(b) §5.6 の ★HP body still 85枚、の両方に使う。**

### ★lane 定義（人物は動かす＝紙芝居にしない → H は motion レーンへ・locked counts 不変）

**H001–H018 は「新規の静止カット」ではなく、既存 42本の i2v 種のうち 18本の中身（＝人物ビート）として作る。additive にしない（象徴種を人物種に転換）。**
- **role = `i2v_source`**（body には回さない）。**42本の i2v 種のうち ★18本を人物ビート**に充て、残り **24本を抽象/象徴種**（§8.1a）。占有 M番号: **M01・M04・M06・M07・M10・M11・M13・M16・M17・M18・M21・M24・M25・M26・M27・M29・M31・M33 ＝ 18**。
- 各人物種は **Wan → RIFE（§8）で motion 化**され、**42本の motion のうち 18本**になり、**84 motion カットのうち最大 36カット**に出る＝**人物が動く**。
- **QC フラグ:** `has_human_body:true`（許可）・`has_identifiable_real_person:false`（必須）・`has_readable_text:false`（必須）・`has_child_depiction:false`（必須）・`has_medical_imagery:false`（必須）・`has_military_insignia:false`（必須）。
- **★locked counts は1つも変わらない:** still_body **210**（＝object 125 ＋ ★HP 85）/ still_i2v_source **42**（＝抽象 24 ＋ 人物 18）/ motion **42** / factory **235** / overlay **30** / thumb_face **3**；cuts **244/235/84 = 563**；still-share **0.4334**；first-use **0.8650**；avg-uses **1.156**。

**共通スタイル `[HSTYLE]`（各 ★HP / H プロンプト末尾に全文連結・匿名/非識別/photoreal）:**
```
, cinematic photoreal still, documentary reenactment stand-in, a generic anonymised adult who resembles no real individual, face kept non-identifiable — turned away, in profile lost to shadow, back-lit to a silhouette, cropped below the eyes, or thrown soft in shallow focus, humid Carolina coastal-plain light as the base register, a chlorinated tap-water aqua as the one recurring cool note wherever water taps glasses or pipes appear, pine-and-clay dusk only in exteriors, a pale record-daylight note only where the beat is a hearing room or a signing table, period-correct United States 1953 to 2026 with era-correct clothing, low-key soft-shadow lighting, telephoto compression, shallow depth of field, restrained dignified framing, adults only, plain unmarked clothing with no insignia of any kind, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no readable documents, no children, no medical equipment, no coffin and no memorial marker in shot
```
**共通ネガティブ `[HNEG]`（各 `Avoid:` の後に全文連結・匿名人体は許可、実在 likeness/子ども/医療/可読テキストは禁止）:**
```
recognizable real person, likeness of a specific person, Jerry Ensminger, Janey Ensminger, Mike Partain, any real senator or congressman, any real general or base commander, any real judge or government scientist, celebrity, mugshot, deepfake, text, words, letters, numbers, captions, watermark, logo, readable document, legible form, legible report, legible date, license plate, military insignia, unit patch, rank device, service emblem, readable base sign, child, children, toddler, baby, sick child, dying child, bald child, hospital bed, patient, IV drip, syringe, medical chart, x-ray, scan image, chemotherapy, oncology ward, examination room, operating theatre, doctor examining a person, nurse, coffin, casket, funeral, grave, headstone, mourner weeping, wounds, blood, gore, corpse, violence, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, evidence-blue bandana, interrogation green-gray, signage red, phosphor green, shop-lamp amber, milky haze, scanline
```

## 5.12 ★サムネ用 emotive-face 静止画（3枚・CTR §4A・thumb_face）

> **owner directive（CTR_PLAYBOOK §4A・emotive face が lane の #1 CTR driver）:** サムネは **単一の AI 生成・非実在・illustrative/dramatized な顔**を peak emotion で。**実在人物（Ensminger / Partain / 議員 / 判事）の likeness を作らない**＝clearly illustrative（semi-painterly, cinematic-render）にして実写に読ませない＝likeness firewall。**子どもの顔・病気の描写・医療機器を作らない。** これらは **本編カットに出ない thumbnail 専用**（role=thumb_face・public_path null・distinct/cuts に数えない・§3.1）。
> **★本作固有のパッケージング制約:** サムネは **法律事務所の広告に見えてはならない**（この案件名はテレビ広告で飽和している）。**ドル記号・金額・"CLAIM"/"COMPENSATION" の気配・電話番号風の要素・赤いバナーを一切置かない。** 夜のストーリーフレーム＋水＝広告レジスターを即座に破る。

**共通スタイル `[TSTYLE]`:**
```
, thumbnail key art, a single non-real dramatized generic human character rendered in a clearly illustrative semi-painterly cinematic style so it never reads as a real photograph of a real person, face occupying 50 to 65 percent of frame height with eyes on the upper third, bright key light on the face and a rim light separating it from a dark desaturated blurred domestic or institutional background, skin warm, background cool aqua-grey, high contrast and vivid, one clean quadrant of negative space for text, 1280x720, ultra-detailed
```
**共通ネガティブ `[TNEG]`:**
```
photoreal photograph of a real person, likeness of Jerry Ensminger or Mike Partain or any real veteran or judge or legislator, recognizable real celebrity, deepfake, a child, a baby, sick person, hospital, medical equipment, wounds, blood, gore, coffin, grave, military insignia, unit patch, service emblem, currency symbol, dollar sign, banner, advertisement layout, phone number, text, words, letters, numbers, watermark, logo, two faces, tiny face, neutral expression, dark muddy low-contrast mush, cartoon flatness, extra limbs, deformed, warped
```
```
- `T01_face.png`
A non-real dramatized generic older white man's face in an illustrative cinematic style at peak emotion — a steady, exhausted, unbroken stare directly at the viewer, a career serviceman's squared jaw and cropped grey hair, the look of a man who has been asking the same question for thirty years, pushed to the right third over a dark blurred kitchen background at night with one cold window, warm rim light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
- `T02_face.png`
A non-real dramatized generic middle-aged man's face in an illustrative cinematic style caught in stunned disbelief, mouth slightly open and eyes wide on the upper third, the instant an ordinary person is told something impossible about his own body, pushed to the left third over a dark blurred suburban interior with a single lamp, cool aqua-grey background and hard rim light, clean negative space on the right [TSTYLE] Avoid: [TNEG]
- `T03_face.png`
A non-real dramatized generic older woman's face in an illustrative cinematic style with a controlled, level, unforgiving expression looking directly at the viewer, decades of waiting set into the eyes and mouth, pushed to the right third over a dark blurred institutional corridor with one pale daylight window, warm key and cold rim, clean negative space on the left [TSTYLE] Avoid: [TNEG]
```
> ★これら3枚は `role:"thumb_face"`・`public_path:null`・`has_human_body:true`・`has_identifiable_real_person:false`。§6 の目視で「実在 likeness でない・illustrative・子ども/医療/墓なし・広告レジスターでない」を確認。B のサムネ案は T01–T03 を前景に、§4.3a の also_thumb body（背景）＋ 2–4語 hook（CTR §4A・例 `IT WAS THE WATER` / `THEY WROTE IT DOWN`）で組む。**金額をサムネに置かない。**

## 5.13 ★EMOTIVE FACES — VISIBLE faces（F-series 12枚・per owner 2026-07-25 standard）

匿名図だけでは「顔がほぼ無い」状態になる。オーナー方針＝**見える感情的な顔**を織り込む（顔は維持率・CTRを上げる）。F-series（見える顔）を既存の匿名図に**加えて**生成する（★distinct/cuts に数えない補助レーン・cuts への採用は B に委ねる）。

**2レーン、いずれも「実在の誰にも似せない・非実在の人物」:**
- **(a) generic-photoreal** — 特定の実在人物に紐づかない役（近隣住民・事務職員・技師・記者・傍聴人・書記）。
- **(b) dramatized-illustrative** — 中心的実在人物に隣接するビート（父 archetype・基地生まれの男 archetype）は**明らかにイラスト調・半絵画的**で写真に見えないスタイルに。実在人物として名指し/キャプションしない。

**HARD BANS（不変）:** Ensminger・Partain・その家族・議員・判事・将官の**肖像を作らない**；**子どもの顔は一切不可**；医療・傷・墓の再現なし；実在の部隊章/エンブレムなし；可読テキストなし。QCフラグ: `has_human_body:true`・`has_identifiable_real_person:false`・`has_child_depiction:false`・`has_medical_imagery:false`・`has_military_insignia:false`・`has_readable_text:false`。

**★ FACE 標準（data-driven・owner choice A）:** 全F画像は**LIGHT + EXPRESSION で目立つ顔**（サイズで盛らない）— **medium-close-up ~30–45% of frame height, eyes on the upper third, front or slight three-quarter, one strong unmistakable emotion, dramatic key + rim light against a DARK moody restrained background**。60%超の顔面充填・背向き・影に沈む・hands-only は不可。

`[FSTYLE]` = `a clearly-visible emotive human face in a strong medium-close-up filling ~30-45 percent of the frame, eyes on the upper third, front or slight three-quarter view looking near camera, one strong unmistakable emotion, dramatic key light plus rim light on the face against a dark moody background, restrained saturation, a generic anonymised non-real adult resembling no real individual, cinematic documentary grade, humid coastal grey with a chlorinated tap-water aqua note and a pale record-daylight note only on hearing beats, plain unmarked clothing with no insignia, ultra-detailed skin and eyes, high contrast, 16:9, adults only, no text, no watermark, no logo`
`[FNEG]` = `likeness of a real or named person, Jerry Ensminger, Janey Ensminger, Mike Partain, any real veteran advocate, any real senator or judge or general, recognizable real person, mugshot, deepfake, child, toddler, baby, sick person, hospital, medical equipment, IV drip, wounds, blood, injury, coffin, grave, military insignia, unit patch, service emblem, readable text, document, caption`

Files `F001.png … F012.png`. Act-mapped beats, **literal 12行（そのまま `ai_prompts.v001.md` 末尾へ追記）**:
```
- `F001.png`
A father-archetype's face rendered clearly illustrative and semi-painterly, a lean weathered man in his late thirties in medium-close-up, eyes on the upper third fixed somewhere past the camera with a flat unreadable calm that is barely holding, humid daylight key and a cold rim, dark base-quarters interior behind, not a likeness of any real serviceman [FSTYLE] Avoid: [FNEG]
- `F002.png`
Photoreal medium-close-up of a generic anonymised neighbour's face at a screen door, mid-forties, mouth open on a question that has not been answered, humid porch light from below and a cold rim from the street, dark hallway bokeh behind, generic anonymised adult [FSTYLE] Avoid: [FNEG]
- `F003.png`
A clearly illustrative semi-painterly face of the same father-archetype fifteen years older, grey at the temples, jaw set and eyes hard with a resolve that has replaced grief, one kitchen lamp as key and a cold window as rim, dark room behind, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
- `F004.png`
Photoreal medium-close-up of a generic anonymised laboratory technician's face lit by a bench lamp, late twenties, brow drawn in the exact moment of reading something that does not make sense, glassware bokeh cold behind, generic anonymised adult [FSTYLE] Avoid: [FNEG]
- `F005.png`
Photoreal medium-close-up of a generic anonymised office worker's face under fluorescent light, fifties, tired and faintly defensive, eyes on the upper third avoiding the camera by a few degrees, a corridor of shut doors soft behind, generic anonymised adult [FSTYLE] Avoid: [FNEG]
- `F006.png`
A clearly illustrative semi-painterly face of a man-born-on-the-base archetype in his late thirties, the instant of being told something impossible about his own body, eyes wide and mouth just open, a warm lamp key against a cold aqua-grey ground, not a likeness of any real man [FSTYLE] Avoid: [FNEG]
- `F007.png`
Photoreal medium-close-up of a generic anonymised woman in her sixties at a town-hall meeting, chin lifted and eyes level with a controlled anger, warm hall light as key and a cold door draught of daylight as rim, blurred folding chairs behind, generic anonymised adult [FSTYLE] Avoid: [FNEG]
- `F008.png`
A clearly illustrative semi-painterly face of a government scientist archetype, fifties, caught between conscience and procedure, one hand just entering frame at the temple, cold record-daylight key from a tall window, dark panelled hall behind, not a likeness of any real official [FSTYLE] Avoid: [FNEG]
- `F009.png`
Photoreal medium-close-up of a generic anonymised committee stenographer's face in a hearing room, thirties, absolutely composed and entirely present, pale record-daylight key with a warm rim from the dais, blurred wood panelling behind, generic anonymised adult [FSTYLE] Avoid: [FNEG]
- `F010.png`
Photoreal medium-close-up of a generic anonymised older veteran's face in a public gallery, seventies, eyes wet but jaw locked and no tear falling, pale daylight key and a cold rim, rows of blurred shoulders behind, generic anonymised adult [FSTYLE] Avoid: [FNEG]
- `F011.png`
Photoreal medium-close-up of a generic anonymised claims clerk's face behind a counter, forties, worn flat by volume rather than unkind, hard overhead key with an aqua monitor rim, stacked trays out of focus behind, generic anonymised adult [FSTYLE] Avoid: [FNEG]
- `F012.png`
A clearly illustrative semi-painterly face of the father-archetype at seventy, at a kitchen window in first light, exhausted and entirely unfinished, warm dawn key and a cold interior rim, the dark room behind him, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
```

Generate all 12; QC each visually (visible emotive face · non-real · no likeness / no child / no medical / no insignia / no text) before manifest.

> **★ shots カウントとの整合:** F001–F012 の12行は、**base 255 行（S001..S210 + M01_src..M42_src + T01_face..T03_face）の `shots=255` 検証が通った後に** `ai_prompts.v001.md` の末尾へ追記して生成する。**追記後の `shots=267`（255+12）が正**。F-series は distinct/cuts に数えない。

---

# 6. A-2/A-3: 静止画のQC・目視（★depth map なし）

## 6.1 機械QC（body 210 + i2v種 42 + thumb_face 3 = 全255枚・`qc_lejeune_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `18.0<=mean_luma<=225.0`（夜/低照度が多い→黒潰れ注意。ACT4 後半の公聴会・ACT5 の署名・ENDING の dawn は明側） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**watch-list（§5.5a の状態連鎖が正）: tap & glass 連鎖(S001–S002 / S027–S028 / S110–S111 / S186 / S197–S198 / S207)・form 7状態(S086 / S104–S106 / S112 / S116 / S150 / S188)・binder 5状態(S072–S073 / S136 / S186 / S195 / S199 / S204)・quarters 3状態(S016 / S045 / S203)・well 3状態(S097–S098 / S109)・treeline/marsh 対(S006–S007 / S201–S202)・corridor 群(S067 / S118 / S128 / S146)・archive 群(S009 / S081 / S116 / S164)・★HP waiting/gallery 群(S079 / S127 / S143 / S157 / S171–S172 / S187 / S190–S191)・★HP hands-macro 群(S010 / S028 / S057 / S062 / S082 / S105 / S135 / S137 / S144 / S161 / S163 / S176 / S181 / S185 / S195 / S204)・far-figure 群(S049 / S119 / S123 / S179 / S209) の被りに注意** | 片方 reject＋プロンプト見直し（削るのではなく §5.5a のルールで作り直す） |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・年（1953/1980/1981/1985/1987/2012/2022/2026）・濃度・件数・金額・様式名・部隊名・企業名 | `has_readable_text=true`→reject |
| Q6 | **実在人物**の顔の混入 | **目視。** 実在人物として識別可能な顔（Ensminger / Partain / 議員 / 将官 / 判事 に**似た**顔）。**匿名・非識別の顔（★HP/F/thumb_face）は OK。** | `has_identifiable_real_person=true`→reject |
| Q7 | **子ども / 医療 / 墓 / 部隊章** | **目視。★本作の最重要検査。** 子どもの姿（健康な子どもも不可）・病室/点滴/注射器/カルテ・棺/墓石/葬列・実在の部隊章/エンブレム/階級章。**★匿名の成人の身体は OK。** | あれば **即 reject** |

**Q5/Q6/Q7 は機械で判定しない。全255枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-058-lejeune --media image
#   → runs/qc/lejeune_footage_contact_NN.png（20枚/シート・約13シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-57 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** 特に **S033/S034（三輪車・ブランコ）に子どもが1人も写り込んでいないこと、S126–S128（病院外観・待合・廊下）にベッド/点滴/患者/子どもが無いこと、S193–S194（半旗・memorial lawn）に読める文字・棺・嘆く人物が無いこと、S023–S025（parade deck / formation / barracks）に実在の部隊章・階級章・基地名の看板が無いこと、S092（dry cleaner）の看板が判読不能であること、S100–S101（ドラム）に企業ロゴ・危険物表示の可読文字が無いこと、S104–S106（分析票）が完全に判読不能であること、S186（binder）のタブが白紙であること、T01–T03/F001/F003/F006/F012 が実在の Ensminger/Partain に似ていないこと、を必ず目で確認する。**

## 6.2 出力
```
episodes/PD-2026-058-lejeune/05_visuals/still_qc.v001.json     # 255枚全部の行（reject も残す）
```

## 6.3 accepted が (body210 / i2v42 / thumb3) に届かなかったとき
```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 58 --only S###   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_lejeune_stills.py
```
accepted body >= 210 かつ i2v_source >= 42 かつ thumb_face >= 3 になるまで繰り返す。**基準を下げない・水増ししない。**

## 6.4 ★depth map は生成しない（本作は depth treatment 不使用）
footage/still treatment は `bleed`/`parallax`/`duotone`/`focus` のみ・`depth` を使わない（depth displacement は被写体を melt/warp させる＝EP48/49 の warp 欠陥）。したがって **`gen_depth_maps.py` を回さない・`<stem>_depth.png` を作らない・マニフェストに `depth_path` を持たせない**（§4.2-11）。

---

# 7. A-4: LAYER 1 — 実写アーカイブ / factory 235本の選定と全点目視QC

## 7.0 ★★★ 選定は `search_archive.py` を通す。生フォルダ名で選ばない ★★★

**在庫は 111,821点の権利処理済みアーカイブ（`H:\pd-media\assets\archive\_ledger\*.jsonl`）＋ factory 棚 88,740点。** 検索窓口は**一つだけ**:

```bash
./.venv/Scripts/python.exe scripts/search_archive.py <keywords> [--theme X] [--source Y] [--kind video] [--license pd|cc0|free_commercial] [--limit N]
./.venv/Scripts/python.exe scripts/search_archive.py --stats     # 全体のテーマ/ソース/ライセンス分布
```

> **★★ 実測された罠（BINDING）: 棚のテーマフォルダ名は約40%が誤ラベルである。** 生の `theme` フォルダや `AF-BG-*__<subtype>` のファイル名を根拠に選んではならない。**本パスで実際に観測した実例:**
> - `AF-BG-0506__courtroom_interior.jpg` の実体タイトルは **"tap black faucet kitchen sink"**（theme は `legal_court`）
> - `AF-BG-9994__balance_scale_brass.jpg` の実体タイトルは **"water tap brass tap brass faucet"**（theme は `legal_court`）
> - `AF-BG-41474__chains_and_padlock_rusty.mp4` の実体タイトルは **"a rusted drum"**（theme は `atmosphere_symbolic`）
> - `AF-BG-21082__foggy_harbor_dawn.jpg` の実体タイトルは **"foggy marsh"**（theme は `nature_landscape`）
> - `AF-BG-14825__evidence_locker_shelves.jpg` の実体タイトルは **"woman drinking water after exercise"**（theme は `crime_police`）
> **この誤ラベルは両方向に効く。**本作にとっては幸運な方向にも効いており（水道・ドラム・湿地の当たりが「別テーマ」フォルダに埋まっている）、**キーワード検索＋ラベル付きコンタクトシートの目視でしか正しく拾えない。**
> **ロック前にラベル付きコンタクトシートを必ず出す**（`select_factory_assets.py` が生成し、失敗時は exit 3）。**シートを見ずに 235本を確定してはならない。**
> **`license_decision` を必ず読む。** `_quarantine/` 配下の行は **`review_required`**（ライセンス審査待ち）＝**設計に組み込まない**。使用可は `pd` / `cc0` / `free_commercial` / `pd_us_gov` のみ。
> **NARA の映像は「巻」単位のことがある**（複数の無関係ショットが1ファイルに連結）。採用時は**必ずショット選択（in/out）を記録**し、`eyeballed_content` に実際に使う区間の内容を書く。

## 7.0a ★このパスで実際に実行したアーカイブ検索（10本以上・結果つき）

| # | 実行コマンド | 結果 | 本作での用途 |
|---|---|---|---|
| 1 | `search_archive.py "marine corps"` | ヒットあり。**NARA** 複数（例 `nara__6350917-14698438__navy-and-marine-corps-troops-aboard-the-utility-landing-craf.jpeg`、`nara__6700923-12955815__u-s-marine-corps-marine-lt-gen-james-f-amos-deputy-commandan.jpeg`、theme `war_history` / `navy_harbor`、license `pd`） | **採用不可の判断**: いずれも戦闘・現代の将官で、**1950–80年代の基地生活ではない**。実在将官の写真は §1.1-1 に触れる。**使わない。** |
| 2 | `search_archive.py "camp lejeune"` | **0件** | 事件固有の実写は在庫に無い。**L3（Codex）と L1 の一般素材で組む**という設計判断の根拠。 |
| 3 | `search_archive.py "north carolina"` | ヒットあり（`AF-BG-9024__rural_road_america.jpg` = 実体 "north carolina america panorama hdr"、`AF-BG-41755__government_building_exterior.jpg` = 実体 "historic north carolina state capitol building in raleigh"、**LoC** `loc__2006678351__photographs-of-the-u-s-post-office-and-courthouse-in-new-ber.tif`＝**New Bern, NC の連邦裁判所**、license `free_commercial`） | **F009_* / F031_*（rural road・red clay）と F170_*/F174_*（courthouse exterior）の第一候補。** New Bern は EDNC の実在の分廷所在地であり、地理的にも正しい。 |
| 4 | `search_archive.py "water tower"` | `AF-BG-9073__rural_road_america.mp4` = 実体 **"4k aerial drone video of water tower in the mississippi delta"**（video, 37MB） | **F020_*（water_tower_silhouette_sky）の第一候補。** ファイル名は rural_road だが実体は水塔＝§7.0 の誤ラベル実例。 |
| 5 | `search_archive.py "drinking water"` | `AF-LIGHT-1840/1845/1896__caustics_water_light.jpg`（"clear drinking glass" 系）、`AF-LIGHT-1945__caustics_water_light.mp4`（"close up shot of drinking glass", video） | **F002_*（glass_filling_backlit）・F114_*（glass_of_water_untouched）・F210_*（water_glass_backlit_still）の第一候補。** |
| 6 | `search_archive.py "faucet"` | `AF-BG-0506__courtroom_interior.jpg`（実体 "tap black faucet kitchen sink"）、`AF-BG-9994__balance_scale_brass.jpg`（実体 "water tap brass tap brass faucet"）、`AF-VFX-1117__water_splash_black_background.jpg` | **F001_*/F010_*（kitchen_tap_running_close）・F113_*（kitchen_tap_shut_off_close）・F203_*（tap_dripping_once）の第一候補。誤ラベルの典型例。** |
| 7 | `search_archive.py "well water"` | `AF-TEX-3019__rusted_metal_texture.jpg`（実体 "well water tank well cover well lid"）、`AF-BG-32989__cell_tower_silhouette.mp4`（実体 "water well in turkana kenya", video） | **F098_*（capped_well_head_field）の候補。**ただし後者はアフリカのロケーションで時代・地理が合わない → **目視で外す前提**。 |
| 8 | `search_archive.py "pine forest"` | `AF-BG-2685/2689/2691/2709__foggy_forest.jpg`、`AF-BG-0168__moody_atmosphere_fog.jpg` 他多数（theme `nature_landscape`） | **F005_*/F029_*（pine_treeline_dusk_wind）・F124_*（pine_canopy_from_above）・F205_*（pine_treeline_first_light）の候補プール。** |
| 9 | `search_archive.py "marsh"` | `AF-BG-21082__foggy_harbor_dawn.jpg`（実体 "foggy marsh"）、`AF-BG-35488__forest_fog_morning.jpg`（実体 "fog marsh landscape wetlands"） | **F006_*（coastal_marsh_fog_still）・F206_*（coastal_marsh_dawn_still）の第一候補。誤ラベル実例。** |
| 10 | `search_archive.py "rusted drum"` / `"industrial barrel"` | `AF-BG-41474__chains_and_padlock_rusty.mp4`（実体 **"a rusted drum"**, video, 6MB）、`AF-BG-54758__oil_refinery_at_night.jpg`（実体 "barrels for liquid substances at industrial factory"） | **F100_*（rusted_drum_in_grass）・F101_*（industrial_barrels_row_yard）の第一候補。誤ラベル実例。** |
| 11 | `search_archive.py laboratory --theme medical_lab` | `AF-BG-1999〜2005__laboratory_glassware.jpg`（"test tubes on test tube rack" / "graduated cylinders" 他） | **F087_*/F155_*（laboratory_glassware_rack）・F088_*（sample_bottles_on_bench）の候補プール。★医療行為・患者の写るものは除外する（§1.1-3）。** |
| 12 | `search_archive.py "archive box" --theme documents_paper` | `AF-BG-5233__warehouse_interior_dark.jpg`（実体 "archive boxes shelf folders"）、`AF-BG-10047__old_library_archive.jpg`（実体 "vintage document in archive box on desk"） | **F008_*/F117_*（steel_shelving_file_boxes）・F073_*（cardboard_boxes_stacked_hall）の第一候補。誤ラベル実例。** |
| 13 | `search_archive.py "chain link fence"` | `AF-BG-12025/12039/12043/12047__padlock_and_chain.jpg`、`AF-BG-0336__blurred_city_night_bokeh.jpg`（実体 "fence chain link bokeh lights"） | **F028_*（chain_link_fence_perimeter）・F112_*（padlock_on_gate_closing）の第一候補。** |
| 14 | `search_archive.py "capitol dome"` | `AF-BG-16234〜16238__capitol_dome_dusk.jpg`（州議事堂各種）、`AF-BG-37134__capitol_dome_dusk.jpg` | **F147_*（capitol_dome_dusk_wide）・F171_*（capitol_steps_daylight_wide）の候補。★連邦議事堂と州議事堂を混同しないよう目視で選ぶ。** |
| 15 | `search_archive.py testimony` / `senate` / `congress hearing` | `congress hearing` = **0件**。`testimony` は Nuremberg / Leo Frank 等の**無関係な歴史素材のみ**（多くが `_quarantine` の `review_required`）。`senate` は `AF-BG-29770__courtroom_interior.mp4`（実体 "panning shot of the texas state senate chamber", video）が唯一有用 | **公聴会の実写は在庫に無い。** ACT4 の公聴会ビートは **L1＝木質パネルの議場/法廷インテリア（F144_*/F175_*/F190_*）＋ L3＝Codex（S139–S144）＋ L2＝AE カード**で構成する。**`_quarantine` の Nuremberg 等は license `review_required` なので設計に入れない。** |
| 16 | `search_archive.py home --theme americana_1930s_1970s` / `family --theme americana_1930s_1970s` | `home` = 2件（`ia__hmpennsylvaniarailro98201__…` 等の家庭映画、license `pd`）／`family` = **0件** | **期待した「1950–70年代の米国家庭生活」は薄い。** ACT1 の基地住宅ビートは **L3（Codex）が主・L1 は環境（洗濯物・網戸・郊外街路）だけ**という配分の根拠。 |

**この16本の実測から出た設計判断（DESIGN §1a と一字一致）:**
1. **事件固有の実写はゼロ** → L1 は「時代と場所の空気」「物」「制度の空間」を担当し、**物語の固有名詞は L2（AE）と L3（Codex）が担当する**。
2. **NARA/LoC の当たりは戦史・裁判所建築に偏る** → 本作で使える NARA/LoC は **New Bern の連邦裁判所（LoC）** が最良で、**海兵隊関連 NARA 画像は実在の将官が写るため使わない**。
3. **水・松林・湿地・ドラム・書庫は factory 側に十分ある** — ただし**全部ラベルが壊れている**ので、**キーワード検索とコンタクトシート目視でしか拾えない**。

## 7.1 選定条件
- `kind:video` を優先（L1 は「動く実写」で紙芝居を潰すレイヤー）。静止画しか無いテーマは L3 に回す。
- **license は `pd` / `cc0` / `free_commercial` / `pd_us_gov` のみ。** `review_required` と `_quarantine/**` は不採用。
- **1本1回のみ使用**（`MAX_USES_FACTORY = 1`）。235本＝235カット。
- **EP39〜EP57 と sha256 が1件も重ならないこと**（§7.4・BLOCKING）。
- **時代・地理の整合を目視で確認**（現代車/スマホ/LED/外国のロケーションが 1970–80年代ビートに紛れ込まない）。
- **★子ども・医療行為・墓・実在の部隊章/企業ロゴが写るクリップは全て外す**（§1.1-2/1.1-3/1.1-5）。

## 7.2 実写在庫でカバーする代表シーン（`covers_scene_id` は §4.4 に pre-assign 済み）
水道と glass（F001_*/F002_*/F010_*/F051_*/F113_*/F114_*/F203_*/F210_*）・基地住宅の環境（F013_*–F016_*/F029_*/F045_*/F207_*）・松林と湿地と海岸（F005_*/F006_*/F029_*/F030_*/F122_*/F205_*/F206_*/F234_*）・水インフラ（F020_*/F095_*–F099_*/F110_*/F125_*/F168_*）・ドラムと廃棄場（F100_*/F101_*/F105_*）・書庫と紙（F008_*/F062_*–F067_*/F073_*/F117_*/F118_*/F150_*/F169_*/F177_*/F192_*/F216_*）・研究室（F087_*–F091_*/F155_*/F156_*）・制度の空間（F070_*/F144_*/F147_*/F171_*/F174_*–F176_*/F190_*/F194_*）・夜と天候（F039_*/F079_*/F161_*/F162_*/F196_*/F224_*）。

## 7.3 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）
`pd` / `pd_us_gov` / `cc0` / `free_commercial`。**`review_required` は不可。** 各行の `license_decision` を `stock_ledger.v001.json` に転記し、`origin` を `factory` / `archive` / `stock` で区別する。

## 7.4 EP39〜EP57 との重複ゼロ（BLOCKING）
```bash
./.venv/Scripts/python.exe scripts/select_lejeune_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39〜EP57 のすべてに対して）
```
色レーンも分離する: 他話の accent 色（§5.3 のリスト）に寄ったクリップを選ばない。**本作は水のアクア＋海岸の灰＋松と赤土。**

## 7.5 出力
```
episodes/PD-2026-058-lejeune/05_stock/factory_selection.v001.json
episodes/PD-2026-058-lejeune/05_visuals/factory_clip_qc.v001.json   # ★235本すべてに eyeballed 記録
```

---

# 8. A-5: i2v モーション化 42本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする42本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）
種画像は §5 と同じ `generate_sdxl_4k.py`（variants なし）で `M<NN>_src.png` として生成。**`role:"i2v_source"` として専用確保し body に回さない**。i2v_source の asset_id は `LEJ-MS01..MS42`、モーション成果物は `LEJ-M01..M42`。**幕別配分は §4.5 に pre-assign 済み**（ACT0 3 / ACT1 7 / ACT2 6 / ACT3 8 / ACT4 8 / ACT5 6 / ACT6 4 = 42）。
> **★このうち ★18本は §5.11 の匿名人物ビート（H001–H018）＝42本の内数**（M01/M04/M06/M07/M10/M11/M13/M16/M17/M18/M21/M24/M25/M26/M27/M29/M31/M33）。**残り 24本が抽象/象徴種。**

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの42行を追加・各1枚・**poised-still の source**）
> 各種プロンプトは §5.6/§4.5 の対応 tag の「動く直前の poised-still」版。**動きが意味を持つ絵**（tap が開く直前・drawer が閉じる直前・pen が margin に触れる直前・binder が閉じる直前 等）。末尾に §5.3 `[STYLE]` ＋ `Avoid:` §5.4 `[NEG]`（人物種は `[HSTYLE]`/`[HNEG]`）を全文連結。

```
- `M01_src.png`
An anonymised adult's hand on a kitchen tap handle at night with a plain glass waiting in the sink beneath, held absolutely still in the half-second before the tap turns, one overhead fixture, the glass empty and clear, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M02_src.png`
A dark living-room wall carrying the cold light of an unseen television, the light held motionless at the instant before the picture cuts and everything in the room changes value, a doorframe and a lamp base catching the edge of it, no person, no readable text [STYLE] Avoid: [NEG]
- `M03_src.png`
A loblolly pine treeline at dusk photographed dead still in the moment before a gust reaches it, every needle and branch frozen, the sky behind holding one last band of pine-and-clay light, no people, no readable text [STYLE] Avoid: [NEG]
- `M04_src.png`
Two anonymised adults halted mid-step on a concrete walkway carrying cartons toward base family quarters, poised in the instant before the leading foot lands, seen from well behind so no face reads, humid 1970s morning, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M05_src.png`
A line of bed sheets hanging dead vertical between two brick quarters in the stilled half-second before a gust takes them, sunlight coming through the cotton, the pegs holding, no people, no readable text [STYLE] Avoid: [NEG]
- `M06_src.png`
An anonymised figure standing with squared shoulders and hands behind the back at the edge of a vast empty parade deck at dawn, held motionless a beat before turning, seen entirely from behind, plain unmarked utilities with no insignia, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M07_src.png`
An anonymised adult's hands holding an empty glass under a kitchen tap that has not yet been opened, framed at the wrists, everything poised, daylight flat through a window above the sink, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M08_src.png`
A steel water tower standing against a sky of fast cloud held frozen for one frame, the tank blank and the ladder sharp, heat shimmer suspended at the base of the legs, no lettering anywhere, no people, no readable text [STYLE] Avoid: [NEG]
- `M09_src.png`
A small tricycle standing motionless on a concrete walkway with one pedal at the top of its arc and the front wheel turned, the walkway and lawn beyond entirely empty, a long low shadow, nobody anywhere in frame, no readable text [STYLE] Avoid: [NEG]
- `M10_src.png`
An anonymised adult sitting alone at a kitchen table with hands flat either side of a closed folder, held completely still in the beat before the hands move, photographed from behind and slightly above so no face reads, one pendant lamp, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M11_src.png`
An anonymised adult standing rigid in front of an unseen television, the cold light on one shoulder held at the instant before it changes, the head turned away entirely, the room otherwise unlit, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M12_src.png`
A plate of food set down on a table and framed from directly above, the steam already gone, a fork laid across it, held in the stillness of a meal that will not be eaten, a chair back at the frame edge, no person, no readable text [STYLE] Avoid: [NEG]
- `M13_src.png`
An anonymised adult's hands resting on typewriter keys with a fresh sheet curled in the platen, poised in the second before the first strike, framed at the wrists, a desk lamp raking across the keys, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M14_src.png`
A sealed envelope held at the mouth of a public post slot, poised the instant before release, the slot's shadow swallowing the lower edge, no address or marking of any kind on the paper, cold street light, no readable text [STYLE] Avoid: [NEG]
- `M15_src.png`
A steel filing drawer stopped an inch from closing over a packed row of folders, held motionless in the moment before it shuts, the folder tabs blank, fluorescent light flat above, no person, no readable text [STYLE] Avoid: [NEG]
- `M16_src.png`
An anonymised adult's hands laid flat on the open covers of an empty ring binder on a kitchen table, poised before the first page goes in, the rings sprung wide, one lamp low, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M17_src.png`
An anonymised technician's hand holding a glass sample bottle up against a bench lamp, held perfectly still, the water inside colourless and throwing a cold aqua refraction on the bench, framed at the wrist, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M18_src.png`
An anonymised hand with a ballpoint poised a millimetre above the remarks box of a printed form, extreme macro, the pen not yet touching, the form's grid sharp and its wording an unreadable smear, hard raking lamp light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M19_src.png`
The needle of a chart recorder resting at the baseline of a rolling paper drum, held in the instant before it kicks, macro on the pen arm and the wet ink, the drum's ruling reduced to unreadable grey, no person, no readable text [STYLE] Avoid: [NEG]
- `M20_src.png`
The lid of a solvent drum lying half-buried in long grass beside the drum itself, the grass around it stopped mid-lean in a wind, ochre paint blistered, a puddle beside catching a flat sky, no people, no readable text [STYLE] Avoid: [NEG]
- `M21_src.png`
An anonymised worker's gloved hands closed on the spokes of a rusted valve wheel, poised in the breath before the wheel turns, framed at the forearms, flakes of ochre paint under the grip, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M22_src.png`
A kitchen tap with its handle at the closing position above a completely dry sink, one last bead hanging at the spout and not yet dropping, the plug chain hanging dead still, cold window light, no person, no readable text [STYLE] Avoid: [NEG]
- `M23_src.png`
A single printed form held at the mouth of an open manila folder, poised an instant before it slides in, macro, the folder tab blank, a desk surface and other folders beyond, cold office light, no person, no readable text [STYLE] Avoid: [NEG]
- `M24_src.png`
An anonymised adult's hands gripping the ends of a grey records carton on a high steel shelf, held in the moment before the box tips out, framed at the forearms, the shelf label holders empty, one strip light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M25_src.png`
An anonymised adult seated at a cluttered home desk with his back to the camera, held motionless before a glowing monitor, the shoulders rimmed by the screen, papers fanned around the keyboard, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M26_src.png`
An anonymised adult's hand holding an index card just above the last gap in a grid of cards laid across a table, poised before it lands, framed at the wrist, every card's writing an unreadable scribble, one warm lamp, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M27_src.png`
An anonymised adult's fingers pinching a map pin a hair above a cork board already thick with them, poised before it is pushed home, macro, the map beneath reduced to unreadable pale shapes, desk lamp raking, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M28_src.png`
A gooseneck microphone and an untouched glass of water on a witness table, absolutely still, the room beyond soft and pale with record-daylight, the chair behind the table empty, no person, no readable text [STYLE] Avoid: [NEG]
- `M29_src.png`
Rows of anonymised adults in a hearing gallery settling into complete stillness, photographed from the very back so only shoulders and the backs of heads read, one late arrival still half-seated, pale record-daylight, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M30_src.png`
A bound report held at the mouth of a gap on a shelf, poised in the instant before it is pushed back in among the other volumes, macro at the spine, every spine blank, the shelf shadow waiting, no person, no readable text [STYLE] Avoid: [NEG]
- `M31_src.png`
An anonymised adult standing before a wall of pinned pages that reaches from waist height to the ceiling, held motionless with one hand raised toward it, seen entirely from behind, every page an unreadable grey, one work lamp, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M32_src.png`
A wall of storm light stopped over a flat coastal horizon, rain visibly hanging beneath one cloud mass and not yet arriving, the water beneath it dead flat, marsh grass frozen mid-lean, no people, no readable text [STYLE] Avoid: [NEG]
- `M33_src.png`
An anonymised hand holding a heavy pen a fraction above the signature line of a document, poised before the nib touches, extreme macro, the printed text an unreadable band, pale record-daylight, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M34_src.png`
A tall stack of identical claim forms on a counter with one more sheet held above it, poised before it lands and makes the stack taller, the paper edges catching hard overhead light, more stacks waiting out of focus, no person, no readable text [STYLE] Avoid: [NEG]
- `M35_src.png`
A single docket page lifted at the corner and held at the top of its arc, poised before it falls across to the other side, macro, the printed columns reduced to grey, the block of paper beneath visibly enormous, no person, no readable text [STYLE] Avoid: [NEG]
- `M36_src.png`
The saturated glow of a late-night television held on one frame in an empty room, the screen unreadable, the light finding a recliner and a cold glass on a side table, the curtains dead still, no person, no readable text [STYLE] Avoid: [NEG]
- `M37_src.png`
An empty courtroom held in complete stillness, the bench and counsel tables vacant, one shaft of window light stopped across the floor with dust suspended in it, chairs squared, nothing moving anywhere, no people, no readable text [STYLE] Avoid: [NEG]
- `M38_src.png`
A wall calendar page lifted at one corner and hanging at the top of its lift, poised before it falls back flat, the grid a pale unreadable pattern, a thumb tack above, bare plaster around, no person, no readable text [STYLE] Avoid: [NEG]
- `M39_src.png`
A thick ring binder with its cover raised and held at the last inch before closing on a kitchen table, the rings about to click, first light across the vinyl, nobody in frame, no readable text [STYLE] Avoid: [NEG]
- `M40_src.png`
A single drop of water gathering at the lip of a kitchen tap and held at maximum size an instant before it falls, extreme macro, the dry sink far below out of focus, dawn light cold on the metal, no person, no readable text [STYLE] Avoid: [NEG]
- `M41_src.png`
A row of low brick family quarters at the exact moment first light reaches the top course of brick and has not yet come further down the wall, dew held on the grass, every window dark, no people, no readable text [STYLE] Avoid: [NEG]
- `M42_src.png`
An absolutely flat sheet of still water running to a grey horizon, held in one unmoving frame with a single band of early light lying across it, no land and no vessel anywhere, the surface unbroken, no people, no readable text [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_postoffice.py` を下敷きにパスと SHOTS だけ差し替え）
既存ドライバの既定値をそのまま使う。**解像度 1280x720 / 出力 mp4 / 1本ずつ直列。** 42本は**複数日**。夜間・分割で回す。開始前にマシン状態（VRAM/温度/他プロセス）を確認する。

## 8.3 実行手順（まず1本で通す・★42本は複数日）
```bash
./.venv/Scripts/python.exe scripts/comfy_wan_lejeune.py --only M01     # まず1本
./.venv/Scripts/python.exe scripts/comfy_wan_lejeune.py                # 残り
./.venv/Scripts/python.exe scripts/rife_lejeune.py                     # RIFE 4x -> 48fps
```

## 8.4 i2v の QC
全42本を**目視**。`frames`/`duration_sec` を記録。**SHORT?（極端に短い）を検出したら作り直す。** ★人物種18本は「匿名・非識別・adults only・子どもゼロ・医療ゼロ・部隊章ゼロ」を必ず目で確認する。

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど30本）
§4.6 の30本を選定する（15 particle / 10 light / 5 vfx）。**per-beat の疎なアクセントのみ**。全編常駐の持続レイヤーにしない（screen-wash ≤0.07）。scanline/CRT/vignette-wash を選ばない。

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_lejeune_assets.py`）
```
remotion/public/lejeune/img/S<NNN>.png
remotion/public/lejeune/factory/F<NNN>_<subtype>.mp4
remotion/public/lejeune/motion/M<NN>_rife.mp4
remotion/public/lejeune/overlay/{P|L|V}<NN>_<subtype>.mp4
remotion/public/lejeune/thumb/   ← thumb_face は public に出さない（B が別途扱う）
```
命名規則は `check_asset_reuse.py` の `kind_of()` がパス文字列で種別を判定するため**必ず守る**。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`
factory/archive の全235行に `source` / `license_decision` / `origin` / `url_or_shelf_id` / `sha256` / `eyeballed_content` / （NARA の巻なら）`in_out_sec` を記録する。

## 10.3 境界契約マニフェストの出力
```bash
./.venv/Scripts/python.exe scripts/build_lejeune_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_lejeune_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_lejeune_asset_manifest.py --reuse-feasibility
```

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）
```python
MAX_USES_FACTORY = 1
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
MAX_AVG_USES_PER_SOURCE = 1.4   # ★EP49 は 1.8 で flag された
```
EP58 の設計値: still 244/210=1.162(≤2) / factory 235/235=1.0(≤1) / motion 84/42=2.0(≤2) / first-use 487/563=0.8650(≥0.70) / avg-uses 563/487=1.156(≤1.4)。**全て達成可能。**

---

# 12. 絶対にやらないこと
- **EP39〜EP57 のファイル・素材に触らない。** 読み取りのみ可。素材・色・音のレーンも分離（§7.4）。
- **スレッドBの所有ファイル（§0.2）に触らない**。ただし `04_scenes/ai_prompts.v001.md` は A が書く。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness をどこにも作らない**（Jerry Ensminger / Janey Ensminger / Mike Partain / その家族 / 議員 / 将官 / 基地司令官 / ATSDR・CDC 職員 / 弁護士 / 判事）。**匿名・非識別の成人は可。**
- **★病気の子ども・死にゆく子ども・子どもの遺体/棺/墓を一切作らない。健康な子どもも本作では作らない。** 悲嘆は物・不在・大人の姿だけで運ぶ（本作の最重要禁止）。
- **★医療行為・医療機器・診療の絵を一切作らない**（成人でも不可）。
- **因果を断定する語・絵を作らない**（"the water killed / caused the cancer"）。政府の責任認定の含意も作らない（**いかなる裁判所も合衆国の責任を認定していない**）。
- **実在の部隊章・エンブレム・旗の意匠・階級章・基地名の看板・企業ロゴを作らない。**
- **可読の偽公文書を作らない**（分析票・報告書・議事録・法案・訴状・小切手）。**数値を画像に描かない。**
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。（factory の subtype `_02` は別素材の意・混同しない。）
- **role=thumb / still_thumb を作らない・overlay を30本以外にしない・thumb_face を3枚以外にしない。** also_thumb は body 4枚（§4.3a）。
- **★factory 235 / motion 42 / overlay 30 の配列を空・stub のまま出荷しない**（EP45/EP38 事故）。
- **★depth map を生成しない・`depth_path` を持たせない**（§6.4）。
- **★`dochighlight` figure を作らない・言及しない**（BANNED・grep で 0 件）。**`DATE_STAMP` レイアウトを使わない**（BANNED・AE に存在せずビルドがクラッシュする。日付カードは `CENTER_STACK`）。
- **★生フォルダ名・ファイル名・subtype を根拠に factory を選ばない**（棚のラベルは約40%が壊れている・§7.0）。**`search_archive.py` ＋ ラベル付きコンタクトシート目視を通す。** `review_required` / `_quarantine` を設計に入れない。
- **枚数を「だいたい」で決めない。** §3 の確定値（still 210 / factory 235 / i2v 42 / thumb_face 3 / distinct 487 / first-use 0.8650 / still-share 0.4334 / avg-uses 1.156 / overlay 30）と §3.3 の検算をそのまま使う。合わなければ本書を疑って報告。

---

# 13. 完了報告に含めるもの
```
1. accepted 静止画の枚数と内訳（body 210 [＝object 125 ＋ ★HP human-present 85 = 40.5%] / i2v_source 42 [＝抽象 24 ＋ ★人物 18] / thumb_face 3 / F-series 12 / also_thumb 4 [§4.3a] / reject N）
2. factory/archive 選定 235本のリスト（asset_id / subtype / origin[factory|archive|stock] / source / license_decision / eyeballed_content / NARA 巻の in_out_sec）と、
   ラベルと食い違って外した本数、review_required を1件も入れていない確認、コンタクトシートを見た記録
3. EP39〜EP57 重複ゼロの確認結果
4. i2v 42本の frames / duration_sec と SHORT? の有無、★H001–H018（18本）の匿名・非識別・adults-only 確認、
   ★HP body 85枚が匿名・非識別・実在 likeness なし・★子どもゼロ・★医療ゼロ・★墓ゼロ・★部隊章ゼロ・
   可読テキストなし・★変化マトリクス（§5.5a-5・被写体+構図+光の3要素同時一致ゼロ）の確認
5. 合成レイヤー30本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code）＋ factory 235/motion 42/overlay 30 が非空で実体化した確認 ＋ depth_path をどこにも生成していない確認
7. §3.3 の検算 [1]〜[8] を自分で再計算した結果（avg-uses/source 1.156≤1.4 を含む）
8. asset_manifest.v001.json の counts ブロック（still_body 210 / still_i2v_source 42 / motion 42 / factory 235 / overlay 30 / thumb_face 3）
9. 制約・1枚前提の自己申告（因果の断定なし・政府の責任認定の含意なし・子どもの描写ゼロ・医療描写ゼロ・墓/棺ゼロ・
   実在の顔/likeness ゼロを目視確認・実在の部隊章/ロゴゼロ・可読の偽公文書ゼロ・数値の可読描画ゼロ・
   dochighlight 文字列ゼロ・DATE_STAMP 不使用・milky wash/scanline なし・depth なし・バリエーション0・時代錯誤なし・
   A↔B同一スキーマ[schema lejeune_assets.v1 / role enum body|i2v_source|thumb_face|reject / counts / also_thumb 集合 4 / overlay 30 / thumb_face 3]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
