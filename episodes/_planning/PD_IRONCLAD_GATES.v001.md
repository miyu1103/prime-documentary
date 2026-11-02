# PD 鉄壁ゲート — 同じ失敗を"仕組み"で二度と繰り返さない (v001, 2026-07-28)

オーナー指示:「確実に同じことを繰り返さない鉄壁の対策」。約束・記憶に頼らず、**守れなければ処理が物理的に止まる機械ゲート**を実装した([[feedback-lessons-must-be-gates]]の原則を全面適用)。以後、全エピソード(EP50-55+)はこのゲートを通す。

## これまでの失敗 → それを止める機械ゲート(実装済み・実行可能)

| # | 過去の失敗(実際に起きた) | 根本原因 | 鉄壁ゲート(コード) | 不合格時の挙動 |
|---|---|---|---|---|
| 1 | 6hレンダー**後**に紙芝居/ワープ/顔なし/実写ゼロ/4行字幕/反復画像を発見→全部作り直し | 品質検査がレンダーの"後"だった | `pd_prerender_gate.py` (film.json+public を検査) | **exit 1 → レンダー実行禁止** |
| 2 | 再i2vでVRAM枯渇→ComfyUIサイレントクラッシュ | webUIとComfyUIの同時GPU使用(直列化違反) | `pd_gpu_lock.py i2v` (webUIアンロード+空きVRAM≥15GB検証) | **exit 1 → i2v開始禁止** |
| 3 | ジョブが無言で停止、オーナーに聞かれるまで気づかず | 監視なし・液性(liveness)確認なし | `pd_watchdog.py` (出力停滞+GPUアイドルを検知→ComfyUI強制再起動) | ALERT記録+自動再起動 |
| 4 | 完成品をフレーム1枚で「完成」判定→通しで見たら欠陥6+ | 通し視聴を省略 | `pd_postrender_gate.py` (黒/フリーズ/無音/尺をffmpegで検査+全編フレーム抽出) | **exit 1 → オーナーに見せる禁止** |
| — | クラッシュしても走り続けた「つもり」 | 例外時に誤って合格扱い | 全ゲート **fail-closed**(例外=FAIL exit1) + UTF-8強制 | 落ちたら必ずFAIL |

## 唯一の正規レンダー手順(これ以外でレンダーしない)
```
scripts/pd_render_guarded.sh <compId> <film.json> <public_dir> <out.mp4> <expect_sec>
```
内部で自動的に: **[1]pre-renderゲート(不合格→中止)→[2]GPU占有チェック(i2v稼働中→中止)→[3]レンダー→[4]post-renderゲート(不合格→見せない)**。

## 生成/i2v の正規手順
- SDXL開始前: `py -3.11 scripts/pd_gpu_lock.py sdxl`
- i2v開始前: `py -3.11 scripts/pd_gpu_lock.py i2v`(webUIアンロード+VRAM検証、exit1なら開始しない)
- 長時間i2v/genには必ずウォッチドッグを併走:
  `py -3.11 scripts/pd_watchdog.py --glob "<出力dir glob>" --target N --stall-min 8`
- 長時間チェーンは自動再起動リトライ付きで組む(例 `_chain_ep50_rei2v_robust.sh`: ComfyUIダウン検知→VRAM解放→再起動→バッチ再開、最大12回)。

## pre-renderゲートが機械判定する項目(EP50実測でキャリブレーション済み)
- **モーションファースト**: 実動画(.mp4=i2v+実写stock)の割合 ≥ 0.62 (紙芝居防止)。static画像がこれを割ると即FAIL。
- **ワープ/走査線禁止**: treatment に `depth/scan/card` があればFAIL。
- **反復防止**: distinct src比 ≥ 0.50、同一srcの再利用 ≤ 3回。
- **字幕2行以内**: 84字超 or 推定3行以上でFAIL。
- **アセット健全性**: 参照srcが全て存在・黒スタブ(<50KB)でない・near-black(luma<8)でない。動画は尺>0。
- **ナレーション**参照の存在確認。

## post-renderゲートが機械判定する項目(最終mp4)
- 尺が想定±8秒以内 / 音声ストリーム有り。
- 黒フレーム連続 > 1.2秒 → FAIL(チラつき/ギャップ)。
- フリーズ連続 > 4秒 → FAIL(紙芝居/静止)。
- 中間の無音 > 3秒 → WARN(イントロ/アウトロ以外なら要確認)。
- 全編を等間隔で30フレーム抽出 → **私が通しで確認**(フレーム抽出はゲート、通し視聴は別途必須)。

## 不変ルール(ゲートで担保しきれない分は運用で)
1. **レンダー前に必ず pre-renderゲート PASS**。落ちたら直してから。
2. **オーナーに見せる前に post-renderゲート PASS + 全編通し視聴**。
3. **GPUは常に1ジョブ**。i2v↔SDXL↔レンダーは gpu_lock で直列化。
4. **落ちても自走**: robustチェーン+ウォッチドッグで無人復旧。停滞は仕組みが検知する。
5. これらは全て git 管理。どのセッション(私が忘れても)も同じ手順を強制される。

## キャリブレーション出典
`remotion/src/data/centralpark_film.json`(EP50 motion-first合格ビルド): cuts=599, 実動画share=0.71, distinct=0.656, 最大再利用2×, 字幕最長84字, treatment=bleed/duotone/focus(ワープ系0)。閾値はこの合格値から安全側に設定。
