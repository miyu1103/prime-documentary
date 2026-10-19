# P09 PLAN — PD Evidence Room（設計のみ・実行はP09到達後）

> エージェント調査(2026-07-12)。**実行しない**（現在P06）。skill/rule/registryは既存(`.claude/skills/pd-phase-09-evidence-room`,`.claude/rules/blender-evidence-room.md`)。

## 方針（invariant14＝既存パターン再利用）
- 既存 `remotion/src/blender/` に16本の手続きスクリプトあり。**CLI規約を踏襲**: `blender -b -P <script> -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES> [CAMERA]`。`.blend`はコミットしない（手続きpy正・保存は成果物）。
- **fcurves 5.x罠は解決済**: `_act_fcurves()`ヘルパー(`aircash_cashstack.py:30`)を**逐語コピー**（無いとカメラeasingのseqレンダで落ちる）。EEVEE Next＋AgX＋Glare bloom。5.xは動画出力廃止→PNG連番→別encode。
- **読める文書/判決文をBlenderに焼かない**（invariant11）。テキスト/図/資料はRemotion合成。

## パイプライン（既存）
Blender PNG連番 `out/evroom/<cam>/f_%04d.png` → `npx remotion ffmpeg -i ... -c:v libx264 -crf16 -pix_fmt yuv420p -vf scale=1920:1080:lanczos` → `remotion/public/_set/evroom/<cam>.mp4` → Remotion `OffthreadVideo`。NVENC禁止・serial・tailで隠さない。

## 実装（新規・上書きなし）
- `remotion/src/blender/pd_evidence_room.py`（1本のprocedural build_room()＋camera引数）。`pd_evidence_room_cameras.json`（カメラmanifest）。
- オブジェクト: floor(metallic)/navy壁/records desk(silver)/evidence board(空panel=Remotion貼付)/verdict monitor(emissive `MONITOR_SCREEN`)/relationship screen/map table/court-hierarchy panel/timeline wall/chapter screen/照明rig/薄いvolumetric haze。
- ブランド配色: world暗navy / navy#0B1A2B matte / electric#1F6BFF=emission&rim(フラット禁止) / silver#C8CDD6 metallic0.85 / gold#E5B53A控えめ。key/fill/rim AREA。cam8で照明+emissionを15%へ減光(keyframe+_act_fcurves)。
- **8カメラ**（C1先行＝CAM1-3 固定/正面）: 1入室 2デスク寄り 3ボードpan 4モニタ寄り(**corner export**) 5地図真上 6判決へ接近(corner export) 7引き 8減光終章。

## screen-corner export（net-new・移動カメラへの貼付に必須）
- 同スクリプトで `MONITOR_SCREEN` の4隅頂点を `bpy_extras.object_utils.world_to_camera_view(scene,cam,world_co)`→ `px=u*RX, py=(1-v)*RY`(top-left)→ フレーム毎JSON `public/_set/evroom/<cam>.corners.json`。
- Remotion側は quad→quad homography で CSS `matrix3d`（**新規util**・motionkit presetとして・fork禁止）。**移動CAM4/6へは corners JSON 無しに貼らない**（rule）。

## 検証 / コスト
- **3フレーム連番で検証**（単フレームstillはseqバグを見逃す）。
- EEVEE Next 1080p ≈ 2-4s/frame → 8カメラ計≈1時間（承認不要枠）。Cycles 4K ≈ 30-44s/frame＝多時間/>5GB＝**§10 owner承認**。

## 参照
`aircash_cashstack.py`(fcurves/camera keyframe)・`tyler_equitytheft_map.py`(aerial/haze/floor/bloom)・`EP35_hinders_RENDER_RUNBOOK.v001.md`(batch model)。phase到達まで実行禁止。
