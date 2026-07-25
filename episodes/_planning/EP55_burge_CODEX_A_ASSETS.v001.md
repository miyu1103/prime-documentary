# EP55 burge — Codex スレッドA「素材生成」引き継ぎプロンプト v001（30分・4幕・payoff 末尾積み上げ）

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN_ARCHITECTURE）も実装スレッドB（CODEX_B）も**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> ★30分尺。素材点数は EP52 morton と同スケール。**「だいたい」で決めず §3 の確定値と §3.3 の検算をそのまま使う。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP55 / Episode ID: PD-2026-055-burge / slug: burge
Composition id: Ep55Burge（B が Root.tsx に登録・A は staging まで）／1920x1080 / fps30 / 30:00
事件:       The Jon Burge torture ring（シカゴ警察 Area 2/3 の司令官 Jon Burge と "Midnight Crew"）
            1972〜1991、シカゴ市警 Area 2（後に Area 3）の刑事集団 "Midnight Crew" が、Burge の指揮下で
            100人超（ほぼ全員が黒人男性）から自白を拷問で引き出した。手回し発電の「black box」による電気
            ショック、タイプライターカバーでの窒息（"bagging"）、模擬処刑、ラジエーター火傷。
            1982-02、警官殺害容疑者 Andrew Wilson が Area 2 で拷問され、Cook County Jail の医師
            Dr. John Raba が負傷を診て警視総監 Brzeczek に調査を求める書簡を書いた——その書簡は放置された。
            1990 記者 John Conroy が Chicago Reader「House of Screams」で告発。同年 OPS の Goldston 報告が
            虐待を "systematic" と認定（1992 まで封印）。1993-02、Burge は Police Board により解雇——
            しかし時効（statute of limitations）の壁で拷問そのものは起訴不能。2002-06 特別検察官
            Egan/Boyle も「虐待はあったが起訴できない」と結論。一方 Death Row 10 の運動を経て、
            2003-01 Ryan 知事が Patterson / Hobley / Orange / Howard の4人を無実として恩赦。
            2003 の民事訴訟で Burge は宣誓供述で「拷問は無かった・知らない」と虚偽回答
            → 連邦検察は【拷問ではなく、その嘘】を突いた。2008-10 逮捕、2010-06-28 偽証＋司法妨害で有罪、
            2011-01 に 4.5 年の刑。年金は理事会 4-4 で維持。2014-15 釈放、無反省の書面を公表。
            2015-05、シカゴ市議会が【全米史上初の警察拷問リパレーション条例】を可決：$5.5M 基金（57人）、
            公式謝罪、市立カレッジ無償、Chicago Torture Justice Center、そして市の公立学校（8・10年生）で
            この事件を必修として教えるカリキュラム。Burge は 2018-09 に死亡、最後まで無反省。
            死後も冤罪の無罪化は続き、市・郡の支払総額は $100M 超。
            ★主題は【拷問は時効で裁けなかった——裁けたのは嘘だけ。そして真実は教科書になった】。
            ★Jon Burge は【死亡（2018）・偽証/司法妨害で有罪確定】＝有罪と公式認定事実は断定してよい。
              ただし【拷問罪では一度も起訴・処罰されていない】＝"convicted of torture" と絶対に書かない。
            ★★被害者・サバイバーは【大半が存命】。2003 年恩赦の4人（Patterson/Hobley/Orange/Howard）は
              無実を断定可。他の申立人は【拷問認定】のみ語り、無実を一括断定しない。
            ★★★拷問の描写は一切作らない＝物・影・aftermath のみ（拘束された人物・人体に触れる装置・
              苦痛の顔・再現は全面禁止）。実在人物（Burge/Wilson/Holmes/恩赦4人/Raba/Daley/Fitzgerald/
              Ryan/Emanuel/判事/刑事）の顔・肖像・likeness を一切作らない。匿名・非識別の一般人は可。
              人種的にセンシティブ＝サバイバー像は尊厳ある silhouette（うずくまり・苦悶ポーズ禁止）。
              時代考証 1972–2018 のシカゴ（スマホ/現代車を混ぜない）。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ・30分スケール）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**210本の固有プロンプト×1枚＝210枚**・バリエーション0） | `H:\pd-media\assets\ai\burge\S<NNN>.png` | 5–8時間（GPU） |
| A-1b | i2v 種画像の生成（**42本の固有プロンプト×1枚＝42枚**・バリエーション0） | `H:\pd-media\assets\ai\burge\M<NN>_src.png` | 1.5–2.5時間（GPU） |
| A-1c | サムネ用 emotive-face 静止画（**3枚**・CTR §4A・非実在の illustrative face・§5.12） | `H:\pd-media\assets\ai\burge\T<NN>_face.png` | 20分（GPU） |
| A-2 | 静止画のQCと目視（**全255枚を目視必須**＝210 body + 42 i2v種 + 3 thumb_face） | `05_visuals/still_qc.v001.json` + コンタクトシート | 2.5–4時間 |
| A-3 | ~~depth map~~ **不要（本作は depth treatment を使わない・§6.4）** | — | — |
| A-4 | factory 実写クリップ **235本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | 4–6時間（うち目視だけで2時間以上） |
| A-5 | i2v モーション化 **42本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\burge\M<NN>_rife.mp4` | 18–48時間（GPU・**複数日**） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **30本** | `05_stock/overlay_selection.v001.json` | 1時間 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 30分 |
| A-8 | Remotion public への staging | `remotion/public/burge/{img,factory,motion,overlay,thumb}/` | 40分 |

> **★★ 最重要の前提（EP42–52 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 210本＝210行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **variants 指定なし（＝1枚）** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 210 + i2v 種 42 + thumb_face 3 = 255枚（各1回）。** factory 235本は生成でなく在庫からの選抜。
> ★**`--only S001` のログで `shots=255` を確認**してから本番を回す（210 body + 42 i2v種 + 3 thumb_face = 255）。
> ★i2v 42本は**複数日GPU**。**開始前にマシン状態を確認**（heavy-job preflight）。夜間・分割で回す。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-055-burge/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を **A(producer)とB(consumer/validator)で一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 235 エントリ、`motion` 配列は 42 エントリ、`overlay` 配列は 30 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5／§4.6 に全 235 + 42 + 30 を列挙済み。build スクリプトはこの列挙を消費するだけで、空配列を書かない）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\burge\**` / `H:\pd-media\assets\ai_video\burge\**` | **A** | 読み書き |
| `episodes/PD-2026-055-burge/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-055-burge/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/burge/{img,factory,motion,overlay,thumb}/**` | **A** | 読み書き |
| `episodes/PD-2026-055-burge/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_burge_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-054-*/**` および EP39〜54 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を読む） | `PD-2026-055-burge`（variants 指定なし） / `55 --only S001` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-055-burge --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit N --exclude-used --ep PD-2026-055-burge --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-055-burge` |

> **★`gen_depth_maps.py` は使わない**（本作は depth treatment を使わない＝depth map 不要・§6.4／DESIGN §1「footage treatment は bleed/parallax、depth 禁止」）。

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（実在確認してから・直近の `*morton*`(EP52) を優先、無ければ `*centralpark*`(EP50)） |
|---|---|---|
| `scripts/qc_burge_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_morton_stills.py`（無ければ `qc_centralpark_stills.py`） |
| `scripts/select_burge_factory.py` | §7 の factory 235本の確定選定・EP39〜54 sha256 除外検証 | `scripts/select_morton_factory.py`（無ければ `select_centralpark_factory.py`） |
| `scripts/comfy_wan_burge.py` | §8 の i2v 42本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_morton.py`（実在確認） |
| `scripts/rife_burge.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_morton.py`（実在確認） |
| `scripts/build_burge_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_morton_asset_manifest.py` |
| `scripts/stage_burge_assets.py` | §10 の staging | `scripts/stage_morton_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.9 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_burge_facts.py`（B が clone して実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の制約に一致し、`check_burge_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_burge_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==235 / motion 配列長==42 / overlay 配列長==30 が非空で実体化していること（EP45 事故回避の必須不変条件）

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_burge_asset_manifest.py --reuse-feasibility
#   → still >=210 / motion >=42 / factory >=235 / distinct 合計 >=487 / first-use >=0.70 / avg-uses/source <=1.4

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_burge_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全235本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-055-burge

# [A-DONE-5] EP39〜EP54 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_burge_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39〜EP54 のすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（正確性制約・ガードレール）★★★

**Jon Burge は【死亡（2018-09-19）・2010-06-28 に司法妨害2件＋偽証1件で有罪・4.5年】＝有罪と公式認定（Goldston 1990 / Police Board 1993 / 特別検察官 2006 / 連邦裁判所 / TIRC）は断定してよい。ただし【拷問罪では一度も起訴・有罪になっていない】＝"convicted of torture / punished for torture" を絶対に書かない。サバイバーは大半が存命: 2003 恩赦の4人（Patterson/Hobley/Orange/Howard）と Kitchen・Jackie Wilson は無実を断定可。Andrew Wilson は警官殺害で有罪（拷問の被害事実のみ語る）。他の申立人は【拷問認定】のみ・無実の一括断定禁止。Midnight Crew の個々の刑事は adjudicated finding のある文脈以外で名指ししない（"his men"）。拷問の視覚化は全面禁止＝物（inert な box・radiator・typewriter）・影・空室・aftermath のみ。拘束された人物・人体に触れる装置・苦悶の顔・再現・叫び声を一切作らない。全実在人物の顔・肖像・likeness 禁止。匿名・非識別の一般人は可。人種的にセンシティブ＝黒人男性サバイバーの silhouette は尊厳第一（直立・静・逆光）。数値は hedged（100+/118・~$7M・~$3,000/月・$210M+）。exact-of-record（4.5年・3 counts・4–4・$5.5M/57・2010-06-28・2015-05-06）は断定可。捏造引用禁止・可読の偽公文書禁止・時代考証 1972–2018。**

## 1.1 R1/R2（生成ビジュアル全般）

1. **★R-FACE: 匿名・非識別の人物は可／実在人物の likeness は不可。** 匿名の一般人（実在の誰にも似せない・非識別のドラマ化スタンドイン）＝顔・身体を出してよい（§5.11 H シリーズ・`[HSTYLE]`/`[HNEG]`・§5.12 thumb_face・§5.13 F シリーズ）。ただし **実在人物の顔・likeness・肖像は作らない**＝Jon Burge・Andrew Wilson・Jackie Wilson・Anthony Holmes・Melvin Jones・Patterson/Hobley/Orange/Howard・Kitchen・Dr. Raba・Brzeczek・Daley・Conroy・Goldston・Egan/Boyle・Fitzgerald・Lefkow 判事・Ryan 知事・Emanuel 市長・実在の刑事/判事/市議を**似せて描かない**。実在人物が示唆される所（司令官・医師・記者・検事・サバイバー）は非識別（背向き/影/逆光/目から下でクロップ/hands-only）を既定に保つ。
2. **★R-TORTURE-DEPICT（本作の最重要禁止）: 拷問・暴行・拘束を一切描かない。** 「box が人に繋がれた絵」「手錠の人物」「頭に袋/カバー」「radiator に接する人体」「銃を向けられる人物」「苦悶/絶叫の顔」「取調室内の被疑者と刑事の対峙」を**正プロンプトにもネガにも構図にも作らない**。box は常に **inert（無人の卓上・引き出しの中・影の中）**。radiator は**無人の部屋**。typewriter cover は**畳まれた事務用品**。部屋は常に**空室＝aftermath**。
3. **可読の偽公文書を再現しない。** Raba の手紙・interrogatory・Goldston 報告・判決文・新聞・カルテ・年金小切手の**可読文字を再現しない**（"blurred into an unreadable smear"）。日付（1982/1990/1993/2003/2010/2015 等）・数値（118/4.5/54/$5.5M/$210M/4-4）・署名は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。
4. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **R-BURGE-CONVICT:** "Burge convicted of torture / punished for the torture / torture conviction" を書かない。有罪は常に **perjury / obstruction（嘘）**。"the man they could only jail for lying" の帰属枠は可。
2. **R-TORTURE-DEPICT:** "man being shocked / suffocated / electrocuted / tortured, suspect handcuffed to a radiator, bag over a head, gun to a head, screaming face, restrained prisoner, interrogation in progress" を書かない。物は inert・部屋は empty・人体と装置を同一フレームに置かない。
3. **R-VICTIM-STATUS:** 恩赦4人＋Kitchen＋Jackie Wilson 以外に "innocent" を一括適用しない。Andrew Wilson を "innocent" と書かない（"tortured" は可）。サバイバーを "criminals/thugs" 側からも描写しない。
4. **R-RACE:** 黒人男性サバイバーの silhouette は "dignified, upright, still, backlit"。"cowering / broken / crouching victim" 等の poses を書かない。lurid・扇情禁止。
5. **R-CREW-NAME:** 個々の刑事名（Yucaitis/O'Hara/その他）をプロンプト・tags に書かない。"anonymous detectives" のみ。
6. **R-NUM:** hedged 数値（100+/118・~$7M・~$3,000・$210M+・~20）を画像に可読で描かない・断定文で書かない。exact-of-record は AE/figures（B）へ。
7. **R-FACE:** 実在人物 likeness ゼロ（§1.1-1）。匿名一般人（"anonymous / generic / non-identifiable person, face turned or in shadow"）は許可。
8. **R-READABLE:** 可読の偽公文書禁止（§1.1-3）。"legible letter / readable report / readable newspaper" を正プロンプトに書かない。
9. **R-DOCHL:** **dochighlight を作らない・言及しない**（grep で 0 を保つ）。
10. **R-QUOTE:** 捏造引用禁止。verbatim は FACTS_LEDGER §VERIFIED-VERBATIM の9系統のみ・AE（B）の担当。画像に可読の引用を描かない。
11. **R-DATE/時代考証:** 1972–2018 のシカゴ。スマホ・現代車・LED街灯・現代のスカイライン（Trump Tower 等 2009以降の輪郭）を1980年代ビートに混ぜない。

## 1.3 機械ゲート（`build_burge_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
# 匿名・非識別の人物は許可。実在人物の likeness だけを弾く。
BANNED_PORTRAIT = re.compile(
    r"likeness of (a )?(real|specific|named) person|real[- ]person likeness|"
    r"face of (jon )?(burge|wilson|holmes|melvin jones|patterson|hobley|orange|howard|kitchen|"
    r"raba|brzeczek|daley|conroy|goldston|egan|boyle|fitzgerald|lefkow|ryan|emanuel)|"
    r"likeness of (burge|wilson|holmes|patterson|hobley|orange|howard|raba|daley|fitzgerald|lefkow|ryan|emanuel)|"
    r"recognizable (real person|celebrity)|identifiable real person|"
    r"mugshot of (a )?real person|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"burge (convicted|guilty) of torture|torture conviction|punished for (the )?torture|"
    r"(man|person|suspect|prisoner) being (shocked|electrocuted|suffocated|tortured|beaten)|"
    r"handcuffed to (a )?radiator|bag over (a |his )?head|typewriter cover over|"
    r"gun (to|against|in) (a |his )?(head|mouth)|mock execution scene|screaming (face|man)|"
    r"restrained (prisoner|suspect|man)|interrogation in progress|electrodes on (skin|a man)|"
    r"cowering|crouching victim|broken victim pose|"
    r"innocent andrew wilson|wilson was innocent|"
    r"legible (letter|document|report|newspaper|verdict|medical record)|readable (letter|document|report)|"
    r"yucaitis|o'?hara as torturer|dochighlight",
    re.IGNORECASE)
```

> **許容:** "the hand-cranked black box inert on an empty table / an empty interview room as aftermath / a cast-iron radiator in an empty room / a buried letter, its text an unreadable smear / dignified anonymized Black man silhouette, upright, backlit / never charged with torture / convicted of perjury and obstruction / the first police-torture reparations in US history / a schoolbook in morning light"。禁止は「拷問の描写/拘束/装置と人体の同一フレーム」「Burge の拷問有罪化」「非恩赦者の無実一括断定」「サバイバーの惨めな pose」「実在人物 likeness」「可読の偽公文書」「hedged 数値の断定」「dochighlight」。

---

# 2. 台本の語数と尺の確定値（Aが素材点数を積算する根拠）

```
words_total          = 4,696（LOCKED script・fact-locked・R1/R2/R3済み・オーナー帯 4,600–4,750 内）
narration_seconds    = 1,582.1（= 26.37分 @178.1wpm・provisional・FINAL は measured TTS forced-align で上書き）
wpm_used             = 178.1
★HOOK-AUDIO 標準（owner・EP52 継続）: Brian の声が 0:00 から鳴る（silent runway なし）。
designed_gap_seconds = 199.9（幕転換の息・AEカード下の music hold・earned breaths ≤3・OST 着地。
                       finished/speech 比 ≈1.13 ∈ 実測 1.04–1.30。check_padding を通る設計ギャップ＝dead air でない）
total_seconds        = 1,791.0（narration 1582.1 + gaps 199.9 + endcard 9.0）= 29:51（band 1740–1860 内）
durationInFrames     = 53,730（provisional・fps30 = 1791×30・VO onset 0.0）
mean_shot            = 3.166秒/カット（picture 1782.0 / 563 cuts）
視覚 acts             = 4（+ HOOK/OPENING/ENDING は別区）
Act 語数配分（provisional）: COLD+OPENING ~330 / ACT1 ~890 / ACT2 ~1,270（engine・最密）/
                            ACT3 ~1,020 / ACT4 ~1,180（climax・cascade・最密②）/ ENDING ~300
```

**Aにとっての意味は1つ:** > **総カット 563 / distinct 487 / 初出 86.50% = still 210 + factory 235 + motion 42。**（§3 で積算）

> **注意（命名差）:** 視覚 act は **0=HOOK/OPENING, 1=ACT I, 2=ACT II, 3=ACT III, 4=ACT IV, 5=ENDING**（6値）。**still は 210 本の固有プロンプトを持つ**ため、still の資産 ID は **S001..S210**（1プロンプト＝1枚）。`covers_scene_id` は still 資産 ID 空間（S001..S210）を指す（§7.3）。

---

# 3. ★素材構成の確定値（この値で調達する・勝手に変えない）

## 3.1 内訳（★勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **210枚** | 244カット | 1.162回(≤2) | **210本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **235本** | 235カット | **各1回(1)** | 在庫11,000本超＋stock から選抜（§7）・全点目視・EP39〜54 と sha256 被りゼロ |
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

> **本編サムネの背景 anchor は body 210枚から4枚を `also_thumb:true` で流用選抜**（§4.3a）。**emotive-face（前景の顔）は §5.12 の thumb_face 3枚**（CTR §4A・B が `BurgeThumbnails.tsx` で face＋hook text を合成）。**role=thumb / still_thumb を作らない。**

## 3.2 幕別配分（★still は確定・factory/i2v は目安。合計だけが確定）

| 区間(act) | still（S番号・確定） | factory（目安） | i2v（確定合計42） | thumb anchor |
|---|---|---|---|---|
| HOOK+OPENING (0) | **15**（S001–S015） | 12 | 3（M01–M03） | S001 |
| ACT1「The Commander」(1) | **42**（S016–S057） | 44 | 8（M04–M11） | — |
| ACT2「The Screams Nobody Heard」(2)（engine・最密） | **50**（S058–S107） | 40 | 9（M12–M20） | S066 |
| ACT3「The Clock Runs Out」(3) | **42**（S108–S149） | 48 | 8（M21–M28） | S128 |
| ACT4「Lying Under Oath」(4)（climax・最密②） | **46**（S150–S195） | 44 | 10（M29–M38） | S186 |
| ENDING (5) | **15**（S196–S210） | 14 | 4（M39–M42） | — |
| 繋ぎ（covers_scene_id:null） | — | 33 | — | — |
| **合計** | **210** | **235** | **42** | **4** |

> **still の per-act 数（15/42/50/42/46/15＝210）は確定**（§5 の motif ライブラリがこの配分で組まれている）。ACT2（無視された警報の engine）が最厚50、ACT4（perjury gambit → reparations cascade）は climax で46＋motion 最多10。**幕別の factory/i2v 内訳は目安値**（合計 235 / 42 のみ確定）。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 563 = still 244 + factory 235 + i2v 84
[2] 平均ショット長 = picture 1782.0 / 563 = 3.166秒/カット  ✓ (≤7.0)
[3] 静止画占有率(check_animation_mix) = 244/563 = 43.34%  ✓ ≤45%（余裕 1.66%pt）
[4] motion coverage = (235+84)/563 = 319/563 = 56.66%     ✓ ≥45%
[5] per-asset 上限: still 244/210=1.162(≤2) / factory 235/235=1.0(≤1) / motion 84/42=2.0(≤2)  ✓
[6] first-use share = 487/563 = 0.8650                    ✓ ≥0.70
[7] avg uses/source = 563/487 = 1.156                     ✓ ≤1.4（EP49 は 1.8 で flag された）
[8] factory 下限 = 1782/30 = 59.4 → ≥60本。設計値 235本 ✓（still-share≤0.45 を守る）
```

> **[3] の余裕は 1.66%pt。** still が210本を割ったら §6.3 の再生成で回復させ、**still-cut 244 を増やさない**（B側の shotlist が244で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-055-burge/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `burge_assets.v1`（固定文字列）
**生産者:** `scripts/build_burge_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を一字一致。** role enum は **`body | i2v_source | thumb_face | reject` のみ**。also_thumb は body still **ちょうど4枚**。thumb_face は **ちょうど3枚**。overlay は **ちょうど30本**。

## 4.1 スキーマ（`burge_assets.v1`）

```jsonc
{
  "schema_version": "burge_assets.v1",
  "episode_id": "PD-2026-055-burge",
  "slug": "burge",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_burge_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 210,        // ==210
    "still_i2v_source": 42,   // ==42
    "motion": 42,             // ==42
    "factory": 235,           // ==235
    "overlay": 30,            // ==30（distinct 素材に数えない）
    "thumb_face": 3           // ==3（thumbnail 専用・distinct/cuts に数えない）
  },
  "stills":  [ /* §4.3: body 210 (BUR-S001..S210) + i2v_source 42 (BUR-MS01..MS42) + thumb_face 3 (BUR-T01..T03) */ ],
  "motion":  [ /* §4.5: BUR-M01..M42 全42本・public_path 必須（★非空） */ ],
  "factory": [ /* §4.4: 235本・public_path 必須（★非空・EP45事故回避の核心） */ ],
  "overlay": [ /* §4.6: 30本 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例・★depth_path なし）

```jsonc
{
  "asset_id": "BUR-S001",                 // body: ^BUR-S\d{3}$（001..210）/ i2v種: ^BUR-MS\d{2}$ / thumb: ^BUR-T\d{2}$
  "scene_id": "S001",                     // still 資産 ID 空間（§5.9 のプロンプト行に対応・S001..S210）
  "role": "body",                         // body|i2v_source|thumb_face|reject
  "also_thumb": false,                    // body から4枚だけ true（§4.3a・追加生成しない）
  "act": 0,                               // 0=HOOK/OPENING, 1..4=ACT I..IV, 5=ENDING
  "path": "H:/pd-media/assets/ai/burge/S001.png",
  "public_path": "burge/img/S001.png",    // role=="body" のみ非null / i2v種・thumb_face は null
  "width": 3840, "height": 2160,          // 長辺>=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 21.0,
  "tags": ["typed_letter","fluorescent_green_edge","buried","symbolic","no_face","no_readable_text"],
  "caption_hint": "a typed letter and envelope on a desk under a single cold fluorescent green-gray edge of light, the text blurred into an unreadable smear, the alarm that was buried, no person, no readable text",
  "seed": 0, "model": "juggernautXL_ragnarokBy",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
         "has_identifiable_real_person": false, "has_human_body": false,
         "has_identifiable_face": false, "has_torture_or_restraint": false, "notes": ""}
  // ★depth_path は無い（本作は depth treatment 不使用・§6.4）。
  // ★reject トリガは has_readable_text / has_identifiable_real_person / has_torture_or_restraint のみ。
  //   匿名人体（has_human_body:true）は reject しない。
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="burge_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 210 / i2v_source 42 / motion 42 / factory 235 / overlay 30 / thumb_face 3）に**一致**
3. 全 `path`/`public_path` がディスクに実在（**depth_path は要求しない**）
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `public_path` が非null かつ実在。`role=="i2v_source"`/`role=="thumb_face"` は `public_path==null`
7. **★reject 条件:** `qc.has_readable_text==true` **または** `qc.has_identifiable_real_person==true` **または** `qc.has_torture_or_restraint==true` は `role=="reject"`。**`qc.has_human_body==true` は reject 条件ではない**（匿名人体は可）。`qc.has_identifiable_face` は「実在人物として識別可能な顔」を意味する（匿名・非識別の顔は可）。H シリーズ（§5.11）・thumb_face（§5.12）は `has_human_body:true`/`has_identifiable_real_person:false`/`has_readable_text:false`/`has_torture_or_restraint:false`
8. `role=="i2v_source"` は `role=="body"`/`role=="thumb_face"` と**同一 asset_id を共有しない**（i2v_source は `^BUR-MS\d{2}$` / thumb_face は `^BUR-T\d{2}$`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39〜EP54 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど4**、かつ `scene_id` 集合が §4.3a の4枚集合と完全一致（**CODEX_B と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|thumb_face|reject のみ）
16. `overlay` 配列長が**ちょうど30**
17. ★**`factory` 配列長==235 かつ全エントリ `public_path` が非空**（EP45 事故回避）
18. ★**`motion` 配列長==42 かつ全エントリ `public_path` が非空**（同上）
19. **★どの still/motion にも `depth_path` キーを要求しない・生成しない**（depth treatment 不使用・§6.4）

`--reuse-feasibility` では §3.3 [5][6][7][8] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 210枚（S001..S210）= §5.9 の210プロンプトの生成物。各1枚。
2. i2v_source 42枚（MS01..MS42 / 種画像 M01_src..M42_src）= §8.1a の42種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. thumb_face 3枚（T01..T03 / T01_face..T03_face）= §5.12 の3プロンプトの生成物。public_path==null。
4. also_thumb : body のうち §4.3a の4枚に true（追加生成しない）
5. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

### 4.3a ★also_thumb 集合（ちょうど4枚・CODEX_B と一字一致必須）

```
{ BUR-S001 (the typed letter under one fluorescent green-gray edge — the hook signature),
  BUR-S066 (the hand-cranked black box, inert in shadow on an empty table — the object),
  BUR-S128 (the institutional clock, hands lost in shadow, time running out — the limitations wall),
  BUR-S186 (an open schoolbook on a classroom desk in curriculum-morning light — the payoff) }
```

> ★この4集合は §5 の該当 S番号に必ず該当 motif を置くこと（§5 の motif ライブラリで anchor 指定済み）。**前景の emotive face は §5.12 の thumb_face（T01–T03）＝これらは背景 anchor。**

## 4.4 ★`factory[]` 全235エントリ（★必ず実体化・public_path 非空。EP45事故回避の核心）

> `select_burge_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id）/`path`（`H:/pd-media/assets/factory/...` or `H:/pd-media/assets/stock/...`）/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`origin`(`factory`|`stock`)/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。** 各 public_path は `burge/factory/F0NN_<subtype>.mp4`。`type:"backgrounds"`, `kind:"video"`。**subtype の `_02`/`_03` は「同一検索テーマの別クリップ」の意で、別 sha256・別素材（同一ファイルの重複ではない）。**

```jsonc
// HOOK+OPENING (act 0) — 12
{ "public_path":"burge/factory/F001_sodium_street_wet_night.mp4", "act":0, "covers_scene_id":"S005", "subtype":"sodium_street_wet_night" }
{ "public_path":"burge/factory/F002_records_archive_shelves_dim.mp4", "act":0, "covers_scene_id":"S008", "subtype":"records_archive_shelves_dim" }
{ "public_path":"burge/factory/F003_el_train_night_pass.mp4", "act":0, "covers_scene_id":null, "subtype":"el_train_night_pass" }
{ "public_path":"burge/factory/F004_police_station_exterior_night.mp4", "act":0, "covers_scene_id":null, "subtype":"police_station_exterior_night" }
{ "public_path":"burge/factory/F005_fluorescent_office_dim.mp4", "act":0, "covers_scene_id":null, "subtype":"fluorescent_office_dim" }
{ "public_path":"burge/factory/F006_file_cabinet_room_dim.mp4", "act":0, "covers_scene_id":null, "subtype":"file_cabinet_room_dim" }
{ "public_path":"burge/factory/F007_dark_institutional_corridor.mp4", "act":0, "covers_scene_id":null, "subtype":"dark_institutional_corridor" }
{ "public_path":"burge/factory/F008_city_skyline_night_grain.mp4", "act":0, "covers_scene_id":null, "subtype":"city_skyline_night_grain" }
{ "public_path":"burge/factory/F009_hospital_corridor_dim.mp4", "act":0, "covers_scene_id":null, "subtype":"hospital_corridor_dim" }
{ "public_path":"burge/factory/F010_sodium_street_wet_night_02.mp4", "act":0, "covers_scene_id":null, "subtype":"sodium_street_wet_night_02" }
{ "public_path":"burge/factory/F011_records_archive_shelves_dim_02.mp4", "act":0, "covers_scene_id":null, "subtype":"records_archive_shelves_dim_02" }
{ "public_path":"burge/factory/F012_jail_exterior_wall_night.mp4", "act":0, "covers_scene_id":null, "subtype":"jail_exterior_wall_night" }
// ACT1 The Commander (act 1) — 44
{ "public_path":"burge/factory/F013_brick_bungalow_street_day.mp4", "act":1, "covers_scene_id":"S016", "subtype":"brick_bungalow_street_day" }
{ "public_path":"burge/factory/F014_steel_mill_smokestacks_dusk.mp4", "act":1, "covers_scene_id":"S017", "subtype":"steel_mill_smokestacks_dusk" }
{ "public_path":"burge/factory/F015_vintage_city_traffic_1970s_look.mp4", "act":1, "covers_scene_id":null, "subtype":"vintage_city_traffic_1970s_look" }
{ "public_path":"burge/factory/F016_precinct_hallway_dim.mp4", "act":1, "covers_scene_id":"S030", "subtype":"precinct_hallway_dim" }
{ "public_path":"burge/factory/F017_desk_lamp_paperwork_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"desk_lamp_paperwork_dim" }
{ "public_path":"burge/factory/F018_typewriter_on_desk_dim.mp4", "act":1, "covers_scene_id":"S040", "subtype":"typewriter_on_desk_dim" }
{ "public_path":"burge/factory/F019_old_radiator_empty_room.mp4", "act":1, "covers_scene_id":"S042", "subtype":"old_radiator_empty_room" }
{ "public_path":"burge/factory/F020_city_hall_facade_day.mp4", "act":1, "covers_scene_id":null, "subtype":"city_hall_facade_day" }
{ "public_path":"burge/factory/F021_lake_michigan_grey_water.mp4", "act":1, "covers_scene_id":null, "subtype":"lake_michigan_grey_water" }
{ "public_path":"burge/factory/F022_freight_yard_dusk.mp4", "act":1, "covers_scene_id":null, "subtype":"freight_yard_dusk" }
{ "public_path":"burge/factory/F023_brick_alley_dusk.mp4", "act":1, "covers_scene_id":null, "subtype":"brick_alley_dusk" }
{ "public_path":"burge/factory/F024_water_tower_silhouette_dusk.mp4", "act":1, "covers_scene_id":null, "subtype":"water_tower_silhouette_dusk" }
{ "public_path":"burge/factory/F025_corner_tavern_neon_night.mp4", "act":1, "covers_scene_id":null, "subtype":"corner_tavern_neon_night" }
{ "public_path":"burge/factory/F026_snowy_street_night.mp4", "act":1, "covers_scene_id":null, "subtype":"snowy_street_night" }
{ "public_path":"burge/factory/F027_police_lights_night_distant.mp4", "act":1, "covers_scene_id":null, "subtype":"police_lights_night_distant" }
{ "public_path":"burge/factory/F028_station_house_exterior_day.mp4", "act":1, "covers_scene_id":null, "subtype":"station_house_exterior_day" }
{ "public_path":"burge/factory/F029_industrial_interior_dark.mp4", "act":1, "covers_scene_id":null, "subtype":"industrial_interior_dark" }
{ "public_path":"burge/factory/F030_church_steeple_south_side.mp4", "act":1, "covers_scene_id":null, "subtype":"church_steeple_south_side" }
{ "public_path":"burge/factory/F031_empty_playground_dusk.mp4", "act":1, "covers_scene_id":null, "subtype":"empty_playground_dusk" }
{ "public_path":"burge/factory/F032_chicago_river_bridge_fog.mp4", "act":1, "covers_scene_id":null, "subtype":"chicago_river_bridge_fog" }
{ "public_path":"burge/factory/F033_vintage_squad_car_static_night.mp4", "act":1, "covers_scene_id":null, "subtype":"vintage_squad_car_static_night" }
{ "public_path":"burge/factory/F034_phone_booth_night.mp4", "act":1, "covers_scene_id":null, "subtype":"phone_booth_night" }
{ "public_path":"burge/factory/F035_medal_ribbon_macro_dim.mp4", "act":1, "covers_scene_id":"S022", "subtype":"medal_ribbon_macro_dim" }
{ "public_path":"burge/factory/F036_fluorescent_tube_flicker.mp4", "act":1, "covers_scene_id":null, "subtype":"fluorescent_tube_flicker" }
{ "public_path":"burge/factory/F037_steam_pipe_basement.mp4", "act":1, "covers_scene_id":null, "subtype":"steam_pipe_basement" }
{ "public_path":"burge/factory/F038_interview_room_empty_dim.mp4", "act":1, "covers_scene_id":"S036", "subtype":"interview_room_empty_dim" }
{ "public_path":"burge/factory/F039_brick_bungalow_street_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"brick_bungalow_street_day_02" }
{ "public_path":"burge/factory/F040_steel_mill_smokestacks_dusk_02.mp4", "act":1, "covers_scene_id":null, "subtype":"steel_mill_smokestacks_dusk_02" }
{ "public_path":"burge/factory/F041_precinct_hallway_dim_02.mp4", "act":1, "covers_scene_id":null, "subtype":"precinct_hallway_dim_02" }
{ "public_path":"burge/factory/F042_desk_lamp_paperwork_dim_02.mp4", "act":1, "covers_scene_id":null, "subtype":"desk_lamp_paperwork_dim_02" }
{ "public_path":"burge/factory/F043_typewriter_on_desk_dim_02.mp4", "act":1, "covers_scene_id":null, "subtype":"typewriter_on_desk_dim_02" }
{ "public_path":"burge/factory/F044_old_radiator_empty_room_02.mp4", "act":1, "covers_scene_id":null, "subtype":"old_radiator_empty_room_02" }
{ "public_path":"burge/factory/F045_el_train_underside_girders.mp4", "act":1, "covers_scene_id":null, "subtype":"el_train_underside_girders" }
{ "public_path":"burge/factory/F046_city_night_aerial_grain.mp4", "act":1, "covers_scene_id":null, "subtype":"city_night_aerial_grain" }
{ "public_path":"burge/factory/F047_vintage_office_blinds_shadow.mp4", "act":1, "covers_scene_id":null, "subtype":"vintage_office_blinds_shadow" }
{ "public_path":"burge/factory/F048_stack_of_case_files_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"stack_of_case_files_dim" }
{ "public_path":"burge/factory/F049_rotary_phone_desk_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"rotary_phone_desk_dim" }
{ "public_path":"burge/factory/F050_south_side_rooftops_dusk.mp4", "act":1, "covers_scene_id":null, "subtype":"south_side_rooftops_dusk" }
{ "public_path":"burge/factory/F051_alley_fire_escape_night.mp4", "act":1, "covers_scene_id":null, "subtype":"alley_fire_escape_night" }
{ "public_path":"burge/factory/F052_street_lamp_halo_fog.mp4", "act":1, "covers_scene_id":null, "subtype":"street_lamp_halo_fog" }
{ "public_path":"burge/factory/F053_interview_room_empty_dim_02.mp4", "act":1, "covers_scene_id":null, "subtype":"interview_room_empty_dim_02" }
{ "public_path":"burge/factory/F054_fluorescent_tube_flicker_02.mp4", "act":1, "covers_scene_id":null, "subtype":"fluorescent_tube_flicker_02" }
{ "public_path":"burge/factory/F055_stack_of_case_files_dim_02.mp4", "act":1, "covers_scene_id":null, "subtype":"stack_of_case_files_dim_02" }
{ "public_path":"burge/factory/F056_snowy_street_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"snowy_street_night_02" }
// ACT2 The Screams Nobody Heard (act 2) — 40
{ "public_path":"burge/factory/F057_county_jail_gate_day.mp4", "act":2, "covers_scene_id":"S060", "subtype":"county_jail_gate_day" }
{ "public_path":"burge/factory/F058_medical_exam_room_empty_dim.mp4", "act":2, "covers_scene_id":"S070", "subtype":"medical_exam_room_empty_dim" }
{ "public_path":"burge/factory/F059_envelope_on_desk_macro.mp4", "act":2, "covers_scene_id":"S074", "subtype":"envelope_on_desk_macro" }
{ "public_path":"burge/factory/F060_mailbox_street_night.mp4", "act":2, "covers_scene_id":"S090", "subtype":"mailbox_street_night" }
{ "public_path":"burge/factory/F061_newspaper_press_rolls.mp4", "act":2, "covers_scene_id":"S094", "subtype":"newspaper_press_rolls" }
{ "public_path":"burge/factory/F062_newsroom_desk_lamp_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"newsroom_desk_lamp_dim" }
{ "public_path":"burge/factory/F063_typewriter_keys_macro.mp4", "act":2, "covers_scene_id":null, "subtype":"typewriter_keys_macro" }
{ "public_path":"burge/factory/F064_courtroom_empty_wood_benches.mp4", "act":2, "covers_scene_id":"S082", "subtype":"courtroom_empty_wood_benches" }
{ "public_path":"burge/factory/F065_courthouse_columns_stone.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_columns_stone" }
{ "public_path":"burge/factory/F066_archive_boxes_stacks_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"archive_boxes_stacks_dim" }
{ "public_path":"burge/factory/F067_microfilm_reader_glow_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"microfilm_reader_glow_dim" }
{ "public_path":"burge/factory/F068_radiator_iron_ribs_macro.mp4", "act":2, "covers_scene_id":null, "subtype":"radiator_iron_ribs_macro" }
{ "public_path":"burge/factory/F069_steam_rising_pipe_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"steam_rising_pipe_dim" }
{ "public_path":"burge/factory/F070_city_hall_night_windows.mp4", "act":2, "covers_scene_id":null, "subtype":"city_hall_night_windows" }
{ "public_path":"burge/factory/F071_precinct_window_night_rain.mp4", "act":2, "covers_scene_id":null, "subtype":"precinct_window_night_rain" }
{ "public_path":"burge/factory/F072_hospital_hall_gurney_empty.mp4", "act":2, "covers_scene_id":null, "subtype":"hospital_hall_gurney_empty" }
{ "public_path":"burge/factory/F073_police_memorial_flowers_day.mp4", "act":2, "covers_scene_id":"S058", "subtype":"police_memorial_flowers_day" }
{ "public_path":"burge/factory/F074_winter_funeral_sky_grey.mp4", "act":2, "covers_scene_id":null, "subtype":"winter_funeral_sky_grey" }
{ "public_path":"burge/factory/F075_letter_paper_macro_blur.mp4", "act":2, "covers_scene_id":null, "subtype":"letter_paper_macro_blur" }
{ "public_path":"burge/factory/F076_filing_drawer_closing_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"filing_drawer_closing_dim" }
{ "public_path":"burge/factory/F077_printing_press_room_02.mp4", "act":2, "covers_scene_id":null, "subtype":"printing_press_room_02" }
{ "public_path":"burge/factory/F078_newsstand_street_1990s_look.mp4", "act":2, "covers_scene_id":null, "subtype":"newsstand_street_1990s_look" }
{ "public_path":"burge/factory/F079_office_blinds_night_slats.mp4", "act":2, "covers_scene_id":null, "subtype":"office_blinds_night_slats" }
{ "public_path":"burge/factory/F080_courtroom_empty_wood_benches_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courtroom_empty_wood_benches_02" }
{ "public_path":"burge/factory/F081_county_jail_gate_day_02.mp4", "act":2, "covers_scene_id":null, "subtype":"county_jail_gate_day_02" }
{ "public_path":"burge/factory/F082_medical_exam_room_empty_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"medical_exam_room_empty_dim_02" }
{ "public_path":"burge/factory/F083_envelope_on_desk_macro_02.mp4", "act":2, "covers_scene_id":null, "subtype":"envelope_on_desk_macro_02" }
{ "public_path":"burge/factory/F084_mailbox_street_night_02.mp4", "act":2, "covers_scene_id":null, "subtype":"mailbox_street_night_02" }
{ "public_path":"burge/factory/F085_typewriter_keys_macro_02.mp4", "act":2, "covers_scene_id":null, "subtype":"typewriter_keys_macro_02" }
{ "public_path":"burge/factory/F086_archive_boxes_stacks_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"archive_boxes_stacks_dim_02" }
{ "public_path":"burge/factory/F087_radiator_iron_ribs_macro_02.mp4", "act":2, "covers_scene_id":null, "subtype":"radiator_iron_ribs_macro_02" }
{ "public_path":"burge/factory/F088_city_night_rain_street.mp4", "act":2, "covers_scene_id":null, "subtype":"city_night_rain_street" }
{ "public_path":"burge/factory/F089_stone_facade_shadow_pan.mp4", "act":2, "covers_scene_id":null, "subtype":"stone_facade_shadow_pan" }
{ "public_path":"burge/factory/F090_fluorescent_stairwell_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"fluorescent_stairwell_dim" }
{ "public_path":"burge/factory/F091_documents_spread_desk_blur.mp4", "act":2, "covers_scene_id":null, "subtype":"documents_spread_desk_blur" }
{ "public_path":"burge/factory/F092_ink_pen_on_paper_macro_blur.mp4", "act":2, "covers_scene_id":null, "subtype":"ink_pen_on_paper_macro_blur" }
{ "public_path":"burge/factory/F093_el_train_night_window_streaks.mp4", "act":2, "covers_scene_id":null, "subtype":"el_train_night_window_streaks" }
{ "public_path":"burge/factory/F094_police_station_steps_night.mp4", "act":2, "covers_scene_id":null, "subtype":"police_station_steps_night" }
{ "public_path":"burge/factory/F095_winter_lake_ice_grey.mp4", "act":2, "covers_scene_id":null, "subtype":"winter_lake_ice_grey" }
{ "public_path":"burge/factory/F096_office_corridor_frosted_glass.mp4", "act":2, "covers_scene_id":null, "subtype":"office_corridor_frosted_glass" }
// ACT3 The Clock Runs Out (act 3) — 48
{ "public_path":"burge/factory/F097_clock_face_shadow_macro.mp4", "act":3, "covers_scene_id":"S128", "subtype":"clock_face_shadow_macro" }
{ "public_path":"burge/factory/F098_courthouse_clock_tower_dusk.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_clock_tower_dusk" }
{ "public_path":"burge/factory/F099_prison_fence_wire_day_nonsensational.mp4", "act":3, "covers_scene_id":"S112", "subtype":"prison_fence_wire_day_nonsensational" }
{ "public_path":"burge/factory/F100_prison_exterior_wall_day.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_exterior_wall_day" }
{ "public_path":"burge/factory/F101_law_library_shelves_dim.mp4", "act":3, "covers_scene_id":"S118", "subtype":"law_library_shelves_dim" }
{ "public_path":"burge/factory/F102_legal_files_boxes_stacked.mp4", "act":3, "covers_scene_id":null, "subtype":"legal_files_boxes_stacked" }
{ "public_path":"burge/factory/F103_capitol_dome_springfield_day.mp4", "act":3, "covers_scene_id":"S136", "subtype":"capitol_dome_springfield_day" }
{ "public_path":"burge/factory/F104_statehouse_interior_marble.mp4", "act":3, "covers_scene_id":null, "subtype":"statehouse_interior_marble" }
{ "public_path":"burge/factory/F105_lectern_empty_hall_dim.mp4", "act":3, "covers_scene_id":null, "subtype":"lectern_empty_hall_dim" }
{ "public_path":"burge/factory/F106_florida_dock_warm_dusk.mp4", "act":3, "covers_scene_id":"S144", "subtype":"florida_dock_warm_dusk" }
{ "public_path":"burge/factory/F107_marina_boats_sunset.mp4", "act":3, "covers_scene_id":null, "subtype":"marina_boats_sunset" }
{ "public_path":"burge/factory/F108_fishing_boat_wake_warm.mp4", "act":3, "covers_scene_id":null, "subtype":"fishing_boat_wake_warm" }
{ "public_path":"burge/factory/F109_palm_street_florida_day.mp4", "act":3, "covers_scene_id":null, "subtype":"palm_street_florida_day" }
{ "public_path":"burge/factory/F110_winter_chicago_street_snow.mp4", "act":3, "covers_scene_id":null, "subtype":"winter_chicago_street_snow" }
{ "public_path":"burge/factory/F111_prison_visiting_room_empty.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_visiting_room_empty" }
{ "public_path":"burge/factory/F112_cell_block_window_light_nonsensational.mp4", "act":3, "covers_scene_id":null, "subtype":"cell_block_window_light_nonsensational" }
{ "public_path":"burge/factory/F113_court_steps_wide_day.mp4", "act":3, "covers_scene_id":null, "subtype":"court_steps_wide_day" }
{ "public_path":"burge/factory/F114_document_stamp_desk_blur.mp4", "act":3, "covers_scene_id":null, "subtype":"document_stamp_desk_blur" }
{ "public_path":"burge/factory/F115_money_ledger_blur_macro.mp4", "act":3, "covers_scene_id":null, "subtype":"money_ledger_blur_macro" }
{ "public_path":"burge/factory/F116_conference_table_empty_dim.mp4", "act":3, "covers_scene_id":null, "subtype":"conference_table_empty_dim" }
{ "public_path":"burge/factory/F117_deposition_room_empty_chairs.mp4", "act":3, "covers_scene_id":null, "subtype":"deposition_room_empty_chairs" }
{ "public_path":"burge/factory/F118_pen_poised_over_paper_macro.mp4", "act":3, "covers_scene_id":"S148", "subtype":"pen_poised_over_paper_macro" }
{ "public_path":"burge/factory/F119_clock_face_shadow_macro_02.mp4", "act":3, "covers_scene_id":null, "subtype":"clock_face_shadow_macro_02" }
{ "public_path":"burge/factory/F120_prison_fence_wire_day_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_fence_wire_day_02" }
{ "public_path":"burge/factory/F121_law_library_shelves_dim_02.mp4", "act":3, "covers_scene_id":null, "subtype":"law_library_shelves_dim_02" }
{ "public_path":"burge/factory/F122_capitol_dome_springfield_day_02.mp4", "act":3, "covers_scene_id":null, "subtype":"capitol_dome_springfield_day_02" }
{ "public_path":"burge/factory/F123_florida_dock_warm_dusk_02.mp4", "act":3, "covers_scene_id":null, "subtype":"florida_dock_warm_dusk_02" }
{ "public_path":"burge/factory/F124_marina_boats_sunset_02.mp4", "act":3, "covers_scene_id":null, "subtype":"marina_boats_sunset_02" }
{ "public_path":"burge/factory/F125_snow_falling_streetlight_night.mp4", "act":3, "covers_scene_id":null, "subtype":"snow_falling_streetlight_night" }
{ "public_path":"burge/factory/F126_gothic_university_hall_day.mp4", "act":3, "covers_scene_id":null, "subtype":"gothic_university_hall_day" }
{ "public_path":"burge/factory/F127_auditorium_empty_seats_dim.mp4", "act":3, "covers_scene_id":null, "subtype":"auditorium_empty_seats_dim" }
{ "public_path":"burge/factory/F128_prison_gate_opening_day.mp4", "act":3, "covers_scene_id":"S140", "subtype":"prison_gate_opening_day" }
{ "public_path":"burge/factory/F129_winter_dawn_city_cold.mp4", "act":3, "covers_scene_id":null, "subtype":"winter_dawn_city_cold" }
{ "public_path":"burge/factory/F130_courthouse_hall_marble_02.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_hall_marble_02" }
{ "public_path":"burge/factory/F131_files_trolley_archive_dim.mp4", "act":3, "covers_scene_id":null, "subtype":"files_trolley_archive_dim" }
{ "public_path":"burge/factory/F132_old_elevator_doors_institutional.mp4", "act":3, "covers_scene_id":null, "subtype":"old_elevator_doors_institutional" }
{ "public_path":"burge/factory/F133_night_highway_south_long_exposure.mp4", "act":3, "covers_scene_id":null, "subtype":"night_highway_south_long_exposure" }
{ "public_path":"burge/factory/F134_warm_gulf_water_glitter.mp4", "act":3, "covers_scene_id":null, "subtype":"warm_gulf_water_glitter" }
{ "public_path":"burge/factory/F135_boat_rope_cleat_macro.mp4", "act":3, "covers_scene_id":null, "subtype":"boat_rope_cleat_macro" }
{ "public_path":"burge/factory/F136_pension_check_envelope_blur.mp4", "act":3, "covers_scene_id":null, "subtype":"pension_check_envelope_blur" }
{ "public_path":"burge/factory/F137_deposition_room_empty_chairs_02.mp4", "act":3, "covers_scene_id":null, "subtype":"deposition_room_empty_chairs_02" }
{ "public_path":"burge/factory/F138_pen_poised_over_paper_macro_02.mp4", "act":3, "covers_scene_id":null, "subtype":"pen_poised_over_paper_macro_02" }
{ "public_path":"burge/factory/F139_court_steps_wide_day_02.mp4", "act":3, "covers_scene_id":null, "subtype":"court_steps_wide_day_02" }
{ "public_path":"burge/factory/F140_statehouse_interior_marble_02.mp4", "act":3, "covers_scene_id":null, "subtype":"statehouse_interior_marble_02" }
{ "public_path":"burge/factory/F141_cell_block_window_light_02.mp4", "act":3, "covers_scene_id":null, "subtype":"cell_block_window_light_02" }
{ "public_path":"burge/factory/F142_prison_gate_opening_day_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_gate_opening_day_02" }
{ "public_path":"burge/factory/F143_winter_dawn_city_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"winter_dawn_city_cold_02" }
{ "public_path":"burge/factory/F144_night_highway_south_long_exposure_02.mp4", "act":3, "covers_scene_id":null, "subtype":"night_highway_south_long_exposure_02" }
// ACT4 Lying Under Oath (act 4) — 44
{ "public_path":"burge/factory/F145_federal_courthouse_plaza_day.mp4", "act":4, "covers_scene_id":"S154", "subtype":"federal_courthouse_plaza_day" }
{ "public_path":"burge/factory/F146_courtroom_corridor_marble.mp4", "act":4, "covers_scene_id":null, "subtype":"courtroom_corridor_marble" }
{ "public_path":"burge/factory/F147_jury_box_empty_wood.mp4", "act":4, "covers_scene_id":"S162", "subtype":"jury_box_empty_wood" }
{ "public_path":"burge/factory/F148_witness_stand_empty_dim.mp4", "act":4, "covers_scene_id":null, "subtype":"witness_stand_empty_dim" }
{ "public_path":"burge/factory/F149_florida_house_drive_day.mp4", "act":4, "covers_scene_id":"S150", "subtype":"florida_house_drive_day" }
{ "public_path":"burge/factory/F150_city_council_chamber_empty.mp4", "act":4, "covers_scene_id":"S178", "subtype":"city_council_chamber_empty" }
{ "public_path":"burge/factory/F151_chicago_flag_wave_day.mp4", "act":4, "covers_scene_id":null, "subtype":"chicago_flag_wave_day" }
{ "public_path":"burge/factory/F152_community_center_exterior_day.mp4", "act":4, "covers_scene_id":"S184", "subtype":"community_center_exterior_day" }
{ "public_path":"burge/factory/F153_school_hallway_empty_morning.mp4", "act":4, "covers_scene_id":null, "subtype":"school_hallway_empty_morning" }
{ "public_path":"burge/factory/F154_classroom_empty_desks_morning.mp4", "act":4, "covers_scene_id":"S186", "subtype":"classroom_empty_desks_morning" }
{ "public_path":"burge/factory/F155_textbook_pages_turn_macro_blur.mp4", "act":4, "covers_scene_id":null, "subtype":"textbook_pages_turn_macro_blur" }
{ "public_path":"burge/factory/F156_morning_light_window_dust.mp4", "act":4, "covers_scene_id":null, "subtype":"morning_light_window_dust" }
{ "public_path":"burge/factory/F157_south_side_morning_street.mp4", "act":4, "covers_scene_id":null, "subtype":"south_side_morning_street" }
{ "public_path":"burge/factory/F158_washington_park_green_day.mp4", "act":4, "covers_scene_id":"S192", "subtype":"washington_park_green_day" }
{ "public_path":"burge/factory/F159_groundbreaking_soil_shovel_macro.mp4", "act":4, "covers_scene_id":null, "subtype":"groundbreaking_soil_shovel_macro" }
{ "public_path":"burge/factory/F160_memorial_flowers_stone_day.mp4", "act":4, "covers_scene_id":null, "subtype":"memorial_flowers_stone_day" }
{ "public_path":"burge/factory/F161_federal_building_columns_dusk.mp4", "act":4, "covers_scene_id":null, "subtype":"federal_building_columns_dusk" }
{ "public_path":"burge/factory/F162_gulf_sunset_dark_water.mp4", "act":4, "covers_scene_id":null, "subtype":"gulf_sunset_dark_water" }
{ "public_path":"burge/factory/F163_empty_marina_dawn_grey.mp4", "act":4, "covers_scene_id":null, "subtype":"empty_marina_dawn_grey" }
{ "public_path":"burge/factory/F164_courtroom_doors_closing_dim.mp4", "act":4, "covers_scene_id":null, "subtype":"courtroom_doors_closing_dim" }
{ "public_path":"burge/factory/F165_marble_staircase_courthouse.mp4", "act":4, "covers_scene_id":null, "subtype":"marble_staircase_courthouse" }
{ "public_path":"burge/factory/F166_document_signature_blur_macro.mp4", "act":4, "covers_scene_id":null, "subtype":"document_signature_blur_macro" }
{ "public_path":"burge/factory/F167_press_microphones_stand_empty.mp4", "act":4, "covers_scene_id":null, "subtype":"press_microphones_stand_empty" }
{ "public_path":"burge/factory/F168_camera_flashes_dark_blur.mp4", "act":4, "covers_scene_id":null, "subtype":"camera_flashes_dark_blur" }
{ "public_path":"burge/factory/F169_city_council_chamber_empty_02.mp4", "act":4, "covers_scene_id":null, "subtype":"city_council_chamber_empty_02" }
{ "public_path":"burge/factory/F170_classroom_empty_desks_morning_02.mp4", "act":4, "covers_scene_id":null, "subtype":"classroom_empty_desks_morning_02" }
{ "public_path":"burge/factory/F171_school_hallway_empty_morning_02.mp4", "act":4, "covers_scene_id":null, "subtype":"school_hallway_empty_morning_02" }
{ "public_path":"burge/factory/F172_textbook_pages_turn_macro_blur_02.mp4", "act":4, "covers_scene_id":null, "subtype":"textbook_pages_turn_macro_blur_02" }
{ "public_path":"burge/factory/F173_federal_courthouse_plaza_day_02.mp4", "act":4, "covers_scene_id":null, "subtype":"federal_courthouse_plaza_day_02" }
{ "public_path":"burge/factory/F174_jury_box_empty_wood_02.mp4", "act":4, "covers_scene_id":null, "subtype":"jury_box_empty_wood_02" }
{ "public_path":"burge/factory/F175_witness_stand_empty_dim_02.mp4", "act":4, "covers_scene_id":null, "subtype":"witness_stand_empty_dim_02" }
{ "public_path":"burge/factory/F176_morning_light_window_dust_02.mp4", "act":4, "covers_scene_id":null, "subtype":"morning_light_window_dust_02" }
{ "public_path":"burge/factory/F177_south_side_morning_street_02.mp4", "act":4, "covers_scene_id":null, "subtype":"south_side_morning_street_02" }
{ "public_path":"burge/factory/F178_washington_park_green_day_02.mp4", "act":4, "covers_scene_id":null, "subtype":"washington_park_green_day_02" }
{ "public_path":"burge/factory/F179_memorial_flowers_stone_day_02.mp4", "act":4, "covers_scene_id":null, "subtype":"memorial_flowers_stone_day_02" }
{ "public_path":"burge/factory/F180_chicago_flag_wave_day_02.mp4", "act":4, "covers_scene_id":null, "subtype":"chicago_flag_wave_day_02" }
{ "public_path":"burge/factory/F181_community_center_exterior_day_02.mp4", "act":4, "covers_scene_id":null, "subtype":"community_center_exterior_day_02" }
{ "public_path":"burge/factory/F182_courtroom_corridor_marble_02.mp4", "act":4, "covers_scene_id":null, "subtype":"courtroom_corridor_marble_02" }
{ "public_path":"burge/factory/F183_document_signature_blur_macro_02.mp4", "act":4, "covers_scene_id":null, "subtype":"document_signature_blur_macro_02" }
{ "public_path":"burge/factory/F184_press_microphones_stand_empty_02.mp4", "act":4, "covers_scene_id":null, "subtype":"press_microphones_stand_empty_02" }
{ "public_path":"burge/factory/F185_marble_staircase_courthouse_02.mp4", "act":4, "covers_scene_id":null, "subtype":"marble_staircase_courthouse_02" }
{ "public_path":"burge/factory/F186_groundbreaking_soil_shovel_macro_02.mp4", "act":4, "covers_scene_id":null, "subtype":"groundbreaking_soil_shovel_macro_02" }
{ "public_path":"burge/factory/F187_federal_building_columns_dusk_02.mp4", "act":4, "covers_scene_id":null, "subtype":"federal_building_columns_dusk_02" }
{ "public_path":"burge/factory/F188_camera_flashes_dark_blur_02.mp4", "act":4, "covers_scene_id":null, "subtype":"camera_flashes_dark_blur_02" }
// ENDING (act 5) — 14
{ "public_path":"burge/factory/F189_open_book_pages_morning_light.mp4", "act":5, "covers_scene_id":"S200", "subtype":"open_book_pages_morning_light" }
{ "public_path":"burge/factory/F190_school_exterior_morning_flag.mp4", "act":5, "covers_scene_id":null, "subtype":"school_exterior_morning_flag" }
{ "public_path":"burge/factory/F191_classroom_windows_light_shaft.mp4", "act":5, "covers_scene_id":"S204", "subtype":"classroom_windows_light_shaft" }
{ "public_path":"burge/factory/F192_dawn_lake_michigan_calm.mp4", "act":5, "covers_scene_id":null, "subtype":"dawn_lake_michigan_calm" }
{ "public_path":"burge/factory/F193_city_dawn_skyline_soft.mp4", "act":5, "covers_scene_id":null, "subtype":"city_dawn_skyline_soft" }
{ "public_path":"burge/factory/F194_letter_paper_macro_light.mp4", "act":5, "covers_scene_id":"S196", "subtype":"letter_paper_macro_light" }
{ "public_path":"burge/factory/F195_quiet_library_shelves_morning.mp4", "act":5, "covers_scene_id":null, "subtype":"quiet_library_shelves_morning" }
{ "public_path":"burge/factory/F196_empty_desks_sunbeam.mp4", "act":5, "covers_scene_id":null, "subtype":"empty_desks_sunbeam" }
{ "public_path":"burge/factory/F197_chalkboard_clean_morning_blur.mp4", "act":5, "covers_scene_id":null, "subtype":"chalkboard_clean_morning_blur" }
{ "public_path":"burge/factory/F198_open_book_pages_morning_light_02.mp4", "act":5, "covers_scene_id":null, "subtype":"open_book_pages_morning_light_02" }
{ "public_path":"burge/factory/F199_dawn_lake_michigan_calm_02.mp4", "act":5, "covers_scene_id":null, "subtype":"dawn_lake_michigan_calm_02" }
{ "public_path":"burge/factory/F200_city_dawn_skyline_soft_02.mp4", "act":5, "covers_scene_id":null, "subtype":"city_dawn_skyline_soft_02" }
{ "public_path":"burge/factory/F201_school_exterior_morning_flag_02.mp4", "act":5, "covers_scene_id":null, "subtype":"school_exterior_morning_flag_02" }
{ "public_path":"burge/factory/F202_classroom_windows_light_shaft_02.mp4", "act":5, "covers_scene_id":null, "subtype":"classroom_windows_light_shaft_02" }
// 繋ぎ connective (covers null・act は最寄り区間に振る) — 33
{ "public_path":"burge/factory/F203_institutional_corridor_pan_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"institutional_corridor_pan_dim" }
{ "public_path":"burge/factory/F204_marble_texture_slow_pan.mp4", "act":2, "covers_scene_id":null, "subtype":"marble_texture_slow_pan" }
{ "public_path":"burge/factory/F205_grey_sky_timelapse_clouds.mp4", "act":1, "covers_scene_id":null, "subtype":"grey_sky_timelapse_clouds" }
{ "public_path":"burge/factory/F206_rain_on_window_night_bokeh.mp4", "act":2, "covers_scene_id":null, "subtype":"rain_on_window_night_bokeh" }
{ "public_path":"burge/factory/F207_river_fog_slow_drift.mp4", "act":1, "covers_scene_id":null, "subtype":"river_fog_slow_drift" }
{ "public_path":"burge/factory/F208_night_traffic_long_exposure.mp4", "act":0, "covers_scene_id":null, "subtype":"night_traffic_long_exposure" }
{ "public_path":"burge/factory/F209_moon_through_clouds_night.mp4", "act":2, "covers_scene_id":null, "subtype":"moon_through_clouds_night" }
{ "public_path":"burge/factory/F210_dust_light_shaft_dark_room.mp4", "act":1, "covers_scene_id":null, "subtype":"dust_light_shaft_dark_room" }
{ "public_path":"burge/factory/F211_brick_wall_texture_shadow.mp4", "act":1, "covers_scene_id":null, "subtype":"brick_wall_texture_shadow" }
{ "public_path":"burge/factory/F212_paper_texture_macro_drift.mp4", "act":2, "covers_scene_id":null, "subtype":"paper_texture_macro_drift" }
{ "public_path":"burge/factory/F213_city_aerial_dusk_slow.mp4", "act":3, "covers_scene_id":null, "subtype":"city_aerial_dusk_slow" }
{ "public_path":"burge/factory/F214_water_reflection_night_lights.mp4", "act":3, "covers_scene_id":null, "subtype":"water_reflection_night_lights" }
{ "public_path":"burge/factory/F215_fog_street_lamp_morning.mp4", "act":3, "covers_scene_id":null, "subtype":"fog_street_lamp_morning" }
{ "public_path":"burge/factory/F216_snow_flurry_dark_sky.mp4", "act":3, "covers_scene_id":null, "subtype":"snow_flurry_dark_sky" }
{ "public_path":"burge/factory/F217_curtain_window_dim_drift.mp4", "act":2, "covers_scene_id":null, "subtype":"curtain_window_dim_drift" }
{ "public_path":"burge/factory/F218_stone_steps_shadow_pan.mp4", "act":2, "covers_scene_id":null, "subtype":"stone_steps_shadow_pan" }
{ "public_path":"burge/factory/F219_wire_fence_bokeh_day.mp4", "act":3, "covers_scene_id":null, "subtype":"wire_fence_bokeh_day" }
{ "public_path":"burge/factory/F220_old_ceiling_fan_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"old_ceiling_fan_dim" }
{ "public_path":"burge/factory/F221_window_blinds_shadow_wall.mp4", "act":2, "covers_scene_id":null, "subtype":"window_blinds_shadow_wall" }
{ "public_path":"burge/factory/F222_street_puddle_reflection_night.mp4", "act":0, "covers_scene_id":null, "subtype":"street_puddle_reflection_night" }
{ "public_path":"burge/factory/F223_industrial_chimney_dusk_smoke.mp4", "act":1, "covers_scene_id":null, "subtype":"industrial_chimney_dusk_smoke" }
{ "public_path":"burge/factory/F224_dark_water_surface_slow.mp4", "act":4, "covers_scene_id":null, "subtype":"dark_water_surface_slow" }
{ "public_path":"burge/factory/F225_sunrise_over_rooftops_soft.mp4", "act":4, "covers_scene_id":null, "subtype":"sunrise_over_rooftops_soft" }
{ "public_path":"burge/factory/F226_flag_shadow_on_wall_day.mp4", "act":4, "covers_scene_id":null, "subtype":"flag_shadow_on_wall_day" }
{ "public_path":"burge/factory/F227_tree_branches_morning_light.mp4", "act":4, "covers_scene_id":null, "subtype":"tree_branches_morning_light" }
{ "public_path":"burge/factory/F228_hallway_light_flicker_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"hallway_light_flicker_dim" }
{ "public_path":"burge/factory/F229_ink_bleed_dark_water_macro.mp4", "act":2, "covers_scene_id":null, "subtype":"ink_bleed_dark_water_macro" }
{ "public_path":"burge/factory/F230_railroad_crossing_night_signal.mp4", "act":1, "covers_scene_id":null, "subtype":"railroad_crossing_night_signal" }
{ "public_path":"burge/factory/F231_park_bench_autumn_empty.mp4", "act":4, "covers_scene_id":null, "subtype":"park_bench_autumn_empty" }
{ "public_path":"burge/factory/F232_grey_sky_timelapse_clouds_02.mp4", "act":3, "covers_scene_id":null, "subtype":"grey_sky_timelapse_clouds_02" }
{ "public_path":"burge/factory/F233_dust_light_shaft_dark_room_02.mp4", "act":2, "covers_scene_id":null, "subtype":"dust_light_shaft_dark_room_02" }
{ "public_path":"burge/factory/F234_sunrise_over_rooftops_soft_02.mp4", "act":5, "covers_scene_id":null, "subtype":"sunrise_over_rooftops_soft_02" }
{ "public_path":"burge/factory/F235_morning_mist_park_trees.mp4", "act":5, "covers_scene_id":null, "subtype":"morning_mist_park_trees" }
```

**検算:** 12 + 44 + 40 + 48 + 44 + 14 + 33 = **235** ✓（act0 12+2繋ぎ=14 / act1 44+8 / act2 40+11 / act3 48+7 / act4 44+5 / act5 14+2 — 繋ぎ33は covers null のまま最寄り act に配置）。全 public_path 非空 ✓（不変条件17）。**暗いクリップは約78本（1/3）まで**・courthouse 昼光・morning light・Florida warm を混ぜる（§7.5）。

## 4.5 ★`motion[]` 全42エントリ（★必ず実体化・public_path 非空）

> エントリ形は §4.1a 準拠 + 動画フィールド。`asset_id ^BUR-M\d{2}$`。`source_still` は §8.1a の種画像、`source_scene_id`=`MS<NN>`。runtime で `sha256`/`width 1280`/`height 720`/`fps 48`/`frames`/`duration_sec`/`qc` を埋める（§8.4）。**空配列を書かない。**

```jsonc
{ "asset_id":"BUR-M01", "source_scene_id":"MS01", "source_still":"H:/pd-media/assets/ai/burge/M01_src.png", "path":"H:/pd-media/assets/ai_video/burge/M01_rife.mp4", "public_path":"burge/motion/M01_rife.mp4", "act":0, "storyboard":"hook", "tags":["letter_under_fluorescent_edge"] }
{ "asset_id":"BUR-M02", "source_scene_id":"MS02", "source_still":"H:/pd-media/assets/ai/burge/M02_src.png", "path":"H:/pd-media/assets/ai_video/burge/M02_rife.mp4", "public_path":"burge/motion/M02_rife.mp4", "act":0, "storyboard":"A0-02", "tags":["drawer_slides_over_letter"] }
{ "asset_id":"BUR-M03", "source_scene_id":"MS03", "source_still":"H:/pd-media/assets/ai/burge/M03_src.png", "path":"H:/pd-media/assets/ai_video/burge/M03_rife.mp4", "public_path":"burge/motion/M03_rife.mp4", "act":0, "storyboard":"A0-03", "tags":["sodium_night_city_breathes"] }
{ "asset_id":"BUR-M04", "source_scene_id":"MS04", "source_still":"H:/pd-media/assets/ai/burge/M04_src.png", "path":"H:/pd-media/assets/ai_video/burge/M04_rife.mp4", "public_path":"burge/motion/M04_rife.mp4", "act":1, "storyboard":"A1-01", "tags":["commander_silhouette_squadroom","H001_anon"] }
{ "asset_id":"BUR-M05", "source_scene_id":"MS05", "source_still":"H:/pd-media/assets/ai/burge/M05_src.png", "path":"H:/pd-media/assets/ai_video/burge/M05_rife.mp4", "public_path":"burge/motion/M05_rife.mp4", "act":1, "storyboard":"A1-02", "tags":["black_box_inert_shadow"] }
{ "asset_id":"BUR-M06", "source_scene_id":"MS06", "source_still":"H:/pd-media/assets/ai/burge/M06_src.png", "path":"H:/pd-media/assets/ai_video/burge/M06_rife.mp4", "public_path":"burge/motion/M06_rife.mp4", "act":1, "storyboard":"A1-03", "tags":["midnight_shift_detectives_backs","H002_anon"] }
{ "asset_id":"BUR-M07", "source_scene_id":"MS07", "source_still":"H:/pd-media/assets/ai/burge/M07_src.png", "path":"H:/pd-media/assets/ai_video/burge/M07_rife.mp4", "public_path":"burge/motion/M07_rife.mp4", "act":1, "storyboard":"A1-04", "tags":["young_mp_silhouette_vietnam_era","H003_anon"] }
{ "asset_id":"BUR-M08", "source_scene_id":"MS08", "source_still":"H:/pd-media/assets/ai/burge/M08_src.png", "path":"H:/pd-media/assets/ai_video/burge/M08_rife.mp4", "public_path":"burge/motion/M08_rife.mp4", "act":1, "storyboard":"A1-05", "tags":["confession_machine_gears_abstract"] }
{ "asset_id":"BUR-M09", "source_scene_id":"MS09", "source_still":"H:/pd-media/assets/ai/burge/M09_src.png", "path":"H:/pd-media/assets/ai_video/burge/M09_rife.mp4", "public_path":"burge/motion/M09_rife.mp4", "act":1, "storyboard":"A1-06", "tags":["dignified_survivor_silhouette_upright","H004_anon"] }
{ "asset_id":"BUR-M10", "source_scene_id":"MS10", "source_still":"H:/pd-media/assets/ai/burge/M10_src.png", "path":"H:/pd-media/assets/ai_video/burge/M10_rife.mp4", "public_path":"burge/motion/M10_rife.mp4", "act":1, "storyboard":"A1-07", "tags":["investigator_hands_typing_report","H005_anon"] }
{ "asset_id":"BUR-M11", "source_scene_id":"MS11", "source_still":"H:/pd-media/assets/ai/burge/M11_src.png", "path":"H:/pd-media/assets/ai_video/burge/M11_rife.mp4", "public_path":"burge/motion/M11_rife.mp4", "act":1, "storyboard":"A1-08", "tags":["radiator_empty_room_steam"] }
{ "asset_id":"BUR-M12", "source_scene_id":"MS12", "source_still":"H:/pd-media/assets/ai/burge/M12_src.png", "path":"H:/pd-media/assets/ai_video/burge/M12_rife.mp4", "public_path":"burge/motion/M12_rife.mp4", "act":2, "storyboard":"A2-01", "tags":["jail_intake_corridor_empty"] }
{ "asset_id":"BUR-M13", "source_scene_id":"MS13", "source_still":"H:/pd-media/assets/ai/burge/M13_src.png", "path":"H:/pd-media/assets/ai_video/burge/M13_rife.mp4", "public_path":"burge/motion/M13_rife.mp4", "act":2, "storyboard":"A2-02", "tags":["doctor_hands_writing_letter","H006_anon"] }
{ "asset_id":"BUR-M14", "source_scene_id":"MS14", "source_still":"H:/pd-media/assets/ai/burge/M14_src.png", "path":"H:/pd-media/assets/ai_video/burge/M14_rife.mp4", "public_path":"burge/motion/M14_rife.mp4", "act":2, "storyboard":"A2-03", "tags":["letter_passed_between_hands","H007_anon"] }
{ "asset_id":"BUR-M15", "source_scene_id":"MS15", "source_still":"H:/pd-media/assets/ai/burge/M15_src.png", "path":"H:/pd-media/assets/ai_video/burge/M15_rife.mp4", "public_path":"burge/motion/M15_rife.mp4", "act":2, "storyboard":"A2-04", "tags":["letter_buried_drawer_closes"] }
{ "asset_id":"BUR-M16", "source_scene_id":"MS16", "source_still":"H:/pd-media/assets/ai/burge/M16_src.png", "path":"H:/pd-media/assets/ai_video/burge/M16_rife.mp4", "public_path":"burge/motion/M16_rife.mp4", "act":2, "storyboard":"A2-05", "tags":["reporter_typing_alone_night","H008_anon"] }
{ "asset_id":"BUR-M17", "source_scene_id":"MS17", "source_still":"H:/pd-media/assets/ai/burge/M17_src.png", "path":"H:/pd-media/assets/ai_video/burge/M17_rife.mp4", "public_path":"burge/motion/M17_rife.mp4", "act":2, "storyboard":"A2-06", "tags":["report_pages_unreadable_smear"] }
{ "asset_id":"BUR-M18", "source_scene_id":"MS18", "source_still":"H:/pd-media/assets/ai/burge/M18_src.png", "path":"H:/pd-media/assets/ai_video/burge/M18_rife.mp4", "public_path":"burge/motion/M18_rife.mp4", "act":2, "storyboard":"A2-07", "tags":["black_box_on_evidence_table_inert"] }
{ "asset_id":"BUR-M19", "source_scene_id":"MS19", "source_still":"H:/pd-media/assets/ai/burge/M19_src.png", "path":"H:/pd-media/assets/ai_video/burge/M19_rife.mp4", "public_path":"burge/motion/M19_rife.mp4", "act":2, "storyboard":"A2-08", "tags":["fired_commander_walks_away_back","H009_anon"] }
{ "asset_id":"BUR-M20", "source_scene_id":"MS20", "source_still":"H:/pd-media/assets/ai/burge/M20_src.png", "path":"H:/pd-media/assets/ai_video/burge/M20_rife.mp4", "public_path":"burge/motion/M20_rife.mp4", "act":2, "storyboard":"A2-09", "tags":["man_walks_to_warm_dock_back","H010_anon"] }
{ "asset_id":"BUR-M21", "source_scene_id":"MS21", "source_still":"H:/pd-media/assets/ai/burge/M21_src.png", "path":"H:/pd-media/assets/ai_video/burge/M21_rife.mp4", "public_path":"burge/motion/M21_rife.mp4", "act":3, "storyboard":"A3-01", "tags":["statute_clock_hands_dissolve"] }
{ "asset_id":"BUR-M22", "source_scene_id":"MS22", "source_still":"H:/pd-media/assets/ai/burge/M22_src.png", "path":"H:/pd-media/assets/ai_video/burge/M22_rife.mp4", "public_path":"burge/motion/M22_rife.mp4", "act":3, "storyboard":"A3-02", "tags":["prison_yard_dignified_backs","H011_anon"] }
{ "asset_id":"BUR-M23", "source_scene_id":"MS23", "source_still":"H:/pd-media/assets/ai/burge/M23_src.png", "path":"H:/pd-media/assets/ai_video/burge/M23_rife.mp4", "public_path":"burge/motion/M23_rife.mp4", "act":3, "storyboard":"A3-03", "tags":["cell_desk_hands_typing_leaflets","H012_anon"] }
{ "asset_id":"BUR-M24", "source_scene_id":"MS24", "source_still":"H:/pd-media/assets/ai/burge/M24_src.png", "path":"H:/pd-media/assets/ai_video/burge/M24_rife.mp4", "public_path":"burge/motion/M24_rife.mp4", "act":3, "storyboard":"A3-04", "tags":["governor_at_podium_back","H013_anon"] }
{ "asset_id":"BUR-M25", "source_scene_id":"MS25", "source_still":"H:/pd-media/assets/ai/burge/M25_src.png", "path":"H:/pd-media/assets/ai_video/burge/M25_rife.mp4", "public_path":"burge/motion/M25_rife.mp4", "act":3, "storyboard":"A3-05", "tags":["pardoned_men_walk_free_cold_light","H014_anon"] }
{ "asset_id":"BUR-M26", "source_scene_id":"MS26", "source_still":"H:/pd-media/assets/ai/burge/M26_src.png", "path":"H:/pd-media/assets/ai_video/burge/M26_rife.mp4", "public_path":"burge/motion/M26_rife.mp4", "act":3, "storyboard":"A3-06", "tags":["report_stack_zero_charges_abstract"] }
{ "asset_id":"BUR-M27", "source_scene_id":"MS27", "source_still":"H:/pd-media/assets/ai/burge/M27_src.png", "path":"H:/pd-media/assets/ai_video/burge/M27_rife.mp4", "public_path":"burge/motion/M27_rife.mp4", "act":3, "storyboard":"A3-07", "tags":["boat_wake_warm_impunity"] }
{ "asset_id":"BUR-M28", "source_scene_id":"MS28", "source_still":"H:/pd-media/assets/ai/burge/M28_src.png", "path":"H:/pd-media/assets/ai_video/burge/M28_rife.mp4", "public_path":"burge/motion/M28_rife.mp4", "act":3, "storyboard":"A3-08", "tags":["oath_page_pen_poised"] }
{ "asset_id":"BUR-M29", "source_scene_id":"MS29", "source_still":"H:/pd-media/assets/ai/burge/M29_src.png", "path":"H:/pd-media/assets/ai_video/burge/M29_rife.mp4", "public_path":"burge/motion/M29_rife.mp4", "act":4, "storyboard":"A4-01", "tags":["signature_lands_smear_macro"] }
{ "asset_id":"BUR-M30", "source_scene_id":"MS30", "source_still":"H:/pd-media/assets/ai/burge/M30_src.png", "path":"H:/pd-media/assets/ai_video/burge/M30_rife.mp4", "public_path":"burge/motion/M30_rife.mp4", "act":4, "storyboard":"A4-02", "tags":["courthouse_plaza_camera_flashes_blur"] }
{ "asset_id":"BUR-M31", "source_scene_id":"MS31", "source_still":"H:/pd-media/assets/ai/burge/M31_src.png", "path":"H:/pd-media/assets/ai_video/burge/M31_rife.mp4", "public_path":"burge/motion/M31_rife.mp4", "act":4, "storyboard":"A4-03", "tags":["limitations_wall_vs_fresh_lie_faultsplit"] }
{ "asset_id":"BUR-M32", "source_scene_id":"MS32", "source_still":"H:/pd-media/assets/ai/burge/M32_src.png", "path":"H:/pd-media/assets/ai_video/burge/M32_rife.mp4", "public_path":"burge/motion/M32_rife.mp4", "act":4, "storyboard":"A4-04", "tags":["verdict_doors_open_light"] }
{ "asset_id":"BUR-M33", "source_scene_id":"MS33", "source_still":"H:/pd-media/assets/ai/burge/M33_src.png", "path":"H:/pd-media/assets/ai_video/burge/M33_rife.mp4", "public_path":"burge/motion/M33_rife.mp4", "act":4, "storyboard":"A4-05", "tags":["survivor_testifies_dignified_silhouette","H015_anon"] }
{ "asset_id":"BUR-M34", "source_scene_id":"MS34", "source_still":"H:/pd-media/assets/ai/burge/M34_src.png", "path":"H:/pd-media/assets/ai_video/burge/M34_rife.mp4", "public_path":"burge/motion/M34_rife.mp4", "act":4, "storyboard":"A4-06", "tags":["gallery_backs_rise_verdict","H016_anon"] }
{ "asset_id":"BUR-M35", "source_scene_id":"MS35", "source_still":"H:/pd-media/assets/ai/burge/M35_src.png", "path":"H:/pd-media/assets/ai_video/burge/M35_rife.mp4", "public_path":"burge/motion/M35_rife.mp4", "act":4, "storyboard":"A4-07", "tags":["pension_envelope_drift_abstract"] }
{ "asset_id":"BUR-M36", "source_scene_id":"MS36", "source_still":"H:/pd-media/assets/ai/burge/M36_src.png", "path":"H:/pd-media/assets/ai_video/burge/M36_rife.mp4", "public_path":"burge/motion/M36_rife.mp4", "act":4, "storyboard":"A4-08", "tags":["council_chamber_survivors_watch_backs","H017_anon"] }
{ "asset_id":"BUR-M37", "source_scene_id":"MS37", "source_still":"H:/pd-media/assets/ai/burge/M37_src.png", "path":"H:/pd-media/assets/ai_video/burge/M37_rife.mp4", "public_path":"burge/motion/M37_rife.mp4", "act":4, "storyboard":"A4-09", "tags":["teacher_before_class_back_morning","H018_anon"] }
{ "asset_id":"BUR-M38", "source_scene_id":"MS38", "source_still":"H:/pd-media/assets/ai/burge/M38_src.png", "path":"H:/pd-media/assets/ai_video/burge/M38_rife.mp4", "public_path":"burge/motion/M38_rife.mp4", "act":4, "storyboard":"A4-10", "tags":["schoolbook_page_turns_morning_light"] }
{ "asset_id":"BUR-M39", "source_scene_id":"MS39", "source_still":"H:/pd-media/assets/ai/burge/M39_src.png", "path":"H:/pd-media/assets/ai_video/burge/M39_rife.mp4", "public_path":"burge/motion/M39_rife.mp4", "act":5, "storyboard":"A5-01", "tags":["drawer_opens_letter_light"] }
{ "asset_id":"BUR-M40", "source_scene_id":"MS40", "source_still":"H:/pd-media/assets/ai/burge/M40_src.png", "path":"H:/pd-media/assets/ai_video/burge/M40_rife.mp4", "public_path":"burge/motion/M40_rife.mp4", "act":5, "storyboard":"A5-02", "tags":["letter_dissolves_to_textbook_page"] }
{ "asset_id":"BUR-M41", "source_scene_id":"MS41", "source_still":"H:/pd-media/assets/ai/burge/M41_src.png", "path":"H:/pd-media/assets/ai_video/burge/M41_rife.mp4", "public_path":"burge/motion/M41_rife.mp4", "act":5, "storyboard":"A5-03", "tags":["classroom_morning_dust_light"] }
{ "asset_id":"BUR-M42", "source_scene_id":"MS42", "source_still":"H:/pd-media/assets/ai/burge/M42_src.png", "path":"H:/pd-media/assets/ai_video/burge/M42_rife.mp4", "public_path":"burge/motion/M42_rife.mp4", "act":5, "storyboard":"A5-04", "tags":["city_dawn_quiet_close"] }
```

**検算:** 42エントリ ✓・全 public_path 非空 ✓（不変条件18）・`^BUR-M\d{2}$` ✓・**★H001–H018（匿名人物・18本）は M04/M06/M07/M09/M10/M13/M14/M16/M19/M20/M22/M23/M24/M25/M33/M34/M36/M37 の内数 ✓**（＝42 motion のうち 18 が人物・84 cuts のうち最大36が人物）。残り24本が抽象/象徴。**★どの motion にも「装置＋人体の同一フレーム」「拘束」「苦悶」なし（R-TORTURE-DEPICT）。**

## 4.6 `overlay[]` 30エントリ（distinct 素材に数えない・15 particle / 10 light / 5 vfx）

```jsonc
{ "public_path":"burge/overlay/P01_fluorescent_room_dust.mp4", "type":"particle_assets", "subtype":"fluorescent_room_dust", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P02_archive_dust_cold.mp4", "type":"particle_assets", "subtype":"archive_dust_cold", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P03_interview_room_dust_drift.mp4", "type":"particle_assets", "subtype":"interview_room_dust_drift", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P04_night_air_sodium_drift.mp4", "type":"particle_assets", "subtype":"night_air_sodium_drift", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P05_fine_grain_dust.mp4", "type":"particle_assets", "subtype":"fine_grain_dust", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P06_paper_fiber_drift.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P07_courtroom_dust_shaft.mp4", "type":"particle_assets", "subtype":"courtroom_dust_shaft", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P08_snow_drift_slow_dark.mp4", "type":"particle_assets", "subtype":"snow_drift_slow_dark", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P09_steam_wisp_dim.mp4", "type":"particle_assets", "subtype":"steam_wisp_dim", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P10_morning_dust_warm.mp4", "type":"particle_assets", "subtype":"morning_dust_warm", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P11_fluorescent_room_dust_02.mp4", "type":"particle_assets", "subtype":"fluorescent_room_dust_02", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P12_archive_dust_cold_02.mp4", "type":"particle_assets", "subtype":"archive_dust_cold_02", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P13_night_air_sodium_drift_02.mp4", "type":"particle_assets", "subtype":"night_air_sodium_drift_02", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P14_paper_fiber_drift_02.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift_02", "blend_hint":"screen" }
{ "public_path":"burge/overlay/P15_morning_dust_warm_02.mp4", "type":"particle_assets", "subtype":"morning_dust_warm_02", "blend_hint":"screen" }
{ "public_path":"burge/overlay/L01_fluorescent_green_shaft.mp4", "type":"light_assets", "subtype":"fluorescent_green_shaft", "blend_hint":"screen" }
{ "public_path":"burge/overlay/L02_cold_window_light_bar.mp4", "type":"light_assets", "subtype":"cold_window_light_bar", "blend_hint":"screen" }
{ "public_path":"burge/overlay/L03_single_desk_lamp_glow.mp4", "type":"light_assets", "subtype":"single_desk_lamp_glow", "blend_hint":"screen" }
{ "public_path":"burge/overlay/L04_sodium_edge_glow_night.mp4", "type":"light_assets", "subtype":"sodium_edge_glow_night", "blend_hint":"screen" }
{ "public_path":"burge/overlay/L05_curriculum_morning_glow.mp4", "type":"light_assets", "subtype":"curriculum_morning_glow", "blend_hint":"screen" }
{ "public_path":"burge/overlay/L06_fluorescent_flicker_soft.mp4", "type":"light_assets", "subtype":"fluorescent_flicker_soft", "blend_hint":"screen" }
{ "public_path":"burge/overlay/L07_cold_key_light_sweep.mp4", "type":"light_assets", "subtype":"cold_key_light_sweep", "blend_hint":"screen" }
{ "public_path":"burge/overlay/L08_fluorescent_green_shaft_02.mp4", "type":"light_assets", "subtype":"fluorescent_green_shaft_02", "blend_hint":"screen" }
{ "public_path":"burge/overlay/L09_curriculum_morning_glow_02.mp4", "type":"light_assets", "subtype":"curriculum_morning_glow_02", "blend_hint":"screen" }
{ "public_path":"burge/overlay/L10_sodium_edge_glow_night_02.mp4", "type":"light_assets", "subtype":"sodium_edge_glow_night_02", "blend_hint":"screen" }
{ "public_path":"burge/overlay/V01_film_grain_fine.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine", "blend_hint":"overlay" }
{ "public_path":"burge/overlay/V02_cold_light_noise.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise", "blend_hint":"screen" }
{ "public_path":"burge/overlay/V03_film_grain_fine_02.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine_02", "blend_hint":"overlay" }
{ "public_path":"burge/overlay/V04_cold_light_noise_02.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise_02", "blend_hint":"screen" }
{ "public_path":"burge/overlay/V05_green_glitch_min.mp4", "type":"vfx_overlays", "subtype":"green_glitch_min", "blend_hint":"screen" }
```

**検算:** 15 + 10 + 5 = 30 ✓。runtime で `asset_id`/`path`/`sha256`/`license`/`eyeballed_content`/`qc` を埋める。**overlay は `cuts[].src` に出さない。★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない（DESIGN §1・screen-wash ≤0.07）。scanline/CRT/vignette-wash の overlay を選ばない。** 発色は B が accent `#7C9082`（interrogation green-gray）に寄せる想定。**curriculum-morning の light（L05/L09）は reparations/curriculum/ENDING 用のみ・sodium glow（L04/L10）は夜景 exterior 用のみ。** 他話色（electric blue/prison gold/porch amber/teal/crimson/forest-green/violet/plum/steel-cyan/evidence-blue #3F5E8C）を選ばない。

---

# 5. A-1: SDXL 静止画のバッチ生成（210本 × 1枚・バリエーション0）— ★motif ライブラリ方式

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-055-burge/04_scenes/ai_prompts.v001.md   ← A が §5.9 の形式で書く
出力:  H:\pd-media\assets\ai\burge\S<NNN>.png（+ remotion/public/burge/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★210本の作り方＝「motif ライブラリ」テンプレート方式

210 の固有プロンプトを**幕×motifで体系化**する。各 motif に (a) **確定 distinct 枚数**、(b) **S番号レンジ**、(c) **literal 例プロンプト** を与える。**各 motif の例プロンプトを下敷きに、割り当てられた枚数ぶんの固有プロンプトを、被写体・角度・光・寄り引き・オブジェの状態を1枚ずつ変えて書き切る**（同一構図の量産＝禁止・1枚1固有）。**motif 合計が幕の確定 still 数（§3.2）に一致し、全幕合計 210 になることを最後に検算。**

> ★**1シーン1枚・variants 0。** 各プロンプト末尾に §5.3 の `[STYLE]`（人物なし象徴 still）**または** §5.11 の `[HSTYLE]`（匿名人物 still）を**全文連結**、`Avoid:` の後に §5.4 `[NEG]`（象徴）**または** §5.11 `[HNEG]`（匿名人物）を**全文連結**。
> **★2レーン構成: 210 body = object/symbolic 153枚（`[STYLE]`+`[NEG]`・人物なし）＋ ★human-present 57枚（27.1%・`[HSTYLE]`+`[HNEG]`・匿名/非識別・背向き/影/silhouette/hands・adults only）。** 該当 S-range は §5.6 で `★HP` と明記。
> **HARD BAN（不変・両レーン共通）: 拷問/拘束/装置と人体の同一フレームなし・苦悶顔なし・実在人物 likeness なし・可読テキストなし・識別可能な子供顔なし。黒人男性サバイバーの silhouette は尊厳第一（直立・静・逆光・うずくまり禁止）。**

## 5.3 共通スタイル `[STYLE]`（body 210 の象徴 still ＋ 抽象 i2v 種に連結・DESIGN §1 と一字一致）

```
, cinematic still, somber documentary grade, a cold institutional fluorescent green-gray key light as the one recurring cool note, near-black ink institutional gravity, 1970s-1990s Chicago rendered in period-correct detail, sodium-vapor orange street light strictly as distant night-exterior ambience, a small hand-cranked dark device with two thin wires shown only inert and alone as the dread object, a cast-iron radiator only ever in an empty room, a typed letter and envelope with all text blurred into an unreadable smear as the buried-truth motif, an institutional clock with unreadable hands as the statute motif, a rust note reserved for the dread objects only, a single warm schoolroom-morning note reserved for the reparations and curriculum beats only, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, no torture, no restraint, no violence, empty rooms as aftermath, objects and shadows only
```

> **EP39〜EP54 の色語（1語も含めない）:** electric blue / sodium prison gold（EP41 の accent＝監獄内装。**本作の sodium は夜景 exterior の環境光のみ・accent は green-gray**）/ porch-amber / teal-green hospital / crimson kitchen / forest-green / civil-violet two-lane Texas road / somber-plum Utah / steel-cyan（EP50）/ **cold evidence/bandana-blue #3F5E8C（EP52）**。**EP55 の色 = interrogation fluorescent green-gray `#7C9082`（INK `#0A0B0C`）＋ 夜景のみ sodium `#C4761B` ＋ dread object のみ rust `#8E3B1F` ＋ 末端のみ curriculum-morning `#E6DCA8`。**

## 5.4 共通ネガティブ `[NEG]`（各 `Avoid:` の後に全文付ける・A/B 同一）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible letter, legible police report, legible newspaper, legible court record, legible medical chart, legible date, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, front-facing person, Jon Burge, Andrew Wilson, Anthony Holmes, torture, torture scene, person being shocked, person being suffocated, electrodes on skin, bag over head, man handcuffed, handcuffs on a person, restrained person, person against a radiator, gun pointed at a person, mock execution, screaming face, crying face, wounds, burns on skin, blood, gore, injury, corpse, victim depiction, interrogation in progress, violence, re-enactment, child, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, evidence-blue bandana, milky haze, foggy wash, scanline, CRT texture, vignette wash
```

> 文字/紙面が必要な絵は「blurred into an unreadable smear」で判読不能に。**拷問・拘束・傷・被害者描写・可読の偽公文書を NEG で明示抑制。** この `[NEG]` は象徴 body ＋ 抽象 i2v 種にのみ使う。**人物ビート（§5.11 H シリーズ・§5.12 thumb_face・§5.13 F シリーズ）には使わない**（人物を弾くため）。H/thumb/F は `[HNEG]`/`[TNEG]`/`[FNEG]` を使う。

## 5.5 プロンプトの絶対ルール（210本すべてに適用）

- **body 210 は2レーン（§5.2）:** object/symbolic 153枚＝§5.3/§5.4（人物なし）、**human-present 57枚（27.1%）＝§5.11 `[HSTYLE]`/`[HNEG]`**。
- **可読文字なし。** letter/report/newspaper/判決/カルテ/小切手/日付/数値/ロゴを描かない。
- **拷問・拘束・装置と人体の同一フレーム・傷・遺体・苦悶顔を一切描かない。** box は inert・radiator は空室・typewriter cover は畳まれた事務用品。取調室は**常に無人＝aftermath**。
- **R-BURGE-CONVICT:** Burge を「拷問で有罪」に見せる絵・語を作らない（有罪は嘘＝perjury/obstruction）。
- **サバイバーの尊厳（R-RACE）:** 黒人男性 silhouette は upright/still/backlit。哀れみポーズ・扇情なし。
- **fluorescent green-gray system（`#7C9082`）基調。sodium `#C4761B` は夜景 exterior のみ。rust `#8E3B1F` は box/radiator motif のみ（≤6枚）。curriculum-morning `#E6DCA8` は ACT4 後半 reparations/curriculum ＋ ACT5 のみ**（§5.6 の per-act motif で指定）。
- **時代考証:** 1972–2018。1980s ビートにスマホ/現代車/LED/現代スカイライン輪郭を混ぜない。
- **★footage treatment は bleed/parallax（DESIGN §1）。depth 前提の絵作りをしない。**
- **dochighlight を作らない・書かない。** milky wash / scanline を描かない。

## 5.6 ★motif ライブラリ（幕別・distinct 数確定・S番号レンジ・literal 例プロンプト）

> 各 motif ブロックは `motif名 — 枚数 — S番号レンジ`。**例で示した S番号は必ずその内容で作り、残りの枚数はその motif の変奏で埋める。**
> **★`[STYLE]`/`[NEG]`＝人物なし象徴。`★HP`＝§5.11 `[HSTYLE]`/`[HNEG]`（匿名・非識別の人物）。** ★HP 合計 = **57枚（27.1%）**: ACT1 10（S031–S036, S054–S057）／ACT2 14（S079–S081, S085–S088, S092–S095, S103–S105）／ACT3 10（S121–S124, S129–S131, S138–S140）／ACT4 23（S150–S153, S160–S165, S169–S171, S178–S181, S182–S184, S189–S191）。ACT0/ACT5 は象徴のまま（0）。

### ACT 0 — HOOK + OPENING（15枚・S001–S015）
- **typed_letter_fluorescent_edge — 4 — S001–S004**（S001 は also_thumb・**hook signature**・埋められた警報）
```
- `S001.png`
A typed letter and its envelope lying on a dark institutional desk, caught by a single cold fluorescent green-gray edge of light in near-black, every line of type blurred into an unreadable smear, the alarm that should have ended everything, no person, no readable text [STYLE] Avoid: [NEG]
```
- **sodium_night_foreshadow — 3 — S005–S007**（1982 シカゴの夜・sodium は遠景環境光のみ）
```
- `S005.png`
A wet South Side Chicago street at night in 1982, distant sodium-vapor lamps burning orange over dark brick two-flats, empty and silent, period-correct cars parked far away, cold green-gray shadow in the foreground, no people, no readable text [STYLE] Avoid: [NEG]
```
- **buried_records_drawer — 4 — S008–S011**（手紙/記録の上に閉まる引き出し＝they buried it）
```
- `S008.png`
A dark institutional file drawer sliding shut over a typed page whose words are an unreadable smear, cold fluorescent green-gray light, the truth being filed away, symbolic, no person, no readable text [STYLE] Avoid: [NEG]
```
- **opening_title_abstract — 4 — S012–S015**（green-gray の abstract field・title 下地・遠いシカゴ夜景の予兆）

### ACT 1 — THE COMMANDER（42枚・S016–S057）
- **south_deering_steel — 5 — S016–S020**（製鋼所の煙突・レンガ bungalow 街区・1950s-60s の面影・無人）
```
- `S016.png`
A quiet street of brick bungalows on Chicago's Southeast Side under a grey steel-mill sky, smokestacks on the horizon, 1960s period-correct and empty of people, cold documentary stillness, no readable text [STYLE] Avoid: [NEG]
```
- **vietnam_echo_field_phone — 4 — S021–S024**（軍用 field telephone を「無人の object」として・ジャングル黄昏の abstract・帰属は narration が担う）
```
- `S021.png`
An olive-drab military field telephone with a hand crank sitting alone on a wooden crate in humid dusk light, era of the late 1960s, shown only as an inert object, ominous restraint, no person, no wires attached to anything, no readable text [STYLE] Avoid: [NEG]
```
- **rise_commander_precinct — 6 — S025–S030**（昇進の machine: 階級章/コメンデーションの smear・precinct 廊下・司令官室のドア・無人）
- **★HP midnight_crew_squadroom — 6 — S031–S036**（深夜の squad room・匿名刑事たちの backs/silhouette・紙巻きの煙・adults only・no faces）
```
- `S031.png`
A 1980s Chicago detective squad room at midnight, three anonymized detectives seen only from behind as dark silhouettes against cold fluorescent green-gray light, cigarette smoke hanging, period-correct, no faces, no violence, no readable text [HSTYLE] Avoid: [HNEG]
```
- **black_box_object — 3 — S037–S039**（★rust note 使用可・**inert・無人・何にも接続しない**）
```
- `S037.png`
A small dark hand-cranked wooden and metal device with two thin coiled wires, sitting alone and inert on the far edge of an empty steel table in a windowless room, one cold fluorescent edge and a faint rust tone, dread rendered as a still object, connected to nothing, no person, no readable text [STYLE] Avoid: [NEG]
```
- **typewriter_and_radiator — 6 — S040–S045**（S040–S042 typewriter＋畳まれた灰色カバー＝banal な事務用品／S043–S045 空室の cast-iron radiator・★rust note・无人）
```
- `S043.png`
A cast-iron radiator against the wall of a completely empty interview room, hissing steam faintly visible, one cold fluorescent green-gray light and a faint rust tone on the iron ribs, the room as aftermath, no person, no restraint, no readable text [STYLE] Avoid: [NEG]
```
- **confession_machine_abstract — 4 — S046–S049**（gears/ベルトコンベアの abstract＝逮捕→部屋→署名→有罪の機械）
- **tally_begins_abstract — 4 — S050–S053**（数えられていく無名の存在＝暗い壁に並ぶ空の椅子・光の列・数字は描かない）
- **★HP survivor_dignity_silhouette — 4 — S054–S057**（尊厳ある匿名黒人男性の silhouette・upright・backlit・static・adults only）
```
- `S054.png`
A dignified anonymized Black man standing upright and still, seen only as a backlit silhouette from behind in a narrow shaft of cold institutional light, composed and unbroken, documentary restraint, no face, no distress pose, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 2 — THE SCREAMS NOBODY HEARD（50枚・S058–S107・engine・最密）
- **fahey_obrien_memorial — 2 — S058–S059**（殉職警官への dignity＝雪の中の花・折られた旗の abstract・no faces）
- **manhunt_wilson_intake — 3 — S060–S062**（1982-02 の緊迫＝夜の police station 外観・jail intake 廊下・無人）
- **wilson_room_aftermath — 3 — S063–S065**（**無人の取調室＝aftermath**・倒れた椅子なし・静かな空室・暴力なし）
- **black_box_anchor — 3 — S066–S068**（S066 は also_thumb・**inert の box が影の中・rust note**）
```
- `S066.png`
The small dark hand-cranked device with two thin wires resting inert in deep shadow on an empty table, a single cold fluorescent green-gray edge finding its crank handle, a faint rust tone, the object the courtroom would one day see, connected to nothing, no person, no readable text [STYLE] Avoid: [NEG]
```
- **injuries_clinical_abstract — 2 — S069–S070**（診察の aftermath＝空の診察室・畳まれたガーゼとクリップボードの smear・**傷/人体を描かない**）
- **raba_letter — 4 — S071–S074**（手紙 macro・封筒・タイプライターの上の一枚・全文 smear）
- **letter_up_chain_buried — 4 — S075–S078**（in-tray の手紙→大きな机→引き出しが閉まる＝procedure としての埋葬）
- **★HP doctor_at_jail — 3 — S079–S081**（匿名の医師 stand-in・背向き/hands・記録を書く・白衣・no face）
```
- `S079.png`
An anonymized doctor stand-in in a white coat seen only from behind at a jail infirmary desk, hands writing into a record under one cold lamp, the page an unreadable smear, conscience at work, no face, no patient shown, no readable text [HSTYLE] Avoid: [HNEG]
```
- **courtroom_civil_trial — 3 — S082–S084**（1989 民事法廷＝無人の法廷・**evidence table の上の inert な box**・cold）
- **★HP civil_trial_gallery — 4 — S085–S088**（匿名の陪審/傍聴の backs・soft-focus・no faces）
- **deep_badge_letters — 3 — S089–S091**（夜の mailbox・匿名の封筒4通・投函の abstract・無人）
```
- `S089.png`
Four plain envelopes lying fanned on a dark surface beside a night-blue window, unsigned and unmarked, their contents an unreadable smear, an anonymous warning mailed out of the building, cold green-gray light, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP conroy_typing — 4 — S092–S095**（匿名記者 stand-in・背向き・深夜のタイプライター/端末・誰も読まない原稿）
- **goldston_systematic — 4 — S096–S099**（内部報告書の abstract＝分厚い綴じ・スタンプの smear・ロックされる引き出し）
- **fired_not_charged — 3 — S100–S102**（Police Board の無人議場・机上の badge と空の椅子・「解雇≠起訴」の冷たさ）
- **★HP walks_away_florida — 3 — S103–S105**（匿名の大柄な男 stand-in・背向きで建物を出て行く→暖色の南へ・no face）
- **vigilante_boat — 2 — S106–S107**（暖かい Florida の dock・cabin cruiser の遠景・**船名は描かない/可読文字なし**）

### ACT 3 — THE CLOCK RUNS OUT（42枚・S108–S149）
- **prison_years_nonsensational — 5 — S108–S112**（塀・フェンス・独房窓の光＝非扇情・無人・gore なし）
- **special_prosecutors_files — 5 — S113–S117**（148件の綴じ・箱の列・4年分の紙・法律図書室）
- **zero_charges_abstract — 3 — S118–S120**（結論の空白＝空の起訴状 smear・閉じられる報告書・静かな机）
- **★HP death_row_10_organizing — 4 — S121–S124**（独房の匿名の手がタイプする leaflet・尊厳・no face・non-sensational）
```
- `S121.png`
Anonymized hands typing on a small manual typewriter on a prison cell desk under one weak lamp, pages of an unreadable smear stacking beside it, organizing from inside, dignified and quiet, no face, no bars in frame, no readable text [HSTYLE] Avoid: [HNEG]
```
- **statute_clock_runs_out — 4 — S125–S128**（S128 は also_thumb・**institutional clock・針は影に溶ける・時間切れ**）
```
- `S128.png`
A large institutional wall clock in near-black, its hands dissolving into shadow so no time can be read, a cold fluorescent green-gray edge across the dial, the limitations clock that ran out, no person, no readable numerals [STYLE] Avoid: [NEG]
```
- **★HP ryan_podium — 3 — S129–S131**（匿名の知事 stand-in・法学部講堂の演壇・背向き/逆光・NOT a likeness）
- **pardons_gates_cold — 3 — S132–S134**（開く鉄扉と冬の冷光＝object レーン）
- **capitol_moratorium — 3 — S135–S137**（州都 Springfield の dome・大理石・無人）
- **★HP pardoned_men_walk — 3 — S138–S140**（4人の匿名 silhouette が冬の冷光へ歩き出す・upright・dignified・no faces）
```
- `S138.png`
Four dignified anonymized Black men seen only from behind walking out of an opening prison gate into cold winter morning light, upright and unhurried, coats and breath in the cold air, freedom rendered with restraint, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **florida_warm_impunity — 4 — S141–S144**（同時刻の対岸＝暖かい dock・boat の wake・split-screen の右半分）
- **oath_page_pen — 5 — S145–S149**（interrogatory の smear・ペン先が紙に触れる直前・署名の運命）
```
- `S145.png`
A fountain pen poised a breath above a typed legal interrogatory page, all text an unreadable smear, one cold fluorescent green-gray light raking the paper, the only mistake the law could still reach, no person visible beyond an out-of-focus cuff, no readable text [STYLE] Avoid: [NEG]
```

### ACT 4 — LYING UNDER OATH（46枚・S150–S195・climax・cascade・最密②）
- **★HP arrest_agents_backs — 4 — S150–S153**（Florida の朝・匿名 agents の backs が家のドライブを歩く・逮捕の phase・no faces・拘束具/手錠を描かない）
- **federal_courthouse — 3 — S154–S156**（連邦裁判所の柱・plaza・報道の脚立と空のマイク）
- **faultsplit_gambit_abstract — 3 — S157–S159**（時効の壁 vs 新しい嘘の道＝二又に割れる abstract 構造）
- **★HP survivors_testify — 6 — S160–S165**（証言台の匿名黒人男性 silhouette・upright・37年後にようやく聞かれる・no faces）
```
- `S160.png`
A dignified anonymized Black man standing at a federal witness stand, seen from behind and lost to a calm silhouette against tall cold windows, testifying at last after decades, still and composed, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **verdict_guilty — 3 — S166–S168**（評決＝法廷の doors が open into light・abstract）
- **★HP gallery_rise — 3 — S169–S171**（傍聴席の backs が立ち上がる・抱き合う輪郭・no faces）
- **sentencing_cold_bench — 3 — S172–S174**（判事席の空・cold・4.5年の重さと軽さ）
- **pension_deadlock — 3 — S175–S177**（割れたテーブルの abstract・封筒が延々と届く drift・数字は描かない）
- **★HP council_apology — 4 — S178–S181**（市議会場・傍聴席のサバイバーの backs・議場の光・no faces）
- **★HP center_door_warm — 3 — S182–S184**（Englewood のセンターの入口・匿名の人々の backs が暖色の戸口へ・★curriculum-morning note 開始）
- **curriculum_schoolbook — 4 — S185–S188**（S186 は also_thumb・**教室の机の上の開いた教科書・curriculum-morning light・頁は smear**）
```
- `S186.png`
An open schoolbook on a wooden classroom desk in warm early-morning light, dust motes in the sunbeam, the pages a soft unreadable smear, the buried letter become a chapter, quiet triumph, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP teacher_classroom — 3 — S189–S191**（教壇の匿名教師 stand-in・背向き・生徒は out-of-focus の輪郭のみ・**識別可能な子供の顔なし**・morning）
- **memorial_groundbreaking — 3 — S192–S194**（Washington Park の緑・掘り返された土とシャベル・花）
- **burge_death_quiet — 1 — S195**（無人の dock・boat の不在・暮れる湾＝終わりは静かに）

### ACT 5 — ENDING（15枚・S196–S210・the truth lands last・strip to essentials）
- **letter_unburied — 4 — S196–S199**（引き出しが開く・手紙が光の中へ・1982 の一枚が戻ってくる）
- **letter_becomes_chapter — 4 — S200–S203**（手紙のページが教科書の見開きへ dissolve する中間状態・smear のまま・morning light）
- **classroom_morning — 4 — S204–S207**（無人の教室・朝陽の shaft・並んだ机・チョークボードの blur）
- **final_breath_dawn — 3 — S208–S210**（湖の夜明け・都市の朝・green-gray が morning gold に解ける一筋）

## 5.7 幕別 motif 枚数の検算（★Codex は書き終えたら足して確認）

```
ACT0  : 4+3+4+4 = 15
ACT1  : 5+4+6+6+3+6+4+4+4 = 42
ACT2  : 2+3+3+3+2+4+4+3+3+4+3+4+4+3+3+2 = 50
ACT3  : 5+5+3+4+4+3+3+3+3+4+5 = 42
ACT4  : 4+3+3+6+3+3+3+3+4+3+4+3+3+1 = 46
ACT5  : 4+4+4+3 = 15
合計   : 15+42+50+42+46+15 = 210 ✓
★human-present(★HP) body: 10(ACT1)+14(ACT2)+10(ACT3)+23(ACT4) = 57 / 210 = 27.1%（残り153は object/symbolic）
```
> **S001..S210 の連番が穴なく210行**そろっていることを `--only S001` の `shots=255`（210 body + 42 i2v種 + 3 thumb_face）で確認する。

## 5.8 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_burge_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

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
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 55 --only S001
#   → ログ "episode=... shots=255 ... -> N images" の shots が 255 であること（210 body + 42 i2v種 + 3 thumb_face）

# 全255枚（body 210 + i2v種 42 + thumb_face 3・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-055-burge
```
> QC で落ちたシーンの再生成は `--only S###`（同じプロンプトで別シードを1枚）。**基準を下げない・水増ししない。**

## 5.11 ★人物画像（匿名・ドラマ化スタンドイン）— HUMAN-FIGURE prompts（★18本・i2v 種の内数）＋ ★HP body still の style

> **owner directive（EP48/49「空/寂しい」却下の恒久対策）: 匿名・非識別の人物を増やし、動かす。** 実在人物（Burge/Wilson/Holmes/Jones/恩赦4人/Raba/Daley/Fitzgerald/Lefkow/Ryan/Emanuel/刑事/判事）の **likeness を作らない**。顔は非識別（背向き/影の横顔/逆光 silhouette/目から下クロップ/浅い被写界深度・**adults only**）。**拷問・拘束・装置と人体の同一フレームを絶対に作らない（R-TORTURE-DEPICT 継続）。黒人男性サバイバーの silhouette は尊厳第一（upright・still・backlit）。識別可能な子供の顔なし（教室ビートは out-of-focus の輪郭のみ）。**
> **★この `[HSTYLE]`/`[HNEG]` は (a) 18本の i2v 人物種、(b) §5.6 の ★HP body still 57枚、の両方に使う。**

### ★lane 定義（人物は動かす＝紙芝居にしない → H は motion レーンへ・locked counts 不変）

**H001–H018 は「新規の静止カット」ではなく、既存 42本の i2v 種のうち 18本の中身（＝人物ビート）として作る。additive にしない（object 種を人物種に転換）。**
- **role = `i2v_source`**（body には回さない）。**42本の i2v 種のうち ★18本を人物ビート**に充て、残り **24本を抽象/象徴種**（§8.1a）。per-act の内数: **ACT1×5・ACT2×5・ACT3×4・ACT4×4 ＝18**（§4.5 の M04/M06/M07/M09/M10・M13/M14/M16/M19/M20・M22/M23/M24/M25・M33/M34/M36/M37）。ACT0/ACT5 は象徴のまま。
- **asset_id は既存の i2v 種 ID 空間（`^BUR-MS\d{2}$`）の 18本を占有**（H001–H018 は本書内のラベル）。種画像ファイルは `M<NN>_src.png`。`public_path==null`。
- 各人物種は **Wan → RIFE（§8）で motion 化**され、**42本の motion のうち 18本**になり、**84 motion カットのうち最大 36カット**に出る＝**人物が動く**。
- **QC フラグ:** `has_human_body:true`（許可）・`has_identifiable_real_person:false`（必須）・`has_readable_text:false`（必須）・`has_torture_or_restraint:false`（必須）。
- **★locked counts は1つも変わらない:** still_body **210**（＝object 153 ＋ ★HP 57）/ still_i2v_source **42**（＝抽象 24 ＋ 人物 18）/ motion **42** / factory **235** / overlay **30** / thumb_face **3**；cuts **244/235/84 = 563**；still-share **0.4334**；first-use **0.8650**；avg-uses **1.156**。

**共通スタイル `[HSTYLE]`（各 H プロンプト末尾に全文連結・匿名/非識別/photoreal/green-gray）:**
```
, cinematic photoreal still, documentary reenactment stand-in, a generic anonymized person who resembles no real individual, face kept non-identifiable — turned away, in profile lost to shadow, back-lit to a silhouette, cropped below the eyes, or thrown soft in shallow focus, a cold institutional fluorescent green-gray key light as the one recurring cool note, near-black ink institutional gravity, period-correct 1970s-2010s Chicago, low-key deep-shadow lighting, telephoto compression, shallow depth of field, restrained dignified framing, Black survivor figures always upright and composed and never in distress poses, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no readable documents, no torture, no restraint, no device touching anyone, a single warm schoolroom-morning note only where the beat is reparations or teaching
```
**共通ネガティブ `[HNEG]`（各 `Avoid:` の後に全文連結・匿名人体は許可、実在 likeness/拷問/拘束/可読テキストは禁止）:**
```
recognizable real person, likeness of a specific person, Jon Burge, Andrew Wilson, Jackie Wilson, Anthony Holmes, Melvin Jones, Aaron Patterson, Madison Hobley, Leroy Orange, Stanley Howard, Richard Daley, Patrick Fitzgerald, Judge Lefkow, George Ryan, Rahm Emanuel, any real judge or detective, celebrity, mugshot, deepfake, text, words, letters, numbers, captions, watermark, logo, readable document, legible letter, legible report, legible date, license plate, torture, person being shocked, person being suffocated, electrodes on skin, bag over head, handcuffs on a person, restrained person, person against a radiator, gun pointed at a person, screaming face, crying face, wounds, burns on skin, blood, gore, injury, corpse, cowering figure, crouching victim, identifiable child face, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, evidence-blue bandana, milky haze, scanline
```

### 人物ビート（★18本・全て匿名・非識別・実在 likeness なし・adults only・i2v 種として motion 化）
```
- `H001.png`  (= M04_src.png · ACT1 · the commander in his squad room)
A single broad-shouldered anonymized commander stand-in seen only from behind, standing at the head of a dark 1980s squad room, back-lit by cold fluorescent green-gray light so no face reads, institutional authority, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `H002.png`  (= M06_src.png · ACT1 · the midnight shift assembles)
Three anonymized detectives seen only from behind walking down a dim precinct corridor at midnight, coats and cigarette smoke, cold green-gray light, period-correct 1980s, no faces, no violence, no readable text [HSTYLE] Avoid: [HNEG]
- `H003.png`  (= M07_src.png · ACT1 · the young MP, Vietnam era)
A young anonymized military policeman stand-in seen only from behind at dusk in a humid 1960s base camp, helmet silhouette against fading light, era texture, no face, no combat, no violence, no readable text [HSTYLE] Avoid: [HNEG]
- `H004.png`  (= M09_src.png · ACT1 · the men the city would not believe)
A dignified anonymized Black man standing upright and still in a narrow shaft of cold institutional light, seen from behind as a composed backlit silhouette, unbroken, documentary restraint, no face, no distress pose, no readable text [HSTYLE] Avoid: [HNEG]
- `H005.png`  (= M10_src.png · ACT1 · the report gets typed)
Anonymized detective's hands typing a report on a manual typewriter under one cold desk lamp, seen over the shoulder so no face reads, the page an unreadable smear, the machine producing paper, no readable text [HSTYLE] Avoid: [HNEG]
- `H006.png`  (= M13_src.png · ACT2 · the doctor writes the letter)
An anonymized doctor stand-in in a white coat seen only from behind at a jail infirmary desk at night, hands writing a letter under a single lamp, the page an unreadable smear, conscience at work, no face, no patient, no readable text [HSTYLE] Avoid: [HNEG]
- `H007.png`  (= M14_src.png · ACT2 · the letter goes up the chain)
A typed letter being passed between two pairs of anonymized hands across a vast dark official desk, both figures cropped to sleeves and shadow, the page an unreadable smear, procedure swallowing an alarm, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H008.png`  (= M16_src.png · ACT2 · the reporter nobody heeded)
An anonymized reporter stand-in seen from behind typing alone in a dark newsroom at night, one desk lamp, stacks of drafts as unreadable smears, seventeen years of shouting on paper, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H009.png`  (= M19_src.png · ACT2 · fired, not charged)
A broad anonymized man in civilian clothes seen only from behind walking away from a stone institutional building carrying a box, cold grey daylight, the end that was not an end, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H010.png`  (= M20_src.png · ACT2 · south to the warm water)
An anonymized man seen from a far distance walking down a warm Florida dock toward a moored cabin cruiser at golden dusk, back to camera, impunity as leisure, no face, no readable boat name, no readable text [HSTYLE] Avoid: [HNEG]
- `H011.png`  (= M22_src.png · ACT3 · the years inside)
Dignified anonymized Black men standing far apart and upright in a bare prison yard in flat winter light, seen only from behind, still and composed across stolen decades, non-sensational, no faces, no gore, no readable text [HSTYLE] Avoid: [HNEG]
- `H012.png`  (= M23_src.png · ACT3 · organizing from death row)
Anonymized hands typing leaflets on a tiny manual typewriter on a cell desk under a weak lamp, pages stacking as unreadable smears, resistance made of paper, dignified, no face, no bars in frame, no readable text [HSTYLE] Avoid: [HNEG]
- `H013.png`  (= M24_src.png · ACT3 · the governor at the podium)
An anonymized older statesman stand-in seen only from behind at a law-school lecture hall podium, hall of shadowed listeners as soft non-identifiable shapes, the weight of a decision, no likeness of any real person, no readable text [HSTYLE] Avoid: [HNEG]
- `H014.png`  (= M25_src.png · ACT3 · four men walk off death row)
Four dignified anonymized Black men seen only from behind walking out of an opening steel gate into cold January morning light, upright and unhurried, breath visible, freedom with restraint, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H015.png`  (= M33_src.png · ACT4 · a survivor finally testifies)
A dignified anonymized Black man standing at a federal witness stand, seen from behind and lost to a calm silhouette against tall cold courtroom windows, heard at last after decades, still and composed, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H016.png`  (= M34_src.png · ACT4 · the gallery rises at the verdict)
A courtroom gallery of anonymized figures seen from the back rising to their feet as one, shoulders and backs only, a long-awaited verdict landing, restrained emotion, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H017.png`  (= M36_src.png · ACT4 · survivors watch the apology)
Rows of dignified anonymized figures seen from behind in a grand city-council gallery, watching the floor below as the city finally says the word, warm light beginning to break into the cold palette, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H018.png`  (= M37_src.png · ACT4 · the lesson is taught)
An anonymized teacher stand-in seen from behind at the front of a morning classroom, students only as soft out-of-focus shapes beyond, warm schoolroom-morning light through tall windows, the record become a lesson, no identifiable child, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
> **★H↔M 対応（§4.5 と一致・18本）:** H001=M04 · H002=M06 · H003=M07 · H004=M09 · H005=M10 · H006=M13 · H007=M14 · H008=M16 · H009=M19 · H010=M20 · H011=M22 · H012=M23 · H013=M24 · H014=M25 · H015=M33 · H016=M34 · H017=M36 · H018=M37。`ai_prompts.v001.md` では**新規行を足さず**、該当する 18本の `M<NN>_src.png` 行を上記の人物内容＋`[HSTYLE]`/`[HNEG]` で書く（`shots=255` 維持）。§8.5 で目視確認（adults only・子供顔なし・拷問/拘束なし・実在 likeness なし・サバイバー silhouette の尊厳）。

## 5.12 ★サムネ用 emotive-face 静止画（3枚・CTR §4A・thumb_face）

> **owner directive（CTR_PLAYBOOK §4A・emotive face が lane の #1 CTR driver）:** サムネは **単一の AI 生成・非実在・illustrative/dramatized な顔**を peak emotion で。**実在人物（Burge/サバイバー/市長/判事）の likeness を作らない**＝clearly illustrative（semi-painterly, cinematic-render）にして実写に読ませない＝likeness firewall。**被害の傷・拷問・子供の顔を作らない。** これらは **本編カットに出ない thumbnail 専用**（role=thumb_face・public_path null・distinct/cuts に数えない・§3.1）。B が `BurgeThumbnails.tsx` で face＋2–4語 hook text を合成。

**共通スタイル `[TSTYLE]`:**
```
, thumbnail key art, a single non-real dramatized generic human character rendered in a clearly illustrative semi-painterly cinematic style so it never reads as a real photograph of a real person, face occupying 50 to 65 percent of frame height with eyes on the upper third, bright key light on the face and a rim light separating it from a dark desaturated blurred Chicago background at night, skin warm, background cool green-gray, high contrast and vivid, one clean quadrant of negative space for text, 1280x720, ultra-detailed
```
**共通ネガティブ `[TNEG]`:**
```
photoreal photograph of a real person, likeness of Jon Burge or any real survivor or judge or mayor or detective, recognizable real celebrity, deepfake, a child, wounds, burns, blood, gore, torture, restraint, violence, weapon, text, words, letters, numbers, watermark, logo, two faces, tiny face, neutral expression, dark muddy low-contrast mush, cartoon flatness, extra limbs, deformed, warped
```
```
- `T01_face.png`
A non-real dramatized generic middle-aged Black man's face in an illustrative cinematic style at peak emotion — a steady, wounded, unbroken stare directly at the viewer, the look of a man nobody believed for thirty years, pushed to the right third over a dark blurred police-station background at night with one cold green-gray window, warm rim light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
- `T02_face.png`
A non-real dramatized generic older white man's face in an illustrative cinematic style with a cold, contemptuous, untouchable authority glare looking directly at the viewer, the decorated-commander-who-cannot-be-charged archetype, pushed to the left third over a dark blurred city-skyline-at-night background with a faint sodium glow, hard rim light, clean negative space on the right [TSTYLE] Avoid: [TNEG]
- `T03_face.png`
A non-real dramatized generic Black man's face in an illustrative cinematic style with eyes closing in stunned relief and a single tear catching warm light, the moment the city finally said sorry, pushed to the right third over a dark blurred council-chamber background with a first band of warm morning light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
```
> ★これら3枚は `role:"thumb_face"`・`public_path:null`・`has_human_body:true`・`has_identifiable_real_person:false`。§6 の目視で「実在 likeness でない・illustrative・傷/拷問なし・子供なし」を確認。B のサムネ案は T01–T03 を前景に、§4.3a の also_thumb body（背景）＋ 2–4語 hook（CTR §4A・例 "100+ TORTURED" / "JAILED FOR LYING"）で組む。

## 5.13 ★EMOTIVE FACES — VISIBLE faces（F-series 12枚・per owner 2026-07-25 standard）

匿名図だけでは「顔がほぼ無い」状態になる。オーナー方針＝**見える感情的な顔**を織り込む（顔は維持率・CTRを上げる）。F-series（見える顔）を既存の匿名図に**加えて**生成する（★distinct/cuts に数えない補助レーンとして B が挿し込み判断・manifest には `role:"body"` 外の扱いを B と合意してから — 迷ったら生成だけして staging し、cuts への採用は B に委ねる）。

**2レーン、いずれも「実在の誰にも似せない・非実在の人物」:**
- **(a) generic-photoreal** — 特定の実在人物に紐づかない役（陪審員・傍聴人・記者・看守・一般の医療者/弁護士/教師）。
- **(b) dramatized-illustrative** — 中心的実在人物に隣接するビート（サバイバー everyman・司令官 archetype）は**明らかにイラスト調・半絵画的**で写真に見えないスタイルに（実在人物の写真に絶対見えないように）。実在人物として名指し/キャプションしない。

**HARD BANS（不変）:** Burge・Wilson・Holmes・恩赦4人・Raba・Daley・Fitzgerald・Lefkow・Ryan・Emanuel の**肖像を作らない**；**識別可能な子供の顔は不可**；傷・拷問・拘束・苦悶の再現なし；可読テキストなし。QCフラグ: `has_human_body:true`・`has_identifiable_real_person:false`・`has_identifiable_face:false`（=実在として識別可能でない）・`has_torture_or_restraint:false`・`has_readable_text:false`。

**★ FACE 標準（data-driven・owner choice A）:** 全F画像は**LIGHT + EXPRESSION で目立つ顔**（サイズで盛らない）— **medium-close-up ~30–45% of frame height, eyes on the upper third, front or slight three-quarter, one strong unmistakable emotion, dramatic key + rim light against a DARK moody restrained background**。60%超の顔面充填・背向き・影に沈む・hands-only は不可。

`[FSTYLE]` = `a clearly-visible emotive human face in a strong medium-close-up filling ~30-45 percent of the frame, eyes on the upper third, front or slight three-quarter view looking near camera, one strong unmistakable {EXPRESSION}, dramatic key light plus rim light on the face against a dark moody background, restrained saturation, a generic anonymized non-real person resembling no real individual, cinematic documentary grade, cold fluorescent green-gray with a single warm schoolroom-morning note only on reparations beats, ultra-detailed skin and eyes, high contrast, {photoreal | clearly illustrative semi-painterly non-photographic}, 16:9, adults only, no text, no watermark, no logo`
`[FNEG]` = `likeness of a real or named person, Jon Burge, Andrew Wilson, Anthony Holmes, Patterson, Hobley, Orange, Howard, Daley, Fitzgerald, Lefkow, Ryan, Emanuel, recognizable real person, mugshot, deepfake, child, toddler, victim wounds, burns, blood, injury, torture, restraint, weapon, readable text, document, caption`

Files `F001.png … F012.png`. Act-mapped beats:
- **F001** (b · ACT1) a survivor everyman's illustrative face, steady and unbroken — the man nobody believed. NOT a likeness of any real survivor.
- **F002** (a · ACT1) detectives' hard, closed faces in fluorescent light — the machine's operators, generic.
- **F003** (b · ACT2) a jail doctor's troubled face over a letter — conscience, generic, not Raba.
- **F004** (a · ACT2) a reporter's exhausted, determined face at a typewriter — seventeen years of shouting, generic, not Conroy.
- **F005** (a · ACT2) jurors' uncertain faces in a 1989 civil courtroom — generic.
- **F006** (b · ACT3) an illustrative face behind prison glass, decades etched in, composed — dignity, not despair. NOT a likeness.
- **F007** (a · ACT3) a governor-archetype's grave face at a podium — the weight of the pardon decision, generic, not Ryan.
- **F008** (b · ACT3) an illustrative face of a man stepping into cold January light, disbelief and relief — freedom. NOT a likeness.
- **F009** (b · ACT4) the untouchable-commander archetype as a cold, contemptuous illustrative face in shadow — NOT a Burge likeness, no glorification.
- **F010** (a · ACT4) a survivor-witness's face on the stand, calm and resolute — finally heard, generic.
- **F011** (a · ACT4) council-gallery faces as the apology lands — tears and stillness, generic adults.
- **F012** (a · ACT4) a teacher's warm, serious face before a morning class — the lesson carried forward, generic; students never in identifiable focus.

Generate all 12; QC each visually (visible emotive face · non-real · no likeness/child/wounds/text) before manifest.

> **★R3 clarifier（shots カウントとの整合）:** F001–F012 の12行は、**base 255 行（S001..S210 + M01_src..M42_src + T01_face..T03_face）の `shots=255` 検証が通った後に** `ai_prompts.v001.md` の末尾へ追記して生成する。**追記後の `shots=267`（255+12）が正**。§5.9/§5.10 の「255」は F-series 追記前の base セットの検算値であり、形式破損の判定はその時点で行う。F-series は distinct/cuts に数えない（§5.13 冒頭のとおり）。

---

# 6. A-2/A-3: 静止画のQC・目視（★depth map なし）

## 6.1 機械QC（body 210 + i2v種 42 + thumb_face 3 = 全255枚・`qc_burge_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `18.0<=mean_luma<=225.0`（near-black ink・green-gray の低照度が多い→黒潰れ注意。ACT4後半/ACT5 の morning ビートは明側） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**衝突は letter(S001/S071系/S196系)・drawer(S008系/S075系)・box(S037系/S066系)・radiator(S043系)・clock(S125–S128)・courtroom(S082系/S160系)・prison(S108系)・classroom(S185系/S204系) の被りに注意** | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・日付(1982/1990/1993/2003/2010/2015)・"Vigilante" の船名・件数(118/57)・金額($5.5M/$210M)・報告書/新聞/手紙のロゴ | `has_readable_text=true`→reject |
| Q6 | **実在人物**の顔の混入 | **目視。** 実在人物として識別可能な顔（Burge/Wilson/Holmes/恩赦4人/Raba/Daley/Fitzgerald/Lefkow/Ryan/Emanuel に**似た**顔）。**匿名・非識別の顔（H/F/thumb_face）は OK。** | `has_identifiable_real_person=true`→reject |
| Q7 | 拷問/拘束/傷/子供 | **目視。** 拷問・拘束・装置と人体の同一フレーム・手錠・傷/火傷/血・苦悶/泣き顔・うずくまるサバイバー・**識別可能な子供の顔**。**★匿名の人体は OK（`has_human_body=true` 単独では reject しない）。** | あれば reject |

**Q5/Q6/Q7 は機械で判定しない。全255枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-055-burge --media image
#   → runs/qc/burge_footage_contact_NN.png（20枚/シート・約13シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-54 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** 特に **S037/S066系(box)は「装置が何かに接続された絵・人の手が写る絵」になっていないこと、S043系(radiator)は無人であること、S054/S138/S160系(サバイバー silhouette)が尊厳ある upright で「哀れみポーズ」に転じていないこと、S150系(逮捕)に手錠/拘束が写らないこと、S189系(教室)に識別可能な子供の顔が無いこと、S106系(boat)に読める船名が無いこと、T01–T03/F009 が実在の Burge/サバイバーに似ていないこと、を必ず目で確認する。**

## 6.2 出力
```
episodes/PD-2026-055-burge/05_visuals/still_qc.v001.json     # 255枚全部の行（reject も残す）
```

## 6.3 accepted が (body210 / i2v42 / thumb3) に届かなかったとき
```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 55 --only S###   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_burge_stills.py
```
accepted body >= 210 かつ i2v_source >= 42 かつ thumb_face >= 3 になるまで繰り返す。**基準を下げない・水増ししない。**

## 6.4 ★depth map は生成しない（本作は depth treatment 不使用）
**DESIGN §1 の hard rule により footage/still treatment は `bleed`/`parallax`/`duotone`/`focus` のみ・`depth` を使わない**（depth displacement は被写体を melt/warp させる＝EP48/49 の warp 欠陥）。したがって **`gen_depth_maps.py` を回さない・`<stem>_depth.png` を作らない・マニフェストに `depth_path` を持たせない**（§4.1a/§4.2-19）。

---

# 7. A-4: factory 実写クリップ 235本の選定と全点目視QC

## 7.1 在庫の実態
```
H:\pd-media\assets\factory\   フラット構成（backgrounds 11,000本超・light_assets・particle_assets・vfx_overlays・texture_assets・loops）
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json（★必ず encoding="utf-8" で開く）
★既知の障害: factory 棚のラベルは全面的に信用できない（evidence_bag=カートゥーン事故の実績）。§7.5 の全点目視が生命線。
```

## 7.2 選定条件
- **`kind=="video"` のみ。** 静止画 factory は使わない
- **235本ちょうど**（§3.3[8] より still-share≤0.45 を守る設計値）
- **各1回しか使わない**（`MAX_USES_FACTORY=1`）
- 幕別割り当て（§4.4）: HOOK+OPENING=12 / ACT1=44 / ACT2=40 / ACT3=48 / ACT4=44 / ACT5=14 ＋ 繋ぎ=33 ＝ 235
- **EP39〜EP54 の絵柄を選ばない（§7.7 の分離語）。** EP55 は 1970s-90s シカゴ夜景/el train/brick bungalow/steel mill・precinct/records/jail・裁判所/連邦裁判所・州都 Springfield・Florida の warm dock/marina・市議会場・学校/教室/教科書・Washington Park・morning light。**実在の顔が写るニュース/デモ映像・拷問/拘束/手錠/傷の imagery・泣く人・葬列の顔・鉄格子内の gore を選ばない。EP41 sodium prison corridor・EP44 病院 teal・EP47 two-lane/pickup・EP49 Utah・EP50 cyan・EP52 Texas suburb/bandana を選ばない。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query el_train_night --limit 60 --exclude-used --ep PD-2026-055-burge --json
```
`--exclude-used` は出荷ゲート `arc_nonrepeat` と同じ指紋集合を使う。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・§4.4 に pre-assign 済み）
> **★`covers_scene_id` は still 資産 ID 空間（S001..S210）を指す。** §4.4 の各エントリに pre-assign 済み（約28本が covers 付き、残りは null の繋ぎ/情景）。

| covers（例） | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S005/S008 | sodium 夜景・records | `sodium_street_night` / `records_archive` | 0 |
| S016/S022/S030/S036/S040/S042 | bungalow/勲章/precinct/interview room/typewriter/radiator | `brick_bungalow` / `medal_macro` / `precinct_hallway` / `interview_room` / `typewriter_desk` / `old_radiator` | 1 |
| S058/S060/S070/S074/S082/S090/S094 | 殉職追悼/jail gate/診察室/封筒/法廷/mailbox/輪転機 | `police_memorial` / `county_jail` / `exam_room` / `envelope_desk` / `empty_courtroom` / `mailbox_night` / `printing_press` | 2 |
| S112/S118/S128/S136/S140/S144/S148 | prison fence/law library/clock/capitol/prison gate/Florida dock/pen | `prison_fence` / `law_library` / `clock_face` / `state_capitol` / `prison_gate` / `florida_dock` / `pen_paper` | 3 |
| S150/S154/S162/S178/S184/S186/S192 | Florida house/連邦裁判所/jury box/市議会場/センター/教室/公園 | `florida_house` / `federal_courthouse` / `jury_box` / `city_council_chamber` / `community_center` / `empty_classroom` / `city_park_green` | 4 |
| S196/S200/S204 | 手紙/開いた本/教室の朝 | `letter_macro` / `open_book_light` / `classroom_morning` | 5 |

**残りは covers を持たない繋ぎ・情景**（institutional 廊下・marble・sky gradient・rain window・river fog・dust shaft・texture）。**暗いクリップに偏りすぎない**（暗側は約78本まで＝1/3・courthouse 昼光・morning light・Florida warm を混ぜる）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）
```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.4a ★★★ 実写ストックライブラリを必ず使う（EP48/49 の burned lesson＝実写0本を潰す）★★★
- **ストックライブラリ:** `H:\pd-media\assets\stock`（`STOCK_MANIFEST.json`・動画74本＋静止155本・pexels/pixabay・商用可）。
- **調達方針（★counts は固定・factory 235 を変えない。レーン内の調達源を広げるだけ）:**
  1. `STOCK_MANIFEST.json` を読み、**意味（§7.3 の covers カテゴリ）に一致し §7.5 の全点目視 QC と R-FACE/R-TORTURE-DEPICT を通る実写動画を優先採用**。
  2. 残り枠を `H:\pd-media\assets\factory` 在庫で埋める。
  3. 各エントリの出所（`origin`: `stock` or `factory`）を `factory_selection.v001.json`（§7.6）と `stock_ledger.v001.json`（§10.2）に記録。
  4. **ストック静止155本は本編 body still（AI 210）レーンに混ぜない。**
- **★R-FACE/R-TORTURE-DEPICT を絶対順守:** 実在の Burge/サバイバー/市長/判事が写るニュース映像・拷問/拘束/傷/泣く人を含むクリップは**ストックでも使わない**。EP39〜54 との sha256 被りゼロ（§7.7）はストック由来にも適用。
- **★カラーマッチは B が担当:** pexels/pixabay の発色バラつきは B が green-gray `#7C9082` の neutral グレードで AI still に合わせる（**milky wash にしない**）。

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★
> **実際に起きた事故（EP36 大聖堂・EP38 牛・factory 棚ラベル全面破損）。** `subtype` は「その検索語で取った」記録であって中身の保証ではない。**235本は分割して全点見る。**

**選抜235本は例外なく次を経る:**
```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-055-burge --media video --dir "<235本の staging フォルダ>"
```
1. コンタクトシートを開き **235本すべてを1本ずつ見る**
2. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて選定から外す（差替え）
3. 実写シネマティックB-roll・EP55テーマ・ウォーターマークなし・識別可能な実在人物なしを確認
4. **★制約の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。**拷問/拘束/手錠/傷・実在の顔が写るニュース映像・鉄格子内 gore・泣く人を使わない。時代錯誤（1980sビートに現代スカイライン/スマホ/現代車）を使わない。**
5. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=42.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。**暗いクリップは約78本（1/3）までに抑える。**

## 7.6 出力
```
episodes/PD-2026-055-burge/05_stock/factory_selection.v001.json   # 選定理由・幕割り当て・origin
episodes/PD-2026-055-burge/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP54 との重複ゼロ（BLOCKING）
```bash
./.venv/Scripts/python.exe scripts/select_burge_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-054-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP55 の235本の積集合が**空**であることを確認。1件でも exit 1。**EP39〜EP54 のファイルは読むだけ。**

**分離レーン（色・素材・語）:** EP41 gold（監獄）／EP42 blue／EP43 amber／EP44 teal（病院）／EP45 crimson／EP46 green／EP47 civil-violet（Texas road）／EP48 glover／EP49 somber-plum（Utah）／EP50 steel-cyan／EP52 evidence-blue（Texas suburb/bandana）。**EP55 = interrogation fluorescent green-gray `#7C9082`（INK `#0A0B0C`）＋夜景のみ sodium `#C4761B`＋dread object のみ rust `#8E3B1F`＋末端のみ curriculum-morning `#E6DCA8`。** これら他話の絵柄・色・被写体を1本も選ばない。

---

# 8. A-5: i2v モーション化 42本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする42本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）
種画像は §5 と同じ `generate_sdxl_4k.py`（variants なし）で `M<NN>_src.png` として生成（`ai_prompts.v001.md` に §8.1a の42行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `BUR-MS01..MS42`、モーション成果物は `BUR-M01..M42`。**幕別配分は §4.5 に pre-assign 済み**（ACT0 3 / ACT1 8 / ACT2 9 / ACT3 8 / ACT4 10 / ACT5 4 = 42）。
> **★このうち ★18本は §5.11 の匿名人物ビート（H001–H018）＝42本の内数**。**残り 24本が抽象/象徴種。**

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの42行を追加・各1枚・**poised-still の source**）
> 各種プロンプトは §5.6/§4.5 の対応 tag の「動く直前の poised-still」版。**動きが意味を持つ絵**（drawer が手紙の上に閉じる直前・clock の針が影に溶ける直前・gate が開く直前・page がめくれる直前 等）。末尾に §5.3 `[STYLE]` ＋ `Avoid:` §5.4 `[NEG]`（人物種は `[HSTYLE]`/`[HNEG]`）を全文連結。**下記は代表6例。残り36行は §4.5 の各 storyboard/tags を「poised, still, about to move」で SDXL 化**（M01_src..M42_src を穴なく）。

```
- `M01_src.png`
A typed letter under a single cold fluorescent green-gray edge of light in near-black, held still and poised a moment before a shadow slides across it, every word an unreadable smear, restraint, no person, no readable text [STYLE] Avoid: [NEG]
- `M02_src.png`
A dark institutional file drawer poised just above a typed page, held motionless a breath before it slides shut and buries it, cold green-gray light, no person, no readable text [STYLE] Avoid: [NEG]
- `M05_src.png`
The small dark hand-cranked device with two thin wires inert in deep shadow on an empty steel table, a faint rust tone, held poised as if the room itself is waiting, connected to nothing, no person, no readable text [STYLE] Avoid: [NEG]
- `M21_src.png`
A large institutional wall clock in near-black, its hands a moment from dissolving into shadow, a cold fluorescent edge raking the dial, time about to run out, no readable numerals, no person [STYLE] Avoid: [NEG]
- `M38_src.png`
An open schoolbook on a classroom desk in warm early-morning light, one page lifted and poised mid-turn, dust motes hanging, the record about to be read, pages a soft unreadable smear, no person, no readable text [STYLE] Avoid: [NEG]
- `M40_src.png`
A typed 1982 letter and an open modern schoolbook aligned on one dark surface, the letter's edge beginning to catch the same warm morning light as the book, two eras a breath from dissolving into each other, all text an unreadable smear, no person [STYLE] Avoid: [NEG]
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
STILL_DIR     = H:\pd-media\assets\ai\burge
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\burge
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, melting, text, watermark, identifiable face, real person likeness, child face, crying person, victim, corpse, torture, restraint, handcuffs, wounds, blood, gore"
```
**ゲート:** `dry_validate`（length=5）/ `assert_loaded_completely` / `assert_frame_math`。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す・★42本は複数日）
```bash
py -3.11 scripts/comfy_wan_burge.py --build
py -3.11 scripts/comfy_wan_burge.py --run --shot M01
py -3.11 scripts/comfy_wan_burge.py --run-all
```
1本 24–73 GPU分・42本で 18–48時間。**夜間分割で回す。開始前にマシン状態を確認（A1111 との VRAM 競合は unload-checkpoint で解放）。**

## 8.4 RIFE で 48fps 化（`rife_burge.py`・`rife_morton.py` と同手順）
```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番 → RIFE 2x を2回（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. フレーム数検証 `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC
- **拷問・拘束・装置と人体の同一フレーム・傷・泣く人・gore が生成されていないこと**（必ず目視）
- モーフィング/ちらつき/ワープ/melt が無いこと → あれば別シードで再生成
- H シリーズ・commander 影・governor 影が**識別可能な実在 likeness**に転じていないこと・**識別可能な子供顔**が出ていないこと・サバイバー silhouette が尊厳を失う動き（うずくまり等）をしていないこと
- box（M05/M18系）は**動いても何にも接続されない**こと／boat（M27）に読める船名が出ないこと／schoolbook（M38/M40）に可読文字が出ないこと
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（42本 × 2回 = 84カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど30本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **15本** | fluorescent room dust・archive dust・night air drift・snow drift・steam wisp・morning warm dust（ACT4後半/ACT5用） |
| `light_assets` | **10本** | fluorescent green shaft・cold window bar・desk lamp glow・**sodium edge glow（夜景 exterior のみ=L04/L10）**・**curriculum-morning glow（reparations/ENDING のみ=L05/L09）** |
| `vfx_overlays` | **5本** | 微細な grain・cold light noise・green glitch min |
| **合計** | **30本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/burge/overlay/` に置き、`burge_film.json` の `cuts[].src` には**出さない**。**★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない・scanline/CRT/vignette-wash を選ばない（DESIGN §1）。** 黒背景でループするものを選び `blend_hint` を書く。他話色を選ばない。§7.5 の目視QC対象（30本）。

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_burge_assets.py`）
```
remotion/public/burge/img/     ← role=body の静止画210枚（★depth なし）
remotion/public/burge/factory/ ← 選定 factory .mp4 235本（§4.4 の F001..F235 名で）
remotion/public/burge/motion/  ← i2v M<NN>_rife.mp4 42本
remotion/public/burge/overlay/ ← 合成レイヤー 30本（§4.6 の P/L/V 名で）
remotion/public/burge/thumb/   ← thumb_face T01..T03（B の BurgeThumbnails が参照）
```
- `public_path` はマニフェストの値（§4.4/§4.5/§4.6）と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）
- **★depth の同名ペアは作らない・置かない**（§6.4）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する）:**
- factory の `public_path` は必ず `burge/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も含めない
- 合成レイヤーは `burge/overlay/` に置き `cuts[].src` に出さない

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`
全静止画・i2v・factory・overlay・thumb_face を1行ずつ: `asset_id`/`path`/`source`(`ai_codex`|`factory`|`stock`)/`origin`/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力
```bash
./.venv/Scripts/python.exe scripts/build_burge_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_burge_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_burge_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**★factory 235 / motion 42 / overlay 30 が非空で実体化しているか（不変条件17/18/16）を必ず確認。**

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
EP55 の設計値: still 244/210=1.162(≤2) / factory 235/235=1.0(≤1) / motion 84/42=2.0(≤2) / first-use 487/563=0.8650(≥0.70) / avg-uses 563/487=1.156(≤1.4)。**全て達成可能。**

---

# 12. 絶対にやらないこと
- **EP39〜EP54 のファイル・素材に触らない。** 読み取りのみ可。素材・色・音のレーンも分離（§7.7）。
- **スレッドBの所有ファイル（§0.2）に触らない**。ただし `04_scenes/ai_prompts.v001.md` は A が書く。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness をどこにも作らない**（Burge/Wilson/Holmes/Jones/恩赦4人/Raba/Brzeczek/Daley/Conroy/Fitzgerald/Lefkow/Ryan/Emanuel/刑事/判事）。**匿名・非識別の一般人は可。**
- **★拷問・拘束・装置と人体の同一フレーム・傷・苦悶顔・泣き顔・再現を一切作らない**（R-TORTURE-DEPICT・本作の最重要禁止）。box は inert・部屋は空室・silhouette は尊厳。
- **制約に反する文言・絵を作らない**（§1.2/§1.3）: Burge の拷問有罪化／非恩赦者の無実一括断定／サバイバーの哀れみポーズ／hedged 数値の断定／可読の偽公文書／実在人物 likeness／dochighlight／捏造・可読引用／milky wash/scanline／時代錯誤。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。（factory の subtype `_02` は別素材の意・混同しない。）
- **role=thumb / still_thumb を作らない・overlay を30本以外にしない・thumb_face を3枚以外にしない。** also_thumb は body 4枚（§4.3a）。
- **★factory 235 / motion 42 / overlay 30 の配列を空・stub のまま出荷しない**（EP45/EP38 事故）。
- **★depth map を生成しない・`depth_path` を持たせない**（§6.4）。
- **★dochighlight figure を作らない・言及しない**（grep で 0）。
- **枚数を「だいたい」で決めない。** §3 の確定値（still 210 / factory 235 / i2v 42 / thumb_face 3 / distinct 487 / first-use 0.8650 / still-share 0.4334 / avg-uses 1.156 / overlay 30）と §3.3 の検算をそのまま使う。合わなければ本書を疑って報告。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** 生成物・在庫クリップを実際に見る。

---

# 13. 完了報告に含めるもの
```
1. accepted 静止画の枚数と内訳（body 210 [＝object 153 ＋ ★HP human-present 57 = 27.1%] / i2v_source 42 [＝抽象 24 ＋ ★人物 18] / thumb_face 3 / F-series 12 / also_thumb 4 [§4.3a] / reject N）
2. factory 選定 235本のリスト（asset_id / subtype / origin / eyeballed_content）と、subtype と食い違って外した本数、
   box/radiator/prison/letter クリップの「no readable text / no logo / no face / no torture-or-restraint imagery」確認、stock 由来の本数
3. EP39〜EP54 重複ゼロの確認結果
4. i2v 42本の frames / duration_sec と、SHORT? の有無、★H001–H018（18本）の匿名・非識別・adults-only・no-torture/restraint 確認、
   ★HP body 57枚が匿名・非識別・実在 likeness なし・識別可能子供顔なし・サバイバー尊厳 pose の確認
5. 合成レイヤー30本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code）＋ factory 235/motion 42/overlay 30 が非空で実体化した確認 ＋ depth_path をどこにも生成していない確認
7. §3.3 の検算 [1]〜[8] を自分で再計算した結果（avg-uses/source 1.156≤1.4 を含む）
8. asset_manifest.v001.json の counts ブロック（still_body 210 / still_i2v_source 42 / motion 42 / factory 235 / overlay 30 / thumb_face 3）
9. 制約・1枚前提の自己申告（Burge の拷問有罪化なし・拷問/拘束/装置+人体の描写ゼロ・非恩赦者の無実断定なし・
   サバイバー silhouette の尊厳確認・hedged 数値の可読断定なし・実在の顔/likeness ゼロを目視確認・dochighlight 文字列ゼロ・
   捏造/可読引用なし・milky wash/scanline なし・depth なし・バリエーション0・時代錯誤なし・A↔B同一スキーマ
   [schema burge_assets.v1 / role enum body|i2v_source|thumb_face|reject / counts / also_thumb 集合 4 / overlay 30 / thumb_face 3]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
