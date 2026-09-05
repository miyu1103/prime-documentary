# EP50–56 MASTER HANDOFF (v002, 2026-07-29) — 実測で全面更新

v001 を**置き換える**。v001 には実測と食い違う記述が3つあり、そのまま着手すると調査をやり直すことになる。
Repo `C:\Users\aab15\Documents\prime-documentary`、Media `H:\pd-media`、branch `claude/vibrant-archimedes-2mmr5h`。

## 0. 最初にやること（1コマンド）

```
py -3.11 scripts/pd_preflight.py --all
```

文書ではなく**ディスクの実測**が正。あわせて `episodes/_planning/PD_FAILURE_REGISTRY.v001.md`（F-01〜F-18、各行に検出器と阻止点）を読む。

## 1. v001 の誤り（訂正済み）

| v001の記述 | 実測 |
|---|---|
| 「narration索引は全話未整備」 | **全6話完成済み**。`06_audio/narration_index.v001.json` は `is_stub=false`（実測タイミング）、ElevenLabs実音声マスターも `H:/pd-media/episodes/<EP>/06_voice/master/vc_master_v001.mp3` に存在（29〜43MB）。**TTS作業は不要** |
| 「EP52 morton が◎最良（i2v 71）」 | i2v実体は **43本**（残りはoverlay粒子）。かつ **staged factory 240本のうち227本が真っ黒動画**（11KB・2.6s・輝度1.0）で使用不可だった。共有ライブラリから245本を再調達して解決済み |
| 「EP50 AE黒はB8合成が原因」 | **誤診**。B8.mp4は黒フレーム0でクリーン、合成も正常動作。真因はAEカード36本中**18本が後半フリーズ・21本が輝度20未満**で、それを不透明・全画面で被せていたこと |

さらに v001 に記載のなかった実測事実:
- **P##顔が全話でpublicにあるのにマニフェスト未登録** → 映像に一度も出ない状態だった
- **EP51/EP53 は本編静止画S##がpublicに1枚も無かった**（顔だけ）→ 150枚/205枚を配置
- **EP56 の asset_manifest.v001 は存在しないファイル277件を参照**していた（使用不可）

## 2. EP50 = 完了

`08_edit/EP50_FINAL.mp4` = **v007_ae**（3.57GB / 3663.8s）。黒0・フリーズ0・ポストゲートPASS・ゲートフレーム40枚＋カード窓8箇所を目視確認済み。

修正方法（`scripts/ae/composite_hero_scrimkey.py`、全話で再利用可）: カードを不透明で被せるのをやめ、**本編を30%スクリムで残したまま、カードの暗背景を `lumakey` で抜いて重ねる**。これで黒判定（98%画素が輝度25.5未満）とフリーズ（下で本編が動き続ける）が同時に消える。

**オーナー判断待ち（急がない）**: カード表示中は本編の焼き込み字幕が暗く沈む。旧方式では完全に隠れていたので後退ではない。直すならスクリムから下部字幕帯を除外して再エンコード1回（1〜2時間）。

## 3. EP51–56 の実測状態（2026-07-29）

全6話 **film.json 構築済み・プリゲートPASS・Remotion配線済み**。

| EP | slug | comp id | カット | 実動画share | 図版 | 尺 | public dir |
|----|------|---------|-------|-----------|-----|-----|-----------|
| 51 | willingham | Ep51Willingham | 263 | 0.681 | 57 | 20:29 | public_ep51 |
| 52 | morton | Ep52Morton | 388 | 0.680 | 82 | 30:06 | public_ep52 |
| 53 | norfolk | Ep53Norfolk | 364 | 0.681 | 78 | 28:14 | public_ep53 |
| 54 | flowers | Ep54Flowers | 372 | 0.680 | 80 | 28:51 | public_ep54 |
| 55 | burge | Ep55Burge | 380 | 0.682 | 84 | 29:30 | public_ep55 |
| 56 | postoffice | Ep56Postoffice | 384 | 0.682 | 88 | 29:46 | public_ep56 |

**i2vはボトルネックではない。** 監査済みライブラリから実写を230〜258本/話ステージングしたことで、i2vゼロでも motion-first（実動画68%）を満たす。i2vは人物モーションの上乗せ（品質向上）であって前提条件ではない。EP51のM元は5/30完了で中断中（`ae-demo/wan_frames_willingham_*`、再開は安全）。

## 4. 正規手順（これ以外でやらない）

```
py -3.11 scripts/pd_preflight.py --slug <slug>                      # 着手前
py -3.11 scripts/stage_factory_for_episode.py --slug <s> --exclude-used --plan <theme:n,...>
py -3.11 scripts/build_asset_manifest_motionfirst.py --slug <s>     # publicを実スキャン+実輝度検査
py -3.11 scripts/build_case_film_generic.py --config episodes/_planning/EP<NN>_<s>_filmconfig.v001.json
py -3.11 scripts/build_render_public_dir.py --slug <s>              # ハードリンク・スリムdir
bash scripts/pd_render_guarded.sh <CompId> <film.json> <public_epNN> out/<s>.mp4 <expect_sec>
py -3.11 scripts/build_case_bgm_generic.py --slug <s> --render out/<s>.mp4 --out <08_edit/...v001.mp4>
py -3.11 scripts/pd_postrender_gate.py <final.mp4> --expect-sec <n> --frames 40 --out out_qc/qc_frames_<s>
# 最後に必ず自分で全編を見る。自己申告の「完成」は禁止
```

連続レンダーは `scripts/pd_render_queue.sh <slug> ...`（直列・各話ゲート付き）。
**ただし1本を見て品質を確認するまでキューを流さない**（ship-then-inspect の再発になる）。

## 5. i2v が必要になったとき

```
py -3.11 scripts/pd_gpu_lock.py i2v
bash scripts/_chain_i2v_robust.sh <slug> <target> M 8      # チャンク毎に新ComfyUI
py -3.11 scripts/pd_watchdog.py --glob "C:/Users/aab15/ae-demo/wan_frames_<slug>_*" --target N --stall-min 12
```
実測 **1本206秒**。ComfyUIは数本ごとに落ちるのでチェーンとwatchdogを必ず併走させる。GPUは常に1ジョブ（レンダーとi2vは排他）。

## 6. まだ手を付けていないこと

- 各話のAEヒーローカード（`08_edit/ae_hero/beats.json` + AEレンダー）。合成は `composite_hero_scrimkey.py` で統一。**合成後は必ず別途ポストゲート**
- サムネイル / パッケージ（タイトル・説明文）
- **スケジュール・公開はしない。最終確認はオーナー**
