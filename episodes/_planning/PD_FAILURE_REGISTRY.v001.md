# PD 失敗レジストリ v001 — 「散在する注意点」を1本にまとめた正典 (2026-07-29)

オーナー方針: **時短ではなく最高品質＋失敗ゼロ**。ただし churn（無意味なやり直し）はしない。
このファイルは、これまで別々の場所（記憶・引継ぎ文書・retro・ADR）に散っていた再発防止事項を
**1本の表**に統合したもの。原則は [[feedback-lessons-must-be-gates]]:
**約束や記憶に頼らない。守れなければ処理が物理的に止まる機械ゲートにする。**

**入口はこの1コマンド:**

```
py -3.11 scripts/pd_preflight.py --all          # 着手前・全話の建設可否を実測で判定
py -3.11 scripts/pd_preflight.py --slug flowers # 1話だけ
```

`--fast` はフレーム復号を省く高速版。**黒動画（F-14）を検出できない**ので、レンダー直前の最終判断には使わない。

---

## 1. 失敗 → 検出器 → 阻止される場所

「実績」列は、その失敗が実際に起きたエピソード。理屈ではなく計測で確認済みのものだけを載せる。

| # | 失敗 | 根本原因 | 機械検出 | 阻止点 | 実績 |
|---|------|---------|---------|--------|------|
| F-01 | 6hレンダー**後**に紙芝居/ワープ/4行字幕/反復画像が判明→全部やり直し | 品質検査がレンダーの後だった | `pd_prerender_gate.py` | exit 1 = レンダー禁止 | EP50 (v001→v006) |
| F-02 | 再i2vでVRAM枯渇→ComfyUIサイレントクラッシュ | webUIとComfyUIの同時GPU使用 | `pd_gpu_lock.py i2v` | exit 1 = i2v開始禁止 | EP50 |
| F-03 | ジョブが無言で停止、聞かれるまで気づかず | 監視なし | `pd_watchdog.py` | ALERT＋自動再起動 | EP50 |
| F-04 | フレーム1枚で「完成」判定→通しで見たら欠陥6件超 | 通し視聴の省略 | `pd_postrender_gate.py` ＋ **人間の全編視聴** | exit 1 = 見せる禁止 | EP39-41 |
| F-05 | 90秒超のジョブを前景実行→2分でkill→部分ファイル量産 | 前景実行 | 運用（`run_in_background`必須） | — | EP50 |
| F-06 | i2vのskip判定が存在しないパスを見ていた→毎回ゼロからやり直し | 出力先を検証せず信用 | `i2v_episode_batch.py` が実出力 `wan_frames_<slug>_<stem>/` を見る | 正しく再開 | EP50 |
| F-07 | v001を読むビルダーにv003を渡して混乱 | versioned成果物の読み手を更新漏れ | 運用（再生成したら読み手を全grep） | — | EP50 |
| F-08 | 3hレンダー未着手なのに「あと4h」と回答 | 最大の未着手工程を見積りから落とした | 運用（見積りは最大の未着手工程基準・控えめに） | — | EP50 |
| F-09 | AE合成が黒6秒＋フリーズ8秒を混入（ベースは正常） | 合成後にゲートを掛けていなかった | 合成後に**別途** `pd_postrender_gate.py` | exit 1 = 見せる禁止 | EP50 |
| F-10 | GPU連続稼働でWanが8〜30本ごとにハードクラッシュ | VRAMリーク | `_chain_i2v_robust.sh`（チャンク毎に新ComfyUI＋lock＋watchdog） | 自動復旧 | EP50 |
| F-11 | 同じチェーンを二重起動→ログ混線・二重キュー | 単一インスタンス保証なし | `_chain_i2v_robust.sh` のlockfile | 二重起動を拒否 | EP50 |
| **F-12** | **AEヒーローカードが暗黒＋静止のまま本編を全画面で覆う** | カードを不透明で被せる方式。36本中**18本が50%以降フリーズ・21本が輝度20未満** | `pd_postrender_gate.py`（黒/フリーズ）＋ 合成方式を `composite_hero_scrimkey.py` に変更 | exit 1 ＋ 方式で根治 | **EP50（本日計測）** |
| **F-13** | **マニフェストが存在しないファイルを参照** | マニフェストの主張を検証せず信用 | `build_asset_manifest_motionfirst.py`（publicを実スキャン）＋ `pd_preflight.py` B | BLOCK | **EP56 postoffice（motion42/factory235が全部不在）** |
| **F-14** | **ステージ済みfactory動画の中身が真っ黒** | サイズ検査だけでは足りない（11KB・2.6s・輝度1.0） | マニフェスト生成時に**実フレーム輝度**を測定し除外/降格 | プールから除外 | **EP52 morton（240本中227本が黒）** |
| **F-15** | **P##顔がpublicにあるのにマニフェストに無く、映像に一度も出ない** | 静止画スキャンがP##接頭辞を拾っていなかった | マニフェスト生成が `img/P*`,`img/F*` を people ロールへ ＋ `pd_preflight.py` C | BLOCK | **EP52/EP54（各16枚が未参照）** |
| **F-16** | **UTF-8のJSONがcp932で読めずクラッシュ** | Windows既定エンコーディング | 全スクリプトが `encoding="utf-8"` 明示＋`sys.stdout.reconfigure` | 誤った exit 0 を防ぐ | 本日・過去にゲートで偽PASSの実績 |
| **F-17** | **引継ぎ文書の記述がディスクの実態と食い違う** | 文書を検証せず着手 | `pd_preflight.py` を**着手前に**実行して実測で上書き | 前提の誤りを初手で検出 | **本日（EP51-56のナレーション「未整備」は誤り＝実際は全話完成）** |
| **F-18a** | **レンダー開始時にpublicディレクトリ56GBをコピーし続けて進まない** | `--public-dir` に共有の `remotion/public` を渡した。Remotionはその**全体**をバンドルへコピーするので、他話の素材も落選素材（flowersの`rejected/`37GB）も巻き込む | レンダーは**話専用のスリムdir** `remotion/public_ep<NN>/` に対してのみ行う | コピー量 56GB→約8GB | **本日 EP54（1回中止）**。EP50が`public_slim`を使っていたのはこの為 |
| **F-18b** | **スリムdirを作ったのに全画像が `EncodingError: source image cannot be decoded`** | スリムdirを**ジャンクション/シンボリックリンク**で作った。Pythonのチェックはリンクを辿るので「存在する」と言うが、**Remotionのpublicコピーは辿らない**→バンドルに入らず404。ゲートが通ってレンダーが死ぬ最悪の組み合わせ | スリムdirは**ハードリンク**で作る（実体複製なし・コピーからは実ファイルに見える）。`pd_prerender_gate.py` 検査7がreparse pointを検出してFAIL | exit 1 | **本日 EP54（2回目の中止）** |
| **F-18c** | **240フレームまでレンダーしてから `banner_sunrise.png` 404 で落ちる** | film.jsonに現れない**リテラル参照のブランド資産**（banner・フォント3種）をスリムdirに入れ忘れた。film.jsonのsrcだけ検査しても捕まらない | `pd_prerender_gate.py` 検査8が `banner_sunrise.png` とフォント3種の実在を必須化 | exit 1 | **本日 EP54（3回目の中止）** |

## 2. 唯一の正規レンダー手順（これ以外でレンダーしない）

```
scripts/pd_render_guarded.sh <compId> <film.json> <public_dir> <out.mp4> <expect_sec>
```

内部で自動的に **[1]プリゲート（不合格→中止）→[2]GPU占有チェック→[3]レンダー→[4]ポストゲート（不合格→見せない）**。
ゲートがパスの上に無ければ何も守らない（EP50はビルダーを直接叩いてゲートを迂回した）。

## 3. 正規手順まとめ

| 工程 | コマンド | 備考 |
|------|---------|------|
| 着手前チェック | `pd_preflight.py --all` | **最初に必ず** |
| マニフェスト | `build_asset_manifest_motionfirst.py --slug <s>` | publicを実スキャン・黒素材を降格 |
| film.json | `build_case_film_generic.py --config <cfg>` | 汎用1本。話ごとにクローンしない |
| i2v | `_chain_i2v_robust.sh <slug> <target> <kinds> <chunk>` | GPUは常に1ジョブ |
| レンダー | `pd_render_guarded.sh ...` | 唯一の正規経路 |
| AE合成 | `ae/composite_hero_scrimkey.py` | 合成後に**必ず**ポストゲート |
| 最終 | `pd_postrender_gate.py` ＋ **全編視聴** | 自己申告の「完成」は禁止 |

## 4. ゲートで担保しきれない運用不変ルール

1. **90秒を超える見込みのジョブは必ずバックグラウンド。** 前景は2分で殺され、部分ファイルを残す。
2. **カウント・スキップ・進捗は、実際の出力パスを確認してから信用する。** 道具の自己申告は証拠ではない。
3. **versioned成果物を作り直したら、その読み手を全部grepして向き先を確認する。**
4. **見積りは最大の未着手工程を基準に、控えめに出す。**
5. **GPUは常に1ジョブ。** i2v ↔ SDXL ↔ レンダーは `pd_gpu_lock.py` で直列化。
6. **ship-then-inspect 禁止。** 欠陥は全部洗い出してから**1回**のレンダーで直す。
7. **オーナーに見せる前に、自分でオーナー基準を1周する**（字幕サイズ／フック8秒先頭／OP-ED／非静止／素材被り／切りの良い終わり）。
8. **スケジュール・公開はしない。** 最終確認はオーナー。

## 5. 品質フロア（数値・全部機械判定）

- 実動画share **≥0.62**（ビルダーは0.68を狙って余裕を取る）／ 静止画は再利用0回・動画は最大2回
- distinct src比 **≥0.50**／同一src再利用 **≤3**
- 字幕 **≤84字＝2行**／ワープ系treatment（depth・scan・card）**禁止**
- 図版kindは正規union限定・**dochighlight禁止**／YEARのnumbertickerは `group:false`
- 黒連続 **>1.2s でFAIL**／フリーズ連続 **>4.0s でFAIL**／尺は想定±8秒
- 素材は 50KB以上 **かつ** 実フレーム輝度 **≥8**
- フック: 1文・平叙・人物＋固有の数値/日付・**疑問文禁止**（勝ち筋26本中0本が疑問文で開始）

## 6. 出典

記憶 `feedback-no-render-churn` / `feedback-lessons-must-be-gates` / `feedback-verify-dont-assume` /
`feedback-top-1-percent-not-average` / `pd-retention-rules` / `pd-opening-formula` / `pd-craft-checklist`、
`episodes/_planning/PD_IRONCLAD_GATES.v001.md`、`EP50-56_MASTER_HANDOFF.v001.md`、
および 2026-07-29 の実測（F-12〜F-17）。
