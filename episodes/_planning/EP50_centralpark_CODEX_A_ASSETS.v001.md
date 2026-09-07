# EP50 centralpark — Codex スレッドA「素材生成」引き継ぎプロンプト v001（★60分・チャンネル初の長尺）

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN_and_CODEX_PROMPTS / DESIGN_ARCHITECTURE）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP50_centralpark_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したもので、手書きで発明していない。
> ★これはチャンネル**初の60:00長尺**。素材点数は12分エピの約5倍。**「だいたい」で決めず §3 の確定値と §3.3 の検算をそのまま使う。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP50 / Episode ID: PD-2026-050-centralpark / slug: centralpark
Composition id: Ep50Centralpark（B が Root.tsx に登録・A は staging まで）／1920x1080 / fps30 / 60:00 長尺
事件:       The Central Park Jogger Case / The Exonerated Five（1989 暴行→1990 有罪→2002 vacatur→2014/2016 和解）
            1989-04-19 夜、Central Park で jogger（Trisha Meili・存命の survivor）が暴行された。
            黒人・ラテン系の少年5人（Antron McCray 15 / Kevin Richardson 14 / Yusef Salaam 15 /
            Raymond Santana 14 / Korey Wise 16）が、カメラを切った長時間の取調べで【虚偽自白】に追い込まれ、
            1990年に誤って有罪となり、years 服役した。
            ★物証（精液のDNA）は1990年の裁判で【5人全員を除外】していた。州は自白だけで有罪にした。
            2002年、既に別件で服役中の連続強姦殺人犯 Matias Reyes が「自分が単独でやった」と自白し、
            DNAが Reyes に一致（1 in 6,000,000,000）。2002-12-19、Justice Charles Tejada が全 conviction を vacate。
            彼らは【The Exonerated Five】。2014年 NYC ~$41M、2016年 NY州 ~$3.9M（reportedly）で和解。
            ★主題は【少年への強要された虚偽自白と冤罪、そして exoneration】。暴行そのものは主題ではない。
            ★R2: 5人・Meili・Reyes は全員【実在（5人と Meili は存命・Reyes は服役中）】＝顔・肖像・likeness を一切出さない。
              silhouette / 手 / 影 / 象徴オブジェのみ。**暴行は一切描かない（clinical・非扇情）。**
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ・★60分スケール＝12分の約5倍）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**430本の固有プロンプト × 1枚 = 430枚**・バリエーション0） | `H:\pd-media\assets\ai\centralpark\S<NNN>.png` | 10–16時間（GPU） |
| A-1b | i2v 種画像の生成（**85本の固有プロンプト × 1枚 = 85枚**・バリエーション0） | `H:\pd-media\assets\ai\centralpark\M<NN>_src.png` | 2.5–4時間（GPU） |
| A-2 | 静止画のQCと目視（**全515枚を目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 4–6時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力・role=body の430枚） | `H:\pd-media\assets\ai\centralpark\S<NNN>_depth.png` | 1時間 |
| A-4 | factory 実写クリップ **485本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **8–12時間（うち目視だけで4時間以上）** |
| A-5 | i2v モーション化 **85本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\centralpark\M<NN>_rife.mp4` | 35–95時間（GPU・**複数日**） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **60本** | `05_stock/overlay_selection.v001.json` | 1.5時間 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 40分 |
| A-8 | Remotion public への staging | `remotion/public/centralpark/{img,factory,motion,overlay}/` | 1時間（~1,000 distinct・12分の4–5倍ディスク） |

> **★★ 最重要の前提（EP42–49 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 430本＝430行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **variants 指定なし（＝1枚）** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 430 + i2v 種 85 = 515枚（各1回）。** factory 485本は生成でなく在庫からの選抜。
> **★`--only S001` のログで `shots=515` を確認**してから本番を回す（430 body + 85 i2v種 = 515）。
> ★i2v 85本は**複数日GPU**。**開始前にマシン状態を確認**（heavy-job preflight）。夜間・分割で回す。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-050-centralpark/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** counts / role enum / overlay枚数 / also_thumb集合 を **A(producer)とB(consumer/validator)で一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 485 エントリ、`motion` 配列は 85 エントリ、`overlay` 配列は 60 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5／§4.6 に全 485 + 85 + 60 を列挙済み。build スクリプトはこの列挙を消費するだけで、空配列を書かない）。EP38 の空マニフェスト事故も同じ理由で禁止。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\centralpark\**` / `H:\pd-media\assets\ai_video\centralpark\**` | **A** | 読み書き |
| `episodes/PD-2026-050-centralpark/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-050-centralpark/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/centralpark/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-050-centralpark/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_centralpark_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-049-*/**` および EP39〜49 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-050-centralpark`（variants 指定なし） / `50 --only S001` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/centralpark"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-050-centralpark --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit N --exclude-used --ep PD-2026-050-centralpark --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-050-centralpark` |

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・実在確認してから） |
|---|---|---|
| `scripts/qc_centralpark_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_strieff_stills.py`（EP49） |
| `scripts/select_centralpark_factory.py` | §7 の factory 485本の確定選定・EP39〜49 sha256 除外検証 | `scripts/select_strieff_factory.py`（EP49） |
| `scripts/comfy_wan_centralpark.py` | §8 の i2v 85本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_strieff.py`（EP49・実在確認） |
| `scripts/rife_centralpark.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_strieff.py`（実在確認） |
| `scripts/build_centralpark_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_strieff_asset_manifest.py`（EP49） |
| `scripts/stage_centralpark_assets.py` | §10 の staging | `scripts/stage_strieff_assets.py`（EP49） |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.9 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_centralpark_facts.py`（B が `check_strieff_facts.py` を clone して実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の7制約に一致し、`check_centralpark_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_centralpark_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==485 / motion 配列長==85 / overlay 配列長==60 が非空で実体化していること（EP45 事故回避の必須不変条件）

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_centralpark_asset_manifest.py --reuse-feasibility
#   → still >=430 / motion >=85 / factory >=485 / distinct 合計 >=1000 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_centralpark_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全485本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-050-centralpark
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39〜EP49 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_centralpark_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39〜EP49 の十一すべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1 + R2 + 正確性7制約）★★★

**5人（Antron McCray / Kevin Richardson / Yusef Salaam / Raymond Santana / Korey Wise）は虚偽自白で誤って有罪となり、full に exonerate された【The Exonerated Five】。彼らが暴行に関与したことを匂わせる絵・語を一切作らない（innocence 絶対）。物証のDNAは1990年に5人全員を除外し、2002年に Matias Reyes に一致（1 in 6,000,000,000）、Reyes は単独犯と自白、2002-12-19 に Justice Tejada が全 conviction を vacate。被害者 Trisha Meili は存命の survivor＝dignity をもって扱い、姿を一切描かない。暴行は一切描かない（clinical・非扇情）。Matias Reyes は服役中の実在の犯罪者＝顔・肖像なし・美化しない・事実として名指すのみ。Armstrong Report（2003・却下）は「却下された反対説」としてのみ扱い、5人がなお有罪かもしれないという含みを絶対に作らない。数値（interrogation の累積時間・per-person の服役年数/金額・Trump ad の費用・Gonzalez 殺害の月・Wise の収容施設）は hedged。捏造引用禁止。すべての実在人物に R2（顔・likeness なし・silhouette/手/影/象徴のみ）。**

## 1.1 R1/R2（生成ビジュアル全般）

1. **★R2（owner 改定・EP50）: 匿名・非識別の人物は可／実在人物の likeness は不可。** **匿名の一般人（実在の誰にも似せない・非識別のドラマ化スタンドイン）＝顔・身体を出してよい**（§5.11 の H シリーズ・専用 `[HSTYLE]`/`[HNEG]`）。ただし **実在人物の顔・likeness・肖像は作らない**＝5人・Trisha Meili（被害者）・Matias Reyes・Trump・**実在の**刑事/判事/検事を**似せて描かない**。**5人・Reyes 本人が示唆される所は非識別**（背向き/影/逆光/ソフト/象徴 silhouette）を既定に保つ＝5人は descending-height silhouette、Korey は taller-but-young spine silhouette、Reyes は separate colder silhouette。**被害者の描写・暴行の imagery は一切作らない（不変）。** 判事評言や verbatim は AE カード（B の担当）であって画像ではない。
2. **実在の自白調書・判決文・判例番号・新聞紙面・日付・DNA数値の可読文字を再現しない。** confession / lab report / newspaper front page / case citation / calendar / ID は雰囲気のみ（判読不能・"blurred into an unreadable smear"）。日付（1989 / 1989-04-19 / 2002-12-19 / 2014 / 2016）・年齢（14/14/15/15/16）・金額（$41M / $3.9M / ~$85,000）・DNA（1 in 6,000,000,000）は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。**Trump ad は空白の full-page 枠のみ**（headline / art を絶対に再現しない）。ロゴ/紙面は**ぼかして判読不能**に。
3. **被害者・暴行・現場を一切描かない。** park は **abstract（treeline・a lamp・cold）のみ**、crime imagery・re-enactment・injury・blood・weapon を作らない。Trisha Meili を象徴でも描かない。
4. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性7制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **R-INNOCENCE:** 5人が暴行に関与したことを匂わせる絵・語を作らない。"the five did it / were involved / guilty / attackers / perpetrators" を書かない。5人は **coerced false confession の被害者・exonerated**。**Armstrong Report は「却下された反対説」としてのみ**（"the five may still be guilty" を書かない）。
2. **R-VICTIM:** 被害者 Trisha Meili に dignity。姿・likeness を描かない・record 以上に naming しない・暴行を graphic に描かない。"graphic assault / rape depiction / injured woman / bleeding victim" を書かない。
3. **R-REYES:** Matias Reyes は established facts のみ（連続強姦殺人犯・33⅓-to-life・2002自白・単独犯・DNA一致）。lurid detail・美化・hero化を書かない。"glorified / heroic Reyes" を書かない。
4. **R-NUM:** hedged 数値を断定で焼かない。interrogation の累積時間（firm は「少なくとも7時間 unrecorded」・それ以上は reported）・per-person の年数/金額・Trump ad ~$85,000・Gonzalez 殺害の月・Wise の施設は**画像に可読で描かない**（AE/figures＝B）。断定表現（"exactly 30 hours" 等）を書かない。
5. **R-FACE（owner 改定）:** **匿名・非識別の人物は可**（§5.11・§1.1）。**実在人物の likeness ゼロ**＝"likeness of <the five/Meili/Reyes/Trump/a real detective/judge/prosecutor> / face of <those names> / recognizable real person / real-person likeness / mugshot of a real person / deepfake" を書かない。**匿名一般人の描写（"anonymous / generic / non-identifiable person, faces turned or in shadow"）は許可。**
6. **R-DOCHL:** **dochighlight（黒バー/box/underline の figure）を作らない・言及しない。** `tags`/`caption_hint`/`notes`/ファイル名に `dochighlight` の文字列を書かない（grep で 0 を保つ）。owner が EP40/41/42 で3回 flag した「バグに見える」図。
7. **R-QUOTE:** 捏造引用禁止。verbatim は verified なもの＋attribution のみ（AE＝B の担当）。画像に可読の引用を描かない。

## 1.3 機械ゲート（`build_centralpark_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
# ★owner 改定（EP50）: 匿名・非識別の人物は許可。実在人物の likeness だけを弾く。
# 汎用の "portrait"/"identifiable face"/"front-facing person"/"human face" は
# もう BANNED にしない（匿名スタンドインを巻き込むため）。実在人物の likeness のみ FAIL。
BANNED_PORTRAIT = re.compile(
    r"likeness of (a )?(real|specific|named) person|real[- ]person likeness|"
    r"face of (antron|mccray|kevin|richardson|yusef|salaam|raymond|santana|korey|wise|trisha|meili|matias|reyes|trump)|"
    r"likeness of (antron|mccray|kevin|richardson|yusef|salaam|raymond|santana|korey|wise|trisha|meili|matias|reyes|trump)|"
    r"recognizable (real person|celebrity)|identifiable real person|"
    r"mugshot of (a )?real person|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"the five (did it|were involved|are guilty|committed|attacked)|"
    r"(guilty|involved) (teens|boys|five|defendants)|"
    r"they (raped|attacked|assaulted) (her|the jogger|the victim)|"
    r"the five (may|might) (still )?be guilty|"
    r"(graphic|explicit) (assault|rape)|bleeding (victim|woman|jogger)|"
    r"(glorified|heroic|admirable) reyes|"
    r"exactly (30|thirty) hours|"
    r"trump ad (headline|artwork|reproduction)|newspaper front page reproduction|"
    r"poverty ?porn|dochighlight",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1〜4・6を機械化したもの。プロンプト・タグ・`caption_hint`・注記のどこにも該当語を書かない。**許容:** "coerced / false confession / wrongfully convicted / exonerated / DNA excluded all five / matched Reyes alone / the state reversed course / vacated / attenuated the case / a room built to produce a yes"・**"anonymous / generic / non-identifiable person, faces turned or in shadow"（匿名スタンドイン・owner 改定・§5.11）**。禁止は「5人の有罪化/関与化」・「被害者の描写・暴行 imagery」・「Reyes の美化」・「hedged 数値の断定」・「Trump ad の art/headline 再現」・「dochighlight」・**「実在人物の likeness」（匿名の一般人は可）**。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP50_centralpark_PRODUCTION_SPEC.v001.json`。** 古い 56-min 資料の値は使うな。

```
words_total          = 10,715（LOCKED script・3x self-checked）
narration_seconds    = 3,606.0（= 60.10分・provisional・FINAL は measured TTS forced-align で上書き）
wpm_used             = 178.3
total_seconds        = 3,626.5（hook 8.0 + OPENING 3.5 + narration 3606.0 + endcard 9.0）= 60:27
durationInFrames     = 108,795（provisional・fps30）
mean_shot            = 3.109秒/カット（SPEC derived）・max_shot 7.0
視覚 acts             = 7（HOOK/OPENING は別レイヤー）
Act 秒（provisional）: ACT1 6.9分 / ACT2 12.6分（最長・engine）/ ACT3 9.8分 / ACT4 10.6分 /
                      ACT5 9.7分 / ACT6 5.3分 / ACT7 5.2分
```

**Aにとっての意味は1つ:** > **総カット 1,160 / distinct 1,000 / 初出 86.21% = still 430 + factory 485 + motion 85。**（§3 で積算）

> **注意（命名差）:** SPEC の視覚 act は7つ。**still は 430 本の固有プロンプトを持つ**ため、still の資産 ID は **S001..S430**（1プロンプト＝1枚）で採番する。7 act ＋ HOOK/OPENING に 430 枚を配分する（engine の ACT2 と climax の ACT5 が最も厚い）。`covers_scene_id` は still 資産 ID 空間（S001..S430）を指す（§7.3）。

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **430枚** | 505カット | 1.174回(≤2) | **430本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **485本** | 485カット | **各1回(1)** | 在庫 11,000本超から選抜（§7）・全点目視・EP39〜49 と sha256 被りゼロ |
| **i2v モーション** | **85本** | 170カット | 各2回(≤2) | 85本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **1,000点** | **1,160カット** | | |
| 合成レイヤー（particle/light/vfx） | 60本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の生成バッチ（本編カットに出ない i2v 種を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **430枚** | 430プロンプト × 1枚（バリエーション0） |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **85枚** | 85種プロンプト × 1枚（バリエーション0） |
| **SDXL 生成バッチ合計** | **430 + 85 = 515枚（各1回）** | **variants 指定なし（＝1枚）** |

> **サムネは新規生成しない。** 完成後に body 430枚から**ちょうど8枚**を `also_thumb:true` で流用選抜（追加生成ゼロ＝1シーン1枚前提を崩さない）。**role=thumb / still_thumb を作らない。**

> **★紙芝居回避（EP40 の最大の失敗）:** **still-cut 505 / (factory 485 + i2v 170)=video 655** で **still-share 43.53% ≤45%・motion coverage 56.47% ≥45%** を構造的に保証する（§3.3）。**stillを増やしてfactoryを削るな。factory 485 と motion 170 が still-share≤0.45 を守る。余裕は 0.15%pt しかない。**

## 3.2 still 430枚・factory 485本・i2v 85本の幕別配分（★still は確定・factory/i2v は目安。合計だけが確定）

| 区間 | still（S番号・確定） | factory（目安） | i2v（確定合計85） | thumb anchor |
|---|---|---|---|---|
| HOOK+OPENING | **20**（S001–S020） | 12 | 3（M01–M03） | S001, S018 |
| ACT1「The Night」 | **80**（S021–S100） | 70 | 12（M04–M15） | S095 |
| ACT2「The Interrogations」（engine・最密） | **110**（S101–S210） | 70 | 18（M16–M33） | S210 |
| ACT3「The Trials」 | **58**（S211–S268） | 65 | 12（M34–M45） | S268 |
| ACT4「The Lost Years」 | **63**（S269–S331） | 70 | 12（M46–M57） | S331 |
| ACT5「The Confession & the DNA」（climax・最密②） | **40**（S332–S371） | 55 | 16（M58–M73） | — |
| ACT6「Exoneration & Reckoning」 | **44**（S372–S415） | 50 | 8（M74–M81） | S372, S408 |
| ACT7「What a Confession Is Worth」 | **15**（S416–S430） | 20 | 4（M82–M85） | — |
| 繋ぎ（covers_scene_id:null） | — | 73 | — | — |
| **合計** | **430** | **485** | **85** | **8** |

> **still の per-act 数（20/80/110/58/63/40/44/15＝430）は確定**（§5 の motif ライブラリがこの配分で組まれている）。ACT2（虚偽自白の engine）が最厚110、ACT5（DNA climax）は AE set-piece（DNA_LADDER 等）と i2v flood が主役なので still は40だが motion は最多16。**幕別の factory/i2v 内訳は目安値**（合計 485 / 85 のみ確定）。ゲートは factory を各1回・合計 485、motion 各2回・合計170でしか見ない。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 1,160 = still 505 + factory 485 + i2v 170
[2] 平均ショット長 = narration 3606.0 / 1160 = 3.109秒/カット  ✓ (SPEC mean_shot 3.109・≤7.0)
[3] 静止画占有率(check_animation_mix) = 505/1160 = 43.53%  ✓ ≤45%（SPEC still_share 0.4353・余裕0.15%pt）
[4] motion coverage = (485+170)/1160 = 655/1160 = 56.47%     ✓ ≥45%
[5] per-asset 上限: still 505/430=1.174(≤2) / factory 485/485=1.0(≤1) / motion 170/85=2.0(≤2)  ✓
[6] first-use share = 1000/1160 = 0.8621                   ✓ ≥0.70（SPEC 一致）
[7] factory 下限 = 3606/30 = 120.2 → ≥121本。設計値 485本 ✓（still-share≤0.45 を守る）
```

> **[3] の余裕は 0.15%pt しかない。** still が430本を割ったら §6.3 の再生成で回復させ、**still-cut 505 を増やさない**（B側の shotlist が505で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-050-centralpark/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `centralpark_assets.v1`（固定文字列）
**生産者:** `scripts/build_centralpark_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数 / also_thumb集合 を一字一致。** role enum は **`body | i2v_source | reject` のみ**（`thumb`/`still_thumb` を作らない）。サムネは `also_thumb:true` の body still **ちょうど8枚**。overlay は **ちょうど60本**。

## 4.1 スキーマ（`centralpark_assets.v1`）

```jsonc
{
  "schema_version": "centralpark_assets.v1",
  "episode_id": "PD-2026-050-centralpark",
  "slug": "centralpark",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_centralpark_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 430,         // ==430
    "still_i2v_source": 85,    // ==85
    "motion": 85,              // ==85
    "factory": 485,            // ==485
    "overlay": 60              // ==60（distinct 素材に数えない）
  },
  "stills":  [ /* §4.3: body 430 (CPK-S001..S430) + i2v_source 85 (CPK-MS01..MS85) */ ],
  "motion":  [ /* §4.5: CPK-M01..M85 全85本・public_path 必須（★非空） */ ],
  "factory": [ /* §4.4: 485本・public_path 必須（★非空・EP45事故回避の核心） */ ],
  "overlay": [ /* §4.6: 60本 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例）

```jsonc
{
  "asset_id": "CPK-S001",                 // body: ^CPK-S\d{3}$（001..430） / i2v種: ^CPK-MS\d{2}$
  "scene_id": "S001",                     // still 資産 ID 空間（§5.9 のプロンプト行に対応・S001..S430）
  "role": "body",                         // body|i2v_source|reject（各1枚・バリエーション概念なし）
  "also_thumb": false,                    // body から8枚だけ true（§4.3・追加生成しない）
  "act": 0,                               // 0=HOOK/OPENING, 1..7=ACT1..ACT7
  "path": "H:/pd-media/assets/ai/centralpark/S001.png",
  "depth_path": "H:/pd-media/assets/ai/centralpark/S001_depth.png",   // role=="body" は実在必須
  "public_path": "centralpark/img/S001.png",   // role=="body" のみ非null
  "width": 3840, "height": 2160,          // 長辺>=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 24.0,
  "tags": ["interrogation_room","empty_chair","cold_cyan_light","off_rec_light","symbolic","no_face"],
  "caption_hint": "an empty interrogation-room chair found by a single cold-cyan light, a steel table and an unlit REC lamp, no person, no readable text",
  "seed": 0, "model": "juggernautXL_ragnarokBy",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
         "has_identifiable_real_person": false, "has_human_body": false,
         "has_identifiable_face": false, "notes": ""}
         // ★owner 改定: 匿名人体は可（has_human_body:true でも reject しない）。
         // reject トリガは has_readable_text か has_identifiable_real_person（実在 likeness）のみ。
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="centralpark_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 430 / i2v_source 85 / motion 85 / factory 485 / overlay 60）に**一致**
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. **★owner 改定:** `qc.has_readable_text==true` **または** `qc.has_identifiable_real_person==true`（＝実在人物として識別可能）は `role=="reject"`。**`qc.has_human_body==true` はもはや reject 条件ではない**（匿名人体は可）。**`qc.has_identifiable_face` は「実在人物として識別可能な顔」を意味するよう再定義**＝匿名・非識別の顔は可。QC は各人物画像で `has_identifiable_real_person`（実在 likeness か）を判定し、true なら reject。H シリーズ（§5.11）は `has_human_body:true`/`has_identifiable_real_person:false`/`has_readable_text:false`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（i2v_source は `^CPK-MS\d{2}$`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39〜EP49（十一話）の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど8**、かつ **`scene_id` 集合が §4.3 の8枚集合と完全一致**（body からの流用。**この集合は CODEX_B と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど60**
17. ★**`factory` 配列長==485 かつ全エントリ `public_path` が非空**（EP45 事故回避・空配列/stub を許さない）
18. ★**`motion` 配列長==85 かつ全エントリ `public_path` が非空**（同上）

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 430枚（S001..S430）= §5.9 の430プロンプトの生成物。各1枚。
2. i2v_source 85枚（MS01..MS85 / 種画像 M01_src..M85_src）= §8.1a の85種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち §4.3a の8枚に true（追加生成しない）
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

### 4.3a ★also_thumb 集合（ちょうど8枚・CODEX_B と一字一致必須）

```
{ CPK-S001 (empty chair + cold-cyan light),
  CPK-S018 (OFF REC lamp — the unrecorded hours signature),
  CPK-S095 (five descending child-height silhouettes),
  CPK-S210 (the interrogation room / clock),
  CPK-S268 (cold-cyan DNA bands — the exclusion),
  CPK-S331 (Korey spine silhouette),
  CPK-S372 (vacatur / dissolving signature),
  CPK-S408 (dawn horizon — the first warm note) }
```

> thumbnail concept（SCALE_NOTE / STRUCTURE 由来）= 五つの empty chairs、単一 cold-cyan light、**REC ドット OFF**、"NO CAMERA. NO LAWYER. NO MATCH."（no faces・ad-safe）。★この8集合は §5 の該当 S番号に必ず該当 motif を置くこと（§5 の motif ライブラリで anchor 指定済み）。

## 4.4 ★`factory[]` 全485エントリ（★必ず実体化・public_path 非空。EP45事故回避の核心）

> `select_centralpark_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id）/`path`（`H:/pd-media/assets/factory/...`）/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。** 各 public_path は `centralpark/factory/F0NN_<subtype>.mp4`。`type:"backgrounds"`, `kind:"video"`。covers は still 資産 ID 空間（§7.3）。**subtype の `_02`/`_03`… は「同一検索テーマの別クリップ」の意で、別 sha256・別素材（同一ファイルの重複ではない）。**

```jsonc
// HOOK+OPENING (act 0) — 12
{ "public_path":"centralpark/factory/F001_dark_institutional_room_cold.mp4", "act":0, "covers_scene_id":"S002", "subtype":"dark_institutional_room_cold" }
{ "public_path":"centralpark/factory/F002_cold_room_low_light.mp4", "act":0, "covers_scene_id":"S018", "subtype":"cold_room_low_light" }
{ "public_path":"centralpark/factory/F003_steel_table_room_ambient.mp4", "act":0, "covers_scene_id":null, "subtype":"steel_table_room_ambient" }
{ "public_path":"centralpark/factory/F004_unlit_room_single_lamp.mp4", "act":0, "covers_scene_id":null, "subtype":"unlit_room_single_lamp" }
{ "public_path":"centralpark/factory/F005_institutional_doorway_dark.mp4", "act":0, "covers_scene_id":null, "subtype":"institutional_doorway_dark" }
{ "public_path":"centralpark/factory/F006_cold_fluorescent_room.mp4", "act":0, "covers_scene_id":null, "subtype":"cold_fluorescent_room" }
{ "public_path":"centralpark/factory/F007_empty_office_night_cold.mp4", "act":0, "covers_scene_id":null, "subtype":"empty_office_night_cold" }
{ "public_path":"centralpark/factory/F008_bare_room_shadow.mp4", "act":0, "covers_scene_id":null, "subtype":"bare_room_shadow" }
{ "public_path":"centralpark/factory/F009_dark_institutional_room_cold_02.mp4", "act":0, "covers_scene_id":null, "subtype":"dark_institutional_room_cold_02" }
{ "public_path":"centralpark/factory/F010_cold_room_low_light_02.mp4", "act":0, "covers_scene_id":null, "subtype":"cold_room_low_light_02" }
{ "public_path":"centralpark/factory/F011_steel_table_room_ambient_02.mp4", "act":0, "covers_scene_id":null, "subtype":"steel_table_room_ambient_02" }
{ "public_path":"centralpark/factory/F012_unlit_room_single_lamp_02.mp4", "act":0, "covers_scene_id":null, "subtype":"unlit_room_single_lamp_02" }
// ACT1 (act 1) — 70
{ "public_path":"centralpark/factory/F013_nyc_street_1989_night.mp4", "act":1, "covers_scene_id":"S021", "subtype":"nyc_street_1989_night" }
{ "public_path":"centralpark/factory/F014_subway_car_interior_empty.mp4", "act":1, "covers_scene_id":"S030", "subtype":"subway_car_interior_empty" }
{ "public_path":"centralpark/factory/F015_subway_platform_cold.mp4", "act":1, "covers_scene_id":"S045", "subtype":"subway_platform_cold" }
{ "public_path":"centralpark/factory/F016_manhattan_avenue_night.mp4", "act":1, "covers_scene_id":"S060", "subtype":"manhattan_avenue_night" }
{ "public_path":"centralpark/factory/F017_tenement_block_night.mp4", "act":1, "covers_scene_id":"S075", "subtype":"tenement_block_night" }
{ "public_path":"centralpark/factory/F018_precinct_exterior_night.mp4", "act":1, "covers_scene_id":"S088", "subtype":"precinct_exterior_night" }
{ "public_path":"centralpark/factory/F019_city_night_traffic_long.mp4", "act":1, "covers_scene_id":"S095", "subtype":"city_night_traffic_long" }
{ "public_path":"centralpark/factory/F020_park_treeline_night_abstract.mp4", "act":1, "covers_scene_id":null, "subtype":"park_treeline_night_abstract" }
{ "public_path":"centralpark/factory/F021_park_lamp_path_night.mp4", "act":1, "covers_scene_id":null, "subtype":"park_lamp_path_night" }
{ "public_path":"centralpark/factory/F022_newsroom_ambient_dim.mp4", "act":1, "covers_scene_id":null, "subtype":"newsroom_ambient_dim" }
{ "public_path":"centralpark/factory/F023_payphone_street_night.mp4", "act":1, "covers_scene_id":null, "subtype":"payphone_street_night" }
{ "public_path":"centralpark/factory/F024_city_skyline_night_cold.mp4", "act":1, "covers_scene_id":null, "subtype":"city_skyline_night_cold" }
{ "public_path":"centralpark/factory/F025_cold_sidewalk_night.mp4", "act":1, "covers_scene_id":null, "subtype":"cold_sidewalk_night" }
{ "public_path":"centralpark/factory/F026_apartment_window_lights_night.mp4", "act":1, "covers_scene_id":null, "subtype":"apartment_window_lights_night" }
{ "public_path":"centralpark/factory/F027_bus_stop_night_empty.mp4", "act":1, "covers_scene_id":null, "subtype":"bus_stop_night_empty" }
{ "public_path":"centralpark/factory/F028_street_steam_grate_night.mp4", "act":1, "covers_scene_id":null, "subtype":"street_steam_grate_night" }
{ "public_path":"centralpark/factory/F029_institutional_hallway_cold.mp4", "act":1, "covers_scene_id":null, "subtype":"institutional_hallway_cold" }
{ "public_path":"centralpark/factory/F030_brownstone_stoop_night.mp4", "act":1, "covers_scene_id":null, "subtype":"brownstone_stoop_night" }
{ "public_path":"centralpark/factory/F031_harlem_street_night_1989.mp4", "act":1, "covers_scene_id":null, "subtype":"harlem_street_night_1989" }
{ "public_path":"centralpark/factory/F032_overpass_underpass_night.mp4", "act":1, "covers_scene_id":null, "subtype":"overpass_underpass_night" }
{ "public_path":"centralpark/factory/F033_nyc_street_1989_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"nyc_street_1989_night_02" }
{ "public_path":"centralpark/factory/F034_subway_car_interior_empty_02.mp4", "act":1, "covers_scene_id":null, "subtype":"subway_car_interior_empty_02" }
{ "public_path":"centralpark/factory/F035_subway_platform_cold_02.mp4", "act":1, "covers_scene_id":null, "subtype":"subway_platform_cold_02" }
{ "public_path":"centralpark/factory/F036_manhattan_avenue_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"manhattan_avenue_night_02" }
{ "public_path":"centralpark/factory/F037_tenement_block_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"tenement_block_night_02" }
{ "public_path":"centralpark/factory/F038_precinct_exterior_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"precinct_exterior_night_02" }
{ "public_path":"centralpark/factory/F039_city_night_traffic_long_02.mp4", "act":1, "covers_scene_id":null, "subtype":"city_night_traffic_long_02" }
{ "public_path":"centralpark/factory/F040_park_treeline_night_abstract_02.mp4", "act":1, "covers_scene_id":null, "subtype":"park_treeline_night_abstract_02" }
{ "public_path":"centralpark/factory/F041_park_lamp_path_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"park_lamp_path_night_02" }
{ "public_path":"centralpark/factory/F042_newsroom_ambient_dim_02.mp4", "act":1, "covers_scene_id":null, "subtype":"newsroom_ambient_dim_02" }
{ "public_path":"centralpark/factory/F043_payphone_street_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"payphone_street_night_02" }
{ "public_path":"centralpark/factory/F044_city_skyline_night_cold_02.mp4", "act":1, "covers_scene_id":null, "subtype":"city_skyline_night_cold_02" }
{ "public_path":"centralpark/factory/F045_cold_sidewalk_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"cold_sidewalk_night_02" }
{ "public_path":"centralpark/factory/F046_apartment_window_lights_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"apartment_window_lights_night_02" }
{ "public_path":"centralpark/factory/F047_bus_stop_night_empty_02.mp4", "act":1, "covers_scene_id":null, "subtype":"bus_stop_night_empty_02" }
{ "public_path":"centralpark/factory/F048_street_steam_grate_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"street_steam_grate_night_02" }
{ "public_path":"centralpark/factory/F049_institutional_hallway_cold_02.mp4", "act":1, "covers_scene_id":null, "subtype":"institutional_hallway_cold_02" }
{ "public_path":"centralpark/factory/F050_brownstone_stoop_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"brownstone_stoop_night_02" }
{ "public_path":"centralpark/factory/F051_harlem_street_night_1989_02.mp4", "act":1, "covers_scene_id":null, "subtype":"harlem_street_night_1989_02" }
{ "public_path":"centralpark/factory/F052_overpass_underpass_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"overpass_underpass_night_02" }
{ "public_path":"centralpark/factory/F053_nyc_street_1989_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"nyc_street_1989_night_03" }
{ "public_path":"centralpark/factory/F054_subway_car_interior_empty_03.mp4", "act":1, "covers_scene_id":null, "subtype":"subway_car_interior_empty_03" }
{ "public_path":"centralpark/factory/F055_subway_platform_cold_03.mp4", "act":1, "covers_scene_id":null, "subtype":"subway_platform_cold_03" }
{ "public_path":"centralpark/factory/F056_manhattan_avenue_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"manhattan_avenue_night_03" }
{ "public_path":"centralpark/factory/F057_tenement_block_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"tenement_block_night_03" }
{ "public_path":"centralpark/factory/F058_precinct_exterior_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"precinct_exterior_night_03" }
{ "public_path":"centralpark/factory/F059_city_night_traffic_long_03.mp4", "act":1, "covers_scene_id":null, "subtype":"city_night_traffic_long_03" }
{ "public_path":"centralpark/factory/F060_park_treeline_night_abstract_03.mp4", "act":1, "covers_scene_id":null, "subtype":"park_treeline_night_abstract_03" }
{ "public_path":"centralpark/factory/F061_park_lamp_path_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"park_lamp_path_night_03" }
{ "public_path":"centralpark/factory/F062_newsroom_ambient_dim_03.mp4", "act":1, "covers_scene_id":null, "subtype":"newsroom_ambient_dim_03" }
{ "public_path":"centralpark/factory/F063_payphone_street_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"payphone_street_night_03" }
{ "public_path":"centralpark/factory/F064_city_skyline_night_cold_03.mp4", "act":1, "covers_scene_id":null, "subtype":"city_skyline_night_cold_03" }
{ "public_path":"centralpark/factory/F065_cold_sidewalk_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"cold_sidewalk_night_03" }
{ "public_path":"centralpark/factory/F066_apartment_window_lights_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"apartment_window_lights_night_03" }
{ "public_path":"centralpark/factory/F067_bus_stop_night_empty_03.mp4", "act":1, "covers_scene_id":null, "subtype":"bus_stop_night_empty_03" }
{ "public_path":"centralpark/factory/F068_street_steam_grate_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"street_steam_grate_night_03" }
{ "public_path":"centralpark/factory/F069_institutional_hallway_cold_03.mp4", "act":1, "covers_scene_id":null, "subtype":"institutional_hallway_cold_03" }
{ "public_path":"centralpark/factory/F070_brownstone_stoop_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"brownstone_stoop_night_03" }
{ "public_path":"centralpark/factory/F071_harlem_street_night_1989_03.mp4", "act":1, "covers_scene_id":null, "subtype":"harlem_street_night_1989_03" }
{ "public_path":"centralpark/factory/F072_overpass_underpass_night_03.mp4", "act":1, "covers_scene_id":null, "subtype":"overpass_underpass_night_03" }
{ "public_path":"centralpark/factory/F073_nyc_street_1989_night_04.mp4", "act":1, "covers_scene_id":null, "subtype":"nyc_street_1989_night_04" }
{ "public_path":"centralpark/factory/F074_subway_car_interior_empty_04.mp4", "act":1, "covers_scene_id":null, "subtype":"subway_car_interior_empty_04" }
{ "public_path":"centralpark/factory/F075_subway_platform_cold_04.mp4", "act":1, "covers_scene_id":null, "subtype":"subway_platform_cold_04" }
{ "public_path":"centralpark/factory/F076_manhattan_avenue_night_04.mp4", "act":1, "covers_scene_id":null, "subtype":"manhattan_avenue_night_04" }
{ "public_path":"centralpark/factory/F077_tenement_block_night_04.mp4", "act":1, "covers_scene_id":null, "subtype":"tenement_block_night_04" }
{ "public_path":"centralpark/factory/F078_precinct_exterior_night_04.mp4", "act":1, "covers_scene_id":null, "subtype":"precinct_exterior_night_04" }
{ "public_path":"centralpark/factory/F079_city_night_traffic_long_04.mp4", "act":1, "covers_scene_id":null, "subtype":"city_night_traffic_long_04" }
{ "public_path":"centralpark/factory/F080_park_treeline_night_abstract_04.mp4", "act":1, "covers_scene_id":null, "subtype":"park_treeline_night_abstract_04" }
{ "public_path":"centralpark/factory/F081_park_lamp_path_night_04.mp4", "act":1, "covers_scene_id":null, "subtype":"park_lamp_path_night_04" }
{ "public_path":"centralpark/factory/F082_newsroom_ambient_dim_04.mp4", "act":1, "covers_scene_id":null, "subtype":"newsroom_ambient_dim_04" }
// ACT2 (act 2) — 70
{ "public_path":"centralpark/factory/F083_interrogation_room_general_cold.mp4", "act":2, "covers_scene_id":"S101", "subtype":"interrogation_room_general_cold" }
{ "public_path":"centralpark/factory/F084_fluorescent_corridor_institutional.mp4", "act":2, "covers_scene_id":"S120", "subtype":"fluorescent_corridor_institutional" }
{ "public_path":"centralpark/factory/F085_closed_door_cold_hallway.mp4", "act":2, "covers_scene_id":"S140", "subtype":"closed_door_cold_hallway" }
{ "public_path":"centralpark/factory/F086_steel_chair_table_ambient.mp4", "act":2, "covers_scene_id":"S160", "subtype":"steel_chair_table_ambient" }
{ "public_path":"centralpark/factory/F087_wall_clock_cold_room.mp4", "act":2, "covers_scene_id":"S180", "subtype":"wall_clock_cold_room" }
{ "public_path":"centralpark/factory/F088_precinct_interior_night.mp4", "act":2, "covers_scene_id":"S200", "subtype":"precinct_interior_night" }
{ "public_path":"centralpark/factory/F089_cold_waiting_room_bench.mp4", "act":2, "covers_scene_id":"S210", "subtype":"cold_waiting_room_bench" }
{ "public_path":"centralpark/factory/F090_narrow_institutional_hall.mp4", "act":2, "covers_scene_id":null, "subtype":"narrow_institutional_hall" }
{ "public_path":"centralpark/factory/F091_holding_area_corridor_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"holding_area_corridor_cold" }
{ "public_path":"centralpark/factory/F092_office_desk_lamp_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"office_desk_lamp_cold" }
{ "public_path":"centralpark/factory/F093_file_cabinets_room_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"file_cabinets_room_dim" }
{ "public_path":"centralpark/factory/F094_one_way_glass_room_abstract.mp4", "act":2, "covers_scene_id":null, "subtype":"one_way_glass_room_abstract" }
{ "public_path":"centralpark/factory/F095_vending_machine_hallway_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"vending_machine_hallway_cold" }
{ "public_path":"centralpark/factory/F096_stairwell_institutional_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"stairwell_institutional_cold" }
{ "public_path":"centralpark/factory/F097_door_light_gap_dark.mp4", "act":2, "covers_scene_id":null, "subtype":"door_light_gap_dark" }
{ "public_path":"centralpark/factory/F098_interrogation_room_general_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"interrogation_room_general_cold_02" }
{ "public_path":"centralpark/factory/F099_fluorescent_corridor_institutional_02.mp4", "act":2, "covers_scene_id":null, "subtype":"fluorescent_corridor_institutional_02" }
{ "public_path":"centralpark/factory/F100_closed_door_cold_hallway_02.mp4", "act":2, "covers_scene_id":null, "subtype":"closed_door_cold_hallway_02" }
{ "public_path":"centralpark/factory/F101_steel_chair_table_ambient_02.mp4", "act":2, "covers_scene_id":null, "subtype":"steel_chair_table_ambient_02" }
{ "public_path":"centralpark/factory/F102_wall_clock_cold_room_02.mp4", "act":2, "covers_scene_id":null, "subtype":"wall_clock_cold_room_02" }
{ "public_path":"centralpark/factory/F103_precinct_interior_night_02.mp4", "act":2, "covers_scene_id":null, "subtype":"precinct_interior_night_02" }
{ "public_path":"centralpark/factory/F104_cold_waiting_room_bench_02.mp4", "act":2, "covers_scene_id":null, "subtype":"cold_waiting_room_bench_02" }
{ "public_path":"centralpark/factory/F105_narrow_institutional_hall_02.mp4", "act":2, "covers_scene_id":null, "subtype":"narrow_institutional_hall_02" }
{ "public_path":"centralpark/factory/F106_holding_area_corridor_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"holding_area_corridor_cold_02" }
{ "public_path":"centralpark/factory/F107_office_desk_lamp_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"office_desk_lamp_cold_02" }
{ "public_path":"centralpark/factory/F108_file_cabinets_room_dim_02.mp4", "act":2, "covers_scene_id":null, "subtype":"file_cabinets_room_dim_02" }
{ "public_path":"centralpark/factory/F109_one_way_glass_room_abstract_02.mp4", "act":2, "covers_scene_id":null, "subtype":"one_way_glass_room_abstract_02" }
{ "public_path":"centralpark/factory/F110_vending_machine_hallway_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"vending_machine_hallway_cold_02" }
{ "public_path":"centralpark/factory/F111_stairwell_institutional_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"stairwell_institutional_cold_02" }
{ "public_path":"centralpark/factory/F112_door_light_gap_dark_02.mp4", "act":2, "covers_scene_id":null, "subtype":"door_light_gap_dark_02" }
{ "public_path":"centralpark/factory/F113_interrogation_room_general_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"interrogation_room_general_cold_03" }
{ "public_path":"centralpark/factory/F114_fluorescent_corridor_institutional_03.mp4", "act":2, "covers_scene_id":null, "subtype":"fluorescent_corridor_institutional_03" }
{ "public_path":"centralpark/factory/F115_closed_door_cold_hallway_03.mp4", "act":2, "covers_scene_id":null, "subtype":"closed_door_cold_hallway_03" }
{ "public_path":"centralpark/factory/F116_steel_chair_table_ambient_03.mp4", "act":2, "covers_scene_id":null, "subtype":"steel_chair_table_ambient_03" }
{ "public_path":"centralpark/factory/F117_wall_clock_cold_room_03.mp4", "act":2, "covers_scene_id":null, "subtype":"wall_clock_cold_room_03" }
{ "public_path":"centralpark/factory/F118_precinct_interior_night_03.mp4", "act":2, "covers_scene_id":null, "subtype":"precinct_interior_night_03" }
{ "public_path":"centralpark/factory/F119_cold_waiting_room_bench_03.mp4", "act":2, "covers_scene_id":null, "subtype":"cold_waiting_room_bench_03" }
{ "public_path":"centralpark/factory/F120_narrow_institutional_hall_03.mp4", "act":2, "covers_scene_id":null, "subtype":"narrow_institutional_hall_03" }
{ "public_path":"centralpark/factory/F121_holding_area_corridor_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"holding_area_corridor_cold_03" }
{ "public_path":"centralpark/factory/F122_office_desk_lamp_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"office_desk_lamp_cold_03" }
{ "public_path":"centralpark/factory/F123_file_cabinets_room_dim_03.mp4", "act":2, "covers_scene_id":null, "subtype":"file_cabinets_room_dim_03" }
{ "public_path":"centralpark/factory/F124_one_way_glass_room_abstract_03.mp4", "act":2, "covers_scene_id":null, "subtype":"one_way_glass_room_abstract_03" }
{ "public_path":"centralpark/factory/F125_vending_machine_hallway_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"vending_machine_hallway_cold_03" }
{ "public_path":"centralpark/factory/F126_stairwell_institutional_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"stairwell_institutional_cold_03" }
{ "public_path":"centralpark/factory/F127_door_light_gap_dark_03.mp4", "act":2, "covers_scene_id":null, "subtype":"door_light_gap_dark_03" }
{ "public_path":"centralpark/factory/F128_interrogation_room_general_cold_04.mp4", "act":2, "covers_scene_id":null, "subtype":"interrogation_room_general_cold_04" }
{ "public_path":"centralpark/factory/F129_fluorescent_corridor_institutional_04.mp4", "act":2, "covers_scene_id":null, "subtype":"fluorescent_corridor_institutional_04" }
{ "public_path":"centralpark/factory/F130_closed_door_cold_hallway_04.mp4", "act":2, "covers_scene_id":null, "subtype":"closed_door_cold_hallway_04" }
{ "public_path":"centralpark/factory/F131_steel_chair_table_ambient_04.mp4", "act":2, "covers_scene_id":null, "subtype":"steel_chair_table_ambient_04" }
{ "public_path":"centralpark/factory/F132_wall_clock_cold_room_04.mp4", "act":2, "covers_scene_id":null, "subtype":"wall_clock_cold_room_04" }
{ "public_path":"centralpark/factory/F133_precinct_interior_night_04.mp4", "act":2, "covers_scene_id":null, "subtype":"precinct_interior_night_04" }
{ "public_path":"centralpark/factory/F134_cold_waiting_room_bench_04.mp4", "act":2, "covers_scene_id":null, "subtype":"cold_waiting_room_bench_04" }
{ "public_path":"centralpark/factory/F135_narrow_institutional_hall_04.mp4", "act":2, "covers_scene_id":null, "subtype":"narrow_institutional_hall_04" }
{ "public_path":"centralpark/factory/F136_holding_area_corridor_cold_04.mp4", "act":2, "covers_scene_id":null, "subtype":"holding_area_corridor_cold_04" }
{ "public_path":"centralpark/factory/F137_office_desk_lamp_cold_04.mp4", "act":2, "covers_scene_id":null, "subtype":"office_desk_lamp_cold_04" }
{ "public_path":"centralpark/factory/F138_file_cabinets_room_dim_04.mp4", "act":2, "covers_scene_id":null, "subtype":"file_cabinets_room_dim_04" }
{ "public_path":"centralpark/factory/F139_one_way_glass_room_abstract_04.mp4", "act":2, "covers_scene_id":null, "subtype":"one_way_glass_room_abstract_04" }
{ "public_path":"centralpark/factory/F140_vending_machine_hallway_cold_04.mp4", "act":2, "covers_scene_id":null, "subtype":"vending_machine_hallway_cold_04" }
{ "public_path":"centralpark/factory/F141_stairwell_institutional_cold_04.mp4", "act":2, "covers_scene_id":null, "subtype":"stairwell_institutional_cold_04" }
{ "public_path":"centralpark/factory/F142_door_light_gap_dark_04.mp4", "act":2, "covers_scene_id":null, "subtype":"door_light_gap_dark_04" }
{ "public_path":"centralpark/factory/F143_interrogation_room_general_cold_05.mp4", "act":2, "covers_scene_id":null, "subtype":"interrogation_room_general_cold_05" }
{ "public_path":"centralpark/factory/F144_fluorescent_corridor_institutional_05.mp4", "act":2, "covers_scene_id":null, "subtype":"fluorescent_corridor_institutional_05" }
{ "public_path":"centralpark/factory/F145_closed_door_cold_hallway_05.mp4", "act":2, "covers_scene_id":null, "subtype":"closed_door_cold_hallway_05" }
{ "public_path":"centralpark/factory/F146_steel_chair_table_ambient_05.mp4", "act":2, "covers_scene_id":null, "subtype":"steel_chair_table_ambient_05" }
{ "public_path":"centralpark/factory/F147_wall_clock_cold_room_05.mp4", "act":2, "covers_scene_id":null, "subtype":"wall_clock_cold_room_05" }
{ "public_path":"centralpark/factory/F148_precinct_interior_night_05.mp4", "act":2, "covers_scene_id":null, "subtype":"precinct_interior_night_05" }
{ "public_path":"centralpark/factory/F149_cold_waiting_room_bench_05.mp4", "act":2, "covers_scene_id":null, "subtype":"cold_waiting_room_bench_05" }
{ "public_path":"centralpark/factory/F150_narrow_institutional_hall_05.mp4", "act":2, "covers_scene_id":null, "subtype":"narrow_institutional_hall_05" }
{ "public_path":"centralpark/factory/F151_holding_area_corridor_cold_05.mp4", "act":2, "covers_scene_id":null, "subtype":"holding_area_corridor_cold_05" }
{ "public_path":"centralpark/factory/F152_office_desk_lamp_cold_05.mp4", "act":2, "covers_scene_id":null, "subtype":"office_desk_lamp_cold_05" }
// ACT3 (act 3) — 65
{ "public_path":"centralpark/factory/F153_ny_supreme_court_columns_day.mp4", "act":3, "covers_scene_id":"S211", "subtype":"ny_supreme_court_columns_day" }
{ "public_path":"centralpark/factory/F154_courthouse_marble_facade.mp4", "act":3, "covers_scene_id":"S225", "subtype":"courthouse_marble_facade" }
{ "public_path":"centralpark/factory/F155_courtroom_interior_empty_cold.mp4", "act":3, "covers_scene_id":"S240", "subtype":"courtroom_interior_empty_cold" }
{ "public_path":"centralpark/factory/F156_courthouse_corridor_long.mp4", "act":3, "covers_scene_id":"S255", "subtype":"courthouse_corridor_long" }
{ "public_path":"centralpark/factory/F157_marble_steps_courthouse.mp4", "act":3, "covers_scene_id":"S268", "subtype":"marble_steps_courthouse" }
{ "public_path":"centralpark/factory/F158_press_scrum_ambient_noface.mp4", "act":3, "covers_scene_id":null, "subtype":"press_scrum_ambient_noface" }
{ "public_path":"centralpark/factory/F159_tv_glow_dark_room.mp4", "act":3, "covers_scene_id":null, "subtype":"tv_glow_dark_room" }
{ "public_path":"centralpark/factory/F160_newspaper_press_rollers_abstract.mp4", "act":3, "covers_scene_id":null, "subtype":"newspaper_press_rollers_abstract" }
{ "public_path":"centralpark/factory/F161_courthouse_rotunda_cold.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_rotunda_cold" }
{ "public_path":"centralpark/factory/F162_judges_bench_empty_cold.mp4", "act":3, "covers_scene_id":null, "subtype":"judges_bench_empty_cold" }
{ "public_path":"centralpark/factory/F163_jury_box_empty.mp4", "act":3, "covers_scene_id":null, "subtype":"jury_box_empty" }
{ "public_path":"centralpark/factory/F164_gallery_benches_empty.mp4", "act":3, "covers_scene_id":null, "subtype":"gallery_benches_empty" }
{ "public_path":"centralpark/factory/F165_flag_courtroom_still.mp4", "act":3, "covers_scene_id":null, "subtype":"flag_courtroom_still" }
{ "public_path":"centralpark/factory/F166_law_books_shelf_dim.mp4", "act":3, "covers_scene_id":null, "subtype":"law_books_shelf_dim" }
{ "public_path":"centralpark/factory/F167_microphones_podium_noface.mp4", "act":3, "covers_scene_id":null, "subtype":"microphones_podium_noface" }
{ "public_path":"centralpark/factory/F168_ny_supreme_court_columns_day_02.mp4", "act":3, "covers_scene_id":null, "subtype":"ny_supreme_court_columns_day_02" }
{ "public_path":"centralpark/factory/F169_courthouse_marble_facade_02.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_marble_facade_02" }
{ "public_path":"centralpark/factory/F170_courtroom_interior_empty_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"courtroom_interior_empty_cold_02" }
{ "public_path":"centralpark/factory/F171_courthouse_corridor_long_02.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_corridor_long_02" }
{ "public_path":"centralpark/factory/F172_marble_steps_courthouse_02.mp4", "act":3, "covers_scene_id":null, "subtype":"marble_steps_courthouse_02" }
{ "public_path":"centralpark/factory/F173_press_scrum_ambient_noface_02.mp4", "act":3, "covers_scene_id":null, "subtype":"press_scrum_ambient_noface_02" }
{ "public_path":"centralpark/factory/F174_tv_glow_dark_room_02.mp4", "act":3, "covers_scene_id":null, "subtype":"tv_glow_dark_room_02" }
{ "public_path":"centralpark/factory/F175_newspaper_press_rollers_abstract_02.mp4", "act":3, "covers_scene_id":null, "subtype":"newspaper_press_rollers_abstract_02" }
{ "public_path":"centralpark/factory/F176_courthouse_rotunda_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_rotunda_cold_02" }
{ "public_path":"centralpark/factory/F177_judges_bench_empty_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"judges_bench_empty_cold_02" }
{ "public_path":"centralpark/factory/F178_jury_box_empty_02.mp4", "act":3, "covers_scene_id":null, "subtype":"jury_box_empty_02" }
{ "public_path":"centralpark/factory/F179_gallery_benches_empty_02.mp4", "act":3, "covers_scene_id":null, "subtype":"gallery_benches_empty_02" }
{ "public_path":"centralpark/factory/F180_flag_courtroom_still_02.mp4", "act":3, "covers_scene_id":null, "subtype":"flag_courtroom_still_02" }
{ "public_path":"centralpark/factory/F181_law_books_shelf_dim_02.mp4", "act":3, "covers_scene_id":null, "subtype":"law_books_shelf_dim_02" }
{ "public_path":"centralpark/factory/F182_microphones_podium_noface_02.mp4", "act":3, "covers_scene_id":null, "subtype":"microphones_podium_noface_02" }
{ "public_path":"centralpark/factory/F183_ny_supreme_court_columns_day_03.mp4", "act":3, "covers_scene_id":null, "subtype":"ny_supreme_court_columns_day_03" }
{ "public_path":"centralpark/factory/F184_courthouse_marble_facade_03.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_marble_facade_03" }
{ "public_path":"centralpark/factory/F185_courtroom_interior_empty_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"courtroom_interior_empty_cold_03" }
{ "public_path":"centralpark/factory/F186_courthouse_corridor_long_03.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_corridor_long_03" }
{ "public_path":"centralpark/factory/F187_marble_steps_courthouse_03.mp4", "act":3, "covers_scene_id":null, "subtype":"marble_steps_courthouse_03" }
{ "public_path":"centralpark/factory/F188_press_scrum_ambient_noface_03.mp4", "act":3, "covers_scene_id":null, "subtype":"press_scrum_ambient_noface_03" }
{ "public_path":"centralpark/factory/F189_tv_glow_dark_room_03.mp4", "act":3, "covers_scene_id":null, "subtype":"tv_glow_dark_room_03" }
{ "public_path":"centralpark/factory/F190_newspaper_press_rollers_abstract_03.mp4", "act":3, "covers_scene_id":null, "subtype":"newspaper_press_rollers_abstract_03" }
{ "public_path":"centralpark/factory/F191_courthouse_rotunda_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_rotunda_cold_03" }
{ "public_path":"centralpark/factory/F192_judges_bench_empty_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"judges_bench_empty_cold_03" }
{ "public_path":"centralpark/factory/F193_jury_box_empty_03.mp4", "act":3, "covers_scene_id":null, "subtype":"jury_box_empty_03" }
{ "public_path":"centralpark/factory/F194_gallery_benches_empty_03.mp4", "act":3, "covers_scene_id":null, "subtype":"gallery_benches_empty_03" }
{ "public_path":"centralpark/factory/F195_flag_courtroom_still_03.mp4", "act":3, "covers_scene_id":null, "subtype":"flag_courtroom_still_03" }
{ "public_path":"centralpark/factory/F196_law_books_shelf_dim_03.mp4", "act":3, "covers_scene_id":null, "subtype":"law_books_shelf_dim_03" }
{ "public_path":"centralpark/factory/F197_microphones_podium_noface_03.mp4", "act":3, "covers_scene_id":null, "subtype":"microphones_podium_noface_03" }
{ "public_path":"centralpark/factory/F198_ny_supreme_court_columns_day_04.mp4", "act":3, "covers_scene_id":null, "subtype":"ny_supreme_court_columns_day_04" }
{ "public_path":"centralpark/factory/F199_courthouse_marble_facade_04.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_marble_facade_04" }
{ "public_path":"centralpark/factory/F200_courtroom_interior_empty_cold_04.mp4", "act":3, "covers_scene_id":null, "subtype":"courtroom_interior_empty_cold_04" }
{ "public_path":"centralpark/factory/F201_courthouse_corridor_long_04.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_corridor_long_04" }
{ "public_path":"centralpark/factory/F202_marble_steps_courthouse_04.mp4", "act":3, "covers_scene_id":null, "subtype":"marble_steps_courthouse_04" }
{ "public_path":"centralpark/factory/F203_press_scrum_ambient_noface_04.mp4", "act":3, "covers_scene_id":null, "subtype":"press_scrum_ambient_noface_04" }
{ "public_path":"centralpark/factory/F204_tv_glow_dark_room_04.mp4", "act":3, "covers_scene_id":null, "subtype":"tv_glow_dark_room_04" }
{ "public_path":"centralpark/factory/F205_newspaper_press_rollers_abstract_04.mp4", "act":3, "covers_scene_id":null, "subtype":"newspaper_press_rollers_abstract_04" }
{ "public_path":"centralpark/factory/F206_courthouse_rotunda_cold_04.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_rotunda_cold_04" }
{ "public_path":"centralpark/factory/F207_judges_bench_empty_cold_04.mp4", "act":3, "covers_scene_id":null, "subtype":"judges_bench_empty_cold_04" }
{ "public_path":"centralpark/factory/F208_jury_box_empty_04.mp4", "act":3, "covers_scene_id":null, "subtype":"jury_box_empty_04" }
{ "public_path":"centralpark/factory/F209_gallery_benches_empty_04.mp4", "act":3, "covers_scene_id":null, "subtype":"gallery_benches_empty_04" }
{ "public_path":"centralpark/factory/F210_flag_courtroom_still_04.mp4", "act":3, "covers_scene_id":null, "subtype":"flag_courtroom_still_04" }
{ "public_path":"centralpark/factory/F211_law_books_shelf_dim_04.mp4", "act":3, "covers_scene_id":null, "subtype":"law_books_shelf_dim_04" }
{ "public_path":"centralpark/factory/F212_microphones_podium_noface_04.mp4", "act":3, "covers_scene_id":null, "subtype":"microphones_podium_noface_04" }
{ "public_path":"centralpark/factory/F213_ny_supreme_court_columns_day_05.mp4", "act":3, "covers_scene_id":null, "subtype":"ny_supreme_court_columns_day_05" }
{ "public_path":"centralpark/factory/F214_courthouse_marble_facade_05.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_marble_facade_05" }
{ "public_path":"centralpark/factory/F215_courtroom_interior_empty_cold_05.mp4", "act":3, "covers_scene_id":null, "subtype":"courtroom_interior_empty_cold_05" }
{ "public_path":"centralpark/factory/F216_courthouse_corridor_long_05.mp4", "act":3, "covers_scene_id":null, "subtype":"courthouse_corridor_long_05" }
{ "public_path":"centralpark/factory/F217_marble_steps_courthouse_05.mp4", "act":3, "covers_scene_id":null, "subtype":"marble_steps_courthouse_05" }
// ACT4 (act 4) — 70
{ "public_path":"centralpark/factory/F218_prison_wall_exterior_dusk.mp4", "act":4, "covers_scene_id":"S269", "subtype":"prison_wall_exterior_dusk" }
{ "public_path":"centralpark/factory/F219_institutional_window_light_abstract.mp4", "act":4, "covers_scene_id":"S285", "subtype":"institutional_window_light_abstract" }
{ "public_path":"centralpark/factory/F220_long_prison_corridor_cold.mp4", "act":4, "covers_scene_id":"S300", "subtype":"long_prison_corridor_cold" }
{ "public_path":"centralpark/factory/F221_chainlink_fence_cold_abstract.mp4", "act":4, "covers_scene_id":"S315", "subtype":"chainlink_fence_cold_abstract" }
{ "public_path":"centralpark/factory/F222_razor_wire_sky_abstract_distant.mp4", "act":4, "covers_scene_id":"S331", "subtype":"razor_wire_sky_abstract_distant" }
{ "public_path":"centralpark/factory/F223_upstate_facility_exterior_winter.mp4", "act":4, "covers_scene_id":null, "subtype":"upstate_facility_exterior_winter" }
{ "public_path":"centralpark/factory/F224_cell_window_light_abstract.mp4", "act":4, "covers_scene_id":null, "subtype":"cell_window_light_abstract" }
{ "public_path":"centralpark/factory/F225_concrete_yard_empty_cold.mp4", "act":4, "covers_scene_id":null, "subtype":"concrete_yard_empty_cold" }
{ "public_path":"centralpark/factory/F226_institutional_door_heavy_cold.mp4", "act":4, "covers_scene_id":null, "subtype":"institutional_door_heavy_cold" }
{ "public_path":"centralpark/factory/F227_seasons_sky_window_shift.mp4", "act":4, "covers_scene_id":null, "subtype":"seasons_sky_window_shift" }
{ "public_path":"centralpark/factory/F228_bare_bunk_room_abstract_noface.mp4", "act":4, "covers_scene_id":null, "subtype":"bare_bunk_room_abstract_noface" }
{ "public_path":"centralpark/factory/F229_prison_fence_snow_distant.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_fence_snow_distant" }
{ "public_path":"centralpark/factory/F230_watchtower_silhouette_distant.mp4", "act":4, "covers_scene_id":null, "subtype":"watchtower_silhouette_distant" }
{ "public_path":"centralpark/factory/F231_cold_visiting_room_empty.mp4", "act":4, "covers_scene_id":null, "subtype":"cold_visiting_room_empty" }
{ "public_path":"centralpark/factory/F232_gray_corridor_receding.mp4", "act":4, "covers_scene_id":null, "subtype":"gray_corridor_receding" }
{ "public_path":"centralpark/factory/F233_prison_wall_exterior_dusk_02.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_wall_exterior_dusk_02" }
{ "public_path":"centralpark/factory/F234_institutional_window_light_abstract_02.mp4", "act":4, "covers_scene_id":null, "subtype":"institutional_window_light_abstract_02" }
{ "public_path":"centralpark/factory/F235_long_prison_corridor_cold_02.mp4", "act":4, "covers_scene_id":null, "subtype":"long_prison_corridor_cold_02" }
{ "public_path":"centralpark/factory/F236_chainlink_fence_cold_abstract_02.mp4", "act":4, "covers_scene_id":null, "subtype":"chainlink_fence_cold_abstract_02" }
{ "public_path":"centralpark/factory/F237_razor_wire_sky_abstract_distant_02.mp4", "act":4, "covers_scene_id":null, "subtype":"razor_wire_sky_abstract_distant_02" }
{ "public_path":"centralpark/factory/F238_upstate_facility_exterior_winter_02.mp4", "act":4, "covers_scene_id":null, "subtype":"upstate_facility_exterior_winter_02" }
{ "public_path":"centralpark/factory/F239_cell_window_light_abstract_02.mp4", "act":4, "covers_scene_id":null, "subtype":"cell_window_light_abstract_02" }
{ "public_path":"centralpark/factory/F240_concrete_yard_empty_cold_02.mp4", "act":4, "covers_scene_id":null, "subtype":"concrete_yard_empty_cold_02" }
{ "public_path":"centralpark/factory/F241_institutional_door_heavy_cold_02.mp4", "act":4, "covers_scene_id":null, "subtype":"institutional_door_heavy_cold_02" }
{ "public_path":"centralpark/factory/F242_seasons_sky_window_shift_02.mp4", "act":4, "covers_scene_id":null, "subtype":"seasons_sky_window_shift_02" }
{ "public_path":"centralpark/factory/F243_bare_bunk_room_abstract_noface_02.mp4", "act":4, "covers_scene_id":null, "subtype":"bare_bunk_room_abstract_noface_02" }
{ "public_path":"centralpark/factory/F244_prison_fence_snow_distant_02.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_fence_snow_distant_02" }
{ "public_path":"centralpark/factory/F245_watchtower_silhouette_distant_02.mp4", "act":4, "covers_scene_id":null, "subtype":"watchtower_silhouette_distant_02" }
{ "public_path":"centralpark/factory/F246_cold_visiting_room_empty_02.mp4", "act":4, "covers_scene_id":null, "subtype":"cold_visiting_room_empty_02" }
{ "public_path":"centralpark/factory/F247_gray_corridor_receding_02.mp4", "act":4, "covers_scene_id":null, "subtype":"gray_corridor_receding_02" }
{ "public_path":"centralpark/factory/F248_prison_wall_exterior_dusk_03.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_wall_exterior_dusk_03" }
{ "public_path":"centralpark/factory/F249_institutional_window_light_abstract_03.mp4", "act":4, "covers_scene_id":null, "subtype":"institutional_window_light_abstract_03" }
{ "public_path":"centralpark/factory/F250_long_prison_corridor_cold_03.mp4", "act":4, "covers_scene_id":null, "subtype":"long_prison_corridor_cold_03" }
{ "public_path":"centralpark/factory/F251_chainlink_fence_cold_abstract_03.mp4", "act":4, "covers_scene_id":null, "subtype":"chainlink_fence_cold_abstract_03" }
{ "public_path":"centralpark/factory/F252_razor_wire_sky_abstract_distant_03.mp4", "act":4, "covers_scene_id":null, "subtype":"razor_wire_sky_abstract_distant_03" }
{ "public_path":"centralpark/factory/F253_upstate_facility_exterior_winter_03.mp4", "act":4, "covers_scene_id":null, "subtype":"upstate_facility_exterior_winter_03" }
{ "public_path":"centralpark/factory/F254_cell_window_light_abstract_03.mp4", "act":4, "covers_scene_id":null, "subtype":"cell_window_light_abstract_03" }
{ "public_path":"centralpark/factory/F255_concrete_yard_empty_cold_03.mp4", "act":4, "covers_scene_id":null, "subtype":"concrete_yard_empty_cold_03" }
{ "public_path":"centralpark/factory/F256_institutional_door_heavy_cold_03.mp4", "act":4, "covers_scene_id":null, "subtype":"institutional_door_heavy_cold_03" }
{ "public_path":"centralpark/factory/F257_seasons_sky_window_shift_03.mp4", "act":4, "covers_scene_id":null, "subtype":"seasons_sky_window_shift_03" }
{ "public_path":"centralpark/factory/F258_bare_bunk_room_abstract_noface_03.mp4", "act":4, "covers_scene_id":null, "subtype":"bare_bunk_room_abstract_noface_03" }
{ "public_path":"centralpark/factory/F259_prison_fence_snow_distant_03.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_fence_snow_distant_03" }
{ "public_path":"centralpark/factory/F260_watchtower_silhouette_distant_03.mp4", "act":4, "covers_scene_id":null, "subtype":"watchtower_silhouette_distant_03" }
{ "public_path":"centralpark/factory/F261_cold_visiting_room_empty_03.mp4", "act":4, "covers_scene_id":null, "subtype":"cold_visiting_room_empty_03" }
{ "public_path":"centralpark/factory/F262_gray_corridor_receding_03.mp4", "act":4, "covers_scene_id":null, "subtype":"gray_corridor_receding_03" }
{ "public_path":"centralpark/factory/F263_prison_wall_exterior_dusk_04.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_wall_exterior_dusk_04" }
{ "public_path":"centralpark/factory/F264_institutional_window_light_abstract_04.mp4", "act":4, "covers_scene_id":null, "subtype":"institutional_window_light_abstract_04" }
{ "public_path":"centralpark/factory/F265_long_prison_corridor_cold_04.mp4", "act":4, "covers_scene_id":null, "subtype":"long_prison_corridor_cold_04" }
{ "public_path":"centralpark/factory/F266_chainlink_fence_cold_abstract_04.mp4", "act":4, "covers_scene_id":null, "subtype":"chainlink_fence_cold_abstract_04" }
{ "public_path":"centralpark/factory/F267_razor_wire_sky_abstract_distant_04.mp4", "act":4, "covers_scene_id":null, "subtype":"razor_wire_sky_abstract_distant_04" }
{ "public_path":"centralpark/factory/F268_upstate_facility_exterior_winter_04.mp4", "act":4, "covers_scene_id":null, "subtype":"upstate_facility_exterior_winter_04" }
{ "public_path":"centralpark/factory/F269_cell_window_light_abstract_04.mp4", "act":4, "covers_scene_id":null, "subtype":"cell_window_light_abstract_04" }
{ "public_path":"centralpark/factory/F270_concrete_yard_empty_cold_04.mp4", "act":4, "covers_scene_id":null, "subtype":"concrete_yard_empty_cold_04" }
{ "public_path":"centralpark/factory/F271_institutional_door_heavy_cold_04.mp4", "act":4, "covers_scene_id":null, "subtype":"institutional_door_heavy_cold_04" }
{ "public_path":"centralpark/factory/F272_seasons_sky_window_shift_04.mp4", "act":4, "covers_scene_id":null, "subtype":"seasons_sky_window_shift_04" }
{ "public_path":"centralpark/factory/F273_bare_bunk_room_abstract_noface_04.mp4", "act":4, "covers_scene_id":null, "subtype":"bare_bunk_room_abstract_noface_04" }
{ "public_path":"centralpark/factory/F274_prison_fence_snow_distant_04.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_fence_snow_distant_04" }
{ "public_path":"centralpark/factory/F275_watchtower_silhouette_distant_04.mp4", "act":4, "covers_scene_id":null, "subtype":"watchtower_silhouette_distant_04" }
{ "public_path":"centralpark/factory/F276_cold_visiting_room_empty_04.mp4", "act":4, "covers_scene_id":null, "subtype":"cold_visiting_room_empty_04" }
{ "public_path":"centralpark/factory/F277_gray_corridor_receding_04.mp4", "act":4, "covers_scene_id":null, "subtype":"gray_corridor_receding_04" }
{ "public_path":"centralpark/factory/F278_prison_wall_exterior_dusk_05.mp4", "act":4, "covers_scene_id":null, "subtype":"prison_wall_exterior_dusk_05" }
{ "public_path":"centralpark/factory/F279_institutional_window_light_abstract_05.mp4", "act":4, "covers_scene_id":null, "subtype":"institutional_window_light_abstract_05" }
{ "public_path":"centralpark/factory/F280_long_prison_corridor_cold_05.mp4", "act":4, "covers_scene_id":null, "subtype":"long_prison_corridor_cold_05" }
{ "public_path":"centralpark/factory/F281_chainlink_fence_cold_abstract_05.mp4", "act":4, "covers_scene_id":null, "subtype":"chainlink_fence_cold_abstract_05" }
{ "public_path":"centralpark/factory/F282_razor_wire_sky_abstract_distant_05.mp4", "act":4, "covers_scene_id":null, "subtype":"razor_wire_sky_abstract_distant_05" }
{ "public_path":"centralpark/factory/F283_upstate_facility_exterior_winter_05.mp4", "act":4, "covers_scene_id":null, "subtype":"upstate_facility_exterior_winter_05" }
{ "public_path":"centralpark/factory/F284_cell_window_light_abstract_05.mp4", "act":4, "covers_scene_id":null, "subtype":"cell_window_light_abstract_05" }
{ "public_path":"centralpark/factory/F285_concrete_yard_empty_cold_05.mp4", "act":4, "covers_scene_id":null, "subtype":"concrete_yard_empty_cold_05" }
{ "public_path":"centralpark/factory/F286_institutional_door_heavy_cold_05.mp4", "act":4, "covers_scene_id":null, "subtype":"institutional_door_heavy_cold_05" }
{ "public_path":"centralpark/factory/F287_seasons_sky_window_shift_05.mp4", "act":4, "covers_scene_id":null, "subtype":"seasons_sky_window_shift_05" }
// ACT5 (act 5) — 55
{ "public_path":"centralpark/factory/F288_forensic_lab_ambient_cold.mp4", "act":5, "covers_scene_id":"S332", "subtype":"forensic_lab_ambient_cold" }
{ "public_path":"centralpark/factory/F289_dna_lab_equipment_abstract.mp4", "act":5, "covers_scene_id":"S345", "subtype":"dna_lab_equipment_abstract" }
{ "public_path":"centralpark/factory/F290_cold_lab_corridor.mp4", "act":5, "covers_scene_id":"S358", "subtype":"cold_lab_corridor" }
{ "public_path":"centralpark/factory/F291_evidence_room_shelves_cold.mp4", "act":5, "covers_scene_id":"S371", "subtype":"evidence_room_shelves_cold" }
{ "public_path":"centralpark/factory/F292_server_records_glow_cold.mp4", "act":5, "covers_scene_id":null, "subtype":"server_records_glow_cold" }
{ "public_path":"centralpark/factory/F293_microscope_bench_cold_abstract.mp4", "act":5, "covers_scene_id":null, "subtype":"microscope_bench_cold_abstract" }
{ "public_path":"centralpark/factory/F294_prison_yard_two_figures_distant_noface.mp4", "act":5, "covers_scene_id":null, "subtype":"prison_yard_two_figures_distant_noface" }
{ "public_path":"centralpark/factory/F295_auburn_facility_exterior_winter.mp4", "act":5, "covers_scene_id":null, "subtype":"auburn_facility_exterior_winter" }
{ "public_path":"centralpark/factory/F296_records_wall_deep_cold.mp4", "act":5, "covers_scene_id":null, "subtype":"records_wall_deep_cold" }
{ "public_path":"centralpark/factory/F297_cold_lab_light_panel.mp4", "act":5, "covers_scene_id":null, "subtype":"cold_lab_light_panel" }
{ "public_path":"centralpark/factory/F298_test_tube_rack_abstract_cold.mp4", "act":5, "covers_scene_id":null, "subtype":"test_tube_rack_abstract_cold" }
{ "public_path":"centralpark/factory/F299_file_boxes_evidence_dim.mp4", "act":5, "covers_scene_id":null, "subtype":"file_boxes_evidence_dim" }
{ "public_path":"centralpark/factory/F300_forensic_lab_ambient_cold_02.mp4", "act":5, "covers_scene_id":null, "subtype":"forensic_lab_ambient_cold_02" }
{ "public_path":"centralpark/factory/F301_dna_lab_equipment_abstract_02.mp4", "act":5, "covers_scene_id":null, "subtype":"dna_lab_equipment_abstract_02" }
{ "public_path":"centralpark/factory/F302_cold_lab_corridor_02.mp4", "act":5, "covers_scene_id":null, "subtype":"cold_lab_corridor_02" }
{ "public_path":"centralpark/factory/F303_evidence_room_shelves_cold_02.mp4", "act":5, "covers_scene_id":null, "subtype":"evidence_room_shelves_cold_02" }
{ "public_path":"centralpark/factory/F304_server_records_glow_cold_02.mp4", "act":5, "covers_scene_id":null, "subtype":"server_records_glow_cold_02" }
{ "public_path":"centralpark/factory/F305_microscope_bench_cold_abstract_02.mp4", "act":5, "covers_scene_id":null, "subtype":"microscope_bench_cold_abstract_02" }
{ "public_path":"centralpark/factory/F306_prison_yard_two_figures_distant_noface_02.mp4", "act":5, "covers_scene_id":null, "subtype":"prison_yard_two_figures_distant_noface_02" }
{ "public_path":"centralpark/factory/F307_auburn_facility_exterior_winter_02.mp4", "act":5, "covers_scene_id":null, "subtype":"auburn_facility_exterior_winter_02" }
{ "public_path":"centralpark/factory/F308_records_wall_deep_cold_02.mp4", "act":5, "covers_scene_id":null, "subtype":"records_wall_deep_cold_02" }
{ "public_path":"centralpark/factory/F309_cold_lab_light_panel_02.mp4", "act":5, "covers_scene_id":null, "subtype":"cold_lab_light_panel_02" }
{ "public_path":"centralpark/factory/F310_test_tube_rack_abstract_cold_02.mp4", "act":5, "covers_scene_id":null, "subtype":"test_tube_rack_abstract_cold_02" }
{ "public_path":"centralpark/factory/F311_file_boxes_evidence_dim_02.mp4", "act":5, "covers_scene_id":null, "subtype":"file_boxes_evidence_dim_02" }
{ "public_path":"centralpark/factory/F312_forensic_lab_ambient_cold_03.mp4", "act":5, "covers_scene_id":null, "subtype":"forensic_lab_ambient_cold_03" }
{ "public_path":"centralpark/factory/F313_dna_lab_equipment_abstract_03.mp4", "act":5, "covers_scene_id":null, "subtype":"dna_lab_equipment_abstract_03" }
{ "public_path":"centralpark/factory/F314_cold_lab_corridor_03.mp4", "act":5, "covers_scene_id":null, "subtype":"cold_lab_corridor_03" }
{ "public_path":"centralpark/factory/F315_evidence_room_shelves_cold_03.mp4", "act":5, "covers_scene_id":null, "subtype":"evidence_room_shelves_cold_03" }
{ "public_path":"centralpark/factory/F316_server_records_glow_cold_03.mp4", "act":5, "covers_scene_id":null, "subtype":"server_records_glow_cold_03" }
{ "public_path":"centralpark/factory/F317_microscope_bench_cold_abstract_03.mp4", "act":5, "covers_scene_id":null, "subtype":"microscope_bench_cold_abstract_03" }
{ "public_path":"centralpark/factory/F318_prison_yard_two_figures_distant_noface_03.mp4", "act":5, "covers_scene_id":null, "subtype":"prison_yard_two_figures_distant_noface_03" }
{ "public_path":"centralpark/factory/F319_auburn_facility_exterior_winter_03.mp4", "act":5, "covers_scene_id":null, "subtype":"auburn_facility_exterior_winter_03" }
{ "public_path":"centralpark/factory/F320_records_wall_deep_cold_03.mp4", "act":5, "covers_scene_id":null, "subtype":"records_wall_deep_cold_03" }
{ "public_path":"centralpark/factory/F321_cold_lab_light_panel_03.mp4", "act":5, "covers_scene_id":null, "subtype":"cold_lab_light_panel_03" }
{ "public_path":"centralpark/factory/F322_test_tube_rack_abstract_cold_03.mp4", "act":5, "covers_scene_id":null, "subtype":"test_tube_rack_abstract_cold_03" }
{ "public_path":"centralpark/factory/F323_file_boxes_evidence_dim_03.mp4", "act":5, "covers_scene_id":null, "subtype":"file_boxes_evidence_dim_03" }
{ "public_path":"centralpark/factory/F324_forensic_lab_ambient_cold_04.mp4", "act":5, "covers_scene_id":null, "subtype":"forensic_lab_ambient_cold_04" }
{ "public_path":"centralpark/factory/F325_dna_lab_equipment_abstract_04.mp4", "act":5, "covers_scene_id":null, "subtype":"dna_lab_equipment_abstract_04" }
{ "public_path":"centralpark/factory/F326_cold_lab_corridor_04.mp4", "act":5, "covers_scene_id":null, "subtype":"cold_lab_corridor_04" }
{ "public_path":"centralpark/factory/F327_evidence_room_shelves_cold_04.mp4", "act":5, "covers_scene_id":null, "subtype":"evidence_room_shelves_cold_04" }
{ "public_path":"centralpark/factory/F328_server_records_glow_cold_04.mp4", "act":5, "covers_scene_id":null, "subtype":"server_records_glow_cold_04" }
{ "public_path":"centralpark/factory/F329_microscope_bench_cold_abstract_04.mp4", "act":5, "covers_scene_id":null, "subtype":"microscope_bench_cold_abstract_04" }
{ "public_path":"centralpark/factory/F330_prison_yard_two_figures_distant_noface_04.mp4", "act":5, "covers_scene_id":null, "subtype":"prison_yard_two_figures_distant_noface_04" }
{ "public_path":"centralpark/factory/F331_auburn_facility_exterior_winter_04.mp4", "act":5, "covers_scene_id":null, "subtype":"auburn_facility_exterior_winter_04" }
{ "public_path":"centralpark/factory/F332_records_wall_deep_cold_04.mp4", "act":5, "covers_scene_id":null, "subtype":"records_wall_deep_cold_04" }
{ "public_path":"centralpark/factory/F333_cold_lab_light_panel_04.mp4", "act":5, "covers_scene_id":null, "subtype":"cold_lab_light_panel_04" }
{ "public_path":"centralpark/factory/F334_test_tube_rack_abstract_cold_04.mp4", "act":5, "covers_scene_id":null, "subtype":"test_tube_rack_abstract_cold_04" }
{ "public_path":"centralpark/factory/F335_file_boxes_evidence_dim_04.mp4", "act":5, "covers_scene_id":null, "subtype":"file_boxes_evidence_dim_04" }
{ "public_path":"centralpark/factory/F336_forensic_lab_ambient_cold_05.mp4", "act":5, "covers_scene_id":null, "subtype":"forensic_lab_ambient_cold_05" }
{ "public_path":"centralpark/factory/F337_dna_lab_equipment_abstract_05.mp4", "act":5, "covers_scene_id":null, "subtype":"dna_lab_equipment_abstract_05" }
{ "public_path":"centralpark/factory/F338_cold_lab_corridor_05.mp4", "act":5, "covers_scene_id":null, "subtype":"cold_lab_corridor_05" }
{ "public_path":"centralpark/factory/F339_evidence_room_shelves_cold_05.mp4", "act":5, "covers_scene_id":null, "subtype":"evidence_room_shelves_cold_05" }
{ "public_path":"centralpark/factory/F340_server_records_glow_cold_05.mp4", "act":5, "covers_scene_id":null, "subtype":"server_records_glow_cold_05" }
{ "public_path":"centralpark/factory/F341_microscope_bench_cold_abstract_05.mp4", "act":5, "covers_scene_id":null, "subtype":"microscope_bench_cold_abstract_05" }
{ "public_path":"centralpark/factory/F342_prison_yard_two_figures_distant_noface_05.mp4", "act":5, "covers_scene_id":null, "subtype":"prison_yard_two_figures_distant_noface_05" }
// ACT6 (act 6) — 50
{ "public_path":"centralpark/factory/F343_courthouse_steps_day.mp4", "act":6, "covers_scene_id":"S372", "subtype":"courthouse_steps_day" }
{ "public_path":"centralpark/factory/F344_city_dawn_skyline.mp4", "act":6, "covers_scene_id":"S385", "subtype":"city_dawn_skyline" }
{ "public_path":"centralpark/factory/F345_government_building_facade_day.mp4", "act":6, "covers_scene_id":"S400", "subtype":"government_building_facade_day" }
{ "public_path":"centralpark/factory/F346_dawn_horizon_amber_soft.mp4", "act":6, "covers_scene_id":"S408", "subtype":"dawn_horizon_amber_soft" }
{ "public_path":"centralpark/factory/F347_press_conference_ambient_noface.mp4", "act":6, "covers_scene_id":null, "subtype":"press_conference_ambient_noface" }
{ "public_path":"centralpark/factory/F348_city_street_morning_light.mp4", "act":6, "covers_scene_id":null, "subtype":"city_street_morning_light" }
{ "public_path":"centralpark/factory/F349_courthouse_exterior_morning.mp4", "act":6, "covers_scene_id":null, "subtype":"courthouse_exterior_morning" }
{ "public_path":"centralpark/factory/F350_council_chamber_empty.mp4", "act":6, "covers_scene_id":null, "subtype":"council_chamber_empty" }
{ "public_path":"centralpark/factory/F351_office_of_record_cold.mp4", "act":6, "covers_scene_id":null, "subtype":"office_of_record_cold" }
{ "public_path":"centralpark/factory/F352_settlement_documents_desk_abstract.mp4", "act":6, "covers_scene_id":null, "subtype":"settlement_documents_desk_abstract" }
{ "public_path":"centralpark/factory/F353_city_hall_facade_day.mp4", "act":6, "covers_scene_id":null, "subtype":"city_hall_facade_day" }
{ "public_path":"centralpark/factory/F354_sunrise_over_park_abstract.mp4", "act":6, "covers_scene_id":null, "subtype":"sunrise_over_park_abstract" }
{ "public_path":"centralpark/factory/F355_courthouse_steps_day_02.mp4", "act":6, "covers_scene_id":null, "subtype":"courthouse_steps_day_02" }
{ "public_path":"centralpark/factory/F356_city_dawn_skyline_02.mp4", "act":6, "covers_scene_id":null, "subtype":"city_dawn_skyline_02" }
{ "public_path":"centralpark/factory/F357_government_building_facade_day_02.mp4", "act":6, "covers_scene_id":null, "subtype":"government_building_facade_day_02" }
{ "public_path":"centralpark/factory/F358_dawn_horizon_amber_soft_02.mp4", "act":6, "covers_scene_id":null, "subtype":"dawn_horizon_amber_soft_02" }
{ "public_path":"centralpark/factory/F359_press_conference_ambient_noface_02.mp4", "act":6, "covers_scene_id":null, "subtype":"press_conference_ambient_noface_02" }
{ "public_path":"centralpark/factory/F360_city_street_morning_light_02.mp4", "act":6, "covers_scene_id":null, "subtype":"city_street_morning_light_02" }
{ "public_path":"centralpark/factory/F361_courthouse_exterior_morning_02.mp4", "act":6, "covers_scene_id":null, "subtype":"courthouse_exterior_morning_02" }
{ "public_path":"centralpark/factory/F362_council_chamber_empty_02.mp4", "act":6, "covers_scene_id":null, "subtype":"council_chamber_empty_02" }
{ "public_path":"centralpark/factory/F363_office_of_record_cold_02.mp4", "act":6, "covers_scene_id":null, "subtype":"office_of_record_cold_02" }
{ "public_path":"centralpark/factory/F364_settlement_documents_desk_abstract_02.mp4", "act":6, "covers_scene_id":null, "subtype":"settlement_documents_desk_abstract_02" }
{ "public_path":"centralpark/factory/F365_city_hall_facade_day_02.mp4", "act":6, "covers_scene_id":null, "subtype":"city_hall_facade_day_02" }
{ "public_path":"centralpark/factory/F366_sunrise_over_park_abstract_02.mp4", "act":6, "covers_scene_id":null, "subtype":"sunrise_over_park_abstract_02" }
{ "public_path":"centralpark/factory/F367_courthouse_steps_day_03.mp4", "act":6, "covers_scene_id":null, "subtype":"courthouse_steps_day_03" }
{ "public_path":"centralpark/factory/F368_city_dawn_skyline_03.mp4", "act":6, "covers_scene_id":null, "subtype":"city_dawn_skyline_03" }
{ "public_path":"centralpark/factory/F369_government_building_facade_day_03.mp4", "act":6, "covers_scene_id":null, "subtype":"government_building_facade_day_03" }
{ "public_path":"centralpark/factory/F370_dawn_horizon_amber_soft_03.mp4", "act":6, "covers_scene_id":null, "subtype":"dawn_horizon_amber_soft_03" }
{ "public_path":"centralpark/factory/F371_press_conference_ambient_noface_03.mp4", "act":6, "covers_scene_id":null, "subtype":"press_conference_ambient_noface_03" }
{ "public_path":"centralpark/factory/F372_city_street_morning_light_03.mp4", "act":6, "covers_scene_id":null, "subtype":"city_street_morning_light_03" }
{ "public_path":"centralpark/factory/F373_courthouse_exterior_morning_03.mp4", "act":6, "covers_scene_id":null, "subtype":"courthouse_exterior_morning_03" }
{ "public_path":"centralpark/factory/F374_council_chamber_empty_03.mp4", "act":6, "covers_scene_id":null, "subtype":"council_chamber_empty_03" }
{ "public_path":"centralpark/factory/F375_office_of_record_cold_03.mp4", "act":6, "covers_scene_id":null, "subtype":"office_of_record_cold_03" }
{ "public_path":"centralpark/factory/F376_settlement_documents_desk_abstract_03.mp4", "act":6, "covers_scene_id":null, "subtype":"settlement_documents_desk_abstract_03" }
{ "public_path":"centralpark/factory/F377_city_hall_facade_day_03.mp4", "act":6, "covers_scene_id":null, "subtype":"city_hall_facade_day_03" }
{ "public_path":"centralpark/factory/F378_sunrise_over_park_abstract_03.mp4", "act":6, "covers_scene_id":null, "subtype":"sunrise_over_park_abstract_03" }
{ "public_path":"centralpark/factory/F379_courthouse_steps_day_04.mp4", "act":6, "covers_scene_id":null, "subtype":"courthouse_steps_day_04" }
{ "public_path":"centralpark/factory/F380_city_dawn_skyline_04.mp4", "act":6, "covers_scene_id":null, "subtype":"city_dawn_skyline_04" }
{ "public_path":"centralpark/factory/F381_government_building_facade_day_04.mp4", "act":6, "covers_scene_id":null, "subtype":"government_building_facade_day_04" }
{ "public_path":"centralpark/factory/F382_dawn_horizon_amber_soft_04.mp4", "act":6, "covers_scene_id":null, "subtype":"dawn_horizon_amber_soft_04" }
{ "public_path":"centralpark/factory/F383_press_conference_ambient_noface_04.mp4", "act":6, "covers_scene_id":null, "subtype":"press_conference_ambient_noface_04" }
{ "public_path":"centralpark/factory/F384_city_street_morning_light_04.mp4", "act":6, "covers_scene_id":null, "subtype":"city_street_morning_light_04" }
{ "public_path":"centralpark/factory/F385_courthouse_exterior_morning_04.mp4", "act":6, "covers_scene_id":null, "subtype":"courthouse_exterior_morning_04" }
{ "public_path":"centralpark/factory/F386_council_chamber_empty_04.mp4", "act":6, "covers_scene_id":null, "subtype":"council_chamber_empty_04" }
{ "public_path":"centralpark/factory/F387_office_of_record_cold_04.mp4", "act":6, "covers_scene_id":null, "subtype":"office_of_record_cold_04" }
{ "public_path":"centralpark/factory/F388_settlement_documents_desk_abstract_04.mp4", "act":6, "covers_scene_id":null, "subtype":"settlement_documents_desk_abstract_04" }
{ "public_path":"centralpark/factory/F389_city_hall_facade_day_04.mp4", "act":6, "covers_scene_id":null, "subtype":"city_hall_facade_day_04" }
{ "public_path":"centralpark/factory/F390_sunrise_over_park_abstract_04.mp4", "act":6, "covers_scene_id":null, "subtype":"sunrise_over_park_abstract_04" }
{ "public_path":"centralpark/factory/F391_courthouse_steps_day_05.mp4", "act":6, "covers_scene_id":null, "subtype":"courthouse_steps_day_05" }
{ "public_path":"centralpark/factory/F392_city_dawn_skyline_05.mp4", "act":6, "covers_scene_id":null, "subtype":"city_dawn_skyline_05" }
// ACT7 (act 7) — 20
{ "public_path":"centralpark/factory/F393_interrogation_room_minimal_cold.mp4", "act":7, "covers_scene_id":"S416", "subtype":"interrogation_room_minimal_cold" }
{ "public_path":"centralpark/factory/F394_empty_chair_single_light.mp4", "act":7, "covers_scene_id":"S423", "subtype":"empty_chair_single_light" }
{ "public_path":"centralpark/factory/F395_wall_clock_cold_close.mp4", "act":7, "covers_scene_id":"S430", "subtype":"wall_clock_cold_close" }
{ "public_path":"centralpark/factory/F396_rec_light_dot_dark_abstract.mp4", "act":7, "covers_scene_id":null, "subtype":"rec_light_dot_dark_abstract" }
{ "public_path":"centralpark/factory/F397_bare_room_dawn_edge.mp4", "act":7, "covers_scene_id":null, "subtype":"bare_room_dawn_edge" }
{ "public_path":"centralpark/factory/F398_cold_room_final_still.mp4", "act":7, "covers_scene_id":null, "subtype":"cold_room_final_still" }
{ "public_path":"centralpark/factory/F399_single_lamp_dark_room.mp4", "act":7, "covers_scene_id":null, "subtype":"single_lamp_dark_room" }
{ "public_path":"centralpark/factory/F400_empty_table_shadow.mp4", "act":7, "covers_scene_id":null, "subtype":"empty_table_shadow" }
{ "public_path":"centralpark/factory/F401_interrogation_room_minimal_cold_02.mp4", "act":7, "covers_scene_id":null, "subtype":"interrogation_room_minimal_cold_02" }
{ "public_path":"centralpark/factory/F402_empty_chair_single_light_02.mp4", "act":7, "covers_scene_id":null, "subtype":"empty_chair_single_light_02" }
{ "public_path":"centralpark/factory/F403_wall_clock_cold_close_02.mp4", "act":7, "covers_scene_id":null, "subtype":"wall_clock_cold_close_02" }
{ "public_path":"centralpark/factory/F404_rec_light_dot_dark_abstract_02.mp4", "act":7, "covers_scene_id":null, "subtype":"rec_light_dot_dark_abstract_02" }
{ "public_path":"centralpark/factory/F405_bare_room_dawn_edge_02.mp4", "act":7, "covers_scene_id":null, "subtype":"bare_room_dawn_edge_02" }
{ "public_path":"centralpark/factory/F406_cold_room_final_still_02.mp4", "act":7, "covers_scene_id":null, "subtype":"cold_room_final_still_02" }
{ "public_path":"centralpark/factory/F407_single_lamp_dark_room_02.mp4", "act":7, "covers_scene_id":null, "subtype":"single_lamp_dark_room_02" }
{ "public_path":"centralpark/factory/F408_empty_table_shadow_02.mp4", "act":7, "covers_scene_id":null, "subtype":"empty_table_shadow_02" }
{ "public_path":"centralpark/factory/F409_interrogation_room_minimal_cold_03.mp4", "act":7, "covers_scene_id":null, "subtype":"interrogation_room_minimal_cold_03" }
{ "public_path":"centralpark/factory/F410_empty_chair_single_light_03.mp4", "act":7, "covers_scene_id":null, "subtype":"empty_chair_single_light_03" }
{ "public_path":"centralpark/factory/F411_wall_clock_cold_close_03.mp4", "act":7, "covers_scene_id":null, "subtype":"wall_clock_cold_close_03" }
{ "public_path":"centralpark/factory/F412_rec_light_dot_dark_abstract_03.mp4", "act":7, "covers_scene_id":null, "subtype":"rec_light_dot_dark_abstract_03" }
// connective (covers null) — 73
{ "public_path":"centralpark/factory/F413_abstract_loop_cold_drift.mp4", "act":9, "covers_scene_id":null, "subtype":"abstract_loop_cold_drift" }
{ "public_path":"centralpark/factory/F414_dust_in_cold_light.mp4", "act":9, "covers_scene_id":null, "subtype":"dust_in_cold_light" }
{ "public_path":"centralpark/factory/F415_light_shaft_dark_slow.mp4", "act":9, "covers_scene_id":null, "subtype":"light_shaft_dark_slow" }
{ "public_path":"centralpark/factory/F416_cityscape_night_bokeh.mp4", "act":9, "covers_scene_id":null, "subtype":"cityscape_night_bokeh" }
{ "public_path":"centralpark/factory/F417_sky_gradient_cold_night.mp4", "act":9, "covers_scene_id":null, "subtype":"sky_gradient_cold_night" }
{ "public_path":"centralpark/factory/F418_marble_texture_pan_cold.mp4", "act":9, "covers_scene_id":null, "subtype":"marble_texture_pan_cold" }
{ "public_path":"centralpark/factory/F419_water_reflection_night_cold.mp4", "act":9, "covers_scene_id":null, "subtype":"water_reflection_night_cold" }
{ "public_path":"centralpark/factory/F420_asphalt_wet_reflection_cold.mp4", "act":9, "covers_scene_id":null, "subtype":"asphalt_wet_reflection_cold" }
{ "public_path":"centralpark/factory/F421_paper_texture_dim.mp4", "act":9, "covers_scene_id":null, "subtype":"paper_texture_dim" }
{ "public_path":"centralpark/factory/F422_concrete_texture_pan.mp4", "act":9, "covers_scene_id":null, "subtype":"concrete_texture_pan" }
{ "public_path":"centralpark/factory/F423_fluorescent_ceiling_pan_cold.mp4", "act":9, "covers_scene_id":null, "subtype":"fluorescent_ceiling_pan_cold" }
{ "public_path":"centralpark/factory/F424_window_rain_night_cold.mp4", "act":9, "covers_scene_id":null, "subtype":"window_rain_night_cold" }
{ "public_path":"centralpark/factory/F425_cold_smoke_drift_black.mp4", "act":9, "covers_scene_id":null, "subtype":"cold_smoke_drift_black" }
{ "public_path":"centralpark/factory/F426_abstract_grid_lines_cold.mp4", "act":9, "covers_scene_id":null, "subtype":"abstract_grid_lines_cold" }
{ "public_path":"centralpark/factory/F427_dark_field_wind_night.mp4", "act":9, "covers_scene_id":null, "subtype":"dark_field_wind_night" }
{ "public_path":"centralpark/factory/F428_horizon_line_cold_dusk.mp4", "act":9, "covers_scene_id":null, "subtype":"horizon_line_cold_dusk" }
{ "public_path":"centralpark/factory/F429_cold_water_ripple.mp4", "act":9, "covers_scene_id":null, "subtype":"cold_water_ripple" }
{ "public_path":"centralpark/factory/F430_institutional_wall_shadow_pan.mp4", "act":9, "covers_scene_id":null, "subtype":"institutional_wall_shadow_pan" }
{ "public_path":"centralpark/factory/F431_abstract_loop_cold_drift_02.mp4", "act":9, "covers_scene_id":null, "subtype":"abstract_loop_cold_drift_02" }
{ "public_path":"centralpark/factory/F432_dust_in_cold_light_02.mp4", "act":9, "covers_scene_id":null, "subtype":"dust_in_cold_light_02" }
{ "public_path":"centralpark/factory/F433_light_shaft_dark_slow_02.mp4", "act":9, "covers_scene_id":null, "subtype":"light_shaft_dark_slow_02" }
{ "public_path":"centralpark/factory/F434_cityscape_night_bokeh_02.mp4", "act":9, "covers_scene_id":null, "subtype":"cityscape_night_bokeh_02" }
{ "public_path":"centralpark/factory/F435_sky_gradient_cold_night_02.mp4", "act":9, "covers_scene_id":null, "subtype":"sky_gradient_cold_night_02" }
{ "public_path":"centralpark/factory/F436_marble_texture_pan_cold_02.mp4", "act":9, "covers_scene_id":null, "subtype":"marble_texture_pan_cold_02" }
{ "public_path":"centralpark/factory/F437_water_reflection_night_cold_02.mp4", "act":9, "covers_scene_id":null, "subtype":"water_reflection_night_cold_02" }
{ "public_path":"centralpark/factory/F438_asphalt_wet_reflection_cold_02.mp4", "act":9, "covers_scene_id":null, "subtype":"asphalt_wet_reflection_cold_02" }
{ "public_path":"centralpark/factory/F439_paper_texture_dim_02.mp4", "act":9, "covers_scene_id":null, "subtype":"paper_texture_dim_02" }
{ "public_path":"centralpark/factory/F440_concrete_texture_pan_02.mp4", "act":9, "covers_scene_id":null, "subtype":"concrete_texture_pan_02" }
{ "public_path":"centralpark/factory/F441_fluorescent_ceiling_pan_cold_02.mp4", "act":9, "covers_scene_id":null, "subtype":"fluorescent_ceiling_pan_cold_02" }
{ "public_path":"centralpark/factory/F442_window_rain_night_cold_02.mp4", "act":9, "covers_scene_id":null, "subtype":"window_rain_night_cold_02" }
{ "public_path":"centralpark/factory/F443_cold_smoke_drift_black_02.mp4", "act":9, "covers_scene_id":null, "subtype":"cold_smoke_drift_black_02" }
{ "public_path":"centralpark/factory/F444_abstract_grid_lines_cold_02.mp4", "act":9, "covers_scene_id":null, "subtype":"abstract_grid_lines_cold_02" }
{ "public_path":"centralpark/factory/F445_dark_field_wind_night_02.mp4", "act":9, "covers_scene_id":null, "subtype":"dark_field_wind_night_02" }
{ "public_path":"centralpark/factory/F446_horizon_line_cold_dusk_02.mp4", "act":9, "covers_scene_id":null, "subtype":"horizon_line_cold_dusk_02" }
{ "public_path":"centralpark/factory/F447_cold_water_ripple_02.mp4", "act":9, "covers_scene_id":null, "subtype":"cold_water_ripple_02" }
{ "public_path":"centralpark/factory/F448_institutional_wall_shadow_pan_02.mp4", "act":9, "covers_scene_id":null, "subtype":"institutional_wall_shadow_pan_02" }
{ "public_path":"centralpark/factory/F449_abstract_loop_cold_drift_03.mp4", "act":9, "covers_scene_id":null, "subtype":"abstract_loop_cold_drift_03" }
{ "public_path":"centralpark/factory/F450_dust_in_cold_light_03.mp4", "act":9, "covers_scene_id":null, "subtype":"dust_in_cold_light_03" }
{ "public_path":"centralpark/factory/F451_light_shaft_dark_slow_03.mp4", "act":9, "covers_scene_id":null, "subtype":"light_shaft_dark_slow_03" }
{ "public_path":"centralpark/factory/F452_cityscape_night_bokeh_03.mp4", "act":9, "covers_scene_id":null, "subtype":"cityscape_night_bokeh_03" }
{ "public_path":"centralpark/factory/F453_sky_gradient_cold_night_03.mp4", "act":9, "covers_scene_id":null, "subtype":"sky_gradient_cold_night_03" }
{ "public_path":"centralpark/factory/F454_marble_texture_pan_cold_03.mp4", "act":9, "covers_scene_id":null, "subtype":"marble_texture_pan_cold_03" }
{ "public_path":"centralpark/factory/F455_water_reflection_night_cold_03.mp4", "act":9, "covers_scene_id":null, "subtype":"water_reflection_night_cold_03" }
{ "public_path":"centralpark/factory/F456_asphalt_wet_reflection_cold_03.mp4", "act":9, "covers_scene_id":null, "subtype":"asphalt_wet_reflection_cold_03" }
{ "public_path":"centralpark/factory/F457_paper_texture_dim_03.mp4", "act":9, "covers_scene_id":null, "subtype":"paper_texture_dim_03" }
{ "public_path":"centralpark/factory/F458_concrete_texture_pan_03.mp4", "act":9, "covers_scene_id":null, "subtype":"concrete_texture_pan_03" }
{ "public_path":"centralpark/factory/F459_fluorescent_ceiling_pan_cold_03.mp4", "act":9, "covers_scene_id":null, "subtype":"fluorescent_ceiling_pan_cold_03" }
{ "public_path":"centralpark/factory/F460_window_rain_night_cold_03.mp4", "act":9, "covers_scene_id":null, "subtype":"window_rain_night_cold_03" }
{ "public_path":"centralpark/factory/F461_cold_smoke_drift_black_03.mp4", "act":9, "covers_scene_id":null, "subtype":"cold_smoke_drift_black_03" }
{ "public_path":"centralpark/factory/F462_abstract_grid_lines_cold_03.mp4", "act":9, "covers_scene_id":null, "subtype":"abstract_grid_lines_cold_03" }
{ "public_path":"centralpark/factory/F463_dark_field_wind_night_03.mp4", "act":9, "covers_scene_id":null, "subtype":"dark_field_wind_night_03" }
{ "public_path":"centralpark/factory/F464_horizon_line_cold_dusk_03.mp4", "act":9, "covers_scene_id":null, "subtype":"horizon_line_cold_dusk_03" }
{ "public_path":"centralpark/factory/F465_cold_water_ripple_03.mp4", "act":9, "covers_scene_id":null, "subtype":"cold_water_ripple_03" }
{ "public_path":"centralpark/factory/F466_institutional_wall_shadow_pan_03.mp4", "act":9, "covers_scene_id":null, "subtype":"institutional_wall_shadow_pan_03" }
{ "public_path":"centralpark/factory/F467_abstract_loop_cold_drift_04.mp4", "act":9, "covers_scene_id":null, "subtype":"abstract_loop_cold_drift_04" }
{ "public_path":"centralpark/factory/F468_dust_in_cold_light_04.mp4", "act":9, "covers_scene_id":null, "subtype":"dust_in_cold_light_04" }
{ "public_path":"centralpark/factory/F469_light_shaft_dark_slow_04.mp4", "act":9, "covers_scene_id":null, "subtype":"light_shaft_dark_slow_04" }
{ "public_path":"centralpark/factory/F470_cityscape_night_bokeh_04.mp4", "act":9, "covers_scene_id":null, "subtype":"cityscape_night_bokeh_04" }
{ "public_path":"centralpark/factory/F471_sky_gradient_cold_night_04.mp4", "act":9, "covers_scene_id":null, "subtype":"sky_gradient_cold_night_04" }
{ "public_path":"centralpark/factory/F472_marble_texture_pan_cold_04.mp4", "act":9, "covers_scene_id":null, "subtype":"marble_texture_pan_cold_04" }
{ "public_path":"centralpark/factory/F473_water_reflection_night_cold_04.mp4", "act":9, "covers_scene_id":null, "subtype":"water_reflection_night_cold_04" }
{ "public_path":"centralpark/factory/F474_asphalt_wet_reflection_cold_04.mp4", "act":9, "covers_scene_id":null, "subtype":"asphalt_wet_reflection_cold_04" }
{ "public_path":"centralpark/factory/F475_paper_texture_dim_04.mp4", "act":9, "covers_scene_id":null, "subtype":"paper_texture_dim_04" }
{ "public_path":"centralpark/factory/F476_concrete_texture_pan_04.mp4", "act":9, "covers_scene_id":null, "subtype":"concrete_texture_pan_04" }
{ "public_path":"centralpark/factory/F477_fluorescent_ceiling_pan_cold_04.mp4", "act":9, "covers_scene_id":null, "subtype":"fluorescent_ceiling_pan_cold_04" }
{ "public_path":"centralpark/factory/F478_window_rain_night_cold_04.mp4", "act":9, "covers_scene_id":null, "subtype":"window_rain_night_cold_04" }
{ "public_path":"centralpark/factory/F479_cold_smoke_drift_black_04.mp4", "act":9, "covers_scene_id":null, "subtype":"cold_smoke_drift_black_04" }
{ "public_path":"centralpark/factory/F480_abstract_grid_lines_cold_04.mp4", "act":9, "covers_scene_id":null, "subtype":"abstract_grid_lines_cold_04" }
{ "public_path":"centralpark/factory/F481_dark_field_wind_night_04.mp4", "act":9, "covers_scene_id":null, "subtype":"dark_field_wind_night_04" }
{ "public_path":"centralpark/factory/F482_horizon_line_cold_dusk_04.mp4", "act":9, "covers_scene_id":null, "subtype":"horizon_line_cold_dusk_04" }
{ "public_path":"centralpark/factory/F483_cold_water_ripple_04.mp4", "act":9, "covers_scene_id":null, "subtype":"cold_water_ripple_04" }
{ "public_path":"centralpark/factory/F484_institutional_wall_shadow_pan_04.mp4", "act":9, "covers_scene_id":null, "subtype":"institutional_wall_shadow_pan_04" }
{ "public_path":"centralpark/factory/F485_abstract_loop_cold_drift_05.mp4", "act":9, "covers_scene_id":null, "subtype":"abstract_loop_cold_drift_05" }
```

**内訳検算:** HOOK+OPENING 12 + ACT1 70 + ACT2 70 + ACT3 65 + ACT4 70 + ACT5 55 + ACT6 50 + ACT7 20 + 繋ぎ 73 = **485** ✓。全 `public_path` 非空 ✓（不変条件17）。

## 4.5 ★`motion[]` 全85エントリ（★必ず実体化・public_path 非空）

> エントリ形は §4.1a 準拠 + 動画フィールド。`asset_id ^CPK-M\d{2}$`。`source_still` は §8.1a の種画像、`source_scene_id`=`MS<NN>`。runtime で `sha256`/`width 1280`/`height 720`/`fps 48`/`frames`/`duration_sec`/`qc` を埋める（§8.4）。**空配列を書かない。** `storyboard` は §2 の Sid 参照（可読の便宜・スキーマ任意）。

```jsonc
{ "asset_id":"CPK-M01", "source_scene_id":"MS01", "source_still":"H:/pd-media/assets/ai/centralpark/M01_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M01_rife.mp4", "public_path":"centralpark/motion/M01_rife.mp4", "act":0, "storyboard":"A1-01", "tags":["empty_chair_cold_light_find"] }
{ "asset_id":"CPK-M02", "source_scene_id":"MS02", "source_still":"H:/pd-media/assets/ai/centralpark/M02_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M02_rife.mp4", "public_path":"centralpark/motion/M02_rife.mp4", "act":0, "storyboard":"A1-02", "tags":["off_rec_lamp_tick"] }
{ "asset_id":"CPK-M03", "source_scene_id":"MS03", "source_still":"H:/pd-media/assets/ai/centralpark/M03_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M03_rife.mp4", "public_path":"centralpark/motion/M03_rife.mp4", "act":0, "storyboard":"hook", "tags":["cold_cyan_edge_cross"] }
{ "asset_id":"CPK-M04", "source_scene_id":"MS04", "source_still":"H:/pd-media/assets/ai/centralpark/M04_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M04_rife.mp4", "public_path":"centralpark/motion/M04_rife.mp4", "act":1, "storyboard":"A1-03", "tags":["subway_graffiti_drift"] }
{ "asset_id":"CPK-M05", "source_scene_id":"MS05", "source_still":"H:/pd-media/assets/ai/centralpark/M05_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M05_rife.mp4", "public_path":"centralpark/motion/M05_rife.mp4", "act":1, "storyboard":"A1-04", "tags":["news_flicker_night"] }
{ "asset_id":"CPK-M06", "source_scene_id":"MS06", "source_still":"H:/pd-media/assets/ai/centralpark/M06_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M06_rife.mp4", "public_path":"centralpark/motion/M06_rife.mp4", "act":1, "storyboard":"A1-05", "tags":["park_treeline_wind_abstract"] }
{ "asset_id":"CPK-M07", "source_scene_id":"MS07", "source_still":"H:/pd-media/assets/ai/centralpark/M07_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M07_rife.mp4", "public_path":"centralpark/motion/M07_rife.mp4", "act":1, "storyboard":"A1-06", "tags":["teen_mass_backs_restless"] }
{ "asset_id":"CPK-M08", "source_scene_id":"MS08", "source_still":"H:/pd-media/assets/ai/centralpark/M08_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M08_rife.mp4", "public_path":"centralpark/motion/M08_rife.mp4", "act":1, "storyboard":"A1-07", "tags":["five_descending_silhouettes"] }
{ "asset_id":"CPK-M09", "source_scene_id":"MS09", "source_still":"H:/pd-media/assets/ai/centralpark/M09_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M09_rife.mp4", "public_path":"centralpark/motion/M09_rife.mp4", "act":1, "storyboard":"A1-10", "tags":["precinct_fills_backs"] }
{ "asset_id":"CPK-M10", "source_scene_id":"MS10", "source_still":"H:/pd-media/assets/ai/centralpark/M10_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M10_rife.mp4", "public_path":"centralpark/motion/M10_rife.mp4", "act":1, "storyboard":"A1-11", "tags":["two_files_collide_snap"] }
{ "asset_id":"CPK-M11", "source_scene_id":"MS11", "source_still":"H:/pd-media/assets/ai/centralpark/M11_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M11_rife.mp4", "public_path":"centralpark/motion/M11_rife.mp4", "act":1, "storyboard":"A1-13", "tags":["cursor_blink_no_evidence"] }
{ "asset_id":"CPK-M12", "source_scene_id":"MS12", "source_still":"H:/pd-media/assets/ai/centralpark/M12_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M12_rife.mp4", "public_path":"centralpark/motion/M12_rife.mp4", "act":1, "storyboard":"A1-14", "tags":["building_looms_upangle"] }
{ "asset_id":"CPK-M13", "source_scene_id":"MS13", "source_still":"H:/pd-media/assets/ai/centralpark/M13_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M13_rife.mp4", "public_path":"centralpark/motion/M13_rife.mp4", "act":1, "storyboard":"A1-15", "tags":["lab_band_cold_ignored"] }
{ "asset_id":"CPK-M14", "source_scene_id":"MS14", "source_still":"H:/pd-media/assets/ai/centralpark/M14_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M14_rife.mp4", "public_path":"centralpark/motion/M14_rife.mp4", "act":1, "storyboard":"A1-12", "tags":["empty_pointing_hand"] }
{ "asset_id":"CPK-M15", "source_scene_id":"MS15", "source_still":"H:/pd-media/assets/ai/centralpark/M15_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M15_rife.mp4", "public_path":"centralpark/motion/M15_rife.mp4", "act":1, "storyboard":"A1-09", "tags":["coma_vacuum_cold_sink"] }
{ "asset_id":"CPK-M16", "source_scene_id":"MS16", "source_still":"H:/pd-media/assets/ai/centralpark/M16_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M16_rife.mp4", "public_path":"centralpark/motion/M16_rife.mp4", "act":2, "storyboard":"A2-01", "tags":["room_general_clock_hold"] }
{ "asset_id":"CPK-M17", "source_scene_id":"MS17", "source_still":"H:/pd-media/assets/ai/centralpark/M17_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M17_rife.mp4", "public_path":"centralpark/motion/M17_rife.mp4", "act":2, "storyboard":"A2-02", "tags":["cold_soda_untouched"] }
{ "asset_id":"CPK-M18", "source_scene_id":"MS18", "source_still":"H:/pd-media/assets/ai/centralpark/M18_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M18_rife.mp4", "public_path":"centralpark/motion/M18_rife.mp4", "act":2, "storyboard":"A2-03", "tags":["detective_child_shadow_face"] }
{ "asset_id":"CPK-M19", "source_scene_id":"MS19", "source_still":"H:/pd-media/assets/ai/centralpark/M19_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M19_rife.mp4", "public_path":"centralpark/motion/M19_rife.mp4", "act":2, "storyboard":"A2-04", "tags":["story_type_migrates"] }
{ "asset_id":"CPK-M20", "source_scene_id":"MS20", "source_still":"H:/pd-media/assets/ai/centralpark/M20_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M20_rife.mp4", "public_path":"centralpark/motion/M20_rife.mp4", "act":2, "storyboard":"A2-06", "tags":["false_evidence_ploy_abstract"] }
{ "asset_id":"CPK-M21", "source_scene_id":"MS21", "source_still":"H:/pd-media/assets/ai/centralpark/M21_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M21_rife.mp4", "public_path":"centralpark/motion/M21_rife.mp4", "act":2, "storyboard":"A2-07", "tags":["minimization_door_closes"] }
{ "asset_id":"CPK-M22", "source_scene_id":"MS22", "source_still":"H:/pd-media/assets/ai/centralpark/M22_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M22_rife.mp4", "public_path":"centralpark/motion/M22_rife.mp4", "act":2, "storyboard":"A2-08", "tags":["pen_writes_signature_line"] }
{ "asset_id":"CPK-M23", "source_scene_id":"MS23", "source_still":"H:/pd-media/assets/ai/centralpark/M23_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M23_rife.mp4", "public_path":"centralpark/motion/M23_rife.mp4", "act":2, "storyboard":"A2-09", "tags":["confession_pages_stack"] }
{ "asset_id":"CPK-M24", "source_scene_id":"MS24", "source_still":"H:/pd-media/assets/ai/centralpark/M24_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M24_rife.mp4", "public_path":"centralpark/motion/M24_rife.mp4", "act":2, "storyboard":"A2-10", "tags":["rape_kit_excludes_five_band"] }
{ "asset_id":"CPK-M25", "source_scene_id":"MS25", "source_still":"H:/pd-media/assets/ai/centralpark/M25_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M25_rife.mp4", "public_path":"centralpark/motion/M25_rife.mp4", "act":2, "storyboard":"A2-11", "tags":["ghost_sixth_silhouette"] }
{ "asset_id":"CPK-M26", "source_scene_id":"MS26", "source_still":"H:/pd-media/assets/ai/centralpark/M26_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M26_rife.mp4", "public_path":"centralpark/motion/M26_rife.mp4", "act":2, "storyboard":"A2-12", "tags":["pressure_gears_turn"] }
{ "asset_id":"CPK-M27", "source_scene_id":"MS27", "source_still":"H:/pd-media/assets/ai/centralpark/M27_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M27_rife.mp4", "public_path":"centralpark/motion/M27_rife.mp4", "act":2, "storyboard":"A2-13", "tags":["tv_glow_after_hours"] }
{ "asset_id":"CPK-M28", "source_scene_id":"MS28", "source_still":"H:/pd-media/assets/ai/centralpark/M28_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M28_rife.mp4", "public_path":"centralpark/motion/M28_rife.mp4", "act":2, "storyboard":"A2-14", "tags":["signatures_down_ordinary_week"] }
{ "asset_id":"CPK-M29", "source_scene_id":"MS29", "source_still":"H:/pd-media/assets/ai/centralpark/M29_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M29_rife.mp4", "public_path":"centralpark/motion/M29_rife.mp4", "act":2, "storyboard":"A2-15", "tags":["machine_moves_next_room"] }
{ "asset_id":"CPK-M30", "source_scene_id":"MS30", "source_still":"H:/pd-media/assets/ai/centralpark/M30_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M30_rife.mp4", "public_path":"centralpark/motion/M30_rife.mp4", "act":2, "storyboard":"A2-01b", "tags":["clock_no_time_drift"] }
{ "asset_id":"CPK-M31", "source_scene_id":"MS31", "source_still":"H:/pd-media/assets/ai/centralpark/M31_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M31_rife.mp4", "public_path":"centralpark/motion/M31_rife.mp4", "act":2, "storyboard":"A2-05", "tags":["detective_backs_lean"] }
{ "asset_id":"CPK-M32", "source_scene_id":"MS32", "source_still":"H:/pd-media/assets/ai/centralpark/M32_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M32_rife.mp4", "public_path":"centralpark/motion/M32_rife.mp4", "act":2, "storyboard":"A2-08b", "tags":["page_line_pressure"] }
{ "asset_id":"CPK-M33", "source_scene_id":"MS33", "source_still":"H:/pd-media/assets/ai/centralpark/M33_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M33_rife.mp4", "public_path":"centralpark/motion/M33_rife.mp4", "act":2, "storyboard":"A2-09b", "tags":["house_of_cards_lean"] }
{ "asset_id":"CPK-M34", "source_scene_id":"MS34", "source_still":"H:/pd-media/assets/ai/centralpark/M34_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M34_rife.mp4", "public_path":"centralpark/motion/M34_rife.mp4", "act":3, "storyboard":"A3-01", "tags":["headline_wall_kinetic"] }
{ "asset_id":"CPK-M35", "source_scene_id":"MS35", "source_still":"H:/pd-media/assets/ai/centralpark/M35_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M35_rife.mp4", "public_path":"centralpark/motion/M35_rife.mp4", "act":3, "storyboard":"A3-02", "tags":["wilding_word_seized"] }
{ "asset_id":"CPK-M36", "source_scene_id":"MS36", "source_still":"H:/pd-media/assets/ai/centralpark/M36_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M36_rife.mp4", "public_path":"centralpark/motion/M36_rife.mp4", "act":3, "storyboard":"A3-03", "tags":["trump_ad_blank_frame"] }
{ "asset_id":"CPK-M37", "source_scene_id":"MS37", "source_still":"H:/pd-media/assets/ai/centralpark/M37_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M37_rife.mp4", "public_path":"centralpark/motion/M37_rife.mp4", "act":3, "storyboard":"A3-04", "tags":["chorus_drowns_presumption"] }
{ "asset_id":"CPK-M38", "source_scene_id":"MS38", "source_still":"H:/pd-media/assets/ai/centralpark/M38_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M38_rife.mp4", "public_path":"centralpark/motion/M38_rife.mp4", "act":3, "storyboard":"A3-06", "tags":["tv_glow_play_triangle"] }
{ "asset_id":"CPK-M39", "source_scene_id":"MS39", "source_still":"H:/pd-media/assets/ai/centralpark/M39_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M39_rife.mp4", "public_path":"centralpark/motion/M39_rife.mp4", "act":3, "storyboard":"A3-08", "tags":["dna_matches_none_table"] }
{ "asset_id":"CPK-M40", "source_scene_id":"MS40", "source_still":"H:/pd-media/assets/ai/centralpark/M40_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M40_rife.mp4", "public_path":"centralpark/motion/M40_rife.mp4", "act":3, "storyboard":"A3-09", "tags":["scale_tips_wrong_way"] }
{ "asset_id":"CPK-M41", "source_scene_id":"MS41", "source_still":"H:/pd-media/assets/ai/centralpark/M41_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M41_rife.mp4", "public_path":"centralpark/motion/M41_rife.mp4", "act":3, "storyboard":"A3-10", "tags":["harlem_parent_row_backs"] }
{ "asset_id":"CPK-M42", "source_scene_id":"MS42", "source_still":"H:/pd-media/assets/ai/centralpark/M42_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M42_rife.mp4", "public_path":"centralpark/motion/M42_rife.mp4", "act":3, "storyboard":"A3-12", "tags":["gavel_shadow_verdict"] }
{ "asset_id":"CPK-M43", "source_scene_id":"MS43", "source_still":"H:/pd-media/assets/ai/centralpark/M43_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M43_rife.mp4", "public_path":"centralpark/motion/M43_rife.mp4", "act":3, "storyboard":"A3-13", "tags":["two_tier_sentence_split"] }
{ "asset_id":"CPK-M44", "source_scene_id":"MS44", "source_still":"H:/pd-media/assets/ai/centralpark/M44_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M44_rife.mp4", "public_path":"centralpark/motion/M44_rife.mp4", "act":3, "storyboard":"A3-14", "tags":["korey_diverges_adult"] }
{ "asset_id":"CPK-M45", "source_scene_id":"MS45", "source_still":"H:/pd-media/assets/ai/centralpark/M45_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M45_rife.mp4", "public_path":"centralpark/motion/M45_rife.mp4", "act":3, "storyboard":"A3-11", "tags":["press_flash_storm_noface"] }
{ "asset_id":"CPK-M46", "source_scene_id":"MS46", "source_still":"H:/pd-media/assets/ai/centralpark/M46_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M46_rife.mp4", "public_path":"centralpark/motion/M46_rife.mp4", "act":4, "storyboard":"A4-01", "tags":["cell_window_seasons_shift"] }
{ "asset_id":"CPK-M47", "source_scene_id":"MS47", "source_still":"H:/pd-media/assets/ai/centralpark/M47_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M47_rife.mp4", "public_path":"centralpark/motion/M47_rife.mp4", "act":4, "storyboard":"A4-02", "tags":["empty_desk_years_taken"] }
{ "asset_id":"CPK-M48", "source_scene_id":"MS48", "source_still":"H:/pd-media/assets/ai/centralpark/M48_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M48_rife.mp4", "public_path":"centralpark/motion/M48_rife.mp4", "act":4, "storyboard":"A4-03", "tags":["yard_danger_arithmetic"] }
{ "asset_id":"CPK-M49", "source_scene_id":"MS49", "source_still":"H:/pd-media/assets/ai/centralpark/M49_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M49_rife.mp4", "public_path":"centralpark/motion/M49_rife.mp4", "act":4, "storyboard":"A4-04", "tags":["smaller_cell_door_open"] }
{ "asset_id":"CPK-M50", "source_scene_id":"MS50", "source_still":"H:/pd-media/assets/ai/centralpark/M50_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M50_rife.mp4", "public_path":"centralpark/motion/M50_rife.mp4", "act":4, "storyboard":"A4-09", "tags":["korey_spine_aging_drift"] }
{ "asset_id":"CPK-M51", "source_scene_id":"MS51", "source_still":"H:/pd-media/assets/ai/centralpark/M51_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M51_rife.mp4", "public_path":"centralpark/motion/M51_rife.mp4", "act":4, "storyboard":"A4-10", "tags":["solitary_box_frame_narrows"] }
{ "asset_id":"CPK-M52", "source_scene_id":"MS52", "source_still":"H:/pd-media/assets/ai/centralpark/M52_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M52_rife.mp4", "public_path":"centralpark/motion/M52_rife.mp4", "act":4, "storyboard":"A4-12", "tags":["closed_file_forgotten"] }
{ "asset_id":"CPK-M53", "source_scene_id":"MS53", "source_still":"H:/pd-media/assets/ai/centralpark/M53_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M53_rife.mp4", "public_path":"centralpark/motion/M53_rife.mp4", "act":4, "storyboard":"A4-13", "tags":["upstate_accident_nears"] }
{ "asset_id":"CPK-M54", "source_scene_id":"MS54", "source_still":"H:/pd-media/assets/ai/centralpark/M54_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M54_rife.mp4", "public_path":"centralpark/motion/M54_rife.mp4", "act":4, "storyboard":"A4-14", "tags":["paths_cross_yard"] }
{ "asset_id":"CPK-M55", "source_scene_id":"MS55", "source_still":"H:/pd-media/assets/ai/centralpark/M55_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M55_rife.mp4", "public_path":"centralpark/motion/M55_rife.mp4", "act":4, "storyboard":"A4-05", "tags":["child_alone_account"] }
{ "asset_id":"CPK-M56", "source_scene_id":"MS56", "source_still":"H:/pd-media/assets/ai/centralpark/M56_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M56_rife.mp4", "public_path":"centralpark/motion/M56_rife.mp4", "act":4, "storyboard":"A4-06", "tags":["conviction_at_every_door"] }
{ "asset_id":"CPK-M57", "source_scene_id":"MS57", "source_still":"H:/pd-media/assets/ai/centralpark/M57_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M57_rife.mp4", "public_path":"centralpark/motion/M57_rife.mp4", "act":4, "storyboard":"A4-08", "tags":["innocence_held_arc"] }
{ "asset_id":"CPK-M58", "source_scene_id":"MS58", "source_still":"H:/pd-media/assets/ai/centralpark/M58_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M58_rife.mp4", "public_path":"centralpark/motion/M58_rife.mp4", "act":5, "storyboard":"A5-01", "tags":["reyes_colder_silhouette"] }
{ "asset_id":"CPK-M59", "source_scene_id":"MS59", "source_still":"H:/pd-media/assets/ai/centralpark/M59_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M59_rife.mp4", "public_path":"centralpark/motion/M59_rife.mp4", "act":5, "storyboard":"A5-02", "tags":["prior_park_pindrop_abstract"] }
{ "asset_id":"CPK-M60", "source_scene_id":"MS60", "source_still":"H:/pd-media/assets/ai/centralpark/M60_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M60_rife.mp4", "public_path":"centralpark/motion/M60_rife.mp4", "act":5, "storyboard":"A5-03", "tags":["silence_ten_years_shift"] }
{ "asset_id":"CPK-M61", "source_scene_id":"MS61", "source_still":"H:/pd-media/assets/ai/centralpark/M61_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M61_rife.mp4", "public_path":"centralpark/motion/M61_rife.mp4", "act":5, "storyboard":"A5-04", "tags":["auburn_paths_cross"] }
{ "asset_id":"CPK-M62", "source_scene_id":"MS62", "source_still":"H:/pd-media/assets/ai/centralpark/M62_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M62_rife.mp4", "public_path":"centralpark/motion/M62_rife.mp4", "act":5, "storyboard":"A5-05", "tags":["alone_faultsplit"] }
{ "asset_id":"CPK-M63", "source_scene_id":"MS63", "source_still":"H:/pd-media/assets/ai/centralpark/M63_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M63_rife.mp4", "public_path":"centralpark/motion/M63_rife.mp4", "act":5, "storyboard":"A5-07", "tags":["truth_in_file_since_1989"] }
{ "asset_id":"CPK-M64", "source_scene_id":"MS64", "source_still":"H:/pd-media/assets/ai/centralpark/M64_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M64_rife.mp4", "public_path":"centralpark/motion/M64_rife.mp4", "act":5, "storyboard":"A5-08", "tags":["reinvestigation_word_to_lab"] }
{ "asset_id":"CPK-M65", "source_scene_id":"MS65", "source_still":"H:/pd-media/assets/ai/centralpark/M65_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M65_rife.mp4", "public_path":"centralpark/motion/M65_rife.mp4", "act":5, "storyboard":"A5-09", "tags":["dna_ladder_draws"] }
{ "asset_id":"CPK-M66", "source_scene_id":"MS66", "source_still":"H:/pd-media/assets/ai/centralpark/M66_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M66_rife.mp4", "public_path":"centralpark/motion/M66_rife.mp4", "act":5, "storyboard":"A5-10", "tags":["cold_cyan_flood_climax"] }
{ "asset_id":"CPK-M67", "source_scene_id":"MS67", "source_still":"H:/pd-media/assets/ai/centralpark/M67_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M67_rife.mp4", "public_path":"centralpark/motion/M67_rife.mp4", "act":5, "storyboard":"A5-11", "tags":["one_in_billions_resolve"] }
{ "asset_id":"CPK-M68", "source_scene_id":"MS68", "source_still":"H:/pd-media/assets/ai/centralpark/M68_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M68_rife.mp4", "public_path":"centralpark/motion/M68_rife.mp4", "act":5, "storyboard":"A5-12", "tags":["confession_false_vertigo"] }
{ "asset_id":"CPK-M69", "source_scene_id":"MS69", "source_still":"H:/pd-media/assets/ai/centralpark/M69_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M69_rife.mp4", "public_path":"centralpark/motion/M69_rife.mp4", "act":5, "storyboard":"A5-13", "tags":["korey_presence_spoke"] }
{ "asset_id":"CPK-M70", "source_scene_id":"MS70", "source_still":"H:/pd-media/assets/ai/centralpark/M70_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M70_rife.mp4", "public_path":"centralpark/motion/M70_rife.mp4", "act":5, "storyboard":"A5-14", "tags":["state_got_it_wrong_loop"] }
{ "asset_id":"CPK-M71", "source_scene_id":"MS71", "source_still":"H:/pd-media/assets/ai/centralpark/M71_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M71_rife.mp4", "public_path":"centralpark/motion/M71_rife.mp4", "act":5, "storyboard":"A5-11b", "tags":["ladder_single_band_align"] }
{ "asset_id":"CPK-M72", "source_scene_id":"MS72", "source_still":"H:/pd-media/assets/ai/centralpark/M72_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M72_rife.mp4", "public_path":"centralpark/motion/M72_rife.mp4", "act":5, "storyboard":"A5-10b", "tags":["cold_cyan_swell"] }
{ "asset_id":"CPK-M73", "source_scene_id":"MS73", "source_still":"H:/pd-media/assets/ai/centralpark/M73_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M73_rife.mp4", "public_path":"centralpark/motion/M73_rife.mp4", "act":5, "storyboard":"A5-06", "tags":["reyes_distance_cold"] }
{ "asset_id":"CPK-M74", "source_scene_id":"MS74", "source_still":"H:/pd-media/assets/ai/centralpark/M74_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M74_rife.mp4", "public_path":"centralpark/motion/M74_rife.mp4", "act":6, "storyboard":"A6-01", "tags":["signature_dissolves_vacatur"] }
{ "asset_id":"CPK-M75", "source_scene_id":"MS75", "source_still":"H:/pd-media/assets/ai/centralpark/M75_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M75_rife.mp4", "public_path":"centralpark/motion/M75_rife.mp4", "act":6, "storyboard":"A6-03", "tags":["first_dawn_amber_bleeds"] }
{ "asset_id":"CPK-M76", "source_scene_id":"MS76", "source_still":"H:/pd-media/assets/ai/centralpark/M76_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M76_rife.mp4", "public_path":"centralpark/motion/M76_rife.mp4", "act":6, "storyboard":"A6-04", "tags":["armstrong_footnote_setdown"] }
{ "asset_id":"CPK-M77", "source_scene_id":"MS77", "source_still":"H:/pd-media/assets/ai/centralpark/M77_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M77_rife.mp4", "public_path":"centralpark/motion/M77_rife.mp4", "act":6, "storyboard":"A6-06", "tags":["settlement_numbers_land"] }
{ "asset_id":"CPK-M78", "source_scene_id":"MS78", "source_still":"H:/pd-media/assets/ai/centralpark/M78_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M78_rife.mp4", "public_path":"centralpark/motion/M78_rife.mp4", "act":6, "storyboard":"A6-09", "tags":["rec_light_finally_on"] }
{ "asset_id":"CPK-M79", "source_scene_id":"MS79", "source_still":"H:/pd-media/assets/ai/centralpark/M79_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M79_rife.mp4", "public_path":"centralpark/motion/M79_rife.mp4", "act":6, "storyboard":"A6-10", "tags":["record_whole_interrogation"] }
{ "asset_id":"CPK-M80", "source_scene_id":"MS80", "source_still":"H:/pd-media/assets/ai/centralpark/M80_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M80_rife.mp4", "public_path":"centralpark/motion/M80_rife.mp4", "act":6, "storyboard":"A6-12", "tags":["renamed_exonerated_five"] }
{ "asset_id":"CPK-M81", "source_scene_id":"MS81", "source_still":"H:/pd-media/assets/ai/centralpark/M81_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M81_rife.mp4", "public_path":"centralpark/motion/M81_rife.mp4", "act":6, "storyboard":"A6-14", "tags":["dawn_horizon_open"] }
{ "asset_id":"CPK-M82", "source_scene_id":"MS82", "source_still":"H:/pd-media/assets/ai/centralpark/M82_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M82_rife.mp4", "public_path":"centralpark/motion/M82_rife.mp4", "act":7, "storyboard":"A7-01", "tags":["back_in_room_child_strip"] }
{ "asset_id":"CPK-M83", "source_scene_id":"MS83", "source_still":"H:/pd-media/assets/ai/centralpark/M83_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M83_rife.mp4", "public_path":"centralpark/motion/M83_rife.mp4", "act":7, "storyboard":"A7-03", "tags":["closing_door_produce_yes"] }
{ "asset_id":"CPK-M84", "source_scene_id":"MS84", "source_still":"H:/pd-media/assets/ai/centralpark/M84_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M84_rife.mp4", "public_path":"centralpark/motion/M84_rife.mp4", "act":7, "storyboard":"A7-08", "tags":["off_to_on_rec_final"] }
{ "asset_id":"CPK-M85", "source_scene_id":"MS85", "source_still":"H:/pd-media/assets/ai/centralpark/M85_src.png", "path":"H:/pd-media/assets/ai_video/centralpark/M85_rife.mp4", "public_path":"centralpark/motion/M85_rife.mp4", "act":7, "storyboard":"A7-09", "tags":["five_names_bone_white"] }
```

**検算:** 85エントリ ✓・全 public_path 非空 ✓（不変条件18）・`^CPK-M\d{2}$` ✓。

## 4.6 `overlay[]` 60エントリ（distinct 素材に数えない・30 particle / 20 light / 10 vfx）

```jsonc
{ "public_path":"centralpark/overlay/P01_cold_room_dust.mp4", "type":"particle_assets", "subtype":"cold_room_dust", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P02_archive_dust_cold.mp4", "type":"particle_assets", "subtype":"archive_dust_cold", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P03_lab_dust_motes.mp4", "type":"particle_assets", "subtype":"lab_dust_motes", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P04_fine_grain_dust.mp4", "type":"particle_assets", "subtype":"fine_grain_dust", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P05_night_air_drift.mp4", "type":"particle_assets", "subtype":"night_air_drift", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P06_shadow_dust.mp4", "type":"particle_assets", "subtype":"shadow_dust", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P07_cold_particle_fall.mp4", "type":"particle_assets", "subtype":"cold_particle_fall", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P08_interrogation_room_dust.mp4", "type":"particle_assets", "subtype":"interrogation_room_dust", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P09_courtroom_dust.mp4", "type":"particle_assets", "subtype":"courtroom_dust", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P10_prison_dust_cold.mp4", "type":"particle_assets", "subtype":"prison_dust_cold", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P11_street_dust_night.mp4", "type":"particle_assets", "subtype":"street_dust_night", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P12_paper_fiber_drift.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P13_cold_ash_drift.mp4", "type":"particle_assets", "subtype":"cold_ash_drift", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P14_dark_speck_drift.mp4", "type":"particle_assets", "subtype":"dark_speck_drift", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P15_evidence_room_dust.mp4", "type":"particle_assets", "subtype":"evidence_room_dust", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P16_cold_room_dust_02.mp4", "type":"particle_assets", "subtype":"cold_room_dust_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P17_archive_dust_cold_02.mp4", "type":"particle_assets", "subtype":"archive_dust_cold_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P18_lab_dust_motes_02.mp4", "type":"particle_assets", "subtype":"lab_dust_motes_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P19_fine_grain_dust_02.mp4", "type":"particle_assets", "subtype":"fine_grain_dust_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P20_night_air_drift_02.mp4", "type":"particle_assets", "subtype":"night_air_drift_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P21_shadow_dust_02.mp4", "type":"particle_assets", "subtype":"shadow_dust_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P22_cold_particle_fall_02.mp4", "type":"particle_assets", "subtype":"cold_particle_fall_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P23_interrogation_room_dust_02.mp4", "type":"particle_assets", "subtype":"interrogation_room_dust_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P24_courtroom_dust_02.mp4", "type":"particle_assets", "subtype":"courtroom_dust_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P25_prison_dust_cold_02.mp4", "type":"particle_assets", "subtype":"prison_dust_cold_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P26_street_dust_night_02.mp4", "type":"particle_assets", "subtype":"street_dust_night_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P27_paper_fiber_drift_02.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P28_cold_ash_drift_02.mp4", "type":"particle_assets", "subtype":"cold_ash_drift_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P29_dark_speck_drift_02.mp4", "type":"particle_assets", "subtype":"dark_speck_drift_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/P30_evidence_room_dust_02.mp4", "type":"particle_assets", "subtype":"evidence_room_dust_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L01_cold_cyan_shaft.mp4", "type":"light_assets", "subtype":"cold_cyan_shaft", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L02_cold_fluorescent_flicker.mp4", "type":"light_assets", "subtype":"cold_fluorescent_flicker", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L03_single_lamp_glow_cold.mp4", "type":"light_assets", "subtype":"single_lamp_glow_cold", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L04_cold_window_light_bar.mp4", "type":"light_assets", "subtype":"cold_window_light_bar", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L05_dawn_amber_edge_glow.mp4", "type":"light_assets", "subtype":"dawn_amber_edge_glow", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L06_cyan_cursor_glow.mp4", "type":"light_assets", "subtype":"cyan_cursor_glow", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L07_tv_scanline_glow_cold.mp4", "type":"light_assets", "subtype":"tv_scanline_glow_cold", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L08_cold_key_light_sweep.mp4", "type":"light_assets", "subtype":"cold_key_light_sweep", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L09_lab_panel_glow_cold.mp4", "type":"light_assets", "subtype":"lab_panel_glow_cold", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L10_interrogation_lamp_flicker.mp4", "type":"light_assets", "subtype":"interrogation_lamp_flicker", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L11_cold_cyan_shaft_02.mp4", "type":"light_assets", "subtype":"cold_cyan_shaft_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L12_cold_fluorescent_flicker_02.mp4", "type":"light_assets", "subtype":"cold_fluorescent_flicker_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L13_single_lamp_glow_cold_02.mp4", "type":"light_assets", "subtype":"single_lamp_glow_cold_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L14_cold_window_light_bar_02.mp4", "type":"light_assets", "subtype":"cold_window_light_bar_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L15_dawn_amber_edge_glow_02.mp4", "type":"light_assets", "subtype":"dawn_amber_edge_glow_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L16_cyan_cursor_glow_02.mp4", "type":"light_assets", "subtype":"cyan_cursor_glow_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L17_tv_scanline_glow_cold_02.mp4", "type":"light_assets", "subtype":"tv_scanline_glow_cold_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L18_cold_key_light_sweep_02.mp4", "type":"light_assets", "subtype":"cold_key_light_sweep_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L19_lab_panel_glow_cold_02.mp4", "type":"light_assets", "subtype":"lab_panel_glow_cold_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/L20_interrogation_lamp_flicker_02.mp4", "type":"light_assets", "subtype":"interrogation_lamp_flicker_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/V01_film_grain_fine.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine", "blend_hint":"overlay" }
{ "public_path":"centralpark/overlay/V02_cold_light_noise.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/V03_subtle_vignette_cold.mp4", "type":"vfx_overlays", "subtype":"subtle_vignette_cold", "blend_hint":"overlay" }
{ "public_path":"centralpark/overlay/V04_chromatic_edge_cold.mp4", "type":"vfx_overlays", "subtype":"chromatic_edge_cold", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/V05_cyan_glitch_min.mp4", "type":"vfx_overlays", "subtype":"cyan_glitch_min", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/V06_film_grain_fine_02.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine_02", "blend_hint":"overlay" }
{ "public_path":"centralpark/overlay/V07_cold_light_noise_02.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/V08_subtle_vignette_cold_02.mp4", "type":"vfx_overlays", "subtype":"subtle_vignette_cold_02", "blend_hint":"overlay" }
{ "public_path":"centralpark/overlay/V09_chromatic_edge_cold_02.mp4", "type":"vfx_overlays", "subtype":"chromatic_edge_cold_02", "blend_hint":"screen" }
{ "public_path":"centralpark/overlay/V10_cyan_glitch_min_02.mp4", "type":"vfx_overlays", "subtype":"cyan_glitch_min_02", "blend_hint":"screen" }
```

runtime で `asset_id`/`path`/`sha256`/`license`/`eyeballed_content`/`qc` を埋める（§9）。**overlay は `cuts[].src` に出さない。** 発色は B が accent `#2F9FC4`（cold steel-cyan）に寄せる想定・A は他話色（gold/blue/amber/teal/crimson/green/civil-violet/plum）の素材を選ばない。dawn-amber `#C98A3C` の overlay（L05 等）は exoneration/close 用の少数のみ。

---

# 5. A-1: SDXL 静止画のバッチ生成（430本 × 1枚・バリエーション0）— ★motif ライブラリ方式

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-050-centralpark/04_scenes/ai_prompts.v001.md   ← A が §5.9 の形式で書く
出力:  H:\pd-media\assets\ai\centralpark\S<NNN>.png（+ remotion/public/centralpark/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★430本の作り方＝「motif ライブラリ」テンプレート方式（430行を丸暗記でなく体系で書く）

430 の固有プロンプトを**幕×motifで体系化**する。各 motif に (a) **確定 distinct 枚数**、(b) **S番号レンジ**、(c) **literal 例プロンプト（正 + `Avoid:[NEG]`）** を与える。**あなたの仕事は、各 motif の例プロンプトを下敷きに、その motif に割り当てられた枚数ぶんの固有プロンプトを、被写体・角度・光・寄り引き・オブジェの状態を1枚ずつ変えて書き切ること**（同一構図の量産＝禁止。1枚1固有）。**motif 合計が幕の確定 still 数（§3.2）に一致し、全幕合計 430 になることを最後に検算する。**

> ★**1シーン1枚・variants 0。** `--variants 3` を使わない。反復回避は「430本の別被写体」で担保。各プロンプト末尾に §5.3 の `[STYLE]` を**全文連結**、`Avoid:` の後に §5.4 の `[NEG]` を**全文連結**。**body 430（この §5.2/§5.6 の象徴 still）は全て顔なし・人物なし・象徴・判読不能・被害者/暴行なし・Trump ad art なし**（★匿名人物は body ではなく §5.11 の H シリーズ i2v 種で出す）。

## 5.3 共通スタイル `[STYLE]`（★body 430 の象徴 still ＋ 69 の抽象 i2v 種のみに連結・DESIGN §5.3 と一字一致）

> **★scope（owner 改定）:** `[STYLE]`（"no people, no visible face…" を含む）と §5.4 `[NEG]` は **象徴 body 430 と抽象 i2v 種 69 に適用**する。**人物ビート（§5.11 の H シリーズ 16 i2v 種）は `[STYLE]`/`[NEG]` を使わず、専用の `[HSTYLE]`/`[HNEG]`（匿名人体は許可・実在 likeness は禁止）を使う。** これで「人物なしの象徴ルック」を大半で保ちつつ、16 の人物ビートだけ匿名人物を許す。

```
, cinematic still, somber documentary grade, a cold forensic steel-cyan key light as the one recurring cool note, near-black ink institutional gravity, an empty interrogation room of a chair a steel table a wall clock and an unlit REC lamp, abstract night park of treeline and a single lamp never any crime imagery, cold cyan gel-electrophoresis bands as the forensic motif, a single dawn-amber note reserved for the very end, five descending child-height silhouettes and one taller-but-young spine silhouette, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, backs and hands and objects only
```

> **EP39〜EP49 の色語（1語も含めない）:** electric blue（EP39）/ midday suburban demolition（EP40）/ sodium prison corridor・gold（EP41）/ warrant-blue・ankle monitor（EP42）/ porch-amber・ambulance（EP43）/ teal-green hospital（EP44）/ warm-tungsten kitchen・crimson overdue（EP45）/ forest-green（EP46）/ civil-violet・two-lane Texas road・pickup（EP47）/ EP48 glover 系 / somber-plum・Utah night parking lot（EP49）。**EP50 の色は cold steel-cyan `#2F9FC4` ＋ 末端のみ dawn-amber `#C98A3C`。**

## 5.4 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける・A/B 同一・DESIGN §5.4 と一字一致）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible confession, legible lab report, legible newspaper, legible case citation, legible date, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, front-facing person, the five defendants, Trisha Meili, Matias Reyes as a person, victim, assault, rape, violence, blood, gore, injury, weapon, sexual content, nudity, crime scene, re-enactment, Donald Trump ad artwork, newspaper front page reproduction, barred cell interior gore, sensational distress, poverty porn, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, electric blue, sodium prison corridor, porch amber, teal-green hospital, crimson overdue, forest-green, civil-violet, somber-plum
```

> ネガティブにも **制約違反語（"the five did it", "graphic assault", "Trump ad headline" 等）を書かない**（§1.3）。**被害者・暴行・現場・可読の confession/lab report/newspaper/citation・Trump ad art・鉄格子/独房の gore を NEG で明示抑制**（制約1〜6）。文字/紙面が必要な絵は「blurred into an unreadable smear」で判読不能に。
> **★scope（owner 改定）:** この `[NEG]` は `human face / identifiable face / portrait / front-facing person / human body` を抑制するので **象徴 body 430 ＋ 抽象 i2v 種 69 にのみ使う**。**人物ビート（§5.11 H シリーズ）には使わない**＝人物を弾いてしまうため。H シリーズは `[HNEG]`（匿名人体は許可・実在 likeness/被害者/暴行/可読テキストは禁止のまま）を使う。

## 5.5 プロンプトの絶対ルール（430本すべてに適用）

- **body 430 の象徴 still はこれまで通り「人物なし・象徴 silhouette のみ」で作る**（この 430 レーンと 69 の抽象 i2v 種は §5.3 `[STYLE]`／§5.4 `[NEG]` を使い続ける）。**★owner 改定: 匿名・非識別の人物（実在の誰にも似せない）は §5.11 の H シリーズ（i2v 種・専用 `[HSTYLE]`/`[HNEG]`）で別途出す**＝body 430 に人物を混ぜない。**5人・Meili・Reyes・実在の刑事/判事を個人として似せて描かない（実在 likeness 禁止・不変）。** 5人＝descending heights、Korey＝taller-but-young spine、Reyes＝separate colder（非識別）。**被害者・暴行は一切描かない（不変）。**
- **可読文字なし。** confession/lab report/newspaper/citation/ID/calendar は雰囲気のみ。日付・年齢・金額・DNA数値・ロゴを描かない。**Trump ad は空白の full-page 枠のみ（art/headline 再現禁止）。**
- **被害者・暴行・現場を一切描かない。** park は abstract（treeline/lamp/cold）のみ。injury/blood/weapon/re-enactment を作らない。
- **innocence 絶対（制約1）:** 5人が関与して見える絵を作らない。彼らは coerced false confession の被害者・exonerated。
- **Reyes を美化しない（制約3）:** cold・distance で。hero 化しない。
- **cold-cyan system（`#2F9FC4`）を基調に、dawn-amber `#C98A3C` は ACT6/close の該当 motif のみ**（§5.6 の per-act motif で指定）。
- **dochighlight を作らない・書かない（制約6）。**

## 5.6 ★motif ライブラリ（幕別・distinct 数確定・S番号レンジ・literal 例プロンプト）

> 各 motif ブロックは `motif名 — 枚数 — S番号レンジ` のヘッダ＋ literal 例（`- \`S0NN.png\`` 行＋プロンプト行）。**例で示した S番号は必ずその内容で作り、残りの枚数はその motif の変奏で埋める。** 各行の `[STYLE]`/`[NEG]` は §5.3/§5.4 を全文展開。

### ACT 0 — HOOK + OPENING（20枚・S001–S020）
- **interrogation_room_establishing — 8枚 — S001–S008**（S001 は also_thumb）
```
- `S001.png`
An empty interrogation-room chair found by a single cold forensic steel-cyan shaft of light in near-black, a steel table edge and an unlit red REC lamp faint in the dark, the room where it began, no person, no face, no readable text [STYLE] Avoid: [NEG]
- `S002.png`
A bare steel interrogation table under one cold-cyan overhead light in a near-black room, two empty chairs facing across it, institutional and silent, no person, no face, no readable text [STYLE] Avoid: [NEG]
- `S003.png`
A wall clock with an unreadable blank face on a cold institutional wall in near-black, the hours no one recorded, only the shape of a clock, no numerals, no person, no readable text [STYLE] Avoid: [NEG]
```
- **off_rec_light — 4枚 — S016–S019**（S018 は also_thumb・**OFF の赤ランプ = the film's signature**）
```
- `S018.png`
A single small red REC indicator lamp sitting UNLIT and dark on a video camera body in a near-black interrogation room, one cold-cyan edge catching the lens, the light that stayed off during the hours that mattered, no person, no face, no readable text [STYLE] Avoid: [NEG]
```
- **cold_cyan_light_finds — 4枚 — S009–S012**（黒→冷 cyan の一筋が chair/table を見つける）
- **opening_title_abstract — 4枚 — S013–S015, S020**（冷 cyan の abstract field・title 下地・park treeline の遠い予兆）

### ACT 1 — THE NIGHT（80枚・S021–S100）
- **nyc_1989_texture — 20枚 — S021–S040**（1989春のNYを mass に・subway graffiti を scar tissue に・遠い news の明滅）
```
- `S021.png`
A 1989 New York City subway car interior at night rendered as cold texture, scarred graffiti reading as unreadable abstract marks under failing fluorescent light, a braced anxious city, no people, no legible text [STYLE] Avoid: [NEG]
- `S030.png`
A cold Manhattan avenue at night in 1989 seen in deep telephoto compression, distant traffic light bloom, the city as an uneasy mass, no faces, no legible signage [STYLE] Avoid: [NEG]
```
- **park_abstract_night — 12枚 — S041–S052**（4/19 の park を**抽象**・treeline/lamp/cold・**crime は描かない**）
```
- `S045.png`
An abstract Central Park at night, only a bare treeline and a single cold lamp against deep blue-black, no path detail and no crime imagery, a place rendered as cold absence, no people, no readable text [STYLE] Avoid: [NEG]
```
- **five_descending_silhouettes — 10枚 — S089–S098**（S095 は also_thumb・14/14/15/15/16 の descending heights・まだ group ではない・別々）
```
- `S095.png`
Five child-height silhouettes standing at descending heights against a cold steel-cyan haze, seen only as dark shapes and backs, five separate children not yet a group, no faces, no features, no readable text [STYLE] Avoid: [NEG]
```
- **teen_mass_backs — 8枚 — S053–S060**（restless な後ろ姿の mass・no single will・顔なし）
- **precinct_institutional — 10枚 — S061–S070**（precinct が boys と parents で満ちる後ろ姿の群れ・3AM の巨大 building を見上げる）
- **the_collide_file — 8枚 — S071–S078**（二つの捜査が1本の file に snap・proximity のみ・no witness の空の指差し）
- **coma_vacuum — 4枚 — S079–S082**（記憶の a vacuum＝empty chair の echo・cold sink・被害者は描かない）
- **cursor_no_evidence — 4枚 — S083–S086**（jogger 攻撃への物証ゼロの cursor が blink）
- **lab_band_foreshadow — 4枚 — S087, S088, S099, S100**（lab に送られる cold-cyan band・Act5 の伏線・ignored）
```
- `S099.png`
A single cold steel-cyan horizontal band glowing faint inside a dark forensic file drawer, biological evidence sent to a lab and then ignored, an abstract gel band with no readable text, no people [STYLE] Avoid: [NEG]
```

### ACT 2 — THE INTERROGATIONS（110枚・S101–S210・engine・最密）
- **interrogation_room_variants — 25枚 — S101–S125**（room の変奏・windows なし・変わらない光・読めない clock）
```
- `S101.png`
A general interrogation room in cold steel-cyan light, an empty chair pulled out from a steel table, no window, a light that never changes, an unreadable wall clock, no person, no face, no readable text [STYLE] Avoid: [NEG]
```
- **detective_child_shadow — 12枚 — S126–S137**（detective 影と child 影の対峙・人物化しない・顔なし・後ろ姿）
```
- `S130.png`
Two shadows on a cold interrogation-room wall, one taller adult shadow leaning over one small child-sized shadow, cast shapes only and no bodies or faces, the pressure of the room, no readable text [STYLE] Avoid: [NEG]
```
- **story_migrate_type — 8枚 — S138–S145**（story fragment の "type" が detective 影 → child 影へ migrate＝false-evidence ploy を抽象化・可読文字なし）
- **technique_symbols — 12枚 — S146–S157**（技法①false-evidence ploy の嘘の "proof"（判読不能）／技法②minimization＝gentle trap＝閉じる扉）
```
- `S150.png`
A plain door in a cold interrogation room closing to a narrow gap of steel-cyan light, a gentle trap offered as a small admission, symbolic minimization, no person, no face, no readable text [STYLE] Avoid: [NEG]
```
- **signature_pen — 8枚 — S158–S165**（pen が page に line を書く・**pressure 下・Act6 で dissolve する motif の初出**・可読署名なし）
```
- `S158.png`
A plain pen pressed to a blank page under cold steel-cyan light, a single ink line being drawn under pressure, the signature that meant nothing, the writing an unreadable smear, no person, no face [STYLE] Avoid: [NEG]
```
- **confession_stack_house_of_cards — 15枚 — S166–S180**（five confession pages が stack、各々が次を cite する house of cards・可読文字なし）
```
- `S170.png`
Five blank confession pages stacked and leaning like a house of cards under cold steel-cyan light, each page's writing an unreadable smear, a structure with no foundation, no person, no readable text [STYLE] Avoid: [NEG]
```
- **dna_exclusion_band — 8枚 — S181–S188**（the rape kit・semen が五人を exclude する lab report＝cold-cyan・file の中・Act5 の払い戻しの伏線）
- **ghost_sixth_silhouette — 6枚 — S189–S194**（unknown な真犯人の empty silhouette・real name は 2002・顔なし）
- **pressure_machine — 8枚 — S195–S202**（why detectives did it＝men under pressure・monsters ではない・機械/歯車の比喩・顔なし）
- **tv_glow_after_hours — 4枚 — S203–S206**（録画は confession の最後だけ＝TV glow が hours の後にだけ点く）
- **clock_room_close — 4枚 — S207–S210**（S210 は also_thumb・the room / clock の close・変わらない光）
```
- `S210.png`
A cold interrogation room reduced to its essentials in steel-cyan light, an empty chair, a steel table, and an unreadable wall clock, the room that produced the words, no person, no face, no numerals, no readable text [STYLE] Avoid: [NEG]
```

### ACT 3 — THE TRIALS（58枚・S211–S268・publicity の machine・the scale tips）
- **headline_wall — 12枚 — S211–S222**（headline mass の oppressive kinetic wall・"wolf pack"/"wilding" は press の label・**可読の紙面文字なし**）
```
- `S215.png`
An oppressive wall of overlapping newspaper pages rendered as an abstract mass under cold light, every headline an unreadable blur, the press storm of 1989, no legible words, no faces, no readable text [STYLE] Avoid: [NEG]
```
- **trump_blank_frame — 4枚 — S223–S226**（1989/5/1 の full-page ad＝**dated context の 1枚**・**ad art/headline 再現禁止**・空白の full-page 枠のみ）
```
- `S223.png`
A single blank full-page newspaper advertisement frame, an empty bordered rectangle on newsprint under cold light, a paid full-page space with nothing legible printed in it, no artwork, no headline, no faces, no readable text [STYLE] Avoid: [NEG]
```
- **courthouse_columns — 8枚 — S227–S234**（NY 州最高裁の marble columns・cold institutional・SCOTUS-of-NY の荘厳）
- **courtroom_empty — 8枚 — S235–S242**（empty courtroom・jury box・thin evidence・no eyewitness/no weapon）
- **scale_tips_wrong — 6枚 — S243–S248**（the scale が confession 側に wrong way に tip・Act6 で戻る motif の初出）
```
- `S245.png`
A plain balance scale under cold steel-cyan light tipping the wrong way, a stack of blank confession pages outweighing a single cold-cyan evidence band, symbolic and severe, no person, no readable text [STYLE] Avoid: [NEG]
```
- **tv_play_triangle — 6枚 — S249–S254**（the tapes＝TV glow・**play triangle**・confession performed・顔は描かない）
- **dna_exclusion_trial — 6枚 — S255–S260**（DNA matches no one at the table＝cold-cyan の exclusion）
- **sentence_split — 4枚 — S261–S264**（sentence 二層＝FOUR juvenile ↔ Korey as an adult・可読数字なし・象徴）
- **families_backs — 4枚 — S265–S268**（S268 は also_thumb だが内容は cold DNA bands＝下記注記参照。families never wavered の親影の row・顔なし）
```
- `S268.png`
A set of cold steel-cyan gel-electrophoresis bands glowing in a dark forensic frame, the physical evidence that matched none of the five at trial, an abstract ladder of light with no readable text, no people [STYLE] Avoid: [NEG]
```
> ★S268 は also_thumb（cold DNA bands）＝この幕の「DNA が誰にも一致しない exclusion」を象徴する cold-cyan band にする（families_backs の変奏ではなく DNA band を S268 に固定）。

### ACT 4 — THE LOST YEARS（63枚・S269–S331・slow・individuals・Korey the spine）
- **cell_window_seasons — 12枚 — S269–S280**（単一 cell window に seasons が横切る・**calendar-flip 禁止**・光の色温度 shift・earned breath）
```
- `S269.png`
A single institutional cell window abstracted to a pale rectangle of light, the color temperature shifting from cold winter to thin summer across it, seasons passing with no calendar and no person, no readable text [STYLE] Avoid: [NEG]
```
- **korey_spine_aging — 12枚 — S320–S331**（S331 は also_thumb・Korey Wise の taller-but-young spine silhouette・adult system・aging drift・顔なし）
```
- `S331.png`
A single taller-but-still-young silhouette seen only from behind in a cold institutional light, shoulders lowered by years, the one who served the longest, no face, no features, no readable text [STYLE] Avoid: [NEG]
```
- **solitary_box — 8枚 — S281–S288**（long solitary＝box の中の単一影・frame itself narrows・非扇情）
- **individual_silhouettes — 12枚 — S289–S300**（四人 younger の individual silhouettes・child asked to account alone・後ろ姿）
- **years_taken_empty — 8枚 — S301–S308**（what is taken＝school/first job/first love の空席・a person assembled する years）
- **prison_institutional — 7枚 — S309–S315**（prison-adjacent の非扇情な institutional 象徴・cold corridor・heavy door・**鉄格子/gore なし**）
- **paths_cross_upstate — 4枚 — S316–S319**（upstate の accident が近づく・yard/corridor で二つの影が交わる・顔なし）

### ACT 5 — THE CONFESSION & THE DNA（40枚・S332–S371・reversal・visual climax）
- **reyes_colder_silhouette — 8枚 — S332–S339**（Matias Reyes＝separate, colder silhouette・convicted・**美化しない**・cold/distance・顔なし）
```
- `S332.png`
A single separate silhouette standing apart in a colder, harder light than the rest of the film, seen only as a dark back at a distance, the man the DNA identified, no face, no glorification, no readable text [STYLE] Avoid: [NEG]
```
- **dna_ladder_climax — 12枚 — S346–S357**（DNA ladder が draw・one in billions・single match に align・**cold-cyan が満ちる payoff**）
```
- `S350.png`
A cold steel-cyan gel-electrophoresis ladder drawing itself band by band in near-black, five faint lanes reading as NO MATCH and one lane snapping into a single aligned bright band, the forensic hinge, abstract, no readable numerals, no people [STYLE] Avoid: [NEG]
```
- **cold_cyan_flood — 8枚 — S358–S365**（the climax＝cold-cyan FLOOD・唯一の声上げ・貯めた色の payoff）
- **faultsplit_alone — 4枚 — S340–S343**（"Alone."＝state の crowd theory を one man が壊す・faultsplit の象徴）
- **reinvestigation — 4枚 — S344, S345, S366, S367**（Morgenthau/Nancy Ryan の reinvestigation＝word を lab に持って行く・truth は 1989 から file の中に）
- **prior_park_pindrop — 4枚 — S368–S371**（4/17/1989＝2日前、同じ park の別 rape＝same signature・pindrop abstracted・hedged・現場は描かない）

### ACT 6 — EXONERATION & RECKONING（44枚・S372–S415・signature dissolves・first dawn・REC ON）
- **signature_dissolve — 6枚 — S372–S377**（S372 は also_thumb・2002/12/19 の vacatur＝**signature が dissolve/erase**・Act2 の署名 motif の反転・particle disperse）
```
- `S372.png`
A single ink signature line on a blank page un-writing itself under cold light, the ink lifting away stroke by stroke into fine particles, a conviction being erased, the writing an unreadable smear, no person, no readable text [STYLE] Avoid: [NEG]
```
- **dawn_amber_first — 6枚 — S378–S383**（冷 cyan に **first dawn-amber `#C98A3C`** が滲む・唯一の暖色の初出・地平線）
- **settlements_money — 6枚 — S384–S389**（2014 ~$41M / 2016 ~$3.9M＝years に比例・money は justice ではない・可読金額なし・象徴）
- **rec_light_on — 4枚 — S390–S393**（**REC light が finally ON**＝HOOK の OFF signature の反転・reform の象徴・赤ランプが点灯）
```
- `S390.png`
A single small red REC indicator lamp finally glowing lit and warm on a camera body in a cold room, the light that was off all film now on, the reform, a first note of dawn-amber at the edge, no person, no readable text [STYLE] Avoid: [NEG]
```
- **reform_record — 4枚 — S394–S397**（record the WHOLE interrogation＝16 hours を jury が見られる・象徴）
- **survivor_dignity — 4枚 — S398–S401**（the survivor への obligation＝recovered・own story・二つの harm・**Meili を描かない**・abstract な dawn・empty chair の rest）
- **renamed_five — 4枚 — S402–S405**（the men＝advocates・renamed THE EXONERATED FIVE・五つの silhouette が立ち上がる・顔なし）
- **armstrong_footnote — 3枚 — S406, S407, S414**（Armstrong Report＝small footnote・visually minor・quickly set down・**却下された反対説としてのみ**）
- **lawsuit_institution — 4枚 — S409–S412**（city が a decade 争う・institution の抵抗の象徴）
- **dawn_horizon — 4枚 — S408, S413, S415, +（S408 は also_thumb）**（dawn horizon＝the first warm note・open sky・plum ではなく amber）
```
- `S408.png`
A wide open dawn horizon in deep cold blue giving way to a single band of warm dawn-amber light, the first warmth allowed in the whole film, no people, no crime imagery, no readable text [STYLE] Avoid: [NEG]
```

### ACT 7 — WHAT A CONFESSION IS WORTH（15枚・S416–S430・second-person・strip to essentials）
- **room_strip — 5枚 — S416–S420**（"back in the room. As the child."＝chair だけ残る strip・単一 cyan light・HOOK 回収）
```
- `S416.png`
A single empty chair alone in a stripped near-black frame under one cold steel-cyan light, everything else removed, back in the room as the child, no person, no face, no readable text [STYLE] Avoid: [NEG]
```
- **rec_final_contrast — 3枚 — S421–S423**（OFF→ON の REC light の最終対比・chair/clock/essentials）
- **five_names_plate — 3枚 — S424–S426**（五つの名前を出す下地＝bone-white の名前は AE/typo＝B。A は五つの descending silhouette が並ぶ abstract な下地・顔なし）
- **closing_door — 2枚 — S427, S428**（the room built to produce a "yes"＝closingdoor・静か）
- **dawn_edge_final — 2枚 — S429, S430**（final breath・restraint returns・冷 cyan に dawn-amber の一筋）

## 5.7 幕別 motif 枚数の検算（★Codex は書き終えたら足して確認）

```
ACT0  : 8+4+4+4 = 20
ACT1  : 20+12+10+8+10+8+4+4+4 = 80
ACT2  : 25+12+8+12+8+15+8+6+8+4+4 = 110
ACT3  : 12+4+8+8+6+6+6+4+4 = 58
ACT4  : 12+12+8+12+8+7+4 = 63
ACT5  : 8+12+8+4+4+4 = 40
ACT6  : 6+6+6+4+4+4+4+3+4+4 = 45  ← ★ +1 過剰。dawn_horizon を 3枚(S408,S413,S415)に減らし 44 に合わせる
ACT7  : 5+3+3+2+2 = 15
合計   : 20+80+110+58+63+40+44+15 = 430 ✓
```
> ★ACT6 は motif の素朴合計が45になる箇所がある（dawn_horizon を4と数えた場合）。**dawn_horizon は S408/S413/S415 の3枚**とし、ACT6 を **44枚**（§3.2 確定値）に一致させる。**最終的に S001..S430 の連番が穴なく430行**そろっていることを `--only S001` の `shots=515`（430 body + 85 i2v種）で確認する。

## 5.8 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_centralpark_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.9 パーサ契約（`read_prompts()` はこの2行形式しか読まない）

```
- `S001.png`
<positive prompt> Avoid: <negative>
```
- **1行目:** `` - `S001.png` ``（バッククォート囲み・行末は `.png` の直後）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト
- `ai_prompts.v001.md` は **body 430行（S001..S430）＋ i2v 種 85行（M01_src..M85_src、§8.1a）＝ 515 エントリ**を書く。すべて1枚生成。

## 5.10 生成コマンド（★variants 指定なし。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=515 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 50 --only S001
#   → ログ "episode=... shots=515 ... -> N images" の shots が 515 であること（430 body + 85 i2v種）

# 全515枚（body 430 + i2v種 85・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-050-centralpark
#   → 生成 S001.png ... S430.png / M01_src.png ... M85_src.png（各1枚。_02/_03 は作らない）
```
> QC で落ちたシーンの再生成は `--only S137`（同じプロンプトで別シードを1枚）。**基準を下げない・バリエーションで水増ししない。** ★515枚は**複数バッチ・複数時間**。夜間で回し、進捗をログで確認。

## 5.11 ★人物画像（匿名・ドラマ化スタンドイン）— HUMAN-FIGURE prompts（owner 追加指示・EP50 が「空/寂しい」にならないための人物ビート）

> **owner directive（本作追加）:** 「必要な人物画像は追加でプロンプトを書き込んで」。owner は **匿名化された人物（実在の顔ではない・ドラマ化スタンドイン）** を明示的に選択した。5人・実在の刑事・被害者・Reyes・Trump・判事の **likeness を作らない**。**実在の誰にも似せない一般化された人物**で、**実在人物が示唆される所（5人・刑事等）は顔を非識別**（背向き/横顔を影に/逆光でシルエット化/目から下でクロップ/浅い被写界深度でソフト）にする。**被害者・暴行・現場は絶対に描かない（R-VICTIM 継続）。** 少年は**強要・脆弱・冤罪の経験**を描くのであって**有罪/加害を示唆しない（R-INNOCENCE 継続）。**

> ### ★★★ RECONCILIATION — RESOLVED（owner 承認済・EP50 は本 §5.11 の匿名人物を採用する）★★★
> **owner 決定:** in-video の人物＝**匿名の一般人**を許可。R2/R-FACE を「顔・人体ゼロ」から**「匿名・非識別の人物と顔は可」**に緩和。**実在人物の likeness（5人・被害者 Meili・Reyes・Trump・実在の刑事/判事/検事）・被害者の描写・暴行の imagery・可読テキスト/偽公文書は引き続き HARD 禁止。少年は脆弱/強要される側で描き、有罪/加害に見せない（R-INNOCENCE 不変）。** この方針で以下は**解消済み**（本書内で反映済）:
> 1. **R2/R-FACE**（DESIGN §1・CODEX_A §1.1/§1.2/§5.5・CODEX_B §2.1/§2.3）＝「匿名は可、実在 likeness は不可」に**改定済**。
> 2. **SDXL NEG**＝`[STYLE]`/§5.4 `[NEG]` は象徴 body 430 ＋ 抽象 i2v 種 69 に**scope 限定済**。H シリーズは専用 `[HSTYLE]`/`[HNEG]`（匿名人体は許可・実在 likeness/被害者/暴行/可読テキストは禁止）。
> 3. **manifest `--verify`**＝`BANNED_PORTRAIT` を実在 likeness のみへ**改定済**（§1.3）。不変条件7を「`has_readable_text` か `has_identifiable_real_person` のみ reject・`has_human_body` は許可」に**改定済**（§4.2）。
> 4. **`check_centralpark_facts.py` R-FACE**（CODEX_B §2.1/§2.3）＝「実在 likeness/被害者/暴行のみ FAIL・匿名人物は許可」に**改定済**。
> 5. **counts/lane**＝下記「lane 定義」で **locked counts を1つも変えずに** H を i2v/motion レーンへ吸収（**additive にしない**）。`shots=515` も維持。

### ★lane 定義（owner: 「人物は動かす＝紙芝居にしない」→ H は motion レーンへ・locked counts 不変）

**H001–H016 は「新規の静止カット」ではなく、既存 85本の i2v 種のうち 16本の中身（＝人物ビート）として作る。additive にしない。**

- **role = `i2v_source`**（body には回さない）。**85本の i2v 種のうち 16本を人物ビートに充て**、残り **69本を従来の抽象/象徴種**（§4.5/§8.1a）とする。per-act の i2v 種数（§3.2/§4.5: HOOK3/ACT1 12/ACT2 18/ACT3 12/ACT4 12/ACT5 16/ACT6 8/ACT7 4）は**変えず**、その内数として人物種を **ACT1×2・ACT2×5・ACT3×6・ACT4×2・ACT6×1 ＝16** 充てる。
- **asset_id は既存の i2v 種 ID 空間（`^CPK-MS\d{2}$`）の 16本を占有**する（H001–H016 は本書内のラベル＝その 16本の種プロンプト内容）。種画像ファイルは i2v 種の命名 `M<NN>_src.png`（§8.1a）に従う（H ラベルと M<NN> の対応は §8.1a の該当行に注記）。**`public_path==null`（i2v 種は本編カットに出ない・§3.2）・depth 不要。**
- 各人物種は **Wan 2.2 A14B → RIFE（§8）で motion 化**され、**85本の motion（`^CPK-M\d{2}$`）のうち 16本**になり、**170 motion カットのうち最大 32カット**（各≤2回）に出る＝**人物は動く**。
- **QC フラグ:** `has_human_body:true`（許可）・`has_identifiable_real_person:false`（必須）・`has_readable_text:false`（必須）。§8.5 の i2v 目視で「実在 likeness/被害者/暴行/可読テキストなし・顔は非識別（背向き/影/ソフト）」を確認。
- **★locked counts は1つも変わらない:** still_body **430** / still_i2v_source **85**（＝抽象 69 ＋ 人物 16）/ motion **85** / factory **485** / overlay **60**；cuts **505/485/170 = 1,160**；still-share **0.4353**；first-use **0.8621**；`ai_prompts.v001.md` は **515エントリのまま**（`shots=515`・§5.10）。**H は 85 i2v 種の内数なので新規行を増やさない**（16本の種プロンプトを人物内容で書くだけ）。
- **i2v 種の書式:** H プロンプトは §8.1a と同じ「poised, still, about to move（動く直前の静止）」の i2v 種として読む（motion は Wan が付ける）。下記16本を `[HSTYLE]`/`[HNEG]` で書き、`ai_prompts.v001.md` では該当する 16本の `M<NN>_src.png` 行として出力する。

**共通スタイル `[HSTYLE]`（各 H プロンプト末尾に全文連結・匿名/非識別/photoreal/cold steel-cyan）:**
```
, cinematic photoreal still, documentary reenactment stand-in, generic anonymized people who resemble no real individual, faces kept non-identifiable where a real person is implied — turned away, in profile lost to shadow, back-lit to a silhouette, cropped below the eyes, or thrown soft in shallow focus, a cold forensic steel-cyan key light as the one recurring cool note, near-black ink institutional gravity, low-key deep-shadow lighting, telephoto compression, shallow depth of field, restrained dignified framing, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no readable documents or signage, a single dawn-amber note only where the beat is exoneration
```
**共通ネガティブ `[HNEG]`（各 `Avoid:` の後に全文連結・★匿名人体は許可、実在 likeness/被害者/暴行/可読テキストは禁止のまま）:**
```
recognizable real person, likeness of a specific person, the actual Central Park Five, Antron McCray, Kevin Richardson, Yusef Salaam, Raymond Santana, Korey Wise, Trisha Meili, Matias Reyes, Donald Trump, any real detective or judge or prosecutor, celebrity, mugshot, deepfake, text, words, letters, numbers, captions, watermark, logo, readable document, legible confession, legible newspaper, legible case citation, legible date, license plate, the victim, the jogger, any depiction of the assault, the attack, rape, violence, blood, gore, injury, weapon, sexual content, nudity, crime scene, re-enactment of the attack, a menacing or guilty framing of the youths, sensational distress, poverty porn, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, electric blue, sodium prison corridor, porch amber, teal-green hospital, crimson overdue, forest-green, civil-violet, somber-plum
```

### ACT 1 — THE NIGHT（precinct が boys と parents で満ちる・script L49・near S061–S070）
```
- `H001.png`
A crowded precinct hallway at three in the morning, anonymous teenage youths and worried parents waiting under cold fluorescent light, all seen from behind and in deep shadow so no face reads, small figures dwarfed by an institutional building, the night two investigations quietly became one [HSTYLE] Avoid: [HNEG]
- `H002.png`
A single anonymous teenage boy sitting small on a precinct bench against a cold institutional wall, shoulders hunched, face turned down and lost to shadow, alone and waiting, backlit by a corridor's steel-cyan glow, no identifiable features [HSTYLE] Avoid: [HNEG]
```

### ACT 2 — THE INTERROGATIONS（the room・detectives・signing・script L71–91・near S101–S165）
```
- `H003.png`
A lone anonymous fourteen-year-old stand-in seated at a bare steel table in a windowless interrogation room under one harsh overhead light, head bowed and face turned away so it cannot be identified, small and exhausted and vulnerable — never menacing, the child the room was built to wear down [HSTYLE] Avoid: [HNEG]
- `H004.png`
Seen from behind the seated youth toward a blank wall and a closed door, only the child's back and the nape of his neck in frame while a taller adult figure looms out of focus at the edge, the patient pressure of the room, no faces visible [HSTYLE] Avoid: [HNEG]
- `H005.png`
Two anonymous plainclothes detective stand-ins at a cluttered precinct desk, both seen from behind and backlit to near-silhouette, one leaning in calmly rather than shouting, generic men under pressure, no identifiable faces, cold steel-cyan light [HSTYLE] Avoid: [HNEG]
- `H006.png`
Close on a pair of anonymous young hands pressing a pen to a blank statement page under cold steel-cyan light, the ink an unreadable smear, the signature that meant nothing being drawn under pressure, no face, no legible text [HSTYLE] Avoid: [HNEG]
- `H007.png`
A stenographer's anonymous hands over a period typewriter and a statement pad in a cold institutional room, shot over the shoulder so no face reads, the paper blurred illegible, a coerced account being transcribed as if it were routine [HSTYLE] Avoid: [HNEG]
```

### ACT 3 — THE TRIALS（courtroom・press・families・script L101–121・near S211–S268）
```
- `H008.png`
An anonymous prosecutor stand-in standing at a courtroom podium, seen from behind and three-quarter with the face lost to shadow, addressing an unseen jury in a cold wood-and-marble courtroom, dignified and grave, no readable text or signage [HSTYLE] Avoid: [HNEG]
- `H009.png`
A 1990 jury box of twelve anonymous jurors, faces shadowed, soft-focus and non-identifiable, all turned toward an unseen television screen, cold institutional light, the tapes about to convict, no readable text [HSTYLE] Avoid: [HNEG]
- `H010.png`
A young anonymous defendant stand-in seated small at a defense table beside the shoulder of an adult lawyer, seen from behind so no face reads, the child dwarfed by the courtroom, cold steel-cyan light, no legible documents [HSTYLE] Avoid: [HNEG]
- `H011.png`
A scrum of anonymous news-camera crews and reporters with shoulder-mounted cameras and microphones crowding courthouse steps, generic press seen from behind and in motion blur, the media hunt of 1989, no readable logos or text [HSTYLE] Avoid: [HNEG]
- `H012.png`
Anonymous Harlem families and parents seated with quiet dignity in a courtroom gallery, seen from behind or thrown soft in shallow focus so no face reads, the families who never wavered, cold light, restrained and grave [HSTYLE] Avoid: [HNEG]
- `H013.png`
A small determined crowd of anonymous protesters outside a courthouse holding blank text-free placards aloft, seen mostly as backs and silhouettes against cold daylight, community support for the accused children, no readable signs or logos [HSTYLE] Avoid: [HNEG]
```

### ACT 4 — THE LOST YEARS（prison・solitary・script L129–139・near S269–S331）
```
- `H014.png`
A lone anonymous young man stand-in sitting on the edge of a bunk in a bare prison cell, seen from behind with the face lost to shadow, small in the frame and still, the stolen years, dignified and non-sensational, cold light, no gore [HSTYLE] Avoid: [HNEG]
- `H015.png`
A solitary anonymous figure against a bare cell wall under a single high cold light, knees drawn up and back to the camera, the long years of solitary confinement rendered as restraint and absence, no face, no violence [HSTYLE] Avoid: [HNEG]
```

### ACT 6 — EXONERATION（free men・dawn・script L181–197・near S372/S408）
```
- `H016.png`
Five anonymous grown men stand-ins — adults now, not boys — standing together on courthouse steps in the first warm dawn-amber light breaking a cold blue morning, seen from behind facing the light, free and dignified, no faces visible, the renaming into the Exonerated Five [HSTYLE] Avoid: [HNEG]
```

> **★H シリーズ ビート対応表（act / serves・全て匿名・非識別・実在 likeness なし・i2v 種として motion 化）:** H001 precinct hallway(ACT1) · H002 youth waiting(ACT1) · H003 youth alone in interrogation(ACT2) · H004 over-shoulder child + looming adult(ACT2) · H005 detectives at desk(ACT2) · H006 signing hands(ACT2) · H007 stenographer hands(ACT2) · H008 prosecutor podium(ACT3) · H009 jurors in box(ACT3) · H010 young defendant at table(ACT3) · H011 news crews/reporters(ACT3) · H012 families in gallery(ACT3) · H013 protesters outside courthouse(ACT3) · H014 lone man in prison cell(ACT4) · H015 solitary figure(ACT4) · H016 exonerated men on courthouse steps at dawn(ACT6)。**計16本＝85 i2v 種の内数（ACT1×2・ACT2×5・ACT3×6・ACT4×2・ACT6×1）。** owner 承認済（RESOLVED）。`ai_prompts.v001.md` では**新規行を足さず**、該当する 16本の `M<NN>_src.png` 行を上記の人物内容＋`[HSTYLE]`/`[HNEG]` で書く（`shots=515` 維持）。§8.1a に H↔M<NN> 対応を注記し、§8.5 で「実在 likeness/被害者/暴行/可読テキストなし・顔非識別」を目視確認。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 430 + i2v種 85 = 全515枚・`qc_centralpark_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `24.0<=mean_luma<=225.0`（EP50 は near-black ink・cold-cyan の低照度が多く全体に暗い→黒潰れリスク大。`DARK_LUMA_FLOOR` を大きく下回る本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**バリエーション0なので本来ほぼ衝突しない。衝突は room系(S001/S002/S101/S210/S416)・five silhouettes(S095/S402系)・DNA band(S087/S099/S181系/S268/S346–S357)・cell window(S269–S280)・headline wall(S211–S222)・courthouse columns(S227–S234)・signature(S158系/S372)・REC light(S018/S390/S421) の被りに注意** | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・日付(1989/2002/2014)・年齢(14–16)・金額($41M)・DNA(1 in 6,000,000,000)・新聞紙面・Trump ad の headline/art・ロゴが写っていないか（R1・制約2） | `has_readable_text=true`→reject |
| Q6 | **実在人物**の顔の混入（owner 改定） | **目視。** **実在人物として識別可能な顔**（5人/Meili/Reyes/Trump/実在の刑事/判事/検事に**似た**顔）が写っていないか。**匿名・非識別の一般人の顔（H シリーズ・背向き/影/ソフト）は OK。** 象徴 body 430 の silhouette が特定実在人物に転じていないか | `has_identifiable_real_person=true`→reject（**匿名顔は reject しない**） |
| Q7 | 被害者/暴行/gore の混入（owner 改定） | **目視。** 被害者の描写・暴行/injury/blood/weapon・鉄格子 gore が写っていないか（制約2/3）。**★匿名の人体そのものは OK（`has_human_body=true` でも reject しない）。** body 430 は象徴のまま人物を入れない・人物は H シリーズ（i2v 種）に限る | 被害者/暴行/gore があれば reject（`has_human_body=true` 単独では reject しない） |

**Q5/Q6/Q7 は機械で判定しない。全515枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-050-centralpark --media image
#   → runs/qc/centralpark_footage_contact_NN.png（20枚/シート・約26シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-49 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** SDXL は平気で読める文字・顔・身体を描く。**特に S223–S226（Trump 空白枠）は headline/art が写らないこと、S211–S222（headline wall）は読める紙面文字が無いこと、S181–S188/S268/S346–S357（DNA band）は読める数字が無いこと、S095/S402系（five silhouettes）と Korey/Reyes 影は顔・横顔が写らないこと、S045系（park）は crime imagery が無いこと、S398–S401（survivor）は Meili が描かれないこと、prison 系(S309–S315)は鉄格子 gore が無いこと、を必ず目で確認する。**

## 6.2 出力

```
episodes/PD-2026-050-centralpark/05_visuals/still_qc.v001.json     # 515枚全部の行（reject も残す）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が (body430 / i2v85) に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 50 --only S137   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_centralpark_stills.py
```
accepted body >= 430 かつ i2v_source >= 85 になるまで繰り返す。**基準を下げない・水増ししない。**

## 6.4 depth map（★既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/centralpark"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`。冪等。
- **role が `body` の静止画（430枚）は depth 必須**（無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/centralpark/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 485本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（1989 NYの街/subway/夜の道・precinct 外観・institutional 廊下/room・
                                          NY州最高裁/courthouse 外観/廊下/空の法廷・prison-adjacent の非扇情な外観/窓/廊下・
                                          abstract park 夜景・lab/records/evidence room・dawn/薄明の街・繋ぎ）
  light_assets/    …            合成レイヤー（cold-cyan shaft・cold fluorescent・cyan cursor・dawn-amber edge）
  particle_assets/ …            合成レイヤー（cold room dust・archive/lab dust・night air）
  vfx_overlays/    …            合成レイヤー（grain・cold light noise・cyan glitch min）
  texture_assets/  …            紙・石・concrete のテクスチャ
  loops/           …            抽象的な繋ぎ
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>（TYPECODE = BG|LIGHT|LOOP|PART|TEX|VFX）
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json
   （トップキーは schema と assets。★必ず encoding="utf-8" で開く。cp932 既定だと落ちる）
```

## 7.2 選定条件

- **`kind=="video"` のみ。** 静止画 factory は使わない
- **485本ちょうど**（§3.3[7] より 485 は still-share≤0.45 を守り motion coverage≥0.45 を保つ設計値）
- **各1回しか使わない**（`MAX_USES_FACTORY=1`）
- 幕別割り当て（§4.4）: HOOK+OPENING=12 / ACT1=70 / ACT2=70 / ACT3=65 / ACT4=70 / ACT5=55 / ACT6=50 / ACT7=20 ＋ 繋ぎ=73 ＝ 485
- **EP39〜EP49 の絵柄を選ばない（§7.7 の分離語）。** EP50 は 1989 NYの街/subway/夜の道・precinct/institutional の room/廊下・NY州最高裁/courthouse・prison-adjacent の非扇情な外観/窓/廊下・abstract park 夜景・lab/records・dawn/薄明。**鉄格子内部の gore/独房の暴力を選ばない。病院/臨床(EP44)・テキサスの二車線道/ピックアップ(EP47)・Utah の駐車場(EP49)を選ばない。被害者/暴行/泣く人/実在の顔が写るニュース映像を選ばない（制約2/3・R2）。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query courthouse --limit 96 --exclude-used --ep PD-2026-050-centralpark --json
```
`--exclude-used` は出荷ゲート `arc_nonrepeat` と同じ指紋集合を使う。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・§4.4 に pre-assign 済み）

> **★`covers_scene_id` は still 資産 ID 空間（S001..S430）を指す。** §4.4 の各エントリに pre-assign 済み（約46本が covers 付き、残りは null の繋ぎ/情景）。

| covers（例） | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S002/S018 | interrogation room ambient・cold room | `interrogation_room` / `cold_institutional_room` | 0 |
| S021/S030/S045 | 1989 NYの街/subway/abstract park | `nyc_street_night` / `subway_interior` / `park_treeline_night` | 1 |
| S101/S120/S200/S210 | institutional room/廊下・precinct interior | `institutional_corridor` / `precinct_interior` / `cold_room` | 2 |
| S211/S225/S240/S268 | NY州最高裁 columns/courthouse/courtroom | `ny_supreme_court` / `courthouse_facade` / `empty_courtroom` | 3 |
| S269/S300/S331 | prison-adjacent 外観/窓/廊下（非扇情） | `prison_exterior_dusk` / `institutional_window` / `long_corridor` | 4 |
| S332/S358/S371 | lab/records/evidence room・cold corridor | `forensic_lab` / `records_wall` / `evidence_room` | 5 |
| S372/S400/S408 | courthouse steps day/city dawn/dawn horizon | `courthouse_steps_day` / `city_dawn` / `dawn_horizon` | 6 |
| S416/S430 | interrogation room minimal・dawn edge | `empty_chair_room` / `dawn_edge` | 7 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: institutional 廊下・空の courtroom・marble columns・prison 外観・abstract loops・dust・light shaft・cityscape・sky gradient・texture pan・water reflection。**暗いクリップに偏りすぎない**（暗側は全体の1/3=約161本まで。courthouse の昼光・dawn 側も混ぜる）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）

```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.4a ★★★ 実写ストックライブラリを必ず使う（EP48/49 の burned lesson＝実写0本を潰す）★★★

> **owner directive（EP48/49 retro）:** 「せっかくたくさんダウンロードしたんだから意味のある所に使ってほしい」。EP48/49 は本編を AI still 100% ＋ AI-i2v で組み、**ダウンロード済みの実写ストックライブラリを1本も使わなかった**。本作（60分・flagship）はこれを潰す。**factory 485レーンの調達源に、既存 `H:\pd-media\assets\factory` 在庫だけでなく、下記の実写ストックライブラリを必ず含める。**

- **ストックライブラリ:** `H:\pd-media\assets\stock`（マニフェスト `H:\pd-media\assets\stock\STOCK_MANIFEST.json`・**動画 74本 ＋ 静止 155本**・pexels/pixabay・**商用可**＝上の `ALLOWED_LICENSES` の `Pexels License`/`Pixabay Content License` に既に含まれる）。
- **調達方針（★counts は固定・factory 485 / motion 85 を変えない。レーン内の調達源を広げるだけ）:**
  1. `STOCK_MANIFEST.json` を読み、**意味（§7.3 の covers カテゴリ: courthouse/NYC street/subway/precinct/prison/lab/records/protest/dawn 等）に一致し、§7.5 の全点目視 QC と R-FACE（顔・被害者・暴行・可読テキストなし）を通る実写動画クリップを優先採用**する。**目標: QC を通る限りの stock 動画 74本を factory 485 に組み込む**（無理な水増しはしない・意味の合わないクリップを差し込まない）。
  2. 残りの factory 枠を `H:\pd-media\assets\factory` 在庫で埋める。
  3. **各 factory エントリの出所（`stock` ライブラリ由来 or `factory` 在庫由来）を `05_stock/stock_ledger.v001.json`（§10.2）と `factory_selection.v001.json`（§7.6）に記録**する（B が実写の使用実態を確認できるように）。
  4. **ストック静止 155本は本編 body still（AI 430本）レーンに混ぜない**（body は 1シーン1 AI プロンプトの固定モデル・§5.5）。使う場合は **顔・可読テキストを目視で除いた face-free/text-free のもののみ**、factory/情景レーンの扱いに限る。
- **★R-FACE/R-VICTIM を絶対順守:** 実在の判事/警官/5人/Reyes/Trump/被害者が写るニュース映像・被害者/暴行/gore を含むクリップは**ストックでも使わない**（§7.5 の目視で除外）。EP39〜49 との sha256 被りゼロ（§7.7）はストック由来にも適用。
- **★カラーマッチは B が担当:** pexels/pixabay の発色バラつきは B が cold-steel-cyan の neutral グレードで AI still に合わせる（§CODEX_B 5.8(d)・**milky wash にしない**）。A は素材を素の色のまま staging（§10.1 の libx264 conform）してよい。

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★

> **推測ではなく実際に起きた事故。** EP36: `city_surveillance_camera_dome` が大聖堂。EP38: 牛が `documents_on_desk`。`subtype` は「その検索語で取った」記録であって**中身の保証ではない**。★485本は12分エピの5倍＝目視だけで4時間以上。分割して全点見る。

**選抜485本は例外なく次を経る:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-050-centralpark --media video --dir "<485本の staging フォルダ>"
#   → runs/qc/centralpark_footage_contact_NN.png（各タイルにファイル名ラベル・約25シート）
```

2. **コンタクトシートを実際に開き、485本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**（差替え）
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP50テーマ・ウォーターマークなし・識別可能な実在人物なし（R2・制約5）を確認
5. **★制約2/3の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。**被害者/暴行/泣く人/gore を含むクリップは使わない。** 実在の判事/警官/5人/Reyes/Trump の顔が写るニュース映像を使わない。**鉄格子内部の gore/独房の暴力・病院/臨床(EP44)・テキサス道/ピックアップ(EP47)・Utah 駐車場(EP49)を含むクリップを使わない。**
6. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=42.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP50 は near-black・cold-cyan・institutional が多いので暗側が本命リスク。** 平均輝度42未満が全体の40%を超えると FAIL。**暗いクリップは約161本（1/3）までに抑え、courthouse の昼光・city dawn・cold fluorescent の実用光がある本を混ぜる。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-050-centralpark/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-050-centralpark/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP49 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_centralpark_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-049-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP50 の485本の積集合が**空**であることを確認。1件でも exit 1。**EP39〜EP49 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

**分離レーン（色・素材・語）:** EP41 gold（監獄）／EP42 blue（ankle monitor）／EP43 amber（porch/救急車）／EP44 teal（病院）／EP45 crimson（暖色台所）／EP46 green／EP47 civil-violet（テキサス道/ピックアップ）／EP48 glover／EP49 somber-plum（Utah 夜の駐車場/記録の壁）。**EP50 = cold steel-cyan `#2F9FC4`（INK `#0A0A0C`）＋末端のみ dawn-amber `#C98A3C`。** これら他話の絵柄・色・被写体を1本も選ばない。

---

# 8. A-5: i2v モーション化 85本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする85本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py`（variants なし）で `M<NN>_src.png` として生成（`ai_prompts.v001.md` に §8.1a の85行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `CPK-MS01..MS85`、モーション成果物は `CPK-M01..M85`。**幕別配分は §4.5 に pre-assign 済み**（HOOK 3 / ACT1 12 / ACT2 18 / ACT3 12 / ACT4 12 / ACT5 16 / ACT6 8 / ACT7 4 = 85）。動きの意味は §4.5 の `storyboard`（§2 の Sid）と `tags` に対応。
> **★このうち 16本は §5.11 の匿名人物ビート（H001–H016・owner 承認済）＝85本の内数**（ACT1×2・ACT2×5・ACT3×6・ACT4×2・ACT6×1）。**残り 69本が抽象/象徴種。** 人物種は §8.1a の該当 `M<NN>_src.png` 行を §5.11 の H プロンプト（`[HSTYLE]`/`[HNEG]`・poised-still）で書く（新規行を足さない＝`shots=515` 維持）。**幕内の抽象種をその本数だけ減らす**（各幕の i2v 種合計は不変）。人物種の Wan NEG（§8.2）は「実在 likeness/被害者/child face closeup」を抑制したままで整合（顔は非識別＝背向き/影で作る）。

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの85行を追加・各1枚・**poised-still の source**）

> 各種プロンプトは §5.6 の対応 motif の「動く直前の poised-still」版。**動きが意味を持つ絵**（DNA ladder が draw する直前・signature が dissolve する直前・REC light が点く直前・five silhouettes が立つ直前・cold-cyan が満ちる直前 等）。末尾に §5.3 `[STYLE]` ＋ `Avoid:` §5.4 `[NEG]` を全文連結。全て顔なし・象徴・判読不能。**下記は代表8例。残り77行は §4.5 の各 storyboard/tags を「poised, still, about to move」で SDXL 化する**（例と同じ書式で M01_src..M85_src を穴なく書く）。

```
- `M01_src.png`
An empty interrogation-room chair in near-black poised and still under a single cold steel-cyan shaft of light about to find it, a steel table edge and an unlit REC lamp, no person, no face, no readable text [STYLE] Avoid: [NEG]
- `M02_src.png`
A single small red REC indicator lamp sitting unlit and dark on a camera body in a cold room, framed and still, poised for nothing to happen, the unrecorded hours, no person, no face, no readable text [STYLE] Avoid: [NEG]
- `M08_src.png`
Five child-height silhouettes at descending heights standing motionless against a cold steel-cyan haze, seen only as dark backs, poised and still before they become a group, no faces, no readable text [STYLE] Avoid: [NEG]
- `M20_src.png`
Two shadows on a cold interrogation-room wall, a taller adult shadow and a small child shadow held motionless and poised, cast shapes only, no bodies or faces, no readable text [STYLE] Avoid: [NEG]
- `M28_src.png`
Five blank confession pages stacked and leaning like a house of cards under cold steel-cyan light, held still and poised to fall, each page an unreadable smear, no person, no readable text [STYLE] Avoid: [NEG]
- `M65_src.png`
A cold steel-cyan gel-electrophoresis ladder in near-black held poised with one lane about to snap into a single aligned bright band, the DNA hinge frozen a moment before it resolves, abstract, no numerals, no people [STYLE] Avoid: [NEG]
- `M74_src.png`
A single ink signature line on a blank page held still and poised to begin dissolving into fine particles under cold light, a conviction about to be erased, the writing an unreadable smear, no person, no readable text [STYLE] Avoid: [NEG]
- `M78_src.png`
A single small red REC lamp on a camera body poised dark and about to illuminate, a first faint note of dawn-amber at the edge of a cold room, the reform a moment away, no person, no readable text [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_strieff.py` を下敷きにパスと SHOTS だけ差し替え）

```python
HOST = "http://127.0.0.1:8188"                              # ローカル ComfyUI
HIGH = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"
LOW  = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"
VAE  = "wan_2.1_vae.safetensors"       # ★2.1（2.2 ではない・無言の品質劣化の原因）
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
WIDTH, HEIGHT = 1280, 720
FRAMES = 41        # 4090 の全ロード上限@720p
STEPS = 40 / SPLIT = 20 / SHIFT = 5.0   # ★SHIFT 5.0（8.0 は 5B からの無言持ち越しでバグ）
CFG = 3.5 / SAMPLER,SCHEDULER = "euler","simple" / FPS = 16
STILL_DIR     = H:\pd-media\assets\ai\centralpark      # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\centralpark
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, child face, crying person, victim, assault, gore, blood"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely` / `assert_frame_math`。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す・★85本は複数日）

```bash
py -3.11 scripts/comfy_wan_centralpark.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_centralpark.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_centralpark.py --run-all          # 残り84本（冪等・既存スキップ）
```
1本 24–73 GPU分・85本で 35–95時間＝**複数日**。`/queue` `/history` を30秒間隔でポーリング。**夜間分割で回す。開始前にマシン状態を確認。**

## 8.4 RIFE で 48fps 化（`rife_centralpark.py`・`rife_strieff.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・身体・**被害者・暴行・泣く人・gore**が生成されていないこと（NEG で抑えているが**必ず目視**・制約2/3/5）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- five silhouettes / Korey / Reyes 影は**識別可能な顔・横顔・正面**に転じていないこと（R2・制約5）
- DNA ladder（M65系）は**可読の数字**が出ていないこと（制約2）／Trump 枠（あれば）は headline/art が出ていないこと（制約2）／REC light（M78）は点灯の動きが自然なこと
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（85本 × 2回 = 170カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど60本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **30本** | cold room dust・archive/lab dust・night air drift。黒背景 drift を screen 合成 |
| `light_assets` | **20本** | cold-cyan shaft・cold fluorescent flicker・cyan cursor glow・TV scanline・**dawn-amber edge（exoneration/close 用の少数）** |
| `vfx_overlays` | **10本** | 微細な grain・cold light noise・subtle vignette・cyan glitch min |
| **合計** | **60本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/centralpark/overlay/` に置き、`centralpark_film.json` の `cuts[].src` には**出さない**。黒背景でループするものを選び `blend_hint` を書く（§4.6 の60本に対応）。発色は B が accent `#2F9FC4`（cold steel-cyan）に寄せる想定・dawn-amber の light は close 用のみ。A は他話色（gold/blue/amber/teal/crimson/green/civil-violet/plum）を選ばない。**§7.5 の目視QC対象**（60本）。

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 40 --exclude-used --ep PD-2026-050-centralpark --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_centralpark_assets.py`）

```
remotion/public/centralpark/img/     ← role=body の静止画430枚（+ 同名 _depth.png）
remotion/public/centralpark/factory/ ← 選定 factory .mp4 485本（§4.4 の F001..F485 名で）
remotion/public/centralpark/motion/  ← i2v M<NN>_rife.mp4 85本
remotion/public/centralpark/overlay/ ← 合成レイヤー 60本（§4.6 の P/L/V 名で）
```
- `public_path` はマニフェストの値（§4.4/§4.5/§4.6）と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）
- ★~1,000 distinct assets＝**12分エピの4–5倍のディスク**を先に確保（EP38 の 50GB-copy trap 回避）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する）:**
- factory の `public_path` は必ず `centralpark/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `centralpark/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep50Centralpark"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/centralpark/` に正典を置くところまで。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_centralpark_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_centralpark_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_centralpark_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**★factory 485 / motion 85 / overlay 60 が非空で実体化しているか（不変条件16/17/18）を必ず確認。** Bのファイルを直接書き換えて知らせようとしない。

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）

```python
MAX_USES_FACTORY = 1
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
```
種別判定は**パス文字列**（`kind_of()`）: `/factory` or `af-bg-` → factory / `.mp4|.mov|.webm` or `ai_video` or `_rife` → motion / それ以外 → still。§10.1 の命名規則を守る。

EP50 の設計値: still 505/430=1.174(≤2) / factory 485/485=1.0(≤1) / motion 170/85=2.0(≤2) / first-use 1000/1160=0.8621(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）〜EP49（strieff）のファイルに一切触らない。** 読み取りのみ可。素材・色・音のレーンも分離（§7.7）。EP50 の accent は **cold steel-cyan #2F9FC4**（INK #0A0A0C・末端 dawn-amber #C98A3C・B が OP/AEカード/サムネで使用・A は絵で流用色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_centralpark_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness をどこにも作らない（R2・owner 改定）**（§1・制約5・§5.11）。特に **5人・Trisha Meili・Matias Reyes・刑事・判事・Trump を個人として似せて描かない。★匿名・非識別の一般人（H シリーズ・実在の誰にも似せない）は可**（人体そのものは禁止でない）。**被害者の描写・暴行 imagery は一切作らない（不変）。**
- **7制約に反する文言・絵をプロンプト・タグ・注記・ファイル名のどこにも作らない**（§1.2/§1.3）:
  - 5人の有罪化/関与化（制約1・R-INNOCENCE）／Armstrong を「なお有罪かも」化（制約1）／被害者の graphic 描写・likeness（制約2・R-VICTIM）／Reyes の美化/hero化（制約3・R-REYES）／hedged 数値の断定（制約4・R-NUM）／実在の顔・likeness（制約5・R-FACE）／dochighlight（制約6・R-DOCHL）／捏造引用・可読引用（制約7・R-QUOTE）／可読の confession/lab report/newspaper/citation/日付/金額/DNA数値/ロゴ／Trump ad の art/headline 再現。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 430 で担保。（★factory の subtype `_02`/`_03` は別素材の意で別物・混同しない。）
- **role=thumb / still_thumb を作らない・overlay を60本以外にしない。** サムネは also_thumb=true の body 8枚（§4.3a の集合）。
- **★factory 485 / motion 85 / overlay 60 の配列を空・stub のまま出荷しない**（EP45/EP38 の事故。§4.4/§4.5/§4.6 を必ず実体化・public_path 非空）。
- **★dochighlight figure（黒バー/box/underline）を作らない・言及しない。** A の `tags`/`caption_hint`/`notes` にも `dochighlight` という文字列を書かない（grep で 0 を保つ）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 430 / factory 485 / i2v 85 / distinct 1000 / first-use 0.8621 / still-share 0.4353 / overlay 60 / 60:00）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約1/2/3/5は目視でしか守れない）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 430 / i2v_source 85 / also_thumb 8 [§4.3a の集合] / reject N）
2. factory 選定 485本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数、
   headline/Trump枠/DNA band/prison クリップの「no readable text / no logo / no face / no victim / no gore / no ad-art」確認
3. EP39〜EP49（十一話）重複ゼロの確認結果
4. i2v 85本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー60本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）＋ factory 485/motion 85/overlay 60 が非空で実体化した確認
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック（still_body 430 / still_i2v_source 85 / motion 85 / factory 485 / overlay 60）
9. 7制約・1枚前提の自己申告（5人の有罪化/関与化なし・Armstrong 中立・被害者 graphic なし・Reyes 美化なし・
   hedged 数値の可読断定なし・実在の顔/likeness ゼロを目視確認・dochighlight 文字列ゼロ・捏造/可読引用なし・
   Trump ad art/headline 再現なし・バリエーション0・A↔B同一スキーマ
   [schema centralpark_assets.v1 / role enum body|i2v_source|reject / counts / also_thumb 集合 8 / overlay 60]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
