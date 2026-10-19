# GATE AUDIT v001 — 未ゲート化の教訓の洗い出しと実装

**作成日:** 2026-07-19
**根拠:** オーナー META-RULE「記憶や約束に頼るな。強制可能な教訓はすべて、パイプラインをブロックするゲートに変換しろ。しかも高コストな工程の**前**に置け」
**方針:** 「仕様に書いてあるが機械チェックが無い」項目を本命として狙った。過去の実例 —
仕様に「単一クリップの再利用は3回まで」と書いてあったのにゲートが無く、実測したら全13本が違反していた。

---

## 0. 結論（先に要点）

新規実装した3ゲート:

| ゲート | 対象 | 根拠 | 全話監査 |
|---|---|---|---|
| `check_retention_cadence.py` | SPEC v2 **row 16** | 契約表で**唯一ゲートが全く存在しなかった行** | PASS 10 / FAIL 3 / SKIP 25 |
| `check_packaging_qc.py` | SPEC v2 **row 13** | 仕様自身が "**Still manual:** row 13" と明記 | PASS 11 / FAIL 15 / SKIP 12 |
| `check_encoder_settings.py` | SPEC v2 **row 6** | 「render logから crf/preset/pix_fmt を assert」が未実装 | PASS 13 / FAIL 12 / SKIP 13 |

3件とも `preflight_render_gate.py` の checks リストに配線済み。
**false-RED は2件発見し、いずれも自分のゲート側のバグとして修正した**（§5）。

---

## 1. 洗い出した「強制可能な教訓」一覧

retro / INCIDENT / REMEDIATION / PREMORTEM 系（EP21-24_INCIDENT_RETRO, EP32_DESIGN_REMEDIATION,
EP33/34/35_DESIGN_REMEDIATION, EP38_PREMORTEM, VIDEO_RULES, PACKAGING_FIX, STRATEGY, PD_SHIP_GATE,
PD_EP32_POSTMORTEM）から抽出した、数値・件数・比率・ファイル存在で機械判定できる教訓。

### 既にゲート化済み（重複実装しない）

| 教訓 | 既存ゲート |
|---|---|
| 台本語数が尺を満たすか（TTS課金前） | `check_script_length` |
| 素材の話内反復使用 | `check_asset_reuse` |
| 字幕の不正な切断・孤立キュー | `check_caption_breaks` |
| 字幕の存在・焼き込み・衝突 | `check_caption_integrity` |
| プレミアムMG密度（紙芝居検出） | `check_motion_density` |
| 静止画依存の偏り | `check_animation_mix` |
| 素材の誤ラベル・暗すぎ・同質すぎ | `check_visual_asset_qc` |
| 完成尺バンド 690–750s | `check_runtime_band` |
| 水増し（無音・言い換え反復） | `check_padding` |
| 局所的フラット区間（12s窓） | `check_flat_windows` |
| 話またぎの素材使い回し | `check_arc_nonrepeat` |
| DL素材が未使用のまま | `check_footage_utilization` |
| 音楽ベッドの途切れ | `check_music_coverage` |
| 4部構成 / Bookends / サムネ枚数 / 画像解像度 / footage多様性 / 明度 | `check_final_acceptance` 各check |
| 静止画の実在・4K・depthマップ | `preflight_render_gate` CHECK2 |

### 未ゲート化だったもの（本監査の発見）

| # | 教訓 | 出典 | 状態 |
|---|---|---|---|
| A | **再フック（re-hook）を2〜3分ごとに置く / 平坦な説明区間を作らない** | SPEC row 16、EP33 #54（6:16のギャップで自己申告の5:30床を割った）、EP35 r2（18:15→EDにフック無し） | **→ ゲート化（本件1）** |
| B | **タイトル ≤60字 / A・Bバリアント ≥2本** | SPEC row 13（仕様自身が "Still manual" と明記）、PACKAGING_FIX §1/§6 | **→ ゲート化（本件2）** |
| C | **教義フレーム題（"X v. Y" / "Supreme Court Case"）を避ける** | PACKAGING_FIX §1/§6（実測: Kelo 1.55% = チャンネル最悪、Mapp 5.3%、Gideon 7.5%） | **→ ゲート化（本件2に統合）** |
| D | **AI開示行を説明文に入れる** | VIDEO_RULES §5、EP38 §G | **→ ゲート化（本件2に統合）** |
| E | **libx264 / yuv420p / bt709 / aac 320k / NVENC禁止** | SPEC row 6 | **→ ゲート化（本件3）** |
| F | 平均ショット長 ≤6s / 静止保持 >2s 禁止 | SPEC row 8 | 保留（§4-1） |
| G | film.json のカット列にギャップ・重複が無いこと | 暗黙 | 保留（§4-2） |
| H | promise-payoff（フックで釣った謎が後で回収されるか） | SPEC row 9 | 保留（§4-3） |
| I | CRF / preset の assert | SPEC row 6 | 保留（§4-4） |
| J | final_delivery ポインタの実在・sha一致 | EP21-24 retro Rule 3（EP23が誤ったファイルを指していた） | 保留（§4-5） |
| K | 全ゲートにネガティブ・フィクスチャを持たせる | EP33 #32 / EP34 #27 / EP35 g34 | 保留（§4-6） |
| L | 同一主題の重複動画を出さない | PACKAGING_FIX §3（Carpenterが2本共食い、17再生と7再生） | 保留（§4-7） |
| M | 台本の全数値がclaim台帳に紐づくこと | EP32 M7（未出典4件）、EP38 §G | 保留（§4-8） |

---

## 2. ゲート化した3件

### 2-1. `scripts/check_retention_cadence.py` — SPEC row 16

**なぜ本命だったか:** 契約表16行のうち、**Verify欄に "script QC (retention map)" と書かれながら、
その스크립트が存在しない唯一の行**。しかも STRATEGY_v001 は retention + CTR をチャンネルの
最重要収益レバーと位置づけている。EP33/EP35 では人間が書き起こしを読んで手作業で検出していた。

**設計上いちばん難しかった点 = しきい値の正直な較正。**
単一指標の設計を2つとも棄却した（どちらも false-RED 製造機だったため）:

- **(a) 疑問符のみ / row 16の「3分ごと」**: 実測レンジ 180〜787s。チャンネル最良の unlock ですら
  180.1s。180s床では **13本中13本FAIL** — 良い作品まで落ちる。単独床としては棄却。
- **(b) 広義マーカー（疑問符 or 二人称 or 転換語）/ 180s**: 実測レンジ 24.7〜139.1s。
  **13本中13本PASS** — 何も検出しない。単独床としては棄却。

真値は中間にあるため、**2つの床をそれぞれの proxy が正直に支えられる閾値で併用**する:

| 床 | 定義 | 閾値 | 役割 |
|---|---|---|---|
| FLOOR 1 | 広義 re-hook マーカーの最大間隔 | ≤180s | row 16 の逐語エンコード。現状13本全PASS = **リグレッション・ロック** |
| FLOOR 2 | 直接疑問文の最大間隔 | ≤420s | 狭いproxyなので緩い閾値。「視聴者に一切問いかけない説明区間」を検出 |

FLOOR 2 の較正実測値（420sは 352.6s クラスタと 555.3s 外れ値の自然な谷に置いた）:

```
unlock      180.1   rodriguez  192.6   tyler      212.1
carsearch   258.0   forfeiture 294.6   katz       301.2
kyllo       310.3   kidsforcash 321.2  williams   324.6
cotton      352.6   hinders    555.3  FAIL
hinton      676.3  FAIL（11.3分間で疑問文ゼロ）
rolin       786.7  FAIL
```

冒頭〜初マーカー、末尾マーカー〜終端も間隔として数える（EP35 r2 は「末尾にフック無し」だった）。

### 2-2. `scripts/check_packaging_qc.py` — SPEC row 13

**なぜ本命だったか:** 仕様の §C が自分で
「**Still manual:** row 13 (title ≤60 / A-B)」と列挙している。EP19以降ずっと拘束力のある
ルールでありながら、何も強制していなかった。仕様 §E の警告そのもの —
「A requirement with no gate WILL drift; add the gate.」

**HARD（ブロックする）:**
1. タイトル ≤60字（row 13）
2. 異なるタイトル候補 ≥2本（row 13 "Ship A/B title × thumb variants"）
3. 選択タイトルに教義フレームが無いこと（PACKAGING_FIX 実測: Kelo 1.55% がチャンネル最悪）
4. 説明文が存在し、AI開示行を含むこと（VIDEO_RULES §5）

**SOFT（報告のみ・絶対にブロックしない）:**
- タイトルに数字が無い。PACKAGING_FIX はCTR向上のヒントとして数字を挙げるが、
  出荷済み26本中20本に数字が無く、その中には好成績のものも含まれる。
  これをHARDにすると**自チャンネルのカタログ全体を落とす false-RED** になるため、報告のみに留めた。
  （`caption_integrity` がCaseFilm全機を誤判定した教訓の適用）

### 2-3. `scripts/check_encoder_settings.py` — SPEC row 6

**なぜ本命だったか:** row 6 は Gate欄に
「crf/preset/pix_fmt asserted from render log」と明記しているが、**実装されていなかった**。
2026-07-19に `check_final_acceptance.py` を精読して確認 —
エンコード関連のcheckは `check_render_resolution` ただ1つで、
`width,height,codec_name` をffprobeして**解像度しか比較していない**。
`codec_name` は人間向けの理由文字列に埋め込まれるだけで、何とも突き合わせられていない。
つまり現状、`h264_nvenc` エンコードも `yuvj420p` フルレンジも bt470bg も 128k音声も、
acceptance を素通りする。

**仮定の話ではない。** `remotion/out/` の全91本を走査したところ28本が row 6 から逸脱しており、
しかも**リポジトリ自身のツールがそれを生成している**（Reel系が yuvj420p + bt470bg、
Shorts の coverfirst が音声184k）。

**スコープは意図的に絞った（false-RED回避）:** 判定対象は
**そのエピソードの長尺ファイナル1本のみ**。Shorts（1080x1920）・probeスライス・無音中間ファイル・
Reelは長尺仕様で裁いてはならない。解決順は
final_delivery ポインタ → `PD-<id>_film.muxed.v*.mp4` → slug一致の muxed。

**CRF/presetは検査していない**（mp4コンテナから復元不能なエンコーダ側パラメータ）。
偽装せず、row 6が実際に気にしている**観測可能な結果**（コーデック族・ピクセルフォーマット・
色タグ・解像度・音声レート）を assert し、映像ビットレートは参考値として報告する。→ §4-4 に保留として記載。

---

## 3. 全話監査の結果表

`evaluate(epdir)` を全38エピソードに対して実行（読み取り専用・課金なし）。

### 3-1. `retention_cadence` — PASS 10 / FAIL 3 / SKIP 25

| エピソード | 判定 | 内容 |
|---|---|---|
| PD-2026-029-hinton | **FAIL** | 676s間 直接疑問なし（>420s）— **全編で疑問文ゼロ** |
| PD-2026-034-rolin | **FAIL** | 787s間 直接疑問なし、5.7分地点から |
| PD-2026-035-hinders | **FAIL** | 555s間 直接疑問なし、冒頭から |
| carsearch / cotton / forfeiture / katz / kidsforcash / kyllo / rodriguez / tyler / unlock / williams | PASS | — |
| 上記以外25本 | SKIP | film.json 未生成 |

FLOOR 1（広義180s）は**現状13本すべてPASS**（最悪 hinders 139.1s）。
つまり検出された3件はすべてFLOOR 2由来 = 「視聴者に問いかけない長い説明区間」。
**false-RED なし**（良い作品を落としていない。unlock/rodriguez/tyler など高品質回はすべてPASS）。

### 3-2. `packaging_qc` — PASS 11 / FAIL 15 / SKIP 12

| エピソード | 違反内容 |
|---|---|
| miranda | 教義題（`v. A`） |
| gideon / mapp / ftx / madoff / terry / carpenter / titan / flashcrash | A/Bバリアント 1本のみ |
| riley | A/Bバリアント 1本のみ ＋ 教義題（`Supreme Court Case`） |
| kelo | 教義題（`Supreme Court Case`） |
| hinton | A/Bバリアント 1本のみ |
| theranos | タイトル70字 > 60 |
| rolin | タイトル64字 > 60 |
| kidsforcash | タイトル73字 > 60 |

**スコープ注記:** SPEC v2 は「BINDING for every episode from EP19 onward」と自ら宣言している。
EP19以降に限ると **12本中3本FAIL**（hinton = A/B無し、rolin = 64字、kidsforcash = 73字）。
残りの12件はすべてv1時代（EP1–18）のもので、違反自体は実在するが v2 の拘束範囲外。
→ カタログを断罪するのではなく**弁別している**ので健全。**false-RED なし**（修正後、§5参照）。

### 3-3. `encoder_settings` — PASS 13 / FAIL 12 / SKIP 13

| エピソード | 違反内容 |
|---|---|
| **cotton (EP30)** | **`h264_nvenc`（row 6が明示的に禁止）** ＋ yuvj420p ＋ bt470bg ＋ 音声166k。映像2703kbps（tylerは11930kbps） |
| miranda / mahanoy / king / lange / theranos | yuvj420p ＋ bt470bg |
| terry / riley / carpenter | yuvj420p ＋ bt470bg ＋ 音声175–198k |
| titan | bt470bg ＋ 音声196k |
| arbitration / onecoin | 音声191k / 195k |
| EP19以降の長尺ファイナル13本 | すべてPASS（h264/High/yuv420p/bt709/aac ~310k） |

**スコープ注記:** FAIL 12件のうち11件はEP1–17（v1時代）。
**v2拘束範囲内の違反は cotton (EP30) の1件で、これが最重要の検出**
— 仕様が名指しで禁じたNVENCで出荷されており、ビットレートも他話の1/4以下。

**false-RED の検証:** リゾルバが「レビュー用中間ファイル」を誤って掴んでいないか個別に確認した。
`carpenter_review_v001.mp4` は名前に反して `final_delivery.v008.json` が
shipped render として指しているファイル本体、`miranda_premium_v001.mp4` は
公開済み動画（video_id `cQFql7tT1fE`）の実体。**いずれも真のファイナルであり誤検出ではない**。
（なお "review" / "final" という名前付けの紛らわしさ自体は EP21-24 retro Rule 3 が既に指摘済み。）

---

## 4. 保留にしたもの（配線しない）と理由

### 4-1. 平均ショット長 ≤6s / 静止保持 >2s（SPEC row 8）— 保留
実測したところ全13本が既に健全（mean 1.78〜3.34s、6s超のカットは最大でも34/350本、
8s超は rolin の8本のみ）。**現状ゼロ検出**のため、独立ゲートを増やす価値が低い。
局所的なフラット区間は `check_flat_windows` が実レンダーに対して既に測っており、そちらの方が強い。

### 4-2. film.json のカット列ギャップ／重複 — 保留
全13本で **gap 0 / overlap 0**、末尾未カバーも最大0.2s。完全に健全なため検出価値なし。
純粋なリグレッション・ガードとしては有用だが、今回の上位3件より優先度が低い。

### 4-3. promise-payoff（SPEC row 9）— 保留
「フックで提示した謎が後で回収されるか」は**意味理解が必要**で、文字列一致では判定できない。
無理に正規表現化すれば `caption_integrity` と同種の false-RED を生む。
LLM判定を挟むなら課金が発生するため、本タスクの制約（課金禁止・読み取り専用）に反する。

### 4-4. CRF / preset の assert（SPEC row 6の残り）— 保留
mp4コンテナからは復元不能（エンコーダ側パラメータであってメタデータではない）。
正しい実装先は**レンダーログ**であり、そのためには
`remotion/out/` のレンダーログを構造化して保存する仕組みを先に作る必要がある。
偽の assert を書くくらいなら未実装と明示する方が良い（EP33 #32「スタブgreen」の教訓）。

### 4-5. final_delivery ポインタ整合（EP21-24 Rule 3）— 保留
実装しようとしたが、**スキーマが話ごとにバラバラ**で安全に書けない。
実測したキー名: `video` / `final_video` / `render`（dict内 `file`）/ `render_actual_path` /
`final_video_sha256` の有無もまちまち。
さらに実体は外付けSSD `H:\pd-media` にあり、未マウント時に全話FAILする危険がある。
**先にスキーマを統一してから**ゲート化すべき。現状で書くと false-RED 製造機になる。

### 4-6. 全ゲートのネガティブ・フィクスチャ（EP33 #32 / EP35 g34）— 保留
これは「ゲート」ではなく**テスト基盤**の話で、`tests/` の設計変更を伴う。
今回の3ゲートについては、実データ上でFAILする実例を確認済み
（hinton/rolin/hinders、kidsforcash 73字、cotton の NVENC）＝ 事実上のネガティブ検証は済んでいる。
体系化は別タスク。

### 4-7. 同一主題の重複動画（PACKAGING_FIX §3）— 保留
実害は記録上1件（Carpenterが2本、17再生と7再生で共食い）。
タイトルのファジーマッチは誤検出リスクが高い割に、発生頻度が低い。優先度低。

### 4-8. 台本数値のclaim台帳紐づけ（EP32 M7）— 保留
claim台帳の所在・形式がエピソード間で統一されておらず、
大半の話で台帳が存在しないため**ほぼ全話SKIPになり実効性が無い**。台帳整備が先。

---

## 5. 自分のゲートを疑った記録（false-RED 2件を自己修正）

タスク指示「全話FAILが出たら、まず自分のゲートを疑え」に従い、初版の結果を精査した。

`packaging_qc` 初版は **26本中23本FAIL（88%）** という異常な数字を出した。
カタログ側ではなく**ゲート側のバグ**だった:

| # | 症状 | 真因 | 修正 |
|---|---|---|---|
| 1 | 20本が「タイトル候補1本」でFAIL | A/B候補は `youtube_meta` ではなく **`title_thumbnail_candidates.v*.json`** に書かれているのが通例。スキーマも4種（`title_candidates[]` / `candidates[]` / `titles[]` / `selection.selected_title`）。timbsのT1/T2/T3、milkenのA/B、miranda等が全て見落とされていた | 両ソースをマージ |
| 2 | mahanoy / milken / hinton が「説明文なし」でFAIL | 説明文は **`description.v001.md` / `.txt` のサイドカー**として存在。インラインフィールドしか見ていなかった | サイドカーもマージ |

修正の効果: **FAIL 23 → 17 → 15**。
この2件は、どちらも「1つの成果物だけを見て、パイプラインが実際に使っている複数の置き場所を見ていない」
という同じ失敗パターンだった。ゲートを書くときは**その情報が実際にどこに書かれているかを全数調査してから**
判定ロジックを書くこと。

`encoder_settings` については、逆に「FAIL 12件は誤検出ではないか」を疑い、
リゾルバが掴んだファイルが真のファイナルかを個別確認した（§3-3）。結果、誤検出なし。

---

## 6. 配線内容

`scripts/preflight_render_gate.py` の `checks` リスト末尾に3件追加（既存ゲートの閾値は一切変更していない）:

```python
_run_ext_gate("check_retention_cadence", "retention_cadence", repo_root, ep_slug),
_run_ext_gate("check_packaging_qc",      "packaging_qc",      repo_root, ep_slug),
_run_ext_gate("check_encoder_settings",  "encoder_settings",  repo_root, ep_slug),
```

3件とも `evaluate(epdir) -> {ok, hard, skipped, reason}` 規約に準拠、
成果物が無ければ SKIP（不在でFAILしない）、読み取り不能な成果物には
**fail-closed**（EP32 B1「例外時にgreenを返すな」の教訓）。
先頭に `sys.stdout.reconfigure(encoding="utf-8")` を配置（cp932対策）。

### 今後の推奨（本タスクの範囲外）

`packaging_qc` と `encoder_settings` は**本来の適所が ship gate 側**である。
preflight はレンダー前に走るため、この2つはその時点では通常SKIPになる
（パッケージメタも最終レンダーもまだ存在しない）。
META-RULE の「高コスト工程の前に置け」を厳密に満たすなら、
この2つは **アップロード/スケジュール前**に噛む必要がある =
`check_final_acceptance.py` にも追加するのが正しい。
今回は既存 acceptance ゲートの改変を避けるため preflight のみに留めた
（再レンダー時には preflight でも実際に発火する）。

---

## 7. 検証コマンド

```bash
# 単体
python scripts/check_retention_cadence.py episodes/PD-2026-038-kidsforcash
python scripts/check_packaging_qc.py       episodes/PD-2026-038-kidsforcash --json
python scripts/check_encoder_settings.py   episodes/PD-2026-030-cotton

# 特定成果物を直接
python scripts/check_retention_cadence.py --film remotion/src/data/hinton_film.json
python scripts/check_encoder_settings.py  --render remotion/out/xxx.mp4

# 統合
python scripts/preflight_render_gate.py --ep PD-2026-038-kidsforcash --no-receipt
```
