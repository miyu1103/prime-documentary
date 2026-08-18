# EP52 morton — Codex スレッドB「実装 + レンダ」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> これは *The Michael Morton Case*（30分・4幕・payoff 末尾積み上げ）の BUILD/RENDER 実行プロンプト。
> 設計 `EP52_morton_DESIGN_ARCHITECTURE.v001.md` の intent を本書に全展開済み（数値は転記済）。
> スレッドA（素材生成）の `EP52_morton_CODEX_A_ASSETS.v001.md` は**読まない**（Aは FROZEN・接続点は §3 のマニフェスト1ファイル）。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP52 / Episode ID: PD-2026-052-morton / slug: morton
Composition id（本編）: Ep52Morton
フォーマット: standard_30min（30分尺・~54,129フレーム provisional・レンダは1–2時間＝想定内）
```

**題材:** 1986年テキサス州 Williamson County で Christine Morton が自宅ベッドで撲殺され、夫 **Michael Morton**（無実）が証拠を隠されて誤って有罪・life・約25年服役。2005年に pro-bono の **John Raley** と Innocence Project（**Nina Morrison**）が DNA 検査を求め、後任 DA **John Bradley** が約6年争ったが 2011-06 に裁判所がバンダナ検査を命令。DNA が別の男 **Mark Alan Norwood**（真犯人）に一致、Morton は 2011-10-04 釈放・**2011-12-19 無罪確定（第45番目のテキサスの DNA 冤罪救済）**。Norwood は Christine 殺害で有罪（2013-03-27）、さらに **1988-01 の Debra Baker 殺害**（Morton が服役中）にも DNA 一致で 2016-09 有罪。検事 **Ken Anderson** は Court of Inquiry で 2013-04-19 逮捕命令・criminal contempt・10日収監（実質約5日）・弁護士資格を返上。**the Michael Morton Act**（証拠開示改革法）が 2013 に成立。
本作の主題は「**証拠を隠された冤罪・25年・二人の実在の villain・末尾に積み上がる真実の連鎖**」。**Michael Morton は存命・法的に完全に無罪確定＝彼の無実を事実として断定してよい。**

> **★正確性制約が全出力を律する（§2・`check_morton_facts.py`）。**
> **R-MORTON-INNOCENT**（Morton の無実を事実として述べる・有罪を匂わせない）・**R-VICTIM**（Christine Morton・Debra Baker は実在の殺害被害者＝尊厳・描写/再現なし）・**R-CHILD**（3歳 Eric は最大限の配慮・documented account のみ・識別可能な子供顔なし）・**R-VILLAIN-FACT**（Norwood/Anderson は record の事実のみ・likeness なし）・**R-NUM**（hedged 数値は断定禁止）・**R-FACE**（匿名は可・実在 likeness は不可）・**R-READABLE**（可読の偽公文書禁止）・**R-DOCHL**（dochighlight 不使用）・**R-QUOTE**（検証済み逐語2件＋帰属のみ）・**R-DATE**。

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。実装は全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-052-morton/**` |
| B-2 | マニフェスト**消費側**バリデータ | `scripts/check_morton_asset_manifest.py`（**複製**） |
| B-3 | 事実台帳 MO-ID と 制約ゲート（**BLOCKING**） | `scripts/check_morton_facts.py`（**複製**） |
| B-4 | `morton_film.json` ビルダ（**manifest→576 cuts＋82 figures＋captions／実素材のみ／★HOOK-AUDIO voice-from-0**） | `scripts/build_morton_film.py`（**複製**） |
| B-5 | beats バリデータ（AE 17 cards ↔ figures 82／年 group:false／layout allowlist） | `scripts/validate_morton_beats.py`（**複製**） |
| B-6 | **AE layout allowlist ゲート**（6 proven のみ許可） | `scripts/check_AE_layouts.py`（**新規／既存があれば流用**） |
| B-7 | 構文境界字幕生成器（実測 narration_index から verbatim） | `scripts/gen_captions_morton.py`（**複製**） |
| B-8 | **After Effects カード**のビルダ（**★6 proven layout のみ・17枚**）とコンポジタ | `scripts/ae/build_morton_hero_cards.py`（**複製**）/ `scripts/ae/composite_morton_hero.py`（**複製**） |
| B-9 | 本編 BGM ミックス（AEカード合成の基底 mp4・**★HOOK-AUDIO: VO ON from 0.0**） | `scripts/build_morton_bgm_real.py`（**複製・OFF→0.0**） |
| B-10 | 本編 Remotion コンポジション登録 `Ep52Morton`（**★CaseFilm の voice-from-0 対応込み**） | `remotion/src/Root.tsx` |
| B-11 | OP バンパー `OpeningMorton`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningMorton.tsx` |
| B-12 | サムネ3案（**CTR §4A emotive-face**） | `remotion/src/compositions/MortonThumbnails.tsx` |
| B-13 | 本編レンダ→BGM→AEカード合成→全ゲート→**全編アイボール3回（FULL ~30分）** | `episodes/PD-2026-052-morton/08_edit/**` |

> **★このスレッドは「実素材のみ」。stub/placeholder のコードパスを作らない**（`grep -riE 'stub|placeholder' scripts/*morton*.py` が 0）。
> **★clone 元は実在ファイルのみ**（`ls scripts/` で確認）。**直近の `*centralpark*`（EP50）を優先、無ければ `*cleveland*`/`*caniglia*` の実在監査済ファイルを複製元にする**（§0.3）。

## 0.2 もう一方のスレッド（A・FROZEN）との境界 — **接続点はただ1ファイル。**
```
episodes/PD-2026-052-morton/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者・FROZEN）        ↓ Bが消費（唯一の消費者・検証者）
```
**Bはこのファイル以外のAの中間生成物を読まない。** counts / role enum / overlay枚数 / also_thumb 集合 / thumb_face枚数 は A↔B で**1バイト単位で共有**（§3）。

### 0.2.1 ファイル所有権（これを破ると並行作業が壊れる）
| パス | 所有 | Bの権限 |
|---|---|---|
| `episodes/PD-2026-052-morton/{manifest.json,00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `scripts/*morton*.py` / `scripts/ae/*morton*.py` | **B** | 新規作成 |
| **`episodes/PD-2026-052-morton/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ** |
| **`H:\pd-media\assets\ai\morton\**` / `ai_video\morton\**`** | **A** | **読み取りのみ** |
| **`remotion/public/morton/{img,factory,motion,overlay,thumb,audio}/**`** | **A** | **読み取りのみ**（B の `public_slim` staging は §12） |
| `EP52_morton_DESIGN*.md` / `EP52_morton_CODEX_A_*.md` / `..._FACTS_LEDGER.v001.md` / `..._script.en.v001.md` | **設計/上流** | **読み取りのみ**（★durationInFrames/narrationSeconds は実測後に B が更新可＝§5.1.1） |
| `episodes/PD-2026-0{01..51}-*/**` / それらの素材 / `scripts/*{他slug}*.py` | **他エージェント** | **絶対に触るな（読み取り可）** |

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）
| パス | 役割 | 手本（実在確認してから複製→パス/定数差し替え・`*centralpark*` 優先） |
|---|---|---|
| `scripts/check_morton_asset_manifest.py` | §3.3 消費側バリデータ | `check_centralpark_asset_manifest.py` |
| `scripts/check_morton_facts.py` | §2 制約＋台帳（BLOCKING） | **`check_centralpark_facts.py`** |
| `scripts/build_morton_film.py` | §5 film.json（実素材・factory/motion 全読込・年 group:false・**★HOOK-AUDIO**） | **`build_centralpark_film.py`** |
| `scripts/validate_morton_beats.py` | §7.6 不変条件 | **`validate_centralpark_beats.py`** |
| `scripts/check_AE_layouts.py` | §7.7 AE layout allowlist（既存があれば流用・無ければ新規） | 既存 `check_AE_layouts.py`（EP50 で作成済のはず）or `check_year_grouping.py` を手本に新規 |
| `scripts/gen_captions_morton.py` | §8 字幕生成器 | **`gen_captions_centralpark.py`** |
| `scripts/ae/build_morton_hero_cards.py` | §7 AEカードビルダ（**6 proven layout のみ・Tier-B を ADD しない**） | **`build_centralpark_hero_cards.py`**（Tier-B builder は使わない／複製元の6 layout をそのまま） |
| `scripts/ae/composite_morton_hero.py` | §7.9 コンポジタ | **`composite_centralpark_hero.py`** |
| `scripts/build_morton_bgm_real.py` | §5.1.2/§7.9 基底 mp4（**★VO ON from 0.0**） | **`build_centralpark_bgm_real.py`** |

> **`build_morton_film.py` 複製時に差し替える定数:** `SLUG="morton"`・`EP="PD-2026-052-morton"`・`DEFAULT_OUT=remotion/src/data/morton_film.json`・`PUB_FILM=remotion/public/morton/film_data.v001.json`・`expected={"still":250,"factory":240,"motion":86}`（distinct: still215/factory240/motion43）。**ロジック（`public_items()`/`repeated()`/`take()`/`allocate`/`build_figures`/`build_captions`）は変えない。ただし §5.1.2 の HOOK-AUDIO（voice-from-0）と §5.3 の treatment=depth 撤去は明示的に改変する。**

## 0.4 完了条件（実素材で、全て緑になったら「実装完了」）— 要旨:
1. マニフェスト消費側バリデータが A の FROZEN 本番マニフェスト相手に PASS（§3.3）
2. 字幕を実測 narration から構文境界で生成し `check_caption_breaks`/`check_caption_integrity` PASS（§8）
3. film.json を実マニフェストから組む（footage 混在・factory240/motion43 全読込・**dochighlight 0**・**年 group:false**・**depth treatment 不使用**・**★VO from 0.0**・§5）
4. **全ゲート PASS**（§10・script_length は **30分 band cap≈5,450**・animation_mix・check_year_grouping・check_AE_layouts・check_morton_facts）
5. AE 17 cards（6 proven layout のみ）をビルド→二段 aerender→composite（§7）
6. 本編レンダ（`--public-dir=public_slim`）→ BGM → AE合成 → `check_final_acceptance 52`（§10）
7. **完成 mp4 を 0→末尾まで FULL ~30分・3周アイボール**（§13.1）

**台本は既に確定済み**（`EP52_morton_script.en.v001.md`・**~5,326語・LOCKED**）。本番配置先 `episodes/PD-2026-052-morton/03_script/script.en.v001.md`（**1バイトも変えずコピー**・整形禁止）。

---

# 0.5 ★★★ EP38–51 で踏んだ失敗＝最初から防ぐ ★★★
1. **紙芝居（EP45 死因）** — `build_morton_film.py` は `public_items(manifest,"factory")` が 240本・`public_items(manifest,"motion")` が 43本を返すことを起動時に assert し、0本 or 不一致なら exit 1。cuts に factory240 + motion86 の footage を最初から入れ still-share を **0.4340**（cap 0.45）に収める（§5.2）。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の figures のみ数える。AE 17 cards は別勘定。→ §6 で **`figures[]` を 82本**（floor 75・`graphics[]=[]`）。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字は無言で消える。**`dochighlight` は使わない**（R-DOCHL）。**`comparebars`→`compbars`／`VoteTally`→`votetally`。quote/votetally は不使用。**
4. **台帳に無い数値を焼くな** — §2 の MO-ID 台帳に検証済み値だけ。`check_morton_facts.py` が全数値照合。hedged（25/6/5/100/$1.96M）は断定表示で FAIL。
5. **★YEAR のコンマ群化バグ（EP46/47 "1,987"）** — YEAR を出す全 figure/AE numeric（1986/1987/1988/2005/2011/2013/2016）に `group:false`。桁区切りが正しい $1,960,000 は `group:true`。`check_year_grouping.py` が enforce（§9）。
6. **字幕は台本本文と対応** — narration_index の実チャンク文を verbatim（§8）。
7. **★phantom-layout crash（EP48/49）** — 複製元 JSX は末尾 `else throw "unsupported layout"`。**`DATE_STAMP`/`SEAM_TRANSITION` は非実装＝BANNED**（日付カードは `CENTER_STACK`）。**EP52 は 6 proven layout のみ・Tier-B 新 layout を ADD しない**（§7）。**`VOTE_SPLIT` も emit しない**（検証済み陪審票割れが台帳に無い＝捏造回避）。
8. **★NEW: HOOK-AUDIO 無音 runway（本作で潰す）** — 従来 CaseFilm は hook 8.0s + opening 3.5s の間 Brian の声が鳴らない「無音の助走」だった。**本作は Brian の声を 0:00 から鳴らす**（§5.1.2）。CaseFilm/BGM/composite/durationInFrames を voice-from-0 に改変。
9. **★NEW: depth treatment の warp** — depth displacement は被写体を melt/warp（EP48/49 欠陥）。**treatment は `bleed`/`parallax`/`duotone`/`focus` のみ・`depth` を使わない・depth map を参照しない**（§5.3・A も depth を生成しない）。
10. **★NEW: milky wash / scanline** — 全画面 haze/fog/vignette-wash・scanline/CRT を乗せない。grade は最小・neutral（screen-wash ≤0.07）・クリア高コントラスト（§5.9）。

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）
| パス | なぜ読むか |
|---|---|
| `scripts/build_centralpark_film.py`（無ければ `build_cleveland_film.py`） | **複製元。** `public_items()`/`repeated()`/`take()`/`allocate`/`build_figures`/`build_captions`。**factory(240)/motion(43) を必ず読む**。**★treatment 循環から depth を外す（§5.3）・★VO from 0.0（§5.1.2）** |
| `scripts/ae/build_centralpark_hero_cards.py`（無ければ `build_cleveland_hero_cards.py`） | **複製元（FIXED版）。** `fit_size()`/`count_keys()`/REPO path 出力/二段レンダ/6 layout（`buildActTitle`/`buildCenter`=CENTER_STACK+MONEY_STACK/`buildQuote`/`buildVote`/`buildCompare`）/`else throw`。**Tier-B builder は使わない・6 proven のみ** |
| `scripts/ae/composite_caniglia_hero.py`（or centralpark 版） | **複製元。** SKIP4条件・ffmpeg フィルタグラフ・`film_offset_sec` 読み込み |
| `scripts/gen_captions_cleveland.py`（or centralpark 版） | **複製元。** `internal_split()`/`chunk_sentence()`/`NO_DANGLE_END` |
| `scripts/build_caniglia_bgm_real.py`（or centralpark 版） | **複製元。** narration＋BGM ミックス（**★VO ON from 0.0**） |
| `scripts/check_centralpark_facts.py`（or cleveland 版） | **複製元（正確性ゲート）。** 構造除外（`asset_manifest` を R-NUM から除外・geometry キー除外・`kind!="acttitle"` 条件） |
| `scripts/check_year_grouping.py` | **既存ゲート。** 年 group:false の検査（§9） |
| `remotion/src/components/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames` / **★HOOK-AUDIO 改変対象（§5.1.2）**。**depthSrcOf は使わない（depth treatment なし）** |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在 `kind`**（§6.2・全小文字・`dochighlight` 使わない）。`numberticker` は `{value;label?;prefix?;suffix?;decimals?;group?}`＝`group?:boolean` 実在 |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC` / `ENDCARD_SEC=9` / `BrandOpening`（**★HOOK-AUDIO で overlap sting 化・§5.1.2**）/ `BrandEndcard` |
| 各ゲート `check_*` | 通すべき判定ロジック（§10） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §11 の OP 正典実装 |

---

# 2. ★ EP52固有の正確性制約・事実性ロック（`scripts/check_morton_facts.py`・BLOCKING）
> 検査対象は `morton_film.json` の figures/captions、AE beats、サムネ、props、固定コメント、`03_script/script.en.v001.md`、`09_package/*`、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。出力 `09_package/facts_lock.v001.json`。**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。**

## 2.1 正確性制約（全出力に適用・違反は BLOCKER）
| # | 制約 | 許可 | 禁止 |
|---|---|---|---|
| **R-MORTON-INNOCENT** | **Morton の無実を事実として** | 「wrongfully convicted」「exonerated」「innocent」「a court declared him innocent」「DNA identified the real killer」「the state's theory that the husband did it」（帰属枠） | Morton が犯人だと**断定/示唆**（"Morton killed / the husband did it" を帰属なし断定で）／"guilty after all" |
| **R-VICTIM** | **Christine Morton・Debra Baker＝実在の殺害被害者・尊厳** | 「Christine Morton was beaten to death in her bed」「Debra Baker was killed in her Austin home」（臨床・平叙） | 暴行/殺害/遺体の**描写・再現・扇情語**／被害者の imagery・肖像／"objects piled on the body" の描写／血・凶器の描写 |
| **R-CHILD** | **Eric（3歳）＝最大限の配慮** | documented account: 「a "monster"」「a big mustache」「his daddy was not home」（帰属付き） | Eric が襲撃を目撃する場面の再現／識別可能な子供の顔・肖像／記録外の子供情報 |
| **R-VILLAIN-FACT** | **Norwood/Anderson＝record の事実のみ** | Norwood「the DNA-identified killer of both women」「convicted」／Anderson「found in criminal contempt」「jailed」「surrendered his law license」「a court ordered his arrest」 | 記録外の犯行詳細・lurid／Anderson の内心の embellish（court の言葉を超える）／likeness |
| **R-NUM** | **数値は台帳一致・hedged は断定禁止** | §2.2 の allowed set のみ。hedged 値は `~`/`about`/`roughly`/`nearly`/`reportedly` 併記 | 台帳外の数値／`~25 years`(hedged)・`~6 years`(hedged)・`~5 days`(hedged)・`~100 yards`(hedged)・`~$1.96M`(hedged) を hedge 語なしで断定 |
| **R-FACE** | **匿名は可／実在 likeness は不可** | 匿名の一般人（顔は背向き/影/ソフトで非識別・§CODEX_A H シリーズ）／empty bed of absence／blue bandana／green van（distant）／crayon monster scrawl（非識別子供）／file drawer／DNA bands／cell window／`AI-assisted visualization`（右下常時） | **実在人物 likeness/顔**（Morton/Christine/Eric/Norwood/Anderson/Bradley/Raley/判事）・mugshot of a real person・deepfake／**被害者の描写・暴行/遺体 imagery**／**識別可能な子供顔**／読める偽公文書 |
| **R-READABLE** | **可読の偽公文書なし** | "unreadable smear" の雰囲気のみ | 読める case file/report/newspaper/DA memo/DNA数値/日付/案件番号 |
| **R-DOCHL** | **dochighlight 不使用** | `kinetic`/`stat`/`highlightring` で代替 | `figures[].kind`/beats/layout 名に `dochighlight` |
| **R-QUOTE** | **検証済み逐語2件＋帰属のみ** | (1)「the other side can't have access to those reports.」— Ken Anderson (of record)／(2)「This court cannot think of a more intentionally harmful act than a prosecutor's conscious choice to hide mitigating evidence so as to create an uneven playing field.」— Court of Inquiry (Apr 19, 2013) | 上記2件以外の引用符／attribution 欠落／**Michael が Christine に残した note の逐語**（未検証＝引用禁止） |
| **R-DATE** | 日付を取り違えない | Aug 13 1986（殺害）/Feb 17 1987（有罪）/Jan 1988（Baker）/2011（exon）/2013（Anderson・Act） | 年は全て `group:false`（§9） |

**★禁止語（`check_morton_facts.py` が全文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`morton killed` / `morton is guilty` / `the husband did it`（**帰属枠 "the state's theory that the husband did it" は許可・帰属なし断定のみ禁止**）/ `guilty after all` / `possibly guilty morton`（R-MORTON-INNOCENT）、`beaten body` / `bludgeoned corpse` / `murder scene` / `objects piled on`（描写として）/ `blood on the bed`（R-VICTIM）、`glorified norwood` / `heroic norwood`（R-VILLAIN-FACT）、`exactly 25 years`（累計の断定・hedged は "nearly/about 25"）。
> **★重要な設計注意:** 台本本文（＝字幕 verbatim）には `beaten to death`/`murder`/`bandana`/`Norwood`/`Anderson` 等の語が正当な文脈で含まれる。**禁止語は主語付き断定形/描写形だけ**を選んである。**`beaten`/`murder`/`bandana`/`confession` の単語単独を禁止語に足すな**（字幕 verbatim を巻き込む）。

## 2.2 事実台帳 MO-ID（`03_script/morton_facts.v001.json`・**B が `EP52_morton_FACTS_LEDGER.v001.md` から転記**）
**スキーマ版:** `morton_facts.v1`。各 MO-ID は `{"claim":..., "value":..., "unit":..., "verified":bool, "confidence":"high|medium", "screen_phrasing":"", "attribution":"", "quote":""}`。

| MO-ID | 内容（screen 要点） | conf | 画面での扱い |
|---|---|---|---|
| MO01 | Christine Morton 撲殺・自宅ベッド・Williamson County TX・木製棍棒（凶器未回収） | high | R-VICTIM 臨床のみ・**描写/遺体なし** |
| MO02 | 殺害 **August 13, 1986**（Michael の32歳誕生日 Aug 12 の翌朝） | high | date 断定（**year group:false**）・`32` 可 |
| MO03 | Michael は当朝**約6時**にスーパーへ出勤・帰宅して遺体発見・3歳 Eric が在宅 | high | `6 a.m.` 可・R-CHILD |
| MO04 | Eric（3歳）が祖母に「a "monster"（父ではない）が母を襲った・父はいなかった」 | high | **帰属付き・識別可能子供顔なし** |
| MO05 | 証言は祖母 **Rita Kirkpatrick** 経由・**Sgt. Don Wood** の transcript | high | 名称・帰属 |
| MO06 | 近隣が家の裏の **緑のバン**の男・林へ歩く、を目撃 | high | green van（distant・no plate） |
| MO07 | 検察の motive theory＝誕生日にセックスを断られた rage（soft-cite） | medium | **"the prosecution's theory" 帰属のみ** |
| MO08 | **1986-09-25 逮捕**・**物証ゼロ**・胃内容物 time-of-death（debunked）でアリバイ消去 | high | `0`（物証）断定可 |
| MO09 | 検事 **Ken Anderson**（Williamson County DA・後に判事） | high | 名称・R-VILLAIN-FACT |
| MO10 | **1987-02-17 有罪・life**（+$5,000 fine soft-cite） | high | date（year **group:false**）・`5,000` は "reportedly ~" |
| MO11 | 隠された証拠: Eric の account／緑のバン／**血のバンダナ**（~100yd・約1ブロック・建設現場付近・後に Christine の血/毛＋別の男の DNA）／盗まれた purse・card/checkbook（San Antonio 使用）／不明の指紋・足跡 | high | 各 hedge（100yd は "roughly ~"）・**可読の偽公文書なし** |
| MO12 | Anderson の隠匿は意図的・record「**the other side can't have access to those reports**」 | high | R-QUOTE verbatim(1)＋attribution |
| MO13 | Morton は**約25年**服役 | high(hedged ~) | "nearly/about 25"（断定 "25 years" 単独は避け hedge 併記） |
| MO14 | **2005** John Raley（pro bono）＋ Nina Morrison/Innocence Project が DNA 検査（バンダナ含む）を申請 | high | year（group:false）・名称 |
| MO15 | 後任 DA **John Bradley** が DNA 検査を**約6年**争った | high(hedged ~) | "roughly six years" |
| MO16 | **2011-06** 裁判所がバンダナ検査を命令 | high | year（group:false） |
| MO17 | バンダナ DNA＝Christine の血/毛＋別の男（not Morton）＝**Mark Alan Norwood** | high | R-VILLAIN-FACT |
| MO18 | **2011-10-04 釈放**・**2011-12-19 無罪確定**（Judge Sid Harle）・**第45番目**のテキサス DNA 冤罪 | high | date（group:false）・`45` 可 |
| MO19 | **Mark Alan Norwood**（dishwasher・Bastrop TX・Austin圏 mid-80s・前科）＝Christine 殺害で有罪・life・**2013-03-27** | high | R-VILLAIN-FACT |
| MO20 | Norwood の DNA が **1988-01 の Debra Masters Baker 殺害**（Austin・similar manner）にも一致＝**Morton 服役中の第二殺人**・Norwood は Baker 殺害で **2016-09** 有罪 | high(THE GUT-PUNCH) | R-VICTIM 尊厳・date（group:false） |
| MO21 | **Court of Inquiry**（2013-02）・**2013-04-19 Anderson 逮捕命令**・「**a more intentionally harmful act…**」 | high | R-QUOTE verbatim(2)＋attribution |
| MO22 | Anderson は判事を辞任（2013-09-23） | high | year（group:false） |
| MO23 | **2013-11-08 criminal contempt・no contest・10日収監（実質約5日）・$500 fine・500時間 community service・弁護士資格を返上**（tampering は取下げ） | high(days hedged ~5) | `10`/`500` 可・"served about 5 days"・**"gave up his license"（disbarred と断定しすぎない）** |
| MO24 | **the Michael Morton Act**（Texas SB 1611）・Perry 知事署名 **2013-05-16**・施行 2013-09-01・証拠開示 open-file 義務を拡大 | high | year（group:false）・名称 |
| MO25 | 釈放後 息子 Eric と再会・再婚（Cindy Chessman・2013）・補償 **約$1.96M**＋annuity | high(hedged ~) | "roughly $1.96 million"（**group:true**） |

> **数値の許可集合（R-NUM・narrative figure/AE/thumb/props のみ対象）:**
> years `{1986, 1987, 1988, 2005, 2011, 2013, 2016}`（**全て group:false**）／`32`（誕生日）／`3`（Eric・age）／`0`（物証）／`45`（45th Texas man）／`10`（Anderson 収監日数）／`500`（$fine・community hours）／hedged `~`: `25`(years・nearly)・`6`(Bradley years・roughly)・`5`(Anderson days・about)・`100`(yards・roughly)・`5,000`($fine・reportedly)・`1,960,000`($・roughly・**group:true**)。**これ以外の数値が figures/AE/サムネ/props に出たら FAIL。** narration verbatim（script.md）は R-NUM 対象外。

## 2.3 `check_morton_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）
**★複製元の構造除外を1行も削らない:** `asset_manifest*.json` は R-NUM 対象外・`start/end/dur/fps/width/height/frames/duration_sec/x/y/index` キーは構造値としてスキップ・文脈ルールは `kind != "acttitle"` のとき発火。
**検査対象ファイル（ハードコード・無いものは `skipped[]` に明記）:**
```
episodes/PD-2026-052-morton/03_script/script.en.v001.md
episodes/PD-2026-052-morton/03_script/morton_facts.v*.json
episodes/PD-2026-052-morton/08_edit/ae_hero/beats.json
episodes/PD-2026-052-morton/09_package/*.json / *.txt
episodes/PD-2026-052-morton/05_visuals/asset_manifest*.json   （tags/caption_hint/qc.notes・★R-NUM 除外）
remotion/src/data/morton_film.json                            （figures[].* の全文字列と数値）
remotion/props/morton*.json                                   （title/subtitle）
```
- **R-FORBID（最優先）** — §2.1 禁止語（主語付き断定/描写形）が出たら即 FAIL。**`beaten`/`murder`/`bandana`/`confession` 単独を足さない。**
- **R-MORTON-INNOCENT（BLOCKING）** — Morton を語る payload に `killed`/`guilty`/`did it` が**帰属なし断定**で付いたら FAIL（"the state's theory"/"the prosecution claimed" 帰属は許可）。
- **R-VICTIM（BLOCKING）** — `Christine`/`Debra`/`Baker`/`victim` payload に負傷詳細・遺体・扇情語・imagery 指示があれば FAIL。臨床枠のみ許可。
- **R-CHILD（BLOCKING）** — `Eric`/`the boy`/`three-year-old` payload に襲撃目撃の再現・識別可能子供顔指示があれば FAIL。documented account（monster/mustache/daddy not home）帰属のみ許可。
- **R-VILLAIN-FACT** — `Norwood`/`Anderson` payload は record の事実のみ（記録外詳細・美化で FAIL）。
- **R-NUM（narrative のみ）** — figures/AE/サムネ数字が §2.2 allowed set に完全一致必須。hedged 値が hedge 語なし断定で FAIL。`asset_manifest*.json` は R-NUM 対象外。
- **R-HEDGE** — `confidence:medium`（MO07）・hedged（MO13/15/23days/25/MO11 yards/MO10 fine/MO25）を hedge なし画面焼きで FAIL。
- **R-FACE** — `has_readable_text==true` or `has_identifiable_real_person==true` or `has_victim_or_violence==true` は `role=="reject"`。**`has_human_body==true` は reject しない。** 正プロンプトに実在 likeness 語・被害者描写・識別可能子供顔があれば FAIL。生成ビジュアル区間の `AI-assisted visualization` 欠落・`description.txt` の AI 開示行欠落で FAIL。
- **R-DOCHL（BLOCKING）** — `morton_film.json` の `figures[].kind` に `dochighlight` が1件でも出たら FAIL。beats.json/layout 名にも出さない。
- **R-QUOTE（BLOCKING）** — 引用符に入る文字列は `APPROVED_QUOTES`（§2.1 の2件・verbatim）に一致＋非空 attribution。それ以外は FAIL。**Michael の note を引用符に入れたら FAIL。**
- **R-DATE** — Aug 13 1986（殺害）/ Feb 17 1987（有罪）/ Jan 1988（Baker 殺害）/ Oct 4 2011（釈放）/ **Dec 19 2011（無罪確定）** / 2013（Norwood 有罪・Anderson contempt・the Act）/ 2016（Norwood-Baker 有罪）を取り違えない。**★本件の exoneration は 2011-12-19（EP50 Central Park の 2002-12-19 と混同しない）。** 年は全て `group:false`。

**出力:** `09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[...],"skipped":[...]}`）。**CLI:** `--json`。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル・FROZEN）

## 3.1 スキーマ（Aが生成する・Bはこの形を前提に読む・A↔B 1バイト一致）
**スキーマ版:** `morton_assets.v1`（固定。異なれば **exit 2**）。点数:
**still_body 215 / still_i2v_source 43 / motion 43 / factory 240 / overlay 30 / thumb_face 3。**
**★サムネ:** body のうち **4枚**に `also_thumb:true`（`role=thumb`/`still_thumb` を作らない）。前景の emotive-face は **thumb_face 3枚**（§12）。
**`role` enum（固定・4値）:** `"body"` | `"i2v_source"` | `"thumb_face"` | `"reject"`。
**`counts`（固定キー・確定値）:** `{ "still_body":215, "still_i2v_source":43, "motion":43, "factory":240, "overlay":30, "thumb_face":3 }`。

- `stills[]`: `asset_id`/`scene_id`/`role`/`also_thumb`/`act`(0..5)/`public_path`(`morton/img/S###.png`)/`width>=3840`/`sha256`/`tags`/`caption_hint`/`qc{...}`。**★`depth_path` は無い（depth treatment 不使用）。** i2v 種・thumb_face は `public_path==null`。
- `motion[]`: **43本**。`public_path` は `.mp4` かつ `_rife` を含む。`build_morton_film` が `public_items(manifest,"motion")` で全読込（**0本 or ≠43 なら exit 1**）。
- `factory[]`: **240本**。`public_path` は `/factory/` を含む。`eyeballed_content` 非空・`qc.label_matches_content==true`。全読込（**0本 or ≠240 なら exit 1**）。
- `overlay[]`: `cuts[].src` に出さない。`public_path` は `/overlay/` を含み `/factory/` を含まない。

## 3.2 Bがこのマニフェストから作るもの（cuts 割当）
| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 215枚 | **静止画カット250本**（`kind:"img"`・**treatment 循環＝bleed/parallax/duotone/focus・depth なし**・各≤2回） | still distinct215/cuts250 |
| body で `also_thumb==true` の4枚 | サムネ3案の**背景**（§12・4 asset ID・A↔B 一字一致） | — |
| `stills[role="thumb_face"]` 3枚 | サムネ3案の**前景 emotive-face**（§12） | — |
| `stills[role="i2v_source"]` 43枚 | **本編カットに出さない** | — |
| `motion` 43本 | **i2vカット86本**（`kind:"footage"`・各≤2回） | motion distinct43/cuts86 |
| `factory` 240本 | **実写カット240本**（`kind:"footage"`・各1回のみ） | factory distinct240/cuts240 |
| `overlay` | **`cuts[].src` に出さない** | — |

**合計 250 + 86 + 240 = 576 カット / distinct 215+43+240 = 498 / first-use 498/576 = 0.8646 ✓／still-share 250/576 = 0.4340 ✓／avg-uses 576/498 = 1.157 ✓≤1.4**

## 3.3 `scripts/check_morton_asset_manifest.py`（消費側バリデータ・BLOCKING）
```bash
$PY scripts/check_morton_asset_manifest.py --assets <path> [--json]
```
検査（1違反で exit 1・`schema_version` 違いだけ exit 2）:
1. `schema_version=="morton_assets.v1"` / `episode_id=="PD-2026-052-morton"` / `slug=="morton"` / `is_stub==false`
2. `counts.*` が各配列の実長と一致し確定値（body215/i2v43/motion43/factory240/overlay30/thumb_face3）
3. `role` は 4値のみ（`thumb`/`still_thumb` で FAIL）
4. `role=="body"` 全 still で `public_path` 非null・`remotion/public/<public_path>` が実在（**★`depth_path` は要求しない・depth 参照なし**）。`role=="i2v_source"`/`role=="thumb_face"` は `public_path==null`
5. `role!="reject"` 全 still で `max(width,height)>=3840`
6. `motion[].public_path` が `.mp4` で終わり `_rife` を含む
7. `factory[].public_path` が `/factory/` を含む
8. `overlay[].public_path` が `/overlay/` を含み `/factory/` を含まない・overlay 長==30
9. `sha256` が全配列を通して一意（B は自集合内一意を検査）
10. `factory[].eyeballed_content` 非空・`qc.label_matches_content==true`
11. **★reject 条件:** `qc.has_readable_text==true` or `qc.has_identifiable_real_person==true` or `qc.has_victim_or_violence==true` は `role=="reject"`。**`qc.has_human_body==true` は reject 条件でない。**
12. `also_thumb==true` の body が**ちょうど4**・`scene_id` 集合が §12 の4 ID と完全一致
13. `thumb_face` が**ちょうど3**（`^MOR-T\d{2}$`・`public_path==null`）
14. 全文字列値が §2 の R-FORBID/R-FACE/R-DOCHL を通る（R-NUM は asset_manifest 除外）
15. **★どの still にも `depth_path` キーが無い**（depth treatment 不使用）

> **★特に `factory==240` と `motion==43` が非0であることを最優先で assert（EP45 空配列事故の直接防止）。**

---

# 4. narration_index（TTS は課金＝B は起動しない。**実測版を消費**する）
## 4.1 なぜ narration_index か
`build_morton_film.py` は**尺・区間・字幕を narration_index から導出**する。秒数をコードに直書きしない。

## 4.2 スキーマ（`morton_narration.v1`）
```jsonc
{
  "schema_version": "morton_narration.v1",
  "episode_id": "PD-2026-052-morton",
  "is_stub": false,
  "voice_id": "nPczCjzI2devNBz1zQrb",   // ElevenLabs "Brian"・NEVER SAPI
  "total_seconds": 1795.3,               // ★provisional。FINAL は forced-align 実測が上書き
  "chunks": [ { "section": "HOOK", "start": 0.0, "end": 6.0, "text": "There was a three-year-old boy in the house the morning his mother was beaten to death, and he told the grown-ups exactly what happened. He said a monster did it." } ]
}
```
**section 値（固定・7区）:** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ACT_4` / `ENDING`。
`build_morton_film.py` は `section_windows()`（各 section 最初のチャンク start）で幕境界を得る。
> **★HOOK-AUDIO（§5.1.2）: HOOK チャンクの `start` は必ず `0.0`**（Brian の cold-open 行が 0:00 から鳴る）。narration_index の最初のチャンクが cold-open 行であること・`voice_id` が Brian であることを assert。

## 4.3 spec のタイムライン（設計目標・実タイミングは narration_index が上書き）
語数配分（provisional）: ACT1 ~1250 / **ACT2 ~1500（engine）** / ACT3 ~1000 / **ACT4 ~1500（climax）** 語。総語数 ~5,326。
**唯一の正は `python scripts/check_script_length.py <script> --json`（30分 band・cap ≈5,450）。**

## 4.4 実測 narration_index の受領
本番は別工程が **ElevenLabs "Brian"（voice_id nPczCjzI2devNBz1zQrb）** TTS→faster-whisper で `06_audio/narration_index.v001.json`（`is_stub:false`・`measure_vo_wpm` 帯 168–190 wpm）を作る。**課金なので B は起動しない。** 来た json を `--narr` に渡すだけ。**台本本文はそのまま。**

---

# 5. `morton_film.json` の構築（`scripts/build_morton_film.py`＝複製・実素材のみ）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から）
```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{...}[]; cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];   // 必須。EP52 は []
  figures?:FigureSpec[]; heroCuts?:{start:number;dur:number;src:string}[];
};
```
- `fps = 30`。`narration = "morton/narration.mp3"`（Brian）。
- **★`hookLine` = morton 固有（流用禁止）:**
  ```
  "A three-year-old told them a monster did it. They buried the truth for twenty-five years."
  ```
  （R-MORTON-INNOCENT/R-QUOTE 整合＝子供の証言・埋められた真実・25年）。

## 5.1.2 ★★★ HOOK-AUDIO — 声が 0:00 から鳴る（owner directive・本作の新標準）★★★
> **owner directive（evidence-based）:** トップ動画は frame 0 から音声/声で開く。従来 CaseFilm は hook 8.0s + opening 3.5s の**約11.5秒 Brian の声が鳴らない「無音の助走」**だった＝これを潰す。**HOOK は Brian の最も掴む cold-open 行を 0:00 から鳴らす**（無音/音楽だけの build-up を作らない）。ハイライトシーンに音ごと放り込む。

**★実装（voice-leads-from-0 モデル）:**
1. **narration（全編・COLD OPEN 行から）を 0:00 に置く。** `narration_index` の最初のチャンク（section `HOOK`）の `start==0.0` が **Brian の cold-open 第一声**。VO onset / captions / BGM VO / AE `film_offset_sec` の**アンカー定数 `BODY_START_SEC` を `0.0`**（従来 11.5）にする。
2. **hook/opening 秒は加算しない。** hook の映像＋sound design は narration と**同時進行**。branded opening（`BrandOpening`）は**残すが overlap sting 化**＝声を鳴らしたまま重ねる短い（~2.0–2.5s）ブランド sting/lower-third で、その音楽を **VO の下に ≥12dB ダック**（声を gate しない・無音 runway を作らない）。
3. **★durationInFrames を再定義（§5.1.1）。** hook/opening の前置秒を除去する。
4. **Real-audio 制約（HARD）:** Brian narration ＋ dramatized SFX/ambience のみ。**実在人物の音声を一切使わない**（Morton/Anderson/判事/ニュース/911 の archival audio なし）。

**★Morton の cold-open 第一声（script COLD OPEN の冒頭・narration_index HOOK チャンク・start 0.0）:**
```
"There was a three-year-old boy in the house the morning his mother was beaten to death,
 and he told the grown-ups exactly what happened. He said a monster did it."
```
- **映像（0:00 から同時・§CODEX_A の hook 素材）:** 最も強い single visual＝a small child's hand ＋ an abstract crayon "monster" scrawl（MOR-S001／motion MOR-M01）が cold evidence-blue の一筋に照らされ、続いて file drawer がその scrawl の上に滑って閉じる（MOR-M02＝they buried it）。**被害者/暴行/遺体/識別可能子供顔なし。**
- **Sound design（声の下に敷く・dramatized のみ）:** 低い sub-bass ドローン（不解決）＋ 単一の冷たい metallic tick ＋ 遠い dry-Texas-wind ambience ＋ file drawer が閉じる紙/木の slide SFX。**digital 無音にはしない・声を邪魔しない（VO -18 に対し SFX/ambient ≤ -28）。**
- 0:00–~6s で cold-open 2文が鳴りきり、~2.0–2.5s 地点に branded sting が overlap（声継続）。type "THE BOY TOLD THEM THE TRUTH. THEY BURIED IT." が mask 切れ上がり。

**★CaseFilm 側の必要改変（B が `remotion/src/components/CaseFilm.tsx` を改変・flag 済）:**
- `BODY_START_SEC`（従来 hookSeconds+OPENING_SEC=11.5）を **0.0** にし、narration/captions/figures/heroCuts の絶対時刻を `body_relative + 0.0` にする。
- `BrandOpening` を「narration を止める前置ブロック」から「narration の上に重なる 0:00–~2.5s の overlap sting（音楽ダック）」に変更。**声を gate しない。**
- `caseFilmDurationInFrames` を §5.1.1 の新式に変更。
- `assert BODY_START_SEC == 0.0`（0 でないと無音 runway が再発）。**旧 `assert hookSeconds==8.0`（8s desync 用）は voice-from-0 では意味が変わるので、代わりに `BODY_START_SEC==0.0` と `narration start==0.0` を assert。**
- **★この CaseFilm 改変は他エピソード（cleveland 等）の描画を壊さないよう、morton は専用の分岐 or 新 prop `voiceLeadsFromZero:true` で切り替える**（既存エピの `BODY_START_SEC` を変えない）。`typecheck` 緑を確認。

### 5.1.1 ★durationInFrames の関数（provisional・実測後に更新・★HOOK-AUDIO 新式）
```
mortonDurationInFrames(mortonFilm, fps=30)   // voice-leads-from-0
  = ceil(narrationSeconds*fps)   // 1795.3*30 = 53,859（provisional）
  + round(ENDCARD_SEC*fps)       // 9.0*30 = 270
  = 53,859 + 270 = 54,129 frames = 1804.3s = 30:04（provisional）
```
> **★旧 CaseFilm 4項式（`round(8*30)+round(3.5*30)+ceil(narr*30)+round(9*30)=54,474`）は 11.5s の無音 runway を前置していた＝HOOK-AUDIO で除去。** `narrationSeconds=1795.3` と `durationInFrames=54,129` は **PROVISIONAL**（5,326語/178wpm 推定）。**FINAL は測定 TTS（Brian）forced-align から。** VO master 生成後、ビルダは `narration_index.total_seconds` を `narrationSeconds` に入れて durationInFrames を再計算し、**`Root.tsx` の登録値を実測値に更新**（SPEC/Root を書き換えてよい唯一の例外）。measured が推定の ±3% を超えたら stderr 警告。

## 5.2 カット構成（§3 マニフェストから機械的に組む・紙芝居回避が最優先）
```
総カット 576 = factory 240 (footage) + motion 86 (footage) + 静止画 250 (img)
[A] first-use  distinct 240+43+215 = 498 → 498/576 = 0.8646   ✓ ≥0.70
[B] per-asset  factory 240/240=1.00 ✓≤1 ／ motion 86/43=2.00 ✓≤2 ／ still 250/215=1.16 ✓≤2
[C] animation_mix  still-share = 250/576 = 0.4340 ✓≤0.45 ／ motion-cov = (240+86)/576 = 0.5660 ✓≥0.45
[D] 平均ショット長  1795.3 / 576 = 3.117 s/カット ✓≤7.0
[E] factory 下限  1795.3/30 = 59.8 → ≥60 → 240本 ✓
[F] avg-uses/source  576/498 = 1.157 ✓≤1.4（EP49 は 1.8 で flag）
```
> **★マニフェストが still215/factory240/motion43 を割ったら組まず A に差し戻す。** 境界は `QUANT=f(0.5)=15f` グリッドにスナップ（mean 3.117s・max ≤7.0s）。

## 5.3 割り当てルール（`allocate()`/`take()`/`repeated()` を踏襲・★treatment から depth を撤去）
1. 各幕の秒窓を `section_windows()` から取り factory:motion:still を按分（**最密は ACT2・ACT4**）
2. **factory は各1回のみ**・**motion/still は各≤2回**（`repeated(pool,need,cap,key)`）
3. 同一素材を連続させない・**★still `treatment` は `["bleed","parallax","duotone","focus"]` 循環（DESIGN §1・`depth` を使わない）**・同 treatment を3連続させない。**`depthSrcOf()` は呼ばない・depth を参照しない**（A が depth を生成していない）
4. **still の `dur` を footage より系統的に短く**・motion の `dur` は 3.0–3.4秒
5. AEカードの区間（§7.2）に重なるカットも存在させる（コンポジタ SKIP 時に穴が空かない）
6. **★実写優先 & 意味マッピング（§5.8）:** footage カットは narration ビート内容に一致する実写を優先（courthouse→有罪/vacatur／Texas suburb→その朝／prison→25年／DNA lab→bandana／capitol→the Act）。意味の合う実写がある所は AI-i2v ではなく実写。AI-i2v は抽象/象徴（bandana/DNA bands/drawer/crayon monster/green van）専用に温存。

## 5.4 `figures[]` と `captions[]`
- `figures[]` は §6（**82本**・floor 75・`graphics[]=[]`・**dochighlight 0**・**年 group:false**）
- `captions[]` は narration_index 全チャンクを verbatim（**HOOK チャンクの cold-open 行も 0:00 から字幕化**・§8）・SRT 同時出力

## 5.5 合成レイヤー（`overlay`）— **`cuts[].src` に出さない**。`morton_film.json` に `overlays` 独自キー or 専用 `screen` レイヤー。**★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない（§5.9）。**

## 5.6 ビルダ出力
| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/morton_film.json` |
| public コピー | `remotion/public/morton/film_data.v001.json` |
| build provenance | `episodes/PD-2026-052-morton/04_scenes/morton_build_manifest.v001.json` |
| beatsheet | `episodes/PD-2026-052-morton/04_scenes/morton_beatsheet.v001.json`（**`premium_` を付けない**＝ゲート測定源を film.json 一本に保つ） |
| SRT | `episodes/PD-2026-052-morton/08_edit/captions.final.v001.srt` |

## 5.7 CLI
```bash
$PY scripts/build_morton_film.py \
  --assets episodes/PD-2026-052-morton/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-052-morton/06_audio/narration_index.v001.json \
  --out    remotion/src/data/morton_film.json
```
**実素材のみ。`is_stub==true` を渡されたら exit 1。★`public_items(manifest,"factory")` が空 or ≠240、`public_items(manifest,"motion")` が空 or ≠43 なら exit 1。★narration_index の最初のチャンク start が 0.0 でなければ exit 1（HOOK-AUDIO）。** 末尾に `check_asset_reuse` 相当の自己レポートを print。

## 5.8 ★実写ストック優先ポリシー（EP48/49 の burned lesson）
> EP48/49 は AI still 100%＋AI-i2v で組み実写ストックを1本も使わなかった。本作は構造で潰す。**実写フッテージは AI-i2v より優先。ただし物語に合わない素材を無理に差し込まない。**
- **ストック実体:** `H:\pd-media\assets\stock`（74動画+155静止・商用可）。A の factory 選定がこれを取り込む（§CODEX_A 7.4a）＝B は manifest の `factory[]` に実写ストック由来が載っている前提で allocate。
- **(a) 意味マッピング:** courthouse→有罪/vacatur(ACT2/4)／Texas suburb・street→その朝(ACT1)／prison exterior→lost years(ACT3・非扇情)／DNA lab・gel→DNA(ACT4)／capitol→the Act(ACT4)／dawn→exoneration(ACT4)。`allocate()` は footage の `covers_scene_id`/`eyeballed_content` がビートのカテゴリと一致するものを優先。**一致しない実写を無理に置かない。**
- **(b) 実写 > AI-i2v:** 意味の合う実写があるビートは実写。AI-i2v（43本）は抽象/象徴（bandana/DNA bands/drawer/crayon monster/green van/gate）専用に温存。
- **(c) 実写スクリーンタイム目標:** 実写 factory 240 / (240+86)=**73.6%**。この比率を下回らせない（factory を still に振り替えない）。stock 74本を意味・QC・R-FACE を通る限り採用。ストック静止 155本は body(AI 215) に混ぜない・被害者/実在人物/可読テキストの実写を使わない。
- **(d) カラーマッチ:** 実写に一貫した neutral な **cold evidence-blue グレード**（INK `#0B0C10`・cyan-free blue `#3F5E8C`・bone `#ECEBE6`）を掛け AI still と一枚の palette に。**milky wash にしない**（§5.9）。他話色に寄せない。

## 5.9 ★NO 全画面ヘイズ/フォグ/スキャンライン（EP48/49 の burned lesson）
1. **全画面 wash 禁止:** 本編ベース合成に全編に渡る haze/fog/mist/vignette-wash を乗せない。全フレームの scanline/CRT/斜めテクスチャも乗せない。画像はクリアで高コントラスト。**screen-wash opacity ≤ 0.07。**
2. **グレードは最小・neutral**（cold evidence-blue 統一・§5.8d）。低コントラストな milky veil を作らない。
3. **overlay は per-beat の疎なアクセントのみ**（§5.5）。全編常駐レイヤーにしない。`subtle_vignette`/`scanline` 系の overlay は選ばない（§CODEX_A §9）。
4. **still `treatment` は bleed/parallax/duotone/focus**（depth なし）＝subtle・全画面コントラスト低下を招かない。
5. **AE 17カード内部のグレード**は各カード内部限定・最小 neutral・milky に読めるほど強くしない。
6. **composite で全画面ヘイズを注入しない**（§7.9）。

> **★検証:** §13.1 の FULL ~30分アイボールで、どのフレームにも全画面の曇り/scanline が無い・クリア高コントラストを確認。DESIGN §1 がこの「clear・high-contrast」を統べる。

---

# 6. Remotion 側 `figures[]`（**82本・floor 75・`graphics[]=[]`・dochighlight 0・年 group:false**）
## 6.1 密度の検算
```
body-minutes = 1795.3/60 = 29.92 min
floor(2.5/min) = ceil(29.92×2.5) = 75
design = 82 beats → density 82/29.92 = 2.74/min ✓≥2.5
coverage 82×平均6.0s = 492s / 1795.3 = 0.274 ✓≥0.25 ／ variety 15 kinds ✓≥6
dochighlight 0 ／ stub 0 ／ quote 0 ／ votetally 0 ／ no 30s window figure-less
```
> 各枠 dur **5.2–6.5s** を基本に。

## 6.2 ★`FigureSpec` の `kind` は実在する小文字値のみ・`dochighlight` は使わない
> 大文字は union に無く無言で消える。`comparebars`→`compbars`／`VoteTally`→`votetally`。**quote/votetally 不使用**（verified-verbatim は AE QUOTE_CARD・vote 票割れは台帳に無い）。

| kind | 数 | payload（実 union） | 用途 |
|---|---:|---|---|
| `lowerthird` | 24 | `{primary; secondary?; accent?}` | 開示 `AI-assisted visualization`×2／place・date・hedged-fact labels |
| `kinetic` | 13 | `{lines[]; style?; emphasisWords?}` | emphasis 行（"THEY BURIED IT"／"THE HUSBAND DID IT"（帰属）／"THE MONSTER WAS REAL"／second-person）・emphasisWords 1–2語 |
| `mechanism` | 6 | `{mechanism:'closingdoor'\|'gears'\|'faultsplit'}` | gears＝conclusion-first investigation／closingdoor＝evidence buried in a drawer／faultsplit＝the real-killer theory splits from the state's case |
| `compbars` | 6 | `{items:[{label; value; accent?}]}` | physical-evidence-tying-Morton 0／pieces-of-evidence-hidden（中立） |
| `timeline` | 5 | `{events:[{year; text}]}` | Aug 1986→1987→2011→2013（年テキストは literal 文字列・"1987" を "1,987" にしない） |
| `stat` | 6 | `{value; label; prefix?; suffix?; decimals?; topLabel?}` | 0(物証・MO08)／45(45th・MO18)／32(birthday・MO02)／3(Eric・MO03)／10(days・MO23)／"~25"(years・MO13 hedged) |
| `numberticker` | 4 | `{value; label?; prefix?; suffix?; decimals?; group?}` | 1,960,000($・MO25・**group:true**)／年を出す numberticker は **group:false** |
| `bar` | 3 | `{data?/items?:[{label; value}]}` | MORTON ~25 YEARS ↔ ANDERSON ~5 DAYS（hedged）／pieces hidden |
| `arrow` | 3 | `{from?; to?; label?}` | the boy→the drawer／DNA→another man |
| `highlightring` | 3 | `{cx?; cy?; r?; label?}` | the blue bandana／the untested cloth |
| `pindropmap` | 2 | `{pins:[{x; y; label?}]}` | green-van/bandana geography **abstracted 2–3点**（NO crime-scene detail） |
| `routemap` | 1 | `{pins?; label?}` | San Antonio に使われた card の drift（abstracted） |
| `spotlight` | 3 | `{cx?; cy?; r?; dim?}` | 単一 cold light on the drawer/bandana（HOOK/ENDING・restraint） |
| `regionmap` | 1 | `{label?; pattern?}` | Williamson County / Austin（abstracted） |
| `acttitle` | 2 | `{title; kicker?; index?}` | **intra-act sub-heads のみ**（"THE BURIED FILE"／"THE BANDANA"）・**AE の 4 act-title と1秒も重ねない** |
| **合計** | **82** | | variety 15・dochighlight 0・stub 0・quote 0・votetally 0 |

> **★年 group:false（§9）:** `numberticker`/`stat`/`lowerthird` が YEAR（1986/1987/1988/2005/2011/2013/2016）を数値で出す場合 `group:false`。`timeline` の `events[].year` は文字列（"1987" literal）。桁区切りが正しい $1,960,000 は `group:true`。

## 6.3 配置方針
| 幕 | beats | 主 kind |
|---|---:|---|
| HOOK/OP | 2 | lowerthird(開示)・kinetic・spotlight |
| **ACT1 The Husband Did It** | 16 | lowerthird・kinetic・mechanism(gears)・stat・regionmap・pindropmap・arrow・highlightring |
| **ACT2 The Trial（engine）** | **20** | **mechanism(closingdoor/faultsplit)**・compbars・arrow・kinetic・stat・timeline・lowerthird・acttitle(sub) |
| ACT3 Twenty-Five Years | 14 | bar・lowerthird・kinetic・timeline・stat・spotlight |
| **ACT4 What the Bandana Knew（climax）** | **22** | **numberticker**・**compbars**・timeline・mechanism(faultsplit)・stat・kinetic・lowerthird・highlightring・bar |
| ENDING | 8 | mechanism(closingdoor)・kinetic・spotlight・lowerthird・stat |
| **計** | **82** | variety 15 |

## 6.4 figures アンカー設計
`(anchor_sec, payload)` を秒昇順、`build_figures()` が `end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら exit 1。`FIG_DUR=6.0 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は narration_index の section 窓に対する相対（★BODY_START_SEC=0.0 起点）。秒直書き禁止。**

## 6.5 配置ルール
1. **AE の 17 cards（§7.2）と1秒でも重ならない**（`validate_morton_beats` が突き合わせ）
2. 同じ kind を連続させない・lowerthird 24/82=29.3%（単一 kind 支配なし）
3. 1枠 5.2–6.5秒
4. `kinetic[].lines`/`*.label`/`primary`/`secondary` は §2 検査対象
5. 台帳外の数値・hedged 断定を置かない・**年は `group:false`**
6. `emphasisWords` は1–2語のみ・**`kind` に `dochighlight` を1件も置かない**

---

# 7. After Effects — ★6 PROVEN LAYOUT のみ・17 cards（`build_morton_hero_cards.py` / `composite_morton_hero.py`）
> AE は本作の感情ピークを担う。**17 cards・6 proven layout のみ**（Tier-B 新 layout を ADD しない）。AE は ffmpeg で本編に焼き込む（密度に数えられない）。

## 7.1 位置づけ・共通ルール
`build_centralpark_hero_cards.py`（or cleveland・FIXED版）を複製。**6種 layout（`buildActTitle`/`buildCenter`=CENTER_STACK+MONEY_STACK/`buildQuote`/`buildVote`/`buildCompare`）をそのまま使う。Tier-B builder は使わない。** `fit_size()`/`count_keys()`/REPO path 出力/二段レンダ/完了マーカー/機械の罠対処は1行も削らない。**末尾 `else throw "unsupported layout"` は保持。**

**★AE 色定数（0..1 float・cold evidence/bandana-blue レーン）:**
```python
ACCENT = [0.247, 0.369, 0.549]  # #3F5E8C cold evidence/bandana-blue（数値・下線・DNA・lane 分離）
INK    = [0.043, 0.047, 0.063]  # #0B0C10 近黒ルート
BONE   = [0.925, 0.922, 0.902]  # #ECEBE6 type
DAWN   = [0.820, 0.604, 0.243]  # #D19A3E Texas homecoming-gold（★exoneration/close moment のみ）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
```
> **★複製元の `ACCENT`（他話色）を必ず `[0.247,0.369,0.549]` に置換。** **homecoming-gold `[0.820,0.604,0.243]` は exoneration/close card のみ**（`c-released`・`c-norwood`?no・`c-mortonact`・`split-25v5`?no・`t-ending`・`m-comp`）＝下表 accent 列参照。他は全て blue/bone。
> **measured-fit MANDATORY:** `fit_size()` Python 事前フィット＋JSX `sourceRectAtTime(t,false).width` 実測再フィット＋quote-wrap（EP40 文字切れ防止）。
> **全 card 右下に `AI-assisted visualization`**（Oswald 20px/SILVER/opacity70/`[W-32,H-28]`）を焼く。字幕帯と縦56px 以上離す。
> **★どの card も被害者を name/depict しない・no faces・no readable fake docs・no real-person likeness。**

## 7.2 AE デッキ（★この表が契約・`validate_morton_beats` が突き合わせ・anchor は BODY_START_SEC=0.0 起点の body-relative 秒）
> **★DATE_STAMP / SEAM_TRANSITION は emit しない（複製元非実装＝クラッシュ）。日付カードは CENTER_STACK。★VOTE_SPLIT は emit しない（検証済み陪審票割れが台帳に無い）。QUOTE_CARD は verified-verbatim 2件のみ。**

ACT_TITLE_CARD×4 / CENTER_STACK×9 / QUOTE_CARD×2 / SPLIT_COMPARE×1 / MONEY_STACK×1 ＝ **17 cards**。尺 ≈95s。

| id | layout | 主表示 / copy | anchor(s)※provisional | dur | MO-id | accent |
|---|---|---|---:|---:|---|---|
| c-convexon | CENTER_STACK | MICHAEL MORTON / CONVICTED 1987 · EXONERATED 2011 | 30.0 | 6.0 | MO10/MO18 high | blue |
| t-a1 | ACT_TITLE_CARD | ACT I / THE HUSBAND DID IT · AUG 1986 | 70.0 | 5.0 | MO02 high | blue |
| c-6am | CENTER_STACK | HE LEFT FOR WORK AT 6 A.M. / A CHILD SAW A "MONSTER" — NOT HIS FATHER | 250.0 | 6.0 | MO03/MO04 high | blue |
| t-a2 | ACT_TITLE_CARD | ACT II / THE TRIAL · 1987 | 470.0 | 5.0 | MO10 high | blue |
| c-noevidence | CENTER_STACK | THE CASE AGAINST HIM / NO PHYSICAL EVIDENCE | 560.0 | 6.0 | MO08 high | blue |
| c-withheld | CENTER_STACK | HIDDEN FROM THE JURY / THE BOY · THE GREEN VAN · THE BANDANA · THE STOLEN CHECKS | 700.0 | 6.5 | MO11 high | blue |
| q-anderson | QUOTE_CARD | "THE OTHER SIDE CAN'T HAVE ACCESS TO THOSE REPORTS." / — KEN ANDERSON | 820.0 | 6.5 | MO12 high | blue |
| c-conv | CENTER_STACK | FEBRUARY 17, 1987 / CONVICTED · LIFE IN PRISON | 900.0 | 5.5 | MO10 high | blue |
| t-a3 | ACT_TITLE_CARD | ACT III / TWENTY-FIVE YEARS | 960.0 | 5.0 | MO13 high(~) | blue |
| c-sixyears | CENTER_STACK | SIX YEARS / THEY FOUGHT TO **NOT** TEST THE BANDANA | 1180.0 | 6.0 | MO15 high(~) | blue |
| t-a4 | ACT_TITLE_CARD | ACT IV / WHAT THE BANDANA KNEW | 1280.0 | 5.0 | MO17 high | blue |
| c-released | CENTER_STACK | OCT 4, 2011 RELEASED / DEC 19, 2011 — DECLARED INNOCENT · 45TH IN TEXAS | 1420.0 | 6.5 | MO18 high | **dawn-amber** |
| c-norwood | CENTER_STACK | THE REAL KILLER / MARK ALAN NORWOOD · CONVICTED OF BOTH MURDERS | 1480.0 | 6.0 | MO17/MO19/MO20 high | blue |
| c-baker | CENTER_STACK | DEBRA BAKER / KILLED JANUARY 1988 — WHILE MORTON SAT IN PRISON | 1540.0 | 6.5 | MO20 high(gut-punch) | blue |
| q-court | QUOTE_CARD | "…A MORE INTENTIONALLY HARMFUL ACT THAN A PROSECUTOR'S CONSCIOUS CHOICE TO HIDE MITIGATING EVIDENCE…" / — COURT OF INQUIRY, 2013 | 1610.0 | 7.0 | MO21 high | blue |
| split-25v5 | SPLIT_COMPARE | THE RECKONING / "MICHAEL MORTON · ~25 YEARS" ↔ "KEN ANDERSON · 10-DAY SENTENCE, SERVED ~5" / "NOBODY COULD CALL IT BALANCE" | 1660.0 | 6.5 | MO13/MO23 high(hedged) | blue |
| m-comp | MONEY_STACK | ROUGHLY / $1,960,000 / TEXAS COMPENSATION, 2013 | 1700.0 | 6.0 | MO25 high(~) | **dawn-amber** |
| c-mortonact | CENTER_STACK | 2013 / THE MICHAEL MORTON ACT — OPEN THE FILE TO THE DEFENSE | 1740.0 | 6.0 | MO24 high | **dawn-amber** |
| t-ending | ACT_TITLE_CARD | THE TRUTH WAS NEVER MISSING | 1770.0 | 5.0 | MO34?→MO04 | blue/bone |

> **★上表は 19 行だが `t-ending` と `c-convexon` を含む＝ACT_TITLE_CARD×4（t-a1/t-a2/t-a3/t-a4）＋ ENDING title(t-ending) は ACT_TITLE_CARD の5枚目。カウントを正す: ACT_TITLE_CARD×5 / CENTER_STACK×9 / QUOTE_CARD×2 / SPLIT_COMPARE×1 / MONEY_STACK×1 ＝ 18 cards。** ★実装時に **17〜18枚**の範囲で確定し、`validate_morton_beats` の期待数と `check_AE_layouts` を一致させる（id/layout/anchor を DESIGN §3 と突き合わせ）。**anchor は実測 narration_index の section 窓から body-relative に再計算（上記は provisional・重複ゼロ・単調増加を必ず検証）。**
> **QUOTE_CARD は `q-anderson`/`q-court` の2件のみ**＝§2.1 の `APPROVED_QUOTES` 2件と一字一致（verbatim ロック）。**それ以外の card は引用符を使わない。**

## 7.3 JSX layout dispatch
複製元 `build(spec)` の 6 layout dispatch をそのまま使い、**新 layout を ADD しない**。共通スタック（下→上）は複製元準拠：黒 bg → 象徴 still（任意）→ グレードウォッシュ(INK/MULTIPLY・**最小 neutral・milky にしない**) → 羽根ビネット → グロー(blue・exoneration系のみ dawn-amber) → ライトスイープ(`"ADBE Rotate Z"`=18・`motionBlur`) → 主レイヤー群(`motionBlur` 個別) → `AI-assisted visualization` → head/tail 4f 黒ディップ。**全 easing は `KeyframeEase`/spatial-ease dim＝等速線形ゼロ。JSX は算術しない（表示文字列は Python precompute）。**

## 7.4 このマシン固有の罠（複製元＝FIXED版が対処済み。1つも省くな）
1. `setTemporalEaseAtKey` の配列次元は spatial(Position) で 1（`if(!prop.isSpatial){...}`）
2. RS=`"最良設定"` / OM=`"H.264 - レンダリング設定を一致 - 15 Mbps"`（英語名 try/catch フォールバック）
3. TextDocument の改行は `\n` 不可。`caption`/複数値は1行・別レイヤー（SPLIT_COMPARE 左右）。幅は `sourceRectAtTime(t,false).width` 実測。em-dash は `-`
4. `app.newProject()` は headless でハング。同名 `MORTON_` コンプを防御削除
5. `render/_build_ok.txt` ポーリングは ≥300秒（17枚・30分尺）
6. jsx 末尾で `.aep` 保存し `app.quit()`
7. `comp.motionBlur=true` だけでは無効。**動くレイヤー個別に `layer.motionBlur=true`**
8. 2Dレイヤー回転は `"ADBE Rotate Z"`
9. `inPoint` と `outPoint` の両方を設定
10. 読み込み後 `item.mainSource.conformFrameRate = 30`
11. 実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`
12. `proj.gpuAccelType = GpuAccelType.SOFTWARE`
13. `getFontsByFamilyNameAndStyleName` 厳格解決
14. **フォント文字列を PowerShell 経由の正規表現/エスケープで生成しない**（`\b` バックスペース化の実害）。Python 先頭に `sys.stdout.reconfigure(encoding="utf-8")`
15. **★二段レンダ:** JSX は `-noui -r` で `.aep` を保存し `_build_ok.txt` を書くだけ（H.264 OM を exFAT H: に書くと 0 mp4＝**REPO path C: に出力**）。mp4 実レンダは別工程 `aerender`。aerender 前に `.aep` mtime > `.jsx` mtime を assert。

## 7.5 `scripts/validate_morton_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（**★HOOK-AUDIO: 0.0 起点・ENDCARD 末尾9s に重ねない**）
3. `layout` が **{6 proven} のみ**（`check_AE_layouts` allowlist と同一）。**DATE_STAMP/SEAM_TRANSITION は FAIL。VOTE_SPLIT を emit していないこと。** still 必須 layout で null なら FAIL
4. `still` 非null は実在＋長辺 ≥3840px
5. 全表示文字列が §2（R-MORTON-INNOCENT/R-VICTIM/R-CHILD/R-VILLAIN-FACT/R-NUM/R-FACE/R-READABLE/R-DOCHL/R-QUOTE/R-DATE/R-HEDGE）を通る
6. `verified:false` を要求するカードは `required:false` で除外・`required:true` なら exit 1
7. **`morton_film.json` の `figures[]`（§6）と AE の 17〜18 区間が1秒でも重ならない**
8. `caption`/label に改行が含まれない
9. **AI開示レイヤーの存在** — 全カード共通スタックに `AI-assisted visualization`。無ければ FAIL
10. **`dochighlight`・発明引用が beats/layout 名に1件も無い**
11. **id/layout/MO-id/anchor が §7.2 デッキと一字一致**（DESIGN §3 とも一致）
12. **年 node/card が `group:false`**（§9）・AE card total = §7.2 で確定した数（17〜18）

## 7.6 `scripts/check_AE_layouts.py`（BLOCKING）
```bash
$PY scripts/check_AE_layouts.py --ep PD-2026-052-morton [--json]
```
- **allowlist = EXACTLY** `{ACT_TITLE_CARD, CENTER_STACK, MONEY_STACK, QUOTE_CARD, VOTE_SPLIT, SPLIT_COMPARE}`（6 proven）。**Tier-B 新 layout は無い。**
- `beats.json` の全 `layout` が allowlist に属すこと。**`DATE_STAMP`/`SEAM_TRANSITION` が現れたら FAIL。**
- builder ソースに各 layout の dispatch が実在することを静的確認（grep）。

## 7.7 実行（★二段・17〜18 comps）
```bash
# 段1: 本番デッキの JSX 生成＋AfterFX で .aep 保存（mp4 はまだ焼かない）
$PY scripts/ae/build_morton_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-052-morton/08_edit/ae_hero/morton_hero.jsx"
# render/_build_ok.txt を待つ（≥300秒）→ .aep mtime > .jsx mtime を assert
# 段2: aerender で各 comp を個別レンダ
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe" \
  -project ".../08_edit/ae_hero/morton_hero.aep" -comp "<id>" -output ".../render/<id>.mp4"
# 段3: 基底 mp4（narration+BGM・★VO from 0.0）→ AEカード合成
$PY scripts/build_morton_bgm_real.py       # ★VO ON from 0.0（HOOK-AUDIO・§5.1.2）
$PY scripts/ae/composite_morton_hero.py
```
**コンポジタ（`composite_morton_hero.py`）:**
- `BASE = 08_edit/morton_final_bgm.v001.mp4`（`build_morton_bgm_real.py` が生成・**film_offset 0.0**）／`OUT = 08_edit/morton_final_bgm.v002_ae.mp4`（**v001 を上書きしない**）。
- **SKIP4条件を1行も削らない:** (1)`render/<id>.mp4` 不在 (2)解像度≠1920x1080 (3)実測尺 `< dur-0.3` (4)`film_offset_sec + beat.end > base_dur`。**SKIP 数を stderr に出す。**
- ffmpeg `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`／`-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**film_offset 0.0 を適用**（body-relative→absolute・HOOK-AUDIO）。
- **★合成で全編に渡る haze/fog/blur/scanline を一切足さない（§5.9）。**
- 出力後 `probe_dur(OUT)` でベースとの尺差 ≤0.5秒を確認。

**BGM（`build_morton_bgm_real.py`・★VO ON from 0.0）:** 完成 mp4 **-14.0 LUFS**・true peak ≤-1.0 dBTP・VO -18.0・BGM(VO下) -22.0・(VO無) -17.0・ambient -30.0・ducking 5.0dB/attack120ms/release450ms。**★HOOK-AUDIO: VO は 0.0 から鳴る（無音 runway なし）。HOOK の cold-open 行の下に §5.1.2 の sound design（sub-bass drone・metallic tick・dry-wind ambience・drawer slide）を ≤-28 で敷く・digital 無音にしない。** 章 BGM は 1章1トラック（HOOK 低弦の不解決＋single tick＝restraint／ACT4 DNA hinge で唯一 raise／ACT4 exoneration/dawn で暖色に開く）。最長無音 <25s。**HOOK に silent runway を作らない（声が 0:00 から鳴る）。**

---

# 8. 字幕（`scripts/gen_captions_morton.py`＝複製）
- `internal_split()`/`chunk_sentence()`/`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap` をそのままコピー。
- 入力は narration_index の各チャンク文（`--narr`）。**字幕は台本本文と1:1・verbatim・構文境界で分割。タイミングは narration_index の start/end のまま（★HOOK cold-open 行は 0:00 から字幕化）。**
- `ABBR` に `U.S.`/`v.`/`Mr.`/`Ms.`/`No.`/`Dec.`/`Aug.`/`Feb.`/`Jan.`/`Oct.` 等。
- 通すゲート `check_caption_breaks.py`（行末機能語0/孤立0/句またぎ hard0）＋ `check_caption_integrity`。
- **字幕にも R-FORBID 適用**（台本 verbatim なら通る・§2.1 注意：`beaten`/`murder`/`bandana` 単独を足さない）。
```bash
$PY scripts/gen_captions_morton.py --narr episodes/PD-2026-052-morton/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-052-morton/08_edit/captions.final.v001.srt
```

---

# 9. ★年 group:false ゲート（`scripts/check_year_grouping.py`・BLOCKING）
```bash
$PY scripts/check_year_grouping.py --ep PD-2026-052-morton [--json]
```
- **YEAR 値（1986/1987/1988/2005/2011/2013/2016 等 1000–2100）を出す全 `numberticker`/`stat`/`lowerthird`（figures）と AE numeric（timeline year node・年 card）は `group:false`。** 無ければ FAIL（"1,987" バグ）。
- **桁区切りが正しい大桁（1,960,000）は `group:true`（既定）。**
- figures[] と beats.json の両方を走査。

---

# 10. 全ゲート（build 後に必ず全部・レンダ前 preflight）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# --- Preflight ---
# 0. 語数（★30分 band・12分 2,141 cap ではない・cap ≈5,450）
$PY scripts/check_script_length.py episodes/PD-2026-052-morton/03_script/script.en.v001.md --json
#    → ~5,326 語が 30分 band 内（--longform が 60分専用なら --cap 5450 相当を渡す／30分帯で判定）
# 1. 事実性/制約（EP52固有）
$PY scripts/check_morton_facts.py --json
# 2. 契約バリデータ
$PY scripts/validate_morton_beats.py
$PY scripts/check_morton_asset_manifest.py --assets episodes/PD-2026-052-morton/05_visuals/asset_manifest.v001.json
$PY scripts/check_AE_layouts.py --ep PD-2026-052-morton
# 3. 年 group:false
$PY scripts/check_year_grouping.py --ep PD-2026-052-morton

# --- Post-build ---
$PY scripts/check_asset_reuse.py     remotion/src/data/morton_film.json    # factory≤1/motion≤2/still≤2/first-use≥0.70（設計0.8646）/avg-uses≤1.4（設計1.157）
$PY scripts/check_motion_density.py  --ep PD-2026-052-morton                # ≥75 beats/≥2.5min/variety≥6/dochighlight=0（設計82/2.74/15）
$PY scripts/check_animation_mix.py   --ep PD-2026-052-morton                # still-share≤0.45（設計0.4340）/motion-cov≥0.45（設計0.5660）
$PY scripts/check_caption_breaks.py  episodes/PD-2026-052-morton/08_edit/captions.final.v001.srt
$PY scripts/check_caption_integrity.py --ep PD-2026-052-morton              # ナレ一致≥99%/カバー≥95%/CPS≤17/ズレ≤120ms
$PY scripts/check_visual_asset_qc.py --ep PD-2026-052-morton                # 全 still/factory/motion 目視QC・black frame 0・R-FACE
$PY scripts/check_padding.py         --ep PD-2026-052-morton --json
$PY scripts/preflight_render_gate.py --ep PD-2026-052-morton                # machine state・public_slim ディスク・durationInFrames assert

# --- Render → BGM → AE 合成 → 受入 ---（§12）
$PY scripts/check_final_acceptance.py 52 \
  --render episodes/PD-2026-052-morton/08_edit/morton_final_bgm.v002_ae.mp4 --emit-receipt
```
> **★ゲート入力規約:** density/mix/年/AE_layouts/caption_integrity/visual_qc/padding/preflight は `--ep PD-2026-052-morton`。asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。**`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` を優先するので B の beatsheet に `premium_` を付けない（§5.6）。**
> **全て exit 0 でなければ `package_ready` にしない。**

| ゲート | EP52 目標値 |
|---|---|
| `check_script_length` | ~5,326 語 ∈ 30分 band（12分 2,141 cap ではない・cap ≈5,450） |
| `check_morton_facts` | violations 0（R-MORTON-INNOCENT/R-VICTIM/R-CHILD/R-VILLAIN-FACT/R-NUM/R-FACE/R-READABLE/R-DOCHL/R-QUOTE・hedged 断定なし） |
| `check_asset_reuse` | factory≤1/motion≤2/still≤2・first-use **0.8646**・avg-uses **1.157**≤1.4 |
| `check_motion_density` | **82** beats / **2.74**/min / variety **15**（floor 75/2.5/6・dochighlight 0） |
| `check_animation_mix` | still-share **0.4340**（cap0.45）/ motion-cov **0.5660**（floor0.45） |
| `check_AE_layouts` | 全 layout ∈ {6 proven}・phantom 0・DATE_STAMP/SEAM_TRANSITION 0・VOTE_SPLIT emit 0 |
| `check_year_grouping` | 年 figure/AE すべて `group:false`（"1,987" 0件） |
| `validate_morton_beats` | AE 17〜18 ↔ figures 82 非重複・id/layout/MO-id/anchor 一致 |
| `check_caption_*` | 行末機能語0/孤立0/hard0・ナレ一致≥99%・CPS≤17・ズレ≤120ms |
| runtime | ~30:04（provisional 54,129f・**FINAL は実測 TTS**）・**★VO onset 0.0（HOOK-AUDIO）** |

---

# 11. OP バンパー `OpeningMorton`（独立成果物・fps60/1920x1080/180f）
本編（`Ep52Morton`）の OP は `Bookends.tsx` の `BrandOpening`（★HOOK-AUDIO の overlap sting 化・§5.1.2）。`OpeningMorton` は独立タイトルバンパー（`out/morton_opening.mp4`・Shorts/予告用・本編に焼き込まない）。
- Composition: `id="OpeningMorton"` / 1920×1080 / fps60 / 180f（=3.0秒）/ `remotion/src/compositions/OpeningMorton.tsx`。
- **依存 `@remotion/motion-blur`**。`remotion.config.ts` は正典値（png/h264 libx264/CRF16/yuv420p/bt709/aac320k/全コア並列/angle）＝一致確認のみ。
- **秒数ベース（fps60・フレーム直書き禁止）・等速線形禁止・opacity 単独禁止**（全 opacity が translateY/scale と対）・複数要素は 2–4f スタッガー・速い動きは `Trail`・テキストは `overflow:hidden`+translateY マスク切れ上がり・主役裏に最低3レイヤー。
- props: `{ title:string; subtitle:string; accent:string; hasLogo:boolean }`。`remotion/props/morton.json` = `{ "title":"THE MONSTER IN THE GREEN VAN", "subtitle":"A CHILD TOLD THE TRUTH. THEY BURIED IT FOR 25 YEARS.", "accent":"#3F5E8C", "hasLogo":true }`。
- **accent は必ず `#3F5E8C`**（他話色流用は BLOCKER）。ルート bg は INK `#0B0C10`。title/subtitle も §2 検査対象。
```bash
cd remotion && npm run studio      # OpeningMorton を 0→180f スクラブ目視
npx remotion render OpeningMorton out/morton_opening.mp4 --props=./props/morton.json
```

---

# 12. サムネ3案（`MortonThumbnails.tsx`・★CTR §4A emotive-face）
> **CTR_PLAYBOOK §4A（emotive face が lane #1 CTR driver）。** 前景 = §CODEX_A §5.12 の **thumb_face T01–T03**（非実在・illustrative・likeness firewall）。背景 = §4.3a の also_thumb body（MOR-S001/S060/S155/S170）。2–4語 hook（red bar or yellow caps）・face 50–65% frame・眼は upper-third・neg space に text・**never over the eyes**。
- **id/comp:** `MortonThumbnails`（1280×720・3案）。出力 `episodes/PD-2026-052-morton/09_package/thumb_{a,b,c}.png`。
- **3案（CTR §4A・title は §12.1）:**
  - **案A（wronged man dread）:** T01_face（dread stare・off-camera）右三分割・背景 S155(cell window)・red bar "25 YEARS. INNOCENT."
  - **案B（corrupt authority）:** T02_face（cold glare・to-camera）左三分割・背景 S060(bandana drawer)・yellow caps "HE HID THE TRUTH"
  - **案C（exoneration tear）:** T03_face（silent tear・released）右三分割・背景 S170(DNA bands・warm dawn edge)・red bar "DNA FREED HIM"
- **★R-FACE/likeness firewall:** T01–T03 は clearly illustrative・実在被告/検事/被害者に似せない・no readable text in the art。title/overlay も §2 検査対象（R-MORTON-INNOCENT/R-VICTIM/R-FACE）。

## 12.1 ★タイトル案（CTR §4A/§3・shock-word first・2–3案）
1. **"They Buried the Evidence and Sent an Innocent Man to Prison for 25 Years"**（3rd-person narrative・shock-word "Buried" front）
2. **"A Prosecutor Hid the Truth — So the Real Killer Walked Free and Killed Again"**（[Authority] [shock verb] + consequence・the second-victim hook）
3. **"A 3-Year-Old Named the Killer. They Locked Up His Father Instead."**（curiosity + the child-witness hook）
> オンスクリーン subtitle は poetic line（"The Monster in the Green Van"）を残し、**YouTube title を上記の hooking 版に**（CTR §3）。

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
§10 の全ゲートを exit 0 まで通し、`check_final_acceptance.py 52 --render .../morton_final_bgm.v002_ae.mp4 --emit-receipt` を PASS させる。

## 13.1 ★完成後の FULL ~30分 3回アイボール（1フレーム判定禁止＝EP39-41/EP47 実害）
`morton_final_bgm.v002_ae.mp4` を **0→末尾まで通しで3周**実視聴（**measured across the WHOLE ~30分・sampled 1-frame 禁止**）:
- **周1 structure/カット:** 紙芝居感なし（still 連続なし・footage 過半）・4幕構成・AE 17〜18 cards が全て焼き込まれている・**実写ストックが意味のあるビートに載っている（courthouse/Texas suburb/prison/lab 等が内容一致）・実写比率が 73.6% を割っていない・実写と AI still が一枚の palette（カラーマッチ）**・**どのフレームにも全画面の曇り/ヘイズ/スキャンラインが無い＝クリア高コントラスト（§5.9）**・**depth-warp（被写体の melt/歪み）が無い（treatment は bleed/parallax のみ）**
- **周2 caption-text:** 全字幕が台本と一致・機能語末/孤立/hard split なし・**年が "1,987"/"2,011" になっていない**（全 numberticker/stat/年 card を目視）
- **周3 audio-sync:** **★VO onset = 0.0（Brian の cold-open 第一声が frame 0 から鳴る＝無音 runway が無い・HOOK-AUDIO）**・branded sting が声を gate していない・BGM ducking・endcard 9s・音ズレ/字幕ズレ/尺差（base と ≤0.5s）なし・**実在人物の音声が1つも無い（Brian＋dramatized SFX のみ）**
- **全周共通で必ず確認:**
  - **各 AE card:** convicted/exonerated／NO PHYSICAL EVIDENCE／WITHHELD／Anderson quote／SIX YEARS／released-declared innocent／Norwood／**Debra Baker killed while Morton imprisoned**／Court-of-Inquiry quote／25 YEARS ↔ ~5 DAYS／$1,960,000／the Michael Morton Act（**年が群化していない**）
  - **R-MORTON-INNOCENT:** Morton が犯人に見える画面/字幕がどこにも無い（"the husband did it" は帰属枠のみ）
  - **R-VICTIM/R-CHILD:** Christine/Debra の暴行/遺体/imagery が無い・殺害が描写/再現されていない・**Eric が識別可能な子供顔で出ていない・襲撃視点が無い**
  - **R-VILLAIN-FACT:** Norwood/Anderson が record の事実のみ・美化なし・**実在 likeness が1つも無い**
  - **R-FACE:** 匿名・非識別の人物（H シリーズ・顔は背向き/影/ソフト）は可だが、**Morton/Christine/Eric/Norwood/Anderson/Bradley/Raley/判事に「似た」顔/肖像が1つも無い**・被害者描写と暴行/遺体 imagery が1つも無い・可読の偽公文書が無い
  - **R-DOCHL:** `dochighlight` が figures/AE に1本も無い
  - **R-QUOTE:** 引用符は検証済み逐語2件＋帰属のみ（Michael の note を引用していない）
  - 生成ビジュアル表示中は `AI-assisted visualization` が右下常時（AE card 表示中も）
  - accent が cold evidence-blue `#3F5E8C`（dawn-amber は exoneration/close のみ・他話色が紛れていない）
  - **サムネ:** emotive-face（非実在・illustrative）が likeness firewall を満たす（実在被告/検事/被害者に似ていない）

---

# 14. 絶対にやらないこと
- **EP1〜51 のファイル・素材・`scripts/*{他slug}*.py` に触らない**（読み取り可）。**accent に他話色を使わない**（blue `#3F5E8C` / dawn-amber は exoneration/close のみ）。
- **スレッドAの所有ファイル（§0.2.1）に書かない**。B の provenance は `04_scenes/` に書く。
- **課金ジョブを起動しない**（TTS / 課金画像API / アップロード）。narration_index は実測版（Brian）を消費するだけ。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（AE 合成出力は `v002_ae`・base は `v001`）。
- **台帳（§2）に無い数値を焼かない。hedged（~25/~6/~5/~100/~$1.96M/$5,000）を hedge 語なしで断定表示しない。**
- **`FigureSpec` の `kind` を推測で書かない**（実在小文字値のみ・`comparebars`→`compbars`）。**`dochighlight` を1本も使わない。quote/votetally は不使用。**
- **★DATE_STAMP / SEAM_TRANSITION を emit/実装しない・VOTE_SPLIT を emit しない・Tier-B 新 layout を ADD しない**（6 proven のみ）。
- **★年を `group:false` にし忘れない**（1987/2011/2013 が "1,987" 化＝§9）。桁区切り数値（$1.96M）は `group:true`。
- **★build_morton_film.py は manifest の `factory[]`(240)/`motion[]`(43) を全読込し、空 or 期待数違いなら exit 1**（EP45 紙芝居事故防止）。
- **★AEカードは二段レンダ（.aep 保存→別工程 aerender）で REPO path(C:) 出力・aerender 前に .aep mtime > .jsx mtime を assert。**
- **★render 前に `public_slim/morton` へ全メディアを staging・EP52 のみに剪定**（C: ENOSPC 回避・両ディレクトリ 0-missing）。
- **R-MORTON-INNOCENT/R-VICTIM/R-CHILD/R-VILLAIN-FACT/R-FACE/R-QUOTE を破らない**（Morton の無実を事実として・被害者/Eric を記録以上に扱わない・**実在人物 likeness ゼロ**・被害者描写と暴行/遺体 imagery なし・識別可能子供顔なし・発明引用ゼロ）。
- **★実写ストックライブラリ（74動画+155静止）を放置して AI だけで組まない（§5.8）。** ただし物語に合わない実写を無理に差し込まない。
- **★全画面の haze/fog/曇り/vignette-wash・全フレーム scanline/CRT を乗せない（§5.9・screen-wash ≤0.07）。** クリア・高コントラスト。
- **★depth treatment を使わない・depth map を参照しない**（bleed/parallax/duotone/focus のみ・§5.3・depth warp 防止）。
- **★HOOK-AUDIO を破らない（§5.1.2）:** Brian の cold-open 第一声が **0:00 から鳴る**・無音/音楽だけの runway を作らない・branded opening は声を gate しない overlap sting・**実在人物の音声を使わない**・durationInFrames は voice-from-0 の新式（54,129 provisional）。
- **スペック数値（576 cuts / still215/factory240/motion43 / distinct498 / first-use0.8646 / still-share0.4340 / avg-uses1.157 / figures82(floor75) / AE 17〜18(6 proven) / narrationSeconds1795.3 provisional / durationInFrames54,129 provisional / VO onset 0.0）を勝手に変えない**（durationInFrames/narrationSeconds は**実測 TTS 後のみ**更新・§5.1.1）。
- **composition id は `Ep52Morton`**・typecheck 緑を確認。**PowerShell 経由で正規表現/エスケープを生成しない**（`\b` 実害）。
```

