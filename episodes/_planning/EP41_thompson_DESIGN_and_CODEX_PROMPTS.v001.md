# EP41 — THE PAPER THAT COULD NOT SAVE HIM — 制作設計書 ＋ Codex引き継ぎプロンプト（v001・確定台本版）

- Episode ID: `PD-2026-041-thompson` / slug: `thompson` / EP41
- 中心の問い（英語・二人称）: **"If a prosecutor hides the evidence that would set you free, can you make them answer for it?"**
- 判例: **Connick v. Thompson, 563 U.S. 51 (2011)**（5–4 reversal・Thomas 執筆）
- 主役: **John Thompson**（故人・exoneree）。一人の尊厳の物語として。
- リスク区分: **R1**（実在の公人・故人。ただし全実在人物の肖像／認識可能な顔を出さない。実在検察官は法廷記録の認定事実のみ。象徴オブジェで尊厳喪失を描く）
- Status: **BINDING**。**唯一の真実 = 機械生成済み `EP41_thompson_PRODUCTION_SPEC.v001.json`**。本書のあらゆる数値はそこから転記したものであり、手書きで発明していない。衝突したら SPEC が勝つ。

## ★このエピソードの唯一の真実（手書きで数値を発明するな）

`episodes/_planning/EP41_thompson_PRODUCTION_SPEC.v001.json`（台本から機械生成・`scripts/build_production_spec.py`）。この設計書は SPEC を**人間可読な実装指示に翻訳しただけ**であり、新しい数字を作っていない。

```
words_total          = 2,026
narration_seconds    = 682.5   （= 11.4分）
scenes               = 46      （S01..S46・確定。増やすな減らすな）
total_cuts           = 214
still  distinct 80 / cuts 96 / mean 1.2 / cap 2
factory distinct 88 / cuts 88 / mean 1.0 / cap 1
motion distinct 15 / cuts 30 / mean 2.0 / cap 2
distinct_total       = 183
first_use_share      = 0.8551  （floor 0.70）
still_share_of_cuts  = 0.4486  （cap 0.45）
MG beats_floor       = 29      （film.json 側。AEカードは check_motion_density に数えられない）
beats_per_min_floor  = 2.5   /  variety_floor = 3
mean_shot_seconds    = 3.19   /  max_shot_seconds = 6.0
wpm_used             = 178.1
```

## ★EP39/EP40 で踏んだ失敗＝本書が最初から潰す設計判断（要約・詳細は各§）

| # | EP39/40 の失敗 | 本書での恒久対策 | 参照 |
|---|---|---|---|
| 1 | **番号ズレ**（旧番号・別リストを発明） | シーンは **SPEC の S01..S46 に固定**。台本の幕に §3.2 で1:1割当。別の番号体系（`SSxx` 等）を一切作らない | §3.2 |
| 2 | **紙芝居**（EP40 は静止画100%で `animation_mix` FAIL） | **必ず factory実写を混ぜる**。still distinct 80 ＋ **factory実写 88本** ＋ i2v 15本。still-share 44.9% ≤45%・motion coverage 55.1% ≥45% を §5.1 で保証 | §5.1 |
| 3 | **SDXLを全部静止画にした** | SDXLは「この作品固有の絵」だけ（Thompson匿名再現・独房・法廷・証拠ファイル・最高裁）。周辺・情景・繋ぎは factory実写 | §5.3 |
| 4 | **画像プロンプトのパーサ非互換** | `generate_sdxl_4k.py` の `read_prompts()` が読む **2行形式**（`` - `S01.png` `` の次行に `Avoid:`）で書く。§9 に確定プロンプト。読める枚数を `--only` で確認 | §9 |
| 5 | **ファイル名を信じた**（牛が `documents_on_desk`、大聖堂が監視カメラ） | factory選定は `build_footage_contact_sheet.py` で**全88本を目視QC必須**。Codex-A の必須工程 | §5.4 / Codex-A |
| 6 | **AEカードを密度に数えた** | `check_motion_density` は film.json の `graphics+figures+heroCuts` だけ数える。**film.json 側に MGビート 29本以上**を必ず置く。AEの8枠は composite 後なので0カウント | §7 |

---

# 0. 環境・Remotion設定（CLAUDE.md §0 準拠）

## 0.1 本編 `Ep41Thompson` の Composition 設定（★本編の正）

| 項目 | 値 |
|---|---|
| `id` | **`Ep41Thompson`** |
| 解像度 | **1920 × 1080** |
| `fps` | **30** |
| `durationInFrames` | **20850**（= `Math.round(30 × 695.0)`・§3.1 で算出） |
| component | `remotion/src/compositions/Ep41Thompson.tsx`（`CaseFilm` 系を使う場合も可。`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を **import**・fork 禁止） |
| data | `remotion/src/data/thompson_film.json` |

## 0.2 タイトルバンパー `OpeningThompson` の Composition 設定（CLAUDE.md 正典部品準拠）

| 項目 | 値 |
|---|---|
| `id` | **`OpeningThompson`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60** |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `remotion/src/compositions/OpeningThompson.tsx` |

> `OpeningThompson` は**独立したタイトルバンパー成果物**（`out/thompson_opening.mp4`）。本編内OP/EDの正典は `Bookends.tsx`（`BrandOpening`/`BrandEndcard`）であり、`OPENING_SEC=3.5`/`ENDCARD_SEC=9` は変更しない。`OpeningThompson` を本編に ffmpeg で焼き込まない（オーナー承認なしに見え方を変えない）。

## 0.3 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur     # CLAUDE.md 必須依存
```

## 0.4 `remotion.config.ts`（CLAUDE.md §0 正典値・この通りにする）

```ts
import {Config} from '@remotion/cli/config';
import os from 'os';

Config.setVideoImageFormat('png');               // png
Config.setConcurrency(os.cpus().length);         // 全コア並列 concurrency最大
Config.setCodec('h264');                          // H.264 libx264（NVENC 禁止）
Config.setCrf(16);                                // CRF16
Config.setX264Preset('slow');
Config.setPixelFormat('yuv420p');                 // pixelFormat yuv420p
Config.setColorSpace('bt709');                    // colorSpace bt709
Config.setAudioCodec('aac');                      // 音声 aac
Config.setAudioBitrate('320k');                   // 320k
Config.setChromiumOpenGlRenderer('angle');        // GPU=angle
```

> レンダーログで `crf 16 / preset slow / yuv420p / bt709 / aac 320k / libx264` を必ず確認する。

## 0.5 ブランド（`remotion/src/brand.ts` から import・ハードコード禁止）

`brand.ts` の実値（確認済み）: ink `#0A0A0C` / navy `#0B1A2B` / electric `#1F6BFF` / silver `#C8CDD6` / **gold `#E5B53A`（アクセント）** / white `#F5F7FA`。フォント: display Oswald / number Anton / body Oswald。**EP41 のアクセントは gold `#E5B53A`（ブランド・カード/OP/数値で使用）。**

---

# 1. 事実の取り扱い（R1 ACCURACY LOCK・BLOCKING）

## 1.1 確定台本（唯一の正・1バイトも変えない）

```
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP41_thompson_script.en.v001.md
```

**本番配置先:** `episodes/PD-2026-041-thompson/03_script/script.en.v001.md`（上記を**1バイトも変えずにコピー**）。語順・短縮形・句読点の「整形」も禁止（AI臭再発と語数ゲート再計算を招く）。

台本の**幕構成（HOOK / OP / 第1〜4幕 / ENDING）**と、ト書き **〔SILENCE …〕**（2箇所のみ）を正典とせよ。この台本には `【OST:】` も `〔CARD:〕` も存在しない（実測確認済み）。**存在しない演出マーカーを発明しない。** 日付・数値の刻印は §6 AEヒーロービート＋§7 Remotion figures で行う。

## 1.2 R1 ビジュアル拘束（全ショット共通・binding。台本冒頭ト書きと同一）

1. **Thompson を含む全実在人物の肖像／認識可能な顔を出さない。** 後ろ姿・シルエット・顔外し・手元のみ・無人の象徴空間に限る。
2. **実在検察官（Connick / Deegan / Williams / Riehlmann 等）は法廷記録の認定事実のみ。** 人物として画に描かない。行為は象徴で示す。
3. **読める判決文・書類を作らない。** 書類は雰囲気のみ（文字は判読不能・illegible）。血液型 B/O、$14M、5–4 等の**数値は AE/figures のタイポで出す**（書類の中に読ませない）。
4. **象徴オブジェで尊厳喪失を描く:** 閉まる鉄扉／独房の天井／ファイルフォルダ／めくれるカレンダー／空の証人席／空の陪審席／最高裁列柱。
5. **裸の身体検査・流血・遺体を描かない。** 血の付いた布は非グラフィックの象徴に限る。
6. 共通ネガティブ: `real celebrity, recognizable real person, identifiable face, nudity, explicit, gore`。

## 1.3 `accuracy_lock`（EP41固有ゲート・`scripts/check_thompson_accuracy.py` を実装・exit≠0 で出荷停止）

**検査対象:** `03_script/script.en.v001.md` / `remotion/src/data/thompson_film.json` の `figures[].text`・`figures[].lines[]` / `08_edit/ae_hero/beats.json` の `top`/`bottom`/`caption`/`footnote` / `09_package/*` / `remotion/props/thompson*.json` の `subtitle` / `04_scenes/ai_prompts.v001.md`。

| ルール | 内容 |
|---|---|
| **R1-A 中立帰属** | 争点評価は多数意見／反対意見に**中立帰属**。`figures[]` の `QuoteCard` は逐語のみ（要約を引用符に入れない）。Thomas/Scalia の論理は「the majority」、Ginsburg は「the dissent」に帰属する語を伴う |
| **R1-B 断定禁止** | Thompson が**有罪だった／無実だったと断定しない**（台本どおり「2003 再審で not guilty」「血は彼のものではなかった＝type B≠O は認定事実」に留める）。検察官個人を**犯罪者と名指ししない**（"buried"/"hid" は台本の認定事実表現のみ許可） |
| **R1-C 数値の出所** | 画面（AE/figures）に出す数値は §0.5 の確定数値表（§1.4）に**存在するものだけ**。台帳外の数字（罪状の量刑年数・発砲数・具体的損害額など台本にないもの）を出したら FAIL |
| **R1-D 肖像・顔** | `ai_prompts.v001.md` に `portrait / mugshot / face of / likeness of / recognizable` 等が正のプロンプトに出たら FAIL（ネガティブでの使用は可） |
| **R1-E 実名の顔化禁止** | `Thompson / Connick / Deegan / Scalia / Thomas / Ginsburg` の直後60字以内に `face / portrait / likeness / depicted as a man` が出たら FAIL |

**出力:** `09_package/accuracy_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}]}`）。`pass:true` でない限り `check_final_acceptance.py` に進まない。

## 1.4 画面に出してよい確定数値（台本に存在するものだけ。★この表以外を画面に出すな）

| ID | 値 | 台本での表現 | 使用先 |
|---|---|---|---|
| N01 | **New Orleans, 1984 → 1985** | Liuzza 殺害1984・訴追1985 | AE **b01**（LABEL_STAMP） |
| N02 | **type B / type O** | ラボ報告書=B、Thompson=O | AE **b03**（COMPARE） |
| N03 | **fourteen years** | 隠匿14年／死刑囚房14年 | AE **b02**（CENTER_STACK・CT_INT） |
| N04 | **eighteen years** | 収監18年（うち14年死刑囚房） | AE **b04**（CT_INT）／figures stat |
| N05 | **nine years** | Deegan が秘密を抱えた年数 | figures stat |
| N06 | **April 16, 1999 / May 20, 1999** | 処刑期日「設定日」／処刑「予定日」 | AE **b05**（DATE_STAMP・脚注で区別） |
| N07 | **2003** | 再審・not guilty | figures timeline |
| N08 | **$14 million（＋$1 million超の費用）** | 陪審評決 | AE **b06**（CT_MONEY） |
| N09 | **5 to 4** | 最高裁 reversal | AE **b07**（VOTE_SPLIT） |
| N10 | **March 29, 2011** | Connick v. Thompson 判決／口頭弁論 Oct 2010 | figures timeline |
| N11 | **four prosecutors** | 少なくとも4検事が血液型を認識 | AE **b08**（CT_INT） |
| N12 | **563 U.S. 51 (2011)** | 引用形式 | `09_package/description.txt` のみ（本文で読み上げない） |

> **N06 の binding 区別（検証者修正・台本準拠）:** 処刑「予定日」は **1999年5月20日**。**1999年4月16日は州が処刑期日を「設定した日」**であり実施日ではない。b05 の脚注で必ず分離して描く。

---

# 2. 視覚・音響レーンの分離（EP39/EP40 との素材被り回避）

> **EP39（frazier）/EP40（lech）のファイルには一切触らない。読み取りのみ可。** レーンを機械的に分離する。

| 軸 | EP39 frazier | EP40 lech | **EP41 thompson** |
|---|---|---|---|
| 舞台 | 取調室/密室 | 郊外の一軒家/屋外 | **独房・死刑囚房・法廷・最高裁（institutional・閉ざされた石と鉄）** |
| 時間帯 | 夜 | 昼 | **夜明け前の灰色〜夜。単一の実用光（sodium）が1つだけ灯る** |
| 支配的出来事 | 心理的圧迫 | 物理的破壊 | **不作為・沈黙・時間の堆積（14年）** |
| アクセント色 | electric `#1F6BFF` | gold/amber（暖・郊外） | **gold `#E5B53A`（ブランド・カードとタイポのみ）＋ 単一の sodium amber `#C98A3A` の実用光** |
| ベース色 | 深navy/黒 | 昼光の白+コンクリート灰 | **鋼灰 `#2A2E33` + コンクリート `#3A3A3E` + 冷たい青灰の影 + near-black `#0A0A0C`** |
| レンズ感 | 望遠・浅い | 広角・引き | **正対・対称・望遠圧縮（独房の閉塞／列柱の反復）** |
| 楽器 | （EP39側） | ソロピアノ+低弦 | **低弦サステイン + 単音の鉄的パーカッション（鉄扉のロック音）+ 疎なピアノ** |
| 画像保存先 | （EP39側） | `H:\pd-media\assets\ai\lech\` | **`H:\pd-media\assets\ai\thompson\`** |
| Remotion データ | — | `lech_film.json` | **`thompson_film.json`** |
| Remotion コンポ | — | `Ep40Lech` | **`Ep41Thompson`** |
| AE 作業ディレクトリ | — | `.../PD-2026-040-lech/08_edit/ae_hero/` | **`.../PD-2026-041-thompson/08_edit/ae_hero/`** |

**素材被り禁止:** EP39/EP40 と同一の factory clip / AI画像を**1点も**使わない。選定前に `episodes/PD-2026-039-*/` `episodes/PD-2026-040-*/` の `05_stock/stock_ledger*.json` を読み、sha256 の重複を除外（Codex-A §7.7 相当で BLOCKING）。

---

# 3. 尺と構成 — SPEC の値をそのまま使う

## 3.1 全区間タイムライン（★この表が唯一の正）

**算出基準:** SPEC の `narration_seconds = 682.5`（マスター）を film.json の `narrationSeconds` に入れる。ブロック表の各幕秒は SPEC の acts テーブルの実測秒。**秒は fps から算出しフレーム直書き禁止**（fps=30 → frame = `Math.round(30 * sec)`）。

| # | ブロック | 役割 | 語数 | 幕秒（SPEC acts） | 台本指定の沈黙 | 固定尺 |
|---|---|---|---|---|---|---|
| 0 | **HOOK** | `hook` | 57 | 19.2 | **1.8**（"said: no." 後） | — |
| 1 | **BrandOpening** | `opening` | 0 | — | — | **3.50** |
| 2 | **OP ナレ** | `opening` | 65 | 21.9 | — | — |
| 3 | **第1幕** The Choice | `body` | 358 | 120.6 | — | — |
| 4 | **第2幕** The Wait | `body` | 359 | 120.9 | **2.2**（"No motion filed." 後） | — |
| 5 | **第3幕** The Verdict | `body` | 532 | 179.2 | — | — |
| 6 | **第4幕** The Reach | `body` | 259 | 87.3 | — | — |
| 7 | **ENDING**（payoff→CTA） | `ending` | 336 | 113.2 | — | — |
| 8 | **BrandEndcard** | `ending` | 0 | — | — | **9.00** |

### 検算（Codex は必ず自分で再計算して一致を確認）

```
[1] film.json narrationSeconds = 682.5（SPEC マスター。手計算で上書きしない）
    ※ SPEC acts テーブルの幕秒合計 19.2+21.9+120.6+120.9+179.2+87.3+113.2 = 662.3s は
      wpm 178.1 からの推定値。SPEC の headline narration_seconds 682.5 が測定マスターであり、
      差 20.2s は幕間の息継ぎ・〔SILENCE〕内包分。film.json には 682.5 を入れる。

[2] 総尺 = narrationSeconds 682.5 + BrandOpening 3.50 + BrandEndcard 9.00 = 695.0 秒 = 11:35
    （台本指定 〔SILENCE〕1.8+2.2 は測定ナレ 682.5 の内側の無音として計上済み）

[3] caseFilmDurationInFrames = round(30 × 695.0) = 20,850

[4] runtime_band: standard 帯（manifest target 12分・band 11.5–12.5分想定なら 690–750s）
    → 695.0s = 11:35 は 690–750 の内側    ✓ PASS（下限まで +5s。§15 premortem で監視）
```

> **fast端リスク:** wpm 237.4 で読むと本編が band 下限を割る可能性がある。§4.1 の voice speed ピン留め（`speed 1.0` 明示）＋ ナレ生成直後の `measure_vo_wpm` 実測（合格帯 168–190 wpm）で運用側で潰す。**190超は破棄・0.95 で再発注。**

## 3.2 シーン→幕の割当（★SPEC の S01..S46 を固定・別番号を発明しない）

各シーンは narrative beat。214カットは46シーンに分散（平均 4.65カット/シーン）。**source列は各シーンの primary 素材**（still=SDXL / factory=実写 / i2v=モーション）。ambient/繋ぎカットは factory を各シーンに撒く（§5.1）。

| Sid | 幕 | 内容（象徴・R1準拠） | primary |
|---|---|---|---|
| S01 | HOOK | 手が古いファイルから1枚を引き抜く（顔なし・手元のみ） | **still** |
| S02 | HOOK | 独房の鉄扉（閉） | **still** |
| S03 | HOOK | 最高裁ファサード／列柱 | factory |
| S04 | OP | 検察官の無人デスク／"seek justice, not just convictions" の象徴（空の椅子） | **still** |
| S05 | 第1幕 | 陪審席の12の空席（シルエット） | **still** |
| S06 | 第1幕 | 空の証人席 | **still** |
| S07 | 第1幕 | New Orleans 1984 の夜景（引き） | factory |
| S08 | 第1幕 | 事件現場の象徴（無人の街路・回転灯の光） | factory |
| S09 | 第1幕 | 逮捕＝記録の象徴（手元・書類・顔なし） | **still** |
| S10 | 第1幕 | 血の付いた布（非グラフィック・象徴） | **still** |
| S11 | 第1幕 | 「強盗を先に」＝2つの事件ファイルが並ぶ | **still** |
| S12 | 第1幕 | ラボ報告書（判読不能）type B / type O | **still** |
| S13 | 第1幕 | 沈黙する被告（後ろ姿・閉じた口の象徴） | **still** |
| S14 | 第1幕 | 死刑囚房への収監（鉄扉の奥・量刑） | **still** |
| S15 | 第2幕 | 単独房の内部（正対・閉塞） | **still** |
| S16 | 第2幕 | 鉄扉のロックが二度掛かる（金属ディテール） | **still** |
| S17 | 第2幕 | 独房天井が夜明けに灰色へ変わる（グラデ） | **still** |
| S18 | 第2幕 | 死の書類が進む＝めくれるカレンダー | **still** |
| S19 | 第2幕 | 夜の廊下のシルエット（〔SILENCE 2.2s〕の画） | **still** |
| S20 | 第2幕 | Deegan 臨終＝病室の窓（顔なし・1994） | **still** |
| S21 | 第2幕 | 告白が同僚へ渡る＝2つの空の椅子 | factory |
| S22 | 第2幕 | 処刑期日設定＝カレンダー 4/16→5/20 | **still** |
| S23 | 第2幕 | PIが古いファイルを漁る（手元・棚） | **still** |
| S24 | 第2幕 | 見つかった1枚が光の中に | **still** |
| S25 | 第3幕 | 2003 再審の法廷（無人） | factory |
| S26 | 第3幕 | "Not guilty" ＝陪審が戻る空席 | **still** |
| S27 | 第3幕 | 提訴＝Orleans Parish DA の建物 | factory |
| S28 | 第3幕 | $14M 評決（金額の象徴・gavel不使用） | **still** |
| S29 | 第3幕 | 事件が最高裁へ上る＝石段・列柱 | factory |
| S30 | 第3幕 | 最高裁法廷内の9つの席（顔なし） | **still** |
| S31 | 第3幕 | 5–4 reversal ＝分割の象徴 | **still** |
| S32 | 第3幕 | 多数意見のページ（判読不能） | **still** |
| S33 | 第3幕 | 「パターン」の論理＝反復するファイルフォルダ | **still** |
| S34 | 第3幕 | ルイジアナの過去の破棄（記録の棚） | factory |
| S35 | 第3幕 | 反対意見＝空の法廷ベンチ＋ページ | **still** |
| S36 | 第3幕 | Ginsburg 反対の朗読＝無人のベンチ（帰属テロップ） | **still** |
| S37 | 第3幕 | 「4検事が知っていた」＝4つのフォルダ＋天井callback | **still** |
| S38 | 第4幕 | Brady ＝約束の象徴（レシート・検査結果・名前の紙） | **still** |
| S39 | 第4幕 | 陪審が「全て」聞く vs 一室が選んだ分だけ聞く | **still** |
| S40 | 第4幕 | 独房の中から＝机の向こうのフォルダ | **still** |
| S41 | 第4幕 | ファイルを持つ人物のシルエット（good suit・顔なし） | **still** |
| S42 | 第4幕 | 彼が歩き戻った国＝自由だが代償なし | factory |
| S43 | ENDING | 朝の光の中を歩く後ろ姿のシルエット | **still** |
| S44 | ENDING | Resurrection After Exoneration ＝灯る戸口 | factory |
| S45 | ENDING | 「彼の声」＝空の証人席 callback／マイクの象徴 | **still** |
| S46 | ENDING | 夕暮れに点る一つの窓（未解決の余韻） | **still** |

**source 集計:** still-primary 39シーン / factory-primary 7シーン（S03 S07 S08 S21 S25 S27 S29 S34 S42 S44 のうち10…**下記で確定**）。→ §5.1 の素材積算で factory 88本・still 80枚・i2v 15本に展開する（scene-primary はカット全体の一部で、残りは ambient factory で埋める）。

> **factory-primary の確定10シーン:** S03, S07, S08, S21, S25, S27, S29, S34, S42, S44。残り36シーンが SDXL-primary。SDXLプロンプトは**36シーン**に書く（§9）。

---

# 4. 音の4層設計（ナレ / BGM / SFX / 環境音）

## 4.1 ラウドネス・voice（確定値）

| 項目 | 確定値 |
|---|---|
| 統合ラウドネス（完成 mp4） | **-14.0 LUFS**（許容 -16〜-12） |
| True peak | **≤ -1.0 dBTP** |
| ナレ（VO）単体 | -18.0 LUFS 目標 |
| BGM ベッド（VO下・ダッキング後） | **-22.0 LUFS**（無音まで落とさない） |
| BGM ベッド（VO無し区間） | -17.0 LUFS |
| 環境音ベッド | -30.0 LUFS |
| ダッキング | リダクション 5.0 dB / attack 120ms / release 450ms |
| **VOICE_ID** | ElevenLabs `nPczCjzI2devNBz1zQrb` / model `eleven_multilingual_v2` / stability **0.35** / similarity_boost **0.80** / style **0** / speaker_boost **on** / **speed 1.0（明示）** |
| VO実測合格帯 | `measure_vo_wpm` で **168.0–190.0 wpm**。190超は破棄・speed 0.95 で再発注（BLOCKING） |

## 4.2 〔SILENCE〕2箇所の実装（★デジタル無音にしない・`bgm_present` を落とす）

台本の `〔SILENCE …〕` は**ナレの沈黙であって音の沈黙ではない**。

| 位置 | 秒 | 鳴らすもの |
|---|---|---|
| HOOK末 "said: no." 後 | **1.8** | BGM mute。**SFX steel-door tail のみ**（鉄扉の残響）。デジタル無音にしない |
| 第2幕 "No motion filed." 後 | **2.2** | BGM mute。**SFX steel-door tail のみ**（夜の廊下シルエット S19 の画）。デジタル無音にしない |

**最長無音候補 2.2秒 << 25秒** ✓ `bgm_present` PASS。両区間とも steel-door tail のリバーブベッドを残す。

## 4.3 章ごとのBGM（1章1トラック・8カテゴリ）

| 区間 | 性格 | 楽器 |
|---|---|---|
| HOOK | 低弦の不解決・17秒から単音ピアノ | 低弦 |
| OP | ブランドスティンガー（`BrandOpening` 付属） | — |
| 第1幕 | 冷たい持続音・鉄的パーカッションが不作為を刻む | 低弦+メタル |
| 第2幕 | 疎なピアノ・時間の堆積。ロック音の反復 | ピアノ+メタル |
| 第3幕 | 法の機械性・僅差の緊張 | 低弦+メタル |
| 第4幕 | 二人称の射程・室内的で近い | ピアノ+弦 |
| ENDING | 解決しない和音 →「his voice」でだけ開く | ピアノ+弦 |
| ENDCARD | ブランドED（`BrandEndcard` 付属） | — |

## 4.4 SFX

| 種別 | 位置 | 音 |
|---|---|---|
| steel-door lock | 全編モチーフ（S16・〔SILENCE〕2箇所） | 鉄のロックが座る音・-14 LUFS |
| impact | AE b02/b06/b07 の数値着地 | 低域インパクト・-12 LUFS |
| tick | カウントアップの桁変化 | 微細クリック・-24 LUFS |
| paper | 報告書・カレンダー・フォルダのカット | 紙擦れ・-22 LUFS |
| room tone | 全編ベッド（独房・法廷の反響） | 石の広いリバーブ・-30 LUFS |

---

# 5. ビジュアル — 素材積算（★紙芝居回避＝factory実写を必ず混ぜる）

## 5.1 素材の積算（★SPEC の値をそのまま満たす配分）

```
[0] 絵が必要な区間
    695.0 − BrandOpening 3.50 − BrandEndcard 9.00 = 682.5 秒

[1] 総カット数 = 214（SPEC）
    682.5 / 214 = 3.19 秒/カット          ✓ mean_shot_seconds 3.19（SPEC 一致・≤6.0）

[2] 素材の内訳（★SPEC の distinct/cuts をそのまま）
    still（SDXL）     80 distinct →  96 カット（16枚が2回・64枚が1回・mean 1.2・cap 2）
    factory 実写      88 distinct →  88 カット（各1回・cap 1）
    i2v モーション    15 distinct →  30 カット（各2回・cap 2）
    ------------------------------------------------
    distinct 合計    183           → 214 カット

[3] first-use share = 183 / 214 = 0.8551   ✓ ≥0.70（SPEC first_use_share 一致）
[4] footage_diversity distinct/total = 0.8551   ✓ ≥0.40
[5] 同一素材の最大使用回数: still 2 / factory 1 / motion 2   ✓ 各 cap 内
[6] 静止画占有率（★紙芝居ゲート check_animation_mix の要）
    still-cuts 96 / 214 = 0.4486 = 44.9%    ✓ ≤45%（SPEC still_share_of_cuts 一致・余裕 0.14%）
[7] motion coverage（動画カットの割合）
    (factory 88 + i2v 30) / 214 = 118/214 = 55.1%   ✓ ≥45%
    → EP40 の「静止画100%で animation_mix FAIL」を構造的に排除
[8] factory 下限 = 682.5/30 = 22.75 → ≥23本。設計値 88本   ✓（7.76秒に1本）
```

> **[6] の余裕は 0.14% しかない。** still-cut を1つでも増やすと 45% を割る。**still-cut は 96 で固定**（16枚だけ2回・残り64枚1回）。QCで still が80枚を割ったら §9 の追加生成で回復させ、cut数を増やさない。

## 5.2 SDXLと実写在庫の振り分け（★どのシーンをどちらで作るか）

- **SDXLで作る = この事件にしか無い固有物**（§3.2 の still-primary 36シーン）: Thompson の匿名再現・独房・鉄扉・独房天井・空の陪審席/証人席・血の布・ラボ報告書（判読不能）・フォルダ・最高裁法廷内・反対意見のベンチ・朝の光のシルエット。
- **実写在庫で足りる = どこにでもある周辺**（factory-primary 10シーン ＋ ambient）: New Orleans 夜景・institutional 建物外観・石段・列柱・廊下・棚・空の椅子・記録庫・戸口・空・光の移ろい・石とコンクリートのテクスチャ。

## 5.3 SDXL 生成量（★全部を静止画にするな）

- SDXLプロンプト: **36シーン**（still-primary）× **`--variants 3`** = **108枚 pool**（§9）。
- 選抜: **80 distinct body still**（各シーン `_01`/`_02` の2枚 ×36 = 72＋強シーンの `_03` から8枚 = 80）＋ **15 i2v-source**（動きが意味を持つシーンの `_03`）＋ サムネ/予備。
- **factory実写 88本**は SDXL で作らない（Codex-A §7 で在庫11,443本から選定・目視QC）。

## 5.4 factory のファイル名を信じない（★EP41 の必須工程）

> **EP36:** `city_surveillance_camera_dome` が実際は大聖堂。**EP38:** 牛が `documents_on_desk`。ラベルは「その検索語で取った」記録であって中身の保証ではない。

選定した **88本すべて**を `scripts/build_footage_contact_sheet.py --ep PD-2026-041-thompson --media video --dir <factory staging>` で**1本1フレーム**のラベル付きコンタクトシート（`runs/qc/thompson_footage_contact_NN.png`）にし、**全点を目視**。中身が subtype と食い違う本は差し替える。Codex-A の必須工程（BLOCKING）。

## 5.5 共通スタイル接尾（各SDXLプロンプト末尾に必ず付ける・§9 の `[STYLE]`）

```
, cinematic still, cold desaturated institutional grade, steel grey and concrete with near-black shadows, a single warm sodium practical light as the only warmth, faintly blue-grey cold shadows, deep shadow detail retained, telephoto compression and frontal symmetry, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo
```

> **EP39/EP40 との分離:** 接尾に `navy`, `electric blue`, `interrogation`（EP39）や `midday sunlight`, `suburban`, `bleached daylight`（EP40）を**一切含めない**。

## 5.6 共通ネガティブ（各SDXLプロンプトの `Avoid:` に必ず付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible court paper, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, cartoon, illustration, 3d render, low quality, blurry, deformed, extra limbs, nudity, explicit, gore, blood pool, corpse, midday suburban daylight, electric blue interrogation
```

## 5.7 AI開示（強め・毎回）

AI生成の静止画・i2v が画面に出ている間、常時、右下に **`AI-assisted visualization`**（破壊/再現度の高い画は **`Artistic reconstruction — AI-assisted`**）。Oswald系 20px / `#C8CDD6` / opacity 70% / 位置 `[W-32, H-28]` 右下。字幕帯と縦 56px 以上離す。概要欄にも1行: `Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.`

---

# 6. After Effects ヒーロービート（8枠）— ★AEカードは密度に数えられない

## 6.1 大原則（★EP39/EP40 の致命傷を回避）

`check_motion_density` は **film.json の `graphics+figures+heroCuts` だけ**を数える。**AE の 8枠は本編mp4に composite された後に焼き込まれる**ため、gate は 0 としてカウントする。→ **密度の下限 29 は §7 の Remotion figures/graphics で満たす。** AE はその上に載る「決め所の数値タイポ」であり、密度要件の充足源にしない。

## 6.2 パイプライン（EP38/EP40 で measured 済み）

```
[1] Remotion で本編を完成 → thompson_final_bgm.v001.mp4（音声ミックス済み）
[2] scripts/ae/build_thompson_hero_jsx.py が beats.json と thompson_hero.jsx を生成
[3] AfterFX -noui -r thompson_hero.jsx → 各ビートを 1920x1080@30fps の不透明 mp4 で書き出し
[4] scripts/ae/composite_thompson_hero.py が ffmpeg overlay + enable='between(t,start,end)' で焼き込み
[5] 出力 → thompson_final_bgm.v002_ae.mp4（v001 は絶対に上書きしない）
```

## 6.3 スロット確定表（§1.4 の確定数値のみ・8枠）

| ID | 内容 | 数値ID | レイアウト | カウント型 | 尺 | 対応する台本の行 |
|---|---|---|---|---|---|---|
| **b01** | 事件の年 | N01 | **LABEL_STAMP** | なし | 5.0 | "New Orleans, 1984. … Early in 1985 … John Thompson." |
| **b02** | 死刑囚房14年 | N03 | **CENTER_STACK** | `CT_INT` | 6.5 | "Fourteen years is not a number when you are the one inside it." |
| **b03** | 血液型 B ≠ O | N02 | **COMPARE_STRIKE** | なし | 7.0 | "type B. John Thompson's blood is type O." |
| **b04** | 消えた18年 | N04 | **CENTER_STACK** | `CT_INT` | 6.5 | "eighteen years, gone." |
| **b05** | 処刑期日 | N06 | **DATE_STAMP** | `CT_DATE` | 6.5 | "the sixteenth of April, 1999 … marks it for the twentieth of May." |
| **b06** | $14M 評決 | N08 | **CENTER_STACK** | `CT_MONEY` | 7.0 | "They award John Thompson fourteen million dollars" |
| **b07** | 5 対 4 | N09 | **VOTE_SPLIT** | なし | 7.5 | "Five to four. The Court reverses. Every dollar, gone." |
| **b08** | 4人が知っていた | N11 | **CENTER_STACK** | `CT_INT` | 6.0 | "Four prosecutors knew the blood was not his. Four." |

### 検算

```
[1] 単調増加・重複ゼロ（start は §6.4 の beats.json で幕位置に配置。台本行の秒に一致させる）
[2] HOOK / BrandOpening / ENDING payoff / BrandEndcard に1秒も重ならない
[3] 合計 = 5.0+6.5+7.0+6.5+6.5+7.0+7.5+6.0 = 52.0秒 / 695.0 = 7.5%   ✓ 過剰でない
[4] レイアウト種類 = LABEL_STAMP, CENTER_STACK, COMPARE_STRIKE, DATE_STAMP, VOTE_SPLIT = 5種   ✓ ≥3
[5] figures[] 30枠と1秒でも重ならないこと（validate_thompson_beats.py が両方を突き合わせ）
```

## 6.4 `beats.json`（`08_edit/ae_hero/beats.json`・`schema_version: "thompson_beats.v1"`）

EP40 §9.3 と同一スキーマ（`id ^b0[1-8]$` / `layout` / `count_type` / `num_id`（§1.4 に無い ID は exit 1） / `start`/`end`/`dur` / `still`（本編同区間と別物・長辺≥3840） / `top`/`bottom`（全大文字・§1.3 検査対象） / `caption`（1行・改行禁止・≤50字） / `footnote`（≤44字・null可） / `value`/`value_b`/`decimals`/`thousands`/`prefix`/`suffix` / `numKeys`（Python が全事前計算・JS で整形しない） / `head`/`tail`=4/30 / `out`）。

**確定ラベル（ASCII のみ・em-dash 禁止・§6.6 罠13）:**
```
b01 LABEL_STAMP  top="THE CITY WANTED AN ANSWER"  main="NEW ORLEANS 1984-1985"  bottom=null
b02 CENTER_STACK top="ON DEATH ROW"        value=14 suffix=" YEARS"  bottom="MORNING AFTER MORNING"
b03 COMPARE_STRIKE top="THE CRIME LAB HAD ALREADY TYPED IT"
        left="THE BLOOD: TYPE B"  right="THOMPSON: TYPE O"  bottom="IT WAS NEVER HIS"
b04 CENTER_STACK top="WHAT THE STATE TOOK"  value=18 suffix=" YEARS"  bottom="GONE"
b05 DATE_STAMP   top="LOUISIANA SET THE DATE"  value=1999
        bottom="EXECUTION SET FOR MAY 20"  footnote="DATE SET APRIL 16 - NOT THE DAY OF EXECUTION"
b06 CENTER_STACK top="A JURY OF CITIZENS AWARDED"  value=14000000 prefix="$" thousands=true
        bottom="ONE FIGURE FOR EIGHTEEN YEARS"
b07 VOTE_SPLIT   top="THE SUPREME COURT"  left="4"  right="5"  bottom="REVERSED - EVERY DOLLAR GONE"
b08 CENTER_STACK top="INSIDE ORLEANS PARISH"  value=4 suffix=" PROSECUTORS"  bottom="KNEW THE BLOOD WAS NOT HIS"
```

> **b07 の帰属:** "THE SUPREME COURT" の後は `reversed`（起きた事実）であり、多数/反対の評価語は入れない。§1.3 R1-A。
> **b03/b05 は数値を書類に読ませない**（§1.2）。タイポとして出す。

## 6.5 レイアウト定義（EP40 §9.4 を踏襲・色定数のみ EP41 値）

**共通レイヤースタック（下→上）:** L9 黒ソリッド → L8 静止画（scale fill→fill×1.08・position drift）→ L7 グレードウォッシュ（**冷色** `addSolid([0.10,0.12,0.14])` / MULTIPLY / opacity 30）→ L6 羽根付き楕円ビネット → L5 グロー（下中央 sodium ランプ ADD）→ L4 ライトスイープ（`"ADBE Rotate Z"`=18）→ L3 上ラベル（Oswald）→ L2b アクセントライン（GOLD・scaleX ワイプ・`motionBlur=true`）→ L2 主数値（Anton・GOLD・`motionBlur=true`）→ L1b 下ラベル → L1 字幕ロワーサード → L0 黒シームディップ（head/tail 各4フレーム）。

**色定数（0..1 float）:**
```python
GOLD   = [0.898, 0.710, 0.227]   # #E5B53A — ブランドアクセント（数値・下線）
WHITE  = [0.961, 0.969, 0.980]   # #F5F7FA
SILVER = [0.784, 0.804, 0.839]   # #C8CDD6
SODIUM = [0.788, 0.541, 0.227]   # #C98A3A — 単一実用光のグロー
STEEL  = [0.165, 0.180, 0.200]   # #2A2E33 — ウォッシュ/ビネット寄り
RED    = [0.780, 0.290, 0.250]   # COMPARE_STRIKE の取り消し線のみ
```

**フォント:** 数値 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**（`C:\Users\aab15\AppData\Local\Microsoft\Windows\Fonts\Anton.ttf` / `Oswald.ttf`）。EP38 と同じ `psName()` ランタイム解決で無言の代替置換を防ぐ。

**カウント型:** `CT_INT`（decimals 0 / thousands false）/ `CT_MONEY`（thousands true / prefix "$"）/ `CT_DATE`（**thousands false 必須**。`1,999` と出たら即バグ）。全キーを Python が事前計算（ease-out cubic・最後に正確値へ settle）。カウント終了から区間終端まで最低 1.20秒ホールド（割ったら `build_thompson_hero_jsx.py` は exit 1）。

## 6.6 このマシン固有の罠（★プロンプトに明記・1つ忘れると無言で品質が落ちる）

| # | 罠 | 正しい対処 |
|---|---|---|
| 1 | **フォント解決が例外を投げる**（`allFonts[i]` はラッパー） | AE 2026 の `app.fonts` は Font オブジェクトのラッパー配列。`allFonts[i]` を直接 postScriptName として使わず、`psName()` で `.postScriptName` を安全に取り出す。存在しなければ try/catch で既定へフォールバックし、無言の代替置換を検出してログに残す |
| 2 | **イーズが無言で効かず等速になる**（spatial 次元） | `setTemporalEaseAtKey` の配列次元は spatial プロパティ（Position）では **1個**。`var dim = prop.isSpatial ? 1 : (prop.value instanceof Array ? prop.value.length : 1);` |
| 3 | **テンプレート名が英語だと失敗**（OM/RS ローカライズ名） | AE 2026・日本語ロケール。RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**。英語名は try/catch のフォールバックに置くだけ |
| 4 | **`app.newProject()` が headless でハングする** | `-noui` では保存プロンプトで固まる。**使うな。** 既存の同名コンプを防御的に削除: `for(i=numItems;i>=1;i--) if(item instanceof CompItem && name.indexOf("THOMPSON_")===0) item.remove();` |
| 5 | **`layer.motionBlur` を個別に立てないと効かない** | `comp.motionBlur=true` だけでは無効。動かすレイヤー個別に `layer.motionBlur=true`（数値・アクセントライン・取り消し線・VOTE列） |
| 6 | **`"ADBE Rotation"` が null** | 2Dレイヤーの回転は **`"ADBE Rotate Z"`**（ライトスイープ18度） |
| 7 | **改行文字が literal 表示** | TextDocument の改行は `\n` ではない。`caption` は1行に保つ（≤50字）。COMPARE の2値は**別レイヤー**にする |
| 8 | **em-dash / 全角記号が豆腐化** | ラベル・条項は **ASCII のみ**。`—` は `-` に置換（§6.4 の b05/b07 参照） |
| 9 | **inPoint だけ設定すると尻が残る** | `inPoint` と `outPoint` の両方を設定する |
| 10 | **画像シーケンスの fps が30にならない** | 読み込み後に `item.mainSource.conformFrameRate = 30;` |
| 11 | 実行パス | `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe` / `aerender.exe` |
| 12 | GPU | RTX4090 だが **ソフトウェアレンダで固定**（`proj.gpuAccelType = GpuAccelType.SOFTWARE`・EP38 で実証） |
| 13 | ビルドが遅く早期killしてしまう | ビルド ~100–120秒。jsx 末尾が書く完了マーカー `render/_build_ok.txt` をポーリング。タイムアウト最低300秒。デタッチ起動＋出力ポーリング。jsx 末尾で必ず `app.quit()` |

## 6.7 コンポジタ（`scripts/ae/composite_thompson_hero.py`・SKIP 4条件を1つも削らない）

`BASE = thompson_final_bgm.v001.mp4` / `OUT = thompson_final_bgm.v002_ae.mp4`（v001 不変）。SKIP: (1) `render/<id>.mp4` 不在 → SKIP / (2) 解像度≠1920x1080 → SKIP / (3) 実測尺 `< dur-0.3` → SKIP / (4) `beat.end > base_dur` → SKIP。ffmpeg: `overlay=0:0:eof_action=pass:enable='between(t,start,end)'` / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**出荷済みを絶対に上書きしない。**

---

# 7. Remotion MGビート — ★密度下限 29 は必ずここで満たす

## 7.1 密度の設計（`thompson_film.json` の `figures[]` ＋ `graphics[]`）

`check_motion_density`（実装確認済み）: 3つを AND で満たす。**body-minutes = narrationSeconds/60 = 682.5/60 = 11.375**。

| 指標 | floor | EP41 設計値 |
|---|---|---|
| density | ≥2.5/min | figures 30 + graphics 3 = **33 beats / 11.375 = 2.90/min** ✓（SPEC beats_floor 29 に対し +4 の余裕） |
| coverage | ≥0.25 | 33 beats × 平均 6.0秒 = 198秒 / 682.5 = **0.29** ✓ |
| variety | ≥3 distinct forms | **8種**（下記） ✓（EP36 williams の variety 1 FAIL を回避） |

> **AE の 8枠は film.json に入れない**（composite 後に焼くため gate に数えられない）。**density は Remotion 側 33 beats だけで 29 を超える。** これが EP39/EP40 の「AEカードに頼って density FAIL」の恒久対策。

## 7.2 `figures[]` の種類配分（★同一 kind を連続させない・EP36 の1種反復を禁止）

| kind | 枠数 | EP41 での用途 |
|---|---|---|
| `acttitle` | 4 | 第1〜4幕の幕頭 |
| `timeline` | 5 | 1984→1985 訴追／1994 Deegan告白／1999 期日設定→PI発見／2003 無罪／2010 弁論→2011/3/29 判決 |
| `stat` | 6 | nine years（Deegan）・eighteen years・four prosecutors・約1か月・four prior reversals・fourteen years callback |
| `quote` (QuoteCard) | 6 | ①Thomas「trained lawyers … you need more than that」②Scalia「a deliberate, dishonest act by one man」③Ginsburg「pervasive, standard operating procedure」④Brady の定義⑤修正第14条デュープロセス系の逐語（台帳内）⑥"a dissent frees no one and pays no one"（台本逐語） |
| `compbars` | 3 | robbery-first の弾劾戦術／多数意見 vs 反対意見の争点／type B vs type O |
| `votetally` | 2 | 5–4 の可視化（AEの b07 と別区間）／4 prosecutors knew |
| `numberticker` | 2 | 14 years・$14M（AE と別区間の副次表示） |
| `pindropmap` | 2 | New Orleans / Orleans Parish / Washington（判決地）の位置関係 |
| **合計** | **30** | variety = 8種（`quote/timeline/stat/compbars/votetally/numberticker/pindropmap/acttitle`）≥3 ✓ |

`graphics[]`（kinetic typography）3枠: 幕タイトルの語同期切れ上がり等。→ variety に `kinetic` が加わり 9種。

## 7.3 配置ルール

1. **AEの8区間（§6.3）と1秒でも重ならない**（`validate_thompson_beats.py` が両方突き合わせ）。
2. 幕あたり配分: 幕1=6 / 幕2=6 / 幕3=9 / 幕4=5 / ED=4（幕3が最長 179.2s なので厚め）。
3. **同じ kind を連続させない。**
4. 1枠 4.0–8.0秒。
5. 幕3の説明区間に `compbars`＋`quote`＋`timeline` を分散し 20秒超の平坦区間をゼロに。
6. `quote` の引用は**逐語のみ**（§1.3 R1-A・要約を引用符に入れない）。争点は多数/反対に中立帰属。
7. `figures[].text`/`lines[]` は `accuracy_lock` 検査対象。

## 7.4 密度の最終検算

```
Remotion figures 30 + graphics 3 = 33 kinetic beats（film.json 内）
  density  = 33 / 11.375 = 2.90/min      ✓ ≥2.5（SPEC beats_floor 29 → 33 で +4）
  coverage = 198s / 682.5 = 0.29         ✓ ≥0.25
  variety  = 9 forms                     ✓ ≥3
AE hero 8枠は composite 後・gate 非カウント（上乗せの決め所）
```

---

# 8. レイヤー構成 と ゾーン分離（CLAUDE.md「主役の裏に最低3レイヤー」）

## 8.1 本編カットのレイヤー構成（下→上・6レイヤー）

| L | 名前 | EP41 の値 |
|---|---|---|
| **L0** | ルート背景 | `#0A0A0C`（ink） |
| **L1** | グラデ背景 | `radial-gradient(120% 120% at 50% 40%, #2A2E33 0%, #14171B 45%, #0A0A0C 100%)`（鋼灰） |
| **L2** | グリッド/ライン | 縦横 64px の反復線＋放射マスク＋ドリフト。`repeating-linear-gradient(0deg/90deg, #E5B53A18 0px 1px, transparent 1px 64px)`、`translateY 0→48px` / `Easing.inOut(Easing.sin)` |
| **L3** | グロー | 単一 sodium 実用光。`radial-gradient(closest-side, #C98A3A66 0%, #C98A3A18 45%, transparent 75%)`、`filter: blur(28px)` |
| **L4** | 主役（still / i2v / factory） | §11 のモーション（Ken Burns/parallax/i2v） |
| **L5** | テロップゾーン（上/中央） | §8.2 |
| **L6** | 字幕ゾーン（下部帯） | §8.2 |

> **主役（L4）の裏に L1/L2/L3 = 3レイヤー**（グラデ背景・グリッド/ライン・グロー）で CLAUDE.md 要件を満たす。

## 8.2 ゾーン分離（一度も重ねない）

| ゾーン | 縦位置（1080基準） | スタイル |
|---|---|---|
| テロップ見出し | `y=96–260` | Oswald 64px / `#F5F7FA` / letterSpacing 4 |
| 中央テロップ / figures | `y=420–660` | §7 |
| 出典テロップ（金ライン） | `y=742–786` | Oswald 28px / 金 `#E5B53A` 3px 下線 |
| 字幕帯 | `y=872–1010` | 白 `#FFFFFF` + `textShadow:0 0 6px #000,0 2px 4px #000` / 半透明黒帯 `rgba(6,8,12,0.62)` / ≤2行・1行≤42字 / 54px / lineHeight 1.28 |
| AI開示 | `y=1024–1052`（右下） | Oswald 20px / `#C8CDD6` / opacity 70% |

**Caption QC:** ナレ一致 ≥99%（faster-whisper 強制アライン）/ `.srt` カバー ≥95% / キュー 1.0–6.0秒 / CPS ≤17 / 単語割り禁止 / 1語孤立キュー禁止 / ズレ ≤120ms。〔SILENCE〕区間には**字幕キューを置かない**。

---

# 9. 画像プロンプト（★`generate_sdxl_4k.py` の `read_prompts()` が読む2行形式）

## 9.1 パーサ契約（★この形式でしか読めない・実装確認済み）

`read_prompts()` の正規表現は `^\s*-\s+`([^`]+\.png)`\s*$`。つまり:
```
- `S01.png`
<positive prompt> Avoid: <negative>
```
- **1行目:** `` - `S01.png` `` （バッククォート囲み・行末は `.png` の直後で終わる。プロンプトを同じ行に書かない）
- **2行目:** 正のプロンプト本文 → `Avoid:` → 負のプロンプト（`Avoid:` の前が pos、後が neg。neg は `DEFAULT_NEG` に自動連結される）
- 配置先: **`episodes/PD-2026-041-thompson/04_scenes/ai_prompts.v001.md`**（`generate_sdxl_4k.py` はこのパスを読む）
- 生成: `.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-041-thompson --variants 3`（または `41 --variants 3 --only S07`）
- 出力: `H:\pd-media\assets\ai\thompson\S01.png / S01_02.png / S01_03.png`（媒体）＋ `remotion/public/thompson/`（自動コピー）。長辺 ≥3840 で冪等スキップ。
- **読める枚数の確認手順:** 書いた直後に `--only S01` で1枚だけ回し、ログの `shots=` が **36**（SDXL-primary 36シーン）になっていることを確認。36 未満なら2行形式が壊れている（バッククォートや `Avoid:` の欠落）。

`[STYLE]` = §5.5 の共通スタイル接尾。`Avoid:` の後 = §5.6 の共通ネガティブ。**各行の正プロンプト末尾に `[STYLE]` を必ず連結。**

## 9.2 確定プロンプト（SDXL-primary 36シーン・§3.2 の Sid に1:1対応）

> 以下を `ai_prompts.v001.md` にそのまま書く。`[STYLE]` は §5.5 を、`Avoid:` 後半は §5.6 を各行に展開する（下記では簡潔化のため `[STYLE]`/`[NEG]` と表記。実ファイルでは全文を貼る）。R1: 全て顔なし・象徴・判読不能。

```
- `S01.png`
Extreme close-up of one anonymous adult hand, cropped at the wrist, pulling a single sheet of paper from a thick aged case file in a cold pool of light, the page text completely illegible, deliberate and quiet, no face [STYLE] Avoid: [NEG]
- `S02.png`
A single closed steel cell door seen head-on in dim institutional light, heavy rivets and a small slot, cold grey metal against near-black, the finality of a lock, no people [STYLE] Avoid: [NEG]
- `S04.png`
An empty prosecutor's office at night, a bare wooden desk and one empty chair under a single sodium lamp, an unopened case file squared on the blotter, impersonal and institutional, no people, no readable text [STYLE] Avoid: [NEG]
- `S05.png`
An empty jury box of twelve vacant wooden seats in a dim courtroom, frontal symmetry, long shadows across the rail, the weight of twelve absent strangers, no people [STYLE] Avoid: [NEG]
- `S06.png`
An empty witness stand beside the judge's bench in cold courtroom light, a microphone turned away, the vacant seat where a voice would go, no people, no readable text [STYLE] Avoid: [NEG]
- `S09.png`
Close-up of anonymous hands and a booking desk, a manila folder and an ink pad in hard side light, the machinery of a record being made, cropped so no face is visible, no legible text [STYLE] Avoid: [NEG]
- `S10.png`
A single folded cloth marked with a dark stain resting in an evidence tray under cold light, non-graphic and symbolic, the object that would decide everything, no people, no readable label [STYLE] Avoid: [NEG]
- `S11.png`
Two case folders laid side by side on a grey table under one lamp, one thicker than the other, a hand withdrawing, the cold arithmetic of trying one case before the other, no face, no legible text [STYLE] Avoid: [NEG]
- `S12.png`
Macro of a crime-lab report form under raking light, the printed characters and a blood-type notation rendered completely illegible and abstract, a paperclip edge, no readable words, no people [STYLE] Avoid: [NEG]
- `S13.png`
The back of a lone figure seated at a defense table in a dim courtroom, seen from behind and unidentifiable, head slightly bowed, the silence of a man who never spoke, no face [STYLE] Avoid: [NEG]
- `S14.png`
A dim cellblock tier receding into shadow with a single steel door standing open at the end, cold institutional geometry, the threshold into death row, no people [STYLE] Avoid: [NEG]
- `S15.png`
The interior of a single prison cell seen head-on, a narrow bunk, a steel toilet, bare concrete walls, one small high window letting in weak grey light, claustrophobic and symmetrical, no people [STYLE] Avoid: [NEG]
- `S16.png`
Extreme close-up of a heavy steel cell lock and bolt mechanism seated shut, scratched metal catching a hard sliver of light, the sound of it implied, no people, no text [STYLE] Avoid: [NEG]
- `S17.png`
The ceiling of a prison cell photographed from the bunk's point of view at dawn, the concrete turning a specific shade of grey as first light arrives, still and endless, no people [STYLE] Avoid: [NEG]
- `S18.png`
A wall calendar in a dim room with pages caught mid-turn, dates blurred and unreadable, the paperwork of a scheduled death moving forward, cold light, no people, no legible numbers [STYLE] Avoid: [NEG]
- `S19.png`
A long empty prison corridor at night lit by a single overhead fixture, a faint human silhouette far down the hall reduced to an outline, cold shadows, the sound of nothing happening, no face [STYLE] Avoid: [NEG]
- `S20.png`
A dim hospital room window at dusk with a bare chair beside an unmade bed, a man dying implied but never shown, only the empty furniture and grey light, no people, no readable text [STYLE] Avoid: [NEG]
- `S22.png`
A calendar page in cold light with two dates isolated in pools of light while the rest falls to shadow, one marked as set and one as the day itself, the numbers abstract and unreadable, no people [STYLE] Avoid: [NEG]
- `S23.png`
Anonymous hands pulling boxes of old files from a records shelf under a bare bulb, dust in the light, the frantic search of an investigator, cropped at the forearms, no face, no legible text [STYLE] Avoid: [NEG]
- `S24.png`
A single sheet of paper held up into a shaft of hard light, the text completely illegible, the proof that had been sitting in the system the entire time, reverent and quiet, no face [STYLE] Avoid: [NEG]
- `S26.png`
An empty jury box with the low gate swung open, cold courtroom light, the seats just vacated after a verdict of minutes, the word "not guilty" implied by absence, no people, no text [STYLE] Avoid: [NEG]
- `S28.png`
A cold institutional table with an empty chair and a single closed ledger under a lamp, the symbol of a fourteen-million-dollar verdict without any number shown, restrained and heavy, no people, no legible figures [STYLE] Avoid: [NEG]
- `S30.png`
The interior of a supreme courtroom photographed frontally, a long empty bench with nine vacant high-backed seats in cold marble light, monumental and unmoved, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S31.png`
A stark composition of a marble surface split by a hard line of shadow into a larger and a smaller side, cold light, the visual of a five-to-four division without any faces or text, abstract and severe, no people [STYLE] Avoid: [NEG]
- `S32.png`
Macro of the corner of a legal opinion page on a dark desk, one block of unreadable text isolated in light while the page falls into shadow, no legible words, no people [STYLE] Avoid: [NEG]
- `S33.png`
A row of identical file folders receding on a shelf under cold light, one pulled slightly proud of the others, the idea of a pattern that was ruled not to be one, no people, no legible labels [STYLE] Avoid: [NEG]
- `S35.png`
An empty appellate courtroom bench in raking cold light, tall and vacant, a single closed folder resting at its center, the seat of a decision, no people, no readable text [STYLE] Avoid: [NEG]
- `S36.png`
A vacant judicial bench seen frontally with one lit lectern below it and a stack of pages, the reading of a dissent implied by absence, cold institutional light, no people, no legible text [STYLE] Avoid: [NEG]
- `S37.png`
Four identical file folders arranged in a cold row under a single lamp, each closed, the weight of four people who knew, above them a faint grey concrete ceiling echoing a cell, no people, no legible labels [STYLE] Avoid: [NEG]
- `S38.png`
A single sheet of paper, a small receipt, and an index card laid on black under one hard light, the symbols of evidence that could set a person free, all text illegible, no people [STYLE] Avoid: [NEG]
- `S39.png`
A dim courtroom composition contrasting a full empty jury box on one side with a single closed office door on the other, the difference between hearing everything and hearing only what one office allows, no people, no text [STYLE] Avoid: [NEG]
- `S40.png`
The view from inside a dark cell looking out through bars toward a distant lit desk with a folder on it, shallow cold light, the one page that could save a life held across an unreachable distance, no face [STYLE] Avoid: [NEG]
- `S41.png`
The silhouette of a well-dressed figure standing at a desk with a folder open under a single lamp, seen against cold light so only the outline exists, no face, the person holding the file, no legible text [STYLE] Avoid: [NEG]
- `S43.png`
The silhouette of a lone figure walking away into soft morning light through an open doorway, seen from far behind, only the outline, quiet and unresolved, no face [STYLE] Avoid: [NEG]
- `S45.png`
An empty witness stand in cold courtroom light with a single microphone now turned toward it, the return of a voice that had been silenced, no people, no readable text [STYLE] Avoid: [NEG]
- `S46.png`
A single lit window in a dark building at dusk, the last blue in the sky, one warm room among many dark ones, quiet and open-ended, no people, no visible address [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記は 36 エントリ。`generate_sdxl_4k.py … --variants 3` → 108枚 pool。§5.3 で 80 body still + 15 i2v-source を選抜。ログ `shots=36` を必ず確認。

## 9.3 i2v にする15シーン（動きが意味を持つ絵）

S01(紙が引き抜かれる) / S16(ロックが座る) / S17(天井が夜明けに灰へ) / S18(カレンダーがめくれる) / S19(廊下のシルエット) / S22(2日付の間の時間) / S24(光の中の1枚) / S23(ファイルを漁る手) / S31(分割の影が動く) / S32(ページに埃) / S36(反対意見のページ) / S38(証拠の紙が並ぶ) / S40(遠い机の光) / S43(朝の光へ歩く) / S46(窓の明かりが灯る)。各シーンの `_03` variant を i2v-source に確保し、body には回さない（distinct 分離）。Wan 2.2 A14B → RIFE 48fps（Codex-A §8）。

## 9.4 サムネ3案（1280×720・実在人物の肖像禁止・「最高裁」は本文で誤認販売しない範囲で可）

- **T1（selected）:** S24（光の中の1枚の紙）＋ `THE PROOF THEY HID`（4語）。金 `#E5B53A` 下線。
- **T2:** S02（鉄扉）＋ `BURIED FOR 14 YEARS`（4語）。`14 YEARS` を金。
- **T3:** S31（5–4 の分割）＋ `5-4: NO PAYMENT`（3語）。黒/紺bg + gold。
UPPERCASE・320pxで可読・目標CTR 6%+（台本のサムネ語①②③準拠）。

---

# 10. props 定義と型（CLAUDE.md §4）＋ OP設計（§11 に接続）

```ts
export type OpeningThompsonProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる。推奨3–8文字
  subtitle: string;   // サブタイトル。UPPERCASE 表示
  accent: string;     // アクセントカラー（HEX6桁・"#"込み）。グリッド/フラクチャー/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true で左上にロゴバッジ
};
```

**EP41 の確定 props（`remotion/props/thompson.json`）:**
```json
{ "title": "THE PAPER", "subtitle": "CONNICK V. THOMPSON", "accent": "#E5B53A", "hasLogo": true }
```
**量産用 `remotion/props/thompson_short.json`:**
```json
{ "title": "BURIED", "subtitle": "FOURTEEN YEARS", "accent": "#E5B53A", "hasLogo": false }
```
> `subtitle` は `accuracy_lock` 検査対象（`remotion/props/thompson*.json` を対象パスに追加）。

---

# 11. オープニング（OP）設計 — 完全仕様（`OpeningThompson`・CLAUDE.md §1–5 全項目）

## 11.1 秒数ベースのタイムライン（fps=60・「フレーム」は全て `Math.round(fps*秒)`・直書き禁止）

| 秒 | フレーム | 起きること |
|---|---|---|
| 0.00–0.10 | f0–f6 | 画面 `#0A0A0C`。**L1** グラデ背景 opacity 0→1（0.40秒）、同時に scale 1.08→1.00 を180fで（`Easing.out(Easing.cubic)`）。**opacity 単独でなく scale 併用** |
| 0.10–0.15 | f6–f9 | **L6 ロゴ**（`hasLogo`）左上 `top:64/left:72` に spring 出現。scale 0.4→1.0・opacity 0→1（併用） |
| 0.15–0.25 | f9–f15 | **L2** グリッドが spring（`damping:200,mass:1,durationInFrames=round(60*0.8)=48`）で reveal。最終 opacity=`gridReveal*0.18`。同時に全体が180fで `translateY 0→48px`（`Easing.inOut(Easing.sin)`） |
| 0.25–0.30 | f15–f18 | **L3** sodium グローが spring（`damping:18,mass:1.2`）。scale 0.6→1.15 / opacity 0→0.85（併用）。`filter:blur(28px)` |
| 0.30–0.86 | f18–f52 | **L4 主役タイトル**が1文字ずつ切れ上がる（`overflow:hidden` マスク）。各文字 spring（`damping:16,mass:1`）で `translateY 110%→0`、opacity=`interpolate(springVal,[0,0.25],[0,1])`。**スタッガー=`round(60*0.04)=2フレーム/文字**。全体を `Trail`（`layers=6,lagInFrames=1.2,trailOpacity=0.45`）で包む（速い動きにモーションブラー） |
| 0.55–1.15 | f33–f69 | **L2b フラクチャーライン**（EP41固有＝隠された1枚が裂ける）。中央からタイトル背後を横切る亀裂が `scaleX 0→1`+`opacity 0→0.55`（spring `damping:22,mass:1.1`, `transformOrigin:'center'`）。opacity 単独禁止のため scaleX 併用 |
| 0.95–1.35 | f57–f81 | **L5a** 金の下線が左から `scaleX 0→1`（spring `damping:16,mass:0.8`, `transformOrigin:'left center'`）。240×6px・`boxShadow:0 0 24px #E5B53Aaa` |
| 1.10–1.55 | f66–f93 | **L5b** サブタイトルが `translateY 24px→0`+opacity 0→1（spring `damping:20,mass:1`・併用） |
| 1.55–2.20 | f93–f132 | 全要素 settle。背景 scale 1.02 付近を減速進行。グリッドのドリフト継続。**完全静止フレームゼロ** |
| 2.20–3.00 | f132–f180 | ホールド。背景 scale 1.00 着地、グリッド translateY 48px 着地。**フェードアウトしない** |

## 11.2 イージング・ディレイ・移動量・damping（数値表・CLAUDE.md §2）

EP40 §11.3 と同一の数値表（背景 scale 1.08→1.00 `Easing.out(Easing.cubic)` / グリッド translateY 0→48 `Easing.inOut(Easing.sin)` / グリッド reveal spring `{damping:200,mass:1,durationInFrames:48}` / グロー spring `{damping:18,mass:1.2}` / タイトル各文字 spring `{damping:16,mass:1}` translateY 110%→0・スタッガー2f / Trail `layers=6,lag=1.2,opacity=0.45` / フラクチャー spring `{damping:22,mass:1.1}` / 下線 spring `{damping:16,mass:0.8}` / サブ spring `{damping:20,mass:1}` / ロゴ spring `{damping:14,mass:0.9}`）を EP41 の accent `#E5B53A`・base `#0A0A0C` で適用。

> **等速線形を1箇所も使わない。** 全て spring か `Easing.out(Easing.cubic)`/`Easing.inOut(Easing.sin)`。**opacity 単独の演出ゼロ**（全 opacity が translateY/scale/scaleX と対）。

## 11.3 レイヤー構成（下→上・主役の裏に最低3レイヤー→4レイヤーで充足）

L0 `#0A0A0C` / L1 グラデ（`radial-gradient(120% 120% at 50% 35%, #2A2E33 0%, #14171B 45%, #0A0A0C 100%)`）/ L2 グリッド（`${accent}22` 64px・放射マスク）/ L2b フラクチャーライン（`linear-gradient(90deg, transparent, ${accent}cc, ${accent}55, ${accent}cc, transparent)`）/ L3 sodium グロー（`radial-gradient(closest-side, #C98A3A88, #C98A3A22, transparent)` `blur(28px)`）/ L4 主役タイトル（Trail 包み・`overflow:hidden` span マスク・Anton/Oswald `fontWeight:800 fontSize:150 letterSpacing:-2 color:#F5F7FA`）/ L5 下線+サブ（Oswald `fontSize:38 letterSpacing:6 uppercase color:#C8CDD6`）/ L6 ロゴ（`linear-gradient(135deg, ${accent}, #ffffff22)`・`border:2px solid ${accent}`）。

## 11.4 確認方法（CLAUDE.md §5）

**プレビュー:**
```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio     # = remotion studio。OpeningThompson を 0→180f でスクラブし §11.1 の各時刻を目視
```
**単体レンダ:**
```bash
npx remotion render OpeningThompson out/thompson_opening.mp4 --props=./props/thompson.json
```
**props 差し替えによる量産:**
```bash
npx remotion render OpeningThompson out/thompson_opening.mp4   --props=./props/thompson.json
npx remotion render OpeningThompson out/thompson_short_op.mp4  --props=./props/thompson_short.json
```
**本編レンダ:**
```bash
npx remotion render Ep41Thompson out/thompson_final.mp4 --props=./src/data/thompson_film.json
```

---

# 12. 工程分担 — Codex単体で可能な範囲 / Claude別工程

## 12.1 Codex-A（素材生成スレッド・別ファイル）

`episodes/_planning/EP41_thompson_CODEX_A_ASSETS.v001.md`（単体完結）。担当: SDXL 108枚生成・QC・depth・factory 88本選定と**全点目視QC**・i2v 15本・合成レイヤー・境界契約マニフェスト。**唯一の停止点なし（課金なしのGPU/目視ジョブ）。即着手可。**

## 12.2 Codex-B（実装スレッド）が単体でできる範囲（台本確定済みなので全て着手可能）

| # | 作業 | 成果物 |
|---|---|---|
| C1 | エピソードディレクトリ生成＋`manifest.json`（`target_duration_minutes:12`/`duration_profile:"standard"`） | `episodes/PD-2026-041-thompson/{...}` |
| C2 | 確定台本の本番配置（1バイトも変えずコピー） | `03_script/script.en.v001.md` |
| C3 | `accuracy_lock` 実装（§1.3 R1-A〜E） | `scripts/check_thompson_accuracy.py` |
| C4 | 画像プロンプト配置（§9・2行形式） | `04_scenes/ai_prompts.v001.md` |
| C5 | shotlist 214 span（全 span に asset_type/motion/transition/caption span・「等」禁止・§5.1 の配分を機械割当） | `04_scenes/shotlist.v001.json` |
| C6 | scene_plan（1ビート8フィールド・§3.2 の Sid 固定） | `04_scenes/scene_plan.v001.json` |
| C7 | `figures[]` 30 + `graphics[]` 3（§7・variety 8種） | `remotion/src/data/thompson_film.json` |
| C8 | 本編コンポジション（`BrandOpening`/`BrandEndcard` を import・fork 禁止） | `remotion/src/compositions/Ep41Thompson.tsx` |
| C9 | OP実装（§11 全仕様）＋ props ＋ Root 登録 ＋ `out/thompson_opening.mp4` | `remotion/src/compositions/OpeningThompson.tsx` |
| C10 | サムネ3案（§9.4） | `remotion/src/compositions/ThompsonThumbnails.tsx` + `09_package/thumb_{1,2,3}.png` |
| C11 | AEビルダ（5レイアウト・3カウント型・§6.6 の罠13件） | `scripts/ae/build_thompson_hero_jsx.py` |
| C12 | AEコンポジタ（SKIP 4条件） | `scripts/ae/composite_thompson_hero.py` |
| C13 | beats バリデータ（§6.4 不変条件・figures との衝突検査） | `scripts/validate_thompson_beats.py` |
| C14 | VO速度検証 | `scripts/measure_vo_wpm.py`（既存があれば流用） |
| C15 | パッケージ生成 | `09_package/description.txt`（`563 U.S. 51 (2011)` 完全一致行）/ `pinned_comment.v001.txt` / `title_candidates.json` |

## 12.3 Claude 別工程（DSP / ゲート・課金あり）

| # | 作業 |
|---|---|
| D1 | ナレ生成（§4.1 の voice・**speed 1.0 明示**）※有料・オーナー承認範囲でのみ |
| D2 | VO速度検証（`measure_vo_wpm` 168–190・範囲外は破棄再発注・BLOCKING） |
| D3 | 強制アラインメント字幕（faster-whisper 語タイム・ズレ ≤120ms） |
| D4 | 4層ミックス（-22 LUFS フロア・統合 -14 LUFS・**〔SILENCE〕をデジタル無音にしない**） |
| D5 | 全ゲート実行（motion_density / animation_mix / caption_integrity / visual_asset_qc / footage_diversity / check_asset_reuse / accuracy_lock） |
| D6 | 最終受入（`check_final_acceptance.py 41 --render <final> --emit-receipt` → exit 0） |
| D7 | アップロード/予約（オーナー操作のみ・receipt `video_sha256` 一致なしで不可） |

## 12.4 唯一の停止点＝アップロード直前のオーナー確認。即時停止する例外3つ:
1. 事実誤り（多数/反対の帰属崩れ・数値の台帳外・Thompson を有罪/無実と断定）
2. 実在人物の肖像リスク（顔・likeness の混入）
3. 検察官個人を犯罪者と名指しした／読める判決文・書類を作った

---

# 13. 受入基準（EP41 の Definition of Done・★語数ゲートが最初）

```bash
cd C:\Users\aab15\Documents\prime-documentary
# 0. 語数（最優先・課金前）
./.venv/Scripts/python.exe scripts/check_script_length.py episodes/PD-2026-041-thompson/03_script/script.en.v001.md --json
# 1. 事実性（EP41固有・§1.3）
./.venv/Scripts/python.exe scripts/check_thompson_accuracy.py --json
# 2. ビート契約
./.venv/Scripts/python.exe scripts/validate_thompson_beats.py
# 3. 密度（★29 を Remotion 側で満たしていること）
./.venv/Scripts/python.exe scripts/check_motion_density.py --ep PD-2026-041-thompson --json runs/qc/thompson_motion.json
# 4. VO速度（ナレ直後・ミックス前）
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep thompson --json
# 5. 最終受入
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 41 --render episodes/PD-2026-041-thompson/08_edit/thompson_final_bgm.v002_ae.mp4 --emit-receipt
```

| ゲート | 閾値 | EP41 設計値 |
|---|---|---|
| `check_script_length` | band内 | 2,026語（SPEC・要 `check_script_length` PASS 確認） |
| `runtime_band` | 690–750s | **695.0s = 11:35** |
| `motion_density` | ≥2.5/min ∧ cov ≥0.25 ∧ variety ≥3 | **2.90/min / 0.29 / 9種**（film.json 33 beats・AE非依存） |
| `animation_mix`（紙芝居） | still-share ≤45% ∧ motion cov ≥45% | **44.9% / 55.1%** |
| `check_asset_reuse` | first-use ≥0.70・still≤2・factory1・motion≤2 | **0.855 / 2 / 1 / 2** |
| `footage_diversity` | distinct/total ≥0.40 | **0.855** |
| `visual_asset_qc` | 全factory 目視 reviewed | **88本 目視（Codex-A）** |
| `image_resolution` | 長辺≥3840 | 全SDXL ≥3840 |
| `bgm_present` | 無音>25秒ゼロ | 最長 2.2秒 |
| `caption_integrity` | 一致≥99%・カバー≥95% | §8.2 |
| `op_ed_bookends` | `BrandOpening`/`BrandEndcard` import・不変 | ✓ |
| `accuracy_lock`（EP41固有） | violations=0 | §1.3 |

---

# 14. premortem（失敗するとしたらここ）

| # | 失敗モード | 事前対処 |
|---|---|---|
| 1 | **番号ズレ**（別番号を発明） | シーンは S01..S46 固定（§3.2）。SDXLプロンプトも S01..S46 の Sid のみ。別体系を作らない |
| 2 | **紙芝居**（still-share 45%超） | §5.1 で still-cut 96 固定・factory 88・i2v 30。still1つ増で 45% 割れ → cut を増やさず §9 で still を追加生成 |
| 3 | **密度 FAIL**（AEカードに頼る） | §7。film.json に 33 beats（29 超）。AE 8枠は composite 後で非カウント |
| 4 | **画像プロンプトが読めない**（0枚生成） | §9.1 の2行形式・`--only S01` で `shots=36` 確認 |
| 5 | **牛が本編に入る**（ファイル名信仰） | §5.4 factory 88本を `build_footage_contact_sheet.py` で全点目視（Codex-A BLOCKING） |
| 6 | **肖像・帰属違反** | §1.3 accuracy_lock。多数/反対の中立帰属・逐語引用・顔なし |
| 7 | **fast端で 9分台** | §4.1 speed 1.0 明示＋`measure_vo_wpm` 168–190・190超は破棄再発注 |
| 8 | **AE em-dash 豆腐 / 等速 / OM名英語** | §6.6 罠13件 |
| 9 | **EP39/EP40 と素材被り** | §2 で両 stock_ledger の sha256 を除外 |

---

# 15. Codex 引き継ぎプロンプト（★このブロックをそのまま Codex-B に貼る）

```
あなたは Prime Documentary EP41（thompson）の実装担当です。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe

【唯一の設計書】
episodes/_planning/EP41_thompson_DESIGN_and_CODEX_PROMPTS.v001.md を全文読んでから着手。

【唯一の真実＝機械生成スペック（手書きで数値を発明するな）】
episodes/_planning/EP41_thompson_PRODUCTION_SPEC.v001.json
  scenes S01..S46（46・固定）/ cuts 214 / still 80 / factory 88 / motion 15 /
  first_use 0.855 / still_share 0.4486 / MG beats_floor 29（film.json 側）

【確定台本（1バイトも変えない）】
episodes/_planning/EP41_thompson_script.en.v001.md（Connick v. Thompson 2011・R1）

【絶対条件（違反したら他が完璧でも出荷不可）】
1. シーンは S01..S46 に固定。別番号・別リストを発明しない（設計書 §3.2）。
2. 紙芝居禁止: still-cut 96 固定・factory実写 88・i2v 30（§5.1）。全部を静止画にしない。
3. MG密度 29 は Remotion figures/graphics（film.json）で満たす。AEカードは密度に数えられない（§6.1/§7）。
4. 画像プロンプトは generate_sdxl_4k.py の read_prompts() が読む2行形式（§9.1）。--only S01 で shots=36 を確認。
5. factory 88本は build_footage_contact_sheet.py で全点目視QC（§5.4）。ファイル名を信じない。
6. R1: 全実在人物の肖像/顔を出さない。実在検察官は法廷記録の認定事実のみ。読める判決文/書類を作らない。
   争点は多数意見/反対意見に中立帰属。Thompson を有罪/無実と断定しない（§1）。
7. AE のマシン罠13件（§6.6）を全て対処（フォント例外・spatial ease・OM/RS日本語名・app.newProject禁止・
   layer.motionBlur個別・ADBE Rotate Z・app.quit・SOFTWAREレンダ）。
8. Python スクリプトは先頭で sys.stdout.reconfigure(encoding="utf-8")。シェル経由で正規表現を生成しない。
9. 有料ジョブ（画像生成API課金・TTS・アップロード）はオーナーGOまで起動しない（ローカルSDXL/ComfyUI/RIFE は可）。
10. EP39/EP40 のファイルに触れない。公開済み mp4 を上書きしない。

【着手順序】
C1→C2→C3→C4→C5→C6→C7→C8→C9→C10→C11→C12→C13→C14→C15（設計書 §12.2）。
素材（SDXL/factory/i2v）は Codex-A（EP41_thompson_CODEX_A_ASSETS.v001.md）が並行生成。

【唯一の停止点】アップロード直前のオーナー確認。それ以外は止まらない。
即時停止3つ: (a) 帰属崩れ/数値台帳外/Thompson断定 (b) 肖像リスク (c) 読める判決文/検察官の名指し。

【解釈の余地】数値が書いてある箇所はその数値を使う。無い判断は止めて質問。推測で埋めない。
```
