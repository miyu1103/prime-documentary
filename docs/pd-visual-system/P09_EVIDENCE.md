# P09 EVIDENCE — C1版 PD Evidence Room（Blender）

- Phase `P09` / by claude-code / 2026-07-12 (JST)

## 実装（既存Blenderパターン再利用・invariant14）
- `remotion/src/blender/pd_evidence_room.py` = **再利用procedural 3Dセット**（毎回作り直さない）。既存 `bpp_eevee.py`（engine/lights/bloom/render）＋`aircash_cashstack.py`（_act_fcurves）に準拠。
- ARGV契約: `-- OUT RX RY FS FE SAMPLES [CAMERA]`。CAMERA∈{cam1_enter_room, cam2_push_desk, cam3_pan_board}（C1=固定/正面3カメラ）。
- セット: records desk(silver metallic)＋evidence board(dark frame＋**3枚 blank貼付スロット**=Remotion overlay対象)＋**MONITOR_SCREEN**(電光ブルー emissive)＋map table(発光)＋navy壁/反射床。ブランド照明(key/fill/rim area＋softbox・electric emission・フラット禁止)＋Glare bloom。**読める文書は焼かない**(invariant11)。

## 検証（実測・実レンダ目視）
```
blender -b -P pd_evidence_room.py -- <OUT> 1280 720 1 1 64 cam1_enter_room → WROTE（全景: ボード3スロット＋モニタ＋デスク＋地図面 目視OK）
blender ... 1 1 48 cam2_push_desk → デスク寄り 目視OK
blender ... 960 540 1 3 32 cam2_push_desk → f_0001..0003.png（3フレーム連番=アニメ検証・fcurvesクラッシュなし）
ENGINE=BLENDER_EEVEE / BLOOM ok / AgX
```
- 出力 `outputs/pd-visual-system/p09_check/{wide_test.png, test_test.png, smoke/f_000{1,2,3}.png}`。

## 受入基準（C1最小）
central desk＋evidence board＋map/verdict monitor＋basic lighting＋固定3カメラ ✅／再利用セット(episodeで作り直さない) ✅／読める偽文書なし ✅。

## rollback / 限界 / 次
- rollback: `pd_evidence_room.py`＋`p09_check/*` 削除。既存blender/remotionに非干渉。
- 限界: screen-corner export（移動CAM4/6のモニタ貼付用 world_to_camera_view）は未実装＝**固定カメラC1では不要**・移動カメラ導入時に追加（P09_PLAN §4）。セットは意図的にミニマル（詳細加飾は今後）。初回smokeがCWD相対で `C:\outputs\` に1枚出た（以降は絶対パス）＝要手動削除の軽微残骸。
- 次 P10 = C2版（AI動画Wan2.2・**数十GB DL=§10承認**）。
