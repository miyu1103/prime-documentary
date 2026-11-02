# EP49 strieff — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP49_strieff_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したもので、手書きで発明していない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP49 / Episode ID: PD-2026-049-strieff / slug: strieff
Composition id: Ep49Strieff（B が Root.tsx に登録・A は staging まで）
事件:       Utah v. Strieff, 579 U.S. 232 (2016)。docket 14-1373。決定 2016-06-20。
            匿名通報の家を約1週間断続監視した刑事が、家から出た男を駐車場で停止した。
            ★その停止は【違法】だった。州は合理的疑いが無かったと CONCEDE し、最高裁もそれを前提にした。
            停止中のID照会で先在する小さな交通違反の逮捕状が判明→逮捕→逮捕に伴う捜索で
            少量のメタンフェタミン発見。証拠は【許容】された。
            ★主題は「停止が合法だったから」ではない。「先在する有効な令状が違法な停止と発見の因果を
            attenuate（希釈・遮断）したから証拠が残った」という一点。排除法則は【廃止でなく狭められた】。
            票決 5-3（Scalia 死去で空席・8名構成）。Thomas 法廷意見。Sotomayor と Kagan が反対。
            Edward Strieff は存命の私人（本件後に薬物有罪）＝顔・身体・肖像を出さない・象徴のみ・薬物は臨床最小限。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**85本の固有プロンプト × 1枚 = 85枚**・バリエーション0） | `H:\pd-media\assets\ai\strieff\S<NN>.png` | 2–3.5時間（GPU） |
| A-1b | i2v 種画像の生成（**16本の固有プロンプト × 1枚 = 16枚**・バリエーション0） | `H:\pd-media\assets\ai\strieff\M<NN>_src.png` | 30–50分（GPU） |
| A-2 | 静止画のQCと目視（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\strieff\S<NN>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **93本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2.5時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\strieff\M<NN>_rife.mp4` | 7–19時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **12本** | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/strieff/{img,factory,motion,overlay}/` | 30分 |

> **★★ 最重要の前提（EP42–48 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 85本＝85行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **`--variants 1`** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 85 + i2v 種 16 = 101枚（各1回）。** factory 93本は生成でなく在庫からの選抜。
> **★`--only S01` のログで `shots=101` を確認**してから本番を回す（85 body + 16 i2v種 = 101）。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-049-strieff/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 93 エントリ、`motion` 配列は 16 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5 に全 93 + 16 を列挙済み。build スクリプトはこの列挙を消費するだけで、空配列を書かない）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\strieff\**` / `H:\pd-media\assets\ai_video\strieff\**` | **A** | 読み書き |
| `episodes/PD-2026-049-strieff/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-049-strieff/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/strieff/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-049-strieff/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_strieff_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-048-*/**` および EP39〜48 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-049-strieff --variants 1` / `49 --variants 1 --only S01` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/strieff"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-049-strieff --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 96 --exclude-used --ep PD-2026-049-strieff --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-049-strieff` |

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・実在確認済み） |
|---|---|---|
| `scripts/qc_strieff_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_atwater_stills.py`（EP47） |
| `scripts/select_strieff_factory.py` | §7 の factory 93本の確定選定・EP39〜48 sha256 除外検証 | `scripts/select_atwater_factory.py`（EP47） |
| `scripts/comfy_wan_strieff.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_atwater.py`（EP47・実在確認） |
| `scripts/rife_strieff.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_atwater.py`（実在確認） |
| `scripts/build_strieff_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_atwater_asset_manifest.py`（EP47） |
| `scripts/stage_strieff_assets.py` | §10 の staging | `scripts/stage_atwater_assets.py`（EP47） |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.2 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_strieff_facts.py`（B が実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の6制約に一致し、`check_strieff_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_strieff_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==93 / motion 配列長==16 が非空で実体化していること（EP45 事故回避の必須不変条件）

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_strieff_asset_manifest.py --reuse-feasibility
#   → still >=85 / motion >=16 / factory >=93 / distinct 合計 >=194 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_strieff_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全93本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-049-strieff
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39〜EP48 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_strieff_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39・EP40・EP41・EP42・EP43・EP44・EP45・EP46・EP47・EP48 の十すべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1 ＋ 正確性6制約）★★★

**その停止は【違法】だった。州が合理的疑いの不在を CONCEDE し、最高裁もそれを前提にした。本作は停止を「合法(legal / lawful / constitutional / justified)」とは決して言わない。証拠が残ったのは「合憲な停止だったから」ではなく、【先在する有効な令状が違法な停止と発見の因果を attenuate（希釈・遮断）したから】という一点のみ。排除法則は【廃止(abolished)】でなく【狭められた(narrowed)】。attenuation は3要素（Brown v. Illinois）で判断され、①時間的近接（数分＝抑制寄り＝州が負け）②介在事情＝先在する有効な令状（多数の決め手・鎖を断つ）③警察の違法の目的/悪質性＝flagrancy（最高裁は「せいぜい過失、悪質でない」＝州寄り）で②③が①を上回った。票決 5-3。Scalia 死去で空席＝8名構成。Thomas 法廷意見。Sotomayor と Kagan が反対で、逐語引用は反対意見に中立帰属する。Edward Strieff は存命の私人で、顔・身体・肖像を一切出さない。象徴オブジェのみ。薬物（メタンフェタミン）は臨床的に最小限で、扇情化・美化しない。捏造引用禁止。**

## 1.1 R1（生成ビジュアル全般）

1. **実在人物の顔・likeness・肖像を作らない。** Edward Strieff（存命私人）、Detective Fackrell、Thomas・Sotomayor・Kagan・Ginsburg・Breyer・Alito・Roberts・Kennedy・Scalia を**顔・身体・肖像として描かない**。人物は原則出さない（象徴オブジェ・後ろ姿・手元・影のみ）。判事評言の逐語引用は AE カード（B の担当）であって画像ではない。
2. **実在の判決文・判例番号・条文・日付・令状の可読文字を再現しない。** 令状・免許証/IDカード・データベース画面・意見書・条文ページ・カレンダーは雰囲気のみ（判読不能）。判例番号（579 U.S. 232 / docket 14-1373）・日付（2016 / 2016-06-20 / 2006）・票決（5-3）は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。会社/州/警察のロゴは**ぼかして判読不能**にする。
3. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性6制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **停止を「合法(legal / lawful / constitutional / justified / valid)」と書かない。** 停止は違法。証拠が残った理由は "attenuation" の一点。**"the stop was legal / lawful / constitutional / justified", "the search was constitutional because the stop was fine" を書かない。** 許容は "the stop was illegal / unlawful", "the State conceded", "no reasonable suspicion", "the warrant broke the chain", "attenuated", "the evidence stayed / was admissible"。
2. **排除法則を「廃止(abolished / eliminated / struck down / repealed / dead / gone)」と書かない。** 正しくは "narrowed", "an exception", "the attenuation exception"。排除法則＝通常は違法な停止の証拠を排除（fruit of the poisonous tree）。attenuation はその例外。**"the exclusionary rule was abolished / is dead / no longer exists" を書かない。**
3. **attenuation 3要素を正確に。** ①時間的近接（数分＝抑制寄り＝州が負けた要素）②介在事情＝先在する有効な令状（多数の決め手）③目的/flagrancy（過失止まり＝州寄り）。②③が①を上回った。**「令状が停止を合法化した」と描かない**（令状は停止を合法化していない・鎖を断っただけ）。
4. **票決 5-3**（Thomas 多数＝Roberts・Kennedy・Breyer・Alito／Sotomayor 反対[Ginsburg が I-III 同調・Part IV は単独]／Kagan 反対[Ginsburg 同調]）。**Scalia 死去で空席＝8名。**画像に数字を描かない（象徴の光点で表す）。**"6-3" と書かない（誤り）。**
5. **Edward Strieff は存命の私人。顔・肖像・身体を描かない・象徴のみ・後ろ姿/手元/影のみ。** 薬物（メタンフェタミン）は臨床的に最小限（小さな無地の証拠袋・中身は見せない/抽象）。**薬物を扇情化・美化しない。** 捏造引用禁止。
6. **数値・引用は原典一致。** Sotomayor "carceral state" 逐語（"...you are not a citizen of a democracy but the subject of a carceral state, just waiting to be cataloged."）＋ "anyone's dignity can be violated in this manner" ＋ Kagan 逐語（"The officer's incentive to violate the Constitution thus increases..."）は AE カード（B）。**★"we are all harmed" は逐語でない＝どこにも書かない/引用しない。** confidence:medium（Fackrell 名・監視期間・2006年・手続経緯）はヘッジ／画面に断定で出さない。数値はどれも画像に可読で描かない（AE/figures＝B）。

## 1.3 機械ゲート（`build_strieff_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (edward |)?strieff|"
    r"face of (fackrell|thomas|sotomayor|kagan|ginsburg|breyer|alito|roberts|kennedy|scalia)|"
    r"recognizable (real )?person|identifiable face|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"the stop (was|is|were)\s*(legal|lawful|constitutional|valid|justified|proper|permitted)|"
    r"(a |the )(legal|lawful|constitutional|valid|justified) stop|"
    r"exclusionary rule\s*(was|is|were|had been)?\s*(abolished|eliminated|struck down|repealed|overturned|ended|dead|gone|no longer exists)|"
    r"(court|scotus|supreme court|justices?) (abolished|eliminated|repealed|struck down|ended) the exclusionary rule|"
    r"strieff (won|prevailed|beat the|defeated)|"
    r"we are all harmed|"
    r"(glamou?ri[sz]ed|celebratory|appealing|enticing) (drug|drugs|narcotics|meth)|"
    r"(crying|sobbing|screaming|terrified) (person|man|woman|child)|"
    r"poverty ?porn",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1・2・4・5・6を機械化したもの。プロンプト・タグ・`caption_hint`・注記のどこにも該当語を書かない。**"the stop was illegal / unlawful" / "the State conceded" / "no reasonable suspicion" / "the warrant broke the chain" / "attenuated" / "the evidence stayed" / "narrowed" / "an exception" は許容。** 禁止は「停止の合法化」・「排除法則の廃止化」・「Strieff が勝った」・「we are all harmed」・薬物の扇情/美化・人の扇情だけ。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP49_strieff_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,139
narration_seconds    = 720.6   （= 12.0分・[SILENCE 1..] の実音無音を含む）
wpm_used             = 178.1
mean_shot            = 3.19秒/カット（SPEC 3.19）・max_shot 6.0
視覚シーン(narrative)  = 48（S01..S48・SPEC derive）
Act 構成（SPEC 秒）: HOOK 65.7 / OPENING 59.6 / ACT1 131.0（最短・最速）/ ACT2 129.0 / ACT3 186.3（最長・最も荘厳）/ ENDING 120.9
```

**Aにとっての意味は1つ:** > **総カット 226 / distinct 194 / 初出 85.84% = still 85 + factory 93 + motion 16。**（§3 で積算）

> **注意（命名差）:** SPEC の視覚シーンは S01..S48。しかし **still は 85 本の固有プロンプトを持つ**ため、still の資産 ID は **S01..S85**（1プロンプト＝1枚）で採番する。48 の narrative シーンに 85 枚を配分する（ドクトリン核の ACT3 が最も厚い）。**still 資産 ID（S01..S85）と narrative シーンコード（S01..S48）は別物。** `covers_scene_id` は still 資産 ID 空間を指す（§7.3）。

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **85枚** | 101カット | 1.19回(≤2) | **85本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **93本** | 93カット | **各1回(1)** | 在庫 11,000本超から選抜（§7）・全点目視・EP39〜48 と sha256 被りゼロ |
| **i2v モーション** | **16本** | 32カット | 各2回(≤2) | 16本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **194点** | **226カット** | | |
| 合成レイヤー（particle/light/vfx） | 12本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の生成バッチ（本編カットに出ない i2v 種を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **85枚** | 85プロンプト × 1枚（バリエーション0） |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **16枚** | 16種プロンプト × 1枚（バリエーション0） |
| **SDXL 生成バッチ合計** | **85 + 16 = 101枚（各1回）** | **`--variants 1`** |

> **サムネは新規生成しない。** 完成後に body 85枚から6枚を `also_thumb:true` で流用選抜（追加生成ゼロ＝1シーン1枚前提を崩さない）。**role=thumb / still_thumb を作らない。**

> **★紙芝居回避（EP40 の最大の失敗）:** **still-cut 101 / (factory 93 + i2v 32)=video 125** で **still-share 44.69% ≤45%・motion coverage 55.31% ≥45%** を構造的に保証する（§3.3）。**stillを増やしてfactoryを削るな。factory 93 が still-share≤0.45 を守る下限。**

## 3.2 still 85枚・factory 93本・i2v 16本の幕別配分（目安・非拘束。合計だけが確定）

| 区間 | still（S番号） | factory | i2v |
|---|---|---|---|
| HOOK | 5（S01–S05） | 6 | 2（M01,M02） |
| OPENING | 3（S06–S08） | 3 | 0 |
| ACT1「その停止」（最短） | 14（S09–S22） | 12 | 4（M03,M04,M05,M06） |
| ACT2「排除法則と例外」 | 20（S23–S42） | 16 | 3（M07,M08,M09） |
| ACT3「5-3と反対」（判例核） | 28（S43–S70） | 24 | 4（M10,M11,M12,M13） |
| ENDING | 15（S71–S85） | 12 | 3（M14,M15,M16） |
| 繋ぎ（covers_scene_id:null） | — | 20 | — |
| **合計** | **85** | **93** | **16** |

> ACT3 は判例核（最も遅く荘厳）なので still も最多の28枚。**幕別の factory/i2v 内訳は非拘束の目安値**（合計 93 / 16 のみ確定）。ゲートは factory を各1回・合計 93 でしか見ない。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 226 = still 101 + factory 93 + i2v 32
[2] 平均ショット長 = narration 720.6 / 226 = 3.188秒/カット  ✓ (SPEC mean_shot 3.19・≤6.0)
[3] 静止画占有率(check_animation_mix) = 101/226 = 44.69%  ✓ ≤45%（SPEC still_share 0.4469・余裕0.31%）
[4] motion coverage = (93+32)/226 = 125/226 = 55.31%     ✓ ≥45%
[5] per-asset 上限: still 101/85=1.19(≤2) / factory 93/93=1.0(≤1) / motion 32/16=2.0(≤2)  ✓
[6] first-use share = 194/226 = 0.8584                   ✓ ≥0.70（SPEC 一致）
[7] factory 下限: i2v 32 は固定なので factory は 93 を下回れない（93+32=125=video）。→ factory 93 は下限であり水増しではない。
```

> **[3] の余裕は 0.31% しかない。** still が85本を割ったら §6.3 の再生成で回復させ、**still-cut 101 を増やさない**（B側の shotlist が101で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-049-strieff/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `strieff_assets.v1`（固定文字列）
**生産者:** `scripts/build_strieff_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を一字一致。** role enum は **`body | i2v_source | reject` のみ**（`thumb`/`still_thumb` を作らない）。サムネは `also_thumb:true` の body still **ちょうど6枚**。overlay は **ちょうど12本**。

## 4.1 スキーマ（`strieff_assets.v1`）

```jsonc
{
  "schema_version": "strieff_assets.v1",
  "episode_id": "PD-2026-049-strieff",
  "slug": "strieff",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_strieff_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 85,          // ==85
    "still_i2v_source": 16,    // ==16
    "motion": 16,              // ==16
    "factory": 93,             // ==93
    "overlay": 12              // ==12（distinct 素材に数えない）
  },
  "stills":  [ /* §4.3: body 85 (STRF-S01..S85) + i2v_source 16 (STRF-MS01..MS16) */ ],
  "motion":  [ /* §4.5: STRF-M01..M16 全16本・public_path 必須（★非空） */ ],
  "factory": [ /* §4.4: 93本・public_path 必須（★非空・EP45事故回避の核心） */ ],
  "overlay": [ /* §4.6: 12本 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例）

```jsonc
{
  "asset_id": "STRF-S01",                 // body: ^STRF-S\d{2}$（01..85） / i2v種: ^STRF-MS\d{2}$
  "scene_id": "S01",                      // still 資産 ID 空間（§5.9 のプロンプト行に対応・S01..S85）
  "role": "body",                         // body|i2v_source|reject（各1枚・バリエーション概念なし）
  "also_thumb": false,                    // body から6枚だけ true（§4.3・追加生成しない）
  "act": 0,                               // 0=HOOK/OPENING, 1=ACT1, 2=ACT2, 3=ACT3, 5=ENDING
  "path": "H:/pd-media/assets/ai/strieff/S01.png",
  "depth_path": "H:/pd-media/assets/ai/strieff/S01_depth.png",   // role=="body" は実在必須
  "public_path": "strieff/img/S01.png",   // role=="body" のみ非null
  "width": 3840, "height": 2160,          // 長辺>=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 34.8,
  "tags": ["front_door","night","figure_back","symbolic"],
  "caption_hint": "a modest Utah house front door opening at night, a figure's back stepping out, no face",
  "seed": 0, "model": "juggernautXL_ragnarokBy",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
         "has_identifiable_face": false, "has_human_body": false, "notes": ""}
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="strieff_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 85 / i2v_source 16 / motion 16 / factory 93 / overlay 12）に**一致**
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（i2v_source は `^STRF-MS\d{2}$`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39・EP40・EP41・EP42・EP43・EP44・EP45・EP46・EP47・EP48 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど6**、かつ **`scene_id` 集合が `{S12,S43,S45,S46,S57,S62}`（§4.3）と完全一致**（body からの流用。**この集合は CODEX_B と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど12**
17. ★**`factory` 配列長==93 かつ全エントリ `public_path` が非空**（EP45 事故回避・空配列/stub を許さない）
18. ★**`motion` 配列長==16 かつ全エントリ `public_path` が非空**（同上）

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 85枚（S01..S85）= §5.9 の85プロンプトの生成物。各1枚。
2. i2v_source 16枚（MS01..MS16 / 種画像 M01_src..M16_src）= §8.1a の16種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち S12 / S43 / S45 / S46 / S57 / S62 の6枚に true（追加生成しない）
     （the stop=S12・SCOTUS=S43・Scalia空席=S45・5-3光点=S46・断ち切られた鎖=S57・パトカーのライト=S62）
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

## 4.4 ★`factory[]` 全93エントリ（★必ず実体化・public_path 非空。EP45事故回避の核心）

> `select_strieff_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id）/`path`（`H:/pd-media/assets/factory/...`）/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。** 各 public_path は `strieff/factory/F0NN_<subtype>.mp4`。`type:"backgrounds"`, `kind:"video"`。covers は still 資産 ID 空間（§7.3）。

```jsonc
// HOOK (act 0) — 6本
{ "public_path":"strieff/factory/F001_suburban_house_night.mp4",       "act":0, "covers_scene_id":"S09",  "subtype":"suburban_house_night" },
{ "public_path":"strieff/factory/F002_quiet_residential_street_night.mp4","act":0,"covers_scene_id":null,  "subtype":"quiet_residential_street_night" },
{ "public_path":"strieff/factory/F003_bare_parking_lot_night.mp4",     "act":0, "covers_scene_id":"S11",  "subtype":"bare_parking_lot_night" },
{ "public_path":"strieff/factory/F004_unmarked_car_across_lot_night.mp4","act":0,"covers_scene_id":null,  "subtype":"unmarked_car_across_lot_night" },
{ "public_path":"strieff/factory/F005_sodium_streetlight_night.mp4",   "act":0, "covers_scene_id":null,   "subtype":"sodium_streetlight_night" },
{ "public_path":"strieff/factory/F006_dark_front_step_night.mp4",      "act":0, "covers_scene_id":null,   "subtype":"dark_front_step_night" },
// OPENING (act 0) — 3本
{ "public_path":"strieff/factory/F007_courthouse_marble_facade_night.mp4","act":0,"covers_scene_id":"S06","subtype":"courthouse_marble_facade_night" },
{ "public_path":"strieff/factory/F008_supreme_court_columns_night.mp4","act":0, "covers_scene_id":"S07",  "subtype":"supreme_court_columns_night" },
{ "public_path":"strieff/factory/F009_marble_corridor_cold_night.mp4", "act":0, "covers_scene_id":null,   "subtype":"marble_corridor_cold_night" },
// ACT1 (act 1) — 12本
{ "public_path":"strieff/factory/F010_residential_night_road.mp4",     "act":1, "covers_scene_id":null,   "subtype":"residential_night_road" },
{ "public_path":"strieff/factory/F011_parking_lot_sodium_night.mp4",   "act":1, "covers_scene_id":null,   "subtype":"parking_lot_sodium_night" },
{ "public_path":"strieff/factory/F012_dispatch_console_glow.mp4",      "act":1, "covers_scene_id":null,   "subtype":"dispatch_console_glow" },
{ "public_path":"strieff/factory/F013_police_station_exterior_night.mp4","act":1,"covers_scene_id":"S21", "subtype":"police_station_exterior_night" },
{ "public_path":"strieff/factory/F014_unmarked_detective_car_curb.mp4","act":1, "covers_scene_id":null,   "subtype":"unmarked_detective_car_curb" },
{ "public_path":"strieff/factory/F015_dark_driveway_night.mp4",        "act":1, "covers_scene_id":null,   "subtype":"dark_driveway_night" },
{ "public_path":"strieff/factory/F016_empty_sidewalk_night.mp4",       "act":1, "covers_scene_id":"S63",  "subtype":"empty_sidewalk_night" },
{ "public_path":"strieff/factory/F017_street_corner_streetlight.mp4",  "act":1, "covers_scene_id":null,   "subtype":"street_corner_streetlight" },
{ "public_path":"strieff/factory/F018_utah_suburb_dusk.mp4",           "act":1, "covers_scene_id":null,   "subtype":"utah_suburb_dusk" },
{ "public_path":"strieff/factory/F019_cold_night_road_wide.mp4",       "act":1, "covers_scene_id":null,   "subtype":"cold_night_road_wide" },
{ "public_path":"strieff/factory/F020_patrol_car_parked_night.mp4",    "act":1, "covers_scene_id":null,   "subtype":"patrol_car_parked_night" },
{ "public_path":"strieff/factory/F021_night_intersection_quiet.mp4",   "act":1, "covers_scene_id":null,   "subtype":"night_intersection_quiet" },
// ACT2 (act 2) — 16本
{ "public_path":"strieff/factory/F022_state_courthouse_corridor.mp4",  "act":2, "covers_scene_id":"S22",  "subtype":"state_courthouse_corridor" },
{ "public_path":"strieff/factory/F023_empty_courtroom_cold.mp4",       "act":2, "covers_scene_id":null,   "subtype":"empty_courtroom_cold" },
{ "public_path":"strieff/factory/F024_long_courthouse_hallway.mp4",    "act":2, "covers_scene_id":"S40",  "subtype":"long_courthouse_hallway" },
{ "public_path":"strieff/factory/F025_marble_stairs_cold.mp4",         "act":2, "covers_scene_id":null,   "subtype":"marble_stairs_cold" },
{ "public_path":"strieff/factory/F026_federal_courthouse_exterior_dusk.mp4","act":2,"covers_scene_id":"S42","subtype":"federal_courthouse_exterior_dusk" },
{ "public_path":"strieff/factory/F027_courtroom_bench_empty.mp4",      "act":2, "covers_scene_id":null,   "subtype":"courtroom_bench_empty" },
{ "public_path":"strieff/factory/F028_law_library_shelves.mp4",        "act":2, "covers_scene_id":null,   "subtype":"law_library_shelves" },
{ "public_path":"strieff/factory/F029_marble_floor_reflection.mp4",    "act":2, "covers_scene_id":null,   "subtype":"marble_floor_reflection" },
{ "public_path":"strieff/factory/F030_clerk_office_cold.mp4",          "act":2, "covers_scene_id":null,   "subtype":"clerk_office_cold" },
{ "public_path":"strieff/factory/F031_records_room_shelves.mp4",       "act":2, "covers_scene_id":null,   "subtype":"records_room_shelves" },
{ "public_path":"strieff/factory/F032_archive_drawers_cold.mp4",       "act":2, "covers_scene_id":null,   "subtype":"archive_drawers_cold" },
{ "public_path":"strieff/factory/F033_courthouse_columns_day.mp4",     "act":2, "covers_scene_id":null,   "subtype":"courthouse_columns_day" },
{ "public_path":"strieff/factory/F034_marble_wall_shadow.mp4",         "act":2, "covers_scene_id":null,   "subtype":"marble_wall_shadow" },
{ "public_path":"strieff/factory/F035_office_corridor_fluorescent.mp4","act":2, "covers_scene_id":null,   "subtype":"office_corridor_fluorescent" },
{ "public_path":"strieff/factory/F036_evidence_locker_shelves.mp4",    "act":2, "covers_scene_id":null,   "subtype":"evidence_locker_shelves" },
{ "public_path":"strieff/factory/F037_dark_road_night_wide.mp4",       "act":2, "covers_scene_id":null,   "subtype":"dark_road_night_wide" },
// ACT3 (act 3) — 24本
{ "public_path":"strieff/factory/F038_supreme_court_facade_night.mp4", "act":3, "covers_scene_id":"S43",  "subtype":"supreme_court_facade_night" },
{ "public_path":"strieff/factory/F039_supreme_court_steps_night.mp4",  "act":3, "covers_scene_id":null,   "subtype":"supreme_court_steps_night" },
{ "public_path":"strieff/factory/F040_marble_colonnade_night.mp4",     "act":3, "covers_scene_id":"S59",  "subtype":"marble_colonnade_night" },
{ "public_path":"strieff/factory/F041_supreme_court_facade_day.mp4",   "act":3, "covers_scene_id":null,   "subtype":"supreme_court_facade_day" },
{ "public_path":"strieff/factory/F042_marble_hallway_grand.mp4",       "act":3, "covers_scene_id":null,   "subtype":"marble_hallway_grand" },
{ "public_path":"strieff/factory/F043_law_volumes_old_shelf.mp4",      "act":3, "covers_scene_id":null,   "subtype":"law_volumes_old_shelf" },
{ "public_path":"strieff/factory/F044_courtroom_grand_empty.mp4",      "act":3, "covers_scene_id":null,   "subtype":"courtroom_grand_empty" },
{ "public_path":"strieff/factory/F045_marble_columns_light.mp4",       "act":3, "covers_scene_id":null,   "subtype":"marble_columns_light" },
{ "public_path":"strieff/factory/F046_capitol_dome_dusk.mp4",         "act":3, "covers_scene_id":null,   "subtype":"capitol_dome_dusk" },
{ "public_path":"strieff/factory/F047_rotunda_cold_marble.mp4",       "act":3, "covers_scene_id":null,   "subtype":"rotunda_cold_marble" },
{ "public_path":"strieff/factory/F048_marble_bench_curved.mp4",        "act":3, "covers_scene_id":null,   "subtype":"marble_bench_curved" },
{ "public_path":"strieff/factory/F049_courthouse_dome_night.mp4",      "act":3, "covers_scene_id":null,   "subtype":"courthouse_dome_night" },
{ "public_path":"strieff/factory/F050_marble_wall_engraving_light.mp4","act":3, "covers_scene_id":null,   "subtype":"marble_wall_engraving_light" },
{ "public_path":"strieff/factory/F051_grand_staircase_marble.mp4",     "act":3, "covers_scene_id":null,   "subtype":"grand_staircase_marble" },
{ "public_path":"strieff/factory/F052_archive_record_wall_deep.mp4",   "act":3, "covers_scene_id":null,   "subtype":"archive_record_wall_deep" },
{ "public_path":"strieff/factory/F053_file_shelves_receding.mp4",      "act":3, "covers_scene_id":null,   "subtype":"file_shelves_receding" },
{ "public_path":"strieff/factory/F054_marble_pillar_detail.mp4",       "act":3, "covers_scene_id":null,   "subtype":"marble_pillar_detail" },
{ "public_path":"strieff/factory/F055_supreme_court_plaza_night.mp4",  "act":3, "covers_scene_id":null,   "subtype":"supreme_court_plaza_night" },
{ "public_path":"strieff/factory/F056_government_building_dusk.mp4",   "act":3, "covers_scene_id":null,   "subtype":"government_building_dusk" },
{ "public_path":"strieff/factory/F057_marble_corridor_deep.mp4",       "act":3, "covers_scene_id":null,   "subtype":"marble_corridor_deep" },
{ "public_path":"strieff/factory/F058_courthouse_interior_cold.mp4",   "act":3, "covers_scene_id":null,   "subtype":"courthouse_interior_cold" },
{ "public_path":"strieff/factory/F059_records_wall_endless.mp4",       "act":3, "covers_scene_id":"S78",  "subtype":"records_wall_endless" },
{ "public_path":"strieff/factory/F060_flag_pole_dusk_generic.mp4",     "act":3, "covers_scene_id":null,   "subtype":"flag_pole_dusk_generic" },
{ "public_path":"strieff/factory/F061_marble_engraving_shadow.mp4",    "act":3, "covers_scene_id":null,   "subtype":"marble_engraving_shadow" },
// ENDING (act 5) — 12本
{ "public_path":"strieff/factory/F062_parking_lot_night_empty.mp4",    "act":5, "covers_scene_id":"S71",  "subtype":"parking_lot_night_empty" },
{ "public_path":"strieff/factory/F063_residential_street_night_receding.mp4","act":5,"covers_scene_id":null,"subtype":"residential_street_night_receding" },
{ "public_path":"strieff/factory/F064_night_road_horizon_plum.mp4",    "act":5, "covers_scene_id":null,   "subtype":"night_road_horizon_plum" },
{ "public_path":"strieff/factory/F065_quiet_suburb_predawn.mp4",       "act":5, "covers_scene_id":null,   "subtype":"quiet_suburb_predawn" },
{ "public_path":"strieff/factory/F066_empty_sidewalk_dawn.mp4",        "act":5, "covers_scene_id":null,   "subtype":"empty_sidewalk_dawn" },
{ "public_path":"strieff/factory/F067_records_wall_warm_low.mp4",      "act":5, "covers_scene_id":null,   "subtype":"records_wall_warm_low" },
{ "public_path":"strieff/factory/F068_marble_shelf_light.mp4",        "act":5, "covers_scene_id":null,   "subtype":"marble_shelf_light" },
{ "public_path":"strieff/factory/F069_road_vanishing_point_night.mp4", "act":5, "covers_scene_id":null,   "subtype":"road_vanishing_point_night" },
{ "public_path":"strieff/factory/F070_dark_sky_open_plum.mp4",        "act":5, "covers_scene_id":null,   "subtype":"dark_sky_open_plum" },
{ "public_path":"strieff/factory/F071_corridor_door_light.mp4",       "act":5, "covers_scene_id":null,   "subtype":"corridor_door_light" },
{ "public_path":"strieff/factory/F072_street_evening_wide.mp4",       "act":5, "covers_scene_id":null,   "subtype":"street_evening_wide" },
{ "public_path":"strieff/factory/F073_parking_lot_dusk_receding.mp4",  "act":5, "covers_scene_id":null,   "subtype":"parking_lot_dusk_receding" },
// 繋ぎ connective (covers null) — 20本
{ "public_path":"strieff/factory/F074_marble_light_shaft.mp4",        "act":3, "covers_scene_id":null,   "subtype":"marble_light_shaft" },
{ "public_path":"strieff/factory/F075_dust_in_light_bg.mp4",         "act":3, "covers_scene_id":null,   "subtype":"dust_in_light_bg" },
{ "public_path":"strieff/factory/F076_rain_asphalt_night.mp4",        "act":1, "covers_scene_id":null,   "subtype":"rain_asphalt_night" },
{ "public_path":"strieff/factory/F077_headlights_road_night.mp4",     "act":1, "covers_scene_id":null,   "subtype":"headlights_road_night" },
{ "public_path":"strieff/factory/F078_cloud_timelapse_night.mp4",     "act":0, "covers_scene_id":null,   "subtype":"cloud_timelapse_night" },
{ "public_path":"strieff/factory/F079_dark_field_wind.mp4",          "act":2, "covers_scene_id":null,   "subtype":"dark_field_wind" },
{ "public_path":"strieff/factory/F080_empty_parking_lot_dusk.mp4",    "act":2, "covers_scene_id":null,   "subtype":"empty_parking_lot_dusk" },
{ "public_path":"strieff/factory/F081_flag_texture_generic.mp4",      "act":2, "covers_scene_id":null,   "subtype":"flag_texture_generic" },
{ "public_path":"strieff/factory/F082_marble_texture_pan.mp4",        "act":2, "covers_scene_id":null,   "subtype":"marble_texture_pan" },
{ "public_path":"strieff/factory/F083_road_lines_passing_night.mp4",  "act":1, "covers_scene_id":null,   "subtype":"road_lines_passing_night" },
{ "public_path":"strieff/factory/F084_fluorescent_ceiling_pan.mp4",   "act":2, "covers_scene_id":null,   "subtype":"fluorescent_ceiling_pan" },
{ "public_path":"strieff/factory/F085_courthouse_window_light.mp4",   "act":3, "covers_scene_id":null,   "subtype":"courthouse_window_light" },
{ "public_path":"strieff/factory/F086_dusk_treeline.mp4",            "act":3, "covers_scene_id":null,   "subtype":"dusk_treeline" },
{ "public_path":"strieff/factory/F087_water_reflection_night.mp4",    "act":3, "covers_scene_id":null,   "subtype":"water_reflection_night" },
{ "public_path":"strieff/factory/F088_asphalt_wet_reflection.mp4",    "act":3, "covers_scene_id":null,   "subtype":"asphalt_wet_reflection" },
{ "public_path":"strieff/factory/F089_marble_floor_reflection_deep.mp4","act":3,"covers_scene_id":null,  "subtype":"marble_floor_reflection_deep" },
{ "public_path":"strieff/factory/F090_night_sky_gradient_plum.mp4",   "act":5, "covers_scene_id":null,   "subtype":"night_sky_gradient_plum" },
{ "public_path":"strieff/factory/F091_road_shoulder_gravel_night.mp4","act":5, "covers_scene_id":null,   "subtype":"road_shoulder_gravel_night" },
{ "public_path":"strieff/factory/F092_horizon_line_dusk_plum.mp4",    "act":5, "covers_scene_id":null,   "subtype":"horizon_line_dusk_plum" },
{ "public_path":"strieff/factory/F093_server_records_glow_bg.mp4",    "act":2, "covers_scene_id":null,   "subtype":"server_records_glow_bg" }
```

**内訳検算:** HOOK 6 + OPENING 3 + ACT1 12 + ACT2 16 + ACT3 24 + ENDING 12 + 繋ぎ 20 = **93** ✓。全 `public_path` 非空 ✓（不変条件17）。

## 4.5 ★`motion[]` 全16エントリ（★必ず実体化・public_path 非空）

> エントリ形は §4.1a 準拠 + 動画フィールド。`asset_id ^STRF-M\d{2}$`。`source_still` は §8.1a の種画像、`source_scene_id`=`MS<NN>`。runtime で `sha256`/`width 1280`/`height 720`/`fps 48`/`frames`/`duration_sec`/`qc` を埋める（§8.4）。**空配列を書かない。**

```jsonc
{ "asset_id":"STRF-M01","source_scene_id":"MS01","source_still":"H:/pd-media/assets/ai/strieff/M01_src.png","path":"H:/pd-media/assets/ai_video/strieff/M01_rife.mp4","public_path":"strieff/motion/M01_rife.mp4","act":0, "tags":["front_door","figure_back"] },
{ "asset_id":"STRF-M02","source_scene_id":"MS02","source_still":"H:/pd-media/assets/ai/strieff/M02_src.png","path":"H:/pd-media/assets/ai_video/strieff/M02_rife.mp4","public_path":"strieff/motion/M02_rife.mp4","act":0, "tags":["parking_lot","patrol_lights"] },
{ "asset_id":"STRF-M03","source_scene_id":"MS03","source_still":"H:/pd-media/assets/ai/strieff/M03_src.png","path":"H:/pd-media/assets/ai_video/strieff/M03_rife.mp4","public_path":"strieff/motion/M03_rife.mp4","act":1, "tags":["id_card","flashlight"] },
{ "asset_id":"STRF-M04","source_scene_id":"MS04","source_still":"H:/pd-media/assets/ai/strieff/M04_src.png","path":"H:/pd-media/assets/ai_video/strieff/M04_rife.mp4","public_path":"strieff/motion/M04_rife.mp4","act":1, "tags":["radio","dispatch"] },
{ "asset_id":"STRF-M05","source_scene_id":"MS05","source_still":"H:/pd-media/assets/ai/strieff/M05_src.png","path":"H:/pd-media/assets/ai_video/strieff/M05_rife.mp4","public_path":"strieff/motion/M05_rife.mp4","act":1, "tags":["database","warrant_flag"] },
{ "asset_id":"STRF-M06","source_scene_id":"MS06","source_still":"H:/pd-media/assets/ai/strieff/M06_src.png","path":"H:/pd-media/assets/ai_video/strieff/M06_rife.mp4","public_path":"strieff/motion/M06_rife.mp4","act":1, "tags":["handcuffs","closing"] },
{ "asset_id":"STRF-M07","source_scene_id":"MS07","source_still":"H:/pd-media/assets/ai/strieff/M07_src.png","path":"H:/pd-media/assets/ai_video/strieff/M07_rife.mp4","public_path":"strieff/motion/M07_rife.mp4","act":2, "tags":["poisonous_tree","fruit"] },
{ "asset_id":"STRF-M08","source_scene_id":"MS08","source_still":"H:/pd-media/assets/ai/strieff/M08_src.png","path":"H:/pd-media/assets/ai_video/strieff/M08_rife.mp4","public_path":"strieff/motion/M08_rife.mp4","act":2, "tags":["chain","weak_link"] },
{ "asset_id":"STRF-M09","source_scene_id":"MS09","source_still":"H:/pd-media/assets/ai/strieff/M09_src.png","path":"H:/pd-media/assets/ai_video/strieff/M09_rife.mp4","public_path":"strieff/motion/M09_rife.mp4","act":2, "tags":["three_factor_scale","balance"] },
{ "asset_id":"STRF-M10","source_scene_id":"MS10","source_still":"H:/pd-media/assets/ai/strieff/M10_src.png","path":"H:/pd-media/assets/ai_video/strieff/M10_rife.mp4","public_path":"strieff/motion/M10_rife.mp4","act":3, "tags":["scotus_colonnade","night"] },
{ "asset_id":"STRF-M11","source_scene_id":"MS11","source_still":"H:/pd-media/assets/ai/strieff/M11_src.png","path":"H:/pd-media/assets/ai_video/strieff/M11_rife.mp4","public_path":"strieff/motion/M11_rife.mp4","act":3, "tags":["empty_seat","scalia"] },
{ "asset_id":"STRF-M12","source_scene_id":"MS12","source_still":"H:/pd-media/assets/ai/strieff/M12_src.png","path":"H:/pd-media/assets/ai_video/strieff/M12_rife.mp4","public_path":"strieff/motion/M12_rife.mp4","act":3, "tags":["five_vs_three_light","vote"] },
{ "asset_id":"STRF-M13","source_scene_id":"MS13","source_still":"H:/pd-media/assets/ai/strieff/M13_src.png","path":"H:/pd-media/assets/ai_video/strieff/M13_rife.mp4","public_path":"strieff/motion/M13_rife.mp4","act":3, "tags":["records_wall","cataloged"] },
{ "asset_id":"STRF-M14","source_scene_id":"MS14","source_still":"H:/pd-media/assets/ai/strieff/M14_src.png","path":"H:/pd-media/assets/ai_video/strieff/M14_rife.mp4","public_path":"strieff/motion/M14_rife.mp4","act":5, "tags":["thinned_chain","attenuation"] },
{ "asset_id":"STRF-M15","source_scene_id":"MS15","source_still":"H:/pd-media/assets/ai/strieff/M15_src.png","path":"H:/pd-media/assets/ai_video/strieff/M15_rife.mp4","public_path":"strieff/motion/M15_rife.mp4","act":5, "tags":["parking_lot","figure_back"] },
{ "asset_id":"STRF-M16","source_scene_id":"MS16","source_still":"H:/pd-media/assets/ai/strieff/M16_src.png","path":"H:/pd-media/assets/ai_video/strieff/M16_rife.mp4","public_path":"strieff/motion/M16_rife.mp4","act":5, "tags":["door_held_open","final"] }
```

**検算:** 16エントリ ✓・全 public_path 非空 ✓（不変条件18）・`^STRF-M\d{2}$` ✓。

## 4.6 `overlay[]` 12エントリ（distinct 素材に数えない）

```jsonc
// particle 6
{ "public_path":"strieff/overlay/P01_marble_dust_motes.mp4",  "type":"particle_assets","subtype":"marble_dust_motes",  "blend_hint":"screen" },
{ "public_path":"strieff/overlay/P02_courtroom_dust.mp4",     "type":"particle_assets","subtype":"courtroom_dust",     "blend_hint":"screen" },
{ "public_path":"strieff/overlay/P03_archive_dust.mp4",       "type":"particle_assets","subtype":"archive_dust",       "blend_hint":"screen" },
{ "public_path":"strieff/overlay/P04_fine_grain_dust.mp4",    "type":"particle_assets","subtype":"fine_grain_dust",    "blend_hint":"screen" },
{ "public_path":"strieff/overlay/P05_night_air_drift.mp4",    "type":"particle_assets","subtype":"night_air_drift",    "blend_hint":"screen" },
{ "public_path":"strieff/overlay/P06_shadow_dust.mp4",        "type":"particle_assets","subtype":"shadow_dust",        "blend_hint":"screen" },
// light 4
{ "public_path":"strieff/overlay/L01_cold_night_shaft.mp4",   "type":"light_assets","subtype":"cold_night_shaft",     "blend_hint":"screen" },
{ "public_path":"strieff/overlay/L02_cold_fluorescent_flicker.mp4","type":"light_assets","subtype":"cold_fluorescent_flicker","blend_hint":"screen" },
{ "public_path":"strieff/overlay/L03_marble_light_shaft.mp4", "type":"light_assets","subtype":"marble_light_shaft",   "blend_hint":"screen" },
{ "public_path":"strieff/overlay/L04_plum_edge_glow.mp4",     "type":"light_assets","subtype":"plum_edge_glow",       "blend_hint":"screen" },
// vfx 2
{ "public_path":"strieff/overlay/V01_film_grain.mp4",         "type":"vfx_overlays","subtype":"film_grain",           "blend_hint":"overlay" },
{ "public_path":"strieff/overlay/V02_cold_light_noise.mp4",   "type":"vfx_overlays","subtype":"cold_light_noise",     "blend_hint":"screen" }
```

runtime で `asset_id`/`path`/`sha256`/`license`/`eyeballed_content`/`qc` を埋める（§9）。**overlay は `cuts[].src` に出さない。** 発色は B が accent `#9C6BAA`（somber-plum）に寄せる想定・A は他話色（gold/blue/amber/teal/crimson/green/civil-violet）の素材を選ばない。

---

# 5. A-1: SDXL 静止画のバッチ生成（85本 × 1枚・バリエーション0）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-049-strieff/04_scenes/ai_prompts.v001.md   ← A が §5.2 の形式で書く
出力:  H:\pd-media\assets\ai\strieff\S<NN>.png（+ remotion/public/strieff/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★パーサ契約（`read_prompts()` はこの2行形式しか読まない）

```
- `S01.png`
<positive prompt> Avoid: <negative>
```

- **1行目:** `` - `S01.png` ``（バッククォート囲み・行末は `.png` の直後）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト
- `ai_prompts.v001.md` は **body 85行（S01..S85）＋ i2v 種 16行（M01_src..M16_src、§8.1a）＝ 101 エントリ**を書く。すべて1枚生成。

## 5.3 生成コマンド（★`--variants 1`。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=101 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 49 --variants 1 --only S01
#   → ログ "episode=... shots=101 variants=1 ... -> 101 images" の shots が 101 であること

# 全101枚（body 85 + i2v種 16・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-049-strieff --variants 1
#   → 生成 S01.png ... S85.png / M01_src.png ... M16_src.png（各1枚。_02/_03 は作らない）
```

> QC で落ちたシーンの再生成は `--only S37`（同じプロンプトで別シードを1枚）。**基準を下げない・バリエーションで水増ししない。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず全文連結）

```
, cinematic still, dark documentary grade, a cold Utah night of quiet suburban houses and a bare parking lot and an unmarked detective's car, set against the pale marble of a state courthouse and the United States Supreme Court and long walls of archived record files, a single somber-plum accent as the one signature note, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face
```

> **EP39〜EP48 との分離（1語も含めない）:** `navy interrogation room`/`electric blue`（EP39 frazier）・`suburban demolition`/`bleached daylight`（EP40 lech）・`prison cell`/`cellblock`/`sodium prison corridor`（EP41 thompson・gold）・`Chicago apartment`/`ankle monitor`/`body-worn camera`（EP42 young・blue #3B7DD8）・`porch-amber house`/`ambulance red lights`/`tow-truck`（EP43 caniglia・amber #E0913C）・`teal-green hospital corridor`/`clinical hospital`（EP44 tekoh・teal #2FA6A0）・`warm-tungsten kitchen table`/`overdue crimson citation stack`（EP45 cleveland・crimson #B23A48）・EP46 tlo の green `#3F8F5F` 系・`dusty warm Texas afternoon`/`two-lane road`/`pickup-truck cab`/`civil-violet #7A5CD0`（EP47 atwater）・EP48 glover 系。**★EP47 の civil-violet #7A5CD0 と EP49 の somber-plum #9C6BAA は別色。混同しない（テキサスの二車線道・ピックアップ・午後の暖色は EP47。EP49 は Utah の夜・駐車場・記録の壁・冷たい大理石・somber-plum）。** EP49 は **Utah の夜の住宅・駐車場・無標識の刑事車・パトカーのライト・IDカードとデータベース画面・令状フラグ・手錠・毒の木/断ち切られた鎖・空席の8席・天秤・最高裁列柱・記録ファイルの壁・somber-plum #9C6BAA の一点差し色。**

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible warrant, legible id card, legible license, legible case citation, legible statute number, legible date, u.s. reports number, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, child, weapon, gun, blood, gore, displayed drugs, drug paraphernalia, syringe, pills, powder, glamorized narcotics, nude, bare skin, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, navy interrogation room, electric blue, suburban demolition, tow truck, ambulance, porch amber house, ankle monitor, body-worn camera, prison cell, steel cellblock, barred cell, sodium prison corridor, teal-green hospital corridor, clinical hospital, warm tungsten kitchen table, two lane texas road, pickup truck, gold, crimson, amber, teal, civil violet
```

> ネガティブにも **制約違反語（"legal stop", "constitutional stop", "exclusionary rule abolished", "we are all harmed" 等）を書かない**（§1.3）。**扇情・薬物の陳列/美化・人体・可読の令状/ID/日付/判例番号・ロゴを NEG で明示的に抑制**（制約2/5）。ロゴ/文字が必要な絵は「blurred into an unreadable smear」で判読不能に。

## 5.6 バリエーション軸（★EP49 では無効）

`--variants 1` は各 stem を**1枚だけ**生成する。反復回避は「85本の固有プロンプト＝85の別被写体」で担保。

## 5.7 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_strieff_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.8 プロンプトの絶対ルール（85本すべてに適用）

- **顔なし・身体なし・裸体なし。** Strieff・Detective Fackrell・判事を個人として描かない（制約1/5）。人物は後ろ姿/手元/影/象徴のみ。
- **可読文字なし。** 令状・IDカード・データベース画面・意見書・条文ページ・カレンダーは雰囲気のみ。判例番号・日付（2016/2006）・票決（5-3）・警察/州/会社ロゴを描かない。
- **薬物は臨床最小限。** メタンフェタミンは「small plain sealed evidence bag, contents not shown, clinical and minimal」の象徴のみ。粉/錠剤/注射器/使用シーン/陳列を描かない・美化しない（制約5）。
- **象徴オブジェのみ:** 夜の家の玄関から出る後ろ姿／駐車場の後ろ姿／無標識の刑事車／パトカーのライト／IDカード（判読不能）／無線マイク／データベースの令状フラグ画面（判読不能）／開いた/閉じた手錠／毒の木と黒ずんだ実（fruit of the poisonous tree）／弱い一環のある鎖／断ち切られた鎖（attenuation）／三要素の天秤／時計（時間的近接）／最高裁列柱・大理石・空席の8席（Scalia）／5-3の光点（可読数字なし）／記録ファイルの壁（カタログ化）／開いたまま保持されるドア。
- **停止を「合法」化しない**（制約1）: 停止が合法/正当に見える絵を作らない。停止は違法。証拠が残ったのは attenuation。
- **排除法則を「廃止」化しない**（制約2）: 排除法則が消滅/廃止に見える絵を作らない。狭められた（例外）。
- **票決を数字で描かない**（制約4）: 5-3 は光点/光の分割の象徴で（可読数字なし）。**"6-3" の光点にしない。**
- **反対の逐語を可読で描かない**（制約6）: "carceral state" / "anyone's dignity" / Kagan の incentive 逐語は AE カード（B）。画像は象徴のみ。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの85エントリをそのまま書く・各1枚）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記のマクロ）。全て顔なし・身体なし・象徴・判読不能・薬物非扇情。

```
- `S01.png`
The front door of a modest Utah house opening at night, warm light spilling onto a dark step, a figure's back just visible stepping out and seen from behind only, an ordinary evening where it all began, no face, no readable text [STYLE] Avoid: [NEG]
- `S02.png`
A man seen only from behind walking across a bare parking lot at night toward a distant car under cold somber-plum sodium light, not running and carrying nothing visible, no face, no readable text [STYLE] Avoid: [NEG]
- `S03.png`
An unmarked detective's car parked across a dark empty lot at night, still and watching, a quiet ordinary sedan under a streetlight, no people, no readable plate, no readable text [STYLE] Avoid: [NEG]
- `S04.png`
A plain identification card lying face-down and abstract under a hard flashlight beam on a dark surface, the ID that was handed over and read out, the print unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S05.png`
A dark database screen with a single line resolving into a small warning flag glowing somber-plum, an outstanding record surfacing, the characters abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S06.png`
The pale marble facade of a courthouse at night lit from below, cold and institutional, the promise that an illegal search is normally thrown out, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S07.png`
The pale marble facade and tall columns of the United States Supreme Court at night, cold stone lit from below, monumental and distant, the court that answered this in 2016, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S08.png`
A heavy chain lying across a dark surface with one link stretched thin and nearly parted, glowing faintly somber-plum, the idea of a connection worn down until it barely holds, symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S09.png`
A modest suburban Utah house seen from a distance at night with one lit window, quiet and ordinary, the house a detective watched on an anonymous tip, no people, no readable signage [STYLE] Avoid: [NEG]
- `S10.png`
A dim residential walkway at night with faint motion-blurred traces of comings and goings, brief visits read as a pattern, figures reduced to blur and never shown, no face, no readable text [STYLE] Avoid: [NEG]
- `S11.png`
A bare parking lot at night lit by a single cold lamp, empty asphalt and long shadows, the ordinary place a man was stopped, no people, no readable text [STYLE] Avoid: [NEG]
- `S12.png`
A man's back halted mid-stride in a hard beam of light on dark night asphalt, stopped where he stood and seen from behind only, the illegal stop that is the whole case, no face, no readable text [STYLE] Avoid: [NEG]
- `S13.png`
A plain identification card held flat in a cold flashlight beam on a dark surface, the print abstract and unreadable, the ID being read out to a dispatcher, no legible text, no people [STYLE] Avoid: [NEG]
- `S14.png`
A handheld police radio microphone resting in the dark with a single somber-plum indicator light, the name relayed over the air, no people, no readable text [STYLE] Avoid: [NEG]
- `S15.png`
The cold glow of a dispatcher's console in a dark room, rows of abstract unreadable light, the name being checked against a database, no legible text, no people [STYLE] Avoid: [NEG]
- `S16.png`
A dark screen with a single record line resolving into a small outstanding warrant flag in somber-plum, a name coming back with something attached, the text abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S17.png`
A single slim record folder half-drawn from a dark filing drawer, an old small matter that had sat in a database for years, the label abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S18.png`
A pair of open handcuffs resting on a dark surface in a hard shaft of cold light, cold steel waiting, the tool the warrant permitted, no people, no readable text [STYLE] Avoid: [NEG]
- `S19.png`
A pair of handcuffs closed shut in cold light on a dark surface, the arrest made on the warrant, symbolic and severe, no people, no readable text [STYLE] Avoid: [NEG]
- `S20.png`
A small plain sealed evidence bag resting alone on a dark surface in cold clinical light, its contents not shown and abstract, the search that rode on the warrant, minimal and clinical, no legible text, no people [STYLE] Avoid: [NEG]
- `S21.png`
The plain exterior of a small Utah police station at night under a cold somber-plum sky, ordinary and civic, the door the case was carried through, no people, no readable sign [STYLE] Avoid: [NEG]
- `S22.png`
The pale stone facade of the Utah state courthouse at dusk under a somber-plum sky, civic and quiet, the state court that first ordered the evidence suppressed, no people, no readable sign [STYLE] Avoid: [NEG]
- `S23.png`
A bare tree at night bearing a few darkened, blighted fruit, stark against a cold sky, the fruit of the poisonous tree, symbolic and abstract, no people, no readable text [STYLE] Avoid: [NEG]
- `S24.png`
A close view of a single darkened, spoiled fruit hanging from a bare branch in cold light, the tainted thing that grew from a wrong, symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S25.png`
A bare tree at night with its dark roots exposed in cold somber-plum light, the illegal act poisoning everything that grows out of it, symbolic and severe, no people, no readable text [STYLE] Avoid: [NEG]
- `S26.png`
A heavy iron chain running taut across a dark surface link by link in cold light, the causal chain from the wrong to the evidence, symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S27.png`
A heavy chain with one link worn thin and glowing somber-plum among solid links in cold light, the single weak point where the connection might give, symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S28.png`
A cold marble wall with a single narrow doorway cut through it in somber-plum shadow, an exception carved into an otherwise solid rule, symbolic and severe, no people, no readable text [STYLE] Avoid: [NEG]
- `S29.png`
A chain stretched so far across a dark gap that its thinned middle link barely spans it in cold light, a connection so attenuated it hardly holds, symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S30.png`
A balance with three separate pans hanging from one cold beam in low light, three factors weighed against each other, symbolic and abstract, no legible text, no people [STYLE] Avoid: [NEG]
- `S31.png`
A pair of plain balance scales weighing a small folded wrong on one pan against a sealed evidence bag on the other in cold light, the wrong against the evidence, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S32.png`
An old pocket watch on a dark surface with its two hands standing only minutes apart under cold light, the short time between the illegal stop and the discovery, no legible numerals, no people [STYLE] Avoid: [NEG]
- `S33.png`
A plain clock face caught with its second hand mid-sweep in cold somber-plum light, only minutes passing, the factor of time, no legible numerals, no people [STYLE] Avoid: [NEG]
- `S34.png`
A taut chain interrupted midway by a single object wedged between two links in cold light, an intervening event breaking the flow from the wrong to the evidence, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S35.png`
A folded official document wedged firmly between two links of a heavy chain in cold somber-plum light, the pre-existing warrant standing as the intervening circumstance, the print abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S36.png`
A cold road forking into two paths in dark light, one an honest wrong turn and one a deliberate route, the question of purpose and flagrancy, symbolic, no people, no readable signage [STYLE] Avoid: [NEG]
- `S37.png`
A single flashlight beam sweeping across dark empty ground at night, searching for something to turn up, the fishing-trip the third factor asks about, no people, no readable text [STYLE] Avoid: [NEG]
- `S38.png`
A single cold glint of light on a dark badge-shaped surface, authority implied by one abstract highlight, no name, no legible text, no people [STYLE] Avoid: [NEG]
- `S39.png`
An old watch, a folded document, and a small balance set together in one cold frame on a dark surface, the three factors of time, intervening event, and flagrancy, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S40.png`
A long courthouse corridor receding into cold institutional light with a polished floor and closed doors, the passage a case is carried up, no people, no readable signage [STYLE] Avoid: [NEG]
- `S41.png`
A neat stack of bound legal briefs on a desk in cold light, the arguments filed on both sides of the question, the spines abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S42.png`
The modest stone facade of a federal courthouse at dusk under a somber-plum sky, civic and unremarkable, the courts the case passed through, no people, no readable sign [STYLE] Avoid: [NEG]
- `S43.png`
The pale marble facade and tall columns of the United States Supreme Court seen frontally at night, monumental and solemn, the court that would decide it, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S44.png`
An empty curved bench in a grand marble courtroom under cold light with eight places set and one place left conspicuously empty, the eight-justice court rendered without any person, solemn and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S45.png`
A single vacant high-backed seat set apart in deep shadow at a curved marble bench in cold light, the seat left empty after a justice's death, solemn and still, no people, no readable text [STYLE] Avoid: [NEG]
- `S46.png`
Five points of somber-plum light standing against three dimmer points on a dark marble field, a five-to-three split rendered as light, no numerals, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `S47.png`
A cold marble floor divided into a larger lit share and a smaller darker share, a majority and a dissent rendered only as light, no numerals, symbolic and severe, no people, no text [STYLE] Avoid: [NEG]
- `S48.png`
An opinion volume lying open under a cold lamp, its pages reduced to abstract illegible lines, the majority walking through the three factors, no legible words, no people [STYLE] Avoid: [NEG]
- `S49.png`
A single plain pen resting on a closed opinion cover in cold light, the majority opinion being written, the cover abstract and unmarked, no legible text, no people [STYLE] Avoid: [NEG]
- `S50.png`
An old pocket watch with its hands only minutes apart lying dim in a corner of cold light, the one factor the majority admitted it lost, time, no legible numerals, no people [STYLE] Avoid: [NEG]
- `S51.png`
A clock face rendered faint and low-weighted in cold somber-plum light, the factor of time pointing toward suppression but outweighed, no legible numerals, no people [STYLE] Avoid: [NEG]
- `S52.png`
A folded official document resting in an old drawer beneath a layer of dust in cold light, a warrant that existed long before and apart from the stop, the print abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S53.png`
A single heavy chain link snapping apart at its thinned point in a shaft of cold light, the warrant standing as a genuine intervening circumstance that breaks the chain, symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S54.png`
A folded document and a pair of closed handcuffs joined by a short length of chain in cold light, the arrest flowing from the warrant and not from the stop, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S55.png`
A pair of balance scales in cold light tipping toward a pan marked only by a faint shape of an honest mistake, the misconduct found at most negligent, not flagrant, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S56.png`
A plain investigator's notebook and a folded tip resting on a dark desk in cold light, a real tip honestly investigated and a bad call made, the writing abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S57.png`
A heavy chain fully broken into two falling halves at a thinned link in cold somber-plum light, the connection attenuated and the chain snapped, the central image of the ruling, symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S58.png`
A small sealed evidence bag settled on a cold surface in a quiet shaft of light, the evidence that stayed in, minimal and clinical, its contents not shown, no legible text, no people [STYLE] Avoid: [NEG]
- `S59.png`
The marble colonnade of the Supreme Court at night lit from below, cold and distant, the ruling handed down, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S60.png`
Two separate closed opinion volumes set slightly apart from a larger volume in cold light, the two dissents standing beside the majority, the covers abstract and unmarked, no legible text, no people [STYLE] Avoid: [NEG]
- `S61.png`
A single closed opinion volume standing in a lone shaft of cold light on a dark surface, the first dissent set apart, the cover abstract and unmarked, no legible text, no people [STYLE] Avoid: [NEG]
- `S62.png`
A patrol car's light bar switching on with a cold somber-plum flare against dark night asphalt, the reason to stop that a ruling can hand the police, no people, no readable text [STYLE] Avoid: [NEG]
- `S63.png`
A lone figure's back standing on an empty night sidewalk under a cold streetlight, seen from behind only, the person the dissent points to on the sidewalk, no face, no readable text [STYLE] Avoid: [NEG]
- `S64.png`
A plain identification card held under a cold scanning beam of light on a dark surface, a legal status that can be checked at any time, the print abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S65.png`
A stark cold doorway opening onto a bare somber-plum threshold in deep shadow, a body subject to invasion while the violation is excused, austere and symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S66.png`
Long receding walls of archived record files vanishing into cold shadow, a citizen reduced to a file to be cataloged, the labels abstract and unreadable, the dissent's warning of a carceral state, no legible text, no people [STYLE] Avoid: [NEG]
- `S67.png`
A single plain file folder standing in a vast dark archive drawer among countless identical files in cold light, a person waiting to be cataloged, the labels abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S68.png`
A single plain unmarked card standing among rows of identical cards in cold light, the point that this can happen to anyone, no name, no face, no legible text, no people [STYLE] Avoid: [NEG]
- `S69.png`
A second closed opinion volume standing alone in a lone shaft of cold light on a dark surface, the second dissent set apart, the cover abstract and unmarked, no legible text, no people [STYLE] Avoid: [NEG]
- `S70.png`
A pair of balance scales tipping steeply toward a somber-plum patrol-light glow on the heavier pan in cold light, the incentive to make an unlawful stop increasing, symbolic, no legible text, no people [STYLE] Avoid: [NEG]
- `S71.png`
The bare parking lot again at night lit by one cold lamp, empty asphalt and long shadows, the question returning to where it began, no people, no readable text [STYLE] Avoid: [NEG]
- `S72.png`
A man's back once more walking away across a dark parking lot at night, seen from behind only, the man we started with, no face, no readable text [STYLE] Avoid: [NEG]
- `S73.png`
A dark database screen with a single line resolving again into a small somber-plum warrant flag, a name run and a warrant found, the text abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S74.png`
A man's back still held motionless in a hard beam of light on dark asphalt, seen from behind only, the stop that was still illegal and never pretended otherwise, no face, no readable text [STYLE] Avoid: [NEG]
- `S75.png`
A single chain link worn thin to almost nothing glowing somber-plum in cold light, everything riding on one word, attenuation, symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S76.png`
A single folded document glowing faint somber-plum in a dark wall of records, an old unrelated warrant sitting in a database and rescuing the evidence, the print abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S77.png`
A faint mark left on a cold marble surface after a shadow lifts away, a wrong that did not disappear but simply stopped mattering, symbolic and abstract, no legible text, no people [STYLE] Avoid: [NEG]
- `S78.png`
A vast dark wall of records dotted with many small somber-plum warning flags receding into shadow, the very large number of people carrying some outstanding warrant, the labels abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S79.png`
A single slim record card for an old small matter resting in a dark drawer in cold light, an unpaid fine or a missed date sitting for years, the print abstract and unreadable, no legible text, no people [STYLE] Avoid: [NEG]
- `S80.png`
A patrol car's light bar glowing cold and untroubled on empty night asphalt, an illegal stop that has become almost free, no people, no readable text [STYLE] Avoid: [NEG]
- `S81.png`
A cold marble floor bearing a single fine crack running across it lit faint somber-plum, the fault line the dissents were pointing at, symbolic and severe, no people, no readable text [STYLE] Avoid: [NEG]
- `S82.png`
A single chain link visibly corroding and thinning in cold light on a dark surface, the rule against breaking the rules growing weaker, symbolic, no people, no readable text [STYLE] Avoid: [NEG]
- `S83.png`
A plain door held slightly open onto a bar of soft somber-plum light in cold shadow, a rule that lets an unlawful stop pay off whenever a warrant is waiting, symbolic, no people, no readable sign [STYLE] Avoid: [NEG]
- `S84.png`
A distant lone figure's back standing small in a vast dark parking lot at night, seen from behind only, the man in the parking lot held once more, no face, no readable text [STYLE] Avoid: [NEG]
- `S85.png`
A single chain link worn thin held in a last quiet shaft of somber-plum light on a dark surface in a slow pull-back, one thinned-out chain, unresolved but open, no people, no readable text [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 85 エントリ（S01..S85）。§5.3 の `--only S01` ログで `shots=101`（body 85 + i2v種 16）を確認してから本番を回す。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 85 + i2v種 16 = 全101枚・`qc_strieff_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `30.0<=mean_luma<=225.0`（EP49 は夜・冷たい大理石・記録の壁が多く全体に暗い→黒潰れリスク大。`DARK_LUMA_FLOOR=42.0` を大きく下回る本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**バリエーション0なので本来ほぼ衝突しない。衝突は駐車場系(S02/S11/S71/S72/S84)・後ろ姿(S01/S12/S63/S72/S74/S84)・手錠系(S18/S19/S54)・鎖系(S08/S26/S27/S29/S53/S57/S75/S82/S85)・最高裁列柱系(S07/S43/S59)・令状フラグ画面(S05/S16/S73/S76)・記録の壁(S66/S67/S78)・パトカーのライト(S62/S70/S80) の被りに注意** | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・判例番号(579 U.S. 232)・日付(2016/2006)・金額・票決(5-3)・警察/州ロゴが写っていないか（R1・制約2/6） | `has_readable_text=true`→reject |
| Q6 | 顔の混入 | **目視。** 識別可能な顔（Strieff/Fackrell/判事）・後ろ姿が横顔に転じていないか（R1・制約1/5） | `has_identifiable_face=true`→reject |
| Q7 | 身体/扇情/薬物の混入 | **目視。** 人体の露出・薬物の陳列（粉/錠剤/注射器）・扇情が写っていないか（制約5） | `has_human_body=true`→reject |

**Q5/Q6/Q7 は機械で判定しない。全101枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-049-strieff --media image
#   → runs/qc/strieff_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-48 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** SDXL は平気で読める文字・顔・身体を描く。**特に S04/S13/S64（IDカード）は読める英字/写真が無いこと、S05/S16/S73/S76（データベース/令状フラグ）は読める英字/数字が無いこと、S20/S58（証拠袋）は薬物の中身が写らず陳列でないこと、S44/S45（8席・空席）は識別可能な人物が写らないこと、S46/S47（票決）は可読の数字が無く"5-3"であって"6-3"に読めないこと、S66/S67/S78（記録の壁）はロゴ/可読ラベルが無いこと、S01/S12/S63/S72/S74/S84（後ろ姿）は顔・横顔が写らないこと、を必ず目で確認する。**

## 6.2 出力

```
episodes/PD-2026-049-strieff/05_visuals/still_qc.v001.json     # 101枚全部の行（reject も残す）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が101枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 49 --variants 1 --only S37   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_strieff_stills.py
```
accepted body >= 85 かつ i2v_source >= 16 になるまで繰り返す。**基準を下げない・水増ししない。**

## 6.4 depth map（★既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/strieff"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`。冪等。
- **role が `body` の静止画は depth 必須**（無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/strieff/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 93本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（Utah の夜の住宅街/駐車場/夜の道・無標識の車/パトカー・警察署や庁舎の外観・大理石の裁判所/長い廊下・空の法廷・最高裁列柱・州会議事堂・記録/書庫の棚・夜〜夕暮れ・繋ぎ）
  light_assets/    …            合成レイヤー（冷たい夜光・冷たい fluorescent・大理石の光条・plum 差し）
  particle_assets/ …            合成レイヤー（大理石法廷の埃・書庫/記録の塵・夜気）
  vfx_overlays/    …            合成レイヤー（グレイン・光ノイズ）
  texture_assets/  …            紙・石・大理石のテクスチャ
  loops/           …            抽象的な繋ぎ
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>（TYPECODE = BG|LIGHT|LOOP|PART|TEX|VFX）
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json
   （トップキーは schema と assets。★必ず encoding="utf-8" で開く。cp932 既定だと落ちる）
```

## 7.2 選定条件

- **`kind=="video"` のみ。** 静止画 factory は使わない
- **93本ちょうど**（§3.3[7] より 93 は still-share≤0.45 を守る下限。減らせない）
- **各1回しか使わない**（`MAX_USES_FACTORY=1`）
- 幕別割り当て（§4.4）: HOOK=6 / OPENING=3 / ACT1=12 / ACT2=16 / ACT3=24 / ED=12 ＋ 繋ぎ=20 ＝ 93
- **EP39〜EP48 の絵柄を選ばない（§7.7 の分離語）。** EP49 は Utah の夜の住宅街/駐車場/夜の道・無標識の車/パトカー・警察署/庁舎の外観・大理石の裁判所の長い廊下/空の法廷/最高裁列柱・州会議事堂・記録/書庫の棚・夜〜夕暮れ。**鉄格子/独房/cellblock を選ばない（EP41 分離）。病院/臨床を選ばない（EP44 分離）。テキサスの二車線道/ピックアップ/暖色の午後を選ばない（EP47 分離）。薬物の陳列・泣く人・実在の顔が写るニュース映像を選ばない（制約5・R1）。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query supreme_court --limit 96 --exclude-used --ep PD-2026-049-strieff --json
```
`--exclude-used` は出荷ゲート `arc_nonrepeat` と同じ指紋集合を使う。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・§4.4 に pre-assign 済み）

> **★`covers_scene_id` は still 資産 ID 空間（S01..S85）を指す。narrative シーン（S01..S48）とは別体系。**

| covers | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S06 | 大理石の裁判所ファサード（夜） | `courthouse_facade_night` / `marble_courthouse` | 0 |
| S07 | 最高裁ファサード・列柱 | `supreme_court_building` / `marble_columns` | 0 |
| S09 | Utah の住宅（夜・監視の家） | `suburban_house_night` / `residential_house_dark` | 0 |
| S11 | 夜の駐車場 | `parking_lot_night` / `empty_lot_streetlight` | 0 |
| S21 | 警察署の外観（夜） | `police_station_exterior` / `small_town_police_night` | 1 |
| S22 | 州裁判所の外観（夕暮れ） | `state_courthouse` / `courthouse_exterior_dusk` | 2 |
| S40 | 裁判所の長い廊下 | `courthouse_corridor` / `long_courthouse_hallway` | 2 |
| S42 | 連邦裁判所の外観（夕暮れ） | `courthouse_exterior_dusk` / `federal_courthouse` | 2 |
| S43 | 最高裁の列柱（正面・夜） | `supreme_court_columns` / `marble_facade_night` | 3 |
| S59 | 最高裁の列柱（夜） | `marble_colonnade_night` / `courthouse_columns_night` | 3 |
| S63 | 夜の空き歩道 | `empty_sidewalk_night` / `street_night` | 1 |
| S71 | 夜の空き駐車場（受け） | `parking_lot_night_empty` / `empty_lot_dark` | 5 |
| S78 | 記録ファイルの壁 | `archive_shelves` / `records_wall` | 3 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: 大理石の廊下・空の法廷・列柱の光条・庁舎の外観・Utah の夜の道・雨のアスファルト・書庫/記録の棚・抽象 `loops`。**暗いクリップに偏りすぎない**（暗側は全体の1/3=約31本まで。大理石の昼光・夕暮れ側も混ぜる）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）

```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★

> **推測ではなく実際に起きた事故。** EP36: `city_surveillance_camera_dome` が大聖堂。EP38: 牛が `documents_on_desk`。`subtype` は「その検索語で取った」記録であって**中身の保証ではない**。

**選抜93本は例外なく次を経る:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-049-strieff --media video --dir "<93本の staging フォルダ>"
#   → runs/qc/strieff_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、93本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP49テーマ・ウォーターマークなし・識別可能な実在人物なし（制約1/5・R1）を確認
5. **★制約5の目視:** 人物が写るクリップは避け、写る場合も後ろ姿/遠景/顔外しのみ。**薬物の陳列・泣く人・扇情を含むクリップは使わない。** 実在の判事/警官の顔が写るニュース映像を使わない。**鉄格子/独房/cellblock（EP41）・病院/臨床（EP44）・テキサスの二車線道/ピックアップ（EP47）を含むクリップを使わない。**
6. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=42.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP49 は夜・冷たい大理石・記録の壁が多いので暗側が本命リスク。** 平均輝度42未満が全体の40%を超えると FAIL。**暗いクリップは約31本（1/3）までに抑え、大理石の昼光・夕暮れ・冷たい fluorescent の実用光がある本を混ぜる。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-049-strieff/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-049-strieff/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP48 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_strieff_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-048-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP49 の93本の積集合が**空**であることを確認。1件でも exit 1。**EP39〜EP48 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

**分離レーン（色・素材・語）:** EP41 gold #E5B53A（監獄）／EP42 blue #3B7DD8（ankle monitor）／EP43 amber #E0913C（porch/救急車/レッカー）／EP44 teal #2FA6A0（病院）／EP45 crimson #B23A48（暖色台所/督促）／EP46 green #3F8F5F／EP47 civil-violet #7A5CD0（テキサスの二車線道/ピックアップ/午後）／EP48 glover。**EP49 = somber-plum #9C6BAA（INK #0A0A0C）。★EP47 の civil-violet #7A5CD0 と近い紫だが別色・別被写体（EP47=テキサス昼の道、EP49=Utah 夜の駐車場/記録の壁）。** これら他話の絵柄・色・被写体を1本も選ばない。

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py --variants 1` で `M<NN>_src.png` として生成（`ai_prompts.v001.md` に §8.1a の16行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `STRF-MS01..MS16`、モーション成果物は `STRF-M01..M16`。

| # | asset_id | 種画像 | 動きの意味 | act |
|---|---|---|---|---|
| 1 | STRF-M01 | M01_src | 夜の家の玄関ドアが開き、後ろ姿がわずかに踏み出す | 0 |
| 2 | STRF-M02 | M02_src | 夜の駐車場・背後からパトカーの灯が近づく | 0 |
| 3 | STRF-M03 | M03_src | IDカードにフラッシュライトの光が移ろう | 1 |
| 4 | STRF-M04 | M04_src | 無線マイクの indicator が明滅する（照会） | 1 |
| 5 | STRF-M05 | M05_src | データベースの行が令状フラグに解決する | 1 |
| 6 | STRF-M06 | M06_src | 手錠が閉じる寸前 | 1 |
| 7 | STRF-M07 | M07_src | 毒の木の実がわずかに揺れる（fruit of the poisonous tree） | 2 |
| 8 | STRF-M08 | M08_src | 鎖の弱い一環が張力で軋む | 2 |
| 9 | STRF-M09 | M09_src | 三要素の天秤・手錠側/証拠側が沈む | 2 |
| 10 | STRF-M10 | M10_src | 最高裁の列柱・冷たい光が動く | 3 |
| 11 | STRF-M11 | M11_src | 8席のうち1席の空席に影が落ちる（Scalia） | 3 |
| 12 | STRF-M12 | M12_src | 5つの plum 光点が3つに対して立つ（5-3・可読数字なし） | 3 |
| 13 | STRF-M13 | M13_src | 記録ファイルの壁への緩い前進（カタログ化） | 3 |
| 14 | STRF-M14 | M14_src | 断ち切られた鎖の細った一環が緩く揺れる（attenuation） | 5 |
| 15 | STRF-M15 | M15_src | 夜の駐車場の後ろ姿が歩き去る | 5 |
| 16 | STRF-M16 | M16_src | わずかに開いたまま保持されるドアへの緩い pull-back（最終） | 5 |

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの16行を追加・各1枚）

```
- `M01_src.png`
The front door of a modest Utah house standing just ajar at night with warm light on a dark step and a figure's back poised to step out and seen from behind only, still and poised, no face, no readable text [STYLE] Avoid: [NEG]
- `M02_src.png`
A bare parking lot at night with a faint patrol-car light glow rising in the far distance behind, cold somber-plum sodium light, still and poised, no people, no readable text [STYLE] Avoid: [NEG]
- `M03_src.png`
A plain identification card lying flat under a hard flashlight beam on a dark surface, the print abstract and unreadable, still and poised for the light to move, no legible text, no people [STYLE] Avoid: [NEG]
- `M04_src.png`
A handheld police radio microphone resting in the dark with a single somber-plum indicator light poised to blink, framed and still, no people, no readable text [STYLE] Avoid: [NEG]
- `M05_src.png`
A dark database screen with a record line poised to resolve into a small somber-plum warrant flag, the characters abstract and unreadable, still, no legible text, no people [STYLE] Avoid: [NEG]
- `M06_src.png`
A pair of handcuffs held open on a dark surface in cold light, poised just before they close, symbolic and still, no people, no readable text [STYLE] Avoid: [NEG]
- `M07_src.png`
A bare tree at night bearing a few darkened blighted fruit poised to sway on the branch in cold light, the fruit of the poisonous tree, still, no people, no readable text [STYLE] Avoid: [NEG]
- `M08_src.png`
A heavy chain with one link worn thin among solid links in cold light, poised under tension and about to strain, symbolic and still, no people, no readable text [STYLE] Avoid: [NEG]
- `M09_src.png`
A balance weighing a small folded wrong against a sealed evidence bag in cold light, poised with the heavier pan about to sink, symbolic and still, no legible text, no people [STYLE] Avoid: [NEG]
- `M10_src.png`
The pale marble colonnade of the United States Supreme Court at night lit from below, monumental and still, poised for a slow move, no people, no readable inscription [STYLE] Avoid: [NEG]
- `M11_src.png`
An empty curved marble bench with eight places and one place left conspicuously empty in cold light, poised and still for a shadow to fall across the vacant seat, no people, no readable text [STYLE] Avoid: [NEG]
- `M12_src.png`
Five points of somber-plum light standing against three dimmer points on a dark marble field, a five-to-three split rendered as light, still and poised, no numerals, symbolic, no people, no text [STYLE] Avoid: [NEG]
- `M13_src.png`
Long receding walls of archived record files vanishing into cold shadow, the labels abstract and unreadable, framed for a slow forward move, no legible text, no people [STYLE] Avoid: [NEG]
- `M14_src.png`
A heavy chain broken at a thinned link on a dark surface in cold somber-plum light, the parted ends poised to sway gently, symbolic and still, no people, no readable text [STYLE] Avoid: [NEG]
- `M15_src.png`
A bare parking lot at night with a figure's back standing motionless and poised to walk away, seen from behind only under cold light, still and open-ended, no face, no readable text [STYLE] Avoid: [NEG]
- `M16_src.png`
A plain door held slightly ajar onto soft somber-plum light, poised and still for a slow pull-back, the held final image, no people, no readable sign [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_atwater.py` を下敷きにパスと SHOTS だけ差し替え）

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
STILL_DIR     = H:\pd-media\assets\ai\strieff      # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\strieff
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, child, crying person, displayed drugs, drug paraphernalia, gore, blood"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely` / `assert_frame_math`。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_strieff.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_strieff.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_strieff.py --run-all          # 残り15本（冪等・既存スキップ）
```
1本 24–73 GPU分・16本で 7–19時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_strieff.py`・`rife_atwater.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・身体・**薬物の陳列・泣く人**が生成されていないこと（NEG で抑えているが**必ず目視**・制約5）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- M01/M02/M15（後ろ姿/駐車場/道路）は**識別可能な顔・横顔・車のナンバー・読める標識**が写り込んでいないこと（制約1/2）
- M05（令状フラグ）は**可読の英字/数字が出ていない**こと（制約2）／M12（5-3 光点）は**可読の数字が出ていない**こと（制約4）
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（16本 × 2回 = 32カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど12本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **6本** | 大理石法廷の埃・書庫/記録の塵・夜気。黒背景 drift を screen 合成 |
| `light_assets` | **4本** | 冷たい夜光・冷たい fluorescent・大理石の光条・plum の差し |
| `vfx_overlays` | **2本** | 微細なグレイン・冷たい光ノイズ |
| **合計** | **12本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/strieff/overlay/` に置き、`strieff_film.json` の `cuts[].src` には**出さない**。黒背景でループするものを選び `blend_hint` を書く（§4.6 の12本に対応）。発色は B が accent `#9C6BAA`（somber-plum）に寄せる想定・A は他話色（gold/blue/amber/teal/crimson/green/civil-violet）を選ばない。**§7.5 の目視QC対象**（12本）。

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 20 --exclude-used --ep PD-2026-049-strieff --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_strieff_assets.py`）

```
remotion/public/strieff/img/     ← role=body の静止画85枚（+ 同名 _depth.png）
remotion/public/strieff/factory/ ← 選定 factory .mp4 93本（§4.4 の F001..F093 名で）
remotion/public/strieff/motion/  ← i2v M<NN>_rife.mp4 16本
remotion/public/strieff/overlay/ ← 合成レイヤー 12本（§4.6 の P/L/V 名で）
```
- `public_path` はマニフェストの値（§4.4/§4.5/§4.6）と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する）:**
- factory の `public_path` は必ず `strieff/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `strieff/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep49Strieff"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/strieff/` に正典を置くところまで。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_strieff_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_strieff_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_strieff_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**★factory 93 / motion 16 が非空で実体化しているか（不変条件17/18）を必ず確認。** Bのファイルを直接書き換えて知らせようとしない。

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）

```python
MAX_USES_FACTORY = 1
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
```
種別判定は**パス文字列**（`kind_of()`）: `/factory` or `af-bg-` → factory / `.mp4|.mov|.webm` or `ai_video` or `_rife` → motion / それ以外 → still。§10.1 の命名規則を守る。

EP49 の設計値: still 101/85=1.19(≤2) / factory 93/93=1.0(≤1) / motion 32/16=2.0(≤2) / first-use 194/226=0.8584(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）〜EP48（glover）のファイルに一切触らない。** 読み取りのみ可。素材・色・音のレーンも分離（§7.7）。EP49 の accent は **somber-plum #9C6BAA**（INK #0A0A0C・B が OP/AEカード/サムネで使用・A は絵で流用色を作らない）。**★EP47 の civil-violet #7A5CD0 と混同しない。**
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_strieff_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness・身体をどこにも作らない**（§1・制約1/5）。特に **Strieff・Detective Fackrell・判事を個人として描かない。**
- **6制約に反する文言・絵をプロンプト・タグ・注記・ファイル名のどこにも作らない**（§1.2/§1.3）:
  - 停止の「合法(legal/lawful/constitutional/justified)」化（制約1）／排除法則の「廃止(abolished/struck down/dead)」化（制約2）／令状が停止を合法化したという描写（制約3）／票決の可読数字化・"6-3"（制約4）／逐語の可読描画・"we are all harmed"（制約6）／薬物の陳列/美化・人の扇情（制約5）／可読の令状/ID/日付/判例番号/ロゴ（制約2/6）。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 85 で担保。
- **role=thumb / still_thumb を作らない・overlay を12本以外にしない。** サムネは also_thumb=true の body 6枚（§4.3 = {S12,S43,S45,S46,S57,S62}）。
- **★factory 93 / motion 16 の配列を空・stub のまま出荷しない**（EP45 の事故。§4.4/§4.5 を必ず実体化・public_path 非空）。
- **★dochighlight figure（黒バー/box/underline）を作らない・言及しない。** A の `tags`/`caption_hint`/`notes` にも `dochighlight` という文字列を書かない（grep で 0 を保つ）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 85 / factory 93 / i2v 16 / distinct 194 / first-use 0.8584 / still-share 0.4469 / MG≥31 / 12.0分）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約1/2/5は目視でしか守れない）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 85 / i2v_source 16 / also_thumb 6 [S12/S43/S45/S46/S57/S62] / reject N）
2. factory 選定 93本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数、駐車場/記録/画面クリップの「no readable text / no logo / no face / no displayed drugs」確認
3. EP39〜EP48（十話）重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）＋ factory 93/motion 16 が非空で実体化した確認
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック（still_body 85 / still_i2v_source 16 / motion 16 / factory 93 / overlay 12）
9. 6制約・1枚前提の自己申告（停止の合法化なし/排除法則の廃止化なし/令状が停止を合法化する描写なし/票決可読数字なし・"6-3"なし/逐語可読描画なし・"we are all harmed"ゼロ/薬物陳列・美化なし・人の扇情なし・バリエーション0・Strieff/Fackrell/判事 非人物化を目視確認・dochighlight 文字列ゼロ・A↔B同一スキーマ [schema strieff_assets.v1 / role enum body|i2v_source|reject / counts / also_thumb 集合 {S12,S43,S45,S46,S57,S62} / overlay 12]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
</content>
</invoke>
