# アーカイブ棚 — 2026-08-09/10 作業記録と、他スレが知るべきこと

> この文書は「素材棚スレ」の全記録。**要点だけ必要なら `PD_CANON.md` §素材棚を読めば足りる。**
> ここは、なぜそうなったか・どう測ったか・何を踏んだかを残す場所。
> 数字はすべて **2026-08-10 時点**。測り直すコマンドを各項に付けてある。

---

## 0. 30秒で分かる現在地

```
棚          63,180 点（archive）＋ 88,963 点（factory）
判定        212 組すべて完了   good 103 / mixed 60 / unusable 49
カバレッジ  Prime Documentary 100% / Prime Finance 90% / Prime Business 100%
動画        31,107 本すべて解像度既知（SD 5.9%）
レーン      ia のみ稼働。gov / sci / web_video / web_audio は枯渇して正常終了
本日削除    498 GB（判定不可 212 + 会議中継 286）
隔離累計    1,330 件
```

測り直す:

```bash
py -3.11 scripts/shelf.py                      # 棚の総数（ソース別）
py -3.11 scripts/build_archive_inventory.py    # 在庫表を作り直す
py -3.11 scripts/check_shot_coverage.py --md   # 3チャンネルのカバレッジ
```

---

## 1. 棚の使い方（他スレが一番使うところ）

### 探す

```bash
py -3.11 scripts/search_archive.py --shot "courthouse building exterior" --kind video --md --sheet
py -3.11 scripts/search_archive.py --pick 1,3 --reject 2,4
```

**ショットは「監督の言葉」でなく「素材提供者が付ける題名の語彙」で書く。**
これが今回いちばん大きな発見だった（§4）。

- `police interview room` → 0件。`interrogation room detective` → 12件
- `handcuffs on wrists` → 0件。`person in handcuffs` → 16件
- `foreclosure sign house` → 0件。`for sale sign house` → 109件

**0件が返ったら `--weak-ok --sheet` を付けて必ず目で見る。**
弱一致プールは大半が語の衝突（`branch`＝木の枝、`card`＝基板）だが、
本命がそこに埋まっていることが12/13の確率であった。

### 検索結果の読み方

動画には `[1920x1080]`、720p未満なら `SD` が付く。SDを選ぶのは**判断であって事故であってはならない**。

```
[ 1] s 38        ia | National Film Board Of Canada Newsreel Excerpts  [640x480] SD
  ! 4 of these are below 720p
```

自動で除外されるもの: オーナー判定 `unusable` の行 / ban-risk 行 / `_quarantine` 配下。

### 見る

```bash
py -3.11 scripts/qc_archive_contact_sheets.py --theme prison_jail --source unsplash --per-theme 24 --refresh
```

`--source` は必須に近い。**未判定の単位はテーマ×ソース**であり、テーマ全体のシートは
ソース間で層化してしまう（pixabay_extra の2,265点が24枚中4枚になる）。

---

## 2. 「棚とは何か」の定義は1か所（`scripts/shelf.py`）

これを作った理由は、**3つのツールが各自の定義を持ち、3つとも違う壊れ方をしていた**から。

| ツール | 壊れ方 | 実害 |
|---|---|---|
| `build_archive_inventory` | `purged.jsonl`（削除記録64,640行）を在庫に加算 | 197,712点と報告。実際は132,948点 |
| 未判定集計（即席） | `ukna_candidates.jsonl` の22,348行を「未レビュー在庫」と誤報 | 全部 `file_path: null`。英国国立公文書館APIはメタデータのみで、1本もDLしていない |
| `qc_archive_contact_sheets` | 同じく `purged` を含む | 削除済みをレビュー対象に出す |

削除記録は元の行と同じ `(source, id)` を持つので、**数えると二重に数える**。

```python
from shelf import shelf_rows
for rec in shelf_rows(include_factory=False):
    ...
```

**新しく棚を数えるコードを書くときは必ずこれを使う。** 自前で `glob("*.jsonl")` しない。

---

## 3. 台帳の行は消さない（重要）

台帳の 47.0%（134,745行）はディスク上に存在しないファイルを指している。
**これは壊れているのではなく、削除の記録**。内訳は purged 134,080 / quarantined 661 / 原因不明 4。

**行を消してはいけない。** 取り込みは `(source, id)` で重複判定しているので、
行を消すと**同じものを取り直す**。46,707枚のニューヨーク市住所録がそれで戻ってきた実績がある。

代わりに `_ledger/absent_index.json` が別管理し、読み手が引く。

```bash
py -3.11 scripts/build_absent_index.py      # 削除・隔離された行の索引を作り直す
```

---

## 4. カバレッジは「棚の大きさ」ではなく「話が組めるか」

点数は制作の答えにならない。**ショット一覧を実際に流すことだけが答えになる。**

```
config/shot_coverage_shots.v002.json    3チャンネル × 20ショット
py -3.11 scripts/check_shot_coverage.py --md
```

| チャンネル | v001(8/6 手動) | v002(8/10 実測) |
|---|---:|---:|
| Prime Documentary | 85% | **100%** |
| Prime Finance | 50% | **90%** |
| Prime Business | 90% | **100%** |

**上がったのは棚が増えたからではない。書き方を直しただけ。**
v001が「素材が無い」とした13ショットのうち12は、最初から棚にあった。

足切り（score>15）は**下げていない**。下げると「郡裁判所の外観」で郊外住宅が返る状態に戻る。

### 本当に足りない2件（購入でなく小道具）

| ショット | 実態 | 対処 |
|---|---|---|
| `savings passbook close up` | 本物の通帳は英国郵便貯金の2点のみ。`savings account book` は16件返るが14件がただの紙幣 | 小道具か生成 |
| `eviction notice on door` | 完全に空。弱一致20枚すべて道路標識・黒板・OPEN看板 | 小道具（書いて撮る） |

どちらも実在人物も実在事件も写らないので invariant 11 に抵触しない。

### v001の推奨を撤回した

v001 は `ticker tape machine` と `run on the bank crowd` に**有料アーカイブが必要**と書いた。**撤回。** 両方とも無料で棚にある。

- `stock ticker board` → Western Union と Edison の実物ティッカー、NYSE取引所ボードの当時写真
- `foreclosure sale crowd` → NARA の農場差押え競売に集まった群衆

---

## 5. 判定（verdicts）— 機械が読む唯一の品質判断

`H:\pd-media\assets\archive\_qc\archive_verdicts.jsonl`

```json
{"theme":"courtroom_justice","source":"unsplash","verdict":"good","note":"...","judged_by":"..."}
```

- `unusable` は**検索から完全に外れ**、取り込みでも**再取得されない**（全4レーン）
- `mixed` / `good` は検索に出る。`note` に落とし穴が書いてある

### 212組の結論（抜粋）

**当たり（そのまま使える）**

| テーマ × ソース | 中身 |
|---|---|
| courtroom_justice / unsplash | 24枚中22枚が米国の裁判所。木製パネルの空の法廷 14467x5736 |
| government_buildings / unsplash | 連邦議事堂・州議事堂・国立公文書館。最大 9324x6216 |
| prison_jail / unsplash | 20枚中18枚が実際の監獄。独房棟・螺旋階段・アルカトラズ |
| money_banking / loc | 24枚中19枚が実物の銀行建築。最大 13150x10199 |
| science_tech / nasa | 管制室・風洞・発射管制。全てPD |
| japan / loc | 真珠湾のUSSウェストバージニア、1942年サンペドロ、横浜錦絵 |
| legal_court / pexels | 最高裁ファサード、法廷内装、正義の女神像 |
| crime_police / pexels | 夜のパトカー、留置場、手錠 |
| audio / oyez | Terry・Kelo・Carpenter・Riley・Timbs の最高裁口頭弁論（一次資料） |

**外れ（全部キーワード衝突1つが原因）**

| テーマ × ソース | 衝突 | 実際に入っていたもの |
|---|---|---|
| courtroom_justice / pixabay_extra | `bench`（判事席） | 24枚中11枚が**公園のベンチ**。緑の照明の幽霊修道女 |
| courtroom_justice / mixkit | `walking` `library` | 9枚が歩く人、8枚が一般図書館 |
| newspapers_printing / pixabay_extra | `press` | 干し草ベーラー、ベンチプレス、コーヒープレス、ブルドーザー |
| newspapers_printing / mixkit | `running`（輪転機が回る） | 12枚がジョギング・陸上競技場 |
| government_buildings / pixabay_extra | `seal`（国璽） | **アシカ**、登山道の道標、国旗の壁紙アニメ |
| government_buildings / mixkit | — | 24枚中12枚が国旗（コロンビア・タイ・海賊旗） |
| prison_jail / pixabay_extra | `cell` | ワイングラスの食卓、ムール貝料理、ドゥカーレ宮殿 |
| uk_period, uk_highstreet_postoffice / loc | `London` | **オハイオ州ロンドン**の地方紙 Madison County Democrat |
| period_telephone_tech / loc | `telegraph` | 新聞**名**（Washington Telegraph / American Telegraph） |
| americana_1930s_1970s / met | `Allegory of America` | ルネサンス寓意版画24枚 |
| landscapes_timelapse / nasa | `glacier` | **ISSの冷凍実験装置「GLACIER」** — 船内の宇宙飛行士7枚 |
| navy_harbor / loc | `harbor` | ワシントン州**フライデーハーバー**の地方紙16枚 |
| laboratory_forensics / noaa | `laboratory` | **アクエリアス海底居住施設** |

**pixebay_extra は金融・ビジネス・PD系のほぼ全テーマで unusable。** 各テーマで最大のソースでありながら中身が無い。

---

## 6. 音声は測って判定する（`scripts/qc_audio_stats.py`）

コンタクトシートは音を見せられず、8,635点を聴くのも無理。
**使えなくなる原因を客観指標で測る。**

```bash
py -3.11 scripts/qc_audio_stats.py --per-theme 60
```

| 検出 | 基準 |
|---|---|
| near-silent | ピーク -50 dBFS 以下、または90%以上が無音 |
| clipped | ピーク -0.1 dBFS 以上 |
| too-short | 0.4秒未満（ベッドとして成立しない） |
| mono-bed | ambience/bgm/environment でモノラル（ステレオミックスの下に敷けない） |
| band-limited | スペクトルロールオフ 8kHz未満 |
| low-rate | 44.1kHz未満 |

**各検出は「わざと壊した音声で落ちること」を実証してから使った**（CLAUDE.md 4.6）。
その作業自体がバグを見つけた — §8-③。

判定結果:

```
bgm_general        good    60本中1件
ambience_beds      good    8件（モノラル6）
sfx_human_movement good    7件（軽微なクリップ）
sfx_environment    mixed   12件（モノラル8・焚き火が +3.6 dBFS）
sfx_mechanical     mixed   15件（13件クリップ。短い音は歪みやすい）
audio / oyez       good    ※計測器の方が間違っていた。§8-④
```

playlist が `_qc/<theme>/listen_<source>.m3u8` に出るので耳で確認できる。

---

## 7. 動画の解像度（`_ledger/video_resolution.json`）

**台帳には幅も高さも無かった。31,156本すべて。** 検索も出荷ゲートも 4K と 320x240 を区別できなかった。

```bash
py -3.11 scripts/build_video_resolution_index.py --source all   # 再開可能
```

全数実測:

```
4K+     5,104   16.4%
1080p  18,222   58.6%
720p    5,946   19.1%
SD      1,835    5.9%
```

**偏りが本体。**

```
nara   814本中 727本 SD  (89.3%)
ia   1,422本中1,037本 SD  (72.9%)
pexels / pixabay / mixkit / nasa / coverr    ほぼ 0%
```

テーマ別で危ないのは **100%のテーマではなく、2割だけ混ざるテーマ**。

```
vintage_ads_cartoons  100%   ← 安全（必ずSDと分かって使う）
factory_manufacturing 100%   ← 安全
navy_harbor            96%
war_history            86%
─────────────────────────
courtroom_justice      17%   ← 危険。8割HDの中に紛れる
prison_jail            19%   ← 危険
```

### 取り込み基準は上げていない（意図的）

`ingest_archive_sources.py` の技術基準は、記録系の480p未満を**削除でなく隔離**する。
7月に書かれた理由がまだ正しい — 関連度ゲートを通った記録映像は代替不能で、
削除経路があってはならない（帯でなく床にすること。過去に帯にして
ニュルンベルク／マウトハウゼンのリールを7本破壊した）。

**480〜719pを通すのは設計通り。必要なのは基準を上げることでなく、見えるようにすること。**

---

## 8. 踏み抜いた罠（このスレで新規に発見したもの）

### ① コンタクトシートが TIF を表示できていなかった（最も重い）

`build_footage_contact_sheet.py` の `IMG_EXT` に `.tif` が無く、TIFが ffmpeg 経路に落ちて
「静止画の1秒目にシークできない」で失敗し、**赤い UNREADABLE の箱**になっていた。

棚のTIFは **2,953点**（LOC 1,447 / Wikimedia 1,404 / NASA 102）。

つまり **8/9以前の全コンタクトシートは、LOCとWikimediaの記録写真が全部見えない状態**で
レビューされ、そこから判定が記録されていた。差押えのシートでは NARA の
「農場差押え競売」4枚が赤い箱の裏に隠れていた — Prime Finance が「無い」と記録していた素材そのもの。

**教訓: 赤い箱を「悪いファイル」と読まない。** 修正後は復号失敗の件数と理由を出力する。

影響を受けた `unusable` 判定2件を再検証し、両方とも正しいことを確認済み
（`prison_jail/loc` は12枚中10枚が印刷物、`weather_disasters/noaa` は
CIRAロゴ入りの気象衛星合成）。

### ② 採用フィードバックが全ショットに漏れていた

「独房の通路」で選んだクリップ4本が、`bank branch interior counter`
`foreclosure sign house` `checkout till transaction` の**首位**に来ていた。

素点0の物に採用ボーナス +15 が**無条件で**足され、足切り15を超えていた。
フィードバックファイルはどのショットで選んだか記録しているのに、読み込み側が捨てていた。

**修正: 加点は素点が正のときだけ。** 採用は「関連する結果の中で正しかった」であって
「あらゆるものに関連する」ではない。

### ③ `-v error` が測定そのものを消していた

`ffmpeg -v error -af astats,silencedetect` — astats と silencedetect は **info レベル**で出力する。
`-v error` を付けると全部消える。結果、音声QCは **ffprobe の項目しか取らず、
無音もクリップも測らないまま「good」と報告していた**。

**教訓: 「検査が緑」より先に「検査は何を読んだか」を見る。**

### ④ 計測器の方が間違っていた（最高裁の音声）

`qc_audio_stats.py` が `audio/oyez` を **100% unusable** と判定した。
中身は Terry・Kelo・Carpenter・Riley・Timbs の**最高裁口頭弁論**。

22kHzモノなのは**最高裁自身の配布形式**で、これは b-roll でなく一次資料。
音楽ベッド用の床を当てたのが設計ミス。`SPEECH_SOURCES` で除外した。

（ただし3本は本当に 0 dBFS を超えており、リミッターが要る。）

### ⑤ 隔離ルールが単語の途中に一致していた

既存の隔離1,249件を監査したら、**米海軍の写真2枚が「過激派の宣伝」として隔離**されていた。

```
"ns "          → "NS Pearl Harbor"（Naval Station）
"illuminati"   → "illuminations"（照明）の前方一致・街灯の写真24枚
"media smart"  → "media smartphone" の前方一致
"taxi driver"  → 新聞を読む本物のタクシー運転手
"disney"       → ディズニーランドの夜景（場所であって版権キャラではない）
```

単語境界を入れ、**12件のテストで両方向を確認**した（海軍の船は通す／メイソンの演説は止める）。
海軍写真2枚は棚に戻した。

### ⑥ ランチャーが指定した数だけ起動していなかった

`launch_ingest_lanes.ps1 sci gov` で **sci だけ起動し、gov について何も言わない**。
`powershell -File` 経由だと `[string[]]$Only` に最初の1つしか束縛されない。
カンマ・空白どちらでも動くようにし、知らない名前は警告を出すようにした。

### ⑦ 「レーンを止めた」が嘘だった

`Name='python.exe'` だけを見ていたが、sci と gov は **`python3.11.exe`**（`py.exe` 経由）で
8月2日から動いていた。私が数えていた `py.exe` は CPU 0秒の起動スタブ。

**そのsciがゲート導入前のコードで、削除した直後の住所録を再ダウンロードしていた。**

さらに `Win32_Process | Where CommandLine -match 'ingest_gov'` は
**自分自身のコマンド文字列にヒットする**（pwshが自分を数える）。除外が要る。

### ⑧ 会議中継が全ゲートを通過していた

1.4GB のダウンロードが止まっているのを見て中身を確認したら、
ワシントン州エナムクロー市の**議会本会議**だった。

```
ia × government_buildings  704点 → うち議会中継・公聴会 646点 / 375 GB
```

**アーカイブ棚の容量の半分以上**が、2時間ずっと固定カメラで壇上を映した映像。
関連度は「city council chambers」で高得点、技術基準は1080pで合格、ライセンスは完全にパブリック。
**「絵として使えない」を測る仕組みがどこにも無かった。**

判定を「主題」でなく**形式**（記録された議事そのもの）にして444件/286GBを削除、
4レーン全部の取り込み時に遮断。記録映像は残る
（1936年の議事堂、WW2期のワシントン、ホームムービー）。

**最初のdry-runは使える素材40点を巻き込むところだった。** Pixabayの題名はタグの羅列なので
`podcast` `webinar` `zoning` がマイクの寄り・黒板・暗い抽象画に当たっていた。
用語を削り、50MBの下限を足した（2時間の議事録画が3MBのはずがない）。

---

## 9. 権利・BANリスクで見つけたもの

| 見つけたもの | 件数 | 対処 |
|---|---:|---|
| AI生成と自己申告している素材 | 1,003 | 隔離。`ai generated, police, patrol, officer` のような**合成の警察映像**を含む |
| 実在政治家の報道写真 | 32 | 隔離。差押えテーマに現職政治家の顔写真が汎用b-rollとして入っていた |
| COVID陰謀論の放送 | 2 | 隔離。Stew Peters / Carrie Madej。USAFの音速実験の隣に並んでいた |
| 現行権利物を pd/cc0 と誤記 | 6 | 隔離。The Wiggles 2本・ABC For Kids 3本・Nintendo® 1本（2.5GB） |
| スター・ウォーズ画像 | 6 | 隔離 |

**factory 棚（88,963点）は一度も検査されていなかった。** ツールが `factory.jsonl` を
明示的に除外していた。検索が最も多く返す棚なのに。対象に含めて81件を隔離。

`depopulation` は**あえてルールに入れていない** — 過疎地のブランコの写真4枚に一致するため。

---

## 10. 他スレへの申し送り（担当外だが影響がある）

### 出荷ゲートは素材の解像度を見ていない

`check_final_acceptance.py` は**完成した動画**を測る（`MIN_VIDEO_W, MIN_VIDEO_H = 1920, 1080`）。
素材側は誰も測っていない。

**640x480の記録映像を1080pのタイムラインに引き伸ばして並べた作品は、ゲートを通る。**

索引は `(source:id)` で引けるので、組み立て側から読める:

```python
import json
R = json.load(open(r"H:\pd-media\assets\archive\_ledger\video_resolution.json", encoding="utf-8"))
wh = R.get(f"{source}:{item_id}")     # {"w":1920,"h":1080} or None
```

### 却下素材・判定の参照先

`film.json` を組む側は、素材を選ぶ前に判定を読むこと。

```python
# unusable の theme×source は使わない
verdicts = {}   # _qc/archive_verdicts.jsonl を (theme,source) -> verdict で読む
```

`search_archive.py` は既に読んでいるので、**検索経由で選んだものは安全**。
台帳を直接舐めて選ぶコードは危ない。

### factory 棚のラベルは今も壊れている

PD_CANON §7-22 の通り。**ただし 88,740点すべてを提供元の実題名にリネーム済み。**

```
AF-BG-0001__dark_cinematic_background.jpg -> pexels__9665187__white-dust-particles-on-black-background.jpg
AF-BG-0002__dark_cinematic_background.jpg -> pexels__13111752__blurred-lights-at-dusk.jpg
AF-TEX-0005__grunge_texture_dark.jpg      -> pexels__18541761__texture-school-chalk-chalkboard.jpg
```

旧名は**ダウンロードに使った検索語**であって中身ではなかった。`factory.jsonl` には
提供元の実題名が最初から入っていたので、これは推測でのラベル付け直しではなく、
既にある値をファイル名に写しただけ。

**ファイル名は真実になったが、テーマフォルダの割り当ては直っていない。**

---

## 11. 作ったもの一覧

| ファイル | 役割 |
|---|---|
| `scripts/shelf.py` | **「棚とは何か」の唯一の定義。**新しく数えるコードは必ずこれを使う |
| `scripts/build_absent_index.py` | 削除・隔離された台帳行の索引（台帳は書き換えない） |
| `scripts/check_shot_coverage.py` | 3チャンネル×20ショットで「話が組めるか」を測る |
| `config/shot_coverage_shots.v002.json` | そのショット一覧。v001からの言い換え表と、本当に足りない2件 |
| `scripts/qc_audio_stats.py` | 音声を客観指標で判定。playlistも出す |
| `scripts/build_video_resolution_index.py` | 全動画の解像度を実測して索引化（再開可能） |
| `scripts/purge_meeting_recordings.py` | 議事録画の削除。取り込み側と同じ語彙を共有 |
| `scripts/purge_unusable.py` | オーナー判定 unusable の削除（墓標にsource_urlを残す） |
| `scripts/qc_archive_contact_sheets.py` | ラベル付きシート。`--source` 追加済み |
| `scripts/quarantine_ban_risk.py` | BANリスク隔離。`ai-generated` `medical_misinformation` 追加済み |
| `episodes/_planning/SHELF_COVERAGE_AND_GAPS.v002.md` | カバレッジの詳細と、言い換えの根拠 |
| `episodes/_planning/ARCHIVE_SHELF_INVENTORY.v001.md` | テーマ×ソースの在庫表（判定付き） |

---

## 12. まだ終わっていないこと

1. **音声の判定は標本**（各組60本・計300本）。全8,635本を測ったわけではない
2. **AI生成の検出は自己申告分だけ。** タグに書いていないものは残っている
3. **ia レーンだけ稼働中。** 他は枯渇。ia は80%がSD・大半が `review_required` なので、
   増やす価値は低い。止めるかどうかはオーナー判断
4. **出荷ゲートの素材解像度検査**（§10）— 組み立てスレの担当
5. **factory 棚のテーマ割り当て** — ファイル名は直したがフォルダは未修正
