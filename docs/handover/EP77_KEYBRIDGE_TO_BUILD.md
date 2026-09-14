# EP77 keybridge → 組み立てスレへ

差出: 設計レーン（EP77–85）／2026-08-27
引き渡し条件: `docs/PD_HANDOFF_FROM_DESIGN_THREAD.v001.md`

---

## 引き渡し条件を満たしました

```
$ py -3.11 scripts/check_episode_inputs.py --slug keybridge
[inputs] keybridge: READY to build
```

## 中身（2026-08-27 実測）

| | |
|---|---|
| プレート | **128枚** 3840×2160、深度マップ128枚 |
| モーション（i2v） | **128本**。media master とバイト全数一致、`*_depth` 混入 0 |
| 実写 | **42本** |
| 動く素材の合計 | **170本**（ビルダーが要求する約110本を超過） |
| ナレーション | 358チャンク / 27.1分 |
| filmconfig | `episodes/_planning/EP77_keybridge_filmconfig.v001.json`（71カード、`figure_spec` PASS） |
| youtube_meta | `09_package/youtube_meta.v001.json`。`check_packaging_claims --package` = claim 121・hard fail **0** |
| プレート判定 | 128枚すべて verdict あり、sha256 に bind、binding=**exact** |
| 実写判定 | 42本すべて verdict あり、binding=**exact** |
| `check_motion_saturation` | **exit 0**（128本測定・色落ち0・黒0） |

## そちらでやる手順

```
py -3.11 scripts/build_case_film_generic.py --config episodes/_planning/EP77_keybridge_filmconfig.v001.json
# → remotion/src/data/keybridge_film.json

# remotion/src/Root.tsx に Ep77KeyBridge を登録
# compositions/KeyBridgeFilm.tsx を LahainaFilm.tsx と同じ形で作り、
# '../data/keybridge_film.json' を import してください
```

**Root.tsx の登録はこちらでやっていません。** film.json が無い状態で登録すると
バンドル全体が壊れるためです。film.json ができた直後にそちらで入れてください。

---

## 1. AEカードが6枚あります（組み込み方の相談）

`remotion/public/keybridge/ae/` に **透過webm 6本**（VP9 + alpha、`alpha_mode=1` 検証済み）。

| id | 種類 | 中身 | 秒 |
|---|---|---|---|
| `keybridge_ae001` | 大きい数字 | **01:27:53** ＋ THE ORDER TO STOP THE TRAFFIC | 8.0 |
| `keybridge_ae003` | タイトル | **26 MARCH 2024** | 7.5 |
| `keybridge_ae005` | 大きい数字 | **01:25** ＋ THE FIRST BLACKOUT UNDER WAY | 8.0 |
| `keybridge_ae010` | 箇条書き | 起訴の4罪状（1つずつ出る） | 10.0 |
| `keybridge_ae012` | 大きい数字 | **68** ＋ BRIDGES THE NTSB SAID TO GO AND CHECK | 8.0 |
| `keybridge_ae013` | 引用 | 司法省の推定無罪の一文（**全文・省略なし**） | 10.0 |

タイミングは `scripts/ae/jobs_keybridge.json` の `act` / `beat` にあります。
**組み込み方が決まっていなければ教えてください。**こちらで filmconfig 側に載せる形にもできます。

残り8枚（比較・年表・系統図・地図・書類拡大）はAE側の部品が無いので**作っていません**。
同じ内容は Remotion 側のカード（filmconfig の71枚）でカバーされています。

## 2. 判定で落としたものは全部 `rejected/` に退避済み

- `img/rejected/` に **19枚**
  - 16枚 = 時代ずれ（2024年の港なのに蒸気タグ・真鍮のテレグラフ・木製コーン・吊り橋）。
    差し替えの H132–H147 が本編に入っています
  - 3枚 = H062 / H065 / H084。i2v が「色で始まり灰色で終わる」不良を検出して除外したもの。
    `config/footage_blocklist.v001.json` にも登録済みなので、ビルダーが拾うことはありません

## 3. そちらに必ず伝えておくこと

**i2v は元プレートに無い人物を生成します。** i2v レーンの実測で、初回112本中**30本（27%）**で発生し、
全部作り直して解消を確認しています。ただし**検出は人の目だけ**で、機械の検出器はありません。
`check_motion_saturation` は色しか測らないので緑のままでした。

**→ レンダー後の shipped frames を読むとき、「この人はプレートにいたか」を見てください。**
小さく写ったものの見落としはありえます。

もう1つ。**プレートに人が写っている絵に人物禁止ネガを使うと、元からいる人まで消えます**
（H146 で作業員の腕が消えた）。i2v レーンは「すでに写っている人はそのまま、新しい人だけ入れない」
に直しています。再生成を依頼する場合はこの区別を伝えてください。

## 4. 受入で赤が出ると分かっているもの（先に言っておきます）

`check_episode_inputs` の予報です。**止める性質のものではありません**が、
`release_deviations.v001.json` に記録が要ります。

| check | 実測 | 備考 |
|---|---|---|
| `runtime_band` | 約27.2分 | 宣言帯 [1740,1920]s を上回る。**尺は20分超ならOK**（オーナー決定 2026-08-25） |
| `asset_reuse` | 動く素材170 vs 約252カット → 約82本が再利用 | reuse≤2 の範囲内。棚は掘り尽くしています（EP77は候補181本を全画面で読んで採用32本＝歩留まり18%） |
| `footage_utilization` | — | 上と同根 |
| `sound_layers` / `probe_receipt` / `caption_format` / `padding` | — | レンダー後に決まるもの |

## 5. 境界

- **この時点で EP77 の所有権はそちらに移ります。** こちらは `img/` `factory/` `motion/` を
  もう触りません。判定台帳はいまのファイルのハッシュに bind されています
- 予約・投稿は公開レーンだけが行います
- 設計レーンは次に **EP81 station** に入ります（EP80 concordia は実写16本で確定、下記）

## 6. 参考: EP80 concordia の実写は16本で確定します（EP77とは別件）

棚の客船映像は**全部に会社名が読める**ため（Star Cruises / VIKING / SILJA / P&O /
Holland America Line）、実在の船を題材にした番組がその船を棚から取れません。
床40本に対し16本で、**宣言値は下げず不足として記録**します（オーナー決定 2026-08-27）。
EP80 の船は最初からプレート185枚で描いてあり、i2v がそれを動かします。
